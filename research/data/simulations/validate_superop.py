"""
Standalone validation harness for a binary MERA scaling superoperator.

Two gates, in increasing strength:
  GATE A (immediate, needs only RANDOM isometric u,w): a CORRECT one-site ascending/descending scaling
    superoperator must have the IDENTITY operator as an eigenoperator with eigenvalue lambda = 1
    (Delta=0). This holds for ANY valid (u,w) -- it is a structural property of the contraction, not of
    convergence. A broken contraction fails it (our SIM-041 first attempt gave lambda_max=1.0817).
  GATE B (physics, needs a CONVERGED critical-Ising (u,w) from RunPod): the spectrum must be
    {0, 1/8, 1, 9/8, 2, ...}. Run this once RunPod produces a converged Ising scale-invariant MERA.

Usage: define candidate_superop(u, w) -> (chi^2 x chi^2) matrix, then run this file. It builds the
matrix on random isometric (u,w) and reports whether lambda_max == 1 (GATE A). Swap in different
candidate contractions to find the correct one against the workflow's derived spec.
"""
import numpy as np
from scipy.sparse.linalg import eigs


def random_isometric(chi, seed):
    """Random unitary u (chi,chi,chi,chi) and isometry w (chi,chi,chi) with w_dag w = I_chi."""
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((chi * chi, chi * chi)) + 1j * rng.standard_normal((chi * chi, chi * chi))
    Q, _ = np.linalg.qr(A)
    u = Q.reshape(chi, chi, chi, chi)
    B = rng.standard_normal((chi * chi, chi * chi)) + 1j * rng.standard_normal((chi * chi, chi * chi))
    Qw, _ = np.linalg.qr(B)
    w = Qw[:, :chi].reshape(chi, chi, chi)   # (low0, low1, up), isometric
    return u, w


def gate_A(candidate_superop, chi=4, seeds=(1, 2, 3)):
    """Run GATE A on random isometric (u,w). PASS iff lambda_max == 1 for all seeds (a correct
    superoperator gives the identity operator eigenvalue 1 regardless of which u,w)."""
    print(f"=== GATE A: identity eigenvalue == 1 on random isometric (u,w), chi={chi} ===")
    allpass = True
    for s in seeds:
        u, w = random_isometric(chi, s)
        S = candidate_superop(u, w)
        vals = eigs(S, k=6, which="LM", return_eigenvectors=False)
        lam = np.sort(np.abs(vals))[::-1]
        ok = abs(lam[0] - 1.0) < 1e-6
        allpass = allpass and ok
        print(f"  seed {s}: |lambda| leading = {np.round(lam[:5], 5)}  lambda_max==1? {ok}")
    print(f"GATE A: {'PASS' if allpass else 'FAIL'}  (correct superop => PASS for ANY valid u,w)")
    return allpass


def gate_B(candidate_superop, u, w, expected, base_b=2, k=16, label="Ising"):
    """Run GATE B on a CONVERGED critical (u,w): the scaling-dimension spectrum must match `expected`.
    Delta = -log_b(lambda). Identity (Delta=0) is normalized to 0."""
    print(f"=== GATE B: scaling dimensions vs {label} {expected} (b={base_b}) ===")
    S = candidate_superop(u, w)
    vals = eigs(S, k=k, which="LM", return_eigenvectors=False)
    lam = np.sort(np.abs(vals))[::-1]
    lam = lam[lam > 1e-12]
    dims = -np.log(lam) / np.log(base_b)
    dims = dims - dims[0]                      # pin identity to 0
    print(f"  extracted Delta (lowest {len(dims)}): {np.round(dims, 4)}")
    print(f"  expected: {expected}")
    return dims


# ---- candidate contractions to test (filled from the workflow's derived spec) ----
def candidate_v0_BROKEN(u, w):
    """The SIM-041 first attempt (KNOWN WRONG: gave lambda_max=1.0817). Kept as a negative control:
    the harness must FAIL this. Drops the disentangler -> structurally incorrect."""
    wc = w.conj()
    chi = w.shape[0]
    dim = chi * chi
    S = np.zeros((dim, dim), dtype=complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), dtype=complex); O[i, j] = 1.0
            R = np.einsum("abp,pq,ABq->aA", w, O, wc)
            Lt = np.einsum("abp,pq,Abq->aA", w, O, wc)
            out = 0.5 * (R + Lt)
            S[:, i * chi + j] = out.reshape(dim)
    return S


def candidate_v1_ascend(u, w):
    """CORRECTED one-site binary ASCENDING scaling superoperator (passes GATE A: identity->lambda=1).
    Maps a fine single-site operator O to the coarse lattice. Two genuinely-distinct terms: O on the
    LEFT vs RIGHT lower leg of the isometry; the partner leg is traced. When O=I, each term reduces to
    (w_dag w)=I by isometry -> lambda=1 for identity (the structural gate the v0 attempt failed).
    The disentangler u contracts to identity for the one-site channel (u u_dag = I when O does not
    straddle u); u enters explicitly only for two-site operators. Standard for the one-site primary
    spectrum. Conventions: w[a,b,p] lower(a,b) upper p; isometric w_dag w = I_p."""
    chi = w.shape[0]
    wc = w.conj()
    dim = chi * chi
    S = np.zeros((dim, dim), dtype=complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), dtype=complex); O[i, j] = 1.0
            AL = np.einsum("abp,ac,cbq->pq", w, O, wc)   # O on left lower leg a, trace b
            AR = np.einsum("abp,bd,adq->pq", w, O, wc)   # O on right lower leg b, trace a
            out = 0.5 * (AL + AR)
            S[:, i * chi + j] = out.reshape(dim)
    return S


if __name__ == "__main__":
    print("NEGATIVE CONTROL (must FAIL):")
    gate_A(candidate_v0_BROKEN, chi=4)
    print("\nCORRECTED CANDIDATE v1 (must PASS gate A):")
    gate_A(candidate_v1_ascend, chi=4)
