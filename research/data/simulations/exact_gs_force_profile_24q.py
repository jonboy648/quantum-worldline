"""
Boundary-Primary Force Profile on EXACT 24q Critical TFIM Ground State
=======================================================================
Decouples physics question (holographic forces?) from state-prep question
(can MERA prepare the critical state?).

Key steps:
1. Build 24q OBC critical TFIM Hamiltonian: H = -sum Z_i Z_{i+1} - sum X_i
2. Find exact ground state via eigsh(H, k=1, which='SA')
3. Verify critical correlations: C_vac(dr) ~ r^(-1/4), NOT flat at 0.70
4. Apply boundary-primary excitations at anchor=6, probes=6+dr for dr=1..12
   sigma_j = 0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})
5. Measure V(dr) = C_two(dr) - C_vac(dr) where C = <ZZ> - <Z><Z>
6. Fit exponential V = B*exp(-dr/xi) and power-law V = A*dr^(-alpha)
7. Compare xi to l_AdS = 1/ln(2) = 1.443

Key question: does V(dr) show clear holographic decay with xi near l_AdS?

If YES: physics confirmed, problem is purely state preparation on hardware.
If NO:  holographic force hypothesis is wrong even for the correct ground state.

Author: computation-lead
Date:   2026-03-17
"""

import sys
import io
import numpy as np
import time
import json
from scipy import sparse
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

# Windows cp1252 console fix - avoid Unicode crashes
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# ── Configuration ─────────────────────────────────────────────────────────────
NQ = 24
E0_EXPECTED = -30.199712
L_ADS = 1.0 / np.log(2)          # 1.4427
ANCHOR = NQ // 4                   # site 6
DR_MAX = 12
DR_VALUES = list(range(1, DR_MAX + 1))

# Boundary-primary coefficients (Zou-Milsted-Vidal / Wang-He)
ALPHA_BP = 0.635
BETA_BP  = -0.026

OUT_PATH = "D:/quantum-worldline/research/data/simulations/SIM-2026-010.json"

# ── Sparse Pauli builders ────────────────────────────────────────────────────
_I = sparse.eye(2, format='csr', dtype=complex)
_X = sparse.csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Y = sparse.csr_matrix([[0, -1j], [1j, 0]], dtype=complex)
_Z = sparse.csr_matrix([[1, 0], [0, -1]], dtype=complex)
_PAULIS = {'I': _I, 'X': _X, 'Y': _Y, 'Z': _Z}


def kron_pauli(n, qubit_ops):
    """
    Build n-qubit sparse operator from a dict {qubit: pauli_char}.
    Qiskit convention: qubit 0 is rightmost (least significant bit).
    Missing qubits are identity.
    """
    ops = [qubit_ops.get(q, 'I') for q in range(n)]
    result = _PAULIS[ops[0]]
    for op in ops[1:]:
        result = sparse.kron(result, _PAULIS[op], format='csr')
    return result


def single_pauli(n, qubit, pauli):
    return kron_pauli(n, {qubit: pauli})


def two_pauli(n, q1, p1, q2, p2):
    return kron_pauli(n, {q1: p1, q2: p2})


# ── Hamiltonian builder ───────────────────────────────────────────────────────
def build_tfim_obc(n):
    """Critical TFIM: H = -sum_{i} Z_i Z_{i+1} - sum_i X_i, OBC."""
    dim = 1 << n
    H = sparse.csr_matrix((dim, dim), dtype=complex)
    for i in range(n - 1):
        H -= two_pauli(n, i, 'Z', i + 1, 'Z')
    for i in range(n):
        H -= single_pauli(n, i, 'X')
    return H


# ── Measurement helpers ──────────────────────────────────────────────────────
def expect(sv, op):
    """<sv|op|sv>, returns real scalar."""
    return float(np.real(sv.conj() @ (op @ sv)))


def zz_connected(sv, ZZ_op, Zi_op, Zj_op):
    """Connected ZZ correlator: <ZZ> - <Z><Z>."""
    return expect(sv, ZZ_op) - expect(sv, Zi_op) * expect(sv, Zj_op)


# ── Boundary-primary operator ─────────────────────────────────────────────────
def build_bp_operator(n, j):
    """
    sigma^boundary_j = ALPHA*(X_j + X_{j+1}) + BETA*(X_j Z_{j+1} + Z_j X_{j+1})
    Valid for j < n-1.
    """
    op = ALPHA_BP * (single_pauli(n, j, 'X') + single_pauli(n, j + 1, 'X'))
    op += BETA_BP * (two_pauli(n, j, 'X', j + 1, 'Z') +
                     two_pauli(n, j, 'Z', j + 1, 'X'))
    return op


def build_ry_matrix(n, qubit, angle):
    """Sparse Ry(angle) gate on qubit."""
    c, s = float(np.cos(angle / 2)), float(np.sin(angle / 2))
    Ry = sparse.csr_matrix([[c, -s], [s, c]], dtype=complex)
    ops = [Ry if q == qubit else _I for q in range(n)]
    result = ops[0]
    for m in ops[1:]:
        result = sparse.kron(result, m, format='csr')
    return result


# ── Fit models ────────────────────────────────────────────────────────────────
def exp_model(x, B, xi):
    """V(dr) = B * exp(-dr / xi)."""
    return B * np.exp(-np.array(x, dtype=float) / xi)


def powerlaw_model(x, A, alpha):
    """V(dr) = A * dr^(-alpha)."""
    return A * np.power(np.array(x, dtype=float), -alpha)


def fit_exponential(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    try:
        popt, pcov = curve_fit(exp_model, x, y,
                               p0=[y[0], 1.5],
                               maxfev=20000,
                               bounds=([-10, 0.05], [10, 20]))
        perr = np.sqrt(np.diag(pcov))
        return True, popt, perr
    except Exception as e:
        return False, None, str(e)


def fit_powerlaw(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float)
    y = np.array(v_arr, dtype=float)
    # Power law only sensible for one-signed data
    try:
        popt, pcov = curve_fit(powerlaw_model, x, y,
                               p0=[y[0], 0.5],
                               maxfev=20000,
                               bounds=([-10, 0.01], [10, 10]))
        perr = np.sqrt(np.diag(pcov))
        return True, popt, perr
    except Exception as e:
        return False, None, str(e)


# ── Main ──────────────────────────────────────────────────────────────────────
def main():
    print("=" * 72)
    print("EXACT GROUND STATE FORCE PROFILE  --  24q critical TFIM")
    print("=" * 72)
    t_global = time.time()

    # ── Step 1: Build Hamiltonian ────────────────────────────────────────────
    print(f"\n[1/7] Building 24q OBC critical TFIM Hamiltonian...")
    t0 = time.time()
    H = build_tfim_obc(NQ)
    print(f"  H shape: {H.shape}  nnz: {H.nnz}  built in {time.time()-t0:.1f}s")

    # ── Step 2: Exact diagonalization ────────────────────────────────────────
    print(f"\n[2/7] eigsh(H, k=1, which='SA')  -- expect ~60-90s...")
    t0 = time.time()
    evals, evecs = eigsh(H, k=1, which='SA')
    E0 = float(evals[0])
    gs = evecs[:, 0].astype(complex)
    # eigsh returns arbitrary phase; make sure gs is real-positive-dominated
    phase_idx = np.argmax(np.abs(gs))
    gs = gs * np.exp(-1j * np.angle(gs[phase_idx]))
    gs = gs / np.linalg.norm(gs)
    elapsed_eig = time.time() - t0
    print(f"  E0 = {E0:.6f}  (expected {E0_EXPECTED:.6f})")
    print(f"  Energy error: {abs(E0 - E0_EXPECTED):.6f}  "
          f"({abs(E0 - E0_EXPECTED)/abs(E0_EXPECTED)*100:.4f}%)")
    print(f"  eigsh elapsed: {elapsed_eig:.1f}s")

    assert abs(E0 - E0_EXPECTED) < 0.01, \
        f"Ground state energy wrong: {E0} vs {E0_EXPECTED}"

    # ── Step 3: Verify critical correlations ─────────────────────────────────
    print(f"\n[3/7] Verifying critical correlations C_vac(dr) ~ r^(-1/4)...")
    # Pre-build a subset of operators for the check
    check_drs = [1, 2, 4, 8, 12]
    check_drs = [dr for dr in check_drs if ANCHOR + dr < NQ]

    Zi_check = {ANCHOR: single_pauli(NQ, ANCHOR, 'Z')}
    for dr in check_drs:
        j = ANCHOR + dr
        Zi_check[j] = single_pauli(NQ, j, 'Z')

    print(f"  {'dr':>4}  {'C_raw':>12}  {'<Z_i>':>10}  {'<Z_j>':>10}  "
          f"{'C_conn':>12}  {'r^(-1/4)':>10}")
    z_anchor = expect(gs, Zi_check[ANCHOR])
    c_check_vals = {}
    for dr in check_drs:
        j = ANCHOR + dr
        ZZ_op = two_pauli(NQ, ANCHOR, 'Z', j, 'Z')
        c_raw = expect(gs, ZZ_op)
        z_j = expect(gs, Zi_check[j])
        c_conn = c_raw - z_anchor * z_j
        c_check_vals[dr] = c_conn
        r_pred = float(dr) ** (-0.25)
        print(f"  {dr:>4d}  {c_raw:+12.6f}  {z_anchor:+10.6f}  "
              f"{z_j:+10.6f}  {c_conn:+12.6f}  {r_pred:+10.6f}")

    # Check: critical state should have C_vac(12) significantly below C_vac(1)
    if 1 in c_check_vals and 12 in c_check_vals:
        ratio = c_check_vals[12] / c_check_vals[1] if abs(c_check_vals[1]) > 1e-10 else 0
        print(f"\n  C_vac(12)/C_vac(1) = {ratio:.4f}  "
              f"(power-law ~{12**(-0.25):.4f}, flat GHZ ~1.0)")
        if abs(ratio - 1.0) < 0.1:
            print("  WARNING: C_vac looks FLAT -- state may not be critical!")
        else:
            print("  OK: C_vac is decaying -- consistent with critical state")

    # ── Step 4: Pre-build all measurement operators ──────────────────────────
    print(f"\n[4/7] Pre-building ZZ and Z operators for dr=1..{DR_MAX}...")
    t0 = time.time()
    # Only build for valid dr
    valid_drs = [dr for dr in DR_VALUES if ANCHOR + dr < NQ]
    ZZ_ops, Zi_ops = {}, {}
    for dr in valid_drs:
        j = ANCHOR + dr
        ZZ_ops[dr] = two_pauli(NQ, ANCHOR, 'Z', j, 'Z')
        if ANCHOR not in Zi_ops:
            Zi_ops[ANCHOR] = single_pauli(NQ, ANCHOR, 'Z')
        if j not in Zi_ops:
            Zi_ops[j] = single_pauli(NQ, j, 'Z')
    print(f"  Built {len(ZZ_ops)} ZZ + {len(Zi_ops)} Z operators "
          f"in {time.time()-t0:.1f}s")

    # ── Step 5: Vacuum correlators ────────────────────────────────────────────
    print(f"\n[5/7] Measuring vacuum ZZ correlators (anchor={ANCHOR})...")
    C_vac = {}
    z_anc = expect(gs, Zi_ops[ANCHOR])
    for dr in valid_drs:
        j = ANCHOR + dr
        c = zz_connected(gs, ZZ_ops[dr], Zi_ops[ANCHOR], Zi_ops[j])
        C_vac[dr] = c
        print(f"  C_vac(dr={dr:2d}) = {c:+.8f}")

    # ── Step 6: Boundary-primary excitations ─────────────────────────────────
    print(f"\n[6/7] Applying boundary-primary excitations...")
    print(f"  sigma_j = {ALPHA_BP}*(X_j + X_{{j+1}}) + ({BETA_BP})*(X_j Z_{{j+1}} + Z_j X_{{j+1}})")

    # Build sigma at anchor (site 6) -- normalise the excited state
    sigma_anchor = build_bp_operator(NQ, ANCHOR)
    sv_exc_anchor = sigma_anchor @ gs
    norm_anchor = np.linalg.norm(sv_exc_anchor)
    print(f"\n  ||sigma_anchor |GS>|| = {norm_anchor:.6f}")

    if norm_anchor < 1e-10:
        print("  ERROR: anchor excitation has zero norm! Aborting.")
        return

    sv_exc_anchor_normed = sv_exc_anchor / norm_anchor

    V_bp = {}       # dual: sigma at anchor AND probe
    C_two_bp = {}
    V_bp_single = {}    # single: sigma at anchor only, ZZ measured
    C_two_bp_single = {}

    print(f"\n  {'dr':>4}  {'C_two_dual':>14}  {'C_vac':>14}  "
          f"{'V_dual':>14}  {'||exc||':>10}")

    for dr in valid_drs:
        j = ANCHOR + dr
        # Dual: apply sigma at probe too (need j+1 < NQ)
        if j + 1 < NQ:
            sigma_probe = build_bp_operator(NQ, j)
            sv_dual = sigma_probe @ sv_exc_anchor
            norm_dual = np.linalg.norm(sv_dual)
            if norm_dual < 1e-10:
                V_bp[dr] = 0.0
                C_two_bp[dr] = 0.0
                print(f"  {dr:>4d}: dual excitation zero norm -- skip")
            else:
                sv_dual_n = sv_dual / norm_dual
                C_two_bp[dr] = zz_connected(sv_dual_n, ZZ_ops[dr],
                                             Zi_ops[ANCHOR], Zi_ops[j])
                V_bp[dr] = C_two_bp[dr] - C_vac[dr]
                print(f"  {dr:>4d}  {C_two_bp[dr]:+14.8f}  {C_vac[dr]:+14.8f}  "
                      f"{V_bp[dr]:+14.8f}  {norm_dual:10.6f}")
        else:
            print(f"  {dr:>4d}: SKIP dual (j+1={j+1} >= N={NQ})")

        # Single: only anchor sigma, measure ZZ at anchor--probe
        C_two_bp_single[dr] = zz_connected(sv_exc_anchor_normed, ZZ_ops[dr],
                                             Zi_ops[ANCHOR], Zi_ops[j])
        V_bp_single[dr] = C_two_bp_single[dr] - C_vac[dr]

    print(f"\n  Single-excitation V(dr) (sigma at anchor only):")
    print(f"  {'dr':>4}  {'C_two_single':>14}  {'C_vac':>14}  {'V_single':>14}")
    for dr in valid_drs:
        print(f"  {dr:>4d}  {C_two_bp_single[dr]:+14.8f}  "
              f"{C_vac[dr]:+14.8f}  {V_bp_single[dr]:+14.8f}")

    # ── Step 7: Fits and analysis ─────────────────────────────────────────────
    print(f"\n[7/7] Fitting force profiles...")

    results = {}

    def do_fits(label, dr_list, V_dict):
        vals = [V_dict[dr] for dr in dr_list if dr in V_dict]
        dr_fit = [dr for dr in dr_list if dr in V_dict]
        if len(dr_fit) < 3:
            print(f"  {label}: too few points ({len(dr_fit)})")
            return {}

        max_abs = max(abs(v) for v in vals)
        print(f"\n  {label}  (n={len(dr_fit)} points, max|V|={max_abs:.6e})")

        fit_res = {}

        # Exponential: V = B * exp(-dr/xi)
        ok_e, popt_e, perr_e = fit_exponential(dr_fit, vals)
        if ok_e:
            B, xi = popt_e
            dB, dxi = perr_e
            xi_dev = abs(xi - L_ADS) / L_ADS * 100
            print(f"    Exponential:  B={B:+.6f}+/-{dB:.4f}  "
                  f"xi={xi:.4f}+/-{dxi:.4f}  "
                  f"(l_AdS={L_ADS:.4f}, dev={xi_dev:.1f}%)")
            fit_res['exponential'] = {
                'B': float(B), 'dB': float(dB),
                'xi': float(xi), 'dxi': float(dxi),
                'l_AdS': float(L_ADS),
                'xi_deviation_pct': float(xi_dev),
                'xi_within_1sigma': bool(abs(xi - L_ADS) < dxi)
            }
        else:
            print(f"    Exponential fit failed: {perr_e}")

        # Power law: V = A * dr^(-alpha)
        ok_p, popt_p, perr_p = fit_powerlaw(dr_fit, vals)
        if ok_p:
            A, alpha = popt_p
            dA, dalpha = perr_p
            print(f"    Power law:    A={A:+.6f}+/-{dA:.4f}  "
                  f"alpha={alpha:.4f}+/-{dalpha:.4f}  "
                  f"(CFT prediction alpha=2*Delta ~ 2)")
            fit_res['power_law'] = {
                'A': float(A), 'dA': float(dA),
                'alpha': float(alpha), 'dalpha': float(dalpha),
                'expected_alpha_stress_tensor': 4.0,
                'expected_alpha_scalar': 2.0
            }
        else:
            print(f"    Power law fit failed: {perr_p}")

        return fit_res

    print("\n-- DUAL boundary-primary (sigma at anchor + probe) --")
    dual_dr_all = [dr for dr in valid_drs if dr in V_bp]
    dual_dr_ge2 = [dr for dr in dual_dr_all if dr >= 2]
    results['BP_dual_all_dr'] = do_fits("BP_dual all dr", dual_dr_all, V_bp)
    results['BP_dual_dr_ge2'] = do_fits("BP_dual dr>=2", dual_dr_ge2, V_bp)

    print("\n-- SINGLE boundary-primary (sigma at anchor only) --")
    single_dr_all = valid_drs
    single_dr_ge2 = [dr for dr in valid_drs if dr >= 2]
    results['BP_single_all_dr'] = do_fits("BP_single all dr", single_dr_all, V_bp_single)
    results['BP_single_dr_ge2'] = do_fits("BP_single dr>=2", single_dr_ge2, V_bp_single)

    # ── Summary ───────────────────────────────────────────────────────────────
    elapsed = time.time() - t_global
    print(f"\n{'=' * 72}")
    print(f"SUMMARY  (total runtime: {elapsed:.1f}s)")
    print(f"{'=' * 72}")
    print(f"  Ground state E0 = {E0:.6f}  (expected {E0_EXPECTED:.6f})")
    print(f"  l_AdS = {L_ADS:.4f},  anchor = {ANCHOR},  NQ = {NQ}")

    if C_vac:
        c1 = C_vac.get(1, None)
        c12 = C_vac.get(12, None) or C_vac.get(max(C_vac.keys()), None)
        if c1 is not None and c12 is not None:
            max_dr = max(C_vac.keys())
            print(f"  C_vac(1)={c1:+.6f}, C_vac({max_dr})={c12:+.6f}, "
                  f"ratio={c12/c1:.4f}  (critical ~{max_dr**(-0.25):.4f})")

    if V_bp:
        dual_max = max(abs(v) for v in V_bp.values())
        print(f"  Dual BP max|V| = {dual_max:.6e}")
        if dual_max > 1e-3:
            print("  >>> STRONG holographic force signal detected!")
        elif dual_max > 1e-4:
            print("  >>> Moderate force signal -- fits may be meaningful")
        else:
            print("  >>> Force signal is weak (< 1e-4) -- holographic interpretation uncertain")

    if V_bp_single:
        single_max = max(abs(v) for v in V_bp_single.values())
        print(f"  Single BP max|V| = {single_max:.6e}")

    # ── Save JSON ──────────────────────────────────────────────────────────────
    print(f"\nSaving results to {OUT_PATH}...")

    def safe_dict(d):
        return {str(k): float(v) for k, v in d.items()}

    out = {
        "id": "SIM-2026-010",
        "date": "2026-03-17",
        "description": "Holographic force profile on EXACT 24q OBC critical TFIM ground state (eigsh)",
        "hypothesis": "HYP-2026-002",
        "ground_state": {
            "method": "eigsh(H, k=1, which='SA')",
            "qubits": int(NQ),
            "E0": float(E0),
            "E0_expected": float(E0_EXPECTED),
            "E0_error_pct": float(abs(E0 - E0_EXPECTED) / abs(E0_EXPECTED) * 100),
            "eigsh_time_s": float(elapsed_eig)
        },
        "anchor": int(ANCHOR),
        "dr_values": [int(d) for d in valid_drs],
        "boundary_primary_coeffs": {
            "alpha": float(ALPHA_BP),
            "beta": float(BETA_BP)
        },
        "C_vac": safe_dict(C_vac),
        "C_two_dual": safe_dict(C_two_bp),
        "V_dual": safe_dict(V_bp),
        "C_two_single": safe_dict(C_two_bp_single),
        "V_single": safe_dict(V_bp_single),
        "fits": results,
        "runtime_s": float(elapsed),
        "hardware": "local_cpu",
        "status": "COMPLETE"
    }

    with open(OUT_PATH, 'w') as f:
        json.dump(out, f, indent=2)
    print("  Saved.")

    print(f"\nDone in {elapsed:.1f}s")


if __name__ == "__main__":
    main()
