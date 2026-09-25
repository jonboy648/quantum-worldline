"""
ADAPT basin-robustness test (follow-up to task #95 / ERRATA D4 corrected verdict).

QUESTION: the 25-op ADAPT state nails GS+force at exact angles but fails the force gate
under ~1% angle jitter (only ~0.1% precision survives). Is that fragility intrinsic to
ADAPT solutions at this gate count, or just an artifact of optimizing the POINT energy?

METHOD: re-run the same ADAPT growth (same pool, same gradient selection, same L=8 critical
TFIM) but optimize a ROBUST loss: L_rob(theta) = mean_k E(theta * (1 + delta_k)) over K fixed
multiplicative jitter draws delta_k ~ N(0, sigma_train^2), sigma_train = 0.01 (the failure
scale; multiplicative = physically faithful per the #95 verification). Common random numbers
(fixed draws) keep L-BFGS stable. Grow to the same op budget (25) plus margin (max 32).

EVALUATION (the only fair comparison -- same protocol as verify_adapt_force_robust.py):
at the final robust solution theta*, measure (a) clean overlap/force RMSE at theta* exactly,
(b) force-gate failure rate under FRESH multiplicative jitter sigma_eval in {0.001, 0.003, 0.01}
x 40 samples, vs the POINT-OPTIMIZED solution's published rates (86.7-100% fail at sigma=0.01).
VERDICT: BASIN_WIDENED if the robust solution keeps force RMSE < 0.02 in >=80% of sigma=0.01
samples while clean force RMSE stays < 0.02; FRAGILITY_INTRINSIC if it cannot reach the force
gate at all or fails jitter as badly as the original; PARTIAL otherwise.
Output: research/data/builds/adapt_robust_basin.json
"""
import json
import time

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh

import adapt_vqe_force as AV
import brickwork_force_check as FC

L = 8
OUT = "D:/quantum-worldline/research/data/builds/adapt_robust_basin.json"
SIGMA_TRAIN = 0.01
K_TRAIN = 8
MAX_OPS = 32
GRAD_TOL = 1e-3
DRS = [1, 2, 3]
FORCE_GATE = 0.02
rng = np.random.default_rng(20260608)
# fixed common-random-number jitter draws for the robust loss
DELTAS = rng.normal(0.0, SIGMA_TRAIN, size=(K_TRAIN,))


def main():
    t0 = time.time()
    print("=" * 70)
    print("ADAPT robust-basin test: jitter-averaged loss, L=8 critical TFIM")
    print("=" * 70)
    H = FC.build_tfim_sparse(L)
    Eg_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Eg_arr[0]); psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)
    pool = AV.build_pool(L)
    psi0 = AV.reference_state(L)

    def energy(theta, ops):
        sv = AV.apply_ansatz(theta, ops, psi0)
        return float(np.real(np.vdot(sv, H @ sv)))

    def robust_loss(theta, ops):
        # multiplicative jitter, common random numbers
        return float(np.mean([energy(theta * (1.0 + d), ops) for d in DELTAS]))

    ops, thetas = [], np.zeros(0)
    trace = []
    final = None
    for step in range(1, MAX_OPS + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, g, _ = AV.select_next_op(psi_cur, H, pool)
        if g < GRAD_TOL:
            print(f"  [grad converged] {g:.2e} at step {step}")
            break
        ops.append(best_op)
        r = minimize(lambda th: robust_loss(th, ops),
                     np.concatenate([thetas, [0.0]]),
                     method="L-BFGS-B", options={"maxiter": 400, "ftol": 1e-11})
        thetas = r.x
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
        rec = {"step": step, "added": best_op["name"], "robust_loss": float(r.fun),
               "clean_energy": energy(thetas, ops), "gs_overlap": ov, "force_rmse": f_rmse}
        trace.append(rec)
        print(f"  step {step:2d} | +{best_op['name']:7s} | E_rob={r.fun:+.4f} | "
              f"GSov={ov:.4f} | F_rmse={f_rmse:.4f}", flush=True)
        with open(OUT, "w") as f:
            json.dump({"trace": trace, "status": "running"}, f, indent=2)
        if ov > 0.99 and f_rmse < FORCE_GATE:
            final = rec
            print(f"  >>> robust-faithful at step {step} <<<")
            break

    # ---- jitter evaluation at the final solution ----
    evals = {}
    for sig in (0.001, 0.003, 0.01):
        fails = 0
        rmses = []
        for _ in range(40):
            d = rng.normal(0.0, sig, size=thetas.shape)
            sv = AV.apply_ansatz(thetas * (1.0 + d), ops, psi0)
            F_b, _, _ = FC.force_profile(sv, H, L, DRS)
            fr = float(np.sqrt(np.mean([(F_b[dr] - F_exact[dr]) ** 2 for dr in DRS])))
            rmses.append(fr)
            if fr >= FORCE_GATE:
                fails += 1
        evals[str(sig)] = {"fail_rate_pct": 100.0 * fails / 40,
                           "rmse_mean": float(np.mean(rmses)), "rmse_max": float(np.max(rmses))}
        print(f"  jitter sigma={sig}: fail {evals[str(sig)]['fail_rate_pct']:.0f}%, "
              f"mean RMSE {evals[str(sig)]['rmse_mean']:.4f}")

    clean_ok = final is not None
    widened = clean_ok and evals["0.01"]["fail_rate_pct"] <= 20.0
    if widened:
        verdict = "BASIN_WIDENED: robust-trained ADAPT survives 1% jitter -- hardware-run blocker removed"
    elif clean_ok:
        verdict = ("PARTIAL: robust training reaches the force gate cleanly but still fails 1% jitter "
                   f"({evals['0.01']['fail_rate_pct']:.0f}%) -- fragility partly intrinsic")
    else:
        verdict = "FRAGILITY_INTRINSIC: robust loss cannot reach the force gate at this op budget"
    out = {"L": L, "sigma_train": SIGMA_TRAIN, "K_train": K_TRAIN,
           "point_optimized_reference": {"fail_rate_pct_at_0.01": "86.7-100 (verify_adapt_force_robust + meta-check)",
                                          "n_ops": 25},
           "n_ops_final": len(ops), "trace": trace, "final": final,
           "jitter_eval": evals, "verdict": verdict,
           "wall_seconds": time.time() - t0, "status": "done"}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  VERDICT: {verdict}")
    print(f"  saved -> {OUT}  ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
