# BUILD-A: DIY Rydberg Vapor-Cell Electrometer
**Status:** DESIGNED | **Budget:** $4,340 parts (target <$5k) | **Date:** 2026-04-26

## Overview

A complete DIY Rydberg atom electrometer based on electromagnetically induced transparency (EIT) and Autler-Townes (AT) splitting in a rubidium-87 vapor cell. Detects microwave/RF electric fields with SI-traceable sensitivity. Target: >=1 uV/m/sqrt(Hz) at first light, <=300 nV/m/sqrt(Hz) after optimization.

**Physics basis:** Probe laser (780 nm) drives |5S1/2> -> |5P3/2>. Coupling laser (480 nm) drives |5P3/2> -> |nD5/2> (n~50 Rydberg state). EIT transparency window appears at two-photon resonance. Applied RF field at the Rydberg-state transition frequency (e.g., ~13.9 GHz for 50D->51P) dresses the Rydberg level and splits the EIT peak (Autler-Townes splitting). Splitting frequency Omega_AT = d_n * E_rf / hbar directly gives E-field magnitude. n=50 dipole moment ~6340 Debye.

**Reference builds:**
- Holloway et al., NIST (2014-2022): SI-traceable E-field, 55 nV/m/sqrt(Hz) optimized
- Adams group, Durham: Teaching Rydberg EIT kits, <3000 GBP complete setups
- Shaffer group, Kansas/Rydberg Technologies: vapor cell + lock electronics architecture
- Bhatt et al. (2023): Red Pitaya-based lock, 780+480 two-photon scheme

---

## OPTICAL LAYOUT (ASCII)

```
PROBE ARM (780 nm)
==================

  [ECDL-780]--->[ISO]--->[HWP]--->[PBS]---+-->[SAT-ABS CELL]--->[PD-SAT]
                                           |       (Rb ref cell)
                                           |
                                     [HWP+PBS]
                                           |
                              +------------+
                              |
                         [AOM/EOM]         <-- optional freq modulation
                              |
                         [beam exp]
                              |
                    +---------+
                    |
               [HWP+PBS] --> dump
                    |
               [780 fiber] ----+
                               |
                               v
COUPLING ARM (480 nm)       [DICHROIC]
====================           |
                               v
  [ECDL-960]--->[SHG]--->[ISO]-->[HWP]--->[PBS]--->[480 fiber]--->[DICHROIC]
  (or ECDL-480 direct)                                                 |
                                                                       v
                                                             +-----------------+
                                                             |   Rb VAPOR CELL |
                                                             |   (50C-80C)     |
                                                             |                 |
                                                             |  probe -> ->    |
                                                             |  coupling <- <- |
                                                             |  (counter-prop) |
                                                             +-----------------+
                                                                      |
                                                             [780 bandpass filter]
                                                                      |
                                                                   [PD-EIT]
                                                                      |
                                                              [Red Pitaya ADC]
                                                              [lock-in, 1 Hz BW]

LOCKING ELECTRONICS
====================

  [PD-SAT] --> [Red Pitaya ch1] --> PID --> [probe ECDL piezo + TEC]
  [PD-EIT] --> [Red Pitaya ch2] --> lock-in demod --> [coupling ECDL piezo]

RF SOURCE
=========

  [HP/Agilent 8340B or equiv] --> [SMA cable] --> [antenna/horn]
                                                        |
                                              [positioned ~10cm from cell]
                                              [calibrated with known gain]
```

---

## BILL OF MATERIALS

Total estimated: **$4,340**

### 1. PROBE LASER — 780.24 nm (Rb D2 line) | Target: $650

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Laser diode 780nm, 100mW | Eagleyard / Roithner / Thorlabs | EYP-RWE-0780-04000-0750-SOT02-0000 or similar TO-3 package 780nm | $60 |
| Diffraction grating 1800 l/mm | Thorlabs GR25-1850 or Edmund Optics | Littrow angle ~36 deg at 780nm | $80 |
| Piezo actuator for grating | APC/PI PZT stack 5x5x2mm | 0-100V, 1 um travel | $25 |
| ECDL sled body (DIY machined Al) | Local machine shop or 3D-print in ABS+epoxy coat | Littrow geometry, grating on kinematic mount | $120 |
| Laser diode mount + TEC + thermistor | Thorlabs TCLDM9 or DIY Al block + TEC1-12706 | TEC: $8, thermistor: $3, mount Al: $15 | $80 |
| TEC controller PCB (JLCPCB) | JLCPCB fabrication | Based on MAX1978 or LT3080; gerbers from open-source repos (e.g., ecdl-controller by jbradshaw) | $45 |
| Collimating lens AR-coated | Thorlabs C230TMD-B or Geltech aspheric | f=4.5mm, 780nm AR | $55 |
| Optical isolator 780nm | Qioptiq/OFR IO-5-780-LP or eBay used | 40 dB isolation, free-space | $120 |
| Anamorphic prism pair | Thorlabs PS875-B | Beam circularization | $65 |
| SUBTOTAL | | | **$650** |

**ECDL design source:** Wieman & Hollberg (1991) Rev. Sci. Instrum. 62, 1 (canonical reference). Open-source sled CAD: nist-amo/ecdl-sled GitHub repo (Lett group NIST). Adams Durham group publishes full machining drawings for their teaching ECDL — contact their lab for drawings (email: ifs@durham.ac.uk). MIT AMO teaching lab 8.422 problem sets include ECDL design notes.

**Note on alternatives:** Semrock diode + JDSU WL-7301 grating mount can substitute. Sacher Lasertechnik sells bare Littrow sleds (without diode) for ~350 EUR — overpriced but plug-and-play.

---

### 2. COUPLING LASER — 480 nm | Target: $1,200

Two approaches; recommend Option B for reliability:

**Option A: Direct 480 nm ECDL**
| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| 480nm laser diode (Nichia NDB4216E or NDHB510APAE1) | Nichia via distributor | 480nm 30-50mW, TO-56 | $180 |
| Same sled/grating/piezo/mount as probe | (same BOM as above minus isolator) | 1200 l/mm grating for 480nm | $200 |
| Optical isolator 488nm | OFR IO-5-488-LP | May omit if well-isolated | $150 |
| SUBTOTAL Option A | | | **~$550** |

**Option B: 960 nm ECDL + frequency doubling (recommended)**
| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| 960nm laser diode (Eagleyard EYP-RWE-0960 or similar) | Eagleyard/eBay | 100mW, TO-3 | $80 |
| ECDL sled + grating for 960nm | Same as probe sled design | 1200 l/mm grating | $200 |
| SHG crystal PPKTP (10 mm) | Raicol Crystals or ADVR | Periodic poling, phase-matched at 960->480nm, 1mm aperture | $350 |
| SHG oven + TEC temperature controller | DIY brass block + TEC + PID | Crystal must stay within 0.1C of phase-match temp | $80 |
| Mode-matching lenses for SHG | Thorlabs LA1131/LA1027 | Two f~75mm lenses in bowtie or linear cavity | $50 |
| Dichroic to separate 480/960 | Thorlabs DMLP505 | Transmits 480nm, reflects 960nm | $85 |
| Optical isolator 960nm | OFR IO-5-980-LP (980nm works at 960nm) | Important before SHG | $100 |
| SUBTOTAL Option B | | | **$945** |

**Recommendation:** Option B is more reliable — 480nm diodes are fragile and expensive to replace. The SHG efficiency with PPKTP is ~10-30% (expect ~10 mW at 480nm from 100 mW pump), which is adequate for EIT coupling.

**Use $1,200 budget:** Option B ($945) + beam shaping for fiber coupling ($120) + contingency ($135).

---

### 3. RUBIDIUM VAPOR CELL | Target: $350

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Natural Rb vapor cell, 75mm length, 25mm dia | Triad RF Systems (triadrf.com) or Precision Glassblowing (precisionglassblowing.com) | Specify: no buffer gas, stem-off, natural Rb (72% Rb-85, 28% Rb-87 — adequate for 87 EIT) | $220 |
| Cell heater assembly (DIY) | Kapton heater tape + PID controller | Wrap cell body, avoid windows. Target 50-80 C for optimal OD=10-30 | $45 |
| TEC-based cell temperature controller PCB | JLCPCB | PID control of Kapton heater; thermistor on cell body. Stability <0.1 C required | $35 |
| Magnetic shielding for cell (see item 8) | — | See mu-metal section below | included |
| Oven/insulated mount (DIY PVC foam) | McMaster | Thermal isolation from optical table | $25 |
| Beam dump for cell transmission | Thorlabs BT610/M | After cell, before photodetector | $15 |
| SUBTOTAL | | | **$340** |

**Note on Rb-87 enriched cell:** Enriched cells (~90% Rb-87) give 3x stronger Rb-87 EIT signal but cost ~$600. For first build, natural abundance is sufficient.

---

### 4. OPTICAL LAYOUT — MOUNTS AND OPTOMECH | Target: $400

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Optical breadboard 600x450mm | Newport/Thorlabs used (eBay) or DIY granite tile | Granite floor tile (600x600x20mm from Home Depot) drilled on press: $40. Rubber vibration isolators: $20. Or used Newport SG-23-2 ~$100 | $80 |
| Post holders, posts, bases (x20) | Thorlabs or aliexpress clones | TR posts + BA2 bases; aliexpress laser optic mounts are adequate for this application | $80 |
| Half-wave plates 780nm (x3) | Thorlabs WPH05M-780 or aliexpress | Need 780nm and 480nm versions | $45 |
| Half-wave plates 480nm (x2) | Thorlabs WPH05M-488 | | $35 |
| Polarizing beam splitters (x4) | Thorlabs PBS251 or aliexpress PBS | 780nm and 480nm versions | $60 |
| Dichroic mirror 480/780 nm | Thorlabs DMLP505R | Combines probe + coupling into cell | $75 |
| 780nm bandpass filter (OD>5 at 480nm) | Thorlabs FBH780-10 | After cell, blocks coupling scatter | $65 |
| Plano-convex lenses (x6) | Thorlabs or surplus | Beam expansion, focusing into cell | $40 |
| Single-mode fiber + coupler 780nm | Thorlabs P1-780A-FC-2 | Route probe to cell area | $60 |
| SUBTOTAL | | | **$540** |

**Note:** Aliexpress optomech is adequate for posts, mounts, wave plates — just verify thread compatibility (M4 vs 8-32). Do NOT use aliexpress for the PBS or dichroic (poor extinction ratio). Budget slightly over at $540 but optomech can be trimmed.

---

### 5. SATURATED ABSORPTION SPECTROSCOPY REFERENCE | Target: $300

Second Rb cell for probe laser frequency reference (independent of main cell).

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Rb vapor cell (small, 50mm x 10mm dia) | Triad RF or Precision Glassblowing | Room-temperature operation fine for sat-abs | $120 |
| Beam splitter to pick off probe sample | Thorlabs BSW10R or similar | ~10% pick-off before main cell | $30 |
| Mirror for counter-propagating beam | Thorlabs BB1-E03 | Retroreflect probe through sat-abs cell | $25 |
| Photodetector for sat-abs signal | DIY: BPW34 + TL071 op-amp (see item 9) | $20 build vs $200 Thorlabs PDA36A | $20 |
| Red Pitaya ADC input (no extra cost) | Already in budget (item 7) | Processes sat-abs signal for PID | — |
| SUBTOTAL | | | **$195** |

**Note:** Sat-abs gives ~crossover resonance accuracy of ~5 MHz. This is adequate for EIT. For better probe lock, use modulation transfer spectroscopy (MTS) — same hardware, software phase-lock on Red Pitaya.

---

### 6. RF SOURCE | Target: $500

For Rydberg state n=50 in Rb-87: the transition 50D5/2 -> 51P3/2 is near 13.92 GHz. For sensing 1-100 GHz RF, choose n to match: n=30 covers ~100 GHz, n=60 covers ~3 GHz.

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| HP/Agilent 8340B or E4433B signal generator | eBay | HP 8340B: DC-26.5 GHz, typically $300-600 on eBay. Verify calibration. | $450 |
| SMA cables (x3, 1m each) | Pasternack or eBay | Low-loss 18 GHz rated | $30 |
| Standard gain horn antenna (10-18 GHz) | A-INFO LB-180400-SF or similar eBay | Gain ~15 dBi, 10-18 GHz band | $80 |
| SUBTOTAL | | | **$560** |

**Alternative RF sources:**
- LMX2595 PLL eval board ($100, covers 10 MHz to 20 GHz) — adequate for fixed-frequency calibration measurements
- HackRF One + amplifier: covers 1 MHz to 6 GHz at $300 total — useful for lower-n Rydberg states
- For <1 GHz RF sensing: use n>60 states, cheaper AWG sources

---

### 7. LOCK-IN DETECTION — RED PITAYA | Target: $350

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Red Pitaya STEMlab 125-14 | Red Pitaya (redpitaya.com) | 14-bit, 125 MSa/s dual ADC/DAC. Use PyRPL (open-source lock-in/PID software) | $320 |
| SMA breakout + adapter kit | Pasternack/Amazon | SMA-BNC adapters for photodetector cables | $25 |
| SUBTOTAL | | | **$345** |

**PyRPL:** Python Red Pitaya Lock-in (github.com/lneuhaus/pyrpl). Provides: lock-in amplifier, PID controllers, VNA, spectrum analyzer. Used in academic labs worldwide for exact this application. Tutorial: Neuhaus et al., SoftwareX (2017).

**Lock-in modulation scheme:** Frequency-modulate the probe laser at 10-100 kHz using the ECDL piezo (driven by Red Pitaya DAC). Detect modulation signal on the EIT transmission photodetector (PD-EIT). Demodulate at 1 Hz bandwidth to get dispersive EIT lineshape signal. Use this to lock coupling laser (or probe laser) to EIT peak. AT splitting appears as differential signal when RF is applied.

---

### 8. MAGNETIC SHIELDING (MU-METAL) | Target: $200

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| Mu-metal sheet 0.5mm thick, 300x600mm | MuMETAL / Magnetic Shield Corp / eBay | Part# ZH070 0.5mm sheet. Order 2 sheets. | $120 |
| Tin snips + rivets for box construction | Hardware store | DIY 150x80x80mm box around vapor cell area | $20 |
| Annealing (critical): local machine shop | — | Mu-metal MUST be annealed after cutting/bending to restore permeability. 1100 C, 1 hr, H2 atmosphere. OR buy pre-formed cylinder | $0 if DIY oven |
| Alternative: pre-formed mu-metal cylinder | Magnetic Shield Corp or eBay surplus | 4-inch dia, 8-inch long cylinder: $80-150 | $120 |
| SUBTOTAL | | | **$180** |

**IMPORTANT:** DIY mu-metal shielding requires annealing after forming. Without annealing, permeability drops 10-100x after cutting/bending. Options: (1) buy pre-annealed cylinder and avoid cutting, (2) use vacuum oven at local university, (3) use 3-layer approach with outer permalloy + inner mu-metal. For first build, a pre-formed cylinder ($120 eBay surplus) is strongly recommended over DIY flat sheet bending.

**Shielding factor requirement:** Residual magnetic field inside cell must be <10 mG (1 uT) to avoid Zeeman broadening killing the EIT. Three-axis Helmholtz coils inside the shield can cancel residual fields — add 3x air-core coil sets ($30 wire cost).

---

### 9. DIY PHOTODETECTORS (x2) | Target: $40

For EIT signal and sat-abs reference. DIY cost vs Thorlabs PDA36A ($250 each).

**Circuit (per detector):**
- BPW34 Si photodiode: $0.50 (Digikey 751-1017-ND)
- TL071 op-amp (transimpedance config): $0.30
- OPA657 or OPA847 for higher bandwidth (>10 MHz): $5 each
- 10 MOhm feedback resistor, 10 pF cap (transimpedance config)
- PCB via JLCPCB: $5 for 5 boards

**Performance:** BPW34 + TL071 at gain 1e7 V/A: noise floor ~1 pA/sqrt(Hz), bandwidth ~2 kHz. Adequate for sat-abs lock (slow signal). For EIT lock-in at 100 kHz modulation, use OPA657 at gain 1e5 V/A, bandwidth ~100 kHz.

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| BPW34 photodiodes (x5) | Digikey | | $3 |
| OPA657 op-amps (x4) | Digikey | High-speed transimpedance | $20 |
| PCB fabrication JLCPCB (2 designs) | JLCPCB | 5-board minimum, $5 each | $10 |
| Passives, connectors | Digikey | | $10 |
| SUBTOTAL | | | **$43** |

---

### 10. LASER CONTROLLERS (JLCPCB) | Target: $200

| Item | Vendor | Part / Notes | Est. Price |
|------|--------|--------------|-----------|
| TEC controller boards (x2) | JLCPCB | Based on MAX1978 reference design. Open-source layout: github.com/jbradshaw/ecdl-controller | $40 |
| Current driver boards for diodes (x2) | JLCPCB | LT3080 linear reg + noise filter. <1 uA RMS noise critical. See nist-amo/diode-driver | $40 |
| High-voltage amplifier for piezo (x2) | JLCPCB or DIY | PA98 or OPA445 0-100V piezo driver. Drives ECDL grating piezo from Red Pitaya 0-1V | $60 |
| Enclosures + power supplies | Amazon/Mouser | Linear regulated PSU (not switching — minimizes noise): 24V/2A LT PSU $30 | $60 |
| SUBTOTAL | | | **$200** |

**Noise requirement for current driver:** Laser RIN (relative intensity noise) at 100 kHz must be below -130 dBc/Hz. Switching regulators inject at 50-500 kHz — always use linear regulators for diode current drive. LT3080 with 10 uF output cap achieves this easily.

---

### BUDGET SUMMARY

| Section | Target | Estimate |
|---------|--------|---------|
| 1. Probe laser 780nm ECDL | $650 | $650 |
| 2. Coupling laser 480nm (Option B SHG) | $1,200 | $945 |
| 3. Rb vapor cell + heater | $350 | $340 |
| 4. Optomech + breadboard | $400 | $540 |
| 5. Sat-abs reference | $300 | $195 |
| 6. RF source (eBay HP 8340B) | $500 | $560 |
| 7. Red Pitaya lock-in | $350 | $345 |
| 8. Mu-metal shielding | $200 | $180 |
| 9. DIY photodetectors | $40 | $43 |
| 10. Laser controllers (JLCPCB) | $200 | $200 |
| **Contingency (10%)** | $430 | $342 |
| **TOTAL** | **$4,620** | **$4,340** |

Under the $5,000 target by $660. Optomech ($540) is the one line over budget — trim by sourcing more from eBay/aliexpress ($350 achievable, saving $190).

---

## FIRST-LIGHT PROTOCOL

### Phase 0: Laser checkout (parallel to cell/RF setup)
1. Power up probe ECDL, verify single-mode output on grating spectrometer (or via Fabry-Perot etalon)
2. Tune to 780 nm Rb D2 line using fluorescence in reference Rb cell (observe orange glow at room temperature)
3. Implement sat-abs lock: send probe through reference cell, observe crossover resonances on oscilloscope
4. Lock probe to F=2->F'=3 crossover using Red Pitaya PID

### Phase 1: Saturated Absorption (Week 5-6)
**Go/No-Go criterion:** Resolve all 6 Rb-87 D2 crossover resonances with FWHM <20 MHz

Steps:
1. Set up counter-propagating probe beams through sat-abs cell
2. Scan ECDL piezo at ~10 Hz over 500 MHz range
3. Observe Doppler-free dips on oscilloscope (PD-SAT)
4. Identify F=2->F'=3 transition (strongest absorption on Rb-87)
5. Engage PID lock: residual frequency noise <100 kHz RMS

### Phase 2: EIT Observation (Week 7-8)
**Go/No-Go criterion:** Observe EIT transmission peak > 3% above background

Steps:
1. Align coupling laser (480 nm) counter-propagating through main Rb cell (probe and coupling must be co-propagating in the cell — both enter same window, exit same window, counter-propagating relative to each other reduces Doppler)
2. Heat cell to 60 C (OD ~5-10 on D2 line), verify with probe transmission
3. Scan coupling laser over 5-state bandwidth with probe locked
4. Look for transparency peak at two-photon resonance on PD-EIT
5. Narrow coupling scan to 100 MHz around EIT peak
6. Lock coupling laser to EIT peak via Red Pitaya lock-in

### Phase 3: Autler-Townes Splitting (Week 9-12)
**Go/No-Go criterion:** Observe resolved AT doublet with known horn power

Steps:
1. Position horn antenna 10 cm from vapor cell (line-of-sight, no metal obstructions)
2. Apply RF at 13.92 GHz (50D5/2 -> 51P3/2 transition), +10 dBm output from HP 8340B
3. Predicted Rabi splitting at 1 m distance from 15 dBi horn at +10 dBm: E~1 V/m, splitting ~450 kHz
4. Scan coupling laser over +/-2 MHz; observe doublet peak splitting
5. Vary RF power; verify linear AT splitting vs E_rf (Omega_AT = d*E/hbar)
6. This is first-light RF detection: ~1 uV/m/sqrt(Hz) sensitivity at this stage

### Phase 4: Calibration and Sensitivity (Week 13-16)
**Go/No-Go criterion:** Measured sensitivity <=300 nV/m/sqrt(Hz)

Steps:
1. Calibrate antenna gain (measure with second calibrated detector or use certified NIST value)
2. Measure AT splitting as function of E_rf with known field
3. Construct V/m calibration curve: Omega_AT (Hz) = (d_n/h) * E_rf (V/m)
   - For n=50, d_n ~ 6340 Debye = 2.12e-26 C.m
   - 1 V/m gives splitting ~ 32 MHz (direct frequency measurement)
4. Reduce modulation bandwidth to 0.1 Hz (10 s integration)
5. Measure noise floor: expected ~300 nV/m/sqrt(Hz) with PDH-locked probe
6. Record "calibration curve" dataset: AT splitting (MHz) vs applied E (V/m)

---

## SENSITIVITY ANALYSIS

**Physical parameters:**
- Rydberg state: n=50, 50D5/2
- Transition dipole moment d_50 ~ 6,340 Debye = 2.12e-26 C.m
- AT splitting at 1 uV/m: Omega_AT/2pi = 31.9 Hz
- EIT linewidth (DIY, no sub-Doppler): ~100 kHz
- EIT linewidth (PDH-locked coupling): ~10 kHz

**Noise sources (ranked):**
1. **Laser frequency noise (dominant at first light):** Free-running ECDL at ~1 MHz linewidth converts to ~31 mV/m equivalent noise. After sat-abs lock (100 kHz): ~3 uV/m. After PDH lock (10 kHz): ~0.3 uV/m. First-light target assumes sat-abs lock only.
2. **Photon shot noise:** At 1e6 photons/s detected, shot noise = 1e-3 (relative). With 100 kHz EIT linewidth: delta_E_shot ~ 3 uV/m. Improves as sqrt(N) with better photon collection.
3. **Vapor cell temperature noise:** 0.1 C stability achievable with PID. At 60 C, dN_Rb/dT ~ 10%/C, so 0.1C -> 1% density noise -> 0.5% EIT amplitude noise -> ~1 uV/m equivalent.
4. **Magnetic field noise:** Unshielded lab fields ~100 mG at 50/60 Hz. Mu-metal shielding reduces to <1 mG. Zeeman shift ~1.4 MHz/G, so 1 mG -> 1.4 kHz frequency noise -> 0.045 uV/m equivalent.
5. **RF source phase noise (HP 8340B):** -80 dBc/Hz at 10 kHz offset. Acceptable for calibration measurements but limits ultimate sensitivity.

**Sensitivity milestones:**
| Stage | Sensitivity | Limiting factor |
|-------|-------------|-----------------|
| First light (week 9) | ~5-10 uV/m/sqrt(Hz) | Probe freq noise, no PDH |
| After sat-abs lock (week 10) | ~1-3 uV/m/sqrt(Hz) | Residual freq noise |
| After PDH coupling lock (week 12) | ~300-500 nV/m/sqrt(Hz) | Shot noise + temperature |
| Optimized (better cell, 77K shield) | ~50-100 nV/m/sqrt(Hz) | Shot noise |
| NIST Holloway research record | 55 nV/m/sqrt(Hz) | Near quantum limit |

---

## RISK REGISTER

### Risk 1: Coupling laser (480 nm SHG) fails to produce adequate power [HIGH]
**Probability:** 40% | **Impact:** High (blocks EIT observation)
**Symptoms:** <3 mW at 480 nm, no visible EIT peak
**Mitigations:**
- Buy PPKTP crystal from reputable vendor (Raicol, not aliexpress)
- Crystal temperature control to 0.05 C reduces phase-mismatch risk
- Fallback: Direct 480 nm diode (Nichia NDB4216E) — lower reliability but no SHG needed
- Second fallback: Use 852 nm probe + 509 nm coupling for Cs (cesium cell ~same cost)

### Risk 2: Probe laser mode-hops prevent stable sat-abs lock [HIGH]
**Probability:** 35% | **Impact:** High (no frequency reference)
**Symptoms:** Multiple mode jumps during piezo scan, irreproducible sat-abs spectrum
**Mitigations:**
- Keep ECDL cavity temperature stable to 0.01 C (TEC controller quality matters)
- Anti-reflection coated diode (specify AR-coated when ordering) reduces feedback
- If persistent: add etalon inside cavity (Fabry-Perot thin glass plate at Brewster angle)
- Thorlabs LDC202C current driver eliminates current noise as mode-hop driver ($200 upgrade)

### Risk 3: EIT linewidth too broad to resolve AT splitting at target sensitivity [MEDIUM]
**Probability:** 25% | **Impact:** Medium (degrades sensitivity 3-10x)
**Symptoms:** EIT FWHM >500 kHz, AT doublet unresolved at E<10 uV/m
**Mitigations:**
- Velocity-selective excitation: choose counter-propagating probe/coupling (most common); co-propagating gives Doppler-free but narrower bandwidth
- Reduce cell temperature (lower OD -> narrower EIT, but weaker signal); optimize at 50-55 C
- Use higher-n Rydberg state (n=60 or 70): larger dipole moment, larger AT splitting, easier to resolve

### Risk 4: 60 Hz magnetic field noise overwhelms EIT signal despite shielding [MEDIUM]
**Probability:** 30% | **Impact:** Medium (floor at ~1 uV/m)
**Symptoms:** 60 Hz sideband in sensitivity spectrum, floor doesn't improve with integration time
**Mitigations:**
- Three-layer shielding: outer permalloy (cheap, ~$50 from eBay speaker magnets' return path material), inner mu-metal, inner Helmholtz coils
- Active field cancellation: fluxgate magnetometer + Helmholtz coil PID (adds ~$200)
- Modulate RF probe signal above 100 Hz to move measurement away from 60 Hz noise

### Risk 5: RF calibration uncertainty limits SI traceability [LOW-MEDIUM]
**Probability:** 50% | **Impact:** Low (absolute calibration off, relative measurements still valid)
**Symptoms:** Measured AT splitting disagrees with predicted AT splitting for known input power
**Mitigations:**
- Use horn antenna with certified gain and known cable loss
- At-cell field strength: E = sqrt(2*Z0*P_delivered) * G_horn^(1/2) / (4*pi*r) — calculate rigorously
- Cross-check with two antenna distances (1/r^2 dependence confirms far-field calibration)
- For SI-traceable absolute calibration: send cell to NIST for cross-calibration at one field strength (low-cost outreach program, ~$0 for academic collaborations)

---

## 16-WEEK BUILD TIMELINE

### Weeks 1-4: Laser Assembly
- Week 1: Order all parts. Machine/3D-print ECDL sled bodies (or source from machine shop). Fabricate JLCPCB boards (TEC controller, current driver, PZT amp).
- Week 2: Assemble probe ECDL (780 nm). Test diode emission on spectrometer. Verify collimation, beam quality.
- Week 3: Assemble coupling ECDL (960 nm) and SHG crystal assembly. Optimize phase-matching temperature for 480 nm output. Target: >3 mW at 480 nm.
- Week 4: Test both lasers for mode-hop-free tuning range. Probe: 1+ GHz mode-hop-free scan required. Couple both into optical fibers.

### Weeks 5-6: Saturated Absorption Lock
- Week 5: Build sat-abs reference setup with secondary Rb cell. Observe Doppler-free hyperfine spectrum on oscilloscope.
- Week 6: Implement Red Pitaya PID lock for probe laser. Target: lock holds for >30 minutes. Verify frequency stability with beat note or wavemeter if available.
- **Milestone:** Probe locked to F=2->F'=3 crossover, <100 kHz residual noise.

### Weeks 7-8: Vapor Cell EIT
- Week 7: Set up main Rb cell at 55 C. Align probe through cell, observe strong absorption. Add coupling beam counter-propagating through cell.
- Week 8: Scan coupling laser; observe EIT transparency peak. Measure EIT linewidth. Lock coupling laser to EIT resonance using Red Pitaya lock-in.
- **Milestone (Go/No-Go):** EIT transmission peak >3%, linewidth <200 kHz, stable lock.

### Weeks 9-12: RF Detection and AT Splitting
- Week 9: Position horn antenna 10 cm from cell. Apply +10 dBm at 13.92 GHz. Observe AT doublet splitting in EIT spectrum.
- Week 10: Characterize AT splitting vs RF power. Verify linear relationship: Omega_AT proportional to E_field.
- Week 11: Implement full lock-in detection chain: modulate probe at 50 kHz, demodulate EIT signal at 1 Hz bandwidth. This gives dispersive sensitivity to E-field.
- Week 12: Move antenna to 50 cm, 1 m, 2 m. Verify 1/r field dependence. First sensitivity estimate.
- **Milestone:** Resolved AT splitting at E < 1 mV/m. Sensitivity estimate < 5 uV/m/sqrt(Hz).

### Weeks 13-16: Calibration and First Publishable Measurement
- Week 13: Rigorous calibration curve: AT splitting (Hz) vs E_rf (V/m) over 1 uV/m to 1 V/m range.
- Week 14: Sensitivity optimization — PDH lock on coupling laser if needed, optimize cell temperature, reduce bandwidth.
- Week 15: Measure sensitivity floor. Identify dominant noise source from noise spectrum shape (white = shot noise, 1/f = laser noise, peak at 60 Hz = magnetic).
- Week 16: First publishable dataset — V/m calibration curve + sensitivity spectrum + comparison with NIST Holloway teaching build benchmark.
- **Final milestone:** Sensitivity <=300 nV/m/sqrt(Hz). SI-calibrated E-field measurement. Reproducible RF detection at 10 GHz.

---

## VENDOR QUICK-REFERENCE

| Vendor | Use Case | URL |
|--------|----------|-----|
| Triad RF Systems | Rb vapor cell | triadrf.com |
| Precision Glassblowing | Rb/Cs cells | precisionglassblowing.com |
| JLCPCB | PCB fabrication | jlcpcb.com |
| Red Pitaya | Lock-in / PID / ADC | redpitaya.com |
| Raicol Crystals | PPKTP SHG crystal | raicol.com |
| eBay search: "HP 8340B" | RF signal generator | ebay.com/sch/i.html?_nkw=HP+8340B |
| eBay search: "mu-metal sheet" | Magnetic shielding | ebay.com/sch/i.html?_nkw=mu+metal+sheet |
| Thorlabs | Optics, mounts, isolators | thorlabs.com |
| Eagleyard Photonics | Laser diodes | eagleyard.com |
| Digikey | Electronics components | digikey.com |
| McMaster-Carr | Hardware, mounts | mcmaster.com |
| A-INFO | Horn antennas | ainfoinc.com |

---

## KEY REFERENCES

1. Holloway et al. (2014), "Broadband Rydberg Atom-Based Electric-Field Probe for SI-Traceable, Self-Calibrated Measurements." IEEE Trans. Antennas Propag. 62, 6169; arXiv:1405.7066. **The canonical NIST broadband probe paper.** (Corrected 2026-06-27 from prior citation "J. Appl. Phys. 116, 244101" per DEEPRESEARCH-rydberg-rf-2026-05-18.md §9.1.)

1a. Sibalic et al. (2017), "ARC: An open-source library for calculating properties of alkali Rydberg atoms." Comput. Phys. Commun. 220, 319. **Primary source for the n=50 dipole-moment number ~6340 Debye used in this BoM.**

2. Shaffer et al. (2018), "A read-out enhancement for microwave electric field sensing with Rydberg atoms." New J. Phys. 20, 073011.

3. Wieman & Hollberg (1991), "Using diode lasers for atomic physics." Rev. Sci. Instrum. 62, 1. **The canonical ECDL DIY reference.**

4. MacAdam et al. (1992), "A narrow-band tunable diode laser system with grating feedback and a saturated absorption spectrometer for Cs and Rb." Am. J. Phys. 60, 1098. **Teaching lab ECDL design.**

5. Neuhaus et al. (2017), "PyRPL (Python Red Pitaya Lockbox) — An open-source software package for FPGA-controlled quantum optics experiments." SoftwareX 6, 206-216. **Red Pitaya lock-in software.**

6. Adams group Durham (2020+), Rydberg EIT teaching lab notes. Available from Durham Quantum Light and Matter group on request.

7. Bhatt et al. (2023), "Low-cost Rydberg electrometer using commercial off-the-shelf components." Phys. Rev. Applied (in press 2023). Demonstrates Red Pitaya + 780/480 nm two-photon scheme.

---

*Generated: 2026-04-26 | Build-A engineer: computation-lead | Task #2*
*Blocks: Task #3 (Build B: tweezer array bridge), Task #5 (Synthesis)*
