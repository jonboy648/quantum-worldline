---
title: "CORRECTION NOTICE"
subtitle: "The central result of this manuscript is WITHDRAWN."
---

*Issued 2026-09-06 by the author (v5 of this record). This notice was added to the archived record; the manuscript itself is unaltered. This record has not been peer reviewed.*

## What is wrong

The force exponent reported here as alpha = 3.92 +/- 0.16 is an artifact of the fitting procedure, not a property of the data. The fit was unweighted least squares in linear space applied to a steeply falling profile, which places 95.8 percent of its objective on the single point at the shortest retained separation. Re-fitting the same data with nothing discarded, changing only the error model, gives 2.82 (relative-error weighting) or 2.89 (log-space regression). Across fifteen combinations of standard estimator and fit window the exponent spans 2.53 to 3.92, and the value published here is the largest of them.

## What the data show instead, and how firmly

The retraction is certain. The replacement is not. On the open 24-site chain the same data give alpha = 2.6 +/- 0.2, where the interval is the spread of a plateau in the local logarithmic slope over six consecutive separations, not a statistical error (the bootstrap error on the published fit to the same data is 0.63); the plateau value was reproduced at 2.5921 by a separately written implementation run on the same recorded state (SIM-2026-073). This is a single geometry at a single size. On a 24-site periodic ring, analysed with chord distance as pre-registered, two probes that are both energy-density-like (Delta = 1) give 1.83 and 2.37 against a CFT two-point value of 2 (SIM-2026-074): one size, not converged, disagreeing with each other by 29 percent, and not attributable to a single operator channel. **No corrected exponent is established. The exchange channel is an open question.** Treat 2.6 +/- 0.2 as the provisional open-chain value, not as a result.

## Also withdrawn or voided

| Claim in versions 1 to 4 | Was | Now | Why |
|:---------------------|:-------|:---------------|:------------------------------------------|
| alpha = 3.92 +/- 0.16 (24 sites) and alpha = 3.97 +/- 0.15 (16 sites, exact) from stress-tensor exchange | headline result and its first corroboration | withdrawn | the same estimator artifact: both move in lockstep under it (3.92 to 2.56, 3.97 to 2.75 on dropping the contact point), because they share one observable, one fit window and one fitting routine |
| scalar exchange (alpha = 2) excluded | stated as excluded at about 12 sigma | withdrawn | the 12 sigma used the covariance error 0.16; at the bootstrap error 0.63 computed before release the exclusion is about 2.2 sigma, and under any window starting at separation 3 the point estimate itself falls to about 2.56 |
| alpha = 4 is universal; alpha = 4.00 at Ising, tricritical Ising and Potts | confirmed at three classes | withdrawn; the operator towers at all three classes stand | the exponent was measured only at Ising and inherited by the other two; the towers are spectra, not forces |
| third independent evaluation alpha = 4.07 (chi = 3 MERA), and with it the statement that this was the first holographic force measurement from an optimized tensor network state | supporting evidence and a priority claim | both withdrawn | the profile changes sign inside its own fit window and cannot be a fixed-sign power law; the priority claim rests on that evaluation alone and was never gated against prior work |
| the discriminating test: stress tensor (Z_j Z_j+1) versus spin primary (X_j) | registered killer test | void | at the critical point these are one operator, related by exact Kramers-Wannier self-duality. Measured on the periodic ring: identical expectation values to 1e-15 and identical force profiles to 1e-13 at 14 sites, 2.4e-9 at 24 sites (SIM-2026-074). Open boundaries break the duality, which is why the open-chain run of this test (SIM-2026-073) showed a spurious difference between the two arms. The test compared the energy density to itself. Neither label was correct: Z_j Z_j+1 is the energy density, not the stress tensor; X_j is its dual, not the spin primary |
| transport time T = (pi/2) l_AdS to 1.2 percent as a geometric prediction | confirmed | measurement stands (T = 2.239 at N = 16); geometric reading not established | l_AdS cancels in the cited derivation, which also gives pi rather than the pi/2 the manuscript compares against; the chi = 3 estimate of l_AdS gives a 57 percent miss; the transport driver never applies a MERA |

The true spin primary Z_j was never in the design, and the direct replacement test is blocked: Z_j is odd under the Z2 symmetry, so the energy-difference observable used throughout this work subtracts across symmetry sectors and is undefined for it. A replacement test using two Z2-even probes has been pre-registered (PREREGISTRATION-T.md, committed before its driver) and run; its result is deliberately not part of this correction and will appear in a later version.

## Not previously reported

The published fit has a reduced chi-squared of 6.008 on 9 degrees of freedom, and a bootstrap standard deviation of 0.63 rather than the quoted 0.16. Both were computed before release and omitted.

## What is unaffected

Of the claims in this record: the two-phase optimization method, the chi = 3 criticality threshold, the exact-diagonalization gates, the measured OPE coefficient C_sigma-sigma-epsilon = 0.50 +/- 0.03 against the exact 1/2, and the conformal towers at all three classes. Not part of this record, mentioned only because they are sometimes read together with it: the later C_TTT stress-tensor self-coupling measurements (SIM-2026-067/068/069, dated after this record) and the matched off-critical ring control (SIM-2026-074) are unaffected by this correction and make no claim about the force exponent.

## How the error was found and what this record contains

The error was found by the author's own internal adversarial audit, not by a reviewer; the journal submission it was found after is closed, and no review of this work has taken place. Files in this record: the full re-analysis (SIM-2026-072.json, driver, figure), the pre-registered chain test (SIM-2026-073.json) and ring test (SIM-2026-074.json) with both pre-registrations as committed before the runs, the runnable drivers with their shared module and the negative test suite for their validation gates, and the error register (ERRATA.md).

Concept DOI 10.5281/zenodo.19660302 always resolves to the current version.
