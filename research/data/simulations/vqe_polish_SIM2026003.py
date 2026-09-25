"""
SIM-2026-003 Polish Run — Resume from best theta
==================================================
Computation Lead dispatch: extended COBYLA optimization.

Strategy:
  1. Load theta_opt_SIM2026003.npy (best from 1-hour run: E=-24.547, 2.24% error)
  2. Multi-phase COBYLA polish: rhobeg 0.10 -> 0.05 -> 0.02 -> 0.01
  3. Also try 4 perturbed-restart variants from best theta
  4. Budget: 7200s (2 hours)

Physics target: push below 1% error (E < -24.857) to get meaningful force profile.

Author: qiskit-builder (Computation Lead dispatch, SIM-2026-003 polish)
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

BUDGET_S   = 7200   # 2 hours

THETA_INIT = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy"
OUT_JSON   = "D:/quantum-worldline/research/data/simulations/SIM-2026-003.json"
OUT_NPY    = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy"

print("=" * 65)
print(f"SIM-2026-003 Polish — 5-layer {N}q MERA (resume from best)")
print(f"Starting E ~ -24.547  target < -24.857 (1% threshold)")
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

print(f"\n[1/5] Exact diagonalization N={N} OBC TFIM ...", flush=True)
t0   = time.time()
vals, _ = eigsh(build_H_sparse_obc(N), k=1, which='SA')
E0_EXACT = float(vals[0])
print(f"  E0 = {E0_EXACT:.8f}  [{time.time()-t0:.1f}s]", flush=True)
E_THRESHOLD_1PCT = E0_EXACT * (1 - 0.01)
E_THRESHOLD_2PCT = E0_EXACT * (1 - 0.02)
print(f"  1% threshold: {E_THRESHOLD_1PCT:.5f}", flush=True)
print(f"  2% threshold: {E_THRESHOLD_2PCT:.5f}", flush=True)

HAM_QISKIT = build_H_qiskit(N)

# ── Circuit ────────────────────────────────────────────────────────────────────
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

print(f"\n[2/5] Circuit: NP={NP}  CX={cx_count}  depth={depth}", flush=True)

ESTIMATOR = AerEstimator(approximation=True)

def energy(theta):
    job = ESTIMATOR.run([QC_TEMPL], [HAM_QISKIT], [theta.tolist()])
    return float(job.result().values[0])

# ── Load best theta ────────────────────────────────────────────────────────────
print(f"\n[3/5] Loading theta from {THETA_INIT} ...", flush=True)
theta_best = np.load(THETA_INIT)
E_best     = energy(theta_best)
print(f"  Loaded: E_init = {E_best:.6f}", flush=True)
sys.stdout.flush()

T_START  = time.time()
T_BUDGET = T_START + BUDGET_S

all_history = [float(E_best)]

# ── Phase 1: Perturbed restarts around best ────────────────────────────────────
# Try 5 variants of the best theta with small perturbations
print(f"\n[3/5] Phase 1: Perturbed restarts (5 variants, rhobeg=0.15) ...", flush=True)

rng = np.random.default_rng(1234)
for trial_i in range(5):
    if time.time() > T_BUDGET:
        break
    t_rem   = T_BUDGET - time.time()
    max_it  = min(3000, max(100, int(t_rem * 0.12 / 0.083)))
    noise   = rng.normal(0, 0.08, NP)  # small perturbation
    th0     = theta_best + noise
    E_init  = energy(th0)
    print(f"\n  [trial {trial_i}]  t_rem={t_rem:.0f}s  max_it={max_it}  E_init={E_init:.5f}", flush=True)
    n_before = len(all_history)
    try:
        def _cb(p):
            E = energy(np.asarray(p))
            all_history.append(E)
            return E
        res = minimize(_cb, th0, method='COBYLA',
                       options={'maxiter': max_it, 'rhobeg': 0.15, 'catol': 1e-5})
        n_ev = len(all_history) - n_before
        print(f"    E_final={res.fun:.6f}  evals={n_ev}  [{time.time()-T_START:.0f}s]", flush=True)
        if res.fun < E_best:
            E_best = res.fun
            theta_best = res.x.copy()
            print(f"    *** NEW BEST: E={E_best:.6f} ***", flush=True)
    except Exception as e:
        print(f"    Error: {e}", flush=True)
    sys.stdout.flush()

print(f"\n  After perturbed restarts: E_best = {E_best:.6f}", flush=True)

# ── Phase 2: Multi-phase tight polish ─────────────────────────────────────────
print(f"\n[4/5] Phase 2: Multi-phase polish ...", flush=True)

for rhobeg, label in [(0.08, 'coarse'), (0.04, 'medium'), (0.02, 'fine'), (0.01, 'ultrafine')]:
    if time.time() > T_BUDGET:
        print(f"  Budget exhausted before {label} phase.", flush=True)
        break
    t_rem   = T_BUDGET - time.time()
    max_it  = min(5000, max(100, int(t_rem * 0.22 / 0.083)))
    print(f"\n  [{label} rhobeg={rhobeg}]  t_rem={t_rem:.0f}s  max_it={max_it}", flush=True)
    n_before = len(all_history)
    try:
        def _cbp(p):
            E = energy(np.asarray(p))
            all_history.append(E)
            return E
        res = minimize(_cbp, theta_best, method='COBYLA',
                       options={'maxiter': max_it, 'rhobeg': rhobeg, 'catol': 1e-7})
        n_ev = len(all_history) - n_before
        print(f"    E_final={res.fun:.6f}  evals={n_ev}  [{time.time()-T_START:.0f}s]", flush=True)
        if res.fun < E_best:
            E_best = res.fun
            theta_best = res.x.copy()
            print(f"    *** NEW BEST: E={E_best:.6f} ***", flush=True)
        if E_best < E_THRESHOLD_1PCT:
            print(f"    Converged below 1%! Stopping early.", flush=True)
            break
    except Exception as e:
        print(f"    Error: {e}", flush=True)
    sys.stdout.flush()

# ── Save best theta ────────────────────────────────────────────────────────────
np.save(OUT_NPY, theta_best)
print(f"\nSaved theta: {OUT_NPY}", flush=True)

E_OPT   = E_best
pct_err = abs(E_OPT - E0_EXACT) / abs(E0_EXACT) * 100
conv_1  = bool(pct_err < 1.0)
conv_2  = bool(pct_err < 2.0)
print(f"\nE_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={pct_err:.4f}%  [{conv_1=}  {conv_2=}]", flush=True)

# ── Force profile ─────────────────────────────────────────────────────────────
print(f"\n[5/5] Force profile V(dr) ...", flush=True)

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

vac_sv = Statevector(bound_circuit(theta_best))

seps_fp, Vs_fp, Cvac_fp, Ctwo_fp = [], [], [], []
for dr in DRHO:
    j_site = ANCHOR + dr
    if j_site >= N:
        print(f"  dr={dr}: skip (j_site={j_site} >= N={N})", flush=True)
        continue
    C_vac = zz_connected(vac_sv, ANCHOR, j_site)
    two_qc = bound_circuit(theta_best)
    two_qc.ry(ANGLE, ANCHOR)
    two_qc.ry(ANGLE, j_site)
    C_two = zz_connected(Statevector(two_qc), ANCHOR, j_site)
    V = C_two - C_vac
    seps_fp.append(dr); Vs_fp.append(float(V))
    Cvac_fp.append(float(C_vac)); Ctwo_fp.append(float(C_two))
    print(f"  dr={dr}: V={V:+.6f}  C_vac={C_vac:.5f}  C_two={C_two:.5f}", flush=True)

V_analytical = [float(C1_PAPER - C2_PAPER * np.exp(-dr / L_ADS)) for dr in seps_fp]

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
            "C1": float(C1f), "C1_err": float(perr[0]),
            "C2": float(C2f), "C2_err": float(perr[1]),
            "xi": float(xif), "xi_err": float(perr[2]),
            "xi_3layer": 1.233,
            "xi_theory": float(L_ADS),
            "xi_improvement_pct": float((1 - abs(xif - L_ADS) / abs(1.233 - L_ADS)) * 100),
        }
        print(f"\n  Fit: C1={C1f:.5f}  C2={C2f:.5f}  xi={xif:.4f}", flush=True)
        print(f"  Theory={L_ADS:.4f}  3-layer={1.233}  improvement={fit_result['xi_improvement_pct']:.1f}%", flush=True)
    except Exception as e:
        fit_result = {"success": False, "error": str(e)}
        print(f"  Fit failed: {e}", flush=True)

# ── Save final JSON ────────────────────────────────────────────────────────────
T_TOTAL = time.time() - T_START

# Load and update the existing SIM-2026-003.json
try:
    with open(OUT_JSON) as f:
        structured = json.load(f)
    # Update with polish results
    old_evals = structured['vqe']['n_total_evals']
    old_E     = structured['vqe']['E_optimized']
    all_hist_json = [float(e) for e in all_history]
    structured['vqe']['E_optimized']     = float(E_OPT)
    structured['vqe']['pct_error']       = float(round(pct_err, 4))
    structured['vqe']['converged_1pct']  = bool(conv_1)
    structured['vqe']['converged_2pct']  = bool(conv_2)
    structured['vqe']['n_total_evals']   = int(old_evals + len(all_history))
    structured['vqe']['optimizer']       = "COBYLA_multistart_polish_perturbed_restart"
    structured['vqe']['energy_history']  = structured['vqe']['energy_history'] + all_hist_json
    structured['vqe']['elapsed_seconds'] = float(round(structured['vqe']['elapsed_seconds'] + T_TOTAL, 1))
    structured['force_profile']['delta_rho']   = [int(x) for x in seps_fp]
    structured['force_profile']['V_quantum']   = [float(x) for x in Vs_fp]
    structured['force_profile']['V_analytical'] = V_analytical
    structured['force_profile']['C_vac']       = [float(x) for x in Cvac_fp]
    structured['force_profile']['C_two']       = [float(x) for x in Ctwo_fp]
    structured['fit'] = {
        k: (bool(v) if isinstance(v, (bool, np.bool_))
            else float(v) if isinstance(v, (int, float, np.floating, np.integer))
            else v)
        for k, v in fit_result.items()
    }
    structured['comparison']['new_pct_error'] = float(round(pct_err, 4))
    if fit_result.get('xi'):
        structured['comparison']['xi_5layer_20q'] = float(fit_result['xi'])
    structured['polish_run'] = {
        "elapsed_seconds": float(round(T_TOTAL, 1)),
        "prev_E_opt": float(old_E),
        "new_E_opt":  float(E_OPT),
        "improvement": float(round(old_E - E_OPT, 6)),
    }
except Exception as e:
    print(f"  Warning: could not load existing JSON ({e}), creating fresh.", flush=True)
    structured = {
        "id": "SIM-2026-003",
        "description": f"VQE optimization of {N}-qubit binary MERA ({N_LAYERS} layers, {NP} params). Polish run.",
        "type": "vqe_optimization",
        "date": "2026-03-10",
        "hypothesis_id": "HYP-2026-002",
        "circuit": {"qubits": int(N), "layers": int(N_LAYERS), "n_params": int(NP),
                    "cx_count": int(cx_count), "depth": int(depth)},
        "vqe": {
            "E_optimized": float(E_OPT), "E0_exact": float(E0_EXACT),
            "pct_error": float(round(pct_err, 4)),
            "converged_1pct": bool(conv_1), "converged_2pct": bool(conv_2),
            "n_total_evals": int(len(all_history)),
            "energy_history": [float(e) for e in all_history],
            "elapsed_seconds": float(round(T_TOTAL, 1)),
        },
        "force_profile": {
            "delta_rho": [int(x) for x in seps_fp], "V_quantum": [float(x) for x in Vs_fp],
            "V_analytical": V_analytical, "C_vac": [float(x) for x in Cvac_fp],
            "C_two": [float(x) for x in Ctwo_fp], "anchor_site": int(ANCHOR),
        },
        "fit": {k: (bool(v) if isinstance(v, (bool, np.bool_))
                    else float(v) if isinstance(v, (int, float, np.floating, np.integer))
                    else v)
                for k, v in fit_result.items()},
        "feasibility": {
            "cx_count": int(cx_count), "depth": int(depth),
            "h2_error_pct": float(round((1 - 0.998**cx_count) * 100, 2)),
            "heron_r3_error_pct": float(round((1 - 0.995**cx_count) * 100, 2)),
            "h2_feasible_poc": bool((1 - 0.998**cx_count) < 0.10),
        },
        "hardware_target": "simulator_qiskit_aer",
    }

with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)

print(f"\nSaved: {OUT_JSON}", flush=True)
print(f"Total polish time: {T_TOTAL:.0f}s", flush=True)
print("=" * 65, flush=True)
print("\n--- POLISH SUMMARY ---", flush=True)
print(f"  E_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={pct_err:.4f}%", flush=True)
print(f"  Force V(dr): {Vs_fp}", flush=True)
if fit_result.get("xi"):
    print(f"  xi_fit={fit_result['xi']:.4f}  xi_theory={L_ADS:.4f}", flush=True)
print("=" * 65, flush=True)
