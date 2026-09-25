"""
PROBE 2 (task #95 verification): is the ADAPT-VQE force RMSE=0.0045 real physics
or 3-point luck from a 25-param optimizer?

Strategy
--------
The faithful gate was force RMSE < 0.02 over dr in {1,2,3} ONLY. Three points plus a
25-parameter optimizer could coincide. We stress-test in three ways:

1. Re-derive the ADAPT state (angles are NOT saved in the JSON). The growth is
   DETERMINISTIC: select_next_op is an argmax over fixed gradients, optimize_angles
   uses theta_init=0 (deterministic L-BFGS-B). So replaying the same loop reproduces
   the same statevector. We replay until step 25 or overlap > 0.999.

2. OUT-OF-SAMPLE force: the state was tuned ONLY on energy (force never entered the
   loss). dr in {1,2,3} were *reported* but not optimized; dr=4 was never even looked
   at. We compute F(dr) for dr in {1,2,3,4} on the final state vs exact GS and report
   per-dr relative error. dr=4 is the genuine held-out test.

3. ROBUSTNESS / basin fragility: perturb the final angles by N(0, 0.01) x5 and report
   the spread in force RMSE (dr 1-3) and GS overlap. Tight spread => robust attractor;
   large spread => fragile, the 0.0045 was a knife-edge.

VERDICT logic (this script only reports numbers; the agent makes the call):
   SUPPORTS only if dr=4 rel err < ~15% AND perturbation spread is small.

Reuses brickwork_force_check.{build_tfim_sparse, force_profile} and the ADAPT helpers
from adapt_vqe_force (build_pool, reference_state, apply_ansatz, select_next_op,
optimize_angles). Does NOT call adapt_vqe_force.main().
"""
import json
import time

import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import adapt_vqe_force as AV

L = 8
OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_force_robust.json"
OVERLAP_STOP = 0.999      # stop growth once we clear this (matches reported 0.9998)
MAX_OPS = 25              # the claim is "step 25"; cap there
GRAD_TOL = 1e-3
DRS_FIT = [1, 2, 3]       # what the original gate used
DRS_EXT = [1, 2, 3, 4]    # extended; dr=4 is out-of-sample
N_PERTURB = 5
PERTURB_SIGMA = 0.01
PERTURB_SEED = 20260608


def grow_adapt(H, psi_gs, F_exact):
    """Replay the deterministic ADAPT growth. Returns (final_sv, thetas, ops, trace)."""
    pool = AV.build_pool(L)
    psi0 = AV.reference_state(L)
    ops, thetas = [], np.zeros(0)
    trace = []
    for step in range(1, MAX_OPS + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = AV.select_next_op(psi_cur, H, pool)
        if best_grad < GRAD_TOL:
            break
        ops.append(best_op)
        theta_init = np.concatenate([thetas, [0.0]])
        thetas, E = AV.optimize_angles(ops, psi0, H, theta_init)
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS_FIT)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS_FIT])))
        trace.append({"step": step, "added": best_op["name"], "gs_overlap": ov,
                      "force_rmse": f_rmse, "energy": E})
        print(f"  step {step:2d} | +{best_op['name']:7s} | GSov={ov:.4f} | "
              f"F_rmse(dr123)={f_rmse:.4f}", flush=True)
        if ov > OVERLAP_STOP:
            print(f"  [reached overlap>{OVERLAP_STOP} at step {step}]")
            break
    return sv, thetas, ops, psi0, trace


def main():
    t0 = time.time()
    print("=" * 74)
    print("PROBE 2: ADAPT-VQE force robustness / out-of-sample / basin fragility")
    print("=" * 74)

    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0])
    psi_gs = psi_eig[:, 0]

    # Exact-GS force over the EXTENDED range (dr=4 included)
    F_exact_ext, E0_ex, Es_ex = FC.force_profile(psi_gs, H, L, DRS_EXT)
    print(f"E_gs = {Egs:.6f}")
    print("F(dr) exact (extended): " +
          ", ".join(f"dr={d}:{F_exact_ext[d]:+.5f}" for d in DRS_EXT))
    print()

    # --- 1. Re-derive the ADAPT state -----------------------------------------
    F_exact_fit = {d: F_exact_ext[d] for d in DRS_FIT}
    print("Replaying deterministic ADAPT growth...")
    sv, thetas, ops, psi0, trace = grow_adapt(H, psi_gs, F_exact_fit)
    overlap_final = float(abs(np.vdot(psi_gs, sv)) ** 2)
    n_ops = len(ops)
    n_2q = sum(1 for o in ops if o["is_2q"])
    E_final = FC.energy(sv, H)
    e_rel = abs(E_final - Egs) / abs(Egs) * 100.0
    print(f"\nReproduced: n_ops={n_ops}, n_2q={n_2q}, overlap={overlap_final:.6f}, "
          f"E_rel={e_rel:.4f}%")

    # --- 2. Out-of-sample force on the reproduced state -----------------------
    F_adapt_ext, _, _ = FC.force_profile(sv, H, L, DRS_EXT)
    per_dr = {}
    for d in DRS_EXT:
        fe, fa = F_exact_ext[d], F_adapt_ext[d]
        rel = abs(fa - fe) / max(abs(fe), 1e-12) * 100.0
        per_dr[str(d)] = {"F_exact": fe, "F_adapt": fa, "rel_err_pct": rel,
                          "in_sample": d in DRS_FIT}
    force_rmse_dr123 = float(np.sqrt(np.mean(
        [(F_adapt_ext[d] - F_exact_ext[d]) ** 2 for d in DRS_FIT])))
    force_rmse_dr1234 = float(np.sqrt(np.mean(
        [(F_adapt_ext[d] - F_exact_ext[d]) ** 2 for d in DRS_EXT])))
    force_rel_err_dr4 = per_dr["4"]["rel_err_pct"]

    print("\n  dr   F_exact      F_adapt     rel_err   sample")
    for d in DRS_EXT:
        r = per_dr[str(d)]
        tag = "in" if r["in_sample"] else "OUT"
        print(f"  {d:>2} {r['F_exact']:>+11.5f} {r['F_adapt']:>+11.5f} "
              f"{r['rel_err_pct']:>8.1f}%   {tag}")
    print(f"\n  force_rmse(dr123)  = {force_rmse_dr123:.5f}  "
          f"(original claim: 0.00453)")
    print(f"  force_rmse(dr1234) = {force_rmse_dr1234:.5f}")
    print(f"  dr=4 rel err (OUT-OF-SAMPLE) = {force_rel_err_dr4:.1f}%")

    # --- 3. Perturbation / basin fragility ------------------------------------
    print(f"\nPerturbing final {len(thetas)} angles by N(0,{PERTURB_SIGMA}) x{N_PERTURB}...")
    rng = np.random.default_rng(PERTURB_SEED)
    perturb_rmses, perturb_overlaps, perturb_rmse_dr4 = [], [], []
    for i in range(N_PERTURB):
        dtheta = rng.normal(0.0, PERTURB_SIGMA, size=thetas.shape)
        sv_p = AV.apply_ansatz(thetas + dtheta, ops, psi0)
        ovp = float(abs(np.vdot(psi_gs, sv_p)) ** 2)
        F_p, _, _ = FC.force_profile(sv_p, H, L, DRS_EXT)
        rmse_p = float(np.sqrt(np.mean(
            [(F_p[d] - F_exact_ext[d]) ** 2 for d in DRS_FIT])))
        rel4_p = abs(F_p[4] - F_exact_ext[4]) / max(abs(F_exact_ext[4]), 1e-12) * 100.0
        perturb_rmses.append(rmse_p)
        perturb_overlaps.append(ovp)
        perturb_rmse_dr4.append(rel4_p)
        print(f"  perturb {i+1}: GSov={ovp:.5f}  F_rmse(dr123)={rmse_p:.5f}  "
              f"dr4_relerr={rel4_p:.1f}%")

    perturb_rmse_mean = float(np.mean(perturb_rmses))
    perturb_rmse_std = float(np.std(perturb_rmses))
    perturb_overlap_mean = float(np.mean(perturb_overlaps))
    perturb_overlap_std = float(np.std(perturb_overlaps))

    print(f"\n  perturb force_rmse(dr123): mean={perturb_rmse_mean:.5f} "
          f"std={perturb_rmse_std:.5f}")
    print(f"  perturb GS overlap:        mean={perturb_overlap_mean:.5f} "
          f"std={perturb_overlap_std:.5f}")

    # --- self-assessment (informational; agent renders the official verdict) --
    dr4_ok = force_rel_err_dr4 < 15.0
    # "small spread" heuristic: std of force rmse under 1% perturbation should be
    # well below the 0.02 gate; we flag if std exceeds 25% of the gate.
    spread_ok = perturb_rmse_std < 0.005
    self_verdict = ("SUPPORTS_CLAIM" if (dr4_ok and spread_ok)
                    else "REFUTES_OR_PARTIAL")

    results = {
        "L": L, "E_gs": Egs,
        "reproduced": {"n_ops": n_ops, "n_2q": n_2q,
                       "overlap_final": overlap_final, "energy": E_final,
                       "energy_rel_pct": e_rel},
        "F_exact_ext": {str(d): F_exact_ext[d] for d in DRS_EXT},
        "F_adapt_ext": {str(d): F_adapt_ext[d] for d in DRS_EXT},
        "per_dr": per_dr,
        "force_rmse_dr123": force_rmse_dr123,
        "force_rmse_dr1234": force_rmse_dr1234,
        "force_rel_err_dr4": force_rel_err_dr4,
        "overlap_final": overlap_final,
        "perturb": {
            "sigma": PERTURB_SIGMA, "n": N_PERTURB, "seed": PERTURB_SEED,
            "rmses_dr123": perturb_rmses, "overlaps": perturb_overlaps,
            "rel_err_dr4": perturb_rmse_dr4,
        },
        "perturb_rmse_mean": perturb_rmse_mean,
        "perturb_rmse_std": perturb_rmse_std,
        "perturb_overlap_mean": perturb_overlap_mean,
        "perturb_overlap_std": perturb_overlap_std,
        "self_assessment": {"dr4_ok": dr4_ok, "spread_ok": spread_ok,
                            "self_verdict": self_verdict},
        "trace": trace,
        "wall_seconds": time.time() - t0,
    }
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  self-assessment: dr4_ok={dr4_ok} spread_ok={spread_ok} "
          f"-> {self_verdict}")
    print(f"  wall: {results['wall_seconds']:.1f} s")
    print(f"  saved -> {OUT}")


if __name__ == "__main__":
    main()
