"""
SIM-2026-043 - HYP-2026-027 stage-4 (THE universality run): chi=6 scale-invariant MERA spectrum.

Answers "is Delta_T=2 (universal stress tensor, alpha=2*Delta_T=4) present at the tricritical-Ising
c=7/10 point?" -- which chi=4 PROVED it cannot resolve (the Ising control, where Delta_T=2 is a
theorem, read only ~1.9 at chi=4). chi=6 (operator space 6^6=46656) is needed for the stress-tensor
dimension. RunPod-deployable (heavy: matrix-free superop on 46656-dim space).

VALIDATED APPROACH (from the chi=4 session, controls confirmed):
  - PLAIN NRG-LIFT (NOT self-consistent-h, which DEGRADED the Ising control 0.139->0.053): build the
    bulk Hamiltonian by ascending the physical d=2 3-site OF term through a first-layer isometry w0
    (w0 = chi lowest eigvecs of the 2-site physical block). Spectrum-preserving, fixes the padding bug.
  - Scale-invariant binary MERA optimization (Evenbly-Vidal SVD-update sweep on the lifted bulk H).
  - Matrix-free ascending superoperator (grad of the tested simple_mera.py energy network) -> {Delta}.
  - GATE B: Ising control (lam3=0) must give {0, 1/8, 1, ..., 2}; at chi=6 the stress tensor should
    resolve much closer to 2.0 than chi=4's 1.9 (this IS the gate that licenses the TCI Delta_T claim).
  - Then TCI (lam3=0.856): read Delta_T. Compare control's Delta_T-resolution to TCI's near-2 value.

Self-contained (energy network inlined). numpy round-trip per iter breaks torch graph accumulation
(the chi=4 silent-death fix). Output: SIM-2026-043.json + uw checkpoints per coupling.
"""
import json
import sys
import time

import numpy as np
import torch
from scipy.sparse.linalg import LinearOperator, eigs

sys.stdout.reconfigure(line_buffering=True)

CHI = 6
N_IT = 200
OUT = "SIM-2026-043.json"


def _T(a):
    return torch.tensor(a, dtype=torch.complex128)


# ---- tested binary MERA energy network (Google simple_mera.py wiring) ----
# VERBATIM from the validated binary_mera_superop.binary_mera_energy_torch (matches the reference to
# 1e-9; do NOT compress the einsum index strings -- a compressed paraphrase broke it 2.58 vs 2.13).
def energy_net(op, rho, w, u):
    wc = torch.conj(w); uc = torch.conj(u)
    out = 0.0
    for dirn in ("left", "right"):
        if dirn == "right":
            expr = ("t a P, b c Q, d s R,"
                    "m i a b, j k c d,"
                    "x y z i j k,"
                    "m x e f, y z g h,"
                    "t e S, f g T, h s U,"
                    "P Q R S T U->")
        else:
            expr = ("t a P, b c Q, d s R,"
                    "i j a b, k n c d,"
                    "x y z i j k,"
                    "x y e f, z n g h,"
                    "t e S, f g T, h s U,"
                    "P Q R S T U->")
        val = torch.einsum(expr, w, w, w, u, u, op, uc, uc, wc, wc, wc, rho)
        out = out + val
    return 0.5 * torch.real(out)


def of_hamiltonian_3site(lam3):
    I = np.eye(2); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)
    def k(a, b, c): return np.kron(np.kron(a, b), c)
    H = (-2.0 * (k(X, I, I) + k(I, X, I) + k(I, I, X)) / 2.0
         - 2.0 * (k(Z, Z, I) + k(I, Z, Z))
         + lam3 * (k(X, Z, Z) + k(Z, Z, X)))
    return H.reshape(2, 2, 2, 2, 2, 2)


def lift_H(lam3, chi):
    """Plain NRG first-layer lift (validated): w0 = chi lowest eigvecs of the 2-site physical block;
    ascend the physical 3-site OF term -> bulk chi-dim 3-site H. Spectrum-preserving.

    EV SHIFT (0707.1454 Eq.63, REQUIRED to escape the trivial fixed point): shift the physical
    3-site term negative-semidefinite, h3 -> h3 - lambda_max(h3)*I, BEFORE the w0 ascend. This is
    the literature-correct placement (per-physical-term, before lifting). Verified spectrum-identical
    to shifting the lifted bulk (off-diag diff 1.8e-15; a constant shift is unital-propagated up the
    RG, Eq.53), but it is what makes the product state HIGHEST-energy so the SVD optimizer flees the
    trivial FP toward the gapless solution. WITHOUT this the run collapses to c~0.14 (trivial FP)."""
    I = np.eye(2); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)
    def k2(a, b): return np.kron(a, b)
    h2 = -2 * (k2(X, I) + k2(I, X)) / 2 - 2 * k2(Z, Z)
    ev, vec = np.linalg.eigh(h2)
    w0 = vec[:, :chi].reshape(2, 2, chi); wc0 = w0.conj()
    h3 = of_hamiltonian_3site(lam3)
    # EV negative-semidefinite shift on the physical d=2 3-site block (BEFORE lift):
    M3 = h3.reshape(8, 8); M3 = 0.5 * (M3 + M3.conj().T)
    lam_max = float(np.linalg.eigvalsh(M3).max())
    h3 = (M3 - lam_max * np.eye(8)).reshape(2, 2, 2, 2, 2, 2)
    hb2 = np.einsum("xiA,jkB,ijkpqr,xpC,qrD->ABCD", w0, w0, h3, wc0, wc0, optimize=True)
    hb2 = 0.5 * (hb2 + hb2.conj().transpose(2, 3, 0, 1))
    Ichi = np.eye(chi)
    return np.einsum("ABCD,EF->ABECDF", hb2, Ichi)


def env_iso(h, rho, w, u):
    wt = w.clone().requires_grad_(True); E = energy_net(h, rho, wt, u)
    g, = torch.autograd.grad(E, wt); return torch.conj(g)


def env_dis(h, rho, w, u):
    ut = u.clone().requires_grad_(True); E = energy_net(h, rho, w, ut)
    g, = torch.autograd.grad(E, ut); return torch.conj(g)


def descend_rho(h, rho, w, u):
    ht = h.clone().requires_grad_(True); E = energy_net(ht, rho, w, u)
    g, = torch.autograd.grad(E, ht); out = torch.conj(g)
    chi = w.shape[0]; Mx = out.reshape(chi ** 3, chi ** 3); Mx = 0.5 * (Mx + Mx.conj().T)
    return (Mx / torch.trace(Mx)).reshape((chi,) * 6)


def svd_iso(env):
    chi = env.shape[0]; U, S, Vh = torch.linalg.svd(env.reshape(chi * chi, chi), full_matrices=False)
    return (-(U @ Vh)).reshape(chi, chi, chi)


def svd_dis(env):
    chi = env.shape[0]; U, S, Vh = torch.linalg.svd(env.reshape(chi * chi, chi * chi), full_matrices=False)
    return (-(U @ Vh)).reshape(chi, chi, chi, chi)


def optimize(lam3, chi, name):
    import gc
    h0_np = lift_H(lam3, chi)
    rng = np.random.default_rng(1)
    def riso(a, b):
        Xr = rng.standard_normal((a, b)) + 1j * rng.standard_normal((a, b)); Q, _ = np.linalg.qr(Xr); return Q[:, :b]
    w_np = riso(chi * chi, chi).reshape(chi, chi, chi)
    u_np = riso(chi * chi, chi * chi).reshape(chi, chi, chi, chi)
    rho_np = (np.eye(chi ** 3) / chi ** 3).reshape((chi,) * 6)
    t0 = time.time()
    for it in range(N_IT):
        h0 = _T(h0_np); w = _T(w_np); u = _T(u_np); rho = _T(rho_np)
        w_np = svd_iso(env_iso(h0, rho, w, u)).detach().numpy()
        u_np = svd_dis(env_dis(h0, _T(rho_np), _T(w_np), u)).detach().numpy()
        for _ in range(8):
            rho_np = descend_rho(h0, _T(rho_np), _T(w_np), _T(u_np)).detach().numpy()
        if it % 25 == 0:
            E = float(torch.real(energy_net(_T(h0_np), _T(rho_np), _T(w_np), _T(u_np))))
            print(f"  [{name}] it {it}: E={E:.5f} ({time.time()-t0:.0f}s)", flush=True)
        gc.collect()
    E = float(torch.real(energy_net(_T(h0_np), _T(rho_np), _T(w_np), _T(u_np))))
    np.savez(f"uw_{name}_chi{chi}.npz", w=w_np, u=u_np, E=E)
    print(f"  [{name}] done E={E:.5f} ({time.time()-t0:.0f}s)", flush=True)
    return w_np, u_np, E


def spectrum(w_np, u_np, chi, k=24):
    D = chi ** 6; shape6 = (chi,) * 6; w = _T(w_np); u = _T(u_np)
    def mv(x):
        op = _T(x.reshape(shape6)); r = torch.zeros(shape6, dtype=torch.complex128, requires_grad=True)
        E = energy_net(op, r, w, u); g, = torch.autograd.grad(E, r); return np.conj(g.detach().numpy().reshape(D))
    lam = np.sort(np.abs(eigs(LinearOperator((D, D), matvec=mv, dtype=complex), k=k, which="LM",
                              return_eigenvectors=False)))[::-1]
    lam = lam[lam > 1e-12]; dims = -np.log2(lam); return dims - dims[0]


def central_charge(w_np, u_np, chi, n_descend=40):
    """c = 3(S(rho2)-S(rho1))/ln2 (Calabrese-Cardy; the /ln2 is essential). rho1,rho2 from the bulk
    descending fixed point. Reads 0.499 on the exact critical-Ising state (validated chi=4 session)."""
    w = _T(w_np); u = _T(u_np)
    rho = _T((np.eye(chi ** 3) / chi ** 3).reshape((chi,) * 6))
    for _ in range(n_descend):
        ot = torch.zeros((chi,) * 6, dtype=torch.complex128, requires_grad=True)
        E = energy_net(ot, rho, w, u); g, = torch.autograd.grad(E, ot)
        Mx = torch.conj(g).resolve_conj().reshape(chi ** 3, chi ** 3); Mx = 0.5 * (Mx + Mx.conj().T)
        rho = (Mx / torch.trace(Mx)).reshape((chi,) * 6)
    r3 = np.asarray(rho.detach()).reshape((chi,) * 6)
    rho2 = np.trace(r3, axis1=2, axis2=5).reshape(chi * chi, chi * chi)
    rho1 = np.trace(rho2.reshape(chi, chi, chi, chi), axis1=1, axis2=3)
    def S(r):
        ev = np.linalg.eigvalsh((r + r.conj().T) / 2); ev = ev[ev > 1e-12]; return float(-np.sum(ev * np.log(ev)))
    s1 = S(rho1)
    return 3 * (S(rho2) - s1) / np.log(2), s1


def main():
    t0 = time.time()
    print(f"SIM-2026-043: chi={CHI} universality run (operator space {CHI**6})", flush=True)
    res = {}
    wi, ui, Ei = optimize(0.0, CHI, "ISING")
    ci, s1i = central_charge(wi, ui, CHI)
    di = spectrum(wi, ui, CHI)
    print(f"  ISING c={ci:.4f} (CFT 0.5) s1={s1i:.4f}; dims: {np.round(di[:12], 4)}", flush=True)
    near2_i = [round(float(x), 3) for x in di if abs(x - 2.0) < 0.25]
    res["ising"] = {"E": Ei, "c": ci, "s1": s1i, "dims": [float(x) for x in di[:18]],
                    "Delta_T_resolution": near2_i}

    wt, ut, Et = optimize(0.856, CHI, "TCI")
    ct, s1t = central_charge(wt, ut, CHI)
    dt = spectrum(wt, ut, CHI)
    print(f"  TCI c={ct:.4f} (CFT 0.70) s1={s1t:.4f}; dims: {np.round(dt[:12], 4)}", flush=True)
    near2_t = [round(float(x), 3) for x in dt if abs(x - 2.0) < 0.25]
    res["tci"] = {"E": Et, "c": ct, "s1": s1t, "dims": [float(x) for x in dt[:18]],
                  "Delta_near_2": near2_t}

    ising_sigma = di[1] if len(di) > 1 else None
    # FULL GATE (from the T1 verification synthesis): control must pass c, sigma, AND Delta_T.
    sigma_ok = ising_sigma is not None and 0.120 <= ising_sigma <= 0.130
    c_ok = abs(ci - 0.5) < 0.05
    ctrl_T = max([x for x in di if x < 2.05], default=0)
    T_ok = ctrl_T > 1.95
    control_ok = bool(sigma_ok and c_ok and T_ok)
    verdict = (f"chi=6. Ising control: c={ci:.4f} (CFT 0.5, ok={c_ok}), sigma={ising_sigma:.4f} "
               f"(CFT 0.125, ok={sigma_ok}), Delta_T resolves to {ctrl_T:.3f} (CFT 2.0, ok={T_ok}). "
               f"GATE {'PASS' if control_ok else 'FAIL'}. "
               f"TCI: c={ct:.4f} (CFT 0.70), sigma={dt[1]:.4f} (CFT 0.075), near-2 = {near2_t}. "
               + ("CONTROL PASSED -> the TCI Delta_T number is trustworthy: a clean TCI dim in [1.8,2.2] "
                  "CONFIRMS the universal stress tensor at c=7/10 (alpha=2*Delta_T=4 universal). "
                  if control_ok else
                  "CONTROL FAILED -> chi=6 insufficient; the TCI Delta_T is NOT yet trustworthy. "
                  "Report light primaries only, escalate to chi=8."))
    res["verdict"] = verdict
    res["control_validated"] = control_ok
    out = {"id": "SIM-2026-043", "type": "classical", "date": "2026-06-18",
           "hypothesis_id": "HYP-2026-027", "chi": CHI, "results": res,
           "description": "chi=6 scale-invariant MERA scaling-dimension spectrum (plain NRG-lift, validated "
                          "at chi=4). The universality run: resolve Delta_T=2 at the TCI point (chi=4 proved "
                          "resolution-limited). Ising control = the Delta_T-resolution licensing gate.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("VERDICT:", verdict, flush=True)
    print(f"saved -> {OUT}", flush=True)


if __name__ == "__main__":
    main()
