"""
LEAD CROSS-CHECK (task #95): independent recompile of the 25-op ADAPT ansatz.

Settles the disputed ZZPhase count between the attack (42, FullPeepholeOptimise)
and the verifier (33, GreedyPauliSimp). Tries every reasonable Quantinuum-native
compile route and reports the full spread, plus a per-box decomposition sanity check.

Also confirms the chi3=451 baseline is a DIFFERENT object (16q / 2-layer holographic
MERA) than the ADAPT circuit (8q bare state-prep), so the "ratio" is documented honestly.

Structure-only: angles were not saved, so distinct nonzero placeholders are used.
Gate count after compile of a Pauli-evolution chain is structure-only (angle-invariant),
which we re-verify across 8 seeds.
"""
import json

import numpy as np
from pytket.circuit import Circuit, PauliExpBox, OpType
from pytket.pauli import Pauli
from pytket.passes import (DecomposeBoxes, AutoRebase, FullPeepholeOptimise,
                           RemoveRedundancies, SequencePass)

RESULTS = "D:/quantum-worldline/research/data/builds/adapt_vqe_results.json"
OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_compile_lead_results.json"
L = 8
QTM = {OpType.ZZPhase, OpType.PhasedX, OpType.Rz}
PAULI = {"X": Pauli.X, "Y": Pauli.Y, "Z": Pauli.Z, "I": Pauli.I}


def parse_generator(name):
    paulis, qubits = [], []
    i = 0
    while i < len(name):
        letter = name[i]
        j = i + 1
        num = ""
        while j < len(name) and name[j].isdigit():
            num += name[j]
            j += 1
        paulis.append(PAULI[letter])
        qubits.append(int(num))
        i = j
    return paulis, qubits


def build(added, rng):
    c = Circuit(L)
    for name in added:
        paulis, qubits = parse_generator(name)
        theta = float(rng.uniform(0.15, 0.85))
        c.add_pauliexpbox(PauliExpBox(paulis, theta), qubits)
    return c


def zz(c):
    return c.n_gates_of_type(OpType.ZZPhase)


def main():
    with open(RESULTS) as f:
        data = json.load(f)
    added = [s["added"] for s in data["steps"]]
    n2 = sum(1 for nm in added if len(parse_generator(nm)[1]) == 2)
    n1 = len(added) - n2
    print(f"generators={len(added)}  2q-gen={n2}  1q-gen={n1}")
    print(f"heuristic = 3*{n2} = {3*n2}")

    routes = {}

    # naive
    c = build(added, np.random.default_rng(1))
    DecomposeBoxes().apply(c)
    AutoRebase(QTM).apply(c)
    routes["naive_rebase"] = zz(c)

    # FullPeepholeOptimise (attack's route)
    c = build(added, np.random.default_rng(1))
    SequencePass([DecomposeBoxes(), FullPeepholeOptimise(), AutoRebase(QTM),
                  RemoveRedundancies()]).apply(c)
    routes["fullpeephole"] = zz(c)

    # GreedyPauliSimp -- canonical for Pauli-evolution circuits (verifier's route)
    try:
        from pytket.passes import GreedyPauliSimp
        c = build(added, np.random.default_rng(1))
        GreedyPauliSimp().apply(c)
        AutoRebase(QTM).apply(c)
        RemoveRedundancies().apply(c)
        routes["greedy_pauli_simp"] = zz(c)
    except Exception as e:
        routes["greedy_pauli_simp"] = f"ERR:{e}"

    # PauliSimp (older term-sequencing synthesis)
    try:
        from pytket.passes import PauliSimp
        c = build(added, np.random.default_rng(1))
        PauliSimp().apply(c)
        DecomposeBoxes().apply(c)
        FullPeepholeOptimise().apply(c)
        AutoRebase(QTM).apply(c)
        RemoveRedundancies().apply(c)
        routes["pauli_simp"] = zz(c)
    except Exception as e:
        routes["pauli_simp"] = f"ERR:{e}"

    # Quantinuum backend default compilation (the REAL submission path), if available
    try:
        from pytket.extensions.quantinuum import QuantinuumBackend
        # offline: use a device name without login by building a default pass via
        # the backend's static helper if present; else skip gracefully.
        backend = QuantinuumBackend(device_name="H1-1LE")  # local emulator descriptor
        c = build(added, np.random.default_rng(1))
        DecomposeBoxes().apply(c)
        cu = backend.get_compiled_circuit(c, optimisation_level=2)
        routes["quantinuum_backend_optlvl2"] = zz(cu)
    except Exception as e:
        routes["quantinuum_backend_optlvl2"] = f"ERR:{type(e).__name__}:{str(e)[:80]}"

    # angle-invariance check on the best static route (greedy if available else peephole)
    seeds_zz = []
    for s in range(8):
        c = build(added, np.random.default_rng(1000 + s))
        try:
            from pytket.passes import GreedyPauliSimp
            GreedyPauliSimp().apply(c)
        except Exception:
            SequencePass([DecomposeBoxes(), FullPeepholeOptimise()]).apply(c)
        AutoRebase(QTM).apply(c)
        RemoveRedundancies().apply(c)
        seeds_zz.append(zz(c))

    best = min(v for v in routes.values() if isinstance(v, int))

    print("\nROUTES (ZZPhase count):")
    for k, v in routes.items():
        print(f"  {k:32s} {v}")
    print(f"\nBEST (min over routes): {best}")
    print(f"angle-invariance seeds (best route): {seeds_zz} "
          f"(unique={sorted(set(seeds_zz))})")
    print("\nchi3 baseline = 451 ZZPhase on a 16-qubit 2-layer MERA "
          "(boundary 8q + top 4q + 4 ancillas); ADAPT is 8-qubit bare state-prep.")
    print(f"ratio 451/{best} = {451/best:.2f}x  (NOT apples-to-apples: different qubit "
          f"count and different deliverable)")

    out = {
        "n_generators": len(added),
        "n_2q_generators": n2,
        "heuristic_75": 3 * n2,
        "routes_zzphase": routes,
        "best_zzphase": best,
        "angle_invariance_seeds": seeds_zz,
        "chi3_451": 451,
        "chi3_qubits": 16,
        "adapt_qubits": 8,
        "ratio_best": 451 / best,
        "apples_to_apples": False,
        "note": "451 = 16q 2-layer holographic MERA; ADAPT = 8q bare GS prep. Ratio is informational only.",
    }
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\nsaved -> {OUT}")


if __name__ == "__main__":
    main()
