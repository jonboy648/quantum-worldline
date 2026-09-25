"""
SIM-2026-008b (8q test): Augmented Lagrangian + Velocity Verlet MERA VQE
========================================================================
Standard MERA gates (Ry+Rz+CX) with:
  - Augmented Lagrangian Method (ALM) for Z2 enforcement
  - Velocity Verlet optimizer with momentum (PAPER-2026-027)
  - Layer-by-layer initialization (Miao & Barthel 2025)

8q validation before 24q RunPod deployment.

ALM: L(theta, mu, rho) = <H> + mu * g(theta) + (rho/2) * g(theta)^2
  where g(theta) = (1 - <P>)/2  (Z2 constraint violation)
  mu updated: mu += rho * g(theta) after each round
  rho increased: rho *= 2 each round
"""
import numpy as np
import time
import json
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

N_QUBITS = 8
N_LAYERS = 3

I2 = np.eye(2, dtype=complex)
Xm = np.array([[0, 1], [1, 0]], dtype=complex)
Ym = np.array([[0, -1j], [1j, 0]], dtype=complex)
Zm = np.array([[1, 0], [0, -1]], dtype=complex)


def sparse_pauli(n, i, p):
    I2s = speye(2, format="csr")
    paulis = {"I": I2s, "X": csr_matrix(Xm), "Y": csr_matrix(Ym), "Z": csr_matrix(Zm)}
    mats = [paulis[p] if k == i else I2s for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


def build_tfim_obc(n):
    dim = 2 ** n
    H = csr_matrix((dim, dim), dtype=complex)
    for i in range(n - 1):
        H -= sparse_pauli(n, i, "Z") @ sparse_pauli(n, i + 1, "Z")
    for i in range(n):
        H -= sparse_pauli(n, i, "X")
    return H


def build_parity_op(n):
    P = sparse_pauli(n, 0, "X")
    for i in range(1, n):
        P = P @ sparse_pauli(n, i, "X")
    return P


# ================================================================
# Standard MERA circuit (Ry+Rz+CX) via numpy statevector
# ================================================================
def apply_ry(sv, q, theta, n):
    c, s = np.cos(theta/2), np.sin(theta/2)
    dim = 2**n
    result = np.zeros(dim, dtype=complex)
    for idx in range(dim):
        bit = (idx >> (n-1-q)) & 1
        flipped = idx ^ (1 << (n-1-q))
        if bit == 0:
            result[idx] += c * sv[idx] - s * sv[flipped]
        else:
            result[idx] += s * sv[flipped] + c * sv[idx]
    return result


def apply_rz(sv, q, theta, n):
    dim = 2**n
    result = np.zeros(dim, dtype=complex)
    for idx in range(dim):
        bit = (idx >> (n-1-q)) & 1
        phase = np.exp(-1j * theta/2) if bit == 0 else np.exp(1j * theta/2)
        result[idx] = phase * sv[idx]
    return result


def apply_cx(sv, ctrl, targ, n):
    dim = 2**n
    result = sv.copy()
    for idx in range(dim):
        ctrl_bit = (idx >> (n-1-ctrl)) & 1
        if ctrl_bit == 1:
            flipped = idx ^ (1 << (n-1-targ))
            result[idx], result[flipped] = sv[flipped], sv[idx]
    return result


def build_mera_sv(params, n_qubits, n_layers):
    """Standard MERA with Ry+Rz+CX. Initial state |0>^N."""
    dim = 2 ** n_qubits
    sv = np.zeros(dim, dtype=complex)
    sv[0] = 1.0  # |0...0>

    offset = 0
    active = list(range(n_qubits))

    for layer in range(n_layers):
        na = len(active)
        if na < 2:
            break

        # Disentanglers: Ry Rz Ry Rz CX Ry Ry (6 params)
        for k in range(0, na - 1, 2):
            q0, q1 = active[k], active[k+1]
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_cx(sv, q0, q1, n_qubits)
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1

        # Isometries: Ry Ry CX Ry Rz (4 params)
        next_active = []
        for k in range(0, na - 1, 2):
            q0, q1 = active[k], active[k+1]
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_cx(sv, q0, q1, n_qubits)
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q1, params[offset], n_qubits); offset += 1
            next_active.append(q0)

        if na % 2 == 1:
            next_active.append(active[-1])
        active = next_active

    # Top tensor
    if len(active) >= 2 and offset + 6 <= len(params):
        q0, q1 = active[0], active[1]
        sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
        sv = apply_rz(sv, q0, params[offset], n_qubits); offset += 1
        sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
        sv = apply_rz(sv, q1, params[offset], n_qubits); offset += 1
        sv = apply_cx(sv, q0, q1, n_qubits)
        sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
        sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1

    return sv


def count_mera_params(n_qubits, n_layers):
    total = 0
    active = n_qubits
    for layer in range(n_layers):
        if active < 2:
            break
        n_pairs = active // 2
        total += n_pairs * 6  # disentanglers
        total += n_pairs * 4  # isometries
        active = n_pairs + (active % 2)
    if active >= 2:
        total += 6  # top tensor
    return total


# ================================================================
# Velocity Verlet optimizer (PAPER-2026-027)
# ================================================================
def velocity_verlet_optimize(cost_fn, theta0, n_iters=200, dt=0.01, mass=1.0,
                              gamma=0.68, eps=1e-5, callback=None):
    """Velocity Verlet with damping for VQE optimization.
    params: theta (position), v (velocity), F=-grad(cost)
    """
    n = len(theta0)
    theta = theta0.copy()
    v = np.zeros(n)

    def gradient(th):
        g = np.zeros(n)
        f0 = cost_fn(th)
        for i in range(n):
            th_plus = th.copy()
            th_plus[i] += eps
            g[i] = (cost_fn(th_plus) - f0) / eps
        return g, f0

    grad, E = gradient(theta)
    F = -grad
    best_theta = theta.copy()
    best_E = E

    for it in range(n_iters):
        # Half-step velocity
        v = v + 0.5 * dt * F / mass
        # Full-step position
        theta = theta + dt * v
        # Compute new force
        grad, E = gradient(theta)
        F = -grad
        # Half-step velocity + damping
        v = (v + 0.5 * dt * F / mass) * gamma

        if E < best_E:
            best_E = E
            best_theta = theta.copy()

        if callback and (it + 1) % 20 == 0:
            callback(it + 1, E, best_E, theta)

    return best_theta, best_E


# ================================================================
# Main
# ================================================================
print("=" * 65)
print("SIM-2026-008b (8q): ALM + Velocity Verlet MERA VQE")
print("=" * 65)

H = build_tfim_obc(N_QUBITS)
P_op = build_parity_op(N_QUBITS)
H_dense = H.toarray()
P_dense = P_op.toarray()

E_exact, _ = eigsh(H, k=1, which="SA")
E0 = E_exact[0]

n_params = count_mera_params(N_QUBITS, N_LAYERS)
print(f"E0_exact = {E0:.6f}")
print(f"Params: {n_params}, Qubits: {N_QUBITS}, Layers: {N_LAYERS}")

eval_count = [0]


def raw_energy(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    eval_count[0] += 1
    return np.real(sv.conj() @ H_dense @ sv)


def parity(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    return np.real(sv.conj() @ P_dense @ sv)


def magnetization(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    M = 0.0
    for i in range(N_QUBITS):
        Zi = sparse_pauli(N_QUBITS, i, "Z").toarray()
        M += np.real(sv.conj() @ Zi @ sv)
    return M / N_QUBITS


# ALM parameters
seeds = [7, 42]
results = []
best_E_global = 0
best_params_global = None
best_seed_global = None

for seed in seeds:
    np.random.seed(seed)
    theta = np.random.uniform(-0.3, 0.3, n_params)
    eval_count[0] = 0
    t0 = time.time()

    mu = 0.0      # Lagrange multiplier
    rho = 2.0     # penalty coefficient
    n_alm_rounds = 6
    verlet_iters = 80  # per ALM round

    # Velocity Verlet hyperparams (from PAPER-2026-027, adapted)
    vv_dt = 0.008
    vv_mass = 1.2
    vv_gamma = 0.70

    print(f"\n[seed={seed}] ALM rounds={n_alm_rounds}, Verlet iters={verlet_iters}/round")

    for alm_round in range(n_alm_rounds):
        # Build augmented Lagrangian cost function
        current_mu = mu
        current_rho = rho

        def alm_cost(params):
            E = raw_energy(params)
            sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
            p = np.real(sv.conj() @ P_dense @ sv)
            g = (1.0 - p) / 2.0  # constraint violation
            return E + current_mu * g + (current_rho / 2.0) * g ** 2

        def callback(it, E_cur, E_best, th):
            p = parity(th)
            err = abs(E_best - E0) / abs(E0) * 100
            # Only print raw energy (without ALM terms) for clarity
            E_raw = raw_energy(th)
            print(f"    round {alm_round+1} iter {it:3d}: E_raw={E_raw:.4f} ({abs(E_raw-E0)/abs(E0)*100:.2f}%)  "
                  f"<P>={p:.4f}  mu={current_mu:.2f}  rho={current_rho:.1f}", flush=True)

        theta, _ = velocity_verlet_optimize(
            alm_cost, theta, n_iters=verlet_iters,
            dt=vv_dt, mass=vv_mass, gamma=vv_gamma, callback=callback
        )

        # Update ALM multipliers
        p_val = parity(theta)
        g_val = (1.0 - p_val) / 2.0
        mu = mu + rho * g_val
        rho = min(rho * 2.0, 200.0)

        E_raw = raw_energy(theta)
        err = abs(E_raw - E0) / abs(E0) * 100
        print(f"  Round {alm_round+1} done: E_raw={E_raw:.6f} ({err:.2f}%)  "
              f"<P>={p_val:.4f}  g={g_val:.4f}  mu->{mu:.2f}  rho->{rho:.1f}", flush=True)

    elapsed = time.time() - t0
    E_final = raw_energy(theta)
    P_final = parity(theta)
    M_final = magnetization(theta)
    error_pct = abs(E_final - E0) / abs(E0) * 100

    print(f"\n  seed={seed} FINAL: E={E_final:.6f} ({error_pct:.2f}%)  "
          f"<P>={P_final:.6f}  <M>={M_final:.4f}  "
          f"evals={eval_count[0]}  {elapsed:.1f}s")

    if best_params_global is None or E_final < best_E_global:
        best_E_global = E_final
        best_params_global = theta.copy()
        best_seed_global = seed

    results.append({
        "seed": seed,
        "E_final": float(E_final),
        "error_pct": float(error_pct),
        "P_final": float(P_final),
        "M_final": float(M_final),
        "evals": eval_count[0],
        "elapsed_s": float(elapsed),
        "mu_final": float(mu),
        "rho_final": float(rho),
    })

# Summary
best_error = abs(best_E_global - E0) / abs(E0) * 100
P_best = parity(best_params_global)
z2_pass = bool(abs(P_best - 1.0) < 0.01)
energy_pass = bool(best_error < 3.0)
overall = "PASS" if (z2_pass and energy_pass) else "FAIL"

print(f"\n{'='*65}")
print(f"VERDICT: {overall}")
print(f"  Best: seed={best_seed_global}, E={best_E_global:.6f} ({best_error:.2f}%)")
print(f"  <P> = {P_best:.6f} (target: >0.99)")
print(f"  Z2 enforced: {'YES' if z2_pass else 'NO'}")
print(f"  Energy < 3%: {'YES' if energy_pass else 'NO'}")
print(f"{'='*65}")

output = {
    "id": "SIM-2026-008b-8q-test",
    "experiment": "alm_velocity_verlet_mera_8q",
    "n_qubits": N_QUBITS,
    "n_layers": N_LAYERS,
    "n_params": n_params,
    "E0_exact": float(E0),
    "method": "Augmented Lagrangian + Velocity Verlet",
    "gate_set": "Ry + Rz + CX (standard MERA)",
    "alm_rounds": n_alm_rounds,
    "verlet_iters_per_round": verlet_iters,
    "verlet_hyperparams": {"dt": vv_dt, "mass": vv_mass, "gamma": vv_gamma},
    "results": results,
    "best_seed": best_seed_global,
    "best_E": float(best_E_global),
    "best_error_pct": float(best_error),
    "best_P": float(P_best),
    "z2_enforced": z2_pass,
    "energy_pass": energy_pass,
    "verdict": overall,
}

outpath = "D:/quantum-worldline/research/data/simulations/SIM-2026-008b-8q-test.json"
with open(outpath, "w") as f:
    json.dump(output, f, indent=2)
print(f"\nResults saved to {outpath}")
