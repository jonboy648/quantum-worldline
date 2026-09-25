"""
SIM-2026-015b: Force profile extraction from chi=3 MERA ground state (8q)
==========================================================================
Uses the optimized chi=3 MERA state from SIM-2026-015 (seed 42, 0.00% error)
to measure the holographic force profile V(dr).

Method:
  1. Rebuild chi=3 ground state from saved parameters
  2. Apply Zou-Milsted-Vidal boundary-primary operator at anchor site
  3. Measure interaction energy V(dr) = E_dual - E_0 - 2*dE_single
  4. Fit power-law V(dr) ~ A * dr^(-alpha)
  5. Compare to SIM-2026-011 (24q exact GS: alpha=3.92)

Key question: does the chi=3 ground state (which has correct C(r) ~ r^{-1/4})
give a cleaner force profile than the chi=2 state (which had flat C(r))?
"""
import numpy as np
import time
import json
from scipy.linalg import expm
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

N_QUBITS = 8
CHI = 3
DIM = 2 ** N_QUBITS
ANCHOR = 1  # boundary site (avoid edges for OBC)
DR_MAX = 5  # max separation (limited by 8 sites)

# Boundary-primary coefficients (Zou-Milsted-Vidal)
ALPHA_BP = 0.635
BETA_BP = -0.026

# ================================================================
# Pauli / Hamiltonian (same as sim2026015)
# ================================================================
_I = speye(2, format="csr", dtype=complex)
_X = csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Z = csr_matrix([[1, 0], [0, -1]], dtype=complex)
_PAULIS = {"I": _I, "X": _X, "Z": _Z}


def kron_pauli(n, qubit_ops):
    ops = [qubit_ops.get(q, "I") for q in range(n)]
    result = _PAULIS[ops[0]]
    for op in ops[1:]:
        result = skron(result, _PAULIS[op], format="csr")
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


# ================================================================
# MERA state builder (from sim2026015)
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


HP4 = hermitian_nparams(4)
HP9 = hermitian_nparams(9)


def build_mera_sv(params):
    offset = 0
    u1s = []
    for _ in range(4):
        u1s.append(make_unitary(params[offset:offset + HP4], 4))
        offset += HP4
    w1s = []
    for _ in range(4):
        w1s.append(make_isometry(params[offset:offset + HP4], 4, CHI))
        offset += HP4
    u2s = []
    for _ in range(2):
        u2s.append(make_unitary(params[offset:offset + HP9], 9))
        offset += HP9
    w2s = []
    for _ in range(2):
        w2s.append(make_isometry(params[offset:offset + HP9], 9, CHI))
        offset += HP9
    raw = params[offset:offset + 18]
    psi_top = raw[0::2] + 1j * raw[1::2]
    norm = np.linalg.norm(psi_top)
    if norm < 1e-15:
        psi_top = np.zeros(9, dtype=complex)
        psi_top[0] = 1.0
    else:
        psi_top /= norm

    state = psi_top.reshape(3, 3)
    state = w2s[0] @ state
    state = state @ w2s[1].T
    state = u2s[0].conj().T @ state
    state = state @ u2s[1].conj().T
    state = state.reshape(3, 3, 3, 3)
    state = np.einsum('ia,jb,kc,ld,abcd->ijkl',
                      w1s[0], w1s[1], w1s[2], w1s[3], state)
    state = np.einsum('Ii,Jj,Kk,Ll,ijkl->IJKL',
                      u1s[0].conj().T, u1s[1].conj().T,
                      u1s[2].conj().T, u1s[3].conj().T, state)
    sv = state.reshape(DIM)
    return sv


# ================================================================
# Boundary-primary operator
# ================================================================

def build_bp_operator(n, j):
    """sigma^boundary_j (Zou-Milsted-Vidal). Requires j+1 < n."""
    op = ALPHA_BP * (single_pauli(n, j, "X") + single_pauli(n, j + 1, "X"))
    op += BETA_BP * (two_pauli(n, j, "X", j + 1, "Z") +
                     two_pauli(n, j, "Z", j + 1, "X"))
    return op


# ================================================================
# Force extraction
# ================================================================

def expect(sv, op):
    return float(np.real(sv.conj() @ (op @ sv)))


def main():
    print("=" * 65)
    print("SIM-2026-015b: Force profile from chi=3 MERA (8q)")
    print("=" * 65)

    # Load optimized parameters from SIM-2026-015
    theta_path = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026015.npy"
    try:
        theta = np.load(theta_path)
        print(f"Loaded parameters from {theta_path}")
    except FileNotFoundError:
        print(f"ERROR: {theta_path} not found. Run sim2026015_chi3_8q.py first.")
        return

    # Rebuild chi=3 ground state
    print("\nRebuilding chi=3 MERA state...")
    gs_mera = build_mera_sv(theta)
    gs_mera = project_z2(gs_mera, N_QUBITS)

    # Build Hamiltonian and get exact GS for comparison
    H = build_tfim_obc(N_QUBITS)
    H_dense = H.toarray()
    E_exact_arr, gs_exact_arr = eigsh(H, k=1, which="SA")
    E0 = float(E_exact_arr[0])
    gs_exact = gs_exact_arr[:, 0]
    gs_exact = project_z2(gs_exact, N_QUBITS)

    E_mera = float(np.real(gs_mera.conj() @ H_dense @ gs_mera))
    err_mera = abs(E_mera - E0) / abs(E0) * 100
    print(f"E0_exact = {E0:.6f}")
    print(f"E_mera   = {E_mera:.6f}  ({err_mera:.4f}%)")

    # Force extraction on BOTH exact and MERA ground states
    valid_drs = [dr for dr in range(1, DR_MAX + 1) if ANCHOR + dr + 1 < N_QUBITS]

    for label, gs in [("EXACT", gs_exact), ("CHI3_MERA", gs_mera)]:
        print(f"\n{'='*65}")
        print(f"Force profile: {label} ground state")
        print(f"{'='*65}")

        E_gs = float(np.real(gs.conj() @ H_dense @ gs))

        # Single excitation at anchor
        sigma_a = build_bp_operator(N_QUBITS, ANCHOR)
        sv_single = sigma_a @ gs
        norm_s = np.linalg.norm(sv_single)
        sv_single = sv_single / norm_s
        E_single_a = float(np.real(sv_single.conj() @ H_dense @ sv_single))
        dE_single_a = E_single_a - E_gs

        print(f"  E_gs = {E_gs:.6f}")
        print(f"  Anchor = {ANCHOR}, ||sigma_a|GS>|| = {norm_s:.4f}")
        print(f"  dE_single(anchor) = {dE_single_a:.6f}")

        print(f"\n  {'dr':>4}  {'dE_single_p':>14}  {'E_dual':>14}  "
              f"{'V(dr)':>14}  {'|V(dr)|':>14}")

        V_data = {}
        for dr in valid_drs:
            j = ANCHOR + dr

            # Single excitation at probe
            sigma_p = build_bp_operator(N_QUBITS, j)
            sv_single_p = sigma_p @ gs
            norm_p = np.linalg.norm(sv_single_p)
            sv_single_p = sv_single_p / norm_p
            E_single_p = float(np.real(sv_single_p.conj() @ H_dense @ sv_single_p))
            dE_single_p = E_single_p - E_gs

            # Dual excitation: sigma at anchor AND probe
            sv_dual = sigma_p @ (sigma_a @ gs)
            norm_d = np.linalg.norm(sv_dual)
            sv_dual = sv_dual / norm_d
            E_dual = float(np.real(sv_dual.conj() @ H_dense @ sv_dual))

            # Interaction energy: V = E_dual - E_gs - dE_single_a - dE_single_p
            V = E_dual - E_gs - dE_single_a - dE_single_p
            V_data[dr] = V

            print(f"  {dr:>4d}  {dE_single_p:+14.8f}  {E_dual:+14.6f}  "
                  f"{V:+14.8f}  {abs(V):14.8f}")

        # Fit power law to |V(dr)|
        if len(V_data) >= 3:
            drs = sorted(V_data.keys())
            vs = [V_data[d] for d in drs]
            vs_abs = [abs(v) for v in vs]

            # Determine sign (attractive or repulsive)
            sign = -1 if vs[0] < 0 else 1
            vs_signed = [sign * v for v in vs]

            try:
                def powerlaw(x, A, alpha):
                    return A * np.power(np.array(x, dtype=float), -alpha)

                popt, pcov = curve_fit(powerlaw, drs, vs_signed,
                                       p0=[vs_signed[0], 2.0],
                                       maxfev=20000,
                                       bounds=([0, 0.1], [100, 10]))
                A, alpha = popt
                perr = np.sqrt(np.diag(pcov))
                dA, dalpha = perr

                print(f"\n  Power-law fit: V(dr) = {sign}*{A:.4f} * dr^(-{alpha:.2f})")
                print(f"    A = {A:.4f} +/- {dA:.4f}")
                print(f"    alpha = {alpha:.2f} +/- {dalpha:.2f}")
                print(f"    (stress-tensor prediction: alpha = 4.0)")
                print(f"    (24q exact result: alpha = 3.92 +/- 0.16)")
            except Exception as e:
                print(f"\n  Power-law fit failed: {e}")
                alpha, dalpha, A, dA = None, None, None, None
        else:
            print(f"\n  Too few points for fit ({len(V_data)})")
            alpha, dalpha, A, dA = None, None, None, None

    # Save results
    outpath = "D:/quantum-worldline/research/data/simulations/SIM-2026-015b.json"
    output = {
        "id": "SIM-2026-015b",
        "description": "Force profile from chi=3 MERA ground state (8q)",
        "n_qubits": N_QUBITS,
        "chi": CHI,
        "anchor": ANCHOR,
        "dr_values": valid_drs,
        "E0_exact": E0,
        "E_mera": E_mera,
        "mera_error_pct": err_mera,
        "V_data_exact": {str(k): float(v) for k, v in V_data.items()},
        "status": "COMPLETE",
    }
    with open(outpath, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {outpath}")


if __name__ == "__main__":
    main()
