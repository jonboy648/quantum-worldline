"""
PROBE 1 (task #95 verification): REAL pytket compile of the 25-operator ADAPT ansatz.

The headline claim "ZZPhase <= 75 (= 3 * 25)" is a HEURISTIC (3 per 2-qubit generator), not a
compile. This script reconstructs the EXACT ADAPT circuit STRUCTURE from the ordered "added"
generators in adapt_vqe_results.json, builds it as a chain of exp(i*theta*P) Pauli-evolution
gates (pytket PauliExpBox), and compiles it to a Quantinuum-Helios-like native gateset
{ZZPhase, PhasedX, Rz} to get the TRUE two-qubit (ZZPhase) gate count.

Gate count after compilation depends only on circuit STRUCTURE, not angle values, so placeholder
nonzero angles are fine (the optimized angles were not saved). We still use distinct nonzero
placeholders so peephole optimisation cannot trivially cancel a gate that a real run would keep.

Two compile levels are reported so the comparison is honest:
  (1) NAIVE rebase only (DecomposeBoxes + AutoRebase): no cross-gate merging. Upper-bound-ish.
  (2) OPTIMISED (FullPeepholeOptimise before rebase + RemoveRedundancies after): what a real
      Quantinuum submission would actually run. This is the number that matters for cost/EV.

Compare to: heuristic 75, and chi=3 MERA's REAL compiled 451 ZZPhase.
"""
import json

import numpy as np
from pytket.circuit import Circuit, PauliExpBox, OpType
from pytket.pauli import Pauli
from pytket.passes import (DecomposeBoxes, AutoRebase, FullPeepholeOptimise,
                           RemoveRedundancies, SequencePass)

RESULTS = "D:/quantum-worldline/research/data/builds/adapt_vqe_results.json"
OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_compile_results.json"
L = 8
HEURISTIC_75 = 75
CHI3_451 = 451
# Quantinuum / Helios native gateset
QTM_GATESET = {OpType.ZZPhase, OpType.PhasedX, OpType.Rz}

PAULI = {"X": Pauli.X, "Y": Pauli.Y, "Z": Pauli.Z, "I": Pauli.I}


def parse_generator(name):
    """Parse a generator name like 'Y0Z1', 'Z5Y6', 'Y3' into (paulis, qubits).

    Returns (list[Pauli], list[int]) e.g. 'Y0Z1' -> ([Pauli.Y, Pauli.Z], [0,1]).
    Names are concatenations of <Letter><index> tokens; index is a single digit here (L=8).
    """
    paulis, qubits = [], []
    i = 0
    while i < len(name):
        letter = name[i]
        assert letter in PAULI, f"bad pauli letter {letter} in {name}"
        j = i + 1
        num = ""
        while j < len(name) and name[j].isdigit():
            num += name[j]
            j += 1
        assert num != "", f"no qubit index after {letter} in {name}"
        paulis.append(PAULI[letter])
        qubits.append(int(num))
        i = j
    return paulis, qubits


def build_adapt_circuit(added_names, rng):
    """Build the ADAPT ansatz as a chain of PauliExpBox(exp(i*theta*P)) in append order.

    Placeholder angles: distinct nonzero values so structure is preserved and trivial
    cancellation is avoided. Gate count post-compile is structure-only, so this is faithful.
    """
    c = Circuit(L)
    for name in added_names:
        paulis, qubits = parse_generator(name)
        theta = float(rng.uniform(0.15, 0.85))  # nonzero, distinct, in (0,1)*pi units
        c.add_pauliexpbox(PauliExpBox(paulis, theta), qubits)
    return c


def counts(c):
    return {
        "ZZPhase": c.n_gates_of_type(OpType.ZZPhase),
        "ZZMax": c.n_gates_of_type(OpType.ZZMax),
        "PhasedX": c.n_gates_of_type(OpType.PhasedX),
        "Rz": c.n_gates_of_type(OpType.Rz),
        "total_gates": c.n_gates,
        "depth": c.depth(),
    }


def main():
    with open(RESULTS) as f:
        data = json.load(f)
    added = [s["added"] for s in data["steps"]]
    assert len(added) == 25, f"expected 25 steps, got {len(added)}"
    n_2q_generators = sum(1 for nm in added if len(parse_generator(nm)[1]) == 2)
    n_1q_generators = len(added) - n_2q_generators

    print("=" * 74)
    print("PROBE 1: REAL pytket compile of the 25-op ADAPT ansatz")
    print("=" * 74)
    print(f"generators ({len(added)}): {added}")
    print(f"  two-qubit generators: {n_2q_generators}, single-qubit: {n_1q_generators}")
    print(f"  heuristic claim: 3 * {n_2q_generators} = {3*n_2q_generators} ZZPhase "
          f"(reported as {HEURISTIC_75})")
    print(f"  chi=3 MERA real compile: {CHI3_451} ZZPhase\n")

    rng = np.random.default_rng(20260607)

    # ---- (1) NAIVE: decompose boxes, rebase to native, no cross-gate optimisation ----
    c_naive = build_adapt_circuit(added, np.random.default_rng(20260607))
    DecomposeBoxes().apply(c_naive)
    AutoRebase(QTM_GATESET).apply(c_naive)
    naive = counts(c_naive)
    print("(1) NAIVE rebase  (DecomposeBoxes + AutoRebase -> {ZZPhase,PhasedX,Rz}):")
    print(f"    ZZPhase={naive['ZZPhase']}  PhasedX={naive['PhasedX']}  Rz={naive['Rz']}  "
          f"total={naive['total_gates']}  depth={naive['depth']}")

    # ---- (2) OPTIMISED: what a real Quantinuum submission runs ----
    c_opt = build_adapt_circuit(added, np.random.default_rng(20260607))
    seq = SequencePass([
        DecomposeBoxes(),
        FullPeepholeOptimise(),
        AutoRebase(QTM_GATESET),
        RemoveRedundancies(),
    ])
    seq.apply(c_opt)
    opt = counts(c_opt)
    print("\n(2) OPTIMISED  (DecomposeBoxes + FullPeepholeOptimise + AutoRebase + "
          "RemoveRedundancies):")
    print(f"    ZZPhase={opt['ZZPhase']}  PhasedX={opt['PhasedX']}  Rz={opt['Rz']}  "
          f"total={opt['total_gates']}  depth={opt['depth']}")

    # ---- verdict ----
    compiled_2q = opt["ZZPhase"]      # the number that matters for a real submission
    naive_2q = naive["ZZPhase"]
    advantage_vs_chi3 = CHI3_451 / compiled_2q if compiled_2q else float("inf")
    heuristic_was = ("CORRECT" if compiled_2q == HEURISTIC_75 else
                     "INFLATED (real < heuristic)" if compiled_2q < HEURISTIC_75 else
                     "OPTIMISTIC (real > heuristic)")
    print("\n" + "=" * 74)
    print(f"  heuristic 75            : {HEURISTIC_75}")
    print(f"  chi=3 MERA real         : {CHI3_451}")
    print(f"  ADAPT naive rebase 2q   : {naive_2q}")
    print(f"  ADAPT optimised 2q (REAL): {compiled_2q}")
    print(f"  heuristic was           : {heuristic_was}")
    print(f"  real advantage vs chi=3 : {advantage_vs_chi3:.2f}x "
          f"(claimed 6x)")

    out = {
        "n_generators": len(added),
        "n_2q_generators": n_2q_generators,
        "n_1q_generators": n_1q_generators,
        "added_order": added,
        "heuristic_75": HEURISTIC_75,
        "chi3_451": CHI3_451,
        "gateset_used": "Quantinuum/Helios native {ZZPhase, PhasedX, Rz}",
        "naive_rebase": naive,
        "optimised": opt,
        "compiled_2q_count": compiled_2q,
        "naive_2q_count": naive_2q,
        "advantage_vs_chi3_real": advantage_vs_chi3,
        "claimed_advantage": 6,
        "heuristic_verdict": heuristic_was,
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  saved -> {OUT}")


if __name__ == "__main__":
    main()
