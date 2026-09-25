# ana:claim-map — Claim-Evidence Map (RESEARCH-DIRECTOR §6)

**Auditor:** `ana:claim-map` (phase-2 analysis agent)
**Date:** 2026-08-17
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` §5 (four contribution levels),
§6 (claim-evidence map + counterfactual novelty), §7 (independence ledger), §8 (novelty gates),
§12 (killer tests), §20 (uncertainty), §23/§24 (framing), §38.B (claim classification).

**Sources.** This map is built from the phase-1 investigation artifacts and re-anchored on the
primary records they cite:
`research/data/audit/raw/inv-manuscript-claims.md` (63 traced manuscript claims),
`inv-hypotheses.md` (30 hypothesis records), `inv-sims-early.md` (SIM-001…030 + named records),
`inv-sims-mid.md` (SIM-031…055), `inv-sims-late.md` (SIM-056…071), `inv-pipelines.md`
(five numerical pipelines), `inv-errata-history.md`, `inv-infrastructure.md`;
plus `README.md`, `research/submission-package/prd/paper-prd.tex`, `research/ERRATA.md`,
and the JSON records under `research/data/{simulations,hypotheses,papers,hardware}/`.

**Scope.** 42 claims (CLM-001 … CLM-042). Every claim the project asserts publicly (manuscript
abstract/body/conclusion, cover letter, README) or internally as a `verdict`/`key_finding` strong
enough to change a research decision. Purely internal bookkeeping is excluded.

---

## 0. How to read this map

Each record carries the 17 fields §6 requires, in fixed order:

| Field | Meaning |
|---|---|
| **Wording** | Exact quoted text from the artifact that makes the claim |
| **Math** | The mathematical statement, stripped of framing |
| **Level** | §5: **1** validation · **2** method · **3** new physics in framework · **4** discriminating |
| **HYP** | Originating hypothesis record |
| **SIMs** | Supporting simulations, exact repo-relative paths |
| **Analytic** | Supporting analytic derivation (or its absence) |
| **Lit** | External literature dependencies |
| **Assumptions** | What must hold for the claim to mean what it says |
| **Exact constraints** | Known exact values/identities that bound or fix the answer |
| **Uncertainty** | Sources of numerical uncertainty, stated and unstated |
| **Alternatives** | Conventional explanations not excluded |
| **Independence** | §7 class: fully independent / partially independent / structurally dependent / algebraically equivalent / consistency check |
| **Falsification** | What outcome would kill it |
| **Status** | Current standing, honestly stated |
| **Framing** | Publication framing that matches the evidence |
| **CF novelty** | §6: **near-zero** / **moderate** / **high**, with the counting argument |

**The §6 question, applied literally throughout:** *before running the calculation, how many
outcomes were genuinely possible?* Where conformal symmetry, a Virasoro identity, a BPZ result, or
an architecture definition fixed the answer in advance, the only possible outcomes were
"implementation worked" and "implementation failed", and the entry reads **near-zero**.

---

## 1. Summary tables

### 1.1 Distribution by contribution level (§5)

| Level | Count | Claims |
|---|---|---|
| **0** (framing / interpretation / priority — not a result) | 8 | CLM-007, 014, 018, 032, 039, 040(partly), 041, 042 |
| **1** (reproduction / validation) | 18 | CLM-001, 002, 003, 004, 005, 006, 008, 010, 011, 012, 013, 015, 016, 017, 019, 020, 023, 026, 033, 034, 036 (some dual-listed with L2) |
| **2** (methodological contribution) | 13 | CLM-009, 021, 022, 024, 025, 027, 028, 029, 030, 031(partly), 035, 037, 038 |
| **3** (new physics/math in framework) | **0 confirmed**; 2 candidates | CLM-027 (L₋₂ε suppression exponent), CLM-030 (negative-c sign) — both pending a §8 gate |
| **4** (discriminating foundational) | **0** | — |

**No Level-4 content exists anywhere in the program.** The two claims closest to Level 3 are
CLM-030 (the Yang-Lee sign, where the discriminating content is one bit, not the quoted magnitude)
and CLM-027 (the contamination-suppression exponent, the only genuinely unconstrained number in
the map). Neither has passed a literature gate, so neither can yet be called Level 3.

### 1.2 Distribution by counterfactual novelty (§6)

| CF novelty | Claims | Count |
|---|---|---|
| **near-zero** | 001, 002, 003, 004, 006, 008, 010, 011, 013, 015, 016, 017, 019, 020, 023, 024, 026, 031(magnitude), 033, 034, 036 | 21 |
| **moderate** | 005, 009, 012, 021, 022, 025, 029, 031, 037, 038 | 10 |
| **high** | **028** (would Route A extract spin-2 — answered NO), **030** (sign of c_KS), **035** (does the unitary identification rule survive non-unitarity — answered NO) | 3 |
| **moderate-to-high** | **027** (L₋₂ε suppression factor and exponent) | 1 |
| **n/a** (priority / framing, no calculation) | 007, 014, 018, 032, 039, 040, 041, 042 | 8 |

**Twenty-one of the thirty-four claims that involve a calculation could not have come out any other
way.** Only four could. That is the quantitative form of the project's own conclusion in
`docs/governance/PROJECT-REVIEW-2026-08-11.md` §4 — and note that **three of the four high-novelty
entries are negatives or method failures** (028, 035, and the sign half of 030), which per §42 is
where the program's real progress has been.

### 1.3 Claims whose stated status exceeds their evidence

| Claim | Stated | Defensible | Gap |
|---|---|---|---|
| CLM-001 | α = 3.92 ± 0.16 | α ≈ 2.5–4.0, window-dependent | fit-window systematic ≈ 8σ, unquantified |
| CLM-002 | "independently confirmed" | consistency check | shares state, observable, code, window |
| CLM-004 | "the exponent is universal" | Δ_T ≈ 2 at three classes | no force measured at 2 of 3 |
| CLM-007 | "first … from an optimized tensor network" | first in this codebase | §8 gate never run |
| CLM-014 | "Wang & He analytically proved t_trans = π" | not in the project's record of that paper | only external-validation claim in the paper |
| CLM-023 | C_σσε = 0.50 ± 0.03 | 0.493 ± 0.021 per the record's own prescription | χ-drift away from 0.5 undisclosed |
| CLM-026 | "C_TTT ladder complete" | central-charge ladder complete | algebraically equivalent, one number not two |
| CLM-030 | "measures the TRUE central charge, −4.29 ± 0.15" | sign robust; magnitude spans [−7.0, −3.7] | 82 % extrapolation; h-model systematic excluded from the band |
| CLM-032 | "First lattice extraction (to our knowledge)" | unknown | §8-prohibited phrase, no search recorded |
| CLM-039 | "3.33 % ceiling regardless of optimizer" | 5 seeds of one optimizer family | repeats the exact inference ERRATA D5 retracted |
| CLM-040 | "hardware path designed for Helios" | one compiled circuit | project's own `PARTIALLY_REFUTED` feasibility verdict omitted |
| CLM-041 | README: "quantitative gravitational content" | Level-1/2 CFT data | no matched non-geometric control has ever been built |
| CLM-042 | README: "may be the first open-source … AI agent team" | unknown | §8 violation; competing prior art sits uncited in the project's own `.bib` |

### 1.4 Claims that are stronger than the project presents them

Overclaiming is not the only failure mode. Four items are **understated**:

| Claim | Understatement |
|---|---|
| CLM-030 | The sign result needs no extrapolation and survives every h_c^∞ variant. It is buried inside a magnitude claim that does not. |
| CLM-037 | Normalization-invariance of the c_KS estimator is provable in two lines and defuses the §12 Yang-Lee killer. It is claimed nowhere. |
| CLM-026 | The ED-vs-puMPS cross-check is a 5e−6 agreement once the Koo–Saleur mode convention is matched; the project records it as a 7 % disagreement papered over with an extrapolated number. |
| CLM-028 | A clean methodological negative (Route A fails) is recorded and then made invisible by Route B's silent substitution of a different observable. |

---

## 2. Claim records

### Cluster A — The force exponent α = 4 (CLM-001 … CLM-009)

---

#### CLM-001 — The 24-qubit force exponent

- **Wording:** *"α = 3.92 ± 0.16 (24 qubits)"* (`research/submission-package/prd/paper-prd.tex` Abstract L29, §5.3 L319). Called *"the central finding of this work"* (§8.1 L523).
- **Math:** F(dr) = E_dual(dr) − E₀ − 2·δE_single, fitted to A·dr^(−α) over dr ∈ [2,12] on the exact 24-qubit critical-TFIM ground state.
- **Level:** 1 (validation of a symmetry-fixed exponent).
- **HYP:** `research/data/hypotheses/HYP-2026-008.json` (`status` SUPPORTED, `confidence` medium).
- **SIMs:** `research/data/simulations/SIM-2026-011-interaction.json` `.fits.F_avg_dr_ge2.power_law` (alpha 3.921759726, dalpha 0.158982157, A −8.672711550); statistics in `research/data/simulations/SIM-2026-017-statistics.json`.
- **Analytic:** α = 2Δ_T with Δ_T = 2 — the conformal Ward identity. No derivation of the lattice observable's asymptotics exists; `paper-prd.tex` §5.3 L329 concedes the spin-2 identification *"rests on the exponent matching and requires further theoretical justification"*.
- **Lit:** `DiFrancesco1997` (Δ_T = 2); `PAPER-2026-010.json` for the boundary-primary operator coefficients (0.635/−0.026) — which the manuscript misattributes to `ZouMilstedVidal2020` (`inv-manuscript-claims.md` DEF-13).
- **Assumptions:** (i) the excitation σ_j creates the ε primary and not a mixture — never verified numerically; (ii) dr ≥ 2 is the correct fit window; (iii) the anchor-6 subtraction removes OBC contamination; (iv) `curve_fit` covariance is a calibrated 1σ.
- **Exact constraints:** Δ_T = 2 in every unitary 2D CFT ⇒ α = 4 exactly. `SIM-2026-014.json` `key_finding` states this itself.
- **Uncertainty:** quoted ±0.16 is a covariance 1σ on a fit whose own `chi2_reduced` = **6.008** (`SIM-2026-017-statistics.json` `.power_law_fit.statistics.chi2_reduced`), i.e. formally rejected. The same record's 1000-resample bootstrap gives `alpha_mean` **3.369**, `alpha_std` **0.6335**, CI [2.520, 4.192]. **Unquantified and dominant:** the fit-window systematic — refitting at dr ≥ 3 gives α = 2.559 ± 0.019 (`inv-sims-early.md` §3.2), a shift of ~1.4 ≈ 8× the quoted σ.
- **Alternatives:** the recorded F(dr) has **no power-law plateau** — local log-slopes are 2.04, **4.23**, 2.60, 2.46, 2.46, 2.53, 2.66, 2.84, 3.10, 3.48, 4.06 (`inv-sims-early.md` §3.1, recomputed from `.F_interaction_avg`). A crossover/contact term at dr = 1–2 plus OBC drift at the chain ends reproduces this pattern without any dr⁻⁴ asymptotics. Not excluded.
- **Independence:** single dataset. See CLM-002 for the "three evaluations".
- **Falsification:** a fit-window scan showing no plateau (this has now effectively occurred); or a longer chain where the mid-range local slope stays near 2.5.
- **Status:** **WEAKENED by this audit.** The number is correctly transcribed from its record; the record's precision claim is not supportable. ERRATA carries no entry for this.
- **Framing:** "an attractive, monotonically decaying interaction energy consistent with, but not resolving, dr⁻⁴ asymptotics at 24 sites". Not a central finding.
- **CF novelty:** **near-zero.** Δ_T = 2 is fixed by Virasoro in advance; only implementation success/failure was possible on the theory side. The one genuinely open question — whether the lattice observable exhibits the asymptotics — is **not answered** by this record (no plateau).

---

#### CLM-002 — "Independently confirmed" at N = 16, two ways

- **Wording:** *"This exponent is independently confirmed at N = 16 (α = 3.97 ± 0.15 from exact diagonalization, α = 4.07 ± 0.18 from χ = 3 MERA optimization)"* (`paper-prd.tex` §5.3 L327); Abstract: *"three consistent evaluations"*.
- **Math:** same F(dr) fit on (a) the exact 16q ground state, (b) a χ=3 MERA approximation of that same state (0.151 % energy error).
- **Level:** 1.
- **HYP:** HYP-2026-008, HYP-2026-009.
- **SIMs:** `SIM-2026-015d.json` `.exact.alpha` 3.9748194 / `.dalpha` 0.14510; `.mera.alpha` 4.0711570 / `.dalpha` 0.17775; `SIM-2026-015c.json` `.best_error_pct` 0.15126.
- **Analytic:** none beyond CLM-001.
- **Lit:** as CLM-001.
- **Assumptions:** that agreement between an exact state and a variational approximation *of that same state* constitutes independent evidence.
- **Exact constraints:** as CLM-001.
- **Uncertainty:** same covariance-1σ method, same undisclosed window systematic — dr ≥ 3 gives 2.753 (exact) and 2.745 (MERA) (`inv-sims-early.md` §3.2), **the same direction in all three datasets**. The χ=3 fit additionally includes **two positive V values** (dr = 9: +0.0012015, dr = 10: +0.00036517) inside a 10-point fit to a strictly negative power law (`SIM-2026-015d.json` `.mera.V_data`), unflagged.
- **Alternatives:** the three numbers agreeing is expected under *any* systematic shared by the pipeline, including the one identified in CLM-001.
- **Independence:** **STRUCTURALLY DEPENDENT / consistency check.** Shared: Hamiltonian family, observable Eq.(6), σ_j operator and its coefficients, fit model, fit window, fit code; the two N=16 numbers share the ground state itself (`inv-sims-early.md` §3.6 ledger). §7 forbids calling this independent. The manuscript's own §6.5 L427 states the correct version — *"all sample the same conformal fixed point"* — so both framings coexist in one paper (`inv-manuscript-claims.md` DEF-24).
- **Falsification:** an evaluation on a genuinely different CFT class, a different observable, or an independent code path disagreeing.
- **Status:** **MISLABELLED.** The measurements are fine; "independently" is wrong.
- **Framing:** "reproduced at a second system size and under variational approximation".
- **CF novelty:** **near-zero.**

---

#### CLM-003 — Exclusion of scalar exchange

- **Wording:** *"all consistent with stress-tensor exchange (α = 4, Δ_T = 2) and inconsistent with scalar exchange (α = 2)"* (Abstract L29; §8.1 item 2 L527).
- **Math:** α = 2Δ_ε = 2 excluded at the quoted uncertainty.
- **Level:** 1.
- **HYP:** HYP-2026-008.
- **SIMs:** `SIM-2026-011-interaction.json`; `SIM-2026-017-statistics.json` `.bootstrap`.
- **Analytic:** Δ_ε = 1 for Ising ⇒ scalar-channel α = 2 (textbook).
- **Lit:** `DiFrancesco1997`.
- **Assumptions:** ±0.16 is the right error bar.
- **Exact constraints:** both candidate exponents (2 and 4) are exactly fixed by the CFT; the experiment is a two-way discrimination between two known numbers.
- **Uncertainty:** decisive. At ±0.16 the exclusion is ~12σ; at the project's own bootstrap σ = 0.633 it is **~2.2σ**, and the bootstrap CI floor is 2.520 — i.e. α = 2 sits just outside a 95 % CI whose lower edge the manuscript quotes without quoting the σ or the mean (3.369). Under the dr ≥ 3 window the point estimate **is** ≈ 2.56.
- **Alternatives:** the mid-range local slope of the raw data is 2.45–2.66, which is closer to the scalar value than to 4.
- **Independence:** none; same data as CLM-001.
- **Falsification:** already effectively falsified at the stated confidence by the window analysis.
- **Status:** **NOT SUPPORTED at the claimed significance.** This is the audit's most consequential physics finding.
- **Framing:** "the data do not currently discriminate stress-tensor from scalar exchange at 24 sites".
- **CF novelty:** **near-zero** on the theory side (two known candidates); **moderate** as an empirical discrimination — which is exactly why the failed discrimination matters.

---

#### CLM-004 — Universality of α = 4 across three CFT classes

- **Wording:** *"The recurrence of α = 4 at two additional, independent universality classes … establishes that the holographic force exponent reflects stress-tensor exchange rather than any property specific to the Ising model. The exponent is universal."* (`paper-prd.tex` §6.5 L457); README L11 *"the force exponent is alpha = 2*Delta_T = 4, and it does not depend on what the material is made of"*.
- **Math:** Δ_T measured at Ising c=1/2, tricritical Ising c=7/10, 3-state Potts c=4/5; α ≡ 2Δ_T applied.
- **Level:** 1.
- **HYP:** HYP-2026-025 (`status` SUPPORTED), HYP-2026-027 (`status` field contains `"TESTABLE_NEAR_TERM"` — a feasibility value, not a status; `inv-hypotheses.md` §0.4).
- **SIMs:** `SIM-2026-051.json` (χ=6 TCI, Δ_T 2.0065), `SIM-2026-052.json` (χ=8 TCI, Δ_T 1.9994), `SIM-2026-062.json`, `SIM-2026-063.json` (Potts χ=12, Δ_T 2.0004/2.0023), `SIM-2026-050.json` (plain Ising, Δ_T 1.998).
- **Analytic:** α = 2Δ_T — the same identity that motivated the test.
- **Lit:** O'Brien–Fendley for the λ₃ = 0.856 TCI point; standard M(4,5)/Potts CFT data.
- **Assumptions:** that measuring Δ_T at a class licenses asserting the force exponent there.
- **Exact constraints:** **Δ_T = 2 in every unitary 2D CFT.** This is a theorem, not a prediction.
- **Uncertainty:** no uncertainty is attached to α in any of the four records (`inv-sims-mid.md` DEFECT on SIM-051/052). SIM-051's 8-seed Δ_T range is [1.9219, 2.1889] (±5 %) while the selected basin is quoted to 4 s.f. SIM-051's recorded `all_8_seeds_mean` 1.9913 is **wrong** — the true mean of its own eight listed values is 2.0163. Potts χ=12 rests on **2 of 6** basins, selection rate undisclosed in the manuscript (`inv-manuscript-claims.md` DEF-10).
- **Alternatives:** none needed — the result was guaranteed by symmetry given a converged fixed point. The *interesting* content is the class identification (Δ_ε = 0.204 at TCI, Δ_σ ≈ 0.133 at Potts), not α.
- **Independence:** the α column is **ALGEBRAICALLY EQUIVALENT** to the Δ_T column. Across classes the measurements are structurally dependent (same MERAKit pipeline, same blocking convention, same basin-selection rule).
- **Falsification:** cannot fire. A Δ_T ≠ 2 result at a unitary CFT would indicate a bug, not new physics. HYP-2026-030's sole criterion has exactly this defect (`inv-hypotheses.md` §2b).
- **Status:** **SUPPORTED as a statement about Δ_T; NOT ESTABLISHED as a statement about the force.** No force was measured at TCI or Potts. The manuscript's own §8.7 item 4 concedes this; the table, the Abstract, the cover letter and the README do not.
- **Framing:** "MERA reaches CFT fixed points at three classes and recovers Δ_T = 2 at each" — a pipeline-credibility result.
- **CF novelty:** **near-zero.** Before the run, the possible outcomes were: converged fixed point ⇒ Δ_T ≈ 2, or non-converged ⇒ garbage. The pass-gate for each SIM *is* "Δ_T ≈ 2", so passing the gate makes the reported result deterministic (`inv-hypotheses.md` §0.5).

---

#### CLM-005 — Power law preferred over exponential

- **Wording:** *"ΔAIC = 11.0 (Burnham–Anderson strong preference), with the exponential RSS 2.7× larger"* (`paper-prd.tex` §5.3 L323).
- **Math:** AIC comparison of A·dr^(−α) vs B·exp(−dr/ξ) on the same 11 points.
- **Level:** 1.
- **HYP:** HYP-2026-002, HYP-2026-011.
- **SIMs:** `SIM-2026-017-statistics.json` `.model_comparison.delta_AIC_exp_minus_pl` = 11.024477; RSS ratio 0.001931527/0.000708990 = 2.724.
- **Analytic:** none.
- **Lit:** Burnham–Anderson (uncited in `references.bib`).
- **Assumptions:** RSS-based Gaussian AIC over a fixed window.
- **Exact constraints:** none.
- **Uncertainty:** the two summary statistics in the record use **different error models** — χ² uses supplied per-point errors (54.07 / 1.01e9), AIC/BIC are RSS-based (`inv-sims-early.md` §3.4). Both papers quote only the favourable ΔAIC and no χ² anywhere (verified by grep in `inv-sims-early.md`). The comparison inherits CLM-001's window dependence entirely.
- **Alternatives:** on the dr ≥ 3 window neither model is a good description; the exponential's poor showing is driven by the same dr = 1–2 region that drives α.
- **Independence:** same data, same window, same code as CLM-001 — a re-analysis, not a check.
- **Falsification:** window variation flipping the preference.
- **Status:** **SUPPORTED as an in-window model comparison; the disclosure is selective.** `SIM-2026-017-statistics.json` is cited nowhere in the manuscript and is absent from Appendix E (`inv-manuscript-claims.md` DEF-23).
- **Framing:** "over the fitted window, a power law describes the data better than an exponential".
- **CF novelty:** **moderate.** Sahay–Lukin–Cotler report an exponential, so the outcome was not preordained — but the two are different observables (bulk-to-bulk vs boundary-to-boundary), which the manuscript itself says in §7.4.

---

#### CLM-006 — Anchor-independence robustness

- **Wording:** *"The measured α varies by only 0.027 across anchors (3.93, 3.92, 3.92, 3.95) — less than one-sixth of the statistical uncertainty — confirming that OBC contamination is subdominant."* (`paper-prd.tex` §5.3 L325).
- **Math:** repeat the extraction at anchor ∈ {4, 6, 8, 12}.
- **Level:** 1.
- **HYP:** HYP-2026-008.
- **SIMs:** `SIM-2026-017-statistics.json` `.anchor_dependence.results` (3.930905, 3.921760, 3.922707, 3.948511), `.consistency.alpha_spread` 0.026751, `.spread_over_sigma` 0.166841.
- **Analytic:** none.
- **Lit:** none.
- **Assumptions:** that anchor position is the dominant systematic.
- **Exact constraints:** none.
- **Uncertainty:** the check is **structurally incapable of firing.** All four anchors use `dr_values` starting at 2, and the anchor-4/6/8 `F_values` agree with each other to ~12 significant figures (anchor 4 dr=12: −0.0022218714808914797 vs anchor 6: −0.0022218714807848983) (`inv-sims-early.md` §3.3). The anchor-12 variant silently uses 9 points, not 11.
- **Alternatives:** —
- **Independence:** none — four re-fits of near-identical arrays.
- **Falsification:** —
- **Status:** **VOID as a control.** §19: "a serious control should be capable of defeating the preferred interpretation". This one varies a parameter the observable is nearly invariant under while holding fixed the choice that determines the answer.
- **Framing:** delete, or replace with a fit-window scan.
- **CF novelty:** **near-zero** (a control that cannot fail has zero counterfactual content by definition).

---

#### CLM-007 — Priority: first force measurement from an optimized tensor network

- **Wording:** *"enabling the first holographic force measurement from an optimized tensor network state"* (Abstract L29, §6.4 L420, §9 L609, cover letter).
- **Math:** —
- **Level:** 2 at most (a codebase-scoped capability claim).
- **HYP:** HYP-2026-009.
- **SIMs:** `SIM-2026-015c.json`, `SIM-2026-015d.json`.
- **Analytic:** —
- **Lit:** **none recorded.** In tension with the manuscript's own §7.4, which credits Sahay et al. with demonstrating hologron forces in classical MERA simulation.
- **Assumptions:** that "optimized (variational)" vs "analytic Evenbly–White" is a distinction the literature has not already crossed — never stated in the manuscript, never searched.
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** Anand et al. (`PAPER-2026-017.json`) ran MERA on trapped-ion hardware in 2022; ZMV and successors optimize MERA routinely.
- **Independence:** —
- **Falsification:** one prior paper measuring an interaction energy from a variationally optimized MERA.
- **Status:** **§8 VIOLATION.** No literature gate exists. Four more claims of this shape are in the same manuscript: "a dynamical test … has not been performed at sub-percent precision" (§1), ALM "have not been applied to quantum variational circuits with discrete symmetry constraints" (§2.2), "introduces holographic transport as a novel observable" (§7.2, self-contradicted by §7.4), "the first N = 24 measurement" (§7.4) (`inv-manuscript-claims.md` DEF-15).
- **Framing:** delete until §8's literature/derivation/prior-art gates are recorded.
- **CF novelty:** not applicable — this is a priority assertion, not a measurement.

---

#### CLM-008 — The mediating operator is the stress tensor (spin-2 / graviton analogue)

- **Wording:** *"the ADM Hamiltonian in superspace produces virtual graviton exchange between boundary-localized excitations, with the graviton propagator decaying as 1/dr^{2Δ_T} = 1/dr⁴"* (§5.3 L329); Conclusion: *"evidence for stress-tensor-mediated holographic forces in a tensor network"*.
- **Math:** identification of the exchanged operator from the fitted exponent alone.
- **Level:** 1 (the exponent) dressed as Level 3 (the identification).
- **HYP:** HYP-2026-008 — whose own `experimental_evidence.operator_caveat` reads verbatim *"Excitation used was Zou-Milsted-Vidal epsilon boundary primary (not the stress tensor T_mu_nu directly) … does not constitute direct proof that the stress tensor is the mediating operator"* (`inv-hypotheses.md` §2a).
- **SIMs:** `SIM-2026-011-interaction.json`, `SIM-2026-015d.json`.
- **Analytic:** §8.5's fusion argument (ε × ε = [1], C_εεT = 2Δ_ε/c = 4) is textbook and shows only which channel *can* contribute.
- **Lit:** `PAPER-2026-023.json` (Roux) — but no recorded Roux result gives a 1/dr⁴ boundary falloff; the exponent is the manuscript's own CFT identity presented as a framework prediction (`inv-manuscript-claims.md` F-14).
- **Assumptions:** that σ_j creates a clean ε excitation. The only spectral evidence offered is x₁ = 0.485 assigned to Δ = 1 — a **51.5 % discrepancy** called "consistent … shifted by open-boundary effects" with no OBC calculation (CLM-017).
- **Exact constraints:** α = 2Δ = 4 for spin-2, = 2 for the scalar channel.
- **Uncertainty:** inherits CLM-001 and CLM-003 in full.
- **Alternatives:** a mixture of channels; a contact/crossover term; the OBC drift of §3.1. None excluded.
- **Independence:** the "prediction" and the "measurement" are the same identity evaluated on a state built to realize that CFT — **structurally dependent**.
- **Falsification:** a direct spin-resolved measurement of the exchanged operator; a spectral decomposition of the excited state.
- **Status:** **NOT ESTABLISHED.** The manuscript's §5.3 concedes it ("requires further theoretical justification"), then §8.5 claims it "resolves the open question from Sec. V.C" — an internal contradiction (`inv-manuscript-claims.md` DEF-25).
- **Framing:** "the exponent is consistent with, but does not identify, stress-tensor exchange".
- **CF novelty:** **near-zero.**

---

#### CLM-009 — Reconciliation with the Sahay–Lukin–Cotler exponential

- **Wording:** *"previous work observed exponential force profiles … We show that this was an artifact of the observable, not the physics."* (§8.1 item 3 L529). Four paragraphs later: *"these are not contradictory … Sahay et al. measure the bulk-to-bulk propagator while we measure the boundary-to-boundary correlator"* (§7.4 L552).
- **Math:** the ZZ-correlator observable V(dr) degenerates to −C_vac when boundary-primary excitations destroy the correlator structure (C_two ≈ 10⁻⁴).
- **Level:** 2 (the observable-failure finding is a real methodological contribution).
- **HYP:** HYP-2026-002, HYP-2026-011.
- **SIMs:** `SIM-2026-010.json`, `SIM-2026-005.json` `.force_profile`, `SIM-2026-006.json` `.force_profile[*].C_vac`.
- **Analytic:** the Poisson-kernel relation asserted in §7.4 is **computed nowhere** in the manuscript or the repository (`inv-manuscript-claims.md` D8-5).
- **Lit:** `PAPER-2026-009.json` `.key_claims[3]` (V ~ C1 − C2·exp(−|ρ1−ρ2|/l_AdS); the manuscript drops the C1 offset).
- **Assumptions:** that the two observables are the two projections claimed.
- **Exact constraints:** none.
- **Uncertainty:** C_two ≈ 10⁻⁴ has no record in the cited SIM (`inv-manuscript-claims.md` F-17).
- **Alternatives:** the two profiles may simply be measuring different physics with no common holographic parent — the Poisson-kernel bridge is unproven.
- **Independence:** —
- **Falsification:** an explicit Poisson-kernel computation failing to map one profile onto the other.
- **Status:** **The negative result (the ZZ observable fails) is solid and valuable. The "artifact of the observable" verdict contradicts the paper's own §7.4** and should be withdrawn.
- **Framing:** Level-2 methods note: "the ZZ-correlator observable is unusable for this measurement; here is the diagnostic and the replacement".
- **CF novelty:** **moderate** for the observable failure (it was discovered, not predicted); **near-zero** for the reconciliation, which is asserted.

---

### Cluster B — Holographic transport and emergent geometry (CLM-010 … CLM-015)

---

#### CLM-010 — Transport time matches the AdS₃ null geodesic

- **Wording:** *"the holographic transport time matches the AdS₃ null geodesic prediction T = (π/2)·l_AdS to 1.2 % at N = 16"* (Abstract L29; §3.3).
- **Math:** T_pred = (π/2)/ln 2 = 2.2661800709; T_meas(dt=1e−3) = 2.23888; residual −1.205 %.
- **Level:** 1.
- **HYP:** `HYP-2026-006.json` (`status` SUPPORTED, `confidence` high).
- **SIMs:** `SIM-2026-025.json` `.runs.N16.T_measured_refined` 2.23888, `.residual_pct_refined` −1.205, `.physical_parameters.T_null_pred` 2.2661800709135966; original coarse run in `research/data/simulations/holographic_transport.json` (which carries **no `id`, no `date`, no `verdict`** — `inv-sims-early.md` §4.1).
- **Analytic:** `composite_geodesic_results.json` `.calculations.embedding_space`: ⟨P₁,P₂⟩ = −cos(Δt) − 1; null condition ⇒ T = π/2. **A two-line trigonometric identity following from a convention choice**, not a derivation with content.
- **Lit:** `PAPER-2026-010.json` (Wang–He boundary Hamiltonian); `KimSwingle2017` / `PAPER-2026-009.json` for l_AdS = 1/ln χ.
- **Assumptions:** (i) l_AdS = 1/ln χ (architecture definition, CLM-015); (ii) the null rather than spacelike geodesic is the right comparison — the manuscript rejects T = π·l_AdS = 4.53 on this basis; (iii) the dip/reappearance timestamps identify a single propagating excitation.
- **Exact constraints:** π/2 and 1/ln 2 are both exact inputs. The predicted number is **fixed before any simulation**.
- **Uncertainty:** grid quantization was the dominant systematic and was found and corrected by the project itself (ERRATA E2: the published 0.72 % was a dt = 0.05 artifact; converged value −1.205 %). No error bar is quoted on the converged residual. The N = 24 companion gives **−31.6 %** and is excluded for a documented reason (double-lobe structure, `SIM-2026-025.json` `.runs.N24.exclusion_reason` — *"clearly not the holographic transport signal"*).
- **Alternatives:** **not excluded and undisclosed** — the same record's Approach A (Wang–He H with mass detuning δ = −0.3…+0.3) gives transport times 2.00, 1.95, 1.70, **2.25**, 3.30, 2.10, 0.55, i.e. residuals −75.7 % to +45.6 % (`hyp010_criticality_scan.json` `.approach_A_wang_he_detuning`). A one-parameter detuning of the *same* Hamiltonian moves T across a factor of 6. The manuscript shows only the Approach-B (different-Hamiltonian) control (`inv-manuscript-claims.md` DEF-19).
- **Independence:** **STRUCTURALLY DEPENDENT.** T and l_AdS both descend from the same MERA/CFT calibration; the "prediction" side contains no information the construction did not put in. `HYP-2026-006.json` does not say so.
- **Falsification:** the record's own named killer ("no systematic dependence on boundary separation, or linear rather than arccosh") was **never executed** (`inv-hypotheses.md` §2b). A live killer would be: the detuning scan above.
- **Status:** **SUPPORTED as a single-point numerical agreement; the geometric interpretation is not tested.** ERRATA E2 was applied correctly and in-text — the project's best instance of self-correction. But the retracted 0.72 % still stands **unmarked in `HYP-2026-006.json` `experimental_evidence`** (`inv-errata-history.md`).
- **Framing:** "an excitation revival time in the Wang–He boundary Hamiltonian lands within 1.2 % of a convention-fixed constant at N = 16".
- **CF novelty:** **near-zero.** The predicted value is an exact identity; the only outcomes were "lands near it" or "doesn't". The detuning scan shows the landing is not robust.

---

#### CLM-011 — The residual shrinks with system size

- **Wording:** *"residual shrinking from 2.8 % at N = 12"* (Abstract L29); README: *"converging as 1/N"*.
- **Math:** −2.777 % at N = 12 → −1.205 % at N = 16.
- **Level:** 1.
- **HYP:** HYP-2026-006, HYP-2026-010, HYP-2026-023.
- **SIMs:** `SIM-2026-025.json` `.runs.N12.residual_pct_refined`, `.runs.N16.residual_pct_refined`.
- **Analytic:** none.
- **Lit:** none.
- **Assumptions:** two points define a trend.
- **Exact constraints:** none.
- **Uncertainty:** the record itself says the fit is degenerate: `.fit_1overN.note` — *"algebraically exact but degenerate — cannot distinguish 1/N from 1/N² without N = 24"*, with a non-zero intercept b = +0.0796 "indicates mixed functional form, not clean 1/N scaling". Undisclosed in the manuscript and contradicted by README's flat assertion "converging as 1/N". The N = 24 point that would break the degeneracy exists and is **excluded** (CLM-010).
- **Alternatives:** any two-parameter family fits two points exactly.
- **Independence:** same pipeline, two sizes — consistency check.
- **Falsification:** N = 24 (or a corrected N = 24) landing off the extrapolation. `holographic_transport_24q.json` `.lin_finite_size.lin_1N_consistent` = **"INCONSISTENT"** — the record's own finite-size verdict is negative and unmentioned anywhere downstream.
- **Status:** **NOT ESTABLISHED.** A two-point trend whose own record calls it degenerate, with the third point excluded and the third point's own verdict negative.
- **Framing:** "the residual is smaller at N = 16 than at N = 12; the functional form is undetermined".
- **CF novelty:** **near-zero.**

---

#### CLM-012 — The MERA value is uniquely consistent with AdS (the TFIM control)

- **Wording:** *"the TFIM ring yields T_TFIM = 3.8 — 69 % larger than the MERA result"*; *"The MERA transport time T = 2.25 is uniquely consistent with the AdS null geodesic formula"* (§3.4 L179–181).
- **Math:** control comparison against a plain critical TFIM ring and a 7-point coupling scan g ∈ [0.75, 1.10].
- **Level:** candidate 3 (a control that could have discriminated), delivered as 1.
- **HYP:** HYP-2026-006, HYP-2026-010.
- **SIMs:** `hyp010_criticality_scan.json` `.approach_B_tfim.results` (T = 5.2, 5.1, 5.0, 4.0, 3.8, 3.55, 3.45 for g = 0.75 → 1.10).
- **Analytic:** none.
- **Lit:** none.
- **Assumptions:** that a different Hamiltonian giving a different T is evidence for the geometric interpretation.
- **Exact constraints:** none.
- **Uncertainty:** —
- **Alternatives:** **the record refutes the manuscript's own reading.** The manuscript calls the seven transport times *"a non-systematic pattern"*; they are **strictly monotonically decreasing in g** (`inv-manuscript-claims.md` DEF-02). T is therefore a smooth function of the coupling, and hitting 2.266 is a question of where a smooth curve lands — which the Approach-A detuning scan (CLM-010) independently demonstrates within the *same* Hamiltonian family.
- **Independence:** **PARTIALLY INDEPENDENT** — a genuinely different Hamiltonian. This is the right kind of control; it is the *reading* that fails.
- **Falsification:** already: monotone dependence on a tuning parameter, plus a factor-6 swing under detuning.
- **Status:** **CONTRADICTED BY ITS OWN RECORD.** "Uniquely consistent" is not supportable.
- **Framing:** "the revival time depends smoothly and monotonically on the chain coupling; the MERA-derived Hamiltonian sits at one point of that curve".
- **CF novelty:** **moderate** as designed (a real control), **near-zero** as delivered (the adverse half was not reported).

---

#### CLM-013 — T·L is approximately conserved

- **Wording:** *"the product T·L is approximately conserved"*: N=16 → 36.0, N=24 → 37.2, *"3.3 % consistency"*; explicitly hedged — *"an empirical observation, not a derived result. We do not claim a theoretical derivation."* (§3.5 L206).
- **Math:** 2.25 × 16 = 36.0; 1.55 × 24 = 37.2.
- **Level:** 1 (arithmetic on two numbers).
- **HYP:** HYP-2026-006.
- **SIMs:** `holographic_transport.json` `.transport_signature.transport_time` 2.25; `holographic_transport_24q.json` `.transport_signature.transport_time_measured` 1.55.
- **Analytic:** none, and the manuscript says so.
- **Lit:** none.
- **Assumptions:** that the N=24 transport time is meaningful.
- **Exact constraints:** none.
- **Uncertainty:** the N = 24 input is the one the project itself **excludes** (`SIM-2026-025.json` `.runs.N24.exclusion_reason`: two overlapping lobes, "clearly not the holographic transport signal"). The table also silently mixes the coarse-grid T = 2.250 with the headline's converged 2.239. Symbol `L` collides with the MERA-layer `L` of §2.1 (`inv-manuscript-claims.md` DEF-11).
- **Alternatives:** two numbers agreeing to 3 % is unremarkable.
- **Independence:** —
- **Falsification:** a third size.
- **Status:** **PROVISIONAL and correctly labelled as such** — the manuscript's hedging here is exemplary and should be preserved. But it is built on an excluded datum.
- **Framing:** keep the hedge; add that the N=24 input is excluded elsewhere in the same paper.
- **CF novelty:** **near-zero.**

---

#### CLM-014 — External analytic validation by Wang & He

- **Wording:** *"Wang and He recently proved the null geodesic formula t_trans = π analytically in the continuum limit, confirming that the N = 16 result agrees with the correct theoretical prediction"* (§3.5 L206; repeated §7.2 L538 and Conclusion item 2 L605).
- **Math:** t_trans = π asserted as an independently proved continuum result.
- **Level:** 0 (an attribution, not a result) — but load-bearing: **this is the manuscript's only claim of third-party confirmation.**
- **HYP:** HYP-2026-006.
- **SIMs:** —
- **Analytic:** —
- **Lit:** `references.bib` `WangHe2026` = arXiv 2603.07639. The project's own canonical record `research/data/papers/PAPER-2026-088.json` (alias `PAPER-2026-039.json`) titles it *"Black-Hole Signatures in the Finite-Temperature Critical Ising Chain"*; its abstract and six `key_claims` contain **no analytic proof and no t_trans = π**. The nearest recorded statement is the project's own annotation that the (π/2)·l_AdS relation is *"consistent with"* the BTZ picture.
- **Assumptions:** —
- **Exact constraints:** the manuscript's §3.3 **rejects** T = π·l_AdS = 4.53 as the wrong (spacelike) formula, then cites "t_trans = π" as confirming T = (π/2)·l_AdS, with no unit or convention reconciliation. §7.2 further garbles the attribution across two bib keys.
- **Uncertainty:** —
- **Alternatives:** transcription/attribution error; a convention in which the two agree (unstated).
- **Independence:** if true, this would be the program's **only fully independent** external check. As recorded, it is unsupported.
- **Falsification:** reading arXiv 2603.07639.
- **Status:** **NOT SUPPORTED by the project's own record of the cited paper.** Not proved false — the paper itself was not read (see UNVERIFIED). **Highest-value item in the entire audit to close**, because a referee who knows this paper will check it first.
- **Framing:** remove or restate as "consistent with the BTZ finite-temperature picture reported by Wang & He" until the paper is read and a record written.
- **CF novelty:** n/a.

---

#### CLM-015 — l_AdS = 1/ln χ = 1.4427 is set by the architecture

- **Wording:** *"l_AdS = 1/ln χ = 1/ln 2 = 1.4427. This value is set by the MERA architecture, not by optimization."* (§2.1 Eq.(2) L64).
- **Math:** l_AdS ≡ 1/ln χ.
- **Level:** 1 (definition adopted from the literature).
- **HYP:** HYP-2026-005, HYP-2026-006.
- **SIMs:** `SIM-2026-001.json` `.results.analytical.l_AdS` = 1.4426950408889634 = 1/ln 2 exactly; `SIM-2026-011-interaction.json` `.fits.*.l_AdS`.
- **Analytic:** entanglement-per-cut argument (external).
- **Lit:** manuscript cites `KimSwingle2017`; the project's own `PAPER-2026-009.json` `.key_claims[2]` attributes it to Sahay/Lukin/Cotler — an attribution defect (`inv-manuscript-claims.md` DEF-13).
- **Assumptions:** that a bond-dimension logarithm is a physical length.
- **Exact constraints:** it is a **definition**, exact by construction.
- **Uncertainty:** zero — and that is the point. It carries no error bar into any downstream "agreement".
- **Alternatives:** —
- **Independence:** this constant appears on the "theory" side of CLM-010, CLM-016 and CLM-017 while also being an input to the state construction. Every such comparison is therefore **structurally dependent** at the root.
- **Falsification:** a χ-scan showing the transport/force results do not track 1/ln χ. **Never run** — every transport number is at χ = 2.
- **Status:** correct as a definition; **the honest label is "a defined constant", and the manuscript says exactly that.** Credit.
- **Framing:** keep as stated. Do not let it appear as a prediction.
- **CF novelty:** **near-zero** (definitional).

---

### Cluster C — Worldline correspondence and effective mass (CLM-016 … CLM-018)

---

#### CLM-016 — m_eff agreement to 3.5 %

- **Wording:** table row *"m_eff (ε CFT, Δ=1) 0.693 / m_eff (MERA force profile) 0.670 / Agreement 3.5 %"* (§4.2 L250–253); README row *"Effective mass | m_eff = 0.670 | 0.693 | 3.5%"*.
- **Math:** m²l²_AdS = Δ(Δ−2); Δ = 1 ⇒ m²l² = −1 ⇒ |m_eff| = 1/l_AdS = ln 2 = 0.6931. Measured side: Δ = l_AdS/ξ_2pt with ξ_2pt = 2.154 ⇒ 0.6698.
- **Level:** 1 on the "theory" side (an algebraic identity); the "measurement" side does not reach Level 1 quality.
- **HYP:** HYP-2026-005, HYP-2026-007.
- **SIMs:** `research/data/simulations/effective_mass_analysis.json` `.ads_mass_dimension.epsilon_m_eff` 0.6931, `.comparison_to_measurements.m_eff_from_MERA` 0.6698, `.match_epsilon_vs_measured` "3.5% (0.693 vs 0.670)"; upstream `SIM-2026-002.json` `.fit.xi`.
- **Analytic:** the BF-bound relation is textbook AdS/CFT. ERRATA §E4 already records "0.693 = 1/l_AdS from Δ=1 exactly".
- **Lit:** Camporesi–Higuchi heat kernel on H²; `CorradiniMuratori2020` (no repo record).
- **Assumptions:** (i) the excitation is ε with Δ = 1; (ii) ξ_2pt from V(2)/V(1) is a decay length.
- **Exact constraints:** 0.693 **is** ln 2, i.e. 1/l_AdS by the definition of CLM-015. It is not a measurement.
- **Uncertainty:** none quoted on either side. ξ_2pt = 2.154 is a **two-point** estimate (`HYP-2026-005.json` `.analysis.key_findings[2]`: *"from the ratio V(2)/V(1)"*) taken from the SIM-002 χ=2 MERA whose correlations the same paper calls *"flat (wrong universality class)"*. The primary record `worldline_mc_results.json` `.decay_analysis.m_eff_to_match_mera_2pt` is literally **`NaN`** (invalid strict JSON, ERRATA §D2).
- **Alternatives:** with one ratio of two numbers, a 3.5 % landing near ln 2 is unremarkable. `research/data/theory/research-challenge.md:99-103` reaches the same conclusion independently: *"post-hoc rationalization, not a prediction … The 'agreement' was found, not predicted"*.
- **Independence:** **ALGEBRAICALLY EQUIVALENT at the root** — both sides are functions of the same Δ = 1 CFT input and the same defined l_AdS. Comparing a CFT-derived constant against a fit to a state built to be that CFT is not a confirmation.
- **Falsification:** a multi-point exponential fit on a state with correct critical correlations disagreeing with ln 2.
- **Status:** **WEAKEST SURVIVING PAPER CLAIM.** The manuscript's §8.6 correctly downgrades it to "preliminary diagnostic … only 2 signal points and a post-hoc fit"; the README table does not, and lists it beside genuine measurements.
- **Framing:** delete from any results table; retain as a §8.6 diagnostic note.
- **CF novelty:** **near-zero.**

---

#### CLM-017 — Operator identification via the 16-qubit gap

- **Wording:** *"corroborated by the 16-qubit exact spectrum: the gap E₁ − E₀ = 0.190 corresponds to a scaling dimension x₁ = 0.485, consistent with the ε primary (Δ = 1) shifted by open-boundary effects"* (§4.2 L243).
- **Math:** x₁ = 0.4847 assigned to Δ_ε = 1.
- **Level:** 1.
- **HYP:** HYP-2026-008.
- **SIMs:** `effective_mass_analysis.json` `.spectrum.gap1` 0.190328, `.scaling_dimensions.x1_from_gap` 0.4847, `.expected_sigma` 0.125, `.expected_epsilon` 1.0, `.note` "OBC shifts scaling dimensions from PBC values".
- **Analytic:** **none.** No quantitative OBC-shift calculation exists anywhere in the manuscript or repository.
- **Lit:** standard OBC CFT finite-size scaling (uncited).
- **Assumptions:** that a 51.5 % discrepancy is an OBC shift rather than a different operator.
- **Exact constraints:** Δ_σ = 1/8, Δ_ε = 1 for Ising. The record lists **both** candidates and makes **no assignment**; the manuscript makes one.
- **Uncertainty:** ERRATA §E4 already noted x₁ = 0.4847 gives m_eff = 0.594 under the record's own formula — i.e. the assignment does not close with CLM-016.
- **Alternatives:** x₁ ≈ 0.485 is 3.9× Δ_σ and 0.49× Δ_ε; neither assignment is clean. A boundary-condition-changing operator or a descendant are unexcluded.
- **Independence:** —
- **Falsification:** a computed OBC shift, or a PBC spectrum.
- **Status:** **NOT ESTABLISHED.** It is the only spectral support for CLM-008 and it is a 51.5 % gap called "consistent".
- **Framing:** "the low-lying gap is not cleanly assigned; the operator content of the excitation is untested".
- **CF novelty:** **near-zero.**

---

#### CLM-018 — The three-level correspondence chain

- **Wording:** *"Together, these establish: quantum gravity in ADM superspace = worldline path integral on AdS = measurable MERA observables."* (§4.1 L231).
- **Math:** two asserted equalities.
- **Level:** **0** — interpretation.
- **HYP:** HYP-2026-005, HYP-2026-007.
- **SIMs:** none.
- **Analytic:** **none.** No derivation, no error term, no domain of validity.
- **Lit:** `PAPER-2026-023.json` (Roux, ADM↔worldline in superspace); Ashok–Murthy arXiv 1712.00885 — **no repository record exists** for the second; `PAPER-2026-009.json`.
- **Assumptions:** that three papers on adjacent topics compose into an identity.
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** the three works share vocabulary, not theorems.
- **Independence:** —
- **Falsification:** —
- **Status:** **the manuscript's single largest Level-0 leap** (`inv-manuscript-claims.md` DEF-21). Compounded by bibliography corruption in the Roux entry (record: **Jean-Baptiste** Roux, "Superspace worldline formalism **approach to** Quantum Gravity"; bib: "Antoine Roux", title altered).
- **Framing:** demote to "motivation" under §1 of the standard, or supply a derivation with a stated approximation.
- **CF novelty:** n/a — no calculation was performed.

---

### Cluster D — CFT spectra and the universality ladder (CLM-019 … CLM-022)

---

#### CLM-019 — Tricritical Ising M(4,5) spectrum

- **Wording:** *"recovers the full M(4,5) primary spectrum (Δ_σ = 0.092, Δ_ε = 0.204, Δ_T = 1.999)"* (Abstract L29; §6.5 table).
- **Math:** χ=8 Z₂-symmetric ternary MERA at the O'Brien–Fendley point λ₃ = 0.856.
- **Level:** 1 (reproduction of published CFT data), with a **moderate**-novelty sub-datum (see below).
- **HYP:** `HYP-2026-027.json` — whose `status` is the malformed `"TESTABLE_NEAR_TERM"` and whose newest result note still says the question is "still OPEN"; SIM-051/052 are **not referenced in the HYP record at all** (`inv-hypotheses.md` §0.4).
- **SIMs:** `SIM-2026-051.json` (χ=6, 8 seeds), `SIM-2026-052.json` `.best_spectrum_seed` (0.0917, 0.2038, 1.9994), `.delta_T_statistics`.
- **Analytic:** M(4,5) exact dimensions (0.075, 0.2, 2.0, plus σ′ 0.875 and ε′ 1.2).
- **Lit:** O'Brien–Fendley (the λ₃ = 0.856 tricritical point is theirs).
- **Assumptions:** basin selection by lowest Δ_σ is unbiased for the other dimensions.
- **Exact constraints:** all three targets exact.
- **Uncertainty:** **no error bars anywhere.** Δ_σ = 0.092 vs exact 0.075 is a **22.7 % error** presented inside a table of agreements (the record is franker: "now within 22 % of CFT (was 105 % off)"). "**Full** spectrum" is false — σ′ and ε′, listed in the record's own `cft_targets_TCI_M45`, are not reported. SIM-052's `delta_T_statistics.note` "ALL 6 seeds within 1.5 %" is **false** (seed 4 = 1.505 %); ERRATA fixed this in the manuscript but **never in the source record** (`inv-sims-mid.md` defect 5).
- **Alternatives:** —
- **Independence:** **PARTIALLY INDEPENDENT of Ising** (different model, different operator content) — this is a genuine cross-class check on the *pipeline*. Not independent of the CFT inputs.
- **Falsification:** Δ_ε landing at 1.0 (the Ising value) instead of 0.2.
- **Status:** **SUPPORTED for the class identification; the "full spectrum" and the error-free presentation are overstated.**
- **Framing:** "a Z₂-symmetric MERA reaches the tricritical fixed point; Δ_ε = 0.204 identifies the class; Δ_σ is 23 % high and not converged".
- **CF novelty:** **near-zero** for Δ_T; **moderate** for Δ_ε = 0.204 — this is the one datum that genuinely discriminates c = 7/10 from c = 1/2, and the record correctly calls it "the decisive new datum". Even so it reproduces literature, not new physics.

---

#### CLM-020 — 3-state Potts spectrum at χ = 12

- **Wording:** *"a Z₃-symmetric MERA at χ = 12 recovers Δ_σ = 0.134, Δ_ε = 0.805, Δ_T = 2.001"* (Abstract L29).
- **Math:** Z₃ clock/shift Potts at self-dual f = 1; graded MERA.
- **Level:** 1.
- **HYP:** `HYP-2026-025.json` (`status` SUPPORTED). Its `test_design` and `refutation_criteria` registered a **force-exponent** test on the **Z₃ chiral clock** model; what was delivered is a **scaling dimension** on **3-state Potts** — both the model and the observable were substituted, and only the model substitution is disclosed (`inv-hypotheses.md` §2a).
- **SIMs:** `SIM-2026-062.json` (graded builder validated to 1.75e−15 vs dense; 4/6 clean basins at χ=6 vs 2/8 dense at χ=8), `SIM-2026-063.json` `.results.chi12` (Dsig 0.1324/0.1351, Deps 0.8039/0.8057, Delta_T 2.0004/2.0023).
- **Analytic:** exact Potts dimensions 2/15 = 0.1333, 4/5 = 0.8, 2.
- **Lit:** standard.
- **Assumptions:** the two clean basins are representative.
- **Exact constraints:** all three targets exact.
- **Uncertainty:** the abstract's three numbers are **midpoints of two basins** with no spread quoted, and the clean-basin rate at χ=12 is **2 of 6** — quoted at χ=6 (4/6) but not at χ=12 (`inv-manuscript-claims.md` DEF-10). The χ-progression of Δ_σ (0.089 → 0.137–0.164 → 0.132–0.135) shows χ-starvation was real and was only resolved at the largest χ tried.
- **Alternatives:** —
- **Independence:** **PARTIALLY INDEPENDENT of Ising and TCI** at the model level; same pipeline, same selection rule.
- **Falsification:** Δ_ε ≠ 0.8.
- **Status:** **SUPPORTED for the class identification.** The χ-convergence story (0.089 → 0.14 → 0.133) is honest and closes a caveat the project itself raised.
- **Framing:** as CLM-019.
- **CF novelty:** **near-zero.**

---

#### CLM-021 — Exact-diagonalization pre-gate on the O'Brien–Fendley blocking

- **Wording:** *"we verify the blocking by exact diagonalization, confirming that the blocked operator reconstructs the full Hamiltonian to machine precision (max|H − H_block| < 10⁻¹⁵) at both λ₃ = 0 and λ₃ = 0.856"* (§6.5 L434).
- **Math:** 3-site blocking of the OF chain is exact.
- **Level:** **2 — a genuine methodological contribution.**
- **HYP:** HYP-2026-027.
- **SIMs:** `SIM-2026-051.json` `.blocking_validation.result` (max|H_orig − H_recon| = 0 at λ₃ = 0; **1.1e−16** at λ₃ = 0.856, on 6- and 8-site PBC rings); pre-gate scripts `research/tools/MERAKit.jl/qw_of_pregate.py`, `qw_of_pregate_compare.py` (both exist).
- **Analytic:** —
- **Lit:** O'Brien–Fendley.
- **Assumptions:** none material.
- **Exact constraints:** the answer is 0 or it isn't.
- **Uncertainty:** —
- **Alternatives:** —
- **Independence:** **FULLY INDEPENDENT of the MERA result it gates** — different algorithm, different code, checks an operator identity rather than a physical number.
- **Falsification:** a non-zero reconstruction error.
- **Status:** **SOLID.** This gate is what proved the earlier "OF blocking is wrong" conclusion to have been a MERA wrong-basin artifact rather than a blocking error.
- **Framing:** keep; this is the kind of check §22 asks for and it should be advertised as a method.
- **CF novelty:** **moderate** — the project had previously concluded the blocking was non-exact, so the outcome was genuinely open when the gate was designed.

---

#### CLM-022 — Symmetric parameterization tames the optimization-basin lottery

- **Wording:** *"the symmetric parameterization substantially tames the optimization-basin lottery (2/8 clean basins dense at χ = 8 vs. 4/6 graded already at χ = 6)"* (§6.5 L455); and for Z₂: the *"Z₂-symmetric optimize → densify → analyze"* pipeline that unblocked the OPE work.
- **Math:** clean-basin rate as a function of parameterization.
- **Level:** **2.**
- **HYP:** HYP-2026-025, HYP-2026-027.
- **SIMs:** `SIM-2026-062.json` `.goal` ("2/8 clean at chi=8, SIM-059"), `.verdict` ("4/6 clean basins (2.7x the dense rate)"), `.what_was_built` (graded gate vs dense reference, err 1.75e−15); `SIM-2026-061.json` (the Z₂ v4 pipeline, 8/8 clean basins after three failed designs SIM-056/058/060).
- **Analytic:** symmetry-adapted parameterization restricts the variational manifold to the symmetric sector — standard reasoning, not derived here.
- **Lit:** symmetric tensor networks are established (TensorKit); the contribution is the applied recipe, not the concept.
- **Assumptions:** "clean basin" is defined by a spectral gate that is itself tuned on CFT targets.
- **Exact constraints:** none.
- **Uncertainty:** rates are 2/8, 4/6, 8/8 — **small-sample counts with no confidence intervals**. 4/6 vs 2/8 is not statistically distinguishable at any conventional level (Fisher exact p ≈ 0.13).
- **Alternatives:** different χ (6 vs 8) confounds the comparison — the two rates are not measured at the same bond dimension.
- **Independence:** —
- **Falsification:** a matched-χ comparison showing no rate difference.
- **Status:** **PLAUSIBLE, UNDERPOWERED.** The qualitative claim is well-motivated; the "2.7×" is six versus eight coin flips at different χ.
- **Framing:** "in our runs the symmetric parameterization produced clean basins more often; the comparison is not matched in χ and the sample is small".
- **CF novelty:** **moderate.**

---

### Cluster E — OPE coefficients and the C_TTT ladder (CLM-023 … CLM-029)

---

#### CLM-023 — C_σσε = 0.50 ± 0.03

- **Wording:** *"The result, C_σσε = 0.50 ± 0.03, agrees with the exact Ising value C_σσε = 1/2"* (§8.5 L573; Conclusion; cover letter; README table row *"OPE structure constant | 0.50 +/- 0.03 | 0.5 (exact) | within error"*).
- **Math:** three-point structure constant from Z₂-symmetric scale-invariant MERA fixed-point tensors.
- **Level:** 1.
- **HYP:** HYP-2026-027.
- **SIMs:** `SIM-2026-061.json` `.results.C_sse` (mean 0.5075 at χ=6), `.chi8_confirmation_2026-07-03` (0.5069); `SIM-2026-064.json` `.results.chi12` (basin spread 0.6 %), `.drift_resolution_2026_07_08`.
- **Analytic:** the exact value 1/2 has been known since **BPZ 1984**.
- **Lit:** Belavin–Polyakov–Zamolodchikov; ZMV lineage for the extraction machinery.
- **Assumptions:** the three-site placement systematic averages out.
- **Exact constraints:** **C_σσε = 1/2 exactly.** Only implementation success or failure was possible.
- **Uncertainty:** **the quoted band does not follow from the record's own prescription.** `SIM-2026-064.json` `.drift_resolution_2026_07_08` prescribes the placement average of 0.4722 (ε-far) and 0.5146 (ε-centre) at χ=12 — literally **0.4934 ± 0.0212**, not 0.50 ± 0.03. No method for ±0.03 is stated anywhere. Worse, the record's single-placement χ-progression is **0.5075 → 0.5069 → 0.4957 → 0.4722**, which the record itself annotates *"NOT monotone toward 0.5 — crossed and undershot"*, and its `verdict` reads *"PRECISION ACHIEVED, ACCURACY PUZZLE FLAGGED"* with suspect (3), a genuine finite-χ turnaround by χ ≈ 16–22, *"remains untested"*. **None of that appears in the manuscript, the cover letter or the README.**
- **Alternatives:** the χ-drift away from 0.5 is unexplained; a systematic that grows with χ would invert the conclusion.
- **Independence:** **structurally dependent** — same MERA states, same pipeline, same basin-selection gate as CLM-019/020.
- **Falsification:** χ = 16–22 continuing to drift below 0.47.
- **Status:** **SUPPORTED as a reproduction; the uncertainty is not derived and the adverse χ-trend is undisclosed.**
- **Framing:** "C_σσε extracted at 0.47–0.51 across placements and bond dimensions, bracketing the exact 1/2, with an unresolved downward drift in χ".
- **CF novelty:** **near-zero** (exact since 1984).

---

#### CLM-024 — Structural zeros and symmetry covariance

- **Wording:** *"Two structural checks pass identically on every clean basin: C_σσσ = 0 to machine precision (the Z₂ selection rule) and the symmetry covariance of the fixed-point tensors at the 10⁻¹⁶ level"* (§8.5 L573).
- **Math:** C_σσσ ≡ 0 by Z₂; |P_lift − P_exact| ~ 2e−16.
- **Level:** **2** (a cheap, reusable correctness gate).
- **HYP:** HYP-2026-027.
- **SIMs:** `SIM-2026-061.json` `.results.structural_zeros` ("C_sss = 0 EXACTLY … overlap 1.000000, |P_lift − P_exact| ~ 2e−16 every seed"); `SIM-2026-064.json` `.results.structural`.
- **Analytic:** the selection rule is exact group theory.
- **Lit:** standard.
- **Assumptions:** none material.
- **Exact constraints:** exactly zero.
- **Uncertainty:** —
- **Alternatives:** —
- **Independence:** **FULLY INDEPENDENT of the physics result it gates** (it tests the code, not the CFT number).
- **Falsification:** a non-zero C_σσσ.
- **Status:** **SOLID and genuinely useful.** Undisclosed nuance: `SIM-2026-061.json` `.verdict` is *"VALIDATED (by-the-letter PARTIAL on the pre-registered spread criterion)"*, and one basin (seed 8, C_sse 0.599) failed and was excluded by a C_εεε probe. The manuscript says only "every clean basin".
- **Framing:** advertise as a method; state the exclusion rule and the basin that triggered it.
- **CF novelty:** **near-zero** for the value; **moderate** for the discovery that a C_εεε probe self-flags bad basins.

---

#### CLM-025 — The ±5 % placement gap is kinematic, not an optimization artifact

- **Wording:** *"the two inequivalent three-site placements … bracket the exact value from below and above (0.472 and 0.515 at χ = 12), a ~5 % placement systematic that extended-iteration re-optimization does not move (i.e. it is kinematic, not an optimization artifact)"* (§8.5 L573).
- **Math:** a kill-test: increase `maxiter` and see whether the gap closes.
- **Level:** **2.**
- **HYP:** HYP-2026-027.
- **SIMs:** `SIM-2026-064.json` `.drift_resolution_2026_07_08` (sse 0.4957/0.4722 vs ses 0.5258/0.5146 at χ=10/12; *"the maxiter kill-test … did NOT pull the mean toward 0.5 … ruling out simple under-convergence"*).
- **Analytic:** none — the kinematic origin is inferred from the kill-test, not derived.
- **Lit:** none recorded.
- **Assumptions:** that "not under-convergence" implies "kinematic".
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** a finite-χ truncation effect (the record's own suspect 3) would also survive a maxiter increase. Ruling out one cause is not establishing another.
- **Independence:** —
- **Falsification:** the gap closing at larger χ.
- **Status:** **SUPPORTED as a negative (not under-convergence); the positive attribution "kinematic" is not established.** This is nonetheless good adversarial practice — a designed kill-test, run, and reported.
- **Framing:** "the placement gap survives extended optimization; its origin is undetermined between kinematics and finite-χ truncation".
- **CF novelty:** **moderate.**

---

#### CLM-026 — The C_TTT ladder is complete at three universality classes

- **Wording:** *"THE SELF-COUPLING LADDER IS COMPLETE (Ising + TCI + Potts)"* (`research/data/simulations/SIM-2026-069.json` `title`); README *"Stress-tensor self-coupling | C_TTT = 3.9936 (Ising) | 4.000 (exact) | 0.16%"*; memory index *"three classes ≤0.15 % each"*.
- **Math:** claimed: the three-point stress-tensor coupling C_TTT at c = 1/2, 7/10, 4/5.
- **Level:** 1 — **and not the quantity named.**
- **HYP:** HYP-2026-027 (reverse-linked).
- **SIMs:** `SIM-2026-067.json` (ED circle, Ising, 3.9936), `SIM-2026-068.json` (puMPS, TCI, 3.381 ± 0.005), `SIM-2026-069.json` (puMPS, Potts, 3.163 ± 0.003).
- **Analytic:** **this is the decisive point.** The records' own `method` fields state the construction: `SIM-2026-068.json` `method` — *"c = 2|<T|H_{+-2}|0> * N/(2 pi v_T)|²; C_TTT = 2*sqrt(2)/sqrt(c)"*. In every driver `C_TTT` is the literal line `C_TTT = 2*sqrt(2)/sqrt(c)` (`inv-pipelines.md` §0). ⟨T|L₋₂|0⟩ with |T⟩ = L₋₂|0⟩ **is** the Virasoro norm ⟨T|T⟩ = c/2. So the measurement is a **two-point** matrix element yielding c, followed by a change of variables.
- **Lit:** the vendored ZMV codebase (`research/tools/pumps-setup/VENDOR.md`, pinned `0557b12`) already ships `OBF_Hn_MPO_split` (annotated by the project itself *"O'Brien-Fendley H_n MPOs (TCI!)"*), `potts3_Hn_MPO_split`, and `Hn_in_basis` — i.e. **the original authors wrote the Koo–Saleur machinery for exactly these two models.**
- **Assumptions:** that reporting C_TTT alongside c constitutes two results.
- **Exact constraints:** **C_TTT = 2√2/√c is a Virasoro identity.** Given c, C_TTT is not measurable independently in this construction.
- **Uncertainty:** `SIM-2026-068`/`069` quote ±0.005 / ±0.003 from three-parameter c(N) fits, reproduced exactly by `inv-pipelines.md` §4.2. A cross-pipeline discrepancy is masked: `pumps-setup/VENDOR.md:50` compares puMPS's raw N=12 value against SIM-067's **extrapolated** number, hiding a **7.2 % same-N disagreement in c** caused by a different Koo–Saleur mode discretization (naive vs half-bond phase) documented nowhere. Correcting the convention makes the two pipelines agree to **5e−6** — a far stronger check the project has and does not know it has (`inv-pipelines.md` §4.4).
- **Alternatives:** —
- **Independence:** **ALGEBRAICALLY EQUIVALENT.** "α = 4 at three classes **and** C_TTT at three classes" reads as six confirmations; it is at most two numbers per class (Δ_T and c), and in SIM-068/069 it is **one** — Δ_T is *imposed* there, not measured (only SIM-067 measures Δ_T independently, → 1.982 at N=18).
- **Falsification:** cannot fire independently of a c measurement.
- **Status:** **MISLABELLED.** The central-charge ladder is real, careful work; the C_TTT framing double-counts it. Route A — the genuine three-point contraction — was attempted and **failed** (CLM-028), and Route B silently substituted a two-point observable with no record flagging the change.
- **Framing:** "central charge extracted by Koo–Saleur at three universality classes to ≤0.15 %", and state that C_TTT follows by identity.
- **CF novelty:** **near-zero.**

---

#### CLM-027 — L₋₂ε contamination suppression in puMPS Bloch states

- **Wording:** `SIM-2026-068.json` field 32: the ~N^−0.2 element mixing that made TCI unreachable by ED is suppressed to ≤0.0003 vs T's 0.109 (≈400×) at N = 56, with an observed correction exponent p ≈ 2.4 rather than 0.2.
- **Math:** cross-module contamination of the stress-tensor matrix element, and its scaling in N.
- **Level:** **2 — and per `inv-pipelines.md` §4.3 the strongest methodological result in the repository.**
- **HYP:** HYP-2026-027 (indirect).
- **SIMs:** `research/data/simulations/SIM-2026-068.json`; raw `research/tools/pumps-setup/qw_cttt_of_results_2026-08-10.jsonl`.
- **Analytic:** none — the improved exponent is observed, not derived.
- **Lit:** ZMV PRL 121 230402 is the parent method. **The §8 prior-art gate has not been run on this claim.**
- **Assumptions:** the identification of the contaminating module is correct.
- **Exact constraints:** none — **this is the rarest field in the map: a genuinely unconstrained number.**
- **Uncertainty:** single pipeline, single model class for the p ≈ 2.4 measurement; no independent implementation.
- **Alternatives:** the improvement may be a property of the Bloch-state ansatz already known to the ZMV authors.
- **Independence:** the ED-vs-puMPS comparison at matched N (once the convention is fixed) is a real **PARTIALLY INDEPENDENT** check.
- **Falsification:** a second model class where p reverts to ≈0.2.
- **Status:** **PROMISING, UNGATED.** This is the best §25 Candidate-Paper-C material in the program and it has never been literature-checked.
- **Framing:** a methods note, after a §8 search.
- **CF novelty:** **moderate-to-high** — the suppression factor and the exponent were not fixed by any identity. This and CLM-030/028/035 are the only entries in the map where that is true.

---

#### CLM-028 — Route A (direct three-point contraction) failed

- **Wording:** `SIM-2026-065.json` / `SIM-2026-066.json` — the direct spin-resolved three-point stress-tensor extraction was attempted and did not work; Route B replaced it.
- **Math:** direct ⟨TTT⟩ contraction on MERA fixed-point tensors.
- **Level:** **2** (a documented methodological negative).
- **HYP:** HYP-2026-027.
- **SIMs:** `research/data/simulations/SIM-2026-065.json`, `SIM-2026-066.json`.
- **Analytic:** —
- **Lit:** —
- **Assumptions:** —
- **Exact constraints:** —
- **Uncertainty:** raw scratchpad logs for both records are **absent from the repository** (`inv-sims-late.md` F3).
- **Alternatives:** —
- **Independence:** —
- **Falsification:** —
- **Status:** **A REAL NEGATIVE RESULT, correctly recorded — and then obscured.** Per §16 and §42 this is meaningful progress. Its value is diminished because no record states that the object measured by Route B is different from the object Route A failed to measure.
- **Framing:** publish as a negative: "the direct three-point contraction is not accessible at these bond dimensions; here is why".
- **CF novelty:** **high** — before the run, "Route A extracts spin-2 / Route A doesn't" were both live, and the answer was NO. One of only three high-novelty entries in the map.

---

#### CLM-029 — Predictive two-error cancellation at Potts

- **Wording:** `SIM-2026-069.json` field 23: N = 40, D = 28 was called at 0.8022 ± 0.0005 from D-shift systematics **before** the run, and landed at 0.80197.
- **Math:** an out-of-sample point prediction of a finite-D corrected value.
- **Level:** **2.**
- **HYP:** HYP-2026-025.
- **SIMs:** `research/data/simulations/SIM-2026-069.json`; raw `research/tools/pumps-setup/qw_cttt_potts3_results_2026-08-11.jsonl`.
- **Analytic:** the error-cancellation model is empirical.
- **Lit:** —
- **Assumptions:** the prediction was genuinely locked before the run (the record says so; there is no timestamped pre-registration artifact).
- **Exact constraints:** the target c = 4/5 is exact, but the *predicted intermediate value at finite D* is not.
- **Uncertainty:** one prediction, one hit.
- **Alternatives:** a single successful prediction is weak evidence for the model.
- **Independence:** —
- **Falsification:** further predictions missing.
- **Status:** **The clearest §18 out-of-sample execution in the program**, and the associated stopping rule (`SIM-2026-069.json` field 36: N = 56 omitted because a 5th rung "cannot change the verdict") is model §30/§31 behaviour. Both deserve credit.
- **Framing:** cite as evidence the pipeline's systematics are understood, not as a physics result.
- **CF novelty:** **moderate.**

---

### Cluster F — Yang-Lee biorthogonal Koo-Saleur (CLM-030 … CLM-037)

This is the program's strongest current work. It is also where the gap between the sign result and
the magnitude result is widest, so the two are separated into distinct claims (CLM-030, CLM-031).

---

#### CLM-030 — c_eff = +2/5 is EXCLUDED

- **Wording:** *"c_eff = +2/5 = +0.400: EXCLUDED (wrong sign, ~11× magnitude)"* (`research/data/simulations/SIM-2026-071.json` `.results.discrimination`).
- **Math:** the product-form biorthogonal Koo–Saleur quantity c_KS = 2⟨vac_L|H₋₂|T_R⟩⟨T_L|H₊₂|vac_R⟩ / (⟨T_L|T_R⟩⟨vac_L|vac_R⟩)·(L/2πv_T)² is **negative at every accessible L**.
- **Level:** **2 with genuine Level-3 character** — a measured quantity not fixed by an identity.
- **HYP:** `HYP-2026-028.json`.
- **SIMs:** `research/data/simulations/SIM-2026-071.json` `.results`; raw `research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl` — c_KS = −1.4131954 (L=10), −1.7028834, −1.9537294, −2.1699264, −2.3562439 (L=18), **verified line-for-line** by `inv-sims-late.md` §071.1 and independently re-implemented in Python/ARPACK by `inv-pipelines.md` §0, reproducing to 6 decimals.
- **Analytic:** η = parity is genuine pseudo-Hermiticity — P σᶻ P = −σᶻ ⇒ P H_YL P = H_YL† — verified analytically by the pipelines auditor. The estimator is **invariant under eigenvector renormalization** (ψ_R → z·ψ_R scales numerator and denominator by |z|²), verified analytically from the driver. That directly answers the §12 *Yang-Lee method killer* ("arises from a normalization convention") in the negative.
- **Lit:** PAPER-133 = arXiv 2606.16785v2 (Liu-Shimizu-Liu-Kawabata) supplies the periodic PT-chain route and the PT-edge dodge; correctly attributed in `method` and in `research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md`.
- **Assumptions:** M(2,5) state identification (vacuum = |1⟩ = the **second** k=0 state, Δ_φ = −2/5); the Δ-gate window (1.75, 2.25).
- **Exact constraints:** c_eff = +2/5 and c = −22/5 are both exact. This is a two-way discrimination between known numbers — but unlike CLM-003, the discriminating variable (**the sign**) is not fixed by any identity the auditors could find.
- **Uncertainty:** **this half needs no extrapolation at all.** At L = 18 alone, |c_KS| = 2.36 vs 0.4 — a 6× magnitude separation on top of the sign. Robust across all three defensible h_c^∞ fits (`inv-pipelines.md` §5.6: every value negative, ≥ 9× |c_eff|). Both chiralities agree to ~1e−11; Im/Re ~ 1e−12.
- **Alternatives:** state misidentification. **The sign is a consequence of the Δ-gate choice**: at L = 10 the three k=+2 products are [+46.470, −4.7446, −12.219]; the naive max-element rule (the rule that works on unitary chains) selects the φ-descendant and yields c_KS ≈ **+13.8** — positive. The record states the identification hazard (key-finding 3) but does not state that the headline's sign therefore depends on it (`inv-sims-late.md` §071.3c). The gate is theory-fixed and **pre-registered in the design doc before the run**, so this is a structural dependency, not circularity — but it belongs in the independence ledger and is absent from it.
- **Independence:** the raw negative products are the **only genuinely independent information** in the whole SIM-071 chain (`inv-sims-late.md` §3.2 — five theory inputs sit upstream of the number).
- **Falsification:** an alternative left-pairing (η ≠ P) or an alternative state assignment yielding a positive product. **Neither has been tested** — the driver has exactly one pairing.
- **Status:** **SUPPORTED, robustly.** The record's own framing calls it "PASSED (discrimination decisive)", which for this half is proportionate and arguably understated.
- **Framing:** *"a biorthogonal lattice stress-tensor matrix element at the Yang-Lee point is negative at every accessible size, excluding the effective central charge by sign"*. This can stand without the worldline/holographic framing entirely — §25 Candidate Paper A.
- **CF novelty:** **HIGH on the sign.** Genuinely binary, not forced by any identity located by three separate auditors. **The only high-novelty measured result in the program.**

---

#### CLM-031 — c_KS = −4.29 ± 0.15 equals the true c = −22/5

- **Wording:** *"biorthogonal Koo-Saleur elements at Yang-Lee measure the TRUE central charge — c_KS = −4.29 +/− 0.15 vs c = −22/5 = −4.4"* (`SIM-2026-071.json` `title`); *"c = −22/5 = −4.400: CONSISTENT (2.6 % at ED scale)"* (`.results.discrimination`).
- **Math:** pairwise 1/L intercepts + geometric tail extrapolation of the c_KS(L) ladder.
- **Level:** 1–2 (the target value is exact CFT data; the achievement would be reaching it).
- **HYP:** HYP-2026-028.
- **SIMs:** `SIM-2026-071.json` `.results.extrapolation`; raw `.jsonl` as CLM-030.
- **Analytic:** as CLM-030.
- **Lit:** as CLM-030.
- **Assumptions:** the geometric-tail ratio estimated from **two** samples (0.730, 0.728) is asymptotic.
- **Exact constraints:** c = −22/5 exactly for M(2,5).
- **Uncertainty:** **three separate problems, all quantified by phase-1 auditors.**
  1. **The extrapolation supplies 82 % of the answer.** Largest-L datum −2.356; quoted limit −4.285 (`inv-sims-late.md` §071.3a). The tail term alone is 11.4 % of the final value.
  2. **The estimator was calibrated in a regime with a 16× smaller lever arm.** In SIM-070 the same estimator's tail contributed **0.7 %** with **four** ratio samples, and the ratio sequence there **drifted monotonically upward** (0.558 → 0.614 → 0.667 → 0.718) without converging. Two samples in SIM-071 cannot exclude the same drift.
  3. **The h_c^∞ systematic is understated by ~5–6× and excluded from the band.** The record states "≤0.01 at L=18"; direct measurement gives **0.056 at L=16** for the record's own Δh, and propagating the three defensible h_c^∞ fits moves the headline from **−3.67 to −7.04** (`inv-pipelines.md` §5.6). The realistic fit-model band is roughly **[−7.0, −3.7]**, not ±0.15. The ±0.15 itself is *"not derived from any stated procedure"* — asserted as "estimator systematic" — and does not even cover the ratio-sensitivity range (r = 0.80 → −4.50).
- **Alternatives:** nothing in the analysis discriminates −4.4 from −4.0 or −5.0; the ratio sweep spans −4.15 to −4.50 under reasonable assumptions alone. Only two candidates were pre-registered.
- **Independence:** the extrapolated value inherits SIM-070's h_c^∞ **and** SIM-070's estimator selection — the two records are **structurally dependent**, not a gate plus an independent measurement.
- **Falsification:** puMPS-scale L; an alternative estimator; an h_c^∞ sensitivity band published with the result.
- **Status:** **NOT ESTABLISHED at the quoted precision.** The honest statement is: *"the extrapolated magnitude is consistent with 22/5 and inconsistent with 2/5, with the magnitude poorly determined."* The record's own `caveats` field says much of this; the `title`, `verdict` and `key_findings` do not, and the downstream restatements (`NEXT-SESSION.md`, `HYP-2026-028.json` `phase2_result`, the memory index, `docs/governance/PROJECT-REVIEW-2026-08-11.md`) propagate the title, not the caveat.
- **Framing:** report the sign result (CLM-030) as the headline and the magnitude as consistent-but-unresolved, with the h-model band shown.
- **CF novelty:** **moderate.** Given the sign, landing near a negative O(1) number was likely; landing on −22/5 specifically was not demonstrated.

---

#### CLM-032 — Priority: first lattice extraction of a negative central charge

- **Wording:** *"First lattice extraction (to our knowledge) of a NEGATIVE central charge from stress-tensor matrix elements; standard approaches obtain only c_eff from Casimir scaling."* (`SIM-2026-071.json` `key_findings[1]`, line 22).
- **Math:** —
- **Level:** n/a (priority claim).
- **HYP:** HYP-2026-028 (inherits it into a `SUPPORTED` status).
- **SIMs:** `SIM-2026-071.json`.
- **Analytic:** —
- **Lit:** **none.** §8 requires searches across thirteen named variants (negative central charge, effective central charge, non-unitary CFT, biorthogonal CFT, Koo–Saleur generators, lattice Virasoro generators, stress-tensor matrix elements, Yang-Lee chains, non-Hermitian spin chains, PT-symmetric criticality, transfer matrices, finite-size scaling, logarithmic/non-unitary conformal methods). **None has been performed.** The weekly-scan notes cited in HYP-028 are window feeds, not a targeted prior-art search, and they surface adjacent work (`PAPER-2026-129` "biorthogonal benchmark", `PAPER-2026-132` "PT-BCFT-dual tooling") without ever asking whether it already contains this extraction.
- **Assumptions:** —
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** —
- **Independence:** —
- **Falsification:** one prior paper.
- **Status:** **§8 VIOLATION — the exact prohibited phrase ("to our knowledge") is in the record.** `research/data/theory/` contains no literature-gate record. Related mislabels: `SIM-2026-058.json` and `SIM-2026-065.json` call TCI C_TTT *"the novel target"* when it is fixed by c = 7/10.
- **Framing:** strike the phrase until the search is recorded. **This is also the single highest-leverage next action in the program**: if the search comes back clean, CLM-030 becomes a publishable methods result (§25 Candidate Paper A); if it does not, the program's strongest claim collapses to a reproduction.
- **CF novelty:** n/a.

---

#### CLM-033 — The unitary Ising control validates the pipeline

- **Wording:** *"extrapolated: 0.49986 (Richardson in 1/L² …) vs exact 0.5 (0.03 %)"*; *"all biorthogonal norms +1.0000 (Hermitian limit), Z2 structural zeros ~1e-24, same orientation convention as YL"* (`SIM-2026-071.json` `.unitary_control`).
- **Math:** the same driver run with `MODE=ising`.
- **Level:** 1.
- **HYP:** HYP-2026-028.
- **SIMs:** `SIM-2026-071.json` `.unitary_control` — **and nowhere else.** Repo-wide grep for 0.517483 / 0.512776 / 0.509748 / 0.49986 returns only downstream restatements (`NEXT-SESSION.md`, `PROJECT-REVIEW-2026-08-11.md`, `HYP-2026-028.json`) (`inv-sims-late.md` §071.4.1).
- **Analytic:** —
- **Lit:** —
- **Assumptions:** that "same code path" implies the control exercises the machinery under test.
- **Exact constraints:** c = 1/2 exactly.
- **Uncertainty:** the control's own extrapolation is a **different estimator** from the headline's — a single 1/L² pairwise intercept on 3 points with a ~2 % correction, versus 1/L intercepts + geometric tail on 5 points with an 82 % correction. Two estimators, one labelled as validating the other.
- **Alternatives:** —
- **Independence:** **the control shares 148 of 152 lines with the measurement it validates, and one of the four differing lines is `HC = 0.0` — which switches non-Hermiticity off** (`inv-pipelines.md` §0, §5.3–5.4). In the Hermitian TFIM, P = Πσˣ commutes with H, so the biorthogonal pairing collapses to ±⟨ψ_R| — confirmed by the record's own *"all biorthogonal norms +1.0000"*. The control therefore validates the Koo–Saleur element arithmetic, momentum resolution, orientation convention and gap normalization, and **exercises none of**: indefinite metric, left ≠ right, non-normality, conditioning, negative norms.
- **Falsification:** —
- **Status:** **VALID for what it tests; MISLABELLED as validating the biorthogonal machinery.** §19: "a serious control should be capable of defeating the preferred interpretation" — this one cannot fail in the way the YL run could. Compounding: **the strongest claim's only control has zero persisted raw output.**
- **Framing:** "a Hermitian null test of the estimator plumbing". A control that *would* count: a synthetic non-normal matrix with known spectrum, or an alternative η-pairing.
- **CF novelty:** **near-zero.**

---

#### CLM-034 — PAPER-133 reproduced at 0.01 % (the Phase-1 gate)

- **Wording:** *"PAPER-133 Yang-Lee boundary-data reproduction PASSED (R_inf = −1.61820 vs −(1+√5)/2, 0.01 %; g_1 = 0.72535 vs 0.725073, 0.04 %)"* (`SIM-2026-070.json` `title`).
- **Math:** projected-partition-function spectroscopy on the periodic PT-symmetric Ising chain, λ = 4, at h = h_c^∞ = 1.5587127.
- **Level:** 1, **correctly labelled Level 1 by its own record.**
- **HYP:** HYP-2026-028.
- **SIMs:** `research/data/simulations/SIM-2026-070.json`; raw logs **committed** — `research/tools/yanglee-pt/yl_run_8_18.log`, `yl_proj.log`; driver `qw_yanglee_pt.jl`; source PDF `research/downloads/2606.16785v2.pdf`. Both phase-1 auditors re-derived h_c^∞ and the Richardson tail from the tracked table and reproduced all seven quoted digits.
- **Analytic:** R_∞ = −(1+√5)/2 and g₁ = 0.725073 are exact BCFT values.
- **Lit:** PAPER-133.
- **Assumptions:** the fixed-exponent (b = 12/5) fit for h_c^∞.
- **Exact constraints:** both targets exact.
- **Uncertainty:** honestly bounded — the auditor's tail-ratio sweep gives ±0.3 % on R_inf, so the quoted 0.01 % is **more precise than the estimator's own spread warrants**, though the agreement is genuinely earned (the tail contributes only 0.7 %). The record openly discloses that the estimator was **selected after seeing that free-power fits overshoot by 8 %** — legitimate here (the answer is known) but it means the estimator is calibrated where the answer is known and then reused where it is not (→ CLM-031).
- **Alternatives:** —
- **Independence:** **PARTIALLY INDEPENDENT** — reproduces a published table with an independent implementation.
- **Falsification:** failure to reproduce.
- **Status:** **SOLID. The cleanest record in the program**: a reproduction, labelled a reproduction, with its raw logs committed. Also the load-bearing physical evidence that the Yang-Lee fixed point was actually reached — a **better** gate than the entanglement-entropy c_eff gate HYP-028 pre-registered, though the substitution is undocumented.
- **Framing:** as stated.
- **CF novelty:** **near-zero** by construction, and the record says so.

---

#### CLM-035 — The module-identification rule inverts at Yang-Lee

- **Wording:** *"The T-identification discipline INVERTS at YL: the cross-module product to the φ-descendant is ~10× LARGER than T's (in unitary chains cross-tower elements are ~1e-4 suppressions). Δ-gating above the vacuum is mandatory; raw element dominance silently measures the wrong state."* (`SIM-2026-071.json` `key_findings[3]`).
- **Math:** ratio of the φ-descendant element to the T element: 9.8× at L = 10, 11.0× at L = 18, with opposite sign.
- **Level:** **2** — and per §13's closing instruction, potentially the most informative aspect of the work.
- **HYP:** HYP-2026-028.
- **SIMs:** `SIM-2026-071.json`; raw `qw_yanglee_ks_results.jsonl` `prods` arrays — [+46.470, −4.7446, −12.219] at L=10; [+28.451, −2.5884, −7.3351] at L=18. Quantitatively verified.
- **Analytic:** the M(2,5) φ level-2 null-vector structure predicts one φ-descendant at Δ_vac → 1.6 below T at 2.0; derivation in `HYP028-BIORTHO-KS-DESIGN.md` Phase-2 refinement 3, internally consistent.
- **Lit:** none recorded — this is exactly the kind of behaviour a §8 search should look for.
- **Assumptions:** the module assignment.
- **Exact constraints:** the *positions* are fixed by the null-vector structure; the *element magnitudes* are not.
- **Uncertainty:** the record calls the k=±2 cluster match *"exactly"*; the raw Δ_vac[1] is 1.524 at L = 18 against the predicted 1.6 — **4.8 % short at the largest L**, trending correctly but not "exactly" (`inv-sims-late.md` §071.1). A **third** k=±2 state at Δ_vac = 3.015 → 3.355 is neither identified nor discussed.
- **Alternatives:** —
- **Independence:** raw data, minimal theory input beyond the assignment.
- **Falsification:** a second non-unitary class where the ordering does not invert.
- **Status:** **SUPPORTED and honestly disclosed.** §13 explicitly instructs *"Do not hide the inversion of the unitary identification rule"* — the project did not hide it. Credit.
- **Framing:** a headline methods finding in Candidate Paper A, not a footnote.
- **CF novelty:** **HIGH.** Nothing predicted this before the run; the naive rule was expected to work.

---

#### CLM-036 — C_TTT is imaginary at c < 0

- **Wording:** *"C_TTT = 2√2/√c is IMAGINARY at c < 0 — the graviton self-coupling does not survive as a real amplitude in the non-unitary theory even though α = 2Δ_T = 4 kinematics does."* (`SIM-2026-071.json` `key_findings[4]`).
- **Math:** substitute c < 0 into an identity.
- **Level:** 1 — trivially, this is arithmetic on a known formula.
- **HYP:** HYP-2026-028.
- **SIMs:** none required.
- **Analytic:** one line.
- **Lit:** the reality/normalization of stress-tensor three-point couplings in non-unitary CFT is a studied question; **no record cites it.**
- **Assumptions:** that the unitary normalization convention for C_TTT carries over unchanged to c < 0.
- **Exact constraints:** the identity itself.
- **Uncertainty:** —
- **Alternatives:** the standard treatment may simply use a different normalization in non-unitary theories, in which case there is nothing to interpret.
- **Independence:** —
- **Falsification:** a literature convention that renders it real.
- **Status:** **TRUE BUT EMPTY as stated.** The record correctly flags the *interpretation* as "Phase 3, open". Listed here because it is being carried forward as a research direction and should not be mistaken for a finding.
- **Framing:** an open question, contingent on a convention check that has not been done.
- **CF novelty:** **near-zero** (it is √ of a negative number).

---

#### CLM-037 — The c_KS estimator is normalization-invariant

- **Wording:** implicit in the design (`HYP028-BIORTHO-KS-DESIGN.md`) and in the product-form estimator; **never stated as a result in any record.**
- **Math:** under ψ_R → z·ψ_R both numerator and denominator scale by |z|², so c_KS is invariant.
- **Level:** **2** (and it answers §13 question 3 outright).
- **HYP:** HYP-2026-028.
- **SIMs:** derived analytically from `research/tools/yanglee-pt/qw_yanglee_ks.jl` by the phase-1 pipelines auditor (`inv-sims-late.md` §071.2); **no numerical normalization-variation test was ever run.**
- **Analytic:** yes — a two-line proof.
- **Lit:** —
- **Assumptions:** the product form (no square roots) is retained.
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** invariance under *rescaling* does not imply invariance under a different **pairing** (η ≠ P), which is untested.
- **Independence:** —
- **Falsification:** a normalization-variation test moving c_KS.
- **Status:** **TRUE AND UNCLAIMED.** It defuses the most obvious §12 killer ("the negative c arises from a normalization convention") and the project does not know it has it. **The cheapest high-value write-up in the program.**
- **Framing:** state it explicitly, with the proof and a numerical confirmation run, in any methods paper.
- **CF novelty:** **moderate** (a design property, but one that had to be checked).

---

### Cluster G — Optimization method, hardware, and program-level claims (CLM-038 … CLM-040)

---

#### CLM-038 — The two-phase ALM + projection optimizer

- **Wording:** *"we introduce a two-phase optimization method … that achieves Z₂-symmetric MERA ground states at 24 qubits where single-phase methods fail"* (Abstract L29); *"At N = 24 (L = 5, 252 parameters), all five seeds converge to 3.33–3.34 % energy error with P = 1.000 throughout, except seed 13 at 4.30 %"* (§2.2 L93).
- **Math:** Phase 1 = augmented Lagrangian on the Z₂ constraint; Phase 2 = projection + L-BFGS-B.
- **Level:** **2 — the most defensible contribution in the manuscript's first half.**
- **HYP:** HYP-2026-002.
- **SIMs:** `SIM-2026-008b-8q-test.json` `.n_params` 70, `.best_error_pct` 1.11505; `SIM-2026-008c.json` `.n_params` 252, `phase2_err` 3.3365 / 3.3340 / 3.3398 / **4.3014** / 3.3345, `.total_time_s` 160010.518 (= 44.45 h); failure baselines `SIM-2026-003.json` `.vqe.state_analysis` (magz −0.7863, `state_type` "ferromagnetic_product_like"), `SIM-2026-005.json` `.pct_error` 3.2151, `SIM-2026-006.json` `.pct_error` 4.3090.
- **Analytic:** ALM is standard constrained optimization; the contribution is the application.
- **Lit:** **the §8 gate has not been run** — §2.2's claim that ALM "[has] not been applied to quantum variational circuits with discrete symmetry constraints" carries no evidence (`inv-manuscript-claims.md` DEF-16).
- **Assumptions:** that the collapse baseline is a property of the method rather than of this ansatz/optimizer pair. The manuscript's ">15 independent seeds" reaches 17 only by counting **Z₂-projection** runs, which are not "standard variational optimization"; the unconstrained-collapse evidence is essentially SIM-003 (20q, 10 seeds) plus one control point.
- **Exact constraints:** none — energies and seed spreads are genuinely unconstrained numbers. **This is one of the few Level-2 claims in the map with real counterfactual content.**
- **Uncertainty:** **"P = 1.000 throughout" is false for Phase 1** — `SIM-2026-008c.json` `phase1_P` = 1.478e−6, 1.504e−6, 5.81e−7, **−1.56e−10**, 1.310e−6; the Z₂ condition holds only *after* Phase 2 (`inv-manuscript-claims.md` DEF-07). Appendix B's "typical Phase 1 energy 8.2 %" is the **8-qubit** figure placed in a 24-qubit appendix (N=24 `phase1_err` = 3.36–5.24 %). A main-text quantitative claim ("all seeds at N=24 remain at ⟨P⟩ = 0 with 4–5 % energy error") rests on `SIM-2026-007.json`, which **does not exist** (ERRATA §E3: JSON lost on RunPod teardown).
- **Alternatives:** a different ansatz or optimizer might not collapse.
- **Independence:** internally consistent; no independent reimplementation.
- **Falsification:** a single-phase method reaching 3.33 % at 24 q.
- **Status:** **SUPPORTED for this codebase, with three record defects in the reporting.**
- **Framing:** a methods contribution, stated as codebase-scoped, after a §8 search.
- **CF novelty:** **moderate** — the energies, seed spreads and the collapse behaviour were not fixed in advance by anything.

---

#### CLM-039 — The 3.33 % floor is an expressibility ceiling regardless of optimizer

- **Wording:** *"The 3.33 % floor is a circuit expressibility ceiling … the χ = 2 binary MERA cannot represent the N = 24 critical ground state beyond this fidelity, regardless of optimizer."* (§2.2 L93; repeated §7.3 L544).
- **Math:** an inference from a seed-cluster to a representability bound.
- **Level:** **0** — an unsupported generalization presented as a result.
- **HYP:** HYP-2026-002, HYP-2026-009.
- **SIMs:** `SIM-2026-008c.json` (5 seeds), `SIM-2026-006.json` (3 seeds).
- **Analytic:** **none.** No bond-dimension entanglement bound is computed; no overlap or fidelity gate on the state is reported.
- **Lit:** —
- **Assumptions:** five seeds of one optimizer family generalize to all optimizers.
- **Exact constraints:** none.
- **Uncertainty:** —
- **Alternatives:** **the project has already been wrong in exactly this way.** `research/ERRATA.md` §D5 / D5-RESOLUTION records that `SIM-2026-036`'s identical "bond-dimension ceiling" verdict was later proved (SIM-039/040) to be a **gradient-engine + wrong-sector-objective artifact**, with the stated lesson *"'energy looks converged' is not 'state is faithful'"*. The manuscript repeats the retracted inference pattern verbatim, with no entanglement or overlap check on the χ = 2 N = 24 state (`inv-manuscript-claims.md` DEF-17).
- **Independence:** —
- **Falsification:** another optimizer beating 3.33 %; or a computed χ = 2 representability bound.
- **Status:** **NOT SUPPORTED.** Related and equally unsupported: the accompanying *"flat C_vac ≈ 0.70 for all dr ≥ 2"* characterization, where the record's values span **0.62–0.83** (a 34 % spread).
- **Framing:** "our optimizer family plateaus at 3.33 %; whether this is a representability limit is untested".
- **CF novelty:** n/a — no calculation supports the generalization.

---

#### CLM-040 — The Helios hardware path

- **Wording:** *"A hardware path is designed for Quantinuum Helios (57 CNOTs, 0.57 % logical error)."* (Abstract L29); README *"57 CNOT gates … 0.57 % accumulated logical error (vs 41.2 % on IBM Heron — not viable)"*.
- **Math:** pytket compile of a 32-qubit 3-layer MERA to Helios-native gates; error budget = 1 − (1 − p)^n.
- **Level:** 2 (an engineering design), presented without its own feasibility verdict.
- **HYP:** `HYP-2026-013.json` — recorded `status` **"proposed"** on disk while its own SIM returned `PARTIALLY_REFUTED` (`inv-hypotheses.md` §0.1).
- **SIMs:** `research/data/hardware/pytket_compilation_results.json` → 32q/3-layer block: `native_quantinuum.zzphase_count` **57** ✓, `error_budget.original_pct` **0.5684** ✓, `.n_params` **286**, `.depth` 15 (native) / 25 (pre-opt) / 9 (TK2). Hardware specs backed by `HW-2026-009/018/024/046.json`.
- **Analytic:** —
- **Lit:** `PAPER-2026-017.json` (Anand et al., MERA on trapped-ion hardware) — cited with **wrong first author, wrong title, wrong venue, and a claim ("entanglement entropy scaling") the record contradicts ("long-range correlations")**.
- **Assumptions:** logical (10⁻⁴) rather than physical (7.9×10⁻⁴) error rates.
- **Exact constraints:** none.
- **Uncertainty:** the section is built on **two mutually inconsistent internal records**: 532 vs **286** parameters, depth ≈30 vs **15/25**, IBM 99.5 % vs **99.8 %**, 57 gates vs the record's **140**-CNOT circuit behind the 24.5 % figure. README's **41.2 %** matches **no repository record at all** (grep returns nothing) and disagrees with the manuscript's own 24.5 %. Azure free credits are overstated **20×** (800 HQC is a $10 000 grant; the free tier is 40 HQC). The stated HQC formula does not reproduce the record's worked examples. The protocol "15–20 steps, dt = 0.05" covers t ∈ [0, 1.0] and **cannot reach** the dip (t = 2.50) or reappearance (t = 4.75) that define T; "280 000 shots for 5σ" has no power calculation anywhere.
- **Alternatives:** —
- **Independence:** —
- **Falsification:** already available and omitted — `research/data/simulations/SIM-2026-019.json` `.verdict` **PARTIALLY_REFUTED**, `.key_finding` *"Helios 99.921 % achieves dr_max = 2, not dr_max = 4 … a 2-point fit is insufficient to establish a power law"*, `.correction` *"~99.97–99.99 % required. Helios is insufficient for power-law detection."* At the physical rate, the same 57 gates give a **4.4 %** budget — *above* the ≈3 % signal.
- **Status:** **UNRELIABLE AS WRITTEN.** The two headline numbers (57, 0.57 %) verify; nearly everything around them does not, and the project's own feasibility verdict is absent from the manuscript, the README and the abstract.
- **Framing:** "a compiled circuit exists at 57 two-qubit gates and a 0.57 % logical budget; the project's own noise study finds that budget insufficient to fit the exponent".
- **CF novelty:** n/a (engineering).

---

### Cluster H — Program-level public claims (CLM-041, CLM-042)

These are the claims a reader meets first. They are not in the manuscript; they are in `README.md`,
which is the repository's front page and the Zenodo/GitHub landing text.

---

#### CLM-041 — Pattern recognition generates emergent geometry with gravitational content

- **Wording:** *"measured a holographic force law inside MERA tensor networks and showed it is universal across three conformal field theory classes — evidence that hierarchical pattern recognition generates emergent anti-de Sitter geometry carrying quantitative gravitational content"* (`README.md` L5). Reinforced at L138–142: *"Eighteen months later, the math says yes"*; L26–27: *"exhibiting the structural signature of gravity rather than of any other interaction"*.
- **Math:** the conjunction of CLM-001, CLM-004, CLM-010, CLM-023, CLM-026.
- **Level:** **0** — interpretation stacked on Level-1 components.
- **HYP:** the program trunk (§29 of the standard).
- **SIMs:** all of the above.
- **Analytic:** none. No definition of "gravitational content" that is operationally testable is given anywhere in the repository.
- **Lit:** —
- **Assumptions:** (i) that a force law was measured at three classes — **it was measured at one** (CLM-004); (ii) that Δ_T = 2 recurring is evidence rather than a theorem; (iii) that "hierarchical pattern recognition" and "MERA optimization" are interchangeable terms — §1 of the standard explicitly forbids letting "pattern recognition", "emergent", "holographic" and "geometry" carry explanatory weight without operational definitions.
- **Exact constraints:** every quantitative component of this claim is exactly fixed by conformal symmetry, a Virasoro identity, BPZ, or an architecture definition. That is the whole finding of this map.
- **Uncertainty:** the README's own results table carries at least four values whose stated agreement this audit does not support: α "3 independent measurements" (CLM-002), "converging as 1/N" (CLM-011), C_σσε "within error" (CLM-023), m_eff 3.5 % (CLM-016).
- **Alternatives:** **Hypothesis A of §4 of the standard** — MERA is an efficient hierarchical representation of critical states and the geometry is descriptive. **Nothing in the program currently distinguishes A from B.** No matched non-geometric control has ever been built (§10, §19); no rewiring experiment (§11.H); no reconstruction-locality test (§11.A).
- **Independence:** —
- **Falsification:** a matched non-geometric ansatz reproducing every reported observable — **never attempted.**
- **Status:** **NOT ESTABLISHED, and it is the claim the whole standard was written to constrain.** The project's own informal review (`docs/governance/PROJECT-REVIEW-2026-08-11.md` §4) already answers it negatively: *"Every quantitative success so far is ordinary CFT data."*
- **Framing:** replace with the §5 ladder: "we validated three numerical pipelines against exact CFT data and developed methods X, Y, Z; whether the geometric language has operational content is the open question."
- **CF novelty:** n/a — no calculation tests this claim.

---

#### CLM-042 — First open-source multi-agent AI team producing original scientific research

- **Wording:** *"This may be the first open-source example of a multi-tier AI agent team producing original scientific research with quantitative results."* (`README.md` L197).
- **Math:** —
- **Level:** n/a (priority claim, meta-scientific).
- **HYP:** —
- **SIMs:** —
- **Analytic:** —
- **Lit:** **none recorded.** `references.bib` contains three uncited AI/science-of-science entries (`Rosenfeld2025` Kosmos multi-agent AI, `Wang2026SciSciGPT`, `Sun2026`) which suggest the adjacent literature was at least encountered — and Kosmos in particular is a directly competing prior claim.
- **Assumptions:** that "original scientific research with quantitative results" is satisfied by Level-1 reproductions.
- **Exact constraints:** —
- **Uncertainty:** —
- **Alternatives:** several published multi-agent scientific-discovery systems.
- **Independence:** —
- **Falsification:** one prior open-source example.
- **Status:** **§8 VIOLATION** (hedged with "may be", which the standard does not accept as a substitute for evidence). It is also weakened by CLM-041: if the quantitative results are reproductions, the claim's own predicate is unmet.
- **Framing:** describe the architecture and let readers judge; the agent infrastructure is genuinely interesting and does not need the priority claim.
- **CF novelty:** n/a.

---





---

## 3. Cross-cutting analysis

### 3.1 The shared-input root system (§7)

Almost every "agreement" in the program traces back to one of five inputs that appear on **both**
sides of the comparison. Mapping this is the point of §7.

| Shared root | Claims that inherit it | Consequence |
|---|---|---|
| **Δ_T = 2** (Virasoro theorem, every unitary 2D CFT) | 001, 002, 003, 004, 008, 019, 020, 026, 031(via v_T), 041 | The "prediction" and the "measurement" are the same number. `SIM-2026-014.json` `key_finding` says this outright. |
| **l_AdS ≡ 1/ln χ** (architecture definition, CLM-015) | 010, 011, 013, 016, 041 | Every transport and mass "agreement" contains a defined constant on the theory side. |
| **The one observable F(dr) = E_dual − E₀ − 2δE_single**, one operator σ_j, one fit window dr ≥ 2, one fit code | 001, 002, 003, 005, 006, 008 | The "three consistent evaluations" are one measurement at two sizes plus a variational copy of one of them. |
| **The MERAKit optimize → densify → spectral-gate pipeline** and its basin-selection rule | 004, 019, 020, 022, 023, 024, 025 | Basin selection tunes on Δ_σ, then a neighbouring dimension is reported as agreement. The mitigation (Δ_T clusters across all basins) is real and is stated — but the selection is never priced as a systematic. |
| **h_c^∞ = 1.5587127 and the two-level Richardson estimator, both from SIM-070** | 030, 031, 033 | SIM-070 is a gate *and* a parameter supplier *and* the estimator's calibration case. It is not an independent check of SIM-071. |

**The only genuinely independent information in the entire map:**
(a) the sign and relative magnitude of the Yang-Lee biorthogonal products (CLM-030, CLM-035);
(b) the L₋₂ε suppression factor and exponent (CLM-027);
(c) the ED pre-gate on OF blocking (CLM-021) and the C_σσσ structural zero (CLM-024) — both of
which test code rather than physics, which is exactly what makes them useful;
(d) the optimizer energies and seed spreads (CLM-038);
(e) the ED-vs-puMPS matched-N comparison the project has but does not use (CLM-026).

### 3.2 The §24 "delete the word" test, applied to the map

`inv-manuscript-claims.md` §4 counted 65 occurrences of holographic/emergent/worldline/geometry in
the manuscript and found **2 load-bearing, 12 manufacturing**. Applied to this map: deleting every
such word removes **CLM-007, 014, 018, 041** entirely, and reduces **CLM-001, 008, 010, 013** to
"an interaction-energy exponent", "an unidentified exchanged operator", "an excitation revival
time", and "a product of two numbers". What survives untouched is exactly the Level-2 set:
CLM-009, 021, 022, 024, 025, 027, 028, 029, 030, 035, 037, 038.

**Every claim that survives the word test is a method. Every claim that fails it is an
interpretation.** That is the cleanest statement of the program's current position.

### 3.3 Killer tests (§12) — status across the map

| Killer named in §12 | Applies to | Status |
|---|---|---|
| **Emergent-geometry killer** (matched non-geometric control reproduces the observable) | 041, 010, 001 | **NEVER ATTEMPTED.** No matched control exists anywhere in the repository. |
| **Independent-prediction killer** (the observable is analytically fixed by the same CFT data) | 001, 004, 008, 016, 026 | **ALREADY FIRED**, repeatedly, and the project states it itself (§6.5 of the manuscript; `SIM-2026-051.json` `verdict`; the cover letter's CL-2). It has not been acted on. |
| **Reconstruction killer** (bulk locality dies under gauge changes) | — | Not applicable yet; no reconstruction work exists. |
| **Yang-Lee method killer** (negative c from normalization / conditioning / misidentification / EP instability) | 030, 031 | **PARTIALLY DEFUSED**: normalization-invariance holds (CLM-037, unclaimed). **NOT tested**: alternative η-pairing, EP-proximity thresholds (the designated ⟨Ψ_L\|Ψ_R⟩ health metric is printed and never checked), pseudospectral conditioning, synthetic non-normal controls, independent code path (now partly supplied by the phase-1 auditor's Python/ARPACK reimplementation). **State misidentification is the live one** — the sign depends on the Δ-gate (CLM-030). |
| **Universality killer** (works in one tuned chain, fails in nearby representatives) | 004, 019, 020 | **Inverted**: the detuning scan in `hyp010_criticality_scan.json` shows the *transport* result failing exactly this test (factor-6 swing), and it is unreported. |

### 3.4 Where the §36 prediction registry broke

`HYP-2026-028.json` is the clearest case and it is instructive because the record's own discipline
is what makes the failure visible: the original `claim` (α outside [3.2, 4.8] at a non-unitary
point), `refutation_criteria`, and prior result notes are all **preserved** — §36 satisfied in
letter — but the `status` was advanced to `SUPPORTED` on the strength of SIM-070/071, which
measured **no α at all** and ran **no c_eff entanglement gate**. No field states "the registered α
test remains untested" (`inv-sims-late.md` §4). Six further hypotheses (011, 012, 013, 014, 015,
016, 022) still read `"proposed"` on disk after their own SIMs returned
`PARTIALLY_SUPPORTED`/`NOT_SUPPORTED`/`PARTIALLY_REFUTED`/`REFUTED`; the corrected statuses live
only in an out-of-repository memory file.

Consequence for this map: **the hypothesis records cannot be used to determine any claim's status.**
Every `Status` line above was reconstructed from SIM `verdict` fields, ERRATA, and the manuscript.

### 3.5 The four things that should be protected in any revision

Per §32, transparent self-correction increases the credibility of surviving claims. The program has
five instances of it and they are its best asset:

1. **ERRATA E2** — a published number (0.72 %) retracted by the project's own follow-up, in-text,
   with the superseding artifact named (CLM-010).
2. **The N = 24 transport exclusion** — `SIM-2026-025.json` `.runs.N24.exclusion_reason` is
   *stronger* language than the manuscript uses ("clearly not the holographic transport signal").
3. **The χ = 3 sign-flip disclosure** (CLM-002) and the two-point-fit disclosure (CLM-016 §8.6).
4. **The Route A negative** (CLM-028) and the SIM-069 stopping rule (CLM-029).
5. **§6.5's "all sample the same conformal fixed point"** — the manuscript stating the §7
   independence problem against its own interest.

---

## 4. Machine-readable index (§6 requires both forms)

Pipe-delimited. Columns: `id | level | cf_novelty | independence | status | primary_record`.
`independence` uses the §7 vocabulary: `IND` fully independent · `PART` partially independent ·
`STRUCT` structurally dependent · `ALG` algebraically equivalent · `CONS` primarily a consistency
check · `-` not applicable.

```
CLM-001 | 1  | near-zero  | STRUCT | WEAKENED (window systematic ~8sigma) | SIM-2026-011-interaction.json
CLM-002 | 1  | near-zero  | STRUCT | MISLABELLED ("independently")        | SIM-2026-015d.json
CLM-003 | 1  | near-zero  | STRUCT | NOT SUPPORTED at claimed sigma       | SIM-2026-017-statistics.json
CLM-004 | 1  | near-zero  | ALG    | SUPPORTED for Delta_T, not for force | SIM-2026-051/052/062/063.json
CLM-005 | 1  | moderate   | CONS   | SUPPORTED in-window, selective       | SIM-2026-017-statistics.json
CLM-006 | 1  | near-zero  | CONS   | VOID as a control                    | SIM-2026-017-statistics.json
CLM-007 | 0  | n/a        | -      | SECTION-8 VIOLATION                  | (none)
CLM-008 | 1  | near-zero  | STRUCT | NOT ESTABLISHED                      | SIM-2026-011-interaction.json
CLM-009 | 2  | moderate   | -      | negative SOLID; verdict contradicted  | SIM-2026-010.json
CLM-010 | 1  | near-zero  | STRUCT | SUPPORTED as one-point agreement     | SIM-2026-025.json
CLM-011 | 1  | near-zero  | CONS   | NOT ESTABLISHED (2-pt degenerate)    | SIM-2026-025.json
CLM-012 | 1  | moderate   | PART   | CONTRADICTED BY OWN RECORD           | hyp010_criticality_scan.json
CLM-013 | 1  | near-zero  | CONS   | PROVISIONAL (correctly hedged)       | holographic_transport_24q.json
CLM-014 | 0  | n/a        | -      | NOT SUPPORTED by project record      | PAPER-2026-088.json
CLM-015 | 1  | near-zero  | -      | CORRECT (a definition, so labelled)  | SIM-2026-001.json
CLM-016 | 1  | near-zero  | ALG    | WEAKEST SURVIVING PAPER CLAIM        | effective_mass_analysis.json
CLM-017 | 1  | near-zero  | -      | NOT ESTABLISHED (51.5% gap)          | effective_mass_analysis.json
CLM-018 | 0  | n/a        | -      | UNSUPPORTED CHAIN OF IDENTITIES      | (none)
CLM-019 | 1  | near-zero / moderate | PART | SUPPORTED for class ID       | SIM-2026-052.json
CLM-020 | 1  | near-zero  | PART   | SUPPORTED for class ID               | SIM-2026-063.json
CLM-021 | 2  | moderate   | IND    | SOLID                                | SIM-2026-051.json
CLM-022 | 2  | moderate   | STRUCT | PLAUSIBLE, UNDERPOWERED              | SIM-2026-062.json
CLM-023 | 1  | near-zero  | STRUCT | SUPPORTED; band not derived          | SIM-2026-064.json
CLM-024 | 2  | near-zero / moderate | IND | SOLID                       | SIM-2026-061.json
CLM-025 | 2  | moderate   | -      | SUPPORTED as negative only           | SIM-2026-064.json
CLM-026 | 1  | near-zero  | ALG    | MISLABELLED (c ladder, not C_TTT)    | SIM-2026-067/068/069.json
CLM-027 | 2  | moderate-to-high | PART | PROMISING, UNGATED             | SIM-2026-068.json
CLM-028 | 2  | high       | -      | REAL NEGATIVE, obscured downstream   | SIM-2026-065/066.json
CLM-029 | 2  | moderate   | -      | SOLID (section-18 out-of-sample)     | SIM-2026-069.json
CLM-030 | 2/3| high       | PART   | SUPPORTED, robustly                  | SIM-2026-071.json
CLM-031 | 1/2| moderate   | STRUCT | NOT ESTABLISHED at quoted precision  | SIM-2026-071.json
CLM-032 | 0  | n/a        | -      | SECTION-8 VIOLATION                  | SIM-2026-071.json:22
CLM-033 | 1  | near-zero  | STRUCT | VALID but MISLABELLED; no raw data   | SIM-2026-071.json (only)
CLM-034 | 1  | near-zero  | PART   | SOLID (cleanest record in program)   | SIM-2026-070.json
CLM-035 | 2  | high       | PART   | SUPPORTED and honestly disclosed     | SIM-2026-071.json
CLM-036 | 1  | near-zero  | -      | TRUE BUT EMPTY as stated             | SIM-2026-071.json
CLM-037 | 2  | moderate   | -      | TRUE AND UNCLAIMED                   | qw_yanglee_ks.jl (derived)
CLM-038 | 2  | moderate   | -      | SUPPORTED; 3 reporting defects       | SIM-2026-008c.json
CLM-039 | 0  | n/a        | -      | NOT SUPPORTED (repeats ERRATA D5)    | SIM-2026-008c.json
CLM-040 | 2  | n/a        | -      | UNRELIABLE AS WRITTEN                | pytket_compilation_results.json
CLM-041 | 0  | n/a        | -      | NOT ESTABLISHED (the trunk question) | README.md:5
CLM-042 | 0  | n/a        | -      | SECTION-8 VIOLATION                  | README.md:197
```

---

## 5. UNVERIFIED

Items I could not confirm or refute. Silence is not a pass — each is open.

1. **What arXiv 2603.07639 (Wang & He) actually proves (CLM-014).** I checked only the project's
   record `PAPER-2026-088.json`. The paper is not in `research/downloads/`. DEF-03 is therefore
   "not supported by the project's own record", **not** "proved false". This remains the highest-value
   single item in the audit to close.
2. **Whether a §8 literature search would clear CLM-030/CLM-032/CLM-027.** I ran no external search.
   The recorded prior-art evidence *against* novelty (the vendored ZMV codebase already ships
   `OBF_Hn_MPO_split`, `potts3_Hn_MPO_split` and `Hn_in_basis`) bears on CLM-026, not on the
   biorthogonal extension. The novelty status of the three candidate contributions is **unknown**,
   not favourable.
3. **Whether the defects in the `.bib` reached the version PRD received.** I relied on
   `inv-manuscript-claims.md`, which audited the `.tex` (mtime 2026-07-21) and not the rendered
   `.bbl`. Submission was 2026-08-07.
4. **The provenance of the manuscript's transport peak `max|ρ| = 0.030`** where the record and the
   raw `.npy` both give 0.0467. No file containing 0.030 was located, so it is unclear whether this
   is transcription, a normalization, or a stale run.
5. **README's "41.2 % on IBM Heron"** matches no repository record I could find and disagrees with
   the manuscript's own 24.5 %. I did not locate its source.
6. **Whether the α = 3.92 ±0.16 was computed with per-point errors or unweighted.** `chi2` = 54.07
   with `chi2_reduced` = 6.01 implies *some* error model, but no record states it, so I can say the
   ±0.16 disagrees with the bootstrap but not which is defensible.
7. **The unitary control's raw output (CLM-033) does not exist in the repository.** Its numbers were
   verified only against downstream restatements of the same JSON field. The phase-1 pipelines
   auditor's independent Python/ARPACK reimplementation reproduced the *Yang-Lee* ladder and the
   control values to 6 decimals, which is reassuring but is that auditor's run, not the project's.
8. **Figure contents.** No PNG in the submission package was opened by any auditor. Figure 2's
   caption asserts "Five independent seeds converge to 3.33 %" (seed 13 is 4.30 %); Figure 6's
   asserts a fitted r^{−1/4} decay that exists in no record.
9. **Schema conformance of the 17 manuscript-cited SIM records** was not re-run. ERRATA D3 recorded
   9/36 valid at 2026-06-08; `inv-hypotheses.md` finds HYP conformance has since *degraded* to
   13/30, so the SIM figure is probably worse, not better.
10. **`research/data/theory/` is NOT empty** — contrary to the task brief it holds 8 prose files
    (`RUN-A-methods.md`, `epsilon-channel-proof.md`, `paper-review-synthesis.md`,
    `research-challenge.md`, `research-practical.md`, `research-primary.md`, `task4-ope-argument.md`,
    `task5-crofton-derivation.md`). The §14 defect is real but different from the one stated: there
    are **no structured theory records**, no schema, and no claim-dependency fields — so none of the
    dependency chains in §3.1 above exists anywhere in the repository except this artifact.
11. **Claim completeness.** 42 claims were extracted from the manuscript, the README, the hypothesis
    records and the SIM verdicts. Claims made only in `research/digests/`, `RESEARCH-LOG.md`, or the
    learning guides were not swept; `RESEARCH-LOG.md` is in any case frozen at 2026-07-21 and
    contains none of SIM-068/069/070/071.

