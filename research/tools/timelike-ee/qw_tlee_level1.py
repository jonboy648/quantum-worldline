#!/usr/bin/env python3
"""
qw_tlee_level1.py -- HYP-2026-032 Level-1 gate: timelike entanglement entropy on the critical TFIM.

Pre-registered: PREREGISTRATION-HYP032.md (approved 2026-09-07, committed before this file).
Construction: ROUTE-X-DERIVATION.md.  Object:  tau_A = Tr_B[e^{i R_H H}] / Tr[e^{i R_H H}],
S = -Tr[tau_A log tau_A] (principal branch), open chain of length L, interval of T0 sites centred.
Prediction (c = 1/2, v = 2, R = 2 R_H):  Re S = (1/6) log((R/pi) sin(pi T0/R)) + const,  Im S = pi/12.

Routes:
  X  exact: full diagonalization at L = 10, 12, (14)      -> the definition, literally
  G  Gaussian (free Majorana, imaginary temperature)       -> exact for quadratic H; L up to 512

Gates (controls):  EXACT  |S_G - S_X| < 1e-10 at every (R_H, T0) in the overlap, else Route G VOID
                   END    doubling L changes S by < 1e-3 over the window, else window shrinks (recorded)
                   SYM    S(T0) = S(R - T0) to 1e-3 (free control)
                   L1     slope within 3% of 1/6 AND |Im S| within 3% of pi/12 with one sign, at every
                          R_H and L in the pass set, else VOID.
Usage:  python qw_tlee_level1.py [--quick]
"""
import argparse, json, os, sys, time
import numpy as np
from numpy.linalg import eigh, eigvals

HERE = os.path.dirname(os.path.abspath(__file__))
C_THIRD = 1.0 / 6.0            # c/3 for c = 1/2
IM_PRED = np.pi / 12.0         # pi c / 6
V = 2.0                        # lattice velocity of the critical TFIM
R_H_LIST = (6.0, 8.0, 12.0)
L_GAUSS = (256, 512)
L_EXACT = (10, 12)


# ------------------------------------------------------------------------------ Route G
def majorana_A(L):
    """H = -sum ZZ - sum X = (i/4) gamma^T A gamma with real antisymmetric A (2L x 2L), open chain.
    JW: X_j = i g_{2j} g_{2j+1};  Z_j Z_{j+1} = -i g_{2j+1} g_{2j+2}  (Kitaev chain at the critical point)."""
    A = np.zeros((2 * L, 2 * L))
    def add(a, b, w):                 # term w * i g_a g_b  ->  (i/4)(A_ab g_a g_b + A_ba g_b g_a) with A_ab = 2w
        A[a, b] += 2 * w; A[b, a] -= 2 * w
    for j in range(L):
        add(2 * j, 2 * j + 1, -1.0)                       # -X_j
    for j in range(L - 1):
        add(2 * j + 1, 2 * j + 2, +1.0)                   # -Z_j Z_{j+1} = +i g g
    return A


def gamma_imag_temp(A, R_H, delta=0.0):
    """Majorana correlation matrix of exp(i R_H H)/Tr, H = (i/4) g^T A g.
    Gamma = tanh(beta * (i A)/2) style; with beta = -i R_H it is complex antisymmetric."""
    M = 1j * A                                            # Hermitian
    w, U = eigh(M)                                        # M = U diag(w) U^dag, eigenvalues +/- eps_k
    t = np.tanh((delta - 1j * R_H) * w / 2.0)            # tanh(beta w / 2), beta = delta - i R_H  (paper: R -> R + i delta)
    G = U @ np.diag(t) @ U.conj().T                       # this is Gamma' = i Gamma; antisymmetric part below
    Gam = -1j * G                                         # Gamma_ab = (i/2)<[g_a, g_b]>  (sign irrelevant for S)
    return Gam


def gaussian_nu(Gam_A):
    ev = eigvals(Gam_A)
    nu = ev / 1j
    return nu[np.argsort(-nu.real)][: len(nu) // 2]        # one of each +/- pair (pairs are exact up to roundoff)


def gaussian_spectrum(nu):
    """All 2^T0 many-body eigenvalues of tau_A implied by the mode values nu (branch-free object)."""
    lam = np.array([1.0 + 0j])
    for v in nu:
        lam = np.concatenate([lam * (1 + v) / 2, lam * (1 - v) / 2])
    return lam


def gaussian_S(Gam_A):
    """Pseudo entropy of a Gaussian operator from its restricted Majorana correlator, PER-MODE
    principal branch (the paper's eq. 2.44 convention). Differs from the per-eigenvalue principal
    branch of route_X exactly when many-body eigenvalues wrap the negative real axis."""
    nu = gaussian_nu(Gam_A)
    p = (1.0 + nu) / 2.0; q = (1.0 - nu) / 2.0
    def xlogx(z):
        return np.where(np.abs(z) < 1e-300, 0.0, z * np.log(z.astype(complex)))
    return complex(np.sum(-xlogx(p) - xlogx(q)))


def route_G(L, R_H, T0_list, delta=0.0):
    A = majorana_A(L); Gam = gamma_imag_temp(A, R_H, delta)
    out = {}
    for T0 in T0_list:
        s = (L - T0) // 2
        idx = np.arange(2 * s, 2 * (s + T0))
        GA = Gam[np.ix_(idx, idx)]
        nu = gaussian_nu(GA)
        rec = {"S_mode_branch": gaussian_S(GA), "S_eig_branch": None, "spectrum": None}
        if T0 <= 12:                                       # 2^T0 many-body eigenvalues: only for the EXACT gate sizes
            lam = gaussian_spectrum(nu); lam = lam[np.abs(lam) > 1e-14]
            rec["S_eig_branch"] = complex(np.sum(-lam * np.log(lam)))   # same convention as route_X
            rec["spectrum"] = lam
        out[int(T0)] = rec
    return out


# ------------------------------------------------------------------------------ Route X
def tfim_dense(L):
    Z = np.array([[1.0, 0.0], [0.0, -1.0]]); X = np.array([[0.0, 1.0], [1.0, 0.0]]); I2 = np.eye(2)
    def site(op, j):
        m = np.array([[1.0]])
        for k in range(L):
            m = np.kron(m, op if k == j else I2)
        return m
    H = np.zeros((1 << L, 1 << L))
    for j in range(L):
        H -= site(X, j)
    for j in range(L - 1):
        H -= site(Z, j) @ site(Z, j + 1)
    return H


def route_X(L, R_H, T0_list, delta=0.0):
    H = tfim_dense(L); w, U = eigh(H)
    E = (U * np.exp((1j * R_H - delta) * w)) @ U.conj().T   # e^{i (R_H + i delta) H}
    tr = np.trace(E)
    out, branch = {}, {}
    for T0 in T0_list:
        s = (L - T0) // 2
        # sites ordered s..s+T0-1 are A; reshape indices (left, A, right) x (left, A, right)
        dl, da, dr = 1 << s, 1 << T0, 1 << (L - s - T0)
        M = E.reshape(dl, da, dr, dl, da, dr)
        tau = np.einsum("iajibj->ab", M) / tr
        lam = eigvals(tau)
        lam = lam[np.abs(lam) > 1e-14]
        S = complex(np.sum(-lam * np.log(lam)))
        out[int(T0)] = S
        branch[int(T0)] = {"max_abs_arg": float(np.max(np.abs(np.angle(lam)))), "spectrum": lam}
    return out, branch


# ------------------------------------------------------------------------------ analysis
def fit_slope(R, T0s, S_real):
    x = np.log((R / np.pi) * np.sin(np.pi * np.asarray(T0s) / R))
    b, a = np.polyfit(x, np.asarray(S_real), 1)
    return float(b), float(a)


def spec_diff(a, b):
    """Hausdorff distance between two eigenvalue multisets (lexicographic complex sort mis-pairs
    near-degenerate values, which produced a false EXACT-gate failure on 2026-09-07)."""
    if len(a) != len(b):
        return float("inf")
    D = np.abs(a[:, None] - b[None, :])
    return float(max(D.min(axis=1).max(), D.min(axis=0).max()))


def main():
    ap = argparse.ArgumentParser(); ap.add_argument("--quick", action="store_true"); args = ap.parse_args()
    t0 = time.time()
    rec = {"preregistration": "PREREGISTRATION-HYP032.md (approved 2026-09-07)", "derivation": "ROUTE-X-DERIVATION.md",
           "c": 0.5, "v": V, "REGISTERED": {}, "EXPLORATORY_post_hoc": {}}
    L_g = (64, 128) if args.quick else L_GAUSS
    reg = rec["REGISTERED"]

    # ---- EXACT gate (registered intent: Route G is an exact evaluation of Route X's operator).
    #      Implemented on the branch-free SPECTRUM of tau_A, because S itself is branch-dependent
    #      (found 2026-09-07 on the first run; recorded, not hidden). Both S conventions reported.
    exact_ok, worst, im_max = True, 0.0, 0.0
    reg["EXACT_gate"] = {}
    for L in L_EXACT:
        for R_H in (3.0, 4.0):
            T0s = list(range(1, L // 2 + 1))
            SX, br = route_X(L, R_H, T0s); SG = route_G(L, R_H, T0s)
            d = max(spec_diff(br[t]["spectrum"], SG[t]["spectrum"]) for t in T0s); worst = max(worst, d)
            im = max(abs(SX[t].imag) for t in T0s); im_max = max(im_max, im)
            dS_eig = max(abs(SX[t] - SG[t]["S_eig_branch"]) for t in T0s)
            dS_mode = max(abs(SX[t] - SG[t]["S_mode_branch"]) for t in T0s)
            reg["EXACT_gate"][f"L{L}_RH{R_H}"] = {"max_spectrum_diff": d, "max_|Im S_X|": im,
                "max|S_X - S_G(eig branch)|": dS_eig, "max|S_X - S_G(mode branch)|": dS_mode,
                "S_X": {t: [SX[t].real, SX[t].imag] for t in T0s},
                "S_G_mode_branch": {t: [SG[t]["S_mode_branch"].real, SG[t]["S_mode_branch"].imag] for t in T0s}}
            print(f"EXACT L={L} R_H={R_H}: spectrum diff {d:.1e} | max|Im S_X| {im:.1e} | S diff eig-branch {dS_eig:.1e}, mode-branch {dS_mode:.1e}")
            exact_ok = exact_ok and d < 1e-10
    reg["EXACT_gate"]["pass"] = bool(exact_ok); reg["EXACT_gate"]["worst_spectrum_diff"] = worst
    reg["Im_S_identically_zero_at_delta0"] = {"max_|Im S_X| over all exact points": im_max,
        "reason": "V = prod_j Y_j * prod_{j even} X_j is a local unitary with V H V^dag = -H for the TFIM, so "
                  "tau_A(R) is unitarily similar (within A) to tau_A(-R) = tau_A(R)^dag; the spectrum is closed "
                  "under conjugation and -sum lam log lam is real in any conjugation-symmetric branch convention."}
    if not exact_ok:
        print("!! EXACT gate FAILED: Route G VOID."); reg["L1_VERDICT"] = "VOID (EXACT gate)"
        json.dump(rec, open(os.path.join(HERE, "tlee_level1_results.json"), "w"), indent=1, default=float); sys.exit(2)

    # ---- Level 1 as registered (delta = 0), Route G at large L
    reg["L1"] = {}
    allpass = True
    for R_H in R_H_LIST:
        R = V * R_H; T0s = list(range(2, int(R) - 1))
        S_by_L = {L: route_G(L, R_H, T0s) for L in L_g}
        Lmax = max(L_g); S = S_by_L[Lmax]
        end = max(abs(S_by_L[Lmax][t]["S_mode_branch"] - S_by_L[min(L_g)][t]["S_mode_branch"]) for t in T0s)
        sym = max(abs(S[t]["S_mode_branch"] - S[int(R) - t]["S_mode_branch"]) for t in T0s if (int(R) - t) in S)
        win = [t for t in T0s if 3 <= t <= R / 2]
        sl_mode, _ = fit_slope(R, win, [S[t]["S_mode_branch"].real for t in win])
        sl_eig = float("nan")
        ims = np.array([S[t]["S_mode_branch"].imag for t in win])
        im_ok = bool(np.all(np.abs(np.abs(ims) - IM_PRED) < 0.03 * IM_PRED) and (np.all(ims > 0) or np.all(ims < 0)))
        sl_ok = bool(abs(sl_mode - C_THIRD) < 0.03 * C_THIRD)
        allpass = allpass and im_ok and sl_ok and end < 1e-3 and sym < 1e-3
        reg["L1"][str(R_H)] = {"R": R, "L": Lmax, "window": win, "slope_mode_branch": sl_mode, "slope_eig_branch": sl_eig,
            "slope_pred": C_THIRD, "slope_pass": sl_ok, "Im_mean": float(ims.mean()), "Im_max_abs": float(np.abs(ims).max()),
            "Im_pred": IM_PRED, "Im_pass": im_ok, "END_maxdiff": end, "SYM_maxdiff": sym,
            "S_mode_branch": {t: [S[t]["S_mode_branch"].real, S[t]["S_mode_branch"].imag] for t in T0s},
            }
        print(f"L1 delta=0 R_H={R_H:4.1f} L={Lmax}: slope mode/eig = {sl_mode:.4f}/{sl_eig:.4f} (pred {C_THIRD:.4f}) {'PASS' if sl_ok else 'FAIL'} | "
              f"max|Im S| {np.abs(ims).max():.1e} (pred {IM_PRED:.4f}) {'PASS' if im_ok else 'FAIL'} | END {end:.1e} SYM {sym:.1e}")
    reg["L1_VERDICT"] = "PASS" if allpass else "VOID (registered Level-1 criterion not met at delta = 0)"
    print("REGISTERED LEVEL-1 VERDICT:", reg["L1_VERDICT"])

    # ---- EXPLORATORY (post hoc, NOT registered): the paper's regulator R -> R + i delta, i.e. e^{iRH} e^{-delta H}.
    #      PAPER-139 Fig. 6: their imaginary part appears only as delta grows. Reproduced here at c = 1/2.
    ex = rec["EXPLORATORY_post_hoc"]; ex["note"] = ("Added after the delta = 0 run showed Im S = 0 exactly. Not part of the "
        "pre-registered verdict. Reported as a Level-2 method observation only.")
    L = max(L_g); R_H = 8.0; R = V * R_H; T0s = list(range(2, int(R) - 1)); win = [t for t in T0s if 3 <= t <= R / 2]
    for delta in (0.25, 0.5, 1.0, 2.0, 4.0, 8.0):
        S = route_G(L, R_H, T0s, delta=delta)
        ims = np.array([S[t]["S_mode_branch"].imag for t in win]); sl, _ = fit_slope(R, win, [S[t]["S_mode_branch"].real for t in win])
        ex[f"delta{delta}"] = {"L": L, "R_H": R_H, "slope_mode_branch": sl, "Im_by_T0": {t: S[t]["S_mode_branch"].imag for t in T0s},
                               "Re_by_T0": {t: S[t]["S_mode_branch"].real for t in T0s},
                               "Im_mean_window": float(ims.mean()), "Im_std_window": float(ims.std())}
        print(f"EXPLORATORY delta={delta:4.2f}: slope {sl:.4f}  Im S window mean {ims.mean():+.4f} +/- {ims.std():.4f}  (pi/12 = {IM_PRED:.4f})")
    print(f"done ({time.time()-t0:.0f}s)")
    json.dump(rec, open(os.path.join(HERE, "tlee_level1_results.json"), "w"), indent=1, default=float)


if __name__ == "__main__":
    main()
