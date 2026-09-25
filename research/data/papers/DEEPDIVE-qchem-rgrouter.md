# DEEPDIVE — RG-Flow-of-Entanglement Universality-Class Method-Router for Quantum Chemistry

Candidate: QCHEM-COMBO-B Rank 1 ("RG-flow criticality fingerprint"). Repurpose the
project's chi=3 MERA causal-cone / disentangler machinery as a per-molecule
universality-class classifier (gapped vs c=1/2 vs c=1 critical) to route the
quantum-chemistry method (CCSD vs DMRG vs CASPT2/large-chi).

Anti-pattern under test: HYP-014 — "a power-law / curve match is not evidence of a
mechanism." The deep-dive question is whether the molecule→1D-CFT→MERA-causal-cone
chain is a STRUCTURAL identity or a second curve-coincidence.

VERDICT: **REFUTED as written** (Mech 2/5, not the claimed 4/5). A de-scoped
model-chain residue is NEEDS-MODIFICATION but competes poorly against existing
free diagnostics. Recommend SHELVE.

---

## 0. Executive summary

The candidate proposes routing quantum-chemistry method choice by running the
project's chi=3 MERA RG-flow on a molecule and reading off a universality class.
Three findings sink the Rank-1 / Mech-4 framing:

1. **Wrong fixed point.** The project's MERA is validated on the c=1/2 transverse
   Ising CFT. The molecular target (half-filled polyacene/PPP pi-chain) flows to a
   **c=1 Luttinger liquid** or to a **gapped Peierls/bond-order-wave** phase — a
   different central charge and operator content, or no CFT at all. The candidate's
   Mech-4 argument asserts the MERA causal cone "IS the RG of exactly that class"
   while silently swapping the validated class (Ising) for the chemical one. That
   class-boundary swap is the HYP-014 curve/mechanism conflation, in a new costume.

2. **The "validated extractor" is not validated.** The project validated a
   force-exponent (alpha≈4) and a transport coefficient (T=(pi/2)l_AdS). It never
   validated a central-charge / RG-flow classifier — the c=1/2 test is stated only
   *conditionally* in the design doc; the code emits raw S(l) and never fits
   (c/3)log L. The candidate names a validated asset that does not exist.

3. **Not free, and out-competed.** It needs a substantial new build (fermionic
   MERA or a re-validated mapping), contradicting the "reuses existing code, no
   new build" pitch. And the actionable routing bit (big-chi vs not) is recoverable
   more cheaply and more faithfully from truncation-error / bond-dimension scaling
   of a pilot DMRG sweep — which the chemistry community already reads off for free.

Mechanism-faithfulness: **2/5**, exponent-coincidental risk, would be rubric-FLAGGED.
A narrow de-scoped *model-chain* version is salvageable (NEEDS-MODIFICATION) but is
not the per-molecule ab-initio router the candidate sells and still must beat the
free truncation-error baseline to justify itself.

## 1. Mechanism faithfulness — the crux

### 1.1 The claimed structural chain

The candidate's Mech=4 rests on a four-link chain, asserted in §(4) of QCHEM-COMBO-B:

```
(L1) long polyacene/GNR pi-system
   --> (L2) quasi-1D half-filled correlated chain (Hubbard/PPP)
   --> (L3) 1D critical effective field theory (a CFT)
   --> (L4) whose real-space RG fixed-point structure IS the MERA causal cone
```

If every link is an *identity in the appropriate limit*, the diagnostic is
mechanism-faithful: the MERA causal cone is then literally the RG of the molecule's
low-energy theory, and the extracted scaling data is the molecule's actual
universality class, not a fitted curve. If any link is an *analogy* or holds only
under fine-tuning, then "we measured S(L) ~ (c/3)log L therefore route to MERA" is
the HYP-014 shape: a curve that matches without the generating mechanism being the
one assumed. Each link is audited below.

### 1.2 Step-by-step audit of the mapping

**L1 → L2 (pi-manifold → quasi-1D half-filled chain): PARTIALLY FAITHFUL.**
The acene/poly-acetylene/PPP pi-system is genuinely a textbook quasi-1D correlated
electron problem at (nominal) half filling — this is real chemistry, not an
analogy. The PPP/Hubbard-Peierls reduction of conjugated pi-systems is a
65-year-old, well-posed effective model (Pariser–Parr–Pople). So L1→L2 is sound
*as a model reduction*. Caveat already correct in the candidate: the sigma framework
and finite-length end effects contaminate this at small n. This caveat is honestly
stated and is a finite-size *uncertainty*, not a mechanism break.

**L2 → L3 (half-filled 1D chain → a 1D CFT): THIS IS WHERE IT BREAKS — TWICE.**

Break (a) — *the universality class is the wrong one for the validated tool.*
A half-filled 1D Hubbard/PPP chain with SU(2) spin and U>0 does **not** flow to the
c=1/2 Ising CFT. Its low-energy theory is, generically:
- the **c=1 Tomonaga–Luttinger liquid** (gapless spin sector; the doped-polyacetylene
  Luttinger-liquid literature — Na/K-doped trans-polyacetylene — confirms c=1, not
  c=1/2), OR
- at commensurate half filling with electron–phonon coupling, a **Peierls /
  bond-order-wave gapped phase** (dimerized polyacetylene is the canonical gapped
  Peierls insulator; long acenes acquire a polyradical/BOW character that is
  *also* gapped at the relevant scale).

The project's chi=3 MERA was validated against the **c=1/2 transverse-field Ising
CFT** (alpha≈4 stress-tensor, T=(pi/2)l_AdS, target C(r)~r^{-1/4}). The molecular
target is c=1 (different central charge, different operator content, different
scaling dimensions) or gapped (no CFT at all). The "scale-invariant layer" and the
disentangler set were optimized for the Z2-symmetric Ising fixed point. **A MERA
whose scale-invariant tensors sit at the Ising fixed point is not the RG of a
Luttinger liquid.** This is not a finite-size caveat; it is a different fixed point.

Break (b) — *the very thing being diagnosed (gapped vs critical) is set by physics
the validated spin-MERA cannot see.* The acene crossover from "few-determinant
multireference" to "strongly correlated polyradical" is driven by the Peierls/BOW
instability and the U/t ratio of the *fermionic, charge-carrying* pi-electrons. The
gap that determines method choice opens in the charge or dimerization sector. A spin
chi=3 MERA on a Z_i Z_j-correlation state has no charge sector and no fermionic
exchange; it cannot represent the Peierls/charge-gap mechanism that is the actual
discriminator. So even where L1→L2→L3 is a valid *Luttinger-liquid* reduction, the
project's specific tool is blind to the operator that flips the routing decision.

**L3 → L4 (1D CFT → MERA causal cone): FAITHFUL IN GENERAL, MIS-INSTANTIATED HERE.**
It is a genuine theorem-level statement that scale-invariant MERA realizes the
real-space RG of *a* 1D critical fixed point (Vidal; Evenbly–Vidal). That generic
statement is mechanism-faithful. The problem is not L3→L4 in the abstract; it is
that the project's *instantiated* MERA is the c=1/2 instance (Break a), and a
fermionic critical chain additionally requires fermionic disentanglers/isometries
(Jordan–Wigner strings through the causal cone) which the project does not have.
### 1.2 Step-by-step audit of the mapping
### 1.3 Where it breaks — consolidated

Four independent breaks, in descending severity:

1. **Wrong fixed point (KILLER for the candidate as written).** Validated asset =
   c=1/2 Ising MERA. Molecular target = c=1 Luttinger liquid or gapped Peierls.
   Routing on a c-extraction from an Ising-tuned MERA measures the *tool's* bias as
   much as the molecule's class. This is structurally the HYP-014 failure mode:
   the candidate's own Mech=4 prose says "the MERA causal cone IS the RG of exactly
   that class of 1D critical Hamiltonian" — but "that class" is silently swapped
   from Ising (what was validated) to "critical pi-chain" (what is not). The
   identity is asserted across a class change. That is the curve/mechanism
   conflation wearing a chemistry hat.

2. **Diagnostic blind to the discriminating operator.** Gapped-vs-critical for
   acenes is decided in the charge/dimerization sector (Peierls/BOW, U/t). Spin
   chi=3 MERA on a ZZ-correlation state cannot represent it. So the diagnostic can
   return "looks critical, S(L) grows" on a system that is in fact Peierls-gapped
   at the scale that matters for method choice — a false route.

3. **2D character.** Acene/GNR pi-systems are NOT clean 1D: rung coupling across
   the fused-ring ladder is O(t), not perturbative. The 1D-CFT reduction is a
   long-chain *limit*, and real molecules of interest (n=6–12 acenes) are squarely
   in the crossover where the 2D ladder character is strong. MERA-1D coarse-graining
   imposes a 1D RG on a 2D-ish object — a structural mismatch, not a finite-size
   error that shrinks with n.

4. **Input-state circularity.** The candidate feeds "an autoCAS-style orbital-
   correlation matrix" into the coarse-graining pipeline (§7). But that input is
   itself the output of a method choice (orbital basis, partial DMRG sweep, bond
   dimension). You cannot cleanly extract the universality class of the *molecule*
   from a correlation matrix whose entanglement content was already shaped by the
   approximate solver you are trying to route. The diagnostic risks measuring the
   pre-conditioner, not the physics.

### 1.4 Does "spin chi=3 only, no fermionic MERA" matter? YES — materially.

The candidate (Rank 1 §7) sells this as "pure classical compute, reuses existing
project code." That is the most overstated line in the document. The existing code
(`sim2026015_chi3_8q.py`, `sim2026015c_chi3_16q.py`) is a **spin** chi=3 MERA for
the Z2 TFIM with a `entanglement_entropy(sv, l)` routine that returns the raw S(l)
array — no central-charge fit, no fermionic structure. Using it on a molecular
electronic Hamiltonian requires either:
- (i) mapping the fermionic problem to spins (Jordan–Wigner), which puts non-local
  string operators through every disentangler/isometry — the project's tensors were
  never optimized with these and the causal-cone locality that makes MERA cheap is
  exactly what JW strings spoil in >1D / long-range-integral settings; OR
- (ii) building a genuine fermionic MERA (anti-symmetrized tensors, fermionic swap
  gates) — which the project does not have and which is, per the candidate's own
  Rank 3 honest note, "a known very hard, largely-unsolved problem."

So the "reuses existing validated code, no new build" framing is false. At minimum
this is a substantial new build (fermionic MERA or a defensible spin mapping plus a
re-validated central-charge extractor). Buildability is NOT 3; realistically 2.

### 1.5 The project's own validated-asset gap (independent of chemistry)

Checked the actual artifacts. The project validated:
- alpha≈4 force exponent (SIM-2026-011, 008-status SUPPORTED, three measurements);
- T=(pi/2)l_AdS transport (HYP-006 SUPPORTED);
- chi=3 restoring the C(r) power-law (HYP-009 PARTIAL).

It did **not** validate a central-charge extraction. `SIM-2026-015-chi3-mera-design.md`
states the c=1/2 test *conditionally and prospectively*: "If chi=3 achieves
S(l) ~ (c/3) log(l) with c=1/2 ... this confirms chi=3 is in the correct
universality class." MEMORY logs HYP-009 as PARTIAL ("need 24q+ for phase
transition"); no SIM reports a fitted c. The code computes `S_l` but never fits
(c/3)log L. **So the load-bearing phrase in the candidate — "the project's
validated RG-flow-of-entanglement extractor" — describes an artifact that does not
exist in validated form.** What is validated is a *force-exponent* and a
*transport-coefficient* pipeline, not a *central-charge / RG-flow classifier*. The
candidate inherits the project's strongest anti-pattern at the root: it names a
"validated extractor" the way HYP-014 named a Crofton match — the validation is
assumed, not present.

## 2. What it would actually output vs existing diagnostics
### 2.1 The proposed diagnostic
Output: per-molecule block-entropy scaling S(L) under explicit MERA coarse-graining,
fitted to S(L) → const (gapped, area law) vs S(L) ~ (c_eff/3) log L (critical),
yielding an effective central charge / leading scaling dimension → routing label.

### 2.2 Existing strong-correlation diagnostics (what chemistry already has)
- **Single-orbital entropy s_i(1) and total Zs(1)** (Boguslawski/Legeza/Reiher,
  arXiv:1208.6586, 1609.02617): magnitude-at-fixed-scale multireference flag.
- **autoCAS** (Stein–Reiher): orbital-entanglement-driven *automated active-space*
  selection — already a method-routing tool driven by entanglement.
- **Orbital mutual-information graph + TTN topology optimization** (Legeza,
  ct501187j): already chooses network *structure* from the entanglement graph.
- **T1/D1/M-diagnostics, %TAE, FOD**: scalar single-vs-multireference flags.
- **Finite-entanglement / finite-size scaling of S to extract c**: standard in the
  DMRG/MPS community (ITensor-level), routinely applied to *model* chains and, in
  the conjugated-polymer literature, to polyacetylene (c=1 Luttinger-liquid
  extractions already exist — Na/K-doped trans-polyacetylene papers).
- **Bond-dimension growth / truncation-error scaling**: the working chemist's
  *de facto* criticality signal — if chi must grow ~linearly to hold truncation
  error, the state is (log-)critical. This already exists for free in any DMRG run.

### 2.3 Honest comparison: new signal or fancier restatement?

Mostly **fancier restatement**, with one thin genuinely-new sliver:

- Versus autoCAS/Zs(1): the candidate is correct that those answer a *binary*
  (multireference yes/no) and do not return a *universality class*. That distinction
  is real. BUT the operational consequence the candidate sells ("which ansatz /
  bond-dim regime") is *already* delivered, in practice, by **bond-dimension /
  truncation-error scaling in a cheap pilot DMRG sweep** — if c>0 the entropy and
  required chi grow logarithmically with block size and the chemist already reads
  that off the pilot run. The MERA RG-flow gives the *same actionable bit* (gapped
  → modest chi/CCSD/CASPT2 ; log-critical → large-chi/ER) via a far more expensive
  and (per §1) less trustworthy route.
- Versus DMRG finite-size-scaling c-extraction: that *already* extracts an effective
  c from entropy scaling and is the established tool. The candidate's only
  differentiator is "do it under explicit MERA coarse-graining and on an ab-initio
  orbital state as a *per-molecule router*." The "per-molecule on an ab-initio
  state" framing is the novel sliver — but it is precisely the part §1.3(4)
  (input circularity) and §1.3(1) (wrong fixed point) undermine.
- Net: the diagnostic's *decision output* (route to big-chi vs not) is recoverable
  more cheaply and more faithfully from truncation-error scaling of a pilot DMRG
  sweep. The candidate's added value would be a *clean universality-class label*
  (c=1 vs c=1/2 vs gapped) — but the validated tool cannot deliver a trustworthy
  one (§1.3). So in its current form it is a more expensive restatement of a signal
  chemistry already extracts, dressed in a class label the tool cannot certify.

## 3. Prior art
### 3.1 Mature — sets the novelty floor (must distinguish from, NOT novel)
- Orbital-entanglement multireference diagnostics: Boguslawski/Tecmer/Legeza/Reiher,
  arXiv:1208.6586 (jz301319v), Zs(1) arXiv:1609.02617.
- autoCAS automated entanglement-based active-space selection (Stein–Reiher); review
  context arXiv:2501.18263.
- TTN topology / orbital ordering from mutual-information graph (Legeza, ct501187j;
  Szalay/Legeza review qua.24898 — which *explicitly speculates* MERA for
  coarse-grained polyacene orbital subgroups but never delivered it).
- Central charge from entanglement-entropy scaling in DMRG/MPS: standard
  (ITensor discourse t/252; arXiv:2412.18602 entanglement-scaling across a QPT).
- Luttinger-liquid (c=1) extraction in conjugated polymers already exists
  (doped trans-polyacetylene literature, ScienceDirect S1386947708000179 /
  S0301010405006671). **This directly contradicts the candidate's implied c=1/2
  Ising analogy for the validated tool.**

### 3.2 Dangerous overlaps (moving targets)
- Szalay/Legeza review (qua.24898): MERA-for-polyacene is *named as a speculation*
  in the canonical TN-chem review — the candidate's "no located precedent" is too
  strong; the *idea* is in the literature, only an *implementation* is missing.
- Generalized-DMET disentanglement-criterion bath (arXiv:2503.09881): adjacent
  entanglement-driven embedding-boundary selection.
- Trotterized-MERA-VQE for critical spin chains (q-2025-02-11-1631; arXiv:2303.08910):
  MERA-as-method for criticality, spin-chain not ab initio — adjacent.

### 3.3 The genuinely-novel slice, if any
The only defensible novel slice is narrow: *using explicit MERA coarse-graining of an
ab-initio orbital-correlation state to emit a universality-class label as a method
router*. The class-label-as-router idea is partly anticipated (autoCAS routes;
Szalay/Legeza speculate MERA-for-acene; finite-size c-extraction is standard). The
unclaimed combination is real but thin, and it is exactly the combination whose
mechanism fails §1.3. Novelty here is not the problem; faithfulness is.

## 4. Verdict
### 4.1 Mechanism-faithfulness judgment (numeric)

Candidate self-rated **Mech 4/5**. Audited value: **Mech 2/5** (exponent-coincidental
risk — would be FLAGGED and USEFULNESS-capped under the document's own rubric).

Per-link faithfulness scoring (1=analogy/coincidence, 5=identity-in-limit):
- L1→L2 (pi → quasi-1D half-filled chain): **4/5** — sound model reduction, honest
  finite-size caveat.
- L2→L3 (chain → CFT): **2/5** — flows to c=1 Luttinger or gapped Peierls, NOT the
  c=1/2 Ising the tool was validated on; the discriminating gap lives in a
  charge/dimerization sector the spin tool cannot see.
- L3→L4 (CFT → MERA causal cone): **5/5 generic, 2/5 as instantiated** — the generic
  statement is theorem-level; the project's MERA is the Ising instance and lacks
  fermionic structure.
- Validated-asset premise: **1/5** — the "validated RG-flow / central-charge
  extractor" does not exist in validated form; only force-exponent and transport
  pipelines are validated. This is the HYP-014 root pattern: a validation is named,
  not demonstrated.

Weakest-link governs a mechanism claim → **Mech 2**. The candidate's Mech-4 prose
performs the exact conflation the project's lesson forbids: it asserts "the MERA
causal cone IS the RG of exactly that class of 1D critical Hamiltonian" while
silently substituting "critical pi-chain (c=1 / gapped)" for the class actually
validated ("c=1/2 Ising"). That substitution across a class boundary is a
curve/mechanism conflation, not a structural identity.

### 4.2 Disposition and required modifications

**VERDICT: REFUTED as written (Rank 1, Mech 4 claim).** Specifically refuted:
the claim that this is mechanism-faithful and reuses validated project code with
no new build. Both are false: (a) the molecular target is c=1/gapped, not the
validated c=1/2 Ising fixed point; (b) the "validated RG-flow extractor" is not
validated (no c-extraction artifact exists); (c) it requires a substantial new
build (fermionic MERA or re-validated mapping), not code reuse; (d) the actionable
routing bit is recoverable more cheaply and more faithfully from truncation-error /
bond-dimension scaling of a pilot DMRG sweep, which chemistry already does.

**A NEEDS-MODIFICATION residue exists** (do not discard the whole direction):
a *defensible, de-scoped* project IS available, but it is NOT the candidate as
pitched and it is NOT mechanism-faithful to the *molecule* — only to a *model*:
1. Drop the ab-initio / per-molecule framing. Restrict to **model PPP/Hubbard
   acene chains** where L1→L2 is exact by construction.
2. Build (or borrow) a **fermionic** critical-chain MERA, or a c=1-validated spin
   mapping; re-validate a central-charge extractor against the *known* c of the
   model (c=1 TLL, or c=1/2 only in a fine-tuned Ising-like limit) BEFORE any
   chemistry claim. This is the missing validated artifact §1.5.
3. Frame the deliverable as the candidate's own honest fallback: report the *flow
   trajectory and its finite-size deviation*, never a hard label on small n, and
   benchmark the routing decision against truncation-error scaling as the cheap
   baseline it must beat to justify itself.
Under this de-scope the project is a model-chain methods note (Rank-3-like,
buildability 2), not the "per-molecule ab-initio router" the candidate sells.

**Net recommendation: do not pursue Rank 1 as written.** If the broader
TN→chemistry thread is pursued at all, the only mechanism-honest entry is the
de-scoped model-chain version above — and even that competes poorly against the
free truncation-error signal. Recommend SHELVE; record so it is not re-proposed
in the original framing.
