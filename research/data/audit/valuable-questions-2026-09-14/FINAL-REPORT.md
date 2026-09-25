# What could this project do that is genuinely valuable? Final report

**Date:** 2026-09-14. **Team:** three Opus researchers (primary physics, alternative angles, practical
constraints) plus one Opus challenger, synthesised by the session lead. Source files in this directory:
`research-primary.md` (427 lines), `research-alt.md` (464), `research-practical.md` (349),
`research-challenge.md` (421). The lead spot-checked the challenger's load-bearing citations against
disk before writing this (the transport driver's "Skipping full MERA bulk computation" line, the JOSS
six-month rule as recorded by practical, the text of primary proposal 4).

**The brief, from Jon:** what questions or equations would make our work valuable and beneficial to
the human race, truly groundbreaking, something the government or other systems cannot answer, that
aligns with our tools.

## Executive summary

Nothing proposed by any researcher meets the bar as written, and the challenger says so plainly. This
project's reach is a small corner of 1+1D lattice conformal field theory plus one unusual process
record. Inside that corner, two things survived adversarial review and are worth the next quarter: a
rebuilt bulk-operator-recovery measurement on MERA (the only proposal that measures a property of the
network rather than of the state, so the only one that can reach Level 4), and a philosophy-of-physics
paper on the trunk question, where the evidence already in hand matches the venue and there is no
endorser gate. Two of the three top-ranked physics proposals were killed on the project's own data
and on 2015 to 2018 literature that nobody had checked.

## Key findings (what the research established)

1. **Compute is not the constraint.** Every headline result since 2026-07-19 ran locally at zero cost.
   The local box has 24 cores and 65 GB; exact diagonalization at L=24 takes 325 s and L=26 has never
   been run. Attributable RunPod spend over 90 days is under 25 USD (practical, billing-checked; the
   self-reported 6 USD for HYP-032 was pod-create price, the billing upper bound is 9.37 USD).
2. **Throughput is 3 to 4 pre-registered, gated, written-up experiments per month**, limited by active
   days (34 of the last 91) and Jon's approval gate, not by hardware.
3. **Distribution is the wall for anything already built.** Lifetime public reach is 75 Zenodo views
   and 42 downloads (checked live). No arXiv endorser, and the endorsement rules tightened on
   2026-01-21. APS has said it will not consider the manuscript further. JOSS requires six months of
   public repository history and the repo went private on 2026-09-07, so that clock reads zero.
4. **The Level-4 experiment is blocked by observable design, not scale and not incentives.** All three
   researchers got the cause wrong. F(dr), transport T, and the Synge chord distance are functionals
   of the exact state; the drivers that produced them never touch a network
   (`research/data/simulations/holographic_transport_16q.py:347` prints "Skipping full MERA bulk
   computation"). A control that swaps the representation cannot separate representations when the
   observable never sees the representation. No rewiring, bulk-insertion, reconstruction, or
   gauge-orbit driver exists anywhere in `research/tools/`. Building one is two to four weeks of
   Jon's time and near zero dollars.
5. **The scarcest artifact the project owns is the self-executed retraction**, Zenodo v5 with the
   estimator matrix that caused it. It is rare, dated, checkable, and already published.

## Alternative perspectives (what was considered)

- **Instrument over result:** release the complex-time MPO driver (`qw_tlee_mpo.py`, G1-validated
  to 1e-7 against exact diagonalization) with its validation ladder as tests. Survives on merit,
  blocked on venue: JOSS shut until March 2027 at the earliest, SciPost Codebases wants a library and
  this is a driver script, and the novelty against TeNPy/ITensor/quimb complex-time evolution has not
  been established.
- **Metascience paper** on symmetry-vacuous and unsatisfiable-bar pre-registration failures
  (SIM-074, SIM-078 G2). Collapsed under challenge: assay sensitivity (ICH E10), Mayo's severity
  requirement, positive controls and manipulation checks all already name the concept. Worth one
  governance paragraph in RESEARCH-DIRECTOR, not a paper.
- **Pseudo-entropy reality structure** generalising SIM-076's chiral theorem. Weakened hard:
  arXiv:2209.07308 publishes the pseudo-Hermiticity reality condition. Alt's own registered killer
  fires on it.
- **Popular science / the reel:** chapter 13 of the story is judged the best artifact of 2026. Pitch
  one chapter, hook on the self-retraction, not fourteen chapters.
- **Registered-negative series** (primary #8): not recommended. Most refuted claims are the
  project's own; self-refutation of an unpublished claim is not a citable event.

## Practical considerations

| Item | Number | Source |
|---|---|---|
| Bulk-recovery measurement (P4) | 10 to 25 USD compute, 2 to 4 weeks of Jon's time to build the driver | primary :216, challenge sec 2 |
| Finish timelike-EE negative (SIM-078 grid) | Settings A+B at chi=128 about 24 USD, the whole cap; setting C or chi=256 is 8x that | practical A |
| One unmeasured number decides SIM-078 affordability | whether chi=128 passes G3 above L=24; one local L=32 run settles it | practical :5 |
| Philosophy-of-physics paper | zero dollars, Jon's writing time, PhilSci-Archive has no gate | alt C.3b, challenge A4 |
| Start the JOSS clock | make the repo public, about two hours, six months elapsed before submission is possible | practical :228 |
| Alignment, last 90 days | 63 percent physics, 37 percent process; no positive result since 2026-08-11; 28-day hole in the research log | practical F |

## Challenges survived

- **P4, bulk operator recovery, cone versus cut.** Insert an operator on internal MERA legs; measure
  recovery error from a boundary region; compare against causal-cone containment and minimal-cut
  containment, which differ in a MERA. Four genuinely possible outcomes. Level 3 for the
  measurement, Level 4 if the gauge control separates cone from cut. The killer as written is broken:
  a random unitary on internal legs changes a fixed inserted operator by construction, so the control
  would fire every time. The repaired version measures a gauge-covariant object, the recovery-error
  profile over the whole operator algebra at the bulk site (max, or average over a unitary 2-design).
  Fold P1's rewired-network arm in as its control.
- **P2, finish the timelike-EE negative.** Survives at Level 2 to 3 with a narrowed claim: it bounds a
  class of lattice regulators against arXiv:2302.11695, it is not a continuum result. The G2 gate
  specification error must go into ERRATA as a post-hoc amendment before any grid runs.
- **A4, the philosophy-of-physics route.** "An operational criterion for emergent geometry, and a
  registered negative against it in one exactly solvable case." Two possible outcomes, evidence
  already leans to the no-go, Level 3 as an argued no-go. Unpublishable in PRD, publishable there.
- **A1, the instrument**, on merit only. Venue closed for six months.
- **Practical's external facts** were verified by the challenger: the 2026-01-21 arXiv endorsement
  change and the JOSS six-month rule are both real.

## Challenges not survived

- **P1, the matched non-geometric control**, as specified. Killed: state functionals cannot
  separate representations. Outcome count 1, claim level 1. Rebuildable only as P4's control arm.
- **P3, the no-go theorem** that every MERA graph-distance observable is a function of scaling
  dimensions. Killed three ways: Milsted and Vidal arXiv:1812.00529 already give MERA a rigorous
  light-cone geometry; Bao et al arXiv:1504.06632 argued against the AdS reading in 2015; and the
  conjecture as stated is refuted by the project's own C_sigma_sigma_eps = 0.5075, a gauge-invariant
  network number that scaling dimensions do not fix.
- **A2, the metascience paper.** Concept already named in clinical-trial and philosophy-of-science
  literature. No referee pool.
- **A3, pseudo-entropy reality.** Pre-empted by arXiv:2209.07308.
- **The framing.** "Beneficial to the human race, something governments cannot answer" is met by
  nothing here. Governments can compute everything in these reports, better resourced. The narrow
  true version: institutions structurally will not fund a six-dollar negative or pay the career cost
  of a headline retraction. That is a real gap and it is small.

## Contradictions adjudicated (from the challenger's table)

Hypothesis records on disk: 32, not 33. SIM records: 79, not 78. HYP-032 cost: 9.37 USD billing
upper bound, not 6. Distribution binding: yes for anything already built, no for the missing Level-4
result. Zenodo v5 date: 09-06 by live API vs 09-07 in ERRATA, likely created-vs-published, one
lookup settles it.

## Recommendation

**GO on two items, NO-GO on the framing. Confidence: high on the kills, medium on the picks.**

1. **Build and pre-register P4, bulk operator recovery, with the repaired gauge-covariant killer and
   the rewiring control folded in.** It is the only proposal in the set that can produce a Level-4
   answer, and the cost is Jon's time, not money. It also supplies the matched control that A4 needs
   to move from position paper to result. Pre-registration first, then code, per the standing rule.
2. **Write the philosophy-of-physics paper on the trunk question and post it to PhilSci-Archive.**
   Claim level, evidence, and audience already match; there is no gate. Say plainly that without P4
   it is a position paper with one worked example.
3. **Cheap enabling acts, this week:** make the GitHub mirror public to start the JOSS clock (two
   hours); run one local L=32 chi=128 G3 check to learn whether the SIM-078 grid fits the cap; put
   the G2 specification error into ERRATA before any grid runs; record the symmetry-vacuous and
   unsatisfiable-bar gate lessons as one paragraph in RESEARCH-DIRECTOR.
4. **Do not** run the registered-negative series, the metascience paper, the pseudo-entropy paper,
   or the no-go theorem. Do not use geometric language for any quantity before a network-sensitive
   observable exists.

**What Jon should hear plainly:** the honest answer to the question as asked is no. The project's
value is bounded to a corner of lattice CFT and to a process record whose best artifact, the
retraction, is already public. Inside that corner there is one experiment that could give a real
Level-4 answer to a question a few hundred people care about, and one paper that fits a venue with no
gate. That is the whole list, and it is not nothing.
