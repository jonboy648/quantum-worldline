# Practical constraints: what this project can afford to produce, and who will ever see it

**Role:** practical-analysis researcher. This file answers cost, throughput, distribution, risk and
timeline. It deliberately recommends **no physics direction**; that is the other two researchers'
job. Every number below names the file and field it came from, or is marked **ESTIMATE**.

---

## Summary (5 lines)

1. **Compute is not the constraint and has not been for months.** Every headline result since
   2026-07-19 ran on the local 24-core / 64 GB box for zero dollars; total RunPod spend attributable
   to this project over the last 90 days is under 25 USD. The binding resource is **active days**:
   34 of the last 91 calendar days carry a commit, a 37 percent duty cycle.
2. **Sustainable throughput is 3 to 4 fully pre-registered, gated, written-up experiments per month**,
   and the recent record shows that number is limited by design and write-up time, not by hardware.
3. **Distribution is the actual wall.** The entire measured public reach of this project is
   **75 views, 72 unique visitors and 42 downloads** on the Zenodo concept record since 2026-04-20
   (verified against the live Zenodo API today). Every peer-reviewed route runs through arXiv, and
   arXiv tightened its endorsement policy on 2026-01-21 in the direction that hurts most here.
4. **The repeat failure mode is a gate or a test that was never smoke-tested against reality before
   it was committed.** SIM-078's G2 smoke test exists and passes, and it was run and committed
   **after** the pod had already failed the gate, not before.
5. **Cost discipline is self-reported and drifts.** Internal records claim about 7 USD across
   2026-09-07 to 09-09; the RunPod billing API returns **9.37 USD** for pods on those three days.

---

## A. Cost per instrument

### A.1 Exact diagonalization, dense state vector, local machine

The local machine is better than the project's own notes suggest: **24 logical cores and 65,296 MB of
RAM** (`systeminfo`, checked this session), not only the RTX 4060 8 GB the memory index names. Every
ED number below is **measured wall clock** from the run logs, single machine, no cloud.

| L (sites) | Hilbert dim | Ground state | Full experiment | Source |
|---|---|---|---|---|
| 12 to 16 | 4.1e3 to 6.6e4 | under 1 s | "seconds" | `SIM-2026-074.json` -> `runtime` |
| 20 | 1.05e6 | 15 s (h=1), 11 s (h=2) | 215 s incl. 168 s G5 | `research/tools/channel-test/run_stress_n20.log` |
| 20, smeared probes | 1.05e6 | 14 s | 87 s | `run_stress_n20_smear.log` |
| 24, open chain | 1.68e7 | 368 s (h=1), 200 s (h=2) | 4,535 s incl. 3,412 s G5 | `run_stress_n24.log` |
| 24, PBC ring, 4 arms | 1.68e7 | 325 s | 1,445 s | `run_ring_n24.log` |
| 24, cached GS | 1.68e7 | 0 (cached) | 214 s | `SIM-2026-073.json` -> `runtime` |
| 24, KW duality check | 1.68e7 | cached | 1,501 s | `SIM-2026-074.json` -> `runtime_s` |

**Dollar cost of every row above: zero.** These were local runs.

**Measured scaling.** Ground state 15 s at L=20 to 325 s at L=24 is **21.7x for a 16x dimension
increase**. Applying that ratio forward:

| L | Hilbert dim | Bytes per complex128 vector | GS, ESTIMATE | Feasible on 64 GB? |
|---|---|---|---|---|
| 26 | 6.7e7 | 1.07 GB | 25 min | Yes, about 21 GB with ncv=20 |
| 28 | 2.7e8 | 4.3 GB | 2.0 h | **No** at ncv=20 (about 86 GB). Needs symmetry sectors |
| 30 | 1.1e9 | 17 GB | 8 h | No |

**L=26 is the real local ED ceiling, not L=24.** Nothing in the record has ever been run at L=26. The
project already owns the tool that would push past it: `SIM-2026-075.json` -> `hardware` records
"sector-projected Lanczos (P H P + shift)" for gate G5. A Z2-sector projection halves the dimension
and would put L=28 inside 64 GB. Marked ESTIMATE; not measured.

### A.2 MERA and puMPS

| Instrument | Sizes reached | Wall clock | Dollars | Source |
|---|---|---|---|---|
| MERA chi=10 and chi=12, Z2, 16 parallel seeds | 8-site blocks | about 4 h | **about 4 USD** | `SIM-2026-066.json` -> `hardware` (RunPod cpu3c, 32 vCPU, 64 GB, 0.96 USD/h) |
| Sparse ED circle route, Ising C_TTT | N=8 to 18 | not recorded | 0 (local) | `SIM-2026-067.json` -> `hardware` |
| puMPS, TCI, D up to 28 | N=14 to 56 | "pairs, about 10-30 min" per round, 7 external kills | 0 (local) | `SIM-2026-068.json` narrative |
| puMPS, Potts, 4 rungs | N=10 to 20+ | "hours of D=28+ compute would purchase no conclusion" | 0 (local) | `SIM-2026-069.json` -> `verdict` |
| Non-Hermitian Arnoldi, Yang-Lee | L=10 to 18 | not recorded; L=20 skipped on build cost | 0 (local) | `SIM-2026-071.json` |

**Gap worth naming:** SIM-067 through SIM-071 record **no wall-clock field at all**. Five of the
project's best results have no cost-of-production number. Any future planning that quotes "what a
MERA run costs" is quoting an estimate, not a measurement. Add a `runtime_s` field to the SIM schema.

The one hard dollar figure in the MERA family is SIM-066's **4 USD for 4 hours of 32 vCPU**, and that
run produced an honest negative (Route A closed).

### A.3 Complex-time MPO, the SIM-078 instrument

Measured locally, `research/tools/timelike-ee/sim078_g2scan_local.json`, single process,
R_H=5, delta=0:

| L | chi | secs | bond actually reached | discarded weight |
|---|---|---|---|---|
| 8 | 64 | 52.3 | 64 | 4.7e-4 |
| 8 | 128 | 81.3 | 128 | 1.8e-4 |
| 8 | 256 | 81.7 | 256 (saturated, exact) | 3.4e-28 |
| 8 | 512 | 96.2 | 256 (saturated, exact) | 3.4e-28 |
| 10 | 64 | 142.3 | 64 | 9.3e-4 |

Measured on RunPod, `research/tools/timelike-ee/runpod_sim078.log` and `sim078_gates.json`:

- Pod `fiip7fruevt6e3`, RTX 4000 Ada host used for its **16 vCPU**, 62 GB, **0.28 USD/h**. The GPU was
  never used; the log says so explicitly.
- Gate stage start 20:34:23Z, finish 22:49:05Z = **2 h 14 min 42 s**. G1 was 12 rows at L=12 and 14,
  chi=128, dbeta=0.05; G2 was 3 rows at L=12, 16, 24, chi=128.
- **Billed: 0.3213 USD** for that pod on 2026-09-09 (RunPod billing API, `podId fiip7fruevt6e3`,
  queried live this session). The second delete line at 04:34:58Z was a no-op; the pod was already
  gone. The "about 1 USD" in `NEXT-SESSION.md` is correct for this pod and slightly conservative.

**Extrapolation to L=32 / 64 / 128 (ESTIMATE, and the most important estimate in this file).**

Cost of one MPO build scales as `n_steps x L x chi^3`, with `n_steps = |beta| / dbeta` and
`|beta| = sqrt(R_H^2 + delta^2)`. Calibrating on L=10, chi=64, 100 steps, 142.3 s gives
about 5.4e-7 s per unit. Under that model, one grid point at dbeta=0.05:

| Setting | R_H | \|beta\| | steps | L=32, chi=128 | L=64, chi=128 | L=128, chi=128 | L=128, chi=256 |
|---|---|---|---|---|---|---|---|
| A | 5 | 7.07 | 141 | 1.4 h | 2.8 h | 5.7 h | 45 h |
| B | 8 | 9.43 | 189 | 1.9 h | 3.8 h | 7.6 h | 61 h |
| C | 12 | 13.0 | 260 | 2.6 h | 5.2 h | 10.4 h | 83 h |

Those are **single-process** hours. The RunPod host gives BLAS threading only, so assume a 3x to 4x
effective speedup, ESTIMATE, not measured. At 0.28 USD/h:

- **Setting A, all seven sizes, all eight h_z values, chi=128:** about 10 USD.
- **Settings A and B together, chi=128:** about 24 USD. That is the entire 25 USD cap in
  `PREREGISTRATION-HYP032-B.md`.
- **Setting C, or any setting at chi=256:** 8x the chi=128 figure. **Not affordable at the registered
  cap, and not close.**

**The cost driver is R_H, the real-time extent, not L.** Under damping delta=5 the operator is
effectively thermal at temperature 0.2, so its entanglement saturates with L but grows with real
time. Setting C's `|beta| = 13` is where this becomes an exponential-in-chi problem. The
pre-registration already hedges Setting C as "best-effort" and "not required for a verdict"; the
numbers say that hedge was correct and should be read as "Setting C will not run".

**Whether chi=128 converges at L greater than 24 is unmeasured.** G3 is the gate that decides it and
it has never been evaluated above L=14. If chi=128 fails G3, the grid does not fit the cap at all.
That single unknown is the difference between a 10 USD experiment and an unaffordable one.

---

## B. Throughput: how many experiments per month actually land

Counted from the `date` field of `research/data/simulations/SIM-2026-0NN.json` and from
`git log --since=2026-06-16`.

| Measure | Value | Source |
|---|---|---|
| SIM records dated in the 90-day window | **23** (SIM-055 to SIM-077) | `date` field of each JSON |
| Distinct calendar dates carrying a SIM record | 16 | same |
| Commits in the window | 151 | `git log --since=2026-06-16 --oneline \| wc -l` |
| Distinct days with any commit | **34 of 91** (37 percent) | `git log --pretty=%ad --date=short \| sort -u` |
| Longest silent gap | 2026-08-24 to 2026-09-04, 11 days | commit dates |
| Second gap | 2026-07-27 to 2026-08-06, 10 days | commit dates |
| Busiest day | 2026-09-07, 24 commits | commit dates |

Raw arithmetic gives 7.7 SIM records per month. **That number is misleading and should not be
planned against.** Ten of the 23 records (SIM-055 to SIM-064, 2026-06-26 to 07-04) were
chi-escalations and repair passes on an already-built pipeline. They cost a day each because the
instrument already existed.

The honest rate is the **pre-registered** rate. Every pre-registration in the repo was committed on
or after 2026-08-23:

| Pre-registration | Committed | Record | Outcome |
|---|---|---|---|
| `channel-test/PREREGISTRATION.md` | 2026-08-23 | SIM-073 | INDETERMINATE |
| `channel-test/PREREGISTRATION-RING.md` | 2026-08-24 | SIM-074 | Voided SIM-073's contrast |
| `channel-test/PREREGISTRATION-T.md` | 2026-09-06 | SIM-075 | VOID, HYP-008 closed |
| `timelike-ee/PREREGISTRATION-HYP032.md` | 2026-09-07 | SIM-076 | Level-1 VOID |
| `timelike-ee/PREREGISTRATION-HYP032-A.md` | 2026-09-07 | SIM-077 | Level-3 negative |
| `timelike-ee/PREREGISTRATION-HYP032-B.md` | 2026-09-09 | SIM-078 | Stopped at a failed gate |

Five completed records in the 22 days from 2026-08-23 to today, including a 14-day stretch
(08-24 to 09-07) that produced none because it went entirely to Zenodo v5 and the story.

**On an active day, pre-registration to written-up record takes about one day.** The delay is never
the compute. It is the gap between active days, plus the approval gate: HYP-032-B waited on Jon's
"pre regis fine" then "word", and SIM-078 has now been stopped at a failed gate waiting on his
decision since 2026-09-09.

**Planning figure: 3 to 4 pre-registered, gated, written-up experiments per month**, sustained, one
person plus agents. Four is the ceiling only in a month with no publishing or correction work in it,
and the last 90 days contained two such months out of three.

---

## C. The distribution problem

### C.1 The measured reach, checked live today

Queried against the Zenodo public API this session, not from any internal note:

| Record | DOI | Published | Views | Unique | Downloads |
|---|---|---|---|---|---|
| Concept (all versions) | 10.5281/zenodo.19660302 | since 2026-04-20 | **75** | **72** | **42** |
| v5 (current) | 10.5281/zenodo.22080720 | 2026-09-06 | (same aggregate) | | |

Zenodo reports these at concept level, so 75 views is the **lifetime total across all five versions
over five months**. The GitHub mirror returns HTTP 404 to an unauthenticated request, confirming it is
private, so it contributes zero.

**That is the whole audience.** Seventy-two people, some of whom are Jon and the crawlers. One
physicist replying to one email would roughly double the number of informed readers.

### C.2 Routes, honestly evaluated

**arXiv is the chokepoint, and it got worse this year.** Verified today: on **2026-01-21** arXiv
stopped accepting an institutional email address as a sole automatic qualifier. New submitters now
need an institutional address **and** prior authorship in the relevant domain, or a personal
endorsement from an established arXiv author. Endorsers must have authored a threshold number of
papers submitted **between three months and five years ago**. There is no unaffiliated route and no
appeal path documented.

| Route | Barrier | Time to first decision | Probability, ESTIMATE | Jon-hours, ESTIMATE |
|---|---|---|---|---|
| **Zenodo DOI** (have it) | None. Already done, v5 live | 0 | 1.0, already achieved | 0 |
| **arXiv endorsement** | Needs a named endorser. 7 physicists emailed 2026-07-15/19, zero replies by 08-04 | Indefinite | **0.10 to 0.20 per new batch of 7** | 6 to 10 per batch |
| **SciPost** | Account approval outstanding since 2026-04-30, never re-checked. SciPost encourages but does not strictly require arXiv, and runs its own preprint server | Unknown; silent 4.5 months | 0.15, and **the account state must be freshly checked before any estimate is trusted** | 2 to check, 15 to submit |
| **PRD / PRB / PRResearch** | APS desk rejection 2026-08-12 said "APS will not consider this manuscript further". Read literally that is all APS journals, not only PRD | n/a | **near 0 for this manuscript**; unknown for a genuinely new one | 0 |
| **PRResearch, new manuscript** | 2,755 USD APC. Waivers are for low-income countries and hardship on request; US independent researcher is not an automatic case | 2 to 6 months | 0.15 to 0.25 for a corrected Level-2 methods paper | 40 to 80 |
| **Quantum (quantum-journal.org)** | **Requires an arXiv reference posted to or cross-listed with quant-ph.** So it is downstream of the endorsement wall. Voluntary APC | n/a until arXiv clears | 0 while arXiv is blocked | 0 |
| **viXra** | No barrier at all, which is precisely the problem. It is not indexed by INSPIRE, NASA ADS or Google Scholar in the way arXiv is, and a viXra listing is read by working physicists as a negative signal. Posting there would make the corrected record harder to take seriously, not easier | 1 day | Reach comparable to Zenodo, credibility lower | 2 |
| **Public GitHub + Zenodo release DOI** | Zero barrier. Currently blocked by Jon's own standing decision (repo private, no push) | 1 day once he agrees | Reach: ESTIMATE 2x to 5x current Zenodo traffic. Citability: same DOI already exists | 1 to 2 |
| **Journal of Open Source Software** | Needs **six months of public repository history before submission**, plus "obvious research application", feature-complete, not a single-paper analysis script. The repo has **zero days** of public history since it went private on 2026-09-07 | 6 months minimum before the clock even permits submission | 0.4 if the instrument is genuinely reusable and the clock is started now | 20 to 40, plus 6 months of elapsed time |
| **Replication initiatives / ReScience** | Would take a reproduction of someone else's published result. The project has several (PAPER-133 reproduced at 0.01 percent, SIM-070) | 2 to 4 months | 0.4 to 0.5 for a clean reproduction paper | 30 to 50 |

### C.3 The three honest readings of C.2

1. **Nothing peer-reviewed happens without an endorser or an institution.** arXiv gates Quantum
   outright, effectively gates SciPost's visibility, and APS has said no. The endorsement problem is
   not a formatting problem; it is the whole problem.
2. **The only lever entirely inside Jon's control is making the repository public.** It costs one to
   two hours, starts the JOSS six-month clock, and is the single highest-leverage distribution act
   available. It is also a standing-rule change and therefore his call alone.
3. **The cheapest credible route that does not need an endorser is a reproduction or an instrument
   paper, not a discovery paper.** ReScience and JOSS both accept unaffiliated authors and neither
   requires arXiv. The project's reproductions are already among its strongest verified artifacts.

---

## D. Risk register, from this project's own history

| # | Failure mode | Where it happened | What mitigates it **now** | What does **not** |
|---|---|---|---|---|
| D-a | **Estimator artifact.** Unweighted least squares in linear space put 95.8 percent of the objective on one point | SIM-072, ERRATA E6, the withdrawn alpha=3.92 | RESEARCH-DIRECTOR section 6 counterfactual novelty; the plateau condition in `PREREGISTRATION-HYP032-B.md` pass rule 4 | **No standing rule requires an estimator sweep before a number is quoted.** HYP-032-B specifies a bar and a window but never says "vary the estimator". The 15-estimator matrix that caught E6 was run once, retrospectively |
| D-b | **Killer test compared a thing to itself.** Kramers-Wannier self-duality makes ZZ and X the same operator at h=1 | SIM-074, voiding SIM-073 | Nothing structural. It was caught by a person noticing, not by a gate | **No gate checks that two probes are independent under the model's symmetries.** This is the cheapest missing control in the project: one commutator or duality check, seconds of compute, before any contrast experiment |
| D-c | **Wrong-basin MERA.** Energy is flat across basins at chi=6; selecting by energy silently picks the wrong state | `of_blocking_was_never_wrong` memory; the old non-critical sigma artifact | Documented discipline: identify by parity class not dimension, require 3 clean basins, C_sigma-sigma-sigma=0 as a cheap Z2 probe | Discipline in prose is not a gate. Nothing in the drivers enforces it |
| D-d | **Same-origin operational records.** Three internal notes agreed for 11 days that PRD had the paper; it had been rejected | The 2026-08-12 desk rejection, found 08-17 | `CLAUDE.md` external-status rule and `NEXT-SESSION.md` item 0d | **No automated check exists.** The expired cron is exactly what caused it. Note how cheap the fix is: verifying Zenodo live and the GitHub mirror's 404 took two curl calls and about five seconds this session. That belongs in a session-start script, not in a rule someone has to remember |
| D-e | **A gate placed where it cannot pass.** G2 was registered at delta=0, undamped real-time evolution, whose cost is exponential in evolution time. Every production setting uses delta=5 | SIM-078, stopped 2026-09-09 | The gate worked as designed: the runner refused to start the grid. That is the system functioning | **The smoke test that would have caught it was run afterwards.** `sim078_g2scan_local.json` was committed at `8c56cf3`, 2026-09-09 18:01 local, which is after the pod reported the failure at 22:49 UTC. The pre-registration permitted "gate-only smoke tests at L <= 12 that take seconds" and they were not run before commit. **Rule that would fix it: no gate may be committed until it has been demonstrated to pass at the smallest size, on the production settings** |
| D-f | **Pre-registration built on a mis-stated summary.** The SIM-077 summary described a peak at L=14 that was at L=12, and omitted both the 52 percent monotone drift and the nonzero background | ERRATA D9; corrected inside `PREREGISTRATION-HYP032-B.md` before the design that depended on it | The HYP-032-B practice of re-reading the raw stored data before designing, and recording the corrections first | It worked because one person chose to do it. Nothing requires it |
| D-g | **Cost records drift from billing.** Internal records say about 6 USD for SIM-077 plus about 1 USD for SIM-078. The RunPod billing API returns **9.37 USD** across pods on 2026-09-07, 09-08 and 09-09 | This session's live billing query | Nothing | The 25 USD caps in the pre-registrations are enforced against self-reported prices at pod-create time, not against billing. Caveat: not every pod on those dates is provably this project's, so 9.37 is an upper bound on the discrepancy, not a proven one |
| D-h | **Research log stopped.** `research/RESEARCH-LOG.md` last entry is 2026-08-17. SIM-073 through SIM-078 are absent | 28 days of unlogged work | The SIM JSON records are complete and are the record of authority | The narrative that lets a future session reconstruct why things were done has a 4-week hole, during which the project closed HYP-008, ran HYP-032 twice and published Zenodo v5 |

---

## E. Timeline for three scales of ambition

Assumptions held constant: 25 USD cap per experiment, 3 to 4 pre-registered experiments per month,
37 percent duty cycle, no institutional access, no new hardware.

### E.1 One clean negative

**Precedent, measured.** SIM-075 (VOID, local, 0 USD). SIM-076 (Level-1 VOID, `budget_used` field:
"one session, about 0 USD"). SIM-077 (Level-3 negative, 6 USD recorded).

- **Calendar:** 2 to 3 weeks from question to committed record, of which 2 to 4 are active days.
- **Budget:** 0 to 10 USD. Most of the project's negatives cost nothing.
- **Probability of completing:** high, 0.8 plus. The project is demonstrably good at this. Six of the
  last seven SIM records are negatives, voids or corrections, and they are properly gated.
- **Caveat:** a negative that nobody reads is worth what the reading is worth. See section C.

### E.2 One Level-3 result, new physics inside an established framework

**Base rate, measured.** `AUDIT-2026-08-11.md` section 2.2: "**None confirmed. Two candidates, both
failed their gate.**" Across 78 SIM records the project has produced zero confirmed Level-3 results.

- **Calendar:** 4 to 7 months. That is 6 to 10 active weeks of work spread at the observed duty
  cycle, across 3 to 5 pre-registered attempts, because the per-attempt success rate is low.
- **Budget:** 25 to 75 USD of compute. Trivial. The cost is entirely Jon's time.
- **Probability of a confirmed Level-3 in that window: ESTIMATE 20 to 35 percent**, anchored on a
  base rate of zero in 78 and adjusted upward because the governing standard and the
  pre-registration discipline now exist and did not before 2026-08-17.
- **Binding constraint:** not compute, not money. It is finding a question whose answer is not fixed
  in advance. `AUDIT-2026-08-11.md` section 1: of 34 claims involving a calculation, **21 could not
  have come out otherwise**. That ratio, not the hardware, is what caps the project's output.

### E.3 One Level-4 discriminating result

**Base rate, measured.** `AUDIT-2026-08-11.md` section 2.1: "**None.** No matched non-geometric
control, no rewiring experiment, no reconstruction-locality test has ever been run in this
repository." The instrument does not exist.

- **Build phase first:** 2 to 4 active weeks to construct the discriminating apparatus at all. The
  concrete candidate already named in `NEXT-SESSION.md` item 3 is a GEO-1 gauge-transformation slice.
  Nothing can be measured until that exists.
- **Calendar:** 6 to 12 months end to end.
- **Budget:** 100 to 300 USD of compute, ESTIMATE, dominated by whatever the control requires at
  L=64 or above. Still small.
- **Probability: ESTIMATE under 15 percent**, and that is generous for a base rate of zero across the
  project's entire history.
- **The honest framing:** a Level-4 result is the only kind of output that would justify the
  distribution fight in section C, and it is the only kind the project has never once produced. Those
  two facts should be weighed together, not separately.

---

## F. Alignment check: physics versus process over the last 90 days

Counted by classifying each of the **34 active commit days** by what that day's commits did.

| Category | Days | Share | Examples |
|---|---|---|---|
| Physics-dominant | 19 | 56 percent | 06-16 to 06-22 (HYP-027 MERA), 06-26 to 07-04 (OPE, Potts), 07-16, 07-19, 08-10, 08-11 (C_TTT ladder, Yang-Lee), 08-23, 08-24, 09-09 |
| Process-dominant | 10 | 29 percent | 06-24 outreach, 06-25 scan, 07-20 credentials, 07-23 and 07-27 scans, 08-06 docs audit, 08-07 PRD submission, 08-17 audit plus rejection, 09-04 code review, 09-06 plan and Zenodo rebuild |
| Mixed | 5 | 15 percent | 07-14, 07-15, 08-09, 09-07, 09-08 |

Splitting the mixed days evenly gives **roughly 63 percent physics, 37 percent process**. That is a
healthier ratio than the recent narrative suggests, and it deserves saying plainly rather than being
buried: the project is not mostly paperwork.

Three qualifications that change how to read it:

1. **Output character has shifted hard.** Since SIM-071 on 2026-08-11, 34 days ago, there has been
   **no positive result of any kind**. SIM-072 is a retraction, 073 indeterminate, 074 a voiding of
   073, 075 VOID, 076 VOID, 077 a registered negative, 078 stopped at a failed gate. Every one of
   those is correctly executed work. None of them adds a finding.
2. **Story and correction consumed the largest single block.** 12,697 words across
   `docs/story/*.md` (`wc -w`), essentially all written on 2026-09-07 and 09-08, plus the Zenodo v5
   rebuild, review and publish. That is defensible work and it was Jon's explicit decision in the plan
   of record. It is also why 08-24 to 09-07 produced zero experiments.
3. **The narrative record has a hole.** `research/RESEARCH-LOG.md` ends at 2026-08-17 and does not
   contain SIM-073 through 078. That is process debt created by prioritizing physics, which is the
   opposite of the usual complaint, and it should be paid down in one sitting rather than left.

---

## What this section did not verify

Named explicitly so nobody quotes it as established.

- **SciPost account state.** Reported silent since 2026-04-30 from internal notes only. Not checked
  against the SciPost site this session; their guidelines pages returned an access-denied
  interstitial to automated fetches. **Check it manually before any estimate in section C.2 is
  acted on.** This is exactly the class of claim the 2026-08-12 miss was made of.
- **Whether the APS desk rejection blocks PRResearch and PRB.** The wording "APS will not consider
  this manuscript further" is quoted from `NEXT-SESSION.md` and `RESEARCH-LOG.md`. Whether it binds a
  substantially rewritten manuscript is a question for APS, not for a reading of the sentence.
- **Attribution of RunPod spend.** The 9.37 USD figure is all pods billed on 2026-09-07 to 09-09 on
  the account. The account serves other projects. Only `fiip7fruevt6e3` at 0.3213 USD is provably
  this project's.
- **Whether chi=128 satisfies G3 above L=24.** Never evaluated. It is the hinge between a 10 USD
  experiment and an unaffordable one, and it can be settled in one local run at L=32.
- **Wall clock for SIM-067 through SIM-071.** No runtime field exists on any of those records.
- **Jon's actual hours.** Nowhere in the repository. Every Jon-hour figure in section C is ESTIMATE.
