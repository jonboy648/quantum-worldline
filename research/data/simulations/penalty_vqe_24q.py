"""
SIM-2026-007: Penalty-method Z2 VQE, 24q/5-layer MERA — RunPod A100
Replaces hard Z2 projection with smooth penalty for better L-BFGS-B convergence.
After VQE: boundary-primary force measurements.

E_eff = <psi|H|psi> + lambda * (1 - <psi|P|psi>) / 2

Setup on RunPod:
  pip install qiskit qiskit-aer-gpu cupy-cuda12x scipy
  python penalty_vqe_24q.py | tee sim_penalty.log
"""
import numpy as np
import time, json, sys
from scipy.optimize import minimize, curve_fit
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

import cupy as cp
import cupyx.scipy.sparse as cpsparse

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-007: Penalty Z2 VQE — 24q/5-layer MERA (RunPod A100)")
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
T_GLOBAL = time.time()

# ── Z2 parity (for penalty, NOT projection) ──
PARITY_MASK = (1 << NQ) - 1
PARITY_INDICES_GPU = cp.arange(1 << NQ, dtype=cp.int64) ^ PARITY_MASK


def parity_expectation_gpu(sv_gpu):
    """<P> = <psi| prod(X_i) |psi> via bit-flip trick."""
    return float(cp.real(cp.sum(sv_gpu.conj() * sv_gpu[PARITY_INDICES_GPU])))


def parity_project_gpu(sv_gpu):
    """Hard projection — used only for final force measurements."""
    sv_plus = sv_gpu + sv_gpu[PARITY_INDICES_GPU]
    norm = cp.linalg.norm(sv_plus)
    if float(norm) < 1e-15:
        return sv_gpu
    return sv_plus / norm


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

# ── Hamiltonian ──
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
print(f"  H built: {time.time() - t0:.1f}s", flush=True)

E0 = -30.199712  # cached exact ground state energy
print(f"  E0 = {E0:.6f} (cached)", flush=True)

print("  Transferring H to GPU...", flush=True)
H_gpu = cpsparse.csr_matrix(
    (cp.asarray(H_scipy.data), cp.asarray(H_scipy.indices), cp.asarray(H_scipy.indptr)),
    shape=H_scipy.shape,
)
print(f"  H on GPU: {H_gpu.nnz} nonzeros", flush=True)

# Z operators
print("[1b] Building Z operators on GPU...", flush=True)
Z_gpu = []
for i in range(NQ):
    z = sparse_pauli(NQ, i, "Z")
    Z_gpu.append(cpsparse.csr_matrix(
        (cp.asarray(z.data), cp.asarray(z.indices), cp.asarray(z.indptr)),
        shape=z.shape,
    ))

# ZZ for force profile
anchor = NQ // 4  # site 6
ZZ_gpu = {}
for dr in range(1, 11):
    site2 = anchor + dr
    if site2 < NQ:
        ZZ_gpu[dr] = Z_gpu[anchor] @ Z_gpu[site2]
print(f"  {len(ZZ_gpu)} ZZ operators precomputed", flush=True)


# ── Simulator ──
try:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector", device="GPU")
    print("[2] Using qiskit-aer GPU backend", flush=True)
except Exception:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector")
    print("[2] Using qiskit-aer CPU fallback", flush=True)


def get_sv_gpu(theta_vec):
    """Run circuit, return raw statevector on GPU (NO projection)."""
    qc = qc_template.assign_parameters(dict(zip(params, theta_vec)))
    qc2 = qc.copy()
    qc2.save_statevector()
    sv_np = np.asarray(sim.run(qc2).result().get_statevector())
    return cp.asarray(sv_np)


# ── Penalty energy function ──
def energy_penalty(theta, lam):
    """E_eff = <H> + lambda * (1 - <P>) / 2"""
    sv = get_sv_gpu(theta)
    Hsv = H_gpu @ sv
    E_raw = float(cp.real(cp.dot(sv.conj(), Hsv)))
    P = parity_expectation_gpu(sv)
    penalty = lam * (1.0 - P) / 2.0
    return E_raw + penalty


def diagnose_gpu(sv_gpu):
    mag = sum(
        float(cp.real(cp.dot(sv_gpu.conj(), Z_gpu[i] @ sv_gpu)))
        for i in range(NQ)
    ) / NQ
    par = parity_expectation_gpu(sv_gpu)
    return mag, par


# ── Warmup + benchmark ──
print("[2b] Warmup + benchmark...", flush=True)
theta_test = np.random.randn(NP) * 0.1

t0 = time.time()
e_test = energy_penalty(theta_test, lam=20.0)
t_eval = time.time() - t0

sv_test = get_sv_gpu(theta_test)
mag_t, par_t = diagnose_gpu(sv_test)
print(f"  Eval time: {t_eval:.3f}s  E_eff={e_test:.4f}  <M>={mag_t:.4f}  <P>={par_t:.4f}")

est_evals = 5 * 20000 + 3000
est_hours = est_evals * t_eval / 3600
print(f"  Estimated runtime: {est_hours:.1f}h ({est_evals} evals x {t_eval:.2f}s)", flush=True)

# ── VQE with penalty method ──
# Strategy: 5 seeds x 20K evals with lambda=20
# Lambda=20 makes ferromagnetic trap cost +10 extra energy units
# (ferro has <P>=0, so penalty = 20*0.5 = 10; true GS has <P>=1, penalty=0)
LAMBDA = 20.0
SEEDS = [7, 42, 99, 13, 77]
MAX_EVALS = 20000

print(f"\n[3] Penalty VQE: {len(SEEDS)} seeds x {MAX_EVALS} evals, lambda={LAMBDA}", flush=True)
best_E = 0.0
best_theta = None
seed_results = []

for seed_idx, seed in enumerate(SEEDS):
    np.random.seed(seed)
    theta0 = np.random.randn(NP) * 0.3
    eval_count = [0]
    t_start = time.time()

    def make_callback(s, ts, ec, lam):
        def cb(theta):
            ec[0] += 1
            e = energy_penalty(theta, lam)
            if ec[0] % 500 == 0:
                sv = get_sv_gpu(theta)
                Hsv = H_gpu @ sv
                E_raw = float(cp.real(cp.dot(sv.conj(), Hsv)))
                mag, par = diagnose_gpu(sv)
                elapsed = time.time() - ts
                rate = ec[0] / elapsed
                eta_m = (MAX_EVALS - ec[0]) / rate / 60 if rate > 0 else 0
                pct = 100 * (1 - E_raw / E0)
                print(
                    f"  seed={s} eval {ec[0]:5d}  E_raw={E_raw:+.6f} ({pct:.2f}%)  "
                    f"E_eff={e:+.6f}  <M>={mag:+.4f}  <P>={par:.4f}  "
                    f"{rate:.1f}ev/s  ETA={eta_m:.0f}m",
                    flush=True,
                )
            return e
        return cb

    print(f"\n  [seed={seed}] starting...", flush=True)
    cb = make_callback(seed, t_start, eval_count, LAMBDA)
    res = minimize(
        cb, theta0, method="L-BFGS-B",
        options={"maxiter": MAX_EVALS, "maxfun": MAX_EVALS, "ftol": 1e-12},
    )

    # Evaluate raw energy (without penalty)
    sv_final = get_sv_gpu(res.x)
    Hsv = H_gpu @ sv_final
    E_raw = float(cp.real(cp.dot(sv_final.conj(), Hsv)))
    mag_f, par_f = diagnose_gpu(sv_final)
    elapsed = time.time() - t_start
    pct = 100 * (1 - E_raw / E0)

    print(
        f"  seed={seed} done: E_raw={E_raw:.6f} ({pct:.2f}%)  "
        f"E_eff={res.fun:.6f}  <M>={mag_f:+.4f}  <P>={par_f:.4f}  "
        f"evals={res.nfev}  t={elapsed:.0f}s",
        flush=True,
    )
    seed_results.append({
        "seed": int(seed), "E_raw": float(E_raw), "E_eff": float(res.fun),
        "pct_error": float(pct), "magnetization": float(mag_f),
        "parity": float(par_f), "nfev": int(res.nfev), "time_s": elapsed,
    })

    if E_raw < best_E:
        best_E = E_raw
        best_theta = res.x.copy()
        print(f"  *** New best: E_raw={E_raw:.6f} ({pct:.2f}%)", flush=True)

pct_err = 100 * (1 - best_E / E0)
print(f"\n  Best across seeds: E={best_E:.6f} ({pct_err:.2f}%)", flush=True)

# ── COBYLA polish (with penalty) ──
print("\n[4] COBYLA polish (penalty)...", flush=True)
polish_count = [0]
t_polish = time.time()


def polish_cb(theta):
    polish_count[0] += 1
    e = energy_penalty(theta, LAMBDA)
    if polish_count[0] % 500 == 0:
        sv = get_sv_gpu(theta)
        Hsv = H_gpu @ sv
        E_raw = float(cp.real(cp.dot(sv.conj(), Hsv)))
        pct = 100 * (1 - E_raw / E0)
        print(
            f"  polish eval {polish_count[0]}  E_raw={E_raw:+.6f} ({pct:.2f}%)  "
            f"E_eff={e:+.6f}  t={time.time()-t_polish:.0f}s",
            flush=True,
        )
    return e


res_polish = minimize(
    polish_cb, best_theta, method="COBYLA",
    options={"maxiter": 3000, "rhobeg": 0.01},
)
sv_pol = get_sv_gpu(res_polish.x)
Hsv_pol = H_gpu @ sv_pol
E_pol = float(cp.real(cp.dot(sv_pol.conj(), Hsv_pol)))
if E_pol < best_E:
    best_E = E_pol
    best_theta = res_polish.x.copy()
pct_err = 100 * (1 - best_E / E0)
print(f"  After polish: E={best_E:.6f} ({pct_err:.2f}%)", flush=True)

# ── Boundary-primary force measurements ──
print("\n[5] Boundary-primary force profile...", flush=True)

# For force measurements, project to Z2=+1 sector for clean symmetry
sv_vac = parity_project_gpu(get_sv_gpu(best_theta))
mag_vac, par_vac = diagnose_gpu(sv_vac)
print(f"  Vacuum (projected): <M>={mag_vac:+.5f}  <P>={par_vac:.4f}", flush=True)

# Build X operators on GPU (needed for boundary-primary)
X_gpu = []
for i in range(NQ):
    x = sparse_pauli(NQ, i, "X")
    X_gpu.append(cpsparse.csr_matrix(
        (cp.asarray(x.data), cp.asarray(x.indices), cp.asarray(x.indptr)),
        shape=x.shape,
    ))


def apply_boundary_primary(sv, site):
    """sigma_j = 0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})"""
    j = site
    j1 = (site + 1) % NQ
    result = 0.635 * (X_gpu[j] @ sv + X_gpu[j1] @ sv)
    result -= 0.026 * (X_gpu[j] @ (Z_gpu[j1] @ sv) + Z_gpu[j] @ (X_gpu[j1] @ sv))
    return result


# Also measure with Ry hologrons for comparison
HOLOGRON_ANGLE = np.pi / 3

force_bp = []  # boundary-primary
force_ry = []  # Ry hologron

for dr in range(1, 11):
    site2 = anchor + dr
    if site2 >= NQ - 1:  # -1 because BP uses site+1
        break

    # Vacuum ZZ
    C_vac = float(cp.real(cp.dot(sv_vac.conj(), ZZ_gpu[dr] @ sv_vac)))
    Zi_vac = float(cp.real(cp.dot(sv_vac.conj(), Z_gpu[anchor] @ sv_vac)))
    Zj_vac = float(cp.real(cp.dot(sv_vac.conj(), Z_gpu[site2] @ sv_vac)))
    C_conn_vac = C_vac - Zi_vac * Zj_vac

    # --- Boundary-primary excitation ---
    sv_bp_a = apply_boundary_primary(sv_vac, anchor)
    sv_bp_b = apply_boundary_primary(sv_vac, site2)
    # Two-excitation state (unnormalized)
    sv_bp_two = apply_boundary_primary(sv_bp_a, site2)
    # Normalize
    norm_a = float(cp.linalg.norm(sv_bp_a))
    norm_b = float(cp.linalg.norm(sv_bp_b))
    norm_two = float(cp.linalg.norm(sv_bp_two))

    if norm_a > 1e-10 and norm_b > 1e-10 and norm_two > 1e-10:
        sv_bp_a_n = sv_bp_a / norm_a
        sv_bp_b_n = sv_bp_b / norm_b
        sv_bp_two_n = sv_bp_two / norm_two

        E_vac_bp = float(cp.real(cp.dot(sv_vac.conj(), H_gpu @ sv_vac)))
        E_a = float(cp.real(cp.dot(sv_bp_a_n.conj(), H_gpu @ sv_bp_a_n)))
        E_b = float(cp.real(cp.dot(sv_bp_b_n.conj(), H_gpu @ sv_bp_b_n)))
        E_two = float(cp.real(cp.dot(sv_bp_two_n.conj(), H_gpu @ sv_bp_two_n)))
        U_int = E_two - E_a - E_b + E_vac_bp

        C_bp = float(cp.real(cp.dot(sv_bp_two_n.conj(), ZZ_gpu[dr] @ sv_bp_two_n)))
        V_bp = C_bp - C_vac

        print(
            f"  BP dr={dr}: V_corr={V_bp:+.6f}  U_int={U_int:+.6f}  "
            f"E_a={E_a:.3f}  E_two={E_two:.3f}",
            flush=True,
        )
        force_bp.append({
            "dr": dr, "V_correlator": float(V_bp), "U_interaction": float(U_int),
            "E_single_a": float(E_a), "E_single_b": float(E_b),
            "E_two": float(E_two), "E_vac": float(E_vac_bp),
        })
    else:
        print(f"  BP dr={dr}: normalization failed (norms: {norm_a:.4f}, {norm_b:.4f}, {norm_two:.4f})", flush=True)

    # --- Ry hologron (for comparison) ---
    qc_ry = qc_template.assign_parameters(dict(zip(params, best_theta)))
    qc_ry.ry(HOLOGRON_ANGLE, anchor)
    qc_ry.ry(HOLOGRON_ANGLE, site2)
    qc_ry.save_statevector()
    sv_ry = parity_project_gpu(cp.asarray(
        np.asarray(sim.run(qc_ry).result().get_statevector())
    ))
    C_ry = float(cp.real(cp.dot(sv_ry.conj(), ZZ_gpu[dr] @ sv_ry)))
    V_ry = C_ry - C_vac
    print(f"  Ry dr={dr}: V={V_ry:+.6f}", flush=True)
    force_ry.append({"dr": dr, "V": float(V_ry)})

# Fit boundary-primary force profile
if len(force_bp) >= 3:
    drs_bp = np.array([d["dr"] for d in force_bp])
    U_ints = np.array([d["U_interaction"] for d in force_bp])

    try:
        def ads_force(r, C1, C2, xi):
            return C1 - C2 * np.exp(-r / xi)

        popt, pcov = curve_fit(
            ads_force, drs_bp, U_ints, p0=[0.0, 0.1, 1.5],
            bounds=([-1, -200, 0.01], [1, 200, 10]),
        )
        fit_err = np.sqrt(np.diag(pcov))
        print(f"\n  BP U_int fit: C1={popt[0]:.6f}  C2={popt[1]:.6f}  xi={popt[2]:.4f}")
        print(f"    errors: dC1={fit_err[0]:.4f}  dC2={fit_err[1]:.4f}  dxi={fit_err[2]:.4f}")
        print(f"  Theory: l_AdS = 1.4427")
        bp_fit = {
            "C1": float(popt[0]), "C2": float(popt[1]), "xi": float(popt[2]),
            "C1_err": float(fit_err[0]), "C2_err": float(fit_err[1]), "xi_err": float(fit_err[2]),
        }
    except Exception as ex:
        print(f"\n  BP fit failed: {ex}")
        bp_fit = {"error": str(ex)}
else:
    print(f"\n  Too few BP data points ({len(force_bp)}) for fit")
    bp_fit = {"error": f"only {len(force_bp)} points"}

# ── Save ──
total_time = time.time() - T_GLOBAL
sv_final = get_sv_gpu(best_theta)
mag_final, par_final = diagnose_gpu(sv_final)

result = {
    "sim_id": "SIM-2026-007",
    "hypothesis_id": "HYP-2026-002",
    "method": "penalty Z2 (smooth)",
    "penalty_lambda": LAMBDA,
    "circuit": {"qubits": NQ, "layers": NLAYERS, "params": NP, "depth": qc_template.depth()},
    "backend": "RunPod A100 (cupy + qiskit-aer)",
    "exact_E0": E0,
    "E_optimized": float(best_E),
    "pct_error": float(pct_err),
    "magnetization_raw": float(mag_final),
    "parity_raw": float(par_final),
    "seed_results": seed_results,
    "force_profile_boundary_primary": force_bp,
    "force_profile_ry_hologron": force_ry,
    "bp_fit": bp_fit,
    "total_time_s": total_time,
}

with open("SIM-2026-007.json", "w") as f:
    json.dump(result, f, indent=2)
np.save("theta_opt_SIM2026007.npy", best_theta)

print(f"\n{'='*65}")
print(f"RESULTS SAVED")
print(f"  SIM-2026-007.json")
print(f"  theta_opt_SIM2026007.npy")
print(f"  Best E = {best_E:.6f} ({pct_err:.2f}% error)")
print(f"  Total time: {total_time:.0f}s ({total_time/3600:.1f}h)")
print(f"{'='*65}")
