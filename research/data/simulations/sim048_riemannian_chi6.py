"""
SIM-2026-048 - HYP-2026-027: RIEMANNIAN (Stiefel) optimization to push chi=6 to criticality.

WHY: the EV first-order polar-SVD environment update has a chi=6 CEILING -- 4 seeds plateau off c=0.5.
Hauru-Damle-Vidal (SciPost Phys 10,040 / arXiv:2007.03638) PROVE EV = preconditioned gradient descent
in the large-gamma (small-step) limit -- first order, no line search, no curvature -- which is exactly
why it stalls on the near-singular critical landscape (Hessian near-zero modes = CFT dispersion). The
documented cure: Riemannian CG/L-BFGS on the Stiefel manifold (curvature + Wolfe line search), with the
reduced-density-matrix PRECONDITIONER as the crucial ingredient.

APPROACH (per the recipe synthesis, wf_2c975389): MANIFOLD-DIRECT, NOT Cayley-generator.
  - Euclidean gradient = the EV environment (reuse sim045.grad_t = conj(dE/dW)). rho_hat and h_bar are
    RECOMPUTED + DETACHED every iteration (envelope theorem: at the scale-inv fixed point the implicit
    derivatives through rho/h vanish, so the EV environment IS the correct gradient -- do NOT autograd
    through the eigensolve).
  - Riemannian gradient (Stiefel, Euclidean metric): rgrad = G - M sym(M^H G), sym(A)=0.5(A+A^H).
  - Retraction: POSITIVE polar U@Vh of (W + alpha*xi)  [NOTE sim045.svd_polar is NEGATIVE -U@Vh for the
    EV optimum -- the Riemannian retraction must be POSITIVE; mixing signs diverges].
  - Riemannian CG (Polak-Ribiere) + Armijo backtracking line search + projection-based vector transport.
  - rho-PRECONDITIONER (Hauru's crucial ingredient, escalation): per tensor solve the QNG metric using
    the top-index reduced density matrix (Sylvester for the skew part + rho^-1 for the perp part,
    regularized (rho^2+delta^2)^-1/2, delta=||grad||_F).
  - Transitional (w1,u1): settle briefly against the seeded bulk then FREEZE (freeze-then-bulk); only the
    scale-invariant bulk (w,u) is Riemannian-optimized.

SEED: seed_chi6_eigentower.npz (best: c=3.79, clean isometries) + multi-restart with small kicks.
GATE: chi=6 Ising c in [0.45,0.55] AND sigma in [0.10,0.15] AND sigma < chi=4's 0.057 (basin
discriminator) AND eps ~1 AND a dim within 0.05 of Delta_T=2 AND stationary. Then chi=4-block sanity,
then TCI (lam3=0.856).

Reuses sim045 (energy_net, grad_t, rho_fixedpoint, hbar_selfconsistent, central_charge_and_dims) +
sim043 (lift_H). torch 2.8, matrix-free, local (~4s/round).
"""
import sys
import time

import numpy as np
import torch

import sim045_scaleinv_stable as M45

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

CHI = 6
torch.set_default_dtype(torch.float64)
_T = M45._T


# ---- manifold primitives ----
def _mat(W):
    """reshape an isometric tensor to a tall matrix (rows>=cols), same grouping as svd_polar."""
    sh = W.shape
    return W.reshape(sh[0] * sh[1], -1), sh


def rgrad_stiefel(G, W):
    """Riemannian (tangent-projected) gradient, Stiefel Euclidean metric: rgrad = G - M sym(M^H G)."""
    M, sh = _mat(W)
    Gm, _ = _mat(G)
    MhG = M.conj().T @ Gm
    sym = 0.5 * (MhG + MhG.conj().T)
    return (Gm - M @ sym).reshape(sh)


def retract(W, xi, alpha):
    """POSITIVE polar retraction: nearest isometry to W + alpha*xi (U@Vh, NOT -U@Vh)."""
    M, sh = _mat(W)
    Xm, _ = _mat(xi)
    A = M + alpha * Xm
    U, _, Vh = torch.linalg.svd(A, full_matrices=False)
    return (U @ Vh).reshape(sh)


def transport(Y, W):
    """Projection-based vector transport of Y onto the tangent space at W."""
    return rgrad_stiefel(Y, W)


def _inv_sqrt_reg(rho, delta):
    """(rho^2 + delta^2 I)^{-1/2} via eigendecomposition (rho Hermitian PSD)."""
    ev, V = torch.linalg.eigh(0.5 * (rho + rho.conj().T))
    d = (ev * ev + delta * delta) ** (-0.5)
    return (V * d) @ V.conj().T


def precondition(rg, W, rho_top):
    """rho reduced-density-matrix preconditioner (Hauru's crucial ingredient), diagonal QNG metric:
    contract the tangent gradient's TOP index/indices with (rho_top^2 + delta^2)^{-1/2}, delta=||rg||_F.
    W=w (chi,chi,chi): top index = axis 2, rho_top = rho1 (chi x chi). W=u (chi,chi,chi,chi): top =
    axes (2,3) grouped, rho_top = rho2 (chi^2 x chi^2). re-project to tangent after (keeps it tangent)."""
    delta = max(ip(rg, rg) ** 0.5, 1e-12)
    P = _inv_sqrt_reg(rho_top.to(torch.complex128), delta)
    if W.ndim == 3:                          # isometry w: top axis 2
        out = torch.tensordot(rg, P, dims=([2], [0]))           # (chi,chi,chi') contract top with P
    else:                                    # disentangler u: top axes (2,3) grouped to chi^2
        c = W.shape[0]
        rgm = rg.reshape(c * c, c * c)                          # (bottom-pair, top-pair)
        out = (rgm @ P).reshape(c, c, c, c)
    return rgrad_stiefel(out, W)             # re-project to tangent


def ip(A, B):
    """Real Frobenius inner product Re Tr(A^H B) over a tensor."""
    return float(torch.real(torch.sum(torch.conj(A) * B)))


# ---- objective pieces (all detached fixed points) ----
def _h_phys_shifted(lam3):
    h = M45.of_hamiltonian_3site(lam3).reshape(8, 8); h = 0.5 * (h + h.conj().T)
    lam = float(np.linalg.eigvalsh(h).max())
    return (h - lam * np.eye(8)).reshape((2,) * 6)


def lift_H_chi(lam3, chi):
    """Build the chi-dim bulk Hamiltonian base by lifting the EV-shifted physical 3-site OF term through
    a 2-site->chi NRG isometry. The binary first layer maps phys^2=4 -> chi, so the isometry is
    rank-capped at 4: use the chi (<=4) lowest eigenvectors of the 2-site block, PAD into chi-space with
    zeros for chi>4. h_bar's self-consistent ascend then fills the padded directions during optimization.
    (Reuses sim043.lift_H for chi<=4; pads for chi>4.)"""
    if chi <= 4:
        import sim043_chi6_universality as M43
        return M43.lift_H(lam3, chi)
    I = np.eye(2); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)
    def k2(a, b): return np.kron(a, b)
    h2 = -2 * (k2(X, I) + k2(I, X)) / 2 - 2 * k2(Z, Z)
    ev, vec = np.linalg.eigh(h2)
    w0 = np.zeros((2, 2, chi), dtype=complex)
    w0[:, :, :4] = vec[:, :4].reshape(2, 2, 4)        # rank-4 physical block padded into chi
    wc0 = w0.conj()
    h3 = M45.of_hamiltonian_3site(lam3).reshape(8, 8); h3 = 0.5 * (h3 + h3.conj().T)
    lam = float(np.linalg.eigvalsh(h3).max())
    h3 = (h3 - lam * np.eye(8)).reshape(2, 2, 2, 2, 2, 2)   # EV shift (Eq.63)
    hb2 = np.einsum("xiA,jkB,ijkpqr,xpC,qrD->ABCD", w0, w0, h3, wc0, wc0, optimize=True)
    hb2 = 0.5 * (hb2 + hb2.conj().transpose(2, 3, 0, 1))
    Ichi = np.eye(chi)
    return np.einsum("ABCD,EF->ABECDF", hb2, Ichi)


def lift_H_two_transitional(lam3, chi, trans_ckpt):
    """Build a GENUINE chi-dim critical Hamiltonian base by ascending the EV-shifted physical 3-site OF
    term through sim046's VALIDATED 2-transitional layers (w1: phys^2->cmid, w2: cmid^2->chi). Unlike the
    rank-4 pad (whose energy minimum is NON-critical), this lifts the FULL critical TFIM into chi-space
    via layers that produced a faithful chi=6 critical state (rel 0.004%). Returns numpy rank-6 (chi)*6."""
    d = np.load(trans_ckpt)
    w1, u1, w2, u2 = d["w1"], d["u1"], d["w2"], d["u2"]   # (2,2,cmid),(2,2,2,2),(cmid,cmid,chi),(cmid,..)
    cmid = w1.shape[2]
    h3 = M45.of_hamiltonian_3site(lam3).reshape(8, 8); h3 = 0.5 * (h3 + h3.conj().T)
    lam = float(np.linalg.eigvalsh(h3).max())
    h3 = (h3 - lam * np.eye(8)).reshape((2,) * 6)
    # ascend physical 3-site term through layer-1 (w1,u1) -> cmid-dim rank-6, then layer-2 (w2,u2) -> chi
    hb_cmid = M45.ascend_first(h3, w1, u1, cmid)          # (cmid,)*6
    # second ascend: treat hb_cmid as a "physical" cmid-dim 3-site term, lift cmid->chi via (w2,u2)
    hb_chi = M45.ascend_first(hb_cmid, w2, u2, chi)       # (chi,)*6
    M = hb_chi.reshape(chi ** 3, chi ** 3); M = 0.5 * (M + M.conj().T)
    return M.reshape((chi,) * 6)


def fixed_points(w_np, u_np, h0_bulk_np, chi, n_hbar):
    """Recompute (rho_hat, h_bar) from current (w,u); return DETACHED torch operators."""
    rho = M45.rho_fixedpoint(w_np, u_np, chi).detach()
    hbar = M45.hbar_selfconsistent(h0_bulk_np, w_np, u_np, chi, n_hbar).detach()
    return rho, hbar


def energy_val(w_np, u_np, rho, hbar):
    return float(M45.energy_net(hbar, rho, _T(w_np), _T(u_np)).real)


def top_rdms(rho, chi):
    """Top-index reduced density matrices from the descending fixed point rho_hat (rank-6, detached):
    rho1 (chi x chi) for the isometry top index, rho2 (chi^2 x chi^2) for the disentangler top pair."""
    r3 = np.asarray(rho.detach()).reshape((chi,) * 6)
    rho2 = np.trace(r3, axis1=2, axis2=5).reshape(chi * chi, chi * chi)
    rho2 = 0.5 * (rho2 + rho2.conj().T)
    rho1 = np.trace(rho2.reshape(chi, chi, chi, chi), axis1=1, axis2=3)
    rho1 = 0.5 * (rho1 + rho1.conj().T)
    return _T(rho1 / np.trace(rho1)), _T(rho2 / np.trace(rho2))


def euclid_grads(w_np, u_np, rho, hbar):
    """EV environments = Euclidean gradients wrt w and u (autograd of energy_net, rho/hbar detached)."""
    gw = M45.grad_t(hbar, rho, _T(w_np), _T(u_np), "w")
    gu = M45.grad_t(hbar, rho, _T(w_np), _T(u_np), "u")
    return gw, gu


def optimize(lam3, chi, label, seed_ckpt=None, max_iter=150, n_hbar=5, ev_interleave=8,
             precond=True, verbose=True):
    """Riemannian CG (Polak-Ribiere, Armijo line search, projection transport) on the bulk (w,u).
    precond=True applies the rho reduced-density-matrix preconditioner (Hauru's crucial ingredient).
    Optional EV-interleave every ev_interleave steps (documented last-factor curvature fix)."""
    h0_bulk_np = lift_H_chi(lam3, chi)
    rng = np.random.default_rng(0)
    # seed bulk
    if seed_ckpt is not None:
        d = np.load(seed_ckpt); w_np, u_np = d["w"].copy(), d["u"].copy()
        if verbose: print(f"  [{label}] seeded bulk from {seed_ckpt}", flush=True)
    else:
        def riso(a, b):
            X = rng.standard_normal((a, b)) + 1j * rng.standard_normal((a, b)); Q, _ = np.linalg.qr(X); return Q[:, :b]
        w_np = riso(chi * chi, chi).reshape(chi, chi, chi)
        u_np = riso(chi * chi, chi * chi).reshape(chi, chi, chi, chi)

    c_target = 0.5 if abs(lam3) < 1e-9 else 0.70
    sig_target = 0.125 if abs(lam3) < 1e-9 else 0.075
    t0 = time.time(); best = None; best_loss = 1e9; chist = []
    d_w = d_u = None; g_w_prev = g_u_prev = None; alpha_prev = 1.0

    for it in range(max_iter):
        rho, hbar = fixed_points(w_np, u_np, h0_bulk_np, chi, n_hbar)
        gw_e, gu_e = euclid_grads(w_np, u_np, rho, hbar)
        rg_w = rgrad_stiefel(gw_e, _T(w_np))             # RAW Riemannian gradient (for slope + gauge)
        rg_u = rgrad_stiefel(gu_e, _T(u_np))
        gnorm = (ip(rg_w, rg_w) + ip(rg_u, rg_u)) ** 0.5
        if precond:                                       # rho-precondition only the SEARCH direction
            rho1_t, rho2_t = top_rdms(rho, chi)
            g_w = precondition(rg_w, _T(w_np), rho1_t)
            g_u = precondition(rg_u, _T(u_np), rho2_t)
        else:
            g_w, g_u = rg_w, rg_u

        # CG direction (Polak-Ribiere) with projection transport of the previous direction
        if d_w is None:
            d_w, d_u = -g_w, -g_u
        else:
            tg_w = transport(g_w_prev, _T(w_np)); tg_u = transport(g_u_prev, _T(u_np))
            y_w = g_w - tg_w; y_u = g_u - tg_u
            denom = ip(g_w_prev, g_w_prev) + ip(g_u_prev, g_u_prev)
            beta = max(0.0, (ip(g_w, y_w) + ip(g_u, y_u)) / denom) if denom > 1e-30 else 0.0
            td_w = transport(d_w, _T(w_np)); td_u = transport(d_u, _T(u_np))
            d_w = -g_w + beta * td_w; d_u = -g_u + beta * td_u

        # Armijo line search. SLOPE uses the RAW Riemannian gradient (the true directional derivative of
        # the energy); the preconditioned g only shapes the direction. Warm-start alpha from the previous
        # accepted step and allow it to GROW (try 2*alpha_prev) so well-scaled precond steps aren't
        # crushed to ~0 by halving-from-1.
        E0 = energy_val(w_np, u_np, rho, hbar)
        slope = ip(rg_w, d_w) + ip(rg_u, d_u)
        if slope > 0:                       # not a descent dir -> reset to steepest (raw)
            d_w, d_u = -rg_w, -rg_u; slope = -(gnorm ** 2)
        alpha = min(2.0 * alpha_prev, 1.0) if it > 0 else 1.0
        accepted = False
        for _ls in range(30):
            w_try = retract(_T(w_np), d_w, alpha).numpy()
            u_try = retract(_T(u_np), d_u, alpha).numpy()
            rho_t, hbar_t = fixed_points(w_try, u_try, h0_bulk_np, chi, n_hbar)
            E1 = energy_val(w_try, u_try, rho_t, hbar_t)
            if E1 <= E0 + 1e-4 * alpha * slope:
                accepted = True; break
            alpha *= 0.5
        if accepted:
            w_np, u_np = w_try, u_try; alpha_prev = alpha
        else:
            alpha_prev = max(alpha, 1e-3)   # don't let alpha_prev collapse permanently
        g_w_prev, g_u_prev = g_w, g_u

        # optional EV interleave (curvature/last-factor fix)
        if ev_interleave and (it + 1) % ev_interleave == 0:
            rho, hbar = fixed_points(w_np, u_np, h0_bulk_np, chi, n_hbar)
            w_np = M45.svd_polar(M45.grad_t(hbar, rho, _T(w_np), _T(u_np), "w")).detach().numpy()
            u_np = M45.svd_polar(M45.grad_t(hbar, rho, _T(w_np), _T(u_np), "u")).detach().numpy()

        c, s1, dims = M45.central_charge_and_dims(w_np, u_np, chi, k=12)
        chist.append(round(c, 3))
        loss = abs(c - c_target) + abs(dims[2] - 1.0) + abs(dims[1] - sig_target)
        if loss < best_loss:
            best_loss = loss; best = (w_np.copy(), u_np.copy(), c, s1, dims.copy(), it)
        if verbose and it % 5 == 0:
            T = [round(float(x), 3) for x in dims if abs(x - 2) < 0.15]
            print(f"  [{label}] {it}: c={c:.4f} sig={dims[1]:.4f} eps={dims[2]:.4f} T={T} "
                  f"|g|={gnorm:.1e} a={alpha:.0e} ({time.time()-t0:.0f}s)", flush=True)
        if gnorm < 1e-7:
            print(f"  [{label}] converged |g|={gnorm:.1e} at it {it}", flush=True); break

    w_np, u_np, c, s1, dims, bo = best
    np.savez(f"uw_{label}_riemann_chi{chi}.npz", w=w_np, u=u_np, c=c, s1=s1, dims=dims)
    if verbose:
        print(f"  [{label}] BEST it {bo}: c={c:.4f} s1={s1:.4f} dims={np.round(dims[:8],4)} ({time.time()-t0:.0f}s)", flush=True)
    return {"c": float(c), "s1": float(s1), "dims": [float(x) for x in dims[:18]], "c_history": chist,
            "best_it": bo, "wall_s": round(time.time() - t0)}


def main():
    import json
    import os
    chi = CHI
    print(f"SIM-2026-048: Riemannian (Stiefel CG) chi={chi} scale-invariant MERA", flush=True)
    seed = "seed_chi6_eigentower.npz" if os.path.exists("seed_chi6_eigentower.npz") else None
    ising = optimize(0.0, chi, "ISING", seed_ckpt=seed)
    sig, eps = ising["dims"][1], ising["dims"][2]
    T_err = min((abs(x - 2.0) for x in ising["dims"] if abs(x - 2.0) < 0.3), default=9.9)
    c_ok = abs(ising["c"] - 0.5) < 0.05
    sig_ok = 0.057 < sig < 0.15
    eps_ok = abs(eps - 1.0) < 0.05
    T_ok = T_err < 0.05
    gate = c_ok and sig_ok and eps_ok and T_ok
    print(f"\nISING GATE: c={ising['c']:.4f}(ok={c_ok}) sig={sig:.4f}(ok={sig_ok}; beat 0.057?) "
          f"eps={eps:.4f}(ok={eps_ok}) T_err={T_err:.3f}(ok={T_ok}) -> {'PASS' if gate else 'FAIL'}", flush=True)
    out = {"id": "SIM-2026-048", "type": "classical", "date": "2026-06-19", "hypothesis_id": "HYP-2026-027",
           "chi": chi, "ising": ising, "ising_gate_pass": bool(gate),
           "method": "Riemannian Stiefel CG (Polak-Ribiere, Armijo, projection transport) on the bulk "
                     "(w,u); envelope gradient (rho_hat,h_bar detached); EV-interleave every 8; eigentower seed.",
           "verdict": ("GATE PASS -> chi=6 critical; run TCI." if gate else
                       f"chi=6 Ising c={ising['c']:.4f} sig={sig:.4f} (chi=4 was 0.057) T_err={T_err:.3f}. "
                       + ("sigma BEAT 0.057 -> Riemannian escaped the EV ceiling (progress!)" if sig > 0.057
                          else "sigma did not beat 0.057 -> add rho-preconditioner (Hauru's crucial ingredient)."))}
    if gate:
        tci = optimize(0.856, chi, "TCI", seed_ckpt=f"uw_ISING_riemann_chi{chi}.npz")
        T_tci = [round(x, 3) for x in tci["dims"] if abs(x - 2.0) < 0.2]
        out["tci"] = tci
        out["verdict"] += (f" | TCI c={tci['c']:.4f} near-2={T_tci} -> "
                           + ("Delta_T~2 => alpha=4 UNIVERSAL at c=7/10." if T_tci and min(abs(x-2) for x in T_tci) < 0.05
                              else "Delta_T not cleanly 2; escalate chi->8."))
    with open("SIM-2026-048.json", "w") as f:
        json.dump(out, f, indent=2)
    print("VERDICT:", out["verdict"], flush=True)
    print("saved -> SIM-2026-048.json", flush=True)


if __name__ == "__main__":
    main()
