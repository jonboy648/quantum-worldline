"""
Holographic Transportation -- 24q MERA (Wang & He, arXiv:2501.03084)
Tests Lin's 1/N finite-size correction to holographic transport time.

HYP-2026-006 established at N=16: T_measured=2.250, T_predicted=2.266 (0.72% residual)
Lin's prediction: residual ~ C/N, so at N=24 we expect ~0.47% residual.

Extends holographic_transport_16q.py to L=24.
Key differences vs L=16:
  - 2^24 = 16M dimensional Hilbert space (vs 65k for L=16)
  - Hamiltonian build: O(L * 2^L) but each 3-body Pauli term is sparse (nnz = 2^L / 4)
  - Time evolution: precompute sum of Y operators to avoid per-step rebuild
  - eigsh: expects ~3-5 min at L=24

Memory budget (L=24):
  - Statevector: 2^24 * 16 bytes = 256 MB per vector
  - H_boundary (sparse, 3-body Paulis, ~4 nnz/row): ~256 MB
  - Y_ops: 24 sparse matrices, ~64 MB each = 1.5 GB total (PRECOMPUTED SUM instead)
  - Total: ~2-3 GB -- manageable on 8+ GB RAM

Approach for perturbation delta_H:
  Instead of rebuilding sum_i J_i(t) Y_i each step, we precompute each Y_i as a
  sparse matrix and cache them. At each step we only need a scalar combo.
  Y_ops list: 24 * 128 MB (dense) is too large. Keep sparse: each Y_i has nnz = 2^24
  (off-diagonal with +-i, so actually nnz = 2^24). That's 24 * 256 MB = 6 GB. Too big.

  Better: precompute the combined action. For each time step, we need:
    delta_H @ psi = -sum_i Re(J_i(t)) * (Y_i @ psi)
  We can apply each Y_i to psi on-the-fly without storing Y_i explicitly.
  Y on site i just flips bit i with factor +-i. So (Y_i @ psi)[k] = -i * psi[k ^ (1 << (L-1-i))]
  with sign = +1 if bit i of k is 0, -1 if bit i is 1.

  This avoids storing any Y_op matrices -- just direct index manipulation.
"""
import numpy as np
import sys, time, json
from scipy.sparse import csr_matrix
from scipy.sparse import eye as speye
from scipy.sparse import kron as skron
from scipy.sparse.linalg import eigsh, expm_multiply

print("=" * 65)
print("Holographic Transportation -- 24q Analytical MERA")
print("Testing Lin 1/N finite-size correction (HYP-2026-006)")
print("=" * 65, flush=True)

L = 24   # boundary sites
T_GLOBAL = time.time()

# Pauli matrices
I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)


# ================================================================
# 1. Build the boundary Hamiltonian (Wang & He Eq 1, PBC)
#    H = L/(4*pi) * sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}]
#
# Memory analysis at L=24:
#   Each X_{j-1} Z_j X_{j+1} term: X flips bit j-1, Z gives +-1 on bit j,
#   X flips bit j+1. Net: each row maps to exactly 1 other row (since XZX).
#   So nnz per row = 1 => total nnz = 2^24 = 16M. Manageable.
#   Each X_j X_{j+1}: nnz = 2^24 (all rows, each flips 2 bits). Also fine.
# ================================================================
print("[1] Building boundary Hamiltonian H_boundary (L=24)...", flush=True)
print("    This will take a few minutes.", flush=True)
t0 = time.time()

dim = 2 ** L  # 16,777,216

def pauli_on_site_sparse(n, site, pauli_char):
    """
    Build sparse matrix for a single Pauli on one site in n-qubit system.
    Uses a vectorized index approach instead of kron products for efficiency.
    """
    I2s = speye(2, format="csr")
    p_map = {
        "I": csr_matrix(I2),
        "X": csr_matrix(X),
        "Y": csr_matrix(Y),
        "Z": csr_matrix(Z),
    }
    mats = [p_map[pauli_char] if k == site else I2s for k in range(n)]
    result = mats[0]
    for m in mats[1:]:
        result = skron(result, m, format="csr")
    return result


def build_3body_term_direct(n, site_a, pauli_a, site_b, pauli_b, site_c, pauli_c):
    """
    Build X_a Z_b X_c type term directly via index manipulation.
    Faster than kronecker for Pauli products.
    Returns sparse CSR matrix.
    """
    dim = 2 ** n
    rows = np.arange(dim, dtype=np.int64)

    # For each Pauli:
    # X: flips bit, coeff=1
    # Z: no flip, coeff = +1 if bit=0, -1 if bit=1
    # Y: flips bit, coeff = -i if bit=0, +i if bit=1 (Y|0>=i|1>, Y|1>=-i|0> ... wait:
    #    Y = [[0,-i],[i,0]]: Y|0> = i|1>, Y|1> = -i|0>
    #    So if input bit is 0: coeff = i, flips to 1
    #    If input bit is 1: coeff = -i, flips to 0

    def apply_pauli_to_row(row_idx, pauli, site):
        """Returns (new_row_idx, coeff) for Pauli acting on row."""
        bit_pos = n - 1 - site  # bit position from right
        bit_val = (row_idx >> bit_pos) & 1

        if pauli == "I":
            return row_idx, 1.0 + 0j
        elif pauli == "X":
            return row_idx ^ (1 << bit_pos), 1.0 + 0j
        elif pauli == "Z":
            return row_idx, (1.0 - 2.0 * bit_val) + 0j  # +1 if 0, -1 if 1
        elif pauli == "Y":
            coeff = 1j * (1.0 - 2.0 * bit_val) if bit_val == 0 else -1j
            # Y|0> = i|1>, Y|1> = -i|0>
            coeff = 1j if bit_val == 0 else -1j
            # Wait: Y = [[0,-i],[i,0]]
            # Y|0> = [[0,-i],[i,0]] [1,0]^T = [0, i]^T = i|1>
            # Y|1> = [[0,-i],[i,0]] [0,1]^T = [-i, 0]^T = -i|0>
            coeff = 1j if bit_val == 0 else -1j
            return row_idx ^ (1 << bit_pos), coeff

    # Vectorized approach: compute output col and coeff for all rows at once
    bit_pos_a = n - 1 - site_a
    bit_pos_b = n - 1 - site_b
    bit_pos_c = n - 1 - site_c

    col = rows.copy()
    coeff = np.ones(dim, dtype=complex)

    # Apply pauli_a on site_a
    if pauli_a == "X":
        col ^= (1 << bit_pos_a)
    elif pauli_a == "Z":
        bit_vals = (rows >> bit_pos_a) & 1
        coeff *= (1.0 - 2.0 * bit_vals)
    elif pauli_a == "Y":
        bit_vals = (rows >> bit_pos_a) & 1
        y_coeff = np.where(bit_vals == 0, 1j, -1j)
        coeff *= y_coeff
        col ^= (1 << bit_pos_a)

    # Apply pauli_b on site_b
    if pauli_b == "X":
        col ^= (1 << bit_pos_b)
    elif pauli_b == "Z":
        bit_vals = (rows >> bit_pos_b) & 1
        coeff *= (1.0 - 2.0 * bit_vals)
    elif pauli_b == "Y":
        bit_vals = (rows >> bit_pos_b) & 1
        y_coeff = np.where(bit_vals == 0, 1j, -1j)
        coeff *= y_coeff
        col ^= (1 << bit_pos_b)

    # Apply pauli_c on site_c
    if pauli_c == "X":
        col ^= (1 << bit_pos_c)
    elif pauli_c == "Z":
        bit_vals = (rows >> bit_pos_c) & 1
        coeff *= (1.0 - 2.0 * bit_vals)
    elif pauli_c == "Y":
        bit_vals = (rows >> bit_pos_c) & 1
        y_coeff = np.where(bit_vals == 0, 1j, -1j)
        coeff *= y_coeff
        col ^= (1 << bit_pos_c)

    return csr_matrix((coeff, (rows, col)), shape=(dim, dim))


def build_2body_term_direct(n, site_a, pauli_a, site_b, pauli_b):
    """Build 2-body Pauli term directly."""
    dim = 2 ** n
    rows = np.arange(dim, dtype=np.int64)

    bit_pos_a = n - 1 - site_a
    bit_pos_b = n - 1 - site_b

    col = rows.copy()
    coeff = np.ones(dim, dtype=complex)

    if pauli_a == "X":
        col ^= (1 << bit_pos_a)
    elif pauli_a == "Z":
        bit_vals = (rows >> bit_pos_a) & 1
        coeff *= (1.0 - 2.0 * bit_vals)
    elif pauli_a == "Y":
        bit_vals = (rows >> bit_pos_a) & 1
        coeff *= np.where(bit_vals == 0, 1j, -1j)
        col ^= (1 << bit_pos_a)

    if pauli_b == "X":
        col ^= (1 << bit_pos_b)
    elif pauli_b == "Z":
        bit_vals = (rows >> bit_pos_b) & 1
        coeff *= (1.0 - 2.0 * bit_vals)
    elif pauli_b == "Y":
        bit_vals = (rows >> bit_pos_b) & 1
        coeff *= np.where(bit_vals == 0, 1j, -1j)
        col ^= (1 << bit_pos_b)

    return csr_matrix((coeff, (rows, col)), shape=(dim, dim))


# Build H_boundary = L/(4*pi) * sum_j [X_{j-1} Z_j X_{j+1} - X_j X_{j+1}]
H_boundary = csr_matrix((dim, dim), dtype=complex)
prefactor = L / (4 * np.pi)

for j in range(L):
    jm1 = (j - 1) % L
    jp1 = (j + 1) % L
    # 3-body: X_{j-1} Z_j X_{j+1}
    H_boundary = H_boundary + prefactor * build_3body_term_direct(L, jm1, "X", j, "Z", jp1, "X")
    # 2-body: -X_j X_{j+1}
    H_boundary = H_boundary + (-prefactor) * build_2body_term_direct(L, j, "X", jp1, "X")

    if (j + 1) % 4 == 0:
        print(f"  Built terms for j={j+1}/{L}...", flush=True)

print(f"  H_boundary: shape={H_boundary.shape}, nnz={H_boundary.nnz}")
print(f"  H_boundary build time: {time.time()-t0:.1f}s", flush=True)


# ================================================================
# 2. Find ground state via eigsh
# ================================================================
print("[2] Finding ground state (eigsh, L=24)...", flush=True)
print("    Expected: 1-5 min on modern CPU", flush=True)
t0 = time.time()
E_gs, psi_gs = eigsh(H_boundary, k=1, which="SA")
E_gs = E_gs[0]
psi_gs = psi_gs[:, 0].astype(complex)
print(f"  E_gs = {float(E_gs):.6f} (eigsh took {time.time()-t0:.1f}s)", flush=True)


# ================================================================
# 3. Perturbation parameters (Wang & He Fig 3(a))
#    Match exactly the L=16 parameters for a clean comparison.
#    Note: phi_i = 2*pi*i/L - 3*pi/4 shifts with L.
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
print(f"    dt={dt}, t_max={t_max}, steps={n_steps}", flush=True)

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


# ================================================================
# 4. Apply Y operator to statevector WITHOUT storing Y_i matrices.
#    Y_i |psi>[k] = i * psi[k ^ bit_mask] * sign
#    where bit_mask = 1 << (L-1-i) and sign = +1 if bit i of k is 0, -1 if 1.
#    In vectorized form:
#      all_indices = arange(dim)
#      flipped_indices = all_indices ^ bit_mask
#      bit_vals = (all_indices >> (L-1-i)) & 1  # 0 or 1
#      y_coeff = where(bit_vals == 0, 1j, -1j)
#      (Y_i @ psi)[k] = y_coeff[k] * psi[flipped_indices[k]]
#    => result_k = y_coeff_k * psi[flipped_k]
# ================================================================

all_indices = np.arange(dim, dtype=np.int64)

def apply_Y_sum_to_sv(psi, J_real_vec):
    """
    Compute -sum_i J_real_vec[i] * Y_i @ psi  (the delta_H action on psi).
    J_real_vec: array of length L, real part of J coupling.
    Returns the result vector.
    """
    result = np.zeros(dim, dtype=complex)
    for i in range(L):
        if abs(J_real_vec[i]) < 1e-14:
            continue
        bit_pos = L - 1 - i
        bit_mask = 1 << bit_pos
        flipped = all_indices ^ bit_mask
        bit_vals = (all_indices >> bit_pos) & 1
        y_coeff = np.where(bit_vals == 0, 1j, -1j)
        # Y_i @ psi contribution
        result -= J_real_vec[i] * y_coeff * psi[flipped]
    return result


# Measure <Y_i> and <Z_i> without storing operators
def measure_Y_expectation(psi, i):
    """<psi|Y_i|psi> - <gs|Y_i|gs>."""
    bit_pos = L - 1 - i
    bit_mask = 1 << bit_pos
    flipped = all_indices ^ bit_mask
    bit_vals = (all_indices >> bit_pos) & 1
    # Y_i|psi>[k] = y_coeff[k] * psi[flipped[k]]
    y_coeff = np.where(bit_vals == 0, 1j, -1j)
    Yipsi = y_coeff * psi[flipped]
    return float(np.real(np.dot(psi.conj(), Yipsi)))


def measure_Z_expectation(psi, i):
    """<psi|Z_i|psi>."""
    bit_pos = L - 1 - i
    bit_vals = (all_indices >> bit_pos) & 1
    z_coeff = 1.0 - 2.0 * bit_vals  # +1 for 0, -1 for 1
    return float(np.real(np.dot(np.abs(psi)**2, z_coeff)))


# Precompute ground state expectation values
print("[4a] Precomputing ground state expectations...", flush=True)
gs_Y_exp = np.array([measure_Y_expectation(psi_gs, i) for i in range(L)])
gs_Z_exp = np.array([measure_Z_expectation(psi_gs, i) for i in range(L)])
print(f"    gs <Y> range: [{gs_Y_exp.min():.4f}, {gs_Y_exp.max():.4f}]")
print(f"    gs <Z> range: [{gs_Z_exp.min():.4f}, {gs_Z_exp.max():.4f}]", flush=True)


# ================================================================
# 5. Time evolution
# ================================================================
print("\n[5] Time evolution (120 steps x L=24)...", flush=True)
print("    Each step: H_boundary expm_multiply + L Y-operator applications")
print("    Expected: 20-60 min depending on CPU", flush=True)

psi = psi_gs.copy().astype(complex)

boundary_density_Y = np.zeros((n_steps + 1, L))
boundary_density_Z = np.zeros((n_steps + 1, L))

# t=0 densities (should be zero)
for i in range(L):
    boundary_density_Y[0, i] = measure_Y_expectation(psi, i) - gs_Y_exp[i]
    boundary_density_Z[0, i] = measure_Z_expectation(psi, i) - gs_Z_exp[i]

t0_evo = time.time()

for step in range(n_steps):
    # J_real: real part of J couplings at this timestep
    J_real = np.real(J_matrix[step])

    # Evolve psi by dt under H_total = H_boundary - sum_i Re(J_i) Y_i
    # Using expm_multiply for H_boundary part, and treating delta_H via
    # operator splitting: exp(-i (H + dH) dt) ~ exp(-i H dt) exp(-i dH dt)
    # This is first-order Trotter, same as L=16 script.
    # For delta_H = -sum J_i Y_i (purely Y terms):
    # exp(-i dH dt) psi = product_i exp(i J_i Y_i dt) psi
    # exp(i theta Y) = cos(theta) I + i sin(theta) Y
    # Apply as sequential 1-qubit rotations.

    # Step 1: apply delta_H rotation
    # For each site i: psi -> cos(J_i*dt)*psi + i*sin(J_i*dt)*(Y_i @ psi)
    for i in range(L):
        ji = J_real[i] * dt
        if abs(ji) < 1e-14:
            continue
        cos_j = np.cos(ji)
        sin_j = np.sin(ji)
        bit_pos = L - 1 - i
        bit_mask = 1 << bit_pos
        flipped = all_indices ^ bit_mask
        bit_vals = (all_indices >> bit_pos) & 1
        y_coeff = np.where(bit_vals == 0, 1j, -1j)
        Yipsi = y_coeff * psi[flipped]
        psi = cos_j * psi + 1j * sin_j * Yipsi

    # Step 2: apply H_boundary evolution
    psi = expm_multiply(-1j * H_boundary * dt, psi)

    # Normalize (numerical safety)
    norm = np.linalg.norm(psi)
    psi /= norm

    # Record densities
    for i in range(L):
        boundary_density_Y[step + 1, i] = measure_Y_expectation(psi, i) - gs_Y_exp[i]
        boundary_density_Z[step + 1, i] = measure_Z_expectation(psi, i) - gs_Z_exp[i]

    # Progress
    if (step + 1) % 10 == 0:
        t_now = times[step + 1]
        max_rho_Y = float(np.max(np.abs(boundary_density_Y[step + 1])))
        max_rho_Z = float(np.max(np.abs(boundary_density_Z[step + 1])))
        elapsed = time.time() - t0_evo
        rate = (step + 1) / elapsed
        eta = (n_steps - step - 1) / rate
        print(
            f"  t={t_now:.2f}  max|rho_Y|={max_rho_Y:.6f}  max|rho_Z|={max_rho_Z:.6f}  "
            f"{rate:.2f} step/s  ETA={eta/60:.1f}min",
            flush=True,
        )

sim_time = time.time() - t0_evo
print(f"  Evolution complete: {sim_time:.1f}s ({sim_time/60:.1f}min)", flush=True)


# ================================================================
# 6. Extract transport signature
# ================================================================
print("\n[6] Transportation signature analysis:", flush=True)

max_rho_over_time = np.max(np.abs(boundary_density_Y), axis=1)

# Find peak (first 30 steps)
peak_search_end = min(30, len(max_rho_over_time))
peak_idx = int(np.argmax(max_rho_over_time[:peak_search_end]))

l_AdS = 1.0 / np.log(2)
T_null_predicted = (np.pi / 2) * l_AdS  # composite geodesic formula

if peak_idx < len(max_rho_over_time) - 5:
    # Dip: minimum after initial peak, search window ~50 steps
    search_end = min(peak_idx + 60, len(max_rho_over_time))
    dip_idx = peak_idx + int(np.argmin(max_rho_over_time[peak_idx:search_end]))
    dip_time = float(times[dip_idx])
    dip_val = float(max_rho_over_time[dip_idx])

    # Reappearance: next peak after dip
    post_dip_start = dip_idx + 3  # skip immediately adjacent points
    post_dip_end = min(dip_idx + 80, len(max_rho_over_time))
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

transport_time = reappear_time - dip_time if dip_time > 0 and reappear_time > 0 else -1.0

# Residual and Lin scaling check
if transport_time > 0:
    residual_pct = (transport_time - T_null_predicted) / T_null_predicted * 100.0
    # Lin 1/N scaling: residual at N=16 was 0.72%, so C = 0.72 * 16 = 11.52
    # Prediction at N=24: 11.52/24 = 0.48%
    lin_C = 0.72 * 16  # constant from N=16 measurement
    lin_prediction_24 = lin_C / L
    lin_check = "CONSISTENT" if abs(residual_pct - lin_prediction_24) < 0.3 else "INCONSISTENT"
else:
    residual_pct = None
    lin_prediction_24 = 0.48
    lin_check = "NO_SIGNAL"

print(f"  l_AdS = 1/ln(2) = {l_AdS:.4f}")
print(f"  T_predicted (pi/2 * l_AdS) = {T_null_predicted:.4f}")
print(f"  Peak boundary excitation: t={times[peak_idx]:.2f}, max|rho|={max_rho_over_time[peak_idx]:.6f}")
print(f"  Dip (enters bulk): t={dip_time:.2f}, max|rho|={dip_val:.6f}")
print(f"  Reappears: t={reappear_time:.2f}, max|rho|={reappear_val:.6f}")
print(f"  Transport time T_measured = {transport_time:.3f}")
print(f"  Residual = {residual_pct:.3f}%" if residual_pct is not None else "  (no clear transport detected)")
print(f"  Lin 1/N prediction at N=24: {lin_prediction_24:.2f}%")
print(f"  Lin 1/N check: {lin_check}")


# ================================================================
# 7. Save results
# ================================================================
total_time = time.time() - T_GLOBAL

# Build comparison with N=16 result
comparison = {
    "N16_residual_pct": 0.72,
    "N24_residual_pct": float(residual_pct) if residual_pct is not None else None,
    "lin_prediction_N24_pct": float(lin_prediction_24),
    "lin_1N_consistent": lin_check,
    "N16_transport_time": 2.250,
    "N24_transport_time": float(transport_time),
    "T_predicted": float(T_null_predicted),
}

result = {
    "experiment": "holographic_transportation_24q",
    "hypothesis_id": "HYP-2026-006",
    "boundary_sites": L,
    "hamiltonian": "Wang_He_H_boundary (Eq 1, PBC)",
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
        "trotter_order": 1,
        "splitting": "exp(-i dH dt) then exp(-i H dt)",
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
    "lin_finite_size": comparison,
    "total_time_s": float(total_time),
    "max_rho_over_time": [float(x) for x in max_rho_over_time],
}

out_path = "D:/quantum-worldline/research/data/simulations/holographic_transport_24q.json"
with open(out_path, "w") as f:
    json.dump(result, f, indent=2)

print(f"\n{'='*65}")
print("RESULTS SAVED:")
print(f"  {out_path}")
print(f"  Total time: {total_time:.0f}s ({total_time/60:.1f}min)")
print(f"{'='*65}", flush=True)
