# Larger-ring confirmation + side-by-side vs the FAILED 'straddle' heuristic from qw_of_build.jl.
import numpy as np
from numpy import kron
from itertools import product
from qw_of_pregate import (X, Z, I2, op_on, of_chain_H, blocked_hb, reconstruct_from_hb,
                           embed4, gs_and_gap)

def blocked_hb_FAILED(lam3, lam=1.0):
    """The PRIOR straddle heuristic (qw_of_build.jl): wt=1 if min<=2 and max>=3 (straddles A|B window
    boundary), else 0.5 -- applied to 1-,2-,3-site placements tiled independently."""
    H4 = np.zeros((16,16), complex)
    def place(pl): return op_on(4, pl)
    def straddle(pos): return (min(pos)<=2) and (max(pos)>=3)
    def w(pos): return 1.0 if straddle(pos) else 0.5
    for p in range(1,5):
        H4 += -2*lam * w([p]) * place([(p-1, X)])
    for p in range(1,4):
        H4 += -2*lam * w([p,p+1]) * place([(p-1, Z),(p, Z)])
    if lam3 != 0.0:
        for (a,b,c) in [(1,2,3),(2,3,4)]:
            H4 += lam3 * w([a,b,c]) * place([(a-1, X),(b-1, Z),(c-1, Z)])
            H4 += lam3 * w([a,b,c]) * place([(a-1, Z),(b-1, Z),(c-1, X)])
    return 0.5*(H4 + H4.conj().T)

def reconstruct_generic(Nsuper, hb_builder, lam3, lam=1.0):
    nphys = 2*Nsuper
    hb4 = hb_builder(lam3, lam).reshape([2]*8)
    dim = 2**nphys
    H = np.zeros((dim, dim), complex)
    for k in range(Nsuper):
        sites = [(2*k + d) % nphys for d in range(4)]
        H += embed4(hb4, sites, nphys)
    return 0.5*(H + H.conj().T)

print("="*78)
print("CONFIRMATION: correct blocking on larger ring (Nsuper=4 -> 8 phys sites)")
for lam3 in (0.0, 0.856):
    Nsuper = 4; nphys = 8
    H_orig = of_chain_H(nphys, lam3, pbc=True)
    H_recon = reconstruct_generic(Nsuper, blocked_hb, lam3)
    e0o, gapo, _ = gs_and_gap(H_orig)
    e0r, gapr, _ = gs_and_gap(H_recon)
    print(f"  lam3={lam3}: max|orig-recon|={np.max(np.abs(H_orig-H_recon)):.3e}  "
          f"E0/site orig={e0o/nphys:.6f} recon={e0r/nphys:.6f}  gap orig={gapo:.5f} recon={gapr:.5f}")

print("="*78)
print("FAILED straddle heuristic (qw_of_build.jl) on Nsuper=3 -> 6 phys: should MISMATCH")
for lam3 in (0.0, 0.856):
    Nsuper = 3; nphys = 6
    H_orig = of_chain_H(nphys, lam3, pbc=True)
    H_fail = reconstruct_generic(Nsuper, blocked_hb_FAILED, lam3)
    e0o, gapo, evo = gs_and_gap(H_orig)
    e0f, gapf, evf = gs_and_gap(H_fail)
    print(f"  lam3={lam3}: max|orig-FAILED|={np.max(np.abs(H_orig-H_fail)):.3e}  "
          f"E0/site orig={e0o/nphys:.6f} FAILED={e0f/nphys:.6f}")
    print(f"            orig low6 ={np.round(evo.real,4)}")
    print(f"            FAIL low6 ={np.round(evf.real,4)}")

print("="*78)
print("Per-window operator difference (correct vs failed), 16x16 dim-4 op at lam3=0:")
print("  max|hb_correct - hb_FAILED| (lam3=0) =", np.max(np.abs(blocked_hb(0.0)-blocked_hb_FAILED(0.0))))
print("  max|hb_correct - hb_FAILED| (lam3=0.856) =", np.max(np.abs(blocked_hb(0.856)-blocked_hb_FAILED(0.856))))
