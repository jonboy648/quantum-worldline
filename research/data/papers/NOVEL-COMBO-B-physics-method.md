# NOVEL-COMBO-B: Physics-Depth Novel Measurement Methods

**Framing B** of a 3-part investigation. Goal: couple one quantum-sensing effect with one effect from broader physics/chemistry into a measurement *method* not in the literature, where the coupling yields an observable neither effect produces alone.

Status: COMPLETE
Date: 2026-05-16
Owner: framing-B physics-method agent

## Ranked Candidates

| Rank | Method | Effects coupled | Emergent observable | N | B | U | Product |
|------|--------|-----------------|---------------------|---|---|---|---------|
| 1 | Radical-pair-gated NV relaxometry ("chemical-compass magnetometer") | Radical-pair singlet-triplet spin chemistry (MFE) + NV ground-state spin relaxometry (T1) | Molecule-*specific* AC magnetic susceptibility: field response that exists only for a named radical-forming analyte | 5 | 4 | 5 | 100 |
| 2 | Cavity-MFE spectroscopy of radical recombination | Vibrational/electronic strong coupling (polariton) + radical-pair recombination-yield magnetic field effect | Polariton-branch-resolved shift of the magnetosensitive recombination yield -> the radical's hyperfine map read optically | 5 | 3 | 4 | 60 |
| 3 | HOM phonon thermometry of a solid-state emitter | Hong-Ou-Mandel two-photon interference + deformation-potential phonon (Bose) occupation in a quantum emitter | Absolute local lattice temperature from two-photon visibility with no external thermal calibration | 4 | 3 | 4 | 48 |
| 4 | Rydberg-AT field ruler co-located with a magnetometer | Autler-Townes splitting in Rydberg-EIT + an independent (NV / vapor) B-field sensor in the same volume | In-situ, SI-anchored frequency ruler that disambiguates a co-located source's E vs B contribution shot-by-shot | 3 | 4 | 4 | 48 |
| 5 | Rydberg-EIT optical detection of hyperpolarized nuclear precession | Hyperpolarized nuclear-spin NMR (PHIP/dDNP) + Rydberg-EIT vapor transduction | Optical, calibration-anchored zero-field NMR free-induction signal in a Rydberg vapor (not a scalar SERF cell) | 3 | 3 | 3 | 27 |
| 6 | QRNG vacuum-noise transfer standard for a force/field sensor | Vacuum-fluctuation shot noise (QRNG primitive) + optomechanical / atomic force-field sensor | Calibration-free absolute noise-floor and gain transfer reference shared by both channels | 3 | 4 | 3 | 36 |
| 7 | Mechanical-ringdown-clocked NV-NMR | Nanomechanical resonator ringdown phase + NV nanoscale NMR | Phase-coherent NMR sampling clocked past NV T2* by the mechanical oscillator | 2 | 3 | 3 | 18 |
| 8 | SERF comagnetometer with squeezed probe + intrinsic reference | Spin-exchange-relaxation-free comagnetometry + parametric-squeezed light | Sub-SQL self-referenced rotation/exotic-field signal | 1 | 2 | 4 | 8 |

## Editorial (top 5)

### 1. Radical-pair-gated NV relaxometry — a molecule-specific magnetometer (N5 B4 U5 = 100)

**Effects coupled.** (a) The radical-pair mechanism: photo- or redox-generated correlated electron-spin pairs interconvert between singlet and triplet manifolds at a rate set by the hyperfine Hamiltonian H = Σ_k a_k S·I_k plus the Zeeman term g μ_B B·(S₁+S₂); the recombination branching (singlet vs triplet product) is therefore magnetic-field-dependent on the ~ns–µs radical lifetime. (b) NV ground-state relaxometry: the NV ms=0↔±1 longitudinal relaxation rate 1/T1 is driven by magnetic noise at the NV Larmor frequency (~GHz to ~MHz under bias), 1/T1 ∝ S_B(ω_NV).

**Emergent observable.** Neither effect alone is analyte-selective: a bare NV relaxometer senses *any* paramagnetic species; a radical-pair yield assay needs a chemical product readout. Coupled, the transient radical pair is a chemically-gated spin-noise *source* sitting nanometers from a shallow NV. The NV 1/T1 acquires a component that switches on only while the analyte's specific radical pair is alive, and whose magnetic-field dependence is the *hyperfine fingerprint of that exact molecule* (the MFE B½ and low-field-effect structure). The new observable is a per-molecule AC magnetic susceptibility — an NV magnetometer that responds to one named radical-forming compound and is blind to others with different hyperfine constants.

**Mechanism specifics.** The radical-pair correlated spins produce a stochastic dipolar field at the NV with spectral weight peaked at the singlet-triplet mixing frequency ω_ST ≈ (a_eff + Δgμ_BB)/ħ. Tuning the NV bias field sweeps ω_NV through ω_ST; the relaxometry resonance occurs only when the analyte radical is present and only at the field set by its own hyperfine constants. The "gate" is the chemistry: no radical, no spin-noise injection, regardless of bulk paramagnetic background.

**Closest prior art / why different.** NV detection of paramagnetic ions/molecules via T1 (Steinert 2013; covariance magnetometry, Science 2023) — but these are non-selective spin-noise detectors with no chemical gating. Radical-pair magnetoreception is studied by transient-absorption/EPR, never by single-NV relaxometry. The combination — using the *field-dependence of the radical-pair lifetime itself* as the selectivity axis of an NV sensor — was not found in the searches (arXiv/web May 2026). Refs for the components: NV relaxometry of paramagnetic species; radical-pair MFE (J. Phys. Chem. B 10.1021/jp9721816; quantum-Zeno magnetosensitivity Nat. Commun. 2024 s41467-024-55124-x).

**Experimental route + hardest obstacle.** Shallow (<10 nm) NV in a nanopillar, analyte radical photogenerated by a pump laser at the diamond surface, NV bias coil swept while reading T1 via standard 532 nm / MW. Hardest obstacle: getting the transient radical to live long enough and close enough — radical lifetimes (ns–µs) must overlap the NV correlation window, and surface chemistry must hold the radical within ~5 nm. This is the make-or-break and is plausibly addressable with tethered cryptochrome-mimic or flavin–tryptophan model dyads (well-characterized MFE systems).

**Result it yields.** A room-temperature, optically read magnetometer whose signal is a specific molecule's hyperfine spectrum — i.e., chemical identification by magnetic-field-effect spectroscopy at the single-NV (sub-attomole) scale. People want molecule-selective nanoscale magnetometry; this delivers it through chemistry rather than NMR chemical shift.

### 2. Cavity-MFE spectroscopy of radical recombination (N5 B3 U4 = 60)

**Effects coupled.** Vibrational or electronic strong light–matter coupling (Rabi splitting Ω_R between cavity photon and a molecular mode, producing polariton branches |±⟩) + the radical-pair recombination-yield magnetic field effect.

**Emergent observable.** Strong coupling alone modifies reaction rates but gives no spin information; the MFE alone gives a single field-dependent yield curve with no mode resolution. Coupled: the recombination channel that the polariton modifies is itself spin-selective, so the *magnetic-field dependence of the yield becomes a function of cavity detuning*. Scanning the cavity across the polariton dispersion maps which vibrational/electronic mode gates the singlet–triplet recombination — an optically read, mode-resolved hyperfine/spin-dynamics spectrum that neither cavity chemistry nor a bare MFE measurement produces.

**Mechanism specifics.** Polariton formation reshapes the recombination potential along the reactive mode (modified Franck–Condon / rate via collective coupling). If the back-electron-transfer rate k_S (singlet channel) is mode-gated, then ΔY(B) = Y(B) − Y(0) acquires a cavity-detuning dependence ΔY(B; δ_cav), because the competition between spin mixing (rate ω_ST) and recombination (rate k_S(δ_cav)) shifts. The MFE amplitude becomes a probe of *which* mode the cavity is dressing.

**Closest prior art / why different.** Polariton chemistry reviews (Chem. Rev. 2c00855) and RP-MFE are mature *separately*. Web search (May 2026) explicitly returned this as "an emerging research area still being actively investigated" with no realized method. The novelty is using the MFE as the *reporter* of polaritonic rate modification — a spin-chemistry assay of cavity chemistry.

**Experimental route + hardest obstacle.** Microfluidic Fabry–Pérot cavity (sub-µm, IR for vibrational SC) loaded with a known exciplex/radical-pair dye; sweep cavity length and B (0–100 mT); read recombination via fluorescence/transient absorption. Hardest obstacle: achieving collective vibrational strong coupling *and* a clean MFE in the same liquid sample — solvent, concentration, and Q-factor windows barely overlap; this is a real but not national-lab obstacle.

**Result.** First measurement of whether (and which) molecular modes gate spin-selective recombination — directly informs the avian-compass and polariton-chemistry mechanism debates.

### 3. HOM phonon thermometry of a solid-state emitter (N4 B3 U4 = 48)

**Effects coupled.** Hong–Ou–Mandel two-photon interference + deformation-potential coupling of the emitter's zero-phonon line to the acoustic-phonon bath (Bose occupation n̄(ω,T)).

**Emergent observable.** HOM visibility is normally treated as a *figure of merit* to be maximized; phonon temperature dependence is treated as a *nuisance*. Inverted and combined, the measured two-photon visibility V(ΔT) becomes a primary, self-referenced **absolute thermometer** of the emitter's local lattice temperature, because the phonon-sideband weight and pure-dephasing rate γ(T) ∝ ∫ J(ω) coth(ħω/2k_BT) dω are fixed by the known deformation potential — no external thermometer calibration is needed.

**Mechanism specifics.** Indistinguishability I = exp(−2γ(T)τ) × (ZPL fraction)², with γ(T) carrying the explicit Bose factor. Measuring V at two delays (Hong–Ou–Mandel with controlled path delay) separates pure dephasing from spectral wandering, yielding T from the coth(ħω/2k_BT) form alone.

**Closest prior art / why different.** Temperature- and time-dependent HOM has been used to *study* emitter dephasing (ResearchGate 280330335; arXiv:2505.16848). Those works characterize the emitter at a *known* temperature. The inversion — using HOM as the calibrated primary thermometer reporting an *unknown* local temperature via the first-principles phonon spectral density — was not found as a stated method. Novelty is the metrological reframing, hence N4 not N5.

**Experimental route + hardest obstacle.** Single quantum dot or hBN/diamond emitter, unbalanced Mach–Zehnder HOM, cryostat with variable stage temperature for validation then deployment as a non-contact local probe. Hardest obstacle: separating temperature-driven pure dephasing from spectral diffusion and charge noise — requires the two-delay protocol and a trusted J(ω); systematic, not fundamental.

**Result.** Non-contact, calibration-free temperature readout of the *emitter's own lattice site* (not the cryostat sensor) — valuable for quantum-photonic device characterization where the local temperature is exactly what is unknown.

### 4. Rydberg-AT field ruler co-located with a magnetometer (N3 B4 U4 = 48)

**Effects coupled.** Autler–Townes splitting of a Rydberg-EIT transition (Ω_AT = d_n E_RF/ħ, an SI-anchored E-field ruler) + an independent magnetometer (NV ensemble or ground-state vapor) sharing the same sensing volume.

**Emergent observable.** Rydberg AT gives absolute E; the magnetometer gives B; each alone is ambiguous when a single nearby source radiates both. Co-located and cross-read, the AT splitting becomes an *in-situ frequency ruler* that timestamps and SI-anchors the E-field, so the source's E and B contributions are disentangled shot-by-shot by their differential response — an emergent vector source-discrimination observable.

**Closest prior art / why different.** Zeeman-resolved AT and dual-frequency Rydberg electrometry (arXiv:2311.07665; NIST SI-traceable probe) use AT only for Rydberg's *own* E calibration. Using AT as a transfer ruler for a *different co-located sensor modality* to separate E vs B sources was not found, but the building blocks are individually mature → N3.

**Experimental route + hardest obstacle.** The BUILD-A Rydberg vapor cell with an NV film or second alkali species in the same shielded volume; common RF/B source; correlate AT splitting with magnetometer output. Hardest obstacle: physically interleaving two sensors in one volume without each perturbing the other (laser scatter on NV, NV bias field shifting Rydberg Zeeman structure). Engineering-hard, not physics-hard → B4.

**Result.** A self-calibrating dual-mode probe that reports "this source is X V/m AND Y nT" with SI traceability on the E axis — directly useful for EMC, near-field antenna metrology, and the project's own HYP-018/019 E/B cross-contamination question.

### 5. Rydberg-EIT optical detection of hyperpolarized nuclear precession (N3 B3 U3 = 27)

**Effects coupled.** Hyperpolarized nuclear spins (PHIP/dissolution-DNP) producing a coherent low-frequency magnetic FID + Rydberg-EIT vapor as the field transducer.

**Emergent observable.** Hyperpolarization gives a strong nuclear magnetization; Rydberg EIT gives an optical, SI-anchored field readout. Coupled, a zero/low-field NMR free-induction signal is read *optically through a Rydberg vapor* rather than through a scalar SERF cell — an optical NMR channel whose absolute scaling is anchored by the same Rydberg structure used for E-field metrology.

**Closest prior art / why different.** Hyperpolarized-nucleus detection by *atomic magnetometers* is established (arXiv:2301.06607; photo-CIDNP magnetometry) — but exclusively with ground-state alkali (SERF/scalar) sensors. Rydberg EIT as the NMR transducer was not found. Novelty is moderate (the broad concept "atomic-vapor optical NMR" exists) → N3.

**Experimental route + hardest obstacle.** Inject hyperpolarized 13C/1H sample adjacent to the BUILD-A Rydberg cell; detect the µHz–kHz Larmor field as an EIT-line modulation. Hardest obstacle (decisive): Rydberg EIT is intrinsically an *E-field* sensor with poor DC/low-frequency *B* sensitivity (nT at best vs fT for SERF). Without a Rydberg-specific B-transduction trick (e.g., motional-Stark or Zeeman-mixed Rydberg states), the SNR is marginal — this is why B and U are 3, and why it ranks below the AT-ruler use of the same hardware.

---

*Generated 2026-05-16. Prior art checked via paper-search arXiv MCP (relevance-degraded — returned recency-sorted results) and WebSearch (primary verification channel). arXiv IDs cited inline. Tool note: Google Scholar MCP returned empty (blocked); arXiv keyword search returned newest-first regardless of query, so WebSearch was used as the prior-art channel.*

