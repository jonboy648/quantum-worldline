# χ=6 Convergence Recipe (HYP-027) — the path past the cold-start basin failure

**Status (2026-06-19):** χ=4 method validated (c stable ≈0.5, ε exact, Δ_T≈1.97/2.04). **χ=6 cold-start
lands in a WRONG basin** (on-disk `uw_ISING_stable_chi6.npz`: c=0.746, σ=0.037 — *worse* than χ=4's
0.057 = textbook collapsed-basin signature, NOT a bond limit). Two independent analysts + ground-truth
agree. Workflow: wf_100c46c9.

## Root cause
1. **Un-damped alternating SVD** (`w' = -U Vh` full replacement each sweep) is a fixed-point map with no
   step control → cold at χ=6 it slams σ high early (A25: σ≈0.2, c≈1.0) then collapses σ→0.04 as ρ
   descends, while c drifts. This is the "flows to trivial FP" failure (ERRATA D5 / SIM-036).
2. **Transitional↔bulk fight from wrong order**: re-ascending h_bulk every round → bulk chases a moving
   target. A single rank-4 transitional layer (4→6 is rank-deficient) injects a non-critical
   perturbation the bulk relaxes by collapsing σ.
3. χ=4 escaped ALL of this only because it warm-started from the near-critical `evsched` checkpoint.
   χ-ramp padding fails: bond expansion changes the descending-FP eigenstructure (pad → c=4.6).

## DECISION: Hybrid C+A (seed-from-finite-MERA + joint autograd), multi-restart. NOT pure ramp, NOT ternary.

### IMPLEMENTED (2026-06-19): sim046_finite_si_mera_seed.py
- Built the scale-invariant finite MERA (torch, Cayley unitaries, shared bulk). VALIDATED: norm=1.0
  exact (correct contraction); χ=3 optimizes to rel=0.27%; **χ=6 optimizes to rel~0.1%** (faithful
  critical state — exactly what cold scale-invariant χ=6 could NOT reach).
- CONFIRMED the fallback-#3 requirement: a SINGLE transitional layer canNOT reach χ=6 (binary first
  layer from qubit-pairs caps at phys²=4; w1 4→6 is rank-deficient → RuntimeError). FIX applied: TWO
  transitional layers (phys²=4→cmid=4, then 4²=16→χ=6), then shared bulk χ=6. This is in sim046 now.
- CAVEAT: N=16 with 2 transitional layers leaves only ONE shared-bulk step (2→4), so the extracted
  (u,w) is a weak scale-invariant seed (used once). Still a critical χ=6 seed — far better than cold.
  If the seed proves too weak for the scale-invariant run, escalate N (needs >16 qubits = infeasible
  dense) OR use the eigen-tower ramp (fallback #2) from this seed.

### Step-1 OUTCOME (2026-06-19): finite-MERA gives a critical STATE but a NON-scale-invariant BULK
- sim046 chi=6 Ising: rel=0.0040%, ov=0.9999, S_ratio=1.004 — a near-PERFECT critical finite state.
- BUT reading the scaling superoperator from the extracted bulk (u,w) gives GARBAGE: c=6.67, sigma=2.34.
  Root cause: the bulk was optimized as a SINGLE coarse-graining tensor (used once at N=16), NOT as a
  scale-invariant fixed point (same u,w at every scale). Criticality != scale-invariance.
- So the finite-MERA seed does NOT directly give a scale-invariant (u,w). Warm-starting the
  scale-invariant refinement (sim045) from it starts at c~6.4 and descends the SAME path as cold (toward
  the wrong basin c~0.75) — the seed solves criticality, not the scale-invariance that is the hard part.
- **CONCLUSION**: three seeding routes have now failed to give a scale-invariant critical chi=6 (u,w):
  cold (wrong basin c=0.75), raw chi-ramp pad (c=4.6), finite-MERA bulk (c=6.67 in the superop).
  The hard part is the SCALE-INVARIANT fixed point at chi=6, not criticality per se.
- **NEXT (the principled fix, fallback #2 promoted to primary): EIGEN-TOWER chi-ramp.** Grow chi=4->6
  in the SCALING-SUPEROPERATOR eigenbasis, not the energy/tensor basis: seed the new bond directions
  from the leading eigenvectors of the converged chi=4 ASCENDING superoperator (sim045 builds it
  matrix-free), re-orthonormalize, re-converge. This preserves the descending fixed point under bond
  growth — operating in the basis where scale-invariance lives. This is the untried, distinct lever.

### DEFINITIVE FINDING (2026-06-19): the EV ScInv SVD-loop has a chi=6 CEILING (seed-independent)
The eigen-tower ramp (sim047) gave the BEST seed yet (c=3.79 pre-refine, vs pad 4.6, finite-MERA 6.67,
all isometries machine-clean). But refining it with the EV ScInv loop PLATEAUS at c~1.95, sigma~0.37,
eps~0.86 — NOT critical. So FOUR seeds (cold, pad, finite-MERA, eigen-tower) × the SAME loop = the same
failure to reach c=0.5 at chi=6. **The bottleneck is the LOOP, not the seed**: the EV first-order
polar-SVD environment update cannot converge the chi=6 critical fixed point (it worked at chi=4 only from
a near-critical warm start). Recurring across ALL chi=6 attempts: scaling dims cluster near 2.0
(1.91-1.99) — Delta_T~2 is persistently present but NOT claimable without a converged control.

**THE REAL NEXT STEP (fallback #1, now primary): RIEMANNIAN / gradient-manifold optimization** of the
scale-invariant tensors (Hauru, Vidal, Evenbly — SciPost 10,040 / arXiv:2007.03638: Riemannian CG/L-BFGS
on the Stiefel manifold, reported to converge where pure EV stalls). The autograd energy is already exact
(sim046 machinery). Options: (a) implement Riemannian L-BFGS on the scale-invariant fixed-point objective
in torch (substantial); (b) adopt a maintained MERA library (MERAKit.jl ternary chi=8 Ising reaches
Delta_sigma=1/8 — also a cross-check of our superoperator GATE). This is a SCOPE step (new optimizer or
new dependency), flagged for a decision rather than another EV-loop variant.

### Step 1 (original plan) — seed from a SCALE-INVARIANT finite MERA (build on sim039)
- sim039 is an already-validated finite autograd MERA (Cayley unitaries, exact-GS at N=16, gradients
  verified vs FD ~1e-10, Ising control faithful, χ=4 TCI gate passed). BUT its middle layers have
  DISTINCT tensors per position — NOT shared.
- **Modify**: reparametrize so the repeated middle layers use ONE SHARED (u,w) (scale-invariant) + a
  transitional (u1,w1). Optimize ALL tensors jointly on the Z2-projected energy (torch/autograd, Adam
  lr~1e-2 cosine, polar-retract to isometric manifold each step — NOT plain GD). The finite-energy
  minimization is WELL-CONDITIONED (unlike the scale-invariant fixed-point chase).
- Read the converged shared (u,w)+(w1,u1) → `seed_chi6_finiteMERA.npz`. This lands the scale-invariant
  optimizer in the Ising basin from step 0 (the exact mechanism that made χ=4 work).

### Step 2 — joint scale-invariant refinement (replace sim045's two-stage SVD)
- One autograd gradient step on the total energy of (transitional + shared bulk) per iter; polar-retract
  each step (reuse `sim045.svd_polar` as the retraction). Warm-start from Step-1 seed.
- Interleave ONE EV env update (`svd_polar(grad_t(...))`) every 5–10 gradient steps (documented
  last-factor-of-10 curvature fix). Keep BINARY.

### Step 3 — multi-restart: 4–8 runs (finite-MERA seed + random-perturbed seeds, kick~0.1), keep lowest
scale-invariant energy. The c-overshoot is partly seed luck.

### Step 4 — converge on OBSERVABLES (lowest-10 dims change ≤0.5% across check interval), matrix-free
superop (already in `read_spectrum.py` / `sim045.central_charge_and_dims`).

### Step 5 — down-projection sanity: χ=4 block of the χ=6 tensors must still give c≈0.5, σ≈0.057.

### Step 6 — ONLY after Ising control PASSES at χ=6, switch λ3=0.856 (TCI), read Δ_T. If Δ_T≠2 cleanly,
ramp 6→8 (same recipe), NOT ternary.

## GATE (all simultaneous, in ONE state, stationary):
c∈[0.45,0.55] AND σ∈[0.10,0.15] **AND σ strictly better than χ=4's 0.057** (the decisive
basin discriminator) AND ε∈[0.95,1.05] AND Δ_T within 0.05 of 2.0 AND χ=4-block down-projection sane.
TCI success: c≈0.70 AND a dim within 0.05 of Δ_T=2 ⇒ α=2Δ_T=4 universal at c=7/10.

## FALLBACK ladder (if C+A still fails after multi-restart):
1. More aggressive interleaved EV env updates (every 3 steps) + **Riemannian L-BFGS on the Stiefel
   manifold** (Hauru SciPost 10,040 / arXiv:2007.03638 — beats pure EV; autograd energy already exact).
2. **Explicit eigen-tower χ-ramp**: seed new χ=4→6 bond directions from the leading eigenvectors of the
   χ=4 ASCENDING superoperator (sim045 builds it matrix-free), re-orthonormalize, re-converge. This
   preserves the descending FP under bond growth — the specific defect that broke pad_mera_chi.py.
3. **TWO transitional layers** (phys→d_mid→χ) to remove the 4→6 rank deficiency (EV 0707.1454 p.18;
   PRA 0810.0580 hit σ=1/8 with two transition layers).
4. Cross-check the superoperator GATE itself against MERAKit.jl ternary χ=8 Ising (σ=1/8 ground truth)
   to rule out a bug before blaming the optimizer.

Citations: EV 0707.1454 Sec V.A/V.C (small q_one/q_lay p.17; 1–2 transitional layers p.18; ScInv1/2);
PRA 0810.0580 p.3 (1–5 transitional layers; Fig.3 moderate-χ Ising tower). Full: wf_100c46c9 output.

## RIEMANNIAN ATTEMPT OUTCOME (2026-06-19): optimizer works, but chi=6 is objective-bound + memory-bound

Built + validated the full Riemannian/Stiefel machinery (sim048) per Hauru 2007.03638:
- Manifold-direct Riemannian CG: Stiefel tangent projection, POSITIVE polar retraction, Polak-Ribiere +
  Armijo line search + projection transport; rho reduced-density-matrix preconditioner (Hauru's crucial
  ingredient). Primitives validated (retraction isometric 7.8e-16, gradient tangent 1.3e-15).
- PROVEN to work as an OPTIMIZER: chi=4 cold c=5.71->0.61 MONOTONE (EV plateaued); chi=6 cold
  preconditioned c=7.62->0.13 in 20 iters -- DECISIVELY broke the EV first-order ceiling.

BUT three independent walls block chi=6 criticality, all BEYOND the optimizer:
1. ENERGY IS FLAT (the core finding): the scale-invariant energy <rho_hat,h_bar> at chi=6 spans only
   ~2% between c=0.5 and c=6.7 states, and its MINIMUM is NON-critical (c->0.05 with sigma=0.34). Both
   the rank-4-padded h0 AND the genuine 2-transitional h0 (sim046's validated layers) show this. So
   energy-minimization (EV or Riemannian) drives AWAY from criticality (c->0). Confirmed: MULTI0 cold
   precond ran to c=0.049.
2. SPECTRAL SPSA is correct-direction but INTRACTABLE: optimizing the conformal-data loss
   (c-c*)^2+(sigma-sig*)^2+(eps-1)^2+(Delta_T-2)^2 (sim049) via SPSA on the ~5000-param Stiefel space
   moves L only 0.045/10-iters (c frozen) -> ~10 hours to converge. Single-direction SPSA can't move
   5000 params.
3. EXACT SPECTRAL GRADIENT needs the DENSE superoperator (chi^6=46656^2 = 35 GB complex128) for
   eigenvalue gradients -> OOM at chi=6. The matrix-free path gives eigenVALUES but not their gradients.

CONCLUSION: chi=6 criticality is NOT reachable with a from-scratch optimizer -- it is objective-bound
(flat energy) and memory-bound (dense superop for spectral gradients). The viable path is a MAINTAINED
MERA LIBRARY (MERAKit.jl) implementing rho-preconditioned Riemannian optimization with SPARSE eigenvalue
gradients -- a dependency, not a from-scratch build. RECURRING across ALL chi=6 attempts (EV, Riemannian,
spectral): Delta_T candidates cluster at 1.9-2.1 -> Delta_T~2 (alpha=4 universal) is very likely present,
but remains uncertifiable without a converged critical control.
