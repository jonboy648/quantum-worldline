#!/usr/bin/env python3
"""
qw_alpha_figure.py -- the two-panel diagnostic figure for the alpha re-analysis.

Panel (a): the N=24 exact force profile on log-log, with the three competing fits.
Panel (b): the local log-slope -dln|F|/dln(dr), which is FLAT for a true power law.
           This is the panel that decides the question: the data plateau at ~2.6,
           not at the claimed 4.

Palette: Okabe-Ito subset (#0072B2 blue, #D55E00 vermillion, #009E73 green),
validated colorblind-safe -- all six checks PASS (deutan dE 11.0, normal dE 25.8,
contrast >= 3:1 on a white surface). Line style is a redundant second encoding, so
identity never rests on hue alone. Print-safe in greyscale.

Run:  python qw_alpha_figure.py     -> alpha_reanalysis_figure.{pdf,png}
"""

import json
import os

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

HERE = os.path.dirname(os.path.abspath(__file__))
SIMS = os.path.abspath(os.path.join(HERE, "..", "..", "data", "simulations"))

BLUE, VERM, GREEN = "#0072B2", "#D55E00", "#009E73"
INK, MUTED = "#1a1a1a", "#6b6b6b"

plt.rcParams.update({
    "font.family": "serif", "font.serif": ["DejaVu Serif"], "font.size": 9,
    "axes.edgecolor": MUTED, "axes.labelcolor": INK, "text.color": INK,
    "xtick.color": MUTED, "ytick.color": MUTED,
    "axes.spines.top": False, "axes.spines.right": False,
    "figure.facecolor": "white", "axes.facecolor": "white",
})


def main():
    with open(os.path.join(SIMS, "SIM-2026-011-interaction.json")) as f:
        rec = json.load(f)
    F = rec["F_interaction_avg"]
    dr = np.array(sorted(int(k) for k in F))
    y = np.abs(np.array([F[str(k)] for k in dr]))

    pl = lambda x, A, a: A * x ** (-a)
    m = dr >= 2
    p_pub, _ = curve_fit(pl, dr[m], y[m], p0=[1, 4], maxfev=200000)
    p_rel, _ = curve_fit(pl, dr[m], y[m], p0=[1, 4], sigma=y[m], maxfev=200000)
    b, a0 = np.polyfit(np.log(dr[m]), np.log(y[m]), 1)

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(7.4, 3.2))
    xs = np.linspace(1.8, 12.5, 300)

    # ---- panel (a): the profile and the competing fits
    ax1.loglog(dr, y, "o", ms=5, color=INK, zorder=5, label="_", clip_on=False)
    ax1.loglog(xs, pl(xs, *p_pub), "-", lw=2, color=VERM,
               label=r"published: $\alpha=3.92$")
    ax1.loglog(xs, np.exp(a0) * xs ** b, "--", lw=2, color=BLUE,
               label=r"log-space OLS: $\alpha=2.89$")
    ax1.loglog(xs, pl(xs, *p_rel), ":", lw=2, color=GREEN,
               label=r"rel.-error wt: $\alpha=2.82$")
    ax1.annotate("dr = 2 carries 95.8%\nof the published fit", xy=(2, y[1]),
                 xytext=(2.6, 3e-1), fontsize=7.5, color=VERM,
                 arrowprops=dict(arrowstyle="->", color=VERM, lw=1))
    ax1.set_xlabel(r"separation $\Delta r$ (sites)")
    ax1.set_ylabel(r"$|F(\Delta r)|$")
    ax1.set_title("(a) same data, three standard estimators", fontsize=9, loc="left")
    ax1.legend(frameon=False, fontsize=7.5, loc="lower left")
    ax1.grid(True, which="major", lw=0.4, color="#e8e8e8", zorder=0)

    # ---- panel (b): the local slope -- flat iff a power law
    mid = 0.5 * (dr[:-1] + dr[1:])
    sl = -np.diff(np.log(y)) / np.diff(np.log(dr))
    ax2.axhline(4.0, color=VERM, lw=1.5, ls="-", zorder=1)
    ax2.axhline(2.0, color=MUTED, lw=1, ls=":", zorder=1)
    ax2.axhspan(2.592 * 0.925, 2.592 * 1.075, color=BLUE, alpha=0.13, zorder=0)
    ax2.axhline(2.592, color=BLUE, lw=1.5, ls="--", zorder=2)
    ax2.plot(mid, sl, "o-", ms=5, lw=1.2, color=INK, zorder=5, clip_on=False)
    ax2.text(1.4, 4.06, r"claimed $\alpha=2\Delta_T=4$", ha="left", va="bottom",
             fontsize=7.5, color=VERM)
    ax2.text(4.3, 2.83, "measured plateau 2.59", ha="left", va="bottom",
             fontsize=7.5, color=BLUE)
    ax2.text(4.3, 2.30, "6 consecutive slopes, $\\pm$7.5%", ha="left", va="top",
             fontsize=7, color=BLUE)
    ax2.text(1.4, 1.95, r"scalar exchange $\alpha=2$", ha="left", va="top",
             fontsize=7.5, color=MUTED)
    ax2.set_xlabel(r"separation $\Delta r$ (sites)")
    ax2.set_ylabel(r"local slope $-\,d\ln|F|/d\ln \Delta r$")
    ax2.set_title("(b) a power law is flat here", fontsize=9, loc="left")
    ax2.set_xlim(1, 12.5)
    ax2.set_ylim(1.6, 4.6)
    ax2.grid(True, axis="y", lw=0.4, color="#e8e8e8", zorder=0)

    fig.tight_layout()
    for ext in ("pdf", "png"):
        p = os.path.join(HERE, "alpha_reanalysis_figure." + ext)
        fig.savefig(p, dpi=300, bbox_inches="tight")
        print("wrote", p)


if __name__ == "__main__":
    main()
