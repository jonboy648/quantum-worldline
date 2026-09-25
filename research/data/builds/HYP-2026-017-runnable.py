"""
HYP-2026-017 + HYP-2026-020: Holographic Force & TEE on QuEra Aquila
=====================================================================
Joint AWS Braket submission for two holographic signatures:

  HYP-017: Force exponent alpha ~ 4 (stress-tensor exchange)
           F(dr) = E_dual - E_0 - 2*(E_single - E_0) ~ A * dr^{-4}
           Expected: alpha = 4.0 +/- 0.3-0.5 (Aquila noise budget)
           Reference: alpha = 4.07 +/- 0.18 (chi=3 MERA, SIM-2026-015d)

  HYP-020: Topological Entanglement Entropy S_topo
           S_topo = S_AB + S_BC - S_B - S_ABC  (Kitaev-Preskill)
           Expected: S_topo ~ 0 (critical Ising CFT has NO topological order;
                                a measured |S_topo| < 0.2 confirms criticality)

Platform:  QuEra Aquila (ANALOG Rydberg tweezer, NOT gate-based)
SDK:       Amazon Braket Python SDK (amazon-braket-sdk)
Cost:      ~$85 (HYP-017: 8000 shots) + ~$30 (HYP-020: 3000 shots) = ~$115
T2* headroom: 4.0 us available, protocol uses ~2.8 us

IMPORTANT: DO NOT EXECUTE against real Aquila without explicit user approval.
           Test locally with the built-in Braket local simulator first.

Setup:
  pip install amazon-braket-sdk bloqade numpy scipy matplotlib

Author: computation-lead
Date:   2026-04-26
"""

import json
import time
import numpy as np
from scipy.optimize import curve_fit
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

# ── AWS Braket imports ─────────────────────────────────────────────────────────
from braket.aws import AwsDevice
from braket.ahs import (
    AtomArrangement,
    AnalogHamiltonianSimulation,
    DrivingField,
    Hamiltonian,
    ShiftingField,
    Field,
    Pattern,
)
from braket.timings.time_series import TimeSeries

# ── Configuration ──────────────────────────────────────────────────────────────
# Set USE_LOCAL=True for free local simulation (no AWS charges).
# Set USE_LOCAL=False ONLY with explicit user approval for real Aquila submission.
USE_LOCAL = True

# Aquila device ARN
AQUILA_ARN = "arn:aws:braket:us-east-1::device/qpu/quera/Aquila"

# 16 boundary atoms + 7 coarse-grain atoms (3-layer binary MERA tree)
N_BOUNDARY = 16
N_ATOMS = 24  # 8 + 4 + 2 + 1 boundary layers + 9 ancilla/coarse

# Rydberg physics (87Rb, |70S1/2> state)
# Blockade radius: Rb = (C6 / Omega_max)^(1/6)
# C6 = 862 GHz*um^6, Omega_max/(2*pi) = 1 MHz => Rb ~ 9.76 um
C6_GHz_UM6 = 862.0          # van der Waals coefficient
OMEGA_MAX_MHZ = 1.0          # Rabi frequency / (2*pi), MHz
OMEGA_MAX_RAD_US = 2 * np.pi * OMEGA_MAX_MHZ  # rad/us
BLOCKADE_RADIUS_UM = (C6_GHz_UM6 / OMEGA_MAX_MHZ) ** (1.0 / 6.0)  # ~9.76 um

# Atom spacing: boundary layer at 5 um so adjacent pairs are within blockade radius
BOUNDARY_SPACING_UM = 5.0    # boundary qubit spacing (< Rb -> blockade active)
LAYER_OFFSET_Y_UM = 10.0     # vertical offset between MERA layers

# Pulse timings (us) — total ~2.8 us, T2* headroom ~1.2 us
T_PREP        = 0.30         # state preparation
T_LAYER3      = 0.80         # UV boundary layer isometry
T_LAYER2      = 0.80         # mid layer isometry
T_LAYER1      = 0.70         # IR coarse-graining
T_HOLD        = 0.20         # coherent hold
T_TOTAL       = T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 + T_HOLD  # 2.80 us

# Rabi ramp parameters
T_RAMP        = 0.05         # rise/fall time for pulses (us)

# Detuning parameters (MHz * 2*pi => rad/us)
DELTA_START   = -2 * np.pi * 5.0   # initial detuning (rad/us), negative = red-detuned
DELTA_END     = +2 * np.pi * 5.0   # final detuning (rad/us), positive = blue-detuned

# Local detuning for hologron injection (boundary-primary excitation)
# sigma_j = 0.635*(Rydberg pop at j) approximation via local detuning shift
HOLOGRON_DELTA_MHZ = 2.0     # local detuning for excitation sites (MHz)

# Shot counts (production)
SHOTS_GS      = 1000         # shots for ground state energy measurement
SHOTS_SINGLE  = 500          # shots per single-hologron configuration
SHOTS_DUAL    = 1000         # shots per dual-hologron configuration (dr=1..8)
SHOTS_TEE     = 500          # shots per TEE partition (6 partitions)

DR_VALUES     = list(range(1, 9))    # dr = 1..8
ANCHOR        = 2                     # anchor site index (0-based), site 3 in 1-indexed

# Smoke mode gate (R5 structural smoke). Set QW_SMOKE=1 to use cheap counts.
# Smoke goal: exercise every code path R1+R2+R3 touched, prove finite alpha + S_topo.
# NOT a physics gate -- precision will be poor, sigma_alpha large, S_topo noisy.
#
# Smoke layout: 8+4+2+1 = 15 atoms (Hilbert dim 2^15 = 32k vs prod 2^30 = 1G).
# Boundary pairs cover ANCHOR=2 + DR=[1,2,4] up to site 6 < N_BOUNDARY=8 -- safe.
import os as _os_for_smoke
QW_SMOKE = _os_for_smoke.environ.get("QW_SMOKE", "").strip() in ("1", "true", "True")
if QW_SMOKE:
    SHOTS_GS     = 200
    SHOTS_SINGLE = 100
    SHOTS_DUAL   = 200
    SHOTS_TEE    = 100
    DR_VALUES    = [1, 2, 4]
    N_BOUNDARY   = 8
    print("=" * 70)
    print("QW_SMOKE=1 -- running smoke configuration (NOT publication-grade)")
    print(f"  SHOTS_GS={SHOTS_GS} SHOTS_SINGLE={SHOTS_SINGLE} "
          f"SHOTS_DUAL={SHOTS_DUAL} SHOTS_TEE={SHOTS_TEE}")
    print(f"  DR_VALUES={DR_VALUES} N_BOUNDARY={N_BOUNDARY} (smoke layout 8+4+2+1=15 atoms)")
    print("=" * 70)

# Expected force profile from SIM-2026-015d (16q chi=3 MERA)
V_DATA_REF = {
    1: -2.243086, 2: -0.521763, 3: -0.087769, 4: -0.044416,
    5: -0.025002, 6: -0.012942, 7: -0.007251, 8: -0.003245,
}
ALPHA_REF  = 4.071   # chi=3 MERA reference
A_REF      = 8.751   # amplitude reference

# Output paths (override via QW_OUT_DIR env-var; default to Windows project tree)
import os as _os_for_outdir
OUT_DIR    = _os_for_outdir.environ.get("QW_OUT_DIR",
                                        "D:/quantum-worldline/research/data/builds")
RESULTS_PATH = f"{OUT_DIR}/HYP-2026-017-results.json"
FIGURE_PATH  = f"{OUT_DIR}/HYP-2026-017-force-profile.png"


# ═══════════════════════════════════════════════════════════════════════════════
# 1.  ATOM LAYOUT — 3-layer binary MERA on 16 boundary + 8 coarse qubits
# ═══════════════════════════════════════════════════════════════════════════════

def build_mera_atom_layout():
    """
    Return AtomArrangement for 3-layer binary MERA.

    Layer 3 (UV, y=0):    16 boundary qubits, 5 um spacing
    Layer 2 (mid, y=10):   8 bond qubits, 10 um spacing (centered over pairs)
    Layer 1 (IR, y=20):    4 coarse qubits, 20 um spacing
    Layer 0 (bulk, y=30):  2 bulk qubits

    Total: 30 atoms  (spec says 24; we use 30 to cover 3 full binary layers
    with proper blockade geometry — hardware supports up to 256)

    Blockade condition: atom pairs within Rb ~ 9.76 um are blockade-coupled.
    Boundary layer spacing = 5 um << Rb: adjacent boundary pairs ARE blockaded.
    Inter-layer spacing ~ 10 um = Rb: layer interface pairs are near-blockade.
    """
    register = AtomArrangement()

    # Smoke mode (QW_SMOKE=1): half-scale 8+4+2+1=15 atoms.
    # Production: 16+8+4+2=30 atoms. Gated to make local-sim tractable.
    if QW_SMOKE:
        n3, n2, n1, n0 = 8, 4, 2, 1
    else:
        n3, n2, n1, n0 = 16, 8, 4, 2

    # Layer 3: boundary atoms at y = 0
    for i in range(n3):
        x = i * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, 0.0])  # Braket expects meters

    # Layer 2: bond atoms, centered over adjacent boundary pairs, y = 10 um
    for i in range(n2):
        x = (2 * i + 0.5) * BOUNDARY_SPACING_UM  # centered between pairs
        register.add([x * 1e-6, LAYER_OFFSET_Y_UM * 1e-6])

    # Layer 1: coarse atoms, y = 20 um
    for i in range(n1):
        x = (4 * i + 1.5) * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, 2 * LAYER_OFFSET_Y_UM * 1e-6])

    # Layer 0: bulk atoms, y = 30 um
    for i in range(n0):
        x = (8 * i + 3.5) * BOUNDARY_SPACING_UM
        register.add([x * 1e-6, 3 * LAYER_OFFSET_Y_UM * 1e-6])

    return register


# ═══════════════════════════════════════════════════════════════════════════════
# 2.  GLOBAL DRIVE FIELD — three-phase pulse sequence
# ═══════════════════════════════════════════════════════════════════════════════

def build_drive_field():
    """
    Build the global DrivingField (Omega, phase, Delta) for MERA state prep.

    Protocol:
      0.0 - 0.05 us  : Rabi ramp up to Omega_max, Delta = Delta_start
      0.05 - 0.35 us : Hold (state prep / optical pumping simulation)
      0.35 - 1.15 us : Layer 3 entanglement: pi/2 pulse at Omega_max
      1.15 - 1.95 us : Layer 2 entanglement: pi pulse with Delta sweep
      1.95 - 2.65 us : Layer 1 coarse-graining: pi pulse
      2.65 - 2.80 us : Ramp down + hold

    Delta sweeps from red- to blue-detuned to create the adiabatic
    passage that implements the isometry (blockade-constrained entanglement).
    """
    n_atoms = 30  # matches build_mera_atom_layout()

    # Time grid
    times = [
        0.0,
        T_RAMP,                                          # 0.05
        T_PREP,                                          # 0.30
        T_PREP + T_LAYER3 / 2,                          # 0.70
        T_PREP + T_LAYER3,                              # 1.10
        T_PREP + T_LAYER3 + T_LAYER2 / 2,              # 1.50
        T_PREP + T_LAYER3 + T_LAYER2,                  # 1.90
        T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 / 2,  # 2.25
        T_TOTAL - T_RAMP,                               # 2.75
        T_TOTAL,                                         # 2.80
    ]
    times_s = [t * 1e-6 for t in times]  # convert to seconds

    # Rabi frequency Omega(t): ramp up, hold at Omega_max, ramp down
    omega_vals = [
        0.0,
        OMEGA_MAX_RAD_US * 1e6,   # ramp up (rad/s for Braket)
        OMEGA_MAX_RAD_US * 1e6,   # hold through prep
        OMEGA_MAX_RAD_US * 1e6,   # layer 3 start
        OMEGA_MAX_RAD_US * 1e6,   # layer 3 end
        OMEGA_MAX_RAD_US * 1e6,   # layer 2 start
        OMEGA_MAX_RAD_US * 1e6,   # layer 2 end
        OMEGA_MAX_RAD_US * 1e6,   # layer 1 start
        OMEGA_MAX_RAD_US * 1e6,   # before ramp down
        0.0,                       # ramp down
    ]

    # Phase phi(t): zero throughout (can be modulated for more complex unitaries)
    phi_vals = [0.0] * len(times_s)

    # Detuning Delta(t): sweep from negative to positive for adiabatic passage
    delta_mid = 0.0
    delta_vals = [
        DELTA_START * 1e6,    # red-detuned start (rad/s)
        DELTA_START * 1e6,
        DELTA_START * 1e6,
        delta_mid * 1e6,      # sweep through zero during layer 3
        DELTA_END * 1e6,
        delta_mid * 1e6,      # sweep during layer 2
        DELTA_END * 1e6,
        delta_mid * 1e6,
        DELTA_END * 1e6,
        DELTA_END * 1e6,
    ]

    omega_ts = TimeSeries()
    phi_ts = TimeSeries()
    delta_ts = TimeSeries()
    for t, o, p, d in zip(times_s, omega_vals, phi_vals, delta_vals):
        omega_ts.put(t, o)
        phi_ts.put(t, p)
        delta_ts.put(t, d)

    drive = DrivingField(
        amplitude=Field(time_series=omega_ts, pattern=Pattern([1.0] * n_atoms)),
        phase=Field(time_series=phi_ts, pattern=Pattern([0.0] * n_atoms)),
        detuning=Field(time_series=delta_ts, pattern=Pattern([1.0] * n_atoms)),
    )
    return drive


# ═══════════════════════════════════════════════════════════════════════════════
# 3.  BOUNDARY-PRIMARY INJECTION (Wang/He 2025: bond-pair sigma_j approx, R1 fix)
# ═══════════════════════════════════════════════════════════════════════════════

def _drive_time_grid_us():
    """The drive's 10-point time grid in microseconds. Must exactly match
    the times list in build_drive_field; AWS AHS rejects programs whose
    DrivingField and ShiftingField TimeSeries are on different grids."""
    return [
        0.0, T_RAMP, T_PREP,
        T_PREP + T_LAYER3 / 2, T_PREP + T_LAYER3,
        T_PREP + T_LAYER3 + T_LAYER2 / 2, T_PREP + T_LAYER3 + T_LAYER2,
        T_PREP + T_LAYER3 + T_LAYER2 + T_LAYER1 / 2,
        T_TOTAL - T_RAMP, T_TOTAL,
    ]


def _shift_envelope(t_us):
    """Hologron-prep envelope: 0 -> 1 over T_RAMP, hold to T_PREP, 1 -> 0 over T_RAMP."""
    if t_us <= 0.0:
        return 0.0
    if t_us < T_RAMP:
        return t_us / T_RAMP
    if t_us <= T_PREP:
        return 1.0
    if t_us < T_PREP + T_RAMP:
        return 1.0 - (t_us - T_PREP) / T_RAMP
    return 0.0


def build_shifting_field(excited_sites, n_atoms):
    """
    Build ShiftingField implementing a boundary-primary excitation
    approximating Wang/He 2025's sigma_j^boundary ~ 0.635*(X_j + X_{j+1}).

    Devil's-advocate R1 fix (2026-05-05): each `j` in excited_sites is
    interpreted as a *bond center*; the prep-time detuning bias is applied
    to BOTH atoms j and j+1 (clamped to the boundary layer). This shifts
    the protocol from "single-site hologron at j" (unstable, decays in
    1.5-80 ns) to "bond-centered boundary primary at (j, j+1)" (Wang/He
    showed ~88% stable at finite size).

    Caveat: this is a leading-order approximation. The full sigma primary
    requires a coherent X-rotation, not a detuning bias; that's a deeper
    architectural change deferred for a future iteration. The bond-pair
    bias captures the dominant structural correction without requiring
    a full pulse-protocol rewrite.

    excited_sites: list of 0-based boundary atom indices (each interpreted
                   as a bond center; partner atom j+1 added automatically).

    AWS AHS schema notes:
      - Pattern values must be dimensionless in [0, 1]
      - All TimeSeries must share the same time grid as the drive
      - Magnitude TimeSeries carries the rad/s scale; pattern weights it per-atom
    """
    pattern_vals = [0.0] * n_atoms
    boundary_pairs = set()
    for s in excited_sites:
        if 0 <= s < N_BOUNDARY:
            boundary_pairs.add(s)
            if s + 1 < N_BOUNDARY:
                boundary_pairs.add(s + 1)
    for s in boundary_pairs:
        pattern_vals[s] = 1.0  # dimensionless weight

    delta_rad_s = HOLOGRON_DELTA_MHZ * 2 * np.pi * 1e6  # rad/s scale
    shift_ts = TimeSeries()
    for t_us in _drive_time_grid_us():
        shift_ts.put(t_us * 1e-6, delta_rad_s * _shift_envelope(t_us))

    shift = ShiftingField(
        magnitude=Field(
            time_series=shift_ts,
            pattern=Pattern(pattern_vals),
        )
    )
    return shift


# ═══════════════════════════════════════════════════════════════════════════════
# 4.  AHS PROGRAM BUILDER
# ═══════════════════════════════════════════════════════════════════════════════

def build_ahs_program(excited_sites=None):
    """
    Build full AnalogHamiltonianSimulation program.

    excited_sites: None for ground state, list of ints for hologron injection.
    """
    register = build_mera_atom_layout()
    n_atoms_actual = len(list(register))
    drive = build_drive_field()

    # AHS uses Hamiltonian([term1, term2, ...]) -- not Python `+`. Earlier
    # code used `drive + shift` which raises TypeError at runtime.
    if excited_sites:
        shift = build_shifting_field(excited_sites, n_atoms=n_atoms_actual)
        hamiltonian = Hamiltonian([drive, shift])
    else:
        hamiltonian = Hamiltonian([drive])
    program = AnalogHamiltonianSimulation(register=register, hamiltonian=hamiltonian)
    return program


# ═══════════════════════════════════════════════════════════════════════════════
# 5.  ENERGY ESTIMATOR from bitstring measurements
# ═══════════════════════════════════════════════════════════════════════════════

def bitstrings_to_rydberg_density(result):
    """
    Extract per-site Rydberg excitation density <n_i> from measurement result.
    Returns array of shape (n_atoms,) with values in [0, 1].
    """
    measurements = result.measurements  # list of ShotResult
    n_atoms = len(measurements[0].pre_sequence)
    n_shots = len(measurements)

    density = np.zeros(n_atoms)
    valid_shots = 0
    for shot in measurements:
        if shot.status.name == "SUCCESS":
            # post_sequence: 0 = ground |g>, 1 = Rydberg |r>
            density += np.array(shot.post_sequence, dtype=float)
            valid_shots += 1

    if valid_shots > 0:
        density /= valid_shots
    return density, valid_shots


def rydberg_density_to_energy(density, n_boundary=16):
    """
    DEPRECATED 2026-05-05 (devil's-advocate R2). One-body density product
    drops connected two-body correlations, which are the holographic signal.
    Use bitstrings_to_connected_zz / energy_proxy_from_zz instead.

    Kept for reference / debugging only. Should not appear in F(dr) pipeline.
    """
    zi = 1.0 - 2.0 * density[:n_boundary]
    zz_sum = np.sum(zi[:-1] * zi[1:])  # <-- BUG: product of averages, not connected
    xi = 2.0 * np.sqrt(np.maximum(density[:n_boundary] * (1.0 - density[:n_boundary]), 1e-10))
    return float(-zz_sum - np.sum(xi))


def bitstrings_to_connected_zz(result, n_boundary=16):
    """
    Compute connected nearest-neighbor ZZ correlator <Z_i Z_{i+1}>_c
    from per-shot bitstrings.

      <Z_i Z_{i+1}>_c = <Z_i Z_{i+1}> - <Z_i><Z_{i+1}>

    where Z_i = 1 - 2 n_i (n_i is the per-site Rydberg occupation 0/1
    in each individual shot). The connected piece carries the two-body
    interaction structure that the boundary stress-tensor exchange
    contributes to the energy.

    Returns:
      zz_connected: ndarray (n_boundary - 1,) -- one entry per nearest-neighbor pair
      zi_means:     ndarray (n_boundary,)     -- single-site <Z_i> for diagnostics
      valid_shots:  int                       -- number of SUCCESS-status shots
    """
    measurements = result.measurements
    if not measurements:
        return np.zeros(n_boundary - 1), np.zeros(n_boundary), 0

    n_atoms = len(measurements[0].pre_sequence)
    valid_bitstrings = []
    for shot in measurements:
        if shot.status.name == "SUCCESS":
            # post_sequence: 0 = ground |g>, 1 = Rydberg |r>
            valid_bitstrings.append(np.array(shot.post_sequence, dtype=np.int8))
    if len(valid_bitstrings) == 0:
        return np.zeros(n_boundary - 1), np.zeros(n_boundary), 0

    bits = np.array(valid_bitstrings)        # shape (n_shots, n_atoms)
    z_per_shot = 1.0 - 2.0 * bits[:, :n_boundary].astype(np.float64)  # (n_shots, n_boundary)

    zi_means = z_per_shot.mean(axis=0)                                   # <Z_i>
    zz_per_shot = z_per_shot[:, :-1] * z_per_shot[:, 1:]                 # Z_i * Z_{i+1} per shot
    zz_full = zz_per_shot.mean(axis=0)                                   # <Z_i Z_{i+1}>
    zz_disconnected = zi_means[:-1] * zi_means[1:]                       # <Z_i><Z_{i+1}>
    zz_connected = zz_full - zz_disconnected                             # <Z_i Z_{i+1}>_c

    return zz_connected, zi_means, len(valid_bitstrings)


def energy_proxy_from_zz(zz_connected, zi_means):
    """
    Boundary energy proxy built from the connected ZZ correlator structure.
    For the boundary stress-tensor signal, what matters is the SUM of
    connected NN correlators across the chain -- this is the leading
    contribution to the energy interaction between two boundary excitations
    that the holographic mapping predicts.

      E_proxy_connected = - sum_i <Z_i Z_{i+1}>_c

    The transverse-field <X_i> piece from the prior estimator is dropped:
    the holographic force F(dr) = E_dual - E0 - (E_j - E0) - (E_k - E0)
    is sensitive only to the *interaction* (two-body) contribution, and
    one-body terms cancel in this difference by construction. Including a
    sqrt(p(1-p)) X-proxy added noise without signal.

    Returns scalar energy proxy.
    """
    return float(-np.sum(zz_connected))


# ═══════════════════════════════════════════════════════════════════════════════
# 6.  SHADOW TOMOGRAPHY for Renyi-2 entropy (HYP-020 TEE)
# ═══════════════════════════════════════════════════════════════════════════════

def renyi2_from_bitstrings(measurements, subsystem_sites):
    """
    Estimate Renyi-2 entropy S_2 of subsystem from computational-basis bitstrings.

    Uses the collision probability estimator (Brydges et al. 2019):
      Tr[rho_A^2] = (2/N_shots^2) * sum_{s!=t} (-2)^{-D(s_A, t_A)}
    where D(s, t) = Hamming distance.

    For binary (0/1) bitstrings, this simplifies via the purity estimator.

    Returns S_2 = -log2(Tr[rho_A^2]) in bits, converted to nats.
    """
    valid = []
    for shot in measurements:
        if shot.status.name == "SUCCESS":
            bits = np.array(shot.post_sequence, dtype=int)
            valid.append(bits[subsystem_sites])

    if len(valid) < 10:
        return float("nan"), float("nan")

    valid = np.array(valid)  # shape (n_valid, n_subsys)
    n_shots, n_sub = valid.shape

    # Purity estimator via collision probability
    # purity ~ sum_{s,t} (-1/2)^{D(s,t)} / (n_shots * (n_shots - 1) / 2)
    purity_sum = 0.0
    n_pairs = 0
    for i in range(n_shots):
        for j in range(i + 1, n_shots):
            hamming = np.sum(valid[i] != valid[j])
            purity_sum += (-0.5) ** hamming
            n_pairs += 1

    if n_pairs == 0:
        return float("nan"), float("nan")

    purity = max(purity_sum / n_pairs, 1e-10)
    s2_bits = -np.log2(purity)
    s2_nats = s2_bits * np.log(2)

    # Bootstrap error estimate
    n_boot = 50
    boot_s2 = []
    for _ in range(n_boot):
        idx = np.random.choice(n_shots, n_shots, replace=True)
        sample = valid[idx]
        ps = 0.0
        np2 = 0
        for i in range(n_shots):
            for j in range(i + 1, n_shots):
                h = np.sum(sample[i] != sample[j])
                ps += (-0.5) ** h
                np2 += 1
        if np2 > 0:
            p_b = max(ps / np2, 1e-10)
            boot_s2.append(-np.log2(p_b) * np.log(2))

    s2_err = float(np.std(boot_s2)) if boot_s2 else float("nan")
    return float(s2_nats), s2_err


def compute_tee(result_gs):
    """
    Compute Kitaev-Preskill TEE from ground state measurement result.

    S_topo = S_AB + S_BC - S_B - S_ABC

    Subsystem definitions scale with N_BOUNDARY: split boundary into roughly
    equal thirds A | B | C. For production N_BOUNDARY=16: A=5, B=5, C=6.
    For smoke N_BOUNDARY=8: A=2, B=3, C=3 (still 3 disjoint subsystems).
    """
    measurements = result_gs.measurements

    # Partition boundary into three contiguous subsystems.
    nb = N_BOUNDARY
    a_end = nb // 3
    b_end = 2 * nb // 3
    A = list(range(0, a_end))
    B = list(range(a_end, b_end))
    C = list(range(b_end, nb))
    AB = A + B
    BC = B + C
    ABC = A + B + C

    s_b,  e_b  = renyi2_from_bitstrings(measurements, B)
    s_ab, e_ab = renyi2_from_bitstrings(measurements, AB)
    s_bc, e_bc = renyi2_from_bitstrings(measurements, BC)
    s_abc, e_abc = renyi2_from_bitstrings(measurements, ABC)

    if any(np.isnan(x) for x in [s_b, s_ab, s_bc, s_abc]):
        return {"S_topo": float("nan"), "S_topo_err": float("nan"),
                "S_B": s_b, "S_AB": s_ab, "S_BC": s_bc, "S_ABC": s_abc}

    s_topo = s_ab + s_bc - s_b - s_abc
    s_topo_err = np.sqrt(e_ab**2 + e_bc**2 + e_b**2 + e_abc**2)

    # Z symmetry check: <Z>_avg ~ 1 - 2*<n>_avg (boundary only)
    density, _ = bitstrings_to_rydberg_density(result_gs)
    z_avg = float(np.mean(1.0 - 2.0 * density[:N_BOUNDARY]))

    return {
        "S_topo": float(s_topo),
        "S_topo_err": float(s_topo_err),
        # Critical Ising CFT has NO topological order (it's a critical / gapless
        # phase, not a Z2 topologically-ordered phase). Predicted S_topo = 0.
        # Earlier value -ln(2) was wrong; matches the toric code, not Ising.
        # See SIM-2026-023.json which correctly has S_topo_ref = 0 ± 0.05.
        "S_topo_predicted": 0.0,
        "S_B": float(s_b),
        "S_AB": float(s_ab),
        "S_BC": float(s_bc),
        "S_ABC": float(s_abc),
        "Z_avg": z_avg,
        "Z_ferromagnetic_check": "FAIL (ferromagnetic, TEE invalid)" if abs(z_avg) > 0.1 else "PASS",
    }


# ═══════════════════════════════════════════════════════════════════════════════
# 7.  FORCE PROFILE EXTRACTION
# ═══════════════════════════════════════════════════════════════════════════════

def power_law(dr, A, alpha):
    return A * np.array(dr, dtype=float) ** (-alpha)


def fit_force_profile(dr_values, F_values, F_errors, fit_dr_min=2):
    """Fit F(dr) = A * dr^{-alpha}, returning (alpha, dalpha, A, dA)."""
    dr = np.array(dr_values)
    F = np.array(F_values)
    sigma = np.array(F_errors)

    mask = (dr >= fit_dr_min) & np.isfinite(F) & (F < 0)
    if mask.sum() < 2:
        return {"alpha": float("nan"), "dalpha": float("nan"),
                "A": float("nan"), "dA": float("nan"),
                "n_points": int(mask.sum())}

    try:
        popt, pcov = curve_fit(
            lambda x, A, alpha: power_law(x, A, alpha),
            dr[mask], -F[mask],  # fit |F| as positive
            p0=[A_REF, ALPHA_REF],
            sigma=sigma[mask] if sigma[mask].sum() > 0 else None,
            absolute_sigma=True,
            maxfev=5000,
        )
        perr = np.sqrt(np.diag(pcov))
        return {
            "alpha": float(popt[1]),
            "dalpha": float(perr[1]),
            "A": float(popt[0]),
            "dA": float(perr[0]),
            "n_points": int(mask.sum()),
        }
    except Exception as e:
        return {"alpha": float("nan"), "dalpha": float("nan"),
                "A": float("nan"), "dA": float("nan"),
                "error": str(e), "n_points": int(mask.sum())}


# ═══════════════════════════════════════════════════════════════════════════════
# 8.  SHOT-NOISE PRECISION ESTIMATE (classical, no hardware needed)
# ═══════════════════════════════════════════════════════════════════════════════

def estimate_alpha_precision(n_shots_per_dr, dr_values, analog_error_pct=6.0):
    """
    Monte Carlo estimate of alpha measurement uncertainty under:
    - Shot noise: sigma_E ~ 1/sqrt(n_shots) * E_scale
    - Analog error: systematic shift sigma_systematic ~ analog_error_pct/100 * |F|

    Returns estimated sigma_alpha.
    """
    E_scale = 1.0   # dimensionless energy units
    n_trials = 1000
    alphas = []

    for _ in range(n_trials):
        F_noisy = {}
        for dr in dr_values:
            F_true = -A_REF * dr ** (-ALPHA_REF)
            # Shot noise contribution
            shot_noise = E_scale / np.sqrt(n_shots_per_dr)
            # Analog systematic noise (coherent error shifts energy)
            systematic = abs(F_true) * analog_error_pct / 100.0
            total_noise = np.sqrt(shot_noise**2 + systematic**2)
            F_noisy[dr] = F_true + np.random.normal(0, total_noise)

        dr_arr = np.array(dr_values[1:])  # exclude dr=1 (contact term)
        F_arr = np.array([F_noisy[d] for d in dr_values[1:]])

        mask = F_arr < 0
        if mask.sum() >= 2:
            try:
                popt, _ = curve_fit(
                    lambda x, A, a: A * x**(-a),
                    dr_arr[mask], -F_arr[mask],
                    p0=[A_REF, ALPHA_REF],
                    maxfev=2000,
                )
                alphas.append(popt[1])
            except Exception:
                pass

    if len(alphas) < 10:
        return float("nan")
    return float(np.std(alphas))


# ═══════════════════════════════════════════════════════════════════════════════
# 9.  TASK SUBMISSION
# ═══════════════════════════════════════════════════════════════════════════════

def get_device():
    """Return Aquila device or local simulator based on USE_LOCAL flag."""
    if USE_LOCAL:
        from braket.devices import LocalSimulator
        # "braket_ahs" is the analog Hamiltonian simulator;
        # "default" resolves to the gate-based state-vector sim and rejects AHS programs.
        return LocalSimulator("braket_ahs")
    else:
        return AwsDevice(AQUILA_ARN)


def submit_and_wait(program, shots, device, tag=""):
    """Submit AHS program and wait for result. Returns result object."""
    print(f"  Submitting {tag} ({shots} shots)...")
    task = device.run(program, shots=shots)
    print(f"  Task ID: {getattr(task, 'id', 'local')}")

    result = task.result()
    print(f"  Done. Measurements: {len(result.measurements)}")
    return result


# ═══════════════════════════════════════════════════════════════════════════════
# 10. MAIN EXECUTION
# ═══════════════════════════════════════════════════════════════════════════════

def main():
    t_start = time.time()
    print("=" * 70)
    print("HYP-2026-017/020: QuEra Aquila holographic force + TEE")
    print(f"Mode: {'LOCAL SIMULATOR (free)' if USE_LOCAL else 'REAL AQUILA ($$$)'}")
    print(f"T2* headroom: {4.0 - T_TOTAL:.2f} us  (protocol: {T_TOTAL:.2f} us)")
    print("=" * 70)

    # ── Shot-noise precision estimate (classical, always runs) ─────────────────
    print("\n[0] Shot-noise alpha precision estimate...")
    sigma_alpha = estimate_alpha_precision(
        n_shots_per_dr=SHOTS_DUAL,
        dr_values=DR_VALUES,
        analog_error_pct=6.0,
    )
    print(f"    Expected sigma_alpha ~ {sigma_alpha:.3f}  "
          f"(target: 0.3-0.5 per HYP-017 spec)")

    device = get_device()

    # ── Step 1: Ground state measurement ─────────────────────────────────────
    print("\n[1] Ground state energy measurement...")
    prog_gs = build_ahs_program(excited_sites=None)
    result_gs = submit_and_wait(prog_gs, SHOTS_GS, device, "ground state")
    # R2 fix: use connected ZZ correlator, not product-of-single-site densities
    zz_gs, zi_gs, valid_gs = bitstrings_to_connected_zz(result_gs, n_boundary=N_BOUNDARY)
    E0 = energy_proxy_from_zz(zz_gs, zi_gs)
    print(f"    E0 (connected-ZZ) = {E0:.6f}  (valid shots: {valid_gs}/{SHOTS_GS})")

    # TEE measurement from ground state (HYP-020)
    print("\n[2] TEE measurement (HYP-020, marginal cost)...")
    # Note: in production, submit separate TEE partition tasks with more shots.
    # Here we reuse the ground state result for a first estimate.
    tee_result = compute_tee(result_gs)
    print(f"    S_topo = {tee_result['S_topo']:.4f} +/- {tee_result['S_topo_err']:.4f} nats")
    print(f"    Predicted: {tee_result['S_topo_predicted']:.4f} nats")
    print(f"    Z_ferromagnetic check: {tee_result['Z_ferromagnetic_check']}")
    print(f"    <Z>_avg = {tee_result['Z_avg']:.4f}")

    # ── Step 2: Single-hologron measurements ─────────────────────────────────
    print("\n[3] Single-hologron measurements (anchor site only)...")
    prog_single_anchor = build_ahs_program(excited_sites=[ANCHOR])
    result_single_anchor = submit_and_wait(prog_single_anchor, SHOTS_SINGLE,
                                           device, f"single hologron (anchor={ANCHOR})")
    zz_single_anchor, zi_single_anchor, _ = bitstrings_to_connected_zz(result_single_anchor, n_boundary=N_BOUNDARY)
    E_single_anchor = energy_proxy_from_zz(zz_single_anchor, zi_single_anchor)
    print(f"    E_single(anchor) connected-ZZ = {E_single_anchor:.6f}")

    # ── Step 3: Dual-hologron force profile ──────────────────────────────────
    print("\n[4] Dual-hologron force profile measurements...")
    F_values = []
    F_errors = []
    E_duals = []

    for dr in DR_VALUES:
        site_j = ANCHOR
        site_k = ANCHOR + dr
        if site_k >= N_BOUNDARY:
            print(f"    dr={dr}: site {site_k} out of boundary range, skipping")
            F_values.append(float("nan"))
            F_errors.append(float("nan"))
            E_duals.append(float("nan"))
            continue

        # Single hologron at site_k (for symmetric force definition)
        prog_single_k = build_ahs_program(excited_sites=[site_k])
        result_single_k = submit_and_wait(prog_single_k, SHOTS_SINGLE,
                                          device, f"single hologron (site={site_k})")
        zz_single_k, zi_single_k, _ = bitstrings_to_connected_zz(result_single_k, n_boundary=N_BOUNDARY)
        E_single_k = energy_proxy_from_zz(zz_single_k, zi_single_k)

        # Dual hologron at anchor and site_k
        prog_dual = build_ahs_program(excited_sites=[site_j, site_k])
        result_dual = submit_and_wait(prog_dual, SHOTS_DUAL, device,
                                      f"dual hologron dr={dr}")
        zz_dual, zi_dual, n_valid_dual = bitstrings_to_connected_zz(result_dual, n_boundary=N_BOUNDARY)
        E_dual = energy_proxy_from_zz(zz_dual, zi_dual)
        E_duals.append(E_dual)

        # F(dr) = E_dual - E0 - 2*(E_single_anchor - E0) - 2*(E_single_k - E0)
        # Simplified: F(dr) = E_dual - E0 - (E_single_anchor - E0) - (E_single_k - E0)
        F_dr = E_dual - E0 - (E_single_anchor - E0) - (E_single_k - E0)

        # Shot noise error estimate
        E_scale = abs(E0) * 0.01  # ~1% energy scale
        shot_err = E_scale / np.sqrt(n_valid_dual)
        analog_err = abs(F_dr) * 0.06  # 6% analog error
        F_err = np.sqrt(shot_err**2 + analog_err**2)

        F_values.append(float(F_dr))
        F_errors.append(float(F_err))

        print(f"    dr={dr:2d}: F={F_dr:+.6f} +/- {F_err:.6f}  "
              f"(ref: {V_DATA_REF.get(dr, float('nan')):+.6f})")

    # ── Step 4: Fit power law ─────────────────────────────────────────────────
    print("\n[5] Power-law fit F(dr) = A * dr^{-alpha}...")
    fit = fit_force_profile(DR_VALUES, F_values, F_errors, fit_dr_min=2)
    print(f"    alpha = {fit['alpha']:.3f} +/- {fit['dalpha']:.3f}")
    print(f"    A     = {fit['A']:.3f} +/- {fit['dA']:.3f}")
    print(f"    Reference (SIM-2026-015d chi=3 MERA): alpha={ALPHA_REF:.3f} +/- 0.178")
    print(f"    Fit points: {fit['n_points']}")

    # ── Step 5: Publication threshold check ──────────────────────────────────
    print("\n[6] Publication threshold checks...")
    alpha_ok = (not np.isnan(fit["alpha"]) and
                abs(fit["alpha"] - 4.0) < 0.5 and
                fit["alpha"] / fit["dalpha"] > 3.0)
    # Critical Ising CFT has NO topological order: predicted S_topo = 0.
    # |S_topo| < 0.2 is a positive confirmation of criticality, not a failure.
    tee_ok = (not np.isnan(tee_result["S_topo"]) and
              abs(tee_result["S_topo"]) < 0.2)
    z_ok = abs(tee_result["Z_avg"]) < 0.05

    print(f"    alpha ~ 4: {'PASS' if alpha_ok else 'FAIL/INCONCLUSIVE'}")
    print(f"    TEE ~ 0 (critical Ising): {'PASS' if tee_ok else 'FAIL/INCONCLUSIVE'}")
    print(f"    Non-ferromagnetic: {'PASS' if z_ok else 'FAIL'}")

    # ── Save results ──────────────────────────────────────────────────────────
    t_elapsed = time.time() - t_start
    results = {
        "hypothesis": "HYP-2026-017 + HYP-2026-020",
        "platform": "QuEra Aquila (analog Rydberg)" if not USE_LOCAL else "Local Braket emulator",
        "mode": "local_simulator" if USE_LOCAL else "real_hardware",
        "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "elapsed_s": round(t_elapsed, 1),
        "n_atoms": N_ATOMS,
        "n_boundary": N_BOUNDARY,
        "T_total_us": T_TOTAL,
        "T2_headroom_us": round(4.0 - T_TOTAL, 2),
        "E0": float(E0),
        "E_single_anchor": float(E_single_anchor),
        "dr_values": DR_VALUES,
        "F_values": [float(x) for x in F_values],
        "F_errors": [float(x) for x in F_errors],
        "F_ref_SIM015d": [V_DATA_REF.get(dr, float("nan")) for dr in DR_VALUES],
        "fit": fit,
        "alpha_reference": ALPHA_REF,
        "sigma_alpha_expected": float(sigma_alpha),
        "tee": tee_result,
        "publication_checks": {
            "alpha_within_0p5_of_4_at_3sigma": bool(alpha_ok),
            "tee_within_0p2_of_ln2": bool(tee_ok),
            "non_ferromagnetic": bool(z_ok),
        },
        "cost_estimate": {
            "shots_gs": SHOTS_GS,
            "shots_single_per_dr": SHOTS_SINGLE,
            "shots_dual_per_dr": SHOTS_DUAL,
            "n_dr": len(DR_VALUES),
            "shots_tee": SHOTS_TEE * 6,
            "total_shots_approx": (SHOTS_GS + len(DR_VALUES) * (2 * SHOTS_SINGLE + SHOTS_DUAL)
                                   + SHOTS_TEE * 6),
            "cost_usd_estimate": round(
                (SHOTS_GS + len(DR_VALUES) * (2 * SHOTS_SINGLE + SHOTS_DUAL)
                 + SHOTS_TEE * 6) * 0.01, 2
            ),
        },
    }

    with open(RESULTS_PATH, "w") as f:
        json.dump(results, f, indent=2)
    print(f"\nResults saved: {RESULTS_PATH}")

    # ── Plot ──────────────────────────────────────────────────────────────────
    try:
        fig, axes = plt.subplots(1, 2, figsize=(12, 5))

        # Force profile
        ax = axes[0]
        dr_arr = np.array(DR_VALUES)
        F_arr = np.array(F_values)
        F_err_arr = np.array(F_errors)

        valid = np.isfinite(F_arr) & (F_arr < 0)
        if valid.any():
            ax.errorbar(dr_arr[valid], -F_arr[valid], yerr=F_err_arr[valid],
                        fmt="o", color="royalblue", label="Aquila (this run)", zorder=5)
        ax.plot(dr_arr, [abs(V_DATA_REF.get(d, float("nan"))) for d in DR_VALUES],
                "s--", color="orange", alpha=0.7, label=f"SIM-015d chi=3 MERA (alpha={ALPHA_REF:.2f})")

        if not np.isnan(fit["alpha"]):
            dr_fit = np.linspace(2, 8, 100)
            F_fit = fit["A"] * dr_fit ** (-fit["alpha"])
            ax.plot(dr_fit, F_fit, "-", color="royalblue", alpha=0.5,
                    label=f"Fit alpha={fit['alpha']:.2f}+/-{fit['dalpha']:.2f}")

        # Power law reference line
        dr_ref = np.linspace(1.5, 8.5, 100)
        ax.plot(dr_ref, A_REF * dr_ref**(-4.0), "k:", alpha=0.4, label="alpha=4.0 prediction")
        ax.set_xscale("log"); ax.set_yscale("log")
        ax.set_xlabel("dr (boundary separation)"); ax.set_ylabel("|F(dr)|")
        ax.set_title("Holographic Force Profile (HYP-017)")
        ax.legend(fontsize=8)
        ax.grid(True, alpha=0.3)

        # TEE bar chart
        ax2 = axes[1]
        tee_keys = ["S_B", "S_AB", "S_BC", "S_ABC", "S_topo"]
        tee_vals = [tee_result.get(k, float("nan")) for k in tee_keys]
        colors = ["steelblue"] * 4 + ["crimson"]
        bars = ax2.bar(tee_keys, tee_vals, color=colors, alpha=0.7)
        # Predicted S_topo = 0 for critical Ising CFT (no topological order).
        ax2.axhline(0.0, color="k", linestyle="--", alpha=0.6,
                    label="S_topo_pred = 0 (critical Ising)")
        ax2.axhline(-np.log(2), color="gray", linestyle=":", alpha=0.4,
                    label=f"-ln(2) = {-np.log(2):.3f} (toric code, NOT our state)")
        ax2.set_ylabel("Entropy (nats)")
        ax2.set_title("TEE Kitaev-Preskill (HYP-020)")
        ax2.legend()
        ax2.grid(True, alpha=0.3, axis="y")

        plt.tight_layout()
        plt.savefig(FIGURE_PATH, dpi=150)
        print(f"Figure saved: {FIGURE_PATH}")
        plt.close()
    except Exception as e:
        print(f"Plot skipped: {e}")

    print(f"\nTotal runtime: {t_elapsed:.1f}s")
    return results


if __name__ == "__main__":
    main()
