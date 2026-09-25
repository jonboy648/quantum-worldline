"""
SIM-2026-032b (stage 1b) — HYP-2026-027: TCI force with a PROPERLY CALIBRATED excitation operator.

Stage 1 (SIM-032) result: gates passed, Ising control reproduced published alpha=3.975+/-0.145,
but the TCI point gave alpha=1.33 with the ISING-tuned bp_op (0.635/-0.026) — an uncalibrated
primary mixture at the new fixed point. Fix: re-derive the operator AT EACH POINT by the same
operational principle the Ising bp_op embodies: the local operator (span of a small 2-site basis)
that MAXIMALLY CREATES the lowest excitation from the GS.

CALIBRATION: for target eigenstate |k> and basis {O_m}, maximize
    |<k| O(c) |GS>|^2 / <GS| O(c)^dag O(c) |GS>,  O(c) = sum_m c_m O_m
=> generalized eigenproblem  (v v^dag) c = mu * G c,  v_m = <k|O_m|GS>, G_mn = <GS|O_m^dag O_n|GS>.
Leading eigenvector c* = calibrated operator. METHOD VALIDATION: applying the identical procedure
at the Ising end must reproduce alpha~3.97 (else the calibration principle itself is suspect and
the TCI number remains uninterpretable).

Basis (2-site, mid-chain site j): Z_j | Z_j Z_{j+1} | X_j | (X_j Z_{j+1} + Z_j X_{j+1}) |
Y_j Y_{j+1} | X_j X_{j+1}. Force protocol identical to SIM-032 final config (OBC, anchor=2,
dr=1..11, per-site dE_single subtraction, fit dr>=2). Targets: try k=1..4, use the k giving the
largest creation amplitude (symmetry sectors select themselves through the overlap).
Output: research/data/simulations/SIM-2026-032b.json + note in HYP-2026-027.json.
"""
import json
import time

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse.linalg import eigsh

import hyp024_tfd_btz_transport as TFD
from sim032_tci_force_stage1 import build_OF

N = 16
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-032b.json"
HYP = "D:/quantum-worldline/research/data/hypotheses/HYP-2026-027.json"
LAM_TCI = 0.856
DRS = list(range(1, 12))
FIT_DR_MIN = 2
WINDOW = (3.2, 4.8)
ANCHOR = 2


def basis_ops(j):
    P = lambda i, p: TFD.sparse_pauli_full(N, i, p)
    return {
        "Z": P(j, "Z"),
        "ZZ": P(j, "Z") @ P(j + 1, "Z"),
        "X": P(j, "X"),
        "XZ+ZX": P(j, "X") @ P(j + 1, "Z") + P(j, "Z") @ P(j + 1, "X"),
        "YY": P(j, "Y") @ P(j + 1, "Y"),
        "XX": P(j, "X") @ P(j + 1, "X"),
    }


def calibrate(gs, excs, j):
    """Best (target k, coefficients) maximizing normalized creation amplitude."""
    ops = basis_ops(j)
    names = list(ops)
    Ogs = {m: ops[m] @ gs for m in names}
    G = np.array([[np.vdot(Ogs[a], Ogs[b]) for b in names] for a in names])
    best = None
    for k in range(excs.shape[1]):
        v = np.array([np.vdot(excs[:, k], Ogs[m]) for m in names])
        # generalized Rayleigh: maximize |v.c|^2 / c^dag G c
        Ginv_v = np.linalg.solve(G + 1e-12 * np.eye(len(names)), v.conj())
        mu = float(np.real(np.vdot(v.conj(), Ginv_v)))  # max creation prob
        c = Ginv_v / np.linalg.norm(Ginv_v)
        if best is None or mu > best["mu"]:
            best = {"k": k, "mu": mu, "coef": c, "names": names}
    # build the calibrated operator (site-independent coefficient pattern)
    return best


def make_op(coef, names, j):
    ops = basis_ops(j)
    O = coef[0] * ops[names[0]]
    for m in range(1, len(names)):
        O = O + coef[m] * ops[names[m]]
    return O


def force(gs, H, coef, names):
    E0 = float(np.real(np.vdot(gs, H @ gs)))
    sa = make_op(coef, names, ANCHOR)
    ps = sa @ gs
    ps = ps / np.linalg.norm(ps)
    dE_a = float(np.real(np.vdot(ps, H @ ps))) - E0
    F = {}
    for dr in DRS:
        sp = make_op(coef, names, ANCHOR + dr)
        pp = sp @ gs
        pp = pp / np.linalg.norm(pp)
        dE_p = float(np.real(np.vdot(pp, H @ pp))) - E0
        pd = sp @ (sa @ gs)
        nrm = np.linalg.norm(pd)
        if nrm < 1e-12:
            F[dr] = None
            continue
        pd = pd / nrm
        F[dr] = float(np.real(np.vdot(pd, H @ pd))) - E0 - dE_a - dE_p
    return F


def fit_alpha(F):
    r = np.array([d for d in DRS if d >= FIT_DR_MIN and F[d] is not None and abs(F[d]) > 1e-12], float)
    if len(r) < 4:
        return float("nan"), float("nan"), 0
    y = np.array([abs(F[int(d)]) for d in r])
    try:
        popt, pcov = curve_fit(lambda x, A, a: A * x ** (-a), r, y, p0=[y[0], 3.0], maxfev=20000)
        return float(popt[1]), float(np.sqrt(pcov[1, 1])), len(r)
    except Exception:
        lp = np.polyfit(np.log(r), np.log(y), 1)
        return float(-lp[0]), float("nan"), len(r)


def run_point(lam3, label):
    H = build_OF(N, lam3, pbc=False)
    vals, vecs = eigsh(H, k=6, which="SA")
    order = np.argsort(vals)
    gs = vecs[:, order[0]]
    excs = vecs[:, order[1:]]
    cal = calibrate(gs, excs, j=N // 2 - 1)
    coef = cal["coef"]
    F = force(gs, H, coef, cal["names"])
    a, da, npts = fit_alpha(F)
    rec = {"lam3": lam3, "target_exc": int(cal["k"]) + 1, "creation_prob": cal["mu"],
           "coef": {n: [float(np.real(c)), float(np.imag(c))] for n, c in zip(cal["names"], coef)},
           "F": {str(d): F[d] for d in DRS}, "alpha": a, "alpha_err": da, "n_fit_pts": npts}
    print(f"  [{label}] target=exc{rec['target_exc']} P_create={cal['mu']:.3f} "
          f"alpha={a:.3f}+/-{da:.3f} ({npts} pts)", flush=True)
    return rec


def main():
    t0 = time.time()
    print("=" * 72)
    print("SIM-2026-032b: TCI force with point-calibrated excitation operator")
    print("=" * 72)
    ising = run_point(0.0, "Ising control (method validation)")
    tci = run_point(LAM_TCI, "TCI point")

    method_ok = WINDOW[0] <= ising["alpha"] <= WINDOW[1]
    in_window = WINDOW[0] <= tci["alpha"] <= WINDOW[1]
    near_primary = abs(tci["alpha"] - 0.4) < 0.5
    if not method_ok:
        verdict = (f"METHOD_NOT_VALIDATED: calibrated-Ising alpha={ising['alpha']:.2f} outside "
                   f"{WINDOW} — the calibration principle does not reproduce the published pipeline; "
                   f"TCI number not interpretable this way")
    elif in_window:
        verdict = (f"UNIVERSALITY_SUPPORTED: calibrated TCI alpha={tci['alpha']:.2f} in {WINDOW} "
                   f"with method validated at the Ising end — second universality class")
    elif near_primary:
        verdict = (f"PRIMARY_TRACKING: calibrated TCI alpha={tci['alpha']:.2f} near 0.4 — force "
                   f"tracks the lightest primary, refutation signal for universality")
    else:
        verdict = (f"STILL_INCONCLUSIVE: calibrated TCI alpha={tci['alpha']:.2f} — needs N=20 "
                   f"and/or MERA stage 2 and/or multi-operator channel decomposition")

    out = {"id": "SIM-2026-032b", "type": "classical", "date": "2026-06-08",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage 1b: point-calibrated excitation operators (max-creation-amplitude "
                           "generalized eigenproblem over a 6-element 2-site basis) for the alpha "
                           "dichotomy at Ising vs TCI points of the O'Brien-Fendley chain."),
           "circuit": {"qubits": N, "script_path": "research/data/simulations/sim032b_tci_operator_calibration.py"},
           "hardware_target": "local CPU (exact statevector)",
           "results": {"ising_control": ising, "tci_point": tci, "verdict": verdict,
                       "dichotomy": {"universal": 4.0, "primary_tracking": 0.4}},
           "comparison": "classical_wins",
           "notes": "Protocol: OBC, anchor=2, dr=2..11 fit, per-site dE_single subtraction (SIM-032 final config).",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  VERDICT: {verdict}")
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
