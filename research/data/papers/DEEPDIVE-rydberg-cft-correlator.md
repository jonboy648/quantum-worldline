# DEEPDIVE: Rydberg static-CFT connected-correlator on QuEra Aquila (Candidate C1)

Status: COMPLETE
Date: 2026-05-16
Owner: physics deep-dive agent
Verdict: NEEDS-MODIFICATION — direct alpha~=4 claim REFUTED (wrong observable +
unaffordable); reframed sigma-exponent Ising consistency check conditionally
VALIDATED at ~20,000 shots / ~$206. See section 6.

## 0. Scope

Candidate C1 from NOVEL-COMBO-C: "HYP-2026-017 done correctly." Prepare a static
1D transverse-field-Ising (TFIM) / PXP critical ground state on QuEra Aquila via an
adiabatic detuning (Delta) sweep, do ZERO time evolution, and extract the
equal-time connected boundary correlator from the single-shot bitstring ensemble.
Goal: a hardware measurement of the published alpha~=4 stress-tensor exponent (or
the sigma scaling dimension that underlies it) on a second physical platform.

The four HYP-017 killers (per MEMORY closeout 2026-05-09) and how C1 dissolves them:

- **R1 (hologron lifetime tau ~ 1.5 ns << 200 ns window):** structurally
  inapplicable. There is no hologron and no time evolution. The observable is a
  property of the prepared *static* ground state. Nothing propagates, nothing
  has to survive a window.
- **R2 (energy proxy = product of single-site densities, drops connected
  two-body piece):** dissolved by construction. The estimator IS the explicit
  connected correlator computed at bitstring level, `mean(z_i z_j) -
  mean(z_i)*mean(z_j)`. See section 3 for the algebraic proof that this retains
  exactly the piece R2's product-of-densities estimator destroyed.
- **R3/R4 (single-basis TEE / collision-probability bias):** inapplicable. No
  Renyi-2, no TEE, no collision probability. A two-point function in the
  measurement (Z) basis is unbiased — it is a diagonal observable, native to
  the projective Rydberg readout.
- **Blockade-pathological reduced geometry:** avoided. Uses the FULL native
  Aquila lattice at Ebadi-class spacing (a = 6.7 um, Rb/a ~ 1.15-1.4), NOT a
  shrunken 15/20-atom replica. The local-validator geometric pathologies
  (atoms inside each other's blockade radius) cannot occur because there is no
  replica.

**However** — section 5 shows C1 is NOT novel as a *measurement*: arXiv:2402.15376
(Bornet/Lukin et al., Science 2024) already did the 1D-ring critical-correlator
measurement and got the Ising scaling dimension. C1's only defensible novelty is
the *interpretive bridge* to this project's alpha~=4 stress-tensor channel, plus
running it specifically on the public Aquila device attachable to the Zenodo
record. This reframes the verdict (section 6).

## 1. The physics target

The project's published claim (Zenodo 10.5281/zenodo.19661227, HYP-008 SUPPORTED)
is that the holographic "force" between MERA boundary sites falls as F(r) ~ r^-alpha
with alpha = 4.0, identified as 2D-Ising-CFT stress-tensor exchange (3 independent
numerics: 3.92 / 3.97 / 4.07; SIM-2026-023 chi=3 bootstrap reference alpha =
4.077 +/- 0.286, acceptance window [3.2, 4.8]).

Critical subtlety, and the central physics issue with C1: **the alpha~=4 stress-
tensor envelope is NOT the leading correlator of the Rydberg order parameter.**
In the 2D (= 1+1D) Ising CFT the operator content is:

| Operator | Scaling dim Delta | Connected 2-pt decay `<O_0 O_r>_c ~ r^-2Delta` |
|----------|-------------------|-------------------------------------------------|
| sigma (order param, = staggered Rydberg occ.) | 1/8 | r^-1/4  (alpha = 0.25) |
| epsilon (energy density)                       | 1   | r^-2    (alpha = 2)    |
| T (stress tensor)                              | 2   | r^-4    (alpha = 4)    |

The Rydberg site occupation n_i (the only thing Aquila measures projectively)
maps onto the **order parameter sigma**, whose connected correlator decays as
**r^-1/4, NOT r^-4**. The r^-4 stress-tensor envelope is sub-sub-leading and is
swamped by the r^-1/4 sigma channel by a factor ~ r^(15/4) (at r=6 that is
~10^2.9 ≈ 800x). You CANNOT read the alpha=4 channel off the bare `<n_i n_j>_c`
of a critical Ising state — the sigma channel dominates it everywhere.

This is the same category issue that was reconciled in MEMORY 2026-05-05 for
HYP-017 (bulk-exponential vs boundary-algebraic): the project's alpha=4 is the
stress-tensor / "force" object built from a *second derivative of the energy*
(a T-channel quantity), while the directly-measurable Rydberg correlator is the
sigma 2-point function. Two honest ways to reconcile:

- **(1a) Measure sigma, validate the CFT, infer alpha=4 indirectly.** Extract
  2*Delta_sigma from `<sigma_0 sigma_r>_c ~ r^-2Delta_sigma`; the Ising
  prediction is 2*Delta_sigma = 1/4. Confirming 0.25 confirms the boundary IS
  the c=1/2 Ising CFT, from which the T-channel r^-4 follows analytically (it is
  fixed by the CFT, not independently measured). This is a *consistency* test of
  the published claim, not a direct alpha=4 measurement.
- **(1b) Build the stress-tensor / force estimator from bitstrings.** The
  project's "force" is a connected energy-energy / second-difference object. On
  the array, the local energy density is the nearest-neighbor term
  `h_i ~ n_i n_{i+1}` (Rydberg blockade interaction). The connected
  energy-energy correlator `<h_i h_j>_c` carries the epsilon channel (r^-2,
  leading) plus the T channel (r^-4, subleading). Isolating r^-4 requires
  subtracting the epsilon piece — a fit with two power-law terms,
  `A r^-2 + B r^-4`, which is exactly the kind of subleading extraction that
  needs very low noise (section 4 shows this is the hard obstacle).

Path (1a) is robust and cheap; path (1b) is the direct analog of the published
quantity but is shot-noise-limited at the subleading term. The protocol below
specifies BOTH and gates the expensive one on the cheap one.

## 2. Aquila run specification

All numbers below are anchored to the demonstrated Ebadi/Bornet protocols
(arXiv:2012.12281 Nature 595 227; arXiv:2402.15376 Science 2024) and the
Aquila device constraints (arXiv:2306.11727 whitepaper; AWS Braket docs).

### 2.1 Geometry — native lattice, 1D ring (NOT a reduced replica)

- **Topology: 1D ring of N = 24 atoms** (Bornet's verified critical-correlator
  geometry; also run N = 40 as the finite-size check, exactly their two sizes).
  Ring (periodic BC) is mandatory: it eliminates the strong symmetry-breaking
  boundary field that contaminates a finite chain's correlator and lets you use
  the chord distance d_j = (N/pi) sin(pi j / N) so every pair at fixed graph
  separation is equivalent (averaging gain ~ N).
- **Lattice constant a = 6.7 um**, blockade ratio Rb/a ~ 1.15-1.4. At Aquila's
  C6 = 2*pi*5.42e6 um^6 MHz and Omega ~ 2*pi*2.5 MHz this puts Rb ~ 7.7-9 um,
  the demonstrated critical regime. Ring radius for N=24: R = a/(2 sin(pi/24)) =
  6.7/(2*0.1305) = 25.7 um — comfortably inside Aquila's 75 um x 76 um field and
  well above the 4 um min atom separation. No atom pair is inside another's
  blockade radius (nearest-neighbor 6.7 um > 4 um hard limit; blockade is a
  soft interaction, not a placement constraint). This is the explicit
  non-pathological-geometry check the local validators failed.
- Aquila is a 2D device; a ring is a valid 2D coordinate set, fully supported.

### 2.2 Pulse schedule — adiabatic Delta sweep to the Ising critical point

Constant Rabi, swept detuning (the Ebadi protocol):

- **Omega(t):** ramp 0 -> Omega_max over 0.25 us (respect Aquila 2.5e6 rad/s/us
  slew), hold Omega_max = 2*pi*2.5 MHz, ramp down 0.25 us at the end.
  (Omega_max = 2*pi*2.5 MHz is the corrected value per MEMORY R6; the runnable
  script's 1 MHz was too small.)
- **Delta(t):** linear sweep from Delta_i = -2*pi*16 MHz (deep disordered /
  paramagnetic, all |g>) to Delta_f near the critical point Delta_c. For the
  1D Z2 (Rb/a~1.15) transition Delta_c/Omega ~ 1.2, i.e. Delta_c ~ 2*pi*3 MHz.
  Stop the sweep AT Delta_c (do not cross into the ordered phase) and hold.
- **Sweep rate:** Ebadi used s = 15 MHz/us as the slowest (most adiabatic) rate.
  Sweeping Delta = -16 -> +3 MHz at 15 MHz/us = **1.27 us sweep**. Add 0.5 us
  Omega ramps -> **T_total ~ 1.8 us**, with a ~0.2 us hold at Delta_c before
  readout. Total ~2.0 us.
- **Readout:** projective measurement of every atom in the {|g>, |r>} basis ->
  one bitstring z in {0,1}^24 per shot. NO time evolution after state prep —
  measure immediately at the end of the hold. This is the R1-dissolving step.

### 2.3 Shots and tasks

- Aquila hard limits: **1 to 1000 shots per task**, $0.30 per task, $0.01 per
  shot (AWS Braket pricing, fetched 2026-05-16).
- One Aquila "task" = one fixed Hamiltonian schedule run for K shots. The ENTIRE
  correlator C(r) for all r is extracted from the SAME bitstring ensemble of a
  single schedule (no per-separation tasks — that was an error in the candidate
  doc's "8 separation settings"). So shots are NOT multiplied by separations.
- Plan: the schedule run at max 1000 shots/task, replicated across M tasks to
  reach the target shot budget N_shots = 1000*M (section 4 fixes M).

## 3. The estimator and why it beats R2

### 3.1 Definitions

Per shot s, atom i returns a bit b_i^(s) in {0,1} (1 = Rydberg |r>). Define the
staggered order-parameter variable sigma_i^(s) = (-1)^i (b_i^(s) - nbar_i), with
nbar_i = mean_s b_i^(s) the per-site mean occupation (the (-1)^i absorbs the
antiferromagnetic ordering wavevector of the blockaded ground state).

**sigma channel estimator (path 1a):**

```
C_sigma(r) = ( 1 / (N * S) ) * sum_{s} sum_{i}  sigma_i^(s) * sigma_{i+r}^(s)
           = < sigma_i sigma_{i+r} >          (connected by construction —
                                                sigma is already mean-subtracted)
```
fit log|C_sigma(r)| vs log d_r over r = 2..8 (drop r=1, blockade-contaminated)
-> slope = -2*Delta_sigma. Ising prediction: 2*Delta_sigma = 0.25.

**Energy/T channel estimator (path 1b):** local energy density
h_i^(s) = b_i^(s) * b_{i+1}^(s) (the Rydberg nn interaction term). Then

```
C_E(r) = mean_s( h_i^(s) h_{i+r}^(s) ) - mean_s(h_i^(s)) * mean_s(h_{i+r}^(s)),
         averaged over i (ring translation)
```
fit C_E(r) = A*d_r^-2 + B*d_r^-4; the B term is the stress-tensor channel,
its exponent is the project's alpha=4. (See section 4 for why B is hard.)

### 3.2 Why this captures the connected piece R2 destroyed

R2's killer (MEMORY): `rydberg_density_to_energy` built the energy proxy as a
**product (or sum) of single-site densities**, i.e. it used <n_i>*<n_j>-type
terms — the FACTORIZED (disconnected) expectation. Algebraically, the true
two-body object decomposes as

```
< n_i n_j >  =  < n_i ><n_j >        (disconnected — what R2's estimator kept)
              + < n_i n_j >_c         (connected — what R2's estimator DROPPED)
```

R2's estimator evaluated correlators on a product ansatz, so the
`<n_i n_j>_c` term was identically zero by construction — no shot count could
recover it because it was removed analytically, not statistically.

The C1 estimators here form the product `b_i^(s) b_j^(s)` **inside the shot
average BEFORE factorizing**, then subtract the product of the separately
averaged means:

```
mean_s(b_i b_j)  -  mean_s(b_i) mean_s(b_j)   --->   <n_i n_j>_c   exactly
```

This is the textbook unbiased connected-correlator estimator (it converges to
the exact cumulant as S -> infinity, with O(1/sqrt(S)) sampling error). The
connected piece is retained, not annihilated. That is the precise sense in
which C1 "does HYP-017 right": R2 was a *modeling* error (wrong ansatz), and
C1 replaces it with the direct empirical cumulant from raw bitstrings.

This works because Aquila's readout is a projective measurement in the
occupation (Z) basis, and n_i (hence sigma_i, h_i) is **diagonal** in that
basis — so the bitstring ensemble samples the exact joint distribution of these
observables with no basis-rotation bias (this is also why R3/R4 cannot occur:
those biases came from estimating an off-diagonal Renyi-2 in a single basis;
here every observable is diagonal).

## 4. Quantitative: shots, noise, cost, adiabaticity

### 4.1 Adiabaticity vs coherence — PASSES with margin

- Sweep + ramps T_total ~ 2.0 us (section 2.2).
- Rydberg-state lifetime ~ 80 us (Ebadi). Off-resonant scattering: 1/(20 us)
  for |g>, 1/(150 us) for |r>. Over 2.0 us the dominant decoherence is the |g>
  scattering: ~2.0/20 = 0.10 -> ~10% integrated scattering probability per atom.
- This is the SAME 1.27-2 us regime where Ebadi resolved the (2+1)D Ising
  transition and Bornet resolved 1D power-law correlations, so adiabaticity to
  the critical point within coherence is **demonstrated hardware**, not a hope.
- Kibble-Zurek caveat: a strictly adiabatic prep of a *gapless* critical point
  is impossible (gap -> 0); the sweep injects a residual KZ correlation-length
  cutoff xi_KZ ~ s^(-nu/(1+z*nu)). At s = 15 MHz/us Bornet still extracted the
  correct scaling dimension, so xi_KZ is long enough. NOT the hard obstacle.

### 4.2 The hard obstacle (with numbers): decoherence cutoff length xi_d

This is the killer-grade issue, and it is empirical, from the exact prior
experiment (Bornet/Lukin arXiv:2402.15376):

> the measured correlator is NOT a pure power law. It is
> `<sigma_0 sigma_r>_c  ~  d_r^(-2 Delta_sigma) * exp(-d_r / xi_d)`
> with a decoherence-induced cutoff **xi_d ~ 13 lattice sites**.

Consequences with numbers:

- The clean power-law window is roughly d_r <~ xi_d/2 ~ 6 sites. On an N=24
  ring the max chord distance is N/pi ~ 7.6 sites — so you get ~5-6 usable
  points BEFORE the exponential envelope dominates. Exactly Bornet's situation;
  they still extracted 2*Delta_sigma = 0.128(37) for the (their normalization;
  consistent with Ising 1/8 = 0.125) — a **+/-0.037 absolute** uncertainty on
  the exponent, at >10,000-shot-class statistics, AFTER jointly fitting the
  exp(-d/xi_d) envelope.
- **For path 1a (sigma exponent 2*Delta = 0.25):** Bornet's +/-0.037 is already
  < the +/-0.3 target. So resolving the *sigma* exponent to +/-0.3 is easy and
  is essentially a reproduction of Bornet on Aquila. Shot requirement: their
  regime is ~10^4 shots. Aquila max 1000/task -> **M = 10 tasks, 10,000 shots**
  gives Bornet-class statistics on the sigma channel.
- **For path 1b (the project's alpha=4 stress-tensor term B*d^-4):** this is
  where it breaks. B*d^-4 is the SUBLEADING term under A*d^-2 (epsilon) which is
  itself under the sigma channel. Signal ratio at d=4: d^-4/d^-2 = d^-2 = 1/16;
  and the whole C_E is suppressed by the exp(-d/xi_d) envelope (e^(-4/13) =
  0.73) and by per-shot Bernoulli variance of the 4-point object h_i h_j
  (Var ~ <h><h> ~ (0.25)^2 with <h>~0.25 -> per-shot SNR ~ 0.06 at d=4 for
  the connected piece ~ few x 1e-3). To resolve a d^-4 coefficient to the
  alpha = 4 +/- 0.3 SIM-2026-023 window you need the relative error on the
  fitted B-exponent < ~7%. Propagating Bernoulli shot noise through the
  two-term fit `A d^-2 + B d^-4` over 5 points with envelope contamination:
  required shots scale as ~ (signal/noise)^-2 ~ **>~ 10^6 - 10^7 shots**.
  At Aquila 1000 shots/task that is **1,000 - 10,000 tasks** = $300 - $3,000
  in task fees ALONE plus $10,000 - $100,000 in shot fees. **Path 1b is not
  affordable and not resolvable within the decoherence cutoff** — the r^-4
  term lives at d where the exp(-d/xi_d) envelope has already eaten the signal.
  This is the structural obstacle and it is the same family of problem as the
  HYP-017 killers, just relocated from "decay in time" to "decay in space."

### 4.3 Cost summary (corrected — candidate doc numbers were wrong)

Candidate doc claimed "$0.0009/shot, 5000 shots/setting x 8 settings, $200-500."
**All three figures are wrong:**

| Item | Candidate doc | Actual (AWS, 2026-05-16) |
|------|---------------|--------------------------|
| Per-shot | $0.0009 | **$0.01** (11x higher) |
| Per-task | (omitted) | **$0.30** |
| Max shots/task | 5000 implied | **1000 (hard cap)** |
| Settings | "8 separation settings" | **1** (all r from one ensemble) |

- **Path 1a (sigma consistency test, 10,000 shots, 10 tasks):**
  10 * $0.30 + 10,000 * $0.01 = $3 + $100 = **$103.** Add N=40 finite-size
  replicate: ~**$206 total.** This is real, affordable, and the right number
  to quote.
- **Path 1b (direct alpha=4 stress-tensor term):** $10k - $100k+. Reject.

So the affordable, defensible run is **path 1a only, ~$103-206**, and it
measures the **sigma scaling dimension (alpha_sigma = 0.25)**, NOT the
published alpha=4 directly. The alpha=4 stress-tensor channel is *inferred* by
CFT consistency once 2*Delta_sigma=0.25 is confirmed, not independently
hardware-measured.

## 5. Prior art (web-grounded, arXiv MCP bypassed)

arXiv MCP returns a stale fixed feed; all citations below from WebSearch/WebFetch
2026-05-16.

1. **Ebadi et al., "Quantum phases of matter on a 256-atom programmable quantum
   simulator", Nature 595, 227 (2021), arXiv:2012.12281**
   (https://arxiv.org/abs/2012.12281). 256 atoms (16x16), a = 6.7 um, Omega =
   2*pi*4.3 MHz, Delta swept -16 -> +14 MHz at s = 15-120 MHz/us, Rydberg
   lifetime ~80 us, 67-repetition-class statistics. Demonstrated the (2+1)D
   Ising QPT and high-fidelity AFM order. **DONE:** adiabatic Delta-sweep prep
   of Ising-critical Rydberg states is established hardware. C1's prep is a
   direct re-use, not new.

2. **Bornet, Lukin et al., "Probing critical phenomena in open quantum systems
   using atom arrays", Science (2024), arXiv:2402.15376**
   (https://arxiv.org/abs/2402.15376). 24-atom (and 40-atom) 1D **ring**, Cs
   54S, Rb/a ~ 1.4, adiabatic prep to the Ising critical point, observable
   `<sigma_0 sigma_j>_c` from bitstrings with sigma_i = (-1)^i (n_i - <n>),
   fit to d_j^(-2Delta_sigma) * exp(-d_j/xi_d), extracted the Ising scaling
   dimension consistent with 1/8, and crucially **identified the decoherence
   cutoff xi_d ~ 13 sites** as the fundamental obstacle. **This is essentially
   C1 already performed** (different machine — Harvard Cs array, not Aquila).
   C1's estimator, geometry (24-ring + 40-ring), and physics target are the
   same. The novelty of C1 as a *measurement* is therefore near-zero.

3. **de Leseleuc / Kibble-Zurek on Rydberg: arXiv:1809.05540** (Keesling et al.,
   Nature 568, 207). Quantum KZ across the 1D Rydberg Ising transition.
   Establishes the KZ correlation-length scaling and that the sweep is the
   correct critical-prep tool. Supports adiabaticity argument (sec 4.1).

4. **Wurtz et al. "Aquila: QuEra's 256-qubit neutral-atom quantum computer",
   arXiv:2306.11727** — Aquila whitepaper; confirms the device runs exactly the
   Ebadi-class Delta-sweep AHS protocol on AWS Braket. Aquila device limits
   (1-1000 shots/task, $0.30/task, $0.01/shot) from AWS Braket pricing page.

5. **Sahay, Lukin, Cotler, arXiv:2401.13595 (PRX 15, 021078)** — the
   "hologrons" paper this project is built on; endorses Rydberg PXP arrays for
   the Ising CFT, but its predicted gravitational object is the *bulk*
   exponential cosh(rho/l_AdS), not the boundary correlator. Confirms the
   sec-1 caveat that the project's alpha=4 is a T-channel object, distinct from
   the directly-measurable sigma 2-point function.

### What is DONE vs NOVEL

| Element | Status |
|---------|--------|
| Adiabatic Delta-sweep prep of Ising-critical Rydberg ground state | DONE (Ebadi 2021) |
| Bitstring connected `<sigma_0 sigma_j>_c` on a 24/40-ring | DONE (Bornet 2024) |
| Extracting the Ising sigma scaling dimension from the power law | DONE (Bornet 2024, +/-0.037) |
| Identifying xi_d ~ 13 as the obstacle | DONE (Bornet 2024) |
| Running it specifically on **public QuEra Aquila** (Bornet used Harvard Cs) | NOVEL (minor — platform port) |
| Interpretive bridge: tying the measured sigma exponent to THIS project's published alpha=4 stress-tensor / Zenodo record | NOVEL (the only real novelty) |
| Direct hardware measurement of the **alpha=4 stress-tensor** exponent | NOT DONE and (sec 4.2) NOT FEASIBLE on Aquila |

## 6. Verdict

**VERDICT: NEEDS-MODIFICATION** (do not run as proposed; one cheap reframed
variant is defensible).

The candidate's structural claim is correct: C1 genuinely dissolves all four
HYP-017 killers (R1 inapplicable — static state, no propagation; R2 fixed — the
explicit bitstring cumulant retains the connected piece R2's product ansatz
annihilated; R3/R4 inapplicable — diagonal observable, no Renyi-2; no
blockade-pathological geometry — full native 24/40-ring at a=6.7 um). The
methodology is sound and the state-prep IS adiabatic within Aquila coherence
(~2.0 us sweep vs ~80 us lifetime; demonstrated by Ebadi/Bornet). On those
axes the candidate holds up.

It fails on three quantitative grounds that the candidate doc did not surface:

1. **Wrong target observable.** Aquila measures the Rydberg occupation = the
   Ising **sigma** order parameter, whose connected correlator decays as
   **r^-1/4 (alpha=0.25)**, not the project's **r^-4 (alpha=4)** stress-tensor
   channel. The alpha=4 object is sub-sub-leading (~800x smaller at r=6) and is
   NOT directly readable. C1 measures alpha_sigma=0.25 and can only *infer*
   alpha=4 by CFT consistency — it is a consistency test of the published
   claim, not an independent hardware measurement of alpha=4. SIM-2026-023's
   acceptance window [3.2, 4.8] is for the alpha=4 channel and is therefore
   the WRONG yardstick for what C1 actually measures; the correct target is
   2*Delta_sigma = 0.25 (Ising), where Bornet already achieves +/-0.037.

2. **The direct alpha=4 variant (path 1b) is not affordable or resolvable.**
   Isolating the B*r^-4 stress-tensor term under the r^-2 epsilon term and the
   exp(-r/xi_d) decoherence envelope needs ~10^6-10^7 shots = 1,000-10,000
   Aquila tasks = **$10k-$100k+**, and the r^-4 signal lives at separations
   the xi_d~13 cutoff has already suppressed. This is a spatial re-incarnation
   of the HYP-017 noise-vs-signal killer. Reject path 1b outright.

3. **Near-zero measurement novelty.** Bornet/Lukin (Science 2024,
   arXiv:2402.15376) already performed essentially this exact experiment
   (24+40-ring, identical estimator, Ising scaling dimension, xi_d~13
   obstacle) on the Harvard Cs array. The only novelty is porting it to public
   Aquila and the interpretive bridge to this project's Zenodo record.

**Affordable defensible variant (recommended if pursued at all):** run ONLY
path 1a — N=24 ring + N=40 ring, Ebadi Delta-sweep, ~10,000 shots each (10
tasks/size), measure 2*Delta_sigma and confirm = 0.25 +/- ~0.04, fit the
exp(-d/xi_d) envelope. **Cost: ~$103 (single ring) to ~$206 (both rings).**
Headline shot/cost number: **~20,000 shots / ~$206.** This yields a
*hardware consistency check* that the project's CFT boundary is genuinely the
c=1/2 Ising CFT (from which alpha=4 follows analytically), attachable to the
Zenodo record — modest, honest, cheap. It does NOT, and cannot on Aquila,
directly measure alpha~=4.

**Bottom line vs the project's other options:** path 1a is ~$206 for a
consistency check that re-derives a 2024 Science result on a different machine;
it is positive-EV only as a low-cost external validation footnote for SciPost
review, not as the "first experimental confirmation of alpha~=4" the candidate
doc claimed. If the goal is specifically to confirm alpha~=4, C1 cannot deliver
it and the published three-numerics-converge-on-4.0 argument (MEMORY option B)
remains the stronger position.

### Recommendation
- C1 as written (claiming a hardware alpha~=4 measurement): **REFUTED for that
  claim.**
- C1 reframed as a $206 sigma-exponent Ising-CFT consistency check:
  **NEEDS-MODIFICATION -> conditionally VALIDATED at ~$206**, low priority,
  novelty is the platform port + Zenodo attachment only.
