"""
SIM-2026-015: chi=3 MERA optimizer for 8-site transverse-field Ising model
===========================================================================
Tests HYP-2026-009: bond dimension chi=2 -> chi=3 phase transition.

Architecture (state prep direction, top -> bottom):
  Layer 2: 2x U(9) disentanglers + 2x (9->3) isometries
  Layer 1: 4x U(4) disentanglers + 4x (4->3) isometries
  Top tensor: normalized C^9 vector
  Total: 470 real parameters (over-parameterized; true DOF ~392)

Key difference from chi=2 (sim2026008b):
  chi=2 used qubit gates (Ry, Rz, CX) on C^256 statevector.
  chi=3 uses tensor network contraction: top C^9 -> expand through
  isometries and disentanglers to C^256. Matrix exponential
  parameterization ensures unitarity/isometry constraints.
"""
import numpy as np
import time
import json
from scipy.linalg import expm, eigvalsh
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize

# ================================================================
# Configuration
# ================================================================
N_QUBITS = 8
CHI = 3
DIM = 2 ** N_QUBITS  # 256
SEEDS = [7, 42, 99]

ALM_ROUNDS = 10
ALM_MAXFUN = 15000
ALM_MAXITER = 500
PROJ_MAXFUN = 40000
PROJ_MAXITER = 800

# ================================================================
# Pauli matrices and Hamiltonian
# ================================================================
I2 = np.eye(2, dtype=complex)
Xm = np.array([[0, 1], [1, 0]], dtype=complex)
Zm = np.array([[1, 0], [0, -1]], dtype=complex)


def sparse_pauli(n, i, p):
    paulis = {"I": speye(2, format="csr"), "X": csr_matrix(Xm), "Z": csr_matrix(Zm)}
    mats = [paulis[p] if k == i else paulis["I"] for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_tfim_obc(n):
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=complex)
    for i in range(n - 1):
        H -= sparse_pauli(n, i, "Z") @ sparse_pauli(n, i + 1, "Z")
    for i in range(n):
        H -= sparse_pauli(n, i, "X")
    return H


def build_parity_op(n):
    P = sparse_pauli(n, 0, "X")
    for i in range(1, n):
        P = P @ sparse_pauli(n, i, "X")
    return P


def project_z2(sv, n_qubits):
    mask = (1 << n_qubits) - 1
    sv_flipped = sv[np.arange(len(sv)) ^ mask]
    sv_plus = sv + sv_flipped
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        return sv
    return sv_plus / norm


# ================================================================
# Tensor parameterization via matrix exponential
# ================================================================

def hermitian_nparams(n):
    return n * n


def params_to_hermitian(params, n):
    A = np.zeros((n, n), dtype=complex)
    idx = 0
    for i in range(n):
        A[i, i] = params[idx]
        idx += 1
    for i in range(n):
        for j in range(i + 1, n):
            A[i, j] = params[idx] + 1j * params[idx + 1]
            A[j, i] = params[idx] - 1j * params[idx + 1]
            idx += 2
    return A


def make_unitary(params, n):
    return expm(1j * params_to_hermitian(params, n))


def make_isometry(params, n_big, n_small):
    return make_unitary(params, n_big)[:, :n_small]


# ================================================================
# MERA state builder (top-down tensor contraction)
# ================================================================

HP4 = hermitian_nparams(4)   # 16
HP9 = hermitian_nparams(9)   # 81
N_PARAMS = 4 * HP4 + 4 * HP4 + 2 * HP9 + 2 * HP9 + 18  # 470


def build_mera_sv(params):
    """
    Build 8-qubit statevector from chi=3 MERA parameters.

    State preparation (top -> bottom):
    1. Top tensor psi_top in C^9 = C^3 x C^3
    2. Layer 2: expand via W2 isometries, apply U2 adjoint
    3. Layer 1: expand via W1 isometries, apply U1 adjoint
    Result: statevector in C^256
    """
    offset = 0

    # Unpack Layer 1 disentanglers: 4x U(4)
    u1s = []
    for _ in range(4):
        u1s.append(make_unitary(params[offset:offset + HP4], 4))
        offset += HP4

    # Unpack Layer 1 isometries: 4x (4 -> 3)
    w1s = []
    for _ in range(4):
        w1s.append(make_isometry(params[offset:offset + HP4], 4, CHI))
        offset += HP4

    # Unpack Layer 2 disentanglers: 2x U(9)
    u2s = []
    for _ in range(2):
        u2s.append(make_unitary(params[offset:offset + HP9], 9))
        offset += HP9

    # Unpack Layer 2 isometries: 2x (9 -> 3)
    w2s = []
    for _ in range(2):
        w2s.append(make_isometry(params[offset:offset + HP9], 9, CHI))
        offset += HP9

    # Top tensor: C^9 normalized
    raw = params[offset:offset + 18]
    psi_top = raw[0::2] + 1j * raw[1::2]
    norm = np.linalg.norm(psi_top)
    if norm < 1e-15:
        psi_top = np.zeros(9, dtype=complex)
        psi_top[0] = 1.0
    else:
        psi_top /= norm

    # --- State preparation ---

    # Top: 2 virtual sites of dim 3
    state = psi_top.reshape(3, 3)

    # Layer 2 isometry expansion: C^3 -> C^9 per site
    state = w2s[0] @ state       # (9, 3): expand first top index
    state = state @ w2s[1].T     # (9, 9): expand second top index

    # Layer 2 disentangler adjoints
    state = u2s[0].conj().T @ state       # U2[0]^dag on first pair (AB)
    state = state @ u2s[1].conj().T       # U2[1]^dag on second pair (CD)

    # Now (9, 9) = 4 virtual sites of dim 3: reshape to (3,3,3,3)
    state = state.reshape(3, 3, 3, 3)

    # Layer 1 isometry expansion: each C^3 -> C^4 = C^2 x C^2
    state = np.einsum('ia,jb,kc,ld,abcd->ijkl',
                      w1s[0], w1s[1], w1s[2], w1s[3], state)

    # Layer 1 disentangler adjoints: each U1[k]^dag on its qubit pair
    state = np.einsum('Ii,Jj,Kk,Ll,ijkl->IJKL',
                      u1s[0].conj().T, u1s[1].conj().T,
                      u1s[2].conj().T, u1s[3].conj().T, state)

    # Flatten to C^256 statevector
    sv = state.reshape(DIM)
    return sv, psi_top


# ================================================================
# Observables
# ================================================================

def entanglement_entropy(sv, l):
    """Von Neumann entropy S(l) for first l qubits."""
    psi = sv.reshape(2**l, 2**(N_QUBITS - l))
    rho = psi @ psi.conj().T
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def top_tensor_entropy(psi_top):
    """Bipartite entropy of top tensor on C^3 x C^3."""
    mat = psi_top.reshape(CHI, CHI)
    rho = mat @ mat.conj().T
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def two_point_corr(sv, i, j, Zops):
    """Connected correlator <ZiZj> - <Zi><Zj>."""
    ZiZj = np.real(sv.conj() @ Zops[i] @ Zops[j] @ sv)
    Zi = np.real(sv.conj() @ Zops[i] @ sv)
    Zj = np.real(sv.conj() @ Zops[j] @ sv)
    return float(ZiZj - Zi * Zj)


def extract_observables(sv, psi_top, Zops):
    """Compute all observables from optimized statevector."""
    obs = {}
    obs["S_l"] = [entanglement_entropy(sv, l) for l in range(1, N_QUBITS)]
    obs["S_top"] = top_tensor_entropy(psi_top) if psi_top is not None else None
    obs["S_half"] = obs["S_l"][N_QUBITS // 2 - 1]
    obs["C_r"] = [two_point_corr(sv, 0, r, Zops) for r in range(1, N_QUBITS)]
    return obs


# ================================================================
# Main
# ================================================================

print("=" * 65)
print("SIM-2026-015: chi=3 MERA optimizer (8q TFIM)")
print("=" * 65)

H = build_tfim_obc(N_QUBITS)
P_op = build_parity_op(N_QUBITS)
H_dense = H.toarray()
P_dense = P_op.toarray()

# Exact ground state
E_exact, gs_exact = eigsh(H, k=1, which="SA")
E0 = float(E_exact[0])
gs = gs_exact[:, 0]
gs = project_z2(gs, N_QUBITS)

# Pre-compute Z operators for correlations
Zops = [sparse_pauli(N_QUBITS, i, "Z").toarray() for i in range(N_QUBITS)]

# Exact observables for comparison
exact_obs = extract_observables(gs, None, Zops)
exact_obs["S_top"] = None  # not defined for exact GS

print(f"E0_exact = {E0:.6f}")
print(f"Params: {N_PARAMS} (chi={CHI}, 2 layers)")
print(f"Exact S(4) = {exact_obs['S_half']:.4f}")
print(f"Exact C(1..4) = {[f'{c:.4f}' for c in exact_obs['C_r'][:4]]}")

eval_count = [0]
results = []
best_E_global = None
best_params_global = None
best_seed_global = None

for seed in SEEDS:
    np.random.seed(seed)
    theta = np.random.uniform(-0.1, 0.1, N_PARAMS)
    eval_count[0] = 0
    t0 = time.time()

    print(f"\n{'='*65}")
    print(f"[seed={seed}] Phase 1: ALM + L-BFGS-B, {ALM_ROUNDS} rounds")
    print(f"{'='*65}")

    mu = 0.0
    rho_alm = 1.0

    for rd in range(ALM_ROUNDS):
        cur_mu = mu
        cur_rho = rho_alm

        def alm_cost(p, _mu=cur_mu, _rho=cur_rho):
            sv, _ = build_mera_sv(p)
            eval_count[0] += 1
            E = np.real(sv.conj() @ H_dense @ sv)
            pval = np.real(sv.conj() @ P_dense @ sv)
            g = (1.0 - pval) / 2.0
            return E + _mu * g + (_rho / 2.0) * g ** 2

        res = minimize(alm_cost, theta, method="L-BFGS-B",
                       options={"maxfun": ALM_MAXFUN, "maxiter": ALM_MAXITER})
        theta = res.x

        sv_check, _ = build_mera_sv(theta)
        E_raw = float(np.real(sv_check.conj() @ H_dense @ sv_check))
        p_val = float(np.real(sv_check.conj() @ P_dense @ sv_check))
        g_val = (1.0 - p_val) / 2.0
        err = abs(E_raw - E0) / abs(E0) * 100

        mu = mu + rho_alm * g_val
        rho_alm = min(rho_alm * 2.0, 100.0)

        print(f"  R{rd+1:2d}: E={E_raw:.4f} ({err:.2f}%)  <P>={p_val:.4f}  "
              f"mu={mu:.1f}  rho={rho_alm:.0f}  evals={eval_count[0]}", flush=True)

    elapsed_alm = time.time() - t0
    sv_alm, psi_top_alm = build_mera_sv(theta)
    E_alm = float(np.real(sv_alm.conj() @ H_dense @ sv_alm))
    P_alm = float(np.real(sv_alm.conj() @ P_dense @ sv_alm))
    err_alm = abs(E_alm - E0) / abs(E0) * 100

    # Phase 2: projected optimization
    print(f"\n[seed={seed}] Phase 2: Z2-projected L-BFGS-B, {PROJ_MAXFUN} evals")
    t1 = time.time()

    def proj_cost(p):
        sv, _ = build_mera_sv(p)
        sv = project_z2(sv, N_QUBITS)
        eval_count[0] += 1
        return np.real(sv.conj() @ H_dense @ sv)

    res_proj = minimize(proj_cost, theta, method="L-BFGS-B",
                        options={"maxfun": PROJ_MAXFUN, "maxiter": PROJ_MAXITER})
    theta_proj = res_proj.x
    elapsed_proj = time.time() - t1

    sv_proj, psi_top_proj = build_mera_sv(theta_proj)
    sv_proj = project_z2(sv_proj, N_QUBITS)
    E_proj = float(np.real(sv_proj.conj() @ H_dense @ sv_proj))
    P_proj = float(np.real(sv_proj.conj() @ P_dense @ sv_proj))
    err_proj = abs(E_proj - E0) / abs(E0) * 100

    # Pick best
    if E_proj < E_alm and abs(P_proj - 1.0) < 0.01:
        best_E = E_proj
        best_err = err_proj
        best_sv = sv_proj
        best_psi_top = psi_top_proj
        best_theta = theta_proj
        best_method = "projected"
    else:
        best_E = E_alm
        best_err = err_alm
        best_sv = sv_alm
        best_psi_top = psi_top_alm
        best_theta = theta
        best_method = "ALM"

    total_time = time.time() - t0

    print(f"\n  seed={seed} RESULTS:")
    print(f"    ALM:       E={E_alm:.6f} ({err_alm:.2f}%)  <P>={P_alm:.4f}  {elapsed_alm:.0f}s")
    print(f"    Projected: E={E_proj:.6f} ({err_proj:.2f}%)  <P>={P_proj:.4f}  {elapsed_proj:.0f}s")
    print(f"    BEST: {best_method}, E={best_E:.6f} ({best_err:.2f}%)  total={total_time:.0f}s")

    # Observables
    obs = extract_observables(best_sv, best_psi_top, Zops)
    S_top = obs["S_top"]

    print(f"    S_top = {S_top:.4f}  (max={np.log(CHI):.4f}=log({CHI}))")
    print(f"    S(4)  = {obs['S_half']:.4f}  (exact={exact_obs['S_half']:.4f})")
    print(f"    C(r)  = {[f'{c:.3f}' for c in obs['C_r'][:4]]}")

    if best_E_global is None or best_E < best_E_global:
        best_E_global = best_E
        best_params_global = best_theta.copy()
        best_seed_global = seed

    results.append({
        "seed": seed,
        "alm_E": E_alm, "alm_err": err_alm, "alm_P": P_alm,
        "proj_E": E_proj, "proj_err": err_proj, "proj_P": P_proj,
        "best_method": best_method, "best_E": best_E, "best_err": best_err,
        "S_top": S_top, "S_half": obs["S_half"],
        "S_l": obs["S_l"], "C_r": obs["C_r"],
        "time_s": total_time,
    })


# ================================================================
# Summary and HYP-2026-009 assessment
# ================================================================

best_result = min(results, key=lambda r: r["best_E"])
best_error = best_result["best_err"]
best_S_top = best_result["S_top"]

# Phase transition test: does S_top jump from ~log(2) to ~log(3)?
S_top_chi2 = np.log(2)  # 0.693
S_top_chi3_max = np.log(3)  # 1.099
jump_ratio = best_S_top / S_top_chi3_max if S_top_chi3_max > 0 else 0
phase_transition = best_S_top > S_top_chi2 * 1.2  # 20% above chi=2 bound

# C(r) power-law test: does C(r) decay (not flat)?
C_values = best_result["C_r"][:4]
C_ratio = abs(C_values[-1] / C_values[0]) if abs(C_values[0]) > 1e-10 else 1.0
power_law = C_ratio < 0.8  # significant decay from C(1) to C(4)

energy_ok = best_error < 1.0
verdict = "PASS" if energy_ok else "PARTIAL" if best_error < 3.0 else "FAIL"

print(f"\n{'='*65}")
print(f"SIM-2026-015 VERDICT: {verdict}")
print(f"{'='*65}")
print(f"  Best seed: {best_result['seed']}, method: {best_result['best_method']}")
print(f"  Energy: {best_result['best_E']:.6f} ({best_error:.2f}%)")
print(f"  S_top:  {best_S_top:.4f} / {S_top_chi3_max:.4f} = {jump_ratio:.1%} of max")
print(f"  Phase transition signal: {'YES' if phase_transition else 'NO'}")
print(f"    (S_top={best_S_top:.4f} {'>' if phase_transition else '<='} "
      f"{S_top_chi2*1.2:.4f} = 1.2*log(2))")
print(f"  C(r) power-law: {'YES' if power_law else 'NO (flat)'}")
print(f"    C(1)={C_values[0]:.4f}  C(4)={C_values[3]:.4f}  ratio={C_ratio:.3f}")
print()
print(f"  HYP-2026-009 assessment:")
if phase_transition and power_law:
    print(f"    SUPPORTED: S_top jumped above log(2), C(r) shows decay.")
elif phase_transition:
    print(f"    PARTIAL: S_top jumped but C(r) still flat.")
elif power_law:
    print(f"    PARTIAL: C(r) improved but S_top didn't jump.")
else:
    print(f"    NOT SUPPORTED at 8 sites. May need larger N.")
print(f"{'='*65}")

# Save results
output = {
    "id": "SIM-2026-015",
    "description": "chi=3 MERA optimizer for 8-site TFIM (HYP-2026-009)",
    "n_qubits": N_QUBITS, "chi": CHI, "n_layers": 2,
    "n_params": N_PARAMS,
    "E0_exact": E0,
    "exact_S_half": exact_obs["S_half"],
    "exact_C_r": exact_obs["C_r"],
    "results": results,
    "best_E": best_result["best_E"],
    "best_error_pct": best_error,
    "best_S_top": best_S_top,
    "S_top_chi2_bound": float(S_top_chi2),
    "S_top_chi3_max": float(S_top_chi3_max),
    "phase_transition_signal": bool(phase_transition),
    "power_law_signal": bool(power_law),
    "verdict": verdict,
}

outpath = "D:/quantum-worldline/research/data/simulations/SIM-2026-015.json"
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {outpath}")

# Save best parameters
np.save("D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026015.npy",
        best_params_global)
print("Saved theta to theta_opt_SIM2026015.npy")
