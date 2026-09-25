# NOVEL-COMBO-A: Sensor-Fusion Combinations of DIY Quantum Instruments

**Framing A of 3** | Date: 2026-05-16 | Goal: novel *combinations* of already-cataloged DIY-tier
instruments that, when FUSED (emergent observable from coupling, not co-located readings),
measure something none measures alone. Constraint: sub-$5k, bench-testable in ~6 months.

**Instrument catalog drawn on:** NV-center diamond magnetometer (UncutGem, arXiv:2509.18329,
~$100); Rydberg vapor-cell electrometer (BUILD-A, ~$4.3k); Earth-field NMR (pyppm/RowleyLab,
~$300-500); optically-pumped magnetometer (OPM, software-only + QuSpin, STRETCH); single-photon
SPAD (OpenSPAD, ~$300-500); beam-splitter QRNG (~$50-200); BBO entangled-photon source (~$1.5k
STRETCH); Rb frequency standard FE-5680A (~$50-200, 1e-11).

**Prior-art tool status:** the `paper-search` arXiv MCP returned the generic latest-submissions
feed (2026-05-14 cs.CV/quant-ph posts) regardless of query across 4 attempts — keyword filtering
is broken in this environment. Stopped after the two-failure protocol. Prior-art notes below are
from established domain literature (cited in BUILD-A itself: Holloway/NIST 2014 J.Appl.Phys.
116:244101; Wieman-Hollberg 1991 RSI 62:1; NV-ODMR canon; pyppm/RowleyLab EF-NMR) plus standard
knowledge of the atomic-sensing field. Novelty scores carry this caveat.

---

## Ranked Candidates

| Rank | Combination | Emergent observable | N | B | U | Product |
|------|-------------|---------------------|---|---|---|---------|
| 1 | NV magnetometer + EF-NMR | Optically-detected proton/sample precession in Earth field (NV reads the EF-NMR FID magnetically — chemically-specific magnetometry) | 4 | 4 | 4 | **64** |
| 2 | NV magnetometer + Rb FE-5680A clock | Drift-locked absolute DC vector magnetometry (ODMR microwave frequency disciplined to 1e-11 Rb reference → ppb-stable absolute B) | 3 | 5 | 4 | **60** |
| 3 | Rydberg electrometer + NV magnetometer | Co-located full EM observable: SI-traceable E (Rydberg) + B (NV) at one point → source disambiguation / Poynting-vector & near/far-field discrimination | 4 | 3 | 4 | **48** |
| 4 | QRNG + NV magnetometer | Calibration-free stochastic-resonance readout: certified white-noise dither recovers sub-ODMR-linewidth fields and yields an absolute noise-floor reference | 4 | 4 | 3 | **48** |
| 5 | SPAD + NV magnetometer | Photon-counting shot-noise-limited ODMR: time-tagged single-photon readout of NV fluorescence → quantum-limited sensitivity + correlation spectroscopy | 3 | 4 | 4 | **48** |
| 6 | EF-NMR + Rb FE-5680A clock | Absolute proton-precession magnetometer / portable gyromagnetic comparator (γ_p·B measured against 1e-11 clock → SI-traceable B with no field calibration) | 3 | 4 | 4 | **48** |
| 7 | Rydberg electrometer + Rb FE-5680A clock | Self-calibrated absolute RF E-field & power standard (AT splitting frequency referenced to Rb clock → primary-standard traceability without a calibrated antenna) | 3 | 2 | 4 | **24** |
| 8 | BBO entangled source + SPAD + QRNG | Loophole-aware / source-monitored randomness beacon (entanglement-witnessed QRNG with live CHSH-visibility health flag) | 3 | 2 | 3 | **18** |

---

## Candidate Detail

### C1 — NV magnetometer + EF-NMR  (N4 B4 U4 = 64)
1. **Instruments:** UncutGem NV diamond magnetometer (~$100) + RowleyLab/pyppm Earth-field NMR coil+sample (~$300-500).
2. **New observable:** the proton free-induction-decay (FID) of an EF-NMR sample, *read out magnetically by the NV sensor* instead of (or alongside) the EF-NMR pickup coil. The fusion observable is a chemically/nuclear-species-specific AC magnetic signature at the Larmor frequency (~2 kHz in Earth's field) localized to the NV's ~mm sensing volume.
3. **Why it beats either alone:** EF-NMR's inductive pickup coil has volume-averaged sensitivity and 1/f and microphonic problems at the ~2 kHz proton Larmor frequency; it sees bulk magnetization only. The NV alone is a broadband DC/AC magnetometer with no chemical selectivity — it cannot tell what is producing a field. Coupled, the EF-NMR prepolarized sample *imprints a species-specific oscillating dipole* that the NV transduces optically, giving spatially-resolved, chemically-tagged magnetometry: an optically-detected NMR microscope on a hobby budget. Neither instrument produces "what nuclear species is here, and where" alone.
4. **Coupling mechanism:** prepolarize sample in the EF-NMR polarizing coil; on coil shutoff the protons precess at γ_p·B_earth (~2.0 kHz). Place the diamond <2 mm from the sample. The precessing nuclear magnetization is a real AC magnetic field at the NV; drive NV with a pulsed (CPMG/XY8) AC-magnetometry sequence with the filter notch tuned to the proton Larmor frequency. NV fluorescence contrast then encodes the FID envelope and frequency.
5. **Dominant failure mode:** the NV's intrinsic AC sensitivity (UncutGem-class, broad ODMR, no isotopic engineering) is ~µT/√Hz-class, while a prepolarized water proton signal at the diamond is ~pT–nT. Without prepolarization geometry tuned for high concentration (e.g., ferritin/contrast agent or a strong prepolarizing field >0.1 T from a cheap NdFeB stack), the proton signal is below the NV noise floor. Mitigation: use a concentrated paramagnetic-doped sample for first light; treat unambiguous *detection* (not imaging) as the milestone. Secondary: 50/60 Hz and its harmonics sit near the Larmor band — needs gradiometric NV pair or notch filtering.
6. **Cost / time:** ~$450-650 ($100 NV + $350-500 EF-NMR + shared lock-in/DAQ already in either kit). ~4-6 months: month 1-2 each instrument standalone, month 3-4 co-location + synchronized pulse timing, month 5-6 first coupled FID.
7. **First validating measurement:** prepolarize a 5 mL CuSO₄-doped water phantom; trigger NV XY8 sequence synchronized to coil shutoff; show the NV fluorescence-contrast signal oscillates at the independently-measured EF-NMR coil frequency (~2 kHz) and decays with the same T2*. Success = NV-read frequency matches coil-read frequency within 1%.
8. **Prior art:** optically-detected NMR with NV ensembles exists in research labs (micron-scale, high-field, isotopically purified diamond, shielded). A *DIY Earth-field* OD-NMR fusing a hobby NV (UncutGem) with a hobby EF-NMR rig at ~2 kHz is not something I can find a precedent for; the DIY/Earth-field regime is the novel slice. (Prior-art search tool degraded — see header caveat.)

### C2 — NV magnetometer + Rb FE-5680A clock  (N3 B5 U4 = 60)
1. **Instruments:** UncutGem NV magnetometer (~$100) + FE-5680A Rb frequency standard (~$50-200).
2. **New observable:** absolute, long-term-drift-corrected DC magnetic field. NV ODMR maps B to a microwave resonance frequency (≈2.87 GHz ± 28 GHz/T·B). Disciplining the ODMR microwave synthesizer to the Rb 10 MHz reference converts the NV from a *relative* magnetometer with synthesizer-drift-limited stability into one whose zero-field splitting readout is stable at the Rb 1e-11 level over hours-to-days.
3. **Why it beats either alone:** the NV alone is limited at long integration times not by spin physics but by the drift of the microwave source defining the ODMR frequency axis (cheap synthesizers drift 1e-7–1e-8/day → tens of nT of apparent field drift). The Rb clock alone measures nothing magnetic. Locking the NV interrogation frequency to the Rb standard removes the clock as an error term, exposing the NV's true ppb-stable Allan deviation floor for absolute DC magnetometry — a regime hobby NV rigs never reach.
4. **Coupling mechanism:** feed FE-5680A 10 MHz into the 10 MHz external-reference input of the microwave synthesizer (or a PLL/ADF435x board) that drives the NV ODMR. The ODMR center frequency is then Rb-traceable; B = (f_ODMR − D)/γ with γ and D fixed constants.
5. **Dominant failure mode:** temperature drift of the NV zero-field splitting D (~ −74 kHz/K) now *dominates* once synthesizer drift is removed — it masquerades as ~2.6 nT/K of field. Requires diamond thermometry (a second ODMR transition pair gives common-mode B / differential-mode T separation) or active temperature stabilization. Without it, the clock upgrade is wasted.
6. **Cost / time:** ~$150-300. Fast: ~2-4 months. The FE-5680A→synthesizer reference path is a cable + lock; most effort is the dual-transition temperature-compensation readout.
7. **First validating measurement:** record Allan deviation of the inferred B in a stable shielded field over 12 h, with vs without Rb discipline. Success = the Rb-disciplined trace breaks below the free-running synthesizer's drift-limited flicker floor at τ > ~100 s.
8. **Prior art:** clock-referenced microwave sources for NV are standard in metrology labs; the novelty here is modest (it is good engineering more than a new observable). Scored N3 honestly.

### C3 — Rydberg electrometer + NV magnetometer  (N4 B3 U4 = 48)
1. **Instruments:** BUILD-A Rydberg vapor-cell electrometer (~$4.3k) + UncutGem NV magnetometer (~$100). Total ~$4.4k, under $5k.
2. **New observable:** the co-located, time-synchronized E-field vector (SI-traceable, from Rydberg AT splitting) and B-field (from NV ODMR) at effectively one point in space → the local electromagnetic state, enabling Poynting-vector estimation and near-field vs far-field / capacitive vs inductive source disambiguation.
3. **Why it beats either alone:** a Rydberg cell measures only the RF E-field; an NV measures only B. An EM source's signature (a wire, an arc, a transmitter, a person-scale magnetic+electric anomaly) is ambiguous from E or B alone — same E can come from many geometries. Jointly, E/B ratio and relative phase distinguish a predominantly-electric near-field source from a radiating far-field one and constrain source impedance/orientation. This is the device-level analogue of the "Rydberg E + OPM B = source disambiguation" shape, but using a *$100 NV* in place of an OPM the user does not own.
4. **Coupling mechanism:** mount the diamond on the outer wall of the Rydberg vapor cell's RF interaction region (NV is non-perturbing to the optical EIT path — different physical channel). Common RF source drives both; cross-correlate the NV ODMR-derived B(t) against the Rydberg AT-derived E(t). The emergent quantity is the complex E/B transfer at the shared point.
5. **Dominant failure mode:** bandwidth/observable mismatch. Rydberg EIT-AT is a GHz-carrier E-field readout; the NV (UncutGem, broad ODMR) is sensitive to DC–low-MHz B, *not* 13.9 GHz. The fusion only works for the *modulation envelope* (e.g., pulsed/AM RF) common to both, or for sources with both a low-frequency magnetic component and an RF electric component. Genuine single-frequency Poynting at 14 GHz is NOT accessible — overclaiming this is the trap. Frame it honestly as envelope-level / multi-band EM source classification.
6. **Cost / time:** ~$4.4k; 16 weeks for BUILD-A + 4 weeks NV + 4 weeks fusion ≈ 6 months — at the edge of the time box and gated on BUILD-A succeeding first.
7. **First validating measurement:** drive a small loop+dipole hybrid antenna with an AM-modulated 14 GHz carrier; show the NV recovers the modulation-envelope B while the Rydberg cell recovers the carrier E, and that switching the antenna from loop-dominant to dipole-dominant changes the measured E/B envelope ratio in the predicted direction.
8. **Prior art:** combined Rydberg-E + atomic-magnetometer-B vector EM sensing is an active research idea (NIST/Army discussions of Rydberg "full-field" sensing). A *DIY* Rydberg + *hobby NV* envelope-level disambiguation rig is novel as a buildable artifact even if the concept is discussed. (Prior-art tool degraded.)

### C4 — QRNG + NV magnetometer  (N4 B4 U3 = 48)
1. **Instruments:** beam-splitter QRNG (~$100-200) + UncutGem NV magnetometer (~$100).
2. **New observable:** a calibration-free absolute noise-floor reference and sub-linewidth field recovery via *certified-entropy stochastic resonance*. The QRNG supplies a provably-white, provably-stationary dither/reference whose statistics are not a model assumption but a measured quantum certificate; injected into the NV readout it both (a) recovers signals below the ODMR linewidth via stochastic resonance and (b) yields an in-situ absolute calibration of the NV noise floor.
3. **Why it beats either alone:** stochastic resonance and noise-floor calibration normally rely on a pseudo-random or analog noise source whose whiteness/stationarity is *assumed*. A quantum beam-splitter RNG's output is certified white and bias-bounded by physics, so the recovered-signal transfer function and the noise-floor estimate become traceable rather than assumed. The NV alone has no internal absolute amplitude reference; the QRNG alone is just bits. Coupled, the QRNG becomes a metrological dither standard for the analog sensor.
4. **Coupling mechanism:** DAC-convert the QRNG bitstream into a known-variance Gaussian current through the NV bias/modulation coil (sub-threshold dither). Sub-linewidth target fields periodically cross the ODMR resonance only with the dither present; lock-in/correlate NV fluorescence against the *known* QRNG sequence to extract the buried signal and, from the residual, an absolute noise-floor number.
5. **Dominant failure mode:** stochastic resonance has a narrow optimal dither amplitude; too little gives no enhancement, too much swamps the signal and broadens the effective line. Also, QRNG → analog reconstruction introduces DAC quantization and bandwidth that can violate the very whiteness the scheme relies on — the reconstruction chain, not the QRNG, becomes the limiting "color." Must validate the analog dither spectrum independently.
6. **Cost / time:** ~$200-400; ~3-5 months (each box is near-turnkey; the fusion is firmware + DSP).
7. **First validating measurement:** apply a sinusoidal test field 6 dB below the NV ODMR-limited detection threshold; show it is undetectable without dither and recovered (SNR > 3) with QRNG dither at the predicted optimal amplitude, and that the recovered amplitude is linear in the known input.
8. **Prior art:** stochastic resonance in magnetometers is known; using a *quantum-certified* RNG specifically to make the dither (and hence the calibration) traceable, on DIY hardware, I could not find precedent for. Concept-novel, modest utility (niche). (Prior-art tool degraded.)

### C5 — SPAD + NV magnetometer  (N3 B4 U4 = 48)
1. **Instruments:** OpenSPAD single-photon detector (~$300-500) + UncutGem NV magnetometer (~$100).
2. **New observable:** photon-counting, shot-noise-limited NV magnetometry plus photon-arrival correlation spectroscopy of the NV (g²/photon-statistics-gated field readout) — replacing the UncutGem analog photodiode with time-tagged single-photon detection.
3. **Why it beats either alone:** UncutGem reads NV fluorescence on an analog photodiode whose electronic/Johnson noise sits above the photon shot-noise limit at the low photon flux of a small NV ensemble or near-single-NV. A SPAD with time tagging reaches the shot-noise floor and additionally enables photon-correlation (intensity-autocorrelation-gated) readout, which rejects background fluorescence and laser RIN that a DC photodiode cannot. The SPAD alone counts photons from nothing in particular; the NV alone is photodiode-noise-limited. Coupled = quantum-limited DIY magnetometry + correlation rejection.
4. **Coupling mechanism:** route NV 637-700 nm fluorescence to the SPAD; time-tag photon arrivals synchronized to the ODMR microwave sweep / pulsed sequence. Field is inferred from photon-count contrast vs microwave frequency; correlation gating uses second-order arrival statistics to suppress uncorrelated background.
5. **Dominant failure mode:** SPAD saturation/dead-time. An NV *ensemble* (UncutGem uses a high-NV-density diamond for sensitivity) emits far more than the ~Mcps a SPAD can count before dead-time nonlinearity destroys the contrast-vs-frequency curve. Either attenuate (throwing away the shot-noise advantage) or switch to a low-NV diamond (losing ensemble averaging). The fusion's value is real only in the low-flux / few-NV regime — must pick the diamond accordingly.
6. **Cost / time:** ~$400-600; ~4-5 months (SPAD timing electronics + sync to ODMR is the bulk of the work).
7. **First validating measurement:** on a low-NV-density diamond, measure ODMR contrast SNR vs integration time with the analog photodiode and with the SPAD; success = SPAD trace follows the √N shot-noise line while the photodiode trace plateaus on electronic noise at short integration.
8. **Prior art:** SPAD/photon-counting NV readout is standard in research confocal setups; the novelty is only in doing it on the DIY UncutGem platform. Scored N3. (Prior-art tool degraded.)

### C6 — EF-NMR + Rb FE-5680A clock  (N3 B4 U4 = 48)
1. **Instruments:** RowleyLab/pyppm EF-NMR (~$300-500) + FE-5680A Rb standard (~$50-200).
2. **New observable:** SI-traceable absolute magnetic field via the proton gyromagnetic ratio — a portable proton-precession magnetometer whose frequency counter is disciplined to a 1e-11 Rb clock, so B = 2π·f_FID / γ_p is absolute with no field calibration step.
3. **Why it beats either alone:** EF-NMR alone measures a precession frequency whose accuracy is bounded by its local timebase (crystal oscillator, ~1e-6, drifting with temperature). The Rb clock alone is non-magnetic. Disciplining the EF-NMR frequency measurement to Rb makes the proton-precession magnetometer accurate to ~1e-8–1e-9 in B (limited then by linewidth/SNR, not timebase) — i.e., a primary-grade absolute scalar magnetometer from two hobby boxes, using the exactly-known fundamental constant γ_p.
4. **Coupling mechanism:** feed FE-5680A 10 MHz into the reference/timebase input of the EF-NMR digitizer or frequency counter; count the proton FID against the Rb-disciplined clock. No physical-field coupling — the fusion is a metrological timebase substitution that upgrades the observable from "relative frequency" to "absolute B."
5. **Dominant failure mode:** EF-NMR FID linewidth and field inhomogeneity, not timebase, become limiting. In an unshielded Earth field with gradients, the proton line is broad and the centroid uncertain at the 1e-7–1e-6 level regardless of how good the clock is — the clock upgrade is moot until field homogeneity is improved (gradient coils / siting). Must demonstrate the FID Q is high enough that the clock is actually the prior limiting term.
6. **Cost / time:** ~$350-700; ~3-5 months.
7. **First validating measurement:** measure Earth's field with EF-NMR using the internal crystal vs the Rb-disciplined counter over a day; success = day-night/temperature-correlated drift in the crystal-referenced B vanishes in the Rb-referenced B, and the absolute value agrees with a local IGRF/INTERMAGNET value within FID-linewidth error.
8. **Prior art:** proton-precession magnetometers are classic and commercial units do use stable oscillators; an explicitly *Rb-clock-disciplined DIY* proton magnetometer characterized for absolute accuracy is a modest but real novelty in the DIY space. N3. (Prior-art tool degraded.)

### C7 — Rydberg electrometer + Rb FE-5680A clock  (N3 B2 U4 = 24)
1. **Instruments:** BUILD-A Rydberg electrometer (~$4.3k) + FE-5680A (~$50-200).
2. **New observable:** an absolute, antenna-calibration-free RF electric-field / power standard. The Autler-Townes splitting Ω_AT = d_n·E/ℏ is a *frequency*; measuring that frequency against a Rb-disciplined reference makes E SI-traceable through the atomic dipole moment and a clock — no calibrated horn antenna needed.
3. **Why it beats either alone:** BUILD-A's stated SI-traceability still leans on antenna-gain calibration for the absolute field; the AT-splitting readout's accuracy is bounded by the timebase defining "splitting in Hz." Disciplining to Rb removes the timebase term and leans the absolute E entirely on the (computable) Rydberg dipole moment + the clock — the NIST self-calibration philosophy, made traceable on a budget. The clock alone is non-EM.
4. **Coupling mechanism:** Rb 10 MHz → reference input of the Red Pitaya / RF source / frequency analysis chain that measures the AT splitting; E = ℏ·Ω_AT/d_n with Ω_AT now Rb-traceable.
5. **Dominant failure mode:** the Rydberg readout is already limited by laser frequency noise and EIT linewidth (BUILD-A sensitivity analysis: laser noise dominant), both far above the timebase error. The clock upgrade buys almost nothing until the laser-lock floor is reached — so the fusion's marginal value is low until BUILD-A is fully optimized. Buildability also gated on the entire $4.3k BUILD-A succeeding first.
6. **Cost / time:** ~$4.4k; >6 months (BUILD-A is 16 weeks alone, fusion only meaningful post-optimization). Time-box risk → B2.
7. **First validating measurement:** measure AT splitting for a fixed known RF drive with internal vs Rb-disciplined frequency reference; success = improved long-term reproducibility of the inferred E once (and only once) the laser lock is good enough that timebase was the limit.
8. **Prior art:** NIST's whole Rydberg-electrometry program is built on clock-traceable self-calibration; this is essentially replicating that philosophy DIY, so low conceptual novelty. N3, low B, included for completeness.

### C8 — BBO entangled-photon source + SPAD + QRNG  (N3 B2 U3 = 18)
1. **Instruments:** Type-I BBO entangled-photon source (~$1.5k STRETCH) + OpenSPAD (~$300-500, ideally a coincidence pair) + beam-splitter QRNG (~$100-200).
2. **New observable:** a self-monitoring randomness beacon — QRNG bits whose extractor is gated in real time by a live CHSH/visibility "health" measurement of the entangled source, so the randomness carries an entanglement-witnessed quality flag rather than only passing statistical tests.
3. **Why it beats either alone:** a beam-splitter QRNG's "quantumness" is assumed, not verified online; statistical test suites (NIST STS) detect classical failure but not subtle bias. The BBO source + SPAD coincidence gives a measurable CHSH S-value / visibility that, when it degrades (misalignment, source drift), flags the randomness as suspect *before* it is used. The entangled source alone isn't a practical RNG; the QRNG alone has no self-witness.
4. **Coupling mechanism:** SPAD coincidence counts from the BBO pairs continuously estimate S/visibility; a threshold on S vetoes/relabels QRNG output blocks (or switches the extractor seed). The fusion observable is "randomness conditioned on a live Bell/visibility certificate."
5. **Dominant failure mode:** DIY BBO + SPAD pairs are alignment-fragile and low-rate; coincidence statistics may be too slow/noisy to gate a useful bit rate, and detection-loophole-open S-values don't constitute true device-independence — risk of *overclaiming* certification it doesn't have. Must frame as a health-flag, not device-independent randomness.
6. **Cost / time:** ~$2k STRETCH; >6 months; two STRETCH instruments → low B.
7. **First validating measurement:** deliberately misalign the BBO source mid-run; show the coincidence-derived S drops below threshold and the beacon flags the contemporaneous QRNG blocks as low-confidence, while a blind statistical test on those same blocks does not.
8. **Prior art:** device-independent and source-monitored QRNG is a mature research area (well-established at lab scale). DIY hobby-tier replication is novel only as an artifact; conceptually not new. Lowest product — included for completeness.

---

## Editorial — Top 5

**1. NV magnetometer + EF-NMR (product 64).** This is the strongest fusion because it produces a
genuinely emergent observable — chemically/nuclear-species-specific, spatially-localized
magnetometry — that neither instrument can approach alone, and it does so for ~$500 using two
already-cataloged hobby kits. The EF-NMR sample becomes a species-tagged AC field source that the
NV transduces optically: this is not two co-located readings, it is one instrument's output
physically driving the other's input. The honest risk is sensitivity (a broad-ODMR UncutGem-class
NV may not see a prepolarized proton signal without a strong cheap-magnet prepolarizer or a
doped/concentrated phantom), so the realistic first milestone is unambiguous *detection* of an
NV-read FID at the EF-NMR frequency, not imaging. Even the detection result — "DIY optically
detected Earth-field NMR" — is citable and is the rare combination here that is both novel and
buildable on a true hobby budget.

**2. NV magnetometer + Rb FE-5680A clock (product 60).** Highest buildability on the board (B5):
the coupling is a 10 MHz reference cable into the ODMR microwave synthesizer, and the payoff —
ppb-stable *absolute* DC magnetometry where the hobby NV is otherwise synthesizer-drift-limited —
is real and useful for any long-baseline magnetometry (including the project's own MagNav
interest). Its honest weakness is novelty: clock-referenced NV interrogation is standard
metrology practice, so the contribution is "doing it well on DIY hardware" rather than a new
observable. The technically interesting part is forced by the fusion itself: once synthesizer
drift is removed, the NV zero-field-splitting temperature coefficient becomes the dominant error,
making a dual-ODMR-transition B/T separation readout mandatory — that sub-problem is where the
real engineering and any publishable angle live.

**3. Rydberg electrometer + NV magnetometer (product 48, top of the 48 tie).** The most
*conceptually* ambitious entry: co-located SI-traceable E plus B at one point, enabling EM source
disambiguation (capacitive/near-field vs radiating/far-field). It is ranked third not for weak
novelty (N4) but for buildability — it inherits BUILD-A's $4.3k cost and 16-week timeline, and
the genuine physics caveat that the GHz Rydberg E-channel and the DC–MHz NV B-channel only fuse
at the common *modulation envelope*, not at a single 14 GHz Poynting vector. Framed honestly as
multi-band / envelope-level EM source classification it is a strong, defensible result and a
natural extension if BUILD-A is built anyway; framed as "full Poynting vector at 14 GHz" it would
be an overclaim. It is the device-level realization of the user's own "Rydberg-E + OPM-B" example
but substituting the $100 NV they can actually build for an OPM they do not own.

**4. QRNG + NV magnetometer (product 48).** The cleverest "shape" on the list: a quantum-certified
RNG used as a *metrological dither standard* so that stochastic-resonance signal recovery and the
noise-floor estimate become traceable rather than assumed. High novelty (N4) and good
buildability (two near-turnkey boxes), held to product 48 by usefulness — it is a niche
calibration trick rather than a result a broad audience cites. The sharpest risk is subtle and
worth flagging: the QRNG output is only certified-white as *bits*; the DAC reconstruction into an
analog dither can itself color the noise, so the reconstruction chain — not the quantum source —
becomes the thing that must be independently validated for the traceability claim to hold.

**5. SPAD + NV magnetometer (product 48).** The most physically standard but most reliably
deliverable of the 48-tie: photon-counting readout takes the DIY NV from photodiode-electronic-
noise-limited to shot-noise-limited and adds photon-correlation background rejection. Novelty is
modest (N3 — this is textbook research practice, the contribution is doing it on UncutGem). The
non-obvious design constraint, again forced by the fusion, is that SPAD dead-time saturates on a
high-density NV *ensemble*, so realizing the advantage requires deliberately choosing a low-NV
diamond and accepting the low-flux regime — a real engineering decision that the combination,
not either instrument alone, imposes.

*Generated 2026-05-16 — Framing A. Prior-art arXiv MCP degraded (latest-feed-only); novelty
scores reflect domain-literature reasoning, not a completed automated search.*
