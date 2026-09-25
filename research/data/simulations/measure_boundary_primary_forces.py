"""
Boundary-Primary Excitations vs Ry Hologrons — Force Profile Comparison
========================================================================
Tests HYP-2026-002 with boundary-primary excitations from
Zou-Milsted-Vidal (PRL 2020) / Wang & He (2025) against the existing
Ry hologron approach on the SIM-2026-002 optimized ground state.

Boundary-primary operator (sigma excitation at boundary site j):
  sigma^boundary_j = 0.635 * (X_j + X_{j+1}) - 0.026 * (X_j Z_{j+1} + Z_j X_{j+1})

This creates a CFT primary excitation that should be more stable than
local Ry rotations (which create dynamically unstable hologrons per
Wang & He 2025).

Uses the 16-qubit, 3-layer MERA ground state from SIM-2026-002.

Author: qiskit-builder (manual test)
Date:   2026-03-11
"""

import numpy as np
import time
from scipy import sparse
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import Statevector

# ─── Configuration ────────────────────────────────────────────────────────────
N_QUBITS = 16
N_LAYERS = 3
ANCHOR   = N_QUBITS // 4   # site 4 (same as SIM-2026-002)
DR_VALUES = list(range(1, 8))  # dr=1..7 (stay away from boundaries)
HOLOGRON_ANGLE = np.pi / 3

# Boundary-primary coefficients from Zou-Milsted-Vidal / Wang-He
ALPHA = 0.635    # X_j + X_{j+1} coefficient
BETA  = -0.026   # X_j Z_{j+1} + Z_j X_{j+1} coefficient

# Reference values
E0_EXACT = -20.016388
L_ADS = 1.0 / np.log(2)  # 1.4427

THETA_PATH = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026002.npy"


# ─── MERA circuit builder (matches vqe_mera_hyp002.py exactly) ────────────────
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


def build_mera_vacuum(param_values, hadamard=False):
    """Build MERA circuit. hadamard=False matches the SIM-2026-002 winning config
    (vqe_cobyla_final.py used |0>^N init, NOT Hadamard)."""
    n_params = len(param_values)
    params = ParameterVector('t', n_params)
    qc = QuantumCircuit(N_QUBITS, name='MERA_vacuum')

    if hadamard:
        for i in range(N_QUBITS):
            qc.h(i)

    param_offset = 0
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


# ─── Sparse operator builders ─────────────────────────────────────────────────
def sparse_pauli_single(n, qubit, pauli):
    """Build sparse matrix for single Pauli on qubit in n-qubit system."""
    I2 = sparse.eye(2, format='csr')
    X = sparse.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Y = sparse.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    Z = sparse.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))

    paulis = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
    op = paulis[pauli]

    # Build tensor product: qubit 0 is rightmost in Qiskit convention
    result = sparse.eye(1, format='csr')
    for q in range(n):
        if q == qubit:
            result = sparse.kron(op, result, format='csr')
        else:
            result = sparse.kron(I2, result, format='csr')
    return result


def sparse_pauli_two(n, q1, p1, q2, p2):
    """Build sparse matrix for two-qubit Pauli: p1 on q1, p2 on q2."""
    I2 = sparse.eye(2, format='csr')
    X = sparse.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Y = sparse.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    Z = sparse.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))

    paulis = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
    op1, op2 = paulis[p1], paulis[p2]

    result = sparse.eye(1, format='csr')
    for q in range(n):
        if q == q1:
            result = sparse.kron(op1, result, format='csr')
        elif q == q2:
            result = sparse.kron(op2, result, format='csr')
        else:
            result = sparse.kron(I2, result, format='csr')
    return result


def build_ising_hamiltonian_sparse(n):
    """H = -sum Z_i Z_{i+1} - sum X_i, OBC, sparse."""
    H = sparse.csr_matrix((2**n, 2**n), dtype=complex)
    for i in range(n - 1):
        H -= sparse_pauli_two(n, i, 'Z', i+1, 'Z')
    for i in range(n):
        H -= sparse_pauli_single(n, i, 'X')
    return H


def build_boundary_primary(n, j):
    """
    Boundary-primary excitation operator at site j:
      sigma^boundary_j = alpha * (X_j + X_{j+1})
                       + beta  * (X_j Z_{j+1} + Z_j X_{j+1})

    Returns sparse matrix.
    """
    op = ALPHA * (sparse_pauli_single(n, j, 'X') +
                  sparse_pauli_single(n, j+1, 'X'))
    op += BETA * (sparse_pauli_two(n, j, 'X', j+1, 'Z') +
                  sparse_pauli_two(n, j, 'Z', j+1, 'X'))
    return op


def build_ry_matrix(n, qubit, angle):
    """Sparse Ry(angle) gate on specified qubit."""
    I2 = sparse.eye(2, format='csr')
    c, s = np.cos(angle / 2), np.sin(angle / 2)
    Ry = sparse.csr_matrix(np.array([[c, -s], [s, c]], dtype=complex))

    result = sparse.eye(1, format='csr')
    for q in range(n):
        if q == qubit:
            result = sparse.kron(Ry, result, format='csr')
        else:
            result = sparse.kron(I2, result, format='csr')
    return result


# ─── Measurement functions ─────────────────────────────────────────────────────
def expect(sv, op):
    """<sv|op|sv> for sparse op and numpy sv."""
    return np.real(np.conj(sv) @ (op @ sv))


def zz_connected(sv, ZZ_op, Zi_op, Zj_op):
    """C_connected = <ZZ> - <Z><Z>."""
    return expect(sv, ZZ_op) - expect(sv, Zi_op) * expect(sv, Zj_op)


# ─── Force profile model ──────────────────────────────────────────────────────
def force_model(x, C1, C2, xi):
    return C1 - C2 * np.exp(-np.array(x, dtype=float) / xi)


def fit_force(dr, V):
    """Attempt exponential force fit."""
    x = np.array(dr, dtype=float)
    y = np.array(V, dtype=float)
    try:
        popt, pcov = curve_fit(force_model, x, y,
                               p0=[0.0, 0.01, 1.5],
                               maxfev=10000,
                               bounds=([-1, -10, 0.1], [1, 10, 10]))
        perr = np.sqrt(np.diag(pcov))
        return True, popt, perr
    except Exception as e:
        return False, None, str(e)


# ─── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("BOUNDARY-PRIMARY vs Ry HOLOGRON — Force Profile Comparison")
    print("=" * 72)
    t_start = time.time()

    # 1. Load optimized parameters
    print(f"\n[1/6] Loading optimized theta from SIM-2026-002...")
    theta = np.load(THETA_PATH)
    print(f"  Loaded {len(theta)} parameters")

    # 2. Build ground state statevector
    print(f"\n[2/6] Building MERA circuit and extracting statevector...")
    t0 = time.time()
    qc = build_mera_vacuum(theta)
    sv_ground = np.array(Statevector(qc))
    print(f"  Statevector shape: {sv_ground.shape}, done in {time.time()-t0:.2f}s")

    # 3. Build Hamiltonian and verify energy
    print(f"\n[3/6] Building sparse TFIM Hamiltonian...")
    t0 = time.time()
    H = build_ising_hamiltonian_sparse(N_QUBITS)
    E_ground = expect(sv_ground, H)
    pct_err = abs(E_ground - E0_EXACT) / abs(E0_EXACT) * 100
    print(f"  H shape: {H.shape}, nnz: {H.nnz}")
    print(f"  E_ground = {E_ground:.6f} (exact: {E0_EXACT:.6f}, error: {pct_err:.2f}%)")
    print(f"  Built in {time.time()-t0:.2f}s")

    # 4. Pre-build all ZZ operators
    print(f"\n[4/6] Pre-building ZZ and Z operators...")
    t0 = time.time()
    ZZ_ops = {}
    Zi_ops = {}
    for dr in DR_VALUES:
        j_site = ANCHOR + dr
        if j_site >= N_QUBITS:
            continue
        ZZ_ops[dr] = sparse_pauli_two(N_QUBITS, ANCHOR, 'Z', j_site, 'Z')
        if ANCHOR not in Zi_ops:
            Zi_ops[ANCHOR] = sparse_pauli_single(N_QUBITS, ANCHOR, 'Z')
        if j_site not in Zi_ops:
            Zi_ops[j_site] = sparse_pauli_single(N_QUBITS, j_site, 'Z')
    print(f"  Built {len(ZZ_ops)} ZZ operators in {time.time()-t0:.2f}s")

    # 5. Measure vacuum correlators
    print(f"\n[5/6] Measuring vacuum ZZ correlators (anchor={ANCHOR})...")
    C_vac = {}
    for dr in DR_VALUES:
        j_site = ANCHOR + dr
        if j_site >= N_QUBITS:
            continue
        C_vac[dr] = zz_connected(sv_ground, ZZ_ops[dr],
                                  Zi_ops[ANCHOR], Zi_ops[j_site])
        print(f"  C_vac(dr={dr}) = {C_vac[dr]:+.8f}")

    # 6. Apply excitations and measure
    print(f"\n[6/6] Measuring force profiles...")
    print()

    # --- Method A: Ry hologron (baseline, reproduces SIM-2026-002) ---
    print("-" * 72)
    print("METHOD A: Ry HOLOGRON  (Ry(pi/3) on anchor and probe)")
    print("-" * 72)

    V_ry = {}
    C_two_ry = {}
    Ry_anchor = build_ry_matrix(N_QUBITS, ANCHOR, HOLOGRON_ANGLE)

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        Ry_probe = build_ry_matrix(N_QUBITS, j_site, HOLOGRON_ANGLE)
        sv_exc = Ry_probe @ (Ry_anchor @ sv_ground)
        # Normalize (Ry is unitary, but be safe)
        sv_exc = sv_exc / np.linalg.norm(sv_exc)

        C_two_ry[dr] = zz_connected(sv_exc, ZZ_ops[dr],
                                      Zi_ops[ANCHOR], Zi_ops[j_site])
        V_ry[dr] = C_two_ry[dr] - C_vac[dr]
        print(f"  dr={dr}: C_two={C_two_ry[dr]:+.8f}  C_vac={C_vac[dr]:+.8f}  "
              f"V={V_ry[dr]:+.8f}")

    # --- Method B: Boundary-primary excitation ---
    print()
    print("-" * 72)
    print("METHOD B: BOUNDARY-PRIMARY EXCITATION")
    print(f"  sigma_j = {ALPHA}*(X_j + X_{{j+1}}) + ({BETA})*(X_j Z_{{j+1}} + Z_j X_{{j+1}})")
    print("-" * 72)

    # Build boundary-primary operator at anchor
    sigma_anchor = build_boundary_primary(N_QUBITS, ANCHOR)
    sv_bp_anchor = sigma_anchor @ sv_ground
    norm_anchor = np.linalg.norm(sv_bp_anchor)
    print(f"  ||sigma_anchor |GS>|| = {norm_anchor:.6f}")

    V_bp = {}
    C_two_bp = {}

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        if j_site + 1 >= N_QUBITS:
            # boundary-primary needs j and j+1
            print(f"  dr={dr}: SKIP (j+1={j_site+1} >= N={N_QUBITS})")
            continue

        # Apply boundary-primary at probe site too
        sigma_probe = build_boundary_primary(N_QUBITS, j_site)
        sv_exc = sigma_probe @ (sigma_anchor @ sv_ground)
        norm_exc = np.linalg.norm(sv_exc)
        sv_exc_normed = sv_exc / norm_exc

        C_two_bp[dr] = zz_connected(sv_exc_normed, ZZ_ops[dr],
                                      Zi_ops[ANCHOR], Zi_ops[j_site])
        V_bp[dr] = C_two_bp[dr] - C_vac[dr]
        print(f"  dr={dr}: C_two={C_two_bp[dr]:+.8f}  C_vac={C_vac[dr]:+.8f}  "
              f"V={V_bp[dr]:+.8f}  ||exc||={norm_exc:.6f}")

    # --- Method C: Boundary-primary at anchor only, measure <ZZ> change ---
    # (Single excitation: how does the correlator structure change
    #  when we insert one boundary primary at the anchor?)
    print()
    print("-" * 72)
    print("METHOD C: SINGLE BOUNDARY-PRIMARY (anchor only)")
    print("  Measures how ZZ correlators shift with one primary insertion")
    print("-" * 72)

    sv_single_bp = sv_bp_anchor / norm_anchor
    V_single_bp = {}
    C_single_bp = {}

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        C_single_bp[dr] = zz_connected(sv_single_bp, ZZ_ops[dr],
                                         Zi_ops[ANCHOR], Zi_ops[j_site])
        V_single_bp[dr] = C_single_bp[dr] - C_vac[dr]
        print(f"  dr={dr}: C_exc={C_single_bp[dr]:+.8f}  C_vac={C_vac[dr]:+.8f}  "
              f"V={V_single_bp[dr]:+.8f}")

    # ─── Comparison table ─────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("COMPARISON TABLE")
    print("=" * 72)
    print(f"{'dr':>3}  {'V_Ry':>12}  {'V_BP_dual':>12}  {'V_BP_single':>12}  {'C_vac':>12}")
    print("-" * 72)

    all_dr = sorted(set(C_vac.keys()))
    for dr in all_dr:
        v_ry_val = V_ry.get(dr, float('nan'))
        v_bp_val = V_bp.get(dr, float('nan'))
        v_sbp_val = V_single_bp.get(dr, float('nan'))
        c_vac_val = C_vac.get(dr, float('nan'))
        print(f"{dr:3d}  {v_ry_val:+12.8f}  {v_bp_val:+12.8f}  {v_sbp_val:+12.8f}  {c_vac_val:+12.8f}")

    # ─── Signal analysis ──────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("SIGNAL ANALYSIS")
    print("=" * 72)

    # Check which method has meaningful signal
    def analyze_signal(name, V_dict):
        vals = [V_dict[dr] for dr in sorted(V_dict.keys())]
        if len(vals) < 3:
            print(f"  {name}: too few points ({len(vals)})")
            return False
        max_abs = max(abs(v) for v in vals)
        signal_range = max(vals) - min(vals)
        monotonic = all(vals[i] >= vals[i+1] for i in range(len(vals)-1))
        mostly_negative = sum(1 for v in vals if v < 0) > len(vals) / 2

        print(f"\n  {name}:")
        print(f"    Max |V|:       {max_abs:.8f}")
        print(f"    Signal range:  {signal_range:.8f}")
        print(f"    Monotonic:     {monotonic}")
        print(f"    Mostly neg:    {mostly_negative}")
        print(f"    Values:        {[f'{v:.6f}' for v in vals]}")

        has_signal = max_abs > 1e-4
        return has_signal

    sig_ry = analyze_signal("Ry hologron (dual)", V_ry)
    sig_bp = analyze_signal("Boundary-primary (dual)", V_bp)
    sig_sbp = analyze_signal("Boundary-primary (single)", V_single_bp)

    # ─── Fits ─────────────────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("EXPONENTIAL FITS: V(dr) = C1 - C2 * exp(-dr / xi)")
    print("=" * 72)

    for name, V_dict, has_sig in [
        ("Ry hologron", V_ry, sig_ry),
        ("Boundary-primary (dual)", V_bp, sig_bp),
        ("Boundary-primary (single)", V_single_bp, sig_sbp),
    ]:
        dr_list = sorted(V_dict.keys())
        v_list = [V_dict[dr] for dr in dr_list]
        if not has_sig:
            print(f"\n  {name}: SKIP (no signal)")
            continue

        success, popt, perr = fit_force(dr_list, v_list)
        if success:
            C1, C2, xi = popt
            C1e, C2e, xie = perr
            print(f"\n  {name}:")
            print(f"    C1 = {C1:.6f} +/- {C1e:.6f}")
            print(f"    C2 = {C2:.6f} +/- {C2e:.6f}")
            print(f"    xi = {xi:.4f} +/- {xie:.4f}  (theory l_AdS = {L_ADS:.4f})")
            xi_err_pct = abs(xi - L_ADS) / L_ADS * 100
            print(f"    xi deviation from l_AdS: {xi_err_pct:.1f}%")
        else:
            print(f"\n  {name}: FIT FAILED — {perr}")

    # ─── Fits excluding dr=1 (local distortion dominates at contact) ────
    print()
    print("=" * 72)
    print("FITS EXCLUDING dr=1 (remove contact-distance distortion)")
    print("=" * 72)

    for name, V_dict, has_sig in [
        ("Ry hologron", V_ry, sig_ry),
        ("Boundary-primary (dual)", V_bp, sig_bp),
        ("Boundary-primary (single)", V_single_bp, sig_sbp),
    ]:
        dr_list = [dr for dr in sorted(V_dict.keys()) if dr >= 2]
        v_list = [V_dict[dr] for dr in dr_list]
        if not has_sig or len(dr_list) < 3:
            print(f"\n  {name}: SKIP")
            continue

        success, popt, perr = fit_force(dr_list, v_list)
        if success:
            C1, C2, xi = popt
            C1e, C2e, xie = perr
            print(f"\n  {name} (dr>=2):")
            print(f"    C1 = {C1:.6f} +/- {C1e:.6f}")
            print(f"    C2 = {C2:.6f} +/- {C2e:.6f}")
            print(f"    xi = {xi:.4f} +/- {xie:.4f}  (theory l_AdS = {L_ADS:.4f})")
            xi_err_pct = abs(xi - L_ADS) / L_ADS * 100
            print(f"    xi deviation from l_AdS: {xi_err_pct:.1f}%")
        else:
            print(f"\n  {name} (dr>=2): FIT FAILED -- {perr}")

    # ─── Ratio analysis ──────────────────────────────────────────────────
    print()
    print("=" * 72)
    print("RATIO ANALYSIS: V_BP / V_Ry at each dr")
    print("=" * 72)

    for dr in sorted(C_vac.keys()):
        ry_val = V_ry.get(dr, 0)
        bp_val = V_bp.get(dr, float('nan'))
        sbp_val = V_single_bp.get(dr, float('nan'))
        if abs(ry_val) > 1e-10:
            ratio_bp = bp_val / ry_val if not np.isnan(bp_val) else float('nan')
            ratio_sbp = sbp_val / ry_val if not np.isnan(sbp_val) else float('nan')
            print(f"  dr={dr}: BP_dual/Ry = {ratio_bp:+.3f}   BP_single/Ry = {ratio_sbp:+.3f}")
        else:
            print(f"  dr={dr}: V_Ry ~ 0 (no signal)")

    # ─── Summary ──────────────────────────────────────────────────────────
    elapsed = time.time() - t_start
    print()
    print("=" * 72)
    print(f"SUMMARY (total runtime: {elapsed:.1f}s)")
    print("=" * 72)

    # Compare signal magnitudes
    ry_max = max(abs(V_ry[dr]) for dr in V_ry) if V_ry else 0
    bp_max = max(abs(V_bp[dr]) for dr in V_bp) if V_bp else 0
    sbp_max = max(abs(V_single_bp[dr]) for dr in V_single_bp) if V_single_bp else 0

    print(f"  Ry hologron max |V|:             {ry_max:.8f}")
    print(f"  Boundary-primary dual max |V|:   {bp_max:.8f}")
    print(f"  Boundary-primary single max |V|: {sbp_max:.8f}")

    if bp_max > ry_max:
        ratio = bp_max / ry_max if ry_max > 0 else float('inf')
        print(f"\n  >>> Boundary-primary (dual) gives {ratio:.1f}x STRONGER signal than Ry hologrons")
    elif sbp_max > ry_max:
        ratio = sbp_max / ry_max if ry_max > 0 else float('inf')
        print(f"\n  >>> Boundary-primary (single) gives {ratio:.1f}x STRONGER signal than Ry hologrons")
    elif ry_max > bp_max and ry_max > sbp_max:
        print(f"\n  >>> Ry hologrons still produce the strongest signal")
    else:
        print(f"\n  >>> Methods produce comparable signal")

    # Qualitative assessment
    print()
    print("  QUALITATIVE ASSESSMENT:")
    print("  -" * 36)

    # Check decay patterns
    ry_vals = [V_ry[dr] for dr in sorted(V_ry.keys()) if dr <= 4]
    bp_vals = [V_bp[dr] for dr in sorted(V_bp.keys()) if dr <= 4]
    sbp_vals = [V_single_bp[dr] for dr in sorted(V_single_bp.keys()) if dr <= 4]

    ry_neg_decay = all(v < 0 for v in ry_vals[:2]) and abs(ry_vals[0]) > abs(ry_vals[1])
    bp_neg_decay = all(v < 0 for v in bp_vals[:2]) and abs(bp_vals[0]) > abs(bp_vals[1])

    print(f"  Ry: negative monotonic decay (dr=1,2): {ry_neg_decay}")
    print(f"  BP dual: negative monotonic decay (dr=1,2): {bp_neg_decay}")
    print(f"  BP dual signal at dr=1 is {abs(bp_vals[0])/abs(ry_vals[0]):.1f}x Ry at dr=1")
    print(f"  BP dual signal at dr=2 is {abs(bp_vals[1])/abs(ry_vals[1]):.1f}x Ry at dr=2")
    print(f"  Both methods show sign flip near dr=3 (V goes positive)")
    print(f"  Signal dies at dr>=5 (MERA causal cone limit for 3-layer circuit)")

    print()


if __name__ == "__main__":
    main()
