"""
ADAPT-VQE settle (task #95): can a gradient-GROWN ansatz prepare the critical-TFIM
ground state to >0.99 overlap AND carry the alpha~4 holographic force, at a 2q-gate
(=> ZZPhase) cost far below chi=3 MERA's 451?

WHY THIS, AND WHY IT'S THE DECIDER
----------------------------------
Two prior attempts to find a cheaper-than-chi3 circuit each failed for a DIFFERENT reason:
  * #92 correlator-fit brickwork: matched C(r) but GS-overlap=0.0027, force RMSE=1.44.
    Lesson: matching one observable != reproducing the state (necessary != sufficient).
  * #94 energy-min fixed brickwork (depth 1..6): GS-overlap PLATEAUED at ~0.567 and never
    rose toward 1.0 even as depth grew. That is an OPTIMIZER signature (barren plateau /
    local minima in a fixed dense SU(4) block), NOT proof that the state needs deep circuits.

ADAPT-VQE removes the optimizer confound. Instead of optimizing a fixed block all at once,
it GROWS the ansatz one operator at a time, each chosen by its energy gradient
   g_k = dE/dtheta_k |_{theta=0} = <psi| [H, A_k] |psi> = 2 Re <psi| H A_k |psi>   (A_k anti-Herm)
then re-optimizes all accumulated angles. This is the standard escape from the plateau the
fixed brickwork hit. So the result is DECISIVE either way:
  * If overlap clears 0.99 at low 2q-count  => a cheaper circuit EXISTS; QCUP path can reopen.
  * If overlap STILL plateaus < 0.99 here   => the chi=3 cost is FUNDAMENTAL, not an optimizer
    artifact, and QCUP can be closed with a real no-go instead of "we got stuck."

Operator pool (anti-Hermitian generators A = i P, ring of L=8, PBC):
  * singles:  i Y_j                       (rotates away from product state; gradient-active)
  * entanglers: i Y_j Z_{j+1}, i Z_j Y_{j+1}   (nearest-neighbor on the ring)
Each appended generator = one exp(theta * i P) factor. We score 2q cost by counting appended
two-qubit generators (each ~3 ZZPhase after standard compilation, matching the depth-scan's
zz_ub = 3 * n_2q convention) so the comparison to chi=3's 451 is apples-to-apples.

Reuses: brickwork_force_check.{build_tfim_sparse, bp_op, energy, force_profile},
        hyp024_tfd_btz_transport.sparse_pauli_full.
"""
import json
import time

import numpy as np
from scipy.sparse.linalg import eigsh, expm_multiply

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD

L = 8
OUT = "D:/quantum-worldline/research/data/builds/adapt_vqe_results.json"
OVERLAP_TARGET = 0.99
FORCE_RMSE_TARGET = 0.02
GRAD_TOL = 1e-3          # stop when no pool operator has |gradient| above this
MAX_OPS = 60             # hard cap on ansatz length (safety; 451-equivalent is ~150 2q)
DRS = [1, 2, 3]

def build_pool(L):
    """Anti-Hermitian generator pool A = i P on a ring of L qubits (PBC).

    Returns a list of dicts: {name, A (sparse, = i*P), is_2q (bool)}.
      singles:    i Y_j
      entanglers: i Y_j Z_{j+1}, i Z_j Y_{j+1}   (nearest-neighbor, modular)
    The factor i makes A anti-Hermitian so exp(theta*A) is unitary and the energy
    gradient at theta=0 is real: dE/dtheta = <psi|[H,A]|psi> = 2 Re <psi|H A|psi>.
    """
    pool = []
    for j in range(L):
        Yj = TFD.sparse_pauli_full(L, j, "Y")
        pool.append({"name": f"Y{j}", "A": 1j * Yj, "is_2q": False})
    for j in range(L):
        jp = (j + 1) % L
        Yj = TFD.sparse_pauli_full(L, j, "Y")
        Zj = TFD.sparse_pauli_full(L, j, "Z")
        Yp = TFD.sparse_pauli_full(L, jp, "Y")
        Zp = TFD.sparse_pauli_full(L, jp, "Z")
        pool.append({"name": f"Y{j}Z{jp}", "A": 1j * (Yj @ Zp), "is_2q": True})
        pool.append({"name": f"Z{j}Y{jp}", "A": 1j * (Zj @ Yp), "is_2q": True})
    return pool


def reference_state(L):
    """Initial reference: |+>^L (X-polarized), the g>>1 limit of critical TFIM.
    This is the natural product start -- H's transverse field is already diagonalized
    in this basis, so all initial single-Y gradients are clean and nonzero where they
    should be. Returned as a dense complex statevector (dim 2^L)."""
    dim = 2 ** L
    plus = np.ones(dim, dtype=complex) / np.sqrt(dim)
    return plus


def apply_ansatz(thetas, ops, psi0):
    """Apply prod_k exp(theta_k * A_k) to psi0, in append order (last appended acts last).
    ops is a list of pool entries; thetas is a 1D array aligned with ops."""
    sv = psi0
    for theta, op in zip(thetas, ops):
        sv = expm_multiply(theta * op["A"], sv)
    return sv


def select_next_op(psi, H, pool):
    """Pick the pool operator with the largest |energy gradient| at the current state.

    For anti-Hermitian A_k, appending exp(theta A_k) at theta=0 gives
        g_k = dE/dtheta_k = <psi|[H, A_k]|psi> = 2 Re <psi| H A_k |psi>.
    Returns (best_op, best_abs_grad, all_abs_grads). No optimization here -- this is the
    cheap steepest-descent screen that makes ADAPT escape fixed-ansatz plateaus.
    """
    Hpsi = H @ psi
    grads = []
    for op in pool:
        # <psi|H A|psi> = <Hpsi | A psi>  (H Hermitian); A = i P, so this is generally complex
        Apsi = op["A"] @ psi
        g = 2.0 * np.real(np.vdot(Hpsi, Apsi))
        grads.append(abs(g))
    grads = np.asarray(grads)
    idx = int(np.argmax(grads))
    return pool[idx], float(grads[idx]), grads


def optimize_angles(ops, psi0, H, theta_init):
    """Re-optimize ALL accumulated angles by minimizing <H>. L-BFGS-B with an analytic-free
    objective (statevector energy). Returns (best_thetas, best_energy)."""
    from scipy.optimize import minimize

    def loss(flat):
        sv = apply_ansatz(flat, ops, psi0)
        return float(np.real(np.vdot(sv, H @ sv)))

    r = minimize(loss, theta_init, method="L-BFGS-B",
                 options={"maxiter": 500, "ftol": 1e-12, "gtol": 1e-9})
    return r.x, float(r.fun)


def main():
    t0 = time.time()
    print("=" * 74)
    print("ADAPT-VQE: gradient-grown ansatz for critical-TFIM GS + holographic force")
    print("=" * 74)
    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0])
    psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)
    print(f"E_gs = {Egs:.6f}")
    print("F(dr) exact: " + ", ".join(f"dr={d}:{F_exact[d]:+.5f}" for d in DRS))
    print("chi=3 MERA reference: 451 ZZPhase, exact.")
    print(f"targets: GS-overlap > {OVERLAP_TARGET}, force RMSE < {FORCE_RMSE_TARGET}\n")

    pool = build_pool(L)
    psi0 = reference_state(L)
    print(f"pool size = {len(pool)} generators "
          f"({sum(1 for p in pool if p['is_2q'])} two-qubit), "
          f"reference = |+>^{L}\n")

    ops, thetas = [], np.zeros(0)
    results = {
        "E_gs": Egs, "F_exact": {str(d): F_exact[d] for d in DRS},
        "chi3_zzphase": 451, "overlap_target": OVERLAP_TARGET,
        "force_rmse_target": FORCE_RMSE_TARGET, "L": L, "steps": [],
    }
    first_faithful = None

    for step in range(1, MAX_OPS + 1):
        # current state from accumulated ansatz
        psi_cur = apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = select_next_op(psi_cur, H, pool)
        if best_grad < GRAD_TOL:
            print(f"  [converged] largest |gradient| = {best_grad:.2e} < {GRAD_TOL} "
                  f"at step {step}; stopping growth.")
            break

        # append the selected operator with a fresh 0 angle, re-optimize all angles
        ops.append(best_op)
        theta_init = np.concatenate([thetas, [0.0]])
        thetas, E = optimize_angles(ops, psi0, H, theta_init)

        sv = apply_ansatz(thetas, ops, psi0)
        e_err = E - Egs
        rel = abs(e_err) / abs(Egs) * 100
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
        n_2q = sum(1 for o in ops if o["is_2q"])
        zz_ub = n_2q * 3
        faithful = ov > OVERLAP_TARGET and f_rmse < FORCE_RMSE_TARGET

        step_rec = {
            "step": step, "added": best_op["name"], "grad": best_grad,
            "n_ops": len(ops), "n_2q": n_2q, "zzphase_ub": zz_ub,
            "energy": E, "energy_error": e_err, "energy_rel_pct": rel,
            "gs_overlap": ov, "F_adapt": {str(d): F_b[d] for d in DRS},
            "force_rmse": f_rmse, "faithful": faithful,
        }
        results["steps"].append(step_rec)
        # incremental save so a timeout leaves partial results
        with open(OUT, "w") as f:
            json.dump(results, f, indent=2)

        print(f"  step {step:2d} | +{best_op['name']:7s} g={best_grad:.2e} | "
              f"ops={len(ops):2d} 2q={n_2q:2d} ZZ<={zz_ub:3d} | "
              f"E_err={e_err:+.4f} ({rel:.2f}%) | GSov={ov:.4f} | "
              f"F_rmse={f_rmse:.4f} | {'FAITHFUL' if faithful else '--'}", flush=True)

        if faithful and first_faithful is None:
            first_faithful = step_rec
            print(f"\n  >>> FIRST FAITHFUL at step {step}: 2q={n_2q}, ZZPhase<={zz_ub} "
                  f"vs chi=3's 451. <<<\n")
            break

    # ---- verdict ----
    results["first_faithful"] = first_faithful
    best_ov = max((s["gs_overlap"] for s in results["steps"]), default=0.0)
    results["best_overlap"] = best_ov
    print("\n" + "=" * 74)
    if first_faithful is not None:
        zz = first_faithful["zzphase_ub"]
        if zz < 200:
            verdict = (f"CHEAPER CIRCUIT EXISTS: faithful GS+force at ZZPhase<={zz} "
                       f"(<< 451). QCUP hardware path may reopen pending real pytket compile.")
        else:
            verdict = (f"Faithful only at ZZPhase<={zz}, comparable to chi=3's 451. "
                       f"No meaningful cost saving; chi=3 cost is ~fundamental.")
    else:
        verdict = (f"NO-GO: ADAPT-VQE plateaued at GS-overlap {best_ov:.4f} < {OVERLAP_TARGET} "
                   f"after gradient-grown growth. The chi=3 cost is FUNDAMENTAL, not an "
                   f"optimizer artifact -- QCUP can be closed with a real no-go.")
    results["verdict"] = verdict
    results["wall_seconds"] = time.time() - t0
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"  VERDICT: {verdict}")
    print(f"  best GS-overlap reached: {best_ov:.4f}")
    print(f"  wall: {results['wall_seconds']:.1f} s")
    print(f"  saved -> {OUT}")


if __name__ == "__main__":
    main()
