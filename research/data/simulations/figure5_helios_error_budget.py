"""
Figure 5: Helios Circuit Layout and Error Budget
=================================================
Two-panel figure:
Left:  MERA binary tree schematic (circuit layout for 16q/3L and 32q/3L)
Right: Error budget comparison across hardware platforms and circuit sizes

Key numbers (from helios-mera-design.md and memory):
- IBM Heron r3: 16q/3L -> 90 CZ, 41.2% error (INFEASIBLE)
- Helios phys:  16q/3L -> 56 CNOT, 4.4% error
- Helios logical: 16q/3L -> 56 CNOT, 0.56% error (error-detection)
- Helios logical: 32q/3L -> 140 CNOT, 1.39% error
- Helios logical: 24q/5L -> 150 CNOT, 1.49% error
- Transport (16q+10 Trotter): 376 CNOT, 3.7% error

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
from matplotlib.patches import FancyBboxPatch, FancyArrowPatch

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

OUT_PATH = "D:/quantum-worldline/research/data/simulations/figure5_helios_error_budget.png"

# ── Error budget data ─────────────────────────────────────────────────────────
# (label, cnot_count, error_pct, hardware, circuit_type)
configs = [
    # IBM Heron r3 (physical, 99.5% CX fidelity ~ 0.5% error/gate + SWAP overhead)
    ("IBM Heron r3\n16q/3L\n(90 CZ)", 90, 41.2, "IBM Heron r3", "force"),
    # Quantinuum H2 physical (99.8% CX)
    ("H2 physical\n16q/3L\n(29 CX)", 29, 5.64, "H2 physical", "force"),
    # Helios physical (99.921% CX -> 7.9e-4 infidelity)
    ("Helios physical\n16q/3L\n(56 CNOT)", 56, 4.3, "Helios physical", "force"),
    # Helios logical (error-detection, 1e-4 per gate)
    ("Helios logical\n16q/3L\n(56 CNOT)", 56, 0.56, "Helios logical", "force"),
    ("Helios logical\n24q/5L\n(150 CNOT)", 150, 1.49, "Helios logical", "force"),
    ("Helios logical\n32q/3L\n(140 CNOT)", 140, 1.39, "Helios logical", "force"),
    # Transport measurement
    ("Helios logical\n16q Transport\n(376 CNOT)", 376, 3.7, "Helios logical", "transport"),
]

HARDWARE_COLORS = {
    "IBM Heron r3":     '#F44336',
    "H2 physical":      '#FF9800',
    "Helios physical":  '#2196F3',
    "Helios logical":   '#4CAF50',
}

# ── Figure setup ──────────────────────────────────────────────────────────────
fig = plt.figure(figsize=(14, 6))
fig.patch.set_facecolor('white')

gs = fig.add_gridspec(1, 2, width_ratios=[1, 1.4], wspace=0.3)
ax_circuit = fig.add_subplot(gs[0])
ax_budget  = fig.add_subplot(gs[1])

# ── Left: MERA circuit schematic ──────────────────────────────────────────────
ax_circuit.set_xlim(-0.5, 5.5)
ax_circuit.set_ylim(-0.5, 4.0)
ax_circuit.set_aspect('equal')
ax_circuit.axis('off')
ax_circuit.set_facecolor('white')
ax_circuit.set_title('Binary MERA Structure\n(16-qubit, 3 layers shown)', fontsize=10, fontweight='bold')

# Draw qubit lines (layer 0 = boundary, 8 qubits shown for clarity)
N_SHOW = 8
x_qubits = np.linspace(0, 5, N_SHOW)
y_layers = [0, 1.3, 2.6, 3.5]

# Boundary qubits (layer 0)
for x in x_qubits:
    ax_circuit.plot([x, x], [y_layers[0] - 0.3, y_layers[0] + 0.3],
                    '-', color='#1565C0', linewidth=2.5, solid_capstyle='round')
    ax_circuit.add_patch(mpatches.Circle((x, y_layers[0]), 0.13,
                                          facecolor='#1565C0', edgecolor='white', linewidth=1.5, zorder=5))

# Disentanglers (2-site, layer 0->1)
def draw_gate(ax, x1, y, label='U', color='#4CAF50', width=0.4):
    rect = FancyBboxPatch((x1 - width/2, y - 0.18), width, 0.36,
                           boxstyle="round,pad=0.02",
                           facecolor=color, edgecolor='white', linewidth=1.5, zorder=6)
    ax.add_patch(rect)
    ax.text(x1, y, label, ha='center', va='center', fontsize=7, color='white',
            fontweight='bold', zorder=7)

def draw_wire(ax, x, y1, y2, color='#9E9E9E'):
    ax.plot([x, x], [y1, y2], '-', color=color, linewidth=1.5, alpha=0.6, zorder=3)

def draw_isometry(ax, x1, x2, y_in, y_out, label='W'):
    # Triangle-ish: two inputs merge to one output
    xm = (x1 + x2) / 2
    tri_x = [x1, x2, xm, x1]
    tri_y = [y_in, y_in, y_out, y_in]
    ax.fill(tri_x, tri_y, color='#FF8F00', alpha=0.85, zorder=6)
    ax.plot(tri_x, tri_y, '-', color='white', linewidth=1, zorder=7)
    ax.text(xm, (y_in * 0.4 + y_out * 0.6), label,
            ha='center', va='center', fontsize=7, color='white', fontweight='bold', zorder=8)
    ax.add_patch(mpatches.Circle((xm, y_out), 0.13,
                                  facecolor='#FF8F00', edgecolor='white', linewidth=1.5, zorder=8))

# Layer 1: disentanglers between pairs
disentangler_xs_l1 = [(x_qubits[i] + x_qubits[i+1]) / 2 for i in [0, 2, 4, 6]]
for xm in disentangler_xs_l1:
    draw_gate(ax_circuit, xm, y_layers[0] + 0.55, 'U', color='#4CAF50', width=0.7)

# Wires going up
for i, x in enumerate(x_qubits):
    draw_wire(ax_circuit, x, y_layers[0] + 0.3, y_layers[1] - 0.3)

# Isometries (layer 1)
isometry_xs_l1 = [(x_qubits[i] + x_qubits[i+1]) / 2 for i in [0, 2, 4, 6]]
for xm in isometry_xs_l1:
    # Show 2->1 compression
    lx = xm - 0.35
    rx = xm + 0.35
    draw_isometry(ax_circuit, lx, rx, y_layers[1], y_layers[1] + 0.6, 'W')

# Layer 2 qubits
x_layer2 = [(x_qubits[i] + x_qubits[i+1]) / 2 for i in [0, 2, 4, 6]]
for x in x_layer2:
    draw_wire(ax_circuit, x, y_layers[1] + 0.6, y_layers[2] - 0.3)
    ax_circuit.add_patch(mpatches.Circle((x, y_layers[2] - 0.15), 0.10,
                                          facecolor='#7E57C2', edgecolor='white', linewidth=1.2, zorder=5))

# Layer 2 disentanglers
for i in range(0, len(x_layer2) - 1, 2):
    xm = (x_layer2[i] + x_layer2[i+1]) / 2
    draw_gate(ax_circuit, xm, y_layers[2], 'U', color='#4CAF50', width=0.6)

# Layer 2 isometries
for i in range(0, len(x_layer2) - 1, 2):
    xm = (x_layer2[i] + x_layer2[i+1]) / 2
    lx = xm - 0.3; rx = xm + 0.3
    draw_isometry(ax_circuit, lx, rx, y_layers[2] + 0.25, y_layers[2] + 0.75, 'W')

# Top tensor
top_x = (x_layer2[1] + x_layer2[2]) / 2
draw_gate(ax_circuit, top_x, y_layers[3], 'Top', color='#E91E63', width=0.8)

# Legend
leg_items = [
    mpatches.Patch(color='#4CAF50', label='Disentangler U (2-site)'),
    mpatches.Patch(color='#FF8F00', label='Isometry W (2->1)'),
    mpatches.Patch(color='#E91E63', label='Top tensor'),
    mpatches.Patch(color='#1565C0', label='Boundary qubits'),
]
ax_circuit.legend(handles=leg_items, loc='lower left', fontsize=7.5, framealpha=0.9)

# Arrows showing layers
for i, (y, lbl) in enumerate(zip(y_layers[:3], ['Layer 0\n(boundary)', 'Layer 1', 'Layer 2'])):
    ax_circuit.text(-0.4, y, lbl, ha='right', va='center', fontsize=7.5,
                    color='#424242', style='italic')

# ── Right: Error budget bar chart ─────────────────────────────────────────────
ax_budget.set_facecolor('#FAFAFA')

labels   = [c[0] for c in configs]
cnots    = [c[1] for c in configs]
errors   = [c[2] for c in configs]
hardware = [c[3] for c in configs]
colors   = [HARDWARE_COLORS[h] for h in hardware]

x = np.arange(len(labels))
bars = ax_budget.bar(x, errors, color=colors, edgecolor='white', linewidth=1.5,
                     width=0.65, zorder=4)

# Value labels
for bar, err, cnot in zip(bars, errors, cnots):
    ax_budget.text(bar.get_x() + bar.get_width()/2, err + 0.4,
                   f'{err:.1f}%\n({cnot} CX)',
                   ha='center', va='bottom', fontsize=8, fontweight='bold',
                   color='#212121')

# Reference lines
ax_budget.axhline(y=5.0, color='orange', linestyle='--', linewidth=1.5, alpha=0.8,
                   label='5% PoC threshold', zorder=5)
ax_budget.axhline(y=10.0, color='red', linestyle='--', linewidth=1.5, alpha=0.6,
                   label='10% feasibility limit', zorder=5)
ax_budget.axhline(y=1.0, color='green', linestyle=':', linewidth=1.5, alpha=0.8,
                   label='1% high-confidence target', zorder=5)

# INFEASIBLE shade
ax_budget.axhspan(10, 45, alpha=0.07, color='red', zorder=1)
ax_budget.text(len(labels) - 0.5, 30, 'INFEASIBLE\nzone', ha='center', fontsize=9,
               color='#B71C1C', alpha=0.6, style='italic')

ax_budget.set_xticks(x)
ax_budget.set_xticklabels(labels, fontsize=8, rotation=10, ha='right')
ax_budget.set_ylabel('Accumulated gate error (%)', fontsize=11)
ax_budget.set_title('Error Budget by Hardware and Circuit Size\n'
                     '(formula: 1 - (1-p_gate)^N_CX + SPAM)',
                     fontsize=11, fontweight='bold')
ax_budget.set_ylim(0, 45)
ax_budget.grid(axis='y', alpha=0.3, zorder=0)

# Hardware legend
leg_patches = [mpatches.Patch(color=c, label=h) for h, c in HARDWARE_COLORS.items()]
ax_budget.legend(handles=leg_patches + [
    plt.Line2D([0], [0], color='orange', lw=1.5, linestyle='--', label='5% threshold'),
    plt.Line2D([0], [0], color='green', lw=1.5, linestyle=':', label='1% target'),
], fontsize=8, loc='upper left', ncol=2, framealpha=0.9)

# ── Finalize ──────────────────────────────────────────────────────────────────
fig.suptitle(
    'Figure 5: Helios Circuit Topology and Hardware Error Budget\n'
    'IBM Heron r3 is infeasible (41%); Helios logical achieves 0.56-3.7% across all configurations',
    fontsize=10, y=1.01, style='italic'
)

plt.tight_layout()
plt.savefig(OUT_PATH, dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved: {OUT_PATH}")
