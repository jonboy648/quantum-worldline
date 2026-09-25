# inv:errata-history — Correction / Retraction Register, Negative-Result Ledger, and Program Timeline

**Investigator artifact.** Governing standard: `docs/governance/RESEARCH-DIRECTOR.md` §5, §6, §7, §8, §12, §32, §38.
**Date of audit:** 2026-08-17. **HEAD at audit:** `a82069f` (branch `public-release`).
**Primary sources read in full:** `research/ERRATA.md` (140 lines), `research/RESEARCH-LOG.md` (1017 lines).
**Verification method:** every propagation claim in ERRATA was re-checked against the actual downstream file
on disk. Nothing below is taken on ERRATA's word.

---

## 0. Headline findings (before the detail)

1. **ERRATA.md is not the project's correction register — it is a snapshot of one audit.** It contains
   exactly ten entries (E1–E5, D1–D5), all originating in the 2026-06-08 full-project audit plus the
   D5 thread that ran 06-16→06-17. **Not one correction made after 2026-06-19 was ever entered into it**,
   despite at least 14 further documented corrections/retractions (§2, Class B). The file's own header
   (`research/ERRATA.md:1-6`) still describes itself as the output of the 2026-06-08 audit.
2. **ERRATA's own status block is stale.** `research/ERRATA.md:17-18` says *"Published Zenodo v3 still
   carries E1–E5; supersede with a new Zenodo version when v5 is final."* Zenodo **v4 was published
   2026-07-15** with v5 content and an explicit corrections changelog
   (`research/zenodo-v4/VERSION-NOTES.md:11-24`). The public record was fixed; the errata file was not
   told.
3. **Propagation is good into the papers and README, and materially incomplete everywhere else.**
   E1–E5 are correctly applied in the **submitted** PRD package (verified line-by-line, §3). But the
   retracted 0.72% transport number still stands, unmarked, in the hypothesis record of the transport
   anchor itself (`research/data/hypotheses/HYP-2026-006.json`, field
   `experimental_evidence.error_percent = 0.72`, `last_updated 2026-03-18`), in the anchors header of
   `research/RESEARCH-LOG.md:15`, in `research/knowledge-base.md:169`, in all three learning guides, and
   in four of the eight `research/data/theory/*.md` files.
4. **One correction was itself corrected, and the retraction of the retraction did not propagate.** The
   2026-07-20 finding "no public puMPS package exists" (`research/RESEARCH-LOG.md:988-996`, commit
   `1e7cea5`) was overturned on 2026-08-09 — the ZMV codebase **is** public at `yijian-physics/puMPS`
   (`TASKS.md:59-65`, commit `a684ebd`). `research/RESEARCH-LOG.md:988-996` and `NEXT-SESSION.md:89`
   still assert the withdrawn claim.
5. **`research/data/theory/` is NOT empty.** `docs/governance/PROJECT-REVIEW-2026-08-11.md:10` and the
   task brief both state it is. It holds **8 git-tracked markdown files** (Apr 1 – Jun 26). What is true
   is that there is no `templates/theory-*.json` schema and no structured theory record; the tier is
   prose-only. The "EMPTY" claim as written is a factual error in the review document.
6. **The hypothesis ledger contradicts the README and the memory index.** README.md:144-147 claims six
   hypotheses "refuted outright (HYP-014, 016, 022, 023 …)". On disk **only HYP-2026-023 carries
   `status: REFUTED`**. HYP-014, 016, 022, 012, 013 all still read `status: proposed`; HYP-027 still
   reads `TESTABLE_NEAR_TERM` although the project declared it SUPPORTED on 2026-06-22. The 2026-06-08
   audit diagnosed exactly this defect ("8 tested hypotheses lacked verdict write-backs",
   `research/RESEARCH-LOG.md:138`) and fixed only 017/023/024.
7. **The RESEARCH-LOG has a 3-week hole over the program's strongest results.** The chronological
   narrative ends at scan #18 (`research/RESEARCH-LOG.md:1006-1017`, 2026-07-27). It contains no entry
   for the PRD submission (08-07), scan #19 (08-09), the puMPS unblock (08-09), SIM-068, SIM-069,
   SIM-070, or **SIM-071 — the Yang–Lee result the project itself calls its strongest**
   (`docs/governance/PROJECT-REVIEW-2026-08-11.md:53-62`).
8. **Two important negatives are effectively buried in the submitted paper** (§3.2, §3.3): the
   exact-diagonalization force measurement at the tricritical point returned **α = 1.33, not 4**
   (`research/RESEARCH-LOG.md:51-53`), and the project's own diagnosis that the published α ≈ 4 survives
   *because the boundary-primary operator is tuned to the Ising point* — "a tuning that does not
   transfer to TCI" (`research/RESEARCH-LOG.md:38-39`). Neither statement appears anywhere in
   `research/submission-package/prd/paper-prd.tex`.

---

## 1. Register of formal ERRATA entries (E1–E5, D1–D5)

Legend for **Propagated?**: **YES** = verified applied in every file the entry names plus the live
files of record; **PARTIAL** = applied to the manuscript but not to the data/record layer;
**NO** = defect still present as described.

| ID | What was claimed | What was wrong | How it was caught | Propagated? |
|----|------------------|----------------|-------------------|-------------|
| E1 | l_AdS deviation "0.76%" (published v3) | Arithmetic slip; record gives 0.714% | 2026-06-08 13-agent audit, hand-verified against `composite_geodesic_results.json` | **PARTIAL** |
| E2 | Transport residual "0.72% at N=16" | dt=0.05 grid-quantization artifact; converged −1.205% | Project's own SIM-025 fine-dt re-run (2026-05-16), *not* noticed until the 06-08 audit | **PARTIAL** |
| E3 | Supplemental S1 penalty row 4.02% (SIM-2026-007) | Record lost on RunPod teardown; ID double-assigned | 06-08 audit, simulation-chain auditor | **YES** (annotated) |
| E4 | §IV.B m_eff derivation m²l²=Δ(Δ−1) | Contradicts own records, which use AdS₃ Δ(Δ−2); x₁=0.485→0.594 not 0.693 | 06-08 audit, anchors auditor | **YES** (in papers) |
| E5 | Zenodo DOI absent from paper front matter | — | 06-08 audit, repo-hygiene auditor | **PARTIAL** (see §3.5) |
| D1 | SIM ID collisions (011, 007, 004) | Two experiments share SIM-2026-011; SIM-007 double-assigned; SIM-004 never written | 06-08 audit | **NO** (documented, not fixed — by design) |
| D2 | `worldline_mc_results.json` contains literal `NaN` | Invalid strict JSON | 06-08 audit | **NO** — still broken |
| D3 | Schema drift (9/36 SIM, 16/25 HYP pass templates) | — | 06-08 audit | **PARTIAL** (improved, enum divergence persists) |
| D4 | Task #95 killer "33 vs 36 = wash" | INVERTED — 451 is the real compile; 36 was a pre-compile estimate. Real advantage ~13.7× | Adversarial verification, same day (2026-06-08) | **PARTIAL** (main fix yes, prose fix no) |
| D5 | SIM-036 verdict "χ=3 INSUFFICIENT, escalate to χ≥4" | Optimizer/objective collapse misdiagnosed as a bond-dimension ceiling | Independent computation-tier feasibility check, 2026-06-16 | **YES** (exemplary) |

### E1 — "l_AdS deviation 0.76%"
- **Source:** `research/ERRATA.md:22-27`. Record of truth: `research/data/simulations/composite_geodesic_results.json`, `l_AdS_needed_to_match_exact = 1.4323944878` vs theory `1.4426950409` → 0.714%.
- **Fixed where verified:** `research/submission-package/prd/paper-prd.tex:167,169,173` — the table now
  reads `l_AdS (theory) 1.4427` and `l_AdS deviation 1.21%` (recomputed against the converged
  T = 2.239), with the parenthetical *"(On the original coarse grid the residual appeared as 0.72% with
  an l_AdS best fit of 1.432, a 0.71% deviation; both were artifacts of dt = 0.05 grid quantization.)"*
  The wrong 0.76 does not appear in the submitted manuscript.
- **NOT fixed:** `research/paper-outline.md:107` (*"1.432 (vs theoretical 1.443, 0.76% …)"*) and
  `research/paper-outline.md:117` (*"The 0.76% gap is consistent with a finite-size correction"*) — both
  in a **git-tracked** file. `research/paper-draft.md:109,111` (untracked v4 source) likewise.

### E2 — the retraction (the project's only retraction of a *published* number)
- **Source:** `research/ERRATA.md:29-40`. Correcting record: `research/data/simulations/SIM-2026-025.json`
  (2026-05-16, dt = 1e-3): N=16 → −1.205%, N=12 → −2.777%.
- **Chronology worth preserving (§32 requirement):** the correcting run was executed **2026-05-16** and
  the errata entry was written **2026-06-08** — a 23-day window in which the project held the disproof of
  its own published number without recording it. `research/RESEARCH-LOG.md:130-132` states this plainly:
  *"no errata existed until today. Same run REFUTED HYP-023 while the memory table still said 'needs
  re-run.'"*
- **Fixed where verified (submitted PRD):** `paper-prd.tex:142` (grid caveat), `:164-169` (table with
  `Relative error (converged) −1.21%`), `:173` (finite-size trend), `:206` (N=24 double-lobe caveat),
  `:605` (conclusion restated at 1.2%), `:681` (appendix data, explicit *"the coarse-grid 0.72% was a
  quantization artifact"*), `:687` (N=24 caveat). E2 is fully and honestly applied in the manuscript.
- **Fixed in the public record:** `research/zenodo-v4/VERSION-NOTES.md:11-19` documents the retraction in
  the Zenodo v4 changelog. `README.md:29-33` carries an explicit supersession note.
  `skills/weekly-scan/SKILL.md:16` makes the corrected number a standing rule for future scans.
- **NOT fixed — the record layer (verified on disk 2026-08-17):**

| File | Line / field | Uncorrected content | Tracked? |
|---|---|---|---|
| `research/data/hypotheses/HYP-2026-006.json` | `experimental_evidence.error_percent` | `0.72`, `T_measured: 2.25`, `last_updated: 2026-03-18` | yes |
| `research/data/hypotheses/HYP-2026-006.json` | `…lin_thread_prediction_N24_error` | `"0.47% (vs 0.72% at N=16)"` — also contradicts the paper's own N=24 raw error of −31.6% | yes |
| `research/RESEARCH-LOG.md` | 15 | anchors header: *"T=(π/2)·l_AdS = 2.250 vs 2.266 (0.72% at N=16)"* | yes |
| `research/RESEARCH-LOG.md` | 12 | anchors header cites superseded **version** DOI 19661227 | yes |
| `research/knowledge-base.md` | 169 | HYP-010 row still framed on "0.72% transport time residual" | yes |
| `research/data/theory/research-primary.md` | 66, 80, 360 | *"Claim: … error = 0.72%"* presented as a verified claim | yes |
| `research/data/theory/research-practical.md` | 20 | publication-strategy text built on "transport (0.72%)" | yes |
| `research/data/theory/research-challenge.md` | 53, 68, 148, 228 | referee-simulation rates the 0.72% claim "YELLOW" — the adversarial document itself uses the retracted number | yes |
| `research/learning/physics-guide.md` | 391, 403, 499 | reader-facing: *"remarkable agreement … error = 0.72%"* | yes |
| `research/learning/intuitive-guide.md` | 123, 161 | reader-facing analogy built entirely on 0.72% | yes |
| `research/learning/connections-guide.md` | 161, 233, 259 | *"Nobody else has the 0.72% transport agreement"* — a novelty claim resting on a retracted number | yes |
| `research/paper-outline.md` | 106, 113, 117, 200, 214, 253 | headline framed as "clean headline result (0.72% transport match)" | yes |
| `research/paper-draft.md` | 13, 25, 104, 106, 135, 337, 383, 489 | the v4 manuscript source, no supersession banner | no (gitignored) |
| `research/paper-draft.html`, `research/paper-draft-pandoc.tex` | 88/136, 330 | stale build artifacts | no |

  Dated scan digests (`research/digests/2026-03-*`, `2026-05-12-*`) also carry 0.72%; those are
  point-in-time snapshots and are **correctly** left alone — digests from `2026-06-16-team-scan.md:7`
  onward all carry the corrected number with an ERRATA E2 pointer, which is the right pattern.
- **Assessment:** the manuscript layer is clean; the **evidence layer is not**. Per §32 ("preserve …
  downstream records affected") the single most serious gap is HYP-2026-006.json: an auditor or reader
  pulling the anchor's own structured record gets the retracted number with no marker.

### E3 — untraceable penalty-method row
- `research/ERRATA.md:42-47`. Verified on disk: `research/data/simulations/SIM-2026-007.json` **does not
  exist**; `SIM-2026-004.json` **does not exist**.
- **Fix applied:** `paper-prd.tex:645` — *"All ferromagnetic (JSON record lost on compute teardown;
  script preserved)"*. Same text at `research/paper-draft-scipost.tex:675`. This is the correct
  disposition and it propagated.

### E4 — m_eff convention clash
- `research/ERRATA.md:49-58`.
- **Fix applied:** `paper-prd.tex:241` gives `m_eff = √|Δ(Δ−2)|/l_AdS`; `:243` states the BF-bound
  saturation and demotes x₁=0.485 to *"corroborated by … consistent with the ε primary"*. `:579`
  further downgrades the whole m_eff agreement to *"preliminary … based on only 2 signal points and a
  post-hoc fit"*. Well handled.
- **Residual defect not tracked in ERRATA:** ERRATA E4 also notes `worldline_mc_results.json` uses a
  *third* convention Δ = 1/2 + √(1/4+m²l²) and "records NaN". That file still contains a literal `NaN`
  (see D2) and no reconciliation note was added to either data record.

### E5 — Zenodo DOI in front matter
- `research/ERRATA.md:60-62` instructed adding **10.5281/zenodo.19661227**.
- **Applied, then found to be the wrong DOI to apply.** `TASKS.md:20-23` records that on 2026-07-20 the
  manuscript was found to cite a **version** DOI rather than the **concept** DOI; `paper-prd.tex:618`
  and `cover-letter-prd.md` were corrected to **10.5281/zenodo.19660302** before the 08-07 submission.
- **Not back-ported:** `research/paper-draft-scipost.tex:37` and
  `research/submission-package/paper-draft-scipost.tex:37` both still read
  `Zenodo \href{…/10.5281/zenodo.19661227}{10.5281/zenodo.19661227}`. The SciPost-format v5 source —
  the file ERRATA names as the corrected draft — carries the defect that was fixed in the PRD build.
- **Not recorded:** the version-vs-concept DOI defect appears in `TASKS.md` and `NEXT-SESSION.md` only.
  It is a manuscript-level correction and belongs in ERRATA. It is not there.

### D1 — SIM ID collisions
- `research/ERRATA.md:66-71`. Verified: `SIM-2026-011.json` has **no internal `id` field** and is the 16q
  IBM Heron design record; `SIM-2026-011-interaction.json` carries `"id": "SIM-2026-011"` and is the
  published 24q force measurement. The documented resolution ("treat `-interaction` as the record of the
  published result; do not rename") is intact and the paper's data-availability list cites the correct
  file (`paper-prd.tex:702`). Deliberate non-fix, correctly disclosed.

### D2 — invalid JSON — **STILL BROKEN**
- `research/ERRATA.md:73`. Verified 2026-08-17: `json.load(..., parse_constant=raise)` on
  `research/data/simulations/worldline_mc_results.json` fails with *"non-standard constant: NaN"*;
  one literal `NaN` token remains. Two months open. This file is cited in the submitted paper's
  data-availability appendix (`paper-prd.tex:701`), so a referee following the data link hits an
  invalid JSON document.

### D3 — schema drift — **improved, not closed**
- `research/ERRATA.md:75-77` recorded 9/36 SIM and 16/25 HYP files passing.
- Re-measured 2026-08-17 against `templates/simulation-result.json` and `templates/hypothesis-record.json`
  (required-field check only): **SIM 27/73 pass**, **HYP 29/30 pass** (only `HYP-2026-021.json` fails,
  missing `confidence`, `source_findings`, `testable`). HYP compliance genuinely improved.
- **Vocabulary divergence persists and is now worse.** `templates/hypothesis-record.json` `status` enum
  is `[proposed, under_review, tested, refuted, supported, archived]` (all lowercase). On disk the live
  vocabulary includes `SUPPORTED`, `REFUTED`, `SHELVED`, `NOT_ESTABLISHED`, `TESTABLE_NEAR_TERM`,
  `PARTIALLY_CONFIRMED`, `analyzed`, `inconclusive`, `proposed_marginal_shielded_room_dependent`, and
  `"SUPPORTED (conditional, confidence LOW)"` — ten distinct values, six of them outside the enum.
- Compounding factor recorded in `CLAUDE.md`: the plugin is not installed, so `hooks/hooks.json` (the
  ID/format validator) "never loads and is currently inert". The mechanism that would have prevented
  D3 is disabled.

### D4 — the inverted killer (task #95)
- `research/ERRATA.md:79-89`. The verdict "ADAPT 33 ZZPhase vs real MERA ~36 = wash" was **inverted**;
  `research/data/hardware/pytket_compile_chi3_8q_results.json` shows 451 ZZPhase is the real compile.
  Corrected same day. Good practice: the artifact itself had flagged "36" as a pre-compile estimate.
- **Minor sub-corrections in D4 that did NOT propagate:** ERRATA:88 instructs that the prose
  *"87–96% perturbation-fail range should read 86.7–100%"*. `research/RESEARCH-LOG.md:159` still reads
  **"fails 0.02 gate in 87–96% of samples"**. Verified by grep — the corrected range appears nowhere in
  the log. Also unresolved per ERRATA:89: `p = 1.51` "exists in no JSON", and
  `verify_adapt_scaling.json` has no L=12 leg.

### D5 — the model correction (SIM-036) — **the best-executed correction in the record**
- `research/ERRATA.md:91-140`. A retracted verdict, a failed cheap fix (SIM-037), a root-cause probe, a
  root cause (finite-difference gradients on 1246 angles + a sector-wrong objective), a validated fix
  (autograd + Cayley + Z₂-projected energy, SIM-039), and a closure (SIM-040, χ=4) — with the honest
  coda that the retracted verdict *"reached the right ANSWER (chi=4) for the WRONG REASON"*
  (`ERRATA.md:136-138`).
- **Propagation verified:** `research/data/simulations/SIM-2026-036.json` itself contains the markers
  `ERRATA`, `D5`, and `SUPERSEDED` — the correction was written **into the corrected record**, not only
  into the errata file. This is the pattern the other nine entries should have followed.
- Also correctly propagated to `HYP-2026-027.json` (12 dated `result_note_*` keys, including
  `result_note_2026_06_16_stage2a_CORRECTION` and `result_note_2026_06_17_stage2d_RESOLVED`).

---

## 2. Class B — corrections and retractions the project made but never entered into ERRATA

These are real, documented reversals of a previously asserted position. Each is recorded *somewhere*
(log, SIM JSON, TASKS, commit message), none is in `research/ERRATA.md`. Ordered chronologically.
This is the register §32 asks for and the ERRATA file does not provide.

| # | Date | Claim withdrawn | Correct position | Where recorded | In ERRATA? |
|---|------|-----------------|------------------|----------------|-----------|
| B1 | 2026-06-12 | SIM-032b max-creation operator calibration | Failed its own validation gate (Ising 2.92 ≠ 3.97); TCI 0.56 "uninterpretable" | commit `17ead76` | no |
| B2 | 2026-06-16 | "HYP-027 has hit an exact-diag ceiling" (called after a local-operator scan only) | Premature; the *real* obstruction is the uncertainty-principle conflict between a pure Δ=2 channel and spatial localization, proven only by doing the full Zou–Milsted–Vidal construction | `RESEARCH-LOG.md:43-46` | no |
| B3 | 2026-06-18 | Scaling superoperator v0 (`_descend_channel`) | Structurally wrong — λ_max = 1.0817, identity must be λ=1; the disentangler was dropped | `RESEARCH-LOG.md:300-310` | no |
| B4 | 2026-06-18 | Superoperator v1 ("with-u one-site") after it *passed* Gate A | Demolished by the workflow's own verifier: **any** one-site superoperator is gauge-equivalent to a bare isometry channel; Gate A cannot distinguish right from wrong | `RESEARCH-LOG.md:332-352` | no |
| B5 | 2026-06-18 | "268 GB superoperator" cost estimate | Arithmetic error; the operator space is χ⁶ = 4096 → 268 **MB** | `RESEARCH-LOG.md:356-359` | no |
| B6 | 2026-06-18 | Hamiltonian corner-padding shortcut (χ-corner embedding of the d=2 OF term) | Wrong target Hamiltonian; two independent optimization paths reaching the same non-CFT spectrum proved the optimizer was innocent | `RESEARCH-LOG.md:415-429` | no |
| B7 | 2026-06-18 | Self-consistent-h variant (ascend h to fixed point) | Ad-hoc and wrong — fixed the TCI energy sign but degraded the Ising control Δ_σ 0.139→0.053; **the control caught it** | `RESEARCH-LOG.md:452-456` | no |
| B8 | 2026-06-18 | c-gate formula `c = 3(S2−S1)` | Missing `/ln 2`; corrected gate validated at 0.4985 on the exact critical Ising GS | `RESEARCH-LOG.md:509-512` | no |
| B9 | 2026-06-18 | **"Validated Ising control"** — all MERA spectra of that session | INVALIDATED: the corrected c-gate reads c = 0.10–0.19 where Ising is exactly 0.5. States looked Ising-like and were not critical. *"eyeballing the dimensions was misleading"* | `RESEARCH-LOG.md:488-495` | no |
| B10 | 2026-06-18 | "χ=6 needs RunPod" | Wrong — the estimate came from the dense superoperator; matrix-free runs in ~4 s/round locally. A RunPod deploy was fired and killed (~$0.15, mis-provisioned GPU) | `RESEARCH-LOG.md:643-648` | no |
| B11 | 2026-06-19 | TASKS T1 ("shift physical terms before lifting will fix σ") | Proven a **non-lever** by three independent arguments incl. bit-identical spectra | `RESEARCH-LOG.md:591-605` | no |
| B12 | 2026-06-19 | Hand-tuned schedule reorderings | Degrade: c diverged 0.46→3.31, unphysical for a minimal model. `uw_ISING_stable.npz` explicitly flagged **DO NOT USE (c=3.3, broken)** | `RESEARCH-LOG.md:560-573` | no |
| **B13** | **2026-06-22** | **"The OF 3-site Hamiltonian blocking into MERAKit block_size=2 form is wrong"** — the recorded blocker for *multiple sessions* | **Never wrong.** Exact-diag pre-gate shows the blocked operator reconstructs the full Hamiltonian to machine precision (0 at λ₃=0, 1.1e-16 at 0.856). The real cause: at χ=6 the energy is flat across basins (spread 3e-4) so **energy cannot select the basin** — select by spectrum | `RESEARCH-LOG.md:725-738`; memory `[[of-blocking-was-never-wrong]]` | no |
| B14 | 2026-06-26 | SIM-053's automated script verdict **REFUTED** | Overridden to INCONCLUSIVE on honest review — α≈4 reflected proximity to the unitary point, not survival at a genuine non-unitary fixed point. Also: the connected-ZZ estimator (superseded HYP-002 observable) gave a spurious α≈0.54 and was replaced by interaction energy | `RESEARCH-LOG.md:774-803`; `SIM-2026-053.json` fields `verdict_rationale`, `estimator_correction_note`, `automated_script_verdict` | no |
| B15 | 2026-06-28 | SIM-058 "MARGINAL pass" from one clean basin (seed1, C_σσε=0.485) | Collapsed under n≥3 basins: C_σσσ 0.008/0.084/1.92, C_σσε 0.485/0.897/0.812. The **best-spectrum** seed gave the **worst** OPE. Second occurrence of the same false positive | `RESEARCH-LOG.md:840-846` | no |
| B16 | 2026-07-02/03 | "Z₂-symmetric tensors are broken at target χ" | A ramp artifact, not a symmetry problem — direct-init at target χ works; the failure was a generic-gauge issue (SIM-060) | `RESEARCH-LOG.md:884-887` | no |
| B17 | 2026-07-08 | Under-convergence as the cause of the OPE drift (C_σσε 5.6% low at χ=12) | Kinematic **placement** systematic; maxiter kill-test ruled out convergence. Prescription changed to the placement average **0.50 ± 0.03** | `RESEARCH-LOG.md:901-907` | no |
| B18 | 2026-07-16 | C_TTT Route A χ=6 hits 4.20 / 3.71 | **Unclaimable.** χ-escalation made scatter worse; G4 = 0.0000 exactly while C_TTT = 25.7 — the gate certifies the chiral split but not membership in the physical {T,T̄} span | `RESEARCH-LOG.md:956-964`; `SIM-2026-066.json` `verdict`, `killer_datum` | no |
| B19 | 2026-07-19 | Equal-time ⟨hh⟩/⟨hhh⟩ cylinder design for C_TTT; and max-element T-identification | Both **falsified same-day** by ED: ⟨hh⟩_conn is negative, non-cylinder-shaped, exactly zero at antipodal separation; band-edge states have ~2× larger UV elements than T | `RESEARCH-LOG.md:970-980`; `TASKS.md:82-83` (§7 "do not reuse those formulas") | no |
| B20 | 2026-07-20 | "vendor `amilsted/puMPS` (Julia — our stack)" | Unverified web-search artifact; no such package. Two further c-extraction routes tested and declared DEAD the same day | `RESEARCH-LOG.md:988-996`; commit `1e7cea5` | no |
| **B21** | **2026-08-09** | **B20's own conclusion "no public puMPS package exists"** | Overturned: `yijian-physics/puMPS` is the authors' own public code, refreshed 2025-09-14, shipping `excitations!`, `Hn_in_basis`, and O'Brien–Fendley + 3-state Potts builders. The 07-20 check "was too narrow — it looked only for `amilsted/puMPS`, and every search engine stems 'puMPS'→'pumps'" | `TASKS.md:59-65`; commit `a684ebd` | no |
| B22 | 2026-08-10 | SIM-068 N=56 D=20 value c = 0.7008 (a "spuriously perfect" number) | **Two-error cancellation** — finite-N high bias against truncation low bias; exposed only by the D=24 re-run. Constant-D ladders or per-N D-convergence now mandatory | `SIM-2026-068.json` `key_findings[3]`, `D_systematics` | no |
| B23 | 2026-08-11 | (Trap re-confirmed) naive ED element-dominance T-identification | Would give **c = 5.9** at Potts: the max-element state is a UV state at Δ≈2.53 with 4.5× T's element | `SIM-2026-069.json` `ed_gate.extra_findings` | no |
| B24 | 2026-08-11 | The unitary T-identification discipline itself | **INVERTS at Yang–Lee**: the φ-descendant cross-module product is ~10× *larger* than T's (in unitary chains such elements are ~1e-4 suppressed). Δ-gating above the vacuum is mandatory; vacuum \|1⟩ is the **2nd** k=0 state and has a **negative** biorthogonal norm | `SIM-2026-071.json` `key_findings[2]`; `NEXT-SESSION.md:37-39` | no |
| B25 | 2026-08-11 | HYP-028's own closure ("ED route CLOSED; next = non-Hermitian MERA, NOT bigger ED") | Superseded — the question was answered **at ED scale (L≤18)** by changing the *realization* (PAPER-133 periodic PT-chain), not the method scale. Memory table now reads "old ED-closure superseded" | `SIM-2026-071.json`; memory index HYP-028 row | no |
| B26 | 2026-07-21 | (Process) Parallel arXiv theme queries | Silently **drop query lines** under the export-API burst limiter — a dropped line reads downstream as a falsely "empty" window. Three anchor-relevant lines were lost in scan #17 and re-run by hand | `RESEARCH-LOG.md:1000-1004`; `CLAUDE.md` MCP section | no |
| B27 | 2026-08-09 | (Process) arXiv `abs:"puMPS"` queries | Stem to "pump" and return the laser-physics firehose | memory scan-#19 row | no |

**Assessment.** Class B is larger and, scientifically, more consequential than Class A. B9, B13, B14,
B18, B21 and B22 are all cases where the project *asserted something and then withdrew it*, which is
exactly what §32 says must be preserved as a durable record. They survive only in a 1017-line narrative
log with no index, a set of JSON `key_findings` arrays, and commit messages. There is no way to answer
"what has this project taken back?" from `ERRATA.md`.

**Two systemic causes are visible in the register itself:**
- **Gates that cannot fail.** B4 (Gate A passes any isometric assembly), B9 (energy + one low dimension
  passes a non-critical state), B13 (energy is flat across basins), B18 (G4 = 0 exactly while the number
  is arbitrary), B15 (one clean basin). Five independent instances of a gate certifying a wrong result.
  The project caught each one, but only after acting on it.
- **Two-error cancellation** (B22) and **inverted identification rules** (B23, B24) are the same failure
  family: a wrong procedure producing a right-looking number.

---

## 3. Negative results — full ledger and surfacing assessment

**Surfacing key:** **SURFACED** = stated in `README.md` or the submitted manuscript;
**PARTIAL** = an abstracted or softened version appears; **BURIED** = present only in
`RESEARCH-LOG.md` / SIM JSON / memory.

### 3.1 Refuted, shelved and not-established hypotheses

| HYP | Project's verdict | On-disk `status` field | In README? | In paper? |
|-----|-------------------|------------------------|-----------|-----------|
| 014 (Crofton sin profile) | REFUTED (high) | **`proposed`** | named, README:144 | no |
| 022 (PEE-thread/Kirillov Crofton) | REFUTED (high) | **`proposed`** | named, README:144 | no |
| 023 (dS₂ composite-geodesic residual) | REFUTED (high) | `REFUTED` ✓ | named, README:144 | no |
| 016 (IonQ Cambridge sufficiency) | REFUTED (high) | **`proposed`** (has an un-acted `result_note_2026_06_08`) | named, README:144 | no |
| 017 (Aquila blockade-MERA) | SHELVED, 5 killers | `SHELVED` ✓ | named, README:145 | no |
| 024 (finite-T BTZ transport) | NOT_ESTABLISHED (artifact) | `NOT_ESTABLISHED` ✓ | named, README:146 | no |
| 012 (force = raw CMI) | NOT_SUPPORTED | **`proposed`** | **not mentioned** | no |
| 013 (Helios threshold) | PARTIALLY_REFUTED | **`proposed`** | not mentioned | no |
| 010 (residual ∝ l_AdS²) | INCONCLUSIVE | `inconclusive` ✓ | not mentioned | no |
| 027 (α=4 at TCI) | **SUPPORTED (high), 2026-06-22** | **`TESTABLE_NEAR_TERM`** (stale since 06-16) | implied by "universality" | §sec:universality |
| 028 (α=4 without unitarity) | SUPPORTED (medium), 2026-08-11 | `SUPPORTED` ✓ (updated 08-11) | README:146 says the route **"closed itself"** — stale by 5 days | Open-question #4 only |

- **Defect:** `README.md:144-147` says *"Six hypotheses were refuted outright (HYP-014, 016, 022, 023
  plus HYP-017 shelved … and HYP-024 …)"*. That sentence names four refutations plus two non-refutations
  and calls all six "refuted outright"; and of the four named refutations, **three carry `status:
  proposed` in the very directory the sentence points a reader to** ("Those negatives are in
  `research/data/hypotheses/` alongside the survivors, which is the point"). A reader who follows the
  pointer finds the opposite of what was claimed. `docs/governance/PROJECT-REVIEW-2026-08-11.md:50`
  independently gives a *different* count ("5 hypotheses formally REFUTED").
- **Level assignment (§5):** the refutations themselves are genuine Level-1/Level-3 negative content —
  HYP-014/022 in particular establish that *the integral-geometry route is a structural failure*
  (`memory` HYP-022 row: "integral-geometry route is the structural failure"), which is a real no-go-ish
  result. It appears in no manuscript.

### 3.2 The buried negative that bears directly on the headline claim

`research/RESEARCH-LOG.md:36-39` (2026-06-16, SIM-2026-035):

> *"the clean Δ_T=2 channel and spatial localization are **mutually exclusive at finite N**
> (uncertainty-principle obstruction). Ising control α collapses to ~1.7, TCI ~1.3. **The published α≈4
> survives only because its specific boundary operator (0.635 X-pair) is tuned to suppress that
> contamination at the Ising point — a tuning that does not transfer to TCI.**"*

And `research/RESEARCH-LOG.md:51-53` (SIM-2026-033/033b): the direct exact-diagonalization force
measurement at the tricritical point gave **α = 1.33**, rising only to 1.63 under Gram–Schmidt removal of
the lightest primaries, never reaching the pre-registered [3.6, 4.4] window — while the Ising control held
at 3.91–3.97.

- **Verified against the submitted manuscript:** `paper-prd.tex:275` defines the boundary-primary operator
  as exactly that tuned object, `σ_j = 0.635(X_j + X_{j+1}) − 0.026(X_jZ_{j+1} + Z_jX_{j+1})`. Grep of the
  full manuscript for `1.33`, `SIM-032`, `SIM-033`, `SIM-035`, `tuned`, `tuning`, `localiz`, `obstruct`
  returns **no hit** on any of these. The α=1.33 result and the tuning caveat are absent.
- **What the paper does say** (partial credit, `paper-prd.tex:329`): *"the boundary-primary operator used
  … is not the stress tensor directly; the identification … rests on the exponent matching and requires
  further theoretical justification"*; and `:592` (Open question 4): *"The transport and force-profile
  measurements, however, have been performed only at c = 1/2."*
- **Why this matters (§24).** The manuscript's universality claim is carried by a **different observable**
  (Δ_T read from the MERA scaling superoperator, `paper-prd.tex:434-457`) than the headline force
  measurement (interaction energy with the tuned operator, `:271-275`). A reader is not told that the
  force observable itself was tried at TCI and returned 1.33. **Verdict: BURIED.** This is the single
  most consequential surfacing gap found.

### 3.3 Method-level negatives (honest failures) and their surfacing

| Result | Date | Content | Surfacing |
|---|---|---|---|
| SIM-2026-035 localization obstruction | 06-16 | Clean Δ_T channel ⟂ spatial localization at finite N | **BURIED** (§3.2) |
| SIM-2026-033/033b TCI force α=1.33 | 06-08/16 | Direct force test at 2nd class fails | **BURIED** (§3.2) |
| SIM-2026-036 → 039/040 optimizer collapse chain | 06-16→17 | Retracted verdict, root-caused, closed | SURFACED in ERRATA D5; not in paper (out of scope) |
| SIM-2026-045 χ=6 Ising control FAILED | 06-19 | `verdict`: *"Ising control FAILED at chi=6 … do NOT trust TCI"* — self-invalidating record | BURIED (correct disposition: it was superseded) |
| χ=6 EV-loop ceiling (4 seeds × 1 loop) | 06-19 | *"the bottleneck is the LOOP, not the seed"* — a clean characterized negative | BURIED (`RESEARCH-LOG.md:694-707`) |
| SIM-2026-053 HYP-028 INCONCLUSIVE | 06-26 | Yang-Lee sits at the PT-breaking edge; κ_c → 0 as ~1/N | PARTIAL — README:146 mentions it, paper Open-question #4 gestures at it |
| SIM-2026-055 INVALID (G4 gate failed) | 06-26 | Two-end realization did not reach the bulk YL fixed point | BURIED |
| SIM-2026-056 / 058 / 060 OPE failures (3 successive) | 06-27→07-03 | Naive ρ³ geometry wrong; disentangler+prefactor necessary-but-insufficient; dense basins sit in a generic gauge | BURIED. The paper reports only the eventual **0.50 ± 0.03** (`paper-prd.tex:603`), with no indication it took four attempts |
| SIM-2026-059 Potts χ=8 partial | 06-28 | Δ_σ improved 0.070→0.094 but still ~30% short; only 2/8 seeds clean | PARTIAL — the paper gives the χ-progression honestly at `:455` |
| SIM-2026-064 OPE drift → placement systematic | 07-04/08 | Mean drifted 5.6% low with 40× tighter spread | SURFACED — `paper-prd.tex` quotes the placement-averaged 0.50 ± 0.03 with the systematic stated (per `ERRATA.md:16-17`) |
| **SIM-2026-066 C_TTT Route A CLOSED** | 07-16 | *"the gate stack certifies the chiral split but NOT membership in the physical {T,T̄} span"* — a genuine methodological no-go | BURIED in log/TASKS. **C_TTT was never in the paper, so no manuscript defect** — but README:19 advertises `C_TTT = 3.9936` with no mention that the first route produced 450× scatter through a perfect gate |
| Normalization no-go theorem | ~06 | PROVEN: no state-only f(ρ) gives chain-independent excess transport degradation | BURIED — memory `[[normalization-invariant-excess]]` only. This is a **Level-3 no-go result with no home in any manuscript** |
| HYP-026 "Synge distance is force-blind" | 06-08 | κ_chord ≈ 2Δ_σ, not α=4 — distance and force are owned by different operators | PARTIAL — a companion note exists (`research/note-synge-force-blind.tex`, `TASKS.md:95` "ready to post") but has **never been posted**; not in the paper |
| C_TTT imaginary at c<0 | 08-11 | `C_TTT = 2√2/√c` is imaginary at Yang–Lee: *"the graviton self-coupling does not survive as a real amplitude in the non-unitary theory"* | BURIED — `SIM-2026-071.json` `key_findings[3]` only. Directly adverse to the program's gravitational framing |
| Hardware negatives (HYP-013/016, QCUP hold) | 04→ | IBM Heron 41.2% error; QCUP stalled | SURFACED — `README.md:170-175`, `paper-prd.tex` §hardware |

### 3.4 Negatives that ARE well surfaced (credit where due)

- `README.md:29-33` — an unprompted, plainly worded retraction notice for the project's own published
  headline number, with a pointer to ERRATA. This is better practice than most published corrections.
- `README.md:144-147` and `:192-195` — the refuted hypotheses are named and the "a pipeline in which
  nothing ever fails is a pipeline that is not testing anything" framing is honest.
- `research/zenodo-v4/VERSION-NOTES.md:11-24` — the corrections are in the *public* version notes, not
  just internal files.
- `paper-prd.tex:206` (N=24 double-lobe unreliability), `:325` (anchor robustness), `:329` (operator is
  not the stress tensor), `:422` (χ=3 tail noise / sign flip), `:579` (m_eff downgraded to preliminary),
  `:586-592` (four open questions including "α could genuinely fail" at non-unitary criticality).
  The manuscript's limitation discipline is real.
- `docs/governance/PROJECT-REVIEW-2026-08-11.md:40-43` — the project states in its own governance
  document that Bin-1 results are "near-zero *discovery*" and "a referee will say so and be right".

### 3.5 Counter-weight: unverified novelty language that is currently in the record

Flagged because §8 forbids it without recorded evidence, and because these sit next to the negatives:
- `NEXT-SESSION.md:35-36` and `SIM-2026-071.json` `key_findings[1]`: *"First lattice extraction (to our
  knowledge) of a NEGATIVE central charge from stress-tensor matrix elements."* No literature gate has
  been run; `PROJECT-REVIEW-2026-08-11.md:62` itself says **"Novelty is UNVERIFIED pending the literature
  gate."** The claim is nevertheless recorded twice in the structured record.
- `SIM-2026-068.json` `key_findings[1]`: L₂ε suppression *"Not written down elsewhere as far as we
  currently know"* (per the review's phrasing) — same status.
- `README.md:197`: *"This may be the first open-source example of a multi-tier AI agent team producing
  original scientific research with quantitative results."* No supporting evidence recorded anywhere.
- `research/learning/connections-guide.md:161`: *"Nobody else has the 0.72% transport agreement"* — a
  novelty claim built on a number the project has retracted.

---

## 4. "Apply to v5+" items vs the SUBMITTED PRD package

**Scope of the instruction.** `research/ERRATA.md:5-6`: *"Apply to any future paper version (v5+) and to
the SciPost submission package BEFORE submission."* `research/ERRATA.md:8-18` then lists what was applied
on 2026-07-13. The manuscript actually submitted is
`research/submission-package/prd/paper-prd.tex` (compiled `paper-prd.pdf`, 2026-07-21; uploaded
2026-08-07, PRD accession `DV13971`, `TASKS.md:16-29`).

### 4.1 Verdict on the direct question

**Every correction explicitly listed as "apply to v5+" IS applied in the submitted PRD package.**
Line-verified, one by one:

| Instruction (ERRATA line) | Applied in `paper-prd.tex`? | Evidence |
|---|---|---|
| E1 — drop "0.76%", use recomputed l_AdS deviation | **YES** | `:167`, `:169`, `:173` (1.21% converged; coarse 0.71% explicitly labeled an artifact). String "0.76" absent |
| E2 — restate transport as grid-converged −1.21% @ N=16 with −2.78% @ N=12 | **YES** | `:142`, `:164-169`, `:173`, `:605`, `:681` |
| E2 — label coarse-grid 0.72%/0.71% as artifacts | **YES** | `:173`, `:681` (*"the coarse-grid 0.72% was a quantization artifact"*) |
| E2 — N=24 double-lobe caveat (§3.5 + App. D) | **YES** | `:206` and `:687` |
| E3 — annotate penalty row "record lost; script preserved" | **YES** | `:645` |
| E4 — rewrite §4.2 in AdS₃ convention Δ(Δ−2); 0.693 = 1/l_AdS from Δ=1 | **YES** | `:241-243` |
| E4 — downgrade x₁=0.485 to operator-identification corroboration | **YES** | `:243`, reinforced at `:579` |
| E5 — Zenodo DOI in front matter | **YES**, and improved to the **concept** DOI 10.5281/zenodo.19660302 | `:618` |
| Same-pass: fix OQ#4 / §6.5 contradiction | **YES** | `:592` consistent with `:427-457` |
| Same-pass: "six seeds within 1.5%" → "within 2%" | **YES** | `:450` (*"all six χ=8 seeds give α within 2% of 4.0"*) |
| Same-pass: data-availability lists SIM-011-interaction + universality + OPE records | **YES** | `:702`, `:706`, `:707`, `:708` |
| New in v5: Potts c=4/5 third class in §6.5 + abstract | **YES** | `:444-455` and abstract `:29` |
| New in v5: measured C_σσε = 0.50 ± 0.03 | **YES** | `:573` (with the placement systematic stated explicitly) and `:603` |

**So: no "apply to v5+" item is missing from the submitted manuscript.** The 2026-07-13 alignment pass
did what it said it did. This is the strongest single piece of evidence for the project's correction
discipline.

### 4.2 But four related defects DID reach or survive the submitted package

1. **The E5 fix was applied with the wrong DOI, corrected only in the PRD copy.**
   `research/paper-draft-scipost.tex:37` and `research/submission-package/paper-draft-scipost.tex:37`
   still read `10.5281/zenodo.19661227` — a **version** DOI. The defect was found and fixed on
   2026-07-20 for `paper-prd.tex:618` and `cover-letter-prd.md` (`TASKS.md:20-23`) but never
   back-ported. ERRATA's status block still points at `paper-draft-scipost.tex` as *the* corrected v5
   draft, so the file ERRATA certifies as corrected carries a known, separately-diagnosed defect.
   The version-vs-concept DOI correction is itself **absent from ERRATA**.

2. **A data file cited in the submitted paper is invalid JSON.** `paper-prd.tex:701` lists
   `worldline_mc_results.json` in Data and Code Availability. That file still fails strict JSON parsing
   on a literal `NaN` — ERRATA D2, open since 2026-06-08 and verified still broken 2026-08-17.

3. **The record that produced the paper's headline transport number is not in the data list.** The
   manuscript quotes T = 2.239 / −1.21% (`:142`, `:166`, `:681`). That value comes from
   `research/data/simulations/SIM-2026-025.json` (dt = 1e-3, 2026-05-16). The data-availability list
   (`:694-709`) cites `holographic_transport.json` *"(N=16 transport, T = 2.25)"* — the **superseded
   coarse-grid file** — and never cites SIM-2026-025. A referee following the data pointer retrieves the
   retracted number, not the published one. Per §21 (reproducibility standards) this is a real defect in
   the submitted package, and it is the direct fingerprint of E2 having been fixed in prose only.

4. **ERRATA's status block was never updated to record the PRD outcome.** `research/ERRATA.md:5-18`
   still frames the target as "the SciPost submission package BEFORE submission" and says the published
   Zenodo v3 "still carries E1–E5". Both statements are now false: SciPost was never submitted to
   (account never approved, `memory qcup_scipost_correspondence`), the manuscript went to PRD on
   2026-08-07, and Zenodo v4 (with the corrections) published 2026-07-15. A reader of ERRATA alone
   cannot determine whether the corrections reached the submitted paper. They did; the file does not
   say so.

5. **The appendix simulation history stops at SIM-015d** (`:640-655`), i.e. at 2026-03. Every simulation
   involved in a correction (SIM-025), a universality claim (SIM-051/052/062/063) or an OPE measurement
   (SIM-061/064) is absent from that table even though those results are in the body. Not a correction
   defect, but it removes the audit trail a referee would use.

---

## 5. Timeline of the program's major phases

Dates are anchored to git (`git log --date=short`), record `created_date` / `last_updated` fields, digest
filenames, and dated RESEARCH-LOG headers. Where a phase boundary is inferred rather than stated, it is
marked *(inferred)*.

| Phase | Dates | What defined it | Key records |
|---|---|---|---|
| **0. Origin** | early 2025 | Conversation about pattern recognition / "quantum-like" intuition → *"can math actually prove any of this?"* Motivation only, explicitly not evidence | `README.md:132-136`; memory `[[user-origin-story]]`; `docs/governance/RESEARCH-DIRECTOR.md:30-73` |
| **1. Construction & first anchors** | 2026-03-10 → 2026-03-29 | Design spec; HYP-001…012 created (`created_date` 03-10/11/26); transport and force anchors declared SUPPORTED on 03-18 (HYP-006, HYP-008 `last_updated`); scans #1–#4; **initial public release commit `78f014f` 2026-03-29** | `docs/specs/2026-03-10-quantum-worldline-design.md`; `research/digests/2026-03-17-scan-4.md`, `2026-03-18-pre-submission-scan.md` |
| **2. Paper v1–v4 and prose theory** | 2026-04-01 → 2026-05-02 | The 8 `research/data/theory/*.md` prose documents written (file dates Apr 1–3), including the self-adversarial `research-challenge.md`; HYP-013…021 created (04-26, 05-02); Zenodo v3 published (concept 19660302 / version 19661227) | `research/data/theory/*`; `research/paper-draft.md` (untracked) |
| **3. Hardware & hypothesis expansion** | 2026-05-09 → 2026-05-16 | HYP-017 Aquila smoke run (commit `eda63b1`); scan #7 → HYP-022…025; **2026-05-16: SIM-2026-025 fine-dt re-run produces −1.205%, silently invalidating the published 0.72%** and refuting HYP-023 | `SIM-2026-025.json`; `HYP-2026-023.json` (`status: REFUTED`, `last_updated 2026-05-16`) |
| **4. The audit and the retraction** | **2026-06-08** | 13-agent full-project audit (workflow `wf_c0e83471-cb7`), all findings adversarially verified, "zero false alarms". **ERRATA.md created**; E1–E5 + D1–D4 written; verdict *"the core science adds up … but the record-keeping had materially decayed"*; task #95 inverted-killer corrected same day; scans #8/#9; SIM-031 (HYP-026 force-blindness) | `research/RESEARCH-LOG.md:120-148`; `research/ERRATA.md`; commit `f3bf307` |
| **5. The χ=6 convergence war** | 2026-06-11 → 2026-06-19 | The longest and most failure-dense phase: SIM-036 retraction (D5) → SIM-037 failed fix → SIM-039/040 autograd resolution → scale-invariant MERA build with **seven** documented wrong turns (B3–B12), ending in the honest characterization *"the bottleneck is the LOOP, not the seed"* | `research/RESEARCH-LOG.md:190-716`; `ERRATA.md:91-140` |
| **6. Universality ladder** | 2026-06-22 → 2026-07-08 | MERAKit unblocks it; the **B13** root-cause reversal (OF blocking was never wrong); HYP-027 SUPPORTED (SIM-051/052); third class Potts (SIM-057/059/062/063, HYP-025 clean at χ=12); OPE pipeline validated on the 4th attempt (SIM-056→058→060→**061**), drift resolved (SIM-064) | `research/RESEARCH-LOG.md:720-907`; SIM-051/052/061/062/063/064 |
| **7. Publication push** | 2026-07-13 → 2026-08-07 | v5 alignment pass applies E1–E5 (`ERRATA.md:8-18`); **Zenodo v4 published 07-15** with a corrections changelog; 7-target outreach batch sent 07-15/19, **zero replies**; version-DOI defect found and fixed 07-20; scans #16–#18; **PRD submission 2026-08-07, accession DV13971** | `research/zenodo-v4/VERSION-NOTES.md`; `TASKS.md:14-47`; commit `f124038` |
| **8. C_TTT ladder + non-unitary frontier** | 2026-07-16 → 2026-08-11 | Route A CLOSED as an honest negative (SIM-066); Route B Ising PASS (SIM-067); puMPS false lead (B20) then unblock (B21); **SIM-068 TCI, SIM-069 Potts — ladder complete**; SIM-070/071 answer HYP-028 (c = −22/5 with sign). **None of this is in RESEARCH-LOG.md** | SIM-066…071 JSONs; `NEXT-SESSION.md:18-40`; commits `92ff5b2`…`9470d69` |
| **9. Governance reset** | 2026-08-11 → 2026-08-17 | Informal `PROJECT-REVIEW-2026-08-11.md` concludes most quantitative successes are ordinary CFT data; **`RESEARCH-DIRECTOR.md` adopted as the governing standard** (commits `5130635`, `a82069f`); this formal audit begins | `docs/governance/*` |

**Cadence observation.** Of the 37 registered corrections (10 Class A + 27 Class B), they cluster in
Phase 5 (B2–B12 plus D5 = 12) and Phase 8 (B18–B25 = 8). Phase 5's density is a *good* sign — that is a
phase in which the project was building a new pipeline and gating it hard. Phase 8's corrections (B22,
B23, B24) are all identification/systematics traps in a new method, i.e. the same signature. The two
process corrections (B26 scan-query dropping, B27 arXiv stemming) straddle Phases 7–8.

**Record-keeping cadence, by contrast, degrades monotonically after Phase 6:** ERRATA last touched
2026-06-19 (D5 closure); RESEARCH-LOG last entry 2026-07-27; TASKS.md last full rewrite 2026-08-06;
README last refreshed 2026-08-06. The project's strongest result (SIM-071, 08-11) exists in a JSON
record, a memory file, `NEXT-SESSION.md`, and a commit message — and in none of the three documents a
reader is told to consult (`README.md`, `RESEARCH-LOG.md`, `ERRATA.md`).

**Stale counts carried by the public-facing README (verified 2026-08-17):** `README.md:119` says
"69 simulation records (through SIM-067)" — on-disk high-water is **SIM-071** (73 `SIM-2026-*.json`
files); `:120` and `:159` say "18 weekly scans" — scan **#19** ran 2026-08-09
(`research/digests/2026-08-09-scan.md`, 30 digest files); `:146` says the HYP-028 exact-diagonalization
route "closed itself" — it was **answered** on 2026-08-11 (`HYP-2026-028.json` `status: SUPPORTED`,
`last_updated 2026-08-11`); `:190` says "executed 67 simulations".

---

## 6. UNVERIFIED — things I could not confirm

1. **Pre-2026-06-08 corrections.** `research/RESEARCH-LOG.md:22` states the log *"begins as the
   consolidated home from 2026-06-08 forward"* and that older history "is distributed across `memory/`
   topic files and `research/digests/`". I read the digests only where grep pointed me at them. Any
   correction made between 2026-03-10 and 2026-06-07 that was recorded **only** in a memory topic file
   or a digest is therefore not in my Class B register. The register should be treated as complete from
   2026-06-08 forward and incomplete before it.
2. **Memory topic files** (`~/.claude/projects/D--quantum-worldline/memory/*.md`) were not read. The
   memory index visible in session context was used for cross-checking status claims only. Corrections
   recorded exclusively there are not captured.
3. **Whether the retracted 0.72% appears in the PDF actually uploaded to APS.** I verified
   `paper-prd.tex` (source, modified 2026-07-21) and the presence of `paper-prd.pdf` (2026-07-21). I did
   not extract text from the PDF, and I did not verify what the APS portal holds. `TASKS.md:20-21`
   asserts the uploaded PDF is the corrected concept-DOI build; that is a project claim I did not
   independently confirm.
4. **Whether the SIM-071 "first lattice extraction … to our knowledge" claim is true.** No literature
   gate has been run by anyone, including me. I record only that the claim exists in the structured
   record without supporting evidence, which `PROJECT-REVIEW-2026-08-11.md:62` also states.
5. **`research/data/builds/` (17 records) and `research/data/hardware/` (76 records)** were not swept for
   corrections. Only `pytket_compile_chi3_8q_results.json` was touched, via ERRATA D4. Hardware-record
   corrections (e.g. superseded vendor numbers) are outside this artifact's evidence base.
6. **Zenodo v4 as published.** I verified the staged version notes at
   `research/zenodo-v4/VERSION-NOTES.md` (whose header still reads *"staged 2026-07-14, NOT yet
   published"*) and the memory record of publication. I did not fetch DOI 10.5281/zenodo.21381474 to
   confirm the live record's content matches the staged notes.
7. **Whether the two-error-cancellation systematic (B22) affects SIM-067 or SIM-071.** `SIM-2026-068.json`
   documents it for the TCI ladder and `SIM-2026-069.json` uses it predictively at Potts. I did not check
   whether the Ising (SIM-067, ED-based) or Yang–Lee (SIM-071, ED-based) results were re-examined under
   the same lens; they use a different substrate, so the systematic may not apply, but no record states
   that it was considered.
8. **Digest-level corrections.** I sampled digests via grep for the 0.72% and ERRATA strings. I did not
   read all 30 digests, so a correction announced only inside a digest body may be missing from §2.
9. **The counterfactual-novelty and independence-ledger fields required by §6/§7** do not exist in any
   record I examined. I am reporting their absence, not evaluating their content.
