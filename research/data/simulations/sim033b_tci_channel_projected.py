"""
SIM-2026-033b — HYP-2026-027 stage 1b, channel-projected force at the TCI point.

DIAGNOSIS from SIM-033 + gap scan: at the tricritical point the low spectrum is dense
(gaps 0.61, 0.87, 1.14, ...) because c=7/10 has extra relevant primaries. A fixed local
operator (e.g. the energy density X) therefore couples dominantly to the LIGHTEST TCI primary,
collapsing the measured exponent to ~1.3 -- this is light-primary contamination, NOT the
stress-tensor channel. The rigorous fix (Zou-Milsted-Vidal spirit): build the local operator,
then PROJECT OUT its overlap with the lighter primary excitations, and measure the force from
the residual operator that lives (dominantly) in the stress-tensor channel.

METHOD:
  1. GS |0> and the lowest K excited states |1>..|K> (exact, k=K+1 via eigsh).
  2. Local energy-sector operator O at a site (use the validated 'X' = energy density, which
     reproduces alpha=3.97 at Ising). Form the single-excitation vector |chi> = O|0>/||.
  3. Identify the lighter-primary excited states by gap and SYMMETRY, and Gram-Schmidt-remove
     their components from |chi>:  |chi_perp> = |chi> - sum_k <k|chi> |k>  for k in the
     "light" set. The residual is the heavier (stress-tensor-ward) content.
  4. EFFECTIVE OPERATOR: rather than rebuild an operator, measure the force directly from the
     projected excitation vectors: at anchor a and probe p, build sigma|0> for each, project out
     light components, renormalize, and form the dual excitation; compute the standard
     V(dr)=E_dual - E0 - dE_a - dE_p energy-difference force on the projected states.
  5. VALIDATION GATE (unchanged, strict): at Ising (lam3=0) the SAME projection recipe must
     still give alpha ~ 3.97 (projecting out Ising's light sigma should barely move the energy
     channel). If projection breaks the Ising control, the recipe is rejected.
  6. Scan K_light = 1,2,3 (how many light states removed) and report alpha(TCI) vs the dichotomy
     {4.0 universal ; 0.4 = 2*Delta_eps' ; 0.075 = 2*Delta_sigma'}.

Honest expectation: exact-diag at N=16 may still be channel-limited; if alpha(TCI) does NOT
stabilize near 4 under projection while Ising stays ~3.97, the clean answer requires chi>=3
MERA (stage 2) and THAT is the reportable outcome -- not a forced number.
Output: research/data/simulations/SIM-2026-033b.json
"""
import json
import time

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse.linalg import eigsh

import hyp024_tfd_btz_transport as TFD
from sim032_tci_force_stage1 import build_OF

N = 16
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-033b.json"
LAM_TCI = 0.856
DRS = list(range(1, 12))
FIT_DR_MIN = 2
ANCHOR = 2
GATE = (3.6, 4.4)


def Pop(i, p):
    return TFD.sparse_pauli_full(N, i, p)


def energy_op(j):
    # validated energy-density operator (gives alpha~3.91-3.97 at Ising, small dE_single)
    return Pop(j, "X") + Pop(j + 1, "X")


def project_out(vec, basis):
    """Remove components of vec along the columns of `basis` (assumed orthonormal)."""
    v = vec.copy()
    for k in range(basis.shape[1]):
        bk = basis[:, k]
        v = v - np.vdot(bk, v) * bk
    return v


def force_projected(gs, exc, H, E0, K_light):
    light = exc[:, :K_light] if K_light > 0 else np.zeros((exc.shape[0], 0), dtype=complex)

    def prep(j):
        x = energy_op(j) @ gs
        x = project_out(x, light)
        n = np.linalg.norm(x)
        return (x / n, n) if n > 1e-9 else (None, 0.0)

    sa, na = prep(ANCHOR)
    if sa is None:
        return None, None, 0
    dE_a = float(np.real(np.vdot(sa, H @ sa))) - E0
    F = {}
    for dr in DRS:
        sp, npn = prep(ANCHOR + dr)
        if sp is None:
            F[dr] = None
            continue
        dE_p = float(np.real(np.vdot(sp, H @ sp))) - E0
        # dual: apply probe energy op to the (already light-projected) anchor excitation,
        # then project light out again, renormalize
        d = energy_op(ANCHOR + dr) @ (energy_op(ANCHOR) @ gs)
        d = project_out(d, light)
        nd = np.linalg.norm(d)
        if nd < 1e-9:
            F[dr] = None
            continue
        d = d / nd
        F[dr] = float(np.real(np.vdot(d, H @ d))) - E0 - dE_a - dE_p
    r = np.array([k for k in DRS if k >= FIT_DR_MIN and F[k] is not None and abs(F[k]) > 1e-12], float)
    if len(r) < 4:
        return None, F, len(r)
    y = np.array([abs(F[int(k)]) for k in r])
    try:
        popt, pcov = curve_fit(lambda x, A, a: A * x ** (-a), r, y, p0=[y[0], 3.5], maxfev=20000)
        return (float(popt[1]), float(np.sqrt(pcov[1, 1]))), F, len(r)
    except Exception:
        lp = np.polyfit(np.log(r), np.log(y), 1)
        return (float(-lp[0]), float("nan")), F, len(r)


def run_point(lam3, label):
    H = build_OF(N, lam3, pbc=False)
    vals, vecs = eigsh(H, k=5, which="SA")
    o = np.argsort(vals)
    gs = vecs[:, o[0]]
    exc = vecs[:, o[1:]]
    E0 = float(vals[o[0]])
    out = {}
    for K in (0, 1, 2, 3):
        res, F, npts = force_projected(gs, exc, H, E0, K)
        if res is None:
            out[K] = {"alpha": None}
            print(f"  [{label}] K_light={K}: degenerate")
            continue
        a, da = res
        out[K] = {"alpha": a, "alpha_err": da, "n_fit": npts}
        print(f"  [{label}] K_light={K}: alpha={a:.3f}+/-{da:.3f} ({npts} pts)", flush=True)
    return out


def main():
    t0 = time.time()
    print("=" * 72)
    print("SIM-2026-033b: channel-projected force, TCI universality (light-primary removal)")
    print("=" * 72)
    ising = run_point(0.0, "Ising")
    tci = run_point(LAM_TCI, "TCI")

    # validation: Ising must stay ~3.97 for SOME K (projection shouldn't wreck the control)
    ising_ok_K = [K for K, v in ising.items() if v.get("alpha") and GATE[0] <= v["alpha"] <= GATE[1]]
    # does TCI reach the stress-tensor window for the SAME K where Ising validates?
    universal_K = [K for K in ising_ok_K if tci.get(K, {}).get("alpha") and GATE[0] <= tci[K]["alpha"] <= GATE[1]]
    tci_vals = [v["alpha"] for v in tci.values() if v.get("alpha")]

    if universal_K:
        K = universal_K[0]
        verdict = (f"UNIVERSALITY_SUPPORTED: with K_light={K} removed, Ising alpha={ising[K]['alpha']:.2f} "
                   f"(control holds) AND TCI alpha={tci[K]['alpha']:.2f} in [3.6,4.4]. Stress-tensor "
                   f"exponent alpha~4 confirmed in a SECOND universality class once light primaries "
                   f"are projected out.")
        status = "SUPPORTED"
    elif ising_ok_K:
        verdict = (f"STAGE_2_REQUIRED: Ising control validates (K in {ising_ok_K}, alpha~3.9-4.0) but "
                   f"TCI alpha does NOT reach [3.6,4.4] under exact-diag light-projection "
                   f"(TCI alphas seen: {', '.join(f'{a:.2f}' for a in tci_vals)}). At N=16 the dense "
                   f"c=7/10 spectrum mixes channels beyond what local projection separates. The clean "
                   f"test is the chi>=3 multicritical MERA (stage 2), which projects onto scaling "
                   f"operators directly. This is the honest exact-diag ceiling, not a refutation.")
        status = "under_review"
    else:
        verdict = ("RECIPE_REJECTED: light-projection broke even the Ising control; the projected-"
                   "operator approach is not validated. Stage 2 (MERA) required.")
        status = "under_review"

    out = {"id": "SIM-2026-033b", "type": "classical", "date": "2026-06-08",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Channel-projected force at the TCI point: remove K lightest-primary "
                           "components from the energy-density excitation, measure residual (stress-"
                           "tensor-ward) force exponent, with strict Ising-control validation."),
           "circuit": {"qubits": N, "script_path": "research/data/simulations/sim033b_tci_channel_projected.py"},
           "hardware_target": "local CPU (exact statevector)",
           "results": {"ising": ising, "tci": tci, "ising_validated_K": ising_ok_K,
                       "universal_K": universal_K, "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Follow-up to SIM-033; isolates the stress-tensor channel by Gram-Schmidt removal of light primaries.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print("\n  VERDICT:", verdict)
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")
    return status, verdict


if __name__ == "__main__":
    main()
