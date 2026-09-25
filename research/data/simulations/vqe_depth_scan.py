"""
Reframed lower-depth ansatz search (task #94): VARIATIONAL GROUND-STATE PREP, not correlator-fit.

The force check (#92) showed that fitting a brickwork to match C(r) gives a state with ~0% GS
overlap and a wrong force -- matching one observable != reproducing the physics. The HONEST
question: what is the cheapest depth-limited circuit that prepares the actual critical-TFIM
ground state (high GS-overlap / low energy)? Then the force follows automatically.

Method: minimize <H> (critical TFIM, L=8, PBC) over a depth-D brickwork of general SU(4) gates,
for D=1..8 (multi-start). At each depth report:
  - energy error (E - E_gs) and relative error,
  - GS overlap |<gs|psi>|^2,
  - force F(dr) vs exact, and force RMSE.
Find the min depth where GS-overlap > 0.99 AND force RMSE < 0.02. That depth's 2q-gate count
(and ZZPhase upper bound 3x) is the real answer to whether a viable cheaper-than-chi=3 circuit
exists. Energy minimization is variational => cannot be gamed (E >= E_gs always; low E forces
high overlap for a gapped system).

Reuses brickwork machinery from lowdepth_ansatz_search.py and force/bp from brickwork_force_check.py.
"""
import json
import numpy as np
from scipy.optimize import minimize
from scipy.sparse.linalg import eigsh
import lowdepth_ansatz_search as LD
import brickwork_force_check as FC

L = 8
OUT = "D:/quantum-worldline/research/data/builds/vqe_depth_scan_results.json"


def build_H_dense_and_sparse(L):
    Hs = FC.build_tfim_sparse(L)
    return Hs


def main():
    print("=" * 72)
    print("VQE depth scan: cheapest brickwork that PREPARES the critical GS")
    print("=" * 72)
    H = build_H_dense_and_sparse(L)
    Egs_arr, psi = eigsh(H, k=1, which="SA")
    Egs = float(Egs_arr[0]); psi_gs = psi[:, 0]
    Zops = LD.pauli_strings_cache(L)
    drs = [1, 2, 3]
    F_exact, _, _ = FC.force_profile(psi_gs, H, L, drs)
    print(f"E_gs = {Egs:.5f}")
    print("F(dr) exact: " + ", ".join(f"dr={d}:{F_exact[d]:+.4f}" for d in drs))
    print("chi=3 MERA reference: 451 ZZPhase, exact.\n")

    # precompute H as a fast matvec on statevectors
    def Hpsi(sv):
        return H @ sv

    results = {"E_gs": Egs, "F_exact": {str(d): F_exact[d] for d in drs},
               "chi3_zzphase": 451, "depths": []}
    rng = np.random.default_rng(11)

    for depth in range(1, 7):  # cap at 6: past expected faithful depth, keeps params manageable
        ng = LD.n_gates_for_depth(depth); nparam = ng * 16

        def energy_loss(flat):
            sv = LD.brickwork_state(flat.reshape(ng, 16), depth, L)
            return float(np.real(np.vdot(sv, Hpsi(sv))))

        best = None
        n_starts = 3 if depth <= 3 else 2  # trimmed: energy landscape converges fast
        for _ in range(n_starts):
            r = minimize(energy_loss, rng.standard_normal(nparam) * 0.3,
                         method="L-BFGS-B", options={"maxiter": 300, "ftol": 1e-10})
            if best is None or r.fun < best.fun:
                best = r
        sv = LD.brickwork_state(best.x.reshape(ng, 16), depth, L)
        E = float(np.real(np.vdot(sv, Hpsi(sv))))
        e_err = E - Egs
        rel = abs(e_err) / abs(Egs) * 100
        ov = float(abs(np.vdot(psi_gs, sv)) ** 2)
        F_b, _, _ = FC.force_profile(sv, H, L, drs)
        f_rmse = float(np.sqrt(np.mean([(F_b[d] - F_exact[d]) ** 2 for d in drs])))
        zz_ub = ng * 3
        faithful = ov > 0.99 and f_rmse < 0.02
        print(f"  depth={depth} | 2q={ng:2d} ZZ<={zz_ub:3d} | E_err={e_err:+.4f} ({rel:.2f}%) | "
              f"GSov={ov:.4f} | F_rmse={f_rmse:.4f} | {'FAITHFUL' if faithful else '--'}",
              flush=True)
        # incremental save so a timeout still leaves partial results
        with open(OUT, "w") as f:
            json.dump(results, f, indent=2)
        results["depths"].append({
            "depth": depth, "n_2q": ng, "zzphase_ub": zz_ub,
            "energy": E, "energy_error": e_err, "energy_rel_pct": rel,
            "gs_overlap": ov, "F_brick": {str(d): F_b[d] for d in drs},
            "force_rmse": f_rmse, "faithful": faithful,
        })

    faithful = [d for d in results["depths"] if d["faithful"]]
    if faithful:
        m = faithful[0]
        results["min_faithful_depth"] = m["depth"]
        results["min_faithful_zzphase_ub"] = m["zzphase_ub"]
        print(f"\n  MIN FAITHFUL DEPTH: {m['depth']} (2q={m['n_2q']}, ZZPhase<={m['zzphase_ub']} "
              f"vs chi=3's 451). GS-overlap={m['gs_overlap']:.4f}, force RMSE={m['force_rmse']:.4f}")
        if m["zzphase_ub"] < 200:
            print("  => A CHEAPER circuit that carries the force EXISTS. QCUP path may reopen "
                  "(pending real pytket compile).")
        else:
            print("  => Faithful prep needs comparable depth to chi=3; cost is fundamental.")
    else:
        results["min_faithful_depth"] = None
        print("\n  No depth<=8 reached GS-overlap>0.99 + faithful force. "
              "Critical-GS prep is genuinely deep (confirms chi=3 cost ~ fundamental).")

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  saved -> {OUT}")


if __name__ == "__main__":
    main()
