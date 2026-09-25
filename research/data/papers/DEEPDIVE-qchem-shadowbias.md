# Deep-Dive — NQS-Biased Classical Shadows on a Shallow VQE State (QCHEM-COMBO #1)

**Date:** 2026-05-17
**Candidate:** FermiNet/Psiformer-class near-FCI NQS used purely as the locally-biased
classical-shadow (LBCS) bias oracle for property readout off a shallow VQE state. NQS supplies
per-Pauli measurement weighting; quantum state untouched. Claim: 10–100× shot reduction for
chemical-accuracy 2-RDM / property extraction.

**Verdict:** _(pending — see §4)_

---

## 1. Mechanism — Locally-Biased Classical Shadows and where the NQS enters

### 1.1 The shadow estimator and its variance

Randomized single-qubit (Pauli) classical shadows (Huang–Kueng–Preskill, arXiv:2002.08953):
each shot picks a random local basis bᵢ ∈ {X,Y,Z} on every qubit (uniform, β = 1/3), measures,
and builds the inverse-channel snapshot ρ̂ = ⊗ᵢ(3|sᵢ⟩⟨sᵢ| − I). For an observable
O = Σ_P α_P P (Pauli decomposition, e.g. a Jordan–Wigner mapped 2-RDM element), the single-shot
variance is dominated, for each k-local Pauli term P with support supp(P), by the inverse of the
probability that the random basis "hits" that term:

```
Var[⟨P⟩]  ∝  ⟨P⟩² · ( Π_{i∈supp(P)} β_i(P_i) )⁻¹  −  ⟨P⟩²
```

For uniform Pauli shadows, Π β = 3^(−|P|): variance blows up as 3^|P| in the **Pauli weight**.
Chemistry 2-RDM elements after JW are dominated by weight-2…4 strings with long Z-tails — exactly
the high-weight regime where naive shadows are worst.

### 1.2 Locally-biased shadows (Hadfield et al., arXiv:2006.15788, CMP 2022)

LBCS replaces the uniform β = 1/3 with a **per-qubit biased distribution** β_i(X), β_i(Y),
β_i(Z) ≥ 0, Σ = 1, chosen to minimize the total estimator variance for the *target Hamiltonian /
observable set*. The exact single-shot variance is their Eq. (11):

```
Var(ν) = Σ_{Q,R} f(Q,R,β) α_Q α_R tr(ρ Q R)  −  (tr ρ O)²
```

This depends on the true state ρ through tr(ρ Q R). Since ρ is unknown, LBCS substitutes a
**classical reference state ρ_ref** for the ρ-dependent factors and minimizes the resulting
surrogate cost. For a single-reference product (Hartree–Fock) reference the diagonal cost

```
cost_diag(β) = Σ_Q α_Q²  Π_{i∈supp(Q)} β_i(Q_i)⁻¹
```

is **convex** (sum of reciprocals of linear functions; −log convex), so the bias is found by a
cheap classical convex solve. The off-diagonal/general cost is non-convex but the diagonal
restriction is the one used in practice.

**Where the NQS enters:** the entire role of ρ_ref is to supply the term-correlation weights
α_Q α_R tr(ρ_ref Q R) (and, in the diagonal approximation, the relative weights of the α_Q²).
The published LBCS paper used ρ_ref = **Hartree–Fock only** (their Table 1 — confirmed by direct
fetch of the ar5iv source). The candidate's proposal is to set ρ_ref = a near-FCI NQS, so the
bias is optimized against the *true correlation structure* instead of a mean-field one. The
quantum device still only runs random single-qubit Cliffords; nothing about the circuit changes.

### 1.3 Is the variance-reduction argument sound, and how large?

Yes, the direction of the argument is sound and is a textbook property of importance-sampling /
biased estimators: a reference state closer to ρ in the relevant 2-norm makes the surrogate cost
a tighter proxy for the true variance, so the convex minimizer of the surrogate is closer to the
true variance-optimal β. The estimator stays **unbiased for any β > 0** (the inverse-channel
reweighting corrects exactly); a wrong ρ_ref only makes the variance sub-optimal, never biases
the answer. This is the crucial safety property — a *bad* NQS prior cannot corrupt the 2-RDM, it
only fails to accelerate it.

**Magnitude — anchored to published numbers, not asserted.** Hadfield Table 1 (HF reference vs
naive Pauli shadows):

| Molecule | qubits | naive-shadow Var | LBCS(HF) Var | factor |
|---|---|---|---|---|
| LiH | 12 | 266 | 14.8 | ~18× |
| H₂O | 14 | 2 840 | 257 | ~11× |
| NH₃ | 16 | 14 400 | 353 | ~41× |

So **HF-prior LBCS already delivers ~11–41×** for exactly the molecule class the candidate
targets. The candidate claims a *further* gain from HF → near-FCI prior. The realistic size of
that incremental gain is bounded and modest, not another 10–100×:

- The variance surrogate depends on ρ_ref through tr(ρ_ref Q R). HF already gets the dominant
  (large-|α|) diagonal Z-strings right because those are determined by occupation numbers, which
  HF has exactly for closed-shell equilibrium geometries. The near-FCI prior mainly corrects the
  *off-diagonal / strong-correlation* term weights.
- Honest estimate: for **weakly correlated, near-equilibrium** systems (H₂O equilibrium, LiH) the
  HF prior is already near-optimal; NQS prior buys maybe **1.2–2×** on top — not worth the
  machinery. For **strongly correlated / stretched** systems (N₂ dissociation, stretched H₂O,
  biradicals, transition-metal active spaces) HF mis-weights the multireference terms badly, the
  CISD prior is also poor (it under-weights the static-correlation block), and a near-FCI NQS
  prior plausibly recovers a further **~3–10×** over HF-LBCS in the regime where it matters.

That is the real, defensible claim: **not 10–100× absolute (that's mostly the already-published
HF-LBCS gain) — the novel increment is ~3–10× over HF-LBCS, localized to the strong-correlation
regime where HF/CISD priors are structurally wrong.** The candidate's headline number conflates
the established LBCS gain with the new prior's marginal gain.

## 2. The catch — circular or not?

This is the decisive question and it must not be hand-waved (cf. the project's standing lesson:
"a power-law exponent match is not evidence of a mechanism" / mechanism-faithful vs coincidental).

### 2.1 The circularity charge, stated at full strength

If you already possess a **near-FCI NQS** for the molecule, you have — by construction — a
classical wavefunction that reproduces the ground state to chemical accuracy. From that NQS you
can directly compute the energy, the 2-RDM, the dipole, forces, *everything the quantum readout
was supposed to deliver*, with **zero quantum shots**. In that case the quantum device contributes
nothing: the chemistry was already solved classically, and the "shadow readout off a shallow VQE
state" is a decoration on a problem the prior already answered. **At face value the candidate is
circular.** This is the same failure pattern as the Tier-X "LC-ladder MERA emulator" (measuring an
exponent you designed in): if the prior already contains the answer, reading it back off the
quantum state is negative information.

### 2.2 The escape: a precise non-circular regime exists

The charge is defeated **only if** there is a regime where the NQS is simultaneously
(a) a *good measurement prior* — i.e. its term-correlation structure tr(ρ_NQS Q R) is close
enough to the truth to bias β well — **but** (b) *not a trustworthy answer* — i.e. its own
expectation values for the target observable are not chemically reliable, while the VQE state's
shadow estimate (debiased, unbiased by construction) is. Both must hold at once. They can:

**Regime 1 — variational energy is tight but the NQS is observable-biased (the strong case).**
NQS/VMC optimizes the *energy* (Rayleigh quotient). The variational principle gives a second-order
bound on energy error but only a *first-order* bound on the error of a general observable ⟨A⟩ that
does not commute with H. Empirically (and confirmed in the excited-state NQS literature,
arXiv:2308.16848), forces, dipoles, density-derived quantities and off-diagonal RDM elements from
VMC carry **first-order** wavefunction error even when the energy is at chemical accuracy. The
gap-to-truth on a dipole or a 2-RDM cumulant can be 5–50 mHa-equivalent while the energy is
< 1 mHa. In that regime: the NQS's *term-weighting* (which is an energy-dominated, occupation-
dominated quantity) is excellent → good bias; but the NQS's *direct* dipole/force/2-RDM value is
biased and you should not trust it → you genuinely want the unbiased shadow estimate off the
physical state. **This is non-circular and physically real.** The NQS answers "where is the
measurement variance" well precisely because that is an energy-like quantity; it answers "what is
the dipole" poorly because that is a first-order-error quantity.

**Regime 2 — the NQS is for a *nearby surrogate*, the VQE state is the *target*.** Train the NQS
on a cheaper/related system (equilibrium geometry, smaller basis, frozen-core, or a
single-reference proxy) and use it as the bias prior for shadow readout of the VQE state at the
*expensive* point (stretched geometry, larger basis, the actual strongly-correlated point). The
prior need only be correlation-structurally similar (good bias), not numerically exact for the
target (so it is not the answer). Variance optimality degrades gracefully with prior mismatch;
correctness does not degrade at all (estimator stays unbiased). This converts the NQS from
"solved the problem" to "informed guess about where to spend shots on a problem it did not solve."

**Regime 3 — verification / non-self-certifying prior.** Even a near-FCI NQS at the target point
is not *self-certifying*: VMC has no internal error bar that proves chemical accuracy
(the variational energy is an upper bound of unknown tightness; the zero-variance principle is
only asymptotic). The debiased shadow estimate off an independently-prepared VQE state is an
**independent, unbiased** estimator of the same 2-RDM. Agreement within shadow error bars
*certifies* the NQS; disagreement flags NQS bias. Here the quantum readout buys a trust
guarantee the classical prior cannot give itself — modest but real value, and explicitly
non-circular.

### 2.3 Where it stays circular (must be excluded)

For **weakly correlated, near-equilibrium** small molecules in a minimal/DZ basis (the easy
demo cases — H₂O equilibrium, LiH, BeH₂): a near-FCI NQS *is* the answer to ~sub-mHa on all
observables, the energy variational error and the observable error are both tiny, and Regime 1
collapses. There the candidate **is circular** and adds nothing over just printing the NQS RDM.
Any demonstration on these systems would be a vacuous self-confirmation — the same trap the
project flagged for HYP-014 / the LC-ladder. The candidate is **only** defensible if the
benchmark is deliberately chosen in Regime 1/2: **stretched N₂, stretched/bent H₂O beyond the
Coulson–Fischer point, π-space biradicals, or a transition-metal minimal active space**, and the
*reported* deliverable is a property where VMC carries first-order error (dipole, force,
off-diagonal 2-RDM / cumulant), **not** the energy.

## 3. Prior art

(arXiv MCP recency feed is stale per project standing note — all checks via WebSearch, URLs/IDs
inline.)

**Published — the components:**

- **Hadfield, Bravyi, Raymond, Mezzacapo, *Measurements of Quantum Hamiltonians with
  Locally-Biased Classical Shadows*, CMP 391 (2022); arXiv:2006.15788.** Defines LBCS, the
  variance Eq. (11), the convex diagonal cost, benchmarks on molecular Hamiltonians up to 16q.
  **Reference state used: Hartree–Fock (single-reference product).** The paper *explicitly* notes
  multi-reference / perturbation-theory references as a possible extension but does **not** use a
  high-accuracy correlated wavefunction and does **not** use any neural network.
  → URL: https://arxiv.org/abs/2006.15788
- **Huang, Kueng, Preskill, *Predicting Many Properties…*, Nat. Phys. 16 (2020);
  arXiv:2002.08953**, and **Huang–Kueng–Preskill, *Efficient estimation of Pauli observables by
  derandomization*, arXiv:2103.07510.** Randomized + derandomized shadows; derandomization is
  observable-aware but **state-agnostic** (no classical wavefunction prior).
  → https://arxiv.org/abs/2002.08953 , https://arxiv.org/abs/2103.07510
- **Biased estimator channels for classical shadows, Phys. Rev. A 111, L030402 (2025);
  arXiv:2402.09511.** Rescales the estimator to trade bias for finite-sample error — a different
  axis (intentional bias), still no wavefunction prior.
- **Neural-Shadow QST (arXiv:2305.01078, PRR 6 023250 2024)** and **Bootstrapping Classical
  Shadows for NQS Tomography (arXiv:2405.06864).** Here the NQS is the *object being learned from
  shadow data* — shadows → NQS. This is the **opposite coupling direction**: the quantum state is
  re-tomographed into an NQS; the NQS is the *output*, not a fixed measurement prior.
- **Neural Error Mitigation (arXiv:2105.08086).** NQS re-tomographs/denoises a VQE state — again
  shadows/measurements → NQS as output, not NQS → measurement bias.
- **Artificial-Intelligence-Driven Shot Reduction in Quantum Measurement (arXiv:2405.02493,
  Chem. Phys. Rev. 2024).** *Checked directly* — this is **RL shot-budget scheduling across VQE
  iterations**, NOT a classical wavefunction supplying per-Pauli bias. Despite the similar title
  it is **not** the candidate's coupling. Not prior art for this idea.
- **Scalable / Retentive / selected-configuration second-quantized NQS for chemistry**
  (IOP Mach. Learn. Sci. Technol. 4 (2023) 045001 — arXiv:2306.16705; Retentive-NQS
  arXiv:2411.03900; NQS-from-selected-configs arXiv:2602.12993). Establishes **orbital-basis,
  occupation-number autoregressive NQS that compute Pauli/2-RDM expectations directly and scale
  to ~76 qubits.** Important: this **dissolves the "hardest obstacle"** the menu listed
  (first-quantization continuum FermiNet → second-quantized Pauli basis). Use a *second-quantized*
  NQS, not FermiNet/Psiformer, and the basis-mismatch cost objection largely vanishes.

**The located novelty (precise):** No located work uses a **high-accuracy correlated /
near-FCI neural quantum state as the LBCS reference (bias) distribution while leaving the
physical quantum state untouched**. Every shadow×NQS paper found runs the coupling
**shadows → NQS** (NQS as estimator/output). The candidate runs it **NQS → shadow bias** (NQS as
a fixed, classically-queried importance prior; quantum state only ever runs random Cliffords).
LBCS itself only ever used an HF reference and flagged "better reference" as open. So the novel
slice is real but **narrow**: it is "replace the HF reference in arXiv:2006.15788 with a
near-FCI second-quantized NQS reference," plus the non-circular regime argument of §2.2. It is an
**incremental, well-posed extension of one specific published method**, not a new primitive.

## 4. Verdict

### **VERDICT: NEEDS-MODIFICATION** (not refuted as circular — a precise non-circular regime
exists; but the headline claim and demo molecules as stated *are* circular and must change).

**Circular-or-not judgment:** **Conditionally non-circular.** The candidate is **circular and
worthless as written** for weakly-correlated near-equilibrium small molecules (H₂O-eq, LiH,
BeH₂, minimal/DZ) — there a near-FCI NQS *is* the answer and the quantum readout is vacuous
self-confirmation (same trap as HYP-014 / the LC-ladder Tier-X kill). It becomes **genuinely
non-circular only in Regime 1/2/3 of §2.2**: the NQS is an energy-optimized prior, so it weights
measurement variance well (energy-like, occupation-dominated) while carrying *first-order* error
on the actually-reported observable (dipole / force / off-diagonal 2-RDM / cumulant) at
strongly-correlated geometries (stretched N₂, post-Coulson–Fischer H₂O, π-biradicals, TM minimal
active space). In that exact regime the prior is a good *measurement* prior but not a trustworthy
*answer*, and the unbiased shadow estimate off the physical state delivers something the prior
cannot self-certify.

**Required modifications (all four are mandatory):**
1. **Drop the headline "10–100× shot reduction."** That factor is overwhelmingly the
   *already-published* HF-LBCS gain (arXiv:2006.15788 Table 1: H₂O 11×, NH₃ 41×). The honest
   novel increment is **~3–10× over HF-LBCS, only in the strong-correlation regime**; ≈1.2–2×
   (not worth it) near equilibrium.
2. **Benchmark must be strong-correlation + a first-order-error observable** (stretched N₂
   dipole/force, bent-stretched H₂O 2-RDM cumulant). Energy is *not* an acceptable target
   observable here — VMC energy is second-order-accurate, so the energy demo would be circular.
3. **Use a second-quantized orbital-basis NQS** (autoregressive; arXiv:2306.16705-class), **not**
   FermiNet/Psiformer. This dissolves the menu's stated "hardest obstacle" (continuum→Pauli
   projection) — it was a non-problem given the wrong NQS choice.
4. **Frame the deliverable as independent cross-validation / shot-optimal readout**, not as
   "solving the chemistry." The value is: unbiased, self-certifying property extraction at
   strong correlation where the classical prior is structurally untrustworthy, at shot cost
   3–10× below HF-LBCS and 30–400× below naive shadows.

**Scoring impact (vs menu's N4·B4·U4·Mech5 = 64):** NOVELTY **4 → 3** (located novelty is a
narrow, well-posed extension of one published method, not a new primitive; coupling-direction
genuinely unpublished). BUILDABILITY **4** (second-quantized NQS + LBCS both run on a laptop;
quantum side is depth-≤20 random Cliffords on free cloud — holds). USEFULNESS **4 → 3** (real but
modest: ~3–10× over an *already-good* baseline, in a niche regime). MECHANISM **5 → 3** (the
coupling is principled *only* under the §2.3 exclusion; as written it fails the project's own
"coincidental vs faithful" axis because the obvious demo is circular). **Revised product ≈
3·4·3 = 36**, down from 64 — survives but drops well below the Tier-0 survivors (S1 = 48).

**Bottom line:** Not refuted, not validated as claimed. A real but narrow, incremental result
hides behind an inflated headline; it is salvageable *only* with the strong-correlation +
first-order-observable framing and the honest ~3–10× increment. Do not demo it on equilibrium
H₂O/LiH — that would be a circular self-confirmation.

---
*Prior-art caveat: arXiv MCP recency feed stale (project standing note); all checks via WebSearch
with inline URLs/IDs; arXiv:2006.15788 variance/table and arXiv:2405.02493 method verified by
direct page fetch.*
