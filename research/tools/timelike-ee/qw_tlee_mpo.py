#!/usr/bin/env python3
"""
qw_tlee_mpo.py -- SIM-2026-078: the HYP-032 C1 thread at large L.

Registered by PREREGISTRATION-HYP032-B.md (approved by Jon 2026-09-09, commit 4743b8c, BEFORE this
file existed). Method: complex-time matrix-product-operator evolution of

    M(beta) = e^{-beta H},   beta = delta - i R_H,   H = -sum ZZ - sum X - h_z sum Z  (open chain)

then tau_A = Tr_B[M] / Tr[M] with A the centred block of T0 sites (identical placement to SIM-077),
and S = -sum lambda log lambda over eigenvalues |lambda| > 1e-14, per-eigenvalue principal branch --
the same branch convention as SIM-077's C1, so the numbers are directly comparable.

Why an MPO: h_z breaks the free-fermion structure that the Gaussian route needs, and exact
diagonalisation stops at L = 14. The question (does the SIM-077 point survive at large L, or does it
move as a finite-size resonance) is only answerable above L = 14.

GATES -- every one can void, none is decorative:
  G1 EXACTNESS (hard)  L = 12, 14 vs SIM-077's stored ED numbers, 1e-6, real and imaginary
  G2 SYMMETRY          h_z = 0, delta = 0  =>  |Im S| < 1e-8 where the MPO is exact: L = 8,
                       chi = 256 (SIM-076 theorem; AMENDED 2026-09-18, ERRATA D10)
  G3 CHI CONVERGENCE   doubling chi moves Im S < 2 %, else the point is UNCONVERGED and excluded
  G4 TROTTER           halving d beta moves Im S < 1 %, else UNCONVERGED and excluded
  G5 BACKGROUND        h_z = 0 run at every (L, R_H, delta); signal must exceed it by 5x

Usage:
  python qw_tlee_mpo.py --gate-smoke          # G1/G2 at L <= 12 only (permitted locally, seconds)
  python qw_tlee_mpo.py --gate G1             # full G1 including L = 14
  python qw_tlee_mpo.py --run                 # the registered grid (pod only)
"""
import argparse, json, os, sys, time

# One BLAS thread per process, set BEFORE numpy loads. Measured on this hardware: a 256x256 complex
# SVD takes 22 ms at 1 thread and 94 ms at 8 -- small-matrix thread thrashing, the same trap already
# recorded for MERAKit in CLAUDE.md. Parallelism belongs across grid points (one process each),
# not inside a 256x256 factorisation.
for _v in ('OPENBLAS_NUM_THREADS', 'OMP_NUM_THREADS', 'MKL_NUM_THREADS', 'NUMEXPR_NUM_THREADS'):
    os.environ.setdefault(_v, '1')

import numpy as np
from numpy.linalg import eigvals, qr, svd
from scipy.linalg import expm

HERE = os.path.dirname(os.path.abspath(__file__))
V = 2.0                       # R = v * R_H, v = 2, as in SIM-076/077
PRED = np.pi * 0.5 / 6        # pi c / 6 at c = 1/2 = 0.261799...

I2 = np.eye(2)
X = np.array([[0.0, 1.0], [1.0, 0.0]])
Z = np.array([[1.0, 0.0], [0.0, -1.0]])


# ------------------------------------------------------------------ MPO container
# W[j] has shape (Dl, out, in, Dr).  M[(o0 o1 ...), (i0 i1 ...)] = prod_j W[j], site 0 leftmost /
# most significant -- matching the kron ordering of qw_tlee_level1.tfim_dense and the
# (left, A, right) reshape used by SIM-077's route_X_H.

class MPO(list):
    """List of rank-4 tensors plus the index of the orthogonality centre."""
    centre = 0


def mpo_identity(L):
    W = np.eye(2).reshape(1, 2, 2, 1).astype(complex)
    return MPO(W.copy() for _ in range(L))


def bond_hamiltonian(L, j, hz):
    """h_{j,j+1} with each site's field split evenly over the bonds that touch it, so that
    sum_j h_{j,j+1} == H exactly (checked by G1, and directly by _check_bond_sum)."""
    # a site's transverse/longitudinal field is split over the bonds touching it: 1 at the ends, 2 in the bulk
    n_left = 1 if j == 0 else 2
    n_right = 1 if j + 1 == L - 1 else 2
    h = -np.kron(Z, Z)
    h -= np.kron(X, I2) / n_left + np.kron(I2, X) / n_right
    if hz != 0.0:
        h -= hz * (np.kron(Z, I2) / n_left + np.kron(I2, Z) / n_right)
    return h


def _suzuki_sequence(order):
    """Flat sweep sequence for the product formula, adjacent same-set steps merged.
    S2(c) = E(c/2) O(c) E(c/2);  S4(1) = S2(p)S2(p)S2(q)S2(p)S2(p), q = 1 - 4p.
    Returns [(set_name, coefficient), ...]. Merging cuts S4 from 15 sweeps to 11."""
    if order == 2:
        cs = [1.0]
    elif order == 4:
        pp = 1.0 / (4.0 - 4.0 ** (1.0 / 3.0))
        cs = [pp, pp, 1.0 - 4.0 * pp, pp, pp]
    else:
        raise ValueError('order must be 2 or 4')
    seq = []
    for c in cs:
        seq += [('E', c / 2), ('O', c), ('E', c / 2)]
    merged = [seq[0]]
    for name, c in seq[1:]:
        if name == merged[-1][0]:
            merged[-1] = (name, merged[-1][1] + c)
        else:
            merged.append((name, c))
    return merged


def trotter_gates(L, hz, dbeta, order=4):
    """Gate sets for each distinct coefficient in the product formula."""
    seq = _suzuki_sequence(order)
    coeffs = sorted({round(c, 15) for _, c in seq})
    hs = [bond_hamiltonian(L, j, hz) for j in range(L - 1)]
    gates = {c: [expm(-c * dbeta * h).reshape(2, 2, 2, 2) for h in hs] for c in coeffs}
    even = [j for j in range(L - 1) if j % 2 == 0]
    odd = [j for j in range(L - 1) if j % 2 == 1]
    plan = [(gates[round(c, 15)], even if name == 'E' else odd) for name, c in seq]
    return plan


# ------------------------------------------------------------------ canonical form and gate application

def _move_center_right(Ws, j):
    Dl, _, _, Dr = Ws[j].shape
    Q, R = qr(Ws[j].reshape(Dl * 4, Dr))
    Ws[j] = Q.reshape(Dl, 2, 2, -1)
    Ws[j + 1] = np.tensordot(R, Ws[j + 1], axes=(1, 0))


def _move_center_left(Ws, j):
    """Move the orthogonality centre from site j to site j-1."""
    Dl, _, _, Dr = Ws[j].shape
    Q, R = qr(Ws[j].reshape(Dl, 4 * Dr).T.conj())
    Ws[j] = (Q.T.conj()).reshape(-1, 2, 2, Dr)
    Ws[j - 1] = np.tensordot(Ws[j - 1], R.T.conj(), axes=(3, 0))


def right_canonicalize(Ws):
    for j in range(len(Ws) - 1, 0, -1):
        _move_center_left(Ws, j)
    Ws[0] = Ws[0] / np.linalg.norm(Ws[0])
    Ws.centre = 0
    return Ws


def _apply_bond(Ws, j, g, chi, tol, stats, to_right=True):
    """Apply the two-site gate g on the OUT legs of sites (j, j+1). Assumes the orthogonality
    centre sits on j (if to_right) or j+1 (if not). Leaves it on the far side."""
    A, B = Ws[j], Ws[j + 1]
    Dl, Dr = A.shape[0], B.shape[3]
    theta = np.tensordot(A, B, axes=(3, 0))                       # a o i p j c
    theta = np.einsum('OPop,aoipjc->aOiPjc', g, theta, optimize=True)
    mat = theta.reshape(Dl * 4, 4 * Dr)
    U, s, Vh = svd(mat, full_matrices=False)
    keep = max(1, int(np.sum(s / s[0] > tol)))
    keep = min(keep, chi, len(s))
    disc = float(np.sum(s[keep:] ** 2) / np.sum(s ** 2)) if keep < len(s) else 0.0
    stats['max_disc'] = max(stats['max_disc'], disc)
    stats['max_chi'] = max(stats['max_chi'], keep)
    U, s, Vh = U[:, :keep], s[:keep], Vh[:keep]
    s = s / np.linalg.norm(s)                                     # overall scale is irrelevant
    if to_right:
        Ws[j] = U.reshape(Dl, 2, 2, keep)
        Ws[j + 1] = (s[:, None] * Vh).reshape(keep, 2, 2, Dr)
    else:
        Ws[j] = (U * s[None, :]).reshape(Dl, 2, 2, keep)
        Ws[j + 1] = Vh.reshape(keep, 2, 2, Dr)


def evolve(L, hz, beta, dbeta, chi, tol=1e-14, order=4, verbose=False):
    """M = e^{-beta H} as an MPO by a fourth-order product formula. Returns (Ws, stats).
    Fourth order because second order plateaus near 1e-4 at an affordable step, and gate G1
    is a 1e-6 bar that was fixed before this file existed and is not negotiable."""
    n_steps = max(1, int(np.ceil(abs(beta) / dbeta)))
    db = beta / n_steps
    plan = trotter_gates(L, hz, db, order=order)
    Ws = right_canonicalize(mpo_identity(L))
    stats = {'max_disc': 0.0, 'max_chi': 1, 'n_steps': n_steps,
             'dbeta_eff': abs(db), 'order': order, 'chi_cap': chi}
    t0 = time.time()
    to_right = True
    for step in range(n_steps):
        for g, bonds in plan:
            # Alternate sweep direction between gate sets. Sweeping every set left-to-right drags
            # the orthogonality centre the full length of the chain 11 times per step, which at
            # L = 128 costs more QRs than the gates themselves.
            order_bonds = bonds if to_right else bonds[::-1]
            for j in order_bonds:
                target = j if to_right else j + 1
                while Ws.centre < target:
                    _move_center_right(Ws, Ws.centre); Ws.centre += 1
                while Ws.centre > target:
                    _move_center_left(Ws, Ws.centre); Ws.centre -= 1
                _apply_bond(Ws, j, g[j], chi, tol, stats, to_right=to_right)
                Ws.centre = j + 1 if to_right else j
            to_right = not to_right
        if verbose and (step % 5 == 0 or step == n_steps - 1):
            print(f"    step {step+1}/{n_steps}  chi={stats['max_chi']}  "
                  f"disc={stats['max_disc']:.2e}  {time.time()-t0:.0f}s", flush=True)
    stats['secs_evolve'] = time.time() - t0
    return Ws, stats



# ------------------------------------------------------------------ observables

def _traced(W):
    """Trace a site tensor over its physical pair: identity insertion on a B site."""
    return np.einsum('assb->ab', W)


def tau_A(Ws, T0):
    """tau_A = Tr_B[M] / Tr[M], with A the centred block of T0 sites -- the same placement
    (s = (L - T0) // 2) that SIM-077's route_X_H used, so the numbers are comparable.
    Dividing the traced block by its own trace IS dividing by Tr[M], so no second pass is needed."""
    L = len(Ws)
    s0 = (L - T0) // 2
    vl = np.ones(1, dtype=complex)
    for j in range(s0):
        vl = vl @ _traced(Ws[j])
    vr = np.ones(1, dtype=complex)
    for j in range(L - 1, s0 + T0 - 1, -1):
        vr = _traced(Ws[j]) @ vr
    T = vl.reshape(1, 1, -1)                                    # (out_dim, in_dim, bond)
    for j in range(s0, s0 + T0):
        T = np.einsum('OIb,boic->OoIic', T, Ws[j], optimize=True)   # b = incoming bond, c = outgoing
        T = T.reshape(T.shape[0] * 2, T.shape[2] * 2, T.shape[4])
    M = T @ vr                                                  # (2^T0, 2^T0)
    tr = np.trace(M)
    if abs(tr) < 1e-300:
        raise FloatingPointError('Tr M underflowed')
    return M / tr


def entropy(tau):
    """S = -sum lambda log lambda, per-eigenvalue principal branch (SIM-077 C1 convention)."""
    lam = eigvals(tau)
    lam = lam[np.abs(lam) > 1e-14]
    return complex(np.sum(-lam * np.log(lam)))


def windows(R):
    """The registered window, unchanged from PREREGISTRATION-HYP032-A: T0 in [3, R/2]."""
    T0s = list(range(2, int(R) - 1))
    return T0s, [t for t in T0s if 3 <= t <= R / 2]


def S_of(L, hz, R_H, delta, T0_list, chi, dbeta, order=4, verbose=False):
    beta = delta - 1j * R_H
    Ws, stats = evolve(L, hz, beta, dbeta, chi, order=order, verbose=verbose)
    out = {}
    for T0 in T0_list:
        out[int(T0)] = entropy(tau_A(Ws, T0))
    return out, stats


# ------------------------------------------------------------------ gates

def check_bond_sum(L, hz):
    """Structural: the Trotter decomposition must sum back to the exact H, else every gate below
    is testing the wrong Hamiltonian."""
    import qw_tlee_candidates as qc
    H = np.zeros((1 << L, 1 << L))
    for j in range(L - 1):
        h = bond_hamiltonian(L, j, hz)
        H += np.kron(np.kron(np.eye(1 << j), h), np.eye(1 << (L - j - 2)))
    err = float(np.max(np.abs(H - qc.tfim_dense_hz(L, hz))))
    return {'max_abs_err': err, 'pass': bool(err < 1e-12)}


def gate_G1(Ls=(12, 14), chi=128, dbeta=0.05, tol=1e-6, settings=None, verbose=False):
    """EXACTNESS (hard). MPO vs exact diagonalisation, same (h_z, R_H, delta, T0)."""
    import qw_tlee_candidates as qc
    settings = settings or [(12, 0.02, 4.0, 5.0), (14, 0.02, 5.0, 5.0)]
    rows, ok = [], True
    for (L, hz, R_H, delta) in settings:
        if L not in Ls:
            continue
        R = V * R_H
        T0s, win = windows(R)
        H = qc.tfim_dense_hz(L, hz)
        qc._H_EIG.clear()
        exact = qc.route_X_H(H, L, R_H, T0s, delta)
        got, stats = S_of(L, hz, R_H, delta, T0s, chi, dbeta, verbose=verbose)
        for T0 in T0s:
            dre = abs(got[T0].real - exact[T0].real)
            dim = abs(got[T0].imag - exact[T0].imag)
            good = bool(dre < tol and dim < tol)
            ok = ok and good
            rows.append({'L': L, 'hz': hz, 'R': R, 'delta': delta, 'T0': T0,
                         'exact': [exact[T0].real, exact[T0].imag],
                         'mpo': [got[T0].real, got[T0].imag],
                         'd_re': dre, 'd_im': dim, 'pass': good})
            print(f"  G1 L={L} hz={hz} R={R:.0f} d={delta:.0f} T0={T0}: "
                  f"exact {exact[T0].real:+.6f}{exact[T0].imag:+.6f}i  "
                  f"mpo {got[T0].real:+.6f}{got[T0].imag:+.6f}i  "
                  f"dre={dre:.2e} dim={dim:.2e} {'ok' if good else 'FAIL'}", flush=True)
        rows[-1]['stats'] = stats
    return {'tol': tol, 'chi': chi, 'dbeta': dbeta, 'rows': rows, 'pass': bool(ok)}


def gate_G2(Ls=(8,), chi=256, dbeta=0.1, tol=1e-8, disc_tol=1e-20):
    """SYMMETRY. h_z = 0, delta = 0  =>  Im S == 0 (SIM-076 theorem) through the new code path.

    AMENDED 2026-09-18 (ERRATA D10, Jon's ruling). Registered at L = 12/16/24, chi = 128, where
    undamped delta = 0 evolution cannot converge. Binds only where the MPO is exact (discarded
    weight < disc_tol); the exactness condition is part of the gate because a truncated run can
    show Im S ~ 1e-13 with the real part wrong by 3 (L = 8, chi = 64)."""
    rows, ok = [], True
    for L in Ls:
        R_H = 5.0
        T0s, _ = windows(V * R_H)
        got, stats = S_of(L, 0.0, R_H, 0.0, T0s, chi, dbeta)
        mx = float(max(abs(got[t].imag) for t in T0s))
        good = bool(mx < tol and stats['max_disc'] < disc_tol)
        ok = ok and good
        rows.append({'L': L, 'max_abs_Im': mx, 'pass': good, 'max_chi': stats['max_chi'],
                     'max_disc': stats['max_disc']})
        print(f"  G2 L={L}: max|Im S| = {mx:.3e}  {'ok' if good else 'FAIL'}", flush=True)
    return {'tol': tol, 'rows': rows, 'pass': bool(ok)}


# ------------------------------------------------------------------ the registered grid

LS = (16, 24, 32, 48, 64, 96, 128)
HZS = (0.0, 0.0003, 0.001, 0.003, 0.005, 0.01, 0.02, 0.05)
SETTINGS = {'A': (5.0, 5.0), 'B': (8.0, 5.0), 'C': (12.0, 5.0)}     # (R_H, delta)


def verdict(ims, full_ims, bg=None):
    """The registered YES conditions that can be evaluated at a single (L, hz, setting).
    The three-size rule and the h_z* motion rule are evaluated in the summary, not here."""
    ims = np.asarray(ims, float)
    full = np.asarray(full_ims, float)
    m = float(ims.mean())
    one_sign = bool(np.all(ims > 0) or np.all(ims < 0))
    within = bool(abs(abs(m) - PRED) < 0.10 * PRED)
    stable = bool(ims.std() < 0.10 * abs(m)) if abs(m) > 0 else False
    drift = float((full.max() - full.min()) / abs(full.mean())) if abs(full.mean()) > 0 else np.inf
    plateau = bool(drift < 0.10)                       # the condition the SIM-077 point fails by 52%
    over_bg = bool(bg is None or abs(m) > 5.0 * abs(bg))
    return {'Im_mean': m, 'Im_std': float(ims.std()), 'pred': PRED, 'one_sign': one_sign,
            'within_10pct': within, 'stable_in_window': stable, 'full_range_drift': drift,
            'plateau': plateau, 'background': bg, 'exceeds_bg_5x': over_bg,
            'YES_at_this_size': bool(one_sign and within and stable and plateau and over_bg)}


def run_point(L, hz, R_H, delta, chi, dbeta, order=4, verbose=False):
    T0s, win = windows(V * R_H)
    got, stats = S_of(L, hz, R_H, delta, T0s, chi, dbeta, order=order, verbose=verbose)
    return {'L': L, 'hz': hz, 'R': V * R_H, 'delta': delta, 'window': win,
            'S': {int(t): [got[t].real, got[t].imag] for t in T0s},
            'ims_window': [got[t].imag for t in win],
            'ims_full': [got[t].imag for t in T0s], 'stats': stats}


def run_point_gated(L, hz, R_H, delta, chi, dbeta, bg=None, order=4, verbose=False):
    """One registered point plus its two convergence controls (G3, G4). A point that fails either
    is marked UNCONVERGED here and excluded from the verdict by the summary -- never rounded in."""
    base = run_point(L, hz, R_H, delta, chi, dbeta, order=order, verbose=verbose)
    half = run_point(L, hz, R_H, delta, max(8, chi // 2), dbeta, order=order)
    coarse = run_point(L, hz, R_H, delta, chi, 2 * dbeta, order=order)

    def rel(a, b):
        a, b = np.asarray(a, float), np.asarray(b, float)
        scale = max(abs(a.mean()), 1e-6)
        return float(np.max(np.abs(a - b)) / scale)

    g3 = rel(base['ims_window'], half['ims_window'])
    g4 = rel(base['ims_window'], coarse['ims_window'])
    base['G3_chi'] = {'chi_half': max(8, chi // 2), 'rel_change': g3, 'pass': bool(g3 < 0.02)}
    base['G4_trotter'] = {'dbeta_coarse': 2 * dbeta, 'rel_change': g4, 'pass': bool(g4 < 0.01)}
    base['converged'] = bool(g3 < 0.02 and g4 < 0.01)
    base['verdict'] = verdict(base['ims_window'], base['ims_full'], bg=bg)
    if not base['converged']:
        base['verdict']['YES_at_this_size'] = False
        base['verdict']['status'] = 'UNCONVERGED - excluded from the verdict'
    return base


def _worker(task):
    L, hz, R_H, delta, chi, dbeta, order = task
    try:
        p = run_point_gated(L, hz, R_H, delta, chi, dbeta, bg=None, order=order)
    except Exception as e:
        p = {'error': f"{type(e).__name__}: {e}", 'L': L, 'hz': hz}
    return (L, hz, p)


def run_grid(setting, Ls, hzs, chi, dbeta, out_path, order=4, workers=None, verbose=False):
    """The registered grid for one setting. Points run in parallel processes -- one BLAS thread
    each, which is where the pod's vCPUs belong. Verdicts are attached in the parent, after the
    h_z = 0 background for that L is known (gate G5)."""
    from concurrent.futures import ProcessPoolExecutor
    R_H, delta = SETTINGS[setting]
    workers = workers or max(1, (os.cpu_count() or 2) - 1)
    rec = {'sim': 'SIM-2026-078', 'preregistration': 'PREREGISTRATION-HYP032-B.md',
           'setting': setting, 'R_H': R_H, 'delta': delta, 'R': V * R_H,
           'method': 'complex-time MPO, 4th-order product formula, own numpy',
           'branch': 'per-eigenvalue principal (same convention as SIM-077 C1)',
           'chi': chi, 'dbeta': dbeta, 'order': order, 'workers': workers,
           'started': time.strftime('%Y-%m-%dT%H:%M:%S'), 'points': {}, 'background': {}}
    tasks = [(L, hz, R_H, delta, chi, dbeta, order) for L in Ls for hz in hzs]
    print(f"setting {setting} (R_H={R_H}, delta={delta}): {len(tasks)} points on {workers} workers",
          flush=True)
    t0 = time.time()
    done = 0
    with ProcessPoolExecutor(max_workers=workers) as ex:
        for L, hz, p in ex.map(_worker, tasks):
            done += 1
            key = f"L{L}_hz{hz}"
            rec['points'][key] = p
            if 'error' in p:
                print(f"  [{done}/{len(tasks)}] {key}: ERROR {p['error']}", flush=True)
            else:
                if hz == 0.0:
                    rec['background'][f"L{L}"] = float(np.mean(p['ims_window']))
                print(f"  [{done}/{len(tasks)}] {key}: Im {np.mean(p['ims_window']):+.4f} "
                      f"(pred {PRED:.4f})  chi {p['stats']['max_chi']}  "
                      f"G3 {p['G3_chi']['rel_change']:.3f} G4 {p['G4_trotter']['rel_change']:.3f}  "
                      f"[{time.time()-t0:.0f}s]", flush=True)
            json.dump(rec, open(out_path, 'w'), indent=1, default=float)    # after EVERY point
    for key, p in rec['points'].items():
        if 'error' in p:
            continue
        bg = rec['background'].get(f"L{p['L']}")
        p['verdict'] = verdict(p['ims_window'], p['ims_full'], bg=bg)
        if not p['converged']:
            p['verdict']['YES_at_this_size'] = False
            p['verdict']['status'] = 'UNCONVERGED - excluded from the verdict'
    rec['finished'] = time.strftime('%Y-%m-%dT%H:%M:%S')
    rec['secs_total'] = time.time() - t0
    json.dump(rec, open(out_path, 'w'), indent=1, default=float)
    return rec


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--gate-smoke', action='store_true', help='G1/G2 at L <= 12 only (local, seconds)')
    ap.add_argument('--gate', choices=['G1', 'G2', 'all'], help='full gates including L = 14 (pod)')
    ap.add_argument('--run', action='store_true')
    ap.add_argument('--summarize', action='store_true')
    ap.add_argument('--setting', default='A', choices=list(SETTINGS))
    ap.add_argument('--Ls', default=','.join(map(str, LS)))
    ap.add_argument('--hzs', default=','.join(map(str, HZS)))
    ap.add_argument('--chi', type=int, default=128)
    ap.add_argument('--dbeta', type=float, default=0.25)
    ap.add_argument('--order', type=int, default=4)
    ap.add_argument('--workers', type=int, default=None)
    ap.add_argument('--out', default=None)
    ap.add_argument('--verbose', action='store_true')
    a = ap.parse_args()

    if a.gate_smoke:
        print('bond-sum structural check (Trotter decomposition must sum back to H):')
        for L in (6, 8, 10, 12):
            for hz in (0.0, 0.02):
                r = check_bond_sum(L, hz)
                print(f"  L={L} hz={hz}: err {r['max_abs_err']:.1e} {'ok' if r['pass'] else 'FAIL'}")
        print('G1 at L = 12 only:')
        g1 = gate_G1(Ls=(12,), chi=a.chi, dbeta=0.05, settings=[(12, 0.02, 4.0, 5.0)],
                     verbose=a.verbose)
        print('G2 at L = 8, chi = 256 (amended, ERRATA D10):')
        g2 = gate_G2()
        out = {'bond_sum': True, 'G1': g1, 'G2': g2}
        json.dump(out, open(os.path.join(HERE, 'sim078_gate_smoke.json'), 'w'), indent=1, default=float)
        print(f"SMOKE: G1 {'PASS' if g1['pass'] else 'FAIL'}  G2 {'PASS' if g2['pass'] else 'FAIL'}")
        return 0 if (g1['pass'] and g2['pass']) else 1

    if a.gate:
        out = {}
        if a.gate in ('G1', 'all'):
            out['G1'] = gate_G1(chi=a.chi, dbeta=0.05, verbose=a.verbose)
        if a.gate in ('G2', 'all'):
            out['G2'] = gate_G2()       # fixed L = 8, chi = 256: --chi does not apply (ERRATA D10)
        json.dump(out, open(os.path.join(HERE, 'sim078_gates.json'), 'w'), indent=1, default=float)
        ok = all(v['pass'] for v in out.values())
        print('GATES:', 'PASS' if ok else 'FAIL')
        return 0 if ok else 1

    if a.summarize:
        paths = [os.path.join(HERE, f'sim078_setting{k}.json') for k in SETTINGS]
        out = summarize(paths)
        json.dump(out, open(os.path.join(HERE, 'sim078_summary.json'), 'w'), indent=1, default=float)
        for st, v in out['settings'].items():
            print(f"setting {st}: {v['verdict']}  peak_hz_by_L={v['peak_motion']['peak_hz_by_L']}  "
                  f"slope={v['peak_motion'].get('fitted_slope')} (artifact law {-Y_RG})")
        print('OVERALL:', out['overall'])
        return 0

    if a.run:
        Ls = tuple(int(x) for x in a.Ls.split(','))
        hzs = tuple(float(x) for x in a.hzs.split(','))
        if hzs[0] != 0.0:
            print('refusing to run: h_z = 0 is the registered G5 background and must come first')
            return 2
        out_path = a.out or os.path.join(HERE, f'sim078_setting{a.setting}.json')
        run_grid(a.setting, Ls, hzs, a.chi, a.dbeta, out_path, order=a.order,
                 workers=a.workers, verbose=a.verbose)
        print('wrote', out_path)
        return 0

    ap.print_help()
    return 0


if __name__ == '__main__':
    sys.exit(main())


# ------------------------------------------------------------------ the registered summary

Y_RG = 15.0 / 8.0          # h_z is relevant with RG dimension 2 - 1/8, so xi ~ h_z^(-8/15)


def summarize(paths):
    """Apply the pre-registered rules that span sizes: the three-consecutive-size YES rule, and the
    two ARTIFACT rules. Nothing here may be re-tuned -- every threshold comes from the document."""
    out = {'settings': {}, 'preregistration': 'PREREGISTRATION-HYP032-B.md'}
    for path in paths:
        if not os.path.exists(path):
            continue
        rec = json.load(open(path))
        st = rec['setting']
        pts = {k: v for k, v in rec['points'].items() if 'error' not in v}
        by = {}
        for v in pts.values():
            by.setdefault(float(v['hz']), {})[int(v['L'])] = v
        Ls = sorted({int(v['L']) for v in pts.values()})

        # --- YES: three or more CONSECUTIVE registered sizes at one (hz, setting)
        yes_runs = {}
        for hz, d in by.items():
            flags = [bool(d.get(L, {}).get('verdict', {}).get('YES_at_this_size')) for L in Ls]
            best = run = 0
            for f in flags:
                run = run + 1 if f else 0
                best = max(best, run)
            if best:
                yes_runs[hz] = {'longest_consecutive': best, 'sizes': Ls, 'flags': flags}
        yes = {hz: r for hz, r in yes_runs.items() if r['longest_consecutive'] >= 3}

        # --- ARTIFACT rule 1: does the peak field move as L^(-15/8)?
        peaks = {}
        for L in Ls:
            cands = [(abs(float(np.mean(d[L]['ims_window']))), hz)
                     for hz, d in by.items() if hz > 0 and L in d and d[L].get('converged')]
            if cands:
                peaks[L] = max(cands)[1]
        motion = {'peak_hz_by_L': peaks}
        pl = sorted(peaks)
        if len(pl) >= 3 and all(peaks[L] > 0 for L in pl):
            sl = float(np.polyfit(np.log([float(L) for L in pl]),
                                  np.log([peaks[L] for L in pl]), 1)[0])
            lo, hi = pl[0], pl[-1]
            predicted = peaks[lo] * (hi / lo) ** (-Y_RG)
            ratio = peaks[hi] / predicted if predicted > 0 else np.inf
            motion.update(fitted_slope=sl, predicted_slope=-Y_RG,
                          predicted_hz_at_largest_L=predicted, observed=peaks[hi],
                          ratio_observed_over_predicted=ratio,
                          matches_artifact_law=bool(0.5 <= ratio <= 2.0))
        else:
            motion['matches_artifact_law'] = None
            motion['note'] = 'fewer than three sizes with a converged peak'

        # --- ARTIFACT rule 2: does Im S at h_z = 0.02 fall monotonically for L >= 32?
        d02 = by.get(0.02, {})
        big = [L for L in sorted(d02) if L >= 32 and d02[L].get('converged')]
        vals = [float(np.mean(d02[L]['ims_window'])) for L in big]
        falling = bool(len(vals) >= 3 and all(b < a for a, b in zip(vals, vals[1:])))
        decay = {'sizes': big, 'Im_mean': vals, 'monotone_falling_from_L32': falling}

        artifact = bool(motion.get('matches_artifact_law') or falling)
        out['settings'][st] = {
            'file': os.path.basename(path), 'sizes': Ls,
            'background_hz0': rec.get('background', {}),
            'YES_candidates': yes, 'peak_motion': motion, 'decay_at_hz_0.02': decay,
            'verdict': 'YES' if yes else ('ARTIFACT' if artifact else 'NEITHER'),
        }
    vs = [v['verdict'] for v in out['settings'].values()]
    out['overall'] = ('YES (Level-3 positive; section-8 novelty gate before any wording '
                      'stronger than "reproduced")' if 'YES' in vs else
                      'ARTIFACT (Level-3 negative; HYP-032 closes with the mechanism named)'
                      if 'ARTIFACT' in vs else
                      'NEITHER (Level-3 negative, unchanged from SIM-077; no third amendment)')
    return out
