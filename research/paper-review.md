# Devil's Advocate Review — Paper Draft v1
**Reviewer:** Theory Lead (theory-lead)
**Date:** 2026-03-18
**Paper:** "AdS Causal Structure in Variational Quantum Circuits: Holographic Transport at Sub-Percent Accuracy"
**Status:** Pre-submission stress test. All attacks are adversarial by design.

---

## Summary Verdict

The transport result (0.72%) is the paper's strongest claim and will likely survive peer review. The ALM method is genuinely novel as a quantum variational technique. The worldline correspondence section is incomplete and needs to be restructured as a speculative bridge rather than a resolved result. Section V (force measurement) is an honest negative result but is currently written in a way that undermines confidence in the paper's scope. The T*L scaling from two data points is premature as a "prediction."

**Publish-readiness:** Conditional. Address attacks #1, #4, #5 before submission. #2, #3, #6, #7 are manageable with wording changes.

---

## Attack #1: "0.72% is coincidence at N=16 — N=24 gives -31.6%"

**Rating: CRITICAL**

This is the most dangerous attack. The paper leads with 0.72% accuracy at N=16, but the N=24 result is T_measured = 1.55 vs T_predicted = 2.266 — a -31.6% discrepancy. The paper rescues this by introducing the T*L scaling, but that introduces a new claim from exactly two data points.

**The circular logic problem:** The T*L = 36-37 "consistency" is engineered from the two measurements in hand. T*L(16) = 2.250 * 16 = 36.0, T*L(24) = 1.550 * 24 = 37.2. These agree to 3.3%, but a reviewer will immediately note: (a) two points define a fit trivially, (b) the chosen scaling T ~ C/L is not derived from any AdS/CFT principle — it is a phenomenological ansatz motivated by the data, and (c) the N=16 agreement (0.72%) may be the anomaly, not the N=24 one.

**Deeper problem:** The paper claims N=16 benefits from "near-cancellation of finite-size corrections." This is post-hoc. Without an independent theoretical prediction of the finite-size correction magnitude, this is curve-fitting masquerading as understanding.

**What a hostile referee will write:** "The authors' central quantitative claim (0.72% accuracy) holds only at N=16. At N=24, the same quantity deviates by 31.6%. The T*L scaling ansatz is empirical, derived from two points, and physically unmotivated. The paper's title claims 'sub-percent accuracy' — this is only true at one system size, and arguably by coincidence."

**Recommended fix:**
1. The title should not say "sub-percent accuracy" unless that accuracy is robust across system sizes. Change to "Sub-Percent Holographic Transport Prediction at N=16" or restructure the claim.
2. Section III.E must acknowledge that T*L ~ C/L is a phenomenological fit, not a derived result.
3. Either (a) provide a theoretical derivation of the 1/L finite-size correction from the MERA geometry (Lin 2026 thread discreteness argument — flesh this out quantitatively), or (b) present T*L scaling as a prediction to be tested rather than as evidence supporting the N=16 result.
4. If Lin 2026 predicts 0.47% error at N=24 from thread discreteness, that is a specific quantitative prediction. Does the T*L = 37.2 result (vs prediction of 36.0 * (24/16) * correction) match that? Work this out explicitly.

---

## Attack #2: "ALM is standard optimization — what's novel?"

**Rating: MAJOR**

Augmented Lagrangian Methods are textbook constrained optimization (Nocedal & Wright, Chapter 17). The "two-phase" warm-starting trick (relax constraint to escape basin, then tighten) is well-known in nonlinear programming. The paper claims this is "novel" but does not characterize what is novel about it.

**The actual novelty** is the application to quantum variational circuits with non-smooth symmetry constraints — specifically, that ALM warm-start enables hard Z2 projection to work where cold-start projection fails. This IS a genuine insight, but the paper does not articulate it clearly. The novelty is in the *diagnosis* (cold-start projection fails because you start in the wrong basin) and the *combination* (ALM for basin escape + hard projection for symmetry exactness).

**What a hostile referee will write:** "The authors' 'novel' method is Augmented Lagrangian Method, which has been used in constrained optimization for decades. The two-phase approach is described in Nocedal & Wright. The application to VQE symmetry constraints may be incremental."

**Recommended fix:**
1. Reframe the novelty claim: "We identify why cold-start Z2 projection fails (wrong-basin initialization) and introduce a two-phase warm-starting protocol that combines ALM basin escape with hard symmetry projection. To our knowledge, this combination has not been demonstrated for quantum variational circuits with discrete symmetry constraints."
2. Add a brief literature survey of prior VQE symmetry enforcement methods (penalty methods, symmetry-adapted ansatze, tapering) and explain why each fails for this problem.
3. Cite Nocedal & Wright explicitly — this demonstrates awareness, not ignorance.

---

## Attack #3: "Chi=2 MERA is known to be insufficient — why not chi=3?"

**Rating: MAJOR**

The paper reports that chi=2 produces a GHZ-like ground state at N=24 with flat correlations. The paper diagnoses this correctly as an "expressibility ceiling." But a reviewer will ask: this is known. Chi=2 binary MERA has been studied extensively and its limitations for TFIM are in the literature. Why spend $22 of compute and 44 hours demonstrating a known insufficiency?

**The specific known result:** The entanglement entropy scaling of chi=2 MERA is bounded by S <= chi (approximately), which is insufficient for the TFIM critical ground state with S ~ log(N)/3. This is not surprising to experts.

**What a hostile referee will write:** "The chi=2 expressibility barrier is well-known. The authors' 44-hour GPU computation at N=24 confirms this known limitation rather than providing new physics. Why not use chi=3?"

**Recommended fix:**
1. Acknowledge explicitly that chi=2 limitation is expected from entanglement entropy arguments. Reframe the 24q computation as: (a) demonstrating that ALM+projection achieves the theoretical energy floor for chi=2 (i.e., the method is optimal for this expressibility), and (b) establishing the baseline for chi=3 comparison.
2. Either provide chi=3 results (even at N=8 or N=12 to show the expressibility improvement), or frame chi=2 as a deliberate hardware-feasibility choice (chi=2 = 57 CNOTs on Helios; chi=3 would require significantly more gates).
3. Add a sentence: "We use chi=2 to remain within the hardware feasibility window for Quantinuum Helios (57 CNOTs at chi=2 vs approximately N CNOTs at chi=3); demonstrating the holographic transport observable at chi=2 suffices for our primary claim."

---

## Attack #4: "No publishable force data (V = -C_vac)"

**Rating: CRITICAL**

Section V is an honest account of the negative force measurement result. But it contains a sentence that will stop a referee cold: "V_BP = C_two - C_vac approximately -C_vac. No holographic decay is visible." And further: "the ZZ correlator change is the wrong observable when the excitation destroys the entire correlator structure."

The paper is presenting a result where: (a) the VQE ground state has GHZ correlations (not critical), (b) boundary-primary excitations destroy all correlations, (c) the correct observable (interaction energy F(dr)) has been identified but not yet computed.

**The problem:** Section V currently reads as "we tried to measure holographic forces and failed." This is fine for a methods paper, but the paper's stated contribution in the abstract is the ALM method and transport measurement — the force measurement was supposed to be a third result. Instead it is a confession of incomplete work.

**PENDING: This attack depends on the F(dr) results from SIM-2026-011 (Task #1, in progress).** If F(dr) shows clean decay with 5+ points, this attack collapses entirely and Section V should be rewritten as a positive result. If F(dr) is also flat or ambiguous, this attack is fatal to the force measurement claim and Section V should be restructured to explicitly remove it from the abstract's claimed contributions.

**Recommended fix (if F(dr) is positive):**
- Rewrite Section V around the interaction energy result. Keep the ZZ correlator negative result as a diagnostic (explains why previous approach failed) but lead with the clean F(dr) data.
- Update the abstract to replace "current status" with the actual F(dr) result.

**Recommended fix (if F(dr) is negative/flat):**
- Remove force measurement from the abstract's contribution list.
- Restructure Section V as "Constraints on holographic force observables" — a diagnostic section explaining what doesn't work and why, setting up future work.
- The paper's three contributions become: (1) transport accuracy, (2) effective mass resolution, (3) ALM method. This is still a complete PRL letter.

---

## Attack #5: "Wang and He already showed holographic transport"

**Rating: MAJOR**

Wang and He (arXiv:2501.03084, PAPER-2026-007) already demonstrated holographic transport in MERA circuits. The paper's transport section largely replicates their experimental protocol. The paper claims its contribution is (a) the composite geodesic framework resolving the factor-of-2, and (b) sub-percent quantitative accuracy.

**The problem with (a):** The composite geodesic framework is from Bohra and Sivaramakrishnan (arXiv:2511.22168, PAPER-2026-020) — it is not the authors' contribution. The paper is applying an existing geometric framework to explain an existing experimental phenomenon. The synthesis is valuable but is it sufficient for a PRL letter?

**The problem with (b):** The 0.72% accuracy is achieved at N=16 using an analytical (not VQE-optimized) MERA. Wang and He used the same analytical MERA. Have the authors actually improved on Wang and He's experiment, or just applied a better theoretical framework to interpret the same type of experiment?

**What a hostile referee will write:** "Wang and He (2025) demonstrated holographic transport in MERA circuits. Bohra and Sivaramakrishnan (2025) provided the composite geodesic framework. This paper applies the latter to interpret the former and reports 0.72% agreement. The experimental novelty over Wang and He is unclear."

**Recommended fix:**
1. Clarify explicitly what this paper does that Wang and He did not: Did Wang and He report a factor-of-2 discrepancy? If so, saying "we resolve the discrepancy they noted" is a contribution. If they did not identify the discrepancy, then "we provide the geometric grounding they lacked" is the contribution.
2. The N=24 transport and T*L scaling (if robust) IS new — Wang and He did not report N=24. Emphasize this.
3. The MERA-specificity control experiment (TFIM ring giving T=3.8) may be new if Wang and He did not include it.
4. The framing should be: "Wang and He discovered holographic transport and reported a factor-of-2 discrepancy. We resolve this discrepancy using the composite geodesic framework, provide the first N=24 measurement, and identify the T*L finite-size scaling."

---

## Attack #6: "T*L scaling from 2 data points is not a prediction"

**Rating: MINOR**

The paper presents T*L ~ 36-37 as a "falsifiable prediction" for N=32. But this emerges from two data points. A straight line through two points is a tautology, not a prediction.

**What a hostile referee will write:** "The 'falsifiable prediction' T(32) ~ 1.13 is derived from exactly two data points. This cannot be distinguished from any other 1/L curve."

**Recommended fix:**
1. Do not call T*L scaling a "prediction" derived from data. Instead, derive it from first principles if possible. The Lin 2026 thread discreteness argument (threads follow geodesics in MERA, 1/N correction from thread discreteness) should be the source of the prediction, not the empirical fit.
2. If Lin 2026 independently predicts T*L ~ C with C calculable from the MERA geometry, and the measured C = 36-37 matches, THAT is a genuine prediction-confirmation. Work this out.
3. Alternatively, present T*L as an "empirical observation" rather than a "prediction," and note that N=32 is currently inaccessible classically (2^32 states) and would require hardware or MPO methods to test.

---

## Attack #7: "OBC spectrum shifts affect m_eff extraction"

**Rating: MINOR**

Section IV.B extracts m_eff = 0.693 from the 16-qubit OBC energy gap: E_1 - E_0 = 0.190, giving scaling dimension x_1 = 0.485. The paper notes this is "shifted from the PBC value by OBC effects." The critical TFIM with PBC has gap E_1 - E_0 = pi/L * v_F (Fermi velocity), giving x_1 = 1/8 (spin field) and x_epsilon = 1. With OBC, the spectrum is different and the extraction requires care.

**The problem:** The paper does not derive x_1 = 0.485 rigorously from OBC conformal field theory. The OBC TFIM spectrum at criticality is known analytically (from free fermion analysis), and the energy gap extracts to specific scaling dimensions depending on boundary conditions. If the identification x_1 = 0.485 -> epsilon operator (Delta=1) is not rigorously justified, the m_eff = 0.693 result is not reliable.

**What a hostile referee will write:** "The authors extract a scaling dimension x_1 = 0.485 from the OBC energy gap and identify it with the epsilon operator (Delta=1). This identification requires justification. The OBC TFIM spectrum has specific finite-size corrections and the scaling dimension of the first excited state is boundary-condition dependent."

**Recommended fix:**
1. Provide the analytical OBC TFIM energy gap formula and show the extrapolation to the continuum limit.
2. Alternatively, cite a reference that establishes the OBC-to-CFT operator map for the TFIM and state explicitly which operator the first excited state corresponds to.
3. If the identification is uncertain, hedge: "consistent with the epsilon operator (Delta approximately 1)" rather than asserting Delta=1.
4. Note that m_eff = 0.693 = ln(2), which suggests a connection to the MERA bond dimension — this could be coincidental or meaningful (worth a footnote).

---

## Additional Issues Not in the Original Brief

### Issue A: Abstract claim "GHZ-like ferromagnetic superposition" is imprecise

The abstract says the chi=2 MERA produces a state with "flat ZZ correlations (C_vac ~ 0.70 for all dr >= 2), rather than the expected critical power-law decay C_vac ~ r^{-1/4}." The diagnosis of "GHZ-like" may be wrong: a GHZ state (|000...> + |111...>)/sqrt(2) would give <Z_i Z_j> = 1 for all pairs, not 0.70. A product state |+>^N gives <Z_i Z_j> = 0. The observed C_vac = 0.70 is intermediate — this is not a pure GHZ state. The correct diagnosis is that the chi=2 MERA converges to a mixture of states in the wrong symmetry sector rather than a pure GHZ state.

**Fix:** Replace "GHZ-like ferromagnetic superposition" with "a state in the ferromagnetic basin with non-critical correlations." Or if the GHZ interpretation is correct, provide more justification.

### Issue B: Section III.A says "analytical MERA isometry tensors (not VQE-optimized)"

This is a crucial methodological distinction that is buried in a parenthetical. The transport measurement uses the ANALYTICAL ground state, not any of the VQE results. This means the transport result is completely independent of the ALM optimization work. The paper should be clearer about this separation: transport is tested on the exact analytical MERA, and the VQE work is about preparing that state on hardware. Currently, sections II.B and III.A sit next to each other in a way that implies the VQE state was used for transport.

**Fix:** Add a clear statement in the introduction of Section III: "The following transport experiments use the analytical MERA ground state (Evenbly-White tensors), not the VQE-optimized circuit. The VQE circuit (Section II.B) is designed for hardware preparation; the analytical state is used here to isolate the transport signal from preparation errors."

### Issue C: Shot budget in Section VI.C is inconsistent with Section VI.A error budget

Section VI.A states 57 CNOTs with 0.57% accumulated logical error on Helios. Section VI.C states 280,000 shots for 5-sigma detection. These numbers should be verified to be consistent: a 0.57% logical error on 280,000 shots still gives substantial state corruption — the 5-sigma detection claim depends on the per-shot error model, which is not shown.

**Fix:** Add a brief shot-noise calculation: if the transport signal amplitude is ~3% and the per-shot error is ~0.57% accumulated, what SNR does 280,000 shots give? Show explicitly that 5-sigma is achievable.

---

## Summary Table

| Attack | Rating | Can fix with wording? | Requires new data? |
|--------|--------|----------------------|-------------------|
| #1: 0.72% is N=16 coincidence | CRITICAL | Partially | Theoretical derivation of 1/L correction |
| #2: ALM not novel | MAJOR | Yes | No |
| #3: chi=2 insufficient | MAJOR | Partially | chi=3 result would help |
| #4: No publishable force data | CRITICAL | Only if F(dr) positive | YES -- awaiting SIM-2026-011 |
| #5: Wang and He prior | MAJOR | Yes | No |
| #6: T*L from 2 points | MINOR | Yes | Derive from Lin 2026 |
| #7: OBC spectrum | MINOR | Partially | OBC gap calculation |
| Issue A: GHZ imprecise | MINOR | Yes | No |
| Issue B: Analytical vs VQE not clear | MINOR | Yes | No |
| Issue C: Shot budget consistency | MINOR | Yes | Simple calculation |

---

## Priority Recommendations Before Submission

1. **Wait for SIM-2026-011 F(dr) results.** The paper's scope depends on whether the force measurement is a positive or negative result. Do not submit until this is resolved.

2. **Derive the 1/L finite-size correction from Lin 2026 theory.** This converts Attack #1 from "coincidence" to "understood finite-size effect." If the thread discreteness calculation gives the right correction coefficient, that is a strong theoretical backing.

3. **Clarify Wang and He priority.** Write a clear priority statement: what did Wang and He observe, what remained unexplained (the factor-of-2), and what this paper contributes (resolution + N=24 + T*L).

4. **Fix the analytical-vs-VQE ambiguity in Section III.** This is a minor edit but important for clarity.

5. **Reframe ALM novelty** with explicit comparison to prior VQE symmetry enforcement methods.

---

*Review prepared by theory-lead. This is an adversarial review designed to stress-test the paper — not a rejection recommendation. The core transport result is solid and the paper has a clear path to publication with the fixes above.*
