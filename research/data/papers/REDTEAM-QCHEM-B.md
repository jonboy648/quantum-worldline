# RED TEAM — QCHEM-COMBO-B Tensor-Network → Quantum-Chemistry Bridge

**Role:** Devil's advocate. Source: `research/data/papers/QCHEM-COMBO-B-tnbridge.md`.
**Lens:** the project's documented repeat failure — "an exponent / curve match is not
a mechanism" (HYP-014 REFUTED, HYP-017 closeout). For each top-5: is the tensor-network
structure GENUINELY faithful to the molecular Hamiltonian, or is it the HYP-014 pattern
(right-looking diagnostic without the real chemistry/correlation physics)? Plus: is it
already standard in mature QC-DMRG / TN-chemistry / entanglement-diagnostic literature?

Status: DRAFTING.

---

## The core attack surface (applies to all five)

There are FOUR structural cracks that every candidate sits on top of. None is
addressed quantitatively in QCHEM-COMBO-B; the file asserts mechanism-faithfulness
where it should be proving it.

**C1 — The molecular Hamiltonian is not a 1D critical model, and the one place it
gets closest is the OPPOSITE regime to what the file invokes.** The file's entire
Mech-4 claim for Ranks 1/2/3 rests on "long polyacene / poly(p-phenylene) / metallic
GNR π-systems are genuinely described by a 1D critical effective theory (Hubbard/PPP
chains at half filling)" (lines 66–72). This is backwards. The 1D Hubbard model **at
half-filling is a gapped Mott insulator** (charge gap opens for any U>0 by exact Bethe
ansatz); it is a *Luttinger liquid / critical* only **off half-filling or under doping**
(arXiv:cond-mat/9510014; the Luttinger-liquid acene evidence in the literature is
explicitly *sodium-DOPED* trans-polyacetylene, ScienceDirect S1386947708000179, not
neutral acene). Neutral closed-shell acene π-systems at half-filling are precisely the
*gapped Mott-like* case — the one the file itself says is the "DMRG/CASPT2 with modest
bond dim suffices" class it wants to route AWAY from. The file has the universality
class of its own flagship example inverted. The genuine static-correlation story in
long acenes is a polyradical / open-shell singlet (Hubbard-Mott, gapped, area-law),
not a gapless c=½/c=1 critical chain. The MERA causal cone is the RG of a *scale-
invariant* (critical) chain; the actual chemistry it points at is *not* at that fixed
point and does not flow to it. This is the HYP-014 pattern in its purest form: a
structure (scale-invariant MERA) whose diagnostic (log-S, finite c) will *look right*
on any system with a long enough correlation length, applied to a Hamiltonian whose
real low-energy physics is a different class.

**C2 — There is no validated map from an ab initio orbital state into the project's
MERA causal cone.** The project asset is *spin* chi=3 MERA validated on the 2D Ising
CFT. A molecular Hamiltonian is fermionic, has long-range 1/r Coulomb two-electron
integrals (not nearest-neighbour), and its "geometry" is an orbital ordering, not a
spatial lattice. Mapping it into a MERA requires (a) a fermionic MERA (Swingle-Corboz
fermionic-tensor swap-gate machinery) and (b) a choice of orbital ordering that
*creates* the 1D structure the ansatz then "discovers." A targeted literature search
for fermionic MERA for ab initio molecular Hamiltonians returns essentially nothing
delivered (only spin-chain Trotterized-MERA-VQE and neural-net fermionic states) —
confirming this is unsolved, but also fatal to the *mechanism-faithful* claim: you
cannot assert the TN structure is faithful to the molecular Hamiltonian when the map
that would make it faithful does not exist and the diagnostic instead runs on a
*spin* surrogate whose relationship to the fermionic problem is itself the unproven
step. The file concedes buildability ≤2 for Ranks 2/3 but does NOT debit
mechanism-faithfulness for the same gap — it should. An unvalidated map is an
unfaithful map until proven otherwise.

**C3 — Orbital ordering manufactures the 1D-critical signal.** S(L) block-entropy
scaling and an extracted "effective central charge" depend entirely on how the
fermionic orbitals are threaded onto the 1D chain that MERA/DMRG sees. Legeza's
mutual-information orbital-ordering optimization (ct501187j) exists precisely because
this choice changes the entanglement profile by orders of magnitude. A log-like S(L)
with c≈½ can be produced or destroyed by reordering the same molecule's orbitals. So
"we measured a log flow ⇒ the molecule is critical-class" is confounded by a free
parameter that the analyst sets. This is a curve-fit-coincidence generator by
construction.

**C4 — Entanglement-scaling central-charge extraction inside a chemistry DMRG
pipeline is already standard.** Finite-entanglement-scaling central charge from DMRG
is textbook (ITensor discourse t/252; finite-entanglement-scaling theory, Pollmann
et al.). Single-/two-orbital entropy and mutual information as the routing diagnostic
for active space and method choice is exactly what autoCAS / Stein–Reiher do from
*partially converged* DMRG (J. Chem. Theory Comput. 2016, 12, 1760; Mol. Phys. 2017,
115, 2110; jcc 2019, 40, 2216), and the DMRG-tailored-CC / pCCD-entanglement lines
already use the orbital-entanglement spectrum to decide what goes to DMRG vs CC. The
novelty therefore lives only in the word "RG-flow under explicit coarse-graining" vs
"magnitude at fixed scale" — a thin slice, and one that C1–C3 undermine.

---

## Rank 1 — RG-flow criticality fingerprint (file score 48, Mech 4)

**Strongest reason it is the HYP-014 pattern, not a mechanism.**

The file's own justification (lines 64–80) is: the MERA causal cone "*is* the real-space
RG of exactly that class of 1D critical Hamiltonian … built to be the fixed-point
structure of a scale-invariant 1D system, which is what a critical π-chain *is*." Every
clause of this is the coincidental-fit trap:

1. **The flagship example is in the wrong universality class (C1, KILLER).** The file
   stakes Mech-4 on long acene π-systems being "Hubbard/PPP chains at half filling …
   1D critical." Neutral acenes at half filling are a *gapped* Mott/polyradical regime,
   not a gapless critical chain. The Luttinger-liquid acene evidence is doped
   polyacetylene, not the neutral closed-shell molecules a chemist would route. So the
   ONE concrete chemical system offered to make the mechanism real is exactly the
   system for which the mechanism is false. A diagnostic whose justifying example is
   mis-assigned is not mechanism-faithful — it is a structure that will report
   "critical-like" because long correlation length + finite bond dim *always* yields a
   pseudo-log S(L) (this is the finite-entanglement-scaling artifact, not physics).
   This is HYP-014 verbatim: amplitude/shape looked right; mechanism was absent.

2. **The "flow, not a label" defense is unfalsifiable, not rigorous (self-inflicted).**
   The file pre-empts the finite-size objection (lines 76–80, 94–99) by saying the
   deliverable is "the *flow* with the finite-size deviation reported as the
   uncertainty." But a molecule that is genuinely gapped *also* shows a rising-then-
   saturating S(L) at small L that, truncated early, is indistinguishable from a
   slow critical flow. With "report the flow and its deviation" there is no
   pre-registered criterion that a gapped molecule would *fail*. A diagnostic that
   cannot produce a NO is a coincidence detector. Compare HYP-017-R3: a publication
   threshold that a correct measurement would *fail* is the tell; here the inverse —
   no threshold a wrong-class molecule would fail.

3. **The signal is operator-defined by the analyst (C3).** c is extracted after an
   orbital ordering is chosen; reordering moves it. No mechanism is faithful if a free
   preprocessing knob sets the answer.

4. **The novel slice is thinner than claimed and partly anticipated (C4).** "RG flow
   under coarse-graining" vs "entropy magnitude at fixed scale": autoCAS already
   routes method choice from partially-converged DMRG entanglement; finite-entanglement
   scaling already extracts c inside chemistry DMRG. The genuinely unclaimed sliver is
   "per-molecule *universality-class label* via explicit MERA blocking." That sliver is
   real but small, and C1–C3 mean the label it produces is not trustworthy on the very
   systems (extended π) it is sold for.

**Verdict on Rank 1:** Down-score hard. The Mech-4 rating is unjustified; on the
evidence it is Mech 2 ("exponent/shape-coincidental risk"), because the structure
produces a critical-looking S(L) flow on systems whose true class is gapped, its
justifying chemical example is mis-classified, and it has no pre-registered failure
mode. It survives ONLY if reframed as a *finite-entanglement-flow heuristic with a
pre-registered gapped-vs-critical decision boundary calibrated on systems of known
class* — i.e. stripped of the universality-class-label claim. As written, it is the
project's documented repeat failure with a chemistry label.

## Rank 2 — Scale-resolved disentangler correlation spectroscopy (file 24, Mech 4)

**Strongest reason it fails / is a disguised standard method.**

1. **The "dangerous overlap" is worse than the file admits.** Confirmed:
   arXiv:2503.09881 (Negre, Faulstich, Kim, Ayral, Lin, Cancès, "New perspectives on
   Density-Matrix Embedding Theory", Mar 2025) builds the embedding bath by
   *optimizing a quantitative criterion of maximal disentanglement between fragments*
   — i.e. the exact deliverable of Rank 2 ("layer at which an orbital block stops
   being disentanglable ⇒ fragment boundary"). The file calls this "adjacent" and
   claims a "new slice" (scale-resolved MERA *layers* vs DMET's abstract optimization).
   But this distinction is mechanically empty: the only thing that matters for the
   chemistry deliverable is *which orbitals end up in the fragment/active space*. DMET-
   2025 already produces that from a disentanglement criterion. "We got the same
   boundary from MERA disentangler layers instead of a 1-RDM disentanglement objective"
   is a reimplementation, not a new mechanism, unless it provably produces a *better*
   boundary — which the file does not argue and cannot, having no fermionic MERA.

2. **C2 fatal here specifically.** "Apply MERA disentanglers to a fermionic orbital
   state" requires fermionic MERA disentangler optimization for ab initio orbitals —
   the file itself rates buildability 2 and the literature search confirms it is not a
   delivered technique. With no working fermionic disentangler the "scale-resolved
   correlation length spectrum" is a thought experiment; the Mech-4 rating ("this is
   structurally what disentanglers *are*") is true for *spin* disentanglers and
   unproven for the fermionic ab initio object actually needed. Mechanism-faithful for
   the wrong Hamiltonian is not mechanism-faithful.

3. **Even granting the tool, the output is already a standard concept.** "Correlation
   length spectrum per orbital region" is what two-orbital mutual information vs orbital
   distance already provides in autoCAS/Legeza workflows; "where short-range correlation
   stops" is the entanglement-localization picture DMET/cluster methods operationalize.
   Mech-faithful, but novelty collapses against C4 + 2503.09881.

**Verdict on Rank 2:** Down-score. Not a curve-fit coincidence (the mechanism is
sound *in principle*), but it is (a) substantially pre-empted by arXiv:2503.09881 and
the mutual-information fragment-selection literature, and (b) un-buildable with project
assets (no fermionic MERA), so its Mech-4 is asserted on a spin surrogate. Net: a
reimplementation of an existing 2025 idea using a tool the project doesn't have.

## Rank 3 — Logarithmic causal cone for long-range π correlation (file 24, Mech 4)

**Strongest reason it fails / is a disguised standard method.**

1. **The premise ("QC-DMRG bond dimension explodes for long acenes because the state's
   1D area law is log-violated by criticality") is the C1 error again, and it is the
   load-bearing claim.** DMRG bond dimension in long acenes grows mainly because (i)
   orbital ordering of a quasi-2D fused-ring π-manifold onto a 1D MPS path has
   intrinsically long-range entanglement (a *2D-character*, not a *1D-critical*,
   problem) and (ii) the open-shell polyradical (Mott) character. Neither is "1D
   criticality." MERA cures *log-violation from a 1D critical point*; it does NOT cure
   *2D area-law entanglement projected onto a line* (that needs 2D PEPS/branching MERA,
   a different ansatz). So the "structural match between the failure mode and the
   ansatz" the file claims for Mech-4 (line 140) is a *mis*-match: the real failure
   mode (2D + Mott + ordering) is not the failure mode MERA fixes (1D critical). This
   is precisely "the structure looks like it should fit the diagnostic but does not
   contain the real physics."

2. **C2, at its most severe.** Fermionic ab initio MERA with long-range two-electron
   integrals threaded through disentanglers and isometries (fermion-sign bookkeeping at
   every tensor) is, by the file's own admission and the literature, a "known very
   hard, largely-unsolved problem … buildability 2 and honestly maybe 1." The project
   has spin chi=3 only. A method that cannot be built on the molecular Hamiltonian
   cannot be mechanism-faithful to it; at best it is faithful to a PPP toy.

3. **The PPP-model fallback is not the chemistry problem.** The file's salvage (line
   149: "even a model-PPP-Hamiltonian acene demonstration") quietly drops the ab initio
   Coulomb tail and the σ-framework — i.e. it solves a *spin/extended-Hubbard toy that
   is engineered to be 1D-critical*, then claims relevance to molecular static
   correlation. That is the HYP-014 move: validate on the model that is built to show
   the effect, infer a mechanism for the real system that the model omits.

**Verdict on Rank 3:** Down-score. Mechanism-faithful only to a 1D-critical toy that
is NOT the regime real long acenes occupy (gapped/Mott/2D), un-buildable ab initio
with project assets, and its central "failure-mode = ansatz" claim is a category error.
High coincidental-fit risk via the PPP-toy fallback.

## Rank 4 — Geometric/holographic bond-structure chooser (file capped 18, Mech 2)

The file already self-flags this as the project's trap shape ("hyperbolic-embeddable ⇒
MERA-appropriate" is suggestive analogy, not a theorem) and caps it. I concur and add
two sharper kills:

1. **Hyperbolicity of the mutual-information graph is generic, not diagnostic.** Almost
   any sparse correlation graph with a few hub orbitals and tree-like decay embeds into
   H² with low distortion (Sarkar/Gromov δ-hyperbolicity is common for real-world
   sparse graphs). Low hyperbolic distortion therefore does NOT discriminate "needs
   MERA" from "needs MPS/TTN" — it is satisfied by molecules all three ansätze handle.
   This is the cleanest possible HYP-014: a geometric property that *looks* like the
   AdS/MERA structure but carries no information about which ansatz minimizes truncation
   error.
2. **Anticipated.** Legeza's mutual-information-graph network-topology / orbital-
   ordering optimization (ct501187j) already selects MPS-vs-TTN structure from exactly
   this graph; the hyperbolic-embedding reframing adds no mechanism. **Verdict:** keep
   killed. Correctly down-scored in the file; do not re-propose.

## Rank 5 — CFT-OPE structured cumulant estimator (file capped 8, Mech 2)

File already flags as "HYP-014 wearing a chemistry hat" and caps it. Concur, sharpen:
a generic molecular connected correlator has no conformal symmetry, so decomposing it
into σ/ε "scaling-operator channels" imposes a basis the Hamiltonian does not select —
the channel weights are an arbitrary projection, and any apparent "channel structure"
would be the analyst's basis, not the molecule's physics. This is the HYP-022 pattern
(PEE-thread/Kirillov-Kostant measure also gave a clean-looking number, α=0.883, with
guards passing, yet was structurally the wrong route). **Verdict:** keep killed.

---

## VERDICT

**Summary table (red-team revision of the file's Mech axis).**

| Rank | File Mech | Red-team Mech | Disposition |
|---|---|---|---|
| 1 RG-flow criticality fingerprint | 4 | **2** | Down-score (coincidental-fit risk); survives only if reframed, stripped of universality-class-label claim |
| 2 Disentangler correlation spectroscopy | 4 | 3 | Down-score: pre-empted by arXiv:2503.09881; un-buildable (no fermionic MERA) |
| 3 Log causal cone for π correlation | 4 | 2 | Down-score: category error (2D/Mott ≠ 1D-critical); PPP-toy fallback is the HYP-014 move |
| 4 Holographic bond-structure chooser | 2 (capped) | 1 | Keep killed (correctly) |
| 5 CFT-OPE cumulant estimator | 2 (capped) | 1 | Keep killed (correctly) |

**What survives:** *Nothing survives at its stated Mech rating.* The file's central
claim — that Ranks 1–3 clear the project's exponent-coincidence trap because the MERA
causal cone is the literal RG of the 1D-critical Hamiltonian that long π-systems
realize — rests on a universality-class misassignment (C1: neutral acenes at half
filling are gapped Mott/polyradical, NOT gapless critical; the only Luttinger-liquid
acene evidence is *doped* polyacetylene). Remove that load-bearing claim and Ranks 1–3
lose their Mech-4 justification simultaneously.

**The single most defensible bridge (conditionally):** **Rank 1, but only in a
deflated form** — a *finite-entanglement-flow heuristic* that does NOT claim to assign
a CFT universality class, and that ships with a **pre-registered gapped-vs-critical
decision boundary calibrated on molecules of independently known character** (e.g.
short vs long acene with reference CASPT2/DMRG polyradical indices). Deflated this way
it is honest (it measures a flow and is allowed to say "gapped"), reuses the project's
real validated asset (the coarse-graining/scaling extractor), needs no fermionic MERA
(it can run on the *spin* orbital-correlation surrogate the project actually has, with
that surrogate explicitly labelled a heuristic), and has a genuine if narrow novel
slice vs autoCAS (flow-based vs magnitude-based routing). It is defensible *as a
heuristic router*, NOT *as a mechanism-faithful universality-class detector*. Sold as
the latter, it is HYP-014 with a chemistry label.

**The one I would kill outright:** **Rank 3 (Logarithmic causal cone for long-range π
correlation).** It combines all three fatal flaws at maximum severity: a category
error in its core premise (DMRG blowup in acenes is 2D-character + Mott, the regime
MERA does *not* fix, not 1D-criticality, the regime it does), zero buildability with
project assets (fermionic ab initio MERA is unsolved; project has spin chi=3 only),
and an explicit PPP-toy fallback that is precisely the documented repeat-failure move —
validate on the model engineered to show the effect, then claim the mechanism for the
real Hamiltonian the model omits. Highest coincidental-fit risk of the five; remove
from the menu.

**Cross-cutting recommendation:** the file's Mech axis was scored on *whether the
analogy is structurally appealing*, not on *whether the molecular-Hamiltonian → 1D-
critical-model map is provably valid for the proposed chemical system*. That is exactly
the scoring error that produced HYP-014. Any future QC-bridge proposal must state the
target molecule's *independently established* correlation class (gapped Mott /
polyradical / genuine LL via doping) BEFORE invoking a critical-TN ansatz, or it is
presumed coincidental.

Status: COMPLETE.
