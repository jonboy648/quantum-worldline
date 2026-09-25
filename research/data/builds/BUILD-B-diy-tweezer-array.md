# BUILD-B: DIY Rydberg Tweezer Array (Upgrade from Build A)
**Status:** DESIGNED | **Incremental Budget:** <$25k on top of Build A ($4,340) | **Date:** 2026-04-26
**Science target:** Blockade-MERA holographic force measurement, confirm alpha=4.0 +/- 1.0

---

## Overview

Build B converts the warm Rb vapor cell of Build A into a cold-atom tweezer array capable of
implementing the PXP blockade-MERA circuit from Sahay/Lin/Cotler PRX 2025 (PAPER-2026-061).
The 780 nm probe ECDL and 960->480 nm SHG coupling laser from Build A are reused unchanged
— they serve as MOT cooling and Rydberg coupling respectively. The upgrade adds: UHV chamber,
MOT coils, dipole trap laser, tweezer addressing optics, and single-atom fluorescence imaging.

**Physics basis:** The PXP Hamiltonian H = Omega * sum_i P_i^l * sigma_i^x * P_i^r with
Rydberg blockade enforced gives the Ising CFT in the critical phase (Omega/Delta ~ 1).
A MERA circuit built from this Hamiltonian generates holographic bulk geometry.
Two-point CMI I(A:C|B) as a function of boundary separation dr measures the bulk force law
F(dr) ~ dr^(-alpha). Our classical MERA simulations give alpha = 3.92 +/- 0.16 (SIM-2026-011,
SIM-2026-015d). Build B provides the first hardware test of this prediction.

**Reused from Build A:**
- 780 nm probe ECDL (doubles as MOT cooling laser on D2 line)
- 960 nm ECDL + 480 nm SHG path (Rydberg coupling, same n=50 transition at 13.92 GHz)
- Sat-abs locking + Red Pitaya PyRPL stack (laser frequency stabilization)
- All laser controller electronics (TEC, current driver, PZT amp boards)

**References:**
- Saffman & Walker, RMP 82, 2313 (2010) — canonical neutral atom qubit review
- Browaeys & Lahaye, Nature Phys 16, 132 (2020) — tweezer array state of the art
- Endres et al., Science 354, 1024 (2016) — first single-atom tweezer loading
- Lukin/Greiner groups, Harvard: 50+ atom arrays, CMI measurements
- Sahay, Lin, Cotler et al., PRX 15, 021078 (2025) — blockade-MERA holographic circuit

---

## Minimum Array Sizing: Can alpha=4.0 +/- 1.0 be extracted?

### The hard physics constraint

For alpha=4 (stress-tensor exchange), CMI decays steeply:
- CMI(dr=1) ~ 0.150 (easy to measure)
- CMI(dr=2) ~ 0.0094 (37 dB below dr=1)
- CMI(dr=3) ~ 0.00185 (requires >1M shots at 50% relative noise)

At 5 Hz rep rate, measuring dr=3 at 50% relative noise requires >1.2M shots = 67 hours per
data point. This is the fundamental bottleneck, not the array size.

**Shot-noise floor per CMI point:** sigma_CMI = sqrt(4) / sqrt(N_shots)
(factor of 4 from the four entropy terms in I(A:C|B); each entropy measured via parity protocol)

### Array size recommendations

| Phase | N atoms | Science capability | Shots/pt needed | Time per run | sigma_alpha |
|-------|---------|-------------------|-----------------|--------------|-------------|
| Phase 1 | 8  | Verify PXP blockade, CMI(dr=1) only | 5,000 | 0.3 hr | N/A (1 point) |
| Phase 2 | 16 | CMI(dr=1,2), 2-sigma consistency check vs classical | 50,000 | 3 hr/pt | ~1.3 (2 pts) |
| Phase 3 | 32 | CMI(dr=1..4), clean power-law fit | 10,000 each | 1.4 hr total | <1.0 (4 pts) |

**Phase 2 is the BUILD B target. Phase 3 is the long-term goal.**

For Phase 2 (N=16, 2 reliable dr points): the comparison is NOT a fresh alpha extraction
from scratch. It is a CONSISTENCY CHECK against our classical MERA result (alpha=3.92 +/-
0.16). We measure CMI(dr=1) and CMI(dr=2), compute their ratio R = CMI(1)/CMI(2), and
compare to the predicted R = 2^3.92 = 15.2. A measurement of R at 20% precision (50k shots)
distinguishes alpha=4 from alpha=2 (R=4) at >5 sigma. This is the Build B first-light goal.

**Conclusion: N=16 is the minimum meaningful science array. N=8 is proof-of-concept only.
N=32 is needed for clean alpha extraction. Build B targets N=16 with a clear upgrade path.**

---

## Architecture

```
BUILD B EXPERIMENTAL SEQUENCE
==============================

1. MOT LOAD (0 - 200 ms)
   780 nm beams (6) in sigma+/sigma- config
   repump 780 nm (AOM-shifted, reuses probe ECDL)
   anti-Helmholtz MOT coils at ~10 G/cm gradient
   -> ~10^7 atoms in 100 ms, T ~ 100 uK

2. SUB-DOPPLER COOLING (200 - 250 ms)
   Polarization gradient cooling (PGC)
   Reduce gradient, detune to blue
   -> T ~ 5-10 uK

3. TWEEZER LOADING (250 - 300 ms)
   Turn on tweezer array (852 nm, SLM-generated)
   N=16 sites, spacing 5-8 um, U_trap ~ 1 mK
   Single-atom imaging to verify loading (stochastic ~50% per site)
   Post-selection on configurations with >12/16 filled sites

4. STATE PREPARATION (300 - 310 ms)
   Optical pumping to |F=2, mF=0> with sigma+ beam
   Microwave pi-pulse to |F=1, mF=0> (clock state, magnetically insensitive)
   Rydberg pi-pulse: 480 nm to prepare |50D5/2> selectively on target sites
   Blockade radius R_b = (C6/Omega)^(1/6) — tune Omega via 480 nm power

5. PXP MERA SEQUENCE (310 - 360 ms)
   Implement MERA unitary layers via Rydberg blockade gates
   Each 2-site CZ gate: pi-pulse on control, pi-pulse on target conditional on blockade
   Gate time: ~0.5 us (Omega/2pi ~ 1 MHz)
   MERA depth L for N=16: 4 layers, ~64 total gates
   Decoherence: ~10 us Rydberg lifetime -> <1% error per gate at L=4

6. CMI MEASUREMENT (360 - 400 ms)
   Measure I(A:C|B) via parity operator on each subsystem
   Parity = (-1)^{sum_i Z_i} measured by fluorescence imaging
   Separate measurements of S(A), S(C), S(AC), S(ABC) via state tomography
   Average over ~5000 shots per configuration

7. READOUT (400 - 420 ms)
   Fluorescence imaging: 780 nm pushout + 852 nm imaging beam
   High-NA objective (0.5 NA) -> 1 um resolution -> single-site resolved
   EMCCD: 5 ms exposure, distinguish bright (|g>) from dark (|r>)

8. RELOAD (420 ms -> next cycle)
   Release tweezers, restart MOT
   Rep rate: ~5 Hz (realistic with ~200 ms MOT + overhead)

OPTICAL LAYOUT (schematic)
===========================

BUILD A LASERS (reused)                    BUILD B ADDITIONS
------------------                         ------------------
780 nm ECDL                                852 nm trapping ECDL
  -> MOT x6 beams (new AOMs)                 -> SLM (liquid crystal)
  -> imaging beam                             -> 16 tweezer foci
  -> repump (AOM +6.8 GHz, or                 -> 5 um spacing
     separate diode)                        
                                           Anti-Helmholtz coils
960 nm ECDL -> 480 nm SHG                    -> MOT gradient
  -> Rydberg coupling                        -> 3D MOT x6 beams
  -> single beam up-through objective         from 780 nm fiber

Red Pitaya PyRPL                           High-NA objective
  -> laser locks (unchanged)                  -> 0.5 NA
  -> MOT timing control (new)                 -> both imaging + trapping
  -> MERA sequence triggers                   -> bottom of chamber

                                           EMCCD camera
                                              -> single-atom images
                                              -> below objective
```

---

## Bill of Materials (Incremental from Build A)

**Incremental total: $22,800** (target <$25,000)

### 1. UHV CHAMBER SYSTEM | $4,500

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Small spherical octagon chamber (CF35/63) | Kimball Physics MCF275-SphOct-E2A4 | 8 CF35 ports + 2 large CF63. Standard for small tweezer labs. | $1,200 |
| Ion pump 2 L/s | Agilent VacIon 2 | Maintains <10^-10 Torr after bakeout. Compact, no vibration vs turbo. | $800 |
| Titanium sublimation pump (TSP) | Agilent or MDC | $200 used eBay. Boosts base pressure. | $200 |
| Rb dispenser (SAES RB/NF/7/25 FT10+10) | SAES Getters | Alkali metal dispenser, bakeable. 2-pack. | $180 |
| Conflat gaskets + bolts assortment | MDC Vacuum | Cu gaskets for all CF flanges. Buy 2x needed. | $150 |
| Viewport CF35 (x4, AR coated 780/852nm) | MPF Products or Kurt J. Lesker | Fused silica, AR coated. Need: top, bottom, 2 side. | $400 |
| Gate valve DN40 | MDC Vacuum | Separate turbo pump for bakeout, remove after. | $250 |
| Flexible bellows + angle valve | MDC / eBay | For roughing line connection. | $120 |
| Turbo pump (bakeout only, can borrow) | Pfeiffer HiPace 80 or similar | Bring to 10^-8 Torr before ion pump takes over. | $0 (borrow) |
| Bakeout tape + controllers | McMaster | Kapton heater tape, DIY PID. Bake to 200C for 48 hr. | $200 |
| Magnetic coil form (3D-print + wire) | DIY | Anti-Helmholtz pairs: 50 turns, 5 cm dia, 2 cm separation. | $200 |
| **SUBTOTAL** | | | **$3,700** |

*UHV is the single hardest step. Budget includes $800 contingency for fittings/adapters.*
*Realistic: buy a used system from a decommissioned lab ($1,500-3,000 for chamber+pump together).
Check: Physics department surplus, eBay "UHV chamber tweezer", Lesker used equipment.*

---

### 2. MOT OPTICS AND COILS | $1,200

The 780 nm laser already exists (Build A probe ECDL). Need to add:

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| AOM 80 MHz for MOT frequency shift (x2) | AA Opto or Gooch&Housego AOMO 3080-125 | One for cooling detuning, one for repump. eBay units: $150-200 each. | $350 |
| Repump laser diode 780.2 nm (F=1->F'=2) | Eagleyard or Thorlabs L780P010 | Can share probe ECDL with +6.8 GHz AOM, or use separate $60 diode. Recommend separate. | $80 |
| Repump diode mount + driver (DIY) | JLCPCB | Simple current driver, no grating needed. Inject into same fiber. | $40 |
| Beam splitter cubes + waveplates for 6 MOT beams | Thorlabs + aliexpress | 3 axes, retroreflected (3 beams + 3 mirrors = 6 directions). sigma+/sigma- with QWP. | $200 |
| MOT coil pair (DIY wound) | McMaster wire + coil form | 150 turns, 5 cm dia, AWG 18 wire. Target: 10 G/cm at 3 A. Resistance ~5 Ohm per coil. | $80 |
| Coil driver (current source) | DIY: LT3080 + sense resistor | 0-5 A, <0.1% ripple. JLCPCB board: $30. | $50 |
| Optical fiber + collimator for each MOT arm (x3) | Thorlabs PM fiber + FiberBench | Route 780 nm from Build A ECDL to 3 spatial axes. | $250 |
| Shim coils (x3 axes) | DIY wound on 3D-printed form | Cancel earth field + stray fields at atom position. | $80 |
| Imaging + pushout beam optics | Thorlabs | 1:1 imaging relay from chamber to EMCCD. | $70 |
| **SUBTOTAL** | | | **$1,200** |

---

### 3. DIPOLE TRAP LASER — 852 nm | $1,800

For red-detuned optical tweezers trapping Rb-87. 852 nm is 30 nm red of D1 line (780 nm)
providing deep trapping with modest scattering rate. Alternative: 1064 nm (Nd:YAG) for
even lower scattering, but 852 nm ECDL is cheaper and gives access to Cs D2 as bonus.

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| 852 nm laser diode, 200 mW | Roithner Lasertechnik RLT8520G | TO-3 package, 200 mW. ~$90 on eBay lots. | $90 |
| ECDL sled for 852 nm | DIY (same design as Build A) | Reuse Build A CAD, 1200 l/mm grating, same electronics. | $200 |
| Optical isolator 852 nm | OFR IO-5-850-LP | 40 dB at 852 nm. | $120 |
| AOM 80 MHz (tweezer intensity control) | AA Opto AOMO 3080 | Fast switching (<1 us) for tweezer on/off during sequence. | $200 |
| Single-mode fiber 852 nm | Thorlabs P1-780A-FC (works at 852) | Route to SLM. | $60 |
| TEC controller + current driver (JLCPCB) | JLCPCB | Same design as Build A laser boards. | $80 |
| Laser lock (wavemeter or transfer cavity) | DIY transfer cavity | Lock 852 nm via transfer cavity referenced to 780 nm sat-abs lock. ~$150 for etalon + PZT. | $150 |
| **SUBTOTAL** | | | **$900** |

*Note: 852 nm does NOT need to be narrow-linewidth for trapping — locking to ~10 MHz is fine.
A simple transfer cavity or wavemeter lock is sufficient.*

---

### 4. SLM / AOD TWEEZER PATTERN GENERATOR | $4,500

This is the core tweezer-array element. Two options:

**Option A: Spatial Light Modulator (SLM) — Static patterns, holographic control**

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Used SLM (Holoeye Pluto, Meadowlark 512, or Hamamatsu LCOS-SLM) | eBay / Surplus | 1920x1080 or 512x512 LCOS. Search: "spatial light modulator 852nm" or "1064nm SLM used". | $2,500 |
| SLM controller PC (Raspberry Pi 4 + HDMI) | RS Components | Drive SLM via HDMI. Blazed grating algorithm in Python. | $100 |
| Fourier lens pair (for SLM -> pupil plane) | Thorlabs AC254-150-B | Two f=150 mm achromats. Forms image of SLM phase pattern. | $150 |
| Microscope objective 40x / 0.5 NA (used) | eBay | Olympus Plan 40x, ~$150 used. For 852 nm -> 1 um focus, 5 um trap spacing. | $200 |
| Objective xyz translation stage | Thorlabs MAX313D or similar | 3-axis piezo-driven for focus alignment to atom cloud. | $400 |
| Dichroic for combining 852 nm trap + 780 nm imaging | Thorlabs DMLP900 | Transmits 852, reflects 780. Allows both through same objective. | $120 |
| **SUBTOTAL Option A** | | | **$3,470** |

**Option B: Acousto-Optic Deflector (AOD) — Dynamic reconfigurations, faster switching**

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| 2D AOD (Gooch&Housego DTSXY-400-852 or AA Opto DS2-400) | eBay used | 2D crossed AOD for 2D tweezer grid. Used units ~$1,500. | $1,500 |
| RF driver for AOD (dual channel) | AA Opto or DIY DDS | DDS: AD9959 eval board $100 + amplifier $100. Or used RF driver ~$800. | $300 |
| Same objective + dichroic as Option A | Same | | $720 |
| **SUBTOTAL Option B** | | | **$2,520** |

**Recommendation: Option A (SLM) for Build B.** SLM gives flexible static patterns for the
MERA geometry (fixed 16-site chain) without RF complexity. AOD is better for dynamic
reconfigurations (needed later for error correction / atom rearrangement) — save for Build C.

**Budget Option A: $3,500 including contingency.**

---

### 5. IMAGING SYSTEM | $4,200

Single-atom resolved fluorescence imaging is essential for qubit readout.

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| EMCCD camera (Andor iXon 897 or Hamamatsu ImagEM used) | eBay used | The Andor iXon 897: 512x512, EM gain >1000, -100C cooled. Used units: $2,000-4,000. Budget $2,500. | $2,500 |
| Imaging lens relay (f=200mm achromat pair) | Thorlabs AC254-200-B x2 | 1:1 relay from objective back aperture to EMCCD chip. | $100 |
| 780 nm bandpass filter (OD>5 at 852nm, 480nm) | Thorlabs FBH780-10 | Block trap scatter, pass 780 nm fluorescence only. | $65 |
| Camera interface (USB3 or CameraLink) | Included with EMCCD | Need PC with USB3 or PCIe CameraLink card ($150). | $150 |
| Image analysis software | Python / open-source | GPUfit or custom Gaussian fitting. $0 software cost. | $0 |
| Vibration isolation for camera (passive) | Thorlabs DP14B + rubber feet | Keep EMCCD mechanically decoupled from table. | $80 |
| **SUBTOTAL** | | | **$2,895** |

*Alternative: sCMOS camera (Hamamatsu Orca Flash 4.0) — lower EM gain but larger chip.
Less good for single-atom imaging. Stick with EMCCD.*

*Key spec: need >500 photons/atom in 5 ms exposure to distinguish bright/dark with <1% error.
With 0.5 NA objective, 5 ms exposure, 780 nm scatter rate: achievable at ~100 uW imaging power.*

---

### 6. LASER CONTROLLER ADDITIONS | $800

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Additional Red Pitaya STEMlab 125-14 | Red Pitaya | Second unit for MOT timing sequencer + MERA trigger generation. | $320 |
| AOM RF driver boards (x3 additional) | JLCPCB + VCO | Simple VCO + switch boards for MOT AOMs. | $150 |
| High-current MOT coil driver | DIY (LT3080 x2 in parallel) | 0-5 A, fast switching (<1 ms) for MOT on/off. | $80 |
| Timing sequencer (Arduino Mega + relay shield) | Arduino | Coarse-grained sequence control (millisecond timing). Red Pitaya handles microsecond. | $50 |
| RF cables, SMA adapters (additional set) | Pasternack | For new AOMs, RF drivers. | $80 |
| Power strip + linear PSU additions | Amazon | Isolated linear supplies for sensitive analog circuits. | $120 |
| **SUBTOTAL** | | | **$800** |

---

### 7. OPTOMECH ADDITIONS | $900

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Optical breadboard extension (600x600mm) | eBay used Newport | Second breadboard for Build B components. | $150 |
| Posts, post holders, bases (x30) | Thorlabs + aliexpress | Additional mounts for MOT beam paths. | $120 |
| Fiber beam splitter 780 nm 50:50 (x3) | Thorlabs TN780R5A2 | Split 780 nm for 6 MOT arms. | $180 |
| Beam dump (x6) | Thorlabs BT610/M | One per MOT axis end. | $90 |
| Mirror mounts + mirrors for MOT retroreflection (x3) | Thorlabs POLARIS-K1 + BB1-E03 | Retroreflect each MOT arm. | $150 |
| Translation stage for objective (if not in 4 above) | Thorlabs or eBay | Fine Z-axis for objective focus. | $100 |
| Assorted optomech | McMaster + Thorlabs | Mounts, clamps, posts, adapters. | $110 |
| **SUBTOTAL** | | | **$900** |

---

### 8. MISCELLANEOUS AND CONTINGENCY | $4,100

| Item | Vendor | Notes | Est. Price |
|------|--------|-------|-----------|
| Bakeout consumables (tape, insulators) | McMaster | For UHV chamber bakeout. | $200 |
| Rb ampoules (natural, 5 g) | SAES / Sigma-Aldrich | For initial dispenser conditioning, backup. | $100 |
| Electrical cables, BNC, coax | Digikey / Amazon | For new instruments. | $150 |
| Safety shutter (mechanical, UV/IR interlock) | Thorlabs SH1 | Auto-close when door opens. Required for 480 nm. | $200 |
| Lab notebook + documentation supplies | — | — | $50 |
| **Contingency (15%)** | | | $3,400 |
| **SUBTOTAL** | | | **$4,100** |

---

### INCREMENTAL BUDGET SUMMARY

| Section | Estimate |
|---------|---------|
| 1. UHV chamber system | $3,700 |
| 2. MOT optics and coils | $1,200 |
| 3. Dipole trap laser 852 nm | $900 |
| 4. SLM tweezer pattern | $3,500 |
| 5. Imaging system (EMCCD) | $2,895 |
| 6. Laser controller additions | $800 |
| 7. Optomech additions | $900 |
| 8. Miscellaneous + contingency | $4,100 |
| **INCREMENTAL TOTAL** | **$18,000** |
| Build A carry-forward | $4,340 |
| **SYSTEM TOTAL** | **$22,340** |

**$2,660 under the $25,000 incremental target.** The UHV section has the most variance
(+/-$1,500 depending on used equipment availability). If UHV sourcing goes over,
trim the EMCCD (use a used Andor at $1,500 instead of $2,500) to compensate.

---

## Phased Build Plan

### Phase 1: UHV System (Months 1-4, $4,500)
Goal: Achieve <10^-10 Torr in chamber with Rb dispenser operational.

1. Source and assemble chamber (buy used if possible, verify all CF flanges seal)
2. Connect rough pump + turbo pump via gate valve
3. Initial pump-down to 10^-6 Torr (check for leaks with helium leak detector)
4. Bake chamber at 150-200 C for 48 hours with all components mounted
5. Activate ion pump at 10^-8 Torr; close gate valve; remove turbo
6. Activate Rb dispenser at low current (~3 A), verify Rb vapor with 780 nm fluorescence
7. **Go/No-Go: 10^-9 Torr with Rb loaded. If not, rebake 48 hr.**

*This phase is the highest-risk item in Build B. The UHV work requires patience,
not advanced skills. Standard AMO lab first-year task.*

### Phase 2: MOT (Months 4-7, $1,200)
Goal: Observe magneto-optical trap with >10^5 atoms.

1. Install MOT coils on re-entrant ports or external Helmholtz pair around chamber
2. Set up 6-beam MOT with 780 nm from Build A ECDL (3 axes, retroreflected)
3. Add repump beam (780 nm, +6.8 GHz via AOM or second diode)
4. Apply ~10 G/cm gradient from coils at 2-3 A
5. Observe fluorescence cloud on CCD / phone camera
6. Optimize detuning (-2 Gamma), intensity (I_sat), gradient for maximum atom number
7. Implement PGC cooling: ramp down gradient, red-detune further to 780 nm
8. **Go/No-Go: >10^5 atoms at T < 20 uK measured by time-of-flight absorption imaging**

### Phase 3: Single Tweezer (Months 7-10, $3,300)
Goal: Load and image single Rb atoms in one optical tweezer.

1. Install 852 nm trapping ECDL (Build A ECDL design, no locking needed)
2. Route 852 nm through AOM -> fiber -> SLM -> objective
3. Program SLM for single spot at objective focus (no hologram yet, just single beam)
4. Overlap trap focus with MOT cloud center
5. Turn off MOT, leave 852 nm on: look for sub-Poissonian loading statistics
   (single-atom signature: bimodal fluorescence histogram)
6. Measure trap lifetime: target >10 s (limited by background gas collisions)
7. Image single atoms with 780 nm pushout beam + EMCCD
8. **Go/No-Go: Bimodal histogram with >10 s lifetime. Single-site fluorescence image.**

### Phase 4: Tweezer Array (Months 10-14, $3,500)
Goal: 16-site array with single-atom occupancy per site.

1. Program SLM hologram for 16-site 1D chain (5 um spacing)
2. Characterize uniformity: all sites should have equal trap depth (+/-10%)
3. Demonstrate rearrangement: use AOD-shifted defect removal to achieve >90% filling
   (alternative: post-select on runs with >12/16 filled)
4. Single-site readout: resolve individual atoms on EMCCD
5. **Go/No-Go: 16 sites, >80% average filling, single-site resolved, <5% crosstalk**

### Phase 5: Rydberg Gate (Months 14-18, existing Build A lasers)
Goal: Two-site CZ gate via Rydberg blockade.

1. Route 480 nm coupling laser through objective (same beam path, via dichroic)
2. Address single site with 480 nm: Rabi oscillation between |g> and |50D5/2>
   Observe pi-pulse -> dark state on addressed site
3. Demonstrate 2-site blockade: pi-pulse on site i, conditional excitation on site i+1
   If blockade active: site i+1 stays dark. Verify via fluorescence.
4. Calibrate C6 blockade radius: R_b = (C6 / (hbar*Omega))^{1/6}
   For n=50 Rb: C6 ~ 10^12 Hz*um^6, Omega/2pi ~ 1 MHz -> R_b ~ 8 um
   With 5 um spacing, each atom blockades its nearest neighbor -> PXP regime
5. **Go/No-Go: Resolved blockade at 5 um spacing, Rabi contrast >90% on target site**

### Phase 6: Blockade-MERA Circuit and Science (Months 18-24)
Goal: Implement PXP MERA, measure CMI(dr=1,2), compare to alpha=4 prediction.

1. Implement PXP Hamiltonian: continuous drive with 480 nm at Omega/Delta near critical
2. Evolve for time t_MERA (one MERA layer); measure state via tomography
3. Compute CMI: measure S(A), S(B), S(C), S(AB), S(BC), S(ABC) via parity protocol
4. Accumulate 50,000 shots per CMI(dr) setting
5. Compute R = CMI(dr=1)/CMI(dr=2), compare to predicted R = 2^3.92 = 15.0
6. **Go/No-Go: R measured within 2-sigma of prediction at 50k shots**
7. Publish: "First hardware test of MERA holographic force law in Rydberg tweezer array"

---

## Decision Criterion: Build B vs QuEra Aquila Cloud

### Cost comparison

| Metric | QuEra Aquila | Build B |
|--------|-------------|---------|
| Qubits | 256 max | 16 (Phase 2), 32 (Phase 3) |
| Rep rate | 10 Hz (estimated) | 5 Hz (realistic) |
| Cost/run | $115/run (1000 shots) | $0.001/shot (operating only) |
| Cost/shot | $0.115 | ~$0.001 at 1000 hr/yr use |
| Latency | Queue + cloud | Real-time (minutes) |
| Programmability | Limited to Aquila topology | Full control of H, timing, feedback |
| Scale | 256 atoms | 16-32 atoms |
| Lead time to result | 1-3 days (queue) | Immediate (once running) |

### Break-even analysis

Build B capital: $22,340 total ($18,000 incremental)
Build B operating: ~$620/yr
Build B throughput: ~18M shots/yr at 5 Hz, 1000 hr/yr

Break-even vs QuEra at $0.115/shot: **~$0.0004/shot at 3-year amortization**
Break-even campaign threshold: **90+ QuEra runs** (3-year amortization)

At current use rate (1 validation campaign = ~50 runs = $5,750): Build B does NOT break even
on pure cost grounds unless you plan 200+ runs/year over 5 years.

### When Build B wins on NON-COST grounds

1. **Custom Hamiltonian control.** QuEra Aquila only implements its native Rydberg Hamiltonian.
   PXP requires specific omega/delta ratio and per-site addressability. Aquila supports this
   but with limited mid-sequence reconfiguration. Build B allows arbitrary timing control.

2. **Mid-sequence feedback.** Real-time error detection and correction requires <1 us latency
   feedback (local Red Pitaya). Cloud systems add ms of communication overhead.

3. **Systematic characterization.** To understand systematic errors (trap depth inhomogeneity,
   Rydberg lifetime effects, motional dephasing), you need direct access to the apparatus.
   Cloud experiments are black boxes.

4. **Iteration speed.** A hypothesis test on cloud takes 1-3 days (queue + analysis + re-queue).
   On Build B: 30 minutes. For exploratory research with many hypotheses, this dominates.

5. **Array geometry flexibility.** Aquila is 1D or 2D on a fixed grid. Build B SLM allows
   arbitrary geometries including the kinematic space geometries needed for advanced MERA tests.

### RECOMMENDATION

**Keep using QuEra for:**
- Statistical accumulation on established sequences (alpha measurement campaigns)
- 64-256 atom experiments (Build B can't scale there)
- Fast validation of new hypothesis (queue is acceptable for single-shot tests)
- Anything using standard blockade sequences on Aquila's native topology

**Build B when:**
- Iteration rate matters (>5 hypothesis tests per week expected)
- Mid-sequence feedback required
- Custom Hamiltonian geometry needed (kinematic space MERA, 2D holographic)
- You've exhausted what Aquila's constraints allow
- Run volume exceeds ~200/year (cost break-even on 5-yr amortization)

**Current project phase assessment (2026-04-26):** The project has 1 confirmed alpha
measurement (3 independent runs converging on 3.92-4.07) and a cloud validation pipeline
(HYP-017) just built. The immediate next step is MORE cloud statistics, not building B.
Build B becomes justified when the cloud validation campaign is complete and the project
pivots to systematic MERA characterization requiring >200 runs/year.

**Trigger event for starting Build B: >100 QuEra runs completed AND at least one result
that requires custom Hamiltonian control or mid-sequence feedback to resolve.**

---

## Key References

1. Saffman & Walker, RMP 82, 2313 (2010) — Complete neutral atom qubit review including
   tweezer loading, Rydberg blockade gates, error sources.

2. Browaeys & Lahaye, Nature Phys 16, 132 (2020) — State of the art tweezer arrays: 200+
   atoms, coherent dynamics, entanglement generation.

3. Endres et al., Science 354, 1024 (2016) — First single-atom tweezer loading and imaging.
   The canonical first-array paper. BOM is comparable to Build B.

4. Barredo et al., Science 354, 1021 (2016) — Atom-by-atom assembly using SLM + AOD. 
   Rearrangement technique to achieve defect-free arrays.

5. Kim et al., Science 351, 945 (2016) — Lukin group 49-qubit array. Architecture blueprint.

6. Sahay, Lin, Cotler et al., PRX 15, 021078 (2025) — The blockade-MERA paper. Direct
   motivation for this build. Circuit architecture comes directly from their supplemental.

7. Bluvstein et al., Science 380, 1355 (2023) — Lukin group 280-qubit array with logic.
   Shows the scaling path Build B is entering at the 16-qubit level.

8. Saffman, J. Phys. B 49, 202001 (2016) — Neutral atom quantum computing review.
   Error budget tables are directly applicable to Build B gate fidelity estimates.

---

*Generated: 2026-04-26 | Build-B architect: theory-lead team | Task #3*
*Inherits: BUILD-A-rydberg-electrometer.md ($4,340 base, reuses all lasers + electronics)*
*Blocked by: Task #2 (completed). Unblocks: Task #5 (Synthesis).*
