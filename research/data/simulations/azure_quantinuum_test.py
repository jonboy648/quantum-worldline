"""
Azure Quantum + Quantinuum emulator test.

Step 1: Submit a small 4-qubit MERA subcircuit to the syntax checker (free).
Step 2: If syntax passes, submit to the H1-1 emulator (uses HQC from Basic plan).

Uses pytket-quantinuum for circuit construction + azure-quantum for submission.
"""
import json
from pytket.circuit import Circuit, OpType
from pytket.extensions.quantinuum import QuantinuumBackend
from pytket.extensions.quantinuum.backends.api_wrappers import QuantinuumAPIError

# ── Build a minimal 4-qubit MERA layer ──────────────────────────────
# This is one disentangler + one isometry from our binary MERA
def build_mini_mera() -> Circuit:
    """4-qubit MERA subcircuit: 1 disentangler + 1 isometry + measurement."""
    c = Circuit(4)

    # Disentangler on qubits 0,1
    c.Rz(0.3, 0).Ry(0.5, 0)
    c.Rz(0.3, 1).Ry(0.5, 1)
    c.ZZMax(0, 1)
    c.Rz(0.2, 0).Ry(0.4, 0)
    c.Rz(0.2, 1).Ry(0.4, 1)

    # Isometry on qubits 1,2,3 (coarse-grains 2->1)
    c.Rz(0.1, 1).Ry(0.6, 1)
    c.Rz(0.1, 2).Ry(0.6, 2)
    c.ZZMax(1, 2)
    c.Rz(0.3, 2).Ry(0.2, 2)
    c.Rz(0.3, 3).Ry(0.2, 3)
    c.ZZMax(2, 3)

    # Measure all
    c.measure_all()
    return c


def main():
    circ = build_mini_mera()
    print(f"Circuit: {circ.n_qubits} qubits, {circ.n_gates} gates, depth {circ.depth()}")

    # Connect to Azure Quantum workspace
    # pytket-quantinuum can authenticate via azure-quantum
    # We use the syntax checker target first (completely free)

    print("\n-- Step 1: Syntax Checker (free) --")
    try:
        # Try machine_debug first - this runs locally without any API connection
        backend_debug = QuantinuumBackend(
            device_name="H1-1SC",  # Syntax Checker
            machine_debug=True     # Local emulation mode
        )
        compiled = backend_debug.get_compiled_circuit(circ)
        print(f"Compiled: {compiled.n_gates} gates, depth {compiled.depth()}")

        # Count gate types
        gate_counts = {}
        for gate in compiled.get_commands():
            op_name = gate.op.type.name
            gate_counts[op_name] = gate_counts.get(op_name, 0) + 1
        print(f"Gate counts: {json.dumps(gate_counts, indent=2)}")

        # Run locally in debug mode (simulates syntax checker behavior)
        handle = backend_debug.process_circuit(compiled, n_shots=100)
        result = backend_debug.get_result(handle)
        counts = result.get_counts()
        print(f"Debug run: {len(counts)} unique bitstrings from 100 shots")
        print(f"Top 5 outcomes: {dict(sorted(counts.items(), key=lambda x: -x[1])[:5])}")
        print("Syntax check: PASSED (debug mode)")

    except Exception as e:
        print(f"Debug mode error: {e}")
        return

    # Step 2: Try actual API connection
    print("\n-- Step 2: Azure Quantum API connection test --")
    try:
        # This will attempt to authenticate via azure-identity
        # (browser login or cached credentials)
        backend_api = QuantinuumBackend(
            device_name="H1-1SC",  # Syntax Checker (free)
        )
        print("API backend created successfully")
        print(f"Device: {backend_api.device_name}")

        # Try to get device status
        # This will trigger authentication
        compiled_api = backend_api.get_compiled_circuit(circ)
        handle_api = backend_api.process_circuit(compiled_api, n_shots=10)
        result_api = backend_api.get_result(handle_api)
        counts_api = result_api.get_counts()
        print(f"API syntax check: PASSED")
        print(f"Results: {dict(sorted(counts_api.items(), key=lambda x: -x[1])[:5])}")

    except QuantinuumAPIError as e:
        print(f"API auth needed: {e}")
        print("Run: pytket-quantinuum login  (or set PYTKET_QUANTINUUM_API_KEY)")
    except Exception as e:
        print(f"API connection: {type(e).__name__}: {e}")
        print("\nTo authenticate, you may need to run:")
        print("  az login  (Azure CLI)")
        print("  or set environment variables for Quantinuum API")

    print("\n-- Summary --")
    print("Circuit compiles to Quantinuum native gates: YES")
    print("Local debug simulation works: YES")
    print("Next: authenticate to Azure Quantum for real emulator access")


if __name__ == "__main__":
    main()
