# Worldline Deep Dive -- 2026-03-11

**Type:** Focused research query (not weekly scan)
**Query:** Deep dive on worldline physics, simulation, and connections to our holographic force work

---

## Executive Summary

The worldline formalism and MERA holographic forces are currently separate research programs that converge on a shared object: particle propagation in emergent AdS geometry. The Sahay-Lukin-Cotler hologron forces (PRX 2025) measure an interaction potential that has the functional form of an AdS bulk-to-bulk propagator in geodesic approximation. The Ashok-Murthy worldline-to-bulk correspondence (2017) provides the mathematical bridge: worldline path integrals compute exactly these propagators. Three new testable hypotheses emerge from this cross-tier synthesis, all TESTABLE_NOW on existing infrastructure.

---

## Tier 1: Literature Findings

### Worldline Formalism -- State of the Art

The worldline formalism (Strassler 1992, Schubert ongoing) reformulates QFT amplitudes as correlators of a 1D worldline theory -- the relativistic quantum mechanics of propagating particles. Key recent advances:

| ID | Paper | Relevance | Status |
|---|---|---|---|
| PAPER-2026-011 | Multi-particle Worldline Monte Carlo (Edwards et al., Dec 2025) | 4 | **NOVEL** |
| PAPER-2026-013 | Canonical Quantisation of WQFT (Gonzo & Mogull, Mar 2026) | 3 | WATCH |
| PAPER-2026-014 | WQFT Unitarity and On-Shell Action (Haddad et al., Feb 2026) | 3 | WATCH |
| PAPER-2026-018 | Worldline instantons in gravitational fields (Semren & Torgrimsson, Aug 2025) | 3 | WATCH |

**Key finding (PAPER-2026-011):** Edwards et al. extended worldline Monte Carlo to multi-particle systems for the first time. The method generates multiple worldlines and simulates inter-worldline interactions with favorable scaling. This is directly relevant: hologrons are multi-particle excitations in the MERA bulk.

**WQFT gravitational program:** Gonzo, Mogull, Haddad, Jakobsen, Plefka have built a complete WQFT framework for gravitational binary dynamics (post-Minkowskian expansion). While aimed at gravitational wave physics, the unitarity and on-shell action methods could in principle be applied to the emergent gravity we see in MERA.

### MERA and Holographic Forces -- Extended Landscape

| ID | Paper | Relevance | Status |
|---|---|---|---|
| PAPER-2026-009 | Emergent Holographic Forces (Sahay, Lukin, Cotler, PRX 2025) | 5 | **CONFIRMED** (core reference) |
| PAPER-2026-010 | Hologron stability and holographic transportation (Wang & He, Jan 2025) | 5 | **NOVEL** |
| PAPER-2026-015 | Trotterized MERA quantum advantage (Miao & Barthel, Feb 2025) | 4 | **ACTIONABLE** |
| PAPER-2026-016 | Entanglement scaling at criticality on quantum hardware (Miao et al., Dec 2024) | 4 | **ACTIONABLE** |
| PAPER-2026-017 | Holographic quantum simulation on Quantinuum (Anand et al., PRX Quantum 2023) | 5 | **CONFIRMED** |

**Critical new finding (PAPER-2026-010):** Wang & He show that hologrons are **unstable** during dynamic evolution. This is directly relevant to our HYP-2026-002 program: it means static MERA optimization may not capture the full physics. However, they show stable bulk excitations CAN be constructed from boundary CFT primaries. Most remarkably, they discover **holographic transportation** -- boundary excitations that vanish and traverse the bulk along AdS geodesics. This is observable on Rydberg arrays.

**Hardware MERA implementations are real (PAPER-2026-016, 017):** MERA circuits have been run on Quantinuum trapped ions (10 qubits, L=32 Ising model) and other trapped-ion hardware. Log-law entanglement scaling at criticality has been demonstrated. This validates the path from our Qiskit simulations to hardware.

### Worldline-to-Bulk Bridge

| ID | Paper | Relevance | Status |
|---|---|---|---|
| PAPER-2026-012 | A view of the bulk from the worldline (Ashok & Murthy, 2017) | 5 | **NOVEL** (newly identified connection) |

**This is the key bridge paper.** Ashok & Murthy derive AdS heat kernels and bulk-to-bulk propagators from worldline quantum mechanics. They show that:
1. Gauge-fixed worldline path integrals produce AdS propagators
2. Vertex operators on the worldline map to bulk field insertions
3. Geodesic Witten diagrams (which compute CFT correlators) emerge from worldline perturbation theory
4. The bulk-to-bulk propagator in geodesic approximation is G(x,x') ~ exp(-m * d_geo(x,x'))

This directly connects to the Sahay et al. hologron force: V ~ C1 - C2*exp(-dr/l_AdS). The exponential decay with AdS distance IS the geodesic approximation of the worldline propagator.

---

## Tier 2: Computation Assessment

### Current State of Worldline Simulation on Quantum Hardware

**Direct worldline circuits: Gap remains large.** No papers were found that implement worldline path integrals as quantum circuits. The worldline formalism remains a classical analytical/numerical tool (worldline Monte Carlo, worldline instantons). There is no known quantum circuit ansatz for worldline propagators.

**Indirect connection via MERA:** The MERA-to-quantum-hardware pipeline is well established:
- Anand et al. (2023): 10 qubits on Quantinuum, L=32 Ising model
- Miao et al. (2024): trapped-ion MERA with log-law entanglement at criticality
- Miao & Barthel (2025): polynomial quantum advantage for Trotterized MERA

**Our approach (VQE-optimized MERA circuits) is validated** by this broader literature. The Trotterized MERA paper (PAPER-2026-015) is particularly relevant: it shows layer-by-layer initialization improves convergence -- this could help with our Z2 convergence issues.

### How Our MERA Approach Relates to Worldline Methods

| Aspect | MERA Circuit (our approach) | Worldline Path Integral |
|---|---|---|
| What is computed | Hologron energies and correlators | Bulk propagators and heat kernels |
| Underlying geometry | Discrete hyperbolic (MERA network) | Continuous AdS manifold |
| Particles | Hologrons (Pauli-X excitations at bulk sites) | Point particles on geodesics |
| Interactions | Extracted from energy differences E_2h - E_1h - E_1h | Vertex operators on worldlines |
| Force law | V ~ C1 - C2*exp(-dr/l_AdS) | G ~ exp(-m*d_geo) |
| Connection | **The force profile IS the propagator in geodesic approximation** | -- |

The gap: no one has yet shown this mapping rigorously. This is HYP-2026-005.

### Practical Computation Recommendations

1. **Layer-by-layer MERA initialization** (from PAPER-2026-015) should be tried for our Z2-projected optimization
2. **Worldline Monte Carlo on hyperbolic lattice** could provide an independent check on hologron forces without VQE
3. **Holographic transportation test** (from PAPER-2026-010) is a new observable our circuits could access

---

## Tier 3: Theory Analysis

### Cross-Tier Synthesis: Three New Hypotheses

#### HYP-2026-005: Force Profile as Discretized Worldline Propagator (TESTABLE_NOW)
**Claim:** V(dr) from MERA = discretized bulk-to-bulk propagator in geodesic approximation
**Evidence chain:** Sahay et al. force law + Ashok-Murthy worldline-bulk bridge
**Test:** Compare functional forms after metric matching. Extract mass from force profile and compare to mc^2 = 2.5(1).
**Confidence:** Medium. The functional forms match by inspection, but the normalization and discretization effects need quantitative verification.

#### HYP-2026-006: Holographic Transportation as Worldline Geodesic Propagation (TESTABLE_NOW)
**Claim:** Transport time of boundary excitations through MERA bulk matches worldline proper time along AdS geodesics
**Evidence chain:** Wang-He holographic transportation + worldline formalism on AdS
**Test:** Time-evolve MERA state with boundary excitation, measure transport time vs. boundary separation, compare to arccosh formula
**Confidence:** Low. The interpretation is compelling but the instability of hologrons (Wang & He) complicates the picture.

#### HYP-2026-007: Worldline Monte Carlo as Independent Hologron Force Calculator (TESTABLE_NOW)
**Claim:** WMC on discrete AdS lattice reproduces MERA tensor-network hologron forces
**Evidence chain:** Edwards et al. multi-particle WMC + MERA emergent geometry
**Test:** Implement WMC on hyperbolic lattice with MERA metric, sample worldline pairs, extract V(dr)
**Confidence:** Low. The WMC method has only been validated for non-relativistic QM; its extension to curved discrete geometry is speculative.

### Key Theoretical Insight

The worldline formalism and MERA holography are computing the same object from different directions:

```
Worldline (bottom-up):  particle paths on AdS  -->  propagator G(x,x')  -->  forces
MERA (top-down):        entanglement structure  -->  emergent bulk       -->  hologron V(dr)
```

The Ashok-Murthy paper (PAPER-2026-012) provides the dictionary:
- Worldline proper time = MERA layer depth
- Worldline vertex operators = hologron Pauli-X insertions
- Geodesic Witten diagrams = MERA causal cone contractions
- Heat kernel = MERA ascending superoperator

If this mapping is correct, our MERA circuit simulations are performing worldline path integrals in disguise. Every VQE evaluation that computes hologron correlators is sampling a discrete version of the worldline path integral on AdS.

### Hologron Instability Implications for HYP-2026-002

Wang & He's finding that hologrons are dynamically unstable is a significant caveat for our program. It means:
1. Our VQE-optimized static MERA states capture the right energetics but may not represent stable particles
2. The force profile we measure is a property of the static tensor network, not necessarily of dynamically stable excitations
3. The stable excitations (constructed from boundary CFT primaries) have a different construction that we should investigate

This does NOT invalidate our results -- the static force profile still matches AdS gravity predictions -- but it changes the interpretation. The forces are between tensor-network defects, not between stable quasiparticles.

---

## Cross-Tier Connections

1. **Literature (PAPER-2026-012) + Theory (HYP-2026-005):** The Ashok-Murthy worldline-bulk bridge, combined with Sahay et al. force measurements, predicts that MERA forces are discretized worldline propagators. This is the central new insight of this deep dive.

2. **Literature (PAPER-2026-010) + Computation (SIM-2026-005):** Hologron instability (Wang & He) explains why our Z2-projected VQE converges slowly -- we may be fighting against the instability of the hologron ansatz itself. Constructing excitations from boundary primaries (as Wang & He suggest) may be a better circuit design.

3. **Literature (PAPER-2026-011) + Computation (HYP-2026-007):** Multi-particle worldline Monte Carlo could provide an entirely classical cross-check on our quantum-circuit-derived forces, bypassing VQE entirely.

4. **Literature (PAPER-2026-015) + Computation (SIM-2026-005):** Layer-by-layer MERA initialization from the Trotterized MERA paper could accelerate our Z2-projected VQE convergence.

5. **Literature (PAPER-2026-017) + Hardware readiness:** Quantinuum has already run MERA for L=32 Ising. Our 16-qubit MERA circuits are well within demonstrated hardware capabilities.

---

## Recommended Next Steps (Priority Order)

1. **Test HYP-2026-005 analytically** -- compute AdS bulk-to-bulk propagator in geodesic approximation on the MERA discrete metric and compare functional form to our measured V(dr). This requires only pen-and-paper + Python numerics. Highest priority because it's zero-cost and potentially highest-impact.

2. **Try layer-by-layer initialization** for Z2-projected VQE (SIM-2026-005/006) based on PAPER-2026-015 findings. This may resolve the convergence issues.

3. **Investigate boundary-primary excitation construction** per Wang & He (PAPER-2026-010) as an alternative to Pauli-X hologrons. This addresses the instability problem.

4. **Implement worldline Monte Carlo on hyperbolic lattice** (HYP-2026-007) as independent cross-check. Medium priority but could provide a fast classical baseline.

5. **Design holographic transportation measurement** (HYP-2026-006) for our MERA circuits. This is a new observable that would be a strong publication result.

---

## Updated ID Counters

- Last paper ID: PAPER-2026-018
- Last hypothesis ID: HYP-2026-007
- Last simulation ID: SIM-2026-006 (unchanged)

---

## Sources

- [Sahay, Lukin, Cotler - Emergent Holographic Forces (PRX 2025)](https://doi.org/10.1103/PhysRevX.15.021078)
- [Wang & He - Stable excitations and holographic transportation (2025)](https://arxiv.org/abs/2501.03084)
- [Edwards et al. - Multi-particle Worldline Monte Carlo (2025)](https://arxiv.org/abs/2512.24942)
- [Ashok & Murthy - A view of the bulk from the worldline (2017)](https://arxiv.org/abs/1712.00885)
- [Gonzo & Mogull - Canonical Quantisation of WQFT (2026)](https://arxiv.org/abs/2603.05237)
- [Haddad et al. - WQFT Unitarity and On-Shell Action (2026)](https://arxiv.org/abs/2510.00988)
- [Miao & Barthel - Trotterized MERA quantum advantage (2025)](https://quantum-journal.org/papers/q-2025-02-11-1631/)
- [Miao et al. - Entanglement scaling on quantum hardware (2024)](https://arxiv.org/abs/2412.18602)
- [Anand et al. - Holographic quantum simulation on Quantinuum (PRX Quantum 2023)](https://arxiv.org/abs/2203.00886)
- [Semren & Torgrimsson - Worldline instantons in gravitational fields (2025)](https://arxiv.org/abs/2508.01901)
- [Schubert - Lectures on the Worldline Formalism](https://indico.cern.ch/event/206621/attachments/317309/442801/lectures_morelia_CS.pdf)
