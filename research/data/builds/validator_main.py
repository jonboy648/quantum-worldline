"""
HYP-2026-017+020 validator runner -- 15-atom local AHS smoke test.

Glues Parts 1-3 (layout, pulses, force) into a 10-task LocalSimulator("braket_ahs")
sweep that produces a force profile F(dr) for dr=1..4 plus a Renyi-2 TEE estimate,
then writes a PASS/FAIL verdict to HYP-2026-017-validator-results.json.

Validator gate (PASS criteria):
  - All 10 tasks complete on LocalSimulator("braket_ahs"), peak RAM < 4 GB
  - Finite F(dr) for dr=1..4
  - Power-law fit alpha in [2, 6]  (acceptance window for the SMALL 15-atom system;
    physics window [3.2, 4.8] is for the real 256-atom Aquila run, not this validator)
  - TEE finite (no exceptions)

Caveat: validator PASS does NOT prove alpha=4. 15 atoms is too small for a clean
force; this gate only confirms the build is wired correctly end-to-end.

Usage:
  python validator_main.py
"""
import json
import os
import sys
import time
import traceback
from pathlib import Path

import numpy as np

from braket.ahs import AnalogHamiltonianSimulation, Hamiltonian
from braket.devices import LocalSimulator

from validator_layout import build_validator_layout, N_TOTAL, N_BOUNDARY
from validator_pulses import build_validator_drive, build_validator_shift, T_TOTAL
from validator_force import (
    bitstrings_to_density,
    density_to_energy_proxy,
    force_dr,
    renyi2_collision,
)


# --- Run configuration ---------------------------------------------------
ANCHOR = 1                       # boundary site index for the "j" excitation
DR_LIST = [1, 2, 3, 4]           # force-profile separations
N_SHOTS = 50                     # per task; 10 tasks * 50 = 500 shots total
TEE_REGION = [0, 1, 2, 3]        # 4-site Renyi-2 region on the boundary
DEVICE_NAME = "braket_ahs"       # NOT the default LocalSimulator()

# --- Acceptance window (validator-scale, not physics-scale) --------------
ACCEPTANCE_ALPHA_MIN = 2.0
ACCEPTANCE_ALPHA_MAX = 6.0

# --- RAM gate ------------------------------------------------------------
RAM_GATE_GB = 4.0

# --- Paths ---------------------------------------------------------------
OUTPUT_PATH = Path(__file__).parent / "HYP-2026-017-validator-results.json"


# --- Helpers -------------------------------------------------------------
def _rss_gb():
    """Best-effort RSS in GB. Returns None if psutil is unavailable."""
    try:
        import psutil
        return psutil.Process(os.getpid()).memory_info().rss / (1024 ** 3)
    except Exception:
        return None


def _build_program(excited_sites):
    """Build an AHS program for a given list of boundary sites to detune."""
    register = build_validator_layout()
    drive = build_validator_drive()
    shift = build_validator_shift(excited_sites)
    hamiltonian = Hamiltonian([drive, shift]) if excited_sites else Hamiltonian([drive])
    return AnalogHamiltonianSimulation(register=register, hamiltonian=hamiltonian)


def _run_task(device, label, excited_sites, n_shots):
    """Run one AHS task and return (energy_proxy, raw_measurements, valid_shots, elapsed_s)."""
    program = _build_program(excited_sites)
    t0 = time.time()
    result = device.run(program, shots=n_shots).result()
    elapsed = time.time() - t0
    density, valid = bitstrings_to_density(result)
    energy = density_to_energy_proxy(density, n_boundary=N_BOUNDARY)
    return energy, result.measurements, valid, elapsed


def main():
    started_at = time.time()
    rss_start = _rss_gb()
    rss_peak = rss_start if rss_start is not None else 0.0

    device = LocalSimulator(DEVICE_NAME)

    tasks = []  # log every task's outcome for the JSON dump
    energies = {}  # label -> energy proxy
    e0_measurements = None  # reused for TEE

    # Build the 10-task list:
    #   1) baseline E0  (no excitation)
    #   2) E_j          (anchor only)
    #   3..6) E_k(dr)   for dr in DR_LIST
    #   7..10) E_dual(dr) for dr in DR_LIST
    task_specs = [("E0", [])]
    task_specs.append((f"E_j(anchor={ANCHOR})", [ANCHOR]))
    for dr in DR_LIST:
        k = ANCHOR + dr
        task_specs.append((f"E_k(dr={dr})", [k]))
    for dr in DR_LIST:
        k = ANCHOR + dr
        task_specs.append((f"E_dual(dr={dr})", [ANCHOR, k]))

    failure_reason = None

    for label, excited in task_specs:
        try:
            energy, measurements, valid, elapsed = _run_task(
                device, label, excited, N_SHOTS
            )
        except Exception as exc:
            tasks.append({
                "label": label,
                "excited_sites": excited,
                "status": "ERROR",
                "error": f"{type(exc).__name__}: {exc}",
                "traceback": traceback.format_exc(),
            })
            failure_reason = f"task '{label}' raised {type(exc).__name__}"
            break

        rss_now = _rss_gb()
        if rss_now is not None and rss_now > rss_peak:
            rss_peak = rss_now

        tasks.append({
            "label": label,
            "excited_sites": excited,
            "status": "OK",
            "energy_proxy": energy,
            "valid_shots": valid,
            "elapsed_s": round(elapsed, 4),
            "rss_gb_after": rss_now,
        })
        energies[label] = energy
        if label == "E0":
            e0_measurements = measurements

        if rss_now is not None and rss_now > RAM_GATE_GB:
            failure_reason = f"RAM gate exceeded: {rss_now:.2f} GB > {RAM_GATE_GB} GB"
            break

    # --- Force profile ---------------------------------------------------
    forces = {}
    if failure_reason is None:
        e0 = energies["E0"]
        ej = energies[f"E_j(anchor={ANCHOR})"]
        for dr in DR_LIST:
            ek = energies[f"E_k(dr={dr})"]
            ed = energies[f"E_dual(dr={dr})"]
            forces[dr] = force_dr(ed, e0, ej, ek)

    # --- Power-law fit ---------------------------------------------------
    alpha = float("nan")
    fit_used = []
    if forces:
        xs, ys = [], []
        for dr, f in forces.items():
            if np.isfinite(f) and f > 0:
                xs.append(np.log(dr))
                ys.append(np.log(f))
                fit_used.append(dr)
        if len(xs) >= 2:
            slope, _intercept = np.polyfit(xs, ys, 1)
            alpha = float(-slope)

    # --- TEE -------------------------------------------------------------
    tee = float("nan")
    if e0_measurements is not None:
        try:
            tee = renyi2_collision(e0_measurements, TEE_REGION)
        except Exception as exc:
            failure_reason = failure_reason or f"TEE crashed: {type(exc).__name__}: {exc}"

    # --- Verdict ---------------------------------------------------------
    if failure_reason is None:
        if any(not np.isfinite(forces.get(dr, float("nan"))) for dr in DR_LIST):
            failure_reason = "non-finite F(dr) for one or more dr"
        elif not np.isfinite(alpha):
            failure_reason = "alpha fit produced non-finite result"
        elif not (ACCEPTANCE_ALPHA_MIN <= alpha <= ACCEPTANCE_ALPHA_MAX):
            failure_reason = (
                f"alpha={alpha:.3f} outside validator window "
                f"[{ACCEPTANCE_ALPHA_MIN}, {ACCEPTANCE_ALPHA_MAX}]"
            )
        elif not np.isfinite(tee):
            failure_reason = "TEE non-finite"

    verdict = "PASS" if failure_reason is None else "FAIL"

    payload = {
        "schema": "qw.validator.v1",
        "hypothesis_id": "HYP-2026-017",
        "validator": "15-atom local AHS",
        "device": DEVICE_NAME,
        "verdict": verdict,
        "reason": failure_reason,
        "config": {
            "anchor": ANCHOR,
            "dr_list": DR_LIST,
            "n_shots_per_task": N_SHOTS,
            "tee_region": TEE_REGION,
            "n_atoms": N_TOTAL,
            "n_boundary": N_BOUNDARY,
            "t_total_us": T_TOTAL,
            "acceptance_alpha": [ACCEPTANCE_ALPHA_MIN, ACCEPTANCE_ALPHA_MAX],
            "ram_gate_gb": RAM_GATE_GB,
        },
        "energies": energies,
        "forces": {str(k): v for k, v in forces.items()},
        "alpha_fit": {
            "alpha": alpha,
            "dr_used": fit_used,
        },
        "tee_renyi2_nats": tee,
        "ram": {
            "rss_start_gb": rss_start,
            "rss_peak_gb": rss_peak,
        },
        "wall_time_s": round(time.time() - started_at, 2),
        "tasks": tasks,
    }

    OUTPUT_PATH.write_text(json.dumps(payload, indent=2))
    print(f"validator_main: verdict={verdict}")
    if failure_reason:
        print(f"validator_main: reason={failure_reason}")
    print(f"validator_main: alpha={alpha:.3f}  TEE={tee:.4f}  peak_rss={rss_peak:.2f} GB")
    print(f"validator_main: results -> {OUTPUT_PATH}")
    return 0 if verdict == "PASS" else 1


if __name__ == "__main__":
    sys.exit(main())
