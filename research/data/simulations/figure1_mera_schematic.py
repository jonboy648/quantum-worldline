"""Figure 1: MERA geometry schematic showing boundary-bulk correspondence."""
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np

fig, ax = plt.subplots(1, 1, figsize=(8, 6))
ax.set_xlim(-1, 17)
ax.set_ylim(-0.5, 7.5)
ax.set_aspect('equal')
ax.axis('off')

# Colors
BOUNDARY_COLOR = '#1565C0'
DISENTANGLER_COLOR = '#4CAF50'
ISOMETRY_COLOR = '#FF9800'
CAUSAL_COLOR = '#FFECB3'
ADS_COLOR = '#E3F2FD'

# Layer positions (y-coords)
y_boundary = 0
y_layers = [1.5, 3.0, 4.5]

# Boundary sites (16 qubits shown as 8 pairs for clarity)
n_sites = 16
x_sites = np.linspace(0, 15, n_sites)

# Draw boundary chain
for i, x in enumerate(x_sites):
    ax.plot(x, y_boundary, 'o', color=BOUNDARY_COLOR, markersize=8, zorder=5)
    if i < n_sites - 1:
        ax.plot([x, x_sites[i+1]], [y_boundary, y_boundary], '-', color=BOUNDARY_COLOR, linewidth=1, alpha=0.4)

ax.text(7.5, -0.4, 'Boundary (CFT)', ha='center', fontsize=10, color=BOUNDARY_COLOR, fontweight='bold')

# Draw MERA layers
for layer, y in enumerate(y_layers):
    n_disentanglers = max(1, n_sites // (2**(layer+1)))
    n_isometries = max(1, n_sites // (2**(layer+1)))

    # Disentanglers (green boxes)
    for i in range(n_disentanglers):
        x_center = (2*i + 0.5) * (15.0 / (n_disentanglers * 2))
        x_center = min(x_center, 14.5)
        rect = patches.FancyBboxPatch(
            (x_center - 0.4, y - 0.25), 0.8, 0.5,
            boxstyle="round,pad=0.1", facecolor=DISENTANGLER_COLOR, alpha=0.7, edgecolor='white', linewidth=1)
        ax.add_patch(rect)

    # Isometries (orange triangles)
    for i in range(n_isometries):
        x_center = (2*i + 1.5) * (15.0 / (n_isometries * 2))
        x_center = min(x_center, 14.5)
        triangle = plt.Polygon(
            [(x_center - 0.35, y - 0.2), (x_center + 0.35, y - 0.2), (x_center, y + 0.3)],
            facecolor=ISOMETRY_COLOR, alpha=0.7, edgecolor='white', linewidth=1)
        ax.add_patch(triangle)

# Layer labels
for i, y in enumerate(y_layers):
    ax.text(16.2, y, f'Layer {i+1}', fontsize=9, va='center', color='gray')

# Top tensor (scale-invariant fixed point)
ax.plot(7.5, 6.0, 's', color='#9C27B0', markersize=14, zorder=5)
ax.text(7.5, 6.5, 'Top tensor', ha='center', fontsize=9, color='#9C27B0')

# Causal cone shading (from one boundary site up through layers)
cone_x = 4  # boundary site index
cone_base = x_sites[cone_x]
cone_verts = [
    (cone_base - 0.3, y_boundary + 0.2),
    (cone_base + 0.3, y_boundary + 0.2),
    (cone_base + 4, 6.0),
    (cone_base - 4, 6.0),
]
cone = plt.Polygon(cone_verts, facecolor=CAUSAL_COLOR, alpha=0.3, edgecolor='#F9A825', linewidth=1.5, linestyle='--', zorder=1)
ax.add_patch(cone)
ax.text(cone_base, y_boundary + 0.5, 'Causal\ncone', fontsize=8, ha='center', color='#F57F17', fontweight='bold')

# Arrows showing bulk direction
ax.annotate('', xy=(16, 5.5), xytext=(16, 0.5),
            arrowprops=dict(arrowstyle='->', color='gray', lw=1.5))
ax.text(16.5, 3.0, 'Bulk\n(radial\ndirection\nin AdS)', fontsize=8, color='gray', ha='left', va='center')

# l_AdS annotation
ax.annotate('', xy=(0.5, 1.5), xytext=(0.5, 0),
            arrowprops=dict(arrowstyle='<->', color='#7B1FA2', lw=1.5))
ax.text(-0.5, 0.75, f'l_AdS = 1/ln(2)\n= 1.443', fontsize=8, color='#7B1FA2', ha='center', va='center')

# Legend
legend_elements = [
    patches.Patch(facecolor=BOUNDARY_COLOR, label='Boundary qubits (CFT)'),
    patches.Patch(facecolor=DISENTANGLER_COLOR, alpha=0.7, label='Disentanglers (u)'),
    patches.Patch(facecolor=ISOMETRY_COLOR, alpha=0.7, label='Isometries (w)'),
    patches.Patch(facecolor=CAUSAL_COLOR, alpha=0.5, edgecolor='#F9A825', label='Causal cone'),
]
ax.legend(handles=legend_elements, loc='upper left', fontsize=8, framealpha=0.9)

fig.suptitle('Figure 1: Binary MERA as Discrete AdS Geometry', fontsize=12, fontweight='bold')
plt.tight_layout()
plt.savefig("D:/quantum-worldline/research/data/simulations/figure1_mera_schematic.png",
            dpi=150, bbox_inches='tight', facecolor='white')
print("Figure 1 saved")
