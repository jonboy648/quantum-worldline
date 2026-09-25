# inv:sims-late — Audit of SIM-2026-056 … SIM-2026-071

**Auditor scope:** the current frontier — OPE parity work (056–064), C_TTT Route A closure (065/066),
the C_TTT ladder (067/068/069), and the Yang-Lee biorthogonal work (070/071).
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` §§5, 6, 7, 8, 12, 20, 21, 36, 38.
**Date of audit:** 2026-08-17. **Stance:** overclaim-hunting, not encouragement.

Everything below is cited to a repo-relative path plus the specific field or line relied on.
Where I recomputed a number myself, I say so and give both the record's value and mine.

---

## 0. Headline of this audit

Three findings dominate. They are stated here and evidenced in the per-record sections.

**F1 — The "C_TTT ladder" contains no three-point measurement.**
`SIM-2026-067/068/069` measure the central charge `c` from a **two-point** Koo-Saleur matrix
element and then apply the exact Virasoro identity `C_TTT = 2√2/√c` as a change of variables.
The method fields say so explicitly
(`research/data/simulations/SIM-2026-068.json` field `method`: *"c = 2|<T|H_{+-2}|0> \* N/(2 pi v_T)|^2;
C_TTT = 2\*sqrt(2)/sqrt(c)"*; identical construction in `SIM-2026-069.json` `method` and
`SIM-2026-067.json` `design_evolution`). `⟨T|L_{-2}|0⟩` with `|T⟩ = L_{-2}|0⟩` **is** the Virasoro
norm `⟨T|T⟩ = c/2`. Reporting `C_TTT = 3.381 vs exact 3.3806` is therefore exactly as informative as
reporting `c_inf = 0.699 vs exact 0.700` — it is one number, not two, and it is
**algebraically equivalent** in the §7 sense. The genuine three-point contraction was attempted in
Route A (`SIM-2026-065`, `SIM-2026-066`) and **failed**; Route B silently substituted a two-point
observable for it. No record in the block flags that the measured object changed.

**F2 — SIM-2026-071's two claims have radically different evidential strength, and the record
merges them.** "c_eff = +2/5 EXCLUDED" is robust: the sign is negative at every L, in both
chiralities, machine-real (verified directly in
`research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl`, all five lines). "c_KS = true c = −22/5"
is not: the largest-L raw datum is `c_KS(L=18) = −2.356`, and the quoted `−4.29` is produced by an
extrapolation that supplies **82 % of the final magnitude**, whose tail term rests on a geometric
ratio estimated from **two** samples. The record's own framing ("PASSED (discrimination decisive)")
is correct for the sign and overstated for the magnitude.

**F3 — Raw evidence is missing for seven of the sixteen records, and for the strongest claim's only
control.** Every scratchpad log cited as evidence by SIM-060/061/062/063/064/065/066 is absent from
the repository (verified by `find`). The SIM-2026-071 unitary control (`0.517483 / 0.512776 /
0.509748 → 0.49986`) exists **nowhere in the repo except the SIM-071 JSON itself** (verified by
repo-wide grep). SIM-067/068/069/070 are, by contrast, exemplary.

---

## 1. Verification method

I did not take the records on trust. For each I:

1. read the JSON in full;
2. located the driver and the raw output file, if any;
3. re-derived the headline numbers from the raw data where raw data existed;
4. re-ran the record's own stated estimator to see whether it reproduces the quoted value;
5. tested the estimator's sensitivity to its own free choices.

Raw sources actually opened:
- `research/tools/yanglee-pt/qw_yanglee_ks.jl` (full source, 152 lines)
- `research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl` (5 stages)
- `research/tools/yanglee-pt/yl_proj.log`, `yl_run_8_18.log`
- `research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md`
- `research/tools/pumps-setup/qw_cttt_of_results_2026-08-10.jsonl` (10 stages)
- `research/tools/pumps-setup/qw_cttt_potts3_results_2026-08-11.jsonl` (11 stages)
- `research/tools/pumps-setup/VENDOR.md`
- `research/tools/cttt-circle/qw_cttt_circle_results_ising.json` (6 stages)
- `research/data/hypotheses/HYP-2026-028.json`
- `research/ERRATA.md`, `research/RESEARCH-LOG.md`, `research/paper-draft-scipost.tex`

---

## 2. Per-record audit

Format per §38A: id, date, title, measurement, pipeline, verdict, supported claim, reproducibility
metadata present vs absent, verdict proportionality.

---

### SIM-2026-056

- **Date** 2026-06-26. **HYP** HYP-2026-028 *(mislabelled — see below)*.
- **Title/measurement** OPE structure constant `C_σσε` from ternary MERA at χ=6, validated against
  the exact Ising 0.5.
- **Pipeline** MERAKit.jl ternary MERA, Riemannian LBFGS, χ=6, block_size=2, dense ComplexSpace,
  Julia 1.8.5, single-thread BLAS, 6 deterministic seeds × 900 iters
  (`SIM-2026-056.json` fields `method`, `chi`, `driver`, `env`).
- **Verdict recorded** `"gate_pass": false` — "VALIDATION GATE NOT PASSED".
- **Supported claim** Only a negative one: the v1 `rho3 = w rho1 w'` object is not a
  translation-invariant 3-site marginal. Evidence is strong and internal: across 6 seeds
  `|C_sse|` spans 0.08–17.2 and the **parity-forbidden** `C_sss` spans 0.09–92 while the
  dimensions are clean (`results_all_seeds_chi6`, `best_spectrum_seed`). A quantity that must
  vanish by Z₂ and does not is a decisive falsifier, and the record uses it correctly.
- **Reproducibility present** driver path, env doc, χ, seed count, iteration count, per-seed table,
  determinism protocol, CFT target with source (`cft_target.source` = PEV arXiv:0810.0580 Eq.15).
- **Reproducibility absent** no code revision / commit hash, no raw log file, no runtime, no
  library versions beyond "Julia 1.8.5", no output checksum.
- **Verdict proportionality** **Proportionate, and a model of the culture the standard asks for**
  (§32). `notes` explicitly says *"Real numbers reported, not fudged."*
- **DEFECT (minor, metadata):** `hypothesis_id` is `HYP-2026-028` (Yang-Lee non-unitarity) but the
  content is the Ising OPE pipeline for HYP-027/025. The successor records 058/060/061 all correctly
  carry `HYP-2026-027`. This is a misfiled cross-reference.

---

### SIM-2026-057

- **Date** 2026-06-27. **HYP** HYP-2026-025.
- **Measurement** 3-state Potts (c=4/5), χ=6, Z₃ clock/shift, 8 seeds: `Δ_T` and `α = 2Δ_T`.
- **Pipeline** `research/tools/MERAKit.jl/qw_potts_measure.jl`, local CPU, single-thread BLAS.
- **Verdict recorded** "SUPPORTED (with caveat; confidence MEDIUM)" — α=4 at a third class.
- **Supported claim** `Δ_T` best basin 1.9972 → α = 3.9943; 8-seed mean 2.0849, ex-outlier 2.0341,
  range [1.9834, 2.3922] (`delta_T_statistics`). `Δ_ε = 0.8608` vs CFT 0.8 identifies the class.
- **What is NOT supported and the record says so** `Δ_σ` best 0.070 vs CFT 0.1333 — "NOT cleanly
  resolved", "NO seed hits 0.133" (`gate_status.Delta_sigma`). Honest.
- **Counterfactual novelty (§6): NEAR ZERO.** `Δ_T = 2` in *every* 2D CFT; the record itself states
  the test is "Confirm-or-find-a-bug" (`purpose`). Only implementation failure was possible. This is
  Level 1 validation, correctly framed inside the record but described in project-level summaries as
  a "universality ladder rung", which imports significance the calculation cannot supply.
- **Reproducibility present** driver, hardware, χ, block_size, 8-seed table, CFT targets.
- **Reproducibility absent** iteration count, wall time, commit hash, raw log, seed values (only
  "seed1..seed8" labels; the mapping to RNG state is in the driver, not the record).
- **Verdict proportionality** Proportionate. MEDIUM confidence with a named caveat is right.
- **DEFECT (minor):** `delta_T_statistics.all_8_mean = 2.0849` is quoted alongside a claim that
  "6 of 8 within [1.98,2.18]" — but seed4 (2.1784) and seed8 (2.3922) are the two outside/edge
  cases, so "6 of 8" counts seed4 as inside its own upper bound. Cosmetic, but the mean is dragged
  4 % high by one seed and the headline uses the *best* basin, not the mean. Best-basin selection
  is a live selection effect nowhere quantified in this record.

---

### SIM-2026-058

- **Date** 2026-06-28. **HYP** HYP-2026-027, related SIM-056.
- **Measurement** OPE v2 — corrected width-3 marginal via `descend_mid` causal cone + CFT kinematic
  prefactor `2^Δ_ε`.
- **Pipeline** `qw_ope_constants_v2.jl`, `ope_cone_v2.jl`, `test_cone_v2.jl`; χ=6, gate
  `|Δσ−0.125|<0.10 AND |Δε−1|<0.20`.
- **Verdict recorded** "STILL_BROKEN (honest negative)".
- **Supported claim** The negative: with a structurally valid RDM (`tr=1`, Hermitian 3e-16) the OPE
  is still basin-unstable — `C_sss` = 0.0077 / 0.0843 / 1.9185 across three clean basins (250×
  spread), `C_sse` = 0.485 / 0.897 / 0.812 (`results_clean_basins`).
- **Strongest methodological content in the whole 056–064 arc** is here, in `decisive_evidence`
  and `what_we_learned`: the build agent stopped at one lucky basin and called it MARGINAL; the
  verifier collected three and it failed. Seed 3 has the *best* spectrum (Δσ exactly 1/8) and the
  *worst* OPE — which kills "clean spectrum ⇒ correct OPE" as an inference. This is a genuine
  §22 adversarial test and it is properly recorded.
- **Reproducibility present** three file paths, gate criteria, per-basin table, rejected basin with
  reason (`rejected_basin.seed2`).
- **Reproducibility absent** χ-run iteration count, wall time, commit, raw log, and — notably —
  the *structural test* result (`test_cone_v2.jl` PASSED) is asserted in prose with no artifact.
- **Verdict proportionality** Proportionate. `runpod_decision` = "NOT WARRANTED … 'GPU on a broken
  contraction is wasted money'" is exactly §30 discipline.

---

### SIM-2026-059

- **Date** 2026-06-28. **HYP** HYP-2026-025, related SIM-057.
- **Measurement** χ=8 sharpening of the Potts tower; 8 seeds × 3000 iters, ~30–40 min/seed.
- **Pipeline** `qw_potts_chi8.jl`, MERAKit.jl, dense tensors.
- **Verdict recorded** "PARTIAL SHARPENING."
- **Supported claim** `Δ_T` across all 8 seeds ∈ [1.9707, 2.0565], mean 2.0150, α ∈ [3.9413, 4.1130]
  (`delta_T_statistics`). Two clean basins (seeds 3, 6) independently agree at Δσ ≈ 0.094.
- **What is NOT supported, stated plainly** Δσ 0.070 → 0.0945 vs CFT 0.1333, "STILL ~30 % short and
  only 2/8 seeds found the clean basin" (`delta_sigma_comparison`).
- **Reproducibility present** driver, χ, seeds, iters, per-seed runtime, full 8-seed table.
- **Reproducibility absent** commit, raw log, wall total, library versions.
- **Verdict proportionality** Proportionate. Refusing to upgrade HYP-025 out of caveat on improved-
  but-unconverged data is correct.

---

### SIM-2026-060

- **Date** 2026-07-02. **HYP** HYP-2026-027.
- **Measurement** OPE v3 "parity-fixed PEV": correct Z-parity lift, layer-by-layer covariance lift,
  parity projection of σ/ε, both width-3 registrations, `C_ssI`/`C_seI` consistency probes.
- **Pipeline** `qw_ope_pev.jl`, χ=6 × 8 seeds × 2500 LBFGS, wall 4390 s.
- **Verdict recorded** "GATE FAIL (honest negative) — but with a DECISIVE new discriminant".
- **Supported claim** Two stacked parity bugs in v1/v2 identified from the primary source
  (`what_was_built`): (1) a **non-symmetry** was lifted — `X⊗X` lifted against a Hamiltonian whose
  Z₂ is `Z^{⊗N}`; (2) v1's `coarse_parity` partial-traced the traceless parity. And the *new*
  structural result: the one-site parity lift itself fails on every dense basin (SVD dominance
  1.2–1.8 where covariance predicts ≫1; overlap 0.05–0.26).
- **The genuinely valuable finding** `why_failed`: "random-init dense optimization lands in a
  GENERIC GAUGE where the pushed-through symmetry is a finite-depth circuit on internal legs, not
  on-site." This is a real §34 state-vs-representation insight and it is the reason v4 worked.
- **Reproducibility present** 4 file paths, χ, seeds, iters, wall time, per-seed one-line table,
  consistency-probe ranges.
- **Reproducibility absent** **the cited log `scratchpad pev_chi6_gate.log` is NOT in the repo**
  (verified: `find . -name pev_chi6_gate.log` → MISSING). Also no commit, no versions.
- **Verdict proportionality** Proportionate; `what_we_learned` item (1) — "Fetch the primary source
  BEFORE redesigning — the PEV paper was on disk all along and settled in one read what two failed
  rebuilds guessed at" — is the most useful sentence in the block.

---

### SIM-2026-061

- **Date** 2026-07-03. **HYP** HYP-2026-027.
- **Measurement** OPE v4 with **Z₂-symmetric tensors**: `C_σσε` at χ=6 (8 seeds) and χ=8 (4 seeds).
- **Pipeline** `qw_ope_pev_z2.jl`, `Z2Space(0=>3,1=>3)`, direct-init, 2500 LBFGS, wall 1898 s
  (χ=6) / 2217 s (χ=8).
- **Verdict recorded** "VALIDATED (by-the-letter PARTIAL on the pre-registered spread criterion,
  driven entirely by one self-flagged outlier basin)."
- **Supported claim**
  - χ=6: 8/8 clean; `C_sse` per seed 0.5053 / 0.4717 / 0.4708 / 0.4758 / 0.5298 / 0.5095 / 0.4981 /
    0.5987; mean **0.5075**; 7/8 within ±10 %; spread 0.128 vs criterion 0.10.
  - χ=8 `Z2(4,4)`: `C_sse` 0.4887 / 0.5074 / 0.5115 / 0.5202, mean **0.5069**, spread **0.0315**
    (4× tighter — finite-χ scaling confirmed).
  - `C_sss = 0` **exactly** and `C_seI = 0` exactly on all seeds; covariance verifier overlap
    1.000000, `|P_lift − P_exact| ~ 2e-16`; `C_ssI` = 0.9999–1.0007; registration TI 0.001–0.005.
- **The outlier handling is defensible** seed 8 is flagged by `C_eee = 0.202` vs ≤0.10 for all
  others — a **pre-listed** diagnostic (the record says "design doc: 'C_eee should also → 0'").
  That is §36-compliant: the exclusion criterion predates the result.
- **HONEST WEAKNESS the record itself surfaces** the χ=8 `WATCH`: "C_eee did NOT shrink (0.03–0.28)
  — its zero is Kramers-Wannier (not Z₂) so the lattice only approximates it; diagnostic only."
  So the outlier-detector used at χ=6 is known not to converge at χ=8. That limits how much the
  seed-8 exclusion can be relied on going forward; the record does not draw that inference.
- **Counterfactual novelty: NEAR ZERO.** `C_σσε = 1/2` for Ising has been exact since BPZ 1984 and
  the record names PEV arXiv:0810.0580 as the target source. This is Level 1 with Level 2
  by-product (the Z₂-symmetric-tensor route that makes parity exact by construction).
- **Reproducibility present** driver + mirror path, symmetry space, χ, seeds, iters, wall times,
  full per-seed values, structural zeros, verifier numbers.
- **Reproducibility absent** **cited log `scratchpad z2_v4_gate.log` NOT in repo** (verified
  MISSING). No commit hash, no MERAKit version.
- **Verdict proportionality** Slightly generous. The header word is "VALIDATED"; the pre-registered
  criterion was **violated** at χ=6 (spread 0.128 > 0.10). The parenthetical is honest, but a record
  whose first word is VALIDATED and whose gate failed at the tested χ is the kind of framing §23
  warns about. The χ=8 pass is what carries it, and the χ=8 pass is a 4-seed run.

---

### SIM-2026-062

- **Date** 2026-07-03. **HYP** HYP-2026-025.
- **Measurement** Z₃-symmetric Potts driver validation at χ=6 `Z3Space(0=>2,1=>2,2=>2)`, 6 seeds
  × 2500 LBFGS, wall 3025 s.
- **Pipeline** `qw_potts_z3.jl`; charge-basis Potts H injected via an empirically derived fusion-tree
  index map, **machine-precision gate vs the dense reference (err 1.75e-15)** — a genuine
  independent-implementation check (§19).
- **Verdict recorded** "VALIDATED as the RunPod payload."
- **Supported claim** 4/6 clean basins (2.7× the dense rate); clean-basin Δσ 0.0871–0.0896,
  Δε 0.7754–0.7900, Δ_T 2.019–2.028 → α 4.038–4.055; σ/σ̄ degeneracy exact by construction.
- **Honest** `Delta_sigma_status`: "0.089 at chi=6(2,2,2) vs CFT 2/15=0.1333 — chi-starved exactly
  as SIM-057/059 diagnosed".
- **Reproducibility present** driver + mirror, symmetry space, seeds, iters, wall, the 1.75e-15
  cross-check, next-step plan with explicit targets.
- **Reproducibility absent** **`scratchpad potts_z3_chi6.log` NOT in repo** (verified MISSING).
- **Verdict proportionality** Proportionate — this is a tooling-validation record and is labelled as
  one (`type: "method-validation"`).

---

### SIM-2026-063

- **Date** 2026-07-04. **HYP** HYP-2026-025. **RunPod chi-escalation.**
- **Measurement** Potts Z₃ at χ=9 (3,3,3) and χ=12 (4,4,4), 6 seeds × 3000 LBFGS each.
- **Pipeline** RunPod pod `jhhcxxp82pa1js`, cpu3c, 32 vCPU, 64 GB, $0.96/hr, ~10.6 h, ~$10.20,
  pod killed + verified.
- **Verdict recorded** "RESOLVED — Delta_sigma converges to the CFT value at chi=12. HYP-025 caveat
  CLOSED; upgrade SUPPORTED (clean, full tower)."
- **Supported claim** χ=9: 3/6 clean, Δσ = 0.1372 / 0.1430 / 0.1635, Δε 0.813–0.853, α 4.01–4.07,
  wall 8537 s. χ=12: **2/6 clean**, Δσ = 0.1324 / 0.1351 (CFT 0.1333, within 1.5 %),
  Δε = 0.8039 / 0.8057 (within 0.7 %), Δ_T = 2.0004 / 2.0023 → α = 4.001 / 4.005, wall 24740 s.
- **Chi progression** 0.089 (χ6) → 0.137–0.164 (χ9) → 0.132–0.135 (χ12). The diagnosis was correct
  and the record says so without embellishment.
- **DEFECT (major, reproducibility): the entire evidentiary basis is missing.** `files` lists
  `"scratchpad potts_chi9.log / potts_chi12.log"` — **both MISSING from the repo** (verified). The
  χ=12 numbers that closed HYP-025's caveat and are quoted in project memory exist only as this JSON
  summary. §21 requires a frozen snapshot; there is none. A $10 RunPod run that upgraded a
  hypothesis status has no recoverable raw output.
- **Counterfactual novelty: NEAR ZERO.** Δσ=2/15, Δε=4/5, Δ_T=2 for 3-state Potts are exact and
  were the stated targets (`goal`). Only convergence-or-not was in question.
- **Verdict proportionality** Overstated by one notch. "RESOLVED / clean full tower" rests on
  **2 of 6 seeds** at χ=12, with Δσ still 1.5 % off and the clean-basin rate *falling* with χ
  (3/6 → 2/6, noted in `results.basin_rate`). "Converges to the CFT value" is a fair description of
  the trend; "CLOSED" on n=2 is stronger than the data.

---

### SIM-2026-064

- **Date** 2026-07-04. **HYP** HYP-2026-027. **RunPod chi-escalation, same session as 063.**
- **Measurement** `C_σσε` at χ=10 `Z2(5,5)` and χ=12 `Z2(6,6)`, 4 seeds × 3000 LBFGS.
- **Verdict recorded** "PRECISION ACHIEVED, ACCURACY PUZZLE FLAGGED."
- **Supported claim**
  - χ=10: 4/4 clean, `C_sse` = 0.4815 / 0.4971 / 0.4999 / 0.5043, mean 0.4957, spread 0.0228.
  - χ=12: 4/4 clean, `C_sse` = 0.4709 / 0.4719 / 0.4723 / 0.4736, mean **0.4722**, spread **0.0027**.
  - Progression of means: 0.5075 (χ6) → 0.5069 (χ8) → 0.4957 (χ10) → 0.4722 (χ12) — **crossed and
    undershot 0.5**, i.e. not monotone toward the exact value.
  - Structural: `C_sss = 0` exactly, covariance 1.000000 at every χ; Δσ within 1 % of 1/8.
- **This is the best §20/§22 work in the block.** The record refuses to quote the tight number,
  lists three ranked drift suspects with named tests, and then *runs the kill-test*:
  - Suspect (2) **CONFIRMED** — the two inequivalent placements bracket the CFT value symmetrically:
    `sse` (ε-far) 0.4957 / 0.4722 vs `ses` (ε-centre) 0.5258 / 0.5146 at χ=10/12; a ±5 % placement
    gap, **20× the 0.27 % basin spread**.
  - Suspect (1) **FALSIFIED** — maxiter 3000→8000 on χ=12 seeds 1–2 (wall 51628 s) moved the values
    in *both* directions (0.4723→0.4227, 0.4736→0.4998), ruling out simple under-convergence.
  - Prescription: quote **`C_sse = 0.50 ± 0.03`** with the placement gap as the honest systematic;
    "do not quote single-placement 0.472." Adopted in paper v5 §7.4 (2026-07-13).
- **This is the correct handling of a systematic and should be the template for the rest of the
  program.** It is also the strongest counter-evidence to any claim that the project sandbags:
  the *tighter* number (0.472, spread 0.0027) was the one thrown away.
- **Reproducibility present** χ, seeds, iters, per-seed values at both χ, the kill-test wall time,
  the drift-resolution date and the paper section it fed.
- **Reproducibility absent** **all three cited logs MISSING** (`ope_chi10.log`, `ope_chi12.log`,
  `ope_chi12_m8000.log` — verified). No commit, no versions. Suspect (3) (genuine finite-χ turnaround
  by χ≈16–22) remains **untested** and the record says so.
- **Verdict proportionality** Proportionate, arguably conservative.

---

### SIM-2026-065

- **Date** 2026-07-14. **HYP** HYP-2026-027. **C_TTT Route A.**
- **Measurement** Attempt at a genuine three-point `⟨TTT⟩` from MERA: T built from ascended energy
  density `h` (reflection-even, `T+T̄`) and momentum density `p = i[h,h']` (reflection-odd, `T−T̄`),
  projected onto the Δ≈2 even one-site block, PEV-normalised, contracted with exact h=2 kinematics.
- **Pipeline** `qw_ope_cttt.jl` (wraps `qw_ope_pev_z2.jl`), design `CTTT-SPIN-RESOLUTION-DESIGN.md`.
- **Verdict recorded** "ROUTE A CLOSED (see SIM-2026-066)".
- **Full failure trajectory recorded (this is a strength):**
  | stage | outcome |
  |---|---|
  | χ=6 smoke | all structural gates pass every seed; `res_h` discriminates: 0.17→C_TTT 3.66; 0.8→6.7; 3.3→120 (Gram conditioning, fixed) |
  | χ=8 v1 | sector dims pristine (5/6 clean, Δ_T 1.996–2.007), `G4 = |C_TTbarI| ≤ 0.007` everywhere, but `res_h` 0.38–2.3 (gate 0.35), C_TTT scatter 3.0–9.3 |
  | χ=8 v2 | parity-resolved reduction **FALSIFIED** — made `res_h` strictly worse (seed2 0.38→2.24), scatter widened to 2.2–11.3; reverted |
  | v3 rho3-pairing | reduction eliminated; two bugs found: (a) leg-swap of a blocked operator ≠ spatial reflection (needs intra-block reversal R), (b) L/R pairing sign at SI level is **gauge-dependent** |
  | χ=6 v3.1 | best: C_TTT = **4.20** vs 4.000 (5 %), regA/B 4.23/4.17, G4 = 0.0011, fracs 0.998/0.999, pin C_sse = 0.505; seeds 2–3 junk (12.2 / 67.5) but G4 flags them (0.12/0.15) |
  | χ=8 v3.1 | **HONEST MISS** — 6/8 pass gates, `|C_TTT|` scatters 0.58–59.3; block towers junky; θ* class flips seed-to-seed |
  | χ=6 8-seed | 5 pass all gates; clean values **4.20, 3.71, 2.13, 1.95, 11.87** — two within 8 % of target but **not basin-stable** |
- **Supported claim** Only the structural machinery: rho3-correlator pairing, exact blocked-reflection
  (R-correction), gauge-sign self-calibration, G4 as a chiral-split certificate. `verdict` states the
  4.20/3.71 hits are **"unclaimable"**. Correct.
- **Reproducibility present** driver path, design doc, per-stage seed/iter counts, two documented
  deviations from the design doc **recorded in the driver header** (θ-scan selecting by MIN
  `|C_TTbarI|` — "structural zero, unbiased" — not max `|C_TTT|`; and rho2-metric orthonormalisation
  of the block basis). Selecting by an unbiased structural zero rather than by the target quantity is
  exactly right and deserves credit.
- **Reproducibility absent** all four cited scratchpad logs MISSING; no commit; no per-seed table
  in machine-readable form (the χ=6 8-seed values appear only in prose inside `chi6_v31_8seed`).
- **Verdict proportionality** Proportionate and unusually disciplined.

---

### SIM-2026-066

- **Date** 2026-07-16. **HYP** HYP-2026-027. **Route A chi-escalation — DECISIVE NEGATIVE.**
- **Pipeline** RunPod pod `v9bpzaqj8wfacu`, cpu3c, 32 vCPU, 64 GB, ~4 h, ~$4, killed + verified;
  16 parallel single-thread runs: χ=10 `Z2(5,5)` × 8 seeds + χ=12 `Z2(6,6)` × 8 seeds, maxiter 4000.
- **Verdict recorded** "FALSIFIED. Escalation made the scatter WORSE, not better."
- **Supported claim** χ=10 gate-clean: **8.29, 146.1** (none near 4); one seed produced **6e8**
  (numerical breakdown). χ=12 gate-clean: **2.22, 2.15, 25.7, 0.057** — a 450× spread among
  "perfect-gate" seeds, none near 4.
- **The killer datum, and it is a real §12 killer:** χ=12 seed 6 has `G4 = |C_TTbarI| = 0.0000
  EXACTLY` with all other gates clean, yet `C_TTT = 25.7`; seed 8 has G4 = 0.0005 with C_TTT = 0.057.
  The record draws the right conclusion: *"The full gate stack can be satisfied exactly while the
  number is arbitrary ⇒ the gates certify the chiral SPLIT but cannot certify that O±  lie in the
  physical {T,T̄} span."*
- **Mechanism offered** the one-site scaling superoperator is isometry-only (no disentangler), which
  breaks the translation covariance spin-2 requires — labelled "theoretical hindsight consistent with
  the data", i.e. correctly marked as post-hoc.
- **Reproducibility absent** all 16 cited logs (`cttt_chi10_s1..8.log`, `cttt_chi12_s1..8.log`)
  MISSING from the repo. Per-seed values appear only in prose.
- **Verdict proportionality** Proportionate. This record retracts a 4.20 that a less disciplined
  program would have published, and `next` item (2) correctly notes the negative is itself
  publishable ("one-site PEV extracts scalar but not spin-2 OPE").
- **CRITICAL CONSEQUENCE FOR F1:** 065 and 066 are the *only* records in the entire block that
  attempt a genuine three-point stress-tensor contraction. **Both failed.** Everything downstream
  labelled "C_TTT" is a two-point central-charge measurement pushed through an identity.

---

### SIM-2026-067 — Route B, Ising rung

- **Date** 2026-07-19. **HYP** HYP-2026-027.
- **Measurement** Koo-Saleur matrix-element route on the periodic chain (circle), sparse ED,
  N = 8…18: `c_meas`, `C_TTT`, `C_sse`, plus the wrong-chirality structural zero.
- **Pipeline** `research/tools/cttt-circle/qw_cttt_circle.py`; design
  `research/tools/merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md`. Formula:
  `H_n = (N/2πv) Σ_x e^{inx2π/N}(h_x − e0) ≈ L_n + L̄_{−n}`; `c_meas = 2|⟨T|H_{±2}|0⟩|²`;
  `C_TTT = 2√2/√c_meas`. Literature anchor **Zou-Milsted-Vidal arXiv:1710.05397, PRL 121 230402**,
  confirmed *after* implementation (`design_evolution`).
- **Verdict recorded** "ROUTE B VALIDATED ON ISING: C_TTT = 3.9936 vs 4.000 (0.16 %)".

**I recomputed everything from `qw_cttt_circle_results_ising.json`.** Per-N (all six stages):

| N | c_meas | C_TTT | C_sse | G4 (wrong chirality) | Δ_T | s_T |
|---|---|---|---|---|---|---|
| 8 | 0.421320 | 4.3575 | 0.509796 | 2.29e-15 | 1.911541 | 2.0000 |
| 10 | 0.448547 | 4.2232 | 0.506233 | 7.37e-15 | 1.943043 | 2.0000 |
| 12 | 0.463848 | 4.1530 | 0.504314 | 2.38e-15 | 1.960316 | 2.0000 |
| 14 | 0.473251 | 4.1115 | 0.503164 | 8.62e-15 | 1.970787 | 2.0000 |
| 16 | 0.479427 | 4.0849 | 0.502419 | 2.07e-14 | 1.977605 | 2.0000 |
| 18 | 0.483693 | 4.0669 | 0.501910 | 1.05e-14 | 1.982290 | 2.0000 |

Recomputed extrapolations (linear in 1/N², all six points): `c → 0.498709` (record: 0.49871 ✔),
`C_sse → 0.499958` (record: 0.49996 ✔), `C_TTT → 3.993610` (record: 3.9936 ✔). All three quoted
numbers are exactly the all-N 1/N² intercepts. Good.

- **DEFECT (major, internal inconsistency — NOT recorded in ERRATA):** the two headline numbers are
  **mutually inconsistent through the record's own identity.** `C_TTT = 2√2/√c`. With
  `c_inf = 0.49871` this gives **4.00517**, not 3.9936. Conversely `C_TTT = 3.9936` implies
  `c = 0.501604`, not 0.49871. The record quotes the pair `(0.49871, 3.9936)` as though one followed
  from the other; in fact `c` and `C_TTT` were extrapolated **independently**, and the two estimators
  disagree by 0.29 % — larger than the 0.16 % accuracy the record claims.
  Estimator variants I computed:
  | estimator | C_TTT | dev from 4.000 |
  |---|---|---|
  | direct 1/N² fit of C_TTT, all N (**quoted**) | 3.99361 | −0.16 % |
  | direct 1/N² fit of C_TTT, last 4 | 3.99780 | −0.055 % |
  | direct 1/N² fit of C_TTT, last 2 | 3.99889 | −0.028 % |
  | derived from c_inf (all N) | 4.00517 | +0.13 % |
  | derived from c_inf (last 4) | 4.00188 | +0.047 % |
  The conclusion (agreement at the few-0.1 % level) is unaffected, so this is a **presentation and
  bookkeeping defect, not a physics error** — and the quoted variant is the *least* flattering of the
  direct fits, so there is no evidence of estimator shopping toward a better number. But the record
  states one estimator, discloses no alternatives, and its two headline numbers cannot both be right.
- **Genuine strengths, verified:**
  - `G4_wrong_chirality` ≤ 2.1e-14 at every N — and unlike Route A's G4 this **cannot be satisfied
    vacuously**: it is enforced by momentum conservation (`method_notes` (3)). The record makes this
    contrast explicitly. Correct and important.
  - `s_T = 2.0000000` at every N — momentum is an exact quantum number here, which was the entire
    point of abandoning Route A.
  - **`v = 2` is exact, not self-calibrated** (`v_used = 2.0` in every stage). Consequently Δ_T is a
    *genuine measurement* in this record (1.9115 → 1.9823, converging to 2). **This is not true of
    068/069/071**, where `v_T` is *defined* by imposing Δ_T = 2 — see §3 independence ledger.
  - `max-element identification tried and FALSIFIED` (`method_notes` (2)): lattice band-edge states
    carry ~2× larger raw UV elements than T (Δ→3 ε-tower s=2 state: element 0.96 vs T's 0.50 at
    N=12). A negative methodological result recorded against the project's own convenience.
  - The original circle design (equal-time `⟨hh⟩`/`⟨hhh⟩` correlators) was **falsified by ED within
    the hour** and the record says so, including the unresolved theory footnote (`⟨hh⟩_conn` is
    negative, vanishes exactly at antipodal separation, closed form `−(16/π²)/(4x²−1)²`).
  - A prior claim in this very record was corrected in place with a dated note: *"NOTE (corrected
    2026-07-20): there is NO public amilsted/puMPS package … An earlier claim here that one existed
    was a web-search artifact, unverified."* That correction was itself later corrected in
    `VENDOR.md` (see 068). Two-level self-correction is good practice.
- **TCI attempt in the same record — honest negative** O'Brien-Fendley λ3 = 0.856, N = 10…16: the
  G1 spectrum matches TCI well (σ 0.071 vs 3/40, ε 0.195 vs 1/5, σ′ 0.876 vs 7/8) but
  `c_meas 1.45 → 1.21`, "far from 0.7 and drifting slowly. NOT CONVERGED AT ED SIZES". Cause
  correctly identified: `L_{−2}ε` at Δ=2.2 carries the same quantum numbers as T (even, s=2), with
  contamination dying only as `~N^{−0.2}`.
- **Reproducibility present** driver **in repo**, two results JSON **in repo**, design doc in repo,
  N range, v convention, identification rule and its falsified alternative.
- **Reproducibility absent** no Python/scipy version, no commit hash, no runtime, no seed (moot —
  deterministic sparse ED), no statement of which extrapolation window/estimator produced each
  quoted number (the defect above).
- **Counterfactual novelty: NEAR ZERO.** c = 1/2 for Ising is exact; the c-formula is ZMV's own
  (record says so). Level 1.
- **Verdict proportionality** "VALIDATED ON ISING" is proportionate for the *pipeline*. The claim
  "the first successful C_TTT extraction in the program" is true only under the identity-substitution
  described in F1 — no `⟨TTT⟩` was contracted.

---

### SIM-2026-068 — TCI rung (requested in full)

- **Date** 2026-08-10. **Hypothesis links** HYP-2026-027, SIM-2026-067.
- **Title (verbatim)** *"C_TTT at the tricritical Ising point via puMPS Koo-Saleur matrix elements:
  3.381 +/- 0.005 vs exact 3.3806 — PASSED"*.
- **Measurement** central charge `c` at the O'Brien-Fendley tricritical point, mapped to `C_TTT`.
- **Pipeline** vendored **`yijian-physics/puMPS`** = the Zou-Milsted-Vidal PRL 121 230402 codebase,
  **commit `0557b12`**; OF chain at λ1 = 1, λ2 = 0.428 (= the SIM-051/067 λ3 = 0.856 point at half
  energy normalisation). GS via `minimize_energy_local_CG!`; Bloch excitations at k = 0, ±2;
  KS Fourier-mode elements via `Hn_in_basis`. T identified by **element dominance with a
  Δ-plausibility gate**. `v_T` calibrated **from Δ_T = 2** (assumed exact), cross-checked by
  `v_σ` (Δ=3/40) and `v_ε` (Δ=1/5). Driver `research/tools/pumps-setup/qw_cttt_of.jl`, per-round
  JLD2 checkpointing, results `qw_cttt_of_results.jsonl`.

**Ladder table (record `ladder.rows`) — every row verified against
`research/tools/pumps-setup/qw_cttt_of_results_2026-08-10.jsonl`:**

| N | D | c_{n+2} | c_{n−2} | C_TTT_mean | raw-file c_{n−2} (my extraction) | match |
|---|---|---|---|---|---|---|
| 14 | 10 | 0.833318 | 0.825720 | 3.1055 | 0.825719535647026 | ✔ |
| 20 | 20 | 0.756406 | 0.756255 | 3.2523 | 0.7562549081105939 | ✔ |
| 28 | 20 | 0.724179 | 0.724245 | 3.3236 | 0.7242451471228689 | ✔ |
| 40 | 20 | 0.710765 | 0.710536 | 3.3552 | 0.7105364120853216 | ✔ |
| 56 | 24 | 0.703726 | 0.703780 | 3.3716 | 0.7037803843235383 | ✔ |

I also recomputed every `C_TTT_mean` as `2√2/√(chirality mean)`: 3.10547, 3.25232, 3.32363, 3.35520,
3.37160 — matching the record to all quoted digits. **The ladder table is faithful.**

Record `ladder.note`, verified: chirality symmetry ≤1e-4 at every N ≥ 20 (largest asymmetry at N=14
where T/L2σ are near-degenerate). Gap ratio ε/σ: **2.749 (N=14) → 2.686 (N=40) → 2.680 (N=56)** vs
M(4,5) exact 8/3 = 2.667 — raw file gives 2.7488614, 2.6863487, 2.6798390 ✔. v spread at N=56 D=24:
`v_T = 1.6325`, `v_σ = 1.6200`, `v_ε = 1.6280` (0.8 %) — raw file gives 1.6325173, 1.6200188,
1.6280210 ✔ (spread 0.77 %).

**D-systematics table (record field `D_systematics`, verbatim content, each shift re-derived by me
from the raw file):**

| N | D shift | record's stated Δc | my re-derivation from raw c_{n−2} | agreement |
|---|---|---|---|---|
| 20 | D12 → D20 | "nil … D12==D20 to 1e-4" | 0.7562139 → 0.7562549 = **+4.1e-5** | ✔ |
| 28 | D12 → D20 | **+0.005** | 0.7189939 → 0.7242451 = **+0.0052512** | ✔ |
| 40 | D16 → D20 | **+0.0034** | 0.7073095 → 0.7105364 = **+0.0032269** | ≈ (record 5 % high) |
| 56 | D20 → D24 | **+0.0030** | 0.7005406 → 0.7037804 = **+0.0032398** | ≈ (record 8 % low) |

Record's further statements, verified: *"Truncation LOWERS c; the bias grows with N"* — true in
sign at every rung. *"The N=56 D=20 value 0.7008 sat anomalously below the power-law trend (two
errors cancelling: finite-N pushes c up, finite-D pushes it down); at D=24 the point lands exactly
on the trend."* — raw c_{n−2} at N=56 D=20 is **0.7005406** (record quotes 0.7008; the record's
figure is presumably the chirality mean, which I cannot form because only c_{n−2} is extractable
by my parser — see UNVERIFIED). *"Residual D→∞ correction at N=56 estimated ≤ +0.001–0.002
(geometric decay of the D-shifts) and is included in the systematic band."*

**Fit-variant table (record field `fit`, complete):**

Model: `c(N) = c_inf + a·N^{−p}`, fitted to best-D chirality means.

| variant | c_inf | fit err | p | C_TTT | my check of 2√2/√c_inf |
|---|---|---|---|---|---|
| `all5` | 0.69858 | 0.00085 | 2.31 | 3.3841 | 3.38409 ✔ |
| `drop_N14` | 0.69942 | 0.00157 | 2.42 | 3.3820 | 3.38206 ✔ |
| `drop_N56` | 0.69891 | 0.00189 | 2.33 | 3.3832 | 3.38329 ✔ |
| `mid3_exact` | 0.70212 | — | 2.67 | 3.3755 | 3.37556 ✔ |
| `D_residual_shifted` | 0.69952 | — | — | 3.3818 | 3.38182 ✔ |

**Quoted (verbatim):** *"c_inf = 0.699 +/- 0.002 (variant spread + fit error) vs exact 7/10;
C_TTT = 3.381 +/- 0.005 vs exact 2\*sqrt(2)/sqrt(7/10) = 3.3806"*. Exact target recomputed:
2√2/√0.7 = **3.38073** ✔.

- **DEFECT (minor, uncertainty accounting):** the quoted band **excludes one of its own listed
  variants.** Variants span c_inf ∈ [0.69858, 0.70212]; the quote `0.699 ± 0.002` = [0.697, 0.701]
  **misses `mid3_exact` = 0.70212** by 0.0011. Correspondingly `C_TTT = 3.381 ± 0.005` = [3.376,
  3.386] misses `mid3_exact` = 3.3755 by 0.0005. The band is described as "variant spread + fit
  error" but does not cover the variant spread. Small, but §20 asks that the error model be stated
  and honoured.

**Key findings (record field `key_findings`, all four, with my assessment):**

1. *"The tricritical C_TTT is MEASURED: 3.381 ± 0.005 vs exact 3.3806 (0.15 %-level agreement)."*
   — **Accurate as arithmetic; mis-titled as physics.** Per F1 this is a central-charge measurement
   (c_inf = 0.699 vs 0.700, 0.14 %) rewritten in other units.
2. *"The feared L2eps contamination (~N^−0.2 element mixing, the reason ED could not close TCI at
   N ≤ 16) is STRONGLY SUPPRESSED in puMPS Bloch-state elements: at N=56 the largest non-T raw
   element is ≤0.0003 vs T's 0.109 (~400×), and the observed finite-size correction exponent is
   p ≈ 2.4, not 0.2."* — **Direction verified and it is the most valuable claim in the record.**
   My extraction of the N=56 D=24 `n−2` block: `raw = [0.10865587, 6.6879e-5, 1.16359e-4,
   1.28456e-5]`, `others_norm = [3.6512e-4, 6.3526e-4, 7.013e-5]`, `M_T = 0.5932`, `jT = 1`.
   So T's raw element **0.10866 ✔ (record 0.109)**; largest non-T **raw** element is **1.164e-4**,
   giving **934×**, not 400×; largest `others_norm` is **6.353e-4**, giving **171×**. The record's
   "≤0.0003 / ~400×" matches neither array exactly. The claim understates the raw suppression and
   overstates the normalised one. Imprecise, not inflated in the aggregate.
3. *"T/L2sigma level ordering flips between N=14 (T = 2nd lowest at k=2) and N ≥ 28 (T = lowest);
   element-dominance identification handles this automatically — position-based ID would have
   silently measured the wrong state."* — **VERIFIED from the raw file:** `jT = 2` at N=14 D=10;
   `jT = 1` at N=40 D=20 and N=56 D=24. Genuine and non-obvious.
4. *"Two-error cancellation observed and resolved: N=56 D=20 gave a spuriously perfect c=0.7008
   (finite-N high bias vs truncation low bias); only the D=24 re-run exposed it. Constant-D ladders
   or per-N D-convergence checks are mandatory."* — **VERIFIED** (0.7005406 vs converged 0.7037804,
   the former being 0.07 % from 0.7 and the latter 0.54 % from it). This is real §22 discipline: the
   number closest to the right answer was the wrong one, and the record says so.

- **DEFECT (minor, incomplete disclosure): an undisclosed discarded stage.** The raw file contains
  **two** N=14, D=10 stages. The first gives `c = 0.00944547510025909` with `jT = 3`,
  `v_T = 1.8132`, `raw = [0.0, 0.0, 0.05592, 0.48541]` — an element array offset by two leading
  zeros, i.e. a mis-aligned/pre-fix run that identified the wrong state. The second gives
  `c = 0.825720` with `jT = 2` and `raw = [0.05592, 0.48541, 0.00083, 0.00063, 0.00215, 0.10723]`.
  Only the second appears in the record. This is very probably a legitimate bug-fix re-run (the
  offset is visible in the data), **but the record does not mention that an earlier N=14 stage
  returned c = 0.0094**, and §32 asks that superseded analyses be preserved rather than silently
  dropped.
- **Operational notes (record, verbatim, worth preserving):** multithreaded BLAS ~3× per CG
  iteration vs the MERAKit single-thread discipline (safe here: CG to a unique GS, no basin
  selection); **warm-starting D by tensor padding throws `LAPACKException(30)` in the transfer-matrix
  eigensolve — the same failure as MERAKit's χ-ramp; direct-init at target D confirmed as the rule**;
  background jobs externally killed 7 times, working pattern = short CG rounds (15 iters) +
  per-round checkpoints + wall-clock `exit(42)` + repeated foreground invocations; **CG gradient
  plateaus at ~9e-5 (linesearch floor)**, energies measurement-quality there.
- **Reproducibility present — the best in the block.** Driver in repo; **vendored dependency pinned
  by full commit SHA** (`VENDOR.md`: `0557b12a387091f96b83900e99bdb13c5f393839`, 2025-09-14, branch
  `main`) with the exact `curl` fetch command, dependency list, Julia channel (1.12.x), license
  status (**NONE on the upstream repo** — vendored copy gitignored, only project drivers tracked),
  and the required source patches; results `.jsonl` committed to `pumps-setup/`; per-N and per-D
  stages all present.
- **Reproducibility absent** no wall times per stage; no seed (moot for CG-to-unique-GS); no
  `Project.toml`/`Manifest.toml` in the tracked mirror (VENDOR.md says the env "lives at
  `research/tools/puMPS/Project.toml` (created locally, **gitignored** with the source)") — so the
  exact dependency versions are **not recoverable from the repo**; no chirality-mean column in the
  raw file (only per-orientation blocks), so the record's `c_{n+2}` column could not be
  independently re-extracted by my parser.
- **Counterfactual novelty (§6): NEAR ZERO on the physics, LOW-MODERATE on the method.** c = 7/10 at
  the tricritical point is exact and was the stated target; only convergence was in question.
- **NOVELTY-GATE FLAG (§8, serious):** `VENDOR.md` documents that the vendored ZMV codebase
  **already exports** `OBF_Hn_MPO_split` — annotated in the file's own table as *"O'Brien-Fendley
  H_n MPOs **(TCI!)**"* — i.e. the Koo-Saleur Fourier-mode MPOs for **precisely this model** were
  written by the original authors. SIM-2026-067 independently states *"ZMV needed N ≤ 128 with puMPS
  for this exact model"* (`results.tci_of`). Taken together, the project's own records indicate this
  measurement lies inside the scope of the prior work whose code is being run. That does **not**
  prove ZMV published this number, but it makes a §8 literature gate **mandatory before any novelty
  language**, and no such gate has been run. See §5 below.
- **Verdict proportionality** *"PASSED"* is proportionate as a **pipeline validation** verdict.
  The framing "Second rung of the stress-tensor self-coupling ladder complete" is not proportionate:
  no self-coupling was measured (F1), and the rung was run on the prior authors' own code for the
  prior authors' own model.

---

### SIM-2026-069 — Potts rung (requested in full)

- **Date** 2026-08-11. **Hypothesis links** HYP-2026-025, SIM-2026-067, SIM-2026-068.
- **Title (verbatim)** *"C_TTT at the 3-state Potts point via puMPS Koo-Saleur matrix elements:
  3.163 +/- 0.003 vs exact 3.16228 — PASSED. THE SELF-COUPLING LADDER IS COMPLETE (Ising + TCI +
  Potts)."*
- **Pipeline** identical to SIM-068 on the critical 3-state Potts chain in the puMPS convention
  `H = Σ_j [−½(U'_j U_{j+1} + U_j U'_{j+1}) − h/2 (V_j + V'_j)]`, h = 1 self-dual, `weylops` d = 3.
  GS via `minimize_energy_local_CG!` with **plateau-accept** (d=3 CG floor ~2.5e-4 vs 9e-5 on OF
  d=2; *"not fixable by step/pinv_tol tuning"*), certified by a **momentum-resolved ED gate at
  N = 10** (base-3 generalisation of the vendored `UnitTestED` trick). Bloch excitations at
  k = 0, ±2; `v_T` from Δ_T = 2; T by element dominance with Δ-plausibility gate (1.5, 2.5).
  Drivers `qw_cttt_potts3.jl`, `qw_potts_ed_gate.jl`.

**ED gate (record field `ed_gate`, verbatim):** N = 10; agreement *"E0/site 1.4e-6 (variational),
T gap 1.8e-4 rel, v's <1e-4, gap ratio 6.1929 vs 6.1924"*. My check: the raw file's N=10 D=12
`ratio_eps_sigma = 6.192857663368611` ✔ matches the puMPS side (6.1929). Extra findings, verbatim:
*"ED spectrum shows EXACT charged doublets with elem=0 (Z3 structural zeros, H neutral) and
reconfirms the SIM-067 band-edge trap in raw ED: max-element state is a UV state at Δ~2.53 with
4.5× T's element — naive ED element-dominance would give c=5.9. puMPS Bloch elements suppress every
non-T element to ≤6e-4 (up to ~4000× dominance at large N)."*
**This is an independent-code cross-check (§19) and it is the single best control in the block.**

**Ladder table (record `ladder.rows`) — every row verified against
`research/tools/pumps-setup/qw_cttt_potts3_results_2026-08-11.jsonl`:**

| N | D_best | c_{n+2} | c_{n−2} | C_TTT_mean | raw-file c_{n−2} (my extraction) | match |
|---|---|---|---|---|---|---|
| 10 | 12 | 0.843509 | 0.843502 | 3.0796 | 0.8435020630534569 | ✔ |
| 14 | 20 | 0.822010 | 0.822015 | 3.1196 | 0.8220152214780894 | ✔ |
| 20 | 24 | 0.810536 | 0.810534 | 3.1417 | 0.8105343145996741 | ✔ |
| 28 | 24 | 0.805001 | 0.805007 | 3.1524 | 0.8050073150701340 | ✔ |
| 40 | 28 | 0.801976 | 0.801969 | 3.1584 | 0.8019689838254727 | ✔ |

Recomputed `C_TTT_mean = 2√2/√(chirality mean)`: 3.07962, 3.11964, 3.14165, 3.15243, 3.15838 —
matching every quoted digit. **The ladder table is faithful.**

Record `ladder.note`, verified: chirality symmetry ≤1e-4 at every rung; σ-pair split down to 1.2e-6;
gap ratio ε/σ → **6.074 at N=40** vs exact (4/5)/(2/15) = **6.0** — raw file N=40 D=28 gives
6.074414 ✔; v spread narrows to 0.5 % at N=40.

**D-systematics table (record field `D_systematics`, verbatim content, each shift re-derived by me
from the raw file):**

| N | D shift | record's stated Δc | my re-derivation from raw c_{n−2} | agreement |
|---|---|---|---|---|
| 14 | D12 → D16 | **+0.0050** ("D16 == D20, converged") | 0.8170880 → 0.8220810 = **+0.0049930**; D16 vs D20 = −6.6e-5 | ✔ both parts |
| 20 | D14 → D20 | **+0.0076** | 0.8020317 → 0.8095522 = **+0.0075205** | ✔ |
| 20 | D20 → D24 | **+0.0010** (geometric, residual ~+0.0002) | 0.8095522 → 0.8105343 = **+0.0009821** | ✔ |
| 28 | D20 → D24 | **+0.0007** (residual ~+0.0004) | 0.8043542 → 0.8050073 = **+0.0006531** | ✔ |
| 40 | D24 → D28 | **+0.0011** (residual ~+0.0003) | 0.8008896 → 0.8019690 = **+0.0010794** | ✔ |

Record: *"Truncation LOWERS c (same sign as TCI) but Potts d=3 needs one D-notch more per rung."*
Verified in sign at every rung.

**Two-error cancellation, caught twice (record, verbatim):** *"N=20 D=14 gave c=0.8019 (spuriously
nearer 0.8 than converged 0.8105) and N=40 D=24 gave 0.80088 sitting BELOW the p~2.2 trend; the
D=28 re-run was PREDICTED to land at 0.8022±0.0005 before it ran, and landed at 0.80197."*
My verification: N=20 D=14 raw = **0.8020317** ✔ (0.25 % from 0.8, vs converged 0.8105343 at 1.3 %);
N=40 D=24 raw = **0.8008896** ✔; N=40 D=28 raw = **0.8019690**, which **falls inside the stated
prediction band [0.8017, 0.8027]** ✔. **This is the only out-of-sample prediction (§18) in the whole
block and it succeeded.** Caveat under UNVERIFIED: the pre-registration cannot be confirmed from the
repo — the prediction and its outcome are asserted in the same field of the same record, and there
is no separate prediction registry (§36).

**Fit-variant table (record field `fit`, complete):**

Model: `c(N) = c_inf + a·N^{−p}`, best-D chirality means.

| variant | c_inf | p | C_TTT | my check of 2√2/√c_inf |
|---|---|---|---|---|
| `all4` | 0.79892 | 1.93 | 3.1644 | 3.16442 ✔ |
| `D_residual_shifted` | 0.79920 | 1.90 | 3.1639 | 3.16386 ✔ |
| `drop_N14` | 0.79887 | 1.91 | 3.1645 | 3.16452 ✔ |
| `with_N10` | 0.79906 | 1.96 | 3.1641 | 3.16414 ✔ |
| `fixed_p_2.0` | 0.79927 | 2.0 (fixed) | 3.1637 | 3.16372 ✔ |
| `fixed_p_2.2` | 0.80009 | 2.2 (fixed) | 3.1621 | 3.16210 ✔ |
| `fixed_p_2.4` | 0.80077 | 2.4 (fixed) | 3.1607 | 3.16076 ✔ |

**Quoted (verbatim):** *"c_inf = 0.7995 +/- 0.0012 (variant span + D-residual systematic) vs exact
4/5; C_TTT = 3.163 +/- 0.003 vs exact 2\*sqrt(2)/sqrt(4/5) = 3.16228. The (p, c_inf) fit degeneracy
dominates the band, as in SIM-068; the Potts band (0.24 % span) is TIGHTER than TCI's (0.5 %)."*
My checks: exact target 2√2/√0.8 = **3.16228** ✔. Potts variant span
(0.80077 − 0.79887)/0.8 = **0.238 %** ✔; TCI span (0.70212 − 0.69858)/0.7 = **0.506 %** ✔. Both
percentages are correct. The C_TTT band [3.160, 3.166] covers **all seven** variants ✔ (unlike
SIM-068's band). The c_inf band [0.7983, 0.8007] misses `fixed_p_2.4` = 0.80077 by 7e-5 — negligible.

**Stopping rule (record, verbatim, and worth quoting in full because it is §30/§31 exactly):**
*"N=56 omitted deliberately: 4 clean D-checked rungs already beat the SIM-068 precision, and a 5th
rung cannot change the verdict; hours of D=28+ compute would purchase no conclusion."*

**Key findings (record field `key_findings`, all four, with my assessment):**

1. *"THE LADDER IS COMPLETE: C_TTT measured at all three unitary universality classes — Ising
   3.9936/4.000 (SIM-067), TCI 3.381/3.3806 (SIM-068), Potts 3.163/3.16228 (this) — each at ≤0.15 %
   agreement with 2√2/√c. The Koo-Saleur circle route is validated method, three-for-three."*
   — Arithmetic correct (Ising −0.16 %, TCI +0.01 %, Potts +0.02 % on the quoted centres; note the
   Ising figure is −0.16 %, marginally outside its own "≤0.15 %" claim). **Mis-titled as physics**
   per F1: three central-charge measurements, three exact known targets.
2. *"Z3 charge does free work: charged sigma-descendants (the states NEAREST T in energy) have
   structurally zero KS elements, confirmed exactly in ED — Potts element space is CLEANER than TCI
   despite the denser spectrum."* — Consistent with my raw extraction: at N=40 D=28 `n−2`,
   `raw = [0.12901, 2.297e-5, 1.796e-5, 9.72e-7, 1.501e-5, 2.899e-5, 4.564e-5]`, `jT = 1`.
   Largest non-T raw = **4.564e-5** ⇒ dominance **2827×**. The record's *"up to ~4000× at large N"*
   is ~41 % above what the `n−2` block supports; the *"≤6e-4"* bound is exceeded at N=10 D=12
   (max non-T raw = **6.366e-4**). Both are loose statements of a correct qualitative result.
3. *"d=3 optimizer floor (~2.5e-4) is a conditioning property, not a convergence failure: energies
   keep creeping ~1e-9/iter. Plateau-accept + independent ED certification is the honest pattern;
   chasing |grad|<1e-6 wastes compute."* — Good practice, and it is backed by the independent ED
   gate rather than asserted.
4. *"Two-error cancellation is now a PREDICTIVE tool, not just a trap."* — Verified above. **This is
   the strongest single methodological item in the block.**

- **Operational notes (record, verbatim):** vendored puMPS needed a `weylops diagm` patch (pre-1.0
  syntax; only the potts3 path hits it) plus a `pinv_tol` passthrough in `minimize_energy_local_CG!`
  (*"tested, did not move the floor; kept"*); one mid-ladder Windows reboot survived via per-round
  JLD2 checkpointing + chained invocations, zero loss.
- **Reproducibility present** two drivers in repo (main + ED gate), results `.jsonl` **in repo with
  11 stages** including all the superseded-D runs (so the D-systematics are independently
  re-derivable — I did exactly that above), pinned vendor commit via `VENDOR.md`, patch notes,
  ED cross-check.
- **Reproducibility absent** no wall times; no environment lockfile in the tracked tree (same
  gitignored `Project.toml` issue as 068); the ED-gate output itself is not committed (only the
  driver and the summary numbers in the JSON).
- **Counterfactual novelty: NEAR ZERO.** c = 4/5 exact; target stated in advance.
- **NOVELTY-GATE FLAG (§8, same as 068 and equally serious):** `VENDOR.md`'s capability table lists
  *"**3-state Potts H_n MPOs** | `potts3_Hn_MPO_split(T, n, N; h)` (`weylops` for clock/shift)"* as
  already exported by the vendored ZMV code, and SIM-069's own `verdict` note says *"potts3_\*
  builders already in the vendored module"*. The Koo-Saleur machinery for this exact model was
  written by the prior authors. §8 gate not run.
- **Verdict proportionality** *"PASSED"* proportionate for pipeline validation. **"THE SELF-COUPLING
  LADDER IS COMPLETE" is not proportionate** — no self-coupling (three-point) quantity was measured
  at any rung.

---

### SIM-2026-070 — Yang-Lee Phase 1 (the gate)

- **Date** 2026-08-11. **Hypothesis links** HYP-2026-028.
- **Title (verbatim)** *"HYP-028 Phase 1: PAPER-133 Yang-Lee boundary-data reproduction PASSED
  (R_inf = −1.61820 vs −(1+√5)/2, 0.01 %; g_1 = 0.72535 vs 0.725073, 0.04 %)"*.
- **Measurement** reproduction of PAPER-133 (arXiv:2606.16785v2, Liu-Shimizu-Liu-Kawabata)
  projected-partition-function spectroscopy on the periodic PT-symmetric Ising chain
  `H_YL = −Σ(σᶻσᶻ + λσˣ + i h σᶻ)`, λ = 4.
- **Pipeline** sparse ED, KrylovKit smallest-real-part Arnoldi, L = 8…20 (2^20 = 1M-dim top rung).
  Finite-size exceptional points `h_c^L` by bisection on Im(E) of the lowest pair (L = 8…18);
  `h_c^∞` from a **fixed-exponent** fit (b = 12/5 + L^{−4} subleading). Biorthogonal projections at
  `h = h_c^∞` with **η = parity** so left = P·right. Driver
  `research/tools/yanglee-pt/qw_yanglee_pt.jl`.
- **Verdict recorded** "PASSED. Phase 2 unlocked."

**Recorded data, all re-derived by me:**

`h_c^L` = (8, 1.5863321), (10, 1.5750539), (12, 1.5693276), (14, 1.5660746), (16, 1.5640705),
(18, 1.5627601) → `h_c^∞ = 1.5587127`.
**My re-fit** of `h_c^L = h_c^∞ + a·L^{−2.4} + b·L^{−4}` (least squares) returns
**1.5587127** — the record's value reproduced to all seven quoted digits ✔. A two-parameter
`b = 12/5`-only fit gives 1.5588876, i.e. the `L^{−4}` term shifts the answer by 1.7e-4, which
matters given the record's own note that *"refining h_c^∞ by 1.2e-4 visibly moved L ≥ 16
amplitudes."* Free-b fits gave 2.33–2.37 vs theory y_φ = 12/5 = 2.4 (`method`).

`R(L)` = (8, −1.012298), (10, −1.118291), (12, −1.193620), (14, −1.249659), (16, −1.292888),
(18, −1.327222), (20, −1.355149). **These are corroborated line-for-line by
`research/tools/yanglee-pt/yl_proj.log`**, which also records `E_φ`, `E_1`, `Z_φ`, `Z_1` per L and
shows **`Z_1` negative at every L** with `|Im|` ≤ 2.9e-10 — the unitarity-forbidden sign, the
microscopic signature the whole reproduction turns on. ✔

**`R_inf` estimator — I re-ran the record's own recipe** ("two-level Richardson: pairwise 1/L
intercepts, then geometric tail sum"):

| pairwise intercept | my value | record |
|---|---|---|
| (8,10) | −1.54226 | "−1.5423…" ✔ |
| (10,12) | −1.57026 | |
| (12,14) | −1.58589 | |
| (14,16) | −1.59549 | |
| (16,18) | −1.60189 | |
| (18,20) | −1.60649 | "…−1.6065" ✔ |

Successive differences −0.02800, −0.01563, −0.00960, −0.00640, −0.00460; ratios
**0.5581, 0.6142, 0.6671, 0.7181** — record says *"ratios 0.56→0.72"* ✔. Geometric tail with
r = 0.7181 gives **R_inf = −1.618205**, record −1.61820 ✔, vs exact −1.6180340, deviation
**0.011 %** ✔ (record 0.01 %).

**Estimator-sensitivity test I ran (not in the record):** varying the assumed tail ratio,
r = 0.65 → −1.6150; r = 0.70 → −1.6172; r = 0.72 → −1.6183; r = 0.75 → −1.6203; r = 0.80 → −1.6249.
So R_inf is robust to ±0.3 % across a wide ratio range — **because the tail term contributes only
≈0.7 % of the final value** (last diff −0.0046 on a base of −1.6065). The 0.01 % agreement is
therefore genuinely earned, though it is more precise than the estimator's own ~0.3 % spread
warrants quoting. **Hold this number: it is the direct contrast with SIM-071 (see below).**

`g_1` = **0.725347** (record's `g1.value`; the summary line rounds to 0.72535), window L ≥ 10 with
spread 0.7246–0.7265 bracketing the exact 0.725073; deviation 0.04 %. The record also notes
*"paper_value: 0.725339(51) — our L ≥ 10 value matches the paper's own number"*, i.e. the
reproduction matches PAPER-133's numerics as well as the BCFT value. Cannot independently verify the
paper's figure (see UNVERIFIED).

**Key findings, verbatim, with assessment:**

1. *"PAPER-133's periodic-chain route to nonunitary boundary data is CONFIRMED at ED scale: the
   negative excited-to-ground amplitude ratio — impossible in any unitary CFT — is reproduced at
   0.01 % with plain sparse ED plus the η = parity left-pairing."* — **Verified.** Correctly framed
   as a reproduction.
2. *"h-sensitivity grows as L^{12/5} (relevant-direction flow) … Extrapolation quality is limited by
   h_c^∞ precision before anything else — pin h_c^∞ with the theory-fixed exponent, never a free-b
   fit alone."* — Consistent with my finding that the `L^{−4}` term moves `h_c^∞` by 1.7e-4.
3. *"Naive polynomial-in-1/L extrapolation over wide L-windows OVERSHOOTS (curvature at small L;
   free-power fits gave −1.75); pairwise-linear intercepts + Richardson on the intercept sequence is
   the stable estimator at these sizes."* — An honest disclosure that the estimator was **selected**
   after seeing that alternatives failed. That is legitimate here (the alternative overshoots the
   known answer by 8 %), but it means the estimator is **calibrated on a case where the answer is
   known**, and it is then reused in SIM-071 where the answer is not. Flagged, not condemned.
4. *"Working point must be h_c^∞ (PT-unbroken at all finite L) — everything is regular there; no
   exceptional-point pathology encountered anywhere in the pipeline."* — This is the "PT-edge dodge"
   that unblocked a branch closed since SIM-053/055. Real progress; it is a **borrowed** technique
   (PAPER-133's), correctly attributed in `method` and in the design doc.

- **Counterfactual novelty (§6): NEAR ZERO** — it is by construction a reproduction of a published
  table. The record labels it that way (`title` says "reproduction", `verdict` says "Phase 2
  unlocked"). Correct handling: this is Level 1 and is presented as Level 1.
- **Reproducibility present — good.** Driver in repo; **both logs in repo** (`yl_run_8_18.log`,
  `yl_proj.log`); design doc in repo; source paper PDF in repo (`research/downloads/2606.16785v2.pdf`);
  λ, h, L range, η choice, solver family, fit form, exponent convention all stated.
- **Reproducibility absent** no Julia/KrylovKit versions; **no RNG seed** (the driver's `eigsolve`
  start vector is `randn(ComplexF64, dim)` — see 071); no `info.converged` check recorded; no
  runtime; no commit hash; no repeat-run consistency check.
- **Verdict proportionality** **Proportionate.** This is the cleanest record in the block: a
  reproduction, labelled a reproduction, with its raw log committed.

---

### SIM-2026-071 — Yang-Lee Phase 2 (**the strongest current claim — full extraction**)

- **Date** 2026-08-11. **Hypothesis links** HYP-2026-028.
- **Title (verbatim)** *"HYP-028 Phase 2: biorthogonal Koo-Saleur elements at Yang-Lee measure the
  TRUE central charge — c_KS = −4.29 +/− 0.15 vs c = −22/5 = −4.4; c_eff = +2/5 EXCLUDED by sign and
  magnitude"*.
- **Verdict recorded** *"PASSED (discrimination decisive). HYP-028 core question answered."*

#### 071.1 — Every number the record contains

**Method parameters (field `method`):** momentum-resolved biorthogonal sparse ED of the PT-symmetric
Yang-Lee chain; λ = 4; **h = h_c^∞ = 1.5587127 imported from SIM-070**; L = 10…18;
translation-composed non-Hermitian Arnoldi; left states via **η = parity (left = P·right)**;
estimator
`c_KS = 2⟨vac_L|H_{−2}|T_R⟩⟨T_L|H_{+2}|vac_R⟩ / (⟨T_L|T_R⟩⟨vac_L|vac_R⟩) · (L/2πv_T)²`
— **product form, no square roots, sign is part of the measurement**;
**vacuum = |1⟩ = the SECOND k=0 state** (physical GS is |φ⟩, Δ_φ = −2/5); `v_T` from Δ_T = 2 above
|1⟩; T identified by **Δ-gate (1.75, 2.25) above vacuum** plus element dominance in-window;
KS-operator momentum orientation determined empirically, both computed, *"the dead one is a
structural zero ~1e-26"*. Driver `research/tools/yanglee-pt/qw_yanglee_ks.jl`.

**Yang-Lee results (field `results`):**

| L | c_KS (record) | c_KS (raw `qw_yanglee_ks_results.jsonl`, n=+2) | match |
|---|---|---|---|
| 10 | −1.413195 | −1.4131953717819705 | ✔ |
| 12 | −1.702883 | −1.7028834172130995 | ✔ |
| 14 | −1.953729 | −1.9537294337235040 | ✔ |
| 16 | −2.169926 | −2.1699263736663600 | ✔ |
| 18 | −2.356244 | −2.3562438686552745 | ✔ |

The n=−2 chirality agrees with n=+2 to ~1e-11 at every L (raw file) — the record's *"NEGATIVE at
every L, both chiralities, machine-real (Im ~ 1e-12 relative)"* ✔.

**Extrapolation (field `results.extrapolation`, verbatim):** *"pairwise 1/L intercepts −3.151,
−3.459, −3.683, −3.847; diff ratios 0.730, 0.728 (STABLE); geometric tail sum → −4.285. Free-exponent
fits are degenerate (w→0 runaway) and discarded honestly. Quoted: c_KS = −4.29 ± 0.15 (estimator
systematic)."*

**My independent re-derivation:** intercepts **−3.15132, −3.45881, −3.68330, −3.84679** ✔;
differences −0.30749, −0.22449, −0.16349; ratios **0.72999, 0.72827** ✔ (record 0.730, 0.728);
geometric tail with r = 0.728 gives **−4.28436** ✔ (record −4.285). Every step reproduces.

**Spectrum checks (field `results.spectrum_checks`, verbatim + my verification against the raw
`Dvac` arrays):**
- *"Δ_vac(T) → 2.0 (1.945 → 1.982 monotone)"* — raw `Dvac[2]`: 1.94471 (L=10), 1.96207, 1.97220,
  1.97843, **1.98236** (L=18) ✔ monotone.
- *"k = ±2 cluster structure matches the M(2,5) φ level-2 null-vector prediction exactly (ONE
  φ-descendant at Δ_vac → 1.6 below T)"* — raw `Dvac[1]`: 1.42607, 1.46587, 1.49223, 1.51069,
  **1.52412** (L=18). Trending toward 1.6 but **4.8 % short at the largest L**. The word
  *"exactly"* is an overstatement; "trending correctly at the few-percent level" is accurate.
  (Design-doc derivation checked: φ-descendant sits at 2.0 − 0.4 = 1.6 above |1⟩, T at
  2.4 − 0.4 = 2.0 above |1⟩ — `HYP028-BIORTHO-KS-DESIGN.md` Phase-2 refinement 3. Internally
  consistent.) A **third** k=±2 state exists at `Dvac[3]` = 3.015 → 3.355 and is neither identified
  nor discussed.
- *"⟨1|1⟩ biorthogonal norm NEGATIVE at every L (the conformal vacuum is a negative-norm state — the
  indefinite metric visible raw)"* — **NOT PERSISTED.** The driver prints it (line 96–97) but the
  `.jsonl` writer (lines 139–140) saves only `cks, vT, Tnorm, DT, prods, Dvac`. See §071.4.
- *"v_ref from the exact Δ = 2/5 (1−φ) split, 4.24 → 4.28"* — raw `v`: 4.24139, 4.25910, 4.27037,
  4.27822, **4.28414** ✔.

**Discrimination (field `results.discrimination`, verbatim):** *"c = −22/5 = −4.400: CONSISTENT
(2.6 % at ED scale). c_eff = +2/5 = +0.400: EXCLUDED (wrong sign, ~11× magnitude)."*
(2.6 % check: (4.400 − 4.285)/4.400 = 2.61 % ✔.)

**Unitary control (field `unitary_control`, verbatim):** critical TFIM, `MODE=ising`, same code path;
`c_KS` = (12, 0.517483), (14, 0.512776), (16, 0.509748); *"extrapolated: 0.49986 (Richardson in
1/L² — unitary corrections are L^{−2}) vs exact 0.5 (0.03 %)"*; *"all biorthogonal norms +1.0000
(Hermitian limit), Z2 structural zeros ~1e-24, same orientation convention as YL."*
**My check:** a two-point 1/L² intercept from L = 14, 16 gives **0.499861** — the quoted 0.49986
exactly. (The L = 12, 14 pair gives 0.49975.) So the control number is the **last** pairwise 1/L²
intercept.

**Caveats (field `caveats`, verbatim, reproduced in full because they are the record's own honest
limits):** *"ED-scale only (L ≤ 18); corrections are slow (effective w < 1) so the magnitude carries
the ±0.15 estimator band — the SIGN and the 11× separation from c_eff are unambiguous. Residual
h_c^∞ error contributes ≤0.01 at L=18 (SIM-070 h-sensitivity scaling). L=20 (1M-dim) skipped: sparse
H_n build cost, cannot change the discrimination."*

**Key findings (field `key_findings`, all five, verbatim):**
1. *"THE HYP-028 QUESTION IS ANSWERED at ED scale: the Koo-Saleur stress-tensor construction SURVIVES
   non-unitarity and measures the TRUE central charge c = −22/5, including its indefinite-metric
   sign — NOT the effective (Casimir) charge c_eff = 2/5 that governs finite-size energies. The
   biorthogonal element structure sees what the energy spectrum cannot."*
2. *"First lattice extraction (to our knowledge) of a NEGATIVE central charge from stress-tensor
   matrix elements; standard approaches obtain only c_eff from Casimir scaling."*
3. *"The T-identification discipline INVERTS at YL: the cross-module product to the φ-descendant is
   ~10× LARGER than T's (in unitary chains cross-tower elements are ~1e-4 suppressions). Δ-gating
   above the vacuum is mandatory; raw element dominance silently measures the wrong state."*
4. *"Implication for the force program: C_TTT = 2√2/√c is IMAGINARY at c < 0 — the graviton
   self-coupling does not survive as a real amplitude in the non-unitary theory even though
   α = 2Δ_T = 4 kinematics does. Interpretation (Phase 3, open): the stress-tensor exchange amplitude
   changes character, not just magnitude, when reflection positivity drops."*
5. *"The same two-level Richardson estimator that hit 0.01 % on SIM-070's R_inf shows MORE stable
   ratios here (0.730/0.728); the 2.6 % residual vs −22/5 is finite-size, not estimator noise.
   puMPS-scale L would sharpen the third digit."*

**Phase-3 candidates (field `verdict`):** interpretation of imaginary C_TTT; puMPS-scale sharpening;
*"the +2.0-Δ φ-descendant cross-module element (anomalously large — possibly its own observable)"*.

#### 071.2 — Controls, systematics and structural checks: present vs absent

| item | status | evidence |
|---|---|---|
| unitary control on same code path | **PRESENT but weak** (see 071.3) | `unitary_control` field; raw data NOT in repo |
| multiple system sizes | PRESENT, L = 10,12,14,16,18 | raw `.jsonl`, 5 stages |
| both chiralities | PRESENT, agree to ~1e-11 | raw `.jsonl` `n=+2` / `n=−2` blocks |
| dead-orientation structural zero (~1e-26) | **ASSERTED, NOT PERSISTED** | driver lines 109–116 compute both; only the chosen one is written |
| eigenvector-normalisation invariance | **PRESENT BY CONSTRUCTION, NOT TESTED** | I verified analytically from the driver: under ψ_R → z·ψ_R the numerator and `den` both scale by |z|², so `c_KS` is invariant. This directly answers RESEARCH-DIRECTOR §13 Q3 — but the record never states it, and no numerical normalisation-variation test was run |
| alternative left-pairing (η ≠ P) | **ABSENT** | driver `lv = i -> conj.(vecs[i][pp])` is the only pairing; §13 Q2 untested |
| η = P justification | **CORRECT** (I verified analytically) | `P σᶻ P = −σᶻ` ⇒ `P H_YL P = H_YL†`, so η = P is genuine pseudo-Hermiticity |
| exceptional-point health metric ⟨L\|R⟩→0 | **DESIGNED BUT NOT REPORTED** | design doc "Traps" §: *"⟨Ψ_L\|Ψ_R⟩ → 0 signals proximity to an EP; monitor it as the health metric."* Driver prints `<vac\|vac>` but the record reports no EP-proximity numbers |
| eigensolver convergence check | **ABSENT — DEFECT** | driver line 71: `vals, vecs, info = eigsolve(...)`; **`info` is never inspected**. An unconverged Arnoldi would return silently |
| RNG seed | **ABSENT — DEFECT** | driver line 71 start vector `randn(ComplexF64, dim)`, unseeded; no repeat-run consistency check recorded |
| solver settings | PRESENT in driver, ABSENT from record | `nev=24, krylovdim=90, tol=1e-11, maxiter=400` |
| Δ_T = 2 treated as measured | **NO — it is imposed** | driver lines 128–129: `v_T = (E_T − E_vac)L/(4π)` then `(L/2πv_T)²`. Substituting, `c_KS = 8·prod/(E_T − E_vac)²`: **v_T and L cancel identically**. The CFT normalisation Δ_T = 2 is an *input*, not a check |
| independent code path | **ABSENT** | one driver, one implementation; §27 "independent reproducer" not exercised |
| synthetic-matrix control with known non-normal behaviour | **ABSENT** (§13 required controls) | |
| pseudospectral / conditioning analysis | **ABSENT** (§13 Q14) | |

#### 071.3 — The three substantive weaknesses

**(a) The extrapolation supplies 82 % of the answer, and its tail rests on two samples.**
Largest-L datum `c_KS(18) = −2.356`; quoted limit **−4.285**. The extrapolation therefore contributes
**−1.929, i.e. 82 % of the final magnitude** — the measurement is 18 % data and 82 % estimator.
Within the estimator, the geometric tail term alone contributes **−0.438 = 11.4 %** of the final
value, and its ratio is estimated from **two** ratio samples (0.730, 0.728).

Contrast **SIM-070**, where the identical estimator was calibrated: there the last intercept
difference was −0.0046 on a base of −1.6065, so the tail contributed **0.7 %**, and there were
**four** ratio samples. **The control case therefore validated the estimator in a regime with a
16× smaller lever arm than the regime it is used in.** That is the single most important
qualification on this result and the record does not state it.

Worse for the "STABLE ratios" reading: in SIM-070 the ratio sequence **drifts monotonically upward**
(0.558 → 0.614 → 0.667 → 0.718) and had *not* converged by the last available pair. Two samples in
SIM-071 cannot exclude the same drift. My sensitivity sweep of the tail ratio:

| assumed asymptotic ratio r | resulting c_KS |
|---|---|
| 0.65 | −4.150 |
| 0.70 | −4.228 |
| 0.728 (**used**) | **−4.285** |
| 0.75 | −4.337 |
| 0.80 | −4.501 |

Two consequences, and they point in opposite directions for the record's credibility:
- The quoted **±0.15** band corresponds to r ∈ [0.65, 0.785] and is **not derived from any stated
  procedure** — it is asserted as "estimator systematic". It also fails to cover r = 0.80.
- **The residual 2.6 % gap to −22/5 is exactly what an upward-drifting ratio would produce.** If
  SIM-070's drift pattern repeats, the true limit is *more* negative than −4.285 and moves toward or
  past −4.4. So the record's reading ("the 2.6 % residual is finite-size, not estimator noise") is
  *plausible and arguably conservative* — but it is an inference from one calibration case, not a
  demonstration, and the record presents it as settled.

**(b) The unitary control does not exercise the feature under test.**
The record says "same code path", and it is *nearly* true — but the driver branches on `MODE` at
four points: `LAMBDA` (line 24), `HC` (line 25), `ivac` (line 84: **`i0[1]` for Ising vs `i0[2]` for
YL** — i.e. a *different state* is called the vacuum), and `v` (line 86: σ-gap Δ=1/8 for Ising vs
1−φ split Δ=2/5 for YL). More importantly:

- In the Hermitian TFIM, `P = Πσˣ` **commutes** with H, so eigenstates are P-eigenstates and the
  "biorthogonal" pairing `⟨ψ_L| = ⟨ψ_R|P` collapses to ±⟨ψ_R|. The record's own observation *"all
  biorthogonal norms +1.0000 (Hermitian limit)"* confirms exactly this collapse.
- Therefore the control validates the KS element arithmetic, the momentum resolution, the orientation
  convention and the gap normalisation — **but it does not exercise indefinite metric, left ≠ right,
  non-normality, conditioning, or negative norms**, which are the properties the whole claim rests
  on. §19's requirement that "a serious control should be capable of defeating the preferred
  interpretation" is not met: this control cannot fail in the way the YL run could.
- The control's extrapolation is also a **different estimator** (single 1/L² pairwise intercept, 3
  data points, ~2 % correction) from the headline's (1/L pairwise intercepts + geometric tail,
  5 points, 82 % correction). Two estimators, one labelled as validating the other.

**(c) The sign of the headline is contingent on the state-identification gate — and the record
half-says so.**
From the raw `.jsonl`, the three normalised products in the k=+2 window at L=10 are
`[+46.470, −4.7446, −12.219]` against `Dvac = [1.426, 1.945, 3.015]`; at L=18
`[+28.451, −2.5884, −7.3351]` against `Dvac = [1.524, 1.982, 3.355]`.
I verified the T entry reproduces the headline: `2 × (−4.7446) × (10/(2π·4.12414))² = −1.41326`
= the recorded `c_KS(10)` ✔.

The φ-descendant's product is **positive and 9.8× larger** (L=10) / **11.0× larger** (L=18) than T's
— confirming key-finding 3's "~10×" quantitatively. **But the sign flip is the point:** had the
naive max-element rule been used (the rule the project itself used successfully on unitary chains),
the answer would have been **c_KS ≈ +13.8 at L=10** — *positive*, and superficially closer to a
"c_eff-like" story. The record states the identification hazard (key-finding 3) but does **not**
state that the headline's sign — the part of the claim it calls "unambiguous" — is therefore a
consequence of the Δ-gate choice, not a raw feature of the element spectrum. Further, the Δ-gate
window is computed from `v` (driver line 123), which itself assumes Δ_φ = −2/5 and the M(2,5)
identification. **The CFT identification is used to select the state whose element then measures the
CFT central charge.** That is a structural dependency, not a circularity — the gate is theory-fixed
in advance and the design doc pre-registers it (`HYP028-BIORTHO-KS-DESIGN.md` refinements 2–4,
written before the run) — but it must appear in the independence ledger and it does not.

Also unremarked: the driver's own comment (line 13) states the CFT expectation *"⟨T|T⟩ = c/2 < 0, so
watch the T biorthogonal norm"* — yet the persisted `Tnorm` is **positive at every L**
(0.09615, 0.04786, 0.02359, 0.01150, 0.005539). The negativity therefore enters via ⟨1|1⟩, which is
not persisted. This tension between the driver's stated expectation and the saved data is discussed
nowhere.

#### 071.4 — Reproducibility metadata: present vs absent

**Present:** driver in repo (152 lines, fully readable); results `.jsonl` in repo with all 5 YL
stages including both chiralities, per-state `prods`, `Dvac`, `Tnorm`, `vT`, `DT`, `Ephi`, `E1`;
design doc in repo, **written before the run** and containing the pre-registered discrimination,
vacuum identification and Δ-gate; Phase-1 gate cross-linked (SIM-070) with its logs in repo; the
working point `h = 1.5587127` traceable to SIM-070's fit, which I reproduced.

**Absent (each a §21 item):**
1. **No raw output for the unitary control anywhere in the repository.** Repo-wide grep for
   `0.517483` / `0.512776` / `0.509748` / `0.49986` returns only: the SIM-071 JSON itself,
   `NEXT-SESSION.md`, `docs/governance/PROJECT-REVIEW-2026-08-11.md`, `HYP-2026-028.json` — all
   downstream restatements. The driver appends to `qw_yanglee_ks_results.jsonl`, which contains
   **only the five YL stages**. **The strongest claim's only control has no persisted evidence.**
2. **No stdout log for the KS run at all** (`ylks_warn.log` is 0 bytes). Everything the driver prints
   and does not write to jsonl is lost: `<GS|GS>` and `<vac|vac>` biorthogonal norms, the
   per-state orientation labels, the dead-orientation magnitudes, the low-spectrum listing.
   Three separate claims in the record (`⟨1|1⟩ NEGATIVE at every L`; `dead orientation ~1e-26`;
   `Z2 structural zeros ~1e-24`) are therefore **unverifiable from repo artifacts**.
3. **No RNG seed** — `randn(ComplexF64, dim)` start vector, no seed, no determinism statement, no
   repeat-run check.
4. **No convergence verification** — `info` from `eigsolve` discarded.
5. No Julia version, no KrylovKit version, no `Project.toml`/`Manifest.toml`, no commit hash, no
   runtime, no output checksum, no platform record.
6. Solver settings (`nev=24, krylovdim=90, tol=1e-11, maxiter=400`) exist only in the driver, not in
   the record.
7. **Not in `research/RESEARCH-LOG.md`** — see §4.

#### 071.5 — What the evidence does and does not establish

**Establishes (high confidence):**
- The product-form biorthogonal KS quantity at the Yang-Lee working point is **negative at every
  accessible L (10–18), in both chiralities, real to ~1e-12**. This is raw data, not extrapolation,
  and it is committed to the repo.
- Therefore `c_eff = +2/5` is **excluded**, by sign at every L and by magnitude (|c_KS(18)| = 2.36
  vs 0.4, ~6× at L=18 alone). This half of the discrimination needs **no extrapolation at all** and
  is the record's most defensible statement.
- The estimator is **invariant under eigenvector renormalisation** (I verified this analytically from
  the driver), which removes the most obvious "it's a normalisation convention" objection — i.e. it
  partially answers the §12 *Yang-Lee method killer*.
- The **module-identification inversion** is real and quantitatively documented: the cross-module
  φ-descendant element exceeds T's by ~10–11×, with opposite sign. §13's closing instruction —
  *"Do not hide the inversion of the unitary identification rule. It may be one of the most
  informative aspects of the work"* — is honoured.

**Does NOT establish:**
- That `c_KS = −22/5` **to 2.6 %**. The −4.285 centre is 82 % extrapolation with a 2-sample tail
  ratio and an undocumented ±0.15 band; the honest statement is "the extrapolated magnitude is
  **consistent with** 22/5 and inconsistent with 2/5, with the magnitude poorly determined".
- That −22/5 is preferred over **other negative values**. Only two candidates were pre-registered.
  Nothing in the analysis discriminates −4.4 from, say, −4.0 or −5.0; the ratio-sensitivity sweep
  above spans −4.15 to −4.50 under reasonable assumptions.
- That the **biorthogonal machinery** works — the unitary control degenerates to the Hermitian case
  (071.3b), so the non-normal/indefinite features are used but never independently validated.
- That the method is **reproducible by an independent party**: no seed, no versions, no convergence
  check, no control raw data, one code path.
- Anything about **Δ_T**: it is imposed, not measured (071.2).
- Anything about the **α = 4 force exponent at a non-unitary point** — which is what HYP-028 was
  actually about. See §4.
- **Novelty.** No literature gate was run (§5).

#### 071.6 — Verdict proportionality

**Split.** *"c_eff = +2/5 EXCLUDED"* → **proportionate, arguably understated**. *"measure the TRUE
central charge — c_KS = −4.29 ± 0.15"* → **overstated by roughly one confidence level**: the title's
verb is "measure", the evidence supports "extrapolate to a value consistent with". *"PASSED
(discrimination decisive)"* → proportionate **for the binary posed**, misleading if read as
"−22/5 measured to 2.6 %". The `caveats` field is genuinely good and says much of this — but the
title, `verdict` and `key_findings` do not carry it, and the downstream restatements
(`NEXT-SESSION.md`, `HYP-2026-028.json` `phase2_result`, memory index) propagate the title, not the
caveat.

---

## 3. Independence ledger (§7)

### 3.1 The C_TTT ladder is algebraically equivalent to a central-charge ladder

| comparison | side A | side B | shared | classification |
|---|---|---|---|---|
| `C_TTT` vs `2√2/√c` at each rung | measured `c` from `2\|⟨T\|H_{±2}\|0⟩\|²` | `2√2/√c` with the *same* measured `c` | **the same single number** | **ALGEBRAICALLY EQUIVALENT** |
| Ising / TCI / Potts rungs | 067 (ED, circle) | 068 / 069 (puMPS) | KS formula, ZMV codebase lineage, `Δ_T = 2` normalisation, `C_TTT = 2√2/√c` identity | **structurally dependent** across rungs; only the *model* differs |
| `Δ_T` in 067 vs 068/069/071 | 067: **measured** (`v_used = 2.0` exact, `Δ_T` → 1.982 at N=18) | 068/069/071: **imposed** (`v_T` defined by Δ_T ≡ 2) | — | 067 is the only rung where `Δ_T` is independent data |
| ED gate vs puMPS (SIM-069) | independent ED at N=10 | puMPS at N=10 | model, Hamiltonian convention | **PARTIALLY INDEPENDENT — the strongest genuine cross-check in the block** (different algorithm, different code, agreement 1.4e-6 on E0/site) |
| `α = 4` (HYP-025/027) vs `C_TTT` ladder | `α = 2Δ_T` | `C_TTT = 2√2/√c` | both are exact CFT identities evaluated on the same states | **primarily a consistency check** |

**Consequence:** the sentence "α = 4 confirmed at three classes **and** C_TTT confirmed at three
classes" reads as six independent confirmations. It is at most **two numbers per class**
(`Δ_T` and `c`), and in 068/069 it is **one** (`c` alone, since `Δ_T` is imposed). In 057/059/062/063
it is `Δ_T` alone. Both `Δ_T = 2` and `C_TTT = 2√2/√c` are fixed in advance by Virasoro algebra for
every unitary 2D CFT.

### 3.2 SIM-071 dependency chain (§15 style)

```
PAPER-133 method (η = P pairing, PT-edge dodge)
  → SIM-070 h_c^∞ = 1.5587127  [fixed-exponent b = 12/5 fit; theory input]
  → SIM-071 working point                       [shared with SIM-070]
  → M(2,5) identification: |1⟩ = 2nd k=0 state, Δ_φ = −2/5   [theory input]
  → v_ref from the 1−φ split assuming Δ = 2/5   [theory input]
  → Δ-gate window (1.75, 2.25) around Δ_T = 2   [theory input]
  → T state selected
  → v_T ≡ (E_T − E_vac)L/4π  (Δ_T = 2 imposed)  [theory input; cancels identically]
  → c_KS = 8·prod/(E_T − E_vac)²
  → two-level Richardson estimator              [calibrated on SIM-070, 16× smaller lever arm]
  → c_KS = −4.29 ± 0.15
  → "true c, not c_eff"                          [interpretation]
```
Five theory inputs sit upstream of the measured number. **None of them is wrong**, and all are
pre-registered in the design doc. But the chain shows precisely what §15 warns about: the numerical
success validates the **estimator**, not the CFT identification that fed it.

**Genuinely independent information in SIM-071:** the sign of the product, and its magnitude ratio to
the φ-descendant. Nothing else.

### 3.3 Counterfactual novelty (§6) by record

| record | possible outcomes before the run | classification |
|---|---|---|
| 056, 058, 060 | implementation works / fails | **near-zero** (and it failed — informative anyway) |
| 057, 059, 062, 063 | Δ_T ≈ 2 or a bug | **near-zero** |
| 061, 064 | C_σσε → 0.5 or a bug | **near-zero** (exact since BPZ 1984) |
| 065, 066 | Route A extracts spin-2 or not | **moderate** — this was a real open methodological question, and it was answered NO |
| 067, 068, 069 | c → 1/2, 7/10, 4/5 or a bug | **near-zero** |
| 070 | reproduce PAPER-133 or not | **near-zero** (published table) |
| **071** | **c_KS → −22/5, → +2/5, → something else, or → numerically unstable** | **MODERATE-TO-HIGH on the sign** (genuinely binary and not forced by any identity I can find); **moderate on the magnitude** |

**SIM-071 is the only record in the block with meaningful counterfactual novelty**, and 065/066 are
the only others above near-zero. That is a precise, evidence-linked restatement of the project's own
central concern.

---

## 4. Hypothesis-level defect: HYP-028's status does not follow from SIM-070/071

`research/data/hypotheses/HYP-2026-028.json` is now `"status": "SUPPORTED"` (`last_updated`
2026-08-11), with `phase2_result` citing SIM-071. But the record's own **pre-registered criteria
describe a different experiment**:

- `claim`: *"a holographic-force measurement on a non-Hermitian critical chain … will land OUTSIDE
  the established stress-tensor window [3.2, 4.8]"* — about the **force exponent α**.
- `refutation_criteria`: SUPPORTED iff *"alpha lands clearly outside [3.2, 4.8] and within calculable
  error of the a-priori non-unitary primary-tracking value 2\*Delta_phi"*; REFUTED iff α lands inside
  and is stable across N = 12, 14, 16.
- `feasibility_mandatory_gates`: *"HARD non-unitary criticality gate: confirm c_eff = 2/5 via the
  established non-unitary biorthogonal entanglement-entropy scaling AND Delta_phi = −1/5 … BEFORE
  reporting alpha."*

**SIM-070 and SIM-071 measured no α at all**, and ran **no biorthogonal entanglement-entropy c_eff
gate**. SIM-071 *assumes* Δ_φ = −2/5 to calibrate `v_ref`; it does not measure it. So:

- **DEFECT (major): the hypothesis status was advanced to SUPPORTED on the basis of a different
  question than the one registered.** §36 is satisfied in letter — the original `claim`,
  `refutation_criteria` and prior result notes (`result_note_2026-06-26`, `runA_note_2026-06-26`) are
  all **preserved**, which is genuinely good — but the record never reconciles the two, and no field
  states "the original α test remains untested". Anyone reading `status: SUPPORTED` alongside
  `claim` will conclude the force exponent was measured at a non-unitary fixed point. It was not.
- **DEFECT (minor, convention conflict):** HYP-028 says `Delta_phi = −1/5`; SIM-071 and the design
  doc say `Δ_φ = −2/5`. Both are defensible (chiral weight h = −1/5 vs total Δ = h + h̄ = −2/5), but
  the records use the same symbol for a factor-2-different quantity with no note.
- **Positive:** the mandatory gate's *purpose* — confirm the Yang-Lee fixed point was reached — is
  arguably met by SIM-070's reproduction of `R_∞ = −(1+√5)/2` and `g_1` at 0.01 %/0.04 %, which is
  stronger evidence of the fixed point than the registered EE gate would have been. The substitution
  is scientifically defensible; the failure is that it is undocumented.

---

## 5. Novelty gate (§8) — not run, and one prohibited phrase is in the record

**The standard's prohibition, verbatim (§8, Prior-art gate):** *"Avoid vague phrases such as 'to our
knowledge,' 'novel framework,' 'first-ever,' or 'unprecedented' until the evidence for them has been
recorded."*

Repo-wide grep across `research/data/simulations/SIM-2026-05*.json`…`SIM-2026-07*.json` and
`HYP-2026-028.json`:

- **`SIM-2026-071.json` line 22:** *"First lattice extraction **(to our knowledge)** of a NEGATIVE
  central charge from stress-tensor matrix elements; standard approaches obtain only c_eff from
  Casimir scaling."* — **DEFECT (major).** No literature search is recorded anywhere for this claim.
  §8 lists thirteen required search variants for exactly this result (negative central charge,
  effective central charge, non-unitary CFT, biorthogonal CFT, Koo-Saleur generators, lattice
  Virasoro generators, stress-tensor matrix elements, Yang-Lee chains, non-Hermitian spin chains,
  PT-symmetric criticality, transfer matrices, finite-size scaling, logarithmic/non-unitary conformal
  methods). None has been performed. The hypothesis file's scan notes (#12, #14, #15, #18, #19) are
  **weekly-window feeds, not a targeted prior-art search**, and they surface adjacent work
  (PAPER-129 "biorthogonal benchmark", PAPER-132 "PT-BCFT-dual tooling") without ever asking whether
  it already contains this extraction.
- `SIM-2026-058.json` and `SIM-2026-065.json` call TCI `C_TTT` *"the novel target"*. Given F1 this is
  a Level-1 quantity fixed by `c = 7/10`. **DEFECT (minor, mislabel).**
- `SIM-2026-067.json` calls itself *"the first successful C_TTT extraction in the program"* —
  program-scoped, which is fine and verifiable.

**Concrete prior-art evidence already in the repo, against the ladder's novelty:**
`research/tools/pumps-setup/VENDOR.md` capability table records that the vendored ZMV codebase
(pinned `0557b12`) already exports:
- `OBF_Hn_MPO_split` — annotated by the project itself as *"**O'Brien-Fendley H_n MPOs (TCI!)**"*
- `potts3_Hn_MPO_split` — *"**3-state Potts H_n MPOs**"*
- `Hn_in_basis` — the Koo-Saleur matrix-element routine

i.e. **the original authors wrote the Koo-Saleur Fourier-mode machinery for exactly the two models
SIM-068 and SIM-069 measure.** Independently, `SIM-2026-067.json` `results.tci_of` states *"ZMV
needed N ≤ 128 with puMPS for this exact model."* This does not prove ZMV published these `c` values,
but it is strong recorded evidence that both rungs sit inside the prior work's scope, and it makes
the §8 gate mandatory before any framing beyond "we reproduced".

**What the project does that the nearest prior work may not** (the §8 question, honestly answerable
only after the search): the candidate is **SIM-071's biorthogonal extension of the KS estimator to a
non-Hermitian chain in product form with the sign retained**, plus the module-identification
inversion. That is the only item in the block worth taking to a novelty gate.

---

## 6. Record-keeping and infrastructure defects across the block

1. **`research/RESEARCH-LOG.md` stops at 2026-07-21/07-27** (verified: last `^## ` heading is
   *"2026-07-21 / 07-27 — scans #17 and #18"*, line 998 of 1017). **SIM-068 (08-10), SIM-069, 070,
   071 (08-11) are all absent from the chronological narrative**, as is scan #19 (08-09). The four
   most consequential results in the block — including the one the governance doc calls the
   "strongest current frontier result" — are not in the project's own history. **DEFECT (major).**
2. **`research/ERRATA.md` contains zero entries for SIM-056…071** (verified by grep for the IDs and
   for `C_TTT`, `Yang-Lee`, `c_KS`, `biorthog` — no hits). The SIM-067 internal inconsistency
   documented in §2 above is therefore unrecorded.
3. **Missing raw evidence — 11 of 11 cited scratchpad logs absent.** Verified by `find` across the
   repo: `pev_chi6_gate.log`, `z2_v4_gate.log`, `potts_z3_chi6.log`, `potts_chi9.log`,
   `potts_chi12.log`, `ope_chi10.log`, `ope_chi12.log`, `ope_chi12_m8000.log`, `cttt_chi8.log`,
   `cttt_chi10_s1.log`, `cttt_chi12_s1.log` — **all MISSING**. These are the sole raw records for
   SIM-060/061/062/063/064/065/066, including both RunPod sessions (~$14 of compute) and the χ=12
   numbers that closed HYP-025's caveat.
4. **Environment not reproducible for the puMPS work**: `VENDOR.md` states the Julia project env
   *"lives at `research/tools/puMPS/Project.toml` (created locally, gitignored with the source)"*.
   Exact dependency versions for SIM-068/069 are unrecoverable from the repo.
5. **No commit hash on any of the sixteen records.** §21 lists "code revision" first.
6. **Positive, and worth protecting:** none of SIM-067/068/069/070/071 appears in the submitted
   manuscript — grep of `research/paper-draft-scipost.tex` for `C_TTT`, `Yang-Lee`, `Koo-Saleur`
   returns **zero** matches. There is therefore **no overclaiming from this block in the PRD
   submission**. The only published claim touched by this block is `C_σσε = 0.50 ± 0.03` (SIM-064's
   placement-averaged prescription, adopted in paper v5 §7.4), which is the conservative value.

---

## 7. Killer tests (§12) — status

| named killer | applies to | status |
|---|---|---|
| **Yang-Lee method killer** — *"the extracted negative c arises from a normalization convention, eigenvector-conditioning artifact, state misidentification, or exceptional-point instability"* | SIM-071 | **PARTIALLY ADDRESSED.** *Normalization*: refuted — I verified analytically that `c_KS` is invariant under `ψ_R → z·ψ_R`. *State misidentification*: **live** — the Δ-gate is what produces the sign (071.3c); the record documents the hazard but not its load-bearing role. *Eigenvector conditioning*: **untested** — no pseudospectral or ⟨L\|R⟩ health numbers reported. *EP instability*: argued away by construction (h = h_c^∞ is PT-unbroken at finite L, SIM-070 finding 4) but no EP-proximity metric is reported |
| **Universality killer** — *"works only in one finely tuned chain"* | ladder 067/068/069 | Addressed for the unitary ladder (three classes). Untested for YL (**one** non-unitary model; §13 Q10 explicitly asks for a second non-unitary universality class) |
| **Independent-prediction killer** — *"the proposed observable is analytically shown to be fixed entirely by the same CFT data already used in the construction"* | C_TTT ladder | **THIS KILLER HAS FIRED AND IS NOT RECORDED AS SUCH.** `C_TTT = 2√2/√c` is a Virasoro identity; the observable is fixed by `c` (F1) |
| Route-A gate-vacuity | SIM-065/066 | **FIRED AND CORRECTLY RECORDED** — SIM-066 `killer_datum`: G4 = 0.0000 exactly with C_TTT = 25.7. Exemplary |

---

## 8. Defect register (severity-ordered)

| # | sev | defect | where |
|---|---|---|---|
| 1 | major | "C_TTT ladder" measures `c` (2-point) and applies the Virasoro identity `C_TTT = 2√2/√c`; no 3-point contraction at any rung. Framing as "stress-tensor self-coupling" / "graviton self-coupling" implies a measurement never made | `SIM-2026-067.json` `design_evolution`; `SIM-2026-068.json` `method`, `key_findings[0]`; `SIM-2026-069.json` `method`, `title`, `key_findings[0]` |
| 2 | major | Prohibited novelty phrase with no recorded literature gate | `SIM-2026-071.json` `key_findings[1]` ("to our knowledge") |
| 3 | major | SIM-071's unitary control has **no raw output anywhere in the repo**; its three `c_KS` values and 0.49986 exist only inside the summary JSON | `SIM-2026-071.json` `unitary_control`; absent from `research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl` |
| 4 | major | SIM-071's unitary control degenerates to the Hermitian case (P commutes with H ⇒ biorthogonal norms ≡ +1), so it cannot exercise indefinite metric / non-normality / conditioning — the features under test. Control cannot fail in the relevant way (§19) | `qw_yanglee_ks.jl` lines 84–94; `SIM-2026-071.json` `unitary_control.checks` |
| 5 | major | The `c_KS = −4.29` centre is 82 % extrapolation; tail ratio from 2 samples; ±0.15 band asserted, not derived; the calibration case (SIM-070) had a 16× smaller lever arm and a still-drifting ratio | `SIM-2026-071.json` `results.extrapolation`, `key_findings[4]`; cf. `SIM-2026-070.json` `R_inf.method` |
| 6 | major | HYP-028 advanced to `SUPPORTED` on a different question than its registered `claim`/`refutation_criteria` (α at a non-unitary point; c_eff EE gate) — neither tested | `research/data/hypotheses/HYP-2026-028.json` `status`, `claim`, `refutation_criteria`, `feasibility_mandatory_gates`, `phase2_result` |
| 7 | major | SIM-068/069 run the prior authors' own code on models that code already ships KS MPOs for (`OBF_Hn_MPO_split`, `potts3_Hn_MPO_split`); prior-art scope unexamined | `research/tools/pumps-setup/VENDOR.md` capability table; `SIM-2026-067.json` `results.tci_of` |
| 8 | major | RESEARCH-LOG.md missing SIM-068/069/070/071 and scan #19 entirely | `research/RESEARCH-LOG.md` (last heading line 998, dated 07-21/07-27) |
| 9 | major | All 11 cited scratchpad logs missing → SIM-060/061/062/063/064/065/066 have no recoverable raw output, including both RunPod sessions | `SIM-2026-060..066.json` `files` fields |
| 10 | major | SIM-067's two headline numbers are mutually inconsistent through its own identity: `c_inf = 0.49871` ⇒ `C_TTT = 4.00517`, not the quoted 3.9936 (which implies c = 0.50160). Independently extrapolated, undisclosed, 0.29 % apart vs a claimed 0.16 % accuracy. Not in ERRATA | `SIM-2026-067.json` `results.ising`; recomputed from `research/tools/cttt-circle/qw_cttt_circle_results_ising.json` |
| 11 | minor | SIM-071 driver: `eigsolve` start vector `randn(ComplexF64, dim)` unseeded; `info` (convergence) captured and never checked | `research/tools/yanglee-pt/qw_yanglee_ks.jl` line 71 |
| 12 | minor | SIM-071: `⟨1\|1⟩ NEGATIVE at every L`, dead-orientation `~1e-26`, `Z2 zeros ~1e-24` are printed but not persisted (jsonl writer saves only `cks, vT, Tnorm, DT, prods, Dvac`); no stdout log (`ylks_warn.log` 0 bytes) | `qw_yanglee_ks.jl` lines 96–97, 139–144 |
| 13 | minor | SIM-068 quoted band `c_inf = 0.699 ± 0.002` / `C_TTT = 3.381 ± 0.005` excludes its own listed `mid3_exact` variant (0.70212 / 3.3755) although described as "variant spread + fit error" | `SIM-2026-068.json` `fit.quoted` vs `fit.variants.mid3_exact` |
| 14 | minor | SIM-068: an undisclosed discarded N=14 D=10 stage giving `c = 0.00944` (`jT=3`, element array offset by two zeros) precedes the reported 0.825720 stage; not mentioned | `research/tools/pumps-setup/qw_cttt_of_results_2026-08-10.jsonl` line 1 |
| 15 | minor | Element-suppression figures imprecise: SIM-068 "≤0.0003 vs 0.109 (~400×)" — raw max non-T is 1.16e-4 (934×), `others_norm` max 6.35e-4 (171×); SIM-069 "≤6e-4 … ~4000×" — N=10 max is 6.37e-4, N=40 dominance 2827× | `SIM-2026-068.json` `key_findings[1]`; `SIM-2026-069.json` `ed_gate.extra_findings`; raw jsonl |
| 16 | minor | SIM-071 says the k=±2 cluster matches the M(2,5) null-vector prediction *"exactly"*; the φ-descendant `Dvac` is 1.524 at L=18 vs predicted 1.6 (4.8 % short). Third cluster state (Dvac → 3.355) unidentified | `SIM-2026-071.json` `results.spectrum_checks`; raw jsonl `Dvac` |
| 17 | minor | Δ_φ convention conflict: HYP-028 `−1/5` vs SIM-071/design-doc `−2/5`, same symbol, no note | `HYP-2026-028.json` `test_design`; `SIM-2026-071.json` `method` |
| 18 | minor | SIM-056 filed under `HYP-2026-028` (Yang-Lee) though it is the Ising OPE pipeline for HYP-027/025; successors 058/060/061 are filed correctly | `SIM-2026-056.json` `hypothesis_id` |
| 19 | minor | SIM-063 "RESOLVED / caveat CLOSED / clean full tower" rests on **2 of 6** χ=12 seeds with Δσ still 1.5 % off and the clean-basin rate falling with χ (3/6 → 2/6) | `SIM-2026-063.json` `verdict`, `results.basin_rate` |
| 20 | minor | SIM-061 headline word "VALIDATED" while the pre-registered χ=6 spread criterion was violated (0.128 > 0.10); the pass rests on a 4-seed χ=8 run | `SIM-2026-061.json` `verdict`, `results.C_sse` |
| 21 | minor | `SIM-2026-058`/`065` call the TCI `C_TTT` "the novel target" — a quantity fixed by `c = 7/10` | `SIM-2026-058.json` `goal`; `SIM-2026-065.json` `goal` |
| 22 | minor | No commit hash on any of the 16 records; puMPS `Project.toml`/`Manifest.toml` gitignored so SIM-068/069 dependency versions are unrecoverable | all `SIM-2026-05*/06*/07*.json`; `VENDOR.md` line ~37 |

---

## 9. What deserves credit

Guarding against overclaiming cuts both ways; these are load-bearing and verified.

1. **SIM-064's drift resolution is exemplary §20/§22 work.** The record threw away the *tighter*
   number (0.4722, spread 0.0027) in favour of `0.50 ± 0.03` after running a kill-test that
   falsified its own leading suspect. The published value is the conservative one.
2. **SIM-066's `killer_datum`** — gates satisfiable exactly while the number is arbitrary — is a
   textbook §12 killer, applied to the project's own preferred result, retracting a 4.20.
3. **SIM-069's predictive two-error cancellation**: the N=40 D=28 value was called at 0.8022 ± 0.0005
   and landed at 0.80197. The only §18 out-of-sample prediction in the block, and it succeeded.
4. **SIM-069's momentum-resolved ED gate** is the block's only genuinely independent code-path check.
5. **SIM-058's three-clean-basin rule** ("one clean basin is the trap — twice now") is a real
   adversarial protocol that caught a false positive the build agent had already accepted.
6. **SIM-060's root-cause finding** (dense-gauge MERAs hide on-site symmetries in circuits) is a
   genuine §34 state-vs-representation result and it unlocked v4.
7. **`VENDOR.md`** is the best reproducibility artifact in the repository: pinned SHA, fetch command,
   license status stated honestly ("**License: NONE** on the yijian repo — do not redistribute"),
   dependency list, patch notes, and a dated correction of the project's own earlier wrong claim.
8. **SIM-070/071 raw data is committed** and every headline number I re-derived from it matched.
9. **SIM-071 honours §13's closing instruction** not to hide the module-identification inversion.
10. **Nothing from this block is in the submitted manuscript**, so none of the above framing problems
    has reached a referee.

---

## 10. UNVERIFIED

Stated explicitly per protocol; silence is not a pass.

1. **Whether ZMV (arXiv:1710.05397) or any other prior work already published `c` for the
   O'Brien-Fendley tricritical point and/or 3-state Potts via puMPS Koo-Saleur elements.** I did not
   read the paper or search the literature. The repo evidence (`VENDOR.md` exports, SIM-067's own
   note) is suggestive but not decisive. **This is the single highest-value unresolved item.**
2. **Whether SIM-071's result is novel.** No literature gate performed by the project or by me.
3. **PAPER-133's own numbers** (`g_1 = 0.725339(51)`, `R_∞ = −1.62184(94)`, Table I / Eq. 14). Taken
   from `HYP028-BIORTHO-KS-DESIGN.md` and `SIM-2026-070.json`; I did not open
   `research/downloads/2606.16785v2.pdf`.
4. **The SIM-068/069 `c_{n+2}` columns.** My parser extracted only the `n−2` block from the Julia
   `repr(Dict)` dumps; every `n−2` value matched the record exactly, and the record's chirality
   asymmetry claims (≤1e-4) are consistent with that, but I did not independently re-extract `n+2`.
   Consequently the exact **chirality means** (and therefore SIM-068's "0.7008" figure, where raw
   `n−2` is 0.7005406) are unverified at the last digit.
5. **The SIM-069 pre-registration of the N=40 D=28 prediction.** The prediction and its outcome are
   asserted in the same field of the same record; there is no prediction registry (§36).
6. **SIM-071's `⟨1|1⟩ < 0`, the dead-orientation `~1e-26`, and the `Z2 structural zeros ~1e-24`.**
   Computed by the driver, printed, but not persisted; no log exists. I could not verify them and I
   could not falsify them. (Note the persisted `Tnorm` is **positive** at every L, so if the record's
   `⟨1|1⟩ < 0` claim is wrong the sign of the headline would need another explanation.)
7. **Whether the missing scratchpad logs exist outside the repo** (session scratchpad, RunPod pods —
   both pods recorded as killed). I checked only the repository.
8. **The SIM-068/069 wall times and the SIM-071 runtime** — not recorded anywhere I could find.
