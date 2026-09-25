"""
Validator pulse schedule — drive field + hologron shift for 15-atom AHS validator.
Same 5-stage protocol as HYP-2026-017 production: state prep + 3 layers + hold = 2.80 us.
"""
import numpy as np
from braket.ahs import DrivingField, ShiftingField, Field, Pattern
from braket.timings.time_series import TimeSeries

N_ATOMS = 15
N_BOUNDARY = 8

# Pulse timings (us)
T_RAMP, T_PREP = 0.05, 0.30
T_LAYER3, T_LAYER2, T_LAYER1, T_HOLD = 0.80, 0.80, 0.70, 0.20
T_TOTAL = T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 + T_HOLD  # 2.80 us

# Rabi & detuning (rad/us, then * 1e6 for rad/s in Braket)
OMEGA_MAX_RAD_US = 2 * np.pi * 1.0      # Omega/(2pi) = 1 MHz
DELTA_START = -2 * np.pi * 5.0
DELTA_END   = +2 * np.pi * 5.0
HOLOGRON_DELTA_MHZ = 2.0


def build_validator_drive():
    times = [
        0.0, T_RAMP, T_PREP,
        T_PREP + T_LAYER3 / 2, T_PREP + T_LAYER3,
        T_PREP + T_LAYER3 + T_LAYER2 / 2, T_PREP + T_LAYER3 + T_LAYER2,
        T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 / 2,
        T_TOTAL - T_RAMP, T_TOTAL,
    ]
    times_s = [t * 1e-6 for t in times]
    omega_vals = [0.0] + [OMEGA_MAX_RAD_US * 1e6] * 8 + [0.0]
    phi_vals = [0.0] * 10
    delta_vals = [
        DELTA_START * 1e6, DELTA_START * 1e6, DELTA_START * 1e6,
        0.0, DELTA_END * 1e6, 0.0, DELTA_END * 1e6, 0.0,
        DELTA_END * 1e6, DELTA_END * 1e6,
    ]
    omega_ts, phi_ts, delta_ts = TimeSeries(), TimeSeries(), TimeSeries()
    for t, o, p, d in zip(times_s, omega_vals, phi_vals, delta_vals):
        omega_ts.put(t, o); phi_ts.put(t, p); delta_ts.put(t, d)
    return DrivingField(
        amplitude=Field(time_series=omega_ts, pattern=Pattern([1.0] * N_ATOMS)),
        phase=Field(time_series=phi_ts, pattern=Pattern([0.0] * N_ATOMS)),
        detuning=Field(time_series=delta_ts, pattern=Pattern([1.0] * N_ATOMS)),
    )


def _drive_times_us():
    """Return the drive's time grid in microseconds (must match build_validator_drive)."""
    return [
        0.0, T_RAMP, T_PREP,
        T_PREP + T_LAYER3 / 2, T_PREP + T_LAYER3,
        T_PREP + T_LAYER3 + T_LAYER2 / 2, T_PREP + T_LAYER3 + T_LAYER2,
        T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 / 2,
        T_TOTAL - T_RAMP, T_TOTAL,
    ]


def _shift_envelope(t_us):
    """Hologron envelope: 0 at t=0, ramps to 1 by T_RAMP, holds 1 until T_PREP,
    ramps to 0 by T_PREP+T_RAMP, then 0 for the rest of the schedule."""
    if t_us <= 0.0:
        return 0.0
    if t_us < T_RAMP:
        return t_us / T_RAMP
    if t_us <= T_PREP:
        return 1.0
    if t_us < T_PREP + T_RAMP:
        return 1.0 - (t_us - T_PREP) / T_RAMP
    return 0.0


def build_validator_shift(excited_sites):
    # AWS AHS pattern values must be in [0, 1] -- they are dimensionless
    # per-atom weights. The actual rad/s magnitude lives in the TimeSeries.
    pattern_vals = [0.0] * N_ATOMS
    for s in excited_sites:
        if 0 <= s < N_BOUNDARY:
            pattern_vals[s] = 1.0
    # AWS AHS also requires every TimeSeries (drive amplitude/phase/detuning
    # AND ShiftingField magnitude) to share the SAME time grid. Carry the
    # full rad/s scale * envelope at every drive timepoint.
    delta_rad_s = HOLOGRON_DELTA_MHZ * 2 * np.pi * 1e6
    shift_ts = TimeSeries()
    for t_us in _drive_times_us():
        shift_ts.put(t_us * 1e-6, delta_rad_s * _shift_envelope(t_us))
    return ShiftingField(magnitude=Field(time_series=shift_ts, pattern=Pattern(pattern_vals)))


if __name__ == "__main__":
    d = build_validator_drive()
    s = build_validator_shift([2])
    print(f"validator_pulses: drive built (T_total={T_TOTAL:.2f} us), shift built for site 2")
