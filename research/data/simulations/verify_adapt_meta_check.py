"""
META-VERIFICATION of PROBE 2's robustness claim (task #95 adversarial check).

PROBE 2 concluded PARTIAL: physics real (dr=4 OOS 4.2%) but 0.0045 RMSE is a
"fragile knife-edge" because N(0,0.01) angle jitter inflates force RMSE ~17x.

I want to attack THAT conclusion three ways:

  (A) SEED ROBUSTNESS: PROBE 2 used a single seed (5 samples). Is the "~17x
      inflation, 4/5 fail the 0.02 gate" conclusion stable across seeds, or did
      one seed happen to land badly? Run many seeds, many samples.

  (B) IS sigma=0.01 A FAIR PERTURBATION? The angles have varying magnitude. A
      flat N(0,0.01) on ALL 25 angles may be small relative to big angles but
      huge relative to small ones. Report the angle magnitude distribution and a
      RELATIVE (multiplicative 1%) perturbation as a sanity cross-check.

  (C) DOES THE PERTURBATION PREMISE EVEN MATTER? On real hardware you do NOT take
      the ideal ADAPT angles and add Gaussian noise to the *gate angles*; you run
      the *circuit* (these exact angles) under gate/readout noise. The honest
      hardware-relevance question is: how good is the NOISELESS prepared state
      (overlap, force) -- which IS the thing a fault-tolerant or low-error run
      targets. The "knife-edge" framing answers a question (angle-parameter
      sensitivity) that is real for a NISQ VQE re-optimization but is NOT the
      same as "the force signal is a 3-point coincidence." Separate the two.

This script does NOT modify any existing file. Reuses adapt_vqe_force + brickwork_force_check.
"""
import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import adapt_vqe_force as AV

L = 8
MAX_OPS = 25
GRAD_TOL = 1e-3
DRS_FIT = [1, 2, 3]
DRS_EXT = [1, 2, 3, 4]
GATE = 0.02  # the faithful force-RMSE gate


def grow():
    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    psi_gs = psi_eig[:, 0]
    pool = AV.build_pool(L)
    psi0 = AV.reference_state(L)
    ops, thetas = [], np.zeros(0)
    for step in range(1, MAX_OPS + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = AV.select_next_op(psi_cur, H, pool)
        if best_grad < GRAD_TOL:
            break
        ops.append(best_op)
        thetas, E = AV.optimize_angles(ops, psi0, H, np.concatenate([thetas, [0.0]]))
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        if ov > 0.999:
            break
    return H, psi_gs, psi0, ops, thetas


def force_rmse(sv, H, F_exact, drs):
    F, _, _ = FC.force_profile(sv, H, L, drs)
    return float(np.sqrt(np.mean([(F[d] - F_exact[d]) ** 2 for d in drs])))


def main():
    H, psi_gs, psi0, ops, thetas = grow()
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS_EXT)

    sv0 = AV.apply_ansatz(thetas, ops, psi0)
    base_rmse = force_rmse(sv0, H, F_exact, DRS_FIT)
    base_ov = float(abs(np.vdot(psi_gs, sv0)) ** 2)
    print(f"baseline: overlap={base_ov:.6f}  force_rmse(dr123)={base_rmse:.5f}")

    # angle magnitude distribution
    am = np.abs(thetas)
    print(f"\nangle |theta|: min={am.min():.4f} med={np.median(am):.4f} "
          f"max={am.max():.4f} mean={am.mean():.4f}")
    print("  -> N(0,0.01) absolute jitter is {:.1f}% of the MEDIAN angle, "
          "{:.1f}% of the SMALLEST".format(100*0.01/np.median(am), 100*0.01/am.min()))

    # (A) SEED ROBUSTNESS: 40 seeds x 5 samples each, absolute N(0,0.01)
    print("\n(A) SEED ROBUSTNESS -- 40 seeds, abs N(0,0.01), 5 samples/seed:")
    all_rmses = []
    frac_fail_per_seed = []
    for s in range(40):
        rng = np.random.default_rng(1000 + s)
        seed_rmses = []
        for _ in range(5):
            dth = rng.normal(0.0, 0.01, size=thetas.shape)
            svp = AV.apply_ansatz(thetas + dth, ops, psi0)
            seed_rmses.append(force_rmse(svp, H, F_exact, DRS_FIT))
        seed_rmses = np.array(seed_rmses)
        all_rmses.extend(seed_rmses.tolist())
        frac_fail_per_seed.append(float(np.mean(seed_rmses > GATE)))
    all_rmses = np.array(all_rmses)
    print(f"  200 perturbed states: mean RMSE={all_rmses.mean():.5f} "
          f"median={np.median(all_rmses):.5f} std={all_rmses.std():.5f}")
    print(f"  fraction EXCEEDING the {GATE} gate: {np.mean(all_rmses > GATE):.2%}")
    print(f"  inflation vs baseline (mean/base): {all_rmses.mean()/base_rmse:.1f}x")
    print(f"  PROBE 2 reported mean=0.078, 4/5 fail. Cross-seed mean here: "
          f"{all_rmses.mean():.4f}, fail-rate {np.mean(all_rmses > GATE):.0%}")

    # (B) RELATIVE perturbation: 1% multiplicative on each angle
    print("\n(B) RELATIVE (multiplicative 1%) perturbation -- 200 samples:")
    rel_rmses = []
    for s in range(40):
        rng = np.random.default_rng(2000 + s)
        for _ in range(5):
            dth = thetas * rng.normal(0.0, 0.01, size=thetas.shape)
            svp = AV.apply_ansatz(thetas + dth, ops, psi0)
            rel_rmses.append(force_rmse(svp, H, F_exact, DRS_FIT))
    rel_rmses = np.array(rel_rmses)
    print(f"  mean RMSE={rel_rmses.mean():.5f} median={np.median(rel_rmses):.5f} "
          f"std={rel_rmses.std():.5f}  fail-rate={np.mean(rel_rmses > GATE):.0%}")

    # (C) smaller absolute jitter sweep: how small must jitter be to stay under gate?
    print("\n(C) JITTER SWEEP -- mean force RMSE vs sigma (200 samples each):")
    for sigma in [0.001, 0.002, 0.005, 0.01, 0.02]:
        vals = []
        for s in range(40):
            rng = np.random.default_rng(3000 + s)
            for _ in range(5):
                dth = rng.normal(0.0, sigma, size=thetas.shape)
                svp = AV.apply_ansatz(thetas + dth, ops, psi0)
                vals.append(force_rmse(svp, H, F_exact, DRS_FIT))
        vals = np.array(vals)
        print(f"  sigma={sigma:.3f}: mean RMSE={vals.mean():.5f} "
              f"fail-rate={np.mean(vals > GATE):.0%}")


if __name__ == "__main__":
    main()
