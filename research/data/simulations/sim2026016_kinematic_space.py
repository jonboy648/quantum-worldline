"""
SIM-2026-016: Kinematic Space and Crofton Integral from 24q Exact Ground State
================================================================================
Tests the theory-researcher's prediction (task5-crofton-derivation.md):
  sigma_MERA(dr) = Crofton integral of S''(u,v) ~ 2*log(dr)
  F(dr) ~ exp(-Delta_T * sigma) = dr^{-2*Delta_T} = dr^{-4}

Key distinction from SIM-2026-013 (cmi_crofton_test.py):
  SIM-2026-013 tested raw CMI ~ force (HYP-012, found NOT_SUPPORTED)
  This test computes the KINEMATIC SPACE metric from S''(u,v) and the
  Crofton integral (geodesic length) from that metric.

Czech et al. 1505.05515 formulas:
  - Kinematic space metric: ds^2 = -(d^2 S / du dv) du dv
  - Crofton form: omega(u,v) = (1/2) * d^2 S(u,v) / du dv
  - Geodesic length: sigma(x1,x2) = integral of omega over geodesics
    connecting boundary points x1, x2
  - For CFT: S(u,v) = (c/3)*log|v-u| + const
    => d^2S/dudv = -(c/3)/(v-u)^2
    => sigma(x1,x2) = integral ~ 2*log|x2-x1| (for c>>1)

For our MERA (c=1/2): compute S(u,v) numerically for all contiguous
intervals [u, v] of the 24-site OBC chain, then:
  1. Build the discrete kinematic space matrix K[u,v] = d^2S/dudv
  2. Compute sigma_MERA(dr) via discrete Crofton sum
  3. Check sigma ~ 2*log(dr)
  4. Compute F_predicted(dr) = A * exp(-Delta_T * sigma)
  5. Compare to measured F(dr) from SIM-2026-011
"""
import sys
import io
import numpy as np
import json
import time
from scipy.optimize import curve_fit

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ================================================================
# Configuration
# ================================================================
NQ = 24
GS_PATH = "D:/quantum-worldline/research/data/simulations/gs_24q_exact.npy"
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-016.json"

# Force data from SIM-2026-011 (dr=1..12)
DR_VALS = list(range(1, 13))
F_MEASURED = [-2.351692, -0.573691, -0.103168, -0.048784, -0.028201,
              -0.018006, -0.012185, -0.008544, -0.006114, -0.004410,
              -0.003164, -0.002222]

DELTA_T = 2.0  # stress tensor scaling dimension in 2D Ising CFT
C_CFT = 0.5    # central charge

t0 = time.time()

# ================================================================
# Load ground state
# ================================================================
print("=" * 65)
print("SIM-2026-016: Kinematic Space Crofton Integral (24q)")
print("=" * 65)

print("\nLoading exact 24q ground state...")
psi = np.load(GS_PATH)
print(f"  Shape: {psi.shape}, norm: {np.linalg.norm(psi):.8f}")

# ================================================================
# Compute entanglement entropy for ALL contiguous intervals
# ================================================================
# S(u, v) = entropy of interval [u, v] (0-indexed, inclusive)
# For OBC chain of N sites: u in [0, N-1], v in [u, N-1]

print("\nComputing S(u,v) for all contiguous intervals...")
t_ent = time.time()

# S_interval[u][v] = S(sites u through v inclusive)
S_interval = np.full((NQ, NQ), np.nan)

psi_tensor = psi.reshape([2] * NQ)

for u in range(NQ):
    for v in range(u, NQ):
        l = v - u + 1  # number of sites in interval
        if l == NQ:
            S_interval[u][v] = 0.0  # full system is pure
            continue

        # For pure states: S(A) = S(complement of A)
        # Use whichever is smaller to keep RDM tractable
        l_eff = min(l, NQ - l)
        if l_eff == l:
            # Trace out complement: RDM is 2^l x 2^l
            sites_in = list(range(u, v + 1))
        else:
            # Use complement (smaller): RDM is 2^(N-l) x 2^(N-l)
            sites_in = [s for s in range(NQ) if s < u or s > v]

        sites_out = [s for s in range(NQ) if s not in sites_in]
        perm = sites_in + sites_out
        psi_perm = np.transpose(psi_tensor, perm)
        d_in = 2 ** len(sites_in)
        d_out = 2 ** len(sites_out)
        psi_mat = psi_perm.reshape(d_in, d_out)
        rdm = psi_mat @ psi_mat.conj().T
        evals = np.linalg.eigvalsh(rdm)
        evals = evals[evals > 1e-15]
        S_interval[u][v] = float(-np.sum(evals * np.log(evals)))

    if u % 6 == 0:
        print(f"  u={u}/{NQ-1}, elapsed {time.time()-t_ent:.1f}s", flush=True)
        sys.stdout.flush()

print(f"  Done in {time.time()-t_ent:.1f}s")

# Verify: S(0, l-1) should match known entanglement entropy
print("\n  Verification: S(0, l-1) for l=1..6:")
for l in range(1, 7):
    print(f"    S(0,{l-1}) = {S_interval[0][l-1]:.4f}")

# ================================================================
# Build discrete kinematic space: K[u,v] = d^2 S / du dv
# ================================================================
# Discrete second derivative: K[u,v] = S(u+1,v) + S(u,v-1) - S(u,v) - S(u+1,v-1)
# (finite difference approximation of mixed partial derivative)
# Valid for u >= 0, v <= N-2, u+1 < v (need at least 2 sites in interval)

print("\nBuilding discrete kinematic space K[u,v] = d^2S/dudv...")

K = np.full((NQ, NQ), np.nan)
for u in range(NQ - 2):
    for v in range(u + 2, NQ):
        # Need: S(u+1, v), S(u, v-1), S(u, v), S(u+1, v-1)
        s_up1_v = S_interval[u + 1][v] if u + 1 <= v else np.nan
        s_u_vm1 = S_interval[u][v - 1] if u <= v - 1 else np.nan
        s_uv = S_interval[u][v]
        s_up1_vm1 = S_interval[u + 1][v - 1] if u + 1 <= v - 1 else np.nan

        if not any(np.isnan([s_up1_v, s_u_vm1, s_uv, s_up1_vm1])):
            K[u][v] = s_up1_v + s_u_vm1 - s_uv - s_up1_vm1

# Print a sample of K values
print("\n  Sample K[u,v] values (should be negative for CFT):")
for u in [2, 4, 6]:
    for v in [u + 3, u + 6, u + 10]:
        if v < NQ and not np.isnan(K[u][v]):
            print(f"    K[{u},{v}] = {K[u][v]:.6f}  (interval length = {v-u+1})")

# ================================================================
# Crofton integral: geodesic length sigma(dr)
# ================================================================
# For two boundary points separated by dr sites:
#   sigma(dr) = sum over all intervals [u,v] that "straddle" the two points
#   weighted by |K[u,v]|
#
# In Czech et al.'s formulation: a geodesic between boundary points x1, x2
# intersects all geodesics (u,v) where u < x1 < x2 < v.
# The Crofton length: sigma(x1,x2) = sum_{u < x1, v > x2} |K[u,v]|
#
# For discrete MERA: anchor at site i, probe at site j = i + dr
# sigma(i, j) = sum_{u <= i, v >= j} |K[u,v]|

print("\nComputing Crofton geodesic length sigma(dr)...")

# Use central region to avoid edge effects
ANCHOR_MIN = 4
ANCHOR_MAX = NQ - 4 - max(DR_VALS)

sigma_by_dr = {}
sigma_cfT_pred = {}

print(f"\n  {'dr':>4}  {'sigma_avg':>12}  {'sigma_CFT':>12}  {'2*log(dr)':>12}  {'ratio':>8}")
print("  " + "-" * 55)

for dr in DR_VALS:
    sigmas = []
    for i in range(ANCHOR_MIN, min(ANCHOR_MAX + 1, NQ - dr)):
        j = i + dr
        if j >= NQ:
            continue
        # Sum |K[u,v]| over all u <= i and v >= j
        s = 0.0
        for u in range(i + 1):  # u <= i
            for v in range(j, NQ):  # v >= j
                if not np.isnan(K[u][v]):
                    s += abs(K[u][v])
        sigmas.append(s)

    if sigmas:
        sigma_avg = np.mean(sigmas)
        sigma_by_dr[dr] = float(sigma_avg)
        sigma_pred = 2.0 * np.log(dr) if dr > 0 else 0.0
        sigma_cfT_pred[dr] = sigma_pred
        ratio = sigma_avg / sigma_pred if sigma_pred > 0 else float('nan')
        print(f"  {dr:>4d}  {sigma_avg:>12.4f}  {sigma_pred:>12.4f}  "
              f"{sigma_pred:>12.4f}  {ratio:>8.3f}")
    else:
        sigma_by_dr[dr] = 0.0
        print(f"  {dr:>4d}  {'N/A':>12}")

# ================================================================
# Test: does sigma ~ 2*log(dr)?
# ================================================================
print("\nFitting sigma(dr) = a * log(dr) + b ...")

dr_fit = np.array([dr for dr in DR_VALS if dr >= 2 and dr in sigma_by_dr], dtype=float)
sigma_fit = np.array([sigma_by_dr[dr] for dr in dr_fit.astype(int)])

if len(dr_fit) >= 3:
    # Linear fit in (log(dr), sigma) space
    log_dr = np.log(dr_fit)
    coeffs = np.polyfit(log_dr, sigma_fit, 1)
    a_fit, b_fit = coeffs
    print(f"  sigma(dr) = {a_fit:.3f} * log(dr) + {b_fit:.3f}")
    print(f"  CFT prediction: sigma = 2.0 * log(dr) + const")
    print(f"  Coefficient ratio: {a_fit:.3f} / 2.0 = {a_fit/2.0:.3f}")
    sigma_log_coeff = float(a_fit)
else:
    print("  Too few points for fit")
    sigma_log_coeff = None

# ================================================================
# Predicted force from Crofton sigma
# ================================================================
# F_pred(dr) = A * exp(-Delta_T * sigma(dr))
# If sigma ~ a*log(dr): F_pred ~ dr^(-a*Delta_T)

print("\nForce prediction from Crofton integral:")
print(f"  F_pred(dr) = A * exp(-{DELTA_T} * sigma(dr))")
print(f"\n  {'dr':>4}  {'sigma':>10}  {'F_pred':>12}  {'F_meas':>12}  {'ratio':>8}")
print("  " + "-" * 50)

F_pred = {}
for dr in DR_VALS:
    if dr in sigma_by_dr and sigma_by_dr[dr] > 0:
        f_p = np.exp(-DELTA_T * sigma_by_dr[dr])
        F_pred[dr] = float(f_p)
        f_m = abs(F_MEASURED[dr - 1])
        ratio = f_p / f_m if f_m > 1e-15 else float('nan')
        print(f"  {dr:>4d}  {sigma_by_dr[dr]:>10.4f}  {f_p:>12.6e}  {f_m:>12.6e}  {ratio:>8.3f}")

# ================================================================
# Effective alpha from sigma-based force
# ================================================================
if sigma_log_coeff is not None:
    alpha_predicted = sigma_log_coeff * DELTA_T
    print(f"\n  Predicted alpha = a * Delta_T = {sigma_log_coeff:.3f} * {DELTA_T} = {alpha_predicted:.3f}")
    print(f"  Measured alpha from SIM-2026-011: 3.92 +/- 0.16")
    print(f"  Deviation: {abs(alpha_predicted - 3.92):.3f}")
else:
    alpha_predicted = None

# ================================================================
# Summary
# ================================================================
runtime = time.time() - t0
print(f"\n{'='*65}")
print(f"SIM-2026-016 SUMMARY")
print(f"{'='*65}")
if sigma_log_coeff is not None:
    print(f"  sigma(dr) = {sigma_log_coeff:.3f} * log(dr) + {b_fit:.3f}")
    print(f"  (CFT: 2.0 * log(dr))")
    print(f"  Predicted alpha = {alpha_predicted:.3f}")
    print(f"  Measured alpha  = 3.92 +/- 0.16")
    delta = abs(alpha_predicted - 3.92) if alpha_predicted else 99
    if delta < 0.5:
        verdict = "SUPPORTED"
    elif delta < 1.5:
        verdict = "PARTIAL"
    else:
        verdict = "NOT_SUPPORTED"
    print(f"  Kinematic space verdict: {verdict}")
else:
    verdict = "INCONCLUSIVE"
    print(f"  Insufficient data for verdict")
print(f"  Runtime: {runtime:.1f}s")

# Save
output = {
    "id": "SIM-2026-016",
    "description": "Kinematic space Crofton integral test (24q exact GS)",
    "hypothesis": "Direction 2 from research sprint (kinematic space / Crofton)",
    "n_qubits": NQ,
    "sigma_by_dr": {str(k): v for k, v in sigma_by_dr.items()},
    "sigma_log_coefficient": sigma_log_coeff,
    "sigma_CFT_prediction": 2.0,
    "alpha_predicted": float(alpha_predicted) if alpha_predicted else None,
    "alpha_measured": 3.92,
    "F_pred": {str(k): v for k, v in F_pred.items()},
    "F_measured": {str(dr): F_MEASURED[dr-1] for dr in DR_VALS},
    "verdict": verdict,
    "runtime_s": runtime,
    "status": "COMPLETE",
}
with open(OUT_PATH, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to {OUT_PATH}")
