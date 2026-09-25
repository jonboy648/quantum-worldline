#!/usr/bin/env python3
"""
qw_channel_test.py -- V_T vs V_X channel discrimination on the exact 24q critical TFIM.

This is HYP-2026-008's OWN registered killer test, written into its refutation_criteria on
2026-03-11 and never executed. Outcomes were pre-registered in PREREGISTRATION.md and committed
(aed9051 / ba1b4ae) BEFORE this file existed.

Protocol, identical across arms:
    F(dr) = [E_dual(dr) - E0] - [dE_single(anchor) + dE_single(anchor+dr)]
    psi = O_j|GS> / ||O_j|GS>||

Arms differ ONLY in O:
    eps : a(X_j + X_{j+1}) + b(X_j Z_{j+1} + Z_j X_{j+1})   a=0.635 b=-0.026   [control]
    T   : -(Z_j Z_{j+1} - <Z_j Z_{j+1}>)                                       [stress-tensor-like]
    X   : X_j - <X_j>                                                          [spin primary]

Vacuum subtraction on T and X is required, not optional: without it O|GS> keeps a large component
along |GS> and the "excitation" is mostly no excitation.

Usage:  python qw_channel_test.py [--n 24] [--quick]
"""
import argparse, json, os, sys, time
import numpy as np
from scipy.sparse.linalg import LinearOperator, eigsh

from qw_channel_common import (  # shared with qw_ring_test.py -- ONE copy of each
    SEED, ALPHA_BP, BETA_BP, GateFailure,
    _ax, _flip, _zmul, _zz_slices,
    op_eps, op_T, op_X, vev_ZZ, vev_X,
    fit_log_ols, fit_relerr, fit_linear_unweighted,
    local_slopes, plateau, bootstrap, classify, enforce_run_gate,
)

HERE = os.path.dirname(os.path.abspath(__file__))
SIMS = os.path.abspath(os.path.join(HERE, "..", "..", "data", "simulations"))


# ---------------------------------------------------------------- Hamiltonian
# MEMORY NOTE. The first implementation used fancy indexing (`v[basis ^ mask]`), which at n=24
# allocates a 134 MB int64 index array per call plus a temp per term -- it died partway through the
# n=24 run. Everything below instead views the state as an (2,)*n tensor, where a bit flip is
# np.flip along one axis and a Z is a sign flip on one slice. Same math, no index arrays.

def build_tfim(n):
    """Critical TFIM H = -sum Z_i Z_{i+1} - sum X_i, OBC. Matrix-free, no index arrays."""
    D = np.zeros((2,) * n)
    for i in range(n - 1):
        eq, ne = _zz_slices(n, i)
        for s in eq:
            D[s] -= 1.0          # -(+1)
        for s in ne:
            D[s] += 1.0          # -(-1)
    diag = D.reshape(-1)
    del D

    def matvec(v):
        out = diag * v
        A = v.reshape((2,) * n)
        for k in range(n):
            out -= np.flip(A, axis=_ax(n, k)).reshape(-1)
        return out
    return LinearOperator((1 << n, 1 << n), matvec=matvec, dtype=np.float64), diag


def ground_state(n):
    """Cached exact GS if present, else eigsh."""
    cache = os.path.join(SIMS, f"gs_{n}q_exact.npy")
    H, _ = build_tfim(n)
    if os.path.exists(cache):
        gs = np.load(cache)
        if gs.size == (1 << n):
            gs = gs / np.linalg.norm(gs)
            e0 = float(gs @ H.matvec(gs))
            print(f"  cached GS loaded: {cache}  E0={e0:.9f}")
            return gs, e0, H
    print(f"  no cache; running eigsh at n={n} ...")
    t = time.time()
    w, v = eigsh(H, k=1, which="SA", tol=1e-10)
    gs = v[:, 0] / np.linalg.norm(v[:, 0])
    print(f"  eigsh done in {time.time()-t:.0f}s  E0={w[0]:.9f}")
    if n >= 20:
        np.save(cache, gs)
    return gs, float(w[0]), H


# ------------------------------------------------------------------ operators
# ------------------------------------------------------------ force profile
def energy(H, sv):
    return float(sv @ H.matvec(sv))


def normalize(v):
    nrm = float(np.linalg.norm(v))
    return (None, nrm) if nrm < 1e-12 else (v / nrm, nrm)


def force_profile(n, gs, e0, H, arm, anchor, dr_values):
    """F(dr) for one arm. Returns dict dr -> F, plus diagnostics."""
    if arm == "eps":
        apply = lambda j, sv: op_eps(n, j, sv)
    elif arm == "T":
        v = vev_ZZ(n, anchor, gs)
        apply = lambda j, sv: op_T(n, j, sv, v)
    elif arm == "X":
        v = vev_X(n, anchor, gs)
        apply = lambda j, sv: op_X(n, j, sv, v)
    else:
        raise ValueError(arm)

    # single-site excitation energies, cached per site
    dE_single, gs_overlap = {}, {}
    def single(j):
        if j not in dE_single:
            psi, nrm = normalize(apply(j, gs))
            if psi is None:
                dE_single[j] = np.nan; gs_overlap[j] = np.nan
            else:
                dE_single[j] = energy(H, psi) - e0
                gs_overlap[j] = abs(float(psi @ gs))
        return dE_single[j]

    # `dropped` records every separation that produced no value and why. Silently skipping
    # points shrinks the fit window with no trace in the output -- flagged by the 2026-09-04
    # code review as unrecorded data loss.
    F, diag, dropped = {}, {}, {}
    for dr in dr_values:
        j2 = anchor + dr
        if j2 + 1 >= n:
            dropped[int(dr)] = {"reason": "operator support would run past the chain end",
                                "far_site": int(j2), "n": int(n)}
            continue
        psi, nrm = normalize(apply(j2, apply(anchor, gs)))
        if psi is None:
            dropped[int(dr)] = {"reason": "dual-excitation norm below 1e-12",
                                "norm": float(nrm)}
            continue
        e_dual = energy(H, psi)
        F[dr] = (e_dual - e0) - (single(anchor) + single(j2))
        diag[dr] = {"E_dual": e_dual, "dual_norm": nrm}
    return F, {"dE_single": dE_single, "gs_overlap_single": gs_overlap, "per_dr": diag,
               "dropped_separations": dropped, "n_dropped": len(dropped)}


# -------------------------------------------------------------- estimators
# ------------------------------------------------------------------- verdict
def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--n", type=int, default=24)
    ap.add_argument("--quick", action="store_true", help="n=16, fast smoke run")
    args = ap.parse_args()
    n = 16 if args.quick else args.n
    anchor = n // 4
    dr_values = list(range(1, n - anchor - 1))

    print("=" * 78)
    print(f"V_T vs V_X CHANNEL TEST -- n={n}, anchor={anchor}, dr={dr_values[0]}..{dr_values[-1]}")
    print("Pre-registered: research/tools/channel-test/PREREGISTRATION.md (aed9051/ba1b4ae)")
    print("=" * 78)

    t0 = time.time()
    print("\n[1/4] ground state")
    gs, e0, H = ground_state(n)

    print("\n[2/4] force profiles (3 arms)")
    arms = {}
    for arm in ("eps", "T", "X"):
        t = time.time()
        F, dg = force_profile(n, gs, e0, H, arm, anchor, dr_values)
        arms[arm] = {"F": F, "diag": dg}
        print(f"  {arm:4s} {len(F)} points in {time.time()-t:.1f}s   "
              f"F(3)={F.get(3, float('nan')):+.6e}  F(6)={F.get(6, float('nan')):+.6e}")

    # ---- validation gate: eps must reproduce SIM-2026-011
    print("\n[3/4] VALIDATION GATE -- eps arm vs SIM-2026-011-interaction.json")
    gate = {"checked": False, "passed": None, "max_rel_err": None, "detail": {}}
    ref_path = os.path.join(SIMS, "SIM-2026-011-interaction.json")
    if n == 24 and os.path.exists(ref_path):
        ref = json.load(open(ref_path, encoding="utf-8"))["F_interaction_avg"]
        worst, det = 0.0, {}
        for k, v in ref.items():
            dr = int(k)
            if dr in arms["eps"]["F"]:
                got, exp = arms["eps"]["F"][dr], float(v)
                rel = abs(got - exp) / max(abs(exp), 1e-30)
                det[dr] = {"published": exp, "recomputed": got, "rel_err": rel}
                worst = max(worst, rel)
        gate = {"checked": True, "passed": bool(worst < 0.01), "max_rel_err": worst, "detail": det}
        print(f"  max relative error {worst:.3%}  ->  {'PASS' if worst < 0.01 else 'FAIL'}")
        # RUN-LEVEL gate. This raises; it does not merely announce.
        # Before 2026-09-04 this block printed "Reporting and stopping" and then fell
        # straight through to the analysis and emitted a verdict -- a gate that could
        # not fail. Found by the two-axis code review.
        enforce_run_gate(
            "REPRO (eps arm vs SIM-2026-011-interaction)", worst < 0.01,
            f"max relative error {worst:.3%} exceeds the 1% bar, so the implementation "
            f"differs from the published one and no arm comparison is meaningful")
    else:
        print(f"  skipped (n={n}, gate is defined at n=24 only)")

    # ---- analysis on the PRE-REGISTERED primary window
    print("\n[4/4] analysis  (PRIMARY WINDOW dr >= 3, fixed in advance)")
    out = {"n": n, "anchor": anchor, "E0": e0, "rng_seed": SEED,
           "preregistration": "research/tools/channel-test/PREREGISTRATION.md",
           "validation_gate": gate, "arms": {}}

    for arm in ("eps", "T", "X"):
        F = arms[arm]["F"]
        x = np.array(sorted(F))
        y = np.array([F[k] for k in x])
        # Sign audit. The reference sign MUST be taken inside the analysis window: dr=1 (and for
        # the two-site operators dr=2) are contact terms that are excluded by pre-registration, and
        # anchoring on them mislabels the whole profile. A power law cannot change sign, so the
        # profile is valid only up to the first sign change AT OR AFTER the window start.
        WSTART = 3
        sgn = np.sign(y)
        in_win = np.where(x >= WSTART)[0]
        ref = sgn[in_win[0]] if len(in_win) else sgn[0]
        flips_in_window = [int(x[i]) for i in in_win if sgn[i] != ref]
        flips_below = [int(x[i]) for i in range(len(y)) if x[i] < WSTART and sgn[i] != ref]
        vmax = (min(flips_in_window) - 1) if flips_in_window else int(x.max())
        m = (x >= WSTART) & (x <= vmax)
        a_ols, se = (fit_log_ols(x[m], y[m]) if m.sum() >= 3 else (np.nan, np.nan))
        bs = bootstrap(x[m], y[m]) if m.sum() >= 3 else {"std": np.nan, "mean": np.nan}
        mid, sl = local_slopes(x, y)
        km = mid <= vmax
        pl = plateau(sl[km])
        m2 = (x >= 2) & (x <= vmax)
        rec = {
            "F": {int(k): float(F[k]) for k in x},
            "dropped_separations": arms[arm]["diag"]["dropped_separations"],
            "n_dropped": arms[arm]["diag"]["n_dropped"],
            "sign_flips_in_window": flips_in_window, "max_dr_valid": int(vmax),
            "sign_changes_below_window_informational": flips_below,
            "sign_note": ("Reference sign taken at dr=3 (window start), not dr=1. Points below the "
                          "window are contact terms and their sign is not evidence of anything. "
                          "Truncation is at the first sign change at or after dr=3, which is also "
                          "where the profile meets the numerical noise floor."),
            "primary_window_dr_ge3": {
                "n_pts": int(m.sum()), "alpha_log_ols": a_ols, "sigma_fit": se,
                "alpha_relerr": fit_relerr(x[m], y[m]) if m.sum() >= 3 else np.nan,
                "alpha_linear_unweighted_BANNED": fit_linear_unweighted(x[m], y[m]) if m.sum() >= 3 else np.nan,
                "bootstrap": bs,
                "amplitude_at_dr3": float(F.get(3, np.nan)),
            },
            "secondary_window_dr_ge2": {
                "alpha_log_ols": fit_log_ols(x[m2], y[m2])[0] if m2.sum() >= 3 else np.nan},
            "local_slopes": [{"dr_mid": float(a), "slope": float(b)} for a, b in zip(mid, sl)],
            "plateau": {"n_slopes": pl[0], "mean_slope": pl[1], "tol_rel": 0.15},
        }
        out["arms"][arm] = rec
        print(f"  {arm:4s} alpha(log-OLS,dr>=3) = {a_ols:6.3f} +/- {bs['std']:.3f} (bootstrap)"
              f"   plateau {pl[0]} slopes @ {pl[1]:.3f}"
              f"   valid dr<={vmax}"
              f"{'  [flip in window at ' + str(flips_in_window) + ']' if flips_in_window else ''}")

    T, X = out["arms"]["T"]["primary_window_dr_ge3"], out["arms"]["X"]["primary_window_dr_ge3"]
    verdict, D, gap, ratio, why = classify(
        T["alpha_log_ols"], T["bootstrap"]["std"],
        X["alpha_log_ols"], X["bootstrap"]["std"],
        out["arms"]["T"]["plateau"]["n_slopes"], out["arms"]["X"]["plateau"]["n_slopes"],
        T["amplitude_at_dr3"], X["amplitude_at_dr3"])
    out["discrimination"] = {"alpha_T": T["alpha_log_ols"], "alpha_X": X["alpha_log_ols"],
                             "separation_sigma": D, "abs_gap": gap, "amplitude_ratio": ratio,
                             "VERDICT": verdict, "reading": why}
    print("\n" + "=" * 78)
    print(f"  alpha_T = {T['alpha_log_ols']:.3f} +/- {T['bootstrap']['std']:.3f}")
    print(f"  alpha_X = {X['alpha_log_ols']:.3f} +/- {X['bootstrap']['std']:.3f}")
    print(f"  separation D = {D:.2f} sigma | gap = {gap:.3f} | amp ratio = {ratio:.2f}")
    print(f"  PRE-REGISTERED VERDICT: {verdict}")
    print(f"  {why}")
    print("=" * 78)

    dst = os.path.join(HERE, f"channel_test_n{n}_results.json")
    json.dump(out, open(dst, "w"), indent=2, default=float)
    print(f"\nwrote {dst}   ({time.time()-t0:.0f}s total)")
    return out


if __name__ == "__main__":
    try:
        main()
    except GateFailure as e:
        print()
        print("!! RUN VOID -- " + str(e))
        sys.exit(2)
