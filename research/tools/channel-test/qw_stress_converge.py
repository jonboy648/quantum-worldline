#!/usr/bin/env python3
"""
qw_stress_converge.py -- apply PREREGISTRATION-T.md's convergence rule and outcome table to the
three single-size result files (stress_test_n{16,20,24}_results.json). This is the ONLY place a
verdict for SIM-2026-075 is computed. It never runs physics.

Convergence (per arm): |a(24) - a(20)| < 0.1 AND sign(a(24) - a(20)) == sign(a(20) - a(16)).
Outcomes: N (null confirmed) / DEV (deviation) / C (no power law) / D (indeterminate) / VOID.
Precedence: VOID > C > N/DEV > D.  An arm that failed any per-arm gate at n=24 is barred.
"""
import json, os, sys
import numpy as np

HERE = os.path.dirname(os.path.abspath(__file__))
SIZES = (16, 20, 24)
NULL = {"H": 4.0, "E": 2.0}
DEV_SIGMA, DEV_GAP, CONV_STEP = 3.0, 0.5, 0.1


def load(n):
    return json.load(open(os.path.join(HERE, f"stress_test_n{n}_results.json")))


def main():
    R = {n: load(n) for n in SIZES}
    report = {"preregistration": "PREREGISTRATION-T.md @ 82b7b4e", "sizes": list(SIZES), "arms": {}}
    if any(R[n]["control"]["verdict"] != "CONTROL_CLEAN" for n in SIZES):
        report["VERDICT"] = "VOID"; report["reason"] = "a matched control was CONTROL_CONTAMINATED"
        print(json.dumps(report, indent=1)); return report
    outcomes = {}
    for a in ("H", "E"):
        arm24 = R[24]["critical"]["arms"][a]
        al = {n: R[n]["critical"]["arms"][a]["alpha_chord"] for n in SIZES}
        s1, s2 = al[20] - al[16], al[24] - al[20]
        converged = bool(abs(s2) < CONV_STEP and np.sign(s2) == np.sign(s1) and np.isfinite(s1 + s2))
        sig = max(arm24["bootstrap_sigma"] if np.isfinite(arm24["bootstrap_sigma"]) else np.inf, abs(s2))
        dist = abs(al[24] - NULL[a])
        gates = {"G2": arm24["G2_pass"], "G4": arm24["G4_pass"], "G5": arm24.get("G5_pass")}
        barred = not arm24["gates_passed"]
        plateau_ok = arm24["plateau_n"] >= 3
        if barred:
            o = "VOID_ARM"
        elif not plateau_ok:
            o = "C"
        elif not converged:
            o = "D"
        elif dist <= max(DEV_SIGMA * sig, DEV_GAP):
            o = "N"
        else:
            o = "DEV"
        outcomes[a] = o
        report["arms"][a] = {"alpha_by_n": al, "step_16_20": s1, "step_20_24": s2, "converged": converged,
                             "sigma_used": sig, "distance_from_null": dist, "null": NULL[a],
                             "gates_at_n24": gates, "barred": barred, "plateau_n_at_24": arm24["plateau_n"],
                             "two_point_exponent_at_24": arm24["G4_two_point_exponent_chord"],
                             "outcome": o}
    both_void = all(o == "VOID_ARM" for o in outcomes.values())
    if both_void:
        v = "VOID"
    elif "C" in outcomes.values() and not any(o in ("N", "DEV") for o in outcomes.values()):
        v = "C_NO_POWER_LAW"
    elif "DEV" in outcomes.values():
        v = "DEV_DEVIATION"
    elif all(o == "N" for o in outcomes.values()):
        v = "N_NULL_CONFIRMED"
    elif "N" in outcomes.values():
        v = "D_INDETERMINATE (one arm null, the other unusable)"
    else:
        v = "D_INDETERMINATE"
    report["VERDICT"] = v
    report["reading"] = ("The verdict is computed from pre-registered rules only. Outcome N is a Level 1 "
                         "validation, not a discovery. Only DEV is a finding.")
    json.dump(report, open(os.path.join(HERE, "stress_test_convergence.json"), "w"), indent=1, default=float)
    print(json.dumps(report, indent=1, default=float))
    return report


if __name__ == "__main__":
    main()
