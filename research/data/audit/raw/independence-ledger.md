# ana:independence — The Independence Ledger

**Task:** `ana:independence`. Governing standard: `docs/governance/RESEARCH-DIRECTOR.md` §7
(independence ledger), with §5 (contribution levels), §6 (counterfactual novelty), §8 (novelty
gates), §12 (killer tests), §17 (beyond single-number agreements), §18 (out-of-sample), §19
(matched controls).
**Date:** 2026-08-17. **Repo:** branch `public-release`, HEAD `9470d69`.
All paths repo-relative to `D:/quantum-worldline/`.

---

## 0. Scope, method, and the one-sentence answer

**Scope.** Every agreement, match, confirmation, or cross-check the project presents as evidence,
in any of: SIM records, hypothesis records, `NEXT-SESSION.md`, the memory index, the submitted PRD
manuscript (`research/submission-package/prd/paper-prd.tex`), the local SciPost v5
(`research/paper-draft-scipost.tex`), and the pipeline design/VENDOR docs. The task named nine
(a)–(i); I found **24** and ledger all of them.

**Method.** For each comparison I opened the record on both sides, opened the driver code that
produced each side where it exists, and asked: *if side A were wrong by a factor, would side B
move with it?* Where the answer was determinable by reading code or by re-deriving arithmetic,
I did that rather than trusting a record's prose. Section 8 lists what I could not determine.

**One-sentence answer.**

> Of the 24 agreements the project presents, **four** carry information that was not already in
> the inputs — the PAPER-133 `h_c(L)` reproduction, the PAPER-133 `g_1` match, the
> puMPS↔ED matched-N cross-implementation check (which the project has but mis-states), and the
> **sign** of the Yang-Lee biorthogonal product. The remaining twenty are exact CFT identities
> evaluated numerically, algebraic restatements of a single measured number, or the same state
> measured twice through the same code with one parameter changed.

---

## 1. Classification scheme (§7) as applied here

§7 supplies five labels. I use them with these operational definitions, stated so the reader can
check my assignments:

| Label | Operational test |
|---|---|
| **ALGEBRAICALLY EQUIVALENT** | Side B is computed from side A by a deterministic formula, in code, with no new input. Agreement is arithmetic, not evidence. |
| **STRUCTURALLY DEPENDENT** | Sides share the state, the code path, the fit window, or a parameter such that a common-mode error moves both. Disagreement would be informative; agreement is weak. |
| **PRIMARILY A CONSISTENCY CHECK** | Side B is an exact identity fixed in advance (CFT, Virasoro, kinematics). Only "implementation works / fails" was possible → §6 counterfactual novelty ≈ 0. |
| **PARTIALLY INDEPENDENT** | Sides differ in at least one load-bearing component (algorithm, code, state construction, or data source) but still share others. |
| **FULLY INDEPENDENT** | No shared code, no shared state construction, and side B is external data or a genuinely different algorithm. |

A comparison can be *both* a consistency check and structurally dependent; where so I give the
dominant label first.

---

## 2. Master ledger

Sorted by evidential weight, strongest first. `CN` = counterfactual novelty (§6).

| # | Comparison | Side A | Side B | Classification | CN | Evidential weight |
|---|---|---|---|---|---|---|
| L-16 | SIM-070 `h_c(L)` vs PAPER-133 Table S1 | project sparse-ED bisection, L=10…18 | published ED table, λ=4.0 row | **FULLY INDEPENDENT** (external) | low | **HIGH** — 5 points at ≤6e-7 |
| L-08a | SIM-070 `g_1` vs PAPER-133 X-prep | 0.725347 | 0.725339(51) | **FULLY INDEPENDENT** (external) | low | **HIGH** — 0.16σ |
| L-10 | puMPS N=12 vs SIM-067 ED N=12 (conventions matched) | Julia variational Bloch MPS | Python dense/sparse ED | **FULLY INDEPENDENT** | near-zero | **HIGH** — 5e-6 in `c`; **mis-stated in the repo** |
| L-11 | SIM-069 Potts ED gate N=10 vs puMPS N=10 | independent Julia ED | puMPS | **PARTIALLY INDEPENDENT** | near-zero | **MEDIUM-HIGH** — 1.4e-6 on E₀/site |
| L-06s | Yang-Lee `c_KS` **sign** vs +2/5 | measured product | unitarity expectation | **PARTIALLY INDEPENDENT** | **moderate–high** | **MEDIUM-HIGH** — the only genuinely binary outcome in the program |
| L-14 | SIM-071 raw numbers vs this audit's Python port | Julia/KrylovKit | Python/ARPACK | **FULLY INDEPENDENT** (raw only) | near-zero | MEDIUM — 6 decimals; validates transcription, not physics |
| L-19 | OF/Potts blocked-H vs dense reference (ED) | blocked operator | dense H | **PARTIALLY INDEPENDENT** | near-zero | MEDIUM — an *operator identity* check, not physics |
| L-05b | SIM-067 `C_sse_ME` = 0.49996 vs 0.5 | ED matrix element | BPZ 1984 exact | **CONSISTENCY CHECK** | near-zero | MEDIUM (as validation) |
| L-05a | SIM-061/064 `C_σσε` vs 0.5 | MERA PEV route | BPZ 1984 exact | **CONSISTENCY CHECK** | near-zero | MEDIUM, **and the best-converged rung misses** |
| L-01 | Transport T vs (π/2)·l_AdS | measured 2.23888 | (π/2)/ln 2 = 2.26618 | **PARTIALLY INDEPENDENT / convention-dependent** | **moderate** | MEDIUM — parameter-free, but two conventions and three competing l_AdS values |
| L-08b | SIM-070 `R_inf` vs −(1+√5)/2 | −1.61820 | exact BCFT | **CONSISTENCY CHECK** | low | MEDIUM — **but 3.87σ from PAPER-133's own X-prep number; see §5.2** |
| L-09a | SIM-015d 16q χ=3 MERA vs 16q exact ED | MERA force profile | ED force profile | **STRUCTURALLY DEPENDENT** | near-zero | LOW-MEDIUM — same state, one variationally approximated |
| L-07 | Ising unitary control vs 0.5 | `MODE=ising`, same file | exact c=1/2 | **STRUCTURALLY DEPENDENT / consistency check** | near-zero | LOW-MEDIUM — mechanism under test is switched **off** |
| L-04a | `C_TTT`(Ising) 3.9936 vs 4.000 | `2√2/√c_meas` | `2√2/√(1/2)` | **ALGEBRAICALLY EQUIVALENT** | near-zero | LOW |
| L-04b | `C_TTT`(TCI) 3.381 vs 3.3806 | `2√2/√c` | `2√2/√(7/10)` | **ALGEBRAICALLY EQUIVALENT** | near-zero | LOW |
| L-04c | `C_TTT`(Potts) 3.163 vs 3.16228 | `2√2/√c` | `2√2/√(4/5)` | **ALGEBRAICALLY EQUIVALENT** | near-zero | LOW |
| L-04d | "the ladder": three rungs agreeing | 067 (P2) | 068/069 (P3) | **STRUCTURALLY DEPENDENT** (shared formula + `Δ_T≡2` + KS lineage) | near-zero | LOW |
| L-03a | α = 3.92 vs stress-tensor 4 | force-profile fit | 2Δ_T, Virasoro | **CONSISTENCY CHECK** | near-zero | LOW — and the fit has no plateau |
| L-03b | α = 4.01 at TCI, α = 4.00 at Potts | 2 × measured Δ_T | 2 × 2 | **ALGEBRAICALLY EQUIVALENT** | near-zero | LOW — **no force was measured at either class** |
| L-03c | "α = 4 universal across three classes" | Ising *force* exponent | TCI/Potts *Δ_T* | **CATEGORY MISMATCH** (see L-03c) | near-zero | LOW |
| L-13 | "three consistent evaluations" of α ≈ 3.9–4.1 | 24q ED, 16q ED, 16q MERA | each other | **STRUCTURALLY DEPENDENT** | near-zero | LOW |
| L-02 | m_eff 0.693 vs 0.670 (3.5 %) | 1/l_AdS from Δ_ε=1 | l_AdS/ξ_2pt | **ALGEBRAICALLY EQUIVALENT up to one datum** | near-zero | **LOW — reduces to ξ_2pt ≈ l_AdS², one two-point ratio** |
| L-06m | Yang-Lee `c_KS` **magnitude** vs −22/5 | −4.29 ± 0.15 | −4.4 exact | **STRUCTURALLY DEPENDENT** | moderate | **LOW — 2.6 % is not robust; see L-06m** |
| L-17 | SIM-071 vs SIM-070 (same programme) | Phase 2 | Phase 1 | **STRUCTURALLY DEPENDENT** | — | LOW — Phase 2 inherits every Phase-1 systematic |
| L-15 | T·L conserved: 36.0 (N=16) vs 37.2 (N=24) | coarse-grid T | coarse-grid T | **STRUCTURALLY DEPENDENT** | moderate | **LOW — N=24 run is EXCLUDED by the project's own record** |

---

## 3. Per-comparison dossiers

Each dossier carries the eight §7 fields verbatim: raw data A, raw data B, shared theory, shared
fitted parameters, shared exact CFT identities, shared numerical code, shared state preparation,
genuinely independent information.

### L-01 — Transport `T` vs `(π/2)·l_AdS`  *(task item a)*

| §7 field | Content |
|---|---|
| **Raw data, side A** | `research/data/simulations/SIM-2026-025.json` → `.runs.N16.T_measured_refined` = **2.23888**, from a first-order Trotter evolution (dt = 1e−3, 6000 steps) of the **analytic Evenbly–White MERA** state under the Wang–He boundary Hamiltonian. Dip 2.49512, reappearance 4.734, both parabolically sub-grid refined. The N=16 boundary-density array `boundary_density_Y.npy` is the underlying raw object. |
| **Raw data, side B** | **None.** `research/submission-package/prd/paper-prd.tex:64`: `l_AdS = 1/ln χ = 1/ln 2 = 1.4427`, followed verbatim by *"This value is set by the MERA architecture, not by optimization."* Side B = (π/2) × 1.4426950408889634 = 2.2661800709135966 (`SIM-2026-025.json` → `.physical_parameters.T_null_pred`). It is two constants multiplied. |
| **Shared theory** | That MERA layer-depth ↔ AdS radial coordinate with metric normalisation `ds ∝ dz/z`, i.e. the Kim–Swingle identification `l_AdS = 1/ln χ`. Neither side is derived from the other, but neither is measured. |
| **Shared fitted parameters** | **None.** This is the comparison's genuine strength: the prediction has zero free parameters. |
| **Shared exact identities** | `T = π/2` from the embedding-space null condition `−⟨P₁,P₂⟩ = 1` (`composite_geodesic_results.json` → `.calculations.embedding_space`). This is two lines of algebra on `⟨P₁,P₂⟩ = −cos Δt − 1`; §6 counterfactual novelty ≈ 0 for the π/2 factor specifically. |
| **Shared code** | None — side B is not computed by code. |
| **Shared state prep** | n/a. **But note (§7-relevant):** the transport state is the *analytic* MERA, whereas the force result (L-03a) uses exact ED and the χ=3 result (L-09a) uses a variational MERA. The manuscript's own §3.1 discloses this. Nothing in the paper is one end-to-end pipeline. |
| **Genuinely independent information** | **The number 2.23888.** One measured time. |

**Classification: PARTIALLY INDEPENDENT, with a convention-dependence that is not disclosed.**

**Why it is not stronger than it looks — three specific, checkable points.**

1. **The time unit is a convention set inside side A.** `SIM-2026-025.json` →
   `.physical_parameters.hamiltonian` is
   `"Wang-He H_boundary = L/(4*pi) * sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}] (PBC)"`.
   The explicit `L/(4π)` prefactor **is** the clock. Rescale it and `T_measured` rescales
   inversely. No record derives that this prefactor and the `l_AdS = 1/ln χ` convention define the
   same unit of time; the agreement is asserted at the level of "both are the natural choice."
   This is the single largest unexamined shared assumption in the comparison.
2. **The same record contains three competing `l_AdS` values, spanning a factor 1.17.**
   `composite_geodesic_results.json` holds `l_AdS_MERA = 1.4426950408889634` (architecture),
   `l_AdS_fitted = 1.233` (from the SIM-002 V(dr) fit), and
   `l_AdS_needed_to_match_exact = 1.432394487827058` (back-solved from T = 2.25). With 1.233 the
   same record's own `T_null_fitted` = 1.9367918709381076 → `percent_error` = **−13.92 %**. The
   record's `verdict.best_agreement` field then names the architecture value *because* it agrees:
   *"l_AdS_MERA = 1/log(2) = 1.4427 gives T_null = 2.265, T_measured = 2.25, error = +0.69%."*
   Choosing among your own candidate constants by which one agrees is selection, not prediction.
   (Compounding: `research/data/hypotheses/HYP-2026-005.json` → `confidence_rationale` records that
   the 1.233 value was itself *"fit to approximate/visual data, not the actual simulation output"*
   — so the discarded alternative was discarded for a good reason. The point stands that the choice
   was made post hoc against the target.)
3. **The supporting finite-size argument is two points and the record says so.**
   `SIM-2026-025.json` → `.fit_1overN.note` concedes the N=12/N=16 fit is *"algebraically exact but
   degenerate — cannot distinguish 1/N from 1/N² without N = 24"*. N=24 is `"EXCLUDED"` with
   `exclusion_reason` *"clearly not the holographic transport signal"*. §17 (functional dependence,
   not single numbers) is not satisfied.

**What survives.** A parameter-free prediction landing within 1.21 % of a measured time is not
nothing. It is the **only** comparison in the program where side B contains no fitted quantity and
side A is a dynamical measurement. Under §6 its counterfactual novelty is genuinely **moderate**:
before the run, T could have been anything. That is more than can be said for the entire C_TTT
ladder. The correct framing is *"a parameter-free kinematic prediction, conditional on two
normalisation conventions neither of which has been independently fixed."*

**Killer test that would settle it (§12):** derive the `L/(4π)` normalisation and the
`l_AdS = 1/ln χ` normalisation from a single common convention, then re-predict. If they cannot be
put on a common footing, the 1.21 % is not a measurement of anything.

---

### L-02 — `m_eff` 0.693 vs MERA 0.670 (3.5 %)  *(task item b)*

| §7 field | Content |
|---|---|
| **Raw data, side A** | **None.** `research/data/simulations/effective_mass_analysis.json` → `.ads_mass_dimension.epsilon_m_eff` = **0.6931**. Derivation: Δ_ε = 1 (exact Ising) → `m²l² = Δ(Δ−2) = −1` (`.epsilon_m_squared_l2` = −1.0) → `|m| = 1/l_AdS = ln 2 = 0.693147`. Every input is exact. |
| **Raw data, side B** | `.comparison_to_measurements.xi_MERA` = **2.154**, then `.m_eff_from_MERA` = **0.6698**. I verified the functional form: `l_AdS/ξ = 1.4426950/2.154 = 0.669777` → 0.6698 ✔. So side B = `l_AdS / ξ_2pt`. |
| **Shared theory** | AdS/CFT mass–dimension relation `m²l² = Δ(Δ−2)`; the geodesic-approximation propagator `G ~ exp(−m·d_geo)`. |
| **Shared fitted parameters** | None fitted jointly, but **`l_AdS` = 1/ln 2 appears on BOTH sides** — as `1/l_AdS` on side A and as `l_AdS/ξ` on side B. |
| **Shared exact identities** | Δ_ε = 1 (Ising minimal model); `l_AdS = 1/ln χ`. |
| **Shared code** | Both numbers live in the same analysis file; no independent implementation on either side. |
| **Shared state prep** | Side B's ξ comes from `SIM-2026-002`, a **χ = 2** MERA. Side A is state-free. |
| **Genuinely independent information** | **`ξ_2pt = 2.154`, and nothing else.** |

**Classification: ALGEBRAICALLY EQUIVALENT up to a single datum.**

**The reduction, done explicitly.** Since side A = `1/l_AdS` and side B = `l_AdS/ξ`, the claimed
agreement `0.6931 ≈ 0.6698` is *identically* the claim

> `ξ_2pt  ≈  l_AdS²  =  (1/ln 2)²  =  2.08137`

against a measured `ξ_2pt = 2.154`. Residual (2.154 − 2.08137)/2.08137 = **3.49 %** — the record's
quoted 3.5 % ✔ (`.match_epsilon_vs_measured` = `"3.5% (0.693 vs 0.670)"`). Presenting this as
"two independent estimates of an effective mass agree to 3.5 %" is a restatement of a one-number
comparison in which the reader is invited to count two agreeing quantities where there is one.

**And that one datum is the weakest in the corpus.**
- `research/data/hypotheses/HYP-2026-005.json` → `.confidence_rationale` states ξ_2pt is
  *"xi_2pt=2.154 from the V(2)/V(1) ratio"* — **two data points** — and that
  *"SIM-2026-002 has only 2 real signal points … V(dr=3+) is numerical noise at the 10^-4 level.
  With 2 points, xi is underdetermined."* The hypothesis's own `confidence` is **`"low"`**.
- The state supplying those two points is the χ = 2 MERA whose correlations the *same manuscript*
  describes as flat / wrong universality class (`research/paper-draft-scipost.tex:486` figure
  caption; corroborated in `inv-sims-early.md` §4.2).
- `research/data/simulations/worldline_mc_results.json` →
  `.decay_analysis.m_eff_to_match_mera_2pt` is the literal token `NaN` (ERRATA D2), i.e. the
  companion record for this very quantity is invalid JSON.
- The project's own `research/data/theory/research-challenge.md:99-103` already reached the same
  verdict independently: *"post-hoc rationalization, not a prediction … The 'agreement' was found,
  not predicted."*

**Counterfactual novelty: near zero on side A (identity), and side B is a two-point ratio with no
uncertainty.** The manuscript's §8.6 correctly downgrades it to *"preliminary diagnostic"*; the
§4.2 table (`paper-prd.tex` L250-253) still typesets "Agreement 3.5 %" alongside measured
quantities. Under §7 this should read *"one two-point decay-length estimate is within 3.5 % of
l_AdS², which is what the ε-channel identification requires."*

---

### L-03 — `α = 4` "universal across three universality classes"  *(task item c)*

This is presented as the program's flagship universality result. It is **three different
observables** wearing one symbol. I split it.

#### L-03a — Ising: α = 3.92 ± 0.16 vs the stress-tensor value 4

| §7 field | Content |
|---|---|
| **Raw data, side A** | `research/data/simulations/SIM-2026-011-interaction.json` → `.F_interaction_avg`, 12 points from an exact 24-qubit `eigsh` ground state (`.ground_state.E0` = −30.199712331300333). Fit `.fits.F_avg_dr_ge2.power_law`: `alpha` = 3.921759726, `dalpha` = 0.158982157. |
| **Raw data, side B** | **None.** `α = 2Δ_T = 4` with `Δ_T = 2` in every unitary 2D CFT. `paper-prd.tex` §6.5 states it outright: *"Δ_T = 2 is a kinematic constant of conformal symmetry, independent of the central charge."* `SIM-2026-014.json` → `key_finding` says it follows *"exactly from conformal symmetry."* |
| **Shared theory** | The identification of the measured force with stress-tensor exchange — which is *inferred from the exponent match itself*. The manuscript concedes this (`paper-prd.tex` §5.3): the spin-2 identification *"rests on the exponent matching and requires further theoretical justification."* |
| **Shared fitted parameters** | Boundary-primary coefficients α = 0.635, β = −0.026 (`.boundary_primary_coeffs`), fixed a priori from literature — shared by every force evaluation. |
| **Shared exact identities** | Δ_T = 2. |
| **Shared code** | One fit routine, one window (`dr ≥ 2`). |
| **Shared state prep** | 24q exact ED. |
| **Genuinely independent information** | The 12 force values — **conditional on the fit window**, which is where the problem lies. |

**Classification: PRIMARILY A CONSISTENCY CHECK.** §6 counterfactual novelty near zero on the
theory side.

**Independence-relevant defect inherited from `inv-sims-early.md` §3.1–3.2 and re-checked here.**
The local logarithmic slope of `.F_interaction_avg` sits at 2.45–2.66 across the middle of the
range and touches 4 only at the single `dr = 2→3` step; refitting from `dr ≥ 3` gives α = 2.559 ±
0.019. The recorded ±0.16 is a covariance error at a fixed window; the window systematic is ~1.4,
i.e. ~8× larger, and larger than the entire α = 2 vs α = 4 discrimination the paper rests on.
**For this ledger the consequence is narrower and sharper:** the "independent information" in side
A is not 12 numbers, it is 12 numbers *plus one analyst choice that dominates them*. The choice is
not recorded as an uncertainty anywhere.

#### L-03b — TCI (c = 7/10) and Potts (c = 4/5): α = 4.01 / 4.00

| §7 field | Content |
|---|---|
| **Raw data, side A** | Scaling dimensions from the MERA scaling superoperator. `SIM-2026-051.json` (TCI χ=6): `Delta_T` per seed 1.9921, 1.9792, 1.9876, 2.0814, 1.9219, 2.0065, 2.1889, 1.9956. `SIM-2026-052.json` (χ=8): 1.9994, 2.0095, 2.0045, 2.0301, 2.0049, 2.0236. `SIM-2026-063.json` (Potts χ=12): `Delta_T = 2.0004/2.0023`. |
| **Raw data, side B** | Δ_T = 2, exact. |
| **Shared exact identities** | **α ≡ 2Δ_T, applied in the record itself.** I verified the arithmetic pairwise in `SIM-2026-051.json`: Δ_T 1.9792 → `alpha` 3.9583 (2×1.9792 = 3.9584); 1.9876 → 3.9752; 2.0814 → 4.1627; 2.0065 → 4.013. Every `alpha` field is exactly twice the adjacent `Delta_T` field. |
| **Shared code** | All four records come from the same MERAKit driver family (`qw_tci*.jl`, `qw_potts*.jl`). |
| **Genuinely independent information** | The measured `Δ_T` values. **`α` adds none.** |

**Classification: ALGEBRAICALLY EQUIVALENT.** The `alpha` column is a derived column typeset
beside measured ones. `inv-manuscript-claims.md` DEF-29 reaches the same conclusion on the
manuscript's universality table.

**The load-bearing fact: no force was ever measured at TCI or at Potts.** I grepped both record
families for a force observable and found none; the only α at those classes is `2Δ_T`. The
manuscript's own §8.7 open question 4 concedes it (*"The transport and force-profile measurements,
however, have been performed only at c = 1/2"*), three pages after §6.5 asserts that the recurrence
*"establishes that the holographic force exponent reflects stress-tensor exchange … The exponent
is universal."*

#### L-03c — The cross-class comparison itself

**Classification: CATEGORY MISMATCH, and therefore not a cross-check at all.**

| | Ising | TCI | Potts |
|---|---|---|---|
| what was measured | a **force profile** F(dr) on an ED ground state | a **scaling dimension** Δ_T from a MERA superoperator | same as TCI |
| pipeline | P5 (loose Python scripts in `research/data/simulations/`) | P1 MERAKit | P1 MERAKit |
| how α was obtained | fitted exponent, 3.92 ± 0.16 | 2 × Δ_T, algebra | 2 × Δ_T, algebra |
| could it have disagreed? | yes (and off-window it does) | only via a broken optimiser | only via a broken optimiser |

Two of the three "confirmations" cannot test the force claim because they do not measure a force;
they test whether MERAKit converges to the right CFT spectrum. That is a real Level-1 validation
of P1 and it is worth having — but it is **not** evidence that the force exponent is universal.

**What a genuine cross-class test would require:** measure F(dr) on a TCI or Potts ground state and
fit its exponent. That experiment does not exist in the repo. It is also the single cheapest
missing measurement in the whole program: the ED ground states and the force-observable code both
already exist (`SIM-2026-011-interaction.json` pipeline; `SIM-2026-051.json`
`.blocking_validation` shows the TCI operator is already built and ED-verified to 1.1e-16).

---

### L-04 — `C_TTT` vs `2√2/√c` at each class  *(task item d)*

| §7 field | Content |
|---|---|
| **Raw data, side A** | Ising: `research/tools/cttt-circle/qw_cttt_circle_results_ising.json`, `c_meas` = 0.421320 / 0.448547 / 0.463848 / 0.473251 / 0.479427 / 0.483693 at N = 8…18. TCI: `pumps-setup/qw_cttt_of_results_2026-08-10.jsonl`, c = 0.8295 → 0.70375 over N = 14…56. Potts: `qw_cttt_potts3_results_2026-08-11.jsonl`, c = 0.82201 → 0.80197 over N = 14…40. |
| **Raw data, side B** | **The same numbers.** |
| **Shared code** | **Verified by reading the source, all three rungs:** `cttt-circle/qw_cttt_circle.py:203` → `res["C_TTT"] = 2 * np.sqrt(2) / np.sqrt(res["c_meas"])`; `pumps-setup/qw_cttt_of.jl:116-117` → `c = 2*MT^2` then `cttt = 2*sqrt(2)/sqrt(c)`; `pumps-setup/qw_cttt_potts3.jl:131-132` → identical two lines; `pumps-setup/qw_pumps_validate_ising.jl:12` → same in the header comment and at L81. |
| **Shared exact identities** | `C_TTT = 2√2/√c` is a Virasoro identity, and it is the *only* thing relating the two sides. |
| **Genuinely independent information** | **Zero.** `C_TTT` is `c` in different units. |

**Classification: ALGEBRAICALLY EQUIVALENT — the strongest instance of it in the repo.**

**The project's own design doc says so** and deserves credit for it:
`merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md:96-102` states this measurement *"is of the same
epistemic kind as C_σσε = 0.5."* That honesty exists **only in the design doc**. The headline
framing in `NEXT-SESSION.md`, the memory index (*"THE LADDER IS COMPLETE … three classes ≤0.15 %
each"*), and `SIM-2026-069.json` → `key_findings[0]` (*"C_TTT measured at all three unitary
universality classes … each at ≤0.15 % agreement with 2*sqrt(2)/sqrt(c)"*) all present it as a
three-fold measurement of a self-coupling constant.

**A concrete arithmetic consequence nobody has flagged as an independence issue.** Because
`C_TTT` is a *nonlinear* function of `c`, extrapolating the two separately gives two different
answers from one dataset (`qw_cttt_circle.py:382-390` fits both in 1/N²):

- fitted `c(N→∞) = 0.49871` ⟹ implied `C_TTT = 2√2/√0.49871 = **4.00517**` (+0.13 %)
- separately fitted `C_TTT(N→∞) = **3.99361**` (−0.16 %)

The two differ by **0.29 %** — larger than either quoted deviation. SIM-067 quotes the second.
The "0.16 %" headline is therefore an **estimator choice within a single measurement**, and the
existence of two answers is itself proof that no second measurement is present.

**What would make `C_TTT` a real measurement:** the equal-time 3-point route,
`qw_cttt_circle.py:293` → `C_TTT = √2·A₃/|A₂|^{3/2}`, which uses ⟨hhh⟩ and ⟨hh⟩ and does **not**
pass through `c`. That route was killed the same day it was designed —
`CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117` records ⟨hh⟩_conn coming out negative with the exact
free-fermion tail `−(16/π²)/(4x²−1)²`, and instructs *"do not quote §3's A₂/A₃ formulas."* That
retraction is exemplary §32 behaviour **and it removed the only genuinely independent 3-point
measurement in the program.** The remaining "ladder" is a central-charge ladder.

#### L-04d — Do the three rungs cross-check each other?

| | Ising rung (067) | TCI rung (068) | Potts rung (069) |
|---|---|---|---|
| pipeline | P2, Python/scipy sparse ED | P3, Julia puMPS | P3, Julia puMPS |
| KS mode discretization | **naive** (one phase on the whole 2-site term, `qw_cttt_circle.py:183`) | **half-bond** (upstream ZMV `models.jl`) | half-bond |
| `Δ_T` | **measured** (`v_used = 2.0` hardcoded exact; `Delta_T` = 1.91154 → 1.98229) | **imposed** (`v_T = (ET−E0)*N/(2π*2.0)`, `qw_cttt_of.jl:114`) | imposed (`qw_cttt_potts3.jl:129`) |
| `C_TTT` | `2√2/√c` | `2√2/√c` | `2√2/√c` |
| shared code with the other rungs | none with 068/069 | ~80 of 140 lines shared with 069 (measured: `diff` reports 133 changed lines across 293) | same |

**Classification: STRUCTURALLY DEPENDENT across rungs.** 068 and 069 are the same driver with the
model swapped. 067 is genuinely a different implementation but uses a **different KS convention**
and therefore is not directly comparable to them (see L-10). Only the *model* varies across the
ladder; the formula, the `Δ_T ≡ 2` normalisation, and (for two of three) the code do not.

**One asymmetry worth recording as a positive:** 067 is the only rung where `Δ_T` is independent
data, because it fixes `v = 2` (exact for critical Ising with `h = −(XX+Z)`) and reads `Δ_T` out.
068/069/071 fix `Δ_T = 2` and read `v` out. Every rung spends exactly one exact CFT input; they
just spend it in different places.

---

### L-05 — `C_σσε` vs 0.5  *(task item e)*

Two separate routes reach this number. The project quotes the weaker one.

#### L-05a — MERA PEV route (`qw_ope_pev_z2.jl`)

| §7 field | Content |
|---|---|
| **Raw data, side A** | `SIM-2026-061.json` → `.results.C_sse`: per-seed 0.5053 / 0.4717 / 0.4708 / 0.4758 / 0.5298 / 0.5095 / 0.4981 / 0.5987 at χ=6, mean **0.5075**, spread 0.128. χ=8 confirmation (`.chi8_confirmation_2026-07-03`): 0.4887 / 0.5074 / 0.5115 / 0.5202, mean **0.5069**, spread 0.0315. |
| **Raw data, side B** | **None — 1/2 exactly, Belavin–Polyakov–Zamolodchikov 1984.** |
| **Shared theory** | Ising minimal-model fusion; the operator identification is by parity class, and σ/ε are *assigned* using their known CFT dimensions. |
| **Shared exact identities** | Δ_σ = 1/8, Δ_ε = 1 (used to identify the operators whose 3-point function is then measured), and the r₁₃ = 2 lattice-separation factor `2^{Δ_ε}` (which uses the **measured** Δ_ε — see the drift diagnosis below). |
| **Genuinely independent information** | The measured structure constant per basin — this **is** a real measurement of a quantity fixed in advance. |

**Classification: PRIMARILY A CONSISTENCY CHECK.** §6 counterfactual novelty near zero (exact since
1984). §5 Level 1.

**The independence-relevant defect: the headline value is the less converged one.**
`SIM-2026-064.json` → `.results.chi_progression_mean` records
`"0.5075 (chi6) -> 0.5069 (chi8) -> 0.4957 (chi10) -> 0.4722 (chi12): NOT monotone toward 0.5 --
crossed and undershot"`. At χ=12 the four basins give 0.4709/0.4719/0.4723/0.4736, spread
**0.0027** — i.e. the *tightest* rung is **5.6 % low and ~10 spreads away from 0.5**. The record's
own verdict is `"PRECISION ACHIEVED, ACCURACY PUZZLE FLAGGED"` and it explicitly instructs
*"do NOT quote C_sse=0.472 as final without resolving it."*

That instruction is right, and the record is honest. But the *project-level* headline
"C_σσε = 0.50 ± 0.03" (task brief; memory index; `NEXT-SESSION.md`) is the **χ=8** number, chosen
because its band brackets the exact answer. Under §7 the accurate statement is: *"agreement at
χ ≤ 8 where the basin spread is wide enough to contain 0.5; at χ = 12, where the spread collapses
to 0.6 %, the mean does not contain 0.5."* Quoting the looser rung because it agrees is the same
selection pattern as L-01's `l_AdS` choice.

Credit where due: `SIM-2026-064.json` → `.drift_suspects` lists three named mechanisms with tests,
and `.drift_resolution_2026_07_08` records the resolution as suspect (2), finite-χ placement
kinematics. That is §22 behaviour. The defect is presentational, not investigative.

#### L-05b — ED matrix-element route (`qw_cttt_circle.py`)

`qw_cttt_circle_results_ising.json` → `C_sse_ME` = 0.50980 / 0.50623 / 0.50431 / 0.50316 /
0.50242 / 0.50191 at N = 8…18, extrapolating to **0.49996**.

**This is a second, genuinely different route to the same number** — a ratio of matrix elements on
an exact ED spectrum, versus a MERA superoperator PEV trace. Different state construction,
different language, different observable definition, no shared code. Its residual is monotone and
converging, unlike L-05a's.

**Classification of L-05a vs L-05b as a mutual cross-check: PARTIALLY INDEPENDENT.** Shared: the
model, the operator identification via exact Δ's, and the target. Not shared: state, code,
estimator. **The project never presents them as a cross-check** — SIM-067 reports `C_sse` as an
incidental gate, and SIM-061/064 never cite it. This is a second instance (see L-10) of the project
holding a real independence result and not knowing it.

---

### L-06 — Yang-Lee `c_KS` vs `−22/5`  *(task item f)*

The program's strongest claim, and the only one with meaningful counterfactual novelty. It must be
split into a **sign** claim and a **magnitude** claim, because their independence properties differ
sharply.

| §7 field | Content |
|---|---|
| **Raw data, side A** | `research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl`, 5 lines, L = 10…18: `c_KS` = −1.4131953717819705, −1.7028834172130995, −1.9537294337235040, −2.1699263736663600, −2.3562438686552745. Both chiralities agree to ~1e-11. Extrapolated by a two-level Richardson estimator to **−4.285**, quoted as **−4.29 ± 0.15** (`SIM-2026-071.json` → `.results.extrapolation`). |
| **Raw data, side B** | **None.** `c = −22/5` is the exact central charge of the M(2,5) minimal model. |
| **Shared theory (five inputs, all upstream of the number)** | (1) `h_c^inf = 1.5587127` imported from SIM-070; (2) M(2,5) state identification — the conformal vacuum \|1⟩ is the **second** k=0 state, not the ground state; (3) `Δ_φ = −2/5` used to calibrate `v_ref`; (4) the Δ-gate window (1.75, 2.25) centred on the exact `Δ_T = 2`; (5) `v_T ≡ (E_T − E_vac)L/4π`, i.e. `Δ_T = 2` **imposed**. |
| **Shared fitted parameters** | `h_c^inf` — shared with SIM-070 and carrying a ~3× lever arm on the headline (see below). |
| **Shared exact identities** | `Δ_T = 2`; `Δ_1 − Δ_φ = 2/5`. Note these **cancel algebraically**: substituting `v_T` back gives `c_KS = 8·prod/(E_T − E_vac)²`, so `v_T` and `L` drop out. The CFT normalisation is an input that leaves no trace, not a check. |
| **Shared code** | One driver, `qw_yanglee_ks.jl` (**151 lines**, verified by `wc -l`; `inv-pipelines.md` quotes 152 — an off-by-one on the trailing newline, immaterial). Its momentum/KS layer is a direct port of `pumps-setup/qw_potts_ed_gate.jl` (identical translation-composed eigensolve idiom, identical `angle(-λ)` momentum decoding, identical `ens = SHIFT .- abs.(vals)`, identical half-bond phase). So P4's KS layer is **not** independent of P3's. |
| **Shared state prep** | Sparse non-Hermitian ED of the same chain as SIM-070, at the same working point. |
| **Genuinely independent information** | **The sign of the product, and its magnitude ratio to the φ-descendant.** Nothing else. |

#### L-06s — the SIGN. **PARTIALLY INDEPENDENT. CN moderate-to-high. This is the real result.**

Before the run, `c_KS` could have come back at +2/5 (Casimir/effective), at −22/5 (true, with the
indefinite-metric sign), or as noise. Three outcomes, three different interpretations, none forced
by an identity I can find. That is §6 **high** counterfactual novelty and it is the **only** place
in the entire repo where the pre-calculation outcome space had more than one physically meaningful
member.

The sign survives everything I can throw at it:
- every L from 10 to 18 is negative, both chiralities;
- it survives all three defensible `h_c^inf` values (`inv-pipelines.md` §5.6 measured
  −3.667 / −4.291 / −7.044 extrapolated — all negative, all ≥ 9× |c_eff|);
- it is corroborated structurally by `⟨1|1⟩ < 0` (the vacuum's biorthogonal norm), whose sign
  `inv-pipelines.md` §5.2 independently confirmed by re-implementation
  (−0.010656 / −0.003996 / −0.001507 at L = 10/12/14);
- the raw per-L numbers were reproduced to 6 decimals by an independent Python/ARPACK port (L-14).

**However, the sign is not fully independent of the theory input**, and the record does not say so.
`Δ_T = 2` enters twice: as the Δ-gate window and as the `v_T` definition. At Yang-Lee the
*empirical* discriminator inverts — `SIM-2026-071.json` → `key_findings[2]` reports the
φ-descendant's cross-module element is ~10× **larger** than T's. `inv-pipelines.md` §5.4(5) traced
the consequence: only one state falls inside (1.75, 2.25) at every L, so `argmax` is a no-op and
**T is selected by energy alone, against a window centred on the exact CFT answer.** So the sign
is the sign of *the product on the state the M(2,5) spectrum says is T*. If the identification were
wrong, the sign would be measuring something else. That is a theory-conditioned measurement, not an
unconditioned one — it is still the strongest thing here, but it is one notch below "independent."

#### L-06m — the MAGNITUDE (2.6 % from −22/5). **STRUCTURALLY DEPENDENT. Not robust.**

`SIM-2026-071.json` → `.caveats` claims *"Residual h_c^inf error contributes ≤0.01 at L=18."*
`inv-pipelines.md` §5.6 measured it directly by re-running Phase 2 at the three `h_c^inf` values
the project's own data support:

| `h_c^inf` | provenance | extrapolated `c_KS` | dev. from −22/5 |
|---|---|---|---|
| 1.5585927 | free-b fit — **what the tracked driver actually prints** (`yl_run_8_18.log:11`) | −3.667 | 16.7 % |
| 1.5587127 | b = 12/5 + L⁻⁴ — the adopted value | **−4.291** | 2.5 % |
| 1.5588876 | pure b = 12/5 | −7.044 | 60.1 % |

The quoted `± 0.15` does not contain this. The realistic band from fit-model choice alone is
roughly **[−7.0, −3.7]**. **The 2.6 % agreement is specific to one of three defensible fits of a
parameter shared with SIM-070.** I extend that finding decisively in §5.1 below: an external,
published, higher-precision value of `h_c^inf` existed and was not used.

**Verdict on L-06.** Report as: *sign and c_eff-exclusion decisive (≥9× under every variant);
magnitude consistent with −22/5 within a large working-point and estimator systematic that is
currently unquantified in the record.*

---

### L-07 — The Ising unitary control vs 0.5  *(task item g)*

| §7 field | Content |
|---|---|
| **Raw data, side A** | `SIM-2026-071.json` → `.unitary_control`: `c_KS` = 0.517483 (L=12), 0.512776 (L=14), 0.509748 (L=16); extrapolated **0.49986** (0.03 %). **No artifact exists** — `qw_yanglee_ks_results.jsonl` contains 5 lines, all Yang-Lee; a repo-wide grep for `0.517483\|0.512776\|0.509748\|0.49986` returns only prose files (`inv-pipelines.md` §5.10). |
| **Raw data, side B** | c = 1/2, exact. |
| **Shared code** | **148 of 152 lines.** The entire mode switch is `qw_yanglee_ks.jl:23-25` (`MODE`, `LAMBDA`, `HC`) plus two later branches (`ivac`, `v`). Shared byte-identical: the Hamiltonian/KS builder, both permutations, the translation-composed Arnoldi call (`ishermitian=false` **even in the Hermitian case**), the energy and momentum decoding, the biorthogonal pairing definition, the orientation selection, the Δ-gate window, the in-window dominance, the `v_T` normalisation, and the estimator. |
| **Shared state prep** | Same builder, different couplings. |
| **Genuinely independent information** | That the KS estimator, its factor of 2, its `(L/2πv_T)²` prefactor, the momentum decoding and the orientation logic are all correctly implemented. |

**Classification: STRUCTURALLY DEPENDENT / primarily a consistency check of the *unitary*
estimator.**

**The decisive fact: `HC = 0.0` in the control.** At h = 0 the `-im*h*mz*sph[j]` term in
`build_Hn` vanishes identically and **H becomes real symmetric, i.e. Hermitian.** Every mechanism
the frontier claim depends on is switched off:

| risk surface the claim depends on | exercised by the control? |
|---|---|
| indefinite metric / negative biorthogonal norm | **No.** `SIM-2026-071.json:11` says so itself: *"all biorthogonal norms +1.0000 (Hermitian limit)."* `inv-pipelines.md` §5.2 measured exactly +1.000000 (imag ≤ 2e-16) at L=12/14/16 for both vacuum and T. The headline depends on `⟨1\|1⟩ < 0`. |
| non-normality / eigenvector conditioning | **No.** At h=0 the matrix is normal; condition number is 1 by construction. At Yang-Lee `1/\|⟨ψ_L\|ψ_R⟩\|` reaches ~181 for T and ~4700 for the vacuum at L=18. |
| cross-state biorthogonality | **No — and never, in either mode.** `HYP028-BIORTHO-KS-DESIGN.md:36` mandates verifying biorthogonality *across states*; the driver only ever evaluates `biod(i,i)` (L95, L111, L117). |
| PT-unbroken guard | **No.** Phase 1 asserts it (`qw_yanglee_pt.jl:75`); Phase 2 has no such assertion, and `ens = S .- abs.(vals)` silently discards imaginary parts. |
| the inverted state-identification rule | **No — it is *anti*-exercised.** In the control the Δ-gate and element dominance **agree** (two states in window, dominance picks the right one, 0.27259 vs a Z₂ structural zero). At Yang-Lee they **disagree** by 10×. The control validates a discriminator that points at the wrong state in the case of interest. |

**§19 verdict: this control cannot defeat the interpretation, because the mechanism the
interpretation depends on is inert in it.** §19 requires *"a serious control should be capable of
defeating the preferred interpretation."*

**This is not a criticism of building it.** It is the right control and it passes a non-trivial
test — 0.49986 vs 0.5 is a real pass of the KS algebra and the code plumbing. The defect is that
the record and `NEXT-SESSION.md` present it as validating *the biorthogonal extension*
(memory index: *"Unitary control 0.49986/0.5"* cited immediately after the c = −22/5 claim). It
validates the estimator around which the extension is wrapped.

**Missing controls that would test the non-Hermitian layer** (§13 required-controls list, none
present): a second non-unitary model; synthetic non-normal matrices with known biorthogonal
structure; **solving `Hᵀw = Ew` directly instead of assuming `w = P v`** (the cheapest and most
direct pairing-invariance test, ~1 hour); an alternate eigensolver at higher precision; an h-scan
showing `c_KS` is stationary at the working point.

**One thing the estimator provably gets right, and claims nowhere.** `c_KS` is *exactly* invariant
under rescaling of the eigenvectors, including complex phases: under `v_i → α v_i` the numerator
picks up `|α|²` from the two elements and `biod(i,i)` picks up the same `|α|²`, which cancels. That
answers §13 Q3 (*"how sensitive is the extracted c to left/right eigenvector normalization?"*) with
**exactly zero sensitivity, by algebra.** It is a genuine property of the product-form choice and
should be stated as a proved result — it is currently claimed nowhere.

---

### L-08 — SIM-070's `g_1` and `R_inf` vs PAPER-133  *(task item h)*

**This is the only place in the program where a side of a comparison is genuinely external data.**
It therefore deserves the most careful treatment, and it is where this audit found the most new
material. `research/downloads/2606.16785v2.pdf` is on disk (509 KB, 19 pages); I extracted its
text and read Table S1 and the main-text results table directly.

#### L-08a — `g_1`: **FULLY INDEPENDENT external match, and it holds**

| | value | source |
|---|---|---|
| SIM-070 | **0.725347** | `SIM-2026-070.json` → `.results.g1.value`, window L ≥ 10 |
| PAPER-133, prep X | **0.725339(51)** | PDF main-text table, row `X` |
| BCFT exact | 0.725073 | PDF, same table row `BCFT`; = ((5−√5)/10)^{1/4} |

**(0.725347 − 0.725339)/0.000051 = 0.16σ.** Independent code, independent implementation,
independent numerics, against a published number. `SIM-2026-070.json` → `.results.g1.paper_value`
even records the comparison correctly: *"0.725339(51) -- our L>=10 value matches the paper's own
number."* **This is model behaviour and the strongest external anchor in the repo.**

Note what it does and does not establish: it establishes that the project implemented PAPER-133's
method correctly. It does not establish anything about Yang-Lee physics that PAPER-133 had not
already established. §5 Level 1 (reproduction), §6 counterfactual novelty **low** — the target was
a published table.

#### L-08b — `R_inf`: the record compares against the exact value, not against the paper's number

| | value | dev. from BCFT exact | σ from SIM-070 |
|---|---|---|---|
| SIM-070 | **−1.61820** | **0.011 %** | — |
| BCFT exact | −1.618034 | 0 | — |
| PAPER-133, **prep X** (the preparation SIM-070 used) | **−1.62184(94)** | 0.23 % | **3.87σ** |
| PAPER-133, prep Z | −1.61811(35) | 0.014 % | 0.26σ |
| PAPER-133, prep Rand | −1.6218(18) | 0.23 % | 2.0σ |

`SIM-2026-070.json` → `.results.R_inf` carries `exact: -1.618034` and `dev_pct: 0.01` and **no
`paper_value` field** — unlike the adjacent `g1` block, which does carry one.

**Finding (NEW, medium severity).** SIM-070 used the **X** preparation (`.method`:
*"X = product (|up>+|down>)/sqrt2 preparation"*). Its `g_1` is compared against the paper's **X**
row and matches at 0.16σ. Its `R_inf` is compared only against the exact BCFT value — and against
the paper's **X** row it sits **3.87σ outside the paper's own quoted uncertainty**, while
coincidentally landing within 0.26σ of the paper's **Z** row. Two readings, and I cannot
discriminate them:

- **Benign:** the project's estimator (two-level Richardson) is simply better than the paper's
  fit-window method at these L, and 0.011 % beats the paper's 0.23 % on the same preparation. Then
  the project has a small methodological win it has not claimed.
- **Adverse:** the project's `R_inf` is not reproducing the paper's X-prep computation at all, and
  the coincidence with the Z row means some part of the boundary-state construction differs.

Either way, **the record's anchor selection is asymmetric**: the paper's number is quoted where it
agrees (`g_1`) and omitted where it disagrees (`R_inf`). Under §7 both anchors must be reported.
The headline framing in memory (*"PAPER-133 reproduced 0.01%"*) is against the exact value, not
against PAPER-133.

**Second, independent caveat on the 0.01 %.** `inv-pipelines.md` §5.8 reconstructed the Richardson
tail from `yl_proj.log`: the diff ratios run 0.5581 → 0.6142 → 0.6671 → 0.7181, **monotonically
rising**. A geometric tail assumes a stable ratio. With the **mean** ratio the same data give
−1.61464 (0.21 %); the quoted −1.61820 (0.011 %) requires selecting the **last** ratio. SIM-070 is
transparent that the ratios run "0.56→0.72" (`.results.R_inf.method`), so nothing is concealed —
but 0.01 % is an estimator-selection coincidence presented as precision. This matters for L-06m,
because `SIM-2026-071.json` → `key_findings[4]` cites *"the same two-level Richardson estimator
that hit 0.01 % on SIM-070's R_inf"* as evidence for the Phase-2 extrapolation.

#### L-08c — `h_c(L)`: **the strongest fully-independent check in the entire program**

Nobody in the project has presented this as a cross-check. It is the best one they have.

PAPER-133 Table S1 (*"Finite-size Yang–Lee exceptional points h_c(L;λ) obtained by exact
diagonalization"*), row λ = 4.0, against `SIM-2026-070.json` → `.results.hcL`:

| L | PAPER-133 Table S1 | SIM-070 | Δ |
|---|---|---|---|
| 10 | 1.57505330308 | 1.5750539 | +6.0e-7 |
| 12 | 1.56932743241 | 1.5693276 | +1.7e-7 |
| 14 | 1.56607420069 | 1.5660746 | +4.0e-7 |
| 16 | 1.56407088458 | 1.5640705 | −3.9e-7 |
| 18 | 1.56276039474 | 1.5627601 | −3.0e-7 |

Five points at the bisection-precision level, from an independently written sparse-ED bisection
against a published ED table. **FULLY INDEPENDENT. This is real.** It is also, honestly, a
validation of a root-finder rather than of physics — §5 Level 1, §6 counterfactual novelty low —
but it is precisely the kind of external anchor §7 asks the project to identify and it should be
stated in SIM-070 and in any methods paper.

#### L-08d — **NEW, MAJOR: the published `h_c^∞` was available and was not used**

PAPER-133 Table S1's last column gives, for λ = 4.0:

> **h_c^(∞) = 1.55872195(5)**

`SIM-2026-070.json` → `.results.hc_inf` = **1.5587127**, obtained by the project's own fit
(*"fixed-exponent fit (b=12/5 + L^-4 subleading)"*) to its own L = 8…18 table.

**Δ = −9.25e-6 = 185 × the paper's quoted uncertainty (5e-8).**

I refit all three models to both datasets to locate the cause:

| data | b = 12/5 | b = 12/5 + L⁻⁴ | free-b |
|---|---|---|---|
| SIM-070, L = 8…18 (what was used) | 1.5588876 | **1.5587127** ✔ reproduces the adopted value exactly | 1.5586049 (b = 2.342) |
| SIM-070, L = 10…18 (drop L = 8) | 1.5588110 | 1.5587155 | 1.5586548 (b = 2.357) |
| **PAPER-133 table, L = 10…22** | 1.5587876 | **1.5587180** | 1.5586747 (b = 2.362) |
| PAPER-133 published | — | **1.55872195(5)** | — |

So the project's fit model is sound — applied to the paper's own 7-point table it gives 1.5587180,
within 4e-6 of the paper's published value. The residual gap comes from the shorter L range and
from including L = 8.

**Why this matters more than 9e-6 suggests.** `h_c^inf` is the single most lever-armed parameter in
the frontier result. `inv-pipelines.md` §5.6 measured the transfer: Δh = 1.2e-4 moved the
extrapolated `c_KS` from −3.667 to −4.291, and a further Δh = 1.75e-4 moved it to −7.044. The
project's own SIM-070 `key_findings[1]` states the same thing in its own words:
*"h-sensitivity grows as L^{12/5} … Extrapolation quality is limited by h_c^inf precision before
anything else."*

**Consequences for the independence ledger:**

1. The `h_c^inf` used in SIM-071 is **project-internal**, not external. The frontier result's most
   sensitive input was fitted in-house when a published, 3-orders-tighter value existed **in the
   same table the project was reproducing**. That converts what could have been a partially
   external anchor into a fully internal one, and it is why L-17 (SIM-071 vs SIM-070) is
   structurally dependent rather than partially independent.
2. There is a **free, decisive, ~1-hour test** sitting here: re-run Phase 2 at
   `h = 1.55872195` and report `c_KS`. If the headline moves materially, the ±0.15 band is wrong
   and the record must say so; if it does not, the project gains a genuine external pin on its most
   fragile parameter. Either outcome is informative. **This is my top recommendation in §8.**
3. PAPER-133 also publishes L = 20 and L = 22 `h_c` values the project never used, and SIM-070's
   own `.method` says it ran *"L=8..20 (2^20 = 1M-dim top rung)"* for the projections — so an L=20
   rung exists on the R-side but the `h_c` fit stopped at 18.

**I did not** attempt to estimate the resulting shift in `c_KS`; doing so requires re-running the
non-Hermitian Arnoldi and my extrapolation of the §5.6 sensitivity curve to Δh = +9e-6 is
non-linear and unreliable. Recorded in §7 UNVERIFIED.

---

### L-09 — MERA-vs-ED comparisons  *(task item i)*

There are **five** distinct ones. They are not of the same kind and the project treats them as if
they were.

#### L-09a — 16q χ=3 MERA force vs 16q exact ED force (`SIM-2026-015d.json`)

| §7 field | Content |
|---|---|
| Raw data A | `.exact.V_data`, 11 points from `E0_exact = −20.01638790048509` |
| Raw data B | `.mera.V_data`, 11 points from `E_mera = −19.986111293142905` (0.151 % energy error) |
| Shared | **the Hamiltonian, the observable definition, the boundary-primary coefficients, the fit model, the fit window (`fit_dr_min: 2`, `fit_n_pts: 10`), the fit code, and — crucially — the target state.** The MERA is a variational approximation *of the very ED state on side A*. |
| Independent info | how much a 0.151 %-energy-error variational ansatz distorts a 10⁻³-scale observable. |

**Classification: STRUCTURALLY DEPENDENT.** Result: α = 3.9748 ± 0.1451 (exact) vs 4.0712 ± 0.1778
(MERA). This is an **ansatz-quality check**, which is a legitimate and useful thing — but it is not
an independent confirmation of α = 4, because if the observable or the window were wrong, both
sides would be wrong identically.

**Additional defect visible in the raw data.** `.mera.V_data` has `"9": +0.0012014968` and
`"10": +0.00036517276` — two **positive** values inside a 10-point window fitted to a strictly
negative power law with `sign: -1`. The fit is therefore to |F| including two sign-flipped points.
The manuscript discloses the sign flip (`paper-prd.tex` §6.4) but not that the flipped points are
inside the fit. Nothing in the record quantifies their effect on α = 4.07.

#### L-09b — Exact-diagonalisation **operator** pre-gates (`SIM-2026-051`, `SIM-2026-062`)

`SIM-2026-051.json` → `.blocking_validation.result`: *"max|H_orig − H_recon| = 0 (lam3=0) and
1.1e-16 (lam3=0.856) on 6- and 8-site PBC rings."* `SIM-2026-062.json` → `.what_was_built`:
graded H validated against the dense reference to **1.75e-15**.

**Classification: PARTIALLY INDEPENDENT, and correctly scoped.** These check that the *blocked
operator equals the original operator* — an algebraic identity between two representations of the
same matrix. They cannot detect a physics error; they detect a construction bug, which is exactly
what they are for. `memory: of_blocking_was_never_wrong` records that this gate resolved a real
prior confusion (a MERA wrong-basin artifact that had been misread as non-critical σ). **Good §22
practice.** Do not count them as evidence for α = 4.

#### L-09c — MERA basin selection *by spectral quality*

`SIM-2026-051.json` → `.best_spectrum_seed.selection` = *"lowest Delta_sigma (cleanest critical
basin)"*, with `.notes`: *"at chi=6 the energy is FLAT across basins (all 8 seeds within E-spread
3e-4) so energy CANNOT select the critical fixed point."*

**This is a selection-on-the-target procedure and it is disclosed.** Δ_σ is selected toward its
known CFT value, and Δ_T is then read from the selected basin. The defence — that Δ_T clusters at
2.0 across *all* basins — is stated and is what makes the procedure acceptable
(`SIM-2026-051.json` → `.delta_T_statistics.all_8_seeds_mean` = 1.9913). **For the ledger:** any
"agreement" read from a spectrally selected basin is conditioned on the selection, so Δ_σ vs 1/8
in those records is **not** an independent check; Δ_T vs 2 is, weakly, because it was not the
selection criterion.

**Selection rate is reported unevenly.** `SIM-2026-062.json` reports 4/6 clean basins at χ=6;
`SIM-2026-063.json` reports 3/6 at χ=9 and **2/6 at χ=12** — and the χ=12 headline
(Δ_σ = 0.132/0.135, Δ_T = 2.0004/2.0023) therefore rests on 2 of 6 optimisations. The manuscript
quotes the 4/6 rate and not the 2/6 rate (`inv-manuscript-claims.md` DEF-10).

#### L-09d — MERA (P1) vs ED/puMPS (P2/P3) on `C_TTT` Route A

`SIM-2026-066.json` — MERA Route A at χ=10 gave 8.29 and 146.1; at χ=12 gave 2.22, 2.15, 25.7,
0.057, and one seed 6e8, against the target 4.000. **Route A was closed rather than salvaged.**

**Classification: a decisive NEGATIVE, correctly reported.** For the ledger this is important in
two ways: (i) it is one of the few results in the repo with non-trivial counterfactual novelty
(*could* Route A resolve spin-2? answer: no); (ii) it means the MERA pipeline has **never**
independently reproduced the ED/puMPS `C_TTT` result, so there is **no MERA↔ED cross-check on
`C_TTT` at all**.

#### L-09e — puMPS↔ED, treated separately as L-10 and L-11 below.

---

### L-10 — puMPS N=12 vs SIM-067 ED N=12  *(not in the task list; the repo's best internal check, mis-stated)*

`pumps-setup/VENDOR.md:44-52` step-1 validation table, verbatim rows:

| quantity | puMPS | "exact / SIM-067" |
|---|---|---|
| Δ_T (energy) | 1.960387 | 2 (finite-N, matches ED scale) |
| c_meas | 0.497156 / 0.497155 | 0.5 |
| **C_TTT** | **4.0114 (raw N=12)** | 4.000 (**SIM-067 extrapolated 3.9936**) |

with the conclusion *"The puMPS pipeline reproduces the SIM-067 circle/KS extraction."*

**SIM-067's own values at N = 12** (`cttt-circle/qw_cttt_circle_results_ising.json`, N=12 entry,
which I read directly): `c_meas` = **0.463848**, `C_TTT` = **4.152955**, `Delta_T` = **1.960316**.

Two things follow, and they point in opposite directions:

1. **The Δ_T row is a genuine matched-N agreement and nobody says so:** puMPS 1.960387 vs SIM-067
   1.9603163662814211 — **Δ = 7.06e-5**. Two completely different state constructions (variational periodic MPS vs
   exact sparse ED), two languages, agreeing on the T-gap.
2. **The `c` row is a 7.2 % matched-N *disagreement*, presented as agreement** by substituting
   SIM-067's *extrapolated* number for its *N=12* number. 0.497156 vs 0.463848.

The two facts together diagnose the cause exactly: `Δ_T` is a pure energy quantity and is
insensitive to the Koo–Saleur mode discretization; `c` comes from the KS matrix element and is
**not**. `inv-pipelines.md` §3.4 identified the mechanism — `qw_cttt_circle.py:183` applies **one**
phase `e^{inx·2π/N}` to the whole two-site term, whereas the vendored ZMV `models.jl`, the Potts ED
gate, and the Yang-Lee driver all use the **half-bond** convention (site phase `e^{inj·2π/N}`, bond
phase `e^{in(j+½)·2π/N}`) — and measured the fix: rebuilding SIM-067's ED with the half-bond phase
gives `c` = 0.495901 / **0.497151** / 0.497905 / 0.498396 at N = 10/12/14/16.

**0.497151 (ED, half-bond) vs 0.497156 (puMPS) = 5e-6 in `c`, 3e-6 in the matrix element.**

**Classification once conventions are matched: FULLY INDEPENDENT.** Different language, different
algorithm, different state construction, no shared code, matched N, no extrapolation. **This is the
single strongest internal cross-validation the project possesses, and the repo currently records it
as a 7 % discrepancy papered over with an extrapolated number.** The convention difference is
documented in no SIM record, no design doc, and no VENDOR note.

**Recommendation (repeated in §8):** replace the VENDOR.md step-1 row with the matched-N comparison
and document the KS mode-discretization convention. It is the difference between a 1e-5-level and a
7 %-level cross-check, and it costs an hour.

---

### L-11 — Potts ED gate N=10 vs puMPS N=10 (`SIM-2026-069`)

`SIM-2026-069.json` → `.ed_gate`: *"E0/site 1.4e-6 (variational), T gap 1.8e-4 rel, v's <1e-4, gap
ratio 6.1929 vs 6.1924."*

| §7 field | Content |
|---|---|
| Shared | the model, the Hamiltonian convention, the **half-bond KS phase**, and the translation-composed eigensolve idiom (`qw_potts_ed_gate.jl` is the file the Yang-Lee driver was later ported from) |
| Not shared | the state construction (exact ED vs variational Bloch MPS), the optimiser, the eigensolver |
| Independent info | that the d=3 CG plateau at \|grad\| ≈ 2.5e-4 does **not** contaminate the measurement |

**Classification: PARTIALLY INDEPENDENT, and methodologically exemplary.** This gate exists
precisely because the optimiser could not be driven lower, and `qw_cttt_potts3.jl:64-66` states
outright that *"measurement quality is certified by the N=10 ED gate, **not** by |grad|."* That is
the right instinct and the right control.

It also produced a genuinely independent adverse finding the project reported against itself
(`.ed_gate.extra_findings`): raw ED element-dominance at N=10 picks a UV state at Δ ~ 2.53 with
4.5× T's element, which *"would give c = 5.9"* — i.e. the identification rule used elsewhere in the
program fails here, and puMPS Bloch elements are what rescue it. **Recording a case where your own
selection rule breaks is §32 behaviour and is worth more than the agreement itself.**

---

### L-12 — `Δ_T = 2` → `α = 4`

**Classification: ALGEBRAICALLY EQUIVALENT to the Virasoro statement.** `Δ_T = 2` holds in every
unitary 2D CFT; `paper-prd.tex` §6.5 says so in the manuscript's own voice. And in P3/P4 `Δ_T` is
not even measured — `qw_cttt_of.jl:114`, `qw_cttt_potts3.jl:129` and `qw_yanglee_ks.jl:128` all
*define* `v_T` by imposing `Δ_T = 2`. So in those pipelines "Δ_T = 2" is an input that appears on
both sides of nothing.

---

### L-13 — "Three consistent evaluations" of α ≈ 3.9–4.1

| | 24q exact | 16q exact | 16q χ=3 MERA |
|---|---|---|---|
| model | critical TFIM, OBC | same | same |
| state | `eigsh` | `eigsh` | MERA optimised **to that same H** |
| observable | `F = E_dual − E₀ − 2ΔE_single` | identical | identical |
| boundary-primary coeffs | α = 0.635, β = −0.026 | same | same |
| fit model / window | `A·dr^−α`, `dr ≥ 2` | identical | identical |
| fit code | same | same | same |

**Classification: STRUCTURALLY DEPENDENT / consistency check.** One observable, one operator, one
fitting procedure, one window, at two system sizes of one model plus one variational approximation
of one of them. The manuscript's phrasing — *"three consistent evaluations"* (Abstract; §5.3
*"independently confirmed"*) — is literally true and reads as more than it is.

**Credit:** `paper-prd.tex` §6.5 contains the correct framing three lines from the incorrect one:
*"the three force measurements above all sample the same conformal fixed point — the c = 1/2 Ising
CFT — so they test the *value* α = 4 but not its claimed *origin*."* The manuscript already knows;
the Abstract and §5.3 do not reflect it.

**The window systematic is common-mode.** Because all three share `dr ≥ 2`, dropping to `dr ≥ 3`
moves all three the same way — 3.922→2.559, 3.975→2.753, 4.071→2.745 (`inv-sims-early.md` §3.2).
Three evaluations that move together under the dominant systematic are one evaluation.

---

### L-14 — SIM-071 raw numbers vs this audit's independent port

`inv-pipelines.md` §5.2 re-implemented `qw_yanglee_ks.jl` in Python (ARPACK instead of KrylovKit,
independently written sparse builders) and reproduced **all six** published raw numbers to 6
decimals — the three Yang-Lee `c_KS` values *and* the three unitary-control values for which the
repo retains **no artifact at all**.

**Classification: FULLY INDEPENDENT at the raw-number level.** This is the §40 "reproduce the
Yang-Lee result through an independent code path" slice and it **passes**.

**What it establishes:** the numbers in `SIM-2026-071.json` are what the algorithm produces; the
hand-transcribed control values are correct; the sign of `⟨1|1⟩` is confirmed.
**What it does not:** anything about the extrapolation, the state identification, the working point,
or the physics. It validates transcription and implementation, not interpretation.

---

### L-15 — `T·L` approximately conserved (36.0 at N=16 vs 37.2 at N=24)

**Classification: STRUCTURALLY DEPENDENT, and built on a record the project itself excluded.**
Both sides are coarse-grid (dt = 0.05) transport times from the same protocol. The N=24 number
(1.55) comes from `holographic_transport_24q.json`, whose own
`.lin_finite_size.lin_1N_consistent` = **"INCONSISTENT"** and whose `residual_pct` = −31.6, and
which `SIM-2026-025.json` → `.runs.N24.exclusion_reason` describes as *"clearly not the holographic
transport signal"* and marks `"EXCLUDED"`. The manuscript hedges it correctly (*"an empirical
observation, not a derived result … provisional"*), but a two-point trend using an excluded run is
not evidence. §17 unsatisfied.

---

### L-16 / L-17 / L-18 / L-19 — remaining entries in brief

- **L-16** — `h_c(L)` vs PAPER-133 Table S1. Fully treated in **L-08c**. Fully independent, holds.
- **L-17 — SIM-071 vs SIM-070.** **STRUCTURALLY DEPENDENT.** Same model, same chain, same
  `h_c^inf`, same left-pairing choice (`η = P`), same driver family. Phase 2 inherits every Phase-1
  systematic, including the `h_c^inf` fit-model choice (L-06m) and the Richardson estimator whose
  Phase-1 stability claim does not survive inspection (L-08b). SIM-070 is a **gate**, not a
  cross-check, and the records treat it correctly as such.
- **L-18 — Z₂ two-phase VQE method, 1.12 % @ 8q / 3.33 % @ 24q** (`SIM-2026-008b-8q-test.json` →
  `.best_error_pct` 1.1150; `SIM-2026-008c.json` → `.best_error_pct` 3.33399, 5 seeds). **Not a
  cross-check at all** — it is an optimiser result with seed spread, compared against an exact
  ground-state energy. §5 **Level 2 (methodological)**, §6 counterfactual novelty genuinely
  non-zero (the optimiser could have failed at any level). Its weakness is §21 (no environment, no
  code revision, θ output untracked), not §7. **This is one of the few numbers in the corpus that
  is not fixed in advance by conformal symmetry.**
- **L-19 — blocked-operator vs dense reference.** Treated in L-09b. An operator identity check;
  correctly scoped; not physics evidence.

---

## 4. Shared-input dependency map

The §38-C dependency question, answered for the ledger. Read each column as: *if this input were
wrong, which agreements would move?*

| Shared input | Where it is fixed | Comparisons it moves |
|---|---|---|
| `Δ_T = 2` (Virasoro, every 2D CFT) | `paper-prd.tex` §6.5; imposed in code at `qw_cttt_of.jl:114`, `qw_cttt_potts3.jl:129`, `qw_yanglee_ks.jl:128` | L-03a, L-03b, L-03c, L-04a-d, L-06, L-07, L-12, L-13 |
| `C_TTT = 2√2/√c` (Virasoro) | `qw_cttt_circle.py:203`, `qw_cttt_of.jl:117`, `qw_cttt_potts3.jl:132` | L-04a, L-04b, L-04c, L-04d |
| `l_AdS = 1/ln χ = 1/ln 2` (MERA architecture convention) | `paper-prd.tex:64` | **L-01 and L-02, on both sides of each** |
| `L/(4π)` boundary-Hamiltonian normalisation (time unit) | `SIM-2026-025.json` → `.physical_parameters.hamiltonian` | L-01, L-15 |
| `Δ_ε = 1` (Ising) | exact | L-02 (both sides), L-05a |
| `Δ_σ = 1/8` (Ising) | exact | L-05a, L-05b, L-09c |
| `C_σσε = 1/2` (BPZ 1984) | exact | L-05a, L-05b |
| boundary-primary coeffs α = 0.635, β = −0.026 | `SIM-2026-011-interaction.json` → `.boundary_primary_coeffs` | L-03a, L-09a, L-13 |
| fit window `dr ≥ 2` | `SIM-2026-011-interaction.json`, `SIM-2026-015d.json` `.fit_dr_min` | **L-03a, L-09a, L-13 — common-mode, and dominant** |
| `h_c^inf = 1.5587127` | `SIM-2026-070.json` → `.results.hc_inf`, fitted in-house | **L-06s, L-06m, L-17 — dominant systematic** |
| M(2,5) state identification (\|1⟩ = 2nd k=0 state, Δ_φ = −2/5) | `HYP028-BIORTHO-KS-DESIGN.md`; hardcoded Δ-gate `qw_yanglee_ks.jl:124` | L-06s, L-06m |
| half-bond KS phase | `puMPS/models.jl`, `qw_potts_ed_gate.jl:92`, `qw_yanglee_ks.jl:35` | L-04d, L-06, L-10, L-11 |
| translation-composed Arnoldi idiom | `qw_potts_ed_gate.jl` → ported into `qw_yanglee_ks.jl` | **L-06, L-11 — P3 and P4 are not independent in their momentum/KS layer** |
| MERA basin selected by lowest Δ_σ | `SIM-2026-051.json` → `.best_spectrum_seed.selection` | L-05a, L-09c, and every P1 Δ value |

**Two structural observations that fall out of the map.**

1. **`l_AdS = 1/ln 2` is the most load-bearing single convention in the manuscript's results**, and
   it appears on *both sides* of both L-01 and L-02. It is not measured anywhere. Every "geometric"
   agreement in the paper is, at bottom, a statement about this one constant.
2. **Only P2 (`cttt-circle`) has an independently written momentum/KS layer**, and it uses a
   *different* KS discretization from everything else — so the program's one architecturally
   independent implementation is also the one that is not directly comparable to the others until
   the convention is reconciled (L-10).

---

## 5. Findings new to this audit

### 5.1 — PAPER-133 publishes `h_c^∞`, three orders tighter, and it was not used (**MAJOR**)

Full treatment in **L-08d**. Summary: `research/downloads/2606.16785v2.pdf` Table S1, row λ = 4.0,
last column gives **h_c^(∞) = 1.55872195(5)**. `SIM-2026-070.json` → `.results.hc_inf` uses
**1.5587127**, fitted in-house from L = 8…18. Δ = 9.25e-6 = **185× the paper's uncertainty**.
Because `SIM-2026-070.json` → `key_findings[1]` itself states *"Extrapolation quality is limited by
h_c^inf precision before anything else"*, and because `inv-pipelines.md` §5.6 measured a ~3× lever
arm on the SIM-071 headline over a 3e-4 spread in `h`, this is the highest-value cheap test
available to the program.

I confirmed the project's fit machinery is not at fault: applying its own `b = 12/5 + L⁻⁴` model to
the paper's 7-point table returns 1.5587180, within 4e-6 of the published value. The gap comes from
the shorter L range and from including the L = 8 point.

### 5.2 — Asymmetric anchor selection in SIM-070 (**MEDIUM**)

Full treatment in **L-08b**. SIM-070 used the **X** boundary preparation. Its `g_1` is compared
against PAPER-133's X-row value and matches at 0.16σ (`.results.g1.paper_value` records this).
Its `R_inf` is compared **only** against the exact BCFT value; against PAPER-133's own X-row value
(−1.62184 ± 0.00094) it is **3.87σ** away, while landing within 0.26σ of the paper's **Z** row.
The `R_inf` block carries no `paper_value` field. The paper's number is quoted where it agrees and
omitted where it does not.

### 5.3 — Two real cross-checks the project owns and does not claim

- **L-10:** puMPS N=12 vs ED N=12 agree to **5e-6 in `c`** once the KS phase convention is matched
  (`inv-pipelines.md` §3.4 measured the corrected ED value). Currently recorded in
  `pumps-setup/VENDOR.md:50` as a comparison against an *extrapolated* number, hiding a 7.2 %
  same-N gap. Additionally, the `Δ_T` row of that same table is already a matched-N agreement at
  **7e-5** (puMPS 1.960387 vs SIM-067's 1.960316) and is not identified as one.
- **L-05b vs L-05a:** the ED matrix-element route to `C_σσε` (0.49996) and the MERA PEV route
  (0.5069 at χ=8) are genuinely different measurements of the same constant, on different states,
  in different languages. Neither record cites the other.

### 5.4 — The one independent 3-point measurement in the program was retracted

`qw_cttt_circle.py:293` implements `C_TTT = √2·A₃/|A₂|^{3/2}` from equal-time connected
correlators — a route to `C_TTT` that does **not** pass through `c`.
`CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117` records its same-day falsification by ED (⟨hh⟩_conn
negative, decaying faster than s(x)⁴, exact free-fermion tail `−(16/π²)/(4x²−1)²`) and instructs
*"do not quote §3's A₂/A₃ formulas."* The retraction is correct and admirable. Its consequence for
this ledger is that **after it, every `C_TTT` number in the program is `c` in disguise** — and no
record states that the independent route was lost.

---

## 6. Which agreements are actually load-bearing evidence, and which are transformations of the same input?

Blunt, as requested.

### Load-bearing (four items, and only one of them is physics)

1. **The Yang-Lee `c_KS` SIGN.** (L-06s) The single genuinely unconstrained result in the program.
   Before the run, +2/5, −22/5 and noise were all live, and they carry different interpretations.
   It came back negative at every L, both chiralities, under all three defensible working points,
   with the vacuum's biorthogonal norm negative as corroboration, and reproduced through an
   independent code path. **Everything the project should be publishing rests on this one bit.**
   Caveat, and it is real: the state whose product's sign was measured is identified by M(2,5)
   theory, because the empirical discriminator inverts at Yang-Lee. It is a theory-conditioned bit.
2. **The `h_c(L)` reproduction of PAPER-133 Table S1** (L-08c) — 5 points at ≤6e-7 against
   published external data. Fully independent. Validates a bisection, not physics, but it is the
   only fully external anchor in the repo besides `g_1`.
3. **The `g_1` match at 0.16σ** (L-08a) — genuinely external, genuinely matched.
4. **puMPS ↔ ED at matched N** (L-10, and its Potts sibling L-11) — 5e-6 in `c`, 7e-5 in `Δ_T`,
   1.4e-6 in E₀/site, across two languages, two algorithms and two state constructions.
   **The project owns this and mis-states it.**

Add to those, as *methodological* rather than cross-check evidence and worth more than most of the
agreements: the L₋₂ε contamination suppression (~400×, exponent p ≈ 2.4 not 0.2,
`SIM-2026-068.json:32`); the Z₂/Z₃-symmetric optimisation converting a 2/8 basin lottery into 8/8;
the predictive use of two-error cancellation at N=40 D=28 (`SIM-2026-069.json:23`); and the Z₂
two-phase VQE result (L-18). None of these is fixed in advance by conformal symmetry, which makes
them the only Level-2 content in the corpus.

### Transformations of the same input

5. **`C_TTT` at all three classes.** (L-04) `C_TTT = 2√2/√c` is a literal line of code in every
   driver. Three rungs of a "self-coupling ladder" are three measurements of `c` re-expressed.
   And because the transform is nonlinear, extrapolating `c` and `C_TTT` separately from one
   dataset gives two answers 0.29 % apart — larger than the quoted deviation. The project's own
   design doc says this; the headlines do not.
6. **`α = 4` at TCI and Potts.** (L-03b) Every `alpha` field is exactly `2 × Delta_T` in the
   adjacent field; I checked the arithmetic pairwise in `SIM-2026-051.json`. **No force was
   measured at either class.** The "universality" claim compares a *force exponent* at Ising to
   *scaling dimensions* at TCI and Potts. That is not a cross-check; it is a category mismatch
   presented in one table column.
7. **`m_eff` 0.693 vs 0.670.** (L-02) Side A is `1/l_AdS`; side B is `l_AdS/ξ_2pt`. The claim is
   identically `ξ_2pt ≈ l_AdS²`, i.e. one two-point ratio from a state the same manuscript calls
   the wrong universality class, against a constant. One datum, presented as two agreeing
   quantities. Its own hypothesis record is `confidence: "low"` and its companion file contains a
   literal `NaN`.
8. **The Ising unitary control.** (L-07) 148 of 152 shared lines, and the differing line that
   matters sets `HC = 0.0`, turning the Hamiltonian real symmetric. Biorthogonal norms are exactly
   +1.000000 in the control; the claim depends on their being negative. It validates the KS
   estimator. It cannot defeat the interpretation, which is what §19 asks a control to be able to
   do.
9. **"Three consistent evaluations" of α = 3.92.** (L-13) One observable, one operator, one fit
   window, two sizes of one model plus a variational copy of one of them. All three move together
   under the dominant systematic (window choice: 3.92→2.56, 3.97→2.75, 4.07→2.75). Three numbers
   that move together under the thing that actually determines them are one number.
10. **`C_σσε` = 0.50.** (L-05a) Exact since BPZ 1984, and the quoted band is the χ=8 one because it
    brackets 0.5; the better-converged χ=12 rung is 5.6 % low with a 0.6 % spread.
11. **Transport `T` vs `(π/2)·l_AdS`.** (L-01) The most interesting borderline case. It is
    parameter-free, which is rare and real. But the time unit is set by an `L/(4π)` prefactor
    inside side A, the length unit by an architecture convention on side B, and the same record
    holds three candidate `l_AdS` values spanning −13.9 % to +0.7 % with the agreeing one named in
    a field called `best_agreement`. Report it as a parameter-free prediction *conditional on two
    unreconciled normalisation conventions*, not as a measurement of the AdS radius.
12. **`R_inf` at 0.01 %.** (L-08b) Requires selecting the last of a monotonically rising ratio
    sequence; the mean ratio gives 0.21 %. And it is measured against the exact value, not against
    the paper it claims to reproduce, from which it differs by 3.87σ.
13. **`T·L` conservation.** (L-15) Two coarse-grid points, one of which the project's own record
    marks `"EXCLUDED"` and *"clearly not the holographic transport signal."*

### The count

The program presents itself as having on the order of twenty independent confirmations. Stripping
the algebra, it has:

- **1** genuinely unconstrained physical bit (the Yang-Lee sign),
- **2** external anchors (`h_c(L)`, `g_1`), both reproductions of a published method,
- **3** genuine internal cross-implementation checks (puMPS↔ED Ising, puMPS↔ED Potts, this audit's
  Python↔Julia port), of which the project claims one and mis-states it,
- **~4** methodological results not fixed by symmetry (L₋₂ε suppression, symmetric-tensor basin
  cure, predictive error-cancellation, Z₂ two-phase VQE),
- **2** well-executed negatives (Route A closure, equal-time-correlator falsification),
- and **everything else is conformal symmetry, evaluated numerically.**

§7's closing line applies exactly: *"A beautiful agreement is not strong evidence if both sides are
transformations of the same input. Do not discard such agreements. Describe them correctly."*
The agreements are, with the exceptions above, correctly *computed*. They are not correctly
*described*.

---

## 7. UNVERIFIED

Stated explicitly rather than passed over.

1. **The shift in `c_KS` from adopting PAPER-133's published `h_c^∞` = 1.55872195.** I established
   the value exists, is external, is 185σ from the adopted one, and sits on the steepest lever arm
   in the program. I did **not** re-run Phase 2 at that `h` — it needs a non-Hermitian Arnoldi
   sweep, and extrapolating `inv-pipelines.md` §5.6's sensitivity curve to Δh = +9e-6 is nonlinear
   and unreliable. **The direction and size of the shift are unknown.**
2. **Whether SIM-070's `R_inf` disagreement with PAPER-133's X row (3.87σ) is a better estimator or
   a different construction.** Two readings given in L-08b; I could not discriminate them without
   re-implementing the paper's fit-window method.
3. **All P1/MERAKit per-seed numbers** (L-05a, L-09c, L-03b). `inv-pipelines.md` §2.3 established
   that every P1 SIM record cites `scratchpad *.log` artifacts that are **absent from the repo**,
   and the vendored `MERAKit.jl` clone has **no commit pin**. Every MERAKit figure in this ledger is
   quoted from SIM JSON prose and is unverified at the raw-data level. That includes C_σσε, the
   Potts χ-ladder, and every Δ_T feeding L-03b.
4. **The `L/(4π)` ↔ `1/ln χ` unit reconciliation** (L-01). I established that both are conventions
   and that neither is derived; I did **not** derive whether they are mutually consistent. This is
   the decisive open question for the transport claim and it is analytic, not numerical.
5. **The effect of the two sign-flipped MERA points on α = 4.07** (L-09a). I confirmed
   `.mera.V_data["9"]` and `["10"]` are positive inside a `sign: -1`, 10-point fit. I did not refit
   without them.
6. **Whether the `⟨ψ_L|ψ_R⟩` exponential decay at Yang-Lee is EP proximity or generic
   extensivity** (bears on whether L-06 scales to larger L). `inv-pipelines.md` §5.7 gives both
   readings and discriminates neither.
7. **Cross-state biorthogonality `⟨ψ_i^L|ψ_j^R⟩` for i ≠ j at Yang-Lee.** Mandated by
   `HYP028-BIORTHO-KS-DESIGN.md:36`, computed by nobody. If the low k=0/k=±2 states are not
   mutually biorthogonal, the product-form denominators in L-06 are ill-defined.
8. **Prior art for the biorthogonal-KS result.** Not searched here (out of scope). `SIM-2026-071.json`
   → `key_findings[1]` contains *"First lattice extraction (to our knowledge)…"*, a phrase §8
   prohibits without a recorded literature gate, and no such gate exists anywhere in the repo. **I
   make no novelty judgement either way**; I record that the gate has not been run.
9. **`ξ_2pt = 2.154` as a number.** I verified it is used as `l_AdS/ξ` to produce 0.6698 and that
   HYP-005 sources it to a `V(2)/V(1)` ratio. I did not recompute it from `SIM-2026-002.json`
   (1.7 MB) or from the gitignored `.npy` inputs.
10. **Whether L-10's corrected agreement holds beyond N = 12.** `inv-pipelines.md` §3.4 measured
    the half-bond ED at N = 10…16; the puMPS side has a single validated point (N = 12, D = 8), and
    `VENDOR.md:53-56` records that the N = 16 D = 12 run was externally killed twice. The
    cross-check is **one matched N**.

---

## 8. Recommendations, ranked by (evidence gained) / (effort)

1. **Re-run Yang-Lee Phase 2 at PAPER-133's published `h_c^∞` = 1.55872195** and report `c_KS`
   alongside the in-house value (§5.1, L-08d). ~1–2 h. Either the headline is externally pinned or
   the ±0.15 band is demonstrably wrong. **Highest-value cheap test in the program.**
2. **Fix `pumps-setup/VENDOR.md:50`**: replace the extrapolated-vs-raw row with the matched-N
   comparison, add the `Δ_T` 7e-5 row, and document the KS mode-discretization convention (L-10).
   ~1 h. Converts the repo's worst-stated comparison into its best-stated one.
3. **Add PAPER-133's X-row `R_inf` = −1.62184(94) to `SIM-2026-070.json`** beside the exact value,
   and state the 3.87σ (§5.2). ~10 min. Removes an asymmetric anchor.
4. **Relabel the `alpha` columns in `SIM-2026-051/052/062/063` and in the manuscript's universality
   table as derived** (`α ≡ 2Δ_T`), or measure a force at TCI/Potts (L-03c). The ED ground states
   and the force code both already exist; this is the cheapest route to a *real* universality test
   the program has.
5. **State in `SIM-2026-067/068/069` that `C_TTT` is computed as `2√2/√c`** and quote both
   extrapolations (4.00517 and 3.99361) rather than one (L-04). ~30 min.
6. **Solve `Hᵀw = Ew` directly for the left eigenvectors** instead of assuming `w = P v`, and
   confirm `c_KS` is unchanged (L-07 missing control iii). ~1 h. The single most informative
   missing test of the biorthogonal layer, and the only cheap thing that could actually defeat the
   interpretation.
7. **Re-run the Yang-Lee unitary control with output retained** — the program's most load-bearing
   validation currently exists as three hand-transcribed numbers with no artifact (L-07).
8. **Record the L-05a/L-05b and L-08c cross-checks in the SIM records** (§5.3). They are already
   true and already computed.
9. **Add a `derivation_dependency` field to every SIM record** naming the exact identities the
   result assumes, per §15. The map in §4 is the seed for it. This is the structural fix that would
   have prevented most of what is in this ledger.
