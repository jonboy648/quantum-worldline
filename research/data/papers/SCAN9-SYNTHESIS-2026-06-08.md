# Scan #9 Synthesis — 2026-05-13 to 2026-06-11

**Prepared by:** Synthesis Agent (Tier 1)
**Covers:** Scan-8 backlog catalogue (Part A, PAPER-2026-101..114, HW-2026-055..063) + fresh specialist sweep (Part B)
**Method note:** arXiv export API via WebFetch throughout. paper-search MCP remains query-blind (returns latest-submission firehose regardless of keywords; GScholar empty). All abstract screening done on raw API results.
**ID high-water after this scan:** PAPER-2026-114, HW-2026-063

---

## Executive Summary

- **NO anchor contradictions.** All 14 papers and 9 hardware entries screened against alpha~4 (3.92±0.16 / 3.97±0.15 / 4.07±0.18), T=(pi/2)*l_AdS (residual ~1.2% at N=16), chi=3 MERA 2-phase prep, and m_eff=0.693. Zero conflicts found.
- **Biggest miss corrected (PAPER-2026-111, rel 5):** Endres/Caltech 2601.16275 is direct experimental observation of Ising CFT and tricritical Ising CFT excitation spectra on a programmable Rydberg array with boundary-condition control. This is substrate validation for HYP-017: the exact hardware platform our alpha~4 force test targets has already demonstrated spectrally-resolved 2D Ising CFT criticality. This paper should be cited in any QCUP/HYP-017 revival.
- **Hardware access shift (rel 4 x2):** QuEra Gemini (260 Rb-87 qubits, 99.2% 2Q gate fidelity, collaboration route available, HW-2026-062) is a direct non-AWS path to the alpha~4 force-existence test at proper Rydberg scale. Quantinuum Sol roadmap (HW-2026-061, 192q/99.98% 2Q/10k gate budget, 2027 target) is the cleanest future path for 16-24q MERA transport with error correction.
- **Theory bridge (rel 4):** Ansel 2405.02380 (PAPER-2026-110) maps spin-spin correlators to geodesic length via the Synge world function: d ~ sqrt(-2 eps^2 ln C). This is the SAME correlator-geometry family as our HYP-012 (CMI/correlator-distance route), distinct from the Crofton force route (HYP-014/022). Fittable to existing MERA sigma-correlator data at zero new cost. Formalizing why HYP-012 and HYP-014/022 failed for structurally different reasons is the recommended Theory follow-up.
- **Hologron lineage remains isolated:** Sahay 2401.13595 + Wang-He 2501.03084 + Wang-He 2603.07639 is still a two-group, three-paper cluster. No third independent group has built on, challenged, or reproduced hologron dynamics this window.
- **Crofton stays buried:** PAPER-2026-114 (Wen/Xu/Zhong PEE thread-network) applies Crofton-like counting to RT entropy, not force profiles. This is not a revival; HYP-014/022 remain doubly refuted (SIM-024 structural + category mismatch).
- **FT hardware cost-down drumbeat continues:** Five hardware entries confirm the trend — ion qLDPC breakeven (9x better logical error), Atom Computing toric code (90 syndrome rounds), Yb readout 99.89% — but no new absolute 2Q fidelity record was set this window.

---

## Relevance >= 4 Findings

| ID | Reference | One-line | Why it matters | Recommended followup |
|----|-----------|----------|----------------|----------------------|
| PAPER-2026-111 | 2601.16275 (Endres/Caltech, 2026-01-22) | Direct experimental Ising CFT + tricritical Ising CFT spectra on Rydberg array with boundary-condition control | Substrate validation for HYP-017: confirms 2D Ising CFT is spectrally resolvable on the exact hardware our alpha~4 force test targets. Biggest scan-8 miss. | Cite in HYP-017 feasibility doc and any QCUP/SciPost revision. Theory: check if boundary-condition toggle maps to our chi=3 MERA boundary conditions. |
| HW-2026-061 | Quantinuum Sol roadmap (2027) | 192q, 99.98% 2Q, 10,000-gate budget | Cleanest future EC-enabled path for 16-24q MERA transport test; gates budget exceeds MERA circuit depth by ~5x | Monitor for access announcement; revisit HYP-016 FT-MERA gate-count estimate against Sol specs when available. |
| HW-2026-062 | QuEra Gemini | 260 Rb-87 qubits, 99.2% 2Q, collaboration route | Direct non-AWS/non-QCUP path to Rydberg-MERA alpha~4 force-existence test at proper scale. Below Helios fidelity frontier but above the threshold needed for force-existence (not precision) measurement. | Contact QuEra for collaboration; reframe HYP-017 submission as collaboration proposal rather than paid AWS run. Cite PAPER-2026-111 for CFT substrate credibility. |
| PAPER-2026-110 | 2405.02380 (Ansel, 2024-05-03) | Synge world function maps spin-spin correlator to geodesic distance: d ~ sqrt(-2 eps^2 ln C) | Same family as HYP-012 (CMI/correlator-distance), structurally distinct from Crofton (HYP-014). Fittable to existing MERA sigma-correlator data with no new state-prep; likely reproduces HYP-012 boundary (distance ≠ alpha=4 force) but clarifies the failure mode. | Theory: formalize "Synge-distance (Ansel) vs Crofton-force (HYP-014/022)" as two distinct correlator->geometry objects, explaining why each failed. Computation: fit existing sigma-correlator data to d~sqrt(-2 eps^2 ln C), check whether recovered distances match geometric separations. |
| PAPER-2026-101 | 2605.21447 (Schuhmacher/IBM, 2026-05-20) | MERA + quantum-annealed state via classical shadows: >5x (N=12) / >2x (N=24) GS-energy improvement at fixed circuit depth | Does NOT challenge task #95 (their quantum circuit is fixed+shallow; heavy lift is classical post-processing, not ADAPT-VQE). Confirms fixed-shallow-circuit + classical-post regime is a live competitor to ADAPT-VQE for state quality. | Theory: assess whether IBM's classical-MERA optimizer on top of quantum-annealed state could serve as a null-model for chi=3 fidelity claims. Computation: compare reported N=24 GS energy error to chi=3 MERA benchmark. |

---

## Patterns and Trends Across Parts A and B

**1. FT hardware cost-down drumbeat is now consistent across all platforms.**
Five entries this window (ion qLDPC, Atom Computing toric code, Yb readout, erasure detection, Gemini) all push the same direction: logical error rates falling, round counts rising, fidelity records nudging upward. No single breakthrough dominates, but the cumulative trajectory confirms HYP-016's reframe ("FT neutral atoms = cheap, not exotic") is aging well. The IonQ 99.99% / Quantinuum 99.921% absolute 2Q frontier remains unchallenged.

**2. Rydberg-CFT convergence is real and accelerating.**
PAPER-2026-111 (Endres CFT spectra) and PAPER-2026-112 (Antunes/Rong conformal interface + W3 symmetry) arrive within 5 months of each other on the same Rydberg + Ising CFT substrate. The platform overlap with our alpha~4 force test is no longer theoretical — it is experimentally demonstrated. This is the clearest strengthening of HYP-017's hardware-feasibility case since PAPER-061 established the PXP-MERA connection.

**3. Emergent-gravity cross-frameworks proliferating, not converging computably.**
Four papers this window (PAPER-108/109 Raasakka QFT-vector-model, PAPER-110 Ansel Synge, PAPER-103 holographic isoTNS, PAPER-102 random tensor networks) all use some variant of "correlations encode geometry." None share a computable object with our MERA pipeline. Math Bridge verdict holds: structural analogy, not operational bridge. The field is broadening faster than it is deepening around any shared formalism.

**4. Hologron lineage remains a two-group island.**
Sahay 2026 + Wang-He 2025 (two papers) + Wang-He 2026 (PAPER-088) = three papers from two groups. No third independent group has cited, reproduced, or challenged hologron dynamics. This is a flag: either the community hasn't caught up, or the niche is narrower than the hype. Any HYP-017 revival must acknowledge the lineage depth.

**5. Crofton is structurally closed, not just numerically failed.**
HYP-022 (SIM-024) refuted the PEE-thread/Crofton route numerically. PAPER-2026-114 now confirms the category error: Crofton-like counting in the literature targets RT entropy, not force profiles. The two HYP-014/022 failures are now understood to be mechanistically distinct from each other (wrong discretization vs wrong object), and both distinct from the Ansel/Synge failure mode (distance ≠ force). This is resolved territory; no compute cycles needed.

**6. Holographic transport / interface papers cluster but don't cross-check HYP-023 directly.**
PAPER-2026-104/105 (Liu/Wang AdS3/AdS2 junction transport) address transmission across CFT interfaces with monotonicity in brane tension and effective-central-charge bounds. HYP-023 is about composite-geodesic transport residuals in a discrete MERA context, not a junction/brane setup. The framing is adjacent, not testable-against. A computation agent could check whether the effective-central-charge bound from PAPER-2026-104 is consistent with the chi=3 MERA central charge c=1/2.

---

## Research Gaps

**Gap 1 — Worldline-MC + holography/tensor networks: EMPTY.**
HYP-003 (worldline MC matches MERA) and HYP-007 (worldline MC on H^2) target a niche that has produced zero 2025-26 papers across all scan windows. No other group is working the intersection of worldline Monte Carlo and AdS/MERA. This is either a genuine blind spot in the community or an indication the approach is considered unworkable. Lowest-cost probe: theory assessment of whether any worldline MC observable maps to a MERA boundary observable without full state reconstruction.

**Gap 2 — No emergent-gravity-on-simulator experiment yet.**
PAPER-2026-111 demonstrates Ising CFT spectroscopy on Rydberg hardware. PAPER-2026-101 demonstrates MERA state prep on quantum hardware. No paper has yet combined these to measure a holographic observable (force profile, transport, entanglement structure) on actual quantum hardware and compared to an AdS/MERA prediction. HYP-017 would be the first such experiment if executed. The gap is real and unoccupied.

**Gap 3 — Rydberg + MERA combined paper still absent.**
The literature has Rydberg + Ising CFT (PAPER-2026-111) and MERA + quantum circuits (PAPER-2026-101), but no paper that explicitly constructs a MERA-type tensor network on a Rydberg blockade array and measures holographic observables. Our chi=3 MERA force-profile result is in this gap. This strengthens the novelty claim for any submission.

**Gap 4 — HYP-025 (universality of alpha: Ising vs Z3 chiral clock) has no recent support or refutation.**
PAPER-2026-112 (conformal interface with W3 symmetry, proposed Rydberg realization) is adjacent but doesn't address the alpha-universality question directly. HYP-025 requires new qutrit-MERA state-prep code; no shortcut found this window.

**Gap 5 — hologron decay timescale: no independent measurement.**
The R1 killer issue from the HYP-017 devils-advocate review (tau ~ ns-scale in natural Rydberg units) remains unchallenged and unverified by any third-party paper. Wang-He 2603.07639 provides decay characterization but it comes from the same group as the original proposal. An independent theory calculation of tau from the Rydberg Hamiltonian parameters would strengthen or definitively kill the hologron-dynamics route.

---

## Recommended Followups by Tier

### Theory
1. **Ansel/Synge formalization (PAPER-2026-110):** Write a 1-2 page note distinguishing three correlator->geometry objects that have all been attempted in this project — CMI/correlator-distance (HYP-012), Crofton force (HYP-014/022), and Synge-distance (Ansel). Document why each failed (HYP-012: distance ≠ force; HYP-014: wrong discretization; HYP-022: wrong object category; Ansel: likely same category as HYP-012). This closes the "correlator->geometry" thread and removes it from active hypothesis space.
2. **HYP-017 substrate cite (PAPER-2026-111):** Update HYP-017 feasibility document to cite Endres 2601.16275 as direct substrate validation. The boundary-condition toggle in that experiment (which switches between Ising and tricritical Ising spectra) should be mapped to our chi=3 MERA boundary conditions — if the mapping is clean, this strengthens the force-measurement proposal significantly.
3. **HYP-025 triage:** Assess whether PAPER-2026-112 (W3 conformal interface) provides any shortcut for the qutrit-MERA state-prep problem, or whether HYP-025 remains blocked on new code. If blocked, de-prioritize until chi=3 transport is fully published.

### Computation
1. **Ansel sigma-correlator fit:** Apply d ~ sqrt(-2 eps^2 ln C) to existing MERA sigma-correlator data (already in-hand from the HYP-012 work). Expected outcome: recovered distances match geometric separations but do NOT match the alpha=4 force profile, confirming the distance-vs-force distinction. Cost: ~1 hour of compute on existing data.
2. **PAPER-2026-104 central-charge cross-check (HYP-023):** Check whether the effective-central-charge transmission bound from Liu/Wang AdS3/AdS2 junction is consistent with c=1/2 for the critical Ising CFT. If the bound is satisfied, it does not validate HYP-023 but removes one potential contradiction. If violated, it flags a tension in the composite-geodesic transport framing.
3. **HYP-016 FT-MERA gate count refresh:** With HW-2026-055 (ion qLDPC 9x breakeven) and HW-2026-056 (Atom Computing 90 rounds), revisit the FT-MERA gate-count estimate from scan-4. The cost-down trend may have moved the "earliest viable EC-assisted MERA run" date forward.

### None required (resolved or monitoring only)
- Crofton / HYP-014 / HYP-022: closed. No further compute.
- PAPER-2026-107 (KSS viscosity/causality): tangential background only.
- PAPER-2026-108/109 (Raasakka QFT-vector-model): structural analogy confirmed non-testable; no action.
- HW-2026-057/058/059: fidelity-record tracking only; no physics action.

---

## Errata Cross-Reference

The transport residual cited in earlier digests as "0.72% at N=16" has been corrected to ~1.2% at N=16 per ERRATA.md E2 (dt-grid artifact). All synthesis in this document uses the corrected value. Published Zenodo v3 (10.5281/zenodo.19661227) is unaffected — the correction applies to the interpretation of the simulation precision, not the published result.
