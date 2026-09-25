# Weekly Scan — 2026-05-12 (Scan #7, consolidated with interrupted Scan #6)

**Window:** 2026-04-26 → 2026-05-12
**Note:** An earlier scan today ("Scan #6") filed data (PAPER-2026-073→086, HW-2026-044→049) but produced **no digest and no memory update** — it was interrupted. This digest is the consolidated record for both batches plus Scan #7's own additions (PAPER-2026-087→100, HW-2026-050→054, HYP-2026-022→025, SIM-2026-024).

---

## Executive Summary

- **No contradictions to any published result.** Nothing in 28 new papers challenges α≈4 (stress-tensor force), T=2.250 (transport), or the chi=3 MERA results.
- **Strongest finding — PAPER-2026-088 (Wang & He, rel 5):** the same authors as the hologron-instability paper map the *finite-temperature* critical Ising chain to a mixed thermal-AdS/BTZ black-hole saddle. Our T=2.250 transport is the **zero-temperature limit** of this picture; their BTZ quasi-normal-mode timescale is the same decay physics that killed HYP-017's R1. This is a CONFIRMS + a new testable direction (HYP-2026-024).
- **HYP-2026-014 stays REFUTED — now for the correct structural reason.** SIM-2026-024 tested the PEE-thread / Kirillov-Kostant Crofton measure (the "right" kinematic-space measure) on the same data: α=0.883, all three mandatory guards pass cleanly (regulator-immune, null control clean, PV=hard-cutoff). The integral-geometry route from K[u,v] to F(dr) is itself the structural failure, not the choice of measure. A clean, high-value negative result.
- **HYP-2026-020 shelving independently validated.** PAPER-2026-093 proves the standard Levin-Wen TEE estimator is inflated in stabilizer codes — third-party confirmation that our R4 killer issue (single-basis collision-probability TEE) was real.
- **Roadmap shift (ACTIONABLE):** QuEra qLDPC hardware (HW-044/045) — 96 logical qubits on 448 atoms (Nature 649, 2026), and a simulated 1156-logical / 2304-physical design — directly lowers the fault-tolerant threshold at our 16q transport scale.

---

## Findings by Classification

### CONFIRMED
| Item | Source | Note |
|---|---|---|
| Finite-T holographic dictionary for our Ising chain | PAPER-088 (2603.07639) | T=2.250 is zero-T AdS limit of Wang-He BTZ saddle. SUPPORTS transport + α≈4. |
| Ising CFT exists in Rydberg hardware at spectrum resolution | PAPER-087/073 (2601.16275) | Endres/Sun group measures Ising + tricritical Ising finite-size spectra. Substrate for the holographic signal is hardware-grounded. |
| MERA methodology generalizes beyond Ising | PAPER-092 (2604.19876) | Guo & Swingle extract scaling dims on Z3 chiral clock line — corroborates chi=3 MERA force methodology. |
| HYP-020 TEE estimator was structurally wrong | PAPER-093 (2604.27053) | Independent proof Levin-Wen TEE inflated in stabilizer codes → our R4 confirmed; HYP-020 shelving correct. |
| HYP-014 refuted for the right reason | SIM-2026-024 | PEE-thread Crofton also fails (α=0.883, guards clean). Integral-geometry route is the structural failure. |

### NOVEL
- **PAPER-2026-088** — finite-T critical Ising → mixed thermal-AdS/BTZ saddle (antipodal transport curve, BTZ QNM relaxation, Hawking-Page entropy dip). New quantitative holographic dictionary for the exact system our transport result lives in.
- **math-bridge** — kinematic-space dS₂ (with Crofton = coadjoint-orbit symplectic form) is the common arena for *both* the refuted Crofton force profile and the factor-of-2 transport residual. (Note: the Crofton salvage was subsequently tested and refuted — SIM-024 — but the dS₂ framing for transport stands as HYP-2026-023.)

### ACTIONABLE
- **HW-2026-044 / 045 (QuEra qLDPC, rel 5):** 96 logical / 448 physical demonstrated (Nature 649 pp39-46); 1156 logical / 2304 physical simulated (arXiv 2604.16209). Lowers FT-MERA cost at our 16q transport scale — revisit the FT neutral-atom roadmap numbers.
- **HYP-2026-024** (finite-T BTZ transport) — TESTABLE_NEAR_TERM. Local statevector sim, single-copy imaginary-time state (no doubled TFD register — 2³² exceeds local RAM), β-ladder. Next-cycle compute target.
- **HYP-2026-025** (universality dependence of α: Ising vs Z3) — TESTABLE_NEAR_TERM. Requires new qutrit-MERA state-prep code (force-extraction back-end reusable).
- **HYP-2026-023** (composite-geodesic transport) — NEEDS_REFINEMENT. The dt=0.05 transport grid cannot resolve a 0.72% residual (3.1× below one time step). Unblock: re-run HYP-006 transport at dt≤1e-3 for ≥3 N values (few hours local).

### CONTRADICTS
- **None.** No paper in either batch challenges α≈4, T=2.250, or chi=3 MERA.

### WATCH
- **eleQtron (HW-050):** unverified 10 s coherence claim. If a peer-reviewed benchmark appears it is a ~28,000× record → relevance-5 frontier update. Recheck next scan.
- **Catalog dedup (data-quality):** the interrupted-Scan-6/Scan-7 collision produced duplicate paper records: PAPER-073≈087 (2601.16275 CFT spectra), PAPER-086≈100 (Holographic Network / Traversable), likely PAPER-075≈089 (measurement-based holographic RT). Scan #7's physics-scanner only deduped from PAPER-080. Recommend a dedup pass — **not auto-deleted** (research records; needs explicit sign-off).
- **HYP-2026-025** Z3 qutrit-MERA convergence risk (corroborated by project's own Z2-penalty history).

---

## Cross-Tier Connections

1. **PAPER-088 ↔ HYP-017 R1 ↔ HYP-024.** The BTZ quasi-normal-mode timescale that Wang & He characterize *is* the hologron-decay physics that killed HYP-017 R1. What was a fatal bug in a measurement strategy is, in HYP-024, the *measurement target itself* — a directly-observed relaxation rate in a controlled local sim, not an inferred decayed quasiparticle. The same physics moves from killer to signal.
2. **math-bridge ↔ SIM-024.** math-bridge predicted the PEE-thread measure would salvage HYP-014. The computation tier tested it and it failed cleanly. This is the pipeline working: a plausible theoretical seed, gated, run with mandatory null controls, and honestly refuted. The dS₂ framing survives only for transport (HYP-023), not the force profile.
3. **PAPER-092 ↔ HYP-025.** Swingle group's continued use of MERA for non-Ising criticality both corroborates our methodology and motivates the universality test: is α≈4 a universal stress-tensor signature or Ising-specific?

---

## Interpretive Brief (synthesized by lead — see process note)

> **Process note:** the weekly-scan skill and CLAUDE.md reference a `philosophy-agent` (Tier 3) that is **not installed** in this environment. Interpretation folded into synthesis rather than substituting a different agent.

- **HYP-022 / SIM-024 (epistemic):** The honest reading is "we found the integral-geometry route from the discrete K[u,v] kinematic matrix to F(dr) does not reproduce the holographic force *under any tested measure*." Because the null control (Neel state → α≈0) and regulator-stability guard both passed, we can say this is a property of the construction, not a fitting failure. **Claim ceiling:** *HYP-014's Crofton route is structurally refuted; the holographic force is not recoverable as a kinematic-space chord integral over this boundary-anchored discrete sum.*
- **HYP-024 (finite-T BTZ):** If MERA transport follows the predicted BTZ horizon-absorption curve under thermalization, the defensible statement is "the same CFT data is consistent with a thermal holographic dual," not "we simulated a black hole." **Claim ceiling:** *the finite-temperature critical Ising chain's transport observable is quantitatively consistent with a BTZ saddle, extending the zero-T AdS result.*
- **HYP-025 (universality):** If α≈4 holds across Ising and Z3, that elevates it from a CFT-specific number toward a genuine stress-tensor (geometric) signature; if it tracks the stress-tensor scaling dimension per-class, it is CFT kinematics. Either outcome is informative. **Claim ceiling:** *α's universality-class dependence distinguishes a geometric signature from a CFT-kinematics artifact — not yet established either way.*

---

## ID Ledger (this consolidated cycle)

| Type | Scan #6 (interrupted) | Scan #7 | Highest now |
|---|---|---|---|
| Papers | PAPER-2026-073→086 | 087→100 | **PAPER-2026-100** |
| Hardware | HW-2026-044→049 | 050→054 | **HW-2026-054** |
| Hypotheses | — | HYP-2026-022→025 | **HYP-2026-025** |
| Simulations | — | SIM-2026-024 | **SIM-2026-024** |

## Next Steps
1. **Dedup pass** on PAPER-073≈087, 086≈100, 075≈089 (needs sign-off — research records).
2. **HYP-024** finite-T BTZ transport sim (near-term, local).
3. **HYP-023** unblock: finer-dt (≤1e-3) HYP-006 transport re-run at N=12,16,24.
4. **HYP-025** scope qutrit-MERA code effort before committing.
5. Recheck eleQtron coherence claim next scan.
6. Frontier table: unchanged (96 logical QuEra already current in knowledge-base.md from Scan #6).
