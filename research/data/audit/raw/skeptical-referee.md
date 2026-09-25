# Referee Report — "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits"

**Manuscript:** `research/submission-package/prd/paper-prd.tex` (714 lines, RevTeX 4.2, `aps,prd,twocolumn`)
**Journal / accession:** Physical Review D, `DV13971`, submitted 2026-08-07, "With editors"
**Author:** Jon Cackler (Independent Researcher, Ames, Iowa)
**Referee role:** `adv:referee` (RESEARCH-DIRECTOR §27 "Skeptical referee" — writes rejection-quality criticism)
**Date:** 2026-08-17
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` §5 (contribution levels), §6 (counterfactual
novelty), §7 (independence ledger), §8 (novelty gates), §12 (killer tests), §17 (beyond single-number
agreements), §19 (matched controls), §20 (uncertainty), §22 (adversarial numerical tests), §24 (PRD referee
prep / the "delete holographic" test), §38 (audit).

**Method note.** Every quantitative claim below was recomputed by this referee directly from the record
JSON in `research/data/simulations/`, not taken from any phase-1 artifact. Where a phase-1 auditor reached
the same conclusion independently that is noted, because independent convergence is evidence; where I
disagree with or extend phase 1 that is also noted.

---

## 0. RECOMMENDATION

> **REJECT.** Resubmission as a substantially different, retitled, and rescoped paper is invited.

**Three-sentence summary.** The manuscript's central claim — a measured force exponent
α = 3.92 ± 0.16 identified with stress-tensor exchange α = 2Δ_T = 4 — is an artifact of the fitting
procedure: 95.8 % of the least-squares weight in the recorded 11-point fit sits on the single data point
dr = 2, the exponent is essentially the two-point local slope between dr = 2 and dr = 3, and any
reasonable alternative analysis of exactly the same data (relative-error weighting, or excluding the one
point whose operator supports are bridged by a Hamiltonian bond) returns α ≈ 2.5–2.9, i.e. away from the
claimed value and toward the α = 2 the abstract says is excluded. Setting that aside, of the four
advertised results, two (α = 2Δ_T = 4; the null-crossing condition T = (π/2)·l_AdS) are fixed in advance
by conformal symmetry and by a two-line algebraic identity respectively and therefore have near-zero
counterfactual novelty, one (the recurrence of Δ_T ≈ 2 at tricritical Ising and three-state Potts) is a
reproduction of what Pfeifer–Evenbly–Vidal-style scaling-superoperator extraction has been doing since
2009, and only the two-phase ALM + projection optimizer and the "interaction energy, not ZZ correlator"
observable diagnostic are genuine, if modest, methodological contributions. Independently of all of this,
the manuscript contains at least six outright errors of fact — a claimed external analytic validation
that does not exist in the cited paper, a bibliography with four wrong author given-names and four wrong
titles, a sparse-matrix size wrong by 6×, an IBM comparison built from two wrong inputs, an Azure free-tier
figure overstated 20×, and a hardware protocol that cannot reach the observable it claims to measure —
any one of which, in my experience, ends a PRD submission on its own.

**What I would accept.** A rewritten methods paper about (i) the ALM + Z₂-projection optimizer, (ii) the
observable diagnostic (energy-based interaction vs. ZZ correlator), and (iii) the exact-diagonalization
pre-gate on blocked lattice operators, with the word "holographic" removed from the title and the α = 4
claim demoted from "central finding" to "pipeline validation consistent with the symmetry-fixed value."
That paper would be publishable in a good numerical-methods venue. It is not a PRD paper.

---

## 1. THE CENTRAL CRITICISM

> *Which results here are NOT fixed by conformal symmetry, standard Virasoro structure, or earlier
> tensor-network CFT work (Vidal 2007/2008, Evenbly–Vidal, Pfeifer–Evenbly–Vidal scaling operators,
> Zou–Milsted–Vidal)?*

I put this in its strongest form, because the manuscript itself hands me the argument.

### 1.1 The manuscript concedes the point in its own §6.5

> "Because the stress tensor has holomorphic–antiholomorphic conformal weight (2,0) ⊕ (0,2) in *every*
> unitary two-dimensional CFT, Δ_T = 2 is a **kinematic constant of conformal symmetry, independent of
> the central charge**." — `paper-prd.tex:427`

That sentence is correct, and it is fatal to the framing. If Δ_T = 2 is kinematic, then α = 2Δ_T = 4 was
known before a single line of code was run. Per §6 (counterfactual novelty), only two outcomes were
possible: the pipeline reproduces 4, or the pipeline is broken. The paper then advertises the recurrence
of 4 at three universality classes as the thing that "establishes" the result (`paper-prd.tex:457`,
`:531`, `:603`). Reproducing a kinematic constant at three fixed points is three implementation checks,
not three discoveries. This is a **Level 1** result under §5.

The same applies to the second headline. §3.3 derives T_predicted = (π/2)·l_AdS from
⟨P₁,P₂⟩ = −cos(Δt) − 1 and the null condition, which is two lines of embedding-space algebra
(`paper-prd.tex:150`; record `composite_geodesic_results.json` → `calculations.embedding_space`). π/2 is
not measured. l_AdS = 1/ln χ = 1/ln 2 is asserted by architecture — the manuscript says so itself: "This
value is set by the MERA architecture, not by optimization" (`paper-prd.tex:66`). So the *prediction* side
of the transport comparison contains no free parameter and no measurement; the entire empirical content of
Result 2 is a single number, T = 2.239, read off as the difference of two local extrema of a boundary
density trace.

Likewise C_σσε = 1/2 (§8.5, `paper-prd.tex:573`) has been exactly known since Belavin–Polyakov–Zamolodchikov
1984; C_εεT = 2Δ_ε/c = 4 at c = 1/2 (`paper-prd.tex:567`) is a Ward identity the manuscript writes down
itself; ε × ε = [1] is a textbook fusion rule cited to Di Francesco.

### 1.2 What earlier tensor-network CFT work already did

The manuscript's spectral results are, mechanically, the standard scale-invariant-MERA scaling-operator
extraction. Reading Δ = −log₃ λ from the eigenvalues of the ascending scaling superoperator
(`paper-prd.tex:434`) **is** the Pfeifer–Evenbly–Vidal 2009 procedure, which the manuscript itself cites
at `paper-prd.tex:573` for the OPE extraction. Evenbly–Vidal (PRB 81, 235102) established that a critical
MERA reproduces the Ising operator tower including Δ_T = 2; extracting a minimal-model tower at
c = 7/10 and c = 4/5 with symmetric (Z₂/Z₃) MERA is the natural, expected continuation, not a new
capability. Nothing in §6.5 identifies what this work does that Pfeifer–Evenbly–Vidal, Evenbly–Vidal, or
the Z_N-symmetric MERA literature does not.

**And the manuscript's own repository has no record for any of this prior art.** I checked
`research/data/papers/`: grepping the 139 catalogued paper records for `evenbly|pfeifer|milsted|zou|
koo.saleur` returns exactly one file — `PAPER-2026-010.json`, the Wang–He paper — and it is not about any
of them. There is **no catalogued record for Vidal 2007, Evenbly–Vidal 2010, Evenbly–Vidal 2011,
Pfeifer–Evenbly–Vidal 2009, or Zou–Milsted–Vidal 2020.** A paper whose entire technical apparatus is
built on a literature it has not catalogued cannot claim to have cleared §8's prior-art gate, and in fact
the manuscript makes five explicit priority claims with no recorded prior-art evidence at all:

| # | Priority claim | Location |
|---|---|---|
| 1 | "the **first** holographic force measurement from an optimized tensor network state" | Abstract `:29`; §6.4 `:420`; §9 `:609` |
| 2 | "a dynamical test of the emergent geometry **has not been performed** at sub-percent precision" | §1 `:43` |
| 3 | ALM "**have not been applied** to quantum variational circuits with discrete symmetry constraints" | §2.2 `:83` |
| 4 | "introduces holographic transport as a **novel observable**" | §7.2 `:490` |
| 5 | "provide the **first** N = 24 measurement" | §7.4 `:556` |

Claims 1 and 4 are self-contradicted inside the manuscript: §7.4 (`:556`) credits Wang & He with
*discovering* holographic transport, and §7.4 (`:552`) credits Sahay–Lukin–Cotler with *demonstrating*
hologron forces in classical MERA simulation. This is a direct §8 violation and, at PRD, a referee-visible
credit problem.

### 1.3 The honest residue

After removing everything fixed by symmetry, by algebra, or by prior tensor-network work, what remains is:

| Survives | Level (§5) | Comment |
|---|---|---|
| Two-phase ALM + Z₂-projection optimizer reaching 3.33 % at 24 q where projection-cold-start reaches 4.31 % and penalty fails | **2** | Real optimizer result with seed spread. The most defensible thing in the paper. |
| The observable diagnostic: ZZ-correlator change collapses to −C_vac under boundary-primary excitation; energy-based F(dr) does not | **2** | A genuine, well-documented negative-then-positive methodological finding (`SIM-2026-010.json` → `V_dual` ≈ −`C_vac` to 3–4 digits at every dr). |
| ED pre-gate on the blocked O'Brien–Fendley operator (max\|H − H_block\| = 1.1e−16) and on the Z₃-graded Potts Hamiltonian (1.75e−15) before trusting the MERA | **2** | Correct practice, and the sort of thing that should be foregrounded, not buried. |
| Everything else | **1 or 0** | Validation, algebra, or interpretation. |

Two Level-2 method notes and a validation suite is not a PRD paper. It is a good *Physical Review E* /
*SciPost Physics Codebases* / *Quantum* methods paper with a different title.

---

## 2. CLAIM-BY-CLAIM: KNOWN / EXPECTED / GUARANTEED / MEASURED

Format per §24. "Guaranteed" means fixed before the calculation by symmetry, algebra, or convention.

### C1 — α = 3.92 ± 0.16 identified with stress-tensor exchange (the stated central finding)

- **Known:** ⟨TT⟩ ∼ x⁻⁴ in every 2D CFT. The project's own `SIM-2026-014.json` → `key_finding` says this
  follows "exactly from conformal symmetry."
- **Expected:** α → 4 asymptotically *if* the propagating channel is the identity/stress-tensor block.
- **Guaranteed:** the *target value* 4. Nothing about whether a 24-site OBC lattice observable would
  display it.
- **Measured:** F(dr) at 12 separations on the exact 24 q ground state
  (`SIM-2026-011-interaction.json` → `F_interaction_avg`), fitted over dr ≥ 2.
- **Verdict: the measurement does not support the claim.** Detailed in §3 below. **This is the single
  item that decides the paper.**

### C2 — "Three consistent evaluations" α = 3.92 / 3.97 / 4.07

- **Known / Guaranteed:** as C1.
- **Measured:** three fits.
- **Verdict:** not independent, and the manuscript knows it. §6.5 (`:427`) states correctly that "the
  three force measurements above all sample the same conformal fixed point." §5.3 (`:327`) and the
  Abstract call the same three numbers "independently confirmed" / "three consistent evaluations." Both
  framings appear in one paper. Independence ledger in §4 below. Additionally the three numbers move
  *together* under the same analysis perturbation (§3.4), which is the signature of a shared systematic,
  not of independent agreement.

### C3 — Universality of α = 4 at c = 7/10 and c = 4/5

- **Known:** Δ_T = 2 in every unitary 2D CFT.
- **Guaranteed:** the value.
- **Measured:** Δ_T from the ascending superoperator spectrum — **not** a force.
- **Verdict: the α column of the universality table (`paper-prd.tex:441–445`) is a derived column typeset
  in bold beside measured quantities.** No F(dr) was computed at TCI or Potts. The manuscript concedes
  this in Open Question 4 (`:592`: "The transport and force-profile measurements, however, have been
  performed only at c = 1/2") and then does not carry the concession into the abstract, table, or
  conclusion. A referee reading only the abstract will believe forces were measured at three fixed points.
- **Additional problem with the control row.** The row labelled "Ising, c = 1/2 (control, λ₃ = 0)" gives
  (Δ_σ, Δ_ε, Δ_T) = (0.125, 1.00, 1.998). I read the records: `SIM-2026-051.json` →
  `control_lam3_0.best_seed` = (0.1402, 0.9882, 1.9921); `SIM-2026-050.json` → `results.seed1` =
  (0.12515, 1.0175, 1.998). **No record anywhere gives Δ_ε = 1.00** — that is the exact CFT value.
  The published control row is therefore assembled from two different runs plus one exact value.
- **Δ_σ = 0.092 vs. CFT 0.075 is a 22.7 % error** presented in a table of agreements with no error bar
  (`SIM-2026-052.json`; the record itself is franker — "now within 22 % of CFT"). Calling this "recovers
  the **full** M(4,5) primary spectrum" (Abstract) is wrong twice over: three primaries are reported, and
  the record's own `cft_targets_TCI_M45` lists σ′ (0.875) and ε′ (1.2), neither reported.
- **Basin selection.** The χ = 12 Potts headline rests on 2 of 6 optimizations (`SIM-2026-063.json` →
  χ = 12 clean-basin rate), selected by a spectral gate; the manuscript quotes the 4/6 rate at χ = 6 and
  not the 2/6 rate at χ = 12, and the abstract reports the midpoint of the two surviving basins as if it
  were a single measurement. §36 (prediction registry) and §20 (formalize uncertainty) are both violated.

### C4 — Transport T = (π/2)·l_AdS to 1.2 % at N = 16

- **Known / Guaranteed:** π/2 (embedding-space null condition, two lines); l_AdS = 1/ln 2 (architecture).
- **Measured:** T = 2.239 from the fine-dt re-run (`SIM-2026-025.json` → `runs.N16.T_measured_refined`).
- **Credit where due:** the ERRATA-E2 self-retraction (the published 0.72 % was a dt = 0.05 grid artifact;
  the true residual is −1.21 %) is handled correctly and prominently, and the N = 24 double-lobe exclusion
  is disclosed. **This is the most honest passage in the paper and I want it on the record.**
- **Verdict: undermined by the manuscript's own unreported control.** See §4.2. Also, the "residual
  shrinks with system size" claim is a **two-point** trend whose own record says
  `fit_1overN.note`: "2-point fit is algebraically exact but degenerate — cannot distinguish 1/N from
  1/N²", with a non-zero intercept b = +0.0796 indicating "mixed functional form, not clean 1/N scaling."
  None of that reaches the manuscript. §17 (move beyond single-number agreements) is not satisfied.

### C5 — m_eff 0.693 (CFT) vs 0.670 (MERA), "3.5 % agreement"

- **Known / Guaranteed:** 0.693 = ln 2 = 1/l_AdS exactly, obtained by putting Δ = 1 into
  m²l² = Δ(Δ−2) = −1 (`effective_mass_analysis.json` → `ads_mass_dimension.epsilon_m_eff` = 0.6931;
  ERRATA §E4 states this). It is an algebraic identity, not a prediction.
- **Measured:** 0.670, from ξ_2pt = 2.154, which is a **two-point** estimate V(dr=1)/V(dr=2) taken on the
  χ = 2 SIM-2026-002 state — the very state the same manuscript describes as having "flat correlations
  (wrong universality class)" (Fig. 6 caption).
- **Verdict:** a two-point ratio on a disqualified state compared against an exact constant. The
  manuscript's §8.6 downgrade ("preliminary diagnostic … only 2 signal points and a post-hoc fit") is
  correct and should be the *only* place this appears. It should not be in the Conclusion (`:612`).
- Note the input record `worldline_mc_results.json` fails its own validation
  (`mc_validation.mc_quality`: "POOR: slope = 26.337 != 1.0 … the MC does not correctly estimate relative
  K values") and contains a literal `NaN` (ERRATA §D2). The file the data-availability appendix advertises
  as "Camporesi–Higuchi validation" contains no usable worldline Monte Carlo result.

### C6 — Two-phase ALM + Z₂-projection (1.12 % @ 8 q, 3.33 % @ 24 q)

- **Known:** ALM is textbook (Nocedal–Wright, correctly cited).
- **Measured:** yes, genuinely. `SIM-2026-008b-8q-test.json` → `best_error_pct` = 1.1150;
  `SIM-2026-008c.json` → `best_error_pct` = 3.33399, five seeds.
- **Verdict: the paper's best result, and it is buried.** Two problems remain.
  (a) "all five seeds converge to 3.33–3.34 % … with P = 1.000 **throughout**" is false for Phase 1:
  the record's `phase1_P` values are 1.48e−6, 1.50e−6, 5.81e−7, −1.56e−10, 1.31e−6, and `phase1_err`
  runs 3.36–5.24 %. Appendix B's "typical Phase 1 energy 8.2 % with ⟨P⟩ > 0.999999" is the **8-qubit**
  number placed in a 24-qubit appendix (`SIM-2026-008b-8q-test.json` → `alm_err` = 8.2349).
  (b) "The 3.33 % floor is a circuit expressibility ceiling … **regardless of optimizer**" is five seeds
  of one optimizer family, and it is precisely the inference the project's own ERRATA §D5 retracted:
  `SIM-2026-036`'s identical "bond-dimension ceiling" verdict was later shown (SIM-039/040) to be a
  gradient-engine plus wrong-sector-objective artifact. No entanglement or overlap gate on the χ = 2
  N = 24 state is reported.

### C7 — χ = 3 overcomes the expressibility barrier (0.15 % at 16 q)

- **Measured:** `SIM-2026-015c.json` → `best_error_pct` = 0.15126. **Single seed (42).** No basin control.
- The N = 8 comparison table (`paper-prd.tex:365–369`) has a χ = 2 column with **no record**:
  `SIM-2026-008b-8q-test.json` — the source of that column's 1.12 % — contains no correlator and no
  entropy fields at all. The "0.70 (flat)" values in a table headed "Results at N = 8" are the N = 24
  numbers from `SIM-2026-006.json`, where they actually span 0.62–0.83, not "flat at 0.70". "S(4) ~0.30"
  matches no record at any N. I verified this by listing the JSON keys.
- "⟨P⟩ = 1.000" at N = 16 (`paper-prd.tex:383`) has no parity field in `SIM-2026-015c.json`.
- "C(r) ~ r^{−1/4}" is asserted; no fitted exponent exists in any record.

### C8 — C_σσε = 0.50 ± 0.03

- **Known:** exactly 1/2 since BPZ 1984. Counterfactual novelty zero.
- **Measured:** yes, and the structural gates (C_σσσ = 0 exactly, symmetry covariance at 1e−16) are good
  practice.
- **Verdict: the uncertainty is not what the record says.** The record's own prescription is a
  placement-average of 0.4722 and 0.5146 (`SIM-2026-064.json` → `drift_resolution_2026_07_08`), which is
  **0.493 ± 0.021**, not 0.50 ± 0.03. More seriously, the record's `verdict` is "PRECISION ACHIEVED,
  **ACCURACY PUZZLE FLAGGED**": the single-placement mean runs 0.5075 → 0.5069 → 0.4957 → 0.4722 with
  increasing χ, i.e. it *crosses and undershoots* the exact value rather than converging to it, and the
  record's own third suspect (a genuine finite-χ turnaround by χ ≈ 16–22) "remains untested." None of
  that adverse structure appears in the manuscript, which presents a clean agreement with 1/2 in the
  Conclusion.

### C9 — Hardware path: Helios, 57 CNOTs, 0.57 %

- **Measured:** the two numbers check out (`pytket_compilation_results.json` → `zzphase_count` = 57;
  `error_budget.original_pct` = 0.5684).
- **Verdict: the section is not usable as written.** Six defects, itemised in §5. Most importantly the
  project's own feasibility study, `SIM-2026-019.json`, has verdict **PARTIALLY_REFUTED** with
  `correction`: "For 4-point α fit, fidelity threshold is ~99.97–99.99 % per gate (not 99.5 %).
  **Helios is insufficient for power-law detection.**" That sentence appears nowhere in the manuscript,
  whose abstract says only "A hardware path is designed for Quantinuum Helios." §38.A.12 ("which important
  negative results are not yet surfaced clearly?") is squarely violated.

---

## 3. THE α = 3.92 RESULT IS A FITTING ARTIFACT

This section is the reason for the recommendation. Everything here I recomputed myself from
`research/data/simulations/SIM-2026-011-interaction.json` → `F_interaction_avg` and
`SIM-2026-015d.json` → `exact.V_data` / `mera.V_data`.

### 3.1 One point carries 95.8 % of the fit

The recorded fit is an unweighted least squares of F(dr) = A·dr^(−α) in **linear** space over
dr = 2…12. F falls by 2.4 decades across that window. The share of total squared signal per point is:

| dr | 2 | 3 | 4 | 5 | 6 | 7 | 8 | 9 | 10 | 11 | 12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| share of ΣF² | **0.958** | 0.031 | 0.0069 | 0.0023 | 0.0009 | 0.0004 | 0.0002 | 0.0001 | 0.0001 | 0.0000 | 0.0000 |

The fit is, to three significant figures, a two-point determination using dr = 2 and dr = 3. The local
logarithmic slope between exactly those two points is **4.2315**. The reported α is **3.9218**. Nine of the
eleven "data points" contribute 1 % of the information.

### 3.2 The data contain no power-law plateau

Local slopes −ln(F_{i+1}/F_i)/ln(dr_{i+1}/dr_i), computed by me from the record:

| interval | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 | 10→11 | 11→12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| 24 q exact | 2.035 | **4.232** | 2.603 | 2.456 | 2.461 | 2.533 | 2.658 | 2.841 | 3.102 | 3.482 | 4.064 |
| 16 q exact | 2.10 | **4.24** | 2.74 | 2.64 | 2.71 | 2.88 | 3.16 | 3.65 | 4.52 | 6.33 | — |
| 16 q χ=3 MERA | 2.10 | **4.40** | 2.37 | 2.58 | 3.61 | 3.76 | 6.02 | 8.44 | 11.30 | −7.44 | — |

A genuine F ∼ dr⁻⁴ gives ≈ 4 at every interval. What is actually there is a single 4.2–4.4 spike at
dr = 2 → 3, a flat region at **2.45–2.66** through the middle of the range, and an upward drift at the
chain ends where OBC contamination is largest. The 16 q χ = 3 MERA tail is not data at all — it changes
sign twice and reaches a "local slope" of 11.3 and −7.4.

This is a stronger statement than "the error bar is too small." **There is no power law in this data set
to have an exponent of.**

### 3.3 The mechanism, and why dr = 2 is special

§5.3 excludes dr = 1 as "dominated by direct exchange." The same argument applies at dr = 2 and the
manuscript does not make it. The boundary-primary operator (Eq. 7) has support on two sites, {j, j+1}.
With anchor a = 6:

- dr = 1: supports {6,7} and {7,8} **overlap**.
- dr = 2: supports {6,7} and {8,9} do not overlap, but the Hamiltonian bond Z₇Z₈ **bridges them**.
- dr ≥ 3: supports {6,7} and {9,10}… no single nearest-neighbour H term connects the two supports.

dr = 2 is therefore the unique separation at which a Hamiltonian term directly couples the two operator
supports — i.e. it carries a contact/direct-exchange contribution that is structurally absent at every
larger separation. It is also the point that carries 95.8 % of the fit weight. The paper's headline
exponent is set by the one point its own stated exclusion criterion should have removed.

### 3.4 Any reasonable alternative analysis destroys the result

All computed by me on the recorded arrays, same model A·dr^(−α), no other change:

| Analysis choice | 24 q exact | 16 q exact | 16 q χ=3 MERA |
|---|---|---|---|
| **As published** (linear LSQ, dr ≥ 2) | **3.922 ± 0.159** | **3.975 ± 0.145** | **4.071 ± 0.178** |
| Relative-error weighting, same dr ≥ 2 window | **2.822** | — | — |
| Unweighted log–log regression, same window | **2.890** (R² = 0.992) | — | — |
| Drop dr = 2 (dr ≥ 3) | 2.559 ± 0.019 | 2.753 ± 0.035 | 2.715 ± 0.143 |
| dr ≥ 4 | 2.534 ± 0.038 | 2.801 ± 0.076 | 3.236 ± 0.224 |
| dr ≥ 5 | 2.621 ± 0.058 | 2.992 ± 0.121 | 4.083 ± 0.261 |
| Record's own fit over **all** dr (1…12) | **2.296 ± 0.105** | — | — |

Three observations a referee cannot get past:

1. **No data are discarded to break the result.** Merely changing from absolute to relative error
   weighting — the physically appropriate choice for a positive quantity spanning three decades, and the
   choice implicit in any log-log presentation such as Fig. 4 — moves α from 3.92 to **2.82**, without
   touching a single point.
2. **The window systematic is ~8× the quoted uncertainty**, in the same direction, in all three datasets,
   and it is quantified nowhere in the manuscript or the records. Per §20 this is a systematic that
   dwarfs the reported statistical error and it is simply absent.
3. **The alternative value is not random.** ~2.5–2.9 is closer to α = 2 than to α = 4, and α = 2 is the
   value the abstract says the data exclude. §20's test — "would the conclusion survive a reasonable
   alternative analysis pipeline?" — is failed, and failed in the direction that reverses the physics
   conclusion.

### 3.5 The quoted uncertainty is not a calibrated 1σ, and the project knows this

`SIM-2026-017-statistics.json`, which is cited nowhere in the manuscript and is absent from the
data-availability appendix, contains:

- `power_law_fit.statistics.chi2_reduced` = **6.008** on dof = 9 (p ≈ 1e−7). By the fit's own error model
  it is a **rejected fit**. Neither paper version contains any χ² for it — I grepped both.
- `bootstrap`: `alpha_mean` = **3.369**, `alpha_std` = **0.6335**, 95 % CI [2.520, 4.192].

The manuscript quotes the CI (favourable — it contains 4) and never the σ or the mean (not favourable).
Under ±0.16, "inconsistent with scalar exchange (α = 2)" reads as a 12σ exclusion. Under the project's own
bootstrap σ it is ~2.2σ, and the bootstrap central value 3.369 is itself 1.0σ from 4 and 2.2σ from 2 —
i.e. the data do not decisively prefer either channel. **Selecting the favourable half of one's own
statistics record, and omitting that record from data availability, is the kind of thing that ends
referee goodwill.**

### 3.6 The χ = 3 MERA "evaluation" fits points of the wrong sign

`SIM-2026-015d.json` → `mera.V_data` contains **+0.0012015** at dr = 9 and **+0.00036517** at dr = 10,
inside a fit window declared `fit_dr_min: 2`, `fit_n_pts: 10`, `sign: −1`. Two of ten fitted points have
the wrong sign for the model. The manuscript discloses the sign flip as "noise at large separation"
(`:422`, honest) but does not state that the flipped points are **inside** the fit. Its own follow-up
record `SIM-2026-023.json` silently re-fits the same data over `fit_window: [2, 6]`, which excludes them,
without explanation.

### 3.7 A competing physical explanation the manuscript never addresses

The manuscript's α = 4 argument requires the excitation to be **ε** (Δ = 1), because ε × ε = [1] leaves
the stress-tensor block as the leading channel. Eq. (7) nevertheless names the operator **σ_j** and cites
it to "Zou–Milsted–Vidal, Boundary operators in MERA."

The project's own catalogued record of the actual source disagrees. `research/data/papers/PAPER-2026-010.json`
(Wang & He, arXiv 2501.03084) → `key_claims`:

> "Stable bulk quasiparticles are |Ψ_j⟩^σ = U† σ^boundary_j U |GS⟩, where **σ^boundary_j is the lattice
> realization of the CFT spin primary operator**"
> "σ^boundary_j = **V†** [0.635(X_j + X_{j+1}) − 0.026(X_jZ_{j+1} + Z_jX_{j+1})] **V**"

So (a) the coefficients 0.635 / −0.026 come from Wang & He, not Zou–Milsted–Vidal (for whom no repository
record exists at all); (b) Wang & He identify the operator as the **spin** primary σ (Δ = 1/8), not ε; and
(c) the manuscript **drops the V†…V conjugation** and applies coefficients derived for
H_boundary = (JL/4π)Σ(X_{j−1}Z_jX_{j+1} − X_jX_{j+1}) to a *different* Hamiltonian, the plain critical
TFIM with open boundaries.

If the excitation is σ, the fusion is σ × σ = [1] + [ε], the leading non-identity channel is ε with
Δ_ε = 1, and the predicted exponent is **α = 2Δ_ε = 2** — precisely the value the manuscript says its data
exclude, and within striking distance of the α ≈ 2.3–2.6 that the data actually give once the contact
point is removed. I am not asserting that σ is the right identification; I am asserting that **the
manuscript has not established which it is**, that its own cited source says the opposite of what it
assumes, and that the alternative identification predicts the exponent the data actually show. §5.3
admits the underlying weakness ("the identification of the propagating degree of freedom … rests on the
exponent matching and requires further theoretical justification"); §8.5 then claims to have "resolved"
it (`:571`) using a symmetry argument that presupposes the identification. That is circular.

I also note that as written the Eq. (7) operator is not a parity eigenstate of P = Π X: the
0.635(X_j + X_{j+1}) piece is P-even and the 0.026(X_jZ_{j+1} + Z_jX_{j+1}) piece is P-odd. In the plain
TFIM frame the manuscript actually uses, the operator is therefore a *mixture* of channels, which no
part of the paper acknowledges. Whatever the correct resolution, the paper needs one before it can claim
a channel.

---

## 4. INDEPENDENCE ATTACK (§7)

The manuscript's persuasive force rests on repeated claims of agreement between quantities the reader is
invited to treat as independent. They are not.

### 4.1 The three α evaluations — structurally dependent

| | 24 q exact | 16 q exact | 16 q χ=3 MERA |
|---|---|---|---|
| Model | critical TFIM, OBC | critical TFIM, OBC | *same 16 q Hamiltonian*, variationally approximated to 0.15 % |
| State source | `eigsh` | `eigsh` | MERA optimized to the same H |
| Observable | F = E_dual − E₀ − 2ΔE_single | identical | identical |
| Operator | Eq. (7), α = 0.635, β = −0.026 | identical | identical |
| Fit model & window | A·dr^(−α), dr ≥ 2 | identical | identical |
| Analysis code path | same | same | same |
| Independent information | — | one extra system size | one variational approximation of a state already in column 2 |

**Classification (§7): structurally dependent / primarily a consistency check.** Two of the three share
the *same ground state*, one exactly and one as a 0.15 %-error approximation of it. The empirical
demonstration that this is not independence is §3.4: perturb the shared analysis choice and all three
numbers move together, by ~1.2–1.4, in the same direction. Three evaluations that fail together are one
evaluation.

### 4.2 Transport — the manuscript's own control refutes its specificity claim

§3.4 claims: "The MERA transport time T = 2.25 is **uniquely consistent** with the AdS null geodesic
formula" (`:181`), supported by (i) a plain TFIM ring giving T = 3.8 and (ii) a seven-value coupling scan
giving T = 3.45–5.2 "in a non-systematic pattern."

I read the record, `research/data/simulations/hyp010_criticality_scan.json`. Two problems, both severe.

**(a) The "non-systematic pattern" is strictly monotone.** `approach_B_tfim.results`:

| g | 0.75 | 0.85 | 0.90 | 0.95 | 1.00 | 1.05 | 1.10 |
|---|---|---|---|---|---|---|---|
| T | 5.20 | 5.10 | 5.00 | 4.00 | 3.80 | 3.55 | 3.45 |

Monotonically decreasing in g, without exception. The manuscript's characterisation contradicts its own
data, and the correct characterisation is much worse for the argument: T is a *smooth decreasing function
of the coupling*, so hitting 2.266 is a question of where on that curve one lands, not of a geometric
mechanism. Linear extrapolation of the last three points reaches 2.266 near g ≈ 1.4.

**(b) The same record contains a control on the *same* Hamiltonian that the manuscript never mentions.**
`approach_A_wang_he_detuning` — the Wang–He boundary H plus a small mass detuning δΣZ_i:

| δ | −0.3 | −0.2 | −0.1 | **0.0** | +0.1 | +0.2 | +0.3 |
|---|---|---|---|---|---|---|---|
| T | 2.00 | 1.95 | 1.70 | **2.25** | 3.30 | 2.10 | 0.55 |
| residual | −11.7 % | −14.0 % | −25.0 % | **−0.7 %** | +45.6 % | −7.3 % | −75.7 % |

A 10 % detuning of the *identical* boundary Hamiltonian moves the transport time by −25 % or +46 %, and
the sequence is not even monotone — it swings from 0.55 to 3.30. This is the §12 killer test for the
transport claim, it was performed, it was recorded, and it is absent from the manuscript. Its correct
reading is that T is a sharply model-dependent, non-monotone functional of the Hamiltonian which happens
to pass through 2.25 at δ = 0; the paper's control (a *different* Hamiltonian giving a *different* number)
does not establish geometric specificity when the *same* Hamiltonian, barely perturbed, gives numbers
spanning the whole range including the one being celebrated.

I would also note that "T" here is the difference of two grid-quantized local extrema of a boundary
density trace, identified by eye. In the detuning table the dip time itself wanders from 2.15 to 3.65.
The N = 24 companion was excluded by the project's own follow-up because the trace has a double-lobe
structure making that identification unreliable (`SIM-2026-025.json` → `runs.N24.exclusion_reason`:
"two overlapping perturbation lobes … **clearly not** the holographic transport signal"). If the
identification is unreliable at N = 24, its reliability at N = 16 needs to be *demonstrated*, not assumed.

**Independence classification for the transport comparison: primarily a consistency check with one
tuned scale.** Side A (prediction) = π/2 × 1/ln 2, both fixed by convention/architecture. Side B
(measurement) = one number from one trace. Shared: the Wang–He construction, the MERA architecture that
sets l_AdS. Genuinely independent information: essentially none. A beautiful agreement between an
architecture-defined constant and a single extremum-difference is not strong evidence.

### 4.3 m_eff — algebraically the same input on both sides

- Side A: m_eff = √|Δ(Δ−2)| / l_AdS with Δ = 1 ⟹ 1/l_AdS = ln 2 = 0.693. **This is 1/l_AdS by
  construction**; it contains no information beyond "Δ_ε = 1" and "l_AdS = 1/ln 2".
- Side B: 0.670 from ξ_2pt = 2.154, itself a *ratio of two numbers* V(1)/V(2) taken on the χ = 2 MERA
  state whose correlations this same paper elsewhere calls flat and of the wrong universality class.

Both sides descend from the same CFT input (Δ_ε = 1) and the same architectural constant. **Classification:
algebraically equivalent on the theory side, uncontrolled on the measurement side.** A 3.5 % agreement
between an identity and a two-point ratio is not a check of the worldline–MERA dictionary. The project's
own `research/data/theory/research-challenge.md:99-103` reaches the same conclusion independently:
"post-hoc rationalization, not a prediction … The 'agreement' was found, not predicted." I agree with the
project's internal critic and not with the manuscript.

### 4.4 Nothing in this paper is a single end-to-end pipeline

Result 1 (force) is on an exact `eigsh` ground state. Result 2 (transport) is on the analytical
Evenbly–White MERA with a Wang–He boundary Hamiltonian — the manuscript correctly and commendably
discloses this at §3.1 (`:119`). Results 3 and 4 are on VQE / χ = 3 optimized states. The universality
results are on scale-invariant ternary MERA in the thermodynamic limit. **Five different states, four
different Hamiltonians, one narrative.** The abstract's framing sentence — "four results from classical
simulation of critical transverse-field Ising model chains on up to 24 qubits" — does not describe half
its own content: TCI and Potts are neither TFIM nor 24-qubit chains.

---

## 5. OUTRIGHT ERRORS (as distinct from overclaims)

These are not matters of interpretation. Each is a statement that is false, verifiable against the
project's own records or against arithmetic.

| # | Error | Where | Evidence |
|---|---|---|---|
| **E-1** | **A claimed external analytic validation that does not exist.** "Wang and He recently **proved** the null geodesic formula t_trans = π analytically in the continuum limit." `WangHe2026` = arXiv 2603.07639, whose project record `research/data/papers/PAPER-2026-088.json` is titled "Black-Hole Signatures in the **Finite-Temperature** Critical Ising Chain" and whose abstract and six `key_claims` contain no analytic proof and no "t_trans = π". This is the manuscript's **only** claim of third-party confirmation and it appears **three times**, including in the Conclusion. It is also unreconciled with §3.3, which *rejects* T = π·l_AdS = 4.53 as the wrong formula. | §3.5 `:206`; §7.2 `:538`; §9 `:605` | `PAPER-2026-088.json` |
| **E-2** | **Bibliography with four wrong author given-names and four wrong titles.** `Anand2023` → "Natalie Anand", "MERA on a Trapped-Ion Quantum Computer", PRX Quantum; record: **Sajant** Anand, Hauschild, Zhang, Potter, Zaletel, "Holographic quantum simulation of entanglement renormalization circuits", arXiv 2203.00886. `BohraSivaramakrishnan2025` → "Kausik Bohra, Mythili Sivaramakrishnan", "Composite geodesics in AdS spacetimes"; record: **Hardik** Bohra, **Allic** Sivaramakrishnan, "Composite AdS geodesics for CFT correlators and timelike entanglement entropy". `Roux2026` → "**Antoine** Roux"; record: **Jean-Baptiste** Roux, and the title is altered. `SahayLukinCotler2025` → "Holographic forces in tensor networks", PRX 15 021078; record: "**Emergent Holographic Forces from Tensor Networks and Criticality**", arXiv 2401.13595. Wrong *given names* in four independent entries is not a typo pattern. Any referee who knows one of these authors will see it in ten seconds. | `references.bib` L53–60, 70–76, 78–84, 117–122 | `PAPER-2026-009/017/020/023.json` |
| **E-3** | **Sparse-matrix size wrong by a factor of 6.** "nnz = N·2^N/3 (≈805 million at N = 24)". 24 × 2²⁴ / 3 = **134,217,728**. 805,306,368 = 48 × 2²⁴. Formula and number cannot both be right. | App. C `:671` | arithmetic |
| **E-4** | **IBM comparison: two wrong inputs, coincidentally plausible output.** "IBM Heron r3 (156 qubits, **99.5 %** CX fidelity) accumulates **24.5 %** error **on the same circuit**." Record: fidelity **99.8 %**, and 24.5 % = 1 − 0.998^**140**, i.e. a 140-CNOT circuit, not the 57-gate circuit just described. Correctly: 1 − 0.998⁵⁷ = **10.8 %**. | §7.1 `:478` | `helios-mera-design.md` L369, L473 |
| **E-5** | **Azure free-tier overstated 20×.** "800 free Hybrid Quantum Credits for new accounts." Record: free credits = "$500 = **40 HQCs**"; 800 HQC corresponds to a **$10,000** Azure Quantum Credits grant. | §7.2 `:487` | `helios-access-research.md` L15, L156, L163 |
| **E-6** | **Stated HQC cost formula is not the record's formula and does not reproduce the record's worked example.** Manuscript: HQC = shots × (5 + n_2q/10). Record: HQC = 5 + C × (N_1q + 10·N_2q + 5·N_m)/5000, whose worked example gives 280,000 shots → 115,925 HQC; the manuscript's formula gives 5.3 M. | §7.2 `:488` | `helios-access-research.md` L28, L47–51 |
| **E-7** | **The proposed experimental protocol cannot measure its own observable.** "Measure boundary spin density at discrete time points (**15–20 steps, dt = 0.05**)." That covers t ∈ [0, 1.0]. The dip is at t = 2.50 and the reappearance at t = 4.75. The protocol as specified never reaches either of the two features whose difference *is* T. The reference simulation used 120 steps. | §7.3 `:500` | `holographic_transport.json` → `time_evolution.n_steps` = 120 |
| **E-8** | **"P = 1.000 throughout" is false for Phase 1** (record `phase1_P` = 1.48e−6, 1.50e−6, 5.81e−7, −1.56e−10, 1.31e−6), and Appendix B's "typical Phase 1 energy 8.2 %" is the 8-qubit number placed in the 24-qubit appendix (24 q Phase 1 errors are 3.36–5.24 %). | §2.2 `:93`; App. B `:663` | `SIM-2026-008c.json`, `SIM-2026-008b-8q-test.json` |
| **E-9** | **A main-text quantitative claim rests on a record that does not exist.** "All seeds at N = 24 remain at ⟨P⟩ = 0 with 4–5 % energy error" — `SIM-2026-007.json` does not exist; ERRATA §E3 records the JSON was lost on RunPod teardown. The caveat is placed only in an appendix table row; the main-text assertion carries none. | §2.2 `:81` | `research/ERRATA.md` §E3, §D1 |
| **E-10** | **A table headed "Results at N = 8" contains N = 24 numbers and one number with no record.** χ = 2 column: C(1) = C(4) = "0.70 (flat)" and S(4) ≈ 0.30. `SIM-2026-008b-8q-test.json` has no correlator or entropy fields; the 0.70 values are the N = 24 numbers, which actually span 0.62–0.83; S(4) ≈ 0.30 matches no record at any N. | §6.2 table `:365–369` | JSON key listing |
| **E-11** | **Universality control row assembled from two runs plus one exact value.** See §2/C3 above: Δ_ε = 1.00 in a row of measurements is the CFT value, present in no record. | §6.5 table `:441` | `SIM-2026-051.json`, `SIM-2026-050.json` |
| **E-12** | **Transport peak amplitude disagrees with the record by 36 %.** Manuscript "max\|ρ\| = 0.030" at t = 0.70, twice. Record `peak_amplitude` = **0.046672**. | §3.2 `:135`; App. D `:680` | `hyp010_criticality_scan.json` → `approach_A_wang_he_detuning.results[3]` |
| **E-13** | **Symbol collision that will actively mislead.** L = MERA layers in §2.1 (L = 3, 5) and L = number of sites in §3.5's "T·L" table (L = 16, 24). A referee reading T·L = 36 will first try 2.25 × 3. | §2.1 `:68` vs §3.5 `:201` | — |
| **E-14** | **χ = 3 gate-cost penalty understated ~3× against the project's own ERRATA.** "~3× more gates at χ = 3." ERRATA §D4 establishes the *real* pytket compile of the χ = 3 MERA is **451** two-qubit gates against the χ = 2 figure of 57 (~8×), and its stated lesson is "verify measurement-vs-estimate provenance before any baseline compare." | §2.2 `:93`; §7.3 `:544` | `research/ERRATA.md` §D4 |
| **E-15** | **Internal contradictions asserted as simultaneous truths.** (a) §8.1 "this was an **artifact of the observable**, not the physics" vs §7.4 "these are **not contradictory** … bulk-to-bulk vs boundary-to-boundary" — if the second is right, the first is wrong. (b) §5.3 "requires further theoretical justification" vs §8.5 "**resolves** the open question from Sec. V.C". (c) §7.2 "introduces holographic transport as a **novel observable**" vs §7.4 "Wang and He **discovered** holographic transport in MERA circuits". | §5.3 `:329`, §7.2 `:490`, §7.4 `:552`/`:556`, §8.1 `:529`, §8.5 `:571` | — |
| **E-16** | **Misattribution of two load-bearing inputs.** (a) The 0.635/−0.026 operator is cited to `ZouMilstedVidal2020`; the project's own record sources it to Wang & He, and the manuscript drops the V†…V conjugation the record includes. No repository record exists for Zou–Milsted–Vidal at all. (b) l_AdS = 1/ln χ is cited to `KimSwingle2017`; the record attributes it to Sahay/Lukin/Cotler. | §5.1 Eq. (7) `:275`; §2.1 Eq. (2) `:64` | `PAPER-2026-010.json`, `PAPER-2026-009.json` |

**On E-2 in particular.** I want to be blunt about how this reads from the outside. Four bibliography
entries with wrong given names and wrong titles, all four contradicted by the submitting project's own
catalogue, is the signature pattern of citations generated rather than checked. Combined with E-1 — an
attributed analytic proof that is not in the cited paper — an editor is entitled to ask whether the
reference list was verified at all. I would recommend the editor request it be checked entry by entry
against the actual papers before any further review, and the acknowledgment's disclosure of AI-assisted
literature analysis (`:618`, correctly and properly placed) makes this a specific, answerable question
rather than an insinuation.

---

## 6. THE WORD "HOLOGRAPHIC" (§24 TEST)

> *Would the technical contribution still matter if every use of the word "holographic" were deleted?*

The word appears **30 times** (9 capitalized, 21 lower-case); "AdS" appears 60 times; "graviton" 3 times.
It is in the title.

Running the deletion:

| Section | With "holographic" | With the word deleted |
|---|---|---|
| Title | "Power-Law **Holographic** Forces and Causal Transport in MERA Quantum Circuits" | "Power-law decay of a two-excitation interaction energy in the critical Ising chain, and a transport-time observable in MERA boundary Hamiltonians" — accurate, and no longer a PRD title. |
| Result 1 | "**holographic** forces exist in the exact TFIM ground state … stress-tensor-mediated" | "the energy cost of two boundary-primary insertions decays with separation." A quantity whose asymptotic exponent is fixed by conformal symmetry, and which this dataset does not resolve. |
| Result 2 | "**holographic** transport matches the AdS₃ null geodesic prediction" | "a boundary-density feature reappears at a time that equals (π/2)/ln 2 to 1.2 %." A single number matched to a product of two constants, one from two-line algebra and one from architecture. |
| Result 3 | ALM + projection | **unchanged and still useful.** |
| Result 4 | χ = 3 restores criticality | **unchanged and still useful** (though single-seed). |
| §4.1 "three-level correspondence" | "quantum gravity in ADM superspace = worldline path integral on AdS = measurable MERA observables" | nothing. Three papers with overlapping subject matter are chained into a two-fold *identity* with no derivation, no error term, and no record. This sentence has no technical content in any reading. |

**Result of the test: two of four results survive deletion, and they are the two the paper treats as
supporting material.** The two headline results are, after deletion, (i) a symmetry-fixed exponent that
the data do not actually resolve and (ii) a one-number agreement with an architecture-defined constant.
Per §24, "where the answer is no, the claim needs stronger support or weaker presentation."

Three specific abuses of the vocabulary, in ascending order of seriousness:

1. **"Holographic force."** F(dr) = E_dual − E₀ − 2δE_single is an energy difference between excited
   states of a 1D spin chain. Nothing in the calculation involves a bulk, a geodesic, a metric, or a
   graviton. Calling it a force is a naming convention; calling it *holographic* asserts the very
   correspondence the paper is supposed to be testing. The manuscript itself concedes the physical
   identification "rests on the exponent matching" (`:329`) — i.e. on the one number §3 shows is an
   artifact.
2. **"Graviton exchange."** §5.3 (`:329`) and §8.1 (`:527`) invoke "virtual graviton exchange" in the Roux
   superspace framework, with "the graviton propagator decaying as 1/dr^{2Δ_T} = 1/dr⁴". No recorded Roux
   result gives a 1/dr⁴ boundary falloff; the exponent is the manuscript's own CFT identity, re-presented
   as a prediction of someone else's framework. §5.3 then immediately concedes the operator is not the
   stress tensor. The paper is simultaneously claiming and disclaiming a spin-2 identification.
3. **"MERA encodes an emergent AdS geometry."** The abstract's opening sentence asserts as established
   fact the thing the program's own governing document (§4) names as its central *unresolved* question,
   and which the project's own internal review answers negatively ("Every quantitative success so far is
   ordinary CFT data. Any good CFT method reproduces it; no geometry required" —
   `docs/governance/PROJECT-REVIEW-2026-08-11.md` §4).

I stress that the criticism is *not* that geometric language is forbidden. It is that in this manuscript
the geometric language is doing the work that the measurements were supposed to do. §23: "Strong framing
clarifies genuine importance. It cannot manufacture it."

---

## 7. REQUIRED ADDITIONAL CALCULATIONS

I would not consider a resubmission without all of R1–R6. R7–R12 are required if the geometric framing is
retained in any form.

### Mandatory before any resubmission

**R1 — Establish that F(dr) has a power-law regime at all, before quoting an exponent.**
Produce the local-slope plot of §3.2 as a figure. Identify a window over which the local slope is
constant within its own scatter. If no such window exists — and on the present data none does — the
correct statement is that F(dr) has no resolved power-law regime at these system sizes, and the α = 4
claim must be withdrawn. Then report the fit *only* over an identified plateau, with the window chosen by
a stated, pre-registered criterion rather than by inspection.

**R2 — Full fit-systematics table, published.**
For each of the three datasets, report α under: (a) linear-space LSQ (as published); (b) relative-error
weighting; (c) log–log regression; (d) every window dr ≥ 2, 3, 4, 5; (e) with and without the sign-flipped
χ = 3 points. Quote the *spread* as the dominant systematic. On the present data that spread is ~1.4,
i.e. ~9× the currently quoted uncertainty and larger than the α = 2 vs α = 4 discrimination the paper
claims. Also report the χ²_red = 6.008 and the bootstrap σ = 0.633 from `SIM-2026-017-statistics.json`,
and add that record to data availability.

**R3 — Resolve the operator identification, numerically.**
Project the state σ_a|GS⟩ onto the exact low-lying eigenstates of the finite chain and report the weight
in the σ tower vs the ε tower. Alternatively: compute ⟨GS|σ_j(0)σ_j(r)|GS⟩ for the Eq. (7) operator and
fit its exponent — 2Δ_σ = 1/4 vs 2Δ_ε = 2 are trivially distinguishable and settle the question in one
run. Reconcile with Wang & He's own identification of the same coefficients as the *spin* primary, and
state explicitly whether the V†…V conjugation is applicable to the Hamiltonian actually used. Until this
is done, no channel assignment and hence no α prediction is licensed.

**R4 — Remove the contact point, or justify keeping it.**
Show explicitly that the dr = 2 point (the unique separation with an H-bond bridging the two operator
supports) is not contaminated by a contact term, e.g. by repeating with a one-site operator, or with
operator supports separated by an extra buffer site, or on a chain with a longer-range but still critical
Hamiltonian. If the point cannot be defended, the exponent must be re-derived without it.

**R5 — Correct every item in §5 (E-1 … E-16).**
In particular: verify every bibliography entry against the actual paper; delete or substantiate the
"Wang and He analytically proved t_trans = π" claim; fix the nnz arithmetic; recompute the IBM comparison
on the circuit actually described; correct the Azure figures and the HQC formula; make the hardware
protocol reach t = 4.75; and either remove the priority claims or supply the literature-gate evidence.

**R6 — Surface `SIM-2026-019`.**
The project's own hardware feasibility verdict is PARTIALLY_REFUTED with "Helios is insufficient for
power-law detection." Either the hardware section states this and explains why the transport observable
is different (with a power calculation, which currently does not exist for the claimed 5σ), or the
hardware section is cut.

### Required if the holographic framing is retained

**R7 — A matched non-geometric control (§10, §19).**
Construct a second ansatz — MPS/puMPS at matched bond dimension and matched energy error, or a rewired
MERA with the same tensor count and disrupted causal structure — and measure the *same* F(dr) and the
*same* transport observable on it. If a matched non-geometric ansatz reproduces both, the geometric
interpretation adds nothing and the paper should say so. This is the named killer for the whole framing
and it has not been attempted.

**R8 — Transport robustness, with the detuning scan included.**
Publish the `approach_A` detuning table (§4.2b). Show whether the T = 2.25 point is a stationary point of
T(δ) or an accident of where the curve crosses. Establish that the dip/reappearance identification is
stable under (i) grid refinement — done at N = 12, 16, so extend to a third size by any means, including
approximate time evolution; (ii) perturbation amplitude A; (iii) width σ_t, σ_φ; (iv) probe site M.
Currently a single (A, σ, M) is reported.

**R9 — A third system size for the finite-size trend.**
Two points cannot distinguish 1/N from 1/N², and the record says so. Either supply N = 20 (2²⁰ is
tractable) or withdraw "the residual shrinks with system size" as a *scaling* claim and present it as two
numbers.

**R10 — Actually measure a force at a second fixed point.**
The universality claim is currently Δ_T at TCI/Potts plus an identity. Measure F(dr) on the tricritical
chain — the Hamiltonian, the operator, and the ED machinery all already exist in this project — and
report its exponent. That is a real test with a possible negative outcome; the present table is not.

**R11 — Seed statistics wherever a single seed is quoted.**
`SIM-2026-015c.json` (the 0.15 % at 16 q, the state used for the third α evaluation) is one seed. The
project's own experience (`SIM-2026-051.json` → `notes`: "the energy is FLAT across basins … so energy
CANNOT select the critical fixed point") shows that energy convergence does not select the right basin.
Report ≥ 5 seeds with the spread, and an overlap or entanglement-spectrum gate against the exact state.

**R12 — Reproducibility metadata (§21).**
Of the records backing this manuscript, **zero** carry a code revision, environment specification,
dependency versions, or output checksums; bootstrap RNG seeds are not recorded; and `*.npy` is gitignored
(`.gitignore:19`), so every ground-state and boundary-density array the data-availability appendix implies
is absent from the public repository. The analysis *scripts* are tracked, which is genuinely good and
better than most submissions — but a reader cannot reproduce a single headline number from the cited
artifact. Freeze a snapshot, pin versions, publish the state files or a script that regenerates them
deterministically from a recorded seed, and add the six load-bearing records currently missing from
Appendix E (`SIM-2026-017-statistics.json`, `SIM-2026-025.json`, `hyp010_criticality_scan.json`,
`SIM-2026-050.json`, `SIM-2026-002/003/005/006.json`, `pytket_compilation_results.json`).

---

## 8. SUMMARY OF THE REFEREE'S POSITION

1. The central result is not supported by its own data. This is not a matter of a slightly optimistic
   error bar; the exponent changes by 1.1–1.4 under analysis choices that discard nothing, and moves
   toward the value the paper says it excludes.
2. Even had the fit been sound, the quantity measured is fixed in advance by conformal symmetry, and the
   manuscript says so itself. Reproducing it is validation, not discovery.
3. The independence claims do not survive the ledger. Three "consistent evaluations" are one evaluation;
   the transport comparison is an architecture-defined constant matched to a single extremum difference;
   the m_eff agreement is an identity compared to a two-point ratio on a state the paper disqualifies
   elsewhere.
4. The strongest control the project ran on transport — the detuning scan — refutes the specificity claim
   and is not in the paper.
5. The paper contains at least sixteen distinct factual errors, including a fabricated-looking external
   validation and a bibliography with four wrong author given-names.
6. Deleting "holographic" removes the paper's two headline claims and leaves two useful method notes.

I want to close the criticism by recording what is *good*, because it is unusual and it should not be lost
in a rewrite: the ERRATA-E2 self-retraction of a published number; the N = 24 double-lobe exclusion; the
`SIM-2026-018` amplitude-coincidence killer; the `SIM-2026-030` catch of its own script's false positive;
the exact-diagonalization pre-gates on blocked operators; the tracked analysis scripts; and the honest
disclosure at §3.1 that the transport work uses a different state from the VQE work. This is a project
that catches its own errors. That capability is worth more than the paper it is currently attached to.

---

## 9. AUTHOR RESPONSE STRATEGY

What follows is the **strongest honest rebuttal available**. I have deliberately excluded every argument I
judge to be spin. Where the referee is right, the strategy is to concede fast and precisely, because the
concessions cost less than they appear to and the surviving paper is better.

### 9.1 On the α = 3.92 fitting artifact — **do not contest it; convert it**

There is no defensible rebuttal to the leverage calculation. 95.8 % of the weight on one point is a fact
about the recorded array. Contesting it will destroy credibility on every other point.

**The honest and genuinely strong move:** the referee's own analysis contains a real physics result the
paper missed. The local slope is *stable* at 2.45–2.66 across dr = 4…8 in the 24 q data and 2.6–2.9 in the
16 q data. That is a plateau — just not at 4. Present it:

> "The referee is correct that our dr ≥ 2 fit is dominated by the dr = 2 point and that the exponent is
> not robust to reweighting. Following the referee's local-slope analysis we now identify a genuine
> intermediate-distance plateau at α = 2.5 ± 0.2, together with an upward drift at dr ≳ 9 which we
> attribute to open-boundary contamination. We have withdrawn the α = 4 identification and now report the
> plateau exponent as the measured quantity, with the channel identification (§9.3) left open."

This is defensible, is a real measurement rather than a symmetry-fixed one, and — crucially — has
**non-zero counterfactual novelty**, because 2.5 is not any obvious CFT prediction. An intermediate
exponent that matches neither 2Δ_ε = 2 nor 2Δ_T = 4 is more interesting than a confirmed identity,
provided it survives R1–R4.

**Also legitimately defensible:** the manuscript did report the bootstrap CI [2.52, 4.19], which straddles
both hypotheses, and did report the anchor-variation check. The author can point out that the CI was
disclosed. But he must concede immediately that the CI was disclosed while the σ = 0.633 and the mean
3.369 from the same record were not, and that this was selective. Say it first, before the referee does.

### 9.2 On "the result is fixed by conformal symmetry"

**Defensible, and this is the author's best structural argument.** The reply is not "no it isn't" — it is
that the paper measured two different things and conflated them:

> "Δ_T = 2 is indeed kinematic and we state this ourselves. What was *not* guaranteed in advance is
> whether a finite open-boundary lattice observable constructed from a two-site boundary-primary operator
> would exhibit the CFT asymptotics at accessible separations, or whether it would be dominated by
> contact terms and boundary effects. That question had a genuinely open answer. Our data now indicate
> the answer is the latter: the CFT asymptotics are *not* resolved at N ≤ 24. That is a useful negative
> result about the observable, and it is the result we should have reported."

This reframing is honest, converts a Level-1 non-result into a Level-2 methodological finding about
observable design, and is consistent with the paper's genuinely good §5.4 diagnostic. It is the single
best available move.

The author may also legitimately say: the specific *prediction* that the exponent should recur at TCI and
Potts was stated before those runs, and the runs were done. That is out-of-sample in the §18 sense, even
if the outcome was constrained. It is a small point but it is true.

### 9.3 On the operator identification (σ vs ε)

**Concede the citation error immediately and completely** — the coefficients are Wang & He's, not
Zou–Milsted–Vidal's, and the paper drops the V†…V conjugation. This is not arguable.

**On the physics there is one honest defence, and it is a good one:** in the plain critical-TFIM frame the
manuscript actually uses, the dominant piece of Eq. (7), 0.635(X_j + X_{j+1}), is the lattice energy
density and is Z₂-even, whereas the spin primary is Z_j and is Z₂-odd. So under P = ΠX the operator is
predominantly in the ε sector, with only a 4 %-amplitude parity-odd admixture. The ε identification is
therefore not baseless — but the author must concede that (a) the operator is *not* a parity eigenstate as
written, which no version of the paper states, and (b) Wang & He's own frame gives the opposite reading,
so the frame-mapping must be made explicit. The correct response is R3: run the projection test and let
the number decide. Do not argue this in prose.

**Do not attempt the argument that ε × ε = [1] settles it.** As the referee notes, that argument
presupposes the identification.

### 9.4 On the transport detuning scan

**Concede the omission; contest the inference.** The honest position:

> "The detuning scan should have been in the paper and will be. We note, however, that δ ≠ 0 moves the
> chain *off criticality*, where no conformal or AdS prediction is claimed to hold, so a large change in
> T is expected rather than damaging: the correct reading is that T is a sensitive probe of criticality,
> which is a positive property of the observable. What the scan does establish, and what we now state, is
> that T is not a *robust* quantity — it is a sharp function of the Hamiltonian, so the agreement at
> δ = 0 must be treated as a single-point agreement, not as a geometric invariant."

That is honest and partially rehabilitates the observable. But two further concessions are unavoidable:
the T(δ) sequence is **non-monotone** (0.55 at δ = +0.3 after 3.30 at δ = +0.1), which is hard to read as
smooth off-critical degradation and does suggest the dip/reappearance identification is fragile; and the
"non-systematic pattern" description of the g-scan is simply wrong and must be corrected to "monotonically
decreasing," with the consequence — that T is a smooth function of coupling — stated rather than hidden.

### 9.5 On independence

**Concede fully.** The paper already contains the correct sentence at §6.5 ("all sample the same conformal
fixed point"). The honest response is that the abstract and §5.3 should have used that framing and will:

> "We have replaced 'independently confirmed' with 'reproduced on a second system size and on a
> variational approximation of the same state', and added an explicit statement that the three
> evaluations share observable, operator, fit model, and analysis code."

There is one legitimate defence worth keeping: the χ = 3 MERA evaluation *does* add one genuinely
independent piece of information — that a variationally optimized tensor network, not merely an exact
eigenvector, reproduces the observable. That is a real, if narrow, contribution and it should be stated as
exactly that narrow thing.

### 9.6 On "holographic"

**The strongest honest position is to give the word up in the title and keep it, clearly labelled, in one
Discussion subsection.** The technical contributions that survive deletion — the ALM + projection
optimizer, the observable diagnostic, the ED pre-gate, and (post-R1) the intermediate-exponent plateau —
are real and are what the paper should be about. Retitling costs nothing scientifically and removes the
referee's most effective line of attack in one move.

The author may honestly note that Sahay–Lukin–Cotler, Swingle, and Kim–Swingle all use the same
vocabulary in the same technical sense, so the usage is community-standard rather than idiosyncratic.
That is true and worth one sentence. It does not answer the §24 test and should not be presented as if it
does.

**Do not defend the §4.1 "three-level correspondence" equality.** "Quantum gravity in ADM superspace =
worldline path integral on AdS = measurable MERA observables" has no derivation and cannot be supported.
Delete it. Replacing it with a clearly labelled "Motivation" paragraph loses nothing the paper can prove.

### 9.7 On the factual errors

**No defence exists for E-1 through E-16 and none should be attempted.** Correct them, and say
specifically what process changed. The bibliography errors (E-2) and the non-existent external validation
(E-1) are the two that determine whether the editor grants a resubmission at all, so the response should
lead with them, not bury them:

> "We verified every reference against the primary source and found four entries with incorrect author
> given names and titles, and one claim of external analytic validation that the cited paper does not
> contain. Both have been corrected; the validation claim has been removed entirely rather than
> reworded. We have added a citation-verification step to our workflow and re-checked all 28 entries."

The author has one genuinely mitigating fact and should state it plainly rather than defensively: the
project maintains a public ERRATA file in which it has already retracted one of its own published numbers
(the 0.72 % transport residual), and the correction propagated into the submitted manuscript. A project
that retracts its own headline number has a claim on the editor's patience that a project that never
found an error does not.

### 9.8 What the author should propose instead

The honest strategic recommendation, consistent with the project's own governing standard §25:

- **Withdraw this manuscript** rather than attempt to defend it through review. The α = 4 claim will not
  survive R1–R4, and defending it while it is being dismantled is the worst available outcome.
- **Split into two papers.** Paper A: the methods paper — ALM + Z₂/Z₃-projected optimization, the
  observable diagnostic, the ED pre-gate on blocked operators, and the negative result that CFT
  asymptotics of the two-excitation interaction energy are *not* resolved at N ≤ 24. This is defensible
  today, needs no geometric framing, and is a genuine service to anyone attempting the same measurement.
  Paper B: the biorthogonal Yang–Lee work (`SIM-2026-070/071`), which the project's own review identifies
  as its strongest result and which postdates this submission — subject to the §8 literature gate, which
  is recorded as UNVERIFIED and must be closed first.
- **Do not resubmit anything with "holographic" in the title until R7** — the matched non-geometric
  control — has been run. If a matched control reproduces the observables, that is a publishable negative
  result under §16 and a better paper than this one. If it does not, the geometric claim finally has
  evidence behind it.

---

## 10. UNVERIFIED

Stated explicitly per the audit protocol. Silence is not a pass.

1. **The actual content of the cited external papers.** I verified the manuscript's claims against the
   project's *own catalogued records* of those papers (`PAPER-2026-009/010/017/020/023/088.json`), not
   against the papers themselves. It is possible — though the four independent given-name errors make it
   unlikely — that a record is wrong and the manuscript is right. In particular, I did **not** fetch
   arXiv 2603.07639 to confirm that Wang & He do not prove t_trans = π; I confirmed only that the
   project's record of that paper contains no such claim in its abstract or six key_claims. This is the
   most consequential single item and it should be checked against the primary source before the finding
   is acted on.
2. **Zou–Milsted–Vidal 2020.** I confirmed no repository record exists and that the project's record of
   Wang & He gives the same coefficients. I did not read the ZMV paper and cannot say whether the
   coefficients also appear there. The citation may be defensible; it is simply unevidenced in this repo.
3. **The parity/channel argument in §3.7.** My statement that the Eq. (7) operator is a parity mixture
   under P = ΠX is an analytic reading of the operator as written, not a numerical projection. R3 is
   required to settle it. I have flagged it as an open identification problem, not as a proven error.
4. **The exact provenance of the 0.030 vs 0.046672 peak amplitude (E-12).** I confirmed the record value;
   I did not open `boundary_density_Y.npy` myself (a phase-1 auditor reports recomputing 0.0466718 from
   it, and the record agrees, so I regard the mismatch as established but the raw-array recomputation is
   second-hand in this report).
5. **Figures.** I read the six figure PNGs' filenames and captions and the generating scripts' presence,
   but did not inspect the rendered images. Whether Fig. 4's plotted fit line corresponds to the α = 3.92
   linear-space fit or to a log-space fit is therefore unchecked, and it matters: if Fig. 4 is plotted
   log–log, the visual will not match the quoted exponent.
6. **Whether the submitted PDF matches `paper-prd.tex`.** `paper-prd.pdf` was built 2026-07-21 09:27 from
   a `.tex` last modified 2026-07-21 09:26 and submitted 2026-08-07. I did not extract the PDF text to
   confirm byte-level correspondence.
7. **The physics interpretation of α ≈ 2.5.** I report that the intermediate-distance local slope sits at
   2.45–2.66 and is stable there. I do **not** claim to know what that exponent is. It is not 2Δ_ε = 2, not
   2Δ_T = 4, and not 2Δ_σ = 1/4. It could be a crossover between channels, an OBC artifact, or an
   amplitude-driven effective exponent with no CFT meaning. Establishing that is R1/R3 work and I make no
   claim about the outcome.
8. **Whether a matched non-geometric control would reproduce these observables (R7).** Untested by
   anyone. The referee's expectation is that it would, but that is an expectation, not a finding.
