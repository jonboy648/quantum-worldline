"""
SIM-2026-028: Null control for the SIM-2026-027 finite-T transport amplitude result.

THE QUESTION (raised by the intent/honest-broker review of SIM-2026-027):
  SIM-2026-027 found the transport response amplitude A(beta) degrades monotonically
  (95%) as the TFD boundary heats up, matching the Wang-He horizon-absorption SIGN.
  BUT: a near-maximally-mixed state has GENERICALLY suppressed reference-subtracted
  response to ANY unitary perturbation. So monotonic A(beta) degradation with the
  same sign is ALSO what plain thermal washout predicts -- the sign alone does not
  discriminate "emergent BTZ horizon absorbs the excitation" from "hot state has low
  signal contrast."

THE TEST:
  Run the IDENTICAL TFD + transport + amplitude pipeline on a NON-HOLOGRAPHIC control
  Hamiltonian on the same L=8 doubled register and the same beta ladder, then compare
  the two A(beta) curves head-to-head.

  Control Hamiltonian: transverse-field Ising chain DEEP in the paramagnetic phase,
    H_para = - sum_j X_j - g * sum_j Z_j Z_{j+1}   (PBC),  g = 0.2  (g << 1: gapped,
  non-critical, NO emergent AdS/MERA holographic geometry, NO horizon). This is a
  generic gapped 1D system -- the canonical "no holography here" control.

  We normalize each A(beta) by its cold (beta=100) value and overlay:
    - If the holographic (Wang-He) curve and the paramagnetic control curve are
      INDISTINGUISHABLE, the SIM-2026-027 degradation is GENERIC THERMAL WASHOUT and
      carries NO holographic content -> SIM-2026-027's positive claim is NOT supported
      by the amplitude observable alone.
    - If the holographic curve degrades DIFFERENTLY (e.g. faster/slower, or with a
      crossover structure tied to the critical gap that the gapped control lacks),
      there is genuine holographic signal beyond washout.

  We quantify the difference by:
    (1) the two normalized A(beta) curves and their max pointwise gap,
    (2) a 'washout-normalized' amplitude A_tilde(beta) = A(beta) / sqrt(purity(beta)),
        which divides out the leading generic-decoherence scaling (response of a mixed
        state scales ~ with the state purity / the largest Boltzmann weight). If
        A_tilde is FLAT for the control but STRUCTURED for the holographic case, the
        structure is the non-generic (candidate-holographic) part.

  Honest-broker stance: this control is designed to be ABLE to kill SIM-2026-027's
  interpretation. A null result here (curves identical) is the correct, publishable
  outcome and demotes SIM-2026-027 to "consistent with washout."

Reuses build_tfd, embed_phys, run_transport_tfd, antipode_response from
hyp024_tfd_btz_transport.py (the verified SIM-2026-027 machinery -- imported, not copied).
"""
import json
import time
import numpy as np
from scipy.sparse import csr_matrix
from scipy.linalg import eigh

import hyp024_tfd_btz_transport as TFD

SCRIPT_START = time.time()
OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-028.json"


def build_H_paramagnetic(L, g=0.2):
    """Non-critical transverse-field Ising deep in the paramagnet (g<<1):
        H = - sum_j X_j - g sum_j Z_j Z_{j+1}   (PBC).
    Gapped, no criticality, no emergent holographic geometry. The 'no holography' control.
    """
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    for j in range(L):
        H += -1.0 * TFD.sparse_pauli_full(L, j, "X")
    for j in range(L):
        jp1 = (j + 1) % L
        H += -g * (TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp1, "Z"))
    return H


def run_ladder(H_sparse, label, L, beta_ladder):
    """Run the TFD + transport + amplitude pipeline on H_sparse across the beta ladder.
    Returns a list of per-beta dicts (beta, A_int, A_pk, gs_pop, N_eff, purity, S_th)."""
    dimL = 2 ** L
    dimR = 2 ** L
    H_dense = H_sparse.toarray()
    evals, evecs = eigh(H_dense)
    gap = float(evals[1] - evals[0])
    print(f"\n[{label}] E_gs={evals[0]:.5f}, gap={gap:.5f}, width={evals[-1]-evals[0]:.4f}", flush=True)

    Y_L = TFD.build_Y_ops(L)
    Y_full = [TFD.embed_phys(y, dimR) for y in Y_L]
    H_full = TFD.embed_phys(H_sparse, dimR)
    psi_gs = evecs[:, 0].astype(complex)

    rows = []
    for beta in beta_ladder:
        t0 = time.time()
        psi_tfd, info = TFD.build_tfd(H_dense, beta)
        gs_pop = TFD.reduced_phys_overlap_with_gs(psi_tfd, psi_gs, dimL)
        purity = float(np.sum(np.array(info["boltzmann_probs"]) ** 2))
        times_x, rho_x, bd_x = TFD.run_transport_tfd(psi_tfd, psi_tfd, H_full, Y_full, L)
        amp = TFD.antipode_response(times_x, bd_x, L)
        dt = time.time() - t0
        print(f"    beta={beta:>9.4f} | A_int={amp['integrated_global']:.5f} "
              f"A_pk={amp['peak_global']:.5f} | gs_pop={gs_pop:.4f} | purity={purity:.4f} | "
              f"N_eff={info['participation_ratio']:.2f} | {dt:.1f}s", flush=True)
        rows.append({
            "beta": float(beta), "temperature": float(1.0 / beta),
            "A_integrated_global": amp["integrated_global"],
            "A_peak_global": amp["peak_global"],
            "gs_population": gs_pop,
            "purity": purity,
            "participation_ratio": info["participation_ratio"],
            "thermal_entropy": info["thermal_entropy"],
        })
    return rows, gap


def main():
    import sys
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 8
    print("=" * 72)
    print(f"SIM-2026-028: NULL CONTROL for SIM-2026-027 amplitude degradation (L={L})")
    print("Holographic (Wang-He critical Ising) vs non-holographic (paramagnet)")
    print("=" * 72, flush=True)

    BETA_LADDER = [100.0, 20.0, 8.0, 5.0, 3.0, 2.0, 1.0, 0.5, 0.25]

    # Holographic arm (identical to SIM-2026-027).
    H_holo = TFD.build_H_boundary(L)
    holo_rows, holo_gap = run_ladder(H_holo, "HOLOGRAPHIC Wang-He", L, BETA_LADDER)

    # Non-holographic control arm.
    H_ctrl = build_H_paramagnetic(L, g=0.2)
    ctrl_rows, ctrl_gap = run_ladder(H_ctrl, "CONTROL paramagnet g=0.2", L, BETA_LADDER)

    # ── Compare normalized curves ──
    betas = np.array([r["beta"] for r in holo_rows])
    order = np.argsort(betas)

    def norm_curve(rows, key):
        a = np.array([r[key] for r in rows])[order]
        cold = a[-1]                       # beta=100 is largest after sort
        return a / cold if cold > 1e-12 else a

    holo_A = norm_curve(holo_rows, "A_integrated_global")
    ctrl_A = norm_curve(ctrl_rows, "A_integrated_global")

    # Washout-normalized: divide out sqrt(purity) (leading generic-decoherence scaling).
    def washout_norm(rows):
        a = np.array([r["A_integrated_global"] for r in rows])[order]
        pur = np.array([r["purity"] for r in rows])[order]
        at = a / np.sqrt(np.maximum(pur, 1e-12))
        return at / at[-1] if at[-1] > 1e-12 else at

    holo_At = washout_norm(holo_rows)
    ctrl_At = washout_norm(ctrl_rows)

    max_gap_raw = float(np.max(np.abs(holo_A - ctrl_A)))
    max_gap_washout = float(np.max(np.abs(holo_At - ctrl_At)))
    # Spearman of each vs beta (both should be +1 if both just wash out).
    holo_sp = TFD._spearman(betas[order], holo_A)
    ctrl_sp = TFD._spearman(betas[order], ctrl_A)

    betas_sorted = betas[order]
    print("\n" + "=" * 72)
    print("[COMPARE] normalized A(beta)/A(cold):")
    print(f"  {'beta':>9} | {'holo':>8} | {'control':>8} | {'gap':>8} | "
          f"{'holo_wn':>8} | {'ctrl_wn':>8}")
    for i in range(len(betas_sorted)):
        print(f"  {betas_sorted[i]:>9.4f} | {holo_A[i]:>8.4f} | {ctrl_A[i]:>8.4f} | "
              f"{abs(holo_A[i]-ctrl_A[i]):>8.4f} | {holo_At[i]:>8.4f} | {ctrl_At[i]:>8.4f}")

    print(f"\n  max |holo - control| (raw normalized)      = {max_gap_raw:.4f}")
    print(f"  max |holo - control| (washout-normalized)  = {max_gap_washout:.4f}")
    print(f"  Spearman(beta, A) holo={holo_sp:.3f}, control={ctrl_sp:.3f}")

    # ── Verdict ──
    # If raw curves are within 10% everywhere -> washout dominates, no holographic content.
    # If washout-normalized curves differ by >15% -> non-generic (candidate-holographic) signal.
    DISTINGUISHABLE_RAW = 0.10
    DISTINGUISHABLE_WASHOUT = 0.15

    if max_gap_washout > DISTINGUISHABLE_WASHOUT:
        verdict = "HOLOGRAPHIC_SIGNAL_BEYOND_WASHOUT"
        reason = (f"After dividing out the generic sqrt(purity) decoherence scaling, the "
                  f"holographic and control A_tilde(beta) curves still differ by "
                  f"{max_gap_washout*100:.1f}% (>{DISTINGUISHABLE_WASHOUT*100:.0f}%). The "
                  f"SIM-2026-027 degradation contains structure NOT explained by generic "
                  f"thermal washout -- consistent with (though still not proof of) "
                  f"holographic horizon absorption.")
    elif max_gap_raw < DISTINGUISHABLE_RAW:
        verdict = "WASHOUT_DOMINATES"
        reason = (f"The holographic and non-holographic normalized A(beta) curves are "
                  f"indistinguishable (max gap {max_gap_raw*100:.1f}% < "
                  f"{DISTINGUISHABLE_RAW*100:.0f}%). The SIM-2026-027 monotonic amplitude "
                  f"degradation is GENERIC THERMAL WASHOUT and carries no holographic "
                  f"content by itself. SIM-2026-027's positive claim must be demoted to "
                  f"'consistent with washout'; the horizon-absorption interpretation needs "
                  f"the (finite-size-limited) functional-form / Gamma-QNM observables.")
    else:
        verdict = "PARTIAL_DISTINCTION"
        reason = (f"The curves differ at the raw level (max gap {max_gap_raw*100:.1f}%) but "
                  f"the washout-normalized difference ({max_gap_washout*100:.1f}%) is below "
                  f"the {DISTINGUISHABLE_WASHOUT*100:.0f}% threshold. Suggestive of some "
                  f"non-generic structure but not decisive; needs N=10/12 cross-check.")

    print(f"\n[VERDICT] {verdict}\n  {reason}", flush=True)

    output = {
        "id": "SIM-2026-028",
        "description": ("Null control for SIM-2026-027: compares finite-T transport "
                        "amplitude A(beta) for the holographic Wang-He critical-Ising "
                        "boundary vs a non-holographic paramagnetic control on the same "
                        "TFD L=8 register + beta ladder. Tests whether the SIM-2026-027 "
                        "amplitude degradation is holographic horizon absorption or "
                        "generic thermal washout."),
        "type": "classical",
        "date": "2026-05-28",
        "hypothesis_id": "HYP-2026-024",
        "relates_to": "SIM-2026-027",
        "hardware_target": "local_cpu",
        "results": {
            "verdict": verdict,
            "verdict_reason": reason,
            "holographic_hamiltonian": "Wang-He critical Ising: (L/4pi) sum_j [X_{j-1}Z_jX_{j+1} - X_jX_{j+1}], PBC",
            "control_hamiltonian": "Paramagnet: - sum_j X_j - 0.2 sum_j Z_jZ_{j+1}, PBC (gapped, non-critical, no holography)",
            "holographic_gap": holo_gap,
            "control_gap": ctrl_gap,
            "beta_ladder": BETA_LADDER,
            "max_gap_raw_normalized": max_gap_raw,
            "max_gap_washout_normalized": max_gap_washout,
            "spearman_beta_A_holo": holo_sp,
            "spearman_beta_A_control": ctrl_sp,
            "normalized_curves": {
                "beta": betas_sorted.tolist(),
                "holo_A_norm": holo_A.tolist(),
                "control_A_norm": ctrl_A.tolist(),
                "holo_A_washout_norm": holo_At.tolist(),
                "control_A_washout_norm": ctrl_At.tolist(),
            },
            "holographic_ladder": holo_rows,
            "control_ladder": ctrl_rows,
            "total_wall_time_s": time.time() - SCRIPT_START,
        },
        "comparison": "classical_wins",
        "notes": ("Honest-broker null control mandated by the intent review of SIM-2026-027. "
                  "Designed to be able to KILL the holographic interpretation. A "
                  "WASHOUT_DOMINATES verdict is the correct, publishable outcome if the "
                  "amplitude sign is generic."),
    }
    # L=8 writes the canonical SIM-2026-028.json; larger L writes an L-tagged
    # finite-size cross-check file so it does not clobber the canonical record.
    out_path = OUT_PATH if L == 8 else OUT_PATH.replace(".json", f"-L{L}.json")
    output["finite_size_crosscheck_of"] = "SIM-2026-028" if L != 8 else None
    output["L_physical"] = L
    with open(out_path, "w") as f:
        json.dump(output, f, indent=2)
    print(f"\nSaved to {out_path}")
    print(f"Total wall time: {time.time()-SCRIPT_START:.0f}s")


if __name__ == "__main__":
    main()
