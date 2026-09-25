# inv:sims-early — Audit of SIM-2026-001 … SIM-2026-030 and pre-031 named records

Auditor: inv:sims-early
Date: 2026-08-17
Governing standard: `docs/governance/RESEARCH-DIRECTOR.md` (§5 contribution levels, §6 counterfactual
novelty, §7 independence ledger, §8 novelty gates, §12 killer tests, §20 uncertainty, §21
reproducibility, §22 adversarial numerical tests, §38 audit assignment)

Scope: every JSON record in `research/data/simulations/` whose id is in the range SIM-2026-001…030,
plus the non-numeric-named records that predate SIM-031
(`composite_geodesic_results.json`, `worldline_mc_results.json`, `effective_mass_analysis.json`,
`holographic_transport.json`, `holographic_transport_24q.json`, `hyp010_criticality_scan.json`,
`dewitt_correction_results.json`, `normalization_convention_analysis.json`,
`classical_baseline_SIM2026002.json`, `classical_baseline_SIM2026003.json`,
`skin_depth_data.json`, `runpod_gpus.json`). 43 records total.

Everything below is cited to a repo-relative path and a specific field. Where I could not verify,
see **UNVERIFIED** at the end.

---

## 0. Headline of this audit

**The α = 3.92 ± 0.16 force exponent — the paper's stated central finding — is not supported at the
claimed precision by the data in its own record. It is a one-interval measurement whose value moves
by ~1.4 (≈8 of its own quoted σ) when the single point dr = 2 is dropped from the fit window, and
the same shift occurs in all three "consistent evaluations."** The fit's own reduced χ² is 6.0
(`SIM-2026-017-statistics.json` → `power_law_fit.statistics.chi2_reduced`), a formally rejected fit,
and the number appears in neither paper. Detail in §3.

Second finding: **no record in the 001–030 range carries a code revision, environment spec,
dependency version, or output checksum, and every state/parameter input file the headline
measurements depend on is gitignored** (`.gitignore:19` = `*.npy`), so the repository the paper
points to cannot reproduce them. Detail in §5.

---

## 1. Record-by-record inventory

Legend for the reproducibility columns (RESEARCH-DIRECTOR §21):
`rev` code revision · `env` environment/dependency versions · `seed` random seeds ·
`solver` solver/optimizer identity · `conv` convergence criteria/iteration counts ·
`model` model parameters · `input` linked input record/file · `chk` output checksum ·
`ascript` analysis-script revision. `Y` present, `–` absent, `~` partial/free-text only.

### SIM-2026-001 — `research/data/simulations/SIM-2026-001.json`
- **Date** 2026-03-10 (`date`). **Title/desc** MERA holographic force verification for HYP-2026-002;
  binary MERA 16q/3 layers with Ry hologrons vs 20-site ED and the Sahay–Lukin–Cotler AdS form.
- **Measured** `results.quantum.V_quantum` (8 points, dr=1..8, four of them exactly 0.0);
  ED connected correlators (`results.classical_baseline.raw_connected_correlators`);
  fitted ξ = 3.229 (`results.classical_baseline.fitted_xi`) vs theory l_AdS = 1.4427.
- **Pipeline** `circuit.script_path` = `.../mera_circuit_hyp002.py` (exists, tracked);
  `results.quantum.backend` = qiskit-aer statevector; `results.classical_baseline.backend` = scipy eigsh.
- **Verdict** `comparison` = `inconclusive`. Honest: `findings[2]` records χ²/dof = 12204 (~200σ/point).
- **Supports** HYP-2026-002 (nothing quantitative; explicitly a circuit-architecture PoC per `notes`).
- **Repro** rev – · env – · seed – · solver Y · conv – · model Y · input Y · chk – · ascript –.
- **Note** `results.analytical.l_AdS = 1.4426950408889634` = 1/ln 2 exactly. This constant is
  *defined*, not measured, and it propagates into every downstream "agreement" (see §4.2).

### SIM-2026-002 — `SIM-2026-002.json` (1.7 MB)
- **Date** 2026-03-10. VQE of 16q/3-layer binary MERA, 146 params, L-BFGS-B multistart + COBYLA polish.
- **Measured** `vqe.E_optimized` = −19.6422 vs `vqe.E0_exact` = −20.0164 → `vqe.pct_error` 1.8696;
  `vqe.converged_1pct` = **false**; force profile → `fit.xi` = 1.2327 ± 0.3869.
- **Verdict** none. `comparison` is an object juxtaposing `fitted_xi` 1.2327 with
  `paper_l_AdS` 1.4427 — an implied 15 % agreement with no verdict text.
- **DEFECT (major, undocumented in ERRATA).** `research/data/hypotheses/HYP-2026-005.json`
  → `analysis.key_findings[1]` states: *"FINDING 2 (CRITICAL BUG IN PRIOR ANALYSIS): SIM-2026-002 has
  signal only at dr=1 and dr=2. V(dr=3+) is numerical noise. The xi=1.233 reported in project memory
  was fit to APPROXIMATE values read from visualization plots, not the actual V_quantum array."*
  **That correction was never written back into `SIM-2026-002.json`**, which still carries
  `fit.xi = 1.2327465560669981` with a spurious 4-significant-figure error bar and no annotation.
  It is also absent from `research/ERRATA.md`. The bad number is then propagated forward verbatim as
  `previous_no_z2_xi: 1.233` in `SIM-2026-005.json` → `fit` and `SIM-2026-006.json` → `fit`, and used
  as `xi_mera_fitted` in `worldline_mc_results.json` → `decay_analysis`.
- **Repro** rev – · env – · seed – · solver Y (`vqe.optimizers`) · conv Y (`n_total_evals` 61068) ·
  model Y · input – · chk – · ascript –. Optimized θ is in `theta_opt_SIM2026002.npy` (untracked).

### SIM-2026-003 — `SIM-2026-003.json`
- **Date** 2026-03-10. 20q/5-layer MERA VQE, 190 params, H-gate init, 10 seeds.
- **Measured** `vqe.converged_1pct` false, `vqe.converged_2pct` true; per-seed bests in
  `vqe.v2_seed_bests` (10 seeds listed by name — best seed-level metadata in the whole early range).
- **Verdict** none (`feasibility`/`next_steps` only).
- **Repro** rev – · env – · **seed Y (10 named)** · solver Y (`vqe.optimizer`) · conv Y · model Y ·
  input Y (`theta_opt_path`, untracked) · chk – · ascript –.

### SIM-2026-004 — **MISSING**
- No file. `research/ERRATA.md` §D1 records: *"never written — run killed at ~13 % before the
  completion-time JSON write (explained gap)."* Verified absent on disk. Accepted as documented.

### SIM-2026-005 — `SIM-2026-005.json`
- **Date field ABSENT** (file mtime 2026-03-11). Z₂ parity projection onto P=+1, 16q/3L, 4 seeds.
- **Measured** `pct_error` 3.2151; `parity` 1.0000; `force_profile` flat at V ≈ −0.001 for
  dr = 1..6, 8 with a single outlier V(dr=7) = **−0.8455** (`force_profile[6]`, C_two = −0.00788,
  i.e. the two-hologron correlator collapses at exactly one separation).
- **Verdict** none. `fit.xi` = **9.999999999998911 ± 104.03** — the optimizer pinned ξ at its upper
  bound with a 10× error bar. Recorded without any flag.
- **DEFECT (moderate)**: a bound-pinned, unusable fit is stored with no verdict, no failure flag, and
  no comment on the dr = 7 outlier. Diagnosis exists only in prose elsewhere
  (`research/data/papers/hologron-instability-analysis.md:94` — "almost certainly poor VQE convergence").
- **Supports** the paper's Table row `SIM-005 … 3.22 … Force degraded`
  (`research/paper-draft-scipost.tex:673`), which is an accurate reading.
- **Repro** rev – · env – · seed Y (7/42/99/137) · solver ~ (`backend` only) · conv Y (`nfev` 15100) ·
  model Y · input – · chk – · ascript –. No `id` field (uses `sim_id`), no `description`, no `type`, no `date`.

### SIM-2026-006 — `SIM-2026-006.json`
- **Date field ABSENT** (mtime 2026-03-11). 24q/5L, 252 params, RunPod A100 (`backend`), 3 seeds.
- **Measured** `pct_error` 4.3090; `force_profile` V values are **1e−9 to 4e−6**, i.e. numerical noise.
- **Verdict** none. **TRAP (moderate):** `fit` records `xi = 1.42181661551006` immediately adjacent to
  `paper_l_AdS = 1.4427` — a 1.4 % apparent agreement with the project's headline constant — obtained
  from fitting noise: `C1_err` (1.09e−6) exceeds |C1| (7.4e−7) and `xi_err` = 7.18 is 5× the value.
  The paper does **not** propagate this (it correctly says "Force flat",
  `research/paper-draft-scipost.tex:674`), but the record as stored is a live overclaim hazard.
- **Repro** rev – · env ~ ("RunPod A100 (cupy + qiskit-aer)", no versions) · seed Y · solver – ·
  conv Y (`nfev`) · model Y · input – · chk – · ascript –.

### SIM-2026-007 — **MISSING FILE, ID DOUBLE-ASSIGNED**
- `ERRATA.md` §D1/E3: the penalty-VQE record was lost on RunPod teardown (only
  `research/data/simulations/penalty_vqe_24q.py` survives, verified present), and the id is
  simultaneously claimed by `worldline_mc_results.json` → `sim_id: "SIM-2026-007"`. **Verified.**
  `research/RESEARCH-LOG.md:133` mentions it only inside the E3 errata line — there is no first-class
  log entry for either run.

### SIM-2026-008 — `SIM-2026-008.json`
- **Date** 2026-03-12. 8q TFIM PBC pipeline test, HEA ansatz, L-BFGS-B, 3 seeds.
- **Measured** `vqe_results.relative_error_pct` 1.4969 vs eigsh `classical_baseline.E0` −10.2517;
  full `convergence_histories` for all 3 seeds (best convergence provenance in the range).
- **Verdict** `pipeline_verdict` = `PASS`; `comparison.speed_winner` = classical, honestly noted.
- **Level** 1 (validation of the harness). Counterfactual novelty ≈ 0.
- **Repro** rev – · env – · seed ~ (count 3, not values) · solver Y · conv Y (`max_feval_per_seed`) ·
  model Y · input – · chk – · ascript –.

### SIM-2026-008a / 008b / 008c — three files
- `SIM-2026-008a.json`: 8q parity-preserving MERA, 84 params, 2 seeds → `verdict: FAIL`
  (`best_error_pct` 6.397, `energy_pass` false). Clean negative.
- `SIM-2026-008b-8q-test.json`: ALM → post-projection → projection-optimized, `verdict: PASS`,
  `best_error_pct` 1.1150. This is the paper's "1.12 % at 8q" (`paper-draft-scipost.tex` App.,
  data-availability list). Verified.
- `SIM-2026-008c.json`: 24q/5L two-phase ALM+projection, 5 seeds (7/42/99/13/77),
  `best_error_pct` 3.33399, `total_time_s` 160010. This is the paper's "3.33 % at 24 q". Verified.
  No `verdict` field at all; the pass/fail judgement lives only downstream.
- **All three violate the id regex** (`SIM-2026-008a`, `-008b-8q-test`, `-008c` vs
  `templates/simulation-result.json` → `properties.id.pattern`), and all three lack `date`, `type`,
  `description`.
- **Repro** rev – · env – · seed Y · solver Y · conv Y (`alm_rounds`, `proj_evals`, `evals`) ·
  model Y · input – · chk – · ascript –.

### SIM-2026-009 — `SIM-2026-009.json`
- **Date** 2026-03-17. Force profile on the SIM-008c variational state.
- **Verdict** `INCONCLUSIVE_WRONG_GROUND_STATE`. Exemplary self-diagnosis:
  `diagnoses.C_vac_structure` = `FERROMAGNETIC_GHZ`, `diagnoses.root_cause` = "Energy-correlation
  decoupling: 3.33 % energy error is achievable with GHZ-like ferromagnetic superposition that has
  wrong entanglement structure."
- **Note (moderate):** `fits.Ry_dr_ge2` reports ξ = 1.5111 ± 0.5378 with `xi_deviation_pct: 4.7` and
  `xi_within_1sigma: true` against l_AdS — an apparent 4.7 % hit on the headline constant that the
  record itself immediately disqualifies (`diagnoses.Ry_signal_structure`: "Decay SNR only 17 %").
  Good practice; but the "within 1σ" flag on a σ that is 36 % of the value is not evidence of anything.
- **Repro** rev – · env – · seed – · solver ~ · conv – · model Y · input Y (`input_theta`, untracked
  `.npy`) · chk – · ascript –.

### SIM-2026-010 — `SIM-2026-010.json`
- **Date** 2026-03-17. Force profile on the **exact** 24q OBC ground state (`ground_state.method` =
  `eigsh(H, k=1, which='SA')`, `E0_error_pct` 1.1e−6).
- **Measured** four fit families. All exponential fits deviate from l_AdS by 279–712 %
  (`fits.BP_dual_dr_ge2.exponential.xi_deviation_pct` = 712.39). All power-law fits give
  α = 0.386–0.442 — **nowhere near 4** (`fits.*.power_law.alpha`).
- **Verdict field ABSENT.** `status: COMPLETE` only.
- **DEFECT (moderate, structural):** `V_dual` ≈ −`C_vac` to 3–4 digits at every dr
  (e.g. dr=2: C_vac 0.49930 vs V_dual −0.49928), because `C_two_dual` collapses to 1e−5…1e−7. The
  "force" measured here is algebraically just minus the vacuum two-point function; the extracted
  α ≈ 0.44 is the OBC correlator exponent, not an interaction exponent. The record does not say this;
  the successor record does (`SIM-2026-011-interaction.json` → `description`: "Energy-based observable
  replacing wrong ZZ correlator observable from SIM-2026-010"). Superseded, but with no
  supersession field inside SIM-010 itself.
- **Repro** rev – · env – · seed – · solver Y · conv – · model Y · input – · chk – · ascript –.

### SIM-2026-011 — **ID COLLISION** (documented, ERRATA D1)
Two files, both with internal id `SIM-2026-011`:
- `SIM-2026-011.json` — 16q analytical MERA circuit **design** for IBM Heron r3.
  `status: DESIGNED -- awaiting user approval`. `error_budget.total_estimated_error_pct` = 41.2,
  `feasibility_verdict: CHALLENGING (> 20% error)`. `classical_verification.power_law_fit_alpha` is
  **null** while `cft_prediction_alpha` is 0.25 — i.e. the design's own classical check never
  produced an exponent. Never submitted. `notes` is a list, not a string (schema violation).
- `SIM-2026-011-interaction.json` — **the paper's headline 24 q measurement.** See §3.

### SIM-2026-011-interaction — `SIM-2026-011-interaction.json`
- **Date** 2026-03-18. Observable `F(dr) = E_dual − E_0 − 2·dE_single_avg` on the exact 24q OBC GS.
- **Measured** `fits.F_avg_dr_ge2.power_law.alpha` = **3.9217597 ± 0.1589822** (11 points, dr = 2…12);
  `fits.F_avg_all_dr.power_law.alpha` = 2.2956 ± 0.1052 (12 points).
- **Verdict field ABSENT** (`status: COMPLETE`).
- **Supports** paper Result 1 (`paper-draft-scipost.tex:342, 436, 681`).
- Defects in §3 below. Also:
  - `decay_analysis.m_eff` = 3.9218 — the α value stored under the field name `m_eff`, which
    elsewhere in the corpus means the 0.693/0.670 mass (`effective_mass_analysis.json`). Field-name collision.
  - `F_interaction_avg` and `F_interaction_probe_only` are **bit-identical arrays**, and
    `fits.F_avg_dr_ge2` and `fits.F_probe_only_dr_ge2` are bit-identical fits. The record presents
    two named variants that carry zero independent information (§7 independence: *algebraically equivalent*).
  - `norms_single` ≈ 1.13 and `norms_dual` ≈ 1.28: the excited states are **not normalized**. How the
    energies were formed from unnormalized states is not stated (see UNVERIFIED).
- **Repro** rev – · env – · seed – · solver Y (`ground_state.method`) · conv – · model Y ·
  input ~ (predecessor named; the `.npy` state is untracked) · chk – · ascript –.

### SIM-2026-012 — `SIM-2026-012.json`
- **Date** 2026-03-26. Tensor-network classical-complexity analysis, χ = 2..5, 24q/3L.
- **DEFECT (major, verdict overstatement — internal self-contradiction).** For χ = 3 the record's own
  computed verdict is `chi_analysis.3.verdict = "CLASSICALLY_EASY"` with an empty
  `hardness_reasons: []`, yet the summary block asserts
  `qcup_framing.key_finding`: *"chi=3 is genuine quantum advantage territory"* and
  `chi_analysis.3.quantum_advantage_claim: "STRONG"`, and
  `qcup_framing.paper_relevance`: *"Strengthens QCUP proposal."* The same field pair contradicts
  itself for χ = 4. The "STRONG" label is driven solely by `rtn_phase` crossing a
  volume-law/area-law label, not by the hardness computation the record performed.
- The thresholds carrying the whole analysis (`chi_threshold` = 64, treewidth < 30) are asserted
  constants with no derivation or citation inside the record.
- **Verdict** `status: COMPLETE`; no `verdict` field.
- **Repro** rev – · env – · seed – · solver – · conv – · model Y · input – · chk – · ascript –.

### SIM-2026-013 — `SIM-2026-013.json`
- **Date** 2026-03-26. CMI/PEE-thread Crofton test (HYP-2026-012).
- **Measured** `alpha_thread` 0.9097 ± 0.0317 vs `alpha_F_measured` 3.9218 →
  `crofton_verdict: NOT_SUPPORTED`. Clean, correctly-labelled negative.
- `ground_state_source: gs_24q_exact.npy (SIM-2026-011)` — **untracked file** (§5).
- **Repro** rev – · env – · seed – · solver – · conv – · model Y · input Y (untracked) · chk – · ascript –.

### SIM-2026-014 — `SIM-2026-014.json`
- **Date** 2026-03-26. Poisson-kernel test (HYP-2026-011). `verdict: PARTIALLY_SUPPORTED`.
- **Honest:** `note_poisson_kernel` records that the scalar kernel gives α = 4.62, wrong form, and
  labels the numerical test INCONCLUSIVE.
- **Overstatement (minor):** `key_finding` calls a 2.0 % deviation "**STRONGLY** consistent"
  (`cft_consistency_pct: 1.955`) using the ±0.16 covariance error. Under the record-set's own
  bootstrap σ = 0.633 (`SIM-2026-017-statistics.json` → `bootstrap.alpha_std`) the same deviation is
  0.12 σ — consistent, but "strongly" is doing rhetorical work.
- **§6 counterfactual novelty: near zero.** ⟨TT⟩ ~ x⁻⁴ in 2D CFT is a Ward identity; the record says
  so itself (`key_finding`: "exactly from conformal symmetry").

### SIM-2026-015 / 015b / 015c / 015d — the χ = 3 MERA family
- All four **violate the id regex** and all four lack `date` and `type`.
- `SIM-2026-015.json` (8q, χ=3, 470 params, seeds 7/42/99): `best_error_pct` 0.002388,
  `verdict: PASS`, `phase_transition_signal: false`, `power_law_signal: true`. Supports HYP-009
  (PARTIAL). Solid; C_r vs `exact_C_r` comparison present.
- `SIM-2026-015b.json` (8q force profile): 5 points, no fit, no verdict.
- `SIM-2026-015c.json` (16q, χ=3, 1246 params): **single seed (42)**, `best_error_pct` 0.15126,
  `time_s` 9413. This is the paper's "0.15 % at 16 qubits". One seed → no basin control.
- `SIM-2026-015d.json` (16q force profiles): `exact.alpha` = 3.9748 ± 0.1451 and
  `mera.alpha` = 4.0712 ± 0.1778 — the paper's second and third "consistent evaluations".
  - **DEFECT (major).** The MERA fit window is `fit_dr_min: 2`, `fit_n_pts: 10` (dr = 2…11) with
    `sign: -1`, but `mera.V_data` contains **two positive values inside that window**:
    dr = 9 → +0.0012014968 and dr = 10 → +0.00036517. A strictly-negative power law is being
    least-squares fitted through two sign-flipped points. The record carries no flag.
  - `SIM-2026-023.json` later re-fits the same MERA data over the narrower window
    `alpha_fit.fit_window: [2, 6]`, which excludes the sign flips, without saying why.

### SIM-2026-016 — `SIM-2026-016.json`
- No `date`, no `type`. Kinematic-space/Crofton test on the 24q exact GS.
- `alpha_predicted` = −0.3848 vs `alpha_measured` = 3.92 → `verdict: NOT_SUPPORTED`. Clean negative.

### SIM-2026-017-statistics — `SIM-2026-017-statistics.json`
- **Date** 2026-04-07. Goodness-of-fit for the 24q force profile. Internal id `SIM-2026-017`;
  no `SIM-2026-017.json` exists (naming irregularity, not a collision).
- Key numbers: `power_law_fit.statistics.chi2_reduced` = **6.008**, dof 9;
  `exponential_fit.statistics.chi2_reduced` = 1.125e8;
  `model_comparison.delta_AIC_exp_minus_pl` = 11.024;
  `bootstrap`: mean 3.369, **std 0.6335**, median 3.4395, 95 % CI [2.520, 4.192].
- Defects in §3.
- **Repro** rev – · env – · seed – (bootstrap RNG seed not recorded, only `n_resamples: 1000`) ·
  solver – · conv – · model Y · input Y (`source_sim`) · chk – · ascript –.

### SIM-2026-018 — `SIM-2026-018.json`
- No `date`; `type: classical_reanalysis` (non-enum). `verdict: REFUTED`, `confidence: high`.
- **Best-practice record in the range.** `key_finding` explicitly names the false positive:
  *"Amplitude ratio (7.78 vs 7.66, 1.6 % agreement) is a coincidence … max residual 5863 % at dr=12."*
  This is exactly the §12 killer-test culture the standard asks for.
- **Minor internal inconsistency:** `power_law_fit.alpha_sigma` = 0.8723 but
  `actual_sigma_profile` says "sigma ~ dr^(-0.99)" and `key_finding` says "dr^(-0.87)". Three
  statements, two numbers.
- `circuit: {qubits: 0, depth: 0, gates: 0}` — schema padding on a pure re-analysis.

### SIM-2026-019 — `SIM-2026-019.json`
- No `date`; `type: noise_model_simulation`; `circuit.depth` = `"estimated ~48"` (string, schema violation).
- `verdict: PARTIALLY_REFUTED`, `confidence: medium`. Honest and consequential:
  `key_finding` = Helios reaches `dr_max_helios: 2`, not 4; `correction` = the 4-point fit needs
  99.97–99.99 % per gate, "Helios is insufficient for power-law detection".
- **Cross-record tension worth surfacing:** the project's memory index and the paper abstract present
  Helios as "the hardware path" (`paper-draft-scipost.tex:45` — "A hardware path is designed for
  Quantinuum Helios"). SIM-019's own conclusion is that this path can demonstrate *force existence*
  at dr = 1–2 but cannot measure the exponent. The framing is not false, but the limiting result is
  the more informative one and is easy to lose.
- **Assumption not validated:** `noise_model: depolarizing_channel_per_2q_gate` with
  `sigma_shot: 0.01` and `signal_est` values that are asserted, not simulated from a circuit run.

### SIM-2026-020 — `SIM-2026-020.json`
- No `date`; `type: analytic_classical`; `circuit: {0,0,0}`; `runtime_s: 1.2`.
- **DEFECT (moderate, verdict overstatement).** `verdict: CONFIRMED_ANALYTIC` for HYP-2026-015.
  The record itself states `gpu_run_status: "NOT_RUN"` and `note`: *"Full GPU VQE (20 runs, ~9 h)
  would provide definitive experimental confirmation."* No simulation was performed; this is a
  second-order perturbation-theory estimate (`disorder_analysis.*.second_order_energy_shift`) with a
  1.2 s runtime. "CONFIRMED" is not a defensible status token for an unrun test, and
  `CONFIRMED_ANALYTIC` is not in the template's status vocabulary (ERRATA D3 already flags the
  vocabulary drift; this instance is the one where the drift changes the reader's conclusion).
  MEMORY.md carries it as `CONFIRMED_ANALYTIC | med | (needs GPU confirm)` — the caveat survives there.

### SIM-2026-021 — `SIM-2026-021.json`
- No `date`; `type: resource_estimation_analytic`; `runtime_s: 4.8`.
- `verdict: REFUTED` (HYP-2026-016). Good: `hypothesis_claim_vs_result.result` = "Threshold is 50×
  tighter than claimed", with the reason (8q N=40 vs 16q N=56 gate count) stated.
- **Uncited input:** `ionq_cambridge.estimated_fidelity` = "~99.3-99.5 % (based on IonQ Forte,
  Cambridge not publicly disclosed)" — honestly labelled as an estimate, and
  `action_required` says to obtain the real number. Correct practice.

### SIM-2026-022 — `SIM-2026-022.json`
- No `date`; `type: resource_estimation_analytic`; `circuit.depth`/`circuit.gates` are prose strings;
  `comparison: "inconclusive_vs_helios"` (non-enum). `status: DESIGNED`, `verdict: FEASIBLE_MARGINAL`.
- **Broken artifact link:** `visualization_path` = `research/data/simulations/SIM-2026-022_aquila_protocol.png`
  — **file does not exist** (verified; it is the only broken artifact path in the range).
- **Mislabel (minor):** `hyp017_force_budget.comparison_helios` cites `sim_ref: SIM-2026-015d`, a
  purely classical χ=3 MERA calculation, under a field named "comparison_helios".
- Superseded by the HYP-017 closeout (MEMORY: SHELVED, R1–R5 killers); no supersession field here.

### SIM-2026-023 — `SIM-2026-023.json`
- `created_date: 2026-05-01` (not `date`); no `description`. `created_by: classical-simulator`.
- **What was measured:** nothing new. `method` = *"Bootstrap-resampled χ=3 MERA force profile from
  SIM-2026-015d (1000 resamples, gaussian noise sigma=1 %)"*. The σ values are a **synthetic error
  model imposed by assumption**, not a measurement uncertainty; `alpha_fit.sigma: 0.286` is
  propagated assumed noise. `r_squared: 0.9971` describes a fit to 5 points over `fit_window: [2, 6]`.
- **Risk:** this record is the "classical reference baseline" and `emulator_acceptance_window`
  ([3.2, 4.8]) that a hardware run would be judged against. An acceptance window derived from an
  assumed 1 % noise model on a 5-point sub-window of a fit with two sign-flipped points elsewhere is
  weak ground for a hardware pass/fail criterion.

### SIM-2026-024 — `SIM-2026-024.json`
- **Date** 2026-05-15, `type: classical` — schema-clean.
- `results.verdict: REFUTED`, `alpha_fit` 0.8830 vs window [3.2, 4.8]. Strong record: it carries a
  **null control** (`null_control_result`: Néel state, α ≈ −6e−15, `pass: true`), a
  **regulator-stability sweep** (`alpha_vs_cutoff_table`, 20 cutoffs, α invariant to 16 digits), and a
  **PV-vs-hard-cutoff agreement check** (`pv_vs_hardcutoff.delta_alpha: 0.0`). This is the §19
  matched-control discipline the standard asks for and it is the best-controlled record in the range.
- Minor: `F_pee_hard` and `F_pee_pv` are bit-identical arrays, so `G3_pv_hard_agree: true` is a
  tautology at the recorded precision, not an independent check.

### SIM-2026-025 — `SIM-2026-025.json`
- **Date** 2026-05-16, `type: classical`. Fine-dt (1e−3) transport re-run, N = 12 and 16.
- `results.verdict: REFUTED` (HYP-2026-023) with five explicitly enumerated `refutation_reasons`,
  including the self-retraction: `grid_quantization_finding.explanation` — the published 0.72 %
  residual was a dt = 0.05 grid artifact; true `runs.N16.residual_pct_refined` = **−1.205**.
- Also honest about its own limits: `fit_1overN.note` ("2-point fit is algebraically exact but
  degenerate"), `runs.N24.status: EXCLUDED` with a stated wall-time and a double-lobe reason.
- **Best record in the entire early range** by §41 standards. Feeds ERRATA E2 (verified consistent).
- **Defect (minor):** `parent_sim: "SIM-2026-006"` is wrong — SIM-006 is the 24q Z₂ VQE, not a
  transport run. The actual parent is `holographic_transport.json` (see below).
- Schema: `circuit.qubits/depth/gates` are all `null`.

### SIM-2026-026 — `SIM-2026-026.json`
- **Date** 2026-05-16, `type: classical` — schema-clean. `results.verdict: REFUTED`.
- Exemplary: proves the failure analytically (`verdict_reason`: exp(−βH/2)|ψ_gs⟩ ∝ |ψ_gs⟩ for an
  energy eigenstate), scopes the refutation to the protocol not the physics
  (`important_distinction`), and pre-registers the operator
  (`prespecified_operator.locked_before_fitting: true`) per §36.
- **DEFECT (moderate, cross-record):** `results.gate1_self_consistency` validates against
  `T_hyp006_target: 2.25` and reports `residual_pct: 0.0`, `pass: true`. But `2.25` is the
  dt = 0.05 grid-quantized value that **SIM-2026-025, dated the same day, retracted**
  (converged value 2.23888, ERRATA E2). The gate "passes exactly" because it reproduces the same
  quantization artifact, on the same dt = 0.05 grid. A self-consistency gate anchored on a
  superseded number cannot detect the error it was retired for.

### SIM-2026-027 — `SIM-2026-027.json`
- **Date** 2026-05-28, `type: classical` — schema-clean. TFD on a doubled L = 8 register.
- `results.verdict: SUPPORTED_AMPLITUDE` (non-template status).
- **DEFECT (major, verdict overstatement).** The record's own primary sanity gate **FAILED**:
  `results.gate1_self_consistency` = `{T_baseline_measured: 1.300, T_hyp006_target: 2.25,
  residual_pct: 42.22, tolerance_pct: 2.0, pass: false}`. A "SUPPORTED_" verdict token is asserted
  over a 42 % failure of the pre-declared 2 % gate. To its credit the `verdict_reason` discloses this
  in a trailing bracket and downgrades the time-curve to secondary — but the machine-readable status
  field, which is what MEMORY/digests/downstream records read, says SUPPORTED.
- The load-bearing evidence is `spearman(beta, A_int) = 1.000` over a **6-point β ladder** — a rank
  correlation on 6 monotone points is close to information-free as a discriminator.

### SIM-2026-028 — **NEW ID COLLISION (not in ERRATA)**
Two files, both with internal `id: "SIM-2026-028"`:
- `SIM-2026-028.json` (L = 8) — `results.verdict: HOLOGRAPHIC_SIGNAL_BEYOND_WASHOUT`,
  raw gap 183.2 %, with a self-caveat that the 183 % is "partly a sqrt(purity) over-correction artifact".
- `SIM-2026-028-L10.json` (`L_physical: 10`) — same internal id, **same verdict token**, different
  number (`verdict_reason`: "still differ by 373.6 % (>15 %)"), and **the `description` field is a
  verbatim copy of the L = 8 record**, stating "on the same TFD **L=8** register", contradicting its
  own `L_physical: 10`. The L10 record also drops the over-correction caveat entirely, so the
  unqualified 373.6 % is the version that reads as strongest.
- **DEFECT (major, uncorrected supersession).** Both records were overturned by `SIM-2026-030.json`
  (see below) and by MEMORY's HYP-024 row (`NOT_ESTABLISHED (artifact)`), yet **neither file contains
  any supersession, retraction, or backlink field** — grep for `supersed|retract|overturn|SIM-2026-030`
  returns 0 hits in `SIM-2026-028-L10.json` and only an unrelated word match in `SIM-2026-028.json`.
  A reader arriving at these files by id gets an unqualified holographic-signal verdict. This
  violates §32 ("preserve original claim, later challenge, corrected analysis … do not silently edit
  history" — here the failure is the opposite: the correction was never linked back).

### SIM-2026-029 — `SIM-2026-029.json`
- **Date** 2026-05-29, `type: classical` — schema-clean.
- `results.verdict: NONFLAT_BUT_NOT_WANG_HE`. Correctly labelled: the AIC-minimum model is
  `boltzmann` (ΔAIC 16.7 over flat), while `results.shape_fit._selection.wang_he_is_aic_min: false`
  and `wang_he_substantial_over_flat: false`. Honest model-selection discipline.
- **Statistical caution:** `results.shape_fit.wang_he.R2 = −0.668` and `tanh.R2 = −0.668` — negative
  R², i.e. worse than the mean — recorded alongside "chi2_per_dof 0.00018". The two summary
  statistics point in opposite directions and neither is reconciled in the record.

### SIM-2026-030 — `SIM-2026-030.json`
- **Date** 2026-05-29, `type: classical` — schema-clean.
- `results.verdict: INCONCLUSIVE_NORMALIZATION_UNSTABLE`, and the record **catches its own script's
  false positive**: the field is literally named `results.verdict_reason_AUTO_WAS_WRONG` and
  `results.CORRECTED_VERDICT_2026_05_29` states *"the script auto-verdict 'SIM028_SURVIVES_STRONGER_NULL'
  is a FALSE POSITIVE from a logic flaw"* and concludes *"the gap-matched non-critical ferro control
  degrades AS MUCH AS holo … HYP-024's 'beyond washout = holography' claim remains NOT established."*
- This is the strongest §12/§19 work in the range: two gap-matched controls, a pre-registered
  agreement gate, an identified root cause (spectral density, not gap), and an explicit script-bug fix.
- **The problem is not this record — it is that SIM-028/-028-L10 were never annotated to point at it.**

---

## 2. Pre-031 named records

| File | id / date | measured | pipeline | verdict | supports |
|---|---|---|---|---|---|
| `composite_geodesic_results.json` | `sim_id: composite_geodesic_test`, 2026-03-11 | T_null = (π/2)·l_AdS = 2.26618 vs T_measured 2.25 → 0.719 % | analytic embedding-space calculation (no simulation) | `verdict.hypothesis_status: SUPPORTED`, `confidence: high` | HYP-006, paper Result 2 |
| `holographic_transport.json` | **no id, no date** | N=16, `transport_signature.transport_time: 2.25` at `time_evolution.dt: 0.05` | Wang-He H_boundary, 120 steps | none | HYP-006 headline |
| `holographic_transport_24q.json` | **no id, no date** | N=24, `transport_time_measured: 1.55`, `residual_pct: −31.60`, `lin_1N_consistent: "INCONSISTENT"` | expm_multiply Krylov, dt 0.05 | none | (excluded by SIM-025) |
| `worldline_mc_results.json` | `sim_id: SIM-2026-007`, `timestamp: 2026-03-11` | Camporesi–Higuchi heat kernel vs MERA V; `decay_analysis` | Brownian-bridge MC + analytic kernel | `comparison.verdict: MISMATCH` | HYP-007 |
| `effective_mass_analysis.json` | **no id**, 2026-03-12 | `m_eff_from_epsilon_CFT: 0.6931` vs `m_eff_from_MERA: 0.6698` → "3.5 %" | 16q ED spectrum + algebra | `resolution.verdict: PARTIALLY_RESOLVED` | paper Result 4 (m_eff) |
| `hyp010_criticality_scan.json` | **no id, no date, no description** | detuning/TFIM criticality scans | ED | none | HYP-010 |
| `dewitt_correction_results.json` | **no id, no date** | ξ under DeWitt/ghost corrections; `best_fit_alpha: 0.5` | analytic | `verdict: PARTIAL` | Roux PAPER-2026-023 |
| `normalization_convention_analysis.json` | **no id**, 2026-03-14 | our ξ = 2.157 vs Sahay ξ = 1.22; scale ratio ~500× | analytic comparison | `conclusion` prose only | convention reconciliation |
| `classical_baseline_SIM2026002.json` | `sim_id: SIM-2026-002-classical`, 2026-03-10 | N=16 **PBC** ED, E0 = −20.4046 | eigsh | none | baseline for SIM-002 |
| `classical_baseline_SIM2026003.json` | `sim_id: SIM-2026-003-classical`, 2026-03-10 | N=20 OBC+PBC ED | eigsh | none | baseline for SIM-003 |
| `skin_depth_data.json` | **no id/date/desc/type** | EM skin depth in granite/concrete | analytic | none | **not a quantum-worldline simulation at all** |
| `runpod_gpus.json` | **no id/date/desc/type** | GPU price list | API dump | none | **infrastructure, not a simulation** |

Specific defects in this group:

- **`worldline_mc_results.json` — the Monte Carlo failed its own validation.**
  `mc_validation.mc_quality` = *"POOR: slope=26.337 != 1.0. Flat Euclidean bridge is a poor importance
  sampler for H². … the MC does not correctly estimate relative K values."* The record then
  substitutes the **analytic** Camporesi–Higuchi formula. So the file named "worldline MC results"
  contains no usable worldline Monte-Carlo result; the surviving content is a closed-form propagator
  evaluation. The record says this plainly (good), but the filename, `algorithm` field, and the
  paper's data-availability line (`paper-draft-scipost.tex`: "worldline_mc_results.json
  (Camporesi–Higuchi validation)") all read as if an MC was validated.
- **Confirms ERRATA D2**: `decay_analysis.m_eff_to_match_mera_2pt: NaN` — literal `NaN`, invalid
  strict JSON. Verified with a strict parser (`parse_constant` raising). **Also newly found:
  `SIM-2026-031.json` contains a literal `NaN`** — outside my range, flagged for the neighbouring
  auditor; ERRATA D2 names only `worldline_mc_results.json`.
- **`classical_baseline_SIM2026002.json` baselines the wrong boundary condition.** It is
  `boundary: "periodic"` with `E0: −20.4046`, while `SIM-2026-002.json` → `vqe.E0_exact` is
  −20.0164 (OBC, per its `description`). A "classical baseline" at a different boundary condition and
  a different ground-state energy is not a baseline for that run. Its own
  `fits.force_profile.xi` is again bound-pinned at 9.999999999999995.
- **`composite_geodesic_results.json` is analytic, not a measurement.** `calculations.composite_geodesic.formula`
  = `T_composite = pi*R/2`, and `verdict.best_agreement` = *"l_AdS_MERA = 1/log(2) = 1.4427 gives
  T_null = 2.265"*. Counterfactual novelty (§6) is **near zero on the theory side** — π/2 is fixed by
  the null condition — so the only content is the measured 2.25, which SIM-025 later showed is a
  grid artifact for 2.23888. The record's `confidence: high` predates that.
  It also carries `l_AdS_needed_to_match_exact: 1.432394487827058`, the source of ERRATA E1.

---

## 3. The α = 3.92 result — detailed defect analysis

This is the paper's stated central finding (`paper-draft-scipost.tex:548`: *"The power-law
F(dr) ~ dr^{-3.92} result is the central finding of this work"*). Five distinct problems, all
verifiable from the records.

### 3.1 The data contain no power-law plateau (NEW — not documented anywhere)
I recomputed the local logarithmic slope, ln(F_i/F_j)/ln(dr_j/dr_i), from
`SIM-2026-011-interaction.json` → `F_interaction_avg`:

| dr interval | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 | 10→11 | 11→12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| local α | 2.035 | **4.232** | 2.603 | 2.456 | 2.461 | 2.533 | 2.658 | 2.841 | 3.102 | 3.482 | 4.064 |

A genuine F ~ dr⁻⁴ would give ≈ 4 at every interval. The measured local slope sits at **2.45–2.66
across the middle of the range**, spikes to 4.23 at the single dr = 2→3 step, and drifts upward at
the chain-end points where OBC contamination is largest. The same pattern is in both 16 q datasets
(`SIM-2026-015d.json`): exact = 2.10, **4.24**, 2.74, 2.64, 2.71, 2.88, 3.16, 3.65, 4.52, 6.33;
MERA = 2.10, **4.40**, 2.37, 2.58, 3.61, 3.76, 6.02, sign-flip, 11.30, sign-flip.

### 3.2 The point estimate is a one-interval measurement (NEW)
Refitting each dataset with the window's lower edge moved by one point (`curve_fit`, same model
A·dr^(−α), verified to reproduce the recorded values exactly at dr ≥ 2):

| dataset | dr ≥ 2 (as recorded) | dr ≥ 3 | dr ≥ 4 | dr ≥ 5 |
|---|---|---|---|---|
| 24 q exact (SIM-011) | **3.922 ± 0.159** | 2.559 ± 0.019 | 2.534 ± 0.038 | 2.621 ± 0.058 |
| 16 q exact (SIM-015d) | **3.975 ± 0.145** | 2.753 ± 0.035 | 2.801 ± 0.076 | 2.992 ± 0.120 |
| 16 q χ=3 MERA (SIM-015d) | **4.071 ± 0.178** | 2.745 ± 0.175 | 3.322 ± 0.315 | 4.331 ± 0.550 |

Dropping one point moves α by ~1.4 — about **8× the quoted uncertainty** — in all three datasets, in
the same direction, toward the scalar value the paper says it excludes. The recorded ±0.16 is a
covariance error conditioned on a fixed window; the fit-window systematic is larger than the entire
claimed discrimination between α = 2 and α = 4 and is quantified nowhere in the records or the papers.

### 3.3 The robustness check cannot detect the dominant systematic
The paper's stated robustness test is anchor variation
(`paper-draft-scipost.tex:348`: *"the measured α varies by only 0.027 across anchors"*). In
`SIM-2026-017-statistics.json` → `anchor_dependence.results`, **all four anchors use
`dr_values` starting at 2**, and the anchor 4/6/8 `F_values` agree with each other to ~12
significant figures (anchor 4 dr=12: −0.0022218714808914797; anchor 6 dr=12: −0.0022218714807848983).
So the check varies a parameter the observable is nearly invariant under, while holding fixed the
one choice that actually determines the answer. Per §19 ("do not choose controls that are designed
to fail" — the inverse failure applies here: a control that cannot fail is not a control).

### 3.4 The preferred model is itself a rejected fit, and this is not reported
`SIM-2026-017-statistics.json` → `power_law_fit.statistics.chi2_reduced` = **6.008** on dof = 9
(p ≈ 1e−7). The record also shows the two summary statistics were computed under **different error
models**: `chi2` uses supplied per-point uncertainties (giving 54.07 for the power law and 1.01e9 for
the exponential), while `AIC`/`BIC` are RSS-based Gaussian (ΔAIC = 11·ln(RSS_exp/RSS_pl) = 11.02,
which I reproduced exactly). Neither `paper-draft-scipost.tex` nor
`research/submission-package/prd/paper-prd.tex` contains any χ² for this fit (verified by grep); both
quote only the favourable ΔAIC = 11.0. The bootstrap in the same record —
`bootstrap.alpha_mean` 3.369, `alpha_std` **0.6335**, CI [2.520, 4.192] — gives an uncertainty
**4× larger** than the headline ±0.16 and a central value 0.55 below the headline. The paper quotes
the CI (line 346) but keeps ±0.16 as the headline error.

### 3.5 The χ = 3 MERA evaluation fits sign-flipped points
`SIM-2026-015d.json` → `mera.V_data` has dr = 9 → +0.00120 and dr = 10 → +0.00037 inside a
`fit_dr_min: 2`, `fit_n_pts: 10`, `sign: -1` window. Two of ten fitted points have the wrong sign for
the model being fitted. Unflagged.

### 3.6 Independence ledger for the "three consistent evaluations" (§7)
| | 24 q exact | 16 q exact | 16 q χ=3 MERA |
|---|---|---|---|
| model | critical TFIM, OBC | critical TFIM, OBC | same 16 q state, variationally approximated (0.15 % E error) |
| state source | `eigsh` | `eigsh` | MERA optimized to the same H |
| observable | F = E_dual − E_0 − 2ΔE_single | identical | identical |
| boundary-primary coeffs | α=0.635, β=−0.026 | same construction | same |
| fit model / window | A·dr^−α, dr ≥ 2 | identical | identical |
| fit code | same | same | same |

**Classification: structurally dependent / primarily a consistency check.** The three numbers are one
observable, one operator, one fitting procedure, and one fit window, applied at two system sizes of
the same model plus one variational approximation of one of them. They are not three independent
tests of α = 4; §7 requires they be described that way. The paper describes them as
"three consistent evaluations" (`paper-draft-scipost.tex:45, 552, 629`), which is literally true and
readable as more than it is.

### 3.7 Contribution level and counterfactual novelty (§5, §6)
Δ_T = 2 holds in every unitary 2D CFT, so 2Δ_T = 4 is fixed in advance; `SIM-2026-014.json` →
`key_finding` states this itself ("exactly from conformal symmetry"). **Level 1 (validation)**;
counterfactual novelty **near zero** on the theory side. The only genuinely open outcome was whether
the lattice observable would exhibit the asymptotics — and §3.1 shows the recorded data do not
exhibit a plateau, so even that question is not yet answered by these records.

---

## 4. Other claims traced through this record set

### 4.1 Transport T = (π/2)·l_AdS
- Chain: `holographic_transport.json` (**no id, no date**, dt = 0.05, T = 2.25) →
  `composite_geodesic_results.json` (analytic π/2, 0.719 % agreement) → `SIM-2026-025.json`
  (dt = 1e−3, T = 2.23888, residual **−1.205 %**, self-retraction) → ERRATA E2.
- **Record-linkage defect:** the paper's Result 2 rests on a file that carries **no `id`, no `date`,
  no `hypothesis` record header and no `verdict`** — `holographic_transport.json`. There is no
  SIM-2026-0NN record for the original HYP-006 transport measurement anywhere in the range.
  `SIM-2026-025.json` → `parent_sim` points at the wrong record (SIM-2026-006).
- The N = 24 companion (`holographic_transport_24q.json`) records `residual_pct: −31.60` and
  `lin_finite_size.lin_1N_consistent: "INCONSISTENT"` and is correctly excluded by SIM-025.
- The two-size trend (−2.78 % @ N=12, −1.21 % @ N=16) is a **two-point** finite-size argument;
  `SIM-2026-025.json` → `fit_1overN.note` says so itself ("degenerate — cannot distinguish 1/N from
  1/N²"). §17 (move beyond single-number agreements) is not yet satisfied here.

### 4.2 m_eff = 0.693 vs 0.670 (3.5 %) — the weakest surviving paper claim in this range
- `effective_mass_analysis.json` → `ads_mass_dimension.epsilon_m_eff` = 0.6931. This is **ln 2**,
  i.e. exactly 1/l_AdS for the project's l_AdS = 1/ln 2, obtained by inserting Δ_ε = 1 into
  m²l² = Δ(Δ−2) = −1. It is an algebraic identity with **zero counterfactual novelty** (§6);
  ERRATA E4 already notes "0.693 = 1/l_AdS from Δ=1 exactly".
- The other side, `m_eff_from_MERA` = 0.6698, comes from Δ = l_AdS/ξ_2pt with
  ξ_2pt = 2.154 — and `research/data/hypotheses/HYP-2026-005.json` → `analysis.key_findings[2]`
  states that ξ_2pt is *"from the ratio V(2)/V(1)"*, i.e. **two data points**, on the SIM-002 χ = 2
  MERA whose correlations the paper itself describes as *"flat (wrong universality class)"*
  (`paper-draft-scipost.tex:486` figure caption).
- So the "3.5 % agreement" compares an exact CFT constant against a single ratio of two numbers taken
  from a state the same paper disqualifies elsewhere. The corresponding row in
  `worldline_mc_results.json` → `decay_analysis.m_eff_to_match_mera_2pt` is literally `NaN`.
- `research/data/theory/research-challenge.md:99-103` reaches the same conclusion independently
  (*"post-hoc rationalization, not a prediction … The 'agreement' was found, not predicted"*), which
  strengthens rather than weakens this finding.
- **Note for the audit lead:** the task brief states `research/data/theory/` is EMPTY. **It is not.**
  It contains 8 files (`RUN-A-methods.md`, `epsilon-channel-proof.md`, `paper-review-synthesis.md`,
  `research-challenge.md`, `research-practical.md`, `research-primary.md`, `task4-ope-argument.md`,
  `task5-crofton-derivation.md`). The §14 defect is real but different from the one stated: the
  directory holds **prose, not structured theory records** — no schema, no `templates/theory-*.json`,
  no claim-dependency fields.

### 4.3 Z₂ two-phase method (1.12 % @ 8 q, 3.33 % @ 24 q)
- `SIM-2026-008b-8q-test.json` → `best_error_pct` 1.1150; `SIM-2026-008c.json` → `best_error_pct`
  3.33399, 5 seeds, both verified against the paper's numbers. **Level 2 (methodological)** and the
  most defensible contribution in this range: it is a real optimizer result with seed spread, not a
  CFT-fixed quantity. Its weakness is §21, not §6 — no environment, no code revision, and the θ
  output is untracked.

---

## 5. Reproducibility findings (§21) — the systematic gap

Nine §21 elements, measured across the 43 in-scope records:

| §21 element | records with it | notes |
|---|---|---|
| code revision (git SHA/tag) | **0 / 43** | grep for `git|commit|sha|revision` returns only false positives inside prose words |
| environment specification | **0 / 43** | free-text only (`"RunPod A100 (cupy + qiskit-aer)"`, `"local_cpu"`) |
| dependency versions | **0 / 43** | no `qiskit`/`numpy`/`scipy` version anywhere |
| platform information | ~14 / 43 | `hardware` / `hardware_target` free-text strings only |
| random seeds | 11 / 43 | good in the VQE family (001–015c), absent everywhere after; **bootstrap seeds never recorded** (SIM-017, SIM-023) |
| model parameters | 43 / 43 | consistently good |
| solver settings | 20 / 43 | `optimizer`, `eigsh`, `integrator` named; tolerances rarely given |
| convergence criteria | 13 / 43 | `nfev`/`evals`/`n_steps` present; explicit tolerances almost never |
| output checksums | **0 / 43** | none |
| analysis-script revision | **0 / 43** | some `script_path`, no revision |

**The load-bearing finding: every state/parameter array these results depend on is gitignored.**
`.gitignore:19` is `*.npy`. `git ls-files research/data/simulations/ | grep -c '\.npy$'` = **0**,
against **31 `.npy` files on disk**. Untracked inputs include `gs_24q_exact.npy` (the input to
SIM-011-interaction and SIM-013, i.e. the α = 3.92 measurement), `theta_opt_SIM2026008c.npy`
(input to SIM-009 via its `input_theta` field), `theta_opt_SIM2026002.npy`, `theta_opt_SIM2026003.npy`,
`theta_opt_SIM2026015.npy`, and the transport arrays.

Meanwhile `paper-draft-scipost.tex` App. "Data and code availability" states: *"All simulation data
and scripts are available at https://github.com/jonboy648/quantum-worldline."* **That statement is
not true for the state and parameter arrays.** A reader cloning the repo can read the JSON summaries
but cannot regenerate the ground states or optimized MERA parameters. This is a §21 violation with
direct manuscript consequences and it is **not in ERRATA**.

Broken/absent artifact links in range: `SIM-2026-022.json` → `visualization_path` (PNG missing).
All other referenced `.py`/`.png` paths verified present.

---

## 6. Defect register

**ID collisions**
| # | severity | finding | location |
|---|---|---|---|
| C1 | documented | SIM-2026-011 assigned to a design record and the headline measurement | `SIM-2026-011.json`, `SIM-2026-011-interaction.json` (ERRATA D1) |
| C2 | documented | SIM-2026-007 double-assigned (lost penalty-VQE + worldline MC) | `worldline_mc_results.json` → `sim_id`; ERRATA D1/E3 |
| C3 | **major, NEW** | SIM-2026-028 assigned to two different runs (L=8 and L=10), and the L10 record's `description` still says "L=8", contradicting its own `L_physical: 10` | `SIM-2026-028.json`, `SIM-2026-028-L10.json` |
| C4 | minor, out of range | SIM-2026-045 also double-assigned (`SIM-2026-045.json`, `SIM-2026-045-chi6.json`) | flagged for the neighbouring auditor |

**Missing records**
| # | severity | finding |
|---|---|---|
| M1 | documented | SIM-2026-004 never written (ERRATA D1) — verified absent |
| M2 | documented | SIM-2026-007 JSON lost (ERRATA E3) — `penalty_vqe_24q.py` verified present |
| M3 | **major, NEW** | The HYP-006 transport measurement (paper Result 2) has **no SIM-2026-0NN record**; it lives in `holographic_transport.json`, which has no `id`, `date`, `description`, `type` or `verdict` |

**Invalid JSON**
| # | severity | finding |
|---|---|---|
| J1 | documented | `worldline_mc_results.json` contains literal `NaN` (ERRATA D2) — **verified** at `decay_analysis.m_eff_to_match_mera_2pt` |
| J2 | minor, NEW (out of range) | `SIM-2026-031.json` also contains a literal `NaN` — ERRATA D2 names only one file |
| — | — | No other strict-JSON violations in the 84 files in the directory (checked with `parse_constant` raising) |

**Schema conformance (ERRATA D3, re-measured for this range)**
Only **8 of 43** in-scope records satisfy `templates/simulation-result.json`
(SIM-001, 024, 026, 027, 028, 028-L10, 029, 030). Failures: 7 records with no `id` field (use
`sim_id`) plus 8 with no `id` at all; 7 id-regex violations (008a, 008b-8q-test, 008c, 015b, 015c,
015d, and the two `sim_id`-only VQE records); 26 with missing or non-enum `type`; 18 with no `date`;
4 with `comparison` as an object where the schema requires an enum string; 3 with non-integer
`circuit.depth`/`gates`; 1 with `notes` as a list.
`skin_depth_data.json` and `runpod_gpus.json` are not simulations at all and should not live in
this directory.

**Verdict wording that overstates the numbers**
| # | severity | finding | location |
|---|---|---|---|
| V1 | **major** | `verdict: CONFIRMED_ANALYTIC` on a test that was never run (`gpu_run_status: "NOT_RUN"`, `runtime_s: 1.2`, pure 2nd-order perturbation estimate) | `SIM-2026-020.json` |
| V2 | **major** | `verdict: SUPPORTED_AMPLITUDE` while the record's own pre-declared self-consistency gate fails at 42.2 % against a 2 % tolerance (`gate1_self_consistency.pass: false`) | `SIM-2026-027.json` |
| V3 | **major** | `qcup_framing.key_finding` = "chi=3 is genuine quantum advantage territory" directly contradicts the same file's `chi_analysis.3.verdict = "CLASSICALLY_EASY"` with `hardness_reasons: []` | `SIM-2026-012.json` |
| V4 | **major** | `HOLOGRAPHIC_SIGNAL_BEYOND_WASHOUT` retained with no supersession backlink after `SIM-2026-030.json` refuted it; the L10 file states 373.6 % with the over-correction caveat dropped | `SIM-2026-028.json`, `SIM-2026-028-L10.json` |
| V5 | moderate | Bound-pinned fit `xi = 9.9999999999989 ± 104.0` stored with no verdict and no failure flag; dr=7 outlier (V = −0.845 against a −0.001 baseline) uncommented | `SIM-2026-005.json` → `fit`, `force_profile[6]` |
| V6 | moderate | `xi = 1.4218` printed beside `paper_l_AdS = 1.4427` from a fit to 1e−9-amplitude noise (`C1_err` > \|C1\|, `xi_err` = 5×\|xi\|); no verdict field | `SIM-2026-006.json` → `fit` |
| V7 | moderate | 2.0 % deviation called "**STRONGLY** consistent" using the ±0.16 covariance error rather than the ±0.63 bootstrap σ from the same corpus | `SIM-2026-014.json` → `key_finding` |
| V8 | moderate | Gate 1 "PASSED exactly (0.00 % residual)" against `T_hyp006_target: 2.25`, the coarse-grid value retracted the same day by SIM-025 (converged 2.23888) | `SIM-2026-026.json` → `results.gate1_self_consistency` |
| V9 | minor | `alpha_sigma: 0.8723` vs prose "dr^(-0.99)" vs key_finding "dr^(-0.87)" — three statements, two numbers | `SIM-2026-018.json` |
| V10 | minor | α value 3.9218 stored in a field named `m_eff`, colliding with the corpus's other m_eff (0.693) | `SIM-2026-011-interaction.json` → `decay_analysis.m_eff` |

**Analysis defects (new, none previously documented)**
| # | severity | finding |
|---|---|---|
| A1 | **critical** | α = 3.92/3.97/4.07 shifts to 2.56/2.75/2.75 when dr = 2 is dropped — ~8× the quoted ±0.16, same direction in all three datasets. Fit-window systematic unquantified everywhere. (§3.2) |
| A2 | **critical** | The recorded F(dr) has no power-law plateau: local exponent runs 2.0 → 4.2 → 2.5 → … → 4.1. (§3.1) |
| A3 | **major** | Headline fit's own `chi2_reduced = 6.008` (dof 9) appears in no paper version; only the favourable ΔAIC is quoted. Bootstrap σ = 0.633 vs headline ±0.16. (§3.4) |
| A4 | **major** | The anchor-robustness control holds `dr_min = 2` fixed at all four anchors and the anchor `F_values` agree to ~12 digits — it cannot detect A1. (§3.3) |
| A5 | **major** | The χ=3 MERA α = 4.07 fit includes two positive points inside a `sign: -1` window. (§3.5) |
| A6 | **major** | The paper's "three consistent evaluations" are structurally dependent (one observable, one operator, one fit window, one code path). (§3.6) |
| A7 | **major** | HYP-2026-005's "CRITICAL BUG" finding (ξ = 1.233 was fitted to values read off a plot) was never written back into `SIM-2026-002.json` and is absent from ERRATA; the number propagates to SIM-005, SIM-006 and `worldline_mc_results.json`. |
| A8 | **major** | The MC in `worldline_mc_results.json` failed validation (`mc_quality: "POOR: slope=26.337 != 1.0"`) and was replaced by an analytic formula; filename, `algorithm` field, and the paper's data-availability line all still read as a validated MC. |
| A9 | moderate | `SIM-2026-010.json`'s "force" is algebraically −C_vac (because `C_two_dual` ≈ 1e−6), so its α ≈ 0.44 is the correlator exponent, not an interaction exponent. Superseded without an in-file supersession field. |
| A10 | moderate | `classical_baseline_SIM2026002.json` is PBC (E0 = −20.4046) while the run it baselines is OBC (E0 = −20.0164). |
| A11 | moderate | `SIM-2026-011-interaction.json` states `norms_single ≈ 1.13`, `norms_dual ≈ 1.28` — excited states are unnormalized; the energy convention is not recorded. |
| A12 | moderate | `SIM-2026-023.json`'s error bars and acceptance window are propagated *assumed* 1 % Gaussian noise on SIM-015d values, and its `fit_window: [2,6]` silently excludes the sign-flipped points. |
| A13 | minor | `F_interaction_avg` ≡ `F_interaction_probe_only` and `F_pee_hard` ≡ `F_pee_pv` (bit-identical), so the corresponding "agreement" guards are tautologies. |
| A14 | minor | `SIM-2026-025.json` → `parent_sim: "SIM-2026-006"` is the wrong predecessor. |
| A15 | minor | `SIM-2026-022.json` → `visualization_path` PNG does not exist. |
| A16 | minor | MEMORY.md's force line says "12 pts (SIM-011)"; the record and the paper both use 11 (`SIM-2026-017-statistics.json` → `power_law_fit.statistics.n_points: 11`). The 12-point fit gives α = 2.296. |

---

## 7. What is actually strong in this range

Stated plainly, because an accurate map must record this too:

1. **`SIM-2026-025.json`** — self-retraction of a published number, with an explicitly enumerated
   refutation list, a stated computational-infeasibility exclusion, and honest labelling of a
   degenerate 2-point fit. Meets §41 end to end.
2. **`SIM-2026-030.json`** — catches its own script's false positive, names the field
   `verdict_reason_AUTO_WAS_WRONG`, identifies the root cause (spectral density, not gap), and
   concludes against the project's preferred interpretation. This is §12 and §19 done properly.
3. **`SIM-2026-024.json`** — the best-controlled record: null control, 20-point regulator sweep,
   cross-method agreement check, pre-declared acceptance window, REFUTED verdict.
4. **`SIM-2026-018.json`** — explicitly identifies a 1.6 % amplitude "agreement" as coincidence and
   refutes on profile shape. Precisely the discipline the whole program needs applied to α = 3.92.
5. **`SIM-2026-009.json`** — refuses to report a force from a state it diagnoses as GHZ-like, despite
   a tempting ξ within 1σ of l_AdS.
6. **`SIM-2026-008b/008c`** — the Z₂ two-phase optimizer result is a genuine **Level 2** contribution
   with real seed spread and no CFT-fixed answer.

The pattern is clear and worth naming: **records that test the project's own preferred conclusion are
rigorous; records that confirm it are not.** SIM-018, 024, 025, 030 all set acceptance windows,
controls and refutation criteria in advance. SIM-011-interaction, 015d and 017 — the ones that produce
the headline — have no verdict field, no window-sensitivity test, an unreported χ²_red = 6, and a
"robustness check" that cannot fail.

---

## 8. UNVERIFIED

1. **Energy convention with unnormalized states.** `SIM-2026-011-interaction.json` records
   `norms_single`/`norms_dual` ≠ 1 but not whether `E_singles`/`E_duals` are ⟨ψ|H|ψ⟩ or
   ⟨ψ|H|ψ⟩/⟨ψ|ψ⟩. I did not locate the generating script for this record (no `script_path` field), so
   I could not determine whether the normalization affects F(dr). If it does, it would bear on §3.1.
2. **Whether the α ≈ 2.5 plateau at dr ≥ 3 is physical or OBC contamination.** I established the
   window sensitivity numerically; I did not determine which end of the range is the contaminated one.
   A finite-size study (N = 8/16/24/32, as `paper-draft-scipost.tex:611` itself proposes) would settle it.
   I make no claim that α = 4 is wrong — only that the records do not establish it at ±0.16.
3. **Provenance of `m_eff_from_MERA = 0.6698`.** `effective_mass_analysis.json` gives ξ_MERA = 2.154
   and m_eff = 0.6698, but 1/2.154 = 0.4643 and l_AdS/ξ = 0.6698 only under the Δ = l_AdS/ξ route
   described in `HYP-2026-005.json`. I confirmed the route from the hypothesis record but not from a
   script.
4. **PAPER-2026-003 / Sahay citation consistency.** `SIM-2026-001.json` cites "Sahay, Lukin, Cotler
   (PRX 2026)"; `normalization_convention_analysis.json` cites "arXiv:2209.12903"; the paper cites
   `SahayLukinCotler2025`. I did not open the paper records to reconcile these; out of scope but
   worth one grep by the literature auditor.
5. **Whether the `.npy` inputs were ever archived elsewhere** (Zenodo deposit, RunPod snapshot). I
   verified only that they are gitignored and untracked in this repository.
6. **`hyp010_criticality_scan.json` and `dewitt_correction_results.json` scientific content.** Both
   are headerless (no id/date/description); I catalogued their fields but did not trace what claim, if
   any, they currently support. Neither is cited in `paper-draft-scipost.tex`.
7. **`skin_depth_data.json` / `runpod_gpus.json` provenance.** I classified them as non-simulation
   artifacts by content; I did not trace which task deposited them here.
8. **Reduced-χ² error model.** `SIM-2026-017-statistics.json` reports χ² but not the per-point σ used.
   χ²_red = 6.0 could reflect an underestimated σ rather than model inadequacy. Either reading
   undermines the ±0.16, but the distinction matters for how to fix it.
