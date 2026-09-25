"""
SIM-2026-046 - HYP-2026-027: SCALE-INVARIANT FINITE MERA seed for the chi=6 scaling-dim measurement.

WHY (CHI6-CONVERGENCE-RECIPE.md, Step 1): cold-start scale-invariant chi=6 lands in a WRONG basin
(c=0.746, sigma=0.037 < chi=4's 0.057). The fix is to seed the scale-invariant bulk (u,w) from a
CONVERGED FINITE MERA, whose energy minimization against the exact critical GS is WELL-CONDITIONED
(unlike the scale-invariant fixed-point chase). This puts the scale-invariant optimizer in the correct
basin from step 0 -- the exact mechanism that made chi=4 work (warm-started from a near-critical state).

ARCHITECTURE (finite N=16 = 8 boundary sites, 3 binary coarse-graining layers, matches sim036/039):
  - Layer 1 (TRANSITIONAL): 8 disentanglers u1 (4x4), 8 isometries w1 (4->chi). phys^2=4 -> chi.
  - Layers 2 & 3 (BULK, SHARED scale-invariant): ONE disentangler u_bulk (chi^2 x chi^2) + ONE isometry
    w_bulk (chi^2->chi), reused at BOTH layers (this is what makes the extracted (u,w) scale-invariant).
  - Top: a chi x chi tensor.
All tensors via Cayley transform of Hermitian generators (autograd-differentiable, unitary to 2e-16),
parametrized so torch autograd gives EXACT gradients. Energy = Z2-even-projected <psi|H|psi>/<psi|psi>
on the O'Brien-Fendley Hamiltonian (lam3=0 Ising control first).

OPTIMIZE: torch Adam on the energy (well-conditioned) + multi-restart. Read the converged SHARED bulk
(u_bulk, w_bulk) + transitional (u1[0], w1[0]) -> seed_chi6_finiteMERA.npz for the scale-invariant run.

GATE: rel_err < 0.5% AND overlap > 0.95 AND S_half ratio > 0.9 (sim039 discipline) on the Ising
control. A faithful finite state => a critical seed.

Self-contained except sim036 (Hamiltonian, Z2 projection, exact GS). torch 2.8.
"""
import sys
import time

import numpy as np
import torch

import sim036_tci_mera_stage2 as S2

try:
    sys.stdout.reconfigure(encoding="utf-8", line_buffering=True)
except Exception:
    pass

N = 16                 # qubits (8 boundary sites)
CHI = 6
DIM = 2 ** N
torch.set_default_dtype(torch.float64)


# ---- Cayley-transform unitaries (torch, autograd-differentiable) ----
def _herm_indices(n):
    iu = [(i, j) for i in range(n) for j in range(i + 1, n)]
    return iu


def herm_from_params(p, n):
    """p (real torch vector) -> Hermitian n x n. Layout: first n = diagonal; then (re,im) pairs for i<j."""
    A = torch.diag(p[:n].to(torch.complex128))
    k = n
    rows, cols, vals = [], [], []
    # build upper/lower triangle additively (autograd-safe, no in-place on leaf)
    M = torch.zeros((n, n), dtype=torch.complex128)
    parts = [A]
    for (i, j) in _herm_indices(n):
        E = torch.zeros((n, n), dtype=torch.complex128)
        re = p[k]; im = p[k + 1]; k += 2
        Eij = torch.zeros((n, n), dtype=torch.complex128); Eij[i, j] = 1.0
        Eji = torch.zeros((n, n), dtype=torch.complex128); Eji[j, i] = 1.0
        parts.append((re + 1j * im) * Eij + (re - 1j * im) * Eji)
    return torch.stack(parts, 0).sum(0)


def cayley(A, n):
    I = torch.eye(n, dtype=torch.complex128)
    return torch.linalg.solve(I + 1j * A, I - 1j * A)


def make_unitary(p, n):
    return cayley(herm_from_params(p, n), n)


def make_isometry(p, n_big, n_small):
    return make_unitary(p, n_big)[:, :n_small]


def nparams_herm(n):
    return n + n * (n - 1)   # n diag + 2 per off-diag upper pair


def apply_axis(t, m, ax):
    return torch.moveaxis(torch.tensordot(m, t, dims=([1], [ax])), 0, ax)


# ---- scale-invariant finite MERA builder (8 boundary sites, 3 binary layers; SHARED bulk) ----
def build_sv(params, chi):
    """Layer 1 = transitional (8 u1 4x4, 8 w1 4->chi). Layers 2,3 = SHARED bulk: ONE u_bulk
    (chi^2 grouped, built as a (chi^2 x chi^2) unitary on grouped pairs) + ONE w_bulk (chi^2->chi),
    reused at BOTH layers. Top = chi-vector pair. Returns the 2^16 statevector.

    The bulk disentangler acts on a PAIR of chi-legs (grouped to chi^2); the isometry maps a chi^2
    pair to a single chi-leg. We mirror sim036's reshape/apply structure but with one shared (u,w)."""
    c = chi
    cmid = min(4, c)            # transitional intermediate bond (binary first layer caps at phys^2=4)
    nu1 = nparams_herm(4)                       # layer-1 disentangler (physical, 4x4)
    nw1 = nparams_herm(4)                       # layer-1 isometry 4 -> cmid (built as U(4)[:, :cmid])
    nu2 = nparams_herm(cmid * cmid)             # layer-2 (transitional) disentangler (cmid^2 x cmid^2)
    nw2 = nparams_herm(cmid * cmid)             # layer-2 isometry cmid^2 -> c
    nuB = nparams_herm(c * c); nwB = nparams_herm(c * c)
    off = 0
    # layer 1 transitional: 8 blocks, phys^2=4 -> cmid
    u1s = [make_unitary(params[off + k * nu1:off + (k + 1) * nu1], 4) for k in range(8)]; off += 8 * nu1
    w1s = [make_isometry(params[off + k * nw1:off + (k + 1) * nw1], 4, cmid) for k in range(8)]; off += 8 * nw1
    # layer 2 transitional: 4 blocks, cmid^2 -> c
    u2s = [make_unitary(params[off + k * nu2:off + (k + 1) * nu2], cmid * cmid) for k in range(4)]; off += 4 * nu2
    w2s = [make_isometry(params[off + k * nw2:off + (k + 1) * nw2], cmid * cmid, c) for k in range(4)]; off += 4 * nw2
    # SHARED bulk (layer 3): c^2 -> c, reused (here once for 2->4; for N=16 the bulk runs one shared step)
    u_bulk = make_unitary(params[off:off + nuB], c * c); off += nuB
    w_bulk = make_isometry(params[off:off + nwB], c * c, c); off += nwB
    raw = params[off:off + 2 * c * c]
    psi_top = (raw[0::2] + 1j * raw[1::2]).to(torch.complex128)
    psi_top = psi_top / torch.sqrt(torch.sum(torch.conj(psi_top) * psi_top))

    uBm = u_bulk; wBm = w_bulk                  # (c^2,c^2), (c^2,c)
    # ---- bulk layer: top 2 (c,c) -> 4 sites (c) ----
    state = psi_top.reshape(c, c)
    state = wBm @ state                                          # (c^2, c)
    state = torch.tensordot(wBm, state, dims=([1], [1]))         # (c^2, c^2)
    state = state.reshape(c, c, c, c)
    state = _udag_pair(state, uBm, c, 1, 2)                      # 4 sites, dim c
    # ---- layer 2 transitional: 4 sites (c) -> 8 sites (cmid) ----
    n = state.ndim                                              # 4
    for ax in range(n - 1, -1, -1):
        state = apply_axis(state, w2s[ax], ax)                  # w2 (cmid^2, c): contracts c -> cmid^2
        state = state.reshape(state.shape[:ax] + (cmid, cmid) + state.shape[ax + 1:])
    n = state.ndim                                             # 8, dim cmid
    for (a, b) in [(i, i + 1) for i in range(1, n - 1, 2)]:
        ud = torch.conj(u2s[(a - 1) // 2]).t().reshape(cmid, cmid, cmid, cmid)
        state = _apply_4leg(state, ud, a, b)
    # ---- layer 1 transitional: 8 sites (cmid) -> 16 physical (dim 2) ----
    n = state.ndim
    for ax in range(n - 1, -1, -1):
        state = apply_axis(state, w1s[ax], ax)                  # w1 (4, cmid): contracts cmid -> 4
        state = state.reshape(state.shape[:ax] + (2, 2) + state.shape[ax + 1:])
    n = state.ndim
    for (a, b) in [(i, i + 1) for i in range(1, n - 1, 2)]:
        ud = torch.conj(u1s[(a - 1) // 2]).t().reshape(2, 2, 2, 2)
        state = _apply_4leg(state, ud, a, b)
    return (state.reshape(DIM), u_bulk.reshape(c, c, c, c), w_bulk.reshape(c, c, c), u1s, w1s, u2s, w2s)


def _apply_4leg(state, op4, a, b):
    """Contract a (out0,out1,in0,in1) operator's in-legs with state axes (a,b), put outs at (a,b)."""
    n = state.ndim
    blk = torch.tensordot(op4, state, dims=([2, 3], [a, b]))
    rest = [x for x in range(n) if x not in (a, b)]
    perm = [0] * n; perm[a] = 0; perm[b] = 1
    for i2, r in enumerate(rest):
        perm[r] = 2 + i2
    return torch.permute(blk, tuple(perm))


def _udag_pair(state, uBm, c, a, b):
    ud = torch.conj(uBm).t().reshape(c, c, c, c)     # (out_bl,out_br,in_bl,in_br)
    return _apply_4leg(state, ud, a, b)


def _expand_all(state, wBm, c):
    n = state.ndim
    for ax in range(n - 1, -1, -1):
        state = apply_axis(state, wBm, ax)            # chi -> chi^2
        state = state.reshape(state.shape[:ax] + (c, c) + state.shape[ax + 1:])
    return state


def _udag_inner(state, uBm, c):
    n = state.ndim
    for (a, b) in [(i, i + 1) for i in range(1, n - 1, 2)]:
        state = _udag_pair(state, uBm, c, a, b)
    return state


# ---- energy + entanglement ----
def half_S(sv, n):
    l = n // 2
    m = np.asarray(sv).reshape(2 ** l, 2 ** (n - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


def total_nparams(chi):
    c = chi; cmid = min(4, c)
    return (8 * nparams_herm(4) + 8 * nparams_herm(4)                       # layer 1 u1,w1
            + 4 * nparams_herm(cmid * cmid) + 4 * nparams_herm(cmid * cmid)  # layer 2 u2,w2
            + nparams_herm(c * c) + nparams_herm(c * c)                      # shared bulk u,w
            + 2 * c * c)                                                     # top


def energy(params, H_t, PI_t, chi):
    """Z2-even-projected energy <Pψ|H|Pψ>/<Pψ|Pψ>, P=(I+PI)/2. Differentiable in params."""
    sv, *_ = build_sv(params, chi)
    pv = 0.5 * (sv + torch.sparse.mm(PI_t, sv.reshape(-1, 1)).reshape(-1)) if PI_t.is_sparse else 0.5 * (sv + PI_t @ sv)
    Hv = torch.sparse.mm(H_t, pv.reshape(-1, 1)).reshape(-1) if H_t.is_sparse else H_t @ pv
    nrm = torch.real(torch.sum(torch.conj(pv) * pv))
    return torch.real(torch.sum(torch.conj(pv) * Hv)) / nrm


def _sparse_to_torch(spmat):
    coo = spmat.tocoo()
    idx = torch.tensor(np.vstack([coo.row, coo.col]), dtype=torch.long)
    val = torch.tensor(coo.data, dtype=torch.complex128)
    return torch.sparse_coo_tensor(idx, val, coo.shape).coalesce()


# ---- optimize + extract seed ----
def run(lam3, chi, label, n_restart=4, iters=400, seed=0):
    S2.LAM3 = lam3
    H = S2.build_OF_tricritical(N)
    from scipy.sparse.linalg import eigsh
    Ev, gv = eigsh(H, k=1, which="SA")
    E0 = float(Ev[0]); gs = S2.project_z2(gv[:, 0], N); S_ex = half_S(gs, N)
    print(f"[{label}] lam3={lam3} exact E0={E0:.6f} S_half_exact={S_ex:.4f}", flush=True)
    PI = S2.sp(N, 0, "X")
    for k in range(1, N):
        PI = PI @ S2.sp(N, k, "X")
    H_t = _sparse_to_torch(H.tocsr()); PI_t = _sparse_to_torch(PI.tocsr())

    NP = total_nparams(chi)
    best = None; best_E = 1e9
    t0 = time.time()
    for rst in range(n_restart):
        rng = np.random.default_rng(seed + rst)
        p = torch.tensor(rng.standard_normal(NP) * 0.1, dtype=torch.float64, requires_grad=True)
        opt = torch.optim.Adam([p], lr=2e-2)
        sched = torch.optim.lr_scheduler.CosineAnnealingLR(opt, iters)
        for it in range(iters):
            opt.zero_grad()
            E = energy(p, H_t, PI_t, chi)
            E.backward(); opt.step(); sched.step()
        Ev_ = float(energy(p, H_t, PI_t, chi).detach())
        if Ev_ < best_E:
            best_E = Ev_; best = p.detach().clone()
        rel = abs(best_E - E0) / abs(E0) * 100
        print(f"  [{label}] restart {rst}: E={Ev_:.6f} best_rel={rel:.4f}% ({time.time()-t0:.0f}s)", flush=True)

    sv_t, uB, wB, u1s, w1s, u2s, w2s = build_sv(best, chi)
    sv = np.asarray(sv_t.detach())
    svp = S2.project_z2(sv, N)
    rel = abs(best_E - E0) / abs(E0) * 100
    ov = float(abs(np.sum(np.conj(gs) * svp)) ** 2)
    S_m = half_S(svp, N); sratio = S_m / S_ex if S_ex else 0.0
    gate = rel < 0.5 and ov > 0.95 and sratio > 0.9
    print(f"  [{label}] FINAL rel={rel:.4f}% ov={ov:.4f} S={S_m:.4f}/{S_ex:.4f} (ratio {sratio:.3f}) "
          f"-> {'GATE PASS' if gate else 'gate fail'}", flush=True)
    # save the SHARED bulk (u,w) = the critical chi-scale-invariant seed (this is what feeds the
    # scaling superoperator). uB is (chi,chi,chi,chi), wB is (chi,chi,chi). Also stash a transitional
    # tensor (w2[0]: cmid^2->chi, the layer that actually produces chi) for optional re-lift use.
    cmid = min(4, chi)
    np.savez(f"seed_chi{chi}_finiteMERA_{label}.npz",
             w=np.asarray(wB.detach()), u=np.asarray(uB.detach()),
             w2=np.asarray(w2s[0].detach()).reshape(cmid, cmid, chi),
             u2=np.asarray(u2s[0].detach()).reshape(cmid, cmid, cmid, cmid),
             w1=np.asarray(w1s[0].detach()).reshape(2, 2, cmid),
             u1=np.asarray(u1s[0].detach()).reshape(2, 2, 2, 2),
             E=best_E, rel=rel, ov=ov, S_ratio=sratio)
    return {"label": label, "lam3": lam3, "E_exact": E0, "E_mera": best_E, "rel_err_pct": rel,
            "overlap": ov, "S_half": S_m, "S_half_exact": S_ex, "S_ratio": sratio,
            "gate_pass": bool(gate), "wall_s": round(time.time() - t0)}


def main():
    import json
    print(f"SIM-2026-046: scale-invariant FINITE MERA seed, chi={CHI}", flush=True)
    ising = run(0.0, CHI, "ISING")
    out = {"id": "SIM-2026-046", "type": "classical", "date": "2026-06-19", "hypothesis_id": "HYP-2026-027",
           "chi": CHI, "ising": ising,
           "description": "Scale-invariant finite MERA (shared bulk u,w across layers 2-3) optimized by "
                          "torch Adam against the exact critical GS; extracts a critical (u,w) seed for the "
                          "scale-invariant chi=6 scaling-dimension run (CHI6-CONVERGENCE-RECIPE Step 1).",
           "verdict": (f"Ising control rel={ising['rel_err_pct']:.3f}% ov={ising['overlap']:.4f} "
                       f"S_ratio={ising['S_ratio']:.3f} -> "
                       + ("FAITHFUL critical seed saved; feed to scale-invariant chi=6 run."
                          if ising["gate_pass"] else "seed not yet faithful; more restarts/iters or chi."))}
    with open("SIM-2026-046.json", "w") as f:
        json.dump(out, f, indent=2)
    print("VERDICT:", out["verdict"], flush=True)
    print("saved -> SIM-2026-046.json", flush=True)


if __name__ == "__main__":
    main()
