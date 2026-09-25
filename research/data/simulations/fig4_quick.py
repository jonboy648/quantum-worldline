"""Figure 4: Power-law force profile from SIM-2026-011 (scipy curve_fit)."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

with open("D:/quantum-worldline/research/data/simulations/SIM-2026-011-interaction.json") as f:
    d = json.load(f)

dr = np.array(d['dr_values'], dtype=float)
F = np.array([d['F_interaction_avg'][str(i)] for i in d['dr_values']])
L_ADS = 1.0 / np.log(2)

mask = dr >= 2
def pl(x, A, a): return A * x**(-a)
popt, pcov = curve_fit(pl, dr[mask], -F[mask], p0=[8.0, 4.0])
A, alpha = popt; dalpha = np.sqrt(pcov[1,1])

dr_fine = np.linspace(1.5, 12.5, 200)
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: log-log
ax1.loglog(dr, -F, 'o', color='#1565C0', markersize=8, zorder=5, label='|F(dr)| (exact 24q GS)')
ax1.loglog(dr_fine, pl(dr_fine, A, alpha), '-', color='#4CAF50', linewidth=2.5,
           label=f'Power-law: a={alpha:.2f}+/-{dalpha:.2f}', zorder=4)
ax1.loglog(dr_fine, pl(dr_fine, A, 4.0), '--', color='#FF9800', linewidth=1.5,
           label='Stress-tensor (a=4.0)', alpha=0.7)
ax1.loglog(dr_fine, pl(dr_fine, A, 2.0), ':', color='#F44336', linewidth=1.5,
           label='Scalar (a=2.0)', alpha=0.7)
ax1.set_xlabel('Boundary separation dr', fontsize=12)
ax1.set_ylabel('|F(dr)|', fontsize=12)
ax1.set_title('Force Profile (log-log)', fontsize=11, fontweight='bold')
ax1.legend(fontsize=9); ax1.grid(True, alpha=0.3, which='both')

# Right: linear with info box
ax2.plot(dr, F, 'o-', color='#1565C0', markersize=8, linewidth=2, label='F(dr)')
ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax2.set_xlabel('Boundary separation dr', fontsize=12)
ax2.set_ylabel('F(dr) (interaction energy)', fontsize=12)
ax2.set_title('Force Profile (linear)', fontsize=11, fontweight='bold')
txt = f'a = {alpha:.2f} +/- {dalpha:.2f}\nStress-tensor: 4.0\nScalar: 2.0\nl_AdS = {L_ADS:.3f}\n12/12 attractive'
ax2.text(0.55, 0.95, txt, transform=ax2.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round', facecolor='#FFF8E1', alpha=0.9, edgecolor='#F9A825'))
ax2.legend(fontsize=9); ax2.grid(True, alpha=0.3)

plt.suptitle('Figure 4: Power-Law Holographic Forces (SIM-2026-011)', fontsize=11, style='italic', y=1.02)
plt.tight_layout()
plt.savefig("D:/quantum-worldline/research/data/simulations/figure4_force_worldline.png",
            dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved. alpha={alpha:.4f}+/-{dalpha:.4f}")
