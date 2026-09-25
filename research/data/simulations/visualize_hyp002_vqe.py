"""
Visualization — HYP-2026-002 VQE Results (SIM-2026-002)
========================================================
Visualization Agent specialist output for Computation Lead.

Reads SIM-2026-002.json and classical_baseline_SIM2026002.json,
produces three plots:

  1. VQE energy convergence curve
     - x: function evaluation number
     - y: Ising energy expectation value
     - Marks: initial, final, exact E0, 1% threshold

  2. Holographic force profile V(delta_rho)
     - Quantum MERA (post-VQE)
     - Classical ED baseline (PBC, N=16)
     - Analytical AdS prediction V = C1 - C2*exp(-dr/l_AdS)
     - Fitted curve from MERA data

  3. Parameter landscape: pre vs post optimization
     - Histogram of theta values before and after VQE

Author: visualization-agent (Computation Lead dispatch)
Date:   2026-03-10
SIM:    SIM-2026-002
"""

import json
import numpy as np
import matplotlib
matplotlib.use('Agg')   # headless rendering
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.patches import FancyArrowPatch
import os

# ─── Load data ────────────────────────────────────────────────────────────────
SIM_PATH      = "D:/quantum-worldline/research/data/simulations/SIM-2026-002.json"
CLASSICAL_PATH = "D:/quantum-worldline/research/data/simulations/classical_baseline_SIM2026002.json"
PLOT_DIR       = "D:/quantum-worldline/research/data/simulations/"

L_ADS   = 1.0 / np.log(2)
C1_PAPER = 0.080
C2_PAPER = 13.6

COLORS = {
    "quantum":    "#2D7DD2",   # blue
    "classical":  "#E84855",   # red
    "analytical": "#3BB273",   # green
    "fitted":     "#F4A261",   # orange
    "threshold":  "#A8DADC",   # light cyan
    "e0_line":    "#1B1B2F",   # near-black
}


def load_data():
    with open(SIM_PATH)      as f: sim      = json.load(f)
    with open(CLASSICAL_PATH) as f: classical = json.load(f)
    return sim, classical


def plot_vqe_convergence(sim: dict, ax: plt.Axes):
    """Plot VQE energy vs function evaluation."""
    vqe       = sim["vqe"]
    history   = vqe["energy_history"]
    E0_exact  = vqe["E0_exact"]
    E_opt     = vqe["E_optimized"]
    threshold = E0_exact * 1.01

    iters = np.arange(1, len(history) + 1)

    ax.plot(iters, history, color=COLORS["quantum"], lw=1.2,
            alpha=0.85, label="VQE energy $E(\\theta)$", zorder=3)

    # Moving average for clarity
    window = max(1, len(history) // 30)
    if len(history) > window:
        ma = np.convolve(history, np.ones(window)/window, mode='valid')
        ax.plot(np.arange(window, len(history) + 1), ma,
                color=COLORS["fitted"], lw=2.0, label=f"Moving avg (w={window})", zorder=4)

    # Reference lines
    ax.axhline(E0_exact,  color=COLORS["e0_line"], lw=1.5, ls='--',
               label=f"Exact $E_0$ = {E0_exact:.4f}", zorder=5)
    ax.axhline(threshold, color=COLORS["threshold"], lw=1.2, ls=':',
               label=f"1% threshold = {threshold:.4f}", zorder=5)

    # Markers
    ax.scatter([1], [history[0]], color='gold', s=80, zorder=6,
               label=f"Initial: {history[0]:.4f}", edgecolors='k', lw=0.8)
    ax.scatter([len(history)], [E_opt], color=COLORS["analytical"], s=80, zorder=6,
               label=f"Final: {E_opt:.4f}", edgecolors='k', lw=0.8, marker='*')

    converged = vqe.get("converged_1pct", False)
    pct_err   = vqe.get("pct_error", 0)
    n_evals   = vqe.get("n_function_evals", len(history))

    ax.set_xlabel("Function Evaluation", fontsize=11)
    ax.set_ylabel("Energy $\\langle H \\rangle$", fontsize=11)
    ax.set_title(f"VQE Energy Convergence — 16-qubit MERA\n"
                 f"COBYLA, {n_evals} evals, "
                 f"error = {pct_err:.2f}%, converged = {converged}",
                 fontsize=10)
    ax.legend(fontsize=8, loc='upper right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0, len(history) + 1)


def plot_force_profile(sim: dict, classical: dict, ax: plt.Axes):
    """Plot V(delta_rho) — quantum, classical, analytical, fitted."""
    fp       = sim["force_profile"]
    dr_q     = np.array(fp["delta_rho"])
    V_q      = np.array(fp["V_quantum"])
    V_anal   = np.array(fp["V_analytical"])

    fit      = sim.get("fit", {})

    cl_corr  = classical["correlators"]
    dr_cl    = np.array(cl_corr["separations"])
    V_cl     = np.array(cl_corr["V_force"])

    # Analytical curve (smooth)
    dr_fine  = np.linspace(0.5, 9, 200)
    V_fine   = C1_PAPER - C2_PAPER * np.exp(-dr_fine / L_ADS)

    # Fitted curve
    fit_ok = fit.get("success", False)
    if fit_ok and fit.get("C1") is not None:
        C1f = fit["C1"]; C2f = fit["C2"]; xif = fit["xi"]
        V_fit_fine = C1f - C2f * np.exp(-dr_fine / xif)
        fit_label = f"MERA fit: $C_1$={C1f:.3f}, $C_2$={C2f:.2f}, $\\xi$={xif:.3f}"
    else:
        V_fit_fine = None
        fit_label  = "MERA fit: failed"

    # Plot
    ax.plot(dr_fine, V_fine, color=COLORS["analytical"], lw=2.0, ls='-',
            label=f"Analytical AdS: $C_1$={C1_PAPER}, $C_2$={C2_PAPER}, $l_{{AdS}}$={L_ADS:.3f}",
            zorder=2)

    if V_fit_fine is not None:
        ax.plot(dr_fine, V_fit_fine, color=COLORS["fitted"], lw=1.8, ls='--',
                label=fit_label, zorder=3)

    ax.scatter(dr_q, V_q, color=COLORS["quantum"], s=70, zorder=5,
               label="MERA VQE (quantum sim)", edgecolors='k', lw=0.8)
    ax.plot(dr_q, V_q, color=COLORS["quantum"], lw=1.0, alpha=0.5, zorder=4)

    ax.scatter(dr_cl, V_cl, color=COLORS["classical"], s=50, marker='s', zorder=5,
               label="Classical ED (N=16 PBC)", edgecolors='k', lw=0.6)
    ax.plot(dr_cl, V_cl, color=COLORS["classical"], lw=1.0, alpha=0.5, zorder=4)

    ax.axhline(0, color='gray', lw=0.8, ls='--', alpha=0.5)
    ax.set_xlabel("Separation $\\delta\\rho$ (lattice units)", fontsize=11)
    ax.set_ylabel("$V(\\delta\\rho)$", fontsize=11)
    ax.set_title("Holographic Force Profile — MERA vs Classical ED vs AdS Theory", fontsize=10)
    ax.legend(fontsize=8, loc='lower right')
    ax.grid(True, alpha=0.3)
    ax.set_xlim(0.5, max(max(dr_q), max(dr_cl)) + 0.5)


def plot_parameter_landscape(sim: dict, ax: plt.Axes):
    """Histogram of initial vs optimized MERA parameters."""
    vqe       = sim["vqe"]
    theta_opt = np.array(vqe.get("theta_optimized", []))

    # Initial params (analytically motivated — reconstruct)
    rng    = np.random.default_rng(seed=0)
    N_QUBITS = 16
    N_LAYERS = 3
    n_params = len(theta_opt)
    theta_init = np.zeros(n_params)
    idx = 0
    for layer in range(N_LAYERS):
        n_sites = N_QUBITS // (2 ** layer)
        n_pairs = n_sites // 2
        for _ in range(n_pairs):
            base = np.array([np.pi/4, np.pi/2, np.pi/4, np.pi/2, np.pi/4, np.pi/4])
            theta_init[idx:idx+6] = base + rng.normal(0, 0.08, 6)
            idx += 6
        for _ in range(n_pairs):
            base = np.array([np.pi/4, np.pi/8, np.pi/4, np.pi/6])
            theta_init[idx:idx+4] = base + rng.normal(0, 0.08, 4)
            idx += 4
    if idx + 6 <= n_params:
        base = np.array([np.pi/3, np.pi/4, np.pi/3, np.pi/4, np.pi/4, np.pi/3])
        theta_init[idx:idx+6] = base + rng.normal(0, 0.08, 6)

    bins = np.linspace(-np.pi, 2*np.pi, 40)
    ax.hist(theta_init[:n_params], bins=bins, alpha=0.55,
            color=COLORS["classical"], label="Initial (analytic + noise)", density=True)
    ax.hist(theta_opt, bins=bins, alpha=0.55,
            color=COLORS["quantum"], label="Optimized (post-VQE)", density=True)

    # Mark key angles
    for angle, label in [(0, '0'), (np.pi/4, 'π/4'), (np.pi/2, 'π/2'),
                          (np.pi, 'π'), (3*np.pi/2, '3π/2')]:
        ax.axvline(angle, color='gray', lw=0.8, ls=':', alpha=0.7)
        ax.text(angle, ax.get_ylim()[1]*0.02 if ax.get_ylim()[1] > 0 else 0.01,
                label, ha='center', fontsize=7, color='gray')

    ax.set_xlabel("Parameter value (radians)", fontsize=11)
    ax.set_ylabel("Density", fontsize=11)
    ax.set_title(f"MERA Parameter Distribution: Before vs After VQE\n"
                 f"({n_params} parameters, 16-qubit 3-layer circuit)", fontsize=10)
    ax.legend(fontsize=8)
    ax.grid(True, alpha=0.3)


def main():
    print("=" * 65)
    print("Visualization Agent — SIM-2026-002")
    print("=" * 65)

    # Load
    sim, classical = load_data()

    # ── Figure 1: VQE convergence + Force profile (2-panel) ──────────────
    fig1, (ax1, ax2) = plt.subplots(1, 2, figsize=(15, 6))
    fig1.suptitle("HYP-2026-002: VQE MERA Optimization & Holographic Force Profile",
                  fontsize=13, fontweight='bold', y=1.01)

    plot_vqe_convergence(sim, ax1)
    plot_force_profile(sim, classical, ax2)

    plt.tight_layout()
    path1 = os.path.join(PLOT_DIR, "SIM-2026-002_vqe_and_force.png")
    fig1.savefig(path1, dpi=150, bbox_inches='tight')
    print(f"  Saved: {path1}")
    plt.close(fig1)

    # ── Figure 2: Parameter landscape ─────────────────────────────────────
    fig2, ax3 = plt.subplots(figsize=(10, 5))
    plot_parameter_landscape(sim, ax3)
    plt.tight_layout()
    path2 = os.path.join(PLOT_DIR, "SIM-2026-002_parameter_landscape.png")
    fig2.savefig(path2, dpi=150, bbox_inches='tight')
    print(f"  Saved: {path2}")
    plt.close(fig2)

    # ── Figure 3: Classical correlators standalone ─────────────────────────
    cl_corr = classical["correlators"]
    dr_cl   = np.array(cl_corr["separations"])
    C_cl    = np.array(cl_corr["C_connected"])
    V_cl    = np.array(cl_corr["V_force"])

    fig3, (ax4, ax5) = plt.subplots(1, 2, figsize=(13, 5))
    fig3.suptitle("Classical ED Baseline — N=16 TFIM (Periodic BC)", fontsize=12,
                  fontweight='bold')

    # Raw correlators
    ax4.scatter(dr_cl, C_cl, color=COLORS["classical"], s=60, zorder=5,
                edgecolors='k', lw=0.7, label="$C(r) = \\langle Z_i Z_j \\rangle_c$")
    ax4.plot(dr_cl, C_cl, color=COLORS["classical"], lw=1.0, alpha=0.5)

    # Power law fit overlay
    fits_cl = classical.get("fits", {}).get("power_law", {})
    A_pw = fits_cl.get("A"); eta_pw = fits_cl.get("eta")
    if A_pw and eta_pw:
        r_fine = np.linspace(1, max(dr_cl)+0.5, 200)
        ax4.plot(r_fine, A_pw * r_fine**(-eta_pw), color=COLORS["analytical"], lw=2,
                 label=f"Power law: $A r^{{-\\eta}}$, $\\eta$={eta_pw:.3f} (theory: 0.25)")
    ax4.set_xlabel("Separation $r$", fontsize=11)
    ax4.set_ylabel("$C(r)$", fontsize=11)
    ax4.set_title("ZZ Connected Correlator", fontsize=10)
    ax4.legend(fontsize=8)
    ax4.grid(True, alpha=0.3)

    # Force profile
    ax5.scatter(dr_cl, V_cl, color=COLORS["classical"], s=60, zorder=5,
                edgecolors='k', lw=0.7, label="$V_{ED}(r) = C_{pert} - C_{vac}$")
    ax5.plot(dr_cl, V_cl, color=COLORS["classical"], lw=1.0, alpha=0.5)

    # AdS prediction
    dr_fine = np.linspace(0.5, max(dr_cl)+0.5, 200)
    V_anal  = C1_PAPER - C2_PAPER * np.exp(-dr_fine / L_ADS)
    ax5.plot(dr_fine, V_anal, color=COLORS["analytical"], lw=2,
             label=f"AdS: $C_1$={C1_PAPER}, $C_2$={C2_PAPER}")

    ax5.axhline(0, color='gray', lw=0.8, ls='--', alpha=0.5)
    ax5.set_xlabel("Separation $r$", fontsize=11)
    ax5.set_ylabel("$V(r)$", fontsize=11)
    ax5.set_title("Force Profile (Ry hologron perturbation)", fontsize=10)
    ax5.legend(fontsize=8)
    ax5.grid(True, alpha=0.3)

    plt.tight_layout()
    path3 = os.path.join(PLOT_DIR, "SIM-2026-002_classical_baseline.png")
    fig3.savefig(path3, dpi=150, bbox_inches='tight')
    print(f"  Saved: {path3}")
    plt.close(fig3)

    print("\nVisualization complete.")
    print("=" * 65)
    return [path1, path2, path3]


if __name__ == "__main__":
    paths = main()
