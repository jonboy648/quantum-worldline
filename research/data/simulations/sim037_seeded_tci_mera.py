"""
SIM-2026-037 — HYP-2026-027 stage-2b: ESCAPE the chi=3 product-state collapse (per ERRATA D5).

SIM-036 proved (ERRATA D5) that chi=3 has the capacity (99.99% of the exact TCI GS) but the
optimizer collapsed into a near-product local minimum (S_half 0.0002, rank 4) from random*0.1
init on the flat multicritical landscape. This script attacks the ROOT CAUSE — initialization /
landscape — not the bond dimension.

We do NOT need DMRG/MPS tensor surgery: the exact GS is already cheap at N=16, and the real fix
is to start the optimizer in an ENTANGLED basin. Two levers, numpy-only:
  (A) INIT-SCALE SWEEP — random*0.1 makes near-identity gates -> near-product start. Try larger
      init scales {0.1, 0.3, 0.6, 1.0} x multiple seeds; bigger/structured init may land in an
      entangled basin directly. Cheapest possible fix; test first.
  (B) ENTANGLEMENT-WARMUP objective — for early rounds minimize <H> - lambda*S_half (reward
      entanglement), then anneal lambda -> 0 so energy takes over. Forces the optimizer out of the
      product minimum first. Used only if (A) alone doesn't clear the gate.

GATE (the SIM-036 lesson, now enforced): a run "succeeds" only if it reaches BOTH low energy
(rel_err < ~0.3%) AND faithful entanglement (S_half/S_exact > 0.9) AND overlap > 0.95. Energy
alone is NOT convergence.

Reuses the MERA builder + Hamiltonian from sim036 (import; its main is under __main__).
Checkpoints the best theta to theta_seeded_SIM2026037.npy every (seed,round). If a seeded chi=3
reaches the gate -> proceed to the Koo-Saleur force read-out (the actual alpha-universality
deliverable). If NO seed/warmup clears it -> THEN the capacity argument is real and chi=4 is
justified (and we'll have earned that conclusion honestly).
Output: research/data/simulations/SIM-2026-037.json.
"""
import json
import time

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh

import sim036_tci_mera_stage2 as S2

N = S2.N_QUBITS
NP = S2.N_PARAMS
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-037.json"
CKPT = "D:/quantum-worldline/research/data/simulations/theta_seeded_SIM2026037.npy"
INIT_SCALES = [0.3, 0.6, 1.0]   # 0.1 already failed in SIM-036; skip it
ROUNDS = 4                       # per seed; energy converged fast in SIM-036
WARMUP_LAMBDA = 0.5              # entanglement reward strength for lever (B)


def half_S(sv):
    l = N // 2
    m = sv.reshape(2 ** l, 2 ** (N - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


def main():
    t0 = time.time()
    print("=" * 70)
    print("SIM-2026-037: seeded chi=3 TCI MERA — escape the product-state collapse")
    print("=" * 70)
    H = S2.build_OF_tricritical(N)
    Earr, gsarr = eigsh(H, k=1, which="SA")
    E0 = float(Earr[0]); gs_exact = S2.project_z2(gsarr[:, 0], N)
    S_exact = half_S(gs_exact)
    print(f"exact: E0={E0:.5f}  S_half_exact={S_exact:.4f}")

    def energy(p):
        sv = S2.build_mera_sv(p)
        return float(np.real(np.vdot(sv, H @ sv)))

    def warmup_loss(p, lam):
        sv = S2.build_mera_sv(p)
        E = float(np.real(np.vdot(sv, H @ sv)))
        return E - lam * half_S(S2.project_z2(sv, N))

    best = None  # (gate_pass, -rel_err, theta, metrics)
    trials = []
    rng = np.random.default_rng(7)

    for scale in INIT_SCALES:
        for seed in range(2):  # 2 seeds per scale
            theta = rng.standard_normal(NP) * scale
            # lever B: 1 warmup round rewarding entanglement, then energy rounds
            r = minimize(lambda p: warmup_loss(p, WARMUP_LAMBDA), theta,
                         method="L-BFGS-B", options={"maxiter": 200, "ftol": 1e-9})
            theta = r.x
            bestE = energy(theta)
            for rnd in range(ROUNDS):
                r = minimize(energy, theta, method="L-BFGS-B",
                             options={"maxiter": 400, "ftol": 1e-11, "gtol": 1e-8})
                if r.fun < bestE:
                    bestE = r.fun; theta = r.x
            sv = S2.project_z2(S2.build_mera_sv(theta), N)
            E_m = energy(theta)
            rel = abs(E_m - E0) / abs(E0) * 100
            ov = float(abs(np.vdot(gs_exact, sv)) ** 2)
            S_m = half_S(sv)
            sratio = S_m / S_exact if S_exact else 0.0
            gate = rel < 0.3 and ov > 0.95 and sratio > 0.9
            metrics = {"init_scale": scale, "seed": seed, "rel_err_pct": rel,
                       "overlap": ov, "S_half": S_m, "S_ratio": sratio, "gate_pass": gate}
            trials.append(metrics)
            print(f"  scale={scale} seed={seed} | rel={rel:.3f}% ov={ov:.4f} "
                  f"S={S_m:.4f} (ratio {sratio:.3f}) | {'GATE PASS' if gate else 'collapsed'}", flush=True)
            key = (gate, -rel)
            if best is None or key > best[0]:
                best = (key, theta, metrics)
                np.save(CKPT, theta)

    best_metrics = best[2]
    any_pass = any(t["gate_pass"] for t in trials)
    best_S = max(t["S_half"] for t in trials)
    if any_pass:
        verdict = (f"PRODUCT-COLLAPSE ESCAPED: a seeded chi=3 MERA reached the gate "
                   f"(rel_err {best_metrics['rel_err_pct']:.3f}%, overlap {best_metrics['overlap']:.4f}, "
                   f"S_half {best_metrics['S_half']:.4f}/{S_exact:.4f}). chi=3 is SUFFICIENT (confirms "
                   f"ERRATA D5: SIM-036 was an optimizer failure). NEXT: Koo-Saleur force read-out on "
                   f"this state -> the alpha-universality answer. Checkpoint: theta_seeded_SIM2026037.npy.")
        status = "CHI3_SUFFICIENT_PROCEED_TO_FORCE"
    else:
        verdict = (f"Seeding did not clear the entanglement gate (best S_half {best_S:.4f} vs "
                   f"{S_exact:.4f} across {len(trials)} init-scale/seed/warmup trials). Either the "
                   f"landscape needs a stronger method (true DMRG seed / imaginary-time) OR chi=3 "
                   f"genuinely saturates here — at which point chi=4 becomes justified. Honest: do NOT "
                   f"jump to chi=4 yet; try a true MPS seed (install quimb) first.")
        status = "SEEDING_INSUFFICIENT_TRY_MPS_SEED"

    out = {"id": "SIM-2026-037", "type": "classical", "date": "2026-06-17",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage-2b: escape the SIM-036 chi=3 product-state collapse via init-scale "
                           "sweep + entanglement-warmup objective (ERRATA D5 fix). Gate enforces "
                           "energy AND entanglement AND overlap."),
           "circuit": {"qubits": N, "chi": 3, "n_params": NP,
                       "script_path": "research/data/simulations/sim037_seeded_tci_mera.py",
                       "theta_checkpoint": CKPT},
           "hardware_target": "local CPU",
           "results": {"E_exact": E0, "S_half_exact": S_exact, "trials": trials,
                       "best": best_metrics, "any_gate_pass": any_pass, "best_S_half": best_S,
                       "status": status, "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Attacks initialization/landscape (the real SIM-036 failure), not bond dimension.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\n  VERDICT:", verdict)
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
