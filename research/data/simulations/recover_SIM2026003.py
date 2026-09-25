"""
SIM-2026-003 Recovery — Force profile + JSON save
==================================================
Reads theta_opt_SIM2026003.npy (v2 result: E=-24.667, 1.756% error)
Computes force profile V(dr=1..8) and writes SIM-2026-003.json.

v2 VQE result (from logs):
  E_opt = -24.666990  E0 = -25.107797  pct_err = 1.756%
  Seeds: 0,1,2,3,42,7,13,99,5,17 (10 seeds x 5000 evals + polish)
  Best seed: 1 (E=-24.660), then polished to -24.667
  Total evals: ~55000 (10 seeds x 5000 + 2 polish x 5000)
  Elapsed: ~7200s (2 hours)

Author: Computation Lead (recovery run after Unicode crash)
Date:   2026-03-10
"""

import sys, io
# Force UTF-8 output to avoid cp1252 encoding errors
sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

import numpy as np
import json
import time
import warnings
warnings.filterwarnings('ignore')
from scipy.optimize import curve_fit
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector

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
ANCHOR     = N // 4

THETA_PATH = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026003.npy"
OUT_JSON   = "D:/quantum-worldline/research/data/simulations/SIM-2026-003.json"

# From v2 logs (verified)
E_OPT_V2   = -24.666990
E0_EXACT   = -25.10779711162392
PCT_ERR    = abs(E_OPT_V2 - E0_EXACT) / abs(E0_EXACT) * 100
N_EVALS_V2 = 55000  # approx: 10 seeds x 5000 + 2 polish x 5000
ELAPSED_V2 = 7200.0

print("=" * 65)
print("SIM-2026-003 Recovery: force profile + JSON save")
print(f"Using theta from v2 run: E=-24.667 (1.756% error)")
print("=" * 65)

# ── Circuit (same as v2 — H gates + MERA) ─────────────────────────────────────
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

pv = ParameterVector('t', NP)
qc = QuantumCircuit(N)
qc.h(range(N))           # H-gate init (critical: same as v2)
o = 0; aq = list(range(N))
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

QC_TEMPL = qc
PV       = pv
cx_count = qc.count_ops().get('cx', 0)
depth    = qc.depth()
print(f"Circuit: NP={NP}  CX={cx_count}  depth={depth}", flush=True)

# ── Load theta ─────────────────────────────────────────────────────────────────
THETA = np.load(THETA_PATH)
print(f"Loaded theta: shape={THETA.shape}", flush=True)

def bound_circuit(theta):
    bd = {PV[i]: float(theta[i]) for i in range(NP)}
    return QC_TEMPL.assign_parameters(bd)

# ── Verify energy ──────────────────────────────────────────────────────────────
print("\nVerifying energy of loaded theta ...", flush=True)
from qiskit_aer.primitives import Estimator as AerEstimator

def build_H_qiskit(n):
    terms, coefs = [], []
    for i in range(n - 1):
        s = ['I'] * n; s[i] = 'Z'; s[i+1] = 'Z'
        terms.append(''.join(reversed(s))); coefs.append(-J)
    for i in range(n):
        s = ['I'] * n; s[i] = 'X'
        terms.append(''.join(reversed(s))); coefs.append(-H_FIELD)
    return SparsePauliOp(terms, coeffs=coefs)

HAM = build_H_qiskit(N)
est = AerEstimator(approximation=True)
job = est.run([QC_TEMPL], [HAM], [THETA.tolist()])
E_verify = float(job.result().values[0])
print(f"  E_verify = {E_verify:.6f}  (v2 log: {E_OPT_V2:.6f})", flush=True)
if abs(E_verify - E_OPT_V2) > 0.01:
    print("  WARNING: large discrepancy. Using verified energy.", flush=True)
    E_OPT = E_verify
    PCT_ERR = abs(E_OPT - E0_EXACT) / abs(E0_EXACT) * 100
else:
    E_OPT = E_OPT_V2

# ── Local magnetization check ─────────────────────────────────────────────────
vac_sv = Statevector(bound_circuit(THETA))

def z_op(i):
    s = ['I'] * N; s[i] = 'Z'
    return SparsePauliOp(''.join(reversed(s)))

magz = [float(vac_sv.expectation_value(z_op(i)).real) for i in range(N)]
magz_avg = float(np.mean(magz))
print(f"  <Z>_avg = {magz_avg:.4f}  (v1 was -0.85, v2 target: ~0)", flush=True)
print(f"  <Z> range: [{min(magz):.3f}, {max(magz):.3f}]", flush=True)

# ── ZZ connected correlators ───────────────────────────────────────────────────
def zz_connected(sv, i, j):
    def op_z(*sites):
        s = ['I'] * N
        for k in sites: s[k] = 'Z'
        return SparsePauliOp(''.join(reversed(s)))
    zi  = float(sv.expectation_value(op_z(i)).real)
    zj  = float(sv.expectation_value(op_z(j)).real)
    zij = float(sv.expectation_value(op_z(i, j)).real)
    return zij - zi * zj

print("\nZZ connected correlators (vacuum):", flush=True)
for r in range(1, 9):
    j = ANCHOR + r
    if j >= N: break
    c = zz_connected(vac_sv, ANCHOR, j)
    print(f"  r={r}: C_quantum={c:.6f}", flush=True)

# ── Force profile ─────────────────────────────────────────────────────────────
print("\nForce profile V(dr) with Ry(pi/3) hologrons ...", flush=True)

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
V_max = max(abs(v) for v in Vs_fp) if Vs_fp else 0
print(f"\n  |V|_max = {V_max:.6f}", flush=True)

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
        xi_3layer = 1.233
        xi_improvement = (1 - abs(xif - L_ADS) / abs(xi_3layer - L_ADS)) * 100
        fit_result = {
            "success": True,
            "C1": float(C1f), "C1_err": float(perr[0]),
            "C2": float(C2f), "C2_err": float(perr[1]),
            "xi": float(xif), "xi_err": float(perr[2]),
            "xi_3layer": xi_3layer,
            "xi_theory": float(L_ADS),
            "xi_improvement_pct": float(xi_improvement),
        }
        print(f"  Fit: C1={C1f:.5f}  C2={C2f:.5f}  xi={xif:.4f}", flush=True)
        print(f"  Theory l_AdS={L_ADS:.4f}  3-layer xi=1.233  improvement={xi_improvement:.1f}%", flush=True)
    except Exception as e:
        fit_result = {"success": False, "error": str(e)}
        print(f"  Fit failed: {e}", flush=True)

# ── Write SIM-2026-003.json ────────────────────────────────────────────────────
error_h2 = 1.0 - (0.998 ** cx_count)
error_h3 = 1.0 - (0.995 ** cx_count)

structured = {
    "id":             "SIM-2026-003",
    "description": (
        f"VQE optimization of {N}-qubit binary MERA ({N_LAYERS} layers, {NP} params, "
        f"H-gate init) to critical Ising GS (J=h=1, OBC N={N}). "
        f"v2: H-gate initialization, paramagnetic sector, <Z>=0. "
        f"10-seed COBYLA + 2-phase polish. AerEstimator(approx=True). "
        f"Force profile dr=1..8. Step 3 of HYP-2026-002."
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
        "architecture":        "Hgate_init_binary_MERA_5layer",
        "hologron_gate":       "Ry",
        "hologron_angle_rad":  float(ANGLE),
        "anchor_site":         int(ANCHOR),
        "causal_cone":         "5 layers -> reach 2^5=32 sites, covers dr=1..8",
        "init_note":           "H gates before MERA: |+>^N, <Z>=0 paramagnetic sector",
    },
    "vqe": {
        "optimizer":           "COBYLA_10seed_multistart_then_2phase_polish",
        "seeds":               [0, 1, 2, 3, 42, 7, 13, 99, 5, 17],
        "n_total_evals":       int(N_EVALS_V2),
        "t_per_eval_s":        0.058,
        "E_optimized":         float(E_OPT),
        "E_verify":            float(E_verify),
        "E0_exact":            float(E0_EXACT),
        "pct_error":           float(round(PCT_ERR, 4)),
        "converged_1pct":      bool(PCT_ERR < 1.0),
        "converged_2pct":      bool(PCT_ERR < 2.0),
        "elapsed_seconds":     float(ELAPSED_V2),
        "energy_history":      [],   # not stored (large; full history in v2 script logs)
        "v1_comparison": {
            "v1_E_opt":        -24.547,
            "v1_pct_err":      2.24,
            "v1_issue":        "ferromagnetic local minimum, <Z>~-0.85",
            "v2_improvement":  float(round(E_OPT - (-24.547), 4)),
        },
        "v2_seed_bests": {
            "seed_0":   -24.607, "seed_1":  -24.660, "seed_2":  -24.632,
            "seed_3":   -24.624, "seed_42": -24.646, "seed_7":  -23.450,
            "seed_13":  -24.648, "seed_99": -24.632, "seed_5":  -24.644,
            "seed_17":  -24.648,
        },
        "polish_medium": float(-24.665),
        "polish_fine":   float(E_OPT),
    },
    "force_profile": {
        "delta_rho":     [int(x) for x in seps_fp],
        "V_quantum":     [float(x) for x in Vs_fp],
        "V_analytical":  V_analytical,
        "C_vac":         [float(x) for x in Cvac_fp],
        "C_two":         [float(x) for x in Ctwo_fp],
        "anchor_site":   int(ANCHOR),
        "magz_avg":      float(magz_avg),
        "magz_range":    [float(min(magz)), float(max(magz))],
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
        "xi_5layer_20q":    (float(fit_result["xi"]) if fit_result.get("success") else None),
        "xi_theory":        float(L_ADS),
        "E_3layer_16q":     -19.642,
        "E0_3layer":        -20.016,
        "pct_err_3layer":   1.87,
        "E_5layer_20q":     float(E_OPT),
        "E0_5layer":        float(E0_EXACT),
        "pct_err_5layer":   float(round(PCT_ERR, 4)),
        "expressibility_note": (
            "5-layer ceiling ~1.76% vs 3-layer ~1.87%. Marginal improvement. "
            "Both circuits hit local-minimum basins around 2% error. "
            "Force profile requires better convergence or different architecture."
        ),
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
        "recommendation": (
            f"H2 at {error_h2*100:.1f}% error budget (CX={cx_count}) within 10% PoC threshold. "
            f"Heron R3 at {error_h3*100:.1f}% would require ZNE error mitigation."
        ),
    },
    "hardware_target":       "simulator_qiskit_aer",
    "total_elapsed_seconds": float(ELAPSED_V2),
    "theta_opt_path":        THETA_PATH,
}

with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)
print(f"\nSaved: {OUT_JSON}", flush=True)
print("=" * 65, flush=True)
print("RECOVERY SUMMARY:", flush=True)
print(f"  Circuit: {N}q/{N_LAYERS}L/{NP}p/{cx_count}CX  depth={depth}", flush=True)
print(f"  E_opt={E_OPT:.6f}  E0={E0_EXACT:.6f}  error={PCT_ERR:.3f}%", flush=True)
print(f"  <Z>_avg={magz_avg:.4f}", flush=True)
print(f"  V(dr): {[round(v,5) for v in Vs_fp]}", flush=True)
if fit_result.get("success"):
    print(f"  xi_fit={fit_result['xi']:.4f}  xi_theory={L_ADS:.4f}", flush=True)
print("=" * 65, flush=True)
