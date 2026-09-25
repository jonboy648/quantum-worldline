# Helios MERA Circuit Design — Holographic Force Measurements

**Date:** 2026-03-11
**Hardware:** Quantinuum Helios (HW-2026-009)
**Hypothesis:** HYP-2026-002 (holographic forces), HYP-2026-006 (holographic transport)
**Status:** DESIGN — pending user approval before any hardware submission

---

## 1. Hardware Summary

| Parameter | Value | Source |
|---|---|---|
| Physical qubits | 98 (137Ba+) | HW-2026-009 |
| Logical qubits (error-detection) | 94 (iceberg code, ~1:1 ratio) | HW-2026-009 |
| Logical qubits (concatenated EC) | 48 (beyond-break-even) | HW-2026-009 |
| Two-qubit gate infidelity (physical) | 7.9e-4 | HW-2026-009 |
| Logical gate error rate | ~1e-4 (error-detection mode) | HW-2026-009 |
| SPAM infidelity | 4.8e-4 | HW-2026-009 |
| Connectivity | All-to-all (trapped ion QCCD) | Architecture |
| Single-qubit gate infidelity | 2.5e-5 | HW-2026-009 |

**Key architectural advantage over IBM:** Trapped-ion all-to-all connectivity means the exact binary MERA topology can be implemented with zero SWAP routing overhead. The full causal cone of any MERA layer maps directly to available qubit pairs.

**Key advantage over H2:** Helios provides 94 logical qubits vs H2's 12 logical qubits (at equivalent error-correction overhead). The iceberg code's ~1:1 physical-to-logical ratio is the enabling factor. At H2's 800:1 ratio, 94 physical qubits would yield only ~12 logical qubits — far too few for our MERA sizes.

---

## 2. MERA Qubit Accounting

### Binary MERA Structure

Binary MERA with N boundary qubits and L layers requires:

```
Layer 0 (boundary):    N qubits
Layer 1:               N/2 qubits  (after isometries)
Layer 2:               N/4 qubits
...
Layer L:               N/2^L qubits  --> 1 qubit (top tensor)
Total MERA qubits:     N + N/2 + N/4 + ... + 1 = 2N - 1  (geometric series)
```

For isometries (3-to-1 qubit compression), each isometry needs an ancilla initialized to |0>. After the isometry, the two "squeezed" qubits are measured and reset. On Helios with mid-circuit measurement and reset (MCMR), these ancillae can be reused across layers, reducing total qubit count.

**With MCMR reuse:** ancilla count = max ancillae needed simultaneously = N/2 (one per disentangler pair in the widest layer). Total = 2N - 1 + N/2 ancillae, but ancillae are reused, so effective total = 2N - 1 active + ~N/2 ancilla slots.

**Conservative (no reuse):** total = 2N - 1 + N (one ancilla per isometry) = 3N - 1.

**Helios logical qubit budget: 94.**

Solving for N with conservative accounting (3N - 1 <= 94): N <= 31.6, so **N = 30 boundary qubits maximum** without MCMR reuse.

With MCMR reuse (2N - 1 + N/4 <= 94, the N/4 being the widest simultaneous ancilla requirement in the deepest layer): N <= 42.4, so **N = 40 boundary qubits maximum** with full MCMR reuse.

**Recommended operating point: N = 32 boundary qubits.** This is conservative, leaves ~6 logical qubits as measurement ancillae for ZZ correlator readout, and fits within 94 total (63 MERA + 16 max ancillae + 6 measurement = 85, comfortable headroom).

### Error-Correction Mode Trade-off

Two modes available on Helios:

| Mode | Logical qubits | Logical error rate | Recommended for |
|---|---|---|---|
| Error-detection (iceberg) | 94 | ~1e-4 | Deep circuits, force measurements |
| Concatenated EC | 48 | <<1e-4 (beyond break-even) | Precision energy eigenvalue circuits |
| Physical (no EC) | 98 | ~7.9e-4 per gate | NOT recommended — errors accumulate |

For holographic force measurements, the key observable is the energy difference delta_E between two-hologron and one-hologron states. This requires precision ~1e-3 in normalized units (see Section 4). Error-detection mode (94 logical qubits, 1e-4 logical error rate) is preferred because it maximizes available qubits while achieving the required precision. Concatenated EC mode (48 logical qubits) would limit us to N <= 16, matching only our existing simulations.

**Recommendation: error-detection mode, N = 32 boundary qubits.**

---

## 3. Circuit Layouts by Layer Count

All gate counts use the standard decomposition: each 2-qubit unitary U(4) = 3 CNOT + 15 single-qubit gates. Each isometry (3-to-1) = 2 CNOTs + auxiliary single-qubit gates.

### 3-Layer MERA (N=32 boundary qubits)

```
MERA topology:
  Layer 0 (boundary):   32 qubits
  Disentanglers L1:     16 disentanglers x (3 CNOT + ~8 single-qubit) = 48 CNOT, ~128 SQ
  Isometries L1:        16 isometries x (2 CNOT + ~4 single-qubit) = 32 CNOT, ~64 SQ
  Layer 1:              16 qubits remain active

  Disentanglers L2:     8 disentanglers = 24 CNOT, ~64 SQ
  Isometries L2:        8 isometries = 16 CNOT, ~32 SQ
  Layer 2:              8 qubits remain active

  Disentanglers L3:     4 disentanglers = 12 CNOT, ~32 SQ
  Isometries L3:        4 isometries = 8 CNOT, ~16 SQ
  Top tensor:           1 qubit

Total (3 layers, N=32):
  CNOT count:    (48+32) + (24+16) + (12+8) = 140 CNOT
  Depth:         3 layers x ~10 gates/layer = ~30 (parallelized, all-to-all)
  Parameters:    ~140 x 1 (each CNOT contributes ~1 variational angle) + single-qubit params
                 Full unitary per disentangler: 15 params each
                 N=32, L=3: 28 disentanglers x 15 + 14 isometries x 8 = 420 + 112 = 532 params
```

Estimated error budget (error-detection, 1e-4 per logical CNOT):
  1 - (1 - 1e-4)^140 = 1 - 0.9999^140 = 1.39% accumulated error.
  Well within the 10% PoC budget. Excellent for precision measurements.

### 5-Layer MERA (N=32 boundary qubits)

```
  Layer 0:  32 qubits
  Layer 1:  16 qubits  -- 16 disentanglers + 16 isometries = 48+32 = 80 CNOT
  Layer 2:  8 qubits   -- 8+8 = 40 CNOT
  Layer 3:  4 qubits   -- 4+4 = 20 CNOT
  Layer 4:  2 qubits   -- 2+2 = 10 CNOT
  Layer 5:  1 qubit (top tensor)

Total (5 layers, N=32):
  CNOT count:    80 + 40 + 20 + 10 = 150 CNOT (disentanglers + isometries)
  Depth:         ~50 (5 layers x ~10 gates each, parallelized)
  Parameters:    (16+8+4+2) x 15 + (16+8+4+2) x 8 = 450 + 240 = 690 params

Accumulated error (logical):  1 - 0.9999^150 = 1.49%  -- still excellent.
```

### 7-Layer MERA (N=32 boundary qubits, MCMR required)

```
  Layer 0:  32 qubits
  Layer 1:  16  -- 80 CNOT
  Layer 2:  8   -- 40 CNOT
  Layer 3:  4   -- 20 CNOT
  Layer 4:  2   -- 10 CNOT
  Layer 5:  1 (top tensor) -- 7 layers would need 128 boundary qubits
```

Note: 7-layer binary MERA requires 2^7 = 128 boundary qubits for a proper binary tree. With N=32 (2^5), 5 layers is already the natural maximum for a complete binary MERA. A 7-layer MERA on N=32 would require a "cropped" tree where the top layers are degenerate. This is non-standard and not recommended.

**Recommended configuration summary:**

| Config | N (boundary) | Layers | CNOT count | Depth | Error budget | Qubit total |
|---|---|---|---|---|---|---|
| Baseline match | 16 | 3 | 56 | 12 | 0.56% | 31 |
| **Recommended** | **32** | **3** | **140** | **30** | **1.39%** | **85** |
| Extended | 32 | 5 | 150 | 50 | 1.49% | 85 |
| Maximum | 40 | 3 | 175 | 30 | 1.74% | 94 |

The 32q/3-layer configuration doubles our boundary chain length compared to existing simulations (16q/3-layer, SIM-2026-002) while staying well within Helios's error budget.

---

## 4. Ground State Preparation Protocol

### Why VQE Cannot Run on QPU Directly

Our classical VQE required 61,068 circuit evaluations (SIM-2026-002) and 55,000 evaluations (SIM-2026-003). At even 1 shot/evaluation, Quantinuum hardware pricing would make this prohibitive. More critically, each Helios job has a circuit execution overhead; running 60K sequential circuits is not operationally feasible.

**Solution: Offline optimization + parameter transfer.**

### Two-Stage Protocol

**Stage 1 (Classical, already done or extendable):**
1. Optimize MERA parameters using VQE on local simulator or RunPod GPU.
2. For 32q/3-layer (532 params), estimated runtime: ~4x SIM-2026-002 wall time = ~40 hours on RunPod A6000 with GPU-accelerated statevector. Use cached E0 = -40.220 (N=32 OBC, computed via sparse eigsh).
3. Apply Z2 parity projection (SIM-2026-005 method) during optimization to avoid ferromagnetic collapse.
4. Export theta_opt as a numpy array.

**Stage 2 (QPU):**
1. Load theta_opt into the parameterized Helios circuit.
2. Prepare the MERA ground state in a single shot using the optimized parameters.
3. Measure observables (ZZ correlators, hologron forces) with the required shot budget.

**Key constraint:** The transfer fidelity depends on how close theta_opt is to the true ground state. Our best result (SIM-2026-002) achieved 1.87% energy error. On Helios, the 1.39% accumulated CNOT error is of comparable magnitude, so the total error budget is approximately 1.87% (optimization) + 1.39% (hardware noise) = 3.26% combined. This is acceptable for demonstrating the force profile qualitative shape. For quantitative C1/C2 extraction, we need either better optimization (converging to <1%) or error mitigation.

### Error Mitigation Strategies

1. **Probabilistic Error Cancellation (PEC):** Quantinuum supports PEC via the t|ket> compiler. This can virtually eliminate systematic gate errors at the cost of ~2x more shots. Recommended for the precision energy difference measurements.

2. **Zero-Noise Extrapolation (ZNE):** Run the same circuit at 1x, 2x, 3x noise by gate folding, then extrapolate to zero. Compatible with Helios.

3. **Symmetry verification:** After each shot, verify the measured state is in the Z2 parity sector P=+1 (since our ground state has this symmetry). Discard shots where P != +1. This is a free post-selection filter that rejects ~50% of noise-corrupted shots.

---

## 5. Force Measurement Protocol

### Observable Definition

The holographic force at boundary separation dr is:

```
V(dr) = C_two(dr) - C_vac(dr)

where:
  C_vac(dr)  = <GS| Z_i Z_{i+dr} |GS>          (vacuum ZZ correlator)
  C_two(dr)  = <GS_2h| Z_i Z_{i+dr} |GS_2h>    (two-hologron ZZ correlator)
  GS_2h      = Ry(theta_h) at site j, GS prepared by MERA
```

The hologron excitation gate is Ry(pi/3) applied at a single boundary site j (anchor site).
Note: Rz is prohibited -- it commutes with Z-basis measurements and gives V=0 identically.

### Measurement Circuits

For each boundary separation dr in {1, 2, ..., 14} (half the boundary chain for N=32):

**Circuit A (vacuum):**
1. Prepare MERA ground state with theta_opt parameters.
2. Measure Z_i and Z_{i+dr} (standard basis readout).
3. Compute C_vac = <Z_i Z_{i+dr}>.

**Circuit B (two-hologron):**
1. Prepare MERA ground state with theta_opt parameters.
2. Apply Ry(pi/3) at anchor site j.
3. Measure Z_i and Z_{i+dr}.
4. Compute C_two = <Z_i Z_{i+dr}>.

**V(dr) = C_two(dr) - C_vac(dr)** for each dr.

### Shot Budget Estimation

The force signal from SIM-2026-002 (our best result) was:
  V(dr=1) = -0.011, V(dr=2) = -0.007 (in normalized units, ZZ convention).

The Z2-projected result (SIM-2026-005) was:
  V(dr) ~ -0.001 for all dr (suppressed by projection issues).

**Target:** measure V(dr) with precision sigma_V < 0.001 (to resolve the ~0.01 signal from SIM-2026-002 at 10-sigma).

The ZZ correlator C has variance bounded by Var(C) <= 1/n_shots (since each shot gives +/-1).
For sigma_V = sigma_C_two + sigma_C_vac (in quadrature) < 0.001:

  Each sigma_C <= 0.001/sqrt(2) ~ 7e-4
  n_shots per circuit >= 1 / (7e-4)^2 = 2.04e6

**This is large.** However, all 15 pairs (i, i+dr) can be measured simultaneously from a single circuit shot (simultaneous readout of all boundary qubits), so one "shot" gives C(dr) for all dr values at once.

With simultaneous readout:
  n_shots for 10-sigma on V(dr=1) ~ 2e6 / 15 ~ 130,000 shots per circuit (vacuum + two-hologron)
  Total shots: 2 circuits x 130,000 = 260,000 shots.

**With error mitigation (PEC, 2x overhead):** 520,000 shots.

**Realistically**, the signal from SIM-2026-002 is ~0.011 at dr=1 and decays. For a 5-sigma detection of V(dr=1):
  n_shots >= (5 / 0.011)^2 / 15 (simultaneous) ~ 137,000 shots per circuit.

**Practical shot budget recommendation:** 200,000 shots per circuit (vacuum + two-hologron), 400,000 shots total. With PEC mitigation: 800,000 shots. At typical Quantinuum shot rates (~1000 shots/minute), this is approximately 13 hours of hardware time. This exceeds the IBM free tier (10 min/month) by 78x and is the primary cost driver.

### Boundary-Primary Excitations (Recommended Alternative to Pauli Hologrons)

Per Wang & He (PAPER-2026-010), Pauli-X hologrons are dynamically unstable. The stable boundary-primary excitations are constructed as:

```
|psi_primary> = O_boundary |GS>

where O_boundary = sum_{j} f(j) sigma^+_j
and f(j) is the primary operator profile (exponentially localized near the boundary site).
```

On a quantum circuit, this translates to a weighted superposition of single-qubit excitations:

```python
for j in range(N_sites):
    qc.ry(2 * arcsin(f(j)), j)  # amplitude encoding of primary profile
```

This requires a classically precomputed profile f(j) (normalized to 1). The f(j) values for TFIM critical point are derivable from the CFT spectrum. This is more circuit-efficient than brute-force Pauli-X (same gate count, better physics). **Recommended for production measurement.**

---

## 6. Holographic Transport Measurement Protocol

Based on HYP-2026-006 and the composite geodesic result (T_transport = pi/2 * l_AdS), the transport measurement tests whether excitations propagate through the bulk along geodesics.

### Transport Circuit Design

For a 32-site boundary chain with MERA bulk:

**Step 1:** Prepare MERA ground state (theta_opt parameters).

**Step 2:** Apply boundary excitation at site j=0 (left boundary).

**Step 3:** Trotterize time evolution under H_TFIM for T time steps:
  U(dt) = exp(-i H_TFIM dt) decomposed as CNOT + Rz + Rx layers.
  For N=32, each Trotter step adds ~32 CNOTs. Over T ~ 3 * pi/2 * l_AdS ~ 3 * 2.27 ~ 7 time units,
  with dt=0.1 this requires 70 Trotter steps = 2240 additional CNOTs.

**Step 4:** After each time step, measure boundary spin expectation values.

**Step 5:** Identify time T* at which the excitation vanishes from site j=0 and reappears at site j' (the emergent bulk trajectory). Compare T* to pi/2 * l_AdS (composite geodesic prediction).

**Expected result:** T* = pi/2 * l_AdS_MERA = pi/2 * 1.4427 = 2.266 time units (error +0.69% vs measured T=2.25).

**Gate depth warning:** 70 Trotter steps on 32 qubits adds ~2240 CNOTs to the ground state preparation circuit. At 1e-4 error rate, this accumulates 1 - 0.9999^2240 = 20% additional error, exceeding the PoC budget. The transport measurement should use:
  (a) Fewer Trotter steps (dt = 0.25, T = 10 steps = 320 CNOTs, 3.2% additional error), or
  (b) The concatenated EC mode (48 logical qubits, lower error rate), or
  (c) Reduction to 16 boundary qubits (baseline match, 31 total MERA qubits, full qubit budget available for Trotter steps).

**Recommended configuration for transport:** 16q boundary, 3 layers, 56 CNOT (ground state) + 320 CNOT (Trotter, 10 steps, dt=0.25), total 376 CNOT, error budget 3.7%. Feasible.

---

## 7. Comparison: Our Simulations vs Helios

### 16q/3-Layer (SIM-2026-002) on Helios

| Metric | Simulator (SIM-2026-002) | Helios projection |
|---|---|---|
| CNOT count | 29 (our compact decomp) | 56 (full U4 decomp) |
| Error budget | 0% | 0.56% (logical) |
| Shots needed | 1 (statevector exact) | ~140,000 for 5-sigma on V(dr=1) |
| V(dr=1) measured | -0.011 | Expected -0.011 +/- 0.002 |
| xi extracted | 1.233 | Expected 1.233 +/- 0.15 |
| Z2 symmetry | Broken (SIM-2026-002), Fixed (SIM-2026-005) | Enforced by post-selection |
| Ground state prep | VQE classical | Parameter transfer from classical opt |

**Verdict:** 16q/3-layer is straightforwardly feasible on Helios. Error budget (0.56%) is comfortable. The xi measurement would yield the first experimental confirmation of a holographic AdS length scale from a MERA circuit on quantum hardware.

### 24q/5-Layer on Helios

| Metric | RunPod GPU (SIM-2026-006) | Helios projection |
|---|---|---|
| CNOT count | ~38 (compact decomp) | ~150 (full U4) |
| Error budget | 0% | 1.49% (logical) |
| Z2 status | In progress (projection) | Post-selection on P=+1 |
| Feasibility | Completed (pending analysis) | **FEASIBLE** |

**Verdict:** 24q/5-layer is feasible on Helios. The deeper causal cone (5 layers covers dr=1..32) would extend the force profile to larger separations, giving a cleaner exponential fit. This is the priority hardware target.

### 32q/3-Layer (New — Helios-only)

| Metric | Value |
|---|---|
| CNOT count | 140 |
| Error budget | 1.39% |
| Classical optimization time | ~40 hours (RunPod A6000) |
| Force profile range | dr = 1..16 |
| Expected xi improvement | Better statistics at large dr |
| Feasibility | **FEASIBLE — recommended** |

The 32-qubit boundary chain is larger than any previously simulated MERA configuration. On Helios it would be the largest holographic force measurement ever performed on a quantum processor, extending our 16q results to a system where boundary effects are smaller and the bulk geometry is more clearly defined.

---

## 8. Cost and Time Estimates

### Quantinuum Pricing Model

Quantinuum does not publish a standard public pricing sheet. Based on available information:

- **Research access programs:** Quantinuum offers partnership and academic access programs. For groups with published results on Quantinuum hardware (Anand et al. 2023 is a direct precedent), research credits are available.
- **Commercial pricing (estimated):** ~$0.01-$0.03 per circuit shot for H-series hardware. Helios pricing is higher due to logical qubit overhead.
- **Academic/partnership rate (estimated):** ~$0.005 per shot.

**Shot cost estimates:**

| Experiment | Shots | Est. cost (commercial) | Est. cost (academic) |
|---|---|---|---|
| 16q force profile | 280,000 | $2,800-$8,400 | $1,400 |
| 24q force profile | 400,000 | $4,000-$12,000 | $2,000 |
| 32q force profile | 600,000 | $6,000-$18,000 | $3,000 |
| Transport (16q) | 200,000 | $2,000-$6,000 | $1,000 |
| Full program (all four) | 1.48M | $14,800-$44,400 | $7,400 |

**IBM comparison:**

IBM free tier: 10 minutes/month on 127q Eagle r3 or 156q Heron r3.
  - At ~100 circuits/minute on IBM hardware: 1000 circuits/month free.
  - Shot-for-shot, IBM is cheaper for large shot counts but has no logical qubit support at this scale.
  - IBM Heron r3 CX fidelity: 99.8% (physical). Our 140-CNOT circuit on IBM: 1 - 0.998^140 = 24.5% error. The 32q circuit is infeasible on IBM without error correction.

**IBM paid tier (IBM Quantum Premium):** ~$1.60/CU, where 1 CU = 1 second of execution. Estimated: 400K shots x 50ms/shot = 5.6 hours = 20,160 seconds = $32,256. More expensive than Quantinuum for comparable experiments and worse error rates.

**Conclusion:** Helios is the right hardware target for this program. The 1:1 logical ratio is the enabling factor. IBM is not viable without error correction at these CNOT depths.

### Time Estimates

| Phase | Duration | Notes |
|---|---|---|
| Classical optimization (32q/3L) | 40-60 hours | RunPod A6000, Z2-projected L-BFGS-B |
| Circuit compilation for Helios | 2-4 hours | pytket compiler, Helios backend |
| Hardware execution (16q force profile) | 2-3 hours | 280K shots at ~1500 shots/min |
| Hardware execution (32q force profile) | 4-6 hours | 600K shots |
| Transport measurement (16q) | 3-4 hours | Including time evolution steps |
| Analysis and visualization | 4-8 hours | Post-processing correlators |
| **Total (full program)** | **~60 hours machine + ~12 hours human** | Excluding classical pre-optimization |

---

## 9. Implementation Sequence

**Phase 1 (No hardware required):**
1. Extend classical optimization to 32q/3-layer using RunPod (build on SIM-2026-006 infrastructure).
2. Compute E0 for N=32 OBC (cached: E0 = -40.220 approximately, verify with sparse eigsh).
3. Validate theta_opt by re-evaluating energy on local Aer simulator.

**Phase 2 (Helios circuit preparation):**
1. Translate MERA circuit from Qiskit to pytket (Quantinuum's native compiler).
2. Compile to Helios native gate set (ZZPhase, U1q, Measure, Reset).
3. Add mid-circuit measurement + reset for isometry ancilla reuse.
4. Add force measurement circuits (vacuum + hologron variants, all dr values).
5. Add Z2 post-selection filter (measure parity after each shot).

**Phase 3 (Hardware submission — requires explicit user approval):**
1. Submit 16q/3-layer first (lowest cost, baseline validation).
2. Analyze results, compare to SIM-2026-002 statevector results.
3. If agreement within 5% on V(dr) shape: submit 32q/3-layer.
4. After force profile confirmed: submit transport measurement.

**Go/no-go criteria after Phase 3 step 1:**
- If V(dr=1) measured within 20% of -0.011: proceed to 32q.
- If V(dr) is flat (as in SIM-2026-005): indicates persistent Z2 or optimization failure -- debug before 32q.
- If energy error > 5%: classical optimization needs improvement before re-submission.

---

## 10. Key Risks and Mitigations

| Risk | Severity | Mitigation |
|---|---|---|
| Classical optimization doesn't converge for 32q | High | Start with 16q (already solved). Scale up incrementally. |
| Ferromagnetic collapse (Z2 trap) at 32q | High | Z2 post-selection on hardware + penalty term in classical opt. |
| Shot count underestimates (force signal weaker than 16q) | Medium | Pilot with 16q first; calibrate shot budget from measured signal. |
| Quantinuum pricing higher than estimated | Medium | Apply for academic/research partnership before purchasing shots. |
| MERA parameter transfer degrades at 32q | Medium | Validate transfer fidelity on Aer simulator with noise model. |
| Hologron instability (Wang & He) suppresses signal | Medium | Switch to boundary-primary excitations if Pauli-X hologrons give flat V(dr). |
| Transport measurement requires too many Trotter steps | Low | Use dt=0.25 (10 steps) as compromise between resolution and circuit depth. |

---

## 11. Connection to Published Results

The Anand et al. (PAPER-2026-017, PRX Quantum 2023) experiment used 10 qubits on Quantinuum H2 to demonstrate log-law entanglement scaling in a MERA for an L=32 Ising chain. Our program extends this in two directions:

1. **Larger boundary chain:** 32q vs 10q -- enables better bulk geometry resolution.
2. **New observable:** holographic forces (hologron interaction potential V(dr)) -- not measured in Anand et al.
3. **Hardware generation:** Helios vs H2 -- 94 logical qubits vs 12, iceberg vs heavy-hex code.

The existing literature proof-of-concept validates our approach. The Helios experiment would be the first measurement of holographic forces on quantum hardware.

---

## 12. Files and Reproducibility

| File | Description |
|---|---|
| `research/data/hardware/HW-2026-009.json` | Helios hardware specification |
| `research/data/simulations/SIM-2026-002.json` | Best 16q/3L VQE result (theta_opt source) |
| `research/data/simulations/theta_opt_SIM2026002.npy` | Optimized parameters for 16q/3L |
| `research/data/simulations/composite_geodesic_results.json` | T_transport = pi/2 * l_AdS (HYP-2026-006) |
| `research/data/hardware/helios-mera-design.md` | This document |

Circuit translation to pytket will be implemented in:
  `research/data/simulations/helios_circuit_16q.py` (Phase 2, not yet written)
  `research/data/simulations/helios_circuit_32q.py` (Phase 2, not yet written)

---

## Summary Table

| Question | Answer |
|---|---|
| Max boundary qubits on Helios | 40 (MCMR reuse), 32 (conservative) |
| Recommended configuration | 32q boundary, 3 layers, error-detection mode |
| CNOT count (32q/3L) | 140 logical |
| Error budget (32q/3L) | 1.39% accumulated |
| Ground state prep method | Classical VQE -> parameter transfer |
| Shots for 5-sigma force detection | ~140,000 per circuit, 280,000 total (16q) |
| Hardware submission approved? | NO -- requires explicit user approval |
| Recommended first experiment | 16q/3-layer (baseline validation, lowest cost) |
| Key publication target | First holographic force measurement on quantum hardware |
| Transport measurement feasibility | FEASIBLE (16q, 10 Trotter steps, dt=0.25) |
| T_transport prediction | 2.266 time units (composite geodesic, 0.69% error vs measured) |
| IBM viability | NOT VIABLE (24.5% error at 140 CNOT depth, no logical qubits) |
| Quantinuum advantage | 94 logical qubits, 1e-4 logical error rate, all-to-all connectivity |
