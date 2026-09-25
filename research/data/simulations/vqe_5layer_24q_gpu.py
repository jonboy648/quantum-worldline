"""
SIM-2026-004: 5-layer 24q MERA VQE on GPU (RTX 4060)
Targets HYP-2026-002: holographic force verification
Run in WSL: source ~/qiskit-gpu/bin/activate && python3 /mnt/d/quantum-worldline/research/data/simulations/vqe_5layer_24q_gpu.py
"""
import numpy as np
import time, json, sys
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

# Qiskit imports
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-004: 5-layer 24q MERA VQE (GPU)")
print("=" * 65, flush=True)

NQ = 24
NLAYERS = 5
HOLOGRON_ANGLE = np.pi / 3
T_GLOBAL = time.time()


# ── Build MERA circuit ──
def build_mera(nq, nlayers):
    qc = QuantumCircuit(nq)
    params = []
    pidx = 0
    for layer in range(nlayers):
        step = 2 ** layer
        # Disentanglers
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
        # Isometries
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


# ── Build Hamiltonian (sparse) ──
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
    """TFIM: H = -sum Z_i Z_{i+1} - sum X_i (OBC)"""
    H = csr_matrix((2**n, 2**n), dtype=complex)
    for i in range(n - 1):
        Zi = sparse_pauli(n, i, "Z")
        Zj = sparse_pauli(n, i + 1, "Z")
        H -= Zi @ Zj
    for i in range(n):
        H -= sparse_pauli(n, i, "X")
    return H


print("[1] Building Hamiltonian...", flush=True)
t0 = time.time()
H_sparse = build_hamiltonian(NQ)
print(f"  H built: {time.time() - t0:.1f}s", flush=True)

E0_val, _ = eigsh(H_sparse, k=1, which="SA")
E0 = float(E0_val[0])
print(f"  E0 = {E0:.6f}", flush=True)

# Keep H sparse — dense would be 4 PB for 24 qubits
# Use sparse mat-vec: H_sparse @ sv is O(nnz), not O(2^2N)

# ── GPU simulator ──
sim = AerSimulator(method="statevector", device="GPU")


def energy(theta):
    qc = qc_template.assign_parameters(dict(zip(params, theta)))
    qc2 = qc.copy()
    qc2.save_statevector()
    result = sim.run(qc2).result()
    sv = np.asarray(result.get_statevector())
    return float(np.real(sv.conj() @ (H_sparse @ sv)))


# Warmup
print("[2] GPU warmup...", flush=True)
theta_test = np.random.randn(NP) * 0.1
e_test = energy(theta_test)
print(f"  Warmup energy: {e_test:.4f}", flush=True)

# ── VQE: Multi-start L-BFGS-B ──
print(f"\n[3] VQE multi-start L-BFGS-B (3 seeds x 15000 evals)...", flush=True)
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
            e = energy(theta)
            if ec[0] % 200 == 0:
                elapsed = time.time() - ts
                print(
                    f"  seed={s} eval {ec[0]:5d}  E={e:+.5f}  t={elapsed:.0f}s",
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
    print(
        f"  seed={seed} done: E={res.fun:.6f}, evals={res.nfev}, t={elapsed:.0f}s",
        flush=True,
    )
    seed_results.append(
        {"seed": int(seed), "E": float(res.fun), "nfev": int(res.nfev), "time": elapsed}
    )

    if res.fun < best_E:
        best_E = res.fun
        best_theta = res.x.copy()

pct_err = 100 * (1 - best_E / E0)
print(f"\n  Best after multi-start: E={best_E:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── Polish with COBYLA ──
print("\n[4] COBYLA polish...", flush=True)
polish_count = [0]
t_polish = time.time()


def polish_cb(theta):
    polish_count[0] += 1
    e = energy(theta)
    if polish_count[0] % 200 == 0:
        print(
            f"  polish eval {polish_count[0]}  E={e:+.5f}  t={time.time() - t_polish:.0f}s",
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
print("\n[5] Force profile V(dr) with Ry hologrons...", flush=True)
anchor = NQ // 4  # site 6


def get_sv(theta_vec):
    qc = qc_template.assign_parameters(dict(zip(params, theta_vec)))
    qc2 = qc.copy()
    qc2.save_statevector()
    return np.asarray(sim.run(qc2).result().get_statevector())


def zz_correlator(sv, i, j):
    Zi = sparse_pauli(NQ, i, "Z")
    Zj = sparse_pauli(NQ, j, "Z")
    ZZ = Zi @ Zj
    return float(np.real(sv.conj() @ (ZZ @ sv)))


sv_vac = get_sv(best_theta)

force_data = []
for dr in range(1, 9):
    site2 = anchor + dr
    if site2 >= NQ:
        break

    C_vac = zz_correlator(sv_vac, anchor, site2)

    # Two hologrons
    qc_two = qc_template.assign_parameters(dict(zip(params, best_theta)))
    qc_two.ry(HOLOGRON_ANGLE, anchor)
    qc_two.ry(HOLOGRON_ANGLE, site2)
    qc_two.save_statevector()
    sv_two = np.asarray(sim.run(qc_two).result().get_statevector())
    C_two = zz_correlator(sv_two, anchor, site2)

    V = C_two - C_vac
    print(f"  dr={dr}: V={V:+.6f}  C_vac={C_vac:.5f}  C_two={C_two:.5f}", flush=True)
    force_data.append(
        {"dr": dr, "V": float(V), "C_vac": float(C_vac), "C_two": float(C_two)}
    )

# Fit
from scipy.optimize import curve_fit

drs = np.array([d["dr"] for d in force_data])
Vs = np.array([d["V"] for d in force_data])


def ads_force(r, C1, C2, xi):
    return C1 - C2 * np.exp(-r / xi)


try:
    popt, pcov = curve_fit(
        ads_force, drs, Vs, p0=[0.0, 0.1, 1.5], bounds=([-1, -200, 0.01], [1, 200, 10])
    )
    C1_fit, C2_fit, xi_fit = popt
    perr = np.sqrt(np.diag(pcov))
except Exception as ex:
    print(f"  Fit failed: {ex}")
    C1_fit, C2_fit, xi_fit = 0, 0, 0
    perr = [0, 0, 0]

print(f"\n  Fit: C1={C1_fit:.6f}  C2={C2_fit:.6f}  xi={xi_fit:.4f}")
print(f"  Theory: l_AdS=1.4427  3-layer_16q xi=1.233")

# ── Save ──
total_time = time.time() - T_GLOBAL
result = {
    "sim_id": "SIM-2026-004",
    "hypothesis_id": "HYP-2026-002",
    "circuit": {
        "qubits": NQ,
        "layers": NLAYERS,
        "params": NP,
        "depth": qc_template.depth(),
    },
    "backend": "qiskit-aer-gpu RTX4060",
    "exact_E0": E0,
    "E_optimized": float(best_E),
    "pct_error": float(pct_err),
    "seed_results": seed_results,
    "force_profile": force_data,
    "fit": {
        "C1": float(C1_fit),
        "C2": float(C2_fit),
        "xi": float(xi_fit),
        "paper_C1": 0.080,
        "paper_C2": 13.6,
        "paper_l_AdS": 1.4427,
    },
    "total_time_s": total_time,
}

with open(
    "/mnt/d/quantum-worldline/research/data/simulations/SIM-2026-004.json", "w"
) as f:
    json.dump(result, f, indent=2)
np.save(
    "/mnt/d/quantum-worldline/research/data/simulations/theta_opt_SIM2026004.npy",
    best_theta,
)

print(f"\nSaved SIM-2026-004.json and theta_opt")
print(f"Total time: {total_time:.0f}s ({total_time/3600:.1f}h)")
print("=" * 65)
