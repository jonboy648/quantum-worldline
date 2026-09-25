# Deep Research — Rydberg Atoms, k-Factor, and RF Sensing (2026-05-18)

**Status:** synthesized from 8 parallel scouts + adversarial verification. All numerical claims here use the verifier-corrected values, not the scout's originals where they disagreed. Citation corrections noted inline.

## TL;DR

A Rydberg atom is an alkali atom (Rb-87, Cs) excited to a very high principal quantum number n ~ 30-100, where every observable that matters - radius, dipole moment, polarizability, lifetime, van der Waals C6 - blows up by a fixed power of n. "k-factor" is overloaded in this field, but in the operational language of Rydberg RF electrometry it almost always means the Autler-Townes calibration coefficient k_AT = mu_RF / h, the SI-traceable conversion from a measured Autler-Townes splitting (Hz) to an applied RF field (V/m); for typical alkali nS->nP or nD->(n+1)P transitions at n ~ 40-60 this lands at roughly 20-30 MHz per (V/m). Rydberg atoms are extraordinary RF sensors because that calibration is anchored only on Planck's constant and an atomic matrix element (no antenna gain, no power meter), they cover roughly d.c. to ~THz with one vapor cell, and the sensor head is sub-wavelength and metal-free. Where they win: SI-traceable self-calibration, broadband one-head tunability, sub-wavelength field mapping, and immunity to in-band damage. Where they lose: the 2024 Backes/Meyer/Kunz/Cox head-to-head in APL 125, 144002 shows real room-temperature Rydberg cells are LESS sensitive than equivalently-sized active LNA+antenna front-ends at GHz; best peer-reviewed sensitivity is ~10 nV/cm/sqrt(Hz) in a laser-cooled-atom apparatus (Tu et al., Sci. Adv. 2024), and ~55 nV/cm/sqrt(Hz) in a vapor-cell superheterodyne (Jing et al., Nat. Phys. 2020) - both still beaten by a matched cm-scale dipole + LNA on raw SNR per Hz.

---

## 1. What is a Rydberg atom (physics fundamentals)

A Rydberg state is an alkali atom (most commonly Rb-87 or Cs) with one valence electron promoted to a large principal quantum number n, typically 30-100. The electron orbits far from a hydrogenic ionic core, so every observable scales as a fixed power of the effective quantum number n* = n - delta_{nlj}, where delta is the quantum defect (encoding short-range core penetration). For Rb-87: delta_S = 3.131180(10), delta_{P1/2} = 2.6549, delta_{P3/2} = 2.6417, delta_{D3/2} = 1.3481, delta_{D5/2} = 1.34646572(30), delta_F ~ 0.0165 (Mack 2011; Li/Mourachko/Noel 2003).

Level energies: E_{nlj} = -hc R_inf / (n - delta)^2, with R_inf = 10 973 731.568 157(12) m^-1 (CODATA 2022; relative uncertainty 1.1x10^-12 - the most precisely known constant in physics).

### 1.1 ASCII level / excitation diagram (Rb-87 two-photon EIT ladder)

```
   |r>  = nS_{1/2} or nD_{5/2}   <-- Rydberg target, lifetime ~100 us at 300 K
                ^
                | coupling laser ~480 nm, ~100-500 mW, Omega_c/2pi ~ MHz
                |
   |e>  = 5P_{3/2}                 (intermediate, Gamma/2pi = 6.07 MHz)
                ^
                | probe laser 780.241 nm, weak, Omega_p/2pi << Gamma
                |
   |g>  = 5S_{1/2}                 (ground)
```

For Cs the analog ladder is 6S_{1/2} -> 6P_{3/2} (852 nm) -> nS or nD (~509-511 nm coupling). The 509 nm step is cheaper to produce than Rb's 480 nm, which is one of the few real reasons to pick Cs.

### 1.2 The n-scaling cheat sheet

| Quantity | Scaling | Order-of-magnitude (Rb-87, n ~ 70) | Source |
|---|---|---|---|
| Mean orbital radius `<r>` | (3/2) n*^2 a_0 | ~ 7400 a_0 ~ 390 nm | Gallagher 1994 §2.3 |
| Binding energy E_n | -hc R_inf / n*^2 = -13.6 eV / n*^2 | ~ 3 meV at n=70 | Gallagher 1994 §1.2 |
| Adjacent level spacing Delta E | 2 hc R_inf / n*^3 | ~ 14 GHz (Delta n = 1 at n ~ 70 nD-(n+1)P) | Gallagher 1994 §1 |
| Radial dipole matrix element | ~ n*^2 e a_0 | ~ 5000 e a_0 ~ 4x10^-26 C.m | SWM RMP 2010 §II |
| Scalar DC polarizability alpha_0 | propto n*^7 | ~ 290 MHz/(V/cm)^2 (Rb 70S) | Gallagher 1994 §5; Sibalic-Adams 2018 |
| Radiative lifetime tau_rad (low-l, 0 K) | propto n*^3 | ~ 300 us | Beterov PRA 79, 052504 (2009) |
| BBR-induced rate Gamma_BBR (300 K) | propto n*^-2 | dominates over spontaneous at n >~ 30 | Beterov 2009 |
| Effective lifetime tau_eff (300 K) | (1/tau_rad + 1/tau_BBR)^-1 | ~ 100-140 us (70S, 70D) | Beterov 2009 |
| Circular state lifetime | propto n^5 (single decay channel) | ~ ms class (cold, vacuum) | Gallagher 1994 Ch.4 |
| van der Waals C_6 (like-Rydberg pairs) | propto n*^11 | C_6(Rb 70S_{1/2}) ~ 880 GHz.um^6 | ARC (Sibalic 2017); Walker-Saffman PRA 77, 032723 (2008) |
| Blockade radius (Omega/2pi = 1 MHz) | (C_6 / hbar Omega)^(1/6) | ~ 9.8 um at n=70 | Browaeys/Lahaye Nat. Phys. 16, 132 (2020) |
| Inglis-Teller field (l-mixing) | E_IT = 1/(3 n^5) a.u. = 1.71x10^9 / n^5 V/cm | ~ 1 V/cm at n=70 | Gallagher 1994 §6.2 |
| Field-ionization threshold | E_ion ~ 1/(16 n^4) a.u. ~ 3.2x10^8 / n^4 V/cm | ~ V/cm class at n=70 | Gallagher 1994 Ch.6 |

**Verifier corrections folded in (from `fundamentals` scout):** the original report gave C_6(70S) ~ 880 **THz.um^6** (off by 1000x in unit), E_IT ~ 3.2x10^8 / n^5 V/cm (off by ~5x; correct prefactor is 1.71x10^9), and alpha_0(50S) ~ 79 MHz/(V/cm)^2 (closer to 60S; 50S is actually ~27). The corrected values above are what should be used in any BUILD-A or HYP-018/019 budget.

### 1.3 Two-photon excitation, in practice

The workhorse Rb-87 Rydberg preparation is the ladder probe (5S_{1/2} -> 5P_{3/2}, 780 nm) + coupling (5P_{3/2} -> nS or nD, 480 nm) with the intermediate detuned by Delta/2pi ~ 0.5-1 GHz from 5P resonance. Effective two-photon Rabi Omega_eff = Omega_1 Omega_2 / (2 Delta) ~ 1-10 MHz at typical mW probe and 100-500 mW coupling intensities. Direct one-photon UV at ~297 nm exists (5S -> nP, asymptoting to the 297.108 nm series limit) but is rarely used because of UV laser cost and short component lifetime.

---

## 2. The "k-factor" - disambiguated

"k-factor" is overloaded. Each plausible meaning:

1. **n-scaling exponent k in `property ~ n^k`** - the tutorial sense (n^2, n^3, n^7, n^11). Explains *why* mu_RF is enormous but is not what gets read off the spectrum.
2. **Rydberg constant R_inf** = 10 973 731.568 157(12) m^-1 (CODATA 2022; arXiv:2409.03787). Sets level energies; never used as a calibration coefficient in RF sensing.
3. **Photon wavenumber k = 2pi/lambda** of the RF wave being detected. At 10 GHz, k ~ 209 m^-1. Relevant to sub-wavelength imaging, not the readout coefficient.
4. **Autler-Townes calibration coefficient k_AT = mu_RF / h** (Hz per V/m). This is THE coefficient that makes Rydberg electrometry SI-traceable.
5. **DC Stark coefficient (1/2) alpha_0** - quadratic regime, alpha_0 propto n^7. Used for stray-field characterization, not AC RF sensing.
6. **Polarizability alpha (the "K-coefficient" in atomic-clock language)** - both scalar alpha_0 and tensor alpha_2 propto n^7. Sets Stark shifts of clock transitions; in RF sensing it's the *unwanted* shift that limits low-frequency operation.
7. **Boltzmann constant k_B** = 1.380649e-23 J/K. Enters only via BBR rates; not a sensing coefficient.

### Numerical value of k_AT

For a typical alkali Rydberg microwave transition (nD_{5/2} -> (n+1)P_{3/2} or nS -> nP near n = 40-60) the radial dipole matrix element is ~ 700-2500 e a_0. Working example: mu ~ 2000 e a_0 = 2000 x 1.602e-19 C x 5.29e-11 m = 1.695e-26 C.m, so

  k_AT = mu / h = 1.695e-26 / 6.626e-34 ~ 2.56x10^7 Hz / (V/m) ~ 25.6 MHz per (V/m).

Better stated as a band: **k_AT ~ 20-30 MHz per (V/m)** for typical nS->nP / nD->(n+1)P transitions at n = 40-60, with the exact value pinned by ARC for the chosen (n, l, j, m_j) and RF polarization. Sedlacek's Cs 53D_{5/2}->54P_{3/2} at 14.231 GHz sits near the top end (~27 MHz/(V/m)).

### Verdict

In Rydberg RF electrometry, "the k-factor" = **k_AT = mu_RF / h**, the conversion that links the measured AT splitting in the probe transmission spectrum to an absolute SI-traceable RF E-field strength via only Planck's constant and an ab-initio atomic dipole. Every other "k" on the list is either a scaling exponent (n^k) or a different physical quantity entirely.

---

## 3. How they detect radio signals - EIT + Autler-Townes

The mechanism is a four-level dressed-atom interference effect read out in probe-laser transmission.

### 3.1 Three-level EIT (no RF)

```
   |r>  nD_{5/2}    -------- coupling Omega_c, ~480 nm (Rb)
                 ^
                 |
   |e>  5P_{3/2}   -------- probe Omega_p, 780 nm  (transmission measured)
                 ^
                 |
   |g>  5S_{1/2}   --------
```

A weak probe on `|g> -> |e>` is normally absorbed (Doppler-broadened ~500 MHz at 300 K). Adding a strong coupling laser on `|e> -> |r>` opens a destructive-interference transparency window in the probe absorption: linewidth Gamma_EIT ~ Omega_c^2 / Gamma_e plus residual two-photon Doppler (k_p - k_c)·v_rms (~3 MHz for 780+480 nm) plus transit-time broadening (~100 kHz - MHz) plus laser linewidth. Net Gamma_EIT in warm cells is typically 1-10 MHz; in cold atoms it can be sub-MHz.

### 3.2 Four-level EIT-AT (RF turned on)

Add a fourth Rydberg level `|r'>` coupled to `|r>` by an RF field resonant with the Rydberg-Rydberg transition mu_RF. The single narrow EIT peak splits into a symmetric Autler-Townes doublet:

  **Delta omega_AT = mu_RF · E_RF / hbar     <=>     Delta f_AT [Hz] = mu_RF [C.m] · E_RF [V/m] / h**

Measuring the doublet separation in the probe transmission directly gives E_RF in V/m, with NO RF power meter, antenna gain, or impedance reference in the calibration chain.

Worked example (verifier-corrected): Cs **53D_{5/2} -> 54P_{3/2}** near **14.231 GHz**, mu ~ 723 e a_0 ~ 6.13x10^-27 C.m. For E_RF = 1 V/m, Delta f_AT ~ (6.13x10^-27)(1) / 6.626x10^-34 ~ **9.3 MHz** - comfortably resolvable above Gamma_EIT ~ 3-6 MHz. The original scout reported this number against a (60D, 13.4 GHz, 723 e a_0) triple that does not exist - 60D->61P sits near 9.67 GHz with mu ~ 2288 e a_0 (Delta f_AT ~ 29 MHz/(V/m)). Citation: Holloway et al., IEEE TAP 62, 6169 (2014), arXiv:1405.7066; Sedlacek et al., Nat. Phys. 8, 819 (2012).

### 3.3 SI-traceability - what it actually means

Calibration depends only on (i) Planck's constant h (defined exactly in the 2019 SI), (ii) the dipole matrix element mu_RF computed from quantum defect theory (cross-checked between Cs and Rb to ~5%, dominated by AC-Stark and dielectric-cell systematics; Holloway/Simons 2016, arXiv:1607.01766), and (iii) a frequency measurement of Delta f_AT. No RF power meter or antenna gain enters. This is why NIST calls the AT-regime probe a *primary* standard for E-field strength.

**Honestly stated:** SI-traceability is real, but only in the AT-splitting regime (~ 100 MHz to ~ 500 GHz canonical; ~ 1-40 GHz workhorse band). Outside that regime - heterodyne, off-resonant Stark, THz upconversion - the technique is highly sensitive but NOT a primary standard, and calibration is referenced back to AT measurements or to classical horns. The dipole-moment ab initio uncertainty is sub-1%; the overall measurement uncertainty (including dielectric-cell perturbation, AC-Stark from probe/coupling, collisional shifts) sits closer to 5-10% in the 2024 Schlossberger/Holloway review (Nat. Rev. Phys. 6, 606).

### 3.4 Pushing below the AT-only limit - heterodyne

The pure AT-splitting method requires resolving Delta f_AT > ~ 0.1 Gamma_EIT, which floors detectable E_RF around 10s of uV/cm at typical vapor-cell parameters (Sedlacek 2012: 30 uV/cm/sqrt(Hz), min detectable ~8 uV/cm).

**Superheterodyne (Jing et al., Nat. Phys. 16, 911 (2020)):** lock a strong on-resonance LO RF field that maintains the AT-split EIT spectrum; inject a weak signal field detuned by delta from the LO; the LO+signal beat inside the Rydberg medium modulates probe transmission at frequency delta. Lock-in readout at delta exploits the steep linear slope of the AT shoulder and beats down 1/f and laser noise. Reported sensitivity **55 nV/cm/sqrt(Hz)**, min detectable E ~ 780 pV/cm - about 3 orders of magnitude beyond AT-only.

**Off-resonant operation** when the carrier doesn't sit on a Rydberg-Rydberg line: (a) DC-Stark tuning into resonance (Anderson/Raithel, arXiv:2106.01968); (b) adjacent-resonance dressing with a strong LO (Berweger/Holloway 2021, arXiv:2105.10561); (c) AC-Stark / Floquet engineering (Hu et al. APL 121, 014002 (2022); Borowka et al. APL 125, 194001 (2024) = arXiv:2407.05676). The NIST mixer variant achieves <1 Hz spectral resolution (Simons et al., AIP Advances 9, 045030 (2019); Gordon et al. NIST 2024).

---

## 4. How sensitive are they really

### 4.1 Headline numbers (verifier-corrected)

| Year | Group | Scheme | Best E-field sensitivity | Min detectable E | Notes |
|---|---|---|---|---|---|
| 2012 | Sedlacek/Shaffer (Stuttgart/Oklahoma) | Vapor-cell CW EIT-AT, Rb 53D | **~30 uV/cm/sqrt(Hz)** | ~8 uV/cm | Nat. Phys. 8, 819. Baseline AT demonstration. |
| 2014 | Holloway et al. (NIST) | Broadband SI-traceable vapor-cell probe | uV/cm/sqrt(Hz) class | n/a | IEEE TAP 62, 6169. Calibration win, not SNR win. |
| 2017 | Kumar/Shaffer | Vapor-cell + FM spectroscopy | ~3 uV/cm/sqrt(Hz) | n/a | Opt. Express 25, 8625. Probe-shot-noise floor. |
| 2020 | Jing/Hu/Ma/Jia (Shanxi/USTC) | Vapor-cell superheterodyne | **~55 nV/cm/sqrt(Hz)** | ~780 pV/cm | Nat. Phys. 16, 911. Laser-frequency-noise-limited, not SQL. |
| 2024 | Tu/Liao/Zhu et al. (South China Normal U) | **Laser-cooled atoms**, heterodyne, ~5.2x10^5 atoms | **~10 nV/cm/sqrt(Hz)** | n/a | Sci. Adv. 10, eads0683; arXiv:2307.15617. Authors claim factor 2.6 above SQL. |
| 2026 | Various | Wideband Stark/comb continuous-spectrum superhet | ~65 nV/cm/sqrt(Hz) (band avg, claimed) | n/a | Comm. Phys. s42005-026-02529-3 (2026). Single-group, not yet independently replicated. |

**Important attribution corrections from the verifier (relative to scout text):** the 2024 Sci. Adv. paper is **Tu et al. (South China Normal University)** - the scout's "Cui Y, Jing M, Jia S" attribution conflates it with the Jing 2020 Shanxi/USTC group. The 2012 Sedlacek baseline is ~30 uV/cm/sqrt(Hz), not 3-5 uV/cm/sqrt(Hz) (the 3 uV/cm number belongs to subsequent FM spectroscopy work in 2017).

### 4.2 Fair comparison to a matched classical antenna

The decisive head-to-head is **Backes et al., Appl. Phys. Lett. 125, 144002 (2024); arXiv:2408.14704** (the scout's "Meyer/Kunz/Solmeyer" attribution is wrong - first author is K. M. Backes; Solmeyer is not on the author list). Conclusion: for cm-scale sensors in the electrically small regime, an unmatched antenna + active LNA back-end **OUTPERFORMS** any demonstrated Rydberg sensor. An idealized Rydberg sensor at the SQL with maximized atom number can in principle beat a 300 K antenna, but no demonstrated device is there yet.

Order-of-magnitude self-check: a matched 1 cm dipole at 10 GHz, 300 K, 50 Ohm has Johnson noise sqrt(4 k_B T R) ~ 0.91 nV/sqrt(Hz); h_eff ~ L/2 = 5 mm, so E-field NEP ~ 0.91 nV / 5 mm ~ **1.8 nV/cm/sqrt(Hz)** - about 5x BETTER than the best demonstrated Rydberg number. The classical dipole loses only when you can't match the antenna (sub-100 MHz with a cm-scale probe; the "electrically very small" regime).

### 4.3 Where Rydberg genuinely wins

- **SI-traceability / self-calibration** anchored on h and an atomic matrix element - no antenna gain, no impedance reference, no power meter.
- **One-head broadband tunability** - kHz to ~THz with different Rydberg-Rydberg transitions in the same cell, replacing an antenna farm with a frequency-tunable laser.
- **Sub-wavelength field mapping** - the sense volume is a vapor cell ~1 cm^3, much smaller than the wavelength at sub-GHz; no metallic scatterer perturbs the field.
- **Immunity to in-band damage** - no semiconductor front-end; survives strong RF that would saturate an LNA.
- **Sub-MHz / VLF / quasi-DC** where a cm-scale classical antenna decouples from the field altogether (Borowka 2026; Damitz/Sandia 2026; Chandra/Dumke 2026).

### 4.4 Where Rydberg does NOT win

- **Raw E-field SNR per Hz at GHz** - matched LNA+antenna chains beat demonstrated Rydberg by ~5x or more at the same volume.
- **Instantaneous bandwidth** - EIT linewidth caps IBW at ~few MHz (workhorse); recent multi-dress / Stark-comb / six-wave-mixing schemes push to ~100-200 MHz at the cost of sensitivity.
- **Dynamic range** - demonstrated ~80-90 dB linear AT regime; PIN-diode/attenuator classical chains trivially give 120+ dB.
- **Radio astronomy weak-signal** - cryo HEMT receivers have noise temperatures of a few K (NF ~ 0.1 dB) vs. Rydberg cells with effective noise temperatures in the thousands of K, ~3 orders of magnitude worse.

---

## 5. Frequency coverage

### 5.1 Resonant Rydberg-Rydberg microwave window

Allowed Delta n = 1 transitions in alkali Rydberg states scale as f ~ 2 R_inf c / n*^3. For the standard EIT electrometry ladder **nD_{5/2} -> (n+1)P_{3/2}** in Rb (quantum-defect-corrected n*):

| n | nD->(n+1)P frequency | nS->(n+1)P frequency (alt ladder) |
|---|---|---|
| 30 | ~245 GHz | ~ |
| 50 | **~38 GHz** | ~63 GHz |
| 70 | **~14 GHz** | ~22 GHz |
| 90 | **~6.5 GHz** | ~10 GHz |

**Verifier note:** the bare 2 Ry / n^3 formula gives 53 GHz at n=50; the 38 GHz number requires the quantum-defect correction (delta_D ~ 1.34, delta_P ~ 2.64). Both the original user-supplied table (which appeared 1-bin shifted) and the textbook hydrogen-like formula need to be reconciled before quoting a number.

### 5.2 THz ceiling

Cs nP -> (n+1)S near n ~ 18 reaches ~ 0.5-0.6 THz. Published demonstrations: Wade et al., Nat. Photonics 11, 40 (2017) - 0.55 THz imaging via Rydberg fluorescence; Downes et al., PRX 10, 011027 (2020) - full-field 0.55 THz at kHz frame rates. ~1 THz is a scaling extrapolation; no published Rydberg-fluorescence demonstration above ~0.65 THz exists.

### 5.3 Sub-GHz and beyond

- **DC-Stark off-resonant sensing** (alpha_0 propto n^7): non-resonant level shift rather than AT splitting. Used for stray-field characterization, MHz-band sensing in dielectric cells.
- **Heterodyne / mixer extension**: Simons et al., AIP Advances 9, 045030 (2019) demonstrated <1 Hz spectral resolution at GHz carriers; Jing 2020 reaches pV/cm at GHz with a strong on-resonance LO.
- **All-dielectric cells push down to sub-kHz**: Borowka, Pyragius, Boyer (Adams group), arXiv:2603.06935 (2026) - all-dielectric K cell from MHz to ~500 Hz.
- **Vapor cells now reach sub-Hz**: Chandra, Paensin, Dumke, arXiv:2603.13827 - paraffin-coated cell + lock-in, **0.5 Hz to 10 kHz** with sensitivity 819 uV/cm/sqrt(Hz) @ 1 Hz down to 2 uV/cm/sqrt(Hz) @ 1 kHz; Damitz, Burns, Jau (Sandia), arXiv:2603.23751 - bare-cell quasi-DC, 0.2-7.7 mV/m/sqrt(Hz) over 1-100 Hz. **The scout's "sub-kHz / quasi-DC remains the open problem" framing is months out of date as of June 2026.**
- **Calibration of low-frequency operation**: Kayim, Viray, La Mantia et al. (Georgia Tech Research Institute), arXiv:2603.10898 (2026) - quartz/sapphire screening models 1 kHz to 300 MHz. **The scout misattributed this to the Holloway group.**

### 5.4 Coverage map

| Band | Coverage | Mechanism | SI-traceable? |
|---|---|---|---|
| DC - sub-Hz | Marginal (Damitz 2026 floor ~0.2 mV/m/sqrt(Hz) at 1 Hz) | DC Stark, off-resonant | No (calibration referenced) |
| sub-Hz - 10 kHz | Sub-Hz vapor-cell demos exist; uV/cm class | Off-resonant Stark + auxiliary modulation | No |
| 10 kHz - 1 MHz | Off-resonant Stark or all-dielectric Borowka | Stark | No |
| 1 MHz - 1 GHz | Heterodyne / Floquet / DC-Stark tuning, off-resonant | Adjacent-resonance dressing | Partial |
| **1 - 500 GHz** | **Native AT-resonant EIT-AT, full sensitivity** | Autler-Townes splitting | **Yes (primary standard)** |
| 0.1 - 0.65 THz | Demonstrated (Wade 2017, Downes 2020) | Rydberg fluorescence upconversion | No (referenced to AT) |
| 0.65 - 1+ THz | Scaling extrapolation, n ~ 15-18 | Not yet imaged | No |

**VHF gap (~30-300 MHz):** scout omitted this dimension. Between the lowest convenient Rydberg-Rydberg dipole transition (~1 GHz) and the all-dielectric MHz regime sits an awkward band that overlaps directly with FM radio, ISM 433 MHz, and GSM 800 MHz fringe - of direct relevance to HYP-019 EMI cross-contamination. Coverage in this band requires off-resonant heterodyne or DC-Stark tuning and is not native.

**Biologically relevant DC-1 kHz (MCG, EEG):** Rydberg vapor cells now demonstrably reach this band (Damitz 2026 at 0.2 mV/m/sqrt(Hz) @ 1 Hz), but the E-field sensitivity is still ~3-5 orders below what an OPM achieves on the B-field side at the same frequency. **Rydberg cannot replace OPM for MCG sensing**; it can serve as the complementary E-field channel (see Section 9).

---

## 6. Hardware and commercial state-of-the-art

### 6.1 Minimum viable BoM (research-grade DIY)

| Item | Spec | Cost |
|---|---|---|
| Vapor cell (Rb-87 enriched, 25x75 mm Pyrex, no buffer) | Triad / Precision Glassblowing TG-ABRB | $500-700 |
| Probe ECDL @ 780.241 nm, sat-abs locked, sub-MHz linewidth | DIY Wieman-Hollberg | $600-1000 parts |
|   - commercial alternative | MOGLabs cateye + DLC202 | $10-18k |
|   - high-end commercial | Toptica DL pro + DLC pro | $25-35k |
| Coupling laser @ 480 nm, >=3 mW (DIY) / >=100 mW (commercial) | 960 nm Eagleyard ECDL + PPKTP SHG cavity | $945 (BUILD-A) |
|   - commercial alternative | Toptica TA-SHG pro (500-800 mW typical at 480 nm) | $80-140k bundled |
| Photodiodes, mounts, optics | BPW34-class + standard cage system | $300-500 |
| FPGA lock-in / PID / scan | Red Pitaya STEMlab 125-14 + PyRPL (Neuhaus 2017) | $350 |
|   - commercial alternative | SR830 | $5-7k |
| Magnetic shield (single mu-metal layer; Rydberg is Stark-dominated, modest shielding suffices) | DIY | $300-800 |

**Verifier corrections:** Toptica TA-SHG pro at 480 nm delivers **500-800 mW** (datasheet specifies 800 mW typical at 420 nm with "similar performance" at neighboring wavelengths including 480 nm); the scout's "up to 1 W" overstates the public 480 nm number. Quote-only pricing is closer to **$80-140k bundled** with DLC controller and warranty, not the scout's $60-100k floor.

### 6.2 Commercial vendors

| Vendor | Product | Frequency coverage | Sensitivity claim | Status |
|---|---|---|---|---|
| **Rydberg Technologies** (D. Anderson, Penn State / Ann Arbor) | RFMS (rack-mount), miniSatSpec (briefcase) | DC to mm-wave | Per-quote | Sells to NIST/DoD calibration labs; demoed long-range atomic comms at U.S. Army NetModX23 (Dec 2023) |
| **Quantum Valley Ideas Lab / WaveRyde spinout** (Adams group + NRC Canada) | WaveRyde receivers for 5G + defense | Per-quote | Per-quote | Spinout 2025-2026; 4 concurrent DARPA-funded projects |
| **Infleqtion** (formerly ColdQuanta) | Quantum Spectrum (launched 2026-05-13), SqyWire predecessor | Per-quote | Per-quote | UK MoD, U.S. DoD, L3Harris, SAIC, Dell Federal partnerships; UK Innovate QuDiFi DF programme |
| **NIST Boulder** (Holloway group) | Open reference designs; calibration service | 1 GHz to 500 GHz canonical; 10 MHz - sub-THz extended | uV/cm/sqrt(Hz) class with <1% SI-traceable uncertainty | Reference standard, not a product |
| **AOSense** | (No public Rydberg-RF product; primarily atom-interferometer gravimeters) | n/a | n/a | Out of scope |

None of the commercial vendors publishes list prices; everything is quote-only and defense-pitched.

### 6.3 Cold-atom Rydberg electrometry (separate hardware track)

The current SOTA sensitivity (~10 nV/cm/sqrt(Hz), Tu et al. 2024) lives in a magneto-optical-trap apparatus - kg-scale, kW-scale, immobile - not a vapor cell. The scout omitted this track entirely. Any "best-in-class" sensitivity claim that lumps cold-atom and vapor-cell numbers together overstates what a deployable BUILD-A-class instrument can reach. Vapor-cell SOTA sensitivity remains ~ 55 nV/cm/sqrt(Hz) (Jing 2020 superheterodyne) and ~ 3 uV/cm/sqrt(Hz) (FM spectroscopy CW).

### 6.4 Does BUILD-A's $4,340 BoM hold up?

The BUILD-A spec is **internally consistent** - it commits to a DIY ECDL + 960 nm-doubled SHG architecture using Wieman-Hollberg ECDL, PyRPL, Raicol PPKTP, Triad cell, and BPW34 photodetectors - and matches the minimum-viable laser stack in the academic teaching-build literature (Bhatt 2023 at ~$3k; Adams Durham < GBP 3000). It is realistic ONLY if:

1. The builder accepts the ~40% probability of SHG-stage failure that the BUILD-A spec correctly flags as Risk 1.
2. First-light sensitivity is treated as **5-30 uV/m/sqrt(Hz)** (sat-abs only, alignment-limited - the literature reproducibility data, not the optimized BUILD-A "1-3 uV/m/sqrt(Hz)" target which requires multi-month tuning).
3. Substituting any one commercial laser module (Toptica/MOGLabs/Sacher 480 nm) inflates the BoM by 10-25x, pushing total cost above $30-100k.
4. The original BUILD-A spec citation of Holloway J. Appl. Phys. 116, 244101 (2014) for the n=50 dipole moment is **incorrect** - the canonical 2014 paper is **IEEE Trans. Antennas Propag. 62, 6169** (Dec 2014). The dipole-moment number itself (~ 6340 Debye = 2.12e-26 C.m for Rb n=50) is order-of-magnitude correct; for an n=50 dipole, ARC (Sibalic et al., Comp. Phys. Commun. 220, 319, 2017) is the right primary source.

The spec also correctly notes magnetic shielding requirements are modest - Rydberg AT readout is Stark-dominated, not Zeeman, so a single mu-metal layer suffices.

---

## 7. Applications

### 7.1 Communications receivers (peer-reviewed demonstrated)

| Year | Group | Carrier | Modulation | Throughput | Source |
|---|---|---|---|---|---|
| 2018 | **Meyer/Cox/Fatemi/Kunz (U.S. Army Research Laboratory)** | 17 GHz | 8-PSK | 8.2 Mbit/s (photon-shot-noise-limited channel capacity, not implemented rate) | **APL 112, 211108** (not Phys. Rev. Applied); arXiv:1803.03545 |
| 2019 | Holloway/Simons/Gordon | 19.626 GHz | QAM / phase | n/a (video) | IEEE AWPL; arXiv:1903.10644 |
| 2022 | NIST | ~17 GHz | live video | n/a | NIST press / video |
| 2024 | Various | ~10.22 GHz | 500 kbps within 200 MHz IBW (single trade-point, not frontier) | 500 kbps | Cited via review arXiv:2507.22909 |
| 2024 | Various | 0.11 THz | Six-wave-mixing coherent photon conversion | 1.16 Mbit/s, 142 MHz BW | APL 126, 194002 (2025) |
| 2024 | Various | 0.5-2 GHz | Warm-cell QAM | up to ~100 Mbit/s region (some 2024 reports) | arXiv:2405.02901 |

**Verifier note:** the scout had Meyer et al. at NIST and the venue as Phys. Rev. Applied; both wrong. Meyer/Cox/Fatemi/Kunz were ARL, paper is APL 112, 211108 (2018). The 500 kbps figure is a tunability-vs-throughput trade point in a single review-of-review chain; multi-Mbit/s to ~100 Mbit/s exists elsewhere.

### 7.2 SI-traceable RF E-field metrology (NIST)

The most mature *deployed* application. NIST/Holloway's broadband self-calibrated probe delivers SI-traceable uncertainty <1% across ~10 MHz to sub-THz, with sensitivities in the uV/cm/sqrt(Hz) regime (state-of-art two-photon ~30 nV/cm/sqrt(Hz) at SQL). Schlossberger et al., Nat. Rev. Phys. 6, 606 (2024) is the current consolidating review. Waveguide-integrated probes have been demonstrated for near-field antenna pattern measurements. NIST already offers traceable calibration services using these probes; commercial Rydberg Technologies RFMS is sold into calibration/EMC labs and DoD.

**Verifier note:** the scout's "~46 uV/m +/- 2 uV/m, ~100x better than commercial probes; traceable >110 GHz" is not a canonical NIST headline number; safer statement is "uV/cm/sqrt(Hz) regime with <1% SI-traceable uncertainty 10 MHz to sub-THz."

### 7.3 Defense / SIGINT

- **DARPA SAVaNT** (Science of Atomic Vapors for New Technologies; 2021, four-year program, three TAs: Rydberg Electrometry, Vector Magnetometry, vQED). 2024 follow-on **EQSTRA** (Enhancing Quantum Sensor Technologies with Rydberg Atoms).
- **DARPA Quantum Apertures (QA)** (2021; ColdQuanta/Infleqtion, Honeywell, Northrop Grumman, SRI). Target spec: **10 MHz - 40+ GHz portable directional receiver in ~1 cm^3 sensor element**.
- **U.S. Army NetModX23** (Dec 2023): Rydberg Technologies demonstrated "first long-range atomic RF communication." Press-release-grade; no peer-reviewed range/throughput/SNR published.

**Verifier note:** "SAVHIN" appears in the user prompt and the scout's task brief; it is **not an attested DARPA program name**. The actual programs are SAVaNT and Quantum Apertures (and follow-on EQSTRA). Any external write-up that quotes "SAVHIN" should be corrected to "SAVaNT."

Claims of EMP-resistance / calibration-free wideband are roadmap or press-release-level; the calibration-free claim has peer-reviewed support via EIT-line traceability, EMP resistance is plausible (no semiconductor front-end) but not benchmarked in published literature.

### 7.4 Sub-GHz "through-wall" speculative use (HYP-018/019)

Pre-2024, sub-GHz coverage in vapor cells was screened out by cell-wall charging. The 2024-2026 papers (Opt. Lett. 49, 5547 (2024) at 3-18 uV/cm down to 1 kHz; arXiv:2603.13827 paraffin cell down to 0.5 Hz; Damitz/Sandia 2603.23751 at 0.2 mV/m/sqrt(Hz) @ 1 Hz) make Rydberg sensors viable on the **E-field side at biologically/architecturally relevant low frequencies**. They do not close the gap on the **B-field side**: no peer-reviewed Rydberg magnetometry exists at MCG sensitivity, and OPMs at ~10 fT/sqrt(Hz) are 3-5 orders of magnitude ahead. For HYP-018 specifically (through-wall MCG-class detection), Rydberg does NOT help on the load-bearing magnetic channel; for HYP-019 (Rydberg + OPM tricorder), Rydberg's role is the E-field complement, not a replacement for OPM. See Section 9 for explicit project framing.

### 7.5 Radio astronomy

No peer-reviewed demonstration. Rydberg noise temperatures are 3 orders of magnitude worse than cryo HEMT/MASER receivers. Dead-end for weak-signal radio astronomy for the foreseeable future.

### 7.6 Roadmap vs reality filter

- **Peer-reviewed demonstrated**: comms 8-PSK at ~8 Mbit/s; NIST E-field metrology with <1% SI-traceable uncertainty; ULF-VLF detection in K vapor cells; SI-traceable AT-regime probes 1-500 GHz; THz imaging at 0.55 THz; superheterodyne sensitivity 55 nV/cm/sqrt(Hz).
- **Press-release / not benchmarked**: Rydberg Technologies long-range comms at NetModX23; EMP-resistance; Infleqtion Sqywire field-deployed claims.
- **Roadmap only**: 6G atomic-receiver papers (arXiv:2603.21498, arXiv:2507.22909); quantum coherent RF receivers (Liao-style proposals; arXiv:2510.02134); commercial-telecom-carrier deployments; automotive radar.

---

## 8. Limitations and open problems

### 8.1 The decisive Backes/Meyer/Kunz/Cox 2024 head-to-head

**Backes et al., Appl. Phys. Lett. 125, 144002 (2024); arXiv:2408.14704** is the definitive comparison: real, room-temperature Rydberg sensors are LESS sensitive than equivalently-sized electrically-small antennas with active amplification. The "Rydberg wins" result requires idealized, atom-number-maximized, standard-quantum-limited operation that has not been built. Both idealized cases sit below the atmospheric noise floor, so even the projected win is below the use-case noise floor.

### 8.2 Direction-of-arrival

Vapor cells are intrinsically isotropic. DoA recovery requires (a) multi-cell arrays, (b) standing-wave sub-wavelength imaging (Simons/Holloway 2025, J. Appl. Phys. 138, 114402; with critical Comment arXiv:2601.20062), or (c) polarization-aware single-cell DoA via vector EIT (arXiv:2508.17179). All add laser, optics, or array complexity, give degrees-level (not arcminute) accuracy, and erase the "small simple head" advantage.

### 8.3 Polarization

Polarization sensitivity is set by the laser linear polarization vs an applied DC magnetic field (~Gauss quantization axis). This works but couples polarimetry to laser alignment AND magnetic-field stability - a regression vs an antenna whose polarization is mechanically fixed.

### 8.4 Linewidth and bandwidth

Room-T vapor cell EIT linewidth: typically **1-6 MHz**, dominated by residual two-photon Doppler (k_p - k_c) v_rms ~ 3 MHz at 780+480 nm, transit-time broadening (~100 kHz - MHz), and laser linewidth (sub-MHz with modern locked lasers; degraded for DIY ECDLs). Cold-atom MOT Rydberg arrays reach ~kHz linewidths but are non-deployable.

Bandwidth-x-sensitivity tradeoff is structural: you cannot have sub-MHz EIT and >10 MHz IBW simultaneously without paying sensitivity. Stark-comb / multi-dress schemes (arXiv:2509.26026; Anderson/Holloway arXiv:2606.25555) push toward 200 MHz IBW at per-channel sensitivity cost ~ sqrt(N_channels).

### 8.5 Dynamic range

Demonstrated **~80-90 dB** linear regime (Jing 2020 superheterodyne; Floquet/AT mixer extensions, arXiv:2601.19305). Upper limit set by ionization at Inglis-Teller / field-ionization fields (~V/cm at n=70). Classical receivers with PIN-diode/attenuator chains trivially give 120+ dB.

### 8.6 Laser cost and reliability

The **480 nm coupling laser is the dominant cost and dominant failure mode** of every research-grade and commercial system. Frequency-doubled 960 nm tapered amplifier modules at 100-500 mW cost ~$30-80k commercial; the Toptica TA-SHG pro reference build is closer to $80-140k bundled. Single-photon UV alternatives (Cs 318.6 nm: Wang et al., Opt. Express 25, 22510 (2017); Rb 297 nm: Patzak 2019) exist but have shorter component lifetimes and lower power; net cost/reliability is worse. No single-laser drop-in replacement has been demonstrated for room-T sensor-grade Rydberg EIT.

### 8.7 Blackbody radiation at 300 K

BBR-induced depopulation dominates over spontaneous decay above n ~ 30-40 at 300 K (Beterov et al., Phys. Rev. A 79, 052504 (2009); arXiv:0810.0339). For Rb n=50 nS/nP/nD at 300 K, effective lifetimes are **50-100 us** (NOT "ms-class" - the scout conflated circular-state lifetimes with sensor-relevant nS/nP/nD lifetimes; the verifier flagged this). BBR is a state-population leak that limits state purity and adds coherent crosstalk to neighboring nP/nF states (Beterov 2009 erratum; Sibalic 2016); it is NOT the dominant dephasing channel in room-T EIT electrometry, which is set by transit-time + Doppler + laser-frequency noise.

### 8.8 Environmental drift

- **Adsorbate-induced DC Stark drift**: Rb/Cs deposits on glass walls create patch potentials that drift on seconds-to-hours timescales (Jau & Carter, PRA 13, 054034 (2020); PRA 97, 023418). Corrupts amplitude calibration of weak fields; at sub-kHz, adsorbate screening is itself the signal coupling channel.
- **Temperature drift**: shifts vapor density and EIT baseline.
- **Magnetic-field excursions**: split EIT lines by Zeeman shift (~MHz/Gauss in Rydberg manifolds) - relevant when co-locating Rydberg cells with OPMs that produce mG bias-field gradients (HYP-019 cross-contamination concern).

### 8.9 Where Rydberg currently does NOT beat classical

- **GHz raw SNR per Hz** at cm form factor: classical wins by ~5x or more (Backes 2024).
- **Instantaneous bandwidth**: classical wins ~ 1-2 orders of magnitude.
- **Dynamic range**: classical wins ~ 30-40 dB.
- **Radio astronomy weak-signal**: cryo HEMT wins ~ 3 orders of magnitude in noise temperature.
- **Cost per band**: classical wins ~ 1-2 orders of magnitude (LNA + antenna << laser stack).

The honest "Rydberg wins" set is **SI traceability, sub-wavelength MHz operation, broadband one-head tunability, and metal-free in-band immunity**. Every "Rydberg X dB better" claim should be treated as falsified-by-default until per-channel, per-Hz, matched-impedance numbers are produced for the specific frequency of interest.

---

## 9. What this means for the project

### 9.1 BUILD-A realism

The $4,340 BUILD-A budget is **defensible at first light** ONLY because it commits to a DIY ECDL + 960 nm-doubled SHG path that the literature has shown to be reproducible at ~$3k (Bhatt 2023; Adams Durham teaching builds). It is realistic if the builder treats first-light sensitivity as **5-30 uV/m/sqrt(Hz)** (alignment-limited reproducibility, not the spec's optimized "1-3 uV/m/sqrt(Hz)" target) and accepts the SHG Risk 1 (~40% failure probability) flagged in the spec. Any one commercial laser substitution (Toptica TA-SHG pro at ~$80-140k bundled, or DLC pro 780 nm controller at ~$25-35k) inflates the BoM to $30-150k, an order of magnitude beyond independent-researcher budget. The smallest defensible bench-top spec is what BUILD-A already lists - there isn't a cheaper credible route to a Rydberg-EIT readout in the published record. Three citation/number corrections to fold into the spec before any external review: (a) Holloway 2014 venue is IEEE TAP 62, 6169 (NOT J. Appl. Phys. 116, 244101); (b) C_6 unit is GHz.um^6 not THz.um^6; (c) Inglis-Teller field prefactor is 1.71x10^9 / n^5 V/cm, not 3.2x10^8 / n^5.

### 9.2 HYP-018 (through-wall MCG-like detection at sub-GHz)

**Rydberg sensing does NOT help on the load-bearing magnetic channel.** MCG signals are 10-100 pT at the skin and live at DC-1 kHz - a band where (a) Rydberg vapor cells are non-competitive on raw sensitivity vs OPMs by 3-5 orders of magnitude, and (b) the relevant signal is magnetic, not electric, and Rydberg magnetometry is not within reach of the MCG floor. The 2024-2026 sub-Hz E-field Rydberg demos (Damitz 2026 at 0.2 mV/m/sqrt(Hz) @ 1 Hz) are interesting but irrelevant to MCG sensing; the per-skin E-field of a beating heart at standoff is well below the Rydberg noise floor even before wall attenuation. Honest verdict for HYP-018: the Rydberg side adds no value to a through-wall MCG hypothesis. The load remains entirely on OPM. If the framing is reformulated as "through-wall sub-GHz E-field signature characterization" (not MCG), Rydberg becomes potentially useful but the underlying physics question changes.

### 9.3 HYP-019 (combined Rydberg + OPM "tricorder")

Inside the native Rydberg AT-resonant window (~1-40 GHz), three roles add value over a $200 SDR + cm-scale antenna front-end:

1. **SI-traceable in-situ calibration of the local RF environment** - the OPM is sensitive to magnetic interference at sub-kHz that classical antennas can't cleanly characterize; the Rydberg arm gives absolute E-field calibration of any nearby radiators with no antenna-gain assumption.
2. **Metal-free near-field probe near the OPM** - the OPM operating environment requires no metallic scatterers; the Rydberg cell is dielectric and can be placed millimeters from the OPM sense volume without perturbing its field.
3. **Broadband cross-band EMI monitoring** in one head from sub-GHz to ~40 GHz, replacing a ~3-antenna farm.

What it does NOT add: raw SNR (matched LNA+antenna wins at cm scale); MCG-band magnetometry (OPM territory); sub-1-second dynamics (EIT response is ~us but readout integration to reach sensitivity floor is ~s).

The cross-contamination concern in HYP-019 is real and underspecified in the published literature: Rydberg coupling-laser blue light at 480 nm sits in a band where OPM cell coatings absorb weakly, but a misaligned beam can scatter into the OPM pump path; Rydberg DC-bias magnetic fields (~Gauss) will write into the OPM bias-field budget at the mG-mG level; no published joint-operation demo exists. Any HYP-019 budget should include a stage gate for empirical EMI characterization before committing to integration.

---

## 10. Net verdict

- **What is a Rydberg atom**: an alkali atom (Rb-87, Cs) excited to high n (~30-100), where every observable - orbital radius (n^2), dipole moment (n^2), polarizability (n^7), lifetime (n^3 at 0 K, BBR-shortened to ~100 us at n=70 at room T), C_6 (n^11), level spacing (n^-3) - follows a fixed power of n. Workhorse prep is Rb 780 + 480 nm two-photon ladder via 5P_{3/2}.
- **What is the k-factor**: in Rydberg RF electrometry, it is the Autler-Townes calibration coefficient k_AT = mu_RF / h ~ 20-30 MHz per (V/m) for typical nS->nP / nD->(n+1)P transitions at n = 40-60. This is the SI-traceable, antenna-free conversion from a measured EIT-AT splitting (Hz) to an absolute RF E-field (V/m). NOT the n-scaling exponent, NOT the Rydberg constant, NOT k_B.
- **How well do they sense radio signals**: extraordinarily well *for SI-traceable calibration and broadband one-head tunability* across roughly d.c. to ~THz with one vapor cell, with best peer-reviewed sensitivities of ~10 nV/cm/sqrt(Hz) cold-atom (Tu 2024) and ~55 nV/cm/sqrt(Hz) vapor-cell superheterodyne (Jing 2020). Poorly compared to a matched LNA + cm-scale antenna on raw SNR per Hz at GHz (Backes 2024), narrow instantaneous bandwidth (~few MHz), modest dynamic range (~80-90 dB), and dominated in BoM by the 480 nm coupling laser (~$30-140k commercial). The honest case for Rydberg is SI-traceability, sub-wavelength MHz operation, one-head broadband tunability, and metal-free in-band immunity - NOT raw SNR.

---

## Low-confidence flags

No scout dimension was graded `significant_concerns` or `weak`. All eight dimensions graded `solid` or `mostly_solid_minor_issues` by the adversarial verifier; the inline corrections above are the issues the verifier raised. The single load-bearing area where I have reduced confidence is the **wideband (1-40 GHz) continuous-spectrum superheterodyne sensitivity figure** of ~65 nV/cm/sqrt(Hz) (Comm. Phys. s42005-026-02529-3, 2026) - the verifier flagged that the underlying number was not cross-checked against the article text and is a single-group claim without independent replication. Treat that band-average number with caution.

---

## Sources

### Section 1 - Fundamentals
- T. F. Gallagher, *Rydberg Atoms*, Cambridge Univ. Press (1994), ISBN 0-521-38531-8.
- M. Saffman, T. G. Walker, K. Molmer, "Quantum information with Rydberg atoms," Rev. Mod. Phys. 82, 2313 (2010); arXiv:0909.4777.
- N. Sibalic, C. S. Adams, *Rydberg Physics*, IOP Publishing (2018).
- I. I. Beterov, I. I. Ryabtsev, D. B. Tretyakov, V. M. Entin, "Quasiclassical calculations of blackbody-radiation-induced depopulation rates and effective lifetimes of Rydberg nS, nP, and nD alkali-metal atoms with n<=80," Phys. Rev. A 79, 052504 (2009); arXiv:0810.0339; erratum PRA 80, 059902.
- W. Li, I. Mourachko, M. W. Noel, T. F. Gallagher, "Millimeter-wave spectroscopy of cold Rb Rydberg atoms in a magneto-optical trap: Quantum defects of the ns, np, and nd series," Phys. Rev. A 67, 052502 (2003).
- M. Mack et al., "Measurement of absolute transition frequencies of 87Rb to nS and nD Rydberg states by means of EIT," Phys. Rev. A 83, 052515 (2011); arXiv:1103.6221.
- N. Sibalic, J. D. Pritchard, C. S. Adams, K. J. Weatherill, "ARC: An open-source library for calculating properties of alkali Rydberg atoms," Comput. Phys. Commun. 220, 319 (2017).
- E. Tiesinga, P. J. Mohr, D. B. Newell, B. N. Taylor, "CODATA Recommended Values of the Fundamental Physical Constants: 2022," Rev. Mod. Phys. 97, 025002 (2024); arXiv:2409.03787.
- K. Singer, J. Stanojevic, M. Weidemuller, R. Cote, "Long-range interactions between alkali Rydberg atom pairs," J. Phys. B 38, S295 (2005).
- A. Browaeys, T. Lahaye, "Many-body physics with individually controlled Rydberg atoms," Nat. Phys. 16, 132 (2020).
- D. A. Steck, "Rubidium 87 D Line Data," rev. 2.2.2 (2021), https://steck.us/alkalidata/
- Walker & Saffman, Phys. Rev. A 77, 032723 (2008) - C_6 numerics.

### Section 2 - k-factor disambiguation
- J. A. Sedlacek et al., "Microwave electrometry with Rydberg atoms in a vapour cell using bright atomic resonances," Nat. Phys. 8, 819 (2012); doi:10.1038/nphys2423.
- C. L. Holloway et al., "Broadband Rydberg Atom-Based Electric-Field Probe for SI-Traceable, Self-Calibrated Measurements," IEEE Trans. Antennas Propag. 62, 6169 (2014); arXiv:1405.7066.
- J. Mitroy, M. S. Safronova, C. W. Clark, "Theory and applications of atomic and ionic polarizabilities," J. Phys. B 43, 202001 (2010).
- BIPM SI brochure (2019).

### Section 3 - EIT-AT
- M. Jing, Y. Hu, J. Ma, H. Zhang, L. Xiao, S. Jia, "Atomic superheterodyne receiver based on microwave-dressed Rydberg spectroscopy," Nat. Phys. 16, 911 (2020); doi:10.1038/s41567-020-0918-5.
- C. L. Holloway, M. T. Simons, J. A. Gordon, A. Dienstfrey, D. A. Anderson, G. Raithel, "Simultaneous use of Cs and Rb Rydberg atoms for dipole-moment assessment and RF E-field measurements via EIT," J. Appl. Phys. 120, 123103 (2016); arXiv:1607.01766.
- S. Berweger et al., "Continuous radio-frequency electric-field detection through adjacent Rydberg resonance tuning," arXiv:2105.10561 (2021).
- D. Hu et al., "Continuously tunable RF electrometry with Rydberg atoms," Appl. Phys. Lett. 121, 014002 (2022).
- S. Borowka et al., "Continuous broadband Rydberg receiver using AC Stark shifts and Floquet states," Appl. Phys. Lett. 125, 194001 (2024); arXiv:2407.05676.
- N. Prajapati et al., "Enhancement of EIT-based Rydberg-atom electrometry through population repumping," Appl. Phys. Lett. 119, 214001 (2021).
- N. Schlossberger, N. Prajapati, S. Berweger, A. Rotunno, A. Artusio-Glimpse, M. T. Simons, A. Sheikh, E. Norrgard, S. Eckel, C. L. Holloway, "Rydberg states of alkali atoms in atomic vapour as SI-traceable field probes and communications receivers," Nat. Rev. Phys. 6, 606 (2024); s42254-024-00756-7.

### Section 4 - Sensitivity
- H.-T. Tu, K.-Y. Liao, G.-D. He, Y.-F. Zhu, S.-Y. Qiu, H. Jiang, W. Huang, W. Bian, H. Yan, S.-L. Zhu, "Approaching the standard quantum limit of a Rydberg-atom microwave electrometer," Sci. Adv. 10, eads0683 (2024); arXiv:2307.15617.
- K. M. Backes, P. K. Elgee, K.-J. LeBlanc, C. T. Fancher, D. H. Meyer, P. D. Kunz, N. Malvania, K. M. Nicolich, J. C. Hill, B. L. Schmittberger Marlow, K. C. Cox, "Performance of Antenna-based and Rydberg Quantum RF Sensors in the Electrically Small Regime," Appl. Phys. Lett. 125, 144002 (2024); arXiv:2408.14704.
- S. Kumar, H. Fan, H. Kubler, A. J. Jahangiri, J. P. Shaffer, "Rydberg-atom based RF electrometry using FM spectroscopy in room-T vapor cells," Opt. Express 25, 8625 (2017); arXiv:1702.00494.
- K. C. Cox, E. B. Norrgard et al., "Optimal Atomic Quantum Sensing using EIT Readout," arXiv:2105.10494 (2021).
- D. A. Anderson, C. L. Holloway et al., "Enhancing the Instantaneous Bandwidth of Rydberg Microwave Sensors," arXiv:2606.25555.
- Communications Physics s42005-026-02529-3 (2026) - wideband 1-40 GHz superhet [single-group, unverified independently].
- MDPI Photonics 12, 1228 (2025) - Rydberg sensors review.

### Section 5 - Frequency coverage
- C. G. Wade et al., "Real-time near-field terahertz imaging with atomic optical fluorescence," Nat. Photonics 11, 40 (2017).
- L. A. Downes et al., "Full-field terahertz imaging at kilohertz frame rates using atomic vapor," Phys. Rev. X 10, 011027 (2020).
- M. T. Simons, J. A. Gordon, A. H. Haddab, C. L. Holloway, "Weak electric-field detection with sub-1 Hz resolution at RF using a Rydberg atom-based mixer," AIP Advances 9, 045030 (2019); arXiv:1903.09712.
- C. L. Holloway et al., "Self-calibrating SI-traceable broadband Rydberg atom-based RF E-field probe," arXiv:1910.07107 (2019).
- S. Borowka, U. Pyragius, V. Boyer (Adams group), "MHz to sub-kHz field detection with an all-dielectric potassium Rydberg-atom sensor," arXiv:2603.06935 (2026).
- B. Kayim, M. A. Viray, D. S. La Mantia, D. Richardson, J. Dee, R. S. Westafer, B. C. Sawyer, R. Wyllie (GTRI), "Calibration of electric fields in low-frequency off-resonant Rydberg receivers," arXiv:2603.10898 (2026). [Verifier correction: NOT a Holloway-group paper.]
- D. Chandra, B. Paensin, R. Dumke, "Electrometry of extremely-low frequencies from kHz to sub-Hz with a Rydberg-atom sensor," arXiv:2603.13827 (2026).
- D. Damitz, A. Burns, Y.-Y. Jau (Sandia), bare-cell quasi-DC Rydberg sensor, arXiv:2603.23751 (2026).
- "High sensitivity measurement of ULF, VLF and LF fields with Rydberg-atom sensor," Opt. Lett. 49, 5547 (2024); arXiv:2405.04761.

### Section 6 - Hardware and commercial
- Toptica Photonics SE, TA-SHG pro datasheet and Rydberg Solutions brochure, toptica.com.
- M. T. Simons, A. Artusio-Glimpse, A. Robinson, N. Prajapati, C. L. Holloway, "Rydberg atom-based sensors for RF electric field metrology, sensing, and communications," NIST/IMEKO2021 (updated 2022).
- "Sensitivity Comparison of Rydberg Atom-Based RF E-Field Detection: Ionization Current vs Optical Readout," arXiv:2509.15463 (2025).
- Rydberg Technologies products RFMS and miniSatSpec, rydbergtechnologies.com/products.
- Infleqtion Quantum Spectrum / SqyWire press, infleqtion.com (2026).
- Quantum Valley Ideas Lab / WaveRyde, thequantuminsider.com 2026-01-16.
- L. Neuhaus et al., "PyRPL: Python Red Pitaya Lockbox for FPGA-controlled quantum optics," SoftwareX 6, 206 (2017).
- C. Wieman, L. Hollberg, "Using diode lasers for atomic physics," Rev. Sci. Instrum. 62, 1 (1991).
- Precision Glassblowing TG-ABRB Rb vapor cell, precisionglassblowing.com.
- BUILD-A: DIY Rydberg Vapor-Cell Electrometer (project spec), D:/quantum-worldline/research/data/builds/BUILD-A-rydberg-electrometer.md.

### Section 7 - Applications
- D. H. Meyer, K. C. Cox, F. K. Fatemi, P. D. Kunz, "Digital Communication with Rydberg Atoms and Amplitude-Modulated Microwave Fields," **Appl. Phys. Lett. 112, 211108 (2018)**; arXiv:1803.03545. [Verifier correction: ARL, not NIST; APL, not Phys. Rev. Applied.]
- Holloway/Simons/Gordon 19.626 GHz QAM, IEEE AWPL; arXiv:1903.10644 (2019).
- "Rydberg atomic receivers for 6G wireless communication and sensing," arXiv:2603.21498 (2026).
- "Rydberg Atomic Receivers for Wireless Communications (review)," arXiv:2507.22909 (2025).
- "Interference Resilient Quantum Receivers with Rydberg Atoms," arXiv:2510.02134 (2025).
- "A warm Rydberg atom-based quadrature amplitude-modulated receiver," arXiv:2405.02901 (2024).
- "Digital terahertz communication with Rydberg-atom-based coherent photon conversion," Appl. Phys. Lett. 126, 194002 (2025).
- DARPA SAVaNT program, darpa.mil/research/programs/science--atomic-vapors-for-new-technologies. DARPA Quantum Apertures, darpa.mil/research/programs/quantum-apertures. EQSTRA follow-on (2024).
- Rydberg Technologies long-range comms at NetModX23, thequantuminsider.com (2023-12).

### Section 8 - Limitations
- Backes et al., APL 125, 144002 (2024); arXiv:2408.14704 (head-to-head antenna comparison) - see Section 4.
- Tu et al., Sci. Adv. 2024; arXiv:2307.15617 (SQL approach, cold atoms) - see Section 4.
- Beterov et al., PRA 79, 052504 (2009); arXiv:0810.0339 (BBR rates) - see Section 1.
- A. K. Robinson, N. Prajapati, D. Senic, M. T. Simons, C. L. Holloway, "Determining the Angle-of-Arrival of an RF Source with a Rydberg Atom-Based Sensor," arXiv:2101.12071 (2021).
- M. T. Simons, N. Prajapati, C. L. Holloway et al., "Determining angle of arrival of RF fields using subwavelength amplitude-only measurements of standing waves in a Rydberg atom sensor," J. Appl. Phys. 138, 114402 (2025); arXiv:2502.09835 (with critical Comment arXiv:2601.20062).
- "Polarization-Aware DoA Detection Relying on a Single Rydberg Atomic Receiver," arXiv:2508.17179 (2025).
- J. Wang, J. Bai, J. He, J. Wang, "Single-photon cesium Rydberg excitation spectroscopy using 318.6-nm UV laser and room-T vapor cell," Opt. Express 25, 22510 (2017); arXiv:1706.06237.
- Y.-Y. Jau, T. Carter, "Vapor-Cell-Based Atomic Electrometry for Detection Frequencies below 1 kHz," Phys. Rev. Applied 13, 054034 (2020).
- "Probing Bandwidth and Sensitivity in Rydberg Atom Sensing via Optical Homodyne and RF Heterodyne Detection," Phys. Rev. A (2025); arXiv:2509.20632.
- G. Santamaria-Botello, S. Verploegh, E. Bottomley, Z. Popovic, "Comparison of Noise Temperature of Rydberg-Atom and Electronic Microwave Receivers," arXiv:2209.00908 (2022).

### Project-specific
- D:/quantum-worldline/research/data/builds/BUILD-A-rydberg-electrometer.md (BUILD-A spec).
- HYP-018, HYP-019, HYP-020 records in D:/quantum-worldline/research/data/hypotheses/.
- MEMORY.md project memory index (D:/quantum-worldline/CLAUDE.md context).
