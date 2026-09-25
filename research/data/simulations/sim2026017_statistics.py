"""
SIM-2026-017: Goodness-of-fit statistics for 24q force profile
===============================================================
1. Load F(dr) from SIM-2026-011-interaction.json (dr=1..12, use dr>=2)
2. Fit power-law and exponential models to |F(dr)| for dr>=2 (11 points)
3. Compute chi^2, reduced chi^2, AIC, BIC for each model
4. Bootstrap uncertainty: 1000 resamples of the 11 points, refit alpha
5. Anchor dependence: compute F(dr) at anchor=4,8,12 from cached 24q GS

Author: computation-lead
Date:   2026-04-07
"""
import sys
import io
import numpy as np
import time
import json
from scipy.optimize import curve_fit

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ============================================================================
# Configuration
# ============================================================================
NQ = 24
E0_EXPECTED = -30.199712
L_ADS = 1.0 / np.log(2)
ALPHA_BP = 0.635
BETA_BP = -0.026

SIM011_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-011-interaction.json"
GS_CACHE = "D:/quantum-worldline/research/data/simulations/gs_24q_exact.npy"
GS_E0_CACHE = "D:/quantum-worldline/research/data/simulations/gs_24q_E0.txt"
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-017-statistics.json"

# ============================================================================
# Fit models
# ============================================================================
def powerlaw_model(x, A, alpha):
    return A * np.power(np.array(x, dtype=float), -alpha)

def exp_model(x, B, xi):
    return B * np.exp(-np.array(x, dtype=float) / xi)

def fit_powerlaw(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    popt, pcov = curve_fit(powerlaw_model, x, y,
                           p0=[y[0] * 4, 3.0],
                           maxfev=20000,
                           bounds=([-1000, 0.01], [1000, 20]))
    perr = np.sqrt(np.diag(pcov))
    return popt, perr, pcov

def fit_exponential(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    popt, pcov = curve_fit(exp_model, x, y,
                           p0=[y[0] * 2, 1.5],
                           maxfev=20000,
                           bounds=([-1000, 0.01], [1000, 50]))
    perr = np.sqrt(np.diag(pcov))
    return popt, perr, pcov

# ============================================================================
# Statistics helpers
# ============================================================================
def compute_stats(dr_arr, obs, model_func, popt, n_params):
    """Compute chi^2, reduced chi^2, AIC, BIC."""
    x = np.array(dr_arr, dtype=float)
    y_obs = np.array(obs, dtype=float)
    y_pred = model_func(x, *popt)
    n = len(x)
    p = n_params

    # Chi-squared: sum (obs - pred)^2 / pred^2
    chi2 = float(np.sum((y_obs - y_pred) ** 2 / y_pred ** 2))
    chi2_reduced = chi2 / (n - p)

    # RSS for AIC/BIC
    rss = float(np.sum((y_obs - y_pred) ** 2))
    aic = n * np.log(rss / n) + 2 * p
    bic = n * np.log(rss / n) + p * np.log(n)

    # Also compute standard residual statistics
    residuals = y_obs - y_pred
    max_resid = float(np.max(np.abs(residuals)))
    rms_resid = float(np.sqrt(np.mean(residuals ** 2)))

    return {
        "chi2": float(chi2),
        "chi2_reduced": float(chi2_reduced),
        "AIC": float(aic),
        "BIC": float(bic),
        "RSS": float(rss),
        "n_points": n,
        "n_params": p,
        "dof": n - p,
        "max_abs_residual": max_resid,
        "rms_residual": rms_resid
    }

# ============================================================================
# Matrix-free Hamiltonian (from interaction_energy_24q.py)
# ============================================================================
from scipy.sparse.linalg import LinearOperator

def build_tfim_linop(n):
    dim = 1 << n
    basis = np.arange(dim, dtype=np.int64)
    diag_zz = np.zeros(dim, dtype=np.float64)
    for i in range(n - 1):
        bit_i = (basis >> i) & 1
        bit_ip1 = (basis >> (i + 1)) & 1
        zz_val = 1 - 2 * (bit_i ^ bit_ip1)
        diag_zz -= zz_val
    flip_indices = [(1 << i) for i in range(n)]

    def matvec(v):
        out = diag_zz * v
        for mask in flip_indices:
            out[basis ^ mask] += -v
        return out

    H_op = LinearOperator((dim, dim), matvec=matvec, dtype=np.float64)
    return H_op, diag_zz

def apply_bp_operator(n, j, sv):
    dim = 1 << n
    out = np.zeros(dim, dtype=np.float64)
    idx = np.arange(dim, dtype=np.int64)
    mask_j = np.int64(1 << j)
    mask_jp1 = np.int64(1 << (j + 1))
    flip_j = idx ^ mask_j
    flip_jp1 = idx ^ mask_jp1
    z_j = 1.0 - 2.0 * ((idx >> j) & 1).astype(np.float64)
    z_jp1 = 1.0 - 2.0 * ((idx >> (j + 1)) & 1).astype(np.float64)

    out += ALPHA_BP * sv[flip_j]
    out += ALPHA_BP * sv[flip_jp1]
    tmp = BETA_BP * z_jp1 * sv
    out[flip_j] += tmp
    tmp2 = BETA_BP * z_j * sv
    out[flip_jp1] += tmp2
    return out

def energy_of_state(sv, H):
    return float(sv @ (H @ sv))

def compute_force_profile(gs, H, anchor, n_qubits, dr_max):
    """Compute F(dr) for dr=1..dr_max at given anchor."""
    E0 = energy_of_state(gs, H)

    valid_drs = [dr for dr in range(1, dr_max + 1) if anchor + dr + 1 < n_qubits]

    # Single excitation at anchor
    sv_a = apply_bp_operator(n_qubits, anchor, gs)
    norm_a = float(np.linalg.norm(sv_a))
    sv_a = sv_a / norm_a
    E_single_a = energy_of_state(sv_a, H)
    dE_a = E_single_a - E0

    F_values = {}
    for dr in valid_drs:
        j = anchor + dr
        # Single at probe
        sv_p = apply_bp_operator(n_qubits, j, gs)
        norm_p = float(np.linalg.norm(sv_p))
        if norm_p < 1e-12:
            continue
        sv_p = sv_p / norm_p
        E_single_p = energy_of_state(sv_p, H)
        dE_p = E_single_p - E0

        # Dual: anchor then probe
        sv_after_a = apply_bp_operator(n_qubits, anchor, gs)
        sv_dual = apply_bp_operator(n_qubits, j, sv_after_a)
        norm_d = float(np.linalg.norm(sv_dual))
        if norm_d < 1e-12:
            continue
        sv_dual = sv_dual / norm_d
        E_dual = energy_of_state(sv_dual, H)

        F = E_dual - E0 - dE_a - dE_p
        F_values[dr] = float(F)

    return F_values, E0

# ============================================================================
# Main
# ============================================================================
def main():
    print("=" * 72)
    print("SIM-2026-017: Goodness-of-fit statistics for 24q force profile")
    print("=" * 72)
    t_global = time.time()

    # ── Load SIM-2026-011 data ────────────────────────────────────────────
    print("\n[1/5] Loading force profile from SIM-2026-011...")
    with open(SIM011_PATH, 'r') as f:
        sim011 = json.load(f)

    F_raw = sim011["F_interaction_avg"]
    all_drs = sorted([int(k) for k in F_raw.keys()])
    all_F = [float(F_raw[str(dr)]) for dr in all_drs]

    print(f"  Loaded {len(all_drs)} F(dr) values: dr = {all_drs}")
    print(f"  Anchor = {sim011['anchor']}")

    # Use dr >= 2 (skip nearest-neighbor boundary artifact)
    mask_ge2 = [i for i, dr in enumerate(all_drs) if dr >= 2]
    dr_fit = [all_drs[i] for i in mask_ge2]
    F_fit = [all_F[i] for i in mask_ge2]
    n_pts = len(dr_fit)

    print(f"  Using dr >= 2: {n_pts} points")
    print(f"  dr = {dr_fit}")
    print(f"  F  = {['%.6e' % v for v in F_fit]}")

    # ── Fit both models ───────────────────────────────────────────────────
    print("\n[2/5] Fitting power-law and exponential models...")

    # Power-law: F = A * dr^{-alpha}
    popt_pl, perr_pl, pcov_pl = fit_powerlaw(dr_fit, F_fit)
    A_pl, alpha_pl = popt_pl
    dA_pl, dalpha_pl = perr_pl
    print(f"  Power-law:    A = {A_pl:.6f} +/- {dA_pl:.4f}")
    print(f"                alpha = {alpha_pl:.4f} +/- {dalpha_pl:.4f}")

    # Exponential: F = B * exp(-dr/xi)
    popt_exp, perr_exp, pcov_exp = fit_exponential(dr_fit, F_fit)
    B_exp, xi_exp = popt_exp
    dB_exp, dxi_exp = perr_exp
    print(f"  Exponential:  B = {B_exp:.6f} +/- {dB_exp:.4f}")
    print(f"                xi = {xi_exp:.4f} +/- {dxi_exp:.4f}")

    # ── Compute statistics ────────────────────────────────────────────────
    print("\n[3/5] Computing goodness-of-fit statistics...")

    stats_pl = compute_stats(dr_fit, F_fit, powerlaw_model, popt_pl, n_params=2)
    stats_exp = compute_stats(dr_fit, F_fit, exp_model, popt_exp, n_params=2)

    print(f"\n  {'Metric':<20}  {'Power-law':>14}  {'Exponential':>14}")
    print(f"  {'-'*20}  {'-'*14}  {'-'*14}")
    for key in ["chi2", "chi2_reduced", "AIC", "BIC", "RSS", "rms_residual"]:
        v_pl = stats_pl[key]
        v_exp = stats_exp[key]
        print(f"  {key:<20}  {v_pl:>14.6f}  {v_exp:>14.6f}")

    # Delta AIC / BIC
    delta_aic = stats_exp["AIC"] - stats_pl["AIC"]
    delta_bic = stats_exp["BIC"] - stats_pl["BIC"]
    print(f"\n  Delta AIC (exp - pl) = {delta_aic:+.4f}")
    print(f"  Delta BIC (exp - pl) = {delta_bic:+.4f}")
    if delta_aic > 0:
        print(f"  --> Power-law PREFERRED by AIC (lower is better)")
    else:
        print(f"  --> Exponential PREFERRED by AIC (lower is better)")
    if delta_bic > 0:
        print(f"  --> Power-law PREFERRED by BIC")
    else:
        print(f"  --> Exponential PREFERRED by BIC")

    # ── Bootstrap ─────────────────────────────────────────────────────────
    print("\n[4/5] Bootstrap uncertainty (1000 resamples)...")
    np.random.seed(42)
    n_boot = 1000
    alpha_boot = []
    A_boot = []
    dr_arr = np.array(dr_fit, dtype=float)
    F_arr = np.array(F_fit, dtype=float)

    n_failed = 0
    for b in range(n_boot):
        idx = np.random.choice(n_pts, size=n_pts, replace=True)
        dr_b = dr_arr[idx]
        F_b = F_arr[idx]
        try:
            popt_b, _ = curve_fit(powerlaw_model, dr_b, F_b,
                                  p0=[A_pl, alpha_pl],
                                  maxfev=10000,
                                  bounds=([-1000, 0.01], [1000, 20]))
            alpha_boot.append(popt_b[1])
            A_boot.append(popt_b[0])
        except Exception:
            n_failed += 1

    alpha_boot = np.array(alpha_boot)
    A_boot = np.array(A_boot)
    n_success = len(alpha_boot)

    alpha_mean = float(np.mean(alpha_boot))
    alpha_std = float(np.std(alpha_boot, ddof=1))
    alpha_median = float(np.median(alpha_boot))
    alpha_ci_lo = float(np.percentile(alpha_boot, 2.5))
    alpha_ci_hi = float(np.percentile(alpha_boot, 97.5))

    print(f"  Bootstrap samples: {n_success}/{n_boot} succeeded ({n_failed} failed)")
    print(f"  alpha: mean = {alpha_mean:.4f}, std = {alpha_std:.4f}")
    print(f"         median = {alpha_median:.4f}")
    print(f"         95% CI = [{alpha_ci_lo:.4f}, {alpha_ci_hi:.4f}]")
    print(f"  Stress-tensor prediction (alpha=4.0) within 95% CI: "
          f"{'YES' if alpha_ci_lo <= 4.0 <= alpha_ci_hi else 'NO'}")

    bootstrap_results = {
        "n_resamples": n_boot,
        "n_success": n_success,
        "n_failed": n_failed,
        "alpha_mean": alpha_mean,
        "alpha_std": alpha_std,
        "alpha_median": alpha_median,
        "alpha_95CI_lo": alpha_ci_lo,
        "alpha_95CI_hi": alpha_ci_hi,
        "stress_tensor_in_CI": bool(alpha_ci_lo <= 4.0 <= alpha_ci_hi),
        "A_mean": float(np.mean(A_boot)),
        "A_std": float(np.std(A_boot, ddof=1))
    }

    # ── Anchor dependence ─────────────────────────────────────────────────
    print("\n[5/5] Anchor dependence test...")
    print("  Loading 24q ground state from cache...")
    sys.stdout.flush()

    gs = np.load(GS_CACHE)
    with open(GS_E0_CACHE, 'r') as f:
        E0_cached = float(f.read().strip())
    print(f"  E0 = {E0_cached:.8f}  (expected {E0_EXPECTED})")

    print("  Building Hamiltonian LinearOperator...")
    sys.stdout.flush()
    H_op, diag_zz = build_tfim_linop(NQ)

    # Verify E0
    E0_check = energy_of_state(gs, H_op)
    print(f"  <GS|H|GS> = {E0_check:.8f}")
    assert abs(E0_check - E0_cached) < 0.001, f"E0 mismatch: {E0_check} vs {E0_cached}"

    anchors_to_test = [4, 6, 8, 12]
    anchor_results = {}

    for anchor in anchors_to_test:
        print(f"\n  --- Anchor = {anchor} ---")
        sys.stdout.flush()
        t_anc = time.time()

        F_anc, E0_anc = compute_force_profile(gs, H_op, anchor, NQ, dr_max=12)

        drs_a = sorted(F_anc.keys())
        drs_ge2 = [dr for dr in drs_a if dr >= 2]
        Fs_ge2 = [F_anc[dr] for dr in drs_ge2]

        if len(drs_ge2) < 3:
            print(f"    Only {len(drs_ge2)} points for dr>=2 -- too few for fit")
            anchor_results[str(anchor)] = {
                "n_points": len(drs_ge2),
                "dr_values": drs_ge2,
                "F_values": {str(k): v for k, v in F_anc.items()},
                "fit_failed": True
            }
            continue

        try:
            popt_a, perr_a, _ = fit_powerlaw(drs_ge2, Fs_ge2)
            A_a, alpha_a = popt_a
            dA_a, dalpha_a = perr_a
            stats_a = compute_stats(drs_ge2, Fs_ge2, powerlaw_model, popt_a, n_params=2)

            print(f"    n_points = {len(drs_ge2)}, dr = {drs_ge2}")
            print(f"    alpha = {alpha_a:.4f} +/- {dalpha_a:.4f}")
            print(f"    chi2_reduced = {stats_a['chi2_reduced']:.6f}")
            print(f"    elapsed = {time.time()-t_anc:.1f}s")

            anchor_results[str(anchor)] = {
                "n_points": len(drs_ge2),
                "dr_values": drs_ge2,
                "F_values": {str(k): v for k, v in F_anc.items()},
                "alpha": float(alpha_a),
                "dalpha": float(dalpha_a),
                "A": float(A_a),
                "dA": float(dA_a),
                "chi2_reduced": stats_a["chi2_reduced"],
                "fit_failed": False
            }
        except Exception as e:
            print(f"    Fit failed: {e}")
            anchor_results[str(anchor)] = {
                "n_points": len(drs_ge2),
                "dr_values": drs_ge2,
                "F_values": {str(k): v for k, v in F_anc.items()},
                "fit_failed": True,
                "error": str(e)
            }

    # Check anchor consistency
    fitted_anchors = {k: v for k, v in anchor_results.items() if not v.get("fit_failed")}
    if len(fitted_anchors) >= 2:
        alphas = [v["alpha"] for v in fitted_anchors.values()]
        dalphas = [v["dalpha"] for v in fitted_anchors.values()]
        alpha_spread = max(alphas) - min(alphas)
        avg_sigma = np.mean(dalphas)
        spread_in_sigma = alpha_spread / avg_sigma if avg_sigma > 0 else float('inf')

        print(f"\n  Anchor dependence summary:")
        print(f"    {'Anchor':>8}  {'alpha':>10}  {'dalpha':>10}  {'n_pts':>6}")
        for k, v in sorted(fitted_anchors.items(), key=lambda x: int(x[0])):
            print(f"    {k:>8}  {v['alpha']:>10.4f}  {v['dalpha']:>10.4f}  {v['n_points']:>6}")
        print(f"    Alpha spread: {alpha_spread:.4f}")
        print(f"    Average 1-sigma: {avg_sigma:.4f}")
        print(f"    Spread / avg_sigma: {spread_in_sigma:.2f}")
        if spread_in_sigma > 1.0:
            print(f"    WARNING: alpha varies by >{spread_in_sigma:.1f} sigma across anchors")
            print(f"    --> OBC contamination likely significant")
        else:
            print(f"    OK: alpha consistent across anchors within 1 sigma")
            print(f"    --> OBC contamination is subdominant")

        anchor_consistency = {
            "alpha_spread": float(alpha_spread),
            "avg_1sigma": float(avg_sigma),
            "spread_over_sigma": float(spread_in_sigma),
            "obc_contamination": "significant" if spread_in_sigma > 1.0 else "subdominant"
        }
    else:
        anchor_consistency = {"note": "insufficient anchors fitted"}

    # ── Save JSON ─────────────────────────────────────────────────────────
    elapsed = time.time() - t_global
    print(f"\n{'='*72}")
    print(f"Saving to {OUT_PATH}...")

    output = {
        "id": "SIM-2026-017",
        "date": "2026-04-07",
        "description": "Goodness-of-fit statistics for 24q force profile: chi^2, AIC, BIC, bootstrap, anchor dependence",
        "hypothesis": "HYP-2026-008",
        "source_sim": "SIM-2026-011",
        "data": {
            "dr_values": dr_fit,
            "F_values": F_fit,
            "n_points": n_pts,
            "note": "dr >= 2, from SIM-2026-011 F_interaction_avg"
        },
        "power_law_fit": {
            "model": "F(dr) = A * dr^{-alpha}",
            "A": float(A_pl),
            "dA": float(dA_pl),
            "alpha": float(alpha_pl),
            "dalpha": float(dalpha_pl),
            "statistics": stats_pl
        },
        "exponential_fit": {
            "model": "F(dr) = B * exp(-dr/xi)",
            "B": float(B_exp),
            "dB": float(dB_exp),
            "xi": float(xi_exp),
            "dxi": float(dxi_exp),
            "statistics": stats_exp
        },
        "model_comparison": {
            "delta_AIC_exp_minus_pl": float(delta_aic),
            "delta_BIC_exp_minus_pl": float(delta_bic),
            "preferred_by_AIC": "power_law" if delta_aic > 0 else "exponential",
            "preferred_by_BIC": "power_law" if delta_bic > 0 else "exponential"
        },
        "bootstrap": bootstrap_results,
        "anchor_dependence": {
            "anchors_tested": anchors_to_test,
            "results": anchor_results,
            "consistency": anchor_consistency
        },
        "runtime_s": float(elapsed),
        "hardware": "local_cpu",
        "status": "COMPLETE"
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(output, f, indent=2)
    print("  Saved.")

    # ── Final summary table ───────────────────────────────────────────────
    print(f"\n{'='*72}")
    print(f"SUMMARY TABLE")
    print(f"{'='*72}")
    print(f"\n  Model Comparison (n={n_pts} points, dr>=2, p=2 parameters each):")
    print(f"  {'Metric':<20}  {'Power-law':>14}  {'Exponential':>14}  {'Winner':>12}")
    print(f"  {'-'*20}  {'-'*14}  {'-'*14}  {'-'*12}")
    for key, fmt in [("chi2", ".6f"), ("chi2_reduced", ".6f"),
                     ("AIC", ".4f"), ("BIC", ".4f"),
                     ("RSS", ".4e"), ("rms_residual", ".4e")]:
        v_pl = stats_pl[key]
        v_exp = stats_exp[key]
        winner = "power-law" if v_pl < v_exp else "exponential"
        print(f"  {key:<20}  {v_pl:>14{fmt}}  {v_exp:>14{fmt}}  {winner:>12}")

    print(f"\n  Bootstrap Alpha Distribution (n={n_success} resamples):")
    print(f"    Mean:      {alpha_mean:.4f}")
    print(f"    Std:       {alpha_std:.4f}")
    print(f"    Median:    {alpha_median:.4f}")
    print(f"    95% CI:    [{alpha_ci_lo:.4f}, {alpha_ci_hi:.4f}]")
    print(f"    CFT prediction (alpha=4): "
          f"{'WITHIN' if alpha_ci_lo <= 4.0 <= alpha_ci_hi else 'OUTSIDE'} 95% CI")

    print(f"\n  Anchor Dependence:")
    for k, v in sorted(fitted_anchors.items(), key=lambda x: int(x[0])):
        print(f"    anchor={k:>2}: alpha = {v['alpha']:.4f} +/- {v['dalpha']:.4f}  "
              f"({v['n_points']} pts)")
    if "spread_over_sigma" in anchor_consistency:
        print(f"    Spread: {anchor_consistency['alpha_spread']:.4f} "
              f"({anchor_consistency['spread_over_sigma']:.2f} sigma)")
        print(f"    OBC contamination: {anchor_consistency['obc_contamination']}")

    print(f"\n  Total runtime: {elapsed:.1f}s")
    print(f"  Results saved to {OUT_PATH}")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
