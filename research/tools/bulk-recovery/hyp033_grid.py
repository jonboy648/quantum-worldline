"""HYP-033 registered driver (PREREGISTRATION-HYP033.md, REGISTERED 2026-09-22).

Assembles the 27-site periodic state from an exported SIM-061 network (qw_hyp033_export.jl):
layers 1 and 2 (the two transitional layers) close on a 3-site ring with a top tensor = ground state
of the ring Hamiltonian H2 (h ascended through the same two layers). Bond b = top leg of the
layer-2 isometry at x = 1 (17-site cone). R_low is attached to the lower end (the isometry side),
R_up to the upper end (the top-tensor side). Registered observable f(A) = I(R_low:A) / 2 S(R_low),
exact von Neumann entropies through the cut-Gram method validated in g0_feasibility.py (1e-15 vs
brute force). Gates G1-G3 run per network; G4 comes from the Julia export; G5 is chi=8 vs chi=6.

Blinding: f values are written to the JSON output only, never printed, until the grid is complete.

Heavy points (D = 13824): spec(GR^T GL) = spec(L^dag GR^T L) with GL = L L^dag (Cholesky, exact), with
the Gram matrices split into the two Z2 parity blocks of the cut legs whenever the off-diagonal blocks
vanish (densified Z2-covariant tensors are in sector order, so parity is diagonal). Dense eigh fallback
when Cholesky fails. Every entropy records its route and the measured off-block leakage.
"""
import argparse
import json
import math
import os
import socket
import sys
import time
from pathlib import Path

import numpy as np
import scipy.linalg
import scipy.sparse.linalg as spla
import opt_einsum as oe

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g0_feasibility import partition, gram, cone, haar_isometry, dense_entropy  # validated machinery

N_SITES, BOND_K, BOND_X, D_PHYS = 27, 2, 1, 4
M_REGISTERED = [m for m in range(17) if m != 4]   # rule 1: m = 4 declared missing before any result
CHI8_ALIGNED = [0, 2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]  # rule 2: block-aligned points only


# ----------------------------------------------------------------------------- network I/O
def load_network(d):
    d = Path(d)
    arrs = {}
    for ln in open(d / 'meta.txt'):
        nm, nd, *shape = ln.split()
        shape = tuple(int(s) for s in shape)
        arrs[nm] = np.fromfile(d / f'{nm}.bin', dtype=np.complex128).reshape(shape, order='F')
    info = {}
    for ln in open(d / 'info.txt'):
        k, *v = ln.split()
        info[k] = v[0] if len(v) == 1 else v
    return arrs, info


def ring_ground_state(H2):
    """H2[o1,o2,i1,i2] on the 3-site periodic ring: bonds (0,1), (1,2), (2,0). Returns top[a,b,c]."""
    chi = H2.shape[0]
    Hm = H2.reshape(chi * chi, chi * chi)
    herm = float(np.abs(Hm - Hm.conj().T).max())
    I = np.eye(chi)
    H01 = np.kron(Hm, I)
    H12 = np.kron(I, Hm)
    # bond (2,0): H20[(a,b,c),(d,e,f)] = H2[c,a; f,d] * I[b,e]  (site 2 is the LEFT leg of the term)
    H2t = H2.reshape(chi, chi, chi, chi)
    H20 = np.zeros((chi,) * 6, dtype=complex)
    for b in range(chi):
        H20[:, b, :, :, b, :] += np.transpose(H2t, (1, 0, 3, 2))   # [a,c,d,f] = H2[c,a,f,d]
    H20 = H20.reshape(chi ** 3, chi ** 3)
    H = H01 + H12 + H20
    H = (H + H.conj().T) / 2
    w, V = np.linalg.eigh(H)
    top = V[:, 0].reshape(chi, chi, chi)
    return top, dict(E0=float(w[0]), E1=float(w[1]), gap=float(w[1] - w[0]), herm=herm)


def build_state(arrs, top, gauge=None, N=N_SITES, k=BOND_K, x=BOND_X, rewire=0):
    """Same labelling as g0_feasibility.build: 'p{i}' boundary, 'Rlow', 'Rup' references, caps on all
    open indices. Layers 1..L-1 from the export, then `top` on the final 3-site ring. `gauge` (chi x chi
    unitary) is applied to the lower end of bond b and undone on the upper end: same state, G3.
    `rewire` = C-REWIRE (fixed 2026-09-22 before any run): in layer 1 the direct (middle) input of
    isometry w1_j is boundary site 3(j + rewire) + 1 instead of 3j + 1, a cyclic shift by `rewire`
    blocks. Same tensors, same A_m intervals; only the graph changes."""
    L = round(math.log(N, 3))
    T, dims = [], {}

    def add(name, arr, idx):
        T.append((name, arr, idx))
        for i, dd in zip(idx, arr.shape):
            assert dims.setdefault(i, dd) == dd, (name, i, dd, dims[i])

    n = N
    for l in range(1, L):
        u, w = arrs[f'u{l}'], arrs[f'w{l}']
        nb = n // 3
        s = lambda i, l=l, n=n: f's{l-1}_{i % n}'
        t = lambda i, l=l, n=n: f't{l}_{i % n}'
        for j in range(nb):
            add(f'u{l}_{j}', u, [s(3 * j + 2), s(3 * j + 3), t(3 * j + 2), t(3 * j + 3)])
        for j in range(nb):
            up, wj = f's{l}_{j}', w
            if l == k and j == x:
                up = 'Rlow_in'
                if gauge is not None:
                    wj = np.einsum('abct,tu->abcu', w, gauge)
            mid = s(3 * (j + rewire) + 1) if l == 1 else s(3 * j + 1)
            add(f'w{l}_{j}', wj, [t(3 * j), mid, t(3 * j + 2), up])
        n = nb
    assert n == 3 and k == L - 1, (n, k, L)
    tt = top
    if gauge is not None:
        tt = np.moveaxis(np.tensordot(top, gauge.conj(), axes=([x], [0])), -1, x)
    add('top', tt, [f's{L-1}_{j}' for j in range(3)])
    cut = f's{k}_{x}'
    T[:] = [(nm, a, ['Rup_in' if i == cut else i for i in idx]) for nm, a, idx in T]
    dims['Rup_in'] = dims.pop(cut)
    for i in range(N):
        add(f'cap_p{i}', np.eye(D_PHYS if arrs['u1'].shape[0] == D_PHYS else arrs['u1'].shape[0]), [f'p{i}', f's0_{i}'])
    add('cap_Rlow', np.eye(dims['Rlow_in']), ['Rlow', 'Rlow_in'])
    add('cap_Rup', np.eye(dims['Rup_in']), ['Rup', 'Rup_in'])
    return T, dims


def graph_cone(T, k=BOND_K, x=BOND_X):
    """Boundary sites in the causal cone of the lower end of b, read off the actual graph: descend from
    w{k}_{x} through bottom legs (labels 't{l}_*' -> the disentangler of layer l, 's{l-1}_*' -> layer
    below). Equals cone(N, k, x) for the standard wiring; differs under rewire."""
    tens = {nm: idx for nm, _, idx in T}
    owner = {}
    for nm, idx in tens.items():
        for i in idx:
            owner.setdefault(i, []).append(nm)
    frontier, sites = [f'w{k}_{x}'], set()
    seen = set(frontier)
    while frontier:
        nm = frontier.pop()
        layer = int(nm[1:].split('_')[0])
        for i in tens[nm]:
            if i.startswith('s0_'):
                sites.add(int(i[3:]))
            elif i.startswith(f's{layer-1}_') or (nm.startswith('w') and i.startswith(f't{layer}_')):
                # w: down through its disentangled legs (t) and its direct leg (s); u: down through s only
                for o in owner.get(i, []):
                    if o != nm and not o.startswith('cap_') and o not in seen:
                        seen.add(o); frontier.append(o)
    return sorted(sites)


# ----------------------------------------------------------------------------- entropies
def spectrum_dense(GL, GR):
    """Validated G0 route: two Hermitian eigenproblems, rank-truncated. Consumes GL."""
    from scipy.linalg.blas import zgemm
    w, V = scipy.linalg.eigh(GL, overwrite_a=True, check_finite=False)
    keep = w > 1e-13 * w.max()
    B = np.ascontiguousarray(V[:, keep] * np.sqrt(w[keep]))     # D x r, so B^dag GR^T B with B := this
    del V
    tmp = zgemm(1.0, B, GR, trans_a=2, trans_b=1)                 # B^dag GR^T   (r x D), no copies
    M = zgemm(1.0, tmp, B)                                        # r x r
    del tmp, B
    ev = scipy.linalg.eigvalsh((M + M.conj().T) / 2, overwrite_a=True, check_finite=False)
    return ev, 'dense'


def spectrum_chol(GL, GR):
    """GL = L L^dag (Cholesky in place; LinAlgError if GL is not positive definite), then the exact spectrum
    of the Hermitian L^dag GR^T L, which equals spec(GR^T GL). BLAS transpose flags avoid every copy:
    peak memory is about four D x D complex matrices."""
    from scipy.linalg.blas import zgemm
    L = scipy.linalg.cholesky(GL, lower=True, overwrite_a=True, check_finite=False)
    L = np.tril(L)                                                # zero the strict upper part (potrf leaves junk there)
    tmp = zgemm(1.0, L, GR, trans_a=2, trans_b=1)                 # L^dag GR^T
    M = zgemm(1.0, tmp, L)                                        # (L^dag GR^T) L
    del tmp, L
    ev = scipy.linalg.eigvalsh((M + M.conj().T) / 2, overwrite_a=True, check_finite=False)
    return ev, 'chol'


def spectrum(GL, GR, prefer='chol'):
    if prefer == 'chol':
        try:
            return spectrum_chol(GL, GR)
        except np.linalg.LinAlgError:
            pass
    return spectrum_dense(GL, GR)


def z2_split(dims, K):
    """Parity of every product-basis state of the cut legs K (C-order, as gram() reshapes them). Every leg
    of a densified Z2 network is in sector order, parity diag(+1 x n/2, -1 x n/2). Returns index arrays
    (even, odd) or None if a leg has odd dimension."""
    P = np.ones(1)
    for i in K:
        n = dims[i]
        if n % 2:
            return None
        P = np.kron(P, np.r_[np.ones(n // 2), -np.ones(n // 2)])
    return np.flatnonzero(P > 0), np.flatnonzero(P < 0)


def entropy(T, dims, X, method='auto', z2=True, block_tol=1e-10, **_):
    """Exact von Neumann entropy of the open indices X. Returns (S, info). With z2=True the Gram matrices
    are split into the two parity blocks of the cut legs when the off-diagonal blocks vanish (Z2-covariant
    tensors); the check is recorded and a non-covariant network (C-HAAR) falls back to the full matrices."""
    names = {nm for nm, _, _ in T}
    inside, K = partition(T, dims, set(X))
    D = int(np.prod([dims[i] for i in K])) if K else 1
    t0 = time.time()
    GL, _ = gram(T, dims, inside, K)
    GR, _ = gram(T, dims, names - inside, K)
    tc = time.time() - t0
    GL = (GL + GL.conj().T) / 2
    GR = (GR + GR.conj().T) / 2
    info = dict(D=D, cut_bonds=len(K), contract_s=round(tc, 1))
    prefer = 'dense' if method == 'dense' else 'chol'
    t0 = time.time()
    split = z2_split(dims, K) if (z2 and D > 64) else None
    if split is not None:
        e, o = split
        off = max(np.abs(GL[np.ix_(e, o)]).max(), np.abs(GR[np.ix_(e, o)]).max())
        scale = max(np.abs(GL).max(), np.abs(GR).max())
        info['z2_offblock'] = float(off / scale)
        if off > block_tol * scale:
            split = None
    if split is not None:
        evs, tags = [], []
        for idx in (e, o):
            ev, tag = spectrum(np.ascontiguousarray(GL[np.ix_(idx, idx)]), np.ascontiguousarray(GR[np.ix_(idx, idx)]), prefer)
            evs.append(ev); tags.append(tag)
        ev = np.concatenate(evs)
        info['route'] = 'z2-' + '+'.join(tags)
    else:
        ev, tag = spectrum(GL, GR, prefer)
        info['route'] = tag
    del GL, GR
    ev = ev[ev > 1e-14 * ev.max()]
    norm = float(ev.sum())
    info['norm'] = norm
    p = ev / norm
    S = float(-(p * np.log(p)).sum())
    info['eig_s'] = round(time.time() - t0, 1)
    return S, info


def f_of(T, dims, A, cache, **kw):
    sites = [f'p{i}' for i in A]
    if 'R' not in cache:
        cache['R'] = entropy(T, dims, ['Rlow'], **kw)
    sR, iR = cache['R']
    sA, iA = entropy(T, dims, sites, **kw)
    sAR, iAR = entropy(T, dims, sites + ['Rlow'], **kw)
    f = (sR + sA - sAR) / (2 * sR)
    return dict(f=f, S_R=sR, S_A=sA, S_AR=sAR, I=sR + sA - sAR, info_A=iA, info_AR=iAR, norm=iA['norm'])


def cut_side(T, dims, A, unit=False):
    """Cut predictor on the actual network graph: is the lower end of b (the layer-k isometry at x)
    on A's side of the minimal cut separating A from the rest of the boundary? References excluded."""
    import networkx as nx
    G = nx.Graph()
    where = {}
    for nm, _, idx in T:
        for i in idx:
            where.setdefault(i, []).append(nm)
    for i, names in where.items():
        if len(names) == 2:
            a, b = names
            w = 1.0 if unit else math.log(dims[i])
            G.add_edge(a, b, capacity=G[a][b]['capacity'] + w if G.has_edge(a, b) else w)
    Aset = {f'p{i}' for i in A}
    for nm, _, _ in T:
        if nm.startswith('cap_p'):
            G.add_edge('SRC' if nm[4:] in Aset else 'SNK', nm, capacity=1e9)
    val, (S, _) = nx.minimum_cut(G, 'SRC', 'SNK')
    return bool(f'w{BOND_K}_{BOND_X}' in S), float(val)


# ----------------------------------------------------------------------------- gates
def regions(C, edge, m):
    return C[m:] if edge == 'left' else C[:len(C) - m]


def run_gates(arrs, top, out, tol=dict(G1=1e-10, G2=1e-8, G3=1e-8), build=None, **kw):
    """G1 structural one/zero, G2 purity sum through independent cuts, G3 gauge invariance.
    Values of f on registered points are NOT printed; only residuals are."""
    build = build or {}
    T, dims = build_state(arrs, top, **build)
    C = graph_cone(T)                      # actual cone of the built graph (== cone(27,2,1) unless rewired)
    comp = [i for i in range(N_SITES) if i not in C]
    cache = {}
    g = dict(graph_cone=C, standard_cone=cone(N_SITES, BOND_K, BOND_X))
    t0 = time.time()
    rC = f_of(T, dims, C, cache, **kw)
    rO = f_of(T, dims, comp, cache, **kw)
    g['G1'] = dict(f_cone_minus_1=rC['f'] - 1, f_outside=rO['f'], S_R=rC['S_R'], log_chi=math.log(dims['Rlow']),
                   norm_cone=rC['norm'], norm_expected=dims['Rlow'],
                   passed=bool(abs(rC['f'] - 1) < tol['G1'] and abs(rO['f']) < tol['G1']
                               and abs(rC['norm'] - dims['Rlow']) < 1e-8 and abs(rC['S_R'] - math.log(dims['Rlow'])) < 1e-8))
    # G2: S(comp+Rup) == S(A+Rlow) and S(comp+Rup+Rlow) == S(A) computed through THEIR OWN cuts
    g2 = []
    for edge, m in (('left', 0), ('left', 8), ('right', 8), ('right', 12)):
        A = regions(C, edge, m)
        cA = [f'p{i}' for i in range(N_SITES) if i not in A]
        sA, _ = entropy(T, dims, [f'p{i}' for i in A], **kw)
        sAR, _ = entropy(T, dims, [f'p{i}' for i in A] + ['Rlow'], **kw)
        s1, _ = entropy(T, dims, cA + ['Rup'], **kw)
        s2, _ = entropy(T, dims, cA + ['Rup', 'Rlow'], **kw)
        g2.append(dict(edge=edge, m=m, d1=s1 - sAR, d2=s2 - sA))
    g['G2'] = dict(points=g2, worst=max(max(abs(p['d1']), abs(p['d2'])) for p in g2))
    g['G2']['passed'] = bool(g['G2']['worst'] < tol['G2'])
    # G3: Haar unitary on the lower end of b, undone on the upper end
    rng = np.random.default_rng(20260922)
    U = haar_isometry(rng, dims['Rlow'], dims['Rlow'])
    Tg, dg = build_state(arrs, top, gauge=U, **build)
    cg = {}
    g3 = []
    for edge, m in (('left', 0), ('left', 2), ('right', 2), ('left', 8), ('right', 8)):
        A = regions(C, edge, m)
        a = f_of(T, dims, A, cache, **kw)
        b = f_of(Tg, dg, A, cg, **kw)
        g3.append(dict(edge=edge, m=m, df=b['f'] - a['f'], dS_R=b['S_R'] - a['S_R']))
    g['G3'] = dict(points=g3, worst=max(abs(p['df']) for p in g3))
    g['G3']['passed'] = bool(g['G3']['worst'] < tol['G3'])
    g['seconds'] = round(time.time() - t0, 1)
    g['all_passed'] = bool(g['G1']['passed'] and g['G2']['passed'] and g['G3']['passed'])
    out['gates'] = g
    print(f"  gates: G1 |f(cone)-1|={abs(g['G1']['f_cone_minus_1']):.1e} f(out)={abs(g['G1']['f_outside']):.1e} "
          f"S_R={g['G1']['S_R']:.4f}/{g['G1']['log_chi']:.4f} norm={g['G1']['norm_cone']:.12f} | "
          f"G2 worst {g['G2']['worst']:.1e} | G3 worst {g['G3']['worst']:.1e} | "
          f"{'PASS' if g['all_passed'] else 'FAIL'} [{g['seconds']}s]", flush=True)
    return g['all_passed']


# ----------------------------------------------------------------------------- grid
def run_grid(arrs, top, out, edge, mlist, outfile, build=None, **kw):
    T, dims = build_state(arrs, top, **(build or {}))
    C = cone(N_SITES, BOND_K, BOND_X)      # the REGISTERED interval family, also under rewire
    out['graph_cone'] = graph_cone(T)
    cache = {}
    done = {(p['edge'], p['m']) for p in out.setdefault('points', [])}
    for m in mlist:
        if (edge, m) in done:
            continue
        A = regions(C, edge, m)
        t0 = time.time()
        r = f_of(T, dims, A, cache, **kw)
        inside_w, cutval = cut_side(T, dims, A)
        inside_u, cutval_u = cut_side(T, dims, A, unit=True)
        p = dict(edge=edge, m=m, sites=len(A), first=A[0], last=A[-1], f=r['f'], I=r['I'], S_R=r['S_R'],
                 S_A=r['S_A'], S_AR=r['S_AR'], norm=r['norm'], D_A=r['info_A']['D'], D_AR=r['info_AR']['D'],
                 route_A=r['info_A'].get('route'), z2_offblock_A=r['info_A'].get('z2_offblock'),
                 eig_s_A=r['info_A'].get('eig_s'), contract_s_A=r['info_A'].get('contract_s'),
                 cut_weighted_b_inside=inside_w, cut_weighted_value=cutval,
                 cut_unit_b_inside=inside_u, cut_unit_value=cutval_u,
                 seconds=round(time.time() - t0, 1), when=time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()))
        out['points'].append(p)
        json.dump(out, open(outfile, 'w'), indent=1)
        # BLINDED: f is not printed
        print(f"  {edge:5s} m={m:2d} |A|={len(A):2d} D={p['D_A']:6d} route={p['route_A']} "
              f"norm={p['norm']:.10f} cutW={'in' if inside_w else 'out'} cutU={'in' if inside_u else 'out'} "
              f"[{p['seconds']}s]", flush=True)


# ----------------------------------------------------------------------------- selftests
def selftest_haar():
    """N=9, chi=4, d=2 Haar layers + random top on the 3-ring, vs brute force; both spectral routes."""
    from g0_feasibility import build as g0build
    rng = np.random.default_rng(5)
    T0, _ = g0build(9, 4, 1, 1, seed=7, d=2)
    arrs = {'u1': next(a for nm, a, _ in T0 if nm == 'u1_0'), 'w1': next(a for nm, a, _ in T0 if nm == 'w1_0')}
    top = rng.normal(size=(4, 4, 4)) + 1j * rng.normal(size=(4, 4, 4))
    top /= np.linalg.norm(top)
    T, dims = build_state(arrs, top, N=9, k=1, x=1)
    C = cone(9, 1, 1)
    worst = {'dense': 0.0, 'chol': 0.0}
    for A in ([0], [3, 4], C, [i for i in range(9) if i not in C], list(range(1, 8))):
        for X in ([f'p{i}' for i in A], [f'p{i}' for i in A] + ['Rlow'], ['Rlow'], ['Rup']):
            b = dense_entropy(T, dims, X)
            for route in worst:
                a, info = entropy(T, dims, X, method=route)
                worst[route] = max(worst[route], abs(a - b))
    cache = {}
    fC = f_of(T, dims, C, cache)['f']
    fO = f_of(T, dims, [i for i in range(9) if i not in C], cache)['f']
    print(f'selftest haar N=9: max|S-S_dense| dense={worst["dense"]:.1e} chol={worst["chol"]:.1e}  '
          f'f(cone)={fC:.12f} f(out)={fO:.1e}')
    return worst['dense'] < 1e-9 and worst['chol'] < 1e-9 and abs(fC - 1) < 1e-9 and abs(fO) < 1e-9


def selftest_export(d):
    """N=9 from an exported network: layer 1 + ring ground state of H2 as top (dims match), vs dense.
    Checks the TensorKit -> numpy conventions: norm 1, isometry direction, f(cone) = 1."""
    arrs, info = load_network(d)
    top, tinfo = ring_ground_state(arrs['H2'])
    T, dims = build_state(arrs, top, N=9, k=1, x=1)
    C = cone(9, 1, 1)
    worst = 0.0
    for A in ([0], [3, 4], C, [i for i in range(9) if i not in C]):
        for X in ([f'p{i}' for i in A], [f'p{i}' for i in A] + ['Rlow'], ['Rlow']):
            a, ia = entropy(T, dims, X, method='chol')
            b = dense_entropy(T, dims, X)
            worst = max(worst, abs(a - b))
    cache = {}
    rC = f_of(T, dims, C, cache)
    rO = f_of(T, dims, [i for i in range(9) if i not in C], cache)
    print(f'selftest export {d}: max|S-S_dense|={worst:.1e} norm={rC["norm"]:.12f} f(cone)={rC["f"]:.12f} '
          f'f(out)={rO["f"]:.1e} S_R={rC["S_R"]:.6f} ring: E0={tinfo["E0"]:.6f} gap={tinfo["gap"]:.4f} herm={tinfo["herm"]:.1e}')
    # <Phi|Phi> = dim(R_low): the reference is the unnormalized identity on the cut bond (the Gram
    # route normalizes the spectrum); S_R must equal log chi when the lower part is isometric
    chi = dims['Rlow']
    return worst < 1e-9 and abs(rC['norm'] - chi) < 1e-10 and abs(rC['f'] - 1) < 1e-9 and abs(rO['f']) < 1e-9


def bench(chi, m=1):
    """Heavy Haar point at N=27: chol route vs the validated dense route. Prints only the difference."""
    from g0_feasibility import build as g0build
    T0, _ = g0build(27, chi, 2, 1, seed=1, d=4)
    arrs = {}
    for l in (1, 2):
        arrs[f'u{l}'] = next(a for nm, a, _ in T0 if nm == f'u{l}_0')
        arrs[f'w{l}'] = next(a for nm, a, _ in T0 if nm == f'w{l}_0')
    rng = np.random.default_rng(1)
    top = rng.normal(size=(chi,) * 3) + 1j * rng.normal(size=(chi,) * 3)
    top /= np.linalg.norm(top)
    T, dims = build_state(arrs, top)
    C = cone(N_SITES, BOND_K, BOND_X)
    A = regions(C, 'right', m)
    X = [f'p{i}' for i in A]
    t0 = time.time(); a, ia = entropy(T, dims, X, method='chol'); ta = time.time() - t0
    print(f'bench chi={chi} m={m} D={ia["D"]}: chol {ta:.0f}s route={ia.get("route")} '
          f'contract={ia["contract_s"]}s eig={ia["eig_s"]}s', flush=True)
    t0 = time.time(); b, ib = entropy(T, dims, X, method='dense'); tb = time.time() - t0
    print(f'   dense {tb:.0f}s   |S_chol - S_dense| = {abs(a - b):.2e}', flush=True)


# ----------------------------------------------------------------------------- main
if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--selftest', choices=['haar', 'export'])
    ap.add_argument('--bench', type=int, default=0, help='heavy Haar point at this chi (timing only)')
    ap.add_argument('--network', help='exported network directory')
    ap.add_argument('--edge', choices=['left', 'right', 'both'], default='both')
    ap.add_argument('--m', type=int, nargs='*', default=None, help='override the registered m list')
    ap.add_argument('--chi8', action='store_true', help='rule 2: aligned points only')
    ap.add_argument('--gates', action='store_true', help='run G1-G3 before the grid')
    ap.add_argument('--out', help='output JSON (default: <network>/hyp033_<edge>.json)')
    ap.add_argument('--no-z2', action='store_true', help='never use the parity blocks')
    ap.add_argument('--pod', default=os.environ.get('RUNPOD_POD_ID', ''))
    ap.add_argument('--rewire', type=int, default=0, help='C-REWIRE: shift of layer-1 direct inputs, in blocks')
    a = ap.parse_args()
    kw = dict(z2=not a.no_z2)
    BUILD = dict(rewire=a.rewire)
    if a.selftest == 'haar':
        sys.exit(0 if selftest_haar() else 1)
    if a.selftest == 'export':
        sys.exit(0 if selftest_export(a.network) else 1)
    if a.bench:
        bench(a.bench); sys.exit(0)
    arrs, info = load_network(a.network)
    if 'top' in arrs:                       # C-HAAR: explicit random top, no Hamiltonian
        top, tinfo = arrs['top'] / np.linalg.norm(arrs['top']), dict(E0=float('nan'), E1=float('nan'), gap=float('nan'), herm=0.0, source='top.bin')
    else:
        top, tinfo = ring_ground_state(arrs['H2'])
        tinfo['source'] = 'ring ground state of H2'
    outfile = a.out or str(Path(a.network) / f'hyp033_{a.edge}{"_rewire%d" % a.rewire if a.rewire else ""}.json')
    out = json.load(open(outfile)) if os.path.exists(outfile) else {}
    out.update(network=str(a.network), info=info, top=tinfo, N=N_SITES, k=BOND_K, x=BOND_X, rewire=a.rewire,
               host=socket.gethostname(), pod=a.pod, started=out.get('started') or time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime()),
               z2=not a.no_z2)
    print(f"network {a.network}: chi={info.get('chi')} h={info.get('hfield')} seed={info.get('seed')} "
          f"E_inf={info.get('E_inf')} basin_clean={info.get('basin_clean')} | ring E0/3={tinfo['E0']/3:.6f} "
          f"gap={tinfo['gap']:.4f} herm={tinfo['herm']:.1e}", flush=True)
    json.dump(out, open(outfile, 'w'), indent=1)
    if a.gates:
        ok = run_gates(arrs, top, out, build=BUILD, **kw)
        json.dump(out, open(outfile, 'w'), indent=1)
        if not ok:
            print('  GATES FAILED: grid not started for this network', flush=True)
            sys.exit(2)
    mlist = a.m if a.m is not None else (CHI8_ALIGNED if a.chi8 else M_REGISTERED)
    t0 = time.time()
    for edge in (['left', 'right'] if a.edge == 'both' else [a.edge]):
        run_grid(arrs, top, out, edge, mlist, outfile, build=BUILD, **kw)
    out['finished'] = time.strftime('%Y-%m-%dT%H:%M:%SZ', time.gmtime())
    out['grid_seconds'] = round(time.time() - t0, 1)
    json.dump(out, open(outfile, 'w'), indent=1)
    print(f'  done: {outfile} [{out["grid_seconds"]}s]', flush=True)
