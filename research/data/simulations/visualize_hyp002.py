"""
Visualization Agent — HYP-2026-002 Holographic Force Comparison
================================================================
Produces three plots:
  1. V(delta_rho): quantum circuit vs classical ED vs AdS analytical prediction
  2. Residuals (sigma) from analytical prediction
  3. Circuit resource analysis (depth, gate counts, H2 feasibility)

Output: research/data/simulations/SIM-2026-001_comparison.png
        research/data/simulations/SIM-2026-001_circuit_analysis.png

SIM: SIM-2026-001
Author: Computation Lead / visualization-agent
Date: 2026-03-10
"""

import numpy as np
import matplotlib
matplotlib.use("Agg")   # headless render
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import json

# ── Data from specialist runs ────────────────────────────────────────────────
L_ADS = 1.0 / np.log(2)   # 1.4427
C1_PAPER = 0.080
C2_PAPER = 13.6
C1_ERR = 0.008
C2_ERR = 0.8

# Analytical prediction (fine grid)
dr_fine = np.linspace(0.5, 9.0, 200)
V_analytical_fine = C1_PAPER - C2_PAPER * np.exp(-dr_fine / L_ADS)

# Integer separations for comparison
DR_INT = np.arange(1, 9, dtype=float)
V_analytical_int = C1_PAPER - C2_PAPER * np.exp(-DR_INT / L_ADS)

# Quantum circuit results (16-qubit MERA, Ry hologrons, statevector sim)
# Values from mera_corrected_run.py execution
QC_SEPS = [1, 2, 3, 4, 5, 6, 7, 8]
QC_V = [
    -0.08400795833165552,
     0.07152002680675953,
     0.16662176884870974,
     0.080385519988777,
     0.0,   # causal cone limit — circuit has no entanglement beyond dr=4
     0.0,
     0.0,
     0.0,
]
QC_ERROR = [0.03125] * 8   # 1/sqrt(1024) shot noise

# Classical ED results (20-site critical Ising, eigsh)
# Raw connected correlators from classical_baseline_hyp002.py
ED_SEPS  = [1, 2, 3, 4, 5, 6, 7, 8]
ED_RAW_C = [
    0.6069560401265943,
    0.49256266531516246,
    0.4270691989891311,
    0.3811056488319524,
    0.3453828137314715,
    0.3157599998601303,
    0.28997979294724885,
    0.26660771582805975,
]
# ED fitted values using holographic model (xi=3.23, not 1.44 — disagreement noted)
ED_FITTED_C1  =  0.23199256900886708
ED_FITTED_C2  = -0.5030008390805493
ED_FITTED_XI  =  3.2294272515537323

# Circuit resource data
CIRCUIT_METRICS = {
    "n_qubits":     16,
    "depth":        15,
    "cx_count":     29,
    "u_count":      74,
    "total_gates": 103,
    "n_params":    146,
    "h2_capacity_qubits":       56,
    "h2_logical_qubits":        12,
    "h2_fidelity_per_cx":    0.998,
    "h2_cx_error_budget_pct":  5.64,
    "h2_qv":               33500000,
}
SCALE_TARGETS = {
    "16q (PoC)":   {"cx": 29,  "depth": 15,  "error_pct": 5.6},
    "24q (full)":  {"cx": 72,  "depth": 36,  "error_pct": 13.3},
    "32q (ext.)":  {"cx": 144, "depth": 60,  "error_pct": 24.8},
}


# ── Color scheme ─────────────────────────────────────────────────────────────
COLOR_ANALYTIC = "#e63946"   # red
COLOR_QC       = "#2196F3"   # blue
COLOR_ED       = "#4CAF50"   # green
COLOR_CAUSAL   = "#FF9800"   # orange
COLOR_FADED    = "#CCCCCC"
BG             = "#0d1117"
FG             = "#e6edf3"
GRID           = "#21262d"


def style_ax(ax, title=""):
    ax.set_facecolor(BG)
    ax.tick_params(colors=FG, labelsize=9)
    ax.spines["bottom"].set_color(GRID)
    ax.spines["left"].set_color(GRID)
    ax.spines["top"].set_visible(False)
    ax.spines["right"].set_visible(False)
    ax.xaxis.label.set_color(FG)
    ax.yaxis.label.set_color(FG)
    ax.title.set_color(FG)
    if title:
        ax.set_title(title, fontsize=10, pad=8)


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 1: Force profile comparison
# ═══════════════════════════════════════════════════════════════════════════
fig1 = plt.figure(figsize=(13, 9), facecolor=BG)
gs = gridspec.GridSpec(3, 2, figure=fig1, hspace=0.55, wspace=0.35,
                       left=0.09, right=0.97, top=0.93, bottom=0.08)

# ── Panel A: Full force profile ───────────────────────────────────────────
ax_main = fig1.add_subplot(gs[0:2, 0])
style_ax(ax_main, "Holographic Force Profile V(delta_rho)")

# Analytical curve
ax_main.plot(dr_fine, V_analytical_fine, color=COLOR_ANALYTIC, lw=2.0,
             label=f"AdS analytical: V = {C1_PAPER} - {C2_PAPER}·exp(-dr/{L_ADS:.3f})", zorder=5)

# Analytical ±1-sigma band (paper uncertainties propagated)
V_hi = (C1_PAPER + C1_ERR) - (C2_PAPER - C2_ERR) * np.exp(-dr_fine / L_ADS)
V_lo = (C1_PAPER - C1_ERR) - (C2_PAPER + C2_ERR) * np.exp(-dr_fine / L_ADS)
ax_main.fill_between(dr_fine, V_lo, V_hi, alpha=0.15, color=COLOR_ANALYTIC, label="Analytical 1-sigma")

# Classical ED raw correlator (normalized to same scale for shape comparison)
ed_arr = np.array(ED_RAW_C)
ax_main.scatter(ED_SEPS, ed_arr, color=COLOR_ED, s=55, zorder=6, marker="s",
                label=f"ED correlator C(r), 20-site Ising (raw scale)", edgecolors="white", lw=0.5)
# ED fitted curve
ed_curve = ED_FITTED_C1 - ED_FITTED_C2 * np.exp(-dr_fine / ED_FITTED_XI)
ax_main.plot(dr_fine, ed_curve, color=COLOR_ED, lw=1.4, ls="--",
             label=f"ED fit: xi={ED_FITTED_XI:.2f} (vs l_AdS={L_ADS:.2f})", alpha=0.8)

# Quantum circuit results — split into causal cone (signal) and beyond (zero)
qc_signal_x = [DR for DR, V in zip(QC_SEPS, QC_V) if abs(V) > 1e-10]
qc_signal_v = [V for V in QC_V if abs(V) > 1e-10]
qc_zero_x   = [DR for DR, V in zip(QC_SEPS, QC_V) if abs(V) <= 1e-10]
qc_zero_v   = [V for V in QC_V if abs(V) <= 1e-10]

ax_main.errorbar(qc_signal_x, qc_signal_v,
                 yerr=[QC_ERROR[i] for i, V in enumerate(QC_V) if abs(V) > 1e-10],
                 fmt="o", color=COLOR_QC, ms=7, lw=1.5, capsize=4, capthick=1.5, zorder=7,
                 label="MERA circuit (16q, Ry hologrons)")
if qc_zero_x:
    ax_main.scatter(qc_zero_x, [0]*len(qc_zero_x), color=COLOR_CAUSAL, s=50, marker="x",
                    lw=2, zorder=7, label="Causal cone boundary (V=0, beyond reach)")

# Causal cone boundary annotation
ax_main.axvline(x=4.5, color=COLOR_CAUSAL, lw=1.0, ls=":", alpha=0.7)
ax_main.text(4.65, -4.0, "Causal cone\nboundary\n(dr > 4)", color=COLOR_CAUSAL,
             fontsize=7.5, va="top")

ax_main.set_xlabel("Hologron separation delta_rho (lattice units)", fontsize=9)
ax_main.set_ylabel("Interaction potential V", fontsize=9)
ax_main.axhline(0, color=GRID, lw=0.8, ls="--")
ax_main.legend(fontsize=7, loc="lower right", facecolor="#161b22", edgecolor=GRID, labelcolor=FG)
ax_main.set_xlim(0.5, 9.0)
ax_main.grid(True, color=GRID, lw=0.5, alpha=0.6)

# ── Panel B: Residuals ────────────────────────────────────────────────────
ax_resid = fig1.add_subplot(gs[0, 1])
style_ax(ax_resid, "Residuals: QC vs Analytical (sigma)")

resid_signal = [(QC_V[i] - V_analytical_int[i]) / QC_ERROR[i]
                for i in range(len(QC_SEPS)) if abs(QC_V[i]) > 1e-10]
dr_signal = [QC_SEPS[i] for i in range(len(QC_SEPS)) if abs(QC_V[i]) > 1e-10]

colors_resid = [COLOR_QC if abs(r) < 50 else COLOR_ANALYTIC for r in resid_signal]
ax_resid.bar(dr_signal, resid_signal, color=colors_resid, width=0.7, alpha=0.85)
ax_resid.axhline(0, color=FG, lw=0.8)
ax_resid.axhline( 3, color=GRID, lw=0.7, ls="--", alpha=0.7)
ax_resid.axhline(-3, color=GRID, lw=0.7, ls="--", alpha=0.7)
ax_resid.set_xlabel("delta_rho", fontsize=9)
ax_resid.set_ylabel("(V_QC - V_analytic) / sigma", fontsize=8)
ax_resid.text(0.05, 0.92, "Large residuals indicate\npre-optimized MERA params\nnot yet converged to\ncritical Ising ground state",
              transform=ax_resid.transAxes, fontsize=7, color=FG, va="top",
              bbox=dict(facecolor="#21262d", edgecolor=GRID, boxstyle="round,pad=0.3"))
ax_resid.grid(True, color=GRID, lw=0.5, alpha=0.6)

# ── Panel C: ED correlator shape vs l_AdS ────────────────────────────────
ax_ed = fig1.add_subplot(gs[1, 1])
style_ax(ax_ed, "ED Correlation Decay vs AdS Prediction")

dr_arr = np.array(ED_SEPS, dtype=float)
ax_ed.semilogy(dr_arr, np.abs(ed_arr), "s-", color=COLOR_ED, ms=6,
               lw=1.4, label="|C(r)| ED (20-site Ising)", zorder=6)

# Exponential fits
r_plot = np.linspace(1, 9, 200)
exp_ads   = np.abs(C2_PAPER) * np.exp(-r_plot / L_ADS)
exp_ed    = np.abs(ED_FITTED_C2) * np.exp(-r_plot / ED_FITTED_XI)
ax_ed.semilogy(r_plot, exp_ads,  color=COLOR_ANALYTIC, lw=1.6, ls="--",
               label=f"AdS: exp(-r/{L_ADS:.3f})", alpha=0.85)
ax_ed.semilogy(r_plot, exp_ed,   color=COLOR_ED,      lw=1.3, ls=":",
               label=f"ED fit: exp(-r/{ED_FITTED_XI:.2f})", alpha=0.85)

ax_ed.set_xlabel("delta_rho", fontsize=9)
ax_ed.set_ylabel("|C(r)|  (log scale)", fontsize=8)
ax_ed.legend(fontsize=7, facecolor="#161b22", edgecolor=GRID, labelcolor=FG)
ax_ed.grid(True, color=GRID, lw=0.5, alpha=0.6, which="both")

# ── Panel D: Summary status ───────────────────────────────────────────────
ax_info = fig1.add_subplot(gs[2, :])
style_ax(ax_info)
ax_info.axis("off")

lines = [
    ("HYP-2026-002  |  Holographic Gravitational Force from MERA",
     14, FG, "bold"),
    ("Sahay, Lukin, Cotler (PRX 2026)  |  V(dr) = C1 - C2*exp(-dr/l_AdS)  |  C1=0.080(8), C2=13.6(8), l_AdS=1/ln(2)=1.4427",
     9, "#8b949e", "normal"),
    ("",
     5, FG, "normal"),
    ("CIRCUIT    16 qubits  |  depth 15  |  29 CX  |  103 gates  |  146 params  |  H2 error budget 5.64%",
     9, COLOR_QC, "normal"),
    ("FINDING 1  Rz hologrons give V=0 identically (commutes with ZZ). Ry hologrons required for non-zero signal.",
     9, COLOR_CAUSAL, "normal"),
    ("FINDING 2  MERA causal cone limits dr to <=4 at this depth (3 layers). Need >=5 layers for full 8-site sweep.",
     9, COLOR_CAUSAL, "normal"),
    ("FINDING 3  ED xi=3.23 vs theory l_AdS=1.44 (2.2x mismatch). Open boundary conditions and finite-size effects.",
     9, COLOR_ED, "normal"),
    ("VERDICT    Circuit is H2-feasible (16q of 56). Variational optimization of MERA params is required before hardware.",
     9, COLOR_ANALYTIC, "bold"),
]

y = 0.97
for text, size, color, weight in lines:
    ax_info.text(0.0, y, text, transform=ax_info.transAxes,
                 fontsize=size, color=color, fontweight=weight, va="top",
                 fontfamily="monospace" if "FINDING" in text or "CIRCUIT" in text or "VERDICT" in text else "sans-serif")
    y -= (size + 3) / 120.0

fig1.suptitle("SIM-2026-001 | MERA Holographic Force | HYP-2026-002",
              color=FG, fontsize=12, y=0.98, fontweight="bold")

out1 = "D:/quantum-worldline/research/data/simulations/SIM-2026-001_comparison.png"
fig1.savefig(out1, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {out1}")
plt.close(fig1)


# ═══════════════════════════════════════════════════════════════════════════
#  FIGURE 2: Circuit resource analysis
# ═══════════════════════════════════════════════════════════════════════════
fig2, axes = plt.subplots(1, 3, figsize=(13, 4.5), facecolor=BG)
fig2.suptitle("SIM-2026-001 | Circuit Resource Analysis for Quantinuum H2",
              color=FG, fontsize=11, y=1.01, fontweight="bold")

# Panel A: Gate composition breakdown
ax_gates = axes[0]
style_ax(ax_gates, "Gate Composition (16-qubit PoC)")
gate_labels = ["CX\n(entangling)", "Single-qubit U\n(rotations)"]
gate_counts = [29, 74]
gate_colors = [COLOR_QC, COLOR_ANALYTIC]
bars = ax_gates.bar(gate_labels, gate_counts, color=gate_colors, width=0.5,
                    edgecolor=GRID, linewidth=0.8)
for bar, count in zip(bars, gate_counts):
    ax_gates.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 1.5,
                  str(count), ha="center", va="bottom", color=FG, fontsize=10, fontweight="bold")
ax_gates.set_ylabel("Gate count", fontsize=9)
ax_gates.set_ylim(0, 95)
ax_gates.axhline(74, color=COLOR_ANALYTIC, lw=0.7, ls="--", alpha=0.4)
ax_gates.text(1.5, 76, f"Total: 103", color=FG, fontsize=8)
ax_gates.grid(True, color=GRID, lw=0.5, alpha=0.5, axis="y")

# Panel B: Scaling to larger systems
ax_scale = axes[1]
style_ax(ax_scale, "CX Count vs Qubit Count (MERA scaling)")
q_sizes = np.array([16, 24, 32, 48, 56])

def cx_estimate(nq):
    # binary MERA: ~1.8*nq CX gates for 3 layers; scales roughly linearly
    return int(1.8 * nq + 0.5)

cx_est = [cx_estimate(q) for q in q_sizes]
h2_limit_cx = -np.log(0.01) / np.log(1 / 0.998)  # ~229 CX for 1% fidelity floor
ax_scale.plot(q_sizes, cx_est, "o-", color=COLOR_QC, ms=8, lw=2, label="Estimated CX count")
ax_scale.axhline(h2_limit_cx, color=COLOR_ANALYTIC, lw=1.4, ls="--",
                 label=f"H2 1%-fidelity floor (~{int(h2_limit_cx)} CX)")
ax_scale.axvline(56, color=COLOR_CAUSAL, lw=1.0, ls=":", alpha=0.8, label="H2 qubit limit (56)")
ax_scale.fill_between(q_sizes, cx_est, h2_limit_cx, where=np.array(cx_est) < h2_limit_cx,
                      alpha=0.12, color=COLOR_ED, label="H2 feasible region")
ax_scale.set_xlabel("Qubit count", fontsize=9)
ax_scale.set_ylabel("CX gate count", fontsize=9)
ax_scale.legend(fontsize=7, facecolor="#161b22", edgecolor=GRID, labelcolor=FG)
ax_scale.grid(True, color=GRID, lw=0.5, alpha=0.5)

# Mark current PoC
ax_scale.annotate("This PoC\n(16q, 29 CX)", xy=(16, cx_estimate(16)),
                  xytext=(20, 40), fontsize=7.5, color=FG,
                  arrowprops=dict(arrowstyle="->", color=FG, lw=1.0))

# Panel C: Error budget pyramid
ax_err = axes[2]
style_ax(ax_err, "H2 Error Budget by System Size")
labels_err = ["16q PoC\n(29 CX)", "24q Full\n(~43 CX)", "32q Extended\n(~58 CX)", "56q (H2 max)\n(~101 CX)"]
cx_counts   = [29, 43, 58, 101]
err_pct     = [round((1 - 0.998 ** n) * 100, 2) for n in cx_counts]
bar_colors  = [COLOR_ED if e < 10 else (COLOR_CAUSAL if e < 20 else COLOR_ANALYTIC) for e in err_pct]

bars2 = ax_err.bar(labels_err, err_pct, color=bar_colors, width=0.55, edgecolor=GRID, linewidth=0.7)
for bar, val in zip(bars2, err_pct):
    ax_err.text(bar.get_x() + bar.get_width() / 2, bar.get_height() + 0.3,
                f"{val:.1f}%", ha="center", va="bottom", color=FG, fontsize=9, fontweight="bold")

ax_err.axhline(10, color=COLOR_CAUSAL, lw=1.0, ls="--", alpha=0.8, label="10% threshold")
ax_err.axhline(5,  color=COLOR_ED,     lw=0.8, ls=":", alpha=0.8, label="5% target")
ax_err.set_ylabel("Accumulated gate error (%)", fontsize=9)
ax_err.set_ylim(0, 25)
ax_err.legend(fontsize=7.5, facecolor="#161b22", edgecolor=GRID, labelcolor=FG)
ax_err.grid(True, color=GRID, lw=0.5, alpha=0.5, axis="y")

plt.tight_layout(pad=1.4)
out2 = "D:/quantum-worldline/research/data/simulations/SIM-2026-001_circuit_analysis.png"
fig2.savefig(out2, dpi=150, bbox_inches="tight", facecolor=BG)
print(f"Saved: {out2}")
plt.close(fig2)

print("Visualization complete.")
print(f"  Plot 1: {out1}")
print(f"  Plot 2: {out2}")
