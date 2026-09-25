#!/usr/bin/env python3
"""
qw_ring_test.py -- V_T vs V_X on a PERIODIC ring, plus a non-critical matched control.

Pre-registered in PREREGISTRATION-RING.md, committed (95fe3fe) before this file existed.

Two changes from SIM-2026-073 (open chain, verdict INDETERMINATE):
  1. PBC ring -> no edge effect at all.
  2. Fits are against the CHORD distance d = (n/pi)*sin(pi*dr/n), which is the correct
     CFT form on a circle. Fitting dr^-a on a ring manufactures curvature near dr=n/2.

Experiment 1: h=1.0 (critical).   Experiment 2: h=2.0 (paramagnetic control).
Expected control result: exponential decay, NO plateau. A plateau there would mean the
2.2-2.7 band belongs to the protocol, not the physics -- and per the pre-registration that
VOIDS experiment 1.

Usage: python qw_ring_test.py [--n 24]
"""
import argparse, json, os, sys, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from qw_channel_common import (  # shared with qw_channel_test.py -- ONE copy of each
    SEED, ALPHA_BP, BETA_BP, GateFailure,
    _ax, _flip, _zmul, _zz_slices,
    op_eps, op_T, op_X, op_Z, vev_ZZ, vev_X,
    fit_log_ols, fit_relerr, local_slopes, plateau, bootstrap,
    classify, enforce_run_gate, usable_arms, select_discriminant,
)

HERE = os.path.dirname(os.path.abspath(__file__))
WLO, WHI = 3, 11          # pre-registered window, n=24


def build_tfim_ring(n, h):
    """PBC: H = -sum_i Z_i Z_{i+1 mod n} - h sum_i X_i."""
    D = np.zeros((2,) * n)
    for i in range(n):                      # note: n bonds, not n-1 -- the ring closes
        eq, ne = _zz_slices(n, i)
        for s in eq: D[s] -= 1.0
        for s in ne: D[s] += 1.0
    diag = D.reshape(-1); del D

    def matvec(v):
        out = diag * v
        A = v.reshape((2,) * n)
        for k in range(n):
            out -= h * np.flip(A, axis=_ax(n, k)).reshape(-1)
        return out
    return LinearOperator((1 << n, 1 << n), matvec=matvec, dtype=np.float64), diag


def exact_e0_ring(n, h):
    """Analytic free-fermion GS energy per site for the PBC TFIM (G1 gate).
    Ground state lives in the even (antiperiodic, NS) sector: k = +-(2m+1)pi/n."""
    ks = [(2 * m + 1) * np.pi / n for m in range(n)]
    eps = [2.0 * np.sqrt(1 + h * h - 2 * h * np.cos(k)) for k in ks]
    return -0.5 * sum(eps) / n


def chord(n, dr):
    return (n / np.pi) * np.sin(np.pi * np.asarray(dr, dtype=float) / n)


def force_profile(n, gs, e0, H, arm, anchor, dr_values):
    """F(dr) for one arm on the ring.

    Returns (F, dropped) where `dropped` records every separation that produced no value
    and why. Silently skipping points shrinks the fit window without leaving a trace in
    the output -- flagged by the 2026-09-04 code review as an unrecorded data loss."""
    if arm == "eps":
        ap = lambda j, sv: op_eps(n, j, sv)
    elif arm == "T":
        v = vev_ZZ(n, anchor, gs); ap = lambda j, sv: op_T(n, j, sv, v)
    elif arm == "X":
        v = vev_X(n, anchor, gs); ap = lambda j, sv: op_X(n, j, sv, v)
    elif arm == "Z":
        ap = lambda j, sv: op_Z(n, j, sv)
    else:
        raise ValueError(
            "unknown arm %r; expected one of eps, T, X, Z. (Before 2026-09-04 this fell "
            "through with no else-branch and raised UnboundLocalError on `ap` instead.)" % (arm,))

    cache = {}
    def single(j):
        if j not in cache:
            w = ap(j, gs); nr = np.linalg.norm(w)
            cache[j] = (float((w / nr) @ H.matvec(w / nr)) - e0) if nr > 1e-12 else np.nan
        return cache[j]

    F, dropped = {}, {}
    for dr in dr_values:
        j2 = (anchor + dr) % n
        w = ap(j2, ap(anchor, gs)); nr = np.linalg.norm(w)
        if nr < 1e-12:
            dropped[int(dr)] = {"reason": "dual-excitation norm below 1e-12",
                                "norm": float(nr)}
            continue
        psi = w / nr
        F[dr] = (float(psi @ H.matvec(psi)) - e0) - (single(anchor) + single(j2))
    return F, dropped


def fit_exp(dr, y):
    """Exponential decay fit |F| ~ B exp(-dr/xi). Returns (xi, r2) -- the control's expectation."""
    ly = np.log(np.abs(y)); x = np.asarray(dr, float)
    b, a = np.polyfit(x, ly, 1)
    pred = b * x + a
    ss = 1.0 - ((ly - pred) ** 2).sum() / max(((ly - ly.mean()) ** 2).sum(), 1e-30)
    return (-1.0 / b if b < 0 else np.inf), float(ss)


def r2_power(x, y):
    lx, ly = np.log(x), np.log(np.abs(y))
    b, a = np.polyfit(lx, ly, 1); pred = b * lx + a
    return 1.0 - ((ly - pred) ** 2).sum() / max(((ly - ly.mean()) ** 2).sum(), 1e-30)


def run(n, h, label):
    anchor = 0
    print(f"\n{'='*76}\n{label}  --  n={n}, h={h}, PBC ring, anchor={anchor}\n{'='*76}")
    H, _ = build_tfim_ring(n, h)
    t = time.time()
    w, vec = eigsh(H, k=1, which="SA", tol=1e-10)
    gs = vec[:, 0] / np.linalg.norm(vec[:, 0]); e0 = float(w[0])
    e_exact = exact_e0_ring(n, h)
    g1 = abs(e0 / n - e_exact)
    print(f"  GS in {time.time()-t:.0f}s   E0/n = {e0/n:.9f}   exact = {e_exact:.9f}   "
          f"|diff| = {g1:.2e}  -> G1 {'PASS' if g1 < 1e-6 else 'FAIL'}")
    # RUN-LEVEL gate: raises, so no verdict can be emitted from a wrong ground state.
    enforce_run_gate("G1 (PBC ground state vs exact free fermions)", g1 < 1e-6,
                     f"|E0/n - exact| = {g1:.3e} exceeds 1e-6")

    dr_all = list(range(1, n - 1))
    out = {"n": n, "h": h, "label": label, "E0": e0, "E0_per_site": e0/n,
           "G1_exact_free_fermion": {"exact": e_exact, "abs_diff": g1, "pass": bool(g1 < 1e-6)},
           "window": [WLO, min(WHI, n // 2 - 1)], "arms": {}}

    for arm in ("eps", "T", "X", "Z"):
        t = time.time()
        F, dropped = force_profile(n, gs, e0, H, arm, anchor, dr_all)
        # G2: ring symmetry F(dr) == F(n-dr)
        sym = {}
        for dr in (3, 5, 7):
            if dr in F and (n - dr) in F:
                sym[dr] = abs(F[dr] - F[n - dr]) / max(abs(F[dr]), 1e-30)
        g2 = max(sym.values()) if sym else np.nan
        whi = min(WHI, n // 2 - 1)   # = 11 at n=24, the pre-registered value;
                                     # smaller n only ever shrinks it (antipode excluded)
        drs = np.array([d for d in sorted(F) if WLO <= d <= whi])
        y = np.array([F[d] for d in drs]); d_ch = chord(n, drs)
        a_ch, se = fit_log_ols(d_ch, y)
        a_raw, _ = fit_log_ols(drs.astype(float), y)
        bs = bootstrap(d_ch, y)
        mid, sl = local_slopes(d_ch, y)
        pl = plateau(sl)
        xi, r2e = fit_exp(drs, y)
        r2p = r2_power(d_ch, y)
        g2_pass = bool(np.isfinite(g2) and g2 < 0.01)
        out["arms"][arm] = {
            # PER-ARM gate. An arm failing G2 may still be REPORTED (its failure is often
            # the finding -- the Z arm's 93% violation IS the Z2 sector obstruction of
            # SIM-2026-074) but usable_arms() bars it from supplying any verdict.
            "gates_passed": g2_pass,
            "dropped_separations": dropped,
            "n_dropped": len(dropped),
            "gate_note": ("PASSED per-arm gates." if g2_pass else
                          "VOID ARM: failed G2 ring symmetry. Reported for diagnosis only; "
                          "barred from every discriminant. No number from this arm may be quoted."),
            "F_full": {int(k): float(v) for k, v in sorted(F.items())},
            "G2_ring_symmetry_max_rel": g2, "G2_pass": g2_pass,
            "alpha_chord": a_ch, "sigma_fit": se, "bootstrap_sigma": bs["std"],
            "bootstrap_sigma_interpretation": bs["sigma_interpretation"],
            # cross-check required by PREREGISTRATION-RING.md; was absent before 2026-09-04
            "alpha_chord_relerr_crosscheck": fit_relerr(d_ch, y),
            "alpha_raw_dr_for_comparison": a_raw,
            "plateau_n": pl[0], "plateau_value": pl[1],
            "chord_slopes": [float(s) for s in sl],
            "amplitude_at_dr3": float(F.get(3, np.nan)),
            "power_r2": r2p, "exp_xi": float(xi), "exp_r2": r2e,
            "better_model": "power" if r2p >= r2e else "exponential",
        }
        print(f"  {arm:4s} {time.time()-t:5.1f}s  alpha_chord={a_ch:6.3f}+/-{bs['std']:.3f}  "
              f"(raw-dr {a_raw:6.3f})  plateau {pl[0]}@{pl[1] if pl[0] else float('nan'):.3f}  "
              f"G2 {'PASS' if out['arms'][arm]['G2_pass'] else 'FAIL'} ({g2:.1e})  "
              f"R2 pow={r2p:.4f} exp={r2e:.4f} -> {out['arms'][arm]['better_model']}")
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=24)
    args = ap.parse_args()
    n = args.n
    t0 = time.time()

    crit = run(n, 1.0, "EXPERIMENT 1 -- CRITICAL")
    ctrl = run(n, 2.0, "EXPERIMENT 2 -- MATCHED CONTROL (paramagnetic)")

    # ---- control verdict FIRST: per pre-registration it can void experiment 1
    plateaus = {a: (ctrl["arms"][a]["plateau_n"], ctrl["arms"][a]["plateau_value"])
                for a in ("eps", "T", "X", "Z")}
    # Band widened to 1.8-3.2 from the 2.2-2.7 named in PREREGISTRATION-RING.md. Widening is
    # CONSERVATIVE (it can only make contamination easier to declare, never harder) but it was
    # undocumented before 2026-09-04; recorded here and in the output per the code review.
    CONTAM_BAND = (1.8, 3.2)
    contaminated = [a for a, (k, v) in plateaus.items()
                    if k >= 3 and np.isfinite(v) and CONTAM_BAND[0] <= v <= CONTAM_BAND[1]]
    ctrl_verdict = "CONTROL_CONTAMINATED" if contaminated else "CONTROL_CLEAN"
    ctrl["verdict"] = ctrl_verdict
    ctrl["contaminated_arms"] = contaminated
    ctrl["contamination_band"] = {
        "used": list(CONTAM_BAND), "preregistered": [2.2, 2.7],
        "note": ("Widened conservatively; a wider band can only make CONTROL_CONTAMINATED "
                 "easier to trigger, never harder. Recorded because the pre-registration "
                 "named a narrower one.")}

    # Kramers-Wannier check: at h=1, Z_jZ_{j+1} and X_j are the SAME operator.
    ft = crit["arms"]["T"]["F_full"]; fx = crit["arms"]["X"]["F_full"]
    kw = max(abs(ft[k] - fx[k]) / max(abs(ft[k]), 1e-30) for k in ft)
    crit["kramers_wannier_TX_identity"] = {
        "max_rel_diff": kw, "identical": bool(kw < 1e-8),
        "meaning": ("At h=1 the TFIM is self-dual with Z_jZ_{j+1} <-> X_j, so the T and X arms are "
                    "the SAME continuum operator (energy density, Delta=1). HYP-2026-008's registered "
                    "test therefore compared epsilon against epsilon and could not discriminate. The "
                    "true spin primary is Z_j (Delta=1/8), measured here as the Z arm.")}
    # ---- PRIMARY discriminant: spin (Z) vs energy (T) -- genuinely different operators.
    #
    # DEVIATION FROM PREREGISTRATION-RING.md, recorded in code AND in the output JSON rather
    # than only in a comment: that document registered three arms with T-vs-X as primary. The
    # Kramers-Wannier identity verified above shows T and X are the SAME operator, making that
    # contrast vacuous. A fourth arm (Z, the true spin primary) was added mid-experiment.
    crit["preregistration_deviation"] = {
        "registered": "three arms (eps, T, X); primary contrast T vs X",
        "executed": "four arms (eps, T, X, Z); primary contrast T vs Z",
        "reason": ("The Kramers-Wannier self-duality identity verified in this same run shows "
                   "T and X are the same continuum operator at h=1, making the registered "
                   "contrast vacuous. Z (the true spin primary) was added to supply a real one."),
        "honest_status": ("A genuine deviation from the pre-registered design, recorded rather "
                          "than concealed. Because it was decided AFTER seeing data, no Z-arm "
                          "exponent may be quoted as a pre-registered result."),
    }

    energy_arm, spin_arm = "T", "Z"
    can_discriminate, barred, bar_reason = select_discriminant(
        crit["arms"], energy_arm, spin_arm)

    if not can_discriminate:
        # A gate-failed arm may NOT supply a verdict. Before 2026-09-04 the Z arm -- which fails
        # G2 ring symmetry at 93% against a 1% bar -- was used anyway and the driver printed a
        # pre-registered verdict computed from it. Found by the two-axis code review.
        crit["discrimination"] = {
            "arms_compared": energy_arm + " (energy density) vs " + spin_arm + " (spin primary)",
            "VERDICT": None,
            "verdict_withheld": True,
            "reason": bar_reason,
            "barred_arms": {a: crit["arms"][a]["gate_note"] for a in barred},
            "what_this_means": ("The spin-vs-energy contrast is UNAVAILABLE, not indeterminate. "
                                "Z_j is Z2-odd, so single excitations are Z2-odd while dual ones "
                                "are Z2-even and the energy-difference observable subtracts across "
                                "symmetry sectors. A redesigned observable is required before this "
                                "contrast can be measured at all. See SIM-2026-074."),
        }
        v, D, gap, ratio, why = None, float("nan"), float("nan"), float("nan"), ""
    else:
        A, B = crit["arms"][energy_arm], crit["arms"][spin_arm]
        v, D, gap, ratio, why = classify(
            A["alpha_chord"], A["bootstrap_sigma"], B["alpha_chord"], B["bootstrap_sigma"],
            A["plateau_n"], B["plateau_n"], A["amplitude_at_dr3"], B["amplitude_at_dr3"])
        crit["discrimination"] = {
            "arms_compared": energy_arm + " (energy density) vs " + spin_arm + " (spin primary)",
            # Keys are named for the ARM they hold. The pre-2026-09-04 code emitted the Z arm
            # under the key "alpha_X" while the real X arm held a different value.
            "alpha_" + energy_arm: A["alpha_chord"],
            "alpha_" + spin_arm: B["alpha_chord"],
            "separation_sigma": D, "abs_gap": gap, "amplitude_ratio": ratio,
            "VERDICT": v, "reading": why,
        }

    if ctrl_verdict == "CONTROL_CONTAMINATED":
        crit["discrimination"]["VOIDED_BY_CONTROL"] = True
        crit["discrimination"]["note"] = (
            "Per PREREGISTRATION-RING.md the contaminated control OVERRIDES this verdict "
            "entirely. Any A/B/C/D label above is VOID.")

    print("\n" + "#" * 76)
    print(f"  CONTROL (h=2, no CFT should exist): {ctrl_verdict}")
    for a, (k, val) in plateaus.items():
        best = ctrl["arms"][a]["better_model"]
        print(f"    {a:4s} plateau {k} slopes @ {val if k else float('nan'):.3f}   "
              f"xi={ctrl['arms'][a]['exp_xi']:.3f}  better fit: {best}")
    print("")
    print("  EXPERIMENT 1 (h=1, critical)   [T=energy vs Z=spin]:")
    for a in ("eps", "T", "X", "Z"):
        r = crit["arms"][a]
        ac = r["alpha_chord"]
        acs = ("%7.3f" % ac) if ac == ac else "    nan"
        pv = r["plateau_value"]
        pvs = ("%.3f" % pv) if pv == pv else "nan"
        flag = "" if r["gates_passed"] else "   <<< VOID ARM (failed G2), barred from verdict"
        print("    %-4s alpha_chord=%s +/- %.3f  plateau %d@%s%s"
              % (a, acs, r["bootstrap_sigma"], r["plateau_n"], pvs, flag))
    d = crit["discrimination"]
    if d.get("verdict_withheld"):
        print("")
        print("    NO VERDICT EMITTED -- " + d["reason"])
    else:
        print("    D = %.2f sigma | gap = %.3f | amp ratio = %.2f" % (D, gap, ratio))
        print("    PRE-REGISTERED VERDICT: %s%s" % (
            v, "   <<< VOIDED BY CONTROL" if ctrl_verdict == "CONTROL_CONTAMINATED" else ""))

    print("#" * 76)

    dst = os.path.join(HERE, f"ring_test_n{n}_results.json")
    json.dump({"critical": crit, "control": ctrl}, open(dst, "w"), indent=2, default=float)
    print(f"\nwrote {dst}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    try:
        main()
    except GateFailure as e:
        print("")
        print("!! RUN VOID -- " + str(e))
        sys.exit(2)
