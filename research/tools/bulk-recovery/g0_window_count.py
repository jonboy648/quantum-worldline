"""Graph-only count for HYP-033 DRAFT: how wide is the region family where the cone predictor and
the minimal-cut predictor disagree? No tensors, no physics numbers. Unit capacity per bond.

Ternary MERA, periodic, N boundary sites, layers N -> N/3 -> ... -> 1.
Layer l on n sites: disentangler u_j on sites (3j+2, 3j+3 mod n); isometry w_j on (3j, 3j+1, 3j+2).
Bulk bond b = output leg of w^{(k)}_x. It is cut; a reference R = R_low (x) R_up is attached to the
two open ends, one unit each. Cut predictor (random-tensor, large chi): S(X) = min cut of X, and
f(A) = [S(R) + S(A) - S(RA)] / (2 S(R)).  Cone predictor: f(A) = 1 iff A contains C(b).
"""
import sys
import networkx as nx

INF = 10**6


def build(N, k, x):
    G = nx.MultiGraph()
    n, l = N, 1
    below = {i: ('site', i) for i in range(N)}          # node carrying the leg below layer l
    cone_top = None
    while n >= 3:
        nb = n // 3
        up = {}
        for i in range(n):
            if i % 3 == 2:
                G.add_edge(below[i], ('u', l, i // 3))
            elif i % 3 == 0:
                G.add_edge(below[i], ('u', l, (i // 3 - 1) % nb))
            else:
                G.add_edge(below[i], ('w', l, i // 3))
        for j in range(nb):
            G.add_edge(('u', l, j), ('w', l, j))             # upper-left leg -> w_j slot 2
            G.add_edge(('u', l, j), ('w', l, (j + 1) % nb))  # upper-right leg -> w_{j+1} slot 0
            up[j] = ('w', l, j)
        if l == k:
            # cut the output bond of w^{(k)}_x: lower end gets R_low, upper end gets R_up
            G.add_edge(('w', l, x), 'R_low')
            up[x] = 'R_up'
        below, n, l = up, nb, l + 1
    return G


def cone(N, k, x):
    """Boundary sites below the output leg of w^{(k)}_x (downward light cone)."""
    sites = {x}
    n = N // 3 ** k
    for _ in range(k):
        n *= 3
        new = set()
        for s in sites:
            for d in range(-1, 4):
                new.add((3 * s + d) % n)
        sites = new
    return sites


def S(G, X, terminals):
    """Min cut separating terminal set X from the other terminals."""
    X = set(X)
    rest = terminals - X
    if not X or not rest:
        return 0
    D = nx.DiGraph()
    for a, b in G.edges():
        for p, q in ((a, b), (b, a)):
            D.add_edge(p, q, capacity=D[p][q]['capacity'] + 1 if D.has_edge(p, q) else 1)
    for t in X:
        D.add_edge('SRC', t, capacity=INF)
    for t in rest:
        D.add_edge(t, 'SNK', capacity=INF)
    return nx.maximum_flow_value(D, 'SRC', 'SNK')


def f_cut(G, A, N):
    term = {('site', i) for i in range(N)} | {'R_low', 'R_up'}
    A = {('site', i) for i in A}
    R = {'R_low', 'R_up'}
    sR = S(G, R, term)
    return (sR + S(G, A, term) - S(G, A | R, term)) / (2 * sR), sR


def run(N, k, x):
    G = build(N, k, x)
    C = cone(N, k, x)
    # order the cone as a contiguous interval
    start = next(s for s in C if (s - 1) % N not in C) if len(C) < N else 0
    order = [(start + i) % N for i in range(len(C))]
    print(f"\nN={N} bulk bond: output of w^({k})_{x}   |C(b)|={len(C)} sites {order[0]}..{order[-1]}")
    for side in ('right', 'left'):
        row = []
        for m in range(len(order)):
            A = order[:len(order) - m] if side == 'right' else order[m:]
            f, sR = f_cut(G, A, N)
            row.append(f)
        window = [m for m, f in enumerate(row) if m >= 1 and abs(f - 1) < 1e-9]
        print(f"  drop from {side:5s}: cut-predictor f(A_m), m=0..: " + ' '.join(f'{f:.2f}' for f in row))
        print(f"      cone predictor: f=1 at m=0 only. Disagreement window (cut says f=1, m>=1): "
              f"{window if window else 'EMPTY'}   S(R)={sR}")
    # all intervals: cone says not fully recoverable (A misses a cone site) but cut says f=1
    hits = []
    for a in range(N):
        for L in range(1, N):
            A = [(a + i) % N for i in range(L)]
            if C <= set(A):
                continue
            f, _ = f_cut(G, A, N)
            if abs(f - 1) < 1e-9:
                hits.append((a, L))
    print(f"  all {N*(N-1)} intervals: cut says f=1 while A misses part of the cone: {len(hits)} intervals"
          + (f", shortest L={min(L for _, L in hits)}, e.g. {hits[:4]}" if hits else ""))


if __name__ == '__main__':
    N = int(sys.argv[1]) if len(sys.argv) > 1 else 27
    layers = round(__import__('math').log(N, 3))
    for k in range(1, layers):
        for x in range(min(3, N // 3 ** k)):
            run(N, k, x)
