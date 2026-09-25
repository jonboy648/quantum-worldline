# inv:hypotheses — Audit of all 30 hypothesis records

**Auditor:** inv:hypotheses subagent
**Date of audit:** 2026-08-17
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` (§5, §6, §7, §8, §12, §32, §36, §38)
**Corpus:** `research/data/hypotheses/HYP-2026-001.json` … `HYP-2026-030.json` (30 files).
`research/data/hypotheses/archived/` is **empty** (verified: `ls -la` returns only `.` and `..`).
`.gitkeep` present, no other records.
**Schema of record:** `templates/hypothesis-record.json`
**Cross-checks:** every `SIM-2026-*.json` in `research/data/simulations/` (verdict/status/comparison
fields read directly), `research/ERRATA.md`, `research/submission-package/prd/paper-prd.tex`.

---

## 0. Headline findings (evidence-linked)

1. **Seven hypotheses carry a `status` that their own linked SIM verdict has already overturned, and
   the record was never written back.** HYP-011, 012, 013, 014, 015, 016 and 022 all still read
   `"status": "proposed"` on disk while the SIM that tested each returned
   `PARTIALLY_SUPPORTED` / `NOT_SUPPORTED` / `PARTIALLY_REFUTED` / `REFUTED` / `CONFIRMED_ANALYTIC` /
   `REFUTED` / `REFUTED` respectively. The corrected statuses live **only** in
   `~/.claude/projects/D--quantum-worldline/memory/MEMORY.md` (outside the repository) and in the SIM
   files. Cites: `research/data/hypotheses/HYP-2026-013.json` field `status`;
   `research/data/simulations/SIM-2026-019.json` field `verdict` = `"PARTIALLY_REFUTED"`.

2. **HYP-028 is marked `SUPPORTED` against pre-registered criteria that were never satisfied, for a
   question that was silently re-scoped.** The record's `claim` is "α=4 does **not** survive a
   non-Hermitian critical point," and its `refutation_criteria` state the hypothesis is SUPPORTED only
   if α lands **outside** [3.2, 4.8] and near 2·Δ_φ. No such α was ever measured at a validated
   Yang–Lee fixed point. The `SUPPORTED` verdict rests on `phase2_result` (SIM-071, c_KS = −4.29),
   which answers a *different* question ("does Koo–Saleur carry true c off unitarity?"). This is
   goalpost movement of exactly the kind §36 forbids. Cites:
   `HYP-2026-028.json` fields `claim`, `refutation_criteria`, `status`, `phase2_result`;
   `research/data/simulations/SIM-2026-071.json` field `results.discrimination`.

3. **HYP-002 (`PARTIALLY_CONFIRMED`) is a hypothesis about *experimental verification on a quantum
   simulator* that has only ever been tested by classical exact diagonalization.** Its `claim` names
   "Quantinuum H2 (56 qubits)"; its `experimental_evidence.ground_state` reads
   `"exact eigsh, 24q OBC TFIM"`. No hardware run exists. The status is stronger than the evidence
   *in kind*, not merely in degree. Cites: `HYP-2026-002.json` fields `claim`, `hardware_required`,
   `experimental_evidence`.

4. **HYP-027's `status` field contains `"TESTABLE_NEAR_TERM"` — a feasibility-verdict value, not a
   status at all** — and its newest result note still says the universality question is "still OPEN",
   while `MEMORY.md` reports HYP-027 as SUPPORTED/high. SIM-051/052 (which *do* support it) are not
   referenced anywhere in the HYP record. The canonical record is simultaneously malformed,
   understated relative to its own evidence, and contradicted by the project's memory index. Cites:
   `HYP-2026-027.json` fields `status`, `result_note_2026_06_17_stage2d_RESOLVED`;
   `SIM-2026-051.json` fields `hypothesis_id`, `verdict`, `gate_pass`.

5. **The α=4 universality ladder is a Δ_T measurement, not a force measurement, and its sanity gate is
   the same number as its result.** HYP-025 and HYP-027 both registered a *force-exponent* test
   ("run through the established force-extraction pipeline"), but SIM-051/052/057/059/062/063 contain
   only `delta_T_statistics` — no force fit. α is then obtained as α ≡ 2Δ_T. Because each SIM's
   pass-gate is "MERA confirmed at the target c with Δ_T = 2", **passing the gate makes the result
   deterministic**: the experiment cannot return anything but α ≈ 4. Counterfactual novelty (§6):
   near-zero. Cites: `SIM-2026-051.json` keys (no force field; `delta_T_statistics`, `gate_pass`);
   `HYP-2026-027.json` field `refutation_criteria`; `HYP-2026-025.json` field `test_design`.

6. **Schema conformance has degraded since ERRATA D3.** ERRATA D3 (2026-06-08) recorded 16/25 HYP
   files valid against `templates/`. My re-check finds **13/30 clean** on the same checks
   (status enum, confidence enum, feasibility enum, required-field presence, `source_findings` minItems 2).
   14 records use a non-enum `status`; 2 a non-enum `confidence`; 3 a non-enum `feasibility_verdict`;
   1 (HYP-021) is missing three required fields. Cite: `research/ERRATA.md` §D3;
   `templates/hypothesis-record.json` lines 8, 15, 17.

7. **Seven hypotheses have never produced a single simulation record and are dormant > 60 days**
   (HYP-001, 003, 004, 007, 019, 020, 021 — 107 to 160 days). Four of them (018/019/020/021) are a
   biomagnetic-sensing / BCI line with no connection to the program trunk defined in §29.

8. **`HYP-006`'s recorded evidence block is retracted numerics that were never corrected in the
   record.** It still states `error_percent: 0.72` and `l_AdS_error_percent: 0.76`. ERRATA E2 says the
   0.72% is a dt=0.05 grid artifact (converged −1.205%); ERRATA E1 says 0.76% is arithmetically wrong
   (correct 0.714%). **The submitted manuscript is clean** — `paper-prd.tex:166` reads
   `Relative error (converged) & −1.21\%` and line 173 explicitly labels 0.72%/0.71% artifacts — so
   this is a *record* defect, not a manuscript defect. Cites: `HYP-2026-006.json` field
   `experimental_evidence`; `research/ERRATA.md` §E1, §E2; `research/submission-package/prd/paper-prd.tex:142,166,173,681`.

9. **`HYP-010`'s entire claim is premised on a number that no longer exists.** Its `claim` opens
   "The 0.72% residual … is a virtual graviton exchange correction". After ERRATA E2 there is no 0.72%
   residual. The record is `inconclusive` and dormant 153 days; it should be formally retired under §31,
   not left as an open hypothesis about a retracted quantity.

10. **A "to our knowledge / first" novelty claim has entered the evidence chain without a recorded
    literature gate.** `SIM-2026-071.json` `key_findings[1]` reads *"First lattice extraction (to our
    knowledge) of a NEGATIVE central charge from stress-tensor matrix elements"*. §8 forbids this
    labelling until the literature gate is recorded; no such record exists in
    `research/data/theory/` (empty) or in the HYP-028 record. HYP-028's `SUPPORTED` status inherits
    this unvetted claim.

---

## 1. Master table

Columns: **Stat** = recorded `status` verbatim · **Cf** = `confidence` · **Created / Updated** ·
**Dorm** = days since `last_updated` at 2026-08-17 · **SIMs** = linked simulation records
(→ = reverse-linked only, i.e. the SIM names the HYP but the HYP does not name the SIM) ·
**Kill** = killer test named per §12 (Y / weak / N) · **Fals** = concrete falsification criterion ·
**Just?** = is the recorded status justified by the linked evidence.

| ID | One-line statement | Stat | Cf | Created | Updated | Dorm | SIMs | Kill | Fals | Just? |
|---|---|---|---|---|---|---|---|---|---|---|
| 001 | Orbifold-lattice YM + qudit encoding enables 2+1D QCD on trapped ions | proposed | medium | 2026-03-10 | 2026-03-10 | 160 | — | Y | Y | n/a (untested) |
| 002 | MERA holographic forces verifiable on a 56q quantum simulator | PARTIALLY_CONFIRMED | medium | 2026-03-10 | 2026-03-18 | 152 | 011, 011-interaction, →001/002/003/005/006 | weak | Y | **NO** — no hardware run; classical ED only |
| 003 | AI-optimized lattice actions cut worldline qubit cost | proposed | low | 2026-03-10 | 2026-03-10 | 160 | — | Y | Y | n/a (untested) |
| 004 | QuPepFold VQE extended to photosynthetic exciton transport | proposed | low | 2026-03-10 | 2026-03-10 | 160 | — | Y | Y | n/a (untested) |
| 005 | Hologron force V(dr) = discretized worldline propagator in AdS bulk | analyzed | low | 2026-03-11 | 2026-03-11 | 159 | 002, 006 | **weak/self-voiding** | partial | partial (status is not an enum verdict) |
| 006 | Holographic transport time = worldline proper time, T=(π/2)·l_AdS | SUPPORTED | high | 2026-03-11 | 2026-03-18 | 152 | none named (raw JSONs only) | weak (never executed) | Y | **partial** — claim survives, evidence block retracted |
| 007 | Worldline Monte Carlo reproduces MERA hologron potential | proposed | low | 2026-03-11 | 2026-03-11 | 159 | — | Y | Y | n/a (untested) |
| 008 | Stress-tensor boundary primaries give 1/dr⁴ force | SUPPORTED | medium | 2026-03-11 | 2026-03-18 | 152 | 002, **007 (nonexistent)**, 011, 011-interaction | Y | Y | **NO** — named operator never used (record's own caveat) |
| 009 | MERA quality improves discontinuously at integer χ (CS level) | proposed | low | 2026-03-11 | 2026-03-26 | 144 | 002, 007(nonexistent), →015 (PASS) | Y | Y | **stale** — SIM-015 ran, never written back |
| 010 | The 0.72% transport residual is a virtual-graviton correction | inconclusive | very_low | 2026-03-11 | 2026-03-17 | 153 | none (raw `hyp010_criticality_scan.json`) | Y | Y | premise retracted (ERRATA E2) |
| 011 | Boundary power-law = CFT block; bulk exponential = AdS propagator | proposed | medium | 2026-03-26 | 2026-03-26 | 144 | 002, 011, →014 (PARTIALLY_SUPPORTED) | Y | Y | **stale** |
| 012 | Force V(dr) = Crofton integral of PEE thread density | proposed | low | 2026-03-26 | 2026-03-26 | 144 | 002, 007(nonexistent), 011, →013 (NOT_SUPPORTED), →016 (NOT_SUPPORTED) | Y | Y | **stale — refuted twice, still "proposed"** |
| 013 | α≈4 force detectable above NISQ noise at ≥99.5% 2q fidelity | proposed | medium | 2026-04-26 | 2026-04-26 | 113 | 015, →019 (PARTIALLY_REFUTED) | Y | Y | **stale** |
| 014 | SIM-016 σ profile matches χ=3 Crofton thread density | proposed | medium | 2026-04-26 | 2026-04-26 | 113 | 015, 015d, 016, →018 (REFUTED) | Y | Y | **stale — REFUTED on disk, "proposed" in record** |
| 015 | Weak quenched disorder will NOT improve MERA force quality | proposed | medium | 2026-04-26 | 2026-04-26 | 113 | 015, →020 (CONFIRMED_ANALYTIC) | Y | Y | **stale** |
| 016 | ≥16q + 99.5% fidelity + all-to-all needed; IonQ Cambridge viable | proposed | low | 2026-04-26 | 2026-06-08 | 70 | 015, 021, →021 (REFUTED) | Y | Y | **stale — REFUTED on disk** |
| 017 | α≈4 reproducible on Rydberg blockade-MERA (Aquila/Vela) | SHELVED | medium | 2026-04-26 | 2026-06-08 | 70 | 011, 015, 015c, 015d, 016, (→022 design) | **Y (5 named killers)** | Y | **YES — exemplary** |
| 018 | 5σ MCG at 10 m through a wall with a 2-OPM gradiometer | proposed_marginal_shielded_room_dependent | low | 2026-04-26 | 2026-06-27 | 51 | — | Y | Y | n/a (untested; off-trunk) |
| 019 | $50k Rydberg+OPM "quantum tricorder" dual-modality build | proposed | medium | 2026-04-26 | 2026-04-26 | 113 | — | Y | Y | n/a (untested; off-trunk) |
| 020 | Rydberg TEE ≡ MERA entanglement structure of our force | proposed | low | 2026-04-26 | 2026-04-26 | 113 | 015 (source only) | Y | Y | n/a (untested; off-trunk) |
| 021 | NV gradiometer reaches ~1 pT/√Hz MCG under $3k | under_review | **absent** | 2026-05-02 | **absent** | 107 | — | **N — no `refutation_criteria` field** | **N** | n/a; **record malformed** |
| 022 | PEE-thread/Kirillov Crofton salvages refuted HYP-014 | proposed | medium | 2026-05-15 | 2026-05-15 | 94 | 015d, 016, 023, →024 (REFUTED, α=0.883) | **Y (3-clause, pre-registered)** | Y | **stale — REFUTED on disk** |
| 023 | The 0.72% residual is a dS₂ composite-geodesic effect | REFUTED | medium | 2026-05-15 | 2026-05-16 | 93 | 006, 025 (REFUTED) | Y | Y | **YES** |
| 024 | Finite-T MERA transport traces a BTZ horizon-absorption curve | NOT_ESTABLISHED | medium | 2026-05-15 | 2026-06-08 | 70 | 006, 026, 027, 028, 028-L10, 029, 030 | Y | Y | **YES — downgrade from SUPPORTED_AMPLITUDE is documented** |
| 025 | α=4 is universal, tested at a third class (Z3 clock → Potts c=4/5) | SUPPORTED | medium | 2026-05-15 | 2026-07-04 | 44 | 006, 011, 015c, 023, 057, 059, (062, 063 in notes), →069 | Y | Y | **partial** — Δ_T measured, force never measured; model substituted |
| 026 | Synge distance is geometric but force-blind (κ≈0.25, not 4) | SUPPORTED | medium | 2026-06-11 | **2026-06-08** | 70 | 011, 011-interaction, 031 | Y (2-sided dichotomy) | Y | **partial** — `claim` text ("~linearly") contradicted by its own result note |
| 027 | α≈4 universal at tricritical Ising c=7/10 | **TESTABLE_NEAR_TERM** | medium | 2026-06-11 | 2026-06-16 | 62 | 015d, 023, 032, 032b, 033, 033b, 034, 035, 036, 037, 039, 040; →042/044/045/050/051/052/058/060/061/064/065/066/067/068 | Y | Y | **NO — `status` is not a status; evidence (051/052) never written back** |
| 028 | α=4 does NOT survive a non-Hermitian (Yang–Lee) critical point | SUPPORTED | medium | 2026-06-25 | 2026-08-11 | 6 | 051, 053, 055, (070/071 in `phase2_result`), →056 (mis-tag) | Y (pre-registered, 4-branch) | Y | **NO — criteria never met; question re-scoped** |
| 029 | Static α=4 force fits a ~megaquop FT STAR budget | SUPPORTED (conditional, confidence LOW) | low | 2026-06-25 | 2026-06-26 | 52 | 015d, 019, 054 | Y (3 numeric ceilings) | Y | **partial** — one costed variant breaches the SUPPORTED line |
| 030 | α=2Δ_T=4 holds along the whole c=1 compact-boson moduli line | proposed | medium | 2026-07-14 | 2026-07-14 | 34 | — (mentions 061/062 as pattern) | **weak — cannot fire** | Y | n/a (untested) |

---

## 2. Flag rollups

### (a) Statuses stronger than their evidence supports — 7 records

| ID | Recorded | Defensible | Gap |
|---|---|---|---|
| **002** | PARTIALLY_CONFIRMED | *nothing about hardware* | Claim is about experimental verification on Quantinuum H2; all evidence is 24q classical `eigsh`. |
| **008** | SUPPORTED | SUPPORTED for "α≈4 exists", not for the claim as written | `experimental_evidence.operator_caveat` states verbatim: *"Excitation used was Zou-Milsted-Vidal epsilon boundary primary (not the stress tensor T_mu_nu directly) … does not constitute direct proof that the stress tensor is the mediating operator."* The claim's whole content is the operator identity. |
| **025** | SUPPORTED | SUPPORTED for "Δ_T=2 at c=4/5" | `test_design` and `refutation_criteria` demand a **force exponent** on the **Z3 chiral clock**. Delivered: a **scaling dimension** on **3-state Potts**. Substitution is disclosed in `result_note_2026-06-27`; the *observable* substitution is not. |
| **026** | SUPPORTED | SUPPORTED for the dichotomy gate only | The `claim` field still asserts d(r) "grows ~linearly with boundary lattice separation r"; `result_note_2026_06_08_sim031` concedes the true form is d = ε·√(0.5 ln r), "monotone but sqrt-logarithmic, not linear". The claim was never edited. |
| **028** | SUPPORTED | OPEN / re-scoped | See §0.2. Under the record's own criteria, SIM-053's stable α = 4.10/4.03/4.00 at N=12/14/16 would have been a **refutation** had the G4 gate passed; the gate failed, so the correct standing verdict is INVALID/OPEN — which is exactly what `runA_note_2026-06-26` and `scan19_note` (2026-08-09, "Status UNCHANGED (OPEN/INCONCLUSIVE)") say two fields above the `SUPPORTED` status. **The record contradicts itself.** |
| **029** | SUPPORTED (conditional, LOW) | conditional-SUPPORTED, correctly hedged | `SIM-2026-054.json` `ceilings_check.ceiling2_physical_qubits`: *"high-rate ~4.5k (SUPPORTED, <5k); transversal ~9-11k (over 5k SUPPORTED line…)"*. Both variants were costed, as the pre-registered INCONCLUSIVE clause required, and they straddle the line. Strictly, INCONCLUSIVE was the registered outcome for that condition. |
| **006** | SUPPORTED / **high** | SUPPORTED / medium | Residual is −1.21%, not 0.72% (ERRATA E2). Confidence "high" was set against a number that is now 1.7× larger and of the opposite sign. Also §7 (independence): T and l_AdS both descend from the same MERA CFT calibration; this is a **consistency check**, not an independent confirmation, and the record does not say so. |

### (b) Hypotheses with no killer test (§12) — 4 records

- **HYP-021** — no `refutation_criteria` field at all. The only kill logic lives in
  `feasibility_notes` / `sensitivity_gap_analysis` (a 4.2-order-of-magnitude sensitivity gap), which is
  a feasibility screen, not a hypothesis killer.
- **HYP-005** — `refutation_criteria` opens by declaring its own unfalsifiability: *"If V(dr) has fewer
  than 5 non-zero signal points … the hypothesis is unfalsifiable at this system size."* That branch
  is what actually occurred (`confidence_rationale`: "only 2 real signal points"), so the killer was
  structurally disabled.
- **HYP-030** — the sole criterion is "a chi-converged Δ_T deviating from 2.0 by more than 2%".
  Δ_T = 2 is a theorem in every unitary 2D CFT; this criterion can only fire on an implementation bug.
  It is a pipeline test, not a killer of the physical claim (§12, §30).
- **HYP-006** — the named killer ("no systematic dependence on boundary separation, or linear rather
  than arccosh") was **never executed**. `experimental_evidence` records a single T at one
  configuration plus an N=16 vs N=24 comparison; there is no arccosh functional test anywhere in the
  record or in the linked JSONs.

Borderline (killer present but weak): **HYP-002** (a 20% deviation band on a form that was
subsequently abandoned — the record's own `what_is_refuted` says the exponential form the criterion
tests is not the right model, so the criterion is now moot and was never rewritten).

### (c) Never tested and dormant > 60 days — 7 records

| ID | Dormant (days) | SIM records | Note |
|---|---|---|---|
| 001 | 160 | none | 2+1D QCD / orbifold lattice — off the program trunk (§29) |
| 003 | 160 | none | AI-optimized lattice actions — off-trunk |
| 004 | 160 | none | photosynthetic exciton VQE — off-trunk |
| 007 | 159 | none | worldline Monte Carlo ↔ MERA equivalence — **on-trunk and never attempted** |
| 019 | 113 | none | $50k Rydberg+OPM instrument — off-trunk |
| 020 | 113 | none | Rydberg TEE ≡ MERA — off-trunk |
| 021 | 107 | none | NV MCG gradiometer — off-trunk, malformed, no killer |

Approaching the line: **HYP-018** (51 days, never tested), **HYP-030** (34 days, never tested).

None of these seven carries a §31 stop-condition record. Under §31 the correct action is a structured
retirement record ("what was attempted, what was learned, why stopped"), not indefinite `proposed`.

### (d) Vocabulary / schema violations vs `templates/hypothesis-record.json`

Template enums: `status` ∈ {proposed, under_review, tested, refuted, supported, archived} (line 17);
`confidence` ∈ {low, medium, high} (line 8); `feasibility_verdict` ∈ {TESTABLE_NOW,
TESTABLE_NEAR_TERM, TESTABLE_FUTURE, INFEASIBLE, NEEDS_REFINEMENT} (line 15);
`source_findings` minItems 2 (line 9); required = id, claim, confidence, source_findings, testable,
status, created_date (line 4).

**`status` not in enum (14):** 002 `PARTIALLY_CONFIRMED` · 005 `analyzed` · 006 `SUPPORTED` (case) ·
008 `SUPPORTED` · 010 `inconclusive` · 017 `SHELVED` · 018 `proposed_marginal_shielded_room_dependent` ·
023 `REFUTED` (case) · 024 `NOT_ESTABLISHED` · 025 `SUPPORTED` · 026 `SUPPORTED` ·
027 **`TESTABLE_NEAR_TERM`** (a feasibility value in the status slot) · 028 `SUPPORTED` ·
029 `SUPPORTED (conditional, confidence LOW)` (free prose).

**`confidence` not in enum (2):** 010 `very_low` · 021 **absent**.

**`feasibility_verdict` not in enum (3):** 009 `NEEDS_SIM` · 010 `TESTED` · 023 `REFUTED`.

**`source_findings` < 2 items (2):** 021 (field absent) · 030 (single item
`"PAPER-2026-135 (arXiv:2607.03534)"`, and the item embeds an arXiv id inside the ID string).

**Missing required fields (1):** HYP-021 — `confidence`, `source_findings`, `testable` all absent;
`last_updated` also absent.

**Date-ordering defect (1):** HYP-026 `created_date` = 2026-06-11, `last_updated` = **2026-06-08**
(update predates creation by 3 days).

**Net:** 13/30 clean on these checks (001, 003, 004, 007, 011, 012, 013, 014, 015, 016, 019, 020, 022).
ERRATA D3 recorded 16/25 clean on 2026-06-08 → **conformance rate fell from 64% to 43%**, and every
newly-added record (025–030) except 030 introduced a fresh non-enum status. The de-facto vocabulary
(`SUPPORTED`, `REFUTED`, `NOT_ESTABLISHED`, `SHELVED`, `PARTIALLY_CONFIRMED`, `analyzed`,
`inconclusive`) is now more widely used than the schema's, and is undocumented anywhere in
`templates/` or `CLAUDE.md`.

**Related SIM-side drift affecting traceability:** SIM-2026-018/019/020/021 — the four records that
tested HYP-013/014/015/016 — have **no `hypothesis_id` field at all**; the linkage exists only in
free-text `description`. SIM-2026-068/069/070/071 use a **different field name**, `hypothesis_links`
(an array of prose strings), instead of `hypothesis_id`. No machine-readable HYP↔SIM join exists
across the corpus.

### (e) Hypotheses whose supporting SIM was superseded or retracted (ERRATA cross-check)

| ID | Affected content | ERRATA entry | Record updated? |
|---|---|---|---|
| **006** | `experimental_evidence.error_percent` = 0.72; `l_AdS_error_percent` = 0.76; `best_fit_l_AdS` = 1.432 | **E2** (0.72% is a dt=0.05 grid artifact; converged −1.205%) and **E1** (0.76% is arithmetically wrong; correct 0.714%) | **NO** — last_updated 2026-03-18, five months stale |
| **010** | `claim` is *about* the 0.72% residual | E2 | **NO** — claim text still quotes 0.72% |
| **023** | `claim` quotes T=2.250 / 0.72% | E2 | Partially — status correctly REFUTED by SIM-025, but the claim text was never annotated |
| **024** | `claim` treats T=2.250 as the zero-T limit | E2 | Partially — `result_note_2026_06_08` correctly downgrades SUPPORTED_AMPLITUDE → NOT_ESTABLISHED, but the superseded 2.250 remains in the claim |
| **002, 008, 011, 012** | `source_findings` cite `SIM-2026-011` | **D1** — `SIM-2026-011.json` is a *design* record; the measurement is in `SIM-2026-011-interaction.json` | Only HYP-002 and HYP-026 point at the `-interaction` file in their evidence blocks; the `source_findings` arrays are wrong in all four |
| **008** | `test_design` step 1: *"Take the optimized MERA ground state from SIM-2026-007 (penalty VQE, 16q)"* | **E3 / D1** — no `SIM-2026-007.json` exists (lost on RunPod teardown); the ID is double-assigned to a worldline-MC run | **NO** — dangling reference still present. Same dangling ref in HYP-009 and HYP-012 `source_findings` |
| **027** | `result_note_2026_06_16_stage2a` asserts "chi=3 INSUFFICIENT … ESCALATE to chi≥4" | **D5** — retracted; the failure was an optimizer/objective artifact, not a bond-dimension ceiling | **YES** — `result_note_2026_06_08_stage2a_CORRECTION` is present and explicit. Good §32 practice, but the retracted note carries no inline `RETRACTED` marker, so a reader scanning top-down meets the wrong conclusion first |
| **028** | `runA_note_2026-06-26`, `scan18_route_note`, `scan19_note` all say OPEN/INCONCLUSIVE | none (internal) | **Contradiction left in place** — `status` says SUPPORTED while three route notes below it say OPEN |

Mis-tagging found: `SIM-2026-056.json` carries `hypothesis_id: HYP-2026-028`, but its content is the
OPE C_σσε validation gate (Ising/Z2 MERA), which belongs to the HYP-027 OPE line. Similarly
`SIM-2026-061/064/065/066/067` all carry `hypothesis_id: HYP-2026-027` although HYP-027's claim is
solely about the tricritical force exponent; the C_TTT / OPE work is a separate research line with no
hypothesis record of its own. **The C_TTT ladder — the project's most-cited recent result — has no
hypothesis record and therefore no pre-registered prediction, no killer, and no falsification
criterion.** (§36 prediction registry: absent.)

---

## 3. Per-hypothesis detail

### HYP-2026-001 — orbifold-lattice Yang–Mills + qudit encoding for 2+1D QCD
- **Status/conf:** `proposed` / `medium`. Created 2026-03-10, updated 2026-03-10 (**160 d dormant**).
- **Linked SIMs:** none. `source_findings`: PAPER-2026-001, PAPER-2026-002.
- **Killer:** yes — "If qudit-encoded orbifold circuits require MORE gates than qubit Kogut-Susskind
  circuits for the same plaquette, or if the orbifold truncation introduces artifacts…". Concrete,
  falsifiable, cheap (a gate count).
- **Justification:** n/a — untested. **Defect:** the killer is a ~1-day gate-count computation and it
  has sat undone for 160 days. Under §31 this should either be executed or formally retired. Also
  entirely off the trunk (§29) — no connection to MERA geometry.

### HYP-2026-002 — experimental verification of MERA holographic forces on a 56q simulator
- **Status/conf:** `PARTIALLY_CONFIRMED` (**not in enum**) / `medium`. Created 2026-03-10,
  updated 2026-03-18 (152 d).
- **Linked SIMs:** `SIM-2026-011` (design record — wrong file per ERRATA D1),
  `SIM-2026-011-interaction` (correct, in `experimental_evidence.data_file`). Reverse-linked:
  SIM-2026-001/002/003/005/006 all carry `hypothesis_id: HYP-2026-002`; SIM-001 `comparison` =
  `inconclusive`.
- **Killer:** weak. The registered criterion (>20% deviation from the *exponential* form) was rendered
  moot by the record's own `what_is_refuted`: *"The Sahay et al. exponential functional form … is not
  the correct governing form."* The criterion was never rewritten after the model changed.
- **Justification: NO.** The claim is explicitly about *experimental* verification on Quantinuum H2
  (`hardware_required`: "Quantinuum H2 (56 qubits, all-to-all connectivity) or equivalent").
  `experimental_evidence.ground_state` = `"exact eigsh, 24q OBC TFIM, E0=-30.199712"` — classical exact
  diagonalization. No quantum-hardware run exists anywhere in `research/data/`. A hypothesis about
  hardware feasibility cannot be `PARTIALLY_CONFIRMED` by a classical simulation.
- **Counterfactual novelty (§6):** the surviving content (power law with α = 3.92 ± 0.16 vs the
  stress-tensor value 4) is fixed by Δ_T = 2 in every 2D CFT — near-zero.
- **Honest residue:** the *negative* half is real and useful — the Sahay et al. exponential form was
  falsified as the governing form (ξ = 0.63 vs l_AdS = 1.443, 56% off), and the ZZ-correlator observable
  was shown to be the wrong observable. That is a Level-1/Level-2 finding (§5) and is recorded well.

### HYP-2026-003 — AI-optimized lattice actions reduce worldline qubit cost
- `proposed` / `low`, 2026-03-10, **160 d dormant**, **no SIMs**.
- **Killer:** yes, quantitative ("less than 2× improvement in accuracy at matched lattice spacing, or
  the fixed-point equations have no solution").
- **Justification:** n/a. **Defect:** dormant, off-trunk, no stop record.

### HYP-2026-004 — QuPepFold VQE extended to photosynthetic light-harvesting
- `proposed` / `low`, 2026-03-10, **160 d dormant**, **no SIMs**.
- **Killer:** yes ("do not reproduce known FMO energy transfer rates within 15%… or no coherent
  pathways not already captured by classical Förster theory").
- **Justification:** n/a. **Defect:** the furthest off-trunk record in the corpus (quantum biology);
  §29 explicitly names "creating disconnected hypotheses" as what *expansive* does not mean.

### HYP-2026-005 — hologron force = discretized worldline propagator
- `analyzed` (**not in enum**) / `low`, 2026-03-11, **159 d dormant**.
- **Linked SIMs:** SIM-2026-002, SIM-2026-006 (neither carries a `verdict`; SIM-005/006 have
  `hypothesis_id: HYP-2026-002`, not 005).
- **Killer: structurally disabled.** `refutation_criteria` begins: *"If V(dr) has fewer than 5 non-zero
  signal points … the hypothesis is unfalsifiable at this system size."* `confidence_rationale`
  confirms that branch fired: *"SIM-2026-002 has only 2 real signal points."* So the hypothesis
  self-declared unfalsifiable and was left there.
- **Justification:** `analyzed` is an honest label for what happened but is not a verdict and is not in
  the enum. `required_next_steps` lists five concrete actions, none of which shows any completion
  marker after 159 days.

### HYP-2026-006 — transport time = worldline proper time, T = (π/2)·l_AdS
- **Status/conf:** `SUPPORTED` / **`high`**, 2026-03-11 → 2026-03-18 (**152 d stale**).
- **Linked SIMs:** **none by ID.** Evidence points at raw files
  (`holographic_transport.json`, `composite_geodesic_results.json`). The grid-converged re-run
  (`SIM-2026-025.json`) is *not* referenced from this record; SIM-025 states
  `results.verdict_applies_to`: *"HYP-2026-023 only -- does NOT affect HYP-2026-006 headline
  (SUPPORTED)"* — a correct scoping note, but it means the correction never propagated upward.
- **Killer named:** yes in text, **never executed**. "no systematic dependence on boundary separation,
  or … linear rather than arccosh" — no arccosh functional test exists in any linked artifact.
- **Justification: PARTIAL.** The qualitative claim survives (ERRATA E2: *"the A2 anchor SURVIVES
  qualitatively"*), but every number in `experimental_evidence` is superseded:
  `error_percent: 0.72` → −1.205% (E2); `l_AdS_error_percent: 0.76` → 0.714% (E1);
  `finite_size_scaling.lin_thread_prediction_N24_error: "0.47% (vs 0.72% at N=16)"` → built on the
  retracted baseline. Confidence `high` was assigned against a 0.72% agreement; the true residual is
  −1.21%, i.e. 1.7× larger and opposite in sign.
- **Independence (§7):** T_measured and T_predicted = (π/2)·l_AdS both derive from the same MERA
  entanglement calibration of l_AdS. Classification: **primarily a consistency check**, not an
  independent confirmation. The record makes no independence statement.
- **Mitigating:** the submitted manuscript is correct — `paper-prd.tex:166` quotes −1.21%, and line 173
  explicitly labels the 0.72%/0.71% figures as dt-grid artifacts. The defect is confined to the
  hypothesis record and to `MEMORY.md`.

### HYP-2026-007 — worldline Monte Carlo reproduces the MERA hologron potential
- `proposed` / `low`, 2026-03-11, **159 d dormant**, **no SIMs**.
- **Killer:** yes ("does not reproduce the MERA tensor-network results within 30%").
- **Defect:** this is the only dormant untested record that is squarely **on the trunk** — it proposes
  an *independent method* (worldline MC) for a quantity the project measures by tensor networks, i.e.
  precisely the "genuinely independent information" §7 asks for. Note ERRATA D2: the associated
  `worldline_mc_results.json` contains a literal `NaN` (invalid strict JSON), and E4 records that this
  file's Δ convention disagrees with `effective_mass_analysis.json`. This branch is both the most
  scientifically valuable dormant item and the one with the worst data hygiene.

### HYP-2026-008 — stress-tensor boundary primaries → 1/dr⁴ force
- **Status/conf:** `SUPPORTED` / `medium`, 2026-03-11 → 2026-03-18 (152 d).
- **Linked SIMs:** SIM-2026-002; **SIM-2026-007 (does not exist — ERRATA E3/D1)**; SIM-2026-011
  (design record); SIM-2026-011-interaction (the real measurement).
- **Killer:** yes and well posed ("If V_T(dr) is indistinguishable from V_X(dr) in both functional form
  and amplitude…; if V_T(dr) is exponential (not power law), the prediction is refuted").
- **Justification: NO, as written.** The record's own `experimental_evidence.operator_caveat` states:
  *"Excitation used was Zou-Milsted-Vidal epsilon boundary primary (not the stress tensor T_mu_nu
  directly). The alpha=3.92 result is consistent with the stress-tensor prediction but does not
  constitute direct proof that the stress tensor is the mediating operator."* The claim's entire
  content is that **stress-tensor** excitation (T = −J ΣZZ) gives 1/dr⁴ *in contrast to* spin
  primaries. The differential test (V_T vs V_X) named in the killer was never run. `open_questions[2]`
  asks it explicitly and it is still open after 152 days.
- **Counterfactual novelty:** near-zero for the number (α = 2Δ_T = 4 is fixed); **moderate** for the
  operator-discrimination test that was not performed. The project measured the guaranteed half and
  skipped the informative half.
- **Dangling reference:** `test_design` step 1 names SIM-2026-007, a record that does not exist.

### HYP-2026-009 — MERA quality improves discontinuously at integer χ (Chern–Simons level)
- `proposed` / `low`, `feasibility_verdict: NEEDS_SIM` (**not in enum**), 2026-03-11 → 2026-03-26 (144 d).
- **Linked SIMs:** SIM-2026-002, SIM-2026-007 (nonexistent). Reverse: `SIM-2026-015.json` description
  = *"chi=3 MERA optimizer for 8-site TFIM (HYP-2026-009)"*, `verdict: PASS`.
- **Killer:** yes, quantitative ("If quality improvements scale smoothly with parameter count
  (improvement proportional to chi^2 within 50%)…").
- **Justification: stale.** SIM-015 ran and passed, but the record was never updated and the actual
  discontinuity test (χ = 2 vs 3 vs 4 quality curve) is not evidenced anywhere. The `PASS` refers to
  the optimizer, not to the hypothesis. Risk: a casual reader could read SIM-015's `PASS` as support
  for the CS-quantization claim. It is not.

### HYP-2026-010 — the 0.72% residual is a virtual-graviton correction
- `inconclusive` (**not in enum**) / `very_low` (**not in enum**), `feasibility_verdict: TESTED`
  (**not in enum**), 2026-03-11 → 2026-03-17 (153 d).
- **Linked SIMs:** none — evidence sits in `test_results` pointing at `hyp010_criticality_scan.json`,
  which is not a SIM record and does not appear in the simulations directory listing.
- **Killer:** yes and it fired ("If the residual shows no systematic J/Omega dependence … the
  hypothesis is refuted"). `test_results.approach_A.verdict`: *"No systematic scaling."*
- **Justification:** `inconclusive` understates it — the registered killer fired cleanly, which is a
  refutation, not an inconclusive. Worse, **the premise no longer exists**: ERRATA E2 retracts the
  0.72% the claim is about. This record should be a §31 stop-condition record, not an open hypothesis.
- **Salvage of value:** `test_results.positive_finding` is genuine and under-surfaced — the TFIM
  ring-propagation control (T ≈ 3.8 vs MERA T ≈ 2.25) is the only **matched non-holographic control**
  I found anywhere in the hypothesis corpus (§19). It is buried inside a `very_low`-confidence
  refuted record.

### HYP-2026-011 — boundary power-law = CFT block; bulk exponential = AdS propagator
- `proposed` / `medium`, 2026-03-26 (144 d).
- **Linked SIMs:** SIM-2026-002, SIM-2026-011. Reverse: `SIM-2026-014.json` description
  *"Poisson kernel integral test for HYP-2026-011"*, `verdict: PARTIALLY_SUPPORTED`.
- **Killer:** yes (α outside 3.5–4.5 ⇒ CFT block picture wrong; amplitude off by >3× ⇒ wrong).
- **Justification: stale.** Tested 2026-03-26, verdict on disk, record never written back.
  `MEMORY.md` carries PARTIAL; the repository does not.

### HYP-2026-012 — force = Crofton integral of PEE thread density
- `proposed` / `low`, 2026-03-26 (144 d).
- **Linked SIMs:** SIM-2026-002, SIM-2026-007 (nonexistent), SIM-2026-011. Reverse:
  `SIM-2026-013.json` `hypothesis: HYP-2026-012`, `crofton_verdict: NOT_SUPPORTED`
  (α_thread = 0.910 vs α_F_measured = 3.922); `SIM-2026-016.json` `verdict: NOT_SUPPORTED`.
- **Killer:** yes, and it fired twice.
- **Justification: stale and materially misleading.** Two independent SIMs returned NOT_SUPPORTED and
  the record still reads `proposed`. This is one of the "5 formally refuted hypotheses" the informal
  review (`docs/governance/PROJECT-REVIEW-2026-08-11.md` §3, Bin 2) counts as evidence of the project's
  error discipline — but the repository does not record it as refuted.

### HYP-2026-013 — α≈4 detectable above NISQ noise at ≥99.5% two-qubit fidelity
- `proposed` / `medium`, 2026-04-26 (113 d).
- **Linked SIMs:** SIM-2026-015. Reverse: `SIM-2026-019.json` (*"Helios fidelity threshold for alpha=4
  force detection"*), `verdict: PARTIALLY_REFUTED` — **no `hypothesis_id` field**.
- **Killer:** yes, two-clause and quantitative.
- **Justification: stale.** MEMORY records "Helios threshold 99.99% not 99.5%; force-existence
  dr=1..2 viable" — a partial refutation of the record's central number (99.5%) — and the record still
  asserts 99.5% as `proposed`. `feasibility_notes` also flags its own weakest link and never resolved
  it: *"Gate count for chi=3 8q circuit must be verified from SIM-2026-015 ansatz code — this is the
  one unverified assumption."*

### HYP-2026-014 — SIM-016 σ profile matches the χ=3 Crofton thread density
- `proposed` / `medium`, 2026-04-26 (113 d).
- **Linked SIMs:** SIM-2026-015, 015d, 016. Reverse: `SIM-2026-018.json` (*"Crofton thread density vs
  SIM-2026-016 sigma_by_dr"*), `verdict: REFUTED` — no `hypothesis_id` field.
- **Killer:** yes (>30% deviation at any dr after normalization).
- **Justification: stale — this is the most consequential status error in the corpus after HYP-028.**
  HYP-022 exists *solely* as a salvage of "REFUTED HYP-014" and says so in its own `claim`
  (*"HYP-2026-014 was REFUTED because it used a naive uniform-chord Crofton measure"*) and in
  `special_flag`. So the project has a downstream record that depends on HYP-014 being refuted, while
  HYP-014 itself is still labelled `proposed`. Internal inconsistency across records.
- **Note on the original evidence:** `confidence_rationale` had flagged the exact reason the test
  would be weak — *"SIM-2026-016 used chi=2 MERA (not chi=3) so the sigma data may not reflect the
  chi=3 tessellation"* — and the test was run anyway. `SIM-2026-018.json` `notes` repeats the caveat.

### HYP-2026-015 — weak quenched disorder will NOT improve MERA force quality
- `proposed` / `medium`, 2026-04-26 (113 d).
- **Linked SIMs:** SIM-2026-015. Reverse: `SIM-2026-020.json` (*"MBL disorder degrades holographic
  force: analytic perturbation theory assessment"*), `verdict: CONFIRMED_ANALYTIC` — no `hypothesis_id`.
- **Killer:** yes, and it is a genuinely good one — the hypothesis is stated as a **negative
  prediction** with the refutation being the positive outcome ("If weak disorder reduces energy error
  below 0.15% … the hypothesis is refuted"). `pipeline_provenance.conjecture_stage` explains this was
  deliberate. This is the best-designed killer in the pre-2026-05 cohort.
- **Justification: stale, and the evidence is weaker than the label.** The verdict is
  `CONFIRMED_ANALYTIC` — an *analytic perturbation-theory assessment*, not the 20-run GPU disorder
  sweep the `test_design` specifies (5 realizations × 4 W values, ~9 h). MEMORY concedes "needs GPU
  confirm". So the record is stale *and* the SIM answered a cheaper question than the one registered.

### HYP-2026-016 — ≥16q + 99.5% fidelity + all-to-all; IonQ Cambridge viable
- `proposed` / `low`, 2026-04-26 → 2026-06-08 (70 d).
- **Linked SIMs:** SIM-2026-015, SIM-2026-021. `SIM-2026-021.json` `verdict: REFUTED` — no
  `hypothesis_id` field.
- **Killer:** yes, two-clause and numeric.
- **Justification: stale.** REFUTED on disk since ~2026-04; the record was touched on 2026-06-08 to add
  `result_note_2026_06_08` (an FT atom-count refresh: 1839 → 75–1500 atoms) **without changing the
  status**. So an editor did open this file after the refutation and left `proposed` in place. That
  makes this an omission of commission rather than mere neglect.

### HYP-2026-017 — α≈4 reproducible on a Rydberg blockade-MERA
- `SHELVED` (**not in enum**) / `medium`, 2026-04-26 → 2026-06-08 (70 d).
- **Linked SIMs:** SIM-2026-011, 015, 015c, 015d, 016; design/cost record `SIM-2026-022`
  (`verdict: FEASIBLE_MARGINAL`).
- **Killer: YES — five named killers, documented before the interpretation.** `result_note_2026_06_08`
  lists R1–R5 (hologron decay timescale; product-density estimator dropping connected correlators;
  wrong S_topo prediction; biased single-basis TEE estimator; production script never run end-to-end),
  plus the decisive empirical fact (*"local smoke run produced F>0 vs literature F<0 — root cause
  structural"*) and the 15-atom exact-diag validator verdict.
- **Justification: YES.** This is the exemplar record of the corpus. It documents the killers, the
  date they were raised (2026-05-05 devil's-advocate NO_GO), the shelving date, the cancelled $115 AWS
  spend, the scope of downstream impact ("paper v4 alpha~4 results unaffected"), and where the full
  closeout lives. Everything §12 and §31 ask for. **Recommendation: use this record's shape as the
  template for retiring HYP-001/003/004/007/010/019/020/021.**
- Only defect: `SHELVED` is not an enum value (the schema's nearest is `archived`).

### HYP-2026-018 — 5σ MCG at 10 m through a wall (2× OPM gradiometer)
- `proposed_marginal_shielded_room_dependent` (**not in enum; a sentence used as a status**) / `low`,
  2026-04-26 → 2026-06-27 (51 d). **No SIMs.**
- **Killer:** yes, two-clause with numeric floors (noise floor >500 fT/√Hz after gradiometric
  subtraction; SNR <2σ at 10 m/300 s).
- **Justification:** n/a — untested. **Defect:** off-trunk; and the status string encodes the *answer*
  (marginal, shielded-room dependent) inside the status slot rather than in a verdict field.

### HYP-2026-019 — $50k Rydberg + OPM "quantum tricorder"
- `proposed` / `medium`, 2026-04-26 (**113 d dormant**). **No SIMs.**
- **Killer:** yes, and unusually well structured (a specific sub-claim "cannot share chassis" with its
  own refutation condition, plus two overall conditions).
- **Justification:** n/a. **Defect:** off-trunk instrument-building; 113 days untouched; no stop record.

### HYP-2026-020 — Rydberg TEE ≡ MERA entanglement structure
- `proposed` / `low`, 2026-04-26 (**113 d dormant**). SIM-2026-015 appears only as a `source_finding`.
- **Killer:** yes, but note the criterion (a) is *"TEE = 0 at the Rydberg PXP operating point"* —
  and HYP-017's `result_note_2026_06_08` records R3/R4 (wrong S_topo prediction, biased single-basis
  TEE estimator) as killers of the closely related Aquila TEE measurement. That finding was never
  propagated to HYP-020, which is arguably already dead by the same argument.
- **Justification:** n/a. **Defect:** dormant + un-propagated adverse finding from a sibling record.

### HYP-2026-021 — NV gradiometer MCG mapper
- `under_review` (in enum) / **no `confidence` field**, created 2026-05-02, **no `last_updated`**
  (107 d by creation date). **No SIMs.**
- **Killer: NONE.** No `refutation_criteria` field exists. The kill logic that does exist is a
  feasibility screen: `sensitivity_gap_analysis` records a 4.2-order-of-magnitude gap and states
  *"this candidate likely fails the sensitivity gate unless laser is added"*; `feasibility_metrics`
  = `{sensitivity_gap_orders_of_magnitude: 4.2, laser_required: true, bom_under_3k_realistic: false}`.
- **Schema:** missing three required fields (`confidence`, `source_findings`, `testable`). Uses a
  wholly different field set (`physics`, `novelty`, `bom_estimate`, `prior_art`,
  `sensitivity_gap_analysis`) that appears in no template.
- **Justification:** n/a. **Defect:** `result_note_2026_06_08` is candid — *"This record was created
  2026-05-02 but never feasibility-gated and is absent from all weekly digests and the MEMORY status
  table"* — i.e. an orphan the project has already identified and then left in place for another
  67 days. Under §31 this is the clearest retire-or-repair candidate in the corpus.

### HYP-2026-022 — PEE-thread / Kirillov Crofton salvage of HYP-014
- `proposed` / `medium`, 2026-05-15 (94 d). `speculative_flag: false`.
- **Linked SIMs:** SIM-2026-015d, 016, 023. Reverse: `SIM-2026-024.json`
  `hypothesis_id: HYP-2026-022`, `results.verdict: REFUTED`,
  `verdict_reason: "alpha=0.883 outside acceptance window [3.2, 4.8]. PEE-thread re-weighting does not
  recover the known alpha~4. HYP-014 stays refuted."`
- **Killer: YES — three pre-registered clauses (a)/(b)/(c) including a regulator-stability clause**
  ("alpha varies by more than ±0.5 as theta_min is swept over [pi/(2N), 2pi/N]"). This is the best
  pre-registration in the corpus and it names a *systematic* failure mode, not just a threshold.
  `feasibility_notes` additionally caught and corrected a false data-availability claim by the
  conjecture generator before the run — good adversarial practice.
- **Justification: stale.** Refuted on disk 2026-05-15; still `proposed` 94 days later.
- **Scientific value:** this and HYP-014 together constitute a clean **negative result** — the
  integral-geometry (Crofton) route to the force is structurally dead across two distinct measures
  (uniform-chord and Kirillov–Kostant/PEE-thread). §16 says such a result "may advance the field more
  than another approximate match", and §38.A.12 asks which important negative results are not surfaced.
  **This one is not surfaced**: it is invisible in the hypothesis statuses and appears nowhere in
  `paper-prd.tex`.

### HYP-2026-023 — the 0.72% residual is a dS₂ composite-geodesic effect
- `REFUTED` (case-mismatched vs enum `refuted`) / `medium`, `feasibility_verdict: REFUTED`
  (**not in enum**), 2026-05-15 → 2026-05-16 (93 d).
- **Linked SIMs:** SIM-2026-006; `SIM-2026-025.json` `hypothesis_id: HYP-2026-023`,
  `results.verdict: REFUTED`.
- **Killer: YES — four-clause, pre-registered, and it fired on multiple clauses.** SIM-025
  `results.refutation_reasons` lists five, including *"The original 0.72% residual was
  grid-quantization artifact; true residual at fine dt is -1.20%, weakening not strengthening the dS2
  case"* and *"2-point 1/N fit is degenerate."*
- **Justification: YES.** Correctly refuted. This is the record that *generated* ERRATA E2 — the
  project's own follow-up retracting its own published number. §32 compliance is real here.
- Residual defect: the `claim` text still recites T = 2.250 / 0.72% without a superseded-value marker.

### HYP-2026-024 — finite-T BTZ transport curve
- `NOT_ESTABLISHED` (**not in enum**) / `medium`, 2026-05-15 → 2026-06-08 (70 d).
- **Linked SIMs:** SIM-2026-006, 026, 027, 028, 028-L10, 029, 030 — all seven carry
  `hypothesis_id: HYP-2026-024`. Best-linked record in the corpus.
- **Killer: YES — four clauses (a)–(d), including a self-consistency floor** ("the beta → infinity
  limit does NOT reproduce HYP-006's T = 2.250 within 2% … the result is INVALID rather than
  refuting"). The invalid-vs-refuted distinction is exactly what §12 asks for.
- **Justification: YES — and this is the corpus's best example of a self-correction.**
  `result_note_2026_05_28` recorded SUPPORTED_AMPLITUDE with a 95% cold→hot degradation, a null
  control (SIM-028) that appeared to exclude generic washout, and a 183% separation from control.
  `result_note_2026_06_08` then **reverses it**: *"Status corrected from SUPPORTED_AMPLITUDE … to
  NOT_ESTABLISHED, artifact-leaning. SIM-2026-030 gap-matched-control test FAILED the pre-registered
  robustness gate … the sqrt-purity normalization is unstable (two gap-matched controls disagree
  violently)."* Both the original and the reversal are preserved (§32).
- **Caveat:** the claim's premise (T = 2.250 as the zero-temperature limit) is a superseded number
  (ERRATA E2). If this branch is resumed, the whole β-ladder is anchored to a retracted value.

### HYP-2026-025 — α=4 universal at a third class (Z3 chiral clock → 3-state Potts, c=4/5)
- `SUPPORTED` (**not in enum**) / `medium`, 2026-05-15 → 2026-07-04 (44 d).
- **Linked SIMs:** `source_findings`/text cite SIM-2026-006, 011, 015c, 023, 057, 059; result notes
  add 062, 063. Reverse: SIM-057/059/062/063 carry `hypothesis_id: HYP-2026-025`; SIM-069
  `hypothesis_links[0]` = "HYP-2026-025 (Potts alpha=4 tower)".
- **Killer:** yes, well posed and with an explicit INVALID branch and an INCONCLUSIVE branch.
- **Justification: PARTIAL — two substitutions, one disclosed, one not.**
  1. *Model substitution (disclosed).* The claim and criteria name the **Z3 chiral clock**;
     `result_note_2026-06-27` states plainly the test used the **3-state Potts** self-dual point and
     argues both are c = 4/5 with Δ_T = 2. Honest and defensible.
  2. *Observable substitution (not disclosed).* The criteria demand a **force exponent α**;
     `SIM-2026-057.json` and `SIM-2026-063.json` contain `delta_T_statistics` and no force fit. α is
     computed as 2Δ_T. The pre-registered test was never run.
- **Counterfactual novelty: near-zero.** `confidence_rationale` says it itself: *"the stress tensor has
  Δ_T = 2 in EVERY unitary 2D CFT (a theorem, not a model fit), so the universality prediction α = 4
  for Z3 clock is parameter-free."* If a theorem fixes the answer, the only possible outcomes were
  "pipeline works" and "pipeline broken" (§6, near-zero counterfactual novelty). **Classification
  under §5: Level 1 (reproduction/validation), not Level 3.**
- **Genuinely informative sub-result (should be surfaced separately):** the χ-starvation trajectory
  Δ_σ = 0.089 (χ=6) → 0.14 (χ=9) → 0.133 (χ=12) vs CFT 2/15 = 0.1333 (`result_note_2026-07-04`) is a
  **convergence-behaviour** finding about the method, i.e. Level 2. That is the part worth writing up.

### HYP-2026-026 — Synge distance is geometric but force-blind
- `SUPPORTED` (**not in enum**) / `medium`, created 2026-06-11, `last_updated` **2026-06-08**
  (**update predates creation**), 70 d.
- **Linked SIMs:** SIM-2026-011, 011-interaction, 031. `SIM-2026-031.json` `hypothesis_id:
  HYP-2026-026`, `comparison: classical_wins`.
- **Killer: YES — a two-sided dichotomy gate (κ ≈ 0.25 vs κ ≈ 4) with an explicit "surprising outcome"
  branch and a defined INCONCLUSIVE band (R² < 0.9).** Plus three `feasibility_mandatory_gates`
  including an explicit instruction not to report "d(r) linear in r" against data that violates it.
- **Justification: PARTIAL.** `result_note_2026_06_08_sim031` reports κ = 0.2429 (dichotomy gate
  passed cleanly), monotone at both tiers, R² = 0.9545 — the registered gates are met. **But** the
  same note concedes: *"WORDING CORRECTION to the claim: the Synge distance for C=r^-1/4 is
  analytically d=eps*sqrt(0.5 ln r) — monotone but sqrt-logarithmic, not linear."* The `claim` field
  still reads "grows ~linearly with boundary lattice separation r". A `SUPPORTED` status sits on top of
  a claim its own evidence corrected and nobody edited.
- **Counterfactual novelty:** low-to-moderate. κ ≈ 2Δ_σ = 0.25 follows from Δ_σ = 1/8 once you accept
  that a σσ correlator carries Δ_σ; the "force-blindness" conclusion is close to a restatement of
  Δ_σ ≠ Δ_T. §7 classification of the comparison: **algebraically equivalent**, and the record does
  not say so.

### HYP-2026-027 — α≈4 universal at tricritical Ising (c=7/10)
- **`status`: `TESTABLE_NEAR_TERM`** — a `feasibility_verdict` value occupying the status slot, identical
  to the record's own `feasibility_verdict`. There is **no status verdict on this record at all**.
  Confidence `medium`, 2026-06-11 → 2026-06-16 (62 d).
- **Linked SIMs (named):** 015d, 023, 032, 032b, 033, 033b, 034, 035, 036, 037, 039, 040 — twelve
  records, all of which are *failures or infrastructure fixes*. **Not named:** SIM-042, 044, 045,
  045-chi6, 050, **051**, **052**, 058, 060, 061, 064, 065, 066, 067 (all carry
  `hypothesis_id: HYP-2026-027`) and SIM-068 (`hypothesis_links`). **The two records that actually
  answer the hypothesis — SIM-051 (`verdict`: "HYP-027 SUPPORTED … Δ_T = 2.007 … α = 4.01",
  `gate_pass: true`) and SIM-052 — are absent from the hypothesis record.**
- **Killer:** yes, well posed, with INVALID and INCONCLUSIVE branches.
- **Justification: NO (malformed), and the direction of the error is unusual — the record is
  *understated*, while `MEMORY.md` is *overstated*.** The newest note in the file
  (`result_note_2026_06_17_stage2e_chi4`) still ends: *"REMAINING for alpha-universality: the FORCE
  read-out … the clean alpha read-out is a SEPARATE build."* `MEMORY.md` meanwhile lists HYP-027 as
  SUPPORTED / **high**. Neither is reconcilable with the file as it stands.
- **Circularity finding (§6/§7):** SIM-051's pass-gate is "MERA confirmed at c = 7/10 with Δ_T = 2";
  its result is α ≡ 2Δ_T. **Gate and result are the same measurement.** Once the gate passes, α = 4 is
  arithmetically forced. The experiment can only detect an unconverged MERA, never a violation of the
  physical claim. Classification: **primarily a consistency check** (§7), **Level 1** (§5).
- **What *is* substantive in this record** (and deserves its own Level-2 write-up): the SIM-034/035
  finding that a clean Δ_T = 2 channel and spatial localization are **mutually exclusive at finite N**
  (`result_note_2026_06_16_FINAL`), and the ERRATA-D5 chain (SIM-036 collapse → SIM-039 autograd +
  Z2-projected objective → SIM-040 χ=4 faithful) which is a genuine optimizer-methodology result with
  a documented retraction of its own earlier diagnosis.
- **Orphaned line:** SIM-061/064/065/066/067 (OPE C_σσε and C_TTT) are tagged to HYP-027 but test
  neither the TCI force nor Δ_T. **The C_TTT ladder has no hypothesis record.**

### HYP-2026-028 — α=4 does NOT survive a non-Hermitian critical point (Yang–Lee)
- `SUPPORTED` (**not in enum**) / `medium`, 2026-06-25 → 2026-08-11 (**6 d — the freshest record**).
- **Linked SIMs:** named — SIM-2026-051, 053, 055; `phase2_result` adds SIM-070/071. Reverse:
  SIM-053/055/**056** carry `hypothesis_id: HYP-2026-028` (056 is a **mis-tag** — it is the OPE C_σσε
  gate); SIM-070/071 use `hypothesis_links`.
- **Killer:** yes — a four-branch pre-registration (PRIMARY refutation / SUPPORTED condition / INVALID
  condition / INCONCLUSIVE condition) plus four `feasibility_mandatory_gates` including the hard G4
  criticality gate (c_eff = 2/5 AND Δ_φ = −1/5) and an explicit instruction that failing it makes the
  result *"INVALID, not a refutation."* This is the strongest pre-registration in the corpus.
- **Justification: NO.** Trace the record's own history:
  - `result_note_2026-06-26` (SIM-053): unitary control validated (α = 3.951 at N=16); non-unitary
    α = 4.10/4.03/4.00 at N = 12/14/16, PT-unbroken, stable. The note records that the script's
    automated logic read this as REFUTED and that it was **overridden to INCONCLUSIVE** because
    G4 was not satisfied. Correct call.
  - `runA_note_2026-06-26` (SIM-055): G4 `FAIL per-N={'12': False, '14': False, '16': False}`,
    verdict `INVALID`. *"HYP-028 stays OPEN."*
  - `scan18_route_note` (2026-07-27): *"Status UNCHANGED: OPEN / INCONCLUSIVE, no new test run."*
  - `scan19_note` (2026-08-09): *"Status UNCHANGED (OPEN/INCONCLUSIVE)."*
  - `phase2_result` (2026-08-11, SIM-071): c_KS = −4.29 ± 0.15 ≈ −22/5; c_eff = +2/5 excluded.
  **Nothing in this chain satisfies the registered SUPPORTED condition** ("α lands clearly outside
  [3.2, 4.8] and within calculable error of 2·Δ_φ"). No α was ever measured at a validated Yang–Lee
  fixed point. The status flipped from OPEN to SUPPORTED on evidence for a **different proposition**.
- **What SIM-071 actually establishes** (and it is the project's most interesting result):
  the biorthogonal Koo–Saleur construction returns the **true** c = −22/5 with its sign rather than
  c_eff = +2/5, with a unitary control on the identical code path at 0.49986 vs 0.5
  (`SIM-2026-071.json` `unitary_control.extrapolated`). Counterfactual novelty here is **genuinely
  moderate-to-high** — nothing guaranteed the construction survives loss of reflection positivity, and
  the record documents a real surprise (`key_findings[2]`: *"The T-identification discipline INVERTS at
  YL: the cross-module product to the phi-descendant is ~10x LARGER than T's"*).
- **Two specific defects in the evidence:**
  1. `SIM-2026-071.json` `key_findings[1]` asserts *"First lattice extraction (to our knowledge) of a
     NEGATIVE central charge from stress-tensor matrix elements."* §8 forbids "to our knowledge" /
     "first" until the literature gate is recorded. **No literature-gate record exists** —
     `research/data/theory/` is empty and the HYP-028 record contains no prior-art comparison for the
     negative-c extraction (its scan notes catalogue *route* papers, not *prior-art* papers).
  2. The extrapolation is fragile and the record says so: c_KS by L runs −1.41 → −2.36 over L = 10…18,
     i.e. **the raw measurement is 46% of the quoted value at the largest size available**, and
     −4.29 comes from a *geometric-tail sum* over pairwise 1/L intercepts after
     *"free-exponent fits are degenerate (w→0 runaway) and discarded honestly."* The **sign** and the
     11× separation from c_eff are robust; the **magnitude** rests on an extrapolation model choice
     (§20: "Would the conclusion survive a reasonable alternative analysis pipeline?" — for the sign,
     yes; for −22/5 specifically, not demonstrated).
- **Correct status under the record's own rules:** the α-question is **OPEN/INVALID** (G4 never
  passed). A *new* hypothesis record should be opened for the biorthogonal-KS proposition, with its
  own pre-registration, rather than re-purposing HYP-028's status field.

### HYP-2026-029 — static α=4 force fits a ~megaquop FT STAR budget
- `SUPPORTED (conditional, confidence LOW)` (**free-prose status, not in enum**) / `low`,
  2026-06-25 → 2026-06-26 (52 d).
- **Linked SIMs:** SIM-2026-015d, 019, 054. `SIM-2026-054.json` `hypothesis_id: HYP-2026-029`,
  `verdict: "SUPPORTED (conditional; confidence LOW)"` — HYP and SIM agree verbatim.
- **Killer:** yes — three numeric ceilings (a) >10× logical volume, (b) >25k physical qubits,
  (c) super-polynomial prep depth; plus a SUPPORTED band (<2× volume, <5k qubits) and an INCONCLUSIVE
  clause tied to the uncatalogued companion gate model. Four mandatory gates including an explicit
  *"Do NOT propose, schedule, or authorize any actual FT hardware run from this hypothesis."*
- **Justification: PARTIAL, but honestly hedged.** `SIM-2026-054.json` `ceilings_check` shows
  ceiling 2 is passed only on one of the two costed variants: *"high-rate ~4.5k (SUPPORTED, <5k);
  transversal ~9-11k (over 5k SUPPORTED line, well under 25k REFUTE)."* The registered INCONCLUSIVE
  clause said the gate-model gap is resolved "by costing both transversal and non-transversal STAR" —
  both were costed and they land on opposite sides of the SUPPORTED line, so INCONCLUSIVE arguably
  fired. `verdict_detail` names this itself: *"the transversal-vs-high-rate gate-model gap is the
  pre-registered INCONCLUSIVE driver."*
- **Second-order dependency:** the logical-volume ratio rests on an **inferred** 8×8 reference volume
  (~87,600) because the source paper publishes no T-count — stated plainly in both records. It also
  depends on `SIM-2026-019`'s SNR model, and SIM-019's own verdict is `PARTIALLY_REFUTED`. That
  dependency-on-a-partially-refuted-input is **not** noted in either record.
- **Contribution level (§5):** Level 1/feasibility engineering. Counterfactual novelty: low — a
  resource estimate whose inputs are two published budgets and one internal SNR model.

### HYP-2026-030 — α = 2Δ_T = 4 along the whole c=1 compact-boson moduli line
- `proposed` / `medium`, 2026-07-14 (34 d). **No SIMs.** `source_findings` has **one** item
  (schema requires ≥2), and that item embeds an arXiv id inside the ID string
  (`"PAPER-2026-135 (arXiv:2607.03534)"`), breaking the ID convention used everywhere else.
- **Killer: present but cannot fire.** *"A clean, chi-converged … Δ_T that deviates from 2.0 by more
  than 2% at any XXZ coupling in the critical window would contradict the kinematic-universality
  mechanism."* The record's own `confidence_rationale` concedes the point: *"The CFT prediction is as
  kinematic as for the minimal models, so the physics risk is low."* A test whose only failure mode is
  a broken implementation is a §30 validation run, not a §12 killer.
- **Justification:** n/a — untested.
- **§30 assessment (protect time from low-value validation):** the five §30 questions answer badly
  here. *What exact failure could this detect?* Only pipeline failure. *Is that failure still
  plausible?* The same symmetric-tensor pattern already passed at Z2 (SIM-061) and Z3 (SIM-062/063).
  *Has this pipeline already been validated at the same structural level?* Yes, twice.
  **Recommendation: do not run as stated.** If a c=1 program is wanted, the informative version is the
  *marginal-deformation* stage — whether the extraction stays stable as the compactification radius
  moves continuously — which is a method question (Level 2), not another Δ_T = 2 confirmation.

---

## 4. Cross-cutting observations (not per-record)

1. **No hypothesis record exists for the C_TTT ladder** (SIM-067 Ising 3.9936/4.000,
   SIM-068 TCI 3.381/3.3806, SIM-069 Potts 3.163/3.16228) or for the C_σσε extraction
   (SIM-061/064). These are the results most prominently reported in `MEMORY.md` and the informal
   review. Consequences: no pre-registered prediction, no killer, no falsification criterion, no
   independence statement — and the SIMs are back-tagged to HYP-027, whose claim they do not test.
   C_TTT = 2√2/√c is a Virasoro identity, so the counterfactual novelty of the numbers is near-zero;
   the *method* content (L₂ε contamination suppression, puMPS Bloch-state convergence) is Level 2 and
   has no hypothesis record to anchor it.

2. **Independence (§7) is never stated in any hypothesis record.** Not one of the 30 files contains an
   independence, shared-input, or "consistency check vs independent confirmation" field. The three
   headline agreements (α = 2Δ_T; T = (π/2)·l_AdS; C_TTT = 2√2/√c) are each **algebraically
   equivalent or structurally dependent** comparisons, and the records present them without that
   qualification.

3. **Matched controls (§19) are near-absent from the hypothesis layer.** The only genuine
   non-holographic matched controls I could find are (i) the TFIM ring-propagation comparison buried in
   HYP-010's `test_results` and (ii) the gap-matched thermal controls in the HYP-024 chain
   (SIM-028/029/030) — which are also the one case where a control **defeated** the project's
   preferred interpretation. That is the pattern §19 wants ("A serious control should be capable of
   defeating the preferred interpretation") and it appears exactly once in 30 records.

4. **Status vocabulary should be formalized, not policed back to the schema.** The de-facto vocabulary
   (SUPPORTED / PARTIALLY_CONFIRMED / NOT_ESTABLISHED / REFUTED / SHELVED / INCONCLUSIVE) is *more
   scientifically expressive* than the template enum. The defect is that it is undocumented and
   inconsistently cased, and that `feasibility_verdict` values have leaked into the `status` slot
   (HYP-027) while prose has leaked in elsewhere (HYP-018, HYP-029). Recommendation: extend
   `templates/hypothesis-record.json` to the real vocabulary and add a separate
   `justified_by: [SIM-ID…]` array so status↔evidence is machine-checkable.

5. **`hooks/hooks.json` is inert** (per `CLAUDE.md`: the plugin is not installed, so the
   `research/data` ID-format check never loads). This is the mechanical reason the schema drift in §2(d)
   accumulated undetected. Any repair should be paired with a CI-style validator that actually runs.

---

## 5. UNVERIFIED

Items I could not confirm, stated explicitly per the output protocol:

1. **Whether the SIM verdicts themselves are correct.** I read `verdict` / `status` / `comparison`
   fields as recorded facts and did not re-derive any numerical result, re-run any script, or check any
   fit. A wrong-but-recorded verdict would propagate through this audit unchallenged.
2. **`hyp010_criticality_scan.json`** exists in `research/data/simulations/` (verified by directory
   listing, alongside `hyp010_criticality_scan.py`), but it carries **no `SIM-2026-NNN` ID** and so is
   invisible to any SIM-ID-based traceability. I did not open its contents; the numbers in HYP-010's
   `test_results` block are therefore unverified against the file.
3. **HYP-006's evidence files** (`holographic_transport.json`, `composite_geodesic_results.json`) were
   not opened; I relied on ERRATA E1/E2, which quote
   `composite_geodesic_results.json: l_AdS_needed_to_match_exact = 1.4323944878`.
4. **Full JSON-Schema validation** was not run. My conformance check covered the enum fields, the seven
   required fields, `source_findings` minItems, and created/updated ordering. Date-format
   (`format: date`) and the `id` regex were not machine-validated, so the true clean count may be lower
   than 13/30.
5. **`MEMORY.md` status table** (`~/.claude/projects/D--quantum-worldline/memory/MEMORY.md`) is outside
   the repository and was read only as it appears in this session's context. I treat every divergence
   between it and the on-disk records as a defect in the *records*, but I did not independently open
   that file to confirm its current contents.
6. **Manuscript alignment beyond transport.** I grepped `research/submission-package/prd/paper-prd.tex`
   only for the transport numbers (0.72 / 1.21 / 2.250 / 0.76). Whether the paper's α=4, m_eff, C_σσε,
   or Z₂-method claims are stated at a strength their hypothesis records support is **not audited
   here** — that belongs to a manuscript-scoped investigator.
7. **Prior art for the SIM-071 negative-c extraction.** I flag the unsupported "first / to our
   knowledge" phrasing as a §8 violation of *process* (no recorded gate). I did **not** search the
   literature and take no position on whether the claim is in fact true.
8. **Whether the 2026-06-08 audit (ERRATA source) formally assigned owners** to the stale-status
   write-backs. HYP-016 and HYP-021 were both touched on/around 2026-06-08–11 with notes added and
   statuses left unchanged, which suggests write-back was out of scope for that pass, but I found no
   record stating so.
