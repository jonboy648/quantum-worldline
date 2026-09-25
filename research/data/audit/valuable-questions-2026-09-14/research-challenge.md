# Adversarial challenge to the three valuable-questions reports

**Author:** challenger agent, team task 2026-09-14.
**Read in full:** `research-primary.md`, `research-alt.md`, `research-practical.md`,
`docs/governance/RESEARCH-DIRECTOR.md` sections 5, 6, 7, 8, 12, 16, 19, 29, 33, 34,
`docs/governance/AUDIT-2026-08-11.md` sections 1 and 2, `research/ERRATA.md` lines 1-120.
**External lookups run this session:** JOSS submission docs, arXiv blog 2026-01-21, SciPost
Physics Codebases about page, four literature searches. Everything else is marked UNVERIFIED.

## Verdict (5 lines)

1. The single highest-ranked physics proposal in the whole set, the matched non-geometric control,
   is **killed as specified**. All three observables it names are functionals of the exact state,
   computed by drivers that never touch a network. A representation control on a state functional
   cannot separate representations. This is the SIM-074 failure mode one level up.
2. The no-go theorem is **pre-empted and, as literally stated, already refuted by this project's own
   data**. Milsted and Vidal settled MERA's geometry in 2018, and the project's own measured OPE
   coefficient is a gauge-invariant network number that scaling dimensions do not fix.
3. The timelike-entanglement negative **survives**, but at Level 2-3 and with a narrower claim than
   primary #2 writes. It bounds a class of lattice regulators, not a continuum result.
4. The instrument release **survives, weakened**: JOSS is shut for six months by a verified rule,
   SciPost Codebases wants a library and this is a driver script, and the novelty claim is unrun.
5. On the framing: **no proposal in any report meets "beneficial to the human race, something
   governments cannot answer."** Two meet a real and much smaller bar. Jon should hear the smaller
   bar stated plainly rather than the larger one hedged.

---

## 0. The defect that runs through the top of every list

`RESEARCH-DIRECTOR.md` section 34 asks, for every proposed geometric quantity, whether it is a
property of the represented state or of the representation. None of the three reports applies that
test to the observables they propose to control. I applied it. Here is what the drivers do.

**F(dr).** `research/data/simulations/interaction_energy_24q.py:1-24` computes
`F(dr) = E_dual - E_0 - 2(E_single - E_0)` from `sigma_j |GS>` on the **exact** 24-qubit TFIM
ground state, built as a `LinearOperator` at `interaction_energy_24q.py:56-60`. Grepping the file
for `mera`, `chi` or `ansatz` returns **nothing**. There is no tensor network anywhere in it.

**Transport T.** `research/data/simulations/holographic_transport_16q.py:347` prints the literal
string `Skipping full MERA bulk computation (complex to implement correctly)`, and the two lines
above it say the bulk part "requires the full MERA U". What is saved is the boundary excitation
density from exact time evolution. The audit records this as D-12 and memory already flags it.

**Synge / chord distance.** `HYP-2026-026.json` `result_note_2026_06_08_sim031` records
`kappa(16q exact, chord-corrected) = 0.2429`, measured on **exact 16q connected ZZ correlators**
after the feasibility gate ruled the on-disk MERA correlators pathological.

**The force re-analysis driver cannot help.** `research/tools/force-reanalysis/qw_alpha_reanalysis.py:43`
opens `SIM-2026-011-interaction.json` and fits the stored array. It is an estimator, not an
evaluator. It cannot be pointed at a new state.

So the project's three flagship "geometric" observables are three exact-state functionals. Two
consequences, and both are load-bearing for everything below.

- **A matched-control experiment on them is guaranteed to pass.** Any ansatz matched on state
  accuracy reproduces a state functional to that accuracy. The "separation ratio" primary #1 defines
  at `research-primary.md:51-53` measures representation error and nothing else. Its outcome is
  fixed before the run, which is section 6 counterfactual novelty **near zero**, the exact category
  primary #1 tells the project to avoid at `research-primary.md:390-394`.
- **The geometric readings were never measurements of geometry in the first place.** They were
  measurements of the state, relabelled. That is a sharper statement than the audit's and it is
  available for free from files already on disk.

---

## 1. Per-proposal challenges

### P1. Matched non-geometric control (`research-primary.md:42-90`) : **KILLED as specified, rebuildable**

**Claim level check.** Primary claims "4 in every branch" (`research-primary.md:67-70`). False for
three of its four branches. Section 5's Level-4 example requires "an observable **differs** between
a geometry-bearing MERA and a non-geometric ansatz matched on ordinary CFT observables". Agreement
on a state functional is not that observable; it is a restatement that both ansaetze represent the
same state. Branches 1 and 3 are Level 1. Branch 4, "the controls cannot be matched at all", is a
representation-efficiency result and is Level 2. Only branch 2 would be Level 4, and section 0
shows it cannot occur for these three observables.

**Outcome count check.** Stated 4 (`research-primary.md:61-66`). Honest count for F(dr), transport
and chord distance: **1**, up to representation error. The only genuine degrees of freedom are
whether puMPS at matched bond dimension reaches the MERA's energy and whether a rewired network
re-optimizes at all. Those are worth knowing and they are not geometry.

**Killer test check.** The registered killer at `research-primary.md:54-59` is
**representation-vacuous**: it is pre-destined to fire in the negative direction, exactly as
SIM-074's test was pre-destined to fire in the positive one. Different sign, same defect.

**Instrument check : the report's own claim is wrong.** `research-primary.md:73-74` says "Nothing
new has to be written except the rewiring." What actually has to be written: a routine to evaluate
F(dr) on a network state, because the existing one takes a dense exact vector; a transport
evaluation that applies a MERA, because the only one in the repo skips it; a network-state chord
distance; and the rewiring plus re-optimization. That is most of an instrument, not a permutation.

**What survives and should be built instead.** The rewiring arm (c) is the good idea in this
proposal and it is section 11H of the standard. Keep it. Point it at observables that are
**defined on the network's internal legs**, where a control can separate: causal-cone versus
minimal-cut structure, recovery error, gauge-orbit variation. That is proposal P4, which primary
ranked fourth. **P4 should be ranked first, and P1 folded into it as its control arm.**

### P2. Finish the timelike-entanglement negative (`research-primary.md:94-134`) : **SURVIVES, claim narrowed**

**Claim level check.** Primary says "3, and a strong one", citing section 5's "failure boundary of
an accepted correspondence" (`research-primary.md:119-120`). The project's own record disagrees
with the strength. `SIM-2026-077.json` `key_findings[1]` states the result as "the imaginary part
... is, on the critical TFIM lattice, a property of the continuum analytic continuation and **not of
any lattice transition matrix examined here**", and `claim_level` in that same file reads "Level 3
negative **within the registered scope** (four constructions, sizes as run). Not a theorem about all
lattice constructions." A continuum quantity that a particular lattice regulator fails to reproduce
is ordinarily a statement about the regulator. Primary's line 16, "a live holography claim in the
literature meets an exact lattice symmetry that forbids it", overstates what the file says. Alt's
hedged "arguably" at `research-alt.md:67` is the honest version.

**Outcome count check.** Stated 3 (`research-primary.md:116-117`); fair for the C1 thread.

**Killer test check.** Real and not symmetry-vacuous. C1 is measured on a symmetry-**broken**
Hamiltonian (`h_z = 0.02`), so the chiral argument that forces zero does not apply by construction.
This is the one killer in the primary report that could genuinely go either way.

**Unflagged risk.** `SIM-2026-077.json` `key_findings[2]` already says "One size-and-setting point
lands within 10 percent of pi/12; the same setting at the other sizes does not." A single point
near the target with no size trend is the shape of the alpha = 3.92 error. The C1 follow-up needs a
plateau condition registered in advance, not a target value to approach.

**Verdict: survives.** Best physics item in the three reports, at Level 2 to 3, and it closes a
thread rather than opening one.

### P3. No-go theorem, MERA observables as functions of scaling dimensions (`research-primary.md:138-177`) : **KILLED**

Three independent kills.

**Kill 1, the project's own data refutes the conjecture as stated.** The conjecture
(`research-primary.md:141-146`) says every gauge-invariant quantity built from the network and its
tensors is a function of the scaling dimensions alone. The project measured `C_sigma_sigma_eps` =
0.5075 from a MERA in SIM-2026-061 (audit section 2.4, CLM-023). An OPE coefficient is
gauge-invariant and is **not** determined by the scaling-dimension set. The counterexample the
proposal offers a Level-4 prize for is already on disk, and it is not a geometric observable, so it
wins nothing. To survive, the conjecture would have to be narrowed to "quantities built only from
causal-cone graph distances", at which point it is close to true by inspection and Level 1-2.

**Kill 2, prior art. VERIFIED this session.** Milsted and Vidal, arXiv:1812.00529, "Geometric
interpretation of the multi-scale entanglement renormalization ansatz", give MERA a rigorous
geometry via path-integral geometry and conclude it is a **light cone or light sheet**, describing
**neither the hyperbolic plane nor de Sitter spacetime**. The geometry is fixed by the CFT path
integral, which is the content the proposal wants to prove. Bao, Cao, Carroll, Chatwin-Davies,
Hunter-Jones, Pollack and Remmen, arXiv:1504.06632 (Phys. Rev. D 91, 125036), had already derived
necessary conditions for an AdS/MERA correspondence and argued against the naive AdS-slice reading.
Both IDs verified. Czech and collaborators on kinematic space point the same way, **UNVERIFIED**.
This is a folk theorem with two published anchors, not an unclaimed result.

**Kill 3, the corollary is a definition, not a theorem.** That l_AdS = 1/ln chi carries no physical
information (`research-primary.md:145-147`) is already the audit's finding: the definition "fixed
the answer before the run" (AUDIT section 1), and the D-1 resolution box records that l_AdS cancels
inside Wang-He's own derivation. Proving a definition carries no information is Level 0.

**What survives.** One sentence for the governance file: the project's three stumbles all reduce to
section 34, state property versus representation property, and the literature settled the geometry
question in 2018 against the reading the project inherited. That belongs in `ERRATA.md` and in the
next session note. It is not a paper.

### A1. Release the complex-time MPO as a tested instrument (`research-alt.md:260-283`) : **SURVIVES, badly weakened on venue and novelty**

**Is it novel enough? Harsh answer: the numerics are not, the packaging might be.** Complex-time
MPO evolution is imaginary-time and real-time evolution with one complex coefficient. TeNPy, ITensor
and quimb all do TEBD and MPO time evolution, and setting the step complex is a parameter change,
not a new method (**UNVERIFIED** as to whether each library exposes it directly; the burden is on
the proposal to show it does not). Alt's own wording at `research-alt.md:271` concedes the gate has
not run: "as far as I can tell (**UNVERIFIED**; needs a section 8 gate against TeNPy, quimb,
ITensor and the pseudo-entropy literature)". Under section 8 that is not a novelty claim yet.

**What would actually be new, stated precisely so it can be checked.** Not the evolution. Three
things: the **branch convention** for the logarithm of a non-positive transition matrix, which
`SIM-2026-076.json` `key_findings[5]` records as an O(1) ambiguity any lattice claim must state;
the **chiral-symmetry exact-zero test** as an executable assertion; and the validation ladder at
1e-7 against exact diagonalization. That is a correctness harness, a real but small contribution.
The write-up should say "reference implementation and branch-convention discipline", not
"instrument".

**Venue check, and this is the weakening.** **VERIFIED this session** against the JOSS submission
docs: "The repository must have been public for more than six months prior to submission, with
active development spanning that period", plus "at least six months of public history ... with
evidence of releases, public issues and pull requests". The repo went **private** on 2026-09-07
(`ERRATA.md` current-status block), so JOSS is shut until at least March 2027, and only if the repo
goes public now. Practical has this right at `research-practical.md:219`; alt lists JOSS as "No,
high confidence" at `research-alt.md:74` and ranks the route **first, "Do this first"** at
`research-alt.md:433-436`. **Alt's top recommendation is blocked for six months and the report does
not know it.**

**SciPost Codebases, verified this session:** acceptance requires benchmarking tests, one example
application presented in detail, and high-level programming standards throughout; arXiv is
encouraged, not required; published examples are libraries, NetKet, HEJ, QDFlow, LEMONS. What exists
is `research/tools/timelike-ee/qw_tlee_mpo.py` at 27 KB plus two runner scripts, one experiment's
driver. Plausible only after it is generalized into something a second person would import. And the
SciPost account has been unapproved since 2026-04-30 and never re-checked
(`research-practical.md:336-339`), which is exactly the external status the 2026-08-23 rule says
must be refreshed in session before it is planned against.

**Verdict: survives as the best non-physics deliverable, but it is a 2027 JOSS item or a
generalize-first SciPost item, not a "do this first" that lands this quarter.**

### A2. Metascience paper on two pre-registration failure modes (`research-alt.md:82-113`) : **WEAKENED to a governance paragraph**

**Is "symmetry-vacuous test" unnamed? Largely no, under other names.** The requirement that a test
be capable of distinguishing the alternatives is old and named. In clinical trials it is **assay
sensitivity**, formalized in ICH E10 as a trial's ability to distinguish an effective treatment from
an ineffective one. In error statistics it is Deborah Mayo's **severity requirement**: a claim
passes severely only if the test would very probably have detected the flaw had it been present, so
a zero-severity test is exactly a vacuous one. **Positive control** and **manipulation check** are
the bench and psychology names for the same guard. All four are **UNVERIFIED** against primary
sources; a targeted search for the specific pairing returned nothing, which is weak evidence of an
unfilled niche and is not the section 8 gate.

The **unsatisfiable-bar** mode is less novel still: a threshold the chosen method cannot reach at
the reachable sizes is a power and feasibility failure, which is what pilot runs and power analyses
exist to catch. SIM-078's G2 is a textbook instance, well executed, not a new category.

**What might genuinely be new.** The mechanism, not the category: in an exactly symmetric system the
vacuity is **algebraic and provable in advance**, so a pre-flight step exists that has no analogue in
psychology, namely prove the two registered probes are not related by a symmetry of the model at the
registered parameter point. That is a concrete, checkable procedure and it is one paragraph.

**Who referees it? Nobody obvious, and that is a real problem.** Alt does not name a referee pool.
Metascience venues referee psychology and biomedicine; a physics methods referee will call it
housekeeping. Alt's own killer at `research-alt.md:112-113` already says the output collapses to one
governance paragraph if the gate finds prior art. **The gate has now partly fired. Take the
paragraph.** Write it into `RESEARCH-DIRECTOR.md` as a mandatory pre-flight and move on.

### A3. Pseudo-entropy reality structure (`research-alt.md:298-328`) : **WEAKENED hard by prior art**

Alt calls this the best physics candidate and asks whether there is a symmetry criterion that
decides in advance when the imaginary part vanishes (`research-alt.md:303-305`).

**That criterion is published.** arXiv:2209.07308, "Constructible reality condition of pseudo
entropy via pseudo-Hermiticity", formulates exactly that reality condition: if M-dagger equals
eta M eta-inverse for invertible Hermitian eta, the reduced transition matrix's eigenvalues are real
or come in conjugate pairs and the pseudo entropy is real. arXiv:2311.01045 extends
pseudo-Hermiticity and pseudo entropy to quantum field theories. Abstracts read this session, full
texts **UNVERIFIED**.

The project's own result, chiral symmetry forcing Im S = 0 on the critical TFIM
(`SIM-2026-076.json` `key_findings[2]`), is very plausibly an instance of that condition rather than
a seed theorem. Alt's registered killer at `research-alt.md:327-328` fires on exactly this: the
criterion following from the standard non-Hermitian symmetry classification makes the result a
restatement, stopping under section 31. Credit where due, alt marked the prior-art risk moderate to
high and demanded the gate first. The gate says stop, or narrows the deliverable to the TFIM case
worked as an instance of a known condition, which is Level 1.

### A4. Philosophy-of-physics route for the trunk question (`research-alt.md:224-240`) : **SURVIVES, and is the sleeper**

The claim level is stated honestly: "Level 3 as an argued no-go, Level 4 only if the matched control
from the primary report's proposal 1 runs and feeds it" (`research-alt.md:238-240`). Given section 0,
the matched control as designed will not feed it, so the ceiling is a position paper with one worked
example, which alt says outright. PhilSci-Archive has no gate, and an author who operationalized a
criterion, registered it, ran it and published the negative is genuinely unusual for that audience.
This is the one proposal whose claimed audience, claimed level and available evidence all match.
Two outcomes, honestly counted. **Survives intact.**

### P4. Bulk operator recovery, cone versus cut (`research-primary.md:181-221`) : **SURVIVES the level check, killer needs repair**

This is the strongest physics proposal in any of the three reports and it is ranked fourth. Recovery
error from an insertion on **internal legs** is a representation property, so unlike P1 it can
separate. Level 3 for the measurement is right, and Level 4 is reachable if the gauge control is
built correctly.

**The killer as written is broken and would fire every time.** `research-primary.md:196-199` says:
apply a random unitary on the internal legs, re-measure, and if apparent bulk locality moves it was
gauge. A gauge transformation on a bond maps an inserted operator O to U O U-dagger. The recovery
error of a **fixed** O therefore changes by construction, so the control is guaranteed to fire and
proves nothing. The well-posed version measures a gauge-covariant object: the recovery error
profile over the **whole operator algebra** supported at that bulk location, for example its maximum
or its average over a unitary 2-design, which is invariant. Register that version, or the experiment
reproduces SIM-074 with the sign flipped.

**Outcome count.** Stated 4 (`research-primary.md:199-201`); honest after the killer is repaired.

### P5-P8 and the remaining alt and practical items, briefly

- **P5 defect response** (`research-primary.md:224-263`). Level and independence risk stated
  correctly, including that the MERA is optimized on the defect Hamiltonian and so knows the answer.
  Survives; needs a modulated MERA and a literature gate before the optimizer.
- **P6 indecomposability parameter b** (`research-primary.md:266-306`). **Survives.** Honestly
  capped at Level 3, highest counterfactual novelty on primary's list, and the Yang-Lee conditioning
  wall at `research-alt.md:360-364` does not bind because the probe table needs no larger L.
- **P7 reopen the force channel at L = 64 to 256** (`research-primary.md:311-344`). Survives as
  hygiene at Level 1 to 3, correctly ranked low. Needs a tool the project does not have.
- **P8 registered-negative series** (`research-primary.md:348-383`). Alt's rebuttal at
  `research-alt.md:59-68` is correct: refuting your own unpublished claim is not a citable event.
- **B.1 CFT-calibrated hardware benchmark** (`research-alt.md:146-164`). Underrated by everyone.
  Three genuine outcomes, Level 2 with a Level-3 path, an audience the project's records already
  name, and no arXiv requirement.
- **B.3 error correction** (`research-alt.md:178-183`). Alt says the angle is empty and refuses to
  manufacture it. Correct, and worth crediting explicitly.

---

## 2. Is the Level-4 control blocked by scale, or by incentives, or by neither?

The brief asks which of alt and practical is right. **Neither is.** Alt says the experiment "is
blocked by scale, not incentives" (`research-alt.md:426-427`). Practical says compute is free
(`research-practical.md:11-14`). Primary says it fits chi <= 12 and L <= 24 for 20 to 40 USD
(`research-primary.md:76-78`).

**Practical is right about compute and alt is wrong about scale.** A chi = 12 MERA at 16 seeds cost
4 USD for 4 hours in SIM-2026-066 (`research-practical.md:67`); a 24-site exact ground state takes
325 seconds locally (`research-practical.md:43`). Nothing proposed is large.

**But the experiment is still not runnable, for a reason none of the three names:** the observables
do not exist. Section 0 shows F(dr), transport and the chord distance are exact-state functionals
whose drivers contain no network, and that `qw_alpha_reanalysis.py:43` is a fitter over a stored
array. Checking `research/tools/` this session: MERAKit.jl and its tracked mirror `merakit-setup/`
hold OPE, C_TTT, Potts, TCI and blocking drivers and **no** rewiring, bulk-insertion,
reconstruction or gauge-orbit driver; `grep -ril "rewir" research/` still returns nothing, as the
audit found in August.

**The honest answer is: blocked by observable design, which is two to four weeks of Jon's attention
and near-zero dollars.** That matches practical's E.3 build phase (`research-practical.md:288-290`)
and contradicts its own framing that distribution is the wall. Here the wall is neither money nor
readers. Nobody has yet written down a quantity that could tell the two hypotheses apart.

---

## 3. The distribution analysis (`research-practical.md:182-232`)

**Accurate on the two facts that matter, and I verified both.**

- The arXiv change is real. The arXiv blog post dated **2026-01-21**, "Attention Authors: updated
  endorsement policy", confirms that institutional email addresses are no longer accepted as the
  sole qualifier for new authors, extended to all sections from that date after a Mathematics-only
  trial announced 2025-12-10. Practical's date and substance are correct.
- The JOSS six-month public-history rule is real and is quoted above. Practical is correct and alt
  is wrong.

**Routes practical missed or understated.**

- **PhilSci-Archive**, which alt names at `research-alt.md:77` and practical's table omits entirely.
  It has no gate, it is indexed, and it is the natural home for the trunk-question paper.
- **ReScience C** is in practical's table at one line (`research-practical.md:220`) and deserves
  more weight: the project has a clean reproduction already banked, PAPER-133 at 0.01 percent
  (SIM-2026-070), which the audit calls "the cleanest record in the program".
- **Direct correspondence with the people who would referee this anyway.** The 2026-07 batch of
  seven got zero replies, but a message attached to a released instrument or a reproduction is a
  different message from one attached to an unendorsed manuscript.

**Is 75 views a meaningful signal? Mostly no, and practical half-says so.** It is a lifetime
concept-level count across five versions of a record never announced anywhere with an audience,
from a repository private since 2026-09-07. It measures the absence of a distribution attempt, not
the reception of the work. Practical's own line at `research-practical.md:197-198`, "some of whom
are Jon and the crawlers", is the right reading and should not be inflated into a verdict on the
science.

---

## 4. Cross-report contradictions

| # | Subject | Primary | Alt | Practical | Adjudication |
|---|---|---|---|---|---|
| 1 | Hypothesis records on disk | 33 (`:401`) | 32 (`:248`) | not stated | **Alt right.** `ls research/data/hypotheses/HYP-*.json` returns **32** this session. |
| 2 | SIM records | not stated | not stated | 78 (`:270`) | **Practical off by one.** `ls research/data/simulations/SIM-*.json` returns **79**. Immaterial to the argument. |
| 3 | Cost of the HYP-032 campaign | about 6 USD (`:37`, `:125`) | about six dollars (`:396`) | internal 7 USD vs billing 9.37 USD, upper bound (`:246`) | **Practical right, and it is the only one that checked billing.** Only pod `fiip7fruevt6e3` at 0.3213 USD is provably this project's; the rest of 9.37 is unattributed. The 6 USD figure is self-reported at pod-create price. |
| 4 | Is distribution the binding constraint? | No, the missing result is (`:425-427`) | Implicitly yes, all five recommendations are venue-shaped | Yes, explicitly (`:18`) | **Both, for different outputs.** For a Level-4 physics result primary is right: there is nothing to distribute. For the instrument, the reproduction and the philosophy paper, practical is right: the artifact exists and the door is shut. Stated as one global fact, each report is wrong half the time. |
| 5 | Is the Level-4 control blocked by scale? | No, 20-40 USD (`:76-78`) | Yes, blocked by scale (`:426-427`) | No, compute is free (`:11`) | **Primary and practical right on scale, alt wrong. All three wrong on the cause.** See section 2: blocked by observable design. |
| 6 | JOSS accessibility | not discussed | No endorser needed, high confidence (`:74`), ranked first (`:433`) | Six months public history, repo has zero days (`:219`) | **Practical right, verified.** Alt's top-ranked recommendation is blocked until at least 2027-03. |
| 7 | Zenodo v5 publication date | not stated | not stated | 2026-09-06 (`:191`) | **Cannot be determined here.** `ERRATA.md` and memory say 2026-09-07. Practical queried the live API, which under the 2026-08-23 rule outranks internal notes, but the two may be version-created versus published. One lookup settles it. |
| 8 | Value of a registered-negative series | Proposal 8, worth doing (`:348`) | Explicitly not recommended (`:458-459`) | not addressed | **Alt right.** Most claims refuted are the project's own, and an unpublished claim's refutation is not a citable event. Primary itself grades it Level 0. |
| 9 | Strength of the timelike-EE negative | "clearest public good this project can produce this year" (`:16-17`) | "arguably" refutes an external claim (`:67`) | not addressed | **Alt right.** `SIM-2026-077.json` `claim_level` says "Level 3 negative within the registered scope ... Not a theorem about all lattice constructions." |
| 10 | Pre-registration discipline | discipline is the product (`:360-362`) | hashes prove registration preceded code (`:46`) | the G2 smoke test was committed after the pod failed (`:244`) | **Not a contradiction, but practical is the one that checked.** Both things are true: registration preceded code, and the feasibility check that would have saved the run came afterwards. |

---

## 5. Framing verdict: does anything here meet "valuable to the human race, something governments cannot answer"?

**No. Not one proposal in the three reports meets that bar, and the reports know it.** Each of them
reaches for a smaller honest claim in its closing pages and then lets the brief's language sit at
the top unchallenged. I am saying it plainly because the brief asked me to.

**What the bar would require.** A result that changes what someone outside this subfield does.
Nothing proposed here does that. The best case in the whole set, the bulk-recovery measurement
(P4), would tell perhaps a few hundred people working on tensor networks and holography whether
MERA's causal cone or its minimal cut predicts recoverability. That is a real contribution to a
real question. It is not a contribution to the human race, and calling it one is the same move that
produced alpha = 3.92.

**What is actually true, and it is not nothing.**

1. **This project's value is bounded to a small corner of lattice conformal field theory, plus one
   genuinely unusual process record.** The audit already said the physics ceiling: no Level-4
   content anywhere, no Level-3 claim surviving its gate, 21 of 34 calculated claims fixed before
   the run. Nothing in these three reports moves that ceiling, and two of the three top proposals
   move it downward once challenged.
2. **The "governments cannot answer this" claim is false as stated and true in one narrow
   mechanical sense.** Governments and institutions can answer every question in these reports, and
   better resourced. What they structurally will not do is fund a six-dollar negative, or pay the
   career cost of retracting a headline. Alt's section F states this correctly as mechanisms rather
   than slogans, including the reverse entry at `research-alt.md:424-427` admitting what an
   institution can do that this project cannot. That section is the most honest page in the set.
3. **The scarce artifact is the retraction, not the physics.** A dated, public, self-executed
   withdrawal of one's own headline, with the estimator matrix that caused it, published as Zenodo
   v5 on a concept DOI. That is rare and it is checkable. It is worth more than any of the eight
   physics proposals, and it is already done.

**What I would tell Jon, in one paragraph.** Two things here are worth the next quarter. The first
is P4, the bulk-recovery measurement, rebuilt with a gauge-covariant killer and with P1's rewiring
folded in as its control, because it is the only proposal in the set that measures a property of the
representation rather than of the state, and therefore the only one that could produce a Level-4
answer. The second is the philosophy-of-physics paper on the trunk question, because it is the only
route where the claim level, the evidence and the audience already match, and PhilSci-Archive has no
gate to pass. Everything else is either pre-empted by literature nobody checked, blocked by a
six-month clock nobody read, or measuring a number that could not have come out otherwise.

---

## 6. What I could not verify

- Full texts of arXiv:2209.07308, arXiv:2311.01045, arXiv:1812.00529 and arXiv:1504.06632. Titles,
  authors and abstract substance confirmed by search; the claim that 2209.07308 subsumes the
  project's chiral-symmetry result is my reading of its abstract and is **UNVERIFIED**.
- Whether TeNPy, ITensor or quimb expose complex-time MPO evolution directly. **UNVERIFIED.** That
  section 8 gate is owed by the proposal, not by me.
- Whether "symmetry-vacuous test" is named in metascience. One search returned nothing specific;
  assay sensitivity, severity, positive control and manipulation check are from memory, **UNVERIFIED**.
- The SciPost account state, unchecked since 2026-04-30; the Zenodo v5 date in contradiction 7; and
  Czech and collaborators on kinematic space, cited from memory only.
