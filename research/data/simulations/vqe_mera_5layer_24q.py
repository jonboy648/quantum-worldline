"""
SIM-2026-003 — VQE: 5-layer binary MERA on 20 qubits
======================================================
Computation Lead dispatch: qiskit-builder specialist

Physics: 1D transverse-field Ising at criticality (J=h=1, OBC N=20)
Circuit: binary MERA with 5 layers of disentanglers + isometries
Goal:    Extend causal cone to dr=1..8 (full range) and push
         expressibility below 1% energy error vs N=20 exact E0.

Design notes (SIM-2026-003):
- N=24 was the target but 24q Statevector ~113s/eval (infeasible)
- N=20 uses AerEstimator(approximation=True) for exact results at ~0.1s/eval
- 5 layers on N=20 is fully supported (layer structure: 20->10->5->2->1 pairs)
- Causal cone: 5 layers gives reach dr <= 2^5 = 32 (covers dr=1..8 trivially)
- Physics is equivalent: critical TFIM with same J=h=1, same hologron protocol

Key learnings from SIM-2026-002:
- Ry hologrons ONLY (Rz commutes with ZZ -> V=0 identically)
- Multi-start COBYLA beats L-BFGS-B for >50 params
- 3-layer 16q ceiling was ~1.87% error; 5-layer target: <1%

Parameter count (N=20, 5 layers):
  L0: 10 pairs -> 10 dis (60p) + 10 iso (40p) = 100
  L1:  5 pairs ->  5 dis (30p) +  5 iso (20p) =  50
  L2:  2 pairs ->  2 dis (12p) +  2 iso  (8p) =  20
  L3:  1 pair  ->  1 dis  (6p) +  1 iso  (4p) =  10
  L4:  1 pair  ->  1 dis  (6p) +  1 iso  (4p) =  10  (from odd remainder)
  Top-level cap: +6
  Total: ~196 params (actual count via circuit inspection)

CX count: ~38
Hardware error budget (H2, 99.8% per CX): 1 - 0.998^38 ~ 7.3% (PoC OK)

Author: qiskit-builder (Computation Lead dispatch, SIM-2026-003)
Date:   2026-03-10
"""

import numpy as np
import json
import time
import sys
import warnings
warnings.filterwarnings('ignore')
from copy import deepcopy
from scipy.optimize import minimize, curve_fit
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer.primitives import Estimator as AerEstimator

# ── Configuration ──────────────────────────────────────────────────────────────
N          = 20          # qubits (5-layer MERA, causal cone dr=1..8)
N_LAYERS   = 5
J          = 1.0
H_FIELD    = 1.0
L_ADS      = 1.0 / np.log(2)     # 1.4427
C1_PAPER   = 0.080
C2_PAPER   = 13.6
ANGLE      = np.pi / 3
DRHO       = list(range(1, 9))   # dr=1..8
ANCHOR     = N // 4              # site 5

BUDGET_S   = 3600   # 1 hour max

OUT_JSON   = "D:/quantum-worldline/research/data/simulations/SIM-2026-003.json"
OUT_NPY    = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy"

print("=" * 65)
print(f"SIM-2026-003 — 5-layer {N}q MERA VQE")
print(f"Using qiskit-aer AerEstimator (exact statevector, approximation=True)")
print("=" * 65)
sys.stdout.flush()

# ── Hamiltonian ────────────────────────────────────────────────────────────────
def build_H_qiskit(n):
    terms, coefs = [], []
    for i in range(n - 1):
        s = ['I'] * n; s[i] = 'Z'; s[i+1] = 'Z'
        terms.append(''.join(reversed(s))); coefs.append(-J)
    for i in range(n):
        s = ['I'] * n; s[i] = 'X'
        terms.append(''.join(reversed(s))); coefs.append(-H_FIELD)
    return SparsePauliOp(terms, coeffs=coefs)

HAM_QISKIT = build_H_qiskit(N)

def build_H_sparse_obc(n):
    """Vectorized sparse OBC Hamiltonian for exact diagonalization."""
    from scipy.sparse import csr_matrix
    dim    = 2 ** n
    states = np.arange(dim, dtype=np.int64)
    diag   = np.zeros(dim, dtype=np.float64)
    for i in range(n - 1):
        si   = (states >> i)     & 1
        sj   = (states >> (i+1)) & 1
        diag += np.where(si == sj, -J, J)
    rows_l, cols_l, data_l = [], [], []
    for i in range(n):
        flipped = states ^ np.int64(1 << i)
        rows_l.append(states); cols_l.append(flipped); data_l.append(np.full(dim, -H_FIELD))
    rows = np.concatenate([states] + rows_l)
    cols = np.concatenate([states] + cols_l)
    data = np.concatenate([diag]   + data_l)
    return csr_matrix((data, (rows, cols)), shape=(dim, dim), dtype=np.float64)

print(f"\n[1/5] Exact diagonalization N={N} OBC TFIM ...", flush=True)
t0   = time.time()
HSPARSE = build_H_sparse_obc(N)
vals, _ = eigsh(HSPARSE, k=1, which='SA')
E0_EXACT = float(vals[0])
print(f"  E0 = {E0_EXACT:.8f}  [{time.time()-t0:.1f}s]", flush=True)

# ── Circuit construction ────────────────────────────────────────────────────────
def add_disentangler(qc, q0, q1, p, o):
    qc.ry(p[o],   q0); qc.rz(p[o+1], q0)
    qc.ry(p[o+2], q1); qc.rz(p[o+3], q1)
    qc.cx(q0, q1)
    qc.ry(p[o+4], q0); qc.ry(p[o+5], q1)
    return o + 6

def add_isometry(qc, q0, q1, p, o):
    qc.ry(p[o],   q0); qc.ry(p[o+1], q1)
    qc.cx(q0, q1)
    qc.ry(p[o+2], q0); qc.rz(p[o+3], q1)
    return o + 4

def count_params(n, n_layers):
    total = 0; active = n
    for l in range(n_layers):
        np2 = active // 2
        if np2 == 0: break
        total += np2 * 6 + np2 * 4
        active = np2 + (active % 2)
    if active >= 2: total += 6
    return total

NP = count_params(N, N_LAYERS)

def build_circuit_template():
    pv  = ParameterVector('t', NP)
    qc  = QuantumCircuit(N)
    o   = 0
    aq  = list(range(N))
    for l in range(N_LAYERS):
        na = len(aq)
        if na < 2: break
        for k in range(0, na - 1, 2):
            o = add_disentangler(qc, aq[k], aq[k+1], pv, o)
        naq = []
        for k in range(0, na - 1, 2):
            o = add_isometry(qc, aq[k], aq[k+1], pv, o)
            naq.append(aq[k])
        if na % 2: naq.append(aq[-1])
        aq = naq
    if len(aq) >= 2 and o + 6 <= NP:
        o = add_disentangler(qc, aq[0], aq[1], pv, o)
    return qc, pv

QC_TEMPL, PV = build_circuit_template()
cx_count = QC_TEMPL.count_ops().get('cx', 0)
depth    = QC_TEMPL.depth()
error_h2 = 1.0 - (0.998 ** cx_count)
error_h3 = 1.0 - (0.995 ** cx_count)

print(f"  NP={NP}  CX={cx_count}  depth={depth}", flush=True)
print(f"  H2 error: {error_h2*100:.1f}%  Heron: {error_h3*100:.1f}%", flush=True)

# ── AerEstimator (exact, fast) ────────────────────────────────────────────────
ESTIMATOR = AerEstimator(approximation=True)

def energy(theta):
    job = ESTIMATOR.run([QC_TEMPL], [HAM_QISKIT], [theta.tolist()])
    return float(job.result().values[0])

# ── Parameter initialization ───────────────────────────────────────────────────
def init_theta(seed, hadamard=False):
    rng   = np.random.default_rng(seed)
    th    = np.zeros(NP)
    o     = 0
    active = N
    for l in range(N_LAYERS):
        na = active
        if na < 2: break
        np2 = na // 2
        for _ in range(np2):
            if not hadamard:
                base_d = np.array([np.pi/2, np.pi/4, np.pi/2, np.pi/4, np.pi/3, np.pi/3])
            else:
                base_d = np.array([np.pi/4, np.pi/2, np.pi/4, np.pi/2, np.pi/4, np.pi/4])
            th[o:o+6] = base_d + rng.normal(0, 0.15, 6); o += 6
        for _ in range(np2):
            base_i = np.array([np.pi/3, np.pi/4, np.pi/3, np.pi/4])
            th[o:o+4] = base_i + rng.normal(0, 0.15, 4); o += 4
        active = np2 + (na % 2)
    if active >= 2 and o + 6 <= NP:
        base_t = np.array([np.pi/2, np.pi/4, np.pi/2, np.pi/4, np.pi/3, np.pi/4])
        th[o:o+6] = base_t + rng.normal(0, 0.15, 6)
    return th

# ── Benchmark eval speed ──────────────────────────────────────────────────────
print(f"\n[2/5] Benchmarking eval speed ...", flush=True)
_bench_theta = init_theta(0)
_bench_times = []
for _ in range(5):
    t0 = time.time()
    energy(_bench_theta)
    _bench_times.append(time.time() - t0)
T_PER_EVAL = float(np.median(_bench_times))
print(f"  {T_PER_EVAL:.3f}s per eval  ->  15000 evals = {15000*T_PER_EVAL/60:.0f} min", flush=True)

# ── VQE multi-start COBYLA ─────────────────────────────────────────────────────
print(f"\n[3/5] VQE multi-start COBYLA (budget={BUDGET_S}s) ...", flush=True)

T_START  = time.time()
T_BUDGET = T_START + BUDGET_S
SEEDS    = [42, 7, 13, 99, 0, 5, 17, 23]

all_history    = []
seed_histories = {}
best_E         = 0.0
best_th        = None
best_hd        = False

for si, seed in enumerate(SEEDS):
    if time.time() > T_BUDGET:
        print(f"  Budget exhausted after {si} seeds.", flush=True)
        break

    hd_flag = (si % 2 == 1)
    t_rem   = T_BUDGET - time.time()
    max_it  = min(5000, max(200, int(t_rem * 0.6 / T_PER_EVAL)))
    print(f"\n  [seed={seed} hd={hd_flag}]  t_rem={t_rem:.0f}s  max_it={max_it}", flush=True)

    th0 = init_theta(seed, hd_flag)
    E_i = energy(th0)
    all_history.append(E_i)
    print(f"    E_init = {E_i:.5f}", flush=True)
    sys.stdout.flush()

    n_before = len(all_history)
    try:
        def wrapped(p):
            E = energy(np.asarray(p))
            all_history.append(E)
            return E

        res = minimize(
            wrapped, th0, method='COBYLA',
            options={'maxiter': max_it, 'rhobeg': 0.25, 'catol': 1e-5}
        )
        seed_histories[seed] = all_history[n_before:]
        E1 = res.fun
        n_ev = len(all_history) - n_before
        print(f"    E_final={E1:.5f}  evals={n_ev}  [{time.time()-T_START:.0f}s]", flush=True)
        if E1 < best_E:
            best_E = E1; best_th = res.x.copy(); best_hd = hd_flag
        sys.stdout.flush()
    except Exception as e:
        print(f"    Error: {e}", flush=True)

print(f"\n  Best after multi-start: E={best_E:.6f}", flush=True)

# ── COBYLA polish ─────────────────────────────────────────────────────────────
if best_th is not None and time.time() < T_BUDGET:
    t_rem   = T_BUDGET - time.time()
    max_it_p = min(3000, max(100, int(t_rem / T_PER_EVAL)))
    print(f"\n  [Polish max_it={max_it_p}]", flush=True)
    n_before = len(all_history)
    try:
        def wrapped_p(p):
            E = energy(np.asarray(p))
            all_history.append(E)
            return E
        res_p = minimize(
            wrapped_p, best_th, method='COBYLA',
            options={'maxiter': max_it_p, 'rhobeg': 0.05, 'catol': 1e-6}
        )
        E_pol = res_p.fun
        print(f"  Polish: E={E_pol:.6f}  evals={len(all_history)-n_before}", flush=True)
        if E_pol < best_E:
            best_E = E_pol; best_th = res_p.x.copy()
    except Exception as e:
        print(f"  Polish error: {e}", flush=True)

E_OPT   = best_E
THETA   = best_th if best_th is not None else init_theta(0)
pct_err = abs(E_OPT - E0_EXACT) / abs(E0_EXACT) * 100
conv_1  = bool(pct_err < 1.0)
conv_2  = bool(pct_err < 2.0)
print(f"\nE_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={pct_err:.3f}%", flush=True)
np.save(OUT_NPY, THETA)

# ── Force profile (exact Statevector for precision) ───────────────────────────
print(f"\n[4/5] Force profile V(dr) with Ry(pi/3) hologrons ...", flush=True)

def zz_connected(sv, i, j):
    def op(*sites):
        s = ['I'] * N
        for k in sites: s[k] = 'Z'
        return SparsePauliOp(''.join(reversed(s)))
    zi  = float(sv.expectation_value(op(i)).real)
    zj  = float(sv.expectation_value(op(j)).real)
    zij = float(sv.expectation_value(op(i, j)).real)
    return zij - zi * zj

def bound_circuit(theta):
    bd = {PV[i]: float(theta[i]) for i in range(NP)}
    return QC_TEMPL.assign_parameters(bd)

vac_sv = Statevector(bound_circuit(THETA))

seps_fp, Vs_fp, Cvac_fp, Ctwo_fp = [], [], [], []
for dr in DRHO:
    j_site = ANCHOR + dr
    if j_site >= N:
        print(f"  dr={dr}: skip (j_site={j_site} >= N={N})", flush=True)
        continue
    C_vac = zz_connected(vac_sv, ANCHOR, j_site)

    two_qc = bound_circuit(THETA)
    two_qc.ry(ANGLE, ANCHOR)
    two_qc.ry(ANGLE, j_site)
    C_two = zz_connected(Statevector(two_qc), ANCHOR, j_site)

    V = C_two - C_vac
    seps_fp.append(dr); Vs_fp.append(float(V))
    Cvac_fp.append(float(C_vac)); Ctwo_fp.append(float(C_two))
    print(f"  dr={dr}: V={V:+.6f}  C_vac={C_vac:.5f}  C_two={C_two:.5f}", flush=True)

V_analytical = [float(C1_PAPER - C2_PAPER * np.exp(-dr / L_ADS)) for dr in seps_fp]

# ── Fit ───────────────────────────────────────────────────────────────────────
def force_model(x, C1, C2, xi):
    return C1 - C2 * np.exp(-np.array(x, float) / xi)

fit_result = {}
if len(seps_fp) >= 3:
    try:
        popt, pcov = curve_fit(
            force_model, seps_fp, Vs_fp,
            p0=[C1_PAPER, C2_PAPER, L_ADS],
            bounds=([-5, -200, 0.1], [5, 200, 10]),
            maxfev=20000
        )
        perr = np.sqrt(np.diag(pcov))
        C1f, C2f, xif = popt
        fit_result = {
            "success": True,
            "C1":     float(C1f),   "C1_err": float(perr[0]),
            "C2":     float(C2f),   "C2_err": float(perr[1]),
            "xi":     float(xif),   "xi_err": float(perr[2]),
            "xi_3layer": 1.233,
            "xi_theory": float(L_ADS),
            "xi_improvement_pct": float((1 - abs(xif - L_ADS) / abs(1.233 - L_ADS)) * 100),
        }
        print(f"\n  Fit: C1={C1f:.5f}  C2={C2f:.5f}  xi={xif:.4f}", flush=True)
        print(f"  Theory l_AdS={L_ADS:.4f}  3-layer xi=1.233  improvement: {fit_result['xi_improvement_pct']:.1f}%", flush=True)
    except Exception as e:
        fit_result = {"success": False, "error": str(e)}
        print(f"  Fit failed: {e}", flush=True)

# ── Save ──────────────────────────────────────────────────────────────────────
print(f"\n[5/5] Saving ...", flush=True)
T_TOTAL = time.time() - T_START

structured = {
    "id":             "SIM-2026-003",
    "description":    (
        f"VQE optimization of {N}-qubit binary MERA ({N_LAYERS} layers, {NP} params) "
        f"to critical Ising ground state (J=h=1, OBC N={N}). "
        f"Multi-start COBYLA. AerEstimator(approximation=True) for exact statevector. "
        f"Force profile at dr=1..8 (full causal cone). Step 3 of HYP-2026-002."
    ),
    "type":           "vqe_optimization",
    "date":           "2026-03-10",
    "hypothesis_id":  "HYP-2026-002",
    "paper_ref":      "PAPER-2026-003",
    "step":           3,
    "backend":        "qiskit_aer_estimator_approximation_true",
    "circuit": {
        "qubits":              int(N),
        "layers":              int(N_LAYERS),
        "n_params":            int(NP),
        "cx_count":            int(cx_count),
        "depth":               int(depth),
        "architecture":        "binary_MERA_disentanglers_isometries",
        "hologron_gate":       "Ry",
        "hologron_angle_rad":  float(ANGLE),
        "anchor_site":         int(ANCHOR),
        "causal_cone":         f"5 layers -> reach 2^5=32 sites, covers dr=1..{max(seps_fp) if seps_fp else 8}",
    },
    "vqe": {
        "optimizer":          "COBYLA_multistart_then_polish",
        "seeds":              SEEDS[:len(seed_histories)],
        "n_total_evals":      int(len(all_history)),
        "t_per_eval_s":       float(round(T_PER_EVAL, 3)),
        "E_optimized":        float(E_OPT),
        "E0_exact":           float(E0_EXACT),
        "pct_error":          float(round(pct_err, 4)),
        "converged_1pct":     bool(conv_1),
        "converged_2pct":     bool(conv_2),
        "best_hd":            bool(best_hd),
        "elapsed_seconds":    float(round(T_TOTAL, 1)),
        "energy_history":     [float(e) for e in all_history],
        "seed_history_lengths": {str(k): len(v) for k, v in seed_histories.items()},
    },
    "force_profile": {
        "delta_rho":      [int(x) for x in seps_fp],
        "V_quantum":      [float(x) for x in Vs_fp],
        "V_analytical":   V_analytical,
        "C_vac":          [float(x) for x in Cvac_fp],
        "C_two":          [float(x) for x in Ctwo_fp],
        "anchor_site":    int(ANCHOR),
    },
    "fit": {
        k: (bool(v) if isinstance(v, (bool, np.bool_))
            else float(v) if isinstance(v, (int, float, np.floating, np.integer))
            else v)
        for k, v in fit_result.items()
    },
    "comparison": {
        "paper_C1":         float(C1_PAPER),
        "paper_C2":         float(C2_PAPER),
        "paper_l_AdS":      float(L_ADS),
        "xi_3layer_16q":    1.233,
        "xi_5layer_20q":    (float(fit_result["xi"]) if fit_result.get("xi") else None),
        "xi_theory":        float(L_ADS),
        "prior_pct_error":  1.87,
        "new_pct_error":    float(round(pct_err, 4)),
        "causal_cone_note": "3-layer dr=1..3 only; 5-layer extends to full dr=1..8",
    },
    "feasibility": {
        "cx_count":              int(cx_count),
        "depth":                 int(depth),
        "n_params":              int(NP),
        "h2_error_pct":          float(round(error_h2 * 100, 2)),
        "heron_r3_error_pct":    float(round(error_h3 * 100, 2)),
        "h2_feasible_poc":       bool(error_h2 < 0.10),
        "hardware_target":       "simulator_qiskit_aer",
        "recommendation":        (
            f"H2 at {error_h2*100:.1f}% error budget (CX={cx_count}) is within 10% PoC threshold. "
            "IBM Heron R3 at {error_h3*100:.1f}% requires ZNE error mitigation."
        ),
    },
    "hardware_target":      "simulator_qiskit_aer",
    "total_elapsed_seconds": float(round(T_TOTAL, 1)),
    "theta_opt_path":       OUT_NPY,
}

with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)
print(f"Saved: {OUT_JSON}", flush=True)
print(f"Saved theta: {OUT_NPY}", flush=True)
print(f"Total time: {T_TOTAL:.0f}s", flush=True)
print("=" * 65, flush=True)
print("\n--- STRUCTURED OUTPUT SUMMARY ---", flush=True)
print(f"  Circuit: {N}q / {N_LAYERS}L / {NP}p / {cx_count}CX / depth={depth}", flush=True)
print(f"  E_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={pct_err:.3f}%", flush=True)
print(f"  Force V(dr): {Vs_fp}", flush=True)
if fit_result.get("xi"):
    print(f"  xi_fit={fit_result['xi']:.4f}  xi_theory={L_ADS:.4f}", flush=True)
print("=" * 65, flush=True)
