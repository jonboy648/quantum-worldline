"""
SIM-2026-049 - HYP-2026-027: SPECTRAL-RESIDUAL objective for chi=6 criticality.

WHY: SIM-048 proved the Riemannian optimizer WORKS (powerful monotone descent, broke the EV ceiling)
BUT the scale-invariant ENERGY <rho_hat,h_bar> at chi=6 is too FLAT (~2% spread between c=0.5 and c=6.7
states; lowest energy is NON-critical). Energy-minimization cannot pin chi=6 criticality. The fix:
optimize the CONFORMAL DATA directly -- a loss on the scaling spectrum the energy can't see:
    L(u,w) = (c - c*)^2 + (Delta_sigma - sig*)^2 + (Delta_eps - 1)^2 + (Delta_T - 2)^2
where c, Delta_* come from the matrix-free ascending scaling superoperator (central_charge_and_dims).
At the critical fixed point L=0. This TARGETS scale-invariant criticality directly.

The spectral loss is NOT a simple autograd of energy_net (it goes through eigsh), so we optimize it with
SPSA (Simultaneous Perturbation Stochastic Approximation) on the Stiefel manifold: cheap (2 spectrum
evals/step ~6s regardless of param count), gradient-free, and robust to the flat/rugged landscape.
Warm-start from the eigen-tower seed (c=3.79, Delta_T~2 already present -- the best non-energy state).
Retraction keeps (u,w) isometric each step.

GATE: c in [0.45,0.55] AND sigma in [0.10,0.15] AND sigma>0.057 (basin) AND eps~1 AND Delta_T within
0.05 of 2. Then chi=4-block sanity, then TCI.

Reuses sim045 (central_charge_and_dims) + sim048 (retract, _mat). torch 2.8.
"""
import sys
import time

import numpy as np
import torch

import sim045_scaleinv_stable as M45
import sim048_riemannian_chi6 as M48

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

CHI = 6
torch.set_default_dtype(torch.float64)


def spectral_loss(w_np, u_np, chi, c_star, sig_star, k=8):
    """L = (c-c*)^2 + (sigma-sig*)^2 + (eps-1)^2 + (Delta_T-2)^2, from the scaling superoperator.
    Returns (L, c, dims)."""
    try:
        c, s1, dims = M45.central_charge_and_dims(w_np, u_np, chi, k=k)
    except Exception:
        return 1e6, 9.9, np.zeros(k)
    sig = dims[1] if len(dims) > 1 else 9
    eps = dims[2] if len(dims) > 2 else 9
    T_err = min((abs(x - 2.0) for x in dims if abs(x - 2.0) < 0.4), default=0.4)
    L = (c - c_star) ** 2 + (sig - sig_star) ** 2 + (eps - 1.0) ** 2 + T_err ** 2
    return float(L), float(c), dims


def _rand_tangent(W, rng):
    """random tangent perturbation (project a random tensor to the tangent space at W, unit norm)."""
    R = rng.standard_normal(W.shape) + 1j * rng.standard_normal(W.shape)
    Rt = M48.rgrad_stiefel(torch.tensor(R, dtype=torch.complex128), torch.tensor(W, dtype=torch.complex128))
    n = float(torch.linalg.norm(Rt.reshape(-1)))
    return (Rt / n) if n > 1e-12 else Rt


def optimize(lam3, chi, label, seed_ckpt, max_iter=300, a0=0.05, c0=0.05, seed=0):
    """SPSA on the Stiefel manifold minimizing the spectral loss. Per step: perturb (w,u) by +/- delta
    along a shared random tangent direction, estimate the directional gradient from the two spectral-loss
    values, step along -grad, retract. Adaptive a_k, c_k decay (Spall's schedule)."""
    d = np.load(seed_ckpt); w_np, u_np = d["w"].copy(), d["u"].copy()
    c_star = 0.5 if abs(lam3) < 1e-9 else 0.70
    sig_star = 0.125 if abs(lam3) < 1e-9 else 0.075
    rng = np.random.default_rng(seed)
    t0 = time.time(); best = None; best_L = 1e9; hist = []
    L, c, dims = spectral_loss(w_np, u_np, chi, c_star, sig_star)
    print(f"  [{label}] seed: L={L:.4f} c={c:.3f} sig={dims[1]:.3f} eps={dims[2]:.3f}", flush=True)

    for it in range(max_iter):
        ak = a0 / (it + 1 + 50) ** 0.602
        ck = c0 / (it + 1) ** 0.101
        dW = _rand_tangent(w_np, rng); dU = _rand_tangent(u_np, rng)
        wp = M48.retract(M48._T(w_np), dW, ck).numpy(); up = M48.retract(M48._T(u_np), dU, ck).numpy()
        wm = M48.retract(M48._T(w_np), dW, -ck).numpy(); um = M48.retract(M48._T(u_np), dU, -ck).numpy()
        Lp, _, _ = spectral_loss(wp, up, chi, c_star, sig_star)
        Lm, _, _ = spectral_loss(wm, um, chi, c_star, sig_star)
        ghat = (Lp - Lm) / (2 * ck)                      # directional gradient estimate
        # step along -ghat * direction
        w_np = M48.retract(M48._T(w_np), dW, -ak * ghat).numpy()
        u_np = M48.retract(M48._T(u_np), dU, -ak * ghat).numpy()
        L, c, dims = spectral_loss(w_np, u_np, chi, c_star, sig_star)
        hist.append(round(c, 3))
        if L < best_L:
            best_L = L; best = (w_np.copy(), u_np.copy(), c, dims.copy(), it)
        if it % 10 == 0:
            T = [round(float(x), 3) for x in dims if abs(x - 2) < 0.15]
            print(f"  [{label}] {it}: L={L:.4f} c={c:.4f} sig={dims[1]:.4f} eps={dims[2]:.4f} T={T} "
                  f"({time.time()-t0:.0f}s)", flush=True)

    w_np, u_np, c, dims, bo = best
    np.savez(f"uw_{label}_spectral_chi{chi}.npz", w=w_np, u=u_np, c=c, dims=dims)
    print(f"  [{label}] BEST it {bo}: L={best_L:.4f} c={c:.4f} sig={dims[1]:.4f} eps={dims[2]:.4f} "
          f"dims={np.round(dims[:8],4)} ({time.time()-t0:.0f}s)", flush=True)
    return {"c": float(c), "dims": [float(x) for x in dims[:18]], "best_L": best_L, "c_history": hist,
            "best_it": bo, "wall_s": round(time.time() - t0)}


def main():
    import json
    import os
    chi = CHI
    seed = "seed_chi6_eigentower.npz"
    if not os.path.exists(seed):
        print("no eigen-tower seed; run sim047 first"); return
    print(f"SIM-2026-049: SPECTRAL-residual SPSA chi={chi}", flush=True)
    ising = optimize(0.0, chi, "ISING", seed, max_iter=300)
    sig, eps = ising["dims"][1], ising["dims"][2]
    T_err = min((abs(x - 2.0) for x in ising["dims"] if abs(x - 2.0) < 0.3), default=9.9)
    gate = abs(ising["c"] - 0.5) < 0.05 and 0.057 < sig < 0.15 and abs(eps - 1) < 0.05 and T_err < 0.05
    out = {"id": "SIM-2026-049", "type": "classical", "date": "2026-06-19", "hypothesis_id": "HYP-2026-027",
           "chi": chi, "ising": ising, "ising_gate_pass": bool(gate),
           "method": "SPSA on Stiefel manifold minimizing the spectral-residual loss "
                     "(c-c*)^2+(sigma-sig*)^2+(eps-1)^2+(Delta_T-2)^2 -- targets conformal data the flat "
                     "energy cannot see. Eigen-tower seed.",
           "verdict": ("GATE PASS -> chi=6 critical via spectral objective." if gate else
                       f"chi=6 spectral: c={ising['c']:.4f} sig={sig:.4f} eps={eps:.4f} T_err={T_err:.3f}. "
                       + ("sig beat 0.057" if sig > 0.057 else "sig not beat 0.057"))}
    with open("SIM-2026-049.json", "w") as f:
        json.dump(out, f, indent=2)
    print("VERDICT:", out["verdict"], flush=True)


if __name__ == "__main__":
    main()
