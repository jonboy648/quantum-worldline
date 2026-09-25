"""
tci_schmidt_diagnostic.py
Schmidt spectrum and bond-dimension feasibility diagnostic for the TCI ground state.
Answers: what chi is needed to faithfully represent the TCI GS at the middle bond?
"""

import numpy as np
from scipy.sparse import kron as skron, csr_matrix
from scipy.sparse.linalg import eigsh

# ── Pauli building blocks ────────────────────────────────────────────────────
_I = csr_matrix(np.eye(2), dtype=complex)
_X = csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Z = csr_matrix([[1, 0], [0, -1]], dtype=complex)

LAMI = 1.0
LAM3_TCI = 0.856
LAM3_ISING = 0.0  # plain critical TFIM for reference


def sp(n, i, p):
    paulis = {"I": _I, "X": _X, "Z": _Z}
    mats = [paulis[p] if k == i else _I for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_OF(n, lam3):
    """O'Brien-Fendley Hamiltonian at given lam3, OBC.
    H = sum_j -2*LAMI*(X_j + Z_j Z_{j+1}) + lam3*(X_j Z_{j+1} Z_{j+2} + Z_j Z_{j+1} X_{j+2})"""
    H = csr_matrix((2 ** n, 2 ** n), dtype=complex)
    for j in range(n):
        H = H - 2 * LAMI * sp(n, j, "X")
        if j + 1 < n:
            H = H - 2 * LAMI * (sp(n, j, "Z") @ sp(n, j + 1, "Z"))
        if j + 2 < n:
            H = H + lam3 * (
                sp(n, j, "X") @ sp(n, j + 1, "Z") @ sp(n, j + 2, "Z")
                + sp(n, j, "Z") @ sp(n, j + 1, "Z") @ sp(n, j + 2, "X")
            )
    return H


def project_z2(sv, n):
    """Project onto Z2-even sector (even parity under product of all X)."""
    flip = sp(n, 0, "X")
    for k in range(1, n):
        flip = flip @ sp(n, k, "X")
    result = sv + flip @ sv
    norm = np.linalg.norm(result)
    return result / norm


def get_gs(n, lam3):
    """Return ground-state vector (Z2-projected, real)."""
    H = build_OF(n, lam3)
    vals, vecs = eigsh(H, k=2, which="SA")
    idx = np.argmin(vals)
    gs = np.array(vecs[:, idx], dtype=complex)
    gs = project_z2(gs, n)
    # make real (GS of this model is real up to a global phase)
    phase = np.exp(-1j * np.angle(gs[np.argmax(np.abs(gs))]))
    gs = np.real(gs * phase)
    gs /= np.linalg.norm(gs)
    return gs, float(vals[idx])


def schmidt_spectrum(gs, n, cut):
    """Compute Schmidt values at bipartition cut (left=cut sites, right=n-cut sites)."""
    psi = gs.reshape(2 ** cut, 2 ** (n - cut))
    sv = np.linalg.svd(psi, compute_uv=False)  # singular values, descending
    return sv


def entanglement_entropy(sv):
    """von Neumann entropy from Schmidt values (singular values)."""
    p = sv ** 2
    p = p[p > 1e-15]
    return float(-np.sum(p * np.log(p)))


def chi_fidelity_table(sv, max_chi=10):
    """For each chi, return truncation fidelity = sum of top-chi squared Schmidt values."""
    p = sv ** 2
    rows = []
    cum = 0.0
    for chi in range(1, max_chi + 1):
        if chi <= len(p):
            cum = float(np.sum(p[:chi]))
        else:
            cum = float(np.sum(p))
        err = 1.0 - cum
        rows.append((chi, cum, err))
    return rows


def print_table(rows, header="chi | fidelity  | trunc_err"):
    print(header)
    print("-" * 44)
    for chi, fid, err in rows:
        print(f"  {chi:2d}  |  {fid:.8f}  |  {err:.2e}")
    print()


def run_diagnostic(n, lam3, label):
    print("=" * 60)
    print(f"  {label}  (N={n}, lam3={lam3})")
    print("=" * 60)

    gs, E0 = get_gs(n, lam3)
    print(f"  Ground state energy E0 = {E0:.6f}")

    # ── Middle cut ──────────────────────────────────────────────
    cut_mid = n // 2
    sv_mid = schmidt_spectrum(gs, n, cut_mid)
    S_mid = entanglement_entropy(sv_mid)
    p_mid = sv_mid ** 2
    p_mid /= p_mid.sum()  # normalize squared SVs to probabilities

    print(f"\n  Middle cut ({cut_mid}|{n-cut_mid}):")
    print(f"  von Neumann S = {S_mid:.5f}")
    print(f"  Schmidt rank (nonzero to 1e-10) = {int(np.sum(p_mid > 1e-10))}")
    print("  Top-12 squared Schmidt values:")
    for i, p in enumerate(p_mid[:12]):
        print(f"    lambda^2[{i:2d}] = {float(p):.8f}")
    print()
    print("  chi-vs-fidelity (middle cut):")
    rows_mid = chi_fidelity_table(sv_mid, max_chi=10)
    print_table(rows_mid)

    # ── Off-center cuts ─────────────────────────────────────────
    for cut in [n // 4, 3 * n // 4]:
        sv_cut = schmidt_spectrum(gs, n, cut)
        S_cut = entanglement_entropy(sv_cut)
        p_cut = sv_cut ** 2
        p_cut /= p_cut.sum()
        print(f"  Off-center cut ({cut}|{n-cut}):")
        print(f"  von Neumann S = {S_cut:.5f}")
        print(f"  Schmidt rank = {int(np.sum(p_cut > 1e-10))}")
        rows_cut = chi_fidelity_table(sv_cut, max_chi=10)
        print_table(rows_cut)

    return S_mid, rows_mid


# ── Main ─────────────────────────────────────────────────────────────────────
print("\n=== TCI SCHMIDT FEASIBILITY DIAGNOSTIC ===\n")

# Step 4: Ising reference at N=16
print("\n--- ISING REFERENCE (N=16, lam3=0) ---\n")
S_ising_16, rows_ising_16 = run_diagnostic(16, LAM3_ISING, "Critical Ising (TFIM), N=16")

# Step 2 & 3: TCI at N=16
print("\n--- TCI MAIN DIAGNOSTIC (N=16, lam3=0.856) ---\n")
S_tci_16, rows_tci_16 = run_diagnostic(16, LAM3_TCI, "TCI (O'Brien-Fendley), N=16")

# Step 5: N-scaling for TCI
print("\n--- TCI N-SCALING (N=12, 14) ---\n")
for N in [12, 14]:
    run_diagnostic(N, LAM3_TCI, f"TCI (O'Brien-Fendley), N={N}")

# ── Summary ──────────────────────────────────────────────────────────────────
print("\n=== SUMMARY ===")
print(f"  Ising N=16  middle S = {S_ising_16:.5f}")
print(f"  TCI   N=16  middle S = {S_tci_16:.5f}")
print()
print("  chi-vs-fidelity comparison (middle cut, N=16):")
print(f"  {'chi':>4}  {'Ising fid':>12}  {'TCI fid':>12}  {'Ising err':>12}  {'TCI err':>12}")
for (chi, fid_i, err_i), (_, fid_t, err_t) in zip(rows_ising_16, rows_tci_16):
    print(f"  {chi:4d}  {fid_i:12.8f}  {fid_t:12.8f}  {err_i:12.2e}  {err_t:12.2e}")
print()
print("KEY CONCLUSION:")
# Find chi where TCI reaches 99% and 99.9%
for chi, fid, err in rows_tci_16:
    if fid >= 0.990:
        print(f"  TCI 99.0%% fidelity reached at chi={chi} (middle cut, N=16)")
        break
for chi, fid, err in rows_tci_16:
    if fid >= 0.999:
        print(f"  TCI 99.9%% fidelity reached at chi={chi} (middle cut, N=16)")
        break
for chi, fid, err in rows_ising_16:
    if fid >= 0.990:
        print(f"  Ising 99.0%% fidelity reached at chi={chi} (middle cut, N=16)")
        break
for chi, fid, err in rows_ising_16:
    if fid >= 0.999:
        print(f"  Ising 99.9%% fidelity reached at chi={chi} (middle cut, N=16)")
        break
print()
print("NOTE: These are MPS Schmidt requirements. A MERA disentangler reduces")
print("the effective entanglement at each bond, so the MERA chi needed is")
print("typically LOWER than the MPS Schmidt rank. These numbers are upper bounds.")
