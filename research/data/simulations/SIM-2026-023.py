"""
SIM-2026-023: Classical reference baseline for HYP-2026-017 / HYP-2026-020.

Bootstrap-resamples the chi=3 MERA force profile from SIM-2026-015d with
gaussian noise (sigma=1% per dr) to produce 1-sigma and 3-sigma envelopes.
Fits abs(F) vs dr with unweighted power law to reproduce reference alpha.
Saves SIM-2026-023.json alongside this script.

Usage: python SIM-2026-023.py
"""

import json
import pathlib
import numpy as np
from scipy.optimize import curve_fit

# --- Reference data from SIM-2026-015d (chi=3 MERA, 16q, anchor=2) ---
F_chi3_mera = {
    1: -2.2430861866566474,
    2: -0.521763129229857,
    3: -0.08776850712683881,
    4: -0.04441621590522615,
    5: -0.025002421093859084,
    6: -0.012942010281033589,
    7: -0.007251419939670711,
    8: -0.003244847883809854,
    9:  0.0012014968002738158,
    10: 0.00036517275546543715,
    11: -0.0007422103086014431,
}
ALPHA_REF   = 4.071157011661138
DALPHA_REF  = 0.17775000857927842
A_REF       = 8.751321149698686

# --- Bootstrap parameters ---
N_BOOT      = 1000
NOISE_SIGMA = 0.01   # 1% gaussian noise per dr
RNG_SEED    = 42
FIT_DRS     = [2, 3, 4, 5, 6]   # fit window matching SIM-2026-015d

OUTPUT_PATH = pathlib.Path(__file__).parent / "SIM-2026-023.json"


def power_law(dr, A, alpha):
    return A * dr ** (-alpha)


def run():
    rng = np.random.default_rng(RNG_SEED)

    # Bootstrap: add gaussian noise proportional to |F|
    boot_samples = {}
    for dr, F in F_chi3_mera.items():
        noise = rng.normal(0.0, abs(F) * NOISE_SIGMA, N_BOOT)
        boot_samples[dr] = F + noise

    # Compute per-dr statistics (dr=1..8 only; dr>=9 values cross zero)
    force_profile = {}
    for dr in range(1, 9):
        s = boot_samples[dr]
        mean   = float(np.mean(s))
        sigma1 = float(np.std(s))
        force_profile[str(dr)] = {
            "value":   round(mean,         6),
            "sigma_1": round(sigma1,        6),
            "sigma_3": round(3.0 * sigma1,  6),
        }

    # Unweighted power-law fit on abs(F) bootstrap means -- matches SIM-2026-015d
    fit_drs   = np.array(FIT_DRS, dtype=float)
    fit_F_abs = np.array([abs(float(np.mean(boot_samples[dr]))) for dr in FIT_DRS])

    popt, pcov = curve_fit(power_law, fit_drs, fit_F_abs, p0=[A_REF, ALPHA_REF])
    perr = np.sqrt(np.diag(pcov))
    A_fit, alpha_fit   = popt
    _dA,   dalpha_fit  = perr

    # R-squared
    F_pred = power_law(fit_drs, A_fit, alpha_fit)
    ss_res = float(np.sum((fit_F_abs - F_pred) ** 2))
    ss_tot = float(np.sum((fit_F_abs - np.mean(fit_F_abs)) ** 2))
    r_squared = 1.0 - ss_res / ss_tot

    print(f"alpha = {alpha_fit:.3f} +/- {dalpha_fit:.3f}, r2 = {r_squared:.3f}")

    # Sanity check against reference
    if not (ALPHA_REF - 3 * DALPHA_REF < alpha_fit < ALPHA_REF + 3 * DALPHA_REF):
        print(f"WARNING: fitted alpha {alpha_fit:.3f} outside 3-sigma of reference {ALPHA_REF:.3f}")

    result = {
        "id": "SIM-2026-023",
        "type": "classical",
        "purpose": (
            "Classical reference baseline for HYP-2026-017 (Aquila Rydberg force law)"
            " and HYP-2026-020 (TEE)"
        ),
        "method": (
            "Bootstrap-resampled chi=3 MERA force profile from SIM-2026-015d"
            " (1000 resamples, gaussian noise sigma=1%)"
        ),
        "n_qubits": 16,
        "chi": 3,
        "force_profile": force_profile,
        "alpha_fit": {
            "value":      round(float(alpha_fit),   3),
            "sigma":      round(float(dalpha_fit),  3),
            "fit_window": FIT_DRS[:1] + FIT_DRS[-1:],
            "r_squared":  round(r_squared,          4),
        },
        "tee_reference": {
            "value":     0.0,
            "sigma":     0.05,
            "rationale": (
                "Critical Ising CFT has no topological order;"
                " expect S_topo ~= 0"
            ),
        },
        "emulator_acceptance_window": {
            "alpha_min": 3.2,
            "alpha_max": 4.8,
            "rationale": "Within 20% of 4.0 per HYP-017 publication threshold",
        },
        "submit_to_hardware": "PENDING_EMULATOR_VALIDATION",
        "created_date": "2026-05-01",
        "created_by":   "classical-simulator",
    }

    with open(OUTPUT_PATH, "w") as fh:
        json.dump(result, fh, indent=2)

    print(f"Saved: {OUTPUT_PATH}")
    return result


if __name__ == "__main__":
    run()
