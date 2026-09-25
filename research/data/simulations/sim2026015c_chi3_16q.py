"""
SIM-2026-015c: chi=3 MERA optimizer for 16-site transverse-field Ising model
=============================================================================
Extends SIM-2026-015 (8q chi=3) to 16 sites for force profile extraction.

Architecture (3 layers):
  Layer 1: 8x U(4) disentanglers + 8x (4->3) isometries  [256 params]
  Layer 2: 4x U(9) disentanglers + 4x (9->3) isometries  [648 params]
  Layer 3: 2x U(9) disentanglers + 2x (9->3) isometries  [324 params]
  Top tensor: C^9 normalized                               [18 params]
  Total: 1246 real parameters

Key differences from 8q:
  - 3 layers instead of 2
  - Hamiltonian MUST be sparse (65536x65536 dense = 68 GB)
  - Sequential tensor contraction for Layer 1 (8 tensors)
  - ~45 min per seed
"""
import sys
import numpy as np
import time

# Force unbuffered output so we can monitor progress
sys.stdout.reconfigure(line_buffering=True)
import json
from scipy.linalg import expm
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize

# ================================================================
# Configuration
# ================================================================
N_QUBITS = 16
CHI = 3
DIM = 2 ** N_QUBITS  # 65536
SEEDS = [42]  # single seed for ~45 min runtime

ALM_ROUNDS = 8
ALM_MAXFUN = 80000
ALM_MAXITER = 500
PROJ_MAXFUN = 80000
PROJ_MAXITER = 500

# ================================================================
# Pauli matrices and Hamiltonian (sparse only)
# ================================================================
_I = speye(2, format="csr", dtype=complex)
_X = csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Z = csr_matrix([[1, 0], [0, -1]], dtype=complex)


def sparse_pauli(n, i, p):
    paulis = {"I": _I, "X": _X, "Z": _Z}
    mats = [paulis[p] if k == i else _I for k in range(n)]
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
# Tensor parameterization
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


HP4 = hermitian_nparams(4)   # 16
HP9 = hermitian_nparams(9)   # 81

# Parameter layout:
# [0..127]:    8x u1 (Layer 1 disentanglers, U(4))        = 128
# [128..255]:  8x w1 (Layer 1 isometries, 4->3)           = 128
# [256..579]:  4x u2 (Layer 2 disentanglers, U(9))        = 324
# [580..903]:  4x w2 (Layer 2 isometries, 9->3)           = 324
# [904..1065]: 2x u3 (Layer 3 disentanglers, U(9))        = 162
# [1066..1227]:2x w3 (Layer 3 isometries, 9->3)           = 162
# [1228..1245]:top tensor (C^9)                            = 18
# Total: 1246
N_PARAMS = 8*HP4 + 8*HP4 + 4*HP9 + 4*HP9 + 2*HP9 + 2*HP9 + 18


def apply_to_axis(tensor, matrix, axis):
    """Apply matrix to specific axis: out[...,I,...] = sum_i M[I,i] * tensor[...,i,...]"""
    result = np.tensordot(matrix, tensor, axes=([1], [axis]))
    return np.moveaxis(result, 0, axis)


# ================================================================
# MERA state builder (16q, 3 layers)
# ================================================================

def build_mera_sv(params):
    """Build 16-qubit statevector from chi=3 MERA parameters."""
    offset = 0

    # Layer 1: 8x U(4) disentanglers
    u1s = []
    for _ in range(8):
        u1s.append(make_unitary(params[offset:offset + HP4], 4))
        offset += HP4

    # Layer 1: 8x (4->3) isometries
    w1s = []
    for _ in range(8):
        w1s.append(make_isometry(params[offset:offset + HP4], 4, CHI))
        offset += HP4

    # Layer 2: 4x U(9) disentanglers
    u2s = []
    for _ in range(4):
        u2s.append(make_unitary(params[offset:offset + HP9], 9))
        offset += HP9

    # Layer 2: 4x (9->3) isometries
    w2s = []
    for _ in range(4):
        w2s.append(make_isometry(params[offset:offset + HP9], 9, CHI))
        offset += HP9

    # Layer 3: 2x U(9) disentanglers
    u3s = []
    for _ in range(2):
        u3s.append(make_unitary(params[offset:offset + HP9], 9))
        offset += HP9

    # Layer 3: 2x (9->3) isometries
    w3s = []
    for _ in range(2):
        w3s.append(make_isometry(params[offset:offset + HP9], 9, CHI))
        offset += HP9

    # Top tensor
    raw = params[offset:offset + 18]
    psi_top = raw[0::2] + 1j * raw[1::2]
    norm = np.linalg.norm(psi_top)
    if norm < 1e-15:
        psi_top = np.zeros(9, dtype=complex)
        psi_top[0] = 1.0
    else:
        psi_top /= norm

    # === State preparation (top -> bottom) ===

    # Top: 2 virtual sites of dim 3
    state = psi_top.reshape(3, 3)

    # Layer 3: 2 sites -> 4 sites (compact matrix form)
    state = w3s[0] @ state            # (9, 3)
    state = state @ w3s[1].T          # (9, 9)
    state = u3s[0].conj().T @ state   # (9, 9)
    state = state @ u3s[1].conj().T   # (9, 9)
    state = state.reshape(3, 3, 3, 3)

    # Layer 2: 4 sites -> 8 sites (sequential tensordot — einsum without
    # optimize=True is 3000x slower due to bad contraction ordering)
    for k in range(4):
        state = apply_to_axis(state, w2s[k], k)
    # state: (9, 9, 9, 9)
    for k in range(4):
        state = apply_to_axis(state, u2s[k].conj().T, k)
    # Reshape to 8 virtual sites
    state = state.reshape(3, 3, 3, 3, 3, 3, 3, 3)

    # Layer 1: 8 virtual sites -> 8 qubit pairs (sequential)
    for k in range(8):
        state = apply_to_axis(state, w1s[k], k)
    # state: (4, 4, 4, 4, 4, 4, 4, 4)
    for k in range(8):
        state = apply_to_axis(state, u1s[k].conj().T, k)

    # Flatten to C^{2^16}
    sv = state.reshape(DIM)
    return sv


# ================================================================
# Observables
# ================================================================

def entanglement_entropy(sv, n_qubits, l):
    psi = sv.reshape(2**l, 2**(n_qubits - l))
    rho = psi @ psi.conj().T
    evals = np.linalg.eigvalsh(rho)
    evals = evals[evals > 1e-15]
    return float(-np.sum(evals * np.log(evals)))


def two_point_corr_sparse(sv, n_qubits, i, j):
    Zi = sparse_pauli(n_qubits, i, "Z")
    Zj = sparse_pauli(n_qubits, j, "Z")
    ZiZj = float(np.real(sv.conj() @ (Zi @ (Zj @ sv))))
    zi = float(np.real(sv.conj() @ (Zi @ sv)))
    zj = float(np.real(sv.conj() @ (Zj @ sv)))
    return ZiZj - zi * zj


# ================================================================
# Main
# ================================================================

print("=" * 65)
print("SIM-2026-015c: chi=3 MERA optimizer (16q TFIM)")
print("=" * 65)
print(f"Params: {N_PARAMS}, Qubits: {N_QUBITS}, Layers: 3, chi={CHI}")

# Build sparse Hamiltonian
print("\nBuilding 16q sparse Hamiltonian...")
t0 = time.time()
H_sp = build_tfim_obc(N_QUBITS)
P_sp = build_parity_op(N_QUBITS)
print(f"  H: {H_sp.shape}, nnz={H_sp.nnz}  ({time.time()-t0:.1f}s)")

# Exact ground state
print("Computing exact ground state (eigsh)...")
t0 = time.time()
E_exact, gs_arr = eigsh(H_sp, k=1, which="SA")
E0 = float(E_exact[0])
gs = gs_arr[:, 0]
print(f"  E0 = {E0:.6f}  ({time.time()-t0:.1f}s)")

eval_count = [0]
results = []

for seed in SEEDS:
    np.random.seed(seed)
    theta = np.random.uniform(-0.05, 0.05, N_PARAMS)
    eval_count[0] = 0
    t_seed = time.time()

    print(f"\n{'='*65}")
    print(f"[seed={seed}] Phase 1: ALM + L-BFGS-B, {ALM_ROUNDS} rounds")
    print(f"{'='*65}")

    mu = 0.0
    rho_alm = 1.0

    for rd in range(ALM_ROUNDS):
        cur_mu = mu
        cur_rho = rho_alm

        def alm_cost(p, _mu=cur_mu, _rho=cur_rho):
            sv = build_mera_sv(p)
            eval_count[0] += 1
            E = float(np.real(sv.conj() @ (H_sp @ sv)))
            pval = float(np.real(sv.conj() @ (P_sp @ sv)))
            g = (1.0 - pval) / 2.0
            return E + _mu * g + (_rho / 2.0) * g ** 2

        res = minimize(alm_cost, theta, method="L-BFGS-B",
                       options={"maxfun": ALM_MAXFUN, "maxiter": ALM_MAXITER})
        theta = res.x

        sv_check = build_mera_sv(theta)
        E_raw = float(np.real(sv_check.conj() @ (H_sp @ sv_check)))
        p_val = float(np.real(sv_check.conj() @ (P_sp @ sv_check)))
        g_val = (1.0 - p_val) / 2.0
        err = abs(E_raw - E0) / abs(E0) * 100

        mu = mu + rho_alm * g_val
        rho_alm = min(rho_alm * 2.0, 100.0)

        elapsed_rd = time.time() - t_seed
        print(f"  R{rd+1:2d}: E={E_raw:.4f} ({err:.2f}%)  <P>={p_val:.4f}  "
              f"mu={mu:.1f}  rho={rho_alm:.0f}  evals={eval_count[0]}  "
              f"[{elapsed_rd:.0f}s]", flush=True)

    E_alm = float(np.real(sv_check.conj() @ (H_sp @ sv_check)))
    P_alm = p_val
    err_alm = abs(E_alm - E0) / abs(E0) * 100

    # Phase 2: projected optimization
    print(f"\n[seed={seed}] Phase 2: Z2-projected L-BFGS-B")
    t_proj = time.time()

    def proj_cost(p):
        sv = build_mera_sv(p)
        sv = project_z2(sv, N_QUBITS)
        eval_count[0] += 1
        return float(np.real(sv.conj() @ (H_sp @ sv)))

    res_proj = minimize(proj_cost, theta, method="L-BFGS-B",
                        options={"maxfun": PROJ_MAXFUN, "maxiter": PROJ_MAXITER})
    theta_proj = res_proj.x

    sv_proj = build_mera_sv(theta_proj)
    sv_proj = project_z2(sv_proj, N_QUBITS)
    E_proj = float(np.real(sv_proj.conj() @ (H_sp @ sv_proj)))
    P_proj = float(np.real(sv_proj.conj() @ (P_sp @ sv_proj)))
    err_proj = abs(E_proj - E0) / abs(E0) * 100

    total_time = time.time() - t_seed
    print(f"  Projected: E={E_proj:.6f} ({err_proj:.2f}%)  <P>={P_proj:.4f}  "
          f"[{time.time()-t_proj:.0f}s]")

    # Pick best
    if E_proj < E_alm and abs(P_proj - 1.0) < 0.01:
        best_E, best_err, best_sv, best_theta = E_proj, err_proj, sv_proj, theta_proj
        best_method = "projected"
    else:
        sv_alm = build_mera_sv(theta)
        best_E, best_err, best_sv, best_theta = E_alm, err_alm, sv_alm, theta
        best_method = "ALM"

    print(f"\n  BEST: {best_method}, E={best_E:.6f} ({best_err:.2f}%)  "
          f"total={total_time:.0f}s")

    # Observables
    print("\n  Extracting observables...")
    S_half = entanglement_entropy(best_sv, N_QUBITS, N_QUBITS // 2)
    C_r = [two_point_corr_sparse(best_sv, N_QUBITS, 0, r) for r in range(1, 8)]

    print(f"  S({N_QUBITS//2}) = {S_half:.4f}")
    print(f"  C(r) = {[f'{c:.4f}' for c in C_r]}")

    # C(r) power-law check
    if abs(C_r[0]) > 1e-10:
        ratio = abs(C_r[3] / C_r[0])
        power_law = ratio < 0.8
        print(f"  C(4)/C(1) = {ratio:.3f}  {'power-law' if power_law else 'FLAT'}")

    results.append({
        "seed": seed,
        "best_method": best_method,
        "best_E": best_E, "best_err": best_err,
        "S_half": S_half, "C_r": C_r,
        "time_s": total_time,
    })

# Save
best_result = results[0]
print(f"\n{'='*65}")
print(f"SIM-2026-015c VERDICT")
print(f"{'='*65}")
print(f"  Energy: {best_result['best_E']:.6f} ({best_result['best_err']:.2f}%)")
print(f"  E0_exact: {E0:.6f}")
print(f"  S({N_QUBITS//2}): {best_result['S_half']:.4f}")
print(f"  C(r): {[f'{c:.4f}' for c in best_result['C_r']]}")
print(f"  Runtime: {best_result['time_s']:.0f}s")

outpath = "D:/quantum-worldline/research/data/simulations/SIM-2026-015c.json"
output = {
    "id": "SIM-2026-015c",
    "description": "chi=3 MERA 16-site TFIM",
    "n_qubits": N_QUBITS, "chi": CHI, "n_layers": 3, "n_params": N_PARAMS,
    "E0_exact": E0, "results": results,
    "best_E": best_result["best_E"], "best_error_pct": best_result["best_err"],
}
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

np.save("D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026015c.npy",
        best_theta)
print(f"\nSaved to {outpath}")
print("Saved theta to theta_opt_SIM2026015c.npy")
