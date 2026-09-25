"""Quick probe: does maximizing overlap with the exact GS pull MERA entanglement off zero?
Tight (maxiter small) with a per-iteration callback so the S-trajectory is visible live."""
import sys
import time

import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh

import sim036_tci_mera_stage2 as S2

sys.stdout.reconfigure(line_buffering=True)
N = S2.N_QUBITS
NP = S2.N_PARAMS


def half_S(sv):
    l = N // 2
    m = sv.reshape(2 ** l, 2 ** (N - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


H = S2.build_OF_tricritical(N)
Ev, gv = eigsh(H, k=1, which="SA")
E0 = float(Ev[0]); gs = S2.project_z2(gv[:, 0], N)
S_ex = half_S(gs)
psi_t = gs

rng = np.random.default_rng(11)
theta = rng.standard_normal(NP) * 0.1
sv0 = S2.project_z2(S2.build_mera_sv(theta), N)
print(f"exact S={S_ex:.4f} | init S={half_S(sv0):.5f}  ov={abs(np.vdot(gs, sv0))**2:.4f}", flush=True)


def neg_ov(p):
    sv = S2.build_mera_sv(p)
    return float(1.0 - abs(np.vdot(psi_t, sv)) ** 2)


t0 = time.time()
it = {"n": 0}


def cb(p):
    it["n"] += 1
    sv = S2.project_z2(S2.build_mera_sv(p), N)
    print(f"  it {it['n']:2d}: 1-ov={neg_ov(p):.4e}  ov-exact={abs(np.vdot(gs, sv))**2:.4f}  "
          f"S={half_S(sv):.4f}  ({time.time()-t0:.0f}s)", flush=True)


minimize(neg_ov, theta, method="L-BFGS-B", callback=cb,
         options={"maxiter": 12, "ftol": 1e-12, "gtol": 1e-9})
print("PROBE DONE", flush=True)
