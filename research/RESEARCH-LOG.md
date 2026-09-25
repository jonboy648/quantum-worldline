# Quantum Worldline — Research Log

**Purpose.** The unlimited, version-controlled narrative record of the project: scans, experiments, verdicts, and dead-ends, in chronological order. This file is NOT loaded into the agent context every session (unlike `~/.claude/.../memory/MEMORY.md`, which is a capped one-line-per-topic *index*). Detail lives here and in `research/data/`; the memory index only points.

**How the records relate:**
- `memory/MEMORY.md` — capped table of contents (≤24.4 KB, hardcoded). One line per topic → pointer.
- `memory/<topic>.md` — uncapped per-topic memory files (durable facts, why/how-to-apply).
- `research/RESEARCH-LOG.md` — **this file**: the long chronological narrative (no cap).
- `research/digests/YYYY-MM-DD-*.md` — per-scan digests.
- `research/data/{papers,hardware,simulations,hypotheses,builds}/` — structured JSON + scripts.

**The four published anchors — CORRECTED 2026-08-17. Read the status text, not the headline number: two of the four have been superseded by the project's own follow-up work.** (Paper / Zenodo concept DOI **10.5281/zenodo.19660302**, which always resolves to the current version; v4 = 10.5281/zenodo.21381474, published 2026-07-15. The version DOI 19661227 that stood here pointed at v3 and is stale.)
- **Force exponent α** — ~~F(dr) ∝ dr^−3.92, stress-tensor exchange; three independent measurements converge (24q exact 3.92, 16q exact 3.97, 16q χ=3 MERA 4.07)~~ **WITHDRAWN 2026-08-17** (`SIM-2026-072`; audit D-2/D-3). The published fit placed **95.8% of its least-squares weight on the single point dr=2** and returned that point's local slope (4.2315) rather than a property of the profile; changing only the error model and **discarding no data** gives 2.82 (relative-error) or 2.89 (log-space OLS). **Corrected measurement: α = 2.6 ± 0.2** — the intermediate-separation plateau, stable across all three datasets and the maximum-to-minimum span of 15 defensible estimator × window choices — **with the exchange channel OPEN**: 2Δ_T = 4 (stress tensor) and 2Δ_ε = 2 (scalar) both sit outside the plateau band. The three "independent" evaluations share one observable, one operator, one window and one fitting routine, and move together under the same systematic (3.92→2.56, 3.97→2.75, 4.07→2.63): one measurement, not three.
- **Transport** — T = (π/2)·l_AdS: **T = 2.23888 vs 2.266, residual −1.21% at N=16** (dt=1e−3, `SIM-2026-025`), −2.78% at N=12. **The 0.72% that stood here was a dt=0.05 time-grid artifact, retracted by ERRATA E2** — do not quote it anywhere. Two live objections to the *geometric* reading (audit): the transport script never applies a MERA (`holographic_transport_16q.py:347` prints "Skipping full MERA bulk computation", D-12), and Wang-He's t_trans = π is ℓ-independent by their own statement, so the l_AdS in the comparison is supplied entirely by the 1/ln 2 = 1.4427 convention (D-1 resolution box).
- **χ=3 method** — ALM+projection 2-phase; correct power-law C(r)~sin(πr/8)^−1/4 recovered at 8q; energy error 1.12% at 8q and 3.33% at 24q, where single-phase collapses. **Stands** (the best-documented headline in the program). The separate claim that the 3.33% floor is an expressibility ceiling "regardless of optimizer" does **not** — it repeats verbatim the inference ERRATA D5 retracted (audit CLM-039).
- **Effective mass** — m_eff = 0.693 vs MERA 0.670 (3.5%). The numbers reproduce, but **ERRATA E4** corrects the derivation text (AdS₃ convention Δ(Δ−2); 0.693 = ln 2 = 1/l_AdS *exactly*), so the comparison reduces algebraically to ξ_2pt ≈ l_AdS² — one datum presented as two agreeing quantities (audit CLM-016). The same model on the project's better 24q exact dataset gives m_eff = 2.29 (**+230%**).

---

## Chronological log

(**Layout, stated accurately as of 2026-08-17:** the first block below — the 2026-06-08 → 06-16 `###` entries — is ordered *newest first*; from the `## 2026-06-17` entry onward the file runs **oldest → newest**, so the most recent work is at the END of the file. New entries append at the bottom. Older history is distributed across `memory/` topic files and `research/digests/`; this log begins as the consolidated home from 2026-06-08 forward.)

### 2026-06-16 (later) — HYP-027: proper Koo-Saleur stress-tensor construction → exact-diag obstruction PROVEN

Pushed past the premature "exact-diag ceiling" call with the actual Zou-Milsted-Vidal / Koo-Saleur
method (Milsted-Vidal arXiv:1706.01436), per user direction. Two more sims:
- **SIM-2026-034** — Koo-Saleur energy-density channel O_j=h_j−⟨h_j⟩. Failed: ε-contaminated, and a
  degenerate-`eigsh`-basis broke the momentum readout (`T_found=False`). Diagnosed, not rationalized.
- **SIM-2026-035** — momentum-resolved, fixed: block-diagonalizes H + translation operator,
  **correctly identifies the |spin|=2 stress-tensor state with Δ_T = 2.0000 exactly at BOTH the Ising
  and tricritical points.** The T-identification is now rigorous and correct.
- **The genuine obstruction (proven, not assumed):** measuring a force vs distance needs a *localized*
  probe, but localizing a pure momentum-2 (Δ=2) excitation on a finite chain necessarily mixes in the
  lighter primaries — a spatially-localized packet is a superposition across the conformal tower. So
  the clean Δ_T=2 channel and spatial localization are **mutually exclusive at finite N**
  (uncertainty-principle obstruction). Ising control α collapses to ~1.7, TCI ~1.3. The published α≈4
  survives only because its specific boundary operator (0.635 X-pair) is *tuned* to suppress that
  contamination at the Ising point — a tuning that does not transfer to TCI.
- **Verdict, now rigorously earned:** the universality question cannot be settled by exact diag at N≤16,
  for a structural reason. The χ≥3 multicritical MERA (stage 2) is genuinely required — it projects onto
  scaling operators *without* spatial localization, dissolving the obstruction. HYP-027 stays OPEN.
- Process note: I had earlier called this an "exact-diag ceiling" after only a local-operator scan; that
  was premature. Doing the real ZMV construction and watching it hit the *actual physical* wall is the
  difference between a rationalized punt and an earned conclusion. (See [[feedback-baseline-provenance]] —
  same lesson family: do the rigorous thing before concluding "can't.") Files: SIM-032..035.

### 2026-06-16 — HYP-027 stage 1b: exact-diag ceiling reached; companion note finalized

**Universality of α≈4 — verdict: still OPEN, now with the exact-diag route exhausted and the path forward pinned to stage-2 MERA.** Two rigorous attacks at N=16 on the O'Brien-Fendley chain (TCI confirmed at c=0.726, SIM-032):
- **SIM-2026-033** — symmetry-resolved operator-basis scan over the Z2-even sector. Selects the operator that reproduces the published Ising α by a hard gate; that operator (energy-density, dE_single≈3.5) gives Ising α=3.91–3.97 ✓ but TCI α=1.33.
- **SIM-2026-033b** — Gram-Schmidt removal of the K lightest primaries from the excitation, measuring the residual (stress-tensor-ward) force. Ising control holds (α≈3.91 for K=0..2); TCI rises only 1.32→1.63 under projection, never reaching [3.6,4.4].
- **Root cause (diagnosed via the gap structure, not guessed):** the c=7/10 spectrum is dense (gaps 0.61/0.87/1.14 vs Ising 0.38/1.14/1.52), so a fixed *local* operator couples dominantly to the lightest TCI primary and exact diagonalization at N=16 cannot separate the stress-tensor channel by energy. Honest exact-diag ceiling — **not** a refutation, **not** a confirmation. The mechanism re-validated a *third* time (Ising control hit 3.97 across SIM-032/033/033b).
- **Resolution requires stage 2:** the χ≥3 multicritical MERA at the TCI point, which projects onto scaling operators directly. HYP-027 stays TESTABLE_NEAR_TERM. Note: this is exactly the campaign flagged as ~9000s/seed and possibly needing χ>3.

**Companion note finalized** — `research/note-synge-force-blind.tex` (the SIM-031 "distance is force-blind" result, item #4). Drafted by a background agent that was killed mid-cleanup; on resume the .tex was verified intact (clean 5-page build, all anchor numbers present) and its 4 honest `% TODO` citation markers were resolved against the live arXiv API: Ansel 2405.02380 = "Emergent gravity from the correlation of spin-½ systems coupled with a scalar field" (gr-qc; the Synge-map application is ours), Sahay/Lukin/Cotler 2401.13595 title corrected verbatim, Wang-He + Zenodo titles confirmed. Zero TODOs, zero LaTeX errors. Ready for arXiv/SciPost companion submission.

### 2026-06-08 — SIM-2026-032 stage 1: TCI universality test (gates pass, control bullseye, TCI inconclusive pending operator calibration)

HYP-027 executed via the **O'Brien-Fendley chain** (design amendment from ANNNI — OF has exactly
documented TCI coordinates λ₃/λ_I=0.856, arXiv:1712.06662, and its λ₃=0 end IS our published Ising
anchor, giving a built-in control). Exact 16q:
- **c-gates PASS**: c=0.502 (Ising end, theory 0.5), c=0.726 (TCI point, theory 0.7).
- **Ising control reproduces the published α: 3.975±0.145 vs published 3.97±0.15** — independent
  re-validation in a doubled-normalization Hamiltonian. Two pipeline lessons captured on the way
  (Gate B caught both): bare-Z excitation gives identically zero force (unitary conjugation);
  a 2×-anchor single-energy subtraction on OBC leaves an ε-channel residue (α≈2.2-2.4) — the
  published per-site dE_single subtraction is what isolates the stress-tensor channel.
- **TCI point: α=1.33±0.09 — INCONCLUSIVE** (neither universal 4.0 nor primary-tracking 0.4).
  Interpretation: the Ising-tuned bp_op coefficients are an uncalibrated primary mixture at TCI.
  **Stage 1b queued: re-derive the boundary-primary coefficients AT the TCI point, rerun.**
- Files: `sim032_tci_force_stage1.py`, `SIM-2026-032.json`, note in HYP-2026-027.json.
Also this block: ADAPT robust-basin test launched (background); QuEra Gemini collaboration inquiry
DRAFTED (research/outreach-emails.md, NOT sent, awaiting user approval).

### 2026-06-08 — SIM-2026-031: HYP-026 SUPPORTED (Synge distance is force-blind) + HYP-016 refresh + catalogue dedup

**SIM-2026-031** executed HYP-026's pre-registered three-tier test same-day:
- Tier 1 (synthetic C=r^(−1/4), registered primary): monotone, κ=0.2500 exactly.
- Tier 2 (exact 16q critical-TFIM connected ZZ — upgrade over the registered 24q regen, which is an
  ~8h eigsh adding nothing to the shape question): monotone, **κ_chord=0.2429 ≈ 2Δ_σ, not α≈4**.
- Tier 3 (SIM-011 pathological proxy as control): non-monotone + κ garbage, exactly as predicted —
  the old data was the problem, not the map.
- **Verdict: SUPPORTED** (both registered gates pass; R²=0.95). A two-point-correlator distance carries
  Δ_σ=1/8; the force carries Δ_T=2 — *distance and force are owned by different operators*. Closes the
  correlator→geometry thread; formalizes why HYP-012 (CMI→force) and HYP-014/022 (Crofton) failed for
  structurally different reasons. Wording correction recorded: d=ε√(½ln r) is √log, not linear.
- Second SUPPORTED new result of the autonomous phase (after the normalization no-go theorem).
- Files: `sim031_synge_force_blindness.py`, `SIM-2026-031.json`; write-back in HYP-2026-026.json.

**HYP-016 FT-MERA estimate refreshed** (pending 3 scans, done by background agent):
old 1839 atoms/8 min → **LOW 75 atoms** (demonstrated qLDPC rates: QuEra 4.67:1, ion 4.5:1) /
**HIGH ~1500** (20× for magic states+routing); wall 15–95 min at 10k shots. **Headline: Quantinuum
Sol (2027 roadmap) runs the chi=3 16q transport circuit BARE-METAL** — ~4–5k ops vs 10k budget,
~80–84% circuit fidelity, dr=1..2 force-existence solid (full α fit borderline at 99.98%).
Biggest unknown: chi=3 top-tensor non-Clifford content has never been mapped to a logical patch
(that single step is the whole LOW→HIGH spread). File: `research/data/hardware/FT-MERA-ESTIMATE-2026-06-08.md`.

**Catalogue dedup resolved non-destructively:** 8 redundant paper records → alias stubs
(`alias_of` field; canonicals 044/111/088/075/100; originals preserved in git history).
**Docs hardened:** CLAUDE.md (paths, real skill names, MCP query-blind warning, catalogue rules)
and weekly-scan SKILL.md (5 standing rules injected into every future teammate prompt).

### 2026-06-08 — Weekly Scan #9 (full team run: literature → theory → computation)

Team qw-scan (3 opus tier leads + their specialist subagents), post-audit. Digest:
`research/digests/2026-06-08-team-scan.md`. **No contradictions to any anchor.**
- Scan-8 backlog catalogued (PAPER-101→110, HW-055→060) + fresh sweep (PAPER-111→114, HW-061→063).
- **HYP-2026-026** (NEEDS_REFINEMENT): Synge world-function distance is geometric but force-blind
  (Δ_σ=1/8 ≠ Δ_T=2) — formalizes why correlator→force and Crofton routes failed differently.
- **HYP-2026-027** (TESTABLE_NEAR_TERM): tricritical Ising c=7/10 should also give α≈4 — second
  universality data point via the ANNNI route; needs a multicritical MERA campaign.
- HYP-021 orphan gated (NEEDS_REFINEMENT; audit item closed). No TESTABLE_NOW → compute tier idle by design.
- **ACTIONABLE: QuEra Gemini 260q/99.2% collaboration program (HW-062)** — second documented non-QCUP
  hardware route (with Azure credits). User-decision item.
- Lead verification caught 2 re-catalogues (111≈073≈087, 114≈044≈021≈078): dupe map now 5 sets / 8
  redundant files. New standing rules in orchestrator memory: dedup-grep before ID assignment; arXiv
  export API via WebFetch (MCP search is query-blind).

### 2026-06-08 — FULL-PROJECT AUDIT (13-agent workflow, all findings adversarially verified)

User asked: "review the entire project... make sure we haven't missed anything and it all adds up."
Six auditors (anchors / hypothesis ledger / simulation chain / task-95 record / open threads / repo
hygiene) + adversarial verifiers + my own hand-checks. **Zero false alarms across all verified findings.**

**Verdict: the core science adds up — every headline number traces to its data file at quoted
precision — but the record-keeping had materially decayed.** Key results (full list: `research/ERRATA.md`):
- **E1:** published "l_AdS deviation 0.76%" is wrong → 0.71% (hand-verified).
- **E2 (most consequential):** published "0.72% at N=16" transport residual is a dt=0.05 grid artifact —
  our own SIM-2026-025 (dt=1e-3, 2026-05-16, post-publication) gives **−1.205% converged**; anchor survives
  qualitatively (residual shrinks with N) but precision claim superseded; no errata existed until today.
  Same run REFUTED HYP-023 while the memory table still said "needs re-run."
- **E3:** paper S1 penalty row (4.02%, P=0.000) untraceable — record lost on RunPod; ID SIM-2026-007 double-assigned.
- **E4:** §IV.B m_eff derivation text uses a convention that contradicts its own data records.
- **D4:** task #95's "33 vs 36 = wash" killer was INVERTED — 451 IS the real compile of the QCUP circuit,
  36 was an estimate → **ADAPT's 33-ZZPhase advantage is real (~13.7×)**; no-go now rests on fragile basin,
  not-a-MERA framing, and the QCUP hold.
- Ledger decay: 8 tested hypotheses lacked verdict write-backs (HYP-017/023/024 corrected today, JSONs +
  memory); HYP-021 orphaned (never gated); SIM ID collisions (011, 007); schema drift (9/36 SIMs, 16/25 HYPs pass).
- Durability: ~27 days of research record uncommitted; published paper source not in version control;
  `.mcp.json` contains a hardcoded auth token on the public branch (MUST NOT be committed as-is); 3 byte-identical
  paper-record dupes; ESMFold (foreign project) artifacts inside `research/data/builds/`.

**Fixes applied same day:** ERRATA.md created; HYP-017→SHELVED and HYP-024→NOT_ESTABLISHED written into JSONs;
MEMORY table rows 017/021/023 corrected + high-water SIM-030 + "SIM-028 not saved" wording fixed; killer-1
inversion corrected in memory, digest, and this log; transport memory annotated with SIM-025 supersession.
**Still pending user sign-off:** commit plan for the uncommitted record (excluding .mcp.json), paper-dupe
deletion, paper source into version control, HYP-021 gate-or-archive, v5 text corrections.

### 2026-06-08 — Task #95 RESOLVED: ADAPT-VQE settles the cheap-circuit question (QCUP stays closed)

**Question:** is chi=3 MERA's 451-ZZPhase cost fundamental, or can a cheaper circuit prepare the critical-TFIM ground state *and* carry the α≈4 holographic force?

**Result:** ADAPT-VQE (pool {iY_j, iY_jZ_{j+1}, iZ_jY_{j+1}}, greedy gradient growth from |+⟩^L, full re-opt each step) reached **faithful at step 25** on L=8: GS-overlap 0.9998, force RMSE 0.0045 (dr∈{1,2,3}), energy rel err 0.014%. This **proves the #92/#94 brickwork plateau (overlap stuck ~0.567) was an optimizer artifact, not fundamental cost** — the genuinely new physics fact of the day.

**But the "6× cheaper → QCUP reopens" headline was REFUTED** by an 8-agent adversarial verification + scaling run:
1. *Wrong baseline:* real compile of the 25-op ansatz = **33 ZZPhase** (GreedyPauliSimp; routes 50/42/48/33), but the 451 was a 16q full-MERA strawman — the MERA QCUP would actually run is **~36 ZZPhase**. 33 vs 36 = wash.
2. *Noise premise unproven:* consistent gate-depolarizing at Helios p2q=7.9e-4 keeps 99% of the force at 33 gates — but **also 90% at 451 gates**; the model never reproduces the recalled ~30% chi=3 kill (must be SPAM/readout/idle, unmodeled). Shot noise fine (dr=1 SNR≈19 @10k shots).
3. *Fragile basin:* 1% angle jitter inflates force RMSE ~17× (fails 0.02 gate in 87–96% of samples); survives only ≤0.1% precision. dr=1 sign robust in 100% of perturbations.
4. *Scaling kills the win:* faithful cost **L=8→25 ops, L=10→35 ops = +5 two-qubit gates/site (p=1.51)**. L=8 was a small-system artifact. (L=12 leg OOM-killed at step 36/n_2q=36, tracking the extrapolated ~45; would confirm p≈1.5, not change it.)

Also real: out-of-sample dr=4 force matches to 4.2% (force never entered the optimizer loss) — the α≈4 signal in the ADAPT state is genuine physics, not 3-point overfit.

**Files of record:** `research/data/simulations/adapt_vqe_force.py`, `research/data/builds/adapt_vqe_results.json`, `research/data/builds/verify_adapt_*.json` (compile/force-robust/noise/shotnoise/scaling). Memory: `adapt_vqe_cheap_circuit.md`. Verification workflow wf_c1affae1-22b.

**Standing conclusion:** paper v4's three α≈4 measurements unaffected; no hardware experiment currently worth money; the one revival condition is a circuit that *both* scales mildly *and* beats a re-compiled real MERA at matched L under a noise model that explains the chi=3 floor.

### 2026-06-08 — Weekly Scan #8 (run by hand: paper-search MCP is query-blind)

Digest: `research/digests/2026-06-08-weekly-scan.md`. **No contradictions to α≈4 / T=2.250 / chi=3.**
- Method note: the arXiv MCP endpoint now ignores query strings entirely (returns the latest-submission firehose for any keywords; verified with disjoint queries returning identical results). Scan run via the arXiv export API through WebFetch (`abs:` field queries honored). New failure mode vs the earlier network hangs.
- Nearest paper to #95: **2605.21447** (IBM — quantum-annealed state as fixed classical-shadow boundary resource + *classical* MERA optimized on top; TFIM N=12/24 at criticality; >5×/>2× energy improvement at fixed 200-gate depth; 10⁵–10⁶ snapshots). **Orthogonal to #95** — their quantum circuit is fixed and shallow; doesn't touch the "can a quantum circuit prep the critical GS cheaply" no-go.
- Anchor 2501.03084 (Wang-He hologron/transport) still SOTA, unsuperseded.
- Hardware: ion qLDPC breakeven (2606.06455, 4L/18P, 9× better), Atom Computing toric 90 rounds (2606.04079), Yb 99.89% readout (2605.24175). Standing action: refresh HYP-016 FT-MERA cost estimate.
- The experimental emergent-gravity-on-simulator niche (HYP-017's target) remains unoccupied.

### 2026-06-08 — Exploratory off-paper-path pass

- **Azure Quantum Credits: $500 free per provider (IonQ, Quantinuum, …), no academic-affiliation gate mentioned** — the cleanest documented end-run around the affiliation walls (arXiv endorsement, SciPost account, IBM credits "tenure-track only", QCUP HQC). Memory: `hardware_access_routes.md`. Only matters once a circuit worth running exists (#95: currently none).
- IBM Quantum Credits: independent researchers ineligible as written.
- New theory lineage to WATCH: Raasakka 2505.07102 + 2507.16346 (emergent gravity from compositional QFT in triangulated spacetime / QFT vector model) — different tensor-network→gravity route than our MERA/AdS-CFT; possible future math-bridge target, not near-term.

### 2026-06-08 — Records architecture change

MEMORY.md (capped 24.4 KB, hardcoded) was overflowing from holding full findings. Decision (user-approved): MEMORY.md becomes a true one-line-per-topic index; detail lives in uncapped `memory/<topic>.md` files; **this RESEARCH-LOG.md is the new unlimited chronological narrative** (version-controlled, in-repo). Index restructure deferred until after the 2026-06-08 full-project audit so corrections fold in once.


---

## 2026-06-17 — HYP-027 stage-2: the product-state collapse was an OPTIMIZER artifact (autograd fix)

Continuation of the chi=3 TCI MERA thread (ERRATA D5). Goal: settle whether α=4 is universal at the
tricritical-Ising (c=7/10) point by getting a faithful chi=3 MERA of the O'Brien-Fendley GS, then a
Koo-Saleur force read-out.

**SIM-037 (cheap seed) — FAILED, as ERRATA D5 hedged.** Init-scale sweep + a one-round soft
entanglement penalty (loss=⟨H⟩−0.5·S_half) did NOT escape the collapse: best S_half=0.0001 vs exact
0.1795. Diagnosis: the penalty's gradient ≈ 0 *at* the product state, so it can't push uphill out of
the basin. Killed at ~4h50m after a >2h plateau. Recorded; narrowed the path to a structured seed.

**Probe (overlap-seed, route A) — also FAILED, same flaw.** Maximizing |⟨ψ_exact|ψ_MERA⟩|² stalled:
overlap crawled 0.010→0.019 over 4 iterations then L-BFGS gave up. The |⟨t|m⟩|² gradient scales WITH
⟨t|m⟩, so it vanishes where we start (far from target) — the identical vanishing-gradient pathology.
KEY OBSERVATION from the probe: the random MERA init is NOT a product state (S_init=1.21 > S_exact=0.18);
the ENERGY optimizer DRIVES the state to product during descent. So the collapse is a landscape
attractor reached *during* optimization, not a starting condition.

**Root cause (all of SIM-036/037/038): finite-difference gradients on 1246 angles.** ~1247 state
rebuilds per gradient → starved optimizer → 69s/iteration → collapse into a near-product local min with
passable energy (0.34%) but wrong entanglement.

**Route C = autograd (exact gradients).** Kept the EXACT validated MERA architecture (8-site, 3-layer,
chi=3, U(4)/U(9)) and swapped only the gradient engine. Three plumbing fixes, each verified vs
finite-difference to ~1e-10 before committing: (1) Cayley transform U=(I+iA)⁻¹(I−iA) replaces scipy.expm
(autograd has no expm VJP; Cayley is unitary to 2e-16 and differentiable); (2) vdot→sum(conj·); (3) the
sparse Hamiltonian H@sv as an autograd primitive with VJP g→Hᵀg (the correct complex-linear convention —
Hᵀ, not H†). Installed quimb (DMRG attempt NaN'd on its 2-site SVD; abandoned — the exact GS at N=16 is a
better target anyway) and autograd. → SIM-2026-039.

**SIM-039 first run (single-descent L-BFGS-B): ~500× faster (0.13s/iter vs 69s) and entanglement does
NOT collapse** — the Ising control descended S 0.66→0.48 (toward exact 0.42) while energy improved. This
CONFIRMS the SIM-036 "chi=3 insufficient" verdict was an optimizer artifact (ERRATA D5 vindicated). BUT
plain single-descent plateaued at rel=0.60% (published protocol reached ~0.15%), so it under-converges
vs ALM. Killed and upgraded to a **multi-round restart loop with perturbation kicks** (the SIM-015c/d
ALM-style protocol) — running now (Ising control then TCI). Decision tree: control validates + TCI clears
gate (rel<0.3%, ov>0.95, S_ratio>0.9) → chi=3 sufficient, proceed to Koo-Saleur force; control validates
+ TCI still collapses S → chi=4 FINALLY earned (optimizer ruled out by exact gradients). Files: SIM-037/039
JSON, sim037/sim038/sim039 scripts, ERRATA D5 follow-up.

**SIM-039 RESULT (autograd, projected-energy objective) — HYP-027 representability RESOLVED.**
After the autograd machinery + a second bug fix (was minimizing RAW energy on a state only ~60% Z2-even;
switched to Z2-PROJECTED energy → Ising control 0.60%→0.18%), both points were optimized with a validated
control. FINAL: Ising control rel 0.183% / ov 0.994 / S_ratio 1.040 → GATE PASS (machinery validated);
TCI (λ3=0.856) rel 0.088% / ov 0.9943 / S_half 0.1336 vs 0.1795 → S_ratio 0.745, gate fail on entanglement
only. Two findings: (1) the SIM-036 product collapse (S=0.0002) was 100% an optimizer+objective artifact —
exact gradients take S 0.0002→0.1336 (~670×); ERRATA D5 fully vindicated end-to-end with a passing control.
(2) chi=3 is energy/overlap-faithful at the TCI point but captures only ~74.5% of the half-chain entanglement
entropy (the c=7/10 Schmidt tail exceeds bond 3), so chi=4 is NOW earned — on a sound, control-validated
footing (optimizer ruled out), unlike the retracted SIM-036 chi-4 call. Corrected the auto-generated verdict
("collapses" → "reaches 74.5% faithfulness"; this is NOT a collapse). NEXT: chi=4 MERA at TCI (same autograd
code, bond 3→4), then the stress-tensor force read-out (the α-universality answer; note a CLEAN read-out may
further need a scale-invariant MERA per SIM-035's hand-off — to be assessed after chi=4). Files: SIM-039 JSON,
sim039_autograd_mera.py, ERRATA D5 resolution.

**SIM-040 RESULT (chi=4 autograd MERA) — HYP-027 representability FULLY CLOSED.**
CHI-generalized the SIM-039 machinery (single-axis contraction, 3->CHI/9->S2D/18->N_TOP; validated:
norm, isometry, grad-vs-FD ~1e-10 at chi=4; 3360 params). Ising control: rel 0.0016% / ov 0.9999 /
S_ratio 0.998 -> GATE PASS (near-exact, validates machinery). TCI (λ3=0.856): rel 0.0061% / ov 0.9998 /
S_half 0.1760 vs 0.1795 -> S_ratio 0.980 -> GATE PASS. The S_ratio jump 0.745 (chi=3) -> 0.980 (chi=4)
confirms chi=3's 26% entanglement shortfall was a real bond-dimension effect. A faithful chi=4 TCI
ground state is now on disk. NEXT for the alpha-universality NUMBER: the force read-out — assessed
honestly against SIM-035, a faithful state does NOT dissolve the finite-N localization obstruction
(isolating Delta_T=2 needs a tuned boundary op [Ising-only] or the scale-invariant scaling
superoperator). So the clean alpha read-out is a SEPARATE build (scale-invariant critical MERA +
ascending superoperator), for which chi=4 confirms the bond budget is ample (chi<=4 suffices).
HYP-027 status: representability RESOLVED; alpha-universality OPEN, path identified (scale-inv MERA).
Files: SIM-040 JSON, sim040_chi4_tci_mera.py.

## 2026-06-18 — HYP-027 alpha-universality: scale-invariant MERA build (scouts + torch verified)

User authorized the next build (scale-invariant MERA + scaling superoperator -> read the dimension
spectrum {Delta}; if Delta_T=2 appears, that IS the universal-stress-tensor answer, no force fit needed).
Deployed 2 parallel scout agents (math-bridge + general-purpose); their findings RESHAPED the plan:
- METHOD SCOUT (Evenbly-Vidal 0707.1454 / Pfeifer-Evenbly-Vidal 0810.0580): the scaling superoperator's
  eigenvalues give Delta = -log_b(lambda) (b=2 binary, b=3 ternary). REQUIRES translation invariance / PBC
  -- our OBC chi=4 state is the WRONG object; must re-optimize a scale-invariant (u,w) pair on the PERIODIC
  TCI Hamiltonian (same bulk physics). Gate on c = 3(S(rho)-S(rho^1)) ~ 0.70. Delta_T=2 is high in the
  tower, converges slowly -> may need chi 6-8. Ternary gives a cleaner single-site superoperator.
- QUIMB SCOUT: quimb builds scale-invariant MERA (one u/one w, dangle=True) and ties tensors across layers
  (TNOptimizer shared_tags), but autograd CANNOT optimize it (no QR/SVD VJP). quimb has NO scaling-
  superoperator tooling -> hand-roll it regardless.
- DECISION (user): install torch -> use quimb's TNOptimizer. VERIFIED torch 2.12.1+cpu: QR & SVD grads work;
  quimb+torch+shared_tags optimizes a scale-invariant MERA END-TO-END (fixes needed: cast H terms to complex,
  take .real of the loss for torch backprop). Ising smoke: E/site -0.499 vs exact -0.532 (6%, 100 L-BFGS
  steps, bond 2) -- machinery SOUND, convergence needs more iters + bond. Next: write the real build (periodic
  TCI H, bond 4-8, c-gate, hand-rolled ascending superoperator -> {Delta}), Ising as built-in control.

**quimb route hit a contraction wall (2026-06-18).** After torch unblocked the gradients, building the
scale-invariant MERA in quimb surfaced two real obstructions: (1) quimb's uniform shared-tensor MERA
needs phys_dim==chi (wrong for a spin-1/2 chain) -> required a fixed bottom layer (2->chi) + uniform
shared bulk (chi->chi), tagged BULK_U/BULK_W so shared_tags ties only the bulk. That construction BUILDS
fine (verified: 8 bottom + 7 bulk tensors of each type, correct shapes). BUT (2) a SINGLE
`compute_local_expectation(max_bond=-1)` energy evaluation DIES SILENTLY (exit 0, no result, no
traceback) on this 30-tensor chi=4 MERA -- diagnostic isolated the death to the single contraction, NOT
the optimization loop, with quimb warning "contraction tree is not a compressed one." Exact MERA
density-matrix contraction is too wide for memory here; the __main__ guard did not help (it's not the mp
storm, it's the contraction). CHECKPOINT DECISION (pre-set): stop patching quimb rather than rabbit-hole
into custom contraction paths / silent-worker debugging. The scale-invariant alpha-universality build
needs either Evenbly's purpose-built reference code (tensors.net/mera, the method scout's original rec --
its hand-tuned MERA contraction avoids quimb's general-purpose blowup) OR a from-scratch numpy
scale-invariant MERA. NOT a quimb problem worth more hours. Representability result (SIM-039/040) stands
fully; this is only the alpha-readout vehicle. torch 2.12.1+cpu now installed (gradients verified).

**Superoperator blocker identified (2026-06-18).** Per user direction switched execution to RunPod
(never local) and chose to retry quimb+torch there. RunPod infra readied: the old GraphQL spin script
is obsolete (403); RunPod migrated to REST at rest.runpod.io/v1 (key rpa_EQKL... is VALID and rotated
from the old rpa_TX2CC..., GET /v1/pods -> 200 []). Pod creation = POST /v1/pods (imageName required;
cpuFlavorIds incl. cpu5m memory-optimized; cloudType SECURE/COMMUNITY; containerDiskInGb; env; ports).
BUT before deploying, a cheap LOCAL structural test caught a real bug: the hand-rolled scaling
superoperator (_descend_channel in sim041) is STRUCTURALLY WRONG -- its leading eigenvalue is 1.0817,
not 1.0; a valid scaling superoperator MUST have the identity operator as an eigenoperator with
lambda=1 (Delta=0). The _descend_channel dropped the disentangler ("traces to identity on the
single-site channel") -- exactly the hand-wave the method scout warned against. So deploying to RunPod
now would burn spend on a pipeline whose final step is broken. BLOCKER = correct binary scaling
superoperator (Evenbly-Vidal Fig. 9, leg-by-leg), NOT compute. Options to fix: (a) browser-extract
Evenbly's embedded tensors.net code (only fetch route untried -- WebFetch can't see the inline code,
GitHub 404'd), (b) derive+validate the binary superoperator by hand against the lambda=1 + Ising
{0,1/8,1} gate. The chi=4 faithful-state result (SIM-039/040) is UNAFFECTED and stands. Clean
checkpoint: representability DONE; alpha-readout blocked on superoperator correctness (a math bug, not
infra). torch 2.12.1+cpu + quimb verified to optimize given enough RAM (the local wall was memory).

**Superoperator FIXED + validation harness + deploy-ready (2026-06-18, ultracode).** Resolved the
structural bug. The broken v0 put the operator on the COARSE leg and descended with two identical
("L==R") terms (a no-op average) and dropped the disentangler -> lambda_max=1.0817 (FAIL: identity must
be lambda=1). CORRECT one-site binary ASCENDING superoperator (validate_superop.py, candidate v1):
operator on a FINE lower leg, ascend to the coarse leg, TWO genuinely-distinct terms (O on left lower
leg a [trace b] vs right lower leg b [trace a]), averaged:
  AL = einsum('abp,ac,cbq->pq', w, O, wc) ; AR = einsum('abp,bd,adq->pq', w, O, wc) ; S=0.5(AL+AR).
When O=I each reduces to (w_dag w)=I by isometry -> lambda=1. PASSES GATE A (identity->1) on random
isometric (u,w), all seeds; the broken v0 is kept as a negative control that FAILS. The disentangler
correctly drops for the ONE-SITE channel (u u_dag=I when O doesn't straddle u); it enters only for
two-site ops. GATE A is necessary-not-sufficient; GATE B (converged-Ising spectrum must give {0,1/8,1})
is built into sim041.main() and runs on the converged Ising control before any TCI claim.
sim041_scaleinv_mera_spectrum.py now COMPLETE + SELF-CONTAINED (builds its own periodic OF Hamiltonian
+ quimb MERA + superoperator; NO sim036 dependency) and parses clean. RunPod deploy ready:
scripts/runpod_deploy_sim041.py (REST POST /v1/pods, cpu5m ~64GB high-RAM, PyTorch image, start cmd
pip-installs quimb+autograd + base64-decodes + runs sim041; ~$0.10-0.40/hr). Cross-check workflow
(wf_b7ee088b-921: 3 independent superoperator derivations -> synthesis -> adversarial verify) running to
confirm the u-treatment before deploy. NEXT: read workflow verdict; if it confirms v1 -> deploy sim041
to RunPod (Ising GATE B + TCI spectrum + Delta_T=2 hunt in one run).

**Superoperator CORRECTED via adversarial workflow + authoritative reference (2026-06-18, ultracode).**
Ran a 5-agent workflow (3 independent derivations -> synthesis -> adversarial verify, wf_b7ee088b-921)
to validate the scaling superoperator BEFORE spending RunPod compute. It caught a real error in my
candidate v1: the workflow's own synthesis proposed a "with-u one-site" fix, and its VERIFIER demolished
it (exact, rel diff 2e-16): ANY one-site superoperator (with or without u) is gauge-equivalent to a bare
isometry channel -- the disentangler is absorbable. A disentangler only survives the trace when it
STRADDLES TWO isometries, which requires the genuine binary causal cone. v1 PASSED gate A (identity->1)
only because S(I)=I is automatic for any isometric assembly -- gate A cannot distinguish the
oversimplified v1 from the correct form; only the Ising {0,1/8,1} spectrum can, and NO one-site build
produced it. Fetched the authoritative tested reference: Google TensorNetwork simple_mera.py. KEY:
the binary ascending superoperator = grad(binary_mera_energy, state); it acts on 3-SITE operators
(rho rank-6); the energy network uses 3 isometries + 2 disentanglers per term (un_l straddles iso_l/iso_c,
un_r straddles iso_c/iso_r -> u survives), averaged 0.5 left/right. Saved the EXACT leg wiring to
research/data/simulations/REFERENCE-binary-mera-superop.md. CORRECT plan: replicate that energy network
in torch, get the superoperator by AUTODIFF (zero hand-contraction bugs, Google's approach), build the
chi^6 x chi^6 (4096x4096 at chi=4) scaling superoperator via 4096 grad evals, diagonalize -> Delta =
-log_2(lambda), validate Ising {0,1/8,1}, then TCI hunt Delta_T=2. This is a REAL implementation step
(3-site grad-based superop) + needs the converged (u,w) from RunPod. SIM-041's one-site superop is
SUPERSEDED; its quimb+torch OPTIMIZATION half is still valid. Net: the alpha-readout architecture is now
CORRECT and reference-anchored; remaining = implement the 3-site grad superop + run on RunPod. Workflow
cost ~475k subagent tokens, well spent (prevented a wrong-physics RunPod run).

**CORRECT 3-site superoperator BUILT + structurally validated (2026-06-18).** Implemented
binary_mera_superop.py: replicates the Google simple_mera.py binary energy network (exact leg wiring
from REFERENCE-binary-mera-superop.md) in torch einsum, and gets the ascending scaling superoperator by
AUTODIFF (ascend = grad(energy, rho)), exactly the reference's method -> zero hand-contraction risk in
the superoperator. Operator space = 3-site = chi^6 (the earlier '268GB' was my arithmetic error; it is
chi^6=4096-dim -> a 4096x4096 = 268 MB matrix at chi=4, built in ~66s via 4096 grad evals). TWO
structural gates PASS at chi=2: (1) identity 3-site op -> eigenvalue exactly 1 (unitality); (2)
DISENTANGLER-MATTERS discriminator -- the spectrum with the real u differs from u=identity
([1,0.343,0.343,...] vs [1,0.384,0.384,...]), proving u is NOT gauge-absorbable, i.e. it genuinely
enters the binary causal cone. This is EXACTLY the property the workflow verifier proved the one-site v1
LACKED (v1's u was absorbable -> wrong). So the superoperator is now correct + reference-anchored +
cheap. REMAINING = GATE B (converged-Ising spectrum {0,1/8,1}), which needs the converged scale-invariant
(u,w) from the MERA optimization (RunPod, the local OOM job). Net status: alpha-readout machinery is
CORRECT and validated up to needing the optimized state; superoperator step is ~66s/state, trivial.
Files: binary_mera_superop.py, REFERENCE-binary-mera-superop.md, validate_superop.py (gate-A harness).

**GATE B PASSES — full alpha-readout pipeline VALIDATED end-to-end (2026-06-18).** sim042 (self-contained,
no quimb: tested Evenbly-Vidal SVD optimization + grad-based 3-site superoperator) RECOVERS the Ising CFT
spectrum from scratch at chi=2 (the minimal bond, 13s): extracted Delta = [0, 0.1055, 1.0356, 1.0864,
1.2701, ...] vs CFT [0, 1/8=0.125, 1, 9/8=1.125, ...]. Identity Delta=0 exact; Delta_sigma 0.106 vs 0.125
(~16% at chi=2, tightens with chi); Delta_eps 1.036 vs 1.0 (~4%); descendant tower present. This is the
DECISIVE physics gate (GATE B) that NO prior attempt passed (one-site v1 and the workflow builds all gave
muddy towers ~1.34). The whole chain is now correct: energy network (real/finite) -> SVD optimizer
(converges E=-4.567) -> grad superoperator (identity->1, disentangler-matters) -> Ising {0,1/8,1}. NEXT:
chi=4 Ising (sharpen dims) + chi=4 TCI (lam3=0.856) -> hunt Delta_T=2 = universal stress tensor
(alpha=2*Delta_T=4 at c=7/10) = THE universality answer. Pipeline runs locally (small per-layer network);
user wants RunPod -> deploy via runpod_deploy (adapt for sim042). Files: sim042_scaleinv_spectrum.py,
binary_mera_superop.py, test042.log.

**chi=4 Ising Gate B + matrix-free superop (2026-06-18).** The chi=4 dense superop build hit the LOCAL
memory wall (268MB matrix + torch per-call alloc died ~col 1500/4096) -- but the matrix-free
LinearOperator formulation (ARPACK needs only matvecs = one grad eval each, never the dense matrix)
runs in 2s with NO memory issue, AND is the scalable design for higher chi (chi=6 dense would be 35GB;
matrix-free is ~12MB Krylov). chi=4 Ising spectrum: [0, 0.101, 1.034, 1.084, 1.280, ...] vs CFT
[0, 1/8, 1, 9/8, ...] -- recognizably Ising (identity 0, sigma~0.1, eps~1, descendant tower), GateB
qualitatively PASS. NOTE: Delta_sigma 0.101 is slightly worse than chi=2's 0.106 -> the Hamiltonian-
padding shortcut (embed d=2 OF term in the chi-corner) + critical-tuning quality matters as much as chi
for PRECISE dims; the spectrum is correct in structure but not high-precision. Optimizer converged
superbly (E=-4.565667, dE 1e-9). NEXT (running): TCI spectrum, hunt Delta_T=2. Files: superop_linop.log,
ising_chi4_dims.npy, uw_SIM2026042_ISING.npz.

**TCI run: pipeline validated but TCI optimization did NOT reach the c=7/10 fixed point (2026-06-18).**
Ran the full chi=4 scale-invariant pipeline. ISING CONTROL: clean (E=-4.5657, dE 1e-9; spectrum
[0, 0.101, 1.034, ...] = correct Ising {0,1/8,1} structure) -> GATE B PASS, machinery validated.
TCI (lam3=0.856): OPTIMIZATION OSCILLATED (E bounced -4.11 to -4.12, dE ~2e-3, never converged --
the documented multicritical-landscape difficulty: TCI needs simultaneous tuning of 2 couplings, and
the SVD-update optimizer doesn't lock onto it). Resulting TCI spectrum:
  [0, 0.473, 0.761, 0.934, 1.242, 1.365, 1.465, 2.110, 2.140, 2.233, ...]
vs TCI CFT [0, 0.075(sigma), 0.2(eps), 0.875, 1.2, ..., 2.0(T)]. HONEST VERDICT: this does NOT match
the c=7/10 CFT -- the lowest non-zero dim is 0.473, MISSING the two lightest primaries (0.075, 0.2)
entirely. This is a QUALITATIVE failure (wrong fixed point), not a precision issue. The cluster near
2.1 ([2.11,2.14,2.23]) CANNOT be claimed as the stress tensor Delta_T=2: with the spectrum's foundation
(light primaries) wrong, a near-2 cluster is as likely artifact/wrong-tower-descendants as T. Reading
"Delta_T~2 found" off this would be a motivated false positive -- explicitly NOT claimed. CONCLUSION:
alpha-universality NOT answered; the blocker is now TCI OPTIMIZATION CONVERGENCE (reach the actual
c=7/10 fixed point), not the superoperator (correct, Ising-validated) or memory (matrix-free solved it).
Likely fixes: better critical tuning (the d=2->chi Hamiltonian-padding shortcut is crude; build the
proper bulk effective H), more sophisticated optimizer (conjugate-gradient / multiple restarts / anneal
lam3 from 0), or a proper c-gate (require c=0.70 before reading dims). Files: tci_spectrum.log,
uw_SIM2026042_TCI.npz, ising_chi4_dims.npy. Ising control is a clean, validated positive.

**TCI blocker ISOLATED to the Hamiltonian-padding shortcut (2026-06-18).** Tried the continuation/
annealing fix (start from clean Ising (u,w), anneal lam3 0->0.856). It FIXED the optimization
oscillation (E stepped smoothly -4.50->-4.118, no bouncing) but the spectrum is ESSENTIALLY IDENTICAL
to the cold start: [0, 0.470, 0.778, 0.930, 1.232, ..., 1.968, 2.14, ...] -- lowest non-zero still
~0.47, STILL missing the TCI light primaries (sigma=0.075, eps=0.2). DIAGNOSTIC CONCLUSION: two
different optimization paths reaching the SAME non-CFT spectrum => the optimizer is NOT the problem;
the TARGET HAMILTONIAN is wrong. Root cause = the crude Hamiltonian-padding shortcut: embedding the
physical d=2 OF 3-site term into the chi=4 corner (h[0:2,...]=h2, other 56/64 dims = ZERO). The MERA
finds the GS of that padded operator, which is NOT the c=7/10 theory (Ising worked by luck -- self-dual
d=2 term is robust; TCI is delicate). CORRECT FIX (Evenbly-Vidal standard): build the bulk Hamiltonian
by ASCENDING the physical d=2 term through a first MERA layer (2->chi isometry), not padding. Status:
optimizer OK (annealing smooth), superoperator OK (Ising-validated {0,1/8,1}), memory OK (matrix-free),
remaining = proper H-lifting (first-layer ascend). This is the last identified blocker for the
alpha-universality number. Ising control remains a clean validated positive. Files: tci_anneal.log,
uw_TCI_annealed.npz.

**H-LIFTING fixes the Hamiltonian; optimization stability now the issue (2026-06-18, ultracode cont.).**
Implemented NRG-style first-layer lifting (w0 = chi lowest eigvecs of the 2-site physical block; ascend
the physical 3-site OF term through w0 -> bulk chi-dim 3-site H) instead of the corner-padding. RESULTS:
- ISING lifted: E=-4.626, dims [0, 0.1389, 1.08, ...] -> Delta_sigma 0.139 vs CFT 0.125 (closer than
  padding's 0.101). Lift VALIDATED on the control.
- Diagnostic: the lifted bulk H is SPECTRUM-PRESERVING (eigenvalue range EXACTLY matches the physical
  3-site H: Ising [-4.806,4.806], TCI [-4.235,5.621]) -> the 3-body term lifts correctly, NOT corrupted.
- TCI lifted: lowest non-zero dim = 0.0686, STRIKINGLY close to TCI sigma=0.075 (~9%) -- vs the padding
  bug's 0.47. So lifting MOVED the MERA to near the c=7/10 fixed point. HUGE improvement.
- BUT: TCI lifted energy = +5.37 (POSITIVE; Ising was -4.63). Since the lifted TCI bulk H spectrum is
  [-4.235, +5.621] (asymmetric, 3-body breaks symmetry), a GS should still be ~negative; landing at +5.37
  means the SVD-update OPTIMIZER is NOT reaching the bulk ground state -- an OPTIMIZATION STABILITY issue
  for the lifted TCI, NOT a Hamiltonian bug (the lift is correct/spectrum-preserving). Consequence: the
  TCI spectrum is PARTIALLY converged -- has sigma~0.069 but MISSES eps=0.2, and no clean Delta_T=2
  (closest 1.747). HONEST: still cannot claim Delta_T=2.
NET: padding bug FIXED (lift validated on Ising, TCI lowest primary now ~sigma). Remaining blocker =
optimization stability for the lifted TCI (reach the actual bulk GS; positive energy = stuck). Likely
fixes: gradient/CG optimizer instead of bare SVD-sweep, anneal lam3 with lifting, more rounds, or a
proper variational energy (the bulk energy expression may need the ascended-H fixed point, not the raw
lifted H). Files: lift_candidate.log, lift_tci.log, uw_TCI_lifted.npz, poc_hamiltonian_lifting.py.

**chi=4 is RESOLUTION-LIMITED for Delta_T=2 — proven by the Ising control (2026-06-18).** Completed the
H-lifting + scale-invariant spectrum at chi=4. Self-consistent-h variant (ascend h to fixed point) FIXED
the energy sign (TCI E +5.37 -> -4.14) but DEGRADED the Ising control (Delta_sigma 0.139 -> 0.053) -> that
ad-hoc modification is WRONG (control caught it; revert to plain lifted). DECISIVE DIAGNOSTIC: the Ising
model has Delta_T=2 EXACTLY (CFT theorem); my chi=4 pipeline resolves it to only ~1.895 (buried in a
descendant cluster 1.63-1.90). So chi=4 CANNOT resolve the stress-tensor dimension even where the answer
is known. Therefore EVERY near-2 TCI value (1.75-1.93) is within chi=4 error of both 2.0 and not-2.0 --
the universality question is UNANSWERABLE at chi=4, NOT because of a bug but because of bond-dimension
resolution. This is a clean, self-validating negative result (the control is its own ruler). WHAT chi=4
DID establish: (1) padding bug FIXED -- TCI lowest primary 0.47 -> ~0.05-0.07 (sigma ballpark, TCI
sigma=0.075); (2) machinery VALIDATED -- Ising recovers its tower; (3) light primaries weakly distinguish
Ising (sigma~0.125) from TCI (sigma~0.075). The Delta_T=2 universality answer NEEDS chi>=6 (scout-predicted;
now PROVEN by the 1.895 control reading). chi=6: matrix-free superop on chi^6=46656-dim space -- genuinely
heavy (this is where RunPod is warranted). Best validated control = PLAIN NRG-lift (Ising Delta_sigma 0.139).
Files: spectra.log, ising_sc_dims.npy, tci_sc_dims.npy, uw_ISING_sc.npz, uw_TCI_sc.npz.

**H-lifting workflow (wf_0369ae32) — confirms approach, CORRECTS the gating (2026-06-18).** The
reference-grounded derivation (read 0707.1454 full text + simple_mera.py) CONFIRMS: one transitional
first layer (own u1,w1) + uniform scale-invariant bulk; padding wrong because it skips w1; 3-site rank-6
operator is the causal-cone-stable unit (3-body OF term needs NO special treatment, same shape as
ham_ising). CORRECTIONS to my implementation: (1) the first layer must be CO-OPTIMIZED (SVD env updates)
jointly with the bulk, h_bulk RE-ASCENDED every outer round -- my fixed-w0 NRG-lift is an approximation
(likely why Ising sigma=0.139 not tighter). (2) ascend via the energy-net grad with bond-heterogeneous
tensors (w1 (chi,2,2), u1 (2,2,2,2)).
**CRITICAL verifier finding (verdict flawed-but-fixable): my CRITICALITY GATE is inadequate.** "A wrong
fixed point can sail through the energy+Delta_2 gates" -- PROVEN: the padding-bug version PASSED
(Delta_sigma 0.101 < 0.04 threshold) while being qualitatively wrong (TCI missed light primaries). So
energy convergence + one low dim is NOT sufficient evidence of criticality. Need a PROPER central-charge
gate (c=0.5 Ising / 0.70 TCI) -- and my c-formulas were broken (inconsistent, ambiguous log base, gives
c~0 on adjacent scales of a scale-inv rho*). Verifier fix: Calabrese-Cardy (different interval lengths
from same rho*) or read c off the spectrum; validate c~0.5 on Ising FIRST. Also: independently verify the
OF coupling lam3=0.856 IS the c=7/10 point (if mis-tuned, nothing else matters). IMPLICATIONS: do NOT
deploy chi=6 yet -- it would risk a confident-but-wrong answer. Prerequisites: (a) correct c-gate reading
c~0.5 on Ising, (b) co-optimized first layer, (c) verified TCI coupling. sim043 energy_net FIXED (verbatim
from validated ref, matches 1e-9; my compressed paraphrase was wrong 2.58 vs 2.13 -- caught before deploy).

**CRITICAL CORRECTION: the c-gate reveals my MERA states are NOT actually critical (2026-06-18).**
Built the proper central-charge gate (c=3(S2-S1) from the descending fixed-point reduced density
matrices, different interval sizes) that the verifier demanded. RESULT: it reads c=0.10 for the
plain-lift Ising state and c=0.19 for the self-consistent one -- but Ising's central charge is EXACTLY
0.5 (CFT theorem). So NEITHER construction is at the c=1/2 critical fixed point. This INVALIDATES the
earlier "validated Ising control" claims: the scaling dimensions {0, 0.139, 1.08, ...} LOOKED Ising-like
but the state is NOT genuinely critical (c=0.10, not 0.5). The verifier's warning was exactly right --
"a wrong fixed point sails through the energy+Delta_2 gates"; eyeballing the dimensions was misleading;
the c-gate is the real criticality test and it FAILS. Root cause (per the workflow recipe): my first
layer is FIXED (NRG truncation), NOT co-optimized, and a single fixed transitional layer + bulk does not
flow to the true scale-invariant critical fixed point. CONSEQUENCE: running chi=6 on this construction
would just give c~0.1 at higher cost -- DO NOT deploy chi=6 yet. The REAL remaining work is the FULL
co-optimized construction (transitional (u1,w1) updated by SVD env each round + h_bulk re-ascended +
proper scale-invariant bulk), validated to read c~0.5 on Ising BEFORE anything else. This is a
substantial algorithm (the workflow's complete ScInv1/ScInv2 loop with a co-optimized first layer), not
a patch. HONEST STATE: alpha-universality NOT answered; all prior MERA spectra this session are
non-critical (c~0.1) and not trustworthy CFT data. The c-gate (built per verifier) is the key new tool
-- it must read c~0.5 (Ising)/0.70 (TCI) before any dimension is reported. Files: cgate.log,
uw_ISING_plainlift.npz. The energy-network, superoperator (identity->1, disentangler-matters), and
matrix-free spectrum machinery remain CORRECT; the OPTIMIZATION is not reaching criticality.

**c-gate FIXED + root cause = bulk flows to TRIVIAL fixed point (2026-06-18, definitive).** Found a real
normalization bug in the c-gate: 'c=3(S2-S1)' is missing /ln2 (Calabrese-Cardy: S(L)=(c/3)ln L, so
increment S2-S1=(c/3)ln2). VALIDATED the corrected gate on the EXACT critical Ising GS reduced states:
3(S2-S1)/ln2 = 0.4985 (true c=0.5) -- gate now correct (exact-diag S(L) fit independently gives c=0.502).
BUT applying the corrected gate to the co-optimized MERA still gives c=0.14 (NOT 0.5), with bulk
fixed-point S1=0.044, S2=0.076 -- the bulk descending fixed-point density matrix is NEARLY A PRODUCT STATE.
ROOT CAUSE (definitive, after 3 first-layer treatments all giving c~0.1): the SCALE-INVARIANT BULK
optimization flows to the TRIVIAL (gapped/product) RG fixed point, not the critical one. This is the
KNOWN central difficulty of scale-invariant MERA -- the trivial fixed point is a more stable attractor
than the critical one from a random start; reaching criticality needs the full Evenbly-Vidal machinery
(Hamiltonian shift, careful multi-sweep schedules, many iterations, often initialization from a converged
FINITE MERA), not the crude from-scratch SVD-sweep loops I built. NOT a first-layer problem, NOT the
c-gate (now validated), NOT the superoperator (validated) -- it's the bulk critical-fixed-point
optimization, which is genuinely hard. HONEST BOTTOM LINE: alpha-universality remains UNANSWERED; reaching
a genuinely critical scale-invariant MERA (c=0.5 Ising / 0.70 TCI) is the prerequisite and my from-scratch
optimizer doesn't get there. Next: either (a) adopt a full battle-tested scale-invariant MERA optimizer
(e.g. adapt simple_mera.py's optimize_linear with shift_ham + proper schedule, or initialize the bulk from
the converged FINITE chi=4 MERA we already have from SIM-040), or (b) accept that this method needs more
than from-scratch implementation. VALIDATED ASSETS THIS SESSION: energy net, superoperator (identity->1,
disentangler-matters), matrix-free spectrum, CORRECTED c-gate (3(S2-S1)/ln2, reads 0.499 on exact crit).
Files: sim044_coopt_mera.py, uw_ISING_coopt.npz; corrected c-formula verified vs exact-diag.

**BREAKTHROUGH: Hamiltonian shift + proper schedule REACHES criticality (2026-06-18).** The trivial-FP
collapse is SOLVED. Adding the Evenbly-Vidal Hamiltonian shift (h_bulk <- h_bulk - lambda_max(h_bulk)*I,
making the bulk H negative-definite so minimization is driven to the true GS, away from the product/
trivial FP) moved the corrected central charge dramatically: c=0.14 (no shift, trivial collapse) ->
c=0.349 (shift, 60 outer rounds) -> c=0.4487 (shift + longer schedule: 150 outer, 12 inner sweeps,
3 descends/sweep, by round 30 and still climbing). c=0.449 vs Ising target 0.5 = ~10%, within striking
distance. CONFIRMED MECHANISM: the shift makes the trivial state high-energy so the variational optimizer
avoids it -- exactly the reference's prescription. Remaining: (1) runs die from torch memory accumulation
before completing (operational, not physics -- need per-round checkpoint + fresh-process continuation);
(2) close the last ~10% (more rounds, or chi headroom). The construction now REACHES the critical fixed
point -- the central blocker of the whole alpha-readout is broken. Next: complete the Ising run to c~0.5
cleanly (checkpoint-and-resume), then TCI (target c~0.70), then the scaling-dimension spectrum + Delta_T=2.
Files: shift.log, shift2.log (c=0.449), uw_ISING_shifted.npz. Workflow wf_7571db20 (canonical schedule)
still finalizing -- will refine the schedule to close the last 10%.

**Shift reaches the critical REGION but optimization OSCILLATES (2026-06-18, honest update).** The
Hamiltonian shift broke the trivial-FP collapse (the key blocker) -- the MERA now reaches the critical
region: corrected c fluctuates 0.32-0.54 AROUND the true Ising 0.5 across consecutive optimization rounds
(round-15 c=0.543, round-20 c=0.320 for the SAME run). But it OSCILLATES rather than converging stably,
so no single checkpoint is a clean c=0.5 state, and the extracted spectrum is correspondingly unstable
(round-20 state gives sigma=0.0215, poor). HONEST: this is real progress (no longer collapsed to 0.14;
now in the critical basin) but NOT a converged critical state -- the bare SVD-sweep overshoots near the
critical point. The classic final scale-invariant-MERA difficulty: getting INTO the critical basin (done,
via shift) vs CONVERGING STABLY within it (needs the full Evenbly-Vidal schedule -- descend-to-convergence
between updates, possibly damping/line-search). Awaiting workflow wf_7571db20's canonical convergence
schedule rather than more hand-tuning. Status: alpha-readout machinery + criticality (region) achieved;
STABLE convergence to c=0.5 is the last step before a trustworthy spectrum + Delta_T=2. Files: shift_c.log
(c=0.543@r15), crit_spec.log (c=0.320@r20, sigma 0.02), uw_ISING_critical.npz (resumable checkpoint).

**Hand-tuned schedule reorderings DEGRADE -- need the principled EV schedule (2026-06-18).** Tested
descend-rho-to-convergence-BEFORE each (u,w) update (EV ordering hypothesis): c DIVERGED monotonically
0.46->1.06->2.08->2.97->3.31 (unphysical, c<=1 for minimal models -- the long descend chain makes rho
pathological). So that reordering is WRONG. Summary of schedule attempts: no-shift c=0.14 (trivial
collapse); shift+12-inner-sweeps c oscillates 0.32-0.54 (critical region, unstable); shift+descend-first
c diverges to 3.3 (broken). CONCLUSION: the SHIFT is the validated key (gets into the critical region),
but STABLE convergence to c=0.5 needs the principled Evenbly-Vidal schedule, NOT my ad-hoc loop
reorderings (which now degrade). Stopping hand-tuning -- the seeding workflow (wf_7571db20) is deriving
the canonical schedule + convergence criteria; that is the principled path. BANKABLE PROGRESS: trivial-FP
collapse SOLVED via Hamiltonian shift; critical region reached (c~0.5 transiently); all machinery
validated (energy net, superoperator, corrected c-gate). REMAINING: stable convergence (principled
schedule) -> trustworthy spectrum -> Delta_T=2. The shift breakthrough is the session's key result on
this thread. Best checkpoint: uw_ISING_critical.npz (c~0.5 region). DO NOT use uw_ISING_stable.npz (c=3.3,
broken).

**EV-schedule (shift + 1iso/1dis/10descend) reaches NEAR-critical: epsilon EXACT, sigma half (2026-06-18).**
Implemented the workflow's canonical Evenbly-Vidal optimize_linear schedule (per round: 1 isometry SVD
update, 1 disentangler SVD update, 10 descends to re-converge rho; Hamiltonian shifted negative-
semidefinite). This DAMPED the oscillation (vs my 12-inner-sweep version): trajectory 1.60->0.71->0.87->
0.61->0.54, landing c=0.54, S1=0.61 (targets 0.5, 0.47). Spectrum from this near-critical state:
[0, 0.0727, 1.0001, 1.069, 1.263, ...] vs CFT [0, 0.125(sig), 1(eps), 1.125, 2]. Delta_eps=1.0001 = EXACT;
identity=0 exact; descendant tower present (1.069~1+1/8). Delta_sigma=0.0727 vs 0.125 = ~half (magnetic
sector, the most delicate, under-resolved). HUGE improvement over collapsed states (sigma was 0.02). 
HONEST: the method WORKS (recovers eps=1.0 exactly, c~0.5, real CFT tower) but is NOT yet PRECISE -- sigma
off 2x, c/S1 slightly high -> state is NEAR but not exactly at the critical FP. Remaining gap: tighter
convergence (the bottom (u1,w1) re-perturbs the bulk each round -> wander +-0.15; fix: converge bulk fully
before touching first layer, or freeze first layer once bulk is critical) + likely chi>4 for the magnetic
sector. NET this thread: trivial-collapse SOLVED (shift); near-criticality ACHIEVED (eps exact); precise
criticality (sigma=0.125) needs convergence polish + higher chi. Best state: uw_ISING_evsched.npz
(c=0.54, eps exact). The shift + EV schedule is the validated recipe; precision is the remaining frontier.

**T1 RESOLVED as a NON-LEVER + co-opt architecture surfaces Delta_T~1.98 at chi=4 (2026-06-19, ultracode).**
Multi-agent verification workflow (wf_808d37cd) + my own numerical check settled the TASKS.md T1
question ("shift physical terms BEFORE lifting -> fix sigma?"). VERDICT: T1 changes ONLY the optimizer
basin, NEVER the converged fixed point. PROOF (three independent): (a) EV 0707.1454 Eq.53 -- the scaling
superoperator is unital S(I)=I, so a constant*I shift propagates up the RG unchanged; (b) a per-term
constant shift leaves the variational gradient wrt the isometric tensors invariant up to an additive
constant; (c) NUMERICS -- shift-then-lift vs lift-then-shift differ by EXACTLY -lambda_max*I on the bulk
(off-diagonal difference 1.8e-15; every diagonal entry = -lambda_max(phys)=-4.806), and both spectra are
bit-identical (sigma=0.0814 either way). The trivial-FP escape is ALREADY solved; T1 fixes a problem we no
longer have. The REAL sigma defect is bond dimension: the Ising CONTROL (where Delta_sigma=1/8 is an exact
theorem and the shift has already succeeded, eps=1.0 exact) STILL under-resolves sigma to ~0.073; that is
the canonical chi-too-small fingerprint (EV's own Fig.27 needs chi=22 for full Ising Delta_sigma=1/8).
Z2-projection ruled OUT (the superoperator is built on the full chi^6 space, no parity restriction).
The EV-correct physical-term shift was folded into sim043.lift_H for correctness (spectrum-identical, but
literature-faithful placement). ERRATA/MEMORY updated.

ARCHITECTURE FORK RESOLVED: plain NRG-lift (sim043, FIXED first layer w0=lowest eigvecs) is CAPPED at
c~0.13-0.24 at chi=4 (smoke: c=0.178; schedule sweep: more-iter LOWERED c to 0.13, more-u raised it only
to 0.24). It CANNOT reach the c=0.54 the co-optimized TWO-LAYER architecture (evsched: variationally-
optimized w1,u1 + bulk) achieves -- the fixed NRG first layer is too rigid. DECISIVE: the co-opt 2-layer
at chi=4 (tight EV schedule: 1 first-layer + 1 bulk + 10 descends per round) produced the spectrum
[0, 0.055, 1.070, 1.083, **1.9816, 1.9816**, 2.078, ...] -- Delta_T=1.9816 RESOLVES TO WITHIN 1% OF 2.0
at chi=4, which neither the plain-lift nor the leading-8 evsched readout ever surfaced. CAVEAT: c
oscillates (5.8->2.7->0.72->0.98->1.49->0.87 across rounds) -- the state passes THROUGH criticality
rather than settling; sub-iterating the bulk to damp it made sigma/eps WORSE (the bulk over-converges to a
stale first-layer h). Fix in progress: take the best-converged round on a COMPOSITE gate (|c-0.5| + |eps-1|
+ |sigma-0.125|), not the last round. NET: the co-optimized two-layer architecture is the correct path to
chi=6, and it ALREADY shows the universal stress tensor Delta_T~2 emerging -- the central HYP-027 signal.

**BREAKTHROUGH: c-oscillation SOLVED via the literal EV ScInv1/ScInv2 loop (2026-06-19, ultracode).**
A second multi-agent diagnosis (wf_9aa73bdb, both analysts HIGH-confidence agreement) + my own freeze
experiment pinned the c-oscillation root cause: the prior co-opt loop violated EV's scale-invariant
algorithm in TWO ways -- (1) rho was iterated a FIXED ~10 descents (never the true descending-superop
fixed point), and (2) h_bulk was a SINGLE ascend of h_phys (not the self-consistent geometric sum
h_bar = sum_tau h_{tau-1}/3^tau, EV Eq.72). The environment was therefore built from a (rho,h) pair
LAGGING the current (u,w) -> the (w1,u1)<->(u,w) coupling formed a LIMIT CYCLE; the c-overshoot (c up
to 3.3) was a rho contaminated by subleading descending modes (c=3(S2-S1)/ln2 is spectrum-sensitive).
Built sim045_scaleinv_stable.py implementing the literal EV ScInv1/ScInv2: each round re-solve rho-hat
as the descending-superoperator FIXED POINT (power-to-1e-11 + PSD-project) and h_bar as the geometric
self-consistent sum, THEN do the SVD update. Two-stage: Stage A co-evolves (multi-sweep) to reach the
critical region (warm-started from uw_ISING_evsched.npz); Stage B freezes (w1,u1)+h_bar and converges
the bulk alone (1 SVD/round, EV ScInv2). RESULT (chi=4 Ising control): c is now STABLE -- trajectory
A0=0.522, A5=0.494, A10=0.479, A15=0.467 (band [0.47,0.52], NO oscillation), eps holding ~1.0. The
limit cycle is GONE. This is the session's key result: the convergence instability that blocked the
entire HYP-027 spectrum measurement is solved. As expected, Delta_sigma stays ~0.06-0.07 at chi=4 (the
known bond-dimension limit -- EV Fig.3/27 needs large chi for the magnetic primary), and Delta_T=2 is
not in the leading chi=4 dims. NEXT: chi=6 on RunPod (sim045 + runpod_deploy_sim045.py, chi-ramp warm
start via pad_mera_chi.py) where sigma should climb toward 0.125 and Delta_T=2 should resolve -> then
TCI (lam3=0.856) to answer the universality question. Files: sim045_scaleinv_stable.py, pad_mera_chi.py,
read_spectrum.py, scripts/runpod_deploy_sim045.py. Diagnoses: wf_808d37cd (T1 non-lever), wf_9aa73bdb
(oscillation fix).

**chi=6 is LOCAL-feasible (matrix-free); RunPod abandoned (2026-06-19).** Timed the chi=6 operations:
rho_fixedpoint 0.3s, SVD updates 0.1s, ascend+hbar 0.1s, c+dims(k=10) 3.4s -> ~4s/round, full run
~10-20min on the 24-core box. The "chi=6 needs RunPod" assumption was wrong: it came from the DENSE
46656^2 superoperator (which OOMs), but the matrix-free LinearOperator superop sidesteps it entirely.
A RunPod deploy was attempted but RunPod's REST /pods misprovisioned a GPU box ($3.29/hr, 8x the cpu5m
estimate) regardless of cpuFlavorIds -> killed within minutes (~$0.15). Lesson recorded in memory
([[runpod-cpu-pod-gotcha]]). chi-ramp WARM START FAILED: padding the chi=4 tensors to chi=6 (even gently,
eps=1e-2) gives a state with c=4.6 not ~0.46 -- the scaling superoperator spectrum is a GLOBAL property
that does NOT transfer cleanly under bond expansion (adding dimensions changes the whole descending-FP
eigenstructure). So chi=6 must COLD-START and anneal. Cold chi=6 (K_COEVOLVE=200, A_SWEEPS=4) RUNNING
locally; descending from c=6.88 (random init). The chi=4 result stands as the method-validation; chi=6
is the science run (resolve sigma->0.125 + Delta_T->2, then TCI). Files unchanged; sim045 chi set via
M.CHI / QW_CHI env.

**chi=6 cold-start PROVEN wrong-basin; recipe decided (2026-06-19).** Cold chi=6 (no warm start)
overshoots: full Ising stage-A trajectory c[A0,A25,A50,A55,A185]=[6.88,1.03,0.66,0.65,0.82] with
sigma best ~0.2 at A25 (c not settled) then COLLAPSED to 0.04 by A50 (c~0.65) -- the two sectors never
simultaneously correct. Best-composite round 43 c=0.686; stage-B from there swept c 0.68->0.41 without
settling. Final on-disk chi=6: c=0.746, sigma=0.037 = WORSE than chi=4's 0.057 -> textbook
collapsed-basin signature, NOT a bond limit (more bond dim resolving the lightest operator WORSE is
conclusive). A 3-agent workflow (wf_100c46c9, WebSearch + EV papers, high conf) + the on-disk ground
truth pinned it: the un-damped alternating-SVD cold-start lands in a wrong basin; chi=4 only worked via
the near-critical evsched warm start; chi-ramp padding fails (bond expansion changes the descending-FP
eigenstructure). DECISION (CHI6-CONVERGENCE-RECIPE.md): Hybrid C+A -- (C) seed the scale-invariant bulk
from a SCALE-INVARIANT finite MERA (modify sim039's validated autograd machinery to SHARE the
middle-layer u,w + joint Adam + polar retraction; the finite-energy minimization is well-conditioned),
then (A) joint autograd refinement of all tensors + multi-restart. NOT pure chi-ramp, NOT ternary. Full
gate (sigma must beat chi=4's 0.057) + fallback ladder (Riemannian L-BFGS / eigen-tower ramp / 2
transitional layers / MERAKit cross-check) in the recipe doc. NEXT = implement sim046 (scale-invariant
finite autograd MERA seed). The HONEST state: alpha-universality remains OPEN, gated on a CONVERGED
chi=6 Ising control; the obstacle is now precisely characterized as a convergence-engineering problem
with a concrete, literature-grounded plan, not a conceptual unknown.

**sim046 finite-MERA seed: critical STATE achieved, but bulk NOT scale-invariant (2026-06-19).** Built
sim046 (scale-invariant finite MERA, torch/Cayley, SHARED bulk, 2 transitional layers to clear the
phys^2=4->chi=6 rank deficiency). VALIDATED end-to-end: norm=1.0 exact; chi=3 rel=0.27%; **chi=6 Ising
rel=0.0040%, ov=0.9999, S_ratio=1.004** -- a near-perfect critical finite state. HOWEVER, reading the
scaling superoperator from the extracted bulk (u,w) gives GARBAGE (c=6.67, sigma=2.34): the bulk was
optimized as a SINGLE coarse-graining tensor (used once at N=16), NOT as a scale-invariant fixed point.
CRITICALITY != SCALE-INVARIANCE. Warm-starting sim045's scale-invariant refinement from it starts at
c~6.4 and descends the SAME path as cold (toward the wrong basin) -- the seed solves criticality, not
the scale-invariance that is the actual hard part. So THREE seeding routes have now failed to give a
scale-invariant critical chi=6 (u,w): cold (c=0.75), raw chi-ramp pad (c=4.6), finite-MERA bulk (c=6.67).
NOTABLE: every chi=6 attempt (cold, refine) shows scaling dims CLUSTERING near 2.0 (1.93, 1.98, 2.10) --
weak recurring evidence that Delta_T~2 IS present, but NOT claimable without a converged critical control
(c=0.5, sigma=0.125). HONEST STATE: the alpha-universality answer remains OPEN, blocked specifically on
obtaining a SCALE-INVARIANT critical chi=6 fixed point. The untried principled lever = EIGEN-TOWER
chi-ramp (grow chi=4->6 in the ascending-superoperator EIGENBASIS, where scale-invariance lives, not the
energy/tensor basis). Documented as the next primary in CHI6-CONVERGENCE-RECIPE.md. The chi=4 result
(method fully validated) stands as the session's solid deliverable.

**DEFINITIVE: the EV ScInv SVD-loop has a chi=6 CEILING, seed-independent (2026-06-19).** Built the
eigen-tower chi-ramp (sim047): grow chi=4->6 by taking the top-6 eigenvectors of the chi=4 2-site bond
reduced density matrix (the SVD-optimal bond expansion in the scaling/eigenbasis). It gave the BEST seed
yet (c=3.79 pre-refine vs pad 4.6, finite-MERA 6.67; isometries machine-clean 1e-16). But refining it
with the EV ScInv loop PLATEAUS at c~1.95, sigma~0.37, eps~0.86 -- still not critical. So FOUR
independent seeds (cold/pad/finite-MERA/eigen-tower) x the SAME loop all fail to reach c=0.5 at chi=6 ->
**the bottleneck is the LOOP, not the seed.** The EV first-order polar-SVD environment update converges
the chi=6 critical fixed point only from an already-near-critical start (which chi=4 had via evsched, and
which no chi=6 seeding provides). Recurring across every chi=6 attempt: scaling dims cluster near 2.0
(1.91-1.99) -- Delta_T~2 is persistently present, the central HYP-027 signal, but NOT claimable without a
converged critical control. THE REAL NEXT STEP (workflow fallback #1, now primary): Riemannian /
gradient-manifold optimization (Hauru-Vidal-Evenbly SciPost 10,040 / 2007.03638: CG/L-BFGS on the
Stiefel manifold, converges where pure EV stalls; our autograd energy is already exact), or a maintained
MERA library (MERAKit.jl) -- a SCOPE step (new optimizer / dependency), flagged for a decision.

SESSION NET (2026-06-19, ultracode): (1) T1 PROVEN a non-lever. (2) the c-OSCILLATION SOLVED (EV
ScInv1/ScInv2: rho-hat eigenvector + geometric h_bar) -- chi=4 Ising stable c~0.5, eps EXACT, Delta_T
1.97/2.04 present. (3) chi=6 obstacle FULLY CHARACTERIZED: it is the EV-loop's first-order convergence
ceiling, not bond capacity (Delta_T~2 keeps appearing) and not seed quality (4 seeds tried) -> Riemannian
optimization is the gated next step. alpha-universality OPEN; chi=4 machinery validated + the obstacle
reduced to a known, named optimization problem with a concrete path. Commits b31c01b, 29249b7, f0946b5,
9987426 (+ this). Files: sim045 (stable loop), sim046 (finite-MERA seed), sim047 (eigen-tower ramp),
read_spectrum, CHI6-CONVERGENCE-RECIPE.md.

---

## 2026-06-22 — HYP-027 SUPPORTED: α=4 is universal at the tricritical fixed point (SIM-2026-051)

The α-universality answer is in. **α=4 is universal at the tricritical Ising fixed point (c=7/10), not
specific to plain Ising.** This closes the central HYP-027 thread.

**The diagnosis was wrong all along.** For multiple sessions the recorded blocker was "the OF 3-site
Hamiltonian blocking into MERAKit's block_size=2 form is wrong" (hand-tilings gave non-critical operators
σ=0.31-0.82). An exact-diag pre-gate (`qw_of_pregate.py`, `qw_of_pregate_compare.py`) demolished that: the
blocked dim-4 operator reconstructs the FULL OF Hamiltonian — including the 3-site XZZ+ZZX terms — to
machine precision (max|H_orig − H_recon| = 0 at λ3=0, 1.1e-16 at λ3=0.856) on 6- and 8-site PBC rings,
with identical E0/site, gap, and spectrum. The supposed "failed straddle heuristic" produces the
ALGEBRAICALLY IDENTICAL operator (diff = 0.0). The blocking was never the problem.

**The real cause was the MERA run.** At χ=6 the energy is FLAT across basins: all 8 random-seed runs land
within an energy spread of 3e-4, but only the clean-basin seeds find the critical fixed point. Energy
cannot select the right basin — you must run multiple seeds and select by SPECTRUM quality (Δ_σ nearest
CFT). The validated λ3=0 control under MERAKit then reproduced critical Ising (Δ_σ=0.140, Δ_ε=0.988,
Δ_T=1.992, matching SIM-050), confirming the operator+driver pipeline end-to-end. The old σ=0.31-0.82 were
simply wrong-basin seeds.

**The measurement** (`qw_tci_measure.jl`, λ3=0.856, χ=6, 8 seeds): best basin (seed 5, Δ_σ=0.154) gives
**Δ_T=2.007 → α=4.01**. Across all 8 seeds Δ_T clusters at ~2.0 (mean 1.99, range 1.92-2.19) regardless of
basin quality — the signature of a UNIVERSAL dimension. This is exactly the CFT symmetry argument: the
stress tensor has conformal weight (2,0)+(0,2), so Δ_T=2 in every unitary 2D CFT, hence α=2Δ_T=4 at ANY
2D critical point. The numerics confirm the symmetry. Δ_σ is only partially resolved at χ=6 (0.154 vs CFT
0.075) because non-universal primaries converge slower than the protected stress tensor, but Δ_σ is not the
α-relevant dimension.

SESSION NET: HYP-027 → **SUPPORTED** (high confidence). Goal "push χ=6 to criticality" (achieved 06-19 via
MERAKit) now extended to the tricritical point. The holographic force exponent α=4 is a universal property
of 2D criticality, established numerically (Ising Δ_T=1.998 + tricritical Δ_T=2.007) and explained by
conformal symmetry. Paper-worthy. Files: SIM-2026-051.json, qw_tci_measure.jl, qw_of_pregate.py,
qw_of_control_correct.jl, of_build_v2.jl. KEY LESSON recorded: validate the cheap certain thing
(exact-diag of the operator) before blaming it — a wrong root cause gated this for sessions.

### 2026-06-22 (cont.) — χ=8 sharpening (SIM-2026-052) + paper-fold

Ran the optional χ=8 TCI sharpening (`qw_tci_chi8.jl`, λ3=0.856, 6 seeds, ~45 min/seed). Decisive
improvement over χ=6: best basin (seed 1) gives Δ_σ=0.092 (CFT 0.075, was 0.154 at χ=6), **Δ_ε=0.204
(CFT 0.2 — exact)**, Δ_T=1.9994 → α=3.999. The Δ_ε=0.2 resolution is the key new datum: it pins the
universality class to c=7/10 DIRECTLY (Ising would give Δ_ε=1.0, unmistakably different), so the full
primary spectrum (σ, ε, T) now confirms M(4,5). Δ_T robust across all 6 seeds (α 3.999–4.060). SIM-052.

PAPER-FOLD (P3 done): integrated the universality result into the local SciPost draft (gitignored until
arXiv) — abstract clause, new §6.5 "Universality of the exponent: the tricritical fixed point" (OF
Hamiltonian Eq.10, exact-diag blocking validation, σ/ε/T comparison table vs M(4,5)), and Discussion
significance item #4. Two citations added to references.bib (OBrienFendley2018 PRL, HauruDamleVidal2021
SciPost). Compiles clean: 22 pages, no undefined refs. χ=8 driver committed 51f2c0c; SIM-052 + this log
trackable. Paper .tex + paired bib entries held local per standing pref.

---

## 2026-06-26 — HYP-028 tested: INCONCLUSIVE (the non-unitary route is structurally obstructed)

Ran HYP-028 (does alpha=4 survive LOSS of unitarity?) per its pre-registration. SIM-2026-053.
Verdict: **INCONCLUSIVE**, with a real methodological finding.

**Built + validated the biorthogonal force pipeline.** New code: i*gamma Ising Hamiltonian (non-Hermitian),
left+right ground vectors via scipy `eigs` (not eigsh), all observables as <L|O|R>/<L|R> biorthogonal
expectations. The mandatory gamma=0 unitary control (G3) reproduces **alpha=3.951 at N=16**, matching
SIM-015d's 3.975 to 0.6% -- but ONLY after correcting the estimator. The first run used the connected-ZZ
correlator change (C_two - C_vac) and failed the control with a spurious alpha~0.54; the root cause is that
that is the SUPERSEDED HYP-002 observable. The validated force is the boundary-primary INTERACTION ENERGY
V = E_dual - E0 - dE_anchor - dE_probe. Switching to it fixed the control. (Same observable-choice lesson the
project has hit before; the G3 control gate is exactly what caught it.)

**Why INCONCLUSIVE, not REFUTED.** The non-unitary runs gave alpha=4.10/4.03/4.00 (N=12/14/16), PT-unbroken
and stable, which the script's automated logic flagged as REFUTED (alpha=4 generic / survives non-unitarity --
the stronger-universality branch). OVERRIDDEN on honest review: the chosen realization (uniform i*gamma-on-Z
chain) has its Yang-Lee critical point sitting AT the PT-breaking edge, and the PT-unbroken window shrinks as
~1/N (kappa_c = 0.0105/0.0074/0.0056/0.0043 at N=10/12/14/16). To keep a real spectrum we must sit at
kappa~0.9*kappa_c = 0.0039 at N=16, a ~0.1% non-Hermitian perturbation whose force profile differs from the
unitary one by <2% at every dr. So alpha~4 reflects PROXIMITY to the unitary point, not survival of the
Delta_T=2 protection at a genuine non-unitary fixed point. The pre-registration's G4 gate (confirm c_eff=2/5,
Delta_phi=-1/5) is NOT satisfied -- the gap_re proxy shows the unitary gaps, no Yang-Lee signature.

**Net finding (design feasibility).** The uniform-imaginary-field route is structurally obstructed at exact-
diagonalization sizes: Yang-Lee criticality = PT-breaking edge, kappa_c -> 0 with N, so no accessible regime
is simultaneously PT-unbroken AND far enough off-unitary to revoke the theorem. A genuine test needs a
realization where the non-unitary fixed point sits at FINITE distance inside the PT-unbroken phase -- a
non-Hermitian FREE-FERMION chain at the Yang-Lee edge (the 2606.17983 biorthogonal construction), or a
metric-operator / PT-inner-product formulation. HYP-028 stays OPEN; the biorthogonal pipeline
(hyp028_nonunitary_force.py) is reusable for the better realization. HYP-027 (the SUPPORTED unitary-class
universality result) is untouched -- this was a probe of the protection's boundary, not of the anchor.

---

## 2026-06-27 — alpha=4 at a THIRD CFT class: 3-state Potts c=4/5 (SIM-2026-057), HYP-025 SUPPORTED (caveat)

Extended the universality ladder to a third, distinct unitary CFT. SIM-057, HYP-025.

The 3-state quantum Potts critical point (Z3 clock/shift, c=4/5) is a genuinely different CFT from Ising
(c=1/2) and tricritical Ising (c=7/10): different central charge, different primaries, qutrit (d=3)
substrate. Sharp a-priori test: Delta_T=2 in every unitary 2D CFT, so alpha=2*Delta_T=4 MUST hold.

RESULT: chi=6 scale-invariant ternary MERA (block_size=2 -> dim-9 super-sites, single-thread-BLAS
deterministic, 8 seeds, select-by-spectrum). Best basin: Delta_T=1.997 -> alpha=3.994; Delta_eps=0.861
(CFT 0.8). Delta_T clusters ~2.0 across ALL 8 seeds (mean ~2.03 ex-outlier, 6/8 in [1.98,2.18]) regardless
of how the rest of the tower resolves -- the same universal-dimension fingerprint seen in both prior
classes. alpha=4 is now confirmed across Ising -> tricritical Ising -> 3-state Potts.

CAVEAT (honest, keeps it SUPPORTED-with-caveat / MEDIUM not high): Delta_sigma is NOT cleanly resolved at
chi=6 (best basin 0.070 vs CFT 0.133; other basins 0.56-0.89). This is the SAME finite-chi ceiling the
tricritical chi=6 run hit (Delta_sigma scattered) and resolved only at chi=8 (SIM-052) -- worse here because
the c=4/5 tower is denser. The alpha verdict rests on Delta_T (well-resolved) plus Delta_eps=0.86 (which
unambiguously identifies c=4/5: Ising eps=1.0, TCI eps=0.2 would be unmistakable). A chi=8 Potts run would
sharpen Delta_sigma->0.133 for a clean full-spectrum confirmation, exactly as chi=8 did for the tricritical
case. Driver: research/tools/MERAKit.jl/qw_potts_measure.jl. The qutrit substrate + block_op(dim-9) pattern
is reusable for any future c>1 / clock-model universality test (e.g. true Z3 chiral clock).

---

## 2026-06-28 — OPE C_sse fix v2 (SIM-2026-058): STILL_BROKEN, genuine PEV route identified

Second attempt at the OPE 3-point extraction (toward C_TTT, the emergent graviton self-coupling). Fixed the
two bugs SIM-056 flagged: (1) disentangler inclusion -- v2 builds the width-3 marginal from MERAKit's
descend_mid causal cone (not the bare w*rho1*w' of one isometry); (2) the kinematic prefactor -- the
straddling triple sits at separations (1,1,2) so the structure constant needs 2^Delta_eps, not the bare
3^Omega. The resulting rho3 is a valid RDM (tr=1, Hermitian 3e-16, partial traces normalize).

VERDICT STILL_BROKEN -- and the adversarial verifier earned its keep. The build agent stopped at ONE clean
basin (seed1: C_sss=0.013, C_sse=0.485) and called it MARGINAL. The verifier re-ran n>=3 clean basins and it
collapsed: C_sss = 0.008/0.084/1.92 (must be ~0; 250x spread), C_sse = 0.485/0.897/0.812 (must be 0.5; mean
~0.73). DECISIVE: the BEST-spectrum seed (Dsig=1/8 exactly) gave the WORST OPE -- so clean spectrum does NOT
predict correct OPE, and seed1 was basin luck (the SIM-056 one-clean-basin false positive, now bit twice).

The disentangler+prefactor fixes were necessary but insufficient. ROOT CAUSE (deeper): building ANY explicit
rho3 from the width-2 rho2 is not a faithful 3-point object -- the ternary causal cone is width-2, and the
straddling-triple marginal, though a valid RDM, is not the correct PEV construction. THE FIX (route b, not
yet implemented): the genuine PEV algorithm -- ascend each of the 3 operators individually up the network
until their supports are adjacent (fit the width-2 cone), then contract against rho2; do not build any rho3.

RunPod correctly NOT spent (chi is not the blocker -- dims clean at chi=6 per SIM-050; the extraction is
wrong; a GPU run would reproduce the basin scatter). Gate before any RunPod: C_sss<0.02 AND C_sse in
[0.45,0.55] across >=3 clean seeds at chi=6, locally. The C_sss Z2 parity probe remains the cheap decisive
correctness test; "collect >=3 clean basins before declaring an OPE pass" is now a hard discipline rule.
Files: qw_ope_constants_v2.jl, ope_cone_v2.jl, test_cone_v2.jl. SIM-058.

---

## 2026-06-28 — chi=8 Potts sharpening (SIM-2026-059): PARTIAL, alpha=4 robust, Delta_sigma improved-not-resolved

Ran chi=8 on the 3-state Potts c=4/5 point (8 seeds) to try to resolve Delta_sigma->0.133, mirroring how
chi=8 sharpened the tricritical case (SIM-052). HONEST RESULT: partial.

alpha=4 is CONFIRMED even more robustly than at chi=6: best basin (seed3) Delta_T=2.014 -> alpha=4.028, and
ALL 8 seeds give alpha in [3.94, 4.11] (Delta_T mean 2.015). Fourth confirmation of the universal-dimension
fingerprint. Delta_sigma IMPROVED from chi=6's 0.070 to 0.094 (two clean basins, seeds 3 and 6, independently
agree). BUT Delta_sigma is still ~30% short of CFT 0.133, and only 2 of 8 seeds reached the clean basin --
chi=8 did NOT replicate the clean tricritical-style resolution. The c=4/5 tower is genuinely denser/harder.

So HYP-025 stays SUPPORTED-WITH-CAVEAT: the caveat is reduced (Delta_sigma moving the right way, alpha
rock-solid, Delta_eps 0.81-0.95 in clean basins) but not eliminated. The alpha=4 universality verdict is solid
(it rests on the well-resolved Delta_T, not on Delta_sigma). A clean full-spectrum confirmation needs chi=10-12
(RunPod A100, ~$10-20, approved). I did NOT overclaim "sharpened" -- chi=8 improved it but fell short of clean.
Driver: qw_potts_chi8.jl. SIM-059.

---

## 2026-07-02/03 — OPE pipeline VALIDATED on 4th attempt (SIM-060 FAIL -> SIM-061 PASS); Z3 Potts port (SIM-062)

SIM-060 (v3, dense parity-lift): FAIL on all 8 chi=6 seeds -- lift dominance ~1.4, overlap 0.05-0.26.
Structural discovery, not a bug: dense random-init LBFGS basins sit in a GENERIC GAUGE where the pushed-through
Z2 symmetry is a finite-depth circuit on internal legs, never a one-site product. One-site parity machinery is
impossible on dense tensors. THE FIX (v4, qw_ope_pev_z2.jl): optimize with Z2-SYMMETRIC tensors (direct-init at
target chi; the old "Z2 broken" myth was a ramp artifact) -> sector-resolved basin gate -> densify (basis =
sector order => P = diag exact) -> dense PEV Eq.10/13 analysis, identifying sigma/eps BY PARITY CLASS.
SIM-061: chi=6 8/8 clean, C_sse mean 0.5075; chi=8 4/4 clean, 0.5069 +- 0.0315. GATE PASS vs CFT 0.5.
C_sss = 0 exactly on every seed (Z2 selection rule); covariance 1.000000. Same day: Z3-graded Potts port
(qw_potts_z3.jl, empirical fusion-tree index map, injection err 1.75e-15): 4/6 clean at chi=6 vs dense 2/8.
SIM-062. RunPod GO.

## 2026-07-04 — RunPod chi-escalation: HYP-025 CLOSED CLEAN (SIM-063); OPE 0.6% precision + drift flag (SIM-064)

RunPod CPU pod (32 vCPU, ~$10.20 total, killed+verified). Potts Z3: chi=9 3/6 clean, chi=12 2/6 clean with
Dsig = 0.1324/0.1351 (CFT 2/15 = 0.1333), Deps = 0.804/0.806 (0.8), alpha = 4.001/4.005. The chi-starvation
diagnosis was exactly right (0.089 -> 0.14 -> 0.133 over chi = 6/9/12). HYP-025 upgraded SUPPORTED-clean.
UNIVERSALITY LADDER COMPLETE: Ising c=1/2, tricritical c=7/10, Potts c=4/5 -- full towers, all alpha=4.
Ising OPE chi=10/12: basin spread collapsed 40x to 0.6% (chi=12: 0.4722 +- 0.0027) but the mean drifted
THROUGH 0.5 to 5.6% low -- flagged with 3 ranked suspects (SIM-064).

## 2026-07-08 — OPE drift RESOLVED: kinematic placement systematic, not under-convergence

Two placement channels BRACKET the CFT value at both chi (sse 0.472 / ses 0.515 at chi=12; gap 20x basin
spread). Maxiter kill-test (chi=12 seeds at 8000 iters, 51.6 ks local) did not move the mean toward 0.5 ->
under-convergence ruled out. Verdict: finite-chi placement kinematics. Prescription: quote the placement
average C_sse = 0.50 +- 0.03. Pipeline precision (0.6%) unaffected -- C_TTT targets differ by 7-18%, far
above both noise floor and systematic. SIM-064 closeout.

## 2026-07-13 — Paper v5 alignment pass: ERRATA E1-E5 applied, Potts + measured OPE folded in, compiles clean

Full findings-vs-paper audit, then v5 edits to paper-draft-scipost.tex (LOCAL): E2 transport restated grid-
converged (-1.21% N=16, -2.78% N=12, coarse 0.72% labeled artifact; N=24 double-lobe caveat); E1 l_AdS table
recomputed; E4 m_eff rewritten in AdS3 convention Delta(Delta-2) (0.693 = 1/l_AdS from Delta=1 exactly);
E3 penalty row annotated; E5 Zenodo DOI added. Fixed OQ#4/sec-6.5 contradiction and the "six seeds within
1.5%" claim (SIM-052 seed 4 = 1.51% -> "within 2%"). NEW: sec 6.5 now Ising/TCI/Potts (three classes, one
exponent); sec 7.4 gains the measured C_sse = 0.50 +- 0.03 with the placement systematic honestly stated.
PfeiferEvenblyVidal2009 added to references.bib. Compiles clean (MiKTeX, 0 errors, 0 undefined citations).
Zenodo v3 still carries E1-E5 -- mint v4 (new version DOI) when v5 is final. Journal targets (2026-07-07
decision): PRD direct (RevTeX, primary), J.Phys.A, JHEP -- none requires arXiv.

---

## 2026-07-14 -- Scan #15 + C_TTT Route A implemented (SIM-065 in progress); paper v5 committed

Scan #15 (digest research/digests/2026-07-14-scan.md): PAPER-135 (2607.03534, c=1 compact-boson
fixed-point tensors -> HYP-030 moduli-line alpha=4 test) + PAPER-136 (fuzzy-sphere Yang-Lee ->
HYP-028 note); HW-070-074; zero anchor contradictions.

C_TTT (qw_ope_cttt.jl, SIM-065): Route A implemented with two documented refinements (theta-phase
scan selected by the C_TTbarI structural zero -- the h/p relative phase is provably invisible to
the 2-pt metric; rho2-orthonormalized block basis). chi=6 smoke: all structural gates pass, best
block-clean seed C_TTT = 3.66 vs target 4.000 (8.5%). chi=8 v1: dims pristine, gates pass, but the
single-sided one-site reduction admits reflection-even contamination into O- (p_side_ratio ~0.8)
and C_TTT scatters 3.0-9.3. Fix: parity-resolved reduction (sym for h, antisym for p); chi=8 v2
in flight. Fallbacks if v2 fails: width-2-space projection or Route B; R5 honest-null stays live.

---

## 2026-07-15 -- Zenodo v4 PUBLISHED; outreach batch SENT; C_TTT v3.1: mechanism validated, number chi-limited

Zenodo v4 live (10.5281/zenodo.21381474, v5 content + changelog; API token minted -> ~/.zenodo-token;
serializer gotchas in memory [zenodo-doi]). Outreach: Orth + Swingle/Sahay/He/Czech + QuEra follow-up
ALL SENT from joncackler@gmail.com citing the v4 DOI (Iadecola silent through deadline; Evenbly pending
via web form). PRD package portal-ready (Sahay ref -> published PRX 15 021078).

C_TTT (SIM-065, v3->v3.1): reduction step ELIMINATED in favor of rho3-correlator pairing; two exact
fixes en route (blocked-operator reflection needs intra-block reversal R; L/R pairing sign is gauge-
dependent -> self-calibrated). RESULT: full gate stack passes (G3=0, G4 structural zero, C_sse pin,
parity); best C_TTT = 4.20 and 3.71 vs exact 4.000 (chi=6); G4 correctly self-flags junk basins. NOT yet
basin-stable (5 clean seeds: 1.95-11.87) -- instability isolated to Delta~2 block pollution at chi<=8.
Next: chi=10-12 RunPod escalation (PEV precedent: chi=22 for tight numbers), window-sensitivity study,
Route B as fallback.

---

## 2026-07-16 -- C_TTT Route A CLOSED by chi-escalation (SIM-066): honest negative, Route B is next

RunPod chi=10/12 x 8 seeds each (~$4, pod killed+verified): scatter WORSENED with chi (gate-clean values
2.2/2.1/25.7/0.06 at chi=12; a 6e8 blowup at chi=10). KILLER DATUM: G4 = 0.0000 exactly with C_TTT = 25.7
-- the gate stack certifies the chiral split but NOT membership in the physical {T,Tbar} span. Conclusion
(R5, the design's honest null): one-site PEV extracts scalar OPE (C_sse = 0.50 +/- 0.03 stands) but NOT
spin-2 self-coupling; the isometry-only one-site superoperator breaks the translation covariance spin
phases require. The chi=6 4.20/3.71 hits are unclaimable. Successor: Route B width-2 translation-phase
eigenbasis (momentum as an actual quantum number). C_TTT was never in the paper -- v4/v5 claims unaffected.
Ops note: full CPU-pod recipe (ubuntu+PUBLIC_KEY+sshd, dedicated runpod_ed25519 key, instantiate-not-setup.jl)
now proven end-to-end; 16-process parallel driver pattern works.

---

## 2026-07-19 -- C_TTT Route B: ISING 4.000 GATE PASSED (SIM-067); TCI needs puMPS-scale N

Route B realized on the CIRCLE (periodic chain ED), not width-2 MERA: on the line, fixed-point
translation eigenphases are restricted to {0, pi} (theta = 3*theta mod 2pi), so conformal spin only
becomes an actual quantum number on the circle -- the rigorous home of SIM-066's successor idea.
First design (equal-time <hh>/<hhh> with cylinder kinematics + KW-parity argument) FALSIFIED by ED
same-day: <hh>_conn is negative, non-cylinder-shaped, exactly zero at antipodal separation (free-fermion
form -(16/pi^2)/(4x^2-1)^2); sign puzzle recorded as open theory footnote. Pivoted to the Koo-Saleur
matrix-element route: c = 2|<T|H_{+-2}|0>|^2 with T = lowest even-sector s=+2 translation eigenstate
(Z2 resolution essential; max-element T-ID falsified -- band-edge states have ~2x larger UV elements).
Chiral split is free by momentum conservation; wrong-chirality element = STRUCTURAL ZERO (0.0000 every N).
ISING RESULT (N=8..18, 1/N^2): c -> 0.49871, C_TTT -> 3.9936 vs 4.000 (0.16%), C_sse pin -> 0.49996.
Literature anchor found after the fact: Zou-Milsted-Vidal PRL 121 230402 uses exactly this c-formula.
TCI (OF lam3=0.856): spectrum gorgeous (3/40, 1/5, 7/8 all hit) but c-element unconverged (1.2 vs 0.7)
-- L_{-2}eps sits 0.2 above T with identical quantum numbers, contamination ~N^{-0.2}; ZMV needed
N<=128 puMPS for this model.
Retrospective: Route A never had a chance at TCI -- even exact ED needs N~128-scale IR resolution.

**CORRECTION 2026-07-20 (was written above as a next step, and was WRONG):** the line "vendor
amilsted/puMPS (Julia -- our stack)" was an unverified web-search artifact. **No public `amilsted/puMPS`
package exists** -- checked against the GitHub API; amilsted's public repos are evoMPS (Python/TDVP) and
ITensor tooling. puMPS must be IMPLEMENTED from Zou-Milsted-Vidal arXiv:1710.05397 (ansatz
Tr(A^s1...A^sN) + momentum-resolved Bloch excited states), or MPSKit.jl / ITensorInfiniteMPS.jl evaluated
as a substrate. Two further routes were tested the same day and are DEAD: (a) ground-state-only
c = 2||H_{-2}|0>||^2, which is UV-dominated and grows ~0.5N; (b) summing matrix elements over the
near-degenerate |s|=2 doublet, which overshoots. The single-state matrix element remains the correct
filter; N is the only blocker.

## 2026-07-21 / 07-27 -- scans #17 and #18

Scan #17 (window 07-19 -> 07-21): EMPTY. Notable as PROCESS, not physics -- the parallel workflow tripped
the arXiv export-API burst limiter and silently dropped 3 anchor-relevant query lines (Yang-Lee/HYP-028,
c=1/HYP-030, and the Koo-Saleur/conformal-data cluster widened *because* of SIM-067). All three were
re-run manually and sequentially before the digest was written; each confirmed genuinely empty. Standing
rule adopted: fire theme queries SEQUENTIALLY with a few seconds' spacing.

Scan #18 (window 07-21 -> 07-27): sequential fix HELD, zero dropped lines. One catalogue,
**PAPER-138 (2607.21536, rel 4, Kuang-Hung Chou)** -- "Beyond Calabrese-Cardy Scaling: Exceptional-Point
Sensitivity from the dS RT Surface". Same author as PAPER-119 (2606.17983), which seeded HYP-028, and it
advances exactly the non-unitary-cMERA route SIM-053/055 designated as the way forward. Supplies a cheap
diagnostic S_res = log(Delta*L) (interval-independent, detectable on a ONE-site subsystem, explicitly no
Hermitian analogue) plus an IR-termination note (a finite-depth circuit on a ring cannot disentangle to a
one-site product state; it leaves an entangled TWO-site IR state). **Honest limit: it does NOT unblock
HYP-028** -- the construction lives near exceptional points, the same PT-edge neighborhood that obstructed
our ED route, and supplies no fixed point at finite distance inside the PT-unbroken window. Preferred next
step UNCHANGED: PAPER-133's periodic PT-chain route first. No new hardware records (RIKEN ROQUO, IBM $50M
DOE + HRL acquisition, EuroHPC MeluXina-Q, OptQC MoQuren, Infleqtion Sqale, Northwestern 24.4 km fiber --
all rel<=2, no frontier number). No anchor contradictions in either window.

---

> **BACKFILL NOTE (written 2026-08-17).** Everything below this line was written in one pass on
> 2026-08-17, closing audit defect **D-24**: the log had a three-week hole from 2026-07-27 to
> 2026-08-17, and the PRD submission, scan #19 and SIM-068 through SIM-071 all happened inside it.
> Entries are dated to the day the work happened and are reconstructed from the structured records,
> the digests and the git history (`f124038` .. `d17b7a2`), NOT from contemporaneous notes -- treat
> the reconstruction itself as a weaker source than a same-day entry. Where the 2026-08-17 audit
> later changed what a result means, the change is stated inside that day's entry rather than
> smoothed away, per RESEARCH-DIRECTOR.md section 32 (preserve the original claim, the evidence at
> the time, the challenge, the corrected analysis, and the changed conclusion).

## 2026-08-07 -- SUBMITTED to Physical Review D: accession DV13971, "With editors"

Paper 1 submitted to PRD as a Regular Article in the section *String theory, quantum gravity,
gauge/gravity duality*. **Accession `DV13971`, status "With editors"** (commit `f124038`). Package:
`research/submission-package/prd/` (RevTeX 4.2, 13 pp, compiles clean); portal draft
`es2026jul20_951`. One real defect was caught and fixed before upload on 07-20: the manuscript cited
the Zenodo **version** DOI 19661227 instead of the **concept** DOI 10.5281/zenodo.19660302; the
corrected PDF is the one on file and the version DOI appears nowhere in the submission.

Why now: the 7-target outreach batch (Orth, Swingle, Sahay, He, Czech, QuEra, Evenbly) was exhausted
as a strategy -- zero replies, inbox verified 2026-08-04 at day 20, well past the self-imposed
"~10 days then PRD regardless" line of 07-25. SciPost account approval and arXiv endorsement both
still blocked; PRD needs neither.

**AUDIT 2026-08-17 (added in backfill -- this is the consequential part of the entry).** The
manuscript went out carrying claims that did not survive the audit ten days later:
- Its **central finding is now withdrawn** -- alpha = 3.92 +/- 0.16 is an estimator artifact
  (`SIM-2026-072`, D-2/D-3; corrected value alpha = 2.6 +/- 0.2, channel OPEN). A correction to the
  editors is required, not optional; the package is `docs/governance/PRD-CORRECTION-PACKAGE.md`.
- **D-4:** four wrong author given-names and four wrong titles in `references.bib`, each contradicted
  by the project's own catalogue -- including `ZouMilstedVidal2020`, the citation that sources the
  operator the whole force result rests on.
- **D-9 / D-25:** the Data-and-Code-Availability statement is unsatisfied at both endpoints (8 of 19
  named items absent from the public repo, which is 85 commits behind; the Zenodo record holds one
  PDF, and it is the SciPost version), and **no frozen snapshot exists for a manuscript under
  review** -- zero git tags, the submission commit unpushed, four SIM records postdating it on the
  same branch.
- **D-1:** the "Wang and He proved t_trans = pi analytically" citation is substantially accurate (the
  derivation is in their Supplemental S3 A, read at primary source 2026-08-17) -- but their result
  carries **no AdS radius at all**, so citing it as confirmation of T = (pi/2)*l_AdS stacks a factor
  of 2 on top of an l_AdS that their derivation says cancels.
Process lesson, stated plainly: submitting was not the error; submitting **without having run the
adversarial passes on our own strongest claim first** was. The audit that found D-2 used only data
that had been sitting on disk since 2026-04.

---

## 2026-08-09 -- Scan #19 (EMPTY 13-day window) + puMPS UNBLOCKED: the ZMV codebase is public

**Scan #19** (digest `research/digests/2026-08-09-scan.md`, window 07-27 -> 08-09, ran 6 days late
because the PRD push took priority): **EMPTY for catalogue purposes -- no new IDs, no anchor
contradictions, no hypothesis candidates.** Sequential-query discipline held for the third
consecutive cycle (zero dropped lines). Two WATCH, neither catalogued: **2608.02716**
(Kumar-Patil-Ludwig-Vasseur, weakly-monitored critical AND tricritical Ising -- our exact models,
an orthogonal observable class; the "does alpha survive weak monitoring?" thought is parked as a
seed, not proposed) and **2608.04083** (g-theorem monotonicity breaking in PT-symmetric Kondo --
consistent with HYP-028's framing that unitarity is the load-bearing axiom, but boundary-impurity,
supplies no bulk fixed point). **PAPER-133 got a v2** (2606.16785v2) -- flagged to diff before
starting the HYP-028 reproduction, and that flag was honoured two days later. Hardware busy but
frontier-static (D-Wave gate-model pivot at 99.9% two-qubit is an order below IonQ's 99.99%; Qarakal
Pangaea design-stage; SaxonQ third re-report). New query gotcha: **arXiv stems "puMPS" to "pump"** --
a 3-clause OR containing `abs:"puMPS"` degraded into the laser-physics firehose; use
`abs:"Koo-Saleur"` or `abs:"periodic uniform matrix product"` instead.

**Same day, the actual unblock:** the Zou-Milsted-Vidal puMPS codebase turned out to be **public**
(`yijian-physics/puMPS`, commit 0557b12) -- so the from-scratch ZMV implementation queued since
07-20 was **cancelled**, not built (commit `a684ebd`). Validation gate passed immediately: Ising
N=12 D=8 gives C_TTT = 4.011 vs exact 4 and c = 0.4972, both chiralities (`09c01be`). This is what
put SIM-068 and SIM-069 within reach the same week.

**AUDIT 2026-08-17 (backfill).** The novelty consequence of that unblock went unrecorded at the
time and should have been obvious on the day: the vendored package already exports
`OBF_Hn_MPO_split` "(TCI!)" and `potts3_Hn_MPO_split` -- i.e. the upstream authors had already built
the TCI and Potts rungs into the tool. Milsted-Vidal 1706.01436 and Zou-Milsted-Vidal 1710.05397
publish `c` for all three of our models, using the same estimator and, for two of three, the same
code. **Neither paper has a PAPER record in this repository** (audit section 4.5: seven of the
project's own methodological parents are uncatalogued). Adopting someone's codebase is exactly the
moment to catalogue their papers, and we did not.

---

## 2026-08-10 -- SIM-2026-068: the TCI rung, c_inf = 0.699 +/- 0.002 (C_TTT 3.381 vs 3.3806)

Second rung of the "self-coupling ladder" on the O'Brien-Fendley chain at lambda2 = 0.428 (our TCI
point in the puMPS half-energy normalization), driver `pumps-setup/qw_cttt_of.jl`. puMPS ladder
N = 14/20/28/40/56 with per-N bond-dimension checks: **c_inf = 0.699 +/- 0.002 vs exact 7/10**, from
which `C_TTT = 2*sqrt(2)/sqrt(c) = 3.381 +/- 0.005` vs 3.3806. Chirality symmetry holds to <=1e-4 at
every N >= 20; gap ratio eps/sigma 2.680 at N=56 vs M(4,5) exact 2.667.

Three things were genuinely learned, and they are the part of this entry that survives:
- **The L_{-2}eps contamination that killed the ED route is strongly suppressed in puMPS Bloch
  elements.** At N=56 the largest non-T raw element is <=0.0003 against T's 0.109 (~400x), and the
  observed finite-size correction exponent is p ~ 2.4, not the N^{-0.2} that raw ED showed. The
  variational Bloch tower resolves the near-degenerate states ED mixed.
- **T/L_{-2}sigma level ordering FLIPS** between N=14 (T is 2nd lowest at k=2) and N >= 28 (T is
  lowest). Element-dominance identification handles it automatically; position-based ID would have
  silently measured the wrong state at one end of the ladder.
- **Two-error cancellation caught:** N=56 at D=20 gave a spuriously perfect c = 0.7008 (finite-N
  biases c up, truncation biases it down); only the D=24 re-run exposed it and put the point back on
  the trend. Constant-D ladders or per-N D-convergence checks are mandatory.
Ops: warm-starting D by tensor padding throws `LAPACKException(30)` in the transfer-matrix
eigensolve -- the same failure as MERAKit's chi-ramp; direct-init at target D is the rule. Background
jobs were externally killed 7 times; short CG rounds + per-round JLD2 checkpoints + wall-clock
exit(42) + repeated foreground invocations is the pattern that finishes.

**AUDIT 2026-08-17 (backfill).** Two corrections, both of which change how this rung should be
described:
1. **This is a central-charge reproduction, not a measurement of a three-point coupling.**
   `C_TTT = 2*sqrt(2)/sqrt(c)` is a Virasoro identity and appears as a literal line of code in every
   driver (`qw_cttt_of.jl:117`). The quantity measured is `c`; C_TTT follows by arithmetic. Because
   the map is a square root, quoting C_TTT rather than c **halves the apparent error** (verified
   ratio 0.5008 here), so "0.15%" is 0.26% in the quantity actually measured. Correct framing:
   *"we reproduce the Milsted-Vidal / Zou-Milsted-Vidal Koo-Saleur central-charge extraction."*
2. **The contamination-suppression result is not new.** Milsted-Vidal 1706.01436 section IV.A
   introduces Eq. (22) explicitly to eliminate the finite-size corrections that connect |I> to states
   other than |T> -- the suppression is the *published rationale* for the estimator we adopted, the
   element-dominance identification rule and its failure mode are also theirs, and the N^{-2} law is
   published for Ising, Potts and the OF/TCI point. The "N^{-0.2} foil" originates inside this
   project, not in the literature. What survives as ours: the numerical dominance ratio reported as a
   quantitative diagnostic (audit CLM-027, novelty ELIMINATED; residue Level 1-2).
Neither correction touches the numbers. Both change the claim they support.

---

## 2026-08-11 -- SIM-2026-069: the Potts rung; the ladder is complete (and is a c-ladder)

Third rung, critical 3-state Potts at self-dual h=1, driver `pumps-setup/qw_cttt_potts3.jl`. Ladder
N = 10/14/20/28/40 with per-rung D-convergence: **c_inf = 0.7995 +/- 0.0012 vs exact 4/5**, giving
`C_TTT = 3.163 +/- 0.003` vs 3.16228. With SIM-067 (Ising) and SIM-068 (TCI) that is three unitary
classes measured through one pipeline, each at <=0.15% in C_TTT.

The methodologically interesting content:
- **A momentum-resolved ED gate at N=10** (base-3 generalization of the vendored `UnitTestED` trick)
  certified the d=3 CG plateau-accept decision: the Potts optimizer floors at |grad| ~ 2.5e-4 versus
  9e-5 on OF d=2, not fixable by step or `pinv_tol` tuning, and energies keep creeping ~1e-9/iter.
  Agreement at the gate: E0/site 1.4e-6, T gap 1.8e-4 rel, gap ratio 6.1929 vs 6.1924.
- **The ED gate reconfirmed the SIM-067 band-edge trap**: in raw ED the max-element state is a UV
  state at Delta ~ 2.53 with 4.5x T's element -- naive element-dominance on ED would have returned
  c = 5.9. puMPS Bloch elements suppress every non-T element to <=6e-4.
- **Z3 charge does free work:** the charged sigma-descendants nearest T in energy have structurally
  zero KS elements (exact in ED, H being neutral), so Potts element space is *cleaner* than TCI's
  despite the denser spectrum.
- **Two-error cancellation became PREDICTIVE.** The N=40 D=28 value was called at 0.8022 +/- 0.0005
  from the D-shift systematics **before the run**, and landed at 0.80197. That is the only
  out-of-sample prediction in the program to date and it succeeded (audit CLM-029).
- **Stopping rule applied, not drifted past:** N=56 was deliberately omitted -- four clean D-checked
  rungs already beat SIM-068's precision and a fifth could not change the verdict.

**AUDIT 2026-08-17 (backfill).** The correction from SIM-068 applies to the whole ladder, and it is
the reason the branch is now closed:
- **"C_TTT ladder complete" overstates what happened.** `C_TTT = 2*sqrt(2)/sqrt(c)` is a line of code
  (`qw_cttt_potts3.jl:132`); the ladder measures `c` three times. Milsted-Vidal 1706.01436 Fig. 4
  publishes c for **Ising (0.4995) and 3-state Potts (0.7985)**, and Zou-Milsted-Vidal 1710.05397
  Table I publishes c for **Ising (0.4999997) and the O'Brien-Fendley TCI point (0.6991)** -- all
  three of our models, same estimator, and for two of three the same vendored code. Our Ising rung is
  **less** precise than MV's at the same sizes. **The honest framing is: "we reproduce the MV/ZMV
  extraction on three minimal models, extending the published Potts rung from N <= 14 (ED) to
  N <= 40 (puMPS)"** -- one rung is a genuine ~1e-3 improvement, and that is the whole of it
  (audit D-16, section 4.2; counterfactual novelty ZERO).
- **The one route that could have measured a three-point function failed and was not replaced.**
  Route A (direct <TTT> contraction) was falsified by ED the day it was designed (SIM-065/066, killer
  datum G4 = 0.0000 exactly with C_TTT = 25.7). Route B then substituted a **two-point** observable
  and no record states that the object it measures differs from the one Route A could not measure.
  Route A's failure was a real negative result, correctly recorded -- then obscured by the
  substitution (audit CLM-028 / section 10.5).
- **Branch CLOSED under RESEARCH-DIRECTOR.md section 31.** A stop condition ("literature shows the
  claimed result is already standard" + "the observable is analytically fixed by existing data") had
  been met and was not declared. It is declared here. Reusable output: the puMPS + ED-gate +
  element-dominance pipeline, the d=3 plateau-accept discipline, and the predictive use of two-error
  cancellation.

---

## 2026-08-11 (cont.) -- SIM-2026-070: HYP-028 Phase 1, PAPER-133 reproduced at ED scale

Gate before frontier. Sparse-ED reproduction of PAPER-133 (2606.16785v2 -- the v2 changelog was
diffed first, per the scan-#19 flag) on the periodic PT-symmetric Ising chain
`H_YL = -sum(sz sz + lambda sx + i h sz)` at lambda=4, driver `yanglee-pt/qw_yanglee_pt.jl`.
Finite-size exceptional points h_c^L by bisection on Im(E), L = 8..18; working point
**h_c^inf = 1.5587127** from a fixed-exponent fit (b = 12/5 + L^-4 subleading). Biorthogonal
projections at that point (PT-unbroken at every finite L), L = 8..20:
- **R_inf = -1.61820 vs -(1+sqrt5)/2 = -1.618034 (0.01%)**;
- **g_1 = 0.725347 vs 0.725073 (0.04%)** -- and matching PAPER-133's own 0.725339(51) to 0.16 sigma;
- **Z_1 negative at every L** -- the unitarity-forbidden sign, reproduced with plain sparse ED plus
  the eta=parity left-pairing.
Estimator lessons that then governed Phase 2: h-sensitivity grows as L^{12/5}, so h_c^inf precision
limits everything before anything else; wide-window polynomial extrapolation in 1/L overshoots
(free-power fits gave -1.75), and pairwise-linear intercepts + Richardson on the intercept sequence
is the stable estimator at these sizes.

**AUDIT 2026-08-17 (backfill).** This is the cleanest record in the program -- raw logs committed,
the near-zero counterfactual novelty labelled as such -- and it still carries three caveats that
were not stated on the day: the tracked driver's own gate prints `GATE: NOT PASSED` for the run of
record; the 0.01% requires selecting the **last** of a monotonically **rising** ratio sequence (the
mean ratio gives 0.21%); and the deviation is quoted against the exact value rather than against the
paper being reproduced, from which our X-prep R_inf differs by **3.87 sigma**. Worse, and only found
in the audit: **PAPER-133 Table S1 publishes h_c^inf = 1.55872195(5)** for lambda=4. We fitted
1.5587127 in-house from our own shorter L-range -- a gap of 9.25e-6, **185x the paper's quoted
uncertainty** -- and our own key_findings said this parameter has the longest lever arm in the
result. Applying our own b = 12/5 + L^-4 model to the paper's 7-point table returns 1.5587180, so the
machinery is fine; the L-range was not. A ~1-2 h re-run at the published h_c is the cheapest
high-value test the program has available (audit section 5.4).

---

## 2026-08-11 (cont.) -- SIM-2026-071: Yang-Lee biorthogonal KS -- the sign result, and a novelty gate that FAILED

Phase 2. Momentum-resolved biorthogonal sparse ED of the same chain at h = h_c^inf, L = 10..18,
driver `yanglee-pt/qw_yanglee_ks.jl`. Product-form estimator
`c_KS = 2<vac_L|H_-2|T_R><T_L|H_+2|vac_R>/(<T_L|T_R><vac_L|vac_R>) * (L/(2 pi v_T))^2` -- no square
roots, so the **sign is part of the measurement**.

**Result as recorded on the day:** `c_KS = -4.29 +/- 0.15`, negative at every L and in both
chiralities, machine-real; read as the TRUE central charge c = -22/5 = -4.400 (2.6% at ED scale),
with `c_eff = +2/5` excluded by sign and by ~11x in magnitude. Unitary control on the same code path
(MODE=ising): 0.49986 vs 0.5 (0.03%). Corroborating structure: `<1|1>` biorthogonal norm negative at
every L (the indefinite metric visible raw); the k=+-2 cluster matches the M(2,5) phi level-2
null-vector prediction exactly.

**Two discoveries that nothing predicted, and they are the durable content:**
- **The T-identification rule INVERTS at Yang-Lee.** The cross-module product to the phi-descendant
  is ~10-11x LARGER than T's and of opposite sign, where unitary chains show ~1e-4 suppressions.
  Delta-gating above the vacuum is mandatory; raw element dominance silently measures the wrong
  state. This was disclosed, not hidden, exactly as RESEARCH-DIRECTOR.md section 13 asks.
- **The conformal vacuum is |1>, the SECOND k=0 state** (the physical ground state is |phi>, with
  Delta_phi = -2/5), and it carries a negative biorthogonal norm.

**NOVELTY GATE: FAILED (recorded 2026-08-17; the claim was made on the day and is retracted here).**
The record as written asserted *"First lattice extraction (to our knowledge) of a NEGATIVE central
charge from stress-tensor matrix elements; standard approaches obtain only c_eff from Casimir
scaling"* (`SIM-2026-071.json` key_findings[2]). Both halves are wrong, and the phrasing violates
RESEARCH-DIRECTOR.md section 8 in any case. Two literature agents working from disjoint sources
converged on the same prior art without contact:
- **Io, Huang & Hsieh, arXiv:2602.02649** (v1 **2026-02-02**, six months and nine days before this
  run): non-Hermitian 1+1D critical lattice chain, biorthogonal left/right pairing, **Koo-Saleur
  Fourier modes by name**, central term of the resulting Virasoro algebra, and the value obtained is
  the **true negative c** (-2), not c_eff -- citing Koo-Saleur 1994 and Milsted-Vidal 2017, the
  identical two references this pipeline rests on. **Aggravating: it is reference [24] of PAPER-133**,
  the paper we downloaded, logged a full v2 read of, and designed this phase around, on the same day.
  The pointer was in hand and was not followed.
- **Couvreur, Jacobsen & Saleur, PRL 119, 040601 (2017)** (arXiv:1611.08506): lattice measurement of
  a negative *true* c on non-Hermitian critical chains beside the positive c_eff of the same model,
  and its introduction names our exact headline pair verbatim -- "for the Yang-Lee singularity,
  c = -22/5 but c_e = 2/5". Nine years prior, in PRL.
- **The premise is false, not merely unnovel:** complex/negative c from biorthogonal Casimir scaling
  is published (Tang et al., PRL 133, 076504 (2024); Zhou-Wang arXiv:2405.01640; Tu-Tzeng-Chang
  SciPost Phys. 12, 194 (2022)), and `c = c_eff + 24 h_min` makes c recoverable from c_eff by
  arithmetic. **Positioning sentence to use from here on:** *this is a finite-L, error-barred
  Koo-Saleur ladder in an INTERACTING non-Hermitian chain (M(2,5), c = -22/5), where
  arXiv:2602.02649 treats the free-fermion c = -2 logarithmic case analytically at an exceptional
  point and PRL 119, 040601 measures true c by left/right eigenstate entropies.*
- Neither 2602.02649 nor 1611.08506 was anywhere in this repository. The gate had been delegated to a
  forward-only weekly newsfeed that begins 2026-03-10, and no backward prior-art search on
  "Koo-Saleur" / "biorthogonal" / "negative central charge" had ever been run (audit section 4.5).

**Also corrected 2026-08-17:**
- **The +/-0.15 band is wrong by ~6x and convergence is not established (D-8).** 82% of the magnitude
  is extrapolation from a 2-sample tail ratio; the h_c^inf model choice alone spans -3.67 -> -7.04; a
  defensible pipeline zoo spans [-5.6, -2.6]; a known-answer calibration of the same estimator gives
  +/-0.86. Decisively: the **KS product element scales as L^{-1.03} where convergence of c_KS
  requires L^{-2}** (the unitary control on the same code gives L^{-2.05}), and a divergent logarithm
  fits the five points **18x better** than any 2-parameter convergent model -- which is what the
  "w -> 0 runaway" the record discarded actually was. Honest restatement: **the sign and the c_eff
  exclusion are decisive; the magnitude lies in [2.6, 5.6] and convergence is not established.**
- **The unitary control cannot defeat the interpretation it is cited for.** 148 of 152 lines are
  shared, and the line that differs sets `HC = 0.0`, making H real symmetric and the biorthogonal
  norms exactly +1 -- the mechanism under test is switched off in the control.
- **HYP-028 was advanced to SUPPORTED on a different question than it registered (D-11).** Its claim
  and refutation criteria are about a force exponent alpha at a non-unitary point; SIM-070/071
  measured no alpha at all, and the mandatory G4 gate was substituted without a recorded amendment.
  The alpha question is untested and returns to OPEN; the biorthogonal-KS proposition needs its own
  pre-registered record.
- **What survives, and it is not nothing:** the T-identification inversion (the most defensible item
  in the frontier work -- no prior statement of it was found), the negative-sign measurement itself,
  and one result proved twice independently during the audit and never claimed: **the c_KS estimator
  is exactly invariant under eigenvector rescaling and under the full pseudo-Hermitian metric family
  eta -> eta*p(H)**, which defuses one branch of the section-12 Yang-Lee killer. That is the cheapest
  publishable item in the program.

---

## 2026-08-17 -- RESEARCH-DIRECTOR.md adopted as the program's governing scientific standard

`docs/governance/RESEARCH-DIRECTOR.md` adopted as the standard every future claim is measured
against (commit `5130635`; `CLAUDE.md` repointed at it in `a82069f`). What it changes in practice:
- **Four contribution levels** (1 reproduction / 2 method / 3 new physics in an established framework
  / 4 discriminating foundational) must be assigned explicitly -- Level 1 work may not be presented
  as Level 3 or 4.
- **Counterfactual novelty** is now a required field: *before running the calculation, how many
  outcomes were genuinely possible?* A number fixed in advance by conformal symmetry or a Virasoro
  identity scores near-zero however precisely it is reproduced.
- **An independence ledger**: agreements between two transformations of the same input are consistency
  checks, and must be described as such.
- **A novelty gate** (literature + derivation + prior-art) that must be *recorded* before the words
  "novel", "first", "to our knowledge" or "unprecedented" may appear anywhere.
- **Named killer tests, matched controls, out-of-sample prediction, stop conditions**, and section 32:
  corrections are additive -- original claim, evidence at the time, challenge, corrected analysis,
  changed conclusion, all preserved. This log follows that rule from here on.
The north-star question it sets: *is MERA revealing an emergent geometry with independently testable
content, or is geometric language a reinterpretation of an efficient CFT ansatz?* -- and its first
assignment is a full audit before any new large simulation.

---

## 2026-08-17 (cont.) -- FORMAL SCIENTIFIC AUDIT: the program's real level, measured

The audit ran as a multi-agent adversarial workflow (23-agent run; **20 investigation artifacts** are
on disk under `research/data/audit/raw/`, phase 1 = eight record audits, phase 2 = twelve analysis
and adversary passes). Result: `docs/governance/AUDIT-2026-08-11.md` (commit `a2ebc91`), which
supersedes `PROJECT-REVIEW-2026-08-11.md` wherever they disagree. The findings that matter:

- **Level 4 (discriminating): zero.** No matched non-geometric control, no rewiring experiment, no
  reconstruction-locality test has ever been run here. `grep -ril "rewir" research/` returns nothing.
- **Level 3 (new physics): zero confirmed.** Two candidates -- the Yang-Lee KS sign and the L_{-2}eps
  suppression -- both failed their gate.
- **Of 34 claims involving a calculation, 21 could not have come out otherwise.** Conformal symmetry,
  a Virasoro identity, BPZ 1984, or the definition `l_AdS = 1/ln chi` fixed the answer before the run.
- **Of 24 agreements the project presents as evidence, 4 carry information not already in the
  inputs**: the Yang-Lee sign, h_c(L) vs PAPER-133's table, g_1 vs PAPER-133, and puMPS-vs-ED at
  matched N (which the project owns and mis-states as a 7% disagreement when it is 5e-6 in c).
- **25 defects registered, 11 critical.** Backfilling this log is D-24; the anchors header at the top
  of this file advertising the retracted 0.72% was part of it and is now fixed.
- **The strongest defensible contribution is methodological**: the Z2/Z3-symmetric optimizer, the
  two-phase ALM+projection VQE, the ED pre-gates, and the documented inversion of the unitary
  state-identification rule at Yang-Lee -- the one thing nothing predicted.
- **The audit corrected itself in public, and that is the template.** D-1 alleged the manuscript's
  Wang-He citation was unsupported, on the strength of *our own catalogue record* of the paper. The
  primary source was then read: the derivation is there, in Supplemental S3 A. The premise was wrong
  and the resolution box says so -- while identifying a worse defect the wrong premise had hidden
  (their t_trans = pi carries **no AdS radius at all**, so the entire 1.2% transport agreement is
  supplied by the free factor 1/ln 2). *Verify the artifact you are about to build an argument on,
  including an audit.*
- **Institutional root cause (D-22):** every finding above came from a section-27 adversarial role
  the agent team does not have. Ten of fourteen agents contain zero adversarial instruction, and the
  only gate in the pipeline asks whether an experiment is affordable -- never whether its answer was
  fixed before it ran.

---

## 2026-08-17 (cont.) -- SIM-2026-072: alpha = 3.92 WITHDRAWN as an estimator artifact; measured value is 2.6 +/- 0.2

The audit's D-2 said the central published finding was a fitting artifact. It was checked before
anything was acted on, then re-derived independently: separate driver, separate author, raw records
the only shared input (`research/tools/force-reanalysis/qw_alpha_reanalysis.py`, seed 20260817;
commit `d17b7a2`). **No new simulation** -- the three force datasets have been on disk since April.
The re-analysis reproduces the original fit exactly (3.9218 vs 3.9218 recorded) before diverging,
which rules out an implementation difference as the cause.

**What the published estimator was doing.** Unweighted nonlinear least squares on F in *linear* space,
applied to a steeply falling profile, puts **95.8% of its objective on the single point dr=2** (96.0%
and 96.3% on the two N=16 datasets). The reported exponent is, to within 8%, that one point's local
slope (4.2315) -- not a property of the profile. Changing only the error model and **discarding no
data**: relative-error weighting gives 2.822, log-space OLS 2.890. Across the 3 x 5 estimator x
window matrix the N=24 alpha spans 2.534-3.922 and **the published value is the maximum of all 15**.

**What the data actually contain.** A true power law has a flat local log-slope. The N=24 local slopes
run 2.035, **4.232**, 2.603, 2.456, 2.461, 2.533, 2.658, 2.841, 3.102, 3.482, 4.064: a spike at dr=2
and a rise at the far end bracketing **a genuine intermediate plateau -- six consecutive slopes flat
to +/-7.5%, centred on 2.592**. No dataset shows any flat region at 4. **Corrected measurement:
alpha = 2.6 +/- 0.2, exchange channel OPEN** -- 2*Delta_T = 4 and 2*Delta_eps = 2 both fall outside
the plateau band.

**Why dr=2 is the wrong anchor:** it is the unique separation at which a Hamiltonian bond bridges the
two operator supports -- a contact term. The manuscript excludes dr=1 on exactly that reasoning and
then rests its result on the next point in the same family.

**Three further consequences:**
- **The "alpha = 2 is excluded" claim does not survive at the stated significance.** ~12 sigma at the
  published +/-0.16; **~2.2 sigma** at the project's own bootstrap sigma = 0.635 (mean 3.369, which
  the manuscript never quotes); and under any dr>=3 window the point estimate itself falls to ~2.56.
- **The three "independent evaluations" fail together** (3.92->2.56, 3.97->2.75, 4.07->2.63 on
  dropping dr=2) because they share one observable, one operator, one window and one fitting routine.
  Their agreement measured the estimator, not the physics.
- **NEW DEFECT, found by the re-analysis and not by the audit:** the chi=3 MERA profile **changes
  sign** at dr=9 and dr=10, and the published chi=3 fit (dr_min=2, n_pts=10) therefore fits a
  fixed-sign power law through two points of the wrong sign. A power law cannot change sign; the
  chi=3 evaluation is invalid beyond dr=8 and its published alpha = 4.071 should not be quoted at all.

**Verdict, and why the correction is an improvement.** The withdrawn number was fixed in advance by a
Virasoro theorem -- alpha = 2*Delta_T = 4 is what conformal symmetry requires for a pure-eps probe,
so its counterfactual novelty was near-zero and only implementation failure could have shown up. The
measured number, 2.6, is predicted by neither candidate channel. It is a smaller claim and a real
open question, which is the better trade.

**Downstream (from `SIM-2026-072.json`, all required, not optional):** correction to PRD accession
DV13971 (`docs/governance/PRD-CORRECTION-PACKAGE.md`); ERRATA entry E6; HYP-2026-008 falls from
SUPPORTED, with its registered killer (V_T vs V_X channel discrimination -- never executed) now the
outstanding test; README headline and the Zenodo record inherit the withdrawn number; and
`SIM-2026-011-interaction.json`, `SIM-2026-015d.json`, `SIM-2026-017-statistics.json` each need a
`verdict_SUPERSEDED_2026_08_17` backlink to SIM-072 -- the SIM-036 -> SIM-039/040 pattern of ERRATA
D5, which remains the house exemplar for how a correction is recorded.

## 2026-08-17 -- PRD REJECTED DV13971 on 2026-08-12; discovered five days late

**The decision.** `prd@aps.org`, 2026-08-12 18:16 UTC, subject "Decision DV13971 Cackler", from
**Dr. Alin Tirziu, Senior Editor, Physical Review D** (Gmail id `19ff730cc7add0c1`; DKIM, SPF and
DMARC all pass on aps.org):

> "Thank you for your submission. Regrettably, this manuscript fails to match the minimal threshold
> for the APS journals. APS will not consider this manuscript further."

A desk rejection at the strongest tier APS uses -- no referee reports, no transfer offer to PRE or
PRResearch. Accession **DV13971 is CLOSED**. The submission itself was real and is separately
confirmed (`esub-adm@aps.org`, 2026-08-07 16:49 UTC, TEMPID `es2026jul20_951`, RECVD Fri Aug 07
12:49:40 2026), so this supersedes the 2026-08-07 entry above at line ~1031, not the fact of
submission.

**Two independent facts, recorded separately on purpose.** The rejection (08-12) PREDATES the audit
finding that the paper's central alpha = 3.92 is an estimator artifact (08-17, SIM-2026-072). Tirziu
rejected on scope/threshold grounds and there is no indication he saw the defect. Equally, the
rejection does not validate the defect: alpha = 3.92 is withdrawn on its own evidence. Any future
write-up that fuses these into "the paper was rejected because the result was wrong" is inventing a
causal link the record does not support.

**How it was missed, which is the more useful finding.** Three internal records -- memory
`paper_status.md`, `TASKS.md`, and this log at line 1031 -- all reported status "With editors". All
three were written by the same process on 2026-08-07, all agreed with each other, and none had been
checked against an external source since the 2026-08-04 inbox sweep. The reply-watcher cron from the
earlier session had expired. So a decision arrived on 08-12 and the project confidently reported the
opposite state for five days, including while drafting a withdrawal letter addressed to the editor
who had already closed the file.

This is **RESEARCH-DIRECTOR.md section 7** -- agreement among quantities sharing an origin is a
consistency check, not evidence -- occurring in the project's *operational* records rather than in
its physics, and it went undetected by the same 23-agent audit that caught the physics instance. It
was found only because Jon asked "we have editors?" and the question was answered by reading the
inbox instead of re-reading the notes. Generalized rule now recorded in NEXT-SESSION.md 0d: **an
external status is only as fresh as the last time the external source was actually read**; internal
records restate it, they never refresh it.

**Consequences.**
1. The withdrawal letter (Letter A), drafted and selected 2026-08-17, is MOOT and was never sent. It
   is retained unsent at `docs/governance/LETTER-A-WITHDRAWAL-DV13971.txt` with a do-not-send header,
   as the record of a decision overtaken by facts.
2. **Nothing is owed to APS.** There is no published or in-review journal record to correct.
3. The entire correction obligation collapses to **Zenodo** (concept DOI 10.5281/zenodo.19660302,
   v4 published 2026-07-15), now the only live public artifact asserting alpha = 3.92. The public
   GitHub repo stays un-pushed by Jon's decision the same day, so it asserts nothing new.
4. Every publication route is now blocked simultaneously: arXiv (no endorser), SciPost (silent since
   2026-04-30), PRD (rejected), direct outreach (7 targets, zero replies). The correct response is
   not another submission attempt but the corrected science -- above all HYP-2026-008's own
   never-executed V_T vs V_X killer test, which with alpha = 2.6 matching neither candidate channel
   is now discriminating rather than confirmatory.


## 2026-09-24 -- HYP-033 unblinded: SIM-2026-079, outcome 4 (smooth), Level 2

Grid finished 2026-09-23 22:18Z on pod 67iskx7js1nimw (~23 h, ~6.5 USD at pod price); fetched and verified
file-by-file (58/58 byte-identical), pod deleted. 24/24 chi-6 networks passed G1-G3; G4 primary 8/8.
All 4 chi-8 networks OOM-killed in their gates at 62 GB, so G5 is NOT EVALUABLE (Jon's ruling T1).
Jon approved I7 (G4 not applied at h = 1.5) before unblinding. Interpretations I1-I7 and T1 are in
hyp033_analyze.py and were committed before any f was printed (e82a367, c7414d8).

Seed means (v3): primary m_0.9 = 4.75/4.34, w = 7.76; C-HAAR m_0.9 = 4.62/4.62, w = 6.06; C-GAPPED
m_0.9 = 4.91/4.19, w = 7.59. m_half = 8.50 everywhere (the v3 identity, now confirmed on registered data).
Verdict: not cut-like (onset < 6 and not 3 above Haar), not cone-like, smooth. Outcome 4, which was the
stated prior. The registered test finds nothing separating the optimized network from random ones on
this graph at chi 6. Post-hoc only: optimized curves are broader and seed-asymmetric where Haar is
symmetric; untested and not claimed. Full table: research/tools/bulk-recovery/runpod_033/UNBLINDED_REPORT_v3.txt.
