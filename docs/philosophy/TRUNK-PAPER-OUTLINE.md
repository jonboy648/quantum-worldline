# Outline: philosophy-of-physics paper on the trunk question

**Status:** OUTLINE, drafted 2026-09-23. **Draft 1 written 2026-10-15: `TRUNK-PAPER-DRAFT.md`** (this outline is now the plan of record, the draft is the text).
**Target venue:** PhilSci-Archive (preprint), then a philosophy-of-physics journal if it holds up.
**Author:** Jon Cackler, independent researcher, Ames, Iowa.
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` (§5 claim levels, §6 counterfactual novelty,
§7 independence ledger, §8 novelty gate, §29 trunk question, §33-34 state vs representation).
**Citation rule:** references verified 2026-10-08 (26 correct, 5 corrected, 0 missing). Any reference added later is checked the same way before it is cited.
**HYP-033 UNBLINDED 2026-09-24: OUTCOME 4 (SMOOTH), Level 2** (`research/data/simulations/SIM-2026-079.json`). §7 takes that branch; the table below is kept as the registered record.

## Working title

**Agreement Without Discrimination: State Functionals, Surplus Structure, and the Operational
Content of Emergent Geometry in Tensor Networks**
Alt: *What would count as evidence that a tensor network's geometry is physical?*

## Abstract draft (~200 words)

Tensor networks such as MERA are often described as giving a discrete picture of a spacetime that
emerges from boundary quantum states. This paper asks what evidence could separate two readings of that
description: that the network's geometry is an efficient bookkeeping of a critical state (call it
Representation), or that it carries operational content not already fixed by the state and its
conformal data (call it Operational Geometry). We argue that a large class of observables cannot bear
on the question at all. Any quantity that is a functional of the boundary state alone is shared by every
faithful representation of that state, so agreement between such a quantity and a geometric prediction
cannot favour one reading over the other, however precise the agreement. We ground the argument in a
documented case: an independent research program whose "geometric" results (a force exponent, a
transport time, a chord distance) were, on audit, functionals of an exactly diagonalized state that
never touched a network, and whose headline number was later retracted as an estimator artifact. We
combine three tools from the program's own governance (claim levels, counterfactual novelty, an
independence ledger) with the philosophical literature on emergence and surplus structure, and we
identify the narrow class of network-dependent, gauge-invariant observables that could carry the
question. One such test was pre-registered and run: recoverability of an operator on an internal leg
degrades smoothly, and its onset in the optimized network is indistinguishable from that in random
networks on the same graph.

## Section-by-section outline

Per section: **claim**, **move**, **evidence** (repo paths; quote numbers from the record of authority).

### §1 Introduction: the trunk question and why a failed program is useful evidence

- **Claim.** Whether emergent geometry adds anything operational to an accurate tensor-network model of
  a CFT state is an open, well-posed-in-principle question. A program that tried to show it does and
  failed supplies evidence about *which kinds of test cannot work*.
- **Move.** State the trunk question (RESEARCH-DIRECTOR §29) and the two hypotheses verbatim (§4:
  A = efficient representation, B = operational emergent geometry). Say plainly this is a case study
  with one worked example, not a general theorem about holography (FINAL-REPORT recommendation 2).
- **Evidence.** `docs/governance/RESEARCH-DIRECTOR.md` §4, §29; `research/data/audit/valuable-questions-2026-09-14/FINAL-REPORT.md` (executive summary, item A4).
- **Framing guard.** Scope is 1+1D lattice CFT (critical Ising and relatives) with MERA. No claim about
  AdS/CFT in general, and none about quantum gravity.

### §2 Background: emergence in holography, and where tensor networks sit

- **Claim.** The philosophy literature on emergent spacetime in gauge/gravity duality mostly asks
  whether a duality makes the bulk emergent, fundamental, or neither. Tensor-network "geometry" raises
  a different, sharper question: the network is not dual to the state, it *represents* it, and the
  same state has many representations. So the relevant contrast is not duality versus emergence but
  *state property versus representation property*.
- **Move.** Brief survey: Butterfield on emergence as novel and robust behaviour, compatible with
  reduction; Dieks, van Dongen and de Haro, and de Haro, on emergence versus duality in holography;
  Rickles and Teh on AdS/CFT and emergence; Huggett and Wüthrich on empirical coherence; Crowther on
  inter-theory relations. Then the physics of MERA-as-geometry (Swingle; Vidal) and its critics
  (Bao et al.; Milsted and Vidal's light-cone reading; Beny on causal structure).
- **Evidence.** None from the project; this section is literature only. All items verified 2026-10-08.

### §3 A distinction: state functionals versus network-sensitive observables

- **Claim (central).** Call an observable a *state functional* if its value is fixed by the boundary
  state rho alone. Every faithful representation of rho (MERA, MPS, exact vector) returns the same
  value. Therefore no degree of agreement between a state functional and a geometric formula can
  discriminate A from B: both hypotheses predict the agreement whenever the representation is accurate.
  Agreement then measures *ansatz fidelity*, not bulk physics.
- **Move.** Give the definition, the one-line argument, and the corollary: a matched control that swaps
  the representation cannot separate representations on an observable that never sees the
  representation. Connect to Redhead's "surplus structure" and to the familiar point that
  gauge-variant quantities are not physical: the internal network is surplus structure relative to rho
  *unless* some observable depends on it.
- **Evidence.**
  - `research/data/simulations/holographic_transport_16q.py:347` prints "Skipping full MERA bulk
    computation (complex to implement correctly)"; the transport time T was measured on the boundary
    chain alone (AUDIT §7.1 item 1).
  - The force exponent was fitted on an exactly diagonalized 24-site chain, no MERA in the measurement
    (`docs/governance/AUDIT-2026-08-11.md` §3 table, row 1).
  - FINAL-REPORT key finding 4 (F, T, Synge chord distance are all exact-state functionals; the P1
    control died on this, "outcome count 1, claim level 1"); chord distance: `SIM-2026-031.json`.

### §4 A dilemma for the geometric reading: gauge invariance versus network dependence

- **Claim.** A candidate observable for B must be (i) invariant under the network's internal gauge
  freedom, or it is surplus structure, and (ii) sensitive to the network's organisation, or it is a
  state functional and cannot discriminate. These pull in opposite directions. B has content only in
  the band of *joint functionals of (state, network)* that survive gauge transformations.
- **Move.** Present the project's own sharpening of B into B-star (the audit's geometry advocate):
  gauge/architecture/chi invariance, plus non-derivability from CFT data {c, Delta, C_ijk} or from
  network parameters {chi, branching, cone width}, plus a parameter-free out-of-sample prediction. Note
  that the *advocate*, not the skeptic, supplied this and found that no project observable met even the
  first two clauses. Discuss whether the band is empty in principle (a possible no-go) or merely
  unexplored; the paper takes no side beyond what §7 permits.
- **Evidence.** `docs/governance/AUDIT-2026-08-11.md` §7.2 item 1 (B-star), §7.3 (editor's ruling:
  "not well-posed inside this project" because no fixed bulk distance, no equivalence relation between
  networks, two conflicting l_AdS definitions, no network-dependent observable); §7.1 item 2 (a
  quantity that shifts 37% when the representation of the identical state improves is a representation
  property). RESEARCH-DIRECTOR §33-34.
- **Counterexample to handle.** The FINAL-REPORT notes a gauge-invariant network number not fixed by
  scaling dimensions (C_sigma_sigma_eps = 0.5075). It *is* fixed by CFT data (exactly 1/2 since
  BPZ 1984), so it is gauge-invariant yet fails B-star's non-derivability clause. Use it to show the
  dilemma is real rather than a straw man. Source: `research/data/simulations/SIM-2026-061.json` (0.5075 found
  there; also AUDIT §5.2 on the chi=8 versus chi=12 band choice, which must be quoted alongside it).

### §5 Counterfactual novelty: how many outcomes were possible?

- **Claim.** The evidential weight of an agreement depends on how many outcomes were genuinely possible
  before the run. When conformal symmetry or a definition fixes the answer, a successful run confirms
  the code, not the interpretation. This is Mayo's severity applied before the data; unlike use-novelty,
  the issue is whether the hypothesis could have failed, not whether the data built it.
- **Move.** Walk through the project's audited ledger. 21 of 34 calculated claims could not have come
  out otherwise. The "universality" of alpha = 4 at three CFTs compared a force exponent at Ising to
  scaling dimensions elsewhere, and every alpha field was exactly twice the adjacent Delta_T field. The
  C_TTT ladder was a Virasoro identity evaluated in code. The Yang-Lee central-charge *sign* is the one
  place where the outcome space had more than one physically meaningful member.
- **Evidence.** `docs/governance/AUDIT-2026-08-11.md` §1 (21 of 34), §3 table ("Guaranteed" column),
  §5.1 row 1 (Yang-Lee sign); `research/data/theory/epsilon-channel-proof.md` (alpha = 4 derived from
  the Kac table alone, no geometry); RESEARCH-DIRECTOR §6.

### §6 Independence: why agreement among same-input quantities is not evidence

- **Claim.** Two numbers that agree because both are transformations of one input are one number.
  Robustness arguments (Wimsatt) require independent derivations; the project's "three independent
  evaluations" of alpha and its l_AdS agreements fail that requirement, and a single shared convention
  (l_AdS = 1/ln chi) sat on both sides of several comparisons.
- **Move.** Present the audit's classification (4 load-bearing agreements of 24; the other 20 exact
  identities, algebraic restatements, or one state measured twice) and the shared-root table. Then the
  retraction as the worked example: three datasets moved together under one systematic, one point
  carried 95.8% of the fit objective, and the published 3.92 was the maximum over 15 defensible
  estimator choices; the measured value is 2.6 +/- 0.2. Extend the point to operational records: the
  same failure (three agreeing internal notes, zero external lookups) hid a journal rejection for 11 days.
- **Evidence.** AUDIT §5.1-5.3; `research/ERRATA.md` E6 and
  `research/data/simulations/SIM-2026-072.json` (retraction, record of authority); CLAUDE.md "External
  Status Must Be Freshly Checked" (operational instance; INCLUDE, decided 2026-09-24 under Jon's delegation:
  the paper's premise is that the project audits itself, so its operational failure belongs beside the physics one).
- **Caution.** Stegenga's discordance point: independence is necessary for robustness to confirm, and
  not sufficient. Do not overstate what an independence ledger delivers.

### §6b Three closed routes as boundary markers

- **Claim.** A negative that closes a route tells us about the shape of the question only if the test
  could have come out the other way.
- **Move.** (a) HYP-008: the registered killer compared the energy density with itself (Kramers-Wannier
  self-duality), so it was vacuous; a pre-registration can be symmetry-vacuous. (b) HYP-032: the
  imaginary part of timelike entanglement entropy is exactly zero on the lattice by chiral symmetry; a
  regulator can erase a quantity geometric readings lean on. (c) HYP-006: l_AdS cancels in the source
  derivation, so the transport number survives and its geometric reading does not.
- **Evidence.** `research/ERRATA.md` E8; `research/data/simulations/SIM-2026-074.json`, `-075.json`,
  `-076.json`, `-077.json`; `research/data/hypotheses/HYP-2026-008.json` (CLOSED_UNTESTABLE_N_LE_24),
  `HYP-2026-032.json` (Level-3 negative), `HYP-2026-006.json` (on disk `status: SUPPORTED`,
  `confidence: low`, checked 2026-09-23; quote both); AUDIT §7.2 item 2.

### §7 A network-sensitive test: bulk operator recovery (see branching section below)

- **Claim.** Recovery of an operator inserted on an internal leg is a joint functional of state and
  network, and the registered version is gauge-invariant by construction. It is therefore in the band
  §4 identifies, and is the only observable in the project that touches the network at all.
- **Move.** Describe the observable in philosophical terms (what the boundary region A can learn about
  an inserted leg), the two predictors (causal cone: "the network is a circuit"; minimal cut:
  "entanglement wedge"), and the controls. Explain honestly that the design was corrected twice before
  unblinding, including a finding that the first registered statistic was pinned by an identity for
  *every* isometric network, and that the v3 amendment lowered the best outcome from Level 4 to Level 3
  because no CFT-matched non-geometric ansatz is registered.
- **Evidence.** `research/tools/bulk-recovery/PREREGISTRATION-HYP033.md`,
  `research/tools/bulk-recovery/AMENDMENT-V3-PROPOSAL-HYP033.md`,
  `research/tools/bulk-recovery/PRIOR-ART-1701.00050-agent-report.md`. Result: `SIM-2026-079.json`,
  `research/tools/bulk-recovery/runpod_033/UNBLINDED_REPORT_v3.txt` (see §7 result below).

### §8 Discussion: what would make geometry more than a visualization?

- **Claim.** On present evidence, Hypothesis A (representation) is the parsimonious reading in this
  setting, and that is a claim about evidence, not a proof that B is false. The live question is whether
  the joint-functional band contains anything that CFT data plus network parameters do not already fix.
- **Move.** Tie to emergence debates: if every network-sensitive gauge-invariant quantity turns out to
  be fixed by graph structure alone (as in random tensor networks), then the geometry is a property of
  the *ansatz*, which is emergence in Butterfield's weak sense at most, and not evidence about the
  state's physics. Note the parallel with analogue-simulation confirmation (Dardashti, Thebault and
  Winsberg): a lattice model can confirm claims about a target only under an independently argued
  universality assumption, and "the network is the bulk" has no such argument yet.
- **Evidence.** AUDIT §7.3; FINAL-REPORT "Challenges not survived" (P3 no-go conjecture refuted three
  ways, incl. prior art arXiv:1812.00529 and arXiv:1504.06632).

### §9 Conclusion

- One paragraph each: the distinction (§3), the dilemma (§4), the two diagnostics (§5-6), and the
  conditional result (§7). Close on the practical recommendation that geometric language be withheld
  from any quantity before a network-sensitive observable exists (FINAL-REPORT recommendation 4).

## §7 HYP-033 RESULT (unblinded 2026-09-24): outcome 4, smooth, Level 2

Seed means at chi = 6 (8 seeds each; G1-G3 24/24; G4 primary 8/8; G5 NOT EVALUABLE, chi 8 out of memory):

| arm | m_0.9 left / right | w |
|---|---|---|
| optimized MERA, critical | 4.75 / 4.34 | 7.76 |
| C-HAAR, same graph | 4.62 / 4.62 | 6.06 |
| C-GAPPED, h = 1.5 | 4.91 / 4.19 | 7.59 |

m_half = 8.50 in every network (the v3 identity). Argument for §7, per the outcome-4 row: the one
network-sensitive, gauge-invariant observable the project built does not separate the optimized network
from a random one at this size; its onset of loss is a property shared with Haar networks on the same
graph, which is §4's dilemma in its sharpest form. "C-HAAR differs" has no registered test beyond m_0.9,
and on m_0.9 it does not differ, so the result is Level 2, not Level 3 negative. The broader, seed-asymmetric
optimized curves are POST-HOC and may be mentioned only as unregistered. chi = 6 only; the question at
larger chi (where 1601.01694 predicts sharp minimal-cut behaviour) stays open. C-REWIRE dropped 2026-09-24.

## §7 HYP-033 branching section (registered record, pre-unblinding)

**Nothing here predicts or hints at the outcome.** Results are blinded under
`research/tools/bulk-recovery/runpod_033/` and were not opened for this outline. The branches are the
registered ones, as amended by v3 (approved 2026-09-22, before unblinding). Write this section only
after unblinding, and pick the branch by the pre-registered precedence (cut-like test first, then
cone, then smooth), never by which branch reads best.

| Registered result | Level (v3) | What the paper would then argue |
|---|---|---|
| **Void: G3 gauge-invariance fails** | none | The observable was wrong, not the physics. §7 reports a failed instrument; the paper's thesis stands on §3-6 alone as a position paper with one worked example. |
| **Gate failure: G1, G2, G4 or G5** (structural zero/one, purity sum, basin, chi stability) | none, or UNCONVERGED points excluded | Report the failure as registered. Same fallback as void. If G5 excludes points, say how many and do not interpolate around them beyond the pre-declared m = 4 gap. |
| **Outcome 1: cone-like** (m_half <= 2) | Level 3 negative | Recovery needs the whole footprint: the optimized MERA behaves as a circuit, not as a code with wedge structure. Strengthens A in this setting and suggests the joint-functional band is occupied by circuit structure only. No geometric language (banned by registration). |
| **Outcome 2: cut-like** (m_0.9 >= 6 on both edges AND seed mean >= 3 sites above C-HAAR at chi = 6) | **Level 3**, "holographic-code-like encoding of the optimized circuit" (downgraded from 4 by v3) | The strongest case the paper could make: a gauge-invariant, network-sensitive observable behaves differently in the optimized network than in a same-graph random one. Argue that this puts content in the §4 band, and state precisely why it still is not Level 4: no CFT-matched non-geometric ansatz was registered, so it does not yet separate A from B. Name that ansatz as the missing control. Cite, never claim, what arXiv:1701.00050 already proves. |
| **Outcome 3: cut-like in both MERA and C-HAAR** | Level 2 | The pattern is a property of the graph, as random-tensor-network results already lead one to expect (arXiv:1601.01694). Argue this is the sharpest illustration of §4's dilemma: the network-sensitive quantity turned out to be an *ansatz* property, neither a state property nor evidence about the state's physics. Supports A. |
| **Outcome 4: smooth** (w > 6 and not cut-like) | Level 2, or Level 3 negative if C-HAAR differs | The registered expected outcome, for the stated reason (small nu for Ising; sharp minimal-cut behaviour is a large-bond-dimension result). Argue the question is not settled at chi = 6-8 and that the band remains unexplored at accessible sizes. Report whether C-HAAR differs; if it does, the difference is a fact about the critical state's encoding, not about geometry. |
| **Cap truncation** (pre-declared order: primary, C-HAAR, C-GAPPED, chi = 8) | depends on what completed | Report which networks ran. If C-HAAR did not complete, outcome 2 cannot be declared and the section says so. |

**Fixed for every branch:** C-REWIRE was left out as infeasible before any result (pre-run spec 2),
so the paper cannot claim a "same tensors, different graph" control. m_half is reported but labelled
"pinned by complementarity, not discriminating" (v3 item 1). The DA finding that m_half <= 8.5 for every
isometric network on this graph belongs in §7 whatever the outcome: it is a clean instance of §5's point
(a statistic that could not have come out otherwise), caught before unblinding.

## Limitations

- **One program, one model class.** The case study is 1+1D critical lattice models with small-chi MERA.
  Nothing generalizes to AdS/CFT, higher dimensions, or large-N holography without a separate argument.
- **Self-audit.** The evidence comes from the author's own program and its own internal audits (AI
  agents working under a written standard). Those audits are same-origin sources in the §7 sense. The
  retraction was re-derived by an independent driver, and the Zenodo v5 correction is public, but no
  outside referee has checked the audit. Say so in the paper.
- **The central distinction may be weaker than it looks.** The bulk-recovery observable is itself a
  functional of an extended pure state (reference plus boundary) that the network defines. The paper
  must argue why "functional of the Choi-type state the network produces" counts as network-sensitive
  rather than a relabelled state functional. This is the most likely referee objection; answer it in §4.
- **No theorem.** §3's argument is simple and may already be stated in the literature in other words
  (surplus structure; gauge-invariance requirements; Bao et al.). The §8 novelty gate has NOT been run
  on it. Until it is, the paper claims no priority and presents §3 as an application.
- **Outcome-conditional.** Without HYP-033 the paper is a position paper with one worked example
  (FINAL-REPORT recommendation 2). Its title and abstract must not promise more.
- **Philosophy engagement is from memory.** The literature map in §2 was written without reading the
  papers for this outline. Positions attributed to Butterfield, de Haro, Crowther and others must be
  checked against the texts before they are paraphrased.
- **Language.** No "novel", "first", "to our knowledge" (RESEARCH-DIRECTOR §8). No "geometry", "wedge"
  or "emergent" for HYP-033 outcomes 1, 3 or 4 (preregistration "Banned" list).

## References (ALL VERIFIED 2026-10-08 against Crossref/arXiv: `REFERENCES-VERIFIED-2026-10-08.md`; Wimsatt 1981 page range unresolved, 123-162 vs 124-163)

(H)/(M) = high/medium confidence the work exists as described. (repo) = already cited in project records.

**Philosophy of emergence and holography**
- Butterfield, J. (2011). "Less is different: emergence and reduction reconciled." *Found. Phys.* 41, 1065-1135.
- De Haro, S., Mayerson, D., Butterfield, J. (2016). "Conceptual aspects of gauge/gravity duality." *Found. Phys.* 46, 1381-1425.
- De Haro, S. (2017). "Dualities and emergent gravity: gauge/gravity duality." *Stud. Hist. Phil. Mod. Phys.* 59, 109-125.
- Dieks, D., van Dongen, J., de Haro, S. (2015). "Emergence in holographic scenarios for gravity." *Stud. Hist. Phil. Mod. Phys.* 52, 203-216.
- Rickles, D. (2013). "AdS/CFT duality and the emergence of spacetime." *Stud. Hist. Phil. Mod. Phys.* 44, 312-320.
- Teh, N. J. (2013). "Holography and emergence." *Stud. Hist. Phil. Mod. Phys.* 44, 300-311.
- Huggett, N., Wuthrich, C. (2013). "Emergent spacetime and empirical (in)coherence." *Stud. Hist. Phil. Mod. Phys.* 44, 276-285.
- Crowther, K. (2016). *Effective Spacetime: Understanding Emergence in Effective Field Theory and Quantum Gravity.* Springer.
- Crowther, K. (2018). "Inter-theory relations in quantum gravity: correspondence, reduction and emergence." *Stud. Hist. Phil. Mod. Phys.* 63, 74-85.
- Jaksland, R. (2021). "Entanglement as the world-making relation: distance from entanglement." *Synthese* 198(10), 9661-9693. doi:10.1007/s11229-020-02671-7 (online 2020-05-18).
- Redhead, M. (1975). "Symmetry in intertheory relations." *Synthese* 32, 77-112. (origin of "surplus structure")

**Confirmation, severity, independence**
- Mayo, D. (1996). *Error and the Growth of Experimental Knowledge.* University of Chicago Press.
- Mayo, D. (2018). *Statistical Inference as Severe Testing: How to Get Beyond the Statistics Wars.* Cambridge University Press.
- Hitchcock, C., Sober, E. (2004). "Prediction versus accommodation and the risk of overfitting." *Brit. J. Phil. Sci.* 55, 1-34.
- Wimsatt, W. C. (1981). "Robustness, reliability, and overdetermination." In Brewer & Collins (eds), *Scientific Inquiry and the Social Sciences.* Jossey-Bass.
- Stegenga, J. (2009). "Robustness, discordance, and relevance." *Phil. Sci.* 76, 650-661.
- Dardashti, R., Thebault, K., Winsberg, E. (2017). "Confirmation via analogue simulation: what dumb holes could tell us about gravity." *Brit. J. Phil. Sci.* 68, 55-89.
- Dawid, R. (2013). *String Theory and the Scientific Method.* Cambridge University Press. (non-empirical confirmation, as a foil)

**Physics: tensor networks, holography, recovery**
- Vidal, G. (2007). "Entanglement renormalization." *Phys. Rev. Lett.* 99, 220405.
- Swingle, B. (2012). "Entanglement renormalization and holography." *Phys. Rev. D* 86, 065007.
- Almheiri, A., Dong, X., Harlow, D. (2015). "Bulk locality and quantum error correction in AdS/CFT." *JHEP* 04, 163.
- Pastawski, F., Yoshida, B., Harlow, D., Preskill, J. (2015). "Holographic quantum error-correcting codes: toy models for the bulk/boundary correspondence." *JHEP* 06, 149. arXiv:1503.06237 (repo).
- Hayden, P., Nezami, S., Qi, X.-L., Thomas, N., Walter, M., Yang, Z. (2016). "Holographic duality from random tensor networks." *JHEP* 11, 009. arXiv:1601.01694 (repo).
- Bao, N., Cao, C., Carroll, S. M., Chatwin-Davies, A., Hunter-Jones, N., Pollack, J., Remmen, G. N. (2015). "Consistency conditions for an AdS multiscale entanglement renormalization ansatz correspondence." *Phys. Rev. D* 91, 125036. arXiv:1504.06632 (repo).
- Beny, C. (2013). "Causal structure of the entanglement renormalization ansatz." *New J. Phys.* 15, 023020.
- Milsted, A., Vidal, G. (2018). "Geometric interpretation of the multi-scale entanglement renormalization ansatz." arXiv:1812.00529 (preprint; no journal version).
- Kim, I. H., Kastoryano, M. J. (2017). "Entanglement renormalization, quantum error correction, and bulk causality." *JHEP* 04, 040. arXiv:1701.00050 (repo, catalogued PAPER-2026-142).
- Cao, C., Carroll, S. M., Michalakis, S. (2017). "Space from Hilbert space: recovering geometry from bulk entanglement." *Phys. Rev. D* 95, 024031.
- Scan #21, MUST CITE: arXiv:2610.00478, "Algebraic structure in holographic tensor networks" (PAPER-2026-153): cut-like algebra structure proven for idealized random networks; finite chi set aside. Frame §7 against it. Verify authors/venue before citing.
- arXiv:2610.08787, "Algebraic Tensor Network Renormalization and Holographic duality" (PAPER-2026-152): cite in §4 beside C_sse = 0.5075 (they reach 0.5004 with 3 fitted parameters). Verify authors/venue before citing.
- Belavin, A. A., Polyakov, A. M., Zamolodchikov, A. B. (1984). "Infinite conformal symmetry in two-dimensional quantum field theory." *Nucl. Phys. B* 241, 333-380.

**Project artifacts (self-citations)**
- Cackler, J. Zenodo v5 correction, DOI 10.5281/zenodo.22080720 (retraction of alpha = 3.92). Re-check the public record before citing (CLAUDE.md external-status rule).
- `docs/governance/RESEARCH-DIRECTOR.md`, `docs/governance/AUDIT-2026-08-11.md`,
  `research/data/audit/valuable-questions-2026-09-14/FINAL-REPORT.md`, `research/ERRATA.md`. The repo is
  PUBLIC since 2026-09-25 (github.com/jonboy648/quantum-worldline, one-commit snapshot), so these paths are
  citable. For a stable citation, deposit a tagged snapshot on Zenodo before posting (a GitHub path can move).
