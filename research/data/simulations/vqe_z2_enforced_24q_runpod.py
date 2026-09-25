"""
SIM-2026-006: Z2-enforced 5-layer 24q MERA VQE — RunPod A100 version
Targets HYP-2026-002: holographic force verification

Uses cupy for GPU-accelerated sparse mat-vec (the bottleneck).
Circuit simulation via qiskit-aer (GPU if available, CPU fallback).

Setup on RunPod:
  pip install qiskit qiskit-aer-gpu cupy-cuda12x scipy
  python vqe_z2_enforced_24q_runpod.py

Expected runtime: ~2-3 hours on A100 80GB (~$3-4)
"""
import numpy as np
import time, json, sys
from scipy.optimize import minimize, curve_fit
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

# GPU sparse math
import cupy as cp
import cupyx.scipy.sparse as cpsparse

# Qiskit
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-006: Z2-enforced 5-layer 24q MERA VQE (RunPod A100)")
print("=" * 65, flush=True)

# ── GPU info ──
print(f"  cupy version: {cp.__version__}")
dev = cp.cuda.Device(0)
try:
    gpu_name = dev.attributes.get('DeviceName', str(dev))
except Exception:
    gpu_name = str(dev)
print(f"  GPU: {gpu_name} ({dev.mem_info[1] / 1e9:.1f} GB)")
print(flush=True)

NQ = 24
NLAYERS = 5
HOLOGRON_ANGLE = np.pi / 3
T_GLOBAL = time.time()

# ── Z2 parity projection (GPU) ──
PARITY_MASK = (1 << NQ) - 1
PARITY_INDICES_GPU = cp.arange(1 << NQ, dtype=cp.int64) ^ PARITY_MASK


def parity_project_gpu(sv_gpu):
    """Project statevector onto P=+1 sector, on GPU."""
    sv_plus = sv_gpu + sv_gpu[PARITY_INDICES_GPU]
    norm = cp.linalg.norm(sv_plus)
    if float(norm) < 1e-15:
        print("  WARNING: state entirely in P=-1 sector!", flush=True)
        return sv_gpu
    return sv_plus / norm


def parity_expectation_gpu(sv_gpu):
    """<P> on GPU."""
    return float(cp.real(cp.sum(sv_gpu.conj() * sv_gpu[PARITY_INDICES_GPU])))


# ── Build MERA circuit ──
def build_mera(nq, nlayers):
    qc = QuantumCircuit(nq)
    params = []
    pidx = 0
    for layer in range(nlayers):
        step = 2 ** layer
        for i in range(0, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp.append(p)
                    pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp2.append(p)
                    pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
        for i in range(step, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp.append(p)
                    pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp2.append(p)
                    pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
    return qc, params


qc_template, params = build_mera(NQ, NLAYERS)
NP = len(params)
print(f"Params: {NP}, depth: {qc_template.depth()}", flush=True)

# ── Build Hamiltonian on CPU, transfer to GPU ──
def sparse_pauli(n, i, p):
    I2 = speye(2, format="csr")
    X = csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Z = csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
    ops = {"I": I2, "X": X, "Z": Z}
    mats = [ops[p] if k == i else I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_hamiltonian(n):
    H = csr_matrix((2**n, 2**n), dtype=complex)
    for i in range(n - 1):
        Zi = sparse_pauli(n, i, "Z")
        Zj = sparse_pauli(n, i + 1, "Z")
        H -= Zi @ Zj
    for i in range(n):
        H -= sparse_pauli(n, i, "X")
    return H


print("[1] Building Hamiltonian (CPU)...", flush=True)
t0 = time.time()
H_scipy = build_hamiltonian(NQ)
print(f"  H built on CPU: {time.time() - t0:.1f}s", flush=True)

# Exact ground state energy (cached — eigsh takes hours on this CPU)
E0 = -30.199712
print(f"  E0 = {E0:.6f} (cached)", flush=True)

# Transfer to GPU
print("  Transferring H to GPU...", flush=True)
H_gpu = cpsparse.csr_matrix(
    (cp.asarray(H_scipy.data), cp.asarray(H_scipy.indices), cp.asarray(H_scipy.indptr)),
    shape=H_scipy.shape,
)
print(f"  H on GPU: {H_gpu.nnz} nonzeros", flush=True)

# Z operators on GPU (for diagnostics)
print("[1b] Building Z operators on GPU...", flush=True)
Z_gpu = []
for i in range(NQ):
    z = sparse_pauli(NQ, i, "Z")
    Z_gpu.append(cpsparse.csr_matrix(
        (cp.asarray(z.data), cp.asarray(z.indices), cp.asarray(z.indptr)),
        shape=z.shape,
    ))
print(f"  {NQ} Z operators on GPU", flush=True)

# ZZ products on GPU (precompute for force profile)
print("[1c] Precomputing ZZ operators...", flush=True)
anchor = NQ // 4  # site 6
ZZ_gpu = {}
for dr in range(1, 9):
    site2 = anchor + dr
    if site2 < NQ:
        ZZ_gpu[dr] = Z_gpu[anchor] @ Z_gpu[site2]
print(f"  {len(ZZ_gpu)} ZZ operators precomputed", flush=True)


# ── Diagnostics ──
def diagnose_gpu(sv_gpu):
    mag = sum(
        float(cp.real(cp.dot(sv_gpu.conj(), Z_gpu[i] @ sv_gpu)))
        for i in range(NQ)
    ) / NQ
    par = parity_expectation_gpu(sv_gpu)
    return mag, par


# ── Simulator ──
try:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector", device="GPU")
    print("[2] Using qiskit-aer GPU backend", flush=True)
except Exception:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector")
    print("[2] Using qiskit-aer CPU backend (GPU not available)", flush=True)


def get_sv_gpu(theta_vec, project=True):
    """Run circuit, return statevector as cupy array on GPU."""
    qc = qc_template.assign_parameters(dict(zip(params, theta_vec)))
    qc2 = qc.copy()
    qc2.save_statevector()
    sv_np = np.asarray(sim.run(qc2).result().get_statevector())
    sv_gpu = cp.asarray(sv_np)
    if project:
        sv_gpu = parity_project_gpu(sv_gpu)
    return sv_gpu


def energy_z2(theta):
    """Energy with Z2 projection, mat-vec on GPU."""
    sv = get_sv_gpu(theta, project=True)
    Hsv = H_gpu @ sv
    return float(cp.real(cp.dot(sv.conj(), Hsv)))


# Warmup + benchmark
print("[2b] Warmup + benchmark...", flush=True)
theta_test = np.random.randn(NP) * 0.1

# Time individual components
t0 = time.time()
sv_test = get_sv_gpu(theta_test, project=False)
t_circuit = time.time() - t0

t0 = time.time()
sv_test = parity_project_gpu(sv_test)
t_proj = time.time() - t0

t0 = time.time()
Hsv = H_gpu @ sv_test
e = float(cp.real(cp.dot(sv_test.conj(), Hsv)))
t_matvec = time.time() - t0

t0 = time.time()
e_full = energy_z2(theta_test)
t_total = time.time() - t0

mag_t, par_t = diagnose_gpu(get_sv_gpu(theta_test, project=True))

print(f"  Circuit: {t_circuit:.3f}s  Projection: {t_proj:.4f}s  Mat-vec: {t_matvec:.4f}s")
print(f"  Total eval: {t_total:.3f}s  (vs ~3s local)")
print(f"  E={e_full:.4f}  <M>={mag_t:.4f}  <P>={par_t:.4f}", flush=True)

# Estimate total runtime
est_evals = 3 * 15000 + 2000  # 3 seeds + polish
est_hours = est_evals * t_total / 3600
print(f"\n  Estimated runtime: {est_hours:.1f}h ({est_evals} evals x {t_total:.2f}s)", flush=True)

# ── VQE ──
print(f"\n[3] Z2-enforced VQE: 3 seeds x 15000 evals (L-BFGS-B)...", flush=True)
best_E = 0.0
best_theta = None
seed_results = []

for seed_idx, seed in enumerate([7, 42, 99]):
    np.random.seed(seed)
    theta0 = np.random.randn(NP) * 0.3
    eval_count = [0]
    t_start = time.time()

    def make_callback(s, ts, ec):
        def cb(theta):
            ec[0] += 1
            e = energy_z2(theta)
            if ec[0] % 200 == 0:
                elapsed = time.time() - ts
                sv = get_sv_gpu(theta, project=True)
                mag, par = diagnose_gpu(sv)
                rate = ec[0] / elapsed
                eta_s = (15000 - ec[0]) / rate if rate > 0 else 0
                print(
                    f"  seed={s} eval {ec[0]:5d}  E={e:+.6f}  <M>={mag:+.4f}  "
                    f"<P>={par:.3f}  {rate:.1f}eval/s  ETA={eta_s/60:.0f}m  t={elapsed:.0f}s",
                    flush=True,
                )
            return e
        return cb

    print(f"\n  [seed={seed}] starting...", flush=True)
    cb = make_callback(seed, t_start, eval_count)
    res = minimize(
        cb,
        theta0,
        method="L-BFGS-B",
        options={"maxiter": 15000, "maxfun": 15000, "ftol": 1e-12},
    )

    elapsed = time.time() - t_start
    sv_final = get_sv_gpu(res.x, project=True)
    mag_f, par_f = diagnose_gpu(sv_final)

    print(
        f"  seed={seed} done: E_z2={res.fun:.6f}  "
        f"<M>={mag_f:+.4f}  <P>={par_f:.3f}  evals={res.nfev}  t={elapsed:.0f}s",
        flush=True,
    )
    seed_results.append({
        "seed": int(seed),
        "E_z2": float(res.fun),
        "magnetization": float(mag_f),
        "parity": float(par_f),
        "nfev": int(res.nfev),
        "time": elapsed,
    })

    if res.fun < best_E:
        best_E = res.fun
        best_theta = res.x.copy()

pct_err = 100 * (1 - best_E / E0)
print(f"\n  Best: E={best_E:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── COBYLA polish ──
print("\n[4] COBYLA polish (Z2 enforced)...", flush=True)
polish_count = [0]
t_polish = time.time()


def polish_cb(theta):
    polish_count[0] += 1
    e = energy_z2(theta)
    if polish_count[0] % 200 == 0:
        print(
            f"  polish eval {polish_count[0]}  E={e:+.6f}  t={time.time()-t_polish:.0f}s",
            flush=True,
        )
    return e


res_polish = minimize(
    polish_cb, best_theta, method="COBYLA", options={"maxiter": 2000, "rhobeg": 0.01}
)
if res_polish.fun < best_E:
    best_E = res_polish.fun
    best_theta = res_polish.x.copy()
pct_err = 100 * (1 - best_E / E0)
print(f"  Polish: E={best_E:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── Force profile ──
print("\n[5] Force profile V(dr) with Ry hologrons (Z2 projected)...", flush=True)

sv_vac = get_sv_gpu(best_theta, project=True)
mag_vac, par_vac = diagnose_gpu(sv_vac)
print(f"  Vacuum: <M>={mag_vac:+.5f}  <P>={par_vac:.4f}", flush=True)

force_data = []
for dr in range(1, 9):
    site2 = anchor + dr
    if site2 >= NQ:
        break

    # Vacuum ZZ
    C_vac = float(cp.real(cp.dot(sv_vac.conj(), ZZ_gpu[dr] @ sv_vac)))
    Zi_vac = float(cp.real(cp.dot(sv_vac.conj(), Z_gpu[anchor] @ sv_vac)))
    Zj_vac = float(cp.real(cp.dot(sv_vac.conj(), Z_gpu[site2] @ sv_vac)))
    C_conn_vac = C_vac - Zi_vac * Zj_vac

    # Two hologrons
    qc_two = qc_template.assign_parameters(dict(zip(params, best_theta)))
    qc_two.ry(HOLOGRON_ANGLE, anchor)
    qc_two.ry(HOLOGRON_ANGLE, site2)
    qc_two.save_statevector()
    sv_two_np = np.asarray(sim.run(qc_two).result().get_statevector())
    sv_two = parity_project_gpu(cp.asarray(sv_two_np))

    C_two = float(cp.real(cp.dot(sv_two.conj(), ZZ_gpu[dr] @ sv_two)))
    Zi_two = float(cp.real(cp.dot(sv_two.conj(), Z_gpu[anchor] @ sv_two)))
    Zj_two = float(cp.real(cp.dot(sv_two.conj(), Z_gpu[site2] @ sv_two)))
    C_conn_two = C_two - Zi_two * Zj_two

    V = C_two - C_vac
    V_conn = C_conn_two - C_conn_vac
    print(
        f"  dr={dr}: V={V:+.6f}  V_conn={V_conn:+.6f}  "
        f"C_vac={C_vac:.5f}  C_two={C_two:.5f}",
        flush=True,
    )
    force_data.append({
        "dr": dr, "V": float(V), "V_connected": float(V_conn),
        "C_vac": float(C_vac), "C_two": float(C_two),
        "C_conn_vac": float(C_conn_vac), "C_conn_two": float(C_conn_two),
    })

# Fit
drs = np.array([d["dr"] for d in force_data])
Vs = np.array([d["V"] for d in force_data])

try:
    def ads_force(r, C1, C2, xi):
        return C1 - C2 * np.exp(-r / xi)

    popt, pcov = curve_fit(
        ads_force, drs, Vs, p0=[0.0, 0.1, 1.5],
        bounds=([-1, -200, 0.01], [1, 200, 10]),
    )
    fit_err = np.sqrt(np.diag(pcov))
    print(f"\n  Fit: C1={popt[0]:.6f}  C2={popt[1]:.6f}  xi={popt[2]:.4f}")
    print(f"    errors: dC1={fit_err[0]:.4f}  dC2={fit_err[1]:.4f}  dxi={fit_err[2]:.4f}")
except Exception as ex:
    print(f"\n  Fit failed: {ex}")
    popt = [0, 0, 0]
    fit_err = [0, 0, 0]

print(f"\n  Theory: l_AdS=1.4427")
print(f"  Previous (3-layer 16q, no Z2): xi=1.233")

# ── Save ──
total_time = time.time() - T_GLOBAL
sv_final = get_sv_gpu(best_theta, project=True)
mag_final, par_final = diagnose_gpu(sv_final)

result = {
    "sim_id": "SIM-2026-006",
    "hypothesis_id": "HYP-2026-002",
    "fix": "Z2 parity projection onto P=+1 sector",
    "circuit": {
        "qubits": NQ, "layers": NLAYERS, "params": NP,
        "depth": qc_template.depth(),
    },
    "backend": "RunPod A100 (cupy + qiskit-aer)",
    "benchmark": {
        "circuit_time_s": t_circuit,
        "projection_time_s": t_proj,
        "matvec_time_s": t_matvec,
        "total_eval_time_s": t_total,
    },
    "exact_E0": E0,
    "E_optimized": float(best_E),
    "pct_error": float(pct_err),
    "magnetization": float(mag_final),
    "parity": float(par_final),
    "seed_results": seed_results,
    "force_profile": force_data,
    "fit": {
        "C1": float(popt[0]), "C2": float(popt[1]), "xi": float(popt[2]),
        "C1_err": float(fit_err[0]), "C2_err": float(fit_err[1]), "xi_err": float(fit_err[2]),
        "paper_l_AdS": 1.4427, "previous_no_z2_xi": 1.233,
    },
    "total_time_s": total_time,
}

# Save locally (RunPod has ephemeral storage — copy results before shutdown)
with open("SIM-2026-006.json", "w") as f:
    json.dump(result, f, indent=2)
np.save("theta_opt_SIM2026006.npy", best_theta)

print(f"\n{'='*65}")
print(f"RESULTS SAVED — COPY BEFORE SHUTTING DOWN POD")
print(f"  scp SIM-2026-006.json theta_opt_SIM2026006.npy <local>:")
print(f"{'='*65}")
print(f"Total time: {total_time:.0f}s ({total_time/3600:.1f}h)")
print("=" * 65)
