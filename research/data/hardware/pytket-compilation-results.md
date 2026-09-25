# pytket Compilation Results -- MERA Circuits for Quantinuum Helios

**Date:** 2026-03-18
**Tool:** pytket 2.15.0, pytket-quantinuum 0.58.0
**Target:** Quantinuum Helios native gate set (ZZPhase, Rz, PhasedX)
**Script:** `research/data/hardware/pytket_compile_mera.py`

---

## Key Finding

Our MERA circuit is already near-optimal for 2-qubit gate count. The compact 1-CX-per-block decomposition (Ry+Rz+CX+Ry per disentangler/isometry) leaves no room for pytket to eliminate 2Q gates -- each CX maps 1:1 to a native ZZPhase(0.5).

The real win is **depth reduction** (40% improvement) and the **2.5x savings versus the design doc's conservative estimate** of 140 CX (which assumed full U(4) decomposition at 3 CX per block).

---

## Circuit Inventory

### Design Doc Estimate vs Actual

The Helios design doc (`helios-mera-design.md`) assumed a full U(4) decomposition:
- Each disentangler: 3 CNOT + 15 single-qubit gates
- Each isometry: 2 CNOT + ~4 single-qubit gates

Our actual VQE circuit uses a compact decomposition:
- Each disentangler: **1 CX** + 6 rotation gates (Ry, Rz)
- Each isometry: **1 CX** + 4 rotation gates (Ry, Rz)

| | Disentanglers | Isometries | Top cap | CX total |
|---|---|---|---|---|
| 32q/3L design doc (full U4) | 28 x 3 = 84 | 28 x 2 = 56 | -- | **140** |
| 32q/3L actual (compact) | 28 x 1 = 28 | 28 x 1 = 28 | 1 | **57** |

---

## pytket Compilation Results

### 32q/3-layer (Helios target)

| Stage | 2Q gates | Depth | 1Q gates | Notes |
|---|---|---|---|---|
| Qiskit original | 57 CX | 25 | 286 (Ry+Rz) | Our compact decomposition |
| pytket CX-optimized | 57 CX | **15** | 146 (TK1) | 40% depth reduction |
| pytket TK2 intermediate | 29 TK2 | 9 | 90 (TK1) | Merges disentangler+isometry pairs |
| pytket ZZPhase native | **57 ZZPhase** | **15** | 146 (TK1) | 1:1 CX-to-ZZPhase mapping |

**Why no 2Q gate savings:** pytket's TK2 peephole pass merges adjacent CX gates on the same qubit pair into a single TK2 gate (57 CX -> 29 TK2). However, each merged TK2 contains 2 non-zero interaction angles and decomposes back to 2 ZZPhase gates. The net 2Q count is unchanged: each CX = one ZZPhase(0.5) on Quantinuum hardware.

**Depth savings are significant:** pytket parallelizes independent 2Q gates across the wide MERA layers, reducing circuit depth from 25 to 15 (40% improvement). This matters for decoherence.

### All Configurations

| Config | CX (orig) | ZZPhase (opt) | Depth (orig) | Depth (opt) | Error (orig) | Error (opt) |
|---|---|---|---|---|---|---|
| 16q/3-layer | 29 | 29 | 25 | 15 | 0.290% | 0.290% |
| 24q/5-layer | 46 | 46 | 35 | 21 | 0.459% | 0.459% |
| **32q/3-layer** | **57** | **57** | **25** | **15** | **0.568%** | **0.568%** |

Error budget: Helios logical 2Q gate error rate = 1e-4 (iceberg error-detection mode).

---

## HQC Cost Analysis

**Formula:** `HQC = n_shots * (5 + n_2q_gates / 10)`

### 32q/3-layer Helios Target

| Scenario | n_2q | n_shots | HQC |
|---|---|---|---|
| Design doc estimate (140 CX) | 140 | 10,000 | 190,000 |
| Full U(4) KAK-optimized (87 CX) | 87 | 10,000 | 137,000 |
| **Our compact circuit (57 ZZPhase)** | **57** | **10,000** | **107,000** |
| Design doc estimate (140 CX) | 140 | 280,000 | 5,320,000 |
| Full U(4) KAK-optimized (87 CX) | 87 | 280,000 | 3,836,000 |
| **Our compact circuit (57 ZZPhase)** | **57** | **280,000** | **2,996,000** |

### Savings vs Design Doc

| Shot count | HQC (140 CX) | HQC (57 ZZPhase) | Saved | % |
|---|---|---|---|---|
| 10,000 (minimal) | 190,000 | 107,000 | 83,000 | 43.7% |
| 280,000 (5-sigma force) | 5,320,000 | 2,996,000 | 2,324,000 | 43.7% |

### All Configurations at 280,000 Shots

| Config | HQC (original) | Notes |
|---|---|---|
| 16q/3-layer | 2,212,000 | Baseline validation |
| 24q/5-layer | 2,688,000 | Current sim parameters |
| **32q/3-layer** | **2,996,000** | **Helios target** |

---

## Error Budget Comparison

| Config | 2Q gates | Error (Helios 1e-4) | Design doc estimate |
|---|---|---|---|
| 16q/3-layer | 29 | 0.29% | 0.56% (56 CX assumed) |
| 24q/5-layer | 46 | 0.46% | ~1.5% (150 CX assumed) |
| 32q/3-layer | 57 | 0.57% | 1.39% (140 CX assumed) |

Our compact decomposition cuts the error budget roughly in half compared to the design doc estimates.

---

## What pytket Does and Does Not Help With

### Does Help
1. **Depth reduction (40%):** parallelizes independent gates, reducing decoherence exposure
2. **1Q gate squashing:** merges adjacent rotations (286 -> 146 gates via TK1 fusion)
3. **Native gate compilation:** converts to Quantinuum's ZZPhase + Rz + PhasedX gate set
4. **Validation:** confirms our circuit is already near the theoretical minimum for 2Q gates

### Does Not Help
1. **2Q gate count reduction:** our compact decomposition already uses 1 CX per block -- there is no redundancy for pytket to exploit
2. **Further CX elimination beyond 1:1 CX-to-ZZPhase:** this is a fundamental limit of our ansatz structure, not a compiler limitation

### Why Our Circuit Is Already Optimal

Each MERA block (disentangler or isometry) contains exactly one CX gate. This CX creates the entanglement between the two qubits in the block. It cannot be removed without destroying the block's function. The only compilation opportunity would arise if:

1. **Adjacent blocks on the same qubit pair had redundant CX gates** -- pytket does detect this (the TK2 merging) but the merged result still requires 2 ZZPhase gates to implement the full 2-qubit interaction.

2. **The circuit had SWAP gates or routing overhead** -- our all-to-all connectivity on Helios means no SWAPs are needed.

3. **We used a richer gate decomposition (full U(4) = 3 CX)** -- then pytket would help significantly. But we already use the compact form.

---

## Comparison: Full U(4) vs Compact Decomposition

If we had used the full U(4) decomposition (as the design doc assumed):

| Decomposition | CX count (32q/3L) | ZZPhase after pytket | Depth | Error budget |
|---|---|---|---|---|
| Full U(4), 3 CX/disentangler | 87 (after Qiskit KAK opt) | 87 | 33 | 0.866% |
| **Compact, 1 CX/block** | **57** | **57** | **15** | **0.568%** |

The compact decomposition is 34% more efficient than even KAK-optimized full U(4). This is because our parameterization restricts each block to a 1-parameter entangling subspace rather than the full U(4) manifold.

Note: the design doc's "140 CX" figure was based on the textbook 3-CX decomposition of U(4) without Qiskit KAK optimization. With KAK, it would be 87 CX. Our compact form achieves 57.

---

## Recommendations

1. **Use pytket for Helios submission:** even without 2Q savings, the 40% depth reduction and proper native gate compilation are essential for hardware execution.

2. **No need to rearchitect the ansatz:** our compact decomposition is already near-optimal. Switching to a richer parameterization (full U(4)) would increase expressibility but at the cost of more 2Q gates and higher error.

3. **The design doc's cost estimates should be revised downward:** 57 ZZPhase instead of 140 CX means ~44% lower HQC cost than originally projected.

4. **Circuit depth 15 on Helios** is excellent -- well within coherence limits for trapped-ion hardware where T2 >> circuit execution time.

---

## Files

| File | Description |
|---|---|
| `research/data/hardware/pytket_compile_mera.py` | Compilation script |
| `research/data/hardware/pytket_compilation_results.json` | Machine-readable results |
| `research/data/hardware/pytket-compilation-results.md` | This document |
| `research/data/hardware/helios-mera-design.md` | Original design doc (140 CX estimate) |
