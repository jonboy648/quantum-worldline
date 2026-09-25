# Weekly Scan — 2026-06-08 (Scan #8)

**Window:** 2026-05-13 → 2026-06-08 (~4 weeks; first scan since #7 on 2026-05-12)
**Method note:** The `paper-search` arXiv MCP endpoint is currently **query-blind** — it ignores the search string and returns the latest-submission firehose regardless of keywords (verified: "twisted bilayer graphene Majorana" and "holographic MERA force" returned identical result sets). Google Scholar endpoint returned empty (rate-limited). **This scan was run by hand via the arXiv export API through WebFetch**, which honors field-prefixed queries (`abs:...`). Five topic threads, results screened against our anchors. See [[feedback-mcp-outage-resilience]] — this is a new failure *mode* (query-blind, not hung): the connection is up but the search is useless.

---

## Executive Summary

- **No contradictions to any published result.** Nothing found challenges α≈4 (stress-tensor force), T=(π/2)·l_AdS=2.250 (transport), or the chi=3 MERA results.
- **Task #95 ADAPT-VQE scaling settled:** faithful-prep 2q-gate count is **L=8→25, L=10→35** — linear **+5 gates/site (p=1.51)**; the cheap-prep cost grows with system size (kills generalization). chi=3's cost is **optimizer-limited, not fundamental** at L=8 (ADAPT escapes the #92/#94 plateau). (L=12 leg killed mid-run at step 36; would confirm p≈1.5, not change it.)
  **CORRECTION (same-day full-project audit, ERRATA.md D4):** this digest originally repeated the verification's "33 vs real-MERA-ask ~36 = wash" killer. That was **inverted**: `pytket_compile_chi3_8q_results.json` records **451 ZZPhase as the REAL compile of the actual chi=3 8q/2L QCUP circuit** (16q register is correct for it); "36" was a pre-compile estimate. **ADAPT 33 vs chi=3 451 = genuine ~13.7× (≈10× HQC).** QCUP still does not reopen today — fragile basin (≤0.1% angle precision), ADAPT-is-not-a-MERA framing, thread administratively HELD — but the gate-count economics are real if those change.
- **Most relevant new paper — 2605.21447 (Schuhmacher, Baiardi, Tacchino, Tavernelli, IBM, rel 2026-05-20):** "Combining non-parametric quantum states and MERA tensor networks for ground-state optimization" — hybrid quantum-annealed + classical MERA for the transverse-field Ising model, improving GS accuracy **without increasing circuit depth**. This is adjacent to our task #95 (ADAPT-VQE cheap-circuit question) and to HYP-002. Abstract gives no gate counts; flagged for a full read.
- **Direct anchor confirmation — 2501.03084 (Wang & He) resurfaced as the canonical "stable excitations + holographic transportation in critical-spin-chain tensor networks" paper.** This is already our HYP-024 / transport foundation; no change, but it is the live state-of-the-art and nothing has superseded it.
- **Hardware frontier moved (ACTIONABLE).** A fresh wave of 2026 milestones: trapped-ion **qLDPC breakeven** (4 logical / 18 physical, 9× better logical error than prior; 2606.06455), Atom Computing **toric code to 90 syndrome rounds** with reloading (2606.04079), Yb tweezer readout at **99.89% discrimination fidelity** (2605.24175). Continues the FT-neutral-atom trend from Scan #7's QuEra qLDPC.
- **No experimental emergent-gravity-on-hardware paper exists yet.** A dedicated thread ("holographic principle / emergent gravity realized on a quantum simulator") returned **zero** direct hits — the niche our HYP-017 targeted remains experimentally unoccupied. (Closest activity is entanglement-transition measurement on QuEra Aquila, 2604.24854 — substrate, not signal.)

---

## Findings by Classification

### CONFIRMED / ANCHOR-STABLE
| Item | Source | Note |
|---|---|---|
| Hologron stability + holographic transportation in critical-chain tensor networks | 2501.03084 (Wang & He) | Our HYP-024 / transport foundation. Still the SOTA; nothing supersedes it. "Stable bulk excitations with attractive interactions" + boundary holographic transportation = exactly our α≈4 + T=2.250 picture. No change to anchors. |
| MERA-style hybrid GS prep generalizes for TFIM | 2605.21447 (Schuhmacher et al., IBM) | Combining annealed non-parametric states + classical MERA improves Ising GS accuracy without deeper circuits. Corroborates that critical-Ising GS prep is an active, tractable target (relevant to #95). |
| Energy transport across CFT interfaces is holographically controlled | 2506.19553 / 2503.20399 (Liu, Wang, Zeng) | AdS₃/CFT junction transport: transmission coefficients vary monotonically with brane tension. Same holographic-transport family as our boundary transport; no conflict, possible cross-check for HYP-023 composite-geodesic framing. |
| KSS viscosity bound ↔ causality in holographic systems | 2604.04222 (Prokhorov, Teryaev) | Tangential: universal transport ratios from holography. Background support for "transport is holographically constrained," not a direct test. |

### NOVEL / WATCH
- **2605.21447 (IBM, MERA + non-parametric hybrid GS prep) — FULL READ DONE 2026-06-08. Orthogonal to #95, does NOT challenge it.** Method: a quantum-annealed state (fixed 200-two-qubit-gate circuit) is used as a **fixed boundary resource via classical shadows**, and a *classical* isometric MERA (bond dim χ_l=2^(2^l), 1-2 layers) is variationally optimized on top. TFIM at **N=12 and N=24, critical (λ=1, J ramped to |J|=λ)**. Result: adding the classical MERA improves GS-energy **>5× at N=12, >2× at N=24** at fixed circuit depth; needs S=10^5 (N=12) to ~10^6 (N=24) shadow snapshots; robust to noise η=0.1–10. **Why it doesn't touch #95:** their quantum circuit is *fixed and shallow*; the heavy lifting is classical post-processing. Our #95 question was "can a *quantum circuit* prepare critical-GS+force cheaply?" — a different decomposition. So #95's no-go stands. (Possible future synergy: their classical-shadow + classical-MERA energy refinement could *sit on top of* our ADAPT state — but that imports the same √-shots cost and doesn't help the hardware-force-measurement problem.)
- **2508.16570 (Qasim, Eisert, Jahn) — "Emergent statistical mechanics in holographic random tensor networks"** — equilibration dynamics on hyperbolic-geometry RTNs under generic Hamiltonians. WATCH for whether their "hierarchical holographic DOF counting" gives an independent handle on bulk excitation lifetimes (the HYP-017 R1 decay physics).
- **2512.11967 (Kobayashi, Sappler, Pollmann) — holographic isoTNS** — embeds D-dim systems in (D+1)-dim isometric networks; volume-law at fixed bond dimension. WATCH as an alternative bulk-from-boundary ansatz; not MERA, but same "extra dimension = geometry" thesis as HYP-001.
- **2409.17235 (Saraidaris, Jahn) — "Critical spin models from holographic disorder"** — generic Hamiltonians on holographic-disorder tensor networks still hit CFT scaling. Mild support for robustness of the chi=3 force methodology under disorder (cf. HYP-015).

### ACTIONABLE
- **Hardware roadmap refresh (carry-forward + new):** trapped-ion qLDPC breakeven (2606.06455, 4L/18P, 9× better logical error) + Atom Computing toric-code 90-round (2606.04079) + Yb 99.89% readout (2605.24175). Combined with Scan #7's QuEra 96L/448P, the FT-neutral-atom threshold keeps dropping. **Revisit HYP-016's FT-MERA cost numbers** (last estimate: 1839 atoms, 8 min) against this new fidelity/logical-qubit frontier.
- **Full read of 2605.21447** — see if IBM's depth-vs-accuracy curve for TFIM GS prep independently corroborates or challenges the task-#95 conclusion (chi=3 cost is optimizer-limited at L=8, but scales with L).
- **No new hypothesis warranted this cycle.** Nothing surfaced that isn't already covered by HYP-023/024/025 or the closed HYP-017. The experimental emergent-gravity niche remains open but no cheaper route to it appeared.

### CONTRADICTS
- **None.** No paper in any of the five threads challenges α≈4, T=2.250, or chi=3 MERA.

---

## Exploratory pass (off-paper-path, 2026-06-08)
General-web sweep for ideas/routes NOT on the arXiv→SciPost→QCUP track. Findings:

**Non-paper routes to create value (ranked by EV):**
1. **IBM Quantum Credits program** — free QPU access, 30,000+ compute-hours granted to date, 5–10 hr/project. **BLOCKER: eligibility = "tenure-track or permanent academic staff at a research institute"** → as an independent researcher, Jon is **ineligible** as written. (Same gate as arXiv endorsement.) Low EV unless an academic co-author is added.
2. **Azure Quantum Credits — $500 free per provider (IonQ, Quantinuum, …) on sign-in**, no academic-affiliation gate mentioned, "more credits for approved research." **This is the most promising non-paper route**: $500 of Quantinuum time ≈ enough for a small real hardware run *without* the QCUP HQC-budget fight or academic eligibility. **ACTIONABLE: verify current Azure Quantum free-credit terms + whether independent researchers qualify.** (Caveat: the #95 verdict says we have no *worth-running* circuit right now — but this changes the cost calculus if a future circuit clears the noise bar.)
3. **Oak Ridge QCUP** — already our path; US researchers can apply, reviewed by QRUC. Status unchanged (blocked on HQC clarification + we have no go-worthy experiment).
4. **Unitary Foundation** (community quantum-access resource) — worth a look as a non-institutional channel; not yet evaluated.

**Adjacent-field tool-reuse (where our machinery could be a tool, not a paper):** searched tensor-network ML / Kaggle / open datasets — returned generic TN-ML literature, **no obvious competition or dataset where our α≈4-force / MERA-transport code is directly the needed tool.** No clear off-ramp here this pass.

**New physics idea surfaced (WATCH, not ours to chase now):**
- **2505.07102 (Raasakka) — "Emergence of gravity from QFT in triangulated spacetime / QFT vector model"** + follow-up **2507.16346 ("Induced quantum gravity from QFT vector models")**. Compositional-QFT + tensor-network route to emergent gravity, unifying causal dynamical triangulations / random tensor models / group field theory / holography. Free massive scalar in 2D Lorentzian as the worked example. **Relevance:** a *different* emergent-gravity-from-tensor-networks lineage than our MERA/AdS-CFT one — potential cross-framework bridge (the kind of thing math-bridge exists to find), but not a near-term experiment. Flagged for a future theory-tier look, not actioned.
- **2405.02380 ("Emergent gravity from correlation of spin-½ systems coupled with a scalar field")** — adjacent spin-system→gravity route; WATCH.

**Bottom line of exploratory pass:** the one genuinely new lever is **Azure's $500/provider free credits** as a possible end-run around the QCUP/academic-eligibility blockers — but it only matters once we have a circuit worth running, which #95 says we currently don't. No new physics direction compelling enough to divert from the published-paper track. The triangulated-spacetime/QFT-vector-model lineage is the most interesting *theory* thread to revisit later.

## Hardware Frontier (this window)
| Milestone | arXiv | Date | Number that matters |
|---|---|---|---|
| Trapped-ion qLDPC **breakeven** | 2606.06455 | 2026-06-04 | 4 logical / 18 physical; logical error up to **9× better** than prior superconducting demo |
| Atom Computing toric code, repeated cycles | 2606.04079 | 2026-06-02 | up to **90 syndrome rounds** with qubit reloading, logical error preserved |
| Yb tweezer minimally-destructive imaging | 2605.24175 | 2026-05-22 | **99.89% discrimination fidelity**, 98.80% survival, 17.6 µs |
| Sr mid-IR tweezer platform | 2606.02560 | 2026-06-01 | high-fidelity single-atom prep + resolved-sideband cooling (new species/transition) |
| Penning-trap site-selective control | 2606.00940 | 2026-05-31 | Rz(π) **94.6%**, NN crosstalk 1.2% (rotating crystal addressing) |
| Trapped-ion thermodynamic-limit dispersion | 2605.28599 | 2026-05-27 | 20-qubit QPU, VQE + adiabatic prep for TFIM (measurement-noise limited) |

**Read for our roadmap:** the FT-neutral-atom and trapped-ion logical-qubit frontier keeps advancing (qLDPC breakeven + 90-round toric code this window, on top of Scan #7's QuEra 96L/448P). None of it changes our *physics* anchors, but it lowers the fault-tolerant cost for the 16q-transport / MERA-on-hardware path — the standing ACTIONABLE is to refresh HYP-016's FT-MERA estimate (1839 atoms / 8 min) against these numbers. **Note for #95:** 2605.28599 independently confirms the measurement-noise wall for VQE/adiabatic TFIM prep on real hardware — consistent with our finding that the ADAPT state's force observable is noise-fragile.

## Method / Coverage caveats
- **paper-search MCP is query-blind right now** (returns latest-submission firehose regardless of keywords; Google Scholar endpoint empty). This scan used the arXiv export API via WebFetch instead, which honors `abs:`-prefixed queries. Coverage is therefore **arXiv-only** for this cycle (no bioRxiv/medRxiv/PubMed, which weren't relevant anyway).
- **Five topic threads run** (tensor-network holography; MERA/bond-dimension; holographic transport/BTZ; neutral-atom/ion hardware; variational/ADAPT GS-prep; emergent-gravity-on-simulator). Each capped at 12-15 results, screened by abstract. This is a **focused** scan (new-paper-wise, per request), not the full 3-tier orchestrated sweep.
- **No deep PDF reads completed** beyond abstract-level except 2605.21447 (abstract only — full text not retrieved). The one ACTIONABLE read (2605.21447 full text) is deferred.
- **Not catalogued to JSON** (`research/data/papers/PAPER-*.json`) this cycle — the MCP download path is unreliable and the find-by-ID step needs the working MCP. Findings recorded in this digest; formal catalog entries deferred until the MCP search is fixed or done by hand. Last reliable catalog high-water marks (from MEMORY): PAPER ~100, HW ~054, HYP 025, SIM 030.

## Catalog
**New papers worth tracking (not yet assigned PAPER-IDs — see caveat above):**
| Ref | Title (short) | Relevance |
|---|---|---|
| 2605.21447 | MERA + non-parametric hybrid GS prep (IBM) | NEAREST to #95 — TFIM GS, no deeper circuits. READ FULL. |
| 2508.16570 | Emergent stat-mech in holographic RTNs (Eisert/Jahn) | WATCH — bulk DOF / equilibration ↔ hologron lifetime |
| 2512.11967 | Holographic isoTNS (Pollmann) | WATCH — extra-dim geometry ansatz, cf. HYP-001 |
| 2506.19553 / 2503.20399 | Holographic junction/interface transport (Liu et al.) | cross-check for HYP-023 transport framing |
| 2409.17235 | Critical spin models from holographic disorder (Jahn) | mild support for chi=3 force robustness (cf. HYP-015) |
| 2606.06455 | Trapped-ion qLDPC breakeven | HW frontier — FT cost ↓ |
| 2606.04079 | Atom Computing toric code 90 rounds | HW frontier — FT cost ↓ |
| 2605.24175 | Yb tweezer 99.89% readout | HW frontier — readout fidelity |
| 2605.28599 | TFIM dispersion on 20q ion QPU | confirms VQE/adiabatic measurement-noise wall (cf. #95 noise finding) |

**Anchors re-affirmed:** 2501.03084 (Wang & He) remains the SOTA hologron/transport reference; nothing supersedes it.

**Catalog hygiene carry-over (still open from Scan #7):** PAPER dupes 073≈087, 086≈100, 075≈089 (scan-6 collision) — still NOT deleted, needs sign-off.
