# RED TEAM — QCHEM-COMBO-A Method Candidates (2026-05-17)

**Role:** Devil's advocate. For each top-5: killer objection, emergent-capability test,
prior-art hit. Every "fails" carries a number or citation. Special scrutiny on
barren-plateau and measurement-overhead claims (the standard overclaim sites).

**Verdict legend:** SURVIVES / DOWN-SCORE / KILL

---

## #1 — NQS-biased classical shadows on a shallow VQE state (claimed 64)

**Killer objection (measurement-overhead claim is unquantified and likely self-defeating).**
The headline is "10–100× fewer shots." That number has no derivation in the candidate and the
LBCS literature gives the bound that kills it. Hadfield et al. (arXiv:2006.15788, CMP 2022) prove
the locally-biased shadow single-shot variance is bounded by `4^k ||O||²_∞` for a weight-`k`
Pauli, and — critically — that the variance reduction from biasing is governed by how close the
bias distribution is to the *true* Pauli marginals, not how accurate the source classical state
is in energy. Two consequences:

1. **The 10–100× is double-counting an already-claimed gain.** LBCS as published already supports
   a "fermionic Gaussian state or perturbative Møller–Plesset" prior (verbatim from the abstract,
   2006.15788). The reported LBCS variance reduction over LDF grouping is roughly **2–10×** for
   molecular Hamiltonians, not 100×. Swapping an MP2 prior for a FermiNet prior changes the bias
   distribution `β*(P) ∝ |⟨P⟩|·w_P` only in the *tail* Paulis where MP2 is already qualitatively
   right (the dominant 1- and 2-body terms). The marginal gain from "MP2 → near-FCI prior" is the
   *residual* mis-estimate of high-weight Paulis, which is small precisely because LBCS variance is
   dominated by the `4^k` prefactor on high-weight terms — a prefactor the better prior **does not
   touch**. Realistic incremental factor: **1.3–2×**, not 10–100×. The candidate's central
   selling number is off by 1–2 orders of magnitude.

2. **The "hardest obstacle" the candidate concedes is actually the killer.** It admits the
   FermiNet/Psiformer state is in *first quantization / continuum* and mapping its amplitudes onto
   the second-quantized Pauli basis is "non-trivial and basis-set dependent." This is not a footnote
   — it is the whole protocol. To produce `⟨P⟩_NQS` for the Paulis the shadow lives in, you must
   evaluate fermionic Gaussian / Pauli expectation values of a *first-quantized continuum* VMC
   wavefunction. There is no cheap estimator for this: it requires either (a) projecting FermiNet
   onto the active-space CI basis (exponential in active orbitals — the exact cost VMC was invented
   to avoid), or (b) Monte-Carlo estimating each `⟨P⟩` from FermiNet samples, which has its **own**
   sampling variance that competes directly with the quantum shot saving. The candidate's own
   parenthetical — "cost may eat the shot saving for large active spaces" — concedes the
   mechanism is **circular in the dominant failure mode**: the classical NQS already had to solve
   the chemistry (produce near-FCI Pauli expectations) to bias the shadows, at which point the
   quantum 2-RDM adds essentially nothing the NQS didn't already give you. **This is the textbook
   near-term-QC circularity flag.**

**Emergent-capability test: FAILS as stated.** If the NQS can supply near-FCI `⟨P⟩` for every
Pauli the 2-RDM needs, you have the 2-RDM classically. The only genuine residual is using the
*hardware* state's deviation from the NQS — but the protocol explicitly "keeps the quantum state
untouched" and never reconciles NQS-vs-device discrepancy, so there is no feedback channel that
would make the quantum data load-bearing. It is "train a good NQS, then collect Cliffords"
in sequence; the combination's claimed emergence (chemical accuracy from depth-≤20) is carried
**entirely by the NQS**.

**Prior-art hit (novelty 4 → 2).** The candidate's own cited differentiator ("neither uses a
FermiNet-class NQS purely as the shadow bias oracle") is thin. (i) LBCS already parameterizes the
bias from *any* classical state including correlated ones (2006.15788). (ii) Neural-Shadow QST
(arXiv:2305.01078 / PRR 6,023250 2024) and "Bootstrapping Classical Shadows for NQS Tomography"
(arXiv:2405.06864) already couple an NQS and classical shadows; the latter literally bootstraps
shadow data with an NQS. (iii) "Biased estimator channels for classical shadows"
(arXiv:2402.09511, PRA 111 L030402) proves biasing is *always* worth it with **no quantum
resources** — meaning the bias-oracle improvement is a known, generic, already-published lever;
swapping in a fancier classical state is an incremental parameter choice, not a new coupling
direction. **Down-score N to 2; the "passed object" (bias distribution from a classical state)
is exactly what LBCS already passes.**

**Verdict: KILL / heavy down-score. Revised N2·B3·U3 ≈ 18 (Mech downgraded to 2 — circular).**

## #2 — QITE block as plateau-free VQE initializer + recycled Krylov (claimed 64)

**Killer objection #1 (the barren-plateau claim is false as stated).** The candidate's emergent
capability is "a barren-plateau-free VQE warm start." This is the classic overclaim site and the
literature is explicit against it. The recent warm-start analyses are unambiguous: *"The warm
start procedure does not eliminate barren plateaus in general"* and an imaginary-time-inspired
warm start *"to a certain extent alleviates the effect of barren plateaus"* — i.e. mitigation,
not removal (consistent across arXiv:2407.02569 / EPJ QT 2025, arXiv:2402.17378, and the
adiabatic warm-start analysis arXiv:2602.06137 which shows guarantees **fail when the spectral
gap vanishes** — exactly the strongly-correlated regime the candidate targets with H4/H6
chains). A QITE endpoint gives you a good *initial point*, but the downstream symmetry-adapted
VQE landscape still has exponentially-vanishing gradients away from that point; one good seed
does not change the cost-landscape concentration. The phrase "plateau-free" is quantitatively
wrong — at best it is "plateau-mitigated for the first few iterations, with no guarantee under
gap closure." Strip that and the headline collapses to "QITE gives VQE a decent start," which
is not emergent.

**Killer objection #2 (the dual-use is QLanczos, already published — circular novelty).** The
candidate concedes QLanczos (Motta et al., Nat. Phys. 2020 / npj QI 2020 s41534-020-00290-1)
"builds Krylov from QITE." Its claimed *differentiator* is the **dual** use: same run → VQE init
**and** spectroscopy. But this is not a new object — it is QLanczos with the terminal iterate
additionally read off as a seed. Reading the final QITE state is free in *any* QITE run; calling
that "a barren-plateau-free initializer" and pairing it with the already-standard QLanczos
spectrum is **"run QITE, then (a) take last state, (b) take all states" relabeled as a
combination.** There is no coupling that produces a capability QLanczos+a-warm-start-paper don't
jointly already have. The Quantinuum VQPE/Krylov line of work and "model-space QITE"
(npj QI 2023, s41534-023-00780-y, multi-state QITE) already deliver ground+excited from one QITE
family. The marginal novelty is the *narration* ("zero-marginal-cost byproduct"), not a method.

**Emergent-capability test: FAILS.** Decompose: (1) QITE to convergence; (2) feed endpoint to
VQE; (3) feed trajectory to generalized eigenproblem. Each is an independent, published step run
in sequence on a shared trajectory. Sharing the trajectory is bookkeeping, not emergence — the
excited states do not improve the ground-state init and vice versa; there is no back-coupling.

**Prior-art hit (novelty 4 → 2).** QLanczos (Motta 2020), folded-spectrum / improved QITE for
excited states (JCTC 2023, acs.jctc.2c00906), multi-state model-space QITE (npj QI 2023),
QITE-inspired VQE warm start (EPJ QT 2025). Every leg is published; the "dual read of one run"
is implicit in QLanczos itself (it *is* the trajectory). **Down-score N to 2.**

**One genuine residual (why not a full KILL):** explicitly *symmetry-projecting* the QITE
trajectory before forming the generalized eigenproblem to de-correlate near-linear-dependent
Krylov vectors by quantum number is a real, useful, lightly-explored engineering improvement
(it overlaps candidate #6, which is the cleaner statement of it). That is worth ~1 USEFUL point,
not a NOVELTY score.

**Verdict: heavy DOWN-SCORE. Revised N2·B4·U3 ≈ 24 (Mech 3 — sequential, not coupled).**

## #3 — Shadow-2-RDM as self-consistent generalized-DMET descriptor (claimed 60)

**Killer objection (the self-consistency loop is the noise amplifier, and the candidate admits
it without quantifying it).** The whole novelty is closing the embedding fixpoint on *measured*
quantum data. But classical-shadow 2-RDM estimates carry shot-noise variance that scales as
`4^k/M` per weight-`k` Pauli (Hadfield 2006.15788; Huang-Kueng-Preskill scaling), and the 2-RDM
needs weight-up-to-4 Paulis → variance prefactor up to `256/M`. Feeding a noisy 1-RDM marginal
back as the DMET *low-level descriptor* means the bath-construction map is recomputed from a
random matrix each iteration. DMET self-consistency is already known to be fragile (the
correlation-potential fit is ill-conditioned even with *exact* RDMs — see the practical-guide
JCTC 6b00316 and the around-critical-point analysis on InspireHEP). Inject `O(1/√M)` noise into
the fixpoint variable and the loop has no contraction guarantee: small RDM noise → bath
reshuffling → different fragment energy → different RDM. The candidate concedes "noise-driven
non-convergence ... needs N-representability projection inside the loop, raising classical cost."
That projection (the DQG/T2 conditions) is itself `O(N^6)`–`O(N^9)` semidefinite programming
**per iteration**; with, say, 20 self-consistency iterations the classical cost of stabilizing
the loop dwarfs the impurity solve. **Quantitatively: to get the 1-RDM to the ~1e-3 precision
DMET self-consistency needs, you need `M ~ 256/(1e-3)^2 ≈ 2.6×10^8` shots per iteration** (order
of magnitude, weight-4 dominated) — that is not "NISQ-depth impurity solve," that is a shot
budget that erases the embedding's whole point.

**Emergent-capability test: PARTIAL but real.** Unlike #1/#2 this is *not* pure sequence:
measured-correlation → bath → re-fragmentation → new measurement is a genuine feedback loop, and
"the bath adapts to where correlation actually is" is a capability neither one-shot shadow-RDM
nor HF-bath DMET has. The emergence is real *in principle*. It is the **noise robustness of the
fixpoint**, not the concept, that is unproven and likely fatal at NISQ shot budgets.

**Prior-art hit (novelty 4 → 3, defensible).** The candidate's cited landscape is accurate and
honest: DMET+SQD (arXiv:2511.22158), generalized DMET (arXiv:2503.09881 — confirmed via
WebSearch, the "arbitrary-1-RDM descriptor / disentanglement bath" paper), shadow-2-RDM with
N-representability (arXiv:2411.18430) — all one-directional. The 2025 generalized-DMET work and
ab-initio finite-T DMET (arXiv:2601.01641) do **not** close the loop on *shadow-measured*
correlation. The closed self-consistent direction with the generalized (non-projector) bath is
genuinely not located. Novelty survives at **3** (not 4: the loop structure itself is the
standard DMET loop; only the descriptor source is new).

**Verdict: SURVIVES but DOWN-SCORE on buildability. The concept is the most genuinely emergent
of the five; the shot budget makes B honest at 2, not 3. Revised N3·B2·U4 ≈ 24, Mech 4. Its
real value is as a *classical-shadow-on-FCI-emulator* proof of concept, deferring the hardware
shot question.**

## #4 — Shadow-trained NQS surrogate as QITE domain oracle (claimed 48)

**Killer objection (terminal circularity — the surrogate is the answer).** This is the most
clearly circular of all five. QITE's per-step least-squares solve needs `⟨domain Pauli⟩`. The
candidate proposes reading those off a *shadow-trained NQS* "instead of re-measuring noisily."
But an NQS that is accurate enough to supply the operator-domain correlators QITE needs to
*converge to the ground state* is, by construction, already a good approximation to the state
QITE is trying to reach. You are using a classical wavefunction model to drive an imaginary-time
projection toward… the classical wavefunction model. **The quantum device's only role is to
generate the shadow training data for the NQS — at which point the NQS, not QITE, is producing
the chemistry.** If the shadow-trained NQS is bad, QITE's domain solve is fed wrong correlators
and diverges/biases; if it is good, you didn't need QITE. There is no regime where the quantum
imaginary-time step is load-bearing.

**The denoising claim is unquantified and contradicted by simpler baselines.** "Noise-robust
QITE because the NQS denoises the state" — Neural-Shadow QST (arXiv:2305.01078, PRR 6 023250) is
already *"robust against various types of noise without any error mitigation"* as a **static**
protocol. So the noise robustness is a property of NQS-from-shadows itself, not of inserting it
into QITE. Inserting it *inside* the QITE loop adds the candidate's own conceded killers:
(a) **NQS retraining every QITE step** — if you retrain, cost per step ~ a full VMC optimization
(hundreds–thousands of NQS gradient steps) × number of QITE steps; if you don't retrain, the
surrogate is *stale* and the imaginary-time dynamics drift off-manifold; (b) **no symmetry-sector
guarantee** — a shadow-trained NQS can leak into the wrong particle-number/spin sector and QITE
has no mechanism to detect this mid-trajectory. Both are conceded; neither is bounded.

**Emergent-capability test: FAILS (sequence + circular).** "Take shadows of noisy VQE → fit NQS
→ read correlators → step QITE" is a 4-stage pipeline. The only candidate-claimed emergence
("imaginary-time dynamics itself becomes noise-robust") is inherited wholesale from NSQST's
static noise robustness; QITE adds nothing the static NQS estimate didn't have, and adds
divergence risk.

**Prior-art hit (novelty 4 → 2).** Neural Error Mitigation (arXiv:2105.08086, conceded) +
Neural-Shadow QST (arXiv:2305.01078) + "Fighting Noise with Noise: Stochastic Projective QE"
(JCTC 2024, acs.jctc.4c00295 — already does noise-tolerant projective/imaginary-time-like
ground-state with stochastic estimates) collectively cover the territory. The "NQS inside the
QITE iteration" wrapper is an integration choice, not a new mechanism.

**Verdict: KILL. The most circular candidate — the classical surrogate already contains the
answer the quantum step is nominally computing. Revised N2·B2·U3 ≈ 12, Mech 2.**

## #5 — MERA disentangler as DMET bath map (claimed 40)

**Killer objection (the "not located" prior art IS located — novelty 5 is wrong).** The
candidate scores NOVELTY = 5 ("MERA-DMET as an explicit bath constructor is not located"). This
is false. WebSearch surfaces directly competing prior art:

- **Vidal & Evenbly, "Algorithms for entanglement renormalization: boundaries, impurities and
  interfaces" (arXiv:1312.0303)** — MERA *specifically built for impurity problems*, using
  disentanglers/isometries to define the impurity↔environment map. This is the MERA-impurity
  bath construction the candidate claims is unlocated, published 2013.
- **"Disentangling Interacting Systems with Fermionic Gaussian Circuits: SIAM"
  (arXiv:2212.09798)** — fermionic disentangling circuits as the embedding/bath map for the
  single-impurity Anderson model. Directly the "disentangler-as-bath-map" idea, with the
  fermionic sign structure *already handled* (the candidate lists fermionic MERA sign structure
  as its hardest obstacle — solved here).
- **Gaussian-MERA (GMERA) impurity work** surfaced in the same search: hierarchical MERA
  structure inducing the effective reduced impurity system — i.e. multi-scale bath from MERA,
  the exact emergent capability claimed.

So the defining claim — "uses MERA's scale-invariant entanglement renormalization as the
embedding map, not located" — collides with at least three published lines. **NOVELTY must drop
5 → 2.**

**Buildability is honestly self-rated low and that is the binding constraint.** The candidate
itself sets B = 2 (fermionic MERA optimization cost + sign structure; classical-sim PoC only).
With novelty corrected to 2, Product = N2·B2·U4 = **16**, below everything. Even granting the
emergent capability is real (multi-scale bath > single Schmidt cut — true in principle and the
one physically sound idea here), the combination is neither novel (1312.0303 / 2212.09798) nor
near-term buildable (no quantum advantage demonstrated; classical fermionic-MERA is itself a hard
open problem).

**Emergent-capability test: GENUINE but pre-empted.** Multi-scale bath capturing
critical/long-range correlation a single Schmidt cut structurally misses is a real, principled
capability — this is the only candidate whose mechanism is physically clean (Mech 4 stands). But
"genuine and already done by Vidal-Evenbly 2013 / Wang-Millis-type Gaussian circuits 2022" is
not a publishable combination.

**Verdict: DOWN-SCORE hard on novelty. Revised N2·B2·U4 ≈ 16, Mech 4. Physically the soundest
idea, but the literature got there first.**

---

## Re-ranking (post red-team)

| Was | Cand | Claimed | Killer | Revised Product | Survives? |
|-----|------|---------|--------|-----------------|-----------|
| 1 | #1 NQS-bias shadows | 64 | First-quant→Pauli mapping is circular; 10–100× off by 1–2 OOM (LBCS variance is `4^k`-dominated, prior already does MP2/Gaussian bias) | **~18** | NO — KILL |
| 1 | #2 QITE dual-use | 64 | "Plateau-free" false (warm starts only mitigate, fail under gap closure); dual-use = QLanczos relabeled | **~24** | DOWN-SCORE |
| 3 | #3 Shadow→genDMET loop | 60 | Genuine feedback, but `~2.6×10^8` shots/iter for stable fixpoint at NISQ kills buildability | **~24** | SURVIVES (B→2) |
| 4 | #4 Shadow-NQS→QITE | 48 | Terminal circularity: surrogate IS the answer; noise robustness inherited from static NSQST | **~12** | NO — KILL |
| 5 | #5 MERA-DMET bath | 40 | Novelty 5 false: arXiv:1312.0303 + 2212.09798 already do MERA/disentangler impurity bath | **~16** | DOWN-SCORE |

**Order after red-team:** #3 (24, real emergence, buildability-capped) ≈ #2 (24, but
sequential/relabeled) > #1 (18, circular) > #5 (16, pre-empted) > #4 (12, circular).

The headline finding: **four of five claimed-Product scores were inflated by the exact two
overclaim sites flagged in the brief** — barren-plateau elimination (#2: "plateau-free" is
literature-contradicted) and measurement-overhead advantage (#1: "10–100× fewer shots" has no
derivation and is `4^k`-bounded away). #1 and #4 are *circular in the dominant near-term-QC
failure mode*: the classical component (FermiNet NQS; shadow-trained NQS) already produces the
chemistry the quantum step nominally computes.

## Single most defensible candidate

**#3 — Shadow-2-RDM as self-consistent generalized-DMET descriptor.** It is the **only**
candidate with a genuine bidirectional coupling (measured correlation → bath → re-fragmentation →
new measurement) rather than a relabeled sequence, and the only one not circular: the embedding
*needs* the quantum 2-RDM and cannot substitute the classical prior for it (the bath is rebuilt
from the measured object, not from a classical state that already solved the problem). Its
weakness is honest and quantified (shot budget for fixpoint stability), and the recommended
de-risking path is concrete: prove the loop on an FCI-emulated 2-RDM with injected `O(1/√M)`
shot noise *before* any hardware claim. Novelty defensibly survives at 3 (generalized,
non-projector bath closed on shadow data is not located in 2503.09881 / 2511.22158 / 2411.18430).

## The one to kill

**#4 — Shadow-trained NQS surrogate as the QITE domain oracle.** Maximally circular: an NQS good
enough to feed QITE the correlators it needs to reach the ground state *is* a ground-state
approximation, so the quantum imaginary-time step is never load-bearing — the device only
generates shadow training data. Its sole claimed emergent property (noise-robust dynamics) is
inherited wholesale from static Neural-Shadow QST (arXiv:2305.01078), and both conceded obstacles
(per-step retraining cost, symmetry-sector leakage) are unbounded. Revised Product ~12; remove
from the slate. (#1 is the close runner-up for the kill on the same circularity diagnosis; #4
edges it out because #1 retains a faint non-circular residual — exploiting hardware-vs-NQS
discrepancy — that #4 structurally lacks.)

