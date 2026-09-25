# HYP-2026-017 + HYP-2026-020: QuEra Aquila Cloud Run

Joint AWS Braket submission. Tests two holographic signatures on analog Rydberg hardware.

**Cost: ~$115 total** ($85 HYP-017 + $30 HYP-020)  
**Do not submit to real Aquila without explicit approval.**

---

## What this tests

**HYP-017**: Is the holographic force exponent alpha=4 platform-independent?
- Already confirmed on 16q exact diagonalization (alpha=3.97+/-0.15) and chi=3 MERA (alpha=4.07+/-0.18) via SIM-2026-015d.
- This run tests whether native Rydberg blockade physics reproduces the same MERA entanglement structure.
- Expected: alpha=4.0 +/- 0.3-0.5 (wider error bar due to 4-8% analog noise).

**HYP-020**: Can we simultaneously measure topological entanglement entropy S_topo = -ln(2)?
- Marginal cost: 3,000 extra shots ($30). Uses same ground state.
- Expected: S_topo = -0.693 nats (Z2 topological order in MERA bulk).

---

## Setup

```bash
pip install amazon-braket-sdk bloqade numpy scipy matplotlib
```

AWS credentials required for real hardware (not for local simulator):
```bash
aws configure  # set AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, region=us-east-1
```

Braket must be enabled in your AWS account: AWS Console -> Amazon Braket -> Enable.

---

## Running locally (free, no AWS charges)

The script defaults to `USE_LOCAL = True` which runs the Braket local AHS emulator
via `LocalSimulator("braket_ahs")`. The default `LocalSimulator()` rejects AHS
programs with `NotImplementedError` — `"braket_ahs"` is required.

```bash
python HYP-2026-017-runnable.py
```

Local emulator limitations:
- Does not model Rydberg blockade exactly (uses mean-field approximation).
- No shot noise from real hardware.
- Results will differ from real Aquila; use to verify the script runs without errors.
- **State-vector blowup:** the AHS local sim builds a 2^N complex state vector.
  At N=30 atoms (full HYP-017 layout), this is ~16 GB minimum and will OOM on a
  16 GB workstation (observed: 54.7 GB resident before kill). Local emulator is
  practical only up to ~20-25 atoms. Real Aquila (256 atoms native) is the only
  way to run the full 30-atom layout end-to-end.

### Reduced 15-atom validator (local-emulator-friendly)

A reduced layout (`validator_*.py`) shrinks the production 30-atom binary tree to
a 15-atom version (8 boundary + 4 bond + 2 coarse + 1 bulk) so the AHS state
vector is 2^15 ~ 32 K (fits in <1 MB). Same 5-stage pulse protocol, same energy
estimator, same Renyi-2 collision TEE — just enough atoms to exercise the full
analysis pipeline without OOM.

| Part | File | Status |
|------|------|--------|
| 1. Atom layout | `validator_layout.py` | written, smoke test passes |
| 2. Pulse schedule | `validator_pulses.py` | written, smoke test passes |
| 3. Force + TEE estimators | `validator_force.py` | written, smoke test passes |
| 4. Runner + JSON output + verdict | `validator_main.py` | not yet written |

Acceptance criteria for Part 4 PASS:
- 10 tasks (1 GS + 1 single@anchor + 4 dual + 4 single@(anchor+dr)) submit and complete on `LocalSimulator("braket_ahs")`
- Peak resident memory < 4 GB
- All F(dr) values finite for dr=1..4
- Power-law fit on dr=2..4 yields alpha in [2, 6] (acceptance window from SIM-2026-023: [3.2, 4.8])
- TEE Renyi-2 collision returns finite value (sign and magnitude not gated; this is a smoke test, not a physics check)
- Output: `D:/quantum-worldline/research/data/builds/HYP-2026-017-validator-results.json` with PASS/FAIL verdict

A PASS on the validator does NOT prove alpha=4 — the 15-atom layout is too small
to give clean force statistics. It only proves the script runs end-to-end without
crashes. Real physics validation happens on the 256-atom Aquila run.

---

## Submitting to real Aquila ($115)

**Only do this with explicit user approval.**

1. Open `HYP-2026-017-runnable.py`.
2. Change line `USE_LOCAL = True` to `USE_LOCAL = False`.
3. Run: `python HYP-2026-017-runnable.py`

The script submits ~19 tasks to Aquila sequentially:
- 1 ground state task (1000 shots)
- 8 single-hologron tasks (500 shots each, one per dr)
- 8 dual-hologron tasks (1000 shots each, one per dr)
- TEE partition tasks (built into ground state readout)

Total shots: ~17,000. Cost at $0.01/shot: ~$170.  
To stay under $115, reduce `SHOTS_DUAL` from 1000 to 500 and `SHOTS_SINGLE` from 500 to 250.

Typical Aquila queue time: 5-30 minutes per task. Full run: several hours.

---

## Platform: QuEra Aquila (analog, NOT gate-based)

Aquila is an analog Rydberg tweezer array. It does NOT support discrete quantum gates.
The MERA circuit is encoded as:

- **Atom geometry**: 30 87Rb atoms in a 3-layer binary tree layout (5 um boundary spacing).
- **Global pulse**: time-dependent Omega(t) and Delta(t) driving all atoms simultaneously.
- **Blockade constraint**: adjacent boundary atoms (5 um spacing << blockade radius 9.76 um) are naturally blockade-coupled. This implements the MERA isometry without explicit gates.
- **Hologron injection**: local detuning shift (ShiftingField) at target boundary sites approximates the boundary-primary operator sigma_j.

Key constraint: Aquila has no single-qubit gates or mid-circuit measurement. The entire MERA state prep happens in a single 2.8 us pulse sequence. T2* = 4.0 us gives 1.2 us headroom.

---

## Atom layout

```
Layer 3 (UV, y=0):    o-o-o-o-o-o-o-o-o-o-o-o-o-o-o-o  16 boundary atoms, 5 um
Layer 2 (mid, y=10):    o   o   o   o   o   o   o   o    8 bond atoms, 10 um
Layer 1 (IR, y=20):         o       o       o       o    4 coarse atoms, 20 um
Layer 0 (bulk, y=30):               o               o    2 bulk atoms
```

Total: 30 atoms. Aquila supports up to 256.

---

## Force measurement protocol

```
F(dr) = E_dual(anchor, anchor+dr) - E0 - (E_single(anchor) - E0) - (E_single(anchor+dr) - E0)
```

Energy is estimated from Rydberg density via the TFIM-Rydberg mapping:
- `<Z_i> ~ 1 - 2*density_i`
- `E_proxy = -sum <Z_i Z_{i+1}> - sum <X_i>`

This is an approximation. The exact TFIM-Rydberg correspondence requires calibrating
Omega_max and Delta against J=1, g=1 TFIM parameters. If results are inconsistent,
recalibrate by sweeping (Omega_max, Delta_max) to minimize energy vs exact E0 = -20.016.

---

## TEE protocol (HYP-020)

Kitaev-Preskill formula: `S_topo = S_AB + S_BC - S_B - S_ABC`

Subsystems (0-indexed boundary sites):
- A = sites 0-4, B = sites 5-9, C = sites 10-15

Renyi-2 entropy estimated via collision probability from bitstring readout.
The script uses the same ground state measurement for TEE (no extra hardware cost).
For production, submit dedicated partition tasks with 500 shots each (6 tasks = $30).

Validity check: if `|<Z>_avg| > 0.1`, the ground state is ferromagnetic and TEE is invalid.
This is the Z2 symmetry trap documented in agent memory. Check this first.

---

## Expected results

| Quantity | Prediction | Pass threshold |
|----------|-----------|----------------|
| alpha | 4.0 +/- 0.3-0.5 | |alpha - 4.0| < 0.5 at 3-sigma |
| S_topo | -0.693 nats | |S_topo + 0.693| < 0.2 nats at 2-sigma |
| Z_avg | ~0 | |Z_avg| < 0.05 |
| dr_max clean | 3-4 | at least 3 points above shot noise |

Reference force values from SIM-2026-015d (chi=3 MERA, 16q):
- F(1) = -2.243, F(2) = -0.522, F(3) = -0.088, F(4) = -0.044
- F(5) = -0.025, F(6) = -0.013, F(7) = -0.007, F(8) = -0.003

Note: dr=1 is excluded from the power-law fit (contact term).

---

## Shot-noise precision estimate

The script runs a classical Monte Carlo at startup (no hardware needed) estimating
sigma_alpha under shot noise + 6% analog error. Expected result: sigma_alpha ~ 0.3-0.5.
This is wider than Helios (0.18) but sufficient to distinguish alpha=4 from alpha=2.

---

## Output files

- `HYP-2026-017-results.json`: Full numerical results, fit parameters, TEE values.
- `HYP-2026-017-force-profile.png`: Force profile comparison + TEE bar chart.

---

## If the run fails

Common failure modes:

1. **Z_avg > 0.1**: Ferromagnetic ground state. The pulse sequence did not implement
   the MERA isometry correctly. Try sweeping Delta_max upward (more blue-detuning)
   or extending T_LAYER3/T_LAYER2 by 0.1 us. This is the analog equivalent of the
   Z2 symmetry trap (see agent memory).

2. **F(dr) all near zero**: The hologron injection detuning is too weak. Increase
   `HOLOGRON_DELTA_MHZ` from 2.0 to 3.0-5.0 MHz.

3. **F(dr) wrong sign**: Energy estimator miscalibration. The TFIM-Rydberg mapping
   assumes Omega_max and Delta_end are tuned to the critical point. Recalibrate.

4. **alpha << 4**: Analog decoherence is dominating. This is expected if the state
   is ferromagnetic. Check Z_avg first. If Z_avg is OK, report as hardware
   characterization (strengthens case for Helios as necessary platform).

5. **Task queue timeout**: Aquila tasks can take 30+ minutes. The Braket SDK waits
   synchronously. For production runs, use async task submission with polling.

---

## Cost control

Current settings in the script:
- `SHOTS_GS = 1000` -> $10
- `SHOTS_SINGLE = 500` per site, 16 tasks -> $80
- `SHOTS_DUAL = 1000` per dr, 8 tasks -> $80
- TEE partitions built into GS readout -> $0 marginal

Total at these settings: ~$170. To hit $85 target, reduce to:
- `SHOTS_SINGLE = 250` per site -> $40
- `SHOTS_DUAL = 500` per dr -> $40

Minimum viable run (3-sigma on dr=2..4 only):
- `DR_VALUES = [1, 2, 3, 4]`, `SHOTS_DUAL = 1000` -> $40 + GS + singles = ~$65

---

## Files

- Script: `research/data/builds/HYP-2026-017-runnable.py`
- Build spec: `research/data/builds/HYP-2026-017.md`
- TEE spec: `research/data/builds/HYP-2026-020.md`
- Reference data: `research/data/simulations/SIM-2026-015d.json`
