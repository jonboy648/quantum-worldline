"""
HYP-2026-028 RUN A: Does alpha=4 survive at a NON-UNITARY (Yang-Lee) critical
point reached at a FINITE distance inside the PT-unbroken phase?
=============================================================================
Successor to SIM-2026-053 (hyp028_nonunitary_force.py). SIM-053's verdict was
INCONCLUSIVE because the UNIFORM i*gamma Ising realization has its Yang-Lee point
AT the PT-breaking edge (kappa_c ~ 1/N): the non-Hermitian perturbation vanishes
as N grows, so alpha~4 there was mere PROXIMITY to the unitary point, not survival
at a genuine non-unitary fixed point. (See HYP-2026-028.json result_note_2026-06-26.)

THE REALIZATION CHOICE (Run A, documented per the design's step 1)
-----------------------------------------------------------------
The design's free-fermion H = sum c+c + m sum(2n-1) + i*g sum(2n-1) is, under
Jordan-Wigner, the SAME uniform i*gamma TFIM that failed: a UNIFORM imaginary term
is a uniform imaginary chemical potential. A single-particle probe (scratchpad/
probe_ff.py) confirms a uniform imaginary on-site potential only rigidly shifts the
spectrum in Im (gaps stay real = gauge), so it is not a genuine Yang-Lee perturbation,
while the spin-TFIM uniform-iZ pairing version PT-breaks at ~1/N. EITHER WAY uniform
is the trap.

The realization with a genuine N-INDEPENDENT FINITE PT-unbroken window is the
PT-SYMMETRIC TWO-END IMAGINARY BOUNDARY FIELD:
   H = -sum_i Z_i Z_{i+1} - sum_i X_i - i*gamma*(Z_0 - Z_{N-1})      (OBC)
PT = (spatial reflection) x (complex conjugation): reflection swaps site 0 <-> N-1
and K conjugates i*gamma -> -i*gamma, so the antisymmetric pair (+iZ_0, -iZ_{N-1})
is PT-invariant. The single-particle probe shows real gaps up to gamma ~ 0.7 at
N=12,14,16 (NO 1/N collapse) -- the finite window the design requires.

HONEST CAVEAT (carried into the G4 gate, NOT assumed away): an imaginary BOUNDARY
field drives a BOUNDARY Yang-Lee criticality. The bulk M(2,5) data (c_eff=2/5,
Delta_phi=-1/5) is a BULK fixed point. Whether this two-end realization reaches the
bulk Yang-Lee fixed point is EXACTLY what the mandatory G4 criticality gate decides.
If G4 fails, the run is INVALID (honest), not a forced verdict.

MANDATORY GATES (pre-registration, honored in order):
  G2  BIORTHOGONAL: all <O> = <L|O|R>/<L|R> from left+right ground vectors (eigs).
  G3  UNITARY CONTROL (gamma=0): MUST reproduce alpha~3.95 through the IDENTICAL layer.
  G4  NON-UNITARY CRITICALITY: c_eff = 2/5 +/- 0.05 AND Delta_phi = -1/5 +/- 0.04,
      both across N=12,14,16, BEFORE any alpha is reported. Else INVALID.
  G5  PT-unbroken (max|Im(E)| < 1e-6). Report alpha across N=12,14,16 (drift < 0.4).

Reuses the VALIDATED biorthogonal layer from hyp028_nonunitary_force.py unchanged.

Author: computation-lead (HYP-028 Run A)   Date: 2026-06-26
Output: research/data/simulations/SIM-2026-055.json  (054 is taken by HYP-029)
"""

import sys, io, json, time
import numpy as np
from scipy import sparse
from scipy.sparse.linalg import eigs

# UTF-8 safe stdout WITHOUT replacing the stream object (the replace-with-new-
# TextIOWrapper trick silently crashes when stdout is redirected to a file).
try:
    sys.stdout.reconfigure(encoding='utf-8', errors='replace')
except Exception:
    pass

# ---------------------------------------------------------------------------
# Sparse Pauli machinery (identical to the validated pipeline)
# ---------------------------------------------------------------------------
_I = sparse.eye(2, format='csr', dtype=complex)
_X = sparse.csr_matrix([[0, 1], [1, 0]], dtype=complex)
_Y = sparse.csr_matrix([[0, -1j], [1j, 0]], dtype=complex)
_Z = sparse.csr_matrix([[1, 0], [0, -1]], dtype=complex)
_PAULIS = {'I': _I, 'X': _X, 'Y': _Y, 'Z': _Z}

def kron_pauli(n, qubit_ops):
    ops = [qubit_ops.get(q, 'I') for q in range(n)]
    result = _PAULIS[ops[0]]
    for op in ops[1:]:
        result = sparse.kron(result, _PAULIS[op], format='csr')
    return result

def single_pauli(n, qubit, pauli):
    return kron_pauli(n, {qubit: pauli})

def two_pauli(n, q1, p1, q2, p2):
    return kron_pauli(n, {q1: p1, q2: p2})

# ---- boundary-primary coefficients (identical to the unitary pipeline) ----
ALPHA_BP = 0.635
BETA_BP = -0.026

def build_bp_operator(n, j):
    op = ALPHA_BP * (single_pauli(n, j, 'X') + single_pauli(n, j + 1, 'X'))
    op += BETA_BP * (two_pauli(n, j, 'X', j + 1, 'Z') +
                     two_pauli(n, j, 'Z', j + 1, 'X'))
    return op

# ---------------------------------------------------------------------------
# Hamiltonians
# ---------------------------------------------------------------------------
def build_tfim_unitary(n):
    """Hermitian critical Ising (gamma=0): -sum ZZ - sum X. The G3 control point."""
    dim = 1 << n
    H = sparse.csr_matrix((dim, dim), dtype=complex)
    for i in range(n - 1):
        H -= two_pauli(n, i, 'Z', i + 1, 'Z')
    for i in range(n):
        H -= single_pauli(n, i, 'X')
    return H

def build_twoend_pt(n, gamma):
    """PT-symmetric two-end imaginary boundary field (Run A realization):
       H = -sum ZZ - sum X - i*gamma*(Z_0 - Z_{n-1}).
    Antisymmetric (+iZ_0, -iZ_{n-1}) is invariant under PT = reflection*K.
    Single-particle probe: real gaps to gamma~0.7 at N=12,14,16 (no 1/N collapse)."""
    H = build_tfim_unitary(n)
    H -= (1j * gamma) * single_pauli(n, 0, 'Z')
    H += (1j * gamma) * single_pauli(n, n - 1, 'Z')
    return H

def build_uniform_iz(n, gamma):
    """SIM-053 realization (reference only): -sum ZZ - sum X - i*gamma*sum Z.
    Yang-Lee point sits AT the PT-edge (kappa_c ~ 1/N). Kept for cross-check."""
    H = build_tfim_unitary(n)
    for i in range(n):
        H -= (1j * gamma) * single_pauli(n, i, 'Z')
    return H

# ---------------------------------------------------------------------------
# G2: biorthogonal ground vectors + <L|O|R>/<L|R> layer (reused VERBATIM)
# ---------------------------------------------------------------------------
def ground_LR(H):
    """(E0, |R>, <L|) for the lowest-real-part eigenvalue, biorthonormalized <L|R>=1.
    H|R>=E0|R>;  H^dag|L>=conj(E0)|L>  so  <L|H = E0<L|. Uses eigs (non-Hermitian)."""
    valsR, vecsR = eigs(H, k=1, which='SR', maxiter=20000, tol=1e-12)
    E0 = complex(valsR[0]); R = vecsR[:, 0].astype(complex)
    valsL, vecsL = eigs(H.conj().T, k=1, which='SR', maxiter=20000, tol=1e-12)
    L = vecsL[:, 0].astype(complex)
    overlap = np.vdot(L, R)  # <L|R>
    if abs(overlap) < 1e-12:
        raise RuntimeError(f"biorthogonal overlap ~0 ({overlap}); PT-broken or degenerate.")
    L = L / np.conj(overlap)  # scale so <L|R>=1
    return E0, R, L

def bexpect(L, O, R):
    """<L|O|R>/<L|R> with <L|R>=1 pre-normalized -> = <L|O|R>."""
    return complex(np.vdot(L, O @ R))

# ---------------------------------------------------------------------------
# G4: non-unitary criticality gate
#   (1) c_eff from biorthogonal entanglement entropy S(L) vs the Calabrese-Cardy
#       chord length on an OBC chain: S(L) = (c_eff/6) ln[ (2N/pi) sin(pi L/N) ] + const.
#       The biorthogonal RDM is rho_A = Tr_B |R><L| (right ket, left bra), which is the
#       standard non-Hermitian entanglement-entropy prescription (eigenvalues can be
#       complex; we use S = -sum lam ln lam over the complex spectrum, real part reported).
#   (2) Delta_phi from the finite-size gap:  E_1 - E_0 = (pi v / N) * Delta_phi, with the
#       Luttinger velocity v fixed by the UNITARY Ising point (v=2 in these units, the
#       known Ising sound speed for H=-ZZ-X), so Delta_phi = (E1-E0)*N/(pi v).
# ---------------------------------------------------------------------------
ISING_VELOCITY = 2.0  # sound speed of H=-sum ZZ - sum X (critical TFIM), standard.

def biorthogonal_rdm(R, L, n, cut):
    """Biorthogonal RDM whose eigenvalues give the block entanglement entropy of the
    first `cut` sites. |R>=sum R[a,b]|a>|b>, <L|=sum conj(L[a,b])<a|<b|, <L|R>=1.
       rho_A[a,a'] = sum_b R[a,b] conj(L[a',b]) = Rm @ Lm.conj().T   (size 2^cut)
       rho_B[b,b'] = sum_a R[a,b] conj(L[a,b']) = Rm.T @ Lm.conj()   (size 2^{N-cut})
    rho_A and rho_B share nonzero eigenvalues (same entropy), so we return whichever is
    SMALLER to cap the dense matrix at 2^(N/2) x 2^(N/2) (avoids the 2^14 OOM)."""
    dA = 1 << cut; dB = 1 << (n - cut)
    Rm = R.reshape(dA, dB); Lm = L.reshape(dA, dB)
    if cut <= n - cut:
        return Rm @ Lm.conj().T            # (2^cut, 2^cut)
    else:
        return Rm.T @ Lm.conj()            # (2^{N-cut}, 2^{N-cut})

def biorthogonal_entropy(R, L, n, cut):
    """S = -sum_k lam_k ln(lam_k) over the (complex) eigenvalues of the biorthogonal RDM.
    Returns (S_real, S_imag, trace) -- trace should be ~1 (since <L|R>=1)."""
    rho = biorthogonal_rdm(R, L, n, cut)
    lam = np.linalg.eigvals(rho)
    tr = complex(np.sum(lam))
    # drop ~0 eigenvalues to avoid log(0); use principal branch of log
    lam = lam[np.abs(lam) > 1e-12]
    S = -np.sum(lam * np.log(lam))
    return float(np.real(S)), float(np.imag(S)), tr

def measure_ceff(H, R, L, n):
    """Fit S(L) over interior cuts to (c_eff/6) ln[(2N/pi) sin(pi L/N)] + b."""
    cuts = list(range(2, n - 1))  # avoid the very ends (boundary entropy noise)
    chord = []
    S = []
    Sim = []
    for c in cuts:
        sr, si, tr = biorthogonal_entropy(R, L, n, c)
        x = np.log((2.0 * n / np.pi) * np.sin(np.pi * c / n))
        chord.append(x); S.append(sr); Sim.append(abs(si))
    chord = np.array(chord); S = np.array(S)
    # linear fit S = (c_eff/6) * chord + b
    A = np.vstack([chord, np.ones_like(chord)]).T
    coef, *_ = np.linalg.lstsq(A, S, rcond=None)
    c_eff = 6.0 * coef[0]
    return {"c_eff": float(c_eff), "slope": float(coef[0]), "intercept": float(coef[1]),
            "S_real": [float(s) for s in S], "S_imag_max": float(np.max(Sim)),
            "cuts": cuts}

def low_spectrum(H, n, k=6):
    """First k eigenvalues by smallest real part; report real parts, max|Im|, gap."""
    k = min(k, (1 << n) - 2)
    vals = eigs(H, k=k, which='SR', maxiter=20000, tol=1e-11, return_eigenvectors=False)
    order = np.argsort(vals.real)
    vals = vals[order]
    re = vals.real
    im_max = float(np.max(np.abs(vals.imag)))
    gap = float(re[1] - re[0]) if len(re) > 1 else float('nan')
    return {"low_real": [float(x) for x in re[:4]],
            "low_imag": [float(x) for x in vals.imag[:4]],
            "gap_re": gap, "max_abs_imag": im_max, "pt_unbroken": im_max < 1e-6}

def measure_delta_phi(H, n):
    """Delta_phi from gap: E1-E0 = (pi v / N) Delta_phi  ->  Delta_phi = (E1-E0) N /(pi v)."""
    sp = low_spectrum(H, n)
    delta_phi = sp["gap_re"] * n / (np.pi * ISING_VELOCITY)
    sp["delta_phi"] = float(delta_phi)
    return sp

# ---------------------------------------------------------------------------
# fit back-end (reused)
# ---------------------------------------------------------------------------
from scipy.optimize import curve_fit

def powerlaw_model(x, A, alpha):
    return A * np.power(np.array(x, dtype=float), -alpha)

def fit_powerlaw(dr_arr, v_arr):
    x = np.array(dr_arr, dtype=float); y = np.array(v_arr, dtype=float)
    try:
        popt, pcov = curve_fit(powerlaw_model, x, y, p0=[y[0], 1.0], maxfev=40000,
                               bounds=([-50, 0.01], [50, 12]))
        return True, popt, np.sqrt(np.diag(pcov))
    except Exception as e:
        return False, None, str(e)

# ---------------------------------------------------------------------------
# Force measurement at (N, builder, gamma) through the biorthogonal layer
# (estimator IDENTICAL to the validated SIM-053/SIM-015d pipeline)
# ---------------------------------------------------------------------------
def measure_force(n, builder, gamma, dr_max=None, verbose=True):
    anchor = n // 4
    if dr_max is None:
        dr_max = n - anchor - 2
    valid_drs = [dr for dr in range(1, dr_max + 1) if anchor + dr + 1 < n]

    H = builder(n, gamma) if gamma is not None else builder(n)
    E0, R, L = ground_LR(H)
    crit_spec = measure_delta_phi(H, n)            # G4 part (2) + PT (G5)
    crit_ee = measure_ceff(H, R, L, n)             # G4 part (1)

    def excite(Lin, Rin, j):
        sig = build_bp_operator(n, j)
        Rout = sig @ Rin
        Lout = sig.conj().T @ Lin
        ov = np.vdot(Lout, Rout)
        if abs(ov) < 1e-12:
            return None, None, False
        return Lout / np.conj(ov), Rout, True

    E0r = bexpect(L, H, R)

    L_a, R_a, ok_a = excite(L, R, anchor)
    if not ok_a:
        raise RuntimeError(f"anchor excitation zero biorthogonal norm at N={n}, gamma={gamma}")
    dE_anchor = bexpect(L_a, H, R_a) - E0r

    V_dual = {}
    for dr in valid_drs:
        j = anchor + dr
        L_p, R_p, ok_p = excite(L, R, j)
        if not ok_p:
            V_dual[dr] = 0.0; continue
        dE_probe = bexpect(L_p, H, R_p) - E0r
        L_d, R_d, ok_d = excite(L_a, R_a, j)
        if not ok_d:
            V_dual[dr] = 0.0; continue
        E_dual = bexpect(L_d, H, R_d)
        V_dual[dr] = E_dual - E0r - dE_anchor - dE_probe

    V_real = {dr: float(np.real(v)) for dr, v in V_dual.items()}
    V_imag_max = max((abs(np.imag(v)) for v in V_dual.values()), default=0.0)

    dr_fit = [dr for dr in valid_drs if dr >= 2 and abs(V_real[dr]) > 1e-14]
    vals = [V_real[dr] for dr in dr_fit]
    fit = {}
    if len(dr_fit) >= 3:
        ok, popt, perr = fit_powerlaw(dr_fit, vals)
        if ok:
            fit = {"alpha": float(popt[1]), "dalpha": float(perr[1]),
                   "A": float(popt[0]), "dA": float(perr[0]), "n_points": len(dr_fit)}
        else:
            fit = {"error": str(perr)}

    if verbose:
        gtxt = f"{gamma:.4f}" if gamma is not None else "0(unitary)"
        print(f"  N={n} gamma={gtxt}: E0={E0.real:+.5f}{E0.imag:+.2e}i  "
              f"PT={crit_spec['pt_unbroken']}  gap={crit_spec['gap_re']:+.4f}  "
              f"Dphi={crit_spec['delta_phi']:+.4f}  c_eff={crit_ee['c_eff']:+.4f}  "
              f"V_imax={V_imag_max:.1e}")
        print(f"     V(real): " + "  ".join(f"{dr}:{V_real[dr]:+.4e}" for dr in valid_drs))
        if fit.get("alpha") is not None:
            print(f"     alpha = {fit['alpha']:.4f} +/- {fit['dalpha']:.4f}  (n={fit['n_points']})")

    return {"N": n, "gamma": (float(gamma) if gamma is not None else 0.0),
            "anchor": anchor, "E0_re": float(E0.real), "E0_im": float(E0.imag),
            "crit_spec": crit_spec, "crit_ee": crit_ee,
            "V_real": {str(k): v for k, v in V_real.items()},
            "V_imag_max": float(V_imag_max), "fit": fit}

# ---------------------------------------------------------------------------
# Yang-Lee critical-point locator: scan gamma, watch c_eff and Delta_phi.
# At the Yang-Lee bulk fixed point c_eff -> 2/5 and Delta_phi -> -1/5.
# We pick gamma_c(N) = the PT-unbroken gamma whose (c_eff, Delta_phi) is closest to
# the M(2,5) target, as a NUMERICAL search (the gate then judges it on the targets).
# ---------------------------------------------------------------------------
C_EFF_TARGET = 2.0 / 5.0       # 0.40
DELTA_PHI_TARGET = -1.0 / 5.0  # -0.20
C_EFF_TOL = 0.05
DELTA_PHI_TOL = 0.04

def locate_yanglee(n, builder, gammas, verbose=True):
    """Scan gammas (PT-unbroken only); return the gamma minimizing a combined distance
    to (c_eff=2/5, Delta_phi=-1/5), plus the full scan trace. During the scan we use a
    CHEAP single mid-cut entropy as the c_eff proxy (full multi-cut fit only happens at
    the selected gamma_c, inside measure_force). This keeps the N=16 scan tractable."""
    trace = []
    best = None
    for g in gammas:
        H = builder(n, g)
        try:
            E0, R, L = ground_LR(H)
        except Exception as e:
            trace.append({"gamma": g, "error": str(e)}); continue
        sp = measure_delta_phi(H, n)
        sr, si, tr = biorthogonal_entropy(R, L, n, n // 2)  # cheap mid-cut proxy
        rec = {"gamma": float(g), "S_mid": float(sr), "delta_phi": sp["delta_phi"],
               "pt_unbroken": sp["pt_unbroken"], "max_abs_imag": sp["max_abs_imag"]}
        trace.append(rec)
        if not sp["pt_unbroken"]:
            if verbose:
                print(f"     scan g={g:6.3f}: S_mid={sr:+.3f} Dphi={sp['delta_phi']:+.3f} "
                      f"PT=False (|Im|={sp['max_abs_imag']:.1e})  [skip]")
            continue
        # rank PT-unbroken points by Delta_phi distance to -1/5 (the unambiguous Yang-Lee
        # signature); S_mid is logged but the multi-cut c_eff is judged later at gamma_c.
        dist = ((sp["delta_phi"] - DELTA_PHI_TARGET) / DELTA_PHI_TOL) ** 2
        if best is None or dist < best["dist"]:
            best = {"gamma": float(g), "dist": float(dist),
                    "S_mid": float(sr), "delta_phi": sp["delta_phi"]}
        if verbose:
            print(f"     scan g={g:6.3f}: S_mid={sr:+.3f} Dphi={sp['delta_phi']:+.3f} "
                  f"PT=True (|Im|={sp['max_abs_imag']:.1e})")
    return best, trace


def main():
    print("=" * 78)
    print("HYP-028 RUN A: alpha=4 at a FINITE-WINDOW non-unitary (Yang-Lee) point")
    print("Realization: PT-symmetric two-end imaginary boundary field -iY(Z0 - Z_{N-1})")
    print("=" * 78)
    t0 = time.time()
    SIZES = (12, 14, 16)

    out = {"id": "SIM-2026-055", "hypothesis_id": "HYP-2026-028", "date": "2026-06-26",
           "run": "A: Yang-Lee non-unitary force via PT-symmetric two-end imaginary "
                  "boundary field (finite PT-unbroken window)",
           "model": "H = -sum ZZ - sum X - i*gamma*(Z_0 - Z_{N-1}), OBC",
           "realization_rationale": "uniform i*gamma (SIM-053) has Yang-Lee point AT the "
               "PT edge (kappa_c~1/N, PT breaks at g~0.02 at these N); the two-end PT field "
               "has a LARGER many-body PT-unbroken window (g<~0.17 at N=10, ~0.14 at N=12) "
               "that still shrinks with N. The single-particle (number-conserving) probe "
               "suggested g~0.7, but the paired spin TFIM many-body window is smaller.",
           "ceff_target": C_EFF_TARGET, "delta_phi_target": DELTA_PHI_TARGET,
           "ising_velocity": ISING_VELOCITY, "biorthogonal": True, "runs": {}}

    # ---- G3: UNITARY CONTROL (gamma=0) through the IDENTICAL biorthogonal layer ----
    print("\n[G3] UNITARY CONTROL (gamma=0) -- MUST give alpha~3.95")
    ctrl = {}
    for n in SIZES:
        r = measure_force(n, build_tfim_unitary, None)
        ctrl[n] = r
        out["runs"][f"unitary_N{n}"] = r
    ctrl_alpha16 = ctrl[16]["fit"].get("alpha")
    control_ok = (ctrl_alpha16 is not None) and (3.2 <= ctrl_alpha16 <= 4.8)
    print(f"\n  Control alpha(N=16) = {ctrl_alpha16}  -> biorthogonal layer "
          f"{'VALIDATED' if control_ok else 'BROKEN'}")

    # ---- Locate the Yang-Lee critical gamma_c(N) on the two-end realization ----
    # Window (measured, scratchpad/scan_lean.py): PT-unbroken to g~0.17(N=10)/0.14(N=12),
    # shrinking with N. Grid samples densely inside and just past the edge so the locator
    # can pick the best PT-unbroken point AND the gate can see whether c_eff/Dphi ever reach
    # the Yang-Lee targets before PT breaks.
    print("\n[locate] scan gamma for the Yang-Lee fixed point (c_eff->2/5, Dphi->-1/5)")
    GAMMA_SCAN = [0.02, 0.04, 0.06, 0.08, 0.10, 0.11, 0.12, 0.13, 0.14, 0.15, 0.16, 0.18, 0.20]
    gc = {}
    for n in SIZES:
        print(f"   N={n}:")
        best, trace = locate_yanglee(n, build_twoend_pt, GAMMA_SCAN)
        gc[n] = best
        out["runs"][f"locate_N{n}"] = {"best": best, "trace": trace}
        print(f"     -> best gamma_c(N={n}) = {best}")

    # ---- G4 + G5 + force at the located gamma_c(N) ----
    print("\n[G4/G5] criticality gate + force at gamma_c(N)")
    nu = {}
    gate_pass = {}
    for n in SIZES:
        if gc[n] is None:
            print(f"  N={n}: no PT-unbroken gamma found -> skip"); nu[n] = None; gate_pass[n] = False
            continue
        g = gc[n]["gamma"]
        r = measure_force(n, build_twoend_pt, g)
        nu[n] = r
        out["runs"][f"nonunitary_N{n}"] = r
        ce = r["crit_ee"]["c_eff"]; dp = r["crit_spec"]["delta_phi"]
        pt = r["crit_spec"]["pt_unbroken"]
        ce_ok = abs(ce - C_EFF_TARGET) <= C_EFF_TOL
        dp_ok = abs(dp - DELTA_PHI_TARGET) <= DELTA_PHI_TOL
        gate_pass[n] = bool(pt and ce_ok and dp_ok)
        print(f"  N={n}: c_eff={ce:+.4f}({'OK' if ce_ok else 'FAIL'}) "
              f"Dphi={dp:+.4f}({'OK' if dp_ok else 'FAIL'}) PT={pt} -> G4 "
              f"{'PASS' if gate_pass[n] else 'FAIL'}")

    g4_all = all(gate_pass[n] for n in SIZES)
    pt_all = all((nu[n] is not None and nu[n]["crit_spec"]["pt_unbroken"]) for n in SIZES)
    nu_alpha = {n: (nu[n]["fit"].get("alpha") if nu[n] else None) for n in SIZES}
    have_all = all(a is not None for a in nu_alpha.values())
    nu_a16 = nu_alpha[16]
    drift = (max(a for a in nu_alpha.values() if a is not None) -
             min(a for a in nu_alpha.values() if a is not None)) if have_all else float('nan')

    # ---- pre-registered verdict logic ----
    print("\n" + "=" * 78)
    print("VERDICT (pre-registered)")
    print("=" * 78)
    print(f"  G3 control_ok (alpha~4 @ gamma=0) : {control_ok} (alpha16={ctrl_alpha16})")
    print(f"  G4 criticality gate (all N)       : {g4_all}  per-N={gate_pass}")
    print(f"  G5 PT-unbroken (all N)            : {pt_all}")
    print(f"  non-unitary alpha (N=12,14,16)    : {nu_alpha}")
    print(f"  alpha drift across N              : {drift}")

    if not control_ok:
        verdict = "INVALID: G3 unitary control did not reproduce alpha~4; biorthogonal estimator broken."
    elif not g4_all:
        verdict = ("INVALID: G4 criticality gate FAILED (c_eff!=2/5 or Delta_phi!=-1/5); the two-end "
                   "realization did NOT reach the bulk Yang-Lee fixed point at these N. NOT a refutation -- "
                   "the realization is wrong/under-resolved, alpha is uninterpretable. Honest negative.")
    elif not pt_all:
        verdict = "INCONCLUSIVE: PT-symmetry broken (complex energies) at gamma_c; force undefined."
    elif nu_a16 is None:
        verdict = "INVALID: non-unitary fit failed."
    elif drift == drift and drift > 0.4:
        verdict = f"INCONCLUSIVE: alpha drifts {drift:.2f} across N (finite-size dominated)."
    elif 3.2 <= nu_a16 <= 4.8:
        verdict = (f"REFUTED (stronger universality): non-unitary alpha={nu_a16:.3f} INSIDE [3.2,4.8] and "
                   "stable at a CONFIRMED Yang-Lee fixed point -> alpha=4 is GENERIC, survives loss of unitarity.")
    else:
        verdict = (f"SUPPORTED: non-unitary alpha={nu_a16:.3f} OUTSIDE [3.2,4.8] at a CONFIRMED Yang-Lee "
                   "fixed point -> alpha=4 is CONDITIONAL on unitarity; the force tracks the model primary.")
    print("\n  >>> " + verdict)

    out["control_ok"] = bool(control_ok)
    out["g4_gate_pass"] = bool(g4_all)
    out["g4_gate_pass_byN"] = {str(k): bool(v) for k, v in gate_pass.items()}
    out["pt_unbroken_all"] = bool(pt_all)
    out["control_alpha_N16"] = ctrl_alpha16
    out["nonunitary_alpha"] = {str(k): v for k, v in nu_alpha.items()}
    out["gamma_c_byN"] = {str(k): (gc[k]["gamma"] if gc[k] else None) for k in SIZES}
    out["verdict"] = verdict
    out["runtime_s"] = time.time() - t0
    with open("D:/quantum-worldline/research/data/simulations/SIM-2026-055.json", "w",
              encoding="utf-8") as f:
        json.dump(out, f, indent=2)
    print(f"\nSaved SIM-2026-055.json  ({out['runtime_s']:.1f}s)")


if __name__ == "__main__":
    import traceback
    try:
        main()
    except Exception:
        tb = traceback.format_exc()
        print("\n!!! RUN A CRASHED !!!\n" + tb, flush=True)
        with open("D:/quantum-worldline/research/data/simulations/SIM-2026-055.json", "w",
                  encoding="utf-8") as f:
            json.dump({"id": "SIM-2026-055", "hypothesis_id": "HYP-2026-028",
                       "status": "CRASHED", "traceback": tb}, f, indent=2)
        sys.exit(1)
