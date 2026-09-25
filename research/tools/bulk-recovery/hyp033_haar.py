"""C-HAAR control networks for HYP-033: same graph and dimensions as the optimized chi networks,
Haar-random disentanglers and isometries, Haar-random normalized top tensor on the 3-site ring.
Written in the qw_hyp033_export.jl format (column-major ComplexF64 .bin + meta.txt + info.txt) so
hyp033_grid.py treats them exactly like an optimized network (top.bin overrides the H2 ring state).

usage: python hyp033_haar.py OUTDIR chi seed_lo seed_hi [d=4]
"""
import sys
import time
from pathlib import Path

import numpy as np

sys.path.insert(0, str(Path(__file__).resolve().parent))
from g0_feasibility import haar_isometry


def write(dir, name, A, meta):
    A = np.ascontiguousarray(np.asfortranarray(A.astype(np.complex128)))
    (dir / f'{name}.bin').write_bytes(np.asfortranarray(A).tobytes(order='F'))
    meta.write(f'{name} {A.ndim} ' + ' '.join(str(s) for s in A.shape) + '\n')


def main():
    out, chi, lo, hi = Path(sys.argv[1]), int(sys.argv[2]), int(sys.argv[3]), int(sys.argv[4])
    d = int(sys.argv[5]) if len(sys.argv) > 5 else 4
    for seed in range(lo, hi + 1):
        rng = np.random.default_rng(1_000_000 + 1000 * chi + seed)
        dir = out / f'haar_chi{chi}_seed{seed}'
        dir.mkdir(parents=True, exist_ok=True)
        dim = [d, min(chi, d ** 3), chi]
        with open(dir / 'meta.txt', 'w') as meta:
            for l in (1, 2):
                din, dout = dim[l - 1], dim[l]
                write(dir, f'u{l}', haar_isometry(rng, din * din, din * din).reshape(din, din, din, din), meta)
                write(dir, f'w{l}', haar_isometry(rng, din ** 3, dout).reshape(din, din, din, dout), meta)
            top = rng.normal(size=(chi,) * 3) + 1j * rng.normal(size=(chi,) * 3)
            write(dir, 'top', top / np.linalg.norm(top), meta)
        (dir / 'info.txt').write_text(f'chi {chi}\nseed {seed}\nhfield nan\ncontrol C-HAAR\nbasin_clean n/a\n'
                                      f'd_sig nan\nd_eps nan\nE_inf nan\ngenerated {time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime())}\n')
        print('wrote', dir)


if __name__ == '__main__':
    main()
