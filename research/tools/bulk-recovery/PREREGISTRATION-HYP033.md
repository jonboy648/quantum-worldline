# Pre-registration: bulk operator recovery in an optimized MERA, causal cone versus minimal cut

**Status: REGISTERED 2026-09-22.** Design approved by Jon 2026-09-21 ("you are approved", thresholds included). G0 ran 2026-09-21 (result below, values blinded). The four post-G0 rules were approved by Jon on 2026-09-22 ("I approve"), with one amendment from Jon in the same message: compute runs on his RunPod account, not local (rule 4 and the Compute section were rewritten to say so BEFORE any network was built). From this commit on, nothing in this document changes except the results section and the closing of listed open questions; any other change is a new version, re-approved by Jon. Committed now so the design carries a timestamp that predates all tensor code. The only code that predates this commit is `g0_window_count.py`, a graph-only count with no tensors and no physics numbers, approved by Jon the same day.

**(Superseded by the G0 result below.) Known G0 risk, stated before G0 ran (lead's arithmetic, 2026-09-21):** at k = 2 the regions A_m have up to 17 sites. A dense reduced state on 17 sites is 2^17 by 2^17, about 275 GB complex, and the complement route needs 2^10 times chi^4. Dense von Neumann entropies therefore look feasible only for roughly |A| <= 13, which is m >= 4, and that excludes the cone end of the family where the cone predictor puts its drop. G0 must settle whether (a) Renyi-2 by replica contraction covers m = 0 to 3, (b) an MPS-style contraction gives von Neumann there, or (c) the design has to change. If the design changes, this document is revised and re-approved, not quietly edited. Hypothesis id reserved: HYP-2026-033.
Origin: `research/data/audit/valuable-questions-2026-09-14/FINAL-REPORT.md`, proposal P4 with P1's
control folded in. Jon ruled "both, recovery first" on 2026-09-18.

## Why this experiment and not another

Every quantity this project has called geometric (force F(dr), transport T, Synge chord distance) is
a functional of the exact boundary state. The drivers never contract a network. A control that swaps
the representation cannot separate representations on such a quantity. This experiment measures
something only a network has: how information inserted on an **internal leg** reaches the boundary.
It orbits the trunk question (RESEARCH-DIRECTOR section 29) directly.

## BLOCKING GATE before registration: prior art (RESEARCH-DIRECTOR section 8)

Verified against the arXiv API on 2026-09-18:

- **arXiv:1701.00050, Kim and Kastoryano, "Entanglement renormalization, quantum error correction,
  and bulk causality."** MERA as an encoding circuit for approximate error-correcting codes; logical
  information better protected against erasure at larger scales; an approximate holographic code
  emerges at criticality. **Not cited by any of the four review agents and not in our catalogue.**
  It may fix the answer analytically in terms of the scaling superoperator's spectrum. If it does,
  the outcome count below collapses toward 1 and the claim level drops to 1 or 2.
- arXiv:1504.06632, Bao, Cao, Carroll, Chatwin-Davies: consistency conditions against AdS/MERA.
- arXiv:1812.00529, Milsted and Vidal: MERA's rigorous geometry is a light cone, not hyperbolic.
- arXiv:1601.01694, Hayden, Nezami, Qi, Thomas: random tensor networks obey minimal-cut recovery at
  large bond dimension. This is why the Haar control below is mandatory: a minimal-cut pattern that
  also appears with random tensors is a property of the graph, not of the CFT.
- arXiv:1503.06237, Pastawski, Yoshida, Harlow, Preskill: exact holographic codes, the reference
  for what wedge recovery looks like when it is exact.

**Done 2026-09-21.** Read in full by one Opus agent; the lead then verified the key quotes against the PDF text. Catalogued as PAPER-2026-142, with its source for the observable, arXiv:1610.06169, as PAPER-2026-143 (abstract only, not read). Outcome count stays at 4; claim level per outcome is fixed below.

## FINDINGS BEFORE REGISTRATION (2026-09-21). These changed the design. The body below was revised to match on 2026-09-21 (v2).

**1. Prior-art gate: PASSED with constraints (agent read of arXiv:1701.00050 v2, full text; the lead
then verified these quotes against the PDF text: the nu definition, Lemma 3, the wedge sentence, the
scaling-dimension-gap disclaimer, the free-fermion remark, "polynomially small error", the Cantor-set
line and the nu to infinity caveat. The agent's numbers for nu, C and "vacuous at three layers" are
its own arithmetic and are not relied on).** Full report: `PRIOR-ART-1701.00050-agent-report.md`. The paper proves upper
bounds on recovery error controlled by nu = -log2(Re lambda_1) of the scaling superoperator. It gives
no lower bound, so it is silent on WHERE recovery fails, which is the registered statistic. It calls
entanglement-wedge reconstruction in its framework open. Its bounds are vacuous at three layers
(agent's arithmetic). Pre-empted, cite and never claim: depth-monotone protection, "critical MERA is
an approximate holographic code", and the decoupling observable itself (their Lemma 3 / Theorem 1,
from arXiv:1610.06169). Small nu (Ising Delta_sigma = 1/8) argues for a SMOOTH f(A_m): outcome 4 is
now the expected outcome, with this reason stated.

**2. Graph-only window count (Jon approved computing this before registration, 2026-09-21).**
`g0_window_count.py`: ternary periodic network, unit capacity per bond, no tensors. Result, identical
at N = 27 and N = 81 and for every position x:

| reference | f(A_m) from the min-cut predictor, sites dropped from either edge | f(complement of cone) |
|---|---|---|
| R_low (lower open end) | 1 for m <= (|C|-1)/2, then 0. k=1: m<=2 of 5. k=2: m<=8 of 17. k=3: m<=26 of 53 | 0 |
| R_up (upper open end) | 0 for every m | 1 |
| both, as this draft defines R | 0.5 then 0 | 0.5 |

**3. DESIGN ERROR FOUND in this draft.** With R attached to BOTH open ends, the upper half R_up holds
the level-k site of the ordinary MERA state. It is correlated with the whole boundary through the top
of the network, not with the cone. Consequences:
- f(C(b)) = 1 is NOT a structural identity. Only the R_low half is recovered from the cone.
- **G1 as written ("A disjoint from C(b) gives I(R:A) = 0") would FAIL**, for the same kind of reason
  SIM-078's G2 failed: the gate was written before the object was worked through.
- I(R_up : A) is a functional of the level-k state, the same "state functional" trap the
  2026-09-14 review identified. Only R_low measures how the network carries an inserted leg.
**Required revision: register R_low alone (R_up kept as a purifier and traced with the complement),
restate G1 for R_low, restate G2 as I(R_low:A) + I(R_low: complement + R_up) = 2 S(R_low).**

**4. The discriminating window is NOT empty** (the agent's worry, checked). For R_low the cone
predictor puts the drop at m = 1 and the cut predictor puts it at about half the cone: 2 sites of
separation at k = 1, 8 sites at k = 2. **Register k = 2, not k = 1.** Caveat: equal capacities and a
0/1 answer; at chi = 6 to 8 the real curve will be smooth, and the honest statistic may need to be
the half-height location rather than "largest single drop".

## G0 FEASIBILITY RESULT (2026-09-21). PASSES at chi = 6 with one declared gap; PARTIAL at chi = 8.

Script `g0_feasibility.py`. Exact von Neumann entropies without ever building rho_A: split the network
along a minimal weighted cut, contract each side against its conjugate into a D x D Gram matrix, and
take the spectrum of GR^T GL through two Hermitian eigenproblems. Validated against a brute-force dense
state on a 9-site network: max entropy difference 1e-15, f(cone) = 1, f(outside cone) = 0.
**Blinding:** G0 uses Haar-random tensors, which is one seed of C-HAAR. The script neither prints nor
saves f. No one has seen a value.

**Correction to the lead's earlier arithmetic:** the SIM-061 pipeline blocks two spins per site
(`ising_hamiltonian(block_size = 2)`), so the physical dimension is 4, not 2. All numbers below use 4.

| region edge (m, either side) | cut dimension D, chi 6 | chi 6 status | D, chi 8 | chi 8 status |
|---|---|---|---|---|
| block-aligned: 0, 2, 6, 8 and up | <= 3456 (m=7: 9216) | RUN: 46 s, < 1 GB | <= 8192 (m=7: 16384) | planned 1 GB, not run at d=4 |
| one site off: 1, 3, 5 | 13824 | RUN: 587 s and 2025 s, peak 14.6 GB | 32768 | 16 GB matrices, NOT feasible locally |
| m = 4 | 55296 | 45 GB matrices, NOT feasible | 131072 | impossible |

An earlier attempt at m = 1 was stopped by the operating system for low memory while other programs
were open; the lean Hermitian routine was written after that and is what the table reports. Heavy
points need about 15 GB free.

**Registration rules that follow from G0 (proposed by the lead 2026-09-21, APPROVED by Jon 2026-09-22, rule 4 amended to RunPod on his instruction):**
1. **chi = 6 is the primary grid**: every m from 0 to 16 from both edges EXCEPT m = 4, which is
   declared missing now, before any result. m_half interpolates linearly across it.
2. **chi = 8 is used only for gate G5**, on the block-aligned points m = 0, 2, 6, 8, 9, ..., where it is
   feasible. G5 becomes: m_half from the chi = 8 aligned points agrees with m_half from the SAME
   aligned subset at chi = 6 within 2 sites.
3. **Top of the network.** The SIM-061 pipeline optimizes an infinite scale-invariant MERA, which has no
   top. The 27-site state uses its two transitional layers plus one copy of the scale-invariant layer,
   closed by a top tensor defined as the ground state of the Hamiltonian ascended through those three
   layers onto the final 3-site ring. Fixed now; not tuned afterwards.
4. **Cost (amended by Jon 2026-09-22: RunPod, not local).** G0 measured about 3 hours per network at
   chi = 6 on the local machine (8 heavy points at 10 to 35 minutes, peak 15 GB). With 8 seeds and
   three controls (8 + 8 + 8 + 8 = 32 networks) that is roughly 100 local-machine hours. Jon ruled
   that this runs on his RunPod account instead. Rules: CPU pod (the work is dense LAPACK, no GPU
   code exists), hourly price stated to Jon before the pod is created, hard cap 25 USD, the pod is
   stopped when the grid finishes or the cap is reached, whichever is first. If the cap would cut the
   grid short, the seed count for the heavy points is reduced BEFORE the run starts and recorded here,
   never after. Every result file carries the pod id and the wall time.

## PRE-RUN SPECIFICATIONS (2026-09-22, recorded before any network was optimized; flagged to Jon)

These close ambiguities found while writing the driver. None changes a threshold, a region, a bond,
a chi, or a statistic. Each is stated here so it cannot be tuned afterwards.

1. **Closure of the 27-site network (clarifies rule 3, whose wording was inconsistent).** 27 = 3^3.
   A ternary layer maps 27 -> 9 -> 3 sites; a third layer would map 3 -> 1 site, and a 2-site
   Hamiltonian on a periodic 1-site ring is not defined. So the state uses layers 1 and 2 (the two
   TRANSITIONAL layers of the SIM-061 optimization) and closes on the 3-site ring with a top tensor
   T[a,b,c] = ground state of H_ring = sum over the three ring bonds of H2, where H2 is the Ising
   Hamiltonian ascended through layers 1 and 2 (MERAKit `ascend(h, m, 3, 1)`, the average of the
   three ternary channels). The scale-invariant layer's tensors are NOT part of the state; they enter
   only through gate G4 (the sector-resolved scaling dimensions are computed from the symmetric MERA).
   The registered bond b = top leg of the layer-2 isometry at x = 1, which is leg x of T; R_up
   attaches there. Cut dimensions are identical to the G0 table (the top tensor has the same three
   chi-legs the G0 top isometry had). The ring gap E1 - E0 is recorded per network; a degenerate ring
   ground state (gap < 1e-6) makes the network UNCONVERGED and excluded, decided now.
2. **C-REWIRE is infeasible at k = 2 with exact von Neumann entropies and is LEFT OUT of this run.**
   Any reconnection that changes the graph non-locally destroys the locality the cut-Gram method
   relies on. Plan-only cut dimensions for the registered intervals (chi = 6, d = 4):
   layer-1 direct inputs shifted by 3 blocks: D(A_1) = 5.7e7 (G0: 13824); shifted by 1 block:
   D(A_1) = 221184, D(A_0) = 55296; layer-2 direct inputs shifted by 1: D(A_1) = 331776. All beyond
   the 45 GB point already declared missing. This is a G0 failure for the control, reported as such.
   Two ways forward, for Jon to pick AFTER the primary result (neither is run now, so neither can be
   chosen to fit a result): (a) drop C-REWIRE, the result then rests on C-HAAR and C-GAPPED for the
   "graph versus state" question; (b) a mirror rewiring (swap the two outputs of every layer-1
   disentangler), which keeps every cut dimension identical to the primary but is only "same graph up
   to reflection, tensors in the wrong places", a weaker control than the one registered.
3. **C-HAAR top tensor.** Haar-random complex Gaussian vector on the 3-site ring, normalized
   (`hyp033_haar.py`, seeds 1000000 + 1000 chi + seed). Everything else in C-HAAR is the G0 build.
4. **chi = 8 seeds: 4** (as in SIM-061), used only for gate G5 on the aligned points. chi = 6: 8 seeds
   primary, 8 seeds C-HAAR, 8 seeds C-GAPPED.
5. **Entropy routes (both exact, both validated against brute force at 1e-15 on N = 9).** For
   D > 1024 the spectrum of GR^T GL is taken as the spectrum of L^dag GR^T L with GL = L L^dag
   (Cholesky), and, for Z2-covariant networks, separately on the two parity blocks of the cut legs
   (parity is diagonal in the densified sector-ordered basis; the off-block leakage is measured per
   entropy and must be < 1e-10 relative, otherwise the full matrices are used; measured 1e-17 on a
   densified chi = 6 network). C-HAAR has no symmetry and uses the full matrices. The G0 dense route
   remains the fallback when Cholesky fails. Every JSON point records its route and leakage.
6. **Order of operations on the pod.** Stage 1 Julia optimizations (SIM-061 pipeline, unchanged code
   path, seeds 1..8), stage 2 C-HAAR generation, stage 3 gates then grid, network by network, with the
   first primary network's G1-G3 as a go/no-go before any other network starts. f is written to JSON
   only and not printed anywhere until the whole grid is fetched.
7. **Cost estimate and cap-truncation order.** Local timing (24 threads, 421 GFLOPS zgemm): eigvalsh of
   4096 takes 7.8 s, so the D = 13824 block-diagonal Z2 route costs about 2 minutes per heavy point
   and the full-matrix C-HAAR route about 7; a chi = 6 Z2 network is about 16 minutes, a C-HAAR
   network about 40, locally. On a 16-vCPU GPU-class host at 0.28 USD/h (SIM-078's rung, roughly a
   third of the local throughput) the whole plan is about 33 pod-hours, about 10 USD, inside the
   25 USD cap. All seed counts stay at their registered values. Should the cap still cut the run
   short, the loss is taken in this pre-declared order, whole networks at a time, from the end:
   chi = 6 primary seeds 1..8 run first, then C-HAAR 1..8, then C-GAPPED 1..8, then chi = 8 seeds
   1..4 (gate G5). Nothing is re-ordered after the run starts.
   Measured before launch on the heavy point D = 13824 (local, 24 threads): G0 dense route 656 s;
   Cholesky full-matrix 325 s, agreeing to 1.8e-15; Z2-block Cholesky on a densified chi = 6 network
   114 s, leakage 1.1e-14, peak 11.7 GB.
8. **Pod actually obtained (2026-09-22 17:16 UTC, third attempt; the first two are in
   `runpod_033/orchestrator_console_attempt{1,2}.log`).** Community-cloud RTX 4090 host bought for its
   cores: 85 vCPU, 167 GB, 0.34 USD/h, pod `topel5v6bm71sm`, cap 25 USD = 73.5 h, deadline
   2026-09-25T18:48Z, NJOBS = 4. Attempt 1 (RTX 4000 Ada, 0.28 USD/h) ran about five minutes and was
   deleted after a bootstrap failure (tar ownership), cost about 0.02 USD, no physics run.

## The object

Ternary MERA for the critical transverse-field Ising chain, Z2-symmetric optimization then
densified, the validated SIM-061 pipeline (`qw_ope_pev_z2.jl`). chi = 6 and 8. Finite depth, three
layers, periodic.

**Bulk site.** A bond b between layer k and layer k+1 at horizontal position x. Cutting it leaves a
tensor with two open indices. Inserting an operator O contracts them with O. The boundary state is
linear in O, so the network defines a linear map from the chi-squared-dimensional operator space on
b to boundary states.

## The registered observable (gauge-invariant by construction)

Cut bond b. Attach a reference to each open end: `|Phi> = sum_ab |a>_Rlow |b>_Rup (x) |Psi^ab>`,
normalized, where a labels the LOWER open end (the leg feeding the network below b) and b the UPPER
one. **The registered observable uses R_low only.** R_up is kept as a purifier and is always grouped
with the complement. For a boundary region A the observable is **I(R_low:A)**, reported as
`f(A) = I(R_low:A) / 2S(R_low)`. The global state on R_low, R_up and the boundary is pure, so
`I(R_low:A) + I(R_low: complement of A, R_up) = 2S(R_low)`. f = 1 means the algebra on the inserted
leg is fully recoverable from A; f = 0 means A learns nothing about it.

**Why R_low only (v1 error, found 2026-09-21).** R_up holds the level-k site of the ordinary MERA
state. It is correlated with the whole boundary through the top of the network, so I(R_up:A) is a
functional of the state, the trap the 2026-09-14 review named. v1 attached R to both ends; its G1
would have failed and its "f(C(b)) = 1" was not an identity. For R_low it is: the layers below b are
isometries, so C(b) recovers R_low exactly. That is a code check, not evidence.

**Why this and not a fixed operator.** A gauge transformation U on bond b maps O to U-dagger O U. A
recovery error for one fixed O changes under U by construction, so a "randomize the gauge and see if
it moves" control would fire every time and prove nothing (the challenger's correction to P4). Under
the same U on the lower end, R_low is rotated by a local unitary and I(R_low:A) is exactly invariant.

Von Neumann entropies where the dense reduced state fits in memory. Where it does not, the Renyi-2
version via replica contraction, labelled as such and never mixed with von Neumann points in one fit.

## The two predictors

For bond b and an interval A:

- **Cone.** C(b) is the set of boundary sites whose reduced state can depend on O. Cone-only
  ("the network is a circuit") predicts f(A) depends on A only through its overlap with C(b), falls
  as soon as any footprint site is dropped, and has no threshold tied to the cut.
- **Cut.** gamma_A is the minimal cut of A in the network graph. Cut ("entanglement wedge")
  predicts f(A) is near 1 while b lies on A's side of gamma_A and drops when the cut flips past b.

**The discriminating family.** A_m = C(b) with m sites removed from one edge, m = 0, 1, 2, ..., run
from the left edge and from the right edge. Registered bond: **k = 2** (output of a second-layer
isometry), |C(b)| = 17 boundary sites. The graph count (`g0_window_count.py`, unit capacities) puts
the cut predictor's drop between m = 8 and m = 9 and the cone predictor's at m = 1: eight sites of
separation. At k = 1 the separation is two sites, too narrow; k = 1 is run as a secondary point only.

**Registered statistic.** m_half: the smallest m at which f(A_m) < 1/2, linearly interpolated, averaged
over the two edges. "Largest single drop" (v1) is dropped because a smooth curve has no meaningful
largest drop. Alongside it, the registered sharpness w = (m at f < 0.1) minus (m at f < 0.9).
Cone-like: m_half <= 2. Cut-like: m_half in [7, 10]. Smooth: w > 6 regardless of m_half.

## Gates (a failed gate is reported, never worked around)

- **G0 FEASIBILITY, run before this document is finalized, not after.** Show that f(A_m) can be
  computed at the registered chi, k and region sizes within memory and a stated time. SIM-078's G2
  failed because this check came after registration (ERRATA D10). No gate may be registered at a
  setting that has not been shown to converge.
- **G1 STRUCTURAL ZERO AND ONE.** For A disjoint from C(b), I(R_low:A) = 0 to 1e-10, and f(C(b)) = 1 to 1e-10. The isometry constraints
  force this; it is a code check, claim level 1, zero novelty.
- **G2 PURITY SUM.** I(R_low:A) + I(R_low: complement, R_up) = 2S(R_low) to 1e-8 wherever both sides are computable.
- **G3 GAUGE INVARIANCE.** Apply a Haar-random unitary on the lower end of bond b, recompute: f changes by < 1e-8.
  This must pass. If it fails the observable is wrong, not the physics.
- **G4 BASIN.** At least 6 of 8 seeds in the clean basin by the SIM-061 spectrum criterion
  (select by spectrum, not by energy).
- **G5 DIMENSION.** The statistic m_half is stable (within 1 site) between chi = 6 and chi = 8, or the point is
  UNCONVERGED and excluded.

## Matched controls (RESEARCH-DIRECTOR section 19)

- **C-HAAR.** Same graph, same dimensions, Haar-random isometries and disentanglers. If m* tracks
  the cut here as well, the pattern is a property of the graph (known from 1601.01694), not of the
  critical state, and the result is Level 2 at most.
- **C-REWIRE** (P1, rebuilt). Same optimized tensors, bonds within a layer reconnected by a fixed
  registered permutation. This changes the state, so it is not a same-state control, and is
  registered as "same tensors, different graph" and nothing stronger.
- **C-GAPPED.** Same pipeline at h = 1.5. Tests whether any cut-tracking is tied to criticality.

## Genuinely possible outcomes (prior-art gate recorded 2026-09-21: count stays at 4)

1. m* tracks the cone: recovery needs the whole footprint. The network is a circuit. Level 3 negative.
2. m* tracks the cut in the optimized MERA **and not** in C-HAAR at the same chi. Level 4 candidate.
3. m* tracks the cut in both. Graph property. Level 2.
4. Smooth (w > 6). **Expected outcome.** Reason, from 1701.00050: protection is controlled by
   nu = -log2(Re lambda_1), and critical Ising has a light operator (Delta_sigma = 1/8), so nu is
   small and recoverability should degrade gradually; sharp minimal-cut behaviour is a large-bond-
   dimension result (1601.01694), not chi = 6 to 8. 1701.00050 gives only upper bounds on error, vacuous
   at three layers, so it does not predict the curve. Level 2, or Level 3 negative if C-HAAR differs.

**Honest prior.** Outcome 4, then 3. A Level-4 result requires outcome 2, which needs sharp behaviour
exactly where both bodies of theory predict smoothness. It is unlikely. The experiment is still worth
running because it is the first observable in this project that touches the network at all, and
because 1701.00050 leaves the location of recovery failure open.

## Kill conditions, fixed now

- G3 fails: the experiment is void, not negative.
- Outcome 3 or 4: no geometric language is used for the result. It is written up as what it is.
- 1701.00050 was read (2026-09-21) and does not predict f(A_m). Anything it does prove (depth-monotone
  protection, the approximate-code statement, the decoupling observable) is cited and never claimed.
- If a later-found paper predicts m_half or w and the measurement agrees: Level 1, and HYP-033 closes
  as "answered by prior art".

## Compute

(Rewritten 2026-09-22 on Jon's instruction.) RunPod CPU pod on Jon's account, per rule 4 above. Local
compute is used only for code validation on small networks (N = 9 selftest and single chi = 6
aligned points), never for the registered grid. Cap 25 USD. Nothing billable starts without the
hourly price stated to Jon first. Standing RunPod authorization applies (spin, run, monitor, fetch,
kill, without per-step asks) inside the cap.

## Banned

Reporting I(R_up:A) or the two-ended I(R:A) as a network observable. Adding regions, bonds, or chi values after results. Reporting a fixed-operator recovery error as the
headline. Mixing Renyi-2 and von Neumann points in one fit. The words "geometry", "wedge" or
"emergent" applied to outcomes 1, 3 or 4. Calling anything novel before the section 8 gate is recorded.

## Open design questions for Jon and for the next draft

1. (Closed 2026-09-22 at registration.) ONE bond: the layer-2 bond used by G0 (`cone(27, 2, 1)`,
   17-site cone). No x scan, no other layers. Anything else is a new experiment.
2. (Closed: Jon approved the thresholds 2026-09-21.) v2 replaces "largest single drop" with m_half and the width w, with thresholds fixed above. Are the
   thresholds (cone <= 2, cut 7 to 10, smooth w > 6) acceptable to Jon as written?
3. (Closed 2026-09-21 by G0.) k = 2 stands; the cut-Gram route makes every point except m = 4
   feasible, and m = 4 is declared missing under rule 1.
4. (Closed 2026-09-21: quotes verified, papers catalogued.)
5. (Closed 2026-09-24, Jon: "approved on all that you think is best".) C-REWIRE (pre-run spec 2): option (a),
   DROPPED. The primary result is outcome 4 (smooth, SIM-2026-079), so there is no cut-tracking claim for a
   rewired control to test; the weaker mirror-rewire variant would not change the claim level.


---

## v3 AMENDMENT — APPROVED by Jon 2026-09-22 ("approved"). Recorded BEFORE any registered f value was printed.

Reason and evidence: `AMENDMENT-V3-PROPOSAL-HYP033.md`. Purity plus monotonicity give m_L + m_R <= 17 for every
isometric network on this graph, so m_half <= 8.5, and the cut predictor sits at exactly 8.5. An unregistered Haar network
(chi 3, seed 9999) gives m_half = 8.50 on both edges. As registered, m_half cannot separate cut-like from random.

1. **Reported per network and edge:** m_L, m_R, and the side-information gap g = 17 - (m_L + m_R). m_half is
   still reported, labelled "pinned by complementarity, not discriminating".
2. **Primary cut statistic: m_0.9**, the first m on each edge with f(A_m) < 0.9, interpolated linearly as for m_half.
   **Cut-like:** m_0.9 >= 6 on both edges, AND the seed mean of m_0.9 is at least 3 sites above the C-HAAR seed mean
   at chi = 6. Both conditions are required. Cone-like (m_half <= 2) is unchanged.
   Smooth: w > 6 AND not cut-like. *Precedence was left open in the proposal; the lead fixed it here before unblinding:
   the cut-like test is applied first.*
3. **Outcome 2 downgraded to Level 3**, "holographic-code-like encoding of the optimized circuit". A Level 4 claim needs a
   CFT-matched non-geometric ansatz. None is registered.
4. Everything else stands as registered: the observable, gates G1 to G5 (G5 still compares m_half between chi 8 and chi 6),
   the controls, the blinding, the cap order, and the network set. No new regions are added.
