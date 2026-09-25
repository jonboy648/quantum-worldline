"""
SIM-2026-040 - HYP-2026-027 stage-2e: chi=4 autograd MERA at the tricritical-Ising point.

SIM-039 RESOLVED the representability question: with exact autograd gradients + the Z2-projected-
energy objective (control-validated, Ising S_ratio 1.040 GATE PASS), a chi=3 MERA reaches the TCI
ground state at rel 0.088% / overlap 0.994 BUT captures only S_ratio=0.745 of the half-chain
entanglement -- the c=7/10 multicritical Schmidt tail exceeds a 3-dim bond. The SIM-036 "collapse"
was a pure optimizer artifact (ERRATA D5 vindicated); chi=4 is now EARNED on a sound footing.

This script generalizes the EXACT SIM-039 autograd machinery to arbitrary CHI (here 4):
  - Cayley-transform unitaries (autograd-differentiable; scipy.expm has no autograd VJP).
  - sparse-H matvec primitive with VJP g -> H^T g (verified convention).
  - Z2-PROJECTED-energy objective (parity primitive PI=prod X_k; minimize <Pψ|H|Pψ>/<Pψ|Pψ>).
  - multi-round L-BFGS-B with perturbation kicks.
All dimensions are parametrized by CHI and S2D=CHI**2 (the merged-pair dim): layer-1 disentanglers
are U(4) on physical pairs (2x2), layer-1 isometries map 4->CHI; layers 2-3 disentanglers are
U(S2D) on CHI-pairs, isometries map S2D->CHI; the top tensor is (CHI,CHI). At CHI=4: ~3360 params
(vs 1246 at chi=3), still trivial with exact gradients.

Ising control (lam3=0) first to re-validate the machinery AT chi=4; then TCI (lam3=0.856).
GATE: rel<0.3% AND overlap>0.95 AND S_ratio>0.9. If chi=4 clears the entanglement gate at TCI ->
chi=4 IS sufficient; the converged state feeds the stress-tensor force read-out (the alpha-
universality answer). If chi=4 ALSO undershoots S -> escalate further / reconsider the observable.

Reuses sim036 for the Hamiltonian + Z2 projection + exact reference. Checkpoints per point.
Output: research/data/simulations/SIM-2026-040.json.
"""
import json
import os
import sys
import time

import autograd.numpy as anp
import numpy as np
from autograd import value_and_grad
from autograd.extend import defvjp, primitive
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh

import sim036_tci_mera_stage2 as S2

sys.stdout.reconfigure(line_buffering=True)

N = S2.N_QUBITS           # 16 physical sites
CHI = 4                   # bond dimension (this run)
S2D = CHI * CHI           # merged-pair dimension for layers 2-3
DIM = 2 ** N
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-040.json"
CKPT = "D:/quantum-worldline/research/data/simulations/theta_chi4_SIM2026040.npy"

# ---- parameter layout (all CHI-dependent) ----
HP4 = 16                  # U(4) Hermitian generator params (layer-1 disentanglers, physical pairs)
HPS = S2D * S2D           # U(S2D) Hermitian generator params (layer 2-3 disentanglers): 256 at chi=4
# layer1: 8 disentanglers U(4) + 8 isometries (4->CHI, parametrized as U(4) then sliced) = 16*HP4
# layer2: 4 disentanglers U(S2D) + 4 isometries (S2D->CHI, U(S2D) sliced) = 8*HPS
# layer3: 2 disentanglers U(S2D) + 2 isometries (S2D->CHI) = 4*HPS
# top: (CHI,CHI) complex = 2*CHI*CHI reals
N_TOP = 2 * CHI * CHI
N_PARAMS = 16 * HP4 + 8 * HPS + 4 * HPS + N_TOP


def cayley(A, n):
    I = anp.eye(n)
    return anp.linalg.solve(I + 1j * A, I - 1j * A)


def params_to_herm(p, n):
    A = anp.diag(p[:n]) + 0j
    k = n
    for i in range(n):
        for j in range(i + 1, n):
            Eij = np.zeros((n, n)); Eij[i, j] = 1.0
            Eji = np.zeros((n, n)); Eji[j, i] = 1.0
            A = A + (p[k] + 1j * p[k + 1]) * Eij + (p[k] - 1j * p[k + 1]) * Eji
            k += 2
    return A


def make_unitary(p, n):
    return cayley(params_to_herm(p, n), n)


def make_isometry(p, n_big, n_small):
    return make_unitary(p, n_big)[:, :n_small]


def apply_to_axis(tensor, matrix, axis):
    return anp.moveaxis(anp.tensordot(matrix, tensor, axes=([1], [axis])), 0, axis)


def build_mera_sv_ag(params):
    """8-boundary-site, 3-layer, chi=CHI MERA -> 16q statevector. CHI-generalized SIM-039 builder
    (EXACT same single-axis-contraction topology as sim039/sim036; only 3->CHI, 9->S2D, 18->N_TOP).
    Each axis carries a merged-pair dim: layer-1 axes are dim 4 (=2x2 physical), layer-2/3 axes are
    dim S2D (=CHI x CHI). Disentanglers are full unitaries on those merged-pair axes; isometries map
    the merged-pair dim down to CHI. This is the validated topology with dimensions widened."""
    off = 0
    u1s = [make_unitary(params[off + k * HP4:off + (k + 1) * HP4], 4) for k in range(8)]; off += 8 * HP4
    w1s = [make_isometry(params[off + k * HP4:off + (k + 1) * HP4], 4, CHI) for k in range(8)]; off += 8 * HP4
    u2s = [make_unitary(params[off + k * HPS:off + (k + 1) * HPS], S2D) for k in range(4)]; off += 4 * HPS
    w2s = [make_isometry(params[off + k * HPS:off + (k + 1) * HPS], S2D, CHI) for k in range(4)]; off += 4 * HPS
    u3s = [make_unitary(params[off + k * HPS:off + (k + 1) * HPS], S2D) for k in range(2)]; off += 2 * HPS
    w3s = [make_isometry(params[off + k * HPS:off + (k + 1) * HPS], S2D, CHI) for k in range(2)]; off += 2 * HPS
    raw = params[off:off + N_TOP]
    psi_top = raw[0::2] + 1j * raw[1::2]
    psi_top = psi_top / anp.sqrt(anp.sum(anp.conj(psi_top) * psi_top))
    state = psi_top.reshape(CHI, CHI)
    state = w3s[0] @ state; state = state @ w3s[1].T               # (S2D, S2D)
    state = anp.conj(u3s[0]).T @ state; state = state @ anp.conj(u3s[1]).T
    state = state.reshape(CHI, CHI, CHI, CHI)                      # 4 axes, dim CHI
    for k in range(4): state = apply_to_axis(state, w2s[k], k)     # axis k: CHI -> S2D
    for k in range(4): state = apply_to_axis(state, anp.conj(u2s[k]).T, k)  # disentangle dim-S2D axis
    state = state.reshape(*([CHI] * 8))                            # 8 axes, dim CHI
    for k in range(8): state = apply_to_axis(state, w1s[k], k)     # axis k: CHI -> 4 (physical pair)
    for k in range(8): state = apply_to_axis(state, anp.conj(u1s[k]).T, k)  # disentangle dim-4 axis
    return state.reshape(DIM)


def half_S(sv):
    l = N // 2
    m = np.asarray(sv).reshape(2 ** l, 2 ** (N - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


def run_point(lam3, label):
    S2.LAM3 = lam3
    H = S2.build_OF_tricritical(N)
    Ev, gv = eigsh(H, k=1, which="SA")
    E0 = float(Ev[0]); gs = S2.project_z2(gv[:, 0], N)
    S_ex = half_S(gs)
    print(f"\n[{label}] lam3={lam3}  exact E0={E0:.6f}  S_half_exact={S_ex:.4f}  (chi={CHI}, {N_PARAMS} params)", flush=True)

    HT = H.T.tocsr()

    @primitive
    def Hmatvec(v):
        return H @ v
    defvjp(Hmatvec, lambda ans, v: lambda g: HT @ g)

    PI = S2.sp(N, 0, "X")
    for k in range(1, N):
        PI = PI @ S2.sp(N, k, "X")
    PI = PI.tocsr()

    @primitive
    def PImatvec(v):
        return PI @ v
    defvjp(PImatvec, lambda ans, v: lambda g: PI @ g)

    def energy(p):
        sv = build_mera_sv_ag(p)
        pv = 0.5 * (sv + PImatvec(sv))
        Hv = Hmatvec(pv)
        nrm = anp.real(anp.sum(anp.conj(pv) * pv))
        return anp.real(anp.sum(anp.conj(pv) * Hv)) / nrm

    vg = value_and_grad(energy)

    ckpt = CKPT.replace(".npy", f"_{label}.npy")
    rng = np.random.default_rng(42)
    theta = np.load(ckpt) if os.path.exists(ckpt) else rng.standard_normal(N_PARAMS) * 0.1
    if os.path.exists(ckpt):
        print(f"  resuming from {ckpt}", flush=True)

    t0 = time.time()
    RESTART_ROUNDS = 4
    best_theta = theta.copy(); best_E = float(energy(theta))
    rng_kick = np.random.default_rng(2026)
    for rnd in range(1, RESTART_ROUNDS + 1):
        r = minimize(vg, theta, jac=True, method="L-BFGS-B",
                     options={"maxiter": 1000, "ftol": 1e-13, "gtol": 1e-10})
        if float(r.fun) < best_E:
            best_E = float(r.fun); best_theta = r.x.copy(); np.save(ckpt, best_theta)
        rel = abs(best_E - E0) / abs(E0) * 100
        S_now = half_S(S2.project_z2(np.asarray(build_mera_sv_ag(best_theta)), N))
        print(f"  round {rnd}/{RESTART_ROUNDS}: E={best_E:.6f} rel={rel:.4f}% S={S_now:.4f} "
              f"nit={r.nit} ({time.time()-t0:.0f}s)", flush=True)
        theta = best_theta + rng_kick.standard_normal(N_PARAMS) * 0.15
        if rel < 0.05:
            break
    theta = best_theta; np.save(ckpt, theta)

    sv = S2.project_z2(np.asarray(build_mera_sv_ag(theta)), N)
    E_m = float(energy(theta))
    rel = abs(E_m - E0) / abs(E0) * 100
    ov = float(abs(np.sum(np.conj(gs) * sv)) ** 2)
    S_m = half_S(sv)
    sratio = S_m / S_ex if S_ex else 0.0
    gate = rel < 0.3 and ov > 0.95 and sratio > 0.9
    print(f"  [{label}] FINAL: rel={rel:.4f}% ov={ov:.4f} S={S_m:.4f}/{S_ex:.4f} "
          f"(ratio {sratio:.3f}) | {'GATE PASS' if gate else 'gate fail'}", flush=True)
    return {"label": label, "lam3": lam3, "E_exact": E0, "S_half_exact": S_ex, "E_mera": E_m,
            "rel_err_pct": rel, "overlap": ov, "S_half": S_m, "S_ratio": sratio,
            "gate_pass": gate, "niter": int(r.nit), "wall_s": time.time() - t0, "checkpoint": ckpt}


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"SIM-2026-040: chi={CHI} autograd MERA — Ising control then TCI (HYP-027 universality)")
    print("=" * 72)
    ising = run_point(0.0, "ISING_CONTROL")
    tci = run_point(0.856, "TCI")

    control_ok = ising["S_ratio"] > 0.9 and ising["rel_err_pct"] < 0.5
    if not control_ok:
        verdict = (f"chi=4 MACHINERY NOT VALIDATED: Ising control rel {ising['rel_err_pct']:.3f}%, "
                   f"S_ratio {ising['S_ratio']:.3f}. Debug before trusting TCI.")
        status = "CONTROL_FAILED"
    elif tci["gate_pass"]:
        verdict = (f"chi=4 SUFFICIENT at the TCI point: rel {tci['rel_err_pct']:.3f}%, overlap "
                   f"{tci['overlap']:.4f}, S_half {tci['S_half']:.4f}/{tci['S_half_exact']:.4f} "
                   f"(ratio {tci['S_ratio']:.3f}). chi=3 missed ~26% of the entanglement (SIM-039 "
                   f"S_ratio 0.745); chi=4 captures it. Control validated (S_ratio {ising['S_ratio']:.3f}). "
                   f"NEXT: stress-tensor force read-out on the chi=4 TCI state -> the alpha-universality answer.")
        status = "CHI4_SUFFICIENT_PROCEED_TO_FORCE"
    elif tci["S_ratio"] > ising["S_ratio"] - 0.1 and tci["S_ratio"] > 0.85:
        verdict = (f"chi=4 NEARLY sufficient at TCI (S_ratio {tci['S_ratio']:.3f} vs chi=3's 0.745); "
                   f"close to the gate (rel {tci['rel_err_pct']:.3f}%, ov {tci['overlap']:.4f}). More "
                   f"rounds or a small chi bump may finish it; re-run from checkpoint.")
        status = "CHI4_NEARLY_SUFFICIENT"
    else:
        verdict = (f"chi=4 STILL undershoots TCI entanglement (S_ratio {tci['S_ratio']:.3f} vs chi=3 0.745; "
                   f"control {ising['S_ratio']:.3f}). The c=7/10 state needs chi>=5 OR the per-layer MERA is "
                   f"the wrong tool for a clean force read-out (scale-invariant MERA may be required, per SIM-035).")
        status = "CHI4_INSUFFICIENT_RECONSIDER"

    out = {"id": "SIM-2026-040", "type": "classical", "date": "2026-06-17",
           "hypothesis_id": "HYP-2026-027",
           "description": (f"Stage-2e: chi={CHI} autograd MERA at the O'Brien-Fendley point. CHI-generalized "
                           f"SIM-039 machinery (Cayley unitaries, sparse-H + parity primitives, Z2-projected "
                           f"energy, restart loop). Tests whether chi=4 captures the c=7/10 entanglement that "
                           f"chi=3 missed (SIM-039 S_ratio 0.745). Ising control validates; TCI is the test."),
           "circuit": {"qubits": N, "chi": CHI, "n_params": N_PARAMS,
                       "script_path": "research/data/simulations/sim040_chi4_tci_mera.py"},
           "hardware_target": "local CPU",
           "results": {"ising_control": ising, "tci": tci, "control_validated": control_ok,
                       "status": status, "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Follows SIM-039 (chi=3: energy-faithful, S_ratio 0.745). chi=4 is the earned escalation on "
                    "a control-validated, optimizer-ruled-out footing. Same exact-gradient autograd machinery, "
                    "bond 3->4 (1246->~3360 params).",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\nVERDICT:", verdict)
    print(f"saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
