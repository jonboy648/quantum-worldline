"""
RED-TEAM cross-check of the ADAPT-VQE physics claim (task #95 verification).

The compile probe verified only the gate COUNT (42 ZZPhase). It explicitly did NOT re-check
that the 25-operator structure it compiled is the SAME structure that achieves
gs_overlap=0.9998 / force_rmse=0.0045, because the optimized angles were never saved.

This script closes that gap: it replays the EXACT ordered 25 generators from
adapt_vqe_results.json, re-optimizes all 25 angles by energy minimisation (same objective the
original used), and recomputes gs_overlap + force RMSE. If those reproduce the claimed
0.9998 / 0.0045, then the structure the compile probe counted is the real, physics-faithful one.

It also reports how the 451 chi=3 baseline breaks down (16q vs 8q, 4-qubit blocks + SWAPs)
so the apples-to-apples question can be judged.
"""
import json
import numpy as np
from scipy.sparse.linalg import eigsh, expm_multiply
from scipy.optimize import minimize

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD

L = 8
DRS = [1, 2, 3]
RESULTS = "D:/quantum-worldline/research/data/builds/adapt_vqe_results.json"


def gen_to_A(name):
    """name like 'Y0Z1' -> anti-Hermitian A = i * P (sparse), matching adapt_vqe_force pool."""
    i = 0
    P = None
    while i < len(name):
        letter = name[i]
        j = i + 1
        num = ""
        while j < len(name) and name[j].isdigit():
            num += name[j]; j += 1
        op = TFD.sparse_pauli_full(L, int(num), letter)
        P = op if P is None else (P @ op)
        i = j
    return 1j * P


def apply_ansatz(thetas, As, psi0):
    sv = psi0
    for theta, A in zip(thetas, As):
        sv = expm_multiply(theta * A, sv)
    return sv


def main():
    data = json.load(open(RESULTS))
    added = [s["added"] for s in data["steps"]]
    assert len(added) == 25

    H = FC.build_tfim_sparse(L)
    Egs_arr, psi_eig = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0]); psi_gs = psi_eig[:, 0]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, DRS)

    dim = 2 ** L
    psi0 = np.ones(dim, dtype=complex) / np.sqrt(dim)
    As = [gen_to_A(nm) for nm in added]

    def loss(flat):
        sv = apply_ansatz(flat, As, psi0)
        return float(np.real(np.vdot(sv, H @ sv)))

    # multi-start so we are not hostage to one local min; report best
    best = None
    for seed in range(3):
        rng = np.random.default_rng(1000 + seed)
        x0 = (rng.standard_normal(25) * 0.1) if seed else np.zeros(25)
        r = minimize(loss, x0, method="L-BFGS-B",
                     options={"maxiter": 1000, "ftol": 1e-13, "gtol": 1e-10})
        if best is None or r.fun < best.fun:
            best = r

    sv = apply_ansatz(best.x, As, psi0)
    E = float(np.real(np.vdot(sv, H @ sv)))
    ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
    F_b, _, _ = FC.force_profile(sv, H, L, DRS)
    f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in DRS])))
    rel = abs(E - Egs) / abs(Egs) * 100

    print("=" * 70)
    print("RED-TEAM: replay 25-op ADAPT structure, re-optimize angles")
    print("=" * 70)
    print(f"E_gs={Egs:.6f}  E_adapt={E:.6f}  rel_err={rel:.4f}%")
    print(f"gs_overlap = {ov:.6f}   (claimed 0.9998)")
    print(f"force_rmse = {f_rmse:.6f}  (claimed 0.0045)")
    print("F(dr): " + ", ".join(
        f"dr={d}: exact {F_exact[d]:+.4f} / adapt {F_b[d]:+.4f}" for d in DRS))
    claimed_ov, claimed_rmse = 0.9997682992354651, 0.00453080956786526
    print(f"\noverlap reproduces 0.99: {ov > 0.99}  (within 0.01 of claim: "
          f"{abs(ov-claimed_ov) < 0.01})")
    print(f"force_rmse < 0.02 target: {f_rmse < 0.02}")
    print(f"force_rmse near claim:    {abs(f_rmse-claimed_rmse) < 0.01}")


if __name__ == "__main__":
    main()
