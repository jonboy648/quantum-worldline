#!/usr/bin/env python3
"""
qw_channel_common.py -- primitives shared by qw_channel_test.py (open chain) and
qw_ring_test.py (PBC ring).

WHY THIS EXISTS
---------------
Extracted 2026-09-04 after a two-axis code review. Both drivers carried near-verbatim
copies of the operators, the estimators, and -- worst -- the PRE-REGISTERED A/B/C/D
decision rule, which existed as a documented function in one file and a bare if-cascade
in the other. Two copies of a pre-registered decision rule will drift, and a drifted
verdict rule silently invalidates the pre-registration it claims to honour.

GATE SEMANTICS (the other review finding)
-----------------------------------------
Every gate in the original drivers was an OBSERVATION, not a CONTROL: G1/G2/G3 and the
reproduction gate each computed a pass/fail, recorded it truthfully, printed it -- and
then nothing branched on it. One driver printed "Reporting and stopping" and did not
stop. This module supplies the missing control paths:

  RUN-LEVEL gates (GateFailure -> the run is void, no verdict is emitted):
      G1  ground-state energy vs the exact free-fermion result
      REPRO  the eps arm reproducing SIM-2026-011-interaction
  PER-ARM gates (the arm is marked void and BARRED from any discriminant):
      G2  ring symmetry F(dr) == F(n-dr)
  REPORT-ONLY (never voids, by explicit pre-registration wording):
      G3  eps continuity band -- "a sanity band, not a target: landing outside it is
          reported, not corrected away" (PREREGISTRATION-RING.md)

The per-arm distinction is not a softening. A blunt run-level G2 would have voided the
n=24 ring run entirely, destroying the valid eps/T/X measurements because the Z arm --
whose failure is itself the finding (a Z2 parity-sector obstruction) -- failed at 93%.
Voiding the arm and barring it from the verdict is the faithful reading.

NUMERICS ARE UNCHANGED. Every function here is byte-equivalent in behaviour to the copy
it replaced; the refactor is verified by re-running both drivers and diffing against the
recorded SIM-2026-073 / SIM-2026-074 values.
"""
import numpy as np

SEED = 20260817
ALPHA_BP, BETA_BP = 0.635, -0.026


class GateFailure(Exception):
    """A run-level validation gate failed. The run is void; no verdict may be emitted."""


# ------------------------------------------------------------------ tensor helpers
# Indices use the modular form (j % n). On the open chain every j is already < n, so the
# modulus is a no-op there; on the ring it closes the chain. One implementation, both uses.
def _ax(n, j):
    """Axis of bit j under C-order reshape to (2,)*n (bit k has weight 2**k)."""
    return n - 1 - (j % n)


def _flip(n, j, v):
    """X_j |v>."""
    return np.flip(v.reshape((2,) * n), axis=_ax(n, j)).reshape(-1)


def _zmul(n, j, v):
    """Z_j |v> (returns a new array)."""
    A = v.reshape((2,) * n).copy()
    sl = [slice(None)] * n
    sl[_ax(n, j)] = 1
    A[tuple(sl)] *= -1.0
    return A.reshape(-1)


def _zz_slices(n, j):
    """(equal_slices, unequal_slices) for bits j, j+1."""
    aj, aj1 = _ax(n, j), _ax(n, (j + 1) % n)
    eq, ne = [], []
    for a in (0, 1):
        for b in (0, 1):
            sl = [slice(None)] * n
            sl[aj], sl[aj1] = a, b
            (eq if a == b else ne).append(tuple(sl))
    return eq, ne


# --------------------------------------------------------------------- operators
def op_eps(n, j, sv):
    """Zou-Milsted-Vidal boundary primary. Purely off-diagonal; no vacuum subtraction
    needed (<GS|eps|GS> = 0 by Z2 parity)."""
    out = ALPHA_BP * _flip(n, j, sv)
    out += ALPHA_BP * _flip(n, (j + 1) % n, sv)
    out += BETA_BP * _flip(n, j, _zmul(n, (j + 1) % n, sv))
    out += BETA_BP * _flip(n, (j + 1) % n, _zmul(n, j, sv))
    return out


def op_T(n, j, sv, vev):
    """-(Z_j Z_{j+1} - vev), the energy density. Diagonal.
    NOTE (SIM-2026-074): at h=1 this is Kramers-Wannier dual to op_X -- the SAME
    continuum operator. It is NOT the stress tensor."""
    A = sv.reshape((2,) * n)
    out = np.empty_like(A)
    eq, ne = _zz_slices(n, j)
    for s in eq:
        out[s] = -(1.0 - vev) * A[s]
    for s in ne:
        out[s] = (1.0 + vev) * A[s]
    return out.reshape(-1)


def op_X(n, j, sv, vev):
    """X_j - vev. NOTE (SIM-2026-074): at h=1 this is the KW dual partner of op_T,
    i.e. also the energy density. It is NOT the spin primary."""
    return _flip(n, j, sv) - vev * sv


def op_Z(n, j, sv):
    """Z_j -- the true spin primary (order parameter, Delta_sigma = 1/8). Z2-ODD, so
    <Z_j> = 0 identically and vacuum subtraction is neither needed nor meaningful.
    WARNING: the energy-difference observable is UNDEFINED for this operator -- single
    excitations are Z2-odd while dual excitations are Z2-even, so F(dr) subtracts across
    symmetry sectors. See SIM-2026-074. Any arm built on it must fail its gates."""
    return _zmul(n, j, sv)


def vev_ZZ(n, j, gs):
    A = gs.reshape((2,) * n)
    eq, ne = _zz_slices(n, j)
    return float(sum(float((A[s] * A[s]).sum()) for s in eq)
                 - sum(float((A[s] * A[s]).sum()) for s in ne))


def vev_X(n, j, gs):
    return float(gs @ _flip(n, j, gs))


# --------------------------------------------------------------------- estimators
def fit_log_ols(x, y):
    """Headline estimator: OLS on log|F| vs log(x)."""
    lx, ly = np.log(x), np.log(np.abs(y))
    if len(lx) < 3:
        return np.nan, np.nan
    b, a = np.polyfit(lx, ly, 1)
    r = ly - (b * lx + a)
    s2 = r @ r / max(len(lx) - 2, 1)
    return -b, float(np.sqrt(s2 / ((lx - lx.mean()) ** 2).sum()))


def fit_relerr(x, y):
    """Cross-check estimator: NLS with errors proportional to |F|. Discards nothing;
    changes only the error model. Required by BOTH pre-registrations."""
    from scipy.optimize import curve_fit
    try:
        p, _ = curve_fit(lambda t, A, al: A * t ** (-al), x, y,
                         p0=[abs(y[0]) * x[0] ** 3, 3.0],
                         sigma=np.abs(y), absolute_sigma=False, maxfev=200000)
        return float(p[1])
    except Exception:
        return np.nan


def fit_linear_unweighted(x, y):
    """The BANNED estimator (unweighted NLS in linear space -- the one that produced the
    withdrawn alpha = 3.92). Computed for continuity ONLY. Never passed to classify()."""
    from scipy.optimize import curve_fit
    try:
        p, _ = curve_fit(lambda t, A, al: A * t ** (-al), x, y,
                         p0=[abs(y[0]) * x[0] ** 3, 3.0], maxfev=200000)
        return float(p[1])
    except Exception:
        return np.nan


def local_slopes(x, y):
    """Point-to-point log-slope -dln|F|/dln(x). FLAT for a true power law.
    Pass raw separation on a chain, chord distance on a ring."""
    lx, ly = np.log(x), np.log(np.abs(y))
    return 0.5 * (x[:-1] + x[1:]), -np.diff(ly) / np.diff(lx)


def plateau(sl, tol=0.15):
    """Longest run of consecutive local slopes whose spread is within tol (relative).
    Returns (length, mean)."""
    best = (0, np.nan)
    for i in range(len(sl)):
        for j in range(i + 3, len(sl) + 1):
            seg = sl[i:j]
            if abs(seg.mean()) > 1e-12 and (seg.max() - seg.min()) / abs(seg.mean()) <= tol:
                if j - i > best[0]:
                    best = (j - i, float(seg.mean()))
    return best


def bootstrap(x, y, n=2000, seed=SEED):
    """Nonparametric resample of the (x, F) pairs.
    CAVEAT recorded per review: over exact-diagonalization data this measures
    departure-from-power-law, not sampling error -- there is no sampling noise in an
    exact spectrum. It nonetheless feeds the pre-registered D > 3 sigma threshold, so
    that threshold is a statement about fit quality, not about statistical confidence."""
    rng = np.random.default_rng(seed)
    idx, vals = np.arange(len(x)), []
    for _ in range(n):
        s = rng.choice(idx, size=len(idx), replace=True)
        if len(np.unique(s)) < 3:
            continue
        o = np.argsort(x[s])
        a, _se = fit_log_ols(x[s][o], y[s][o])
        if np.isfinite(a) and 0 < a < 20:
            vals.append(a)
    v = np.array(vals)
    # The interpretation travels WITH the number, in the machine-readable output -- not only
    # in this docstring. A downstream reader consuming .bootstrap.std would otherwise take it
    # for a statistical error bar. Same lesson as the verdict key: prose disclaims, JSON gets
    # parsed.
    meaning = ("Resampling spread over an EXACT-diagonalization profile. There is no sampling "
               "noise in an exact spectrum, so this sigma measures DEPARTURE FROM A POWER LAW "
               "across the window, not statistical uncertainty. It feeds the pre-registered "
               "D > 3 sigma threshold, which is therefore a statement about fit quality, not "
               "about statistical confidence.")
    if v.size == 0:
        return {"mean": float("nan"), "std": float("nan"), "n": 0,
                "sigma_interpretation": meaning}
    return {"mean": float(v.mean()), "std": float(v.std(ddof=1)), "n": int(v.size),
            "sigma_interpretation": meaning}


# ------------------------------------------------------------------ gate controls
def enforce_run_gate(name, passed, detail):
    """RUN-LEVEL gate. Raises GateFailure so the caller CANNOT emit a verdict.

    This is the control path that was missing: the original drivers printed
    'Reporting and stopping' and then reported without stopping."""
    if not passed:
        raise GateFailure(f"{name} FAILED: {detail}. The run is void; no verdict emitted.")


def usable_arms(arms):
    """Arms eligible to supply a discriminant: those whose PER-ARM gates all passed.

    A gate-failed arm may still be reported (its failure is often the finding -- the Z
    arm's 93% ring-symmetry violation IS the Z2 sector obstruction of SIM-2026-074), but
    it must never reach a verdict."""
    return {k: v for k, v in arms.items() if v.get("gates_passed", True)}


def select_discriminant(arms, arm_a, arm_b):
    """Decide whether a discriminant may be computed from these two arms.

    Returns (ok, barred, reason). `ok` is False when either arm failed a per-arm gate, in
    which case NO verdict may be emitted -- the pre-registered A/B/C/D rule is not
    evaluated on invalid inputs. Extracted as a function so it can be tested behaviourally;
    a mutation test showed that string-matching the driver for a withholding branch was a
    check that could not fail."""
    usable = usable_arms(arms)
    barred = [a for a in (arm_a, arm_b) if a not in usable]
    if barred:
        return False, barred, (
            "No verdict emitted. Arm(s) " + str(barred) + " failed a per-arm validation "
            "gate and are barred from the discriminant. The pre-registered A/B/C/D rule is "
            "not evaluated on invalid inputs.")
    return True, [], ""


# --------------------------------------------------- the PRE-REGISTERED decision rule
# ONE copy. Thresholds are fixed by PREREGISTRATION.md and PREREGISTRATION-RING.md and
# must not be edited without a new pre-registration committed before the change.
THRESH = {"A_sigma": 3.0, "A_gap": 0.5, "B_sigma": 1.0, "B_gap": 0.3, "B_ratio": 2.0,
          "plateau_min_slopes": 3}


def classify(a1, s1, a2, s2, plateau_n1, plateau_n2, amp1, amp2):
    """Apply the pre-registered A/B/C/D rule. Returns (verdict, D, gap, ratio, reading).

    Arguments are (exponent, sigma, plateau_run_length, amplitude) for the two arms being
    compared. NO post-hoc reinterpretation: the D fall-through is deliberate and the
    pre-registrations state 'Do not round toward A.'"""
    den = float(np.sqrt(s1 ** 2 + s2 ** 2))
    D = abs(a1 - a2) / den if den > 0 else np.inf
    gap = abs(a1 - a2)
    ratio = max(abs(amp1), abs(amp2)) / max(min(abs(amp1), abs(amp2)), 1e-30)

    if plateau_n1 < THRESH["plateau_min_slopes"] and plateau_n2 < THRESH["plateau_min_slopes"]:
        return ("C_NO_POWER_LAW", D, gap, ratio,
                "Neither arm shows a local-slope plateau flat to 15% over >=3 consecutive "
                "slopes in the primary window. The dr^-alpha framing is unsupported for "
                "these operators.")
    if D > THRESH["A_sigma"] and gap > THRESH["A_gap"]:
        return ("A_CHANNEL_SPECIFIC", D, gap, ratio,
                "The exponent depends on which operator probes the state. alpha carries "
                "mechanism.")
    if D < THRESH["B_sigma"] and gap < THRESH["B_gap"] and ratio < THRESH["B_ratio"]:
        return ("B_CHANNEL_BLIND", D, gap, ratio,
                "The two arms are indistinguishable in form and amplitude. This REFUTES "
                "HYP-2026-008 by its own 2026-03-11 refutation_criteria: the falloff is "
                "generic, not probe-dependent.")
    return ("D_INDETERMINATE", D, gap, ratio,
            "Separation falls between the pre-registered thresholds, or form and amplitude "
            "disagree. Underpowered. Do NOT round toward A.")
