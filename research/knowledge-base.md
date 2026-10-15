# Quantum Worldline Knowledge Base

Accumulated core knowledge from research operations. Updated by Synthesis Agent.

> ### ⚠ Advisory, 2026-08-17 — this file predates the audit
> Content below was written before `docs/governance/AUDIT-2026-08-11.md`. Two classes of statement in
> it are now withdrawn, and are **not** individually annotated here:
> 1. **Any force-exponent value near 4** (α = 4, α ≈ 4, 2Δ_T = 4, 3.92 / 3.97 / 4.07). The published
>    exponent is an estimator artifact; the measured value is **α = 2.6 ± 0.2** with the exchange
>    channel **open**. See `research/data/simulations/SIM-2026-072.json` and `ERRATA.md` E6/D7.
> 2. **The 0.72% transport residual.** A dt = 0.05 grid artifact; dt-converged is −1.21% at N = 16
>    (`ERRATA.md` E2), and the geometric reading of that agreement is itself disputed
>    (AUDIT D-1 resolution, D-12, D-13; `HYP-2026-006.json` → `confidence_downgraded_2026_08_17`).
>
> The literature entries, hardware records and method notes below are unaffected. **Check
> `ERRATA.md` before quoting any number from this file.**

**Last updated:** 2026-08-06 (scan #18 reconciliation). Frontier table VALUES re-verified: **no record in
the table has moved since 2026-05-15.** Scans #11–#18 (HW-2026-068..074) added roadmaps, deployments,
funding, and method demos — none frontier-beating.

**Scans #11–#18 hardware summary (nothing above the rel-3 cataloguing bar since HW-074):**
- **#11 (06-25)** QuEra gigaquop FTQC roadmap names an 8×8-TFIM flagship (HW-068) → seeded HYP-029.
- **#15 (07-14)** HW-070→074 catalogued.
- **#16 (07-19)** IBM ~25× qubit-reset speedup; Google Willow RL mid-circuit calibration (~31% logical
  error reduction). Both rel 2 — throughput/calibration engineering, no new count or fidelity record.
- **#17 (07-21)** Quantinuum/SoftBank white paper; QuEra Libra re-report; SaxonQ NV launch. All rel ≤2.
- **#18 (07-27)** RIKEN "ROQUO" (Quantinuum Reimei + NVIDIA Blackwell hybrid quantum-HPC); IBM $50M DOE
  Genesis Mission commitment and HRL Laboratories acquisition (interconnect/cryogenics for
  Starling-2029); EuroHPC MeluXina-Q (silicon spin, 10→80+ qubits); OptQC MoQuren (first Japanese
  commercial optical machine); Infleqtion Sqale (>50 logical, 2027 *delivery*); Northwestern
  entanglement over 24.4 km live commercial fiber alongside 800 Gbps classical traffic. All rel ≤2 —
  integration, funding, deployment, and networking, none a current-frontier number.

**Reading the pattern:** the frontier table has been static for ~3 months while announcement volume has
stayed high. Vendor news since scan #10 has been about *integration* (quantum+HPC), *supply chain*
(IBM/HRL), *funding*, and *networking* — not about qubit counts or fidelities. Treat press volume as a
poor proxy for frontier movement.

See "Notable since scan #7" below for the earlier reconciliation.

## Current Hardware Frontier

| Metric | Best Value | Organization | Processor | Date |
|---|---|---|---|---|
| Physical qubits (array) | 6,100 | Caltech | Neutral atom tweezer | Sep 2025 |
| Physical qubits (gate-based, trapped-ion) | 256 | IonQ | 6th-gen (Cambridge) | Mar 2026 |
| Physical qubits (gate-based, superconducting) | 120 | IBM | Nighthawk | Nov 2025 |
| Physical qubits (neutral atom, QPU target 2026) | 256 | Pasqal | Vela | 2026 target |
| Physical qubits (modular) | 1,386 (single chip); 4,158 (3-chip) | IBM | Kookaburra | 2026 target |
| Logical qubits (demonstrated) | **96** (error-corrected, [[16,6,4]] code) | **QuEra / Harvard / MIT** | **448-atom reconfigurable array** | **Jan 2026** | [FRONTIER UPDATE — exceeds prior record of 48 EC / 94 ED on Helios]
| Logical qubits (error-detection, trapped-ion) | 94 | Quantinuum | Helios | Feb 2026 |
| Logical qubits (error-correction, trapped-ion) | 48 | Quantinuum | Helios | Feb 2026 |
| Logical qubits (target 2026) | 100 | QuEra | Gen-3 neutral atom | 2026 target |
| Error correction ratio (demonstrated hardware) | ~4.67:1 (96 LQ from 448 phys) | QuEra / Harvard | 448-atom array | Jan 2026 |
| Error correction ratio (simulated qLDPC) | **~2:1** (1,156 LQ from 2,304 phys) | **QuEra / Harvard / MIT** | **qLDPC co-design for neutral atom** | **Apr 2026** | [FRONTIER UPDATE — best ratio demonstrated in any architecture, simulation]
| Logical gate error rate | ~1e-4 (1 per 10,000 ops) | Quantinuum | Helios | Feb 2026 |
| Logical memory error rate (qLDPC simulated) | 1.3e-13 per logical per round | QuEra / Harvard | qLDPC neutral-atom design | Apr 2026 |
| Two-qubit gate fidelity | 99.99% (four nines) | IonQ | Tempo (EQC) | Oct 2025 |
| Coherence time | 350 us | IBM | Nighthawk | Jan 2026 |
| Circuit depth | **7,500+ gates** (accurate observable estimation with PEA mitigation) | IBM | **Nighthawk r2** | **Aug 2026** | [FRONTIER UPDATE 2026-10-15: was 5,000 gates (Nighthawk, Jan 2026). Source: https://www.ibm.com/quantum/blog/nighthawk-r2 (2026-08-31), restated in IBM Q3 2026 update (2026-10-07). HW-2026-076]
| Circuit depth (target) | 7,500 gates | IBM | Nighthawk iteration | End 2026 |
| Quantum volume | 2^25 (33.5M) | Quantinuum | H2 | 2025 |
| Algorithmic qubits | 64 | IonQ | Tempo | 2026 |

### Notable since scan #7 (scans #8-#10, HW-2026-055..067 — none frontier-beating, but project-relevant)
| Entry | What | Relevance to us |
|---|---|---|
| **HW-062 QuEra Gemini** | 260q neutral-atom gate-model, 99.2% 2q, **collaboration-available** | **The realistic platform for our force-existence test.** (α≈4 struck 2026-08-17 — the target exponent is now α = 2.6 ± 0.2, channel open; the test itself is unaffected, and the V_T/V_X channel discrimination is now the measurement worth running.) Inquiry SENT 2026-06-16 (thread 19ed11650e5ed845). Not a fidelity record; it's the *accessible* route. |
| **HW-061 Quantinuum Sol** (2027 roadmap) | 192q / **99.98% 2q** / 10k-gate budget | Would run the chi=3 16q transport circuit bare-metal (~4-5k ops) when it ships. Best near-future fit. |
| **HW-064 QuEra Libra** (2028 roadmap) | 256 logical / megaquop / ~1e-6 error, on demonstrated 3,000-phys array | Long-game; extends the Gemini collaboration route to fault-tolerant scale. |
| HW-055 ion qLDPC breakeven | 4 logical / 18 phys, 9× better logical error vs prior | Method milestone (breakeven demo), not a count record. |
| HW-063 USTC neutral-atom | sustained 99.81% 2q via erasure detection across rounds | Multi-layer-MERA fidelity relevance. |
| HW-066 Atom Computing | >1,200 physical qubits + $300M raise | Scale/funding, not a demonstrated logical record. |
| HW-067 Pasqal Orion | 140q deployed at CINECA (Italy) | Deployment milestone. |

**Bottom line for our experiment:** IonQ's 99.99% 2q remains the fidelity ceiling, but the *collaboration-accessible* platforms (Gemini now, Sol 2027) are what matter for actually running the test. No record in the table above moved 2026-05-15 → 2026-06-17.

## Key Milestones

- 2026-05-15: Scan #7 -- hardware scan, window 2026-04-26 to 2026-05-15, 5 new entries HW-2026-050 to 054. No new frontier records. New: eleQtron MAGIC €57M Series A (new European trapped-ion vendor), IonQ 256q first fab chip samples back + first system sale confirmed (Q1 earnings), IonQ DARPA HARQ program (modular networking), Google Willow EAP deadline (105q research access), IonQ Tempo KISTI South Korea deployment finalized.
- 2026-05-15: Scan #6 -- hardware-only scan, window 2026-04-26 to 2026-05-12, 6 entries HW-2026-044 to 049. FRONTIER UPDATES: QuEra 448-atom / 96 logical qubits (Jan 2026, caught up); QuEra qLDPC 2:1 ratio simulation (arXiv 2604.16209, Apr 2026). New: IonQ 256q shipped to Cambridge (May 2026), Hanyuan-2 dual-core (China, 200 qubits, May 2026), Pasqal first logical-qubit application (Apr 2026), Helios SDU deployment (May 2026).
- 2026-04-26: Scan #5 -- 11 papers (PAPER-042 to 052), 9 hardware entries (HW-023 to 031). Key: MERA on trapped-ion hardware demonstrated (Miao et al., CONFIRMED), PEE-thread Crofton tessellation NOVEL, IonQ 256q Cambridge, Pasqal Vela 256q, Google dual-modality neutral atom expansion. Our Zenodo paper published 2026-04-20, too early for citation tracking.
- 2026-03-17: Scan #4 -- 5 papers (PAPER-034 to 038), 5 hardware milestones (HW-018 to 022). Key: Helios commercially available NOW, Lin thread embodiment (NOVEL), Miao-Barthel published in Quantum, symmetry-VQE floor confirmed.
- 2026-03-14: Weekly scan #3 -- 8 papers (PAPER-026 to 033), 5 hardware milestones (HW-013 to 017). Key: MERA barren-plateau-free proof, velocity Verlet VQE optimizer, IonQ 256-qubit announcement
- 2026-03-11: Full research scan #2 -- 7 new papers (PAPER-019 to 025), 4 new hardware milestones (HW-009 to 012)
- 2026-03-17: Quantinuum Helios COMMERCIALLY LAUNCHED -- cloud + on-premise, 98 phys / 94 logical, 99.921% 2Q fidelity. Apply for research access NOW.
- 2026-03-10: Quantinuum Helios: 94 logical qubits beyond break-even, iceberg codes (arxiv 2602.22211)
- 2026-03: First weekly scan by Worldline Orchestrator team
- 2026-01: AI-optimized lattice QFT actions solve 30-year problem (TU Wien, PRL)
- 2025-11: IBM Nighthawk (120 qubits) and Loon (qLDPC validation) unveiled
- 2025-11: 112-qubit Schwinger model vacuum simulation (largest digital QFT sim)
- 2025-10: Google Quantum Echoes -- 13,000x speedup, first verifiable quantum advantage for physics
- 2025-09: Quantinuum H2 reaches 56 qubits, QV 33.5M, 800x error suppression, 12 logical qubits
- 2025-09: Caltech 6,100-qubit neutral atom array (not yet entangled)
- 2025-04: First 2D lattice QED simulation using qudit trapped-ion quantum computer (Nature Physics)
- 2025-02: Microsoft unveils Majorana 1 -- first topological QPU (8 qubits, controversial)
- 2025-02: Photonic SHYPS codes: computation in qLDPC with 20x overhead reduction
- 2025: Universal Yang-Mills framework via orbifold lattice (Halimeh et al.)
- 2025: Emergent holographic forces measured in MERA tensor networks (Sahay, Lukin, Cotler, PRX)
- 2025: Google AlphaQubit neural-network decoder (6% over tensor networks, 30% over correlated matching)
- 2025: Google Willow below-threshold error correction (105 qubits)
- 2025: IBM + RIKEN 77-qubit iron-sulfur biological cluster simulation
- 2025-06: 12-amino-acid protein folding on 36-qubit trapped-ion system
- 2026-02: 80-qubit curved spacetime simulation on IBM Heron
- 2026-02: QuPepFold -- hybrid quantum-classical protein folding for disordered proteins (90% fidelity on IonQ Aria-1)
- 2025-06: Emergent holographic forces published in PRX (Sahay, Lukin, Cotler) -- C1=0.080, C2=13.6, l_AdS=1/log(2)
- 2025-01: Hologron instability and holographic transportation discovered (Wang & He)
- 2025-12: Multi-particle worldline Monte Carlo formalism extended (Edwards et al.)
- 2025-02: Trotterized MERA polynomial quantum advantage demonstrated (Miao & Barthel)
- 2024-12: First log-law entanglement scaling at criticality on quantum hardware via MERA (Miao et al., updated Aug 2025)
- 2026-04-20: Our paper published on Zenodo (DOI: 10.5281/zenodo.19661227 v3). Under SciPost review.
- 2026-05-13: IonQ 256-qubit 6th-gen chip-based system shipped to Cambridge Cavendish Lab (Ray Dolby Centre). No fidelity benchmarks released yet for 256q system at time of shipment.
- 2026-05-08: China's Hanyuan-2 (CAS Cold Atom Technology): world's first dual-core neutral-atom quantum computer, 200 qubits (100 Rb-85 + 100 Rb-87). Architecture novelty only -- no gate fidelity or benchmark results published.
- 2026-05-07: Quantinuum Helios: University of Southern Denmark (SDU) gained research access via DeiC, operating at 48 logical qubits. Confirms transatlantic commercial research availability.
- 2026-04-20: QuEra / Harvard / MIT: arXiv 2604.16209 -- ultra-high-rate qLDPC codes simulated at ~2:1 physical-to-logical ratio (1,156 LQ from 2,304 physical) on neutral-atom architecture. Error rate 1.3e-13 per logical per round. Best demonstrated ratio in any architecture (simulation).
- 2026-04-10: Pasqal: first end-to-end application (differential equations) solved using logical qubits on neutral-atom hardware. 2 logical qubits; logical outperformed physical.
- 2026-01-19: QuEra / Harvard / MIT / UMD / Caltech / ARL: 448-atom neutral-atom array demonstrates 96 logical qubits using [[16,6,4]] qLDPC code. 2.14(13)x below-threshold QEC. Universal FT stack on single platform. Published Nature vol 649. Doubled prior logical qubit record in 13 months.
- 2026-05-15: Google Willow Early Access Program deadline. 105-qubit Willow open to research proposals (selection 2026-07-01). First research access path to Google's below-threshold QEC superconducting platform.
- 2026-05-06: IonQ Q1 2026 earnings: first 256-qubit ion trap chip samples back from fab. First 256q system sale confirmed (Cambridge). Revenue $64.7M, +755% YoY. 256q commissioning results expected H2 2026.
- 2026-05-05: eleQtron (Germany) secures €57M Series A. MAGIC microwave-controlled trapped-ion platform with claimed 10s coherence time. Systems deployed to DLR and FZ Jülich. New European trapped-ion vendor to track.
- 2026-04-14: IonQ selected for DARPA HARQ (Heterogeneous Architectures for Quantum) program. Focuses on diamond-core quantum memories for multi-technology modular networking (trapped-ion + neutral atom + superconducting hybrid).
- 2026-01-16: IonQ Tempo (100-qubit, 99.99% 2Q fidelity) delivery agreement finalized with KISTI South Korea. Integration into KISTI-6 HPC cluster; first onsite hybrid quantum-classical deployment in South Korea.
- 2026-04-07: Rigetti Cepheus-1-108Q generally available (99.1% 2Q fidelity, Amazon Braket + QCS)
- 2026-04-06: MBL protects holographic geometry in random tensor networks (Liang, arxiv:2604.04596)
- 2026-03-24: Google Quantum AI expands to neutral atoms (Dr. Adam Kaufman, CU Boulder; QuEra collaboration)
- 2026-03-11: IonQ 256q partnership with University of Cambridge at Cavendish (Ray Dolby Centre)
- 2026-01: QuEra Gemini-class system delivered to AIST Japan (260 phys / ~37 logical qubits)
- 2025-12: Holographic tensor networks as PEE-thread tessellations of geometry (Wen, Xu, Zhong; exact RT formula)
- 2023: Holographic quantum simulation of L=32 Ising on 10 qubits, Quantinuum (Anand et al., PRX Quantum)

## Active Research Threads

- Quantum simulation of curved spacetime (1+1D and 2+1D models)
- **Universal Yang-Mills simulation via orbifold lattice** -- first explicit circuits scalable to continuum limit for any SU(N), any dimension (Halimeh et al., 2025)
- **2D lattice gauge theory on qudit hardware** -- trapped-ion qudits break 1D barrier (Meth et al., Nature Physics 2025)
- **Emergent holographic forces from MERA tensor networks** -- quantitative AdS gravity predictions testable on quantum simulators (Sahay et al., PRX 2025). **CAVEAT:** hologrons are dynamically unstable (Wang & He 2025) with tau ~ 0.5-0.85/J; stable excitations must be constructed from boundary CFT primaries. **Stable excitation formula:** `sigma^boundary_j = 0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})` (leading order). Static force profiles (energy differences) are still valid but cleaner with boundary-primary excitations.
- **Hologron instability mechanism** -- root cause: spin-flip hologron basis is incomplete (misses 2^4 IR core states). No energy gap separates 1-hologron from 2-hologron+IR sectors. Model-dependent: hologrons ARE stable for H_C-Ising (Chua 2017) because X_j IS the primary there.
- **Flat force profile diagnosis (SIM-2026-005)** -- NOT caused by hologron instability directly (static energy differences are well-defined for unstable states). Caused by VQE convergence failure: Z2 projection non-smooth landscape -> 3.22% energy error. Fix convergence first (penalty method), then optionally switch to boundary-primary excitations for cleaner observable.
- **Holographic transportation** -- boundary excitations vanish at t~1.5/J and reappear at t~2.5/J (L=16, J=1, Omega=5). Perturbation uses Y_i coupling (not X_i or Ry). Robust against M!=0 and off-criticality detuning. Observable is boundary excitation density rho^boundary_i[Y_i](t) = <Y_i>(t) - <Y_i>_GS. No VQE needed -- pure time-evolution measurement.
- **Worldline-MERA bridge** -- worldline path integrals on AdS compute bulk-to-bulk propagators (Ashok & Murthy 2017) whose geodesic approximation matches the MERA hologron force profile. Potential unification of worldline QFT and tensor-network holography.
- **Superspace worldline = quantum gravity** -- Roux (2026, PAPER-2026-023) shows QG Hamiltonian IS a worldline formalism in superspace. Keldysh partition function -> Euclidean 3D gravity -> two CS theories -> WZW -> 2D Liouville CFT (c=25, Q=2). Virtual graviton propagator ~ 1/|z_i - z_j|^4 (power-law, NOT exponential) from cosmological boundary. CS level k must be integer (quantization condition); minimum time step beta_m = sqrt(Lambda) * Planck units. **Key distinctions from scalar propagation:** graviton exchange (spin-2, Delta=1) gives power law; scalar (spin-0, Delta=1/8 for Ising) gives exponential. Liouville vertex operator interpretation explains why boundary-primary excitations give cleaner force profiles than Pauli-X hologrons. Deep analysis: research/data/papers/roux-superspace-analysis.md
- **Entanglement thread embodiment (Lin, PRL 2026, arXiv:2501.10691)** -- thread trajectories in holographic bulk are exactly geodesics (proved via no-return rule on RT surfaces). Thread flux = (1/2)*CMI. Each MERA tensor contributes chi threads. Kinematic space (dS2 geometry) acts as circuit board organizing threads as wires. Thread-state correspondence: each thread carries GHZ-like state among all bulk sites it passes through. Key connection to our work: (1) V(dr) ~ CMI/2 = thread flux F_{ij} -- testable from existing theta files with ~30 lines Python. (2) Transport time T = (pi/2)*l_AdS is the null geodesic condition in thread language. (3) Force profile should be geodesic formula V(dr) ~ dr/sqrt(dr^2 + dr^4/(4*l_AdS^2)) (power-law at large dr), not exponential. (4) Bond dimension chi=2->3 is a discrete thread count jump (supports HYP-2026-009). (5) Max signal range at dr ~ 2^(L-1) from thread counting. Full analysis: research/data/papers/lin-thread-analysis.md
- **Composite geodesics for transport time** -- Bohra & Sivaramakrishnan (2025) show composite timelike-spacelike geodesics connect timelike-separated boundary points in AdS. May explain factor-of-2 discrepancy in holographic transport: pure spacelike geodesics undercount by factor ~2 vs composite paths. Directly relevant to our HYP-2026-006 transport time measurement.
- **Worldline MC on curved space** -- Corradini & Muratori (2020) developed numerical worldline MC on D-spheres and D-hyperboloids. Foundational methodology for HYP-2026-007.
- **Multi-particle worldline Monte Carlo** -- extended to interacting multi-particle systems (Edwards et al., Dec 2025). Scalable alternative to VQE for extracting interaction potentials.
- **MERA provably barren-plateau-free** -- Barthel & Miao (Comm. Math. Phys. 2025, arXiv:2304.00161) prove gradient variance scales polynomially with system size for MERA, MPS, and TTN. Mathematical guarantee of trainability for randomly initialized tensor network states. Our VQE convergence issues are definitively from Z2 symmetry-breaking basins, NOT from MERA architecture.
- **MERA on quantum hardware** -- 10-qubit L=32 Ising on Quantinuum (2023), log-law entanglement at criticality on trapped ions (2024), polynomial quantum advantage for Trotterized MERA (2025). **First log-law entanglement scaling** at criticality demonstrated on 12-qubit trapped-ion system (Miao et al., arXiv:2412.18602, 2025): binary MERA chi=2 up to T=5 layers probed L=96 Ising, using symmetry-constrained gate compilation preserving Z2 and time-reversal. Methodology directly applicable to our Helios design.
- **Velocity Verlet VQE optimizer** -- momentum-based optimizer from molecular dynamics outperforms L-BFGS-B on molecular VQE (Miura 2026, arXiv:2603.09862). Inertial velocity term helps escape local minima. Potential application to our Z2 penalty VQE convergence issues.
- **Measurement-based holographic entanglement** -- Jeffrey, Gandarias, Schleier-Smith, Swingle (arXiv:2601.21065, Jan 2026). Alternative to MERA for preparing states with Ryu-Takayanagi entanglement using only Gaussian operations. Demonstrated on hyperbolic disk and wormhole geometries. Could provide independent cross-check of MERA-based holographic force measurements.
- qLDPC error correction codes (IBM Kookaburra qLDPC+LPU 2026, Photonic SHYPS 20x reduction, Tsinghua self-dual codes)
- **AI-optimized lattice QFT actions** -- neural network fixed-point formulations (TU Wien, PRL Jan 2026)
- Neutral atom scaling path (QuEra 100 logical qubit target 2026 -- effectively achieved at 96 LQ in Jan 2026; 2:1 ratio qLDPC simulation Apr 2026 points toward teraquop-scale fault tolerance)
- IBM roadmap: Kookaburra (2026) -> Cockatoo (2027) -> Starling (200 logical qubits, 100M gates, 2029)
- Google AlphaQubit -- AI-powered error correction decoder, core component of Willow
- Hybrid quantum-classical molecular simulation (IBM + RIKEN + Fugaku)
- **Biological quantum modeling** -- QuPepFold for disordered proteins, VQE on IonQ hardware
- Microsoft topological qubits -- Majorana 1 (early stage, controversial, DARPA US2QC)
- **Holographic tensor network tessellations** -- Wen, Xu, Zhong (2025) achieve exact Ryu-Takayanagi formula using PEE-thread tessellations of AdS, overcoming discrete approximation limits of existing holographic TNs
- **Tensor networks for quantum computing** -- Major Nature Reviews Physics review (Berezutskii et al., 2025): 30+ researchers from industry/academia. Notes MERA criticisms (preferred directions from unitary tensors) but establishes TN as mainstream QC tool
- **Quantinuum Helios beyond break-even** -- 94 logical qubits (error-detection) and 48 logical qubits (error-correction) on 98-qubit Helios. Iceberg codes with ~1:1 physical-to-logical ratio. Logical gate error rate ~1e-4. Upgrades MERA hardware feasibility significantly.
- **IonQ Tempo #AQ 64** -- 100-qubit trapped-ion, 99.99% two-qubit gate fidelity (four nines). Roadmap: 256 qubits at 99.99% by 2026
- **IonQ 256-qubit 6th-gen system** -- announced March 2026, chip-based 256-qubit trapped-ion to be deployed at University of Cambridge Cavendish Laboratory. Will be UK's most powerful quantum computer. If maintains Tempo-level fidelity, enables 8+ layer MERA circuits representing L=768 sites. Alternative hardware target to Helios for deep holographic MERA.
- **Quantinuum Helios Singapore expansion** -- first international Helios deployment outside US announced March 2026, R&D centre in Singapore. Specs unchanged from Nov 2025 launch. Quantinuum filed for IPO January 2026.
- **Pasqal Vela QPU** -- 256+ neutral atom qubits, targeting quantum advantage demo H1 2026. 140-qubit system delivered to Italy CINECA. Going public at $2B valuation.
- **IBM Nighthawk 100-qubit physics demo** -- 10x10 grid thermalization study (Alam et al., arXiv:2603.12236, March 2026). Quantum simulation validated against tensor-network benchmarks, accessing volume-law entanglement regime beyond classical reach.
- **PsiQuantum deployment shift** -- CEO transition Feb 2026, shifting from R&D to deployment execution. Omega photonic chipset manufactured at GlobalFoundries.

## Active Hypotheses

| ID | Claim | Feasibility | Status |
|---|---|---|---|
| HYP-2026-001 | Orbifold lattice + qudit encoding for 2+1D QCD | TESTABLE_NEAR_TERM | proposed |
| HYP-2026-002 | Holographic force verification on Quantinuum Helios (98q, was H2) | **TESTABLE_NOW** | proposed |
| HYP-2026-003 | AI-optimized lattice actions for worldline path integrals | TESTABLE_NEAR_TERM | proposed |
| HYP-2026-004 | QuPepFold extension to photosynthetic quantum coherence | TESTABLE_NEAR_TERM | proposed |
| HYP-2026-005 | MERA force profile = discretized worldline propagator in AdS | **TESTABLE_NOW** | proposed |
| HYP-2026-006 | Holographic transportation time = worldline geodesic proper time | **TESTABLE_NOW** | proposed |
| HYP-2026-007 | Worldline Monte Carlo on hyperbolic lattice reproduces MERA forces | **TESTABLE_NOW** | proposed |
| HYP-2026-008 | Stress-tensor boundary primaries produce power-law (not exponential) force: V ~ 1/dr^4 | NEEDS_SIM | proposed |
| HYP-2026-009 | Roux CS level quantization -> MERA bond dimension chi=3 gives discontinuous quality jump | NEEDS_SIM | proposed |
| HYP-2026-010 | 0.72% transport time residual scales as l_AdS^2 (Roux graviton exchange correction) | **TESTABLE_NOW** | proposed |

## Core Mission Focus Areas

1. Worldline simulation -- can we mathematically describe 4D worldlines and compute time-slices?
2. Temporal projection -- what are the mathematical shortcuts for projecting higher-dimensional structure?
3. Biological quantum modeling -- path from molecular simulation to cellular-scale quantum modeling
4. Hardware readiness -- tracking when specific simulations become feasible

## Hardware Readiness Assessment (updated 2026-03-14)

| Simulation Target | Qubits Needed | Error Correction Needed | Earliest Feasible |
|---|---|---|---|
| 1+1D curved spacetime (Dirac field) | 8-20 | No (NISQ tolerant) | **NOW** (Qiskit sim) |
| 2D lattice QED (single plaquette) | 4-8 qudits | No | **NOW** (qudit trapped-ion) |
| 2+1D SU(2) Yang-Mills | 50-200 | Likely needed | 2027-2028 |
| Holographic force measurement (MERA) | 40-256 | No (noise-robust) | **NOW** (Quantinuum Helios 98q, IonQ 256q 6th-gen) |
| Small protein folding (IDP) | 20-40 | Helpful (VQE tolerant) | **NOW** (IonQ Tempo, #AQ 64) |
| Full QCD (3+1D) | 10,000+ | Required (qLDPC) | 2029+ (IBM Starling) |
| Worldline 4D path integral | 100-1,000 logical | Required | 2028-2030 |
| MERA holographic transportation | 16-24 | No (noise-robust) | **NOW** (Qiskit sim, Quantinuum Helios) |
| Worldline Monte Carlo on AdS lattice | N/A (classical) | N/A | **NOW** (classical CPU) |
| MERA with error correction | 48-94 logical | Yes (iceberg codes) | **NOW** (Quantinuum Helios, beyond break-even) |
| Deep MERA (8+ layers, L=768) | 256 | No (if high fidelity) | **NEAR-TERM** (IonQ 256q 6th-gen, 2026) |
