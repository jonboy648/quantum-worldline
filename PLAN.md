# Quantum Worldline — Plan of Record

**Updated:** 2026-08-06 (C_TTT Ising passed; paper v5 + Zenodo v4 published; PRD submission in flight).
Branch `public-release`; all commits LOCAL (not pushed, per standing pref). Read with `NEXT-SESSION.md`
(hot state) + `TASKS.md` (actionable queue) + `research/RESEARCH-LOG.md` (narrative). Latest commit: `6e936e1`.

> **HEADLINE (as of 2026-06-27): α=4 is UNIVERSAL across THREE unitary 2D CFT classes.**
> Ising c=1/2 (HYP-008) → tricritical Ising c=7/10 (HYP-027, SIM-051/052) → 3-state Potts c=4/5 (HYP-025,
> SIM-057). Best-basin Δ_T = 1.998 / 2.007 / 1.997 → α ≈ 4 in every class; Δ_T clusters ~2.0 across all
> basins (the universal-dimension fingerprint). This is the CFT theorem made numerical: Δ_T=2 in every
> unitary 2D CFT ⇒ α=2Δ_T=4. The boundary of the law was also probed: HYP-028 (does α=4 survive LOSS of
> unitarity?) is OPEN — the ED route is CLOSED (Yang-Lee fixed point is PT-inaccessible at N≤16).

---

## North star
**Is the holographic force exponent α=4 (= 2·Δ_T, stress-tensor exchange) a universal feature of emergent
holography?** Answered for unitary 2D CFTs (YES, 3 classes). The frontier now: (a) does it survive
non-unitarity / extend to the de Sitter sector (HYP-028, OPEN); (b) can we reach *interaction*-level bulk
physics — the OPE structure constant C_TTT = emergent graviton self-coupling.

> **UPDATE 2026-07-19 — (b) is now PARTLY ANSWERED.** C_TTT was extracted successfully on Ising:
> **3.9936 vs exact 4.000 (0.16%)**, via the circle / Koo-Saleur matrix-element route (SIM-067), after
> the MERA-native one-site route was closed as a structural negative (SIM-066: the one-site scaling
> superoperator is isometry-only and breaks the translation covariance spin-2 requires — falsified as a
> finite-χ effect by escalating to χ=12). Conformal spin is only a genuine quantum number on the
> **circle**, not on the line, which is why periodic-chain ED succeeded where width-2 MERA could not.
> TCI (3.381) and Potts (3.162) remain blocked on system size, not method: L₋₂ε contaminates T with
> identical quantum numbers and dies only as ~N^-0.2, requiring N ≈ 64–128 via puMPS.
>
> **UPDATE 2026-08-06 — publication status.** Paper v5 complete with ERRATA E1–E5 applied; Zenodo v4
> published 2026-07-15 (concept DOI 10.5281/zenodo.19660302); PRD submission draft `es2026jul20_951`
> open at authors.aps.org, 5 of 8 steps done, blocked on two manual portal actions. Outreach batch
> (7 targets) fully sent and fully unanswered as of 2026-08-04.

---

## Status snapshot (2026-06-27)

### DONE — SUPPORTED + committed (the spine)
- **HYP-008** α=4 in critical Ising (c=1/2): 3 converging measurements (24q/16q exact + χ=3 MERA).
- **HYP-006** holographic transport = AdS₃ null geodesic T=(π/2)·l_AdS (~-1.2% N=16, ERRATA E2).
- **HYP-026** Synge distance geometric but FORCE-BLIND (κ_chord≈2Δ_σ ≠ α=4); distance ≠ force (SIM-031).
- **HYP-027** α=4 UNIVERSAL at tricritical Ising c=7/10: χ=6 Δ_T=2.007→α=4.01 (SIM-051); χ=8 full M(4,5)
  spectrum (SIM-052). OF blocking proven correct (exact-diag pre-gate); old blocker was a wrong-basin
  artifact (energy flat at χ=6, select by spectrum). See [[of-blocking-was-never-wrong]].
- **HYP-025** α=4 at a THIRD class, 3-state Potts c=4/5 (SIM-057, 2026-06-27): best basin Δ_T=1.997→α=3.994,
  Δ_ε=0.86 IDs c=4/5. SUPPORTED-with-caveat (Δ_σ unresolved at χ=6 = same ceiling as TCI χ=6).
- **HYP-029** static α=4 force fits a ~4.5k-qubit digital-FT STAR budget (SIM-054); SUPPORTED-conditional.

### DONE — honest negatives (the gates worked, no false positives)
- **HYP-028** Yang-Lee non-unitary force: ED route CLOSED (SIM-053 + SIM-055). The M(2,5) fixed point sits
  at/beyond the PT-breaking edge at N≤16 across THREE realizations; no honest non-unitary α extractable by
  ED. OPEN; next is a non-Hermitian MERA or PT-inner-product reformulation. See [[frontier-runs-yanglee-ope]].
- **OPE C_σσε extraction** (SIM-056): validation FAILED — the naive ternary ρ³ is geometrically wrong
  (needs the full causal cone incl. inter-block disentanglers). χ is NOT the blocker. Method fix needed
  before C_TTT. See [[frontier-runs-yanglee-ope]].
- **HYP-014/022** (Crofton route) REFUTED; **HYP-017** (analog Aquila) SHELVED.

### OPEN — the live frontier (ranked in the plan below)

---

## The plan (ranked, 2026-06-27)

### P1 — χ=8 Potts sharpening [CHEAP, closes the just-finished result]
Resolve Δ_σ→0.133 at the 3-state Potts point (best basin gave 0.070 at χ=6). Local, ~45min/seed, mirrors
exactly how SIM-052's χ=8 run sharpened the tricritical case. Turns HYP-025 from SUPPORTED-caveat (medium)
into a clean high-confidence full-spectrum confirmation. Driver: adapt `qw_potts_measure.jl` to χ=8.

### P2 — Fix the OPE ρ³ contraction → extract C_TTT [the genuinely-novel frontier]
The only path toward *interaction*-level bulk physics (C_TTT = emergent graviton self-coupling; lattice OPE
extraction is near-empty in the literature). Local TensorKit task: rebuild ρ³ with the full width-3 causal
cone (inter-block disentanglers) or the PEV coarse-grain-until-adjacent algorithm. Re-validate C_σσε→0.5
AND C_σσσ→0 (Z₂ parity) on Ising BEFORE any C_TTT. THEN a RunPod A100 χ=10-12 run (~$10-20) for a clean
number. See [[frontier-runs-yanglee-ope]] for the diagnosed bug.

### P3 — HYP-028 non-Hermitian MERA route [harder, OPEN]
The ED route is closed. A genuine non-unitary α test needs a non-Hermitian MERA (large effective size where
the bulk Yang-Lee window opens) or a metric/PT-inner-product reformulation. Code does not yet exist; this is
new-method work, not a sim run. Lower priority than P1/P2.

### P4 — Paper integration [gated on SciPost/arXiv access]
- ✅ SIM records, RESEARCH-LOG, MEMORY all current through SIM-057.
- REMAINING: fold the universality result into the paper (v5 section or a short companion note) when
  SciPost/arXiv unblocks. Consider a 2-3 paragraph result block: "α=4 is not Ising-specific — it is the
  stress-tensor dimension Δ_T=2, universal in every unitary 2D CFT, verified numerically at c=1/2 and
  c=7/10." Optional χ=8 sharpening of the non-universal TCI primaries (Δ_σ, Δ_ε) — not needed for α.

---

## Standing threads (independent of HYP-027)
- **QuEra Gemini email** — sent 2026-06-16 (thread 19ed11650e5ed845); follow up ~2026-06-30 if no reply.
- **Paper v5** — fold ERRATA E1–E5 into the LaTeX when SciPost/arXiv unblocks (blocked on affiliation).
- **Companion note** — `research/note-synge-force-blind.tex` ready to post as an arXiv companion.
- **SciPost/arXiv endorsement** — blocked on independent-researcher affiliation (Azure $500/provider +
  QuEra are the documented end-runs).

---

## Environment / reproducibility notes
- **MERAKit:** Julia 1.8.5 (NOT 1.12 — CUDA/TensorKit-1.x API breaks). Run via
  `research/tools/merakit-setup/RUN-MERAKIT.md` (essential env: clean HOME with readable empty
  `.ssh/known_hosts`; `JULIA_PKG_SERVER=https://pkg.julialang.org`; pinned Project.toml; χ=6 by
  direct-init NOT `expand_bonddim` which LAPACK-crashes).
- **From-scratch superop code:** sim045 (stable EV loop), sim048 (Riemannian CG), read_spectrum.py — all
  validated at χ=4; kept for cross-checks but superseded by MERAKit for χ≥6.
- Commits stay local; never commit .mcp.json / paper drafts / RunPod key. RunPod not needed (MERAKit is
  local).
