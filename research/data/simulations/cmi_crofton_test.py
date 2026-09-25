"""
CMI Crofton Test -- HYP-2026-012
==================================
Tests whether V(dr) = Crofton integral of PEE thread density.

Approach:
  1. Load exact 24q OBC TFIM ground state (from gs_24q_exact.npy).
  2. For each pair (i, j), compute CMI(A_i; A_j | complement) as proxy for
     thread density rho(i->j) in the MERA bulk.
  3. For each dr, sum CMI over all pairs with |i-j|=dr.
  4. Compare V_thread(dr) to SIM-2026-011 force profile.

CMI definition:
  CMI(i; j | L) = S(i,L) + S(j,L) - S(i,j,L) - S(L)
  where S(A) = -Tr(rho_A log rho_A) (von Neumann entropy of reduced state)

  For a pure state |psi>:
  CMI(i; j | L) = S_i + S_j - S_ij (when L is the remainder complement)
  This simplifies for the boundary-primary probe sites.

Thread density proxy (Lin 2501.10691):
  rho(i, j) = (1/2) * CMI(A_i; A_j | complement)

Crofton formula test:
  V_crofton(dr) = C * sum_{|i-j|=dr} rho(i,j)
  Compare to measured F(dr) from SIM-2026-011.

Author: computation-lead
Date:   2026-03-26
"""

import sys
import io
import numpy as np
import json
import time
from scipy import sparse
from scipy.sparse.linalg import eigsh

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Configuration ──────────────────────────────────────────────────────────────
NQ = 24
L_ADS = 1.0 / np.log(2)
GS_PATH = "D:/quantum-worldline/research/data/simulations/gs_24q_exact.npy"
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-013.json"

# Force data from SIM-2026-011 (dr=1..12)
DR_VALS = list(range(1, 13))
F_MEASURED = [-2.351692, -0.573691, -0.103168, -0.048784, -0.028201,
              -0.018006, -0.012185, -0.008544, -0.006114, -0.004410,
              -0.003164, -0.002222]

t0 = time.time()

# ── Load exact ground state ────────────────────────────────────────────────────
print("Loading exact 24q ground state...")
psi = np.load(GS_PATH)
print(f"  State shape: {psi.shape}, norm: {np.linalg.norm(psi):.8f}")

# ── Von Neumann entropy helper ─────────────────────────────────────────────────
def entropy_from_rdm(rdm):
    """Compute von Neumann entropy of reduced density matrix."""
    evals = np.linalg.eigvalsh(rdm)
    evals = evals[evals > 1e-15]
    return -np.sum(evals * np.log(evals))

def rdm_from_statevec(psi, subsys_sites, n_total):
    """
    Compute reduced density matrix for subsystem of sites.

    psi: statevector of length 2^n_total
    subsys_sites: list of site indices (0-indexed)
    Returns: rdm of shape (2^k, 2^k) where k = len(subsys_sites)
    """
    k = len(subsys_sites)
    psi_mat = psi.reshape([2] * n_total)

    # Move subsystem sites to front
    other_sites = [s for s in range(n_total) if s not in subsys_sites]
    perm = list(subsys_sites) + other_sites
    psi_perm = np.transpose(psi_mat, perm)
    psi_perm = psi_perm.reshape(2**k, 2**(n_total - k))

    # RDM = Tr_{complement}(|psi><psi|)
    rdm = psi_perm @ psi_perm.conj().T
    return rdm

def entropy_subsystem(psi, sites, n_total):
    """Von Neumann entropy of subsystem."""
    rdm = rdm_from_statevec(psi, sites, n_total)
    return entropy_from_rdm(rdm)

# ── CMI calculation ────────────────────────────────────────────────────────────
# CMI(i; j | L) where L = everything except i and j (pure state simplification)
# For pure state: CMI(i; j | rest) = S(i) + S(j) - S(i,j)
# This is the "mutual information" I(i:j) but computed more carefully

def cmi_pair(psi, i, j, n_total):
    """
    Compute CMI(A_i; A_j | L) = S_i + S_j - S_{ij}
    For pure state |psi>, this equals the mutual information I(i:j).
    """
    S_i = entropy_subsystem(psi, [i], n_total)
    S_j = entropy_subsystem(psi, [j], n_total)
    S_ij = entropy_subsystem(psi, [i, j], n_total)
    return S_i + S_j - S_ij  # = I(i:j) for pure state, but this is the correct CMI

print("\nComputing CMI(i,j) for all pairs with dr=1..12...")
print("(This may take a few minutes for 24 sites)")

# Precompute single-site entropies
print("  Computing single-site entropies...")
S_single = {}
for site in range(NQ):
    S_single[site] = entropy_subsystem(psi, [site], NQ)
    sys.stdout.flush()
print(f"  Done. S(site 0)={S_single[0]:.4f}, S(site 12)={S_single[12]:.4f}")

# Compute CMI for pairs at each dr value
# To keep runtime manageable: only compute for central region (sites 4..20)
# to avoid OBC edge effects (same strategy as SIM-2026-011)
SITE_MIN = 4
SITE_MAX = NQ - 4  # = 20

cmi_by_dr = {dr: [] for dr in DR_VALS}
pair_count = {dr: 0 for dr in DR_VALS}

print("  Computing two-site entropies for CMI...")
t_cmi_start = time.time()
for i in range(SITE_MIN, SITE_MAX):
    for dr in DR_VALS:
        j = i + dr
        if j < SITE_MAX:
            S_ij = entropy_subsystem(psi, [i, j], NQ)
            cmi = S_single[i] + S_single[j] - S_ij
            cmi_by_dr[dr].append(cmi)
            pair_count[dr] += 1
    if i % 4 == 0:
        elapsed = time.time() - t_cmi_start
        print(f"    Site {i}/{SITE_MAX}, elapsed {elapsed:.1f}s")
        sys.stdout.flush()

print(f"  CMI computation done in {time.time() - t_cmi_start:.1f}s")

# ── Thread density proxy ───────────────────────────────────────────────────────
# rho(i,j) = (1/2) * CMI(i; j | L)   (Lin 2501.10691 Eq. 4)
# V_thread(dr) = C * sum_{|i-j|=dr} rho(i,j) / n_pairs  [normalized per pair]

V_thread_raw = {}
V_thread_normalized = {}
print("\nThread density V_thread(dr):")
print(f"{'dr':>4} {'n_pairs':>8} {'CMI_avg':>10} {'V_thread':>12} {'F_meas':>12} {'ratio':>8}")
print("-" * 60)

for dr in DR_VALS:
    cmis = cmi_by_dr[dr]
    if len(cmis) == 0:
        V_thread_raw[dr] = 0.0
        V_thread_normalized[dr] = 0.0
        print(f"{dr:>4} {0:>8} {'N/A':>10} {'N/A':>12} {F_MEASURED[dr-1]:>12.6f} {'N/A':>8}")
        continue
    cmi_avg = np.mean(cmis)
    V_raw = 0.5 * cmi_avg
    V_thread_raw[dr] = float(V_raw)
    V_thread_normalized[dr] = float(-V_raw)  # sign: attractive force corresponds to positive CMI

    F_meas = F_MEASURED[dr - 1]
    ratio = V_raw / abs(F_meas) if F_meas != 0 else float('nan')
    print(f"{dr:>4} {len(cmis):>8} {cmi_avg:>10.6f} {V_raw:>12.6f} {F_meas:>12.6f} {ratio:>8.3f}")

sys.stdout.flush()

# ── Check correlation between V_thread and F_measured ─────────────────────────
dr_for_fit = [dr for dr in DR_VALS if cmi_by_dr[dr]]
V_thread_arr = np.array([V_thread_raw[dr] for dr in dr_for_fit])
F_meas_arr = np.array([abs(F_MEASURED[dr-1]) for dr in dr_for_fit])

# Pearson correlation on log-log scale
log_V = np.log(V_thread_arr + 1e-20)
log_F = np.log(F_meas_arr)
correlation = np.corrcoef(log_V, log_F)[0, 1]

# Linear regression in log-log space: log(V_thread) = a + b*log(F_meas)
b_coeffs = np.polyfit(log_F, log_V, 1)
b_slope = b_coeffs[0]
b_intercept = b_coeffs[1]

print(f"\nLog-log correlation between V_thread and |F_meas|: {correlation:.4f}")
print(f"Log-log regression: log(V_thread) = {b_slope:.3f}*log(|F|) + {b_intercept:.3f}")
print(f"  Slope=1.0 would mean V_thread proportional to F_meas (Crofton confirmed)")
print(f"  Slope={b_slope:.3f} (deviation from proportionality)")

# Power-law fit of V_thread vs dr
from scipy.optimize import curve_fit

def powerlaw(x, A, alpha):
    return A * x**(-alpha)

dr_arr = np.array(dr_for_fit, dtype=float)
try:
    popt_thread, pcov_thread = curve_fit(powerlaw, dr_arr[1:], V_thread_arr[1:],
                                          p0=[0.5, 2.0], maxfev=2000)
    alpha_thread = popt_thread[1]
    A_thread = popt_thread[0]
    dalpha_thread = np.sqrt(pcov_thread[1, 1])
    print(f"\nPower-law fit of V_thread(dr>=2): alpha={alpha_thread:.3f} +/- {dalpha_thread:.3f}")
    print(f"  Compare to F_measured alpha=3.92 +/- 0.16")
    print(f"  Difference: {abs(alpha_thread - 3.92):.3f} (expected ~0 if Crofton holds)")
except Exception as e:
    alpha_thread = None
    A_thread = None
    dalpha_thread = None
    print(f"Power-law fit failed: {e}")

# ── Crofton integral prediction ────────────────────────────────────────────────
# Pure AdS2 prediction: V_crofton(dr) = C * 1/dr^2 (alpha=2 from uniform thread density)
# Our MERA: alpha_thread from above; compare to alpha_F=3.92

print("\nCrofton formula assessment:")
print("-" * 40)
if alpha_thread is not None:
    delta_alpha = abs(alpha_thread - 3.922)
    if delta_alpha < 0.3:
        crofton_verdict = "SUPPORTED"
        print(f"  Thread density power law alpha={alpha_thread:.3f} matches F(dr) alpha=3.92")
        print(f"  -> Crofton formula SUPPORTED: V(dr) ~ thread density integral")
    elif delta_alpha < 1.0:
        crofton_verdict = "PARTIALLY_SUPPORTED"
        print(f"  Thread density power law alpha={alpha_thread:.3f} deviates by {delta_alpha:.3f}")
        print(f"  -> Crofton formula PARTIALLY SUPPORTED")
    else:
        crofton_verdict = "NOT_SUPPORTED"
        print(f"  Thread density power law alpha={alpha_thread:.3f} differs by {delta_alpha:.3f} from F alpha=3.92")
        print(f"  -> Crofton formula NOT SUPPORTED at this level")
        print(f"  -> CMI proxy may differ from true PEE thread density")
else:
    crofton_verdict = "INCONCLUSIVE"

# ── Save Results ───────────────────────────────────────────────────────────────
runtime = time.time() - t0
output = {
    "id": "SIM-2026-013",
    "date": "2026-03-26",
    "description": "CMI Crofton test: does V(dr) = Crofton integral of PEE thread density? Tests HYP-2026-012.",
    "hypothesis": "HYP-2026-012",
    "type": "cmi_analysis",
    "hardware": "local_cpu",
    "n_qubits": NQ,
    "ground_state_source": "gs_24q_exact.npy (SIM-2026-011)",
    "site_range": [SITE_MIN, SITE_MAX],
    "cmi_by_dr": {str(dr): float(np.mean(cmi_by_dr[dr])) if cmi_by_dr[dr] else None
                  for dr in DR_VALS},
    "V_thread_by_dr": {str(dr): V_thread_raw[dr] for dr in DR_VALS},
    "F_measured_by_dr": {str(dr): F_MEASURED[dr-1] for dr in DR_VALS},
    "correlation_loglog": float(correlation),
    "regression_slope_loglog": float(b_slope),
    "alpha_thread": float(alpha_thread) if alpha_thread is not None else None,
    "alpha_F_measured": 3.9218,
    "dalpha_thread": float(dalpha_thread) if dalpha_thread is not None else None,
    "crofton_verdict": crofton_verdict,
    "runtime_s": float(runtime),
    "status": "COMPLETE"
}

with open(OUT_PATH, 'w') as f:
    json.dump(output, f, indent=2)

print(f"\nSaved to {OUT_PATH}")
print(f"Total runtime: {runtime:.1f}s")
print(f"\nHYP-2026-012 verdict: {crofton_verdict}")
