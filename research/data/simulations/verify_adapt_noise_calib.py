"""
PROBE 3 calibration / adversarial cross-check.

The headline (verify_adapt_noise.py) says ~99% of the force survives at 99.921% with 25 2q gates.
That seems TOO clean given CONTEXT says chi=3's 451 gates gave a ~30% noise floor. Two adversarial
questions:

  (A) SCALING SANITY: does the SAME per-gate depolarizing model, applied to a circuit with ~451
      2q gates, reproduce a ~30%-ish degradation? If 25 gates -> 1% loss and the loss is roughly
      multiplicative per gate, 451 gates should give a much larger loss. We test by repeating the
      25-gate ADAPT block back-to-back to inflate the 2q-gate count (18 reps ~ 450 gates) WITHOUT
      changing the ideal state (each rep is followed by its exact inverse so the noiseless state
      is unchanged; only the noise accumulates). This isolates "noise per gate-count" cleanly.

      NOTE: a faithful inverse block returns the state to the ADAPT state, so noiseless force is
      identical; the only thing that grows is the depolarizing-accumulated mixing. This is the
      honest way to ask "what would 451 gates of THIS noise do to THIS observable".

  (B) OBSERVABLE-CANCELLATION CHECK: the force is a difference of energies all taken on the same
      noisy rho. Global depolarizing rho -> (1-q) rho_ideal + q I/d shrinks EVERY energy
      expectation by the same factor toward Tr[H]/d = 0, AND the sigma-excited-then-renormalized
      states partially undo that shrink. So the force could be artificially robust. We quantify
      by also reporting the GLOBAL effective depolarization q_eff (from purity) and what a pure
      global-depolarizing toy model predicts for the force, vs the real per-gate sim.

Reuses verify_adapt_noise helpers.
"""
import json
import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import adapt_vqe_force as AV
import verify_adapt_noise as VN

L = VN.L
DRS = VN.DRS
OUT = "D:/quantum-worldline/research/data/builds/adapt_noise_calib_results.json"


def evolve_noisy_repeated(ops, thetas, p2q, p1q, reps):
    """Apply the ADAPT block then its exact inverse, `reps` times, accumulating noise each gate.
    Noiseless net unitary = identity per (forward+inverse) pair AFTER the first forward, so the
    final ideal state is the ADAPT state. Returns final rho.

    Sequence: forward(block) [-> ADAPT state], then reps-1 times: inverse(block); forward(block).
    Each gate (forward or inverse) is followed by its depolarizing channel.
    Total 2q gate count = (2*reps - 1) * n_2q_block.
    """
    psi0 = AV.reference_state(L)
    rho = np.outer(psi0, psi0.conj())

    # forward gate list (theta, op) and inverse gate list (-theta, op) in REVERSE order
    fwd = list(zip(thetas, ops))
    inv = [(-t, o) for (t, o) in reversed(fwd)]

    bond_cache, site_cache = {}, {}

    def apply_block(block):
        nonlocal rho
        for theta, op in block:
            U = VN.gate_unitary(theta, op)
            rho = U @ rho @ U.conj().T
            sites = VN.op_support(op)
            if op["is_2q"]:
                a, b = sorted(sites)
                key = (a, b)
                if key not in bond_cache:
                    bond_cache[key] = VN.bond_paulis(a, b)
                rho = VN.depolarize_support(rho, bond_cache[key], p2q)
            else:
                a = sites[0]
                if a not in site_cache:
                    site_cache[a] = VN.site_paulis(a)
                rho = VN.depolarize_support(rho, site_cache[a], p1q)

    apply_block(fwd)
    for _ in range(reps - 1):
        apply_block(inv)
        apply_block(fwd)

    tr = np.real(np.trace(rho))
    return rho / tr


def main():
    print("=" * 74)
    print("PROBE 3 calibration: scaling to ~451 gates + global-depol cancellation check")
    print("=" * 74)

    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)
    VN.F_exact_global = F_exact
    ideal_norm = float(np.sqrt(np.mean([F_exact[d] ** 2 for d in DRS])))
    print("F(dr) EXACT GS: " + ", ".join(f"dr={d}:{F_exact[d]:+.5f}" for d in DRS))

    ops, thetas = VN.reconstruct_adapt(H, psi_gs)
    n_2q = sum(1 for o in ops if o["is_2q"])
    print(f"ADAPT block: {len(ops)} ops, {n_2q} two-qubit gates")

    sig_ops = {0: FC.bp_op(L, 0).toarray()}
    for dr in DRS:
        sig_ops[dr] = FC.bp_op(L, dr).toarray()
    Hd = H.toarray()

    p2q = 1.0 - 0.99921
    p1q = p2q / 10.0

    results = {"p_2q": p2q, "F_exact": {str(d): F_exact[d] for d in DRS},
               "ideal_force_rms": ideal_norm, "n_2q_block": n_2q, "scaling": []}

    # Scaling: reps -> total 2q gates = (2*reps - 1) * n_2q
    print("\n(A) SCALING under the SAME per-gate depolarizing (forward/inverse padding):")
    print(f"{'reps':>5} {'tot_2q':>7} {'purity':>9} {'q_eff':>8} | "
          f"{'F1':>8} {'surv_rms':>9} {'surv_dr1':>9}")
    for reps in [1, 2, 4, 9, 18]:
        rho = evolve_noisy_repeated(ops, thetas, p2q, p1q, reps)
        tot2q = (2 * reps - 1) * n_2q
        purity = float(np.real(np.trace(rho @ rho)))
        # global-equivalent depol q_eff: purity of (1-q)|psi><psi| + q I/d  =  (1-q)^2 + q^2/d...
        # but our state isn't globally depolarized; we report purity as the diagnostic.
        # effective q from purity assuming near-pure: solve (1-q)^2 + 2(1-q)q/d + q^2(2^L)/d^2.
        d = 2 ** L
        # purity of rho_q = (1-q) P + q I/d  where P pure: Tr(rho_q^2) = (1-q)^2 + 2(1-q)q/d + q^2/d
        # solve for q numerically
        a = 1.0 - 2.0 / d + 1.0 / d  # coefficient bookkeeping below instead
        # quadratic: (1 - 2/d + 1/d) q^2 + (-2 + 2/d) q + (1 - purity) = 0
        A = 1.0 - 2.0 / d + 1.0 / d
        B = -2.0 + 2.0 / d
        C = 1.0 - purity
        disc = B * B - 4 * A * C
        q_eff = (-B - np.sqrt(max(disc, 0))) / (2 * A) if A != 0 else None
        F_n, _, _ = VN.force_profile_rho(rho, H, sig_ops)
        noisy_rms = float(np.sqrt(np.mean([F_n[d] ** 2 for d in DRS])))
        surv_rms = noisy_rms / ideal_norm
        surv1 = F_n[1] / F_exact[1]
        print(f"{reps:>5} {tot2q:>7} {purity:>9.4f} {q_eff:>8.4f} | "
              f"{F_n[1]:>+8.4f} {surv_rms:>9.4f} {surv1:>9.4f}")
        results["scaling"].append({
            "reps": reps, "total_2q_gates": tot2q, "purity": purity,
            "q_eff_global": float(q_eff),
            "F_noisy": {str(d): F_n[d] for d in DRS},
            "signal_survival_fraction_rms": surv_rms,
            "signal_survival_fraction_dr1": float(surv1),
        })

    # (B) Global-depolarizing toy: rho_q = (1-q) |adapt><adapt| + q I/d, force vs q.
    print("\n(B) GLOBAL-DEPOL TOY (force under uniform rho->(1-q)P+qI/d):")
    sv = AV.apply_ansatz(thetas, ops, AV.reference_state(L))
    P = np.outer(sv, sv.conj())
    d = 2 ** L
    Imm = np.eye(d, dtype=complex) / d
    print(f"{'q':>8} | {'F1':>8} {'F2':>8} {'F3':>8} {'surv_rms':>9}")
    toy = []
    for q in [0.0, 0.05, 0.1, 0.2, 0.3, 0.5]:
        rho = (1 - q) * P + q * Imm
        F_n, _, _ = VN.force_profile_rho(rho, H, sig_ops)
        noisy_rms = float(np.sqrt(np.mean([F_n[d2] ** 2 for d2 in DRS])))
        surv = noisy_rms / ideal_norm
        print(f"{q:>8.2f} | {F_n[1]:>+8.4f} {F_n[2]:>+8.4f} {F_n[3]:>+8.4f} {surv:>9.4f}")
        toy.append({"q": q, "F_noisy": {str(dd): F_n[dd] for dd in DRS},
                    "signal_survival_fraction_rms": surv})
    results["global_depol_toy"] = toy

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nsaved -> {OUT}")


if __name__ == "__main__":
    main()
