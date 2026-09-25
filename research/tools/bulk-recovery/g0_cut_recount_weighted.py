"""DA point 4: cut predictor for the REGISTERED observable f=I(R_low:A)/(2S(R_low)), unit vs log-dim capacities.
Leg capacities: physical/site legs log d=log4, layer-1 internal legs log4, layer-1 outputs log chi, layer-2 legs log chi, R legs log chi."""
import sys, math, networkx as nx
sys.path.insert(0, '.')
from g0_window_count import build, cone
INF = 10**9
def cap_of(a, b, w):
    def lay(n):
        return n[1] if isinstance(n, tuple) and n[0] in ('u', 'w') else None
    la, lb = lay(a), lay(b)
    if 'site' in (a[0] if isinstance(a, tuple) else '', b[0] if isinstance(b, tuple) else ''): return w['d']
    if 'R_low' in (a, b) or 'R_up' in (a, b): return w['chi']
    if la == 1 and lb == 1: return w['d']          # u1 -> w1 internal
    return w['chi']                                 # w1 output and everything above
def S(G, X, term, w):
    X = set(X); rest = term - X
    if not X or not rest: return 0
    D = nx.DiGraph()
    for a, b in G.edges():
        c = cap_of(a, b, w)
        for p, q in ((a, b), (b, a)):
            D.add_edge(p, q, capacity=(D[p][q]['capacity'] if D.has_edge(p, q) else 0) + c)
    for t in X: D.add_edge('SRC', t, capacity=INF)
    for t in rest: D.add_edge(t, 'SNK', capacity=INF)
    return nx.maximum_flow_value(D, 'SRC', 'SNK')
N, k, x = 27, 2, 1
G = build(N, k, x); C = cone(N, k, x)
start = next(s for s in C if (s - 1) % N not in C); order = [(start + i) % N for i in range(len(C))]
term = {('site', i) for i in range(N)} | {'R_low', 'R_up'}
if __name__ == '__main__':
  for name, w in (('unit', dict(d=1, chi=1)), ('log-dim chi6 d4', dict(d=math.log(4), chi=math.log(6))), ('log-dim chi8 d4', dict(d=math.log(4), chi=math.log(8)))):
      sR = S(G, {'R_low'}, term, w)
      for side in ('left', 'right'):
          row = []
          for m in range(len(order)):
              A = {('site', i) for i in (order[m:] if side == 'left' else order[:len(order) - m])}
              row.append((sR + S(G, A, term, w) - S(G, A | {'R_low'}, term, w)) / (2 * sR))
          mh = next((m for m, f in enumerate(row) if f < 0.5 - 1e-9), None)
          print(f'{name:16s} {side:5s} f_cut(m)= ' + ' '.join(f'{f:.2f}' for f in row) + f'   first m with f<1/2: {mh}')
