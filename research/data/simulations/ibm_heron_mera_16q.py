"""
IBM Heron r3 Hardware Experiment: Analytical MERA ZZ Correlators
================================================================
Prepares the 16-qubit analytical MERA state (Evenbly-White 2016) on a quantum circuit,
transpiles to IBM Heron r3 (ibm_fez / ibm_marrakesh) native gate set, and reports
circuit statistics without submitting to hardware.

Physics goal:
- Demonstrate that the analytical MERA circuit produces critical ZZ correlations
  consistent with power-law decay C(r) ~ r^(-1/4) (CFT prediction for TFIM).
- This serves as the quantum-hardware component of the holographic transport paper:
  the MERA faithfully encodes AdS3 causal structure (0.72% transport error in sim),
  and this circuit verifies the quantum state preparation on real hardware.

Circuit design:
- 16-qubit brick-wall MERA circuit: 3 layers of u (disentangler) and w (isometry)
- u and w are fixed 4x4 real unitary matrices from Evenbly & White 2016 (Eq S3-S4)
- Each layer applies w to all even pairs (0,1),(2,3),...,(14,15)
  then u to all odd pairs (1,2),(3,4),...,(13,14)
- Starting from |0>^16, this produces the scale-invariant MERA ground state approx.
- The state has entanglement structure of a CFT vacuum, exhibiting power-law ZZ correlations.

DO NOT SUBMIT to hardware without explicit user approval.
Run locally first to get circuit stats and verify correlators on simulator.
"""

import sys
import io
import json
import time
import numpy as np

# Unicode-safe output for Windows cp1252 consoles
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=" * 70)
print("IBM Heron r3 MERA Circuit Builder")
print("16q Analytical MERA (Evenbly-White 2016) -- ZZ Correlator Measurement")
print("=" * 70, flush=True)

# ===========================================================================
# 1. Define MERA tensors (Evenbly & White 2016, Eq S3-S4)
# ===========================================================================
print("\n[1] Building MERA tensors...", flush=True)

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

sqrt3 = np.sqrt(3.0)
sqrt2 = np.sqrt(2.0)

# u_dag (disentangler adjoint) -- Eq S3
u_dag = (
    (sqrt3 + 2) / 4 * np.kron(I2, I2)
    + (sqrt3 - 2) / 4 * np.kron(Z, Z)
    + 1j / 4 * np.kron(X, Y)
    + 1j / 4 * np.kron(Y, X)
)
u = u_dag.conj().T  # u (not dagger) -- used for state prep (descending direction)

# w_dag (isometry adjoint) -- Eq S4
w_dag = (
    (sqrt3 + sqrt2) / 4 * np.kron(I2, I2)
    + (sqrt3 - sqrt2) / 4 * np.kron(Z, Z)
    + 1j * (1 + sqrt2) / 4 * np.kron(X, Y)
    + 1j * (1 - sqrt2) / 4 * np.kron(Y, X)
)
w = w_dag.conj().T  # w (not dagger) -- used for state prep (descending direction)

# Verify unitarity
u_err = np.max(np.abs(u_dag @ u - np.eye(4)))
w_err = np.max(np.abs(w_dag @ w - np.eye(4)))
print(f"  u unitary check: max|u_dag @ u - I| = {u_err:.2e}")
print(f"  w unitary check: max|w_dag @ w - I| = {w_err:.2e}")
assert u_err < 1e-12 and w_err < 1e-12, "Tensor unitarity check failed!"

# Check that tensors are real (important: real unitaries decompose with fewer gates)
u_imag_max = np.max(np.abs(np.imag(u)))
w_imag_max = np.max(np.abs(np.imag(w)))
print(f"  u imaginary part: max = {u_imag_max:.2e}  ({'REAL' if u_imag_max < 1e-12 else 'COMPLEX'})")
print(f"  w imaginary part: max = {w_imag_max:.2e}  ({'REAL' if w_imag_max < 1e-12 else 'COMPLEX'})")

# Display the matrices
print("\n  u (disentangler) =")
for row in u.real:
    vals = "  ".join(f"{v:+.4f}" for v in row)
    print(f"    [{vals}]")
print("  w (isometry) =")
for row in w.real:
    vals = "  ".join(f"{v:+.4f}" for v in row)
    print(f"    [{vals}]")

# ===========================================================================
# 2. Build the analytical MERA state preparation circuit
# ===========================================================================
print("\n[2] Building MERA circuit...", flush=True)

from qiskit import QuantumCircuit, QuantumRegister, ClassicalRegister
from qiskit.circuit.library import UnitaryGate
from qiskit.quantum_info import Operator

N_QUBITS = 16
N_LAYERS = 3   # 3 layers of u,w for L=16 (log2(16) = 4, gives 3 active layers)
N_SHOTS = 10000

# Create UnitaryGate objects from the MERA tensors
# NOTE: Qiskit uses little-endian qubit ordering internally, but we will be careful
# to add gates with the qubit ordering matching our convention.
# For a 2-qubit gate on (ctrl=site_i, target=site_j), Qiskit's UnitaryGate
# matrix convention: U[out_state, in_state] where state is (target, ctrl) in binary.
# To match our physics convention (tensor product: site_i is higher bit),
# we transpose the matrix indices for Qiskit's qubit ordering.
# Qiskit UnitaryGate: gate.definition acts on qubits [q0, q1] where
# the matrix is indexed as U[2*q0_out + q1_out, 2*q0_in + q1_in].
# Our convention: u[2*i + j, 2*k + l] = <ij|u|kl> with i = high-bit site.
# Qiskit appends gate to [low_qubit, high_qubit], and its matrix is
# in the low-first ordering. So we need to transpose qubit order.
# For a 2-qubit gate in our convention (A tensored with B = A on high, B on low):
# To add as qiskit UnitaryGate on [q_low, q_high], we need to swap qubit order.
# Swap unitary: S @ U_phys @ S where S is the SWAP gate matrix.
SWAP4 = np.array([[1,0,0,0],[0,0,1,0],[0,1,0,0],[0,0,0,1]], dtype=complex)

def phys_to_qiskit(mat_phys):
    """Convert 2-qubit gate from physics (big-endian) to Qiskit (little-endian) ordering."""
    return SWAP4 @ mat_phys @ SWAP4

# Build gates: apply qiskit ordering swap
u_qiskit = phys_to_qiskit(u)
w_qiskit = phys_to_qiskit(w)

u_gate = UnitaryGate(u_qiskit, label="u")
w_gate = UnitaryGate(w_qiskit, label="w")

def build_mera_circuit(n_qubits, n_layers, include_barriers=True):
    """
    Build the analytical MERA state preparation circuit.

    Structure: n_layers repetitions of:
      - w gate on all even pairs (0,1),(2,3),...,(n-2,n-1)
      - u gate on all odd pairs (1,2),(3,4),...,(n-3,n-2)

    Starting from |0>^n_qubits.

    The brick-wall structure is scale-invariant: each layer applies the same
    u,w tensors uniformly, consistent with the scale-invariant MERA ansatz.
    For L=16 qubits, 3 layers captures the entanglement structure of the
    MERA ground state (causal cone reaches dr=8 at 3 layers).

    Gate count:
      Per layer: L/2 w-gates + (L/2 - 1) u-gates
      L=16: 8 w + 7 u = 15 gates/layer
      3 layers: 45 gates total
    """
    qr = QuantumRegister(n_qubits, name="q")
    cr = ClassicalRegister(n_qubits, name="c")
    qc = QuantumCircuit(qr, cr)

    gate_log = []

    for layer in range(n_layers):
        # w gates on even pairs: (0,1), (2,3), ..., (n-2, n-1)
        for i in range(0, n_qubits - 1, 2):
            # Qiskit ordering: append gate to [q_low, q_high] = [q_i, q_{i+1}]
            qc.append(w_gate, [qr[i], qr[i + 1]])
            gate_log.append(("w", i, i + 1))

        # u gates on odd pairs: (1,2), (3,4), ..., (n-3, n-2)
        for i in range(1, n_qubits - 1, 2):
            qc.append(u_gate, [qr[i], qr[i + 1]])
            gate_log.append(("u", i, i + 1))

        if include_barriers and layer < n_layers - 1:
            qc.barrier()

    return qc, gate_log

# Build the main MERA circuit (no measurement yet -- add later for transpilation)
qc_mera, gate_log = build_mera_circuit(N_QUBITS, N_LAYERS, include_barriers=True)

print(f"  MERA circuit built: {N_QUBITS} qubits, {N_LAYERS} layers")
print(f"  Gates applied: {len(gate_log)} 2-qubit UnitaryGate blocks")
print(f"    w gates: {sum(1 for g in gate_log if g[0] == 'w')}")
print(f"    u gates: {sum(1 for g in gate_log if g[0] == 'u')}")
print(f"  Circuit depth (before transpile): {qc_mera.depth()}")

# ===========================================================================
# 3. Classical simulator verification of ZZ correlators
# ===========================================================================
print("\n[3] Classical simulator verification (Statevector)...", flush=True)

try:
    from qiskit_aer import AerSimulator
    from qiskit_aer.primitives import EstimatorV2 as AerEstimator
    from qiskit.quantum_info import SparsePauliOp

    # Build the MERA state on statevector simulator to check ZZ correlators
    qc_sv = build_mera_circuit(N_QUBITS, N_LAYERS, include_barriers=False)[0]

    # Run on statevector simulator
    sim = AerSimulator(method="statevector")
    qc_sv_save = qc_sv.copy()
    qc_sv_save.save_statevector()

    from qiskit.compiler import transpile
    qc_compiled = transpile(qc_sv_save, backend=sim, optimization_level=0)
    job = sim.run(qc_compiled, shots=1)
    sv = np.array(job.result().get_statevector(qc_compiled))

    print(f"  Statevector computed, dim={len(sv)}")
    print(f"  State norm: {np.linalg.norm(sv):.8f}")

    # Compute ZZ correlators C(site_0, site_0+dr) for dr = 1..8
    def zz_from_sv(sv, i, j, n):
        """Compute <Z_i Z_j> from statevector using bit manipulation."""
        total = 0.0
        for idx in range(len(sv)):
            # Z_i Z_j: eigenvalue (+1 if both same, -1 if different)
            bit_i = (idx >> (n - 1 - i)) & 1
            bit_j = (idx >> (n - 1 - j)) & 1
            sign = 1 if bit_i == bit_j else -1
            total += sign * abs(sv[idx]) ** 2
        return total

    anchor = 0  # measure from site 0
    print(f"\n  ZZ correlators C({anchor}, {anchor}+dr):")
    print(f"  {'dr':>4}  {'C(dr)':>10}  {'r^(-1/4)':>10}  {'ratio':>8}")
    print(f"  {'-'*40}")
    corrs = {}
    for dr in range(1, 9):
        j = anchor + dr
        if j < N_QUBITS:
            c = zz_from_sv(sv, anchor, j, N_QUBITS)
            pl = dr ** (-0.25)  # CFT prediction
            corrs[dr] = c
            print(f"  {dr:>4}  {c:>10.6f}  {pl:>10.6f}  {c/pl:>8.3f}")

    # Check power-law fit
    dr_vals = np.array(list(corrs.keys()), dtype=float)
    c_vals = np.array([corrs[dr] for dr in corrs.keys()])
    if np.all(c_vals > 0):
        log_dr = np.log(dr_vals)
        log_c = np.log(c_vals)
        coeffs = np.polyfit(log_dr, log_c, 1)
        alpha_fit = -coeffs[0]
        print(f"\n  Power-law fit C(r) ~ r^(-alpha): alpha = {alpha_fit:.4f}")
        print(f"  CFT prediction for critical TFIM: alpha = 0.2500")
        print(f"  Deviation from CFT: {abs(alpha_fit - 0.25)/0.25*100:.1f}%")
    else:
        print("\n  Note: some correlators non-positive -- power-law fit requires adjustment")

except ImportError as e:
    print(f"  AerSimulator not available: {e}")
    print("  Skipping classical verification (will be done on IBM simulator at submission)")
    corrs = {}
    sv = None

# ===========================================================================
# 4. Build measurement circuits for ZZ correlator tomography
# ===========================================================================
print("\n[4] Building measurement circuits...", flush=True)

# Strategy: measure ZZ correlators using simultaneous Pauli measurements.
# For C(i,j) = <Z_i Z_j>, we can measure all Z_i simultaneously in one shot
# because all ZZ correlators commute (they're all diagonal in the Z basis).
# This means ONE circuit with all-Z measurement covers ALL ZZ correlators!

def build_mera_zz_circuit(n_qubits, n_layers, anchor, dr_list):
    """
    Build MERA circuit with Z-basis measurement on all qubits.
    Post-process shots to extract ZZ correlators for all requested dr values.

    A single circuit with Z-measurement covers all ZZ pairs.
    """
    qc, _ = build_mera_circuit(n_qubits, n_layers, include_barriers=False)
    qc.measure_all()
    return qc

# One measurement circuit covers all ZZ correlators (Z basis is diagonal)
qc_measure = build_mera_zz_circuit(N_QUBITS, N_LAYERS, 0, list(range(1, 9)))
print(f"  Measurement circuit: {N_QUBITS} qubits, measure all in Z basis")
print(f"  One circuit covers ALL ZZ correlators (commuting observables)")
print(f"  Planned shots: {N_SHOTS:,}")
print(f"  Expected ZZ error per correlator: ~1/sqrt({N_SHOTS}) = {1/np.sqrt(N_SHOTS):.4f}")

# ===========================================================================
# 5. Transpile to IBM Heron r3 native gate set
# ===========================================================================
print("\n[5] Transpiling to IBM Heron r3 (FakeMarrakesh)...", flush=True)

try:
    from qiskit_ibm_runtime.fake_provider import FakeMarrakesh

    backend = FakeMarrakesh()
    backend_name = "FakeMarrakesh (ibm_marrakesh proxy)"
    native_gates = backend.operation_names
    print(f"  Backend: {backend_name}")
    print(f"  Native gates: {[g for g in native_gates if g not in ('id', 'reset', 'delay', 'measure', 'barrier')]}")
    print(f"  N physical qubits: {backend.num_qubits}")

except ImportError:
    print("  FakeMarrakesh not available, using generic transpilation")
    backend = None
    backend_name = "generic"

t_start = time.time()

if backend is not None:
    from qiskit.compiler import transpile

    # Transpile at optimization level 3 (highest optimization, slowest but best depth)
    # Use qubit 0..15 mapped to the chain topology
    qc_transpiled = transpile(
        qc_measure,
        backend=backend,
        optimization_level=3,
        seed_transpiler=42,
    )
    t_transpile = time.time() - t_start
    print(f"  Transpile time: {t_transpile:.1f}s")

    # Count gates in transpiled circuit
    gate_counts = qc_transpiled.count_ops()
    print(f"\n  Transpiled circuit stats:")
    for gate_name, count in sorted(gate_counts.items()):
        print(f"    {gate_name}: {count}")

    cx_count = gate_counts.get("cx", 0) + gate_counts.get("ecr", 0) + gate_counts.get("cz", 0)
    # Heron r3 uses ECR (echoed cross-resonance) as the native 2-qubit gate
    ecr_count = gate_counts.get("ecr", 0)
    total_2q = sum(
        cnt for g, cnt in gate_counts.items()
        if g not in ("rz", "x", "sx", "id", "reset", "delay", "measure", "barrier", "h", "ry", "rx", "s", "sdg", "t", "tdg")
    )
    depth = qc_transpiled.depth()

    print(f"\n  Total 2-qubit gates: {total_2q}")
    print(f"  Circuit depth (after transpile): {depth}")

    # Error budget estimate (IBM Heron r3 specs)
    # ECR gate fidelity on Heron r3: ~99.5-99.8% typical (conservative: 99.5%)
    ecr_fidelity = 0.995
    # SPAM (state prep + measurement) per qubit: ~99.5% typical on Heron r3
    spam_per_qubit = 0.995

    error_from_2q = 1.0 - ecr_fidelity ** total_2q
    error_from_spam = 1.0 - spam_per_qubit ** N_QUBITS

    print(f"\n  Error budget estimate (IBM Heron r3):")
    print(f"    2-qubit gate fidelity assumed: {ecr_fidelity*100:.1f}%")
    print(f"    SPAM fidelity per qubit assumed: {spam_per_qubit*100:.1f}%")
    print(f"    Accumulated error from 2q gates: {error_from_2q*100:.1f}%")
    print(f"    Accumulated SPAM error (16q): {error_from_spam*100:.1f}%")
    print(f"    Total estimated error floor: {(1-(1-error_from_2q)*(1-error_from_spam))*100:.1f}%")

    # Runtime estimate
    # IBM Heron r3 speed: ~1-2 ms/shot for typical circuits
    shot_time_ms = 1.5  # conservative estimate
    runtime_s = N_SHOTS * shot_time_ms / 1000.0
    print(f"\n  Runtime estimate ({N_SHOTS:,} shots @ {shot_time_ms}ms/shot):")
    print(f"    Estimated execution time: {runtime_s:.0f}s = {runtime_s/60:.1f} min")
    print(f"    IBM free tier budget: 10 min/month")
    print(f"    Budget usage: {runtime_s/60/10*100:.1f}%")

else:
    qc_transpiled = qc_measure
    total_2q = 0
    depth = qc_transpiled.depth()
    error_from_2q = None
    error_from_spam = None
    print("  Transpilation skipped (no backend available)")

# ===========================================================================
# 6. Hardware feasibility assessment
# ===========================================================================
print("\n[6] Hardware feasibility assessment...", flush=True)

# Check against our standard hardware feasibility rules (from MEMORY)
# Target: < 10% accumulated error for PoC, < 5% preferred
feasibility_verdict = "UNKNOWN"
if error_from_2q is not None:
    total_err = 1 - (1 - error_from_2q) * (1 - error_from_spam)
    if total_err < 0.05:
        feasibility_verdict = "PREFERRED (< 5% error)"
    elif total_err < 0.10:
        feasibility_verdict = "FEASIBLE (< 10% error)"
    elif total_err < 0.20:
        feasibility_verdict = "MARGINAL (10-20% error)"
    else:
        feasibility_verdict = "CHALLENGING (> 20% error)"

    print(f"  Total estimated error: {total_err*100:.1f}%")
    print(f"  Verdict: {feasibility_verdict}")
else:
    print("  Cannot assess without transpilation stats")

# For reference, our helios feasibility rule from MEMORY:
# 16q 3L MERA: 56 CNOTs on Helios = 0.56% error -- excellent baseline
# 16q 3L MERA on IBM Heron: depends on routing overhead
print(f"\n  Note: Helios (logical gate error 1e-4) would give:")
helios_err = 1 - (1 - 1e-4) ** total_2q if total_2q > 0 else None
if helios_err is not None:
    print(f"    Same circuit: {helios_err*100:.2f}% error (vs IBM: {error_from_2q*100:.1f}%)")
    print(f"    Helios is {error_from_2q/helios_err:.0f}x better for this experiment")

# ===========================================================================
# 7. Save results and circuit
# ===========================================================================
print("\n[7] Saving results...", flush=True)

import os
out_dir = "D:/quantum-worldline/research/data/simulations"

# Save transpiled circuit as QASM
qasm_path = os.path.join(out_dir, "ibm_heron_mera_16q_transpiled.qasm")
try:
    from qiskit.qasm2 import dumps as qasm2_dumps
    qasm_str = qasm2_dumps(qc_transpiled)
    with open(qasm_path, "w") as f:
        f.write(qasm_str)
    print(f"  Transpiled circuit QASM saved: {qasm_path}")
except Exception as e:
    print(f"  QASM export failed: {e} (Qiskit 2.x may require qasm3)")
    try:
        from qiskit.qasm3 import dumps as qasm3_dumps
        qasm_path = qasm_path.replace(".qasm", ".qasm3")
        qasm_str = qasm3_dumps(qc_transpiled)
        with open(qasm_path, "w") as f:
            f.write(qasm_str)
        print(f"  Transpiled circuit QASM3 saved: {qasm_path}")
    except Exception as e2:
        print(f"  QASM3 export also failed: {e2}")
        qasm_path = None

# Save results JSON
results = {
    "sim_id": "SIM-2026-011",
    "date": "2026-03-18",
    "description": "16q analytical MERA circuit for IBM Heron r3 -- ZZ correlator measurement",
    "hypothesis": "HYP-2026-002",
    "hardware_target": "ibm_marrakesh (Heron r3) or ibm_fez (Heron r3)",
    "status": "DESIGNED -- awaiting user approval before submission",
    "circuit": {
        "qubits": int(N_QUBITS),
        "n_layers": int(N_LAYERS),
        "gates_before_transpile": int(len(gate_log)),
        "gate_type": "UnitaryGate (u + w from Evenbly-White 2016)",
        "tensor_source": "Evenbly & White 2016, Eq S3-S4 (ANALYTICAL, not VQE)",
        "shots": int(N_SHOTS),
    },
    "transpile": {
        "backend": backend_name,
        "optimization_level": 3,
        "gate_counts": {k: int(v) for k, v in gate_counts.items()} if backend is not None else {},
        "total_2q_gates": int(total_2q) if total_2q else None,
        "depth_after_transpile": int(depth),
    },
    "error_budget": {
        "ecr_fidelity_assumed": float(ecr_fidelity) if backend is not None else None,
        "spam_fidelity_per_qubit": float(spam_per_qubit) if backend is not None else None,
        "accumulated_2q_error_pct": float(error_from_2q * 100) if error_from_2q is not None else None,
        "accumulated_spam_error_pct": float(error_from_spam * 100) if error_from_spam is not None else None,
        "total_estimated_error_pct": float(total_err * 100) if error_from_2q is not None else None,
        "feasibility_verdict": feasibility_verdict,
        "helios_comparison_error_pct": float(helios_err * 100) if helios_err else None,
    },
    "runtime_estimate": {
        "shots": int(N_SHOTS),
        "shot_time_ms": float(shot_time_ms) if backend is not None else None,
        "total_runtime_s": float(runtime_s) if backend is not None else None,
        "total_runtime_min": float(runtime_s / 60) if backend is not None else None,
        "free_tier_budget_min": 10.0,
        "budget_usage_pct": float(runtime_s / 60 / 10 * 100) if backend is not None else None,
    },
    "classical_verification": {
        "zz_correlators": {str(k): float(v) for k, v in corrs.items()},
        "power_law_fit_alpha": float(alpha_fit) if "alpha_fit" in dir() else None,
        "cft_prediction_alpha": 0.25,
    },
    "measurement_strategy": "All-Z measurement: single circuit covers all ZZ correlators (commuting observables)",
    "notes": [
        "u and w matrices are REAL -- cheaper decomposition than complex unitaries",
        "Brick-wall MERA: N_LAYERS repetitions of (w on even pairs) + (u on odd pairs)",
        "Starting from |0>^16 -- scale-invariant MERA approximates CFT vacuum",
        "DO NOT SUBMIT without user approval",
        "Qubit ordering: physics (big-endian) converted to Qiskit (little-endian) via SWAP transform",
    ],
    "next_steps": [
        "1. User reviews this report and approves submission",
        "2. Load IBM credentials: QiskitRuntimeService(channel='ibm_quantum_platform', instance='Worldline work')",
        "3. Select backend: ibm_fez or ibm_marrakesh (both Heron r3)",
        "4. Submit with Sampler primitive, N_SHOTS=10000",
        "5. Post-process bitstrings to extract ZZ correlators",
        "6. Plot C(r) vs r and fit power-law alpha",
        "7. Compare to simulator prediction and CFT prediction (alpha=0.25)",
    ],
}

results_path = os.path.join(out_dir, "SIM-2026-011.json")
with open(results_path, "w") as f:
    json.dump(results, f, indent=2)
print(f"  Results JSON saved: {results_path}")

# ===========================================================================
# 8. Print circuit diagram (first layer only -- full circuit too large to print)
# ===========================================================================
print("\n[8] Circuit structure summary...", flush=True)

qc_preview, _ = build_mera_circuit(N_QUBITS, 1, include_barriers=False)
print(f"  First layer of MERA circuit (Layer 1 of {N_LAYERS}):")
print(f"    {N_QUBITS // 2} w-gates on even pairs: " +
      ", ".join(f"({i},{i+1})" for i in range(0, N_QUBITS, 2)))
print(f"    {N_QUBITS // 2 - 1} u-gates on odd pairs: " +
      ", ".join(f"({i},{i+1})" for i in range(1, N_QUBITS - 1, 2)))
print(f"  Repeated for {N_LAYERS} layers total.")
print(f"  Then: measure all qubits in Z basis.")

# ===========================================================================
# Summary
# ===========================================================================
print("\n" + "=" * 70)
print("SUMMARY")
print("=" * 70)
print(f"  Circuit: {N_QUBITS}q analytical MERA, {N_LAYERS} layers")
print(f"  Gate count (before transpile): {len(gate_log)} blocks")
if backend is not None:
    print(f"  Gate count (after transpile to Heron r3): {total_2q} 2-qubit gates, depth={depth}")
    print(f"  Estimated hardware error: {total_err*100:.1f}%")
    print(f"  Feasibility: {feasibility_verdict}")
    print(f"  Estimated runtime: {runtime_s:.0f}s ({runtime_s/60:.1f} min) -- within 10 min free tier")
if corrs:
    print(f"  Simulator ZZ correlators: C(1)={corrs.get(1,0):.4f} -> C(8)={corrs.get(8,0):.4f}")
if "alpha_fit" in dir():
    print(f"  Power-law fit alpha = {alpha_fit:.4f} (CFT: 0.250)")
print(f"\n  Files saved:")
print(f"    {results_path}")
if qasm_path:
    print(f"    {qasm_path}")
print(f"\n  STATUS: DESIGNED. Awaiting user approval before hardware submission.")
print(f"  To submit: set hardware_target to 'ibm_marrakesh' or 'ibm_fez' and")
print(f"  run the submission section below (commented out).")
print("=" * 70)


# ===========================================================================
# SUBMISSION SECTION (COMMENTED OUT -- do not run without user approval)
# ===========================================================================
"""
HARDWARE SUBMISSION CODE (requires user approval)
Uncomment ONLY after user gives explicit approval to submit.

from qiskit_ibm_runtime import QiskitRuntimeService, SamplerV2 as Sampler
from qiskit_ibm_runtime import Options
from qiskit.compiler import transpile

# Load IBM credentials
service = QiskitRuntimeService(channel="ibm_quantum_platform", instance="Worldline work")
backend = service.backend("ibm_marrakesh")  # or ibm_fez

# Transpile for real hardware
qc_hw = transpile(qc_measure, backend=backend, optimization_level=3, seed_transpiler=42)

# Run with Sampler primitive
with Sampler(backend) as sampler:
    job = sampler.run([qc_hw], shots=N_SHOTS)
    print(f"Job submitted: {job.job_id()}")
    result = job.result()

# Post-process: extract ZZ correlators from bitstrings
counts = result[0].data.c.get_counts()
anchor = 0
zz_hardware = {}
total_shots = sum(counts.values())
for dr in range(1, 9):
    j = anchor + dr
    zz_sum = 0.0
    for bitstring, count in counts.items():
        # Qiskit bitstring is little-endian: bitstring[0] = qubit N-1
        bits = [int(b) for b in reversed(bitstring)]  # convert to big-endian
        sign = 1 if bits[anchor] == bits[j] else -1
        zz_sum += sign * count
    zz_hardware[dr] = zz_sum / total_shots

print("Hardware ZZ correlators:")
for dr, c in zz_hardware.items():
    print(f"  C(0,{dr}) = {c:.6f}")
"""
