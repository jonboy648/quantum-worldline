"""
SIM-2026-047 - HYP-2026-027: EIGEN-TOWER chi-ramp 4->6 for a SCALE-INVARIANT critical MERA.

WHY (CHI6-CONVERGENCE-RECIPE, fallback #2 -> promoted to primary): three seeding routes failed to give
a scale-invariant critical chi=6 (u,w) -- cold (c=0.75), raw chi-ramp pad (c=4.6), finite-MERA bulk
(critical STATE but bulk c=6.67 in the superop: criticality != scale-invariance). The principled fix is
to grow chi in the ASCENDING-SUPEROPERATOR / bond-density-matrix EIGENBASIS, where scale-invariance
lives -- NOT the energy or raw-tensor basis.

THE RAMP (SVD-optimal bond expansion, Evenbly-Vidal standard):
  - The chi=4 isometry w (16->4) keeps the top-4 eigenvectors of the 2-site bond reduced density matrix
    rho_pair (from the descending fixed point). To grow to chi=6, build w (16->6) from the TOP-6
    eigenvectors of rho_pair. This is the optimal truncation at the larger bond and PRESERVES the
    chi=4 scaling structure (the top-4 directions are unchanged; 2 small-weight directions are added).
  - The disentangler u: embed the chi=4 (16x16) block into the chi=6 (36x36) unitary; complete the new
    directions with identity (they carry negligible weight initially and relax during re-convergence).
  - Re-converge with the EV ScInv1/ScInv2 loop (sim045) warm-started from this eigen-tower seed. Because
    the seed already sits at the scale-invariant fixed point (to leading order), the loop should settle
    at c=0.5 with sigma BETTER than chi=4's 0.057 -- the decisive basin discriminator.

GATE: chi=6 Ising c in [0.45,0.55] AND sigma in [0.10,0.15] AND sigma < chi=4's 0.057 AND eps ~1.0 AND
a dim within 0.05 of Delta_T=2. Only then is the chi=6 control trustworthy -> run TCI.
"""
import sys

import numpy as np
import torch

import sim045_scaleinv_stable as M

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass


def bond_rho_pair(w4, u4, chi):
    """2-site reduced density matrix (chi^2 x chi^2) from the descending fixed point at chi=4."""
    rho = M.rho_fixedpoint(w4, u4, chi)
    r3 = np.asarray(rho.detach()).reshape((chi,) * 6)
    rho2 = np.trace(r3, axis1=2, axis2=5).reshape(chi * chi, chi * chi)
    return 0.5 * (rho2 + rho2.conj().T)


def eigentower_w(w4, u4, chi_old, chi_new):
    """chi_new isometry (chi_new^2... no: (chi_old^2 bottom)->chi_new top) from the top-chi_new
    eigenvectors of the chi_old 2-site bond rho. The bottom bond stays chi_old^2 (the ramp grows the
    TOP/coarse bond chi_old->chi_new). Returns w_new shape (chi_new, chi_new, chi_new) by ALSO growing
    the bottom legs: we embed the chi_old block and add eigen-directions. NOTE: a scale-invariant w has
    bottom=chi^2 and top=chi; growing chi changes BOTH. We construct the new w on the chi_new^2 bottom
    by embedding chi_old tensors and orthonormal-completing."""
    # Top bond: top-chi_new eigenvectors of rho_pair (chi_old^2 dim). These live in the chi_old^2 space.
    rho2 = bond_rho_pair(w4, u4, chi_old)            # (chi_old^2 x chi_old^2)
    ev, V = np.linalg.eigh(rho2)
    order = np.argsort(ev)[::-1]
    V = V[:, order]                                  # columns = bond directions, descending weight
    # w_old is (chi_old^2, chi_old) = top-chi_old eigenvectors (approx). Build w on chi_new^2 bottom:
    # embed the chi_old^2 eigen-directions into the chi_new^2 space (pad bottom with zeros), take top
    # chi_new columns.
    cob = chi_old * chi_old; cnb = chi_new * chi_new
    Wbig = np.zeros((cnb, chi_new), dtype=complex)
    # embed each chosen eigenvector (length chi_old^2) into the chi_new^2 bottom space at the block
    # positions (i,j)->(i,j) of the chi_new grid
    def embed_bottom(vec):
        m = vec.reshape(chi_old, chi_old)
        M_ = np.zeros((chi_new, chi_new), dtype=complex); M_[:chi_old, :chi_old] = m
        return M_.reshape(cnb)
    for col in range(chi_new):
        Wbig[:, col] = embed_bottom(V[:, col])
    # re-orthonormalize columns (they may not be orthonormal after embedding)
    Q, _ = np.linalg.qr(Wbig)
    return Q[:, :chi_new].reshape(chi_new, chi_new, chi_new)


def eigentower_u(u4, chi_old, chi_new):
    """Embed the chi_old disentangler (chi_old^2 x chi_old^2) into a chi_new (chi_new^2 x chi_new^2)
    unitary; complete with identity on the new directions."""
    cob = chi_old * chi_old; cnb = chi_new * chi_new
    Ubig = np.eye(cnb, dtype=complex)
    u4m = u4.reshape(cob, cob)
    # place the chi_old block at the grid positions corresponding to (i<chi_old, j<chi_old)
    idx = [i * chi_new + j for i in range(chi_old) for j in range(chi_old)]
    for a, ia in enumerate(idx):
        for b, ib in enumerate(idx):
            Ubig[ia, ib] = u4m[a, b]
    # re-unitarize (the block-embed + identity may not be exactly unitary at the boundary)
    U, _, Vh = np.linalg.svd(Ubig)
    return (U @ Vh).reshape(chi_new, chi_new, chi_new, chi_new)


def main():
    chi_old, chi_new = 4, 6
    d = np.load("uw_ISING_stable_chi4.npz")
    w4, u4 = d["w"], d["u"]
    c4, s14, dims4 = M.central_charge_and_dims(w4, u4, chi_old, k=8)
    print(f"chi=4 base: c={c4:.4f} sigma={dims4[1]:.4f} eps={dims4[2]:.4f}", flush=True)

    w6 = eigentower_w(w4, u4, chi_old, chi_new)
    u6 = eigentower_u(u4, chi_old, chi_new)
    # verify isometry
    W = w6.reshape(chi_new * chi_new, chi_new)
    U = u6.reshape(chi_new * chi_new, chi_new * chi_new)
    print(f"seed isometry errs: w {np.abs(W.conj().T @ W - np.eye(chi_new)).max():.1e} "
          f"u {np.abs(U.conj().T @ U - np.eye(chi_new * chi_new)).max():.1e}", flush=True)
    c6, s16, dims6 = M.central_charge_and_dims(w6, u6, chi_new, k=12)
    print(f"eigen-tower SEED (pre-refine): c={c6:.4f} sigma={dims6[1]:.4f} eps={dims6[2]:.4f}", flush=True)
    print(f"  dims: {np.round(dims6[:8], 4)}", flush=True)
    np.savez("seed_chi6_eigentower.npz", w=w6, u=u6, c=c6)
    print("saved seed_chi6_eigentower.npz  (feed to sim045 refine)", flush=True)


if __name__ == "__main__":
    main()
