"""
Pad a converged scale-invariant MERA checkpoint from chi -> chi_new (standard MERA chi-ramp seed).

Isometric padding: embed each tensor's bond indices into the larger space with zeros, then
re-orthonormalize via QR/polar so the result is still a valid isometry/unitary. This gives chi_new a
warm start from the chi solution (EV-recommended: init the larger-chi optimization from the converged
smaller-chi state) instead of a cold random start, which converges painfully slowly.

Usage: python pad_mera_chi.py <in.npz> <chi_new> <out.npz>
  e.g. python pad_mera_chi.py uw_ISING_stable_chi4.npz 6 seed_chi6.npz
"""
import sys

import numpy as np


def pad_isometry_w(w, chi_new, eps=1e-2):
    """w: (chi,chi,chi)=[bl,br,top]. GENTLE chi-ramp: keep the chi-block exactly, fill the new
    bottom/top directions with SMALL (eps) perturbations, then re-orthonormalize via QR. Small eps
    keeps the padded state close to the converged chi state (c stays near its chi value) instead of
    jumping far off (random fill sent c 0.46 -> 4.17 and stalled convergence)."""
    chi = w.shape[0]
    M = np.zeros((chi_new * chi_new, chi_new), dtype=complex)
    Wblk = np.zeros((chi_new, chi_new, chi_new), dtype=complex); Wblk[:chi, :chi, :chi] = w
    M = Wblk.reshape(chi_new * chi_new, chi_new)
    rng = np.random.default_rng(0)
    R = rng.standard_normal(M.shape) + 1j * rng.standard_normal(M.shape)
    nullcol = (np.abs(M).sum(axis=0) < 1e-12)            # the new top-bond columns
    M[:, nullcol] = eps * R[:, nullcol]
    Q, _ = np.linalg.qr(M)
    # preserve sign/phase alignment of the original chi columns where possible
    return Q[:, :chi_new].reshape(chi_new, chi_new, chi_new)


def pad_unitary_u(u, chi_new, eps=1e-2):
    """u: (chi,chi,chi,chi). GENTLE: keep the chi-block, fill new rows/cols with small eps, re-unitarize."""
    chi = u.shape[0]
    U = np.zeros((chi_new,) * 4, dtype=complex); U[:chi, :chi, :chi, :chi] = u
    M = U.reshape(chi_new * chi_new, chi_new * chi_new)
    rng = np.random.default_rng(1)
    R = rng.standard_normal(M.shape) + 1j * rng.standard_normal(M.shape)
    nullrow = (np.abs(M).sum(axis=1) < 1e-12)
    nullcol = (np.abs(M).sum(axis=0) < 1e-12)
    M[nullrow, :] += eps * R[nullrow, :]
    M[:, nullcol] += eps * R[:, nullcol]
    Q, _ = np.linalg.qr(M)
    return Q.reshape((chi_new,) * 4)


def main():
    inp, chi_new, out = sys.argv[1], int(sys.argv[2]), sys.argv[3]
    d = np.load(inp)
    w = pad_isometry_w(d["w"], chi_new)
    u = pad_unitary_u(d["u"], chi_new)
    save = {"w": w, "u": u}
    # transitional layer w1 (2,2,chi), u1 (2,2,2,2): w1's top bond grows but is RANK-CAPPED at 4
    # (it maps phys^2=4 -> chi, so at most 4 orthonormal columns; the rest stay zero columns).
    if "w1" in d:
        chi = d["w"].shape[0]
        w1 = np.zeros((2, 2, chi_new), dtype=d["w1"].dtype)
        w1[:, :, :chi] = d["w1"]                      # embed; columns chi..chi_new-1 are zero
        # re-orthonormalize the (at most 4) non-trivial columns via QR of the 4 x chi_new matrix
        M = w1.reshape(4, chi_new)
        Q, _ = np.linalg.qr(M.conj().T)              # QR on (chi_new x 4): Q is (chi_new x 4) isometry
        w1_new = np.zeros((chi_new, 4), dtype=d["w1"].dtype)
        w1_new[:, :Q.shape[1]] = Q[:, :4]
        save["w1"] = w1_new.T.reshape(2, 2, chi_new)
        save["u1"] = d["u1"]
    np.savez(out, **save)
    print(f"padded {inp} (chi={d['w'].shape[0]}) -> {out} (chi={chi_new})")
    print(f"  w {w.shape}, u {u.shape}" + (f", w1 {save['w1'].shape}" if "w1" in save else ""))


if __name__ == "__main__":
    main()
