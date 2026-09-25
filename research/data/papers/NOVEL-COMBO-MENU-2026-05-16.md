# Novel Combination Investigation — Consolidated Menu (2026-05-16)

**Question asked:** not "find new devices" but "find novel *combinations* of measurements or
physical effects that produce interesting or usable results — a new quantum method."

**Method:** 3 generation agents (Framing A buildable sensor-fusion, B cross-domain physics
method, C MERA/holographic physical bridge) → 9 + 9 + 7 scored candidates. Then 6 second-wave
agents: 3 physics deep-dives on the headline winners + 3 adversarial red-teams. Scoring rubric
identical across framings: NOVELTY × BUILDABILITY × USEFULNESS, each 1–5.

> **Headline: every wave-1 #1 winner was knocked down by wave-2 scrutiny.** That is the finding,
> not a failure of the process — the red-team is why you trust what's left. Two survivors remain
> worth doing. The rest are documented so they are not re-proposed.

---

## Tier 0 — Survives scrutiny, worth building

### S1. NV magnetometer + permanent-magnet-prepolarized Earth-field NMR
*(Framing A #1, reframed)*

- **Emergent observable (genuinely emergent — not co-location):** the prepolarized sample's
  nuclear magnetization *physically drives* the NV optical transducer. One instrument is the
  source term in the other's Hamiltonian.
- **Deep-dive verdict: NEEDS-MODIFICATION (physically sound).** Signal budget: 5 cm³ water at
  **1 T** prepolarization (cheap NdFeB Halbach, ~$80–200), 1 mm standoff → **~1.6 µT AC** at the
  proton Larmor line (2.13 kHz) → clears even a worst-case broad-CW-ODMR hobby NV at SNR=3 in
  ~2 s ideal. The wave-1 nominal geometry (0.5 T, 1 cm³, 2 mm) → only ~20 nT (needs a good DIY
  *pulsed* NV, arXiv:2512.03106-class). Earth-field-only prepolarization → ~2 pT: **REFUTED** for
  every NV class. **The prepolarizer magnet is the single load-bearing component.**
- **Red-team caveat:** realistic honest deliverable on UncutGem-class hardware is a
  negative-result / upper-bound paper unless the 1 T prepolarizer + fast-discharge switch is
  built. Every *component* is published (nanoscale NV-NMR; Budker–Pines optical low-field NMR);
  the narrow novel slice is the *specific cheap tuple*: sub-$200 broad-ODMR DIY NV (not a vapor
  cell, not lab confocal) transducing a permanent-magnet-prepolarized mL bulk proton FID at mm
  standoff in the 2 kHz regime. No located precedent for that exact artifact + regime.
- **Scores:** N3 · B4 · U4 = **48** (down from wave-1 64; honest, build-real).
- **MVP:** ~$530–980 (1 T Halbach + fast-discharge switch + DIY pulsed NV + 2 kHz lock-in).
  Build-critical: 2.13 kHz sits in the 50/60 Hz mains-harmonic forest — trim B₀ to park the
  Larmor line in a clean window.

### S2. Rydberg static-CFT connected-correlator on QuEra Aquila — as an ε-channel test
*(Framing C #1, reframed — "HYP-017 done correctly")*

- **What genuinely works:** preparing a *static* Ising-critical ground state via Δ-sweep with
  **zero time evolution** truly dissolves the R1 hologron-decay killer (nothing propagates), and
  the explicit bitstring cumulant `mean(bᵢbⱼ) − mean(bᵢ)mean(bⱼ)` truly fixes the R2
  product-of-densities killer (retains exactly the connected piece R2 destroyed). This is real
  and worth recording: it is HYP-017's two fatal defects actually dissolved, not worked around.
- **But the deep-dive + red-team both independently caught the same fatal flaw:** Aquila reads
  **only Rydberg occupation (n-basis, no rotated readout** — confirmed arXiv:2306.11727). The
  connected occupation correlator lives in the **energy/ε channel (α≈2)**, NOT the stress-tensor
  channel (**α≈4**) the paper's headline claim needs. The α≈4 object is sub-sub-leading (~800×
  smaller at r=6) and unreadable on this platform. SIM-2026-023's [3.2, 4.8] window is the wrong
  yardstick here. Plus near-zero *measurement* novelty: **Bornet/Lukin, Science 2024
  (arXiv:2402.15376)** already ran this exact estimator on a 24+40-atom ring.
- **Salvageable deliverable:** a ~$206 / ~20k-shot **ε-channel α≈2 + σ-exponent consistency
  check** — an honest external-validation footnote for SciPost review. It does **not** confirm
  α≈4; the published "three numerics converge on 4.0" (MEMORY option B) stays the stronger
  argument for that claim.
- **Scores (reframed):** N2 · B4 · U3 = **24** as an ε-channel cross-check. (As an α≈4 test: REFUTED.)
- **Cost correction:** real Aquila is $0.01/shot, $0.30/task, 1000-shot/task cap — not the
  wave-1 figures.

---

## Tier 1 — Survives only as engineering-recoverable, modest value

### S3. Rydberg Autler–Townes "field ruler" co-located with a magnetometer
*(Framing B #4 — the red-team's single most defensible Framing-B candidate)*

- The only Framing-B candidate whose novelty score (N3) was **not** inflated by the red-team.
  AT splitting of a Rydberg transition is an SI-traceable in-situ E-field ruler; co-locating it
  with a magnetometer disambiguates E vs B source contributions.
- Objection is engineering-recoverable, not fatal: a mT NV bias field broadens the AT ruler
  (first-order coupled systematic) — separable with a dual-readout scheme.
- Directly serves the project's existing **HYP-018 / HYP-019** EMI cross-contamination question.
- **Scores:** N3 · B4 · U4 = **48**.

---

## Tier X — Refuted by deep-dive or red-team. Do NOT re-propose.

| Candidate | Framing | Killer (quantitative) |
|---|---|---|
| **Radical-pair-gated NV relaxometry** (wave-1 overall #1, score 100) | B | **REFUTED.** NV listens at 2.87 GHz; radical singlet-triplet noise band is 10–100 MHz → spectral-overlap suppression ~3×10⁻⁹ (SNR=3 unreachable in >10³ yr). Tuning NV down via GSLAC needs B₀≈102 mT, which saturates the radical-pair MFE and erases the selectivity fingerprint — the two operating fields cannot coexist. Also: prior art exists — **PRR 6, 013218 (2024)**, "Sensing of magnetic field effects in radical-pair reactions using a quantum sensor." Idea was genuinely new; the physics forbids the device. |
| LC-ladder / transmission-line MERA emulator | C | **KILL.** (1) Published: arXiv:2407.04171 already does transmission-line→cMERA→AdS. (2) Pure reinstantiation of the HYP-014 failure — a free linear network where r⁻⁴ is *designed in* by Cauer synthesis. Measuring an exponent you specified analytically = negative information. |
| Coupled-resonator hyperbolic-lattice transport analog | C | Designed-in geodesic; prior art (Kollár et al., Nature 2019). Cannot resolve the load-bearing 0.72% π/2 prefactor. |
| QRNG + NV magnetometer (stochastic-resonance) | A | Category error: the quantum certificate is on *bit unpredictability*; SR quality depends on post-DAC analog amplitude PDF, identical to a $0.50 noise diode. Net gain over prior-art SR magnetometry: zero. Not a fusion — a failed substitution. |
| NV + Rb-clock "drift-locked" magnetometry | A | NV is already SI-traceable with no clock (Qnami/NIST). On an unstabilized hobby diamond the ZFS temperature drift ≥ the synthesizer drift it removes — its own success test fails. A reference cable, not a fusion. |
| Rydberg-EIT optical NMR | B | Wrong B-transducer by 3–6 orders vs SERF. Substituting a strictly worse transducer = negative-value novelty. |
| Cavity-MFE spectroscopy | B | VSC needs molar concentrations; a clean MFE needs isolated geminate pairs — mutually exclusive operating points. Exploratory theory only. |
| HOM phonon thermometry | B | Incremental reframing of published coupling (PRL 116, 033601). "Calibration-free" claim fails — needs sample-specific Debye–Waller factor. |
| Rydberg E + NV B "single-point Poynting vector" | A | GHz E-channel and DC–MHz B-channel only co-modulate at the envelope, not a 14 GHz Poynting vector. A single Rydberg cell already does co-located E+B (US 10,823,775 B2). Co-location, not fusion. |

---

## Cross-cutting lesson (added to project methodology)

4 of 5 Framing-C bridges and the Framing-A QRNG candidate failed through **the same mechanism
the project already learned twice (HYP-014 REFUTED, HYP-017 closeout):**

> **A power-law exponent match is not evidence of a mechanism.**

The wave-1 rubric rewarded "killer avoided" cells that were true-but-vacuous (a classical linear
network avoids R1–R4 only by deleting all the physics) and rewarded "measures r⁻⁴" without
asking whether the system *contains* stress-tensor exchange. **Recommended permanent rubric
addition: a `mechanism-faithful vs exponent-coincidental` axis** alongside N/B/U for any future
holographic-bridge proposal.

## What to actually do (recommendation)

1. **S1 (NV + prepolarized EF-NMR)** is the one buildable, genuinely-emergent combination. If
   built honestly with the 1 T prepolarizer, it is a real DIY optically-detected-NMR instrument
   in a regime with no exact precedent. ~$530–980, ~6 months. **Highest expected value.**
2. **S3 (Rydberg-AT ruler + magnetometer)** is the cleanest path that also feeds an existing
   project hypothesis (HYP-018/019). Lower novelty, solid utility.
3. **S2** only as a cheap honest SciPost-review footnote (ε-channel, ~$206) — explicitly *not* a
   confirmation of α≈4.
4. Do not pursue any Tier-X item; this file is the record so they are not regenerated.

---
*Source files: NOVEL-COMBO-{A,B,C}-*.md (generation), DEEPDIVE-{radical-pair-NV,
rydberg-cft-correlator,nv-efnmr}.md (physics deep-dives), REDTEAM-{A,B,C}-*.md (adversarial).
All in research/data/papers/. Prior-art caveat: the paper-search arXiv MCP returned a stale
recency feed throughout; all prior-art checks done via WebSearch with cited URLs/arXiv IDs.*
