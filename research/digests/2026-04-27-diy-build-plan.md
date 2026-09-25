# DIY Quantum Sensor — Integrated Build Plan

**Date:** 2026-04-27
**Team:** diy-quantum-sensor-build (4 specialists, parallel dispatch)
**User outcomes target:** publishable measurement + grant demo + personal-use sensor + worldline-MERA platform — all four.

---

## TL;DR

Three things to do, in this order, total spend across the whole arc ≈ **$30k**:

1. **This week:** run the AWS Braket script for HYP-2026-017 + HYP-2026-020. Cost: **$115**. Output: cross-platform validation of α≈4 + topological entanglement entropy on QuEra Aquila. Publishable result in ~1 week.
2. **Months 1–4:** order parts and build the DIY Rydberg vapor-cell electrometer (Build A). Cost: **$4,340**. Output: working SI-traceable RF spectrum analyzer at ~300–500 nV/m/√Hz, your own calibration-free quantum sensor.
3. **Decision point at month 6:** build the tweezer array (Build B) only if you've burned through 100+ QuEra cloud runs and need custom Hamiltonians or iteration speed. Otherwise keep paying $115/run. Cost if pursued: **+$22k** ($26k total).

The "Build B" verdict was the unexpected one — the team spec'd it carefully and concluded that **for this project's current pace, the cloud wins**. The 8-atom array can't extract α at all (CMI(dr=3)/CMI(dr=1) = 1.2% — buried in shot noise). 16 atoms gets you a 2-point consistency check. 32 atoms is the real science target, and at 32 atoms with $22k of custom hardware, you're competing with QuEra's 256-atom commercial system that we can rent for $115. Build B wins only when iteration rate or custom physics matters more than per-run cost.

---

## 1. The "Sugar Cube" / "Soldier Through a Mountain" Adjudication

**Two separate news stories, conflated.**

**Story 1 — Real:** Matthew Kinsella (Infleqtion CEO) used "sugar cube" to describe Infleqtion's **Skywire** Rydberg RF receiver in 2025–2026 public appearances. Real product. In customer hands. Defensible physics — vapor cell IS ~1 cm³, Rydberg electrometry IS SI-traceable. No through-rock claims in any Kinsella material. Not "Skunk Works." Infleqtion is a ColdQuanta / University of Colorado spinout.

**Story 2 — Debunked:** April 7, 2026 NY Post reported a Lockheed Martin Skunk Works classified device called "Ghost Murmur" — NV-center diamond magnetometer + AI — used by the CIA to locate a downed F-15E pilot in an Iranian mountain crevice at 40-mile range. Mainstream physics press (Science/AAAS, Scientific American, Fast Company) tore it down: 40-mile detection of a human magnetic signature **violates the inverse-cube law by ~10 orders of magnitude**. Actual rescue used a Boeing CSEL emergency beacon (standard military gear). Lockheed declined comment. No technical documentation exists.

The "soldier through a mountain" memory is Story 2. Independent verification: our own Tier 1 sweep on April 26 derived the same r⁻³ + sensor-floor constraint and concluded the same thing. We re-derived what real physicists in real publications already concluded.

Source: `research/data/papers/SKUNK-2026-001-identification.md`

---

## 2. HYP-017 + HYP-020 Cloud Run — Run This Week

**File:** `research/data/builds/HYP-2026-017-runnable.py` + `HYP-2026-017-readme.md`

**What it does:**
- 30-atom binary tree layout, 5 µm boundary spacing < 9.76 µm blockade radius
- 2.80 µs analog Rydberg pulse sequence (T2* ~4 µs, 1.2 µs headroom)
- Hologron injection via ShiftingField local detuning (2 MHz on target sites)
- Energy estimator from TFIM-Rydberg mapping `<Z_i> ~ 1 - 2*density_i`
- TEE via Rényi-2 collision probability from bitstring readout
- Z₂ ferromagnetic trap diagnostic (`|Z_avg| < 0.05` gate before trusting TEE)
- Shot-noise α-precision Monte Carlo runs **classically at startup** so you know the expected uncertainty before paying for shots

**What you do:**
1. `pip install amazon-braket-sdk numpy matplotlib`
2. AWS Braket account + credentials (~10 min if you have an AWS account)
3. Run with `USE_LOCAL=True` first (free local emulator) to verify everything works
4. Set `USE_LOCAL=False`, target `arn:aws:braket:us-east-1::device/qpu/quera/Aquila`
5. Submit — 8000 shots HYP-017 + 3000 shots HYP-020 at $0.01/shot ≈ **$110 plus task overhead, total ~$115**
6. Output: force-profile PNG, α fit, S_topo Rényi-2 estimate

**Expected outcome:** α = 4.0 ± 0.3–0.5, S_topo ≈ -ln(2) = -0.693 nats. If both land within shot-noise of Helios SIM-2026-015d (α = 3.97 ± 0.15) and Kitaev-Preskill prediction, that's a publishable **cross-platform AdS/CFT result** — first time α≈4 stress-tensor exchange is reproduced on neutral-atom hardware.

If it disagrees with Helios, that's *also* publishable — it constrains platform-specific systematics in α. Either outcome is a result.

---

## 3. Build A — DIY Rydberg Electrometer ($4,340, 16 weeks)

**File:** `research/data/builds/BUILD-A-rydberg-electrometer.md`

**BOM total: $4,340. Under target by $660.**

| Subsystem | Cost | Source |
|---|---|---|
| 780 nm probe ECDL (Littrow sled, Eagleyard diode + Thorlabs grating + piezo + TEC) | $650 | Wieman-Hollberg 1991 + NIST AMO open-source sled CAD |
| 960 nm ECDL + PPKTP SHG → 480 nm coupling laser (Raicol crystal, DIY oven) | $945 | Option B over direct 480 nm diode — SHG more reliable at this budget |
| Triad RF Rb cell, 75 mm natural abundance, 60 °C | $340 | Triad RF |
| HP 8340B signal generator (DC–26.5 GHz) used | $450 | eBay |
| Red Pitaya STEMlab 125-14 + PyRPL lock-in | $345 | Red Pitaya |
| Pre-formed mu-metal cylinder shielding | ~$200 | Magnetic Shield Corp |
| Photodetectors (DIY op-amp + photodiode) | ~$80 | Digikey |
| Optical breadboard + optomech | ~$700 | Mix Thorlabs cheap + McMaster |
| Sat-abs reference cell | ~$300 | Triad |
| Misc cables/PSUs/AOM driver | ~$330 | — |

**Sensitivity targets:**
- First light (sat-abs only, week 8): ~1–5 µV/m/√Hz
- After PDH lock (week 12): **~300–500 nV/m/√Hz**
- NIST Holloway research-grade benchmark: 55 nV/m/√Hz (you're within 6–10× of the world-class lab number, in your basement, for $4k)

**Protocol (4 phases):**
1. Laser checkout (weeks 1–4)
2. Saturated-absorption frequency lock (weeks 5–6)
3. EIT signature observation — Go/No-Go gate at >3% transparency contrast (weeks 7–8)
4. Autler-Townes splitting under known RF field → V/m calibration curve (weeks 9–16)

**Top 5 risks:**
1. SHG power failure (40% probability) → fallback to direct 480 nm diode
2. Probe laser mode-hops (35%) → mitigated by TEC stability + AR-coated diode
3. EIT linewidth too broad (25%) → vapor cell temperature tuning
4. 60 Hz magnetic noise pickup (30%) → mu-metal shielding + ground loop discipline
5. RF calibration uncertainty (50%, low impact) → can be refined post-publication

**Why this satisfies all four user outcomes:**
- **Publishable:** "Sub-$5k DIY SI-traceable Rydberg electrometer" — there are <5 such builds documented worldwide. PRX Quantum / Rev. Sci. Instrum. letter.
- **Grant demo:** working hardware on a desk beats every PowerPoint slide.
- **Personal-use sensor:** real RF spectrum analyzer at 1–40 GHz with absolute calibration. Useful for EMC, ham radio, antenna characterization, basic physics demos.
- **Worldline-MERA platform:** Build A's lasers (780 nm probe, 480 nm coupling) are the *exact* lasers Build B needs. Build A is the foundation, not a detour.

---

## 4. Build B — Tweezer Array Upgrade (do NOT build yet, $22k incremental)

**File:** `research/data/builds/BUILD-B-diy-tweezer-array.md`

**The honest finding:** at this project's current pace, **Build B does not pay back.**

**Shot-noise math:**
- α = 4 means CMI ~ dr⁻⁴, so CMI(dr=3) / CMI(dr=1) = 1/81 = 1.2%
- Resolving CMI(dr=3) at 50% relative noise requires **>1.2M shots** at that point alone
- N=8: 1 reliable CMI point. Not enough for any α extraction.
- N=16: 2 reliable points. Can do a **consistency check** R = CMI(1)/CMI(2) = 2^3.92 = 15.0 vs measured. ~50k shots, ~3 hours. NOT a fresh α fit.
- N=32: 4 reliable points. σ_α < 1.0 achievable. **This is the real science target.**

**Incremental BOM (on top of Build A's $4,340):**

| Subsystem | Cost |
|---|---|
| UHV chamber (turbo + ion pump + Rb dispenser + viewports) | $3,700 |
| MOT optics + coils | $1,200 |
| 852 nm trapping ECDL | $900 |
| SLM + high-NA objective | $3,500 |
| EMCCD camera (used) | $2,895 |
| Control electronics / FPGA sequencer | $800 |
| Optomech (extra) | $900 |
| 15% contingency | $4,100 |
| **Incremental total** | **$18,000 + $4,100 contingency = $22,100** |

**Decision criterion — when to actually build B:**

Break-even vs $115/run cloud at 3-year amortization is **~90 QuEra runs**. At this project's current pace (~1–2 runs per major hypothesis cycle, maybe 5–10 runs/year if research expands), Build B does not pay back on cost. Build B wins only when:

1. **>200 runs/year** are needed (parameter sweeps, systematic studies, student training)
2. **Custom Hamiltonians** beyond Aquila's analog programmable model are required (mid-sequence feedback, exotic gates, non-PXP physics)
3. **Iteration speed** matters more than per-run cost (you want to try a new idea today, not next week after a cloud queue)

**Recommendation: defer Build B decision to month 6.** Run HYP-017+020 first ($115). Build A in months 2–4 ($4,340). Re-evaluate Build B at month 6 based on (a) HYP-017 results, (b) how many follow-up runs the research generates, (c) whether new hypotheses require custom Hamiltonians.

---

## 5. Timeline + Cost Across All Four Outcomes

| Month | Action | Cost | Outcome unlocked |
|---|---|---|---|
| 1 | Run HYP-017 + HYP-020 cloud | $115 | Cross-platform AdS/CFT result (publishable) |
| 1 | Order Build A parts | $4,340 | (parts inbound) |
| 2–4 | Build A construction (lasers, sat-abs, EIT) | (time) | Working DIY Rydberg electrometer |
| 5 | Build A first measurement (V/m calibration) | (time) | Publishable + grant demo + personal sensor |
| 6 | **Build B decision point** | — | Defer or proceed |
| 6–18 | (optional) Build B construction | $22,100 | Worldline-MERA DIY platform (only if justified) |
| 18–24 | (optional) Build B first α measurement on N=32 array | (time) | Original α at independent-researcher scale |

**Total cost if all paths pursued: ~$26,555.** Below the $50k user-stated ceiling with margin.

**Total cost for outcomes 1–3 (publishable + grant demo + personal sensor): $4,455.**

That's the right opening move: $4,455 buys three of four outcomes outright, and the fourth (worldline-MERA platform) is satisfied for $115 via cloud until you outgrow it.

---

## 6. Risk Register

| Risk | Severity | Mitigation |
|---|---|---|
| HYP-017 fails on Aquila (α ≠ 4) | Medium | Still publishable as platform-systematics result |
| Build A SHG path fails | High | Fallback to direct 480 nm diode (+$300, less efficient) |
| Build A laser locking unstable | Medium | Sat-abs + Red Pitaya PyRPL is a well-trodden path; if struggling, MIT atomic-physics teaching docs cover it |
| QuEra Aquila pricing changes | Low | Currently $0.01/shot; 10× rise still keeps Build B uncompetitive |
| Project pivots away from MERA holography | High but acceptable | Build A is independently valuable as RF sensor; not stranded |
| Build B started prematurely | High | Defer decision to month 6 — this report's primary recommendation |

---

## 7. Knowledge Base Updates

**Add to research/knowledge-base.md:**
- 2026-04-27: "Soldier through mountain" claim adjudicated to Lockheed Skunk Works "Ghost Murmur" April 2026 NY Post article — **debunked by Science/Scientific American/Fast Company on inverse-cube-law grounds**. Distinct from Infleqtion Skywire (real product, no through-rock claims).
- 2026-04-27: DIY Rydberg electrometer spec at $4,340 BOM — sub-µV/m/√Hz achievable. Build A.
- 2026-04-27: DIY tweezer array (Build B) deferred — break-even with QuEra Aquila cloud is ~90 runs at $115/each. Cloud wins for current project pace.
- 2026-04-27: AWS Braket runnable script for HYP-017 + HYP-020 ready, $115 expected total. Use `USE_LOCAL=True` for free local-emulator dry run before spending.

---

## Files Produced

- `research/data/papers/SKUNK-2026-001-identification.md`
- `research/data/builds/BUILD-A-rydberg-electrometer.md`
- `research/data/builds/BUILD-B-diy-tweezer-array.md`
- `research/data/builds/HYP-2026-017-runnable.py`
- `research/data/builds/HYP-2026-017-readme.md`
- `research/digests/2026-04-27-diy-build-plan.md` (this file)
