"""
PROBE 4 -- SCALING verification of the ADAPT-VQE cheap-circuit claim (task #95).

Claim under test (from adapt_vqe_results.json):
    At L=8, ADAPT-VQE reaches GS-overlap 0.9998 + force RMSE 0.0045 at n_2q=25
    (ZZPhase<=75), 6x cheaper than chi=3 MERA's 451. -> QCUP hardware path may reopen.

L=8 alone proves nothing. The holographic / continuum story REQUIRES a trend: the
2q-gate cost at first force-faithfulness must grow MILDLY with L (sub-linear/linear)
for the cheap-win to be real. If it BLOWS UP with L, the L=8 result is a small-system
artifact and the QCUP path stays closed.

This script reuses the EXACT ADAPT growth from adapt_vqe_force.py (build_pool,
reference_state, apply_ansatz, select_next_op, optimize_angles), all of which already
take L, and runs it for L = 8, 10, 12. The TFIM is built the same way
(FC.build_tfim_sparse(L)); exact GS via eigsh.

For each L we record n_2q at FIRST faithfulness (overlap>0.99 AND force RMSE<0.02 over
dr in {1,2,3}). If faithfulness is not reached by MAX_OPS, we report n_2q at the first
overlap>0.99 (and its force RMSE) and flag faithful-not-reached.

Does NOT modify adapt_vqe_force.py or any existing result JSON. Imports its functions.
"""
import json
import time

import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import adapt_vqe_force as AV

OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_scaling.json"
LS = [8, 10, 12]
OVERLAP_TARGET = 0.99
FORCE_RMSE_TARGET = 0.02
GRAD_TOL = 1e-3
MAX_OPS = 60
DRS = [1, 2, 3]


def run_one_L(L):
    """Run ADAPT-VQE growth for a single L, reusing adapt_vqe_force functions.

    Returns a dict with the full per-step trace plus the two milestone records:
      first_overlap99   -> first step with GS-overlap > 0.99
      first_faithful    -> first step with overlap>0.99 AND force_rmse<0.02
    """
    t0 = time.time()
    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0])
    psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)

    pool = AV.build_pool(L)             # generalizes to any L
    psi0 = AV.reference_state(L)        # |+>^L

    ops, thetas = [], np.zeros(0)
    steps = []
    first_overlap99 = None
    first_faithful = None

    print(f"\n{'='*74}\nL = {L}  (dim 2^{L} = {2**L})  E_gs = {Egs:.6f}")
    print("  F(dr) exact: " + ", ".join(f"dr={d}:{F_exact[d]:+.5f}" for d in DRS))
    print(f"  pool = {len(pool)} gens; target overlap>{OVERLAP_TARGET}, force RMSE<{FORCE_RMSE_TARGET}")

    for step in range(1, MAX_OPS + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = AV.select_next_op(psi_cur, H, pool)
        if best_grad < GRAD_TOL:
            print(f"  [converged] |grad| {best_grad:.2e} < {GRAD_TOL} at step {step}; stop.")
            break

        ops.append(best_op)
        theta_init = np.concatenate([thetas, [0.0]])
        thetas, E = AV.optimize_angles(ops, psi0, H, theta_init)

        sv = AV.apply_ansatz(thetas, ops, psi0)
        e_err = E - Egs
        rel = abs(e_err) / abs(Egs) * 100
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
        n_2q = sum(1 for o in ops if o["is_2q"])
        zz_ub = n_2q * 3
        faithful = ov > OVERLAP_TARGET and f_rmse < FORCE_RMSE_TARGET

        rec = {
            "step": step, "added": best_op["name"], "grad": best_grad,
            "n_ops": len(ops), "n_2q": n_2q, "zzphase_ub": zz_ub,
            "energy": E, "energy_rel_pct": rel, "gs_overlap": ov,
            "F_adapt": {str(d): F_b[d] for d in DRS},
            "force_rmse": f_rmse, "faithful": faithful,
        }
        steps.append(rec)

        if ov > OVERLAP_TARGET and first_overlap99 is None:
            first_overlap99 = rec
        if faithful and first_faithful is None:
            first_faithful = rec

        flag = "FAITHFUL" if faithful else ("ov>0.99" if ov > OVERLAP_TARGET else "--")
        print(f"  step {step:2d} | +{best_op['name']:7s} | ops={len(ops):2d} 2q={n_2q:2d} "
              f"ZZ<={zz_ub:3d} | E_rel={rel:5.2f}% | GSov={ov:.4f} | "
              f"F_rmse={f_rmse:.4f} | {flag}", flush=True)

        # stop once we have BOTH a faithful point (the deliverable). If we only have
        # overlap>0.99 but not yet faithful, keep growing up to MAX_OPS to give force
        # a chance.
        if first_faithful is not None:
            break

    wall = time.time() - t0
    out = {
        "L": L, "E_gs": Egs,
        "F_exact": {str(d): F_exact[d] for d in DRS},
        "pool_size": len(pool), "max_ops": MAX_OPS, "n_steps_run": len(steps),
        "first_overlap99": first_overlap99,
        "first_faithful": first_faithful,
        "best_overlap": max((s["gs_overlap"] for s in steps), default=0.0),
        "best_force_rmse_at_ov99": (first_overlap99["force_rmse"]
                                    if first_overlap99 else None),
        "steps": steps, "wall_seconds": wall,
    }
    return out


def naive_chi3_cost(L):
    """chi=3-style MERA 2q-gate cost estimate that scales with L.

    The chi=3 MERA compile gave 451 ZZPhase at L=8. A MERA on L sites has O(log2 L)
    layers, each with O(L) disentangler+isometry tensors; each chi=3 two-site tensor
    compiles to a roughly fixed ZZPhase budget. So total ZZPhase ~ c * L * log2(L).
    Anchor the constant c so the estimate hits 451 at L=8:
        451 = c * 8 * log2(8) = c * 8 * 3 = 24c  =>  c = 18.79.
    This is a TRANSPARENT yardstick (not a real compile) for "does ADAPT beat a
    MERA whose cost grows with system size".
    """
    c = 451.0 / (8 * np.log2(8))
    return c * L * np.log2(L)


def main():
    t_all = time.time()
    print("#" * 74)
    print("PROBE 4 -- ADAPT-VQE cheap-circuit SCALING: n_2q(faithful) vs L")
    print("#" * 74)

    per_L = {}
    full = {"LS": LS, "overlap_target": OVERLAP_TARGET,
            "force_rmse_target": FORCE_RMSE_TARGET, "max_ops": MAX_OPS,
            "drs": DRS, "results": {}}

    for L in LS:
        try:
            res = run_one_L(L)
        except Exception as e:  # never silently drop a missing L
            print(f"  L={L} FAILED: {type(e).__name__}: {e}")
            per_L[str(L)] = {"error": f"{type(e).__name__}: {e}"}
            full["results"][str(L)] = {"error": f"{type(e).__name__}: {e}"}
            with open(OUT, "w") as f:
                json.dump(full, f, indent=2)
            continue

        full["results"][str(L)] = res
        ff = res["first_faithful"]
        o99 = res["first_overlap99"]
        chi3 = naive_chi3_cost(L)
        if ff is not None:
            per_L[str(L)] = {
                "n_2q": ff["n_2q"], "zzphase_ub": ff["zzphase_ub"],
                "overlap": ff["gs_overlap"], "force_rmse": ff["force_rmse"],
                "faithful": True, "chi3_naive_zzphase": chi3,
            }
        elif o99 is not None:
            per_L[str(L)] = {
                "n_2q": o99["n_2q"], "zzphase_ub": o99["zzphase_ub"],
                "overlap": o99["gs_overlap"], "force_rmse": o99["force_rmse"],
                "faithful": False, "note": "faithful-not-reached: n_2q at first overlap>0.99",
                "chi3_naive_zzphase": chi3,
            }
        else:
            per_L[str(L)] = {
                "n_2q": None, "zzphase_ub": None,
                "overlap": res["best_overlap"], "force_rmse": None,
                "faithful": False, "note": "overlap>0.99 never reached within MAX_OPS",
                "chi3_naive_zzphase": chi3,
            }
        full["per_L"] = per_L
        with open(OUT, "w") as f:
            json.dump(full, f, indent=2)

    # ---- scaling analysis / verdict ----
    print("\n" + "#" * 74)
    print("SCALING TABLE")
    print(f"  {'L':>3} {'n_2q(faith)':>12} {'ZZ<=':>6} {'overlap':>9} {'F_rmse':>9} "
          f"{'faithful':>9} {'chi3~ZZ':>9}")
    xs, ys = [], []
    for L in LS:
        p = per_L.get(str(L), {})
        if "error" in p:
            print(f"  {L:>3}  ERROR: {p['error']}")
            continue
        n2 = p.get("n_2q")
        print(f"  {L:>3} {str(n2):>12} {str(p.get('zzphase_ub')):>6} "
              f"{p.get('overlap', float('nan')):>9.4f} "
              f"{(p.get('force_rmse') if p.get('force_rmse') is not None else float('nan')):>9.4f} "
              f"{str(p.get('faithful')):>9} {p.get('chi3_naive_zzphase', float('nan')):>9.1f}")
        if n2 is not None:
            xs.append(L); ys.append(n2)

    # quantify growth: linear and log-log slopes on n_2q(faithful) vs L
    growth = {}
    verdict = None
    if len(xs) >= 2:
        xs = np.array(xs, float); ys = np.array(ys, float)
        # linear slope (gates per added site)
        lin_slope = float(np.polyfit(xs, ys, 1)[0])
        # power-law exponent p in n_2q ~ L^p
        loglog_p = float(np.polyfit(np.log(xs), np.log(ys), 1)[0])
        ratio = float(ys[-1] / ys[0])
        L_ratio = float(xs[-1] / xs[0])
        growth = {"L_points": xs.tolist(), "n2q_points": ys.tolist(),
                  "linear_slope_gates_per_site": lin_slope,
                  "loglog_exponent_p": loglog_p,
                  "n2q_ratio_last_over_first": ratio,
                  "L_ratio_last_over_first": L_ratio}
        print(f"\n  linear slope (gates/site): {lin_slope:.2f}")
        print(f"  power-law exponent p (n_2q ~ L^p): {loglog_p:.2f}")
        print(f"  n_2q grew {ratio:.2f}x while L grew {L_ratio:.2f}x")

        # criterion: cheap-win persists if growth is at-most-mild.
        # "explodes" => super-linear AND n_2q already comparable to chi=3's 451.
        all_faithful = all(per_L.get(str(L), {}).get("faithful") for L in LS
                           if "error" not in per_L.get(str(L), {}))
        biggest_n2 = ys[-1]
        chi3_big = naive_chi3_cost(xs[-1])
        if loglog_p <= 1.3 and biggest_n2 < 0.5 * chi3_big:
            verdict = "SUPPORTS_CLAIM"
        elif loglog_p <= 1.6 and biggest_n2 < chi3_big:
            verdict = "PARTIAL"
        else:
            verdict = "REFUTES_CLAIM"
        growth["all_L_faithful"] = bool(all_faithful)
        growth["verdict"] = verdict
        growth["biggest_n2q"] = float(biggest_n2)
        growth["chi3_naive_at_biggest_L"] = float(chi3_big)
    else:
        verdict = "INCONCLUSIVE"
        growth["verdict"] = verdict
        growth["note"] = "fewer than 2 usable L points"

    full["per_L"] = per_L
    full["growth"] = growth
    full["wall_seconds_total"] = time.time() - t_all
    with open(OUT, "w") as f:
        json.dump(full, f, indent=2)
    print(f"\n  VERDICT: {verdict}")
    print(f"  total wall: {full['wall_seconds_total']:.1f} s")
    print(f"  saved -> {OUT}")


if __name__ == "__main__":
    main()
