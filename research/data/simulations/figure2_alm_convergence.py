"""
Figure 2: ALM + Z2-Projection Convergence Curves (SIM-2026-008b/c)
===================================================================
Shows the two-phase optimization:
- Phase 1 (ALM): unconstrained L-BFGS-B with ALM penalty forces Z2
- Phase 2 (projection): projected L-BFGS-B from ALM warm-start

Left panel: 8q validation (SIM-2026-008b) showing dramatic improvement
Right panel: 24q/5-layer production (SIM-2026-008c) showing 5 seeds

Author: computation-lead
Date:   2026-03-18
"""

import sys
import io
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT_PATH = "D:/quantum-worldline/research/data/simulations/figure2_alm_convergence.png"

# ── Data from JSON results ────────────────────────────────────────────────────

# SIM-2026-008b: 8q, seeds 7 and 42
data_8q = {
    "E0_exact": -9.837951447459433,
    "seeds": [7, 42],
    "alm_E": [-9.027806812649306, -9.027802303220763],
    "alm_err": [8.234891, 8.234937],
    "alm_P": [1.000, 1.000],
    "projopt_E": [-9.728252180770722, -9.728253541651274],
    "projopt_err": [1.115062, 1.115048],
    "projopt_P": [1.0, 1.0],
    # SIM-2026-008a: parity-preserving gate set (failure baseline)
    "baseline_err": [6.396900, 6.396901],
}

# SIM-2026-008c: 24q/5-layer, 5 seeds
data_24q = {
    "E0_exact": -30.199712,
    "seeds": [7, 42, 99, 13, 77],
    "phase1_err": [3.3637, 3.3370, 4.0938, 5.2397, 3.3718],
    "phase2_err": [3.3365, 3.3340, 3.3398, 4.3014, 3.3345],
    "phase1_P": [1e-6, 1.5e-6, 5.8e-7, -1.6e-10, 1.3e-6],
    "phase2_P": [1.0, 1.0, 1.0, 1.0, 1.0],
    "best_seed": 42,
}

# ── Colors and style ──────────────────────────────────────────────────────────
SEED_COLORS = ['#2196F3', '#4CAF50', '#FF9800', '#E91E63', '#9C27B0']
ALM_COLOR   = '#9E9E9E'    # grey for phase 1
PROJ_COLOR  = '#2196F3'    # blue for phase 2
BASELINE_COLOR = '#F44336' # red for bad baseline

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.patch.set_facecolor('white')

# ── Left panel: 8q validation (before/after comparison) ──────────────────────
ax1 = axes[0]
ax1.set_facecolor('#FAFAFA')

methods = ['Parity-\npreserving\ngates (fail)', 'Phase 1\nALM', 'Phase 2\nProjected\nL-BFGS-B']
x_pos = [0, 1, 2]

for i, seed in enumerate([7, 42]):
    label = f'Seed {seed}'
    baseline_err = data_8q['baseline_err'][i]
    alm_err = data_8q['alm_err'][i]
    proj_err = data_8q['projopt_err'][i]

    offset = (i - 0.5) * 0.12
    ax1.plot([0 + offset, 1 + offset, 2 + offset],
             [baseline_err, alm_err, proj_err],
             'o-', color=SEED_COLORS[i], linewidth=2, markersize=7,
             label=label, zorder=5)

# Annotate final values
for i, seed in enumerate([7, 42]):
    proj_err = data_8q['projopt_err'][i]
    ax1.annotate(f'{proj_err:.2f}%',
                 xy=(2 + (i - 0.5) * 0.12, proj_err),
                 xytext=(5, 3), textcoords='offset points',
                 fontsize=9, color=SEED_COLORS[i], fontweight='bold')

# Reference lines
ax1.axhline(y=5.0, color='orange', linestyle='--', linewidth=1, alpha=0.7,
            label='5% threshold')
ax1.axhline(y=1.5, color='green', linestyle='--', linewidth=1, alpha=0.7,
            label='1.5% target')

ax1.set_xticks(x_pos)
ax1.set_xticklabels(methods, fontsize=9)
ax1.set_ylabel('Energy error (%)', fontsize=11)
ax1.set_title('8q Validation: ALM + Projection Pipeline\n(SIM-2026-008b)', fontsize=11, fontweight='bold')
ax1.legend(fontsize=9, loc='upper right')
ax1.set_ylim(0, 10)
ax1.grid(axis='y', alpha=0.3)

# Z2 parity annotation
ax1.text(0.5, 0.08, 'P = 1.000 throughout all methods',
         transform=ax1.transAxes, fontsize=8.5, ha='center',
         style='italic', color='#1565C0',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#E3F2FD', alpha=0.8))

# ── Right panel: 24q/5-layer production results ───────────────────────────────
ax2 = axes[1]
ax2.set_facecolor('#FAFAFA')

n_seeds = len(data_24q['seeds'])
x = np.arange(n_seeds)
bar_w = 0.32

bars1 = ax2.bar(x - bar_w/2, data_24q['phase1_err'],
                bar_w, label='Phase 1 (ALM)', color=ALM_COLOR, alpha=0.8,
                edgecolor='white', linewidth=1.5)
bars2 = ax2.bar(x + bar_w/2, data_24q['phase2_err'],
                bar_w, label='Phase 2 (Projected L-BFGS-B)', color=PROJ_COLOR, alpha=0.9,
                edgecolor='white', linewidth=1.5)

# Highlight best seed
best_idx = data_24q['seeds'].index(data_24q['best_seed'])
ax2.bar(best_idx + bar_w/2, data_24q['phase2_err'][best_idx],
        bar_w, color='#FF8F00', alpha=1.0, edgecolor='#E65100', linewidth=2,
        label=f'Best (seed {data_24q["best_seed"]})')

# Value labels on phase 2 bars
for i, (bar, err) in enumerate(zip(bars2, data_24q['phase2_err'])):
    ax2.text(bar.get_x() + bar.get_width() / 2, err + 0.08,
             f'{err:.2f}%', ha='center', va='bottom', fontsize=8,
             color='#1A237E', fontweight='bold')

# Reference lines
ax2.axhline(y=5.0, color='orange', linestyle='--', linewidth=1, alpha=0.7,
            label='5% threshold')
ax2.axhline(y=3.334, color='#F44336', linestyle=':', linewidth=1.5, alpha=0.8,
            label='Architecture floor (3.33%)')

ax2.set_xticks(x)
ax2.set_xticklabels([f'Seed {s}' for s in data_24q['seeds']], fontsize=9)
ax2.set_ylabel('Energy error (%)', fontsize=11)
ax2.set_title('24q / 5-Layer MERA: ALM+Projection Production Run\n(SIM-2026-008c, 44h on RunPod A6000)',
              fontsize=11, fontweight='bold')
ax2.legend(fontsize=8.5, loc='upper right')
ax2.set_ylim(0, 7)
ax2.grid(axis='y', alpha=0.3)

# Z2 parity annotation
ax2.text(0.5, 0.92, '<P> = 1.000  <M> = 0.000  for ALL seeds after Phase 2',
         transform=ax2.transAxes, fontsize=8.5, ha='center',
         style='italic', color='#1565C0',
         bbox=dict(boxstyle='round,pad=0.2', facecolor='#E3F2FD', alpha=0.8))

# ── Finalize ──────────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure 2: Two-Phase ALM + Z2-Projection Optimization\n'
    'Left: 8q validation shows ALM warmstart enables 1.12% energy error. '
    'Right: 24q/5L production converges to ~3.33% structural floor.',
    fontsize=10, y=1.01, style='italic'
)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {OUT_PATH}")
