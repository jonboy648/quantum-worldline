#!/usr/bin/env python3
"""
qw_alpha_reanalysis.py -- fit-window x weighting re-analysis of the force exponent alpha.

WHY THIS EXISTS
---------------
The submitted PRD manuscript (accession DV13971) reports alpha = 3.92 +/- 0.16 as "the central
finding of this work", from an unweighted least-squares fit of F(dr) = A*dr^(-alpha) in LINEAR
space over dr >= 2. The 2026-08-17 audit (docs/governance/AUDIT-2026-08-11.md, D-2/D-3) found
that fit is dominated by a single point. This script settles the question from the raw records,
reproducibly, with no free choices hidden.

It answers exactly three questions:
  Q1  How much does alpha depend on the fit window and the error model?
  Q2  Is there a power-law plateau in the data at all (local log-slope constant over a range)?
  Q3  What is the honest uncertainty, and what does it do to the "alpha = 2 is excluded" claim?

DATA (raw, from the project's own records -- nothing re-simulated):
  D1  N=24 exact diagonalization    research/data/simulations/SIM-2026-011-interaction.json
                                    .F_interaction_avg              (dr = 1..12)
  D2  N=16 exact diagonalization    research/data/simulations/SIM-2026-015d.json .exact.V_data
  D3  N=16 chi=3 MERA               research/data/simulations/SIM-2026-015d.json .mera.V_data
The manuscript presents D1/D2/D3 as three consistent evaluations.

USAGE
  python qw_alpha_reanalysis.py            # writes JSON + figure next to this script
"""

import json
import os

import numpy as np
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
REPO = os.path.abspath(os.path.join(HERE, "..", "..", ".."))
SIMS = os.path.join(REPO, "research", "data", "simulations")
RNG_SEED = 20260817          # fixed: every bootstrap number here is reproducible


# --------------------------------------------------------------------------- data
def load():
    with open(os.path.join(SIMS, "SIM-2026-011-interaction.json")) as f:
        d11 = json.load(f)
    with open(os.path.join(SIMS, "SIM-2026-015d.json")) as f:
        d15 = json.load(f)

    def arr(dct):
        k = np.array(sorted(int(x) for x in dct))
        return k, np.array([dct[str(i)] for i in k], dtype=float)

    out = {}
    out["D1_N24_exact"] = arr(d11["F_interaction_avg"])
    out["D2_N16_exact"] = arr(d15["exact"]["V_data"])
    out["D3_N16_mera_chi3"] = arr(d15["mera"]["V_data"])
    published = {
        "D1_N24_exact": (d11["fits"]["F_avg_dr_ge2"]["power_law"]["alpha"],
                         d11["fits"]["F_avg_dr_ge2"]["power_law"]["dalpha"]),
        "D2_N16_exact": (d15["exact"]["alpha"], d15["exact"]["dalpha"]),
        "D3_N16_mera_chi3": (d15["mera"]["alpha"], d15["mera"]["dalpha"]),
    }
    return out, published


# ----------------------------------------------------------------------- estimators
def pl(x, A, a):
    return A * x ** (-a)


def fit_linear_unweighted(x, y):
    """The PUBLISHED estimator: NLS on F itself, uniform absolute errors."""
    p, c = curve_fit(pl, x, y, p0=[abs(y[0]) * x[0] ** 4, 4.0], maxfev=200000)
    return p[1], float(np.sqrt(np.diag(c))[1])


def fit_linear_relerr(x, y):
    """NLS on F with errors proportional to |F| -- i.e. every point matters equally
    in RELATIVE terms. Discards nothing; only changes the error model."""
    p, c = curve_fit(pl, x, y, p0=[abs(y[0]) * x[0] ** 4, 4.0],
                     sigma=np.abs(y), absolute_sigma=False, maxfev=200000)
    return p[1], float(np.sqrt(np.diag(c))[1])


def fit_log_ols(x, y):
    """Ordinary least squares on log|F| vs log dr -- the textbook power-law estimator."""
    lx, ly = np.log(x), np.log(np.abs(y))
    n = len(lx)
    b, a = np.polyfit(lx, ly, 1)
    resid = ly - (b * lx + a)
    s2 = resid @ resid / max(n - 2, 1)
    se = float(np.sqrt(s2 / ((lx - lx.mean()) ** 2).sum())) if n > 2 else float("nan")
    return -b, se


ESTIMATORS = {
    "linear_unweighted_PUBLISHED": fit_linear_unweighted,
    "linear_relative_error": fit_linear_relerr,
    "log_space_OLS": fit_log_ols,
}


# ------------------------------------------------------------------------ diagnostics
def leverage(x, y):
    """Share of the unweighted least-squares objective carried by each point.
    For NLS on F with uniform sigma the objective is sum of residuals^2, and the
    scale of each residual is set by |F| itself -- so |F|^2 / sum |F|^2 is the
    fraction of the fit's 'attention' a point receives."""
    w = y ** 2
    return w / w.sum()


def local_slopes(x, y):
    """Point-to-point log-slope: -dln|F| / dln dr. A true power law is FLAT here."""
    lx, ly = np.log(x), np.log(np.abs(y))
    return 0.5 * (x[:-1] + x[1:]), -np.diff(ly) / np.diff(lx)


def plateau_scan(mid, sl, tol=0.15):
    """Longest run of consecutive local slopes whose spread is within tol (relative).
    Returns (length, start_index, mean). A genuine power law over a decade should
    give a long run; a curved profile gives short ones."""
    best = (0, -1, float("nan"))
    for i in range(len(sl)):
        for j in range(i + 2, len(sl) + 1):
            seg = sl[i:j]
            if (seg.max() - seg.min()) / abs(seg.mean()) <= tol:
                if j - i > best[0]:
                    best = (j - i, i, float(seg.mean()))
    return best


def bootstrap(x, y, est, n=2000, seed=RNG_SEED):
    """Residual-free, nonparametric: resample the (dr, F) pairs with replacement."""
    rng = np.random.default_rng(seed)
    vals = []
    idx = np.arange(len(x))
    for _ in range(n):
        s = rng.choice(idx, size=len(idx), replace=True)
        if len(np.unique(s)) < 3:
            continue
        o = np.argsort(x[s])
        try:
            a, _ = est(x[s][o], y[s][o])
            if np.isfinite(a) and 0 < a < 20:
                vals.append(a)
        except Exception:
            continue
    v = np.array(vals)
    return dict(n=int(v.size), mean=float(v.mean()), std=float(v.std(ddof=1)),
                median=float(np.median(v)),
                ci_lo=float(np.percentile(v, 2.5)), ci_hi=float(np.percentile(v, 97.5)))


# ----------------------------------------------------------------------------- main
def main():
    data, published = load()
    results = {
        "generated": "2026-08-17",
        "purpose": "fit-window x weighting re-analysis of alpha; audit D-2/D-3",
        "rng_seed": RNG_SEED,
        "datasets": {},
    }

    for name, (x, y) in data.items():
        ds = {"published_alpha": published[name][0], "published_dalpha": published[name][1]}

        # sign audit -- a power law cannot change sign; log fits are invalid past a flip
        sgn = np.sign(y)
        flips = [int(x[i]) for i in range(len(y)) if sgn[i] != sgn[0]]
        ds["sign_flips_at_dr"] = flips
        valid_max = min(flips) - 1 if flips else int(x.max())
        ds["max_dr_before_sign_flip"] = valid_max

        m2 = x >= 2
        ds["leverage_dr_ge2"] = {int(k): float(v) for k, v in zip(x[m2], leverage(x[m2], y[m2]))}
        ds["leverage_of_dr2"] = ds["leverage_dr_ge2"][2]

        mid, sl = local_slopes(x, y)
        ds["local_slopes"] = [{"dr_mid": float(a), "slope": float(b)} for a, b in zip(mid, sl)]
        sl_ok = sl[mid <= valid_max]
        L, i0, mval = plateau_scan(mid[mid <= valid_max], sl_ok)
        ds["plateau"] = {"longest_flat_run_points": int(L), "mean_slope_in_run": mval,
                         "tolerance_rel": 0.15,
                         "note": "a genuine power law is FLAT here; run length counts slopes, not data points"}

        # the matrix
        matrix = {}
        for est_name, est in ESTIMATORS.items():
            row = {}
            for dmin in range(2, 7):
                mask = (x >= dmin) & (x <= valid_max)
                if mask.sum() < 3:
                    continue
                try:
                    a, da = est(x[mask], y[mask])
                    row["dr_ge_%d" % dmin] = {"alpha": float(a), "sigma_fit": float(da),
                                              "n_pts": int(mask.sum())}
                except Exception as e:
                    row["dr_ge_%d" % dmin] = {"error": str(e)}
            matrix[est_name] = row
        ds["window_weighting_matrix"] = matrix

        # honest uncertainty on the published window, per estimator
        mask = (x >= 2) & (x <= valid_max)
        ds["bootstrap_dr_ge2"] = {k: bootstrap(x[mask], y[mask], e)
                                  for k, e in ESTIMATORS.items()}

        allv = [c["alpha"] for r in matrix.values() for c in r.values() if "alpha" in c]
        ds["alpha_spread_over_all_choices"] = {"min": float(min(allv)), "max": float(max(allv)),
                                               "n_choices": len(allv)}
        results["datasets"][name] = ds

    out = os.path.join(HERE, "alpha_reanalysis_results.json")
    with open(out, "w") as f:
        json.dump(results, f, indent=2)
    print("wrote", out)

    # ------------------------------------------------------------------ console table
    for name, ds in results["datasets"].items():
        print("\n" + "=" * 78)
        print("%s   published alpha = %.4f +/- %.4f" %
              (name, ds["published_alpha"], ds["published_dalpha"]))
        if ds["sign_flips_at_dr"]:
            print("  !! SIGN FLIPS at dr = %s -- power law undefined beyond dr=%d"
                  % (ds["sign_flips_at_dr"], ds["max_dr_before_sign_flip"]))
        print("  leverage of the single point dr=2 : %.1f%% of the fit objective"
              % (100 * ds["leverage_of_dr2"]))
        print("  longest flat run in local slope    : %d slopes (mean %.3f) at 15%% tolerance"
              % (ds["plateau"]["longest_flat_run_points"], ds["plateau"]["mean_slope_in_run"]))
        print("  %-30s %s" % ("estimator \ window",
                              "  ".join("dr>=%d" % d for d in range(2, 7))))
        for est, row in ds["window_weighting_matrix"].items():
            cells = []
            for d in range(2, 7):
                c = row.get("dr_ge_%d" % d)
                cells.append("%6.3f" % c["alpha"] if c and "alpha" in c else "     -")
            print("  %-30s %s" % (est, "  ".join(cells)))
        b = ds["bootstrap_dr_ge2"]["linear_unweighted_PUBLISHED"]
        print("  bootstrap (published estimator)    : mean %.3f  sigma %.3f  95%% CI [%.2f, %.2f]"
              % (b["mean"], b["std"], b["ci_lo"], b["ci_hi"]))
        s = ds["alpha_spread_over_all_choices"]
        print("  ALPHA SPREAD over %d defensible choices: %.3f .. %.3f"
              % (s["n_choices"], s["min"], s["max"]))
    return results


if __name__ == "__main__":
    main()
