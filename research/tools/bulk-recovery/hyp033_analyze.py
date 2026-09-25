#!/usr/bin/env python3
"""hyp033_analyze.py -- HYP-033 analysis under the v3 amendment (PREREGISTRATION-HYP033.md).

Written 2026-09-23, BEFORE any registered f value was printed. Tested only on unregistered networks
(haar_test/). Default mode is BLINDED: it reports completeness, gates G1-G4 and routes, and refuses to
print anything derived from f until every planned network is finished (or cap-truncated) and
--unblind is given.

Registered definitions implemented here (prereg + v3):
  crossing(edge, L)  smallest m with f(A_m) < L, linearly interpolated between the neighbouring grid
                     points (m = 4 is declared missing at chi 6; interpolation runs across it)
  m_L, m_R           crossing at L = 1/2 per edge; m_half = mean; gap g = 17 - (m_L + m_R)
                     (m_half is reported but labelled "pinned by complementarity, not discriminating")
  m_0.9              crossing at L = 0.9 per edge (v3 primary cut statistic)
  w                  crossing(0.1) - crossing(0.9)
  cone-like          m_half <= 2
  cut-like (first)   m_0.9 >= 6 on both edges AND seed-mean m_0.9 >= C-HAAR seed-mean m_0.9 + 3 (chi 6)
  smooth             w > 6 AND not cut-like
  G5                 m_half on the chi-8 aligned points vs m_half on the SAME aligned subset at chi 6,
                     within 2 sites

Interpretations the registration left open, FIXED HERE BEFORE UNBLINDING (2026-09-23):
  I1  Verdicts are made on SEED MEANS per group; per-network values are printed alongside.
      "m_0.9 >= 6 on both edges" = seed-mean m_0.9 per edge >= 6; the +3 test compares the
      two-edge average of seed means.
  I2  w for the smooth test is the two-edge average of seed means (per-edge values printed).
  I3  A network enters the statistics only if G1-G3 passed, ring gap >= 1e-6 (pre-run spec 1),
      and, for optimized networks, basin_clean is true (G4 criterion; select by spectrum).
      G4 per group: >= 6 of 8 seeds clean.
  I4  An edge whose f never drops below L gets crossing = None ("> 16") and fails any ">= / <="
      test that needs a number, except that a missing 0.9 crossing counts as >= 6.
  I5  Outcome mapping: cone -> 1; primary cut-like and C-HAAR not reaching m_0.9 >= 6 on both edges
      -> 2 (Level 3 after v3); primary AND C-HAAR both m_0.9 >= 6 on both edges -> 3 ("graph
      property"); smooth -> 4; anything else -> "no registered pattern".
  I6  w is ambiguous in the registration ("m at f < 0.1 minus m at f < 0.9"). The devil's-advocate check
      used GRID points (first grid m below the level; Haar chi3 seed9999 -> w = 9); v3 defines m_0.9 as
      interpolated. Primary w = INTERPOLATED (consistent with v3); w_grid is printed alongside and the
      report flags it if the smooth verdict differs between the two.
  I7  G4's clean-basin criterion (SIM-061: spectrum matches the critical Ising CFT) is undefined for the
      GAPPED control (h = 1.5 has no CFT spectrum; all 8 report basin_clean=false). Found in the blinded
      report 2026-09-23 before any f was printed. G4 therefore applies to h = 1 networks only; C-GAPPED
      networks enter if G1-G3 pass and the ring gap >= 1e-6. APPROVED by Jon 2026-09-24 before unblinding.
  T1  DECLARED TRUNCATION (Jon 2026-09-24, before unblinding): all 4 chi-8 networks were OOM-killed
      (rc=137) ~3 min into their gates on the 62 GB host; no chi-8 point exists. chi 8 was last in the
      registered cap-truncation order. They are removed from PLANNED; G5 is reported NOT EVALUABLE.
"""
import argparse
import json
import math
import sys
from pathlib import Path

N_CONE = 17
CHI8_ALIGNED = [0, 2, 6, 8, 9, 10, 11, 12, 13, 14, 15, 16]
PLANNED = ([f'chi6_h1.00_seed{s}' for s in range(1, 9)] + [f'haar_chi6_seed{s}' for s in range(1, 9)]
           + [f'chi6_h1.50_seed{s}' for s in range(1, 9)])   # T1: chi8 seeds 1-4 truncated (OOM)
GROUPS = {'primary': 'chi6_h1.00', 'C-HAAR': 'haar_chi6', 'C-GAPPED': 'chi6_h1.50', 'chi8': 'chi8_h1.00'}


def crossing(curve, level):
    """curve: sorted [(m, f)]. Smallest m with f < level, linearly interpolated from the previous point."""
    prev = None
    for m, f in curve:
        if f < level:
            if prev is None:
                return float(m)
            (m0, f0) = prev
            return m0 + (f0 - level) / (f0 - f) * (m - m0)
        prev = (m, f)
    return None


def curves(d, only=None):
    out = {}
    for edge in ('left', 'right'):
        pts = sorted((p['m'], p['f']) for p in d.get('points', []) if p['edge'] == edge
                     and (only is None or p['m'] in only))
        out[edge] = pts
    return out


def grid_crossing(curve, level):
    return next((float(m) for m, f in curve if f < level), None)


def stats(d, only=None):
    c = curves(d, only)
    s = {}
    for edge in ('left', 'right'):
        s[edge] = {L: crossing(c[edge], L) for L in (0.9, 0.5, 0.1)}
    mL, mR = s['left'][0.5], s['right'][0.5]
    r = dict(m_L=mL, m_R=mR, m09_L=s['left'][0.9], m09_R=s['right'][0.9])
    r['m_half'] = None if None in (mL, mR) else (mL + mR) / 2
    r['gap'] = None if None in (mL, mR) else N_CONE - (mL + mR)
    for e, k in (('left', 'w_L'), ('right', 'w_R')):
        a, b = s[e][0.1], s[e][0.9]
        r[k] = None if None in (a, b) else a - b
        a, b = grid_crossing(c[e], 0.1), grid_crossing(c[e], 0.9)
        r[k + 'g'] = None if None in (a, b) else a - b
    return r


def gates(d):
    g = d.get('gates', {})
    ok = all(g.get(k, {}).get('passed') for k in ('G1', 'G2', 'G3'))
    info = d.get('info', {})
    gap = d.get('top', {}).get('gap', float('nan'))
    ring_ok = math.isnan(gap) or gap >= 1e-6            # C-HAAR has no ring Hamiltonian (nan)
    basin = str(info.get('basin_clean', 'n/a'))
    h = float(info.get('hfield', 'nan'))
    gapped = not math.isnan(h) and abs(h - 1.0) > 1e-9
    basin_ok = basin in ('n/a', 'true', 'True', '1') or gapped          # I7
    return dict(G1=g.get('G1', {}).get('passed'), G2=g.get('G2', {}).get('passed'),
                G3=g.get('G3', {}).get('passed'), G3_worst=g.get('G3', {}).get('worst'),
                basin=basin, ring_gap=gap, usable=bool(ok and ring_ok and basin_ok),
                finished='finished' in d, npts=len(d.get('points', [])),
                routes=sorted({str(p.get('route_A')) for p in d.get('points', [])}))


def mean(xs):
    xs = [x for x in xs if x is not None]
    return sum(xs) / len(xs) if xs else None


def fmt(x, n=2):
    return '  >16' if x is None else f'{x:5.{n}f}'


def cen(x):
    """I4: a crossing that never happens is censored at 17 (one past the grid) for group means."""
    return 17.0 if x is None else x


def load(root):
    nets = {}
    for name in PLANNED:
        f = Path(root) / name / 'hyp033_both.json'
        nets[name] = json.load(open(f)) if f.exists() else None
    return nets


def report_blinded(nets):
    print('BLINDED REPORT (no f-derived number is printed)')
    print(f'{"network":20s} {"done":5s} {"pts":>4s} G1    G2    G3    {"basin":6s} {"ring_gap":>9s} usable  routes')
    for name, d in nets.items():
        if d is None:
            print(f'{name:20s} MISSING'); continue
        g = gates(d)
        print(f'{name:20s} {str(g["finished"]):5s} {g["npts"]:4d} {str(g["G1"]):5s} {str(g["G2"]):5s} '
              f'{str(g["G3"]):5s} {g["basin"]:6s} {g["ring_gap"]:9.2e} {str(g["usable"]):6s}  {",".join(g["routes"])}')
    for grp, pre in GROUPS.items():
        members = [n for n in nets if n.startswith(pre)]
        if grp in ('primary', 'chi8'):
            clean = sum(1 for n in members if nets[n] and gates(nets[n])['basin'] in ('true', 'True', '1'))
            verdict_g4 = ("PASS" if clean >= 6 else "FAIL") if grp == 'primary' else 'count only (no registered threshold)'
            print(f'G4 {grp}: {clean}/{len(members)} clean -> {verdict_g4}')
    print('G4 C-GAPPED: not applicable (I7: no CFT spectrum at h = 1.5)')
    done = sum(1 for d in nets.values() if d and 'finished' in d)
    print(f'complete: {done}/{len(nets)} networks finished')
    return done == len(nets)


def group_stats(nets, pre, only=None):
    rows = {n: stats(d, only) for n, d in nets.items() if n.startswith(pre) and d and gates(d)['usable']
            and 'finished' in d}
    agg = {k: mean([cen(r[k]) for r in rows.values()]) for k in ('m_L', 'm_R', 'm09_L', 'm09_R', 'w_L', 'w_R', 'w_Lg', 'w_Rg')}
    agg['m_half'] = mean([r['m_half'] for r in rows.values()])
    agg['m09'] = None if None in (agg['m09_L'], agg['m09_R']) else (agg['m09_L'] + agg['m09_R']) / 2
    agg['w'] = None if None in (agg['w_L'], agg['w_R']) else (agg['w_L'] + agg['w_R']) / 2
    agg['wg'] = None if None in (agg['w_Lg'], agg['w_Rg']) else (agg['w_Lg'] + agg['w_Rg']) / 2
    agg['n'] = len(rows)
    return rows, agg


def verdict(a, haar):
    if a['n'] == 0:
        return 'NO USABLE NETWORKS'
    both6 = a['m09_L'] >= 6 and a['m09_R'] >= 6
    if both6 and haar and haar['n'] and a['m09'] >= haar['m09'] + 3:
        return 'CUT-LIKE'
    if a['m_half'] is not None and a['m_half'] <= 2:
        return 'CONE-LIKE'
    if a['w'] is not None and a['w'] > 6:
        return 'SMOOTH'
    return 'NO REGISTERED PATTERN'


def report_unblinded(nets):
    print('\nUNBLINDED REPORT (v3)')
    aggs = {}
    for grp, pre in GROUPS.items():
        if grp == 'chi8':
            continue
        rows, a = group_stats(nets, pre)
        aggs[grp] = a
        print(f'\n[{grp}] usable networks: {a["n"]}')
        print(f'  {"network":20s}   m_L   m_R  m_half   gap  m09_L m09_R   w_L   w_R')
        for n, r in rows.items():
            print(f'  {n:20s} {fmt(r["m_L"])} {fmt(r["m_R"])} {fmt(r["m_half"])} {fmt(r["gap"])} '
                  f'{fmt(r["m09_L"])} {fmt(r["m09_R"])} {fmt(r["w_L"])} {fmt(r["w_R"])}')
        print(f'  seed mean            {fmt(a["m_L"])} {fmt(a["m_R"])} {fmt(a["m_half"])}       '
              f'{fmt(a["m09_L"])} {fmt(a["m09_R"])} {fmt(a["w_L"])} {fmt(a["w_R"])}   (m_half pinned by complementarity, not discriminating)')
    haar = aggs.get('C-HAAR')
    for grp in ('primary', 'C-GAPPED', 'C-HAAR'):
        a = aggs[grp]
        v = verdict(a, haar if grp != "C-HAAR" else None)
        vg = verdict(dict(a, w=a['wg']), haar if grp != "C-HAAR" else None)
        print(f'verdict {grp}: {v}   (w interp {fmt(a["w"])}, w grid {fmt(a["wg"])})'
              + ('' if v == vg else f'   ** I6 FLAG: grid-point w gives {vg} **'))
    # G5: chi 8 vs chi 6 on the same aligned subset
    _, a8 = group_stats(nets, GROUPS['chi8'], CHI8_ALIGNED)
    _, a6 = group_stats(nets, GROUPS['primary'], CHI8_ALIGNED)
    if a8['n'] and a6['n'] and None not in (a8['m_half'], a6['m_half']):
        d = abs(a8['m_half'] - a6['m_half'])
        print(f'G5: m_half aligned chi8 {a8["m_half"]:.2f} (n={a8["n"]}) vs chi6 {a6["m_half"]:.2f} (n={a6["n"]}): '
              f'|diff| {d:.2f} -> {"PASS" if d <= 2 else "UNCONVERGED"}')
    else:
        print('G5: not evaluable (missing chi8 or chi6 aligned data)')
    # I5 outcome mapping
    p, h = aggs['primary'], haar
    vp = verdict(p, h)
    haar_both6 = h['n'] and h['m09_L'] >= 6 and h['m09_R'] >= 6
    prim_both6 = p['n'] and p['m09_L'] >= 6 and p['m09_R'] >= 6
    if vp == 'CONE-LIKE':
        oc = '1 (cone; Level 3 negative)'
    elif vp == 'CUT-LIKE' and not haar_both6:
        oc = '2 (cut in optimized, not in C-HAAR; Level 3 after v3)'
    elif prim_both6 and haar_both6:
        oc = '3 (cut-like onset in both; graph property, Level 2)'
    elif vp == 'SMOOTH':
        oc = '4 (smooth; Level 2, or Level 3 negative if C-HAAR differs)'
    else:
        oc = 'no registered pattern'
    print(f'OUTCOME (I5): {oc}')


def selftest():
    """Known answer: the unregistered Haar network (chi 3, seed 9999) of the devil's-advocate check
    gave m_half = 8.50 on both edges and w = 9 (AMENDMENT-V3-PROPOSAL-HYP033.md)."""
    assert crossing([(0, 1.0), (1, 0.8)], 0.9) == 0.5
    assert crossing([(3, 1.0), (5, 0.0)], 0.5) == 4.0            # interpolation across the missing m = 4
    assert crossing([(0, 1.0), (1, 0.95)], 0.9) is None
    d = json.load(open(Path(__file__).parent / 'haar_test/haar_chi3_seed9999/da_check.json'))
    s = stats(d)
    print('selftest haar chi3 seed9999:', {k: (round(v, 3) if v is not None else None) for k, v in s.items()})
    assert abs(s['m_L'] - 8.5) < 0.01 and abs(s['m_R'] - 8.5) < 0.01, s
    assert abs(s['m_half'] - 8.5) < 0.01 and abs(s['gap']) < 0.02, s
    assert s['w_Lg'] == 9 and s['w_Rg'] == 9, s                  # the DA check's grid-point w
    print('selftest PASS')


if __name__ == '__main__':
    ap = argparse.ArgumentParser()
    ap.add_argument('--root', default=str(Path(__file__).parent / 'runpod_033/networks'))
    ap.add_argument('--unblind', action='store_true')
    ap.add_argument('--selftest', action='store_true')
    a = ap.parse_args()
    if a.selftest:
        selftest(); sys.exit(0)
    nets = load(a.root)
    complete = report_blinded(nets)
    if a.unblind:
        if not complete:
            sys.exit('REFUSING to unblind: not every planned network is finished (cap-truncation must be '
                     'declared by editing PLANNED, with the reason, before unblinding).')
        report_unblinded(nets)
