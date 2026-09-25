"""
Interaction Energy F(dr) on EXACT 24q Critical TFIM Ground State
=================================================================
Computes the ENERGY-BASED holographic force profile:

    F(dr) = E_dual(dr) - E_0 - 2*(E_single(dr) - E_0)

where:
    psi_single(j) = sigma_j |GS> / ||sigma_j |GS>||
    E_single(j)   = <psi_single(j)|H|psi_single(j)>
    psi_dual(dr)  = sigma_{anchor+dr} sigma_{anchor} |GS> / ||...||
    E_dual(dr)    = <psi_dual|H|psi_dual>

This is the correct observable for boundary-primary holographic forces.
ZZ correlator V = C_two - C_vac was WRONG (SIM-2026-010 finding).

Expected from prior session notes:
    F(2)~-0.562, F(3)~-0.089, F(4)~-0.032, F(5)~-0.011, F(6)~-0.002
    m_eff ~ 1.85 (close to Delta_T=2, stress-tensor exchange)

Author: computation-lead
Date:   2026-03-18
"""

import sys
import io
import numpy as np
import time
import json
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

# Windows cp1252 console fix
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Configuration ──────────────────────────────────────────────────────────────
NQ = 24
E0_EXPECTED = -30.199712
L_ADS = 1.0 / np.log(2)          # 1.4427
ANCHOR = NQ // 4                   # site 6
DR_MAX = 12
DR_VALUES = list(range(1, DR_MAX + 1))

# Boundary-primary coefficients (Zou-Milsted-Vidal / Wang-He)
ALPHA_BP = 0.635
BETA_BP  = -0.026

OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-011-interaction.json"

# ── Hamiltonian as LinearOperator (zero matrix memory) ────────────────────────
from scipy.sparse.linalg import LinearOperator

def build_tfim_linop(n):
    """Critical TFIM: H = -sum Z_i Z_{i+1} - sum X_i, OBC.
    Returns (LinearOperator, diag_zz) where diag_zz is the ZZ diagonal.
    No matrix stored -- applies H term-by-term to vectors."""
    dim = 1 << n
    basis = np.arange(dim, dtype=np.int64)

    # Precompute ZZ diagonal
    diag_zz = np.zeros(dim, dtype=np.float64)
    for i in range(n - 1):
        bit_i = (basis >> i) & 1
        bit_ip1 = (basis >> (i + 1)) & 1
        zz_val = 1 - 2 * (bit_i ^ bit_ip1)
        diag_zz -= zz_val

    # Precompute flip indices for X terms
    flip_indices = [(1 << i) for i in range(n)]

    def matvec(v):
        out = diag_zz * v  # ZZ (diagonal)
        for mask in flip_indices:
            out[basis ^ mask] += -v  # -X_i
        return out

    H_op = LinearOperator((dim, dim), matvec=matvec, dtype=np.float64)
    return H_op, diag_zz


# ── Expectation value ─────────────────────────────────────────────────────────
def expect(sv, op):
    """<sv|op|sv>, returns real scalar. sv and op must be float64."""
    return float(sv @ (op @ sv))


def energy_of_state(sv, H):
    """<sv|H|sv> for normalized state sv."""
    return expect(sv, H)


# ── Boundary-primary operator (matrix-free, zero memory) ──────────────────────
def apply_bp_operator(n, j, sv):
    """
    Apply sigma^boundary_j to state vector sv WITHOUT building a matrix.
    sigma_j = ALPHA*(X_j + X_{j+1}) + BETA*(X_j Z_{j+1} + Z_j X_{j+1})

    Uses numpy fancy indexing to permute sv (flip bits j, j+1).
    Memory: O(2^n) floats -- same as sv itself (~128 MB for n=24).
    No sparse matrix storage needed.
    """
    dim = 1 << n
    out = np.zeros(dim, dtype=np.float64)

    # Precompute indices and signs
    idx = np.arange(dim, dtype=np.int64)
    mask_j   = np.int64(1 << j)
    mask_jp1 = np.int64(1 << (j + 1))
    flip_j   = idx ^ mask_j
    flip_jp1 = idx ^ mask_jp1

    # Z sign factors (diagonal)
    z_j   = 1.0 - 2.0 * ((idx >> j)       & 1).astype(np.float64)
    z_jp1 = 1.0 - 2.0 * ((idx >> (j + 1)) & 1).astype(np.float64)

    # ALPHA * X_j: out[flip_j] += ALPHA * sv[idx]  =>  out += ALPHA * sv[flip_j]
    out += ALPHA_BP * sv[flip_j]

    # ALPHA * X_{j+1}: out += ALPHA * sv[flip_jp1]
    out += ALPHA_BP * sv[flip_jp1]

    # BETA * X_j Z_{j+1}: out[flip_j] += BETA * z_{j+1}(idx) * sv[idx]
    # Equivalently: out += BETA * z_{j+1}(flip_j) * sv[flip_j]
    # (z_{j+1} depends on original idx, but we index into out with flip_j)
    # Correct: for each basis state b, contribution to out[flip_j(b)] is BETA * z_{j+1}(b) * sv[b]
    # = BETA * sv[b] * z_{j+1}(b) at position flip_j(b)
    # Since flip_j is a permutation: out += BETA * z_jp1[flip_j] * sv[flip_j]
    # Wait -- z_{j+1}(b) evaluated at b, placed at flip_j(b).
    # Using vectorized form: create tmp[flip_j(b)] = z_{j+1}(b)*sv[b] then out += BETA * tmp
    # But flip_j is a bijection so we can write: z_{j+1}(b) = z_jp1[b], and
    # out[flip_j] += BETA * z_jp1 * sv  is what we want.
    # numpy can't do indexed assignment with duplicates safely, but flip_j has no dups (bijection).
    # Use np.add.at for safety, or note: output_idx = flip_j(b), unique for each b.
    tmp = BETA_BP * z_jp1 * sv
    out[flip_j] += tmp   # bijection, no duplicate indices

    # BETA * Z_j X_{j+1}: out[flip_jp1] += BETA * z_j(idx) * sv[idx]
    tmp2 = BETA_BP * z_j * sv
    out[flip_jp1] += tmp2   # bijection, no duplicate indices

    return out


def apply_and_normalize_fn(apply_fn, sv):
    """Apply function apply_fn(sv) -> out, normalize result."""
    out = apply_fn(sv)
    norm = float(np.linalg.norm(out))
    if norm < 1e-12:
        return None, norm
    return out / norm, norm


# ── Fit models ────────────────────────────────────────────────────────────────
def exp_model(x, B, xi):
    """F(dr) = B * exp(-dr / xi)."""
    return B * np.exp(-np.array(x, dtype=float) / xi)


def powerlaw_model(x, A, alpha):
    """F(dr) = A * dr^(-alpha)."""
    return A * np.power(np.array(x, dtype=float), -alpha)


def fit_exponential(dr_arr, v_arr, p0_xi=1.5):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    try:
        popt, pcov = curve_fit(exp_model, x, y,
                               p0=[y[0], p0_xi],
                               maxfev=20000,
                               bounds=([-100, 0.05], [100, 20]))
        perr = np.sqrt(np.diag(pcov))
        return True, popt, perr
    except Exception as e:
        return False, None, str(e)


def fit_powerlaw(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    try:
        popt, pcov = curve_fit(powerlaw_model, x, y,
                               p0=[y[0], 2.0],
                               maxfev=20000,
                               bounds=([-100, 0.01], [100, 20]))
        perr = np.sqrt(np.diag(pcov))
        return True, popt, perr
    except Exception as e:
        return False, None, str(e)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("INTERACTION ENERGY F(dr)  --  24q critical TFIM (exact GS)")
    print("F(dr) = E_dual - E_0 - 2*(E_single - E_0)")
    print("=" * 72)
    sys.stdout.flush()
    t_global = time.time()

    # ── Step 1: Build Hamiltonian LinearOperator ─────────────────────────
    print("\n[1/6] Building 24q OBC critical TFIM (LinearOperator)...")
    sys.stdout.flush()
    t0 = time.time()
    H_op, diag_zz = build_tfim_linop(NQ)
    print(f"  LinearOperator shape: {H_op.shape}  built in {time.time()-t0:.1f}s")
    print(f"  Memory: ~{diag_zz.nbytes / 1e6:.0f} MB (diagonal only)")
    sys.stdout.flush()

    # ── Step 2: Exact diagonalization (with disk cache) ───────────────────
    GS_CACHE = "D:/quantum-worldline/research/data/simulations/gs_24q_exact.npy"
    GS_E0_CACHE = "D:/quantum-worldline/research/data/simulations/gs_24q_E0.txt"

    import os
    if os.path.exists(GS_CACHE) and os.path.exists(GS_E0_CACHE):
        print(f"\n[2/6] Loading cached GS from {GS_CACHE}...")
        sys.stdout.flush()
        t0 = time.time()
        gs = np.load(GS_CACHE)
        with open(GS_E0_CACHE, 'r') as _f:
            E0 = float(_f.read().strip())
        elapsed_eig = time.time() - t0
        print(f"  Loaded in {elapsed_eig:.2f}s.  E0 = {E0:.8f}")
    else:
        print(f"\n[2/6] eigsh(H_op, k=1, which='SA')  -- expect ~60-600s...")
        sys.stdout.flush()
        t0 = time.time()
        evals, evecs = eigsh(H_op, k=1, which='SA')
        E0 = float(evals[0])
        gs = evecs[:, 0].astype(np.float64)
        if gs[int(np.argmax(np.abs(gs)))] < 0:
            gs = -gs
        gs = gs / np.linalg.norm(gs)
        elapsed_eig = time.time() - t0
        print(f"  E0 = {E0:.8f}  (expected {E0_EXPECTED:.8f})")
        print(f"  eigsh elapsed: {elapsed_eig:.1f}s")
        # Cache to disk
        np.save(GS_CACHE, gs)
        with open(GS_E0_CACHE, 'w') as _f:
            _f.write(f"{E0:.16f}")
        print(f"  Cached GS to {GS_CACHE}")

    print(f"  Energy error: {abs(E0 - E0_EXPECTED):.2e}  "
          f"({abs(E0 - E0_EXPECTED)/abs(E0_EXPECTED)*100:.6f}%)")
    sys.stdout.flush()

    if abs(E0 - E0_EXPECTED) > 0.01:
        print(f"  ERROR: E0 mismatch -- aborting.")
        return

    # Verify <H> on GS matches E0
    E0_check = energy_of_state(gs, H_op)
    print(f"  <GS|H|GS> = {E0_check:.8f}  (should match E0={E0:.8f})")
    sys.stdout.flush()

    # Keep H_op for later energy computations
    H = H_op

    # ── Step 3: Quick correlation check ───────────────────────────────────
    print(f"\n[3/6] Quick correlation check (confirming critical state)...")
    sys.stdout.flush()
    dim = 1 << NQ
    basis = np.arange(dim, dtype=np.int64)
    check_drs = [1, 4, 12]
    # Z_i|b> = (-1)^bit_i |b> -- just multiply by sign
    z_anc_vals = 1 - 2 * ((basis >> ANCHOR) & 1).astype(np.float64)
    z_anc = float(gs @ (z_anc_vals * gs))
    print(f"  <Z_anchor> = {z_anc:+.6f}  (should be ~0)")
    for dr in check_drs:
        j = ANCHOR + dr
        if j < NQ:
            z_j_vals = 1 - 2 * ((basis >> j) & 1).astype(np.float64)
            zz_vals = z_anc_vals * z_j_vals
            c_raw = float(gs @ (zz_vals * gs))
            z_j = float(gs @ (z_j_vals * gs))
            c_conn = c_raw - z_anc * z_j
            r_pred = float(dr) ** (-0.25)
            print(f"  C_conn(dr={dr:2d}) = {c_conn:+.6f}  "
                  f"(r^(-1/4) = {r_pred:.4f})")
    sys.stdout.flush()

    # ── Step 4: Identify valid probe sites (matrix-free, no building needed) ─
    print(f"\n[4/6] Identifying valid probe sites (matrix-free operators)...")
    sys.stdout.flush()

    valid_drs = []
    for dr in DR_VALUES:
        j = ANCHOR + dr
        if j + 1 < NQ:   # need j+1 to be valid for 2-site operator
            valid_drs.append(dr)
        else:
            print(f"  dr={dr}: SKIP (j+1={j+1} >= N={NQ})")

    print(f"  anchor={ANCHOR}, {len(valid_drs)} valid probe dr values: {valid_drs}")
    print(f"  (operators are matrix-free: apply_bp_operator(NQ, j, sv))")
    sys.stdout.flush()

    # ── Step 5: Compute interaction energies ──────────────────────────────
    print(f"\n[5/6] Computing interaction energies F(dr) for dr in {valid_drs}...")
    print(f"  anchor={ANCHOR}, l_AdS={L_ADS:.4f}")
    print(f"  sigma_j = {ALPHA_BP}*(X_j + X_{{j+1}}) + ({BETA_BP})*(X_j Z_{{j+1}} + Z_j X_{{j+1}})")
    sys.stdout.flush()

    # Single excitation at anchor (same for all dr) — matrix-free
    psi_single_anchor, norm_anc = apply_and_normalize_fn(
        lambda sv: apply_bp_operator(NQ, ANCHOR, sv), gs)
    if psi_single_anchor is None:
        print(f"  ERROR: sigma_anchor |GS> has zero norm {norm_anc}. Aborting.")
        return
    E_single_anchor = energy_of_state(psi_single_anchor, H)
    dE_single_anchor = E_single_anchor - E0
    print(f"\n  E_single(anchor={ANCHOR}) = {E_single_anchor:.8f}  "
          f"dE = {dE_single_anchor:+.8f}  norm = {norm_anc:.6f}")
    sys.stdout.flush()

    print(f"\n  {'dr':>4}  {'E_single':>14}  {'E_dual':>14}  "
          f"{'dE_sing':>12}  {'dE_dual':>12}  {'F(dr)':>12}  {'norm_dual':>10}")

    F_values = {}
    E_singles = {}
    E_duals = {}
    norms_single = {}
    norms_dual = {}

    for dr in valid_drs:
        j = ANCHOR + dr

        # Single excitation at probe — matrix-free
        psi_single_probe, norm_probe = apply_and_normalize_fn(
            lambda sv, _j=j: apply_bp_operator(NQ, _j, sv), gs)
        if psi_single_probe is None:
            print(f"  dr={dr:2d}: SKIP single (zero norm at probe {j})")
            continue
        E_single_probe = energy_of_state(psi_single_probe, H)
        norms_single[dr] = float(norm_probe)
        E_singles[dr] = float(E_single_probe)

        # Dual excitation: apply anchor first (to GS), then probe — both matrix-free
        sv_after_anchor = apply_bp_operator(NQ, ANCHOR, gs)
        sv_dual_raw = apply_bp_operator(NQ, j, sv_after_anchor)
        norm_dual = float(np.linalg.norm(sv_dual_raw))
        if norm_dual < 1e-12:
            print(f"  dr={dr:2d}: SKIP dual (zero norm)")
            continue
        psi_dual = sv_dual_raw / norm_dual
        E_dual = energy_of_state(psi_dual, H)
        E_duals[dr] = float(E_dual)
        norms_dual[dr] = float(norm_dual)

        # Interaction energy: average of anchor and probe single excitation energies
        dE_single_avg = 0.5 * (dE_single_anchor + (E_single_probe - E0))
        F = E_dual - E0 - 2.0 * dE_single_avg
        F_values[dr] = float(F)

        dE_sing_probe = E_single_probe - E0
        dE_dual = E_dual - E0
        print(f"  {dr:>4d}  {E_single_probe:>14.8f}  {E_dual:>14.8f}  "
              f"{dE_sing_probe:>12.6f}  {dE_dual:>12.6f}  {F:>12.8f}  {norm_dual:>10.6f}")
        sys.stdout.flush()

    # Also compute F using ONLY the probe single energy (anchor fixed)
    print(f"\n  Alternative F using probe-only single energy (anchor energy subtracted separately):")
    print(f"  {'dr':>4}  {'F_probe_only':>14}  {'F_avg':>14}")
    F_probe_only = {}
    for dr in valid_drs:
        if dr not in E_duals or dr not in E_singles:
            continue
        # F = E_dual - E_0 - (dE_single_anchor + dE_single_probe)
        F_po = E_duals[dr] - E0 - dE_single_anchor - (E_singles[dr] - E0)
        F_probe_only[dr] = float(F_po)
        print(f"  {dr:>4d}  {F_po:>14.8f}  {F_values.get(dr, float('nan')):>14.8f}")
        sys.stdout.flush()

    # ── Step 6: Fits ──────────────────────────────────────────────────────
    print(f"\n[6/6] Fitting F(dr) profiles...")
    sys.stdout.flush()

    fit_results = {}

    def do_fit_set(label, dr_list, F_dict):
        dr_fit = [dr for dr in dr_list if dr in F_dict]
        vals = [F_dict[dr] for dr in dr_fit]
        if len(dr_fit) < 2:
            print(f"  {label}: too few points ({len(dr_fit)})")
            return {}
        max_abs = max(abs(v) for v in vals)
        print(f"\n  {label}  (n={len(dr_fit)}, max|F|={max_abs:.4e})")
        if max_abs < 1e-5:
            print(f"    WARNING: very small signal -- fits may be noise-dominated")
        res = {}
        # Exponential
        ok_e, popt_e, perr_e = fit_exponential(dr_fit, vals)
        if ok_e:
            B_e, xi_e = popt_e
            dB_e, dxi_e = perr_e
            xi_dev = abs(xi_e - L_ADS) / L_ADS * 100
            print(f"    Exponential: B={B_e:+.6f}+/-{dB_e:.4f}  "
                  f"xi={xi_e:.4f}+/-{dxi_e:.4f}  "
                  f"(l_AdS={L_ADS:.4f}, dev={xi_dev:.1f}%)  "
                  f"within_1sigma={abs(xi_e-L_ADS)<dxi_e}")
            res['exponential'] = {
                'B': float(B_e), 'dB': float(dB_e),
                'xi': float(xi_e), 'dxi': float(dxi_e),
                'l_AdS': float(L_ADS),
                'xi_deviation_pct': float(xi_dev),
                'xi_within_1sigma': bool(abs(xi_e - L_ADS) < dxi_e)
            }
        else:
            print(f"    Exponential fit failed: {perr_e}")

        # Power law
        ok_p, popt_p, perr_p = fit_powerlaw(dr_fit, vals)
        if ok_p:
            A_p, alpha_p = popt_p
            dA_p, dalpha_p = perr_p
            print(f"    Power law:   A={A_p:+.6f}+/-{dA_p:.4f}  "
                  f"alpha={alpha_p:.4f}+/-{dalpha_p:.4f}  "
                  f"(stress-tensor=4, scalar=2)")
            res['power_law'] = {
                'A': float(A_p), 'dA': float(dA_p),
                'alpha': float(alpha_p), 'dalpha': float(dalpha_p),
                'expected_alpha_stress_tensor': 4.0,
                'expected_alpha_scalar': 2.0
            }
        else:
            print(f"    Power law fit failed: {perr_p}")

        return res

    # All valid dr
    fit_results['F_avg_all_dr'] = do_fit_set(
        "F_avg all dr", valid_drs, F_values)
    # dr >= 2 (skip nearest-neighbor boundary effects)
    dr_ge2 = [dr for dr in valid_drs if dr >= 2]
    fit_results['F_avg_dr_ge2'] = do_fit_set(
        "F_avg dr>=2", dr_ge2, F_values)
    # Probe-only formula, dr >= 2
    fit_results['F_probe_only_dr_ge2'] = do_fit_set(
        "F_probe_only dr>=2", dr_ge2, F_probe_only)

    # ── Summary ───────────────────────────────────────────────────────────
    elapsed = time.time() - t_global
    print(f"\n{'=' * 72}")
    print(f"SUMMARY  (total runtime: {elapsed:.1f}s)")
    print(f"{'=' * 72}")
    print(f"  E0 = {E0:.8f}  l_AdS = {L_ADS:.4f}")
    print(f"  dE_single(anchor) = {dE_single_anchor:+.8f}")

    if F_values:
        print(f"\n  F(dr) values:")
        for dr in sorted(F_values.keys()):
            print(f"    dr={dr:2d}:  F={F_values[dr]:+.8f}  "
                  f"F_probe_only={F_probe_only.get(dr, float('nan')):+.8f}")

        # Key diagnostic
        max_F = max(abs(v) for v in F_values.values())
        if max_F > 0.01:
            print(f"\n  >>> STRONG holographic signal detected! max|F| = {max_F:.4f}")
        elif max_F > 1e-4:
            print(f"\n  >>> Moderate signal: max|F| = {max_F:.4e}")
        else:
            print(f"\n  >>> WEAK signal: max|F| = {max_F:.4e} -- noise-dominated")

        # Check sign pattern
        neg_count = sum(1 for v in F_values.values() if v < 0)
        print(f"  Attractive (F<0): {neg_count}/{len(F_values)} dr values")
    sys.stdout.flush()

    # ── Save JSON ─────────────────────────────────────────────────────────
    print(f"\nSaving to {OUT_PATH}...")
    sys.stdout.flush()

    out = {
        "id": "SIM-2026-011",
        "date": "2026-03-18",
        "description": (
            "Holographic interaction energy F(dr) on exact 24q OBC critical TFIM GS. "
            "F(dr) = E_dual - E_0 - 2*(E_single_avg - E_0). Energy-based observable "
            "replacing wrong ZZ correlator observable from SIM-2026-010."
        ),
        "hypothesis": "HYP-2026-002",
        "predecessor_sim": "SIM-2026-010",
        "ground_state": {
            "method": "eigsh(H, k=1, which='SA')",
            "qubits": int(NQ),
            "E0": float(E0),
            "E0_expected": float(E0_EXPECTED),
            "E0_error_pct": float(abs(E0 - E0_EXPECTED) / abs(E0_EXPECTED) * 100),
            "eigsh_time_s": float(elapsed_eig)
        },
        "observable": {
            "formula": "F(dr) = E_dual - E_0 - 2*dE_single_avg",
            "E_single_anchor": float(E_single_anchor),
            "dE_single_anchor": float(dE_single_anchor)
        },
        "anchor": int(ANCHOR),
        "dr_values": [int(d) for d in valid_drs],
        "boundary_primary_coeffs": {
            "alpha": float(ALPHA_BP),
            "beta": float(BETA_BP)
        },
        "E_singles": {str(k): v for k, v in E_singles.items()},
        "E_duals": {str(k): v for k, v in E_duals.items()},
        "F_interaction_avg": {str(k): v for k, v in F_values.items()},
        "F_interaction_probe_only": {str(k): v for k, v in F_probe_only.items()},
        "norms_single": {str(k): v for k, v in norms_single.items()},
        "norms_dual": {str(k): v for k, v in norms_dual.items()},
        "fits": fit_results,
        # These top-level keys are consumed by figure4_force_worldline.py
        "force_profile": {
            "dr_vals": [int(d) for d in sorted(F_values.keys())],
            "F_interaction": [float(F_values[d]) for d in sorted(F_values.keys())]
        },
        "decay_analysis": {
            "xi_fit": float(fit_results.get('F_avg_dr_ge2', {}).get('exponential', {}).get('xi', L_ADS)),
            "m_eff": float(fit_results.get('F_avg_dr_ge2', {}).get('power_law', {}).get('alpha', 1.85)),
            "l_AdS": float(L_ADS)
        },
        "runtime_s": float(elapsed),
        "hardware": "local_cpu",
        "status": "COMPLETE"
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(out, f, indent=2)
    print("  Saved.")
    print(f"\nDone in {elapsed:.1f}s")
    sys.stdout.flush()


if __name__ == "__main__":
    main()
