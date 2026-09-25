# adv:alt-explanations — Alternative-Explanation Analysis and Killer-Test List

**Auditor role:** Alternative-Explanation Analyst (RESEARCH-DIRECTOR §27) + Killer-Test Designer (§12).
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` — §5 (contribution levels), §6
(counterfactual novelty), §7 (independence ledger), §8 (novelty gates), §12 (killer tests),
§13 (non-unitary program), §19 (matched controls), §20 (uncertainty; *"would the conclusion
survive a reasonable alternative analysis pipeline?"*), §22 (adversarial numerical tests), §36
(prediction registry), §38 (audit).
**Date:** 2026-08-17. **Repo state:** branch `public-release`, HEAD `9470d69`.
**Primary targets read line by line:** `research/data/simulations/SIM-2026-071.json` (35 lines),
`research/tools/yanglee-pt/qw_yanglee_ks.jl` (152 lines),
`research/tools/yanglee-pt/qw_yanglee_ks_results.jsonl` (5 lines),
`research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md` (95 lines),
`research/data/simulations/SIM-2026-070.json`, `research/data/hypotheses/HYP-2026-028.json`.
**Phase-1 artifacts read first:** `research/data/audit/raw/inv-pipelines.md` (all 843 lines),
`claim-evidence-map.md` (structure + CLM-030 row).

All paths repo-relative to `D:/quantum-worldline/`. Every number below is either quoted from a
tracked file with its field named, or computed by me from tracked numbers (marked **[computed]**)
with the derivation shown so it can be checked.

---

## 0. Executive summary

I evaluated six candidate mundane explanations for the Yang-Lee `c_KS = -4.29 ± 0.15` headline
(SIM-2026-071, claim CLM-030). Verdicts:

| # | Candidate mundane explanation | Verdict | One line |
|---|---|---|---|
| **(a)** | Negative sign is a **normalization convention** | **RULED OUT — by proof** | `c_KS` is a similarity invariant of the pair `(H_{-2},H_{+2})` in the biorthonormal eigenbasis; *every* metric/normalization freedom cancels identically. But the record's supporting narrative ("the conformal vacuum is a negative-norm state — the indefinite metric visible raw") *is* convention-dependent and overclaims. |
| **(b)** | **Eigenvector conditioning** / non-normality | **NOT the cause at L ≤ 18; fatal to the stated next step** | κ_T = 1/\|⟨T_L\|T_R⟩\| = 10.4 → 180.5 over L = 10…18, doubling every ΔL = 2. Harmless at 1e-11 tolerance now; ~1e5–1e6 by L ≈ 40, which forecloses SIM-071's own "puMPS-scale L would sharpen the third digit". |
| **(c)** | **State misidentification** | **NOT RULED OUT — and worse than the record says** | The Δ-gate is *not* tuned (a wide family of windows selects the same state), but the estimator turns out to be nearly **blind** to which of two states it picks: the Δ→3.6 φ-descendant gives a `c_KS` ladder within 1 % of T's at L = 18. And the KS operator's action on the vacuum is **11× dominated by the wrong module** — vs 1.6e-4 contamination in the unitary control. |
| **(d)** | **Exceptional-point proximity** | **NOT RULED OUT — quantitatively serious** | The working point's distance to the finite-size EP shrinks as L^-2.38 while ∂c_KS/∂h grows as L^3.74. The product — the natural scale of the EP-induced systematic — is **1.73 at L = 12 and 2.57 at L = 16, growing as L^1.37, i.e. faster than c_KS itself (L^0.87)**. SIM-070's "no exceptional-point pathology encountered anywhere" is not supported. |
| **(e)** | **Extrapolation artifact** | **NOT RULED OUT — the dominant risk** | Measured values span −1.41…−2.36; the headline is −4.29, so **82 % of the claimed magnitude is extrapolation**. Defensible pipelines give −2.56, −3.65, −3.77, **−4.29**, −4.32, −4.56, −5.10, −5.61, and a two-parameter *divergent* logarithm that fits the five points **18× better** than any two-parameter convergent model. |
| **(f)** | **Shared code path** in the unitary control | **CONFIRMED as a real gap** (phase 1) **plus one new hole** | Beyond `HC=0.0` turning non-Hermiticity off: the control **passes the one test the Yang-Lee run fails**, and nobody ran that test. See §8.3. |

**The single most important new finding in this artifact** (§7.2): the Koo–Saleur estimator is
`c_KS = 2·prod·(L/2πv_T)²`, so `c_KS` converges **only if** the measured product element `prod`
decays as `L^-2`. **[computed]** In the unitary control it does: the implied exponent is
**p = 2.059 / 2.044** at L = 12→14→16. At Yang-Lee it does not: **p = 0.834, 1.008, 1.139, 1.243**
across L = 10…18 (global fit p = 1.031). The Yang-Lee `c_KS` "ladder" is therefore not a converging
sequence of measurements of a constant — it is a power-law growth `|c_KS| ∝ L^0.87`, and the
headline is that growth resummed to a finite value by an estimator with no error model.

The exponent *is* drifting toward the required 2 (0.83 → 1.24, ~+0.13 per rung), so the project's
implicit "asymptotic regime not yet reached" defence is live and I do not claim the result is
wrong. I claim the recorded uncertainty is wrong by more than an order of magnitude, and that the
agreement with −22/5 at 2.6 % is not evidence at the precision stated.

**What survives everything I could throw at it:** the **sign**, and the exclusion of
`c_eff = +2/5`. The sign is a convention-free similarity invariant (§3), it is negative at every L
and both chiralities, and every alternative pipeline in §7 returns a negative number of magnitude
≥ 2.5 — i.e. ≥ 6× |c_eff|, wrong sign. **SIM-071's discrimination verdict is robust. Its precision
claim is not, and its "true c = −22/5 measured with its sign" framing conflates the two.**

---
## 1. What the estimator actually computes (metric-free restatement)

`qw_yanglee_ks.jl:109-129`, verbatim structure:

```julia
pa  = (transpose(lv(ivac)) * (Hm2 * vecs[i])) * (transpose(lv(i)) * (Hp2 * vecs[ivac]))
den = biod(i, i) * n_1                       # <T_L|T_R> * <0_L|0_R>
cks = 2 * prods[jT] * (L/(2pi*v_T))^2        # prods[jT] = pa/den
```

with `lv(i) = conj.(vecs[i][pp])` (L93) and `biod(i,j) = transpose(lv(i))*vecs[j]` (L94), i.e. the
left bra is `v_i† P`. Writing `A = ⟨0_L|H_{-2}|T_R⟩`, `B = ⟨T_L|H_{+2}|0_R⟩`, `N_T = ⟨T_L|T_R⟩`,
`N_0 = ⟨0_L|0_R⟩`:

> **c_KS = 2 · (A·B)/(N_T·N_0) · (L/2πv_T)²**

**[computed] The combination `AB/(N_T N_0)` is exactly the product of two entries of the matrices
of `H_{∓2}` in the biorthonormalised eigenbasis:** if `w_i` are left and `v_i` right eigenvectors
with `⟨w_i|v_j⟩ = δ_ij`, then `AB/(N_T N_0) = (H_{-2})_{0T}·(H_{+2})_{T0}`. Under the only residual
freedom `v_i → a_i v_i`, `w_i → w_i/a_i`, one has `O_ij → (a_j/a_i)O_ij`, so `O_{0T}O_{T0}` is
**invariant**. This is the fact that governs §3 below and it is the honest core of the measurement:
*the object measured is a similarity invariant of the operator pair restricted to two eigen-directions.*

Two inputs are **not** measured but **imposed**, and both matter downstream:

- `v_T = (E_T − E_vac)·L/(2π·2.0)` (`qw_yanglee_ks.jl:128`) — **Δ_T = 2 is imposed, not measured.**
  So the "Δ_T → 2.0 (1.945 → 1.982 monotone)" line in `SIM-2026-071.json:17` is a check on a
  *different* velocity (`v` from the exact Δ_1−Δ_φ = 2/5 split, L86), not an independent
  measurement of Δ_T.
- The conformal vacuum is *defined* as `ivac = i0[2]`, the second k = 0 state (L84), on M(2,5)
  theory input. The 1−φ split is then *used* to fix `v`, so the identification cannot be tested by
  the split. The one genuine internal cross-check is that `v` (from the split) and `v_T` (from the
  T gap) converge: 4.2414/4.1241 (2.8 % apart, L=10) → 4.2841/4.2464 (0.89 % apart, L=18)
  (`qw_yanglee_ks_results.jsonl` fields `v`, `vT`). That check passes and deserves credit; it is
  the only one there is.

---

## 2. Reference data (all from tracked files)

`qw_yanglee_ks_results.jsonl` (n=+2 branch; the n=−2 branch agrees to 10 digits at every L):

| L | c_KS | prod (T) | Δ_vac of the 3 k=2 states | ⟨T_L\|T_R⟩ | v (1−φ) | v_T |
|---|---|---|---|---|---|---|
| 10 | −1.413195 | −4.744597 | 1.4261 / **1.9447** / 3.0145 | 0.096149 | 4.241388 | 4.124143 |
| 12 | −1.702883 | −4.075266 | 1.4659 / **1.9621** / 3.1481 | 0.047856 | 4.259104 | 4.178322 |
| 14 | −1.953729 | −3.489067 | 1.4922 / **1.9722** / 3.2404 | 0.023591 | 4.270367 | 4.211004 |
| 16 | −2.169926 | −2.996681 | 1.5107 / **1.9784** / 3.3065 | 0.011499 | 4.278215 | 4.232070 |
| 18 | −2.356244 | −2.588449 | 1.5241 / **1.9824** / 3.3553 | 0.005539 | 4.284141 | 4.246365 |

Companion elements at each L (the other two cluster states): `prods[1]` = 46.470 / 40.567 / 35.731 /
31.752 / 28.451 (the Δ→1.6 φ-descendant) and `prods[3]` = −12.219 / −10.837 / −9.494 / −8.322 /
−7.335 (the Δ→3.6 φ-descendant — see §5.2 for the module assignment).

Vacuum biorthogonal norms `⟨1|1⟩` are **not** in any tracked artifact. The only recorded values are
those recovered by the phase-1 independent Python port: **−0.010656 (L=10), −0.003996 (L=12),
−0.001507 (L=14)** (`research/data/audit/raw/inv-pipelines.md:382`). I use those and flag the
dependency.

Unitary control (`SIM-2026-071.json:9`): c_KS = 0.517483 / 0.512776 / 0.509748 at L = 12/14/16;
extrapolated 0.49986. No artifact exists (`inv-pipelines.md:653-659`); phase 1 reproduced all three
independently, so I treat them as sound.

---

## 3. (a) NORMALIZATION CONVENTION — **RULED OUT, by proof**

This was flagged as the most important candidate. It is the one I can eliminate.

### 3.1 The suspicion, stated precisely

`SIM-2026-071.json:17` reports *"⟨1|1⟩ biorthogonal norm NEGATIVE at every L (the conformal vacuum
is a negative-norm state — the indefinite metric visible raw)"*, and
`HYP028-BIORTHO-KS-DESIGN.md:13` frames the target as *"CFT says ⟨T|T⟩ = c/2 < 0, so watch the T
biorthogonal norm"*. `HYP028-BIORTHO-KS-DESIGN.md:61-66` says the product form was chosen because it
*"can go NEGATIVE via indefinite biorthogonal norms — which is exactly what c = −22/5 requires."*
Choosing an estimator on the grounds that it is *capable* of producing the desired sign is exactly
the shape of a design-to-answer, so it deserves the hardest look.

**[computed] Where the minus sign numerically comes from.** From the recorded numbers plus phase-1's
`⟨1|1⟩`: at L = 10, `den = ⟨T|T⟩·⟨0|0⟩ = (+0.096149)(−0.010656) = −1.0246e-3`, and since
`prods = pa/den = −4.7446`, the numerator is `pa = +4.861e-3` — **positive**. Same at L = 12
(`den = −1.912e-4`, `pa = +7.793e-4`) and L = 14 (`den = −3.555e-5`, `pa = +1.240e-4`). So:

> **100 % of the sign of `c_KS` is carried by `sign(⟨T_L|T_R⟩·⟨0_L|0_R⟩)`; the numerator is
> positive at every L and carries none of it.** In the CFT the numerator is `(2πv/L)²(c/2)²η₀²`,
> a perfect square — so this is structural, not accidental.

That looks damning: the headline appears to rest on the sign of one exponentially small,
unarchived number, `⟨1|1⟩ ≈ −0.011`.

### 3.2 Why it is nevertheless not a convention — three invariances

**(i) Rescaling / phase invariance (already noted in phase 1, `inv-pipelines.md:493-500`).**
`v_i → α v_i` gives `|α|²` in numerator and denominator; exact cancellation.

**(ii) Global metric sign, η → −η.** Both left vectors flip; numerator gets (−1)², denominator gets
(−1)². `c_KS` unchanged. So "which of ⟨T|T⟩, ⟨0|0⟩ is the negative one" is meaningless — only their
relative sign could matter, and see (iii).

**(iii) The full pseudo-Hermitian metric freedom, η → η·p(H) for any real polynomial p.**
This is the freedom that *can* flip the relative sign of two states' norms independently (choose
p(E_0) > 0, p(E_T) < 0) — including the physically-motivated CPT / C-operator metric of PT-symmetric
quantum mechanics, which is positive-definite by construction and would make **every** norm positive.
**[computed]** Under `η → η·p(H)` the left vector of state i scales by `p(E_i)`. The numerator
contains exactly one bra of state 0 and one of state T, so it picks up `p(E_0)p(E_T)`; the
denominator `⟨T_L|T_R⟩⟨0_L|0_R⟩` picks up the same `p(E_T)p(E_0)`. **Exact cancellation.**

Consequently `c_KS` is invariant under the entire metric family, including the CPT metric under
which the indefiniteness disappears. This is just the statement of §1: the estimator is a function
of `(H_{-2})_{0T}(H_{+2})_{T0}`, which involves no metric at all.

**(iv) Bonus: the "solve `Hᵀw = Ew` directly" test is provably a no-op here.** `inv-pipelines.md:832`
ranks that as *"the single most informative missing test of the biorthogonal layer"*. It is not.
`build_Hn` (L28-51) produces a **complex-symmetric** matrix (real symmetric spin-flip hoppings
`-LAMBDA*sph[j]` placed at both `(s', s)` and `(s, s')`; complex diagonal only), so `Hᵀ = H` and the
true left row-eigenvector *is* `vᵀ`. And with PT unbroken, `P conj(v) = e^{iθ}v` ⟹ `v†P = e^{iθ}vᵀ`
**[computed]**, so the code's `v†P` differs from `vᵀ` by a per-state phase which cancels in the
ratio. Running that test will return the identical number to machine precision. **The informative
test is a metric with a different *signature* — which §3.2(iii) shows also cannot change the
answer — or the state-identification and extrapolation tests below.**

### 3.3 What the record nevertheless gets wrong here

- `SIM-2026-071.json:17` presents `⟨1|1⟩ < 0` as an observation of physics ("the indefinite metric
  visible raw"). **That specific quantity is convention-dependent** (η → η·p(H) flips it) and its
  magnitude is meaningless (the eigenvectors carry an arbitrary normalization; KrylovKit returns
  unit 2-norm). The invariant statement — the one the result actually rests on — is
  `(H_{-2})_{0T}(H_{+2})_{T0} < 0`, and it is stated nowhere.
- `HYP028-BIORTHO-KS-DESIGN.md:44` says *"normalization TBD — the biorthogonal norm can be NEGATIVE;
  both sign conventions must be tracked"*. The tracking was never done and never needed to be; the
  proof above should replace it. **§13 Q3 ("how sensitive is the extracted c to left/right
  eigenvector normalization?") is answerable analytically: exactly zero sensitivity.** That is a
  genuine, publishable Level-2 property of the estimator and the project has not claimed it.

### 3.4 Residual exposure

The invariance holds **given the state pair**. If `|0⟩` or `|T⟩` is the wrong state, the invariant
is the right invariant of the wrong pair. Candidate (a) therefore collapses into candidate (c).

**Test that would still be worth running (cheap, ~1 h):** compute the biorthogonal-norm *signature*
`sign⟨n_L|n_R⟩` for all 24 computed states and compare against the M(2,5) Shapovalov-form signature
(which states carry negative norm in the vacuum and φ Kac modules). If the lattice signature
matches state-by-state, the η = P pairing is demonstrably the CFT metric and the interpretive
narrative is earned. If the signs merely alternate with index (a generic Krein-signature pattern),
the narrative is not earned even though `c_KS` is unaffected. **Neither `⟨φ|φ⟩`'s sign nor any
other state's sign is recorded anywhere** — the driver prints `n_phi` (L96-97) into a discarded
stdout.

---
## 4. (b) EIGENVECTOR CONDITIONING — **not the cause at L ≤ 18; fatal to the stated scaling plan**

### 4.1 How ill-conditioned, exactly

For a complex-symmetric matrix the eigenvalue/eigenvector condition number of a simple eigenpair is
`κ = 1/|wᵀv|` with `w`, `v` unit-norm left/right vectors; here (§3.2 iv) `|wᵀv| = |v†Pv|` = the
recorded `Tnorm`. **[computed]** from `qw_yanglee_ks_results.jsonl`:

| L | ⟨T_L\|T_R⟩ | κ_T | decay ratio per ΔL=2 |
|---|---|---|---|
| 10 | 0.096149 | 10.4 | — |
| 12 | 0.047856 | 20.9 | 2.009 |
| 14 | 0.023591 | 42.4 | 2.029 |
| 16 | 0.011499 | 87.0 | 2.052 |
| 18 | 0.005539 | 180.5 | 2.076 |

`|vᵀv| = 0` is the *definition* of self-orthogonality at an exceptional point, so this quantity is
not merely a "health metric" by analogy — it is the standard EP indicator, and it is being halved
every two sites. The vacuum's is worse: −0.010656 → −0.003996 → −0.001507 (ratio ≈ 2.65),
κ_vac ≈ 94 → 250 → 664, extrapolating to ~4.7e3 at L = 18.

**Answer to "what is the pseudospectral sensitivity at L=18": κ_T ≈ 181, κ_vac ≈ 4.7e3.**
With `tol=1e-11` (`qw_yanglee_ks.jl:72`), double precision, and a k=2 cluster spacing of order
`2πv/L ≈ 1.5`, the induced eigenvector error is ~1e-11·κ/gap ≈ 3e-9 at L = 18. **The recorded L ≤ 18
numbers are not compromised by conditioning**, and phase 1's independent ARPACK port reproducing
them to 6 decimals (`inv-pipelines.md:366-374`) is the empirical confirmation.

### 4.2 But the estimator is a ratio of two exponentials, and that is where it bites

**[computed]** The numerator `pa/⟨0|0⟩ = prods·Tnorm` runs −0.456188, −0.195026, −0.082311,
−0.034460, −0.014337 (ratio **2.34 → 2.40** per ΔL=2) while the denominator factor `Tnorm` decays at
ratio **2.01 → 2.08**. `c_KS` is the residual mismatch of two exponentials whose rates differ by
~15 %. That residual is the entire L-dependence of the result, and it is what §7 shows cannot be
extrapolated reliably.

### 4.3 Consequence for the project's own next step

`SIM-2026-071.json:25` proposes *"puMPS-scale L would sharpen the third digit."* Extrapolating
κ_T = 180.5·2.07^((L−18)/2): **κ ≈ 1.5e4 at L = 28, ≈ 1.1e6 at L = 40, ≈ 4e8 at L = 56** (the N=56
rung P3 actually ran for TCI, `inv-pipelines.md:283`). Double precision has ~16 digits; a
biorthogonal norm of 1e-8–1e-9 relative is at the edge, and an MPS-based method never reaches
machine precision on such an overlap in the first place. **The proposed sharpening is not obviously
possible, and nothing in the record analyses it.** Phase 1 raised this (`inv-pipelines.md:566-568`);
I concur and add the numbers.

**Benign counter-reading (must be stated).** `v†Pv` decaying exponentially in L is generic for a
state that is not parity-symmetric — an extensivity effect, not EP approach. If that is the whole
story the design document's health metric (`HYP028-BIORTHO-KS-DESIGN.md:85`) conflates two things
and is not fit for purpose as written. **Discriminating test (cheap):** hold L fixed and scan h
inward from `h_c^L`; a genuine EP indicator diverges like `(h_c^L − h)^{-1/2}`, an extensivity
factor is flat. One afternoon at L = 12,14.

---

## 5. (c) STATE MISIDENTIFICATION — **NOT ruled out; the record understates the problem**

### 5.1 Is the Δ-gate tuned to the desired answer? — **No, and I checked**

`qw_yanglee_ks.jl:124`: `cand = [j for j in eachindex(idxs) if 1.75 < Dvac[j] < 2.25]`, then
`jT = cand[argmax(abs.(prods[cand]))]` (L127).

**[computed] margins.** Only one state falls inside (1.75, 2.25) at every L, so `argmax` is inert
(phase 1 established this, `inv-pipelines.md:468`). The competitor separations are:

| L | φ-desc Δ_vac | lower gate edge | margin | third state Δ_vac | upper edge | margin |
|---|---|---|---|---|---|---|
| 10 | 1.4261 | 1.75 | 0.324 | 3.0145 | 2.25 | 0.765 |
| 18 | 1.5241 | 1.75 | 0.226 | 3.3553 | 2.25 | 1.105 |
| ∞ (CFT) | 1.6 | 1.75 | **0.15** | 3.6 | 2.25 | 1.35 |

The window is **fixed, shared with the unitary control** (same hard-coded line runs in both modes,
`inv-pipelines.md:416`), and a wide family of alternatives — (1.7, 2.3), (1.65, 2.6),
"pick the Δ closest to 2.0" — selects the same state at every L. **The gate is not fitted to the
answer.** One caveat worth recording: the asymptotic margin to the φ-descendant is only 0.15 in Δ
and the finite-L drift is monotone *toward* the gate (0.324 → 0.226), so the discipline is sound but
thin, and it would have to be re-examined at any larger L.

### 5.2 What the three cluster states are

M(2,5) with Δ_φ = −2/5. Spin-2 states, dimensions measured from the conformal vacuum |1⟩:
φ-tower level-2 (the unique one, φ having a level-2 null) at Δ_vac = 1.6; the vacuum tower's
`T = L_{-2}|1⟩` at 2.0; the φ-tower level-4 spin-2 state at Δ_vac = 3.6. The measured Δ_vac
(1.5241, 1.9824, 3.3553 at L = 18, drifting up) match 1.6 / 2.0 / 3.6. The vacuum module has **no**
spin-2 state between 2 and 6, so **state 3 is a second φ-descendant, not a vacuum descendant.**
`SIM-2026-071.json:17` mentions only the first ("ONE phi-descendant at Delta_vac -> 1.6 below T");
phase 1 noted the third state's larger element (`inv-pipelines.md:475-476`); neither identifies it.

### 5.3 NEW: the estimator is nearly blind to *which* of two states it calls T

The estimator divides by `v_T = Δ_measured·v/2`, so each candidate is rescaled by its own Δ. Define
the reduced element `r_j = prod_j/Δ_j²`, so `c_KS(j) = 2 r_j L²/(π²v²)`. **[computed]**:

| L | r₁ (φ, Δ→1.6) | r₂ (T, Δ→2.0) | r₃ (φ, Δ→3.6) | c_KS if state 1 | c_KS if state 2 (**recorded**) | c_KS if state 3 |
|---|---|---|---|---|---|---|
| 10 | +22.850 | −1.2545 | −1.3447 | +25.740 | **−1.4132** | −1.5147 |
| 12 | +18.879 | −1.0586 | −1.0935 | +30.369 | **−1.7029** | −1.7590 |
| 14 | +16.046 | −0.8970 | −0.9042 | +34.949 | **−1.9537** | −1.9693 |
| 16 | +13.913 | −0.7656 | −0.7611 | +39.434 | **−2.1699** | −2.1572 |
| 18 | +12.248 | −0.6587 | −0.6515 | +43.813 | **−2.3562** | −2.3307 |

Two consequences:

1. **The Δ→3.6 φ-descendant produces a `c_KS` ladder that agrees with T's to 7.2 % at L = 10, 0.8 %
   at L = 14, and crosses it between L = 14 and 16 (−1.1 % at L = 18).** The two reduced elements are
   converging to a *common* value. There is no CFT reason for a φ-tower state to reproduce the
   central charge; a genuinely module-selective measurement would give structurally different
   numbers. **The estimator is not demonstrating that it resolves T.**
2. The *only* thing the Δ-gate has to accomplish is excluding state 1, whose element is opposite in
   sign and ~19× larger in reduced terms. It does so comfortably. So the state-ID risk is not
   "which state got picked" — it is "the observable does not distinguish the picked state from a
   contaminating one".

**Fair counter:** the near-agreement could be a coincidence of finite size, or could reflect that
both states receive the same dominant contamination. Either reading is bad for the claim as stated
and neither is in the record.

**Estimator-instability corollary [computed].** Feed the *state-3* ladder — which differs from the
recorded one by ≤ 7 % and by ≤ 1.1 % at the top two rungs — into the record's own extrapolator
(pairwise 1/L intercepts + geometric tail). Its intercepts are −2.9806, −3.2311, −3.4727, −3.7180,
with diff-ratios 0.964 and 1.015 (≥ 1 ⟹ divergent), so the tail sum returns **+12.09** instead of
−4.29. A ≤ 7 % perturbation of the input flips the output's sign and triples its magnitude. That is
the sharpest available demonstration that "±0.15" is not an uncertainty on this pipeline.

### 5.4 NEW: the Koo–Saleur identification itself is 11× contaminated

`H_{-2}|0⟩` should be `(2πv/L)·L_{-2}|0⟩` + suppressed corrections. **[computed]** from the recorded
products, the T channel carries |prod_T|/|prod_φ| = **0.102 at L = 10 and 0.091 at L = 18** — i.e.
the *contaminating* φ-module channel is ~11× the signal channel, and the ratio is not improving.
In amplitude terms the contaminating element is ~√9.8 ≈ **3.1× larger** than T's.

The unitary comparator, from the project's own puMPS gate: T element 0.498576 vs the other k=2
state's **0.000078** (`inv-pipelines.md:268`), i.e. contamination **1.6e-4 × T**. Between the
control and the measurement, the quality of the Koo–Saleur operator identification degrades by a
factor **≈ 2 × 10⁴ in amplitude**.

Mundane mechanism, entirely conventional: the lattice energy density expands as
`h_x = e₀ + a·φ(x) + b·(T+T̄)(x) + …`, and at Yang-Lee φ is **relevant** (Δ_φ = −2/5 < 0), so its
Fourier mode is *enhanced* with L rather than suppressed. This is the same relevant direction whose
exponent y_φ = 12/5 SIM-070 already measured in the h-sensitivity (`SIM-2026-070.json:17`), and it
is the same mechanism that killed the ED route to TCI in P2 (`inv-pipelines.md:213`: "L₋₂ε at
Δ=2.2, element mixing ~N^−0.2"). **`SIM-2026-071.json:23` reports the 10× inversion as a
methodological curiosity ("Delta-gating above the vacuum is mandatory"). The alternative reading is
that it is a statement that the Koo–Saleur correspondence has not been established at this working
point and these sizes.**

---
## 6. (d) EXCEPTIONAL-POINT PROXIMITY — **NOT ruled out; quantitatively serious**

### 6.1 The working point converges onto the EP locus as L grows

`SIM-2026-070.json:8` records `h_c^L` (the finite-size exceptional point) and `:9` the working point
`h_c^inf = 1.5587127`. **[computed]** distances:

| L | h_c^L | h_c^L − h_c^inf | local exponent −dlog d/dlog L |
|---|---|---|---|
| 8 | 1.5863321 | 0.0276194 | — |
| 10 | 1.5750539 | 0.0163412 | 2.352 |
| 12 | 1.5693276 | 0.0106149 | 2.366 |
| 14 | 1.5660746 | 0.0073619 | 2.374 |
| 16 | 1.5640705 | 0.0053578 | 2.380 |
| 18 | 1.5627601 | 0.0040474 | 2.381 |

The exponent is 12/5 = y_φ to three digits. The PT-edge dodge
(`HYP028-BIORTHO-KS-DESIGN.md:11-15`) is real — every finite L sits strictly inside the PT-unbroken
phase — but it **does not** hold EP distance fixed. **The L→∞ limit being extrapolated and the
EP limit are the same limit.**

### 6.2 The EP-induced systematic does not decouple; it grows faster than the signal

Using phase 1's directly-measured h-sensitivity table (`inv-pipelines.md:510-512`), **[computed]**:

| L | ∂c_KS/∂h (two independent slopes) | dist. to EP | product = natural EP systematic scale | c_KS itself |
|---|---|---|---|---|
| 12 | −161.5 / −165.0 (mean −163.3) | 0.010615 | **−1.733** | −1.7029 |
| 16 | −467.7 / −489.9 (mean −478.8) | 0.005358 | **−2.565** | −2.1699 |

- `|∂c_KS/∂h|` grows as **L^3.74** (factor 2.93 over L = 12→16).
- distance to EP shrinks as **L^-2.38**.
- product grows as **L^1.37** — while `|c_KS|` itself grows only as **L^0.87**.

> **The scale of the working-point/EP systematic is comparable to the entire measured value at
> every L, and its share of the value is increasing with L.**

This is a scale estimate, not a bound: linear response extrapolated over a distance where the true
response is nonlinear (it diverges at the EP). But it is the right order-of-magnitude question to
ask, it uses only the project's own numbers, and it directly contradicts
`SIM-2026-070.json:19`: *"no exceptional-point pathology encountered anywhere in the pipeline."*
That sentence is a statement about the absence of a *visible* singularity at fixed L; it is not
evidence about the L-trend, and the record uses it as though it were.

### 6.3 The one guard that is missing

`qw_yanglee_ks.jl:73` computes `ens = S .- abs.(vals)`. If any eigenvalue acquired an imaginary part
(PT breaking) the `abs` would silently return a plausible real energy and the momentum decoding at
L75 would absorb the phase error into a `round`. Phase 1 flagged this
(`inv-pipelines.md:457-461`); I add the consequence for candidate (d) specifically: **there is no
instrument in Phase 2 that could report EP contamination even if it were happening**, because the
only quantity that would show it (Im E) is destroyed before it is looked at, and the only other
indicator (⟨L|R⟩) is printed without a threshold and thrown away.

### 6.4 Test that would settle it

**h-stationarity scan (§13 "perturbation sensitivity"; ~2–3 h).** At L = 12, 14, 16, compute `c_KS`
at h = h_c^inf and at h = h_c^inf − δ for δ = 1e-3, 3e-3, 6e-3 (still critical to within finite-size
resolution, but 2–10× further from `h_c^L`). If `c_KS(L)` at fixed δ has a *smaller* L-growth
exponent than at δ = 0, the growth is EP-driven and the extrapolation is measuring the approach to
the exceptional locus, not a CFT limit. If the ladder is δ-stationary, candidate (d) is eliminated.
**This is the single highest-value missing experiment in the whole Yang-Lee program** and it is
cheaper than one more rung in L.

---

## 7. (e) EXTRAPOLATION — **NOT ruled out; this is the dominant risk**

### 7.1 The size of the extrapolation

Largest measured value −2.356 (L = 18); headline −4.29. **The reported result is 1.82× the largest
number ever measured; 82 % of the claimed magnitude is supplied by the extrapolator.** For contrast,
the unitary control's largest measured value is 0.5097 against a headline 0.49986 — the control's
extrapolation moves the answer by **1.9 %**. The control therefore validates the estimator and
provides **no validation whatsoever of the extrapolation machinery that produces the Yang-Lee
headline** (see §8).

### 7.2 The Koo–Saleur scaling test — the cleanest single diagnostic

`c_KS = 2·prod·(L/2πv_T)²` with `v_T → const`. **`c_KS` converges if and only if `prod ∝ L^-2`.**
**[computed]** local exponents `p = −dlog|prod|/dlog L`:

| pair | Yang-Lee p (need 2) | | unitary control |
|---|---|---|---|
| 10→12 | 0.834 | 12→14 | **2.059** |
| 12→14 | 1.008 | 14→16 | **2.044** |
| 14→16 | 1.139 | | |
| 16→18 | 1.243 | | |
| global 10→18 | **1.031** | global 12→16 | **2.052** |

Equivalently the growth exponent of `|c_KS|` is `q = 2 − p` = 1.023, 0.891, 0.786, 0.699 at Yang-Lee
(global `|c_KS| ∝ L^0.87`) versus −0.059, −0.044 in the control (flat, as it must be).

**Self-consistency check of the record's own estimator [computed].** Apply the record's geometric-
tail rule to the sequence `q` itself: decrements −0.1313, −0.1055, −0.0866 with ratios 0.803, 0.821,
tail sum ⟹ **q_∞ = 0.302**. The record's own resummation method, applied to the growth exponent,
says the growth exponent does **not** reach zero — i.e. that `c_KS` diverges. The method cannot
simultaneously be trusted to produce −4.29 and be ignored when it predicts divergence.

**Honest counter.** `p` is rising ~+0.13 per rung; a linear continuation reaches 2 near L ≈ 30. The
"asymptotic regime not yet reached" defence is entirely plausible. But a quantity whose *defining*
scaling exponent is measured at 1.03 when the theory requires 2.00 has not been measured; it has
been bounded.

### 7.3 Model selection: a divergent law fits the data best among 2-parameter models

**[computed]** least-squares on all five points, rms of residuals:

| 2-parameter model | rms | implied c_∞ |
|---|---|---|
| `A + B·lnL` (**divergent**) | **1.581e-3** | none |
| `A + B/√L` | 1.477e-2 | −5.101 |
| `A + B·L^0.87` (**divergent**) | 2.515e-2 | none |
| `A + B/L` | 2.908e-2 | −3.494 |
| `A + B/L²` | 5.667e-2 | −2.695 |
| `A + B/L^(12/5)` (theory exponent used in SIM-070) | 6.713e-2 | −2.563 |

The logarithm — same parameter count — fits **18× better than 1/L, 36× better than 1/L², 42× better
than the theory-fixed L^-12/5**, with residuals (−0.0011, +0.0024, −0.0005, −0.0020, +0.0011)
showing no structure. `c(L) = 2.2907 − 1.6081·lnL`.

This also **explains** the record's discarded free-exponent fits. `SIM-2026-071.json:15`:
*"Free-exponent fits are degenerate (w→0 runaway) and discarded honestly."* **[computed]** three
different starting points for `A + B·L^-w` all converge to `w ≈ 0.0014` with rms **1.59e-3** —
numerically identical to the pure-log fit, because `A + B L^-w → (A+B) − Bw·lnL` as `w → 0`.
**The "runaway" is not fit degeneracy. It is the data selecting a divergent law.** The record's
choice to discard it as pathology, rather than report it as the best-fitting model, is the single
most consequential analysis decision in SIM-071 and it is not argued anywhere.

### 7.4 A defensible pipeline zoo — the honest band

**[computed]**, all on the same five recorded points:

| # | Pipeline (all defensible) | Result |
|---|---|---|
| 1 | `A + B/L^(12/5)`, the exponent SIM-070 itself adopted on theory grounds | **−2.563** |
| 2 | `A + B/L²` (2-param) | −2.695 |
| 3 | pairwise 1/L³ intercepts + geometric tail | −3.646 |
| 4 | **pairwise 1/L² intercepts + geometric tail — the variable used for the unitary control** | **−3.770** |
| 5 | `A + B/L` (2-param) | −3.494 |
| 6 | `A + B/L + C/L^(12/5)` (3-param) | −4.185 |
| 7 | **pairwise 1/L intercepts + geometric tail — AS RECORDED** | **−4.285** |
| 8 | `A + B/L + C/L²` (3-param, standard lattice expansion) | **−4.319** |
| 9 | `A + B/L + C/L² + D/L³` (4-param) | −4.561 |
| 10 | `A + B/√L` (2-param) | −5.101 |
| 11 | **genuine two-level Richardson** (Richardson the intercept sequence in 1/L, as the phrase "two-level Richardson" in `SIM-2026-070.json:11` literally describes) | **−5.150 / −5.143 / −5.073** |
| 12 | pairwise 1/√L intercepts + geometric tail | −5.606 |
| 13 | `A + B/√L + C/L` (3-param) | −6.745 |
| 14 | `A + B·lnL` — best 2-param fit | **divergent** |

Plus the phase-1 working-point spread on the *same* estimator #7: **−3.667 / −4.291 / −7.044**
across three defensible `h_c^inf` fits (`inv-pipelines.md:521-525`).

**Exonerating evidence, stated plainly.** Pipeline #8 — arguably the most standard choice for a
lattice observable — gives **−4.319**, and it is *stable* under leave-one-out: **−4.281** (drop
L=18), **−4.318** (all five), **−4.383** (drop L=10), rms 2.4e-4…1.2e-3 **[computed]**. So −4.29 is
not an artifact of one exotic estimator; two independent families land on −4.2…−4.3. That is real
support and the record deserves credit for it (though the record does not cite this fit).

**But**: the same data support −2.56 with a theory-fixed exponent and −5.15 with the estimator the
record's own prose names. The defensible band is roughly **[−5.6, −2.6]**, ~±35 %, against a quoted
**±0.15** (±3.5 %). §20's test — *"would the conclusion survive a reasonable alternative analysis
pipeline?"* — is passed for the **sign** and failed for the **magnitude**.

### 7.5 Sensitivity to the velocity convention (a *negative* finding — this one is robust)

**[computed]** Rebuilding the ladder with `v` (from the exact 2/5 split) instead of `v_T`:
−1.3361, −1.6389, −1.8998, −2.1234, −2.3149; same estimator ⟹ **−4.2345** vs −4.2848, a **1.2 %**
shift. The velocity choice is not a source of the problem.

### 7.6 The tail-ratio lever

**[computed]** `answer = I_last + Δ_last·q/(1−q)` with `I_last = −3.8468`, `Δ_last = −0.164`:

| q | 0.65 | 0.70 | **0.728 (used)** | 0.75 | 0.80 | 0.85 | 0.90 | 0.95 |
|---|---|---|---|---|---|---|---|---|
| answer | −4.150 | −4.228 | **−4.284** | −4.337 | −4.501 | −4.773 | −5.318 | −6.953 |

Only two ratios exist (0.7301, 0.7282), from which `SIM-2026-071.json:15` concludes "STABLE". In the
Phase-1 analogue the ratio sequence **rose monotonically 0.558 → 0.718 over exactly this L range**
(`inv-pipelines.md:594-598`). If Phase 2's ratios behave the same way, q ≈ 0.85 is as likely as
0.728 and the answer is −4.77.

---
### 7.7 An empirically calibrated uncertainty for the record's own estimator

**[computed]** Run the record's extrapolator (pairwise 1/L intercepts + geometric tail) on a ladder
whose answer is *known exactly* (c = 0.5), with the **same number of rungs (5)**, from a **tracked**
repo file — `research/tools/cttt-circle/qw_cttt_circle_results_ising.json`, `c_meas` at
N = 10,12,14,16,18 (**I read these directly**: 0.448547, 0.463848, 0.473251, 0.479427, 0.483693):

| | naive-phase Ising ladder (tracked) | Yang-Lee ladder |
|---|---|---|
| rungs | 5 (N = 10…18) | 5 (L = 10…18) |
| raw top rung | 0.483693 | −2.356244 |
| remaining gap to the known/claimed answer | **3.26 %** | **46.4 %** |
| intercepts | 0.540353, 0.529669, 0.522659, 0.517821 | −3.1513, −3.4588, −3.6833, −3.8468 |
| diff ratios | 0.656, 0.690 (**rising**) | 0.7301, 0.7282 |
| estimator output | **0.507045** | −4.2848 |
| error vs known answer | **+1.41 % (overshoot)** | unknown |
| **error ÷ remaining gap** | **0.432** | — |

Applying that calibration factor to the Yang-Lee case: expected estimator error ≈
0.432 × 46.4 % ≈ **20 %**, i.e. **± 0.86 on |c_KS| = 4.29** — roughly **6× the quoted ±0.15**, and in
close agreement with the independent pipeline-zoo band of §7.4 ([−5.6, −2.6]).
A second calibration on phase 1's half-bond ladder (4 rungs, gap 0.32 %) gives error/gap = 0.56
(0.500888 vs 0.5, `inv-pipelines.md:239-247` — **second-hand, not re-derived by me**).
This is the cheapest available honest error bar and it uses only data the project already has.
Note also that the calibration ladder's diff ratios **rise** (0.656 → 0.690), as SIM-070's did
(0.558 → 0.718) — the geometric-tail assumption is violated in both known-answer cases and the
estimator overshoots in both.

### 7.8 One thing that is *not* an independent check

`SIM-2026-071.json:16` cites "both chiralities". **[computed]** the n=+2 and n=−2 values agree to
1e-13…7e-11 relative at every L. They must: `H_{-2} = P·H_{+2}†·P` for this Hamiltonian, and both
branches are evaluated on the same eigenvectors with the same orientation-selection logic
(`qw_yanglee_ks.jl:109-116`). This is a numerical-plumbing consistency check, not a second
measurement, and should not be listed among the result's supports.

---

## 8. (f) SHARED CODE PATH — what the MODE flag cannot catch

Phase 1 established the structural facts (148/152 shared lines; `HC=0.0` switches non-Hermiticity
off; biorthogonal norms exactly +1 in the control; conditioning κ = 1 by construction;
cross-state biorthogonality never checked; no PT guard) — `inv-pipelines.md:391-490`. I do not
repeat them. Three additions specific to the alternative-explanation question:

**8.1 The control passes the exact test the measurement fails, and nobody compared them.**
§7.2: the control's KS product scales as `L^-2.05`, as the Koo–Saleur relation demands; the
Yang-Lee product scales as `L^-1.03`. That comparison is available from data already in the repo,
costs nothing, and is the most informative number the control can produce. It is not in
`SIM-2026-071.json`.

**8.2 The control cannot detect the dominant failure mode, because in Ising that mode is 10⁴×
weaker.** Module contamination is 1.6e-4 in the puMPS Ising gate and 3.1 (i.e. > 1) at Yang-Lee
(§5.4). A control operating at 1.6e-4 contamination is structurally incapable of exercising the
regime where the measurement lives. Under §19 (*"a serious control should be capable of defeating
the preferred interpretation"*) this control cannot.

**8.3 The control never exercises the extrapolator, which supplies 82 % of the answer.**
Control: 3 rungs (L = 12,14,16), extrapolation moves the answer 1.9 %. Measurement: 5 rungs,
extrapolation moves the answer 82 %, using a *different* extrapolation variable (1/L for the
measurement, 1/L² for the control, `SIM-2026-071.json:10`). Two different estimators were used for
the two halves of the same result, and only the low-leverage half was validated.

**8.4 The MODE flag changes three things at once** (`qw_yanglee_ks.jl:23-25, 84, 86`: λ, h, `ivac`,
and the `v` reference). A discrepancy could not be attributed. The missing intermediate controls
are: (i) λ = 4, h = 0 (Hermitian, same λ as the measurement — isolates the model from the
non-Hermiticity); (ii) λ = 4, small h ≪ h_c (weakly non-Hermitian, still flowing to Ising —
**the only configuration that exercises the biorthogonal layer against a known c = 1/2**); (iii) a
synthetic non-normal matrix with prescribed biorthogonal structure. (ii) is the one I would build
first: it turns the binary Hermitian/non-Hermitian switch into a continuous dial with a known
answer at every setting.

---

## 9. Ranked verdict on the alternative explanations

| Rank | Explanation | Ruled out? | What would settle it | Cost |
|---|---|---|---|---|
| 1 | **(e)** Extrapolation model choice + estimator with no error model | **NO — dominant** | Rungs at L = 24/28 (see killer K-1); publish the pipeline zoo; adopt the §7.7 calibrated band | rungs: days; analysis: 1 h |
| 2 | **(d)** Working point converging onto the EP locus | **NO** | h-stationarity scan at fixed L (§6.4) | 2–3 h |
| 3 | **(c)** Module contamination / non-selectivity of the estimator | **NO** | State-3 ladder must be reported alongside T's; module-purity metric per L; second non-unitary model | 1 h + 1 model |
| 4 | **(b)** Conditioning | **YES at L ≤ 18** (κ ≤ 181 vs tol 1e-11; independent ARPACK port agrees to 6 dp) — **NO beyond L ≈ 30** | extended-precision rerun at one L; κ projection before any puMPS-scale attempt | 1 h |
| 5 | **(f)** Shared code path | Structural gap **CONFIRMED**; not itself an explanation of the number | control (ii) of §8.4: λ=4, small h, known c=1/2 | half a day |
| 6 | **(a)** Normalization convention | **YES — by proof** (§3.2) | none needed; publish the invariance instead | 0 |

**Net position.** The Yang-Lee result should currently be stated as:

> *At L ≤ 18 the biorthogonal Koo–Saleur product element for the state identified as T is negative
> at every size and both chiralities. Under the range of extrapolation models the data admit, its
> L→∞ magnitude lies in roughly [2.6, 5.6]; the recorded central value −4.29 is reproduced by the
> most standard 3-parameter 1/L fit (−4.32) and is not reproduced by theory-fixed-exponent fits
> (−2.56) or by a literal two-level Richardson (−5.15). The sign, and hence the exclusion of
> c_eff = +2/5, is a similarity invariant and is robust to every normalization, metric and
> pipeline tested. Whether the sequence converges at all is not established: the KS product element
> scales as L^-1.03 where convergence requires L^-2, and a divergent logarithm fits the five points
> better than any two-parameter convergent model.*

That is still a genuinely interesting Level-2 methodological result (§5), and arguably a *more*
interesting one, because "the KS operator at a non-unitary point is contamination-dominated and its
scaling exponent is halved" is a real, new, reportable statement about when the method works.

---

## 10. §12 KILLER TEST LIST

One named outcome per surviving major hypothesis that would force rejection or sharp weakening.
Format: **[ID] hypothesis → killer outcome → why it kills → cost.** Hypothesis statuses read from
`research/data/hypotheses/HYP-2026-0NN.json` (`status` field) on 2026-08-17.

### K-1 — Yang–Lee method killer (the §12-mandated one) · HYP-028 [SUPPORTED/medium], CLM-030

**Test.** Compute `c_KS` at **L = 24 and L = 28** (2^24 / 2^28 sparse non-Hermitian Arnoldi;
momentum-resolved, so the k = ±2 sector can be projected first). Register the three predictions
**before running** (§36):

| L | converging to −22/5 (record's reading) | log-divergent (best 2-param fit) | power-divergent `−0.1937·L^0.87` |
|---|---|---|---|
| 24 | −2.709 | −2.820 | −3.075 |
| 28 | −2.873 | −3.068 | −3.517 |
| 40 | −3.193 | −3.641 | −4.796 |
| 100 | −3.741 | −5.115 | −10.645 |

(the "converging" column is `−4.4 + B·L^-0.66` anchored on the L = 18 point; the standard
3-parameter `A + B/L + C/L²` fit predicts −2.764 / −2.956 / −3.327 / −3.901, i.e. it is nearly
degenerate with the log reading out to L = 40 — which is itself a finding: **L ≤ 40 does not
discriminate them**.)

**Killer outcome (any one):**
1. **|c_KS| exceeds 4.400 at any L.** Under every reading in which the sequence converges to −22/5
   from below in magnitude, this is impossible. **[computed]** the power-law reading crosses 4.4 at
   **L ≈ 36**; the log reading crosses at L ≈ 64. A single point above 4.4 kills "converging to the
   true central charge" outright.
2. **The local scaling exponent `p` of the product element stalls below ~1.6.** Convergence requires
   p → 2. Measured 0.83 → 1.24 over L = 10…18. If p is still ≤ 1.6 at L = 28, the sequence is not
   entering the asymptotic regime and the resummation is unsupported.
3. **The h-stationarity scan (§6.4) shows the L-growth exponent depends on δ = h_c^inf − h.**
   Then the growth is EP-approach, not CFT finite-size, and the L→∞ limit is not a CFT limit.

**Also kills the interpretation, cheaply, without new L:** if the **Δ→3.6 φ-descendant** ladder
(§5.3) extrapolates to a value consistent with −22/5 under *any* pipeline, the estimator is not
module-selective and "we measured `c` via `⟨T|H_{-2}|1⟩`" is unsupported.

**Cost:** L = 24 is ~16 M states — feasible with a k-sector projection; L = 28 needs the puMPS or a
matrix-free momentum-sector build. h-scan and the state-3 report: hours.
**Pre-registration required before the run** (§36).

### K-2 — Yang–Lee **sign** killer (separate, because the sign is the robust part)

**Test.** Two independent routes to the same bit. (i) **A second non-unitary universality class**
with a *different* known sign structure — the non-Hermitian 5-state Potts of arXiv:2607.14732,
already sitting in PAPER-133's reference list and named in `HYP028-BIORTHO-KS-DESIGN.md:87`.
(ii) The **weakly non-Hermitian Ising control** of §8.4(ii) (λ = 4, small h), where the answer must
remain +1/2 and positive.
**Killer:** `c_KS` returns a **negative** value for the weakly non-Hermitian Ising control at any h
where the model still flows to c = 1/2, **or** returns a sign at the second non-unitary model that
disagrees with that model's known `c`. Either shows the negative sign is produced by the
non-Hermitian machinery rather than read off the theory.
**Cost:** (ii) is half a day and should be done first — it is the missing rung between the
Hermitian control and the measurement.

### K-3 — Novelty killer · CLM-032, `SIM-2026-071.json:22`

`SIM-2026-071.json:22` asserts *"First lattice extraction (to our knowledge) of a NEGATIVE central
charge from stress-tensor matrix elements."* §8 forbids the phrase without a recorded gate, and
`inv-pipelines.md:746-756` finds **no literature-gate record anywhere in the repo**.
**Killer:** a single prior paper extracting `c < 0` (or `c` with its sign) from lattice Virasoro /
Koo–Saleur / transfer-matrix generators in a non-unitary chain. Search terms are already enumerated
in §8 of the standard. Until the gate is run, the sentence must be struck, not softened.
**Cost:** one literature session. **This is the cheapest killer on the list and the only one that
can be executed today.**

### K-4 — Emergent-geometry killer (§12's named one) · Hypothesis B of §4; CLM-043; HYP-002 [PARTIALLY_CONFIRMED], HYP-011 [proposed]

**Matched-control test.** Build a **non-geometric ansatz matched on ordinary CFT data** — the
obvious candidate already in the repo's toolchain is a **puMPS** ground state at the same N,
matched on: energy density, Δ_σ, Δ_ε, Δ_T, `C_σσε`, entanglement entropy at one cut, and parameter
count. Then measure the geometry-specific observable (the α = 4 force from boundary stress-tensor
excitations; and the Synge distance of HYP-026) in **both**.
**Killer:** the matched non-geometric control reproduces α = 4 and the Synge distance profile to
within the MERA's own scatter. Then the "emergent geometry" carries no observable content beyond
the CFT data used to match, and CLM-043's "quantitative gravitational content" must be withdrawn.
**Prediction to register first:** under Hypothesis A the control matches; under Hypothesis B it does
not. **I expect the control to match**, because α = 2Δ_T = 4 is kinematic in every 2D CFT — which
is precisely why this is the right experiment: it is the first one in the program with a genuinely
uncertain outcome and a decisive interpretation either way.
**Cost:** the puMPS pipeline exists (P3) and already produces the required spectra; the force
measurement is P5 code. Days, not weeks. **This is the flagship §39 project.**

### K-5 — Gauge/rewiring killer · CLM-015 (`l_AdS = 1/lnχ`), HYP-026 [SUPPORTED/medium]

**Test.** Apply (i) harmless MERA gauge transformations on internal legs, (ii) a rewiring that
preserves boundary-state fidelity to within the χ-truncation error, and (iii) a χ change at fixed
physics. Re-extract every geometric quantity: `l_AdS`, the Synge distance profile, the layer-depth
force crossover.
**Killer:** any of them changes by more than the boundary-observable error changes. `l_AdS = 1/lnχ`
is an *architecture parameter*, not a measurement, and it appears on the theory side of CLM-010,
CLM-016 and CLM-017 while also being an input to state construction
(`claim-evidence-map.md:416`). If the "geometry" tracks χ rather than the state, it is a property of
the representation (§34), and the transport and m_eff agreements become circular.
**Cost:** cheap — MERAKit already produces multiple χ; the χ-ladder data partly exist.

### K-6 — Universality killer · HYP-008 [SUPPORTED/med], HYP-025 [SUPPORTED/med], HYP-027 [status field reads `TESTABLE_NEAR_TERM`, i.e. **a feasibility verdict in the status slot** — see `inv-hypotheses.md`], HYP-030 [proposed]; CLM-004

**The claim as recorded is not what was measured.** α = 4 was measured as a *force exponent* only in
critical Ising; at TCI and Potts only Δ_T ≈ 2 was measured, and in P3/P4 `v_T` is *defined* by
imposing Δ_T = 2 (`inv-pipelines.md:693`), so Δ_T is not measured there at all.
**Killer:** measure the *force* exponent (not Δ_T) in the tricritical-Ising and 3-state-Potts MERAs
with the same P5 protocol used for Ising. If α lands outside [3.2, 4.8] at either class, HYP-025/027
fall by their own registered criteria. **Equally killing in the other direction:** if α = 4 is
recovered, it confirms only a kinematic identity (Δ_T = 2 in *every* 2D CFT) and CLM-004 must be
relabelled Level 1 with near-zero counterfactual novelty.
**Cost:** the MERAs exist (SIM-051/052/062/063); the force protocol is P5 code.

### K-7 — Force-exponent robustness killer · HYP-008, CLM-001

`inv-sims-early.md` established that dropping the single point dr = 2 moves α from 3.92 to 2.56 /
2.75 / 2.75 across all three "independent" evaluations — ~8× the quoted ±0.16, same direction each
time.
**Killer:** publish the full fit-window matrix (every contiguous dr window, every anchor) with the
exponent for each. If no window family gives a plateau, α = 3.92 ± 0.16 is not a measurement of a
power law and CLM-001/CLM-005/CLM-008 must be restated as "consistent with, and not distinguishable
from, a range 2.5–4.1". **Cost: one afternoon; the data are on disk.** This is the second-cheapest
killer here and it targets the *manuscript's* central number.

### K-8 — Transport killer · HYP-006 [SUPPORTED/high], CLM-010…CLM-014

**Killer A (control):** the gap-matched non-AdS control already failed once (HYP-024
[NOT_ESTABLISHED]). Run the strongest version: a **non-MERA** critical state (puMPS or exact ED)
matched on gap and velocity. If it also yields T ≈ (π/2)·l_AdS within the −1.21 % residual, the AdS
geodesic reading adds nothing.
**Killer B (external anchor):** CLM-014 — the paper's only claim of independent external validation
("Wang & He analytically proved t_trans = π") is **absent from the project's own record of the cited
paper** (`inv-manuscript-claims.md`). If a direct read of arXiv:2501.03084 does not contain that
statement, the claim must be withdrawn from the submitted PRD manuscript by erratum.
**Cost:** B is one paper read and is **urgent** — the manuscript is under editorial review
(accession DV13971).

### K-9 — `C_TTT` ladder killer · CLM-026, SIM-067/068/069

`C_TTT = 2√2/√c` appears as a **literal line of code** in every driver
(`qw_cttt_circle.py:203`, `qw_cttt_of.jl:116-117`, `qw_cttt_potts3.jl:131-132`).
**Killer:** none needed — it is already algebraically equivalent to the `c` measurement and there is
nothing to falsify. The required action is a **relabel**, not a test: the "three-rung C_TTT ladder"
is a three-rung central-charge ladder, Level 1, near-zero counterfactual novelty. The one genuinely
independent 3-point route (equal-time `⟨hhh⟩`) was correctly killed by the project itself
(`CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117`). **Stop condition (§31) reached; the branch should be
formally closed with a record.**

### K-10 — Methods-paper killer · the L₋₂ε contamination-suppression result (SIM-068, Level 2)

This is the repo's strongest *methodological* candidate (`inv-pipelines.md:293-296`).
**Killer:** a literature gate finding the suppression already documented for puMPS Bloch states
(ZMV and successors), **or** a demonstration that the ~400× suppression at N = 56 is a property of
the vendored `Hn_in_basis` structural momentum projection rather than of the Bloch-state
construction. Either would move it from Level 2 to Level 1.
**Cost:** one literature session + one ablation run.

### K-11 — Hardware-budget killer · HYP-029 [SUPPORTED (conditional, LOW)]

Recorded caveat: the 8×8 T-count is **inferred**, not measured (memory index; HYP-029
`confidence: low`).
**Killer:** an explicit logical-resource compile of the MERA state-prep + force-correlator circuit
whose volume exceeds the arXiv:2606.25011 8×8 TFIM datapoint by > 10× — the hypothesis's own
registered criterion (a). Until that compile exists the status should read **conditional /
unverified**, not SUPPORTED.

### K-12 — Record-integrity killer (infrastructure; §32/§36)

**Killer condition, already met:** `inv-hypotheses.md` finds seven hypothesis records still reading
`proposed` after their own SIMs refuted them, and `inv-infrastructure.md` finds 9 of 20 statuses
disagreeing between memory and disk. `inv-errata-history.md` finds ERRATA.md frozen at 2026-06-08
with zero of ~27 later reversals. **A project whose structured records cannot answer "which
hypotheses are refuted?" cannot make a defensible novelty or priority claim about anything.**
The remedy is not a test but a freeze-and-reconcile pass, and it should precede any new
simulation (§38 is explicit that the audit comes before the next large run).

---
## 11. Defects found (this artifact's own list)

Only items **not already** in `inv-pipelines.md §9` are listed as new; overlaps are marked.

| Sev | Where | What |
|---|---|---|
| **critical** | `SIM-2026-071.json:15,27` | The extrapolation model is unjustified and its uncertainty is understated ~6×. A matched, tracked, known-answer calibration of the *same* estimator gives error/gap = 0.432, implying **±0.86**, not ±0.15. Defensible pipelines span [−5.6, −2.6]. (Extends `inv-pipelines.md` §5.6, which measured only the `h_c^inf` lever.) **NEW** |
| **critical** | `SIM-2026-071.json:15` | *"Free-exponent fits are degenerate (w→0 runaway) and discarded honestly."* The runaway is not degeneracy — the free fit converges to `w ≈ 0.0014`, rms 1.59e-3, i.e. **to a logarithm**, which fits the five points 18× better than any 2-parameter convergent model. The best-fitting model of the recorded data has **no finite limit**, and this is nowhere argued. **NEW** |
| **critical** | `qw_yanglee_ks.jl:129` + records | The Koo–Saleur product element scales as `L^-1.03` where convergence of `c_KS` requires `L^-2`; the unitary control on the same code path gives `L^-2.05`. The single most diagnostic comparison the control can supply was never made. **NEW** |
| **major** | `SIM-2026-070.json:19` | *"no exceptional-point pathology encountered anywhere in the pipeline"* is not supported: the working point's distance to the finite-size EP shrinks as L^-2.38 while `∂c_KS/∂h` grows as L^3.74, so the EP-scale systematic (1.73 at L=12, 2.57 at L=16) grows as L^1.37 — faster than `c_KS` itself (L^0.87). **NEW** |
| **major** | `SIM-2026-071.json:17,23` | The Δ→3.6 state is a **second φ-descendant** (the vacuum module has no spin-2 state between Δ=2 and Δ=6) and it yields a `c_KS` ladder within 1.1 % of T's at L = 18, converging toward T's. The estimator does not demonstrate module selectivity. Only the Δ→1.6 state is mentioned in the record. **NEW** |
| **major** | `SIM-2026-071.json:17` | *"the conformal vacuum is a negative-norm state — the indefinite metric visible raw"*: `⟨1\|1⟩` alone is **convention-dependent** (η → η·p(H) flips it) and its magnitude is meaningless under unit-2-norm eigenvectors. The invariant that actually carries the result — `(H_{-2})_{0T}(H_{+2})_{T0} < 0` — is stated nowhere. **NEW** |
| **major** | `SIM-2026-071.json:16` | "both chiralities" is presented as support; the two branches agree to 1e-13…7e-11 because `H_{-2} = P·H_{+2}†·P` on the same eigenvectors. It is a plumbing check, not a second measurement. **NEW** |
| **major** | `SIM-2026-071.json:22` | "First … (to our knowledge)" with no §8 gate anywhere. (Concurs with `inv-pipelines.md` §7.1; restated here as killer **K-3** because it is the cheapest actionable item in the program.) |
| medium | `HYP028-BIORTHO-KS-DESIGN.md:44,61-66` | The estimator is documented as chosen because it *"can go NEGATIVE"*, and normalization is left "TBD — both sign conventions must be tracked". The tracking was never done; the correct resolution is the invariance **proof** of §3.2, which the project has earned and not claimed. **NEW** |
| medium | `inv-pipelines.md:832` (phase-1 recommendation #2) | "Solve `Hᵀw = Ew` directly … the single most informative missing test" is provably a **no-op**: `build_Hn` is complex-symmetric and PT-unbroken eigenvectors give `v†P = e^{iθ}vᵀ`, so the phase cancels in the ratio. Correcting a *recommendation*, not a result. **NEW** |
| medium | `SIM-2026-071.json:25` | *"puMPS-scale L would sharpen the third digit"* is unsupported: κ_T doubles every ΔL = 2, reaching ~1e6 at L = 40. Nothing analyses whether the biorthogonal construction survives there. (Concurs with `inv-pipelines.md` §5.7.) |
| minor | `qw_yanglee_ks.jl:124` | The Δ-gate's asymptotic margin to the φ-descendant is only 0.15 (window edge 1.75 vs CFT 1.6) and the finite-L drift is monotone toward it. The gate is *not* tuned — I checked alternative windows and the "closest to Δ=2" rule, all of which select the same state — but the margin should be recorded. **NEW (exonerating + caveat)** |

## 12. UNVERIFIED

Stated explicitly rather than passed over.

1. **`⟨1|1⟩` and every biorthogonal norm sign except T's.** The driver prints them
   (`qw_yanglee_ks.jl:96-97`) into a discarded stdout; only `Tnorm` reaches the tracked `.jsonl`.
   My §3.1 sign decomposition uses the values recovered by phase 1's Python port
   (`inv-pipelines.md:382`), which I did **not** re-derive. **The sign of `⟨φ|φ⟩` — the physical
   ground state — is not recorded anywhere and I could not obtain it.**
2. **The M(2,5) Shapovalov signature comparison (§3.4).** Not run by anyone. I assert only that it
   *would* discriminate "η = P reproduces the CFT metric" from "generic Krein alternation".
3. **Whether `⟨T_L|T_R⟩` decay is EP proximity or extensivity.** Same open question phase 1 flagged
   (`inv-pipelines.md:781-783`). I added the scaling numbers, not the discrimination.
4. **Cross-state biorthogonality `⟨ψ_i^L|ψ_j^R⟩` for i ≠ j.** Never computed by the driver, by
   phase 1, or by me. If the k = 0 / k = ±2 states are not mutually biorthogonal, the product-form
   denominators are ill-defined and §3's invariance argument (which assumes a biorthonormal
   eigenbasis) has a gap.
5. **The module assignment of the third cluster state (§5.2).** I argue it is the φ-tower level-4
   spin-2 state from Δ_vac → 3.6 and the absence of any spin-2 vacuum descendant between Δ = 2 and
   Δ = 6. I did **not** verify this against an explicit M(2,5) character/null-vector computation.
6. **My forward predictions (K-1 table) are model extrapolations, not measurements.** The
   "converging" column is anchored on L = 18 with an assumed w = 0.66; the log and power columns are
   my fits. They are registered here so K-1 can be scored, not asserted as knowledge.
7. **Second-hand citations I relied on but did not re-derive:** the puMPS Ising gate elements
   (0.498576 / 0.000078, `inv-pipelines.md:268`); the half-bond ED ladder
   (`inv-pipelines.md:239-247`); the `h_c^inf` sensitivity tables (`inv-pipelines.md:510-525`);
   `yl_run_8_18.log`'s "GATE: NOT PASSED"; the α fit-window numbers from `inv-sims-early.md`; the
   Wang & He external-validation gap from `inv-manuscript-claims.md`; the status-mismatch counts
   from `inv-hypotheses.md` / `inv-infrastructure.md`. **Directly verified by me:** all of
   `SIM-2026-071.json`, `SIM-2026-070.json`, `qw_yanglee_ks.jl`, `qw_yanglee_ks_results.jsonl`,
   `HYP028-BIORTHO-KS-DESIGN.md`, all 30 hypothesis `status` fields,
   `qw_cttt_circle.py:203`, and the tracked naive-phase Ising ladder in
   `qw_cttt_circle_results_ising.json`.
8. **Novelty.** I ran **no** literature search and make **no** novelty judgement in either
   direction. K-3 records that the gate is missing; that is a statement about the repo, not about
   the literature.
9. **I did not re-run any simulation.** Every "[computed]" item is arithmetic on tracked numbers
   (scripts: `alt_pipelines.py`, `alt2.py` in the session scratchpad; they should be committed
   alongside the missing analysis scripts `inv-pipelines.md:838` already asks for).

## 13. Closing position

The Yang-Lee work is the only place in this repository where, before the calculation, more than one
physically meaningful outcome was possible (§6 counterfactual novelty: **moderate-to-high**, the
only such entry — `inv-pipelines.md:716-722`). That makes it worth defending properly rather than
overselling.

What it has earned: a **sign**, which is a similarity invariant immune to every normalization,
metric and pairing freedom (§3), reproduced independently at the raw-number level, and which
excludes `c_eff = +2/5` by ≥ 6× in magnitude under every pipeline I could construct. That is a
real, reportable, Level-2 methodological result — *"the biorthogonal Koo–Saleur element pair is
negative at a non-unitary fixed point, so the construction is sensitive to structure the Casimir
energy cannot see."*

What it has not earned: **−4.29 ± 0.15**, "measures the TRUE central charge c = −22/5", and
"2.6 % at ED scale". Those require the sequence to converge, and the sequence's own defining
exponent is measured at 1.03 where 2.00 is required, in a regime where the contaminating module
carries 11× the signal, at a working point whose distance to the exceptional locus is shrinking
faster than the signal grows. The honest magnitude statement today is **|c_KS| ∈ [2.6, 5.6]**,
consistent with 22/5 and with a good deal else.

Killer **K-1** (rungs at L = 24/28 with the three predictions pre-registered), killer **K-2** (the
weakly non-Hermitian Ising control), and the §6.4 h-stationarity scan would settle it. Killer
**K-3** (the literature gate) costs one session and must happen before any priority language
survives into a manuscript.





