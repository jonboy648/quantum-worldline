"""
SIM-2026-029: Functional-form fit of finite-T holographic transport TIME T(beta)
via the HYP-006 PRODUCTION time-extractor on a Thermofield Double at N=10.

WHY THIS EXISTS
---------------
SIM-2026-027 established (and SIM-2026-028/-L10 confirmed beyond thermal washout +
size-robust) that the finite-T transport AMPLITUDE degrades with temperature in the
horizon-absorption direction. But the transport TIME T(beta) was NOT fit to a functional
form, because the TFD harness used a naive grid-quantized peak/dip/reappear extractor that
misfires at small L (gave T=1.30 at the L=8 cold limit, not the HYP-006 value).

This script ports the HYP-006 PRODUCTION extractor (holographic_transport_finedt.py):
  - parabolic SUB-GRID refinement of the dip and reappearance times (continuous T, not
    grid-quantized), and
  - on-the-fly Y measurement on the PHYSICAL half of the doubled register (memory-safe at
    2^20; no stored embedded Y matrices),
and runs the beta-ladder at FINE dt so T(beta) is a smooth, fittable curve.

CRITICAL FINITE-SIZE FRAMING (honest)
-------------------------------------
HYP-006's OWN cold transport time is strongly finite-size dependent: T=2.250 at N=16 but
T=1.55 at N=24 (-31.6%). So the L=10 cold (beta->inf) transport time is NOT expected to be
(pi/2)*l_AdS=2.266. We therefore:
  (1) MEASURE the L=10 cold anchor T_cold = T(beta->inf) directly (this is the finite-size
      baseline), and
  (2) fit the SHAPE T(beta)/T_cold vs beta to candidate functional forms. The physics is in
      the temperature DEPENDENCE of the shape, not the absolute cold value.

MODELS FITTED (Gate: pre-committed before fitting)
--------------------------------------------------
  - Wang-He horizon absorption (amplitude ratio form adapted to the time observable's
    approach to the cold value): T(beta)/T_cold = WH(beta; params)
  - tanh crossover: T(beta)/T_cold = tanh(beta/beta_c)
  - Boltzmann: T(beta)/T_cold = exp(-a/beta)
  - flat null: T(beta)/T_cold = const
Selected by AIC and BIC (penalize parameters); also report R^2 and chi^2/dof. A model is
'preferred' only if it beats flat by Delta-AIC > 4 (substantial) AND is the AIC-min model.

GATES
-----
  Gate A: cold anchor must be a STABLE plateau (the 2-3 coldest betas agree within 3%);
          if not, the time extractor is unreliable at L=10 and we report fit as UNRELIABLE.
  Gate B: pre-committed model set + Delta=1 for any QNM cross-reference (locked).
  Gate C: report finite-size caveat explicitly; the cold anchor is L=10-specific.

Reuses verified TFD machinery from hyp024_tfd_btz_transport.py (build_tfd, embed_phys,
run on physical half) and the production extractor logic from holographic_transport_finedt.py
(parabolic refinement, on-the-fly Y).
"""
import time
import json
import numpy as np
from scipy.sparse.linalg import expm_multiply
from scipy.linalg import eigh
from scipy.optimize import curve_fit

import hyp024_tfd_btz_transport as TFD

SCRIPT_START = time.time()
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-029.json"

L_ADS = 1.0 / np.log(2)
T_NULL_PRED = (np.pi / 2) * L_ADS          # 2.2662 -- thermodynamic-limit prediction (reference only)
PRESPECIFIED_DELTA = 1.0                    # epsilon energy primary (locked, QNM reference)


# ══════════════════════════════════════════════════════════════════════════════
# PHYSICAL-HALF on-the-fly Y measurement and rotation on the DOUBLED register.
# Index convention (matches hyp024_tfd_btz_transport.build_tfd): physical sites are
# the HIGH L bits, ancilla the LOW L bits -> index = iphys * 2^L + ianc.
# So physical site i (0-indexed from the left of the L-bit physical block) corresponds
# to global bit position (2L - 1 - i) in the 2L-qubit doubled register.
# ══════════════════════════════════════════════════════════════════════════════
def measure_Y_phys(psi, i, L):
    """<psi| Y_i^phys (x) I_anc |psi> on the doubled register, on-the-fly (no stored op)."""
    n_total = 2 * L
    all_idx = np.arange(psi.shape[0], dtype=np.int64)
    bp = n_total - 1 - i                      # physical site i lives in the high-L block
    flipped = all_idx ^ (1 << bp)
    bv = (all_idx >> bp) & 1
    y_coeff = np.where(bv == 0, 1j, -1j)
    return float(np.real(np.dot(psi.conj(), y_coeff * psi[flipped])))


def apply_Y_rotation_phys(psi, i, L, theta):
    """exp(i*theta*Y_i^phys (x) I_anc) applied to a doubled-register statevector."""
    n_total = 2 * L
    all_idx = np.arange(psi.shape[0], dtype=np.int64)
    bp = n_total - 1 - i
    flipped = all_idx ^ (1 << bp)
    bv = (all_idx >> bp) & 1
    y_coeff = np.where(bv == 0, 1j, -1j)
    Yipsi = y_coeff * psi[flipped]
    return np.cos(theta) * psi + 1j * np.sin(theta) * Yipsi


# ══════════════════════════════════════════════════════════════════════════════
# Production transport-time extractor with parabolic sub-grid refinement
# (ported from holographic_transport_finedt.py:extract_transport_time).
# ══════════════════════════════════════════════════════════════════════════════
def extract_transport_time_refined(times, max_rho, n_steps):
    """T_transport = t_reappear - t_dip with 3-point parabolic sub-grid refinement
    of both the dip and the reappearance peak. Returns dict (grid + refined)."""
    dt_grid = float(times[1] - times[0])
    peak_search_end = max(5, int(0.3 * n_steps))
    peak_idx = int(np.argmax(max_rho[:peak_search_end]))
    peak_time = float(times[peak_idx])
    peak_val = float(max_rho[peak_idx])

    search_end = min(peak_idx + max(40, n_steps // 6), len(max_rho))
    dip_idx = peak_idx + int(np.argmin(max_rho[peak_idx:search_end]))
    dip_time_grid = float(times[dip_idx])
    dip_val = float(max_rho[dip_idx])
    dip_time = dip_time_grid
    if 1 <= dip_idx < len(max_rho) - 1:
        y0, y1, y2 = max_rho[dip_idx - 1], max_rho[dip_idx], max_rho[dip_idx + 1]
        denom = y0 - 2 * y1 + y2
        if abs(denom) > 1e-12:
            dip_time = dip_time_grid + 0.5 * (y0 - y2) / denom * dt_grid

    post_start = dip_idx + 3
    post_end = min(dip_idx + max(80, n_steps // 4), len(max_rho))
    if post_end <= post_start:
        return {"peak_time": peak_time, "peak_val": peak_val,
                "dip_time": dip_time, "dip_val": dip_val,
                "reappear_time": None, "reappear_val": None,
                "transport_time": None, "status": "NO_REAPPEARANCE"}
    rel = int(np.argmax(max_rho[post_start:post_end]))
    reappear_idx = post_start + rel
    reappear_time_grid = float(times[min(reappear_idx, len(times) - 1)])
    reappear_val = float(max_rho[min(reappear_idx, len(max_rho) - 1)])
    reappear_time = reappear_time_grid
    if 1 <= reappear_idx < len(max_rho) - 1:
        y0, y1, y2 = max_rho[reappear_idx - 1], max_rho[reappear_idx], max_rho[reappear_idx + 1]
        denom = y0 - 2 * y1 + y2
        if abs(denom) > 1e-12:
            reappear_time = reappear_time_grid + 0.5 * (y0 - y2) / denom * dt_grid

    return {"peak_time": peak_time, "peak_val": peak_val,
            "dip_time": dip_time, "dip_val": dip_val,
            "reappear_time": reappear_time, "reappear_val": reappear_val,
            "transport_time": reappear_time - dip_time, "status": "OK"}


# ══════════════════════════════════════════════════════════════════════════════
# TFD transport on the physical half with the production (refined) measurement.
# Ancilla evolves under identity (verified equivalent for physical-only observables,
# SIM-2026-027 confirm phase). First-order Trotter: rotations then H_phys evolution.
# ══════════════════════════════════════════════════════════════════════════════
def run_transport_tfd_refined(psi_init, H_full, L, gs_ref_Y,
                              dt=0.01, t_max=6.0,
                              OMEGA=5.0, M_ang=0, sigma_t=0.4, sigma_phi=0.4):
    """Returns (times, max_rho, n_steps). gs_ref_Y = reference <Y_i> for subtraction
    (the thermal state's own expectation, matching SIM-2026-027)."""
    phi = np.array([2 * np.pi * i / L - 3 * np.pi / 4 for i in range(L)])
    A = np.sqrt(2 * L / (sigma_t * sigma_phi)) / (40 * np.pi)
    n_steps = int(t_max / dt)
    times = np.arange(n_steps + 1) * dt

    J_matrix = np.zeros((n_steps + 1, L), dtype=complex)
    for step in range(n_steps + 1):
        t = times[step]
        J_matrix[step] = A * np.exp(
            -t ** 2 / (2 * sigma_t ** 2) - phi ** 2 / (2 * sigma_phi ** 2)
            - 1j * OMEGA * t + 1j * M_ang * phi)

    psi = psi_init.copy().astype(complex)
    max_rho = np.zeros(n_steps + 1)
    rho0 = np.array([measure_Y_phys(psi, i, L) - gs_ref_Y[i] for i in range(L)])
    max_rho[0] = float(np.max(np.abs(rho0)))

    for step in range(n_steps):
        J_real = np.real(J_matrix[step])
        for i in range(L):
            ji = J_real[i] * dt
            if abs(ji) >= 1e-14:
                psi = apply_Y_rotation_phys(psi, i, L, ji)
        psi = expm_multiply(-1j * H_full * dt, psi)
        psi /= np.linalg.norm(psi)
        rho_t = np.array([measure_Y_phys(psi, i, L) - gs_ref_Y[i] for i in range(L)])
        max_rho[step + 1] = float(np.max(np.abs(rho_t)))
    return times, max_rho, n_steps


# ══════════════════════════════════════════════════════════════════════════════
# Candidate functional forms for the SHAPE s(beta) = T(beta)/T_cold in [0,1].
# All approach 1 as beta->inf (cold = full transport time) and decrease as T rises.
# ══════════════════════════════════════════════════════════════════════════════
def m_wang_he(beta, beta_c, p):
    """Wang-He-style horizon absorption: smooth sigmoidal suppression of the AdS weight.
    s = 1 / (1 + (beta_c/beta)^p)  -> 1 as beta->inf, -> 0 as beta->0. Two params."""
    return 1.0 / (1.0 + (beta_c / np.maximum(beta, 1e-9)) ** p)


def m_tanh(beta, beta_c):
    return np.tanh(beta / beta_c)


def m_boltzmann(beta, a):
    return np.exp(-a / np.maximum(beta, 1e-9))


def m_flat(beta, c):
    return np.full_like(np.asarray(beta, float), c)


def _aic_bic(residuals, k, n):
    rss = float(np.sum(residuals ** 2))
    if rss <= 0 or n <= 0:
        return None, None, rss
    aic = n * np.log(rss / n) + 2 * k
    bic = n * np.log(rss / n) + k * np.log(n)
    return float(aic), float(bic), rss


def fit_models(beta, s):
    """Fit all candidate shape models; return dict with params, AIC, BIC, R2, and selection."""
    beta = np.asarray(beta, float); s = np.asarray(s, float)
    n = len(s)
    ss_tot = float(np.sum((s - s.mean()) ** 2))
    out = {}
    specs = [
        ("wang_he", m_wang_he, [np.median(beta), 1.0], 2),
        ("tanh", m_tanh, [np.median(beta)], 1),
        ("boltzmann", m_boltzmann, [1.0], 1),
        ("flat", m_flat, [float(s.mean())], 1),
    ]
    for name, fn, p0, k in specs:
        try:
            if name == "flat":
                popt = [float(s.mean())]
                resid = s - m_flat(beta, *popt)
            else:
                popt, _ = curve_fit(fn, beta, s, p0=p0, maxfev=40000)
                resid = s - fn(beta, *popt)
            aic, bic, rss = _aic_bic(resid, k, n)
            r2 = float(1 - np.sum(resid ** 2) / ss_tot) if ss_tot > 0 else None
            out[name] = {"params": [float(x) for x in np.atleast_1d(popt)],
                         "k": k, "AIC": aic, "BIC": bic, "rss": rss,
                         "chi2_per_dof": float(rss / max(1, n - k)), "R2": r2}
        except Exception as e:
            out[name] = {"params": None, "k": k, "AIC": None, "BIC": None,
                         "rss": None, "chi2_per_dof": None, "R2": None, "error": str(e)}
    # Selection: AIC-min model; preference over flat by Delta-AIC.
    aics = {k: v["AIC"] for k, v in out.items() if v["AIC"] is not None}
    if aics:
        best = min(aics, key=aics.get)
        flat_aic = aics.get("flat")
        wh_aic = aics.get("wang_he")
        out["_selection"] = {
            "aic_min_model": best,
            "delta_aic_flat_minus_best": (flat_aic - aics[best]) if flat_aic is not None else None,
            "delta_aic_flat_minus_wang_he": (flat_aic - wh_aic) if (flat_aic is not None and wh_aic is not None) else None,
            "wang_he_is_aic_min": best == "wang_he",
            "wang_he_substantial_over_flat": (
                wh_aic is not None and flat_aic is not None and (flat_aic - wh_aic) > 4.0),
        }
    else:
        out["_selection"] = {"aic_min_model": None}
    return out


def main():
    import sys
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 10
    DT = float(sys.argv[2]) if len(sys.argv) > 2 else 0.01
    print("=" * 72)
    print(f"SIM-2026-029: Functional-form fit of T(beta) via HYP-006 extractor "
          f"(TFD, L={L}, dt={DT})")
    print("=" * 72, flush=True)
    print(f"[GATE B -- LOCKED] models {{wang_he, tanh, boltzmann, flat}}; Delta=1 (epsilon) "
          f"for QNM reference. Thermodynamic-limit T_null=(pi/2)l_AdS={T_NULL_PRED:.4f} "
          f"is reference-only (finite-size anchor measured below).\n", flush=True)

    dimL = 2 ** L
    dimR = 2 ** L
    print(f"[1] Physical H_boundary (L={L}) + full spectrum...", flush=True)
    t0 = time.time()
    H_L_sparse = TFD.build_H_boundary(L)
    H_L_dense = H_L_sparse.toarray()
    evals, evecs = eigh(H_L_dense)
    E_gs = float(evals[0]); gap = float(evals[1] - evals[0])
    H_full = TFD.embed_phys(H_L_sparse, dimR)
    print(f"    E_gs={E_gs:.5f}, gap={gap:.5f}, dim_full={dimL*dimR} ({time.time()-t0:.2f}s)",
          flush=True)

    # Beta ladder: deep-cold anchors (for plateau gate) + thermal crossover + hot.
    BETA_LADDER = [200.0, 100.0, 50.0, 20.0, 10.0, 8.0, 5.0, 3.0, 2.0, 1.0, 0.5]
    print(f"[2] Beta ladder: {BETA_LADDER}\n", flush=True)

    rows = []
    for beta in BETA_LADDER:
        tb = time.time()
        psi_tfd, info = TFD.build_tfd(H_L_dense, beta)
        gs_ref_Y = np.array([measure_Y_phys(psi_tfd, i, L) for i in range(L)])
        times_x, max_rho, n_steps = run_transport_tfd_refined(
            psi_tfd, H_full, L, gs_ref_Y, dt=DT)
        sig = extract_transport_time_refined(times_x, max_rho, n_steps)
        T = sig["transport_time"]
        rows.append({
            "beta": float(beta), "temperature": float(1.0 / beta),
            "transport_time": T, "status": sig["status"],
            "peak_time": sig["peak_time"], "dip_time": sig["dip_time"],
            "reappear_time": sig["reappear_time"],
            "gs_population": TFD.reduced_phys_overlap_with_gs(psi_tfd, evecs[:, 0].astype(complex), dimL),
            "participation_ratio": info["participation_ratio"],
            "thermal_entropy": info["thermal_entropy"],
            "wall_time_s": time.time() - tb,
        })
        print(f"    beta={beta:>8.2f} | T={('%.4f'%T) if T else 'NA':>8} | {sig['status']:>14} | "
              f"gs_pop={rows[-1]['gs_population']:.3f} | N_eff={info['participation_ratio']:.2f} | "
              f"{rows[-1]['wall_time_s']:.0f}s", flush=True)

    # ── Gate A: cold-anchor plateau ──
    cold = [r for r in rows if r["beta"] >= 50 and r["transport_time"] and r["transport_time"] > 0]
    if len(cold) >= 2:
        cvals = np.array([r["transport_time"] for r in cold])
        T_cold = float(np.median(cvals))
        cold_spread = float((cvals.max() - cvals.min()) / T_cold) if T_cold > 0 else None
        gateA = cold_spread is not None and cold_spread < 0.03
    else:
        T_cold, cold_spread, gateA = None, None, False
    print(f"\n[GATE A] cold anchor T_cold={T_cold} (spread={cold_spread}); "
          f"plateau {'PASS' if gateA else 'FAIL/UNRELIABLE'}", flush=True)

    # ── Fit shape s(beta) = T(beta)/T_cold ──
    fit = None
    valid = [r for r in rows if r["transport_time"] and r["transport_time"] > 0]
    if T_cold and len(valid) >= 4:
        bb = np.array([r["beta"] for r in valid])
        ss = np.array([r["transport_time"] for r in valid]) / T_cold
        fit = fit_models(bb, ss)
        sel = fit["_selection"]
        print(f"\n[FIT] AIC-min model: {sel['aic_min_model']}; "
              f"Wang-He is AIC-min: {sel.get('wang_he_is_aic_min')}; "
              f"Delta-AIC(flat-WH)={sel.get('delta_aic_flat_minus_wang_he')}", flush=True)
        for name in ("wang_he", "tanh", "boltzmann", "flat"):
            m = fit[name]
            print(f"    {name:>10}: AIC={m['AIC']}, R2={m['R2']}, params={m['params']}", flush=True)

    # ── Verdict ──
    if not gateA:
        verdict = "UNRELIABLE_EXTRACTOR"
        reason = (f"Cold-anchor plateau gate FAILED (spread={cold_spread}). The transport-TIME "
                  f"extractor is not stable at L={L}; T(beta) functional-form fit is not "
                  f"trustworthy. The amplitude result (SIM-027/028) is unaffected.")
    elif fit is None:
        verdict = "INSUFFICIENT_POINTS"
        reason = "Too few valid T(beta) points to fit a functional form."
    else:
        sel = fit["_selection"]
        # MAGNITUDE FLOOR (added 2026-05-29 after SIM-029): AIC-beats-flat is necessary
        # but NOT sufficient. AIC will crown a model on a sub-percent wiggle. Require the
        # actual T(beta) shape to vary by more than a physical threshold across the
        # RELIABLE regime (exclude the hottest near-maximally-mixed point where extraction
        # is least trustworthy) before claiming any temperature dependence is real.
        T_vals = np.array([r["transport_time"] for r in valid if r["transport_time"] and r["transport_time"] > 0])
        b_vals = np.array([r["beta"] for r in valid if r["transport_time"] and r["transport_time"] > 0])
        reliable = b_vals >= 1.0   # exclude beta<1 (N_eff huge, dip/reappear unreliable)
        if reliable.sum() >= 2 and T_cold and T_cold > 0:
            shape_var_reliable = float((T_vals[reliable].max() - T_vals[reliable].min()) / T_cold)
        else:
            shape_var_reliable = float((T_vals.max() - T_vals.min()) / T_cold) if T_cold else 0.0
        MAG_FLOOR = 0.10   # require >10% of T_cold variation to call T(beta) genuinely non-flat
        magnitude_ok = shape_var_reliable > MAG_FLOOR
        print(f"  [magnitude floor] reliable-regime T variation = {shape_var_reliable*100:.2f}% "
              f"of T_cold (floor {MAG_FLOOR*100:.0f}%): {'PASS' if magnitude_ok else 'FAIL -> effectively flat'}",
              flush=True)
        if not magnitude_ok:
            verdict = "TIME_OBSERVABLE_FLAT"
            reason = (f"T(beta) is effectively FLAT: it varies only {shape_var_reliable*100:.2f}% of "
                      f"T_cold across the reliable regime (beta>=1), below the {MAG_FLOOR*100:.0f}% "
                      f"physical floor. Any AIC 'preference' (best={sel.get('aic_min_model')}, "
                      f"Delta-AIC={sel.get('delta_aic_flat_minus_best')}) is fitting sub-threshold "
                      f"noise, NOT real temperature dependence. CONCLUSION: the transport-TIME channel "
                      f"does not carry the horizon signal at L={L}; this dissociates from the AMPLITUDE "
                      f"channel (SIM-027/028) which did. Functional form NOT claimable.")
        elif sel.get("wang_he_is_aic_min") and sel.get("wang_he_substantial_over_flat"):
            verdict = "WANG_HE_FUNCTIONAL_FORM_PREFERRED"
            reason = (f"T(beta)/T_cold is best described by the Wang-He horizon-absorption form "
                      f"(AIC-min, Delta-AIC over flat = {sel['delta_aic_flat_minus_wang_he']:.1f} > 4). "
                      f"Cold anchor T_cold={T_cold:.3f} is the L={L} finite-size value (NOT the "
                      f"thermodynamic 2.266; HYP-006 N=24 gave 1.55, so this is expected).")
        elif fit["_selection"].get("delta_aic_flat_minus_best", 0) and fit["_selection"]["delta_aic_flat_minus_best"] > 4:
            verdict = "NONFLAT_BUT_NOT_WANG_HE"
            reason = (f"T(beta) is significantly non-flat (best={sel['aic_min_model']}, beats flat "
                      f"by Delta-AIC={sel['delta_aic_flat_minus_best']:.1f}), but the Wang-He form "
                      f"is not the AIC-minimum. Temperature dependence is real; functional-form "
                      f"identification is ambiguous at L={L}.")
        else:
            verdict = "FLAT_OR_INCONCLUSIVE"
            reason = (f"No functional form beats the flat null substantially (best={sel['aic_min_model']}, "
                      f"Delta-AIC over flat = {sel.get('delta_aic_flat_minus_best')}). T(beta) shape "
                      f"is not resolved at L={L}.")
    print(f"\n[VERDICT] {verdict}\n  {reason}", flush=True)

    out_path = OUT_PATH if L == 10 else OUT_PATH.replace(".json", f"-L{L}.json")
    output = {
        "id": "SIM-2026-029", "L_physical": L, "dt": DT,
        "description": ("Functional-form fit of finite-T holographic transport TIME T(beta) "
                        "via the HYP-006 production extractor (parabolic sub-grid refinement, "
                        "on-the-fly physical-half Y) on a Thermofield Double at L={}.".format(L)),
        "type": "classical", "date": "2026-05-29", "hypothesis_id": "HYP-2026-024",
        "relates_to": ["SIM-2026-027", "SIM-2026-028"],
        "hardware_target": "local_cpu",
        "results": {
            "verdict": verdict, "verdict_reason": reason,
            "T_cold_finite_size_anchor": T_cold, "cold_plateau_spread": cold_spread,
            "gate_A_plateau_pass": gateA,
            "thermodynamic_limit_reference_T_null": T_NULL_PRED,
            "spectral_gap": gap, "E_gs": E_gs,
            "beta_ladder": rows,
            "shape_fit": fit,
            "prespecified": {"Delta": PRESPECIFIED_DELTA, "models_locked": True},
            "total_wall_time_s": time.time() - SCRIPT_START,
        },
        "classical_baseline": {
            "method": f"Exact TFD on doubled {2*L}-qubit register; HYP-006 production extractor",
            "extractor": "parabolic sub-grid dip/reappear refinement, on-the-fly physical-half Y",
            "finite_size_note": ("Cold anchor is L-specific; HYP-006 T=2.250@N16, 1.55@N24 -> "
                                 "transport time is strongly finite-size dependent. Fit is on the "
                                 "SHAPE T(beta)/T_cold, not the absolute value."),
        },
        "comparison": "classical_wins",
        "notes": ("SIM-2026-029 fits the transport-TIME functional form, complementing the "
                  "extractor-independent amplitude result (SIM-027/028). Honest scope: the cold "
                  "anchor is finite-size; the claim is about the temperature-dependent SHAPE."),
    }
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}\nTotal wall time: {time.time()-SCRIPT_START:.0f}s", flush=True)


if __name__ == "__main__":
    main()
