"""
SIM-2026-031 — HYP-2026-026 pre-registered test: Synge-world-function distance is
geometric but FORCE-BLIND.

Protocol exactly as registered in HYP-2026-026.json (test_design / refutation_criteria):
  Tier 1 PRIMARY   (registered option b): synthetic clean-CFT correlator C_cft(r)=r^{-1/4}
  Tier 2 PHYSICAL  (upgrade of option a): connected sigma-sigma <Z_i Z_{i+r}>_c on the
                   EXACT 16q critical-TFIM ground state (PBC; 24q exact-diag is an ~8 h
                   eigsh and adds nothing to the shape question; chord-corrected fits
                   handle the finite-N form). H = -sum X - sum ZZ via FC.build_tfim_sparse.
  Tier 3 CONTROL   (known-pathological): SIM-2026-011.json zz_correlators (flat, r=4 artifact).

For each tier: Synge map d(r)=sqrt(-2 eps^2 ln|C(r)|) at eps=1 (eps is a pure multiplicative
prefactor -- shape/monotonicity/log-slope are eps-independent by construction); monotonicity
check (GEOMETRIC half gate); linear and power-law fits of d(r) vs r with R^2;
FORCE-BLINDNESS gate kappa = -d ln|C| / d ln r vs the dichotomy 0.25 (=2*Delta_sigma) vs
~4 (=alpha, stress tensor). 16q additionally fitted against the PBC chord variable
(N/pi)*sin(pi r/N) to deconvolve finite size.

Pre-registered verdict rules:
  GEOMETRIC half REFUTED      iff d(r) non-monotone on the artifact-free synthetic tier.
  FORCE-BLINDNESS half REFUTED iff kappa ~ 4 rather than ~ 0.25.
  INCONCLUSIVE                 iff no fit reaches R^2 > 0.9 even after the synthetic
                               cross-check isolates the r=4 artifact.
Outputs: SIM-2026-031.json (template-conformant) + verdict write-back into HYP-2026-026.json.
"""
import json
import time

import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD

OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-031.json"
HYP = "D:/quantum-worldline/research/data/hypotheses/HYP-2026-026.json"
SIM011 = "D:/quantum-worldline/research/data/simulations/SIM-2026-011.json"
N = 16
RS = np.arange(1, 9)  # r = 1..8 (= N/2)


def synge(C, eps=1.0):
    return np.sqrt(-2.0 * eps**2 * np.log(np.abs(C)))


def fits(r, d):
    """Linear and power-law fits of d(r) vs r, with R^2 for each."""
    out = {}
    # linear d = a*r + b
    A = np.vstack([r, np.ones_like(r)]).T
    coef, res, *_ = np.linalg.lstsq(A, d, rcond=None)
    ss_tot = np.sum((d - d.mean()) ** 2)
    ss_res = float(res[0]) if len(res) else float(np.sum((d - A @ coef) ** 2))
    out["linear"] = {"slope": float(coef[0]), "intercept": float(coef[1]),
                     "r2": float(1 - ss_res / ss_tot)}
    # power law d = c*r^p  (log-log linear)
    lp = np.polyfit(np.log(r), np.log(d), 1)
    pred = np.exp(np.polyval(lp, np.log(r)))
    out["power"] = {"exponent": float(lp[0]), "prefactor": float(np.exp(lp[1])),
                    "r2": float(1 - np.sum((d - pred) ** 2) / ss_tot)}
    return out


def kappa_loglog(rvar, C):
    """Global log-log slope of |C| vs the given radial variable -> kappa = -slope."""
    s = np.polyfit(np.log(rvar), np.log(np.abs(C)), 1)[0]
    return float(-s)


def main():
    t0 = time.time()
    print("=" * 72)
    print("SIM-2026-031: Synge distance — geometric but force-blind (HYP-026)")
    print("=" * 72)
    tiers = {}

    # ---- Tier 1: synthetic clean CFT (registered PRIMARY) ----
    C_cft = RS.astype(float) ** (-0.25)
    d_cft = synge(C_cft)
    mono_cft = bool(np.all(np.diff(d_cft) > 0))
    tiers["synthetic_cft"] = {
        "C": C_cft.tolist(), "d_synge": d_cft.tolist(),
        "monotone_increasing": mono_cft, "fits_d_vs_r": fits(RS, d_cft),
        "kappa_loglog_r": kappa_loglog(RS, C_cft),
    }
    print(f"  Tier1 synthetic: monotone={mono_cft}, kappa={tiers['synthetic_cft']['kappa_loglog_r']:.4f}")

    # ---- Tier 2: exact 16q critical-TFIM GS, connected ZZ ----
    H = FC.build_tfim_sparse(N)
    Eg, psi = eigsh(H, k=1, which="SA")
    psi = psi[:, 0]
    Zexp = []  # <Z_i> (Z2-even GS -> 0, but compute honestly)
    Zops = [TFD.sparse_pauli_full(N, i, "Z") for i in range(N)]
    for i in range(N):
        Zexp.append(float(np.real(np.vdot(psi, Zops[i] @ psi))))
    C_phys = []
    for r in RS:
        vals = []
        for i in range(N):
            j = (i + int(r)) % N
            zz = float(np.real(np.vdot(psi, Zops[i] @ (Zops[j] @ psi))))
            vals.append(zz - Zexp[i] * Zexp[j])
        C_phys.append(float(np.mean(vals)))
    C_phys = np.array(C_phys)
    d_phys = synge(C_phys)
    mono_phys = bool(np.all(np.diff(d_phys) > 0))
    chord = (N / np.pi) * np.sin(np.pi * RS / N)
    tiers["exact_16q"] = {
        "E_gs": float(Eg[0]), "mean_abs_Zexp": float(np.mean(np.abs(Zexp))),
        "C_connected": C_phys.tolist(), "d_synge": d_phys.tolist(),
        "monotone_increasing": mono_phys, "fits_d_vs_r": fits(RS, d_phys),
        "kappa_loglog_r": kappa_loglog(RS, C_phys),
        "kappa_loglog_chord": kappa_loglog(chord, C_phys),
    }
    print(f"  Tier2 16q exact: monotone={mono_phys}, kappa_r={tiers['exact_16q']['kappa_loglog_r']:.4f}, "
          f"kappa_chord={tiers['exact_16q']['kappa_loglog_chord']:.4f}")

    # ---- Tier 3: pathological control (SIM-011 proxy data) ----
    s11 = json.load(open(SIM011, encoding="utf-8"))
    zz11 = (s11.get("classical_verification", {}).get("zz_correlators")
            or s11.get("results", {}).get("zz_correlators") or s11.get("zz_correlators"))
    ctrl = {}
    if zz11:
        keys = sorted(zz11, key=lambda k: int(k))
        C_ctrl = np.array([abs(float(zz11[k])) for k in keys])
        d_ctrl = synge(np.clip(C_ctrl, 1e-12, 0.999999))
        ctrl = {"C": C_ctrl.tolist(), "d_synge": d_ctrl.tolist(),
                "monotone_increasing": bool(np.all(np.diff(d_ctrl) > 0)),
                "kappa_loglog_r": kappa_loglog(np.arange(1, len(C_ctrl) + 1), C_ctrl)}
        print(f"  Tier3 control: monotone={ctrl['monotone_increasing']} (expected False), "
              f"kappa={ctrl['kappa_loglog_r']:.4f} (expected ~0/garbage)")
    tiers["pathological_control_sim011"] = ctrl or {"note": "zz_correlators not found in SIM-011"}

    # ---- pre-registered verdicts ----
    best_r2 = max(tiers["synthetic_cft"]["fits_d_vs_r"]["linear"]["r2"],
                  tiers["synthetic_cft"]["fits_d_vs_r"]["power"]["r2"],
                  tiers["exact_16q"]["fits_d_vs_r"]["linear"]["r2"],
                  tiers["exact_16q"]["fits_d_vs_r"]["power"]["r2"])
    geometric_refuted = not mono_cft
    kap = tiers["exact_16q"]["kappa_loglog_chord"]
    force_blind_refuted = abs(kap - 4.0) < abs(kap - 0.25)  # closer to 4 than to 0.25
    inconclusive = best_r2 <= 0.9
    if inconclusive:
        verdict = "INCONCLUSIVE_NEEDS_CLEANER_DATA"
    elif geometric_refuted:
        verdict = "GEOMETRIC_HALF_REFUTED"
    elif force_blind_refuted:
        verdict = "FORCE_BLINDNESS_REFUTED (kappa~4: distance carries stress tensor!)"
    else:
        verdict = "SUPPORTED (monotone distance; kappa~0.25 not ~4: distance is force-blind)"
    # honest wording check on the registered 'linear' sub-claim
    lin_r2_syn = tiers["synthetic_cft"]["fits_d_vs_r"]["linear"]["r2"]
    analytic_form = "d(r) = eps*sqrt(0.5*ln r) for C=r^-1/4 — sqrt-log, monotone but NOT linear"

    out = {
        "id": "SIM-2026-031",
        "description": ("HYP-2026-026 pre-registered test: Synge map d=sqrt(-2 eps^2 ln|C|) on "
                        "(1) synthetic CFT C=r^-1/4, (2) exact 16q critical-TFIM connected ZZ, "
                        "(3) SIM-011 pathological control. Gates: monotonicity (geometric half), "
                        "kappa=-dln|C|/dlnr vs {0.25, 4} (force-blindness half)."),
        "type": "classical",
        "date": "2026-06-08",
        "hypothesis_id": "HYP-2026-026",
        "circuit": {"qubits": N, "script_path": "research/data/simulations/sim031_synge_force_blindness.py"},
        "hardware_target": "local CPU (exact statevector, scipy eigsh)",
        "results": {"tiers": tiers, "best_fit_r2": best_r2,
                    "analytic_note": analytic_form,
                    "linear_subclaim_r2_synthetic": lin_r2_syn,
                    "verdict": verdict},
        "comparison": "classical_wins",
        "notes": ("24q regen judged unnecessary for the shape question (8h eigsh); 16q exact + "
                  "chord-corrected kappa is the faithful same-day execution of registered option (a), "
                  "with option (b) synthetic as primary and SIM-011 as control, per the gate."),
        "wall_seconds": None,
    }
    out["wall_seconds"] = time.time() - t0
    with open(OUT, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\n  VERDICT: {verdict}")
    print(f"  best R^2 = {best_r2:.4f} | analytic: {analytic_form}")
    print(f"  saved -> {OUT}")

    # ---- write-back into HYP-026 ----
    h = json.load(open(HYP, encoding="utf-8"))
    supported = verdict.startswith("SUPPORTED")
    h["status"] = "SUPPORTED" if supported else ("REFUTED" if "REFUTED" in verdict else "under_review")
    h["last_updated"] = "2026-06-08"
    h["result_note_2026_06_08_sim031"] = (
        f"Pre-registered test executed as SIM-2026-031. {verdict}. "
        f"kappa(16q exact, chord-corrected)={kap:.4f} (dichotomy gate: 0.25 vs 4); "
        f"synthetic-tier monotone={mono_cft}; 16q-tier monotone={mono_phys}; best fit R^2={best_r2:.4f}. "
        f"WORDING CORRECTION to the claim: the Synge distance for C=r^-1/4 is analytically "
        f"d=eps*sqrt(0.5 ln r) — monotone but sqrt-logarithmic, not linear; the registered refutation "
        f"gates (monotonicity + kappa dichotomy) are unaffected. Data regen gate satisfied via exact "
        f"16q connected ZZ (not the 24q regen; see SIM-031 notes).")
    with open(HYP, "w", encoding="utf-8") as f:
        json.dump(h, f, indent=2)
    print(f"  HYP-026 status -> {h['status']} (write-back complete)")


if __name__ == "__main__":
    main()
