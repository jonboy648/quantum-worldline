# Alternative perspectives: what is worth attacking, from the angles a physics-first reading misses

**Author role:** alternative-perspectives researcher. **Date:** 2026-09-14.
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` sections 5, 6, 7, 8, 12, 29.
**Companion:** `research-primary.md` in this directory, which covers the physics-experiment menu.
Where I disagree with it I say so explicitly (section A.2 against its proposal 8).

---

## Summary (5 lines)

1. The project's most transferable asset is not a number. It is a dated corpus of research
   self-correction, and it contains at least two failure modes that the pre-registration literature
   does not name, because its subject matter has no exact symmetries and physics does.
2. The highest-value product available right now is an instrument, not a result: an exact
   complex-time transition-matrix entropy implementation, already validated to 1e-7 against exact
   diagonalisation, in a corner with many papers and no tested public reference code.
3. The best genuinely open small physics question in reach is the reality structure of
   pseudo-entropy on the lattice, which reuses the SIM-076 and SIM-077 machinery unchanged.
4. The story chapters are already the best artifact the project produced in 2026, and the trunk
   question of section 29 is publishable in philosophy of physics where it is not in Physical Review.
5. Every publication route that has failed so far required an endorser or an institution. Every
   route recommended here does not.

---

## Verification status of this document

- Verified against `research/data/papers/*.json` in this session: **2302.11695** (Doi et al.,
  "Timelike entanglement entropy", PAPER-2026-139), **2210.09457** (PAPER-2026-140), **2210.03134**
  (PAPER-2026-141), plus **2603.07639** and **2606.16785**. **2602.02649** is cited in project
  records with no PAPER record, a known catalogue debt.
- arXiv IDs cited from my own knowledge **could not be verified in this session**: the export API
  returned HTTP 429 on three spaced attempts, consistent with the burst-block gotcha in `CLAUDE.md`.
  Every such ID is marked **UNVERIFIED**. Do not quote one without a lookup.
- No venue or journal claim was checked against a live page. All are **needs one lookup**, which is
  what the 2026-08-23 external-status rule requires.

---

## A. Method and process as the product

### A.1 What the project actually has, read as an artifact rather than as physics

- Pre-registrations committed **before** driver code, with hashes proving the order
  (`PREREGISTRATION-HYP032-B.md` at `4743b8c`, driver `qw_tlee_mpo.py` at `a2bff9a`).
- A gate that fired and stopped a paid run: SIM-2026-078 G2 failed, the runner refused the grid.
- A retraction of the project's own headline executed into the public record (Zenodo v5, DOI
  10.5281/zenodo.22080720), including that the published value was the maximum of all 15 defensible
  estimator and window choices.
- An additive errata register that forbids silently rewriting history, with an entry (D9) correcting
  a summary that restated itself rather than its data.
- A 23-agent adversarial audit finding no Level-4 content anywhere, whose own D-1 was later found
  wrong and carries a correction box rather than an edit.

That is a longitudinal record of how a research program fails and catches itself, timestamped, run
by one person at roughly six dollars of compute per experiment.

### A.2 The honest answer on whether physics values this, and where I disagree with the primary

**Mostly no.** Physics has no functioning negative-results venue with readership. The primary
report's proposal 8, a registered-negative series published whether or not anyone reads it, is right
about the discipline and wrong about the destination. A series is a bad citation bet for a specific
reason: most claims being refuted are the project's own, and refuting your own unpublished claim is
not a citable event. Where the project refutes an **external** claim, as SIM-076 arguably does for
the imaginary part of timelike entanglement entropy, the format is a short paper on that claim, not
a series. The same content redirected to metascience, instrument and philosophy venues does have
readers. All **needs one lookup**:

| Venue | What it takes | Endorser or affiliation needed |
|---|---|---|
| ReScience C | Replications of computational results | No, high confidence |
| SciPost Physics Codebases | Software with a physics use case | No, but the SciPost account is already a project blocker |
| Journal of Open Source Software | Research software of scholarly substance | No, high confidence |
| PCI Registered Reports | Stage-1 registered reports, cross-discipline | No, medium confidence on physics coverage |
| Philosophy of Physics (LSE, open access) | Foundations arguments | No, medium confidence |
| PhilSci-Archive | Preprints in philosophy of science, no gate | No, high confidence |

The last two matter more than they look. Section C uses them.

### A.3 The genuinely novel piece: two unnamed pre-registration failure modes

This is the strongest item in my report and I do not think a physics-first reading finds it.

The project has documented **two instances of a pre-registration failing not because the science was
wrong but because the registered test was vacuous by construction**, and they are different types:

1. **Symmetry-vacuous test.** SIM-2026-074. HYP-008's registered killer test compared epsilon to
   epsilon, because Kramers-Wannier self-duality makes `Z_j Z_{j+1}` and `X_j` the same operator at
   `h = 1`. Verified to 1e-15. The test could not have discriminated anything, and nobody noticed
   until after it ran and after SIM-073 had been interpreted against it.
2. **Unsatisfiable-bar test.** SIM-2026-078. Gate G2 was registered at `delta = 0`, which is undamped
   real-time evolution whose cost is exponential in evolution time. The gate demanded 1e-8 from a
   computation that cannot reach 1e-8 at the registered sizes. The code path was proven correct at
   L = 8, chi = 256, where the MPO is exact to a discarded weight of 3e-28 and G2 passes at 4e-14.
   The specification was wrong, not the implementation.

The pre-registration literature grew up in psychology and clinical medicine. It names p-hacking,
outcome switching, undisclosed analytic flexibility. It does not, as far as I know (**UNVERIFIED**,
and this is exactly the claim that must pass a section 8 gate before anyone writes it down), name
**a pre-registered discriminating test that an exact symmetry of the system renders identically
trivial**. It cannot: psychology's systems have no exact symmetries, and every mathematised science
does. The deliverable is a short methods piece with the two failure modes, the two instances with
the algebraic reason each was vacuous, and a pre-flight procedure. Before registering a contrast
between A and B, prove they are not related by a symmetry at the registered parameter point. Before
registering a numerical bar, show the bar is attainable by the chosen method at one reachable size.

- **Genuinely possible outcomes: not applicable in the section 6 sense.** Not a measurement; its
  entire risk is prior art, so the literature gate is the whole gate.
- **Achievable claim level: Level 2 (methodological), in metascience rather than physics.**
- Cost: one literature gate, then two days of writing. The data exists and is already public.
- Killer: the gate finds this named and worked, in which case the output is one paragraph in the
  project's own governance file and nothing else.

### A.4 The operational independence failure, generalised

`CLAUDE.md` records that three internal notes agreed PRD had the paper "with editors" for 11 days
after PRD rejected it, all three written by the same process on the same day from one lookup, and a
withdrawal letter was nearly sent to an editor who had closed the file. That is a section 7
independence failure in **operational records**, and the 23-agent audit that caught the physics
instance walked past it. It generalises: any agent-run pipeline that writes a status into several
files from one fetch manufactures apparent corroboration, and a later reader counts agreement rather
than lookups. The mitigations are cheap: records restate external status and never refresh it, and a
status line carries the timestamp of the lookup rather than of the write.

- **Genuinely possible outcomes: not applicable. It is an incident report plus a rule.**
- **Achievable claim level: Level 2, in agent and research-infrastructure practice.**
- The audience that verifiably exists and is growing is AI-for-science evaluation. Benchmarks score
  agents on reproducing computational results (CORE-Bench, **UNVERIFIED** arXiv 2409.11363;
  ScienceAgentBench, **UNVERIFIED** arXiv 2410.05080). None I know of tests whether an agent notices
  its own records are same-origin, and this project has a real incident, near-miss and fix, which a
  benchmark author cannot synthesise credibly.

---

## B. Adjacent applied domains using the same instruments

The instruments, stated concretely: MERAKit.jl with a Z2 and Z3 symmetric optimiser that converted a
basin lottery into reliable convergence; puMPS with Koo-Saleur lattice Virasoro extraction; exact
diagonalisation of 1D critical chains to n = 24; a complex-time MPO validated to 1e-7 against ED; an
augmented-Lagrangian plus projection two-phase VQE (1.12 percent at 8 qubits, 3.33 percent at 24);
and a 25-operator ADAPT circuit preparing the critical TFIM ground state at L = 8 with overlap
0.9998.

### B.1 A CFT-calibrated hardware benchmark. Real, and the best item in this section.

Hardware benchmarks report fidelity, randomised-benchmarking error, or cross-entropy. They almost
never report **whether the device reproduces a universal number**. A different shape: prepare the
critical TFIM ground state with the published 25-operator ADAPT circuit, measure two-point functions
on the device, extract `Delta_sigma` and `Delta_eps`, report the error against the exact 1/8 and 1.
A universal exponent is insensitive to what fidelity conflates and sensitive to correlated error
differently.

Concrete artifact: a repository with the circuit in OpenQASM, the exact reference values, the
extraction script, a scoring rule, and one worked run under a realistic noise model. The audience is
named in the project's own records: QuEra's roadmap lists an 8x8 TFIM flagship (HW-068).

- **Genuinely possible outcomes: 3.** The universal extraction is (a) more forgiving than fidelity,
  so devices below a fidelity threshold still recover the exponent, (b) about equally strict, or
  (c) stricter, because the exponent needs long-distance correlations that decohere first. Nobody has
  measured which. That is real counterfactual novelty for a benchmark, which is unusual.
- **Achievable claim level: Level 2**, with a Level 3 path if the answer is (a) or (c) and the
  mechanism is identified and stated as a prediction for other devices.

### B.2 An exact CFT lattice-data dataset. Real, low ceiling, very cheap.

Tensor-network library authors need regression fixtures. On disk: spectra and scaling dimensions for
critical Ising, tricritical Ising and 3-state Potts at several bond dimensions,
`C_sigma_sigma_eps = 0.5075` against the CFT 0.5, `C_TTT` at three universality classes each within
0.15 percent, and exact ED ground states. Artifact: a versioned Zenodo or HuggingFace dataset with a
30-line loader, each row carrying method, bond dimension, size, the exact value where one exists, and
the originating SIM ID.

- **Genuinely possible outcomes: 1.** The values are known or symmetry-fixed. Pure **Level 1**
  packaging, section 6 novelty zero by construction. Ship it as a by-product of section D, never as
  a project.

### B.3 Error-correction code capacity. Empty, and I am saying so.

I found nothing in the repository that produces an error-correction capacity number. The adjacency
from MERA to holographic codes is real in the literature and absent from this codebase. The one
hardware-code contact point in the record is PAPER-137, a trapped-ion HaPPY-code experiment, which is
someone else's result. **This angle is empty. Do not manufacture it.**

### B.4 Education. Real, but not the same product as section C.

The learning guides and the story chapters have different audiences. Chapter 13 is not education, it
is narrative nonfiction about a negative result. Section C handles it.

---

## C. The reel: popular science and philosophy of physics

### C.1 What the project actually did with a viral claim

The reel (Instagram DVe5jiJj1rv) made two claims: a person is a worldline "worm", and a triple
integral is the "shadow of a 4D object". The project turned the first into an entanglement entropy
for a **timelike** interval, found the paper that states it precisely (2302.11695, verified in
catalogue), built the object exactly on a lattice, and found the imaginary part the paper calls
"emergent time" is **exactly zero** to 1e-14 at every size, interval and temperature, because the
critical chain has a symmetry `V H V^dagger = -H` that forces the entropy real. It then registered
four alternative constructions, ran them for about six dollars, got four noes, and recorded a Level-3
negative. Then it re-read its own stored numbers and corrected its own summary of the one surviving
thread, in public, before anyone asked. That correction is ERRATA D9.

### C.2 Why this is worth more than another lattice number

Lattice numbers are not scarce. A legible, honest, checkable account of checking a beautiful claim
and watching it fail in an interesting way is scarce.

I read chapter 13 in full. It has a question a general reader already has, an exact answer, a two-line
reason, a table of four noes, and an author correcting himself inside the text. The register is right:
first person, no hedging, no triumph. It ends "It is a no. It is the best no we have." That sentence
does more for public understanding of how science works than the force exponent would have, in either
the 3.92 version or the 2.6 version.

### C.3 Where it goes. Two products, not one.

**C.3a Narrative nonfiction.** Outlets that take long-form first-person science narrative: Nautilus,
Aeon, The Atlantic's science desk, Quanta (usually commissioned, harder). All **needs one lookup** on
pitch process. A pitch needs one chapter, not fourteen: send chapter 13, or chapter 8, the story of
95.8 percent of a fit resting on one point. The hook is the self-retraction, not the physics.

**C.3b Philosophy of physics, the underrated one.** The trunk question of section 29 is *"what
mathematical and operational content, if any, does emergent geometry add beyond an accurate CFT
tensor-network representation?"* A Physical Review D referee does not recognise that as a physics
question. It is a live question in philosophy of physics, and what philosophers almost never have is
an author who operationalised it, wrote the criterion down in advance, ran it, and reports a negative
with the code attached. A paper of the form "an operational criterion for emergent geometry, and a
registered negative against it in one exactly solvable case" is publishable there and unpublishable
in PRD, with no endorser gate. PhilSci-Archive takes the preprint immediately with no gate at all.

- **Genuinely possible outcomes: 2, already partly constrained.** Either the criterion has content
  and the tensor network fails it in a statable way, or the criterion collapses into CFT data and
  emergent geometry adds no operational content here. The audit (no Level-4 content, zero matched
  controls ever run) and SIM-076's exact zero both point toward the second.
- **Achievable claim level: Level 3 as an argued no-go, Level 4 only if the matched control from the
  primary report's proposal 1 runs and feeds it.** Without that control it is a position paper with
  one worked example, worth writing provided it says so. Section 16 is explicit that a clean no-go is
  a result, not a failure.

---

## D. Contrarian: stop generating hypotheses, build one instrument

### D.1 The case, from the project's own counters

There are 32 hypothesis records on disk. By their status fields: 6 refuted or retired, 7
not-established or not-supported, 1 closed as untestable, 9 still "proposed" and never run, and the
two that once carried the highest confidence both had it withdrawn. Generation has outrun resolution
for months. Section 29 names this anti-pattern directly: "creating disconnected hypotheses" is
explicitly not what expansive means. Meanwhile the durable outputs are the Z2 and Z3 symmetric
optimiser that made MERA convergence reliable, the two-phase VQE, the exact-diagonalisation
pre-gates, the documented inversion of the unitary state-identification rule at Yang-Lee, and now the
complex-time MPO. Every one is an instrument, and the audit reaches the same conclusion in its own
words: the strongest defensible contribution the program has is methodological.

### D.2 The specific instrument

`research/tools/timelike-ee/qw_tlee_mpo.py`, hardened and released.

What it does: complex-time matrix-product-operator evolution producing transition matrices and their
entropies, for timelike entanglement entropy and pseudo-entropy on 1D chains. The load-bearing fact:
**gate G1 passed at 1e-7 against a 1e-6 bar at L = 12 and 14 against exact diagonalisation, in both
real and imaginary parts, and the pod's exact values reproduced the stored SIM-077 numbers digit for
digit.** At L = 8 with chi = 256 the MPO is exact to a discarded weight of 3e-28.

That is a validated instrument in a subfield that, as far as I can tell (**UNVERIFIED**; needs a
section 8 gate against TeNPy, quimb, ITensor and the pseudo-entropy literature), has had a steady
stream of papers since 2020 and no tested public reference implementation, because each group rolls
its own. Release contents: the MPO driver, the ED reference, the validation ladder as runnable tests
with 1e-7 and 3e-28 as assertions, the chiral-symmetry exact-zero theorem as a test that must return
zero, the regulator convention documented because the imaginary part depends on it, and a short paper.

- **Genuinely possible outcomes: 1.** It already works. This is Level 1 and Level 2 packaging, and
  section 6 novelty is the wrong lens for a tool. Saying so is part of the deliverable: do not dress
  an instrument as a discovery.
- **Achievable claim level: Level 2.** Publishable at JOSS or SciPost Physics Codebases, neither of
  which needs an endorser.
- **The comparison the brief asks for.** An instrument twenty people use beats a Level-3 number
  nobody reads, and here the instrument route is the only one where the blockers that killed every
  publication attempt so far (no arXiv endorser, no affiliation, no referee pool, a desk rejection)
  do not apply. That is not a consolation prize, it is the route with a working door.

### D.3 What I am not saying

I am not saying stop doing physics. I am saying the ratio is wrong: nine unrun proposed hypotheses
against zero released instruments. Release one instrument, then run one pre-registered question on
it. That is section 29's "grow outward from a strong trunk" read literally rather than as a slogan.

---

## E. Lesser-known open questions small enough for ED and MERA

For each: whether it is actually open, who is working on it, and what one clean number would add.

### E.1 Reality structure of pseudo-entropy on the lattice. Best physics candidate.

Pseudo-entropy generalises entanglement entropy to a transition matrix between two states and is in
general complex. The founding work is Nakata, Takayanagi, Taki, Tamaoka and Wei (**UNVERIFIED**
arXiv 2005.13801). The open question this project is uniquely placed to attack: **for the critical
transverse-field Ising chain, which pairs of states give a pseudo-entropy with a nonzero imaginary
part, and is there a symmetry criterion that decides it in advance?**

SIM-2026-076 already proved one instance of exactly that kind of criterion. The chiral symmetry
`V H V^dagger = -H` forces `Im S = 0` for the timelike transition matrix at `delta = 0`. That is a
theorem-shaped statement about when the imaginary part **must** vanish, found by this project, in a
literature where the imaginary part is usually discussed as a phenomenon rather than as something a
symmetry can forbid.

Generalising it is a small exact program sized for ED: classify pairs (ground state, excited state),
(ground state, symmetry-broken state), (thermal, quenched), by whether a symmetry of `H` forces
reality, then check numerically at n up to 24 in the cases where no symmetry applies.

- **Genuinely possible outcomes: 3.** (a) A clean symmetry criterion covers every case tested, a real
  structural result. (b) A criterion covers some cases and fails for a nameable class, which localises
  the interesting physics. (c) No criterion, the imaginary part is generic, which makes SIM-076 a
  feature of one construction and is itself worth recording.
- **Achievable claim level: Level 3**, and unusually for this project it is a Level 3 whose outcome is
  not fixed by conformal symmetry, because the question is about which lattice symmetry acts, not
  about the value of a CFT coefficient.
- **Prior-art risk: moderate to high.** The section 8 literature gate must run first. Search terms:
  pseudo-entropy, transition matrix entropy, non-Hermitian entanglement, reality conditions, PT
  symmetry, timelike entanglement. This is the gate whose absence cost HYP-028 its priority claim.
- Cost: ED only, no rented compute, the code exists and is validated.
- Named killer, per section 12: the criterion is shown to follow directly from the anti-unitary
  symmetry classification already standard in non-Hermitian physics, in which case the result is a
  restatement and stops under section 31.

### E.2 Finite-size corrections to timelike entanglement entropy. Open, cheap, low ceiling.

SIM-076 reproduced the real part of the published formula to 2 to 3 percent with the regulator on.
Nothing in the record characterises **how that 2 to 3 percent scales with L and with the regulator
`delta`**, or whether the correction exponent matches the irrelevant operator governing spacelike
entanglement corrections.

- **Genuinely possible outcomes: 3.** The exponent matches the spacelike one, differs by a statable
  amount, or shows no power law at reachable sizes.
- **Achievable claim level: Level 3 if it matches or differs cleanly, Level 1 if it is only
  convergence.** This sits close to "measuring a quantity the theory already fixes" and section 30
  applies. Run it as a rider on E.1 or on the instrument release, never alone.

### E.3 Non-unitary entanglement: true c versus effective c, by probe. Open, prior-art risk high.

Established result (**UNVERIFIED** arXiv 1405.2804, Bianchini, Castro-Alvaredo, Doyon, Levi,
Ravanini): the entanglement entropy of a non-unitary CFT sees the **effective** central charge
`c_eff = c - 24 h_min`, not `c`. SIM-2026-071 measured `c_KS = -4.29 +/- 0.15` at Yang-Lee, which is
the **true** `c = -22/5` with the correct sign, and excluded `c_eff = +2/5` by a factor of 11.

So the interesting question is not "what is c at Yang-Lee", which is known. It is **which lattice
probes see `c`, which see `c_eff`, and what structural property of a probe decides it**. One clean
table: four or five probes (entanglement entropy, Casimir energy from the spectrum, Koo-Saleur
stress-tensor matrix elements, the biorthogonal norm), each with its answer, at one non-unitary chain.

- **Genuinely possible outcomes: 4 or more.** Each probe independently lands on `c` or `c_eff`, and a
  pattern across probes either exists or does not.
- **Achievable claim level: Level 3.**
- **Caution, and it is serious.** HYP-028's priority claim already failed its section 8 gate against
  arXiv 2602.02649 and PRL 119, 040601. The audit also found the non-Hermitian conditioning grows
  faster than the signal: `kappa_T` doubles every `Delta L = 2`, reaching roughly 1e5 to 1e6 by
  L = 30 to 40, while the distance to the finite-size exceptional point shrinks as `L^-2.38` and the
  sensitivity grows as `L^3.74`. **Any Yang-Lee proposal needing larger L is already dead.** The probe
  table does not need larger L, which is why it is the version worth running. The audit's own
  highest-value-per-effort item, re-running Yang-Lee Phase 2 at PAPER-133's published `h_c` of
  1.55872195 for one to two hours of compute, is still unrun and should precede it.

### E.4 Koo-Saleur lattice Virasoro completeness. Open, but on borrowed tooling.

The Koo-Saleur construction builds lattice approximations to Virasoro generators (Koo and Saleur,
**UNVERIFIED** hep-th/9312156), refined into a practical extraction method by Milsted and Vidal
(**UNVERIFIED** arXiv 1706.01436) whose puMPS code this project vendors. Open: the form and exponent
of the leading finite-size correction to `<phi| L_n |psi>` for non-vacuum modules, and the level at
which the lattice generators stop closing the algebra.

- **Genuinely possible outcomes: 3.** A single clean exponent, module-dependent exponents, or no power
  law at reachable sizes.
- **Achievable claim level: Level 3**, with a live derivation-gate risk: some of this may follow from
  known operator-content arguments, so run that gate before spending compute. Ranked below E.1 and
  E.3 because the project would be extending someone else's instrument, which weakens both the
  methodological claim and the prior-art position.

### E.5 Operator entanglement growth at criticality. Skip as a project.

Operator entanglement of the time-evolution operator at criticality grows logarithmically with a
CFT-predicted coefficient (Dubail, **UNVERIFIED** arXiv 1612.08630). The complex-time MPO is nearly
the right instrument, but the area is well studied, prior art is dense, and reproducing a predicted
log coefficient has near-zero counterfactual novelty. **Correct use: a validation case inside the
instrument release of section D**, honestly labelled Level 1.

---

## F. What a large institution structurally will not do

Stated as mechanisms, not slogans.

1. **Granularity of attention.** SIM-076 and SIM-077 together cost about six dollars and answered a
   question posed by a cited paper. A national lab's minimum unit of allocation, review and
   reporting is orders of magnitude larger. Six-dollar questions sit below the granularity at which
   institutional compute is scheduled, so nobody runs them, not because they are hard but because
   they are too small to enter the queue.

2. **Who pays for a retraction.** When this project found its headline was the maximum of 15
   defensible estimator choices, the cost of saying so fell on a person with no CV to damage, no
   co-authors to consult, no student whose thesis cites it, and no renewal listing it as a
   deliverable. Inside an institution each of those is a named person with a real cost, and those
   people make the retraction decision. The asymmetry is structural, not moral, and it is the
   clearest thing this project can do that an institution cannot.

3. **Registered negatives do not renew grants.** A gated three-month program ending in "among these
   four constructions, no" is an excellent scientific outcome and a career-neutral to
   career-negative one for a postdoc. Renewals are written against proposed and achieved milestones,
   and nobody proposes a milestone whose achievement is a no.

4. **No home department.** Sections A, C and D sit across lattice physics, philosophy of physics,
   metascience and AI agent design. No review panel owns that intersection, so there is no funding
   line and no institutional actor whose job it is. One person holding all four contexts pays zero
   coordination cost.

5. **Publishing the mistakes.** No institution publishes a chapter-by-chapter account of its own
   program including the mis-specified killer test, the gates that could not fail, and eleven days of
   believing a rejected paper was with editors. Reputational accounting forbids it. That account is
   what is scarce, and what sections A and C propose to ship.

6. **The reverse entry, for honesty.** An institution can put a matched non-geometric control on real
   hardware, sustain a program past one person's attention, and supply the referee pool this project
   spent a year failing to reach. The Level-4 experiment the audit says has never been run is blocked
   by scale, not incentives, and pretending otherwise repeats the overclaiming the audit documented.

---

## Ranked top 5 alternatives

**1. Release the complex-time MPO as a validated instrument, validation ladder as tests.** Section
D.2. Level 2, one possible outcome because it already works. Highest value per remaining effort in
this report: the hard part is done and verified at 1e-7, and JOSS and SciPost Codebases need no
endorser. Do this first.

**2. Write up the two pre-registration failure modes, symmetry-vacuous and unsatisfiable-bar, with
their worked instances.** Section A.3. Level 2 in metascience. Literature gate before a word is
written; if it finds prior art, the output is one paragraph in the governance file and nothing else.
Cheap, transferable far beyond physics, and it turns the project's scar tissue into something others
can use.

**3. Classify the reality structure of pseudo-entropy on the lattice.** Section E.1. Level 3, three
possible outcomes, and the only physics question here whose answer is not fixed by conformal
symmetry. Reuses SIM-076 and SIM-077 code unchanged, costs ED time and no rented compute, and SIM-076
already holds the seed theorem. Run the section 8 gate first: the prior-art risk is the real one.

**4. The operational-criterion paper for emergent geometry, carrying the registered negative.**
Section C.3b. Level 3 as an argued no-go, Level 4 only if the matched control runs and feeds it. Two
possible outcomes and the evidence leans to the no-go. The trunk question written for the audience
that recognises it, at venues with no endorser gate.

**5. Pitch one story chapter as narrative nonfiction.** Section C.3a. Not a claim level, it is
communication. One chapter, and the hook is the self-retraction. Ranked fifth only because it waits
on Jon's voice note on chapter 1 and competes for his attention with everything above.

**Explicitly not recommended:** a registered-negative series aimed at physics readers (A.2, no
readership, and most refuted claims are the project's own, so redirect that content to metascience,
codebase and philosophy venues); any Yang-Lee work needing larger L (E.3, conditioning grows faster
than signal); operator entanglement as a standalone project (E.5, near-zero novelty); any
error-correction angle (B.3, nothing in the repository supports it).


