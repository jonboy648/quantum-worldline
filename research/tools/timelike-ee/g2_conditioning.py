#!/usr/bin/env python3
"""
g2_conditioning.py -- is SIM-078's gate G2 reachable by ANY method, or is it ill-conditioned?

The G2 failure could be either of two very different things:
  (a) the MPO is not converged at delta = 0, in which case more bond dimension fixes it and the
      gate stands; or
  (b) Im S at delta = 0 is ill-conditioned -- an arbitrarily small perturbation of tau_A moves it
      by O(1) -- in which case NO method at any cost can clear a 1e-8 bar, and the gate is testing
      the branch convention rather than the code.

This decides between them without any MPO at all. It takes the EXACT tau_A from dense
diagonalisation, perturbs it by a relative epsilon, and watches Im S. Truncation in an MPO is one
particular such perturbation, so the response to a generic one bounds what any method can do.

Run at delta = 0 (the gate) and delta = 5 (every production setting) for contrast.

The chiral theorem says the spectrum of tau_A is closed under conjugation, so conjugate pairs
contribute -2 Re(lambda log lambda) and Im S vanishes. That cancellation is exact only while the
pairing is exact and no eigenvalue sits on the log's branch cut.
"""
import sys, os, json
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import numpy as np
import qw_tlee_mpo as m
import qw_tlee_candidates as qc

OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'sim078_g2_conditioning.json')


def tau_exact(L, hz, R_H, delta, T0):
    H = qc.tfim_dense_hz(L, hz)
    w, U = np.linalg.eigh(H)
    E = (U * np.exp((1j * R_H - delta) * w)) @ U.conj().T
    s = (L - T0) // 2
    dl, da, dr = 1 << s, 1 << T0, 1 << (L - s - T0)
    tau = np.einsum('iajibj->ab', E.reshape(dl, da, dr, dl, da, dr))
    return tau / np.trace(tau)


def S_of_tau(tau):
    lam = np.linalg.eigvals(tau)
    lam = lam[np.abs(lam) > 1e-14]
    return complex(np.sum(-lam * np.log(lam)))


def cut_distance(tau):
    """How close does any eigenvalue come to the negative real axis, where the principal
    branch of the log jumps by 2 pi i? Normalised by |lambda|."""
    lam = np.linalg.eigvals(tau)
    lam = lam[np.abs(lam) > 1e-14]
    return float(np.min(np.abs(np.pi - np.abs(np.angle(lam)))))


def main():
    rng = np.random.default_rng(0)
    L = int(sys.argv[1]) if len(sys.argv) > 1 else 12
    R_H, T0 = 5.0, 4
    eps_list = [0.0, 1e-12, 1e-10, 1e-8, 1e-6, 1e-4]
    out = {'L': L, 'R_H': R_H, 'T0': T0, 'hz': 0.0, 'bar': 1e-8, 'runs': {}}
    for delta in (0.0, 5.0):
        tau = tau_exact(L, 0.0, R_H, delta, T0)
        base = S_of_tau(tau)
        d_cut = cut_distance(tau)
        scale = float(np.max(np.abs(tau)))
        print(f"delta={delta}: exact Im S = {base.imag:.3e}   nearest eigenvalue-to-branch-cut "
              f"angle = {d_cut:.3e} rad", flush=True)
        rows = {}
        for eps in eps_list:
            ims = []
            for trial in range(5 if eps else 1):
                P = rng.normal(size=tau.shape) + 1j * rng.normal(size=tau.shape)
                t2 = tau + eps * scale * P / np.linalg.norm(P) * np.sqrt(P.size)
                t2 = t2 / np.trace(t2)
                ims.append(abs(S_of_tau(t2).imag))
            rows[f'{eps:.0e}'] = {'max_abs_Im': float(max(ims)), 'median': float(np.median(ims)),
                                  'pass_1e-8': bool(max(ims) < 1e-8)}
            print(f"    perturbation {eps:.0e} -> max|Im S| = {max(ims):.3e}  "
                  f"{'ok' if max(ims) < 1e-8 else 'FAIL'}", flush=True)
        out['runs'][f'delta{delta}'] = {'exact_Im': base.imag, 'branch_cut_angle': d_cut,
                                        'perturbations': rows}
    json.dump(out, open(OUT, 'w'), indent=1, default=float)
    print('wrote', OUT)


if __name__ == '__main__':
    main()
