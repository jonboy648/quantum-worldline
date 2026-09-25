"""
Pytket compilation of MERA circuits for Quantinuum Helios.

Builds MERA circuits in Qiskit using our standard decomposition,
converts to pytket, applies full peephole optimization targeting
Quantinuum's native ZZPhase gate, and reports gate count / depth
improvements and HQC cost estimates.

Key insight: pytket's FullPeepholeOptimise with TK2 target identifies
2-qubit gate reductions. DecomposeTK2 with ZZPhase_fidelity then
converts each TK2 into the minimum number of ZZPhase gates (0, 1, 2,
or 3 depending on the interaction content).

Author: hardware-tracker (via Claude Code)
Date: 2026-03-18
"""

import sys
import json
import time
from math import pi
import numpy as np

# ── Qiskit circuit construction (matches our VQE code exactly) ───────────────

from qiskit import QuantumCircuit

def add_disentangler(qc, q0, q1, p, o):
    """Standard disentangler: Ry,Rz on each qubit -> CX -> Ry on each."""
    qc.ry(p[o],   q0); qc.rz(p[o+1], q0)
    qc.ry(p[o+2], q1); qc.rz(p[o+3], q1)
    qc.cx(q0, q1)
    qc.ry(p[o+4], q0); qc.ry(p[o+5], q1)
    return o + 6

def add_isometry(qc, q0, q1, p, o):
    """Standard isometry: Ry on each -> CX -> Ry,Rz."""
    qc.ry(p[o],   q0); qc.ry(p[o+1], q1)
    qc.cx(q0, q1)
    qc.ry(p[o+2], q0); qc.rz(p[o+3], q1)
    return o + 4

def count_params(n, n_layers):
    total = 0
    active = n
    for l in range(n_layers):
        np2 = active // 2
        if np2 == 0:
            break
        total += np2 * 6 + np2 * 4
        active = np2 + (active % 2)
    if active >= 2:
        total += 6
    return total

def build_mera_circuit(n_qubits, n_layers):
    """Build binary MERA circuit with random concrete angles."""
    NP = count_params(n_qubits, n_layers)
    rng = np.random.default_rng(42)
    pv = rng.uniform(-pi, pi, NP)

    qc = QuantumCircuit(n_qubits)
    o = 0
    aq = list(range(n_qubits))

    for l in range(n_layers):
        na = len(aq)
        if na < 2:
            break
        for k in range(0, na - 1, 2):
            o = add_disentangler(qc, aq[k], aq[k+1], pv, o)
        naq = []
        for k in range(0, na - 1, 2):
            o = add_isometry(qc, aq[k], aq[k+1], pv, o)
            naq.append(aq[k])
        if na % 2:
            naq.append(aq[-1])
        aq = naq

    if len(aq) >= 2 and o + 6 <= NP:
        o = add_disentangler(qc, aq[0], aq[1], pv, o)

    return qc, NP


def count_gates(circ):
    """Count gates by type in a pytket circuit."""
    counts = {}
    for cmd in circ.get_commands():
        op_name = cmd.op.type.name
        counts[op_name] = counts.get(op_name, 0) + 1
    return counts


def count_2q(counts):
    """Sum all 2-qubit gates in a gate count dict."""
    TWO_Q_GATES = {'CX', 'TK2', 'ZZPhase', 'XXPhase', 'YYPhase', 'ZZMax', 'SWAP'}
    return sum(v for k, v in counts.items() if k in TWO_Q_GATES)


# ── Imports ──────────────────────────────────────────────────────────────────

from pytket.extensions.qiskit import qiskit_to_tk
from pytket._tket.circuit import OpType
from pytket.passes import (
    FullPeepholeOptimise,
    RemoveRedundancies,
    SquashTK1,
    DecomposeTK2,
    NormaliseTK2,
    AutoRebase,
)

# ── Main ─────────────────────────────────────────────────────────────────────

print("=" * 70)
print("MERA Circuit Compilation for Quantinuum Helios via pytket")
print("=" * 70)

configs = [
    (16, 3, "16q/3-layer (baseline)"),
    (24, 5, "24q/5-layer (current sim)"),
    (32, 3, "32q/3-layer (Helios target)"),
]

results = {}

for n_qubits, n_layers, label in configs:
    print(f"\n{'='*70}")
    print(f"  {label}")
    print(f"{'='*70}")

    qc, n_params = build_mera_circuit(n_qubits, n_layers)

    # ── Qiskit original stats ────────────────────────────────────────────
    ops_orig = qc.count_ops()
    cx_orig = ops_orig.get('cx', 0)
    depth_orig = qc.depth()
    ry_orig = ops_orig.get('ry', 0)
    rz_orig = ops_orig.get('rz', 0)
    sq_orig = ry_orig + rz_orig

    print(f"\n  [1] Qiskit original circuit:")
    print(f"    CX gates:      {cx_orig}")
    print(f"    1Q gates:      {sq_orig}  (Ry: {ry_orig}, Rz: {rz_orig})")
    print(f"    Total gates:   {cx_orig + sq_orig}")
    print(f"    Depth:         {depth_orig}")
    print(f"    Parameters:    {n_params}")

    # ── Convert to pytket ────────────────────────────────────────────────
    tk_circ = qiskit_to_tk(qc)

    # ── Pass 1: FullPeepholeOptimise targeting CX ────────────────────────
    tk_cx = tk_circ.copy()
    t0 = time.time()
    FullPeepholeOptimise().apply(tk_cx)
    t_cx = time.time() - t0

    cx_counts = count_gates(tk_cx)
    cx_2q = count_2q(cx_counts)
    cx_depth = tk_cx.depth()

    print(f"\n  [2] pytket FullPeepholeOptimise (CX target):")
    print(f"    CX gates:      {cx_2q}  (was {cx_orig})")
    print(f"    Depth:         {cx_depth}  (was {depth_orig})")
    print(f"    All gates:     {cx_counts}")
    print(f"    Time:          {t_cx:.3f}s")

    # ── Pass 2: FullPeepholeOptimise targeting TK2 ───────────────────────
    # TK2 is pytket's universal 2-qubit gate. The peephole pass merges
    # adjacent 2Q interactions into single TK2 gates, reducing count.
    tk_tk2 = tk_circ.copy()
    t0 = time.time()
    FullPeepholeOptimise(target_2qb_gate=OpType.TK2).apply(tk_tk2)
    t_tk2 = time.time() - t0

    tk2_counts = count_gates(tk_tk2)
    tk2_2q = count_2q(tk2_counts)
    tk2_depth = tk_tk2.depth()

    print(f"\n  [3] pytket FullPeepholeOptimise (TK2 target):")
    print(f"    TK2 gates:     {tk2_2q}  (was {cx_orig} CX, saved {cx_orig - tk2_2q})")
    print(f"    Depth:         {tk2_depth}")
    print(f"    All gates:     {tk2_counts}")
    print(f"    Time:          {t_tk2:.3f}s")

    # ── Pass 3: TK2 -> ZZPhase (noise-aware Quantinuum decomposition) ────
    # DecomposeTK2 with ZZPhase_fidelity=1.0 decomposes each TK2 into the
    # MINIMUM number of ZZPhase gates (0, 1, 2, or 3) needed.
    # This is the key: a TK2(a,b,c) where b=c=0 needs only 1 ZZPhase,
    # not the 3 you'd get from naive CX decomposition.
    tk_native = tk_tk2.copy()
    t0 = time.time()

    # Normalize TK2 parameters first (required by DecomposeTK2)
    NormaliseTK2().apply(tk_native)

    # Decompose TK2 -> minimal ZZPhase gates
    DecomposeTK2(ZZPhase_fidelity=1.0).apply(tk_native)

    # Rebase remaining 1Q gates to Quantinuum native set
    AutoRebase({OpType.Rz, OpType.PhasedX, OpType.ZZPhase}).apply(tk_native)

    # Clean up redundancies
    RemoveRedundancies().apply(tk_native)
    SquashTK1().apply(tk_native)
    RemoveRedundancies().apply(tk_native)

    t_native = time.time() - t0

    native_counts = count_gates(tk_native)
    native_2q = count_2q(native_counts)
    native_zzphase = native_counts.get('ZZPhase', 0)
    native_phasedx = native_counts.get('PhasedX', 0)
    native_rz = native_counts.get('Rz', 0)
    native_tk1 = native_counts.get('TK1', 0)
    native_1q = native_phasedx + native_rz + native_tk1
    native_depth = tk_native.depth()

    print(f"\n  [4] Quantinuum native (ZZPhase + Rz + PhasedX):")
    print(f"    ZZPhase gates: {native_zzphase}  (was {cx_orig} CX, saved {cx_orig - native_zzphase})")
    print(f"    PhasedX gates: {native_phasedx}")
    print(f"    Rz gates:      {native_rz}")
    print(f"    TK1 gates:     {native_tk1}")
    print(f"    Total 2Q:      {native_2q}")
    print(f"    Total 1Q:      {native_1q}")
    print(f"    Depth:         {native_depth}  (was {depth_orig})")
    print(f"    All gates:     {native_counts}")
    print(f"    Time:          {t_native:.3f}s")

    # ── Pass 4: Also try CX-first optimization -> ZZPhase decomp ────────
    # Compare: optimize for CX first, then convert each CX to 1 ZZPhase
    tk_cx_to_zz = tk_cx.copy()
    t0 = time.time()
    AutoRebase({OpType.Rz, OpType.PhasedX, OpType.ZZPhase}).apply(tk_cx_to_zz)
    RemoveRedundancies().apply(tk_cx_to_zz)
    t_cx_zz = time.time() - t0

    cx_zz_counts = count_gates(tk_cx_to_zz)
    cx_zz_2q = count_2q(cx_zz_counts)

    print(f"\n  [5] Alternative: CX-optimized -> rebase to ZZPhase:")
    print(f"    ZZPhase gates: {cx_zz_counts.get('ZZPhase', 0)}  (1:1 from {cx_2q} CX)")
    print(f"    Total 2Q:      {cx_zz_2q}")
    print(f"    All gates:     {cx_zz_counts}")

    # ── Pick best result ─────────────────────────────────────────────────
    best_2q = min(native_2q, cx_zz_2q)
    best_method = "TK2->ZZPhase" if native_2q <= cx_zz_2q else "CX->ZZPhase"
    best_depth = native_depth if native_2q <= cx_zz_2q else tk_cx_to_zz.depth()

    if native_2q <= cx_zz_2q:
        best_counts = native_counts
    else:
        best_counts = cx_zz_counts

    savings_2q = cx_orig - best_2q
    savings_pct = (savings_2q / cx_orig * 100) if cx_orig > 0 else 0

    print(f"\n  BEST: {best_method} -> {best_2q} 2Q gates (was {cx_orig}, saved {savings_2q} = {savings_pct:.1f}%)")

    # ── HQC cost ─────────────────────────────────────────────────────────
    n_shots_10k = 10000
    n_shots_280k = 280000

    hqc_orig_10k = n_shots_10k * (5 + cx_orig / 10)
    hqc_opt_10k = n_shots_10k * (5 + best_2q / 10)
    hqc_orig_280k = n_shots_280k * (5 + cx_orig / 10)
    hqc_opt_280k = n_shots_280k * (5 + best_2q / 10)

    hqc_savings_10k_pct = (1 - hqc_opt_10k / hqc_orig_10k) * 100 if hqc_orig_10k > 0 else 0

    print(f"\n  HQC Cost (formula: n_shots * (5 + n_2q_gates / 10)):")
    print(f"    10,000 shots:  {hqc_orig_10k:>12,.0f} -> {hqc_opt_10k:>12,.0f}  (saved {hqc_orig_10k - hqc_opt_10k:,.0f} = {hqc_savings_10k_pct:.1f}%)")
    print(f"    280,000 shots: {hqc_orig_280k:>12,.0f} -> {hqc_opt_280k:>12,.0f}  (saved {hqc_orig_280k - hqc_opt_280k:,.0f})")

    # ── Error budget ─────────────────────────────────────────────────────
    err_rate = 1e-4  # Helios logical 2Q gate error
    err_orig = 1 - (1 - err_rate) ** cx_orig
    err_opt = 1 - (1 - err_rate) ** best_2q

    print(f"\n  Error Budget (Helios, 1e-4 per logical 2Q gate):")
    print(f"    Original:  {err_orig*100:.4f}%  ({cx_orig} gates)")
    print(f"    Optimized: {err_opt*100:.4f}%  ({best_2q} gates)")
    print(f"    Improvement: {(err_orig - err_opt)*100:.4f}%")

    # ── Store ────────────────────────────────────────────────────────────
    results[label] = {
        "n_qubits": n_qubits,
        "n_layers": n_layers,
        "n_params": n_params,
        "original": {
            "cx_count": cx_orig,
            "ry_count": ry_orig,
            "rz_count": rz_orig,
            "sq_count": sq_orig,
            "depth": depth_orig,
        },
        "optimized_cx_target": {
            "cx_count": cx_2q,
            "depth": cx_depth,
        },
        "optimized_tk2_target": {
            "tk2_count": tk2_2q,
            "depth": tk2_depth,
        },
        "native_quantinuum": {
            "zzphase_count": native_zzphase,
            "phasedx_count": native_phasedx,
            "rz_count": native_rz,
            "tk1_count": native_tk1,
            "total_2q": native_2q,
            "total_1q": native_1q,
            "depth": native_depth,
        },
        "cx_to_zzphase": {
            "zzphase_count": cx_zz_counts.get('ZZPhase', 0),
            "total_2q": cx_zz_2q,
        },
        "best": {
            "method": best_method,
            "two_q_count": best_2q,
            "depth": best_depth,
            "savings_count": savings_2q,
            "savings_pct": savings_pct,
        },
        "hqc": {
            "original_10k": hqc_orig_10k,
            "optimized_10k": hqc_opt_10k,
            "savings_10k": hqc_orig_10k - hqc_opt_10k,
            "savings_10k_pct": hqc_savings_10k_pct,
            "original_280k": hqc_orig_280k,
            "optimized_280k": hqc_opt_280k,
            "savings_280k": hqc_orig_280k - hqc_opt_280k,
        },
        "error_budget": {
            "original_pct": err_orig * 100,
            "optimized_pct": err_opt * 100,
            "improvement_pct": (err_orig - err_opt) * 100,
        },
    }


# ── Summary ──────────────────────────────────────────────────────────────────

print(f"\n\n{'='*70}")
print("SUMMARY TABLE")
print(f"{'='*70}")
hdr = f"{'Config':<28} {'CX':>5} {'Opt2Q':>6} {'Saved':>6} {'D_in':>5} {'D_out':>6} {'Err_in':>7} {'Err_out':>8}"
print(hdr)
print("-" * len(hdr))
for label, r in results.items():
    cx = r['original']['cx_count']
    o2q = r['best']['two_q_count']
    sav = f"{r['best']['savings_pct']:.1f}%"
    din = r['original']['depth']
    dout = r['best']['depth']
    ein = f"{r['error_budget']['original_pct']:.3f}%"
    eout = f"{r['error_budget']['optimized_pct']:.3f}%"
    print(f"{label:<28} {cx:>5} {o2q:>6} {sav:>6} {din:>5} {dout:>6} {ein:>7} {eout:>8}")

print(f"\n{'='*70}")
print("HQC COST TABLE (280,000 shots - force measurement)")
print(f"{'='*70}")
hdr2 = f"{'Config':<28} {'HQC_orig':>12} {'HQC_opt':>12} {'Saved':>12} {'%':>6}"
print(hdr2)
print("-" * len(hdr2))
for label, r in results.items():
    ho = r['hqc']['original_280k']
    hn = r['hqc']['optimized_280k']
    hs = r['hqc']['savings_280k']
    hp = hs / ho * 100 if ho > 0 else 0
    print(f"{label:<28} {ho:>12,.0f} {hn:>12,.0f} {hs:>12,.0f} {hp:>5.1f}%")

print(f"\n{'='*70}")
print("NOTES")
print(f"{'='*70}")
print("- Our MERA uses a compact 1-CX decomposition per disentangler/isometry block.")
print("  The Helios design doc assumed 3 CX per disentangler (full U(4) decomposition),")
print("  giving 140 CX for 32q/3-layer. Our actual circuit uses 57 CX -- already 2.5x")
print("  more efficient than the conservative estimate.")
print("- pytket's TK2 peephole merges consecutive CX gates on the same qubit pair")
print("  into a single 2Q interaction, yielding ~50% reduction.")
print("- The CX->ZZPhase rebase is 1:1 (each CX = one ZZPhase(0.5)).")
print("- The TK2->ZZPhase path uses DecomposeTK2 which picks the minimum ZZPhase count")
print("  per TK2 gate based on its interaction angles.")
print("- Quantinuum HQC formula: n_shots * (5 + n_2q_gates / 10)")
print("- Helios logical 2Q gate error: ~1e-4 (iceberg error-detection mode)")

# ── Save JSON ────────────────────────────────────────────────────────────────
out_json = "D:/quantum-worldline/research/data/hardware/pytket_compilation_results.json"
with open(out_json, 'w') as f:
    json.dump(results, f, indent=2, default=str)
print(f"\nJSON saved: {out_json}")
print("Done.")
