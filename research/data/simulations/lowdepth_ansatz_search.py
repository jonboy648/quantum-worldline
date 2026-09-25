"""
Lower-depth ansatz search: can a circuit with FAR fewer than chi=3 MERA's 451 ZZPhase gates
reproduce the critical-Ising power-law boundary correlator C(r)=<Z_0 Z_r> ~ sin(pi r/L)^{-1/4}
(the signal chi=2 MERA fails to capture, flat ~0.70)?

Approach: variationally fit a depth-D BRICKWORK ansatz of 2-qubit gates on L=8 qubits to the
exact critical-TFIM ground-state correlator, for D=1..Dmax. Find the minimum depth (hence
minimum 2-qubit-gate / ZZPhase count) at which the POWER-LAW emerges (decaying C(r) with
chord-exponent ~ -0.25), vs the chi=2 failure (flat) and chi=3 success (451 ZZPhase, exact).

Maps the Pareto frontier: 2-qubit-gate count vs correlator-fidelity. Determines whether a
viable hardware experiment exists at improved (lower) depth -- the QCUP re-scope question, done
honestly via compute rather than estimate.

Each 2-qubit brickwork gate is a general SU(4) (15 params). On Helios a generic SU(4) compiles
to <=3 ZZPhase (KAK), so ZZPhase_count ~ 3 * (#2q gates). We report both #2q-gates and the
implied ZZPhase upper bound.
"""
import numpy as np
import json
from scipy.optimize import minimize
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh
import hyp024_tfd_btz_transport as TFD

L = 8
OUT = "D:/quantum-worldline/research/data/builds/lowdepth_ansatz_results.json"


# ---- exact target: critical TFIM GS <Z0 Zr> ----
def build_tfim(L, g=1.0):
    dim = 2 ** L
    H = csr_matrix((dim, dim), dtype=complex)
    for j in range(L):
        H = H - g * TFD.sparse_pauli_full(L, j, "X")
    for j in range(L):
        jp = (j + 1) % L
        H = H - (TFD.sparse_pauli_full(L, j, "Z") @ TFD.sparse_pauli_full(L, jp, "Z"))
    return H


# ---- single-qubit and two-qubit gate builders on the full 2^L statevector ----
# We optimize each 2-qubit block as a general SU(4) via its 4x4 anti-Hermitian generator (16 real
# params -> exp(iH)). Brickwork: even bonds then odd bonds per layer.
def pauli_strings_cache(L):
    # precompute single-qubit Z operators (sparse) for correlator measurement
    return [TFD.sparse_pauli_full(L, i, "Z") for i in range(L)]


def herm_from_params(p):
    # p: 16 reals -> 4x4 Hermitian (diag 4 + off-diag 6 complex)
    A = np.zeros((4, 4), dtype=complex)
    idx = 0
    for i in range(4):
        A[i, i] = p[idx]; idx += 1
    for i in range(4):
        for j in range(i + 1, 4):
            A[i, j] = p[idx] + 1j * p[idx + 1]
            A[j, i] = p[idx] - 1j * p[idx + 1]
            idx += 2
    return A


from scipy.linalg import expm

def su4(p):
    return expm(1j * herm_from_params(p))


def apply_2q(sv, U4, i, j, L):
    """Apply 4x4 U on qubits (i,j) to statevector sv (length 2^L). i<j adjacent not required."""
    sv = sv.reshape([2] * L)
    sv = np.moveaxis(sv, [i, j], [0, 1])
    shp = sv.shape
    sv = sv.reshape(4, -1)
    sv = U4 @ sv
    sv = sv.reshape(shp)
    sv = np.moveaxis(sv, [0, 1], [i, j])
    return sv.reshape(-1)


def brickwork_state(params, depth, L):
    """Build |psi> = brickwork(|0>^L). params: list of (16,) per 2q gate, layer by layer.
    Layer pattern: even bonds (0,1),(2,3),(4,5),(6,7) then odd bonds (1,2),(3,4),(5,6),(7,0)."""
    sv = np.zeros(2 ** L, dtype=complex); sv[0] = 1.0
    even = [(0, 1), (2, 3), (4, 5), (6, 7)]
    odd = [(1, 2), (3, 4), (5, 6), (7, 0)]
    k = 0
    for d in range(depth):
        bonds = even if d % 2 == 0 else odd
        for (i, j) in bonds:
            sv = apply_2q(sv, su4(params[k]), i, j, L)
            k += 1
    return sv


def n_gates_for_depth(depth):
    return depth * 4  # 4 bonds per layer


def correlator(sv, Zops, L, connected=True):
    """CONNECTED correlator <Z0 Zr> - <Z0><Zr> by default.
    Critical: the power-law physics is in the CONNECTED correlator. The RAW <Z0 Zr> is gameable
    by a product/shallow state tuning single-site magnetizations <Zi> -- which made an earlier
    version 'fit' the power-law with causally-disconnected depth-1 gates (a degenerate shortcut).
    The exact critical GS is Z2-symmetric (<Zi>=0) so raw==connected for the TARGET, but ansatz
    states are not, so we MUST subtract the disconnected part to compare physics not numbers."""
    z = np.array([np.real(np.vdot(sv, Zops[i] @ sv)) for i in range(L)])
    out = []
    for r in range(1, L // 2 + 1):
        raw = np.real(np.vdot(sv, Zops[0] @ (Zops[r] @ sv)))
        out.append(raw - (z[0] * z[r] if connected else 0.0))
    return np.array(out)


def main():
    print("=" * 72)
    print("Lower-depth ansatz search: brickwork vs chi=3 MERA power-law C(r)")
    print("=" * 72)
    H = build_tfim(L)
    E, psi = eigsh(H, k=1, which="SA"); psi = psi[:, 0]
    Zops = pauli_strings_cache(L)
    target = correlator(psi, Zops, L)
    chord = np.array([np.sin(np.pi * r / L) for r in range(1, L // 2 + 1)])
    rr = np.arange(2, L // 2 + 1)
    tgt_exp = np.polyfit(np.log(chord[1:]), np.log(np.abs(target[1:])), 1)[0]
    print(f"TARGET (exact crit-TFIM): C(r)={np.round(target,4)}, chord-exp={tgt_exp:.3f}")
    print("  (chi=2 MERA gives flat ~0.70; chi=3 MERA = exact at 451 ZZPhase)\n")

    results = {"target_Cr": target.tolist(), "target_exponent": float(tgt_exp),
               "chi2_reference": "flat ~0.70 (GHZ artifact, no power law)",
               "chi3_reference": {"zzphase": 451, "fidelity": "exact"},
               "depths": []}

    rng = np.random.default_rng(7)
    for depth in range(1, 9):
        ng = n_gates_for_depth(depth)
        nparam = ng * 16

        def loss(flat):
            params = flat.reshape(ng, 16)
            sv = brickwork_state(params, depth, L)
            c = correlator(sv, Zops, L)
            return float(np.sum((c - target) ** 2))

        best = None
        for trial in range(3):  # multi-start
            x0 = rng.standard_normal(nparam) * 0.3
            res = minimize(loss, x0, method="L-BFGS-B",
                           options={"maxiter": 400, "ftol": 1e-10})
            if best is None or res.fun < best.fun:
                best = res
        params = best.x.reshape(ng, 16)
        sv = brickwork_state(params, depth, L)
        c = correlator(sv, Zops, L)
        rmse = float(np.sqrt(np.mean((c - target) ** 2)))
        # is it a power law? fit exponent + check decay
        try:
            exp_fit = float(np.polyfit(np.log(chord[1:]), np.log(np.abs(c[1:]) + 1e-12), 1)[0])
        except Exception:
            exp_fit = None
        decaying = bool(c[-1] < c[0] - 0.02)
        zz_upper = ng * 3  # KAK: <=3 ZZPhase per SU(4)
        verdict = ("POWER-LAW captured" if rmse < 0.02 and decaying
                   else "partial" if decaying else "FLAT/failed")
        print(f"  depth={depth} | 2q-gates={ng:2d} | ZZPhase<={zz_upper:3d} | "
              f"RMSE={rmse:.4f} | exp={exp_fit:.3f} | {verdict}")
        results["depths"].append({
            "depth": depth, "n_2q_gates": ng, "zzphase_upper_bound": zz_upper,
            "rmse_vs_target": rmse, "fitted_exponent": exp_fit, "decaying": decaying,
            "Cr": c.tolist(), "verdict": verdict,
        })

    # find minimum depth that captures the power law
    captured = [d for d in results["depths"] if d["verdict"] == "POWER-LAW captured"]
    if captured:
        m = captured[0]
        results["min_depth_powerlaw"] = m["depth"]
        results["min_zzphase_powerlaw"] = m["zzphase_upper_bound"]
        print(f"\n  MIN DEPTH capturing power-law: {m['depth']} "
              f"(<={m['zzphase_upper_bound']} ZZPhase vs chi=3's 451)")
    else:
        results["min_depth_powerlaw"] = None
        print("\n  No tested depth captured the power-law within RMSE<0.02.")

    with open(OUT, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\n  saved -> {OUT}")


if __name__ == "__main__":
    main()
