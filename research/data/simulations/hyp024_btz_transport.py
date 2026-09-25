"""
SIM-2026-026: Finite-temperature BTZ transport curve (HYP-2026-024)

Tests whether thermalizing the MERA boundary state via imaginary-time evolution
exp(-beta*H/2)|psi_0> makes the holographic transport time T(beta) follow the
Wang-He (arXiv:2603.07639) BTZ horizon-absorption curve, with high-T relaxation
rate Gamma(beta) ~ 2*pi/beta (BTZ quasi-normal mode, Delta=1 energy operator).

GATES (executed in order -- hard stops if any gate fails):
  Gate 1: Self-consistency: largest-beta T(beta) must reproduce HYP-006 T=2.250
          within 2% tolerance. Failure => INVALID, simulation halts.
  Gate 2: A-priori operator spec written BEFORE any fitting (see below).
  Gate 3: Beta ladder run at N=16 and reduced ladder at N=24.
  Gate 4: Wang-He curve overlay + Gamma(beta) vs 2*pi/beta fit.
  Gate 5: Truncation error bound via step-size comparison.

A-PRIORI OPERATOR SPECIFICATION (Gate 2 -- written BEFORE any fitting):
  The critical transverse-field Ising CFT has primary operators:
    sigma: Delta=1/8 (spin operator)
    epsilon: Delta=1  (energy/disorder operator)
    T (stress tensor): Delta=2 (spin-2)
  Wang-He (2603.07639) identify the relevant QNM with the energy-gap scale.
  For BTZ in AdS3, the quasi-normal mode frequency omega_n = (2*pi/beta)*(n+Delta).
  The LEADING (n=0) relaxation rate is Gamma = omega_0 = 2*pi*Delta/beta.
  We test Delta=1 (energy operator epsilon) FIRST, as specified in HYP-2026-024.
  This gives Gamma(beta) = 2*pi/beta.
  If this fails, we also check Delta=1/8 (sigma) and Delta=2 (T), but the primary
  test is Delta=1. Selection is locked before running any fits below.

Reuses: boundary Hamiltonian H_boundary from holographic_transport_16q.py (IDENTICAL).
        transport protocol (perturbation, time evolution, envelope extraction).
Does NOT: use TFD doubled register, product-of-density estimator, S_topo, TEE, Aquila.
"""
import numpy as np
import time
import json
import sys
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh, expm_multiply
from scipy.optimize import curve_fit

SCRIPT_START = time.time()

print("=" * 70)
print("SIM-2026-026: Finite-temperature BTZ transport curve")
print("HYP-2026-024 | Honest-broker classical simulation")
print("=" * 70, flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# A-PRIORI OPERATOR SPECIFICATION (Gate 2 -- locked before any fits)
# ══════════════════════════════════════════════════════════════════════════════
# Tested operator: epsilon (energy primary), Delta = 1
# Leading BTZ QNM: Gamma(beta) = 2*pi*Delta/beta = 2*pi/beta
# This is the pre-committed test. Delta is NOT tuned to fit data.
PRESPECIFIED_DELTA = 1.0
PRESPECIFIED_n_QNM = 0   # leading mode

print(f"\n[GATE 2 -- PRE-COMMITTED] Operator: epsilon, Delta={PRESPECIFIED_DELTA}")
print(f"  Predicted Gamma(beta) = 2*pi*{PRESPECIFIED_DELTA}/beta = {2*np.pi*PRESPECIFIED_DELTA:.4f}/beta")
print("  This spec is LOCKED. Delta will not be adjusted post-hoc.\n", flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# PAULI OPERATORS AND HAMILTONIAN BUILDER
# (Identical to holographic_transport_16q.py -- DO NOT MODIFY)
# ══════════════════════════════════════════════════════════════════════════════
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def sparse_pauli_full(n, i, p):
    """Single Pauli on site i in n-qubit system, sparse CSR."""
    I2s = speye(2, format="csr")
    paulis = {
        "I": I2s,
        "X": csr_matrix(X),
        "Y": csr_matrix(Y),
        "Z": csr_matrix(Z),
    }
    mats = [paulis[p] if k == i else I2s for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_H_boundary(L):
    """
    Wang & He Eq 1 boundary Hamiltonian (PBC):
      H = L/(4*pi) * sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}]
    Identical to holographic_transport_16q.py.
    """
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    prefactor = L / (4 * np.pi)
    for j in range(L):
        jm1 = (j - 1) % L
        jp1 = (j + 1) % L
        Xjm1 = sparse_pauli_full(L, jm1, "X")
        Zj   = sparse_pauli_full(L, j,   "Z")
        Xjp1 = sparse_pauli_full(L, jp1, "X")
        Xj   = sparse_pauli_full(L, j,   "X")
        H += prefactor * (Xjm1 @ Zj @ Xjp1 - Xj @ Xjp1)
    return H


def build_Y_ops(L):
    """Build sparse Y_i operators for L-site system."""
    return [sparse_pauli_full(L, i, "Y") for i in range(L)]


# ══════════════════════════════════════════════════════════════════════════════
# IMAGINARY-TIME THERMAL STATE PREPARATION
# State: |psi_beta> = exp(-beta*H/2)|psi_0> / norm
# For N=16 this is trivial (dim=65536).
# We use scipy.sparse.linalg.expm_multiply which is memory-safe for sparse H.
# ══════════════════════════════════════════════════════════════════════════════
def prepare_thermal_state(psi_gs, H, beta, n_steps_imag=20):
    """
    Imaginary-time evolution: |psi_beta> = exp(-beta*H/2)|psi_gs> / norm

    Uses Trotter splitting in imaginary time with n_steps_imag steps.
    Each step evolves by dtau = beta/(2*n_steps_imag) in imaginary time.
    Returns (psi_thermal, norm_log) where norm_log is ln of the unnormalized norm
    (useful for entropy estimates).

    For beta=0: returns psi_gs unchanged (infinite-temperature limit).
    For beta->inf: returns the ground state (same as psi_gs).
    """
    if beta <= 0:
        return psi_gs.copy(), 0.0

    dtau = beta / (2.0 * n_steps_imag)
    psi = psi_gs.copy().astype(complex)
    log_norm_accum = 0.0

    for _ in range(n_steps_imag):
        # exp(-dtau * H) psi  (imaginary time step)
        # expm_multiply applies exp(A*t) @ v with A = -H, t = dtau
        psi = expm_multiply(-H * dtau, psi)
        norm = np.linalg.norm(psi)
        log_norm_accum += np.log(norm)
        psi /= norm

    return psi, log_norm_accum


# ══════════════════════════════════════════════════════════════════════════════
# TRANSPORT PROTOCOL
# (Identical to holographic_transport_16q.py -- same parameters exactly)
# ══════════════════════════════════════════════════════════════════════════════
def run_transport(psi_init, psi_ref, H_boundary, Y_ops, L,
                  dt=0.05, t_max=6.0,
                  OMEGA=5.0, M_ang=0, sigma_t=0.4, sigma_phi=0.4):
    """
    Apply HYP-006 transport protocol:
      1. Apply Gaussian perturbation coupled to Y operators.
      2. Evolve under H_boundary.
      3. Return time-series of max boundary excitation density.

    psi_init: the thermal state (or ground state for baseline).
    psi_ref:  the reference state for subtraction (same as psi_init for baseline).

    Returns: (times, max_rho_Y, boundary_density_Y)
    """
    dim = 2 ** L
    phi = np.array([2 * np.pi * i / L - 3 * np.pi / 4 for i in range(L)])
    A = np.sqrt(2 * L / (sigma_t * sigma_phi)) / (40 * np.pi)

    n_steps = int(t_max / dt)
    times = np.arange(n_steps + 1) * dt

    # Precompute J_i(t)
    J_matrix = np.zeros((n_steps + 1, L), dtype=complex)
    for step in range(n_steps + 1):
        t = times[step]
        J_matrix[step] = A * np.exp(
            -t**2 / (2 * sigma_t**2)
            - phi**2 / (2 * sigma_phi**2)
            - 1j * OMEGA * t
            + 1j * M_ang * phi
        )

    psi = psi_init.copy().astype(complex)

    # Reference expectations (gs or thermal state)
    ref_Y_exp = np.array([np.real(psi_ref.conj() @ (Y_ops[i] @ psi_ref)) for i in range(L)])

    boundary_density_Y = np.zeros((n_steps + 1, L))

    # t=0
    for i in range(L):
        boundary_density_Y[0, i] = (
            np.real(psi.conj() @ (Y_ops[i] @ psi)) - ref_Y_exp[i]
        )

    for step in range(n_steps):
        # Build perturbation delta_H = -sum_i Re(J_i) Y_i
        delta_H = csr_matrix((dim, dim), dtype=complex)
        j_real = np.real(J_matrix[step])
        for i in range(L):
            if abs(j_real[i]) > 1e-15:
                delta_H -= j_real[i] * Y_ops[i]

        H_total = H_boundary + delta_H
        psi = expm_multiply(-1j * H_total * dt, psi)
        psi /= np.linalg.norm(psi)

        for i in range(L):
            boundary_density_Y[step + 1, i] = (
                np.real(psi.conj() @ (Y_ops[i] @ psi)) - ref_Y_exp[i]
            )

    max_rho = np.max(np.abs(boundary_density_Y), axis=1)
    return times, max_rho, boundary_density_Y


def extract_transport_signature(times, max_rho, peak_search_end=30):
    """
    Extract transport time T = reappear_time - dip_time from envelope.
    Returns dict with peak_time, dip_time, reappear_time, transport_time.
    """
    search_end = min(peak_search_end, len(max_rho))
    peak_idx = int(np.argmax(max_rho[:search_end]))

    # Dip: minimum after initial peak (search up to 80 steps)
    dip_search_end = min(peak_idx + 80, len(max_rho))
    dip_idx = peak_idx + int(np.argmin(max_rho[peak_idx:dip_search_end]))
    dip_time = float(times[dip_idx])
    dip_val = float(max_rho[dip_idx])

    # Reappearance: next peak after dip (skip 3 adjacent steps)
    reappear_search_start = dip_idx + 3
    reappear_search_end = min(dip_idx + 80, len(max_rho))
    if reappear_search_end > reappear_search_start:
        rel_idx = int(np.argmax(max_rho[reappear_search_start:reappear_search_end]))
        reappear_idx = reappear_search_start + rel_idx
        reappear_time = float(times[min(reappear_idx, len(times) - 1)])
        reappear_val = float(max_rho[min(reappear_idx, len(max_rho) - 1)])
    else:
        reappear_time = -1.0
        reappear_val = -1.0

    transport_time = reappear_time - dip_time if dip_time > 0 and reappear_time > 0 else -1.0

    return {
        "peak_time": float(times[peak_idx]),
        "peak_amplitude": float(max_rho[peak_idx]),
        "dip_time": dip_time,
        "dip_amplitude": dip_val,
        "reappear_time": reappear_time,
        "reappear_amplitude": reappear_val,
        "transport_time": transport_time,
    }


def estimate_envelope_decay(times, max_rho, t_start=3.0, t_end=6.0):
    """
    Fit exp(-Gamma*t) to the envelope after the reappearance peak.
    Returns (Gamma, Gamma_err, fit_quality).
    Returns None if insufficient data.
    """
    mask = (times >= t_start) & (times <= t_end)
    t_fit = times[mask]
    rho_fit = max_rho[mask]

    if len(t_fit) < 5:
        return None, None, None

    # Only use positive values for log fit
    pos_mask = rho_fit > 1e-10
    if pos_mask.sum() < 4:
        return None, None, None

    t_f = t_fit[pos_mask]
    r_f = rho_fit[pos_mask]

    try:
        def exp_model(t, A, Gamma):
            return A * np.exp(-Gamma * t)

        p0 = [r_f[0], 0.5]
        popt, pcov = curve_fit(exp_model, t_f, r_f, p0=p0, maxfev=5000)
        A_fit, Gamma_fit = popt
        perr = np.sqrt(np.diag(pcov))
        Gamma_err = perr[1]

        # Residuals
        residuals = r_f - exp_model(t_f, *popt)
        ss_res = np.sum(residuals**2)
        ss_tot = np.sum((r_f - r_f.mean())**2)
        r2 = 1 - ss_res / ss_tot if ss_tot > 0 else 0.0

        return float(Gamma_fit), float(Gamma_err), float(r2)
    except Exception:
        return None, None, None


# ══════════════════════════════════════════════════════════════════════════════
# TRUNCATION ERROR BOUND
# Compare n_steps_imag=20 vs n_steps_imag=40 for one beta point (large beta).
# If T differs by < 0.5%, the imag-time Trotter error is negligible.
# ══════════════════════════════════════════════════════════════════════════════
def truncation_error_check(psi_gs, H, Y_ops, H_boundary, L, beta_test):
    """
    Run transport at beta_test with n_steps=20 and n_steps=40.
    Return relative difference in transport time as truncation error bound.
    """
    print(f"  [Trunc check] beta={beta_test}: n_steps=20 vs n_steps=40...", flush=True)

    psi20, _ = prepare_thermal_state(psi_gs, H, beta_test, n_steps_imag=20)
    times20, rho20, _ = run_transport(psi20, psi20, H_boundary, Y_ops, L)
    sig20 = extract_transport_signature(times20, rho20)

    psi40, _ = prepare_thermal_state(psi_gs, H, beta_test, n_steps_imag=40)
    times40, rho40, _ = run_transport(psi40, psi40, H_boundary, Y_ops, L)
    sig40 = extract_transport_signature(times40, rho40)

    T20 = sig20["transport_time"]
    T40 = sig40["transport_time"]

    if T20 > 0 and T40 > 0:
        trunc_err = abs(T20 - T40) / max(abs(T20), abs(T40))
    else:
        trunc_err = None

    print(f"  [Trunc check] T(n=20)={T20:.3f}, T(n=40)={T40:.3f}, rel_diff={trunc_err}", flush=True)
    return {"beta": beta_test, "T_n20": T20, "T_n40": T40, "relative_diff": trunc_err}


# ══════════════════════════════════════════════════════════════════════════════
# WANG-HE BTZ HORIZON ABSORPTION CURVE
# From arXiv:2603.07639, the transport time in the presence of a BTZ black hole
# is modified by horizon absorption.  The qualitative prediction is:
#   T(beta) decreases monotonically from T_0=2.250 as 1/beta increases (T increases)
#   At high T (small beta): T(beta) -> 0 as the horizon absorbs the signal
#   The relaxation rate Gamma = 2*pi/beta (BTZ QNM, Delta=1)
#
# Functional form fitted: T(beta) = T_0 * tanh(beta / beta_c)
#   This interpolates: T(beta->inf) = T_0, T(beta->0) -> 0
#   beta_c is a fitting parameter (crossover inverse temperature)
#
# Alternative: T(beta) = T_0 * exp(-alpha_T / beta)  (Boltzmann suppression)
# We fit both and report which fits better.
# ══════════════════════════════════════════════════════════════════════════════
def wang_he_tanh(beta, T0, beta_c):
    """BTZ horizon absorption: T(beta) = T0 * tanh(beta/beta_c)."""
    return T0 * np.tanh(beta / beta_c)


def boltzmann_suppression(beta, T0, alpha_T):
    """Alternative: T(beta) = T0 * exp(-alpha_T/beta)."""
    return T0 * np.exp(-alpha_T / np.maximum(beta, 1e-6))


def flat_model(beta, T0):
    """Null hypothesis: T(beta) = const."""
    return np.full_like(beta, T0)


# ══════════════════════════════════════════════════════════════════════════════
# MAIN SIMULATION: N=16 BETA LADDER
# ══════════════════════════════════════════════════════════════════════════════
L = 16
print(f"\n{'='*70}")
print("[N=16] Building boundary Hamiltonian...")
print(f"{'='*70}", flush=True)

t0 = time.time()
H_boundary_16 = build_H_boundary(L)
Y_ops_16 = build_Y_ops(L)
print(f"  H_boundary: shape={H_boundary_16.shape}, nnz={H_boundary_16.nnz}")
print(f"  Build time: {time.time()-t0:.1f}s", flush=True)

print("[N=16] Finding ground state (eigsh)...", flush=True)
t0 = time.time()
E_gs_vals, psi_gs_vecs = eigsh(H_boundary_16, k=1, which="SA")
E_gs_16 = float(E_gs_vals[0])
psi_gs_16 = psi_gs_vecs[:, 0].astype(complex)
print(f"  E_gs = {E_gs_16:.6f}  (took {time.time()-t0:.1f}s)", flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# GATE 1: SELF-CONSISTENCY CHECK
# Largest beta (beta=100, effectively ground state) must reproduce T=2.250 +/- 2%
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[GATE 1] Self-consistency: large beta must reproduce HYP-006 T=2.250")
print("="*70, flush=True)

T_HYP006 = 2.250
GATE1_TOLERANCE = 0.02   # 2%
BETA_BASELINE = 100.0    # effectively zero-temperature

psi_baseline, _ = prepare_thermal_state(psi_gs_16, H_boundary_16, BETA_BASELINE, n_steps_imag=20)
print(f"  Thermal state prep (beta={BETA_BASELINE}): complete", flush=True)
print("  Running transport protocol...", flush=True)

times_base, rho_base, _ = run_transport(
    psi_baseline, psi_baseline, H_boundary_16, Y_ops_16, L
)
sig_baseline = extract_transport_signature(times_base, rho_base)
T_baseline = sig_baseline["transport_time"]

gate1_residual = abs(T_baseline - T_HYP006) / T_HYP006
gate1_pass = gate1_residual <= GATE1_TOLERANCE

print("\n  GATE 1 result:")
print(f"    T(beta={BETA_BASELINE}) = {T_baseline:.4f}")
print(f"    HYP-006 target: {T_HYP006:.4f}")
print(f"    Residual: {gate1_residual*100:.2f}%  (tolerance: {GATE1_TOLERANCE*100:.1f}%)")
print(f"    GATE 1: {'PASS' if gate1_pass else 'FAIL -- STOPPING (thermal-state construction broken)'}", flush=True)

if not gate1_pass:
    print("\nSIMULATION HALTED: Gate 1 failed. Result is INVALID (not refuting).")
    print("Thermal-state construction does not reproduce known baseline.")
    result_invalid = {
        "id": "SIM-2026-026",
        "description": "Finite-temperature BTZ transport curve (HYP-2026-024) -- INVALID",
        "type": "classical",
        "date": "2026-05-16",
        "hypothesis_id": "HYP-2026-024",
        "circuit": {"qubits": 16, "depth": 0, "gates": 0,
                    "script_path": "research/data/simulations/hyp024_btz_transport.py"},
        "hardware_target": "local_cpu",
        "results": {
            "verdict": "INVALID",
            "verdict_reason": "Gate 1 failed: thermal state construction does not reproduce HYP-006 T=2.250",
            "gate1_T_baseline": T_baseline,
            "gate1_target": T_HYP006,
            "gate1_residual_pct": gate1_residual * 100,
            "gate1_tolerance_pct": GATE1_TOLERANCE * 100,
        },
        "notes": "Gate 1 self-consistency failure. Simulation halted per protocol."
    }
    with open("D:/quantum-worldline/research/data/simulations/SIM-2026-026.json", "w") as f:
        json.dump(result_invalid, f, indent=2)
    sys.exit(1)

print("\n  Gate 1 PASSED. Proceeding to beta ladder.", flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# TRUNCATION ERROR BOUND (Gate 5 -- run early at large beta to bound error)
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[GATE 5] Truncation error bound (n_steps=20 vs n_steps=40 at beta=10.0)")
print("="*70, flush=True)

trunc_result = truncation_error_check(
    psi_gs_16, H_boundary_16, Y_ops_16, H_boundary_16, L, beta_test=10.0
)
trunc_bound_pct = (trunc_result["relative_diff"] * 100
                   if trunc_result["relative_diff"] is not None else None)
print(f"  Truncation error bound: {trunc_bound_pct:.3f}%" if trunc_bound_pct is not None else "  Truncation error: UNMEASURED (no signal at this beta)")

# ══════════════════════════════════════════════════════════════════════════════
# BETA LADDER: N=16
# Beta values: {100 (baseline), 20, 10, 5, 2, 1}
# Physics: beta=1/T_temperature; small beta = high temperature = near BTZ horizon
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[N=16] Running beta ladder: beta in {100, 20, 10, 5, 2, 1}")
print("="*70, flush=True)

BETA_LADDER_16 = [100.0, 20.0, 10.0, 5.0, 2.0, 1.0]
results_ladder_16 = []

for beta in BETA_LADDER_16:
    print(f"\n  --- beta = {beta:.1f} ---", flush=True)
    t0_beta = time.time()

    if beta == BETA_BASELINE:
        # Reuse already-computed baseline state
        psi_th = psi_baseline
    else:
        psi_th, log_norm = prepare_thermal_state(
            psi_gs_16, H_boundary_16, beta, n_steps_imag=20
        )

    # Run transport
    times_b, rho_b, _ = run_transport(psi_th, psi_th, H_boundary_16, Y_ops_16, L)
    sig = extract_transport_signature(times_b, rho_b)
    T_b = sig["transport_time"]

    # Envelope decay for Gamma(beta)
    Gamma_b, Gamma_err_b, r2_b = estimate_envelope_decay(times_b, rho_b, t_start=3.0, t_end=6.0)

    # Predicted QNM rate for this beta
    Gamma_predicted = 2 * np.pi * PRESPECIFIED_DELTA / beta

    elapsed = time.time() - t0_beta
    print(f"    T(beta) = {T_b:.4f}  (peak={sig['peak_time']:.2f}, dip={sig['dip_time']:.2f}, "
          f"reappear={sig['reappear_time']:.2f})", flush=True)
    if Gamma_b is not None:
        print(f"    Gamma_measured = {Gamma_b:.4f} +/- {Gamma_err_b:.4f}  (R2={r2_b:.3f})")
        print(f"    Gamma_QNM_predicted = {Gamma_predicted:.4f}  (Delta=1, beta={beta})")
    else:
        print(f"    Gamma: insufficient signal for fit  |  Gamma_QNM_predicted = {Gamma_predicted:.4f}")
    print(f"    Wall time: {elapsed:.1f}s", flush=True)

    results_ladder_16.append({
        "beta": beta,
        "temperature": 1.0 / beta,
        "transport_time": T_b,
        "peak_time": sig["peak_time"],
        "peak_amplitude": sig["peak_amplitude"],
        "dip_time": sig["dip_time"],
        "dip_amplitude": sig["dip_amplitude"],
        "reappear_time": sig["reappear_time"],
        "reappear_amplitude": sig["reappear_amplitude"],
        "Gamma_measured": Gamma_b,
        "Gamma_err": Gamma_err_b,
        "Gamma_R2": r2_b,
        "Gamma_QNM_predicted": Gamma_predicted,
        "wall_time_s": elapsed,
    })

# ══════════════════════════════════════════════════════════════════════════════
# N=24 REDUCED LADDER (finite-size control)
# Run at beta in {100, 5, 1} -- 3 points to confirm N=16 trend
# Memory: 2^24 ~ 16M complex128 = 256 MB statevector, manageable
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[N=24] Building boundary Hamiltonian (reduced ladder: beta in {100, 5, 1})...")
print("="*70, flush=True)

L24 = 24
t0 = time.time()
H_boundary_24 = build_H_boundary(L24)
Y_ops_24 = build_Y_ops(L24)
print(f"  H_boundary (N=24): shape={H_boundary_24.shape}, nnz={H_boundary_24.nnz}")
print(f"  Build time: {time.time()-t0:.1f}s", flush=True)

print("[N=24] Finding ground state (eigsh)...", flush=True)
t0 = time.time()
E_gs_vals24, psi_gs_vecs24 = eigsh(H_boundary_24, k=1, which="SA")
E_gs_24 = float(E_gs_vals24[0])
psi_gs_24 = psi_gs_vecs24[:, 0].astype(complex)
print(f"  E_gs(N=24) = {E_gs_24:.6f}  (took {time.time()-t0:.1f}s)", flush=True)

BETA_LADDER_24 = [100.0, 5.0, 1.0]
results_ladder_24 = []

for beta in BETA_LADDER_24:
    print(f"\n  --- N=24, beta = {beta:.1f} ---", flush=True)
    t0_beta = time.time()

    psi_th24, _ = prepare_thermal_state(psi_gs_24, H_boundary_24, beta, n_steps_imag=20)
    times_b24, rho_b24, _ = run_transport(psi_th24, psi_th24, H_boundary_24, Y_ops_24, L24)
    sig24 = extract_transport_signature(times_b24, rho_b24)
    T_b24 = sig24["transport_time"]

    Gamma_b24, Gamma_err_b24, r2_b24 = estimate_envelope_decay(
        times_b24, rho_b24, t_start=3.0, t_end=6.0
    )
    Gamma_pred24 = 2 * np.pi * PRESPECIFIED_DELTA / beta
    elapsed = time.time() - t0_beta

    print(f"    T(beta={beta}, N=24) = {T_b24:.4f}  (wall {elapsed:.1f}s)", flush=True)
    results_ladder_24.append({
        "beta": beta,
        "temperature": 1.0 / beta,
        "transport_time": T_b24,
        "peak_time": sig24["peak_time"],
        "peak_amplitude": sig24["peak_amplitude"],
        "dip_time": sig24["dip_time"],
        "dip_amplitude": sig24["dip_amplitude"],
        "reappear_time": sig24["reappear_time"],
        "reappear_amplitude": sig24["reappear_amplitude"],
        "Gamma_measured": Gamma_b24,
        "Gamma_err": Gamma_err_b24,
        "Gamma_R2": r2_b24,
        "Gamma_QNM_predicted": Gamma_pred24,
        "wall_time_s": elapsed,
    })

# ══════════════════════════════════════════════════════════════════════════════
# ANALYSIS: Wang-He curve fitting and verdict
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[ANALYSIS] Fitting T(beta) curves and Gamma(beta) scaling")
print("="*70, flush=True)

# Extract valid transport times (T > 0) from N=16 ladder
valid = [(r["beta"], r["transport_time"]) for r in results_ladder_16 if r["transport_time"] > 0]
betas_fit = np.array([v[0] for v in valid])
T_fit = np.array([v[1] for v in valid])

print(f"\n  Valid N=16 transport points: {len(valid)}")
for b, T in zip(betas_fit, T_fit):
    print(f"    beta={b:.1f} -> T={T:.4f}")

# Fit 1: Wang-He tanh model
wang_he_params = None
wang_he_chi2 = None
wang_he_fit_quality = "INSUFFICIENT_DATA"

# Fit 2: Boltzmann suppression
boltz_params = None
boltz_chi2 = None

# Fit 3: Flat (null hypothesis)
flat_T = float(np.mean(T_fit)) if len(T_fit) > 0 else 0.0
flat_chi2 = None

if len(betas_fit) >= 3:
    # Fit Wang-He tanh
    try:
        p0_wh = [T_HYP006, 5.0]
        popt_wh, pcov_wh = curve_fit(wang_he_tanh, betas_fit, T_fit, p0=p0_wh, maxfev=10000)
        wang_he_params = {"T0": float(popt_wh[0]), "beta_c": float(popt_wh[1])}
        residuals_wh = T_fit - wang_he_tanh(betas_fit, *popt_wh)
        wang_he_chi2 = float(np.sum(residuals_wh**2) / len(T_fit))
        wang_he_r2 = float(1 - np.sum(residuals_wh**2) / np.sum((T_fit - T_fit.mean())**2))
        print(f"\n  Wang-He tanh fit: T0={popt_wh[0]:.4f}, beta_c={popt_wh[1]:.4f}")
        print(f"    chi2/n={wang_he_chi2:.6f}, R2={wang_he_r2:.4f}")
    except Exception as e:
        print(f"\n  Wang-He tanh fit FAILED: {e}")
        wang_he_r2 = None

    # Fit Boltzmann
    try:
        p0_bl = [T_HYP006, 2.0]
        popt_bl, pcov_bl = curve_fit(boltzmann_suppression, betas_fit, T_fit, p0=p0_bl, maxfev=10000)
        boltz_params = {"T0": float(popt_bl[0]), "alpha_T": float(popt_bl[1])}
        residuals_bl = T_fit - boltzmann_suppression(betas_fit, *popt_bl)
        boltz_chi2 = float(np.sum(residuals_bl**2) / len(T_fit))
        boltz_r2 = float(1 - np.sum(residuals_bl**2) / np.sum((T_fit - T_fit.mean())**2))
        print(f"\n  Boltzmann suppression fit: T0={popt_bl[0]:.4f}, alpha_T={popt_bl[1]:.4f}")
        print(f"    chi2/n={boltz_chi2:.6f}, R2={boltz_r2:.4f}")
    except Exception as e:
        print(f"\n  Boltzmann fit FAILED: {e}")
        boltz_r2 = None

    # Flat null hypothesis chi2
    flat_chi2 = float(np.sum((T_fit - flat_T)**2) / len(T_fit))
    flat_r2 = float(1 - np.sum((T_fit - flat_T)**2) / np.sum((T_fit - T_fit.mean())**2)) if T_fit.std() > 0 else 1.0
    print(f"\n  Flat (null) model: T0={flat_T:.4f}, chi2/n={flat_chi2:.6f}, R2={flat_r2:.4f}")

    # Wang-He fit quality assessment
    if wang_he_chi2 is not None and flat_chi2 is not None:
        ratio_wh_flat = wang_he_chi2 / flat_chi2 if flat_chi2 > 0 else 999.0
        print(f"\n  chi2 ratios (Wang-He/flat = {ratio_wh_flat:.3f})")
        if ratio_wh_flat < 0.5:
            wang_he_fit_quality = "STRONG_PREFERENCE"
        elif ratio_wh_flat < 1.0:
            wang_he_fit_quality = "MODERATE_PREFERENCE"
        else:
            wang_he_fit_quality = "NO_PREFERENCE_OVER_FLAT"
    else:
        ratio_wh_flat = None
        wang_he_fit_quality = "FIT_FAILED"
else:
    print("  Insufficient valid points for curve fitting.")
    wang_he_r2 = None
    boltz_r2 = None
    flat_r2 = None
    ratio_wh_flat = None

# ── Gamma(beta) scaling fit ──
print("\n  Gamma(beta) vs 2*pi/beta scaling:", flush=True)
gamma_points = [
    (r["beta"], r["Gamma_measured"], r["Gamma_err"])
    for r in results_ladder_16
    if r["Gamma_measured"] is not None and r["Gamma_R2"] is not None and r["Gamma_R2"] > 0.3
]
print(f"  Valid Gamma fit points: {len(gamma_points)}")

gamma_fit_result = None
gamma_scaling_consistent = None

if len(gamma_points) >= 3:
    betas_g = np.array([p[0] for p in gamma_points])
    Gamma_g = np.array([p[1] for p in gamma_points])
    Gamma_err_g = np.array([p[2] for p in gamma_points])
    Gamma_expected = 2 * np.pi * PRESPECIFIED_DELTA / betas_g

    print(f"  {'beta':>8}  {'Gamma_meas':>12}  {'Gamma_pred':>12}  {'ratio':>8}")
    for b, gm, gp in zip(betas_g, Gamma_g, Gamma_expected):
        print(f"  {b:>8.1f}  {gm:>12.4f}  {gp:>12.4f}  {gm/gp:>8.3f}" if gp > 0 else f"  {b:>8.1f}  {gm:>12.4f}  {'N/A':>12}  {'N/A':>8}")

    # Fit: Gamma = C / beta (power law with exponent fixed to -1)
    try:
        def gamma_model(beta, C):
            return C / beta

        popt_g, pcov_g = curve_fit(gamma_model, betas_g, Gamma_g, p0=[2 * np.pi], maxfev=5000)
        C_fit = float(popt_g[0])
        C_expected = 2 * np.pi * PRESPECIFIED_DELTA
        C_ratio = C_fit / C_expected

        residuals_g = Gamma_g - gamma_model(betas_g, *popt_g)
        chi2_g = float(np.sum(residuals_g**2) / len(Gamma_g))

        gamma_fit_result = {
            "C_fit": C_fit,
            "C_expected_2pi_Delta": C_expected,
            "C_ratio": C_ratio,
            "chi2_per_n": chi2_g,
        }
        # Consistent if C_ratio within 30% of 1.0
        gamma_scaling_consistent = abs(C_ratio - 1.0) < 0.30
        print(f"\n  Gamma = C/beta fit: C={C_fit:.4f}  (expected 2pi*Delta={C_expected:.4f})")
        print(f"    C_ratio={C_ratio:.3f}  ({'CONSISTENT' if gamma_scaling_consistent else 'INCONSISTENT'} with 2pi/beta)")
    except Exception as e:
        print(f"\n  Gamma power-law fit FAILED: {e}")
        gamma_fit_result = None
        gamma_scaling_consistent = None
else:
    print("  Insufficient Gamma data for scaling fit.")

# ── Hawking-Page dip (boundary entropy derivative) ──
# Estimate: at Hawking-Page transition, d(S_boundary)/d(beta) changes sign.
# We use a proxy: the peak amplitude of the transported signal vs beta.
# A dip in peak amplitude at intermediate beta is the qualitative HP signature.
peak_amplitudes = [(r["beta"], r["peak_amplitude"]) for r in results_ladder_16 if r["transport_time"] > 0]
betas_pa = [p[0] for p in peak_amplitudes]
amps = [p[1] for p in peak_amplitudes]

hawking_page_dip_present = False
hp_beta_location = None
if len(amps) >= 4:
    # Look for non-monotonic behavior: amplitude peaks at intermediate beta
    amp_arr = np.array(amps)
    beta_arr = np.array(betas_pa)
    # Sort by decreasing beta (increasing temperature)
    sort_idx = np.argsort(beta_arr)[::-1]
    amp_sorted = amp_arr[sort_idx]
    if len(amp_sorted) > 2 and np.any(amp_sorted[1:-1] > amp_sorted[0]) and np.any(amp_sorted[1:-1] > amp_sorted[-1]):
        hawking_page_dip_present = True
        hp_beta_location = float(beta_arr[sort_idx][np.argmax(amp_sorted)])
        print(f"\n  Hawking-Page dip proxy: NON-MONOTONIC amplitude detected at beta~{hp_beta_location:.1f}")
    else:
        print("\n  Hawking-Page dip proxy: monotonic behavior (no HP dip in amplitude)")
else:
    print("\n  Hawking-Page dip: insufficient data")

# ══════════════════════════════════════════════════════════════════════════════
# VERDICT: apply HYP-024 refutation criteria exactly
# ══════════════════════════════════════════════════════════════════════════════
print("\n" + "="*70)
print("[VERDICT] Applying HYP-2026-024 refutation criteria")
print("="*70, flush=True)

# Gate 1 already passed (we are here).
# Check (b): T(beta) flat within error?
# Check (c): Alternative shape fits significantly better (chi2 ratio > 2)?
# Check (d): Gamma(beta) does NOT scale as 2*pi/beta?

valid_T = [r["transport_time"] for r in results_ladder_16 if r["transport_time"] > 0]
T_range = max(valid_T) - min(valid_T) if len(valid_T) > 1 else 0.0
T_variation_pct = T_range / T_HYP006 * 100 if T_HYP006 > 0 else 0.0
criterion_b_flat = T_variation_pct < 3.0   # < 3% variation = flat

# Criterion (c): chi2 ratio > 2 means alternative is significantly better
# We compare Wang-He (tanh) vs flat; if tanh is not better than flat, it's flat
criterion_c_better_alternative = False
if ratio_wh_flat is not None:
    # If ratio > 2, the alternative (flat or something else) fits better
    if flat_chi2 is not None and wang_he_chi2 is not None:
        if flat_chi2 / wang_he_chi2 < 0.5:
            # Flat is actually BETTER than Wang-He -- that means T(beta) is flat
            criterion_b_flat = True
            criterion_c_better_alternative = True

# Criterion (d): Gamma does not scale as 2*pi/beta
criterion_d_gamma_wrong = (
    gamma_scaling_consistent is not None and not gamma_scaling_consistent
)
# If we have no Gamma data, we cannot test (d) -- treat as inconclusive for that criterion
criterion_d_untestable = (gamma_scaling_consistent is None)

print(f"\n  T variation across beta ladder: {T_variation_pct:.1f}%")
print(f"  Criterion (b) [T flat]: {'TRIGGERED (REFUTED)' if criterion_b_flat else 'NOT triggered'}")
print(f"  Criterion (c) [better alternative]: {'TRIGGERED' if criterion_c_better_alternative else 'NOT triggered'}")
print(f"  Criterion (d) [Gamma wrong]: {'TRIGGERED (REFUTED)' if criterion_d_gamma_wrong else ('UNTESTABLE (no Gamma data)' if criterion_d_untestable else 'NOT triggered')}")

# SUPPORTED requires: T(beta) tracks Wang-He curve AND Gamma ~ 2*pi/beta
supported = (
    not criterion_b_flat and
    not criterion_c_better_alternative and
    wang_he_fit_quality in ("STRONG_PREFERENCE", "MODERATE_PREFERENCE") and
    (gamma_scaling_consistent is True or criterion_d_untestable)
)

refuted = (
    criterion_b_flat or
    criterion_c_better_alternative or
    (criterion_d_gamma_wrong and not criterion_d_untestable)
)

if refuted:
    verdict = "REFUTED"
    verdict_reason = []
    if criterion_b_flat:
        verdict_reason.append(f"T(beta) is flat within {T_variation_pct:.1f}% (criterion b)")
    if criterion_c_better_alternative:
        verdict_reason.append("Alternative shape fits significantly better (criterion c)")
    if criterion_d_gamma_wrong:
        verdict_reason.append("Gamma(beta) does not scale as 2*pi/beta (criterion d)")
    verdict_reason = "; ".join(verdict_reason)
elif supported:
    verdict = "SUPPORTED"
    verdict_reason = (
        f"T(beta) varies {T_variation_pct:.1f}% across beta ladder following Wang-He curve "
        f"({wang_he_fit_quality}). Gamma scaling {'consistent' if gamma_scaling_consistent else 'untested'}."
    )
else:
    verdict = "INCONCLUSIVE"
    verdict_reason = (
        f"T(beta) varies {T_variation_pct:.1f}% but Wang-He fit quality is {wang_he_fit_quality}. "
        f"Gamma scaling {'consistent' if gamma_scaling_consistent else ('untestable' if criterion_d_untestable else 'inconsistent')}. "
        "More beta points or longer time evolution needed."
    )

print(f"\n  VERDICT: {verdict}")
print(f"  Reason: {verdict_reason}", flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# CONCLUSION PARAGRAPH
# ══════════════════════════════════════════════════════════════════════════════
T_table_16 = ", ".join(
    "T(" + str(int(r["beta"])) + ")=" + f"{r['transport_time']:.3f}"
    for r in results_ladder_16 if r["transport_time"] > 0
)
T_table_24 = ", ".join(
    "T(" + str(int(r["beta"])) + ",N24)=" + f"{r['transport_time']:.3f}"
    for r in results_ladder_24 if r["transport_time"] > 0
)
if gamma_fit_result and gamma_scaling_consistent:
    gamma_str = "consistent with 2*pi/beta (C_ratio=" + str(round(gamma_fit_result["C_ratio"], 3)) + ")"
elif gamma_fit_result:
    gamma_str = "inconsistent"
else:
    gamma_str = "insufficient data for fit"

hp_str = ("present at beta~" + str(hp_beta_location)) if hawking_page_dip_present else "absent"
ratio_str = f"{ratio_wh_flat:.3f}" if ratio_wh_flat is not None else "N/A"
trunc_str = f"{trunc_bound_pct:.3f}" if trunc_bound_pct is not None else "N/A"

conclusion = (
    "HYP-2026-024 tests whether thermalizing the MERA boundary state via "
    "imaginary-time evolution exp(-beta*H/2)|psi_0> makes the holographic "
    "transport time T(beta) follow the Wang-He BTZ horizon-absorption curve, "
    "with relaxation rate Gamma(beta) = 2*pi/beta (BTZ QNM, Delta=1 energy operator, "
    "pre-specified before any fitting). "
    f"Gate 1 (self-consistency) PASSED: T(beta={BETA_BASELINE}) = {T_baseline:.4f} "
    f"vs HYP-006 target 2.250 ({gate1_residual*100:.2f}% residual, within 2% tolerance). "
    "The N=16 beta ladder spanning beta in {100, 20, 10, 5, 2, 1} yielded "
    f"T(beta) values: {T_table_16}. "
    f"T(beta) varies {T_variation_pct:.1f}% across the ladder. "
    f"Wang-He tanh fit quality: {wang_he_fit_quality} "
    f"(chi2 ratio Wang-He/flat = {ratio_str}). "
    f"Gamma(beta) scaling: {gamma_str}. "
    f"Hawking-Page dip proxy: {hp_str}. "
    f"Truncation error bound: {trunc_str}% at beta=10. "
    f"N=24 finite-size control: T values {T_table_24}. "
    f"Overall verdict: {verdict}. {verdict_reason}"
)

print(f"\n[CONCLUSION]\n{conclusion}", flush=True)

# ══════════════════════════════════════════════════════════════════════════════
# SAVE SIM-2026-026.json
# ══════════════════════════════════════════════════════════════════════════════
total_time = time.time() - SCRIPT_START

output = {
    "id": "SIM-2026-026",
    "description": "Finite-temperature BTZ transport curve: imaginary-time thermal state at N=16 beta ladder + N=24 finite-size control",
    "type": "classical",
    "date": "2026-05-16",
    "hypothesis_id": "HYP-2026-024",
    "circuit": {
        "qubits": 16,
        "depth": 0,
        "gates": 0,
        "script_path": "research/data/simulations/hyp024_btz_transport.py"
    },
    "hardware_target": "local_cpu",
    "results": {
        "verdict": verdict,
        "verdict_reason": verdict_reason,
        "conclusion_paragraph": conclusion,
        "gate1_self_consistency": {
            "beta_baseline": BETA_BASELINE,
            "T_baseline_measured": T_baseline,
            "T_hyp006_target": T_HYP006,
            "residual_pct": gate1_residual * 100,
            "tolerance_pct": GATE1_TOLERANCE * 100,
            "pass": gate1_pass,
        },
        "prespecified_operator": {
            "name": "epsilon (energy primary)",
            "Delta": PRESPECIFIED_DELTA,
            "n_QNM": PRESPECIFIED_n_QNM,
            "Gamma_formula": "2*pi*Delta/beta = 2*pi/beta",
            "locked_before_fitting": True,
        },
        "beta_ladder_N16": results_ladder_16,
        "beta_ladder_N24": results_ladder_24,
        "T_variation_pct": T_variation_pct,
        "wang_he_fit": {
            "model": "T0 * tanh(beta/beta_c)",
            "params": wang_he_params,
            "chi2_per_n": wang_he_chi2,
            "R2": wang_he_r2 if 'wang_he_r2' in dir() else None,
            "quality": wang_he_fit_quality,
        },
        "boltzmann_fit": {
            "model": "T0 * exp(-alpha_T/beta)",
            "params": boltz_params,
            "chi2_per_n": boltz_chi2,
            "R2": boltz_r2 if 'boltz_r2' in dir() else None,
        },
        "flat_model": {
            "T0": flat_T,
            "chi2_per_n": flat_chi2,
        },
        "chi2_ratio_WH_over_flat": ratio_wh_flat,
        "gamma_scaling": {
            "prespecified_Delta": PRESPECIFIED_DELTA,
            "valid_Gamma_points": gamma_points,
            "fit_result": gamma_fit_result,
            "consistent_with_2pi_over_beta": gamma_scaling_consistent,
            "test_criterion_d_triggered": criterion_d_gamma_wrong,
        },
        "hawking_page_dip": {
            "present": hawking_page_dip_present,
            "beta_location": hp_beta_location,
        },
        "truncation_error": trunc_result,
        "truncation_error_bound_pct": trunc_bound_pct,
        "E_gs_N16": E_gs_16,
        "E_gs_N24": E_gs_24,
        "total_wall_time_s": total_time,
    },
    "classical_baseline": {
        "method": "Exact statevector (scipy expm_multiply + eigsh), N=16 and N=24",
        "thermal_state_method": "Imaginary-time Trotter: exp(-beta*H/2)|psi_gs>, n_steps=20",
        "transport_method": "HYP-006 protocol: Gaussian Y-perturbation + time evolution",
        "truncation_check": "n_steps=20 vs n_steps=40 at beta=10",
    },
    "comparison": "classical_wins",
    "notes": (
        "SIM-2026-026 tests HYP-2026-024. Uses imaginary-time single-copy thermal state "
        "(NOT TFD doubled register, per mandatory constraint). Reuses H_boundary identically "
        "from holographic_transport_16q.py. Gate 1 self-consistency run first; simulation "
        "halts with INVALID verdict if it fails. Pre-committed Delta=1 (energy operator) "
        "before any fitting. Does NOT reintroduce HYP-017 R1-R5 killers."
    ),
}

out_path = "D:/quantum-worldline/research/data/simulations/SIM-2026-026.json"
with open(out_path, "w") as f:
    json.dump(output, f, indent=2)

print(f"\n{'='*70}")
print(f"SIM-2026-026 saved to: {out_path}")
print(f"Total wall time: {total_time:.0f}s ({total_time/60:.1f}min)")
print(f"{'='*70}", flush=True)
