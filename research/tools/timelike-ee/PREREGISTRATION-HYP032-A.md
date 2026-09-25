# Pre-registration IV-A: the imaginary part as the registered question

**Status: APPROVED by Jon 2026-09-07 ("approved"), committed BEFORE any candidate code existed. Amends
PREREGISTRATION-HYP032.md after its Level-1 gate returned VOID (SIM-2026-076). Governs SIM-2026-077.**

## Why this amendment exists

SIM-2026-076 established, before any of this was planned:
- The literal lattice object `tau_A = Tr_B[e^{iRH}]/Tr` on the critical TFIM has EXACTLY real pseudo
  entropy for every R, T0, L, because `V = prod_j Y_j prod_{j even} X_j` satisfies `V H V^dag = -H`
  and makes the spectrum of `tau_A` closed under conjugation.
- With PAPER-139's regulator `e^{-delta H}` the REAL part follows `(c/3) log((R/pi) sin(pi T0/R))` at
  c = 1/2 to 2-3 percent; the IMAGINARY part stays at or below 0.017 against a prediction of 0.262 and
  never approaches it up to delta = 50.
- PAPER-139's own Fig. 6 calls the imaginary part "the challenge" and shows it approaching pi c/6 for
  a scalar only as delta grows, unstably.

The reel's second idea, and the paper's abstract, hang on that imaginary part ("emergent time").
So the amended, registered question is:

**Q. Is there ANY consistent lattice construction at c = 1/2 (or, as the control, at the paper's own
c = 1) whose exact evaluation gives `Im S = pi c / 6`, stable across the window?**

A YES on any registered candidate is a Level-1/2 reproduction with the construction named. A NO on
every registered candidate is a **Level-3 negative**: among these constructions, the imaginary part
of timelike entanglement entropy is a branch phase of the continuum analytic continuation, not an
observable of the lattice transition matrix, and "emergent time" has no lattice realization here.

## The four registered candidates (fixed now; no fifth may be added after results)

**C1. Chiral symmetry broken by a longitudinal field.** `H = -sum ZZ - sum X - h_z sum Z`, open chain.
The theorem needs `V H V^dag = -H`, which `h_z` destroys. Values `h_z = 0.05, 0.02, 0.01, 0.005`; if
Im S is nonzero, extrapolate `h_z -> 0`; if it returns to zero as the symmetry is restored, the zero
is robust. Regulator delta in {0, 2, 5}. This model is NOT free-fermion: exact diagonalization only,
L = 10, 12, 14 (2^14 = 16384, dense complex, fits on a 32 GB pod). Small L is the honest cost of
leaving the free theory.

**C2. Branch tracked continuously from real temperature.** Free TFIM, Gaussian route, L = 512 and
1024. Start at real inverse temperature `beta_0 = 20` (a thermal state, S real) and move along the
straight path `beta(s) = beta_0 (1 - s) + s (delta - i R_H)`, s from 0 to 1 in 400 steps, following
each mode value `nu_j(s)` and each log continuously (the branch that makes `S(s)` continuous).
Report `Im S(1)` for R = 50, 100 and delta in {0, 2, 5}. This is what the closed-form analytic
continuation does; it tests whether `i pi c/6` is a path-dependent phase that a principal-branch
evaluation drops.

**C3. Dirac chain, c = 1, the paper's own case.** Two decoupled critical TFIM chains = one free Dirac
fermion (c = 1/2 + 1/2). Gaussian route, L = 512, 1024, same R and delta grid as SIM-076. Prediction
`Im S = pi/6`. Checks whether c = 1/2 (a single Majorana) is special. Also the single-chain result
must equal exactly half of the two-chain result (a free identity gate).

**C4. Periodic ring with both fermion-parity sectors.** Free TFIM on a ring, `Tr` over the full
Hilbert space realized as the correctly weighted sum of the NS and R fermion sectors (the standard
`Z = (Z_NS+ + Z_NS- + Z_R+ - Z_R-)/2` bookkeeping, with signs fixed BEFORE running and checked
against exact diagonalization at L = 10, 12 to 1e-10 as a gate). L = 256, 512. This is the paper's
torus geometry (section 2.3). If the sector sum breaks the effective conjugation symmetry, Im S can
be nonzero here.

## Gates (controls; a failed gate voids that candidate, not the others)

- Every candidate: the exactness gate of SIM-076 (Gaussian spectrum = exact spectrum to 1e-10 at
  L = 10, 12 wherever a Gaussian route is used).
- C1: `h_z = 0` must reproduce SIM-076's `Im S = 0` to 1e-12 (the code path is the same).
- C2: at `s = 0` the entropy must equal the ordinary thermal entropy at `beta_0` to 1e-10; the path
  must not pass within 1e-3 of any zero of `Tr e^{-beta(s) H}` (recorded; if it does, the path is
  deformed by a fixed rule: add `+0.5 i` to `beta` at the crossing, and this is reported).
- C3: the two-chain result must equal twice the one-chain result to 1e-10.
- C4: sector-sum gate above.

## Pass, kill, and reporting (fixed now)

- **YES for a candidate:** `|Im S|` within 10 percent of `pi c/6` (0.2618 at c = 1/2; 0.5236 at c = 1)
  with one sign throughout the window `T0 in [3, R/2]`, window standard deviation under 10 percent of
  the mean, at BOTH sizes for that candidate, for at least one registered (R, delta, h_z) setting.
- **NO for a candidate:** anything else. Partial plateaus, drifting values, or a value at one size only
  are NO. Do not round toward YES.
- **Level-3 negative:** all four candidates NO.
- **Level-3 positive:** any YES, with the construction and parameters named. Its novelty passes
  through the section-8 gate before any wording stronger than "reproduced".
- The real part's slope (against 1/6 or 1/3) is reported for every candidate as a control but does
  not enter the verdict.
- Branch convention is stated for every number: per-mode principal (C1 uses per-eigenvalue), or
  tracked (C2).

## Compute and budget (decision of 2026-09-07: all runs on RunPod, none local)

RunPod CPU pod, 16-32 vCPU, 32 GB or more RAM (C1 at L = 14 needs ~8 GB for the dense complex
propagator plus workspace), spun up per run and torn down after results are fetched. Spending cap
for this amendment: **20 USD**. Exact diagonalization and Gaussian routes are numpy/scipy; no GPU.
Drivers are written and unit-tested locally against SIM-076's stored numbers ONLY through the
exactness gate at L = 10 (seconds); every registered run executes on the pod. Results land in
`research/data/simulations/SIM-2026-077.json` with pod id, image, and run log.

## Banned

Adding candidates after results; changing the 10 percent bar; changing branch rules after seeing
Im S; quoting a single-size value; calling a NO "inconclusive"; "first"/"novel" without the
section-8 record.
