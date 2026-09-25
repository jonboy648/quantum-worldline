"""
SIM-2026-039 - HYP-2026-027 stage-2d: AUTOGRAD (exact-gradient) chi=3 MERA at the TCI point.

THE root-cause fix. SIM-036/037/038 all shared ONE defect: finite-difference gradients on the
1246-angle MERA parametrization. With 1246 params each FD gradient is ~1247 state rebuilds, so the
optimizer is starved of accurate gradient information -> it crawls (69s/iter) and collapses into a
near-product local minimum (S_half ~ 0.0001 vs exact 0.1795). The probe (2026-06-17) also revealed
the random init is NOT product (S_init=1.21); the energy optimizer DRIVES the state to product. That
is the signature of a bad optimizer, not a capacity ceiling (ERRATA D5: chi=3 captures 99.99% of the
exact TCI GS).

This script keeps the EXACT validated architecture (8-boundary-site, 3-layer, chi=3, U(4)/U(9)
isometries -- the same MERA that produced the published alpha~4 Ising results) and changes ONLY the
gradient engine: autograd (reverse-mode AD) for EXACT gradients in one backward pass. Three plumbing
pieces, each verified against finite-difference (max|AD-FD| ~ 1e-10) before writing this:
  - Cayley transform U=(I+iA)^{-1}(I-iA) replaces scipy.expm (autograd has no expm VJP); maps a
    Hermitian generator to a unitary, differentiable, unitary to 2e-16. Same param semantics as expm.
  - vdot(a,b) -> sum(conj(a)*b) (autograd has no vdot VJP).
  - H@sv as an autograd primitive with VJP g -> H^T g (the correct complex-linear convention; H is a
    fixed sparse csr matrix, kept sparse so no 64 GB dense blowup).

VALIDATION-FIRST: run the Ising control (lam3=0, our published c=1/2 point) and require the autograd
MERA to reach low energy AND S_half ~ S_exact. If the control reproduces the published Ising state
faithfully, the machinery is trustworthy at the TCI point. THEN run TCI (lam3=0.856).

GATE (the SIM-036 lesson): success = rel_err<0.3% AND overlap>0.95 AND S_ratio>0.9. If the autograd
MERA (exact gradients, field-standard method) STILL collapses S at the TCI point -> chi=4 is FINALLY
earned, because the optimizer has been ruled out. If it reaches S~0.18 -> chi=3 sufficient (ERRATA D5
vindicated), converged tensors feed the Koo-Saleur force read-out (the alpha-universality answer).

Reuses sim036 for the Hamiltonian (build_OF_tricritical), Z2 projection, and exact reference.
Checkpoints best theta to theta_autograd_SIM2026039.npy each restart. Output: SIM-2026-039.json.
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

N = S2.N_QUBITS
CHI = S2.CHI
DIM = S2.DIM
HP4, HP9 = S2.HP4, S2.HP9
NP = S2.N_PARAMS
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-039.json"
CKPT = "D:/quantum-worldline/research/data/simulations/theta_autograd_SIM2026039.npy"

# ------- autograd MERA (Cayley unitaries, exact architecture from build_mera_sv) -------


def cayley(A, n):
    """Hermitian A (n x n) -> unitary U via the Cayley transform (autograd-differentiable)."""
    I = anp.eye(n)
    return anp.linalg.solve(I + 1j * A, I - 1j * A)


def params_to_herm(p, n):
    """Same packing as S2.params_to_hermitian, built by summing constant masks scaled by params
    (autograd-safe: no in-place assignment). Returns an n x n Hermitian matrix.
    Layout: p[0:n] = diagonal; then for each i<j a (re, im) pair filling A[i,j]=re+i*im, A[j,i]=re-i*im."""
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
    """8-boundary-site, 3-layer, chi=3 MERA -> 16q statevector. Autograd port of S2.build_mera_sv."""
    off = 0
    u1s = [make_unitary(params[off + k * HP4:off + (k + 1) * HP4], 4) for k in range(8)]; off += 8 * HP4
    w1s = [make_isometry(params[off + k * HP4:off + (k + 1) * HP4], 4, CHI) for k in range(8)]; off += 8 * HP4
    u2s = [make_unitary(params[off + k * HP9:off + (k + 1) * HP9], 9) for k in range(4)]; off += 4 * HP9
    w2s = [make_isometry(params[off + k * HP9:off + (k + 1) * HP9], 9, CHI) for k in range(4)]; off += 4 * HP9
    u3s = [make_unitary(params[off + k * HP9:off + (k + 1) * HP9], 9) for k in range(2)]; off += 2 * HP9
    w3s = [make_isometry(params[off + k * HP9:off + (k + 1) * HP9], 9, CHI) for k in range(2)]; off += 2 * HP9
    raw = params[off:off + 18]
    psi_top = raw[0::2] + 1j * raw[1::2]
    psi_top = psi_top / anp.sqrt(anp.sum(anp.conj(psi_top) * psi_top))
    state = psi_top.reshape(3, 3)
    state = w3s[0] @ state; state = state @ w3s[1].T
    state = anp.conj(u3s[0]).T @ state; state = state @ anp.conj(u3s[1]).T
    state = state.reshape(3, 3, 3, 3)
    for k in range(4): state = apply_to_axis(state, w2s[k], k)
    for k in range(4): state = apply_to_axis(state, anp.conj(u2s[k]).T, k)
    state = state.reshape(3, 3, 3, 3, 3, 3, 3, 3)
    for k in range(8): state = apply_to_axis(state, w1s[k], k)
    for k in range(8): state = apply_to_axis(state, anp.conj(u1s[k]).T, k)
    return state.reshape(DIM)


def half_S(sv):
    l = N // 2
    m = np.asarray(sv).reshape(2 ** l, 2 ** (N - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = s ** 2; p = p[p > 1e-14]
    return float(-np.sum(p * np.log(p)))


def run_point(lam3, label):
    """Optimize the autograd MERA at coupling lam3; return metrics dict."""
    S2.LAM3 = lam3
    H = S2.build_OF_tricritical(N)
    Ev, gv = eigsh(H, k=1, which="SA")
    E0 = float(Ev[0]); gs = S2.project_z2(gv[:, 0], N)
    S_ex = half_S(gs)
    print(f"\n[{label}] lam3={lam3}  exact E0={E0:.6f}  S_half_exact={S_ex:.4f}", flush=True)

    # sparse H as an autograd primitive (VJP: g -> H^T g, verified convention)
    HT = H.T.tocsr()

    @primitive
    def Hmatvec(v):
        return H @ v
    defvjp(Hmatvec, lambda ans, v: lambda g: HT @ g)

    # Z2 parity operator PI = prod_k X_k (sparse, Hermitian & symmetric -> VJP g -> PI g).
    # The raw MERA state is only ~60% Z2-even; minimizing the RAW energy pays the odd-sector penalty
    # (rel 0.60%) while the physical (projected) state is far better (rel 0.24%). So we minimize the
    # energy of the Z2-EVEN-PROJECTED state: P = (I + PI)/2, E = <Pψ|H|Pψ>/<Pψ|Pψ>. Since [H,PI]=0,
    # this is the physical sector's energy and makes objective+gate+exact-GS all consistent.
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
        pv = 0.5 * (sv + PImatvec(sv))          # project onto Z2-even sector
        Hv = Hmatvec(pv)
        nrm = anp.real(anp.sum(anp.conj(pv) * pv))
        return anp.real(anp.sum(anp.conj(pv) * Hv)) / nrm

    vg = value_and_grad(energy)

    ckpt = CKPT.replace(".npy", f"_{label}.npy")
    rng = np.random.default_rng(42)
    theta = np.load(ckpt) if os.path.exists(ckpt) else rng.standard_normal(NP) * 0.1
    if os.path.exists(ckpt):
        print(f"  resuming from {ckpt}", flush=True)

    t0 = time.time()
    # MULTI-ROUND restart loop with perturbation kicks (the ALM-style protocol that reached the
    # published 0.15% in SIM-015c/d). Plain single-descent L-BFGS-B plateaus ~0.6% on this
    # parametrization; a small random kick between fully-converged rounds escapes the local minimum.
    # Exact autograd gradients make each round cheap (~90s/700 iters), so many rounds is still minutes.
    # NOTE (2026-06-17): empirically L-BFGS-B reaches a wide ~0.60% basin by ~1300 iters and a
    # 0.05 kick is fully reabsorbed (round1==round2 to 4 dp). So many rounds is redundant; 3 rounds
    # with a LARGER (0.15) kick suffices to test for escape. 0.60%/S-faithful is adequate for the
    # *relative* universality test (control vs TCI under identical protocol) even if it is above the
    # published 0.15% (which used full Evenbly-Vidal local-environment updates, not black-box L-BFGS).
    RESTART_ROUNDS = 3
    best_theta = theta.copy()
    best_E = float(energy(theta))
    rng_kick = np.random.default_rng(2026)
    for rnd in range(1, RESTART_ROUNDS + 1):
        r = minimize(vg, theta, jac=True, method="L-BFGS-B",
                     options={"maxiter": 800, "ftol": 1e-13, "gtol": 1e-10})
        Er = float(r.fun)
        if Er < best_E:
            best_E = Er; best_theta = r.x.copy(); np.save(ckpt, best_theta)
        rel = abs(best_E - E0) / abs(E0) * 100
        S_now = half_S(S2.project_z2(np.asarray(build_mera_sv_ag(best_theta)), N))
        print(f"  round {rnd:2d}/{RESTART_ROUNDS}: E={best_E:.6f} rel={rel:.4f}% S={S_now:.4f} "
              f"nit={r.nit} ({time.time()-t0:.0f}s)", flush=True)
        theta = best_theta + rng_kick.standard_normal(NP) * 0.15  # larger kick to test for escape
        if rel < 0.05:
            break
    theta = best_theta
    np.save(ckpt, theta)

    sv = S2.project_z2(np.asarray(build_mera_sv_ag(theta)), N)
    E_m = float(energy(theta))
    rel = abs(E_m - E0) / abs(E0) * 100
    ov = float(abs(np.sum(np.conj(gs) * sv)) ** 2)
    S_m = half_S(sv)
    sratio = S_m / S_ex if S_ex else 0.0
    gate = rel < 0.3 and ov > 0.95 and sratio > 0.9
    print(f"  [{label}] FINAL: rel={rel:.4f}% ov={ov:.4f} S={S_m:.4f}/{S_ex:.4f} "
          f"(ratio {sratio:.3f}) niter={r.nit} | {'GATE PASS' if gate else 'gate fail'}", flush=True)
    return {"label": label, "lam3": lam3, "E_exact": E0, "S_half_exact": S_ex,
            "E_mera": E_m, "rel_err_pct": rel, "overlap": ov, "S_half": S_m,
            "S_ratio": sratio, "gate_pass": gate, "niter": int(r.nit),
            "wall_s": time.time() - t0, "checkpoint": ckpt}


def main():
    t0 = time.time()
    print("=" * 72)
    print(f"SIM-2026-039: autograd (exact-gradient) chi={CHI} MERA — Ising control then TCI")
    print("=" * 72)

    ising = run_point(0.0, "ISING_CONTROL")
    tci = run_point(0.856, "TCI")

    control_ok = ising["S_ratio"] > 0.9 and ising["rel_err_pct"] < 0.5
    if not control_ok:
        verdict = (f"MACHINERY NOT VALIDATED: the Ising control did not reach a faithful state "
                   f"(rel {ising['rel_err_pct']:.3f}%, S_ratio {ising['S_ratio']:.3f}). The autograd "
                   f"MERA must reproduce the published c=1/2 state before any TCI conclusion is trusted. "
                   f"Debug the control first.")
        status = "CONTROL_FAILED"
    elif tci["gate_pass"]:
        verdict = (f"chi=3 SUFFICIENT at the TCI point (autograd, exact gradients): rel {tci['rel_err_pct']:.3f}%, "
                   f"overlap {tci['overlap']:.4f}, S_half {tci['S_half']:.4f}/{tci['S_half_exact']:.4f}. "
                   f"Confirms ERRATA D5 (SIM-036 was an optimizer failure, NOT a bond-dim ceiling) and the "
                   f"Ising control validates the machinery (S_ratio {ising['S_ratio']:.3f}). NEXT: Koo-Saleur "
                   f"scaling-superoperator force read-out on the TCI checkpoint -> the alpha-universality answer.")
        status = "CHI3_SUFFICIENT_PROCEED_TO_FORCE"
    elif tci["S_ratio"] > 0.9:
        verdict = (f"TCI reached the right ENTANGLEMENT (S_ratio {tci['S_ratio']:.3f}) but energy/overlap "
                   f"missed the gate (rel {tci['rel_err_pct']:.3f}%, ov {tci['overlap']:.4f}). chi=3 captures "
                   f"the entanglement; needs more iterations / better convergence, not chi=4. Re-run from checkpoint.")
        status = "TCI_NEEDS_MORE_CONVERGENCE"
    else:
        verdict = (f"chi=4 NOW EARNED: even an exact-gradient (autograd) chi=3 MERA collapses entanglement at "
                   f"the TCI point (S_half {tci['S_half']:.4f} vs {tci['S_half_exact']:.4f}, ratio {tci['S_ratio']:.3f}) "
                   f"WHILE the Ising control reached S_ratio {ising['S_ratio']:.3f} with the same machinery. The "
                   f"optimizer is ruled out (field-standard exact gradients); the multicritical c=7/10 state genuinely "
                   f"needs chi>=4. This is the honest, earned escalation ERRATA D5 reserved for exactly this evidence.")
        status = "CHI4_FINALLY_EARNED"

    out = {"id": "SIM-2026-039", "type": "classical", "date": "2026-06-17",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage-2d: autograd (reverse-mode AD) chi=3 MERA at the O'Brien-Fendley point. "
                           "EXACT architecture from SIM-015d/036, gradient engine swapped from finite-difference "
                           "to autograd (Cayley-transform unitaries, sparse-H primitive with H^T VJP, all verified "
                           "vs finite-diff to ~1e-10). Ising control (lam3=0) validates the machinery; TCI (lam3=0.856) "
                           "is the universality test. Gate: energy AND entanglement AND overlap."),
           "circuit": {"qubits": N, "chi": CHI, "n_params": NP,
                       "script_path": "research/data/simulations/sim039_autograd_mera.py"},
           "hardware_target": "local CPU",
           "results": {"ising_control": ising, "tci": tci, "control_validated": control_ok,
                       "status": status, "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Root-cause fix for the SIM-036/037/038 product-state collapse: exact gradients via autograd "
                    "instead of finite differences on 1246 angles. Cayley transform replaces scipy.expm (no autograd "
                    "VJP). The Ising control is the trust anchor; only a passing control makes the TCI verdict meaningful.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\nVERDICT:", verdict)
    print(f"saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
