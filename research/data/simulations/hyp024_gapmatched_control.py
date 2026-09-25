"""
SIM-2026-030: Gap-matched null control -- the decisive test of SIM-2026-028's
"HOLOGRAPHIC_SIGNAL_BEYOND_WASHOUT" verdict.

THE PROBLEM (raised by the 2026-05-29 red-team of SIM-027/028):
SIM-028 compared the holographic Wang-He boundary chain (spectral gap 0.1254 at L=8)
against a paramagnet control g=0.2 (gap 1.600). That is a 13x gap mismatch baked into
the comparison, so "holographic vs non-holographic" is perfectly CONFOUNDED with
"small gap vs large gap". The control sits far deeper in the frozen/all-washout regime
by construction. SIM-028's discriminator (washout-normalized amplitude sub-unity for
holographic, flat for control) may therefore measure the GAP, not criticality/horizon.

THE DECISIVE TEST:
Replace the gap-1.60 paramagnet with NON-CRITICAL controls whose spectral gap EQUALS
the holographic gap 0.12540 at L=8. If a gap-matched non-critical chain reproduces the
holographic sub-unity washout-normalized residual, then SIM-028 measured "small gap",
not horizon physics -> verdict KILLED. If the gap-matched control stays flat ~1.0, the
holographic verdict SURVIVES a far stronger null.

TWO independent gap-matched controls (agreement = robustness check):
  (A) Energy-rescaled gapped chain  H_A = lambda*(-sum X - 0.5 sum ZZ),  lambda=0.125221
      -> gap 0.125403 (exact, linear in lambda). Manifestly non-critical, no degeneracy. PRIMARY.
  (B) Ferromagnetic TFI  H_B = -sum X - g* sum ZZ,  g*=1.09620  -> gap 0.125403.
      Non-critical (ordered phase), independent functional form. SECONDARY.
Both gaps root-found/verified against the holographic gap to 1e-6.

REFUTATION CRITERION:
- SIM-028 verdict KILLED if a gap-matched control reproduces the holographic
  washout-normalized residual within 3% RMS over beta>=0.5 (i.e. max|holo - control| small).
- SIM-028 verdict SURVIVES if gap-matched control stays flat ~1.0
  (max|holo - control| > 0.15 over beta>=0.5).

Reuses verified machinery from hyp024_tfd_null_control.py (build_tfd, embed_phys,
run_ladder, antipode amplitude). Exact diagonalization, L=8 doubled register (2^16).
"""
import json
import time
import numpy as np
from scipy.sparse import csr_matrix

import hyp024_tfd_btz_transport as TFD
import hyp024_tfd_null_control as NC

SCRIPT_START = time.time()
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-030.json"


def build_rescaled_gapped(L, lam, J=0.5):
    """H = lambda*(-sum_j X_j - J sum_j Z_j Z_{j+1}), PBC. Non-critical (J=0.5 != 1);
    gap is linear in lambda. lam=0.125221 -> gap 0.125403 at L=8 (matches holo gap)."""
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    for j in range(L):
        H = H - lam * TFD.sparse_pauli_full(L, j, "X")
    for j in range(L):
        jp = (j + 1) % L
        H = H - lam * J * (TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp, "Z"))
    return H


def build_ferro_tfi(L, g):
    """H = -sum_j X_j - g sum_j Z_j Z_{j+1}, PBC. g>1 = ordered (non-critical) phase.
    g*=1.09620 -> gap 0.125403 at L=8."""
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    for j in range(L):
        H = H - TFD.sparse_pauli_full(L, j, "X")
    for j in range(L):
        jp = (j + 1) % L
        H = H - g * (TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp, "Z"))
    return H


def gap_of(H_sparse):
    ev = np.sort(np.linalg.eigvalsh(H_sparse.toarray()).real)
    return float(ev[1] - ev[0])


def washout_norm_curve(rows, order):
    """A/sqrt(purity) normalized to cold (largest beta). Same definition as SIM-028."""
    a = np.array([r["A_integrated_global"] for r in rows])[order]
    pur = np.array([r["purity"] for r in rows])[order]
    at = a / np.sqrt(np.maximum(pur, 1e-12))
    return at / at[-1] if at[-1] > 1e-12 else at


def main():
    L = 8
    BETA_LADDER = [100.0, 20.0, 8.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.25]
    LAMBDA_STAR = 0.125221     # rescaled-control gap match (verified gap 0.125403)
    G_STAR = 1.09620           # ferromagnetic-control gap match (verified gap 0.125403)

    print("=" * 74)
    print("SIM-2026-030: GAP-MATCHED control -- decisive test of SIM-028 verdict")
    print("=" * 74, flush=True)

    # Build the three Hamiltonians and VERIFY gaps match before running.
    H_holo = TFD.build_H_boundary(L)
    H_rescaled = build_rescaled_gapped(L, LAMBDA_STAR)
    H_ferro = build_ferro_tfi(L, G_STAR)
    H_paramagnet = NC.build_H_paramagnetic(L, g=0.2)   # the ORIGINAL (gap-mismatched) control

    gaps = {
        "holographic": gap_of(H_holo),
        "rescaled_gapmatched": gap_of(H_rescaled),
        "ferro_gapmatched": gap_of(H_ferro),
        "paramagnet_original": gap_of(H_paramagnet),
    }
    print("[gap check]")
    for k, v in gaps.items():
        print(f"    {k:>22}: gap = {v:.6f}")
    gap_match_ok = (abs(gaps["rescaled_gapmatched"] - gaps["holographic"]) < 1e-3 and
                    abs(gaps["ferro_gapmatched"] - gaps["holographic"]) < 1e-3)
    print(f"    gap-match within 1e-3: {'PASS' if gap_match_ok else 'FAIL'}\n", flush=True)

    # Run all arms through the SAME verified ladder machinery (NC.run_ladder).
    arms = {}
    for name, H in [("holographic", H_holo),
                    ("rescaled_gapmatched", H_rescaled),
                    ("ferro_gapmatched", H_ferro),
                    ("paramagnet_original", H_paramagnet)]:
        print(f"--- arm: {name} ---", flush=True)
        rows, gap = NC.run_ladder(H, name, L, BETA_LADDER)
        arms[name] = rows

    # Compare washout-normalized curves.
    betas = np.array([r["beta"] for r in arms["holographic"]])
    order = np.argsort(betas)
    betas_sorted = betas[order]
    wn = {name: washout_norm_curve(rows, order) for name, rows in arms.items()}

    # Restrict comparison to beta>=0.5 (the SIM-028 "interesting" regime).
    mask = betas_sorted >= 0.5
    def rms_gap(a, b):
        return float(np.sqrt(np.mean((a[mask] - b[mask]) ** 2)))
    def max_gap(a, b):
        return float(np.max(np.abs(a[mask] - b[mask])))

    holo = wn["holographic"]
    cmp = {}
    for name in ("rescaled_gapmatched", "ferro_gapmatched", "paramagnet_original"):
        cmp[name] = {"rms_vs_holo_beta_ge_0.5": rms_gap(holo, wn[name]),
                     "max_vs_holo_beta_ge_0.5": max_gap(holo, wn[name])}

    print("\n" + "=" * 74)
    print("[COMPARE] washout-normalized A/sqrt(purity), normalized to cold:")
    print(f"  {'beta':>7} | {'holo':>7} | {'rescaled':>9} | {'ferro':>7} | {'paramag':>8}")
    for i in range(len(betas_sorted)):
        print(f"  {betas_sorted[i]:>7.2f} | {holo[i]:>7.4f} | {wn['rescaled_gapmatched'][i]:>9.4f} | "
              f"{wn['ferro_gapmatched'][i]:>7.4f} | {wn['paramagnet_original'][i]:>8.4f}")
    print()
    for name, d in cmp.items():
        print(f"  holo vs {name}: RMS(beta>=0.5)={d['rms_vs_holo_beta_ge_0.5']:.4f}, "
              f"max={d['max_vs_holo_beta_ge_0.5']:.4f}")

    # ── VERDICT ──
    # KILLED if a gap-matched control REPRODUCES the holo residual (RMS < 0.03).
    # SURVIVES if gap-matched controls stay AWAY from holo (max > 0.15), like the paramagnet.
    rescaled_reproduces = cmp["rescaled_gapmatched"]["rms_vs_holo_beta_ge_0.5"] < 0.03
    ferro_reproduces = cmp["ferro_gapmatched"]["rms_vs_holo_beta_ge_0.5"] < 0.03
    rescaled_far = cmp["rescaled_gapmatched"]["max_vs_holo_beta_ge_0.5"] > 0.15
    ferro_far = cmp["ferro_gapmatched"]["max_vs_holo_beta_ge_0.5"] > 0.15

    if rescaled_reproduces or ferro_reproduces:
        verdict = "SIM028_KILLED_GAP_ARTIFACT"
        reason = (f"A gap-matched NON-CRITICAL control reproduces the holographic washout-normalized "
                  f"residual within 3% RMS (rescaled RMS={cmp['rescaled_gapmatched']['rms_vs_holo_beta_ge_0.5']:.3f}, "
                  f"ferro RMS={cmp['ferro_gapmatched']['rms_vs_holo_beta_ge_0.5']:.3f}). The SIM-028 "
                  f"'beyond washout' signal is a GAP artifact, not criticality/horizon. HYP-024 "
                  f"amplitude claim must be demoted to 'gap-driven washout', NOT holographic.")
    elif rescaled_far and ferro_far:
        verdict = "SIM028_SURVIVES_STRONGER_NULL"
        reason = (f"Both gap-matched non-critical controls stay flat (away from holo: rescaled "
                  f"max={cmp['rescaled_gapmatched']['max_vs_holo_beta_ge_0.5']:.3f}, ferro "
                  f"max={cmp['ferro_gapmatched']['max_vs_holo_beta_ge_0.5']:.3f} > 0.15) while the "
                  f"holographic chain dips sub-unity. The sub-unity residual is NOT a gap artifact -- "
                  f"it survives a gap-matched null. SIM-028 verdict strengthened.")
    else:
        verdict = "AMBIGUOUS"
        reason = (f"Gap-matched controls land between reproduce (<3% RMS) and far (>0.15 max). "
                  f"rescaled RMS={cmp['rescaled_gapmatched']['rms_vs_holo_beta_ge_0.5']:.3f}/"
                  f"max={cmp['rescaled_gapmatched']['max_vs_holo_beta_ge_0.5']:.3f}; "
                  f"ferro RMS={cmp['ferro_gapmatched']['rms_vs_holo_beta_ge_0.5']:.3f}/"
                  f"max={cmp['ferro_gapmatched']['max_vs_holo_beta_ge_0.5']:.3f}. "
                  f"Partial gap contribution; needs finer analysis (e.g. beta*Delta collapse).")

    print(f"\n[VERDICT] {verdict}\n  {reason}", flush=True)

    output = {
        "id": "SIM-2026-030",
        "description": ("Gap-matched null control: decisive test of whether SIM-028's "
                        "HOLOGRAPHIC_SIGNAL_BEYOND_WASHOUT verdict is a spectral-gap artifact. "
                        "Compares holographic chain vs TWO non-critical controls with gap tuned "
                        "to equal the holographic gap (0.1254) at L=8, plus the original "
                        "gap-mismatched paramagnet for reference."),
        "type": "classical", "date": "2026-05-29", "hypothesis_id": "HYP-2026-024",
        "relates_to": ["SIM-2026-027", "SIM-2026-028"],
        "hardware_target": "local_cpu",
        "results": {
            "verdict": verdict, "verdict_reason": reason,
            "gaps": gaps, "gap_match_ok": gap_match_ok,
            "lambda_star_rescaled": LAMBDA_STAR, "g_star_ferro": G_STAR,
            "beta_ladder": BETA_LADDER,
            "washout_normalized_curves": {
                "beta": betas_sorted.tolist(),
                **{name: wn[name].tolist() for name in wn},
            },
            "comparisons_beta_ge_0.5": cmp,
            "arms_full": arms,
            "total_wall_time_s": time.time() - SCRIPT_START,
        },
        "classical_baseline": {
            "method": "Exact statevector TFD on doubled 16-qubit register; reuses hyp024_tfd_null_control.run_ladder",
            "controls": {
                "rescaled_gapmatched": f"lambda(-sumX-0.5 sumZZ), lambda={LAMBDA_STAR}, gap-matched to 0.1254",
                "ferro_gapmatched": f"-sumX - g sumZZ, g={G_STAR} (ordered phase), gap-matched to 0.1254",
                "paramagnet_original": "-sumX - 0.2 sumZZ (gap 1.60, ORIGINAL mismatched SIM-028 control)",
            },
        },
        "comparison": "classical_wins",
        "notes": ("SIM-2026-030 removes the 13x gap confound from SIM-028 by gap-matching the "
                  "non-critical control. This is the decisive falsification test of the "
                  "'beyond washout = holography' claim, generated by the autonomous frontier "
                  "workflow and prioritized #1 by significance x tractability."),
    }
    with open(OUT_PATH, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {OUT_PATH}\nTotal wall time: {time.time()-SCRIPT_START:.0f}s", flush=True)


if __name__ == "__main__":
    main()
