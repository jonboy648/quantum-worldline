# Agreement Without Discrimination: State Functionals, Surplus Structure, and the Operational Content of Emergent Geometry in Tensor Networks

**Jon Cackler**, independent researcher, Ames, Iowa

Preprint, version 1, 19 October 2026.

## Abstract

Tensor networks such as the multiscale entanglement renormalization ansatz (MERA) are often described as
discrete pictures of a spacetime that emerges from boundary quantum states. This paper asks what evidence
could separate two readings of that description: that the network's geometry is an efficient
bookkeeping of a critical state (Representation), or that it carries operational content not already
fixed by the state and its conformal data (Operational Geometry). We argue that a large class of
observables cannot bear on the question. A quantity fixed by the boundary state alone takes the same
value in every faithful representation of that state, so its agreement with a geometric formula cannot
favour either reading, however precise the agreement. Content for the geometric reading can live only in
quantities that are invariant under the network's gauge freedom yet sensitive to its organization, and
these two requirements pull against each other. We ground the argument in a documented case: a research
program whose central "geometric" results were, on audit, functionals of exactly computed boundary
states, obtained without the network, and whose headline number was retracted as an estimator artifact. Two
diagnostics from the program's own governance, counterfactual novelty and an independence ledger, show
what went wrong and what they caught. Finally we report a pre-registered test of the one gauge-invariant,
network-sensitive observable the program built, bulk operator recovery. At the accessible bond
dimension, the onset of recovery loss in the optimized network could not be told apart from that in
random networks on the same graph.

**Keywords:** emergent spacetime; tensor networks; MERA; surplus structure; gauge invariance;
severe testing; robustness; pre-registration.

## 1. Introduction

The multiscale entanglement renormalization ansatz (MERA) represents ground states of critical
one-dimensional quantum systems as hierarchical networks of small tensors (Vidal 2007). Because the
network has an extra direction that tracks length scale, and because its graph resembles a discretized
hyperbolic plane, it has been read as a discrete realization of holography, with the network itself
playing the part of a bulk spacetime (Swingle 2012). Tensor networks have since become a standard toy
setting for the idea that geometry is in some sense built out of entanglement. Bulk locality has been
connected to quantum error correction (Almheiri, Dong and Harlow 2015), and holographic codes built as
tensor networks reproduce features of bulk reconstruction (Pastawski et al. 2015). Random tensor
networks obey the Ryu-Takayanagi formula for boundary entanglement at large bond dimension (Hayden et
al. 2016). And MERA itself has been given more than one geometric reading: a de Sitter causal structure
offered as an independent justification of its link to hyperbolic geometry (Beny 2013), and a rigorous
light-sheet or light-cone geometry offered in place of the hyperbolic plane (Milsted and Vidal 2018).

This paper asks a narrower question. We call it the trunk question, because a research program adopted
it as the question all its other work should serve:

> What mathematical and operational content, if any, does emergent geometry add beyond an accurate CFT
> tensor-network representation? (Director 2026, §29)

The question contrasts two hypotheses, which the program's governing standard states as follows.
**Hypothesis A** (efficient representation): "MERA is an efficient hierarchical representation of
critical quantum states. Apparent geometry is descriptive or computational, but adds no independently
predictive physical content beyond the underlying CFT and tensor-network structure." **Hypothesis B**
(operational emergent geometry): "MERA contains geometric structure that supports predictions,
reconstruction behavior, locality properties, dynamical relations, or invariants not automatically fixed
by ordinary CFT data alone" (Director 2026, §4). The standard adds that a result supporting either
hypothesis would be meaningful, as would "a proof that the distinction cannot be operationally made
within the proposed framework", and that the one unacceptable outcome is "to avoid the distinction while
continuing to relabel known CFT quantities as geometric discoveries".

Our evidence comes from a program that set out to support B and did not. Between March and August
2026 the Quantum Worldline program, the author's own, carried out with a team of AI research agents,
produced a series of "geometric" results for the critical
transverse-field Ising chain and related minimal models: a force exponent between two probes, a
transport time, a chord distance. An internal audit later found that 21 of the 34 claims involving a
calculation could not have come out otherwise, that no result discriminated A from B, and that the
headline number was a fitting artifact (Audit 2026, §1). The number was then publicly retracted
(Errata 2026, E6; Cackler 2026a). The standard quoted above was adopted on 11 August 2026, after those
results, and its first assignment was the audit of them (Director 2026, §38). We treat this record as a
case study. Its value is not that it settles
the trunk question, which it does not, but that it shows in detail which kinds of test cannot bear on
the question at all, and why.

The argument runs as follows. Section 2 places the question in the literature on emergence and on
tensor-network holography. Section 3 distinguishes state functionals, quantities fixed by the
represented boundary state alone, from network-sensitive observables, and argues that agreement between
a state functional and a geometric formula cannot discriminate A from B. Section 4 turns this into a
dilemma: a candidate observable for B must be invariant under the network's gauge freedom, yet sensitive
to the network's organization, and these requirements pull against each other. Sections 5 and 6 present
two diagnostics the program applied to itself, counterfactual novelty and an independence ledger, and
show what each caught, including the retraction. Section 7 describes three routes that ended or
narrowed in ways that mark the boundaries of the question. Section 8 reports a pre-registered test of the one
network-sensitive, gauge-invariant observable the program built. It came out as the registration
expected: at the accessible bond dimension, the onset of recovery loss in the optimized network could
not be told apart from that in random networks on the same graph. Section 9 asks what would make tensor-network geometry more than a
visualization.

Three limits should be stated at the outset. The setting is 1+1-dimensional lattice conformal field
theory with small-bond-dimension MERA; nothing here is a claim about AdS/CFT in general or about quantum
gravity. The evidence is one program's record, audited by agents of the same program, so its internal
agreements are themselves same-origin sources in the sense of Section 6; we flag the places where an
independent check exists. And the central argument of Section 3 is simple. It combines two familiar
points, that tensor-network representations of a state are not unique (Molnar et al. 2018; Singh 2018)
and that an observation predicted equally by two hypotheses is evidence for neither (Hacking 1965;
Royall 1997), and Ney (2021) has made a closely related argument about holographic entanglement-distance
relations. We present it as an application of those points to a specific scientific practice.
What the paper adds is that application, documented in detail, and in Section 4 an explicit dilemma
whose horns have each been recognized in the literature.

## 2. Background: emergence, duality, and representation

### 2.1 Emergence and duality

Philosophical work on emergent spacetime has largely been organized around two questions: what
emergence is, and whether gauge/gravity duality supports it. On the first, Butterfield takes "emergence
as behaviour that is novel and robust relative to some comparison class" and argues that emergence so
understood "is compatible with reduction" (Butterfield 2011, §§1.1-1.2). Crowther develops a conception
of emergence suited to effective field theories and applies it to approaches to quantum gravity
(Crowther 2016), and separately argues that reduction is "a special case of correspondence" and forms part of
the definition of quantum gravity, while emergence "is not part of the definition of QG" (Crowther 2018). Huggett and Wüthrich (2013) raise the worry that a theory without fundamental
spacetime may be "empirically incoherent", in that its truth would undermine the empirical justification
for believing it, and sketch how the worry can be answered.

On the second question, the literature is cautious about reading AdS/CFT as a case of emergence. Teh
(2013) finds it "difficult to find compelling arguments for the emergence of full quantum gravity from
gauge theory via AdS/CFT, i.e. for the boundary theory's being metaphysically more fundamental than the
bulk theory". Rickles (2013) argues that the emergence in question is "relatively weak" and that "at the
core of AdS/CFT is an issue of representation and redundancy in representation". Dieks, van Dongen and de
Haro (2015, §3.3.2) read the two sides of an exact duality as "different representations of one and the
same physical theory", so that there is "no emergence of one side of the duality from the other". De
Haro (2017) and De Haro, Mayerson and Butterfield (2016) treat duality and emergence as close but mutually
exclusive relations, with emergence requiring the duality to be approximate.

A smaller literature asks directly whether geometry can be derived from entanglement. Cao, Carroll and
Michalakis (2017) "examine how to construct a spatial manifold and its geometry from the entanglement
structure of an abstract quantum state in Hilbert space". Jaksland (2021) offers "entanglement as an
alternative world-making relation", while noting that his argument "is not demonstrating how distance
can be recovered from entanglement". More recently Jaksland (2025) argues that results grouped as
evidence for spacetime from entanglement "are not about the same spatiotemporal aspects" and that "more
than entanglement is needed to furnish the emergence basis". On the physics side, Li (2026) shows that the
state-dependent entropy remainders of a holographic code "need not be the extremal lengths of any one bulk
metric": a vector "may satisfy every universal holographic entropy inequality and still fail" a
fixed-background realization test. Earlier, Ney (2021) asked how far the case for the entanglement-distance link is
evidence that spacetime is nonfundamental, and argued that the results support only the weaker
conclusion that entanglement facts are constrained by distance facts. Ney's and Jaksland's are the
nearest prior applications of evidential scrutiny to emergent-geometry claims that the searches for this
paper found; neither discusses tensor networks.

### 2.2 Tensor networks and their geometric readings

The physics on which this paper draws starts from the MERA ansatz itself, a network of isometric tensors
with an extra direction that tracks length scale (Vidal 2007). Vidal's construction is a variational
method; the geometric reading came later. Swingle (2012) proposed that the network's structure defines
a higher-dimensional geometry, so that "the state at a quantum critical point gives a discrete version of
anti de Sitter space". The reading has since been elaborated, constrained and contested. Beny (2013)
recasts MERA as a causality constraint with the causal structure of de Sitter space, and presents this as
"an independent justification of the connection between MERA and hyperbolic geometry". Milsted and Vidal
(2018) give MERA "a rigorous interpretation as a two-dimensional geometry, namely a light sheet
(respectively, a light cone)", and conclude that it "describes neither the hyperbolic plane nor de Sitter
spacetime". Bao et al. (2015) argue that "the MERA lattice can only describe physics on length scales
larger than the AdS radius" and that no conventional MERA parameters "completely reproduce bulk physics
even on super-AdS scales".

A second line connects tensor networks to quantum error correction. Almheiri, Dong and Harlow (2015)
connect "the emergence of bulk locality in AdS/CFT and the theory of quantum error correction";
Pastawski et al. (2015) build exactly solvable holographic codes as tensor networks; Hayden et al. (2016)
show that random tensor networks obey the Ryu-Takayanagi formula at large bond dimension; and Kim and
Kastoryano (2017) show that for critical systems "an approximate variant of holographic quantum error
correcting code emerges at low energy". Most recently, Sahu et al. (2026) derive subalgebras for
minimal-cut-type regions in networks assumed to be exactly isometric, and argue for them in random
networks at large bond dimension.

### 2.3 Where this paper sits

The philosophical literature already reads exact duals as different representations of one theory, and
already puts redundancy of representation at the centre of AdS/CFT. Tensor networks sharpen that point
rather than break from it. A tensor network is not a dual theory. It is one of many non-unique,
approximate representations of a single state of a single theory, and the same state has representations
(a matrix product state, an exact vector) with no geometric reading at all. So the live contrast in the
tensor-network case is between properties of the represented state and properties of the
representation. The question is not whether the bulk is emergent from the boundary, or fundamental, but
whether anything about the network is physical beyond the state it represents. That question is also
narrower than the empirical-coherence worry: the boundary theory and its spacetime are taken for
granted throughout, and only the bulk is in question.

## 3. State functionals and network-sensitive observables

### 3.1 Definitions

A tensor network $N$ consists of a graph $G$ and an assignment of tensors to its vertices. Contracting
it yields a boundary state $|\psi_N\rangle$. Call $N$ a *faithful representation* of a target state
$|\psi\rangle$ to accuracy $\epsilon$ if $\| |\psi_N\rangle - |\psi\rangle \| \le \epsilon$. Call a
real-valued quantity $Q$ a *state functional* if it depends on $N$ only through
$\rho_N = |\psi_N\rangle\langle\psi_N|$ and is continuous in $\rho_N$. Correlation functions of
boundary operators, entanglement entropies of boundary regions, energy profiles and spectra of reduced
density matrices are state functionals in this sense. So is any quantity computed from an exactly
diagonalized ground state, where no network is involved at all.

The observation that drives the paper is immediate. If $N$ and $N'$ both represent $|\psi\rangle$
faithfully, then $Q(\rho_N)$ and $Q(\rho_{N'})$ both approximate $Q(\rho)$, to within a bound set by
$\epsilon$ and the continuity of $Q$. A MERA, a matrix product state and an exact state vector, if all
are accurate, return the same value of every state functional.

### 3.2 Why agreement cannot discriminate

Suppose a geometric reading of the network yields a formula $g$ for some state functional $Q$, and
suppose $Q(\rho_N)$ agrees with $g$ to high precision. On Hypothesis B the agreement is what one expects
if the network's geometry is physical. On Hypothesis A it is equally expected, provided the network is
an accurate representation and the conformal field theory fixes $Q$: then $Q(\rho_N) \approx Q(\rho)$,
and $g$ is a re-expression of CFT data in geometric vocabulary. Both hypotheses predict the agreement
with the same probability, so observing it cannot move the balance between them, however precise it
is. What the agreement measures is *ansatz fidelity*: how well the network represents $\rho$.

This is the law of likelihood at work: an observation supports one hypothesis over another only if it is
more probable under the one than under the other (Royall 1997, p. 3, after Hacking 1965). The premise is
already familiar in the tensor-network literature. Of two MERAs related by a gauge transformation, Singh
writes that they "are an equivalent representation of the state since the expectation value of any
observable is equal in both representations" (Singh 2018, §VI); more generally, "different sets of
tensors may generate the very same state" (Molnar et al. 2018). The argument form also appears in the
philosophy of dualities, where duals that "are indistinguishable with respect to all physical quantities
represented by observables" cannot settle a geometric property on which they disagree (Huggett 2017). Closest in subject matter is
Ney (2021), who argues that the entanglement-distance correspondences of holography, including the
agreement between the Ryu-Takayanagi formula and the Calabrese-Cardy entanglement entropy, are "compatible
with the holding of several possible inter-theoretic relationships" between entanglement facts and metric
facts (p. 88): such results "certainly confirm an entanglement-distance link" but "cannot support Option
(1) over its three rivals" (p. 94), Option (1) being that metric facts emerge from entanglement facts.
Our argument has the same form but compares a different pair of hypotheses: not which of two sets of
physical facts is more fundamental, but whether a representation's internal organization carries content
beyond the state it represents. Ney also argues that the physics favours the reverse order, with distance
constraining entanglement (pp. 96-98); nothing here depends on that further claim.

The argument has a limit that should be stated. It does not touch the separate claim that MERA's
efficiency on critical states (its logarithmic depth and small bond dimension at high accuracy) is itself
evidence for a geometric reading, as the best explanation of that efficiency. Efficiency is a property of
the representation class relative to the state, not a state functional. Arguments from efficiency have
to be assessed on their own terms. We note only that the MERA's originators trace such structural
properties to the network: certain properties of the represented states "are preconditioned by the
geometry of the tensor network and are therefore largely independent of the choice of variational
parameters" (Evenbly and Vidal 2011).

A corollary concerns controls. The natural way to test whether an agreement is due to the network's
geometry is to swap the representation: replace the MERA by a non-geometric ansatz matched on ordinary
observables, and see whether the agreement survives. For a state functional, the result of this control
is fixed in advance. If both representations are accurate, both reproduce $Q$. A review inside the
program reached exactly this verdict on a proposed matched-control experiment: because the observables
in question were state functionals, "state functionals cannot separate representations. Outcome count 1,
claim level 1" (Review 2026, "Challenges not survived").

### 3.3 Surplus structure

The point can be put in the vocabulary of surplus structure: formal structure in a representation to
which nothing physical corresponds. The term is credited to Redhead (1975), as cited in French and Rickles
(2003), and it is commonly linked to gauge freedom: surplus structure "frequently
points to the existence of 'gauge freedom'" (French and Rickles 2003, arXiv version, p. 2). Rickles (2013) has put
"representation and redundancy in representation" at the core of AdS/CFT itself. A tensor network has a
large gauge freedom.
Inserting $U U^{-1}$ on any internal bond, and absorbing $U$ and $U^{-1}$ into the neighbouring tensors,
changes the individual tensors without changing $|\psi_N\rangle$. For a MERA, whose tensors are
constrained to be isometries, the freedom that preserves the constraint is unitary, $U^{-1} = U^\dagger$.
The tensors are therefore surplus
relative to the boundary state. More than that, the whole internal organization of the network (which
graph, which bond dimensions, which tensors) is surplus relative to $\rho$ unless some quantity that
counts as physical depends on it. Hypothesis B is, in these terms, the claim that some of that
organization is not surplus. State functionals cannot bear on the claim, because by definition they do
not depend on the organization.

### 3.4 Computed through the network is not dependent on the network

One distinction prevents a confusion. Some quantities are computed *through* a network without
*depending* on it. The scaling dimensions read off the spectrum of a MERA's scaling superoperator are
computed from the network's tensors, and the spectrum is gauge-invariant. But for a faithful network
those dimensions are the scaling dimensions of the conformal field theory: they are fixed by the
represented state and its CFT data, not by the network's organization. A *network-sensitive* observable,
in our sense, is one whose value can differ between two faithful representations of the same state that
are not related by a gauge transformation.

### 3.5 The case

The program's central "geometric" results were state functionals, and in all three cases below no
network took part in the measurement at all.

- **Transport time.** The program's flagship parameter-free comparison was a transport time measured on
  the boundary spin chain alone. The driver builds the MERA tensors, checks their unitarity, and then
  prints "Skipping full MERA bulk computation (complex to implement correctly)" (Transport driver
  2026, line 347). The audit described the measured object as "a lattice light-cone crossing time on a
  boundary spin chain" (Audit 2026, §7.1).
- **Force exponent.** The headline exponent was fitted to an interaction-energy profile on an exactly
  diagonalized 24-site chain: "No MERA is used in this measurement" (Audit 2026, §3).
- **Chord distance.** A distance built from the spin-spin correlator of an exactly diagonalized
  16-site chain (the program's "Synge distance") inherited that correlator's decay exponent, 0.243,
  close to twice the spin operator's scaling dimension ($2\Delta_\sigma = 0.25$), and did not track the
  force exponent (Audit 2026, §7.1 item 4; SIM-2026-031). This is what one expects of a re-expression of
  boundary data.

The audit's skeptic summarized the pattern: "Everything measured is a state property recoverable from
the boundary; everything network-specific ($l_{AdS}$, $d_{geo}$) is asserted from the architecture and
multiplied in" (Audit 2026, §7.1 item 5). Where a small-bond-dimension MERA did reproduce the exact
results, the agreement measured how good the MERA was as an approximation to the exact state. A
later review located the program's failure to produce a discriminating result in the same place: the
experiment was "blocked by observable design, not scale and not incentives" (Review 2026, key finding 4).

## 4. A dilemma for the geometric reading

### 4.1 Two requirements that pull apart

Section 3 gives a necessary condition on any observable that could support Hypothesis B: its value must
be able to differ between faithful representations of the same state. Call this *network sensitivity*.
A second condition is necessary on a widely shared assumption: that quantities which vary under a
theory's symmetries are not physically real. On that assumption, a quantity that changes under the
network's gauge transformations (Section 3.3) is a property of the chosen gauge, surplus in the plainest
sense, and the observable must also be *gauge-invariant*. The assumption is contested in general. Jacobs
(2021) argues that this "Invariance Principle" is orthogonal to the view that symmetry-related models
represent the same state of affairs, and Rovelli (2014) that gauge "is more than mathematical
redundancy"; Nguyen, Teh and Wells (2020) and Bradley and Weatherall (2020) distinguish senses of
"surplus structure". We adopt the assumption because both sides of the case adopted it, and because a
defender of B who rejected it would have to locate geometric content in the choice of gauge itself, a
position nothing in the case supports.

The two requirements pull in opposite directions. Gauge invariance pushes an observable toward the
boundary state, the most obvious gauge-invariant object a network defines. Network sensitivity pushes it
away. Whatever content Hypothesis B has must live in the band between them: quantities that are joint
functionals of the state and the network, invariant under gauge transformations, but not fixed by the
state alone.

Each part of this has been recognized before. Singh (2018, §VI) notes that bulk states built from
gauge-equivalent MERAs "are generally different", an "ambiguity ... that arises due to the 'gauge
freedom' inherent in tensor network representations", and Molina-Vilaplana (2015) checks a
network-derived metric for gauge invariance. Qi (2013) defines a bulk geometry "determined by the
boundary state and the mapping", a joint functional in our sense. And the worry that network-sensitive
quantities may belong to the ansatz rather than to the state is stated by the MERA's originators
(Evenbly and Vidal 2011, quoted in Section 3.2) and by Hyatt, Garrison and Bauer (2017), who introduce a method of extracting geometry from a state
by noting that "conventionally, the structure of the network - and hence the geometry - is largely fixed
a priori by the choice of tensor network ansatz". What we add is
the combination: the two requirements stated together as a dilemma about where evidence for B could
live.

There is a further squeeze inside the band. A quantity that is gauge-invariant and network-sensitive may
still vary with incidental choices of representation, such as bond dimension or branching ratio. Such a
quantity is a property of the particular network rather than of anything the network might be a picture
of. And a quantity invariant across *every* faithful representation is a state functional again. What
Hypothesis B needs is narrower: a quantity robust across the incidental choices within a class of
networks (hierarchical, multiscale ones), yet different between that class and other representations of
the same state, and not fixed by data that Hypothesis A already grants.

### 4.2 The advocate's sharpening

The program's audit assigned an adversary to make the strongest case for B, and that adversary arrived
at the same band from the other direction. Because Hypothesis A already grants "the CFT and
tensor-network structure", an observable that is a functional of the state alone belongs to A, and so
does one that is a functional of the network alone; B has content in exactly one band, "joint functionals
of (state, network)". The advocate's operational version, B★, requires three clauses together: invariance
under gauge, architecture and bond dimension; non-derivability from network parameters (bond
dimension, branching, cone width) or from CFT data (central charge, scaling dimensions, OPE
coefficients); and a parameter-free out-of-sample prediction. "All three clauses are required, and no
observable currently in the project satisfies even the first two" (Audit 2026, §7.2). That the
assessment came from the side assigned to defend B is part of its weight.

B★'s invariance clause should be read in the way 4.1 suggests: as robustness across discretization
choices within the class of networks whose geometry is in question, not as invariance across all
representations, which would make the quantity a state functional and hand it to A.

### 4.3 Two cases at the edges of the band

The program's record contains quantities on both sides of the band, and none inside it until Section 8.

**A network-specific quantity that fails robustness.** The program's "AdS radius" was a definition,
$l_{AdS} = 1/\ln\chi$, taken from the architecture. Its geometric claims therefore used different radii
for what was described as one geometry: 1.4427 for a $\chi = 2$ network (transport), 0.9102 for
$\chi = 3$ (force) and 0.4024 for $\chi = 12$ (a Potts-model network) (Audit 2026, §7.2 item 3). In the
skeptic's words, "A quantity that changes 37% when you *improve* the representation of the identical
state is, by §34, a property of the representation" (Audit 2026, §7.1 item 2, citing Director 2026,
§34).

**A gauge-invariant quantity that fails non-derivability.** The program extracted the operator product
coefficient $C_{\sigma\sigma\epsilon}$ of the Ising model from optimized networks with a
symmetry-respecting pipeline: a mean of 0.5075 over eight optimizations at $\chi = 6$, and 0.5069 over
four at $\chi = 8$ (SIM-2026-061); the audit notes that a better-converged $\chi = 12$ rung came out
5.6% low (Audit 2026, §5.2). The quantity is gauge-invariant, and a review inside the program cited it,
correctly, as "a gauge-invariant network number that scaling dimensions do not fix" (Review 2026). But
it is fixed by CFT data: $C_{\sigma\sigma\epsilon} = 1/2$ exactly in the Ising model, as follows from
the level-2 null-vector equation for the Ising four-point function (the method of Belavin, Polyakov and
Zamolodchikov 1984; the derivation of the value is in Ginsparg 1989, §5.2). It is computed through the
network (Section 3.4) and fails B★'s non-derivability clause. An independent tensor-network method
makes the same point from the other side. It reports 0.5004, 0.4997 and 0.5005 for three orderings of
the coefficient, after a correction whose three lengths are fitted per model to two-point channels only;
its uncorrected error over channels outside the fit is 0.496% RMS; and its input includes the fusion
category and the conformal weights (Meng, Lan and Gu 2026, §V A and Table II). The value is recovered
from CFT data because it is CFT data.

The two cases show that the dilemma is not a straw man. The program found quantities that were
network-specific but not robust, and quantities that were invariant but fixed by CFT data. It found none
that was both robust and not already fixed.

### 4.4 The relabelling objection

The most natural objection to the whole distinction runs as follows. Any observable that depends on a
network is still a functional of *some* state. Open an internal bond, attach a reference system to the
open end, and the network defines a state on the reference and the boundary, a Choi-type state of the
map from the internal leg to the boundary. A quantity defined on that state is a state functional after
all. Is the contrast between state functionals and network-sensitive observables then a relabelling?

The objection has a published form. Singh (2018, §I) views "a tensor network as representing two
different states by associating a many-body Hilbert space with the tensor network in two different
ways", treating the internal legs as physical degrees of freedom of an extended lattice. His construction
differs in detail from a Choi state, but it makes the same move.

It is not, because the contrast was never between states and non-states. It is between the *represented*
state and the *representing* map. Both hypotheses agree that the network represents the boundary state
$\rho$ faithfully; that is the common ground the trunk question presupposes. The question is whether the
representation has physical content beyond $\rho$. The Choi-type state of an internal leg is not fixed
by $\rho$. Two networks that produce the same boundary state can differ in it, because it records how the
network routes information from that leg to the boundary. Functionals of it are therefore exactly the
representation-dependent quantities B needs, and they are not state functionals in the sense of
Section 3. Singh's own observation that the extended states of gauge-equivalent networks "are generally
different" is the first requirement of Section 4.1 at work: a quantity defined on an extended state must
still be checked for gauge invariance, and the recovery observable of Section 8 was built to pass that
check.

Granting this does not make them physical. It relocates the question. Once a gauge-invariant,
representation-dependent quantity is in hand, one must still ask whether its value reflects the
represented state's physics or merely the ansatz: the graph, the bond dimension, the optimization.
The design of the program's recovery test (Section 8) shows the distinction doing work. Of the two
reference systems attached to a cut bond, the registration excluded the one on the upper end, which
holds a site of the network's ordinary state at the level of the bond. Its correlation with the
boundary tracks that state, which the registration calls "a functional of the state". The registration
kept the one on the lower end, whose correlation with the boundary depends on the isometries below the
bond (Prereg 2026).

### 4.5 Is the band empty?

One might hope to close the question with a no-go result: a proof that every gauge-invariant,
network-sensitive quantity of a MERA is fixed by CFT data and network parameters. The program considered
a version of this: the conjecture that every gauge-invariant quantity built from a MERA's causal-cone
graph distances and its tensors is a function of the scaling dimensions alone (Review working papers 2026,
research-primary.md §3; Review 2026, "Challenges not survived"). Its own review dropped it. Prior work on the
geometry of MERA pre-empted much of what the conjecture would have said: Milsted and Vidal (2018) give
MERA a rigorous light-sheet or light-cone geometry and conclude that it "describes neither the
hyperbolic plane nor de Sitter spacetime", and Bao et al. (2015) argue that "there are no conventional
MERA parameters that completely reproduce bulk physics even on super-AdS scales". Neither paper bears
directly on the conjecture's truth. What refutes it as stated is $C_{\sigma\sigma\epsilon}$: built from
the network's tensors, gauge-invariant, and not fixed by scaling dimensions alone. Narrowed to graph
distances only, the conjecture is, in the review challenger's words, "close to true by inspection"
(Review working papers 2026, research-challenge.md, P3); broadened to
all CFT data, which would include $C_{\sigma\sigma\epsilon}$, it is untested. Whether the band is
empty in principle is open. This paper takes no side beyond what the test of Section 8 permits.

## 5. Counterfactual novelty: how many outcomes were possible?

### 5.1 The question

Before a calculation is run, how many outcomes are genuinely possible? The program's standard asks this
of every claim and grades the answer. Counterfactual novelty is near zero when "conformal symmetry fixes
the answer exactly", so that "only implementation failure or success was possible"; moderate when "a
plausible extension was expected but not guaranteed"; and high when "multiple physically meaningful
outcomes were possible and each would support a different interpretation" (Director 2026, §6).

In Mayo and Spanos's formulation, a hypothesis H passes a severe test only if, among other things,
"with very high probability, test T would have produced a result that accords less well with H than x0
does, if H were false" (Mayo and Spanos 2006, p. 329). Counting outcomes before the run asks that question
before the data are in. The idea is Mayo's minimal severity requirement. Agreement produced by a
method "practically guaranteed to find such agreement" is "bad evidence, no test" (Mayo 2018, §1.1). It
also takes her side in the debate over use-novelty, which asks whether data used in constructing a
hypothesis can also support it (see Hitchcock and Sober 2004): what matters "is not whether passing is
assured but whether erroneous passing is" (Mayo 1996, pp. 274-275). Applied to a calculation offered as
evidence for a geometric interpretation, the question is whether the run would have disagreed had the
interpretation been false. When conformal symmetry fixes the answer, it would have agreed either way, so
its agreement says nothing about the interpretation. It confirms the implementation of the theorem.

The requirement has names in other fields. Clinical trials require "assay sensitivity", "the ability to
distinguish an effective treatment from a less effective or ineffective treatment" (ICH 2000, §1.5), and
Parker (2008) applies the error-statistical view to computer simulation. The founders of AdS/CFT made the
point about their own evidence: "some of the most direct checks" of the correspondence "are determined by
properties of the supergroup SU(2, 2|4)", and they were "inclined to believe that the correspondence is a
fundamental dynamical principle, valid independent of group theory" for reasons beyond those checks
(Aharony et al. 2000, §4.1.3).

### 5.2 The ledger

Applied to the program's 34 claims involving a calculation, the count found that 21 "could not have
come out otherwise": "conformal symmetry, a Virasoro identity, BPZ 1984, or the definition
$l_{AdS} = 1/\ln\chi$ fixed the answer before the run" (Audit 2026, §1). Four examples:

- **The force exponent.** The prediction $\alpha = 4$ is twice the scaling dimension of the stress
  tensor, $\Delta_T = 2$, which holds in every two-dimensional conformal field theory. In the Ising model
  the fusion rule $\epsilon \times \epsilon = 1$ leaves the identity's Virasoro family as the only
  exchange between two pure energy-density probes, and its lowest non-trivial member is the stress tensor.
  The program's own derivation obtains $\alpha = 4$ from the Kac table alone, with no geometry
  (Epsilon-channel note 2026; Audit 2026, §3). The prediction could not fail; only the measurement could.
- **"Universality."** The claim that $\alpha = 4$ also holds at the tricritical Ising and three-state
  Potts points compared a force exponent measured at Ising with scaling dimensions measured at the other
  two. No force was fitted at either, and every recorded $\alpha$ was exactly twice the adjacent
  $\Delta_T$: "a category mismatch presented in one table column" (Audit 2026, §5.2).
- **A coefficient ladder.** A sequence of stress-tensor three-point coefficients across three models
  was, in the audit's words, "a line of code, not a contraction": the identity
  $C_{TTT} = 2\sqrt{2}/\sqrt{c}$ evaluated on a measured central charge (Audit 2026, §3). The central
  charges were real measurements, and one improved on a published value; the coefficients added nothing
  to them.
- **A mass.** An effective mass $m_{\rm eff} = 0.693$ "agreeing" with 0.670 was $\ln 2 = 1/l_{AdS}$
  exactly (Audit 2026, §3).

The remaining 13 include the program's methodological work, none of which was "fixed in advance by
conformal symmetry" (Audit 2026, §5.1). The most promising physics candidate is instructive. In an
extension to the non-unitary Yang-Lee model, the sign of a central charge extracted from stress-tensor
matrix elements was first counted as the one measured bit with high counterfactual novelty. On
adjudication the audit ruled that, given four stated assumptions, the value and its sign follow
identically, so that "we measured $c = -22/5$ with its sign" has near-zero novelty. The open question was
whether the assumptions hold off unitarity at all: whether the lattice-to-continuum correspondence the
method relies on survives a non-normal Hamiltonian with an indefinite pairing. That is where the novelty lived (Audit 2026,
§10.3). Counterfactual novelty can sit in the assumptions of a calculation rather than in its output.

### 5.3 A pinned statistic, caught before the data

The diagnostic also works prospectively. The statistic originally registered for the program's
recovery test (Section 8) was $m_{1/2}$: the number of sites that can be removed from a boundary region
before a recovery measure falls below one half, with the "minimal cut" prediction located at about 8.5
sites. A devil's-advocate review, carried out before any registered value was looked at, showed that
purity and monotonicity force $m_L + m_R \le 17$ (the two edges' values) for *every* isometric network
on the registered graph. So $m_{1/2} \le 8.5$ always, with the cut prediction sitting exactly at the
bound, and an unregistered random network gave 8.50 (Amendment v3 2026). The registered statistic could
not have separated a cut-like network from a random one. The registration was amended before
unblinding, and the registered data later confirmed the identity: $m_{1/2} = 8.50$ in every network,
optimized or random (SIM-2026-079).

### 5.4 What the diagnostic does and does not do

Counterfactual novelty is a property of a test before it is run, not of its result, and it says nothing
about whether a result is correct. Low-novelty calculations remain valuable as validation of code and
methods; the program's standard calls this Level 1 work and asks only that it be labelled as such
(Director 2026, §5). The error the diagnostic prevents is the presentation of validation as discovery,
which is the error Hypothesis A predicts a geometry-minded program will make.

## 6. Independence: agreement among same-input quantities

### 6.1 One input, two numbers

Two numbers that agree because both are transformations of one input are one number. The point is
familiar from the philosophy of robustness. Robustness procedures "require at least partial independence
of the various processes across which invariance is shown", and presuming independence on thin evidence
produces "a kind of illusory robustness" (Wimsatt 1981, §2.1). The program's standard turns the point
into a ledger. For every comparison, list the raw data, assumptions, fitted parameters, exact identities, code
and state preparation shared by both sides, then classify the comparison as fully independent, partially
independent, structurally dependent, algebraically equivalent, or a consistency check: "A beautiful
agreement is not strong evidence if both sides are transformations of the same input" (Director 2026,
§7).

### 6.2 The ledger applied

The audit catalogued 24 agreements the program presented as evidence. "Four carry information that was
not already in the inputs. The other twenty are exact CFT identities evaluated numerically, algebraic
restatements of one measured number, or the same state measured twice through the same code with one
parameter changed" (Audit 2026, §5). Most traced to a handful of inputs that appeared on both sides of a
comparison. The two that mattered for the geometric claims were $\Delta_T = 2$, a theorem, and
$l_{AdS} = 1/\ln\chi$, a definition, the latter sitting on both sides of two of the comparisons (Audit
2026, §5.3). A convention on both sides of a comparison is illusory robustness in its plainest form. The audit's editor concluded that "every geometric quantity in the manuscript reduces along
the dependency graph to $l_{AdS} = 1/\ln\chi$ (a definition) or $\Delta_T = 2$ (a theorem)" (Audit
2026, §7.3).

### 6.3 The retraction as a worked example

The program's headline was a force exponent $\alpha = 3.92 \pm 0.16$, matching the stress-tensor
prediction of 4 to within 2%, and presented as supported by three independent evaluations: 3.92, 3.97 and
4.07, from a 24-site exact chain, a 16-site exact chain and a 16-site $\chi = 3$ MERA. A re-analysis
found the following (SIM-2026-072):

- Unweighted least squares in linear space, applied to a steeply falling profile, put 95.8% of its
  objective on the single point at separation $dr = 2$. The published exponent was, to within 8%, the
  local slope between $dr = 2$ and $dr = 3$. Changing nothing but the error model, and discarding no
  data, gave 2.82 or 2.89.
- Across 15 defensible estimator choices the exponent ranged from 2.534 to 3.922. The published value
  was the largest of the 15.
- The profile did contain a power law, just not the claimed one. Six consecutive local slopes were flat
  to within 7.5% around 2.592, giving $\alpha = 2.6 \pm 0.2$, which matches neither candidate exchange
  channel the program considered: stress-tensor exchange, $2\Delta_T = 4$, expected for pure
  energy-density probes (Section 5.2), or exchange of the energy operator itself,
  $2\Delta_\epsilon = 2$, possible if the lattice probes are not pure. The point at $dr = 2$ is the one
  separation at which a Hamiltonian bond bridges the two probes, a contact term.
- The three "independent evaluations" moved together under the dominant systematic: on dropping
  $dr = 2$ they became 2.56, 2.75 and 2.63. They shared one observable, one operator, one fit window
  and one fitting routine. "Agreement among them measured the estimator, not the physics."

The corrected plateau value was reproduced (2.5920966 against 2.592) by a rewritten code path with a
different operator implementation and Hamiltonian routine (SIM-2026-073), and the retraction was
published (Cackler 2026a; Errata 2026, E6). This is one of the few places in the case where a result rests on
independently written code, although both analyses read the same cached ground state.

Two features matter for the argument. First, the three agreeing numbers failed together, as the ledger
predicts of structurally dependent quantities; their agreement had been offered as robustness, and it was
the opposite. Second, the two diagnostics point the same way. The withdrawn value had near-zero
counterfactual novelty, because a theorem fixed it in advance. The corrected value has more: a plateau at
2.6 was predicted by neither channel, which makes it a modest open question rather than a confirmation
(SIM-2026-072).

### 6.4 The same failure in operational records

The ledger's logic applies to a program's records about the world as much as to its physics. On
17 August 2026 the program discovered that a journal had rejected its manuscript on 12 August. For those
five days three internal records, a task list, a memory file and the research log, had said that the
manuscript was "with editors". They had been written by one process on 7 August from a single lookup;
they agreed with each other and with nothing outside, and the rejection surfaced only when the inbox
rather than the notes was checked (Discovery commit 2026). Three agreeing notes and no fresh lookup
amount to one lookup. The program's audit, written in the same days, still set its priorities "because a
paper is with editors" (Audit 2026, §9). And the failure recurred in miniature: the rule the program then wrote to
prevent it recorded the discovery as 23 August and the delay as eleven days, an error the commit history
corrects (Project instructions 2026; corrected 15 October 2026).

### 6.5 What the ledger does not deliver

Independence is necessary for agreement to count as robust, but not sufficient. Robustness "requires
having multiple modes of evidence, knowing that multiple modes of evidence are independent, and knowing
how they should be independent, and yet remains fallible" (Stegenga 2009, p. 654): concordant independent
evidence can still support a false conclusion. Stegenga's separate discordance problem is that real
evidence from several modes is usually discordant, and robustness offers no rule for weighing it
(Stegenga 2009, §3). The ledger classifies comparisons by shared data, assumptions and code, which is
what Stegenga and Menon (2017) call ontic independence, and they argue that, as typically construed, it
"is not a sufficient independence condition" for robustness arguments. Parker (2011) reaches a related
conclusion for agreeing climate models, and Gueguen (2020) for cosmological simulations, proposing
"crucial simulations" in place of robustness analysis, a move that parallels this program's turn from
agreements to a discriminating observable (Section 8). The ledger is a filter against overclaiming. It
does not manufacture confirmation.

## 7. Three narrowed routes as boundary markers

A negative result that closes or narrows a route tells us about the shape of the question only if the
test could have come out the other way. Three of the program's routes show three different ways this can
happen. Only the first was formally closed.

### 7.1 A pre-registration that was vacuous by symmetry

To decide which operator carried the force, the program registered a killer test comparing the force
measured with two lattice probes, $Z_j Z_{j+1}$ and $X_j$, expected to give exponents 4 and 2. At its
critical point the transverse-field Ising chain is Kramers-Wannier self-dual, and the duality maps
$Z_j Z_{j+1}$ to $X_j$: the two probes are one continuum operator, the energy density. Their vacuum
expectation values agree to $10^{-15}$ and their force profiles to $10^{-13}$ at every separation on a
ring (SIM-2026-074; Errata 2026, E8). The registered test could never have discriminated, and an earlier
run's apparent contrast between the two probes turned out to be an open-boundary artifact. The direct
replacement, comparing the spin operator with the energy density, was blocked by a parity-sector
obstruction. A further registered attempt returned VOID: the force vanishes exactly for the
duality-odd local energy density, and at accessible sizes the local energy density is dominated by
short-distance effects. The hypothesis was closed as untestable at up to 24 sites (SIM-2026-075;
HYP-2026-008). The lesson extends Section 5: counting the possible
outcomes of a test must include checking that its alternatives are distinct.

### 7.2 A regulator that erases the quantity

In the continuum, the entanglement entropy of a timelike interval in a two-dimensional conformal field
theory acquires an imaginary part, $i\pi c/6$, and its authors suggest that this imaginary part
"describes an emergent time which generalizes the notion of an emergent space from quantum entanglement"
(Doi et al. 2023, abstract and eq. 2.23 of the arXiv version). The program's hypothesis took up that
reading (HYP-2026-032). On the critical lattice, the literal
transition matrix $e^{iRH}$ gives an exactly real pseudo-entropy, because the chain has a chiral symmetry
$VHV^\dagger = -H$. None of four registered lattice constructions reproduced the imaginary part, while, with a regulator
added, the real part followed the expected logarithmic form with $c = 1/2$ to within 2 to 3% in an
exploratory run (SIM-2026-076; SIM-2026-077). One follow-up thread remains open. The imaginary part is, on this lattice, a property of the continuum analytic
continuation, not of any transition matrix the program examined. A geometric reading can lean on a
quantity that the regulator removes.

### 7.3 A number that survives its interpretation

The program's transport time, $T = 2.239$ (16 sites), agreed with the geometric prediction
$(\pi/2)\,l_{AdS} = 2.266$ to 1.2%, with $l_{AdS} = 1/\ln 2$ (Audit 2026, §3). The derivation the
program cited for the prediction gives a crossing time of $\pi$, "independently of the values of M,
$\Omega$, and $\ell$": the AdS radius cancels (Wang and He 2026, Supplemental Material §S3 A; see also
Audit 2026, D-1 resolution). In the boundary normalization, the radius-free predictions are
$\pi/2 = 1.571$ or $\pi = 3.142$, and neither matches; the reported agreement "is supplied entirely by
the free factor $1/\ln 2$" (Audit 2026, §7.2 item 2). The measured time survives as a fact about the
lattice. Its geometric reading does not. The program's record keeps the hypothesis at status SUPPORTED
with confidence lowered to "low" (HYP-2026-006).

Each marks a different boundary. The first shows that a registration can be emptied by a
symmetry nobody checked. The second shows that a geometric signature can belong to the continuum
idealization rather than to the system represented. The third shows that a number and its
interpretation can come apart, so that confirming the one does nothing for the other.

## 8. A registered network-sensitive test: bulk operator recovery

### 8.1 Why this observable

A review of the program's options found one candidate that measures a property of the network rather
than of the state, and so the only one that could reach a discriminating result: bulk operator recovery
(Review 2026, executive summary). The idea is to open an internal bond, treat it as a bulk input, and
ask how much of what is fed in there a boundary region can recover. The test was pre-registered before
any network was optimized, revised before registration and amended once after it, all before
unblinding, and run once (Prereg 2026; Amendment v3
2026; SIM-2026-079).

### 8.2 The construction

The network was a ternary MERA for the critical transverse-field Ising chain: 27 boundary sites of two spins
each, two ternary layers closed by a top tensor on a three-site ring, periodic, bond dimension $\chi = 6$, optimized with a symmetry-respecting routine validated
earlier (SIM-2026-061). A bond $b$ at the output of a second-layer isometry was cut; its causal footprint
$C(b)$ covers 17 boundary sites. A reference system was attached to each open end of the cut, $R_{low}$
on the end that feeds the network below $b$ and $R_{up}$ on the other. The global state on the two
references and the boundary is pure. For a boundary region $A$ the registered observable is

$$ f(A) = \frac{I(R_{low} : A)}{2\,S(R_{low})}, $$

which is 1 when everything about the inserted leg is recoverable from $A$ and 0 when $A$ learns nothing
about it (Prereg 2026).

Two choices in the design carry the philosophical weight.

- **Only the lower reference counts.** The registration explains that the upper reference "is correlated
  with the whole boundary through the top of the network, so $I(R_{up}:A)$ is a functional of the
  state", which it calls "the trap the 2026-09-14 review named" (Prereg 2026). The design applies
  Section 3's distinction to its own components.
- **A mutual information, not the error for a fixed operator.** A gauge transformation $U$ on the bond
  maps a fixed inserted operator $O$ to $U^\dagger O U$, so a fixed-operator recovery error changes under
  gauge by construction, and a control that randomizes the gauge "would fire every time and prove
  nothing". Under the same $U$, $R_{low}$ is rotated by a local unitary and $I(R_{low}:A)$ is exactly
  invariant (Prereg 2026). A gate checked the invariance numerically and passed in all 24 networks
  (SIM-2026-079).

The observable is therefore a gauge-invariant joint functional of state and network. It sits in the
band of Section 4.

### 8.3 Predictions and registered outcomes

The region $A$ starts as the full footprint and shrinks by removing $m$ sites from one edge, run from
each side. Two predictors disagree about where recovery fails. If the network behaves as a circuit,
recovery depends only on overlap with the causal footprint and fails as soon as one footprint site is
dropped, near $m = 1$. If it behaves like a holographic code, recovery holds while the bond lies on
$A$'s side of the minimal cut through the network, and fails when the cut flips past the bond, between
$m = 8$ and $m = 9$ on this graph (Prereg 2026).

Four outcomes were registered as genuinely possible: cone-like (recovery needs the whole footprint);
cut-like in the optimized network but not in Haar-random networks on the same graph; cut-like in both, a
property of the graph; and smooth, with no sharp threshold. The registration named the smooth outcome as
the expected one, for two stated reasons. First, Kim and Kastoryano (2017) treat MERA for critical
systems as an encoding circuit for approximate error-correcting codes, with protection controlled by a
parameter that the registration argued is small for the Ising model, which has a light operator
($\Delta_\sigma = 1/8$); recovery should then degrade gradually. Second, minimal-cut entropies and
reconstruction are established for independent random tensors at large bond dimension (Hayden et al.
2016), not at $\chi = 6$ to 8. The
registration banned the words "geometry", "wedge" and "emergent" for the cone-like, graph-property and
smooth outcomes (Prereg 2026). Controls, eight optimizations or draws each: Haar-random tensors on the
same graph (C-HAAR), and the same pipeline at a gapped point, transverse field $h = 1.5$ (C-GAPPED). A
planned rewiring control, the same tensors on a different graph, was found infeasible before any result
and left out.

### 8.4 Corrections before unblinding

The design changed several times before unblinding. Two of the changes moved it toward the band of
Section 4. The first version attached a reference to both ends of the bond, and so mixed a state
functional into the observable; it was corrected to the lower end only. The second change was the
amendment of Section 5.3: the registered statistic $m_{1/2}$ was pinned by an identity, so the primary
statistic became $m_{0.9}$, the first $m$ at which $f$ falls below 0.9. A cut-like verdict now required
$m_{0.9} \ge 6$ on both edges *and* a seed mean at least three sites above the Haar control. The same
amendment lowered the best possible outcome from Level 4 to Level 3, "holographic-code-like encoding of
the optimized circuit", because a discriminating (Level 4) claim needs a non-geometric ansatz matched on
CFT data and none was registered (Prereg 2026, v3 amendment).

### 8.5 Result

Seed means at $\chi = 6$, eight networks per arm (SIM-2026-079):

| Network | $m_{0.9}$, left / right | width $w$ | $m_{1/2}$ |
|---|---|---|---|
| Optimized MERA, critical | 4.75 / 4.34 | 7.76 | 8.50 |
| Haar-random, same graph (C-HAAR) | 4.62 / 4.62 | 6.06 | 8.50 |
| Optimized MERA, gapped $h = 1.5$ (C-GAPPED) | 4.91 / 4.19 | 7.59 | 8.50 |

The verdict was outcome 4, smooth: the width of the loss curve exceeded the registered threshold
($w = 7.76 > 6$); the curve was not cut-like ($m_{0.9}$ below 6 on both edges, and a mean of 4.55
against the Haar control's 4.62, where three sites of separation were needed); and it was not cone-like
($m_{1/2} = 8.50$). This was the registered expected outcome, at Level 2 (SIM-2026-079). The gates for
structure, purity and gauge invariance passed in all 24 networks. The gate for stability under bond
dimension could not be evaluated: all four $\chi = 8$ networks exceeded the 62 GB memory available.

In words: the onset of recovery loss in the optimized critical network, about four and a half of
seventeen sites, cannot be told apart from that in Haar-random networks on the same graph, and the
gapped network shows the same picture, so nothing in the registered statistics tracks criticality. The
optimized networks' loss curves are broader than the Haar networks' and asymmetric between edges, by up
to 1.9 sites in the critical networks and 2.26 in the gapped ones, against at most 0.04 for Haar. That difference was noticed after unblinding, has no
registered test, and is not offered as evidence for anything (SIM-2026-079).

### 8.6 What the result shows, and what it does not

Section 4 described four ways a candidate observable can fail: it can be gauge-variant; it can be a
state functional; it can vary with incidental choices of representation; or it can be a gauge-invariant,
network-sensitive quantity whose value is fixed by something Hypothesis A already grants. The recovery
observable avoids the first two by construction and by gate. The third could not be tested, because the
bond-dimension gate failed to run. At the accessible bond dimension, its registered statistic falls into
the fourth: the onset of
recovery loss is a property shared with random tensors on the same graph, and so, as far as this test
can see, a property of the graph. In the one observable in the program that touched the network, the registered statistic, the onset of
recovery loss, did not separate the optimized network's encoding of the critical state from the graph
that carries it.

The result is not a refutation of Hypothesis B. Bond dimension 6 is far from the large-bond-dimension
regime of the random-tensor-network results (Hayden et al. 2016), which in any case concern independent
random tensors rather than the random isometries of the control arm, so they bear on this test only by
analogy. Recent work derives cut-like algebraic structure for networks assumed to be exactly isometric,
argues for it in random networks at large bond dimension, and sets finite bond dimension aside; its
networks also have no bulk legs, unlike the internal-leg insertion used here (Sahu et al. 2026). The test
could not reach $\chi = 8$. Its counterfactual novelty was moderate and its surprise low: four outcomes were possible
and the stated prior obtained (SIM-2026-079). Nor was it built to discriminate: no non-geometric ansatz
matched on CFT data was registered, which is why its best outcome was capped below Level 4. What the
result does is show the fourth failure mode of Section 4 occurring in the one probe of the band the
program could afford, at a stated size and for a stated reason. It adds nothing in favour of Hypothesis
B, and it does not refute it.

## 9. Discussion: what would make geometry more than a visualization?

### 9.1 Where the evidence leaves the hypotheses

On the evidence of this case, Hypothesis A is the parsimonious reading in this setting. That is a claim
about evidence, not a proof that B is false. The audit's editor drew the same line: Hypothesis A "is
unrefuted and is the parsimonious reading of the project's own records. That is not 'A is proven'"
(Audit 2026, §7.3). The reason it is parsimonious is not that the program tested B and B failed. It is
that every result the program offered for B turned out, on inspection, to be something A already
predicts: a state functional, a theorem, a definition, or (for the onset of recovery loss in Section 8) a
property of the graph.

### 9.2 What Hypothesis B would need

The analysis of Sections 3, 4 and 8 yields a list of conditions that a result supporting B in this
setting would have to meet. It would need an observable that is

1. a gauge-invariant joint functional of state and network (Sections 3 and 4);
2. robust across incidental choices of discretization, such as bond dimension and branching, within the
   class of networks whose geometry is in question (Section 4.1);
3. different between optimized networks and random networks on the same graph, or else it is a property
   of the graph (Section 8);
4. different between geometry-bearing networks and a non-geometric ansatz matched on ordinary CFT
   observables, a control the program never had;
5. not fixed by CFT data or by network parameters (B★'s second clause); and
6. the subject of a parameter-free prediction made before the measurement (B★'s third clause).

These conditions are demanding, but nothing shows them to be unsatisfiable. The audit's advocate
identified three classes of test that survive in principle: rewiring the network's internal
connectivity while preserving the boundary state (Director 2026, §11.H), entanglement-wedge-style
reconstruction, and the dependence of transport on the central charge (Audit 2026, §7.2 item 4). The
recovery test of Section 8 belongs to the second class; the rewiring control planned for it was found
infeasible at that size.

### 9.3 Emergence of what?

Suppose every network-sensitive invariant turns out, in the end, to be fixed by the graph. Then the
"geometry" of tensor networks would be a property of the ansatz: of a class of representations, not of
the states they represent. It might still count as emergent in Butterfield's sense, behaviour "novel and
robust relative to some comparison class" (Butterfield 2011, §1.1), with the individual tensors as the
comparison class. But it would be a fact about the class of networks on that graph, not about the
physics of the critical state.

This sharpens a theme already present in the philosophy of gauge/gravity duality. Dieks, van Dongen and
de Haro (2015, §3.3.2) read the two sides of an exact duality as "different representations of one and
the same physical theory", with "no emergence of one side of the duality from the other". Rickles (2013)
locates "an issue of representation and redundancy in representation" at the core of AdS/CFT. De Haro
(2017) calls duality and emergence "two notions that are close to each other but also exclude one
another", and De Haro, Mayerson and Butterfield (2016, §10.2) argue that for emergence the duality
concerned "can only be approximate". The tensor-network case is not a duality at all. There is one theory, the boundary CFT,
and a family of non-unique, approximate representations of one of its states. The question is whether a
feature shared by some of those representations is a feature of the physics, which is closer to asking
whether a gauge-dependent structure is physical than to asking whether a dual is emergent.

### 9.4 A parallel with analogue confirmation

Dardashti, Thébault and Winsberg (2017, §1) argue that an analogue system can confirm claims about an
inaccessible target only through "model-external and empirically grounded arguments": in their case,
universality arguments combined with diverse realisations of the effect. Their subject is physical
analogue systems, and they treat computer simulation as a related but distinct case (§3.1), so applying
the point to a computational representation is our extension. With that caveat, the claim that a
network is a bulk needs a comparable model-external argument: a reason, other than a resemblance of
graphs, to expect the internal structure of an optimized small-bond-dimension MERA to share properties
with a gravitational bulk. Such reasons exist in idealized regimes: exactly solvable codes (Pastawski et
al. 2015), random tensors at large bond dimension (Hayden et al. 2016), and networks assumed to be
exactly isometric (Sahu et al. 2026). Those are the regimes this case does not reach, and for the
networks it does reach, the bridge is the claim in question.

### 9.5 Lessons for practice

The case supports five habits for anyone using tensor networks to study emergent geometry, at small
cost:

1. **Withhold geometric language** from any quantity until a network-sensitive observable exists
   (Review 2026, recommendation 4).
2. **Count the possible outcomes** of a calculation before running it, and record the count, including
   a check that the alternatives are distinct (Sections 5 and 7.1).
3. **Keep an independence ledger** for every agreement offered as evidence, and for records about the
   world as well as for physics (Section 6).
4. **Register the expected outcome** alongside the alternatives, and report it plainly when it occurs
   (Section 8).
5. **Retract quickly and in public.** A review inside the program judged the self-executed retraction to
   be "the scarcest artifact the project owns" (Review 2026, key finding 5).

None of this was expensive. The registered recovery test ran under a 25 USD cap; its final run cost about
6.5 USD at the provider's list price, not counting earlier attempts whose optimized networks it reused
(SIM-2026-079; Prereg 2026).

## 10. Conclusion

A quantity fixed by the boundary state alone takes the same value in every faithful representation of
that state. Its agreement with a geometric formula therefore cannot discriminate between the view that a
tensor network's geometry is an efficient representation and the view that it carries operational
content, however precise the agreement is. The precision measures ansatz fidelity.

Any content for the geometric reading must live in quantities that are invariant under the network's
gauge freedom yet sensitive to its organization, robust across incidental choices of discretization, and
not fixed by CFT data or network parameters. The requirements pull against each other, and the case
examined here contains quantities that fail each of them except gauge invariance, which its recovery
test was built to satisfy.

Two diagnostics, counterfactual novelty and an independence ledger, explain most of what went wrong in
the case. They caught one problem in advance, a registered statistic pinned by an identity, and they
account after the fact for three "independent" evaluations that failed together and for three internal
records that agreed with each other and with nothing outside.

The one gauge-invariant, network-sensitive observable the program built, bulk operator recovery, came
out as its registration expected. At bond dimension 6 the onset of recovery loss in the optimized
network could not be told apart from that in random networks on the same graph. The trunk question
remains open. What the case settles is narrower and, we think, useful: which kinds of evidence cannot
answer it, and what an answer would have to look like.

## Limitations

- **One program, one model class.** The case is 1+1-dimensional critical lattice models with
  small-bond-dimension MERA. Nothing generalizes to AdS/CFT, higher dimensions or large-N holography
  without a separate argument.
- **Self-audit.** The evidence comes from the author's own program and its internal audits, carried out
  by AI agents working under a written standard. Those audits are same-origin sources in the sense of
  Section 6. The retraction was reproduced by independently written analysis code, reading the same cached
  ground state (SIM-2026-073), and the correction is public (Cackler 2026a), but no outside referee has checked the audit.
- **The represented state is taken as the target.** Section 4.4 answers the relabelling objection by
  fixing the boundary state as what the network represents, which is how both hypotheses frame the
  question. A reader who takes the network's full state on all its legs as the physical target would
  dissolve the distinction, but would also dissolve the trunk question with it.
- **One size.** The recovery test ran at $\chi = 6$ only; the bond-dimension stability gate could not be
  evaluated.
- **No new theorem, and partial prior statements.** A novelty check run under the program's standard
  (Director 2026, §8) found partial prior statements of all three central moves: the
  state-functional argument (Singh 2018; Molnar et al. 2018; Huggett 2017; the law of likelihood), each
  horn of the dilemma (Section 4.1), and the two diagnostics (Mayo and Spanos 2006; ICH 2000; Stegenga
  and Menon 2017). It found no statement of the dilemma as a combined, evidentially framed argument, and
  none of the state-functional conclusion for tensor-network geometry. Ney (2021) states the
  non-discrimination step for holographic entanglement-distance agreements and is cited in Section 3.2.
  PhilSci-Archive and PhilPapers could not be searched automatically, so a further
  prior statement there cannot be ruled out.
- **Literature positions.** Positions attributed to other authors were checked against their texts.
  Redhead (1975) could not be accessed, so it is cited through French
  and Rickles (2003).

## Disclosure and data availability

**Use of AI.** The research program examined here was carried out with
AI research agents (Claude, by Anthropic); from 11 August 2026 they worked under the written standard
cited as Director (2026), and the program's audits and reviews were performed by such agents. This paper was drafted with the same
assistance from the author's outline and the program's records. Every quotation and number was checked
against those records. The author is responsible for the content.

**Data availability.** All program records cited here (the standard, the audit, the review, the errata,
the simulation and hypothesis records, the pre-registration and its amendment) are in a public
repository, github.com/jonboy648/quantum-worldline, at the paths listed under Program records below. The
published correction is Cackler (2026a). A snapshot of the repository in the state cited here is archived as
Cackler (2026b), doi:10.5281/zenodo.23403085.

## References

Aharony, O., Gubser, S. S., Maldacena, J., Ooguri, H., Oz, Y. (2000). Large N field theories, string
theory and gravity. *Physics Reports* 323, 183-386. arXiv:hep-th/9905111.

Almheiri, A., Dong, X., Harlow, D. (2015). Bulk locality and quantum error correction in AdS/CFT.
*Journal of High Energy Physics* 2015(04), 163.

Bao, N., Cao, C., Carroll, S. M., Chatwin-Davies, A., Hunter-Jones, N., Pollack, J., Remmen, G. N.
(2015). Consistency conditions for an AdS multiscale entanglement renormalization ansatz
correspondence. *Physical Review D* 91, 125036. arXiv:1504.06632.

Belavin, A. A., Polyakov, A. M., Zamolodchikov, A. B. (1984). Infinite conformal symmetry in
two-dimensional quantum field theory. *Nuclear Physics B* 241, 333-380.

Beny, C. (2013). Causal structure of the entanglement renormalization ansatz. *New Journal of Physics*
15, 023020.

Bradley, C., Weatherall, J. O. (2020). On representational redundancy, surplus structure, and the hole
argument. *Foundations of Physics* 50, 270-293. doi:10.1007/s10701-020-00330-y.

Butterfield, J. (2011). Less is different: emergence and reduction reconciled. *Foundations of Physics*
41, 1065-1135.

Cackler, J. (2026a). *Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits*,
version 5 (correction and retraction of the force exponent). Zenodo. doi:10.5281/zenodo.22080720.

Cackler, J. (2026b). *Quantum Worldline: research repository snapshot (2026-10-15)*. Zenodo.
doi:10.5281/zenodo.23403085.

Cao, C., Carroll, S. M., Michalakis, S. (2017). Space from Hilbert space: recovering geometry from bulk
entanglement. *Physical Review D* 95, 024031.

Crowther, K. (2016). *Effective Spacetime: Understanding Emergence in Effective Field Theory and Quantum
Gravity*. Springer.

Crowther, K. (2018). Inter-theory relations in quantum gravity: correspondence, reduction and emergence.
*Studies in History and Philosophy of Modern Physics* 63, 74-85.

Dardashti, R., Thébault, K. P. Y., Winsberg, E. (2017). Confirmation via analogue simulation: what dumb
holes could tell us about gravity. *British Journal for the Philosophy of Science* 68, 55-89.

De Haro, S. (2017). Dualities and emergent gravity: gauge/gravity duality. *Studies in History and
Philosophy of Modern Physics* 59, 109-125.

De Haro, S., Mayerson, D. R., Butterfield, J. N. (2016). Conceptual aspects of gauge/gravity duality.
*Foundations of Physics* 46, 1381-1425.

Dieks, D., van Dongen, J., de Haro, S. (2015). Emergence in holographic scenarios for gravity. *Studies
in History and Philosophy of Modern Physics* 52, 203-216.

Doi, K., Harper, J., Mollabashi, A., Takayanagi, T., Taki, Y. (2023). Timelike entanglement entropy.
*Journal of High Energy Physics* 2023(05), 052. doi:10.1007/JHEP05(2023)052. arXiv:2302.11695.

Evenbly, G., Vidal, G. (2011). Tensor network states and geometry. *Journal of Statistical Physics* 145,
891-918. arXiv:1106.1082.

French, S., Rickles, D. (2003). Understanding permutation symmetry. In K. Brading and E. Castellani
(eds.), *Symmetries in Physics: Philosophical Reflections*. Cambridge University Press.
arXiv:quant-ph/0301020.

Ginsparg, P. (1989). Applied conformal field theory. In E. Brézin and J. Zinn-Justin (eds.), *Fields,
Strings and Critical Phenomena* (Les Houches, Session XLIX, 1988). North-Holland. arXiv:hep-th/9108028.

Gueguen, M. (2020). On robustness in cosmological simulations. *Philosophy of Science* 87, 1197-1208.
doi:10.1086/710839.

Hacking, I. (1965). *Logic of Statistical Inference*. Cambridge University Press.

Hayden, P., Nezami, S., Qi, X.-L., Thomas, N., Walter, M., Yang, Z. (2016). Holographic duality from
random tensor networks. *Journal of High Energy Physics* 2016(11), 009. arXiv:1601.01694.

Hitchcock, C., Sober, E. (2004). Prediction versus accommodation and the risk of overfitting. *British
Journal for the Philosophy of Science* 55, 1-34.

Huggett, N. (2017). Target space ≠ space. *Studies in History and Philosophy of Modern Physics* 59,
81-88. doi:10.1016/j.shpsb.2015.08.007. arXiv:1509.06229.

Huggett, N., Wüthrich, C. (2013). Emergent spacetime and empirical (in)coherence. *Studies in History
and Philosophy of Modern Physics* 44, 276-285.

Hyatt, K., Garrison, J. R., Bauer, B. (2017). Extracting entanglement geometry from quantum states.
*Physical Review Letters* 119, 140502. arXiv:1704.01974.

ICH (2000). *E10: Choice of Control Group and Related Issues in Clinical Trials*. International Council
for Harmonisation (FDA guidance, May 2001).

Jacobs, C. (2021). Invariance or equivalence: a tale of two principles. *Synthese* 199, 9337-9357.
doi:10.1007/s11229-021-03205-5.

Jaksland, R. (2021). Entanglement as the world-making relation: distance from entanglement. *Synthese*
198(10), 9661-9693. doi:10.1007/s11229-020-02671-7.

Jaksland, R. (2025). Spacetime from entanglement: the emergence of metric, gravity, or topology.
*Philosophy of Physics* 3(1), 18. doi:10.31389/pop.219. arXiv:2607.09823.

Kim, I. H., Kastoryano, M. J. (2017). Entanglement renormalization, quantum error correction, and bulk
causality. *Journal of High Energy Physics* 2017(04), 040. arXiv:1701.00050.

Li, R. (2026). When does a state-dependent proto-area define a bulk geometry? arXiv:2606.22598
(v3, 12 October 2026).

Mayo, D. G. (1996). *Error and the Growth of Experimental Knowledge*. University of Chicago Press.

Mayo, D. G. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars*.
Cambridge University Press.

Mayo, D. G., Spanos, A. (2006). Severe testing as a basic concept in a Neyman-Pearson philosophy of
induction. *British Journal for the Philosophy of Science* 57, 323-357. doi:10.1093/bjps/axl003.

Meng, C., Lan, T., Gu, Z. (2026). Algebraic tensor network renormalization and holographic duality.
arXiv:2610.08787 (preprint).

Milsted, A., Vidal, G. (2018). Geometric interpretation of the multi-scale entanglement renormalization
ansatz. arXiv:1812.00529 (preprint).

Molina-Vilaplana, J. (2015). Information geometry of entanglement renormalization for free quantum
fields. *Journal of High Energy Physics* 2015(09), 002. arXiv:1503.07699.

Molnar, A., Garre-Rubio, J., Pérez-García, D., Schuch, N., Cirac, J. I. (2018). Normal projected entangled
pair states generating the same state. *New Journal of Physics* 20, 113017. arXiv:1804.04964.

Ney, A. (2021). From quantum entanglement to spatiotemporal distance. In C. Wüthrich, B. Le Bihan and
N. Huggett (eds.), *Philosophy Beyond Spacetime: Implications from Quantum Gravity*. Oxford University
Press, 78-102. doi:10.1093/oso/9780198844143.003.0004.

Nguyen, J., Teh, N. J., Wells, L. (2020). Why surplus structure is not superfluous. *British Journal for
the Philosophy of Science* 71, 665-695. doi:10.1093/bjps/axy026.

Parker, W. S. (2008). Computer simulation through an error-statistical lens. *Synthese* 163, 371-384.
doi:10.1007/s11229-007-9296-0.

Parker, W. S. (2011). When climate models agree: the significance of robust model predictions.
*Philosophy of Science* 78, 579-600. doi:10.1086/661566.

Pastawski, F., Yoshida, B., Harlow, D., Preskill, J. (2015). Holographic quantum error-correcting codes:
toy models for the bulk/boundary correspondence. *Journal of High Energy Physics* 2015(06), 149.
arXiv:1503.06237.

Qi, X.-L. (2013). Exact holographic mapping and emergent space-time geometry. arXiv:1309.6282
(preprint).

Redhead, M. (1975). Symmetry in intertheory relations. *Synthese* 32, 77-112. [Not seen; cited as in French
and Rickles 2003.]

Rickles, D. (2013). AdS/CFT duality and the emergence of spacetime. *Studies in History and Philosophy
of Modern Physics* 44, 312-320.

Rovelli, C. (2014). Why gauge? *Foundations of Physics* 44, 91-104. arXiv:1308.5599.

Royall, R. (1997). *Statistical Evidence: A Likelihood Paradigm*. Chapman & Hall.

Sahu, A., van der Heijden, J., Van Raamsdonk, M., Zibakhsh, R. (2026). Algebraic structure in
holographic tensor networks. arXiv:2610.00478 (preprint).

Singh, S. (2018). Tensor network state correspondence and holography. *Physical Review D* 97, 026012.
arXiv:1701.04778.

Stegenga, J. (2009). Robustness, discordance, and relevance. *Philosophy of Science* 76, 650-661.

Stegenga, J., Menon, T. (2017). Robustness and independent evidence. *Philosophy of Science* 84,
414-435. doi:10.1086/692141.

Swingle, B. (2012). Entanglement renormalization and holography. *Physical Review D* 86, 065007.

Teh, N. J. (2013). Holography and emergence. *Studies in History and Philosophy of Modern Physics* 44,
300-311.

Vidal, G. (2007). Entanglement renormalization. *Physical Review Letters* 99, 220405.

Wang, Z., He, L. (2026). Black-hole signatures in the finite-temperature critical Ising chain.
arXiv:2603.07639 (preprint).

Wimsatt, W. C. (1981). Robustness, reliability, and overdetermination. In M. B. Brewer and B. E.
Collins (eds.), *Scientific Inquiry and the Social Sciences*. San Francisco: Jossey-Bass.

### Program records

All paths are relative to the public repository github.com/jonboy648/quantum-worldline, archived as Cackler (2026b).

- **Director (2026).** Quantum Worldline: Advanced Scientific Research Director (governing standard,
  adopted 11 August 2026). `docs/governance/RESEARCH-DIRECTOR.md`.
- **Audit (2026).** Quantum Worldline: Formal Scientific Audit (dated 11 August 2026, written
  17 August 2026). `docs/governance/AUDIT-2026-08-11.md`.
- **Review (2026).** What could this project do that is genuinely valuable? Final report
  (14 September 2026). `research/data/audit/valuable-questions-2026-09-14/FINAL-REPORT.md`.
- **Errata (2026).** Errata register, entries E6 and E8. `research/ERRATA.md`.
- **Prereg (2026).** Pre-registration: bulk operator recovery in an optimized MERA, causal cone versus
  minimal cut (registered 22 September 2026, with the v3 amendment approved the same day).
  `research/tools/bulk-recovery/PREREGISTRATION-HYP033.md`.
- **Amendment v3 (2026).** `research/tools/bulk-recovery/AMENDMENT-V3-PROPOSAL-HYP033.md`.
- **Epsilon-channel note (2026).** `research/data/theory/epsilon-channel-proof.md`.
- **Transport driver (2026).** `research/data/simulations/holographic_transport_16q.py`.
- **Project instructions (2026).** `CLAUDE.md`, section "External Status Must Be Freshly Checked"
  (added 23 August 2026; its dates were wrong until corrected on 15 October 2026, see the next entry).
- **Review working papers (2026).** `research/data/audit/valuable-questions-2026-09-14/research-primary.md`
  (§3, the conjecture) and `research-challenge.md` (P3, its rejection).
- **Discovery commit (2026).** Commit `0bdb172`, 17 August 2026, "PRD REJECTED 2026-08-12 -- found 5
  days late", with the matching `TASKS.md` entry.
- **Simulation records.** `research/data/simulations/SIM-2026-031.json`, `-061`, `-072`, `-073`,
  `-074`, `-075`, `-076`, `-077`, `-079`.
- **Hypothesis records.** `research/data/hypotheses/HYP-2026-006.json`, `-008`, `-032`.
