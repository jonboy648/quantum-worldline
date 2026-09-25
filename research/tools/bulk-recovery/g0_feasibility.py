"""HYP-033 gate G0 (feasibility). Runs BEFORE the pre-registration is final, by its own rule.

Question: can f(A) = I(R_low:A) / 2 S(R_low) be computed with EXACT von Neumann entropies for the
registered family (27 sites, 3 layers, bond k = 2, regions up to 17 sites) on this machine?

Method ("option 2", Jon 2026-09-21): never build rho_A. Split the network's tensors into an A side
and a rest side along a minimal weighted cut K. Then |Phi> = sum_c |L_c>_A |R_c>_rest with c running
over the cut bonds (dimension D), and the nonzero spectrum of rho_A equals the spectrum of
GR^T @ GL, where GL[c',c] = <L_c'|L_c> and GR[c',c] = <R_c'|R_c> are D x D Gram matrices obtained by
contracting each side against its own conjugate.

Tensors here are HAAR-RANDOM isometries: G0 measures cost, not physics. No registered number comes
out of this file. Self-test: --selftest compares against a brute-force dense state on a 9-site network.
"""
import argparse
import itertools
import json
import math
import sys
import time

import networkx as nx
import numpy as np
import opt_einsum as oe
import scipy.linalg


def haar_isometry(rng, rows, cols):
    """rows x cols matrix with orthonormal columns (rows >= cols)."""
    z = rng.normal(size=(rows, cols)) + 1j * rng.normal(size=(rows, cols))
    q, r = np.linalg.qr(z)
    return q * (np.diagonal(r) / np.abs(np.diagonal(r)))


def build(N, chi, k, x, seed=0, d=4):
    """Return (tensors, dims). tensors: list of (name, array, [index labels]). Open indices:
    'p{i}' for boundary sites, 'Rlow', 'Rup'. Every open index sits on an identity 'cap' tensor so that
    a cut may pass between a physical leg and the tensor it enters."""
    rng = np.random.default_rng(seed)
    L = round(math.log(N, 3))
    # d = 4: the SIM-061 pipeline blocks two spins per site (ising_hamiltonian(block_size = 2))
    dim = [d] + [min(chi, d ** 3)] + [chi] * (L - 1)
    T, dims = [], {}

    def add(name, arr, idx):
        T.append((name, arr, idx))
        for i, d in zip(idx, arr.shape):
            assert dims.setdefault(i, d) == d, (name, i, d, dims[i])

    n = N
    for l in range(1, L + 1):
        din, nb, top = dim[l - 1], n // 3, l == L
        dout = 1 if top else dim[l]
        s = lambda i: f's{l-1}_{i % n}'
        t = lambda i: f't{l}_{i % n}'
        for j in range(nb):
            u = haar_isometry(rng, din * din, din * din).reshape(din, din, din, din)
            add(f'u{l}_{j}', u, [s(3 * j + 2), s(3 * j + 3), t(3 * j + 2), t(3 * j + 3)])
        for j in range(nb):
            w = haar_isometry(rng, din ** 3, dout).reshape(din, din, din, dout)
            up = f's{l}_{j}'
            if l == k and j == x:
                up = 'Rlow_in'
            if top:
                add(f'w{l}_{j}', w[..., 0], [t(3 * j), s(3 * j + 1), t(3 * j + 2)])
            else:
                add(f'w{l}_{j}', w, [t(3 * j), s(3 * j + 1), t(3 * j + 2), up])
        n = nb
    # rename the upper end of the cut bond, then cap every open index with an identity
    cut = f's{k}_{x}'
    T[:] = [(nm, a, ['Rup_in' if i == cut else i for i in idx]) for nm, a, idx in T]
    dims['Rup_in'] = dims.pop(cut)
    for i in range(N):
        add(f'cap_p{i}', np.eye(d), [f'p{i}', f's0_{i}'])
    add('cap_Rlow', np.eye(dims['Rlow_in']), ['Rlow', 'Rlow_in'])
    add('cap_Rup', np.eye(dims['Rup_in']), ['Rup', 'Rup_in'])
    return T, dims


def partition(T, dims, X):
    """Minimal weighted cut separating the caps of open indices X from the other caps."""
    G = nx.Graph()
    where = {}
    for nm, _, idx in T:
        for i in idx:
            where.setdefault(i, []).append(nm)
    for i, names in where.items():
        if len(names) == 2:
            a, b = names
            w = math.log(dims[i])
            G.add_edge(a, b, capacity=G[a][b]['capacity'] + w if G.has_edge(a, b) else w)
    caps = [nm for nm, _, _ in T if nm.startswith('cap_')]
    for c in caps:
        G.add_edge('SRC' if c[4:] in X else 'SNK', c, capacity=1e9)
    _, (S, _) = nx.minimum_cut(G, 'SRC', 'SNK')
    inside = {nm for nm, _, _ in T if nm in S}
    K = sorted(i for i, names in where.items() if len(names) == 2 and (names[0] in inside) != (names[1] in inside))
    return inside, K


def gram(T, dims, side, K, plan_only=False):
    """Gram matrix over the cut indices K for the tensors in `side`. Open indices are traced ket-bra."""
    sym, ops = {}, []
    g = lambda lab: sym.setdefault(lab, len(sym))
    for nm, a, idx in T:
        if nm not in side:
            continue
        # only OPEN indices are shared between ket and bra (that is the trace over the region);
        # internal bonds and cut bonds get separate ket and bra labels
        is_open = lambda i: i.startswith('p') or i in ('Rlow', 'Rup')
        ops += [a, [g(i) if is_open(i) else g(('k', i)) for i in idx]]
        ops += [a.conj(), [g(i) if is_open(i) else g(('b', i)) for i in idx]]
    out = [g(('b', i)) for i in K] + [g(('k', i)) for i in K]
    path, info = oe.contract_path(*ops, out, optimize='auto-hq', memory_limit=None)
    stats = dict(flops=float(info.opt_cost), largest=float(info.largest_intermediate))
    if plan_only:
        return None, stats
    D = int(np.prod([dims[i] for i in K])) if K else 1
    return oe.contract(*ops, out, optimize=path).reshape(D, D), stats


def entropy(T, dims, X, plan_only=False, max_gb=20.0):
    names = {nm for nm, _, _ in T}
    inside, K = partition(T, dims, set(X))
    D = int(np.prod([dims[i] for i in K])) if K else 1
    _, sL = gram(T, dims, inside, K, plan_only=True)
    _, sR = gram(T, dims, names - inside, K, plan_only=True)
    gb = 16 * max(sL['largest'], sR['largest'], D * D) / 2 ** 30
    info = dict(D=D, cut_bonds=len(K), flops=sL['flops'] + sR['flops'], peak_gb=gb)
    if plan_only or gb > max_gb:
        return None, info
    # Lean Hermitian route (2026-09-21, after a low-memory stop): spec(GR^T GL) = spec(B GR^T B^dag)
    # with GL = V diag(w) V^dag and B = sqrt(w) V^dag restricted to the numerical rank of GL.
    # Two Hermitian eigenproblems instead of one non-symmetric one, and matrices freed as we go.
    GL, _ = gram(T, dims, inside, K)
    w, V = scipy.linalg.eigh(GL, overwrite_a=True, check_finite=False)
    del GL
    keep = w > 1e-13 * w.max()
    B = (V[:, keep] * np.sqrt(w[keep])).conj().T          # r x D
    del V
    GR, _ = gram(T, dims, names - inside, K)
    M = B @ GR.T @ B.conj().T
    del GR, B
    ev = scipy.linalg.eigvalsh((M + M.conj().T) / 2, overwrite_a=True, check_finite=False)
    ev = ev[ev > 1e-14 * ev.max()]
    ev /= ev.sum()
    return float(-(ev * np.log(ev)).sum()), info


def f_of(T, dims, A, **kw):
    sites = [f'p{i}' for i in A]
    sR, _ = entropy(T, dims, ['Rlow'], **kw)
    sA, iA = entropy(T, dims, sites, **kw)
    sAR, iAR = entropy(T, dims, sites + ['Rlow'], **kw)
    ok = None not in (sR, sA, sAR)
    return ((sR + sA - sAR) / (2 * sR) if ok else None), sR, iA, iAR


def dense_entropy(T, dims, X):
    """Brute force, small networks only."""
    sym, ops = {}, []
    g = lambda lab: sym.setdefault(lab, len(sym))
    for _, a, idx in T:
        ops += [a, [g(i) for i in idx]]
    opens = sorted(i for i in dims if i.startswith('p') or i in ('Rlow', 'Rup'))
    keep = [i for i in opens if i in X]
    rest = [i for i in opens if i not in X]
    psi = oe.contract(*ops, [g(i) for i in keep + rest])
    M = psi.reshape(int(np.prod([dims[i] for i in keep])), -1)
    sv = np.linalg.svd(M, compute_uv=False) ** 2
    sv = sv[sv > 1e-14 * sv.max()]
    sv /= sv.sum()
    return float(-(sv * np.log(sv)).sum())


def cone(N, k, x):
    sites, n = {x}, N // 3 ** k
    for _ in range(k):
        n *= 3
        sites = {(3 * s + d) % n for s in sites for d in range(-1, 4)}
    start = next(s for s in sites if (s - 1) % N not in sites)
    return [(start + i) % N for i in range(len(sites))]


def selftest():
    N, chi, k, x = 9, 4, 1, 1
    T, dims = build(N, chi, k, x, seed=3, d=2)
    worst = 0.0
    regions = [[0], [3, 4], [2, 3, 4, 5, 6], [0, 1, 7, 8], list(range(1, 8))]
    for A in regions:
        for X in ([f'p{i}' for i in A], [f'p{i}' for i in A] + ['Rlow'], ['Rlow'], ['Rup']):
            a, _ = entropy(T, dims, X)
            b = dense_entropy(T, dims, X)
            worst = max(worst, abs(a - b))
    C = cone(N, k, x)
    fC = f_of(T, dims, C)[0]
    comp = [i for i in range(N) if i not in C]
    fout = f_of(T, dims, comp)[0]
    sR = entropy(T, dims, ['Rlow'])[0]
    print(f'selftest N=9 chi=4: max |S_gram - S_dense| = {worst:.2e}')
    print(f'  G1: f(cone) = {fC:.12f} (expect 1), f(complement of cone) = {fout:.2e} (expect 0), '
          f'S(Rlow) = {sR:.6f} vs log chi = {math.log(chi):.6f}')
    return worst < 1e-9 and abs(fC - 1) < 1e-9 and abs(fout) < 1e-9


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', action='store_true')
    ap.add_argument('--chi', type=int, default=6)
    ap.add_argument('--N', type=int, default=27)
    ap.add_argument('--k', type=int, default=2)
    ap.add_argument('--x', type=int, default=1)
    ap.add_argument('--d', type=int, default=4, help='physical site dimension (pipeline blocks 2 spins: 4)')
    ap.add_argument('--run', action='store_true', help='actually contract (default: plan only)')
    ap.add_argument('--max-gb', type=float, default=20.0)
    ap.add_argument('--m', type=int, nargs='*', default=None)
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    T, dims = build(a.N, a.chi, a.k, a.x, d=a.d)
    C = cone(a.N, a.k, a.x)
    print(f'N={a.N} chi={a.chi} bond=w^({a.k})_{a.x} |cone|={len(C)} sites {C[0]}..{C[-1]}  '
          f'mode={"RUN" if a.run else "PLAN"}')
    rows = []
    for m in (a.m if a.m is not None else range(len(C))):
        A = C[:len(C) - m]
        t0 = time.time()
        f, sR, iA, iAR = f_of(T, dims, A, plan_only=not a.run, max_gb=a.max_gb)
        # BLINDING: these are Haar tensors, i.e. one seed of the C-HAAR control. G0 runs before
        # registration, so the value of f is neither printed nor saved. Only "did it compute".
        f = None if f is None else 'computed (blinded)'
        row = dict(m=m, sites=len(A), D_A=iA['D'], D_AR=iAR['D'], peak_gb=max(iA['peak_gb'], iAR['peak_gb']),
                   flops=iA['flops'] + iAR['flops'], f=f, seconds=round(time.time() - t0, 1))
        rows.append(row)
        print(f"  m={m:2d} |A|={len(A):2d}  D(A)={iA['D']:6d} D(A+Rlow)={iAR['D']:6d}  "
              f"peak {row['peak_gb']:8.2f} GB  flops {row['flops']:.1e}  "
              f"f={'-' if f is None else f}  [{row['seconds']}s]", flush=True)
    json.dump(dict(N=a.N, chi=a.chi, k=a.k, x=a.x, run=a.run, rows=rows),
              open(f'g0_feasibility_N{a.N}_d{a.d}_chi{a.chi}_k{a.k}{"_run" if a.run else "_plan"}.json', 'w'), indent=1)
