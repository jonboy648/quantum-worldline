# DEEP-DIVE: NV Magnetometer + Earth-Field NMR Fusion

**Subject:** Quantitative validation of the #1 sensor-fusion candidate (NOVEL-COMBO-A C1).
**Date:** 2026-05-16
**Verdict line:** **NEEDS-MODIFICATION** — signal chain validates, but a bare broad-CW
hobby NV does NOT see the proton FID; requires a ~1 T cheap NdFeB prepolarizer (→ ~1.6 µT
@ NV, SNR=3 in ~2 s) or a good DIY pulsed NV (→ 20 nT case, SNR=3 in ~1-10 s).
Earth-field-only prepolarization is REFUTED (~2 pT). MVP ≈ $530-980.

---

## 0. The Claim Under Test

An EF-NMR sample is prepolarized (Earth field, or a cheap 0.1-1 T permanent-magnet
prepolarizer). On polarizing-field shutoff the protons precess at the Larmor frequency
in Earth's field (~2 kHz). A DIY NV diamond magnetometer placed mm-scale from the sample
transduces the precessing nuclear dipole field optically (pulsed AC magnetometry, filter
notch at the Larmor frequency), giving spatially-localized, chemically-specific,
optically-detected Earth-field NMR.

The wave-1 file flagged the killer risk explicitly: a broad-ODMR hobby NV may not see a
bare proton signal; need a strong prepolarizer or a doped phantom. This file resolves
that quantitatively.

---

## 1. Signal Budget

### 1.1 Constants and geometry

| Quantity | Symbol | Value |
|---|---|---|
| Proton gyromagnetic ratio | γ_p / 2π | 42.577 MHz/T |
| Proton magnetic moment | μ_p | 1.4106 × 10⁻²⁶ J/T |
| Proton number density, pure water | n_p | 6.7 × 10²⁸ m⁻³ (2 × 55.5 mol/L) |
| Boltzmann constant | k_B | 1.381 × 10⁻²³ J/K |
| Temperature | T | 300 K |
| Earth field (measurement) | B₀ | 50 µT → f_L = γ_p·B₀/2π ≈ **2.13 kHz** |
| Vacuum permeability | μ₀/4π | 1.0 × 10⁻⁷ T·m/A |

The fusion is a **detection of bulk (Boltzmann) magnetization**, not statistical
polarization. This is the decisive distinction from the lab NV-NMR literature (see §3):
nanoscale/microscale NV-NMR detects the √N *statistical* polarization of a zL-pL droplet
sitting directly on the diamond (standoff ~ nm). The EF-NMR fusion instead detects the
*net thermal dipole* of a mL-scale sample at a **mm standoff**. Different regime, different
math, and that is exactly where the risk lives.

### 1.2 Thermal polarization

Boltzmann polarization at prepolarizing field B_p:

  P = tanh(γ_p ℏ B_p / 2 k_B T) ≈ μ_p B_p / k_B T

- Earth's field only (B_p = 50 µT): P = 1.4106e-26 × 5e-5 / (1.381e-23 × 300)
  = **1.7 × 10⁻¹⁰** (0.17 ppb). Essentially nothing.
- NdFeB stack, B_p = 0.5 T: P = 1.4106e-26 × 0.5 / 4.14e-21 = **1.7 × 10⁻⁶** (1.7 ppm).
- Strong cheap Halbach / 1 T: P = **3.4 × 10⁻⁶**.

Prepolarization buys a factor B_p/B₀ ≈ **10⁴** over Earth-field-only equilibrium. This
is the standard EF-NMR trick and it is mandatory here — bare Earth-field equilibrium
magnetization is hopeless for any magnetometer at a mm standoff.

### 1.3 Sample magnetic moment and the AC field at the NV

Net magnetization of a sample of volume V:

  M = n_p · μ_p · P · V  (total moment, A·m²)

After 90° tip the transverse moment precesses at f_L; the NV at standoff d sees a dipole
field that, for an optimally-placed sensor (on the dipole axis), is

  B_AC ≈ (μ₀/4π) · 2 M / d³   (axial), or (μ₀/4π) · M / d³ (equatorial).

Use the equatorial / order-of-magnitude form B_AC ≈ (μ₀/4π) · M / d³ and treat the
factor-2 as geometry headroom.

**Worked case A — realistic first-light phantom.**
B_p = 0.5 T NdFeB prepolarizer, V = 1 cm³ = 1e-6 m³ pure water, standoff d = 2 mm.

- M = n_p·μ_p·P·V = 6.7e28 × 1.4106e-26 × 1.7e-6 × 1e-6
  = (944.7) × 1.7e-6 × 1e-6 = **1.61 × 10⁻⁹ A·m²**
- B_AC = (μ₀/4π)·M/d³ = 1e-7 × 1.61e-9 / (2e-3)³ = 1e-7 × 1.61e-9 / 8e-9
  = **2.0 × 10⁻⁸ T ≈ 20 nT** (axial ~40 nT)

20 nT at the NV. This is the number the wave-1 file's risk flag was really about: it is
*not* µT-scale. The mm-standoff dipole of a mL sample is **nT-class**, which sits right at
the boundary between "good DIY pulsed NV" and "broad CW hobby NV."

**Worked case B — pure Earth-field prepolarization (no magnet), same geometry.**
P = 1.7e-10 → M scales by (1.7e-10 / 1.7e-6) = 1e-4 → M = 1.61e-13 A·m²
→ B_AC = 1e-7 × 1.61e-13 / 8e-9 = **2.0 × 10⁻¹² T ≈ 2 pT**.

**Worked case C — small sample, larger standoff (imaging-like).**
B_p = 0.5 T, V = 10 µL = 1e-8 m³, d = 5 mm.
M = 1.61e-9 × (1e-8/1e-6) = 1.61e-11 A·m²;
B_AC = 1e-7 × 1.61e-11 / (5e-3)³ = 1e-7 × 1.61e-11 / 1.25e-7 = **1.3 × 10⁻¹¹ T ≈ 13 pT**.

**Worked case D — bigger sample, tight standoff, stronger magnet (best feasible cheap).**
B_p = 1.0 T (Halbach NdFeB), V = 5 cm³ = 5e-6 m³, d = 1 mm.
P = 3.4e-6; M = 6.7e28 × 1.4106e-26 × 3.4e-6 × 5e-6 = 944.7 × 3.4e-6 × 5e-6
= **1.6 × 10⁻⁸ A·m²**;
B_AC = 1e-7 × 1.6e-8 / (1e-3)³ = 1e-7 × 1.6e-8 / 1e-9 = **1.6 × 10⁻⁶ T ≈ 1.6 µT** (axial ~3 µT).

### 1.4 NV noise floors

| NV class | AC sensitivity (B_min for 1 s, ≈ noise √Hz) | Source |
|---|---|---|
| Hobby broad-CW-ODMR (UncutGem-class) | ~1-30 µT/√Hz (broad ODMR, LED pump, no DD) | DIY-SENSOR-SURVEY: UncutGem "not stated"; MDPI CW-ODMR "µT range"; LED-NV arXiv:2512.03106 "nT-scale" (best DIY) |
| Good DIY pulsed ensemble (XY8/CPMG) | ~1-10 nT/√Hz | LED-NV portable arXiv:2512.03106 quotes nT-scale |
| Research ensemble (optimized) | ~10 pT/√Hz | arXiv:2410.21182 / 2504.00887; 8.9 pT/√Hz @ 2.9 GHz demonstrated |

The honest hobby number to design against: **broad-CW-ODMR UncutGem ≈ 1-30 µT/√Hz**;
a *well-built* DIY pulsed-AC LED-NV (arXiv:2512.03106 class) ≈ **1-10 nT/√Hz**. The
fusion's viability hinges entirely on which of these the build achieves, because the
proton FID at the NV in Case A is ~20 µT and in Case C is ~13 nT.

### 1.5 SNR and integration time

SNR after averaging time τ with white-noise floor S_B (T/√Hz) over detection bandwidth
set by τ (single-sided, Δf ≈ 1/2τ):

  SNR ≈ B_AC / (S_B · √(1/2τ)) = B_AC · √(2τ) / S_B
  → τ(SNR=3) = (1/2) · (3 · S_B / B_AC)²

Caveat: the FID decays with T2* (Earth-field, unshielded, mL water ≈ 0.1-1 s; gradients
dominate). Useful coherent averaging per shot is capped at ~T2*; longer τ means more
prepolarize→acquire **shots**, each costing a ~1-5 s prepolarization dead time. So the
effective duty cycle is poor (~10-30%); multiply τ below by ~3-10× for wall-clock.

| Case | B_AC | NV floor S_B | τ for SNR=3 (ideal) | Verdict |
|---|---|---|---|---|
| **D** (1 T, 5 cm³, 1 mm) | 1.6 µT | 30 µT/√Hz (worst hobby CW) | (1/2)(3·30000/1600)² ≈ **1580 s (26 min)** | marginal/no |
| D | 1.6 µT | 1 µT/√Hz (good hobby CW) | (1/2)(3·1/1.6)² ≈ **1.8 s** | ✅ yes |
| D | 1.6 µT | 10 nT/√Hz (good DIY pulsed) | ~0.2 ms | ✅ trivial (1-shot) |
| **A** (0.5 T, 1 cm³, 2 mm) | 20 nT | 1 µT/√Hz (good hobby CW) | (1/2)(3·1000/20)² ≈ **1.1 × 10⁴ s (3 h)** | ❌ no |
| A | 20 nT | 30 nT/√Hz (best DIY LED-NV, 2512.03106) | (1/2)(3·30/20)² ≈ **10 s** | ✅ yes |
| A | 20 nT | 10 nT/√Hz (good DIY pulsed XY8) | (1/2)(3·10/20)² ≈ **1.1 s** | ✅ yes |
| **C** (0.5 T, 10 µL, 5 mm) | 13 pT | 10 nT/√Hz (good DIY pulsed) | (1/2)(3·10000/13)² ≈ **2.7 × 10⁷ s** | ❌ dead |
| C | 13 pT | 10 pT/√Hz (research ensemble) | (1/2)(3·10/13)² ≈ **27 s** | ✅ (lab only) |
| **B** (Earth-pol only) | 2 pT | 10 nT/√Hz (good DIY) | ~10⁸ s | ❌ dead |

**Killer subtlety:** SNR=3 integration assumes coherent averaging, but each prepolarize→
acquire shot yields only ~T2* of signal (Earth-field, unshielded mL water ≈ 0.1-1 s,
gradient-limited) and costs ~1-5 s prepolarization dead time. Effective duty cycle
~10-30%, so multiply ideal τ by ~3-10× for wall-clock. Earth-field-only prepolarization
(Case B, 2 pT) is **refuted for any NV class** — orders of magnitude under even research
ensembles. Microscale imaging (Case C) is **refuted for DIY**; only research ensembles
reach it.

### 1.6 Signal-budget headline

> **A 5 cm³ water sample prepolarized at 1 T (cheap NdFeB Halbach) and read at 1 mm
> standoff produces a ~1.6 µT AC field at the NV at the 2.13 kHz proton Larmor
> frequency.** That clears a *good* hobby CW-ODMR floor (~1 µT/√Hz) at SNR=3 in
> ~2 s ideal (~10-20 s wall-clock), and a good DIY pulsed-AC NV trivially in one shot.
> The 0.5 T / 1 cm³ / 2 mm case is ~20 nT — **requires a good DIY pulsed NV
> (arXiv:2512.03106-class, ~10-30 nT/√Hz), NOT a bare broad-CW UncutGem.** The
> Earth-field-only proton signal (~2 pT at 2 mm) is refuted: the prepolarizer is the
> single load-bearing component.

## 2. The Sub-Problem the Fusion Forces

The fusion forces exactly the sub-problem the wave-1 file flagged, and the numbers above
make it precise:

**The real sub-problem: closing the gap between a ~nT-µT proton AC field and a hobby NV
floor that ranges over 3 orders of magnitude (10 pT/√Hz research → 30 µT/√Hz broad CW).
This is *not* solved by buying a better NV; it is solved by maximizing the source dipole
moment so the signal lands above whatever NV the builder actually has.**

Three knobs, with the quantitative requirement for each (target: B_AC ≥ 1 µT so even a
mediocre CW-ODMR hobby NV works in seconds; this is the conservative design point):

### 2.1 Prepolarizer strength (the dominant knob)
B_AC ∝ B_p linearly (through P = μ_p B_p / k_B T).
- Earth field (50 µT): refuted (2 pT @ Case-A geom).
- 0.1 T cheap disc magnet: P ≈ 3.4e-7 → ~4 nT in Case-A geometry. Needs good DIY pulsed NV.
- **0.5 T (stack of N52 NdFeB discs, ~$30-60): P ≈ 1.7e-6 → 20 nT @ Case A.** DIY pulsed NV only.
- **1.0 T (small NdFeB Halbach array, ~$80-200): P ≈ 3.4e-6 → 1.6 µT @ Case D.** Any NV.
A Halbach cylinder bore of 1-1.5 T is achievable with hobby NdFeB for a few-cm³ sample
(this is exactly how commercial benchtop and EF-NMR prepolarizers work — confirmed by the
EF-NMR prepolarization literature, §3). **This is the single highest-leverage fix.**

### 2.2 Sample volume × proximity (geometry knob)
B_AC ∝ V/d³. Going from (1 cm³, 2 mm) to (5 cm³, 1 mm) is a ×40 gain (×5 volume, ×8 from
d⁻³). The constraint: the sample must fit inside the prepolarizer bore *and* sit ≤1-2 mm
from the diamond after transfer. A flow/transfer geometry (prepolarize in magnet, shuttle
to NV) decouples these but adds T1 decay during transfer (water T1 ≈ 2-3 s, transfer must
be < ~1 s). Static geometry (diamond inside/adjacent to a prepolarizer with a shutoff
coil) avoids transfer loss but requires fast field switching near the NV — the EF-NMR
"fast discharge" prepolarization technique (§3, ScienceDirect S109078071730157X) is
directly applicable.

### 2.3 Paramagnetic doping / contrast agent (signal-shaping knob)
Doping does **not** increase equilibrium M (it slightly *reduces* proton density), but it
collapses T1 from ~2-3 s to ~10-100 ms. Effect: **far faster prepolarization recycling**
→ higher duty cycle → more shots per minute → better averaged SNR per wall-clock second.
- CuSO₄ ~10-50 mM (the wave-1 file's proposed phantom): T1 → ~50-200 ms. ~10-20× faster
  recycling. Good first-light choice.
- Gd-DTPA (MRI contrast, ~$0 from an expired clinical vial or ~$30 research grade):
  T1 → ~10-50 ms at ~1-5 mM. Best recycling, but too much Gd broadens the line (T2*↓)
  and *hurts* frequency resolution — there is an optimum (~1-2 mM).
Doping is a **duty-cycle multiplier, not a signal-amplitude fix.** It cannot rescue a
sub-floor B_AC; it only makes an above-floor signal accumulate faster. The amplitude
problem is solved only by §2.1 + §2.2.

### 2.4 The quantitative bottom line on the sub-problem
To make this work with the *actual cataloged hobby NV* (UncutGem, broad CW-ODMR, the
worst case ~µT-class), the source must deliver **B_AC ≳ 1 µT**, which requires
**B_p ≈ 1 T (cheap NdFeB Halbach) + V ≈ 5 cm³ + d ≈ 1 mm** (Case D). With a *good DIY
pulsed* LED-NV (arXiv:2512.03106, ~10-30 nT/√Hz) the requirement relaxes to **B_p ≈
0.5 T + 1 cm³ + 2 mm** (Case A, 20 nT, SNR=3 in seconds). Doping (CuSO₄ ~20 mM) is
recommended in both cases purely to lift duty cycle.

## 3. Prior Art

(arXiv MCP stale per task brief; the following is from WebSearch, 2026-05-16.)

### 3.1 NV detection of NMR — PUBLISHED, but a different regime
NV-NMR is a mature lab field. Key precedents:
- **Nanoscale NV-NMR**: single-NV detection of ~nm³ proton ensembles, statistical-
  polarization regime, zL volumes, nm standoff — *Nanoscale NMR with an NV spin sensor*,
  Science 339, 561 (2013); single-protein detection. (science.org/doi/10.1126/science.1231540)
- **Microscale NV-NMR**: ensemble NV under a ~pL-nL droplet, ~10 pT/√Hz, picoliter
  volumes (single-cell scale), 2D NMR demonstrated — *2D NMR with a microfluidic diamond
  quantum sensor*, Sci. Adv. 5, eaaw7895 (2019); review PMC9301930; high-field microscale
  ensemble work arXiv:2410.21182, 2504.00887; 8.9 pT/√Hz @ 2.9 GHz demonstrated.
- These all operate at **high field** (often several T bias for the *nuclear* Larmor),
  on **diamond-surface-contacting** samples, with **shielded research apparatus** and
  isotopically engineered diamond. The detected polarization is usually the √N
  *statistical* fluctuation of a tiny volume, not bulk thermal magnetization at a
  mm standoff.

### 3.2 Optical-magnetometer-detected low-field / Earth-field NMR — PUBLISHED
The Budker–Pines program is the canonical prior art for *optically read out* low-field NMR:
- All-optical (alkali vapor / SERF) magnetometer detecting a **proton free-precession
  signal from water prepolarized at 0.7 T and detected in a ~4 µT field** —
  arXiv:0906.1089 ("All-optical magnetometry for NMR detection in a micro-...");
  Berkeley/LBL "NMR Using Earth's Magnetic Field" (2014).
- Zero-/ultra-low-field NMR with atomic magnetometers and J-spectroscopy — Pines Lab
  zero-field optical detection; PNAS 105, 2286 (2008) microfabricated atomic magnetometer
  remote zero-field NMR.
- SQUID-detected prepolarized low-field NMR — long-established (no cryogen-free benefit).
**Crucially: the optical magnetometer in all this prior art is an alkali-vapor / SERF
magnetometer, NOT an NV diamond.** The 0.7 T-prepolarize → µT-detect → optical-readout
architecture is exactly the EF-NMR fusion's architecture — but realized with a vapor cell,
not a hobby NV.

### 3.3 EF-NMR prepolarization engineering — PUBLISHED
Prepolarized Earth-field NMR with ~0.1 T (≈100 G) permanent-magnet/coil prepolarizers,
fast-discharge switching, is textbook (ScienceDirect S1090780712001577 "Earth field NMR
with chemical shift resolution"; S109078071730157X "Pre-polarization fields … fast
discharge"; TeachSpin Earth's-Field-NMR product; Wikipedia "Earth's field NMR"). The
~10⁴ prepolarization gain assumed in §1.2 is standard, validated practice.

### 3.4 What is NOVEL in THIS specific cheap fusion
| Element | Status |
|---|---|
| NV detecting NMR | Published (nano/microscale, high-field, lab) |
| Optical-magnetometer-detected Earth/low-field NMR | Published — but with **vapor/SERF**, not NV |
| Prepolarized EF-NMR with cheap permanent magnet | Published (standard) |
| **Bulk-magnetization, mm-standoff, Earth-field (2 kHz) proton FID read by a sub-$200 broad-ODMR DIY NV, with a cheap NdFeB prepolarizer, as a fused instrument** | **No precedent found** |

The novel slice is narrow but real: every *component* is published, but the specific
combination — DIY hobby-NV (not vapor cell, not lab confocal NV) transducing a
*permanent-magnet-prepolarized, Earth-field-precessing, mL bulk* proton FID at mm standoff
— has no located precedent. It is the **DIY/Earth-field/bulk regime of NV-detected NMR**,
adjacent to but distinct from (a) lab nanoscale NV-NMR and (b) vapor-cell low-field
OD-NMR. The contribution is an *artifact and a regime*, not new physics.

## 4. Verdict + Minimum Viable Build

### 4.1 Verdict: **NEEDS-MODIFICATION** (signal chain is sound; the cheap NV alone is not)

The signal chain validates *quantitatively* — but only with the modifications the numbers
dictate:

1. **The proton FID does NOT clear a bare broad-CW-ODMR UncutGem-class NV (~1-30 µT/√Hz)
   in the wave-1 file's nominal geometry.** At B_p=0.5 T, 1 cm³, 2 mm the field is ~20 nT,
   100-1000× under that floor. The wave-1 risk flag was correct and is *confirmed
   quantitatively*.
2. **It DOES clear the floor with one of two modifications:**
   - **(M1) Strong cheap prepolarizer:** B_p ≈ 1 T NdFeB Halbach + 5 cm³ + 1 mm standoff
     → **B_AC ≈ 1.6 µT**, detectable at SNR=3 in **~2 s ideal / ~10-20 s wall-clock even
     on a worst-case µT-class hobby CW-ODMR NV.** This rescues the *actual cataloged
     UncutGem*.
   - **(M2) Better DIY NV:** use the arXiv:2512.03106 portable LED-NV (nT-class,
     ~$200) or a DIY pulsed-XY8 ensemble (~10 nT/√Hz). Then B_p=0.5 T / 1 cm³ / 2 mm
     (20 nT) detects at SNR=3 in ~1-10 s.
3. **Earth-field-only prepolarization is REFUTED** for every NV class (~2 pT @ 2 mm).
4. **Microscale chemical *imaging* (Case C, pL-nL voxels) is REFUTED for DIY** — needs a
   research ~10 pT/√Hz ensemble. The realistic DIY milestone is **unambiguous detection
   of a bulk FID at the correct Larmor frequency and T2***, not imaging — exactly as the
   wave-1 editorial already concluded.
5. Net: the fusion is real and buildable, but it is a **prepolarizer-dominated** instrument.
   The headline deliverable is "DIY optically-detected (NV) prepolarized low-field NMR" —
   which is *adjacent to but not the same as* the published vapor-cell Budker–Pines result
   (§3.2). Novelty survives; the NV (not vapor cell) and the hobby budget are the
   distinguishing claims.

### 4.2 Minimum Viable Build (parts + cost)

Design point M1 (works with the cheapest NV — recommended for de-risking first light):

| Item | Spec | Cost |
|---|---|---|
| DIY NV magnetometer | UncutGem v2 (arXiv:2509.18329) — cheapest; OR LED-NV portable arXiv:2512.03106 (better, recommended) | $100 / $200 |
| Prepolarizer | NdFeB N52 Halbach array or stacked-disc bore, ≥1 T over a ~1 cm bore | $80-200 |
| Fast-discharge switch | MOSFET H-bridge + freewheel for <1 ms B_p shutoff (EF-NMR fast-discharge design, ScienceDirect S109078071730157X) | $30-60 |
| EF-NMR base kit | RowleyLab EF-NMR or pyppm (sample cell, B₀ trim/Helmholtz coils, DAQ, lock-in) | $300-500 |
| Phantom | 5 mL water + CuSO₄ ~20 mM (T1 → ~100 ms, duty-cycle multiplier) | <$5 |
| Standoff jig | 3D-printed cell holder fixing diamond ≤1 mm from sample wall, non-magnetic | ~$10 |
| Shielding (optional first-light) | mu-metal can or distance from 50/60 Hz sources (Larmor 2.13 kHz sits near mains harmonics — see below) | $0-150 |
| **Total** | | **≈ $530-980** (vs wave-1 estimate $450-650; the +$ is the 1 T prepolarizer + switch the physics demands) |

### 4.3 Build-critical caveats (from the physics, not optional)

- **Mains-harmonic collision:** f_L ≈ 2.13 kHz at 50 µT. 60 Hz × 35 = 2100 Hz; 50 Hz × 43
  = 2150 Hz. The proton line sits *inside* the mains-harmonic forest. **Tune B₀ with the
  EF-NMR trim coils to park f_L in a clean window (e.g. set B₀ → 47 µT for f_L ≈ 2.00 kHz,
  or 55 µT for 2.34 kHz) and use a gradiometric NV pair or notch.** This is mandatory, not
  cosmetic — it was the wave-1 file's secondary failure mode and the numbers confirm it.
- **T2* / duty cycle:** unshielded Earth-field mL water T2* ≈ 0.1-1 s (gradient-limited).
  Each shot ≈ T2* signal + 1-5 s prepolarization dead time. Wall-clock ≈ 3-10× the ideal
  τ in §1.5. CuSO₄ doping (M-neutral, T1↓) is the duty-cycle fix.
- **Pulsed vs CW NV:** a 2.13 kHz AC signal is best read with NV **pulsed AC magnetometry
  (CPMG/XY8 with the filter notch at f_L)**, not raw CW-ODMR. UncutGem is primarily a
  CW-ODMR design; the build must add a pulsed-AC sequence (microwave + timing) or accept
  the worst-case µT-class CW floor (still works at M1's 1.6 µT, but pulsed is strongly
  preferred and is how the §1.4 "good DIY" nT floors are reached).
- **First validating measurement (unchanged from wave-1, now quantified):** prepolarize
  the 5 mL CuSO₄ phantom at 1 T, fast-discharge, run NV pulsed-AC notch at f_L; success =
  NV-read frequency matches the EF-NMR pickup-coil frequency within 1% and decays with the
  same T2*. Expected SNR=3 in ~10-20 s wall-clock (M1, worst-case hobby NV).

---

*Generated 2026-05-16. Signal budget computed from first principles; prior art from
WebSearch (arXiv MCP stale). All B_AC values are equatorial point-dipole order-of-
magnitude; axial geometry gives ×2 headroom.*
