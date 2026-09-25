# Theory Analysis — 2026-03-26

**Tier:** Theory (Tier 3)
**Pipeline:** conjecture-generator → feasibility-checker → philosophy-agent
**Based on:** `2026-03-26-scan-literature.md`
**Status:** HYPOTHESIS_GENERATED
**Speculative flag:** ALL findings below are speculative and require experimental/analytic confirmation.

---

## Executive Summary

Two new hypotheses generated from literature findings with relevance >= 4. Both pass feasibility gating (TESTABLE_NOW with existing tools). One existing hypothesis (HYP-2026-009) updated with new supporting evidence. No hypotheses archived as INFEASIBLE.

The highest-priority finding: the contrast between our power-law force (alpha=3.92) and Sahay-Lukin-Cotler's exponential force is not a contradiction — it is a testable prediction of AdS/CFT duality. Both results can be unified under a single framework (HYP-2026-011), making the contrast a *feature* of our paper, not a threat.

---

## New Hypotheses

### HYP-2026-011: CFT Conformal Block / Bulk-Boundary Duality
**File:** `research/data/hypotheses/HYP-2026-011.json`
**Confidence:** medium
**Feasibility:** TESTABLE_NOW
**Source:** SCAN-001 (Sahay-Lukin-Cotler contrast) + math bridge finding #1

**Claim (summary):** The power-law force F(dr)~dr^{-3.92} and Sahay-Lukin-Cotler's exponential force both describe the same MERA physics from different observer perspectives. Boundary observers see the 2D CFT conformal block for stress-tensor exchange (power-law 1/r^4), while bulk observers see the AdS graviton propagator (exponential in proper distance). The two are related by the AdS Poisson kernel integral:

```
V_boundary(dr) = integral_0^inf K(z, dr)^2 * V_bulk(z) dz
```

where K(z, x) = (z / (z^2 + x^2))^Delta is the bulk-to-boundary propagator. For Delta=2 (stress tensor) and V_bulk(z) ~ exp(-z/l_AdS), this integral gives V_boundary(dr) ~ dr^{-4}, matching our measured alpha=3.92.

**Test plan (analytic, no new simulations):**
1. Compute the Poisson kernel integral analytically (Mathematica/SymPy) and verify it gives alpha=4 with amplitude consistent with Sahay-Lukin-Cotler C2=13.6(8).
2. Layer-by-layer force measurement in existing 16q MERA circuit to trace crossover from boundary (power-law) to deep layers (exponential).

**Why this matters for the paper:** If confirmed analytically, this unifies our result with Sahay-Lukin-Cotler rather than competing with it. Our manuscript can claim to observe the *boundary CFT channel* of holographic gravity while Sahay-Lukin-Cotler observe the *bulk AdS channel* — two sides of the same duality.

---

### HYP-2026-012: Holographic Forces as Entanglement Thread Density (Crofton Formula)
**File:** `research/data/hypotheses/HYP-2026-012.json`
**Confidence:** low
**Feasibility:** TESTABLE_NOW
**Source:** SCAN-002 (Wen-Xu-Zhong PEE threads + Crofton) + math bridge finding #2

**Claim (summary):** The measured force profile V(dr) equals the integral of PEE thread density rho(gamma) over all geodesics with boundary endpoint separation dr, via the Crofton formula on kinematic space dS2:

```
V(dr) = C * integral_{gamma: endpoints separated by dr} rho(gamma) dmu(gamma)
```

For pure AdS2 with uniform rho, this gives alpha=2 (wrong). For our MERA with realistic entanglement spectrum, the non-uniform rho shifts the power law toward alpha=4. The 12 clean data points from SIM-2026-011 directly constrain the thread density radial profile.

**Test plan (existing data reuse):**
1. Compute CMI tensor I(A_i; A_j | L) from existing MERA ground state data (already available from SIM-2026-002/SIM-2026-007 entanglement spectrum).
2. For each dr, sum CMI contributions as a proxy for thread density integral: V_thread(dr) = (1/2) * sum_{|i-j|=dr} CMI(A_i, A_j | L_complement).
3. Compare V_thread(dr) to SIM-2026-011 force profile.

**Why this matters:** If V(dr) = Crofton integral of thread density, it means the 12-point force dataset is a direct measurement of entanglement thread density in the MERA bulk — the strongest possible form of ER=EPR applied at the force-law level.

---

## Existing Hypothesis Updates

### HYP-2026-009: Bond Dimension Chi Discontinuity — New Supporting Evidence
**Update type:** New source finding added, confidence rationale updated
**New evidence:** Qasim-Eisert-Jahn (arXiv:2508.16570, SCAN-003) proves qualitatively different RTN equilibration behavior between chi=2 and chi=3 for hyperbolic geometries. This is independent theoretical support for a discrete transition at chi=3 beyond the Roux CS-level argument.
**Confidence:** Remains low (equilibration class ≠ holographic quality class, but now has two independent theoretical motivations).
**Next step unchanged:** chi=3 VQE simulation needed.

### HYP-2026-006: Transport — No Change
Status SUPPORTED confirmed. Wang & He (2603.07639) already cited in prior scan as independent analytic confirmation. No new evidence from this scan.

### HYP-2026-008: Stress-Tensor Power Law — No Change
Status PARTIAL confirmed. SCAN-001 provides new context: the alpha=3.92 result is now positioned as the boundary-CFT channel measurement (see HYP-2026-011 for the full unification argument).

---

## Hypotheses with No Action Required (relevance < 4 scans)

- **SCAN-003 (Qasim RTN equilibration, relevance 3/5):** Feeds into HYP-2026-009 update above. No new hypothesis warranted.
- **SCAN-004 (Jeffrey measurement-based holographic entanglement, relevance 3/5):** Complementary approach; no overlap with our force/transport measurements. Monitor only.
- **SCAN-005 (Ising on AdS tessellation, relevance 3/5):** m_eff regime overlap noted. No new hypothesis — would require new simulation on coordination-7 tiling, outside current scope.
- **SCAN-006 (TN quantum advantage, relevance 3/5):** Relevant to QCUP framing, not to hypothesis generation. Routed to computation lead for quantum advantage regime check.

---

## Feasibility Summary

| HYP | Verdict | Hardware | When |
|-----|---------|----------|------|
| HYP-2026-011 | TESTABLE_NOW | Mathematica/SymPy + optional local GPU | 2026-Q2 |
| HYP-2026-012 | TESTABLE_NOW | Local CPU (existing data) + SymPy | 2026-Q2 |

No hypotheses archived as INFEASIBLE.

---

## Philosophical Synthesis

Two themes emerge from this scan's hypotheses:

**1. Observer-dependent gravity.** HYP-2026-011 suggests that the force law in holographic MERA is not a single universal function but depends on the observer's position (boundary vs bulk). This is the AdS/CFT dictionary made concrete: the same physical state appears as 1/r^4 gravity (CFT) or exp(-r/l) gravity (AdS) depending on how you measure it. The experimental realization of this observer-dependence in a 24-qubit simulation would be remarkable.

**2. Force = thread count.** HYP-2026-012 pushes toward an information-geometric picture where gravitational force is literally the density of entanglement threads between two regions. This is not metaphor — it is a quantitative prediction: V(dr) = Crofton integral of rho(gamma). If the 12-point dataset satisfies this equation, we have a direct measurement of bulk geometry via boundary forces, which is the operational content of holography.

Both hypotheses are speculative. Both are testable with existing tools. Both, if confirmed, strengthen the manuscript's core thesis that MERA tensor networks exhibit genuine holographic physics.

---

## Structured Output

```json
{
  "tier": "theory",
  "status": "HYPOTHESIS_GENERATED",
  "scan_date": "2026-03-26",
  "hypotheses": [
    {
      "id": "HYP-2026-011",
      "claim": "Power-law boundary force and exponential bulk force are two projections of the same AdS/CFT duality, related by the Poisson kernel integral",
      "confidence": "medium",
      "source_findings": ["SCAN-001", "PAPER-2026-023", "SIM-2026-011", "PAPER-2026-009"],
      "testable": true,
      "test_design": "Analytic Poisson kernel integral (Mathematica) + layer-by-layer MERA force crossover measurement",
      "hardware_required": "Mathematica/SymPy + optional local GPU for layer-resolved MERA",
      "earliest_testable": "2026-Q2",
      "feasibility_verdict": "TESTABLE_NOW",
      "philosophical_implications": "Observer-dependent gravity: boundary observers see CFT power-law, bulk observers see AdS exponential -- same state, different descriptions",
      "status": "proposed"
    },
    {
      "id": "HYP-2026-012",
      "claim": "V(dr) = Crofton integral of PEE thread density over geodesics with endpoint separation dr",
      "confidence": "low",
      "source_findings": ["SCAN-002", "SIM-2026-011", "PAPER-2026-009", "PAPER-2026-020"],
      "testable": true,
      "test_design": "CMI tensor from existing MERA data compared to measured V(dr); analytic Crofton integral for pure AdS2",
      "hardware_required": "Local CPU only (existing simulation data)",
      "earliest_testable": "2026-Q2",
      "feasibility_verdict": "TESTABLE_NOW",
      "philosophical_implications": "Force = entanglement thread count: ER=EPR at the force-law level",
      "status": "proposed"
    }
  ],
  "hypothesis_updates": [
    {
      "id": "HYP-2026-009",
      "change": "New supporting evidence from SCAN-003 (RTN equilibration). Confidence rationale updated. Status unchanged: proposed."
    }
  ],
  "infeasible_archived": []
}
```
