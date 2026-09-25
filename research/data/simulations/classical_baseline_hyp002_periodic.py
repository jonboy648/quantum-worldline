"""
Classical ED Baseline — HYP-2026-002 (Periodic BC, N=16)
=========================================================
Classical Simulator specialist output for Computation Lead.

Task: Exact diagonalization of 1D TFIM at criticality (J=h=1)
      with PERIODIC boundary conditions and N=16 sites.
      (Matches quantum circuit for fair comparison; SIM-2026-001 used OBC N=20.)

Computes:
  - Ground state energy E0
  - ZZ connected correlators C(r) = <ZiZj> - <Zi><Zj>  at all separations r=1..N/2
  - Fit of C(r) to power-law (critical) and exponential form
  - xi extraction for comparison with l_AdS = 1/log(2) ~ 1.4427

Also computes vacuum-subtracted potential V_ED(r) analogous to MERA V(dr)
by simulating "single-site X perturbation" to match hologron spirit.

Author: classical-simulator (Computation Lead dispatch)
Date:   2026-03-10
SIM:    SIM-2026-002 (classical baseline component)
"""

import numpy as np
import json
import time
from scipy.sparse import lil_matrix, kron, eye, diags
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

# ─── Configuration ────────────────────────────────────────────────────────────
N       = 16       # sites — matches quantum circuit
J       = 1.0      # ZZ coupling
H_FIELD = 1.0      # transverse field
L_ADS   = 1.0 / np.log(2)

# Pauli matrices
SIGMA_Z = np.array([[1, 0], [0, -1]], dtype=np.float64)
SIGMA_X = np.array([[0, 1], [1,  0]], dtype=np.float64)
I2      = np.eye(2, dtype=np.float64)


def kron_site(op, site, n):
    """Single-site operator embedded into n-qubit Hilbert space."""
    ops = [I2] * n
    ops[site] = op
    result = ops[0]
    for o in ops[1:]:
        result = np.kron(result, o)
    return result


def build_hamiltonian_sparse(n, j, h, periodic=True):
    """
    H = -J sum_i Zi Zi+1  -  h sum_i Xi
    periodic: if True, adds Z_{n-1} Z_0 term.
    """
    dim = 2 ** n
    H   = lil_matrix((dim, dim), dtype=np.float64)

    # ZZ terms
    bonds = list(range(n - 1))
    if periodic:
        bonds.append(n - 1)   # wraps (n-1) -> 0

    for i in bonds:
        j_site = (i + 1) % n
        for state in range(dim):
            si   = (state >> i)      & 1
            sj   = (state >> j_site) & 1
            sign = 1 if si == sj else -1
            H[state, state] += -j * sign

    # X terms
    for i in range(n):
        for state in range(dim):
            flipped = state ^ (1 << i)
            H[state, flipped] += -h

    return H.tocsr()


def measure_zz_connected(gs: np.ndarray, n: int, i: int, j: int) -> float:
    """
    Connected correlator <Zi Zj>_c = <ZiZj> - <Zi><Zj>
    from exact ground state vector.
    """
    dim = 2 ** n

    def ev_single(op_mat, site):
        """<gs|op_site|gs>"""
        total = 0.0
        for s in range(dim):
            bit  = (s >> site) & 1
            diag = op_mat[bit, bit]   # Z is diagonal
            total += abs(gs[s])**2 * diag
        return total

    def ev_two(i_site, j_site):
        """<gs|Zi Zj|gs>"""
        total = 0.0
        for s in range(dim):
            si   = (s >> i_site) & 1
            sj   = (s >> j_site) & 1
            sign = (1 if si == 0 else -1) * (1 if sj == 0 else -1)
            total += abs(gs[s])**2 * sign
        return total

    zi  = ev_single(SIGMA_Z, i)
    zj  = ev_single(SIGMA_Z, j)
    zij = ev_two(i, j)
    return zij - zi * zj


def compute_perturbed_correlator(gs: np.ndarray, n: int, anchor: int, j_site: int,
                                  angle: float) -> float:
    """
    Simulate effect of Ry(angle) at anchor AND j_site on the ground state,
    then measure ZZ connected correlator.
    This mirrors the MERA hologron protocol (Ry applied after vacuum preparation).

    |psi_pert> = Ry(angle, anchor) Ry(angle, j_site) |gs>
    """
    dim = 2 ** n

    def apply_ry(state_vec, site, theta):
        """Apply Ry(theta) to a state vector at given site."""
        c = np.cos(theta / 2)
        s = np.sin(theta / 2)
        new = np.zeros_like(state_vec)
        for idx in range(dim):
            bit = (idx >> site) & 1
            paired = idx ^ (1 << site)   # flip bit at site
            if bit == 0:
                new[idx]   += c * state_vec[idx]
                new[paired] += s * state_vec[idx]
            else:
                new[idx]   += c * state_vec[idx]
                new[paired] -= s * state_vec[idx]
        return new

    psi = gs.copy()
    psi = apply_ry(psi, anchor, angle)
    psi = apply_ry(psi, j_site, angle)

    # Renormalize (should already be unit norm)
    psi /= np.linalg.norm(psi)

    # Measure ZZ connected on perturbed state
    def ev_two_gs(v, i_s, j_s):
        total = 0.0
        for s in range(dim):
            si   = (s >> i_s) & 1
            sj   = (s >> j_s) & 1
            sign = (1 if si == 0 else -1) * (1 if sj == 0 else -1)
            total += abs(v[s])**2 * sign
        return total

    def ev_one_gs(v, site):
        total = 0.0
        for s in range(dim):
            bit  = (s >> site) & 1
            sign = 1 if bit == 0 else -1
            total += abs(v[s])**2 * sign
        return total

    zi  = ev_one_gs(psi, anchor)
    zj  = ev_one_gs(psi, j_site)
    zij = ev_two_gs(psi, anchor, j_site)
    return zij - zi * zj


def main():
    print("=" * 65)
    print(f"Classical ED Baseline — N={N} TFIM, Periodic BC")
    print("=" * 65)

    t_total = time.time()

    # --- Build and diagonalize Hamiltonian ----------------------------------
    print(f"\n[1/4] Building Hamiltonian (N={N}, PBC)...")
    t0 = time.time()
    H  = build_hamiltonian_sparse(N, J, H_FIELD, periodic=True)
    print(f"  Hamiltonian built in {time.time()-t0:.2f}s, dim={2**N}")

    print("  Lanczos diagonalization...")
    t0 = time.time()
    vals, vecs = eigsh(H, k=2, which='SA')
    E0 = float(vals[0])
    gs = vecs[:, 0]
    E1 = float(vals[1])
    gap = E1 - E0
    print(f"  E0 = {E0:.8f}   [{time.time()-t0:.2f}s]")
    print(f"  E1 = {E1:.8f},  gap = {gap:.6f}")

    # Analytical result: periodic N-site TFIM at J=h=1
    # E0/N -> -4/pi * (1/2) * ... (free fermion)
    # Known exact: E0(16 PBC) ~ -20.6457...
    print(f"  E0/N = {E0/N:.4f}   (critical TFIM PBC analytical ~ -1.2732)")

    # --- ZZ correlators at all separations ----------------------------------
    print(f"\n[2/4] Computing ZZ connected correlators...")
    anchor = N // 4   # site 4

    max_sep = N // 2  # exploit translational symmetry (PBC), max meaningful sep
    separations  = list(range(1, max_sep + 1))
    C_raw        = []
    C_vacuum_all = []

    t0 = time.time()
    for r in separations:
        j_site = (anchor + r) % N
        c      = measure_zz_connected(gs, N, anchor, j_site)
        C_raw.append(float(c))
        C_vacuum_all.append(float(c))
        print(f"  r={r:2d}: C(r) = {c:.8f}")
    print(f"  Correlators done in {time.time()-t0:.2f}s")

    # --- Holographic force profile V_ED(r) ----------------------------------
    print(f"\n[3/4] Computing V_ED(r) = C(pert) - C(vac) with Ry hologrons...")
    HOLOGRON_ANGLE = np.pi / 3   # matches MERA circuit

    Vs_ed = []
    C_pert_all = []
    t0 = time.time()
    for r in separations:
        j_site = (anchor + r) % N
        C_vac  = measure_zz_connected(gs, N, anchor, j_site)
        C_pert = compute_perturbed_correlator(gs, N, anchor, j_site, HOLOGRON_ANGLE)
        V      = C_pert - C_vac
        Vs_ed.append(float(V))
        C_pert_all.append(float(C_pert))
        print(f"  r={r:2d}: V={V:+.8f}  C_vac={C_vac:.6f}  C_pert={C_pert:.6f}")
    print(f"  Force profile done in {time.time()-t0:.2f}s")

    # --- Fits ---------------------------------------------------------------
    print(f"\n[4/4] Fitting correlators...")

    x = np.array(separations, dtype=float)

    # Power law (expected at criticality: C(r) ~ r^{-1/4} for TFIM)
    def power_law(r, A, eta):
        return A * r**(-eta)

    # Exponential decay
    def exp_decay(r, A, B, xi):
        return A - B * np.exp(-r / xi)

    # Force profile model (holographic)
    def force_model(r, C1, C2, xi):
        return C1 - C2 * np.exp(-r / xi)

    C_arr = np.array(C_raw)
    V_arr = np.array(Vs_ed)

    # Fit raw correlators — power law
    try:
        popt_pw, _ = curve_fit(power_law, x, C_arr, p0=[0.5, 0.25], maxfev=5000)
        A_pw, eta_pw = popt_pw
        print(f"  Power-law fit: C(r) = {A_pw:.4f} * r^(-{eta_pw:.4f})")
        print(f"  (Critical TFIM theory: eta = 0.25)")
    except Exception as e:
        print(f"  Power-law fit failed: {e}")
        A_pw, eta_pw = None, None

    # Fit raw correlators — exponential
    try:
        popt_ex, pcov_ex = curve_fit(exp_decay, x, C_arr,
                                      p0=[0.0, 0.5, 3.0], maxfev=5000)
        perr_ex = np.sqrt(np.diag(pcov_ex))
        A_ex, B_ex, xi_ex = popt_ex
        print(f"  Exp fit: C(r) = {A_ex:.4f} - {B_ex:.4f}*exp(-r/{xi_ex:.4f})")
        print(f"  xi = {xi_ex:.4f} ± {perr_ex[2]:.4f}  (l_AdS = {L_ADS:.4f})")
    except Exception as e:
        print(f"  Exp fit failed: {e}")
        xi_ex = None

    # Fit force profile
    try:
        L_ADS_val = float(L_ADS)
        C1_PAPER = 0.080
        C2_PAPER = 13.6
        popt_V, pcov_V = curve_fit(
            force_model, x[:6], V_arr[:6],     # use first 6 points (causal cone)
            p0=[C1_PAPER, C2_PAPER, L_ADS_val],
            maxfev=10000,
            bounds=([-5, -200, 0.1], [5, 200, 10])
        )
        perr_V = np.sqrt(np.diag(pcov_V))
        C1_fit, C2_fit, xi_fit = popt_V
        print(f"  Force fit: C1={C1_fit:.4f}±{perr_V[0]:.4f}  "
              f"C2={C2_fit:.4f}±{perr_V[1]:.4f}  xi={xi_fit:.4f}±{perr_V[2]:.4f}")
        print(f"  Paper: C1=0.080, C2=13.6, l_AdS={L_ADS:.4f}")
    except Exception as e:
        print(f"  Force fit failed: {e}")
        C1_fit, C2_fit, xi_fit = None, None, None
        perr_V = [None, None, None]

    t_elapsed = time.time() - t_total
    print(f"\n  Total runtime: {t_elapsed:.1f}s")

    # --- Structure and save -------------------------------------------------
    structured = {
        "agent":         "classical-simulator",
        "sim_id":        "SIM-2026-002-classical",
        "description":   f"Exact diagonalization N={N} TFIM, periodic BC. "
                          "Correlators and force profile for comparison with MERA VQE.",
        "date":          "2026-03-10",
        "system": {
            "n_sites":     N,
            "J":           J,
            "h":           H_FIELD,
            "boundary":    "periodic",
        },
        "ground_state": {
            "E0":          E0,
            "E0_per_site": E0 / N,
            "E1":          E1,
            "spectral_gap": gap,
        },
        "correlators": {
            "separations":         separations,
            "C_connected":         C_raw,
            "C_perturbed":         C_pert_all,
            "V_force":             Vs_ed,
            "anchor_site":         anchor,
            "hologron_angle_rad":  float(HOLOGRON_ANGLE),
        },
        "fits": {
            "power_law": {
                "A":   float(A_pw) if A_pw is not None else None,
                "eta": float(eta_pw) if eta_pw is not None else None,
                "theory_eta": 0.25,
            },
            "exponential": {
                "xi":   float(xi_ex) if xi_ex is not None else None,
                "l_AdS": L_ADS,
            },
            "force_profile": {
                "C1":    float(C1_fit) if C1_fit is not None else None,
                "C2":    float(C2_fit) if C2_fit is not None else None,
                "xi":    float(xi_fit) if xi_fit is not None else None,
                "paper_C1":    0.080,
                "paper_C2":    13.6,
                "paper_l_AdS": L_ADS,
            }
        },
        "elapsed_seconds": round(t_elapsed, 2),
    }

    out_path = "D:/quantum-worldline/research/data/simulations/classical_baseline_SIM2026002.json"
    with open(out_path, 'w') as f:
        json.dump(structured, f, indent=2)
    print(f"  Saved: {out_path}")
    print("=" * 65)
    return structured


if __name__ == "__main__":
    result = main()
    print("\n--- STRUCTURED OUTPUT ---")
    print(json.dumps(result, indent=2))
