# Remediation verification — independent check of the 2026-08-17 audit-remediation pass

**Verifier:** independent agent, no edit authority over the remediated files. **Date:** 2026-08-17.
**Method:** every claimed file opened; every claimed edit grep-checked against its specific new
text; all `research/data/**/*.json` re-parsed; the §8 and retracted-number sweeps run as specified;
git state inspected. Two numerical claims were re-derived from the raw records rather than trusted.

**Bottom line.** Of the ~90 claimed edits, **every one landed**. No claim was found to be false.
Every record touched by the pass parses. Nothing was committed or pushed by the remediation pass.
**Six residual defects survive**, four of them in the two most-read files in the repository
(`README.md`, `NEXT-SESSION.md`), and one of those — the α headline in `README.md` — is the single
largest remaining hole in the correction. Separately, a stricter re-run of the JSON check found
**four pre-existing records containing literal `NaN`** (§2), untouched by this pass and
under-reported by ERRATA D2.

---

## 0. Scope discipline (checked first)

`find . -newermt "2026-08-17 06:59" -type f` returns **exactly 37 files**, and every one is on the
claimed-changed list. Specifically:

- **`research/submission-package/` was not touched.** `find research/submission-package -newermt
  "2026-08-17 06:30"` returns nothing. The manuscript remains the human's.
- No file outside the six agents' ownership lists was modified.
- `.mcp.json` shows as modified in `git status`, but that predates this session (it is in the
  session-start snapshot). It must never be committed.

---

## 1. Claim-by-claim verification

### 1.1 `research/references.bib` — ALL CLAIMS TRUE

32 `@` entries, braces balanced 314/314, 31 `eprint` fields, header comment dated 2026-08-17
present with the §32 "keys retained, never silently re-keyed" rule stated.

All 33 claimed strings found: `Kastoryano`, `Maxfield, Henry`, `A view of the bulk from the
worldline`, `Emergent Holographic Forces from Tensor Networks`, `2401.13595`, `Hardik`, `Allic`,
`Jean-Baptiste`, `Olindo`, `Conformal Fields and Operator Product Expansion`, `1901.06439`,
`Anand, Sajant`, `2203.00886`, `DeCross`, `Mitchener`, `Kosmos`, `SciSciGPT`, `2412.07727`,
`Haegeman, Jutho`, `2007.03638`, `noninteracting fermionic systems`, `0710.0692`.

Prior-art additions present: **`IoHuangHsieh2026` / arXiv:2602.02649** and
**`CouvreurJacobsenSaleur2017` / PRL 119 040601**. Methodological parents present:
`MilstedVidal2017` (1706.01436), `ZouMilstedVidal2018` (1710.05397), `MilstedVidal2018`
(1812.00529), `Bao2015` (PRD 91, 125036).

Enrichment claim spot-checked: all 8 named keys (`Vidal2007`, `Swingle2012`, `RyuTakayanagi2006`,
`EvenblyVidal2011`, `Hayden2016`, `Vasseur2019`, `OBrienFendley2018`, `PfeiferEvenblyVidal2009`)
carry an `eprint`; both `@book` entries carry a DOI.

> **Honest limit of this check.** I verified that the corrected author names, titles and identifiers
> are *present in the file*. I did **not** re-query arXiv or Crossref to confirm that the new values
> are themselves correct. The bibliography agent's per-entry primary-source table is in
> `bibliography-verification.md`; that table is unaudited by me.

### 1.2 `research/data/audit/bibliography-verification.md` — TRUE

New file, 17,820 B. Contains: §0 headline before/after table (8 wrong authors → 0; 8 wrong titles →
0; arXiv IDs 9 → 29; DOIs 11 → 24), §1 full entry table split into wrong / already-correct / added,
§2 on entries naming non-authors, §3 what was deliberately not changed, §4 a proposed process rule.

Minor: §2 is titled "the three errors…" while the claim says "four entries naming non-authors". The
section body does name a fourth (`KimSwingle2017`) inside it, so the summary claim is accurate; the
heading undercounts its own contents.

### 1.3 `SIM-2026-071.json` — ALL CLAIMS TRUE

Top-level `literature_gate` = `{run: 2026-08-17, by: qw-scientific-audit workflow, outcome:
FAILED}`. Top-level `prior_art` present with 12 sub-fields including
`original_claim_withdrawn_2026_08_17` (the priority sentence preserved verbatim),
`evidence_at_the_time`, `challenge`, `references`, `premise_also_false`, `what_remains_distinct`,
`novelty_verdict`, `search_plan_remaining`, `changed_conclusion`, `downstream_records_affected`.

`key_findings[0]` carries the inline `[AMENDED 2026-08-17: … 'The biorthogonal element structure
sees what the energy spectrum cannot.' — is WITHDRAWN as false. c = c_eff + 24*h_min …]`.
`key_findings[1]` is the cited positioning sentence naming both references. Both references carry a
`citation_verified` field stating the arXiv-export-API check and explicitly disclaiming inheritance
from the audit document.

### 1.4 `NEXT-SESSION.md` — CLAIMS TRUE (but see §4, F2)

Lines 37–50 hold the `PRIORITY CLAIM WITHDRAWN 2026-08-17` blockquote naming both prior-art works
and quoting the CJS introduction verbatim. The blockquote is closed by a blank line at L51; the
`Driver yanglee-pt/…` paragraph is not absorbed.

### 1.5 `README.md` — BOTH CLAIMED EDITS TRUE (but see §4, F1)

L198–211: the AI-priority claim is replaced by a cited positioning paragraph (Kosmos
arXiv:2511.02824, SciSciGPT, Sun et al.) plus a dated `*Withdrawn 2026-08-17:*` retraction
blockquote naming CLM-042 / D-5. L177–178 now reads "reports **what its authors describe as** the
first trapped-ion realization" — attributed, not asserted. The three "judged and left" items
(L155 verdict enum, SIM-071 caveats, NEXT-SESSION "first"/"only") are correctly not priority claims.

### 1.6 `research/ERRATA.md` — ALL CLAIMS TRUE

Verified present: the §32 standing header with all five rules and D5 → SIM-037/039/040 named as the
exemplar; the `## Current status of the record (updated 2026-08-17)` block (PRD DV13971 08-07 "with
editors"; Zenodo v4 21381474 / concept 19660302; the explicit statement that **v4 and DV13971 both
carry the E6/E7 withdrawn claims**); the 2026-07-13 paragraph relabelled `HISTORICAL STATUS …
(superseded by the block above; preserved per rule 1)` with its text intact; the pointer note under
the Zenodo-v3 heading. **E6** (α retraction, L115–197), **E7** (Yang-Lee novelty retraction,
L199–268), **D6** (SIM-042 same-day repudiation), **D7** (χ=3 sign flip) all present with the
claimed internal structure.

### 1.7 Hypothesis records — ALL 30 CLAIMS TRUE

| File | status now | confidence | new keys present |
|---|---|---|---|
| HYP-002 | PARTIALLY_CONFIRMED | medium | justified_by, justified_by_note, evidence_withdrawal_2026_08_17 |
| HYP-005 | analyzed | low | justified_by, justified_by_note |
| HYP-006 | SUPPORTED | high | justified_by, justified_by_note, correction_2026_08_17 |
| HYP-008 | **NOT_ESTABLISHED** (was SUPPORTED) | medium | status_change_2026_08_17, experimental_evidence_SUPERSEDED_2026_08_17, section8_flag_2026_08_17 |
| HYP-009 | PARTIALLY_SUPPORTED | low | status_writeback_2026_08_17 |
| HYP-010 | inconclusive | very_low | adverse_content_in_this_record_2026_08_17 |
| HYP-011 | PARTIALLY_SUPPORTED | medium | status_writeback, claim_dependency_alert_2026_08_17 |
| HYP-012 | NOT_SUPPORTED | low | status_writeback_2026_08_17 |
| HYP-013 | PARTIALLY_REFUTED | medium | status_writeback_2026_08_17 |
| HYP-014 | REFUTED | medium | status_writeback_2026_08_17 |
| HYP-015 | CONFIRMED_ANALYTIC | medium | status_writeback_2026_08_17 |
| HYP-016 | REFUTED | low | status_writeback_2026_08_17 |
| HYP-017 | SHELVED | medium | justified_by, justified_by_note |
| HYP-021 | **RETIRED** | low | prior_art, refutation_criteria, closeout_2026_08_17, feasibility_* (5 schema fields supplied) |
| HYP-022 | REFUTED | medium | status_writeback_2026_08_17 |
| HYP-023 | REFUTED | medium | justified_by, justified_by_note |
| HYP-024 | NOT_ESTABLISHED | medium | justified_by, justified_by_note |
| HYP-025 | **NOT_ESTABLISHED** (was SUPPORTED) | **low** | confidence_downgraded_2026_08_17, status_change_2026_08_17 |
| HYP-026 | SUPPORTED | medium | justified_by, justified_by_note |
| HYP-027 | **NOT_ESTABLISHED** (was the feasibility value `TESTABLE_NEAR_TERM`) | **low** | status_field_repair_2026_08_17, status_change, confidence_downgraded |
| HYP-028 | **OPEN** (was SUPPORTED) | **low** | status_change, founding_premise_correction, phase2_result_ANNOTATION |
| HYP-029 | SUPPORTED (conditional, LOW) | low | section8_flag_2026_08_17 |
| HYP-031 | PARTIALLY_SUPPORTED | medium | **NEW FILE**; refutation_criteria (a)–(e), killer_test "The L^-2 convergence killer" (NOT RUN), prior_art, pre_registered_predictions locked 2026-08-17 |

Detail spot-checks that passed:

- **HYP-006**: `T_measured` = 2.23888, `error_percent` = −1.205, `l_AdS_error_percent` = 0.714, with
  `superseded_values` preserving 2.25 / 0.72 / 0.76 verbatim under a "NOT to be quoted" note and
  naming ERRATA E1/E2.
- **HYP-028**: the `-1/5 → -2/5` issue is **flagged, not silently rewritten** — a dedicated note
  states "Delta_phi = -1/5 appears in SIX places in this record … The Yang-Lee SCALING DIMENSION is
  Delta_phi = -2/5; -1/5 is the CHIRAL WEIGHT h. The drivers use the correct value." Correct §32
  handling.
- **HYP-031**: five refutation branches, with (b) CONVERGENCE explicitly marked "CURRENTLY FAILING
  at L <= 18 and is the single most likely killer" — a pre-registration that can lose.

### 1.8 SIM supersession write-backs — ALL FOUR PRESENT

| Record | Field | Sub-fields |
|---|---|---|
| SIM-2026-011-interaction | `verdict_SUPERSEDED_2026_08_17` | summary, superseded_fits, cause, corrected_result, raw_data_NOT_in_question, see_also, correction_policy |
| SIM-2026-015d | `verdict_SUPERSEDED_2026_08_17` | + `sign_flip_defect_mera_chi3`, `not_an_independent_confirmation` |
| SIM-2026-017-statistics | `verdict_SUPERSEDED_2026_08_17` | + `alpha_equals_2_exclusion_does_not_survive`, `not_superseded_here` |
| SIM-2026-042 | `verdict_SUPERSEDED_2026_06_18` | + `field_dated_by_the_repudiation_added_2026_08_17`, `repudiation_quoted`, `central_charge_failure` |

### 1.9 `.gitignore` — TRUE AND EFFECTIVE

The un-ignores work: `git status --short` now shows **exactly 31 `.npy` files** as untracked
(theta_* 14, transport_* 8, boundary_density_* 4, *_dims 4, target_Cr_8site 1) — matching the
claimed measurement, and correcting the audit's "24 files / 432 KB" in place with the original
preserved. `git check-ignore -v research/data/simulations/gs_24q_exact.npy` returns
`.gitignore:67: research/data/simulations/gs_*.npy` — the 128 MB array is still excluded, as
intended. The reverted MERAKit `!` experiment is documented with the embedded-`.git` and
gitlink-hazard reasons.

### 1.10 `RUN-MERAKIT.md` — TRUE

`## VENDOR PROVENANCE (added 2026-08-17 — AUDIT-2026-08-11 defect D-21)`, pinned SHA `ace2f92` (×3),
MIT license, 49 local additions, Manifest.toml env. `### Correction to this file's own earlier text`
states "**There is no local pin.** `Project.toml` is byte-identical to both …" while the original
"Compat pinned to TensorOperations 3 era" line survives at L74 — correct additive §32 handling.
`### setup.jl is destructive — use instantiate.jl` quotes `rm("Manifest.toml"; force=true)`.
`### Known gaps (stated, not fixed here)` present.

### 1.11 `MANIFEST-plan.md` — TRUE

New file, 27,402 B, all nine claimed sections present (§0 measured starting state … §8 standing
rule). §0's facts independently re-checked: **`git tag` returns 0 tags**; **`f124038` exists**;
**`git log f124038..HEAD` = 18 commits**. The added-files-only gate is written as a machine-checkable
rule at L66–68.

### 1.12 `RESEARCH-LOG.md` — ALL LINE-ANCHORED CLAIMS TRUE

Header (L12–16): α struck through with `~~…~~` and replaced by **2.6 ± 0.2, channel OPEN,
SIM-2026-072**; transport restated as −1.21% at N=16 with the 0.72% named a dt=0.05 artifact;
concept DOI 19660302 in place of the stale version DOI; χ=3 and m_eff anchors annotated. L22 layout
note corrected. Backfill note at **L1021**. New entries at **L1031** (PRD submission), **L1068**
(scan #19), **L1102** (SIM-068), **L1145** (SIM-069), **L1194** (SIM-070), **L1226** (SIM-071 +
failed novelty gate), **L1302** (standard adopted), **L1325** (formal audit), **L1360** (SIM-072 α
withdrawal). File is 1,411 lines.

---

## 2. JSON validity (required check 2)

```
python -c "import json,glob
for p in glob.glob('D:/quantum-worldline/research/data/**/*.json', recursive=True): json.load(open(p,encoding='utf-8'))"
```

**TOTAL BAD: 0.** Every JSON record in `research/data/` parses under `json.load`, including all 37
files touched by the remediation pass. No agent broke a record.

**But the specified check is too weak, and re-running it strictly finds a pre-existing defect the
remediation did not touch.** Python's `json.load` accepts `NaN`/`Infinity` by default; RFC 8259 does
not. Re-run with `parse_constant` raising:

```
BAD(strict) research/data/builds/runpod_results/diag20_partial.json        NaN
BAD(strict) research/data/builds/smoke_results/HYP-2026-017-results.json   NaN
BAD(strict) research/data/simulations/SIM-2026-031.json                    NaN
BAD(strict) research/data/simulations/worldline_mc_results.json            NaN
```

**Four records contain literal `NaN` and are not valid JSON.** None was modified today — this is
pre-existing and outside every remediation agent's ownership, reported here rather than fixed. Note
that **ERRATA D2 names only one of the four** (`worldline_mc_results.json`); D2 undercounts its own
defect by three files, and the standing claim that it is a single-file problem is wrong.

---

## 3. §8 sweep (required check 3)

`grep -rniE "\b(first|novel|unprecedented|to our knowledge)\b"` over `README.md`,
`NEXT-SESSION.md`, `SIM-2026-071.json` returns **8 hits, none of them a surviving priority claim**:

| Hit | Verdict |
|---|---|
| `README.md:155` "status verdicts (NOVEL/CONFIRMED/…)" | Enum value of the project's own schema. Not a claim. **OK** |
| `README.md:178` "reports **what its authors describe as** the first trapped-ion realization" | Attributed to PAPER-137's authors, not asserted. **OK** |
| `README.md:208` "this line previously read 'This may be the first …'" | Inside the retraction quote. **OK** |
| `NEXT-SESSION.md:38–39` "This block previously read *'First lattice extraction … (to our knowledge)'*" | Inside the withdrawal quote. **OK** |
| `NEXT-SESSION.md:82` "Resize to ~1400x1000 **first**" | Ordinary adverb, Playwright note. **OK** |
| `SIM-2026-071.json:36` `original_claim_withdrawn_2026_08_17` | Preserved verbatim inside `prior_art`, as §32 requires. **OK** |
| `SIM-2026-071.json:63` "NOT NOVEL as originally claimed" | The gate verdict itself. **OK** |

**No ungated priority claim survives in the three swept files.** One is *disclosed* elsewhere:
`HYP-2026-008.json` `philosophical_implications` still contains "would constitute the first
detection of spin-dependent exchange…", but it is explicitly quarantined by the record's own
`section8_flag_2026_08_17` field and is conditional prose, not a stated result.

---

## 4. Retracted-number sweep (required check 4) — SIX SURVIVING DEFECTS

`grep -rn "0\.72\|3\.92\|3.9218"` over `README.md`, `RESEARCH-LOG.md`, `data/hypotheses/`,
`NEXT-SESSION.md`. False positives (`c=0.726`, `g₁=0.72535`, `0.725347`, `α spans 2.534–3.922`
inside E6's own re-analysis prose) are excluded below. What remains:

### F1 — HIGH — `README.md` still asserts the WITHDRAWN α headline, with no correction note anywhere

The most-read file in the repository still presents α = 3.92/3.97/4.07 as a verified result. There
is a correction blockquote at L29–33 — but it is for the **transport** number only. The α retraction
has **no README note at all**.

| Line | Text | Problem |
|---|---|---|
| 15 | `\| Holographic force exponent \| alpha = 4.0 (3 independent measurements: 3.92 / 3.97 / 4.07) \| alpha = 2*Delta_T = 4 \| ~1% \|` | The withdrawn number, in the headline table, presented as ~1% agreement. Also asserts the "three independent measurements" framing that E6 §6 explicitly retracts as lockstep, not independent. |
| 11 | "**The headline: the force exponent is alpha = 2\*Delta_T = 4**, and it does not depend on what the material is made of." | The withdrawn channel identification, stated as the project's headline. |
| 23–27 | "α = 4 is not three coincidences; it is one law measured three times… exhibiting the structural signature of gravity" | CLM-002 + CLM-004, both withdrawn/downgraded (HYP-025 and HYP-027 are now NOT_ESTABLISHED). |
| 5 | "…**universal across three conformal field theory classes** — evidence that hierarchical pattern recognition generates emergent anti-de Sitter geometry carrying **quantitative gravitational content**" | CLM-041 verbatim; the audit's verdict on it is NOT ESTABLISHED. |
| 157 | "69 simulation records … through the force law (SIM-011)" | Unmarked pointer to the superseded record. Low harm. |

**This is disclosed, not concealed** — ERRATA E6 names `README.md:15` under *Not yet propagated*, and
the README agent's ownership was scoped to §8 language. But the correction is not complete while it
stands, and a reader arriving at the repo from the Zenodo DOI reads line 15 before anything else.

### F2 — MEDIUM — `NEXT-SESSION.md` carries none of the α withdrawal, and now contradicts HYP-028

`NEXT-SESSION.md` is the file the project's own memory index instructs every new session to read
first. The single largest correction of this pass does not appear in it.

- **The α retraction is absent.** No `SIM-2026-072`, no `2.6 ± 0.2`, no mention that the force
  exponent was withdrawn.
- **L91** still reads "**Universality ladder COMPLETE**: Ising c=1/2, TCI c=7/10, Potts c=4/5 — full
  towers, **all α=4** (SIM-051/052/062/063)" — exactly the CLM-004 claim the audit classes as
  algebraically circular (α ≡ 2Δ_T, no force field in any of those four records), and for which
  HYP-025 and HYP-027 were downgraded to NOT_ESTABLISHED **in this same pass**.
- **L35** still reads "HYP-028 → **SUPPORTED (medium)**" while `HYP-2026-028.json` is now
  `status: OPEN`, `confidence: low`. The two files now disagree about the same hypothesis.
- **L3** is stale: "Last updated: **2026-08-10**", "commits through **`342fbb9`**". HEAD is
  `d17b7a2`.

### F3 — MEDIUM — `HYP-2026-008` status fell but its confidence and rationale did not

`status` is now NOT_ESTABLISHED, correctly, with a full §32 `status_change_2026_08_17` block. But:

- `confidence` is still **`medium`**. HYP-025, HYP-027 and HYP-028 each received an explicit
  `confidence_downgraded_2026_08_17` block in this pass; the one hypothesis whose *direct* support
  was withdrawn did not.
- `confidence_rationale` — a live top-level field — still reads: *"SIM-2026-011 measured alpha=3.92
  +/- 0.16 … **This is strong evidence for a power-law force consistent with spin-2 exchange.**"*
  The supersession marker was attached to `experimental_evidence`, not to this field, so the
  withdrawn number stands here unqualified.

### F4 — LOW — ERRATA E6/E7 contain statements that were already stale when written

- **E6 → *Not yet propagated*** lists "the three `verdict_SUPERSEDED_2026_08_17` write-backs". All
  three **are present** (§1.8 above). The entry hedges with "Items handled by other agents in the
  same remediation pass are tracked in AUDIT-2026-08-11.md", but the propagation ledger is the
  mechanism rule 3 exists to make reliable, and it currently under-reports its own completion.
- **E7:238** states in the present tense: *"Neither 2602.02649 nor 1611.08506 appears anywhere in
  the repository."* Both now appear in `research/references.bib` (`IoHuangHsieh2026`,
  `CouvreurJacobsenSaleur2017`) and in `SIM-2026-071.json` `prior_art`. The sentence is true of the
  state at audit time and should be tensed as such.
- Neither reference is yet catalogued in `research/data/papers/` — `NEXT-SESSION.md` and E7 both
  correctly flag this as an open action.

### F5 — LOW — residual unmarked withdrawn numbers inside `HYP-2026-006.json`

The file carries an exemplary `superseded_values` block, but two fields outside it still quote the
retracted values with no adjacent marker:

- `.experimental_evidence.mera_specificity`: "Wang & He MERA gives **T=2.25**…"
- `lin_thread_prediction_N24_error`: "0.47% (vs **0.72%** at N=16)"

A reader who finds the correction block is warned; a reader who greps is not.

### F6 — LOW — `HYP-2026-023.json` quotes the retracted 0.72% five times as a live premise

`claim`, `refutation_criteria`, `philosophical_implications`, `special_flag` and `conjecture_stage`
all rest on "a 0.72% residual" with only a `justified_by_note` added. Bounded harm — the record's
status is REFUTED — but the retracted number stands unmarked inside its prose, and ERRATA E2 says it
is not to be quoted anywhere.

### Numbers checked and found correctly handled (not defects)

`RESEARCH-LOG.md:13–14` (struck-through α, transport corrected), `:1366`/`:1374`/`:1391` (inside the
SIM-072 entry), `HYP-002:40` (`alpha: 3.9218` under an `evidence_withdrawal_2026_08_17` block),
`HYP-008:22/46/50` (under the supersession blocks), `HYP-011:3/5` (under
`claim_dependency_alert_2026_08_17`), `HYP-025:5` and `HYP-027:5` (under
`status_change_2026_08_17`), `README:29–33` (transport correction blockquote), `NEXT-SESSION:27`
(g₁ = 0.72535, unrelated).

---

## 5. Independent re-derivation (not required, done anyway)

Two load-bearing numbers were recomputed from raw records rather than trusted:

1. **The α re-analysis.** From `SIM-2026-011-interaction.json` `.F_interaction_avg`, dr ≥ 2:
   unweighted linear-space NLS gives **α = 3.9218** (reproducing the published fit exactly);
   log-space OLS on the identical window, discarding nothing, gives **α = 2.8897** — matching the
   audit's stated value to four decimals. The estimator dependence is real.
2. **ERRATA D7.** `SIM-2026-015d.json` `.mera.V_data` confirmed: dr = 9 → **+1.2015e−3**,
   dr = 10 → **+3.6517e−4**, against dr = 8 → −3.2448e−3 and dr = 11 → −7.4221e−4. A fixed-sign
   power law is being fitted through two points of the opposite sign. D7 is correct, and it is a
   defect the original audit did not find.

---

## 6. Git state (required check 5)

```
HEAD:   d17b7a2  "SIM-072: alpha = 3.92 WITHDRAWN as an estimator artifact; measured value is
                  2.6 +/- 0.2, channel OPEN"   2026-08-17 06:58:46 -0500
Tree:   127 entries in `git status --short` — UNCOMMITTED, as intended.
Push:   origin/public-release is 87 commits BEHIND HEAD. Nothing was pushed.
Tags:   0.
```

**Nothing from this remediation pass was committed.** All 37 modified/created files carry mtimes
07:01–07:14, after the 06:58:46 HEAD commit, and all 37 appear as `M`/`??` in the working tree.

**One thing the caller should know:** the session-start snapshot recorded HEAD as `9470d69`. HEAD is
now `d17b7a2`, i.e. **three commits landed on `public-release` today before the remediation pass
began** — `5130635` (adopt RESEARCH-DIRECTOR), `a82069f` (CLAUDE.md pointer), `a2ebc91` (formal
audit + D-1), `d17b7a2` (SIM-072). These predate the remediation edits and were not made by this
verifier. Local only; nothing reached `origin`.

---

## 7. What this verification did NOT establish

- **Correctness of the corrected bibliography values.** I confirmed the new author names, titles,
  DOIs and arXiv IDs are *present*. I did not re-query arXiv or Crossref to confirm they are *right*.
- **Correctness of SIM-2026-072's α = 2.6 ± 0.2 plateau.** I reproduced the estimator-dependence
  finding (3.9218 → 2.8897) but did not re-run the plateau scan, the bootstrap, or the 3 × 3 × 5
  estimator/window matrix.
- **The MANIFEST-plan's archive sizes** (~46.4 MB, ~175 MB Zenodo) and the `.gitignore` per-glob byte
  counts — I verified the *file count* (31) but not the byte totals.
- **Whether the audit's other defect IDs (D-8, D-10, D-15…D-25) were addressed.** This check covered
  only the claimed edits, not audit coverage.
- **`research/knowledge-base.md`, the digests, the learning guide and the theory prose files** —
  E6 lists these as carrying the withdrawn α and as not yet propagated. I did not sweep them; they
  were outside every agent's claimed ownership.
