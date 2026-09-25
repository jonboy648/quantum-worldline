"""
SIM-2026-003 v2 — VQE: 5-layer binary MERA on 20 qubits (corrected)
=====================================================================
Computation Lead dispatch: qiskit-builder specialist (v2 — corrected init)

FIX FROM v1: v1 init_theta biased the MERA toward ferromagnetic state
  (large <Z_i> ~ -0.85). TFIM critical ground state has <Z_i> ≈ 0.
  Fix: add H gates BEFORE MERA to initialize in paramagnetic sector.
  H-gate init + theta=0 gives E=-20, <Z>=0 — correct starting basin.

Physics: 1D transverse-field Ising at criticality (J=h=1, OBC N=20)
Circuit: H^N + binary MERA, 5 layers, 190 parameters, 38 CX
Goal:    E error < 1%, meaningful V(dr=1..8), xi converging to l_AdS

Key learnings:
- Ry hologrons ONLY (Rz commutes with ZZ -> V=0)
- H-gate init breaks Z2 symmetry correctly for TFIM critical state
- Multi-start COBYLA with rhobeg=0.25 for exploration
- Starting from paramagnetic sector avoids ferromagnetic basin trap

Author: qiskit-builder (Computation Lead dispatch, SIM-2026-003)
Date:   2026-03-10
"""

import numpy as np
import json
import time
import sys
import warnings
warnings.filterwarnings('ignore')
from scipy.optimize import minimize, curve_fit
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector
from qiskit_aer.primitives import Estimator as AerEstimator

# ── Configuration ──────────────────────────────────────────────────────────────
N          = 20
N_LAYERS   = 5
J          = 1.0
H_FIELD    = 1.0
L_ADS      = 1.0 / np.log(2)
C1_PAPER   = 0.080
C2_PAPER   = 13.6
ANGLE      = np.pi / 3
DRHO       = list(range(1, 9))
ANCHOR     = N // 4              # site 5

BUDGET_S   = 7200    # 2 hours (v2 extended budget)

OUT_JSON   = "D:/quantum-worldline/research/data/simulations/SIM-2026-003.json"
OUT_NPY    = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy"

print("=" * 65)
print(f"SIM-2026-003 v2 — 5-layer {N}q MERA VQE (H-gate init)")
print(f"Fix: H gates before MERA -> paramagnetic sector, <Z>=0")
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
    dim    = 2 ** n
    states = np.arange(dim, dtype=np.int64)
    diag   = np.zeros(dim, dtype=np.float64)
    for i in range(n - 1):
        si   = (states >> i) & 1
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

print(f"\n[1/6] Exact diagonalization N={N} OBC TFIM ...", flush=True)
t0   = time.time()
vals, _ = eigsh(build_H_sparse_obc(N), k=1, which='SA')
E0_EXACT = float(vals[0])
print(f"  E0 = {E0_EXACT:.8f}  [{time.time()-t0:.1f}s]", flush=True)
E_1PCT = E0_EXACT * (1 - 0.01)
E_2PCT = E0_EXACT * (1 - 0.02)
print(f"  1% target: E < {E_1PCT:.5f}", flush=True)

# ── Circuit (H-gate initialized) ───────────────────────────────────────────────
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

def build_circuit_template():
    pv  = ParameterVector('t', NP)
    qc  = QuantumCircuit(N)
    qc.h(range(N))          # KEY FIX: H gates -> paramagnetic sector
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

print(f"\n[2/6] Circuit: NP={NP}  CX={cx_count}  depth={depth}", flush=True)
print(f"  H2 error: {error_h2*100:.1f}%  Heron: {error_h3*100:.1f}%", flush=True)

# Verify init: theta=0 should give E=-20 and <Z>=0
ESTIMATOR = AerEstimator(approximation=True)

def energy(theta):
    job = ESTIMATOR.run([QC_TEMPL], [HAM_QISKIT], [theta.tolist()])
    return float(job.result().values[0])

print(f"\n[3/6] Verifying initialization ...", flush=True)
E_init_check = energy(np.zeros(NP))
print(f"  E(theta=0) = {E_init_check:.4f}  (expect -20.0 for |+>^N)", flush=True)
if abs(E_init_check + 20.0) > 0.5:
    print("  WARNING: init energy unexpected. Check H-gate placement.", flush=True)
sys.stdout.flush()

# ── Benchmark ─────────────────────────────────────────────────────────────────
print(f"\n[3/6] Benchmarking eval speed ...", flush=True)
_t = []
for _ in range(5):
    t0 = time.time(); energy(np.random.randn(NP) * 0.1); _t.append(time.time()-t0)
T_PER_EVAL = float(np.median(_t))
print(f"  {T_PER_EVAL:.3f}s/eval  ->  budget={BUDGET_S}s = ~{BUDGET_S/T_PER_EVAL:.0f} evals", flush=True)

# ── Parameter initialization ───────────────────────────────────────────────────
def init_theta(seed):
    """Small random perturbations around 0 (near-identity MERA on top of |+>^N)."""
    rng = np.random.default_rng(seed)
    return rng.normal(0, 0.3, NP)

# ── VQE multi-start COBYLA ─────────────────────────────────────────────────────
print(f"\n[4/6] VQE multi-start COBYLA (budget={BUDGET_S}s) ...", flush=True)

T_START  = time.time()
T_BUDGET = T_START + BUDGET_S
SEEDS    = [0, 1, 2, 3, 42, 7, 13, 99, 5, 17]

all_history    = []
seed_histories = {}
best_E         = 0.0
best_th        = None

for si, seed in enumerate(SEEDS):
    if time.time() > T_BUDGET:
        print(f"  Budget exhausted after {si} seeds.", flush=True)
        break

    t_rem   = T_BUDGET - time.time()
    max_it  = min(5000, max(200, int(t_rem * 0.55 / T_PER_EVAL)))
    th0     = init_theta(seed)
    E_i     = energy(th0)
    all_history.append(E_i)
    print(f"\n  [seed={seed}]  t_rem={t_rem:.0f}s  max_it={max_it}  E_init={E_i:.4f}", flush=True)
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
            best_E = E1; best_th = res.x.copy()
            print(f"    *** NEW BEST ***", flush=True)
        sys.stdout.flush()

        if best_E < E_1PCT:
            print(f"  Converged below 1%! Stopping early.", flush=True)
            break
    except Exception as e:
        print(f"    Error: {e}", flush=True)

print(f"\n  Best after multi-start: E={best_E:.6f}", flush=True)

# ── COBYLA polish ─────────────────────────────────────────────────────────────
if best_th is not None and time.time() < T_BUDGET:
    for rhobeg, label in [(0.08, 'medium'), (0.03, 'fine')]:
        if time.time() > T_BUDGET: break
        t_rem    = T_BUDGET - time.time()
        max_it_p = min(5000, max(100, int(t_rem * 0.45 / T_PER_EVAL)))
        print(f"\n  [Polish {label} rhobeg={rhobeg}  max_it={max_it_p}]", flush=True)
        n_before = len(all_history)
        try:
            def wrapped_p(p):
                E = energy(np.asarray(p))
                all_history.append(E)
                return E
            res_p = minimize(
                wrapped_p, best_th, method='COBYLA',
                options={'maxiter': max_it_p, 'rhobeg': rhobeg, 'catol': 1e-7}
            )
            E_pol = res_p.fun
            print(f"  Polish {label}: E={E_pol:.6f}  evals={len(all_history)-n_before}", flush=True)
            if E_pol < best_E:
                best_E = E_pol; best_th = res_p.x.copy()
        except Exception as e:
            print(f"  Polish error: {e}", flush=True)
        sys.stdout.flush()

E_OPT   = best_E
THETA   = best_th if best_th is not None else np.zeros(NP)
pct_err = abs(E_OPT - E0_EXACT) / abs(E0_EXACT) * 100
conv_1  = bool(pct_err < 1.0)
conv_2  = bool(pct_err < 2.0)
print(f"\nE_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={pct_err:.3f}%", flush=True)
np.save(OUT_NPY, THETA)

# ── Force profile ─────────────────────────────────────────────────────────────
print(f"\n[5/6] Force profile V(dr) with Ry(pi/3) hologrons ...", flush=True)

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

# Verify magnetization of optimized state
def z_op_sv(sv, i):
    s = ['I'] * N; s[i] = 'Z'
    return float(sv.expectation_value(SparsePauliOp(''.join(reversed(s)))).real)
magz_avg = np.mean([z_op_sv(vac_sv, i) for i in range(N)])
print(f"  <Z> avg = {magz_avg:.4f}  (expect ≈ 0 for paramagnetic state)", flush=True)

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
if len(seps_fp) >= 3 and any(abs(v) > 0.001 for v in Vs_fp):
    try:
        # Initial guess: use paper values; bounds are loose
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
            "C1": float(C1f), "C1_err": float(perr[0]),
            "C2": float(C2f), "C2_err": float(perr[1]),
            "xi": float(xif), "xi_err": float(perr[2]),
            "xi_3layer": 1.233,
            "xi_theory": float(L_ADS),
            "xi_improvement_pct": float((1 - abs(xif - L_ADS) / abs(1.233 - L_ADS)) * 100),
        }
        print(f"\n  Fit: C1={C1f:.5f}  C2={C2f:.5f}  xi={xif:.4f}", flush=True)
        print(f"  Theory l_AdS={L_ADS:.4f}  3-layer xi=1.233", flush=True)
    except Exception as e:
        fit_result = {"success": False, "error": str(e)}
        print(f"  Fit: {e}", flush=True)
else:
    fit_result = {"success": False, "error": "V(dr) signals too small to fit — VQE state not converged enough"}
    print(f"  Fit skipped: V signals too small", flush=True)

# ── Save ──────────────────────────────────────────────────────────────────────
print(f"\n[6/6] Saving ...", flush=True)
T_TOTAL = time.time() - T_START

structured = {
    "id":             "SIM-2026-003",
    "description":    (
        f"VQE optimization of {N}-qubit binary MERA ({N_LAYERS} layers, {NP} params, "
        f"H-gate init) to critical Ising ground state (J=h=1, OBC N={N}). "
        f"Multi-start COBYLA. AerEstimator(approximation=True). "
        f"v2: H-gate initialization for correct paramagnetic starting sector. "
        f"Force profile at dr=1..8 (full 5-layer causal cone). Step 3 of HYP-2026-002."
    ),
    "type":           "vqe_optimization",
    "date":           "2026-03-10",
    "hypothesis_id":  "HYP-2026-002",
    "paper_ref":      "PAPER-2026-003",
    "step":           3,
    "version":        "v2_hgate_init",
    "backend":        "qiskit_aer_estimator_approximation_true",
    "circuit": {
        "qubits":              int(N),
        "layers":              int(N_LAYERS),
        "n_params":            int(NP),
        "cx_count":            int(cx_count),
        "depth":               int(depth),
        "architecture":        "Hgate_init_binary_MERA_disentanglers_isometries",
        "hologron_gate":       "Ry",
        "hologron_angle_rad":  float(ANGLE),
        "anchor_site":         int(ANCHOR),
        "causal_cone":         f"5 layers -> reach 2^5=32, covers dr=1..{max(seps_fp) if seps_fp else 8}",
        "init_note":           "H gates before MERA: |+>^N basis, <Z>=0 paramagnetic sector",
    },
    "vqe": {
        "optimizer":              "COBYLA_multistart_then_polish",
        "seeds":                  SEEDS[:len(seed_histories)],
        "n_total_evals":          int(len(all_history)),
        "t_per_eval_s":           float(round(T_PER_EVAL, 3)),
        "E_optimized":            float(E_OPT),
        "E0_exact":               float(E0_EXACT),
        "pct_error":              float(round(pct_err, 4)),
        "converged_1pct":         bool(conv_1),
        "converged_2pct":         bool(conv_2),
        "elapsed_seconds":        float(round(T_TOTAL, 1)),
        "energy_history":         [float(e) for e in all_history],
        "seed_history_lengths":   {str(k): len(v) for k, v in seed_histories.items()},
        "v1_comparison": {
            "v1_E_opt":    -24.547,
            "v1_pct_err":  2.24,
            "v1_magnetization_issue": "v1 converged to ferromagnetic state, <Z>~-0.85"
        },
    },
    "force_profile": {
        "delta_rho":     [int(x) for x in seps_fp],
        "V_quantum":     [float(x) for x in Vs_fp],
        "V_analytical":  V_analytical,
        "C_vac":         [float(x) for x in Cvac_fp],
        "C_two":         [float(x) for x in Ctwo_fp],
        "anchor_site":   int(ANCHOR),
        "magz_avg":      float(magz_avg),
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
        "v1_bug_note":      "v1 wrong init (ferromagnetic), v2 fixed with H-gate init",
    },
    "feasibility": {
        "cx_count":              int(cx_count),
        "depth":                 int(depth),
        "n_params":              int(NP),
        "h2_error_pct":          float(round(error_h2 * 100, 2)),
        "heron_r3_error_pct":    float(round(error_h3 * 100, 2)),
        "h2_feasible_poc":       bool(error_h2 < 0.10),
        "hardware_target":       "simulator_qiskit_aer",
    },
    "hardware_target":       "simulator_qiskit_aer",
    "total_elapsed_seconds": float(round(T_TOTAL, 1)),
    "theta_opt_path":        OUT_NPY,
}

with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)
np.save(OUT_NPY, THETA)

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
print(f"  <Z>_avg = {magz_avg:.4f}", flush=True)
print("=" * 65, flush=True)
