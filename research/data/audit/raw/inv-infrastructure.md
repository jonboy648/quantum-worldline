# inv:infrastructure — Research Infrastructure Audit

**Auditor:** inv:infrastructure subagent
**Date:** 2026-08-17
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` (§5, §6, §7, §8, §12, §14, §15, §21, §27, §38)
**Repo state:** branch `public-release`, HEAD `9470d69`

---

## 0. Headline corrections to the task brief

Three premises handed to me were wrong on disk. Recording them first because downstream audit
agents may be working from the same brief.

| Brief premise | Ground truth | Evidence |
|---|---|---|
| "`research/data/theory/` is EMPTY (known defect)" | **NOT empty.** 8 markdown files, 2,488 lines total. The real defect is different: **zero structured records, and no `theory-record.json` template exists in `templates/`.** | `ls research/data/theory/` → `RUN-A-methods.md`, `epsilon-channel-proof.md` (684 ln), `paper-review-synthesis.md`, `research-challenge.md` (249 ln), `research-practical.md`, `research-primary.md` (392 ln), `task4-ope-argument.md` (345 ln), `task5-crofton-derivation.md` (450 ln); `ls templates/` → only 4 templates, none for theory |
| "Simulations (85)" | **85 `.json` files, but only 73 are SIM-ID'd records, spanning 62 distinct numeric IDs.** 12 are raw output blobs with no `id` field. 9 ID numbers are unassigned gaps. | `research/data/simulations/`: 12 non-`SIM-2026-*` json (`worldline_mc_results.json`, `holographic_transport.json`, `runpod_gpus.json`, …); ID gaps `{4,7,38,41,43,46,47,48,49}` |
| "Papers (139)" / "Hardware (76)" | 139 and 76 `.json` files, but **138 PAPER records + 1 stray `scan-2026-03-26.json`**, and **74 HW records + 2 stray pytket result blobs**. | `ls papers/*.json \| grep -v PAPER-2026` → `scan-2026-03-26.json`; `ls hardware/*.json \| grep -v HW-2026` → `pytket_compilation_results.json`, `pytket_compile_chi3_8q_results.json` |

`RESEARCH-DIRECTOR.md` §3 itself is also mildly off: it claims "approximately 30 weekly literature
scans." `research/digests/` holds 30 files, but only **19 numbered scans** exist (memory scan history
runs #4 → #19); the other digest files are one-off reports (`2026-04-26-rydberg-playground.html`,
`2026-05-01-quantum-village-eli5.md`, build plans). The "30" is a file count, not a scan count.

---

## 1. Agents — inventory, tier, model, adversarial function

### 1.1 Deployment integrity (verified, passes)

`CLAUDE.md` warns that `agents/*.md` is canonical but **not** what the runtime loads. I diffed all 14
canonical files against `~/.claude/agents/`:

```
SAME  classical-simulator.md   SAME  computation-lead.md      SAME  conjecture-generator.md
SAME  feasibility-checker.md   SAME  hardware-tracker.md      SAME  literature-lead.md
SAME  math-bridge.md           SAME  philosophy-agent.md      SAME  physics-scanner.md
SAME  qiskit-builder.md        SAME  synthesis-agent.md       SAME  theory-lead.md
SAME  visualization-agent.md   SAME  worldline-orchestrator.md
```

**All 14 byte-identical as of 2026-08-17.** This re-verifies the `CLAUDE.md` claim ("verified
2026-07-06") at a later date. No sync drift. Skills are symlinks into
`~/.claude/skills/` (`ls -la` confirms 6 live symlinks → `/d/quantum-worldline/skills/*`), so skill
edits take effect immediately as documented.

Stale note resolved: `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md` line 11 (2026-05-12)
records "`philosophy-agent` referenced by skill+CLAUDE.md is NOT installed". It **is** installed now
(`~/.claude/agents/philosophy-agent.md`, 2,820 bytes, byte-identical to canonical). That note is
obsolete and should be struck.

### 1.2 The 14 agents

Model assignment read from YAML frontmatter `model:` field of each `agents/*.md`.

| # | Agent | Tier | Lead | Model | Function class |
|---|---|---|---|---|---|
| 1 | `worldline-orchestrator` | 0 (top) | — (user entry) | **opus** | Generative / dispatch |
| 2 | `literature-lead` | 1 lead | orchestrator | sonnet | Generative / aggregation |
| 3 | `physics-scanner` | 1 spec | literature-lead | sonnet | Generative (catalogue) |
| 4 | `hardware-tracker` | 1 spec | literature-lead | sonnet | Generative (catalogue) |
| 5 | `math-bridge` | 1 spec | literature-lead | **opus** | Generative (connection-seeking) |
| 6 | `synthesis-agent` | 1 spec | literature-lead | sonnet | Generative (editorial) |
| 7 | `computation-lead` | 2 lead | orchestrator | sonnet | Generative / dispatch |
| 8 | `qiskit-builder` | 2 spec | computation-lead | **opus** | Generative (build) |
| 9 | `classical-simulator` | 2 spec | computation-lead | sonnet | **PARTIALLY ADVERSARIAL** |
| 10 | `visualization-agent` | 2 spec | computation-lead | sonnet | Generative (render) |
| 11 | `theory-lead` | 3 lead | orchestrator | sonnet | Generative / dispatch |
| 12 | `conjecture-generator` | 3 spec | theory-lead | **opus** | Generative (+ self-imposed Popperian discipline) |
| 13 | `feasibility-checker` | 3 spec | theory-lead | **opus** | **PARTIALLY ADVERSARIAL** (gate) |
| 14 | `philosophy-agent` | 3 spec | theory-lead | **opus** | Generative (interpretive) |

**Model-policy contradiction (defect).** Memory topic
[`feedback_model_assignment.md`] is indexed in `MEMORY.md` as "Opus for ALL physics agents, no Sonnet
on science." On disk **8 of 14 agents run `model: sonnet`**, including three that do science:
`physics-scanner` (paper triage + relevance scoring), `hardware-tracker` (frontier numbers), and
`classical-simulator` (the honest-broker numerical baseline). The stated policy and the deployed
frontmatter disagree; one of the two is wrong and neither has been reconciled.

### 1.3 Adversarial vs purely generative — verdict

I counted adversarial-vocabulary density per agent
(`refut|falsif|adversar|skeptic|challenge|criticis|reject|control|artifact|prior art|overclaim|reality gate|counter`):

```
5  conjecture-generator.md      0  visualization-agent.md   0  theory-lead.md
2  feasibility-checker.md       0  synthesis-agent.md       0  qiskit-builder.md
2  classical-simulator.md       0  physics-scanner.md       0  philosophy-agent.md
1  worldline-orchestrator.md    0  math-bridge.md           0  literature-lead.md
                                0  hardware-tracker.md      0  computation-lead.md
```

**Ten of fourteen agents contain zero adversarial instruction.** The four that contain any:

- **`feasibility-checker`** — the strongest adversarial role in the team. Self-describes as "the
  reality gate. Nothing reaches the user without your assessment," and has a KILL SWITCH clause
  archiving hypotheses on `INFEASIBLE`. **But its adversarial axis is resources, not truth.** Its four
  evaluation dimensions are hardware, circuit, mathematical no-go, and budget feasibility. It asks
  "can this be run?", never "is this result fixed in advance?" (§8 derivation gate) or "has someone
  already published this?" (§8 literature gate). It also explicitly self-limits: "Be rigorous but not
  dismissive." Evidence: `agents/feasibility-checker.md` lines 12-16 (EVALUATION DIMENSIONS), 25-28
  (KILL SWITCH), 38 (RULES).
- **`classical-simulator`** — has an "INTELLECTUAL HONESTY" block ("The purpose is truth, not advocacy
  for quantum computing"; "Use the best known classical algorithm, not a strawman"). This is a real
  §19 matched-control instinct, but scoped to a question the project no longer asks: quantum-vs-classical
  advantage. Its verdict enum is `advantage / parity / classical_wins / inconclusive`. It is **not** an
  independent reproducer of the project's own MERA/Koo-Saleur analyses. Evidence:
  `agents/classical-simulator.md` COMPARISON VERDICTS + INTELLECTUAL HONESTY blocks.
- **`conjecture-generator`** — highest keyword count, but the hits are *self-discipline on output
  quality*, not adversarial review of others' work: mandatory `refutation_criteria` ("Popperian
  discipline"), a LANGUAGE block ("'suggests' not 'proves'"), and `NO_VIABLE_CONJECTURE` as an honest
  null return. This is calibration, not adversarial function. It is the team's primary *generator*.
- **`worldline-orchestrator`** — one hit: "If a finding contradicts the knowledge base, flag it
  prominently." A contradiction-flagging clause, not an adversarial role.

**Net:** the team has **one partial gate (resources), one partial control (obsolete axis), and zero
agents whose job is to attack a project result.** Every documented adversarial artifact in the repo
was produced *outside* the agent roster — `research/data/theory/research-challenge.md` is titled
"Devil's Advocate Challenge: Paper v3" and came from the **global** `devils-advocate` skill, not from
any `agents/*.md`. The project's most valuable self-criticism is therefore ad hoc and unowned.

This is exactly the failure §27 names: *"Do not let fourteen agents become fourteen agreeable
assistants."*

### 1.4 GAP TABLE — §27 roles vs deployed agents

§27 lists 14 roles. The team has 14 agents. **The overlap is 4 partial and 10 empty.**

| # | §27 role | §27 mandate | Nearest agent | Status | Why it fails |
|---|---|---|---|---|---|
| 1 | **Research director** | Maintains scientific portfolio and priorities | `worldline-orchestrator` | **PARTIAL** | Dispatches tier leads and aggregates output. No portfolio, no priority ranking, no §28 decision score. Its OUTPUT FORMAT ends at "Recommended next steps" — no notion of a research program. |
| 2 | **Literature adversary** | Searches prior art *to eliminate novelty claims* | `physics-scanner` | **GAP** | Scanner catalogues papers and scores `relevance` 1-5. Its SEARCH DOMAINS list is topic discovery. Zero instruction to attack a project claim's novelty. §8 literature gate has no owner. |
| 3 | **Analytic theorist** | Determines which numerical results are *fixed by known identities* | `math-bridge` | **GAP** | Math-bridge's FOCUS AREAS are 7 cross-domain *bridges* (Radon↔tomography, path integrals↔worldline, …) — it is described as "the agent most likely to find unpublished connections," i.e. purely generative. The §8 derivation gate — the single most important check for this project, given that Δ_T=2, C_TTT=2√2/√c and C_σσε=0.5 are all fixed in advance — has **no owner**. |
| 4 | **Numerical architect** | Simulation correctness and scalability | `computation-lead` + `qiskit-builder` | **PARTIAL** | Covers circuit design/transpile/resource estimate. But the project's actual numerics are Julia/MERAKit + puMPS + biorthogonal ED; `qiskit-builder` is Qiskit-only and has no mandate over those pipelines. |
| 5 | **Independent reproducer** | Reimplements key calcs *without copying the primary analysis path* | `classical-simulator` | **GAP** | Nearest, but its job is a classical baseline for a quantum circuit, not an independent code path for a project result. No agent has ever re-derived c_KS, C_TTT, or α by a second implementation. §40 explicitly names "reproduce the Yang-Lee result through an independent code path" as a candidate first slice — unowned. |
| 6 | **Skeptical referee** | Writes rejection-quality criticism | — | **GAP** | No agent. The only rejection-quality document in the repo (`theory/research-challenge.md`) came from a global skill. §24 ("Prepare for the PRD referee") has no owner while a paper sits at PRD (`DV13971`). |
| 7 | **Alternative-explanation analyst** | Finds conventional explanations for surprising results | — | **GAP** | No agent. Notable given the project's history: ERRATA E2 (grid artifact), D5 (optimizer collapse misread as bond-dimension ceiling), and the retracted Crofton amplitude "coincidence" (HYP-014) were *all* conventional explanations for apparently-real effects, each found late. |
| 8 | **Statistics and uncertainty lead** | Audits fits, error models, model selection | — | **GAP** | No agent. §20 asks for 10 separated error classes; SIM records report a single ± with no decomposition (see §3.4 below). |
| 9 | **Non-Hermitian specialist** | Biorthogonality, conditioning, exceptional points, c vs c_eff | — | **GAP** | No agent, despite this being the standard's own nominated strongest contribution (§13, Track A, Candidate Paper A). The entire HYP-028 program ran with no dedicated role; its design doc `research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md` is prose outside the record system. |
| 10 | **Geometry skeptic** | Assumes MERA is only an efficient ansatz; designs tests accordingly | — | **GAP** | No agent. This is the §4 Hypothesis-A advocate. Its absence is the structural reason the project has 30 hypotheses and zero matched non-geometric controls. |
| 11 | **Geometry advocate** | Strongest operational predictions of emergent geometry | `conjecture-generator` + `philosophy-agent` | **PARTIAL** | Covered de facto — and *only* this side of the §4 dichotomy is staffed. `philosophy-agent`'s framework list (eternalism, presentism, IIT, holographic principle, many-worlds) is interpretive amplification with no falsification duty; its scope note says it "never GENERATEs hypotheses," so it cannot even propose a discriminating test. |
| 12 | **Reproducibility auditor** | Ensures every result can be reconstructed | — | **GAP** | No agent. Measured consequence: 3/73 SIM records carry a code revision, 1/73 an environment spec, 0/73 a checksum (§3.4). |
| 13 | **Scientific editor** | Aligns claims with evidence | `synthesis-agent` | **PARTIAL** | Self-describes as "the editor, not the reporter," but its SYNTHESIS TASKS are ranking, pattern-spotting, gap-spotting, frontier updates, and cross-tier routing — all about *findings flow*, none about claim/evidence calibration. It cannot catch an overclaim. |
| 14 | **Program historian** | Maintains logs, errata, dependencies, decision records | — | **GAP** | No agent. `RESEARCH-LOG.md` and `ERRATA.md` are maintained by hand. Measured consequence: the log has a 3-week hole over the project's most important results (§4.3). |

**Score: 0 roles fully covered, 4 partial, 10 absent.**

**Structural reading:** every partial coverage sits on the *generative* side of §27's design. All six
roles whose explicit purpose is to destroy a claim — literature adversary, independent reproducer,
skeptical referee, alternative-explanation analyst, geometry skeptic, statistics lead — are absent
without exception. The team is architected as a discovery pipeline (`discover → hypothesize → gate →
test → interpret`, per `CLAUDE.md`), and the only gate in that pipeline asks whether an experiment is
*affordable*, never whether its answer was fixed before it ran.

---

## 2. Skills

Six skills, all symlinked live into `~/.claude/skills/`. Note the **name mismatch**: directory names
(`weekly-scan/`) differ from the frontmatter `name:` field (`qw-scan`). The runtime uses the
frontmatter name; `CLAUDE.md`'s skill table lists the directory names (`/weekly-scan`). Cosmetic, but
it means the documented invocation strings are not the registered ones.

| Dir | `name:` | Lines | Dispatch mode | Reads for ID counters | Adversarial content |
|---|---|---|---|---|---|
| `hardware-status/` | `qw-hardware` | 11 | direct subagent (`hardware-tracker`) | — | none |
| `hypothesis-review/` | `qw-hypotheses` | 13 | none (file read + table) | — | none |
| `research-query/` | `qw-query` | 60 | subagent or team | `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md` | none |
| `simulate/` | `qw-simulate` | 42 | team `qw-simulate` | same | none |
| `weekly-scan/` | `qw-scan` | 58 | team | same | none |
| `worldline-orchestrator/` | `qw-orchestrate` | 72 | mode chooser | — | none |

**No skill contains an adversarial or verification step.** `weekly-scan` is the closest to a
quality-controlled workflow — it carries a "Standing Rules (2026-06-08)" block encoding the
MCP-query-blind lesson and the sequential-query rate-limit fix — but those are *operational* rules
against producing false-empty scans, not scientific challenge. There is no `/novelty-gate`,
`/independence-ledger`, `/claim-map`, or `/killer-test` skill; §6, §7, §8 and §12 of the standard have
no tooling at all.

### 2.1 DEFECT (live, high severity): three skills read a stale ID-counter file

`research-query`, `simulate`, and `weekly-scan` each instruct the agent to
"Read `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md` for ID counters."

That file was **last modified 2026-07-14** and its newest entry is Scan #15. Its stated high-water is:

> `High-water: **PAPER-136, HW-074, HYP-030, SIM-064** → next PAPER-137, HW-075, HYP-031, SIM-065`
> — `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md` line 4

Actual disk high-water (recomputed 2026-08-17): **PAPER-138, HW-074, HYP-030, SIM-071.**

The SIM counter is **7 IDs stale**; PAPER is 2 stale. Any skill-driven session that trusts this file
will mint `SIM-2026-065` over an existing record. `ERRATA.md` D1 already documents "SIM ID collisions"
as a realized defect, and `CLAUDE.md` states the rule "Verify ID high-water marks on disk before any
scan; memory counters drift." **The three skills do not implement that rule — they implement its
opposite.** The accurate source (`~/.claude/projects/D--quantum-worldline/memory/MEMORY.md`) is not
the file the skills point at.

### 2.2 Referenced-file integrity

`hardware-status`, `feasibility-checker`, and `worldline-orchestrator` all read
`research/knowledge-base.md`. Verified present (24,792 bytes, mtime 2026-08-06, contains the
`## Current Hardware Frontier` heading at line 29). No broken reference.

### 2.3 Inert hook (confirmed, matches `CLAUDE.md`)

`hooks/hooks.json` defines a `PostToolUse`/`Write` prompt hook that checks `research/data/` writes for
a well-formed `id` field. `.claude-plugin/plugin.json` contains only `{name, description, version}` —
**no `hooks` key** — and the plugin is not installed. The hook has therefore never fired. This is
directly causal for §3: the one automated guard against exactly the ID/schema defects measured below
has been dead for the whole project.

---

## 3. Schema drift — recomputation of ERRATA D3

### 3.1 What D3 claimed

> `research/ERRATA.md:75-77` — "**D3** — Schema drift: only 9/36 SIM files and 16/25 HYP files satisfy
> `templates/*.json`; 7 sim ids violate the id regex; 13 use non-enum `type`; 14 lack `date`.
> Vocabulary has diverged (e.g. status values like SUPPORTED_AMPLITUDE, CONFIRMED_ANALYTIC not in
> template enum)."

### 3.2 Method

Wrote a JSON-Schema-subset validator implementing the constructs the four templates actually use
(`type`, `required`, `enum`, `pattern`, `format: date`, `minimum`/`maximum`, `minItems`, nested
`properties`, array `items`). Strict and case-sensitive, as the templates are written. Validated every
`.json` under each of the four record directories against its template.
Validator: `<scratchpad>/validate.py`; raw output: `<scratchpad>/validate_out.txt`.

### 3.3 Current conformance (2026-08-17)

| Class | Template | Conformant | Rate | D3 baseline | Direction |
|---|---|---|---|---|---|
| **SIM** (all 85 json) | `simulation-result.json` | **20 / 85** | **23.5%** | 9/36 = 25.0% | worse |
| **SIM** (73 SIM-ID'd only) | same | **20 / 73** | **27.4%** | — | — |
| **HYP** | `hypothesis-record.json` | **13 / 30** | **43.3%** | 16/25 = 64.0% | **substantially worse** |
| **HYP** (lenient: case-insensitive enums) | same | **18 / 30** | 60.0% | — | still below baseline |
| **PAPER** | `paper-record.json` | **101 / 139** | **72.7%** | not measured in D3 | — |
| **HW** | `hardware-milestone.json` | **48 / 76** | **63.2%** | not measured in D3 | — |

**D3 is stale and understates the problem.** Absolute non-conformant counts have grown from 27 SIM +
9 HYP to **65 SIM + 17 HYP**, and D3 covered only two of the four record classes. Papers and hardware
were never audited; 38 paper records and 28 hardware records are also non-conformant.

The 20 conformant SIM records are `SIM-2026-001, 024–037, 039, 040, 042, 045` — one early record plus
a single contiguous band from the April–June 2026 era. Everything before 024 and everything after 045
fails. Conformance was briefly enforced, then abandoned.

### 3.4 Failure-mode breakdown

**SIM (65 failures):**

| Count | Failure |
|---|---|
| 36 | missing required `description` |
| 36 | missing required `type` |
| 24 | missing required `date` |
| 20 | `type` present but outside enum `[quantum, classical, comparison]` (e.g. `vqe_optimization`) |
| 15 | missing required `id` entirely |
| 8 | `id` violates regex `^SIM-\d{4}-\d{3,}$` (suffixed variants `008a`, `008b-8q-test`, `008c`, `015b/c/d`, `032b`, `033b`) |
| 5 | `comparison` is an object where the schema declares a string enum |
| 4 | `circuit.depth` / `circuit.gates` / `notes` wrong scalar type |

D3 said "7 sim ids violate the id regex" — now **8**. It said "13 use non-enum `type`" — now **20**.
It said "14 lack `date`" — now **24**. Every counter D3 tracked has grown.

**HYP (17 failures):** 14 are `status` outside the enum, 3 are `feasibility_verdict` outside the enum,
plus `HYP-2026-021` missing three required fields (`confidence`, `source_findings`, `testable`) and
`HYP-2026-030` carrying one `source_findings` entry where the schema mandates `minItems: 2`.

The vocabulary has forked into a parallel, undeclared enum:

```
PARTIALLY_CONFIRMED   analyzed   inconclusive   SHELVED   NOT_ESTABLISHED
proposed_marginal_shielded_room_dependent      TESTABLE_NEAR_TERM
SUPPORTED (conditional, confidence LOW)
```

Two of these are worse than vocabulary drift:

- **`HYP-2026-027.status = "TESTABLE_NEAR_TERM"`** — a *feasibility verdict* stored in the *status*
  field, duplicating the record's own `feasibility_verdict`. HYP-027 therefore has **no recorded
  outcome at all** on disk, despite carrying twelve `result_note_*` fields.
- **`HYP-2026-029.status = "SUPPORTED (conditional, confidence LOW)"`** — confidence smuggled into the
  status string, duplicating the dedicated `confidence: low` field.

**PAPER (38 failures):** 36 missing `abstract`, 36 missing `tags`, 27 missing `date`, 27 missing
`source`, 10 with a non-ISO `date`, 9 missing `authors`, 9 missing `relevance`, 9 with a non-enum
`source`, 1 (`scan-2026-03-26.json`) missing `id` and `title` because it is not a paper record.

**HW (28 failures):** 28 missing `processor`, 23 missing `organization`, 16 missing `date`, 12 missing
`source_url`, 10 missing `id` (incl. the 2 stray pytket blobs), 5 malformed dates.

### 3.5 The newest records are the least conformant

The five records carrying the project's headline results all fail:

| Record | Result | Schema |
|---|---|---|
| `SIM-2026-067.json` | C_TTT Ising 3.9936 / 4.000 | FAIL |
| `SIM-2026-068.json` | C_TTT TCI 3.381 / 3.3806 | FAIL |
| `SIM-2026-069.json` | C_TTT Potts 3.163 / 3.16228 | FAIL |
| `SIM-2026-070.json` | HYP-028 Phase 1 gate, 0.01% | FAIL |
| `SIM-2026-071.json` | c_KS = −4.29 (the frontier result) | FAIL |

They use an undeclared field vocabulary — `{id, date, title, hypothesis_links, method, ladder,
D_systematics, fit, key_findings, operational_notes, verdict, files, caveats, unitary_control}` — with
no `description`, no `type`, no `hypothesis_id`, no `comparison`. Field-frequency across the 73
SIM-ID records confirms this is systemic: `id` 70, `date` 56, `type` 49, `hypothesis_id` 45,
`description` 43 — but also `verdict` 35 and `status` 30 (neither in the template), plus a long tail
of ~60 one-off keys.

**Traceability consequence:** SIM-070 and SIM-071 answer HYP-028, but neither carries the
`hypothesis_id` field the template defines. They use `hypothesis_links: ["HYP-2026-028"]` instead.
Any tool, skill, or query joining simulations to hypotheses on `hypothesis_id` — which is what the
templates and the `hypothesis-review` skill presume — **will not find the evidence for the project's
strongest claim.** Same for SIM-068 (`hypothesis_links: ["HYP-2026-027 (…)", "SIM-2026-067 (…)"]`),
where the link values are free-text with parenthetical commentary rather than bare IDs, so even a
`hypothesis_links` join needs string surgery.

### 3.6 Strict-JSON validity

Two files contain the bare literal `NaN`, invalid per RFC 8259 and rejected by strict parsers
(Python's `json` accepts it only by default leniency):

- `research/data/simulations/worldline_mc_results.json` — already logged as ERRATA D2
- `research/data/simulations/SIM-2026-031.json` — **not** logged in ERRATA

SIM-2026-031 is the HYP-026 record (Synge distance is force-blind), a hypothesis carried as
**SUPPORTED / high** in the memory index. D2 should be widened to name it.

### 3.7 Reproducibility metadata (§21) — measured

§21 requires code revision, environment spec, dependency versions, platform, seeds, parameters, solver
settings, convergence criteria, input records, output checksums, runtime metadata, analysis script
revision. Coverage across the 73 SIM-ID records (recursive key-name match, generous — a key merely
*containing* the term counts):

| §21 item | Coverage |
|---|---|
| script / driver path | 58 / 73 (79%) |
| runtime metadata | 43 / 73 (59%) |
| platform / host | 18 / 73 (25%) |
| random seeds | 16 / 73 (22%) |
| **code revision (git sha)** | **3 / 73 (4%)** |
| **solver settings / tolerances** | **3 / 73 (4%)** |
| **environment / dependency versions** | **1 / 73 (1%)** |
| **output checksums** | **0 / 73 (0%)** |

§21 further requires that "a submitted manuscript should be linked to a frozen research snapshot." The
PRD submission (`DV13971`, 2026-08-07) is linked to no frozen commit or tag in any record; the branch
has continued to advance (SIM-068 → 071 all postdate the submission). **No evidentiary freeze exists.**

### 3.8 Missing templates

`templates/` holds 4 schemas. Two record directories have none:

- **`research/data/theory/`** — no `theory-record.json`. §15 specifies exactly what one should contain
  (definitions, axioms, prior results, derived equations, unresolved steps, numerical quantities
  required, conclusions, counterexamples, affected claims, dependency chains). Nothing implements it.
- **`research/data/builds/`** — no `build-record.json`. 17 JSON files there, **0 with an `id` field**.
  Filenames are free-form (`adapt_noise_calib_results.json`, `verify_adapt_scaling.json`). There is no
  BUILD ID space at all, so `CLAUDE.md`'s dedup and high-water rules cannot apply to builds.

There is also no schema for the §6 claim-evidence map, the §7 independence ledger, or the §36
prediction registry — none of which exist in any form on disk.

---

## 4. The theory tier (§14 / §15)

### 4.1 The directory is not empty — the defect is sharper than reported

`research/data/theory/` contains 8 markdown files, 2,488 lines:

| File | Lines | mtime | Content class | §15 gaps |
|---|---|---|---|---|
| `epsilon-channel-proof.md` | 684 | 2026-04-03 | **Analytic derivation.** Proves the ε-channel cancels in ⟨εεεε⟩ via three independent arguments; computes C_εεT; compares to measurement; §9 "Formal Statement for Publication" | No assumption list, no dependency chain, no simulation back-link, no counterexamples section |
| `task5-crofton-derivation.md` | 450 | 2026-04-01 | **Analytic derivation** (Crofton kinematic-space → force). Has a `## Caveats` section | Derivation for a route later **REFUTED** (HYP-014, HYP-022). No status field marks it superseded |
| `research-primary.md` | 392 | 2026-04-03 | **Claim-by-claim verification** of paper v3 (10 claims incl. α, T=2.250, m_eff, χ=3) | Closest thing to a §6 claim-evidence map. Not machine-readable, no claim IDs, frozen at v3 (paper is now v5) |
| `task4-ope-argument.md` | 345 | 2026-04-01 | **Analytic argument** (spin-2 identification via OPE channel) | Self-superseded — `epsilon-channel-proof.md` §8 is titled "Correction to task4-ope-argument.md", but task4 carries no retraction banner |
| `research-challenge.md` | 249 | 2026-04-03 | **Adversarial review** — "Devil's Advocate Challenge: Paper v3." Has "Challenges Survived / NOT Survived", a "SINGLE WEAKEST LINK", and a traffic-light rating per result | The single most §12-shaped document in the repo, and it is unlinked from any hypothesis or simulation record |
| `research-practical.md` | 216 | 2026-04-03 | Submission-readiness assessment | Operational, not theory |
| `RUN-A-methods.md` | 93 | 2026-06-26 | **Pre-registered protocol** for HYP-028 Run A: realization choice, honest caveat, mandatory gates, "§6 Verdict logic (pre-registered)" | This is a genuine §36 prediction-registry entry in disguise. Not identified as one, not indexed, not machine-readable |
| `paper-review-synthesis.md` | 59 | 2026-04-03 | Synthesis of the above three reviews | — |

**Accurate statement of the defect:** the theory tier holds real analytic and adversarial content, but
**(a)** all of it is prose with no structured records, **(b)** no `theory-record.json` template exists
to structure it against, **(c)** 6 of 8 files are frozen at 2026-04 and describe paper **v3** while the
paper is at **v5** and is submitted to PRD, and **(d)** two of the files are superseded (task4 by
epsilon-channel-proof; task5-crofton by the refutation of HYP-014/022) **with no supersession marker
in the files themselves.** §32 forbids silently editing history; these files instead silently *retain*
it, which fails the same standard from the other direction.

### 4.2 Interpretive/theoretical content that exists ONLY in prose

Inventory of substantive theory/interpretation with **no** structured record anywhere. Each would need
a §14/§15 record.

**A. Design and protocol documents living beside the code (untracked as records):**

| Location | Content | Why it needs a record |
|---|---|---|
| `research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md` | The full biorthogonal-Koo-Saleur design for the project's **strongest** result (c_KS = −22/5). Referenced from `MEMORY.md` by relative path. | §13's fifteen questions (normalization sensitivity, conditioning, exceptional points, c vs c_eff) live here or nowhere. §15 dependency chain `CFT spectrum → T-identification → matrix-element normalization → central-charge estimator` is exactly this document's subject. |
| `research/tools/merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md` | Route-B circle design that produced SIM-067/068/069 | Method record for the C_TTT ladder |
| `research/tools/merakit-setup/CTTT-SPIN-RESOLUTION-DESIGN.md` | T/T̄ spin-resolution design step | Prerequisite derivation for C_TTT |
| `research/tools/merakit-setup/OPE-PEV-ROUTE-DESIGN.md` | PEV route for C_σσε (validated at SIM-061 after 3 failures) | Method record + failure history |

**B. Interpretation carried only in the memory topic files** (`~/.claude/projects/D--quantum-worldline/memory/`, 45 files, outside the repo entirely):

- `of_blocking_was_never_wrong.md` — the **wrong-basin** discovery: "energy FLAT across basins at χ=6,
  select by spectrum not energy." A methodological finding of genuine §5-Level-2 character. Not in
  `research/data/` in any form; not in ERRATA; not in the paper.
- `ope_parity_root_cause.md` — root-cause analysis distinguishing parity bugs from ρ³ geometry across
  SIM-056/058/060/061. A four-simulation debugging arc whose *conclusion* exists only in memory.
- `normalization_invariant_excess.md` — an explicit **no-go**: "PROVEN no state-only f(ρ) gives
  chain-independent excess transport degradation." §16 asks the project to pursue no-go results
  seriously; it has one, and it is filed in a session-memory note rather than a theory record.
- `discrete_crofton_positivity.md`, `crofton_force_failure_mechanism.md` — the *mechanism* of the
  Crofton failure (as opposed to the bare REFUTED verdict on HYP-014/022).
- `wanghe_boundary_not_free_fermion.md` — "not JW-quadratic; exact-diag caps ~N=16-18." A structural
  limit statement constraining every future ED plan.
- `mera-scaleinv-recipe.md`, `lowdepth_ansatz_powerlaw.md`, `z2_method.md` — method knowledge.
- `research_agenda_2026_05_29.md` — a self-generated ranked research menu. This is a §28/§39 portfolio
  artifact with no home in the repo.

**C. Interpretation embedded in the paper only.** `research/paper-draft-scipost.tex` and the PRD
package carry the holographic/worldline interpretation (stress-tensor exchange ⇒ "structural signature
of gravity"). §24 asks: "would the technical contribution still matter if every use of the word
'holographic' were deleted?" No record anywhere answers that question, per claim.

**D. Absent entirely (§6/§7/§12/§36).** The following required structures do not exist in prose or
otherwise: the **claim-evidence map** with `counterfactual_novelty` (§6), the **independence ledger**
(§7), **named killer tests** per hypothesis (§12 — `refutation_criteria` exists in the HYP schema and
is a partial proxy, but no killer is recorded as *applied*), and the **prediction registry** (§36 —
`RUN-A-methods.md` §6 is the only pre-registered verdict logic in the project, for one run).

### 4.3 RESEARCH-LOG defects

**(a) The log has a 3-week hole over the project's most consequential period.** Last entry is
`## 2026-07-21 / 07-27 -- scans #17 and #18` (`research/RESEARCH-LOG.md`, final section). Missing:

| Date | Event | Recorded in log? |
|---|---|---|
| 2026-08-07 | **PRD submission, accession DV13971** | No |
| 2026-08-09 | Scan #19 | No |
| 2026-08-10 | SIM-068 (C_TTT TCI) | No |
| 2026-08-11 | SIM-069 (Potts — "ladder complete") | No |
| 2026-08-11 | SIM-070 (HYP-028 Phase 1) | No |
| 2026-08-11 | **SIM-071 (c_KS = −4.29, the frontier result)** | No |

All six are in `NEXT-SESSION.md` and `MEMORY.md`, both of which are *state* documents that get
overwritten. The log is described in its own header as "the unlimited, version-controlled narrative
record… Detail lives here." For the last three weeks it does not.

**(b) The log header quotes a retracted number as a current anchor.**

> `research/RESEARCH-LOG.md:14` — "**Holographic transport** — T=(π/2)·l_AdS = 2.250 vs 2.266
> (**0.72%** at N=16)."

listed under "**The four published findings (anchors)**". ERRATA E2 retracted exactly this value:
`research/ERRATA.md:29` — "**E2** — Published '0.72% at N=16' transport residual is a time-grid
artifact; converged value −1.205%." The log's own line 129 records E2 as "most consequential."
**The file states the retracted number as an anchor 115 lines above its own retraction.** `README.md`
line 29 handles this correctly ("Earlier versions … quoted 0.72% … That value is a time-grid
artifact"); the log does not.

**(c) Chronological ordering is inconsistent.** The header says "(Newest first)". Lines 24–190 run
newest-first (2026-06-16 → 2026-06-08); from line 190 onward the file runs oldest-first (2026-06-17 →
2026-07-27). A reader following the stated convention reads the middle of the project first.

### 4.4 Forbidden-phrase scan (§8)

§8: "Avoid vague phrases such as 'to our knowledge,' 'novel framework,' 'first-ever,' or
'unprecedented' until the evidence for them has been recorded." Repo-wide grep over state docs, the
research log, the paper source, and the project review returned exactly one hit — and it is on the
frontier claim:

> `NEXT-SESSION.md:35-36` — "**First lattice extraction of a negative c from stress-tensor elements
> (to our knowledge).** HYP-028 → SUPPORTED (medium)."

Two §8 violations in one sentence ("First…", "to our knowledge"), attached to the single result the
standard nominates as the project's strongest and most novelty-sensitive (§13, §25 Candidate Paper A).
No literature-gate record supporting it exists anywhere in `research/data/`. The paper source
(`research/paper-draft-scipost.tex`) is **clean** of all four phrases — the overclaim is confined to
the internal state document, which is where the next session's framing comes from.

---

## 5. Memory index vs disk

Memory index: `C:/Users/jonca/.claude/projects/D--quantum-worldline/memory/MEMORY.md`.

### 5.1 ID high-water marks — PASS

| Class | MEMORY.md claim | Disk max | Match |
|---|---|---|---|
| PAPER | PAPER-138 | PAPER-2026-138 | ✅ |
| HW | HW-074 | HW-2026-074 | ✅ |
| HYP | HYP-030 | HYP-2026-030 | ✅ |
| SIM | SIM-071 | SIM-2026-071 | ✅ |

All four correct. HYP, PAPER and HW have **no ID gaps** (contiguous 1..N). SIM has 9 unassigned gaps
(`4, 7, 38, 41, 43, 46, 47, 48, 49`) — the memory index does not mention them, so "SIM-071" reads as
71 simulations when the real count is 62 distinct IDs / 73 record files.

*(Caveat: the high-water marks are correct in the **project** memory index but 7 SIM stale in the
**agent-memory** file the skills actually read — see §2.1. Two memory files, one right, one wrong, and
the tooling points at the wrong one.)*

### 5.2 Hypothesis status: MEMORY.md vs disk — **9 of 20 MISMATCH**

The `## Hypothesis Status Summary` table in `MEMORY.md` vs the `status` field in each
`research/data/hypotheses/HYP-2026-0NN.json`:

| HYP | MEMORY.md status | Disk `status` | Disk `last_updated` | Verdict |
|---|---|---|---|---|
| 002 | PARTIAL | `PARTIALLY_CONFIRMED` | — | OK |
| 006 | SUPPORTED | `SUPPORTED` | — | OK |
| 008 | SUPPORTED | `SUPPORTED` | — | OK |
| **009** | **PARTIAL** | `proposed` | 2026-03-26 | **MISMATCH** |
| 010 | INCONCLUSIVE | `inconclusive` | — | OK |
| **011** | **PARTIAL** | `proposed` | 2026-03-26 | **MISMATCH** |
| **012** | **NOT_SUPPORTED** | `proposed` | 2026-03-26 | **MISMATCH** |
| **013** | **PARTIALLY_REFUTED** | `proposed` | 2026-04-26 | **MISMATCH** |
| **014** | **REFUTED (high)** | `proposed` | 2026-04-26 | **MISMATCH** |
| **015** | **CONFIRMED_ANALYTIC** | `proposed` | 2026-04-26 | **MISMATCH** |
| **016** | **REFUTED (high)** | `proposed` | 2026-06-08 | **MISMATCH** |
| 017 | SHELVED | `SHELVED` | — | OK |
| **022** | **REFUTED (high)** | `proposed` | 2026-05-15 | **MISMATCH** |
| 023 | REFUTED | `REFUTED` | — | OK |
| 024 | NOT_ESTABLISHED | `NOT_ESTABLISHED` | — | OK |
| 025 | SUPPORTED | `SUPPORTED` | — | OK |
| 026 | SUPPORTED | `SUPPORTED` | — | OK |
| **027** | **SUPPORTED (high)** | `TESTABLE_NEAR_TERM` | 2026-06-16 | **MISMATCH** |
| 028 | SUPPORTED | `SUPPORTED` | — | OK |
| 029 | SUPPORTED (cond, low) | `SUPPORTED (conditional, confidence LOW)` | — | OK |

**Nine of twenty tracked hypotheses disagree.** The pattern is one-directional and unambiguous: **every
mismatch is a record that was never advanced past `proposed` after being tested.** I checked whether
the outcome was recorded in some *other* field instead — for 8 of the 9 it was not (only
`refutation_criteria`, `feasibility_verdict`, `feasibility_notes`, `status`, `last_updated` are
present; HYP-016 additionally has one `result_note_2026_06_08`).

The three worst, because memory rates them **REFUTED with high confidence**:

- **HYP-2026-014** (Crofton sin profile) — memory: "REFUTED / high / amplitude match coincidence."
  Disk: `status: proposed`, untouched since 2026-04-26. §32 requires preserving original claim,
  challenge, corrected analysis, and changed conclusion. The changed conclusion is not on disk.
- **HYP-2026-016** (IonQ Cambridge insufficient) — memory: REFUTED / high. Disk: `proposed`.
- **HYP-2026-022** (PEE-thread/Kirillov Crofton, α=0.883) — memory: REFUTED / high. Disk: `proposed`.

And the most operationally damaging:

- **HYP-2026-027** — memory: "**SUPPORTED / high**, α=4 UNIVERSAL at tricritical Ising." Disk:
  `status: TESTABLE_NEAR_TERM`, `last_updated: 2026-06-16`. Nine simulations link to HYP-027
  (SIM-050/051/052/058/060/061/064/065/066/067), **five of which postdate the record's last update**,
  including SIM-067 (C_TTT Ising, 2026-07-19) and SIM-068 (2026-08-10). A hypothesis the project
  presents as a headline supported result has, on disk, neither an outcome nor an update in two months.

**Read against §38.A.2 ("Which are active, confirmed, supported, refuted, or shelved?"): the structured
records cannot answer that question. Only the memory index can, and the memory index is not
version-controlled with the repo.** Anyone auditing `research/data/hypotheses/` alone would conclude
that 17 of 30 hypotheses are still merely `proposed`, including three the project considers firmly
refuted.

### 5.3 Other memory-vs-disk checks

| Memory claim | Disk | Verdict |
|---|---|---|
| "14 agents at `~/.claude/agents/` (copies, Windows); 6 skills symlinked" | 14 agents byte-identical; 6 symlinks live | ✅ |
| `feedback_model_assignment.md` — "Opus for ALL physics agents, no Sonnet on science" | 8/14 agents are `model: sonnet`, incl. `physics-scanner`, `hardware-tracker`, `classical-simulator` | ❌ contradicted |
| "Scan #19 (2026-08-09) … EMPTY" | `research/digests/2026-08-09-scan.md` present | ✅ |
| "Scan #20 due ~08-16" | Today is 08-17; no `2026-08-1[6-7]*` digest | ⚠️ overdue by 1 day |
| `research/data/theory/` implied empty (audit brief; not a memory claim) | 8 files | ❌ (see §4.1) |

### 5.4 Pipeline mirror drift (`CLAUDE.md` rule)

`CLAUDE.md`: "`research/tools/MERAKit.jl/` is GITIGNORED (vendored package). After editing any `qw_*.jl`
driver there, copy it to `research/tools/merakit-setup/` (the tracked mirror) before committing."

Verified: 48 files under `research/tools/` **are** git-tracked (`merakit-setup` 27, `pumps-setup` 8,
`yanglee-pt` 8, `cttt-circle` 4, `RUN-MERAKIT.md` 1); `.gitignore:51-54` ignores only `MERAKit.jl/`,
`juliahome/`, `puMPS/`. The mirror mechanism works. Two exceptions:

1. **4 drivers exist only in the gitignored vendor tree** — `qw_diag_blocking.jl`,
   `qw_diag_blocking2.jl`, `qw_diag_fusion.jl`, `qw_potts_smoke.jl` (20 in `MERAKit.jl/`, 16 in
   `merakit-setup/`). Diagnostics and a Potts smoke test, i.e. exactly the validation code §22 wants
   preserved so known failures cannot silently return. They are one `rm -rf` from gone.
2. **`qw_tci.jl` has DRIFTED** — the tracked mirror is stale and materially different, not cosmetically:

   | | tracked `merakit-setup/qw_tci.jl` | vendored `MERAKit.jl/qw_tci.jl` |
   |---|---|---|
   | mtime | 2026-06-20 22:57 | 2026-06-20 **23:13** (newer) |
   | size | 1,469 B | 1,557 B |
   | blocking | `block_size=3` → dim-8 sites | `block_size=2` → dim-4 sites |
   | loader | `load_hb` reads `hb_lam3_*.txt` (64×64) | `load_hb4` reads `hb4_lam3_*.txt` (16×16) |

   Different lattice blocking and a different operator file. The version under version control is
   **not** the version that ran last. This is the tricritical-Ising driver behind HYP-027 / SIM-051 /
   SIM-052 — the α=4 universality claim. Which of the two produced which record is not determinable
   from the records (no code revision field: 3/73, §3.7).

---

## 6. Consolidated defect register

Severity: **CRITICAL** = corrupts or loses evidence for a headline claim; **MAJOR** = defeats a
governing-standard requirement; **MINOR** = hygiene.

| # | Sev | Defect | Location |
|---|---|---|---|
| 1 | CRITICAL | 9/20 hypothesis statuses disagree between memory index and disk; every mismatch is a tested hypothesis left at `proposed`. Includes 3 rated REFUTED/high (014, 016, 022) and HYP-027 rated SUPPORTED/high but stored as a feasibility verdict. | `research/data/hypotheses/HYP-2026-{009,011,012,013,014,015,016,022,027}.json` `status` field vs `MEMORY.md` "Hypothesis Status Summary" |
| 2 | CRITICAL | RESEARCH-LOG header lists the **retracted** 0.72% transport residual as a current published anchor, 115 lines above its own record of the retraction. | `research/RESEARCH-LOG.md:14` vs `research/ERRATA.md:29` |
| 3 | CRITICAL | §8 forbidden novelty language on the frontier result, with no literature-gate record: "First lattice extraction of a negative c … (to our knowledge)". | `NEXT-SESSION.md:35-36` |
| 4 | CRITICAL | Three skills instruct agents to read a **7-ID-stale** counter file; ID collisions are an already-realized defect (ERRATA D1). | `skills/{research-query,simulate,weekly-scan}/SKILL.md` → `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md:4` |
| 5 | MAJOR | 10 of §27's 14 roles have no agent; **all six purely-adversarial roles are absent**. 0 fully covered, 4 partial. | `agents/*.md` vs RESEARCH-DIRECTOR §27 |
| 6 | MAJOR | Schema conformance has **regressed** since ERRATA D3: SIM 20/85 (23.5%), HYP 13/30 (43.3%, was 64%). PAPER 101/139 and HW 48/76 were never audited. | `research/data/{simulations,hypotheses,papers,hardware}/` vs `templates/*.json`; ERRATA D3 |
| 7 | MAJOR | The 5 headline-result SIM records (067–071) all fail schema and omit `hypothesis_id`, so the evidence for the strongest claim is not joinable to HYP-028 by the documented key. | `research/data/simulations/SIM-2026-0{67,68,69,70,71}.json` |
| 8 | MAJOR | §21 reproducibility metadata effectively absent: code revision 3/73, environment 1/73, checksums 0/73, solver settings 3/73. | `research/data/simulations/SIM-2026-*.json` |
| 9 | MAJOR | No frozen research snapshot linked to the PRD submission (DV13971, 2026-08-07); 4 SIM records landed after it on the same branch. §21. | `NEXT-SESSION.md` hot-state block; git log |
| 10 | MAJOR | RESEARCH-LOG has a 3-week gap covering PRD submission, scan #19, and SIM-068/069/070/071 — the project's most consequential results. | `research/RESEARCH-LOG.md` final entry `2026-07-21 / 07-27` |
| 11 | MAJOR | No `theory-record.json` template; theory tier is 8 prose files, 6 frozen at paper v3, 2 silently superseded. §14/§15. | `research/data/theory/`, `templates/` |
| 12 | MAJOR | No claim-evidence map (§6), no independence ledger (§7), no prediction registry (§36), no applied-killer records (§12) in any form. | absent repo-wide |
| 13 | MAJOR | Tracked mirror `merakit-setup/qw_tci.jl` differs materially (block_size 3→2, different operator file) from the newer vendored driver behind HYP-027/SIM-051/052; 4 further drivers exist only in the gitignored tree. | `research/tools/{MERAKit.jl,merakit-setup}/qw_*.jl` |
| 14 | MAJOR | `hooks/hooks.json` (the ID-format guard) has never fired — plugin not installed and `plugin.json` declares no `hooks` key. The one automated defence against defects #6/#7 is dead. | `hooks/hooks.json`, `.claude-plugin/plugin.json` |
| 15 | MINOR | Model policy contradiction: memory says "Opus for ALL physics agents, no Sonnet on science"; 8/14 agents are sonnet, 3 of them doing science. | `agents/*.md` frontmatter vs `MEMORY.md` → `feedback_model_assignment.md` |
| 16 | MINOR | `SIM-2026-031.json` contains a literal `NaN` (strict-JSON invalid) and is not covered by ERRATA D2, which names only `worldline_mc_results.json`. | `research/data/simulations/SIM-2026-031.json`; `research/ERRATA.md:73` |
| 17 | MINOR | `builds/` has no template, no ID space, and 0/17 JSON files carry an `id`. | `research/data/builds/`, `templates/` |
| 18 | MINOR | 12 raw-output blobs sit in `simulations/` and 3 in `papers/`+`hardware/`, inflating record counts (85 vs 73 real SIM records). | `research/data/simulations/*.json` (non-`SIM-2026-*`) |
| 19 | MINOR | 9 unassigned SIM ID gaps (4, 7, 38, 41, 43, 46–49) undocumented; `SIM-071` reads as 71 sims, actual 62 distinct IDs. | `research/data/simulations/` |
| 20 | MINOR | 8 SIM ids violate the `^SIM-\d{4}-\d{3,}$` regex via letter/word suffixes (`008a`, `008b-8q-test`, `015b/c/d`, `032b`, `033b`). | `research/data/simulations/` |
| 21 | MINOR | RESEARCH-LOG chronology is newest-first for lines 24–190 then oldest-first from 190 on, contradicting its own stated convention. | `research/RESEARCH-LOG.md:22` |
| 22 | MINOR | Skill directory names ≠ registered `name:` (`weekly-scan` vs `qw-scan`); `CLAUDE.md`'s skill table documents the non-registered form. | `skills/*/SKILL.md`, `CLAUDE.md` Skills table |
| 23 | MINOR | Stale obsolete note: agent-memory records "`philosophy-agent` … is NOT installed" (2026-05-12); it is installed and byte-identical today. | `~/.claude/agent-memory/worldline-orchestrator/MEMORY.md:11` |
| 24 | MINOR | RESEARCH-DIRECTOR §3 says "approximately 30 weekly literature scans"; there are 19 numbered scans (30 files in `digests/`, incl. non-scan reports). | `docs/governance/RESEARCH-DIRECTOR.md:122`, `research/digests/` |

### 6.1 Things that PASS (recorded so the map is not one-sided)

- All 14 agents byte-identical between `agents/` and `~/.claude/agents/` (re-verified 2026-08-17,
  extending the `CLAUDE.md` 2026-07-06 check).
- All 6 skills correctly symlinked; `research/knowledge-base.md` present and contains the heading the
  `hardware-status` skill parses.
- PAPER, HW, HYP ID spaces are **contiguous with zero gaps** — the dedup/high-water discipline
  `CLAUDE.md` describes is working for three of four classes.
- Project memory-index high-water marks (PAPER-138/HW-074/HYP-030/SIM-071) are **all four correct**.
- `research/tools/` mirrors ARE git-tracked (48 files); only 1 file drifted and 4 are unmirrored.
- The paper source `research/paper-draft-scipost.tex` is **clean** of all four §8 forbidden phrases.
- `README.md:29` correctly and prominently carries the E2 transport retraction.
- The project produced genuine adversarial artifacts (`theory/research-challenge.md`) and a genuine
  pre-registration (`theory/RUN-A-methods.md` §6 "Verdict logic (pre-registered)"). The failure is that
  neither is institutionalized as a role or a record type — both were one-offs.

---

## 7. UNVERIFIED

Stated explicitly per protocol; silence is not a pass.

1. **Whether the 9 status mismatches are "wrong on disk" or "wrong in memory."** I verified only that
   they *disagree*, and that the disk records carry no outcome field. I did not re-derive from the
   simulation evidence whether HYP-014/016/022 are genuinely refuted or HYP-027 genuinely supported.
   Another audit thread must adjudicate; my finding is the inconsistency, not the truth.
2. **Which `qw_tci.jl` variant produced SIM-051 and SIM-052.** No code-revision field exists in either
   record, and both driver copies predate the records. I established that the tracked and vendored
   copies differ materially and that the vendored one is newer; I did not run either.
3. **Whether the 4 vendor-only drivers were ever load-bearing for a recorded result.** Filenames
   (`qw_diag_*`, `qw_potts_smoke`) suggest diagnostics; I did not trace them to specific SIM records.
4. **Adversarial-role coverage inside teammate sessions.** §27 roles could in principle be enacted by
   prompt at dispatch time rather than by agent definition. I audited `agents/*.md` and
   `skills/*/SKILL.md` only. I found no such prompt-level adversarial injection in the skills, but I did
   not read session transcripts in `~/.claude/projects/`.
5. **Whether the 38 non-conformant PAPER records and 28 HW records represent lost information or just
   sparse-but-adequate records.** I measured schema conformance, not scientific adequacy. Many are
   probably deliberate stubs for low-relevance items.
6. **Whether ERRATA D3's original 9/36 and 16/25 were computed with the same strictness as my
   validator.** My numbers use strict case-sensitive enum matching. If D3 was lenient, the HYP
   regression (64% → 43%) may be partly definitional; the lenient recomputation (60%) is still below
   D3's 64%, so a regression exists under either reading, but its size is uncertain.
7. **`research/data/audit/`** was empty except for `raw/` at session start; I did not check for prior
   audit outputs elsewhere that might already cover some of this ground.
8. **Content of the 6 archived-scan digests and the paper's §-by-§ interpretive claims.** §4.2.C is an
   inventory-by-location claim, not a line-level audit of the manuscript's interpretive assertions —
   that belongs to the manuscript audit thread.

---

*End of `inv:infrastructure` artifact.*
