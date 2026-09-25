# Quantum Worldline — Task List

**Updated:** 2026-08-06. Read with `NEXT-SESSION.md` (hot state) + `research/RESEARCH-LOG.md` (narrative)
+ `research/ERRATA.md` (before quoting any published number).
Branch `public-release`; commits LOCAL, never pushed. Latest commit: `6e936e1`.

> **This file was rewritten 2026-08-06.** The previous version (dated 2026-06-18) described HYP-027 as an
> open blocker with four sub-tasks. That work has since completed and the hypothesis is SUPPORTED — the
> stale content was actively misleading and was removed rather than archived. Historical detail lives in
> `research/RESEARCH-LOG.md` and in memory `[[of-blocking-was-never-wrong]]`.

---

## Critical path — publication

- [x] **⛔ REJECTED BY PHYSICAL REVIEW D — 2026-08-12. Branch CLOSED.**
      Desk rejection from `prd@aps.org`, **Dr. Alin Tirziu, Senior Editor**, 18:16 UTC
      (Gmail id `19ff730cc7add0c1`, DKIM/SPF/DMARC pass): *"Regrettably, this manuscript fails to
      match the minimal threshold for the APS journals. APS will not consider this manuscript
      further."* No referee reports; no transfer offer.
      - **Found 2026-08-17, five days late.** This entry, memory, and `RESEARCH-LOG.md:1031` all
        said "With editors" — three same-origin notes written on 08-07, agreeing with each other and
        with nothing external. Last real inbox check was 08-04; the reply-watcher cron had expired.
        Caught only when Jon asked whether we had editors at all and the inbox was checked instead
        of the notes. **§7 of the governing standard, in our own operations.**
      - **Independent of the alpha retraction.** The rejection (08-12) predates the audit's finding
        (08-17). Tirziu rejected on scope/threshold; nothing indicates he saw the estimator defect.
        Do not narrate this as "rejected for the error" — and do not treat the rejection as
        validating the error either. The two are unrelated facts.
      - **Consequence:** nothing is owed to APS, and no journal record exists to correct. The whole
        correction obligation moves to **Zenodo** (see below).
      - Historical submission detail follows, retained as the record of what was submitted:
      **Accession Code: `DV13971`** · Status: ~~With editors~~ **REJECTED** · Type: Regular Article ·
      Section: *String theory, quantum gravity, gauge/gravity duality* (auto-routed by the PhySH
      primary term). Temporary ID `es2026jul20_951` is retired.
      - Manuscript PDF uploaded 07Aug2026 11:55:31 — the corrected build citing the **concept** DOI
        10.5281/zenodo.19660302. Verified: the old version DOI (19661227) appears nowhere.
      - Cover letter pasted as text (3,584 chars, concept DOI). `cover-letter-prd.md` had the same
        version-DOI defect as the manuscript; fixed 2026-08-07.
      - PhySH: primary **Gauge-gravity dualities** (under the Particles & Fields discipline, which had
        to be added — the term is unreachable without it). Only that one concept transferred; valid
        (minimum 1) and it produced the correct section routing.
      - Suggested Referees intentionally left blank; the cover letter offers them on request.
      - Categories: Theoretical. 6 figures, none in color (no charges). Author unaffiliated, so no
        institutional OA agreement applies and no APC is owed.
- [ ] **Watch for the editor decision.** Confirmation should have gone to joncackler@gmail.com.
      Typical PRD first response is weeks; a desk rejection would arrive sooner.
- [ ] **arXiv endorsement** — still blocked on the unaffiliated-researcher gate. Zenodo concept DOI
      10.5281/zenodo.19660302 remains the public record.
- [ ] **Rotate the APS password** — it passed through a session transcript on 2026-07-20.
      Stored in gitignored `CREDENTIALS-APS.local.md`.

## Outreach — batch sent, all silent

Sent 2026-07-15 (Orth, Swingle, Sahay, He, Czech, QuEra follow-up) + Evenbly 2026-07-19. Iadecola went
silent through the 07-13 deadline; that branch is closed.

- [x] Batch sent, all citing the v4 DOI
- [ ] **Zero replies as of 2026-08-04** (inbox verified, all 80 messages since 07-19 — no target, no APS,
      no SciPost). Day 20 past send. The plan was "give it ~10 days, then PRD regardless" — that deadline
      passed 07-25, so the PRD submission above is the live path, not a fallback.
- [ ] Verify the cloud reply-watcher's Gmail connector is bound to joncackler@gmail.com
- [ ] Discard 6 stale Gmail drafts (superseded by the sends) — user action, Gmail UI only

## Live science thread — C_TTT continuation

- [x] **Route A CLOSED** (SIM-066, honest negative, 07-16) — one-site PEV superoperator is isometry-only,
      breaks the translation covariance spin-2 requires. Falsified the finite-χ explanation at χ=12.
- [x] **Route B ISING PASSED** (SIM-067, 07-19) — circle / Koo-Saleur matrix elements.
      **C_TTT = 3.9936 vs exact 4.000 (0.16%)**, c → 0.49871, C_σσε pin → 0.49996, wrong-chirality
      element a structural zero at every N. Driver: `research/tools/cttt-circle/qw_cttt_circle.py`.
- [ ] **TCI (target 3.381) and Potts (target 3.162) — UNBLOCKED 2026-08-09.** L₋₂ε sits 0.2 above T
      with identical quantum numbers; contamination dies only as ~N^-0.2, so ZMV needed N ≤ 128 puMPS on
      the same O'Brien-Fendley model.
      - **THE ZMV CODEBASE IS PUBLIC: `yijian-physics/puMPS`** (found 2026-08-09; the 2026-07-20 "no
        public puMPS exists" check was too narrow — it looked only for `amilsted/puMPS`, and every
        search engine stems "puMPS"→"pumps"; searching the exact phrase "periodic uniform matrix
        product" finds it instantly). It is the authors' own code (Zou-Milsted-Vidal 2017, refreshed
        for Julia 1.11 on 2025-09-14) and ships **everything**: `excitations!` Bloch solver,
        `Hn_in_basis` Koo-Saleur matrix elements, and `_Hn_MPO_split` builders for Ising,
        **O'Brien-Fendley**, and **3-state Potts**. From-scratch build CANCELLED.
      - Vendored (gitignored, no upstream license) at `research/tools/puMPS/`, commit `0557b12`;
        tracked mirror + plan of record: `research/tools/pumps-setup/VENDOR.md`. MIT fallback:
        `FuTen/puMPS.jl` (Milsted's packaging). Julia 1.12 default channel, NOT MERAKit's +1.8.
      - [x] **Validation gate PASSED 2026-08-09** (N=12 D=8): Δ_σ=0.1252, Δ_ε=0.9972,
            Δ_T=1.9604, c=0.4972 both chiralities (equal to 1e-6), **C_TTT=4.011 vs exact 4**;
            T-discrimination clean (competing element 6400× smaller). Results table in VENDOR.md.
      - [x] OF convention mapped: λ1=1, λ2=λ3/2=0.428 = our TCI point (verify vs ED at N=12
            as production step 0).
      - [ ] **Production driver next session:** `qw_pumps_cttt_of.jl` with JLD2 GS checkpointing
            (two background runs were externally killed mid-N=16 — checkpoint after GS converge,
            resume flag). Use `puMPS.minimize_energy_local_CG!` (not exported). OF at N=24 (ED
            cross-check vs qw_cttt_circle.py) → N=64 → 96 → 128, D ramped; v CALIBRATED not
            assumed. Target C_TTT = 3.381. Then potts3, target 3.162.
      - **Dead ends already tested (do not retry):** ground-state-only c = 2‖H₋₂|0⟩‖² (UV-divergent,
        c grows ~0.5N); summing elements over the near-degenerate |s|=2 doublet (overshoots). The
        single-state matrix element remains the correct filter; only N was the blocker.
      - Design + addenda: `research/tools/merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md` (§7 records the
        falsified equal-time ⟨hh⟩/⟨hhh⟩ design — do not reuse those formulas).

## Standing / lower-priority

- [ ] **HYP-028** (does α=4 survive loss of unitarity?) — OPEN/INCONCLUSIVE. ED route CLOSED: the
      Yang-Lee fixed point is PT-inaccessible at N ≤ 16 in every realization tried. Next step per the
      scan-#14 and scan-#18 notes: reproduce PAPER-133's (2606.16785) periodic PT-chain / left-dual
      boundary-data extraction on our lattice plumbing **before** building any non-Hermitian MERA, now
      with PAPER-138's S_res = log(Δ·L) as a secondary diagnostic. That diagnostic does **not** satisfy
      the mandatory G4 criticality gate (c_eff = 2/5 AND Δ_φ = −1/5).
- [ ] **HYP-030** (c=1 compact-boson moduli line) — a fourth universality-class test, seeded scan #15,
      not yet started.
- [ ] **Companion note** — `research/note-synge-force-blind.tex` ready to post as an arXiv companion.
- [ ] **Scan #19** — overdue (was due ~2026-08-03). Run queries **sequentially**; parallel fan-out trips
      the arXiv export-API burst limiter and silently drops query lines (scan #17 lesson, fix held in #18).

## Credentials — never in this file

APS portal credentials live in `CREDENTIALS-APS.local.md` (gitignored). Zenodo token at
`~/.zenodo-token`. RunPod key in the `RUNPOD_API_KEY` environment variable. The previous version of this
file contained a partial RunPod key string; it has been removed. Consider rotating the APS password,
which passed through a session transcript.
