"""
DeWitt Supermetric Correction Test

Hypothesis (from Roux superspace analysis):
The DeWitt supermetric on superspace contributes a correction factor of chi
(MERA bond dimension) to geodesic distances. For chi=2 (binary MERA),
effective geodesic distance = r_geod / chi = r_geod / 2.

Test: if we rescale the worldline MC geodesic distances by 1/chi=0.5,
does the resulting decay length xi match the MERA xi=2.154?

Also tests ghost contribution factor of 1.4x (from Lee-Yang ghosts in
Roux Eq. 33), giving total correction chi * ghost = 2 * 1.4 = 2.8.
"""

import numpy as np
import json
from scipy.integrate import quad

# Parameters from worldline MC
l_AdS = 1.443
m = 1.0
chi = 2  # binary MERA bond dimension

# MERA data from SIM-2026-002
V_dr1 = -0.01140
V_dr2 = -0.00717
xi_mera_2pt = -1.0 / np.log(abs(V_dr2 / V_dr1))  # = 2.154

# Camporesi-Higuchi heat kernel on H^2
def heat_kernel_H2(r, T, l):
    """Exact heat kernel on H^2 with curvature radius l."""
    if T <= 0 or r < 0:
        return 0.0
    rho = r / l  # dimensionless geodesic distance
    tau = T / l**2  # dimensionless proper time
    prefactor = np.sqrt(2) / (4 * np.pi * tau)**1.5
    if rho < 1e-10:
        # r->0 limit: rho/sinh(rho) -> 1
        return prefactor * np.exp(-tau / 4)
    exp_arg = -rho**2 / (4 * tau) - tau / 4
    if exp_arg < -700:
        return 0.0
    return prefactor * (rho / np.sinh(rho)) * np.exp(exp_arg)

def propagator(r, l, m, T_max=50.0):
    """Bulk-to-bulk propagator G(r) = int_0^infty dT K(r,T) exp(-m^2 T/4)."""
    def integrand(T):
        K = heat_kernel_H2(r, T, l)
        return K * np.exp(-m**2 * T / 4)
    result, _ = quad(integrand, 0.01, T_max, limit=200)
    return result

print("=" * 60)
print("DeWitt Supermetric Correction Test")
print("=" * 60)
print(f"\nl_AdS = {l_AdS}, m = {m}, chi = {chi}")
print(f"MERA xi_2pt = {xi_mera_2pt:.4f}")

# --- Test 1: Original worldline MC (no correction) ---
print("\n--- Original (no correction) ---")
dr_vals = [1, 2, 3, 4, 5]
log_G_original = []
for dr in dr_vals:
    r = dr * l_AdS  # geodesic distance
    G = propagator(r, l_AdS, m)
    log_G = np.log(G) if G > 0 else -999
    log_G_original.append(log_G)
    print(f"  dr={dr}  r_geod={r:.3f}  log G = {log_G:.4f}")

# Fit xi from consecutive ratios
xi_orig = -1.0 / ((log_G_original[1] - log_G_original[0]) / l_AdS)
print(f"  xi_original (dr=1,2) = {xi_orig:.4f}")

# --- Test 2: DeWitt correction (r_eff = r / chi) ---
print("\n--- DeWitt correction: r_eff = r / chi ---")
log_G_dewitt = []
for dr in dr_vals:
    r_eff = dr * l_AdS / chi  # rescaled geodesic distance
    G = propagator(r_eff, l_AdS, m)
    log_G = np.log(G) if G > 0 else -999
    log_G_dewitt.append(log_G)
    print(f"  dr={dr}  r_eff={r_eff:.3f}  log G = {log_G:.4f}")

xi_dewitt = -1.0 / ((log_G_dewitt[1] - log_G_dewitt[0]) / (l_AdS / chi))
print(f"  xi_dewitt (dr=1,2) = {xi_dewitt:.4f}")
print(f"  Ratio xi_dewitt / xi_mera = {xi_dewitt / xi_mera_2pt:.4f}")

# --- Test 3: DeWitt + ghost correction (r_eff = r / (chi * 1.4)) ---
ghost_factor = 1.4
total_correction = chi * ghost_factor
print(f"\n--- DeWitt + ghost correction: r_eff = r / {total_correction} ---")
log_G_full = []
for dr in dr_vals:
    r_eff = dr * l_AdS / total_correction
    G = propagator(r_eff, l_AdS, m)
    log_G = np.log(G) if G > 0 else -999
    log_G_full.append(log_G)
    print(f"  dr={dr}  r_eff={r_eff:.3f}  log G = {log_G:.4f}")

xi_full = -1.0 / ((log_G_full[1] - log_G_full[0]) / (l_AdS / total_correction))
print(f"  xi_full (dr=1,2) = {xi_full:.4f}")
print(f"  Ratio xi_full / xi_mera = {xi_full / xi_mera_2pt:.4f}")

# --- Test 4: What correction factor gives exact match? ---
print("\n--- Best-fit correction factor ---")
# We want xi_corrected = xi_mera_2pt = 2.154
# xi_corrected = -1 / (d(log G)/dr_eff) where dr_eff = dr * l_AdS / alpha
# Scan alpha to find match
best_alpha = None
best_diff = 999
for alpha in np.linspace(0.5, 5.0, 500):
    r1 = 1 * l_AdS / alpha
    r2 = 2 * l_AdS / alpha
    G1 = propagator(r1, l_AdS, m)
    G2 = propagator(r2, l_AdS, m)
    if G1 > 0 and G2 > 0:
        xi_test = -1.0 / ((np.log(G2) - np.log(G1)) / (l_AdS / alpha))
        diff = abs(xi_test - xi_mera_2pt)
        if diff < best_diff:
            best_diff = diff
            best_alpha = alpha
            best_xi = xi_test

print(f"  Best alpha = {best_alpha:.4f}")
print(f"  xi at best alpha = {best_xi:.4f}")
print(f"  Predicted: chi * ghost = {best_alpha:.2f}")
print(f"  If chi=2: ghost_factor = {best_alpha/2:.3f}")

# --- Summary ---
print("\n" + "=" * 60)
print("SUMMARY")
print("=" * 60)
print(f"  MERA xi_2pt:            {xi_mera_2pt:.4f}")
print(f"  Worldline (no corr):    {xi_orig:.4f}  (ratio: {xi_orig/xi_mera_2pt:.3f})")
print(f"  DeWitt (chi=2):         {xi_dewitt:.4f}  (ratio: {xi_dewitt/xi_mera_2pt:.3f})")
print(f"  DeWitt+ghost (2.8x):    {xi_full:.4f}  (ratio: {xi_full/xi_mera_2pt:.3f})")
print(f"  Best-fit alpha:         {best_alpha:.4f}")

verdict = "RESOLVED" if abs(best_alpha - total_correction) / total_correction < 0.15 else "PARTIAL"
print(f"\n  Verdict: {verdict}")
if verdict == "RESOLVED":
    print(f"  The DeWitt + ghost correction (alpha={total_correction}) matches within 15%")
else:
    print(f"  The best-fit alpha ({best_alpha:.2f}) differs from chi*ghost ({total_correction:.1f})")
    print(f"  Additional physics needed to explain the gap")

# Save results
results = {
    "test": "DeWitt supermetric correction",
    "hypothesis": "Roux PAPER-2026-023 predicts r_eff = r_geod / (chi * ghost_factor)",
    "parameters": {
        "l_AdS": l_AdS,
        "m": m,
        "chi": chi,
        "ghost_factor": ghost_factor,
        "total_correction": total_correction
    },
    "results": {
        "xi_mera_2pt": xi_mera_2pt,
        "xi_original": xi_orig,
        "xi_dewitt_chi2": xi_dewitt,
        "xi_dewitt_plus_ghost": xi_full,
        "best_fit_alpha": best_alpha,
        "ratio_original": xi_orig / xi_mera_2pt,
        "ratio_dewitt": xi_dewitt / xi_mera_2pt,
        "ratio_full": xi_full / xi_mera_2pt,
    },
    "verdict": verdict
}

with open("D:/quantum-worldline/research/data/simulations/dewitt_correction_results.json", "w") as f:
    json.dump(results, f, indent=2)
print(f"\nResults saved to dewitt_correction_results.json")
