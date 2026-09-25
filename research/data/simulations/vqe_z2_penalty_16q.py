"""
SIM-2026-005b: Z2 penalty-enforced MERA VQE (16q / 3-layer, CPU)
Targets HYP-2026-002: holographic force verification

Unlike SIM-2026-005 (projection), this uses a smooth penalty term:
  E_eff = <psi|H|psi> + lambda * (1 - <psi|P|psi>) / 2

The penalty is smooth in theta (no normalization discontinuity),
so L-BFGS-B's Hessian approximation stays accurate.

Run: python research/data/simulations/vqe_z2_penalty_16q.py
"""
import numpy as np
import time, json
from scipy.optimize import minimize, curve_fit
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-005b: Z2-penalty 16q/3-layer MERA VQE")
print("=" * 65, flush=True)

NQ = 16
NLAYERS = 3
HOLOGRON_ANGLE = np.pi / 3
LAMBDA_Z2 = 10.0  # penalty strength
T_GLOBAL = time.time()


# ── Z2 parity helpers ──
PARITY_MASK = (1 << NQ) - 1
PARITY_INDICES = np.arange(1 << NQ) ^ PARITY_MASK


def parity_expectation(sv):
    """<P> = <psi|prod(X_i)|psi> = sum_x conj(sv[x]) * sv[~x]"""
    return float(np.real(np.sum(sv.conj() * sv[PARITY_INDICES])))


def parity_project(sv):
    """Project onto P=+1 sector (for final analysis only, not during optimization)."""
    sv_plus = sv + sv[PARITY_INDICES]
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        return sv
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


print("[1] Building Hamiltonian...", flush=True)
t0 = time.time()
H_sparse = build_hamiltonian(NQ)
print(f"  H built: {time.time() - t0:.1f}s", flush=True)

E0 = -20.016388
print(f"  E0 = {E0:.6f} (cached)", flush=True)

Z_sparse = [sparse_pauli(NQ, i, "Z") for i in range(NQ)]

sim = AerSimulator(method="statevector")


def get_sv_raw(theta_vec):
    qc = qc_template.assign_parameters(dict(zip(params, theta_vec)))
    qc2 = qc.copy()
    qc2.save_statevector()
    return np.asarray(sim.run(qc2).result().get_statevector())


def diagnose(sv):
    mag = sum(float(np.real(sv.conj() @ (Zop @ sv))) for Zop in Z_sparse) / NQ
    par = parity_expectation(sv)
    return mag, par


# ── Energy functions ──
def energy_penalty(theta):
    """E_eff = <H> + lambda * (1 - <P>) / 2"""
    sv = get_sv_raw(theta)
    e_ham = float(np.real(sv.conj() @ (H_sparse @ sv)))
    par = parity_expectation(sv)
    penalty = LAMBDA_Z2 * (1.0 - par) / 2.0
    return e_ham + penalty


def energy_raw(theta):
    sv = get_sv_raw(theta)
    return float(np.real(sv.conj() @ (H_sparse @ sv)))


# Warmup
print(f"[2] Warmup (lambda={LAMBDA_Z2})...", flush=True)
theta_test = np.random.randn(NP) * 0.1
sv_t = get_sv_raw(theta_test)
e_raw = float(np.real(sv_t.conj() @ (H_sparse @ sv_t)))
par_t = parity_expectation(sv_t)
e_pen = e_raw + LAMBDA_Z2 * (1.0 - par_t) / 2.0
print(f"  E_raw={e_raw:.4f}  <P>={par_t:.4f}  penalty={LAMBDA_Z2*(1-par_t)/2:.4f}  E_eff={e_pen:.4f}", flush=True)

# ── VQE ──
print(f"\n[3] Penalty VQE: 4 seeds x 15000 evals (L-BFGS-B)...", flush=True)
best_E_eff = 0.0
best_E_raw = 0.0
best_theta = None
seed_results = []

for seed_idx, seed in enumerate([7, 42, 99, 137]):
    np.random.seed(seed)
    theta0 = np.random.randn(NP) * 0.3
    eval_count = [0]
    t_start = time.time()

    def make_callback(s, ts, ec):
        def cb(theta):
            ec[0] += 1
            e = energy_penalty(theta)
            if ec[0] % 500 == 0:
                sv = get_sv_raw(theta)
                mag, par = diagnose(sv)
                e_r = float(np.real(sv.conj() @ (H_sparse @ sv)))
                elapsed = time.time() - ts
                print(
                    f"  seed={s} eval {ec[0]:5d}  E_eff={e:+.5f}  E_raw={e_r:+.5f}  "
                    f"<M>={mag:+.4f}  <P>={par:.3f}  t={elapsed:.0f}s",
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
    sv_final = get_sv_raw(res.x)
    mag_f, par_f = diagnose(sv_final)
    e_raw_f = float(np.real(sv_final.conj() @ (H_sparse @ sv_final)))

    print(
        f"  seed={seed} done: E_eff={res.fun:.6f}  E_raw={e_raw_f:.6f}  "
        f"<M>={mag_f:+.4f}  <P>={par_f:.3f}  evals={res.nfev}  t={elapsed:.0f}s",
        flush=True,
    )
    seed_results.append({
        "seed": int(seed),
        "E_eff": float(res.fun),
        "E_raw": float(e_raw_f),
        "magnetization": float(mag_f),
        "parity": float(par_f),
        "nfev": int(res.nfev),
        "time": elapsed,
    })

    if e_raw_f < best_E_raw or best_theta is None:
        best_E_eff = res.fun
        best_E_raw = e_raw_f
        best_theta = res.x.copy()

pct_err = 100 * (1 - best_E_raw / E0)
print(f"\n  Best: E_raw={best_E_raw:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── COBYLA polish (still with penalty) ──
print("\n[4] COBYLA polish (penalty)...", flush=True)
polish_count = [0]
t_polish = time.time()


def polish_cb(theta):
    polish_count[0] += 1
    e = energy_penalty(theta)
    if polish_count[0] % 500 == 0:
        print(
            f"  polish eval {polish_count[0]}  E_eff={e:+.5f}  t={time.time()-t_polish:.0f}s",
            flush=True,
        )
    return e


res_polish = minimize(
    polish_cb, best_theta, method="COBYLA", options={"maxiter": 3000, "rhobeg": 0.01}
)
sv_pol = get_sv_raw(res_polish.x)
e_raw_pol = float(np.real(sv_pol.conj() @ (H_sparse @ sv_pol)))
if e_raw_pol < best_E_raw:
    best_E_raw = e_raw_pol
    best_theta = res_polish.x.copy()
pct_err = 100 * (1 - best_E_raw / E0)
print(f"  Polish: E_raw={best_E_raw:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── Force profile (use projection for final state analysis) ──
print("\n[5] Force profile V(dr) with Ry hologrons...", flush=True)
anchor = NQ // 4


def zz_correlator(sv, i, j):
    ZZ = Z_sparse[i] @ Z_sparse[j]
    return float(np.real(sv.conj() @ (ZZ @ sv)))


def z_expectation(sv, i):
    return float(np.real(sv.conj() @ (Z_sparse[i] @ sv)))


# Project final vacuum state for clean force measurement
sv_vac = parity_project(get_sv_raw(best_theta))
mag_vac, par_vac = diagnose(sv_vac)
print(f"  Vacuum (projected): <M>={mag_vac:+.5f}  <P>={par_vac:.4f}", flush=True)

force_data = []
for dr in range(1, 9):
    site2 = anchor + dr
    if site2 >= NQ:
        break

    C_vac = zz_correlator(sv_vac, anchor, site2)
    Zi_vac = z_expectation(sv_vac, anchor)
    Zj_vac = z_expectation(sv_vac, site2)
    C_conn_vac = C_vac - Zi_vac * Zj_vac

    qc_two = qc_template.assign_parameters(dict(zip(params, best_theta)))
    qc_two.ry(HOLOGRON_ANGLE, anchor)
    qc_two.ry(HOLOGRON_ANGLE, site2)
    qc_two.save_statevector()
    sv_two = np.asarray(sim.run(qc_two).result().get_statevector())
    sv_two = parity_project(sv_two)

    C_two = zz_correlator(sv_two, anchor, site2)
    Zi_two = z_expectation(sv_two, anchor)
    Zj_two = z_expectation(sv_two, site2)
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


def ads_force(r, C1, C2, xi):
    return C1 - C2 * np.exp(-r / xi)


try:
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
print(f"  Previous (no Z2): xi=1.233")

# ── Save ──
total_time = time.time() - T_GLOBAL
sv_final = parity_project(get_sv_raw(best_theta))
mag_final, par_final = diagnose(sv_final)

result = {
    "sim_id": "SIM-2026-005b",
    "hypothesis_id": "HYP-2026-002",
    "fix": "Z2 penalty: E_eff = <H> + lambda*(1-<P>)/2",
    "lambda_z2": LAMBDA_Z2,
    "circuit": {"qubits": NQ, "layers": NLAYERS, "params": NP, "depth": qc_template.depth()},
    "backend": "qiskit-aer CPU (statevector)",
    "exact_E0": E0,
    "E_optimized": float(best_E_raw),
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

with open("research/data/simulations/SIM-2026-005b.json", "w") as f:
    json.dump(result, f, indent=2)
np.save("research/data/simulations/theta_opt_SIM2026005b.npy", best_theta)

print(f"\nSaved SIM-2026-005b.json")
print(f"Total time: {total_time:.0f}s ({total_time/60:.1f}m)")
print("=" * 65)
