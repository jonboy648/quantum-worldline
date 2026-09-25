"""
Holographic Transportation -- 24q MERA (Wang & He, arXiv:2501.03084) [v3]
Tests Lin's 1/N finite-size correction to holographic transport time.

v3 fixes the critical RK4 integrator error from v2:
  v2 used RK4 with dt=0.05, but the H_boundary spectral radius at L=24
  is large enough that RK4 has significant phase-accumulation errors.
  v3 restores the EXACT expm_multiply approach from the original 16q script
  using a scipy LinearOperator to avoid forming H_total as a matrix.

The LinearOperator computes H_total(t) @ v = H_boundary @ v + delta_H(t) @ v
where delta_H(t) @ v = -sum_i Re(J_i(t)) * Y_i @ v is computed analytically
per site via bit-flip index arithmetic -- no sparse matrix storage needed.

This matches EXACTLY the physics of holographic_transport_16q.py which found:
  T_measured = 2.250, T_predicted = 2.266 (0.72% residual)

Lin 1/N prediction at N=24: residual ~ (0.72 * 16) / 24 = 0.48%

Memory estimate at L=24:
  H_boundary CSR: ~16 GB
  psi: 128 MB
  Total: ~18-20 GB (fits in 64 GB system)

Time estimate:
  H_boundary build (COO method): ~90s
  eigsh ground state: ~520s (~9 min)
  expm_multiply time evolution: 120 steps
    Each step: expm_multiply on 16M-dim LinearOperator
    expm_multiply uses Krylov (~30-80 matvecs per step)
    Each matvec: H_boundary @ v (~4s) + 24 analytic Y ops (~0.5s) = ~4.5s
    Per step: ~30-80 * 4.5s = 135-360s
    120 steps: ~4.5-12 hours
    --> May still be slow. Use tol=1e-6 to limit Krylov iterations.
    --> With tol, ~15-25 matvecs expected, so ~70-115s/step, 2.3-3.8 hours.

If too slow: fall back to midpoint/Crank-Nicolson (spectral-radius aware).
"""
import numpy as np
import sys, io, time, json
from scipy.sparse import coo_matrix, csr_matrix
from scipy.sparse.linalg import eigsh, expm_multiply, LinearOperator

# Fix Windows cp1252 encoding
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

print("=" * 65)
print("Holographic Transportation -- 24q v3 (expm_multiply + LinearOperator)")
print("Testing Lin 1/N finite-size correction (HYP-2026-006)")
print("=" * 65, flush=True)

L = 24
dim = 2 ** L   # 16,777,216
T_GLOBAL = time.time()

all_indices = np.arange(dim, dtype=np.int64)

# ================================================================
# 1. Build H_boundary using COO accumulation (same as v2)
#    H = L/(4*pi) * sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}]
# ================================================================
print("[1] Building H_boundary via COO accumulation...", flush=True)
t0 = time.time()

prefactor = L / (4 * np.pi)
rows_list = []
cols_list = []
data_list = []

rows_base = np.arange(dim, dtype=np.int64)

for j in range(L):
    jm1 = (j - 1) % L
    jp1 = (j + 1) % L

    bp_jm1 = L - 1 - jm1
    bp_j   = L - 1 - j
    bp_jp1 = L - 1 - jp1

    # --- 3-body term: prefactor * X_{jm1} Z_j X_{jp1} ---
    col = rows_base.copy()
    coeff = np.full(dim, prefactor, dtype=complex)
    col ^= (np.int64(1) << bp_jm1)
    bv_j = (rows_base >> bp_j) & np.int64(1)
    coeff *= (1.0 - 2.0 * bv_j)
    col ^= (np.int64(1) << bp_jp1)

    rows_list.append(rows_base.copy())
    cols_list.append(col)
    data_list.append(coeff)

    # --- 2-body term: -prefactor * X_j X_{jp1} ---
    col2 = rows_base.copy()
    coeff2 = np.full(dim, -prefactor, dtype=complex)
    col2 ^= (np.int64(1) << bp_j)
    col2 ^= (np.int64(1) << bp_jp1)

    rows_list.append(rows_base.copy())
    cols_list.append(col2)
    data_list.append(coeff2)

    if (j + 1) % 6 == 0:
        print(f"  j={j+1}/{L} done ({time.time()-t0:.1f}s)...", flush=True)

print(f"  Concatenating COO entries...", flush=True)
all_rows = np.concatenate(rows_list)
all_cols = np.concatenate(cols_list)
all_data = np.concatenate(data_list)

del rows_list, cols_list, data_list

H_boundary = coo_matrix((all_data, (all_rows, all_cols)), shape=(dim, dim)).tocsr()
H_boundary.sum_duplicates()
del all_rows, all_cols, all_data

print(f"  H_boundary: shape={H_boundary.shape}, nnz={H_boundary.nnz:,}")
print(f"  H memory: ~{(H_boundary.data.nbytes + H_boundary.indices.nbytes + H_boundary.indptr.nbytes)/1e9:.2f} GB")
print(f"  Build time: {time.time()-t0:.1f}s", flush=True)


# ================================================================
# 2. Ground state
# ================================================================
print("[2] Finding ground state (eigsh)...", flush=True)
t0 = time.time()
E_gs_arr, psi_gs_arr = eigsh(H_boundary, k=1, which="SA")
E_gs = float(E_gs_arr[0])
psi_gs = psi_gs_arr[:, 0].astype(complex)
print(f"  E_gs = {E_gs:.6f}  (took {time.time()-t0:.1f}s)", flush=True)


# ================================================================
# 3. Perturbation parameters (identical to 16q script)
# ================================================================
OMEGA = 5.0
M_ang = 0
sigma_t = 0.4
sigma_phi = 0.4

phi = np.array([2 * np.pi * i / L - 3 * np.pi / 4 for i in range(L)])
A = np.sqrt(2 * L / (sigma_t * sigma_phi)) / (40 * np.pi)

dt = 0.05
t_max = 6.0
n_steps = int(t_max / dt)
times = np.arange(n_steps + 1) * dt

print(f"[3] Perturbation: Omega={OMEGA}, M={M_ang}, sigma_t={sigma_t}, sigma_phi={sigma_phi}")
print(f"    A={A:.6f}, dt={dt}, t_max={t_max}, steps={n_steps}", flush=True)

# Precompute J_i(t) for all timesteps
J_matrix = np.zeros((n_steps + 1, L), dtype=complex)
for step in range(n_steps + 1):
    t_val = times[step]
    for i in range(L):
        J_matrix[step, i] = A * np.exp(
            -t_val**2 / (2 * sigma_t**2)
            - phi[i]**2 / (2 * sigma_phi**2)
            - 1j * OMEGA * t_val
            + 1j * M_ang * phi[i]
        )

J_real_matrix = np.real(J_matrix)  # only real part enters H


# ================================================================
# 4. Analytic Y operator and Z measurement (no sparse storage)
# ================================================================

def apply_Y_single(psi, i):
    """Y_i @ psi via bit-flip index arithmetic."""
    bp = L - 1 - i
    bm = np.int64(1) << bp
    flipped = all_indices ^ bm
    bv = (all_indices >> bp) & np.int64(1)
    y_coeff = np.where(bv == 0, 1j, -1j)
    return y_coeff * psi[flipped]


def apply_delta_H(psi, J_real_vec):
    """
    delta_H @ psi = -sum_i Re(J_i) * Y_i @ psi
    This is the perturbation contribution to H_total.
    """
    result = np.zeros(dim, dtype=complex)
    for i in range(L):
        ji = J_real_vec[i]
        if abs(ji) < 1e-14:
            continue
        result -= ji * apply_Y_single(psi, i)
    return result


def measure_Y(psi, i):
    """<psi|Y_i|psi>."""
    return float(np.real(np.dot(psi.conj(), apply_Y_single(psi, i))))


def measure_Z(psi, i):
    """<psi|Z_i|psi>."""
    bp = L - 1 - i
    bv = (all_indices >> bp) & np.int64(1)
    z_coeff = 1.0 - 2.0 * bv
    return float(np.real(np.dot(np.abs(psi)**2, z_coeff)))


# Ground state expectations
print("[4] Precomputing ground state expectations...", flush=True)
gs_Y_exp = np.array([measure_Y(psi_gs, i) for i in range(L)])
gs_Z_exp = np.array([measure_Z(psi_gs, i) for i in range(L)])
print(f"    gs <Y>: [{gs_Y_exp.min():.4f}, {gs_Y_exp.max():.4f}]")
print(f"    gs <Z>: [{gs_Z_exp.min():.4f}, {gs_Z_exp.max():.4f}]", flush=True)


# ================================================================
# 5. Time evolution using expm_multiply + LinearOperator
#
#    psi(t+dt) = exp(-i * H_total(t) * dt) @ psi(t)
#
#    H_total(t) @ v = H_boundary @ v + delta_H(t) @ v
#
#    We create a fresh LinearOperator at each step capturing the
#    current J_real_vec via a closure, then call:
#      psi_new = expm_multiply(-1j * dt * H_total_op, psi)
#
#    expm_multiply uses a Krylov subspace method internally.
#    tol=1e-8 limits Krylov steps to keep runtime manageable.
# ================================================================
print("\n[5] Time evolution (expm_multiply + LinearOperator, 120 steps)...", flush=True)
print("    Each step builds a LinearOperator and calls expm_multiply.", flush=True)


def make_matvec(J_rv):
    """Factory: returns matvec closure capturing current J_real_vec."""
    def matvec(v):
        v_c = v.astype(complex, copy=False)
        return H_boundary.dot(v_c) + apply_delta_H(v_c, J_rv)
    return matvec


def make_matmat(mv_fn):
    """Column-by-column matmat for onenormest (onenormest passes t=2 columns)."""
    def matmat(X):
        return np.column_stack([mv_fn(X[:, k]) for k in range(X.shape[1])])
    return matmat


psi = psi_gs.copy().astype(complex)
boundary_density_Y = np.zeros((n_steps + 1, L))
boundary_density_Z = np.zeros((n_steps + 1, L))

# t=0 densities (should be 0)
for i in range(L):
    boundary_density_Y[0, i] = measure_Y(psi, i) - gs_Y_exp[i]
    boundary_density_Z[0, i] = measure_Z(psi, i) - gs_Z_exp[i]

t0_evo = time.time()

for step in range(n_steps):
    t_step = float(times[step])
    J_real_vec = J_real_matrix[step]  # shape (L,)

    # Build LinearOperator for H_total(t) at this step
    # H_total(t) @ v = H_boundary @ v + delta_H(t) @ v
    mv = make_matvec(J_real_vec)
    mm = make_matmat(mv)

    # H_total is Hermitian -> rmatvec = matvec, rmatmat = matmat
    # trace(H_total) = trace(H_boundary) + trace(delta_H) = 0 + 0 = 0
    # (Y operators and XZX, XX all traceless)
    H_total_op = LinearOperator(
        shape=(dim, dim),
        matvec=mv,
        rmatvec=mv,   # H_total is Hermitian
        matmat=mm,
        rmatmat=mm,   # also Hermitian for adjoint
        dtype=complex
    )

    # Exact matrix exponential action via Krylov
    # psi_new = exp(-i * dt * H_total) @ psi
    # traceA = -i * dt * trace(H_total) = 0
    psi = expm_multiply(-1j * dt * H_total_op, psi, traceA=0.0)

    # Normalize for numerical safety
    psi /= np.linalg.norm(psi)

    # Measure boundary densities
    for i in range(L):
        boundary_density_Y[step + 1, i] = measure_Y(psi, i) - gs_Y_exp[i]
        boundary_density_Z[step + 1, i] = measure_Z(psi, i) - gs_Z_exp[i]

    elapsed = time.time() - t0_evo
    rate = (step + 1) / elapsed
    eta = (n_steps - step - 1) / rate

    if (step + 1) % 5 == 0 or step < 5:
        max_rho_Y = float(np.max(np.abs(boundary_density_Y[step + 1])))
        max_rho_Z = float(np.max(np.abs(boundary_density_Z[step + 1])))
        print(
            f"  t={times[step+1]:.2f}  max|rho_Y|={max_rho_Y:.6f}  max|rho_Z|={max_rho_Z:.6f}"
            f"  {rate:.4f} step/s  ETA={eta/3600:.2f}h",
            flush=True,
        )
    sys.stdout.flush()

sim_time = time.time() - t0_evo
print(f"  Evolution complete: {sim_time:.1f}s ({sim_time/3600:.2f}h)", flush=True)


# ================================================================
# 6. Transport signature analysis
# ================================================================
print("\n[6] Transport signature analysis:", flush=True)

max_rho_over_time = np.max(np.abs(boundary_density_Y), axis=1)

peak_idx = int(np.argmax(max_rho_over_time[:30]))

l_AdS = 1.0 / np.log(2)
T_null_predicted = (np.pi / 2) * l_AdS

if peak_idx < len(max_rho_over_time) - 5:
    search_end_dip = min(peak_idx + 70, len(max_rho_over_time))
    dip_idx = peak_idx + int(np.argmin(max_rho_over_time[peak_idx:search_end_dip]))
    dip_time = float(times[dip_idx])
    dip_val = float(max_rho_over_time[dip_idx])

    post_dip_start = dip_idx + 3
    post_dip_end = min(dip_idx + 90, len(max_rho_over_time))
    if post_dip_end > post_dip_start:
        rel_reappear = int(np.argmax(max_rho_over_time[post_dip_start:post_dip_end]))
        reappear_idx = post_dip_start + rel_reappear
        reappear_time = float(times[min(reappear_idx, len(times) - 1)])
        reappear_val = float(max_rho_over_time[min(reappear_idx, len(max_rho_over_time) - 1)])
    else:
        reappear_time = -1.0
        reappear_val = -1.0
else:
    dip_time = -1.0
    dip_val = -1.0
    reappear_time = -1.0
    reappear_val = -1.0

transport_time = reappear_time - dip_time if (dip_time > 0 and reappear_time > 0) else -1.0

if transport_time > 0:
    residual_pct = (transport_time - T_null_predicted) / T_null_predicted * 100.0
    lin_C = 0.72 * 16  # 11.52
    lin_pred_24 = lin_C / L
    lin_check = "CONSISTENT" if abs(residual_pct - lin_pred_24) < 0.30 else "INCONSISTENT"
else:
    residual_pct = None
    lin_pred_24 = 11.52 / L
    lin_check = "NO_SIGNAL"

print(f"  l_AdS = 1/ln(2) = {l_AdS:.4f}")
print(f"  T_predicted (pi/2 * l_AdS) = {T_null_predicted:.4f}")
print(f"  Peak at t={times[peak_idx]:.2f}, max|rho|={max_rho_over_time[peak_idx]:.6f}")
print(f"  Dip at t={dip_time:.2f}, max|rho|={dip_val:.6f}")
print(f"  Reappears at t={reappear_time:.2f}, max|rho|={reappear_val:.6f}")
print(f"  T_measured = {transport_time:.3f}" if transport_time > 0 else "  T_measured = NO_SIGNAL")
if residual_pct is not None:
    print(f"  Residual = {residual_pct:.3f}%  (Lin 1/N prediction: {lin_pred_24:.2f}%)")
    print(f"  Lin 1/N check: {lin_check}")


# ================================================================
# 7. Save results
# ================================================================
total_time = time.time() - T_GLOBAL

result = {
    "experiment": "holographic_transportation_24q_v3",
    "hypothesis_id": "HYP-2026-006",
    "boundary_sites": L,
    "hamiltonian": "Wang_He_H_boundary (Eq 1, PBC, L=24)",
    "integrator": "expm_multiply + LinearOperator (exact Krylov)",
    "E_gs": float(E_gs),
    "l_AdS_theory": float(l_AdS),
    "T_predicted_composite_geodesic": float(T_null_predicted),
    "perturbation": {
        "Omega": float(OMEGA), "M": int(M_ang),
        "sigma_t": float(sigma_t), "sigma_phi": float(sigma_phi),
        "A": float(A),
    },
    "time_evolution": {
        "dt": float(dt), "t_max": float(t_max), "n_steps": int(n_steps),
        "sim_time_s": float(sim_time),
    },
    "transport_signature": {
        "peak_time": float(times[peak_idx]),
        "peak_amplitude": float(max_rho_over_time[peak_idx]),
        "dip_time": float(dip_time),
        "dip_amplitude": float(dip_val),
        "reappear_time": float(reappear_time),
        "reappear_amplitude": float(reappear_val),
        "transport_time_measured": float(transport_time),
        "residual_pct": float(residual_pct) if residual_pct is not None else None,
    },
    "lin_finite_size": {
        "N16_residual_pct": 0.72,
        "N16_transport_time": 2.250,
        "N24_residual_pct": float(residual_pct) if residual_pct is not None else None,
        "N24_transport_time": float(transport_time),
        "T_predicted": float(T_null_predicted),
        "lin_prediction_N24_pct": float(lin_pred_24),
        "lin_1N_consistent": lin_check,
        "lin_C_constant": float(11.52),
    },
    "total_time_s": float(total_time),
    "max_rho_over_time": [float(x) for x in max_rho_over_time],
}

out_path = "D:/quantum-worldline/research/data/simulations/holographic_transport_24q.json"
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

np.save("D:/quantum-worldline/research/data/simulations/boundary_density_Y_24q.npy", boundary_density_Y)
np.save("D:/quantum-worldline/research/data/simulations/boundary_density_Z_24q.npy", boundary_density_Z)
np.save("D:/quantum-worldline/research/data/simulations/transport_times_24q.npy", times)
np.save("D:/quantum-worldline/research/data/simulations/transport_max_rho_24q.npy", max_rho_over_time)

print(f"\n{'='*65}")
print("RESULTS SAVED:")
print(f"  {out_path}")
print(f"  boundary_density_Y_24q.npy  (shape {boundary_density_Y.shape})")
print(f"  boundary_density_Z_24q.npy  (shape {boundary_density_Z.shape})")
print(f"  Total wall time: {total_time:.0f}s ({total_time/3600:.2f}h)")
print(f"{'='*65}", flush=True)
