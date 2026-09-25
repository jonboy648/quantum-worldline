"""
Classical Baseline — SIM-2026-003 (N=24 TFIM)
===============================================
Classical Simulator specialist output for Computation Lead.

Computes:
  - Exact diagonalization N=24 TFIM, OBC  (matches quantum circuit)
  - Exact diagonalization N=24 TFIM, PBC  (translational symmetry baseline)
  - ZZ connected correlators C(r) at all separations r=1..12
  - Holographic force profile V(r) using exact Ry perturbation (dr=1..8)
  - Power-law fit (critical exponent eta) + exponential fit (xi)
  - Comparison with l_AdS = 1/log(2)

SIM:  SIM-2026-003 (classical baseline component)
Date: 2026-03-10
"""

import numpy as np
import json
import time
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from scipy.optimize import curve_fit

# ── Configuration ──────────────────────────────────────────────────────────────
N           = 20          # matches VQE circuit (20q 5-layer MERA)
J           = 1.0
H_FIELD     = 1.0
L_ADS       = 1.0 / np.log(2)
ANCHOR      = N // 4   # site 5
ANGLE       = np.pi / 3
MAX_SEP     = 10       # N/2 = 10 for PBC
OUT_JSON    = "D:/quantum-worldline/research/data/simulations/classical_baseline_SIM2026003.json"

print("=" * 65)
print(f"Classical ED Baseline — N={N} TFIM, OBC + PBC")
print("=" * 65)


# ── Hamiltonian construction ───────────────────────────────────────────────────
def build_H(n, j, h, periodic=False):
    """
    Vectorized sparse Hamiltonian for N-site TFIM.
    Uses integer bit manipulation on state arrays — O(N * 2^N) memory, no Python loops.
    Safe for N=24 (~16M states); avoid for N>26 (memory limited).
    """
    from scipy.sparse import csr_matrix
    dim    = 2 ** n
    states = np.arange(dim, dtype=np.int64)

    rows_all, cols_all, data_all = [], [], []

    # ZZ terms (diagonal)
    bonds = list(range(n - 1))
    if periodic:
        bonds.append(n - 1)
    # Accumulate diagonal in a dense vector, then convert
    diag = np.zeros(dim, dtype=np.float64)
    for i in bonds:
        js   = (i + 1) % n
        si   = (states >> i)  & 1
        sj   = (states >> js) & 1
        sign = np.where(si == sj, 1, -1).astype(np.float64)
        diag += -j * sign

    # X terms (off-diagonal): flip bit i -> connects state s to s^(1<<i)
    for i in range(n):
        flipped = states ^ np.int64(1 << i)
        rows_all.append(states)
        cols_all.append(flipped)
        data_all.append(np.full(dim, -h))

    rows = np.concatenate([states] + rows_all)
    cols = np.concatenate([states] + cols_all)
    data = np.concatenate([diag] + data_all)

    H = csr_matrix((data, (rows, cols)), shape=(dim, dim), dtype=np.float64)
    return H


# ── Correlators ───────────────────────────────────────────────────────────────
def _state_array(n):
    """Integer array [0, 1, ..., 2^n - 1] for vectorized bit ops."""
    return np.arange(2 ** n, dtype=np.int64)

_STATES = None  # cached after first build

def _get_states(n):
    global _STATES
    if _STATES is None or len(_STATES) != 2**n:
        _STATES = _state_array(n)
    return _STATES


def zz_connected_exact(gs, n, i, j):
    """<ZiZj>_c = <ZiZj> - <Zi><Zj>  from exact GS vector. Vectorized."""
    states = _get_states(n)
    probs  = np.abs(gs) ** 2
    si     = np.where((states >> i) & 1, -1.0,  1.0)
    sj     = np.where((states >> j) & 1, -1.0,  1.0)
    zij    = float(np.dot(probs, si * sj))
    zi     = float(np.dot(probs, si))
    zj     = float(np.dot(probs, sj))
    return zij - zi * zj


def apply_ry_vec(psi, n, site, theta):
    """Apply Ry(theta) to statevector psi at given site. Vectorized."""
    c      = np.cos(theta / 2)
    s      = np.sin(theta / 2)
    states = _get_states(n)
    bit    = ((states >> site) & 1).astype(bool)
    paired = states ^ np.int64(1 << site)
    out    = np.zeros_like(psi)
    # bit==0: out[s] += c*psi[s],  out[paired] += s*psi[s]
    # bit==1: out[s] += c*psi[s],  out[paired] -= s*psi[s]
    np.add.at(out, states[~bit], c * psi[~bit])
    np.add.at(out, paired[~bit],  s * psi[~bit])
    np.add.at(out, states[bit],  c * psi[bit])
    np.add.at(out, paired[bit], -s * psi[bit])
    return out


def perturbed_correlator(gs, n, anchor, j_site, theta):
    """ZZ connected correlator after Ry(theta) at anchor and j_site."""
    psi = gs.copy()
    psi = apply_ry_vec(psi, n, anchor, theta)
    psi = apply_ry_vec(psi, n, j_site, theta)
    psi /= np.linalg.norm(psi)
    return zz_connected_exact(psi, n, anchor, j_site)


# ── Diagonalize OBC ───────────────────────────────────────────────────────────
print(f"\n[1/5] OBC N={N} TFIM ...", flush=True)
t0       = time.time()
H_obc    = build_H(N, J, H_FIELD, periodic=False)
vals_obc, vecs_obc = eigsh(H_obc, k=2, which='SA')
E0_obc   = float(vals_obc[0])
E1_obc   = float(vals_obc[1])
gs_obc   = vecs_obc[:, 0]
gap_obc  = E1_obc - E0_obc
print(f"  E0={E0_obc:.8f}  E1={E1_obc:.8f}  gap={gap_obc:.6f}  [{time.time()-t0:.1f}s]", flush=True)

# ── Diagonalize PBC ───────────────────────────────────────────────────────────
print(f"\n[2/5] PBC N={N} TFIM ...", flush=True)
t0       = time.time()
H_pbc    = build_H(N, J, H_FIELD, periodic=True)
vals_pbc, vecs_pbc = eigsh(H_pbc, k=2, which='SA')
E0_pbc   = float(vals_pbc[0])
E1_pbc   = float(vals_pbc[1])
gs_pbc   = vecs_pbc[:, 0]
gap_pbc  = E1_pbc - E0_pbc
print(f"  E0={E0_pbc:.8f}  E1={E1_pbc:.8f}  gap={gap_pbc:.6f}  [{time.time()-t0:.1f}s]", flush=True)

# ── Correlators (OBC) ─────────────────────────────────────────────────────────
print(f"\n[3/5] ZZ correlators (OBC, anchor={ANCHOR}) ...", flush=True)
t0          = time.time()
seps        = list(range(1, MAX_SEP + 1))
C_obc       = []
C_pert_obc  = []
V_obc       = []

for r in seps:
    j_site = ANCHOR + r
    if j_site >= N:
        break
    c_vac  = zz_connected_exact(gs_obc, N, ANCHOR, j_site)
    c_pert = perturbed_correlator(gs_obc, N, ANCHOR, j_site, ANGLE)
    V      = c_pert - c_vac
    C_obc.append(float(c_vac))
    C_pert_obc.append(float(c_pert))
    V_obc.append(float(V))
    print(f"  r={r:2d}: C={c_vac:.6f}  V={V:+.6f}", flush=True)

seps_obc = seps[:len(C_obc)]
print(f"  [{time.time()-t0:.1f}s]", flush=True)

# ── Correlators (PBC) ─────────────────────────────────────────────────────────
print(f"\n[4/5] ZZ correlators (PBC, anchor={ANCHOR}) ...", flush=True)
t0         = time.time()
C_pbc      = []
C_pert_pbc = []
V_pbc      = []
seps_pbc   = list(range(1, N // 2 + 1))

for r in seps_pbc:
    j_site = (ANCHOR + r) % N
    c_vac  = zz_connected_exact(gs_pbc, N, ANCHOR, j_site)
    c_pert = perturbed_correlator(gs_pbc, N, ANCHOR, j_site, ANGLE)
    V      = c_pert - c_vac
    C_pbc.append(float(c_vac))
    C_pert_pbc.append(float(c_pert))
    V_pbc.append(float(V))
    print(f"  r={r:2d}: C={c_vac:.6f}  V={V:+.6f}", flush=True)

print(f"  [{time.time()-t0:.1f}s]", flush=True)

# ── Fits ──────────────────────────────────────────────────────────────────────
print(f"\n[5/5] Fitting ...", flush=True)

def power_law(r, A, eta): return A * r ** (-eta)
def exp_decay(r, A, B, xi): return A - B * np.exp(-r / xi)
def force_model(r, C1, C2, xi): return C1 - C2 * np.exp(-np.array(r, float) / xi)

fits = {}

# OBC correlator fits
x_obc = np.array(seps_obc[:8], dtype=float)  # dr=1..8 for fair comparison
y_obc = np.array(C_obc[:8])

try:
    popt, _ = curve_fit(power_law, x_obc, y_obc, p0=[0.5, 0.25])
    fits['power_law_obc'] = {"A": float(popt[0]), "eta": float(popt[1]), "theory_eta": 0.25}
    print(f"  OBC power-law: A={popt[0]:.4f} eta={popt[1]:.4f} (theory 0.25)", flush=True)
except Exception as e:
    fits['power_law_obc'] = {"error": str(e)}

try:
    popt, _ = curve_fit(exp_decay, x_obc, y_obc, p0=[0.0, 0.5, 3.0])
    fits['exp_obc'] = {"A": float(popt[0]), "B": float(popt[1]), "xi": float(popt[2]), "l_AdS": L_ADS}
    print(f"  OBC exp: xi={popt[2]:.4f}  (l_AdS={L_ADS:.4f})", flush=True)
except Exception as e:
    fits['exp_obc'] = {"error": str(e)}

# OBC force profile fit
x_v = np.array(seps_obc[:8], dtype=float)
y_v = np.array(V_obc[:8])
try:
    popt, pcov = curve_fit(
        force_model, x_v, y_v,
        p0=[0.08, 13.6, L_ADS],
        bounds=([-5, -200, 0.1], [5, 200, 10]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    fits['force_obc'] = {
        "C1": float(popt[0]), "C1_err": float(perr[0]),
        "C2": float(popt[1]), "C2_err": float(perr[1]),
        "xi": float(popt[2]), "xi_err": float(perr[2]),
        "paper_C1": 0.080, "paper_C2": 13.6, "paper_l_AdS": L_ADS,
    }
    print(f"  OBC force: C1={popt[0]:.4f} C2={popt[1]:.4f} xi={popt[2]:.4f}", flush=True)
except Exception as e:
    fits['force_obc'] = {"error": str(e)}

# PBC force profile fit
x_vp = np.array(seps_pbc[:8], dtype=float)
y_vp = np.array(V_pbc[:8])
try:
    popt, pcov = curve_fit(
        force_model, x_vp, y_vp,
        p0=[0.08, 13.6, L_ADS],
        bounds=([-5, -200, 0.1], [5, 200, 10]),
        maxfev=20000
    )
    perr = np.sqrt(np.diag(pcov))
    fits['force_pbc'] = {
        "C1": float(popt[0]), "C1_err": float(perr[0]),
        "C2": float(popt[1]), "C2_err": float(perr[1]),
        "xi": float(popt[2]), "xi_err": float(perr[2]),
    }
    print(f"  PBC force: C1={popt[0]:.4f} C2={popt[1]:.4f} xi={popt[2]:.4f}", flush=True)
except Exception as e:
    fits['force_pbc'] = {"error": str(e)}

T_TOTAL = time.time()

structured = {
    "agent":        "classical-simulator",
    "sim_id":       "SIM-2026-003-classical",
    "description":  f"Exact diagonalization N={N} TFIM, OBC and PBC. "
                    "Correlators and force profile for comparison with 5-layer 20q MERA VQE.",
    "date":         "2026-03-10",
    "systems": {
        "obc": {
            "n_sites": N, "J": J, "h": H_FIELD, "boundary": "open",
            "E0": E0_obc, "E0_per_site": E0_obc / N,
            "E1": E1_obc, "spectral_gap": gap_obc,
        },
        "pbc": {
            "n_sites": N, "J": J, "h": H_FIELD, "boundary": "periodic",
            "E0": E0_pbc, "E0_per_site": E0_pbc / N,
            "E1": E1_pbc, "spectral_gap": gap_pbc,
        },
    },
    "correlators": {
        "obc": {
            "separations":  seps_obc,
            "C_connected":  C_obc,
            "C_perturbed":  C_pert_obc,
            "V_force":      V_obc,
            "anchor_site":  ANCHOR,
            "hologron_angle_rad": float(ANGLE),
        },
        "pbc": {
            "separations":  seps_pbc,
            "C_connected":  C_pbc,
            "C_perturbed":  C_pert_pbc,
            "V_force":      V_pbc,
            "anchor_site":  ANCHOR,
            "hologron_angle_rad": float(ANGLE),
        },
    },
    "fits": fits,
    "l_AdS": float(L_ADS),
}

with open(OUT_JSON, 'w') as f:
    json.dump(structured, f, indent=2)
print(f"\nSaved: {OUT_JSON}", flush=True)
print("=" * 65, flush=True)
