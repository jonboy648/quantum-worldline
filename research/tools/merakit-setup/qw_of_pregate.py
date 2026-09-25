# EXACT-DIAG PRE-GATE for the OF blocking (block_size=2, dim-4 super-sites).
#
# DERIVATION (global-sum route, the CORRECT one):
# Lattice: physical sites 1..2N, grouped into N super-sites A_k = (2k-1, 2k).
# Super-pair windows: W_k = (A_k, A_{k+1}) covers physical sites (2k-1, 2k, 2k+1, 2k+2).
# Consecutive windows STEP BY 2 PHYSICAL SITES (one super-site), NOT 4. So window W_{k-1} covers
# (2k-3,2k-2,2k-1,2k) and W_k covers (2k-1,2k,2k+1,2k+2): they OVERLAP on super-site A_k = (2k-1,2k).
#
# A physical-lattice term T on a set of physical sites S is "seen" by window W_k iff S ⊆ phys(W_k).
# To reconstruct H = sum_terms T exactly with NO double counting, we put weight
#       w(T placed in window W_k) = 1 / (number of windows whose phys-range fully contains S).
# Because each window is a 4-physical-site sliding window stepping by 2, the number of windows that
# fully contain a contiguous site-set S of span (max-min+1) depends ONLY on which super-sites S touches:
#   - S inside a SINGLE super-site (span<=2, both sites in same A_k): contained by W_{k-1} and W_k -> 2 windows -> weight 1/2.
#   - S spanning TWO adjacent super-sites (touches A_k and A_{k+1}): contained ONLY by W_k -> 1 window -> weight 1.
#   - S spanning THREE super-sites: contained by NO 4-physical-site window -> CANNOT be represented at block=2.
#
# Map to within-window local coordinates (1,2,3,4) where (1,2)=left super-site A, (3,4)=right super-site B:
#   k=1 term:
#       pos in {1,2}  (inside A)  -> 1/2 ;  pos in {3,4} (inside B) -> 1/2   [single super-site]
#   k=2 term (bond):
#       (1,2) inside A -> 1/2 ; (3,4) inside B -> 1/2 ; (2,3) straddles A|B -> 1   [span 2 super-sites for (2,3)]
#   k=3 term:
#       (1,2,3): touches A(1,2)+B(3) -> spans 2 super-sites -> weight 1, ONE window
#       (2,3,4): touches A(2)+B(3,4) -> spans 2 super-sites -> weight 1, ONE window
#       (3,4,5)/(everything touching a 3rd super-site) -> NOT representable, lives in the NEXT window
#   KEY: to avoid double counting a 3-site term that could be placed in two different windows, we assign
#   each lattice 3-site term to the UNIQUE window that contains all 3 of its sites. A 3-site term on
#   phys (2k-1,2k,2k+1) [=local (1,2,3)] and on phys (2k,2k+1,2k+2) [=local (2,3,4)] are DISTINCT lattice
#   terms; each is contained in exactly ONE window -> weight 1 each. There is NO 3-site placement that is
#   double-counted, hence NO 1/2 ever appears for 3-site terms. (A 3-site set can never sit inside one
#   2-site super-site, and it can never sit inside two windows.)
#
# This is the CORRECT generalization of block_op. The earlier "straddle" heuristic in qw_of_build.jl used
# wt=0.5 for non-straddling and wt=1 for straddling applied to SINGLE-SITE and 2-SITE placements TILED
# INDEPENDENTLY on the 4-site window -- but the 1-site weight there is WRONG: a 1-site term sits inside one
# super-site and is seen by 2 windows -> 1/2, which it had, BUT it ALSO incorrectly placed 1-site terms at
# all 4 local positions with the straddle test never firing (so all got 1/2), DOUBLE counting was actually
# right for 1-site... the real failure is subtler: see below. We just TEST it.
#
# PRE-GATE TEST: build the blocked dim-4 2-site operator h_b (16x16). Reconstruct the GLOBAL Hamiltonian on
# a periodic chain of N super-sites (=2N physical sites) by summing h_b over all super-pairs with PBC, then
# compare its full spectrum (or at least GS energy/site + low gap) to exact-diag of the ORIGINAL OF chain on
# 2N physical sites with PBC. They MUST match.

import numpy as np
from numpy import kron
from itertools import product

X = np.array([[0,1],[1,0]], complex)
Z = np.array([[1,0],[0,-1]], complex)
I2 = np.eye(2, dtype=complex)

def op_on(n_sites, placements):
    """placements: list of (site_index_0based, 2x2 matrix). identity elsewhere. n_sites physical sites."""
    m = np.array([[1.0]], complex)
    for s in range(n_sites):
        o = I2
        for (idx, mat) in placements:
            if idx == s:
                o = mat
        m = np.kron(m, o)
    return m

def of_chain_H(nphys, lam3, lam=1.0, pbc=True):
    """Original OF Hamiltonian on nphys physical sites.
    h_j = -2*lam*(X_j + Z_j Z_{j+1}) + lam3*(X_j Z_{j+1} Z_{j+2} + Z_j Z_{j+1} X_{j+2})."""
    dim = 2**nphys
    H = np.zeros((dim, dim), complex)
    rng = range(nphys) if pbc else range(nphys)
    # 1-site X_j (every site)
    for j in range(nphys):
        H += -2*lam * op_on(nphys, [(j, X)])
    # 2-site Z_j Z_{j+1}
    jmax = nphys if pbc else nphys-1
    for j in range(jmax):
        a, b = j % nphys, (j+1) % nphys
        H += -2*lam * op_on(nphys, [(a, Z),(b, Z)])
    # 3-site
    if lam3 != 0.0:
        jmax3 = nphys if pbc else nphys-2
        for j in range(jmax3):
            a, b, c = j % nphys, (j+1) % nphys, (j+2) % nphys
            H += lam3 * op_on(nphys, [(a, X),(b, Z),(c, Z)])
            H += lam3 * op_on(nphys, [(a, Z),(b, Z),(c, X)])
    return 0.5*(H + H.conj().T)

def blocked_hb(lam3, lam=1.0):
    """dim-4 super-site blocked 2-site operator on a 4-physical-site window (1,2,3,4)=(A:1,2 | B:3,4).
    Weights per CORRECT global-sum rule above."""
    H4 = np.zeros((16,16), complex)
    def place(pl): return op_on(4, pl)
    # weight rule (window-local): single super-site -> 1/2 ; spans two super-sites -> 1
    # super-site of local pos: pos in {1,2}->A(0), {3,4}->B(1) ; 1-based here, convert.
    def superset(pos1based):
        return set(0 if p<=2 else 1 for p in pos1based)
    def w(pos1based):
        return 0.5 if len(superset(pos1based))==1 else 1.0
    # 1-site X at local 1..4
    for p in range(1,5):
        H4 += -2*lam * w([p]) * place([(p-1, X)])
    # 2-site ZZ at (1,2),(2,3),(3,4)
    for p in range(1,4):
        H4 += -2*lam * w([p,p+1]) * place([(p-1, Z),(p, Z)])
    # 3-site XZZ + ZZX. Only placements fully inside [1..4] that span exactly two super-sites:
    # (1,2,3) and (2,3,4). Both weight 1 (each contained in exactly one window).
    if lam3 != 0.0:
        for (a,b,c) in [(1,2,3),(2,3,4)]:
            H4 += lam3 * w([a,b,c]) * place([(a-1, X),(b-1, Z),(c-1, Z)])
            H4 += lam3 * w([a,b,c]) * place([(a-1, Z),(b-1, Z),(c-1, X)])
    return 0.5*(H4 + H4.conj().T)

def reconstruct_from_hb(Nsuper, lam3, lam=1.0):
    """Sum the blocked 2-super-site op over all super-pairs on a periodic ring of Nsuper super-sites.
    Each super-site = 2 physical sites; total nphys=2*Nsuper. h_b acts on (A_k, A_{k+1}); the operator is
    expressed in the FUSED (dim-4) basis, but to compare to physical exact-diag we work in the UNFUSED
    physical basis: h_b's 16x16 IS already in the physical (4-site) basis before fusion, so just tile it."""
    nphys = 2*Nsuper
    hb_phys = blocked_hb(lam3, lam)  # 16x16 in physical basis of a 4-site window (no fusion needed for ED)
    dim = 2**nphys
    H = np.zeros((dim, dim), complex)
    hb4 = hb_phys.reshape([2]*8)  # 4 ket sites, 4 bra sites
    for k in range(Nsuper):
        # window covers physical sites (2k, 2k+1, 2k+2, 2k+3) mod nphys
        sites = [(2*k + d) % nphys for d in range(4)]
        # embed hb4 acting on these 4 sites into the full operator
        H += embed4(hb4, sites, nphys)
    return 0.5*(H + H.conj().T)

def embed4(hb4, sites, nphys):
    """Embed a 4-site operator (given as a 2^4 x 2^4 reshaped [2]*8 tensor) acting on `sites`
    into the full 2^nphys operator via tensor index placement."""
    dim = 2**nphys
    full = np.zeros((dim, dim), complex)
    # Build by iterating over all bra/ket configs of the 4 active sites; identity on the rest.
    other = [s for s in range(nphys) if s not in sites]
    for kets in product(range(2), repeat=4):
        for bras in product(range(2), repeat=4):
            amp = hb4[kets + bras]
            if amp == 0: continue
            # construct outer product on active sites x identity on others
            # do it as a sparse-ish kron over site order
            mats = [None]*nphys
            for idx, s in enumerate(sites):
                m = np.zeros((2,2), complex); m[bras[idx], kets[idx]] = 1.0  # |bra><ket|
                mats[s] = m
            for s in other:
                mats[s] = I2
            term = np.array([[1.0]], complex)
            for s in range(nphys):
                term = np.kron(term, mats[s])
            full += amp*term
    return full

def gs_and_gap(H):
    ev = np.linalg.eigvalsh(H)
    return ev[0], ev[1]-ev[0], ev[:6]

print("="*70)
for lam3 in (0.0, 0.856):
    Nsuper = 3   # 3 super-sites = 6 physical sites, PBC ring of super-pairs
    nphys = 2*Nsuper
    H_orig = of_chain_H(nphys, lam3, pbc=True)
    H_recon = reconstruct_from_hb(Nsuper, lam3)
    e0o, gapo, evo = gs_and_gap(H_orig)
    e0r, gapr, evr = gs_and_gap(H_recon)
    diff = np.max(np.abs(H_orig - H_recon))
    print(f"lam3={lam3}: nphys={nphys}")
    print(f"  ORIG   E0/site={e0o/nphys:.6f}  gap={gapo:.6f}  low6={np.round(evo.real,4)}")
    print(f"  RECON  E0/site={e0r/nphys:.6f}  gap={gapr:.6f}  low6={np.round(evr.real,4)}")
    print(f"  max|H_orig - H_recon| = {diff:.3e}   (MUST be ~0 for exact blocking)")
    print("-"*70)
