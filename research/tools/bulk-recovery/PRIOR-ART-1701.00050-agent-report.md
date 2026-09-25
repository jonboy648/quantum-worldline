# Prior-art gate report: arXiv:1701.00050 (Kim & Kastoryano) vs PREREGISTRATION-HYP033-DRAFT

Read: arXiv v2, 13 Apr 2017, full text. Target: the BLOCKING GATE in
`D:\quantum-worldline\research\tools\bulk-recovery\PREREGISTRATION-HYP033-DRAFT.md`.

**Gate verdict: the paper does NOT fix the answer. The draft's outcome count stays at 4 and the
cone-vs-cut contrast survives — but for a different and less comfortable reason than the draft
assumes, and the paper supplies a physics argument that shifts the honest prior further toward
outcome 4.**

---

## a. Precise main results, and what controls them

**Framework.** MERA read in the Heisenberg picture: the coarse-graining map
`Phi^{s+1}_s(.) = W_{s+1}(.)W+_{s+1}` is a unital CPTP channel (Eq. 2.3). Code subspaces are
`C_s = {W_1...W_s|phi_s> : |phi_s> in H_s}` — the *whole* Hilbert space at scale s pushed to the
boundary, not one bond. Logical operators are bulk operators at scale s conjugated down by the
isometries (Sec. 3), i.e. exactly the draft's insertion-on-an-internal-leg object, generalized to
the full layer.

**The controlling quantity.** On an *elementary block* the channel has the spectral form (Eq. 2.5)

> `Phi(O) = sum_k lambda_k tr[O R_k] L_k`, with `lambda_0 = 1`, `L_0 = 1`, `R_0 = rho_ss`

and Definition 2 sets

> "`nu := -log_2(Re[lambda_1])` will be referred to as the **scaling dimension**", with the class of
> channels called **RG-regular** when nu is "strictly larger than zero."

So the draft's guess was right in form: **the scaling superoperator's second eigenvalue is exactly
what controls everything.** Every bound in the paper is a power of `2^{-nu(...)}`.

**The three results.**

- **Lemma 3 (Sec. 4.1, Eq. 4.1)** — decoupling of a simply connected region A from the purifier R:
  `|tr[(rho^{AR}_0 - rho^A_0 (x) rho^R_0) O^{AR}]| <= C||O^{AR}|| 2^{-nu(s - log_2|A|)}`,
  with (from the proof) `C = 2d^2`, d = elementary-block dimension.
- **Corollary 1 (Eq. 4.5)** — erasure correctability:
  `||R(rho^{A^c R}) - rho^{A A^c R}||_1 <= C 2^{-nu(s - log_2|A|)/2}`.
- **Theorem 2 (Sec. 4.2, Eq. 4.6)** — *local* correctability, the key technical result. A simply
  connected, B a shield of width x around A, `|AB| < 2^s`, C the complement of AB. Then there
  exists `R^{AB}_B : B(H_B) -> B(H_AB)` with
  `||R^{AB}_B(rho^{BCR}_0) - rho^{ABCR}_0||_1 <= c(|A|/x)^{nu/2}`.
- **Theorem 3 (Sec. 5.2, Eq. 5.4)** — the Lieb-Robinson/bulk-causality application:
  `|<rho_0|[O_1(t),O_2]|sigma_0>| <= c'(v|t| + xi nu s)^nu 2^{-nu s}`.
- **Sec. 5.1** — code distance `d <= C(n/k)^alpha`, `alpha = log2/log(2z/(z-1)) ~ 0.63` for
  `z = |AB|/|A| = 3`; minimal logical support is a Cantor set (Fig. 2b), "we partially recover the
  so called `uberholography,' which was suggested recently by Pastawski and Preskill [29]" — and
  their alpha is *stronger* than Pastawski-Preskill's ~0.78.

**The machinery underneath** is Theorem 1, imported verbatim from ref. [22] (Flammia-Haah-
Kastoryano-Kim, arXiv:1610.06169): the decoupling <=> recoverability duality. In words, per Sec. 3:
"erasure of a region A is locally correctable from a recovery operation on AB if and only if ACR is
decoupled into A and CR."

**Assumptions.**
- **Scale invariance is required** (Definition 1: `V_xs = V for all xs,s` and `U_ys = U for all
  ys,s`) for the transfer-operator step. Their s ranges to `s_max = O(log N)`.
- **RG-regular**: the block channel is non-defective (spectral decomposition exists — the appendix
  notes `T^` "typically has Jordan blocks" in general) and nu > 0.
- **Binary vs ternary**: figures are binary ("Locality (3-adjacent) of the observable is preserved
  at all levels"; "the constant c is 2"), but "our results hold for the more general construction
  above" — i.e. any `W_s = (x)_xs V_xs (x)_ys U_ys`. Ternary is covered; the branching ratio enters
  through c and through the log base.
- **Bond dimension never appears.** chi enters *only* through the prefactor `C = 2d^2` — so a larger
  chi makes their bound numerically *worse*, and the exponent nu is chi-independent.
- **Approximate, not exact**, and explicitly so: "erasures of bounded regions can be corrected up to
  a polynomially small error, rather than exponentially small error."
- 1D for concreteness; they claim straightforward extension to higher d.

---

## b. Which boundary region suffices? (the part the draft actually needs)

The paper gives **three different answers, none of which is the draft's contrast**, and it
explicitly declines the wedge.

1. **Corollary 1**: recovery from the *complement of a small simply connected region*. Global, not a
   cone.
2. **Theorem 2**: recovery from a **shielding metric neighborhood** B of width `x >= |A|`. Not a
   causal cone, not a minimal cut — an annulus, with the recovery region's *width* the tuning
   parameter.
3. **Sec. 5.1**: the minimal support of a logical operator is **fractal** — "We see that it takes a
   cantor-set type form, as already suggested in Ref. [29]."

**The causal cone appears only as a hypothesis, never as a conclusion.** Sec. 2.1 defines it purely
as support bookkeeping ("The set of the supports over different scales ... is said to be the past
causal cone"), and Lemma 2 (Eq. 2.10) *assumes* non-overlap: "If `A_{s'} ^ C_{s'} = empty, for all
s' <= s`". In Theorem 2's proof, "r is chosen to be the scale after which the past causal cones of A
and CR overlap with each other." The cone sets where the estimate stops working; it is never
identified as the minimal recovery region.

**The entanglement wedge is named as an open problem.** Sec. 6, verbatim:

> "However, many important issues remain. For one thing, it will be interesting to understand the
> entanglement wedge reconstruction[4] in our framework. **The approximate nature of our bound makes
> this analysis challenging.**"

And on why the bound is too coarse:

> "our bound is not strong enough to ensure locality at sub-AdS scale. This was to be expected
> because our bound does not incorporate the properties that are expected to be satisfied by
> conformal field theories with a semi-classical gravitational dual: **that there is a gap in the
> scaling dimension of the operators.**[33]"

One more quote the draft should carry, because it speaks directly to RESEARCH-DIRECTOR Sec. 29 (the
trunk question):

> "In its present form, our conclusion is so general that it is even applicable to **free-fermion
> systems, which is unlikely to admit a semiclassical gravitational dual** [18]."

That is the authors stating that their own emergent-code result carries **no** operational content
distinguishing "has a gravity dual" from "doesn't."

---

## c. What it predicts for ternary MERA, critical Ising, chi = 6-8, three layers

**Nothing usable. The bounds are numerically vacuous at this depth by roughly ten orders of
magnitude in the required scale separation.** Three independent reasons:

**1. nu is small for Ising, and the paper's exponent is nu.** *(This calculation is mine; the paper
never evaluates nu for any model.)* The ascending superoperator's eigenvalues are
`lambda_alpha = b^{-Delta_alpha}` with b the coarse-graining factor. For ternary MERA b = 3, and
Ising's lowest nonzero scaling dimension is Delta_sigma = 1/8, so `lambda_1 = 3^{-1/8} = 0.8717`. In
K-K's base-2 convention `nu = -log_2(0.8717) = 0.198`; in the base natural to a ternary net,
`nu = Delta_sigma = 0.125`. Either way **nu ~ 0.13-0.20**. Useful side effect: nu is *not* a free
parameter for this project — the SIM-061 pipeline already measures Delta_sigma to ~1.3%, so nu is
measured, not fitted.

**2. Corollary 1 at s = 3.** With `|A| = 2`, nu = 0.198: `2^{-nu(s-log_2|A|)/2} = 2^{-0.198} = 0.87`.
The prefactor `C = 2d^2` with `d = chi^2` (ternary cone width 2) is 2592 at chi=6 and 8192 at chi=8.
Bound ~ **2.3e3**, against a trace distance that cannot exceed 2. To reach a 10% bound you need
~ **150 layers** at chi=6 — or ~ **34 layers** even if you charitably set the prefactor to 1.

**3. Theorem 2 at s = 3.** Exponent nu/2 ~ 0.099. A 10% error with c = 1 needs
`x/|A| ~ 1.2e10`, while the theorem's own constraint `|AB| < 3^s = 27` caps x at ~25 sites.

**Bound, not equality, and one-sided.** Every result is an *upper* bound on recovery error, i.e. a
*lower* bound on the draft's f. **There is no lower bound on recovery error anywhere in the paper**
— nothing that says "f must drop here." The draft's registered statistic is `m*`, the *location of
the largest single drop* in `f(A_m)`. That statistic is unconstrained by this paper in either
direction. This is the single most important finding for the gate.

**Silent on the contrast.** The paper never sets cone against cut, and Sec. 6 says the wedge
analysis is blocked by the approximate nature of the bound.

---

## d. Honest assessment: outcomes remaining, and what is pre-empted

**Outcome count: still 4.** The draft's kill condition "If 1701.00050 predicts f(A_m)
quantitatively and the measurement agrees -> Level 1, HYP-033 closes as answered by prior art"
**does not fire.** The bound is one-sided, asymptotic, and vacuous at k=3.

**Pre-empted — must be cited, never claimed:**

| Draft element | Status after K-K |
|---|---|
| "Bulk information at deeper layers is better protected against boundary erasure" | **Theirs** (Lemma 3, Corollary 1). Monotone improvement with depth is Level 1 validation. |
| "MERA at criticality is an approximate holographic code" | **Their headline.** Unavailable as a finding. |
| **G1** (structural zero for A disjoint from the cone) | Follows from support preservation, Sec. 2.1. Draft already calls it Level 1 — correct. |
| The observable itself: `rho^{AR}` vs `rho^A (x) rho^R`, with a purifying reference R | **Exactly the quantity Lemma 3 bounds**, and the decoupling<=>recoverability duality is their Theorem 1 (from 1610.06169). The draft should cite this as *why* I(R:A) is the right observable, not present it as a design insight. |
| "Recovery does not need the whole footprint" as a qualitative claim | **Pre-empted** by Sec. 5.1 uberholography (alpha ~ 0.63) and Pastawski-Preskill 1612.00017 — in the nu -> infinity limit only. |

**Not pre-empted:**

- **`m*`, the location of the drop.** No bound in either direction. The primary observable retains
  its content.
- **Cone vs cut at finite nu and finite depth.** Explicitly open (Sec. 6).
- **Whether cut-tracking is specific to the optimized critical state vs. the graph.** K-K
  *strengthens* the case that the controls are load-bearing: their result is so
  representation-generic it covers free fermions with no gravity dual. A result that does not
  separate optimized from Haar is therefore *expected*, and only C-HAAR separation is interesting.
- **Anything at finite chi.** chi is absent from the paper.
- **C-GAPPED (h = 1.5).** Outside their hypotheses entirely — Definition 1 requires scale invariance
  and Definition 2 requires nu > 0.

**The prior update the draft should absorb.** K-K supplies a *physics* reason, not merely a
resolution reason, to expect outcome 4:

> nu = Delta_sigma = 1/8 is small **because the Ising CFT has a light operator.** Recoverability
> therefore degrades *slowly and smoothly* with scale separation. Nothing in the theory produces a
> sharp threshold at finite nu. A sharp threshold is a nu -> infinity phenomenon (K-K's own
> admittedly unphysical limit: "We do not expect this limit to be physical... However, it is the
> limit in which all of our statements become exact"), and the competing minimal-cut result
> (1601.01694) lives at **large bond dimension** — not chi = 6-8.

So outcome 2 (sharp cut-tracking in the optimized net, smooth in Haar) requires sharp behavior in
precisely the regime where both relevant theories predict smoothness, at a chi far below where the
random-tensor minimal-cut result applies. **Most likely result: smooth in both arms — outcome 4,
with C-HAAR also smooth. Level 2, or Level 3-negative.** That should be written into the draft's
honest prior with this reason attached, replacing the current bare assertion.

**Two structural notes, flagged as my analysis rather than the paper's:**

1. **f(A_0) = 1 and f(A_disjoint) = 0 are structural identities, not measurements.** G1 forces
   I(R : outside cone) = 0; purity (G2) then gives f(C(b)) = 1 exactly. So the plateau and the floor
   are guaranteed and carry zero information — only the *shape* between them is data. The draft
   should say so explicitly, or G1/G2 passing will read as partial confirmation when it is
   arithmetic.
2. **The discriminating window may be empty, and this is a bigger threat than prior art.**
   `A_m` is a subset of `C(b)`, so A_m is a *small* boundary region — for a k=1 bond in a 27-site
   ternary net, roughly 6 sites. The minimal cut of a small interval reaches depth ~log_3|A| and
   encloses only the layers below it, so for `A = C(b)` the cut passes essentially *at* b. In a
   MERA, cone and wedge are governed by the same geometry, so "b inside the wedge while the
   footprint is incomplete" may be a window of width zero or one site at three layers. **This
   belongs in G0**: before registration, compute gamma_{A_m} explicitly for every m in the family
   and show the window is non-empty at k = 1 and k = 2. If it is empty, the experiment has no
   discriminating region and the draft's own logic voids it.

---

## e. Follow-up papers doing the numerical experiment

**None that I can verify.** I pulled the citation graph (34 entries; Semantic Scholar's list is
noisy and includes pre-2017 references, so treat it as non-exhaustive) and read the abstracts of the
six plausible candidates via the arXiv API. Verified as existing, and what each actually is:

- **arXiv:2406.09555**, Sang, Hsieh, Zou, *Approximate quantum error correcting codes from conformal
  field theory* (2024) — closest in spirit, and **analytic**: 1+1D CFT codes under extensive local
  dephasing, finite threshold iff the minimal nonzero scaling dimension in the jump operator's
  fusion algebra exceeds 1/2, `k >= Omega(log log n)`. Applies it to critical Ising. **Note the
  collision with our setting: Delta_sigma = 1/8 < 1/2.** No MERA numerics, no cone/cut contrast.
- **arXiv:2103.08631**, Cao, Pollack, Wang, *Hyper-invariant MERA* — construction plus an analytic
  no-go (a single tensor type cannot be both locally contractible and power-law correlated). Not the
  measurement.
- **arXiv:2010.05960**, Cao, Lackey, *Approximate Bacon-Shor code and holography* — discusses
  entanglement wedge and bulk reconstruction, but in a Bacon-Shor/perfect-tensor construction, not
  an optimized MERA.
- **arXiv:2112.05099**, Furuya, Lashkari, Moosa, *Renormalization group and approximate error
  correction* — cMERA for massive free fields, and argues code price/distance must be defined w.r.t.
  the reconstructable wedge. Analytic, non-critical, no MERA numerics.
- **arXiv:1806.05007**, Ling et al., *Quantum error correction and entanglement spectrum in tensor
  networks* — greedy-algorithm/"critical protection" in constrained planar networks. Adjacent
  (greedy ~ causal wedge) but not optimized-MERA numerics.
- **arXiv:2004.04173**, Jahn, Zimboras, Eisert, *Tensor network models of AdS/qCFT* — regular
  hyperbolic tilings, qCFT; not MERA recovery.

Two targeted arXiv export API queries returned genuine zeros —
`abs:"multiscale entanglement renormalization" AND abs:"entanglement wedge"` and
`abs:"causal cone" AND abs:"minimal cut"` both reported `totalResults = 0`. I confirmed the endpoint
was live rather than silently dropping lines with a control query
(`abs:"entanglement renormalization" AND abs:"quantum error correction"` -> `totalResults = 3`,
correctly including 1701.00050 itself). So the emptiness is real, not the scan-#17 failure mode.

Also relevant and verified present in the citation set, worth cataloguing alongside:
**arXiv:2102.02619** (Jahn & Eisert, *Holographic tensor network models and quantum error
correction: a topical review*) — the natural place to check for any numerics I missed;
**arXiv:1612.00017** (Pastawski & Preskill, uberholography — the alpha ~ 0.78 that K-K improves on);
**arXiv:1610.06169** (Flammia, Haah, Kastoryano, Kim — the source of Theorem 1).

---

## Could not verify / labelled as inference

- I read **arXiv v2 (13 Apr 2017)** via PDF text extraction. The extraction garbles some math:
  daggers, sub/superscripts, and the operator ordering in Sec. 3's logical-operator expression
  (`W_s...W_1 O W+_1...W+_s`, whose index order is inconsistent with `W_s : H_s -> H_{s-1}` as
  printed). I quoted around the damage where I could; equation *content* I reconstructed from
  surrounding prose is flagged in place. **I did not check the published JHEP version against arXiv
  v2.**
- **nu ~ 0.125-0.198 for ternary Ising is my calculation**, from the standard
  `lambda_alpha = b^{-Delta_alpha}` relation plus Delta_sigma = 1/8. The paper evaluates nu for no
  model.
- **`C = 2d^2` with `d = chi^2`** is Lemma 3's proof combined with the standard ternary causal-cone
  width of 2. The paper says only "d is the dimension of the elementary block, which is bounded by
  some constant."
- The structural notes in (d) — f(A_0) = 1 as an identity, and the possibly-empty discriminating
  window — are **my structural reasoning about the draft, not statements from the paper.**
- One genuine mismatch with the draft's object that I could not resolve from the paper: K-K's code
  subspace is the *whole* layer-s Hilbert space, whereas the draft inserts on a *single bond*. Their
  bounds apply to the draft's case (a bond is a subsystem of H_k) but are loose there — correcting
  erasure for the whole logical space is strictly harder than for one bond. The paper offers no
  single-bond refinement.
- The Semantic Scholar citation list is **not exhaustive** (34 entries, one with no id, several
  evidently references rather than citations). I cannot rule out a numerical follow-up outside both
  that list and the two arXiv queries.

---

## Recommended disposition of the gate

Record it as PASSED-with-constraints, not as a block. Cite 1701.00050 for the observable, for the
depth-monotonicity result, for nu as the controlling parameter, and for the wedge being open. Delete
any draft language claiming emergent-code or depth-protection novelty. Re-weight the honest prior to
outcome 4 *with K-K's small-nu reason stated*. Add the gamma_{A_m} window computation to G0 before
registration.
