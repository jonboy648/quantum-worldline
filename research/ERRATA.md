# Errata & Record Corrections — quantum-worldline paper and data

Live register of known errors in published/submitted text (**E**-entries) and defects in the
internal data records (**D**-entries).

- E1–E5, D1–D5 originate in the full-project audit 2026-06-08 (13-agent workflow wf_c0e83471-cb7,
  all findings adversarially verified against files of record).
- E6–E7, D6–D7 originate in the 23-agent scientific audit 2026-08-11
  (`docs/governance/AUDIT-2026-08-11.md`), governing standard
  `docs/governance/RESEARCH-DIRECTOR.md`.

## How this register works (RESEARCH-DIRECTOR.md §32)

This file is a **live correction register**, not a snapshot of any one audit. It was allowed to
become the latter between 2026-06-19 and 2026-08-11 (audit defect **D-18**); these rules exist so
that it does not happen again.

1. **Corrections are additive. Never silently rewrite history.** Do not delete or quietly reword an
   entry. Every entry preserves, in order: the **original claim**, the **evidence available at the
   time**, the **later challenge**, the **corrected analysis**, the **changed conclusion**, and the
   **downstream records affected**. When a correction is itself later corrected, append a dated
   follow-up paragraph rather than editing the earlier text. The exemplar is
   **D5 → SIM-037 (cheap fix failed) → SIM-039 (root cause) → SIM-040 (closure)** below.
2. **Write the correction into the corrected record, not only here.** Each superseded JSON record
   gets a `verdict_SUPERSEDED_<yyyy_mm_dd>` field naming this entry and the superseding SIM id.
   An ERRATA entry with no write-back is half a correction.
3. **Every entry must name where the correction was propagated.** Each entry carries an explicit
   *Propagated to* list; anything not yet propagated is listed under *Not yet propagated* and stays
   there until it is. Nine of the first ten entries lacked this and propagation silently stalled.
4. **Numbering is append-only.** Entries are never renumbered or removed, only superseded in place.
5. **Record retractions at full strength, in the project's own words, before anyone else writes
   them down.** A transparent retraction raises the credibility of the surviving claims.

## Current status of the record (updated 2026-09-08)

- **Manuscript**: **REJECTED by Physical Review D on 2026-08-12** (desk reject, accession
  `DV13971`, closed). Nothing is owed to APS; the correction package written for a live submission
  is moot. The 2026-08-17 block below said "with editors" and was wrong for that reason — it is
  superseded, not edited, per rule 1.
- **Public data record**: **Zenodo v5 PUBLISHED 2026-09-07**, version DOI
  **10.5281/zenodo.22080720**, carrying the E6 retraction, the E7 retraction, and the E8 killer-test
  retraction as the first pages of the record and as the record description. Verified against the
  public API the same day. Concept DOI **10.5281/zenodo.19660302** resolves to the current version
  and is the one to cite. The GitHub mirror, which restated the withdrawn headline on its front
  page, was made **private** on 2026-09-07.
- **Outstanding at the top of the file**: **E6, E7 and E8 are now EXECUTED** in the public record.
  No public artifact asserts α = 3.92 without the correction. What remains unexecuted is the "Class
  B" backlog: roughly two dozen post-2026-06-19 reversals catalogued in
  `research/data/audit/raw/inv-errata-history.md` §2 are still missing from this register.
- **Data-record defects**: **D9** (added 2026-09-08) records a summary that restated itself rather
  than its data, in the HYP-032 line of work.

**HISTORICAL STATUS 2026-08-17 (superseded by the block above; preserved per rule 1): manuscript
"SUBMITTED to PRD, with editors" — stale by five days at the time it was written, the PRD rejection
having landed 2026-08-12; public record "Zenodo v4 published, E6/E7 neither has been executed."**

**HISTORICAL STATUS 2026-07-13 (superseded by the block above; preserved per rule 1):
E1–E5 ALL APPLIED to the local v5 draft (paper-draft-scipost.tex),
alignment audit pass.** E1/E2: transport restated as grid-converged −1.21% @ N=16 with
−2.78% @ N=12 trend; coarse-grid 0.72%/0.71% explicitly labeled artifacts; N=24 double-lobe
caveat added (§3.5 + App. D). E3: appendix row annotated "record lost; script preserved".
E4: §4.2 rewritten in AdS3 convention Δ(Δ−2); 0.693 = 1/l_AdS from Δ=1 exactly; x1=0.485
downgraded to operator-identification corroboration. E5: Zenodo DOI added to front matter.
Same pass also fixed: OQ#4 contradiction with §6.5; "six seeds within 1.5%" → 2% (seed 4 is
1.51% per SIM-052); data-availability appendix now lists SIM-011-interaction + universality
+ OPE records. NEW in v5: Potts c=4/5 third class (SIM-062/063) in §6.5 + abstract;
measured C_σσε = 0.50 ± 0.03 (SIM-061/064) in §7.4. Published Zenodo v3 still carries
E1–E5; supersede with a new Zenodo version when v5 is final.

## Published-text errata (Zenodo v3, DOI 10.5281/zenodo.19661227)

> **The most consequential entry in this file is E6 — the retraction of the force exponent
> α = 3.92 ± 0.16, the manuscript's central finding. E7 retracts the Yang-Lee novelty claim.
> Both post-date the Zenodo v3 heading of this section and apply to Zenodo v4 and to PRD
> accession DV13971.**

### E1 — "l_AdS deviation 0.76%" is wrong; correct value 0.71%
- Where: paper-draft.md §III.C table (~line 109); paper-draft-scipost.tex lines ~186-192. Appears twice per version.
- Record: `research/data/simulations/composite_geodesic_results.json`:
  l_AdS_needed_to_match_exact = 1.4323944878 vs theory 1.4426950409 → (Δ/theory) = **0.714%**
  (0.719% if normalized by the fitted value). No rounding path yields 0.76.
- Impact: low (derived value; the headline transport agreement is computed independently). Still a wrong number in published text.

### E2 — Published "0.72% at N=16" transport residual is a time-grid artifact; converged value −1.205%
- Where: paper-draft.md lines ~104/106/383/489 (T=2.250, 0.72%); also MEMORY/transport summaries.
- Record: `research/data/simulations/SIM-2026-025.json` (2026-05-16, dt=1e-3, 50× finer than the
  original dt=0.05): N=16 T_refined = 2.23888 → residual **−1.205%**; N=12 → −2.777%.
  The original dt=0.05 grid quantization made the residual look smaller (T=2.250 → −0.72%).
- Science impact: the A2 anchor SURVIVES qualitatively — T ≈ (π/2)·l_AdS with residual shrinking
  as N grows (−2.78% @ N=12 → −1.21% @ N=16, consistent with 1/N finite-size convergence) — but the
  published precision claim "0.72%" is superseded by the project's own follow-up. v5 should state
  "≈1.2% at N=16 (dt-converged), with 1/N trend" and note the grid systematic.
- Note: this re-run also REFUTED HYP-2026-023 (composite-geodesic residual explanation predicted <0.2%).
- N=24 fine-dt is computationally infeasible (~7300 min); the coarse N=24 signal is excluded as
  unreliable (double-lobe structure) per SIM-025 — any v5 treatment of N=24 transport must carry this caveat.

### E3 — Supplemental S1 penalty-method row (4.02%, P=0.000) is untraceable
- Where: paper S1 table, row "24q, 5-layer, Penalty (λ=20, RunPod A100), SIM-2026-007".
- Problem: no SIM-2026-007.json exists (JSON lost on RunPod teardown); the only artifact is the
  script `penalty_vqe_24q.py`. Additionally the ID "SIM-2026-007" is claimed by a different
  experiment (worldline MC on H², inside worldline_mc_results.json).
- v5 action: either re-run to regenerate the record, or annotate the row "record lost; script preserved".

### E4 — §IV.B m_eff derivation text contradicts the data records (convention clash)
- Where: paper §IV.B; records `effective_mass_analysis.json`, `worldline_mc_results.json`.
- Problem: paper states m²l² = Δ(Δ−1) ("for Δ=1 this gives m²=0") but the record computes
  Δ(Δ−2) = −1 (AdS₃ convention, tachyonic-allowed) to get m_eff = 0.6931 = √|−1|/l_AdS... and the
  paper's claim that gap-derived x₁=0.485 "corresponds to m_eff=0.693" is wrong under the record's own
  formula (x₁=0.4847 → 0.594). 0.693=ln 2 follows only from Δ=1 exactly. The two records also
  disagree with each other on convention (worldline_mc uses Δ=1/2+√(1/4+m²l²) and records NaN).
- Impact: the A4 *numbers* (0.693 vs 0.670, 3.5%) are reproducible from the record; the *derivation
  text* needs a consistent convention in v5. The m_eff agreement claim should be reviewed under
  whichever convention is chosen.

### E5 — Zenodo DOI absent from both paper source files
- Neither paper-draft.md nor paper-draft-scipost.tex contains the published DOI 10.5281/zenodo.19661227.
  Add to v5 front matter.

### E6 — RETRACTION: the force exponent α = 3.92 ± 0.16 is an estimator artifact; the measured value is α = 2.6 ± 0.2 and the exchange channel is OPEN

**This is a retraction of the manuscript's central finding, on a manuscript currently under review.**

> **Update 2026-09-06.** The manuscript is no longer under review: PRD desk-rejected accession DV13971 on 2026-08-12, before this error was found and on separate grounds. Nothing is owed to APS. The public artifacts that still carried alpha = 3.92 are the Zenodo record (v5 correction built 2026-09-06, see `docs/governance/PLAN-2026-09-06.md`) and the public GitHub mirror README (`github.com/jonboy648/quantum-worldline`, last pushed 2026-06-17), whose fate is a pending decision. **2026-09-07: Zenodo v5 PUBLISHED (10.5281/zenodo.22080720); GitHub mirror made PRIVATE. No public artifact asserts alpha = 3.92 without the correction attached.**

- **Original claim (as published/submitted).** "The force between two boundary regions falls off as
  F(dr) ∝ dr^(−α) with **α = 3.92 ± 0.16**", presented as agreeing with the stress-tensor
  prediction α = 2Δ_T = 4 to ~2%, corroborated by "three independent evaluations" (N=24 exact
  3.9218; N=16 exact 3.9748; N=16 χ=3 MERA 4.0712), and used to **exclude** the scalar channel
  α = 2Δ_ε = 2 at ~12σ.
- **Where it appears.** `research/submission-package/prd/paper-prd.tex` — Abstract, §5.3, §8.1
  (PRD accession **DV13971**, with editors; the human is handling that file, do **not** edit it
  from the repo side); `README.md:15` ("alpha = 4.0 (3 independent measurements: 3.92 / 3.97 /
  4.07)"); the Zenodo record (v3, v4) which inherits the manuscript text; and the source records
  `research/data/simulations/SIM-2026-011-interaction.json` (`.power_law_fit.alpha` 3.9217597),
  `SIM-2026-015d.json` (`.exact` 3.9748, `.mera` 4.0712), `SIM-2026-017-statistics.json`.
- **Evidence available at the time.** An 11-point profile (dr = 1..11 with dr = 1 excluded as a
  contact term), fitted by unweighted nonlinear least squares to F = A·dr^(−α) in **linear** space;
  `curve_fit` covariance 1σ = ±0.16; three datasets agreeing to ~2%.
- **The challenge.** Audit defects **D-2** and **D-3** of `docs/governance/AUDIT-2026-08-11.md`
  (23-agent scientific audit), then confirmed by **independent recomputation from the raw records
  before any action was taken** — separate driver, separate author, records the only shared input.
  The re-analysis reproduces the original number exactly (3.9218 vs 3.9218 recorded) before
  diverging, which rules out an implementation difference as the cause.
- **Corrected analysis — record of authority: `research/data/simulations/SIM-2026-072.json`**
  (2026-08-17; driver `research/tools/force-reanalysis/qw_alpha_reanalysis.py`, seed 20260817,
  deterministic; three datasets × 3 estimators × 5 fit windows, plus leverage, local-log-slope,
  plateau-scan and bootstrap diagnostics). What is wrong:
  1. **Leverage.** The single point dr = 2 carries **95.8%** of the unweighted least-squares
     objective (96.0% and 96.3% on the other two datasets). The published α is, to within 8%, the
     dr = 2→3 **local slope** (4.2315) — a property of one point, not of the profile.
  2. **Estimator dependence, discarding no data.** Changing only the error model gives α = **2.822**
     (relative-error weighting) and α = **2.890** (log-space OLS, the textbook power-law estimator).
     Dropping dr = 2 gives 2.559 / 2.753 / 2.633 across the three datasets — same direction every
     time. Over 15 defensible estimator × window choices the published value is the **maximum**.
  3. **No plateau at 4.** A true power law has a flat local log-slope. The N=24 local slopes run
     2.035, **4.232**, 2.603, 2.456, 2.461, 2.533, 2.658, 2.841, 3.102, 3.482, 4.064 — a spike at
     dr = 2 and a rise at the far end bracketing a genuine intermediate plateau (6 consecutive
     slopes flat to ±7.5%) centred on **2.592**. **No dataset shows any flat region at 4.**
  4. **The quoted uncertainty is not the project's own.** ±0.16 is a covariance 1σ on a fit whose
     own **χ²_red = 6.008** (dof 9, p ≈ 1e−7 — a formally rejected fit). The same record's
     bootstrap gives mean **3.369**, **σ = 0.635** (re-derived here as 3.358 ± 0.635, 95% CI
     [2.52, 4.18], 2000 resamples). The manuscript quotes the covariance CI and never the bootstrap
     σ or mean, and `SIM-2026-017-statistics.json` is cited nowhere and is absent from data
     availability.
  5. **Why dr = 2 is the wrong anchor.** dr = 2 is the unique separation at which a Hamiltonian
     bond bridges the two operator supports — a contact term. The manuscript excludes dr = 1 on
     exactly this reasoning and then rests its result on the next point in the same family.
  6. **The "three independent evaluations" are not independent.** They move in lockstep under the
     dominant systematic (3.92 → 2.56, 3.97 → 2.75, 4.07 → 2.63) because they share one observable,
     one operator, one fit window and one fitting routine. Their agreement measured the estimator,
     not the physics.
- **Changed conclusion.** **α = 3.92 ± 0.16 is WITHDRAWN as stated.** The corrected measurement is
  the intermediate-separation exponent **α = 2.6 ± 0.2**, stable across all three datasets and
  across estimator choice. This matches **neither** candidate channel: 2Δ_T = 4 (stress tensor) is
  excluded by the plateau, and 2Δ_ε = 2 (scalar) lies outside the plateau band — so **the exchange
  channel identification is OPEN**. The "α = 2 is excluded" claim does not survive at the stated
  significance: ~12σ at ±0.16, but only **~2.2σ** at the project's own bootstrap σ = 0.635, and
  under any dr ≥ 3 window the point estimate itself falls to ≈ 2.56.
- **Scientific effect of the correction.** It strengthens the content rather than emptying it. The
  withdrawn number was fixed in advance by a Virasoro theorem (near-zero counterfactual novelty);
  the measured number is predicted by neither candidate channel and is therefore a real, if modest,
  open question. The registered killer test for HYP-2026-008 (V_T vs V_X channel discrimination)
  was never executed and is now the outstanding test.
- **Downstream records affected.**
  - `HYP-2026-008` status must fall from SUPPORTED (its supporting fit is withdrawn).
  - `HYP-2026-002` ("holographic forces power-law not exponential") — the power-law-vs-exponential
    model comparison should be re-stated under a defensible estimator; the exponent it quotes is
    the withdrawn one.
  - `SIM-2026-011-interaction.json`, `SIM-2026-015d.json`, `SIM-2026-017-statistics.json` each need
    a `verdict_SUPERSEDED_2026_08_17` field pointing to SIM-2026-072 (rule 2 above; the SIM-036 →
    SIM-039/040 pattern of D5).
  - `README.md:15` headline row; the Zenodo record; `research/knowledge-base.md` and any digest,
    learning guide or theory prose quoting 3.92 / "α = 4.0, three independent measurements".
  - **PRD accession DV13971 (with editors): a correction is required.** See
    `docs/governance/PRD-CORRECTION-PACKAGE.md`.
- **Propagated to:** this register (E6); `research/data/simulations/SIM-2026-072.json` (record of
  authority, `status: COMPLETE`); the three `verdict_SUPERSEDED_2026_08_17` write-backs on
  `SIM-2026-011-interaction` / `SIM-2026-015d` / `SIM-2026-017-statistics` (**verified present on
  disk 2026-08-17**); `HYP-2026-008.json` (→ NOT_ESTABLISHED / low, with the killer test named) and
  the annotated downstream hypotheses HYP-002 / 011 / 022 / 025 / 027; `README.md` (headline row
  struck, correction box added, citation block warns off both the manuscript and the Zenodo record);
  `NEXT-SESSION.md` (HOT STATE #1).
  Also `research/knowledge-base.md` (dated advisory header + the α≈4 line struck).
- **Not yet propagated (as of 2026-08-17):** the PRD manuscript and its accession **DV13971**
  (letters drafted, unsent, awaiting approval — `docs/governance/PRD-CORRECTION-PACKAGE.md`); a new
  Zenodo version; the `research/learning/` guides and any theory prose not yet swept. The first two
  are the remaining **public** surfaces carrying the withdrawn number, and both require Jon's
  decision before they can move.
- **See also D7**, a further defect in the same family found by the re-analysis and *not* by the
  audit: the χ = 3 MERA fit runs through two points of the wrong sign.

### E7 — RETRACTION: the Yang-Lee "first lattice extraction of a negative central charge" novelty claim, and the false premise it rested on

- **Original claim.** `research/data/simulations/SIM-2026-071.json` (2026-08-11), key finding:
  *"First lattice extraction (to our knowledge) of a NEGATIVE central charge from stress-tensor
  matrix elements; standard approaches obtain only c_eff from Casimir scaling."* Echoed in
  `NEXT-SESSION.md:35-36` and in the project's own framing of SIM-071 as its strongest result.
- **Evidence available at the time.** A genuine and reproducible measurement — biorthogonal
  Koo-Saleur elements at the M(2,5) Yang-Lee point giving c_KS = −4.29 ± 0.15 against
  c = −22/5 = −4.4, with c_eff = +2/5 excluded by sign and by ~11× in magnitude, unitary control
  0.49986/0.5. **The measurement is not retracted here — only the priority claim and its premise.**
- **The challenge.** Audit §4.1 / defect **D-5** of `docs/governance/AUDIT-2026-08-11.md`. Two
  investigators attacked the claim from disjoint endpoints (one arXiv-export-API-only, one
  WebSearch / Semantic Scholar / INSPIRE / ar5iv / publisher-page only) and converged on the same
  prior art without contact.
- **Prior art (both absent from this repository at the time of the claim).**
  1. **Io, Huang & Hsieh, arXiv:2602.02649** [cond-mat.str-el], v1 **2026-02-02** — *"Non-Hermitian
     free-fermion critical systems and logarithmic conformal field theory."* Six months and nine
     days before SIM-071. Overlap on six of six elements: 1+1D non-Hermitian critical lattice
     chain; biorthogonal left/right pairing; **Koo-Saleur Fourier modes, named**; the central term
     of the resulting Virasoro algebra; the extracted value is the **true negative c** (−2), not
     c_eff; and an explicit claim that the KS/stress-tensor route survives non-unitarity. They cite
     Koo-Saleur (hep-th/9312156) and Milsted-Vidal (1706.01436) — the identical two references this
     pipeline rests on.
  2. **Couvreur, Jacobsen & Saleur, PRL 119, 040601 (2017)**, arXiv:1611.08506 — left+right
     eigenstate entropies on non-Hermitian critical chains scaling with the **true** c, including a
     lattice measurement of a negative true c (−3/5) beside the positive c_eff of the same model.
     Its introduction names this project's exact headline pair verbatim: *"for the Yang-Lee
     singularity, c = −22/5 but c_e = 2/5."* Nine years prior, in PRL.
- **The premise was false, not merely unnovel.** *"Standard approaches obtain only c_eff from
  Casimir scaling"* is contradicted by Tang et al., PRL 133, 076504 (2024) (complex c from
  biorthogonal Casimir scaling); Zhou & Wang, arXiv:2405.01640 (negative c from OBC energy
  scaling); Tu, Tzeng & Chang, SciPost Phys. 12, 194 (2022); Chang et al., PRResearch 2, 033069
  (2020); and Shimizu & Kawabata, PRB 112, 085112 (2025) — **the same senior author whose paper
  SIM-2026-070 reproduces.** Moreover c = c_eff + 24·h_min makes c recoverable from c_eff by
  arithmetic, so the companion statement that *"the biorthogonal element structure sees what the
  energy spectrum cannot"* is also false.
- **Aggravating — this was a process failure, not bad luck.** arXiv:2602.02649 is **reference [24]
  of PAPER-133** (arXiv:2606.16785), the paper the project downloaded, logged a *"FULL v2 READ
  DONE"* for, and designed this entire phase around **on the same day**. The pointer was in hand
  and was not followed. Neither 2602.02649 nor 1611.08506 appeared anywhere in the repository when
  this entry was written; both were added to `research/references.bib` and to
  `SIM-2026-071.json` → `prior_art` later the same day, and **still have no `PAPER-` catalogue
  record** — catalogue both before the next scan. Root
  cause: the novelty gate was delegated to a forward-only weekly newsfeed
  (`research/digests/` begins 2026-03-10; 2602.02649 posted 2026-02-02), an architecture
  structurally incapable of catching prior art older than its first scan; no backward search on
  "Koo-Saleur" / "biorthogonal" / "negative central charge" was ever run.
- **Changed conclusion.** The priority claim is **WITHDRAWN**. Per RESEARCH-DIRECTOR.md §8, the
  words "first", "novel", "to our knowledge" and "unprecedented" must be **struck, not softened**,
  and replaced by a **cited positioning sentence** naming arXiv:2602.02649 and PRL 119, 040601 —
  for example: *"Biorthogonal Koo-Saleur constructions have been shown to yield the true (negative)
  central charge in non-Hermitian free-fermion chains (Io, Huang & Hsieh, arXiv:2602.02649), and
  left/right eigenstate entropies were used to measure a negative true c on non-Hermitian lattice
  models by Couvreur, Jacobsen & Saleur (PRL 119, 040601 (2017)). We extend that line to an
  interacting chain, the PT-symmetric Ising model at M(2,5)."*
- **Honest residue that survives the gate** (all Level 1–2, none of it a priority claim): a
  finite-L numerical, error-barred KS ladder in an *interacting* non-Hermitian chain; the sharpest
  available c-vs-c_eff instance (sign flip plus 11×); the provable rescaling/metric invariance of
  the product-form estimator; and the state-identification inversion at Yang-Lee.
- **Downstream records affected.** `SIM-2026-071.json` (the "First … (to our knowledge)" key
  finding and its `prior_art` field, which does not exist — `grep -c "prior_art|novelty|literature"`
  returns 0); `NEXT-SESSION.md:35-36`; `README.md:197`; the manuscript's five ungated priority
  claims; the paper catalogue, which lacks records for 2602.02649, 1611.08506, Milsted-Vidal
  1706.01436 and Zou-Milsted-Vidal 1710.05397 — *the papers that publish the values of this
  project's own headline numbers*.
- **Open search (do not treat the gate as closed).** INSPIRE, Crossref and Semantic Scholar were
  not swept; forward citations of 1611.08506 were not walked. The highest-value remaining check is
  whether arXiv:2007.11539 Appendix A already fits c numerically from KS matrix elements in a
  logarithmic model — a hit there pushes the prior art back to 2020 and removes the residue above.
- **Propagated to:** this register (E7); `SIM-2026-071.json` (→ `prior_art`, priority claim struck);
  `NEXT-SESSION.md` (withdrawal box, and the HYP-028 status corrected from the "SUPPORTED (medium)"
  it had wrongly carried); `HYP-2026-028.json` (→ OPEN / low, with
  `founding_premise_correction_2026_08_17`); `research/references.bib`.
- **Not yet propagated (as of 2026-08-17):** the paper catalogue (no `PAPER-` record yet exists for
  either 2602.02649 or 1611.08506), and the submitted manuscript. `README.md` never carried this
  claim, so nothing was owed there.

### E8 — RETRACTION of the registered killer test: it compared the energy density to itself (Kramers-Wannier self-duality), and the direct replacement is blocked by Z2 parity

- **Original claim (as registered, 2026-03-11, HYP-2026-008 `refutation_criteria`; restated in
  `research/tools/channel-test/PREREGISTRATION.md` and run as SIM-2026-073).** The exchange channel
  would be discriminated by comparing the force measured with "stress tensor operators
  T(x) = -J sum_i Z_i Z_{i+1}" against "spin primaries X_i": alpha_T = 4 vs alpha_X = 2.
- **Evidence available at the time.** The two lattice operators look different and have different
  vacuum expectation values away from criticality. SIM-2026-073 (open chain, n = 24) returned
  alpha_T = 2.68 +/- 0.33 and alpha_X = 2.34 +/- 0.10 with a 4.5x amplitude ratio, verdict
  D_INDETERMINATE.
- **The challenge.** At h = 1 the TFIM is Kramers-Wannier self-dual and the duality maps
  Z_j Z_{j+1} <-> X_j. The two probes are the SAME continuum operator, the energy density
  epsilon (Delta = 1). Verified in `research/data/simulations/SIM-2026-074.json` (2026-08-24):
  vevs identical to 1.1e-15 at n = 14, force profiles identical to 1e-13 on the ring, T-vs-X
  identity 2.4e-9 at n = 24. The h = 2 control breaks the identity as it must (vev difference 0.68).
- **Changed conclusion.** (1) The registered test could never have discriminated any channel; its
  SIM-2026-073 operator contrast is an open-boundary artifact between equivalent bulk operators and
  is VOID (the INDETERMINATE verdict stands, its signal was absent, not weak). (2) Both labels were
  wrong: Z_j Z_{j+1} is the energy density, not the stress tensor (the stress tensor is the spin-2
  Koo-Saleur object of SIM-2026-067/068/069); X_j is the dual of Z_j Z_{j+1}, not the spin primary.
  (3) The true spin primary Z_j (Delta_sigma = 1/8) never appeared in the design, and the direct
  Z-vs-ZZ replacement is BLOCKED: Z_j is Z2-odd, so the energy-difference observable
  F = E_dual - E0 - 2 dE_single subtracts across parity sectors and is undefined (ring gate G2
  fails at 0.93 against a 1 percent bar; measured parity of Z|GS> is -1).
- **What survives.** On the 24-site ring with chord-distance analysis the energy-density arm gives
  alpha = 1.83 +/- 0.03 (plateau of 8 slopes at 1.87), consistent with 2 Delta_epsilon = 2 at a
  single size, NOT converged; the matched h = 2 control is CLEAN. HYP-2026-008 has no valid
  registered test until the two-probe Z2-even design (local Hamiltonian density, KW-even, leading
  T + Tbar, vs its KW-odd partner) is pre-registered and run; see
  `docs/governance/PLAN-2026-09-06.md`.
- **Where the wrong labels appear.** HYP-2026-008.json (`refutation_criteria`,
  `outstanding_killer_test`), PREREGISTRATION.md (arm table, now annotated), SIM-2026-073.json
  (annotated `operator_contrast_VOIDED_2026_08_24`), and the Zenodo v5 correction notice, which
  carries this entry's content in its withdrawal table.
- **Required action (rule 2).** Done: SIM-2026-073 annotated; SIM-2026-074 is the record of
  authority; drivers corrected 2026-09-04 so a gate-failed arm is barred from every discriminant.
  Open: HYP-2026-008.json `refutation_criteria` must be rewritten to the two-probe design once
  its pre-registration is committed.
  **Done 2026-09-07:** PREREGISTRATION-T.md committed (82b7b4e), run as SIM-2026-075, verdict VOID at
  n = 16/20/24 and in the pre-registered retry; HYP-2026-008 CLOSED as untestable at n <= 24.
  New structural fact from that run: the energy-difference force is IDENTICALLY ZERO for the KW-odd
  local energy density at h = 1, so the ring 1.83 quoted above was a KW-even/odd cross term.

## Data-record defects (non-published)

### D1 — SIM ID collisions
- **SIM-2026-011**: file `SIM-2026-011.json` is a 16q IBM Heron circuit DESIGN record; the paper's
  cited 24q force measurement actually lives in `SIM-2026-011-interaction.json` (same internal id).
  Resolution: treat `-interaction` as the record of the published result (do not rename; references exist).
- **SIM-2026-007**: double-assigned (lost penalty-VQE record + worldline MC inside worldline_mc_results.json).
- **SIM-2026-004**: never written — run killed at ~13% before the completion-time JSON write (explained gap).

### D2 — four records contain a literal `NaN` and are not valid strict JSON (RFC 8259)
- **Original entry (2026-06):** named `worldline_mc_results.json` only.
- **Corrected 2026-08-17 — the count was wrong by a factor of four.** A strict re-scan of every
  `*.json` under `research/data/` (parsing with `parse_constant` raising, which is what rejects the
  non-standard tokens) returns **four** failures, not one:
  - `builds/runpod_results/diag20_partial.json`
  - `builds/smoke_results/HYP-2026-017-results.json`
  - `simulations/SIM-2026-031.json`
  - `simulations/worldline_mc_results.json`
- **Why it went unnoticed — the check itself was the bug.** Python's `json.load` accepts `NaN`,
  `Infinity` and `-Infinity` by default as an extension to the standard, so every validation pass
  the project ran over these files reported them clean. A validator that cannot fail is worth as
  much as a test that cannot fail. Any future schema check must pass
  `parse_constant=` (or use a strict parser); consumers in other languages —
  `JSON.parse`, Go's `encoding/json`, Julia's `JSON3` — will simply reject these files.
- **Impact:** low for the science (the `NaN`s are genuinely undefined quantities, e.g. E4's
  Δ = 1/2 + √(1/4 + m²l²) under a convention that makes the radicand negative), but they make the
  affected records unreadable to any standards-conforming reader, including anyone reproducing from
  the public repo. Fix by writing `null` with a sibling field stating why the value is undefined.
- **Propagated to:** this register (D2).
- **Not yet propagated (as of 2026-08-17):** the four files themselves, and `templates/`-based
  schema validation (which must be re-run under a strict parser before it can be trusted at all).

### D3 — Schema drift: only 9/36 SIM files and 16/25 HYP files satisfy `templates/*.json`;
7 sim ids violate the id regex; 13 use non-enum `type`; 14 lack `date`. Vocabulary has diverged
(e.g. status values like SUPPORTED_AMPLITUDE, CONFIRMED_ANALYTIC not in template enum).

### D4 — Task #95 (2026-06-08) verification "killer #1" was INVERTED, corrected same day
- The #95 verdict claimed "ADAPT 33 ZZPhase vs real MERA ask ~36 = wash". The compile artifact
  `research/data/hardware/pytket_compile_chi3_8q_results.json` shows **451 ZZPhase is the REAL pytket
  compile** of the actual chi=3 8q/2-layer MERA QCUP circuit (16q register = 8 boundary + 4 top +
  4 ancilla; "36" was a pre-compile ESTIMATE, flagged as such in the artifact itself).
  Corrected statement: ADAPT-33 (real) vs chi=3-451 (real) is a genuine ~13.7× two-qubit advantage
  (~10× in HQC). The #95 no-go now rests on: fragile basin (≤0.1% angle precision), ADAPT-is-not-a-MERA
  framing (weakens the QCUP novelty claim), scaling (+5 gates/site kills generalization but NOT the
  fixed 8q deliverable), and the QCUP thread being administratively HELD.
  Minor: the "87–96%" perturbation-fail range in prose should read "86.7–100%"; p=1.51 is recomputable
  from saved L=8/L=10 points but exists in no JSON; verify_adapt_scaling.json has no L=12 leg or growth block.

### D5 — SIM-2026-036 verdict misdiagnosed an OPTIMIZER collapse as a bond-dimension ceiling
- Where: `research/data/simulations/SIM-2026-036.json` verdict ("chi=3 INSUFFICIENT for the
  multicritical TCI point... ESCALATE to chi≥4", citing PAPER-115/112 boundary/W3 mechanism), and the
  matching lines in HYP-2026-027.json, the 2026-06-16 digest, RESEARCH-LOG, and MEMORY.md.
- Problem (verified independently 2026-06-16, computation-tier feasibility check + direct re-inspection):
  the conclusion is WRONG. The chi=3 MERA has ample capacity — chi=3 captures **99.99%** of the exact TCI
  ground state's middle-cut weight (Schmidt² = 0.961, 0.034, 0.005, ...; chi=4 adds only 4e-5). The SIM-036
  converged state is a **near-product local minimum** (top Schmidt² 0.99998, S_half 0.0002, rank 4) that
  reached 0.34% energy / 0.926 overlap but never used the available entanglement. So the failure is an
  **optimizer / initialization collapse** (same family as the ADAPT fragile-basin issue), NOT a
  representational limit. The PAPER-115/112 boundary/channel-mixing mechanism was never actually tested —
  the energy run died in a product minimum first.
- Correction: chi-escalation is NOT the fix and would waste ~40 hr/seed reproducing the same collapse.
  The right next step is to **seed the chi=3 MERA from a DMRG/MPS ground state** (seconds to get; chi≤6 MPS
  hits 99.99%+) and re-optimize; only if a *well-initialized* chi=3 demonstrably saturates below S≈0.18 is
  chi=4 justified. Then read the force via the Koo-Saleur scaling superoperator (SIM-035 machinery), which
  isolates the stress-tensor channel without spatial localization. HYP-027 remains OPEN; the universality
  question was never actually answered by SIM-036 — it was answered by a broken optimizer.
- Lesson (process): "energy looks converged" is not "state is faithful." ALWAYS gate a variational state on
  entanglement/overlap, and seed from a known-good state, BEFORE concluding a capacity ceiling. Diagnostics:
  `feasibility_chi4_diagnostic.py`, `tci_schmidt_diagnostic.py`, `feasibility_chi4_timing.py`.
- Follow-up (SIM-2026-037, 2026-06-17): the *cheap* version of the D5 fix FAILED, exactly as the D5 note
  hedged. An init-scale sweep (random*{0.3,0.6,1.0}) + a one-round soft entanglement penalty
  (loss=<H>-0.5*S_half) did NOT escape the basin — best trial S_half=0.0001 vs 0.1795 exact, indistinguishable
  from SIM-036's collapse. Diagnosis: the entanglement penalty's gradient ≈ 0 *at* the product state, so a soft
  reward cannot push the optimizer uphill out of the minimum it already occupies.
- RESOLUTION (SIM-2026-039, 2026-06-17): D5 is now FULLY VINDICATED, and the root cause was even broader than
  "initialization." The probe showed the random MERA init is NOT product (S_init=1.21); the ENERGY optimizer
  DROVE the state to product under finite-difference gradients on 1246 angles. Fix = exact gradients via
  autograd (Cayley-transform unitaries replace scipy.expm which has no autograd VJP; sparse-H matvec primitive
  with VJP g->H^T g; all verified vs finite-diff to ~1e-10) PLUS a second bug fix: the objective was minimizing
  RAW energy on a state only ~60% in the Z2-even sector (rel 0.60%); minimizing the Z2-PROJECTED energy
  (physical sector, since [H,prod X]=0) dropped the Ising control to rel 0.18%. Result: with the same chi=3
  architecture, S_half went 0.0002 (SIM-036 collapse) -> 0.1336 (ratio 0.745), a ~670x increase, at rel 0.088%
  / overlap 0.9943; the Ising control PASSED the gate (S_ratio 1.040) under the identical protocol.
  TWO conclusions: (a) the SIM-036 "collapse" was 100% an optimizer+objective artifact (NOT bond-dim);
  (b) chi=3 is energy/overlap-faithful at the TCI point but reaches only ~74.5% of the half-chain entanglement
  entropy, so chi=4 IS now earned -- but ONLY on this sound footing (control-validated, optimizer ruled out),
  a fundamentally stronger basis than the retracted SIM-036 chi-4 call. NOT random×scale, NOT a DMRG seed (the
  exact GS at N=16 was the better target anyway); the actual fix was the GRADIENT ENGINE + the SECTOR-CORRECT
  OBJECTIVE. quimb DMRG was tried and abandoned (its 2-site SVD NaN'd on this build).
- CLOSURE (SIM-2026-040, 2026-06-17): chi=4 (same CHI-generalized autograd machinery, 3360 params) reaches a
  NEAR-EXACT TCI representation — Ising control rel 0.0016%/S_ratio 0.998, TCI rel 0.0061%/ov 0.9998/S_ratio
  0.980, both GATE PASS. The S_ratio jump 0.745(chi=3)->0.980(chi=4) confirms chi=3's 26% shortfall was a true
  bond-dimension effect. So the FULL picture: SIM-036 collapse = optimizer artifact (chi-irrelevant); chi=3 =
  energy-faithful/entanglement-partial; chi=4 = faithful. The retracted SIM-036 "escalate to chi>=4" reached
  the right ANSWER (chi=4) for the WRONG REASON (it cited a collapse + confounded optimizer, not the genuine
  S_ratio-0.745 capacity limit that SIM-039/040 actually measured). Representability RESOLVED; the alpha read-out
  remains a separate scale-invariant-MERA build (a faithful state does not by itself dissolve the SIM-035
  finite-N localization obstruction).

### D6 — SIM-2026-042's "TCI Δ_T~2 FOUND … UNIVERSALITY SUPPORTED" verdict was repudiated the same day it was written and the record was never amended
- **Original claim (still standing in the record).** `research/data/simulations/SIM-2026-042.json`
  (2026-06-18), field `verdict`: *"Superoperator+optimizer VALIDATED (Ising Delta_2=0.1010~0.125).
  TCI Delta_T~2 FOUND [2.110243915080525, 2.1396273166896695, 2.233223193546826]: universal stress
  tensor, alpha=2*Delta_T=4 at c=7/10. UNIVERSALITY SUPPORTED."* `status` reads
  `ISING_PASS_TCI_MEASURED`.
- **Evidence available at the time.** A χ=4 scale-invariant MERA run whose **Ising control was
  clean** (E = −4.5657, dE ~1e−9; dims [0, 0.1010, 1.034, …] = correct {0, 1/8, 1} structure →
  GATE B pass) and whose TCI leg produced a cluster of scaling dimensions near 2
  ([2.110, 2.140, 2.233]).
- **The challenge — made by the project itself, same day, in `research/RESEARCH-LOG.md:395-413`.**
  The TCI optimization **oscillated and never converged** (E bounced −4.11 to −4.12, dE ~2e−3), and
  the resulting spectrum [0, 0.473, 0.761, 0.934, 1.242, …] **misses the two lightest TCI primaries
  entirely** (σ = 0.075, ε = 0.2); the lowest non-zero dimension is 0.473. That is a **qualitative
  failure — the wrong fixed point**, not a precision shortfall. The log's own words: *"with the
  spectrum's foundation (light primaries) wrong, a near-2 cluster is as likely artifact/wrong-tower-
  descendants as T. Reading 'Delta_T~2 found' off this would be **a motivated false positive —
  explicitly NOT claimed**."* A continuation/annealing re-run the same day fixed the oscillation and
  reached an essentially identical non-CFT spectrum, isolating the blocker to the crude
  d=2→χ Hamiltonian-padding shortcut rather than the optimizer.
- **Changed conclusion.** SIM-2026-042 establishes **only** the Ising-validated superoperator
  machinery (a clean positive). It does **not** measure Δ_T at the tricritical point and does
  **not** support α-universality. The universality question was later answered on a sound footing
  by SIM-2026-051/052 (χ=6/χ=8, Δ_T = 2.007 → α = 4.01), and it is those records, not SIM-042, that
  carry HYP-2026-027.
- **The defect.** The repudiation lives only in the narrative log; the JSON record has one commit
  and still asserts "FOUND … UNIVERSALITY SUPPORTED" to any automated or human reader who queries
  the structured data. Raised as **D-19** in `docs/governance/AUDIT-2026-08-11.md`.
- **Required action (rule 2).** Add `verdict_SUPERSEDED_2026_06_18` to `SIM-2026-042.json` pointing
  to this entry and to `RESEARCH-LOG.md:395-413`, mirroring the SIM-036 pattern of D5; do not delete
  the original `verdict` string.
- **Accuracy note on the audit wording.** D-19 as written states *"the state's own c reads 0.10
  against Ising's exact 0.5."* The record contains **no central-charge field**: 0.10105 is the
  Ising control's lowest non-trivial **scaling dimension** Δ_σ (exact 1/8 = 0.125), which the log
  labels `Delta_2`. The defect is real as described above; that one clause of its supporting text
  is a misreading and should not be repeated downstream.
- **Propagated to:** this register (D6) and `SIM-2026-042.json` (`verdict_SUPERSEDED_2026_06_18`,
  dated to the repudiation with an `added_2026_08_17` provenance note inside it — **verified present
  on disk 2026-08-17**).
- **Not yet propagated:** nothing outstanding.

### D7 — the published χ=3 MERA force fit runs a fixed-sign power law through two points of the wrong sign
- **Original claim.** `research/data/simulations/SIM-2026-015d.json` `.mera` reports
  **α = 4.0712 ± 0.1778** from a fit of F(dr) = A·dr^(−α) with `fit_dr_min = 2`, `fit_n_pts = 10`
  (i.e. dr = 2…11). This is the third of the manuscript's "three independent evaluations"
  (the "4.07" in `README.md:15` and in the paper's α = 3.92 / 3.97 / 4.07 triple).
- **The defect.** `.mera.V_data` **changes sign inside the fit window**: dr = 9 gives
  **+1.2015e−3** and dr = 10 gives **+3.6517e−4**, against a negative branch everywhere else
  (dr = 8 → −3.2448e−3, dr = 11 → −7.4221e−4). A power law A·dr^(−α) cannot change sign. The fit
  therefore passes a fixed-sign model through two points of the opposite sign, and the χ=3 MERA
  force evaluation is **invalid beyond dr = 8**.
- **Consequence.** **α = 4.071 should not be quoted at all**, in any of its appearances. The
  cause has **not** been diagnosed; the leading conjecture — untested, recorded here only so it is
  not mistaken for a finding — is that χ=3 truncation error dominates the interaction energy once
  |F| falls below ~1e−3, in which case the far-window points that pull the exponent upward carry no
  signal. Testing it requires re-running the χ=3 profile at higher χ and watching where the sign
  stabilises.
- **How it was caught.** Not by the 2026-08-11 audit. It emerged from the sign audit built into the
  independent α re-analysis driver — see `research/data/simulations/SIM-2026-072.json`, field
  `results.NEW_DEFECT_sign_flips`, and E6 above.
- **Required action (rule 2).** Add `verdict_SUPERSEDED_2026_08_17` to `SIM-2026-015d.json` pointing
  to SIM-2026-072 and to this entry; restrict any future χ=3 fit to dr ≤ 8 with the noise floor
  stated, or drop the χ=3 leg entirely; remove "4.07" from the README headline row and from the
  manuscript's independence argument (which E6 shows was never independent in the first place).
- **Propagated to:** this register (D7); `SIM-2026-072.json`; `SIM-2026-015d.json`
  (`verdict_SUPERSEDED_2026_08_17`, verified present on disk 2026-08-17); `README.md` (the "4.07"
  headline row is struck); `NEXT-SESSION.md` (HOT STATE #1 carries the sign-flip defect explicitly,
  since it is the one defect the audit did not find).
- **Not yet propagated (as of 2026-08-17):** the submitted manuscript.

### D8 — HYP-2026-029 (fault-tolerant STAR budget) is conditional on a withdrawn input, and its status did not say so
- **Original claim.** HYP-2026-029 / SIM-2026-054: a static alpha = 4 holographic force fits a
  ~4.5k-qubit digital fault-tolerant budget via log-depth MERA preparation; status SUPPORTED
  (conditional, confidence low).
- **The defect.** The "alpha = 4" input is the E6 retraction. The budget arithmetic is untouched,
  but the physical claim it prices (a stress-tensor-exchange force) is not established, and the
  measured open-chain exponent (2.6, provisional) would change the target observable's scaling and
  therefore the signal-to-noise assumptions in SIM-2026-054. Not in the manuscript; repo-internal.
- **Required action (rule 2).** Add `inherits_withdrawn_input_2026_09_06` to HYP-2026-029.json
  pointing to E6/E8; status stays conditional; do not quote the 4.5k figure without the caveat.

### D9 — the SIM-2026-077 C1 "peak at the largest size" was never measured, and two controls on the surviving thread were missing from the summary

**Found:** 2026-09-08, by re-reading `research/tools/timelike-ee/sim077_C1_merged.json` directly
instead of the SIM-077 summary text. **Status: corrected in the record the same day.**

SIM-2026-077's C1 reading, and a verbal summary of it, said that at the largest size the imaginary
part *peaks* at `h_z = 0.02` and falls away on both sides as the symmetry is restored — offered as
the argument that the surviving thread is artifact-shaped.

**That measurement does not exist.** At `L = 14, delta = 5, R = 10` the stored runs are `h_z =
0.005, 0.01, 0.02` giving `Im S = 0.0766, 0.1572, 0.2795` — monotone rising, no maximum. `h_z =
0.05` and the `h_z = 0` control were never run at `L = 14`; that run was cut. The peak-and-fall
shape (`0.0622, 0.1034, 0.1957, 0.0321`) is at **L = 12, R = 8**, a different size and a different
interval length.

Two further omissions in the same summary, both material to the follow-up design:

- **The passing window is a slice of a monotone rise, not a plateau.** At the passing setting,
  `Im S` over `T0 = 2..8` is `0.2262, 0.2564, 0.2815, 0.3007, 0.3180, 0.3316, 0.3429` — a 52 percent
  drift with no flat region. The registered window `[3,5]` is three points wide and crosses the
  predicted `0.2618` on the way up. The stability gate passed because the window was narrow.
- **There is an unmeasured background.** SIM-076's exact-zero theorem holds only at `delta = 0`;
  with the regulator on and the field off, `Im S = 0.0427` (L=10) and `0.0466` (L=12). Whether that
  background grows with L has never been measured, and the signal being chased is 0.28.

**Effect on conclusions:** none on the SIM-077 verdict, which stays NO on all four candidates and a
Level-3 negative. The thread is *thinner* than the summary described, not stronger. All three facts
are carried into `PREREGISTRATION-HYP032-B.md`, which registers a matched `h_z = 0` control at every
size, a plateau condition over the full interval range, and a three-size rule.

**Class:** this is the RESEARCH-DIRECTOR §7 independence failure in operational form again — a
summary restating itself rather than the data — and the same failure named in SOUL.md: skepticism
applied to what is being built, not to what is being quoted. `docs/story/13-snapshots-along-the-worm.md`
quoted the wrong claim and was corrected the same day.

### D10 — SIM-2026-078's gate G2 was registered at a setting where it cannot converge; amended post hoc

**Found:** 2026-09-09, when the pod runner refused to start the grid. **Amended:** 2026-09-18, on
Jon's ruling (option 1 of three in `docs/governance/PLAN-2026-09-06.md`). **Status: post-hoc gate
change, recorded here before any grid point is computed.**

`PREREGISTRATION-HYP032-B.md` registered G2 as `|Im S| < 1e-8` at `h_z = 0, delta = 0` at every L,
run at L = 12/16/24 with chi = 128. It failed: `5.6e-2 / 3.05 / 2.99` (`sim078_gates.log`).

**The specification was wrong, and the error was mine.** `delta = 0` is undamped real-time
evolution, whose operator entanglement grows with the evolution time; chi = 128 cannot represent it
at L >= 12. It is not ill-conditioning (`sim078_g2_conditioning.json`: perturbing the exact tau_A
moves Im S linearly, nearest eigenvalue 1.35 rad from the branch cut) and it is not a code fault: at
L = 8, chi = 256 the MPO is exact (discarded weight 3e-28) and G2 passes at 4e-14
(`sim078_g2scan_local.json`). No production setting uses `delta = 0`; all use `delta = 5`, where G1
validates the same code path against exact diagonalization to better than 5e-7 at L = 12 and 14.

**Amended G2:** `|Im S| < 1e-8` at `h_z = 0, delta = 0` **where the MPO is exact**, meaning maximum
discarded weight below 1e-20. Run at L = 8, chi = 256. The exactness condition is part of the gate,
not decoration: at L = 8, chi = 64 a truncated run shows `|Im S| = 2e-13` while the real part is
wrong by 3.07, so the symmetry bar alone can pass on garbage. Re-run 2026-09-18 through the amended
`gate_G2()`: `5.2e-13`, discarded weight `3.4e-28`, PASS (`sim078_gates_G2_amended.json`).

**What the amendment costs.** G2 no longer tests the symmetry at any production size. At L >= 12 it
is NOT EVALUABLE, which is weaker than PASSED and must be written that way in SIM-2026-078. The
code-path check at production sizes rests on G1 alone.

**A second error, made while amending.** Re-running the gate on 2026-09-18 overwrote
`sim078_gates.json`, which held the original failed-gate result and had never been committed. The
JSON form of the original is lost. Every number in it survives in the tracked, unmodified
`sim078_gates.log` (all twelve G1 rows, the three G2 failures, `GATES: FAIL`). Nothing was
reconstructed.

**Also authorized 2026-09-18 by Jon:** one local feasibility probe at L = 32, chi = 128, setting A
(`sim078_FEASIBILITY_L32_local.*`), to learn whether the grid fits the 24 USD cap. The
pre-registration says every registered number is produced on the pod; this probe produces no
registered number and must not be quoted as one.

**Class:** a gate that could not pass, the mirror image of SIM-074's test that could not fail. The
feasibility check that would have caught it (does the gate converge at the registered chi?) was run
after the pod failed, not before the registration was approved.
