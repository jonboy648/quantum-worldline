# Quantum Worldline Weekly Scan — 2026-04-26

**Period covered:** 2026-03-15 to 2026-04-26 (6 weeks)
**Scan type:** Full Tier 1 (literature + hardware + math-bridge)
**Papers catalogued:** PAPER-2026-042 through PAPER-2026-052 (11 papers)
**Hardware catalogued:** HW-2026-023 through HW-2026-031 (9 entries)

---

## Executive Summary

The 6-week period since the last scan (2026-03-14) saw no paper that directly cites or contradicts our Zenodo publication (10.5281/zenodo.19661227, posted 2026-04-20 — too recent for citation tracking). The key physics finding is that the holographic geometry/tensor network literature has bifurcated into two active threads that both converge toward our results: (1) PEE-thread tessellations of AdS confirming the geometric interpretation of MERA, and (2) the first experimental MERA demonstration on trapped-ion hardware showing log-law entanglement scaling at criticality. On hardware, the most significant news is IonQ's 256q Cambridge deployment and Pasqal's Vela 256q QPU — both within reach for 2026 MERA experiments. Google's expansion into neutral atoms with a dedicated modeling & simulation pillar signals increased competition and collaboration opportunities. No paper was found that directly contradicts our alpha~4 force or T=2.250 transport results.

---

## Findings Classification

### NOVEL (new to the field, high relevance)

**PAPER-2026-044** | `2512.19452` | Wen, Xu, Zhong (Dec 2025, revised Apr 2026)
*Holographic Tensor Networks as Tessellations of Geometry*
Relevance: 4
PEE threads (= bulk geodesics with Crofton-formula density) generate a **perfect tessellation of AdS space**, with minimal cuts reproducing the exact RT formula. Three tensor network variants constructed. This is the geometric picture that underlies our Lin 2025 thread analysis: our MERA threads ARE the PEE threads are the geodesics. The tessellation gives a rigorous reason why chi=3 MERA achieves 0.15% accuracy on RT formula.
**Flagged for theory** — the Crofton density formula gives a testable prediction for how thread flux should scale with chi, which we can check against our SIM-2026-016 kinematic space data.

---

### CONFIRMED (supports existing results)

**PAPER-2026-043** | `2412.18602` | Miao, Wang, Brown, Barthel, Cetina (Dec 2024, rev Aug 2025)
*Probing Entanglement Scaling Across a Quantum Phase Transition on a Quantum Computer*
Relevance: 5
**First experimental demonstration of log-law entanglement entropy at criticality on digital quantum computer**, using MERA on trapped-ion hardware. Barthel is co-author (same as our Miao & Barthel 2025 MERA convergence paper). This is the closest published experiment to our proposed Helios run. The hardware is trapped-ion (same family as Helios). Confirms our circuit compilation approach is experimentally validated.
**Flagged for theory** — the Barthel group is directly relevant; reaching out to them post-SciPost publication is a priority.

**PAPER-2026-042** | `2604.04596` | Liang (Apr 2026)
*Breaking the Entanglement-Structure Trade-off: Many-Body Localization Protects Emergent Holographic Geometry in Random Tensor Networks*
Relevance: 4
MBL sustains emergent holographic geometry (entanglement structure + mutual information simultaneously) in disordered XXZ model. Verifies the entanglement→geometry→gravity chain. Directly supports our MERA holographic geometry results from a different model class.
**Flagged for theory** — MBL stabilization as an alternative to our ALM+projection method warrants a feasibility note.

---

### WATCH (adjacent, monitor for follow-ups)

**PAPER-2026-045** | `2601.21065` | Jeffrey, Gandarias, Schleier-Smith, Swingle (Jan 2026)
*Building Holographic Entanglement by Measurement*
Relevance: 3
Measurement-based holographic state preparation (not unitary MERA). RT formula demonstrated for hyperbolic disk and wormhole geometries with Gaussian ops. Swingle (MERA/holography pioneer) is co-author. Alternative hardware path.

**PAPER-2026-046** | `2503.20566` | Wu, Liu (Mar 2025)
*Accurate Gauge-Invariant Tensor Network Simulations for Abelian LGT in (2+1)D*
Relevance: 3
Gauge-canonical tensor network form for Z2/Z3/Z4 gauge theories up to 32x32 lattice. First VMC real-time dynamics of PEPS. Directly adjacent to our Z2 symmetry projection method. Could improve our 3.33% energy floor.

**PAPER-2026-047** | `2604.17874` | Sekiyama, Nagano (Apr 2026)
*Ground state preparation in 2D pure Z2 lattice gauge theory via deterministic QITE*
Relevance: 3
Gauge-invariant QITE for 2D Z2 gauge theory. <0.1% relative error for 12-plaquette classical simulation. The Gauss's law constraint enforcement is the same physics as our Z2 projection. Provides a quantum circuit path (not VQE) to Z2-invariant ground states.

**PAPER-2026-049** | `2604.19735` | Khan et al. (Apr 2026)
*Architecting Early Fault Tolerant Neutral Atoms Systems with Quantum Advantage*
Relevance: 3
Teleportation-based scheme for fault-tolerant neutral atom dynamics simulations. ~11,495 atoms, ~15 hour runtime for full fault-tolerant dynamics. Brackets the long-term resource cost of fault-tolerant MERA transport.

**PAPER-2026-048** | `2602.07895` | Zhang, Yang, Bhattacharya, Mann (Feb 2026)
*Probing holographic CFTs*
Relevance: 2
Unruh-DeWitt detector + CFT Wightman functions + mana harvesting to probe AdS/CFT. Novel quantum information approach. Wightman function methods adjacent to our transport observable.

**PAPER-2026-050** | `2512.11967` | Kobayashi, Sappler, Pollmann (Dec 2025)
*Holographic Representation of 1D Many-Body States via Isometric Tensor Networks*
Relevance: 3
Holographic isoTNS achieves volume-law entanglement at low bond dimension. Cousin of MERA with explicit holographic axis. Expressivity comparison with chi=3 MERA is informative.

**PAPER-2026-051** | `2603.19726` | Fecit (Mar 2026)
*Advances in the Worldline Approach to QFT: Strong Fields, Amplitudes and Gravity* [PhD thesis]
Relevance: 2
Worldline formalism in QFT. Heat kernel methods relevant to AdS propagators. Low direct relevance.

**PAPER-2026-052** | `2603.09717` | (Mar 2026)
*Entanglement Measure Response to Modular Flow and Chiral Topological Phases*
Relevance: 3
Modular flow as driver of entanglement dynamics. Modular commutator generalization. Adjacent to our transport observable (Y response tracks modular flow).

---

### Hardware Frontier Update

| HW ID | Vendor | System | Qubits | Fidelity 2Q | Status | Relevance |
|-------|--------|--------|--------|-------------|--------|-----------|
| HW-2026-023 | IBM | Kookaburra (1386q module, 4158q 3-module) | 4158 total | TBD | 2026 roadmap target | 4 |
| HW-2026-024 | Quantinuum | Helios + H2@RIKEN + IPO filing | 98/94L | 99.921% | LIVE (Helios); H2 at RIKEN | 5 |
| HW-2026-025 | IonQ | 256q @ Cambridge Cavendish (announced 2026-03-11) | 256 | TBD | Announced, deploying | 4 |
| HW-2026-026 | Google | Neutral atom program (Adam Kaufman, CU Boulder) | TBD | TBD | New program announced 2026-03-24 | 3 |
| HW-2026-027 | QuEra | Gemini@AIST Japan; 3rd-gen roadmap 2026-2027 | 260/37L | TBD | Operational at AIST | 3 |
| HW-2026-028 | Pasqal | Vela (256q, 2026) + PINQ2 Canada | 256 | TBD | Vela launching 2026 | 3 |
| HW-2026-029 | Microsoft/Atom | Magne (50L qubits from ~1200 physical) | 1200/50L | TBD | Target start 2027 | 3 |
| HW-2026-030 | Rigetti | Cepheus-1-108Q (GA Apr 2026) | 108 | 99.1% | Generally available | 2 |
| HW-2026-031 | PsiQuantum | Omega (photonic, utility-scale target Feb 2026) | TBD | TBD | Announced | 1 |

**Hardware frontier summary:** Quantinuum Helios remains the best near-term target (99.921% 2Q, all-to-all, commercially live). IonQ's 256q Cambridge system and Pasqal's Vela 256q in 2026 open two new paths. IBM's Kookaburra with qLDPC + LPU is the 2026 fault-tolerant milestone to watch. Google's dual-modality strategy (superconducting + neutral atom) with an explicit "Modeling & Simulation" pillar increases the neutral atom ecosystem for MERA-type experiments. Microsoft/Atom Computing's Magne (50 logical qubits, start 2027) is the first concrete fault-tolerant deployment date on the near-term horizon.

---

## Math-Bridge Connections

### CONN-001: PEE Threads + Crofton Formula → Thread Density Prediction for chi=3 MERA
**Relevance: 5** | **Novelty: unexplored**
PAPER-2026-044 constructs holographic networks from PEE threads with Crofton-formula density. Lin 2025 (in our knowledge base) already connects MERA tensors to threads. The **new bridge**: the Crofton density formula gives a quantitative prediction for how thread flux should change when chi: 2→3. Our SIM-2026-016 kinematic space simulation computed CMI-based thread flux — we can directly test whether the chi=3 flux agrees with the Crofton tessellation prediction. This is a **novel cross-check** not in either paper.
**Suggested experiment:** Compute Crofton thread density for chi=3 MERA analytically and compare to SIM-2026-016 CMI data.

### CONN-002: MBL + MERA → Disorder-Protected Holographic Geometry
**Relevance: 4** | **Novelty: unexplored**
PAPER-2026-042 shows MBL protects holographic geometry in random tensor networks. Our MERA uses a critical (non-disordered) Hamiltonian. The bridge: could introducing a small amount of disorder into the Ising Hamiltonian strengthen the holographic geometry signal in the force profile? MBL is a different stability mechanism than our Z2 projection — worth a feasibility check.
**Suggested experiment:** Add small random field disorder to H_Ising, rerun force profile. Check if alpha deviates from 4.

### CONN-003: Measurement-Based Holography → Large-N Transport Test
**Relevance: 3** | **Novelty: partial**
PAPER-2026-045 (Swingle et al.) prepares holographic states via measurements, not MERA unitaries. For our transport experiment (T=2.250), the bottleneck is state preparation fidelity. If measurement-based prep is feasible on Gaussian hardware at larger N (say, N=32), it could test our T*L~scaling beyond the N=24 analytical limit. The wormhole geometry target in that paper directly matches our transport observable.
**Suggested experiment:** Adapt Swingle measurement protocol to prepare MERA ground state at N=32 and run transport protocol.

### CONN-004: qLDPC codes + Holographic Tensor Networks
**Relevance: 3** | **Novelty: partial**
No 2026 paper found that explicitly bridges qLDPC (Panteleev-Kalachev, Dinur-Evra et al.) to MERA holography. However, IBM's Kookaburra uses qLDPC memory + LPU — running holographic MERA on a qLDPC-encoded logical system is an untested combination. The HaPPY code (holographic quantum error correction) is a special case of tensor network codes, but not qLDPC-type. The **gap is real** and represents a future research direction.

### CONN-005: Fault-Tolerant MERA Architecture (Neutral Atoms)
**Relevance: 4** | **Novelty: partial**
PAPER-2026-049 provides concrete fault-tolerant neutral atom resource estimates for quantum dynamics (~11k atoms, ~15h). Our chi=3 MERA transport is a quantum dynamics simulation. **The bridge:** mapping our specific MERA circuit (chi=3, 16q, transport protocol) onto this fault-tolerant neutral atom architecture would give concrete estimates for when we can do a noise-free run. Rigetti Cepheus-1 and IonQ 256q Cambridge provide near-term NISQ rungs before the full fault-tolerant regime.

---

## Flagged for Theory (Relevance >= 4)

| Paper/Finding | Why | Recommended Action |
|---------------|-----|--------------------|
| PAPER-2026-043 (relevance 5) | Barthel group MERA experiment on trapped-ion = direct predecessor to our Helios run | Contact Barthel group post-SciPost; check if they're aware of our results |
| PAPER-2026-042 (relevance 4) | MBL stabilizes holographic geometry — new mechanism adjacent to our Z2 projection | Theory: feasibility note on disorder-protected MERA |
| PAPER-2026-044 (relevance 4) | PEE-thread Crofton tessellation → prediction for chi=3 thread flux | Computation: compare Crofton density to SIM-2026-016 CMI data |
| CONN-001 (relevance 5) | Crofton thread density gives testable chi=3 prediction | Theory + computation: cross-check against SIM-2026-016 |
| CONN-005 (relevance 4) | Fault-tolerant neutral atom resource estimates for MERA transport | Theory: map our circuit onto PAPER-2026-049 architecture |
| HW-2026-025 (relevance 4) | IonQ 256q at Cambridge = new access route comparable to Helios | Action: identify Cambridge academic collaboration contact |

---

## Recommended Follow-up

**Theory:** CONN-001 (Crofton thread density prediction for chi=3) is the highest-value cross-check available now — it uses existing SIM-2026-016 data and requires only an analytic calculation. This could strengthen the HYP-2026-009 case and provide a new figure for a follow-up paper.

**Hardware:** After SciPost submission, resubmit QCUP with smaller ask (~500 HQC) and update the case with the Zenodo DOI. Simultaneously open a Cambridge/IonQ channel (HW-2026-025) as a parallel hardware path.

**No contradicting papers found** for alpha~4 force, T=2.250 transport, or chi=3 MERA results in this period.

---

## Tier 2 + Tier 3 Synthesis (Hypothesis Pipeline → Computation)

Theory-lead generated 4 hypotheses (HYP-2026-013 through 016) from the flagged findings. All passed feasibility (TESTABLE_NOW). Computation-lead ran all 4 (SIM-2026-018 through 021).

### Hypothesis Verdicts

| HYP | Source | Verdict | Headline |
|-----|--------|---------|----------|
| HYP-2026-013 | PAPER-2026-043, HW-2026-024 | **PARTIALLY_REFUTED** | Helios fidelity threshold is 99.99%, not 99.5%. Detects force at dr=1..2 only (SNR=44 at dr=1, SNR=10 at dr=2 per SIM-2026-019) — sufficient for "force exists" but not for alpha fit. |
| HYP-2026-014 | PAPER-2026-044, CONN-001 | **REFUTED** | Crofton sin(pi*dr/N) profile fails catastrophically (max residual 5863% at dr=12). The 7.6 vs 7.8 amplitude ratio match was a numerical coincidence. Sigma profile is power-law dr^(-0.87), not sinusoidal. **Note:** SIM-2026-016 is exact 24q GS data (not chi=2 MERA as HYP-014 stated). The refutation is therefore against the strongest available data, not a chi-mismatched proxy. The chi=3 sigma test theory-lead suggested as a fallback is not currently runnable — SIM-2026-015d does not contain sigma data. A future chi=3 sigma run would test the broader Crofton-tessellation question, which remains INCONCLUSIVE for that functional form. |
| HYP-2026-015 | PAPER-2026-042 | **INCONCLUSIVE_ANALYTIC** (downgraded post-review) | Initial analytic verdict of "CONFIRMED" does not survive its own perturbation parameter: at gap_critical_N16 = 0.125, W=0.05J gives W/Δ = 0.4, which is **not** "weak coupling." The first-order vanishing argument applies only to disorder-averaged shift, not realization-by-realization values that the proposed test measures. **GPU run on at least W=0.05J × 5 realizations is required** before this verdict can support strategic claims. |
| HYP-2026-016 | HW-2026-025, CONN-005 | **REFUTED** (claim) / **TBD** (FT estimate) | IonQ 256q Cambridge not viable at typical 99.3-99.5% fidelity (gives dr_max=1 only) — this part of the verdict is robust. **However:** the "1839 atoms / ~8 min" FT neutral atom estimate is bare linear extrapolation from PAPER-2026-049's 100q/15h benchmark, with no architectural mapping of MERA's chi=3 isometry decomposition or magic-state distillation overhead. Treat as back-of-envelope, not as architectural evidence. |

### Cross-Tier Connections (post-computation)

The Tier 1 → Tier 2 → Tier 3 pipeline produced two important corrections to the Tier 1 narrative:

1. **CONN-001 was a false positive at Tier 1.** The Crofton thread density "agreement" (7.6 vs 7.8) was a numerical coincidence, not a real cross-validation. Without classical-simulator's residual check at intermediate dr (max 5863%), this would have been published as a confirmation. **Lesson: amplitude ratios are not enough — full profile residuals must always be checked.**

2. **Helios is a "force-existence + 2-point" platform, not a "force law" platform.** HYP-2026-013 reframed the near-term experimental story: Helios at 99.921% with a noise model and 10,000 shots gives **SNR = 44 at dr=1 and SNR = 10 at dr=2** (per SIM-2026-019; an earlier digest version mistranscribed these as 4.4σ and 1.0σ — corrected). dr=3 falls below the 3σ threshold (SNR = 1.9). Two clean data points confirm an attractive correlation but cannot distinguish alpha=3 vs alpha=4 vs alpha=5 — the dr=1/dr=2 ratio for power laws is just 2^alpha, with shot-noise overlap across reasonable alphas. The full alpha=4 measurement requires either (a) Helios at 99.99%+ or (b) FT neutral atoms 2027+. The next experimental proposal should claim "detect attractive holographic correlation with 2 dr points" rather than "measure alpha=4."

3. **MBL/MERA asymmetry hypothesized but not yet confirmed.** HYP-2026-015 was initially marked CONFIRMED_ANALYTIC, then downgraded to INCONCLUSIVE_ANALYTIC after devils-advocate review: the perturbation parameter W/Δ = 0.4 at the tested W=0.05J is not weak coupling, and the Z2-symmetry first-order vanishing argument applies to disorder-AVERAGE shift only, not realization-by-realization values. The qualitative claim that random tensor networks gain geometry from disorder while MERA loses its chi=3 critical point remains plausible but is not currently established. **GPU run on 5 realizations × W=0.05J required** before this verdict supports strategic claims.

### Surprises

- **FT neutral atoms naive linear estimate gives 1839 atoms / 8 min** for our circuit (vs PAPER-2026-049's 11,495 / 15h benchmark). **Caveat (post-review):** this is bare linear extrapolation. It does not account for chi=3 isometry decomposition, magic-state distillation budgets that scale with T-count, or atom-movement routing overhead. A more realistic estimate could be 5x–20x worse on either axis. Treat as back-of-envelope, not as architectural evidence. The qualitative "ordinary experiment when 256-1000q FT systems ship" point still holds; the specific numbers do not yet.
- **The Crofton coincidence is a teaching moment.** A future paper claiming a tessellation-MERA cross-check based purely on amplitude ratios should be regarded with extreme skepticism. The intermediate-point profile is the discriminating test.

---

## Final Cross-Tier Findings Classification

| Class | Count | Items |
|-------|-------|-------|
| **NOVEL** | 1 | PAPER-2026-044 (Wen-Xu-Zhong PEE tessellation, geometric foundation but not predictive for our chi=3 sigma) |
| **CONFIRMED** | 1 | PAPER-2026-043 (MERA on trapped-ion log-law entanglement) |
| **CONTRADICTS** | 0 | None this period — alpha~4 force, T=2.250, chi=3 results all unchallenged |
| **ACTIONABLE** | 4 | (a) Contact Barthel group post-SciPost re PAPER-2026-043; (b) Reframe near-term proposal as "Helios 2-point existence detection" (NOT "alpha=4 measurement") with FT neutral atoms as the eventual alpha target; (c) Pursue Cambridge IonQ contact only if their fidelity is confirmed >= 99.99%; (d) Run GPU MBL sweep before HYP-2026-015 verdict propagates |
| **INCONCLUSIVE_ANALYTIC** | 1 | HYP-2026-015 (MBL/MERA asymmetry — perturbation parameter not actually weak; needs GPU run) |
| **WATCH** | 6 | PAPER-2026-045 (Swingle measurement-based holography); PAPER-2026-046 (Z2 LGT tensor networks); PAPER-2026-047 (Z2 QITE); PAPER-2026-049 (FT neutral atom architecture); PAPER-2026-050 (holographic isoTNS); PAPER-2026-052 (modular flow + entanglement) |
| **REFUTED** | 2 | HYP-2026-014 (Crofton sin profile incompatible with sigma_by_dr); HYP-2026-016 (IonQ 99.5% threshold insufficient — robust; FT neutral atom estimate is back-of-envelope, not architectural) |
| **PARTIALLY_REFUTED** | 1 | HYP-2026-013 (Helios fidelity threshold for full alpha fit is 99.99% not 99.5%; 2-point detection at SNR=44/10 is the actual viable result) |

---

## Next Steps

1. **Send revised "Helios as 2-point force-existence detection" framing** to QCUP resubmission. Smaller ask (~500 HQC) is now motivated by SIM-2026-019's SNR=44/10 noise-model results — frame as "confirm attractive correlation," NOT as "measure alpha=4."
2. **Reach out to Barthel group** post-SciPost decision (their experimental MERA on trapped-ion is the closest published predecessor).
3. **GPU MBL run IS needed** (downgraded from "not needed"). Run 5 realizations × W=[0.05]J overnight before treating HYP-2026-015's verdict as confirmed.
4. **Update knowledge base + project memory** with verdicts and counters.
5. **Run a retrospective coverage audit** for 2024-08 through 2026-03 papers — PAPER-2026-043 (Dec 2024 / Aug 2025) being a 14-month-late discovery is a coverage-gap alarm. Specifically query for negative-result phrases ("fails to reproduce," "no power-law force," "MERA does not match AdS").
6. **Add feasibility-checker rule:** when two hypotheses use the same circuit, force shared parameters. HYP-013 (N_2Q≈40 at 8q) vs HYP-016 (N_2Q=56 at 16q) used inconsistent gate counts; this should not have passed feasibility.
7. **Next scan recommended:** 2026-05-10 (2-week cadence) — track first citations of our Zenodo paper.

## Devils-Advocate Review Conducted

A devils-advocate review of this digest (2026-04-26) caught 5 issues. Summary applied above:
1. SNR transcription error (4.4σ → SNR=44; 1.0σ → SNR=10) — fixed.
2. HYP-014 source-data classification (chi=2 → exact 24q GS) — fixed; refutation strengthened.
3. HYP-015 verdict downgraded CONFIRMED_ANALYTIC → INCONCLUSIVE_ANALYTIC; GPU run added to next steps.
4. FT neutral atom estimate marked as linear extrapolation, not architectural mapping.
5. Coverage-gap audit added to next steps after PAPER-2026-043 14-month-late catch.

---

*Tier 1 generated: 2026-04-26 by Literature Lead*
*Tier 2 generated: 2026-04-26 by Theory Lead*
*Tier 3 generated: 2026-04-26 by Computation Lead*
*Synthesized: 2026-04-26 by Worldline Orchestrator*
*Next scan recommended: 2026-05-10*
