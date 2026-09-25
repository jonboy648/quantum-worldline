"""
Reconciliation acid-test, ONE-SITE binary ascending scaling superoperator.

The disagreement: does the disentangler u appear in the one-site channel?
  - REPO sim041 _build_superop: NO u  (only w, O, w*)
  - first-principles-rg: YES u, two placements (O on left vs right lower leg of u), avg 1/2

Gate 1 (structural): S(I) = I  (lambda = 1 for identity).
Gate 2 (physics): critical-TFIM dims -> {0, 1/8, 1, 9/8, 2, ...}.

Conventions:
  u: (chi,chi,chi,chi)=(low0,low1,up0,up1), unitary as chi^2 x chi^2 (rows = lower pair).
  w: (chi,chi,chi)=(low0,low1,up), isometry: sum_{a,b} w[a,b,p] conj(w[a,b,q]) = delta_pq.
  Binary causal cone: u BELOW w; u's two UPPER legs feed two w lower legs of adjacent isometries.

A single coarse site = upper leg of ONE isometry w. Its two lower legs are fed by upper legs of
two DIFFERENT disentanglers (left u and right u), each shared with a neighbouring isometry that is
traced out. So a fine one-site operator enters on ONE lower leg of one of those disentanglers; the
partner lower leg + the neighbour structure are traced. Two inequivalent placements (left u / right u).
"""
import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import eigs

# ---------------- generic isometric (u,w) for the structural gate ----------------
def random_uw(chi, seed=0):
    rng = np.random.default_rng(seed)
    A = rng.standard_normal((chi * chi, chi * chi)) + 1j * rng.standard_normal((chi * chi, chi * chi))
    U, _ = np.linalg.qr(A)                       # unitary chi^2 x chi^2
    u = U.reshape(chi, chi, chi, chi)            # (low0,low1,up0,up1)
    B = rng.standard_normal((chi * chi, chi * chi)) + 1j * rng.standard_normal((chi * chi, chi * chi))
    Wf, _ = np.linalg.qr(B)
    w = Wf[:, :chi].reshape(chi, chi, chi)       # (low0,low1,up); w_dag w = I_chi
    return u, w


# ---------------- candidate A: REPO (no u) ----------------
def superop_no_u(u, w):
    chi = w.shape[0]
    wc = w.conj()
    dim = chi * chi
    S = np.zeros((dim, dim), complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), complex); O[i, j] = 1.0
            AL = np.einsum('abp,ac,cbq->pq', w, O, wc)   # O on left lower leg, trace right
            AR = np.einsum('abp,bd,adq->pq', w, O, wc)   # O on right lower leg, trace left
            S[:, i * chi + j] = (0.5 * (AL + AR)).reshape(dim)
    return S


# ---------------- candidate B: first-principles (with u) ----------------
# Ascending: fine 1-site O -> coarse 1-site. O sits on a lower leg of u; u's upper legs feed w.
# LEFT placement: O on u's LEFT lower leg (index c), trace the right child d.
#   A(O)[p,P] = sum  u[c,d,e,f] w[e,f,p] O[c,C] w*[E,F,P] u*[C,d,E,F]
# RIGHT placement: O on u's RIGHT lower leg (index d), trace left child c.
#   A(O)[p,P] = sum  u[c,d,e,f] w[e,f,p] O[d,D] w*[E,F,P] u*[c,D,E,F]
def superop_with_u(u, w):
    chi = w.shape[0]
    uc, wc = u.conj(), w.conj()
    dim = chi * chi
    S = np.zeros((dim, dim), complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), complex); O[i, j] = 1.0
            # u[low0,low1,up0,up1]=u[c,d,e,f]; w[low0,low1,up]=w[e,f,p]
            AL = np.einsum('cdef,efp,cC,CdEF,EFP->pP', u, w, O, uc, wc, optimize=True)
            AR = np.einsum('cdef,efp,dD,cDEF,EFP->pP', u, w, O, uc, wc, optimize=True)
            S[:, i * chi + j] = (0.5 * (AL + AR)).reshape(dim)
    return S


def check_identity(S, chi, name):
    I = np.eye(chi, dtype=complex).reshape(-1)
    out = (S @ I).reshape(chi, chi)
    err = np.linalg.norm(out - np.eye(chi)) / np.linalg.norm(np.eye(chi))
    print(f"  {name:14s}: S(I) rel-error = {err:.3e}   (gate 1 {'PASS' if err < 1e-10 else 'FAIL'})")
    return err


if __name__ == "__main__":
    print("=" * 64)
    print("GATE 1 (structural): S(I)=I, on a random isometric (u,w), chi=4")
    print("=" * 64)
    for seed in (0, 1, 2):
        u, w = random_uw(4, seed)
        print(f"seed {seed}:")
        check_identity(superop_no_u(u, w), 4, "no-u (repo)")
        check_identity(superop_with_u(u, w), 4, "with-u (FP)")
