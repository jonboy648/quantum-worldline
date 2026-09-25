"""Create a 'frosted glass' diagram showing boundary = surface, MERA = depth, bulk = behind the glass."""
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(10, 6))
ax.set_xlim(0, 10)
ax.set_ylim(0, 6.5)
ax.axis('off')

# The frosted glass surface (boundary)
glass_x = [1, 9]
glass_y = [1.2, 1.2]
ax.plot(glass_x, glass_y, color='#5588bb', linewidth=4, solid_capstyle='round')
ax.fill_between([1, 9], [0, 0], [1.2, 1.2], color='#d0dde8', alpha=0.4)

# Boundary label and dots (qubits)
for i in range(16):
    x = 1.5 + i * 0.44
    ax.plot(x, 1.2, 'o', color='#2255aa', markersize=6, zorder=5)
ax.text(5, 0.5, 'BOUNDARY  (the frosted glass surface)', ha='center', fontsize=11,
        color='#2255aa', fontweight='bold', style='italic')
ax.text(5, 0.05, 'What you can see and measure: quantum spins, correlations, entanglement',
        ha='center', fontsize=8.5, color='#5577aa')

# MERA layers (depth behind the glass)
layer_colors = ['#aaccee', '#88bbdd', '#66aacc', '#4499bb', '#2288aa']
layer_labels = ['Layer 1: fine patterns', 'Layer 2: medium patterns', 'Layer 3: coarse patterns',
                'Layer 4: large-scale', 'Layer 5: global']
for i, (color, label) in enumerate(zip(layer_colors, layer_labels)):
    y_bot = 1.4 + i * 0.85
    y_top = y_bot + 0.65
    # Narrowing trapezoid
    shrink = i * 0.4
    ax.fill([1.5 + shrink, 8.5 - shrink, 8.2 - shrink - 0.3, 1.8 + shrink + 0.3],
            [y_bot, y_bot, y_top, y_top],
            color=color, alpha=0.5, edgecolor='#4488aa', linewidth=0.8)
    # Nodes in this layer
    n_nodes = max(2, 16 // (2 ** (i + 1)))
    for j in range(n_nodes):
        nx = 2.0 + shrink + j * (6.0 - 2 * shrink) / max(1, n_nodes - 1)
        ny = (y_bot + y_top) / 2
        ax.plot(nx, ny, 's', color='white', markersize=5, markeredgecolor='#336699', zorder=5)
    # Label
    ax.text(9.0 - shrink + 0.15, (y_bot + y_top) / 2, label, fontsize=7.5,
            va='center', color='#336699', fontstyle='italic')

# Top label: the bulk
y_top_final = 1.4 + 5 * 0.85 + 0.1
ax.text(5, y_top_final + 0.3, 'EMERGENT AdS GEOMETRY  (behind the glass)',
        ha='center', fontsize=11, color='#115577', fontweight='bold', style='italic')
ax.text(5, y_top_final - 0.1, 'Forces, geodesics, curved spacetime - all from the pattern hierarchy',
        ha='center', fontsize=8.5, color='#4488aa')

# Arrows showing "depth"
ax.annotate('', xy=(0.6, 5.8), xytext=(0.6, 1.2),
            arrowprops=dict(arrowstyle='->', color='#cc6633', lw=2))
ax.text(0.35, 3.5, 'D\nE\nP\nT\nH', ha='center', fontsize=9, color='#cc6633',
        fontweight='bold', linespacing=1.8)

# "Wiping the glass" annotation
ax.annotate('MERA reveals\nwhat is behind\nthe glass', xy=(5, 1.4), xytext=(0.3, 0.8),
            fontsize=8, color='#885522', fontstyle='italic',
            arrowprops=dict(arrowstyle='->', color='#885522', lw=1.2))

plt.tight_layout()
plt.savefig('D:/quantum-worldline/research/learning/frosted_glass_diagram.png', dpi=200, bbox_inches='tight',
            facecolor='white')
print("Saved frosted_glass_diagram.png")
