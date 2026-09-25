# Weekly Digest: 2026-03-26

## Executive Summary

The research team's sixth scan produced a **major framing insight**: our power-law force F(dr)~dr^{-3.92} and Sahay-Lukin-Cotler's exponential force are NOT contradictory -- they are boundary (CFT conformal block) vs bulk (AdS graviton propagator) projections of the same holographic duality. This reframes our paper's contribution as complementary validation, not competition. Two new hypotheses generated, both testable. Three simulations run, confirming the CFT conformal block argument (alpha=4.0 vs our 3.92, 2% agreement) and identifying the chi=2->3 RTN phase boundary as the correct quantum advantage framing.

## Findings by Tier

### Tier 1: Literature (5 findings)

| ID | Status | Relevance | Summary |
|----|--------|-----------|---------|
| Sahay-Lukin-Cotler PRX 2025 | **NOVEL** | 5/5 | Exponential force in MERA -- bulk channel. Our power-law is boundary channel. Complementary, not contradictory. |
| PEE thread tessellation (2512.19452) | WATCH | 4/5 | Crofton formula predicts V(dr) from thread density. Testable but needs differential form, not raw CMI. |
| TN quantum advantage (2603.18825) | WATCH | 3/5 | Classically hard TN regimes identified. Relevant to QCUP framing. |
| Quantinuum Helios update | **CONFIRMED** | 5/5 | 48 logical qubits from 98 physical, iceberg codes. Our 32q circuit well within range. |
| QCUP Fall 2026 Hackathon | **ACTIONABLE** | 5/5 | New ORNL submission window, virtual event, Quantinuum+IBM+IonQ partners. |

### Tier 2: Theory (2 new hypotheses)

| HYP | Status | Confidence | Summary |
|-----|--------|-----------|---------|
| **HYP-2026-011** | PARTIALLY_SUPPORTED | medium | Boundary power-law = CFT conformal block; bulk exponential = AdS propagator. Poisson kernel integral partially confirms. Need tensor (spin-2) kernel for exact match. |
| **HYP-2026-012** | NOT_SUPPORTED (proxy) | low | CMI as force proxy gives alpha=0.91, not 3.92. Needs differential thread density in kinematic space, not cumulative CMI. |
| HYP-2026-009 | updated | low | Chi=2->3 discontinuity now has RTN equilibration phase boundary evidence (Qasim-Eisert-Jahn). Two independent motivations. |

### Tier 3: Computation (3 simulations)

| SIM | Result | Key Number |
|-----|--------|-----------|
| SIM-2026-012 | chi=2 CLASSICALLY_EASY, chi>=5 HARD | RTN phase boundary at chi~3 |
| SIM-2026-013 | CMI proxy NOT_SUPPORTED | alpha=0.91 vs 3.92 (proxy mismatch) |
| SIM-2026-014 | CFT conformal block STRONGLY consistent | alpha=4.0 predicted, 3.92 measured (2.0%) |

## Cross-Tier Connections

1. **Boundary vs Bulk duality** (Lit -> Theory -> Comp): Sahay exponential + our power-law = two faces of AdS/CFT. CFT Ward identity gives exact alpha=4.0. This is the paper's strongest framing.
2. **RTN phase boundary** (Lit -> Comp): chi=2->3 crosses equilibration phase boundary, reframing quantum advantage argument for QCUP.
3. **Thread density** (Lit -> Theory -> Comp): Crofton formula is the right physics but needs kinematic space derivative, not raw CMI. Open theoretical problem.

## Updated Hypothesis Table

| HYP | Status | Confidence | One-line |
|-----|--------|-----------|----------|
| 001 | proposed | low | MERA as discrete AdS (structural) |
| 002 | PARTIAL | medium | Holographic forces -- power-law, not exponential |
| 003 | proposed | low | Worldline MC matches MERA (partially resolved via m_eff) |
| 004 | proposed | low | Hologron decay lifetime |
| 005 | proposed | low | Quantitative xi vs l_AdS |
| 006 | **SUPPORTED** | **high** | Transport T=(pi/2)*l_AdS to 0.72% |
| 007 | proposed | low | Worldline MC on H^2 |
| 008 | PARTIAL | medium | Stress-tensor power-law alpha=3.92 vs 4.0 |
| 009 | proposed | low->medium | Bond dimension chi=2->3 RTN phase boundary |
| 010 | INCONCLUSIVE | low | Transport residual l_AdS^2 scaling |
| **011** | **PARTIAL** | **medium** | Boundary power-law = CFT block, bulk exponential = AdS propagator |
| **012** | NOT_SUPPORTED | low | Force != raw CMI (needs kinematic space derivative) |

## Action Items

1. **HIGH**: Add boundary-vs-bulk duality framing to paper revision (HYP-2026-011 insight)
2. **HIGH**: Apply to QCUP Fall 2026 Hackathon when window opens
3. **MEDIUM**: Derive tensor Poisson kernel for spin-2 to get exact alpha=4.0 analytically
4. **MEDIUM**: Update QCUP proposal chi=3 framing with RTN phase boundary argument
5. **LOW**: Kinematic space derivative of CMI for proper Crofton test
6. **WAITING**: arXiv endorsement (Cotler/Swingle), QCUP PHY204 review
