# OPE C_TTT via the genuine PEV route — implementation design (for P2)

**Status:** SUPERSEDED-IN-MECHANISM 2026-07-02 (gate unchanged). Implemented as `qw_ope_pev.jl` (v3),
but NOT via the ChargedTernaryOperator ascend-to-adjacency route below. Re-reading the actual PEV
paper (research/downloads/0810.0580.pdf) showed Eq. 13 IS the trace on three consecutive sites
against rho^(3)-from-rho-hat with a 2^Omega kinematic factor — i.e. v2's rho3 GEOMETRY WAS CORRECT
(audited index-by-index against MERAKit descend conventions; Fig 2(iii)'s landing registration =
build_rho3_cone exactly). The REAL root cause of v1/v2 failures was operator contamination from TWO
stacked parity bugs: (1) the physical "parity" was X(x)X, but DemoTools' Ising is H=-XX+Z-field whose
Z2 symmetry is Z^{(x)N} — a non-symmetry was being lifted; (2) coarse_parity partial-traced the
ascended width-2 parity, but parity is traceless, so it annihilated to noise that re-converged to
the identity ("p_sig came out +1"). v3 fixes: correct Z-parity + a layer-by-layer covariance LIFT
(rank-1 SVD factorization of u'(P⊗P)u, no partial traces, identity-lift selftest) + parity
projection of sigma/eps + PEV Eq. 10 normalization under the width-2 fixed point + BOTH width-3
registrations as a translation-invariance error bar. This section's charged-operator mechanism is
retained below for reference only. Validation gate: UNCHANGED (section "Validation gate").

**Original design (2026-06-28), mechanism superseded:** Written before the paper re-read.
**Why:** v1 (SIM-056) and v2 (SIM-058) both STILL_BROKEN — both built an explicit rho3 from the width-2
rho2, which is not a faithful 3-point object (ternary causal cone is width-2). The decisive failure: the
Z2-forbidden C_sss did NOT vanish across clean basins (0.008/0.084/1.92). Root cause = wrong extraction
route, NOT chi (dims clean at chi=6) and NOT the prefactor (v2 fixed that).

## The correct route (PEV "coarse-grain operators until adjacent")

Do NOT build any explicit rho3. Instead compute the 3-point function as a scale-invariant network expectation:

1. Place the three single-site operators (sigma, sigma, eps) at boundary sites chosen so that, after K
   coarse-graining layers, their supports merge into ONE width-2 causal cone. In a ternary MERA (3 sites ->
   1 per layer) three operators at separations ~3^K coarse-grain together after K layers.
2. ASCEND each insertion up the network using MERAKit's own ascend machinery — which INCLUDES the
   disentangler u at every layer (this is the whole point; the explicit-rho3 route dropped the u's).
3. When the three supports have merged into a width-2 operator at the scale-invariant layer, contract the
   resulting 2-site operator against the width-2 fixed-point density matrix rho2 = fixedpoint_densitymatrix(m).
4. Apply the CFT kinematic normalization for the chosen lattice separations (NOT the bare 3^Omega — that
   only holds when all three already sit at unit separation; v2's 2^Delta_eps fix was correct for (1,1,2)).

## MERAKit primitives to use (from src/ternarylayer.jl, src/genericmera.jl)
- `TernaryOperator` = a 2-site operator (causal_cone_width = 2). All ascend/descend work on these.
- `ChargedTernaryOperator` / `DoubleChargedTernaryOperator`: operators carrying an extra "charge" leg
  (the `-1000` index in ascend_left/right) = the machinery for a SINGLE-site insertion that does not fill
  the 2-site cone. THIS is how PEV ascends a lone operator: as a charged op until it can fuse with a
  neighbour. ascend(op::ChargedTernaryOperator, layer) is implemented (lines ~266-307).
- `ascend(op, m, endscale, startscale)` (genericmera.jl:469) ascends an op across multiple layers.
- `ascended_operator(op, m, depth)` (genericmera.jl:581) — cached multi-layer ascend.
- `fixedpoint_densitymatrix(m)` — the width-2 rho2 (translation-invariant, includes u). The contraction target.
- `expand_support(op, width)` — pad a 1-site op to the causal-cone width.

## Concrete plan
- Build single-site sigma, eps as charged 1-site operators on the SI-layer coarse space (reuse the
  parity-classified scaling-operator eigenvectors from qw_ope_constants.jl, which ALREADY work — only the
  3-point geometry was wrong).
- Two operators on ADJACENT sites fuse into one ordinary TernaryOperator at the same scale (a 2-site op);
  the third, on a site that merges one layer up, is carried as a charged op and ascended one more layer,
  then fused. (PEV Fig 2(iii): ascend each until all three are within one 2-site cone.)
- Contract the merged 2-site op against rho2. Multiply by the kinematic factor for the realized separations.

## Validation gate (UNCHANGED, non-negotiable)
- Ising: C_sigma-sigma-eps -> 0.5 (target +-10%) AND the Z2-forbidden C_sigma-sigma-sigma -> 0
  (|C_sss| < 0.02) STABLY across >=3 CLEAN basins (|Delta_sigma-0.125|<0.10). One clean basin is the
  false-positive trap — bit twice (SIM-056 seed3, SIM-058 seed1). C_eps-eps-eps should also -> 0.
- Only AFTER this passes at chi=6: escalate to chi=10-12 on RunPod A100 (~$10-20, APPROVED) for a tight
  number, then the tricritical C_TTT (the emergent graviton self-coupling, the actually-novel target).

## Why this fixes C_sss
Ascending preserves the Z2 charge at every layer (the tensors are parity-covariant). An odd-odd-odd
composite stays Z2-odd all the way up and contracts to zero against the parity-even rho2 — automatically,
because the disentanglers are included. The explicit-rho3 route broke this by omitting the u's, so parity
was not respected and C_sss leaked. This is the structural reason the PEV route is correct where rho3 was not.

## Files
- New: qw_ope_pev.jl (the genuine-PEV driver). Reuse the dim/parity/2-pt machinery from qw_ope_constants.jl.
- Reference: qw_ope_constants_v2.jl (the kinematic-prefactor fix is correct and reusable; only its rho3 is wrong).
