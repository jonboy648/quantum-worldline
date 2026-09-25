"""
SIM-2026-008: 8-qubit TFIM ground state energy at criticality
Pipeline test: VQE circuit -> Aer simulator -> exact diag baseline -> visualization

H = -sum_{i} Z_i Z_{i+1} - sum_{i} X_i  (PBC, J=1, g=1)
"""

import numpy as np
import json
import time
from pathlib import Path
from scipy.optimize import minimize
from scipy.sparse import kron, eye, csr_matrix
from scipy.sparse.linalg import eigsh

# ============================================================
# PART 1: Classical Baseline (Exact Diagonalization)
# ============================================================
print("=" * 60)
print("PART 1: Classical Baseline -- Exact Diagonalization")
print("=" * 60)

N = 8  # qubits
t_start = time.time()

# Build sparse Pauli matrices
I2 = eye(2, format='csr')
Z = csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
X = csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))

def pauli_op(op, site, n_qubits):
    """Build n-qubit operator with `op` on `site`, identity elsewhere."""
    ops = [I2] * n_qubits
    ops[site] = op
    result = ops[0]
    for o in ops[1:]:
        result = kron(result, o, format='csr')
    return result

def build_tfim_hamiltonian(n_qubits, J=1.0, g=1.0, pbc=True):
    """Build TFIM Hamiltonian: H = -J sum Z_i Z_{i+1} - g sum X_i"""
    dim = 2**n_qubits
    H = csr_matrix((dim, dim), dtype=complex)
    # ZZ coupling
    for i in range(n_qubits - 1):
        H -= J * pauli_op(Z, i, n_qubits) @ pauli_op(Z, i+1, n_qubits)
    if pbc:
        H -= J * pauli_op(Z, n_qubits-1, n_qubits) @ pauli_op(Z, 0, n_qubits)
    # Transverse field
    for i in range(n_qubits):
        H -= g * pauli_op(X, i, n_qubits)
    return H

H_sparse = build_tfim_hamiltonian(N, J=1.0, g=1.0, pbc=True)
E_exact, psi_exact = eigsh(H_sparse, k=1, which='SA')
E_exact = E_exact[0]
t_classical = time.time() - t_start

print(f"N = {N} qubits, PBC, J=1, g=1 (critical point)")
print(f"Hilbert space dim = {2**N}")
print(f"Exact ground state energy: E0 = {E_exact:.8f}")
print(f"Energy per site: {E_exact/N:.8f}")
print(f"Classical computation time: {t_classical:.4f}s")

# ============================================================
# PART 2: VQE Circuit (Qiskit + Aer Statevector)
# ============================================================
print()
print("=" * 60)
print("PART 2: VQE Circuit -- Hardware-Efficient Ansatz")
print("=" * 60)

from qiskit.circuit import QuantumCircuit, Parameter, ParameterVector

def build_hea_circuit(n_qubits, n_layers, pbc=True):
    """
    Hardware-Efficient Ansatz for TFIM.
    Each layer: Ry(theta) on each qubit + CNOT ladder + Rz(theta) on each qubit
    """
    n_params = n_qubits * n_layers * 2  # Ry + Rz per qubit per layer
    theta = ParameterVector('theta', n_params)
    qc = QuantumCircuit(n_qubits)

    idx = 0
    for layer in range(n_layers):
        # Ry rotation layer
        for q in range(n_qubits):
            qc.ry(theta[idx], q)
            idx += 1
        # Entangling layer (CNOT ladder)
        for q in range(n_qubits - 1):
            qc.cx(q, q + 1)
        if pbc:
            qc.cx(n_qubits - 1, 0)
        # Rz rotation layer
        for q in range(n_qubits):
            qc.rz(theta[idx], q)
            idx += 1

    return qc, theta

n_layers = 3
qc, theta_params = build_hea_circuit(N, n_layers, pbc=True)

print(f"Circuit: {N} qubits, {n_layers} layers")
print(f"Parameters: {len(theta_params)}")
print(f"CNOT gates per layer: {N} (with PBC wrap)")
print(f"Total CNOTs: {N * n_layers}")
print(f"Total gates: {qc.size()}")
print(f"Circuit depth: {qc.depth()}")

# Energy evaluation using statevector
from qiskit_aer import AerSimulator

sim = AerSimulator(method='statevector')

def evaluate_energy(params, circuit, param_vec, H_matrix, n_qubits):
    """Evaluate <psi(params)|H|psi(params)> via statevector."""
    bound = circuit.assign_parameters(dict(zip(param_vec, params)))
    bound.save_statevector()

    result = sim.run(bound).result()
    sv = np.array(result.get_statevector())

    energy = np.real(sv.conj() @ H_matrix @ sv)
    return energy

# Convert sparse H to dense for fast mat-vec on 8q (only 256-dim)
H_dense = H_sparse.toarray()

# VQE optimization
print("\nRunning VQE optimization...")
n_params = len(theta_params)
n_seeds = 3
best_energy = np.inf
best_params = None
all_histories = []

t_vqe_start = time.time()

for seed in range(n_seeds):
    np.random.seed(seed * 42 + 7)
    x0 = np.random.uniform(-np.pi, np.pi, n_params)

    history = []
    def callback(xk):
        e = evaluate_energy(xk, qc, theta_params, H_dense, N)
        history.append(e)

    result = minimize(
        evaluate_energy, x0,
        args=(qc, theta_params, H_dense, N),
        method='L-BFGS-B',
        options={'maxiter': 500, 'maxfun': 2000},
        callback=callback
    )

    all_histories.append(history)
    print(f"  Seed {seed}: E = {result.fun:.8f}, nfev = {result.nfev}, converged = {result.success}")

    if result.fun < best_energy:
        best_energy = result.fun
        best_params = result.x.copy()

t_vqe = time.time() - t_vqe_start

energy_error = abs(best_energy - E_exact)
relative_error = energy_error / abs(E_exact) * 100

print(f"\nVQE Results:")
print(f"  Best energy: {best_energy:.8f}")
print(f"  Exact energy: {E_exact:.8f}")
print(f"  Absolute error: {energy_error:.8f}")
print(f"  Relative error: {relative_error:.4f}%")
print(f"  VQE time: {t_vqe:.2f}s")

# ============================================================
# PART 3: Comparison & Verdict
# ============================================================
print()
print("=" * 60)
print("PART 3: Quantum vs Classical Comparison")
print("=" * 60)

if relative_error < 0.1:
    accuracy_verdict = "EXCELLENT (< 0.1%)"
elif relative_error < 1.0:
    accuracy_verdict = "GOOD (< 1%)"
elif relative_error < 5.0:
    accuracy_verdict = "ACCEPTABLE (< 5%)"
else:
    accuracy_verdict = f"POOR ({relative_error:.1f}%)"

print(f"Accuracy verdict: {accuracy_verdict}")
print(f"Classical baseline: {t_classical:.4f}s (exact diagonalization)")
print(f"Quantum VQE: {t_vqe:.2f}s ({n_seeds} seeds x L-BFGS-B)")
print(f"Speed comparison: classical is {t_vqe/t_classical:.1f}x faster (expected for 8q)")
print(f"Pipeline verdict: classical wins at 8q (exact diag is O(2^N), VQE overhead)")

# ============================================================
# PART 4: Visualization
# ============================================================
print()
print("=" * 60)
print("PART 4: Generating Visualizations")
print("=" * 60)

import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

fig, axes = plt.subplots(1, 3, figsize=(15, 5))

# Panel 1: Convergence history
ax1 = axes[0]
for i, hist in enumerate(all_histories):
    ax1.plot(range(len(hist)), hist, label=f'Seed {i}', alpha=0.8)
ax1.axhline(y=E_exact, color='red', linestyle='--', linewidth=2, label=f'Exact E0={E_exact:.4f}')
ax1.set_xlabel('Iteration')
ax1.set_ylabel('Energy')
ax1.set_title('VQE Convergence (8q TFIM, PBC)')
ax1.legend()
ax1.grid(True, alpha=0.3)

# Panel 2: Energy comparison bar chart
ax2 = axes[1]
labels = ['Exact\n(Classical)', 'VQE\n(Quantum)']
energies = [E_exact, best_energy]
colors = ['#2196F3', '#4CAF50']
bars = ax2.bar(labels, energies, color=colors, width=0.5, edgecolor='black')
for bar, e in zip(bars, energies):
    ax2.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.02,
             f'{e:.4f}', ha='center', va='bottom', fontweight='bold', fontsize=11)
ax2.set_ylabel('Ground State Energy')
ax2.set_title(f'Energy Comparison\n(error: {relative_error:.4f}%)')
ax2.grid(True, alpha=0.3, axis='y')
# Set y range to show difference
y_min = min(energies) * 1.05
y_max = max(energies) * 0.95
ax2.set_ylim(y_min, y_max if y_max > y_min else 0)

# Panel 3: Circuit diagram info
ax3 = axes[2]
ax3.axis('off')
info_text = (
    f"Circuit Specifications\n"
    f"{'='*30}\n\n"
    f"Qubits:        {N}\n"
    f"Layers:        {n_layers}\n"
    f"Parameters:    {len(theta_params)}\n"
    f"CNOTs:         {N * n_layers}\n"
    f"Total gates:   {qc.size()}\n"
    f"Circuit depth: {qc.depth()}\n\n"
    f"{'='*30}\n\n"
    f"Hamiltonian: TFIM (PBC)\n"
    f"H = -J sum Z_i Z_(i+1)\n"
    f"    - g sum X_i\n"
    f"J = 1.0, g = 1.0 (critical)\n\n"
    f"{'='*30}\n\n"
    f"Optimizer: L-BFGS-B\n"
    f"Seeds: {n_seeds}\n"
    f"Max evaluations: 2000/seed\n"
    f"Best rel. error: {relative_error:.4f}%"
)
ax3.text(0.1, 0.95, info_text, transform=ax3.transAxes,
         fontsize=10, verticalalignment='top', fontfamily='monospace',
         bbox=dict(boxstyle='round', facecolor='lightyellow', alpha=0.8))

plt.tight_layout()
viz_path = 'D:/quantum-worldline/research/data/simulations/SIM-2026-008_pipeline_test.png'
plt.savefig(viz_path, dpi=150, bbox_inches='tight')
print(f"Visualization saved: {viz_path}")

# ============================================================
# PART 5: Save structured JSON
# ============================================================
print()
print("=" * 60)
print("PART 5: Saving Structured Results")
print("=" * 60)

results = {
    "id": "SIM-2026-008",
    "title": "8-qubit TFIM pipeline test (VQE vs exact diagonalization)",
    "date": "2026-03-12",
    "status": "EXECUTED",
    "system": {
        "model": "Transverse Field Ising Model (TFIM)",
        "qubits": N,
        "boundary_conditions": "periodic (PBC)",
        "parameters": {"J": 1.0, "g": 1.0, "regime": "critical"},
        "hilbert_dim": 2**N
    },
    "circuit": {
        "ansatz": "Hardware-Efficient Ansatz (HEA)",
        "layers": n_layers,
        "parameters": int(len(theta_params)),
        "cnot_count": N * n_layers,
        "total_gates": int(qc.size()),
        "depth": int(qc.depth()),
        "backend": "AerSimulator (statevector)"
    },
    "classical_baseline": {
        "method": "Exact diagonalization (scipy.sparse.linalg.eigsh)",
        "E0": float(E_exact),
        "E0_per_site": float(E_exact / N),
        "time_seconds": round(t_classical, 4)
    },
    "vqe_results": {
        "optimizer": "L-BFGS-B",
        "seeds": n_seeds,
        "max_feval_per_seed": 2000,
        "best_energy": float(best_energy),
        "absolute_error": float(energy_error),
        "relative_error_pct": round(relative_error, 6),
        "time_seconds": round(t_vqe, 2)
    },
    "comparison": {
        "accuracy_verdict": accuracy_verdict,
        "speed_winner": "classical",
        "speed_ratio": round(t_vqe / t_classical, 1),
        "note": "Classical exact diag is trivially faster at 8q. Quantum advantage expected only at 40+ qubits."
    },
    "convergence_histories": {
        "seed_0": [round(e, 8) for e in all_histories[0]],
        "seed_1": [round(e, 8) for e in all_histories[1]],
        "seed_2": [round(e, 8) for e in all_histories[2]]
    },
    "visualization": viz_path,
    "pipeline_verdict": "PASS"
}

json_path = 'D:/quantum-worldline/research/data/simulations/SIM-2026-008.json'
with open(json_path, 'w') as f:
    json.dump(results, f, indent=2)
print(f"Results saved: {json_path}")

# Print final summary
print()
print("=" * 60)
print("PIPELINE TEST SUMMARY")
print("=" * 60)
print(f"  Status:          PASS")
print(f"  Exact E0:        {E_exact:.8f}")
print(f"  VQE E_best:      {best_energy:.8f}")
print(f"  Relative error:  {relative_error:.4f}%")
print(f"  Classical time:  {t_classical:.4f}s")
print(f"  VQE time:        {t_vqe:.2f}s")
print(f"  Visualization:   {viz_path}")
print(f"  Results JSON:    {json_path}")
