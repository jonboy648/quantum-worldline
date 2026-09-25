"""
SIM-2026-015d: Force profile from chi=3 MERA ground state (16q)
================================================================
Uses optimized 16q chi=3 state from SIM-2026-015c (0.15% error).
With 16 sites, we get dr up to ~10 — enough to fit alpha.
"""
import sys
import numpy as np
import time
import json
from scipy.linalg import expm
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

sys.stdout.reconfigure(line_buffering=True)

N_QUBITS = 16
CHI = 3
DIM = 2 ** N_QUBITS
ANCHOR = 2
DR_MAX = 11  # anchor=2, need probe+1 < 16, so max probe=13, dr_max=11

ALPHA_BP = 0.635
BETA_BP = -0.026

# ================================================================
# Sparse operators
# ================================================================
_I = speye(2, format="csr", dtype=complex)
_X = csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Z = csr_matrix([[1, 0], [0, -1]], dtype=complex)


def kron_pauli(n, qubit_ops):
    ops = [qubit_ops.get(q, "I") for q in range(n)]
    paulis = {"I": _I, "X": _X, "Z": _Z}
    result = paulis[ops[0]]
    for op in ops[1:]:
        result = skron(result, paulis[op], format="csr")
    return result


def single_pauli(n, q, p):
    return kron_pauli(n, {q: p})


def two_pauli(n, q1, p1, q2, p2):
    return kron_pauli(n, {q1: p1, q2: p2})


def build_tfim_obc(n):
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=complex)
    for i in range(n - 1):
        H -= two_pauli(n, i, "Z", i + 1, "Z")
    for i in range(n):
        H -= single_pauli(n, i, "X")
    return H


def project_z2(sv, n_qubits):
    mask = (1 << n_qubits) - 1
    sv_flipped = sv[np.arange(len(sv)) ^ mask]
    sv_plus = sv + sv_flipped
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        return sv
    return sv_plus / norm


def build_bp_operator(n, j):
    op = ALPHA_BP * (single_pauli(n, j, "X") + single_pauli(n, j + 1, "X"))
    op += BETA_BP * (two_pauli(n, j, "X", j + 1, "Z") +
                     two_pauli(n, j, "Z", j + 1, "X"))
    return op


# ================================================================
# MERA state builder (16q, 3 layers — from sim2026015c)
# ================================================================

def params_to_hermitian(params, n):
    A = np.zeros((n, n), dtype=complex)
    idx = 0
    for i in range(n):
        A[i, i] = params[idx]; idx += 1
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


def apply_to_axis(tensor, matrix, axis):
    return np.moveaxis(np.tensordot(matrix, tensor, axes=([1], [axis])), 0, axis)


HP4, HP9 = 16, 81


def build_mera_sv(params):
    offset = 0
    u1s = [make_unitary(params[offset + k * HP4:offset + (k + 1) * HP4], 4) for k in range(8)]; offset += 8 * HP4
    w1s = [make_isometry(params[offset + k * HP4:offset + (k + 1) * HP4], 4, CHI) for k in range(8)]; offset += 8 * HP4
    u2s = [make_unitary(params[offset + k * HP9:offset + (k + 1) * HP9], 9) for k in range(4)]; offset += 4 * HP9
    w2s = [make_isometry(params[offset + k * HP9:offset + (k + 1) * HP9], 9, CHI) for k in range(4)]; offset += 4 * HP9
    u3s = [make_unitary(params[offset + k * HP9:offset + (k + 1) * HP9], 9) for k in range(2)]; offset += 2 * HP9
    w3s = [make_isometry(params[offset + k * HP9:offset + (k + 1) * HP9], 9, CHI) for k in range(2)]; offset += 2 * HP9
    raw = params[offset:offset + 18]
    psi_top = raw[0::2] + 1j * raw[1::2]
    psi_top /= np.linalg.norm(psi_top)

    state = psi_top.reshape(3, 3)
    state = w3s[0] @ state; state = state @ w3s[1].T
    state = u3s[0].conj().T @ state; state = state @ u3s[1].conj().T
    state = state.reshape(3, 3, 3, 3)
    for k in range(4): state = apply_to_axis(state, w2s[k], k)
    for k in range(4): state = apply_to_axis(state, u2s[k].conj().T, k)
    state = state.reshape(3, 3, 3, 3, 3, 3, 3, 3)
    for k in range(8): state = apply_to_axis(state, w1s[k], k)
    for k in range(8): state = apply_to_axis(state, u1s[k].conj().T, k)
    return state.reshape(DIM)


# ================================================================
# Main
# ================================================================

print("=" * 65)
print("SIM-2026-015d: Force profile from chi=3 MERA (16q)")
print("=" * 65)

theta = np.load("D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026015c.npy")
print(f"Loaded 16q chi=3 parameters ({len(theta)} params)")

print("Rebuilding MERA state...")
t0 = time.time()
gs_mera = build_mera_sv(theta)
gs_mera = project_z2(gs_mera, N_QUBITS)
print(f"  Done in {time.time()-t0:.1f}s")

H_sp = build_tfim_obc(N_QUBITS)
E_exact_arr, gs_exact_arr = eigsh(H_sp, k=1, which="SA")
E0 = float(E_exact_arr[0])
gs_exact = gs_exact_arr[:, 0]
gs_exact = project_z2(gs_exact, N_QUBITS)

E_mera = float(np.real(gs_mera.conj() @ (H_sp @ gs_mera)))
print(f"E0_exact = {E0:.6f}")
print(f"E_mera   = {E_mera:.6f}  ({abs(E_mera-E0)/abs(E0)*100:.4f}%)")

H_dense = H_sp.toarray()

valid_drs = [dr for dr in range(1, DR_MAX + 1) if ANCHOR + dr + 1 < N_QUBITS]
print(f"Anchor={ANCHOR}, dr=1..{max(valid_drs)}")

# Accumulate results for both exact and MERA states
all_results = {}

for label, gs in [("EXACT", gs_exact), ("CHI3_MERA", gs_mera)]:
    print(f"\n{'='*65}")
    print(f"Force profile: {label} ground state (16q)")
    print(f"{'='*65}")

    E_gs = float(np.real(gs.conj() @ H_dense @ gs))

    sigma_a = build_bp_operator(N_QUBITS, ANCHOR)
    sv_single_a = sigma_a @ gs
    norm_a = np.linalg.norm(sv_single_a)
    sv_single_a = sv_single_a / norm_a
    E_single_a = float(np.real(sv_single_a.conj() @ H_dense @ sv_single_a))
    dE_single_a = E_single_a - E_gs

    print(f"  E_gs = {E_gs:.6f}")
    print(f"  Anchor = {ANCHOR}, ||sigma_a|GS>|| = {norm_a:.4f}")
    print(f"  dE_single(anchor) = {dE_single_a:.6f}")

    print(f"\n  {'dr':>4}  {'dE_single_p':>14}  {'V(dr)':>14}  {'|V(dr)|':>14}")

    V_data = {}
    for dr in valid_drs:
        j = ANCHOR + dr
        sigma_p = build_bp_operator(N_QUBITS, j)
        sv_single_p = sigma_p @ gs
        norm_p = np.linalg.norm(sv_single_p)
        sv_single_p = sv_single_p / norm_p
        E_single_p = float(np.real(sv_single_p.conj() @ H_dense @ sv_single_p))
        dE_single_p = E_single_p - E_gs

        sv_dual = sigma_p @ (sigma_a @ gs)
        norm_d = np.linalg.norm(sv_dual)
        sv_dual = sv_dual / norm_d
        E_dual = float(np.real(sv_dual.conj() @ H_dense @ sv_dual))

        V = E_dual - E_gs - dE_single_a - dE_single_p
        V_data[dr] = V

        print(f"  {dr:>4d}  {dE_single_p:+14.8f}  {V:+14.8f}  {abs(V):14.8f}")

    # Fit power law to V(dr) for dr >= 2
    result_entry = {
        "E_gs": E_gs,
        "V_data": {str(k): float(v) for k, v in V_data.items()},
    }

    drs_fit = [dr for dr in sorted(V_data.keys()) if dr >= 2]
    if len(drs_fit) >= 4:
        vs = [V_data[d] for d in drs_fit]
        sign = -1 if vs[0] < 0 else 1
        vs_signed = [sign * v for v in vs]

        try:
            def powerlaw(x, A, alpha):
                return A * np.power(np.array(x, dtype=float), -alpha)

            popt, pcov = curve_fit(powerlaw, drs_fit, vs_signed,
                                   p0=[vs_signed[0] * 4, 3.0],
                                   maxfev=20000,
                                   bounds=([0, 0.1], [1000, 10]))
            A, alpha = popt
            perr = np.sqrt(np.diag(pcov))
            dA, dalpha = perr

            result_entry["alpha"] = float(alpha)
            result_entry["dalpha"] = float(dalpha)
            result_entry["A"] = float(A)
            result_entry["dA"] = float(dA)
            result_entry["sign"] = int(sign)
            result_entry["fit_dr_min"] = 2
            result_entry["fit_n_pts"] = len(drs_fit)

            print(f"\n  Power-law fit (dr>=2, n={len(drs_fit)} pts):")
            print(f"    V(dr) = {sign}*{A:.4f} * dr^(-{alpha:.2f})")
            print(f"    alpha = {alpha:.2f} +/- {dalpha:.2f}")
            print(f"    (stress-tensor prediction: alpha = 4.0)")
            print(f"    (24q exact result: alpha = 3.92 +/- 0.16)")
        except Exception as e:
            print(f"\n  Power-law fit failed: {e}")
    else:
        print(f"\n  Too few points for fit")

    key = "exact" if label == "EXACT" else "mera"
    all_results[key] = result_entry

runtime = time.time() - t0
print(f"\nTotal runtime: {runtime:.1f}s")

outpath = "D:/quantum-worldline/research/data/simulations/SIM-2026-015d.json"
output = {
    "id": "SIM-2026-015d",
    "description": "Force profile from exact and chi=3 MERA ground states (16q)",
    "n_qubits": N_QUBITS, "chi": CHI, "anchor": ANCHOR,
    "dr_values": valid_drs,
    "E0_exact": E0, "E_mera": E_mera,
    "exact": all_results["exact"],
    "mera": all_results["mera"],
    "status": "COMPLETE",
}
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)
print(f"Saved to {outpath}")
