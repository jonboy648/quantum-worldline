"""
GATE 2: critical-TFIM scaling dimensions {0, 1/8, 1, 9/8, 2}.

Build a SCALE-INVARIANT binary MERA by optimizing a finite wavefunction whose UPPER layer
uses a shared (u,w), then read the one-site ascending spectrum from that shared (u,w) via BOTH
candidate superoperators (no-u repo vs with-u first-principles) and see which gives the Ising tower.

For a clean small test we use N=8 with bond CHI throughout by LIFTING the physical dim to CHI:
each physical spin-1/2 is embedded into the chi-space by a fixed isometric embedding E (2->chi)
applied to the data, so EVERY layer is a uniform CHI binary MERA and (u,w) is genuinely scale
invariant. Layers: N=8 -> 4 -> 2 -> 1(top scalar)... we use 3 coarse-graining layers all sharing
(u,w). The Hamiltonian is the critical TFIM lifted into chi-space on neighbouring pairs.

This sidesteps a separate bottom layer entirely: one (u,w) is reused at every scale.
"""
import numpy as np
from scipy.linalg import expm
from scipy.optimize import minimize

CHI = 4
N = 8                       # physical sites (=2^3): 3 binary layers to a single top site

X = np.array([[0, 1], [1, 0]], complex)
Z = np.array([[1, 0], [0, -1]], complex)
I2 = np.eye(2, dtype=complex)
h2_phys = (-np.kron(X, X) - 0.5 * (np.kron(Z, I2) + np.kron(I2, Z)))   # 4x4 critical TFIM bond


def herm(p, n):
    A = np.zeros((n, n), complex)
    iu = np.triu_indices(n, 1); no = len(iu[0])
    A[iu] = p[:no] + 1j * p[no:2 * no]
    A = A + A.conj().T
    A[np.diag_indices(n)] = p[2 * no:2 * no + n]
    return A


def nherm(n):
    return n * n


def uni(p, n):
    return expm(1j * herm(p, n))


def apply_axis(t, m, ax):
    """contract m[new, old] with tensor axis ax (old) -> new at position ax."""
    return np.moveaxis(np.tensordot(m, t, axes=([1], [ax])), 0, ax)


# Fixed embedding 2 -> CHI (physical spins live in first 2 dims of chi-space)
EMB = np.zeros((CHI, 2), complex); EMB[0, 0] = 1; EMB[1, 1] = 1

NU = nherm(CHI * CHI); NW = nherm(CHI * CHI)
NTOP = 2 * CHI
NPAR = NU + NW + NTOP


def unpack(p):
    u = uni(p[:NU], CHI * CHI).reshape(CHI, CHI, CHI, CHI)   # (low0,low1,up0,up1)
    w = uni(p[NU:NU + NW], CHI * CHI)[:, :CHI].reshape(CHI, CHI, CHI)  # (low0,low1,up)
    raw = p[NU + NW:NU + NW + NTOP]
    top = raw[0::2] + 1j * raw[1::2]; top = top / np.linalg.norm(top)
    return u, w, top   # top is a CHI-vector (single top site)


def build_sv(p):
    """Top-down: 1 top site -> 2 -> 4 -> 8, all in CHI-space, then project the physical 2-dim.
    Each layer: isometry w expands each coarse site to a pair (low0,low1); disentangler u acts on
    adjacent inter-pair legs. Returns a length-(2^N) physical statevector (after EMB projection)."""
    u, w, top = unpack(p)
    wexp = w.reshape(CHI * CHI, CHI)         # (low-pair, up)
    st = top.reshape(CHI)                    # 1 axis

    def expand(state):
        n = state.ndim
        s = state
        # expand every axis CHI -> CHI^2 (low pair) using w
        for ax in range(n - 1, -1, -1):
            s = apply_axis(s, wexp, ax)      # ax becomes CHI^2
            s = s.reshape(s.shape[:ax] + (CHI, CHI) + s.shape[ax + 1:])
        return s                             # now 2n axes

    def disentangle(state):
        # apply u downward on internal adjacent pairs (1,2),(3,4),...; PBC-free (OBC) so skip ends
        n = state.ndim
        s = state
        pairs = [(i, i + 1) for i in range(1, n - 1, 2)]
        for (a, b) in pairs:
            blk = np.tensordot(u, s, axes=([2, 3], [a, b]))   # u up-legs -> state axes a,b
            rest = [x for x in range(n) if x not in (a, b)]
            perm = [None] * n; perm[a] = 0; perm[b] = 1
            for i, r in enumerate(rest):
                perm[r] = 2 + i
            s = np.transpose(blk, perm)
        return s

    # 1 -> 2
    st = expand(st)              # 2 axes
    st = disentangle(st)         # OBC: no internal pair for 2 axes -> unchanged
    # 2 -> 4
    st = expand(st)              # 4 axes
    st = disentangle(st)         # pair (1,2)
    # 4 -> 8
    st = expand(st)              # 8 axes
    st = disentangle(st)         # pairs (1,2),(3,4),(5,6)
    # project each chi-axis down to physical 2-dim
    for ax in range(N):
        st = apply_axis(st, EMB.conj().T, ax)   # CHI -> 2
    return st.reshape(2 ** N)


def build_H():
    DIM = 2 ** N
    H = np.zeros((DIM, DIM), complex)
    for k in range(N - 1):
        XXk = np.array([[1.0]], complex)
        for i in range(N):
            XXk = np.kron(XXk, X if (i == k or i == k + 1) else I2)
        H -= XXk
    for k in range(N):
        Zk = np.array([[1.0]], complex)
        for i in range(N):
            Zk = np.kron(Zk, Z if i == k else I2)
        H -= Zk
    return H


def energy(p, H):
    sv = build_sv(p)
    nrm = np.vdot(sv, sv).real
    if nrm < 1e-14:
        return 10.0
    return (np.vdot(sv, H @ sv).real) / nrm


def superop_no_u(u, w):
    chi = w.shape[0]; wc = w.conj(); dim = chi * chi
    S = np.zeros((dim, dim), complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), complex); O[i, j] = 1.0
            AL = np.einsum('abp,ac,cbq->pq', w, O, wc)
            AR = np.einsum('abp,bd,adq->pq', w, O, wc)
            S[:, i * chi + j] = (0.5 * (AL + AR)).reshape(dim)
    return S


def superop_with_u(u, w):
    chi = w.shape[0]; uc, wc = u.conj(), w.conj(); dim = chi * chi
    S = np.zeros((dim, dim), complex)
    for i in range(chi):
        for j in range(chi):
            O = np.zeros((chi, chi), complex); O[i, j] = 1.0
            AL = np.einsum('cdef,efp,cC,CdEF,EFP->pP', u, w, O, uc, wc, optimize=True)
            AR = np.einsum('cdef,efp,dD,cDEF,EFP->pP', u, w, O, uc, wc, optimize=True)
            S[:, i * chi + j] = (0.5 * (AL + AR)).reshape(dim)
    return S


def dims_from(S):
    lam = np.sort(np.abs(np.linalg.eigvals(S)))[::-1]
    lam = lam[lam > 1e-9]
    d = -np.log2(lam)
    return d - d[0], lam


if __name__ == "__main__":
    H = build_H()
    E0 = np.linalg.eigvalsh(H)[0]
    print(f"exact E0 = {E0:.6f}")
    rng = np.random.default_rng(11)
    best = None; bestE = 1e9
    for trial in range(6):
        p0 = rng.standard_normal(NPAR) * 0.3
        r = minimize(energy, p0, args=(H,), method="L-BFGS-B",
                     options={"maxiter": 600, "ftol": 1e-12})
        if r.fun < bestE:
            bestE = r.fun; best = r.x
        print(f"  trial {trial}: E={r.fun:.5f} rel={abs(r.fun-E0)/abs(E0)*100:.2f}%")
    print(f"BEST MERA E={bestE:.6f} rel={abs(bestE-E0)/abs(E0)*100:.2f}%")
    u, w, top = unpack(best)
    dnu, _ = dims_from(superop_no_u(u, w))
    dwu, _ = dims_from(superop_with_u(u, w))
    print("\nIsing tower target: [0, 0.125, 1, 1.125, 2]")
    print("no-u (repo) dims:", np.round(dnu[:7], 4))
    print("with-u (FP) dims:", np.round(dwu[:7], 4))
