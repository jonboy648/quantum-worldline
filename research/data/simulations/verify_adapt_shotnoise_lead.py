"""
LEAD CROSS-CHECK (task #95): shot-noise resolvability of the dr=1 force, the REAL
near-term QCUP deliverable ("2-point existence detection", per qcup-resubmission doc).

The force F(dr)=E_dual - E0 - 2(E_single - E0) is a sum/difference of FOUR energy
expectations, each estimated from finite shots. We need P( F_hat(dr=1) < 0 ) -- i.e.
is the attractive force resolvable above shot noise -- at realistic shot budgets.

Method: build the exact ADAPT state (statevector). For each of the three states
(psi, sig0 psi normalized, sig1 sig0 psi normalized), H = -sum X - sum ZZ is measured
in TWO commuting bases: the X-basis (all -X_j terms) and the Z-basis (all -Z_jZ_{j+1}).
Per-shot energy variance per basis = Var(sum of that basis's terms) under the state.
We propagate to Var(E_hat) = (VarX + VarZ)/(shots/2) assuming the shot budget is split
between the two bases. Then F_hat ~ Normal(F_true, sqrt(sum of the 4 states' Var(E)
with the 1,-1,-2,(+2 for E0 double-count)) ) and we report P(F_hat(dr=1)<0) and SNR.

This is the standard variance-based shot estimate (no full MC needed); it is a CEILING
on resolvability (ignores SPAM/readout/gate noise, which only worsen it).
"""
import json
import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD
import adapt_vqe_force as AV

L = 8
DRS = [1, 2]
OUT = "D:/quantum-worldline/research/data/builds/verify_adapt_shotnoise_lead_results.json"


def regrow():
    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)
    pool = AV.build_pool(L); psi0 = AV.reference_state(L)
    ops, thetas = [], np.zeros(0)
    for _ in range(60):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, g, _ = AV.select_next_op(psi_cur, H, pool)
        if g < 1e-3:
            break
        ops.append(best_op)
        thetas, E = AV.optimize_angles(ops, psi0, H, np.concatenate([thetas, [0.0]]))
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        fr = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
        if ov > 0.99 and fr < 0.02:
            break
    return AV.apply_ansatz(thetas, ops, psi0), F_exact


def basis_ops():
    """Return (X_terms, ZZ_terms) as dense matrices summed: HX = -sum X_j, HZZ = -sum ZjZj+1."""
    X = sum(_PD[(j, "X")] for j in range(L))
    ZZ = sum(_PD[(j, "Z")] @ _PD[((j + 1) % L, "Z")] for j in range(L))
    return -X, -ZZ  # signs as in H


_PD = {(s, p): TFD.sparse_pauli_full(L, s, p).toarray() for s in range(L)
       for p in ("I", "X", "Y", "Z")}


def var_of(op, sv):
    """Var(op) = <op^2> - <op>^2 for state sv (per-shot variance of the basis sum)."""
    o_sv = op @ sv
    mean = float(np.real(np.vdot(sv, o_sv)))
    msq = float(np.real(np.vdot(o_sv, o_sv)))
    return msq - mean ** 2, mean


def var_energy(sv, HX, HZZ, shots):
    """Var(E_hat) splitting shots equally between X and ZZ commuting groups."""
    vX, _ = var_of(HX, sv)
    vZ, _ = var_of(HZZ, sv)
    s = shots / 2.0
    return vX / s + vZ / s


def main():
    sv, F_exact = regrow()
    HX, HZZ = basis_ops()
    sig0 = FC.bp_op(L, 0).toarray()

    # the three states for dr=1 force
    p_single = sig0 @ sv; p_single /= np.linalg.norm(p_single)
    out = {"F_exact_dr1": F_exact[1], "F_exact_dr2": F_exact[2], "shots_scan": []}

    print("=" * 70)
    print("SHOT-NOISE resolvability of the dr=1 / dr=2 force (ceiling estimate)")
    print(f"F_exact dr1 = {F_exact[1]:+.4f}, dr2 = {F_exact[2]:+.4f}")
    print("=" * 70)
    print(f"{'shots/state':>12} {'sigma_F1':>10} {'SNR_F1':>8} {'P(F1<0)':>9} "
          f"{'sigma_F2':>10} {'SNR_F2':>8} {'P(F2<0)':>9}")

    sig1 = FC.bp_op(L, 1).toarray()
    sig2 = FC.bp_op(L, 2).toarray()
    p_dual1 = sig1 @ (sig0 @ sv); p_dual1 /= np.linalg.norm(p_dual1)
    p_dual2 = sig2 @ (sig0 @ sv); p_dual2 /= np.linalg.norm(p_dual2)

    from math import erf, sqrt
    def p_neg(mean, sigma):
        # P(N(mean,sigma) < 0)
        z = -mean / sigma
        return 0.5 * (1 + erf(z / sqrt(2)))

    for shots in [1000, 5000, 10000, 50000, 100000]:
        # F = E_dual - E0 - 2 E_single + 2 E0 = E_dual - 2 E_single + E0
        vE0 = var_energy(sv, HX, HZZ, shots)
        vEs = var_energy(p_single, HX, HZZ, shots)
        vEd1 = var_energy(p_dual1, HX, HZZ, shots)
        vEd2 = var_energy(p_dual2, HX, HZZ, shots)
        # coefficients: E_dual(+1), E_single(-2), E0(+1) -> independent estimates
        sigF1 = float(np.sqrt(vEd1 + 4 * vEs + vE0))
        sigF2 = float(np.sqrt(vEd2 + 4 * vEs + vE0))
        snr1 = abs(F_exact[1]) / sigF1
        snr2 = abs(F_exact[2]) / sigF2
        pneg1 = p_neg(F_exact[1], sigF1)
        pneg2 = p_neg(F_exact[2], sigF2)
        out["shots_scan"].append({
            "shots_per_state": shots, "sigma_F1": sigF1, "SNR_F1": snr1,
            "P_F1_neg": pneg1, "sigma_F2": sigF2, "SNR_F2": snr2, "P_F2_neg": pneg2})
        print(f"{shots:>12} {sigF1:>10.4f} {snr1:>8.2f} {pneg1:>9.4f} "
              f"{sigF2:>10.4f} {snr2:>8.2f} {pneg2:>9.4f}")

    print("\nNote: ceiling estimate (gate/SPAM/readout noise omitted, which only lower SNR).")
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"saved -> {OUT}")


if __name__ == "__main__":
    main()
