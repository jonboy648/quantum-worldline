#!/usr/bin/env python3
"""
qw_stress_test.py -- the stress-tensor test HYP-2026-008 never had (SIM-2026-075).

Pre-registered in PREREGISTRATION-T.md (commit 82b7b4e, 2026-09-06) BEFORE this file existed.

Arms (both Z2-even, local, vev-subtracted, built from op_T and op_X):
  H : KW-even Hamiltonian density  O_H = op_T - op_X = -(ZZ - <ZZ>) - (X - <X>)  -> leading T+Tbar (Delta 2)
  E : KW-odd partner               O_E = op_T + op_X = -(ZZ - <ZZ>) + (X - <X>)  -> leading eps (Delta 1)

Gates (all CONTROLS; a failed run-level gate raises, a failed per-arm gate bars the arm):
  G1 ground state vs free fermions      G2 ring symmetry       G4 the arm's own two-point
  function scales as chord^-(2 Delta)   G5 Koo-Saleur structural zeros   G7 h=2 control clean.

Null (fixed in advance): the force IS the probe's two-point function, alpha_H = 4, alpha_E = 2.
Observing the null closes HYP-2026-008 at Level 1. Only a DEVIATION is a finding.

Usage: python qw_stress_test.py --n 16      (run each of 16, 20, 24; convergence is judged
       across the three result files by qw_stress_converge.py, never inside one run)
"""
import argparse, json, os, sys, time
import numpy as np
from scipy.sparse.linalg import eigsh, LinearOperator

from qw_channel_common import (
    SEED, GateFailure, _ax, op_T, op_X, vev_ZZ, vev_X,
    fit_log_ols, fit_relerr, local_slopes, plateau, bootstrap,
    enforce_run_gate, usable_arms,
)
from qw_ring_test import build_tfim_ring, exact_e0_ring, chord, fit_exp, r2_power

HERE = os.path.dirname(os.path.abspath(__file__))
WLO = 3
DELTA = {"H": 2.0, "E": 1.0}          # leading scaling dimension of each probe
G4_TOL = 0.3                          # |two-point exponent - 2 Delta| bar, pre-registered
G5_TOL = 1e-8                         # structural-zero bar, relative, pre-registered
PREREG = "PREREGISTRATION-T.md @ 82b7b4e"


def window_hi(n):
    return n // 2 - 1                 # antipode excluded: 7, 9, 11 at n = 16, 20, 24


SMEAR = 0.0                           # set by --smear: the ONE pre-registered retry (see below)


def make_arm(n, arm, gs, anchor):
    """Local probes. With SMEAR > 0 (the pre-registered retry after Arm H failed G4 at all three
    sizes): each probe is replaced by a Gaussian-weighted sum over neighbouring sites,
    O~(j) = sum_m w_m O(j+m), w_m ~ exp(-m^2 / 2 SMEAR^2), |m| <= 4, sum w = 1. This is the reading
    of PREREGISTRATION-T.md's retry clause ("project the excitation onto the low-momentum sector")
    that keeps the probe LOCAL so G4 remains a chord-distance scaling test: a fixed physical
    smearing width filters the lattice-scale (band-edge) modes that dominated the local probe,
    without restricting the operator to so few Fourier modes that a power-law fit is meaningless.
    The width is fixed here BEFORE any smeared result was seen (2026-09-07). KW parity is
    preserved term by term."""
    vzz, vx = vev_ZZ(n, anchor, gs), vev_X(n, anchor, gs)
    if arm == "H":
        base = lambda j, sv: op_T(n, j, sv, vzz) - op_X(n, j, sv, vx)
    elif arm == "E":
        base = lambda j, sv: op_T(n, j, sv, vzz) + op_X(n, j, sv, vx)
    else:
        raise ValueError("unknown arm %r; expected H or E" % (arm,))
    if SMEAR <= 0:
        return base
    ms = list(range(-4, 5))
    w = np.array([np.exp(-m * m / (2.0 * SMEAR * SMEAR)) for m in ms]); w /= w.sum()
    def smeared(j, sv):
        acc = None
        for m, wm in zip(ms, w):
            term = wm * base((j + m) % n, sv)
            acc = term if acc is None else acc + term
        return acc
    return smeared


def force_profile(n, gs, e0, H, ap, anchor, dr_values):
    cache = {}
    def single(j):
        if j not in cache:
            w = ap(j, gs); nr = np.linalg.norm(w)
            cache[j] = (float((w / nr) @ H.matvec(w / nr)) - e0) if nr > 1e-12 else np.nan
        return cache[j]
    F, dropped = {}, {}
    for dr in dr_values:
        j2 = (anchor + dr) % n
        w = ap(j2, ap(anchor, gs)); nr = np.linalg.norm(w)
        if nr < 1e-12:
            dropped[int(dr)] = {"reason": "dual-excitation norm below 1e-12", "norm": float(nr)}
            continue
        psi = w / nr
        F[dr] = (float(psi @ H.matvec(psi)) - e0) - (single(anchor) + single(j2))
    return F, dropped


def two_point(n, gs, ap, anchor, dr_values):
    """Connected <O(anchor) O(anchor+dr)> (both operators are vev-subtracted)."""
    w1 = ap(anchor, gs)
    return {int(dr): float(ap((anchor + dr) % n, gs) @ w1) for dr in dr_values}


# ------------------------------------------------------------------ G5: spectrum + structural zeros
def translate(n, v):
    """Site j -> j+1. Site j lives on axis _ax(n, j) = n-1-j, so shifting sites by +1 moves
    axis a to axis a-1 (mod n)."""
    A = v.reshape((2,) * n)
    return np.moveaxis(A, list(range(n)), [(a - 1) % n for a in range(n)]).reshape(-1)


def z2_flip(v):
    return v[::-1]                    # prod_j X_j: index i -> all bits flipped


def project_sector(n, v, s_abs, q):
    """Real projector onto the (s = +s_abs) + (s = -s_abs) translation subspace and Z2 charge q."""
    acc = np.zeros_like(v); w = v.copy()
    for m in range(n):
        acc += np.cos(2 * np.pi * s_abs * m / n) * w
        w = translate(n, w)
    acc *= (1.0 if s_abs % n == 0 or 2 * s_abs == n else 2.0) / n   # s and -s together: factor 2
    return 0.5 * (acc + q * z2_flip(acc))


def sector_lowest(H, n, s_abs, q, k):
    """Lowest k eigenpairs of H inside one (|s|, q) sector. The projector is applied INSIDE the
    matvec (P H P): Lanczos from a merely in-sector start leaks to the global ground state through
    roundoff (observed: leak = 1.0 at n = 16), so the sector must be enforced, not assumed.
    The result's sector leakage is still measured and reported."""
    rng = np.random.default_rng(SEED)
    P = lambda v: project_sector(n, v, s_abs, q)
    v0 = P(rng.standard_normal(1 << n)); v0 /= np.linalg.norm(v0)
    # P H P alone has a null space of dimension ~(1 - 1/n) 2^n at eigenvalue 0, which ARPACK
    # stalls on. Push the out-of-sector space up by SHIFT so "SA" sees only in-sector states.
    SHIFT = 10.0 * n
    HP = LinearOperator(H.shape, matvec=lambda v: P(H.matvec(P(v))) + SHIFT * (v - P(v)), dtype=np.float64)
    vals, vecs = eigsh(HP, k=k, which="SA", tol=1e-12, v0=v0)
    order = np.argsort(vals); vals, vecs = vals[order], vecs[:, order]
    out = []
    for i in range(k):
        v = vecs[:, i]; leak = np.linalg.norm(v - P(v))
        out.append({"E": float(vals[i]), "s_abs": s_abs, "q": q, "vec": v, "sector_leak": float(leak)})
    return out


def fourier_mode(n, ap, gs, kk):
    acc = np.zeros(1 << n, dtype=complex)
    for j in range(n):
        acc += np.exp(1j * 2 * np.pi * kk * j / n) * ap(j, gs)
    return acc


def g5_structural_zeros(n, gs, arms):
    """|eps> = lowest even s=0 state above the vacuum; |T>,|Tbar> = lowest even |s|=2 pair.
    Check the KW structural zeros:  <eps|O_H(0)|GS> == 0 relative to <T|O_H(+2)|GS>,
    and <T|O_E(+2)|GS> == 0 relative to <eps|O_E(0)|GS>.  Both partners of the |s|=2 pair are
    tried and the larger element taken, so a momentum sign convention cannot manufacture a zero."""
    H, _ = build_tfim_ring(n, 1.0)
    s0 = sector_lowest(H, n, 0, 1.0, 2)          # vacuum, eps
    s2 = sector_lowest(H, n, 2, 1.0, 2)          # T, Tbar (degenerate pair)
    E0 = s0[0]["E"]; eps = s0[1]; Tpair = s2[:2]
    leak = max(x["sector_leak"] for x in s0 + s2)
    OH0 = fourier_mode(n, arms["H"], gs, 0); OH2 = fourier_mode(n, arms["H"], gs, 2)
    OE0 = fourier_mode(n, arms["E"], gs, 0); OE2 = fourier_mode(n, arms["E"], gs, 2)
    e_H_zero = abs(np.vdot(eps["vec"], OH0)); e_H_ref = max(abs(np.vdot(x["vec"], OH2)) for x in Tpair)
    e_E_zero = max(abs(np.vdot(x["vec"], OE2)) for x in Tpair); e_E_ref = abs(np.vdot(eps["vec"], OE0))
    rH = e_H_zero / max(e_H_ref, 1e-300); rE = e_E_zero / max(e_E_ref, 1e-300)
    dT = Tpair[0]["E"] - E0; de = eps["E"] - E0
    ok_sectors = leak < 1e-8 and abs(Tpair[1]["E"] - Tpair[0]["E"]) < 1e-6
    return {
        "states": {"eps_E-E0": de, "T_E-E0": dT, "T_pair_split": Tpair[1]["E"] - Tpair[0]["E"],
                   "Delta_T_over_Delta_eps": dT / de, "max_sector_leak": leak},
        "H": {"zero_element_|<eps|O_H(0)|GS>|": e_H_zero, "ref_element_|<T|O_H(2)|GS>|": e_H_ref, "ratio": rH},
        "E": {"zero_element_|<T|O_E(2)|GS>|": e_E_zero, "ref_element_|<eps|O_E(0)|GS>|": e_E_ref, "ratio": rE},
        "pass": {"H": bool(ok_sectors and rH < G5_TOL and e_H_ref > 1e-6),
                 "E": bool(ok_sectors and rE < G5_TOL and e_E_ref > 1e-6)},
        "bar": G5_TOL,
    }


# ------------------------------------------------------------------------------------ one run
def run(n, h, label, do_g5):
    anchor = 0
    print(f"\n{'='*76}\n{label}  --  n={n}, h={h}, PBC ring\n{'='*76}")
    H, _ = build_tfim_ring(n, h)
    t = time.time()
    w, vec = eigsh(H, k=1, which="SA", tol=1e-12)
    gs = vec[:, 0] / np.linalg.norm(vec[:, 0]); e0 = float(w[0])
    e_exact = exact_e0_ring(n, h); g1 = abs(e0 / n - e_exact)
    print(f"  GS in {time.time()-t:.0f}s   |E0/n - exact| = {g1:.2e}  -> G1 {'PASS' if g1 < 1e-6 else 'FAIL'}")
    enforce_run_gate("G1 (PBC ground state vs exact free fermions)", g1 < 1e-6, f"{g1:.3e} > 1e-6")

    whi = window_hi(n)
    out = {"n": n, "h": h, "label": label, "E0": e0, "preregistration": PREREG,
           "G1": {"abs_diff": g1, "pass": True}, "window": [WLO, whi], "arms": {}}
    arms = {a: make_arm(n, a, gs, anchor) for a in ("H", "E")}
    dr_all = list(range(1, n - 1))
    for a, ap in arms.items():
        t = time.time()
        F, dropped = force_profile(n, gs, e0, H, ap, anchor, dr_all)
        C = two_point(n, gs, ap, anchor, dr_all)
        sym = {dr: abs(F[dr] - F[n - dr]) / max(abs(F[dr]), 1e-30) for dr in (3, 5, 7) if dr in F and (n - dr) in F}
        g2 = max(sym.values()) if sym else np.nan
        drs = np.array([d for d in sorted(F) if WLO <= d <= whi]); d_ch = chord(n, drs)
        y = np.array([F[d] for d in drs]); c = np.array([C[int(d)] for d in drs])
        a_ch, se = fit_log_ols(d_ch, y); bs = bootstrap(d_ch, y)
        mid, sl = local_slopes(d_ch, y); pl = plateau(sl)
        xi, r2e = fit_exp(drs, y); r2p = r2_power(d_ch, y)
        a2, _ = fit_log_ols(d_ch, c); _, sl2 = local_slopes(d_ch, c)
        g4_dev = abs(a2 - 2 * DELTA[a]); g4 = bool(np.isfinite(g4_dev) and g4_dev < G4_TOL) if h == 1.0 else None
        g2_pass = bool(np.isfinite(g2) and g2 < 0.01)
        out["arms"][a] = {
            "gates_passed": bool(g2_pass and (g4 in (True, None))),
            "gate_note": "", "dropped_separations": dropped, "n_dropped": len(dropped),
            "F_full": {int(k): float(v) for k, v in sorted(F.items())},
            "two_point_full": C,
            "G2_ring_symmetry_max_rel": g2, "G2_pass": g2_pass,
            "G4_two_point_exponent_chord": a2, "G4_two_point_slopes": [float(s) for s in sl2],
            "G4_expected_2Delta": 2 * DELTA[a], "G4_abs_dev": g4_dev, "G4_pass": g4,
            "alpha_chord": a_ch, "sigma_fit": se, "bootstrap_sigma": bs["std"],
            "bootstrap_sigma_interpretation": bs["sigma_interpretation"],
            "alpha_chord_relerr_crosscheck": fit_relerr(d_ch, y),
            "plateau_n": pl[0], "plateau_value": pl[1], "chord_slopes": [float(s) for s in sl],
            "amplitude_at_dr3": float(F.get(3, np.nan)),
            "power_r2": r2p, "exp_xi": float(xi), "exp_r2": r2e,
            "better_model": "power" if r2p >= r2e else "exponential",
        }
        print(f"  {a}  {time.time()-t:5.1f}s  force alpha_chord={a_ch:6.3f}+/-{bs['std']:.3f}  plateau {pl[0]}@{pl[1] if pl[0] else float('nan'):.3f}  "
              f"| two-point exp={a2:6.3f} (want {2*DELTA[a]:.0f}) G4 {g4}  G2 {'PASS' if g2_pass else 'FAIL'} ({g2:.1e})  "
              f"R2 pow={r2p:.4f} exp={r2e:.4f}")
    if do_g5 and h == 1.0:
        t = time.time()
        g5 = g5_structural_zeros(n, gs, arms)
        out["G5"] = g5
        for a in ("H", "E"):
            ok = g5["pass"][a]
            out["arms"][a]["G5_pass"] = ok
            out["arms"][a]["gates_passed"] = bool(out["arms"][a]["gates_passed"] and ok)
        print(f"  G5 in {time.time()-t:.0f}s: pass={g5['pass']}  H ratio={g5['H']['ratio']:.2e} (ref {g5['H']['ref_element_|<T|O_H(2)|GS>|']:.3e})  "
              f"E ratio={g5['E']['ratio']:.2e} (ref {g5['E']['ref_element_|<eps|O_E(0)|GS>|']:.3e})")
        print(f"     states: {g5['states']}")
    for a in ("H", "E"):
        r = out["arms"][a]
        r["gate_note"] = ("PASSED per-arm gates." if r["gates_passed"] else
                          "VOID ARM: failed a per-arm gate (see G2_pass / G4_pass / G5_pass). Barred from every verdict.")
    return out


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--n", type=int, default=16)
    ap.add_argument("--no-g5", action="store_true"); ap.add_argument("--smear", type=float, default=0.0)
    args = ap.parse_args(); n = args.n; t0 = time.time()
    global SMEAR; SMEAR = args.smear
    crit = run(n, 1.0, "EXPERIMENT 1 -- CRITICAL", do_g5=not args.no_g5)
    ctrl = run(n, 2.0, "MATCHED CONTROL (h=2)", do_g5=False)
    contaminated = [a for a in ("H", "E") if ctrl["arms"][a]["plateau_n"] >= 3
                    and np.isfinite(ctrl["arms"][a]["plateau_value"]) and 1.5 <= ctrl["arms"][a]["plateau_value"] <= 4.5]
    ctrl["verdict"] = "CONTROL_CONTAMINATED" if contaminated else "CONTROL_CLEAN"
    ctrl["contaminated_arms"] = contaminated
    ctrl["contamination_band"] = [1.5, 4.5]
    enforce_run_gate("G7 (matched h=2 control must be clean)", not contaminated,
                     "control shows a power-law plateau in " + str(contaminated))
    usable = usable_arms(crit["arms"])
    crit["usable_arms"] = sorted(usable)
    crit["verdict"] = None
    crit["verdict_note"] = ("Single-size run. No verdict is drawn here by design: convergence across "
                            "n = 16, 20, 24 is judged by qw_stress_converge.py per PREREGISTRATION-T.md.")
    print("\n" + "#" * 76)
    print(f"  CONTROL: {ctrl['verdict']}   usable arms at h=1: {sorted(usable)}")
    for a in ("H", "E"):
        r = crit["arms"][a]
        print(f"  {a}: force alpha_chord = {r['alpha_chord']:.3f} +/- {r['bootstrap_sigma']:.3f}   "
              f"two-point exponent = {r['G4_two_point_exponent_chord']:.3f} (null {2*DELTA[a]:.0f})   "
              f"{'OK' if r['gates_passed'] else 'VOID ARM'}")
    print("#" * 76)
    crit["smear_sigma_sites"] = SMEAR; crit["retry"] = bool(SMEAR > 0)
    dst = os.path.join(HERE, f"stress_test_n{n}{'_smear%g' % SMEAR if SMEAR > 0 else ''}_results.json")
    json.dump({"critical": crit, "control": ctrl}, open(dst, "w"), indent=2, default=float)
    print(f"wrote {dst}  ({time.time()-t0:.0f}s)")


if __name__ == "__main__":
    try:
        main()
    except GateFailure as e:
        print("\n!! RUN VOID -- " + str(e)); sys.exit(2)
