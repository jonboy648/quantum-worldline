# Pre-registration: V_T vs V_X channel discrimination (HYP-2026-008's own killer test)

**Written 2026-08-23, BEFORE any measurement was run.**

> **Date correction, same day.** This file was first committed (`aed9051`) with the date written as
> 2026-08-17. That was wrong: 08-17 is when the audit and the alpha retraction happened, and six days
> have since passed. The git timestamp on `aed9051` reads 2026-08-23 10:21:58 -0500 and is the
> authority. Corrected in a follow-up commit rather than an amend, deliberately -- a pre-registration
> is worth exactly its verifiable timestamp, so rewriting history here would destroy the thing that
> makes the document useful. Nothing else changed; no measurement had been run at either commit. Per RESEARCH-DIRECTOR.md §12, the outcomes
below are named in advance so the result cannot be reinterpreted after the fact. Git-committed before
the driver was executed; check `git log` on this file against the SIM record's timestamp.

## Why this test, and why now

`HYP-2026-008` registered this exact test in its `refutation_criteria` on **2026-03-11** and it was
never run. The hypothesis was set SUPPORTED anyway, off a single curve.

Its status changed on 2026-08-17 (six days before this test): the force exponent it rested on, alpha = 3.92, was withdrawn as an
estimator artifact (`SIM-2026-072`). The corrected exponent is **alpha = 2.6 +/- 0.2**, which matches
**neither** candidate channel (2*Delta_T = 4 for stress tensor, 2*Delta_eps = 2 for scalar).

That change is what makes this test worth running. Under the old expectation of alpha = 4, the test
was near-worthless: Delta_T = 2 is a Virasoro theorem, so a working implementation had to return 4
and the test could only confirm. With alpha = 2.6 matching nothing, **the outcome is genuinely open**
and the test discriminates. §6 counterfactual novelty: HIGH.

## The three arms

All three use the SAME cached exact ground state and the SAME energy-difference protocol:

    F(dr) = [E_dual(dr) - E_0] - [dE_single(anchor) + dE_single(anchor+dr)]

where each excited state is O_j|GS> renormalized. Arms differ ONLY in the operator O:

| arm | operator | sector | role |
|---|---|---|---|
| **eps** | `a(X_j + X_j+1) + b(X_j Z_j+1 + Z_j X_j+1)`, a=0.635, b=-0.026 | Zou-Milsted-Vidal boundary primary | **reproduction control** -- this is what SIM-2026-011 measured |
| **T** | `-(Z_j Z_j+1 - <Z_j Z_j+1>_GS)` | energy density / stress-tensor-like | the hypothesis's named probe |
| **X** | `X_j - <X_j>_GS` | spin primary (sigma sector) | the hypothesis's named comparison |

**Vacuum subtraction on T and X is deliberate and is not a free choice.** Without it, `O|GS>` retains
a large component along `|GS>` itself, so the "excitation" is mostly no excitation and F(dr) measures
a contaminated quantity. The connected operator is the correct local insertion. The eps operator needs
no subtraction (it is purely off-diagonal in the X basis, `<GS|sigma_eps|GS>` = 0 by Z2 parity).

## Fit window, fixed in advance

**Primary window: dr >= 3.** Reason, stated before seeing results: a contact term exists wherever a
Hamiltonian bond still bridges the two operator supports. eps and T both have support {j, j+1}, so
their supports are bridged by a bond through dr = 2. X has support {j}, bridged through dr = 1.
**dr >= 3 is the smallest window that is contact-free for all three arms simultaneously**, and only a
common window permits a like-for-like comparison.

This is exactly where the original analysis went wrong: it excluded dr = 1 as a contact term and then
rested 95.8% of its fit on dr = 2, the next member of the same family (`SIM-2026-072`).
dr >= 2 will be reported as a secondary window for continuity, never as the headline.

## Estimators, fixed in advance

**Headline: log-space OLS**, cross-checked against relative-error-weighted NLS. The unweighted
linear-space NLS that produced alpha = 3.92 **will be computed and reported for continuity but is
banned from any conclusion.** Uncertainty comes from a bootstrap (seed 20260817), not from the
covariance band, because `SIM-2026-017`'s own bootstrap gave sigma four times the quoted +/-0.16.

Primary discriminant is the **local log-slope plateau**, not a whole-window fit.

## Validation gate (must pass or the run is void)

The **eps** arm must reproduce `SIM-2026-011-interaction.json` `.F_interaction_avg` to **< 1%** at
every dr in 2..12. If it does not, the implementation differs from the published one and no
comparison between arms is meaningful. This gate is checked and reported before any other number.

## Pre-registered outcomes

Let `a_T`, `a_X` be the dr >= 3 log-space exponents with bootstrap sigmas `s_T`, `s_X`.
Define separation `D = |a_T - a_X| / sqrt(s_T^2 + s_X^2)`.

- **Outcome A -- CHANNEL-SPECIFIC.** `D > 3` AND `|a_T - a_X| > 0.5`.
  The force depends on what probes it. alpha carries mechanism. HYP-008 survives in corrected form
  and the follow-up is to identify what a_T actually corresponds to (it is not required to be 4).

- **Outcome B -- CHANNEL-BLIND. This REFUTES HYP-008 by its own 2026-03-11 wording**
  (*"If V_T(dr) is indistinguishable from V_X(dr) in both functional form and amplitude, the Roux
  graviton-vs-scalar distinction does not manifest at this MERA resolution"*).
  `D < 1` AND `|a_T - a_X| < 0.3` AND the amplitudes agree within a factor of 2.
  Reading: the ~2.6 falloff is generic -- a property of the lattice/state, not of the probe. This
  would be a **negative result and must be recorded as one**, not softened.

- **Outcome C -- NO POWER LAW.** Neither arm shows a local-slope plateau flat to 15% over >= 3
  consecutive slopes in the primary window. The power-law framing itself is then unsupported for
  these operators and the correct report is that F(dr) is not well described by dr^-alpha.

- **Outcome D -- INDETERMINATE.** `1 <= D <= 3`, or the arms disagree in functional form but not
  cleanly. Report as underpowered and state what N or precision would settle it. **Do not round
  toward A.**

## Banned in advance

- Selecting a fit window after seeing exponents.
- Quoting the unweighted-linear estimator as a result.
- Any use of "first", "novel", "to our knowledge" without a recorded §8 literature gate.
- Reporting Outcome A on the strength of amplitude difference alone -- the hypothesis's own criterion
  names *both* functional form and amplitude, and amplitude alone is trivially operator-normalization
  dependent.
