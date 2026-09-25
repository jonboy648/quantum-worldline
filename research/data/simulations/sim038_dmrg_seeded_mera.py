"""
SIM-2026-038 - HYP-2026-027 stage-2c: TARGET-SEEDED chi=3 MERA at the tricritical Ising point.

The resolving move per ERRATA D5 and the SIM-037 negative. SIM-036/037 proved chi=3 has the
CAPACITY (99.99% of the exact TCI GS) but random/cheap seeds collapse the optimizer into a
near-product local minimum (S_half ~ 0.0001 vs exact 0.1795). SIM-037 showed a soft entanglement
PENALTY cannot escape it (its gradient vanishes AT the product state).

This script attacks the basin with a STRUCTURED target. The target is the EXACT N=16 ground state
(from eigsh, already in hand) -- which is strictly better than a truncated DMRG/MPS seed (we tried
quimb DMRG; the exact GS at N=16 is free and faithful, so no truncation is needed). Strategy
(route A, state-vector overlap seed):
  1. psi_target = exact TCI ground state (E0=-32.7028, S_half=0.1795).
  2. PRE-OPTIMIZE the MERA's 1246 angles to MAXIMIZE OVERLAP with psi_target:
        loss_overlap(theta) = 1 - |<psi_target | mera(theta)>|^2
     This objective has a NON-VANISHING gradient at the product state (the entangled target pulls
     the optimizer uphill into the entangled basin) -- exactly the force the SIM-037 S-penalty lacked.
  3. ANNEAL to ENERGY: once overlap is high (state is in the right basin), switch to pure energy
     minimization to polish to the variational optimum.
  4. GATE (the SIM-036 lesson): success requires rel_err<0.3% AND overlap>0.95 AND S_ratio>0.9.

SCIENTIFIC FRAMING (stated plainly): this is a REPRESENTABILITY demonstration -- it answers the
ERRATA D5 question "can a chi=3 MERA faithfully represent the TCI ground state?" by fitting the MERA
to the exact GS, escaping the product-state local minimum that blind energy minimization fell into.
It is NOT a from-scratch blind-variational result. That is exactly what we need: the subsequent
Koo-Saleur force read-out is a property of the converged MERA TENSORS (its scaling superoperator),
independent of how they were initialized. A faithful chi=3 representation is the prerequisite; the
seed is scaffolding to reach it, and the final state is still gated on energy AND entanglement AND
overlap independently.

If a target-seeded chi=3 clears the gate -> chi=3 is SUFFICIENT (ERRATA D5 confirmed), proceed to the
Koo-Saleur force read-out (the alpha-universality deliverable). If it STILL collapses -> only THEN
is chi=4 honestly justified.

Reuses sim036's MERA builder + Hamiltonian + Z2 projection (import). Checkpoints best theta to
theta_dmrgseed_SIM2026038.npy every stage so a kill never loses work.
Output: research/data/simulations/SIM-2026-038.json.
"""
import json
import os
import time

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh

import sim036_tci_mera_stage2 as S2

N = S2.N_QUBITS
NP = S2.N_PARAMS
LAM3 = S2.LAM3
LAMI = S2.LAMI
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-038.json"
CKPT = "D:/quantum-worldline/research/data/simulations/theta_dmrgseed_SIM2026038.npy"

OVERLAP_ROUNDS = 6     # pre-optimization toward the DMRG target
ENERGY_ROUNDS = 6      # polish to the variational optimum


def half_S(sv):
    l = N // 2
    m = sv.reshape(2 ** l, 2 ** (N - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


def main():
    t0 = time.time()
    print("=" * 70)
    print("SIM-2026-038: DMRG-seeded chi=3 TCI MERA - escape the product collapse via a structured target")
    print("=" * 70)

    # exact reference (ground truth gate AND the seed target)
    H = S2.build_OF_tricritical(N)
    Earr, gsarr = eigsh(H, k=1, which="SA")
    E0 = float(Earr[0]); gs_exact = S2.project_z2(gsarr[:, 0], N)
    S_exact = half_S(gs_exact)
    print(f"exact: E0={E0:.6f}  S_half_exact={S_exact:.4f}", flush=True)

    # seed target = the exact GS itself (faithful, free at N=16; better than a truncated MPS)
    psi_t = gs_exact
    E_dmrg = E0
    dmrg_ov = 1.0

    def energy(p):
        sv = S2.build_mera_sv(p)
        return float(np.real(np.vdot(sv, H @ sv)))

    def neg_overlap(p):
        sv = S2.build_mera_sv(p)
        return float(1.0 - abs(np.vdot(psi_t, sv)) ** 2)

    rng = np.random.default_rng(11)
    if os.path.exists(CKPT):
        theta = np.load(CKPT)
        print(f"  RESUMING from {CKPT}", flush=True)
    else:
        theta = rng.standard_normal(NP) * 0.1

    # STAGE 1: pre-optimize overlap with the DMRG target (climbs into the entangled basin)
    for rnd in range(1, OVERLAP_ROUNDS + 1):
        r = minimize(neg_overlap, theta, method="L-BFGS-B",
                     options={"maxiter": 400, "ftol": 1e-12, "gtol": 1e-9})
        theta = r.x
        sv = S2.project_z2(S2.build_mera_sv(theta), N)
        ov = float(abs(np.vdot(gs_exact, sv)) ** 2)
        S_m = half_S(sv)
        np.save(CKPT, theta)
        print(f"  [overlap {rnd}/{OVERLAP_ROUNDS}] 1-|<t|m>|^2={r.fun:.3e}  "
              f"ov-exact={ov:.4f}  S={S_m:.4f}", flush=True)

    # STAGE 2: anneal to energy minimization (polish to variational optimum)
    bestE = energy(theta)
    for rnd in range(1, ENERGY_ROUNDS + 1):
        r = minimize(energy, theta, method="L-BFGS-B",
                     options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-9})
        if r.fun < bestE:
            bestE = r.fun; theta = r.x
        np.save(CKPT, theta)
        rel = abs(bestE - E0) / abs(E0) * 100
        S_m = half_S(S2.project_z2(S2.build_mera_sv(theta), N))
        print(f"  [energy {rnd}/{ENERGY_ROUNDS}] E={bestE:.6f}  rel={rel:.4f}%  S={S_m:.4f}", flush=True)

    # final gate
    sv = S2.project_z2(S2.build_mera_sv(theta), N)
    E_m = energy(theta)
    rel = abs(E_m - E0) / abs(E0) * 100
    ov = float(abs(np.vdot(gs_exact, sv)) ** 2)
    S_m = half_S(sv)
    sratio = S_m / S_exact if S_exact else 0.0
    gate = rel < 0.3 and ov > 0.95 and sratio > 0.9

    if gate:
        verdict = (f"PRODUCT-COLLAPSE ESCAPED via DMRG seed: chi=3 reached the gate "
                   f"(rel_err {rel:.3f}%, overlap {ov:.4f}, S_half {S_m:.4f}/{S_exact:.4f}, "
                   f"ratio {sratio:.3f}). chi=3 IS SUFFICIENT for the TCI point (confirms ERRATA D5). "
                   f"NEXT: Koo-Saleur scaling-superoperator force read-out on this faithful state -> "
                   f"the alpha-universality answer. Checkpoint: theta_dmrgseed_SIM2026038.npy.")
        status = "CHI3_SUFFICIENT_PROCEED_TO_FORCE"
    else:
        verdict = (f"Even a DMRG-seeded chi=3 did NOT clear the gate (rel {rel:.3f}%, ov {ov:.4f}, "
                   f"S {S_m:.4f}/{S_exact:.4f}, ratio {sratio:.3f}). If S is still ~0 the seed didn't "
                   f"take (overlap pre-opt failed); if S grew but plateaued below 0.9*S_exact, THEN "
                   f"chi=3 genuinely saturates at the multicritical point and chi=4 is finally justified.")
        status = "DMRG_SEED_INSUFFICIENT_ESCALATE_CHI4" if S_m > 0.05 else "DMRG_SEED_DID_NOT_TAKE"

    out = {"id": "SIM-2026-038", "type": "classical", "date": "2026-06-17",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage-2c: exact-GS-seeded chi=3 MERA at the O'Brien-Fendley TCI point. "
                           "Exact N=16 ground state -> state-vector target -> overlap pre-optimization "
                           "(non-vanishing gradient at the product state, unlike SIM-037's penalty) -> "
                           "anneal to energy. REPRESENTABILITY demonstration (fit chi=3 MERA to the exact "
                           "GS to escape the SIM-036/037 product minimum), NOT a blind-variational result; "
                           "the subsequent force read-out is a property of the converged tensors. Gate "
                           "enforces energy AND entanglement AND overlap independently."),
           "circuit": {"qubits": N, "chi": 3, "n_params": NP,
                       "script_path": "research/data/simulations/sim038_dmrg_seeded_mera.py",
                       "theta_checkpoint": CKPT},
           "hardware_target": "local CPU",
           "results": {"E_exact": E0, "seed_target": "exact_ground_state", "seed_overlap_with_exact": dmrg_ov,
                       "S_half_exact": S_exact, "E_mera": E_m, "rel_err_pct": rel,
                       "overlap": ov, "S_half": S_m, "S_ratio": sratio, "gate_pass": gate,
                       "status": status, "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Attacks the SIM-036/037 product-state basin with a structured target (the exact GS, "
                    "faithful and free at N=16). Route A (state-vector overlap seed), no MPS->MERA tensor "
                    "surgery, no quimb dependency. quimb DMRG was tried but its 2-site SVD NaN'd on this "
                    "build; the exact GS is a strictly better seed target anyway.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\n  VERDICT:", verdict)
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
