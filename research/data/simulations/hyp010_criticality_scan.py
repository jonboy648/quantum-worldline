"""
HYP-2026-010: J/Omega Criticality Scan
Tests whether the holographic transport time residual scales with l_AdS^2
by detuning the TFIM away from criticality.

Two approaches:
  A) Wang & He boundary Hamiltonian + mass detuning delta*sum(Z_i)
  B) Standard TFIM: H = -sum Z_i Z_{i+1} - g sum X_i (PBC)

Same perturbation protocol as HYP-2026-006 (Y-coupled Gaussian pulse).
Runs locally on CPU. ~15 min total.
"""
import numpy as np
import time
import json
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh, expm_multiply

L = 16
T_GLOBAL = time.time()

# Pauli matrices
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


def sparse_pauli(n, i, p):
    """Single Pauli on site i in n-qubit system, sparse."""
    I2s = speye(2, format="csr")
    paulis = {"I": I2s, "X": csr_matrix(X), "Y": csr_matrix(Y), "Z": csr_matrix(Z)}
    mats = [paulis[p] if k == i else I2s for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_wang_he(n):
    """Wang & He boundary H: H = L/(4*pi) sum [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}] (PBC)"""
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=complex)
    prefactor = n / (4 * np.pi)
    for j in range(n):
        jm1 = (j - 1) % n
        jp1 = (j + 1) % n
        H += prefactor * (
            sparse_pauli(n, jm1, "X") @ sparse_pauli(n, j, "Z") @ sparse_pauli(n, jp1, "X")
            - sparse_pauli(n, j, "X") @ sparse_pauli(n, jp1, "X")
        )
    return H


def build_tfim(n, g):
    """Standard TFIM: H = -sum Z_i Z_{i+1} - g sum X_i (PBC)"""
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=complex)
    for i in range(n):
        ip1 = (i + 1) % n
        H -= sparse_pauli(n, i, "Z") @ sparse_pauli(n, ip1, "Z")
        H -= g * sparse_pauli(n, i, "X")
    return H


def half_chain_entropy(psi, n):
    """Entanglement entropy for half-chain bipartition."""
    n_half = n // 2
    psi_matrix = psi.reshape(2 ** n_half, 2 ** (n - n_half))
    s = np.linalg.svd(psi_matrix, compute_uv=False)
    s = s[s > 1e-15]
    p = s ** 2
    return -np.sum(p * np.log(p))


# Perturbation parameters (same as HYP-2026-006)
OMEGA_PERT = 5.0
M_ANG = 0
SIGMA_T = 0.4
SIGMA_PHI = 0.4
dt = 0.05
t_max = 6.0
n_steps = int(t_max / dt)
times = np.arange(n_steps + 1) * dt

phi = np.array([2 * np.pi * i / L - 3 * np.pi / 4 for i in range(L)])
A_PERT = np.sqrt(2 * L / (SIGMA_T * SIGMA_PHI)) / (40 * np.pi)

# Precompute J_i(t)
J_matrix = np.zeros((n_steps + 1, L), dtype=complex)
for step in range(n_steps + 1):
    t = times[step]
    for i in range(L):
        J_matrix[step, i] = A_PERT * np.exp(
            -t ** 2 / (2 * SIGMA_T ** 2)
            - phi[i] ** 2 / (2 * SIGMA_PHI ** 2)
            - 1j * OMEGA_PERT * t
            + 1j * M_ANG * phi[i]
        )

# Build Y operators once
Y_ops = [sparse_pauli(L, i, "Y") for i in range(L)]

# Sum of Z_i for mass detuning
Z_sum = sum(sparse_pauli(L, i, "Z") for i in range(L))

# Baseline predictions
l_AdS_crit = 1.0 / np.log(2)
T_pred_null = (np.pi / 2) * l_AdS_crit  # 2.266


def run_transport(H, label, extra_info=None):
    """Run the transport protocol on a given Hamiltonian. Returns result dict."""
    t0 = time.time()

    # Ground state
    E_gs, psi_gs = eigsh(H, k=1, which="SA")
    E_gs = E_gs[0]
    psi_gs = psi_gs[:, 0]
    S_half = half_chain_entropy(psi_gs, L)

    # Time evolution
    psi = psi_gs.copy().astype(complex)
    max_rho = np.zeros(n_steps + 1)

    # Initial density (should be ~0)
    for i in range(L):
        val = np.real(psi.conj() @ (Y_ops[i] @ psi)) - np.real(psi_gs.conj() @ (Y_ops[i] @ psi_gs))
        max_rho[0] = max(max_rho[0], abs(val))

    for step in range(n_steps):
        # Build perturbation
        delta_H = csr_matrix((2 ** L, 2 ** L), dtype=complex)
        for i in range(L):
            j_val = J_matrix[step, i]
            if abs(j_val) > 1e-15:
                delta_H -= np.real(j_val) * Y_ops[i]

        H_total = H + delta_H
        psi = expm_multiply(-1j * H_total * dt, psi)
        psi /= np.linalg.norm(psi)

        for i in range(L):
            val = np.real(psi.conj() @ (Y_ops[i] @ psi)) - np.real(psi_gs.conj() @ (Y_ops[i] @ psi_gs))
            max_rho[step + 1] = max(max_rho[step + 1], abs(val))

        if (step + 1) % 40 == 0:
            elapsed = time.time() - t0
            rate = (step + 1) / elapsed
            eta = (n_steps - step - 1) / rate
            print(f"    t={times[step+1]:.2f}  max|rho|={max_rho[step+1]:.6f}  "
                  f"{rate:.1f} step/s  ETA={eta:.0f}s", flush=True)

    # Extract transport signature
    peak_idx = np.argmax(max_rho[:30])
    dip_time = dip_val = reappear_time = reappear_val = transport_time = -1.0

    if peak_idx < len(max_rho) - 1:
        search_end = min(peak_idx + 60, len(max_rho))
        dip_idx = peak_idx + np.argmin(max_rho[peak_idx:search_end])
        dip_time = float(times[dip_idx])
        dip_val = float(max_rho[dip_idx])

        post_dip = max_rho[dip_idx:]
        if len(post_dip) > 10:
            reappear_idx = dip_idx + np.argmax(post_dip[5:]) + 5
            reappear_idx = min(reappear_idx, len(times) - 1)
            reappear_time = float(times[reappear_idx])
            reappear_val = float(max_rho[reappear_idx])
            transport_time = reappear_time - dip_time

    residual_pct = ((transport_time - T_pred_null) / T_pred_null * 100) if transport_time > 0 else None
    elapsed = time.time() - t0

    result = {
        "label": label,
        "E_gs": float(E_gs),
        "S_half": float(S_half),
        "peak_time": float(times[peak_idx]),
        "peak_amplitude": float(max_rho[peak_idx]),
        "dip_time": dip_time,
        "dip_amplitude": dip_val,
        "reappear_time": reappear_time,
        "reappear_amplitude": reappear_val,
        "transport_time": transport_time,
        "residual_pct": residual_pct,
        "elapsed_s": float(elapsed),
    }
    if extra_info:
        result.update(extra_info)

    print(f"  E_gs={E_gs:.6f}  S_half={S_half:.4f}")
    print(f"  Peak t={times[peak_idx]:.2f}  Dip t={dip_time:.2f} (rho={dip_val:.6f})  "
          f"Reappear t={reappear_time:.2f}")
    if residual_pct is not None:
        print(f"  T_transport={transport_time:.4f}  residual={residual_pct:.2f}%")
    else:
        print(f"  T_transport={transport_time:.4f}  residual=N/A")
    print(f"  Elapsed: {elapsed:.1f}s", flush=True)

    return result


# ==================================================================
# APPROACH A: Wang & He + mass detuning delta*sum(Z_i)
# ==================================================================
print("=" * 70)
print("HYP-2026-010: Criticality Scan")
print(f"L={L}  dt={dt}  t_max={t_max}  T_pred(null geodesic)={T_pred_null:.4f}")
print("=" * 70)

print("\n-- APPROACH A: Wang & He + mass detuning --")
H_WH = build_wang_he(L)
print(f"  H_WH built: nnz={H_WH.nnz}", flush=True)

delta_values = [-0.3, -0.2, -0.1, 0.0, 0.1, 0.2, 0.3]
results_A = []

for d_idx, delta in enumerate(delta_values):
    print(f"\n[A{d_idx + 1}/{len(delta_values)}] delta = {delta:+.1f}")
    H = H_WH + delta * Z_sum
    r = run_transport(H, f"WH_delta={delta:+.1f}", {"delta": delta, "approach": "wang_he_mass"})
    results_A.append(r)

# ==================================================================
# APPROACH B: Standard TFIM at different g = Omega/J
# ==================================================================
print("\n-- APPROACH B: Standard TFIM --")

g_values = [0.75, 0.85, 0.90, 0.95, 1.00, 1.05, 1.10]
results_B = []

for g_idx, g in enumerate(g_values):
    print(f"\n[B{g_idx + 1}/{len(g_values)}] g = Omega/J = {g:.2f}")
    H = build_tfim(L, g)
    xi = 1.0 / abs(np.log(g)) if abs(g - 1.0) > 1e-10 else float("inf")
    xi_str = f"{xi:.2f}" if xi != float("inf") else "inf"
    print(f"  xi_theory = {xi_str}  H nnz={H.nnz}")
    r = run_transport(H, f"TFIM_g={g:.2f}", {
        "g": g, "xi_theory": xi if xi != float("inf") else None, "approach": "tfim"
    })
    results_B.append(r)

# ==================================================================
# Summary
# ==================================================================
total_time = time.time() - T_GLOBAL

print(f"\n{'=' * 70}")
print("SUMMARY -- Approach A (Wang & He + detuning)")
print(f"{'delta':>6} {'T_transport':>12} {'residual%':>10} {'S_half':>8} {'dip_rho':>10}")
for r in results_A:
    res = f"{r['residual_pct']:.2f}%" if r['residual_pct'] else "N/A"
    print(f"{r['delta']:>+6.1f} {r['transport_time']:>12.4f} {res:>10} "
          f"{r['S_half']:>8.4f} {r['dip_amplitude']:>10.6f}")

print(f"\nSUMMARY -- Approach B (Standard TFIM)")
print(f"{'g':>6} {'T_transport':>12} {'residual%':>10} {'S_half':>8} {'xi':>8}")
for r in results_B:
    res = f"{r['residual_pct']:.2f}%" if r['residual_pct'] else "N/A"
    xi_str = f"{r['xi_theory']:.2f}" if r.get('xi_theory') else "inf"
    print(f"{r['g']:>6.2f} {r['transport_time']:>12.4f} {res:>10} "
          f"{r['S_half']:>8.4f} {xi_str:>8}")

# Check for l_AdS^2 scaling
print(f"\nl_AdS(crit) = {l_AdS_crit:.4f}, l_AdS^2 = {l_AdS_crit**2:.4f}")
print(f"T_predicted(null) = {T_pred_null:.4f}")
print(f"Total elapsed: {total_time:.0f}s ({total_time / 60:.1f} min)")

# ==================================================================
# Save
# ==================================================================
output = {
    "experiment": "hyp2026010_criticality_scan",
    "hypothesis_id": "HYP-2026-010",
    "L": L,
    "perturbation": {
        "Omega": OMEGA_PERT, "M": M_ANG,
        "sigma_t": SIGMA_T, "sigma_phi": SIGMA_PHI,
        "A": float(A_PERT),
    },
    "time_evolution": {"dt": dt, "t_max": t_max, "n_steps": n_steps},
    "predictions": {
        "l_AdS_critical": float(l_AdS_crit),
        "T_null_geodesic": float(T_pred_null),
    },
    "approach_A_wang_he_detuning": {
        "description": "Wang & He boundary H + delta*sum(Z_i) mass detuning",
        "delta_values": delta_values,
        "results": results_A,
    },
    "approach_B_tfim": {
        "description": "Standard TFIM: H = -sum Z_i Z_{i+1} - g sum X_i (PBC)",
        "g_values": g_values,
        "results": results_B,
    },
    "total_time_s": total_time,
}

outpath = "D:/quantum-worldline/research/data/simulations/hyp010_criticality_scan.json"
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)

print(f"\nResults saved to {outpath}")
print("=" * 70)
