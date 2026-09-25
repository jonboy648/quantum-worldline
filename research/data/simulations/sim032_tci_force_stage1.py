"""
SIM-2026-032 (stage 1) — HYP-2026-027: is alpha~4 universal? Tricritical-Ising test, exact diag.

DESIGN AMENDMENT (recorded): HYP-027 registered the "ANNNI route" to c=7/10, but no documented
coupling coordinates exist for a TCI point on the vanilla transverse-field ANNNI line. The
O'Brien-Fendley chain (arXiv:1712.06662, PRL 120, 206403) provides an EXACTLY-LOCATED spin-1/2
TCI point and satisfies the registered design's intent better (2-level sites, 2x2 Paulis,
documented couplings, ~3-line Hamiltonian edit):
    H = 2*lam_I * H_I + lam3 * H_3,   H_I = -sum_j (X_j + Z_j Z_{j+1}),
    H_3 = +sum_j (X_j Z_{j+1} Z_{j+2} + Z_j Z_{j+1} X_{j+2})        [PBC]
    Self-dual line; critical Ising (c=1/2) for 0 <= lam3/lam_I < 0.856;
    TRICRITICAL Ising (c=7/10) at lam3/lam_I ~= 0.856.
KEY DESIGN WIN: lam3=0 is our published Ising anchor -> the same pipeline runs at BOTH ends;
the Ising end is a built-in control that must reproduce alpha~4 before the TCI number counts.

STAGE 1 (this script, exact diag, N=16 PBC):
  GATE A (central charge): half-chain-block entanglement S(l) = (c/3) ln[(N/pi) sin(pi l/N)] + k
     (Calabrese-Cardy, PBC). Fit c at lam3=0 (expect ~0.50) and lam3=0.856 (expect ~0.70).
  GATE B (Ising-end control): force pipeline at lam3=0 must give alpha in [3.2, 4.8].
  MEASUREMENT: same pipeline at lam3=0.856. Dichotomy: universal alpha=4.0 vs primary-tracking
     2*Delta_eps(TCI) = 0.4. Excitation operator: local sigma^z pair (order parameter), with the
     legitimate energy-difference estimator V(dr) = E_dual - E0 - 2*(E_single - E0).
Stage 2 (separate, later): chi>=3 MERA optimization at the TCI point (hardware/circuit story).
Output: research/data/simulations/SIM-2026-032.json
"""
import json
import time

import numpy as np
from scipy.optimize import curve_fit
from scipy.sparse import csr_matrix
from scipy.sparse.linalg import eigsh

import brickwork_force_check as FC
import hyp024_tfd_btz_transport as TFD

N = 16
OUT = "D:/quantum-worldline/research/data/simulations/SIM-2026-032.json"
LAM_TCI = 0.856
DRS = list(range(1, 12))  # published config: anchor=2, dr=1..11 (probe+1 < N)
FIT_DR_MIN = 2            # published fit window: dr >= 2
WINDOW = (3.2, 4.8)


def build_OF(N, lam3, lamI=1.0, pbc=True):
    """O'Brien-Fendley Hamiltonian. PBC for the c-gate; OBC for the force measurement
    (the published 16q Ising force, SIM-2026-015d, used build_tfim_obc — PBC chord
    geometry flattens the F(r) tail and was caught by Gate B on the first run)."""
    dim = 2 ** N
    H = csr_matrix((dim, dim), dtype=complex)
    P = lambda i, p: TFD.sparse_pauli_full(N, i % N, p)
    for j in range(N):
        H = H - 2 * lamI * P(j, "X")
        if pbc or j + 1 < N:
            H = H - 2 * lamI * (P(j, "Z") @ P(j + 1, "Z"))
        if lam3 != 0.0 and (pbc or j + 2 < N):
            H = H + lam3 * (P(j, "X") @ P(j + 1, "Z") @ P(j + 2, "Z")
                            + P(j, "Z") @ P(j + 1, "Z") @ P(j + 2, "X"))
    return H


def entanglement_c(psi, N):
    """Fit central charge from block entropies S(l), l=2..N/2, PBC Calabrese-Cardy."""
    ls = np.arange(2, N // 2 + 1)
    S = []
    for l in ls:
        m = psi.reshape(2 ** l, 2 ** (N - l))
        s = np.linalg.svd(m, compute_uv=False)
        p = s ** 2
        p = p[p > 1e-14]
        S.append(float(-np.sum(p * np.log(p))))
    x = np.log((N / np.pi) * np.sin(np.pi * ls / N))
    coef = np.polyfit(x, S, 1)
    return float(3.0 * coef[0]), ls.tolist(), S


def force_profile_bp(psi0, H, N, drs):
    """V(dr) = E_dual - E0 - 2(E_single - E0), exciting with the published BOUNDARY-PRIMARY
    operator FC.bp_op (hermitian, NON-unitary). NOTE: a bare-Z excitation is unitary, so it
    merely conjugates H and V(dr) vanishes identically by translation invariance (verified:
    first run gave |F|<1e-12 everywhere) -- the non-unitary primary is required, exactly as
    in the published pipeline. The Ising-end control validates this operator choice."""
    E0 = float(np.real(np.vdot(psi0, H @ psi0)))
    base = 2  # published anchor (SIM-015d: ANCHOR=2)
    sig0 = FC.bp_op(N, base)
    ps = sig0 @ psi0
    ps = ps / np.linalg.norm(ps)
    dE_a = float(np.real(np.vdot(ps, H @ ps))) - E0
    F = {}
    for dr in drs:
        j = base + dr
        sigp = FC.bp_op(N, j)
        # PER-SITE single-excitation subtraction (published formula; on OBC sites are
        # inequivalent and a 2x-anchor subtraction leaves an epsilon-channel residue --
        # exactly the alpha~2 contamination Gate B caught in runs 1-2)
        pp = sigp @ psi0
        pp = pp / np.linalg.norm(pp)
        dE_p = float(np.real(np.vdot(pp, H @ pp))) - E0
        pd = sigp @ (sig0 @ psi0)
        nrm = np.linalg.norm(pd)
        if nrm < 1e-12:
            F[dr] = None
            continue
        pd = pd / nrm
        E_dual = float(np.real(np.vdot(pd, H @ pd)))
        F[dr] = E_dual - E0 - dE_a - dE_p
    return F, E0, dE_a


def fit_alpha(F, drs):
    """|F| ~ A * dr^-alpha on the attractive points."""
    r = np.array([d for d in drs if d >= FIT_DR_MIN and F[d] is not None and abs(F[d]) > 1e-12], float)
    if len(r) < 3:
        return float("nan"), float("nan")  # degenerate profile -- gates will report it
    y = np.array([abs(F[int(d)]) for d in r])
    try:
        popt, pcov = curve_fit(lambda x, A, a: A * x ** (-a), r, y,
                               p0=[abs(y[0]), 3.0], maxfev=20000)
        return float(popt[1]), float(np.sqrt(pcov[1, 1]))
    except Exception:
        lp = np.polyfit(np.log(r), np.log(y), 1)
        return float(-lp[0]), float("nan")


def run_point(lam3, label):
    t = time.time()
    # c-gate on the PBC ground state (Calabrese-Cardy PBC formula)
    Hp = build_OF(N, lam3, pbc=True)
    Egp, psip = eigsh(Hp, k=1, which="SA")
    c_fit, ls, S = entanglement_c(psip[:, 0], N)
    # force on the OBC ground state (matches the published SIM-015d configuration)
    H = build_OF(N, lam3, pbc=False)
    Eg, psis = eigsh(H, k=1, which="SA")
    psi = psis[:, 0]
    F, E0, Es = force_profile_bp(psi, H, N, DRS)
    alpha, da = fit_alpha(F, DRS)
    rec = {"lam3_over_lamI": lam3, "E_gs": float(Eg[0]), "c_fit": c_fit,
           "block_entropies": dict(zip(map(str, ls), S)),
           "F": {str(d): F[d] for d in DRS}, "alpha": alpha, "alpha_err": da,
           "wall_s": time.time() - t}
    print(f"  [{label}] lam3={lam3}: c={c_fit:.4f}, alpha={alpha:.3f}+/-{da:.3f}", flush=True)
    return rec


def main():
    t0 = time.time()
    print("=" * 72)
    print("SIM-2026-032 stage 1: TCI universality of alpha (O'Brien-Fendley, exact 16q)")
    print("=" * 72)
    ising = run_point(0.0, "Ising control")
    tci = run_point(LAM_TCI, "TCI point")

    gateA_ising = abs(ising["c_fit"] - 0.5) < 0.08
    gateA_tci = abs(tci["c_fit"] - 0.7) < 0.08
    gateB = WINDOW[0] <= ising["alpha"] <= WINDOW[1]
    in_window = WINDOW[0] <= tci["alpha"] <= WINDOW[1]
    near_primary = abs(tci["alpha"] - 0.4) < 0.5  # 2*Delta_eps(TCI)=0.4

    if not (gateA_ising and gateA_tci):
        verdict = (f"GATE_A_FAILED: c-fit Ising={ising['c_fit']:.3f} (want 0.50), "
                   f"TCI={tci['c_fit']:.3f} (want 0.70) — point location/finite-size issue; "
                   f"alpha numbers NOT reportable")
    elif not gateB:
        verdict = (f"GATE_B_FAILED: Ising-end control alpha={ising['alpha']:.2f} outside {WINDOW} "
                   f"with Z-pair excitation — operator choice not calibrated; do not interpret TCI")
    elif in_window:
        verdict = (f"UNIVERSALITY_SUPPORTED (stage 1): TCI alpha={tci['alpha']:.2f} in {WINDOW} "
                   f"with both gates passed — second universality class shows the stress-tensor exponent")
    elif near_primary:
        verdict = (f"PRIMARY_TRACKING (stage-1 refutation signal): TCI alpha={tci['alpha']:.2f} "
                   f"near 2*Delta_eps=0.4 — force tracks the model's lightest primary, NOT universal")
    else:
        verdict = (f"INCONCLUSIVE: TCI alpha={tci['alpha']:.2f} matches neither 4.0 nor 0.4 cleanly "
                   f"— needs N=20+ / MERA stage 2 / operator variants")

    out = {"id": "SIM-2026-032", "type": "classical", "date": "2026-06-08",
           "hypothesis_id": "HYP-2026-027",
           "description": ("Stage-1 exact-diag test of alpha universality at the tricritical Ising "
                           "point using the O'Brien-Fendley chain (design amendment from ANNNI — "
                           "documented TCI coordinates lam3/lamI=0.856, arXiv:1712.06662). Gates: "
                           "central-charge fit (0.5 / 0.7) + Ising-end pipeline control."),
           "circuit": {"qubits": N, "script_path": "research/data/simulations/sim032_tci_force_stage1.py"},
           "hardware_target": "local CPU (exact statevector)",
           "results": {"ising_control": ising, "tci_point": tci,
                       "gates": {"cA_ising": gateA_ising, "cA_tci": gateA_tci, "B_control": gateB},
                       "dichotomy": {"universal": 4.0, "primary_tracking": 0.4},
                       "verdict": verdict},
           "comparison": "classical_wins",
           "notes": "Stage 2 (chi>=3 MERA at the TCI point, hardware story) pending stage-1 outcome.",
           "wall_seconds": time.time() - t0}
    with open(OUT, "w") as f:
        json.dump(out, f, indent=2)
    print(f"\n  VERDICT: {verdict}")
    print(f"  saved -> {OUT} ({out['wall_seconds']:.0f}s)")


if __name__ == "__main__":
    main()
