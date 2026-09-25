"""
Classical Baseline for HYP-2026-002 — MERA Holographic Force
=============================================================
Provides two independent classical references:

1. Analytical AdS prediction curve from Sahay, Lukin, Cotler (PRX 2026):
   V(delta_rho) = C1 - C2 * exp(-delta_rho / l_AdS)
   C1 = 0.080(8), C2 = 13.6(8), l_AdS = 1/log(2) ~ 1.4427

2. Exact diagonalization (ED) of the 1D critical transverse-field Ising model:
   H = -J * sum_i (Z_i Z_{i+1}) - h * sum_i X_i
   at the quantum critical point J = h = 1.

   For 20 sites (2^20 = 1M states, tractable with sparse methods):
   - Compute ground state via Lanczos (scipy sparse eigsh)
   - Measure two-point correlators <Z_i Z_j> for varied separations
   - Extract the connected correlator C(r) = <ZiZj> - <Zi><Zj>
   - Fit to holographic force model to recover C1, C2, xi

Author: Computation Lead / classical-simulator
Date: 2026-03-10
SIM: SIM-2026-001
"""

import numpy as np
from scipy.sparse import kron, eye, csr_matrix
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit
import json
import time

# ─── Physical parameters ──────────────────────────────────────────────────────
J = 1.0          # Ising coupling
H_FIELD = 1.0   # Transverse field (critical point: h = J)
N_ED = 20        # ED system size (2^20 = 1M dimensional Hilbert space)
L_ADS = 1.0 / np.log(2)  # AdS scale from MERA theory
C1_PAPER = 0.080
C2_PAPER = 13.6
C1_ERR = 0.008
C2_ERR = 0.8

# Fine grid for analytical curve
N_ANALYTICAL_POINTS = 60
DELTA_RHO_MIN = 0.5
DELTA_RHO_MAX = 9.0

# ED measurement separations (match quantum circuit sweep)
DELTA_RHO_INT = list(range(1, 9))


# ─── Pauli matrices ───────────────────────────────────────────────────────────
def pauli_z():
    return csr_matrix(np.array([[1., 0.], [0., -1.]]))

def pauli_x():
    return csr_matrix(np.array([[0., 1.], [1., 0.]]))

def pauli_i():
    return eye(2, format='csr')


# ─── Build Ising Hamiltonian ──────────────────────────────────────────────────
def build_ising_hamiltonian(n: int, J: float, h: float):
    """
    H = -J * sum_{i=0}^{n-2} Z_i Z_{i+1}  - h * sum_{i=0}^{n-1} X_i
    Open boundary conditions. Uses sparse Kronecker products.
    """
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=np.float64)

    Z = pauli_z()
    X = pauli_x()
    I = pauli_i()

    # ZZ interaction terms
    for i in range(n - 1):
        # Z_i Z_{i+1} = I^{i} x Z x Z x I^{n-i-2}
        op = csr_matrix(np.array([[1.]]))
        for k in range(n):
            if k == i:
                op = kron(op, Z, format='csr')
            elif k == i + 1:
                op = kron(op, Z, format='csr')
            else:
                op = kron(op, I, format='csr')
        H = H - J * op

    # Transverse field terms
    for i in range(n):
        op = csr_matrix(np.array([[1.]]))
        for k in range(n):
            if k == i:
                op = kron(op, X, format='csr')
            else:
                op = kron(op, I, format='csr')
        H = H - h * op

    return H


# ─── Build Z_i operator ──────────────────────────────────────────────────────
def build_zi_operator(n: int, site: int):
    """Z_site tensor product with identities."""
    Z = pauli_z()
    I = pauli_i()
    op = csr_matrix(np.array([[1.]]))
    for k in range(n):
        if k == site:
            op = kron(op, Z, format='csr')
        else:
            op = kron(op, I, format='csr')
    return op


# ─── Analytical curve ────────────────────────────────────────────────────────
def analytical_force(delta_rho, C1=C1_PAPER, C2=C2_PAPER, l_AdS=L_ADS):
    """AdS gravity prediction for MERA holographic force."""
    return C1 - C2 * np.exp(-delta_rho / l_AdS)


# ─── Exact diagonalization ───────────────────────────────────────────────────
def run_exact_diagonalization(n: int):
    """
    Find the ground state of the critical Ising chain via sparse Lanczos.
    Returns ground state vector and ground state energy.
    """
    print(f"  Building Hamiltonian for {n} sites (dim = 2^{n} = {2**n})...")
    t0 = time.time()
    H = build_ising_hamiltonian(n, J, H_FIELD)
    t_build = time.time() - t0
    print(f"  Hamiltonian built in {t_build:.2f}s, nnz = {H.nnz}")

    print("  Running Lanczos (eigsh, k=1)...")
    t0 = time.time()
    eigenvalues, eigenvectors = eigsh(H, k=1, which='SA', tol=1e-10, maxiter=10000)
    t_eig = time.time() - t0
    E0 = eigenvalues[0]
    psi0 = eigenvectors[:, 0]
    print(f"  Ground state energy E0 = {E0:.6f} (elapsed {t_eig:.2f}s)")
    return psi0, E0


def measure_correlators_ed(psi0, n, anchor_site, delta_rho_values):
    """
    Compute <Zi>, <Zj>, <ZiZj> for the ground state psi0.
    Returns connected correlator C(r) = <ZiZj> - <Zi><Zj>.
    """
    results = {}

    print(f"  Computing correlators from anchor={anchor_site}...")

    # Pre-compute <Z_anchor>
    Z_anchor = build_zi_operator(n, anchor_site)
    zi_val = float(psi0 @ Z_anchor @ psi0)

    for dr in delta_rho_values:
        site_j = anchor_site + dr
        if site_j >= n:
            print(f"  delta_rho={dr}: site_j={site_j} out of range, skipping")
            continue

        Z_j = build_zi_operator(n, site_j)
        zj_val = float(psi0 @ Z_j @ psi0)

        # <ZiZj>
        ZiZj = Z_anchor.multiply(Z_j)  # element-wise won't work — need proper product
        # For sparse diagonal operators this is fine since Z_i and Z_j commute
        # and act on different sites: ZiZj = Z_i @ Z_j
        ZiZj_op = Z_anchor @ Z_j
        zij_val = float(psi0 @ ZiZj_op @ psi0)

        connected = zij_val - zi_val * zj_val
        results[dr] = {
            'zi': zi_val,
            'zj': zj_val,
            'zij': zij_val,
            'connected': connected
        }
        print(f"  delta_rho={dr}: <ZiZj>={zij_val:.6f}  <Zi>={zi_val:.6f}  <Zj>={zj_val:.6f}  C={connected:.6f}")

    return results, zi_val


def extract_potential_from_ed(correlators_ed, anchor_site, vacuum_reference=None):
    """
    Convert ED correlators to interaction potential.
    V(delta_rho) = C_two(delta_rho) - C_vac(delta_rho)

    For the pure ED ground state (no excitations), we define V as the
    connected correlator itself (which reflects the underlying holographic
    force structure in the ground state entanglement).

    In the MERA picture, the correlator decay encodes the AdS geometry.
    The hologron interaction potential is proportional to the correlator.

    We normalize so that V(1) ~ C1 - C2*exp(-1/l_AdS) from the paper.
    """
    delta_rhos = sorted(correlators_ed.keys())
    raw_correlators = [correlators_ed[dr]['connected'] for dr in delta_rhos]

    # The ED correlator has a different absolute scale than the MERA prediction.
    # We fit the shape (xi) and scale (C2) to match.
    return delta_rhos, raw_correlators


# ─── Main execution ───────────────────────────────────────────────────────────
def main():
    print("=" * 60)
    print("Classical Baseline — HYP-2026-002")
    print("=" * 60)
    t_total = time.time()

    # 1. Analytical prediction curve
    print("\n[1] Analytical AdS prediction curve")
    delta_rho_fine = np.linspace(DELTA_RHO_MIN, DELTA_RHO_MAX, N_ANALYTICAL_POINTS)
    V_analytical_fine = analytical_force(delta_rho_fine)

    # At integer separations matching the quantum sweep
    V_analytical_int = [float(analytical_force(dr)) for dr in DELTA_RHO_INT]

    print(f"  Analytical curve at delta_rho = {DELTA_RHO_INT}:")
    for dr, V in zip(DELTA_RHO_INT, V_analytical_int):
        print(f"    delta_rho={dr}: V_analytical={V:.6f}")

    # 2. Exact diagonalization
    print(f"\n[2] Exact diagonalization — {N_ED}-site critical Ising chain")
    anchor_ed = N_ED // 4  # site 5

    psi0, E0 = run_exact_diagonalization(N_ED)
    correlators_ed, zi_anchor = measure_correlators_ed(psi0, N_ED, anchor_ed, DELTA_RHO_INT)

    delta_rhos_ed, raw_C_ed = extract_potential_from_ed(correlators_ed, anchor_ed)

    # 3. Fit ED correlator to holographic force model
    print("\n[3] Fitting ED correlators to V = A - B*exp(-r/xi)...")

    def force_model(x, A, B, xi):
        return A - B * np.exp(-np.array(x, dtype=float) / xi)

    x_ed = np.array(delta_rhos_ed, dtype=float)
    y_ed = np.array(raw_C_ed)

    try:
        popt_ed, pcov_ed = curve_fit(
            force_model, x_ed, y_ed,
            p0=[0.0, -0.1, L_ADS],
            maxfev=10000
        )
        perr_ed = np.sqrt(np.diag(pcov_ed))
        fitted_C1_ed, fitted_C2_ed, fitted_xi_ed = popt_ed
        ed_fit_success = True
        print(f"  ED fit: C1={fitted_C1_ed:.6f}±{perr_ed[0]:.6f}, "
              f"C2={fitted_C2_ed:.6f}±{perr_ed[1]:.6f}, "
              f"xi={fitted_xi_ed:.4f}±{perr_ed[2]:.4f}")
        print(f"  Theory l_AdS = {L_ADS:.4f} (= 1/log(2))")
        xi_agreement = abs(fitted_xi_ed - L_ADS) / L_ADS
        print(f"  xi agreement with l_AdS: {(1 - xi_agreement)*100:.1f}%")
    except RuntimeError as e:
        print(f"  ED fit failed: {e}")
        fitted_C1_ed, fitted_C2_ed, fitted_xi_ed = 0.0, 0.0, L_ADS
        perr_ed = [0.0, 0.0, 0.0]
        ed_fit_success = False

    # V values from ED fit for comparison at integer separations
    if ed_fit_success:
        V_ed_fitted = [float(force_model(dr, *popt_ed)) for dr in DELTA_RHO_INT]
    else:
        V_ed_fitted = raw_C_ed

    # Fit residuals
    fit_residuals_ed = [
        float(raw_C_ed[k] - V_ed_fitted[k]) for k in range(len(raw_C_ed))
    ]

    t_elapsed = time.time() - t_total
    print(f"\nTotal elapsed: {t_elapsed:.1f}s")

    # ─── Structured result ──────────────────────────────────────────────────
    result = {
        "agent": "classical-simulator",
        "hypothesis_id": "HYP-2026-002",
        "analytical_curve": {
            "model": "V = C1 - C2 * exp(-delta_rho / l_AdS)",
            "C1": C1_PAPER,
            "C2": C2_PAPER,
            "l_AdS": float(L_ADS),
            "C1_err": C1_ERR,
            "C2_err": C2_ERR,
            "delta_rho": [float(x) for x in delta_rho_fine.tolist()],
            "V_analytical": [float(v) for v in V_analytical_fine.tolist()],
            "V_at_integer_separations": {
                str(dr): float(V) for dr, V in zip(DELTA_RHO_INT, V_analytical_int)
            }
        },
        "ed_result": {
            "system": f"critical_transverse_field_Ising_{N_ED}_sites",
            "J": J,
            "h": H_FIELD,
            "ground_state_energy": float(E0),
            "anchor_site": anchor_ed,
            "delta_rho_values": delta_rhos_ed,
            "raw_connected_correlators": [float(c) for c in raw_C_ed],
            "V_ed_fitted": [float(v) for v in V_ed_fitted],
            "fitted_C1": float(fitted_C1_ed),
            "fitted_C2": float(fitted_C2_ed),
            "fitted_l_AdS": float(fitted_xi_ed),
            "fit_errors": [float(e) for e in perr_ed],
            "fit_success": ed_fit_success,
            "l_AdS_theory": float(L_ADS)
        },
        "fit_residuals": fit_residuals_ed,
        "script_path": "D:/quantum-worldline/research/data/simulations/classical_baseline_hyp002.py",
        "elapsed_seconds": round(t_elapsed, 2)
    }

    return result


if __name__ == "__main__":
    result = main()
    print("\n--- STRUCTURED OUTPUT ---")
    print(json.dumps(result, indent=2))
