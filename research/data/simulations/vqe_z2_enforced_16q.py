"""
SIM-2026-005: Z2 symmetry-enforced MERA VQE (16q / 3-layer, CPU)
Targets HYP-2026-002: holographic force verification
Fix for Z2 trap found in SIM-2026-003/004.

Key change: project statevector onto P=+1 parity sector before computing
energy. P = prod(X_i) is the global spin-flip operator of the TFIM.

Run: python research/data/simulations/vqe_z2_enforced_16q.py
"""
import numpy as np
import time, json
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

# Qiskit imports
from qiskit_aer import AerSimulator
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-005: Z2-enforced 16q/3-layer MERA VQE")
print("=" * 65, flush=True)

NQ = 16
NLAYERS = 3
HOLOGRON_ANGLE = np.pi / 3
T_GLOBAL = time.time()


# ── Z2 parity projection ──
def parity_project(sv, nq):
    """Project statevector onto P=+1 (Z2 symmetric) sector.

    P = prod(X_i) flips all qubits: P|x> = |~x>.
    Projector onto P=+1: (I + P)/2.
    """
    mask = (1 << nq) - 1
    indices = np.arange(len(sv)) ^ mask  # bit-flip all qubits
    sv_plus = sv + sv[indices]
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        # Entirely in P=-1 sector — shouldn't happen with good init
        print("  WARNING: state entirely in P=-1 sector!", flush=True)
        return sv
    return sv_plus / norm


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

# Cached from classical baseline
E0 = -20.016388
print(f"  E0 = {E0:.6f} (cached)", flush=True)

# ── Diagnostics (all sparse) ──
Z_sparse = [sparse_pauli(NQ, i, "Z") for i in range(NQ)]


def diagnose(sv, label=""):
    """Compute magnetization and parity to verify Z2 enforcement."""
    mag = sum(float(np.real(sv.conj() @ (Zop @ sv))) for Zop in Z_sparse) / NQ
    # Parity: <P> = <prod(X_i)> = overlap with bit-flipped state
    mask = (1 << NQ) - 1
    indices = np.arange(len(sv)) ^ mask
    parity = float(np.real(np.sum(sv.conj() * sv[indices])))
    return mag, parity


# ── Simulator ──
sim = AerSimulator(method="statevector")


def get_sv(theta_vec, project=True):
    qc = qc_template.assign_parameters(dict(zip(params, theta_vec)))
    qc2 = qc.copy()
    qc2.save_statevector()
    sv = np.asarray(sim.run(qc2).result().get_statevector())
    if project:
        sv = parity_project(sv, NQ)
    return sv


eval_log = []


def energy_z2(theta):
    """Energy with Z2 parity projection."""
    sv = get_sv(theta, project=True)
    return float(np.real(sv.conj() @ (H_sparse @ sv)))


def energy_raw(theta):
    """Energy WITHOUT projection (for comparison)."""
    sv = get_sv(theta, project=False)
    return float(np.real(sv.conj() @ (H_sparse @ sv)))


# Warmup
print("[2] Warmup...", flush=True)
theta_test = np.random.randn(NP) * 0.1
e_z2 = energy_z2(theta_test)
e_raw = energy_raw(theta_test)
mag, par = diagnose(get_sv(theta_test, project=True))
print(f"  Z2 energy: {e_z2:.4f}  raw energy: {e_raw:.4f}", flush=True)
print(f"  After projection: <M>={mag:.4f}  <P>={par:.4f}", flush=True)

# ── VQE with Z2 projection ──
print(f"\n[3] Z2-enforced VQE: 4 seeds x 15000 evals (L-BFGS-B)...", flush=True)
best_E = 0.0
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
            e = energy_z2(theta)
            if ec[0] % 500 == 0:
                elapsed = time.time() - ts
                sv = get_sv(theta, project=True)
                mag, par = diagnose(sv)
                print(
                    f"  seed={s} eval {ec[0]:5d}  E={e:+.6f}  <M>={mag:+.4f}  <P>={par:.3f}  t={elapsed:.0f}s",
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
    sv_final = get_sv(res.x, project=True)
    mag_f, par_f = diagnose(sv_final)
    e_raw_f = energy_raw(res.x)

    print(
        f"  seed={seed} done: E_z2={res.fun:.6f}  E_raw={e_raw_f:.6f}  "
        f"<M>={mag_f:+.4f}  <P>={par_f:.3f}  evals={res.nfev}  t={elapsed:.0f}s",
        flush=True,
    )
    seed_results.append({
        "seed": int(seed),
        "E_z2": float(res.fun),
        "E_raw": float(e_raw_f),
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

# ── Compare: run WITHOUT Z2 (same seeds, for fair comparison) ──
print(f"\n[3b] Control: NO Z2 projection (seed=7 only, 5000 evals)...", flush=True)
np.random.seed(7)
theta0_ctrl = np.random.randn(NP) * 0.3
ctrl_count = [0]
t_ctrl = time.time()


def ctrl_cb(theta):
    ctrl_count[0] += 1
    e = energy_raw(theta)
    if ctrl_count[0] % 500 == 0:
        sv = get_sv(theta, project=False)
        mag, par = diagnose(sv)
        print(
            f"  ctrl eval {ctrl_count[0]:5d}  E={e:+.6f}  <M>={mag:+.4f}  <P>={par:.3f}  t={time.time()-t_ctrl:.0f}s",
            flush=True,
        )
    return e


res_ctrl = minimize(
    ctrl_cb,
    theta0_ctrl,
    method="L-BFGS-B",
    options={"maxiter": 5000, "maxfun": 5000, "ftol": 1e-12},
)
sv_ctrl = get_sv(res_ctrl.x, project=False)
mag_ctrl, par_ctrl = diagnose(sv_ctrl)
print(
    f"  Control: E={res_ctrl.fun:.6f}  <M>={mag_ctrl:+.4f}  <P>={par_ctrl:.3f}",
    flush=True,
)

# ── COBYLA polish (Z2 enforced) ──
print("\n[4] COBYLA polish (Z2 enforced)...", flush=True)
polish_count = [0]
t_polish = time.time()


def polish_cb(theta):
    polish_count[0] += 1
    e = energy_z2(theta)
    if polish_count[0] % 500 == 0:
        print(
            f"  polish eval {polish_count[0]}  E={e:+.6f}  t={time.time()-t_polish:.0f}s",
            flush=True,
        )
    return e


res_polish = minimize(
    polish_cb, best_theta, method="COBYLA", options={"maxiter": 3000, "rhobeg": 0.01}
)
if res_polish.fun < best_E:
    best_E = res_polish.fun
    best_theta = res_polish.x.copy()
pct_err = 100 * (1 - best_E / E0)
print(f"  Polish: E={best_E:.6f} ({pct_err:.2f}% from exact)", flush=True)

# ── Force profile with Z2 enforcement ──
print("\n[5] Force profile V(dr) with Ry hologrons (Z2 projected)...", flush=True)
anchor = NQ // 4  # site 4


def zz_correlator(sv, i, j):
    ZZ = Z_sparse[i] @ Z_sparse[j]
    return float(np.real(sv.conj() @ (ZZ @ sv)))


def z_expectation(sv, i):
    return float(np.real(sv.conj() @ (Z_sparse[i] @ sv)))


sv_vac = get_sv(best_theta, project=True)
mag_vac, par_vac = diagnose(sv_vac)
print(f"  Vacuum: <M>={mag_vac:+.5f}  <P>={par_vac:.4f}", flush=True)

force_data = []
for dr in range(1, 9):
    site2 = anchor + dr
    if site2 >= NQ:
        break

    # Vacuum ZZ
    C_vac = zz_correlator(sv_vac, anchor, site2)
    # Connected correlator: C_conn = <ZiZj> - <Zi><Zj>
    Zi_vac = z_expectation(sv_vac, anchor)
    Zj_vac = z_expectation(sv_vac, site2)
    C_conn_vac = C_vac - Zi_vac * Zj_vac

    # Two hologrons (also project)
    qc_two = qc_template.assign_parameters(dict(zip(params, best_theta)))
    qc_two.ry(HOLOGRON_ANGLE, anchor)
    qc_two.ry(HOLOGRON_ANGLE, site2)
    qc_two.save_statevector()
    sv_two = np.asarray(sim.run(qc_two).result().get_statevector())
    sv_two = parity_project(sv_two, NQ)

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
        "dr": dr,
        "V": float(V),
        "V_connected": float(V_conn),
        "C_vac": float(C_vac),
        "C_two": float(C_two),
        "C_conn_vac": float(C_conn_vac),
        "C_conn_two": float(C_conn_two),
    })

# Fit
drs = np.array([d["dr"] for d in force_data])
Vs = np.array([d["V"] for d in force_data])
Vs_conn = np.array([d["V_connected"] for d in force_data])


def ads_force(r, C1, C2, xi):
    return C1 - C2 * np.exp(-r / xi)


# Fit both raw V and connected V
for label, v_arr in [("V_raw", Vs), ("V_conn", Vs_conn)]:
    try:
        popt, pcov = curve_fit(
            ads_force, drs, v_arr,
            p0=[0.0, 0.1, 1.5],
            bounds=([-1, -200, 0.01], [1, 200, 10]),
        )
        perr = np.sqrt(np.diag(pcov))
        print(f"\n  Fit ({label}): C1={popt[0]:.6f}  C2={popt[1]:.6f}  xi={popt[2]:.4f}")
        print(f"    errors: dC1={perr[0]:.4f}  dC2={perr[1]:.4f}  dxi={perr[2]:.4f}")
    except Exception as ex:
        print(f"\n  Fit ({label}) failed: {ex}")
        popt = [0, 0, 0]
        perr = [0, 0, 0]

    if label == "V_raw":
        C1_fit, C2_fit, xi_fit = popt
        fit_err = perr

print(f"\n  Theory: l_AdS=1.4427")
print(f"  Previous (no Z2): xi=1.233")

# ── Save ──
total_time = time.time() - T_GLOBAL

sv_final = get_sv(best_theta, project=True)
mag_final, par_final = diagnose(sv_final)

result = {
    "sim_id": "SIM-2026-005",
    "hypothesis_id": "HYP-2026-002",
    "fix": "Z2 parity projection onto P=+1 sector",
    "circuit": {
        "qubits": NQ,
        "layers": NLAYERS,
        "params": NP,
        "depth": qc_template.depth(),
    },
    "backend": "qiskit-aer CPU (statevector)",
    "exact_E0": E0,
    "E_optimized": float(best_E),
    "pct_error": float(pct_err),
    "magnetization": float(mag_final),
    "parity": float(par_final),
    "seed_results": seed_results,
    "control_no_z2": {
        "E": float(res_ctrl.fun),
        "magnetization": float(mag_ctrl),
        "parity": float(par_ctrl),
    },
    "force_profile": force_data,
    "fit": {
        "C1": float(C1_fit),
        "C2": float(C2_fit),
        "xi": float(xi_fit),
        "C1_err": float(fit_err[0]),
        "C2_err": float(fit_err[1]),
        "xi_err": float(fit_err[2]),
        "paper_l_AdS": 1.4427,
        "previous_no_z2_xi": 1.233,
    },
    "total_time_s": total_time,
}

out_path = "research/data/simulations/SIM-2026-005.json"
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)
np.save("research/data/simulations/theta_opt_SIM2026005.npy", best_theta)

print(f"\nSaved {out_path}")
print(f"Total time: {total_time:.0f}s ({total_time/60:.1f}m)")
print("=" * 65)
