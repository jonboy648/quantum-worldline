# Pre-registration IV-B: the C1 thread at large L (matrix-product route)

**Status: APPROVED by Jon 2026-09-09 ("word"). Committed BEFORE any driver code for SIM-2026-078 existed. Follows
PREREGISTRATION-HYP032-A.md, whose verdict (SIM-2026-077) was a Level-3 negative on all four
candidates. This registers the ONE follow-up that amendment named as worth pursuing, and no other.
Governs SIM-2026-078.**

## The thread being followed

SIM-2026-077 candidate C1 (chiral symmetry broken by a longitudinal field `h_z`) produced exactly one
setting whose window satisfied the registered YES conditions at a single size:

`L = 14, h_z = 0.02, R_H = 5 (R = 10), delta = 5`, window `T0 in {3,4,5}`,
`Im S = 0.2564, 0.2815, 0.3007`, mean **0.2795**, std 0.0181, against the prediction
`pi c / 6 = 0.2618` at c = 1/2. That is 6.8 percent high, one sign, window std 6.5 percent of the mean.

It was recorded as **NO** because the registered rule required the same setting to pass at two sizes,
and the geometry at L = 10 and 12 used `R_H = 3` and `4`, so the identical setting was never evaluated
at a second size. That is the whole of the thread. Everything below is designed to close it.

## Three facts about that point, established by re-reading the stored data on 2026-09-08

These were not in the SIM-077 summary and they change what this pre-registration must control for.
They are recorded here BEFORE the follow-up is designed around them.

1. **The passing window is a narrow slice of a monotone rise, not a plateau.** At that setting the
   full stored `Im S` over `T0 = 2..8` is `0.2262, 0.2564, 0.2815, 0.3007, 0.3180, 0.3316, 0.3429`.
   It rises by 52 percent across the available range and never flattens. The registered window
   `[3, R/2] = [3,5]` is three points wide and crosses `0.2618` inside that rise. A wider window
   would have failed the stability gate. **This is the single strongest argument that the point is an
   artifact**, and it is why this pre-registration requires a plateau over a wide window (below).

2. **There is a nonzero background with the symmetry intact.** SIM-076's exact-zero theorem
   (`V H V^dag = -H`) forces `Im S = 0` only at `delta = 0`; with the regulator on,
   `V e^{(iR_H - delta)H} V^dag = e^{(-iR_H + delta)H}`, which is not the conjugate of the original.
   The stored `h_z = 0` runs at `delta = 5` give `Im S = 0.0427` at L = 10 and `0.0466` at L = 12,
   against the 0.2795 being chased. **Whether that background grows with L has never been measured.**
   SIM-077 never ran `h_z = 0` at L = 14 at all; the run was cut.

3. **The field scan does not peak at L = 14.** SIM-077 ran only `h_z = 0.005, 0.01, 0.02` at L = 14
   (`0.0766, 0.1572, 0.2795` at `R_H = 5, delta = 5`) -- monotone rising, no maximum. The
   peak-and-fall shape (`0.0622, 0.1034, 0.1957, 0.0321` for `h_z = 0.005, 0.01, 0.02, 0.05`) is at
   **L = 12, R_H = 4**. An earlier verbal summary of SIM-077 stated the peak was at L = 14; that was
   wrong and is corrected here and in the SIM-077 record.

## The two competing hypotheses, with distinct quantitative predictions (RESEARCH-DIRECTOR section 12)

`h_z` is a relevant perturbation of the Ising fixed point with RG dimension `y = 2 - 1/8 = 15/8`, so
the correlation length is `xi ~ h_z^(-8/15)`. At `h_z = 0.02`, `xi ~ 8.0` sites. **L = 14 is 1.7
correlation lengths.** The passing point sits exactly where `xi ~ L`, which is where finite-size
resonances live.

**H_signal.** The imaginary part is a real property of the symmetry-broken lattice theory. Then at
fixed `(h_z = 0.02, R_H = 5, delta = 5)`, `Im S` converges to `0.2618` as L grows, it forms a genuine
plateau in `T0` when the window is made wide, and the location of the maximum in `h_z` does not move
with L.

**H_artifact.** The point is a finite-size resonance at `xi ~ L`. Then the maximum in `h_z` moves as
`h_z*(L) proportional to L^(-15/8)`, and at fixed `h_z = 0.02` the value falls once `L >> xi(0.02)`.
Numerically: from L = 14 to L = 64 the maximum should move from 0.02 to **0.0012 +/- a factor of 2**;
from L = 14 to L = 128, to **0.00031**.

These predictions differ by more than an order of magnitude in the observable that is cheapest to
measure, which is what makes this follow-up worth its compute. **Counterfactual novelty
(section 6): genuinely two outcomes are possible, and the artifact branch makes a sharp numerical
prediction it can fail.** This is not a case where the answer is fixed in advance.

## The registered method

`h_z` breaks the free-fermion structure, so neither the Gaussian route nor exact diagonalization
reaches the sizes this question needs. The registered method is **complex-time matrix-product
operator evolution**:

1. Build `M(beta) = e^{-beta H}` with `beta = delta - i R_H` as an MPO, starting from the identity
   MPO and applying second-order Trotterized two-site gates `e^{-d beta h_{j,j+1}}` from one side,
   with singular-value truncation to bond dimension `chi` after each sweep.
2. Form `tau_A = Tr_B M / Tr M` by tracing the physical index pair of every site outside A and
   contracting the remainder to a dense `2^T0 x 2^T0` matrix. A is the centred block of T0 sites,
   `s = (L - T0) // 2`, identical to the SIM-077 placement.
3. `S = -sum lambda log lambda` over eigenvalues with `|lambda| > 1e-14`, **per-eigenvalue principal
   branch** -- the same convention as SIM-077's C1, so the numbers are directly comparable.

Implementation is our own numpy code, not an external tensor library: it keeps the whole path
auditable and avoids vendoring a package we cannot redistribute. What makes that safe is gate G1,
which checks it against numbers a completely different method already produced.

## Gates (each one a control that can void; a failed gate is reported, never worked around)

- **G1 EXACTNESS (hard, voids the run).** At L = 12 and L = 14 the MPO result must reproduce
  SIM-077's stored exact-diagonalization values for the same `(h_z, R_H, delta, T0)` to **1e-6** in
  both real and imaginary parts. Two methods, one answer, or nothing downstream is computed.
- **G2 SYMMETRY.** At `h_z = 0, delta = 0`, `|Im S| < 1e-8` at every L, reproducing the SIM-076
  theorem through the new code path.
- **G3 BOND-DIMENSION CONVERGENCE.** Doubling `chi` must change `Im S` by less than **2 percent** at
  every reported point. A point that fails is marked UNCONVERGED, excluded from the verdict, and
  listed in the record. It is never rounded into the verdict in either direction.
- **G4 TROTTER CONVERGENCE.** Halving `d beta` must change `Im S` by less than **1 percent** at every
  reported point, same exclusion rule.
- **G5 BACKGROUND CONTROL (the control SIM-077 lacked).** `h_z = 0` is run at every L, every `R_H`,
  and every `delta`, and reported beside every signal. **No point counts as signal unless it exceeds
  the `h_z = 0` background at the same `(L, R_H, delta)` by a factor of 5.**

## The registered grid (fixed now; nothing may be added after results)

- **Sizes** L = 16, 24, 32, 48, 64, 96, 128.
- **Fields** `h_z` = 0, 0.0003, 0.001, 0.003, 0.005, 0.01, 0.02, 0.05. The small end exists to catch
  H_artifact's predicted `h_z*` at the largest sizes; it was chosen from the `L^(-15/8)` law before
  any run, not from results.
- **Setting A (thread-matched)** `R_H = 5, delta = 5`, window `T0 in [3,5]`. Reproduces the passing
  point's geometry exactly at every size.
- **Setting B (wide window)** `R_H = 8, delta = 5`, window `T0 in [3,8]` -- six points instead of
  three, which is what tests a plateau rather than a slice.
- **Setting C (widest, best-effort)** `R_H = 12, delta = 5`, window `T0 in [3,12]`. `|beta| = 13`
  makes the operator entanglement expensive; if G3 fails here beyond some L, the largest converged L
  is reported and the rest is marked UNCONVERGED. Setting C is not required for a verdict.
- `delta = 0` is run at `h_z = 0` only, as gate G2.

## Pass, kill, and what each outcome does to HYP-032 (all fixed now)

**YES -- H_signal supported.** Every one of the following, together, at Setting A or Setting B:
1. `|Im S|` within **10 percent** of `pi c / 6 = 0.2618`, one sign across the window;
2. window standard deviation under 10 percent of the window mean;
3. **at three or more consecutive sizes L** at the same `(h_z, R_H, delta)` -- not two, because two
   adjacent sizes can share a finite-size resonance;
4. **plateau, not slice**: across the FULL available range `T0 = 2 .. R-2`, the monotone drift in
   `Im S` is under 10 percent of the mean. This is the condition the SIM-077 point fails by 52
   percent, and it is the reason this gate exists;
5. exceeds the `h_z = 0` background at the same setting by a factor of 5 (G5);
6. the location of the maximum in `h_z` moves by less than a factor of 2 across those sizes.

A YES is a **Level-3 positive**: the imaginary part of timelike entanglement entropy has a lattice
realization once chiral symmetry is broken, with the construction and parameters named. Its wording
passes the section-8 novelty gate before anything stronger than "reproduced" is written, and the
prior-art search on the `Im S = 0` theorem (currently outstanding) is completed first.

**ARTIFACT -- H_artifact supported.** Either of:
- the maximum in `h_z` moves across L = 16..128 consistently with `h_z* proportional to L^(-15/8)`
  within a factor of 2; or
- `Im S` at fixed `h_z = 0.02`, Setting A, falls monotonically for `L >= 32`.

This **closes HYP-032** as a Level-3 negative with the mechanism identified: the SIM-077 point was a
finite-size resonance at `xi ~ L`. That is a better closure than the one we have now, because it
names the cause instead of only failing a size rule.

**NEITHER.** Anything else -- drift without the predicted exponent, no maximum, or too many points
excluded by G3/G4 to decide. HYP-032 closes as a Level-3 negative **unchanged from SIM-077**, and
this pre-registration records that the thread was followed and did not resolve. No third amendment.

In all three cases the real part's slope against `1/6` is reported as a control and does not enter
the verdict. Branch convention is stated on every number.

## Compute and budget

RunPod, per the standing decision that all HYP-032 computation runs there and none locally. CPU pod,
16-32 vCPU, 64 GB (the MPO at `chi = 512`, L = 128 is the memory driver, not the dense block).
**Cap: 25 USD. Wall clock: 7 days from approval.** Runs are detached with partial results fetched
every 2 minutes and dumped after every setting -- SIM-077 lost finished settings to a time cap twice
before that was fixed, and the fix stays.

Local work permitted: writing the driver, and gate-only smoke tests at `L <= 12` that take seconds.
Every registered number is produced on the pod. Results land in
`research/data/simulations/SIM-2026-078.json` with pod id, image, chi, `d beta`, and run log.

## Banned

Adding a size, field, or setting after results; changing the 10 percent bar or the 5x background
factor; relaxing the plateau condition or the three-size rule; quoting a point that failed G3 or G4;
quoting a single size; dropping the `h_z = 0` control; calling a NEITHER outcome "inconclusive" or
"promising"; any wording stronger than "reproduced" without the section-8 record.

## Provenance

Written 2026-09-08 after re-reading `sim077_C1_merged.json` directly. The three facts in the second
section were not in the SIM-077 summary and are corrections to it, entered here before the design
that depends on them. Approved by Jon 2026-09-09; committed before any driver code for SIM-2026-078 existed.
