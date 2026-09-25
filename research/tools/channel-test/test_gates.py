#!/usr/bin/env python3
"""
test_gates.py -- NEGATIVE tests for the validation gates and the pre-registered verdict rule.

Run:  python test_gates.py      (exit 0 = pass, 1 = failures)

WHY THESE ARE NEGATIVE TESTS
----------------------------
A two-axis code review (2026-09-04) found that every gate in these drivers was an
OBSERVATION rather than a CONTROL: G1/G2/G3 and the reproduction gate each computed a
pass/fail, recorded it truthfully, printed it, and then nothing branched on it. One
driver printed "Reporting and stopping" and did not stop; a ring arm that failed its
symmetry gate at 93% (against a 1% bar) went on to supply the headline verdict.

So asserting the PASS path here would be worthless -- the old code passed too. Every test
below asserts that something CAN FAIL: that the gate raises, that the barred arm is
actually barred, that the thresholds have not drifted, and that the verdict rule does not
round toward the interesting answer. This project has twice been bitten by checks that
could not fail (a json.load that accepts NaN; three same-origin notes agreeing about an
external status). These tests exist so that cannot happen a third time in this code.
"""
import importlib.util as u
import inspect
import io
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = u.spec_from_file_location("qw_channel_common", os.path.join(HERE, "qw_channel_common.py"))
c = u.module_from_spec(spec)
spec.loader.exec_module(c)

fails = []


def check(cond, msg):
    if not cond:
        fails.append(msg)


# 1. A run-level gate must RAISE on failure -- not merely return, print, or record.
try:
    c.enforce_run_gate("G1", False, "deliberately failed")
    fails.append("enforce_run_gate did NOT raise on a failing gate (the original defect)")
except c.GateFailure:
    pass

# ...and must not raise on success.
try:
    c.enforce_run_gate("G1", True, "fine")
except c.GateFailure:
    fails.append("enforce_run_gate raised on a PASSING gate")

# 2. A per-arm gate failure must BAR that arm and keep every valid one.
arms = {"eps": {"gates_passed": True}, "T": {"gates_passed": True},
        "X": {"gates_passed": True}, "Z": {"gates_passed": False}}
ok = c.usable_arms(arms)
check("Z" not in ok, "usable_arms did NOT bar the gate-failed arm (the ring defect)")
check(set(ok) == {"eps", "T", "X"}, "usable_arms dropped a valid arm")

# 3. The pre-registered thresholds must be exactly as registered. Any drift here silently
#    invalidates the pre-registration the drivers claim to honour.
want = {"A_sigma": 3.0, "A_gap": 0.5, "B_sigma": 1.0, "B_gap": 0.3, "B_ratio": 2.0,
        "plateau_min_slopes": 3}
check(c.THRESH == want, "THRESH drifted from the pre-registered values: %s != %s" % (c.THRESH, want))

# 4. classify() must reach every branch, and must NOT round toward A.
#    args = (alpha1, sigma1, alpha2, sigma2, plateau_n1, plateau_n2, amp1, amp2)
cases = [
    ((4.00, 0.05, 2.00, 0.05, 5, 5, 1, 1.0), "A_CHANNEL_SPECIFIC"),
    ((2.10, 0.20, 2.15, 0.20, 5, 5, 1, 1.2), "B_CHANNEL_BLIND"),
    ((2.00, 0.10, 3.00, 0.10, 0, 0, 1, 1.0), "C_NO_POWER_LAW"),
    ((2.68, 0.33, 2.34, 0.10, 0, 5, 1, 4.5), "D_INDETERMINATE"),
    # D = 2.83, just UNDER the A bar of 3 -> must fall through to D, never round up.
    ((4.00, 0.50, 2.00, 0.50, 5, 5, 1, 1.0), "D_INDETERMINATE"),
    # D = 4.04, just OVER the bar -> A. Proves the boundary is live, not stuck.
    ((4.00, 0.35, 2.00, 0.35, 5, 5, 1, 1.0), "A_CHANNEL_SPECIFIC"),
    # B requires all three conditions; a big amplitude ratio alone must block it.
    ((2.10, 0.20, 2.15, 0.20, 5, 5, 1, 9.0), "D_INDETERMINATE"),
    # C takes precedence: no plateau in either arm, even with a huge separation.
    ((6.00, 0.05, 1.00, 0.05, 0, 0, 1, 1.0), "C_NO_POWER_LAW"),
]
for args, want_v in cases:
    got = c.classify(*args)[0]
    check(got == want_v, "classify%s -> %s, expected %s" % (args[:4], got, want_v))

# 5. The banned estimator must be unreachable from the verdict path.
check("linear_unweighted" not in inspect.getsource(c.classify),
      "BANNED unweighted-linear estimator is referenced inside classify()")

# 6. Both pre-registered estimators must exist (the ring driver was missing the cross-check).
for fn in ("fit_log_ols", "fit_relerr", "fit_linear_unweighted"):
    check(hasattr(c, fn), "missing estimator %s" % fn)


# 7. WIRING: the gate must sit on the code path BEFORE the verdict, and a GateFailure must
#    reach a non-zero exit. This is a static check on the drivers themselves -- unit-testing
#    enforce_run_gate proves the gate can raise, but not that anyone calls it in the right
#    place, which is exactly what the original code got wrong.
for drv, gate_marker, verdict_marker in (
        ("qw_channel_test.py", "enforce_run_gate(", "verdict, D, gap, ratio, why = classify("),
        ("qw_ring_test.py", "enforce_run_gate(", "usable_arms(")):
    src = io.open(os.path.join(HERE, drv), encoding="utf-8").read()
    check(gate_marker in src, "%s never calls enforce_run_gate" % drv)
    check(verdict_marker in src, "%s: verdict marker not found (test is stale)" % drv)
    if gate_marker in src and verdict_marker in src:
        check(src.index(gate_marker) < src.index(verdict_marker),
              "%s calls the gate AFTER the verdict path -- the gate cannot prevent a verdict" % drv)
    check("except GateFailure" in src, "%s does not catch GateFailure at entry" % drv)
    check("sys.exit(2)" in src, "%s does not exit non-zero on a void run" % drv)

# 8. BEHAVIOURAL: the discriminant selector must refuse a gate-failed arm.
#    This replaces an earlier substring check for "verdict_withheld" in the driver, which
#    mutation testing showed could not fail -- flipping the flag True->False left it green.
_arms = {"eps": {"gates_passed": True}, "T": {"gates_passed": True},
         "X": {"gates_passed": True}, "Z": {"gates_passed": False}}
ok_, barred_, reason_ = c.select_discriminant(_arms, "T", "Z")
check(ok_ is False, "select_discriminant permitted a discriminant using a gate-failed arm")
check(barred_ == ["Z"], "select_discriminant did not name the barred arm: %s" % barred_)
check(bool(reason_), "select_discriminant gave no reason for withholding")
ok2_, barred2_, _ = c.select_discriminant(_arms, "T", "X")
check(ok2_ is True, "select_discriminant refused two VALID arms")
check(barred2_ == [], "select_discriminant barred a valid arm")
# both arms bad -> both named
ok3_, barred3_, _ = c.select_discriminant(
    {"T": {"gates_passed": False}, "Z": {"gates_passed": False}}, "T", "Z")
check(ok3_ is False and set(barred3_) == {"T", "Z"},
      "select_discriminant mishandled two failing arms: %s" % barred3_)

# 9. The ring driver must route through the selector, not hard-wire an arm.
ring = io.open(os.path.join(HERE, "qw_ring_test.py"), encoding="utf-8").read()
check("select_discriminant(" in ring, "ring driver does not call select_discriminant")
check('crit["arms"]["Z"]' not in ring,
      "ring driver still hard-wires the Z arm into the discriminant")

# 10. The bootstrap sigma must carry its interpretation in the RETURNED OBJECT, not only in
#     a docstring. A reader consuming .bootstrap.std would otherwise take a
#     departure-from-power-law measure for a statistical error bar.
import numpy as _np
_bs = c.bootstrap(_np.array([3., 4., 5., 6., 7., 8.]),
                  _np.array([-1e-1, -5e-2, -3e-2, -2e-2, -1.4e-2, -1e-2]), n=50)
check("sigma_interpretation" in _bs, "bootstrap() does not return sigma_interpretation")
check("not statistical uncertainty" in _bs.get("sigma_interpretation", ""),
      "bootstrap sigma_interpretation does not say what the sigma is NOT")
_bs0 = c.bootstrap(_np.array([1., 2.]), _np.array([-1., -1.]), n=5)
check("sigma_interpretation" in _bs0,
      "bootstrap() drops the interpretation on the empty-resample path")

# 11. Unknown arm names must RAISE, not fall through to UnboundLocalError.
import importlib.util as _u
_rspec = _u.spec_from_file_location("qw_ring_test", os.path.join(HERE, "qw_ring_test.py"))
_ring = _u.module_from_spec(_rspec)
try:
    _rspec.loader.exec_module(_ring)
    try:
        _ring.force_profile(4, _np.ones(16) / 4.0, 0.0, None, "NOT_AN_ARM", 0, [1])
        fails.append("ring force_profile accepted an unknown arm name")
    except ValueError:
        pass
    except UnboundLocalError:
        fails.append("ring force_profile raised UnboundLocalError -- the else-branch is missing")
    except Exception as e:
        fails.append("ring force_profile raised %s, expected ValueError" % type(e).__name__)
except Exception as e:
    fails.append("could not import qw_ring_test for the arm-dispatch test: %s" % e)

# 12. BEHAVIOURAL: dropped separations must actually appear in the returned record.
#     An earlier version of this check counted `continue` against `dropped[` occurrences in the
#     source; mutation testing showed it could not fail, because commenting the line out left the
#     substring present inside the comment. String-counting is not a test.
_cspec = _u.spec_from_file_location("qw_channel_test", os.path.join(HERE, "qw_channel_test.py"))
_chain = _u.module_from_spec(_cspec)
try:
    _cspec.loader.exec_module(_chain)
    _n = 6
    _H, _ = _chain.build_tfim(_n)
    _gs = _np.ones(1 << _n) / _np.sqrt(1 << _n)
    # anchor=1 with dr up to 6 forces separations whose support runs past the chain end.
    _F, _dg = _chain.force_profile(_n, _gs, 0.0, _H, "eps", 1, list(range(1, 7)))
    _drop = _dg.get("dropped_separations", {})
    check(isinstance(_drop, dict) and len(_drop) > 0,
          "chain force_profile silently skipped out-of-range separations (nothing recorded)")
    check(_dg.get("n_dropped", 0) == len(_drop),
          "chain n_dropped disagrees with the recorded drops")
    check(all("reason" in v for v in _drop.values()),
          "chain recorded a dropped separation with no reason")
    check(set(_drop).isdisjoint(set(_F)),
          "a separation is both recorded as dropped and present in F")
except Exception as e:
    fails.append("chain drop-recording test could not run: %s: %s" % (type(e).__name__, e))

# ring: same, behaviourally -- an unnormalizable dual excitation must be recorded
_rF, _rdrop = _ring.force_profile(4, _np.zeros(16), 0.0, None, "eps", 0, [1])
check(isinstance(_rdrop, dict) and 1 in _rdrop,
      "ring force_profile silently skipped a zero-norm separation")
check(_rdrop.get(1, {}).get("reason", "") != "",
      "ring recorded a dropped separation with no reason")

print("NEGATIVE-TEST RESULTS (%d checks)" % (len(cases) + 36))
for f in fails:
    print("  FAIL:", f)
print("  all gate/verdict tests passed" if not fails else "  %d FAILURES" % len(fails))
sys.exit(1 if fails else 0)
