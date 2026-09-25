# DEEP-DIVE: DIY EF-NMR / NV-NMR as a Field-Independent Heteronuclear J-Coupling Spectrometer

**Subject:** Quantitative validation of QCHEM-COMBO-C candidate #1 (the top hardware
quantum-chemistry candidate). Run a sub-$500 DIY Earth-field-NMR rig (RowleyLab/pyppm
class) as a heteronuclear scalar-J spectrometer, fit a classical spin Hamiltonian, and
extract the Fermi-contact s-character of a real P–H / P–F bond.
**Date:** 2026-05-17
**Verdict line:** *(see §5)*

---

## 0. The claim under test

1. Chemical shift is dead at Earth field (~2 kHz proton Larmor): shift dispersion is
   sub-mHz — unresolvable.
2. Heteronuclear scalar J-coupling IS field-independent and fully resolvable at Earth
   field — a 10–20 Hz P–H multiplet survives.
3. The extracted J is a *bona fide electronic-structure observable* (Fermi-contact ∝
   s-electron density at both nuclei / bond s-character), not a weak proxy.
4. A DIY rig (pyppm/RowleyLab ~$300–500, or an UncutGem-class NV) can reach the linewidth
   needed to resolve 2J/3J ≈ 10–20 Hz.

This file tests all four with numbers and against prior art.

---

## 1. Physics

### 1.1 Why chemical shift is dead but J survives — the field-scaling argument

Two spin–spin / spin–field terms set the spectrum:

- **Chemical shift.** The shift offset of a nucleus in Hz is `Δν = σ · γ B₀ / 2π`,
  where σ is the (dimensionless, ~ppm) shielding. It scales **linearly with B₀**. At a
  9.4 T benchtop (400 MHz ¹H), 1 ppm = 400 Hz. At Earth field B₀ = 50 µT, f_L(¹H) =
  γ_p B₀/2π = 42.577 MHz/T × 50e-6 T ≈ **2.13 kHz**. There 1 ppm = 2.13 mHz, and the
  *entire* ¹H shift range (~10 ppm) spans **~21 mHz**. To resolve even the full proton
  window you would need a linewidth < ~20 mHz, i.e. a coherence time T2* > ~15 s in a
  field homogeneous to < 1 ppb. Unshielded Earth-field water gives T2* ≈ 0.1–1 s
  (gradient-limited) → linewidth 0.3–3 Hz, which is **100–1000× too coarse**. Chemical
  shift is unrecoverable on any DIY rig. Confirmed standard physics (Wikipedia *J-coupling*;
  LibreTexts; nanalysis benchtop blog; QCHEM-COMBO-C carry-over).

- **Scalar J-coupling.** The indirect electron-mediated spin–spin coupling enters the
  Hamiltonian as `2π J Î·Ŝ` (heteronuclear weak-coupling limit: `2π J Î_z Ŝ_z`). J is a
  **molecular constant in Hz that does not contain B₀ at all** — it is an intramolecular
  electron-mediated interaction, not a Zeeman term. This is textbook and was demonstrated
  in the original Hahn–Maxwell spin-echo modulation experiment: the echo carried a
  field-independent beat at J alongside the field-dependent shift beat (Wikipedia
  *J-coupling*; NMR-Wiki *Scalar coupling*; LibreTexts). **J is field-independent to
  better than the ppm level** (a tiny B₀-dependence exists only through second-order
  field-dependent mixing, utterly negligible here). So a 10–20 Hz P–H J that is a
  *small perturbation buried under kHz of shift dispersion at 9.4 T* becomes, at Earth
  field, **the dominant resolvable internal structure** of the spectrum.

> **Core result, confirmed:** at Earth field, shift → dead (sub-mHz), J → fully alive
> (Hz, field-independent). The claim in QCHEM-COMBO-C is physically correct.

### 1.2 Spin Hamiltonian — heteronuclear AX and AX₃ at Earth field

Take ¹H (spin I, γ_H) and ³¹P (spin S, γ_P; ³¹P is spin-½, 100% abundant — ideal). In
the lab/rotating frame at B₀ along z:

**AX (one ¹H, one ³¹P), weak-coupling (heteronuclear) limit.**
Because γ_H/γ_P ≈ 2.47, the two Larmor frequencies differ by hundreds of Hz even at
Earth field (see §1.4) ≫ J, so the secular (weak-coupling) Hamiltonian is:

```
H/h = ν_H Î_z + ν_P Ŝ_z + J Î_z Ŝ_z
ν_H = γ_H B₀ / 2π ≈ 2129 Hz   (B₀ = 50 µT)
ν_P = γ_P B₀ / 2π ≈  862 Hz   (γ_P/2π = 17.235 MHz/T)
```

Eigenvalues for the four `|m_I, m_S⟩` states give two ¹H transitions at
`ν_H ± J/2` and two ³¹P transitions at `ν_P ± J/2`. **Observed proton spectrum: a
doublet split by exactly J Hz, centred at 2.13 kHz.** No shift information; the only
internal structure is the J doublet.

**AX₃ (three equivalent ¹H, one ³¹P) — e.g. one OCH₃ ↔ P pathway, or the P–H + 3×
equivalent topology.** Three equivalent protons coupled to one ³¹P with common coupling
J:

```
H/h = ν_H Σᵢ Î_z^(i) + ν_P Ŝ_z + J (Σᵢ Î_z^(i)) Ŝ_z
```

The three equivalent ¹H give a total `M_I ∈ {+3/2,+1/2,−1/2,−3/2}`. The **³¹P resonance
splits into a 1:3:3:1 quartet** spaced by J; each **¹H line is a doublet split by J**
(coupled to the single ³¹P). For trimethyl phosphate the nine OCH₃ protons are all
3-bond equivalent to ³¹P → the ³¹P line is a **1:9:36:84:126:126:84:36:9:1 decet**
(10 lines) spaced by ³J(P,H), and the ¹H line is a **doublet** split by the same ³J.
This decet/doublet pattern *is* the entire low-field spectrum and it is a clean,
closed-form classical fit target.

### 1.3 What the low-field spectrum looks like — numbers

Representative molecules and their literature J values:

| Molecule | Spin pair | Coupling | J (Hz) | Source |
|---|---|---|---|---|
| Trimethyl phosphate (MeO)₃P=O | ³J(³¹P,¹H) (P–O–C–H) | 3-bond | **10.4 ± 0.6** | McDermott SQUID @ 4.8 µT; Glover/Appelt EF-NMR |
| Trimethyl phosphite (MeO)₃P | ³J(³¹P,¹H) | 3-bond | **~10.5–11** | ZULF organophosphorus (PMC7877728) |
| Phosphorous acid / phosphonates H–P | **¹J(³¹P,¹H)** (direct P–H bond) | 1-bond | **500–700** | textbook ³¹P NMR; LibreTexts 9.10 |
| Fluorophosphate / R–O–PF₂ etc. | ¹J(³¹P,¹⁹F) | 1-bond | **~900–1400** | organophosphorus ³¹P/¹⁹F NMR |

**Spectrum for trimethyl phosphate at B₀ = 50 µT:** a ¹H line at ~2129 Hz split into a
**doublet, spacing 10.4 Hz**; a ³¹P line at ~862 Hz split into a multiplet, spacing
10.4 Hz. The chemically interesting number is just that one splitting, ~10 Hz, sitting
on a ~2.13 kHz carrier. The *direct-bond* couplings (¹J P–H ≈ 500–700 Hz, ¹J P–F ≈
1 kHz) are huge and trivially resolvable — but those molecules (e.g. dimethyl phosphite,
which has both a 700 Hz ¹J(P–H) AND a ~10 Hz ³J(P–OCH₃)) are the **best targets**
because the large ¹J is unmissable even on a noisy rig and doubles as a built-in
sanity/calibration line.

### 1.4 Linewidth / T2* requirement — the load-bearing number

To resolve a doublet of spacing J you need full-width-half-max linewidth
`Δν_½ ≲ J/2` (Rayleigh-ish; J/3 to be comfortable). Linewidth ties to coherence by
`Δν_½ = 1/(π T2*)`.

| Target coupling | J (Hz) | Required Δν_½ (≈J/3) | Required T2* = 1/(π Δν_½) |
|---|---|---|---|
| ³J(P,OCH₃), TMP | 10.4 | ~3.5 Hz | **~0.09 s** |
| 2J/3J generic "10–20 Hz" | 10–20 | ~3–7 Hz | **~0.05–0.10 s** |
| ¹J(P–H) direct bond | ~600 | ~200 Hz | ~1.6 ms (trivial) |
| ¹J(P–F) | ~1000 | ~300 Hz | ~1 ms (trivial) |

**This is the decisive finding: resolving a ~10 Hz heteronuclear J needs only
T2* ≳ 0.1 s and field homogeneity good enough for ~3 Hz linewidth (≈ a few ppm
of 2 kHz, i.e. ~1.5 nT absolute over the sample).** That is a *spectacularly* loose
requirement compared to resolving chemical shift (which needed T2* > 15 s and < 1 ppb).
Earth-field water routinely shows T2* ≈ 0.1–1 s on hobby rigs → Δν_½ ≈ 0.3–3 Hz. A
**3 Hz linewidth resolves a 10 Hz J; a 1 Hz linewidth resolves it cleanly.** The DIY
linewidth budget is met by the pyppm/RowleyLab class with ordinary Helmholtz B₀
trimming, **no µ-metal shield required for first light**, no superconducting magnet,
no lab.

### 1.5 Can the actual cataloged hardware reach it?

- **pyppm / RowleyLab EF-NMR (~$300–500).** This is a *coil-detected* (Faraday pickup),
  not NV-detected, instrument. Published EF-NMR rigs of exactly this class have resolved
  the ~10 Hz ¹H–³¹P J of trimethyl phosphate (Glover/Appelt EF-NMR C-NOT paper;
  Callaghan-type Terranova/TeachSpin EF-NMR teaching kits). T2* ≈ 0.5–1 s is standard
  for water-based EF-NMR with a homemade Helmholtz B₀ cage. **It reaches the ~0.1 s /
  3 Hz target with margin.** This is the recommended transducer. SNR is solved by the
  same trick as the NV deep-dive: a cheap ~0.3–1 T NdFeB **prepolarizer** (the S1
  load-bearing component), giving the standard ~10⁴ Boltzmann gain over Earth-field
  equilibrium. Coil detection of a prepolarized mL sample at 2 kHz is the *original,
  routine* EF-NMR mode — not the hard nT-standoff regime of the NV fusion.
- **UncutGem-class NV (~$100–200).** Per DEEPDIVE-nv-efnmr §1, a broad-CW hobby NV does
  NOT see a bare proton FID at mm standoff (~2 pT Earth-pol; ~20 nT–1.6 µT only with a
  0.5–1 T prepolarizer + favourable geometry). NV adds *nothing* for a bulk-J chemistry
  measurement — it is a strictly worse B-transducer than a tuned pickup coil at 2 kHz
  (NOVEL-COMBO-MENU Tier-X "Rydberg-EIT optical NMR" lesson generalizes: don't substitute
  a worse transducer). **The NV path is recommended ONLY if the deliverable is
  explicitly "NV-detected", i.e. tied to the separate S1 NV-NMR artifact; for the
  chemistry result, use the coil-detected EF-NMR rig.** Frequency *resolution* (the
  linewidth that resolves J) is set by B₀ homogeneity and T2*, identical for both
  transducers; the NV only changes SNR/standoff, and changes it for the worse here.

## 2. The chemistry payoff — is J actually a useful electronic-structure observable?

### 2.1 The physics of J → electronic structure (this part is solid)

The scalar coupling decomposes (Ramsey) into Fermi-contact (FC), spin-dipolar (SD),
paramagnetic spin-orbit (PSO) and diamagnetic spin-orbit (DSO) terms. For couplings
involving ¹H (and dominantly for ¹J(P,H)/¹J(P,F) one-bond couplings), the **Fermi-contact
term dominates**. FC is an *operator that samples the wavefunction amplitude at the
nuclei*:

```
J_FC ∝ γ_A γ_B · |ψ(r_A)|² · |ψ(r_B)|² · (s-character of the A–B bond) · (1/ΔE)
```

i.e. it is proportional to the **s-electron density at both coupled nuclei** and to the
**s-character of the hybrid orbitals forming the bond** (only s orbitals have non-zero
amplitude at the nucleus). This is genuine, well-established electronic-structure physics
— the Muller–Pritchard / Bent's-rule relation `¹J ∝ %s-character` is standard
(LibreTexts; Kwan Chem 117 notes; the P-coordination re-hybridisation result in the RSC
manuscript C4CC06094F: P–H s-character rises on going to tetrahedral P, ¹J(P,H) rises
correspondingly). So **yes — a measured one-bond J carries a quantitative statement
about bond hybridization / s-density at the nuclei.** It is not a tenuous analogy; the
coupling *is* an electron-mediated observable of the molecular wavefunction.

### 2.2 The honest part — is *measuring it on this rig* actually wanted?

This is where intellectual honesty bites, and the answer is **mixed, leaning weak**:

1. **The number is already known to higher precision.** ³J(P,H) of trimethyl phosphate =
   10.4 ± 0.6 Hz has been measured by SQUID-NMR and EF-NMR (and to ±0.05 Hz on any
   benchtop). ¹J(P,H) of phosphonates is textbook. Re-measuring it on a DIY rig **does
   not produce a new chemistry number** — it reproduces a known textbook value. By the
   QCHEM-COMBO-C rubric's own "classical/known-beats-it ⇒ U≤2" rule, a *bare
   re-measurement* of a tabulated J is U≈2, not U≈4.

2. **The s-character extraction is a one-parameter inversion of a known correlation,
   not a measurement of hybridization.** You measure J, then *invoke* a literature
   `J ↔ %s` regression to *report* a hybridization. The hybridization is not
   independently observed — it is back-computed through a calibration curve that itself
   came from quantum chemistry + reference molecules. So the deliverable "we measured the
   P–H bond is X% s-character" is **a derived quantity riding on an external model**, not
   a primary observable. Honest framing: the rig measures **J**; everything past that is
   interpretation borrowed from DFT.

3. **What a DFT/coupled-cluster calculation gives instead.** Modern DFT (GGA + exact HF
   exchange, e.g. specialized J functionals) predicts FC-dominated one-bond couplings to
   **σ ≲ 2 Hz (≲ 7 Hz worst-case before linear-regression correction)** (PMC4218771).
   Coupled-cluster (CCSD/CC3 with FC + SD + SO and tight s-augmented basis) does
   ¹J(C,H)/¹J(P,H) to within a few Hz of experiment. **A laptop DFT job predicts the same
   J the DIY rig would measure, to comparable or better accuracy, in minutes, for $0.**
   The rig does *not* beat the classical electronic-structure calculation for the number
   itself.

4. **Where there IS genuine value (the salvage).** The defensible deliverable is **not**
   "we extracted s-character." It is the **closed loop**: *predict J ab initio (DFT/CC)
   → measure the same J on a $400 home-built quantum sensor → agreement validates that
   the FC mechanism and the rig both work end-to-end on a real molecule.* That is a real,
   non-trivial, mechanism-faithful artifact: an experimental electronic-structure
   datum produced by a DIY instrument, cross-checked against first-principles theory.
   The value is **pedagogical / instrumental / "DIY quantum-sensor produces a real
   electronic-structure measurement that agrees with theory"**, not **"new chemistry
   knowledge."** This is exactly the QCHEM-COMBO-C editorial's own honest framing
   ("a laptop cannot produce an *experimental* J-coupling") — and that framing survives,
   but U should be **3, not 4**: it is a real measurement, but of a known quantity, whose
   only edge over the laptop is that it is *empirical* rather than *computed*.

> **Honest chemistry verdict:** J is a *bona fide* FC/s-character electronic-structure
> observable (§2.1 solid). But measured on this rig it **reproduces a known textbook
> number that a laptop DFT job predicts to ≲2 Hz for free**. The "s-character" output is
> a model-mediated re-expression, not an independent measurement. Net usefulness is
> **U≈3**: a genuine end-to-end experimental electronic-structure datum from a DIY
> quantum sensor, valuable as a validated artifact and theory cross-check, **not** as
> new chemical knowledge. The rubric's #1 score of U=4 was half a point optimistic.

## 3. Prior art

(arXiv MCP stale per project standing note; all checks via WebSearch 2026-05-17, URLs cited.)

### 3.1 Earth-field NMR heteronuclear J-spectroscopy — PUBLISHED, and the EXACT molecule

- **Glover / Appelt et al., "NMR Spectroscopy of a ¹H–³¹P Heteronuclear System in the
  Earth's Field: Spinor Properties and Demonstration of a Quantum Computing C-NOT Gate."**
  This is **the precedent that does almost exactly the proposed experiment**: trimethyl
  phosphate, ¹H–³¹P, in Earth's field, resolving the ~10 Hz ³J(P,H) splitting, with
  low-cost EF-NMR equipment. (academia.edu/109602269 ; ScienceDirect S1090780709001621
  / *J. Magn. Reson.* 200 (2009) 88, "Quantitative analysis of Earth's field NMR spectra
  of strongly-coupled heteronuclear systems"; PubMed 19596600.) It explicitly states
  trimethyl phosphate is "a convenient heteronuclear system for experiments with low-cost
  Earth's Field NMR equipment, illustrating J-coupling." **The exact molecule, exact
  spin pair, exact ~10 Hz observable, on exactly the low-cost EF-NMR class, is already
  published.**
- McDermott et al. — ³J(³¹P,¹H) = 10.4 ± 0.6 Hz of trimethyl phosphate by **SQUID NMR at
  4.8 µT** (the canonical ultralow-field heteronuclear-J number this protocol would
  reproduce).
- Earth-field NMR J-spectroscopy generally: standard (TeachSpin/Terranova teaching kits;
  ScienceDirect "Earth's Field Spectroscopy"; PubMed 22595293, carried from
  QCHEM-COMBO-C).

### 3.2 Zero- to ultralow-field (ZULF) NMR J-spectroscopy — A MATURE FIELD

The Budker–Blanchard–Pines ZULF program is the canonical, mature prior art for using
**J-coupling as the entire spectroscopic observable in the absence of chemical shift**:

- Blanchard & Budker, *Zero- to Ultralow-Field NMR*, eMagRes (2016) — foundational
  review (onlinelibrary.wiley.com/doi/10.1002/9780470034590.emrstm1369; Semantic Scholar
  7ac337de). ZULF "permits particularly high-resolution measurement of spin–spin
  couplings due to high absolute field homogeneity and absence of CSA / susceptibility
  gradients" — i.e. *the entire premise of this candidate is the ZULF thesis statement*.
- Tayler et al., "ZULF NMR J-spectroscopy with **commercial atomic magnetometers**,"
  arXiv:1911.07554 / PubMed 32298993 — J-spectra of [¹³C]-formic acid, glycine,
  fumarate, glucose with prepolarized samples. Standard, reproducible.
- **Zero-Field NMR J-Spectroscopy of Organophosphorus Compounds**, *J. Phys. Chem.
  Lett.* (2021), PMC7877728 / pubs.acs.org/10.1021/acs.jpclett.0c03532 — **³¹P-containing
  organophosphorus J-spectra at zero field, including trimethyl phosphite (³J ≈ 10.5–11
  Hz).** Directly overlapping target chemistry, already done at zero field.
- Zero-field J-spectroscopy of quadrupolar nuclei, *Nat. Commun.* (2024)
  s41467-024-48390-2; ZULF of exchanging systems s41467-019-10787-9. Field is active and
  mature.

### 3.3 NV-detected J-coupling — PUBLISHED (and it's the SAME molecule again)

- **Glenn et al., "High-resolution magnetic resonance spectroscopy using a solid-state
  spin sensor," *Nature* 555, 351 (2018)** (nature.com/articles/nature25781). NV-ensemble
  + synchronized readout (CASR), ~1 Hz resolution in ~10 pL — and the search-confirmed
  demonstration molecule **resolves the ¹H–³¹P J-coupling of trimethyl phosphate**. The
  NV-detected version of this exact measurement is *also* already published.
- Smits/Bucher microfluidic NV-NMR 2D, *Sci. Adv.* 5, eaaw7895 (2019); review PMC9301930
  ("Hz linewidths resolving J-couplings and chemical shifts in pL volumes"); high-field
  NV J-coupling PRR 6, 043017 / arXiv:2311.11880.
- These are **lab** instruments (engineered diamond, confocal/shielded, often a several-T
  bias for the *NV* readout), not a $200 hobby NV — but the *concept* "NV resolves the
  TMP ¹H–³¹P J" is occupied.

### 3.4 DIY / amateur EF-NMR rigs — the hardware exists and is open-source

- **pyppm** (github.com/geekysuavo/pyppm; opensourceimaging.org; Hackaday 1376) — single-
  board open-source EF-NMR spectrometer; PyPPMv2 adds adiabatic prepolarization "required
  to perform more complex NMR experiments." USB, Python API.
- **RowleyLab/EF-NMR** (github.com/RowleyLab/EF-NMR; rowleylab.github.io/EF-NMR) — open
  hardware+software EF-NMR spectrometer; RowleyLab also forks pyppm.
- Low-cost low-field NMR/MRI review PMC7538153. The DIY rig is real, documented, and in
  the project's own catalogued survey.

### 3.5 What is standard vs. what (if anything) is novel in THIS framing

| Element | Status |
|---|---|
| Chemical shift dead at Earth field; J field-independent | **Standard / textbook** |
| Earth-field heteronuclear ¹H–³¹P J-spectroscopy of **trimethyl phosphate** | **PUBLISHED** (Glover/Appelt; *J. Magn. Reson.* 200, 88) |
| ZULF J-spectroscopy as the whole observable, incl. **organophosphorus** | **PUBLISHED & MATURE** (Budker/Blanchard; PMC7877728) |
| NV-detected J-coupling of trimethyl phosphate | **PUBLISHED** (Glenn *Nature* 2018) |
| J → Fermi-contact → s-character interpretation | **Standard textbook chemistry** (Bent's rule / Muller–Pritchard) |
| Open-source DIY EF-NMR hardware (pyppm/RowleyLab) | **EXISTS, open-source** |
| Running a **specifically sub-$500 DIY rig** as a deliberate *electronic-structure* probe (J→s-character), framed as a chemistry deliverable | Narrow, **largely occupied**: the measurement is the published Glover/Appelt EF-NMR experiment; the only unclaimed slice is the *framing/price-point/pedagogical packaging*, **not new physics or a new number** |

**Bottom line on novelty:** essentially every component — and the *specific
end-to-end experiment on the specific molecule* — is published. EF-NMR ¹H–³¹P J of
trimethyl phosphate (Glover/Appelt) and NV-detected ¹H–³¹P J of trimethyl phosphate
(Glenn *Nature* 2018) **both already exist**. ZULF organophosphorus J-spectroscopy is a
mature subfield. The novelty here is **N≈2 at most**, not the N=3 the rubric assigned:
the only thing without a located exact precedent is the *cheap-rig-as-chemistry-deliverable
framing*, which is a packaging claim, not a scientific contribution. Mechanism-faithful
is genuinely **5** (the spins literally are the molecule's nuclei — no analogy gap, the
one unambiguous strength).

## 4. Protocol

The physics validates; the novelty does not. The protocol below is therefore written as
an **honest validated-instrument / theory-cross-check artifact**, NOT as a novelty claim.

### 4.1 Molecule choice — recommended: dimethyl phosphite (MeO)₂P(O)H

Rationale: it carries **two** couplings on one cheap sample:
- **¹J(³¹P,¹H) ≈ 690 Hz** (direct P–H bond) — huge, unmissable even on a noisy rig,
  serves as a self-calibrating sanity line and a strong-coupling test.
- **³J(³¹P,¹H) ≈ 10–12 Hz** (P–O–C–H, to the OCH₃) — the ~10 Hz target that exercises
  the linewidth requirement.
Fallback / simplest: **trimethyl phosphate** (single ³J ≈ 10.4 Hz, the published
Glover/Appelt system — use it precisely *because* it is the validation benchmark).

### 4.2 Hardware (coil-detected EF-NMR — NOT NV)

| Item | Spec | Cost |
|---|---|---|
| EF-NMR rig | pyppm v2 or RowleyLab/EF-NMR (B₀ Helmholtz cage, pickup coil, prepolarize coil, USB DAQ, Python API) | $300–500 |
| Prepolarizer | ~0.3–1 T NdFeB stack/Halbach (Boltzmann ×10⁴ gain — load-bearing, per S1) | $30–200 |
| Fast-discharge switch | MOSFET H-bridge + freewheel, <1 ms B_p shutoff (ScienceDirect S109078071730157X) | $30–60 |
| Sample | ~5 mL neat dimethyl phosphite or trimethyl phosphate (no deuteration needed) | <$20 |
| B₀ trim | tune f_L OUT of the 50/60 Hz mains-harmonic forest (e.g. B₀ → 47 µT ⇒ f_L ≈ 2.00 kHz) | (in kit) |
| NV path | **Not recommended** for the chemistry result (§1.5). Use only if the deliverable is explicitly "NV-detected", tying to the separate S1 NV-NMR artifact | — |
| **Total** | | **≈ $360–780** |

### 4.3 Acquisition sequence

1. Prepolarize sample in the NdFeB field (T1 ≈ 1–3 s; dope ~10–20 mM CuSO₄-equivalent
   only if a faster duty cycle is needed — does not change J).
2. Non-adiabatic / fast-discharge shutoff of B_p (<1 ms) → coherent transverse
   magnetization precessing in the trimmed Earth field B₀ (~50 µT, f_L ≈ 2.0 kHz).
3. Record the FID on the pickup coil for ≥ 1 s (need T2* ≳ 0.1 s → linewidth ≲ 3 Hz; the
   rig delivers 0.3–3 Hz routinely).
4. Average N shots for SNR (prepolarized mL sample at 2 kHz is the *routine* EF-NMR
   regime — coil SNR is not the bottleneck here, unlike the NV fusion).
5. FFT → spectrum: a ~2.0 kHz ¹H line split into a **doublet at ³J ≈ 10 Hz** (and, for
   dimethyl phosphite, an additional **¹J ≈ 690 Hz** large splitting).

### 4.4 Classical spin-Hamiltonian fit (the "computation" half)

Model: weak-coupling heteronuclear Hamiltonian of §1.2,
`H/h = ν_H Î_z + ν_P Ŝ_z + J Î_z Ŝ_z` (extend to Σ over equivalent protons for the
AX₃/AX₉ multiplet). Free parameters: {ν_H, ν_P, J, Δν_½ (Lorentzian linewidth),
amplitude, phase}. Fit by non-linear least squares (a 30-line scipy job) to the complex
FID or magnitude spectrum. **Deliverable J with uncertainty: target ±0.5–1 Hz**, which
on a clean ~1 Hz-linewidth rig is achievable for the ~10 Hz coupling.

### 4.5 The theory cross-check (the part that gives this any value)

*Before* the experiment, compute J ab initio: a DFT J-coupling job
(B3LYP/PBE0 + a J-optimized basis, FC+SD+SO terms; or CCSD if feasible) on the chosen
molecule — minutes on a laptop, predicts ³J(P,H) and ¹J(P,H) to ≲ 2–7 Hz (PMC4218771).
**Success criterion:** measured J agrees with the DFT-predicted J within combined
uncertainty (rig ±0.5–1 Hz, DFT ±2–7 Hz), AND with the published 10.4 ± 0.6 Hz (TMP).
That closed loop — *theory predicts → DIY quantum sensor measures → they agree* — is the
entire, honest, deliverable. It is a validated-instrument result, not a discovery.

## 5. Verdict

### **VERDICT: NEEDS-MODIFICATION** — physics fully validated; novelty refuted; reframe as a validated-instrument / theory-cross-check artifact, not a chemistry discovery.

**What validates (numbers):**
- Chemical shift IS dead at Earth field: full ¹H shift range ≈ **21 mHz** at f_L ≈ 2.13 kHz;
  needs T2* > 15 s / < 1 ppb — impossible on DIY. Confirmed.
- Scalar J **is field-independent** (no B₀ in the `2πJ Î·Ŝ` term; Hahn–Maxwell). Confirmed
  textbook.
- **The load-bearing number:** resolving a ~10 Hz heteronuclear J needs only linewidth
  **Δν_½ ≈ 3 Hz ⇒ T2* ≳ 0.1 s** — *spectacularly* loose. EF-NMR water routinely gives
  T2* ≈ 0.1–1 s ⇒ Δν_½ ≈ 0.3–3 Hz. **A pyppm/RowleyLab-class rig (~$360–780 with a
  prepolarizer) reaches this with margin.** A bare UncutGem NV does **not** help (worse
  B-transducer at 2 kHz than a tuned pickup coil; SNR-bound, not resolution-bound).
- J → Fermi-contact → s-character is **genuine** electronic-structure physics
  (mechanism-faithful = 5; the spins literally are the molecule's nuclei).

**What fails (why NEEDS-MODIFICATION, not VALIDATED):**
- **Novelty is N≈2, not 3.** Earth-field ¹H–³¹P J of *trimethyl phosphate* on low-cost
  EF-NMR is **already published** (Glover/Appelt, *J. Magn. Reson.* 200 (2009) 88).
  NV-detected ¹H–³¹P J of the same molecule is **already published** (Glenn, *Nature*
  555, 351 (2018)). ZULF organophosphorus J-spectroscopy is a **mature subfield**
  (Budker/Blanchard; PMC7877728). The only unclaimed slice is the cheap-rig *framing* —
  packaging, not science.
- **Usefulness is U≈3, not 4.** The measured J reproduces a textbook value
  (10.4 ± 0.6 Hz) that **laptop DFT predicts to ≲ 2 Hz for free**. The "s-character"
  output is a model-mediated re-expression via a borrowed `J↔%s` regression, not an
  independent measurement. The only real edge over the laptop is that the datum is
  *empirical*, not *computed*.
- Revised score: **N2 · B5 · U3 · Mech5** → product ≈ **30** (down from the rubric's 60;
  honest, build-real). Still the top *hardware* quantum-chemistry candidate by
  buildability + mechanism-faithfulness, but the headline must change.

**The salvage (the modification):** do NOT pitch this as novel chemistry or as an
s-character measurement. Pitch it as: *a $360–780 home-built quantum sensor produces a
real, end-to-end experimental electronic-structure observable (a Fermi-contact J-coupling
of a real molecule) that agrees with a first-principles DFT prediction and the published
ZULF/EF-NMR literature.* That is a legitimate, mechanism-faithful, reproducible artifact
— a DIY-quantum-sensor validation result and theory cross-check — just not a discovery.
Recommended molecule: **dimethyl phosphite** (¹J ≈ 690 Hz self-calibration line +
³J ≈ 10–12 Hz resolution test); fallback **trimethyl phosphate** (the published 10.4 Hz
benchmark). Expected spectrum: ~2.0 kHz ¹H line, **doublet split by ³J ≈ 10 Hz**
(+ 690 Hz ¹J for dimethyl phosphite). Fit a 6-parameter weak-coupling spin Hamiltonian;
deliver J ± 0.5–1 Hz.

**One-line:** the physics is real and the rig genuinely reaches it (T2* ≳ 0.1 s resolves
a ~10 Hz J — easy), but the experiment and the molecule are already in the literature on
this exact hardware class, so it lands as a validated-instrument / theory-cross-check
artifact (U≈3, N≈2), not the novel chemistry deliverable the rubric implied.

---
*Generated 2026-05-17. Spin Hamiltonian worked from first principles; prior art from
WebSearch (arXiv MCP stale per project standing note). J/linewidth numbers are
order-of-magnitude design targets with cited literature anchors.*
