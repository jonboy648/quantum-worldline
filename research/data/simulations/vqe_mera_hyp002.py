"""
VQE Optimization of MERA Circuit — HYP-2026-002
================================================
Qiskit Builder specialist output for Computation Lead.

Task: Variationally optimize 16-qubit binary MERA (3-layer, 146 params)
      to minimize 1D transverse-field Ising energy at criticality (J=h=1).

      H = -sum_i Z_i Z_{i+1} - sum_i X_i   (open boundary, 16 sites)

Optimizer:  scipy COBYLA (gradient-free, robust for noisy energy landscapes)
Fallback:   L-BFGS-B with finite-difference gradients

After convergence, measures holographic force profile V(delta_rho)
using Ry hologrons (confirmed non-commuting with ZZ — see SIM-2026-001 FIND-001).

Author: qiskit-builder (Computation Lead dispatch)
Date:   2026-03-10
SIM:    SIM-2026-002
"""

import numpy as np
import json
import time
from copy import deepcopy
from scipy.optimize import minimize
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector

# ─── Configuration ────────────────────────────────────────────────────────────
N_QUBITS = 16
N_LAYERS = 3
J = 1.0
H_FIELD = 1.0
L_ADS   = 1.0 / np.log(2)   # 1.4427...
C1_PAPER = 0.080
C2_PAPER = 13.6

DELTA_RHO_VALUES = list(range(1, 9))
HOLOGRON_ANGLE   = np.pi / 3    # Ry angle for hologron excitation

# VQE convergence settings
VQE_MAX_ITER    = 800
VQE_TOL         = 1e-5          # function tolerance for COBYLA
VQE_ENERGY_TOL  = 0.01         # 1% of |E0| for convergence check

np.random.seed(42)


# ─── Parameter counting ────────────────────────────────────────────────────────
def count_mera_params(n_qubits: int, n_layers: int) -> int:
    total = 0
    for layer in range(n_layers):
        n_sites = n_qubits // (2 ** layer)
        n_pairs = n_sites // 2
        total += n_pairs * 6   # disentanglers: 6 params each
        total += n_pairs * 4   # isometries:    4 params each
    total += 6                 # top tensor
    return total


# ─── Circuit builders ─────────────────────────────────────────────────────────
def add_disentangler(qc, q0, q1, params, offset):
    qc.ry(params[offset + 0], q0)
    qc.rz(params[offset + 1], q0)
    qc.ry(params[offset + 2], q1)
    qc.rz(params[offset + 3], q1)
    qc.cx(q0, q1)
    qc.ry(params[offset + 4], q0)
    qc.ry(params[offset + 5], q1)
    return offset + 6


def add_isometry(qc, q0, q1, params, offset):
    qc.ry(params[offset + 0], q0)
    qc.ry(params[offset + 1], q1)
    qc.cx(q0, q1)
    qc.ry(params[offset + 2], q0)
    qc.rz(params[offset + 3], q1)
    return offset + 4


def build_mera_vacuum(param_values: np.ndarray):
    """
    Build 16-qubit binary MERA circuit and bind parameters.
    Returns bound QuantumCircuit.
    """
    n_params = len(param_values)
    params   = ParameterVector('θ', n_params)
    qc       = QuantumCircuit(N_QUBITS, name='MERA_vacuum')

    # Initialization: Hadamard on all qubits
    for i in range(N_QUBITS):
        qc.h(i)

    param_offset  = 0
    active_qubits = list(range(N_QUBITS))

    for layer in range(N_LAYERS):
        n_active = len(active_qubits)
        if n_active < 2:
            break

        # Disentanglers
        for k in range(0, n_active - 1, 2):
            q0 = active_qubits[k]
            q1 = active_qubits[k + 1]
            param_offset = add_disentangler(qc, q0, q1, params, param_offset)

        # Isometries
        next_active = []
        for k in range(0, n_active - 1, 2):
            q0 = active_qubits[k]
            q1 = active_qubits[k + 1]
            param_offset = add_isometry(qc, q0, q1, params, param_offset)
            next_active.append(q0)

        if n_active % 2 == 1:
            next_active.append(active_qubits[-1])
        active_qubits = next_active

    # Top tensor
    if len(active_qubits) >= 2 and param_offset + 6 <= n_params:
        q0, q1 = active_qubits[0], active_qubits[1]
        param_offset = add_disentangler(qc, q0, q1, params, param_offset)

    binding = {params[i]: float(param_values[i]) for i in range(n_params)}
    return qc.assign_parameters(binding)


# ─── Ising Hamiltonian ─────────────────────────────────────────────────────────
def build_ising_hamiltonian(n: int, j: float, h: float) -> SparsePauliOp:
    """
    H = -J * sum_{i=0}^{n-2} Z_i Z_{i+1}  -  h * sum_{i=0}^{n-1} X_i
    Open boundary conditions.
    Qiskit convention: Pauli string index 0 = rightmost qubit.
    """
    terms = []
    coeffs = []

    # ZZ terms
    for i in range(n - 1):
        s = ['I'] * n
        s[i]   = 'Z'
        s[i+1] = 'Z'
        terms.append(''.join(reversed(s)))
        coeffs.append(-j)

    # X terms
    for i in range(n):
        s = ['I'] * n
        s[i] = 'X'
        terms.append(''.join(reversed(s)))
        coeffs.append(-h)

    return SparsePauliOp(terms, coeffs=coeffs)


HAMILTONIAN = build_ising_hamiltonian(N_QUBITS, J, H_FIELD)

# Exact ground state energy via ED for reference
def exact_ground_energy(n, j, h):
    """
    Exact ground energy of open-boundary TFIM via free-fermion solution.
    E0 = -sum_k epsilon_k where epsilon_k = sqrt((j*cos(k) + h)^2 + (j*sin(k))^2)
    Modes: k = pi*(m+1/2)/n for m = 0,...,n-1 (open BC approximate)
    """
    # Use explicit matrix diagonalization for small N
    from scipy.sparse import lil_matrix
    from scipy.sparse.linalg import eigsh

    dim = 2 ** n
    # Build sparse Hamiltonian
    H = lil_matrix((dim, dim), dtype=np.float64)

    # ZZ terms
    for i in range(n - 1):
        for state in range(dim):
            si = (state >> i) & 1
            sj = (state >> (i+1)) & 1
            sign = 1 if si == sj else -1
            H[state, state] += -j * sign

    # X terms
    for i in range(n):
        for state in range(dim):
            flipped = state ^ (1 << i)
            H[state, flipped] += -h

    H = H.tocsr()
    vals, _ = eigsh(H, k=1, which='SA')
    return float(vals[0])


# ─── VQE energy function ───────────────────────────────────────────────────────
iteration_count  = [0]
energy_history   = []
time_history     = []
t_vqe_start      = [0.0]

def energy_function(param_values: np.ndarray) -> float:
    """Energy expectation value <psi(theta)|H|psi(theta)> on statevector."""
    qc = build_mera_vacuum(param_values)
    sv = Statevector(qc)
    E  = sv.expectation_value(HAMILTONIAN).real
    iteration_count[0] += 1

    elapsed = time.time() - t_vqe_start[0]
    energy_history.append(float(E))
    time_history.append(elapsed)

    if iteration_count[0] % 50 == 0:
        print(f"  iter {iteration_count[0]:4d}  E = {E:+.6f}  t = {elapsed:.1f}s")

    return float(E)


# ─── Initial parameters ────────────────────────────────────────────────────────
def get_initial_params(n_params: int) -> np.ndarray:
    """
    Analytically motivated starting point for critical Ising MERA.

    For the critical TFIM ground state, the MERA tensors at criticality
    approximate perfect tensors (maximally entangling). The optimal
    single-qubit rotation angles are near pi/4 (45 deg).

    We interleave:
      - Ry: pi/4 (approximate pi/2 disentangler baseline / 2)
      - Rz: pi/2 (full phase rotation)
    with small perturbations drawn from N(0, 0.1) to break symmetry
    and avoid saddle points.
    """
    rng    = np.random.default_rng(seed=0)
    params = np.zeros(n_params)
    idx    = 0

    for layer in range(N_LAYERS):
        n_sites = N_QUBITS // (2 ** layer)
        n_pairs = n_sites // 2

        # Disentanglers
        for _ in range(n_pairs):
            base = np.array([np.pi/4, np.pi/2, np.pi/4, np.pi/2, np.pi/4, np.pi/4])
            params[idx:idx+6] = base + rng.normal(0, 0.08, 6)
            idx += 6

        # Isometries
        for _ in range(n_pairs):
            base = np.array([np.pi/4, np.pi/8, np.pi/4, np.pi/6])
            params[idx:idx+4] = base + rng.normal(0, 0.08, 4)
            idx += 4

    # Top tensor
    if idx + 6 <= n_params:
        base = np.array([np.pi/3, np.pi/4, np.pi/3, np.pi/4, np.pi/4, np.pi/3])
        params[idx:idx+6] = base + rng.normal(0, 0.08, 6)
        idx += 6

    return params


# ─── Correlator measurement ────────────────────────────────────────────────────
def measure_zz_correlator(qc: QuantumCircuit, i: int, j: int):
    sv  = Statevector(qc)

    zi_s  = ['I'] * N_QUBITS; zi_s[i]  = 'Z'
    zj_s  = ['I'] * N_QUBITS; zj_s[j]  = 'Z'
    zij_s = ['I'] * N_QUBITS; zij_s[i] = 'Z'; zij_s[j] = 'Z'

    zi_op  = SparsePauliOp(''.join(reversed(zi_s)))
    zj_op  = SparsePauliOp(''.join(reversed(zj_s)))
    zij_op = SparsePauliOp(''.join(reversed(zij_s)))

    zi  = sv.expectation_value(zi_op).real
    zj  = sv.expectation_value(zj_op).real
    zij = sv.expectation_value(zij_op).real
    return zij - zi * zj


def compute_force_profile(vacuum_qc: QuantumCircuit, anchor: int):
    """
    Sweep delta_rho and compute V(delta_rho) = C(two hologrons) - C(vacuum).
    Uses Ry hologrons (non-commuting with ZZ — confirmed SIM-2026-001).
    """
    Vs, C_vacs, C_twos, separations = [], [], [], []
    for dr in DELTA_RHO_VALUES:
        j_site = anchor + dr
        if j_site >= N_QUBITS:
            continue

        C_vac = measure_zz_correlator(vacuum_qc, anchor, j_site)

        two_qc = deepcopy(vacuum_qc)
        two_qc.ry(HOLOGRON_ANGLE, anchor)
        two_qc.ry(HOLOGRON_ANGLE, j_site)

        C_two = measure_zz_correlator(two_qc, anchor, j_site)

        V = C_two - C_vac
        Vs.append(float(V))
        C_vacs.append(float(C_vac))
        C_twos.append(float(C_two))
        separations.append(dr)
        print(f"  dr={dr}: V={V:+.6f}  C_vac={C_vac:.6f}  C_two={C_two:.6f}")

    return separations, Vs, C_vacs, C_twos


# ─── Fit holographic force model ───────────────────────────────────────────────
def fit_force_profile(separations, Vs):
    from scipy.optimize import curve_fit

    def model(x, C1, C2, xi):
        return C1 - C2 * np.exp(-np.array(x, dtype=float) / xi)

    x = np.array(separations, dtype=float)
    y = np.array(Vs, dtype=float)

    try:
        popt, pcov = curve_fit(model, x, y,
                               p0=[C1_PAPER, C2_PAPER, L_ADS],
                               maxfev=10000,
                               bounds=([-2, -100, 0.1], [2, 100, 10]))
        perr = np.sqrt(np.diag(pcov))
        return {
            "success": True,
            "C1": float(popt[0]), "C2": float(popt[1]), "xi": float(popt[2]),
            "C1_err": float(perr[0]), "C2_err": float(perr[1]), "xi_err": float(perr[2]),
        }
    except Exception as e:
        print(f"  Fit failed: {e}")
        return {"success": False, "C1": None, "C2": None, "xi": None}


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 65)
    print("VQE MERA Optimization — HYP-2026-002  (SIM-2026-002)")
    print("=" * 65)

    t_total = time.time()

    # --- Exact ground energy (reference) ------------------------------------
    print("\n[1/4] Computing exact ground energy via ED...")
    t0 = time.time()
    E0_exact = exact_ground_energy(N_QUBITS, J, H_FIELD)
    print(f"  Exact E0 ({N_QUBITS} sites, OBC) = {E0_exact:.6f}  [{time.time()-t0:.1f}s]")
    target_energy = E0_exact * 1.01   # 1% threshold

    # --- VQE optimization ---------------------------------------------------
    n_params     = count_mera_params(N_QUBITS, N_LAYERS)
    theta0       = get_initial_params(n_params)
    E_init       = energy_function(theta0.copy())
    print(f"\n[2/4] VQE optimization (COBYLA, max {VQE_MAX_ITER} iter)")
    print(f"  Initial energy = {E_init:+.6f}  (target: {target_energy:+.6f})")
    print(f"  n_params = {n_params}")
    print()

    iteration_count[0] = 0
    energy_history.clear()
    time_history.clear()
    t_vqe_start[0] = time.time()

    result = minimize(
        energy_function,
        theta0,
        method='COBYLA',
        options={
            'maxiter': VQE_MAX_ITER,
            'rhobeg': 0.3,      # initial trust-region radius (larger = more exploration)
            'catol':  VQE_TOL,
        }
    )

    t_vqe = time.time() - t_vqe_start[0]
    theta_opt = result.x
    E_opt     = result.fun

    converged = E_opt <= target_energy
    pct_error = abs(E_opt - E0_exact) / abs(E0_exact) * 100

    print(f"\n  VQE complete in {t_vqe:.1f}s ({iteration_count[0]} function evals)")
    print(f"  E_opt          = {E_opt:+.6f}")
    print(f"  E0_exact       = {E0_exact:+.6f}")
    print(f"  Error          = {pct_error:.2f}%")
    print(f"  Converged <1%  = {converged}")

    # --- Force profile with optimized params --------------------------------
    print(f"\n[3/4] Measuring holographic force profile V(delta_rho)...")
    vacuum_qc = build_mera_vacuum(theta_opt)
    anchor    = N_QUBITS // 4   # site 4

    separations, Vs, C_vacs, C_twos = compute_force_profile(vacuum_qc, anchor)

    # Analytical prediction
    def analytical(dr):
        return C1_PAPER - C2_PAPER * np.exp(-dr / L_ADS)
    V_analytical = [analytical(dr) for dr in separations]

    # Fit
    fit = fit_force_profile(separations, Vs)
    print(f"\n  Fit: C1={fit['C1']}, C2={fit['C2']}, xi={fit['xi']}")
    print(f"  Paper: C1={C1_PAPER}, C2={C2_PAPER}, l_AdS={L_ADS:.4f}")

    # --- Save energy history -------------------------------------------------
    print(f"\n[4/4] Saving results...")
    t_elapsed = time.time() - t_total

    structured = {
        "id":             "SIM-2026-002",
        "description":   "VQE optimization of 16-qubit binary MERA to critical Ising ground state. "
                          "Follows SIM-2026-001. Parameters optimized via COBYLA. "
                          "Holographic force profile measured with Ry hologrons post-optimization.",
        "type":          "vqe_optimization",
        "date":          "2026-03-10",
        "hypothesis_id": "HYP-2026-002",
        "paper_ref":     "PAPER-2026-003",
        "circuit": {
            "qubits":       N_QUBITS,
            "layers":       N_LAYERS,
            "n_params":     n_params,
            "architecture": "binary_MERA_disentanglers_isometries",
            "hologron_gate":  "Ry",
            "hologron_angle_rad": float(HOLOGRON_ANGLE),
        },
        "vqe": {
            "optimizer":         "COBYLA",
            "max_iter":          VQE_MAX_ITER,
            "n_function_evals":  iteration_count[0],
            "elapsed_seconds":   round(t_vqe, 2),
            "E_initial":         float(E_init),
            "E_optimized":       float(E_opt),
            "E0_exact":          float(E0_exact),
            "pct_error":         round(pct_error, 4),
            "converged_1pct":    converged,
            "energy_history":    energy_history,
            "time_history":      [round(t, 3) for t in time_history],
            "theta_optimized":   theta_opt.tolist(),
        },
        "force_profile": {
            "delta_rho":     separations,
            "V_quantum":     Vs,
            "V_analytical":  V_analytical,
            "C_vac":         C_vacs,
            "C_two":         C_twos,
            "anchor_site":   anchor,
        },
        "fit": fit,
        "comparison": {
            "paper_C1":    C1_PAPER,
            "paper_C2":    C2_PAPER,
            "paper_l_AdS": L_ADS,
            "fitted_C1":   fit.get("C1"),
            "fitted_C2":   fit.get("C2"),
            "fitted_xi":   fit.get("xi"),
        },
        "hardware_target": "simulator_qiskit_aer_statevector",
        "total_elapsed_seconds": round(t_elapsed, 2),
    }

    out_path = "D:/quantum-worldline/research/data/simulations/SIM-2026-002.json"
    with open(out_path, 'w') as f:
        json.dump(structured, f, indent=2)
    print(f"  Saved: {out_path}")

    # Also save optimized params as numpy array
    np_path = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026002.npy"
    np.save(np_path, theta_opt)
    print(f"  Saved theta_opt: {np_path}")

    print(f"\n  Total runtime: {t_elapsed:.1f}s")
    print("=" * 65)
    return structured


if __name__ == "__main__":
    result = main()
    print("\n--- STRUCTURED OUTPUT (summary) ---")
    summary = {k: v for k, v in result.items() if k not in ("vqe",)}
    summary["vqe_summary"] = {
        k: v for k, v in result["vqe"].items()
        if k not in ("energy_history", "time_history", "theta_optimized")
    }
    print(json.dumps(summary, indent=2))
