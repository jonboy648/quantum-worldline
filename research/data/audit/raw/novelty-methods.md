# Novelty Audit — Methodological Contributions (adv:lit-methods)

**Role:** Literature adversary (RESEARCH-DIRECTOR.md §27 "Literature adversary"; gate defined in §8).
**Mandate:** attempt to *eliminate* the project's novelty claims for four methodological targets.
**Date:** 2026-08-17. **Repo HEAD at start:** `9470d69` (branch `public-release`).
**Endpoints used:** WebSearch, WebFetch, Semantic Scholar (rate-limited, see UNVERIFIED),
`mcp__paper-search__download_arxiv`, `mcp__paper-search__search_google_scholar`.
**Endpoint NOT used (owned by sibling agent this phase):** arXiv export API.

**Standard applied.** §8 has three gates: *literature* (does prior art exist?), *derivation* (does the
number follow automatically once known assumptions are accepted?), *prior art* (state precisely what
this project does that the nearest work does not). §6 requires a **counterfactual novelty** field.
§7 requires an **independence ledger**. I apply all four. Per the task framing I never write
"novel", "first", or "to our knowledge" without a recorded citation.

---

## 0. Executive verdict table

| # | Claim under test | Nearest prior work | Verdict | Level (§5) | Counterfactual novelty (§6) |
|---|---|---|---|---|---|
| 1 | L₂ε contamination ~400× suppressed in puMPS Bloch elements; finite-size exponent p≈2.4 not N^−0.2 | Milsted & Vidal, PRB 96 245105 (arXiv:1706.01436) §IV.A Eq. (22) + Fig. 4; Zou–Milsted–Vidal, PRL 121 230402 (arXiv:1710.05397) Table I + SM "Extrapolation of conformal data" | **NOVELTY LARGELY ELIMINATED.** The suppression *mechanism* is the published rationale for the very estimator used; the exponent-2 finite-size law is published for Ising, Potts **and** the OF/TCI point. Surviving increment: the numerical *ratio* as a reported diagnostic. | Level 1 with a thin Level-2 sliver | Near-zero to low |
| 2 | C_TTT measured across three universality classes (Ising/TCI/Potts) | Milsted & Vidal 1706.01436 Fig. 4 (Ising c=0.4995, **3-state Potts c=0.7985**); Zou–Milsted–Vidal 1710.05397 Table I (Ising c=0.4999997, **OF/TCI c=0.6991**) | **NOVELTY ELIMINATED.** No three-point function is ever computed. The drivers literally execute `cttt = 2*sqrt(2)/sqrt(c)`. All three "measurements" are lower-precision re-runs of published c-extractions, on the original authors' code, with the original authors' model builders. | Level 1 | **Zero** |
| 3 | Force exponent α = 2Δ_T = 4 from MERA / stress-tensor exchange | Sahay–Lukin–Cotler, PRX 15 021078 (arXiv:2401.13595); **Wang & He, arXiv:2501.03084** (identical observable, identical operator, identical model, 14 months earlier); Chua–Passias–Tiwari–Ryu, PRB 95 195152 | **NOVELTY LARGELY ELIMINATED.** The mechanism (stress-tensor/graviton exchange producing an attractive hologron potential) is SLC's stated result; the observable is Wang & He's U_int verbatim. Surviving increment: 12 separations instead of 4, and a fitted exponent — an increment already destabilised by inv-sims-early. | Level 1–2 | Near-zero (project's own manuscript calls α=4 "exact") |
| 4 | MERA-as-geometry discrimination (matched control / rewiring) — the proposed flagship | Milsted & Vidal, arXiv:1812.00529; Bao *et al.*, PRD 91 125036 (arXiv:1504.06632); Czech–Nguyen–Swaminathan, JHEP 03(2017)090; Evenbly, PRL 119 141602; Singh, arXiv:1701.04778 | **NOT ALREADY DONE — but the framing is obsolete.** No published *matched-control / rewiring numerical* experiment found. However the analytic question the flagship intends to answer has a published answer that contradicts the project's premise: Milsted & Vidal prove MERA's geometry is a **light sheet/light cone, neither the hyperbolic plane nor de Sitter**. The flagship must be redesigned around that, or it will be refereed as re-litigating a settled derivation. | Would be Level 4 if done | High — *if* the premise is repaired |

**One-sentence headline.** Milsted & Vidal (2017) and Zou–Milsted–Vidal (2018) already published the
central charge for all three of the project's "C_TTT ladder" models — Ising, the O'Brien–Fendley
tricritical point, and 3-state Potts — using the same estimator and, for two of the three, the same
code the project vendored; the project's C_TTT numbers are that published `c` pushed through the
algebraic identity `2√2/√c`, and no stress-tensor three-point function is computed anywhere in the
repository.

---

## 1. TARGET 1 — "L₂ε contamination is ~400× suppressed in puMPS Bloch-state matrix elements, with finite-size corrections p≈2.4 instead of N^−0.2"

### 1.1 The claim as recorded

`research/data/simulations/SIM-2026-068.json`, field `key_findings[1]`, verbatim:

> "The feared L2eps contamination (~N^-0.2 element mixing, the reason ED could not close TCI at
> N<=16) is STRONGLY SUPPRESSED in puMPS Bloch-state elements: at N=56 the largest non-T raw element
> is <=0.0003 vs T's 0.109 (~400x), and the observed finite-size correction exponent is p ~ 2.4, not
> 0.2. The variational Bloch tower resolves the near-degenerate states that raw ED mixed."

Two further items are presented as findings in the same field list:

- `key_findings[2]`: "T/L2sigma level ordering flips between N=14 … and N>=28 …; element-dominance
  identification handles this automatically — position-based ID would have silently measured the
  wrong state."
- `key_findings[3]`: the "two-error cancellation" between finite-N and finite-D bias.

The "N^−0.2" foil originates inside the project, not in the literature:
`research/data/simulations/SIM-2026-067.json`, field `results.tci_of`, verbatim: "TCI has L_{-2}eps at
Delta=2.2 with the SAME quantum numbers as T (even, s=2), element contamination dies as ~N^{-0.2}".
That is the project's own degenerate-perturbation estimate. **I found no publication asserting an
N^−0.2 law for this quantity.** So the headline "p≈2.4, not 0.2" is a correction of an internal
expectation, not of a literature claim — and, as shown below, the literature had already published
the correct law.

### 1.2 Nearest prior work — A: Milsted & Vidal, PRB 96, 245105 (2017), arXiv:1706.01436

Downloaded and text-extracted (scratch copy `1706.01436.pdf` → `mv2017.txt`). Section IV.A,
"Normalization of H and central charge c", verbatim (extracted-text lines 793–802):

> "…the central charge c of the emergent CFT can then be estimated by the simple expectation value
> [9]  c ≈ 2⟨I|H†₂H₂|I⟩. (21)
> **Alternatively, in order to eliminate finite-size corrections of H₂ that connect |I⟩ to states
> other than |T⟩, we can use  c ≈ 2|⟨T|H₂|I⟩|², (22)  which often produces more accurate results.**"

This is the *published statement of the contamination problem and its fix*. "Finite-size corrections
of H₂ that connect |I⟩ to states other than |T⟩" **is** L₂ε-type contamination stated in general
form. Equation (22) is the single-state estimator the project uses. The project therefore did not
discover that the estimator suppresses contamination; **suppressing contamination is the published
reason the estimator exists**, and the project adopted the estimator from that paper's successor.

Two further items in the same section pre-empt the project's `key_findings[2]` (extracted-text
lines 760–766 and 805–811), verbatim:

> "…|T⟩ is the eigenstate with momentum P_T = 2 × 2π/N that **has maximal overlap with H̃₋₂|I⟩**"

> "The usual procedure to normalize H is to identify |T⟩ as the lowest-energy state with
> P_α = 2 × 2π/N [4]. **However, this fails if finite-size corrections shift the energy of another
> state with P_α = 2 × 2π/N below that of |T⟩, as happens e.g. in the ANNNI model discussed in
> Sect. V C.**"

So (i) element-dominance identification of T is Milsted & Vidal's published rule, and (ii) the
failure of position-based identification when a competing |s|=2 state drops below T is Milsted &
Vidal's published warning, with a named example model. SIM-2026-068 `key_findings[2]` restates both.
SIM-2026-067's `results.ising` note that "max-element identification tried and FALSIFIED" in raw ED,
requiring a Δ-plausibility gate, is a genuine — but small — refinement of MV's rule for the ED
regime; it is correctly a Level-2 sliver, not a discovery.

### 1.3 Nearest prior work — B: the finite-size exponent

Milsted & Vidal 1706.01436, Figure 4 caption, verbatim (extracted-text lines 1037–1043):

> "Central charge from (21), with linear extrapolation to large N using all visible data. System
> sizes shown are **N = 8…18 for the Ising model and N = 8…14 for the three-state Potts model.** …
> **The scaling exponent 2 is consistent with known finite-size corrections present in both models
> [12, 18, 54].**"

Zou–Milsted–Vidal 1710.05397, Supplemental "Extrapolation of conformal data" (extracted-text
lines 1549–1563), verbatim:

> "For the Ising model, x_α = x_c = 2 due to the presence of perturbations of operators with scaling
> dimension Δ = 4. Thus we can linearly fit finite size conformal data with N^−2 to extrapolate the
> thermodynamic quantities… Since we can only approximately locate the TCI point of the
> O'Brien–Fendley (OF) model… **Indeed, we observe scaling compatible with a dominant contribution
> from a Δ = 4 operator, as for the Ising model, and perform ex[trapolation]…**"

**Result: the exponent-2 finite-size law for c is published for the Ising chain, the 3-state Potts
chain, and the O'Brien–Fendley model at its TCI point.** SIM-2026-068's fitted p ∈ [2.31, 2.42]
(field `fit.variants`) and SIM-2026-069's p ∈ [1.90, 1.96] (same field) bracket the published value
2 from either side. This is a reproduction of a published scaling law, presented as a finding.

### 1.4 What survives

| Component of the claim | Status against literature |
|---|---|
| puMPS Bloch states resolve TCI conformal data where ED cannot | **Published.** ZMV 1710.05397 Table I: OF model at the TCI point, c = 0.6991 (quoted error 10^−4), N ≤ 128, D ∈ [28,44]. |
| Single-state element estimator suppresses non-T contamination | **Published rationale.** MV 1706.01436 Eq. (22) and the sentence introducing it. |
| Level-ordering flip; position-based ID is unsafe | **Published.** MV 1706.01436 §IV.A (ANNNI example). |
| Finite-size correction exponent ≈ 2, not 0.2 | **Published.** MV Fig. 4 (Ising, Potts); ZMV SM (Ising, OF/TCI). |
| The *numerical ratio* (largest non-T raw element vs T's) reported as a quantitative diagnostic | **Not found in the literature.** This is the only surviving element. |
| Two-error cancellation (finite-N bias up, finite-D bias down) used *predictively* | **Adjacent prior art.** ZMV SM notes "finite D affects the T T̄ state far more seriously than other lower-energy states" (extracted-text lines 1584–1586), i.e. D-systematics are documented; the *cancellation* framing and the pre-run prediction (SIM-2026-069 `D_systematics`, "the D=28 re-run was PREDICTED to land at 0.8022+-0.0005 before it ran, and landed at 0.80197") I did not find published. Small but real. |

### 1.5 Verification of the project's own numbers

I checked the underlying data, not just the record. `research/tools/pumps-setup/qw_cttt_of_results_2026-08-10.jsonl`
carries a `raw` array of KS element magnitudes per stage. At N=40 the row reads
`"raw" : [0.1531556120698552, 0.00011952372972711859, 1.3740183033432898e-5, …]` → dominance
≈ 1280×, not 400×; the quoted "~400×" corresponds to the N=56 row only. The order of magnitude is
supported by the data; the specific figure is one row of a size-dependent ratio and should be quoted
as a range, not a constant. The N=14 rows show two different `c` values (0.00944… and 0.8257…) from
the same `spectrum`, which is the identification ambiguity the record describes — the data is
consistent with the record's account.

### 1.6 Independence ledger entry (§7)

| Field | Value |
|---|---|
| Side A raw data | puMPS Bloch-state KS elements, this project, N=14…56 |
| Side B (comparison) | exact 2√2/√c and exact c = 7/10 |
| Shared theory | Koo–Saleur correspondence; Δ_T = 2; Virasoro central term |
| Shared code | **`yijian-physics/puMPS` @ `0557b12` — the ZMV authors' own implementation**, including `OBF_Hn_MPO_split` (the OF/TCI model builder) and `Hn_in_basis` (the KS element routine). Source: `research/tools/pumps-setup/VENDOR.md`, "What" section and the function table. |
| Shared state prep | ZMV's `minimize_energy_local_CG!` |
| Genuinely independent info | The D-convergence ladder run at this project's own D values; nothing else. |
| **Classification** | **Structurally dependent / primarily a consistency check.** |

### 1.7 Verdict

**Novelty largely eliminated.** Publication framing that would survive: *"we report quantitative
element-dominance ratios for the Koo–Saleur T-identification in puMPS Bloch bases at the TCI and
Potts points, and a predictive treatment of the competing finite-N / finite-D biases"* — a short
methods note, explicitly citing MV 1706.01436 Eq. (22) as the origin of the estimator and ZMV
1710.05397 for the N^−2 law. Any wording implying the suppression or the exponent was discovered
here fails the §8 prior-art gate.

**Killer test (§12) that this claim must now pass:** re-run the c extraction with the *other*
published estimator, MV Eq. (21), at matched N and D. If (21) also converges (as MV's own Fig. 4
shows it does at N ≤ 18 for Ising and N ≤ 14 for Potts), the "suppression" is a quantitative
convenience, not an enabling mechanism. **Note that the project has recorded the opposite
conclusion without this control** — see §5.3 below.

---

## 2. TARGET 2 — "The C_TTT = 2√2/√c measurement across three universality classes"

### 2.1 The derivation gate comes first, and it closes the question

§8's derivation gate asks: "Is it a direct Virasoro identity? Does it follow algebraically from a
previously extracted parameter?"

In a 2D CFT with the standard normalisations ⟨T(z₁)T(z₂)⟩ = (c/2)/z₁₂⁴ and
⟨T(z₁)T(z₂)T(z₃)⟩ = c/(z₁₂²z₁₃²z₂₃²) (Belavin–Polyakov–Zamolodchikov 1984; standard textbook
result, e.g. Di Francesco–Mathieu–Sénéchal ch. 5–6), define the unit-normalised
T̂ ≡ T/√(c/2). Then

  C_TTT ≡ ⟨T̂T̂T̂⟩-coefficient = c / (c/2)^{3/2} = 2√2/√c.

This is two lines of algebra from the Virasoro central term. **C_TTT carries no information that c
does not.** Measuring C_TTT is measuring c.

### 2.2 The code confirms it: no three-point function is ever computed

`research/tools/pumps-setup/qw_cttt_of.jl:117` — verbatim:

```julia
        cttt = 2*sqrt(2)/sqrt(c)
```

`research/tools/pumps-setup/qw_cttt_potts3.jl:132` — identical line.

The upstream c is computed by `research/data/simulations/SIM-2026-068.json` field `method`:
"c = 2|<T|H_{+-2}|0>*N/(2 pi v_T)|^2; C_TTT = 2*sqrt(2)/sqrt(c)". There is no `⟨TTT⟩`, no
three-point correlator, no OPE contraction of three stress tensors anywhere in either driver.
`research/data/simulations/SIM-2026-067.json` field `design_evolution` records that the *original*
Route B design did attempt a genuine correlator route (`<hh>`/`<hhh>`) and that it "was FALSIFIED by
ED within the hour"; the project then "Pivoted same-day to the Koo-Saleur MATRIX-ELEMENT route".
That pivot converted a three-point measurement into a one-point-plus-identity calculation. The record
is transparent about the pivot but the headline was never re-labelled.

**Consequence:** every occurrence of "C_TTT measured", "the self-coupling ladder", and "stress-tensor
self-coupling confirmed at c = 1/2, 7/10, 4/5" (SIM-2026-069 `verdict`; `NEXT-SESSION.md` lines 21–24)
describes a central-charge extraction wearing a different name.

### 2.3 Literature gate: the c values themselves are published, for all three models

| Model | Project value | Published prior value | Source |
|---|---|---|---|
| Critical Ising | c → 0.49871 (SIM-2026-067 `results.ising`, ED N=8…18) | **c = 0.4995** (ED, N = 8…18, same sizes) | Milsted & Vidal 1706.01436, Fig. 4 |
| Critical Ising | — | **c = 0.4999997, error 10^−7** (puMPS, N ≤ 228, D ≤ 49) | Zou–Milsted–Vidal 1710.05397, Table I |
| O'Brien–Fendley at TCI | c_inf = 0.699 ± 0.002 (SIM-2026-068 `fit.quoted`, N=14…56) | **c = 0.6991, error 10^−4** (puMPS, N ≤ 128, D ∈ [28,44]) | Zou–Milsted–Vidal 1710.05397, Table I |
| 3-state Potts | c_inf = 0.7995 ± 0.0012 (SIM-2026-069 `fit.quoted`, N=10…40) | **c = 0.7985** (ED, N = 8…14) | Milsted & Vidal 1706.01436, Fig. 4 |

ZMV Table I is reproduced verbatim from the extracted text (lines 197–220):

> Critical Ising model — exact / puMPS / error: c 0.5 / 0.4999997 / 10⁻⁷ ; Δ_σ 0.125 / 0.1249995 /
> 10⁻⁷ ; Δ_ε 1 / 0.9999994 / 10⁻⁷ ; Δ_∂∂̄σ 2.125 / 2.12501 / 10⁻⁵ ; Δ_∂∂̄ε 3 / 3.00002 / 10⁻⁵ ;
> Δ_TT̄ 4 / 4.007 / 10⁻³.
> **OF model, TCI point** — exact / puMPS / error: **c 0.7 / 0.6991 / 10⁻⁴** ; Δ_σ 0.075 / 0.07492 /
> 10⁻⁵ ; Δ_ε 0.2 / 0.2001 / 10⁻⁴ ; Δ_σ′ 0.875 / 0.8747 / 10⁻⁴ ; Δ_ε′ 1.2 / 1.203 / 10⁻³ ;
> Δ_ε″ 3.0 / 3.002 / 10⁻³.
> "For the Ising model, we used system sizes N ≤ 228 and bond dimensions 24 ≤ D ≤ 49. For the OF
> model near its Tri-Critical Ising (TCI) point, we used N ≤ 128 and 28 ≤ D ≤ 44."

And ZMV's estimator, verbatim (extracted-text lines 184–190):

> "The lattice state |T⟩ corresponding to the stress tensor operator T is characterized as the energy
> eigenstate |ψ⟩ which maximizes |⟨ψ|H₋₂|I⟩|, in analogy with the CFT relation
> L₋₂|I⟩ = √(c/2)|T⟩. Below we use eigenstates |I⟩ and |T⟩ to compute an estimate of the central
> charge **c ≈ 2|⟨T|H₋₂|I⟩|²**."

That is, character for character, the project's estimator.

**Precision comparison, stated plainly.** On the Ising rung the project's ED result (0.49871) is
worse than Milsted & Vidal's ED result at the *same system sizes* (0.4995), and roughly four orders
of magnitude worse than ZMV's puMPS result (0.4999997). On the TCI rung the project's ±0.002 band is
~20× wider than ZMV's 10⁻⁴. On the Potts rung the project is more precise than MV's ED fit
(0.7995 ± 0.0012 vs 0.7985) — that is the ladder's one genuine numerical improvement over published
work, and it is an improvement of about one part in 10³ obtained by running the same authors' code
at larger N.

### 2.4 Independence ledger (§7) — the ladder is not three independent confirmations

`research/tools/pumps-setup/VENDOR.md` states the provenance without ambiguity:

> "`research/tools/puMPS/` holds a vendored copy of **`yijian-physics/puMPS`** — the authors' own
> implementation of periodic uniform Matrix Product States from **Zou, Milsted & Vidal, PRL 121,
> 230402 (2018)** (arXiv:1710.05397)… Pinned commit `0557b12…`"

and its function table lists, as already-implemented upstream:
`OBF_Hn_MPO_split` ("**O'Brien-Fendley H_n MPOs (TCI!)**"), `potts3_Hn_MPO_split`
("**3-state Potts H_n MPOs**"), `Hn_in_basis`, `excitations!`, `minimize_energy_local!`.

So: the three rungs share the same ansatz, the same optimiser, the same KS element routine, the same
model Hamiltonians, the same estimator, the same identification rule, and the same authors' code.
What differs between rungs is only the model builder called and the target constant. The three-model
agreement is therefore **a consistency check across three inputs to one pipeline**, not three
independent confirmations of a physical relation.

| Field | Value |
|---|---|
| Shared exact CFT identities | Δ_T = 2 (used to *calibrate* v_T — see below); C_TTT = 2√2/√c |
| Shared numerical code | ZMV `puMPS` @ 0557b12, all rungs |
| Shared state preparation | `minimize_energy_local_CG!`, all rungs |
| **Classification** | **Algebraically equivalent (C_TTT ← c) and structurally dependent (one pipeline).** |

**A circularity worth flagging to the analytic sibling** (outside my remit to adjudicate):
SIM-2026-068 `method` states "v_T calibrated from Delta_T=2 (exact in any CFT)". The velocity used to
normalise the Hamiltonian is fixed by assuming Δ_T = 2 — and Δ_T = 2 is the same input that makes
α = 2Δ_T = 4 (Target 3) "exact". Milsted & Vidal 1706.01436 §IV.A make the same calibration explicit
("recalling that the scaling dimension of T is Δ_T = 2 … we set a = 4π/N/(Ẽ_T − Ẽ_I)"), so this is
standard practice, not an error — but it means Δ_T = 2 cannot simultaneously be a *measured*
confirmation and a *calibration input*, and several project records treat it as measured
(e.g. SIM-2026-051's "Δ_T = 2.007 → α = 4.01").

### 2.5 Verdict

**Novelty eliminated (§8 literature gate AND derivation gate).** Counterfactual novelty: **zero** —
before the calculation, only "the implementation works" or "the implementation is broken" were
possible, because c was already published for all three models and C_TTT is c by algebra.

**Honest framing that would survive referee scrutiny:** *"We reproduce the Koo–Saleur central-charge
extraction of Milsted–Vidal and Zou–Milsted–Vidal on three minimal models, extending the published
3-state Potts extraction from N ≤ 14 (ED) to N ≤ 40 (puMPS) and improving its precision; we quote the
result equivalently as the unit-normalised stress-tensor self-coupling 2√2/√c."* Anything stronger —
in particular the phrase "THE LADDER IS COMPLETE" (SIM-2026-069 `title`) presented as a scientific
result rather than a pipeline milestone — exceeds the evidence.

**Recommended record edits:** add to `research/ERRATA.md` and to SIM-2026-067/068/069 an explicit
prior-art field naming MV 1706.01436 Fig. 4 and ZMV 1710.05397 Table I with the published c values,
and re-label `title`/`verdict` from "C_TTT … MEASURED" to "central charge reproduced; C_TTT quoted
via the Virasoro identity".

---

## 3. TARGET 3 — "Force exponent α = 2Δ_T = 4 from MERA; stress-tensor exchange"

### 3.1 What was actually measured

`research/data/simulations/SIM-2026-011-interaction.json`:

- `description`: "Holographic interaction energy F(dr) on **exact 24q OBC critical TFIM GS**.
  F(dr) = E_dual - E_0 - 2*(E_single_avg - E_0)."
- `ground_state.method`: `"eigsh(H, k=1, which='SA')"`, `qubits: 24`.
- `boundary_primary_coeffs`: `{"alpha": 0.635, "beta": -0.026}`.
- `fits.F_avg_dr_ge2.power_law`: `alpha = 3.9217…`, `dalpha = 0.1589…`.
- `fits.F_avg_all_dr.power_law`: `alpha = 2.2956…` (the dr≥2 window is what produces 3.92).

**Structural observation that bears directly on novelty: there is no MERA in this calculation.**
The state is an exactly diagonalised 24-qubit spin chain; the observable is an energy difference on
that chain. Whatever α = 3.92 measures, it is a property of the critical chain and of the operator
inserted, not of a tensor network. The manuscript's own §sec:force confirms this
(`research/submission-package/prd/paper-prd.tex`, "On the exact 24-qubit eigsh ground state").
A quantity computed without a MERA cannot discriminate MERA geometry from ordinary CFT (§4 Hypothesis
A vs B) — by construction.

### 3.2 Nearest prior work — A: Wang & He, arXiv:2501.03084 (submitted 2025-01-06)

This is the closest prior art and it is **closer than the manuscript acknowledges**. Extracted from
the repository's own copy `research/data/papers/2501.03084.pdf`, verbatim:

> "we directly calculate the interaction energy **U_int(j, j′)** between two bulk quasiparticles
> generated by two boundary spin primary operators σ^∂_j and σ^∂_{j′}, i.e.,
> **U_int(j, j′) = ⟨Ψ_{j,j′}|H|Ψ_{j,j′}⟩ − ⟨Ψ_j|H|Ψ_j⟩ − ⟨Ψ_{j′}|H|Ψ_{j′}⟩**, with
> |Ψ_{j,j′}⟩ ≡ U†σ^∂_j σ^∂_{j′} U|Ψ_GS⟩ representing the two-quasiparticle state. As shown in
> Fig. 2(b), **all interaction energies are negative**, indicating that these quasiparticles ex[hibit
> attractive interactions]"

and their Eq. (3), verbatim:

> "σ^∂_j = V†[**0.635**(X_j + X_{j+1}) − **0.026**(X_j Z_{j+1} + Z_j X_{j+1})]V"

Compare the project's manuscript, `research/submission-package/prd/paper-prd.tex` §"Observable:
interaction energy" (line ~268 onward):

> "The ZZ correlator change V(dr) = C_two(dr) − C_vac(dr) used in prior work~\cite{SahayLukinCotler2025}
> fails … **We identify the correct observable as the interaction energy:**
> F(dr) = E_dual(dr) − E_0 − 2 δE_single … The boundary-primary operator is~\cite{ZouMilstedVidal2020}
> σ_j = 0.635(X_j + X_{j+1}) − 0.026(X_j Z_{j+1} + Z_j X_{j+1})."

**Same observable (two-particle energy minus the two one-particle energies), same boundary-primary
operator with the same numerical coefficients, same universality class, published 14 months before
SIM-2026-011 (2026-03-18), and already catalogued by this project** as
`research/data/papers/PAPER-2026-010.json`, whose `interaction_energy` field records Wang & He's
formula and whose `key_claims` records "Attractive interactions confirmed: U_int(j,j′) < 0 for all
measured separations j′=5,6,7,8".

The manuscript's Eq. (eq:Fdr) is not attributed to Wang & He. The phrase "We identify the correct
observable" therefore fails the §8 prior-art gate. **Defect.** The manuscript *does* cite Wang & He
elsewhere — line 121 ("We follow the protocol of Wang and He") for the *transport* experiment, and
line 556 in the prior-art list where they are credited only with "Discovered holographic transport in
MERA circuits". The interaction-energy observable is credited to nobody.

**What genuinely differs from Wang & He:** they report 4 separations (j′ = 5…8) on MERA-mapped bulk
quasiparticle states and fit nothing; the project reports 12 separations on the exact boundary chain
and fits an exponent. That is the whole increment.

### 3.3 Nearest prior work — B: Sahay, Lukin & Cotler, PRX 15, 021078 (2025), arXiv:2401.13595

Abstract, verbatim: "…the bulk theory arising from this optimized tensor network furnishes
excitations with **attractive interactions**. Remarkably, these excitations have one- and
two-particle energies **matching the predictions for matter coupled to AdS gravity at long
distances**…"

Their two-particle potential (retrieved from the ar5iv full text; consistent with the project's own
`research/data/papers/PAPER-2026-009.json` field `key_claims`):

> Ṽ_TN(|ρ₁ − ρ₂|) ≈ C₁ − C₂ e^{−|ρ₁−ρ₂|/ℓ_AdS}, with C₁ = 0.080(8), C₂ = 13.6(8),
> ℓ_AdS⁻¹ = 0.69(1) ≈ log 2, mc² = 2.5(1),

and, crucially for this target, the mechanism attribution, verbatim from the same source:

> "Since the boundary stress tensor is dual to the bulk graviton in AdS/CFT, **the attractive part of
> the potential is evidently dominated by gravitational attraction**",
> with the stress-tensor contribution written as b_AdS(ρ₁,ρ₂)·(C_T + C_T̄)·e^{−|ρ₁−ρ₂|/ℓ_AdS};
> and the long-range constant part attributed to "energy from ε-primary of the Ising CFT".

**So "the attractive interaction between these excitations is dominated by stress-tensor /
graviton exchange" is Sahay–Lukin–Cotler's published conclusion, not this project's finding.** The
project's contribution is a different *coordinate presentation* of that mechanism.

### 3.4 A defect in the manuscript's differentiation argument

The manuscript's separation from SLC rests on "they found an exponential, we found a power law".
`paper-prd.tex` line 41:

> "Sahay, Lukin, and Cotler~\cite{SahayLukinCotler2025} demonstrated that pairs of hologrons
> experience an attractive force **$V(\dr) \sim \exp(-\dr/\xi)$**"

and line 229:

> "MERA hologron forces **$V(\dr) \sim C_1 - C_2 \exp(-\dr/\xi)$**"

`\dr` is defined at `paper-prd.tex:11` as `\newcommand{\dr}{\mathrm{d}r}` and is used throughout the
paper as the **boundary lattice separation** between the two probes. But SLC's exponential is in
**|ρ₁ − ρ₂|, a bulk radial/hyperbolic coordinate**. The project's own catalogue has this right —
`research/data/papers/PAPER-2026-009.json` `key_claims` reads "V_TN(|rho1-rho2|) ~ C1 - C2 *
exp(-|rho1-rho2|/l_AdS)" — while the manuscript substitutes the boundary variable. Since bulk radial
distance in a MERA is logarithmic in boundary separation, an exponential in ρ *is* a power law in
boundary separation; the manuscript itself says so at line 529 ("d_geo = 2 ℓ_AdS ln(dr) in the MERA,
giving G ~ dr^{−2m ℓ_AdS}"). **The "exponential vs power law" contrast is therefore an artifact of
mis-transcribing the prior work's independent variable, and the manuscript simultaneously contains
the derivation that dissolves it.** This is the load-bearing sentence of the differentiation
argument at line 552 ("Our boundary-primary interaction energy F(dr) ~ dr^{−3.92} follows a power law
rather than an exponential"). **Defect, major.**

### 3.5 Derivation gate: is α = 4 fixed in advance?

The project answers this itself. `paper-prd.tex` line 552: "**The CFT conformal Ward identity
predicts α = 2Δ_T = 4 exactly for stress-tensor exchange**". `docs/governance/PROJECT-REVIEW-2026-08-11.md`
§3 Bin 1: "α = 2Δ_T = 4 across Ising/TCI/Potts is fixed by conformal symmetry (Δ_T = 2 in *every*
2D CFT)… Excellent *pipeline validation*, near-zero *discovery*." I agree, and add that Δ_T = 2 is
also the calibration input for v_T in the C_TTT pipeline (§2.4 above), so the same number is doing
double duty as assumption and as result across two targets.

**Counterfactual novelty: near-zero.** Before the run, the possible outcomes were "≈4" or
"implementation/observable is wrong". The measured 3.92 ± 0.16 is a 0.5σ agreement with a
pre-determined value.

### 3.6 Adjacent prior art the project's scans missed

`arXiv:2607.06511`, "Static vacancies as parametrized conformal defects in the critical J₁–J₂
transverse-field Ising chain", R. L. Silva, R. C. Silva, R. J. C. Lopes, A. R. Pereira, submitted
2026-07-07. DMRG on chains up to 300 sites; measures the **Casimir-like interaction energy between
two static defects in a critical Ising-class chain** and fits |Δ_b(r)| ~ r^{−α} with
α_∞ ≃ 1.070 + 0.091 J₂/J₁, described as "close to the universal Casimir value of unity".

This is the same *observable class* (interaction energy between two local perturbations of a critical
chain, fitted to a power law) at 300 sites — an order of magnitude beyond the project's 24. The
exponent differs (their defect is a vacancy = a conformal defect, not a primary-operator insertion),
so it is **not** a novelty kill; it is a directly relevant methods benchmark and a much larger
system-size precedent. A grep of `research/data/papers/` and `research/digests/` returns no record of
it: the 2026-07-07 submission date places it in the scan-#15 window (2026-07-02 → 2026-07-14), which
catalogued PAPER-135/136 only. **Scan miss.**

Also relevant and uncatalogued as prior art for the observable: Chua, Passias, Tiwari & Ryu,
"Holographic dynamics from multiscale entanglement renormalization ansatz", PRB 95, 195152 (2017),
arXiv:1611.05877 — the paper that introduced hologrons, their bulk Hamiltonian and multi-hologron
sectors. (`research/data/papers/PAPER-2026-010.json` cites "Chua et al. 2017" inside its
`hologron_instability_mechanism` field, so the project knows of it, but there is no PAPER record.)

### 3.7 Independence ledger (§7)

| Field | Value |
|---|---|
| Side A | F(dr) from exact 24-qubit ED of the critical TFIM |
| Side B | α = 2Δ_T = 4, a conformal-symmetry consequence |
| Shared theory | Δ_T = 2; the boundary-primary operator σ_j, itself taken from Zou–Milsted–Vidal 2020 |
| Shared with prior work | observable (Wang & He), operator (ZMV 2020), mechanism (SLC) |
| Independent info | the 12-point profile and its fit window |
| **Classification** | **Primarily a consistency check**, and one whose fit window is contested — inv-sims-early records that dropping dr=2 moves α to 2.56/2.75/2.75 across the three evaluations. |

### 3.8 Verdict

**Novelty largely eliminated.** The mechanism is published (SLC), the observable is published
(Wang & He), the operator is published (ZMV 2020), and the exponent is fixed by conformal symmetry
(the project's own statement). What remains is a longer separation profile and a fit — and the fit is
the item inv-sims-early shows to be unstable. Level 1 with a Level-2 sliver at best.

**Required corrections before any further submission:**
1. Cite Wang & He 2501.03084 at Eq. (eq:Fdr) and delete "We identify the correct observable".
2. Correct the SLC potential's independent variable from `\dr` to the bulk radial coordinate at
   `paper-prd.tex` lines 41 and 229, and withdraw the "exponential vs power law" differentiation at
   line 552 or restate it in the coordinates that make it true.
3. Catalogue 2607.06511 and 1611.05877.

---

## 4. TARGET 4 (CRITICAL) — MERA-as-geometry discrimination: has the flagship already been run?

**Question as posed:** has anyone already run matched-control / rewiring experiments testing whether
MERA geometry has operational content beyond the CFT data?

**Short answer: no published *matched-control numerical rewiring experiment* of the kind
RESEARCH-DIRECTOR §10/§11-H specifies was found. But the flagship as currently conceived is aimed at
a question the literature has already answered analytically, and answered against the project's
premise.** The flagship is not pre-empted; its *premise* is.

### 4.1 The finding that matters most: MERA's geometry is already derived, and it is not AdS

**Milsted & Vidal, "Geometric interpretation of the multi-scale entanglement renormalization
ansatz", arXiv:1812.00529 (3 Dec 2018).** Abstract findings, as retrieved:

> "MERA on the real line (and finite circle) can be given a **rigorous interpretation as a
> two-dimensional geometry, namely a light sheet (respectively, a light cone)**." …
> "**MERA describes neither the hyperbolic plane nor de Sitter spacetime**", though generalisations
> corresponding to path integrals on those geometries are proposed.

This sits on their path-integral-geometry framework (Milsted & Vidal, "Tensor networks as path
integral geometry", arXiv:1807.02501; "Tensor networks as conformal transformations",
arXiv:1805.12524).

**Why this is the single most consequential item in this report.** The project's entire geometric
layer — ℓ_AdS = 1/log 2, d_geo = 2ℓ_AdS ln(dr), "AdS null geodesic" transport T = (π/2)ℓ_AdS, "the
MERA geometry encodes the full causal structure of AdS" (`paper-prd.tex` line 538) — presupposes that
the MERA *is* a discretisation of a hyperbolic/AdS slice. Guifré Vidal, who created the MERA,
published a derivation five years before this project began that it is not. Note that Evenbly
(co-author of the analytic tensors the project uses, `SIM-2026-011.json` field
`circuit.tensor_source`: "Evenbly & White 2016") and Vidal are also two of the seven outreach targets
who did not reply.

I found **no** record of 1812.00529, 1807.02501 or 1805.12524 in `research/data/papers/`
(grep for `1812.00529|1805.12524|1807.02501` returns only three `.md` scratch files and
`PAPER-2026-010.json`, which cites ZMV inside its own text). The manuscript's bibliography does not
cite them (`research/submission-package/prd/references.bib`). **A PRD referee in the
gauge/gravity-duality section will know this paper.**

### 4.2 The published no-go on AdS/MERA

**Bao, Cao, Carroll, Chatwin-Davies, Hunter-Jones, Pollack & Remmen, "Consistency conditions for an
AdS/MERA correspondence", PRD 91, 125036 (2015), arXiv:1504.06632.** Abstract, verbatim:

> "…we investigate this proposal and derive necessary conditions for it to apply, using geometric
> features and entropy inequalities that we expect to hold in the bulk. We show that, perhaps
> unsurprisingly, **the MERA lattice can only describe physics on length scales larger than the AdS
> radius. Further, using the covariant entropy bound in the bulk, we show that there are no
> conventional MERA parameters that completely reproduce bulk physics even on super-AdS scales.**
> We suggest modifications or generalizations of this kind of tensor network that may be able to
> provide a more robust correspondence."

This is a Level-4-style negative result (§5) obtained analytically in 2015. Also uncatalogued.

### 4.3 Architecture-variation and representation-dependence prior art

These are the closest published things to "rewiring experiments", and they matter for §11-H and §33–34:

| Work | What it does | Relation to the proposed flagship |
|---|---|---|
| Evenbly, "Hyper-invariant tensor networks and holography", PRL 119, 141602 (2017), arXiv:1704.04229 | Constructs an alternative network built on a *uniform tiling of hyperbolic space*, "without inherent directionality or preferred locations in the holographic bulk, and thus circumvent[ing] key arguments made against the MERA as a model for AdS/CFT", while retaining algebraic correlations and variational freedom | **This is an architecture-variation experiment already published.** It establishes that the MERA's directionality/preferred-location structure is an artifact removable by rewiring — i.e. part of the answer §11-H seeks |
| Czech, Nguyen & Swaminathan, "A defect in holographic interpretations of tensor networks", JHEP 03(2017)090, arXiv:1612.05698 | Deforms the CFT (defects, interfaces, boundaries) and asks which tensors must update; finds "**even identical tensors can contribute differently to estimates of entanglement entropies**"; proposes "rayed MERA" | This is §11-E (response to defects and deformations) already executed at the level of network structure vs. holographic geometry |
| Singh, "Tensor network state correspondence and holography", arXiv:1701.04778 | Analyses when a TN admits a holographic reading | Retrieved statement: "**a given MERA representation can be interpreted in dual (even several) ways**" — directly on §33's "can different networks represent the same state with incompatible internal geometries?" |
| Bény, "Causal structure of the entanglement renormalization ansatz", NJP 15, 023020 (2013) | Argues MERA's causal structure is de Sitter-like | A *competing geometric reading of the same network*, which is itself evidence that the geometric label is under-determined |
| Vidal *et al.*, "MERA as a holographic strange correlator", arXiv:1812.11644 | Re-reads the MERA as the overlap of a 2D short-range-entangled state with a product state; derives a quantum-corrected RT formula | Yet another inequivalent geometric reading |
| Hayden, Nezami, Qi, Thomas, Walter & Yang, "Holographic duality from random tensor networks", arXiv:1601.01694 | Random tensor networks reproduce RT | Supplies the natural **non-geometric / randomised matched control class** the flagship needs |
| Jahn & Eisert, "Holographic tensor network models and quantum error correction: a topical review", QST 6, 033002 (2021), arXiv:2102.02619; Jahn *et al.*, "Boundary theories of critical matchgate tensor networks", arXiv:2110.02972 | Systematic study of what boundary theories hyperbolic TNs actually produce | Establishes that matching *some* CFT data does not imply matching the CFT — the exact logic §10 needs |

**Net:** the ingredients of the flagship exist in the literature as separate published pieces
(architecture variation: Evenbly; deformation response: Czech *et al.*; representation-dependence:
Singh, Bény; control class: random TNs). What does **not** exist, so far as I could find, is the
assembled experiment: *construct MERA and a matched non-geometric ansatz agreeing on ground-state
energy, scaling dimensions, entanglement entropy and bond dimension, then test whether a nominated
geometric observable separates them.*

### 4.4 Does the project already have such a control? No.

Two things in the repository are described in control language; neither is a matched control in the
§10 sense.

1. **`paper-prd.tex` line 179** — the "TFIM control": "To confirm that the transport time T = 2.25 is
   specific to the MERA geometry … we perform the same transport experiment on the standard periodic
   TFIM at criticality (g = 1.0), **without the MERA-derived boundary Hamiltonian**. The TFIM ring
   yields T_TFIM = 3.8 — 69% larger…". This compares two *different Hamiltonians with different
   boundary conditions and different normalisations*; nothing is matched. It cannot distinguish
   "MERA geometry has content" from "these are two different chains". Note also that Wang & He's H_∂
   is *unitarily equivalent* to the critical Ising chain via their V (PAPER-2026-010,
   `stable_excitation_construction.step1_find_V`), so a large part of the difference is a change of
   basis and normalisation, not of geometry. `paper-prd.tex` line 556 nonetheless bills this as
   "the TFIM control experiment confirming MERA-specificity". **Overclaim.**

2. **`research/RESEARCH-LOG.md` line ~361** — the "DISENTANGLER-MATTERS discriminator": the ascending
   superoperator spectrum with the real disentangler differs from u = identity, "proving u is NOT
   gauge-absorbable". This is a correct and useful *implementation* gate; it is also the defining
   property of MERA versus a tree tensor network (Vidal 2007) and says nothing about whether the
   emergent geometry has operational content.

So the flagship has not been run internally either. The project's most recent state document lists no
geometry-discrimination task: `NEXT-SESSION.md` "Next-session menu" items 1–4 are Phase-3
interpretation, puMPS sharpening of c_KS, paper-v6 planning, and scan #20.

### 4.5 What the flagship must do differently to be publishable

Given §4.1–4.3, a defensible flagship cannot be framed as "does MERA encode AdS geometry?" — that
framing is answered (Bao *et al.*: not consistently; Milsted & Vidal: it is a light sheet). Three
reframings that are *not* pre-empted by anything I found:

1. **Take Milsted–Vidal's light-sheet/light-cone geometry as the null hypothesis, not AdS.** Ask
   whether any project observable distinguishes the light-cone reading from the AdS reading. The
   transport result T = (π/2)ℓ_AdS is the obvious candidate, since a light-cone geometry makes its
   own causal-propagation prediction. This is a genuinely open, high-counterfactual-novelty question
   and it uses machinery the project already has.
2. **Run the assembled matched control that the literature has only in pieces:** MERA vs. a random
   tensor network vs. a hyperinvariant network (Evenbly) vs. a tree tensor network, all optimised to
   matched E₀, Δ_σ, Δ_ε, S(ℓ) and bond dimension, and test one nominated geometric observable across
   all four. Prior art supplies the control classes but not the comparison.
3. **Gauge-invariance test (§34):** apply a nontrivial bond gauge transformation to a converged MERA
   and recompute every geometric diagnostic the project uses (ℓ_AdS, d_geo, transport time, force
   exponent). Anything that moves is a representation property. Singh's "dual (even several)
   readings" makes this a live question; I found no paper that runs it numerically for the project's
   specific diagnostics.

Each of these has a clean killer (§12): (1) dies if the light-cone and AdS readings predict the same
transport time; (2) dies if the matched controls reproduce the observable; (3) dies if every
diagnostic is gauge-invariant (which would be a positive result, and interesting).

### 4.6 Verdict

**Not already done — but the current framing is refuted by published work the project has not
catalogued.** The flagship is worth pursuing *after* the premise is repaired. Until 1812.00529 and
1504.06632 are read, catalogued, and answered in writing, any geometry claim in the project is
exposed to a one-paragraph referee rejection.

---

## 5. Cross-cutting defects surfaced by this literature pass

### 5.1 The direct methodological ancestors are not in the paper catalogue

`grep -rl "1710.05397|1901.06439|1706.01436|1812.00529|1805.12524|1807.02501" research/data/papers/`
returns four files, of which only one is a structured record (`PAPER-2026-010.json`, a Wang & He
record that merely *cites* ZMV in its `stable_excitation_construction.step2_sigma_C-Ising` field).
There is **no PAPER record for any of**:

| arXiv | Paper | Why it must be catalogued |
|---|---|---|
| 1706.01436 | Milsted & Vidal, PRB 96 245105 | Source of the estimator, the T-identification rule, the contamination rationale, and published c for Ising **and 3-state Potts** |
| 1710.05397 | Zou, Milsted & Vidal, PRL 121 230402 | The vendored codebase; published c at the OF/TCI point |
| 1901.06439 | Zou, Milsted & Vidal, PRL 124 040604 | Source of the boundary-primary operator the force result uses; published lattice OPE coefficients |
| 1812.00529 | Milsted & Vidal | MERA is a light sheet, not the hyperbolic plane — refutes the project's geometric premise |
| 1504.06632 | Bao *et al.*, PRD 91 125036 | Published AdS/MERA no-go |
| 1611.05877 | Chua, Passias, Tiwari & Ryu, PRB 95 195152 | Origin of hologrons and their interactions |
| 2607.06511 | Silva *et al.* | Defect-interaction power law in a critical Ising chain at 300 sites; scan-#15 miss |

The catalogue is the project's literature-gate instrument (§8). Seven absences, four of them the
project's own methodological parents, is a systemic gate failure, not a bookkeeping lapse.

### 5.2 Duplicate PAPER records for Sahay–Lukin–Cotler

`research/data/papers/PAPER-2026-003.json` and `research/data/papers/PAPER-2026-009.json` are both
records for arXiv:2401.13595 (both carry `"arxiv_id": "2401.13595"` and the same title "Emergent
Holographic Forces from Tensor Networks and Criticality"). Neither has an `alias_of` field. This
violates `CLAUDE.md` → "Catalogue Rules" → "Duplicate records become alias stubs (`alias_of` field),
never silent deletions." Minor, but it is the same dedup failure the rules were written to prevent.

### 5.3 A published, working estimator was declared "DEAD" on the basis of a local implementation

`NEXT-SESSION.md` task 5, verbatim:

> "Also DEAD (tested 07-20): c = 2||H_-2|0>||^2 ground-state-only route (**UV-divergent, c grows
> ~0.5N**)"

That route is Milsted & Vidal 1706.01436 **Eq. (21)**, and their Figure 4 shows it converging: Ising
c(N) running over roughly 0.50–0.56 for N = 8…18 and Potts c(N) over roughly 0.80–0.90 for N = 8…14,
both extrapolating linearly in 1/N² to 0.4995 and 0.7985. It does not grow like 0.5N. MV Section IV.A
also specifies the normalisation that Eq. (21) requires (their Eq. (20): H = aH̃ + Nb, with
a = (4π/N)/(Ẽ_T − Ẽ_I) fixed by Δ_T = 2, and the extensive constant b removed). The most likely
explanation for "c grows ~0.5N" is an unsubtracted extensive term — i.e. a missing `b`.

**This is a live scientific defect, not just a novelty issue.** The project retired a published
estimator, and with it the natural independent-code-path cross-check on its own headline c values
(RESEARCH-DIRECTOR §19 "independent implementation"; §13 "independent code-path reproduction"),
because of an unrecognised normalisation error. It should be re-run against MV Fig. 4 before any
methods paper is written.

### 5.4 An unsupported novelty phrase is already in a state document

`NEXT-SESSION.md` line 36, verbatim:

> "First lattice extraction of a negative c from stress-tensor elements (**to our knowledge**)."

§8 forbids exactly this phrase until the evidence is recorded. The Yang–Lee literature gate belongs
to a sibling agent this phase; I flag the wording only, and note that the same document carries the
claim into the "HYP-028 → SUPPORTED (medium)" line that feeds memory and the hypothesis record.

### 5.5 The manuscript's only citation to the lattice-CFT foundation is mis-titled and incomplete

`research/submission-package/prd/references.bib` (227 lines) contains **no entry** for Milsted &
Vidal 1706.01436, Zou–Milsted–Vidal 1710.05397, Milsted & Vidal 1812.00529, or Bao *et al.*
1504.06632. The single entry touching this literature is, verbatim, lines 102–107:

```bibtex
@article{ZouMilstedVidal2020,
  author    = {Zou, Yijian and Milsted, Ashley and Vidal, Guifr\'e},
  title     = {Boundary operators in {MERA}},
  journal   = {Phys. Rev. Lett.},
  year      = {2020}
}
```

The cited work's actual title is **"Conformal Fields and Operator Product Expansion in Critical
Quantum Spin Chains", Phys. Rev. Lett. **124**, 040604 (2020), arXiv:1901.06439** (verified via APS
listing for PRL vol. 124 issue 4). "Boundary operators in MERA" does not appear to be a paper by
these authors. The entry also carries no volume, no page, no DOI and no eprint.

This is the citation that sources the boundary-primary operator σ_j on which the entire force result
rests (`paper-prd.tex`, "The boundary-primary operator is~\cite{ZouMilstedVidal2020}"). It is
consistent with the four bibliography defects reported in
`research/data/audit/raw/inv-manuscript-claims.md`; I record it here because of *which* citation it
is — the load-bearing one for Target 3.

### 5.6 Δ_T = 2 is simultaneously a calibration input and a claimed result

Recorded in §2.4 above; repeated here because it spans targets. `SIM-2026-068.json` `method`:
"v_T calibrated from Delta_T=2 (exact in any CFT)". `MEMORY.md` hypothesis table, HYP-027:
"Δ_T=2.007→α=4.01" is quoted as a measurement supporting universality. Both cannot be true of the
same pipeline run. (Note: SIM-2026-051/052 use the MERA scaling-superoperator route, where Δ_T is
read from an eigenvalue and *is* measured; SIM-2026-067/068/069 use the KS route, where it is
assumed. The records do not distinguish these two provenances when the number is quoted.)

---

## 6. Consolidated independence ledger (§7)

| Comparison | Side A | Side B | Shared inputs | Classification |
|---|---|---|---|---|
| C_TTT(Ising/TCI/Potts) vs 2√2/√c | KS elements from vendored ZMV puMPS | Virasoro identity | Δ_T=2 calibration; ZMV code; ZMV model builders; ZMV estimator | **Algebraically equivalent** |
| Three rungs of the ladder vs each other | rung *i* | rung *j* | one pipeline, one estimator, one codebase; only the model builder differs | **Structurally dependent** |
| Project c vs published c | this project | MV 1706.01436 / ZMV 1710.05397 | same estimator, same models, same code for 2 of 3 | **Primarily a consistency check** (and lower precision on 2 of 3) |
| α=3.92 vs 2Δ_T=4 | 24q ED interaction energy | conformal symmetry | Δ_T=2; ZMV-2020 boundary primary | **Primarily a consistency check** |
| Project force vs Sahay–Lukin–Cotler | boundary chain, no MERA | MERA bulk, ρ coordinate | same mechanism (stress-tensor exchange), same universality class | **Partially independent** (different setups, same physics claim) |
| Project force vs Wang & He | 12 separations, exact 24q chain | 4 separations, MERA-mapped states | **identical observable and identical operator** | **Structurally dependent** |
| L₂ε suppression claim vs literature | this project's element ratios | MV Eq. (22) rationale, ZMV N^−2 law | same estimator, same code | **Primarily a consistency check** |

---

## 7. UNVERIFIED

Explicit, per instruction — silence is not a pass.

1. **Semantic Scholar was unavailable.** Both `api.semanticscholar.org/graph/v1/paper/search` calls
   returned HTTP 429. The §8 literature gate names Semantic Scholar explicitly; that index was
   therefore not swept. Recommend a retry with backoff before any novelty claim is finalised.
2. **INSPIRE and Crossref were not searched** (§8 names both). Out of budget this pass.
3. **arXiv export API deliberately not used** (assigned to a sibling agent this phase). A systematic
   in-window sweep for 2025–2026 work on lattice C_TTT or MERA-geometry controls has therefore not
   been done by me; my coverage of 2025–2026 rests on WebSearch, which is not exhaustive.
4. **Sahay–Lukin–Cotler full text read via ar5iv only.** The PRX page returned HTTP 403 and
   `arxiv.org/pdf/2401.13595v2` returned 404. The quoted formulae (Ṽ_TN, the b_AdS·(C_T+C_T̄)
   expression, the "gravitational attraction" sentence) come from an ar5iv rendering summarised by
   WebFetch's model, cross-checked against the project's own `PAPER-2026-009.json` `key_claims`,
   which agree on C₁, C₂, ℓ_AdS⁻¹ and the ρ-dependence. **I did not read the PRX PDF directly.**
   The one claim I would most want re-verified from the published PDF is the sentence attributing
   the attractive part to stress-tensor/graviton exchange, since §3.3's verdict leans on it.
5. **Milsted & Vidal 1812.00529 read from the arXiv abstract page only**, via WebFetch. I did not
   read the body. The claim "MERA describes neither the hyperbolic plane nor de Sitter spacetime" is
   quoted from that page and is corroborated by two independent WebSearch summaries, but I have not
   verified the scope conditions of the theorem (e.g. whether it applies to the binary MERA the
   project uses, or under what continuum limit). **This is the highest-leverage item in the report
   and it deserves a direct full-text read before it is acted on.**
6. **Whether ZMV ever published a c value for the 3-state Potts chain.** 1710.05397 states only
   "we have also tested the validity of the ansatz in the 3-state and 4-state Potts models"
   (extracted text, lines 1416–1418) without a Potts entry in Table I. The published Potts c I cite
   (0.7985) is Milsted & Vidal 1706.01436 Fig. 4, by ED at N = 8…14. I did not search Zou's later
   papers (e.g. arXiv:2104.00103) or his thesis for a puMPS Potts c.
7. **Zou–Milsted–Vidal 1901.06439 (PRL 124, 040604) was not read.** It is the source of the boundary
   primary operator and of published lattice OPE coefficients; whether it contains C_σσε = 0.5 as a
   measured lattice value (which would bear on the project's SIM-061/064 claim) is **not established
   by me** and is flagged for whichever agent owns the OPE target.
8. **The "N^−0.2" foil.** I searched for a published claim that L₂ε contamination decays as N^−0.2
   and found none, but absence of evidence over a handful of queries is weak. What I can state
   positively is that the *published* finite-size law for c in these models is N^−2 (§1.3).
9. **The C_TTT = 2√2/√c algebra in §2.1 is my own two-line derivation** from standard ⟨TT⟩ and
   ⟨TTT⟩ normalisations. I did not locate a paper that writes "2√2/√c" verbatim; the searches for
   that literal string returned nothing on point. The derivation is elementary and I am confident in
   it, but it is not a citation.
10. **Wang & He's U_int is computed on MERA-mapped bulk states** (|Ψ_{j,j′}⟩ = U†σ_jσ_{j′}U|Ψ_GS⟩)
    while the project's F(dr) is computed directly on the boundary chain. I assert these are the
    "same observable"; strictly they are the same *formula* applied to states related by the MERA
    isometry U. Whether the two coincide numerically is not something I tested.
11. **I did not verify the claim in `paper-prd.tex` line 206/538 that Wang & He analytically proved
    t_trans = π** — inv-manuscript-claims already reports that this is absent from the project's own
    record of the cited paper. I did not re-check it and defer to that agent.

---

## 8. Search log

Queries and endpoints, so this pass is reproducible and its gaps auditable.

**WebSearch (11 queries):** ZMV puMPS/Koo-Saleur; Milsted-Vidal geometric interpretation of MERA;
Grans-Samuelsson/Jacobsen/Saleur Virasoro in spin chains; lattice C_TTT stress-tensor three-point;
MERA geometry gauge dependence / rewiring / operational content; Chua-Passias-Tiwari-Ryu hologron
interaction power law; Evenbly hyperinvariant tensor networks; "Emergent Holographic Forces…" PRX;
interaction energy of two local excitations / critical Casimir; bulk locality MERA reconstruction;
Swingle criticism / MERA-not-AdS; Jahn-Eisert review; Zou-Vidal Potts; ZMV OPE paper; MERA-vs-MPS
matched control; MERA as strange correlator; "same state different network different geometry".

**WebFetch:** arxiv.org/abs/1812.00529; ar5iv 1710.05397; arxiv.org/abs/1706.01436;
arxiv.org/abs/1504.06632; arxiv.org/abs/1612.05698; arxiv.org/abs/2401.13595; ar5iv 2401.13595;
arxiv.org/abs/2607.06511; arxiv.org/abs/2512.19452; journals.aps.org PRX 15 021078 (**403**);
arxiv.org/pdf/2401.13595v2 (**404**); Semantic Scholar API ×3 (**429**).

**paper-search MCP:** `download_arxiv` 1710.05397, 1706.01436 (both then text-extracted locally with
`pypdf` and read/grepped in full); `search_google_scholar` (returned non-physics noise — not usable).

**Local:** `research/data/papers/2501.03084.pdf` text-extracted and searched;
`research/tools/pumps-setup/{qw_cttt_of.jl, qw_cttt_potts3.jl, VENDOR.md, *.jsonl}`;
`research/submission-package/prd/{paper-prd.tex, references.bib}`; SIM-2026-011,
SIM-2026-011-interaction, SIM-2026-067/068/069; PAPER-2026-003/009/010; `NEXT-SESSION.md`;
`docs/governance/PROJECT-REVIEW-2026-08-11.md`; `research/RESEARCH-LOG.md`.

**Scratch artifacts** (not in the repo):
`C:\Users\jonca\AppData\Local\Temp\claude\D--quantum-worldline\0ca162cd-b7ba-4d61-b1c4-b747de77b26f\scratchpad\`
→ `1710.05397.pdf`, `zmv.txt`, `1706.01436.pdf`, `mv2017.txt`, `wanghe.txt`.

---

## 9. Recommended actions, ranked by leverage

1. **Read 1812.00529 in full and write a theory record answering it** (§14 wants
   `research/data/theory/` repaired; this is the record to start it with). Every geometric claim in
   the program depends on the answer.
2. **Add the seven missing PAPER records** (§5.1). Two of them (1706.01436, 1710.05397) contain the
   published values of the project's own headline numbers.
3. **Re-label SIM-2026-067/068/069** from "C_TTT measured" to "central charge reproduced; C_TTT via
   the Virasoro identity", and add a `prior_art` field to each carrying the published c values.
4. **Fix the three manuscript defects in §3.8** before PRD referee reports arrive; the SLC
   independent-variable error is the one a referee is most likely to catch unaided.
5. **Re-run MV Eq. (21)** with the correct normalisation and retract the "DEAD" verdict in
   `NEXT-SESSION.md` task 5, or record why it genuinely fails here when it worked for MV.
6. **Redesign the flagship** around one of §4.5's three reframings, each of which has a named killer.
7. **Retry Semantic Scholar / INSPIRE / Crossref** to close the gate properly (§7 UNVERIFIED items
   1–3).
