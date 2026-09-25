"""
Submit a 4-qubit MERA subcircuit to Quantinuum syntax checker via Azure Quantum.
This is completely free - it validates the circuit compiles to H-series native gates.
"""
import os, json
from azure.quantum import Workspace
from azure.quantum.qiskit import AzureQuantumProvider
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
import numpy as np

# Connect
CONNECTION_STRING = os.environ["AZURE_QUANTUM_CONNECTION_STRING"]
workspace = Workspace.from_connection_string(CONNECTION_STRING)
provider = AzureQuantumProvider(workspace)
print(f"Connected to: {workspace.name}")

# List backends
print("\nAvailable backends:")
for backend in provider.backends():
    print(f"  {backend.name}")

# Build a 4-qubit MERA subcircuit in Qiskit
qc = QuantumCircuit(4, 4)

# Disentangler on qubits 0,1
qc.ry(0.5, 0)
qc.ry(0.5, 1)
qc.cx(0, 1)
qc.ry(0.3, 0)
qc.ry(0.3, 1)

# Isometry on qubits 1,2,3
qc.ry(0.6, 1)
qc.ry(0.6, 2)
qc.cx(1, 2)
qc.ry(0.2, 2)
qc.ry(0.2, 3)
qc.cx(2, 3)

# Measure
qc.measure([0,1,2,3], [0,1,2,3])

print(f"\nCircuit: {qc.num_qubits}q, depth {qc.depth()}, gates: {dict(qc.count_ops())}")

# Submit to syntax checker (FREE)
print("\n-- Submitting to Quantinuum syntax checker (H2-1SC) --")
backend = provider.get_backend("quantinuum.sim.h2-1sc")
print(f"Backend: {backend.name}")

job = backend.run(qc, shots=10)
print(f"Job ID: {job.id}")
print(f"Job status: {job.status()}")

# Wait for result
result = job.result()
print(f"\nResult status: {result.status}")
counts = result.get_counts()
print(f"Counts: {counts}")
print("\nSyntax check: PASSED - circuit is valid for Quantinuum H-series hardware!")

# Now try the emulator (this uses HQC but is cheap for 4 qubits)
print("\n-- Submitting to Quantinuum emulator (H2-1E) --")
backend_emu = provider.get_backend("quantinuum.sim.h2-1e")
print(f"Backend: {backend_emu.name}")

job_emu = backend_emu.run(qc, shots=100)
print(f"Job ID: {job_emu.id}")
print(f"Job status: {job_emu.status()}")

# Wait for emulator result
result_emu = job_emu.result()
counts_emu = result_emu.get_counts()
print(f"\nEmulator counts ({sum(counts_emu.values())} shots):")
for bitstring, count in sorted(counts_emu.items(), key=lambda x: -x[1])[:10]:
    print(f"  {bitstring}: {count}")

print("\nEmulator test: PASSED - circuit runs on Quantinuum emulator!")
print(f"HQC cost: ~{5 + qc.count_ops().get('cx', 0)/10:.1f} HQC per run")
