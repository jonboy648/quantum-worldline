# Novelty Gate — Yang-Lee / biorthogonal Koo-Saleur true negative central charge
## Literature adversary, NON-arXiv-API sources

**Agent role:** `adv:lit-yanglee-other` (RESEARCH-DIRECTOR.md §8 literature gate, §8 prior-art gate,
§6 counterfactual novelty, §5 contribution levels, §38.D novelty audit)
**Date:** 2026-08-17
**Constraint honoured:** the arXiv export API was NOT used (a sibling agent holds that endpoint
sequentially). All searches ran through WebSearch, Semantic Scholar API, INSPIRE-HEP API, ar5iv
HTML mirrors, publisher pages, and the local PDF of PAPER-133.

---

# 0. VERDICT (read this first)

| Sub-claim, as written in the record | Verdict |
|---|---|
| **A.** "First lattice extraction (to our knowledge) of a NEGATIVE central charge from stress-tensor matrix elements" — `research/data/simulations/SIM-2026-071.json:22` | **NOT NOVEL** |
| **B.** "the Koo-Saleur stress-tensor construction SURVIVES non-unitarity and measures the TRUE central charge ... NOT the effective (Casimir) charge" — `SIM-2026-071.json:21` | **NOT NOVEL** |
| **C.** "standard approaches obtain only c_eff from Casimir scaling" — `SIM-2026-071.json:22` | **FALSE**, not merely unnovel |
| **D.** "c = -22/5 CONSISTENT ... c_eff = +2/5 EXCLUDED" as a *discrimination* — `SIM-2026-071.json:18` | **NOT NOVEL** (the assignment c = -22/5 to this exact lattice model dates to 1991) |
| **E.** Narrow residual: *numerical* KS matrix-element measurement of c in an **interacting** (non-free-fermion) non-Hermitian chain at **M(2,5)** | **PARTIALLY NOVEL** (no prior instance found; increment is Level 1-2, not Level 3) |
| **F.** "The T-identification discipline INVERTS at YL: the cross-module product to the phi-descendant is ~10x LARGER than T's" — `SIM-2026-071.json:23` | **UNDETERMINED, leaning novel** — smallest and most defensible atom in the whole result |

**Bottom line.** The concept the project believes it originated — *a biorthogonal, left/right-eigenvector
Koo-Saleur construction on a non-Hermitian critical lattice chain whose Virasoro central term is the
TRUE negative central charge rather than c_eff* — was published as **arXiv:2602.02649** (Io, Huang &
Hsieh, RIKEN-iTHEMS) on **2 February 2026**, six months before SIM-071 was run on 2026-08-11.
That paper is **cited as reference [24] of PAPER-133** — the very manuscript the project read in full
on 2026-08-11 to design this phase. The pointer was in the project's hands and was not followed.

---

# 1. What exactly is being gated

The claim under test, quoted verbatim from the record:

> "First lattice extraction (to our knowledge) of a NEGATIVE central charge from stress-tensor matrix
> elements; standard approaches obtain only c_eff from Casimir scaling."
> — `research/data/simulations/SIM-2026-071.json:22` (`key_findings[1]`)

> "THE HYP-028 QUESTION IS ANSWERED at ED scale: the Koo-Saleur stress-tensor construction SURVIVES
> non-unitarity and measures the TRUE central charge c = -22/5, including its indefinite-metric sign
> -- NOT the effective (Casimir) charge c_eff = 2/5 ... The biorthogonal element structure sees what
> the energy spectrum cannot."
> — `SIM-2026-071.json:21` (`key_findings[0]`)

The estimator, quoted from the driver:

> `c_KS = 2 * <0_L|H_-2|T_R><T_L|H_+2|0_R> / (<T_L|T_R><0_L|0_R>) * (L/(2 pi v_T))^2`
> — `research/tools/yanglee-pt/qw_yanglee_ks.jl:8`

Status write-back: `research/data/hypotheses/HYP-2026-028.json:37` (`"status": "SUPPORTED"`) and
`:54` (`phase2_result`).

**Pre-existing audit context.** The phase-1 pipelines agent already flagged that this claim has no
gate behind it: *"I find no literature-gate record anywhere for [it] ... The novelty claim in SIM-071
should be struck until the gate is executed"* — `research/data/audit/raw/inv-pipelines.md:748-756`,
with the prior-art search explicitly deferred at `:788-789`. **This artifact executes that gate.**

**Independent confirmation that no gate was ever run.** A grep of the only design document for this
work returns *zero* matches for `novel|prior art|literature|to our knowledge|first`:

```
grep -niE "novel|prior art|literature|to our knowledge|first" \
     research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md
   → (no output)
```

And neither of the two most damaging prior-art papers exists anywhere in the repository:

```
grep -rl "2602.02649"                 → (no matches, whole repo)
grep -rli "couvreur|1611.08506"       → (no matches, whole repo)
```

Under §8 the phrase "to our knowledge" is prohibited "until the evidence for them has been recorded."
No evidence was recorded. The phrase is therefore a governance violation independent of whether the
underlying claim happens to be true — and, as shown below, it is not.

---

# 2. NEAREST PRIOR WORK (P1) — the one that decides the verdict

## Io, Huang & Hsieh, *Non-Hermitian free-fermion critical systems and logarithmic conformal field theory*
**arXiv:2602.02649** [cond-mat.str-el], v1 **2 February 2026**, v2 6 April 2026.
Authors: Iao-Fai Io, Fu-Hsiang Huang, Chang-Tse Hsieh. Report number RIKEN-iTHEMS-Report-26.
(No journal reference located as of 2026-08-17.)

### What it does (verbatim quotes, retrieved from the ar5iv/HTML full text)

- Framework: *"Working in the biorthogonal formalism"* (abstract). Ground states are built as explicit
  **left** and **right** eigenvectors — `⟨ρ_0^L| := ⟨0|∏_{m} η_L(p_m)` (Eq. S84) — and correlators are
  biorthogonal, `⟨GS_L|O|GS_R⟩` (Eq. S66).
- Construction: **the Koo-Saleur prescription, by name.**
  *"The central idea is to form appropriate Fourier modes of the local energy and momentum densities,
  which converge to (linear combinations of) Virasoro generators in the continuum."*
  *"the Koo-Saleur prescription defines the corresponding momentum density ... p_j := i[h_j, h_{j+1}]"*
  (Supplemental §IV, ~Eq. S68). They build improved lattice modes **H_n and P_n**.
- Result: *"we identify the conformal structure of this theory by constructing a traceless
  energy-momentum tensor whose Fourier modes generate a Virasoro algebra with central charge **c = -2**"*
  (Introduction); *"This construction yields a **negative central charge c = c̄ = -2**, reflecting the
  intrinsically non-Hermitian character"* (main text); *"in the scaling limit, the algebra converges to
  a Virasoro algebra with c = -2"* (~Eq. S78).
- It is the **true** c, not c_eff: no effective central charge is used anywhere; c = -2 is presented as
  the Virasoro central extension itself. (They do not even discuss c_eff.)
- Model: non-Hermitian SSH-type free-fermion chain at exceptional-point criticality,
  `h_j = -[t + (-1)^j δ](c†_{j+1}c_j + h.c.) - (-1)^j μ_s c†_j c_j` at `μ_s = 2iδ` (Eqs. S52-S53).
- Known systematic they document and the project does not: *"For the EP lattice model with the bare
  density h_j ..., a direct implementation of the Koo-Saleur construction does not reproduce the
  expected Virasoro algebra in the scaling limit"* — fixed by *"adding a lattice total-derivative
  (boundary) term."*

### EXACT OVERLAP with SIM-071

| Element | Io-Huang-Hsieh 2602.02649 | SIM-2026-071 |
|---|---|---|
| 1+1D non-Hermitian critical lattice chain | yes | yes |
| Biorthogonal left/right eigenvector pairing | yes (Eqs. S66, S84) | yes (`qw_yanglee_ks.jl:8`) |
| Koo-Saleur Fourier modes `H_n` of the lattice density | yes (named) | yes (`SIM-2026-071.json:6`) |
| Central term of the resulting Virasoro algebra | yes | yes |
| Value obtained is the TRUE **negative** c, not c_eff | yes (c = -2) | yes (c = -4.29) |
| Claim that the KS/stress-tensor route survives non-unitarity | yes | yes |

**Six of six.** Claims A and B are contained in this paper.

### EXACT DIFFERENCE (what SIM-071 has that P1 does not)

1. **Interacting vs free.** P1's chain is quadratic (free fermions, exactly solvable, c = -2 symplectic-
   fermion / logarithmic CFT). SIM-071's chain is the interacting PT-symmetric Ising chain at the
   Yang-Lee point → M(2,5), c = -22/5. Different universality class, different solvability class.
2. **Numerical measurement vs analytic closure.** P1 fixes c analytically: *"Requiring the standard
   Virasoro central extension then fixes c = -2"* (Eq. S37); the lattice check is carried by the
   **indecomposability parameters** β_M (`β_1^latt = -1 + (17/48)(2π/N)² + O(N⁻⁴)`), not by a
   finite-size fit of c itself. SIM-071 instead *measures* c from a matrix-element product at
   L = 10…18 and extrapolates to `-4.29 ± 0.15` (`SIM-2026-071.json:15`).
3. **Regime.** P1's criticality sits **at** an exceptional point (defective/Jordan). SIM-071 sits in
   the PT-unbroken interior with a diagonalizable, real spectrum.
4. **Explicit c-vs-c_eff discrimination test.** P1 never mentions c_eff. SIM-071 states an explicit
   two-outcome discrimination (`SIM-2026-071.json:18`). (This is a presentational difference, not a
   physics one — see §6 on why the discrimination was fixed in advance.)
5. **A systematic P1 documents that SIM-071 does not address.** P1 reports that the *bare* KS density
   fails at a non-Hermitian critical point and requires a lattice total-derivative improvement.
   Nothing in `qw_yanglee_ks.jl` or `SIM-2026-071.json` mentions such a term. This is simultaneously a
   prior-art hit **and** a live candidate explanation for SIM-071's unexplained 2.6% residual.

**Net:** difference #1 and #2 are real. They downgrade the claim from "first to do X" to "first to do
X in an interacting model, numerically." That is a Level-1/Level-2 increment under §5, not Level 3.

---

# 3. THE OTHER PRIOR-ART BLOCKS

## P2 — the estimator itself is published, and unitary-only was never the barrier

**Zou, Milsted & Vidal**, *Emergence of conformal symmetry in critical quantum spin chains: applying
the Koo-Saleur formula to nonintegrable models*, **arXiv:1706.01436**, Phys. Rev. B (INSPIRE recid
1602627, 66 citations). Retrieved verbatim from the ar5iv full text:

> `H_n ≡ (N/2π) Σ_j e^{+ijn2π/N} h_j`, with `H_n^CFT = L_n^CFT + L̄_{-n}^CFT - (c/12)δ_{n,0}`
> `√(c/2)|T⟩ = H_{-2}^CFT|I⟩` and `√(c/2)|T̄⟩ = H_2^CFT|I⟩`
> **`c ≈ 2|⟨T|H_2|I⟩|²`**

That last line is SIM-071's estimator. `qw_yanglee_ks.jl:8` is the same expression with `|·|²`
replaced by the bilinear product `⟨0_L|H_{-2}|T_R⟩⟨T_L|H_{+2}|0_R⟩ / (⟨T_L|T_R⟩⟨0_L|0_R⟩)` — i.e. the
Hermitian square swapped for the biorthogonal pairing. Models treated there: TFIM (c=1/2), 3-state
Potts (c=4/5), self-dual ANNNI — **all unitary**.

**Consequence for the derivation gate (§8).** The step from `2|⟨T|H_2|I⟩|²` to the bilinear product is
the *only* algebraic novelty, and it is the textbook substitution that defines every biorthogonal
observable. Once P1 had established that the KS construction closes on a Virasoro algebra in the
biorthogonal formalism, the sign-carrying product form follows immediately. The number is not new
machinery.

## P3 — a lattice extraction of a TRUE NEGATIVE central charge, from left/right eigenstates, in 2017

**Couvreur, Jacobsen & Saleur**, *Entanglement in nonunitary quantum critical spin chains*,
**Phys. Rev. Lett. 119, 040601 (2017)**, arXiv:1611.08506. Retrieved verbatim from ar5iv:

- Motivating models, named explicitly: *"the Ising chain in an imaginary magnetic field (whose
  critical point is described by the **Yang-Lee singularity**), the alternating sl(2|1) chain
  describing percolation hulls, or the alternating gl(2|2) chain describing the IQHE plateau
  transition."* — the project's own model family.
- Biorthogonal object: for non-Hermitian H with `|0_L⟩ ≠ |0_R⟩`, they build `ρ̃ ≡ |0_R⟩⟨0_L|`, with a
  modified trace `ρ̃_A = Tr_B(q^{-2δ_B^z} ρ̃)` and `S̃_A = -Tr(q^{2δ_A^z} ρ̃_A ln ρ̃_A)`.
- Numerics (their Fig. 2), model (p,m) = (2,4), n = 2cos(2π/5), **M = 400 sites**, OBC:
  - unmodified trace → `c_XXZ = 1`
  - modified trace, `n₁ = 2cos(π/5)` → **c_eff = 3/5**
  - modified trace, `n₁ = n` → **true c = -3/5 (negative)**
- They state the point of the paper is exactly the discrimination: *"This allows us to distinguish
  the role of the central charge and effective central charge in rational minimal models of CFT."*
- They quote the project's own headline pair: *"For instance, for the Yang-Lee singularity, c = -22/5
  but c_eff = 2/5."*

**This alone refutes claim A** in its plain reading ("first lattice extraction of a negative central
charge"): a negative *true* central charge was measured on a lattice, from left+right eigenstates, in
a non-Hermitian setting, with an explicit c-vs-c_eff separation, nine years earlier, in PRL.
Claim A survives only under the narrow qualifier "from stress-tensor matrix elements", which P1 then
takes.

## P4 — c = -22/5 was assigned to *this exact lattice model* in 1991

**G. von Gehlen**, *Critical and off-critical conformal analysis of the Ising quantum chain in an
imaginary field*, **J. Phys. A 24, 5371-5400 (1991)**. This is the founding lattice paper for the
imaginary-field Ising chain, and it is **cited as ref. [50] of PAPER-133** — present in the project's
own downloaded PDF (`research/downloads/2606.16785v2.pdf`, bibliography entry [50]).

Secondary sources consistently report that von Gehlen identified the transition as *"of the Yang-Lee
universality class with central charge c = -22/5"*, obtained by finite-size analysis of the chain.
(Direct verification of the abstract was blocked — see UNVERIFIED §9.1.)

**Consequence for claim D.** The proposition "this lattice model realizes the CFT with c = -22/5, and
c_eff = 2/5 is the *Casimir* shadow of it" has been settled lattice knowledge for 35 years. SIM-071
did not discriminate an open question; it re-derived a settled assignment through a new estimator.
That is Level 1 (reproduction/validation) presented as if it were Level 3.

## P5 — Casimir scaling in a biorthogonal setting already yields the non-c_eff central charge

**Tang, Ma, Tang, He & Zhu**, *Reclaiming the lost conformality in a non-Hermitian quantum 5-state
Potts model*, **Phys. Rev. Lett. 133, 076504 (2024)**, arXiv:2403.00852. From the v2 HTML:

- They numerically extract **c ≈ 1.1405 − 0.0224i** (complex, hence certainly not a c_eff) together
  with `v ≈ 2.8810 − 0.7091i`.
- Method: **ground-state energy-density scaling** — `E₀/L = E_m − πcv/(6L²) + …` (App. D, Eq. S24).
  I.e. **Casimir scaling.**
- Framework: *"left and right eigenstates satisfying biorthogonal relations"*, plus radial
  quantization / state-operator correspondence.

**This directly falsifies claim C.** "Standard approaches obtain only c_eff from Casimir scaling" is
not true: once the biorthogonal pairing and the correct vacuum are used, Casimir scaling returns the
genuine (here complex) central charge. It is also false for a more elementary reason: `c_eff = c − 24 h_min`
is an identity, and `h_min = -1/5` at Yang-Lee has been known since Cardy (1985), so `c` is recoverable
from `c_eff` by arithmetic. The energy spectrum is not blind to c, contrary to
`SIM-2026-071.json:21` ("The biorthogonal element structure sees what the energy spectrum cannot").

## P6 — negative central charges from non-Hermitian lattices, 2022

**Tu, Tzeng & Chang**, *Rényi entropies and negative central charges in non-Hermitian quantum
systems*, **SciPost Phys. 12, 194 (2022)**, arXiv:2107.13006. Abstract: they propose generic
entanglement/Rényi entropies for non-Hermitian systems and report *"excellent agreement between the
numerical extrapolation of the negative central charges ... and the non-unitary CFT prediction"*,
on XXZ and six-vertex lattice models.

## P7 — negative c from finite-size energy scaling in a PT-symmetric chain, 2024

**Zhou & Wang**, *Universal non-Hermitian flow in one-dimensional PT-symmetric quantum criticalities*,
arXiv:2405.01640 (SciPost submission scipost_202405_00008). Abstract, verbatim: *"under open boundary
condition (OBC), the energy scaling E(L) ∼ c/L reveals a **negative central charge c = -2** at the
non-Hermitian critical point, indicative of a non-unitary CFT."* Another Casimir-route negative c,
reinforcing the falsification of claim C.

## P8 — the original Koo-Saleur paper already "observed the central term" on the lattice

**W. M. Koo & H. Saleur**, *Representations of the Virasoro algebra from lattice models*,
**Nucl. Phys. B 426, 459-504 (1994)**, hep-th/9312156. Abstract, verbatim: *"Most features of the
Virasoro algebra (like **central term**, null vectors, metric properties...) can thus be observed
using the lattice models."* Models: XXZ and RSOS. Note their own honest phrasing — *"Our approach is
straightforward but **to our knowledge** had never been tried so far"* — which is the standard the
project's record borrowed the wording of without borrowing the search.

## P9 — the Saleur school has run Koo-Saleur generators inside non-unitary / logarithmic models

- **Grans-Samuelsson, Liu, He, Jacobsen & Saleur**, *The action of the Virasoro algebra in the
  two-dimensional Potts and loop models at generic Q*, **JHEP 10 (2020) 109**, arXiv:2007.11539.
  Uses *"a careful study of 'Koo-Saleur generators'"* numerically; central charge `c = 1 − 6/(x(x+1))`
  (their Eq. 5), which is **negative** over part of the generic-Q range; establishes that *"the
  Potts-model CFT is logarithmic for Q generic"*; defines two scalar products with distinct adjoints
  (`L_n†` vs `L_n‡ = L_{-n}`) — i.e. a non-Hermitian bilinear/"conjugate-state" pairing.
- **Grans-Samuelsson, Jacobsen & Saleur**, *The action of the Virasoro algebra in quantum spin chains.
  I. The non-rational case*, **JHEP 02 (2021) 130**, arXiv:2010.12819. Koo-Saleur generators in the
  critical XXZ chain; Verma / co-Verma dual structures from *"pairs of 'conjugate states'"*; form
  factors for *"relevant combinations of three neighbouring spin operators."*

Neither paper reports a numerical fit of `c` from a `⟨T|H_2|I⟩` matrix element (I checked for exactly
that formula and did not find it — see UNVERIFIED §9.2). Their significance here is that **KS
generators inside non-unitary, logarithmic, non-Hermitian-paired lattice models is an established
programme**, not virgin territory, and that the project's framing of the non-unitary KS extension as
unexplored is not supportable.

## P10 — Yang-Lee conformal data from a microscopic non-Hermitian model, 2025

**Fan, Dong & Vishwanath**, *Simulating the non-unitary Yang-Lee conformal field theory on the fuzzy
sphere*, arXiv:2505.06342 (9 May 2025). Ising quantum-Hall ferromagnet with transverse field and
**imaginary longitudinal field**; state-operator correspondence; reports *"one previously unknown
primary operator and several operator product expansion coefficients"*, benchmarked against the
(1+1)D Yang-Lee problem. Related: **Arguello Cruz, Klebanov, Tarnopolsky & Xin**, *Yang-Lee quantum
criticality in various dimensions*, arXiv:2505.06369.
These are the current frontier for "new Yang-Lee conformal data." They set the bar SIM-071 would have
to clear to be Level 3: a *previously uncomputed* quantity. `c = -22/5` is not one.

## P11 — the c-vs-c_eff framing itself

**Bianchini, Castro-Alvaredo, Doyon, Levi & Ravanini**, *Entanglement entropy of non-unitary conformal
field theory*, **J. Phys. A 48, 04FT01 (2015)**, arXiv:1405.2804. `c_eff = c − 24Δ > 0`. This is the
standard reference for the statement that entanglement sees `c_eff`; it is the *motivation* for P3 and
P6, both of which then went and got the true `c` anyway.

---

# 4. FORWARD-CITATION TRACE FROM ZOU-MILSTED-VIDAL (as tasked)

INSPIRE-HEP recid **1630913** = Zou, Milsted & Vidal, *Conformal data and renormalization group flow
in critical quantum spin chains using periodic uniform matrix product states*, **PRL 121, 230402
(2018)**, arXiv:1710.05397. Citation count 70 (INSPIRE) / 52 (Semantic Scholar). I enumerated all 68
citing records returned by `refersto recid 1630913`. Filtering for non-unitarity / non-Hermiticity:

| Citing work | arXiv | Non-unitary? | Extracts c? | KS matrix elements? |
|---|---|---|---|---|
| Universal non-Hermitian flow in 1D PT-symmetric quantum criticalities (Zhou-Wang) | 2405.01640 | yes | yes, c = -2 | no (Casimir) |
| Reclaiming the lost conformality in a non-Hermitian 5-state Potts model (Tang et al., PRL 133, 076504) | 2403.00852 | yes | yes, c = 1.14 − 0.022i | no (Casimir, biorthogonal) |
| Emerging Jordan forms ... critical statistical models and CFT (L. Liu) | 2403.09881 | yes ("relaxes hermiticity postulate") | not established | not established |
| Virasoro action in 2D Potts and loop models at generic Q (Grans-Samuelsson et al., JHEP) | 2007.11539 | yes (logarithmic) | no fit reported | KS generators used, c not fitted |
| Virasoro action in quantum spin chains I: non-rational case (JHEP) | 2010.12819 | partially | no | KS generators used |
| Yang-Lee quantum criticality in various dimensions (Klebanov et al.) | 2505.06369 | yes | not established | no |
| Approximate conformality before it's lost: Q>4 Potts (Ma-He) | 1811.11189 | complex CFT | — | no |
| Topological defects in periodic RSOS models and anyonic chains | 2003.11293 | RSOS | — | — |
| Virasoro generators in the Fibonacci model tensor network (Zeng et al.) | 2212.02937 | **no** (Fibonacci is unitary, c = 7/10) | — | Virasoro operators in TN |
| Virasoro and Kac-Moody in generic TN representations (Zeng et al.) | 2205.04500 | no | — | yes, unitary |

**Result of the forward trace: nobody in the puMPS/Koo-Saleur citation tree extended the KS
matrix-element estimator to a non-unitary model.** That is the one honest gap SIM-071 sits in — and it
is filled from *outside* the tree, by P1 (Io-Huang-Hsieh), which is a cond-mat paper not indexed in
INSPIRE and therefore invisible to a citation-trail search anchored on Zou-Milsted-Vidal. This is a
methodological lesson for the project's scanning: **a citation-trail-only search would have missed the
single nearest prior work.**

---

# 5. PAPER-133 REFERENCE-LIST AUDIT (as tasked)

Source: `research/downloads/2606.16785v2.pdf`, full text extracted locally to `_p133.txt`.

First, a correction to the project's mental model of this paper: **PAPER-133 does not use Koo-Saleur,
does not construct Virasoro generators, and does not measure any central charge.** Grepping its full
text: `Koo` → 0 hits; `Virasoro` → 0 hits; `c_eff`/`effective central` → 0 hits; `central charge` → 1
hit, in the Supplemental benchmark table (*"The Yang-Lee CFT is the nonunitary minimal model M(2,5),
with central charge c = -22/5 and two primaries 1 and φ"*). It measures **boundary g-functions**.
That is consistent with its use as the SIM-070 Phase-1 gate, but it is *not* prior art for the c
extraction, and it should not be cited as such.

The requested citation neighbourhood, resolved:

| Ref | Identity | Relevance to this gate |
|---|---|---|
| [16] | Chang, You, Wen & Ryu, *Entanglement spectrum and entropy in topological non-Hermitian systems and nonunitary CFT*, PRResearch 2, 033069 (2020), arXiv:1909.01346 | non-Hermitian lattice + non-unitary CFT entanglement |
| [17] | Shimizu & Kawabata, *Complex entanglement entropy for complex conformal field theory*, PRB 112, 085112 (2025), arXiv:2502.02001 | complex (non-c_eff) universal data from non-Hermitian chains |
| [18] | Vander Linden, De Vos, Vervoort, Verstraete & Ueda, PRB 113, 205106 (2026), arXiv:2507.14732 | non-Hermitian 5-state Potts, universal entanglement spectrum |
| **[24]** | **Io, Huang & Hsieh, arXiv:2602.02649** | **THE NEAREST PRIOR WORK — see §2** |
| [25-30] | Kaplan-Lee-Son-Stephanov; Gorbenko-Rychkov-Zan I & II; Ma-He; Haldar et al.; Jacobsen-Wiese PRL 133, 077101 (2024) | complex-CFT lattice realizations |
| [31] | Tang, Ma, Tang, He & Zhu, PRL 133, 076504 (2024) | **P5 — complex c from biorthogonal Casimir scaling** |
| [32] | Tang, Liu, Tang & Zhu, SciPost Phys. 19, 164 (2025), arXiv:2512.07625 | boundary criticality of complex CFT, non-Hermitian |
| [38] | Fisher, PRL 40, 1610 (1978) | Yang-Lee = iφ³ |
| [39] | Cardy, PRL 54, 1354 (1985) | **Yang-Lee = M(2,5), c = -22/5, h_φ = -1/5** — the origin of the number SIM-071 "measured" |
| [43-48] | technical notes + Ishibashi (1989); Bender-Boettcher (1998); Mostafazadeh (2002); Brockmann-Stéphan | PT / pseudo-Hermiticity toolkit |
| [50] | **von Gehlen, J. Phys. A 24, 5371 (1991)** | **P4 — c = -22/5 on this lattice model, 1991** |

**The task's hypothesis was correct: the result was already in the neighbourhood, and specifically in
reference [24].** The project had `2606.16785v2.pdf` on disk and logged a "FULL v2 READ DONE"
(`HYP-2026-028.json:53`) on the same day the design was written. Reference [24] was not followed.

---

# 6. DERIVATION GATE AND COUNTERFACTUAL NOVELTY (§8, §6)

## 6.1 Was the outcome fixed in advance?

**Yes, essentially.** Three independent reasons:

1. **The central term of a Virasoro algebra IS c, by definition.** `c_eff` is not a central extension
   of anything; it is the combination `c − 24 h_min` that governs the *Casimir* energy relative to the
   *lowest* state. The Koo-Saleur `H_n` operators are constructed to converge to `L_n + L̄_{-n}`. A
   correctly implemented KS estimator evaluated on the *identity* module could not have returned
   `+2/5`. The "competing outcome" was never live physics — it was the implementation-failure branch.
   Under §6 this is **near-zero counterfactual novelty**: "only implementation failure or success was
   possible."

2. **The answer was on the lattice since 1991.** P4 assigns c = -22/5 to this exact chain. The
   project's own inputs already encode it: `SIM-2026-071.json:17` uses *"v_ref from the exact
   Delta = 2/5 (1−phi) split"*, and the vacuum is selected as *"|1>, THE SECOND k=0 STATE (physical GS
   is |phi>, Delta_phi = -2/5)"* (`SIM-2026-071.json:6`) — both M(2,5) CFT inputs.

3. **The velocity is calibrated by imposing the answer's kinematics.** `qw_yanglee_ks.jl:128`:
   ```julia
   v_T = (ET-ens[ivac])*L/(2pi*2.0)
   ```
   i.e. `v_T` is *defined* by asserting `Δ_T = 2.0`, then fed into `c_KS = 2*prods[jT]*(L/(2pi*v_T))^2`
   (line 129). Algebraically this collapses to `c_KS = 8·(product)/(E_T − E_vac)²`. So the estimator
   consumes the assumption `Δ_T = 2` — the same stress-tensor kinematics whose survival off the
   unitary point HYP-028 was created to test (`HYP-2026-028.json:5`). Under §7 this is a
   **structurally dependent** comparison, not an independent one.

## 6.2 What *was* genuinely uncertain beforehand

Honestly stated, and worth stating: whether the KS construction *converges at all* at a non-Hermitian
fixed point, whether the biorthogonal pairing keeps the element real, and whether state identification
survives. Those are real risks — P1 documents that the **bare** KS density *fails* at a non-Hermitian
critical point and needs a total-derivative improvement. So the run was not vacuous. But "the
implementation worked" is **Level 1 / Level 2** under §5, and the record files it as an answered
frontier question (`HYP-2026-028.json:37` = `SUPPORTED`).

## 6.3 Contribution level (§5)

| Component | Level | Reason |
|---|---|---|
| c_KS = -4.29 vs -22/5 at Yang-Lee | **1** (reproduction/validation) | value fixed by Cardy 1985, on the lattice since von Gehlen 1991 |
| Unitary control 0.49986 vs 0.5 | **1** | validation of an estimator published in 2017 (P2) |
| "c_eff excluded" discrimination | **1** | fixed by the definition of a Virasoro central extension |
| Biorthogonal product-form KS estimator | **2**, contested | the construction is P1 (Feb 2026); the increment is interacting-model + numerical fit |
| Cross-module element ~10× larger than T's; Δ-gating mandatory | **2**, plausibly the only defensible atom | no prior statement found |
| "C_TTT imaginary at c<0" (`SIM-2026-071.json:24`) | **not a result** | `C_TTT = 2√2/√c` with c<0 is arithmetic, not measurement |

---

# 7. WHAT SHOULD BE STRUCK, AND WHAT COULD SURVIVE

## 7.1 Required corrections to the record

1. `research/data/simulations/SIM-2026-071.json:22` — **strike** `key_findings[1]` in its entirety.
   Both clauses fail: "first ... negative central charge from stress-tensor matrix elements" is taken
   by arXiv:2602.02649; "standard approaches obtain only c_eff from Casimir scaling" is falsified by
   PRL 133, 076504 (2024) and arXiv:2405.01640. Replace with a cited positioning sentence.
2. `SIM-2026-071.json:21` — the sentence *"The biorthogonal element structure sees what the energy
   spectrum cannot"* is false and should go. The energy spectrum in a biorthogonal framework sees the
   true c (P5, P7), and `c = c_eff + 24 h_min` makes it recoverable arithmetically.
3. `research/data/hypotheses/HYP-2026-028.json:37` — `"status": "SUPPORTED"` needs re-derivation
   against the pre-registered criteria now that the literature gate has run; at minimum the
   confidence rationale must record that the measured value was known lattice data since 1991.
4. **Add an ERRATA entry.** The phase-1 errata agent found ERRATA.md frozen at 2026-06-08
   (`research/data/audit/raw/inv-errata-history.md`). A struck novelty claim is exactly what that
   register exists for.
5. **Catalogue the missing papers.** arXiv:2602.02649, arXiv:1611.08506, arXiv:2107.13006,
   arXiv:2403.00852, arXiv:2405.01640, hep-th/9312156, arXiv:1706.01436, von Gehlen 1991 — none of
   which are in `research/data/papers/`. The ID high-water is PAPER-138; these are eight records.

## 7.2 What could still be written up honestly

A **methods note**, framed as an extension of arXiv:2602.02649 from free to interacting non-Hermitian
chains, whose contributions are:

- the first *numerical, error-barred* KS matrix-element determination of a true negative c in an
  **interacting** non-Hermitian chain (M(2,5)), with the unitary control on the same code path;
- the **state-identification failure mode**: at Yang-Lee the cross-module product to the φ-descendant
  exceeds T's by ~10×, inverting the unitary heuristic and making Δ-gating mandatory
  (`SIM-2026-071.json:23`). This is a genuine trap for anyone applying P2's estimator off the unitary
  point, and I found no prior statement of it;
- the negative biorthogonal norm `⟨1|1⟩ < 0` observed raw at every L (`SIM-2026-071.json:17`) as an
  operational indefinite-metric diagnostic.

Under §25 this belongs in Candidate Paper A. It must cite P1, P2, P3, P4, P5 in the introduction, and
it must **not** claim priority for the biorthogonal-KS-measures-true-c idea.

**Two things must be resolved before that note is credible:**
(a) whether the KS density needs P1's lattice total-derivative improvement at this fixed point — an
untested systematic that could account for the 2.6% residual;
(b) the `v_T` circularity at `qw_yanglee_ks.jl:128` (Δ_T = 2 imposed, then c inferred). An independent
velocity determination is needed, or the result must be stated as a *conditional* measurement.

---

# 8. INDEPENDENCE LEDGER FOR THIS CLAIM (§7)

| Side A: SIM-071 c_KS | Side B: c = -22/5 target |
|---|---|
| raw data: biorthogonal ED eigenvectors, L = 10…18, PT-symmetric YL chain | raw data: none — exact M(2,5) value |
| shared theoretical assumption | Yang-Lee lattice point ⇒ M(2,5); source: Cardy PRL 54, 1354 (1985), von Gehlen 1991 |
| shared fitted parameter | `h_c^inf = 1.5587127`, itself taken from SIM-070, itself gated on PAPER-133 |
| shared exact CFT identity | `Δ_T = 2` (imposed at `qw_yanglee_ks.jl:128`); `Δ_φ = -2/5` (vacuum selection, `SIM-2026-071.json:6`); `Δ = 2/5` split (`v_ref`, `:17`) |
| shared numerical code | unitary control shares 148/152 lines with the result (`inv-pipelines.md` headline) |
| genuinely independent information | the *magnitudes* of the KS matrix elements themselves |

**Classification: structurally dependent, verging on a consistency check.** The comparison confirms
that a KS estimator fed M(2,5) kinematics returns an M(2,5) central charge. That is a valid pipeline
validation. It is not an independent measurement of c.

---

# 9. UNVERIFIED

Explicitly listed per instruction; silence would not be a pass.

**9.1 von Gehlen 1991 primary text.** IOPscience (doi 10.1088/0305-4470/24/22/021) returned an error
page; I could not read the abstract or the paper. The attribution "c = -22/5 for the imaginary-field
Ising chain" rests on (a) secondary statements retrieved in search, (b) its citation as ref. [50] of
PAPER-133 in exactly that context, and (c) its citation in arXiv:2403.00852 and arXiv:2510.19085 in
that context. **If the paper turns out to have reported only c_eff and inferred c, claim D softens
from NOT NOVEL to PARTIALLY NOVEL — but claims A, B and C are unaffected**, since they fall to P1,
P3 and P5 independently.

**9.2 Whether the Saleur-school loop/Potts papers (P9) fit c numerically from KS matrix elements.**
I searched arXiv:2007.11539 for an explicit `⟨T|H_{-2}|0⟩ ↔ √(c/2)` comparison and the fetch reported
none, but their Appendix A numerics were not fully retrieved. If such a fit exists in that appendix
(a non-unitary logarithmic model with c<0 at generic Q), **claim A and the §7.2 residual would both
collapse further**, back to 2020. This is the single highest-value follow-up check.

**9.3 arXiv:2602.02649 version dates.** Two fetches of the same page reported "v1 2 Feb 2026 / v2
6 Apr 2026" and "v2 posted April 6, 2026 (submitted August 11, 2026)". The latter is almost certainly
a mis-parse of the retrieval date. **Priority over SIM-071 (2026-08-11) depends on the v1 date** —
if v1 is genuinely February 2026 the paper precedes SIM-071 by six months. Its appearance as ref. [24]
in PAPER-133's v1 (June 2026) independently establishes it existed before June 2026, which is
sufficient for priority. Confirm the v1 date via the arXiv listing when the endpoint is free.

**9.4 Whether P1 numerically extracts c or only asserts it.** The fetch reported no finite-size
convergence figure for c, and stated the value is fixed analytically from the Virasoro central
extension with lattice verification carried by the indecomposability parameters β_M. I did not obtain
the full supplemental text. **If P1 does contain a numerical c fit, the §7.2 residual disappears
entirely.**

**9.5 arXiv:2604.25999** (*Lattice Topological Defects in Non-Unitary Conformal Field Theories*, 2026)
and **arXiv:2606.19732** (*Quantum models with the Yang-Lee phase transition*, 2026) surfaced in
search but were not opened. Both are in-neighbourhood and could contain further prior art.

**9.6 Semantic Scholar forward citations** returned HTTP 429 and could not be cross-checked against
INSPIRE. The INSPIRE trail (68 records) is INSPIRE-indexed only; pure cond-mat citing papers — the
category P1 belongs to — are systematically under-represented. **The true forward-citation set is
larger than the 68 I enumerated.**

**9.7 Google Scholar** was not reachable as a structured source; its coverage of non-INSPIRE cond-mat
is the main blind spot in this gate.

---

# 10. SEARCH RECORD (for reproducibility, §21)

Sources queried: WebSearch (9 distinct queries), INSPIRE-HEP REST API (`/api/literature`, `refersto
recid 1630913`, keyword search), Semantic Scholar Graph API (`/graph/v1/paper/arXiv:*`),
ar5iv HTML mirrors (1611.08506, 1706.01436, 2007.11539, 2602.02649), arXiv abstract pages
(2010.12819, 2107.13006, 2212.02937, 2402.10732, 2403.00852, 2403.09881, 2405.01640, 2505.06342,
2505.06369, 2510.13581, hep-th/9312156), arXiv HTML (2403.00852v2, 2510.19085, 2602.02649),
IOPscience (blocked), HAL (blocked by Anubis), and the local PDF `research/downloads/2606.16785v2.pdf`
(19 pp., extracted to `_p133.txt`, 65,934 chars).

Terminology variants covered per §8: negative central charge, effective central charge, non-unitary
CFT, biorthogonal CFT, Koo-Saleur generators, lattice Virasoro generators, stress-tensor matrix
elements, Yang-Lee chains, non-Hermitian spin chains, PT-symmetric criticality, transfer matrices,
finite-size scaling, entanglement methods, logarithmic CFT, complex CFT, indecomposability parameters,
Jordan cells, exceptional-point criticality, fuzzy sphere.

**arXiv export API: NOT USED** (constraint honoured).
