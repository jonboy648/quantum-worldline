# novelty:yanglee-arxiv — Literature-Adversary Report on SIM-2026-071

**Auditor role:** Literature adversary (RESEARCH-DIRECTOR.md §8 novelty gate, §27 "Literature adversary",
§38.D novelty audit). **Mandate:** destroy the novelty claim if it can be destroyed; default to NOT NOVEL
when equivalents are found.
**Date:** 2026-08-17. **Repo:** `D:/quantum-worldline`, branch `public-release`, HEAD `9470d69`.
All repo paths below are relative to `D:/quantum-worldline/`.

---

## 0. Verdict up front

**VERDICT: NOT NOVEL** for the headline as written in `research/data/simulations/SIM-2026-071.json`.

The record's two headline sentences are:

> `SIM-2026-071.json:21` — *"the Koo-Saleur stress-tensor construction SURVIVES non-unitarity and measures
> the TRUE central charge c = -22/5, including its indefinite-metric sign -- NOT the effective (Casimir)
> charge c_eff = 2/5. The biorthogonal element structure sees what the energy spectrum cannot."*
>
> `SIM-2026-071.json:22` — *"First lattice extraction (to our knowledge) of a NEGATIVE central charge from
> stress-tensor matrix elements; standard approaches obtain only c_eff from Casimir scaling."*

Both are pre-empted:

1. **The conceptual claim** (a biorthogonal left/right construction on a non-Hermitian critical lattice chain
   recovers the *true* negative `c` rather than the positive `c_eff`) is **Couvreur–Jacobsen–Saleur, PRL 119,
   040601 (2017), arXiv:1611.08506** — nine years prior, and their paper names the Yang-Lee case
   (`c = -22/5` vs `c_eff = 2/5`) explicitly in its introduction.
2. **The specific observable claim** (Koo–Saleur lattice stress-tensor Fourier modes, evaluated with a
   *biorthogonal* pairing on a non-Hermitian PT-symmetric critical chain, generate a Virasoro algebra with a
   **negative** central charge, with the conformal data extracted from the lattice at finite size) is
   **Io, Huang & Hsieh, arXiv:2602.02649** — v1 2026-02-02, v2 2026-04-06, i.e. **six months before
   SIM-071 (2026-08-11)**. Their §"Lattice realization" says verbatim: *"To test conformal symmetry directly
   on the lattice, we employ the Koo-Saleur construction [37, 38]"*, and their Eq. (S77) is `c = -2`.
3. **Sentence 2's premise is false as stated.** "Standard approaches obtain only c_eff from Casimir scaling"
   is contradicted by a continuous 2016–2026 literature of biorthogonal lattice methods that obtain the
   *true, negative* `c` (arXiv:1611.08506; 1909.01346; 2107.13006; 2502.02001; 2602.02649).
4. The phrase **"to our knowledge"** is one of the four phrases RESEARCH-DIRECTOR §8 forbids *"until the
   evidence for them has been recorded."* No such evidence is recorded: `SIM-2026-071.json` contains **zero**
   occurrences of `prior_art`, `novelty`, or `literature` (verified by grep), and
   `research/data/hypotheses/HYP-2026-028.json` has no prior-art field either.

A narrow residue survives (§6 below) and is real but small: it is Level 1–2 under §5, not a discovery.

---

## 1. What exactly was searched, and how

Per the mandated protocol, every arXiv export-API query was fired **strictly sequentially with ≥4 s spacing**
(`Start-Sleep -Seconds 4` before each `Invoke-WebRequest`), each response was parsed as XML and checked for a
non-zero `totalResults` and topical hits before the next query. Zero HTTP 429s; zero dropped query lines.
No OR-query with 4+ phrases was used. The token `puMPS` was never searched.

| # | Query (arXiv export API `search_query=`) | Total | Outcome |
|---|---|---|---|
| 0 | `id_list=2606.16785` | 1 | Sanity check: PAPER-133 exists, v2 dated 2026-07-30. API live. |
| 1 | `all:"Koo-Saleur"` | 7 | **Decisive.** Yielded 1706.01436, 1710.05397, 2010.12819, 2007.11539, 2107.13834, 1907.10704 |
| 2 | `id_list=2010.12819,2007.11539,1706.01436,2107.13834` | 4 | Abstracts |
| 3 | `au:"Grans-Samuelsson"` | 12 | No part-II; series is complete at 2007.11539 + 2010.12819 |
| 4 | `au:"Couvreur" AND cat:cond-mat.stat-mech` | 5 | **Decisive.** 1611.08506 |
| 5 | `id_list=1611.08506,1809.07429` | 2 | Abstracts |
| 6 | `abs:"non-Hermitian" AND abs:"central charge"` | 28 | **Decisive.** 2602.02649, 2107.13006, 1909.01346, 2502.02001, 2607.25256, 2211.12525, 2405.01640 |
| 7 | `id_list=2107.13006,1909.01346,2502.02001,2602.02649,2607.25256` | 5 | Abstracts |
| 8 | `abs:"biorthogonal" AND abs:"Virasoro"` | 2 | Only 2602.02649 (+1 unrelated math paper) |
| 9 | `abs:"Yang-Lee" AND abs:"central charge"` | 10 | von Gehlen hep-th/9402143; Wydro–McCabe cond-mat/0510190; no KS |
| 10 | `abs:"negative central charge"` | 20 | 2107.13006, 2211.12525, 2208.12169, 2405.01640 |
| 11 | `abs:"effective central charge" AND abs:"nonunitary"` | 6 | 2512.21808 (Pearce et al.), 2606.30720 |
| 12 | `abs:"effective central charge" AND abs:"non-unitary"` | 12 | 1611.08506, 1405.2804, 1502.03275, 1509.04601, 1706.01871 |
| 13 | `abs:"Virasoro" AND abs:"non-Hermitian"` | 2 | 2602.02649, 2408.08241 |
| 14 | `abs:"lattice Virasoro"` | 7 | 1907.10704, 1212.1378 (Gainutdinov–Saleur–Tipunin) |
| 15 | `abs:"PT-symmetric" AND abs:"Ising" AND abs:"conformal"` | 3 | 2606.16785, 2510.13581, 2407.20106 |
| 16 | `au:"Kohei Kawabata" AND cat:cond-mat.stat-mech` | 22 | No KS work; PAPER-133 is his only KS-adjacent paper |
| 17 | `au:"Yijian Zou"` | 30 | No non-Hermitian KS from the Zou/Milsted/Vidal line |
| 18 | `abs:"biorthogonal" AND abs:"central charge"` | 5 | 2606.32035, 2602.02649, 2311.11251, 2310.07599, 1909.01346 |
| 19 | `abs:"true central charge"` | 0 | Confirms the phrase is not an abstract-level term of art |
| 20 | `ti:"Logarithmic conformal field theory: a lattice approach"` | 1 | 1303.2082 |
| 21 | `id_list=2509.09587,2510.13581,2311.11251,1303.2082` | 4 | Abstracts |

**Google Scholar (paper-search MCP), 2 queries** — used because the arXiv API indexes only title/abstract/
comments, and the decisive hit cites Koo–Saleur only in its *body*:

- `"Koo-Saleur non-Hermitian biorthogonal central charge lattice"` → top hit **2602.02649**, returned with the
  snippet *"… on the lattice, we employ the Koo-Saleur construction [37…"*. Second hit: L. Liu PhD thesis
  (2023), *"Emerging Jordan forms, with applications to critical statistical models and conformal field
  theory"* (the Saleur-school lattice-Virasoro line).
- `"Koo-Saleur" Yang-Lee non-unitary central charge stress tensor matrix elements` → **1303.2082**
  (Gainutdinov–Jacobsen–Read–Saleur–Vasseur review) with snippet *"…the case p = 5 and q = 2 describes the
  Yang–Lee … Adding to it the conjectured Koo–Saleur formula (49) for the …"*; and Eck & Wang (2026), 3d fuzzy
  sphere, *"…by the Koo-Saleur formulas via the Fourier transform … the non-unitary Yang-Lee CFT …"*.

**Full texts read (not just abstracts):** 2602.02649 (main text + SM §IV, complete), 2107.13006 (main text),
1611.08506 (main text + the RSOS supplement section), 2010.12819 (targeted sections 3.3, 7.2, Appendix A),
2311.11251 (complete).

---

## 2. Decomposition of the claim under test

To be fair to the record, I split the headline into six separately falsifiable sub-claims.

| ID | Sub-claim | Source line |
|---|---|---|
| **C1** | A biorthogonal (left/right eigenstate) construction on a non-Hermitian critical **lattice chain** can access the **true** `c` rather than `c_eff`. | `SIM-2026-071.json:21` |
| **C2** | The **Koo–Saleur** lattice stress-tensor Fourier-mode construction specifically survives non-unitarity and yields the true `c`. | `SIM-2026-071.json:21`; `HYP028-BIORTHO-KS-DESIGN.md:40-58` |
| **C3** | The **sign** of `c` (indefinite metric) is recoverable from a lattice measurement. | `SIM-2026-071.json:16,21` |
| **C4** | "Standard approaches obtain **only** `c_eff` from Casimir scaling." | `SIM-2026-071.json:22` |
| **C5** | **First** lattice extraction of a negative `c` **from stress-tensor matrix elements**. | `SIM-2026-071.json:22` |
| **C6** | The specific number `c_KS = -4.29 ± 0.15` at the Yang-Lee point of the PT-Ising chain, from biorthogonal KS elements at L ≤ 18. | `SIM-2026-071.json:14,15,18` |

---

## 3. Prior-art register (ranked by threat)

### P1 — **Io, Huang & Hsieh, arXiv:2602.02649** — *"Non-Hermitian free-fermion critical systems and logarithmic conformal field theory"* (v1 2026-02-02, v2 2026-04-06, cond-mat.str-el)

**THE NEAREST PRIOR WORK. This is the paper that kills C2 and C5.**

*What it does, quoted from the text I read:*

- Abstract: *"Working in the **biorthogonal formalism**, we identify the conformal structure of this theory by
  constructing a traceless energy-momentum tensor whose **Fourier modes generate a Virasoro algebra with
  central charge c = −2**. … We further present a microscopic construction and show how the same conformal
  data (with finite-size corrections) can be **extracted from the lattice model** at exceptional-point
  criticality."*
- Main text, "Lattice realization": *"To test conformal symmetry directly on the lattice, **we employ the
  Koo-Saleur construction [37, 38]**."* Their refs [37] = Koo & Saleur, Nucl. Phys. B 426, 459 (1994),
  hep-th/9312156; [38] = Milsted & Vidal, PRB 96, 245105 (2017), arXiv:1706.01436 — **the identical two
  references the Quantum Worldline pipeline rests on.**
- Their Eq. (25)/(S68) is, up to notation, the **same object** as `research/tools/yanglee-pt/qw_yanglee_ks.jl`
  builds:
  `H_n^latt = L_n^latt + L̄_{−n}^latt := (Na/2πv_F) Σ_j e^{−i2πnj/N}(h_j − h_∞) + (c/12)δ_{n,0}`
- Their SM §IV rewrites `H_n`, `P_n` **in the biorthogonal eigenmode basis** `χ_{L/R}(p)`, `η_{L/R}(p)` defined
  by `S_L†(p) H(p) S_R(p) = diag(E,−E)`, `S_L†(p)S_R(p) = 1` (Eq. S56–S58) — i.e. exactly the left/right
  pairing SIM-071 calls its contribution.
- Eq. (S77): *"Evaluating commutators among H_n and P_n, and hence among L_n = (H_n+P_n)/2 and
  L̄_n = (H_{−n}−P_{−n})/2, we find that, in the scaling limit, the algebra converges to a Virasoro algebra …
  with **c = −2**."*
- They also report **finite-size lattice extractions with explicit 1/N² corrections** of the level-1 and
  level-2 indecomposability parameters: `β_1^latt = −1 + (17/48)(2π/N)² + O(N⁻⁴)`,
  `β_2^latt = −18 + (125/4)(2π/N)² + O(N⁻⁴)` (Eqs. 27 / S89 / S93).
- Their introduction already frames the problem the way SIM-071 does: *"recent studies of PT-symmetric lattice
  models have reported unusual universal signatures at EP criticality, such as entanglement-entropy scaling
  consistent with a **negative or even complex-valued central charge** [13–19]"* — citing 1611.08506,
  1909.01346, 2107.13006, 2502.02001 among others.

**EXACT OVERLAP with SIM-071:** non-Hermitian PT-symmetric critical lattice chain; biorthogonal left/right
pairing; Koo–Saleur Fourier modes of the local Hamiltonian density; a **negative true central charge** read out
of those modes; lattice-side finite-size analysis of the resulting conformal data; and the same two founding
citations (Koo–Saleur 1994, Milsted–Vidal 2017).

**EXACT DIFFERENCE:**
1. **Model / universality class.** Io et al.: free-fermion tight-binding chain with alternating hopping and a
   staggered *imaginary* onsite potential, at a second-order **exceptional point**, → `c = −2` **logarithmic**
   CFT (staggered Virasoro modules, symplectic-fermion-like `β_M`). QW: interacting PT-symmetric Ising chain
   `H = −Σ(σ^z σ^z + λσ^x + i h σ^z)` at λ=4, `h = h_c^∞`, → Yang-Lee **M(2,5)**, `c = −22/5`, a *rational*
   non-unitary minimal model, deliberately **away** from the EP (`HYP028-BIORTHO-KS-DESIGN.md:83` — *"Do NOT
   work at h_c^L (exceptional point — defective, no biorthogonal basis)"*).
2. **Estimator.** Io et al. read `c` from the **central term of the commutator** `[L_m,L_n]`, evaluated
   analytically in the scaling limit (their model is quadratic, so this is exact). QW reads `c` from a
   **single off-diagonal matrix element** —
   `c_KS = 2⟨0_L|H_{−2}|T_R⟩⟨T_L|H_{+2}|0_R⟩/(⟨T_L|T_R⟩⟨0_L|0_R⟩)·(L/2πv_T)²`
   (`research/tools/yanglee-pt/qw_yanglee_ks.jl:129`) — i.e. the Milsted–Vidal estimator, numerically, on a
   finite-L ladder with an extrapolation.
3. **Nature of the lattice result.** Io et al.'s lattice `c = −2` is *derived*, not fitted; their fitted
   finite-size quantities are `β_1, β_2`, not `c`. QW's `c_KS(L)` ladder with an extrapolated value and a
   quoted uncertainty is a genuinely numerical, interacting-model measurement.
4. **The `c` vs `c_eff` framing** is explicit in QW and implicit in Io et al. (at `c = −2`, the corresponding
   `c_eff = c − 24h_min = −2 + 3 = 1`, so a true-vs-effective fork exists there too, but the paper does not
   put it in those words).

**Consequence for C2 and C5:** the *class* of result — "biorthogonal Koo–Saleur lattice modes carry a negative
true central charge in a non-Hermitian critical chain" — was in the literature, on arXiv, in a
`cond-mat.str-el` posting, **six months and nine days before SIM-071 was recorded**.

---

### P2 — **Couvreur, Jacobsen & Saleur, PRL 119, 040601 (2017), arXiv:1611.08506** — *"Entanglement in non-unitary quantum critical spin chains"*

**Kills C1, C3 and C4.**

- Abstract: *"We show that the consideration of **left and right eigenstates** combined with appropriate
  definitions of the trace leads to a natural definition of Rényi entropies in a large variety of models. …
  This allows us to **distinguish the role of the central charge and effective central charge** in rational
  minimal models of CFT."*
- Introduction, verbatim: *"For instance, for the Yang-Lee singularity, **c = −22/5 but c_e = 2/5**."*
  — i.e. **the exact numerical fork SIM-071 presents as its discrimination result is stated as the setup of a
  2016 paper.**
- Body: *"We derive (1) for minimal non-unitary models, and **define modified EE involving the true c even in
  non-unitary cases**."*
- Coulomb-gas section: *"For the critical QG invariant XXZ chain with H = −Σe_i, the EE S̃ scales as expected
  in CFT, but with the **true central charge c = 1 − 6/(x(x+1))** (instead of `c_e = 1`)."*
- Supplement, section heading: *"**Extracting the real central charge in the non-unitary case** — We describe
  now the general construction of a modified trace in the RSOS models that will enable us to **extract the true
  central charge from the entanglement, even in the non-unitary case**."*
- They give the general A_m RSOS family `c = 1 − 6p²/[(m+1)(m+1−p)]`, `c_eff = 1 − 6/[(m+1)(m+1−p)]`, and state
  *"The case (m,p) = (4,3) gives the **Yang-Lee singularity universality class**"* — which is exactly
  `c = −22/5`, `c_eff = 2/5`.
- **Numerics:** their figure at `M = 400` sites shows three curves: the unmodified trace scaling with
  `c_XXZ = 1`; the modified trace with non-contractible-loop weight `n_1 = 2cos(π/5)` scaling with
  `c_e = 3/5`; and the modified trace with `n_1 = n`, where *"the scaling then involves the **true central
  charge c = −3/5**"* — a **lattice measurement of a negative true `c`, side by side with the positive `c_eff`
  of the same model.**

**EXACT OVERLAP with SIM-071:** left+right (biorthogonal) eigenstates on a non-Hermitian critical spin chain;
an explicitly constructed pairing/trace that is *not* the positive-definite one; the resulting quantity scales
with the **true, negative** `c`, not `c_eff`; demonstrated numerically on a lattice; the Yang-Lee
`c = −22/5` / `c_eff = 2/5` pair named as the canonical example.

**EXACT DIFFERENCE:** the observable is **Rényi/entanglement entropy with a quantum-group-modified trace**, not
Koo–Saleur stress-tensor matrix elements; the numerical demonstration shown is at `c = −3/5` (m,p)=(4,2), not
at Yang-Lee itself; and the models are quantum-group/supergroup-symmetric TL chains and RSOS models, not the
`i h σ^z` PT-Ising chain.

---

### P3 — **Grans-Samuelsson, Jacobsen & Saleur, arXiv:2010.12819** — *"The action of the Virasoro algebra in quantum spin chains. I. The non-rational case"* (61 pp.)

**Kills the "which pairing?" and "does KS survive?" framing of RESEARCH-DIRECTOR §13 Q1–Q2 as open questions,
and supplies an unaddressed adverse result.**

- Abstract: *"We investigate the action of discretized Virasoro generators, built out of generators of the
  lattice Temperley-Lieb algebra (**"Koo-Saleur generators"**) … In order to obtain **matrix elements of
  Koo-Saleur generators** at large system size N we use Bethe ansatz and Quantum Inverse Scattering methods …
  We also study **in which sense Koo-Saleur generators converge to Virasoro generators** … We find that it
  coincides **only up to the central term**."*
- §3.3 "The choices of metric": *"Two possible scalar products can be introduced in the CFT. The one for which
  `a_n† = a_{−n}` … is positive definite … A crucial observation is that for this scalar product
  **`L_n† ≠ L_{−n}`**."* And in Appendix A: *"we see that this dagger operation is **the one that exchanges
  left and right eigenstates in the non-Hermitian case**. This conformal scalar product is the continuum limit
  of the loop scalar product … **It is not, in general, positive definite.**"*
  → The indefinite-metric / biorthogonal-pairing choice that SIM-071 treats as its methodological novelty is
  set out here, with a derivation, in 2020.
- §7.2, the **adverse** result the QW record does not engage with: their conjecture (136) is
  `[L_m, L_n] = (m−n)L_{m+n} + δ_{m+n,0}·(1/12)(m³c − m c̃)`, with `c̃ ≠ c`. In their words: *"Although the
  relation in (136) is no longer the expected relation of the Virasoro algebra at central charge c…"*, and
  *"the central term is wrong by a constant term, rather than by an operator."*
  They further checked the Shokrian-Zini–Wang modified KS phases (1706.08497, Conjecture 5.5) and found:
  *"while the numerical values show a faster convergence, **the change of the central term is the same** as
  with the original Koo-Saleur generators."*

**Why this matters adversarially:** SIM-071's estimator extracts `c` from **one matrix element**, and the
project has never tested the KS *algebra* (`[L_m,L_n]`) on any model, unitary or not. GJS is direct evidence
that the KS construction has a **known anomaly precisely in the central term** — the quantity SIM-071 claims
to measure. That is an alternative explanation for a residual (SIM-071 quotes −4.29 vs −4.400, a 2.6 % miss)
that the record attributes entirely to finite size (`SIM-2026-071.json:25`).

**Companion:** **arXiv:2007.11539** (Grans-Samuelsson, Liu, He, Jacobsen, Saleur) does the same for the
**non-unitary, logarithmic** Potts/loop models at generic Q — *"a careful study of 'Koo–Saleur generators' …
combined with measurements of four-point amplitudes"* — i.e. KS generators used as a measurement instrument in
a demonstrably non-unitary lattice theory, in 2020.

---

### P4 — **Tu, Tzeng & Chang, SciPost Phys. 12, 194 (2022), arXiv:2107.13006** — *"Rényi entropies and negative central charges in non-Hermitian quantum systems"*

**Reinforces the kill on C1/C3/C4 with explicit numbers.**

- *"one can define a reduced density matrix which involves the **left and right eigenstates** in non-Hermitian
  systems. In this definition, the entanglement entropy is no longer guaranteed to be positive and **leads to a
  possibility to obtain the negative central charge**."*
- Their footnote 1 states the `c_eff` alternative explicitly: *"the true central charge is replaced by an
  effective central charge `c_eff` which is positive … `c_eff = c − 24h`, where h is the conformal weight of
  the ground state with `h < 0`."*
- **Numerical lattice extractions of the true negative c** (Fig. 1e–h, two-legged non-Hermitian SSH):
  `c = −1.99999, −2.00003, −2.00105` (n = 1,2,3) and `c = −3.99992, −4.00026, −4.00564` at a two-EP point.
- **A continuous family of negative c on an interacting spin chain**: the q-deformed critical XXZ chain with
  imaginary boundary terms, `c = 1 − 6θ²/[π(π−θ)]`, extracted by **Lanczos exact diagonalisation of left and
  right ground states up to L = 32** (their §2.2, Fig. 2b–f), giving e.g. `c_odd = −0.5440 / c_even = −0.6424`
  at `θ = 2π/5`, and `c ≈ −1.955/−2.035` near `θ = π/2`.
- Appendix C proves *"the equivalency of the generic entanglement entropy and the quantum group entanglement
  entropy"* of Couvreur–Jacobsen–Saleur.

**Overlap:** biorthogonal ED on a non-Hermitian critical chain at ED-comparable sizes (L ≤ 32 vs QW's L ≤ 18);
numerically extracted **negative true central charges** with explicit contrast against `c_eff`.
**Difference:** entanglement entropy, not KS matrix elements; models are SSH / q-deformed XXZ / AKLT, not the
Yang-Lee PT-Ising chain; no value at `−22/5`.

---

### P5 — **Chang, You, Wen & Ryu, Phys. Rev. Research 2, 033069 (2020), arXiv:1909.01346**

*"We propose a method of computing and studying entanglement quantities in non-Hermitian systems by use of a
**biorthogonal basis** … at a critical point in the PT symmetric SSH model, the entanglement entropy has a
logarithmic scaling with corresponding **central charge c = −2**. This critical point then is a free-fermion
lattice realization of the non-unitary conformal field theory."*

Six years before SIM-071: negative true `c` from a biorthogonal lattice construction. Same statement,
different observable.

---

### P6 — **Shimizu & Kawabata, Phys. Rev. B 112, 085112 (2025), arXiv:2502.02001** — *"Complex entanglement entropy for complex conformal field theory"*

Same senior author as PAPER-133 (2606.16785), the paper HYP-028 Phase 1 reproduces.
*"This is based on **non-Hermitian reduced density matrices constructed from the combination of right and left
ground states**. Applying the density matrix renormalization group to non-Hermitian systems, we numerically
calculate the **complex entanglement entropy of the non-Hermitian five-state Potts model**, thereby confirming
the scaling behavior predicted by complex conformal field theory."*

Relevance: the exact research group whose paper the project reproduced was, six months earlier, already
extracting **complex-valued** (hence certainly non-`c_eff`) central charges from biorthogonal lattice data.
This is the strongest available evidence that the project's framing ("standard approaches obtain only c_eff")
misdescribes the field it is publishing into.

---

### P7 — **Gainutdinov, Jacobsen, Read, Saleur & Vasseur, J. Phys. A 46 (2013) 494012, arXiv:1303.2082** — *"Logarithmic Conformal Field Theory: a Lattice Approach"*

Review, retrieved via Google Scholar with the snippet: *"…non-unitary CFTs are known, whose central charges
are … For instance, the case p = 5 and q = 2 describes the **Yang–Lee** … Adding to it the conjectured
**Koo–Saleur formula (49)** for the …"*.

Abstract also establishes the lattice-measurement-of-stress-tensor-sector-data tradition:
*"…provides an 'experimental' way of measuring couplings, such as the **'number b' quantifying the logarithmic
coupling of the stress energy tensor with its partner**."*

So the pairing "Koo–Saleur formula + Yang-Lee/non-unitary lattice CFT" is at minimum thirteen years old as an
explicit programme statement.

---

### P8 — **Osborne & Stottmeister, arXiv:2107.13834** — *"Conformal field theory from lattice fermions"*

*"we prove the **convergence of the approximation of the Virasoro generators by the Koo-Saleur formula**"*, with
a v3 comment *"including comment on **modified Koo-Saleur formula**"*. Rigorous-convergence context that the
project's records do not cite.

---

### P9 — model-family prior art on the PT-Ising chain itself

- **Lu, Deng, Kou & Sun, PRB 110, 014441 (2024), arXiv:2311.11251** — *"Many-body phase transitions in a
  non-Hermitian Ising chain."* One-dimensional TFIM with an imaginary field, PBC, **biorthogonal density
  matrix** `ρ^{RL} = |φ_R⟩⟨φ_L|/Tr(...)`, ED at L = 10…20, and *"an approach to perform finite-size scaling
  theory to **extract the central charge for small systems**"*, obtaining `c = 0.501` vs exact 0.5, and
  reporting that the **biorthogonal normalisation `√|⟨ψ_L|ψ_R⟩|` collapses near the exceptional point** (their
  Fig. 5), which is the same conditioning pathology flagged at `inv-pipelines.md §5.7`.
  *Difference:* their imaginary field is on `σ^y` (removable by a similarity transformation → ordinary Ising
  `c = 1/2`), not the `i h σ^z` that reaches Yang-Lee. Model-adjacent, not the same fixed point.
- **Zhang, Mao, Hu, Zhao, Sun & You, PRB 112, 155135 (2025), arXiv:2510.13581** — Yang-Lee edge singularity in
  the non-Hermitian PXP model via **biorthogonal entanglement entropy and biorthogonal Loschmidt echo**,
  extracting critical exponents *"which agree with the predictions of non-unitary conformal field theory."*
- **von Gehlen, hep-th/9402143** (1994) and **J. Phys. A 24 (1991) 5371** — the original imaginary-field
  Ising/Blume-Capel lattice route to Yang-Lee; **Wydro & McCabe, cond-mat/0510190** — YL-edge excitation
  spectrum from a lattice transfer matrix.
- **Chou, Yu & Chang, arXiv:2509.09587** — PT-symmetry-enriched non-unitary criticality, `c = −2`, biorthogonal.
- **Xiao & Ryu, arXiv:2607.25256** (2026-07-28) — a caution the project should read: in critical non-Hermitian
  free fermions, log-scaling coefficients *"vary continuously with the parameters and form a Rényi family that
  **no single central charge can reproduce**"*, traced to eigenvector **nonorthogonality**.

---

### P10 — the estimator itself is not the project's

- **Koo & Saleur, Nucl. Phys. B 426, 459 (1994), hep-th/9312156** — the construction. **Not cited by arXiv ID
  anywhere in the repository** (`grep -rIl -F "9312156"` → no hits outside vendored/ignored trees).
- **Milsted & Vidal, PRB 96, 245105 (2017), arXiv:1706.01436** — *"Extraction of conformal data in critical
  quantum spin chains using the Koo-Saleur formula."* This is where `c = 2|⟨T|H_{±2}|0⟩|²` as a practical
  lattice estimator comes from. It *is* cited (`SIM-2026-034.json`, `RESEARCH-LOG.md`,
  `research/data/simulations/sim034_koosaleur_stress_tensor.py`).
- **Zou, Milsted & Vidal, PRL 121, 230402 (2018), arXiv:1710.05397** — the puMPS route; cited in
  `SIM-2026-067.json`, `NEXT-SESSION.md`.

So the estimator, the mode discretization, and the identification machinery are all inherited. The only
project-side change is replacing `⟨T|` with `⟨T_L|` and dividing by biorthogonal norms.

---

## 4. Sub-claim verdicts

| ID | Verdict | Nearest prior work | One-line reason |
|---|---|---|---|
| **C1** | **NOT NOVEL** | arXiv:1611.08506 (2016/PRL 2017) | CJS define left+right-eigenstate entropies on non-Hermitian critical chains that scale with the **true** `c`, and name Yang-Lee `c=−22/5` vs `c_eff=2/5` as *the* example. Reinforced by 2107.13006, 1909.01346, 2502.02001. |
| **C2** | **NOT NOVEL** | **arXiv:2602.02649** (2026-02-02) | Io–Huang–Hsieh build biorthogonal **Koo–Saleur** lattice Virasoro generators on a non-Hermitian PT-symmetric critical chain and obtain **c = −2**; they cite Koo–Saleur 1994 and Milsted–Vidal 2017, i.e. the same lineage. 6 months prior. |
| **C3** | **NOT NOVEL** | 1611.08506; 2107.13006 | Negative (and in 2502.02001, complex) `c` values measured on lattices with sign, from indefinite-metric constructions, since 2016. |
| **C4** | **FALSE AS STATED** | 1611.08506; 1909.01346; 2107.13006; 2502.02001; 2602.02649 | "Standard approaches obtain **only** `c_eff`" is true of *Casimir/finite-size-energy* scaling and of the *naive* (right-only) entanglement entropy. It is not true of "standard approaches" — the biorthogonal-entropy method that gets true `c` is itself now standard and has a 2017 PRL. |
| **C5** | **NOT ESTABLISHED; on the evidence, NOT NOVEL** | arXiv:2602.02649 | Under the narrowest defensible reading ("from KS stress-tensor Fourier modes"), Io et al. did it first. The only residue is estimator form (single matrix element vs commutator central term) and model (interacting M(2,5) vs free-fermion c=−2 LCFT). That is a difference in *instance*, not in *kind*. |
| **C6** | **PARTIALLY NOVEL (as a datapoint), LOW VALUE** | none found | I found no published `c = −22/5` obtained from Koo–Saleur matrix elements on a Yang-Lee lattice chain. The number itself appears to be new. See §5 and §6 for why this is worth little. |

---

## 5. Derivation gate (RESEARCH-DIRECTOR §8, second gate)

*Is the number fixed once known assumptions are accepted?*

- `c = −22/5` is the defining central charge of the minimal model **M(2,5)**; it has been the accepted value
  of the Yang-Lee universality class since Cardy, PRL 54, 1354 (1985). Nothing about the measurement could
  have produced a *different physical answer*; the only free outcomes were about the **estimator**.
- `Δ_T = 2` is **imposed, not measured**, in the QW driver: `qw_yanglee_ks.jl:128` sets
  `v_T = (E_T − E_vac)·L/(2π·2.0)`, and the T-state Δ-gate window `(1.75, 2.25)` at line 124 is centred on the
  exact CFT answer. The velocity cross-check `v` uses the exact `Δ_1 − Δ_φ = 2/5`
  (`qw_yanglee_ks.jl:86`). So two exact CFT inputs are injected before `c_KS` is formed.
- The record itself notes (`SIM-2026-071.json:23`) that at Yang-Lee the empirical discriminator inverts —
  the φ-descendant element is ~10× larger than T's — so **T is selected by the theory-fixed Δ-gate alone**
  (independently confirmed at `inv-pipelines.md §5.4 item 5`). The state identification is therefore an
  M(2,5) theory input, not a measurement.
- **Counterfactual novelty (§6): LOW-MODERATE.** Before the run, three outcomes were nominally live —
  `c_KS → −22/5`, `c_KS → +2/5`, or `c_KS → garbage`. That is a genuine fork, and I credit it. But
  **Io et al. had already resolved the general form of that fork six months earlier** (KS modes with
  biorthogonal pairing → the true negative `c`, not `c_eff`), and CJS had resolved the underlying
  true-vs-effective question in 2017. The residual uncertainty at the time of the run was implementation
  uncertainty, not physics uncertainty.

---

## 6. What actually survives — the honest residue

Stated with no inflation, the following are **not** found in the literature I searched and appear to be new:

1. **A finite-L numerical ladder of `c_KS` from biorthogonal Koo–Saleur matrix elements in an *interacting*
   non-Hermitian critical chain.** Io et al.'s lattice result is analytic (their model is quadratic);
   GJS 2020 use Bethe ansatz/QISM on an integrable chain. The QW route is brute-force sparse biorthogonal ED
   on a non-integrable-looking Hamiltonian, with no free-fermion or Bethe structure exploited.
   **Level 2** under §5 (a demonstration that a known technique works in a harder setting) — **not Level 3.**
2. **The `c` vs `c_eff` fork realised in a case where the two differ in sign *and* by ~11×.** At Io et al.'s
   `c = −2` the corresponding `c_eff = +1` (`c − 24h_min`, `h_min = −1/8`), so the fork exists but is
   quantitatively softer. Yang-Lee's `−22/5` vs `+2/5` is the sharpest available instance. This is a
   presentational advantage, not a new mechanism.
3. **The product-form estimator's exact invariance under eigenvector rescaling** (proved at
   `inv-pipelines.md §5.5`, claimed nowhere in the project's own records). This answers §13 Q3 and is a small,
   real, publishable methodological point — **if it is stated as a lemma and not as a discovery**, and if the
   literature check is extended to see whether GJS/Io already note it.
4. **The documented inversion of the unitary state-identification rule at Yang-Lee**
   (`SIM-2026-071.json:23`: the cross-module element to the φ-descendant is ~10× *larger* than T's).
   RESEARCH-DIRECTOR §13 already flags this as *"one of the most informative aspects of the work"*, and I
   agree — but note that it is a **negative** methodological finding: it says the KS element-dominance
   heuristic, which is the identification workhorse in Milsted–Vidal, **fails** off the unitary point. That is
   a caveat for the field, and it is the single most defensible thing in the record.

Everything else in the SIM-071 headline is a re-instantiation of published results.

---

## 7. Prior-art gate (§8, third gate) — the required statement

> **What does this project do that the nearest prior work does not?**

**Nearest prior work: Io, Huang & Hsieh, arXiv:2602.02649.**

QW measures the biorthogonal Koo–Saleur central charge (a) in an **interacting** rather than free-fermion
non-Hermitian chain, (b) at a **rational non-unitary minimal model** (M(2,5), `c = −22/5`) rather than a
`c = −2` logarithmic theory, (c) at a **finite distance inside the PT-unbroken phase** rather than at an
exceptional point, (d) from a **single off-diagonal matrix element** with a numerical finite-size ladder rather
than from the commutator central term evaluated analytically, and (e) with a **matched unitary control on the
same code path**.

**Nearest prior work on the conceptual claim: Couvreur, Jacobsen & Saleur, arXiv:1611.08506.**

QW uses a **stress-tensor** observable rather than an entanglement observable to make the same true-vs-effective
discrimination.

That is the whole of the difference. It supports **a methods note**, not a first-of-kind claim.

---

## 8. Defects in the project's own record (my findings, as an auditor)

| Sev | Defect | Evidence |
|---|---|---|
| **Critical** | `SIM-2026-071.json:22` makes a "first … to our knowledge" claim with **no literature gate performed and no prior-art field in the record**. RESEARCH-DIRECTOR §8 forbids exactly this phrase absent recorded evidence. | `grep -c "prior_art\|novelty\|literature" research/data/simulations/SIM-2026-071.json` → **0**. `HYP-2026-028.json` → 1 hit, and it is the word "literature" inside `confidence_rationale` ("Strong, specific literature anchor"), not a prior-art search. |
| **Critical** | `SIM-2026-071.json:22`'s premise — *"standard approaches obtain only c_eff from Casimir scaling"* — is **factually wrong** and would be caught by any referee in this subfield. | arXiv:1611.08506 abstract; 2107.13006 Figs. 1e–h and §2.2; 2502.02001 abstract. |
| **Major** | **Zero of the relevant non-unitary/biorthogonal literature is catalogued.** Searched the whole repo for 10 arXiv IDs: `9312156`, `1611.08506`, `2010.12819`, `2007.11539`, `2602.02649`, `2107.13006`, `1909.01346`, `2502.02001`, `1303.2082`, `2311.11251` → **all ten have no hits** outside gitignored vendor trees and this audit directory. Only Milsted–Vidal (1706.01436) and ZMV (1710.05397) are recorded. | `grep -rIl` over the repo, 2026-08-17. Also `research/data/papers/` grep for `Koo|Saleur|Jacobsen|Gainutdinov|Couvreur|logarithmic CFT|lattice Virasoro` → 2 files, neither a paper record. |
| **Major** | The **novelty gate was delegated to a forward-only newsfeed.** `research/digests/` starts at `2026-03-10-weekly-digest.md`; arXiv:2602.02649 v1 posted 2026-02-02. The weekly-scan architecture is structurally incapable of catching prior art older than the first scan — yet HYP-028's route notes (`scan12/14/15/18/19`) are the *only* literature process attached to this hypothesis. A backward prior-art search on "Koo–Saleur" / "biorthogonal" / "negative central charge" was never run. | `ls research/digests`; `HYP-2026-028.json:39-42,52`. |
| **Major** | **A known adverse result about the KS central term is unengaged.** GJS 2020 (§7.2, conj. 136) find the KS commutator's central term converges to `(1/12)(m³c − m c̃)` with `c̃ ≠ c`, and that the Shokrian-Zini–Wang modified phases do **not** fix it. SIM-071 attributes its entire 2.6 % residual to finite size (`SIM-2026-071.json:25`). This is an unexamined alternative explanation (§41 "Alternative explanations"). | arXiv:2010.12819 §7.2 and Fig. 7. |
| **Medium** | The design doc's chosen health metric is known-imperfect in the literature. `HYP028-BIORTHO-KS-DESIGN.md:85` uses `⟨Ψ_L|Ψ_R⟩ → 0` as the EP proximity monitor; Lu et al. (2311.11251, Fig. 5) show the same normalisation collapsing near an EP **and** decaying with L away from it — the same conflation flagged independently at `inv-pipelines.md §5.7`. | arXiv:2311.11251 §IV.B; `HYP028-BIORTHO-KS-DESIGN.md:85`. |
| **Medium** | `HYP-2026-028.json:54` claims *"G4 gate satisfied at ED scale"*, where G4 (line 24) mandates `c_eff = 2/5` **via biorthogonal entanglement-entropy scaling**. That mandated measurement is exactly what arXiv:1611.08506 / 2107.13006 / 2502.02001 make routine, and it was never performed — the substitute was `g_1`/`R_∞` boundary data. A cheap, literature-standard route to closing the actual gate exists and was not taken. | `HYP-2026-028.json:24,54`; corroborates `inv-pipelines.md §5.9`. |
| **Minor** | `SIM-2026-071.json:24` — *"C_TTT = 2√2/√c is IMAGINARY at c < 0"* — is presented as an implication of the measurement. It is an algebraic consequence of a formula the project applies (`qw_cttt_circle.py:203`), independent of any Yang-Lee number, and follows from `c = −22/5` being known since 1985. Framing it as a finding of SIM-071 overstates it. | `SIM-2026-071.json:24`; `research/tools/cttt-circle/qw_cttt_circle.py:203`. |

---

## 9. Recommended reframing (so the work is not lost)

If the residue in §6 is written up honestly, the defensible claim is roughly:

> "Koo–Saleur stress-tensor matrix elements, evaluated with a parity-induced biorthogonal pairing on a
> PT-symmetric Ising chain at the Yang-Lee point, return the true central charge `c = −22/5` rather than the
> effective charge `c_eff = 2/5`. This extends to an interacting rational non-unitary minimal model the
> biorthogonal-KS conformal-structure result established for free-fermion exceptional-point criticality by
> Io, Huang and Hsieh [arXiv:2602.02649], and is consistent with the true-versus-effective central-charge
> discrimination established for entanglement observables by Couvreur, Jacobsen and Saleur
> [PRL 119, 040601 (2017)]. We further report that the unitary state-identification heuristic of
> Milsted and Vidal [PRB 96, 245105 (2017)] **inverts** at this fixed point: the cross-module element to the
> φ-descendant exceeds T's by an order of magnitude, so element dominance alone selects the wrong state."

That is Level 2 methodological work with one genuinely useful negative finding. It is publishable in
SciPost Phys. Core / PRB as a short methods paper. It is not a first, and the word should not appear.

**Mandatory citations before any write-up** (none currently in the repo): hep-th/9312156; 1706.01436;
1710.05397; 1611.08506; 1909.01346; 2107.13006; 2010.12819; 2007.11539; 1303.2082; 2502.02001; **2602.02649**;
2311.11251; 2510.13581; 2607.25256.

---

## 10. UNVERIFIED

Stated explicitly, per the audit protocol. Silence is not a pass.

1. **I did not read arXiv:2606.16785 (PAPER-133) itself.** I read its abstract via the API and the project's
   summary of it in `HYP028-BIORTHO-KS-DESIGN.md`. I therefore **cannot rule out** that PAPER-133 or its
   supplemental material already contains a central-charge extraction (its abstract is about boundary
   `g`-factors and the negative excited-to-ground ratio, which suggests not). The design doc's reading of it
   was not independently checked.
2. **I did not verify whether Io et al. (2602.02649) ALSO produce a finite-size numerical `c` ladder** anywhere
   beyond the main text and SM §IV that I read. Their main text says the algebra *"converges to a Virasoro
   algebra with c = −2 in the scaling limit"* and their fitted finite-size quantities are `β_1, β_2`. If a
   numerical `c(N)` ladder exists in a part of the SM I did not reach, residue item §6.1 collapses too.
3. **INSPIRE-HEP and Crossref were not queried.** §8 names them. I used arXiv export API + Google Scholar
   (via `paper-search` MCP) only. A journal-database sweep (PRB / PRL / SciPost / J. Phys. A) could surface
   non-arXiv or arXiv-untagged work.
4. **Citation-trail search (references-of-references) was only partial.** I harvested the reference lists of
   2602.02649 and 2311.11251 in full, and 2107.13006's intro references. I did not systematically walk the
   forward citations of 1611.08506 (a highly cited PRL), which is where a Yang-Lee-specific KS paper would
   most likely sit if one exists.
5. **My model knowledge cutoff is 2026-05.** Everything with an arXiv ID of `2606.*` or later was verified
   live, but I cannot bring background familiarity to it. In particular I cannot assert that the June–August
   2026 window is clean beyond what queries 6, 9, 10, 13, 15, 18 returned.
6. **I did not check non-English or conference/thesis literature**, except that Google Scholar surfaced
   L. Liu's 2023 thesis *"Emerging Jordan forms, with applications to critical statistical models and
   conformal field theory"* (Saleur school), which I did not read and which is a plausible location for
   further biorthogonal-KS material.
7. **I did not verify the QW numbers themselves** (`c_KS = −4.29 ± 0.15`, the unitary control 0.49986).
   That is `inv:pipelines`' territory, and that artifact reports an independent Python reproduction of the raw
   per-L values plus a **critical** finding that the `h_c^∞` fit-model systematic moves the headline over
   `[−7.0, −3.7]` (`inv-pipelines.md §5.6`). If that band is right, C6's "specific number" residue is weaker
   than I have credited it above, and the only surviving claim is the **sign**.
8. **The relationship between the two `c` conventions in Io et al. and QW was not checked dimension-by-
   dimension.** Their `H_n^latt` carries the same `+ (c/12)δ_{n,0}` offset and `Na/2πv_F` prefactor as the QW
   driver, so I believe the objects are the same up to the half-bond phase convention, but I did not verify
   the normalisation of their `L_n` against `qw_yanglee_ks.jl:129`'s factor of 2.
