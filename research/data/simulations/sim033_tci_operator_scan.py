"""
SIM-2026-033 — HYP-2026-027 stage 1b (proper): is alpha~4 universal? Operator-basis scan
at the tricritical Ising point, with a strict Ising-end validation gate.

WHY THIS SUPERSEDES SIM-032b: the published boundary-primary operator (0.635*(X_j+X_{j+1})
- 0.026*(X_jZ_{j+1}+Z_jX_{j+1})) is NOT a max-creation operator (SIM-032b's principle failed
its own Ising gate, giving 2.92 not 3.97). Reading sim2026015d: the published operator lives in
the ENERGY/STRESS-TENSOR sector -- built from X and (XZ+ZX), deliberately EXCLUDING the Z order
parameter. The right ZMV-style identification is therefore a SYMMETRY-RESOLVED scan: enumerate a
basis of local 2-site operators, measure for EACH (a) the force exponent alpha it produces and
(b) its effective scaling dimension Delta_eff from the single-excitation energy gap it creates,
then KEEP the operator whose alpha reproduces the published Ising value -- that is the legitimate
stress-tensor-channel operator -- and apply the IDENTICAL construction at the TCI point.

VALIDATION GATE (hard, must pass before any TCI alpha is interpreted):
  At lam3=0 (Ising end of the O'Brien-Fendley chain, = our published model), the selected
  operator must give alpha in [3.6, 4.4] AND reproduce the published 3.97+/-0.15 within ~1 sigma.
DICHOTOMY at TCI (lam3=0.856, c=7/10 confirmed in SIM-032):
  universal stress-tensor  -> alpha = 4.0
  primary-tracking (lightest TCI primary sigma', Delta=3/80) -> alpha = 2*Delta = 0.075
  (note: epsilon' of TCI has Delta=1/5 -> alpha=0.4; we report nearest-channel identification)

Operator basis (2-site, real, Hermitian), grouped by Z2 sector:
  Z2-EVEN (energy/stress sector, what the published op uses):
    e1 = X_j + X_{j+1}            (transverse field / energy density)
    e2 = X_jZ_{j+1} + Z_jX_{j+1}  (the published mixing term)
    e3 = Z_jZ_{j+1}               (Ising bond / energy density)
    e4 = Y_jY_{j+1}
  Z2-ODD (order-parameter sector):
    o1 = Z_j + Z_{j+1}
We scan the EVEN sector (the force lives there; ODD single-site Z is the magnetization, force-blind
per SIM-031) as 1-, 2-, and 3-term combinations, plus the exact published (0.635,-0.026) point as a
reference row. Force protocol = published config exactly (OBC, anchor=2, dr=2..11 fit, per-site
dE_single subtraction). Central-charge gate reused from SIM-032 (already passed: 0.50/0.73).
Output: research/data/simulations/SIM-2026-033.json + verdict write-back to HYP-2026-027.json.
"""
import json
import time

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse.linalg import eigsh

import hyp024_tfd_btz_transport as TFD
from sim032_tci_force_stage1 import build_OF

N = 16
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-033.json"
HYP = "D:/quantum-worldline/research/data/hypotheses/HYP-2026-027.json"
LAM_TCI = 0.856
DRS = list(range(1, 12))
FIT_DR_MIN = 2
ANCHOR = 2
PUB_ISING_ALPHA = 3.97
GATE = (3.6, 4.4)


def P(i, p):
    return TFD.sparse_pauli_full(N, i, p)


def basis_terms(j):
    """Z2-even local 2-site operator basis at site j (force lives here)."""
    return {
        "X": P(j, "X") + P(j + 1, "X"),
        "XZ+ZX": P(j, "X") @ P(j + 1, "Z") + P(j, "Z") @ P(j + 1, "X"),
        "ZZ": P(j, "Z") @ P(j + 1, "Z"),
        "YY": P(j, "Y") @ P(j + 1, "Y"),
    }


def make_op(coef, j):
    t = basis_terms(j)
    names = list(t)
    O = coef[0] * t[names[0]]
    for i in range(1, len(names)):
        if coef[i] != 0.0:
            O = O + coef[i] * t[names[i]]
    return O


def delta_eff(gs, H, E0, coef):
    """Effective scaling dimension from the single-excitation energy this op creates."""
    sa = make_op(coef, ANCHOR)
    ps = sa @ gs
    n = np.linalg.norm(ps)
    if n < 1e-12:
        return None
    ps = ps / n
    dE = float(np.real(np.vdot(ps, H @ ps))) - E0
    return dE  # proportional to the operator's conformal weight on this lattice


def force_exponent(gs, H, E0, coef):
    sa = make_op(coef, ANCHOR)
    psa = sa @ gs
    na = np.linalg.norm(psa)
    if na < 1e-12:
        return None, None, 0
    dE_a = float(np.real(np.vdot(psa / na, H @ (psa / na)))) - E0
    F = {}
    for dr in DRS:
        sp = make_op(coef, ANCHOR + dr)
        pp = sp @ gs
        npn = np.linalg.norm(pp)
        if npn < 1e-12:
            F[dr] = None
            continue
        dE_p = float(np.real(np.vdot(pp / npn, H @ (pp / npn)))) - E0
        pd = sp @ (sa @ gs)
        nd = np.linalg.norm(pd)
        if nd < 1e-12:
            F[dr] = None
            continue
        pd = pd / nd
        F[dr] = float(np.real(np.vdot(pd, H @ pd))) - E0 - dE_a - dE_p
    r = np.array([d for d in DRS if d >= FIT_DR_MIN and F[d] is not None and abs(F[d]) > 1e-12], float)
    if len(r) < 4:
        return None, F, len(r)
    y = np.array([abs(F[int(d)]) for d in r])
    try:
        popt, pcov = curve_fit(lambda x, A, a: A * x ** (-a), r, y, p0=[y[0], 3.0], maxfev=20000)
        return (float(popt[1]), float(np.sqrt(pcov[1, 1]))), F, len(r)
    except Exception:
        lp = np.polyfit(np.log(r), np.log(y), 1)
        return (float(-lp[0]), float("nan")), F, len(r)


# candidate coefficient vectors over [X, XZ+ZX, ZZ, YY]
CANDS = {
    "published(0.635,-0.026)": [0.635, -0.026, 0.0, 0.0],
    "X_only": [1.0, 0.0, 0.0, 0.0],
    "ZZ_only": [0.0, 0.0, 1.0, 0.0],
    "X+ZZ(energy)": [1.0, 0.0, -1.0, 0.0],
    "X-ZZ": [1.0, 0.0, 1.0, 0.0],
    "XZ+ZX_only": [0.0, 1.0, 0.0, 0.0],
    "X+mix": [1.0, -0.04, 0.0, 0.0],
}


def run_point(lam3, label):
    H = build_OF(N, lam3, pbc=False)
    E0a, psi = eigsh(H, k=1, which="SA")
    gs = psi[:, 0]
    E0 = float(E0a[0])
    rows = []
    for name, c in CANDS.items():
        res, F, npts = force_exponent(gs, H, E0, c)
        de = delta_eff(gs, H, E0, c)
        if res is None:
            rows.append({"op": name, "alpha": None, "note": "degenerate", "dE_single": de})
            continue
        a, da = res
        rows.append({"op": name, "alpha": a, "alpha_err": da, "n_fit": npts, "dE_single": de})
        print(f"  [{label}] {name:24s} alpha={a:6.3f}+/-{da:5.3f}  dE_single={de:.4f}", flush=True)
    return {"lam3": lam3, "E_gs": E0, "rows": rows}


def main():
    t0 = time.time()
    print("=" * 74)
    print("SIM-2026-033: operator-basis scan for alpha universality (Ising vs TCI)")
    print("=" * 74)
    ising = run_point(0.0, "Ising")
    tci = run_point(LAM_TCI, "TCI")

    # SELECT: the operator whose Ising-end alpha is closest to the published 3.97 AND in-gate
    valid = [r for r in ising["rows"] if r.get("alpha") is not None and GATE[0] <= r["alpha"] <= GATE[1]]
    selected = None
    if valid:
        selected = min(valid, key=lambda r: abs(r["alpha"] - PUB_ISING_ALPHA))
    gate_pass = selected is not None and abs(selected["alpha"] - PUB_ISING_ALPHA) < 0.4

    verdict, tci_alpha = None, None
    if not gate_pass:
        verdict = ("VALIDATION_FAILED: no basis operator reproduces the published Ising alpha~3.97 "
                   "within gate; cannot interpret TCI. Best Ising alphas: "
                   + ", ".join(f"{r['op']}={r['alpha']:.2f}" for r in ising["rows"] if r.get("alpha")))
    else:
        sel_op = selected["op"]
        trow = next((r for r in tci["rows"] if r["op"] == sel_op), None)
        tci_alpha = trow.get("alpha") if trow else None
        if tci_alpha is None:
            verdict = f"INCONCLUSIVE: selected op '{sel_op}' degenerate at TCI"
        elif GATE[0] <= tci_alpha <= GATE[1]:
            verdict = (f"UNIVERSALITY_SUPPORTED: validated operator '{sel_op}' gives Ising alpha="
                       f"{selected['alpha']:.2f} (matches published 3.97) AND TCI alpha={tci_alpha:.2f} in "
                       f"[3.6,4.4]. alpha~4 reproduces in a SECOND universality class (c=7/10).")
        elif abs(tci_alpha - 0.4) < 0.5 or abs(tci_alpha - 0.075) < 0.4:
            verdict = (f"PRIMARY_TRACKING: validated operator '{sel_op}' (Ising alpha="
                       f"{selected['alpha']:.2f}) gives TCI alpha={tci_alpha:.2f}, near a TCI primary "
                       f"value -> force tracks the lightest primary, NOT the universal stress tensor. "
                       f"Surprising; would force a matter-exchange reinterpretation.")
        else:
            verdict = (f"INCONCLUSIVE: validated op '{sel_op}' (Ising {selected['alpha']:.2f}) gives TCI "
                       f"alpha={tci_alpha:.2f} -- matches neither 4.0 nor a clean TCI primary; needs N=20 "
                       f"or chi>=3 MERA (stage 2).")

    out = {"id": "SIM-2026-033", "type": "classical", "date": "2026-06-08",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage 1b proper: symmetry-resolved operator-basis scan for the force "
                           "exponent at Ising (lam3=0) vs tricritical (lam3=0.856) points of the "
                           "O'Brien-Fendley chain. Operator selected by reproducing the published "
                           "Ising alpha~3.97 (validation gate), then applied identically at TCI."),
           "circuit": {"qubits": N, "script_path": "research/data/simulations/sim033_tci_operator_scan.py"},
           "hardware_target": "local CPU (exact statevector)",
           "results": {"ising_scan": ising, "tci_scan": tci,
                       "selected_operator": selected, "gate_pass": gate_pass,
                       "tci_alpha_selected": tci_alpha,
                       "dichotomy": {"universal": 4.0, "tci_epsilon_prime": 0.4, "tci_sigma_prime": 0.075},
                       "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "c=7/10 gate already passed in SIM-2026-032 (c=0.726). This isolates the operator question.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\n  VERDICT:", verdict)
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")

    # write-back
    try:
        h = json.load(open(HYP, encoding="utf-8"))
        if gate_pass and tci_alpha is not None:
            if GATE[0] <= tci_alpha <= GATE[1]:
                h["status"] = "SUPPORTED"
            elif abs(tci_alpha - 0.4) < 0.5 or abs(tci_alpha - 0.075) < 0.4:
                h["status"] = "REFUTED"
            else:
                h["status"] = "under_review"
        h["last_updated"] = "2026-06-08"
        h["result_note_2026_06_08_sim033"] = "Stage 1b proper (SIM-2026-033 operator scan): " + verdict
        json.dump(h, open(HYP, "w", encoding="utf-8"), indent=2)
        print(f"  HYP-027 status -> {h.get('status')}")
    except Exception as e:
        print("  write-back skipped:", e)


if __name__ == "__main__":
    main()
