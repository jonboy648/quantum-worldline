# DEEP-DIVE: Radical-Pair-Gated NV Relaxometry

**Source proposal:** `NOVEL-COMBO-B-physics-method.md`, candidate #1 (N5 B4 U5 = 100)
**Date:** 2026-05-16
**Owner:** physics deep-dive agent
**Status:** COMPLETE — verdict REFUTED

The claim under test: a shallow NV center reads out the field-dependent
singlet-triplet interconversion of a chemically-specific radical pair via
T1 relaxometry, turning a non-selective spin-noise sensor into a
molecule-specific magnetometer whose selectivity axis is the radical's
own hyperfine fingerprint (the MFE B-half / low-field-effect structure).

---

## 1. Spin Hamiltonian and the T1 coupling mechanism

### 1.1 Radical-pair Hamiltonian

Two correlated S=1/2 electron spins **S₁**, **S₂** (e.g. flavin
semiquinone FAD•⁻ and tryptophan TrpH•⁺), each hyperfine-coupled to a
set of nuclei **I**_k, in an applied field **B₀**:

```
H_RP = ω_1·S₁z + ω_2·S₂z                      (electron Zeeman, ω = gμ_B B₀/ħ)
     + Σ_k S₁·A₁k·I_k + Σ_m S₂·A₂m·I_m         (hyperfine, tensors A)
     + S₁·D·S₂ + J(r) S₁·S₂                     (dipolar + exchange e-e coupling)
```

with the recombination (Haberkorn) terms making it open:
`dρ/dt = -i[H_RP,ρ] - (k_S/2){Q_S,ρ} - (k_T/2){Q_T,ρ}`, where Q_S, Q_T
are singlet/triplet projectors and k_S, k_T the spin-selective
recombination rates.

**Key scales (flavin–tryptophan, the canonical well-characterized
model dyad — Kattnig/Hore, PCCP 2019, 10.1039/c9cp01916b):**

- Effective hyperfine `a_eff ≈ 0.5–1.5 mT` → in frequency,
  `ω_HFC = γ_e·a_eff ≈ 2π × (14–42 MHz)` (γ_e = 28 GHz/T).
- Electron Zeeman at Earth field (50 µT): `ω_Z ≈ 2π × 1.4 MHz`;
  at a deliberate bias of 1–30 mT: `2π × 28–840 MHz`.
- Exchange/dipolar `J, D`: 0.1–10 mT depending on radical separation
  (≈1–2 nm in a tethered dyad).
- Singlet–triplet interconversion frequency
  `ω_ST ≈ √(ω_HFC² + (Δg μ_B B₀/ħ)²) ≈ 2π × 10–100 MHz`.
- Radical-pair lifetime τ_RP: **1 ns** (ultrafast flavin/Trp,
  PMC7301759) up to **~1 µs** (engineered/cryptochrome-mimic,
  spin-relaxation-limited).

The magnetic-field effect (MFE): the singlet recombination yield
Φ_S(B₀) changes by a few % to ~30 % over 0→a few mT, with the
characteristic **B₁/₂ ≈ a_eff** and a low-field-effect (LFE) dip. This
B-dependence *is* the chemical fingerprint — a_eff is molecule-specific.

### 1.2 NV ground-state Hamiltonian and T1 channel

NV ground triplet (S=1):

```
H_NV = D_gs S_z² + γ_e B₀ S_z + ...     (D_gs = 2π × 2.87 GHz)
```

Longitudinal relaxation between m_s=0 and m_s=±1 is driven by
**transverse magnetic noise resonant at the NV Larmor / transition
frequency**. The Fermi-golden-rule rate:

```
1/T1 ≈ (3 γ_e² / 2) · S_B⊥(ω_NV)
```

where S_B⊥(ω_NV) is the one-sided spectral density of the magnetic
field transverse to the NV axis, evaluated at the relevant transition
frequency ω_NV. Two operating regimes:

- **Zero/low bias:** the m_s=0↔±1 splitting is the zero-field
  splitting, ω_NV = D_gs = 2π × 2.87 GHz.
- **Biased to "tune down":** applying B₀ along the NV axis the
  0↔−1 gap is `D_gs − γ_e B₀`. To bring ω_NV down to the radical
  S-T band (~10–100 MHz) requires γ_e B₀ ≈ D_gs, i.e.
  **B₀ ≈ 102 mT (the NV GSLAC)**. Near the ground-state
  level-anticrossing the 0/−1 states mix and the NV becomes sensitive
  to ~MHz–tens-of-MHz noise. This is the *only* regime where the NV
  Larmor frequency overlaps the radical S-T mixing band.

### 1.3 The coupling mechanism (the crux)

A radical electron spin at distance r from the NV produces a dipolar
field of RMS magnitude

```
B_rad ≈ (μ_0/4π) · (g μ_B / r³)
```

≈ **2.8 µT at r = 5 nm**, ≈ 0.35 µT at 10 nm, ≈ 22 nT at 20 nm
(∝ 1/r³, single spin). For the radical pair to inject *T1 noise* it
must fluctuate at ω_NV. The fluctuation spectrum of a single radical
spin is a Lorentzian centered at 0 (or at its own Larmor) with width
set by its correlation time τ_c = min(τ_RP, T1_rad, τ_tumble):

```
S_B(ω) ≈ B_rad² · (2 τ_c) / (1 + (ω τ_c)² )
```

**The chemical gate.** The radical *exists* only while the pair is
alive (τ_RP). Its spin furthermore *re-randomizes* its singlet/triplet
character at ω_ST, which is set by the molecule's own a_eff and by B₀.
So the spin-noise the NV sees is (i) present only when the analyte's
radical pair is photogenerated (chemical ON/OFF gate), and (ii)
carries spectral weight at ω_ST(B₀) = the hyperfine fingerprint. As B₀
is swept, the NV 1/T1 shows resonant enhancement when **ω_NV(B₀)
overlaps ω_ST(B₀)** — and the field at which that happens is fixed by
a_eff, which differs molecule-to-molecule. That is the claimed
molecule-selective magnetometer.

**The structural problem already visible here.** Sweeping B₀ moves
*both* ω_NV and ω_ST. ω_NV needs B₀ ≈ 102 mT (GSLAC) to reach the
10–100 MHz band. But at 102 mT the radical electron Zeeman
(γ_e·102 mT = 2π × 2.86 GHz) totally dominates a_eff (≤ 2π × 42 MHz):
the singlet–triplet mixing is **quenched** by the high field (this is
exactly why the MFE *saturates* above ~10 mT — the high-field limit of
the radical-pair mechanism). At the field needed to make the NV
listen, the chemistry that carries the fingerprint is turned off. The
two resonance conditions are mutually exclusive across most of the
useful range. Quantified in §2.

## 2. Quantitative feasibility

### 2.1 Signal: fractional change in 1/T1

Baseline shallow-NV T1 ≈ 1–5 ms (surface-limited; bulk can reach
ms–s). Take T1₀ = 2 ms → 1/T1₀ = 500 s⁻¹.

A single radical at r with correlation time τ_c contributes
`Δ(1/T1) ≈ 3γ_e² · B_rad²(r) · τ_c / (1+(ω_NV τ_c)²)`. The radicals
only inject noise efficiently when `ω_NV τ_c ≲ 1`. With τ_c ≈ τ_RP and
two regimes:

- **τ_RP = 1 µs, ω_NV at GSLAC tuned to ~5 MHz:** ω_NV τ_c ≈ 30 →
  the (1+(ωτ_c)²) denominator is ~900, killing 99.9 % of the noise
  power. Effective.
- **τ_RP = 1 ns (realistic fast flavin/Trp):** ω_NV τ_c ≈ 0.03 →
  matched, BUT then B_rad² τ_c is tiny because τ_c is 1 ns.

Take the **optimistic** case: a long-lived (τ_RP = 1 µs) cryptochrome-
mimic dyad, single radical at r = 5 nm, NV biased near GSLAC so
ω_NV ≈ 2π × 5 MHz (ω_NV τ_c ≈ 31):

```
Δ(1/T1) ≈ 3 · (1.76e11)² · (2.8e-6 T)² · (1e-6 s) / (1 + 31²)
        ≈ 3 · 3.1e22 · 7.8e-12 · 1e-6 / 962
        ≈ 7.5e5 / 962 ≈ 780 s⁻¹  per radical, instantaneous.
```

But the radical is only present a fraction `f = τ_RP / T_cycle` of the
time (photo-cycle: generate, decay, regenerate). With pump cycling at
~10⁵–10⁶ s⁻¹ and τ_RP = 1 µs, duty f ≈ 0.1–1. Time-averaged single-
radical contribution ≈ 78–780 s⁻¹, i.e. **fractional Δ(1/T1)/(1/T1₀)
≈ 0.15–1.5 per radical at 5 nm.** That is a large, easily detectable
signal — *if* a single radical sits 5 nm from the NV with τ_RP = 1 µs.
Realistically you place an ensemble of ~10–100 tethered dyads in the
near field of the NV (within ~15 nm shell), each contributing ∝1/r⁶ in
rate. The 1/r⁶ weighting means the closest 1–3 radicals dominate.

**Net: signal is not the problem in the optimistic regime.** Required
"concentration" is essentially *one* well-placed long-lived radical
pair within 5 nm. As a bulk concentration that near-field shell
(volume ~4 nm³ effective for the dominant 1/r⁶ weight, ~10⁴ nm³ for
the full 15 nm sphere) needs ~1 radical per 10⁴ nm³ ≈ **0.17 mM**
*time-averaged radical population* — but because τ_RP/T_cycle ≪ 1 for
short-lived pairs, the *precursor* (flavin dye) concentration must be
~10²–10⁴× higher, i.e. **0.1–1 M of photoactive dye tethered at the
surface** to keep one radical alive in the near field at all times.
That is a dense, essentially close-packed surface monolayer — feasible
as a SAM but not as a dilute analyte. **This kills the "single named
analyte molecule at sub-attomole" selling point**: you need a packed
layer of the reporter dye, not detection of a trace analyte.

### 2.2 The hardest obstacle, with numbers (the killer)

**Frequency mismatch between the NV listening band and the radical
S-T band, compounded by high-field MFE quench.**

- NV T1 noise band: ω_NV = D_gs = 2π × 2.87 GHz at zero bias.
  Radical S-T noise sits at ω_ST = 2π × 10–100 MHz. The overlap of
  S_B(ω) (Lorentzian, width 1/τ_c ≈ 2π × 0.16 MHz for τ_RP=1µs, or
  2π × 160 MHz for τ_RP=1 ns) with a 2.87 GHz NV is:

  - τ_RP = 1 µs: S_B(2.87 GHz)/S_B(0) ≈ 1/(ω_NV τ_c)² ≈
    1/(2π·2.87e9·1e-6)² ≈ **3 × 10⁻⁹**. Nine orders of magnitude
    suppression. Δ(1/T1) ≈ 780 s⁻¹ × 3e-9 ≈ **2 × 10⁻⁶ s⁻¹**, i.e.
    fractional change 4 × 10⁻⁹ of 1/T1₀. Undetectable.
  - τ_RP = 1 ns: S_B(2.87 GHz) Lorentzian width 2π×160 MHz still
    rolls off as 1/(ω τ_c)²; at 2.87 GHz, (ω τ_c)² ≈ (2π·2.87e9·1e-9)²
    ≈ 325 → suppression ≈ 3 × 10⁻³. Δ(1/T1) for a 1 ns radical at
    5 nm: 3γ_e²·B_rad²·τ_c ≈ 3·3.1e22·7.8e-12·1e-9 ≈ 0.73 s⁻¹, times
    3e-3 ≈ **2 × 10⁻³ s⁻¹** → fractional 4 × 10⁻⁶. Marginal at best.

- To fix the mismatch, bias the NV to GSLAC (B₀ ≈ 102 mT) so
  ω_NV → few MHz. **But γ_e × 102 mT = 2π × 2.86 GHz acting on the
  radical electrons** drives the radical pair deep into the
  high-field MFE regime. In that regime only the Δm=0 (T₀–S) channel
  remains and the field-*dependence* (the fingerprint) is gone: the
  MFE has saturated. The B½ structure that encodes a_eff lives at
  0–~5 mT; the NV can only listen at ~102 mT. **The selectivity axis
  and the readout condition do not coexist.**

  Quantitative gap: useful chemical contrast lives in the window
  B₀ = 0–5 mT. NV needs B₀ = 97–107 mT. The required operating fields
  differ by a factor of ~20–100 and are non-overlapping. There is no
  single B₀ at which both (a) the NV T1 is sensitive to the S-T band
  and (b) the radical-pair yield still depends on a_eff.

### 2.3 Integration time / SNR for a hobby-grade NV

Even granting the optimistic τ_RP = 1 µs, r = 5 nm geometry and the
GSLAC trick, with the 3 × 10⁻⁹ frequency-overlap factor the signal is
Δ(1/T1) ≈ 2 × 10⁻⁶ s⁻¹ against 1/T1₀ = 500 s⁻¹ (fractional 4e-9).

NV relaxometry shot-noise-limited contrast δ(1/T1)/(1/T1) per sqrt-Hz:

- **Research single NV (good photon collection, η ≈ 0.05,
  C ≈ 0.3 contrast, ~10⁴ counts/s):** T1 estimate precision per shot
  ~1 %; reaching 4 × 10⁻⁹ fractional needs (1e-2/4e-9)² ≈ 6 × 10¹²
  averages. At ~1 kHz T1-sequence rate that is **~2 × 10⁹ s ≈ 60
  years.** Infeasible.
- **Hobby-grade broad-ODMR ensemble NV (UncutGem-class, ~$100):**
  ensemble (N ≈ 10⁹–10¹² NVs) gives √N sensitivity *for a bulk
  field*, but relaxometry of a *single near-field radical* does NOT
  benefit from ensemble averaging — only the few NVs within ~15 nm of
  the radical see it; the other 10¹² NVs add only background and
  photon shot noise. Effective single-NV-equivalent. Broad ODMR (no
  pulsed control, ~MHz linewidth, no clean T1 sequence) further
  degrades T1 contrast by ≈10–100×. SNR = 3 for a 4 × 10⁻⁹ fractional
  change is **not reachable in any human timescale** (>10³–10⁴ years).

Even in the "no frequency mismatch" fantasy (τ_RP and ω_NV perfectly
matched, fractional signal ~0.15/radical): a research NV reaches
SNR=3 in seconds–minutes; a hobby broad-ODMR NV in minutes–hours,
*assuming* it can do any T1 measurement at all (most ~$100
broad-ODMR boards do CW-ODMR magnetometry, not T1 relaxometry — the
$100 class typically cannot run the required pump–wait–readout
sequence with µs-resolved dark times, so in practice **a hobby NV
cannot perform this measurement even in the ideal case**).

## 3. Prior art

WebSearch (May 2026) used as the prior-art channel; arXiv MCP feed is
stale and was not relied on.

### What IS already done

1. **NV T1 relaxometry of free radicals — DONE, multiple groups.**
   Schirhagl group: detection of free-radical species (NO•, O₂•⁻)
   produced in chemical reactions under biologically relevant
   conditions via nanodiamond T1 relaxometry.
   - ACS Sensors 2021, 10.1021/acssensors.0c01037
     (https://pubs.acs.org/doi/10.1021/acssensors.0c01037)
   - PMC8651177 (https://www.ncbi.nlm.nih.gov/pmc/articles/PMC8651177/)
   - Review: *Relaxometry with NV Centers in Diamond*, Acc. Chem. Res.
     2022, 10.1021/acs.accounts.2c00520
     (https://pubs.acs.org/doi/10.1021/acs.accounts.2c00520)
   - *Diamond-Based Nanoscale Quantum Relaxometry for Sensing Free
     Radical Production in Cells*, Small 2022,
     10.1002/smll.202105750
     (https://onlinelibrary.wiley.com/doi/full/10.1002/smll.202105750)
   So: "NV reads spin noise from radicals" is established, **but
   non-selectively** — it reports total paramagnetic load, exactly as
   the proposal concedes.

2. **NV T1 of paramagnetic ions (Gd³⁺, Mn²⁺, Cu²⁺) — DONE.** Steinert
   2013 and the 2013 single-NV nanocrystal relaxometry work
   (arXiv:1304.1197, https://arxiv.org/abs/1304.1197). Non-selective.

3. **Single-molecule electron-spin detection by shallow NV — DONE.**
   *All-Optical Sensing of a Single-Molecule Electron Spin*, Nano
   Lett. 2014, 10.1021/nl502988n
   (https://pubs.acs.org/doi/10.1021/nl502988n). Establishes that a
   single surface electron spin is within NV reach at <10 nm — the
   geometric premise is sound.

4. **Radical-pair magnetoreception / MFE spectroscopy — DONE, by
   transient absorption / EPR / reaction-yield-detected magnetic
   resonance, NOT by NV.** Hore & Timmel review, Annu. Rev. Biophys.
   2016, 10.1146/annurev-biophys-032116-094545
   (https://www.annualreviews.org/content/journals/10.1146/annurev-biophys-032116-094545);
   quantum-Zeno magnetosensitivity, Nat. Commun. 2024,
   s41467-024-55124-x
   (https://www.nature.com/articles/s41467-024-55124-x);
   ultrafast flavin/Trp RP kinetics PCCP 2019, 10.1039/c9cp01916b
   (https://pubs.rsc.org/en/content/articlelanding/2019/cp/c9cp01916b);
   singlet–triplet dephasing JCP 2023, 10.1063/5.0166675
   (https://pubs.aip.org/aip/jcp/article/159/10/105102/2910503).

5. **Shallow-NV surface coherence engineering — DONE/active.**
   Coherence-protection for 1-nm-deep NV, Nat. Commun. 2025,
   s41467-025-64771-7
   (https://www.nature.com/articles/s41467-025-64771-7); diamond
   surface engineering review, J. Mater. Chem. C 2022,
   10.1039/D2TC01258H
   (https://pubs.rsc.org/en/content/articlehtml/2022/tc/d2tc01258h).

### What is NOT done (the genuine novelty claim)

- **No work uses the *field-dependence of the radical-pair lifetime/
  yield* (the MFE B½ fingerprint) as a chemical-selectivity axis of an
  NV sensor.** Searches for NV + radical-pair + MFE + selectivity
  return only the non-selective free-radical relaxometry above and the
  separate (non-NV) RP-magnetoreception literature. The *combination*
  as a selectivity mechanism is genuinely absent. The proposal's
  novelty claim survives the literature check — the idea is new.
- The novelty is real; the physics (§1–2) is what defeats it, not
  prior art.

### Adjacent caution

NV optical readout near a flavin photo-cycle: the 532 nm NV pump and
the radical pump laser, plus flavin fluorescence (~520 nm) overlapping
NV phonon-sideband collection (~650–800 nm — partially separable but
the pump is not), create a photophysical cross-talk channel not
discussed in the proposal. Not the killer, but a real systematic.

## 4. Verdict

### REFUTED (as a molecule-selective magnetometer) — with the killer number

**The killer:** the NV T1 listening frequency and the radical-pair
singlet–triplet noise band are non-overlapping, and the field that
would close that gap destroys the chemical fingerprint.

- At zero/low bias the NV listens at **ω_NV = 2π × 2.87 GHz**; the
  radical S-T noise sits at **2π × 10–100 MHz** with Lorentzian roll-
  off. Spectral overlap factor `S_B(ω_NV)/S_B(0) ≈ 1/(ω_NV τ_c)²`:
  - τ_RP = 1 µs → **3 × 10⁻⁹** (Δ(1/T1) ≈ 2 × 10⁻⁶ s⁻¹, fractional
    4 × 10⁻⁹ → SNR=3 needs >10³ years even on a research NV).
  - τ_RP = 1 ns → 3 × 10⁻³ (fractional ~4 × 10⁻⁶ → still
    impractical, and 1 ns pairs barely show an MFE).
- Tuning the NV down to the S-T band requires biasing to the GSLAC,
  **B₀ ≈ 102 mT**. That same field puts the radical electrons at
  γ_e B₀ = 2π × 2.86 GHz ≫ a_eff (≤ 2π × 42 MHz): the radical pair is
  in the **saturated high-field MFE regime where Φ_S(B₀) no longer
  depends on a_eff**. The selectivity axis (B½ structure at 0–5 mT)
  and the NV readout condition (≈102 mT) are separated by ~20–100× and
  do not coexist. There is no B₀ that satisfies both.
- Independently, the "trace single analyte at sub-attomole" claim
  fails on duty cycle: keeping one radical alive in the NV near field
  needs a **~0.1–1 M close-packed surface monolayer of the reporter
  dye**, not a dilute analyte — so even the geometric/concentration
  story is a packed-SAM reporter assay, not single-molecule chemical
  ID.
- Hobby-grade ~$100 broad-ODMR NV: cannot run the required µs-resolved
  pulsed T1 relaxometry sequence at all (CW-ODMR class), and ensemble
  averaging does **not** help a single near-field radical. Hard NO for
  the UncutGem-class device independent of the frequency-mismatch
  killer.

### Salvageable NEEDS-MODIFICATION fragment (logged, not endorsed)

A *non-selective* variant — pulsed-NV relaxometry that detects the
**presence and decay kinetics** of a photogenerated radical pair
(τ_RP) by gating the pump and watching 1/T1 transients — IS physically
sound and partly demonstrated (free-radical relaxometry, ACS Sensors
2021). One could extract a *magnetic-field-effect on τ_RP* by
repeating the τ_RP measurement at several **low** fields (0–10 mT,
NV at zero-field, reading the *envelope* not a resonance). This
recovers an MFE-of-lifetime curve and is genuinely an "optically
detected MFE via NV." But it (a) requires a research-grade pulsed NV,
(b) is not single-molecule-selective (reports the dye you put there),
and (c) the NV is then just a slow lifetime probe competing with
transient absorption, which already does this far better. Net EV: low;
not worth a build. Filed as the only non-refuted residue.

### Bottom line

The novelty claim is real (no prior art does this) but the physics
forbids the headline device. Frequency mismatch (3 × 10⁻⁹ spectral
overlap) and mutually exclusive operating fields (0–5 mT vs ≈102 mT)
are the quantitative killers. **REFUTED** as proposed; only a
non-selective, research-grade, low-value lifetime-MFE variant
survives.

---

*Deep-dive complete 2026-05-16. Prior art via WebSearch (arXiv MCP
feed stale, not used). Numbers are order-of-magnitude analytic
estimates; the two killer ratios (1/(ω_NV τ_c)² and the GSLAC-vs-B½
field separation) are robust to factor-of-a-few uncertainty.*
