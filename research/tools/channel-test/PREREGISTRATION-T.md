# Pre-registration III: the stress-tensor test HYP-2026-008 never had

**Written 2026-09-06, BEFORE the driver existed.** Committed before any code for it was written;
check `git log` on this file against the run record. Decisions taken with Jon in the grilling
session of 2026-09-06 (`docs/governance/PLAN-2026-09-06.md`, section T). Governs SIM-2026-075.

## Why a third experiment

HYP-2026-008 asks whether the holographic force between boundary excitations is carried by the
stress tensor (alpha = 2 Delta_T = 4) or by the energy density (alpha = 2 Delta_eps = 2). Its
registered test (SIM-2026-073, SIM-2026-074) compared `Z_j Z_{j+1}` against `X_j`, which at the
critical point are the SAME operator under Kramers-Wannier self-duality (ERRATA E8). Nothing that
has been run so far has probed the stress tensor at all: the "T" arm was the energy density, and the
"eps" arm was the Zou-Milsted-Vidal boundary primary, also Delta = 1. The direct spin-primary
replacement (`Z_j`) is blocked because it is Z2-odd and the energy-difference observable subtracts
across parity sectors.

This experiment uses two Z2-EVEN local probes whose leading CFT content differs by construction.

## The probes

At h = 1 the Kramers-Wannier map sends `Z_j Z_{j+1} <-> X_j` and acts on the Ising CFT as
`eps -> -eps`, `sigma <-> mu`, `T -> T`. Therefore:

- **Arm H (the stress-tensor-like probe): the local Hamiltonian density,**
  `O_H(j) = -(Z_j Z_{j+1} - <Z Z>) - (X_j - <X>)`. KW-even, so its expansion contains NO epsilon
  (KW-odd) and no epsilon descendants. Leading non-identity content: `T + Tbar`, Delta = 2. This is
  the same fact the Koo-Saleur construction rests on (SIM-2026-067/068/069): Fourier modes of the
  Hamiltonian density give `T_n + Tbar_{-n}`.
- **Arm E (the energy-density control): the KW-odd partner,**
  `O_E(j) = -(Z_j Z_{j+1} - <Z Z>) + (X_j - <X>)`. Leading content: `eps`, Delta = 1.

Both are sums and differences of operators already implemented (`op_T`, `op_X` in
`qw_channel_common.py`). Both are Z2-even, local (support {j, j+1}), and vev-subtracted. Both
excitations live in the parity +1 sector, so the observable
`F(dr) = [E_dual(dr) - E0] - [dE_single(j) + dE_single(j+dr)]` is well defined for both.

## Geometry, sizes, windows

Ring (PBC), chord distance `d_chord = (n/pi) sin(pi dr/n)` as PRIMARY, exactly as in
PREREGISTRATION-RING.md. Sizes **n = 16, 20, 24**. Windows fixed now on the same rules as before
(contact dr <= 2 excluded; antipode excluded; beyond antipode redundant):

| n | window dr | points | antipode |
|---|-----------|--------|----------|
| 16 | 3..7 | 5 | 8 |
| 20 | 3..9 | 7 | 10 |
| 24 | 3..11 | 9 | 12 |

n = 16 has only 5 points and 4 local slopes; a plateau there needs 3 of 4. It is included for the
convergence trend, not as a stand-alone verdict.

## Validation gates (every one is a CONTROL: failure voids the run or the arm, no verdict)

Run-level (raise `GateFailure`, run void):
- **G1 -- ground state.** PBC energy matches the free-fermion result to < 1e-6 (carried over).
- **G7 -- matched control.** The h = 2 ring, same two arms, same analysis, must return
  `CONTROL_CLEAN` (exponential decay, no chord-slope plateau in either arm). `CONTROL_CONTAMINATED`
  overrides everything, as in PREREGISTRATION-RING.md.

Per-arm (arm barred from every discriminant via `select_discriminant`; its failure is reported):
- **G2 -- ring symmetry.** `F(dr) = F(n - dr)` to < 1% (carried over).
- **G4 -- the probe IS what it claims. Two-point function scaling.** Before any force is read, the
  connected two-point function `<O(j) O(j+dr)> - <O>^2` of each arm on the critical ring must scale
  as a power of `d_chord` with exponent within **0.3 of 2 Delta** over the window at n = 24:
  Arm H -> 4, Arm E -> 2. This is a direct check that Arm H is Delta = 2 on this lattice at this size.
  If Arm H's two-point function does NOT go as chord^-4, Arm H is void and no force is measured with
  it. (The two-point function is also the NULL prediction for the force; see below.)
- **G5 -- Koo-Saleur identification, structural zeros.** In the n = 24 ring spectrum resolved by
  (energy, Z2 charge, momentum) as in SIM-2026-067, identify `|T>` (lowest even-sector |s| = 2 state)
  and `|eps>` (lowest even-sector s = 0 state above vacuum). Then, with `O(k)` the momentum-k Fourier
  mode of each arm: `<eps| O_H(0) |GS>` must vanish to < 1e-8 relative to `<T| O_H(2) |GS>` (KW-odd
  state, KW-even operator: a structural zero), and `<T| O_E(2) |GS>` must vanish to < 1e-8 relative
  to `<eps| O_E(0) |GS>`. Both zeros are exact identities if the arms are what this document says;
  a non-zero here means the vev subtraction or the KW bookkeeping is wrong.

## The null hypothesis, stated before running (RESEARCH-DIRECTOR.md section 6)

**Null: the force is the probe's connected two-point function, so alpha_H = 4 and alpha_E = 2.**
Conformal symmetry fixes this outcome completely. If it is observed, HYP-2026-008 closes as a
**Level 1 validation** ("the force sees whatever operator you probe with") with counterfactual
novelty near zero. It is NOT a discovery and must not be written up as one.

The only Level 3 outcome is a **DEVIATION** from the null. Everything else is null, void, or
indeterminate.

## Convergence, fixed now

For each arm, with `a(n)` the chord-fit log-OLS exponent on that size's window:
**converged** means `|a(24) - a(20)| < 0.1` AND `sign(a(24) - a(20)) = sign(a(20) - a(16))`
(monotone approach, shrinking step). Reported value: `a(24)`, with `|a(24) - a(20)|` quoted as the
finite-size systematic alongside the bootstrap sigma. If not converged, the arm's exponent is
reported as NOT CONVERGED with all three values and no verdict is drawn from it.

## Outcomes (thresholds fixed now)

With `a_H`, `a_E` converged chord-fit exponents at n = 24, `s` the larger of bootstrap sigma and the
finite-size step, and `Delta_2 = |a - 2 Delta|` the distance from the null:

- **N -- NULL CONFIRMED:** both arms within their bars: `|a_H - 4| <= max(3 s_H, 0.5)` and
  `|a_E - 2| <= max(3 s_E, 0.5)`. HYP-2026-008 closes, Level 1.
- **DEV -- DEVIATION (the registered finding):** an arm is **more than 3 s AND more than 0.5** from
  its 2 Delta, after convergence, with G4 passed (so the probe's own correlator DID scale correctly
  while the force did not). Report which arm, by how much, and the full slope series. Do not
  interpret beyond "the force is not the two-point function of this probe at these sizes".
- **C -- NO POWER LAW:** neither arm has a chord-slope plateau flat to 15% over >= 3 slopes.
- **D -- INDETERMINATE:** anything else, including not-converged. **Do not round toward DEV.**
- **VOID:** any run-level gate fails, or both arms are barred.

Precedence: VOID > CONTROL_CONTAMINATED (a form of VOID) > C > N/DEV > D.

## If Arm H fails G4

One retry, pre-registered: project the Arm H excitation onto the `|T>` momentum sector using the
SIM-2026-067 state identification (Koo-Saleur mode `O_H(k = 2)` applied to the ground state instead
of the local `O_H(j)`), re-run G4 on that object. If it also fails, HYP-2026-008 is closed as
**untestable at n <= 24 in this framework** and that closure is the result. No third attempt.

## Banned, carried over

Selecting windows after seeing exponents; the unweighted-linear-space estimator as a result;
"first"/"novel"/"to our knowledge" without a recorded section 8 gate; calling outcome N a
discovery; rounding D toward DEV; quoting an unconverged exponent as a value.

## Estimators, carried over

Headline: log-space OLS on `log|F|` vs `log d_chord`. Cross-check: relative-error-weighted NLS.
Uncertainty: nonparametric bootstrap, seed 20260817, whose sigma is a departure-from-power-law
measure and travels with `sigma_interpretation` in the record. Primary diagnostic: the chord-slope
series, not the whole-window fit.

## Record

Results to `research/data/simulations/SIM-2026-075.json` (chain of authority: this file's commit
hash, the driver's commit hash, the run log). Verdict field is null unless every gate above passed.
