# REDTEAM-C: Devil's Advocate Review of NOVEL-COMBO-C MERA-Bridge Candidates

**Role:** Devil's advocate. Sole job: find the strongest reason each top-5 bridge
fails, OR secretly trips a known HYP-017 killer (R1 hologron decay, R2
product-of-single-site-density estimator, R3/R4 single-basis TEE, blockade-
pathological geometry) despite claiming to avoid it.

**Reference:** NOVEL-COMBO-C-mera-bridge.md; project MEMORY HYP-017 closeout +
DEVILS-ADVOCATE 2026-05-05 (R1-R5).

**Hard lesson invoked throughout:** HYP-014 was REFUTED at high confidence because
an *amplitude match was coincidental* -- a curve fit to the right power with the
wrong mechanism. Any candidate whose evidentiary value rests on "we measured
r^-4" without independently pinning the *stress-tensor-exchange mechanism*
inherits that exact failure mode.

Status: IN PROGRESS
Date: 2026-05-16

---

## C1 — Rydberg static-CFT connected-correlator on Aquila

### Killer objection (STRONGEST): C1 secretly trips the exact HYP-017 closeout killer it claims to fix

The candidate's central defense is that R2 is "fixed by explicit bitstring
connected-correlator: `mean(z_i z_j) - mean(z_i) mean(z_j)` over shots." This
relabels R2 without dissolving the *real* HYP-017 closeout defect. Recall the
closeout root cause was three-fold: **wrong observable, wrong operator, and
"z-basis blind to OmegaX."** C1 fixes only the first two and walks straight into
the third.

**The measurement-basis trip.** QuEra Aquila's analog mode performs a single
global readout: each atom is projectively measured as ground vs. Rydberg
(occupation `n_i in {0,1}`) by fluorescence at the end of the run. There is **no
single-qubit rotation layer and no rotated-basis readout** — confirmed by the
Aquila whitepaper (arXiv:2306.11727) and AWS Braket Aquila docs: "measurements of
ground and Rydberg state populations are recorded globally for all atoms," with
no local control of one-/two-atom gates. The Aquila bitstring `z_i` is therefore
the **occupation/Z-basis only**.

The critical transverse-field Ising / PXP order parameter whose two-point
function carries the stress-tensor envelope is the **transverse magnetization
sigma^x**, not the occupation sigma^z. The 2D Ising CFT's primary fields:
sigma (Delta=1/8) -> `<sigma sigma> ~ r^{-1/4}`; epsilon (Delta=1) ->
`<epsilon epsilon> ~ r^{-2}`; stress tensor T (Delta=2) -> `~ r^{-4}`. In the
Rydberg/PXP mapping the *order-parameter* sigma maps onto an off-diagonal
combination; the occupation `n_i` (= projector onto Rydberg) is a **diagonal,
sigma^z-like operator**. Its connected correlator `<n_i n_j>_c` is dominated by
the **energy-density channel epsilon (r^{-2})**, NOT the stress-tensor channel
(r^{-4}). Measuring `<n_i n_j>_c` on Aquila and fitting to `r^{-alpha}` will
asymptote toward **alpha~=2, not alpha~=4** — and any value landing inside the
SIM-2026-023 acceptance window [3.2, 4.8] at finite N would be a finite-size
crossover artifact, i.e., precisely the HYP-014 coincidental-amplitude-match
failure mode, on hardware, for ~$200-500. This is the single most defensible
reason C1 fails as written.

This is *the same structural defect* as the HYP-017 closeout's "z-basis blind to
OmegaX": the observable you can actually read on Aquila is in the wrong CFT
channel. C1 dissolves R1 and the literal R2 estimator bug but re-trips the wrong-
observable/wrong-operator pair that the closeout explicitly named as the reason
HYP-017 was shelved.

### Does it dissolve R1 or relabel it?

R1 (hologron decay) IS genuinely dissolved, not relabeled. A Delta-sweep-prepared
static ground state has no propagating quasiparticle and no measurement window to
outlive; the closeout's R1 ("measuring noise after the hologron is gone") is
structurally inapplicable to an equal-time ground-state correlator. Credit where
due: C1's R1 claim survives. It is R2-as-relabeled and the un-addressed third
closeout defect (basis) that kill it.

### Secondary objections

- **Adiabatic state-prep fidelity at the critical point.** Ebadi et al. prepared
  ordered Z2 phases, where the gap stays open. The *critical point* itself has a
  vanishing gap (gap ~ 1/N), so an adiabatic Delta-sweep cannot prepare the
  critical ground state without diverging sweep time; in finite Aquila coherence
  the prepared state is a gapped near-critical state with a finite correlation
  length xi < N. The fitted exponent is then contaminated by the exponential
  cutoff `e^{-r/xi}` over exactly the dr=1..6 window proposed — biasing alpha
  upward and mimicking a steeper power. This is a second independent route to a
  coincidental r^{-4}-looking fit.
- **dr range too short.** dr=1..6 on a lattice with O(1) lattice-scale UV
  corrections cannot cleanly separate alpha=2 from alpha=4: across a 6x distance
  span the multiplicative lattice/UV prefactor is not yet subdominant, and a
  2-parameter `A r^{-alpha}` fit over 6 points with shot noise has wide enough
  error bars to "land in [3.2, 4.8]" by chance. The published numerics used 12
  points (SIM-2026-011) for exactly this reason.

### Prior-art check

Critical Rydberg-array correlators are an active, crowded field (arXiv:2508.05381
random displacements in critical Rydberg arrays; arXiv:2407.05455 quantum
supercriticality in the Ising/Rydberg array; Science adq0278 probing critical
phenomena in open atom arrays). The clean-system finite-size correlator is
*already* known to follow `G(x) ∝ [sin(pi x/N)]^{-2 Delta}` with Delta the
scaling dimension of the *measured* operator — i.e., the literature confirms the
occupation correlator returns the energy/order-parameter Delta, NOT the
stress-tensor Delta=2 (alpha=4). The proposed measurement, as a measurement of
`<n n>_c`, would reproduce a *known* exponent for the *wrong* channel. Sources:
[arXiv:2508.05381](https://arxiv.org/abs/2508.05381),
[arXiv:2407.05455](https://arxiv.org/html/2407.05455v1),
[Science adq0278](https://www.science.org/doi/10.1126/science.adq0278),
[Aquila whitepaper arXiv:2306.11727](https://arxiv.org/abs/2306.11727),
[AWS Braket Aquila docs](https://docs.aws.amazon.com/braket/latest/developerguide/braket-quera-submitting-analog-program-aquila.html).

**Verdict on C1: FAILS as written.** Down-score from 80 to ~25. Salvageable
*only* if reframed to (a) explicitly target the epsilon-channel alpha=2 (a
different, weaker claim than the paper's alpha=4), or (b) reconstruct sigma^x
correlators via many-body Hamiltonian-learning post-processing (expensive, not
"a NumPy sweep," and itself an open research problem). Neither is the candidate
as scored.

## C2 — Passive transmission-line / LC-ladder MERA emulator

### Killer objection 1: PRIOR ART. The transmission-line ↔ MERA/AdS bridge is already published.

The candidate's novelty claim is "analog-gravity tradition applied to the
project-specific r^-4 prediction." But the *core bridge it proposes* — a
transmission-line / LC-ladder network whose structure realizes a continuous-MERA
entanglement-renormalization flow and yields the corresponding AdS holographic
spacetime — was published two years ago: **"Holography of Transmission Lines:
Insights of Continuous MERA and AdS/CFT," arXiv:2407.04171 (Jul 2024, rev. Aug
2024).** That paper uses Yurke-Denker quantum-circuit network theory inside a
cMERA framework, derives the AdS metric from the line's inductance, and treats
transmission lines with endpoints exactly as a discretized RG / causal-cone
structure. The "design the impedance taper to mimic the chi=3 MERA causal cone"
step the candidate frames as the novel contribution is the *already-solved
problem* in that reference. C2's stated novelty (U=4) is overstated; this is
incremental at best. Source:
[arXiv:2407.04171](https://arxiv.org/abs/2407.04171).

### Killer objection 2 (the HYP-014 trap): coincidental r^-4, NOT stress-tensor exchange.

This is the decisive scientific objection and it is fatal to C2's evidentiary
value. A passive LC ladder is a **linear, Gaussian (free-field) network**. Its
port-to-port Green function is fixed entirely by the engineered impedance taper
(a continued-fraction/Cauer synthesis the candidate itself specifies). You *input*
the network topology that produces `|G(dr)| ~ dr^{-4}`; you then *measure* that it
produces `dr^{-4}`. This is **circular**: the exponent is a designed-in property
of the chosen taper, not an emergent consequence of CFT stress-tensor exchange.

Critically: the 2D Ising CFT stress-tensor channel (alpha=4) is a property of an
**interacting/critical** field theory's operator content — the Delta=2 stress
tensor with its specific OPE. A passive linear ladder has **no interactions, no
operator product expansion, no central charge, no stress tensor** in any
non-trivial sense. Reproducing the *number* 4 by impedance design is exactly the
HYP-014 failure: "amplitude/exponent match was coincidental; the mechanism is
wrong." HYP-014 was REFUTED at high confidence for fitting the right power-law
shape (sin(pi dr/N) profile) with the wrong mechanism. C2 is structurally
identical: a hand-tuned linear network that fits r^-4 by construction tells you
**nothing** about whether the published alpha=4 originates from stress-tensor
exchange. It can only ever confirm "if I build a network with a r^-4 transfer
function, it has a r^-4 transfer function."

The candidate's own caveat ("tests only the kinematic/geometric origin, not the
entanglement interpretation") drastically *understates* this: it tests neither.
It tests whether a circuit synthesized to have exponent 4 has exponent 4.

### Does it avoid the killers? Relabel check.

C2 trivially avoids R1/R2/R3/R4 (no quantum state at all) — but this is vacuous.
Avoiding the killers by removing all physics that could trip them also removes
all the physics that made the original result meaningful. The "All killers
avoided" cell is true and irrelevant.

### Prior-art / scaling claim check

The claim "delivers the finite-size alpha trend at N=32,48,64 beyond the
statevector ceiling" is also weak: a *classical linear* ladder has no
"statevector ceiling" because there was never a quantum many-body state — its
"finite-size alpha(N)" is just the transfer function of a longer designed
network, which can be computed analytically with a transfer-matrix product in
microseconds. Building hardware to measure a quantity you can derive in closed
form from the synthesis you yourself specified adds no information.

**Verdict on C2: FAILS as a physics test. This is the bridge to KILL.**
Down-score from 80 to ~10. It is simultaneously (a) prior art (arXiv:2407.04171),
and (b) a textbook instance of the exact coincidental-fit failure that got
HYP-014 REFUTED — measuring a designed-in exponent and calling it confirmation of
a mechanism the system does not contain.

## C3 — Coupled-resonator hyperbolic-lattice transport analog

### Killer objection 1: PRIOR ART, and the experiment has already been done.

Hyperbolic-lattice coupled-resonator transport is not a novel bridge — it is an
established experimental platform. **Kollár, Fitzpatrick & Houck, "Hyperbolic
lattices in circuit quantum electrodynamics," Nature 571, 45 (2019)
(arXiv:1802.09549)** built coplanar-waveguide resonator arrays on a {7,3}/{8,3}
hyperbolic tiling and explicitly demonstrated that photons propagate along
**geodesics of the hyperbolic metric** and that interactions are mediated along
the Poincaré-disk geodesic (the dashed semicircle). Follow-ups extend this to
photonic emulation at scale (ACS Photonics 2024, "Scalable and Programmable
Emulation of Photonic Hyperbolic Lattices") and to photon-bound-state / spin
models (PRL 128, 013601). The "tabletop demonstration that transport follows
hyperbolic geodesics" the candidate proposes as its result is the *headline
finding of a 2019 Nature paper*. Sources:
[arXiv:1802.09549](https://ar5iv.labs.arxiv.org/html/1802.09549),
[Nature s41586-019-1348-3](https://www.nature.com/articles/s41586-019-1348-3),
[ACS Photonics 4c01184](https://pubs.acs.org/doi/10.1021/acsphotonics.4c01184).

### Killer objection 2 (HYP-014 trap, transport edition): the specific constant (pi/2)*l_AdS is not tested.

The project's HYP-006 result is *quantitative*: T = (pi/2)*l_AdS to **0.72% at
N=16**. A coupled-resonator hyperbolic lattice reproduces *qualitative* geodesic
transport (already shown in 2019), but the candidate gives no argument that the
**numerical prefactor pi/2** emerges. The transport time on a physical resonator
lattice is set by the resonator-resonator coupling rate, group velocity,
dispersion of the gapped flat-band structure (Kollár et al. emphasize a highly
unusual band structure with a gapped flat band), and lattice truncation — none of
which are tuned to reproduce the MERA causal-cone depth law that yields exactly
pi/2. Confirming "transport scales with network depth" is consistent with pi/2
*and with a continuum of other prefactors*; a loose qualitative match to a
geometric expectation, then claiming it validates a 0.72%-level constant, is the
HYP-014 coincidental-match pattern again. To actually test (pi/2)*l_AdS the
resonator lattice would need an independent, first-principles calibration of l_AdS
from the lattice curvature and a sub-percent transport-time measurement — neither
specified, and dispersion/disorder in a 30-50 node DIY lattice realistically
gives ~5-15% timing scatter, an order of magnitude too coarse to test 0.72%.

### Relabel check on killers

Like C2, "all killers avoided" is true but vacuous: it is a classical wave
network with no quasiparticle, estimator, or entropy. The relevant failure is not
a tripped killer; it is prior art + inability to resolve the load-bearing
constant.

**Verdict on C3: FAILS as a quantitative test; partially redundant with 2019
literature.** Down-score from 64 to ~20. Survives only as a qualitative outreach
demo (like C5), not as a test of the HYP-006 headline.

## C4 — Cheap classical-compute chi=3 MERA finite-size alpha at N=32,48

### Killer objection 1: chi=3 is too small to certify a finite-size *systematic* — the bond dimension IS the systematic.

C4's stated purpose is to "close the finite-size-systematic gap" by extending the
chi=3 MERA connected correlator to N=32,48. This conflates two different errors.
At a critical point, a finite-bond-dimension tensor network induces a **relevant
perturbation that opens an effective gap and an emergent finite correlation
length xi(chi)** — a well-documented effect (an MPS/MERA with finite chi "can
never properly capture the scale invariance of a critical state"; see
[arXiv:1109.5334](https://ar5iv.labs.arxiv.org/html/1109.5334) and the
finite-entanglement-scaling literature). chi=3 is *extremely* small: xi(chi=3) is
short, so extending to N=32,48 does not probe the conformal regime — it pushes
N well past xi(chi=3), where the correlator crosses over to the **gapped /
finite-chi-cutoff regime**, bending alpha *away* from any CFT value. C4 would
measure the chi-truncation crossover and mislabel it a finite-*size* systematic.
The honest robustness check is finite-**entanglement** scaling (vary chi at fixed
large N and extrapolate chi->inf), not finite-size scaling at fixed chi=3. The
candidate proposes the wrong extrapolation axis.

### Killer objection 2 (R2 relabel risk): "back-end reused, observable-agnostic" is an assertion, not a verification.

C4 claims the connected-correlator back-end "already exists and is observable-
agnostic (HYP-025 note on sim2026015d_chi3_16q_force.py)." This is exactly the
class of claim the project's own subagent rule flags: *never trust a claim of
correctness without reading the code.* The HYP-017 R2 killer was a
product-of-single-site-densities estimator that *looked* like it computed an
energy/correlator but silently dropped the connected piece. Reusing a back-end
"because it's there" without re-deriving that `<Z_iZ_j>_c` is computed as a true
two-body contraction (not a product of one-body reduced expectations from the
MERA causal cone) is the precise mechanism by which R2 propagates. C4 does not
demonstrate the back-end is R2-clean; it asserts it. Unverified, this is R2
relabeled "observable-agnostic," not R2 dissolved. (This is a flag, not a proven
trip — but the burden is on C4 to show the contraction, and it does not.)

### Prior-art note

Tensor-network finite-size and finite-entanglement scaling for the 2D/1D Ising
critical exponents is mature (HOTRG reaches 1e-4 on exponents at D=70;
[arXiv:2302.02585](https://arxiv.org/abs/2302.02585),
[arXiv:0810.1414](https://arxiv.org/abs/0810.1414)). Doing it at chi=3 is not a
novel result; doing it *correctly* requires chi >> 3, at which point the "zero
marginal cost, hours on local GPU" feasibility claim no longer holds (chi=3 ->
larger chi is a steep cost increase, plus the contraction front-end the candidate
admits is new code).

**Verdict on C4: SURVIVES, but heavily down-scored and re-scoped.** From 60 to
~38. It is the only candidate with no physics-killer and no prior-art
disqualification *in principle* — but only if (a) re-scoped as finite-
*entanglement* scaling (vary chi, not just N) and (b) the back-end is *read and
shown* to compute a true connected two-body contraction before any number is
trusted. As written (chi=3 fixed, N extended, back-end assumed clean) it would
produce a misleading crossover number with R2 unverified. It is a robustness
check, not a physical bridge, and only valuable post-verification.

## C5 — DIY NV/SPAD g2 witness for wave-optics transport rig

### Killer objection: it is a coincidental-fit machine with even looser tolerances than C3, and the candidate already concedes it.

C5 proposes a GRIN / multi-segment light-pipe whose eikonal transport reproduces
the hyperbolic-geodesic transit time, read out with a DIY SPAD/NV g2 front-end.
The candidate's own text concedes "the mapping ... to the specific (pi/2)*l_AdS
constant is loose ... pinning the 0.72%-level constant optically is hard (U=3)"
and rates it "at best a qualitative public-facing demonstration; weak as a
quantitative test." A devil's advocate need only agree and sharpen:

1. **Same HYP-014 trap as C3, worse.** A GRIN index profile is *designed* to bend
   rays along a chosen path; reproducing a geodesic-like transit time is a
   designed-in property of the chosen n(r) profile, not emergent confirmation of
   the MERA causal-cone law. Eikonal ray transport in a tuned-index medium fitting
   a geometric time is the textbook coincidental match — there is no CFT, no
   stress tensor, no entanglement anywhere in a light pipe.
2. **The g2 / NV front-end is decorative.** Intensity (g2) photon correlations add
   nothing to a *classical transit-time* measurement; the transport time is a
   first-order intensity quantity measurable with a $5 photodiode and a scope. The
   "DIY SPAD/NV witness" framing imports the cataloged sensor toolbox for its own
   sake (the candidate even says it was "included because the framing asked about
   the DIY toolbox"), not because the physics needs single-photon statistics.
3. **Tolerance gap is fatal to the only claim that mattered.** HYP-006's value is
   load-bearing *because* it is 0.72%. A DIY light-pipe with fabrication tolerance,
   index inhomogeneity, and segment-junction scattering gives transit-time scatter
   far above 1%; it cannot test the constant it nominally targets.

**Verdict on C5: FAILS as a test (outreach-only), exactly as the candidate
itself half-admits.** Score 27 is already low; no rescue. Dominated by C3 for the
qualitative-demo role and by C4 for the quantitative-robustness role.

---

## Verdict

### Re-scored after red-team

| Bridge | Orig product | Red-team verdict | Re-scored | Why |
|--------|-------------|------------------|-----------|-----|
| C1 Rydberg static connected-correlator | 80 | FAILS as written | ~25 | Dissolves R1 honestly, but re-trips the HYP-017 closeout's *third* defect (z-basis/wrong-operator). Aquila reads occupation (sigma^z / n) only — `<n n>_c` lives in the epsilon channel (alpha~=2), not the stress-tensor channel (alpha~=4). Any in-window hit is a finite-size coincidence (HYP-014 pattern). Critical-point adiabatic prep also unreachable (gap~1/N). |
| C2 LC-ladder MERA emulator | 80 | FAILS — **KILL** | ~10 | Prior art (arXiv:2407.04171, transmission-line cMERA→AdS, 2024). And a designed-in r^-4 in a free linear network with no stress tensor/OPE/central charge = the exact HYP-014 coincidental-fit refutation, in hardware. Confirms only "a circuit built to have exponent 4 has exponent 4." |
| C3 Hyperbolic resonator transport | 64 | FAILS as quantitative test | ~20 | Prior art — geodesic transport already shown in Kollár et al. Nature 2019. Cannot resolve the load-bearing pi/2 prefactor at 0.72%; DIY timing scatter ~5-15%. Outreach-only. |
| C4 chi=3 MERA finite-size alpha | 60 | SURVIVES, re-scoped | ~38 | No physics-killer, no prior-art disqualifier *in principle*. But chi=3 fixed + N extended measures the finite-chi crossover, not a finite-size systematic — must be re-scoped to finite-*entanglement* scaling (vary chi). R2-clean back-end asserted, not verified — must read the contraction code first. |
| C5 DIY g2 light-pipe | 27 | FAILS (outreach-only) | ~12 | Same HYP-014 designed-geodesic trap as C3, looser tolerance; g2/NV front-end decorative. Candidate already half-concedes. |

### Which bridges survive

**Only C4 survives — and only conditionally.** It is the single candidate that
does not trip a physics-killer and is not disqualified by prior art *in
principle*. But it survives only if re-scoped: vary bond dimension chi at fixed
large N (finite-entanglement scaling) rather than extending N at fixed chi=3, AND
only after the connected-correlator back-end is *read and shown* to compute a
genuine two-body contraction (not an R2-style product of one-body causal-cone
expectations). Its value is a robustness check for SciPost reviewers, not a
physical bridge — and it is contingent on code verification, not a turnkey win.

C1 is *salvageable but not as scored*: it would have to drop the alpha=4 claim
and instead test the **epsilon-channel alpha=2** (a weaker, different result),
because that is the only exponent the Aquila occupation basis can actually
deliver. As a test of the project's headline alpha~=4 it fails.

### The single bridge to KILL

**C2 (LC-ladder MERA emulator).** It is the worst of the set on two independent,
each-sufficient grounds: (1) it is already-published prior art
(arXiv:2407.04171), and (2) it is the purest re-instantiation of the exact
failure that got HYP-014 REFUTED at high confidence — fitting the right power-law
exponent with a mechanism (a free, linear, non-interacting network) that contains
no stress tensor, no OPE, and no central charge, so the r^-4 is designed in by
the impedance synthesis rather than emergent. Spending BOM + build time to
"measure" an exponent you analytically specified in the Cauer synthesis is
negative-information. Kill it outright; do not down-score-and-keep.

### Most defensible bridge

**None is defensible as a *physical* confirmation of alpha~=4 at hardware level.**
The least-bad, and the only one worth resourcing, is **C4 in its re-scoped form**
(finite-entanglement scaling, chi varied, back-end code verified R2-clean first)
— purely as an internal robustness check for the SciPost submission, at zero
marginal cost. It does not ground the physics in a new physical system; it tightens
the existing numerical claim. The framing's premise — that a cheap classical or
near-term-hardware analog can independently confirm stress-tensor-exchange
alpha~=4 — does not survive red-team: every analog either trips the wrong-channel/
wrong-operator defect (C1) or reduces to fitting a designed-in exponent (C2/C3/C5),
which is the HYP-014 refutation in new clothing.

### Cross-cutting finding

Four of five candidates (C1 on Aquila in z-basis, C2, C3, C5) fail through the
*same* mechanism the project already learned the hard way with HYP-014 and the
HYP-017 closeout: **a power-law exponent match is not evidence of a mechanism.**
The NOVEL-COMBO-C scoring rewarded "killer avoided" cells that are true but
vacuous (C2/C3/C5 avoid R1-R4 only by deleting all the physics that could trip
them) and rewarded "measures r^-4" without asking whether the system *contains*
stress-tensor exchange. Recommend the scoring rubric add an explicit
**"mechanism-faithful vs. exponent-coincidental"** axis before any of these is
resourced.

---

**Output file:** `D:\quantum-worldline\research\data\papers\REDTEAM-C-mera-bridge.md`
