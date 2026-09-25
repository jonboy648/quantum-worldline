# FT-MERA Cost Estimate Refresh — chi=3 16q Transport Circuit

**Date:** 2026-06-08 (written 2026-06-11)
**Hypothesis:** HYP-2026-016 (FT neutral-atom side)
**Supersedes:** SIM-2026-021 atom/runtime estimate (1839 atoms / 8.1 min, 115:1 teleportation overhead)
**Refreshes against:** 2026 qLDPC frontier (HW-2026-044/045/055/056, HW-2026-061/062/063)

This refresh was flagged ACTIONABLE in three consecutive scans. The driver: the original
estimate used the Khan et al. (PAPER-2026-049) **surface-code-era teleportation overhead of
115 physical atoms per logical qubit**. Two 2026 demonstrations now show qLDPC encoding at
~4.5-4.7 phys/logical on real hardware — a ~25x improvement in encoding rate that was never
folded into HYP-016.

---

## 1. Headline numbers

| Quantity | OLD (SIM-021) | NEW LOW (bare) | NEW HIGH (20x) |
|---|---|---|---|
| Encoding overhead | 115:1 (teleport) | 4.7:1 (qLDPC) | 4.7:1 + factories |
| Physical atoms (16 logical) | 1839 | **~75** | **~1500** |
| Wall-time (10k shots, 5σ fit) | 8.1 min | **~15 min** | **~95 min (1.6 h)** |

The NEW LOW atom count (~75) is **~25x below** the old estimate. Even the NEW HIGH (~1500)
sits below the old 1839 — because the old estimate was *itself* a bare-linear number with the
wrong (surface-code-era) encoding ratio, while the new HIGH already includes a 20x overhead
multiplier on top of a far better ratio.

---

## 2. Atom-count derivation

**Encoding ratios actually DEMONSTRATED in 2026 (hardware, not simulation):**

| Source | Ratio | Status |
|---|---|---|
| QuEra Nature 649 — [[16,6,4]] qLDPC, 448 phys / 96 logical (HW-044) | **4.67:1** | demonstrated |
| IonQ trapped-ion qLDPC breakeven, 18 phys / 4 logical (HW-055) | **4.50:1** | demonstrated |
| QuEra co-design simulation, 2304 / 1156 (HW-045) | 1.99:1 | **simulation only — not used as a bound** |

The two demonstrated ratios converge tightly (4.5-4.7:1), independently across the two
substrate families (neutral atom and trapped ion). The ~2:1 simulated co-design number is
deliberately **excluded** from the bound because it has never been run on hardware; it is
noted only as the optimistic horizon.

- **LOW = 16 × 4.67 ≈ 75 atoms** — bare data-qubit encoding at the QuEra Nature 649 rate.
  Leans on **HW-2026-044**. Assumes the chi=3 isometry decomposition maps onto the logical
  layer with no extra logical qubits (carried-forward caveat: this mapping has never been done).
- **HIGH = 75 × 20 ≈ 1500 atoms** — applies the original SIM-021 20x worst-case multiplier
  to cover: (a) magic-state distillation factory for the non-Clifford content of the U(2^4)
  top-tensor decomposition, (b) atom-routing/AOD-shuttle buffer region, (c) syndrome ancillas
  for repeated QEC cycles (HW-056 Atom Computing demonstrated 90 syndrome rounds with
  reloading, confirming the ancilla machinery is real but not free). Leans on **HW-2026-056**.

**Caveats carried forward verbatim from SIM-021 (still unaddressed):**
1. No architectural mapping for the chi=3 isometry decomposition onto a logical qLDPC patch.
2. No magic-state distillation overhead computed for the specific top-tensor non-Clifford gates.
3. No atom-routing time / AOD scheduling included in the geometry.

---

## 3. Wall-time derivation

Logical 2Q count, scaled honestly from the **measured** compiled chi=3 **8q** circuit
(451 ZZPhase, `pytket_compile_chi3_8q_results.json`):

- **Scaling assumption:** 8q→16q adds one MERA boundary-halving layer (boundary width doubles)
  plus a wider top-tensor decomposition. Logical 2Q count scales **2.0x (low) to 2.5x (high)**:
  451 → **902-1128 ZZPhase** at the logical level.
- Per-logical-2Q time on early-FT neutral atoms: **2 ms (low) to 5 ms (high)**, covering
  transversal CNOT + a syndrome-extraction cycle + AOD move. Anchored to HW-056's
  demonstrated repeated-cycle cadence.
- Parallelism: 20 parallel 2Q pairs (HW-062 Gemini spec) for LOW; degraded to ~10 for HIGH
  to account for routing-bound qLDPC scheduling.
- Shots: 10,000 for a 5σ alpha fit over dr=1..6 (SIM-021 lineage).

→ **LOW ≈ 15 min, HIGH ≈ 95 min (1.6 h).** Old 8.1 min was bare-linear with *no shot budget
and no routing* — it was optimistic on time even though pessimistic on atoms.

---

## 4. Quantinuum Sol question — does the 10k-gate budget cover chi=3 16q WITHOUT error correction?

**Answer: YES, comfortably — and this is the most consequential finding of the refresh.**

Sol (HW-061, roadmap 2027): 192 physical qubits, **99.98% 2Q fidelity**, **10,000 gate
operations per circuit**, 2x faster than Helios.

Scaling the measured compiled 8q circuit (451 ZZPhase + 771 PhasedX + 753 Rz = 1975 total
ops, or 1222 excluding virtual Rz) by the same 2.0-2.5x:

| Metric | 16q @ 2.0x | 16q @ 2.5x | Sol budget |
|---|---|---|---|
| Total ops (incl. Rz) | ~3950 | ~4940 | **10,000** |
| Total ops (excl. virtual Rz) | ~2440 | ~3060 | 10,000 |
| ZZPhase (2Q) | 902 | 1128 | — |
| **Circuit fidelity @ 99.98%** | **83.5%** | **79.8%** | — |

Two independent gates pass:
1. **Gate-count gate:** ~4-5k total ops vs a 10k budget — fits with ~2x headroom even on the
   conservative (incl-Rz) accounting.
2. **Fidelity gate:** ~80-84% surviving circuit fidelity from the 2Q layer alone, which clears
   the SIM-021 fidelity-sweep requirement (99.99%/gate was needed to reach dr=4 on the
   noise-floor analysis; Sol's 99.98% is one notch below that 99.99% target, so the
   **power-law fit at dr≥4 is borderline**, but **dr=1..2 force existence is solidly in range**).

**Implication:** Sol (2027) could run the chi=3 16q transport circuit **bare-metal, no error
correction required** — making the entire FT-encoding question moot for the 16q transport
target specifically. The FT atom-count estimate above remains relevant only for the
*definitive noise-free* run (full dr=1..6 alpha fit to high precision) or for scaling beyond
16q. This directly updates the HYP-016 resource hierarchy: a NISQ-class but high-fidelity
gate machine (Sol) now sits *between* Helios-now and FT-neutral-atom-future, and likely
subsumes the 16q goal.

Caveat: Sol is a **roadmap target, not a demonstrated spec** (HW-061). The 99.98% and 10k-gate
numbers are unproven. Treat the Sol answer as "passes on the published roadmap spec."

---

## 5. Single biggest remaining unknown

**The chi=3 isometry decomposition has never been mapped to a logical qLDPC patch.** Every
atom-count number here applies the demonstrated *encoding rate* to the *logical-qubit count*,
but assumes the MERA isometries (especially the U(2^4) top tensor's non-Clifford content)
compile onto the logical layer without inflating the logical qubit count or demanding a large
magic-state factory. The factor between LOW and HIGH (20x) is almost entirely the uncertainty
in this one mapping. Resolving it requires an actual transversal/lattice-surgery compilation
of the chi=3 circuit onto a specific qLDPC code — the same step SIM-021 deferred and that
remains undone.

---

## Provenance

- Encoding rates: HW-2026-044 (QuEra Nature 649, demonstrated 4.67:1), HW-2026-055 (IonQ qLDPC
  breakeven, demonstrated 4.5:1), HW-2026-045 (QuEra co-design, simulation 1.99:1, excluded).
- Syndrome/cycle cadence: HW-2026-056 (Atom Computing, 90 rounds + reloading),
  HW-2026-063 (USTC, sustained 99.81% across rounds), HW-2026-057 (Yb readout 99.89%).
- Sol spec: HW-2026-061. Gemini parallelism: HW-2026-062.
- Logical 2Q baseline: pytket_compile_chi3_8q_results.json (451 ZZPhase, measured).
- Method lineage: SIM-2026-021, PAPER-2026-049 (Khan et al., 115:1 teleportation overhead).
