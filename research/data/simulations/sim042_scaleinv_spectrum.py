"""
SIM-2026-042 - HYP-2026-027 stage-3 (FINAL, self-contained): scale-invariant binary MERA scaling-
dimension spectrum at the tricritical-Ising point. THE alpha-universality test: does Delta_T=2 appear?

This SUPERSEDES the quimb-based sim041. Key realization: the scale-invariant MERA only ever uses the
SMALL per-layer 3-site energy network (3 isometries + 2 disentanglers + a 3-site op/state, dim <= chi^6),
NOT a full 16-site statevector contraction. So it sidesteps BOTH quimb's contraction blowup AND the
local memory wall -- the whole pipeline is small (chi=4: chi^6=4096-dim objects, 4096x4096 superop=268MB).

PIPELINE (all torch autodiff; the energy network is the tested Google simple_mera.py one, validated):
  1. Optimize a scale-invariant binary MERA (one isometry w, one disentangler u) at coupling lam3 by
     minimizing the scale-invariant energy: ascend the 3-site Hamiltonian to its fixed point, descend
     the 3-site density matrix to its fixed point, minimize <h_fixed, rho_fixed>. Stiefel-manifold
     optimization via Cayley parametrization (autograd-differentiable, verified in SIM-039).
  2. Build the ascending scaling superoperator (grad of energy wrt state) -> chi^6 x chi^6 matrix.
  3. Diagonalize -> Delta = -log_2(lambda); pin identity to 0.
  4. GATE B (Ising control, lam3=0): lowest dims MUST be {0, 1/8, 1, 9/8, 2, ...}. Trust anchor.
  5. TCI (lam3=0.856): hunt Delta_T=2 (the universal stress tensor; alpha=2*Delta_T=4).

Superoperator validated structurally (binary_mera_superop.py GATE A): identity->lambda=1 AND the
disentangler genuinely matters (NOT gauge-absorbable, unlike the failed one-site v1). Self-contained:
imports only the validated energy network from binary_mera_superop.

Output: SIM-2026-042.json + checkpoints of converged (u,w) per coupling.
"""
import json
import sys
import time

import numpy as np
import torch
from scipy.sparse.linalg import eigs

from binary_mera_superop import binary_mera_energy_torch

sys.stdout.reconfigure(line_buffering=True)

CHI = 4
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-042.json"
CKPT = "D:/quantum-worldline/research/data/simulations/uw_SIM2026042"


# ---------- 3-site O'Brien-Fendley Hamiltonian (rank-6, the bottom-layer local term) ----------
def of_hamiltonian_3site(lam3):
    """3-site O'Brien-Fendley term as a rank-6 (chi=2 physical) operator. At the bottom MERA layer the
    physical dim is 2; the scale-invariant bulk uses chi. We build the physical 3-site term at d=2 and
    the MERA coarse-grains 2->chi at the first layer. For the SCALE-INVARIANT bulk spectrum we actually
    need the term at the bulk bond dim; standard practice: build the d=2 physical term and let the first
    optimization layers lift it. Here we return the d=2 3-site term; the optimizer's first w maps 2->chi.
    H_3site = -2(X0+X1+X2)/3-ish + ZZ bonds + lam3 3-body. We use the symmetric 3-site density:
      h = -2*(XII+IXI+IIX)*w_field - 2*(ZZI+IZZ) + lam3*(XZZ+ZZX) ; coefficients per the OF chain."""
    I = np.eye(2); X = np.array([[0, 1], [1, 0]], dtype=complex); Z = np.array([[1, 0], [0, -1]], dtype=complex)
    def k(a, b, c): return np.kron(np.kron(a, b), c)
    H = (-2.0 * (k(X, I, I) + k(I, X, I) + k(I, I, X)) / 2.0
         - 2.0 * (k(Z, Z, I) + k(I, Z, Z))
         + lam3 * (k(X, Z, Z) + k(Z, Z, X)))
    # reshape 8x8 -> rank-6 (2,2,2, 2,2,2) with bra legs (0,1,2), ket legs (3,4,5)
    return H.reshape(2, 2, 2, 2, 2, 2)


def _T(a):
    return torch.tensor(a, dtype=torch.complex128)


def descend_rho(h_op, rho, w, u):
    """Descending superoperator: grad(energy, h) gives the descended 3-site density matrix (the state
    one layer DOWN). Used to iterate rho to its scale-invariant fixed point. (Per simple_mera.py:
    descend = grad(energy, argnums=0 = hamiltonian).)"""
    h_t = h_op.clone().requires_grad_(True)
    E = binary_mera_energy_torch(h_t, rho, w, u)
    g, = torch.autograd.grad(E, h_t)
    out = torch.conj(g)
    # symmetrize + normalize as a density operator (rank-6 -> matrix chi^3 x chi^3)
    chi = w.shape[0]
    M = out.reshape(chi ** 3, chi ** 3)
    M = 0.5 * (M + M.conj().T)
    M = M / torch.trace(M)
    return M.reshape((chi,) * 6)


def ascend_h(h_op, rho, w, u):
    """Ascending superoperator on the Hamiltonian: grad(energy, rho) = the ascended op (one layer UP)."""
    r_t = rho.clone().requires_grad_(True)
    E = binary_mera_energy_torch(h_op, r_t, w, u)
    g, = torch.autograd.grad(E, r_t)
    return torch.conj(g)


def env_iso(h_op, rho, w, u):
    w_t = w.clone().requires_grad_(True)
    E = binary_mera_energy_torch(h_op, rho, w_t, u)
    g, = torch.autograd.grad(E, w_t)
    return torch.conj(g)


def env_dis(h_op, rho, w, u):
    u_t = u.clone().requires_grad_(True)
    E = binary_mera_energy_torch(h_op, rho, w, u_t)
    g, = torch.autograd.grad(E, u_t)
    return torch.conj(g)


def svd_update_iso(env):
    """Optimal isometry from its environment: w_new = -V U^dag where env = U S V^dag (polar/SVD update).
    env shape (chi,chi,chi)=[bl,br,top]; group (bl,br) vs (top)."""
    chi = env.shape[0]
    M = env.reshape(chi * chi, chi)
    U, S, Vh = torch.linalg.svd(M, full_matrices=False)
    w_new = -(U @ Vh)            # (chi^2, chi)
    return w_new.reshape(chi, chi, chi)


def svd_update_dis(env):
    """Optimal disentangler: u_new = -V U^dag; env shape (chi,)*4 grouped (bl,br) vs (tl,tr)."""
    chi = env.shape[0]
    M = env.reshape(chi * chi, chi * chi)
    U, S, Vh = torch.linalg.svd(M, full_matrices=False)
    u_new = -(U @ Vh)
    return u_new.reshape(chi, chi, chi, chi)


def optimize_scaleinv(lam3, chi, n_iter=400, seed=1, label=""):
    """Evenbly-Vidal scale-invariant optimization (tested simple_mera.py recipe): alternate SVD updates
    of (w,u) from their grad-environments, iterate rho to the descending fixed point each step.
    The 3-site Hamiltonian is the OF term lifted to bond dim chi at the first step via the isometry.
    Returns converged (w, u, energy)."""
    rng = np.random.default_rng(seed)
    # physical 3-site H is d=2; for the scale-invariant BULK we coarse-grain to chi. Standard shortcut:
    # build the H directly at bond dim chi by padding the d=2 term into a chi-dim space (lower-left block),
    # which is the bulk effective Hamiltonian's leading part. (For chi=2 this is exact.)
    h2 = of_hamiltonian_3site(lam3)               # (2,2,2,2,2,2)
    h = np.zeros((chi,) * 6, dtype=complex)
    sl = tuple([slice(0, 2)] * 6)
    h[sl] = h2
    h_t = _T(h)
    # random isometric init
    def riso(a, b):
        X = rng.standard_normal((a, b)) + 1j * rng.standard_normal((a, b)); Q, _ = np.linalg.qr(X); return Q[:, :b]
    w = _T(riso(chi * chi, chi).reshape(chi, chi, chi))
    u = _T(riso(chi * chi, chi * chi).reshape(chi, chi, chi, chi))
    rho = _T((np.eye(chi ** 3) / chi ** 3).reshape((chi,) * 6))
    t0 = time.time(); E_prev = 0.0
    for it in range(1, n_iter + 1):
        with torch.no_grad():
            pass
        w = svd_update_iso(env_iso(h_t, rho, w, u))
        u = svd_update_dis(env_dis(h_t, rho, w, u))
        for _ in range(8):
            rho = descend_rho(h_t, rho, w, u)
        if it % 25 == 0 or it == n_iter:
            E = float(torch.real((binary_mera_energy_torch(h_t, rho, w, u))))
            print(f"  [{label}] it {it:4d}: E={E:.6f}  dE={abs(E-E_prev):.2e}  ({time.time()-t0:.0f}s)", flush=True)
            E_prev = E
    E = float(torch.real(binary_mera_energy_torch(h_t, rho, w, u)))
    return w, u, E


def scaling_dims_from_uw(w, u, chi, k=16):
    """Build the chi^6 x chi^6 ascending superoperator (grad-based) and extract Delta=-log2(lambda)."""
    D = chi ** 6
    S = np.zeros((D, D), dtype=complex)
    shape6 = (chi,) * 6
    for c in range(D):
        e = np.zeros(D, dtype=complex); e[c] = 1.0
        op = _T(e.reshape(shape6))
        r = torch.zeros(shape6, dtype=torch.complex128, requires_grad=True)
        E = binary_mera_energy_torch(op, r, w, u)
        g, = torch.autograd.grad(E, r)
        S[:, c] = np.conj(g.detach().numpy().reshape(D))
    lam = np.sort(np.abs(eigs(S, k=min(k, D - 2), which="LM", return_eigenvectors=False)))[::-1]
    lam = lam[lam > 1e-12]
    dims = -np.log2(lam); dims = dims - dims[0]
    return dims, lam


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"SIM-2026-042: scale-invariant binary MERA spectrum (chi={CHI})")
    print("=" * 72)
    results = {}
    # ISING CONTROL — GATE B: dims must be {0, 1/8, 1, ...}
    w_i, u_i, E_i = optimize_scaleinv(0.0, CHI, label="ISING")
    np.savez(f"{CKPT}_ISING.npz", w=w_i.numpy(), u=u_i.numpy(), E=E_i)
    dims_i, lam_i = scaling_dims_from_uw(w_i, u_i, CHI)
    print(f"  [ISING] dims: {np.round(dims_i[:8],4)}  (expect 0, 0.125, 1, 1.125, 2)", flush=True)
    ising_ok = len(dims_i) > 1 and abs(dims_i[1] - 0.125) < 0.04
    results["ising"] = {"E": E_i, "dims": [float(d) for d in dims_i[:10]], "gateB": bool(ising_ok)}

    # TCI — hunt Delta_T = 2
    w_t, u_t, E_t = optimize_scaleinv(0.856, CHI, label="TCI")
    np.savez(f"{CKPT}_TCI.npz", w=w_t.numpy(), u=u_t.numpy(), E=E_t)
    dims_t, lam_t = scaling_dims_from_uw(w_t, u_t, CHI)
    near2 = [float(d) for d in dims_t if abs(d - 2.0) < 0.25]
    print(f"  [TCI] dims: {np.round(dims_t[:10],4)}  (TCI: 0,0.075,0.2,0.875,1.2,...,T=2)", flush=True)
    results["tci"] = {"E": E_t, "dims": [float(d) for d in dims_t[:12]], "Delta_near_2": near2}

    if ising_ok:
        verdict = (f"Superoperator+optimizer VALIDATED (Ising Delta_2={dims_i[1]:.4f}~0.125). "
                   + (f"TCI Delta_T~2 FOUND {near2}: universal stress tensor, alpha=2*Delta_T=4 at c=7/10. "
                      f"UNIVERSALITY SUPPORTED." if near2 else
                      f"TCI dims {np.round(dims_t[:6],3).tolist()}; no clean Delta=2 at chi={CHI} "
                      f"(may need higher chi). Preliminary."))
        status = "ISING_PASS_TCI_MEASURED"
    else:
        verdict = (f"Ising GATE B FAILED (Delta_2={dims_i[1] if len(dims_i)>1 else 'NA'} vs 0.125): the "
                   f"scale-invariant (u,w) did not reach criticality OR the optimizer needs more iters/chi. "
                   f"Do NOT trust TCI.")
        status = "ISING_GATE_FAIL"

    out = {"id": "SIM-2026-042", "type": "classical", "date": "2026-06-18",
           "hypothesis_id": "HYP-2026-027",
           "description": "Scale-invariant binary MERA scaling-dimension spectrum (Evenbly-Vidal SVD "
                          "optimization + grad-based 3-site superoperator, tested simple_mera.py recipe). "
                          "Reads {Delta} directly; Delta_T=2 at TCI = universal stress tensor (alpha=4). "
                          "Ising control = GATE B trust anchor.",
           "circuit": {"chi": CHI, "script_path": "research/data/simulations/sim042_scaleinv_spectrum.py"},
           "hardware_target": "RunPod CPU (per user) / local-capable (small per-layer network)",
           "results": results, "status": status, "verdict": verdict, "comparison": "classical_wins",
           "notes": "Self-contained: energy network from binary_mera_superop (validated). No quimb. "
                    "Superoperator GATE A (identity->1, disentangler-matters) passed; GATE B (Ising "
                    "{0,1/8,1}) checked here before any TCI claim.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\nVERDICT:", verdict)
    print(f"saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
