"""
Boundary-Primary Excitations vs Ry Hologrons - Force Profile (24q/5-layer)
==========================================================================
Tests HYP-2026-002 on the SIM-2026-008c optimized ground state (24q, 5-layer
MERA with 2-phase ALM+projection, <P>=1.000).

Key differences from the 16q version:
- NQ=24, NLAYERS=5 (252 parameters)
- MERA circuit matches vqe_z2_enforced_24q_runpod.py: U(t,p,l) gates,
  even+odd offset pairs per layer, CX entangling
- Z2 parity projection applied to ground state and all excited states
- dr range 1..12 (5-layer circuit has deeper causal cone)
- All operators sparse (2^24 = 16M dimensional Hilbert space)

Boundary-primary operator (sigma excitation at boundary site j):
  sigma^boundary_j = 0.635 * (X_j + X_{j+1})
                   - 0.026 * (X_j Z_{j+1} + Z_j X_{j+1})

Author: qiskit-builder (manual test)
Date:   2026-03-11
"""

import numpy as np
import time
from scipy import sparse
from scipy.optimize import curve_fit
from qiskit import QuantumCircuit
from qiskit.circuit import Parameter
from qiskit.quantum_info import Statevector

# --- Configuration --------------------------------------------------------
NQ = 24
NLAYERS = 5
ANCHOR = NQ // 4  # site 6
DR_MAX = min(12, NQ - ANCHOR - 1)  # 12 or 17, whichever is smaller
DR_VALUES = list(range(1, DR_MAX + 1))
HOLOGRON_ANGLE = np.pi / 3

# Boundary-primary coefficients (Zou-Milsted-Vidal / Wang-He)
ALPHA = 0.635
BETA = -0.026

# Reference values
E0_EXACT = -30.199712
L_ADS = 1.0 / np.log(2)  # 1.4427

THETA_PATH = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026008c.npy"


# --- MERA circuit builder (matches vqe_z2_enforced_24q_runpod.py) ----------
def build_mera(nq, nlayers):
    """Build MERA circuit with U gates. Returns (circuit, params_list)."""
    qc = QuantumCircuit(nq)
    params = []
    pidx = 0
    for layer in range(nlayers):
        step = 2 ** layer
        # Even-offset pairs
        for i in range(0, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp.append(p)
                    pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp2.append(p)
                    pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
        # Odd-offset pairs
        for i in range(step, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp.append(p)
                    pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}")
                    params.append(p)
                    pp2.append(p)
                    pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
    return qc, params


# --- Z2 parity projection (CPU, numpy) ------------------------------------
PARITY_MASK = (1 << NQ) - 1
PARITY_INDICES = np.arange(1 << NQ, dtype=np.int64) ^ PARITY_MASK


def parity_project(sv):
    """Project statevector onto P=+1 sector."""
    sv_plus = sv + sv[PARITY_INDICES]
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        print("  WARNING: state entirely in P=-1 sector!")
        return sv
    return sv_plus / norm


def parity_expectation(sv):
    """<P> = <sv|P|sv> where P = prod X_i."""
    return float(np.real(np.sum(np.conj(sv) * sv[PARITY_INDICES])))


# --- Sparse operator builders ---------------------------------------------
def sparse_pauli_single(n, qubit, pauli):
    """Build sparse matrix for single Pauli on qubit in n-qubit system."""
    I2 = sparse.eye(2, format='csr')
    X = sparse.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Y = sparse.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    Z = sparse.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
    paulis = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
    op = paulis[pauli]
    # Qiskit convention: qubit 0 is rightmost
    mats = [op if q == qubit else I2 for q in range(n)]
    result = mats[0]
    for m in mats[1:]:
        result = sparse.kron(result, m, format='csr')
    return result


def sparse_pauli_two(n, q1, p1, q2, p2):
    """Build sparse matrix for two-qubit Pauli: p1 on q1, p2 on q2."""
    I2 = sparse.eye(2, format='csr')
    X = sparse.csr_matrix(np.array([[0, 1], [1, 0]], dtype=complex))
    Y = sparse.csr_matrix(np.array([[0, -1j], [1j, 0]], dtype=complex))
    Z = sparse.csr_matrix(np.array([[1, 0], [0, -1]], dtype=complex))
    paulis = {'I': I2, 'X': X, 'Y': Y, 'Z': Z}
    op1, op2 = paulis[p1], paulis[p2]
    mats = []
    for q in range(n):
        if q == q1:
            mats.append(op1)
        elif q == q2:
            mats.append(op2)
        else:
            mats.append(I2)
    result = mats[0]
    for m in mats[1:]:
        result = sparse.kron(result, m, format='csr')
    return result


def build_boundary_primary(n, j):
    """
    Boundary-primary excitation operator at site j:
      sigma^boundary_j = alpha * (X_j + X_{j+1})
                       + beta  * (X_j Z_{j+1} + Z_j X_{j+1})
    Returns sparse matrix.
    """
    op = ALPHA * (sparse_pauli_single(n, j, 'X') +
                  sparse_pauli_single(n, j + 1, 'X'))
    op += BETA * (sparse_pauli_two(n, j, 'X', j + 1, 'Z') +
                  sparse_pauli_two(n, j, 'Z', j + 1, 'X'))
    return op


def build_ry_matrix(n, qubit, angle):
    """Sparse Ry(angle) gate on specified qubit."""
    I2 = sparse.eye(2, format='csr')
    c, s = np.cos(angle / 2), np.sin(angle / 2)
    Ry = sparse.csr_matrix(np.array([[c, -s], [s, c]], dtype=complex))
    mats = [Ry if q == qubit else I2 for q in range(n)]
    result = mats[0]
    for m in mats[1:]:
        result = sparse.kron(result, m, format='csr')
    return result


# --- Measurement functions -------------------------------------------------
def expect(sv, op):
    """<sv|op|sv> for sparse op and numpy sv."""
    return np.real(np.conj(sv) @ (op @ sv))


def zz_connected(sv, ZZ_op, Zi_op, Zj_op):
    """C_connected = <ZZ> - <Z><Z>."""
    return expect(sv, ZZ_op) - expect(sv, Zi_op) * expect(sv, Zj_op)


# --- Force profile model --------------------------------------------------
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


# --- Main ------------------------------------------------------------------
def main():
    print("=" * 76)
    print("BOUNDARY-PRIMARY vs Ry HOLOGRON - Force Profile (24q/5-layer MERA)")
    print("=" * 76)
    t_start = time.time()

    # 1. Load optimized parameters
    print(f"\n[1/7] Loading optimized theta from SIM-2026-006...")
    theta = np.load(THETA_PATH)
    print(f"  Loaded {len(theta)} parameters")
    assert len(theta) == 252, f"Expected 252 params, got {len(theta)}"

    # 2. Build circuit template
    print(f"\n[2/7] Building MERA circuit template...")
    t0 = time.time()
    qc_template, params_list = build_mera(NQ, NLAYERS)
    n_params = len(params_list)
    print(f"  Circuit: {NQ}q, {NLAYERS} layers, {n_params} params, "
          f"depth={qc_template.depth()}")
    assert n_params == 252, f"Expected 252 params in circuit, got {n_params}"

    # 3. Build ground state statevector with Z2 projection
    print(f"\n[3/7] Building statevector + Z2 projection...")
    t0 = time.time()
    qc_bound = qc_template.assign_parameters(
        dict(zip(params_list, theta.tolist()))
    )
    sv_raw = np.array(Statevector(qc_bound))
    sv_ground = parity_project(sv_raw)
    parity = parity_expectation(sv_ground)
    print(f"  Statevector shape: {sv_ground.shape}")
    print(f"  <P> = {parity:.6f} (should be 1.0)")
    print(f"  Done in {time.time()-t0:.2f}s")

    # 4. Build sparse Hamiltonian and verify energy
    print(f"\n[4/7] Building sparse TFIM Hamiltonian (this takes ~30-60s)...")
    t0 = time.time()
    H = sparse.csr_matrix((2**NQ, 2**NQ), dtype=complex)
    for i in range(NQ - 1):
        H -= sparse_pauli_two(NQ, i, 'Z', i + 1, 'Z')
    for i in range(NQ):
        H -= sparse_pauli_single(NQ, i, 'X')
    E_ground = expect(sv_ground, H)
    pct_err = abs(E_ground - E0_EXACT) / abs(E0_EXACT) * 100
    print(f"  H shape: {H.shape}, nnz: {H.nnz}")
    print(f"  E_ground = {E_ground:.6f} (exact: {E0_EXACT:.6f}, error: {pct_err:.2f}%)")
    print(f"  Built in {time.time()-t0:.2f}s")

    # 5. Pre-build ZZ and Z operators
    print(f"\n[5/7] Pre-building ZZ and Z operators for dr=1..{DR_MAX}...")
    t0 = time.time()
    ZZ_ops = {}
    Zi_ops = {}
    for dr in DR_VALUES:
        j_site = ANCHOR + dr
        if j_site >= NQ:
            continue
        ZZ_ops[dr] = sparse_pauli_two(NQ, ANCHOR, 'Z', j_site, 'Z')
        if ANCHOR not in Zi_ops:
            Zi_ops[ANCHOR] = sparse_pauli_single(NQ, ANCHOR, 'Z')
        if j_site not in Zi_ops:
            Zi_ops[j_site] = sparse_pauli_single(NQ, j_site, 'Z')
    print(f"  Built {len(ZZ_ops)} ZZ operators + {len(Zi_ops)} Z operators "
          f"in {time.time()-t0:.2f}s")

    # 6. Measure vacuum correlators
    print(f"\n[6/7] Measuring vacuum ZZ correlators (anchor={ANCHOR})...")
    C_vac = {}
    for dr in DR_VALUES:
        j_site = ANCHOR + dr
        if j_site >= NQ:
            continue
        C_vac[dr] = zz_connected(sv_ground, ZZ_ops[dr],
                                  Zi_ops[ANCHOR], Zi_ops[j_site])
        print(f"  C_vac(dr={dr:2d}) = {C_vac[dr]:+.8f}")

    # 7. Apply excitations and measure
    print(f"\n[7/7] Measuring force profiles...")
    print()

    # --- Method A: Ry hologron ---
    print("-" * 76)
    print("METHOD A: Ry HOLOGRON  (Ry(pi/3) on anchor and probe)")
    print("-" * 76)

    V_ry = {}
    C_two_ry = {}
    Ry_anchor = build_ry_matrix(NQ, ANCHOR, HOLOGRON_ANGLE)

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        Ry_probe = build_ry_matrix(NQ, j_site, HOLOGRON_ANGLE)
        # Apply Ry to projected ground state, then re-project
        sv_exc = Ry_probe @ (Ry_anchor @ sv_ground)
        sv_exc = parity_project(sv_exc)

        C_two_ry[dr] = zz_connected(sv_exc, ZZ_ops[dr],
                                      Zi_ops[ANCHOR], Zi_ops[j_site])
        V_ry[dr] = C_two_ry[dr] - C_vac[dr]
        print(f"  dr={dr:2d}: C_two={C_two_ry[dr]:+.10f}  "
              f"C_vac={C_vac[dr]:+.10f}  V={V_ry[dr]:+.10f}")

    # --- Method B: Boundary-primary excitation (dual) ---
    print()
    print("-" * 76)
    print("METHOD B: BOUNDARY-PRIMARY EXCITATION (dual)")
    print(f"  sigma_j = {ALPHA}*(X_j + X_{{j+1}}) "
          f"+ ({BETA})*(X_j Z_{{j+1}} + Z_j X_{{j+1}})")
    print("-" * 76)

    sigma_anchor = build_boundary_primary(NQ, ANCHOR)
    sv_bp_anchor = sigma_anchor @ sv_ground
    norm_anchor = np.linalg.norm(sv_bp_anchor)
    print(f"  ||sigma_anchor |GS>|| = {norm_anchor:.6f}")

    V_bp = {}
    C_two_bp = {}

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        if j_site + 1 >= NQ:
            print(f"  dr={dr:2d}: SKIP (j+1={j_site+1} >= N={NQ})")
            continue

        sigma_probe = build_boundary_primary(NQ, j_site)
        sv_exc = sigma_probe @ sv_bp_anchor
        # Re-project after excitation
        sv_exc = parity_project(sv_exc)

        C_two_bp[dr] = zz_connected(sv_exc, ZZ_ops[dr],
                                      Zi_ops[ANCHOR], Zi_ops[j_site])
        V_bp[dr] = C_two_bp[dr] - C_vac[dr]
        print(f"  dr={dr:2d}: C_two={C_two_bp[dr]:+.10f}  "
              f"C_vac={C_vac[dr]:+.10f}  V={V_bp[dr]:+.10f}  "
              f"||exc||={np.linalg.norm(sigma_probe @ sv_bp_anchor):.6f}")

    # --- Method C: Single boundary-primary (anchor only) ---
    print()
    print("-" * 76)
    print("METHOD C: SINGLE BOUNDARY-PRIMARY (anchor only)")
    print("  Measures how ZZ correlators shift with one primary insertion")
    print("-" * 76)

    sv_single_bp = parity_project(sv_bp_anchor)
    V_single_bp = {}
    C_single_bp = {}

    for dr in sorted(C_vac.keys()):
        j_site = ANCHOR + dr
        C_single_bp[dr] = zz_connected(sv_single_bp, ZZ_ops[dr],
                                         Zi_ops[ANCHOR], Zi_ops[j_site])
        V_single_bp[dr] = C_single_bp[dr] - C_vac[dr]
        print(f"  dr={dr:2d}: C_exc={C_single_bp[dr]:+.10f}  "
              f"C_vac={C_vac[dr]:+.10f}  V={V_single_bp[dr]:+.10f}")

    # --- Comparison table ---
    print()
    print("=" * 76)
    print("COMPARISON TABLE")
    print("=" * 76)
    print(f"{'dr':>3}  {'V_Ry':>14}  {'V_BP_dual':>14}  "
          f"{'V_BP_single':>14}  {'C_vac':>14}")
    print("-" * 76)

    all_dr = sorted(set(C_vac.keys()))
    for dr in all_dr:
        v_ry_val = V_ry.get(dr, float('nan'))
        v_bp_val = V_bp.get(dr, float('nan'))
        v_sbp_val = V_single_bp.get(dr, float('nan'))
        c_vac_val = C_vac.get(dr, float('nan'))
        print(f"{dr:3d}  {v_ry_val:+14.10f}  {v_bp_val:+14.10f}  "
              f"{v_sbp_val:+14.10f}  {c_vac_val:+14.10f}")

    # --- Signal analysis ---
    print()
    print("=" * 76)
    print("SIGNAL ANALYSIS")
    print("=" * 76)

    def analyze_signal(name, V_dict):
        if not V_dict:
            print(f"  {name}: no data")
            return False
        vals = [V_dict[dr] for dr in sorted(V_dict.keys())]
        if len(vals) < 3:
            print(f"  {name}: too few points ({len(vals)})")
            return False
        max_abs = max(abs(v) for v in vals)
        signal_range = max(vals) - min(vals)
        monotonic = all(vals[i] >= vals[i + 1] for i in range(len(vals) - 1))
        mostly_negative = sum(1 for v in vals if v < 0) > len(vals) / 2

        print(f"\n  {name}:")
        print(f"    Max |V|:       {max_abs:.10f}")
        print(f"    Signal range:  {signal_range:.10f}")
        print(f"    Monotonic:     {monotonic}")
        print(f"    Mostly neg:    {mostly_negative}")
        print(f"    Values:        {[f'{v:.8f}' for v in vals]}")

        # Key test: signal at dr >= 5 (beyond 3-layer causal cone)
        deep_vals = [V_dict[dr] for dr in sorted(V_dict.keys()) if dr >= 5]
        if deep_vals:
            deep_max = max(abs(v) for v in deep_vals)
            print(f"    Signal at dr>=5: max|V|={deep_max:.10f}  "
                  f"({'SIGNIFICANT' if deep_max > 1e-4 else 'weak/zero'})")
            # Signal at dr >= 8 (deep bulk)
            very_deep = [V_dict[dr] for dr in sorted(V_dict.keys()) if dr >= 8]
            if very_deep:
                vd_max = max(abs(v) for v in very_deep)
                print(f"    Signal at dr>=8: max|V|={vd_max:.10f}  "
                      f"({'SIGNIFICANT' if vd_max > 1e-4 else 'weak/zero'})")

        has_signal = max_abs > 1e-4
        return has_signal

    sig_ry = analyze_signal("Ry hologron (dual)", V_ry)
    sig_bp = analyze_signal("Boundary-primary (dual)", V_bp)
    sig_sbp = analyze_signal("Boundary-primary (single)", V_single_bp)

    # --- Exponential fits ---
    print()
    print("=" * 76)
    print("EXPONENTIAL FITS: V(dr) = C1 - C2 * exp(-dr / xi)")
    print("=" * 76)

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
            print(f"    C1 = {C1:.8f} +/- {C1e:.8f}")
            print(f"    C2 = {C2:.8f} +/- {C2e:.8f}")
            print(f"    xi = {xi:.4f} +/- {xie:.4f}  "
                  f"(theory l_AdS = {L_ADS:.4f})")
            xi_err_pct = abs(xi - L_ADS) / L_ADS * 100
            print(f"    xi deviation from l_AdS: {xi_err_pct:.1f}%")
        else:
            print(f"\n  {name}: FIT FAILED -- {perr}")

    # --- Fits excluding dr=1 ---
    print()
    print("=" * 76)
    print("FITS EXCLUDING dr=1 (remove contact-distance distortion)")
    print("=" * 76)

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
            print(f"    C1 = {C1:.8f} +/- {C1e:.8f}")
            print(f"    C2 = {C2:.8f} +/- {C2e:.8f}")
            print(f"    xi = {xi:.4f} +/- {xie:.4f}  "
                  f"(theory l_AdS = {L_ADS:.4f})")
            xi_err_pct = abs(xi - L_ADS) / L_ADS * 100
            print(f"    xi deviation from l_AdS: {xi_err_pct:.1f}%")
        else:
            print(f"\n  {name} (dr>=2): FIT FAILED -- {perr}")

    # --- Ratio analysis ---
    print()
    print("=" * 76)
    print("RATIO ANALYSIS: V_BP / V_Ry at each dr")
    print("=" * 76)

    for dr in sorted(C_vac.keys()):
        ry_val = V_ry.get(dr, 0)
        bp_val = V_bp.get(dr, float('nan'))
        sbp_val = V_single_bp.get(dr, float('nan'))
        if abs(ry_val) > 1e-10:
            ratio_bp = bp_val / ry_val if not np.isnan(bp_val) else float('nan')
            ratio_sbp = sbp_val / ry_val if not np.isnan(sbp_val) else float('nan')
            print(f"  dr={dr:2d}: BP_dual/Ry = {ratio_bp:+.4f}   "
                  f"BP_single/Ry = {ratio_sbp:+.4f}")
        else:
            print(f"  dr={dr:2d}: V_Ry ~ 0 (no signal)")

    # --- Causal cone analysis (KEY for 5-layer) ---
    print()
    print("=" * 76)
    print("CAUSAL CONE ANALYSIS (5-layer vs 3-layer)")
    print("=" * 76)
    print("  3-layer causal cone limit: dr ~ 4-5")
    print("  5-layer causal cone limit: dr ~ 16-17")
    print()

    for name, V_dict in [
        ("Ry hologron", V_ry),
        ("BP dual", V_bp),
        ("BP single", V_single_bp),
    ]:
        if not V_dict:
            continue
        dr_sorted = sorted(V_dict.keys())
        # Find where signal drops below noise (1e-5)
        threshold = 1e-5
        last_sig_dr = 0
        for dr in dr_sorted:
            if abs(V_dict[dr]) > threshold:
                last_sig_dr = dr
        print(f"  {name:20s}: signal extends to dr={last_sig_dr} "
              f"(threshold={threshold:.0e})")
        # Show dr=5..8 values specifically
        print(f"    dr=5..8: {[f'{V_dict.get(dr, 0):.8f}' for dr in range(5, 9)]}")

    # --- Summary ---
    elapsed = time.time() - t_start
    print()
    print("=" * 76)
    print(f"SUMMARY (total runtime: {elapsed:.1f}s)")
    print("=" * 76)

    ry_max = max(abs(V_ry[dr]) for dr in V_ry) if V_ry else 0
    bp_max = max(abs(V_bp[dr]) for dr in V_bp) if V_bp else 0
    sbp_max = max(abs(V_single_bp[dr]) for dr in V_single_bp) if V_single_bp else 0

    print(f"  Ry hologron max |V|:             {ry_max:.10f}")
    print(f"  Boundary-primary dual max |V|:   {bp_max:.10f}")
    print(f"  Boundary-primary single max |V|: {sbp_max:.10f}")
    print(f"  Ground state energy: {E_ground:.6f} "
          f"(exact: {E0_EXACT}, error: {pct_err:.2f}%)")
    print(f"  <P> = {parity:.6f}")

    if bp_max > ry_max:
        ratio = bp_max / ry_max if ry_max > 0 else float('inf')
        print(f"\n  >>> Boundary-primary (dual) gives {ratio:.1f}x "
              f"STRONGER signal than Ry hologrons")
    elif sbp_max > ry_max:
        ratio = sbp_max / ry_max if ry_max > 0 else float('inf')
        print(f"\n  >>> Boundary-primary (single) gives {ratio:.1f}x "
              f"STRONGER signal than Ry hologrons")
    elif ry_max > bp_max and ry_max > sbp_max:
        print(f"\n  >>> Ry hologrons still produce the strongest signal")
    else:
        print(f"\n  >>> Methods produce comparable signal")

    # Key verdict: does 5-layer MERA propagate deeper?
    print()
    print("  KEY QUESTION: Does signal extend beyond dr=4 (3-layer limit)?")
    for name, V_dict in [("Ry", V_ry), ("BP_dual", V_bp), ("BP_single", V_single_bp)]:
        deep = {dr: V_dict[dr] for dr in V_dict if dr >= 5}
        if deep:
            deep_max = max(abs(v) for v in deep.values())
            if deep_max > 1e-4:
                print(f"    {name}: YES - signal at dr>=5, max|V|={deep_max:.8f}")
            elif deep_max > 1e-5:
                print(f"    {name}: MARGINAL - weak signal at dr>=5, "
                      f"max|V|={deep_max:.8f}")
            else:
                print(f"    {name}: NO - signal dies at dr>=5, "
                      f"max|V|={deep_max:.10f}")

    print()


if __name__ == "__main__":
    main()
