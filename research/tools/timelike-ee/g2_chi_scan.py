#!/usr/bin/env python3
"""
g2_chi_scan.py -- diagnosis of the SIM-2026-078 gate G2 failure.

G2 (PREREGISTRATION-HYP032-B.md): at h_z = 0, delta = 0, |Im S| < 1e-8 at every L, reproducing the
SIM-076 theorem through the MPO code path. It FAILED on the pod at chi = 128: 5.6e-2 (L=12),
3.05 (L=16), 2.99 (L=24).

THE BAR IS NOT BEING CHANGED. This asks the only legitimate question: can the calculation be made
good enough to clear an unchanged gate, the way a fourth-order product formula was the answer to
G1's 1e-6? At delta = 0 there is no damping, so the cost is real-time operator entanglement.

Reports, at each (L, chi): |Im S| against the 1e-8 bar, the truncation error, AND the distance from
exact diagonalisation in the REAL part -- because the L=8 probe showed the imaginary part sitting at
1e-13 while the real part was still wrong by 3e-4, i.e. the symmetry survives truncation and the
value does not.

Local run, L <= 12 only: the pre-registration permits gate-only smoke tests at that size.
"""
import sys, os, json, time
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import qw_tlee_mpo as m
import qw_tlee_candidates as qc

R_H = 5.0
DELTA = 0.0
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sim078_g2scan_local.json')


def main():
    Ls = tuple(int(x) for x in (sys.argv[1] if len(sys.argv) > 1 else '8,10,12').split(','))
    chis = tuple(int(x) for x in (sys.argv[2] if len(sys.argv) > 2 else '64,128,256,512').split(','))
    T0s, _ = m.windows(m.V * R_H)
    out = {'gate': 'G2', 'bar': 1e-8, 'R_H': R_H, 'delta': DELTA, 'hz': 0.0,
           'note': 'bar unchanged; asking whether chi can reach it', 'rows': {}}
    for L in Ls:
        H = qc.tfim_dense_hz(L, 0.0)
        qc._H_EIG.clear()
        ex = qc.route_X_H(H, L, R_H, T0s, DELTA)
        ed_im = float(max(abs(ex[t].imag) for t in T0s))
        print(f"L={L}: exact-diagonalisation max|Im S| = {ed_im:.3e} (the theorem)", flush=True)
        for chi in chis:
            t0 = time.time()
            got, st = m.S_of(L, 0.0, R_H, DELTA, T0s, chi, 0.1)
            im = float(max(abs(got[t].imag) for t in T0s))
            dre = float(max(abs(got[t].real - ex[t].real) for t in T0s))
            row = {'L': L, 'chi': chi, 'max_abs_Im': im, 'pass': bool(im < 1e-8),
                   'max_err_real_vs_ED': dre, 'max_chi': st['max_chi'],
                   'disc': st['max_disc'], 'secs': time.time() - t0}
            out['rows'][f'L{L}_chi{chi}'] = row
            print(f"   chi={chi:4d} maxchi={st['max_chi']:4d}  |Im S|={im:.3e} "
                  f"{'ok' if im < 1e-8 else 'FAIL'}   real-part err vs ED={dre:.2e}  "
                  f"disc={st['max_disc']:.1e}  [{time.time()-t0:.0f}s]", flush=True)
            json.dump(out, open(OUT, 'w'), indent=1, default=float)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
