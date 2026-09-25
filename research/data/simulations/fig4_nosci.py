"""Figure 4: Power-law force profile (no scipy dependency)."""
import json, numpy as np
import matplotlib; matplotlib.use('Agg')
import matplotlib.pyplot as plt

with open("D:/quantum-worldline/research/data/simulations/SIM-2026-011-interaction.json") as f:
    d = json.load(f)

dr = np.array(d['dr_values'], dtype=float)
F = np.array([d['F_interaction_avg'][str(i)] for i in d['dr_values']])
L_ADS = 1.0 / np.log(2)

# Power-law fit via linear regression on log-log (dr>=2)
mask = dr >= 2
log_dr = np.log(dr[mask])
log_F = np.log(-F[mask])  # F<0, so -F>0
slope, intercept = np.polyfit(log_dr, log_F, 1)
alpha = -slope  # F ~ dr^{-alpha} => log(-F) = log(A) - alpha*log(dr)
A_fit = np.exp(intercept)
dr_fine = np.linspace(1.5, 12.5, 200)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Left: log-log
ax1.loglog(dr, -F, 'o', color='#1565C0', markersize=8, label=f'|F(dr)| (exact 24q GS)', zorder=5)
ax1.loglog(dr_fine, A_fit * dr_fine**(-alpha), '-', color='#4CAF50', linewidth=2.5,
           label=f'Fit: alpha={alpha:.2f} (stress-tensor=4.0)', zorder=4)
ax1.loglog(dr_fine, A_fit * dr_fine**(-4.0), '--', color='#FF9800', linewidth=1.5,
           label='alpha=4.0 (stress-tensor)', alpha=0.7, zorder=3)
ax1.loglog(dr_fine, A_fit * dr_fine**(-2.0), ':', color='#F44336', linewidth=1.5,
           label='alpha=2.0 (scalar)', alpha=0.7, zorder=3)
ax1.set_xlabel('Boundary separation dr', fontsize=12)
ax1.set_ylabel('|F(dr)|', fontsize=12)
ax1.set_title('Force Profile (log-log)', fontsize=11, fontweight='bold')
ax1.legend(fontsize=9)
ax1.grid(True, alpha=0.3, which='both')

# Right: linear
ax2.plot(dr, F, 'o-', color='#1565C0', markersize=8, linewidth=2, label='F(dr)')
ax2.axhline(y=0, color='gray', linestyle='-', alpha=0.3)
ax2.set_xlabel('Boundary separation dr', fontsize=12)
ax2.set_ylabel('F(dr) (interaction energy)', fontsize=12)
ax2.set_title('Force Profile (linear)', fontsize=11, fontweight='bold')
txt = f"alpha = {alpha:.2f}\nStress-tensor: 4.0\nScalar: 2.0\nl_AdS = {L_ADS:.3f}\n12/12 attractive"
ax2.text(0.55, 0.95, txt, transform=ax2.transAxes, fontsize=10, va='top',
         bbox=dict(boxstyle='round', facecolor='#FFF8E1', alpha=0.9, edgecolor='#F9A825'))
ax2.legend(fontsize=9)
ax2.grid(True, alpha=0.3)

plt.suptitle('Figure 4: Power-Law Holographic Forces (SIM-2026-011)', fontsize=11, style='italic', y=1.02)
plt.tight_layout()
plt.savefig("D:/quantum-worldline/research/data/simulations/figure4_force_worldline.png",
            dpi=150, bbox_inches='tight', facecolor='white')
print(f"Saved. alpha={alpha:.4f}")
