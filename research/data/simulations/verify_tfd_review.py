"""
Adversarial verification of the TFD GO_WITH_CAVEAT verdict for HYP-2026-024.
Independent re-derivation. Builds the exact Wang-He boundary H at small L,
constructs |TFD(beta)>, traces out the ancilla, and tests every load-bearing claim.
"""
import numpy as np
from numpy.linalg import eigh

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def pauli_full(n, i, P):
    mats = [P if k == i else I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out


def build_H(L):
    """Wang-He Eq 1: L/(4pi) sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}], PBC."""
    dim = 2 ** L
    H = np.zeros((dim, dim), dtype=complex)
    pref = L / (4 * np.pi)
    Xs = [pauli_full(L, i, X) for i in range(L)]
    Zs = [pauli_full(L, i, Z) for i in range(L)]
    for j in range(L):
        jm1 = (j - 1) % L
        jp1 = (j + 1) % L
        H += pref * (Xs[jm1] @ Zs[j] @ Xs[jp1] - Xs[j] @ Xs[jp1])
    return H


def tfd_state(evals, evecs, beta):
    """|TFD> = (1/sqrt(Z)) sum_n exp(-beta E_n /2) |n>_L |n>_R, in computational basis."""
    dim = len(evals)
    w = np.exp(-beta * evals / 2.0)
    Zp = np.sum(w ** 2)  # = sum exp(-beta E_n)
    # |TFD> = sum_n (w_n/sqrt(Z)) |n>_L (x) |n>_R
    # |n> is the eigenvector evecs[:,n]. Build the 2^(2L) vector.
    psi = np.zeros(dim * dim, dtype=complex)
    for n in range(dim):
        vn = evecs[:, n]
        coeff = w[n] / np.sqrt(Zp)
        # |n>_L (x) |n>_R  as kron
        psi += coeff * np.kron(vn, vn)
    return psi, Zp


def reduced_phys(psi, dim):
    """Tr_R |psi><psi| where psi lives on dim_L (x) dim_R, both = dim."""
    M = psi.reshape(dim, dim)  # index [L, R]
    # rho_L = M M^dagger (trace over R)
    rho = M @ M.conj().T
    return rho


print("=" * 70)
print("CLAIM 1 & 4: rho_phys = exp(-beta H)/Z  and  beta->inf -> |gs><gs|")
print("=" * 70)
for L in [3, 4]:
    H = build_H(L)
    evals, evecs = eigh(H)
    dim = 2 ** L
    print(f"\nL={L}, dim={dim}, E0={evals[0]:.6f}, gap={evals[1]-evals[0]:.6f}")
    for beta in [0.3, 1.0, 5.0, 100.0]:
        psi, Zp = tfd_state(evals, evecs, beta)
        # norm check
        nrm = np.linalg.norm(psi)
        rho = reduced_phys(psi, dim)
        # thermal target exp(-beta H)/Z
        rho_th = evecs @ np.diag(np.exp(-beta * evals)) @ evecs.conj().T
        rho_th /= np.trace(rho_th).real
        diff = np.max(np.abs(rho - rho_th))
        # gs projector
        gs = evecs[:, 0]
        Pgs = np.outer(gs, gs.conj())
        diff_gs = np.max(np.abs(rho - Pgs))
        purity = np.trace(rho @ rho).real
        print(f"  beta={beta:6.1f}  |psi|={nrm:.6f}  max|rho-exp(-bH)/Z|={diff:.2e}  "
              f"purity={purity:.4f}  max|rho-|gs><gs||={diff_gs:.4f}")

print()
print("=" * 70)
print("CLAIM 2: ancilla evolution choice. Does ancilla NEED to evolve?")
print("Compare physical-half correlator under U_R = I, +H, -H against the")
print("ground-truth thermal real-time 2pt function Tr[U(t) Akick rho Akick^d U^d B].")
print("=" * 70)

L = 3
H = build_H(L)
evals, evecs = eigh(H)
dim = 2 ** L
beta = 2.0
psi0, Zp = tfd_state(evals, evecs, beta)

# physical-site operators tensored with identity on ancilla
Y0_phys = np.kron(pauli_full(L, 0, Y), np.eye(dim))      # Y on phys site 0
Z0_phys = np.kron(pauli_full(L, 0, Z), np.eye(dim))      # observable: Z on phys site 0
# Gaussian Y-kick on physical site 0: a small unitary kick exp(-i eps Y0)
eps = 0.3
Ykick_phys = np.kron(pauli_full(L, 0, Y), np.eye(dim))

import scipy.linalg as sla
H_phys = np.kron(H, np.eye(dim))
H_anc = np.kron(np.eye(dim), H)

# kick
Ukick = sla.expm(-1j * eps * Ykick_phys)
psi_kicked = Ukick @ psi0

def signal_under_ancilla(sign):
    """Evolve phys under +H, ancilla under sign*H. Measure <Z0_phys>(t)."""
    gen = H_phys + sign * H_anc
    ts = np.linspace(0, 4, 9)
    out = []
    for t in ts:
        U = sla.expm(-1j * gen * t)
        psi_t = U @ psi_kicked
        val = (psi_t.conj() @ (Z0_phys @ psi_t)).real
        out.append(val)
    return np.array(ts), np.array(out)

ts, sig_I = signal_under_ancilla(0.0)
_, sig_plus = signal_under_ancilla(+1.0)
_, sig_minus = signal_under_ancilla(-1.0)

# ground truth: thermal mixed-state correlator on physical Hilbert space alone
rho_th = evecs @ np.diag(np.exp(-beta * evals)) @ evecs.conj().T
rho_th /= np.trace(rho_th).real
Y0 = pauli_full(L, 0, Y)
Z0 = pauli_full(L, 0, Z)
Uk = sla.expm(-1j * eps * Y0)
rho_kicked = Uk @ rho_th @ Uk.conj().T
gt = []
for t in ts:
    Ut = sla.expm(-1j * H * t)
    rho_t = Ut @ rho_kicked @ Ut.conj().T
    gt.append(np.trace(rho_t @ Z0).real)
gt = np.array(gt)

print(f"\nL={L}, beta={beta}, eps_kick={eps}")
print(f"{'t':>5} {'anc=I':>12} {'anc=+H':>12} {'anc=-H':>12} {'thermal_GT':>12}")
for i, t in enumerate(ts):
    print(f"{t:5.2f} {sig_I[i]:12.8f} {sig_plus[i]:12.8f} {sig_minus[i]:12.8f} {gt[i]:12.8f}")
print(f"\nmax|anc=I  - GT| = {np.max(np.abs(sig_I - gt)):.2e}")
print(f"max|anc=+H - GT| = {np.max(np.abs(sig_plus - gt)):.2e}")
print(f"max|anc=-H - GT| = {np.max(np.abs(sig_minus - gt)):.2e}")

# Check (H_phys - H_anc)|TFD> = 0
gen_diff = H_phys - H_anc
resid = np.linalg.norm(gen_diff @ psi0)
print(f"\n||(H_phys - H_anc)|TFD>|| = {resid:.2e}  (TFD stationary under H_L - H_R?)")

print()
print("=" * 70)
print("CLAIM 3 (small-N killer): gap scaling and thermal participation")
print("Delta_E across L; N_eff(beta) participation ratio at L=8.")
print("=" * 70)
for L in [3, 4, 5, 6, 7, 8]:
    H = build_H(L)
    evals = np.linalg.eigvalsh(H)
    gap = evals[1] - evals[0]
    gap2 = evals[2] - evals[0]
    print(f"  L={L:2d}  E0={evals[0]:9.5f}  gap(E1-E0)={gap:.5f}  (E2-E0)={gap2:.5f}")
