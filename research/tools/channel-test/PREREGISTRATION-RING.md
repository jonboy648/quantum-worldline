# Pre-registration II: the ring (PBC) channel test + a non-critical matched control

**Written 2026-08-24, BEFORE the driver existed.** Committed before `qw_ring_test.py` was created;
check `git log` on this file against the run record. Supersedes nothing in
`PREREGISTRATION.md` -- that one governs SIM-2026-073 (open chain) and its INDETERMINATE verdict
stands as recorded.

## Why a second experiment

SIM-2026-073 ran HYP-2026-008's registered V_T vs V_X test on a 24-site **open** chain and returned
**D_INDETERMINATE**. Two systematics were identified as the limiters, and both are fixable:

1. **The open boundary.** Every arm's local slope curved sharply upward at large separation
   (eps reached 19.51 at dr=16, where the far operator sits at site 22 of 23). This inflated all
   whole-window fits -- it is why the eps arm read 3.46 over the window but 2.59 on its interior
   plateau.
2. **The T probe's weakness.** Its signal is 4.5x smaller than X's, it reaches the numerical noise
   floor by dr=16, and its bootstrap sigma (0.329) is 3.3x X's. That imprecision, not a genuine
   coincidence of exponents, is what produced D = 0.98.

Fixing (1) by re-cutting the window *after seeing the slopes* is the window-shopping banned by the
first pre-registration. The legitimate fix is to change the geometry so the systematic does not exist,
and to say so in advance. That is this document.

## The central methodological change: chord distance

A ring has no edges, but it does have a circumference. In a 2D CFT on a circle of L sites, a
two-point function does **not** go as `dr^-a`. It goes as the **chord distance**

    d_chord(dr) = (L / pi) * sin(pi * dr / L)

raised to the same power. Fitting `dr^-a` on a ring therefore produces a spurious upward curvature
near dr = L/2 that has nothing to do with physics -- structurally the same mistake as fitting through
an edge effect.

**PRIMARY ANALYSIS: fit F against d_chord, not against dr.** The local-slope diagnostic becomes
`-d ln|F| / d ln d_chord`, which is flat for a true power law across the whole ring. Fits against
raw `dr` will be computed and reported for comparison but are **not** the headline.

This is the substantive improvement over SIM-2026-073: the finite-size curvature is removed
*analytically* rather than by choosing a window.

## Experiment 1 -- ring, critical (h = 1)

- `H = -sum_i Z_i Z_{i+1 mod n} - h sum_i X_i`, `h = 1.0`, `n = 24`, PBC.
- Same three arms as SIM-2026-073, same protocol, same vacuum subtraction on T and X:
  `F(dr) = [E_dual(dr) - E0] - [dE_single(anchor) + dE_single(anchor+dr)]`.
- **Window, fixed now: dr = 3..11.**
  - `dr <= 2` excluded as contact: eps and T have support {j, j+1}, bridged by a bond through dr = 2.
    Same criterion as the first pre-registration; unchanged.
  - `dr = 12` excluded as **antipodal**: at n = 24 the two paths around the ring are exactly equal
    length, a geometric special point. Excluded on geometry, decided before any data exist.
  - `dr > 12` is redundant by symmetry (see gate G2).

### Validation gates (all must pass or the run is void)

- **G1 -- ground state.** PBC critical TFIM ground-state energy per site must match the exact
  free-fermion result `e0 = -(1/n) * sum_k 2|cos(k/2)|` over the appropriate momentum sector, to
  `< 1e-6`. This is an *analytic* check, not a comparison to our own earlier numbers.
- **G2 -- ring symmetry.** `F(dr)` must equal `F(n - dr)` to `< 1%` for at least three values of dr.
  This is free on a ring and is a genuine correctness test of the operator placement; the open chain
  had no equivalent.
- **G3 -- eps continuity.** The eps arm's chord-fit exponent must lie within the SIM-2026-073
  plateau band (2.59 +/- 0.2 x 3). A wild disagreement means the geometry change did something
  unintended and must be understood before the arms are compared. **This is a sanity band, not a
  target** -- landing outside it is reported, not corrected away.

## Experiment 2 -- the matched control (RESEARCH-DIRECTOR.md section 19)

**This is the more important of the two experiments, and it is the one that can embarrass us.**

Same ring, same three arms, same analysis, but at **h = 2.0** -- deep in the paramagnetic phase,
far from criticality, correlation length of order one site.

**Pre-registered expectation:** away from a critical point there is no CFT and no conformal power
law. `F(dr)` should decay **exponentially**, and the local chord-slope should therefore *rise without
limit* rather than plateau. A clean exponential decay is the expected, boring, correct result.

**The failure mode this is designed to catch:** if the h = 2 control ALSO yields a power-law plateau
somewhere in the 2.2-2.7 band, then that band is a property of the *protocol* -- the energy-difference
observable, the operator normalisation, the lattice -- and not of the critical state. In that case
**the entire alpha measurement programme, including the corrected alpha = 2.6, is measuring the
method rather than the physics.** That would be a more consequential finding than anything in
SIM-2026-073, and it is recorded here in advance so it cannot be quietly dropped if it occurs.

Reported as: `CONTROL_CLEAN` (exponential, no plateau) or **`CONTROL_CONTAMINATED`** (power-law
plateau present) with the plateau value.

## Outcomes for Experiment 1 (thresholds unchanged from PREREGISTRATION.md)

With `a_T`, `a_X` the chord-fit log-space exponents on dr = 3..11 and `s_T`, `s_X` their bootstrap
sigmas, `D = |a_T - a_X| / sqrt(s_T^2 + s_X^2)`:

- **A -- CHANNEL-SPECIFIC:** `D > 3` AND `|a_T - a_X| > 0.5`.
- **B -- CHANNEL-BLIND (refutes HYP-2026-008 by its own 2026-03-11 wording):** `D < 1` AND
  `|a_T - a_X| < 0.3` AND amplitude ratio `< 2`.
- **C -- NO POWER LAW:** neither arm shows a chord-slope plateau flat to 15% over >= 3 consecutive
  slopes.
- **D -- INDETERMINATE:** anything else. **Do not round toward A.**

**Precedence rule, fixed now:** if Experiment 2 returns `CONTROL_CONTAMINATED`, that result
**overrides** the Experiment 1 verdict entirely and the correct report is that the observable is not
measuring critical physics. Experiment 1's A/B/C/D label is then void, not merely weakened.

## Banned, carried over

Selecting windows after seeing exponents; quoting the unweighted-linear-space estimator as a result;
"first"/"novel"/"to our knowledge" without a recorded section 8 gate; reporting A on amplitude
difference alone.

## Estimators, carried over

Headline: log-space OLS on `log|F|` vs `log d_chord`. Cross-check: relative-error-weighted NLS.
Uncertainty: nonparametric bootstrap, seed 20260817. Primary discriminant: the chord-slope plateau,
not the whole-window fit.
