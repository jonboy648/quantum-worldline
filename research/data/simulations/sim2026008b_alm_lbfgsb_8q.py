"""
SIM-2026-008b (8q): Augmented Lagrangian + L-BFGS-B MERA VQE
=============================================================
Standard MERA gates (Ry+Rz+CX) with Augmented Lagrangian Method.
Uses L-BFGS-B (efficient) instead of Velocity Verlet (too slow in numpy).

Key insight: ALM gradually increases penalty on Z2 violation while
L-BFGS-B optimizes within each round. The Lagrange multiplier mu
tracks violation history, eventually forcing Z2 compliance.

Velocity Verlet reserved for RunPod (where Aer GPU makes it fast).
"""
import numpy as np
import time
import json
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh
from scipy.optimize import minimize

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


# Parity projection via bit-flip trick (fast, no matrix needed)
def project_z2(sv, n_qubits):
    """Project statevector onto P=+1 sector: sv_plus = (sv + P*sv)/norm"""
    mask = (1 << n_qubits) - 1  # all bits set
    sv_flipped = sv[np.arange(len(sv)) ^ mask]  # P|psi> = flip all bits
    sv_plus = sv + sv_flipped
    norm = np.linalg.norm(sv_plus)
    if norm < 1e-15:
        return sv  # already in P=-1, don't project
    return sv_plus / norm


# Standard MERA via numpy (same as before but with Z2 projection option)
def apply_ry(sv, q, theta, n):
    c, s = np.cos(theta / 2), np.sin(theta / 2)
    dim = 2 ** n
    result = np.zeros(dim, dtype=complex)
    for idx in range(dim):
        bit = (idx >> (n - 1 - q)) & 1
        flipped = idx ^ (1 << (n - 1 - q))
        if bit == 0:
            result[idx] += c * sv[idx] - s * sv[flipped]
        else:
            result[idx] += s * sv[flipped] + c * sv[idx]
    return result


def apply_rz(sv, q, theta, n):
    dim = 2 ** n
    result = np.zeros(dim, dtype=complex)
    for idx in range(dim):
        bit = (idx >> (n - 1 - q)) & 1
        phase = np.exp(-1j * theta / 2) if bit == 0 else np.exp(1j * theta / 2)
        result[idx] = phase * sv[idx]
    return result


def apply_cx(sv, ctrl, targ, n):
    dim = 2 ** n
    result = sv.copy()
    for idx in range(dim):
        ctrl_bit = (idx >> (n - 1 - ctrl)) & 1
        if ctrl_bit == 1:
            flipped = idx ^ (1 << (n - 1 - targ))
            result[idx], result[flipped] = sv[flipped], sv[idx]
    return result


def build_mera_sv(params, n_qubits, n_layers):
    dim = 2 ** n_qubits
    sv = np.zeros(dim, dtype=complex)
    sv[0] = 1.0

    offset = 0
    active = list(range(n_qubits))

    for layer in range(n_layers):
        na = len(active)
        if na < 2:
            break
        for k in range(0, na - 1, 2):
            q0, q1 = active[k], active[k + 1]
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_cx(sv, q0, q1, n_qubits)
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
        next_active = []
        for k in range(0, na - 1, 2):
            q0, q1 = active[k], active[k + 1]
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_ry(sv, q1, params[offset], n_qubits); offset += 1
            sv = apply_cx(sv, q0, q1, n_qubits)
            sv = apply_ry(sv, q0, params[offset], n_qubits); offset += 1
            sv = apply_rz(sv, q1, params[offset], n_qubits); offset += 1
            next_active.append(q0)
        if na % 2 == 1:
            next_active.append(active[-1])
        active = next_active
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
        total += n_pairs * 6 + n_pairs * 4
        active = n_pairs + (active % 2)
    if active >= 2:
        total += 6
    return total


# ================================================================
print("=" * 65)
print("SIM-2026-008b (8q): ALM + L-BFGS-B MERA VQE")
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


def parity_val(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    return np.real(sv.conj() @ P_dense @ sv)


def magnetization(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    M = 0.0
    for i in range(N_QUBITS):
        Zi = sparse_pauli(N_QUBITS, i, "Z").toarray()
        M += np.real(sv.conj() @ Zi @ sv)
    return M / N_QUBITS


# Also test: standard MERA + Z2 projection (for comparison)
def projected_energy(params):
    sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
    sv = project_z2(sv, N_QUBITS)
    eval_count[0] += 1
    return np.real(sv.conj() @ H_dense @ sv)


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

    # ── METHOD A: ALM with L-BFGS-B ──
    mu = 0.0
    rho = 1.0
    n_rounds = 8
    evals_per_round = 3000

    print(f"\n[seed={seed}] METHOD A: ALM + L-BFGS-B, {n_rounds} rounds x {evals_per_round} evals")

    for rd in range(n_rounds):
        cur_mu = mu
        cur_rho = rho

        def alm_cost(params):
            sv = build_mera_sv(params, N_QUBITS, N_LAYERS)
            eval_count[0] += 1
            E = np.real(sv.conj() @ H_dense @ sv)
            p = np.real(sv.conj() @ P_dense @ sv)
            g = (1.0 - p) / 2.0
            return E + cur_mu * g + (cur_rho / 2.0) * g ** 2

        res = minimize(alm_cost, theta, method="L-BFGS-B",
                       options={"maxfun": evals_per_round, "maxiter": 300})
        theta = res.x

        p_val = parity_val(theta)
        g_val = (1.0 - p_val) / 2.0
        E_raw = raw_energy(theta)
        err = abs(E_raw - E0) / abs(E0) * 100
        M_val = magnetization(theta)

        mu = mu + rho * g_val
        rho = min(rho * 2.0, 100.0)

        print(f"  R{rd+1}: E={E_raw:.4f} ({err:.1f}%)  <P>={p_val:.4f}  <M>={M_val:.3f}  "
              f"mu={mu:.1f}  rho={rho:.0f}  evals={eval_count[0]}", flush=True)

    elapsed_A = time.time() - t0
    E_alm = raw_energy(theta)
    P_alm = parity_val(theta)
    M_alm = magnetization(theta)
    err_alm = abs(E_alm - E0) / abs(E0) * 100

    # ── METHOD B: Same theta, now project to P=+1 and report ──
    sv_proj = build_mera_sv(theta, N_QUBITS, N_LAYERS)
    sv_proj = project_z2(sv_proj, N_QUBITS)
    E_proj = np.real(sv_proj.conj() @ H_dense @ sv_proj)
    P_proj = np.real(sv_proj.conj() @ P_dense @ sv_proj)
    err_proj = abs(E_proj - E0) / abs(E0) * 100

    # ── METHOD C: Optimize directly with projection ──
    t1 = time.time()
    print(f"  [seed={seed}] METHOD C: L-BFGS-B with Z2 projection, 5000 evals")
    eval_count[0] = 0
    theta_c = theta.copy()  # warm start from ALM result
    res_c = minimize(projected_energy, theta_c, method="L-BFGS-B",
                     options={"maxfun": 5000, "maxiter": 300})
    theta_c = res_c.x
    sv_c = build_mera_sv(theta_c, N_QUBITS, N_LAYERS)
    sv_c = project_z2(sv_c, N_QUBITS)
    E_c = np.real(sv_c.conj() @ H_dense @ sv_c)
    P_c = np.real(sv_c.conj() @ P_dense @ sv_c)
    err_c = abs(E_c - E0) / abs(E0) * 100
    elapsed_C = time.time() - t1

    print(f"\n  seed={seed} RESULTS:")
    print(f"    A (ALM):        E={E_alm:.6f} ({err_alm:.2f}%)  <P>={P_alm:.4f}  <M>={M_alm:.3f}  {elapsed_A:.0f}s")
    print(f"    B (post-proj):  E={E_proj:.6f} ({err_proj:.2f}%)  <P>={P_proj:.4f}")
    print(f"    C (proj-opt):   E={E_c:.6f} ({err_c:.2f}%)  <P>={P_c:.4f}  {elapsed_C:.0f}s")

    # Pick best method
    best_method = "A"
    best_E_seed = E_alm
    best_P_seed = P_alm
    if E_proj < best_E_seed and abs(P_proj - 1.0) < 0.01:
        best_method = "B"
        best_E_seed = E_proj
        best_P_seed = P_proj
    if E_c < best_E_seed and abs(P_c - 1.0) < 0.01:
        best_method = "C"
        best_E_seed = E_c
        best_P_seed = P_c

    best_err_seed = abs(best_E_seed - E0) / abs(E0) * 100
    print(f"    BEST: method {best_method}, E={best_E_seed:.6f} ({best_err_seed:.2f}%)")

    if best_params_global is None or best_E_seed < best_E_global:
        best_E_global = best_E_seed
        best_params_global = theta.copy()
        best_seed_global = seed

    results.append({
        "seed": seed,
        "alm_E": float(E_alm), "alm_err": float(err_alm), "alm_P": float(P_alm), "alm_M": float(M_alm),
        "proj_E": float(E_proj), "proj_err": float(err_proj), "proj_P": float(P_proj),
        "projopt_E": float(E_c), "projopt_err": float(err_c), "projopt_P": float(P_c),
        "best_method": best_method, "best_E": float(best_E_seed), "best_err": float(best_err_seed),
    })

# Summary
best_error = abs(best_E_global - E0) / abs(E0) * 100
z2_ok = bool(any(abs(r["best_E"] - r.get("projopt_E", 0)) < 0.01 or r["best_method"] in ("B", "C") for r in results))
energy_ok = bool(best_error < 3.0)
overall = "PASS" if energy_ok else "FAIL"

print(f"\n{'='*65}")
print(f"VERDICT: {overall}")
print(f"  Best: seed={best_seed_global}, E={best_E_global:.6f} ({best_error:.2f}%)")
print(f"  Energy < 3%: {'YES' if energy_ok else 'NO'}")
print(f"{'='*65}")

output = {
    "id": "SIM-2026-008b-8q-test",
    "method": "ALM + L-BFGS-B, then post-projection, then projection-optimized",
    "n_qubits": N_QUBITS, "n_layers": N_LAYERS, "n_params": n_params,
    "E0_exact": float(E0),
    "results": results,
    "best_E": float(best_E_global), "best_error_pct": float(best_error),
    "verdict": overall,
}
with open("D:/quantum-worldline/research/data/simulations/SIM-2026-008b-8q-test.json", "w") as f:
    json.dump(output, f, indent=2)
print(f"\nSaved to SIM-2026-008b-8q-test.json")
