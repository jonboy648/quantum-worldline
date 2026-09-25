"""
Figure 8: Null control -- holographic vs non-holographic finite-T transport amplitude
(SIM-2026-028, supporting HYP-2026-024 / SIM-2026-027).

Two panels:
  (a) Normalized A(beta)/A(cold) for the holographic (Wang-He critical Ising) boundary
      vs the non-holographic gapped paramagnet control. The control stays near 1 until
      its (large) gap is thermally bridged; the holographic case degrades earlier and
      further.
  (b) WASHOUT-NORMALIZED A(beta)/sqrt(purity), normalized to cold. The control is FLAT
      (~1.0): its amplitude drop is entirely generic decoherence. The holographic case
      is STRUCTURED: residual degradation beyond purity loss = candidate horizon signal.

Consumes SIM-2026-028.json. Saves figure8_null_control.png/pdf.
"""
import json
import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

JSON_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-028.json"


def main():
    with open(JSON_PATH) as f:
        sim = json.load(f)
    res = sim["results"]
    c = res["normalized_curves"]
    beta = np.array(c["beta"])
    holo = np.array(c["holo_A_norm"])
    ctrl = np.array(c["control_A_norm"])
    holo_wn = np.array(c["holo_A_washout_norm"])
    ctrl_wn = np.array(c["control_A_washout_norm"])

    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

    ax1.semilogx(beta, holo, "o-", color="#1f77b4", lw=2, ms=7,
                 label="holographic (critical Ising)")
    ax1.semilogx(beta, ctrl, "s--", color="#ff7f0e", lw=2, ms=7,
                 label="control (gapped paramagnet)")
    ax1.set_xlabel(r"inverse temperature $\beta$")
    ax1.set_ylabel(r"normalized transport amplitude $A(\beta)/A_{\rm cold}$")
    ax1.set_title("(a) Raw amplitude degradation\nboth fall, but the control lags (large gap)",
                  fontsize=10)
    ax1.legend(fontsize=9, loc="upper left")
    ax1.grid(alpha=0.3)

    ax2.semilogx(beta, holo_wn, "o-", color="#1f77b4", lw=2, ms=7,
                 label="holographic")
    ax2.semilogx(beta, ctrl_wn, "s--", color="#ff7f0e", lw=2, ms=7,
                 label="control")
    ax2.axhline(1.0, ls=":", color="gray", alpha=0.7, label="pure washout (=1)")
    ax2.set_xlabel(r"inverse temperature $\beta$")
    ax2.set_ylabel(r"washout-normalized $A(\beta)/\sqrt{\rm purity}$ (norm.)")
    gapw = res.get("max_gap_washout_normalized")
    ax2.set_title(f"(b) Washout-normalized: control FLAT, holographic STRUCTURED\n"
                  f"max gap = {gapw*100:.0f}%  ->  signal beyond washout", fontsize=10)
    ax2.legend(fontsize=9, loc="upper left")
    ax2.grid(alpha=0.3)
    ax2.annotate("control = pure\nthermal washout", xy=(8, 1.0), xytext=(2, 1.5),
                 fontsize=8, color="#ff7f0e",
                 arrowprops=dict(arrowstyle="->", color="#ff7f0e", alpha=0.6))
    ax2.annotate("holographic: residual\ndegradation (candidate horizon)",
                 xy=(0.5, holo_wn[np.argmin(np.abs(beta - 0.5))]), xytext=(0.3, 0.4),
                 fontsize=8, color="#1f77b4",
                 arrowprops=dict(arrowstyle="->", color="#1f77b4", alpha=0.6))

    verdict = res.get("verdict", "")
    fig.suptitle(f"SIM-2026-028 null control (L=8): holographic vs non-holographic "
                 f"finite-T transport -- {verdict}", fontsize=11, y=1.02)
    fig.tight_layout()
    for ext in ("png", "pdf"):
        fig.savefig(f"D:/quantum-worldline/research/data/simulations/figure8_null_control.{ext}",
                    dpi=150, bbox_inches="tight")
    print("Saved figure8_null_control.png/pdf")
    print(f"Verdict: {verdict}")


if __name__ == "__main__":
    main()
