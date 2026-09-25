"""
LEAD CROSS-CHECK (task #95): independent end-to-end reproduction of the ADAPT-VQE
physics + robustness, reusing ONLY the production modules (no reimplementation of H
or the force). Settles whether the force signal is (a) reproducible, (b) genuine
out-of-sample, (c) robust to angle error at the level a real device would impose.

I re-grow the 25-op ansatz deterministically (same growth loop as adapt_vqe_force.main,
but called piecewise so I can grab the final angles, which the JSON did not save), then:
  1. Reproduce force_rmse(dr123), overlap, n_2q, E_rel  -> must match the saved JSON.
  2. Out-of-sample dr=4 (force was NEVER in the optimizer loss; loss is <H> only).
  3. Robustness: FAIR multiplicative angle jitter (relative 0.1%/0.3%/1%) x 30 seeds,
     since hardware angle error is ~relative, plus the additive N(0,0.01) the probe used.
     Report force-RMSE(dr123) distribution and 0.02-gate fail rate at each level.
"""
import json
import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import adapt_vqe_force as AV

L = 8
DRS = [1, 2, 3]
OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_lead_physics_results.json"


def regrow():
    """Replay ADAPT growth, return (final_thetas, ops, psi0, H, psi_gs, Egs, F_exact)."""
    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0]); psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS + [4])
    pool = AV.build_pool(L)
    psi0 = AV.reference_state(L)
    ops, thetas = [], np.zeros(0)
    for step in range(1, 60 + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = AV.select_next_op(psi_cur, H, pool)
        if best_grad < 1e-3:
            break
        ops.append(best_op)
        theta_init = np.concatenate([thetas, [0.0]])
        thetas, E = AV.optimize_angles(ops, psi0, H, theta_init)
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
        if ov > 0.99 and f_rmse < 0.02:
            break
    return thetas, ops, psi0, H, psi_gs, Egs, F_exact


def force_rmse_of(sv, H, F_exact, drs):
    F_b, _, _ = FC.force_profile(sv, H, L, drs)
    return float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in drs]))), F_b


def main():
    thetas, ops, psi0, H, psi_gs, Egs, F_exact = regrow()
    n_2q = sum(1 for o in ops if o["is_2q"])
    sv = AV.apply_ansatz(thetas, ops, psi0)
    ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
    E = FC.energy(sv, H)
    e_rel = abs(E - Egs) / abs(Egs) * 100
    rmse123, F_b = force_rmse_of(sv, H, F_exact, DRS)
    rmse1234, _ = force_rmse_of(sv, H, F_exact, DRS + [4])
    rel4 = abs(F_b.get(4, 0) - F_exact[4]) / abs(F_exact[4]) * 100 if 4 in F_b else None
    # recompute dr4 explicitly via force_profile on the adapt state
    F_b4, _, _ = FC.force_profile(sv, H, L, [4])
    rel4 = abs(F_b4[4] - F_exact[4]) / abs(F_exact[4]) * 100

    print("=" * 70)
    print("REPRODUCTION (re-grown ADAPT, final angles recovered):")
    print(f"  n_ops={len(ops)}  n_2q={n_2q}")
    print(f"  GS overlap        = {ov:.6f}   (JSON: 0.999768)")
    print(f"  energy rel %      = {e_rel:.5f}  (JSON: 0.013865)")
    print(f"  force_rmse(dr123) = {rmse123:.6f} (JSON: 0.004531)")
    print(f"  OUT-OF-SAMPLE dr=4: F_adapt={F_b4[4]:+.5f} vs F_exact={F_exact[4]:+.5f} "
          f"-> rel {rel4:.2f}%")
    print(f"  force_rmse(dr1234)= {rmse1234:.6f}")

    # ---- robustness: fair multiplicative + additive jitter ----
    print("\nROBUSTNESS (force_rmse dr123 under angle jitter; gate=0.02):")
    rng = np.random.default_rng(20260608)
    N = 30
    summary = {}
    for label, kind, sigma in [("rel_0.1%", "mult", 0.001),
                               ("rel_0.3%", "mult", 0.003),
                               ("rel_1.0%", "mult", 0.01),
                               ("abs_0.01", "add", 0.01)]:
        rmses, fails, neg_dr1 = [], 0, 0
        for _ in range(N):
            if kind == "mult":
                pert = thetas * (1.0 + sigma * rng.standard_normal(len(thetas)))
            else:
                pert = thetas + sigma * rng.standard_normal(len(thetas))
            svp = AV.apply_ansatz(pert, ops, psi0)
            r, Fp = force_rmse_of(svp, H, F_exact, DRS)
            rmses.append(r)
            if r > 0.02:
                fails += 1
            if Fp[1] < 0:
                neg_dr1 += 1
        rmses = np.array(rmses)
        summary[label] = {
            "kind": kind, "sigma": sigma, "n": N,
            "rmse_mean": float(rmses.mean()), "rmse_median": float(np.median(rmses)),
            "rmse_max": float(rmses.max()),
            "gate_fail_rate_pct": 100.0 * fails / N,
            "dr1_stays_negative_pct": 100.0 * neg_dr1 / N,
        }
        print(f"  {label:9s} ({kind}): mean={rmses.mean():.4f} median={np.median(rmses):.4f} "
              f"max={rmses.max():.4f} | fail {100*fails/N:.0f}% | dr1<0 {100*neg_dr1/N:.0f}%")

    out = {
        "reproduced": {
            "n_ops": len(ops), "n_2q": n_2q, "gs_overlap": ov,
            "energy_rel_pct": e_rel, "force_rmse_dr123": rmse123,
            "force_rmse_dr1234": rmse1234,
            "out_of_sample_dr4": {"F_adapt": F_b4[4], "F_exact": F_exact[4],
                                  "rel_pct": rel4},
        },
        "robustness": summary,
        "note": ("Multiplicative jitter is the physically faithful model for device "
                 "angle error; additive 0.01 reproduces the probe. Both quantify basin width."),
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nsaved -> {OUT}")


if __name__ == "__main__":
    main()
