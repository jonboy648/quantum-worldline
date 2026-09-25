#!/usr/bin/env python3
"""
qw_tlee_candidates.py -- SIM-2026-077: the four pre-registered candidates of PREREGISTRATION-HYP032-A.md
(approved 2026-09-07, commit cff338a, before this file existed).

Question: is there any consistent lattice construction whose exact evaluation gives Im S = pi c/6?
  C1  chiral symmetry broken by a longitudinal field h_z (exact diagonalization, L = 10, 12, 14)
  C2  branch tracked continuously from real temperature (Gaussian, L = 512, 1024)
  C3  Dirac chain = two decoupled critical TFIM chains, c = 1 (Gaussian, L = 512, 1024)
  C4  periodic ring, full trace = weighted NS/R sector sum (Gaussian with ED gate at L = 10, 12; L = 256, 512)

YES for a candidate: |Im S| within 10% of pi c/6, one sign across T0 in [3, R/2], window std < 10% of
the mean, at BOTH sizes, for at least one registered setting. Anything else is NO. All NO = Level-3 negative.
Branch convention is stated for every number. Real-part slope is reported as a control only.

Usage: python qw_tlee_candidates.py --cand C1|C2|C3|C4 [--quick]
"""
import argparse, json, os, sys, time
import numpy as np
from numpy.linalg import eigh, eigvals, eig
import qw_tlee_level1 as q

HERE = os.path.dirname(os.path.abspath(__file__))
V = 2.0
BAR = 0.10


def verdict(c, ims):
    """Pre-registered YES/NO on a window of Im S values for central charge c."""
    ims = np.asarray(ims); pred = np.pi * c / 6
    m = ims.mean(); one_sign = bool(np.all(ims > 0) or np.all(ims < 0))
    within = abs(abs(m) - pred) < BAR * pred
    stable = (ims.std() < BAR * abs(m)) if abs(m) > 0 else False
    return {"Im_mean": float(m), "Im_std": float(ims.std()), "pred": float(pred), "one_sign": one_sign,
            "within_10pct": bool(within), "stable": bool(stable), "YES": bool(one_sign and within and stable)}


def windows(R):
    T0s = list(range(2, int(R) - 1)); win = [t for t in T0s if 3 <= t <= R / 2]
    return T0s, win


# --------------------------------------------------------------------------------------- C1
def tfim_dense_hz(L, hz):
    H = q.tfim_dense(L)
    if hz != 0.0:
        Z = np.array([[1.0, 0.0], [0.0, -1.0]]); I2 = np.eye(2)
        for j in range(L):
            m = np.array([[1.0]])
            for k in range(L):
                m = np.kron(m, Z if k == j else I2)
            H -= hz * m
    return H


_H_EIG = {}


def route_X_H(H, L, R_H, T0_list, delta):
    """Exact route for a given dense H. The eigendecomposition is cached per H object: the first
    pod run re-diagonalized the same 16384 x 16384 matrix six times per field value (45 min each)."""
    key = id(H)
    if key not in _H_EIG:
        _H_EIG.clear(); _H_EIG[key] = eigh(H)
    w, U = _H_EIG[key]
    E = (U * np.exp((1j * R_H - delta) * w)) @ U.conj().T
    tr = np.trace(E); out = {}
    for T0 in T0_list:
        s = (L - T0) // 2; dl, da, dr = 1 << s, 1 << T0, 1 << (L - s - T0)
        tau = np.einsum("iajibj->ab", E.reshape(dl, da, dr, dl, da, dr)) / tr
        lam = eigvals(tau); lam = lam[np.abs(lam) > 1e-14]
        out[int(T0)] = complex(np.sum(-lam * np.log(lam)))            # per-eigenvalue principal branch
    return out


def run_C1(quick):
    rec = {"candidate": "C1 longitudinal field (chiral symmetry broken)", "branch": "per-eigenvalue principal",
           "model": "H = -sum ZZ - sum X - h_z sum Z, open chain, exact diagonalization", "runs": {}, "gate_hz0": {}}
    Ls = (10, 12) if quick else (10, 12, 14)
    hzs = tuple(float(x) for x in os.environ.get("C1_HZ", "0.0,0.05,0.02,0.01,0.005").split(",")); deltas = (0.0, 2.0, 5.0)
    settings = {10: [3.0], 12: [4.0], 14: [4.0, 5.0]}       # R_H -> R = 6, 8, 8/10 (windows tiny; honest cost)
    yes_any = False
    Ls = tuple(int(x) for x in os.environ.get("C1_LS", ",".join(map(str, Ls))).split(","))
    partial = os.path.join(HERE, "sim077_C1_partial.json")
    for L in Ls:
        try:
            H0 = tfim_dense_hz(L, 0.0)
        except MemoryError:
            rec["runs"][f"L{L}"] = {"error": "MemoryError building H"}; break
        for hz in hzs:
            H = H0 if hz == 0.0 else tfim_dense_hz(L, hz)
            for R_H in settings[L]:
                R = V * R_H; T0s, win = windows(R)
                for delta in deltas:
                    t = time.time(); S = route_X_H(H, L, R_H, T0s, delta)
                    ims = [S[x].imag for x in win]; res = [S[x].real for x in win]
                    key = f"L{L}_hz{hz}_RH{R_H}_d{delta}"
                    v = verdict(0.5, ims) if len(win) >= 2 else {"Im_mean": float(np.mean(ims)), "YES": False, "note": "window < 2 points"}
                    rec["runs"][key] = {"L": L, "hz": hz, "R": R, "delta": delta, "window": win,
                                        "S": {x: [S[x].real, S[x].imag] for x in T0s}, "verdict": v, "secs": time.time() - t}
                    if hz == 0.0:
                        rec["gate_hz0"][key] = {"max_abs_Im": float(np.max(np.abs([S[x].imag for x in T0s]))), "pass": bool(np.max(np.abs([S[x].imag for x in T0s])) < 1e-9)}
                    yes_any = yes_any or v.get("YES", False)
                    print(f"C1 L={L} hz={hz:<6} R={R:4.0f} delta={delta:3.0f}: Im mean {v.get('Im_mean', float('nan')):+.4f} (pred 0.2618) {'YES' if v.get('YES') else 'no'}  [{time.time()-t:.0f}s]", flush=True)
                    json.dump(rec, open(partial, "w"), indent=1, default=float)     # after EVERY setting (run 3 lost L=14 to a cap)
    # size pairing: YES requires both sizes at the same (hz, delta); evaluated in the summary
    rec["YES_any_setting_single_size"] = yes_any
    return rec


# --------------------------------------------------------------------------------------- C2
_EIG_CACHE = {}


def gaussian_modes_path(L, R_H, delta, T0, beta0=3.0, steps=200, shift=0.0):
    """Track nu_j(s) and log p_j(s), log q_j(s) continuously along beta(s) = beta0(1-s) + s(delta - i R_H).
    The single-particle eigenbasis is computed once per L and cached; per step only the restricted
    2T0 x 2T0 correlator is formed (U_A diag(t) U_A^dag), which is what made this affordable."""
    if L not in _EIG_CACHE:
        A = q.majorana_A(L); _EIG_CACHE[L] = eigh(1j * A)
    w, U = _EIG_CACHE[L]
    s_idx = (L - T0) // 2; idx = np.arange(2 * s_idx, 2 * (s_idx + T0)); UA = U[idx, :]
    min_cosh = np.inf; prev_nu = None; logp = None; logq = None
    # beta0 = 3 (not 20 as first written): at beta0 = 20 the mode occupations are exactly 0/1 in
    # double precision, log(0/0) is NaN, and the tracked branch is undefined (run 3, 2026-09-08).
    # shift: the pre-registered path deformation (+0.5 i * s) applied when the path passes a zero of
    # Tr e^{-beta H} (min |cosh| < 1e-3); the caller reruns with shift = 0.5 and reports it.
    for k in range(steps + 1):
        s = k / steps; beta = beta0 * (1 - s) + s * (delta - 1j * R_H) + 1j * shift * s
        min_cosh = min(min_cosh, float(np.min(np.abs(np.cosh(beta * w[w > 0] / 2.0)))))
        t = np.tanh(beta * w / 2.0)
        GamA = -1j * ((UA * t[None, :]) @ UA.conj().T)
        nu = q.gaussian_nu(GamA)
        if prev_nu is not None:                       # match modes to the previous step (optimal assignment)
            from scipy.optimize import linear_sum_assignment
            D = np.abs(nu[:, None] - prev_nu[None, :])
            rows, cols = linear_sum_assignment(D)     # rows: new index, cols: previous index
            order = np.empty(len(nu), dtype=int); order[cols] = rows
            nu = nu[order]
        p = (1 + nu) / 2; qq = (1 - nu) / 2
        # Saturated modes (|p| or |q| below 1e-14: fully occupied/empty inside A) contribute nothing to S
        # and their ratio p/p_prev is 0/0. They are excluded from the tracking step (their log is
        # reset to the principal value, which is what a zero contribution needs). Found in run 3 as NaN
        # at large T0 with delta > 0.
        if logp is None:
            logp = np.log(p.astype(complex)); logq = np.log(qq.astype(complex))    # s = 0: real thermal state
            p_prev, q_prev = p, qq
        else:
            okp = (np.abs(p) > 1e-14) & (np.abs(p_prev) > 1e-14); okq = (np.abs(qq) > 1e-14) & (np.abs(q_prev) > 1e-14)
            logp = np.where(okp, logp + np.log(np.where(okp, p / np.where(okp, p_prev, 1), 1).astype(complex)), np.log(np.where(np.abs(p) > 1e-300, p, 1e-300).astype(complex)))
            logq = np.where(okq, logq + np.log(np.where(okq, qq / np.where(okq, q_prev, 1), 1).astype(complex)), np.log(np.where(np.abs(qq) > 1e-300, qq, 1e-300).astype(complex)))
            p_prev, q_prev = p, qq
        prev_nu = nu
    S_tracked = complex(np.sum(-p * logp - qq * logq))
    S_principal = complex(np.sum(-p * np.log(p.astype(complex)) - qq * np.log(qq.astype(complex))))
    return S_tracked, S_principal, min_cosh


def run_C2(quick):
    rec = {"candidate": "C2 branch tracked continuously from real temperature beta0 = 20", "branch": "tracked (continuous along the path); per-mode principal also reported",
           "runs": {}}
    Ls = (256,) if quick else (512, 1024)
    for L in Ls:
        for R_H in (25.0, 50.0):
            R = V * R_H; T0s, win = windows(R)
            for delta in (0.0, 2.0, 5.0):
                t = time.time(); St, Sp, mc = {}, {}, np.inf; shift = 0.0
                for T0 in win:
                    a, b, c = gaussian_modes_path(L, R_H, delta, T0); St[T0] = a; Sp[T0] = b; mc = min(mc, c)
                gate = mc > 1e-3
                if not gate:                       # pre-registered deformation, applied once and reported
                    shift = 0.5; St, Sp, mc2 = {}, {}, np.inf
                    for T0 in win:
                        a, b, c = gaussian_modes_path(L, R_H, delta, T0, shift=shift); St[T0] = a; Sp[T0] = b; mc2 = min(mc2, c)
                    gate = mc2 > 1e-3
                v = verdict(0.5, [St[x].imag for x in win]); vp = verdict(0.5, [Sp[x].imag for x in win])
                key = f"L{L}_RH{R_H}_d{delta}"
                rec["runs"][key] = {"L": L, "R": R, "delta": delta, "window": win, "min_abs_cosh_on_path": mc, "path_gate_pass": gate, "path_shift_applied": shift, "beta0": 3.0,
                                    "S_tracked": {x: [St[x].real, St[x].imag] for x in win}, "S_principal": {x: [Sp[x].real, Sp[x].imag] for x in win},
                                    "verdict_tracked": v, "verdict_principal": vp}
                json.dump(rec, open(os.path.join(HERE, "sim077_C2_partial.json"), "w"), indent=1, default=float)
                print(f"C2 L={L} R={R:4.0f} delta={delta:3.0f}: tracked Im {v['Im_mean']:+.4f}+/-{v['Im_std']:.4f} {'YES' if v['YES'] else 'no'} | principal Im {vp['Im_mean']:+.4f} | path gate {'PASS' if gate else 'FAIL'} (min|cosh| {mc:.1e})  [{time.time()-t:.0f}s]", flush=True)
    return rec


# --------------------------------------------------------------------------------------- C3
def run_C3(quick):
    rec = {"candidate": "C3 Dirac c = 1: two decoupled critical TFIM chains", "branch": "per-mode principal", "runs": {}, "identity_gate": {}}
    Ls = (256,) if quick else (512, 1024)
    for L in Ls:
        A1 = q.majorana_A(L); n = A1.shape[0]
        A2 = np.zeros((2 * n, 2 * n)); A2[:n, :n] = A1; A2[n:, n:] = A1        # block-diagonal: two chains
        for R_H in (25.0, 50.0):
            R = V * R_H; T0s, win = windows(R)
            for delta in (2.0, 5.0, 10.0):
                t = time.time()
                G1 = q.gamma_imag_temp(A1, R_H, delta); G2 = q.gamma_imag_temp(A2, R_H, delta)
                S1, S2 = {}, {}
                for T0 in win:
                    s = (L - T0) // 2; idx = np.arange(2 * s, 2 * (s + T0))
                    idx2 = np.concatenate([idx, idx + n])                      # same interval on both chains
                    S1[T0] = q.gaussian_S(G1[np.ix_(idx, idx)]); S2[T0] = q.gaussian_S(G2[np.ix_(idx2, idx2)])
                ident = max(abs(S2[x] - 2 * S1[x]) for x in win)
                v = verdict(1.0, [S2[x].imag for x in win])
                key = f"L{L}_RH{R_H}_d{delta}"
                rec["runs"][key] = {"L": L, "R": R, "delta": delta, "window": win, "S_dirac": {x: [S2[x].real, S2[x].imag] for x in win},
                                    "identity_2x_gate_maxdiff": ident, "identity_pass": bool(ident < 1e-10), "verdict": v}
                print(f"C3 L={L} R={R:4.0f} delta={delta:3.0f}: Im {v['Im_mean']:+.4f}+/-{v['Im_std']:.4f} (pred 0.5236) {'YES' if v['YES'] else 'no'} | 2x identity {ident:.1e}  [{time.time()-t:.0f}s]", flush=True)
    return rec


# --------------------------------------------------------------------------------------- C4
def tfim_dense_ring(L):
    Z = np.array([[1.0, 0.0], [0.0, -1.0]]); X = np.array([[0.0, 1.0], [1.0, 0.0]]); I2 = np.eye(2)
    def site(op, j):
        m = np.array([[1.0]])
        for k in range(L):
            m = np.kron(m, op if k == j else I2)
        return m
    H = np.zeros((1 << L, 1 << L))
    for j in range(L):
        H -= site(X, j); H -= site(Z, j) @ site(Z, (j + 1) % L)
    return H


def majorana_A_ring(L, antiperiodic):
    """Ring: the JW closing bond Z_{L-1} Z_0 becomes -i g_{2L-1} g_0 times (-1) in the NS (antiperiodic) sector."""
    A = q.majorana_A(L)
    sgn = -1.0 if antiperiodic else 1.0
    a, b, w = 2 * L - 1, 0, sgn * 1.0
    A[a, b] += 2 * w; A[b, a] -= 2 * w
    return A


def run_C4(quick):
    """C4 by EXACT ring diagonalization only (L = 10, 12, 14).

    Why not the registered Gaussian sector sum at L = 256/512: at h = 1 the Ramond (periodic) fermion
    sector has an exact zero mode, so the parity-inserted Gaussian Tr[P e^{-beta H_R}] has zero total
    trace while its partial trace does not vanish; the correlation-matrix construction (tanh -> coth)
    is singular there and a first implementation failed its ED gate by 0.1-0.2 (2026-09-07, local
    L = 10 gate, sim077_C4_quick.json). Rather than debug a construction the gate had already voided,
    C4 is evaluated by the definition itself: the full spin-chain trace on the ring, exactly. Sizes are
    smaller than registered; that is reported as the cost, not hidden."""
    rec = {"candidate": "C4 periodic ring, full trace, EXACT diagonalization", "branch": "per-eigenvalue principal",
           "registered_construction_status": "Gaussian NS/R sector sum VOID (failed ED gate; zero-mode singularity at h=1); ED fallback used",
           "runs": {}}
    Ls = (10, 12) if quick else (10, 12, 14)
    settings = {10: [3.0], 12: [4.0], 14: [4.0, 5.0]}
    for L in Ls:
        H = tfim_dense_ring(L); w, U = eigh(H)
        for R_H in settings[L]:
            R = V * R_H; T0s, win = windows(R)
            for delta in (0.0, 2.0, 5.0):
                t = time.time()
                E = (U * np.exp((1j * R_H - delta) * w)) @ U.conj().T; tr = np.trace(E); S = {}
                for T0 in T0s:
                    s = (L - T0) // 2; dl, da, dr = 1 << s, 1 << T0, 1 << (L - s - T0)
                    tau = np.einsum("iajibj->ab", E.reshape(dl, da, dr, dl, da, dr)) / tr
                    lam = eigvals(tau); lam = lam[np.abs(lam) > 1e-14]
                    S[T0] = complex(np.sum(-lam * np.log(lam)))
                ims = [S[x].imag for x in win]
                v = verdict(0.5, ims) if len(win) >= 2 else {"Im_mean": float(np.mean(ims)), "YES": False, "note": "window < 2 points"}
                key = f"L{L}_RH{R_H}_d{delta}"
                rec["runs"][key] = {"L": L, "R": R, "delta": delta, "window": win, "S": {x: [S[x].real, S[x].imag] for x in T0s}, "verdict": v, "secs": time.time() - t}
                print(f"C4 ring ED L={L} R={R:4.0f} delta={delta:3.0f}: Im mean {v.get('Im_mean', float('nan')):+.4f} (pred 0.2618) {'YES' if v.get('YES') else 'no'}  [{time.time()-t:.0f}s]", flush=True)
    return rec


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--cand", required=True); ap.add_argument("--quick", action="store_true")
    a = ap.parse_args(); t0 = time.time()
    rec = {"C1": run_C1, "C2": run_C2, "C3": run_C3, "C4": run_C4}[a.cand](a.quick)
    rec["preregistration"] = "PREREGISTRATION-HYP032-A.md @ cff338a"; rec["quick"] = a.quick; rec["secs"] = time.time() - t0
    dst = os.path.join(HERE, f"sim077_{a.cand}{'_quick' if a.quick else ''}.json")
    json.dump(rec, open(dst, "w"), indent=1, default=float); print("wrote", dst)


if __name__ == "__main__":
    main()
