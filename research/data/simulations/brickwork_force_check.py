"""
Force-observable check for the depth-3 brickwork (task #92).

The depth-3 brickwork was fit ONLY to match the connected correlator C(r)=<Z0 Zr>. But QCUP
measures the alpha~4 holographic FORCE:
    F(dr) = E_dual(dr) - E_0 - 2*(E_single - E_0)
where sigma_j is the boundary-primary op, psi_dual = sigma_{dr} sigma_0 |psi> (normalized),
E_* = <psi_*|H|psi_*>, H = critical TFIM. This is a HAMILTONIAN-energy observable, not a
correlator -- a state can match C(r) yet have the wrong energy landscape.

TEST: fit depth-3 brickwork to C(r), then compute F(dr) on it vs the exact GS. If F(dr) matches
(power-law, alpha~4-ish, right magnitude/sign), the cheap circuit carries the force -> QCUP path
viable. If F(dr) is wrong (the brickwork matched the correlator but not the energy), the cheap
circuit is moot -- a necessary-but-not-sufficient failure.

Compares THREE things on F(dr): exact GS (ground truth), depth-3 brickwork (C(r)-fit), and the
energy gap E_brick - E_gs (how far from the true GS the brickwork sits).
"""
import numpy as np
from scipy.optimize import minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
import hyp024_tfd_btz_transport as TFD
import lowdepth_ansatz_search as LD

L = 8
ALPHA_BP = 0.635
BETA_BP = -0.026


def build_tfim_sparse(L, g=1.0):
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    for j in range(L):
        H = H - g * TFD.sparse_pauli_full(L, j, "X")
    for j in range(L):
        jp = (j + 1) % L
        H = H - (TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp, "Z"))
    return H


def bp_op(L, j):
    """Boundary-primary sigma_j (PBC-safe via modular j+1)."""
    jp = (j + 1) % L
    op = ALPHA_BP * (TFD.sparse_pauli_full(L, j, "X") + TFD.sparse_pauli_full(L, jp, "X"))
    op = op + BETA_BP * (TFD.sparse_pauli_full(L, j, "X") @ TFD.sparse_pauli_full(L, jp, "Z")
                         + TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp, "X"))
    return op


def energy(sv, H):
    return float(np.real(np.vdot(sv, H @ sv)))


def force_profile(sv0, H, L, drs):
    """F(dr) on state sv0 (already an eigen/approx-GS). Returns dict dr->F."""
    E0 = energy(sv0, H)
    # single excitation at site 0
    sig0 = bp_op(L, 0)
    ps = sig0 @ sv0
    ps = ps / np.linalg.norm(ps)
    E_single = energy(ps, H)
    out = {}
    for dr in drs:
        sigd = bp_op(L, dr)
        pd = sigd @ (sig0 @ sv0)
        nrm = np.linalg.norm(pd)
        if nrm < 1e-12:
            out[dr] = None; continue
        pd = pd / nrm
        E_dual = energy(pd, H)
        F = E_dual - E0 - 2.0 * (E_single - E0)
        out[dr] = F
    return out, E0, E_single


def main():
    print("=" * 70)
    print("Force-observable check: depth-3 brickwork vs exact GS")
    print("=" * 70)
    H = build_tfim_sparse(L)
    Egs_arr, psi = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0]); psi = psi[:, 0]
    Zops = LD.pauli_strings_cache(L)
    target = LD.correlator(psi, Zops, L)  # connected

    drs = [1, 2, 3]
    # exact GS force (ground truth)
    F_exact, E0e, Ese = force_profile(psi, H, L, drs)
    print(f"\nEXACT GS: E_gs={Egs:.5f}")
    print("  F(dr) exact: " + ", ".join(f"dr={d}:{F_exact[d]:+.5f}" for d in drs))

    # fit depth-3 brickwork to C(r)
    depth = 3; ng = LD.n_gates_for_depth(depth); nparam = ng * 16
    rng = np.random.default_rng(7)

    def loss(flat):
        sv = LD.brickwork_state(flat.reshape(ng, 16), depth, L)
        c = LD.correlator(sv, Zops, L)
        return float(np.sum((c - target) ** 2))

    best = None
    for _ in range(4):
        r = minimize(loss, rng.standard_normal(nparam) * 0.3, method="L-BFGS-B",
                     options={"maxiter": 600, "ftol": 1e-11})
        if best is None or r.fun < best.fun:
            best = r
    sv_b = LD.brickwork_state(best.x.reshape(ng, 16), depth, L)
    c_b = LD.correlator(sv_b, Zops, L)
    cr_rmse = float(np.sqrt(np.mean((c_b - target) ** 2)))
    E_brick = energy(sv_b, H)
    gs_overlap = float(abs(np.vdot(psi, sv_b)) ** 2)

    F_brick, E0b, Esb = force_profile(sv_b, H, L, drs)
    print(f"\nDEPTH-3 BRICKWORK (C(r)-fit): C(r) RMSE={cr_rmse:.5f}")
    print(f"  E_brick={E_brick:.5f}  (E_gs={Egs:.5f}, energy gap={E_brick-Egs:+.5f})")
    print(f"  |<gs|brick>|^2 = {gs_overlap:.4f}  (1.0 = exactly the ground state)")
    print("  F(dr) brick: " + ", ".join(f"dr={d}:{F_brick[d]:+.5f}" for d in drs))

    # comparison
    print("\n" + "=" * 70)
    print(f"  {'dr':>4} {'F_exact':>12} {'F_brick':>12} {'rel_err':>10}")
    for d in drs:
        fe, fb = F_exact[d], F_brick[d]
        rel = abs(fb - fe) / max(abs(fe), 1e-9) * 100
        print(f"  {d:>4} {fe:>+12.5f} {fb:>+12.5f} {rel:>9.1f}%")

    force_rmse = float(np.sqrt(np.mean([(F_brick[d] - F_exact[d]) ** 2 for d in drs])))
    verdict = ("FORCE REPRODUCED (cheap circuit carries the physics)"
               if force_rmse < 0.02 and gs_overlap > 0.9
               else "FORCE FAILED (matched C(r) but NOT the force -- necessary != sufficient)")
    print(f"\n  Force RMSE = {force_rmse:.5f} | GS overlap = {gs_overlap:.4f}")
    print(f"  VERDICT: {verdict}")

    import json
    out = {
        "E_gs": Egs, "E_brick": E_brick, "energy_gap": E_brick - Egs,
        "gs_overlap": gs_overlap, "cr_rmse": cr_rmse,
        "F_exact": {str(d): F_exact[d] for d in drs},
        "F_brick": {str(d): F_brick[d] for d in drs},
        "force_rmse": force_rmse, "verdict": verdict,
    }
    with open("D:/quantum-worldline/research/data/builds/brickwork_force_check.json", "w") as f:
        json.dump(out, f, indent=2)
    print("  saved -> research/data/builds/brickwork_force_check.json")


if __name__ == "__main__":
    main()
