# adv:derivation-gate — Analytic Theorist / Derivation Gate

**Auditor task:** `adv:derivation-gate` (RESEARCH-DIRECTOR §8 "Derivation gate", §27 "Analytic theorist").
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` — §5 (four contribution levels),
§6 (counterfactual novelty), §7 (independence ledger), §8 (novelty gates), §12 (killer tests),
§15 (claim dependency chains), §16 (no-go results), §24 (PRD referee prep), §38 (audit assignment).
**Date:** 2026-08-17. **Repo state:** branch `public-release`, HEAD `9470d69`.
**Scope:** pure theory. No literature search was performed (that is `adv:literature`'s task); every
statement of "known result" below is an algebraic identity I derive in place, not a citation claim.

All paths are repo-relative to `D:/quantum-worldline/`.

---

## 0. Executive summary

I applied the §8 derivation gate — *"is the number fixed by symmetry? is it a direct Virasoro
identity? is it determined by a known operator algebra? does it follow algebraically from a
previously extracted parameter? is the numerical experiment only checking whether the
implementation works?"* — to every quantitative claim the project makes.

**Headline:** of the eight headline quantities, **seven are algebraically forced** once their own
stated assumptions are granted. The single most important finding is that this includes the
project's strongest frontier claim:

> **Given that the Koo–Saleur lattice operators converge to Virasoro generators under the
> biorthogonal (bilinear/Shapovalov) pairing, and given the correct identification of the
> conformal vacuum |1⟩ and its level-2 descendant L₋₂|1⟩, the product-form estimator returns
> `c` and cannot return anything else. `c = −22/5` rather than `c_eff = +2/5` is a two-line
> consequence of ⟨L₋₂1, L₋₂1⟩ = c/2. `c_eff` has no algebraic expression anywhere inside the
> vacuum Virasoro module — it is the spectrum-wide combination c − 24h_min and appears only in
> Casimir energies. The "discrimination" between c and c_eff was therefore not a contest between
> two live outcomes of this estimator: c_eff was never on its menu.**

That is **not** a verdict that SIM-071 is worthless. What the experiment *did* test — and what the
algebra emphatically did **not** guarantee — is (i) that the Koo–Saleur correspondence extends at
all to a non-Hermitian chain with η = P pairing, (ii) that the identity module and its L₋₂
descendant are findable on a finite non-Hermitian lattice, and (iii) that module mixing does not
destroy the identification. Item (iii) came back *adverse-leaning and informative*: the unitary
discriminator inverts, and the identification survives only on injected M(2,5) theory input.
Full derivation and the exact partition of "forced" vs "at risk" is §9, which is the longest
section of this document by design.

Second-order findings, each derived and verified numerically in-place:

1. **α = 2Δ_T = 4 is fixed by conformal symmetry in every 2D CFT, unitary or not** — the project
   says so itself in `SIM-2026-051.json` (verdict: *"Δ_T=2 in every unitary 2D CFT … so α=2Δ_T=4
   must hold at any 2D critical point. The numerics confirm the symmetry argument."*). The claimed
   *universality across three classes* has **exactly zero** counterfactual novelty, and at TCI and
   Potts **no force was measured at all** — α is obtained by multiplying a measured Δ_T by 2.
2. **The genuinely non-trivial half of the α claim is the channel argument, not Δ_T** — and the
   channel argument is Ising-specific. At TCI the fusion ε×ε = 1 + ε′ puts a **Δ = 6/5 scalar
   below T**, predicting α = 12/5 = 2.4, not 4. The project's own universality claim is therefore
   *weaker* than symmetry at TCI, not stronger. §3.4.
3. **The recorded 24-qubit F(dr) has no power-law plateau** (independently re-derived here: local
   exponent runs 2.04, 4.23, 2.60, 2.46, 2.46, 2.53, 2.66, 2.84, 3.10, 3.48, 4.06). §3.6.
4. **C_TTT = 2√2/√c is a Virasoro identity and is computed as a literal line of code in every
   driver.** Quoting C_TTT instead of c **halves the apparent error** — verified: the error ratio
   is 0.5010 / 0.5008 / 0.5005 at Ising / TCI / Potts. §4.
5. **m_eff = 0.693 is `ln 2` by construction**, not a measurement: it equals 1/l_AdS with
   l_AdS = 1/ln χ fixed by architecture. The comparison "0.693 vs 0.670 = 3.5%" reduces exactly
   to "ξ_MERA = l_AdS²", i.e. 2.154 vs 2.0814. **The same model applied to the project's better
   dataset (SIM-011, 24q exact, 11 points) gives m_eff = 2.29 — 230% off.** §8.
6. **T = (π/2)·l_AdS is a genuinely parameter-free prediction** (the one place in the manuscript
   where nothing is fitted) — but the π/2 was **selected after the measurement** to replace a
   π that overshot by exactly the observed factor of 2, and the manuscript's own cited external
   confirmation states π, not π/2, with no reconciliation. §7.
7. **The `(L/2πv_T)²` prefactor in the Yang-Lee estimator carries no information.** Because
   `v_T` is *defined* by imposing Δ_T = 2, the estimator reduces identically to
   `c_KS = 8·prod/(E_T − E_vac)²`; L and v_T cancel. §9.5. The same substitution means **Δ_T is
   not measured in P3 or P4 at all** — only in P1 and P2.
8. **HYP-028's founding premise is false as written.** `HYP-2026-028.json` (`claim`) asserts
   *"In a non-unitary CFT the Δ_T = 2 protection is NOT guaranteed."* It is guaranteed: T is the
   spin-2 conserved current whose dimension equals d = 2 by conservation, in any 2D CFT with a
   stress tensor; and M(2,5) is a non-logarithmic minimal model, so the Jordan-block escape the
   record invokes does not apply to the model it chose. The manuscript gets this right
   (`paper-draft-scipost.tex:617`); the hypothesis record does not. §9.10.

**One recommendation stands above the rest** (§12): the project abandoned a measurement with
*genuinely high* counterfactual novelty in favour of one with near-zero. Yang-Lee fusion is
φ × φ = 1 + φ with Δ_φ = **−2/5**, so a φ-channel force at the Yang-Lee point should
**grow** as dr^{+4/5} rather than decay as dr^{−4}. HYP-028's own step 6 pre-registered exactly
this comparison. It was never run. It is cheap, it reuses the existing biorthogonal ED, and
several outcomes are physically meaningful.

---

## 1. Method and scoring scale

For each claim I ask §8's five questions and assign one of four **derivation-gate grades**:

| Grade | Meaning | §6 counterfactual novelty | §5 level |
|---|---|---|---|
| **FORCED** | The number follows from symmetry / a Virasoro identity / a fixed operator algebra. Only "implementation works" or "implementation fails" was possible. | near-zero | 1 |
| **FORCED-CONDITIONAL** | Forced *given* stated assumptions that are themselves non-trivial and were at risk. The number is guaranteed; the *applicability* was not. | low for the value, moderate for the assumption | 1 for the number, 2 for the method |
| **ALGEBRAIC-TRANSFORM** | Not measured; computed as a closed-form function of a previously extracted parameter. | zero (it is the same measurement, re-expressed) | not a separate result |
| **AT RISK** | Multiple physically meaningful outcomes were available before the run. | moderate–high | 2–4 |

A claim can decompose: e.g. "α = 4 is universal" splits into a FORCED part (Δ_T = 2) and an
AT-RISK part (which operator dominates the probe channel) that was never tested.

I derive every identity in place rather than asserting it, so that a referee can check the
algebra without leaving this document.

---

## 2. Master derivation-gate table

| # | Claim | Where recorded | §8 verdict | Grade |
|---|---|---|---|---|
| C1 | Δ_T = 2 (Ising, TCI, Potts) | `SIM-2026-050/051/052/062/063` | Fixed by conformal symmetry: T is the spin-2 conserved current, Δ_T = d = 2 in **every** 2D CFT | **FORCED** |
| C2 | α = 2Δ_T = 4 | same + `paper-draft-scipost.tex:45` | Algebraic doubling of C1. **No force measured at TCI or Potts.** | **ALGEBRAIC-TRANSFORM** of C1 |
| C3 | α = 4 is *universal* across c = 1/2, 7/10, 4/5 | abstract L45; `SIM-2026-051` verdict | The project's own verdict states it "must hold at any 2D critical point" | **FORCED** |
| C4 | The Ising force channel is T (ε×ε = [1]) | `paper-draft-scipost.tex:45,577` | Correct *for a pure-ε probe*; channel purity never established | **AT RISK, untested** |
| C5 | The TCI/Potts force channel is also T | asserted implicitly by C3 | **False at TCI**: ε×ε = 1 + ε′ with Δ_{ε′} = 6/5 < 2 | **AT RISK, contradicted** |
| C6 | α = 3.92 ± 0.16 measured at 24q | `SIM-2026-011-interaction.json:fits.F_avg_dr_ge2` | A fit-window artifact; no plateau exists in the data | **AT RISK, adverse** |
| C7 | Δ_σ, Δ_ε at three classes | `SIM-2026-052/061/063` | Kac formula; exact rationals | **FORCED** |
| C8 | C_σσε = 0.50 ± 0.03 | `SIM-2026-061.json:15` | Exact Ising structure constant = 1/2 | **FORCED** |
| C9 | C_σσσ = 0 (exactly) | `SIM-2026-061.json:17` | ℤ₂ selection rule; structural zero in code | **FORCED** |
| C10 | C_TTT = 4.000 / 3.3806 / 3.16228 | `SIM-2026-067/068/069` | `C_TTT = 2√2/√c` is a Virasoro identity **and a literal line of code** | **ALGEBRAIC-TRANSFORM** of c |
| C11 | c = 1/2, 7/10, 4/5 measured | `qw_cttt_circle_results_ising.json`, `*_results_*.jsonl` | Fixed by the minimal model | **FORCED** |
| C12 | l_AdS = 1/ln χ = 1.4427 | `paper-draft-scipost.tex:84-86` | "set by the MERA architecture, not by optimization" (the paper's own words) | **FORCED (definition)** |
| C13 | T_pred = (π/2)·l_AdS = 2.266 | `paper-draft-scipost.tex:175` | π/2 from a null-geodesic condition in global AdS₃; no fitted parameter | **FORCED prediction**, but see §7 on post-hoc selection |
| C14 | T_meas = 2.239, residual −1.21% | `SIM-2026-025`, ERRATA E2 | Genuinely measured | **AT RISK** (the only clean parameter-free comparison in the manuscript) |
| C15 | m_eff(CFT) = 0.693 | `effective_mass_analysis.json:ads_mass_dimension` | = 1/l_AdS = ln 2, from Δ_ε = 1 and BF saturation. Pure algebra | **FORCED** |
| C16 | m_eff(MERA) = 0.670, 3.5% agreement | same, `comparison_to_measurements` | = l_AdS/ξ from a **2-point** exponential; equivalent to ξ = l_AdS² | **AT RISK, adverse** (§8) |
| C17 | c_KS(Yang-Lee) = −4.29, = −22/5 | `SIM-2026-071.json` | **Forced by ⟨L₋₂1,L₋₂1⟩ = c/2 once the pairing and the state ID are granted** | **FORCED-CONDITIONAL** (§9) |
| C18 | c_eff = +2/5 EXCLUDED | `SIM-2026-071.json:18` | c_eff is not expressible in the vacuum module; this estimator could never have returned it | **FORCED** (vacuous exclusion) |
| C19 | Unitary control 0.49986 vs 0.5 | `SIM-2026-071.json:10` | Same algebra at c = 1/2 | **FORCED** |
| C20 | KS survives non-unitarity | `SIM-2026-071.json:21` | **No theorem covers this.** The one genuinely at-risk proposition in the Yang-Lee work | **AT RISK — the real result** |
| C21 | C_TTT imaginary at c < 0 | `SIM-2026-071.json:24` | Immediate from C10: 2√2/√c with c < 0. Zero content | **ALGEBRAIC-TRANSFORM** |
| C22 | ⟨1\|1⟩ negative = "the conformal vacuum is a negative-norm state" | `SIM-2026-071.json:17` | **Over-read.** Only the *ratio* is invariant; in M(2,5) the vacuum has *positive* Shapovalov norm and it is L₋₂\|1⟩ that has c/2 < 0 | **mis-stated** (§9.7) |
| C23 | Δ_φ = −1/5 (Yang-Lee) | `HYP-2026-028.json` ×6 | −1/5 is the *chiral weight*; Δ_φ = 2h = −2/5 | **wrong by 2×** (already logged by `inv-pipelines` §5.9) |
| C24 | R_∞ → −(1+√5)/2, g₁ = ((5−√5)/10)^{1/4} | `SIM-2026-070.json` | Exact BCFT values of M(2,5); reproduction of an external table | **FORCED** (Level 1, and correctly labelled as a gate) |

Count: **17 FORCED / ALGEBRAIC-TRANSFORM, 1 FORCED-CONDITIONAL, 4 AT RISK (2 of them adverse),
2 mis-stated.** Exactly one claim in the whole program (C20) had multiple physically meaningful
outcomes and was answered by the numerics.

---

## 3. α = 4 and its claimed universality

### 3.1 The derivation, in full

The stress tensor of a 2D CFT is the conserved current generating conformal transformations.
Conservation ∂^μ T_{μν} = 0 plus tracelessness fixes its scaling dimension to equal the spacetime
dimension:

```
  Δ_T = d = 2 ,   with (h, h̄) = (2,0) for T and (0,2) for T̄ ,  spin s = ±2 .
```

Equivalently, in the Virasoro algebra the generator L₋₂ raises L₀ by 2 by construction:
[L₀, L₋₂] = 2 L₋₂, so L₋₂|0⟩ sits at h = 2 identically. **Nothing about this uses unitarity,
reflection positivity, the sign of c, or which minimal model is in play.** It is true at
c = 1/2, at c = 7/10, at c = 4/5, and at c = −22/5.

The project states this correctly and prominently in its own record. `SIM-2026-051.json`
(`verdict`), verbatim:

> *"This is exactly the CFT prediction: Delta_T=2 in every unitary 2D CFT (the stress tensor has
> conformal weight (2,0)+(0,2)), so alpha=2*Delta_T=4 must hold at any 2D critical point.
> **The numerics confirm the symmetry argument.**"*

**§8 verdict: the number is fixed by symmetry.** Before running SIM-051, SIM-052, SIM-062 or
SIM-063, the only possible outcomes were "the MERA scaling superoperator resolves the level-2
vacuum descendant" or "it does not". §6 counterfactual novelty: **near-zero**. §5 level: **1**.

### 3.2 The universality claim contains no additional information

The abstract (`research/paper-draft-scipost.tex:45`) presents the three-class result as a
confirmation:

> *"Because Δ_T = 2 is fixed by conformal symmetry in every unitary two-dimensional CFT, α = 4 is
> universal; we confirm this at two further fixed points…"*

The sentence is self-refuting as a discovery claim: it states the theorem, then reports confirming
the theorem. Under §5 that is validation (Level 1) and must be labelled as such. It is **not** a
universality *test*, because a universality test requires that the classes could have differed,
and Δ_T = 2 forbids that.

### 3.3 What the three-class programme actually measured

Reading the records rather than the abstract:

| Class | Record | What was measured | What was inferred |
|---|---|---|---|
| Ising c=1/2 | `research/data/simulations/SIM-2026-011-interaction.json` | **F(dr) at 24 qubits** — a real force profile | α = 3.92 ± 0.16 by fit |
| TCI c=7/10 | `research/data/simulations/SIM-2026-051.json`, `SIM-2026-052.json` | **Δ_T from the MERA scaling superoperator** (2.007, 1.9994) | α = 2Δ_T = 4.01 / 3.999 |
| Potts c=4/5 | `research/data/simulations/SIM-2026-062.json`, `SIM-2026-063.json` | **Δ_T from the MERA scaling superoperator** (2.001) | α = 2Δ_T = 4.00 |

**No force profile was ever measured at TCI or at Potts.** The manuscript concedes this in the
open-questions section (`research/paper-draft-scipost.tex:617`): *"The transport and force-profile
measurements, however, have been performed only at c = 1/2."* But the abstract (L45) reports
"α = 4.00 at all three universality classes" without that qualifier, and the memory index records
HYP-027 as *"α=4 UNIVERSAL at tricritical Ising"*. The operation performed at TCI and Potts was
**multiplication of a symmetry-fixed number by 2**.

**§8 verdict: it follows algebraically from a previously extracted parameter, and that parameter
was itself fixed by symmetry.** Double-forced.

### 3.4 The one part of the α argument that is NOT forced — and it fails at TCI

The genuinely non-trivial step is not Δ_T = 2. It is: *which operator dominates the exchange
channel between the two probes?* The manuscript's argument
(`research/paper-draft-scipost.tex:45`, repeated at L577) is the Ising fusion rule

```
  ε × ε = [1]                      (Ising, M(3,4))
```

so the ε-probe channel contains only the identity family — 1, T, T̄ and descendants — the identity
piece is r-independent, and the leading r-dependent term is T-exchange at r^(−2Δ_T) = r^(−4).
**That argument is correct and it is Ising-specific.** It does not survive class change. Using the
Kac formula h_{r,s} = ((p′r − ps)² − (p − p′)²)/(4pp′):

**Tricritical Ising, M(4,5), c = 7/10** (p=4, p′=5, h = ((5r−4s)²−1)/80):

```
  ε  = φ_{1,2} : h = (3²−1)/80 = 1/10   → Δ_ε  = 1/5
  ε′ = φ_{1,3} : h = (7²−1)/80 = 3/5    → Δ_ε′ = 6/5
  fusion:  φ_{1,2} × φ_{1,2} = φ_{1,1} + φ_{1,3}  =  1 + ε′
```

So at TCI the probe channel **does** contain a scalar primary, ε′, at Δ_{ε′} = 6/5 = 1.2 < 2. Its
exchange gives r^(−2Δ_{ε′}) = **r^(−12/5) = r^(−2.4)**, which dominates T's r^(−4) at every
distance. **The a-priori prediction at TCI is α = 2.4, not 4.** The relevance of ε′ is exactly why
TCI is tricritical (ε′ is the relevant direction that flows to Ising), so this is not an exotic
edge case.

**Potts, M(6,5) D-series, c = 4/5** (p=5, p′=6, h = ((6r−5s)²−1)/120):

```
  ε  = φ_{2,1} : h = (7²−1)/120 = 2/5   → Δ_ε = 4/5
  fusion:  φ_{2,1} × φ_{2,1} = φ_{1,1} + φ_{3,1},   h_{3,1} = (13²−1)/120 = 7/5 → Δ = 14/5 = 2.8
```

Here the leading non-identity scalar in the ε channel sits at Δ = 2.8 > 2, so **T does dominate
at Potts** and α = 4 is the correct prediction — *for an exactly-ε probe*. (The ℤ₃-charged sector
changes this if the probe carries ℤ₃ charge: σ × σ† ∋ ε at Δ_ε = 4/5 gives r^(−8/5).)

**Consequence.** The project's universality claim is exactly inverted relative to the physics.
The quantity it validated (Δ_T = 2) could not have varied. The quantity that *could* have varied —
the exchange channel, and therefore the observable exponent — **predicts a class-dependent α**
(2.4 at TCI, 4 at Potts, 4 at Ising), and was never measured at two of the three classes. A force
measurement at TCI is therefore a genuine §6-moderate-to-high experiment: α ≈ 2.4 would confirm the
conformal-block bookkeeping and *refute* the universality slogan; α ≈ 4 would be a real surprise
requiring explanation.

**§12 killer test, previously unnamed, now named:** *A force profile at the tricritical point that
returns α ≈ 4 rather than α ≈ 2.4 falsifies the conformal-block mechanism the project has advanced
as the explanation of α = 4; a value near 2.4 falsifies the universality claim.* Either outcome
changes a decision. This is among the cheapest high-value experiments identified in this audit.

### 3.5 The channel-purity assumption is unstated and probably violated

α = 2Δ_T requires the probe density O†O to couple only to the identity family. The manuscript's
probe (`research/paper-draft-scipost.tex:275`,
`research/data/simulations/SIM-2026-011-interaction.json` field `boundary_primary_coeffs`
{alpha 0.635, beta −0.026}) is

```
  σ_j = 0.635 (X_j + X_{j+1}) − 0.026 (X_j Z_{j+1} + Z_j X_{j+1})
```

Under P = ∏X: X → X (ℤ₂-even, ε channel) but X_j Z_{j+1} → −X_j Z_{j+1} (**ℤ₂-odd, σ
channel**). The operator is therefore an ε/σ mixture, and the manuscript's own naming
is internally inconsistent — it calls the operator σ_j at Eq. (7) while §4.2 identifies the
propagating excitation as **ε**. Any σ admixture opens channels with *smaller* exponents
(σ × σ ∋ ε → r^(−2Δ_ε) = r^(−2); and the density's ℤ₂-odd piece → r^(−2Δ_σ) = r^(−1/4)), all of
which flatten the profile at large dr relative to r^(−4).

**This is an alternative explanation for a measured exponent below 4 that the project has not
considered anywhere in the records.** Whether the admixture is numerically significant I did not
compute (see §13 UNVERIFIED item 3) — but the *assumption* of channel purity is load-bearing for
the headline and is stated nowhere.

### 3.6 The 24-qubit data contain no power law (independently re-derived)

I re-derived the local exponent −d ln|F| / d ln dr directly from
`research/data/simulations/SIM-2026-011-interaction.json` field `F_interaction_avg` (all twelve
points, no fitting):

| interval | 1→2 | 2→3 | 3→4 | 4→5 | 5→6 | 6→7 | 7→8 | 8→9 | 9→10 | 10→11 | 11→12 |
|---|---|---|---|---|---|---|---|---|---|---|---|
| local α | 2.04 | **4.23** | 2.60 | 2.46 | 2.46 | 2.53 | 2.66 | 2.84 | 3.10 | 3.48 | 4.06 |

A true F ∼ dr^(−4) would give ≈ 4 in every interval. The measured sequence has a single spike at
dr = 2→3, a broad shelf at **2.45–2.66** across dr = 3…8, and a monotone climb at dr ≥ 9 that is
the far-boundary artifact of an open 24-site chain probed with an anchor at site 6 (field
`anchor: 6`). The quoted `alpha = 3.9218 ± 0.1590`
(`fits.F_avg_dr_ge2.power_law.alpha` / `.dalpha`) is therefore a **weighted average over a spike
and a shelf**, not the slope of a plateau.

This independently confirms the phase-1 finding (`research/data/audit/raw/inv-sims-early.md`
§3.1–3.2, defects A1/A2) by a different route — local log-derivatives rather than fit-window
ablation — and it adds the mechanism: the 3.92 comes from the dr = 2 point at one end and the
boundary upturn at the other. The shelf value 2.45–2.66 sits closer to **2Δ_ε = 2** (scalar
exchange, the hypothesis the paper declares "inconsistent") than to 2Δ_T = 4.

**§8 verdict for C6: the number is not fixed by symmetry — it is fixed by the fit window.**
Grade AT RISK, outcome adverse.

### 3.7 Where Δ_T is and is not actually measured

| Pipeline | Δ_T status |
|---|---|
| P1 MERAKit (SIM-050/051/052/062/063) | **measured** from the scaling-superoperator spectrum |
| P2 cttt-circle (SIM-067) | **measured** (conformal spin s_T = 2.0000000000000004 at every N, an eigenphase, plus the Δ gap) |
| P3 puMPS (SIM-068/069) | **imposed**: v_T is defined by Δ_T = 2 (`research/tools/pumps-setup/qw_cttt_of.jl`, `qw_cttt_potts3.jl`) |
| P4 yanglee (SIM-070/071) | **imposed**: `research/tools/yanglee-pt/qw_yanglee_ks.jl:128`, `v_T = (ET-ens[ivac])*L/(2pi*2.0)` |

Two of the four pipelines cannot measure the quantity that the α claim rests on, because they
consume it as an input. This matters for §7 independence: any comparison between a P3/P4 number
and "Δ_T = 2" is **algebraically equivalent**, not a check.

---

## 4. C_TTT at each class — a Virasoro identity computed as a line of code

### 4.1 The identity

The Virasoro algebra fixes the T × T operator product completely:

```
  T(z) T(w) = (c/2)/(z−w)^4  +  2T(w)/(z−w)^2  +  ∂T(w)/(z−w)  +  regular
```

There is **exactly one free parameter in the whole T-sector: c.** Consequently

```
  ⟨T(z1)T(z2)⟩          = (c/2) / z12^4
  ⟨T(z1)T(z2)T(z3)⟩     = c / (z12^2 z13^2 z23^2)
```

and the *unit-normalised* three-point coefficient is a pure function of c:

```
  T̂ ≡ T/√(c/2)   ⇒   C_TTT ≡ ⟨T̂T̂T̂⟩-coefficient = (c/2)/(c/2)^{3/2} = √(2/c)
```

The project uses the convention C_TTT = 2√2/√c, i.e. exactly 2× the above (a normalisation
convention for the two-point function; harmless). Check against the project's own targets:

| c | 2√2/√c | project's "exact" |
|---|---|---|
| 1/2 | 4.00000 | 4.000 |
| 7/10 | 3.38062 | 3.3806 |
| 4/5 | 3.16228 | 3.16228 |

**§8 verdict: it is a direct Virasoro identity.** There is no independent "structure constant"
C_TTT in 2D CFT; the TTT coefficient *is* the central charge. Measuring C_TTT and measuring c are
the same measurement.

### 4.2 The project computes it that way, literally

`research/tools/cttt-circle/qw_cttt_circle.py:203`:

```python
  res["C_TTT"] = 2*np.sqrt(2)/np.sqrt(res["c_meas"])
```

and identically in `research/tools/pumps-setup/qw_cttt_of.jl:116-117`,
`qw_cttt_potts3.jl:131-132`, `qw_pumps_validate_ising.jl:79-82`. There is no independent
three-point evaluation anywhere in the shipped ladder. The project's own design document says so:
`research/tools/cttt-circle/CTTT-ROUTE-B-CIRCLE-DESIGN.md:96-102` states this measurement is
*"of the same epistemic kind as C_σσε = 0.5."* The two attempts at a genuinely independent
three-point route were both retracted or closed:

- **Route A** (MERA PEV spin-resolved, `SIM-2026-066.json`): χ=12 seeds scattered
  2.15 / 2.22 / 25.7 / 0.057, one at 6e8 — **closed as a decisive negative**, correctly.
- **Equal-time correlator route** (`qw_cttt_circle.py:analyze()`, C_TTT = √2·A₃/|A₂|^{3/2}):
  falsified by ED the same day it was designed; `CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117` instructs
  *"do not quote §3's A₂/A₃ formulas."*

So **the one independent three-point measurement in the entire program was retracted**, leaving
only the algebraic transform. That is honest and correctly recorded — but the headline framing
("THE LADDER IS COMPLETE … three classes ≤0.15% each", memory index and
`NEXT-SESSION.md`) reports it as three measurements of a coupling constant.

### 4.3 Quoting C_TTT instead of c halves the apparent error

Because C_TTT ∝ c^(−1/2), a relative error δ in c propagates to δ/2 in C_TTT. I verified this on
the project's own fitted values:

| class | fitted c | dev. in c | implied C_TTT | dev. in C_TTT | ratio |
|---|---|---|---|---|---|
| Ising | 0.49871 | −0.2580 % | 4.00517 | +0.1293 % | **0.5010** |
| TCI | 0.69858 | −0.2029 % | 3.38405 | +0.1016 % | **0.5008** |
| Potts | 0.79891 | −0.1363 % | 3.16443 | +0.0682 % | **0.5005** |

(fitted c from `research/tools/cttt-circle/qw_cttt_circle_results_ising.json` extrapolation and
from `SIM-2026-068.json` / `SIM-2026-069.json` `c_inf`.)

The "≤0.15 %" ladder is a ≤0.26 % ladder in the quantity actually measured. Reporting the
square-root-transformed variable is not wrong, but it is a **precision claim inflated by a factor
of two** relative to the underlying measurement, and no record states the transformation's effect
on the error.

This compounds with the separately-fitted-extrapolation defect that `inv-pipelines.md` §3.3 found
(fitting c and C_TTT independently in 1/N² gives 4.00517 vs 3.99361, i.e. 0.29 % apart — larger
than either quoted deviation).

**§5 level for the C_TTT ladder: 1.** **§6 counterfactual novelty: zero** — it is the same number
as c, and c was fixed by the minimal model.

---

## 5. C_σσε = 0.50 ± 0.03

The Ising structure constant is an exact rational of the minimal model:

```
  C_σσε = 1/2   exactly   (M(3,4); BPZ/Dotsenko–Fateev Coulomb-gas value)
```

`SIM-2026-061.json:15` records mean 0.5075 across 8 ℤ₂-symmetric basins; `SIM-2026-064.json`
records the χ=10/12 drift to 5.6 % low.

**§8 verdict: determined by a known operator algebra.** Only implementation success or failure
was possible. §6 counterfactual novelty **near-zero**; §5 level **1**. The project's own
`CTTT-ROUTE-B-CIRCLE-DESIGN.md:96-102` already classifies it this way.

Two genuine sub-results attach to it and should be separated out under §5 Level 2:

- **C_σσσ = exactly 0** (`SIM-2026-061.json:17`) — a ℤ₂ selection rule realised as a *structural*
  zero in the symmetric tensor code rather than a fitted small number. Forced, but the fact that
  the implementation realises it structurally is a real methodological property.
- **The ℤ₂/ℤ₃-symmetric optimisation converting 2/8 → 8/8 clean basins**
  (`SIM-2026-061.json:12`, `SIM-2026-062.json`) — this is **not** forced by anything and is a
  legitimate Level-2 contribution.
- **`SIM-2026-064.json`'s honest flag** that precision improved 40× while accuracy drifted through
  the exact answer to 5.6 % low is the most scientifically informative thing in the OPE branch,
  and it is a *negative*.

---

## 6. The scaling dimensions

Every Δ the project reports is a Kac-formula rational:

| Model | c | Δ_σ | Δ_ε | Δ_T |
|---|---|---|---|---|
| Ising M(3,4) | 1/2 | 1/8 = 0.125 | 1 | 2 |
| TCI M(4,5) | 7/10 | 3/40 = 0.075 | 1/5 = 0.2 | 2 |
| Potts M(6,5) D-series | 4/5 | 2/15 = 0.1333 | 4/5 = 0.8 | 2 |
| Yang-Lee M(2,5) | −22/5 | — | Δ_φ = −2/5 | 2 |

with c = 1 − 6(p − p′)²/(pp′) and h_{r,s} = ((p′r − ps)² − (p − p′)²)/(4pp′). I re-derived each
entry from the Kac formula in §3.4 and §9.2; all match the values used in the records.

**§8 verdict: fixed by symmetry (representation theory of the Virasoro algebra at the given c).**
§6 near-zero. §5 level 1.

**One caveat in the project's favour.** The Potts χ-ladder Δ_σ = 0.089 (χ=6) → 0.14 (χ=9) →
0.133 (χ=12) (`SIM-2026-063.json`) is a *convergence* study, and convergence behaviour under
χ-escalation is genuinely not fixed by symmetry. That is Level-2 methodological content, and
`SIM-2026-063` correctly frames it as closing a χ-starvation caveat rather than as a discovery.

---

## 7. Transport: T = (π/2)·l_AdS

### 7.1 What is fixed and what is measured

Three ingredients:

```
  (i)   l_AdS = 1/ln χ = 1/ln 2 = 1.442695        (research/paper-draft-scipost.tex:84-86)
  (ii)  null-geodesic condition in global AdS3:  ⟨P1,P2⟩ = −cos(Δt) − 1,  −⟨P1,P2⟩ = 1
        ⇒ cos(T) + 1 = 1 ⇒ T = π/2                (research/paper-draft-scipost.tex:172)
  (iii) T_pred = (π/2)·l_AdS = 2.266               (ibid. :175)
```

Ingredient (i) is a *definition* fixed by the architecture — the paper says so explicitly:
*"This value is set by the MERA architecture, not by optimization"* (L86). Ingredient (ii) is a
pure geometric number. So **T_pred = 2.266 contains zero fitted parameters**, and the comparison
against T_meas = 2.239 is the one genuinely parameter-free confrontation in the manuscript.

**§8 verdict: the prediction is forced; the measurement is not.** Grade for C13: FORCED. Grade for
C14 (the measurement and hence the 1.21 % residual): **AT RISK** — this is the strongest
non-trivial comparison in the manuscript, and it should be defended as such rather than being
crowded out by the α = 4 framing, which is forced.

### 7.2 Three things that weaken it, all derivational rather than numerical

**(a) The π/2 was selected after the measurement, to replace a π that missed by exactly 2×.**
The manuscript's own narrative order (`research/paper-draft-scipost.tex:170`):

> *"The naive spacelike geodesic formula predicts T = π·l_AdS = 4.53, a factor of 2 larger than
> the measurement. This discrepancy is resolved by the composite geodesic framework of Bohra and
> Sivaramakrishnan…"*

Two candidate prescriptions (spacelike vs null) differ by exactly the factor by which the first
missed, and the second was adopted after seeing the data. Under §18/§36 this is a *calibrated*,
not out-of-sample, agreement: one binary choice was fixed by the observation, leaving the 1.21 %
residual as the only unconstrained content. That does not make the choice wrong — the null
condition is the physically correct one for a light-cone crossing event — but the record contains
no pre-registration, and §36 requires the original entry to be preserved.

**(b) The manuscript's cited external confirmation states π, not π/2, and this is never
reconciled.** `paper-draft-scipost.tex:228`, `:563` and `:631` all assert Wang & He *"analytically
proved the null geodesic formula t_trans = π"* and present it as confirming T = (π/2)·l_AdS.
π ≠ π/2. §3.3 of the same manuscript *rejects* T = π·l_AdS = 4.53. A units/convention
reconciliation (e.g. round-trip vs one-way) is required and is absent. `inv-manuscript-claims.md`
DEF-03 independently found that the claim is also absent from the project's own record of the
cited paper (`research/data/papers/PAPER-2026-088.json`). **This is the manuscript's only claim of
independent third-party confirmation, and as written it is numerically inconsistent with the
quantity it confirms.**

**(c) An unstated time-normalisation assumption.** T_meas is measured in units of the Wang–He
boundary Hamiltonian's inverse energy. Under H_boundary → λH_boundary, T_meas → T_meas/λ, while
T_pred = (π/2)/ln 2 is unchanged. The comparison therefore silently asserts that the Wang–He
normalisation `H = (L/4π)·Σ[X_{j−1}Z_jX_{j+1} − X_jX_{j+1}]`
(`research/data/simulations/SIM-2026-025.json` `physical_parameters.hamiltonian`) is the canonical
one that sets the emergent light-cone velocity to 1 in lattice units. That is inherited from the
cited construction and is very likely correct — but it is an **input, not a derivation**, and the
manuscript never states that the agreement is conditional on it. A referee will ask.

**(d) Prior finding that compounds this:** `inv-manuscript-claims.md` DEF-19 records that the
*same* record's detuning scan (`hyp010_criticality_scan.json`, `approach_A_wang_he_detuning`) gives
transport times 0.55–3.30 under δ = ±0.3 of the *same* Hamiltonian. Since the normalisation
question in (c) is a one-parameter deformation of that same Hamiltonian, the sensitivity is
directly relevant and is omitted from the manuscript.

### 7.3 Net

The transport result is the **only** headline in the manuscript whose predicted value could not be
obtained by re-expressing a CFT input. It deserves to be the paper's lead claim rather than its
second. Its weaknesses are all of the "one binary choice was made after seeing the data, and one
normalisation is assumed" kind, which is a far better position than "the answer was fixed by
symmetry" — but neither is currently disclosed.

---

## 8. m_eff = 0.693 vs 0.670 (3.5 %)

### 8.1 The prediction is `ln 2` by construction

From `research/paper-draft-scipost.tex:262-266` and
`research/data/simulations/effective_mass_analysis.json` (`ads_mass_dimension`):

```
  m² l_AdS² = Δ(Δ − d) = Δ(Δ − 2)        (AdS3 mass–dimension relation)
  Δ_ε = 1  ⇒  m² l_AdS² = −1             (exactly the BF bound, −d²/4 = −1)
  ⇒  |m_eff| = 1/l_AdS = ln χ = ln 2 = 0.693147
```

Every step is algebra on two inputs that are themselves fixed: Δ_ε = 1 (Ising CFT) and
l_AdS = 1/ln 2 (MERA architecture). **§8 verdict: forced.** §6 counterfactual novelty: **zero**.
Note also that the BF saturation is not a coincidence to be marvelled at — it is forced too:
Δ = 1 = d/2 is precisely the value at which m²l² = Δ(Δ−d) attains its minimum −d²/4.

### 8.2 What the "0.670" actually is, and what the 3.5 % actually compares

`effective_mass_analysis.json` `comparison_to_measurements` gives `xi_MERA = 2.154` and
`m_eff_from_MERA = 0.6698`. Reverse-engineering the arithmetic (verified):

```
  m_eff(MERA) = l_AdS / ξ_MERA = 1.442695 / 2.154 = 0.669775   ✓ (record: 0.6698)
```

So the claim "0.693 vs 0.670, 3.5 %" is algebraically identical to

```
  ξ_MERA  ==  l_AdS²  :   2.154  vs  1/(ln2)² = 2.081369   →  +3.49 %
```

which is precisely the record's quoted 3.5 %. The relation ξ = l_AdS² itself follows from the two
assumptions m = 1/l_AdS and d_geo = dr·l_AdS, so **the entire comparison is one measured number
(ξ_MERA) against one algebraic number (l_AdS²)**.

### 8.3 The one measured number is a two-point ratio, and better data destroy it

`effective_mass_analysis.json` states ξ_MERA = 2.154 is a *"two-point estimate from
V(dr=1)/V(dr=2)"* on SIM-2026-002 (N=16, L=3, 1.87 % energy error). Two points and one
free parameter: **zero degrees of freedom**, so the exponential model cannot be tested, only
solved. The paper concedes this (`:280`: *"only 2 MERA signal points available"*).

Applying the **same exponential model** to the project's better dataset —
`SIM-2026-011-interaction.json` `fits.F_avg_dr_ge2.exponential`, 24 qubits, exact ED, 11 points,
ξ = 0.6299 — gives

```
  m_eff(MERA, 24q exact) = l_AdS / ξ = 1.442695 / 0.629927 = 2.2903
  deviation from 0.693147:  +230.4 %
```

The record itself flags the same tension from the other side: the exponential fit's ξ = 0.63 is a
*"56 % deviation from l_AdS"* (`paper-draft-scipost.tex:344`) and the manuscript argues at length
(§5.2, §8.1) that the force is **power-law, not exponential** — which makes ξ, and therefore
m_eff(MERA), an artifact of a model the manuscript elsewhere rejects.

**§8 verdict for C16: not fixed by symmetry; fixed by choosing the two-point, low-quality dataset
and a functional form the project's own better data contradict.** Grade AT RISK, outcome adverse.
The 3.5 % agreement is not robust to dataset choice by a factor of ~66.

**Note on ERRATA coverage.** ERRATA E4 already flags the m_eff *derivation text* as
convention-clashing and says *"The m_eff agreement claim should be reviewed under whichever
convention is chosen."* That review has evidently not extended to the dataset question raised
here, which is the larger effect.

---

## 9. The Yang-Lee result: c_KS = −22/5 (the crux)

This is the project's strongest claim, so it receives the fullest treatment. The task asks a
sharp question:

> *Given that the Koo–Saleur lattice operators converge to Virasoro generators with the
> biorthogonal (bilinear) pairing, does c = −22/5 rather than c_eff = +2/5 follow ALGEBRAICALLY
> from ⟨T|T⟩ = c/2 with an indefinite metric?*

**Answer: yes, completely, in four lines. And more strongly than the question suggests — c_eff
is not merely disfavoured by the algebra, it is not expressible in the object being measured.**
The derivation follows; then §9.6 states precisely what the numerics tested that the algebra did
not guarantee.

## 9.1 Statement of the assumptions being granted

The derivation is conditional on exactly four inputs, all of which are *design decisions* recorded
in `research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md` **before** the run:

- **(A1) KS convergence.** The lattice Fourier modes of the Hamiltonian density,
  H_n = Σ_j e^{i n j θ}(h_j − e₀) with θ = 2π/L (half-bond phase for the two-site term;
  `qw_yanglee_ks.jl:34-35`), converge in the scaling limit — after the normalisation
  L/(2πv) — to the non-chiral Virasoro combination

  ```
     Ĥ_n  ≡  (L/2πv) H_n   →   L_n + L̄_{−n}   (mod an additive c-number at n = 0)
  ```

- **(A2) The pairing is the bilinear/Shapovalov form, not the Hermitian inner product.**
  On the lattice this is ⟨ψ_L|ψ_R⟩ with ⟨ψ_L| = (P|ψ_R⟩)^† from η-pseudo-Hermiticity with η = P
  (`qw_yanglee_ks.jl:93-94`: `lv = i -> conj.(vecs[i][pp])`, `biod = (i,j) -> transpose(lv(i))*vecs[j]`).
  Algebraically this realises the Virasoro antiautomorphism L_n^T = L_{−n}, i.e. the **Shapovalov
  form**, which is a *bilinear* form defined over ℂ with no positivity requirement.
- **(A3) State identification.** |0_R⟩ is the **conformal vacuum |1⟩** (the identity-module base,
  the SECOND k = 0 state; the *lowest*-energy state is |φ⟩ with Δ_φ = −2/5) and |T_R⟩ = L₋₂|1⟩
  (`qw_yanglee_ks.jl:84`, `ivac = MODE=="ising" ? i0[1] : i0[2]`).
- **(A4) Normalisation.** v_T is fixed by imposing Δ_T = 2 (`qw_yanglee_ks.jl:128`).

## 9.2 The M(2,5) data, re-derived

Yang-Lee is the minimal model M(2,5), p = 2, p′ = 5:

```
  c    = 1 − 6(p−p′)²/(pp′) = 1 − 6·9/10 = 1 − 27/5 = −22/5 = −4.4
  h_{r,s} = ((p′r − ps)² − (p−p′)²)/(4pp′) = ((5r − 2s)² − 9)/40
     h_{1,1} = (9−9)/40 = 0          → identity 1
     h_{1,2} = (1−9)/40 = −1/5       → φ,  Δ_φ = 2h_φ = −2/5
  fusion:  φ_{1,2} × φ_{1,2} = φ_{1,1} + φ_{1,3},  h_{1,3} = (1−9)/40 = −1/5 = h_φ
        ⇒  φ × φ = 1 + φ    (M(2,5) has only two primaries)
  effective central charge:  c_eff ≡ c − 24 h_min = −22/5 − 24(−1/5) = −22/5 + 24/5 = +2/5
```

All four values match the ones used in the records. (Note in passing: `HYP-2026-028.json` quotes
Δ_φ = −1/5 in six places; −1/5 is the *chiral weight* h_φ, and Δ_φ = 2h_φ = −2/5. The live
drivers use −2/5 correctly — `qw_yanglee_ks.jl:86` divides by `2pi*(2/5)` — so the running code is
right and the hypothesis record is wrong by a factor of 2. Already logged by `inv-pipelines.md`
§5.9; I confirm it independently from the Kac formula.)

## 9.3 Why c_eff = +2/5 exists at all, and where it lives

c_eff is **not** a central charge of any Virasoro algebra. It is a spectrum-wide bookkeeping
combination that appears in exactly one place: the *ground-state* Casimir energy on the cylinder,
because in a non-unitary theory the lowest-lying state is **not** the conformal vacuum.

For a state of weights (h, h̄) on a circle of circumference L:

```
  E_{h,h̄}(L)  =  (2πv/L) ( h + h̄ − c/12 )      + extensive term
```

Take the actual lowest state of M(2,5), which is |φ⟩ with h = h̄ = −1/5:

```
  h + h̄ − c/12  =  −2/5 − (−22/5)/12  =  −2/5 + 11/30  =  −1/30
```

and the standard non-unitary parameterisation of the *same* number as an effective charge:

```
  E_0(L) = −(π v /6L) c_eff  =  (2πv/L)(−c_eff/12)  =  (2πv/L)(−(2/5)/12) = (2πv/L)(−1/30)   ✓
```

(both sides verified numerically: −0.0333333…). So:

> **c_eff is a statement about which module has the lowest h. It is a property of the global
> spectrum, obtained by a Casimir-energy or entanglement-entropy fit. It has no representation
> inside a single Virasoro module.**

That is the entire reason the "true c vs c_eff" question is a real *physics* question — standard
lattice routes (S ∼ (c_eff/3)ln L, or E₀(L) scaling) return c_eff, and one wants a lattice
observable that returns c. It is also the reason the answer is forced once an estimator is written
that never looks outside the identity module.

## 9.4 The derivation: ⟨T|T⟩ = c/2 and the product-form estimator

**Step 1 — the Shapovalov norm of the level-2 vacuum descendant.**
The vacuum |1⟩ is sl(2,ℂ)-invariant: L_n|1⟩ = 0 for n ≥ −1, and L₀|1⟩ = 0. Define |T⟩ = L₋₂|1⟩.
Using the Virasoro commutator

```
  [L_m, L_n] = (m − n) L_{m+n} + (c/12) m(m² − 1) δ_{m+n,0}
```

with m = 2, n = −2:

```
  ⟨1| L_2 L_{−2} |1⟩ = ⟨1| [L_2, L_{−2}] |1⟩          (since L_2|1⟩ = 0)
                     = ⟨1| ( 4 L_0 + (c/12)·2·(4−1) ) |1⟩
                     = ⟨1| ( 4 L_0 + c/2 ) |1⟩
                     = (c/2) ⟨1|1⟩                      (since L_0|1⟩ = 0)
```

Hence

```
  ⟨T|T⟩ = (c/2) ⟨1|1⟩                                  (★)
```

**No step used unitarity.** ⟨·|·⟩ here is the Shapovalov bilinear form defined by the
antiautomorphism L_n^T = L_{−n}; it is defined for every c ∈ ℂ. For c < 0, (★) says the level-2
vacuum descendant has **negative** Shapovalov norm relative to the vacuum. That statement is not a
discovery: *it is the definition of a non-unitary highest-weight representation.* For M(2,5),
c/2 = −11/5 = −2.2.

**Step 2 — the KS matrix elements.**
Under (A1), Ĥ_{+2} → L_2 + L̄_{−2} and Ĥ_{−2} → L_{−2} + L̄_{+2}. Acting on the vacuum and on |T⟩:

```
  Ĥ_{+2} |1⟩       = (L_2 + L̄_{−2})|1⟩ = L̄_{−2}|1⟩ = |T̄⟩        (L_2|1⟩ = 0)
  Ĥ_{−2} |1⟩       = (L_{−2} + L̄_{2})|1⟩ = L_{−2}|1⟩ = |T⟩       (L̄_2|1⟩ = 0)
  ⟨T| Ĥ_{−2} |1⟩   = ⟨T|T⟩ = c/2 · ⟨1|1⟩
  ⟨1| Ĥ_{+2} |T⟩   = ⟨1| (L_2 + L̄_{−2}) L_{−2} |1⟩
                    = ⟨1|L_2 L_{−2}|1⟩ + ⟨1| L̄_{−2} L_{−2} |1⟩
                    = (c/2)⟨1|1⟩ + 0                              (second term is (h,h̄)=(2,2), pairs to 0 with ⟨1|)
```

Both surviving elements equal (c/2)⟨1|1⟩. The chirality bookkeeping is the reason the driver
computes **both orientations** and lets the structural zero pick (`qw_yanglee_ks.jl:109-116`,
"the dead orientation is a structural zero ~1e-26") — that machinery is implementing exactly the
L̄_2|1⟩ = 0 / L_2|1⟩ = 0 annihilations above.

**Step 3 — the estimator.**
`HYP028-BIORTHO-KS-DESIGN.md:62-66` and `qw_yanglee_ks.jl:129`:

```
  c_KS  =  2 · ⟨1_L|Ĥ_{−2}|T_R⟩ ⟨T_L|Ĥ_{+2}|1_R⟩ / ( ⟨T_L|T_R⟩ ⟨1_L|1_R⟩ )
```

Substituting the Step-2 values and (★), and writing N ≡ ⟨1|1⟩:

```
  numerator    = (c/2 · N) · (c/2 · N) = (c/2)² N²
  denominator  = ⟨T|T⟩ · ⟨1|1⟩ = (c/2 · N) · N = (c/2) N²
  c_KS         = 2 · (c/2)² N² / ((c/2) N²) = 2 · (c/2) = c            ∎
```

**c_KS = c, identically.** Every factor of the arbitrary lattice normalisation N cancels, which is
also why the estimator is exactly invariant under complex rescaling of the eigenvectors (the
property `inv-pipelines.md` §5.5 proves independently and correctly recommends stating as a
theorem).

**Step 4 — could c_eff have appeared?**
No, and not by a small margin. c_eff = c − 24 h_min requires h_min, i.e. knowledge of *which
module* sits lowest. The estimator's inputs are: |1⟩, L₋₂|1⟩, and Ĥ_{±2}. All three live inside
the identity module. The Virasoro algebra restricted to the vacuum Verma module contains c as its
only free parameter and contains no function of h_φ whatsoever. **There is no assignment of the
estimator's inputs that produces +2/5.**

For completeness, the "unitary-habit mistake" — taking the physical ground state |φ⟩ as the
vacuum — does *not* produce c_eff either. In the φ module,

```
  ⟨φ| L_2 L_{−2} |φ⟩ = ⟨φ|(4L_0 + c/2)|φ⟩ = (4h_φ + c/2)⟨φ|φ⟩ = (−4/5 − 11/5)⟨φ|φ⟩ = −3⟨φ|φ⟩
```

so the corresponding estimator would return 2·(−3)²/(−3) = −6, not +0.4. (And in M(2,5) the φ
module has a level-2 null vector, (L₋₂ − (5/2)L₋₁²)|φ⟩ = 0, so the level-2 structure differs
again — the design document notes this at line 71-74.)

> **Conclusion of the derivation.** Granted (A1)–(A4), c_KS = −22/5 is forced, its sign is forced,
> and c_eff = +2/5 was never an available outcome of this estimator under any state assignment.
> **The "discrimination" reported in `SIM-2026-071.json:18` ("c_eff = +2/5: EXCLUDED (wrong sign,
> ~11x magnitude)") is a vacuous exclusion: it rules out a hypothesis the measurement was
> structurally incapable of confirming.**

## 9.5 A further reduction: the estimator has no L and no v in it

`qw_yanglee_ks.jl:128-129`:

```julia
  v_T = (ET - ens[ivac]) * L / (2pi*2.0)
  cks = 2 * prods[jT] * (L/(2pi*v_T))^2
```

Substituting v_T:

```
  L / (2π v_T) = L / ( 2π · (E_T − E_vac)·L/(4π) ) = 2 / (E_T − E_vac)

  ⇒   c_KS  =  8 · prods[jT] / (E_T − E_vac)²
```

**L and v_T cancel identically.** The "(L/2πv_T)² finite-size normalisation" carries no
information; it is bookkeeping. v and v_T enter the result *only* through the Δ-gate that selects
which cluster state is called T (`qw_yanglee_ks.jl:123-126`). This is worth stating in the record
because it makes the true dependency structure visible: the entire finite-size content of c_KS is
in `prods` and in the single gap (E_T − E_vac).

It also means the imposed Δ_T = 2 is doing double duty — it defines v_T (which then cancels) *and*
centres the acceptance window (which does not).

## 9.6 What the numerical experiment ACTUALLY tested that the algebra did not guarantee

This is the part that must not be softened in either direction. The following were genuinely at
risk and are genuinely answered — they constitute the real result:

**(R1) That the Koo–Saleur correspondence extends at all to a non-Hermitian chain with η = P
biorthogonal pairing. [HIGH VALUE — the actual contribution]**
Assumption (A1) is a *conjecture* even in the unitary case (Koo–Saleur is a lattice→continuum
correspondence supported by numerics, not a theorem), and in the biorthogonal non-Hermitian case
there is no result at all: non-normal H, complex-symmetric structure, an indefinite pairing, and
eigenvectors that are not orthogonal in any Hilbert-space sense. Nothing forces Ĥ_n to converge to
L_n + L̄_{−n} there. **A ladder of c_KS values monotonically tracking toward a negative number of
the right order is real evidence that it does.** This is Level 2 (methodological) aspiring to
Level 3, exactly as `inv-pipelines.md` §6.3 classifies it, and it is the correct thing to write a
paper about.

**(R2) That the conformal vacuum |1⟩ is identifiable at finite L, and that the M(2,5) module
structure appears. [MODERATE VALUE, and cleanly separable]**
The prediction that |1⟩ is the *second* k = 0 state and that the k = ±2 cluster contains exactly
one φ-descendant below T (from the level-2 null vector) was pre-registered
(`HYP028-BIORTHO-KS-DESIGN.md:67-74`) and confirmed (`SIM-2026-071.json:17`). **Note that this is
a pure spectrum observation** — gaps and momenta only, no KS elements — so it is a *separate and
cleaner* result than c_KS, independent of (A1) and (A2). It is currently buried inside the c_KS
record. It should be surfaced on its own.

**(R3) That module mixing does not destroy the T identification. [HIGH INFORMATION, ADVERSE-LEANING]**
It was not guaranteed, and the answer is the most interesting fact in SIM-071:
`SIM-2026-071.json:23` records that the cross-module product to the φ-descendant is **~10× larger
than T's** (at L=18: 28.451 for the φ-descendant vs −2.588 for T; and a third state at
D_vac ≈ 3.36 carries −7.335, i.e. 2.8× T's — the third state is not mentioned in the record).
In unitary chains cross-tower elements are ~1e−4 suppressions; here the hierarchy **inverts**.
Consequence, correctly identified by `inv-pipelines.md` §5.4(5) and confirmed by my reading of
`qw_yanglee_ks.jl:124-127`: since only one state falls inside the window (1.75, 2.25) at every L,
`argmax` is a **no-op**, and T is selected by energy alone against a window centred on the exact
CFT value Δ_T = 2, in units of a velocity fixed by imposing the exact CFT value Δ₁ − Δ_φ = 2/5.
**At Yang-Lee the T identification has no empirical discriminator left; it rests entirely on
M(2,5) theory input.** That the construction still returns the right answer is evidence *for* the
correspondence; that the unitary discriminator points at the wrong state is a genuine, novel,
honestly-reported methodological finding and should be a headline of the methods paper in its own
right (§13 of the governing standard, item 9: *"How should states be identified when familiar
unitary hierarchy rules invert?"*).

**(R4) That the finite-size flow converges. [PARTIALLY ANSWERED, ADVERSE]**
It did not converge within reach. The measured ladder
(`research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl`, and `SIM-2026-071.json:14`) is

```
  L:    10        12        14        16        18
  c_KS: −1.413    −1.703    −1.954    −2.170    −2.356
```

At L = 18 the raw measurement is **53.5 % of −22/5**. The remaining 46.5 % is supplied by a
two-level Richardson extrapolator that is not committed to the repository, whose Phase-1 sibling
required selecting the last of a rising ratio sequence to hit its quoted 0.01 %
(`inv-pipelines.md` §5.8), and whose input working point h_c^∞ carries a documented ~3× lever arm
on the headline (−3.67 / −4.29 / −7.04 for three defensible fits; `inv-pipelines.md` §5.6).
**The "2.6 % agreement with −22/5" is therefore an extrapolator result, not a measurement**, and it
is the least robust part of the claim. The **sign** and the order of magnitude survive all three
h fits — that part is solid.

**(R5) That numerical conditioning permits the extraction at all. [ANSWERED, WITH A WARNING]**
1/|⟨ψ_L|ψ_R⟩| grows from 10.4 (L=10) to 180.5 (L=18) for T, doubling every ΔL = 2
(`Tnorm` field; tabulated in `inv-pipelines.md` §5.7). At L ≤ 18 double precision is ample. The
trend extrapolates to κ ~ 1e5–1e6 at L ~ 30, which bears directly on SIM-071's own proposed next
step ("puMPS-scale L would sharpen the third digit", `SIM-2026-071.json:25`).

## 9.7 The sign: what is and is not measured

`SIM-2026-071.json:17` states:
*"⟨1|1⟩ biorthogonal norm NEGATIVE at every L (the conformal vacuum is a negative-norm state — the
indefinite metric visible raw)."*

The physics behind this is right; the statement as written is **over-read**, in a way worth
correcting before publication:

1. Under the pairing ⟨ψ_L|ψ_R⟩ = ψ†Pψ, the *sign* of a state's norm is invariant under
   ψ → αψ (it scales by |α|²), so the individual signs ARE meaningful lattice observables
   (measured: ⟨1|1⟩ < 0, ⟨T|T⟩ > 0 — the magnitudes −0.0107/−0.0040/−0.0015 at L = 10/12/14 were
   recovered by `inv-pipelines.md` §5.2 from an independent reimplementation, since the repo
   retains no Phase-2 log).
2. **But the identification of the lattice pairing with the Shapovalov form is only fixed up to a
   single global real constant κ.** Only the *ratio* ⟨T|T⟩/⟨1|1⟩ is convention-free, and (★) says
   that ratio must equal c/2 < 0. The observed pattern (⟨1|1⟩ < 0, ⟨T|T⟩ > 0) is the CFT pattern
   (⟨1|1⟩ > 0, ⟨T|T⟩ = c/2 < 0) multiplied by κ < 0. Both are consistent.
3. So in **M(2,5) itself the conformal vacuum has positive Shapovalov norm**, and it is L₋₂|1⟩
   that carries the negative one. Describing the vacuum as "a negative-norm state" is a statement
   about the lattice sign convention, not about the CFT, and a referee who knows minimal models
   will flag it.

**The correct, defensible statement:** *the relative η-signature of |1⟩ and L₋₂|1⟩ is opposite,
which by (★) requires c < 0; this single bit is the sign content of the measurement.*

And that bit was **predicted with certainty** by (★) before the run. §6 counterfactual novelty of
the sign, given (A1)–(A4): near-zero. §6 counterfactual novelty of "(A1)–(A4) hold at all":
moderate-to-high. Those are different claims and the record conflates them.

One further point the record does not make, and should: the sign of the *estimator* is

```
  sign(c_KS) = sign( numerator / denominator )
             = sign( (product of two elements) / (⟨T|T⟩⟨1|1⟩) )
```

and in the exact limit the numerator is (c/2)²N² ≥ 0, so **the sign of c_KS is entirely the sign
of ⟨T|T⟩⟨1|1⟩** — i.e. the relative signature. Had the Hermitian inner product ⟨ψ_R|ψ_R⟩ been used
instead of the bilinear pairing, both norms would be positive and c_KS would come out **positive**
regardless of the physics. **"Sign is now part of the measurement, not a convention"
(`HYP028-BIORTHO-KS-DESIGN.md:66`) is therefore true only relative to a pairing choice that is
itself an input.** The choice is the correct one — the Shapovalov form is the right algebraic
object — but the record should say that the negative sign is *conditional on* (A2), not
independent evidence for it.

## 9.8 Independence ledger for the Yang-Lee claim (§7)

Exact M(2,5) CFT data is injected into the measurement in **four** places, and the output is
compared against exact M(2,5) CFT data:

```
  c = −22/5, h_φ = −1/5, Δ_T = 2   (external exact input)
      │
      ├─► Δ₁ − Δ_φ = 2/5 imposed  →  v      (qw_yanglee_ks.jl:86)
      │                                │
      │                                └─► Δ_vac scale for the T-window
      ├─► Δ_T = 2 imposed         →  window (1.75, 2.25)   (line 124)
      ├─► Δ_T = 2 imposed         →  v_T    (line 128)   [cancels; see §9.5]
      └─► the M(2,5) module structure       →  "the vacuum is the 2nd k=0 state" (line 84)
                                                │
                                                ▼
                                    prods, (E_T − E_vac)  →  c_KS  →  compared to c = −22/5
```

**§7 classification: structurally dependent.** Not fraudulent and not unusual — every lattice CFT
measurement calibrates against known data — but the record presents the comparison as a
discrimination between two hypotheses, and three of the four injected inputs are consequences of
the very model whose central charge is the answer. Under §7's own words: *"a beautiful agreement
is not strong evidence if both sides are transformations of the same input."*

The one genuinely external anchor in the whole P4 pipeline is Phase 1's reproduction of
PAPER-133's Table I (g₁ = 0.725073, R_∞ = −(1+√5)/2), which is external data from a different
group — correctly identified as such by `inv-pipelines.md` §6.2 and correctly framed by
`SIM-2026-070.json` as a *gate*, not a result. Note however that both of those targets are
themselves exact BCFT values of M(2,5), so Phase 1 is Level 1 validation against exact numbers,
independent in *provenance* but not in *content*.

## 9.9 The missing independent extraction (cheap, and it would close the loop)

There is an obvious, cheap cross-check the project has not run and which would convert a
structurally-dependent comparison into a partially independent one:

```
  c_eff  from  E_0(L) = −π v c_eff/(6L)   [Casimir fit on the SAME spectra already computed]
  Δ_φ    from  the 1−φ gap                [already computed, currently used as an INPUT]
  ⇒  c = c_eff + 24 h_min = c_eff + 12 Δ_φ    →  compare against c_KS
```

Every ingredient is already in the L = 10…18 spectra that Phase 2 produced. This would (a) supply
the c_eff number that HYP-028's own mandatory G4 gate demanded and never got
(`HYP-2026-028.json:feasibility_mandatory_gates[3]` requires *"confirm c_eff=2/5 … AND
Delta_phi=-1/5 … BEFORE reporting alpha. If the fixed point is not reached, the result is
INVALID"* — substituted, per `inv-pipelines.md` §5.9, by g₁/R_∞ with no recorded amendment), and
(b) give a second, *algebraically distinct* route to c that does not pass through the KS elements
at all. If the two agree, the KS extraction gains a real independent confirmation. If they
disagree, that is a killer.

**Estimated cost: hours, on data already on disk.** This is the highest value-per-effort item in
the Yang-Lee branch.

## 9.10 HYP-028's founding premise is false, and the hypothesis it answered is not the one it asked

`HYP-2026-028.json` field `claim` states:

> *"In a non-unitary CFT the Delta_T = 2 protection is NOT guaranteed: non-unitary minimal models
> (e.g. Yang-Lee M(2,5), c = -22/5) carry negative central charge, a non-diagonalizable
> (Jordan-block) dilation generator, and primary dimensions that need not be real or bounded by
> the unitary spectrum, so the stress-tensor two-point exchange that fixes alpha=4 in the unitary
> case has no theorem behind it."*

Three defects, in increasing severity:

1. **Δ_T = 2 IS guaranteed.** As derived in §3.1, T is the spin-2 conserved current and
   Δ_T = d = 2 follows from conformal invariance alone. Nothing in the argument uses unitarity,
   positivity, or the sign of c. The manuscript states this correctly
   (`paper-draft-scipost.tex:617`: *"the Yang–Lee edge singularity, c = −22/5, where Δ_T = 2 still
   holds but the unitarity assumptions behind the fusion-rule argument do not"*). The hypothesis
   record contradicts the manuscript.
2. **The Jordan-block escape does not apply to the chosen model.** L₀ is non-diagonalisable in
   *logarithmic* CFTs. **M(2,5) is not logarithmic** — it is a rational, non-logarithmic minimal
   model with a diagonalisable L₀ and two primaries. The record invokes a mechanism that its own
   chosen model does not exhibit.
3. **The mechanism that *can* break α = 4 at Yang-Lee is the fusion rule, and the record does not
   name it.** From §9.2, φ × φ = 1 + **φ**, and Δ_φ = −2/5 < 0. So at the Yang-Lee point the
   φ-probe channel contains a *negative-dimension* primary below the stress tensor, and the leading
   exchange predicts

   ```
      F(dr)  ∼  dr^(−2Δ_φ)  =  dr^(+4/5)
   ```

   — a force that **grows** with separation. That is a spectacular, sharp, cheap, and genuinely
   high-counterfactual-novelty prediction, and it is exactly what HYP-028 originally
   pre-registered: `test_design` step (6), *"Compare alpha to (i) the unitary value 4.0 and
   (ii) the a-priori non-unitary prediction … 2*Delta_phi if the force tracks the
   (negative-dimension) Yang-Lee primary"*, and `refutation_criteria`, which requires α measured at
   N = 12, 14, 16.

**None of that was done.** SIM-071 measured **c**, not α. `HYP-2026-028.json:status` is
`SUPPORTED` and `phase2_result` records the c_KS answer — but the hypothesis's own `claim` and
`refutation_criteria` are about the *force exponent at a non-unitary fixed point*, which remains
untested. The status field answers a different question from the one the record states.
(`inv-hypotheses.md` reached the same conclusion from the record side: *"a SUPPORTED verdict whose
pre-registered criteria were never met."* I confirm it from the physics side and can now say
precisely which experiment is missing.)

## 9.11 Yang-Lee: final grades

| Sub-claim | §8 verdict | §6 novelty | §5 level |
|---|---|---|---|
| c_KS = c given (A1)–(A4) | direct Virasoro identity (★) | zero | — (algebra) |
| The value −22/5 | fixed by the minimal model | near-zero | 1 |
| The **sign** | forced by (★) once (A2) is chosen | near-zero | 1 |
| c_eff = +2/5 "EXCLUDED" | not expressible in the vacuum module | **zero — vacuous** | — |
| Unitary control = 0.49986 | same algebra at c = 1/2 | near-zero | 1 |
| C_TTT imaginary at c < 0 | 2√2/√c with c<0 | zero | — |
| **(A1) holds for a non-Hermitian chain** | **no theorem** | **moderate–high** | **2→3** |
| The k=±2 cluster matches the M(2,5) null-vector structure | predicted, but confirmable | moderate | 2 |
| **The unitary T-ID discriminator inverts** | **not predicted by anything** | **high** | **2** |
| The magnitude −4.29 ± 0.15 | extrapolator + h-fit dependent | n/a | — (see §9.6 R4) |

**Bottom line, stated without softening in either direction.** The Yang-Lee work is a real
methodological contribution whose value lies in demonstrating that a lattice→Virasoro
correspondence with no theorem behind it survives a non-Hermitian, indefinite-metric setting, and
in the *surprising* discovery that the unitary state-identification rule inverts there. Its value
does **not** lie in "measuring c = −22/5" or in "excluding c_eff", both of which were fixed before
the machine was switched on. The manuscript-facing claim should be Track A of §25 — *biorthogonal
lattice Virasoro extraction, its scope, and its failure modes* — with the negative central charge
reported as a **consistency check that the construction passes**, not as the discovery.

---

## 10. Claim-dependency graph (§15)

The governing standard asks for derivations represented as dependency chains, so that "a numerical
success validates an estimator but does not independently validate the final interpretation" is
visible. Here is the graph for the whole program, with **[F]** marking a node whose value is forced
by symmetry/algebra and **[M]** marking a node with genuine measured content.

```
  Virasoro algebra  [F]
    │
    ├── Δ_T = 2  in every 2D CFT  [F]
    │     ├── α ≡ 2Δ_T = 4                                       [F, algebraic doubling]
    │     │     ├── "α=4 universal at c=1/2, 7/10, 4/5"          [F — no force measured at 2 of 3]
    │     │     └── α = 3.92 ± 0.16 at 24q                       [M — but no plateau; §3.6]
    │     ├── v_T ≡ (E_T−E_vac)L/4π  (P3, P4)                    [F by imposition — cancels, §9.5]
    │     └── T-window (1.75, 2.25) at Yang-Lee                  [F by imposition — load-bearing]
    │
    ├── ⟨L₋₂1, L₋₂1⟩ = (c/2)⟨1|1⟩   (★)                          [F]
    │     ├── C_TTT = 2√2/√c                                      [F — a line of code]
    │     │     └── C_TTT ladder 3.9936 / 3.381 / 3.163          [F — = c, error halved]
    │     ├── c_KS(estimator) = c                                 [F — §9.4]
    │     │     ├── c_KS(YL) = −22/5 incl. sign                   [F given (A1)-(A4)]
    │     │     ├── c_eff = +2/5 "excluded"                       [F — vacuous]
    │     │     └── unitary control 0.49986                       [F]
    │     └── C_TTT imaginary at c<0                              [F]
    │
    ├── Kac formula → Δ_σ, Δ_ε, Δ_φ, c per model                  [F]
    │     └── C_σσε = 1/2                                         [F]
    │
    └── (A1) KS lattice → Virasoro, biorthogonal case             [M — NO THEOREM, the real result]
          ├── monotone c_KS ladder −1.41 → −2.36                  [M]
          ├── M(2,5) k=±2 null-vector cluster structure           [M — spectrum only, separable]
          └── T-ID discriminator INVERTS (10×)                     [M — unpredicted, high value]

  MERA architecture
    └── l_AdS ≡ 1/ln χ = 1/ln 2                                   [F by definition]
          ├── m_eff(CFT) = 1/l_AdS = ln 2 = 0.693                 [F]
          │     └── "3.5% agreement" ⇔ ξ_MERA = l_AdS²            [M — 2 points; 24q data give 230%]
          └── T_pred = (π/2)·l_AdS = 2.266                        [F, but π/2 chosen post hoc]
                └── T_meas = 2.239, residual −1.21%               [M — the best comparison in the paper]

  Wang–He boundary Hamiltonian normalisation                      [ASSUMED, undisclosed — §7.2(c)]
```

**Reading of the graph.** Nine of the eleven leaf nodes the project reports as results are
downstream of a **[F]** node with no intervening measurement. Exactly three leaves carry
independent measured content: the transport residual, the 24q force profile (whose content is
adverse to its own headline), and the (A1) subtree. **Every geometry-specific claim in the program
reduces, along this graph, to l_AdS = 1/ln χ — a definition — or to Δ_T = 2 — a theorem.** That is
the concrete, graph-level form of the §3 "central unresolved issue", and it constitutes a partial
answer to §16's request for no-go results: *within the current observable set, no proposed
geometric quantity has been shown to carry information beyond a CFT scaling dimension and an
architectural constant.*

---

## 11. What WOULD have counterfactual novelty (§6, §28)

Derived from the analysis above, ranked by (information gained)/(effort). All four are cheap and
all four have at least two physically meaningful possible outcomes.

**1. Force profile at the tricritical Ising point. [highest]**
*Prediction table, written before the run:*

| Hypothesis | Predicted α at TCI | Meaning if observed |
|---|---|---|
| Conformal-block bookkeeping (ε×ε = 1+ε′) | **2.4** = 2Δ_{ε′} | The α=4 "universality" slogan is refuted; the mechanism the paper advances is confirmed |
| The project's universality claim | 4.0 | The conformal-block mechanism is wrong or the probe is not ε; requires explanation |
| Neither, e.g. ≈ 2 | 2 = 2Δ_ε | Probe-channel contamination dominates (§3.5); explains the Ising shelf at 2.45–2.66 too |

Each outcome changes a decision. Reuses the existing 24q ED force pipeline plus an OF/TCI
Hamiltonian the project already has (`research/tools/merakit-setup/of_build_v2.jl`,
`qw_of_pregate.py`). This is the single test that converts the α programme from Level 1 to
Level 3.

**2. Yang-Lee force exponent — HYP-028's own pre-registered step 6.**
φ × φ = 1 + φ with Δ_φ = −2/5 predicts F ∼ dr^(+4/5), a *growing* force. Outcomes: +0.8 confirms
the negative-dimension primary tracks the force; 4.0 would mean α = 2Δ_T survives even where the
leading channel is a Δ<0 operator, which would be genuinely surprising and would sharpen exactly
the "is α=4 generic?" question HYP-028 was created to ask. The biorthogonal ED at h = h_c^∞ that
Phase 2 already built is the required apparatus.

**3. c from Casimir + Δ_φ, cross-checked against c_KS.** §9.9. Turns a structurally-dependent
comparison into a partially independent one, and retroactively satisfies the abandoned G4 gate.
Data already on disk.

**4. Left eigenvectors by direct solve of Hᵀw = Ew rather than w = Pψ.**
Already recommended by `inv-pipelines.md` §5.4(iii) as the cheapest missing test of the
biorthogonal layer. From the derivation side its value is specific: (A2) is the assumption that
carries the sign, and this is the only test that probes (A2) rather than assuming it.

**Explicitly NOT recommended:** any further extraction of a quantity fixed by symmetry — more
C_TTT rungs, more Δ_T confirmations, more C_σσε basins, more classes on the α ladder.
Per §30, the ruler has been established to be twelve inches long.

---

## 12. Killer tests implied by this analysis (§12)

The standard requires every major hypothesis to have a named killer, documented *before*
interpretation. From the derivation gate:

| Hypothesis | Named killer |
|---|---|
| α = 4 is universal | A TCI force measurement returning 2.4 (§3.4). **This killer is currently unarmed and the hypothesis is recorded SUPPORTED.** |
| α = 4 is stress-tensor exchange | Local exponent has no plateau (§3.6). **Already fired; not recorded as a killer anywhere.** |
| C_TTT ladder is a measurement | It is `2*sqrt(2)/sqrt(c)` in code (§4.2). **Already fired; recorded only in a design doc.** |
| m_eff agreement at 3.5 % | Same model on the 24q dataset gives 230 % (§8.3). **Already fired; not recorded.** |
| Yang-Lee c_KS measures true c | §12's own "Yang–Lee method killer": normalization convention / conditioning / state misidentification. Of these, **state misidentification is live** — the discriminator inverts (§9.6 R3) and identification rests on injected theory. |
| Yang-Lee: c_eff excluded | Cannot be killed — cannot be confirmed either. Vacuous (§9.4 step 4). |
| Transport T = (π/2)l_AdS | Detuning scan already shows T ∈ [0.55, 3.30] under δ = ±0.3 of the same H (`hyp010_criticality_scan.json`, via `inv-manuscript-claims.md` DEF-19). **Fired, omitted from the manuscript.** |
| Emergent geometry has operational content | Every proposed geometric observable reduces along §10's graph to Δ_T = 2 or to l_AdS ≡ 1/ln χ. **This is §12's "independent-prediction killer", and on present evidence it has fired.** |

---

## 13. UNVERIFIED

Stated explicitly rather than passed over, per the task brief.

1. **Potts D-series fusion in the charged sector.** I derived φ_{2,1} × φ_{2,1} = φ_{1,1} + φ_{3,1}
   from the M(6,5) Kac formula and concluded T dominates the neutral channel at Potts. I did
   **not** work out the ℤ₃-charged sector's full OPE content for the D-series modular invariant,
   so the claim "α = 4 is the correct a-priori prediction at Potts" is verified only for a
   ℤ₃-neutral, exactly-ε probe.
2. **Whether the project's TCI/Potts probes would even couple to ε.** No force measurement exists
   at those classes, so there is no probe operator on record to analyse. §3.4's prediction table is
   conditional on the probe being the analogue of the Ising one.
3. **The numerical size of the σ-admixture effect in the Ising probe (§3.5).** I established that
   the −0.026 (X_jZ_{j+1} + Z_jX_{j+1}) term is ℤ₂-odd and therefore opens lower-exponent channels.
   I did **not** compute the resulting amplitude ratios or fit a two-channel model to the recorded
   F(dr). Whether channel contamination *explains* the 2.45–2.66 shelf is therefore a hypothesis,
   not a finding.
4. **Whether the F(dr) shelf at 2.45–2.66 is physical or an open-boundary artifact.** The dr ≥ 9
   upturn is clearly the far boundary of a 24-site OBC chain. Whether dr = 3…8 is clean I did not
   establish; `inv-sims-early.md` §3 reaches the same limit.
5. **The Koo–Saleur normalisation convention in the continuum limit.** I took (A1) in the form
   Ĥ_n → L_n + L̄_{−n} with a single overall normalisation. The additive c-number at n = 0 and any
   n-dependent lattice correction factors were not tracked; they do not affect the ratio structure
   of §9.4 (all normalisation cancels), but a full statement of (A1) with corrections would be
   needed for a theorem-grade result.
6. **The Wang–He boundary-Hamiltonian normalisation (§7.2c).** I identified that T_meas scales as
   1/λ under H → λH while T_pred does not, so the comparison presupposes a canonical normalisation.
   I did **not** verify from the cited construction whether that normalisation is in fact canonical.
   This is a derivational gap in the manuscript, not necessarily an error in the result.
7. **Whether Wang & He's "t_trans = π" can be reconciled with (π/2)·l_AdS by a units convention.**
   I did not read the cited paper (no literature access in this task, and
   `inv-manuscript-claims.md` records that the repo's own paper record contains no such proof).
   The manuscript supplies no reconciliation; whether one exists is open.
8. **P4's raw numbers.** I did not re-run any simulation. All Yang-Lee per-L values quoted here are
   from `SIM-2026-071.json` / `qw_yanglee_ks_results.jsonl` and from `inv-pipelines.md` §5.2's
   independent Python reimplementation, which reproduced them to six decimals.
9. **Whether the M(2,5) φ-module level-2 null vector affects the T-window occupancy at every L.**
   The design doc predicts exactly one φ-descendant below T; SIM-071 reports one; `inv-pipelines.md`
   §5.4 reports a *third* state at D_vac ≈ 3.36 with a 2.8× larger element. I did not check whether
   that third state's identity is accounted for by M(2,5).
10. **Prior art for any of this.** Out of scope for the derivation gate by construction. Nothing in
    this document asserts or denies novelty; §8's literature gate is a separate task and, per
    `inv-pipelines.md` §7.1, has not been run for the Yang-Lee claim.

---

## 14. Prioritised defect list (derivation-gate findings only)

| Sev | Where | What |
|---|---|---|
| **critical** | `research/paper-draft-scipost.tex:45` (abstract) + `SIM-2026-051/052/062/063` + memory index | "α = 4.00 at all three universality classes" is presented as a universality *test*. Δ_T = 2 holds in every 2D CFT (the records say so themselves), and **no force was measured at TCI or Potts** — α there is 2 × a symmetry-fixed number. Counterfactual novelty zero; must be relabelled Level 1. |
| **critical** | `HYP-2026-028.json` field `claim` | Founding premise false: "in a non-unitary CFT the Δ_T = 2 protection is NOT guaranteed". Δ_T = 2 follows from conformal invariance alone; and the Jordan-block mechanism invoked does not apply to M(2,5), which is non-logarithmic. Contradicts the project's own manuscript (`paper-draft-scipost.tex:617`). |
| **critical** | `SIM-2026-071.json:18,21` + `HYP-2026-028.json:phase2_result` | "c_eff = +2/5 EXCLUDED / discrimination decisive" is a **vacuous exclusion**: c_eff = c − 24h_min has no expression inside the vacuum Virasoro module, so this estimator could not have returned it under any state assignment (§9.4 step 4). The genuine content is (A1), not the discrimination. |
| **major** | §3.4, unrecorded anywhere | At TCI the fusion ε×ε = 1 + ε′ places a Δ = 6/5 scalar **below** T, predicting α = 2.4. The project's universality claim is contradicted by the conformal-block mechanism it itself advances. No record considers this. |
| **major** | `SIM-2026-011-interaction.json` `F_interaction_avg` | No power-law plateau: local exponent 2.04 / **4.23** / 2.60 / 2.46 / 2.46 / 2.53 / 2.66 / 2.84 / 3.10 / 3.48 / 4.06. The quoted α = 3.92 ± 0.16 averages a spike and a shelf. (Independent re-derivation of `inv-sims-early.md` A1/A2 by local log-derivatives.) |
| **major** | `effective_mass_analysis.json` + `paper-draft-scipost.tex:266-272` | The "3.5 % m_eff agreement" reduces to ξ_MERA = l_AdS² from a **two-point** (zero-DOF) exponential on the project's *worst* force dataset. The same model on the 24q exact dataset gives m_eff = 2.29, i.e. **+230 %**. Not robust by a factor of ~66. |
| **major** | `SIM-2026-067/068/069` + memory "LADDER COMPLETE" | C_TTT = 2√2/√c is a Virasoro identity and a literal line of code; the square root **halves the quoted error** (verified: 0.5010 / 0.5008 / 0.5005). The ladder's "≤0.15 %" is ≤0.26 % in c. The only independent 3-point route was retracted (`CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117`). |
| **major** | `paper-draft-scipost.tex:170-175` vs `:228,563,631` | π/2 was adopted after the measurement missed π by exactly 2×, with no pre-registration; and the manuscript's only claimed external confirmation states **π**, not π/2, unreconciled, three times. |
| **medium** | `SIM-2026-071.json:17` | "the conformal vacuum is a negative-norm state" is over-read: only the *ratio* ⟨T\|T⟩/⟨1\|1⟩ is convention-free. In M(2,5) the vacuum has **positive** Shapovalov norm and L₋₂\|1⟩ carries c/2 < 0 (§9.7). |
| **medium** | `HYP028-BIORTHO-KS-DESIGN.md:66` | "Sign is now part of the measurement, not a convention" — true only relative to the pairing choice (A2), which is an input. Under the Hermitian inner product the same data give a positive c_KS. |
| **medium** | `qw_yanglee_ks.jl:128-129` | The `(L/2πv_T)²` normalisation cancels identically; c_KS = 8·prod/(E_T−E_vac)². Not a defect in the code, but the record presents a finite-size normalisation that carries no information, obscuring the true dependency structure. |
| **medium** | `paper-draft-scipost.tex:275` + `SIM-2026-011-interaction.json` | The probe operator is named σ_j yet the excitation is identified as ε, and the operator contains a ℤ₂-**odd** term (−0.026 · X_jZ_{j+1}+Z_jX_{j+1}). Channel purity is load-bearing for α = 2Δ_T and is asserted nowhere. |
| **medium** | `HYP-2026-028.json` (6 places) | Δ_φ = −1/5 is the chiral weight h_φ; the scaling dimension is −2/5 (re-derived from the Kac formula). Drivers are correct; the live gate text is not. |
| **minor** | `research/data/theory/` | Empty. Every derivation in this document — (★), the estimator reduction, the fusion-rule channel analysis, the c/c_eff distinction — exists nowhere in the repository as a structured record. §14/§15 call this "a scientific risk"; the derivation gate makes it concrete: the project's interpretation layer is carrying claims whose algebra has never been written down and therefore never been checked. |

---

## 15. Answer to the §24 PRD-referee question, claim by claim

> *"Which results are not fixed by conformal symmetry, standard Virasoro structure, or earlier
> tensor-network CFT work?"*

Prepared answer, honestly:

| Manuscript result | What was known | What was guaranteed | What was measured | What survives deleting "holographic" |
|---|---|---|---|---|
| α = 3.92 ± 0.16 at 24q | α = 2Δ_T = 4 for a pure-ε probe with ε×ε = [1] | the *prediction*, exactly | one interaction-energy profile with no plateau | an interaction-energy profile of two ε-like probes on a critical chain, whose exponent is fit-window dependent |
| α = 4 at TCI and Potts | Δ_T = 2 everywhere | everything | Δ_T from a MERA superoperator | two clean scale-invariant MERA spectra at c = 7/10 and 4/5 (Level-1 validation, genuinely well executed) |
| T = (π/2)·l_AdS to 1.2 % | Wang–He's transport phenomenon; the AdS₃ null condition | the predicted number, once π/2 is chosen | the transport time, grid-converged | **a parameter-free numerical coincidence at the 1 % level between a lattice revival time and 1/(2 ln 2)·π — the only such thing in the paper.** Genuinely notable. |
| m_eff 0.693 vs 0.670 | Δ_ε = 1, BF bound saturation at Δ = d/2 | 0.693 = ln 2 exactly | a two-point decay length | nothing, once the 24q data are used |
| ℤ₂ two-phase ALM+projection | — | nothing | a working optimiser at 24q where single-phase fails | **the method** — Level 2, survives the word test |
| χ=3 force measurement | — | nothing | that χ=3 clears the expressibility barrier | a bond-dimension threshold result |
| (not in manuscript) c_KS at Yang-Lee | c = −22/5; ⟨T\|T⟩ = c/2 | the value and the sign, given (A1)–(A4) | that (A1) survives non-Hermiticity; that the T-ID rule inverts | **the method and the inversion** — the strongest Level-2 content in the program |

The manuscript's §24 word test — *"would the technical contribution still matter if every use of
'holographic' were deleted?"* — is passed by three items (the transport coincidence, the ℤ₂
optimiser, the χ=3 threshold) and failed by the two that the abstract leads with.
