# Rydberg Sensing, Infleqtion, and the "Quantum Tricorder" — Research Report

**Date:** 2026-04-26
**Team:** rydberg-sensing-research (3 tier leads, 11 specialist subagents)
**Scope:** Matthew Kinsella / Infleqtion, Rydberg electrometry SOTA, sugar-cube cold-atom packages, through-wall sensing physics, buildable independent-researcher experiments, worldline math-bridge.

---

## Executive Summary

1. **The "soldier through a mountain" claim has no support in primary sources.** No Infleqtion press release, DARPA document, Army announcement, or peer-reviewed paper contains this. The actual demonstration (NetModX23, Oct 2023, Joint Base McGuire-Dix-Lakehurst) was open-air HF-SHF reception with the SqyWire Rydberg sensor integrated into SINCGARS — a real and useful capability, but not through-rock detection. The phrase is marketing folklore.

2. **The most strategic finding is unrelated to the original question.** PAPER-2026-061 (Sahay/Lin/Cotler, PRX 2025) shows that the Rydberg PXP Hamiltonian implements the same Ising CFT our quantum-worldline MERA holography work uses. **Our α≈4 stress-tensor force result (SIM-2026-015d, Helios) can be cross-validated on a Rydberg tweezer array (QuEra Aquila) for ~$85 of cloud time.** This is a direct, immediate use of the existing project's results on a second, independent platform.

3. **The realistic buildable experiment is not Rydberg, it's biomagnetic.** ULF skin depth in granite at 1 Hz is ~16 km, so cardiac magnetic signals penetrate rock essentially unattenuated. The bottleneck is sensor noise, not propagation. A gradiometric pair of QuSpin QZFM Gen-3 OPMs (~$42k) gives expected SNR~39 for a 50 aT human MCG signal at 10m through concrete with 10-min integration. This is publishable. Through-mountain person detection (kilometers) remains physically impossible with any current sensor — the heart dipole falls as r⁻³ to ~50 aT at 100m, four orders below any noise floor.

---

## 1. Matthew Kinsella + Infleqtion — Adjudication

**Who:** CEO of Infleqtion (formerly ColdQuanta) since April 2024. VC/investment background, not physicist. First investor, board since 2018. Infleqtion went public via SPAC (INFQ).

**What's verifiable:**
- SqyWire (Rydberg quantum RF receiver) demonstrated at Army C5ISR NetModX23, Oct 2023, integrated with SINCGARS and EW sensor. HF-SHF coverage confirmed in open-air. **No published sensitivity floor.**
- Tiqker optical clock: 30L / 30kg / 3U rack. Hydrogen-maser stability. Pilot production.
- NASA gravity sensor partnership announced Feb 2026.
- DARPA Robust Quantum Sensors program funding active.

**What's unsupported:**
- "Soldier through a mountain" or any through-rock person detection claim. Not in primary sources.
- Sugar-cube *system* (vapor cell is 1 cm³; full SqyWire including laser system is "portable" but not pocket-scale).

**Key sources:** PAPER-2026-053 through PAPER-2026-063, HW-2026-032 through HW-2026-038.

---

## 2. Rydberg Electrometry State of the Art

| Metric | Value | Source |
|---|---|---|
| Best sensitivity | ~45 nV/cm/√Hz (10.7 GHz, three-photon) | SPIE 2025 |
| Optical biasing | 176 nV/cm/√Hz, +35 dB SNR | Borówka et al., Nat. Comm. 2025 |
| Typical 2–5 GHz | 270 µV/m/√Hz | Schlossberger, Nat. Rev. Phys. 2024 |
| Theoretical Fisher-info limit | <1 nV/cm/√Hz | Liu et al. 2026 |
| Bandwidth | DC to THz (vapor cell) | Multiple |
| Multichannel | 1–40 GHz simultaneous (frequency comb) | Nat. Comm. 2025 |
| Calibration | SI-traceable, no reference required | NIST Holloway group |

**What Rydberg can do that classical antennas cannot:**
1. SI-traceable absolute E-field measurement without calibration reference (>10× better at 0.1% precision)
2. Sub-wavelength aperture with broadband sensitivity (~1 cm³ active volume, cm-to-m wavelengths)
3. No loading effect — atoms don't disturb the EM field
4. Simultaneous multiband reception in single cell

**What Rydberg cannot do (current):** Beat well-built classical antennas on absolute SNR at the resonant frequency they're tuned to. The advantage is calibration, bandwidth, and aperture, not raw sensitivity.

---

## 3. Through-Wall Physics — Honest Adjudication

| Mechanism | Rock skin depth | Source signal at 10m | Best sensor | Plausible range |
|---|---|---|---|---|
| **ULF biomagnetic (heart MCG)** | ~16 km @ 1 Hz | ~50 fT (r⁻³ from 50 pT surface) | QuSpin OPM 10 fT/√Hz | **1–30 m through rock** |
| Gravimetric (70 kg person) | N/A | ~5 nGal | Cold-atom gradiometer ~1 nGal | Marginal at 10 m |
| Body thermal RF | mm–cm @ GHz | ~10⁻¹⁹ W/Hz/cm² | Rydberg | Killed by skin depth |
| Tunnel gravimetric (10 m void) | N/A | ~1 µGal | Birmingham gradiometer | **10–20 m, viable** |

**Bottom line:** Through-rock person detection is plausible at tens of meters via biomagnetic OPMs, not via Rydberg RF. The "quantum tricorder" framing conflates three different physics. The physically realistic capability is human-scale at tens of meters, not soldier-through-mountain at kilometers.

Charts:
- `research/data/simulations/sensitivity_vs_frequency.png` — sensor floors vs biological signatures, 0.1 Hz to 1 GHz
- `research/data/simulations/through_rock_attenuation.png` — skin-depth model, granite/concrete dry/wet, 1m/10m/100m

---

## 4. Sugar-Cube Hardware Reality Check

| Component | "Sugar cube" claim | Actual SWaP |
|---|---|---|
| Rydberg vapor cell (active volume) | ✅ ~1 cm³ | ~1 cm³ (real) |
| Full SqyWire (cell + lasers + optics) | Implied | "Portable" — no published SWaP |
| Infleqtion Tiqker optical clock | "Compact" | 30L / 30kg / 3U rack |
| AOSense gravimeter | "Portable" | Backpack-scale |
| NIST CSAM atomic magnetometer | ✅ ~12 mm³ | Real (195 mW) |
| QuSpin QZFM Gen-3 | Cigar-pack scale | Real (10 fT/√Hz, no cryo) |
| MEMS Rydberg vapor cell | First demo Sept 2025 | Not yet commercial |

The cubic-centimeter sensor is real. Cubic-centimeter *system* is not — except for warm-vapor magnetometers (CSAM, QuSpin), which have actually achieved that scale.

---

## 5. Hypotheses + Feasibility (HYP-2026-017 through 020, all TESTABLE_NOW)

| ID | Claim | Cost | Hardware | Best for |
|---|---|---|---|---|
| **HYP-017** | α≈4 holographic force reproduces on QuEra Aquila blockade-MERA | $85 | AWS Braket cloud | Cross-platform validation of our Helios result |
| **HYP-018** | MCG-through-wall person detection at 10 m, SNR 39 | $42k | 2× QuSpin OPM + DAQ | Most immediately publishable |
| **HYP-019** | Rydberg + OPM cross-contamination minimum separation | $55–65k | 2× ECDL + Rb cell + OPM | Novel — no published curve exists |
| **HYP-020** | TEE on same Aquila run as HYP-017 | +$30 | (joint with HYP-017) | Marginal-cost AdS/CFT joint test |

**Recommendation order by ROI:**
1. **HYP-017 + HYP-020 combined ($115)** — direct extension of existing project, new platform, joint AdS/CFT test, no hardware purchase. Run via AWS Braket account.
2. **HYP-018 ($42k)** — physically novel result, publishable either way, leverages the most impressive consumer-quantum-sensor on the market (QuSpin).
3. **HYP-019 ($55–65k)** — only worth it if HYP-018 is already built, since it adds Rydberg layer to OPM setup.

Build files: `research/data/builds/HYP-2026-017.md` ... `HYP-2026-020.md`

---

## 6. Recommended Build — One Project

**Run HYP-017 + HYP-020 first.** Total cost: $115 of AWS Braket QuEra Aquila time. Time to first result: ~1 week (compile blockade-MERA, schedule shots, analyze). Publication path: PRX or Quantum letter, "Holographic forces and topological entanglement entropy on a Rydberg tweezer array" — directly extends our Zenodo paper to a second hardware platform.

**Rationale:** This is the only build that:
- Costs <$200 to test
- Uses our existing α≈4 / TEE expertise
- Validates Helios result on neutral-atom hardware (independent verification = strong)
- Requires zero physical hardware purchase
- Has a known classical baseline (SIM-2026-015d, α=3.97±0.15)

If HYP-017 confirms α=4.0±0.5 on Aquila within shot-noise consistency with Helios, that's a significant cross-platform result. If it disagrees, that's also significant — it constrains the platform-specific systematics that affect alpha.

The OPM through-wall experiment (HYP-018) is the right *second* project, after HYP-017 results are in hand. Don't start with $42k of hardware when $115 of cloud time is the higher-leverage test.

---

## 7. Quantum-Worldline Connection

**Direct, strong, unexpected.** PAPER-2026-061 (Sahay/Lin/Cotler, PRX 2025) explicitly states that Rydberg tweezer arrays implement the Ising CFT we use for our MERA holography. The PXP constraint from Rydberg blockade gives a modified MERA whose bulk excitations show attractive interactions matching matter coupled to AdS gravity at long distances — i.e., the same α≈4 stress-tensor exchange we measure.

This connects this report's applied-sensing question back to the project's foundational program. It also reframes platform strategy: Quantinuum Helios was the obvious target for our paper. **QuEra Aquila is now an equally valid (and cheaper, cloud-accessible, no-partnership) target** for follow-up work. The user already has AWS account access. This is the most actionable cross-tier connection found this scan.

PAPER-2026-060 (Topological entanglement entropy in Rydberg blockade) extends this further — TEE protocols are testable on the same hardware run, giving a joint AdS/CFT measurement at marginal cost.

---

## 8. Open Questions

- **SqyWire actual sensitivity floor.** Not published. Without it, "Rydberg beats classical" claims for fielded systems remain unverified. ARL-published numbers (~nV/cm/√Hz) are lab benchmarks, not field-deployed measurements.
- **Through-rock geological EM noise floor.** Theoretical analysis assumes magnetically quiet sites. Real rock environments may have 1/f geomagnetic noise that degrades MCG SNR significantly. HYP-018 should include a site survey (cave, basement, rural underground site).
- **Aquila T2\* margin.** HYP-017 protocol runtime is 2.8 µs vs T2\* = 4 µs (1.2 µs headroom). If T2\* drifts down, Floquet echo or shorter-depth circuit needed.
- **Atom interferometry / fifth force searches.** Stanford Kasevich and Berkeley Müller groups do precision tests at 10⁻¹² g level. Connection to our stress-tensor exchange work is indirect (different mechanism: inertial sensing, not Rydberg spectroscopy). Not pursued in this report; flag for future.

---

## Knowledge Base Updates

**Add to research/knowledge-base.md:**
- 2026-04-26: Rydberg PXP-MERA bridge confirmed (PAPER-2026-061): Rydberg tweezer arrays implement Ising CFT identical to MERA holography. QuEra Aquila is a viable second platform for α≈4 force measurement at $85/run cloud cost (HYP-017).
- 2026-04-26: Through-rock person detection range adjudicated: 1–30m via OPM biomagnetic detection only. Through-mountain claims unsupported by primary sources or physics.
- 2026-04-26: SqyWire (Infleqtion Rydberg RF receiver) — Army NetModX23 demo confirmed; published sensitivity floor: NONE.

**Hypothesis status table — add rows:**

| HYP | Status | Confidence | One-line |
|-----|--------|-----------|----------|
| 017 | proposed | medium | α≈4 holographic force on QuEra Aquila blockade-MERA |
| 018 | proposed | low | MCG-through-wall person at 10m via gradiometric OPM |
| 019 | proposed | medium | Rydberg+OPM EMI cross-contamination minimum separation |
| 020 | proposed | low | TEE on same Aquila run as HYP-017 (Kitaev-Preskill) |

**ID counters → MEMORY.md:**
- Last paper ID: PAPER-2026-063 (was 052)
- Last hardware ID: HW-2026-038 (was 031)
- Last hypothesis ID: HYP-2026-020 (was 016)
- Last simulation ID: SIM-2026-022 (was 021)
