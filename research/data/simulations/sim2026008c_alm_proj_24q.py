"""
SIM-2026-008c: 2-Phase ALM + Projection 24q/5-layer MERA VQE
=============================================================
Proven approach from 8q test (1.12% error, <P>=1.000):
  Phase 1: ALM forces Z2 compliance (escapes ferromagnetic basin)
  Phase 2: Z2-projected L-BFGS-B from ALM warm-start (refines energy)

Uses Aer GPU + cupy sparse mat-vec on RunPod A100.

Setup on RunPod:
  pip install 'qiskit>=1.4,<2.0' 'qiskit-aer-gpu>=0.15,<0.16' cupy-cuda12x scipy
  nohup python sim2026008c_alm_proj_24q.py > sim2026008c.log 2>&1 &
"""
import numpy as np
import time, json, sys
from scipy.optimize import minimize
from scipy.sparse import csr_matrix, eye as speye, kron as skron

import cupy as cp
import cupyx.scipy.sparse as cpsparse

from qiskit import QuantumCircuit
from qiskit.circuit import Parameter

print("=" * 65)
print("SIM-2026-008c: 2-Phase ALM+Projection 24q/5L MERA VQE")
print("=" * 65, flush=True)

# GPU info
print(f"  cupy: {cp.__version__}")
dev = cp.cuda.Device(0)
print(f"  GPU: {dev} ({dev.mem_info[1]/1e9:.1f} GB)", flush=True)

NQ = 24
NLAYERS = 5
E0 = -30.199712  # cached exact ground state energy (OBC)
T_GLOBAL = time.time()

# ── Z2 parity tools (GPU) ──
PARITY_MASK = (1 << NQ) - 1
PARITY_IDX = cp.arange(1 << NQ, dtype=cp.int64) ^ PARITY_MASK


def parity_project_gpu(sv):
    sv_plus = sv + sv[PARITY_IDX]
    norm = cp.linalg.norm(sv_plus)
    if float(norm) < 1e-15:
        return sv
    return sv_plus / norm


def parity_expect_gpu(sv):
    return float(cp.real(cp.sum(sv.conj() * sv[PARITY_IDX])))


# ── MERA circuit (same structure as SIM-2026-006/007) ──
def build_mera(nq, nlayers):
    qc = QuantumCircuit(nq)
    params = []
    pidx = 0
    for layer in range(nlayers):
        step = 2 ** layer
        for i in range(0, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}"); params.append(p); pp.append(p); pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}"); params.append(p); pp2.append(p); pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
        for i in range(step, nq - step, 2 * step):
            j = i + step
            if j < nq:
                pp = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}"); params.append(p); pp.append(p); pidx += 1
                qc.u(pp[0], pp[1], pp[2], i)
                pp2 = []
                for _ in range(3):
                    p = Parameter(f"p{pidx}"); params.append(p); pp2.append(p); pidx += 1
                qc.u(pp2[0], pp2[1], pp2[2], j)
                qc.cx(i, j)
    return qc, params


qc_template, params = build_mera(NQ, NLAYERS)
NP = len(params)
print(f"Params: {NP}, depth: {qc_template.depth()}", flush=True)

# ── Hamiltonian (CPU build, GPU transfer) ──
def sparse_pauli(n, i, p):
    I2 = speye(2, format="csr")
    X = csr_matrix(np.array([[0,1],[1,0]], dtype=complex))
    Z = csr_matrix(np.array([[1,0],[0,-1]], dtype=complex))
    ops = {"I": I2, "X": X, "Z": Z}
    mats = [ops[p] if k == i else I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out


print("[1] Building Hamiltonian...", flush=True)
t0 = time.time()
H_scipy = csr_matrix((2**NQ, 2**NQ), dtype=complex)
for i in range(NQ - 1):
    H_scipy -= sparse_pauli(NQ, i, "Z") @ sparse_pauli(NQ, i+1, "Z")
for i in range(NQ):
    H_scipy -= sparse_pauli(NQ, i, "X")
print(f"  H built: {time.time()-t0:.1f}s, nnz={H_scipy.nnz}", flush=True)
print(f"  E0 = {E0:.6f} (cached)", flush=True)

H_gpu = cpsparse.csr_matrix(
    (cp.asarray(H_scipy.data), cp.asarray(H_scipy.indices), cp.asarray(H_scipy.indptr)),
    shape=H_scipy.shape,
)

# Z operators for diagnostics
Z_gpu = []
for i in range(NQ):
    z = sparse_pauli(NQ, i, "Z")
    Z_gpu.append(cpsparse.csr_matrix(
        (cp.asarray(z.data), cp.asarray(z.indices), cp.asarray(z.indptr)), shape=z.shape
    ))
print(f"  {NQ} Z operators on GPU", flush=True)

# ── Simulator ──
try:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector", device="GPU")
    print("[2] Aer GPU backend", flush=True)
except Exception:
    from qiskit_aer import AerSimulator
    sim = AerSimulator(method="statevector")
    print("[2] Aer CPU fallback", flush=True)


# ── Core functions ──
def get_sv_gpu(theta):
    """Run circuit, return statevector on GPU."""
    binds = {params[i]: float(theta[i]) for i in range(NP)}
    qc = qc_template.assign_parameters(binds)
    qc.save_statevector()
    result = sim.run(qc, shots=0).result()
    sv_np = np.asarray(result.get_statevector(qc))
    return cp.asarray(sv_np)


def energy_gpu(sv):
    return float(cp.real(cp.dot(sv.conj(), H_gpu @ sv)))


def diagnose(sv):
    mag = sum(float(cp.real(cp.dot(sv.conj(), Z_gpu[i] @ sv))) for i in range(NQ)) / NQ
    par = parity_expect_gpu(sv)
    return mag, par


eval_count = [0]


def raw_energy_fn(theta):
    sv = get_sv_gpu(theta)
    eval_count[0] += 1
    return energy_gpu(sv)


def projected_energy_fn(theta):
    sv = get_sv_gpu(theta)
    sv = parity_project_gpu(sv)
    eval_count[0] += 1
    return energy_gpu(sv)


# ── Main loop ──
SEEDS = [7, 42, 99, 13, 77]
ALM_ROUNDS = 8
ALM_EVALS = 5000
PROJ_EVALS = 15000

results = []
global_best_E = 0
global_best_theta = None
global_best_seed = None

for seed_idx, seed in enumerate(SEEDS):
    np.random.seed(seed)
    theta = np.random.uniform(-0.3, 0.3, NP)
    eval_count[0] = 0
    t_seed = time.time()

    print(f"\n{'='*65}")
    print(f"[seed={seed}] ({seed_idx+1}/{len(SEEDS)})")
    print(f"{'='*65}", flush=True)

    # ════════════════════════════════════════════════════════
    # PHASE 1: Augmented Lagrangian (escape ferromagnetic basin)
    # ════════════════════════════════════════════════════════
    mu = 0.0
    rho = 1.0

    print(f"  PHASE 1: ALM, {ALM_ROUNDS} rounds x {ALM_EVALS} evals", flush=True)

    for rd in range(ALM_ROUNDS):
        cur_mu = mu
        cur_rho = rho

        def alm_cost(th):
            sv = get_sv_gpu(th)
            eval_count[0] += 1
            E = energy_gpu(sv)
            p = parity_expect_gpu(sv)
            g = (1.0 - p) / 2.0
            return E + cur_mu * g + (cur_rho / 2.0) * g ** 2

        res = minimize(alm_cost, theta, method="L-BFGS-B",
                       options={"maxfun": ALM_EVALS, "maxiter": 300})
        theta = res.x

        sv = get_sv_gpu(theta)
        E_raw = energy_gpu(sv)
        mag, par = diagnose(sv)
        g_val = (1.0 - par) / 2.0
        err = abs(E_raw - E0) / abs(E0) * 100

        mu = mu + rho * g_val
        rho = min(rho * 2.0, 100.0)

        rate = eval_count[0] / (time.time() - t_seed)
        print(f"  R{rd+1}: E={E_raw:.4f} ({err:.1f}%)  <P>={par:.4f}  <M>={mag:.3f}  "
              f"mu={mu:.1f}  rho={rho:.0f}  evals={eval_count[0]}  {rate:.1f}ev/s", flush=True)

        # Early exit if Z2 already converged
        if abs(par - 1.0) < 0.001 and rd >= 3:
            print(f"  Z2 converged at round {rd+1}, moving to Phase 2", flush=True)
            break

    phase1_E = E_raw
    phase1_P = par
    phase1_err = err

    # ════════════════════════════════════════════════════════
    # PHASE 2: Z2-projected optimization (warm-started from ALM)
    # ════════════════════════════════════════════════════════
    print(f"\n  PHASE 2: Projected L-BFGS-B, {PROJ_EVALS} evals (warm start)", flush=True)

    res2 = minimize(projected_energy_fn, theta, method="L-BFGS-B",
                    options={"maxfun": PROJ_EVALS, "maxiter": 500})
    theta = res2.x

    sv_final = get_sv_gpu(theta)
    sv_proj = parity_project_gpu(sv_final)
    E_final = energy_gpu(sv_proj)
    mag_f, par_f = diagnose(sv_proj)
    err_f = abs(E_final - E0) / abs(E0) * 100
    elapsed = time.time() - t_seed

    print(f"\n  seed={seed} FINAL:")
    print(f"    Phase 1 (ALM):  E={phase1_E:.6f} ({phase1_err:.2f}%)  <P>={phase1_P:.4f}")
    print(f"    Phase 2 (proj): E={E_final:.6f} ({err_f:.2f}%)  <P>={par_f:.4f}  <M>={mag_f:.4f}")
    print(f"    evals={eval_count[0]}  time={elapsed:.0f}s ({elapsed/3600:.1f}h)", flush=True)

    if global_best_theta is None or E_final < global_best_E:
        global_best_E = E_final
        global_best_theta = theta.copy()
        global_best_seed = seed
        print(f"    *** NEW BEST ***", flush=True)

    results.append({
        "seed": seed,
        "phase1_E": float(phase1_E), "phase1_err": float(phase1_err), "phase1_P": float(phase1_P),
        "phase2_E": float(E_final), "phase2_err": float(err_f), "phase2_P": float(par_f),
        "phase2_M": float(mag_f),
        "evals": eval_count[0], "elapsed_s": float(elapsed),
    })

    # Save checkpoint after each seed
    checkpoint = {
        "id": "SIM-2026-008c",
        "completed_seeds": [r["seed"] for r in results],
        "results": results,
        "best_seed": global_best_seed,
        "best_E": float(global_best_E),
        "best_err": float(abs(global_best_E - E0) / abs(E0) * 100),
    }
    with open("/workspace/SIM-2026-008c.json", "w") as f:
        json.dump(checkpoint, f, indent=2)
    np.save("/workspace/theta_opt_SIM2026008c.npy", global_best_theta)
    print(f"  Checkpoint saved (seed {seed})", flush=True)

# ── Final summary ──
total_time = time.time() - T_GLOBAL
best_err = abs(global_best_E - E0) / abs(E0) * 100

print(f"\n{'='*65}")
print(f"FINAL SUMMARY")
print(f"{'='*65}")
print(f"Best: seed={global_best_seed}  E={global_best_E:.6f} ({best_err:.2f}%)")
for r in results:
    print(f"  seed={r['seed']}: phase1={r['phase1_err']:.1f}%  phase2={r['phase2_err']:.2f}%  "
          f"<P>={r['phase2_P']:.4f}  <M>={r['phase2_M']:.4f}  {r['elapsed_s']/3600:.1f}h")
print(f"Total time: {total_time:.0f}s ({total_time/3600:.1f}h)")
print(f"{'='*65}")

# Final save
output = {
    "id": "SIM-2026-008c",
    "experiment": "2phase_alm_projection_24q_5layer_mera",
    "method": "Phase 1: ALM (L-BFGS-B), Phase 2: Z2-projected L-BFGS-B",
    "n_qubits": NQ, "n_layers": NLAYERS, "n_params": NP,
    "E0_exact": E0,
    "alm_rounds": ALM_ROUNDS, "alm_evals_per_round": ALM_EVALS,
    "proj_evals": PROJ_EVALS,
    "seeds": SEEDS,
    "results": results,
    "best_seed": global_best_seed,
    "best_E": float(global_best_E),
    "best_error_pct": float(best_err),
    "total_time_s": float(total_time),
}
with open("/workspace/SIM-2026-008c.json", "w") as f:
    json.dump(output, f, indent=2)
np.save("/workspace/theta_opt_SIM2026008c.npy", global_best_theta)
print(f"\nResults saved to /workspace/SIM-2026-008c.json")
