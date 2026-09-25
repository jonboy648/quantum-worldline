# QCHEM-COMBO-B — Tensor-Network → Quantum-Chemistry Bridge Hunt (2026-05-17)

**Framing QC-B.** Goal: novel combinations bridging this project's MERA / CFT /
entanglement-structure machinery to QUANTUM CHEMISTRY (molecular/material electronic
structure). Scored N×B×U plus a MECHANISM-FAITHFUL axis (5 = structurally principled
for that electronic Hamiltonian; 1 = curve-fit coincidence). Mech≤2 ⇒ flagged
"exponent-coincidental risk" and USEFULNESS capped at 2.

**Project lesson applied ruthlessly:** "a power-law exponent / energy-curve match is not
evidence of a mechanism" (HYP-014 REFUTED, HYP-017 closeout). A tensor network that
reproduces a dissociation curve or correlation-energy number is NOT thereby the right
ansatz for that Hamiltonian. Every candidate must state why the TN *structure* is
faithful to the chemical Hamiltonian's entanglement geometry.

**Prior-art posture:** QC-DMRG / tensor-network chemistry (White, Chan, Legeza,
Reiher, Wouters, Schollwöck) is a LARGE mature field. MERA-for-chemistry specifically
is much less developed. Novelty is judged against that boundary, not against TN-chem
in general.

---

## Ranked table

| Rank | Bridge | Project asset | QC problem | N | B | U | Mech | Product (N·B·U) |
|---|---|---|---|---|---|---|---|---|
| 1 | **RG-flow criticality fingerprint**: use the project's *entanglement-scaling-under-coarse-graining* tooling (not entropy magnitude) to classify a molecule's static-correlation **universality class** (gapped / c=1 Luttinger / c=½ Ising-like) → routes method choice (CCSD vs DMRG vs CASPT2) | chi=3 MERA scale-invariance machinery + central-charge / scaling-dimension extraction validated on 2D Ising CFT (HYP-006/008) | When is a π-system *critical-like* (polyacene/graphene-nanoribbon/Mott-edge) vs merely multireference — and which is the right method | 4 | 3 | 4 | 4 | **48** |
| 2 | **Scale-resolved disentangler correlation spectroscopy**: MERA disentanglers tag *which length scale* electron correlation lives at; feed the layer at which correlation stops being removable as the embedding/active-space boundary | MERA disentangler + causal-cone code; entanglement-renormalization layer structure | Active-space / embedding-fragment boundary selection for extended conjugated systems where the cut is length-scale-ambiguous | 4 | 2 | 3 | 4 | **24** |
| 3 | **Logarithmic causal cone for long-range π correlation**: fermionic-MERA on the delocalized π manifold of polyacene/GNR where MPS area-law forces exponential bond-dim growth | chi=3 MERA, log-depth causal cone, scale-invariant layer (the literal validated artifact) | Correlation energy of long, near-metallic conjugated chains where QC-DMRG bond dimension explodes | 3 | 2 | 4 | 4 | **24** |
| 4 | **Geometric/holographic bond-structure chooser**: use the molecular orbital-entanglement graph's *hyperbolic embeddability* to decide MPS vs TTN vs MERA before any solve | holographic/geometric entanglement picture; AdS-like bulk geometry intuition from the paper | A-priori tensor-network ansatz selection for an arbitrary molecular graph | 3 | 3 | 3 | 2 | **27** (capped U≤2 ⇒ **18**) |
| 5 | **CFT-OPE structured cumulant estimator** for connected orbital correlators in near-critical chains | connected-correlator extraction + CFT operator-product intuition (epsilon/sigma channel work) | Decomposing molecular static correlation into scaling-operator channels | 2 | 2 | 3 | 2 | **12** (capped U≤2 ⇒ **8**) |
| 6 | Plain "entanglement entropy ⇒ multireference diagnostic" | single-site entropy | strong-correlation detection | 1 | 5 | 1 | 3 | **5** (already standard: autoCAS/Zs(1)) |

---

## Editorial — top 5

### Rank 1 — RG-flow criticality fingerprint (N4·B3·U4, Mech 4 → 48)

**(1) Project asset.** Not "MERA exists" — the *specific validated tooling*: the chi=3
MERA + scale-invariant-layer + central-charge / scaling-dimension extraction that the
project demonstrated reproduces the 2D Ising CFT (c=½, the alpha≈4 stress-tensor and
T=(pi/2)l_AdS results). The load-bearing artifact is the **entanglement-flow-under-
coarse-graining** pipeline, not entropy magnitude.

**(2) QC problem.** Multireference diagnostics today (Zs(1), autoCAS single-orbital
entropy, T1/D1, M-diagnostic) answer a *binary*: is this molecule strongly correlated?
They do **not** answer the question that actually determines method choice for extended
π-systems: *what universality class is the static correlation?* A finite polyacene that
is flowing toward a gapless c=1/c=½ critical point (the long-acene / GNR / Mott-edge
regime) needs a fundamentally different ansatz (MERA-like, log-entanglement) than a
molecule with the same *magnitude* of single-orbital entropy that is gapped (a few
near-degenerate frontier orbitals — DMRG/CASPT2 with modest bond dim suffices). Entropy
magnitude cannot separate these; **how the entanglement flows under blocking** can.

**(3) Emergent capability.** A *universality-class label* for a molecule: run the
orbital-ordered correlation state through the project's coarse-graining layers, measure
the block-entropy scaling S(L) and its RG flow, and classify gapped (area-law,
S→const) vs critical (S ~ (c/3)log L) and extract an effective central charge / leading
scaling dimension. Output is a routing decision: "this acene has crossed into the
c≈1-like regime at n=9 rings — single-reference and even moderate-bond-dim DMRG will
mis-converge; deploy entanglement-renormalization / large-chi." That is information
**no existing chemistry diagnostic produces**.

**(4) Why mechanism-faithful (Mech 4).** This is the crux and the reason it clears the
project's own trap. The faithfulness is *not* "it fits a log curve." Long polyacene /
poly(p-phenylene) / metallic GNR π-systems are genuinely described, in the appropriate
limit, by a 1D critical effective theory (Hubbard/PPP chains at half filling; the
acene π-band is a textbook quasi-1D correlated ladder — confirmed in the strong-π-
correlation polyacene literature). The MERA causal-cone *is* the real-space RG of
exactly that class of 1D critical Hamiltonian — it was built to be the fixed-point
structure of a scale-invariant 1D system, which is what a critical π-chain *is*. So the
tensor-network structure is matched to the chemistry's actual low-energy effective
Hamiltonian, not retrofitted to a number. Capped at 4 not 5 because the mapping
"acene π-manifold → clean 1D CFT" holds only in the long-chain limit and is
contaminated by sigma-framework and 2D-rung coupling at finite size — the diagnostic
must be honest that it measures *flow toward* a class, with a finite-size caveat, not a
clean fixed point. (If it were sold as "we measured c=½ therefore Ising" on a 6-ring
acene, that would be the HYP-014 trap; the deliverable is explicitly the *flow*, with
the finite-size deviation reported as the uncertainty, which is mechanistically the
correct thing to report.)

**(5) Closest prior art.** *Mature and must be distinguished from:* autoCAS / Stein–
Reiher orbital-entropy active-space selection (jz301319v; arXiv:1609.02617 Zs(1);
arXiv:2501.18263 review); finite-entanglement-scaling central-charge extraction in DMRG
(standard, ITensor-level). *What is genuinely new:* every existing chemistry tool uses
entropy *magnitude at fixed scale* as a binary multireference flag. None performs the
**RG flow of the entanglement under explicit coarse-graining to assign a universality
class and route the method**. The central-charge-from-DMRG literature extracts c for
*model spin chains*, not as a *per-molecule method-selection diagnostic on an ab initio
orbital-correlation state*. The combination — project's validated RG-flow extractor +
ab initio orbital-entanglement input → class label → method router — has no located
precedent.

**(6) Hardest obstacle.** Finite molecules are *not* at a fixed point; the signal is a
*flow*, and short acenes may not have flowed far enough to classify cleanly. Mitigation
is built into the design: report the flow trajectory and its finite-size deviation as
the diagnostic's uncertainty rather than forcing a label — but this caps confidence on
small systems and means the method is only sharp for the *extended* systems (which,
fortunately, are exactly the ones existing diagnostics handle worst).

**(7) Usable result.** A short methods paper / open tool: feed an autoCAS-style
partially-converged orbital-correlation matrix for an acene series (n=2…12) into the
project's coarse-graining pipeline; output S(L) flow + extracted effective c; show the
crossover ring count where the class changes and that it predicts the documented
single-reference-method breakdown in the polyacene literature. Pure classical compute,
reuses existing project code, no hardware, no money.

### Rank 2 — Scale-resolved disentangler correlation spectroscopy (N4·B2·U3, Mech 4 → 24)

**(1) Asset.** MERA disentangler tensors + causal-cone code. **(2) QC problem.** Where
to put the active-space / embedding-fragment boundary in an extended conjugated system
when the cut is length-scale-ambiguous. **(3) Capability.** Disentanglers at each MERA
layer remove correlation *at a definite length scale*; the layer at which a given
orbital block stops being disentanglable is a principled, scale-resolved fragment
boundary — a "correlation length spectrum" per orbital region. **(4) Mech-faithful
(4).** This is structurally what disentanglers *are* (Vidal: coarse-graining must be
preceded by removal of short-range entanglement); applying them to a fermionic orbital
state inherits that meaning faithfully — it is not a curve fit, it is the actual
operational definition of "short-range vs long-range correlation" applied to the
chemical state. **(5) Prior art.** Generalized-DMET 2025 (arXiv:2503.09881) *already*
uses a "disentanglement criterion" for bath construction — this is the dangerous
overlap. *New slice:* DMET's is an abstract bath-optimization disentanglement; using
*literal scale-resolved MERA disentangler layers to produce a correlation-length-
resolved fragment boundary* is distinct, but the novelty is narrower than Rank 1 and
must be framed against 2503.09881 explicitly. **(6) Obstacle.** Fermionic MERA
disentangler optimization for ab initio orbitals is heavy, poorly tooled, and the
project has no fermionic-MERA code (only spin chi=3) — buildability 2. **(7) Result.**
A proof-of-concept on a single small polyene showing the disentangler-layer fragment
boundary differs from (and is more principled than) a distance cutoff.

### Rank 3 — Logarithmic causal cone for long-range π correlation (N3·B2·U4, Mech 4 → 24)

**(1) Asset.** The literal validated chi=3 MERA with log-depth causal cone and scale-
invariant layer. **(2) QC problem.** Correlation energy of long near-metallic
conjugated chains (polyacene, armchair-edge GNR) where QC-DMRG bond dimension grows
because the state's entanglement violates the 1D area law (logarithmic) — exactly
MERA's home turf. **(3) Capability.** A tensor-network energy method whose cost scales
log, not exponentially, in the bond dimension demanded by the critical entanglement.
**(4) Mech-faithful (4).** Faithful because the *reason* DMRG struggles here (log area-
law violation from criticality) is the *exact reason* MERA was constructed; this is a
structural match between the failure mode and the ansatz, not a number match. **(5)
Prior art.** This is the most contested: Szalay/Legeza review *explicitly speculates*
MERA for coarse-grained entangled-orbital subgroups in polyacene, but it was never
delivered; Trotterized-MERA-VQE (Quantum 2025, q-2025-02-11-1631) is spin-chain, not ab
initio molecular. Genuinely new = *delivering* fermionic ab initio MERA energies for an
acene series. **(6) Obstacle.** Fermionic MERA for ab initio Hamiltonians (long-range
two-electron integrals, fermion signs through disentanglers) is a known very hard,
largely-unsolved problem — this is why nobody has shipped it; buildability 2 and
honestly maybe 1 for full ab initio. **(7) Result.** Even a model-PPP-Hamiltonian acene
demonstration (not full ab initio) showing MERA bond-dim stays bounded where DMRG
blows up would be a publishable proof-of-principle.

### Rank 4 — Geometric/holographic bond-structure chooser (N3·B3·U3, Mech 2 → capped 18)

**(1) Asset.** The paper's holographic/geometric entanglement (AdS-like bulk) picture.
**(2) Problem.** Pick MPS vs TTN vs MERA for an arbitrary molecular orbital graph
*before* solving. **(3) Capability.** Test whether the orbital mutual-information graph
embeds with low distortion into hyperbolic space → prescribe MERA; into a line → MPS.
**(4) Mech-faithful — only 2, FLAGGED "exponent-coincidental risk."** The link
"hyperbolic-embeddable ⇒ MERA-appropriate" is *suggestive analogy*, not a theorem about
the molecular Hamiltonian; a graph can be hyperbolic-embeddable for reasons unrelated to
the entanglement structure the ansatz needs to capture. This is precisely the
project's trap shape (geometry matches → assume mechanism). USEFULNESS capped at 2.
**(5) Prior art.** Legeza orbital-ordering / TTN-topology optimization already chooses
network structure from the mutual-information graph — this is largely *anticipated*; the
hyperbolic-embedding framing adds little mechanistically. **(6) Obstacle.** No proof the
embedding distortion correlates with ansatz error. **(7) Result.** At best a heuristic
correlation study, explicitly not a principled selector.

### Rank 5 — CFT-OPE structured cumulant estimator (N2·B2·U3, Mech 2 → capped 8)

Decompose molecular connected orbital correlators into CFT scaling-operator channels
using the project's epsilon/sigma-channel cumulant tooling. **Mech 2, FLAGGED.** A
molecule is not a CFT except in a fine-tuned limit; assigning "scaling-operator
channels" to a generic molecular correlator imposes a structure the Hamiltonian does
not have — channel labels would be coincidental bookkeeping, not mechanism. This is the
HYP-014 failure mode wearing a chemistry hat. Capped USEFULNESS 2, low rank, recorded
so it is not re-proposed.

---

## Prior-art log (URLs / arXiv IDs)

**Mature — sets the novelty floor (must be distinguished from, not novel):**
- Orbital-entanglement multireference diagnostic Zs(1): arXiv:1609.02617;
  pubs.acs.org/doi/10.1021/jz301319v (Boguslawski/Tecmer/Legeza/Reiher).
- autoCAS entanglement-based automated active-space selection (Stein–Reiher) — described
  in review arXiv:2501.18263 "Tensor network state methods and quantum information
  theory for strongly correlated molecular systems".
- TTN topology / orbital-ordering optimization from mutual-information graph (Legeza):
  pubs.acs.org/doi/10.1021/ct501187j (variable-tensor-order TTN); Szalay et al. review
  onlinelibrary.wiley.com/doi/full/10.1002/qua.24898.
- Finite-entanglement-scaling central charge from DMRG: standard
  (researchgate finite-entanglement-scaling 1D QCP; ITensor discourse t/252).
- QC-DMRG maturity: pubs.aip.org/aip/jcp/article/152/4/040903 (DMRG-in-chemistry review).

**Closest moving targets (the dangerous overlaps, must frame against):**
- Generalized DMET with disentanglement-criterion bath construction (2025):
  arXiv:2503.09881 — directly adjacent to Rank 2.
- Trotterized-MERA VQE, polynomial quantum advantage for critical *spin chains*:
  quantum-journal.org/papers/q-2025-02-11-1631 ; arXiv:2303.08910 — spin-chain, NOT ab
  initio molecular; adjacent to Rank 3.
- MERA-for-polyacene is *speculated but undelivered* in Szalay/Legeza review
  (qua.24898) — the gap Rank 1/Rank 3 target.

**Chemistry context supporting Mech-faithful claim (acene π = quasi-1D critical):**
- Strong π-correlation / near-metallic polyacene: sciencedirect S2667056922000025
  ("Manifestations of strong electron correlation in polyacene").
- Multireference-diagnostic landscape (T1/D1/M-diagnostic baselines):
  pmc.ncbi.nlm.nih.gov/articles/PMC10809408 (all-purpose electron-correlation measure).

**Verdict on the framing.** The single defensible novel slice is **Rank 1**: the
project's *RG-flow-of-entanglement-under-coarse-graining* extractor (validated on Ising
CFT) repurposed as a *per-molecule universality-class router* — distinct from every
mature entropy-magnitude multireference diagnostic, and mechanism-faithful because the
MERA causal cone is the literal RG of the quasi-1D critical Hamiltonian that long
π-systems actually realize. Ranks 2–3 are mechanism-faithful but buildability-limited
(project has no fermionic MERA). Ranks 4–5 are flagged exponent-coincidental and
recorded so they are not re-proposed.
