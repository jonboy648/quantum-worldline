# NEXT SESSION — Start Here

**Last updated:** 2026-09-25. **Branch:** `public-release`, pushed to PRIVATE origin `quantum-worldline-archive`. The PUBLIC repo `jonboy648/quantum-worldline` is a separate one-commit snapshot (see #-4). Never push local `master` (old RunPod key); never commit .mcp.json or paper drafts .tex/.pdf/.html.
**Read order:** this file → `docs/governance/RESEARCH-DIRECTOR.md` (the governing standard) → `docs/governance/AUDIT-2026-08-11.md` → memory `MEMORY.md` → `TASKS.md` → `research/RESEARCH-LOG.md` → `research/ERRATA.md`.

---

## ⚡ HOT STATE #-4 (2026-09-24): HYP-033 UNBLINDED -> SIM-2026-079, OUTCOME 4 (SMOOTH), LEVEL 2

- Recovery onset in the optimized MERA equals Haar's (m_0.9 4.55 vs 4.62); not cone, not cut; C-GAPPED also smooth.
  G5 not evaluable (chi 8 OOM, Jon ruled T1); I7 approved by Jon. Report: `research/tools/bulk-recovery/runpod_033/UNBLINDED_REPORT_v3.txt`.
- Next: trunk-paper outline takes the outcome-4 branch (`docs/philosophy/TRUNK-PAPER-OUTLINE.md`); ask Jon re C-REWIRE (moot for a
  positive claim); post-hoc width/asymmetry difference is NOT claimed and needs its own pre-registration if pursued.
- **REPO PUBLIC 2026-09-25 (Jon: fresh public repo).** https://github.com/jonboy648/quantum-worldline is a ONE-COMMIT
  public snapshot of public-release@2a70f15 (the URL Zenodo v5 cites; JOSS six-month clock starts 2026-09-25).
  The working repo's full history moved to PRIVATE `jonboy648/quantum-worldline-archive`; local `origin` now points
  there. Histories are unrelated: to update the public repo, `git archive HEAD` into a clone of the public repo,
  commit, push. Never push the archive history (old emails/PDFs) or local `master` (old RunPod key) to the public repo.
  Third-party PDFs + correspondence are untracked and gitignored (still on disk).
- OLD RUNPOD KEY (rpa_TX2C...): still LIVE (API 200, checked 2026-10-08), only in local `master` history, on no remote.
  Jon 2026-10-08: "drop the runpod key its fine" -- do NOT raise revocation again. The one rule that keeps it fine:
  never push local `master` anywhere.
- 2026-10-15 (later): DRAFT 1 COMPLETE, ~11k words, all four checks applied (positions: 2 wrong + 10 reworded fixed;
  fact-check: 26 items verified at source and fixed, incl. PRD rejection found 08-17 not 08-23 (CLAUDE.md corrected);
  novelty gate: partial prior statements for all 3 claims, cited; paper claims only the application + combined dilemma).
  OPEN before posting: Redhead 1975 pp. 86-89 (library), read Ney 2021, Jon approves AI-use disclosure, Zenodo snapshot
  of repo for stable citations, update public snapshot repo so cited paths exist there.
- 2026-10-15: TRUNK PAPER DRAFT 1 WRITTEN: `docs/philosophy/TRUNK-PAPER-DRAFT.md` (~8.3k words, §1 and §3-§10 +
  limitations/disclosure/refs; §2 waits on the positions check). Running/landed checks: POSITIONS-CHECK (cited authors'
  positions vs texts), NOVELTY-GATE (§8 gate on the central argument), DRAFT1-FACTCHECK (numbers/quotes vs records),
  hardware refresh (gap from scan #21). 2610.00478 = Sahu, van der Heijden, Van Raamsdonk, Zibakhsh; 2610.08787 = Meng,
  Lan, Gu; both preprints, no journal (checked 10-15). Jon must approve the AI-use disclosure wording before posting.
- 2026-10-08: scan #21 done (PAPER-152..155; must-cite 152/153; next PAPER-156). Trunk-paper references ALL VERIFIED
  (`docs/philosophy/REFERENCES-VERIFIED-2026-10-08.md`, 5 corrected). HYP-033 post-hoc follow-up NOT PURSUED.
  NEXT: draft the trunk paper from `docs/philosophy/TRUNK-PAPER-OUTLINE.md` (authors/venue of 2610.00478 + 2610.08787 still to check).
- C-REWIRE DROPPED (prereg open question 5, 2026-09-24). Chapter 1 audio PAUSED by Jon 2026-09-25.

## ⚡ HOT STATE #-3 (2026-09-22): HYP-033 REGISTERED AND RUNNING ON RUNPOD. SUPERSEDES #-2 item 2.

- **Registered** (commit 03df0d0) after Jon approved the four post-G0 rules; his amendment: RunPod,
  not local. Contract: `research/tools/bulk-recovery/PREREGISTRATION-HYP033.md` (read its PRE-RUN
  SPECIFICATIONS: closure = layers 1+2 + ring-ground-state top; C-REWIRE INFEASIBLE and left out;
  cap-truncation order; entropy routes).
- **Run history (verified live 2026-09-22 21:55Z).** Attempts 1-2 died at pod create/host loss. Attempt 3
  (pod `topel5v6bm71sm`, community RTX 4090, 0.34 USD/h) finished stage 1 (20 optimized networks), stage 2
  (8 C-HAAR) and the first-network gates (G1-G3 PASS), then its HOST DIED at ~17:50Z (SSH gone, container
  stuck "awaiting_container" after a restart). Deleted 21:49Z. Attempt 4 (pod `k03odd9xsv9sao`, 62 GB cgroup, NJOBS=3) OOM-KILLED 26 of 28 grid jobs
  within minutes; only chi6_h1.50_seed8 finished. The pod script reported the kills as rc=0 (the `$?`
  after `$(date)` bug, fixed). **Attempt 5 LIVE: pod `67iskx7js1nimw`, SECURE RTX 4000 Ada, 16 vCPU,
  62 GB, 0.28 USD/h, NJOBS=1, cap 22 USD, deadline 2026-09-26T06:02Z**, `RESUME_LOCAL=1` (the fetched
  networks are reused, never re-optimized; finished points are skipped). Orchestrator log:
  `research/tools/bulk-recovery/runpod_033/orchestrator_console.log` (attempt 3's is `_attempt3.log`).
- **2026-09-23 20:21Z:** the orchestrator's ssh died at 23:29Z on 09-22 but the pod kept running (20/28
  done at 20:20Z, ~1.5-1.9 h/job). Re-watched with `reattach_033.sh` (session background task): fetches
  every 10 min, on all.done verifies pod.log md5 then deletes the pod; leaves it running if the copy fails.
  If this session is gone, re-run it with the same POD_ID/IP/PORT (IP 157.157.221.29, port 22941).
- **GRID DONE 2026-09-23 22:18Z, fetched + verified, pod DELETED (cca4c44).** 24/28: chi6 primary/C-HAAR/C-GAPPED
  all finished, G1-G3 pass on all 24. **All 4 chi8 OOM-killed in their gates (62 GB): G5 not evaluable.**
  Still BLINDED. Jon to decide: (a) I7 yes/veto; (b) chi8 on a bigger-RAM pod vs declare G5 NOT EVALUABLE
  (then edit PLANNED in hyp033_analyze.py with the reason, commit, then --unblind).
- **Analysis ready (e82a367, before unblinding):** `research/tools/bulk-recovery/hyp033_analyze.py`.
  Blinded by default; `--unblind` refuses until 28/28 finished. Interpretations I1-I7 in its docstring.
  **Jon may veto I7** (G4 clean-basin criterion undefined at h=1.5, so the gapped control enters on
  G1-G3 + ring gap only) — ask before unblinding. Trunk-paper outline: `docs/philosophy/TRUNK-PAPER-OUTLINE.md`.
- Orchestrator SIGTERM-trap bug FIXED before attempt 5 (`trap cleanup EXIT; trap 'exit 1' INT TERM`).
- **DEVIL'S-ADVOCATE FINDING, CONFIRMED (2026-09-22): the registered m_half is pinned by an identity.**
  Purity + monotonicity give m_L + m_R <= 17, so m_half <= 8.5 for ANY isometric network, and the cut
  predictor sits exactly at 8.5. An UNREGISTERED Haar network (chi=3, seed 9999) gives m_half = 8.50 on
  both edges, w = 9. m_half cannot separate cut-like from random. Weighted capacities do not move the
  cut drop (still m = 8/9). **v3 AMENDMENT APPROVED by Jon 2026-09-22 (in PREREGISTRATION-HYP033.md):**
  `research/tools/bulk-recovery/AMENDMENT-V3-PROPOSAL-HYP033.md` (report m_L, m_R and the gap; onset of loss
  m_0.9 as the primary cut-vs-random statistic; outcome 2 downgraded to Level 3). It uses only points the
  grid already produces, so the run continues. Unblind only when every network is finished or cap-truncated, then analyse under v3.
- **BLINDING: do not print f from any JSON until every planned network is finished or cap-truncated.**
  Then: gates table (G1-G3 per network, G4 from info.txt basin_clean, G5 chi8 vs chi6 aligned),
  m_half and w per network/edge, cone vs cut vs smooth verdict per the registered thresholds,
  SIM-2026-079. Cite 1701.00050 (PAPER-142), never claim its results.
- **Ask Jon after the primary result:** drop C-REWIRE, or run the weaker mirror-rewire variant.
- If the orchestrator died (no new log lines, pod still listed by `runpodctl pod list`): the pod
  keeps its state in /workspace/hyp033; reattach by ssh (key ~/.ssh/runpod_ed25519, port from
  `runpod_033/pod.json`) and fetch; the run is resumable (JSON points are skipped if present).
  ALWAYS verify the pod is deleted at the end (`runpodctl pod list` empty).

## ⚡ HOT STATE #-2 (2026-09-18): JON RULED ON FOUR THINGS. THIS SUPERSEDES #-1's "WAITING ON JON"

1. **G2 AMENDED (ERRATA D10).** Binds only where the MPO is exact: L=8, chi=256, discarded weight
   < 1e-20. Re-run through the amended `gate_G2()`: 5.2e-13, PASS. At L >= 12 G2 is NOT EVALUABLE,
   which is weaker than PASSED; write it that way in SIM-2026-078. The grid is unblocked but has NOT
   run. Before any pod: read `sim078_FEASIBILITY_L32_local.*` (local L=32, chi=128 probe, authorized
   by Jon, produces no registered number) to see whether chi=128 passes G3 and the grid fits 24 USD.
   **TRAP: `--gate` writes `sim078_gates.json` and I overwrote the never-committed original with
   it. The original numbers survive only in `sim078_gates.log`. Commit result files when made.**
2. **DIRECTION: both, bulk recovery first.** From the 2026-09-14 review
   (`research/data/audit/valuable-questions-2026-09-14/FINAL-REPORT.md`): pre-register MERA bulk
   operator recovery (causal cone vs minimal cut) with a gauge-COVARIANT killer (recovery error over
   the whole operator algebra at the bulk site, not a fixed operator) and the rewired-network control
   folded in; then the philosophy-of-physics paper on the trunk question for PhilSci-Archive.
   Pre-registration before code. No driver exists yet for insertion, recovery, rewiring or gauge orbit.
   The review's key finding: every "geometric" observable so far (F, T, Synge) is a functional of
   the exact state and never touched a network, which is why no matched control ever separated anything.
3. **SUPERSEDED: repo went public 2026-09-25 as a fresh snapshot, see #-4.** Before flipping public: tracked arXiv PDFs in research/downloads/, outreach emails, cover letter, and possible uncorrected 3.92 in knowledge-base.md / learning guides / Synge note. Original note: Jon said make it public (starts the JOSS six-month
   clock). GitHub was last pushed 2026-06-17; `main`'s README line 13 asserts alpha = 3.92 with no
   correction and 29 files carry 3.92. Going public as-is republishes the retracted headline. It
   needs a push of the corrected state first, and this file's standing rule is never push. Ask Jon.
4. **Chapter 1: Jon wants an ElevenLabs narration** rather than recording a voice note himself.
   Cost-optimized model per his 2026-09-11 ruling. See the 2026-09-18 session for status.

HYP-032 campaign cost is **9.37 USD billing upper bound**, not the ~6 USD written elsewhere in this
file (that was pod-create price; only 0.32 USD is provably this project's pod).

## ⚡ HOT STATE #-1 (2026-09-09): SIM-2026-078 WAS STOPPED AT A FAILED GATE (RULED 2026-09-18, see #-2)

**Do not start compute. HYP-032's follow-up is mid-flight and blocked by design.**

Jon approved a registered follow-up on SIM-077's one surviving thread ("pre regis fine", then "word").
`research/tools/timelike-ee/PREREGISTRATION-HYP032-B.md` was committed at `4743b8c` BEFORE any driver
code; driver `qw_tlee_mpo.py` at `a2bff9a`; runner at `302935b`; cross-size rules at `e95d9a2`.

**What ran:** the gate stage of SIM-2026-078 on a RunPod GPU-class host (16 vCPU, 62 GB, 0.28 USD/h).
- **G1 EXACTNESS PASSES.** Complex-time MPO vs exact diagonalisation at L=12 and 14: 1e-7 against a
  1e-6 bar, both parts, and the pod's exact values reproduce the stored SIM-077 numbers digit for
  digit (0.2815 / 0.3007 / 0.3180 / 0.3316 / 0.3429 at the passing point).
- **G2 SYMMETRY FAILS.** 0.056 / 3.05 / 2.99 at L=12/16/24 against a 1e-8 bar. The runner refused to
  start the grid. That is the gate working.
- **Diagnosis, after one wrong hypothesis of mine.** It is NOT branch/ill-conditioning: perturbing the
  exact tau_A moves Im S linearly (1e-12 -> 8.7e-13, 1e-8 -> 7.1e-9) and the nearest eigenvalue sits
  1.35 rad from the log's branch cut (`g2_conditioning.py`). It IS non-convergence: delta=0 is undamped
  real-time evolution, cost exponential in the evolution time. At L=8 with chi=256 the MPO is EXACT
  (discarded weight 3e-28) and G2 passes at 4e-14 -- the code path is correct. Production uses delta=5
  everywhere, where the same code is accurate to 5e-6 at chi=32. **Putting G2 at delta=0 was my
  pre-registration error.**
- **G5 was checked and STANDS.** The 5x background rule looked unsatisfiable (background 0.066 vs a
  0.2618 target at L=12, ratio 4.0) but the background decays with size (0.152 / 0.104 / 0.066 at
  L=8/10/12), crosses 5x by about L=14, and the grid starts at L=16.

**JON'S DECISION (three options, in `docs/governance/PLAN-2026-09-06.md`):** amend G2 to bind only where
delta=0 converges, recorded as a post-hoc gate change in ERRATA with the specification error named
(RECOMMENDED); or close HYP-032 on the SIM-077 negative; or run the grid with G2 recorded FAILED and
results provisional (not recommended).

**Housekeeping from this session:**
- Pod deleted, `runpodctl pod list` empty, ~1 USD of the 25 USD cap spent.
- **ERRATA D9** corrects the SIM-077 C1 summary, which described a peak measurement that was never run
  at L=14, and omitted both the 52% monotone drift under the passing window and the nonzero zero-field
  background. Chapter 13 quoted the wrong claim and is fixed.
- The ERRATA status block was stale (said PRD "with editors" after the 2026-08-12 rejection, and E6/E7
  unexecuted after Zenodo v5 published). Refreshed.
- **Two RunPod traps found by running it:** CPU pods reject any vcpuCount that is not a power of two,
  and on 2026-09-09 every CPU flavor was unavailable in BOTH clouds at 4/8/16/32 vCPU. The runner falls
  through to GPU-class hosts and uses only their cores.
- **A runner launched with `nohup ... &` from a tool call is killed with its parent** and left the pod
  billing unattended. Use `run_in_background`; `attach_sim078.sh` reattaches and always deletes the pod.
- Still owed by Jon: the voice note on story chapter 1, before the other 13 are revised.

---

## ⚡ HOT STATE #0 (2026-09-07): PLAN OF RECORD + WHAT IS WAITING ON JON

**Read `docs/governance/PLAN-2026-09-06.md` first.** Two grilling sessions fixed the purpose (answer the
origin video's question honestly; write the story) and four workstreams: Z (Zenodo v5), T (SIM-075),
S (story, after v5), HYP-032 (timelike entanglement, queued behind T).

- **Z: DONE. Zenodo v5 PUBLISHED 2026-09-07 on Jon's word: DOI 10.5281/zenodo.22080720, verified from the public API.**
  (Was: draft rebuilt, adversarially reviewed, 33/33 verified.) Single source `research/tools/zenodo-v5/notice.md`; build/verify with
  `zenodo_v5_build.py` (no publish subcommand on purpose). Waiting on: reviewer's confirmation pass,
  then **Jon reads the rendered notice, then Jon's explicit "publish"**. Nothing else.
- **DISCOVERED: the GitHub mirror `github.com/jonboy648/quantum-worldline` is PUBLIC** (last push
  2026-06-17) and its README still asserts alpha = 3.92. Zenodo was never the only public artifact.
  **RESOLVED 2026-09-07: repo made PRIVATE on Jon's word (gh repo edit; unauthenticated GET -> 404).**
- **T: SIM-075 ran at n = 16/20/24. Pre-registered verdict VOID** (`stress_test_convergence.json`):
  the local KW-even Hamiltonian density fails G4 (two-point exponent 8.5/7.7/7.2, not 4; lattice-scale
  modes dominate at these sizes) while its Koo-Saleur identification passes (structural zero 1e-13,
  Delta_T/Delta_eps 1.99). **The KW-odd partner's force is IDENTICALLY ZERO at h = 1** (1e-14, every dr,
  every n; nonzero at h = 0.9 and 2), and the force scales as the square of the KW-even admixture: the
  ring's 1.83 was a cross term inside ZZ, not the epsilon two-point function. The one pre-registered
  retry (Gaussian-smeared probes, sigma = 1.5 sites) ALSO failed G4 at 16/20/24 (smeared H two-point
  exponent 2.6/5.0/6.6, slopes -1..+30, no power law). **HYP-008 CLOSED as untestable at n <= 24;
  record of authority `research/data/simulations/SIM-2026-075.json`; HYP-008.json updated; ERRATA E8 closed.**
- **HYP-032 RAN (2026-09-07/08).** SIM-076: Level-1 VOID; **Im S == 0 EXACTLY for the literal lattice transition matrix (chiral symmetry V H V^dag = -H)**; with the paper's regulator the real part follows (c/3) log((R/pi) sin(pi T0/R)) to 2-3% at c=1/2, the imaginary part never approaches pi/12. Amendment A (four candidates, approved by Jon) ran as **SIM-077 on RunPod: all four NO -> registered Level-3 negative**. Open thread: C1 (h_z=0.02, delta=5) rises with L to 0.28 but peaks in h_z; a registered MPS follow-up at L=32..128 is the only sensible next step and is Jon's call. **RunPod lessons (cost ~6 USD):** default CPU flavor = 2 vCPU / 4 GB cap; use POD_KIND=gpu (RTX 2000 Ada 0.24/h or fallback list); the runner now fetches partials every 2 min because two runs lost finished settings to time caps.
- **Story: chapters 1-14 drafted and committed in `docs/story/` (13 written from SIM-076/077).** Each chapter lists its sources; every quotation was checked against the record. Jon's voice note on chapter 1 is still owed; nothing published. PAPER-139/140/141 catalogued (timelike EE papers).
  No code may be written before the approving commit.
- **Origin found 2026-09-06:** Instagram reel DVe5jiJj1rv (the worldline "worm" + "shadow of a 4D
  object"); transcript at repo root. Memory `user_origin_story.md` updated.

---

## 🛑 HOT STATE #1: THE HEADLINE RESULT IS WITHDRAWN (2026-08-17)

**α = 3.92 ± 0.16 is an estimator artifact, not a measurement.** Unweighted least squares in LINEAR
space on a steeply falling profile puts **95.8% of the fit objective on the single point dr = 2**.
Change only the error model, discard nothing: 2.82 (relative-error) / 2.89 (log-space OLS). Across
15 defensible estimator × window choices α spans 2.53–3.92 and **the published value is the maximum
of all 15**. The data DO hold a power law — **α = 2.6 ± 0.2**, six consecutive local log-slopes flat
to 7.5% — which matches neither 2Δ_T = 4 nor 2Δ_ε = 2. **Channel identification is OPEN.**

Record: `research/data/simulations/SIM-2026-072.json`. Driver:
`research/tools/force-reanalysis/qw_alpha_reanalysis.py` (seed 20260817, reproduces the published
3.9218 exactly before diverging — so this is not an implementation difference). Figure:
`alpha_reanalysis_figure.pdf`. **Extra defect found in the re-analysis, not in the audit:** the χ=3
MERA profile CHANGES SIGN at dr=9,10 while the published fit spans dr=2..11 with a fixed-sign model —
that third "independent evaluation" is invalid past dr=8 and its α=4.071 must not be quoted.

**HYP-008 → NOT_ESTABLISHED / low.** Its own registered killer test (V_T vs V_X channel
discrimination) was **never run** — that is now the outstanding discriminating measurement, and its
outcome is genuinely open in the §6 sense (which α=4 never was: Δ_T=2 is a Virasoro theorem).

~~PRD DV13971 needs contact~~ — **MOOT, the paper was REJECTED 2026-08-12 (see HOT STATE #2).**
Nothing is owed to APS. The withdrawal letter was drafted, chosen, then overtaken by facts; it is
retained UNSENT with a do-not-send header. **The only public artifact still asserting α=3.92 is the
ZENODO record** — a corrected v5 draft (id `22080720`, reserved DOI 10.5281/zenodo.22080720) is BUILT
and VERIFIED (14/14 pre-publish checks, correction notice merged as page 1 of the PDF) but
**NOT PUBLISHED — awaiting Jon's explicit go-ahead.**

**Governing standard adopted:** `docs/governance/RESEARCH-DIRECTOR.md` (§5 claim levels, §6
counterfactual novelty, §7 independence ledger, §8 novelty gates, §12 killer tests, §29 the trunk
question). Read it before proposing or writing up anything. Standing audit:
`docs/governance/AUDIT-2026-08-11.md` (23 agents; its D-1 is WRONG and carries a resolution box —
Wang-He's proof DOES exist, in Supplemental §S3.A, but is independent of ℓ_AdS, which is worse for us).

---

## 🔬 HOT STATE #1b: THE KILLER TEST WAS MIS-SPECIFIED (SIM-074, 2026-08-24)

**HYP-008's registered test compared a thing to itself.** At h=1 the TFIM is Kramers-Wannier
self-dual, mapping Z_jZ_{j+1} ↔ X_j — the two probes its refutation_criteria named. They are the SAME
continuum operator (energy density, Δ=1). Verified at three sizes: identical vevs to 1e-15, identical
force profiles to 1e-13, ring identity 2.4e-9 at n=24.
- **Both labels in the hypothesis are wrong.** Z_jZ_{j+1} is the energy density, NOT the stress
  tensor (that is the spin-2 Koo-Saleur object from SIM-067/068/069). X_j is its dual, NOT the spin
  primary. The real spin primary is **Z_j** (Δ_σ=1/8) and it was never in the design.
- **This voids SIM-073's operator contrast.** Its 0.337 gap / 4.5× amplitude ratio were open-boundary
  artifacts between exactly equivalent bulk operators. Its INDETERMINATE verdict stands; its signal
  was absent, not weak.
- **The correct test (Z vs ZZ) is BLOCKED by symmetry, not precision.** Z_j is Z2-odd: |GS⟩ parity
  +1, Z|GS⟩ −1, ZZ|GS⟩ +1. The energy-difference observable subtracts across parity sectors and is
  undefined for a Z2-odd probe. **Designing a valid observable is now the blocking item for HYP-008.**

**GOOD NEWS FROM THE SAME RUN (n=24 ring, chord-distance analysis):**
- **Energy-density exponent = 1.834 ± 0.033, slopes rising 1.673→1.943, power R²=0.9993 vs
  exponential 0.9190.** Consistent with **2Δ_ε = 2**, the CFT value for the operator actually used —
  the first exponent in this programme to match the prediction for its own operator. NOT 4.
  **CAVEAT: not converged.** Slopes still climbing at the window edge; the correct statement is
  "consistent with 2 from below with finite-size corrections", not "2 measured". Needs multi-n
  extrapolation before any value is quoted.
- **MATCHED CONTROL IS CLEAN** at n=16 and n=24. At h=2 nothing plateaus and the energy arms prefer
  exponential (R² 0.9966 vs 0.8979). The protocol does NOT manufacture power laws where no CFT
  exists — the failure mode that would have invalidated the whole α programme did not occur.
- **Geometry matters ~10%:** ε gives 2.592 (open chain) vs 2.353 (ring). Always state geometry AND
  distance convention (chord vs raw) with any exponent.
- Analytic gate G1 (PBC ground state vs exact free fermions) passes at 1e-15/4e-16 — a genuinely
  independent check sharing no code with the simulation.

Driver `research/tools/channel-test/qw_ring_test.py`; pre-registered `PREREGISTRATION-RING.md` (95fe3fe,
before the driver existed).

---

## ⛔ HOT STATE #2: THE PAPER WAS REJECTED BY PRD — 2026-08-12, found 08-17

**Desk rejection, no referee reports, no transfer offer.** `prd@aps.org`, 2026-08-12 18:16 UTC,
**Dr. Alin Tirziu, Senior Editor, Physical Review D** (Gmail id `19ff730cc7add0c1`, DKIM/SPF/DMARC
pass): *"Regrettably, this manuscript fails to match the minimal threshold for the APS journals.
APS will not consider this manuscript further."*

Submission itself was real and separately confirmed (`esub-adm@aps.org`, 2026-08-07 16:49 UTC,
TEMPID `es2026jul20_951`). Accession **`DV13971` is CLOSED.**

**Two independent facts — do not conflate them.** The rejection (08-12) came *before* the audit
found the alpha estimator artifact (08-17). Tirziu rejected on scope/threshold grounds; nothing
suggests he saw the defect. And the rejection does not vindicate the defect either: alpha = 3.92 is
withdrawn on its own evidence regardless of any editorial opinion.

**It went unnoticed for five days because three internal records agreed with each other.** Memory,
`TASKS.md` and `RESEARCH-LOG.md:1031` all said "With editors" — all written by the same process on
08-07, none checked against the inbox since 08-04, reply-watcher cron expired. That is
RESEARCH-DIRECTOR.md §7 (same-origin agreement is a consistency check, not evidence) reproducing
itself in our operational records rather than in the physics. See 0d below for the fix.

**Publication routes are now ALL blocked:** arXiv (no endorser), SciPost (silent since 2026-04-30),
PRD (rejected), outreach batch (7 targets, zero replies). Do not re-submit anywhere until there is
corrected science to submit.

**Outreach is exhausted as a strategy:** all 7 targets silent, inbox verified 2026-08-04, day 20. The
"~10 days then PRD regardless" deadline passed 2026-07-25 — hence the submission.

**TCI C_TTT IS MEASURED (SIM-068, 2026-08-10): 3.381 ± 0.005 vs exact 3.3806 — PASSED.**
puMPS ladder N=14..56, c_inf = 0.699 ± 0.002 vs 7/10. Ladder now Ising ✓ + TCI ✓.

**POTTS C_TTT IS MEASURED (SIM-069, 2026-08-11): 3.163 ± 0.003 vs exact 3.16228 — PASSED.**
**THE SELF-COUPLING LADDER IS COMPLETE**: Ising ✓ (SIM-067) + TCI ✓ (SIM-068) + Potts ✓
(SIM-069), all ≤0.15%. Full record: research/data/simulations/SIM-2026-069.json (ED gate,
D-systematics, the twice-caught two-error cancellation, d=3 plateau-accept discipline).

**HYP-028 PHASE 1 PASSED (SIM-070, 2026-08-11): PAPER-133 REPRODUCED.**
R_∞ = −1.61820 vs −(1+√5)/2 (0.01%); g₁ = 0.72535 vs 0.725073 (0.04%, = the paper's own
number); negative amplitude at every L. Working point h_c^∞ = 1.5587127 (λ=4). Estimator
lessons in SIM-2026-070.json (h-error amplifies as L^2.4; pairwise-intercept+Richardson,
never wide-window polynomial fits).

**HYP-028 PHASE 2 ANSWERED (SIM-071, 2026-08-11) — THE STRIKING OUTCOME:**
**c_KS(Yang-Lee) = −4.29 ± 0.15 = the TRUE central charge −22/5, sign included; c_eff = +2/5
EXCLUDED** (wrong sign, 11×). Unitary control on the same code path: 0.49986 vs 0.5. The
KS/force construction survives non-unitarity carrying true c.

> **STATUS CORRECTED 2026-08-17: HYP-028 is `OPEN` / confidence `low`, NOT "SUPPORTED (medium)".**
> The line above previously said SUPPORTED. The numerical result stands (c_KS = −4.29 ± 0.15 is a real
> measurement and c_eff = +2/5 is genuinely excluded), but the hypothesis it was advanced to settle is
> not thereby established — see `HYP-2026-028.json` → `status_change_2026_08_17` and
> `founding_premise_correction_2026_08_17`. The founding premise ("standard approaches obtain only
> c_eff") is FALSE, and the priority framing failed its §8 gate (below). Read the record, not this line.

> **PRIORITY CLAIM WITHDRAWN 2026-08-17 — §8 literature gate run, outcome FAILED (audit D-5).**
> This block previously read *"First lattice extraction of a negative c from stress-tensor elements
> (to our knowledge)."* It is not first. Biorthogonal Koo-Saleur extraction of a true **negative**
> central charge on a non-Hermitian lattice was demonstrated by **Io, Huang & Hsieh
> (arXiv:2602.02649)**, v1 2026-02-02, for free fermions at c = −2 — and that paper is reference [24]
> of PAPER-133, which this phase was designed around. Lattice measurement of true vs effective c on
> non-unitary chains is **Couvreur, Jacobsen & Saleur, PRL 119, 040601 (2017)** (arXiv:1611.08506),
> whose introduction names our exact pair verbatim: *"for the Yang-Lee singularity, c = −22/5 but
> c_e = 2/5."* What is actually ours: the construction applied to an **interacting** chain at
> M(2,5), and the documented **inversion of the unitary state-identification rule**. The companion
> premise *"standard approaches obtain only c_eff"* is also false (Tang et al., PRL 133, 076504
> (2024); and c = c_eff + 24·h_min). Full gate record: `SIM-2026-071.json` → `prior_art`.
> Neither reference is catalogued in `research/data/papers/` — catalogue both before the next scan.

Driver `yanglee-pt/qw_yanglee_ks.jl` (modes: yl / ising control). Traps discovered: T-ID
INVERTS at YL (φ-descendant cross-module product 10× bigger than T's — Δ-gate above vacuum
mandatory); vacuum |1⟩ = 2nd k=0 state with NEGATIVE biorthogonal norm.

**Next-session menu — REORDERED 2026-08-17 by the audit:**

*Blocking on Jon (do not act unilaterally):*
0a. ~~PRD DV13971 withdrawal letter~~ — **MOOT. THE PAPER WAS REJECTED 2026-08-12.** Desk reject from
    `prd@aps.org`, Dr. Alin Tirziu: *"fails to match the minimal threshold for the APS journals."*
    Accession CLOSED; a rejected manuscript cannot be withdrawn. Letter A was drafted and chosen
    before this was known, and is retained UNSENT as a record. **Nothing is owed to APS.**
    The rejection PREDATES the audit and is independent of it — do not conflate the two.
0b. **Push/tag — DECIDED 2026-08-17: HOLD, stay local.** No push, no tag. Freeze plan stays staged at
    `research/data/audit/MANIFEST-plan.md` for whenever the hold lifts.
0c. **⇒ ZENODO IS NOW THE ENTIRE CORRECTION JOB.** With the manuscript dead and the repo unpushed,
    the Zenodo record (concept DOI 10.5281/zenodo.19660302, v4 published 2026-07-15) is **the only
    live public artifact asserting alpha = 3.92.** Needs a v5 or an annotation. Token at
    `~/.zenodo-token`; record GET output is NOT PUT-safe — rebuild resource_type/creators/rights/
    subjects/publisher/related_identifiers in canonical id-shape (memory [[zenodo-doi]]).
    **Awaiting Jon's go-ahead** — it is an outward-facing publication action.

*Operational fix worth making (cheap, prevents a repeat):*
0d. **Re-arm a reply/decision watcher on joncackler@gmail.com.** The old cron expired, the last real
    inbox check was 2026-08-04, and a decision landed 08-12 that nobody saw for five days while three
    internal records confidently reported the wrong status. **An external status is only as fresh as
    the last time the external source was actually read.**

*The science that would actually move the program (all now higher-value than paper v6):*
1. **Run HYP-008's own killer test: V_T vs V_X channel discrimination.** Never executed in the entire
   program. With α=2.6 matching neither channel this is now DISCRIMINATING rather than confirmatory —
   the highest counterfactual-novelty experiment available, and it is cheap (same state, same
   energy-difference protocol, second excitation arm).
2. **Fix the transport anchor or drop it.** D-13 (χ=3 gives ℓ_AdS=0.9102 → predicts 1.430 vs measured
   2.239) and D-1-resolved (Wang-He is ℓ-independent) are both unresolved. Also D-12: the transport
   script never applies a MERA (`holographic_transport_16q.py:347` prints "Skipping full MERA bulk
   computation") — either perform the computation or state it.
3. **§29, the trunk question**: what operational content does emergent geometry add beyond an accurate
   CFT tensor-network representation? The audit's §24 word test (delete "geometric", lose nothing)
   currently answers "none". A GEO-1 gauge-transformation slice is the concrete first probe.
4. **Phase 3 interpretation** (unchanged, still interesting): C_TTT = 2√2/√c imaginary at c<0 — what
   the force construction means without reflection positivity; the anomalously large φ-descendant
   cross-module element as its own observable.
5. Scan #20 (DUE); PRD watch (DV13971) continues.
6. ~~Paper v6 planning~~ — **deferred.** Do not start a second paper while paper 1 is uncorrected.

### Shell gotcha (bit three times 2026-08-11)
**Backgrounded Bash commands do NOT inherit the session's persisted cwd** — they reset to the
repo root. EVERY `run_in_background` command needs its own explicit `cd` (the MERAKit "explicit
cd in the same command" rule applies doubly to background jobs). Symptom: julia "No such file",
stray empty logs at repo root.

### Browser-automation gotchas learned 2026-08-07 (save hours next time)
- **File uploads via the Playwright Chrome-extension relay are BLOCKED** — `DOM.setFileInputFiles:
  Not allowed`. Asymmetry discovered: a file chooser opened by a **programmatic** click always
  refuses; one opened by a **human** click accepts `setFiles`. Most reliable fix is still: user
  disconnects the extension, does the upload natively, reconnects.
- While the relay is attached, a human clicking "Choose File" sees **nothing happen** — Playwright
  swallows the native dialog. Do not let the user click repeatedly; each click queues another chooser
  and they block every other tool until drained (`browser_file_upload` with paths omitted = cancel).
- **PhySH tagger: the shadow root is OPEN**, so Playwright locators pierce it natively. The earlier
  "★ won't click" conclusion was wrong — it failed because of JS `dispatchEvent` (untrusted) and a
  too-small viewport ("element is outside of the viewport"). **Resize to ~1400x1000 first**, then
  click the `label[for=...]`, not the visually-hidden checkbox.
- The tagger returns results by `postMessage` to `window.opener`, so it must be opened **from** the
  APS page. Terms reached the hidden field `#taxonomyDataField`; the page's own setter is
  `window.taxonomyUI._setData(data)`.

## Where the science stands (2026-08-06)

**Science is NOT in a clean resting state — see HOT STATE #1. Below is the pre-audit picture,
corrected inline:**
- **Universality ladder**: Ising c=1/2, TCI c=7/10, Potts c=4/5 — full conformal towers measured
  cleanly (SIM-051/052/062/063), and *that* part holds: the scaling dimensions are accurate to ~0.2%.
  ~~all α=4~~ — **the α=4 reading is WITHDRAWN (HOT STATE #1)**. HYP-025 and HYP-027 were downgraded
  to NOT_ESTABLISHED on 2026-08-17 for exactly this reason: their universality claims compared a force
  exponent measured at Ising against scaling dimensions measured elsewhere, and the Ising anchor is
  gone. What survives is "the pipeline reproduces CFT data across three classes" — a Level-1/2
  validation, not a universal force law.
- **OPE measured**: C_σσε = 0.50 ± 0.03 (placement-average; drift RESOLVED as kinematic placement systematic, see SIM-064 closeout; 0.6% precision at χ=12).
- **Paper v5** (`research/paper-draft-scipost.tex`, LOCAL): ERRATA E1–E5 applied, Potts + measured OPE folded in, compiles clean via MiKTeX in `research/submission-package/`. Zenodo v4 PUBLISHED 2026-07-15 (10.5281/zenodo.21381474) — public record now matches v5.

## Task queue (in the session task system — TaskList to see live state)

1. **PRD submission IN FLIGHT.** Package at `research/submission-package/prd/` (RevTeX 4.2, 13-pp, compiles clean). APS account created 2026-07-20 (credentials in gitignored `CREDENTIALS-APS.local.md`), draft **`es2026jul20_951`** built through 5 of 8 steps, status "Awaiting submission". **A real defect was found and fixed 07-20:** the manuscript cited a *version* DOI (19661227) instead of the concept DOI; `paper-prd.tex` line ~618 now cites **10.5281/zenodo.19660302** and the PDF was recompiled (13 pp, 0 undefined refs). **That corrected PDF has NOT yet been uploaded to the portal.**
2. **Outreach COMPLETE and EXHAUSTED.** 2026-07-15: Orth, Swingle, Sahay, He, Czech, QuEra follow-up. 2026-07-19: **Evenbly SENT by email** (id 19f7b83871458f9c — his contact page publishes glen.evenbly@gmail.com, there is no form; he is now at AWS Center for Quantum Computing). Iadecola silent through the deadline, branch closed. **ZERO replies as of 2026-08-04** (inbox verified: 80 messages since 07-19, no target, no APS, no SciPost). Remaining: verify the reply-watcher's Gmail connector is on joncackler@gmail.com; user to discard 6 stale drafts.
3. **DONE 2026-07-15: Zenodo v4 PUBLISHED** — 10.5281/zenodo.21381474 (v5 content + changelog). API token at `~/.zenodo-token` (deposit scopes, joncackler account). Gotchas in memory [zenodo-doi].
4. **Scans #16/#17/#18 DONE.** #16 (07-19): PAPER-137, HaPPY code on trapped-ion hardware, FLM confirmed experimentally. #17 (07-21): EMPTY window, but 3 query lines were silently dropped by the arXiv rate limiter and had to be re-run by hand — **fire theme queries SEQUENTIALLY, never in parallel**. #18 (07-27): PAPER-138 (2607.21536, Chou) advances the non-unitary cMERA route for HYP-028 but does NOT unblock the G4 gate; sequential fix held, zero dropped lines.
   **#19 DONE (08-09):** 13-day window, EMPTY — no new IDs, no anchor contradictions. Two WATCH
   (2608.02716 measurement-altered Ising/TCI; 2608.04083 PT-Kondo g-theorem). **Query gotcha: arXiv
   stems "puMPS" → "pump"** — use `abs:"Koo-Saleur"` or `abs:"periodic uniform matrix product"`.
   **Current high-water (verified on disk 2026-08-17): PAPER-138 · HW-074 · HYP-031 · SIM-072**
   → next PAPER-139 / HW-075 / HYP-032 / SIM-073.
   **Scan #20 is DUE** (was ~2026-08-16). **Catalogue first:** arXiv:2602.02649 (Io-Huang-Hsieh) and
   arXiv:1611.08506 (Couvreur-Jacobsen-Saleur) are cited in our records but have no PAPER- record.
5. **C_TTT: Route A CLOSED (SIM-066, honest negative, 07-16); Route B ISING PASSED (SIM-067, 07-19)**: circle/Koo-Saleur matrix-element route, `research/tools/cttt-circle/qw_cttt_circle.py` — Ising C_TTT = 3.9936 vs 4.000 (0.16%), C_sse pin 0.49996, structural-zero chirality gate. TCI/Potts blocked on system size (L₋₂ε contamination ~N^-0.2; ZMV PRL 121 230402 needed N≤128 puMPS on the same OF model). NEXT: **no public puMPS package exists** (verified 07-20: amilsted has evoMPS/Python + ITensor tooling only; the earlier 'vendor amilsted/puMPS' note was an unverified search artifact). Must either implement puMPS from ZMV arXiv:1710.05397 (ansatz Tr(A^s1..A^sN) + Bloch excited states, momentum-resolved) or evaluate MPSKit.jl / ITensorInfiniteMPS.jl. Also DEAD (tested 07-20): c = 2||H_-2|0>||^2 ground-state-only route (UV-divergent, c grows ~0.5N) and summing elements over the near-degenerate |s|=2 doublet (overshoots). The single-state matrix element remains the right filter; only N is the blocker. Design + addenda: `research/tools/merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md`.
6. **DONE 2026-07-15: QuEra follow-up SENT** (id 19f66abc1559dc3f; own-thread quirk on our side, threads by subject on theirs).

## Standing gotchas (verified)

- MERAKit: Julia 1.8 via `+1.8`, clean HOME (`research/tools/juliahome`), `OPENBLAS_NUM_THREADS=1`, direct-init at target χ (ramp → LAPACKException). Long scripts to FILE, not inline (PowerShell mangles `'`).
- OPE discipline: identify σ/ε by PARITY CLASS never dimension; ≥3 clean basins before declaring a pass; C_σσσ=0 is the cheap Z2 correctness probe; quote placement-averaged C's.
- arXiv MCP search is QUERY-BLIND → arXiv export API via WebFetch for topical search.
- RunPod: standing end-to-end auth; verify costPerHr/gpuCount after spin; kill + verify `[]` when done.
- Email: NEVER send without explicit "send"; NO em dashes ever.
