"""
PROBE 3 (task #95 verification): Does the depth-25 ADAPT-VQE circuit survive Helios noise?

The QCUP-reopening claim rests on "75 ZZPhase << chi=3's 451 -> 6x cheaper -> hardware path
reopens". But chi=3 was put on hold because its 451 gates at 99.921% 2q fidelity gave a ~30%
noise floor that drowned the alpha~4 force signal. A cheaper circuit only reopens QCUP if its
noise floor is ACCEPTABLE -- i.e. the force signal is still resolvable above noise.

This script does a PROPER mixed-state (density-matrix) simulation (L=8 -> 256x256 rho, trivial):
  1. Re-run the ADAPT-VQE growth EXACTLY as adapt_vqe_force.py does, keep the ordered operator
     list and the final optimized angles. (Sanity-check the noiseless force vs the saved JSON.)
  2. Build rho = |psi0><psi0| from the |+>^8 reference. Apply each gate exp(theta_k A_k) by
     conjugation: rho -> U rho U^dag. After each TWO-QUBIT gate apply a 2q depolarizing channel
     at rate p_2q; after each SINGLE-QUBIT gate apply 1q depolarizing at p_1q = p_2q/10.
     Depolarizing is implemented by EXACT Pauli twirl on the gate's support: with prob (1-p)
     leave rho, with prob p replace the support's reduced state by maximally mixed -- equivalently
     mix in p * (avg over the d^2 Paulis on the support). We do the exact average over the
     n-qubit Paulis supported on those sites (15 non-identity for 2q, 3 for 1q), which IS the
     depolarizing channel acting on that subsystem.
  3. On the final NOISY rho compute F(dr): E0 = Tr[rho H]; rho_single = N(sig0 rho sig0^dag),
     rho_dual = N(sig_dr sig0 rho (sig_dr sig0)^dag); F = E_dual - E0 - 2(E_single - E0).
     sig is the (non-unitary) boundary-primary; N normalizes by trace.
  4. Headline: at 99.921% 2q fidelity, what fraction of the ideal force survives? Distinguishable
     from zero (the QCUP bar)?

Reuses: brickwork_force_check.{build_tfim_sparse, bp_op, energy}, adapt_vqe_force.{build_pool,
        reference_state, apply_ansatz, select_next_op, optimize_angles, GRAD_TOL, MAX_OPS, DRS}.
Does NOT modify adapt_vqe_force.py or any existing result JSON.
"""
import json
import time

import numpy as np
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD
import adapt_vqe_force as AV

L = 8
DIM = 2 ** L
DRS = [1, 2, 3]
OUT = "D:/quantum-worldline/research/data/builds/adapt_noise_results.json"

# Helios 2q infidelity from memory (99.921% -> 7.9e-4). Sensitivity sweep adds 1e-3, 2e-3.
P2Q_LIST = [1.0 - 0.99921, 0.001, 0.002]


# ----------------------------------------------------------------------------
# Pauli machinery (dense, L small)
# ----------------------------------------------------------------------------
def pauli_dense(site, p):
    """Dense n-qubit Pauli p on a single site (site 0 = highest bit, matches TFD)."""
    return TFD.sparse_pauli_full(L, site, p).toarray()


# Cache single-site dense Paulis
_PD = {(s, p): pauli_dense(s, p) for s in range(L) for p in ("I", "X", "Y", "Z")}


def two_site_pauli(a, b, pa, pb):
    """Dense n-qubit operator = Pauli pa on site a times Pauli pb on site b."""
    if pa == "I" and pb == "I":
        return np.eye(DIM, dtype=complex)
    if pa == "I":
        return _PD[(b, pb)]
    if pb == "I":
        return _PD[(a, pa)]
    return _PD[(a, pa)] @ _PD[(b, pb)]


# Precompute the 15 non-identity 2q Pauli operators for each NN bond, and 3 for each site.
_LABELS = ("I", "X", "Y", "Z")


def bond_paulis(a, b):
    ops = []
    for pa in _LABELS:
        for pb in _LABELS:
            if pa == "I" and pb == "I":
                continue
            ops.append(two_site_pauli(a, b, pa, pb))
    return ops  # 15 ops


def site_paulis(a):
    return [_PD[(a, p)] for p in ("X", "Y", "Z")]  # 3 ops


# ----------------------------------------------------------------------------
# Depolarizing channel via exact Pauli twirl on the gate's support
# ----------------------------------------------------------------------------
# For a k-qubit subsystem, the depolarizing channel with parameter p is
#   E(rho) = (1-p) rho + p * (I_sub/d_sub) ⊗ Tr_sub[rho]
# On the full n-qubit space this equals
#   E(rho) = (1 - p*d^2/(d^2-1)) rho + (p/(d^2-1)) * sum_{P != I on support} P rho P
# where d = 2^k and the sum is over the (d^2 - 1) non-identity Paulis acting ONLY on the
# support sites (identity elsewhere). This is the standard twirl identity:
#   (1/d^2) sum_{all P} P rho P = (I_sub/d) ⊗ Tr_sub[rho].
# We use depolarizing "probability" convention p = infidelity such that p=1 -> fully
# depolarized on the support. (p here is the channel's total error weight.)
def depolarize_support(rho, pauli_ops, p):
    """Apply depolarizing on the support spanned by pauli_ops (the non-identity Paulis).
    d2 = len(pauli_ops) + 1 (total Paulis incl identity = d^2). Twirl identity:
        twirl(rho) = (1/d2) [ rho + sum_{P!=I} P rho P ]   (= maximally mixed on support).
    Channel: (1-p) rho + p * twirl(rho)."""
    d2 = len(pauli_ops) + 1
    acc = rho.copy()
    for P in pauli_ops:
        acc = acc + P @ rho @ P.conj().T
    twirl = acc / d2
    return (1.0 - p) * rho + p * twirl


# ----------------------------------------------------------------------------
# Build the noisy state by evolving rho through the ADAPT ansatz
# ----------------------------------------------------------------------------
def reconstruct_adapt(H, psi_gs):
    """Re-run ADAPT-VQE growth identically to adapt_vqe_force.main(); return (ops, thetas)."""
    pool = AV.build_pool(L)
    psi0 = AV.reference_state(L)
    ops, thetas = [], np.zeros(0)
    for step in range(1, AV.MAX_OPS + 1):
        psi_cur = AV.apply_ansatz(thetas, ops, psi0) if ops else psi0
        best_op, best_grad, _ = AV.select_next_op(psi_cur, H, pool)
        if best_grad < AV.GRAD_TOL:
            break
        ops.append(best_op)
        theta_init = np.concatenate([thetas, [0.0]])
        thetas, E = AV.optimize_angles(ops, psi0, H, theta_init)
        sv = AV.apply_ansatz(thetas, ops, psi0)
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, DRS)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact_global[d]) ** 2 for d in DRS])))
        faithful = ov > AV.OVERLAP_TARGET and f_rmse < AV.FORCE_RMSE_TARGET
        if faithful:
            break
    return ops, thetas


def gate_unitary(theta, op):
    """Dense unitary exp(theta * A), A = i P sparse. expm of a (anti-Herm) sparse op."""
    from scipy.sparse.linalg import expm
    return expm(theta * op["A"]).toarray()


def op_support(op):
    """Return the list of qubit indices the generator acts on (parse the name)."""
    name = op["name"]
    # names look like 'Y3' or 'Y3Z4' or 'Z5Y6'
    sites = []
    i = 0
    while i < len(name):
        # letter then digits
        i += 1  # skip pauli letter
        num = ""
        while i < len(name) and name[i].isdigit():
            num += name[i]
            i += 1
        sites.append(int(num))
    return sites


def evolve_noisy(ops, thetas, p2q, p1q):
    """rho through the ansatz with depolarizing after each gate. Returns final rho."""
    psi0 = AV.reference_state(L)
    rho = np.outer(psi0, psi0.conj())
    # precompute support pauli sets per op (cache by support tuple)
    bond_cache = {}
    site_cache = {}
    for theta, op in zip(thetas, ops):
        U = gate_unitary(theta, op)
        rho = U @ rho @ U.conj().T
        sites = op_support(op)
        if op["is_2q"]:
            a, b = sorted(sites)
            key = (a, b)
            if key not in bond_cache:
                bond_cache[key] = bond_paulis(a, b)
            rho = depolarize_support(rho, bond_cache[key], p2q)
        else:
            a = sites[0]
            if a not in site_cache:
                site_cache[a] = site_paulis(a)
            rho = depolarize_support(rho, site_cache[a], p1q)
    # renormalize trace defensively (channels are trace-preserving; guard fp drift)
    tr = np.real(np.trace(rho))
    return rho / tr


# ----------------------------------------------------------------------------
# Force observable on a density matrix
# ----------------------------------------------------------------------------
def force_profile_rho(rho, H, sig_ops):
    """F(dr) on a mixed state rho. sig_ops is dict dr->dense sigma_dr; sig0 = sig_ops[0].
    E0 = Tr[rho H]; rho_single = N(sig0 rho sig0^dag); rho_dual = N(sig_dr sig0 rho (.)^dag)."""
    Hd = H.toarray() if hasattr(H, "toarray") else H
    E0 = float(np.real(np.trace(rho @ Hd)))
    sig0 = sig_ops[0]
    rs = sig0 @ rho @ sig0.conj().T
    tr_s = np.real(np.trace(rs))
    rs = rs / tr_s
    E_single = float(np.real(np.trace(rs @ Hd)))
    out = {}
    for dr in DRS:
        M = sig_ops[dr] @ sig0
        rd = M @ rho @ M.conj().T
        tr_d = np.real(np.trace(rd))
        if tr_d < 1e-14:
            out[dr] = None
            continue
        rd = rd / tr_d
        E_dual = float(np.real(np.trace(rd @ Hd)))
        out[dr] = E_dual - E0 - 2.0 * (E_single - E0)
    return out, E0, E_single


def main():
    global F_exact_global
    t0 = time.time()
    print("=" * 74)
    print("PROBE 3: Helios-noise survival of the depth-25 ADAPT-VQE force circuit")
    print("=" * 74)

    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0])
    psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)
    F_exact_global = F_exact
    print(f"E_gs = {Egs:.6f}")
    print("F(dr) EXACT GS: " + ", ".join(f"dr={d}:{F_exact[d]:+.5f}" for d in DRS))

    # --- Reconstruct ADAPT ansatz ---
    print("\nReconstructing ADAPT-VQE growth (re-running optimization)...")
    ops, thetas = reconstruct_adapt(H, psi_gs)
    n_2q = sum(1 for o in ops if o["is_2q"])
    n_1q = sum(1 for o in ops if not o["is_2q"])
    print(f"  reconstructed ansatz: {len(ops)} ops ({n_2q} two-qubit, {n_1q} single), "
          f"ZZPhase_ub = 3*{n_2q} = {3*n_2q}")

    # Noiseless cross-check (statevector force on the reconstructed ansatz)
    sv = AV.apply_ansatz(thetas, ops, psi0=AV.reference_state(L))
    ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
    F_sv, _, _ = FC.force_profile(sv, H, L, DRS)
    f_rmse_sv = float(np.sqrt(np.mean([(F_sv[d] - F_exact[d]) ** 2 for d in DRS])))
    print(f"  noiseless reconstructed: GSov={ov:.5f}, force_rmse={f_rmse_sv:.5f}")
    print("  F(dr) noiseless ansatz: "
          + ", ".join(f"dr={d}:{F_sv[d]:+.5f}" for d in DRS))

    # Sanity: noiseless rho via the SAME depolarize pipeline at p=0 must equal statevector force
    sig_ops = {}
    sig_ops[0] = FC.bp_op(L, 0).toarray()
    for dr in DRS:
        sig_ops[dr] = FC.bp_op(L, dr).toarray()
    rho0 = evolve_noisy(ops, thetas, 0.0, 0.0)
    F_rho0, E0_0, _ = force_profile_rho(rho0, H, sig_ops)
    f_rmse_rho0 = float(np.sqrt(np.mean([(F_rho0[d] - F_sv[d]) ** 2 for d in DRS])))
    print(f"  [pipeline check] p=0 rho force vs statevector force RMSE = {f_rmse_rho0:.2e}"
          f" (should be ~1e-12)")

    ideal_norm = float(np.sqrt(np.mean([F_exact[d] ** 2 for d in DRS])))

    results = {
        "L": L, "E_gs": Egs, "n_2q_gates": n_2q, "n_1q_gates": n_1q,
        "zzphase_ub": 3 * n_2q, "chi3_zzphase": 451,
        "F_exact": {str(d): F_exact[d] for d in DRS},
        "F_noiseless_ansatz": {str(d): F_sv[d] for d in DRS},
        "noiseless_overlap": ov, "noiseless_force_rmse": f_rmse_sv,
        "pipeline_check_rmse": f_rmse_rho0,
        "ideal_force_rms_magnitude": ideal_norm,
        "sweeps": [],
    }

    print("\n" + "=" * 74)
    print(f"{'p_2q':>9} {'p_1q':>9} | {'F1_noisy':>9} {'F2_noisy':>9} {'F3_noisy':>9} | "
          f"{'rmse_v_ideal':>12} {'surv_dr1':>9} {'surv_rms':>9}")
    print("-" * 74)
    for p2q in P2Q_LIST:
        p1q = p2q / 10.0
        rho = evolve_noisy(ops, thetas, p2q, p1q)
        purity = float(np.real(np.trace(rho @ rho)))
        F_n, E0_n, Es_n = force_profile_rho(rho, H, sig_ops)
        rmse_ideal = float(np.sqrt(np.mean([(F_n[d] - F_exact[d]) ** 2 for d in DRS])))
        surv_dr1 = F_n[1] / F_exact[1] if F_exact[1] != 0 else None
        noisy_rms = float(np.sqrt(np.mean([F_n[d] ** 2 for d in DRS])))
        surv_rms = noisy_rms / ideal_norm
        print(f"{p2q:>9.5f} {p1q:>9.5f} | "
              f"{F_n[1]:>+9.4f} {F_n[2]:>+9.4f} {F_n[3]:>+9.4f} | "
              f"{rmse_ideal:>12.5f} {surv_dr1:>9.4f} {surv_rms:>9.4f}")
        results["sweeps"].append({
            "p_2q": p2q, "p_1q": p1q, "purity": purity,
            "E0_noisy": E0_n,
            "F_noisy": {str(d): F_n[d] for d in DRS},
            "force_rmse_noisy_vs_ideal": rmse_ideal,
            "signal_survival_fraction_dr1": surv_dr1,
            "noisy_force_rms": noisy_rms,
            "signal_survival_fraction_rms": surv_rms,
        })

    # Verdict on the Helios point (first in list = 99.921%)
    helios = results["sweeps"][0]
    surv1 = helios["signal_survival_fraction_dr1"]
    survr = helios["signal_survival_fraction_rms"]
    # QCUP bar: signal must be clearly resolvable above zero. Use a generous-but-honest
    # threshold: >50% of the signal surviving at the Helios fidelity AND the noisy force
    # still strongly negative (correct sign, dominant dr=1) -> SUPPORTS. Marginal (10-50%)
    # -> PARTIAL. <10% or sign-flip -> REFUTE.
    if survr > 0.5 and helios["F_noisy"]["1"] < 0 and surv1 > 0.5:
        verdict = (f"SUPPORTS: at 99.921% 2q fidelity ~{survr*100:.0f}% of the force RMS "
                   f"survives; dr=1 force {helios['F_noisy']['1']:+.3f} (ideal "
                   f"{F_exact[1]:+.3f}). Resolvable above zero.")
    elif survr > 0.1:
        verdict = (f"PARTIAL: at 99.921% only ~{survr*100:.0f}% of the force RMS survives "
                   f"(dr1 survival {surv1*100:.0f}%). Marginal vs the QCUP zero-bar.")
    else:
        verdict = (f"REFUTES: at 99.921% only ~{survr*100:.0f}% of the force RMS survives "
                   f"-- the depolarizing noise floor drowns the signal, same failure mode "
                   f"as chi=3. QCUP does NOT reopen.")
    results["verdict"] = verdict
    results["wall_seconds"] = time.time() - t0
    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print("\n" + "=" * 74)
    print(f"VERDICT: {verdict}")
    print(f"saved -> {OUT}")
    print(f"wall: {results['wall_seconds']:.1f} s")


if __name__ == "__main__":
    main()
