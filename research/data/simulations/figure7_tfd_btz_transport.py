"""
Figure 7: Finite-temperature BTZ transport via Thermofield Double (SIM-2026-027, HYP-2026-024).

Two-panel publication figure:
  (a) Transport response amplitude A(beta) vs beta  -- PRIMARY observable.
      Wang-He horizon absorption predicts monotonic decrease as T rises (beta falls).
      Overlaid with participation ratio N_eff (thermal mixing) on a twin axis.
  (b) Transport time T(beta) vs beta (SECONDARY, finite-size caveated) + Gamma(beta)
      vs the pre-committed 2*pi/beta BTZ-QNM prediction (inset or twin axis).

Consumes research/data/simulations/SIM-2026-027.json. Saves figure7_tfd_btz_transport.png/pdf.
Run AFTER the simulation completes.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JSON_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-027.json"


def main():
    with open(JSON_PATH) as f:
        sim = json.load(f)
    res = sim["results"]
    ladder = res["beta_ladder_L8"]

    betas = np.array([r["beta"] for r in ladder])
    A_int = np.array([r["A_integrated_global"] for r in ladder])
    A_pk = np.array([r["A_peak_global"] for r in ladder])
    Neff = np.array([r["participation_ratio"] for r in ladder])
    Ts = np.array([r["transport_time"] for r in ladder])
    order = np.argsort(betas)
    betas, A_int, A_pk, Neff, Ts = (a[order] for a in (betas, A_int, A_pk, Neff, Ts))

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    # ── (a) Amplitude A(beta): primary horizon-absorption signal ──
    ax1.semilogx(betas, A_int / A_int.max(), "o-", color="#1f77b4",
                 label="integrated $A(\\beta)$ (norm.)", lw=2, ms=7)
    ax1.semilogx(betas, A_pk / A_pk.max(), "s--", color="#2ca02c",
                 label="peak $A(\\beta)$ (norm.)", lw=1.5, ms=6, alpha=0.8)
    ax1.set_xlabel(r"inverse temperature $\beta$")
    ax1.set_ylabel("normalized transport response $A(\\beta)$")
    amp = res.get("amplitude_analysis", {})
    rho = amp.get("spearman_beta_vs_Aint")
    deg = amp.get("A_fractional_degradation_cold_to_hot")
    title_a = "(a) Transport amplitude vs temperature"
    if rho is not None and deg is not None:
        title_a += f"\nSpearman$(\\beta,A)$={rho:.2f}, degradation={deg*100:.0f}%"
    ax1.set_title(title_a, fontsize=10)
    axt = ax1.twinx()
    axt.semilogx(betas, Neff, "^:", color="#d62728", alpha=0.5,
                 label="$N_{eff}$ (thermal mixing)")
    axt.set_ylabel("$N_{eff}$", color="#d62728")
    axt.tick_params(axis="y", labelcolor="#d62728")
    l1, lab1 = ax1.get_legend_handles_labels()
    l2, lab2 = axt.get_legend_handles_labels()
    ax1.legend(l1 + l2, lab1 + lab2, fontsize=8, loc="center left")
    ax1.annotate("hot\n(horizon absorbs)", xy=(betas.min(), 0.1),
                 fontsize=8, ha="left", color="gray")
    ax1.annotate("cold (AdS)", xy=(betas.max(), 0.95), fontsize=8, ha="right", color="gray")

    # ── (b) Transport time T(beta) (secondary) + Gamma scaling ──
    valid = Ts > 0
    ax2.semilogx(betas[valid], Ts[valid], "o-", color="#9467bd",
                 label="$T(\\beta)$ (transport time)", lw=2, ms=7)
    anchor = res.get("T_anchor_beta_inf")
    if anchor:
        ax2.axhline(anchor, ls=":", color="gray", alpha=0.6,
                    label=f"$\\beta\\!\\to\\!\\infty$ anchor T={anchor:.2f}")
    ax2.set_xlabel(r"inverse temperature $\beta$")
    ax2.set_ylabel("transport time $T(\\beta)$")
    sc = res.get("secondary_time_curve", "")
    ax2.set_title(f"(b) Transport time (secondary)\ntime-curve: {sc}", fontsize=10)

    # Gamma(beta) inset
    gpts = res.get("gamma_scaling", {}).get("valid_points", [])
    if gpts:
        axin = ax2.inset_axes([0.55, 0.55, 0.4, 0.4])
        bg = np.array([p[0] for p in gpts]); gg = np.array([p[1] for p in gpts])
        axin.loglog(bg, gg, "ko", ms=5, label="$\\Gamma$ meas.")
        bb = np.logspace(np.log10(bg.min()), np.log10(bg.max()), 50)
        axin.loglog(bb, 2 * np.pi / bb, "r-", lw=1, label="$2\\pi/\\beta$")
        axin.set_title("$\\Gamma(\\beta)$ vs BTZ-QNM", fontsize=7)
        axin.tick_params(labelsize=6)
        axin.legend(fontsize=6)
    ax2.legend(fontsize=8, loc="lower right")

    verdict = res.get("verdict", "")
    fig.suptitle(f"SIM-2026-027: Finite-T holographic transport via Thermofield Double "
                 f"(L=8) -- verdict: {verdict}", fontsize=11, y=1.02)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(f"D:/quantum-worldline/research/data/simulations/figure7_tfd_btz_transport.{ext}",
                    dpi=150, bbox_inches="tight")
    print("Saved figure7_tfd_btz_transport.png/pdf")
    print(f"Verdict: {verdict}")
    print(f"Reason: {res.get('verdict_reason','')}")


if __name__ == "__main__":
    main()
