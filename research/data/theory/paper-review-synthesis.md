# Paper Review Synthesis: Draft v3

**Date:** 2026-04-03
**Sources:** research-primary.md, research-practical.md, research-challenge.md
**Note:** researcher-alt (referee attack vectors) timed out without output; challenger covered that ground independently.

---

## Executive Summary

The paper's force profile result (alpha=3.92, backed by OPE fusion rules) is PRL-caliber science that would survive serious referee scrutiny. However, the paper itself is not submission-ready: it's 2x over PRL's word limit, tries to present five results of wildly unequal strength, has data provenance gaps, and would be better served by PRX Quantum. The effective mass result (Result 3) is the weakest link and should be demoted.

## Key Findings

- **All core numbers verified** against source JSONs (24q alpha, transport T, ALM errors, chi=3 energies). Two gaps: 16q exact fit parameters not persisted to JSON, and "0.00%" is actually 0.0024%.
- **OPE fusion rule proof is rigorous** -- epsilon x epsilon = [1] is exact, C_{eps,eps,eps}=0, three independent arguments confirm.
- **All 5 figures exist** on disk. Missing: chi=3 comparison figure (potential Fig 6).
- **Reference cleanup needed** -- [3] has wrong journal, 6-7 refs missing volume/pages, Nocedal & Wright cited but absent from list.

## Practical Considerations

- **Word count: ~5,500 vs PRL limit 3,750.** Fatal for PRL. PRX Quantum has no strict limit.
- **LaTeX stale** -- paper-draft.tex is v2, missing entire chi=3 section and OPE analysis.
- **arXiv endorsement**: 4 emails sent, 0 responses after 9 days. Need fallback (SciPost, Quantum journal).
- **GitHub repo**: chi=3 data not pushed to public branch. [repository URL] placeholder in Supplemental.
- **Estimated time to submission-ready**: 1-2 weeks.

## Challenges Survived

1. **Force profile (GREEN)**: Exact CFT prediction, 12 clean points, 0.5 sigma agreement, rigorous OPE proof, novel observable. This is the paper's anchor.
2. **Chi=3 MERA (YELLOW)**: First TN-based force measurement, correct universality class, path to hardware. Defensible with hardware-path framing.
3. **Transport (YELLOW)**: Sub-percent match at N=16, Wang-He analytical validation. Defensible if N=24 deviation is framed honestly.
4. **ALM method (YELLOW)**: Solves real Z2 problem across 5 seeds. Standard technique but novel application.

## Challenges NOT Survived

1. **Effective mass (RED)**: Post-hoc parameter matching, internally inconsistent derivation (m^2=0 but m_eff=0.693), only 2 data points, no error bars. Should be demoted from "result" to "discussion point."
2. **"Three independent measurements" language**: They share the same observable, operator, and Hamiltonian family. Should say "three consistent evaluations."
3. **Graviton language**: "Gravitational forces" is overclaimed. Should say "consistent with holographic stress-tensor exchange."
4. **No goodness-of-fit statistics**: No chi-squared, AIC/BIC, or residual analysis for power-law vs exponential. Must add before submission.
5. **No anchor dependence test**: All force measurements use anchor=6. Untested for OBC artifacts.

## Recommendation

**REVISE, then SUBMIT to PRX Quantum.** Confidence: HIGH.

Specific actions before submission:
1. Retarget from PRL to PRX Quantum (removes word count crisis)
2. Restructure as 2-result core (force profile + chi=3 method), with transport and ALM as supporting
3. Demote effective mass to discussion/motivation
4. Add chi-squared / goodness-of-fit statistics to force profile
5. Fix "three independent measurements" -> "three consistent evaluations"
6. Hedge graviton language throughout
7. Cut or shrink Section VIII.E (AI methodology) -- move to acknowledgments
8. Fix reference errors ([3] journal, missing volumes, add Nocedal & Wright)
9. Re-run 16q force scripts to persist fit parameters to JSON
10. Push chi=3 data to public GitHub repo
11. Regenerate paper-draft.tex from updated .md
12. Add chi=3 comparison figure (Fig 6)
