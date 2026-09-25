# What is worth attacking, given the instruments this project actually has

**Author:** primary researcher agent, team task 2026-09-14.
**Graded against:** `docs/governance/RESEARCH-DIRECTOR.md` sections 5, 6, 8, 12, 29, and
`docs/governance/AUDIT-2026-08-11.md`.
**Status of every proposal below:** unrun. Nothing here is a result.

## Summary (5 lines)

1. The audit's central finding is not that the project measured things badly. It is that the project
   has never once run the experiment its own standard names as the point of the program: hold
   ordinary conformal-field-theory accuracy fixed, vary the alleged geometry, and see whether
   anything measurable changes. That experiment is cheap, it fits chi <= 12 and L <= 24, and it
   returns a Level-4 answer whichever way it falls.
2. The second-best asset is the half-finished timelike-entanglement negative. A live holography claim
   in the literature meets an exact lattice symmetry that forbids it. Finishing and publishing that
   is the clearest public good this project can produce this year.
3. The third asset is a theorem attempt, not a simulation. Three independent stumbles in the record
   (l_AdS cancelling in Wang-He, the Synge distance being force-blind, l_AdS being a definition) all
   point at the same no-go, and a no-go here is Level 4 by the standard's own wording.
4. What governments and large institutions structurally do not fund is exactly what fits here:
   pre-registered negatives, replication of small claims, and running one question to the ground
   without a grant cycle. That is the honest public-value case, not a claim to scale.
5. What this project should stop doing is measuring quantities that conformal symmetry already fixes
   and then reading geometry into the agreement. Twenty-one of thirty-four calculated claims in the
   audit could not have come out otherwise.

---

## Ranking rationale

Proposals are ranked by achievable claim level, multiplied by the count of genuinely possible
outcomes, divided by cost and blocking risk, with a hard penalty for anything whose answer is fixed
in advance by conformal symmetry, a Virasoro identity, or a definition. Cost is quoted at RunPod
rates this project actually observed in September 2026: 0.24 USD per hour for an RTX 2000 Ada class
host, 0.28 per hour for the 16 vCPU host used by SIM-078, and roughly 1 USD per hour for anything
larger. The entire HYP-032 campaign cost about 6 USD. Compute is not the binding constraint here.
Attention is, and so is the discipline of not starting a fifth thing before the fourth is closed.

---

## 1. The matched non-geometric control: does anything geometric about MERA survive a control that is not geometric?

**Exact quantity.** Build three representations of the same critical Ising ground state at matched
variational accuracy and matched bond dimension. (a) The scale-invariant MERA that MERAKit already
optimizes. (b) A periodic uniform matrix product state at the bond dimension whose energy error
matches the MERA's to a stated tolerance. (c) A deliberately rewired hierarchical network: the same
tensor shapes and the same bond dimension, with the causal connectivity permuted, re-optimized to the
same energy tolerance. Evaluate on all three the geometric observables this project has actually
claimed: the interaction force profile F(dr) from SIM-011, the transport number T against
(pi/2) l_AdS from HYP-006, and the chord or Synge distance from HYP-026. Report one number per
observable, the separation ratio, meaning the spread across the three constructions divided by the
numerical uncertainty within a single construction.

**Killer test.** If the matched non-geometric controls reproduce every one of those observables
inside their own error bars, the geometric reading has no operational content in this setting. That
is section 12's emergent-geometry killer, stated in the standard's own words. If the MERA separates
from both controls on at least one observable that is not a restatement of a scaling dimension,
Hypothesis B survives its first genuine test.

**Genuinely possible outcomes: 4.** All three agree, so geometry is bookkeeping. The MERA separates
on everything, which is strong Hypothesis B. The MERA separates only on observables that reduce to
the transfer spectrum, which is the sharpest and most likely outcome and means geometry is a
relabelling. Or the controls cannot be matched at all, meaning no non-geometric ansatz reaches the
same accuracy at the same bond dimension, which is itself a result about representation efficiency.

**Claim level.** 4 in every branch. Section 5 lists "a no-go result proves that the geometric
interpretation has no independent observable content in the tested setting" as a Level-4 example, and
lists the separating observable as the other one.

**Instrument.** MERAKit.jl for (a) and (c). The existing puMPS code for (b). The existing
force-reanalysis driver for the F(dr) evaluation, so that the linear-space estimator defect recorded
in ERRATA E6 is not repeated. Nothing new has to be written except the rewiring, which is a
permutation of the isometry index assignment plus a re-optimization.

**Compute.** Local at chi = 6 for Ising. Roughly 20 to 40 USD on RunPod for chi = 8 to 12 across
three constructions with enough seeds to report the basin spread honestly, since this project's own
record shows a clean-basin rate of 2 in 6 at chi = 12.

**Who outside cares and why.** Everyone in the tensor-network holography argument: Swingle
(arXiv:0905.1317), the AdS/MERA consistency-condition line (Bao and collaborators, arXiv:1504.06632),
the kinematic-space reading (Czech and collaborators, arXiv:1512.01548, UNVERIFIED id), and the
holographic-code community descended from HaPPY (arXiv:1503.06237). Each asserts or disputes that
MERA carries geometry. The matched-control measurement that would adjudicate it has, as far as this
project's own audit established, never been run in this repository and, UNVERIFIED, may not have been
published anywhere. Run the section 8 literature gate before that clause leaves the file.

**Why an institution will not do it.** The likely branch has no positive headline. A postdoc who
spends six months showing that a fashionable interpretation adds nothing gets a null result and no
job talk. Someone with no grant cycle is the natural person to run it.

---

## 2. Finish the timelike entanglement negative and publish it as a registered negative

**Exact quantity.** The imaginary part of the timelike entanglement entropy of an interval in a
critical 1+1d lattice model, against the continuum claim Im S = pi c / 6 (Doi, Harper, Mollabashi,
Takayanagi and Taki, arXiv:2302.11695, a copy of which is already in `research/downloads/`, and the
earlier arXiv:2210.09457). SIM-076 and SIM-077 have already established that for the literal lattice
transition matrix the imaginary part is exactly zero by chiral symmetry, V H V dagger = -H, that none
of four registered regulated constructions produces pi c / 6, and that the real part reproduces the
continuum formula to 2 or 3 percent.

**What remains.** One open thread, C1 at h_z = 0.02 and delta = 5, which rises with system size to
0.28 but peaks in the field. The registered MPS follow-up at L = 32 to 128 with the existing complex
time MPO driver settles whether that rise approaches pi/12 or is a crossover artifact. Separately,
the G2 gate specification error found in SIM-078 has to be recorded in ERRATA as a post-hoc gate
amendment naming the specification error, per the plan of record, before any grid runs.

**Killer test.** If the C1 quantity converges to pi c / 6 as L grows with the regulator held fixed,
the negative collapses and the lattice does realize the continuum claim. If it saturates below,
drifts with the regulator, or fails the 5x background rule, the negative stands and becomes a clean
statement: no lattice construction in this registered class reproduces the universal imaginary part,
and the obstruction is a symmetry rather than a numerical limitation.

**Genuinely possible outcomes: 3.** Converges to pi c / 6. Converges to something else. Fails to
converge at all, which is informative given that the symmetry argument predicts exactly zero.

**Claim level.** 3, and a strong one. Section 5 names "a failure boundary of an accepted
correspondence" as a Level-3 example, and this is exactly that.

**Instrument.** `research/tools/timelike-ee/qw_tlee_mpo.py`, already validated to 1e-7 against exact
diagonalization at L = 12 and 14, and exact at L = 8 with chi = 256.

**Compute.** 5 to 15 USD. The entire campaign to date cost about 6.

**Who outside cares and why.** The timelike-entanglement and pseudo-entropy community, which is
active and growing, and anyone building lattice regulators for de Sitter holography. This is a live
claim from a well-known group, and a clean lattice obstruction gets cited for years if it is stated
honestly and defended.

**Why an institution will not do it.** Because the paper says a fashionable quantity does not exist
on the lattice. The group that published the original will not publish its obstruction, and no other
group gains by attacking a result they can simply decline to cite.

---

## 3. Attempt the no-go theorem: is every MERA geometric observable a function of the transfer spectrum?

**Exact statement to prove or refute.** For a scale-invariant MERA with bond dimension chi and
ascending superoperator eigenvalues lambda_i, conjecture that every quantity constructible from the
network's causal-cone graph distances and its tensors, and invariant under the network's internal
gauge freedom, is a function of the scaling dimensions Delta_i = -log_3 lambda_i alone, with chi
entering only through the truncation error. Corollary if true: l_AdS = 1 / ln chi carries no physical
information, because chi appears in no gauge-invariant observable except as an error scale.

**Why this is a bet worth placing rather than idle speculation.** The project has hit this wall three
times independently and never named it. The l_AdS dependence cancels inside Wang-He's own derivation,
per the audit's D-1 resolution box. The Synge distance of HYP-026 is geometric and force-blind. The
transport relation T = (pi/2) l_AdS rests on a definition of l_AdS rather than a measurement. Three
separate routes producing the same cancellation is what a theorem looks like before anyone writes it
down.

**Killer test.** Exhibit one gauge-invariant MERA observable that depends on network geometry and is
provably not a function of the scaling-dimension set. A single counterexample kills the theorem, and
is worth more than the theorem, because it is precisely the geometric observable the program has been
hunting since 2026.

**Genuinely possible outcomes: 3.** The theorem holds with a proof. A counterexample appears, which
hands the program its Level-4 positive observable. Or neither, meaning the statement is true for the
tested class but not provable in general, which is still a sharpening.

**Claim level.** 4 if proved, since a no-go of exactly this shape is the standard's own Level-4
example. 4 if refuted by counterexample. 2 if it lands as a restricted result.

**Instrument.** Analysis first, then MERAKit for small numerical checks that any candidate invariant
actually varies across gauge orbits. The numerical side is hours on a laptop.

**Compute.** Under 5 USD.

**Who outside cares and why.** The audience of proposal 1, plus the quantum-error-correction and
holography line (Harlow, arXiv:1607.03901), where the analogous question of what is gauge and what is
physical in a holographic code is taken seriously and is partly open.

**Why an institution will not do it.** It is a negative structural result about a framework many
people's grants describe positively. It is also too small to justify a postdoc and too large to do in
an afternoon, which is the exact size of problem that goes unclaimed.

---

## 4. Bulk operator recovery: does the causal cone or the minimal cut predict recoverability?

**Exact quantity.** Insert an operator on the internal legs of an optimized MERA at layer k and
horizontal position x. For a boundary region A, measure the recovery error, meaning the distance
between the exact reduced state with the insertion and the best state reconstructible by acting only
on A. Then compare that error against two competing predictors: containment of the insertion point in
the causal cone of A, and containment in the minimal-cut region of A. These two regions are not the
same in a MERA, and the disagreement between them is the whole content of the question. Report the
recovery error as a function of graph-geodesic separation from each boundary.

**Killer test.** If recovery error is predicted by causal-cone containment alone, with no residual
structure once the cone is accounted for, the entanglement-wedge reading of MERA fails and the
network is a circuit, not a geometry. If recovery tracks the minimal cut beyond what the cone
explains, that is an operational geometric property, and it is the first one this project would have.
Either way a gauge-transformation control is mandatory: apply a random unitary on the internal legs,
which leaves the boundary state exactly invariant, and re-measure. If apparent bulk locality moves,
it was gauge, which is section 12's reconstruction killer.

**Genuinely possible outcomes: 4.** Cone predicts. Cut predicts. Both fail and recovery is smooth in
graph distance with no sharp region structure. Or the whole pattern is destroyed by gauge, in which
case the answer is that the question was ill-posed and that itself is worth recording.

**Claim level.** 3 for the measurement, 4 if the gauge control separates cone from cut cleanly,
because that is an observable distinguishing a geometry-bearing network from a matched circuit.

**Instrument.** MERAKit.jl at chi = 6 to 8 on critical Ising, three to four layers, so an effective
boundary of 27 to 81 sites. Exact diagonalization is not needed. The reconstruction step is a small
convex problem per region.

**Compute.** 10 to 25 USD, dominated by seed count rather than by any single run.

**Who outside cares and why.** Holographic quantum error correction (arXiv:1503.06237,
arXiv:1607.03901), and the specific unresolved question of whether MERA's causal cone is too large to
support entanglement-wedge reconstruction, which is what the AdS/MERA consistency-condition paper
(arXiv:1504.06632) argues in the negative from general principles rather than from measurement.
Turning a principled argument into a measured curve is a real contribution.

**Why an institution will not do it.** Because the general argument is already believed, so the
measurement reads as confirmatory until it disagrees, and nobody funds a measurement whose expected
value is confirming what a 2015 paper said.

---

## 5. Defect response as an out-of-sample geometric prediction

**Exact quantity.** Introduce a marginal defect into the critical Ising chain by altering a single
bond coupling to J' = J(1 + g). The Ising defect line carries a continuously varying boundary exponent
as a function of g (Oshikawa and Affleck, arXiv:cond-mat/9612187, UNVERIFIED id), so the answer is
known exactly in the continuum and is not fixed by a single symmetry. Optimize a MERA on the defect
Hamiltonian. Then compute, from the network's geometry alone, the deficit-angle-like deformation of
the causal cone around the defect, and use it to predict the defect two-point exponent before
measuring that exponent from the transfer spectrum.

**Killer test.** Pre-register the geometric prediction with its uncertainty, then measure the exponent
from the spectrum. If the geometric route predicts the known exponent across a range of g with no
fitted parameter, Hypothesis B has its first out-of-sample success in the sense of section 18. If the
geometric route requires the answer as an input, or only works after fitting one constant per g, it
adds nothing and that must be said plainly.

**Genuinely possible outcomes: 3 or more.** Geometric prediction succeeds across g. It succeeds at
small g and fails as the defect strengthens, which would locate a failure boundary. It requires
fitting, meaning there was never a prediction.

**Claim level.** 3 if the exponent curve is reproduced by an independent route, 4 if the geometric
route and the spectral route can be shown to use genuinely disjoint inputs. The independence ledger
of section 7 has to be filled in before any claim, because the MERA was optimized on the defect
Hamiltonian and therefore knows the answer implicitly. State that risk in the pre-registration, not
after.

**Instrument.** MERAKit.jl with a modulated MERA, which requires breaking translation invariance in
one column of tensors. That is the main implementation cost and it is real, perhaps a week of work.

**Compute.** 30 to 60 USD, because inhomogeneous MERA optimization is slower and needs a g sweep.

**Who outside cares and why.** The defect and interface CFT community, and anyone claiming that
tensor-network geometry deforms predictively under perturbations. Section 11E of the standard names
this as a candidate test and notes correctly that a geometry claim gets much stronger when it predicts
a response that was not part of the calibration.

**Why an institution will not do it.** They might. This is the proposal on this list most likely to
already exist somewhere in partial form, so run the literature gate hard before committing a week to
the modulated optimizer.

---

## 6. Biorthogonal Koo-Saleur at a second non-unitary class, and the c = 0 indecomposability parameter

**Exact quantity.** The project's strongest instrument is the biorthogonal non-Hermitian Koo-Saleur
extraction that returned c = -4.29 plus or minus 0.15 at Yang-Lee against the true value -22/5,
excluding c_eff = +2/5. The audit denied it Level 3 on the literature gate and on the algebra being
forced, and the priority claim failed outright against prior art (arXiv:2602.02649 and PRL 119,
040601 per the memory record). What is not forced, and what no symmetry fixes, is the
indecomposability parameter b of a logarithmic c = 0 theory: the number that distinguishes percolation
from polymers where the central charge cannot, with competing values in the literature that are not
derivable from c (Dubail, Jacobsen and Saleur, arXiv:1008.1216, UNVERIFIED id; the c to 0 catastrophe
literature descending from Gurarie, UNVERIFIED). Measure b from the Koo-Saleur lattice Virasoro
generators rather than from the transfer-matrix route the existing measurements use.

**Killer test.** Before any new number, the pipeline must return the published b for one model where b
is agreed. If it cannot reproduce an agreed b, it cannot claim a new one. A second killer: if the
extracted b depends on the biorthogonal normalization convention, the result is a convention and not a
measurement, which is section 12's Yang-Lee method killer applied to a new quantity.

**Genuinely possible outcomes: high.** b is not fixed by symmetry, competing values exist, and the
question of whether the Koo-Saleur route even converges in a logarithmic theory where the dilatation
operator is non-diagonalizable is genuinely open. This is the highest counterfactual novelty on the
list.

**Claim level.** 2 for the method extension, 3 if b is extracted and matches an independent route, and
the honest ceiling is 3. This proposal does not touch the trunk question at all, which is why it is
ranked sixth despite being the most likely to produce a publishable paper.

**Instrument.** The existing `research/tools/yanglee-pt/` biorthogonal exact-diagonalization stack,
plus puMPS if sizes beyond L = 18 are needed. Logarithmic theories need a Jordan-block-aware
eigensolver, which is the main new code.

**Compute.** 15 to 40 USD.

**Who outside cares and why.** A small, serious and identifiable community: Saleur, Jacobsen, Vasseur,
Read and their students. That is a feature, not a bug. It is the one audience this project could
plausibly reach without an arXiv endorser, because the work speaks their language and they referee
each other's numerics closely.

**Why an institution will not do it.** They will, eventually, and better resourced. The window here is
narrow and the contribution is a cross-check rather than a discovery. Treat this as the Track A
credibility project, not as the groundbreaking one.

---

## 7. Reopen the force-exponent channel at sizes where an exponent can exist

**Exact quantity.** The retracted headline left a real measurement behind: alpha = 2.6 plus or minus
0.2, with six consecutive local log-slopes flat to 7.5 percent, matching neither 2 Delta_T = 4 nor
2 Delta_eps = 2. HYP-008 is closed as untestable at n <= 24 because the force is identically zero for
the Kramers-Wannier odd energy density at h = 1, and the local Hamiltonian density is
ultraviolet-dominated at those sizes. The question of what operator channel produces 2.6 is open and
unanswered. Attack it at L = 64 to 256 with matrix product states, where dr can range far enough for a
window to exist at all, using a probe that is not blind by symmetry.

**Killer test.** If the exponent drifts monotonically with L and shows no plateau over at least a
decade in dr, then no exponent exists and 2.6 was a crossover. Say so and close the channel for good.
If it stabilizes, identify the channel by matching to a scaling-dimension combination, and require the
match to survive the matched-control test of proposal 1 before any geometric language is used.

**Genuinely possible outcomes: 3.** No exponent, so the number was a crossover. An exponent matching a
known channel combination. An exponent matching nothing known, which would be the interesting branch
and would demand very careful handling given this project's history with exactly this number.

**Claim level.** 3 at best, 1 if it resolves to a crossover, and the crossover branch is still worth
publishing as the closure of the project's own retracted claim.

**Instrument.** The complex-time MPO driver generalizes to real-time and static MPS work, or a
standard density-matrix renormalization group implementation. This is the one proposal that needs a
tool the project does not already have in finished form.

**Compute.** 20 to 50 USD.

**Who outside cares and why.** Honestly, few people outside. This matters because it closes the
project's own open wound, and because leaving a retracted headline with an unexplained residual number
is exactly the state that produces the next overclaim. Rank it here for hygiene, not for impact.

**Why an institution will not do it.** Nobody outside this project has any reason to care what
happened to a number in a desk-rejected manuscript. That is precisely why it has to be this project
that closes it.

---

## 8. The meta-proposal: a registered-negative series, published whether or not anyone reads it

**Exact quantity.** Not a physical quantity. A publication format: a numbered series of short,
pre-registered, fully reproducible reports, each attacking one specific claim in the lattice and
holography literature, each with its gates registered before the run, each published with its data and
its drivers, and each published whether the result is positive, negative or void. HYP-032 is entry one
and is already 80 percent written. The alpha retraction is entry zero and is already published as
Zenodo v5.

**Killer test.** The format fails if a report's gates are amended after seeing results without the
amendment being recorded as such. That already nearly happened once, in SIM-078's G2 gate. The
discipline is the product, so a silent amendment destroys the entire value of the series.

**Genuinely possible outcomes: not applicable.** This is infrastructure, not a measurement, and it
should be labelled that way rather than dressed as a result.

**Claim level.** 0 by section 5, meaning framing rather than a result. It is on this list because the
question asked what would be valuable to people, and this is the honest answer to the part of the
question about what institutions structurally will not do.

**Instrument.** Zenodo, which already works and already holds a published correction, plus the
existing pre-registration habit, which is the genuinely unusual asset here. Publication routes are
otherwise blocked: no arXiv endorser, SciPost silent, PRD desk-rejected 2026-08-12. Zenodo with a
concept DOI and a public repository is the realistic channel, and it is sufficient for work that other
people can check.

**Compute.** Zero.

**Who outside cares and why.** Anyone who has ever tried and failed to reproduce a small numerical
claim in this field. The replication gap in computational physics is real and nobody is paid to close
it. A person with validated pipelines, no grant cycle and a written standard is unusually well placed
to produce a handful of these per year.

**Why an institution will not do it.** Because nothing in the academic reward structure pays for it.
This is the single clearest place where the structural gap named in the task is the actual value.

---

## What this project should NOT do

These are drawn from the project's own record, not from general advice.

**Do not measure another quantity that conformal symmetry already fixes.** The audit found that 21 of
34 calculated claims could not have come out otherwise. C_TTT equal to 2 sqrt 2 over sqrt c is a
literal line of code in three drivers. Delta_T equals 2 is a Virasoro theorem. Quoting C_TTT rather
than c halved the apparent error. Before any run, write down the number of genuinely possible
outcomes, and if the answer is one, do not run it.

**Do not treat agreement between quantities derived from the same inputs as evidence.** Section 7
exists because of this, and the most expensive instance was not in the physics. Three internal records
agreed that a manuscript was with editors for 11 days after it had been rejected, because all three
came from one lookup on one day. Same-origin agreement is a consistency check.

**Do not start a new hypothesis while an old one sits at a failed gate.** There are 33 hypothesis
records. Two are refuted with high confidence and useful, most sit at proposed with low confidence and
have never been touched. HYP-032 is stopped at a failed gate right now, waiting on a decision. The
program's failure mode is starting, not finishing.

**Do not use geometric language for a quantity before the matched control has run.** Every geometric
claim in this repository was made without one. That is the single structural defect that produced the
retraction, and proposal 1 exists to fix it at the root rather than per-claim.

**Do not build a new pipeline when an existing one can be pointed at the question.** MERAKit, puMPS,
the biorthogonal exact-diagonalization stack and the complex-time MPO driver are all validated against
known results. Six of the eight proposals above need no new instrument. The two that do, proposals 5
and 7, are ranked below the six that do not, for that reason.

**Do not report the status of anything external from an internal note.** Journal decisions, portal
states, email replies and remote job states get checked against the source in the same session they
are reported. This is already a project rule, written after a real miss.

**Do not pursue the hardware and instrumentation hypotheses.** HYP-018, 019 and 020 propose Rydberg
vapour cells, optically pumped magnetometers and a 50,000 USD instrument budget. They are not
supported by any instrument this project has, they do not orbit the trunk question, and they are the
clearest example of what section 29 calls expanding the agent count without expanding the evidence.

**Do not chase publication venues before there is a Level-3 or Level-4 result to publish.** All
conventional routes are currently blocked and the batch of seven outreach emails returned zero
replies. The binding constraint is not distribution. It is that, by the project's own audit, there is
not yet a result that clears the bar. Fix that first, and the venue problem changes shape.
