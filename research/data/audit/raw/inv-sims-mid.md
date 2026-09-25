# inv:sims-mid — Audit of SIM-2026-031 through SIM-2026-055

Auditor: subagent `inv:sims-mid`. Date of audit: 2026-08-17.
Governing standard: `docs/governance/RESEARCH-DIRECTOR.md` (§5 contribution levels, §6 counterfactual
novelty, §7 independence ledger, §8 novelty gates, §12 killer tests, §20 uncertainty, §21
reproducibility, §32 retraction discipline, §38 audit assignment).

All citations are repo-relative paths plus the specific JSON field or file line relied on.

---

## 0. Headline of this range

**The retraction that IS documented (ERRATA D5 / SIM-036) propagated correctly to two of the four
records ERRATA D5 itself names, and NOT to the other two. Separately, a second over-claim of the same
severity — SIM-2026-042's "TCI Delta_T~2 FOUND … UNIVERSALITY SUPPORTED" — was repudiated in prose in
`research/RESEARCH-LOG.md` on the same day it was written, in language explicitly calling it "a
motivated false positive", and the structured record was never corrected and never entered into
ERRATA at all.**

That is the single most important finding: the project's retraction machinery is real but is applied
by hand and has already failed twice inside this 25-record window.

---

## 1. Record inventory for the range

Files present (21 records; `research/data/simulations/`):

`SIM-2026-031.json`, `-032.json`, `-032b.json`, `-033.json`, `-033b.json`, `-034.json`, `-035.json`,
`-036.json`, `-037.json`, `-039.json`, `-040.json`, `-042.json`, `-044.json`, `-045.json`,
`-045-chi6.json`, `-050.json`, `-051.json`, `-052.json`, `-053.json`, `-054.json`, `-055.json`.

**ID slots consumed with no structured record (7):** SIM-038, 041, 043, 046, 047, 048, 049.
Driver scripts for every one of them exist on disk —
`research/data/simulations/sim038_dmrg_seeded_mera.py`, `sim041_scaleinv_mera_spectrum.py`,
`sim043_chi6_universality.py`, `sim046_finite_si_mera_seed.py`, `sim047_eigentower_ramp.py`,
`sim048_riemannian_chi6.py`, `sim049_spectral_objective.py` — and their outcomes are narrated only in
`research/RESEARCH-LOG.md` (e.g. lines 657-672 for the sim046-049 ladder). Seven runs, zero
machine-readable records. `ERRATA.md` D1 documents only the SIM-004/007/011 gaps; this seven-slot gap
is undocumented.

---

## 2. Per-record audit

Legend for **Level** = RESEARCH-DIRECTOR §5. **CFN** = counterfactual novelty (§6):
`near-zero` / `moderate` / `high`.

---

### SIM-2026-031 — Synge-map distance vs force-blindness

| field | value |
|---|---|
| id / date | `SIM-2026-031`, `"date": "2026-06-08"` |
| hypothesis | HYP-2026-026 |
| title | Pre-registered test of the Synge map `d = sqrt(-2 eps^2 ln|C|)` on synthetic CFT, exact 16q TFIM, and a SIM-011 pathological control |
| measurement | `results.tiers.exact_16q.kappa_loglog_chord = 0.24289`, `kappa_loglog_r = 0.19553`; monotonicity flags |
| pipeline | local CPU exact statevector + scipy eigsh; `circuit.script_path = research/data/simulations/sim031_synge_force_blindness.py` (exists) |
| verdict | `results.verdict`: "SUPPORTED (monotone distance; kappa~0.25 not ~4: distance is force-blind)" |
| claim supported | The Synge geodesic-distance reconstruction carries the correlator exponent 2*Delta_sigma = 0.25, not the force exponent alpha = 4 |

**Level 2 / borderline 3 (a genuine small no-go, §16).** **CFN: near-zero.** `d` is defined as a
strictly monotone function of `ln|C|`, so `kappa = -dln|C|/dln r` is *by construction* the correlator
exponent 2*Delta_sigma = 0.25 for `C ~ r^{-1/4}`. Only implementation failure could have produced any
other number. The "monotone_increasing: true" half of the verdict has literally zero counterfactual
content: `d` increases whenever `|C|` decreases.

**Verdict proportionality: OVERSTATED label, correct substance.** The word "SUPPORTED" attaches to a
hypothesis (HYP-026) whose "geometric" half is an automatic consequence of the map's definition. The
force-blindness half is the real (and useful) content and is stated honestly.

**Reproducibility — present:** script_path, hardware_target, `wall_seconds: 1.14376…`, full raw
`C`/`d_synge` arrays for all three tiers, an explicit `analytic_note` giving the closed form
`d(r) = eps*sqrt(0.5*ln r)`.
**Absent:** code revision/commit, dependency versions, platform, RNG seed, output checksum.

**DEFECT (minor, unrecorded):** the file is **invalid strict JSON** — `results.tiers.synthetic_cft.fits_d_vs_r.power`
contains bare `NaN` tokens (`"exponent": NaN, "prefactor": NaN, "r2": NaN`). This is the same defect
class as `ERRATA.md` D2 ("worldline_mc_results.json contains a literal NaN (invalid strict JSON)") but
SIM-031 is **not** listed in D2 or anywhere in ERRATA. Verified: `json.loads(..., parse_constant=raise)`
fails on this file and on no other file in the range.

**Note on the control:** `pathological_control_sim011` returns `monotone_increasing: false`, i.e. the
control behaves differently from the signal. That is a real matched control (§19) and it is used
correctly.

---

### SIM-2026-032 — TCI stage-1 exact diagonalization (O'Brien–Fendley chain)

| field | value |
|---|---|
| id / date | `SIM-2026-032`, `2026-06-08` |
| measurement | Ising end `c_fit = 0.50176`, `alpha = 3.97482 ± 0.14510`; TCI end `c_fit = 0.72630`, `alpha = 1.33105 ± 0.09093` |
| pipeline | 16q exact statevector, `sim032_tci_force_stage1.py` (exists) |
| verdict | "INCONCLUSIVE: TCI alpha=1.33 matches neither 4.0 nor 0.4 cleanly" |

**Level 1.** **CFN: moderate** — before the run, alpha at TCI could plausibly have been 4 (universal)
or ~0.4 (primary-tracking); it came out at neither, which is genuinely informative about the *method*.
**Verdict proportionate — good.** The record does not spin an off-target number into either branch.

Notable design change recorded honestly: `description` documents the amendment from ANNNI to the
O'Brien–Fendley chain ("vanilla ANNNI has no documented TCI coordinates"), and
`research/data/hypotheses/HYP-2026-027.json` field `result_note_2026_06_08_sim032` repeats it. This
contradicts nothing but is worth flagging because HYP-027's own
`feasibility_mandatory_gates[0]` still reads "Commit to the ANNNI … route, NOT spin-1 Blume-Capel" —
a gate that the executed work superseded, left unedited in the hypothesis record.

Reproducibility: script, N, couplings, per-dr `F` table, `wall_s` per branch. Absent: commit, versions,
seed, checksum.

---

### SIM-2026-032b — max-creation operator calibration

| field | value |
|---|---|
| id / date | `SIM-2026-032b`, `2026-06-08` |
| measurement | `ising_control.alpha = 2.91897 ± 0.02789`; `tci_point.alpha = 0.55456 ± 0.20455` |
| verdict | "METHOD_NOT_VALIDATED: calibrated-Ising alpha=2.92 outside (3.2, 4.8) … TCI number not interpretable this way" |

**Level 1 (negative).** **CFN: moderate.** **Verdict proportionate — exemplary.** The TCI value
(0.5546) sits near the primary-tracking prediction 0.4 and the record *refuses to use it* because the
control failed. This is the correct discipline and should be cited as a positive precedent.

**Schema defect:** id `SIM-2026-032b` violates `templates/simulation-result.json` `id` pattern
`^SIM-\d{4}-\d{3,}$` (ERRATA D3 class; D3 records the aggregate but not this instance).

---

### SIM-2026-033 — symmetry-resolved operator-basis scan

| field | value |
|---|---|
| id / date | `SIM-2026-033`, `2026-06-08` |
| measurement | 7-operator scan at each point; `selected_operator = X+mix`, Ising `alpha = 3.97184 ± 0.14547`, TCI `alpha = 1.33070 ± 0.09095` |
| verdict | "INCONCLUSIVE: validated op 'X+mix' (Ising 3.97) gives TCI alpha=1.33" |

**Level 1.** **CFN: moderate.** **Verdict proportionate.**

**Methodological risk documented but not flagged as such:** the operator is *selected* by which one
reproduces the already-published Ising alpha ≈ 3.97 (`results.selected_operator`, `gate_pass: true`),
then applied at TCI. That is a legitimate validation gate, but it is also a selection on the target
statistic — of the 7 operators scanned, the Ising alphas span 3.910 to 4.931, so "the pipeline
reproduces 3.97" is partly a choice, not only a check. The record does not say this. Under §7 this is
a **structurally dependent** comparison: side A (Ising) and side B (TCI) share the operator whose
definition was fixed by side A.

---

### SIM-2026-033b — Gram–Schmidt light-primary projection

| field | value |
|---|---|
| id / date | `SIM-2026-033b`, `2026-06-08` |
| measurement | Ising K=0..2 alpha ≈ 3.9100; TCI K=0..3 alpha ∈ {1.3235, 1.3235, 1.6271, 1.6271} |
| verdict | "STAGE_2_REQUIRED … This is the honest exact-diag ceiling, not a refutation." |

**Level 1 (negative).** **CFN: moderate.** **Verdict proportionate — good.** Explicitly declines to
call the failure a refutation of HYP-027 and names the reason (dense c=7/10 spectrum at N=16).
Schema: id-regex violation (as 032b).

---

### SIM-2026-034 — Koo–Saleur energy-density channel

| field | value |
|---|---|
| id / date | `SIM-2026-034`, `2026-06-16` |
| measurement | Ising `alpha = 1.32646 ± 0.90684` (n_fit 5); TCI `alpha = 4.41250 ± 0.23170`; `T_found: false` at both |
| verdict | "VALIDATION_FAILED: Ising stress-tensor-channel alpha=1.3265 outside (3.4, 4.6)" |

**Level 1 (negative).** **CFN: moderate.** **Verdict proportionate — and notably strong discipline:**
the TCI value 4.4125 ± 0.2317 is *inside* the alpha≈4 window and would have been a headline had it been
reported; the record discards it because the Ising control failed. `T_found: false` and
`Delta_T_check: null` are recorded rather than hidden. This is the §19 standard being met.

Reproducibility: script, N=14, low_spectrum + low_momenta arrays, `wall_seconds`. Absent: commit,
versions, seed, checksum.

---

### SIM-2026-035 — momentum-resolved stress-tensor identification

| field | value |
|---|---|
| id / date | `SIM-2026-035`, `2026-06-16` |
| measurement | `ising.Delta_T_check = 1.9999999999999998`, `tci.Delta_T_check = 2.0` (both `T_found: true`); Ising `alpha = 1.71759 ± 0.63250`, TCI `alpha = 1.25483 ± 0.37848` |
| verdict | "VALIDATION_FAILED: even the momentum-2 (stress-tensor) packet gives Ising alpha=1.7176 outside (3.4, 4.6) at N=14 … honest hand-off" |

**Level 1 for the Delta_T number; Level 2 for the obstruction finding.**
**CFN for `Delta_T_check ≈ 2.0000`: near-zero.** Delta_T = 2 is a Virasoro identity in every 2D CFT;
recovering 2.0000 tests only that the momentum block-diagonalization is coded correctly.
**CFN for the localization obstruction: moderate-to-high** and this is the real content —
`HYP-2026-027.json` field `result_note_2026_06_16_FINAL` states it precisely: "clean Delta_T=2 channel
AND spatial localization are mutually exclusive at finite N", and further concedes that "The published
alpha~4 worked only because its specific boundary operator (0.635 X-pair) is tuned to suppress that
contamination at the Ising point — a tuning that does NOT transfer to TCI."

**That concession is material to the manuscript and is not surfaced in the paper.** `research/paper-draft-scipost.tex`
line 346 and `research/submission-package/prd/paper-prd.tex` line 603 present the 24q/16q alpha ≈ 3.92/3.97
as measurements of stress-tensor exchange without noting that the boundary operator was tuned at the
Ising point and that the same tuning demonstrably fails to transfer. Flagged for the manuscript-audit
agent; I do not assert it invalidates the numbers, only that a §24-style referee will ask.

**Verdict proportionate — good.**

---

### SIM-2026-036 — chi=3 TCI MERA (THE RETRACTED RECORD)

| field | value |
|---|---|
| id / date | `SIM-2026-036`, `2026-06-16` |
| measurement | `rel_err_pct = 0.34080`, `gs_overlap = 0.92563`, `S_half_mera = 0.00021867` vs `S_half_exact = 0.17948`, `S_ratio = 0.0012183` |
| current verdict | `results.verdict` = "CORRECTED 2026-06-16 (ERRATA D5) … the original 'chi=3 INSUFFICIENT, escalate chi>=4' verdict MISDIAGNOSED an optimizer collapse as a capacity ceiling …" |
| retracted verdict | preserved verbatim in `results.verdict_SUPERSEDED_2026_06_16` |
| status | `results.status = "OPTIMIZER_COLLAPSE_RESEED_NEEDED"` |

**Retraction handling in this file: CORRECT and exemplary.** The old verdict is preserved, not deleted
(§32), under an explicitly dated `_SUPERSEDED_` key, adjacent to the correction. Git confirms the
two-commit history: `82a8630` ("chi=3 MERA insufficient for tricritical point") then `da1d126`
("CORRECTION (ERRATA D5) …").

**Residual weakness:** `notes` still reads "Optimization rounds plateaued 0.417->0.416->0.416%
(chi=3 floor). … Scan-10 papers 115/112 predicted this boundary/symmetry-sector ceiling." — the phrase
"chi=3 floor" and the PAPER-115/112 prediction credit are exactly what ERRATA D5 retracts
(`ERRATA.md` lines 100-102: "The PAPER-115/112 boundary/channel-mixing mechanism was never actually
tested — the energy run died in a product minimum first"). The `notes` field was not updated.
**DEFECT (minor).**

---

### RETRACTION-PROPAGATION AUDIT (ERRATA D5)

`ERRATA.md` lines 92-94 name four affected records: **(a)** `SIM-2026-036.json` verdict, **(b)** the
matching lines in `HYP-2026-027.json`, **(c)** the 2026-06-16 digest, **(d)** RESEARCH-LOG, **(e)** MEMORY.md.

| target | corrected? | evidence |
|---|---|---|
| (a) `research/data/simulations/SIM-2026-036.json` | **YES** | `results.verdict` carries "CORRECTED 2026-06-16 (ERRATA D5)"; old text preserved in `verdict_SUPERSEDED_2026_06_16`. Except `notes` (see above). |
| (b) `research/data/hypotheses/HYP-2026-027.json` | **PARTIAL** | The stale note `result_note_2026_06_16_stage2a` still reads "chi=3 INSUFFICIENT … ESCALATE to chi>=4 … This QUANTITATIVELY confirms the scan-10 prediction" with **no inline retraction marker**. A separate adjacent key `result_note_2026_06_16_stage2a_CORRECTION` carries the correction. Acceptable under §32 (history preserved) but a reader or agent quoting `…_stage2a` in isolation gets the retracted claim. |
| (c) `research/digests/2026-06-16-team-scan.md` | **NO — MAJOR DEFECT** | Line 9 still asserts "**HYP-027 stage-2a RESULT (SIM-2026-036): chi=3 MERA is INSUFFICIENT for the tricritical point — a clean, quantitative negative on sufficiency (not on the physics).** Escalate to chi≥4." Lines 33-35 elaborate: "**Verdict: chi=3 cannot represent the tricritical state. ESCALATE to chi≥4.** This *quantitatively confirms* the scan's independent literature prediction (PAPER-115 … + PAPER-112 …)". `git log -- research/digests/2026-06-16-team-scan.md` returns exactly one commit, `82a8630` — the pre-retraction commit. The digest has never been touched since. This is the *one* document in the set formatted as a distributable report, and it is the one that still carries the retracted conclusion **and** the false literature-confirmation credit. |
| (d) `research/RESEARCH-LOG.md` | **YES** | Lines 208-210 ("Root cause (all of SIM-036/037/038): finite-difference gradients on 1246 angles"), 222 ("CONFIRMS the SIM-036 'chi=3 insufficient' verdict was an optimizer artifact (ERRATA D5 vindicated)"), 235-239. |
| (e) MEMORY.md | **YES (indirectly)** | The memory index topic line for HYP-027 cites SIM-051/052 and the OF-blocking topic file, not SIM-036; no stale "chi=3 insufficient" claim found. |

---

### SIM-2026-037 — cheap-lever escape attempt

| field | value |
|---|---|
| id / date | `SIM-2026-037`, `2026-06-17` |
| measurement | best trial `rel_err_pct 0.4445`, `overlap 0.9096`, `S_half 0.0001`, `S_ratio 0.0007`, `gate_pass: false` |
| verdict | "CHEAP seeding … does NOT escape the chi=3 product-state collapse … a TRUE DMRG/MPS seed is required" |

**Level 1 (negative), Level 2 for the diagnosis.** **CFN: moderate.** **Verdict proportionate.**

**Reproducibility — a documented but real integrity issue, disclosed by the record itself:**
`results.note_on_completeness` states "Run was killed at ~4h50m … The remaining trials were not allowed
to finish … **The full 6-trial JSON the script would have written was therefore authored by hand from
the evaluated checkpoint.**" A hand-authored record standing in for machine output is a §21 deviation.
The disclosure is the right behaviour; the record should nonetheless be marked as partially synthetic
in any provenance ledger. `wall_seconds_partial: 17400` (non-standard key) instead of `wall_seconds`.

---

### SIM-2026-039 — autograd chi=3 MERA (the D5 resolution)

| field | value |
|---|---|
| id / date | `SIM-2026-039`, `2026-06-17` |
| measurement | Ising control `rel_err_pct 0.18319`, `overlap 0.99399`, `S_ratio 1.03971`, `gate_pass: true`; TCI `rel_err_pct 0.08795`, `overlap 0.99427`, `S_half 0.13364` vs exact `0.17948`, `S_ratio 0.74456`, `gate_pass: false` |
| verdict | Two findings: D5 vindicated (S 0.0002 → 0.1336, ~670x) and chi=3 is energy-faithful / entanglement-partial |

**Level 2 — the strongest methodological record in the range.** Two independent bugs were found and
fixed: (i) finite-difference gradients on 1246 angles replaced by exact autograd (Cayley-transform
unitaries + a sparse-H matvec primitive with VJP `g -> H^T g`, "all verified vs finite-diff to ~1e-10"),
(ii) the objective was minimizing **raw** energy on a state only ~60% in the Z2-even sector; switching
to the Z2-**projected** energy dropped the Ising control from rel 0.60% to 0.18%.

**CFN: moderate-to-high** for the optimizer question — before the run it was genuinely open whether the
collapse was capacity or landscape.

**Verdict proportionate — and self-correcting:** the record notes "the auto-generated 'collapses'
wording is CORRECTED — this is NOT a collapse", i.e. the author overrode the script's own language.
It also explicitly distinguishes the new chi=4 justification from the retracted one: "a DIFFERENT,
stronger basis than the retracted SIM-036 chi-4 call".

**Reproducibility — present:** script_path, per-branch `niter` (800), `wall_s`, both theta checkpoints
(`theta_autograd_SIM2026039_ISING_CONTROL.npy`, `…_TCI.npy` — both verified on disk), exact E values.
**Absent:** the RNG seeds are **hard-coded in the script but not stated in the record**
(`sim039_autograd_mera.py:168` `rng = np.random.default_rng(42)`, `:186` `rng_kick = np.random.default_rng(2026)`).
Also absent: commit hash, autograd/numpy/scipy versions, platform.

---

### SIM-2026-040 — chi=4 TCI MERA (closure)

| field | value |
|---|---|
| id / date | `SIM-2026-040`, `2026-06-17` |
| measurement | Ising `rel 0.0016440%`, `ov 0.99994`, `S_ratio 0.99848`; TCI `rel 0.0061128%`, `ov 0.99978`, `S_half 0.17598` vs `0.17948`, `S_ratio 0.98048`; both `gate_pass: true` |
| verdict | "chi=4 SUFFICIENT at the TCI point … NEXT: stress-tensor force read-out … -> the alpha-universality answer" |

**Level 1/2 (representability, not physics).** **CFN: moderate.** **Verdict proportionate**, with one
important honest caveat *outside* the record: `HYP-2026-027.json` field
`result_note_2026_06_17_stage2e_chi4` adds "NOTE (assessed against SIM-035): a faithful state alone
does NOT dissolve the finite-N localization obstruction … the clean alpha read-out is a SEPARATE build".
`ERRATA.md` lines 138-140 repeat it. The SIM-040 JSON's own `verdict` does **not** carry that caveat and
reads as if the force read-out is the immediate next step. **DEFECT (minor):** the caveat lives in the
hypothesis record and ERRATA but not in the simulation record it qualifies.

Same reproducibility profile as SIM-039 (seeds 42/2026 hard-coded in `sim040_chi4_tci_mera.py:162,170`,
not stated in the record; checkpoints present).

---

### SIM-2026-042 — scale-invariant spectrum (THE UNDOCUMENTED OVER-CLAIM)

| field | value |
|---|---|
| id / date | `SIM-2026-042`, `2026-06-18` |
| measurement | Ising `dims[1] = 0.10104…` (CFT 0.125); TCI `dims = [0, 0.473, 0.761, 0.934, 1.242, 1.365, 1.465, 2.110, 2.140, 2.233, …]`, `Delta_near_2 = [2.1102, 2.1396, 2.2332]` |
| verdict (unchanged, on disk today) | "Superoperator+optimizer VALIDATED (Ising Delta_2=0.1010~0.125). **TCI Delta_T~2 FOUND [2.110…, 2.1396…, 2.2332…]: universal stress tensor, alpha=2*Delta_T=4 at c=7/10. UNIVERSALITY SUPPORTED.**" |
| status field | `"ISING_PASS_TCI_MEASURED"` |

**CRITICAL DEFECT — an unretracted, un-erratum'd over-claim that directly asserts the project's
headline conclusion off a state the project itself established was at the wrong fixed point.**

Evidence that the claim is repudiated, in the project's own words, `research/RESEARCH-LOG.md`
lines 395-413 (entry dated 2026-06-18, i.e. the same day):

> "TCI run: pipeline validated but TCI optimization did NOT reach the c=7/10 fixed point … Resulting
> TCI spectrum: [0, 0.473, 0.761, 0.934, 1.242, 1.365, 1.465, 2.110, 2.140, 2.233, …] vs TCI CFT
> [0, 0.075(sigma), 0.2(eps), 0.875, 1.2, …, 2.0(T)]. HONEST VERDICT: this does NOT match the c=7/10
> CFT — the lowest non-zero dim is 0.473, MISSING the two lightest primaries (0.075, 0.2) entirely.
> This is a QUALITATIVE failure (wrong fixed point), not a precision issue. **The cluster near 2.1
> ([2.11,2.14,2.23]) CANNOT be claimed as the stress tensor Delta_T=2** … **Reading "Delta_T~2 found"
> off this would be a motivated false positive — explicitly NOT claimed.**"

The JSON record contains the exact phrase the log forbids. Corroboration that the underlying state was
non-critical: `SIM-2026-044.json` `ising_c = 0.09714487655978005`, `gate_pass: false`, with
`notes` = "Fixes the non-criticality (c=0.10) of the fixed-first-layer construction" — i.e. the SIM-042
construction reads c ≈ 0.10 against Ising's exact c = 0.5. `RESEARCH-LOG.md` lines 490-501 confirm
("it reads c=0.10 … the state is NOT genuinely critical (c=0.10, not 0.5)").

`git log --oneline -- research/data/simulations/SIM-2026-042.json` returns exactly one commit,
`55fcba6`. The record has never been amended. `ERRATA.md` ends at D5; there is **no** entry for SIM-042.

Additional problems inside the same record:
- Ising `dims[1] = 0.1010` vs CFT 0.125 is **19% off** and is labelled "VALIDATED … 0.1010~0.125".
  `RESEARCH-LOG.md` lines 388-391 is more careful ("Delta_sigma 0.101 is slightly worse than chi=2's
  0.106 … the spectrum is correct in structure but not high-precision"). The record's "~" hides a 19%
  discrepancy behind a tilde.
- The record has **no conformal-spin resolution** and no c-gate; "Delta_T" is asserted from proximity to
  2 alone. Values 2.110/2.140/2.233 are 5.5%/7.0%/11.6% from 2.0.
- `gateB: true` is recorded for a control that the log describes as only "qualitatively PASS".

**Level: none earned. CFN: near-zero (Delta_T=2 is a theorem) — and the measurement did not even reach
a CFT.** **Verdict grossly disproportionate to evidence.**

**Required remediation:** an ERRATA entry (D6) plus a `verdict_SUPERSEDED_2026_06_18` restructuring of
`SIM-2026-042.json` mirroring the SIM-036 pattern.

---

### SIM-2026-044 — co-optimized transitional-layer MERA

| field | value |
|---|---|
| id / date | `SIM-2026-044`, `2026-06-18` |
| measurement | `ising_c = 0.09714487655978005`, `gate_pass: false` |
| verdict | none — no `verdict` field |

**Level: none (negative control result).** **CFN: near-zero.** The record is a 352-byte stub: no
`type` (schema-required), no `results` object, no script reference, no `wall_seconds`, no verdict text.
Its scientific value is entirely as the disconfirming evidence against SIM-042 — and it is not
cross-linked to SIM-042 in either direction. **DEFECT (major, structural):** the record that refutes
SIM-042 does not reference SIM-042, and SIM-042 does not reference it.

---

### SIM-2026-045 / SIM-2026-045-chi6 — stable EV scale-invariant loop

| field | value |
|---|---|
| id / date | `SIM-2026-045`, `2026-06-19`; the `-chi6` file has **no date** |
| measurement (`-045.json`) | `ising.c = 0.74559`, `s1 = 0.70293`, `ising_gate_pass: false`, 80-entry `c_history` |
| measurement (`-045-chi6.json`) | `ising.c = 0.33058`, `s1 = 0.31847`, 210-entry `c_history`, `"cold": true` |
| verdict (`-045.json`) | "Ising control FAILED at chi=6 (c=0.7456, sig=0.0372 …). chi insufficient OR loop bug; do NOT trust TCI. Escalate chi." |

**Level: none.** **CFN: near-zero.** **Verdict proportionate** ("do NOT trust TCI" is the right call).

**DEFECTS:**
1. **ID collision.** Both `SIM-2026-045.json` and `SIM-2026-045-chi6.json` carry `"id": "SIM-2026-045"`.
   ERRATA D1 documents ID collisions for SIM-007/011 only; this one is undocumented.
2. **Self-documented record overwrite.** `SIM-2026-045.json` field `chi6_wrong_basin_note`: "This file
   **was overwritten by a chi=6 run**. c=0.746, sigma=0.037 = WRONG BASIN (worse than chi=4
   sigma=0.057). The VALIDATED chi=4 result (c=0.464, eps=1.038 exact, sigma=0.057, Delta_T=1.97/2.04)
   is in RESEARCH-LOG + uw_ISING_stable_chi4.npz (commit b31c01b)." A result described as "VALIDATED"
   therefore has **no structured record at all** — only prose and a binary. Commit `b31c01b` exists.
3. **The record contradicts the log about that same chi=4 state.** The note claims
   "Delta_T=1.97/2.04"; `RESEARCH-LOG.md` line 636 says of the identical run "**Delta_T=2 is not in the
   leading chi=4 dims**". One of the two is wrong; neither is reconcilable from the surviving artifacts.
4. Calling sigma = 0.057 (54% below the exact 0.125) part of a "VALIDATED" result is not proportionate;
   the log at line 635 is more careful ("as expected, Delta_sigma stays ~0.06-0.07 at chi=4").
5. `-chi6.json` is missing schema-required `description`, `type`, `date`, and has no
   `hypothesis_id` or verdict.

**Systemic observation (this is the important one):** across SIM-042 (2026-06-18), the
`RESEARCH-LOG.md` line 618 remark on an unconverged chi=6 run ("it ALREADY shows the universal stress
tensor Delta_T~2 emerging — the central HYP-027 signal"), and SIM-045's "Delta_T=1.97/2.04" note, the
project repeatedly reads Delta_T ≈ 2 off states whose light primaries are demonstrably wrong. The log
itself named the failure mode ("a motivated false positive"). Because Delta_T = 2 is a Virasoro
identity, *any* near-2 eigenvalue in a crowded superoperator spectrum can be mistaken for T. **A
conformal-spin (or Z2-sector) requirement should be a hard gate on any future Delta_T claim**; SIM-035
already demonstrates that spin resolution is implementable (`results.ising.low_spins`).

---

### SIM-2026-050 — MERAKit chi=6 Ising control

| field | value |
|---|---|
| id / date | `SIM-2026-050`, `2026-06-19` |
| measurement | seed1 `E_err 2.29e-6`, `Delta_sigma 0.12515`, `Delta_eps 1.0175`, `Delta_T 1.9980`; seed2 `2.44e-6 / 0.12534 / 1.0176 / 1.9925` |
| pipeline | MERAKit.jl (Hauru, arXiv:2007.03638) ternary MERA, Riemannian LBFGS, direct-init bond 6, Z2 sector-3, block_size 2, Julia 1.8.5 |
| verdict | "chi=6 Ising CONTROL PASSES … VALIDATES the chi=6 machinery" |

**Level 1 — pure validation, correctly labelled.** **CFN: near-zero** (Delta_sigma = 1/8,
Delta_eps = 1, Delta_T = 2 are exact Ising CFT values, known since BPZ 1984).
**Verdict proportionate** — the record says "VALIDATES the machinery", not "measures".

**Honest disclosure present:** `notes` flags "Delta_eps slightly high (1.018) is the known small-chi
residual" and that `expand_bonddim` throws `LAPACKException(15)`.

**Reproducibility — the important gap:** two seeds are reported as `seed1`/`seed2` but **no RNG seed
values, no driver filename, and no commit** are given. `method` names the package and Julia version
only. Contrast SIM-052, which does name a commit. Missing schema-required `description`.

---

### SIM-2026-051 — MERAKit chi=6 at the TCI point

| field | value |
|---|---|
| id / date | `SIM-2026-051`, `2026-06-22` |
| measurement | 8 seeds; best-spectrum seed 5: `Delta_sigma 0.1538`, `Delta_T 2.0065`, `alpha 4.013`. Blocking validated to `1.1e-16` by exact diagonalization on 6- and 8-site PBC rings |
| verdict | "HYP-027 SUPPORTED. … alpha = 2*Delta_T = 4.01 … **This is exactly the CFT prediction: Delta_T=2 in every unitary 2D CFT** … The numerics confirm the symmetry argument." |

**Level 1 (validation), correctly self-described.** The verdict text is one of the few places in the
repository that states the counterfactual-novelty problem out loud. Credit where due.

**CFN: near-zero for Delta_T / alpha.** Delta_T = 2 is fixed by conformal symmetry; the only possible
outcomes were "the MERA reached a CFT fixed point" or "it didn't".
**CFN: moderate for Delta_sigma / Delta_eps** — those test the class assignment, though O'Brien–Fendley
(2018) already established that lam3/lamI = 0.856 is the TCI point, so this is reproduction of
published literature, not new information.

**DEFECT (major, arithmetic):** `delta_T_statistics.all_8_seeds_mean` is recorded as **1.9913**. The
mean of the eight `results_all_seeds.*.Delta_T` values actually listed in the same file
(1.9792, 1.9876, 2.0814, 1.9219, 2.0065, 2.1889, 1.9956, 1.9691) is **2.0163** (I recomputed it; the
median is 1.9916, also not 1.9913). The `verdict` field then quotes the wrong figure — "1.99 mean
across 8 seeds". Correct mean alpha across the 8 seeds is **4.0325**, not 3.983. Magnitude is small
(0.8%), but a headline statistic in a verdict that is not reproducible from the record's own data is a
§21/§20 failure and would be fatal in referee review.

**DEFECT (moderate, uncertainty):** no uncertainty is attached to alpha anywhere in the record. The
8-seed `all_8_seeds_range` is [1.9219, 2.1889] — a ±5% spread on Delta_T — yet the selected value is
quoted as `alpha 4.013` (4 significant figures). §20 requires optimization/basin-selection uncertainty
to be separated and reported; it is not.

**DEFECT (moderate, selection):** the basin is chosen by `selection: "lowest Delta_sigma (cleanest
critical basin)"` — i.e. selected using one part of the measured spectrum, after which a different part
of that same spectrum is reported as agreement. The record partially defends this
(`delta_T_statistics.note`: "Delta_T clusters at ~2.0 across ALL basins regardless of basin quality"),
which is a legitimate mitigation, but the selection is not treated as a source of systematic error.

**OVERSTATEMENT (minor):** `control_lam3_0.note` says the lam3=0 control "reproduces critical Ising
(matches SIM-050)". Its `Delta_sigma` is **0.1402**, vs SIM-050's 0.12515 and CFT 0.125 — a 12%
deviation, roughly 12x SIM-050's. "Matches SIM-050" is not accurate at the stated precision.

**Reproducibility — best-in-range for the blocking validation:** the exact-diagonalization pre-gate is
fully specified (`blocking_validation.exact_diag_pregate` names
`research/tools/MERAKit.jl/qw_of_pregate.py` + `qw_of_pregate_compare.py`; both exist) and reports
`max|H_orig - H_recon| = 0` / `1.1e-16`. Driver named in `notes`
(`research/tools/MERAKit.jl/qw_tci_measure.jl`; tracked mirror `research/tools/merakit-setup/qw_tci_measure.jl`
verified on disk). **Absent:** commit hash, RNG seed values, iteration counts, wall time, checksum;
missing schema-required `description`.

---

### SIM-2026-052 — MERAKit chi=8 at the TCI point (the paper's TCI datum)

| field | value |
|---|---|
| id / date | `SIM-2026-052`, `2026-06-22` |
| measurement | 6 seeds; best seed 1: `Delta_sigma 0.0917`, `Delta_eps 0.2038`, `Delta_T 1.9994`, `alpha 3.9987`; `full_low_tower` 16 entries |
| verdict | "Sharpens and confirms SIM-051 … HYP-027 SUPPORTED with strengthened evidence" |

**Level 1 for Delta_T; Level 1 (literature reproduction) for the class identification.**
**CFN: near-zero for alpha; moderate for `Delta_eps = 0.2038`,** which is the genuinely discriminating
datum (Ising would give 1.0) and is correctly identified as such by both the record
(`notes`: "The Delta_eps=0.204 resolution is the decisive new datum") and the manuscript
(`research/submission-package/prd/paper-prd.tex` line 450).

**DEFECT (moderate, uncorrected errata propagation):** `delta_T_statistics.note` claims "**ALL 6 seeds
give alpha within 1.5% of 4.0**". Seed 4 has `alpha 4.0602`, which is **1.505%** from 4.0 — the claim is
false at its own stated precision. `ERRATA.md` line 16 records that this was caught and fixed **in the
manuscript** ("'six seeds within 1.5%' → 2% (seed 4 is 1.51% per SIM-052)"), and both
`research/paper-draft-scipost.tex` line 474 and `research/submission-package/prd/paper-prd.tex` line 450
now correctly read "within 2%". **The underlying data record was never corrected.** This is the errata
process running one-directionally: manuscript fixed, source record left carrying the wrong number.

**Verified-correct statistics (I recomputed):** `all_6_seeds_mean = 2.0120` matches the listed values
exactly; `all_6_seeds_range = [1.9994, 2.0301]` correct; `comparison_to_chi6_SIM051` percentages
(0.1538 → 105% off 0.075; 0.0917 → 22% off) correct.

**DEFECT (moderate, uncertainty):** as with SIM-051, no uncertainty on alpha. The manuscript quotes
`Delta_T = 1.999` → `alpha = 4.00` from the **best of 6 seeds** to four significant figures while the
ensemble spans 1.9994–2.0301. §20: basin-selection systematic is not separated from statistical error
anywhere in the chain from record to manuscript.

**Reproducibility — best in the range:** `notes` gives the driver *and a commit*: "Driver
research/tools/MERAKit.jl/qw_tci_chi8.jl (committed merakit-setup/qw_tci_chi8.jl **51f2c0c**)". Commit
verified to exist (`git cat-file -t 51f2c0c` → `commit`); the tracked mirror exists on disk. Also gives
per-seed runtime ("~45 min at chi=8"), iteration count (2500), bond dim, block size, and the dense
`ComplexSpace` choice. **Absent:** RNG seed values, Julia package manifest hash, output checksums;
missing schema-required `description`.

---

### SIM-2026-053 — Yang–Lee via uniform i·gamma field

| field | value |
|---|---|
| id / date | `SIM-2026-053`, `2026-06-26` |
| measurement | `nonunitary_alpha = {12: 4.0969, 14: 4.0348, 16: 4.0004}`; `control_alpha_N16 = 3.95076`; `gamma_c_by_N = {12: 0.00744, 14: 0.00557, 16: 0.00433}` |
| script verdict | `automated_script_verdict`: "REFUTED (stronger universality): non-unitary alpha=4.000 INSIDE [3.2,4.8] and stable -> alpha=4 is GENERIC, survives loss of unitarity" |
| final verdict | `verdict`: "**INCONCLUSIVE**" — the automated verdict **overridden** |

**Level 2 (a mapped structural obstruction).** **CFN: high in intent, near-zero in delivery** — and the
record says so itself. `verdict_rationale`: "the test never got meaningfully OFF the unitary point …
we sat at kappa=0.9*kappa_c … a ~0.1% non-Hermitian perturbation … The resulting force profile is
nearly identical to the unitary one (V_dual differ by <2% at every dr), so alpha~4 here reflects
proximity to the unitary point, NOT survival of alpha=4 at a genuinely non-unitary fixed point."

**Verdict proportionality: EXEMPLARY — the single best epistemic act in this range.** An automated
pipeline produced a publishable-sounding positive ("alpha=4 is GENERIC") and the human/agent overrode
it downward on a structural argument. §12 killer-test discipline and §19 control discipline are both
satisfied: the gate ledger is explicit, including
`G5_PT_unbroken: "PASS but VACUOUS (only achievable by sitting negligibly far from the unitary point)"`.

**Also records a prior error transparently:** `estimator_correction_note` — the first run used the
superseded connected-ZZ observable and failed the control at alpha ≈ 0.54; switching to the validated
energy-difference estimator `V = E_dual - E0 - dE_anchor - dE_probe` fixed it to 3.95. Recording a
failed first attempt in the final artifact is exactly §32 behaviour.

**DEFECT (minor, factual slip inside the rationale):** `verdict_rationale` says "Im(E0)~2e-2 vs
E0~-20". The record's own `runs.nonunitary_N16.E0_im` is `-6.148e-15`; the 2e-2 figure is
`V_imag_max = 0.020736`. The magnitude of the argument is unaffected, but the quantity is misnamed.

**DEFECT (minor, terminology drift):** the top-level field is `gamma_c_by_N` while the rationale text
uses `kappa_c` for the same quantity; the rationale additionally cites an N=10 value (0.0105) that
appears nowhere in the record.

**Reproducibility — weak:** **no script path anywhere in the record** (the driver is
`research/data/simulations/hyp028b_yanglee_force.py`, which exists but is never referenced). No
`type` field (schema-required), no `description` (schema-required), no dependency versions, no seeds
(deterministic ED, so low impact), `runtime_s: 5.838` present.

---

### SIM-2026-054 — HYP-029 fault-tolerant resource estimate

| field | value |
|---|---|
| id / date | `SIM-2026-054`, `2026-06-26`, `type: "resource-estimation"` |
| measurement | `estimate.physical_qubits`: high-rate STAR ~3,700–4,550; transversal ~9,000–11,000; `logical_qubits ~20`; MERA-route logical volume ~0.03x the 8x8 datapoint |
| verdict | "SUPPORTED (conditional; confidence LOW)" |

**Level: not a measurement — a costing exercise.** **CFN: moderate** (the three pre-registered ceilings
could have been breached). **Verdict proportionate — good.** The `verdict_detail` separates the robust
part from the fragile part explicitly: "The PHYSICAL-QUBIT figure (~4.5k) is the ROBUST part …
independent of the unknown T-count. CONDITIONALITY (kept LOW, not raised to medium): (1) the
LOGICAL-VOLUME ratio rests on an **INFERRED** 8x8 reference volume (~87,600) because PAPER-120 does NOT
publish the T-count or logical depth". Declining to raise confidence because a denominator is inferred
is precisely the §20/§6 behaviour the standard asks for.

**Safety note honoured:** `no_hardware_run` field explicitly states no hardware run is authorized —
consistent with the project rule that the Qiskit Builder never submits to real hardware without
approval.

**DEFECTS:** `type: "resource-estimation"` violates the `templates/simulation-result.json` enum
(`quantum` / `classical` / `comparison`); missing schema-required `description`. **Dependency on
SIM-015d and SIM-019 is cited by ID** (`primary_sources`) — good practice — but the SIM-015d figure it
quotes, "alpha=3.97 (exact) / 4.07 (chi3 MERA)", is a *derived* input, so under §7 this estimate is
**structurally dependent** on the same force data it is costing.

---

### SIM-2026-055 — Yang–Lee via two-end PT-symmetric boundary field

| field | value |
|---|---|
| id / date | `SIM-2026-055`, `2026-06-26` |
| measurement | `nonunitary_alpha = {12: 3.7546, 14: 3.7541, 16: 3.7848}`; `g4_gate_pass: false` at every N; located `gamma` 0.16/0.15/0.14 with `c_eff ≈ 0.525/0.522/0.520` and `delta_phi ≈ +0.453/+0.455/+0.457` against targets `ceff_target 0.4`, `delta_phi_target -0.2` |
| verdict | "INVALID: G4 criticality gate FAILED … the two-end realization did NOT reach the bulk Yang-Lee fixed point at these N. **NOT a refutation** — the realization is wrong/under-resolved, alpha is uninterpretable. Honest negative." |

**Level: none earned (clean negative).** **CFN: high in intent, unrealized.** **Verdict proportionate —
exemplary.** Three alpha values in the 3.75–3.78 band are recorded and then explicitly declared
uninterpretable because the gate failed. That is the same discipline as SIM-032b/034.

**Unflagged systematic worth recording:** the unitary controls in this very file give
`crit_ee.c_eff` = 0.5649 (N=12), 0.5616 (N=14), 0.5587 (N=16) for a theory whose exact central charge is
**0.5** — a ~12% positive bias in the `c_eff` estimator at these sizes, measured by the record's own
control and never mentioned. The G4 gate is a comparison against `c_eff = 0.4`; using an estimator with
a self-measured 12% bias to adjudicate that gate should have been noted. (It does not change the
verdict here — the miss is 0.52 vs 0.4 with `delta_phi` wrong in **sign** as well as magnitude — but it
is an uncalibrated instrument being used as a gate.)

**Reproducibility — weak:** no script path, no `type`, no `description`; `runtime_s: 228.67` present;
full `locate_*` traces present (good). The `locate` objective values (`best.dist` ≈ 266–270) are
recorded without any statement of what the distance metric is — a reader cannot tell whether 266 is
close or far.

---

## 3. Cross-cutting findings

### 3.1 Contribution-level distribution for the range (§5)

| Level | Records |
|---|---|
| Level 1 — reproduction/validation | 032, 032b, 033, 033b, 034, 035 (the Delta_T=2.0000 datum), 036 (post-correction), 037, 040, 050, 051, 052 |
| Level 2 — methodological contribution | 031 (small no-go), 035 (localization obstruction), 039 (autograd + Z2-projected objective; the strongest), 053 (PT-edge structural obstruction) |
| Level 3 — new physics/mathematics | **none** |
| Level 4 — discriminating foundational | **none** |
| Not earned / invalid | 042, 044, 045, 045-chi6, 055 |
| Not a measurement | 054 (costing) |

**No record in SIM-031..055 is Level 3 or Level 4.** The MERA universality work (031, 035, 036, 037,
039, 040, 051, 052) delivers, at its best, Level-1 validation of quantities fixed in advance by
conformal symmetry (Delta_T = 2 → alpha = 4) plus Level-2 optimizer methodology. The Yang–Lee arm
(053, 055) produced two honest negatives and one useful structural no-go.

### 3.2 Independence ledger for the alpha-universality claim (§7)

The manuscript's "three universality classes, one exponent" rests on SIM-051/052 (TCI) and SIM-062/063
(Potts, outside this range), with SIM-050 as control.

| Shared between the Ising control and the TCI measurement |
|---|
| MERAKit.jl code path (Hauru arXiv:2007.03638), identical version |
| Ternary MERA architecture, block_size = 2, dense `ComplexSpace` |
| Riemannian LBFGS optimizer, direct-init at the same bond dimension |
| The scaling-superoperator estimator `Delta = -log_3 lambda` |
| The basin-selection rule "lowest Delta_sigma" |
| Julia 1.8.5 runtime |
| **Genuinely independent input: the Hamiltonian coefficient lam3 (0 vs 0.856) — and nothing else.** |

**Classification: structurally dependent / primarily a consistency check.** SIM-050 → SIM-051 →
SIM-052 is one pipeline evaluated at three settings, not three independent confirmations. Its
agreement with CFT is strong evidence the *pipeline* is correct and weak evidence about *physics*,
because the target values (0.125, 1.0, 2.0, 0.075, 0.2, 2.0) were all known exactly in advance.

Additional dependency: the **alpha** column in `paper-prd.tex` Table (line 466) and in SIM-051/052 is
not measured at TCI or Potts at all — it is `2 x Delta_T` applied to the measured Delta_T. No force was
computed at c = 7/10. The manuscript is honest about this in one place
(`research/submission-package/prd/paper-prd.tex` line 592: "The transport and force-profile
measurements, however, have been performed only at c = 1/2") but the abstract (line 29) reads
"giving alpha = 4.00 at all three universality classes", which a reader will take as three force
measurements. Flagged for the manuscript audit; the underlying records (SIM-051 `verdict`) are more
careful than the abstract.

### 3.3 Reproducibility metadata scorecard (§21)

Scoring the twelve §21 items across the 21 records:

| §21 item | Coverage |
|---|---|
| code revision / commit | **1 / 21** (SIM-052 only, `51f2c0c`). SIM-045 cites `b31c01b` for a *lost* record. |
| environment / dependency versions | **4 / 21** (050, 051, 052 give "Julia 1.8.5"; 031-042 give "local CPU" only) |
| platform information | 13 / 21 (`hardware_target` present on 031-042; absent on 044, 045, 045-chi6, 050-055) |
| random seeds | **0 / 21 stated in-record.** SIM-039/040 seeds are hard-coded in the scripts (`sim039_autograd_mera.py:168` `default_rng(42)`, `:186` `default_rng(2026)`; same lines in `sim040_chi4_tci_mera.py:162,170`) but never written to the record. SIM-051/052 label seeds `seed1..seed8` with no RNG values. |
| model parameters | 21 / 21 (good — N, chi, lam3, gamma all present) |
| solver settings | ~14 / 21 (niter, LBFGS/Adam, block_size where relevant) |
| convergence criteria | ~12 / 21 (gate thresholds stated for 036-040, 050-052; absent for 042, 044, 045) |
| input records cited by ID | 3 / 21 (053, 054 exemplary; 051 cites its pre-gate scripts) |
| output checksums | **0 / 21** |
| runtime metadata | 16 / 21 (`wall_seconds` / `wall_s` / `runtime_s`) |
| analysis script revision | **0 / 21** |
| one-command reproduction | **0 / 21** |

**Script-path presence:** present for 031–042 (`circuit.script_path`, all verified to exist);
**absent for 044, 045, 045-chi6, 050, 053, 054, 055** (7 of 21). For SIM-053/055 the driver
`research/data/simulations/hyp028b_yanglee_force.py` exists but is nowhere named in either record.

### 3.4 Schema conformance vs `templates/simulation-result.json`

| Violation | Records |
|---|---|
| `id` regex `^SIM-\d{4}-\d{3,}$` | `SIM-2026-032b`, `SIM-2026-033b` |
| missing required `description` | 045-chi6, 050, 051, 052, 053, 054, 055 |
| missing required `type` | 044, 045-chi6, 053, 055 |
| missing required `date` | 045-chi6 |
| `type` outside enum | 054 (`"resource-estimation"`) |
| duplicate `id` across files | 045 / 045-chi6 (both `"id": "SIM-2026-045"`) |
| invalid strict JSON (bare `NaN`) | 031 |

11 of 21 records in this range violate the project's own schema. ERRATA D3 records the aggregate
("only 9/36 SIM files … satisfy templates/*.json") but is stale (written 2026-06-08, before most of
this range existed) and none of the specific instances above are itemized.

### 3.5 Uncertainty reporting (§20)

- SIM-032/032b/033/033b/034/035/053/055 all report `alpha_err` / `dalpha` from the fit. Good.
- **SIM-042, 050, 051, 052 report no uncertainty on any scaling dimension or on alpha.** These are
  exactly the records the manuscript cites. The available uncertainty information — the seed-to-seed
  spread, [1.9219, 2.1889] at chi=6 and [1.9994, 2.0301] at chi=8 — is present as raw data but is never
  converted into an error bar, and the manuscript quotes `Delta_T = 1.999` / `alpha = 4.00` from the
  single best seed with no interval.
- No record in the range separates truncation (finite chi), finite-size, optimization/basin, and
  state-identification error as §20 requires.

### 3.6 Killer tests (§12)

- HYP-027's registered killer is well-formed and is quoted in `HYP-2026-027.json`
  `refutation_criteria`: refuted if, *after* the c = 7/10 gate passes, alpha lands outside [3.2, 4.8]
  and within error of `2*Delta_lightest`. It was never triggered — but note that as executed, alpha at
  TCI was never measured at all (only `2*Delta_T` was inferred), so **the registered killer was never
  actually exposed to data.** The hypothesis was upgraded to SUPPORTED on a quantity that cannot fail if
  the state is a CFT.
- HYP-028's G4 gate (`c_eff = 2/5`, `Delta_phi = -1/5`) *did* fire, twice, and both times the project
  declined to claim the result (SIM-053 `gates.G4_nonunitary_criticality: "NOT SATISFIED"`, SIM-055
  `g4_gate_pass: false`). The killer machinery works when the gate is a genuine physical requirement
  rather than an identity.

### 3.7 Hypothesis-record staleness (HYP-2026-027)

`research/data/hypotheses/HYP-2026-027.json`: `"status": "TESTABLE_NEAR_TERM"`,
`"last_updated": "2026-06-16"`. Its latest result note is `result_note_2026_06_17_stage2e_chi4`
(SIM-040). **There is no result note for SIM-042, 044, 045, 050, 051 or 052** — that is, the record for
the hypothesis contains nothing about the runs that actually answered it, and still carries status
`TESTABLE_NEAR_TERM` while `MEMORY.md` and the submitted manuscript both treat HYP-027 as **SUPPORTED
(high confidence)**. The structured record of record disagrees with the published claim.
**DEFECT (major).**

---

## 4. Defect register for this range

| # | Severity | Where | What |
|---|---|---|---|
| 1 | critical | `research/data/simulations/SIM-2026-042.json` `verdict` | "TCI Delta_T~2 FOUND … UNIVERSALITY SUPPORTED" read off a state whose own light primaries are wrong (lowest non-zero Delta = 0.473 vs CFT 0.075) and whose c reads 0.10 (SIM-044). `RESEARCH-LOG.md` 395-413 calls this exact reading "a motivated false positive — explicitly NOT claimed". Never corrected (single commit `55fcba6`), no ERRATA entry. |
| 2 | major | `research/digests/2026-06-16-team-scan.md` lines 9, 33-35 | Still asserts the ERRATA-D5-retracted "chi=3 MERA is INSUFFICIENT … ESCALATE to chi≥4" and credits PAPER-115/112 with "quantitatively confirming" a mechanism ERRATA D5 says was never tested. `git log` shows one commit, pre-retraction. D5 explicitly names this digest as affected. |
| 3 | major | `research/data/hypotheses/HYP-2026-027.json` `status`, `last_updated` | Status `TESTABLE_NEAR_TERM` / last updated 2026-06-16; no result notes for SIM-042/044/045/050/051/052; contradicts MEMORY.md ("HYP-027 SUPPORTED high") and the submitted manuscript. |
| 4 | major | `SIM-2026-051.json` `delta_T_statistics.all_8_seeds_mean` + `verdict` | Recorded mean 1.9913; actual mean of the eight listed Delta_T values is 2.0163 (median 1.9916). The verdict quotes the wrong figure ("1.99 mean across 8 seeds"). Correct mean alpha = 4.0325. |
| 5 | major | `SIM-2026-052.json` `delta_T_statistics.note` | "ALL 6 seeds give alpha within 1.5% of 4.0" is false (seed 4 = 4.0602 = 1.505%). ERRATA line 16 fixed this **in the manuscript** (now "within 2%") but never in the source record. |
| 6 | major | `SIM-2026-044.json` (whole file) | 352-byte stub with no `type`, no `results`, no verdict, no script reference — yet it is the record that disconfirms SIM-042. No cross-reference in either direction. |
| 7 | major | `SIM-2026-045.json` / `SIM-2026-045-chi6.json` | Duplicate `"id": "SIM-2026-045"`; `-045.json` self-reports "This file was overwritten by a chi=6 run"; the chi=4 result it calls "VALIDATED" has no structured record (prose + `.npz` only) and its "Delta_T=1.97/2.04" contradicts `RESEARCH-LOG.md` line 636 ("Delta_T=2 is not in the leading chi=4 dims"). |
| 8 | major | `research/data/simulations/` (7 ID slots) | SIM-038, 041, 043, 046, 047, 048, 049 have driver scripts on disk but no JSON record; outcomes exist only in `RESEARCH-LOG.md`. Not covered by ERRATA D1. |
| 9 | major | SIM-051, SIM-052, and the manuscript chain | No uncertainty is reported on Delta_T or alpha anywhere, while the record's own seed spread is [1.9219, 2.1889] (chi=6) and [1.9994, 2.0301] (chi=8); `paper-prd.tex` line 450 quotes the single best seed to four significant figures. Basin selection (`lowest Delta_sigma`) is a selection on the same spectrum and is not treated as a systematic. |
| 10 | minor | `SIM-2026-031.json` `results.tiers.synthetic_cft.fits_d_vs_r.power` | Bare `NaN` tokens → invalid strict JSON. Same class as ERRATA D2 but not listed there. |
| 11 | minor | `SIM-2026-036.json` `notes` | Still says "chi=3 floor" and credits PAPER-115/112 with predicting the ceiling — the exact claim ERRATA D5 retracts. Verdict was fixed; notes were not. |
| 12 | minor | `SIM-2026-040.json` `verdict` | Omits the caveat carried by `HYP-2026-027.json` `result_note_2026_06_17_stage2e_chi4` and `ERRATA.md` 138-140 that a faithful state does not dissolve the SIM-035 localization obstruction; reads as if the force read-out follows immediately. |
| 13 | minor | `SIM-2026-051.json` `control_lam3_0.note` | "matches SIM-050" for `Delta_sigma = 0.1402` vs SIM-050's 0.12515 / CFT 0.125 — a 12% deviation, ~12x the control's. |
| 14 | minor | `SIM-2026-042.json` `verdict` | Ising `Delta_sigma = 0.1010` vs CFT 0.125 (19% off) written as "VALIDATED … 0.1010~0.125"; `gateB: true` where `RESEARCH-LOG.md` 388 says only "qualitatively PASS". |
| 15 | minor | `SIM-2026-053.json` `verdict_rationale` | "Im(E0)~2e-2" is wrong — `E0_im` is −6.1e-15; 2e-2 is `V_imag_max`. Also `gamma_c_by_N` vs `kappa_c` naming drift, and an N=10 value cited that is not in the record. |
| 16 | minor | `SIM-2026-055.json` | Unitary controls give `c_eff` = 0.5649/0.5616/0.5587 for exact c = 0.5 (~12% estimator bias, self-measured) and this is never flagged, though `c_eff` is the G4 gate quantity. |
| 17 | minor | 11 of 21 records | Schema violations vs `templates/simulation-result.json` (see §3.4). ERRATA D3 is stale and itemizes none of them. |
| 18 | minor | `SIM-2026-037.json` `results.note_on_completeness` | Record was "authored by hand from the evaluated checkpoint" rather than written by the script. Disclosed (good), but should be marked as partially synthetic in any provenance ledger. |
| 19 | minor | `HYP-2026-027.json` `feasibility_mandatory_gates[0]` | Still mandates the ANNNI route ("NOT spin-1 Blume-Capel"); the executed work used O'Brien–Fendley and the manuscript describes the target as "the Blume–Capel point of the … O'Brien–Fendley spin chain" (`paper-prd.tex` line 429). The gate was superseded and left unedited. |

---

## 5. What this range did well (recorded so the audit is calibrated, per §"take the good for what it's worth")

1. **SIM-053's override of its own automated verdict** from "REFUTED (stronger universality)" to
   "INCONCLUSIVE", with a structural argument (`verdict_rationale`) and an explicit
   `G5_PT_unbroken: "PASS but VACUOUS"`. A pipeline handed the project a publishable positive and the
   project declined it.
2. **SIM-032b, SIM-034 and SIM-055 each discard an on-target number because a control failed.**
   SIM-034's TCI alpha = 4.4125 ± 0.2317 sits inside the acceptance window and was thrown away because
   the Ising control read 1.3265. That is the §19 standard actually being met.
3. **SIM-039's two-bug diagnosis** (finite-difference gradients; raw vs Z2-projected objective), with
   gradients verified against finite differences to ~1e-10 and a passing control under the identical
   protocol. This is the range's one durable Level-2 contribution.
4. **SIM-051's blocking pre-gate**: exact-diagonalization proof that the block_size=2 dim-4 operator
   reconstructs the full three-site O'Brien–Fendley Hamiltonian to `1.1e-16` on 6- and 8-site PBC
   rings, which retired an earlier false "blocking is wrong" diagnosis.
5. **SIM-051's verdict states the counterfactual-novelty problem itself**: "This is exactly the CFT
   prediction: Delta_T=2 in every unitary 2D CFT … The numerics confirm the symmetry argument."
6. **SIM-036's retraction structure** (`verdict` + preserved `verdict_SUPERSEDED_2026_06_16`, two-commit
   git history) is the right template — it just needs to be applied to SIM-042.
7. **SIM-054 refuses to raise its confidence** above LOW because a denominator is inferred rather than
   published.

---

## 6. UNVERIFIED

Items I could not confirm within this task's scope. Silence would not be a pass, so they are listed.

1. **I did not re-run any simulation.** All numerical agreement claims (energies, Delta values, alphas)
   are audited for internal consistency and against exact CFT values I can state from theory; I did not
   independently recompute any MERA optimization, exact diagonalization, or superoperator spectrum. The
   two arithmetic checks I *did* perform independently are the SIM-051 seed mean (defect #4) and the
   SIM-052 1.5% claim (defect #5).
2. **I did not verify the MERAKit.jl driver contents.** `research/tools/MERAKit.jl/` is gitignored
   vendored code; I confirmed the tracked mirrors `research/tools/merakit-setup/qw_tci_measure.jl`,
   `qw_tci_chi8.jl`, `qw_of_control_correct.jl` exist as files but did not read them to confirm the
   recorded `method` strings (bond dim, block_size, seed count, iteration count) match the code.
3. **I did not verify commit `51f2c0c` actually contains `qw_tci_chi8.jl`** — only that the object
   resolves to a commit (`git cat-file -t`). Same for `b31c01b`.
4. **Prior art / novelty (§8) was not searched.** No literature gate was run for anything in this
   range. My Level assignments rest on the derivation gate only (is the number fixed by symmetry or a
   Virasoro identity), which I can assert for Delta_T = 2, Delta_sigma = 1/8, Delta_eps = 1 (Ising) and
   Delta_sigma = 3/40, Delta_eps = 1/5 (M(4,5)). The claim that O'Brien–Fendley (2018) already
   establishes lam3/lamI = 0.856 as the TCI point is taken from `SIM-2026-032.json` `description`
   (citing arXiv:1712.06662) and `paper-prd.tex` line 429, not from reading that paper.
5. **The `locate` objective in SIM-055** (`best.dist` ≈ 266–270) is undefined in the record; I could not
   determine whether those values indicate near or far, so my statement that "the scan never got near
   Yang–Lee" rests on the reported `c_eff ≈ 0.52` vs target 0.4 and `delta_phi ≈ +0.455` vs target
   −0.2, not on `dist`.
6. **SIM-053/055 driver identification.** I inferred `research/data/simulations/hyp028b_yanglee_force.py`
   is the driver from filename and the HYP-028 association; neither record names any script, so this is
   an inference, not a verified linkage.
7. **`research/data/theory/` is NOT empty**, contrary to the premise given in my task brief. It
   contains 8 markdown files (`RUN-A-methods.md`, `epsilon-channel-proof.md`,
   `paper-review-synthesis.md`, `research-challenge.md`, `research-practical.md`, `research-primary.md`,
   `task4-ope-argument.md`, `task5-crofton-derivation.md`). What it lacks is any *structured* (JSON)
   theory record. I did not read those files, so I cannot say whether any of them documents the
   theoretical dependencies of the SIM-031..055 claims.
8. **Manuscript audit is out of scope.** I flag the abstract-vs-body tension on "alpha = 4.00 at all
   three universality classes" (`research/submission-package/prd/paper-prd.tex` line 29 vs line 592) and
   the untransferable-boundary-operator concession from SIM-035, but I did not audit the manuscript
   systematically; that belongs to the manuscript agent.
9. **Whether any of the 7 recordless SIM slots (038, 041, 043, 046–049) produced results that would
   change conclusions.** I read the RESEARCH-LOG narrative around them (lines 643–685) but did not
   attempt to reconstruct their outputs from the `.npz` files in the working tree.
