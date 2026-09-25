# C_TTT via spin-resolved stress-tensor extraction — implementation design (P2 next step)

**STATUS:** DESIGN, ready to implement. Extends the VALIDATED v4 OPE pipeline
(`qw_ope_pev_z2.jl`, SIM-061: Ising C_σσε = 0.507 vs CFT 0.5 at χ=6–8, C_σσσ structural
zero, covariance clean). Target: C_TTT, the OPE self-coupling of the stress tensor T (the
"emergent graviton self-coupling"). Validate on Ising c=1/2, then tricritical Ising c=7/10.

**One-line conclusion (recommended route):** resolve T vs T̄ inside the Δ≈2 even subspace
using the **ascended lattice energy density h (spin-0 ⇒ T+T̄) and the ascended lattice
momentum/energy-current density p (spin-±1 in lattice units ⇒ T−T̄)** as the two physical
reference operators, then form T = ½(𝒪_h + 𝒪_p) after PEV Eq. 10 normalization. This uses
only operators MERAKit already produces (h ascends natively; p is a known local operator for
TFIM), avoids the ill-posed one-site eigenbasis mixing, and gives a clean falsifiable target.

---

## 1. The target number (careful CFT algebra)

### 1.1 Chiral stress tensor normalization on a line

Work in the chiral (holomorphic) sector. The 2D CFT stress tensor T(z) is a quasi-primary of
dimension (h, h̄) = (2, 0), scaling dimension Δ_T = 2, conformal spin s = h − h̄ = +2. Its
antiholomorphic partner T̄(z̄) has (0, 2), spin −2. The canonical normalizations are

  ⟨T(z) T(0)⟩ = (c/2) z⁻⁴,   ⟨T̄(z̄) T̄(0)⟩ = (c/2) z̄⁻⁴,   ⟨T(z) T̄(0)⟩ = 0.   (T1)

The three-point function of the holomorphic stress tensor with itself is fixed by conformal
Ward identities up to the central charge:

  ⟨T(z₁) T(z₂) T(z₃)⟩ = c · (z₁₂ z₂₃ z₃₁)⁻² ,   z_ij ≡ z_i − z_j.   (T2)

(Standard result, Di Francesco–Mathieu–Sénéchal Eq. 6.180 / Ward identity for ⟨TTT⟩; the
coefficient is exactly c with the (T1) normalization ⟨TT⟩ = (c/2)z⁻⁴.)

### 1.2 PEV's convention vs the CFT convention — the key rescaling

PEV (Eq. 10) normalizes every scaling operator to **UNIT two-point coefficient**:

  C_αβ ≡ ⟨φ_α(1) φ_β(0)⟩ = tr[(φ_α ⊗ φ_β) ρ̂]  →  normalized so C_αα = 1.   (PEV10)

So the PEV-normalized stress operator is 𝒯 = T / √(c/2), giving ⟨𝒯 𝒯⟩ = z⁻⁴ (unit
coefficient), and by (T2)

  ⟨𝒯 𝒯 𝒯⟩ = ⟨TTT⟩ / (c/2)^{3/2} = c / (c/2)^{3/2} = 2^{3/2} / c^{1/2} = **2√2 / √c**.   (T3)

Therefore the PEV-convention OPE structure constant is

  **C_TTT = 2√2 / √c = 2^{3/2} c^{-1/2}.**   (TARGET)

This is the number the pipeline must reproduce. Sanity: like C_σσε = ½, it is a pure number
independent of any lattice detail once operators are unit-normalized under Eq. 10.

| CFT | c | C_TTT = 2√2/√c |
|-----|------|----------------|
| Ising | 1/2 | 2√2 / √(1/2) = 2√2·√2 = **4.000** |
| Tricritical Ising | 7/10 | 2√2 / √0.7 = 2.8284 / 0.83666 = **3.3806** |
| 3-state Potts | 4/5 | 2√2 / √0.8 = 2.8284 / 0.89443 = **3.1623** |

So the sharp validation target is **C_TTT = 4.000 for Ising**, **3.381 for tricritical Ising**.
(The Potts row is listed for completeness / a possible fourth-class check; the flagship novel
number is 3.381 at c=7/10.)

### 1.3 Why the spin-2 phase does NOT change the number on a line

A worry: T has spin 2, so under a rotation/translation there are phase factors e^{isθ}. On the
LATTICE all three insertions sit on the real axis (z_i real, all at y=0), so every z_ij is real
and positive-ordered. The (z₁₂z₂₃z₃₁)⁻² factor in (T2) is then real and the correlator is a
real number — no residual phase. The spin only matters for (i) SEPARATING T from T̄ (Section 3)
and (ii) the KINEMATIC EXPONENTS in the width-3 registration (Section 1.4). The scalar
coefficient C_TTT in (TARGET) is phase-free because we evaluate on a line. This is the same
reason C_σσε is a clean real number in the current pipeline.

### 1.4 Kinematic factor for the (1,1,2) lattice registration

The pipeline's `ope_from_rho3` (ope_cone_v2.jl) evaluates the raw trace against ρ₃ at the
realized separations r₁₂=1, r₂₃=1, r₁₃=2 and multiplies by the kinematic factor

  kin = r₁₂^{e₁₂} r₂₃^{e₂₃} r₁₃^{e₁₃},   e_ij = Δ_i + Δ_j − Δ_k.

For three operators of EQUAL dimension Δ_T = 2 this is e₁₂ = e₂₃ = e₁₃ = 2, so

  kin = 1² · 1² · 2² = **4**,   raw_TTT ≈ C_TTT / 4 ≈ 1.0 (Ising).   (KIN)

Crucial subtlety for spin-2 operators: the general 3-pt function of operators with spin has
the form ∏ z_ij^{−(h_i+h_j−h_k)} z̄_ij^{−(h̄_i+h̄_j−h̄_k)}. For **all-holomorphic T** (h̄=0)
the antiholomorphic exponents vanish and only the holomorphic z_ij^{−(h_i+h_j−h_k)} survive,
with h_i = Δ_i = 2 (since h̄=0). So the scalar `ope_from_rho3` kinematic factor with Δ→h=2 is
EXACTLY correct **provided the operator fed in is the pure-holomorphic T**, not the mixture.
This is the whole reason spin resolution is mandatory: a T+T̄ mixture has a DIFFERENT kinematic
structure (mixed holomorphic/antiholomorphic exponents) and no single real `kin` reproduces it.
Feeding the ascended energy density h (= T+T̄) into the scalar 3-pt formula gives a WRONG number
even though its dimension is 2 — this is the trap the design must avoid, and the falsification
probe in Section 4 checks exactly this.

---

## 2. What lives at Δ≈2 in the even sector (the multiplet problem)

On the one-site (or width-2) scaling superoperator, the even (Z2-even for Ising) Δ≈2 subspace
is degenerate and mixes several quasi-primaries and descendants:

- **T** (holomorphic stress tensor): (h,h̄)=(2,0), Δ=2, spin +2. Present in EVERY unitary CFT
  (it is L_{−2}·𝟙, the level-2 descendant of the identity).
- **T̄** (antiholomorphic): (0,2), Δ=2, spin −2.
- **Λ = L_{−1}L̄_{−1} ε** (Ising) or the analogous ε-descendant: for Ising ε has (½,½), so
  L_{−1}L̄_{−1}ε has (3/2, 3/2), Δ=3 — NOT at Δ=2. Good: in Ising there is no ε-descendant at
  Δ=2, so the Δ=2 even subspace is spanned by {T, T̄} plus possibly the identity descendant
  L_{−2}L̄_{−2}𝟙 (Δ=4, also not at 2). **So for Ising the Δ=2 even subspace is exactly 2-dim:
  {T, T̄}.** This is why Ising is the clean validation case.
- **Tricritical Ising** c=7/10: primaries have (h,h̄) with h ∈ {0, 1/10, 3/5, 3/2, 7/16, 3/80}.
  The Δ=2 even sector again contains {T, T̄}. The nearest even scalar descendants: ε′ (the
  subleading energy, h=h̄=3/5, Δ=6/5) has descendants L_{−1}L̄_{−1}ε′ at Δ = 6/5+2 = 16/5 = 3.2
  (not 2); ε (h=h̄=1/10, Δ=1/5) descendant L_{−1}L̄_{−1}ε at Δ=1/5+2=11/5=2.2 — CLOSE to 2 but
  distinct, and it is a SCALAR (spin 0), so the spin-resolution filter separates it from T/T̄.
  This 2.2 contaminant is the main reason the Δ-window must be tight AND spin-filtered at c=7/10.

**Consequence:** dimension alone cannot pull T out. We need a spin-resolving criterion that
isolates the spin-+2 combination. Sections 3 ranks the routes.

---

## 3. Spin-resolution routes (ranked; recommended first)

### ROUTE A (RECOMMENDED) — physical reference operators: energy density h and momentum density p

**Idea.** We do not need to diagonalize spin abstractly. We already possess two PHYSICAL local
operators whose continuum limits are known combinations of T and T̄:

- The lattice **energy density** h (the Hamiltonian term, blocked to the SI layer by ascension).
  Its continuum limit is the trace-adjusted energy density, whose scaling piece is the spin-0
  combination
      h → a·(T + T̄) + (const)·𝟙 + irrelevant.        (A1)
  (T+T̄ is the Δ=2 spin-0 quasi-primary; the identity piece is the ground-state energy density
  subtracted below.)
- The lattice **momentum density / energy current** p. For the TFIM H = −Σ(X_r X_{r+1} + g Z_r)
  at criticality g=1, the energy current (momentum density) is the known local operator
      j_r ∝ (X_{r−1} Y_r − Y_r X_{r+1})  ·  (Z-field pieces)      (A2)
  more precisely the lattice momentum density is p_r = i[h_{r−1,r}, h_{r,r+1}] (the commutator
  of adjacent energy-density bonds), which is a strictly LOCAL 3-site operator and whose
  continuum limit is the spin-±1 combination
      p → b·(T − T̄) + irrelevant.        (A3)
  p is odd under spatial reflection (it is a current); T+T̄ is even. This parity-under-reflection
  is the exact discrete analog of conformal spin and is what separates them.

**Extraction.** Build h and p as local operators on the physical (blocked) lattice, ASCEND both
to the SI layer via MERAKit's native `ascend` (which includes the disentanglers — the same
machinery that makes h's expectation value correct), then within the Δ∈[1.8,2.2] even subspace:

  1. Project h_ascended and p_ascended onto the Δ≈2 even eigenspace of the one-site scaling
     superoperator (span of the near-degenerate Δ≈2 eigenoperators from `onesite_scaling_operators`).
  2. Subtract the identity/lower-descendant components of h (Gram–Schmidt against 𝟙 and against
     any Δ<2 operator, exactly as the current code orthogonalizes ε against 𝟙).
  3. Define the two physical reference operators:
        𝒪_+ = P_{Δ=2}(h) − (its 𝟙, ε components)      → ∝ (T + T̄)
        𝒪_− = P_{Δ=2}(p)                                → ∝ (T − T̄)
  4. Normalize each to unit PEV 2-pt coefficient under Eq. 10 (twopoint against ρ₂), then form
        T   = (𝒪̂_+ + 𝒪̂_−)/√2 ,   T̄ = (𝒪̂_+ − 𝒪̂_−)/√2         (A4)
     where 𝒪̂_± are unit-normalized. The √2 makes ⟨TT⟩=⟨T̄T̄⟩=1 and ⟨TT̄⟩=0 IF 𝒪̂_+ ⟂ 𝒪̂_−
     under the 2-pt form (checked — see gate G3). (A4) is the discrete analog of
     T = ½(h + ip) in the continuum current algebra.

**Why recommended.** (i) Uses only operators MERAKit already ascends correctly — no new tensor
network primitive. (ii) h is the SAME object whose expectation gives the validated ground-state
energy, so its ascension is battle-tested. (iii) The reflection-parity of p vs h is exact on the
lattice, giving a clean, non-heuristic separation. (iv) Directly yields both T and T̄, enabling
the ⟨TT̄⟩=0 falsification probe (Section 4). (v) Degrades gracefully: if p is hard to build, the
2-pt null-pairing fallback (Route D) recovers the same 2-dim {T,T̄} basis from 𝒪_+ alone plus one
more Δ=2 even eigenoperator.

**Cost/risk.** Requires the analytic lattice momentum density p. For blocked TFIM this is
p_r = i[h_{r−1,r}, h_{r,r+1}]; it is a 3-site operator on the UNBLOCKED chain (2-site after
blocking), so it fits the physical-layer operator width and ascends like h. Build and unit-test
p by checking ⟨p⟩=0 in the ground state (a current has zero expectation) and that its ascended
dimension is ≈2 in the correct (spin-odd) sector.

---

### ROUTE B — lattice translation phase on the WIDTH-2 scaling operators (the "momentum" route)

**Idea.** MERAKit's `scalingdimensions` diagonalizes the **width-2** ascending superoperator
(`causal_cone_width(TernaryLayer)=2`); its eigenoperators live on a 2-site interlayer space and
CAN carry a translation phase, unlike the one-site operators used in the current pipeline. Conformal
spin s manifests as the eigenvalue of the one-site lattice translation T̂ acting on the width-2
fixed-point operators: T̂ φ_s = e^{iθ_s} φ_s with θ_s → (2π/N_eff)·s in the continuum, so T
(s=+2) and T̄ (s=−2) are the two eigenvectors with conjugate phases within the Δ≈2 width-2 block.

**Procedure.** (1) Compute the width-2 scaling operators via `scalingdimensions`-style eigsolve on
`ascend(·, SI-layer)`. (2) Within the Δ≈2 degenerate block, build the lattice translation-by-one
superoperator on the width-2 space (cyclic shift composed with one ascension — the ternary MERA's
translation-by-3 is trivial by SI; translation-by-1 is the non-trivial generator). (3) Simultaneously
diagonalize the scaling superoperator and the translation operator in the block; the eigenphases
±θ label spin ±2. (4) Feed the spin-+2 eigenoperator into the 3-pt machinery.

**Assessment — SOUND BUT HARDER.** The width-2 eigenoperators genuinely carry momentum, so this
is theoretically the "purest" route. But: (a) constructing the explicit translation-by-one operator
on the ternary width-2 fixed-point space is non-trivial (translation by 1 site is NOT a symmetry of
a single ternary block; it maps between the three inequivalent registrations — `ascend_left/mid/right`).
The correct generator is the "one-site shift" that PEV's Fig 2(iii) three registrations encode, and
extracting a single unitary phase from it requires care about the block boundary. (b) The current
VALIDATED pipeline is built entirely on the ONE-SITE superoperator; switching σ/ε/T to the width-2
superoperator is a larger rewrite and re-validation than Route A. **Recommend as the independent
cross-check** (if Route A gives C_TTT≈4 and Route B agrees, the number is bulletproof), not as the
primary route.

---

### ROUTE C — ascended h and p as the T±T̄ generators (this is Route A's engine, stated as a route)

Route C is the mechanism inside Route A: T = ½(𝒪_h + 𝒪_p), T̄ = ½(𝒪_h − 𝒪_p), from the ascended
energy density (spin-0, T+T̄) and momentum density (spin-1, T−T̄). Listed separately only to be
explicit that the "h gives T+T̄, p gives T−T̄" identity IS the physics; Route A wraps it with the
projection + normalization plumbing. **Is the momentum density available as a local operator?** Yes
for TFIM: p_r = i[h_{r−1,r}, h_{r,r+1}] is exactly local and analytically known; for tricritical
Ising (the Blume–Capel / dilute A3 lattice realization or the O'Brien–Fendley Ising+next-nearest
model used to reach c=7/10) the energy current is likewise p = i[h,h'] of adjacent local terms —
build it the same mechanical way from whatever h the Potts/TCI driver uses. This generality is why
Route A is portable across the c-ladder.

---

### ROUTE D — 2-point null-pairing basis (fallback / internal consistency check)

**Idea.** Use ⟨T T̄⟩ = 0 (T1) directly. Restrict the 2-point matrix C_αβ = twopoint(φ_α, φ_β, ρ₂)
to the Δ≈2 even subspace {φ₁, φ₂} (the two near-degenerate eigenoperators). In the {T, T̄} basis
the 2-pt Gram matrix in the CHIRAL-conjugate structure is off-diagonal-dominated: ⟨TT⟩=⟨T̄T̄⟩=0 in
a purely holomorphic 2-pt at EQUAL points?? — **no**: on the lattice at finite separation
⟨T(r)T(0)⟩ = (c/2) r⁻⁴ ≠ 0. So the naive Gram matrix in the {T,T̄} basis is diag(c/2, c/2) r⁻⁴, NOT
off-diagonal. The vanishing ⟨TT̄⟩ only distinguishes the CROSS term. This means the 2-pt matrix
ALONE is degenerate (proportional to identity on the {T,T̄} subspace) and CANNOT by itself pick the
spin eigenbasis — any orthonormal rotation of {T,T̄} is still 2-pt-orthonormal.

**Assessment — INSUFFICIENT ALONE (stated honestly).** Route D cannot resolve spin from the 2-pt
function on a line, because on a line ⟨TT⟩ and ⟨T̄T̄⟩ are both nonzero and equal, leaving a U(2)
degeneracy. It becomes useful only combined with a spin-odd probe (Route A's p, or Route B's
translation phase). Its real role: once Route A fixes T, verify ⟨T̂ T̄̂⟩/√(⟨TT⟩⟨T̄T̄⟩) ≈ 0 as the
G3 falsification gate. **Do not use Route D as a standalone spin resolver — it is provably
insufficient (U(2) degeneracy on the line).** This is the honest negative that rules out the
"just use ⟨TT̄⟩=0 on the 2-pt matrix" shortcut suggested in the design questions.

---

### Route ranking summary

| Route | Mechanism | Verdict | Role |
|-------|-----------|---------|------|
| **A** | ascended h (T+T̄) + p (T−T̄), reflection-parity split | **RECOMMENDED** | primary |
| B | width-2 translation-phase eigenbasis | sound, harder | independent cross-check |
| C | = A's engine (T=½(h±p)) | — | the physics inside A |
| D | 2-pt null-pairing ⟨TT̄⟩=0 | **insufficient alone** (U(2) degeneracy on the line) | G3 verification only |

---

## 4. Contamination control / falsification probes (the C_sss analog)

The current pipeline's decisive discriminant was the Z2-forbidden C_σσσ → 0. For C_TTT the analogous
probes are:

- **G3 — chiral orthogonality ⟨T T̄⟩ = 0.** After forming T, T̄ by Route A, compute the normalized
  cross 2-pt |⟨T T̄⟩| / √(⟨TT⟩⟨T̄T̄⟩). Must be < ~0.05. A nonzero value means 𝒪_+ and 𝒪_− were not
  the clean spin-0/spin-1 combinations (contamination from the Δ=2.2 ε-descendant at c=7/10, or
  basin noise). This is the primary "route worked" gate.

- **G4 — spurious mixed constant C_{T T̄ 𝟙} and C_{T T̄ ε}.** ⟨T(z)T̄(z̄)X⟩ for a scalar X: by chiral
  factorization ⟨T T̄ X⟩ = ⟨T⟩_X-type terms that vanish for X=𝟙 (⟨T T̄⟩=0) — so C_{TT̄𝟙} → 0 is a
  structural probe. Its non-vanishing flags a broken chiral split.

- **C_TTε (allowed but computable).** In Ising, the fusion T × T contains 𝟙 and ε-tower descendants;
  the primary ε appears via the descendant channel. The leading C_{TTε} is fixed but small; treat as
  a SECONDARY consistency number, not a gate (its exact value requires the descendant OPE coefficient,
  out of scope for v1). Do NOT gate on it.

- **G5 — the number itself.** C_TTT within ±10% of 4.000 (Ising) STABLE across ≥3 clean basins
  (|Δ_σ−0.125|<0.10 AND the Δ≈2 even block cleanly 2-dimensional, i.e. the 3rd even eigenoperator
  has Δ > 2.5). One clean basin is the false-positive trap (bit twice before: SIM-056, SIM-058).

- **Reflection-symmetry self-check:** C_T̄T̄T̄ must equal C_TTT (parity). If they differ by more than
  basin spread, the h/p split is asymmetric — a plumbing bug.

**Gate order:** G3 (chiral orthogonality) is checked FIRST — if T and T̄ are not clean, the number is
meaningless regardless of what it reads. Only on G3 pass does G5 (the number) count.

---

## 5. Implementation plan for `qw_ope_pev_z2.jl` extension

New driver `qw_ope_cttt.jl`, reusing the v4 machinery verbatim where possible. Changes/additions:

**Reused unchanged (from qw_ope_pev_z2.jl / ope_cone_v2.jl):**
- `optimize_ising_mera_z2`, `sector_dims`, `densify_mera`, `diag_parity`, `verify_covariance`
  (the Z2-symmetric optimize → densify → covariance-verify front end — do not touch).
- `onesite_scaling_operators` (the one-site eigsolve — reused to get the Δ≈2 even eigenoperators).
- `fixedpoint_rho2`, `rho1_from_rho2`, `twopoint`, `gram_schmidt`, `build_rho3_cone`,
  `build_rho3_mirror`, `ope_from_rho3` (kinematics — the (1,1,2) factor with Δ→2 is already correct
  per Section 1.4, since T is all-holomorphic).

**New code:**
1. `build_energy_density(k0, k1)` / reuse the DemoTools `h` blocked to physical layer — ASCEND it
   to the SI layer with MERAKit `ascended_operator(h, md, nt+1)` to get 𝒪_h on the densified SI space.
   (Careful: ascend on the DENSE MERA `md`, matching the space the one-site operators live on.)
2. `build_momentum_density(k0, k1)` — construct p = i[h_{bond1}, h_{bond2}] on the physical blocked
   lattice (a width-2 operator after blocking); ascend the same way to get 𝒪_p. Unit-test: ⟨p⟩≈0.
3. `resolve_stress_tensor(md, rho2, rho1)`:
   - eigsolve one-site scaling operators (howmany≥20 to capture the Δ≈2 block).
   - even-sector indices with Δ ∈ [1.8, 2.2] (parity_of > +0.5) → the degenerate block B.
   - project 𝒪_h, 𝒪_p onto span(B); Gram–Schmidt 𝒪_h against 𝟙 and the ε operator (remove Δ<2 tails).
   - unit-normalize 𝒪̂_+ = 𝒪_h/√⟨𝒪_h 𝒪_h⟩, 𝒪̂_− = 𝒪_p/√⟨𝒪_p 𝒪_p⟩ under twopoint(·,·,rho2).
   - T = (𝒪̂_+ + 𝒪̂_−)/√2, T̄ = (𝒪̂_+ − 𝒪̂_−)/√2. Return T, T̄, and diagnostics (block dim, ⟨TT̄⟩).
4. `analyze_cttt(m_z2, k0, k1)`: front end identical to `analyze`, then resolve_stress_tensor,
   then C_TTT = ope_from_rho3(T, T, T, 2.0, 2.0, 2.0, rho3avg) over both registrations A/B; also
   C_{TT̄𝟙}, C_T̄T̄T̄, and the G3 cross-2pt. Kinematic factor uses Δ=2 for all three (Section 1.4).
5. `main`: same seed loop; gate on G3 then G5.

**χ requirements.** The Δ=2 even block needs the identity's level-2 descendant (T,T̄) resolved
cleanly. Ising σ/ε converge by χ=6; T/T̄ are higher in the tower and need more bond dimension:
- **χ=6 (K0=K1=3):** SMOKE — expect the Δ≈2 block present but possibly noisy; use to debug plumbing
  and confirm G3 direction. Do NOT expect C_TTT=4 tight here.
- **χ=8 (4,4):** first real attempt at the number.
- **χ=10–12 (RunPod A100, ~$10–20, APPROVED per prior gate):** the tight Ising C_TTT=4.000 and then
  the tricritical C_TTT=3.381. This is where the flagship number is claimed.

**Order of operations:** (1) Ising χ=6 smoke → plumbing + G3 sign. (2) Ising χ=8 local → number ≈4?
(3) Only on pass: RunPod χ=10–12 Ising tight, THEN tricritical. Never jump to c=7/10 before Ising=4
is locked — same discipline that saved the C_σσε validation.

---

## 6. Risks and failure signatures (judge the run honestly)

- **R1 — momentum density p wrong / not clean.** If p is mis-constructed, 𝒪_− is not pure spin-1
  and G3 (⟨TT̄⟩≠0) fires. Signature: cross-2pt ~ O(1), C_TTT wanders with basin. Mitigation: unit-test
  ⟨p⟩≈0 and Δ_p≈2 in the reflection-odd sector BEFORE trusting any C_TTT.
- **R2 — Δ=2.2 ε-descendant contamination (tricritical only).** At c=7/10 the L_{−1}L̄_{−1}ε scalar at
  Δ=2.2 leaks into the [1.8,2.2] window. Signature: 3rd even eigenoperator at Δ≈2.2 with spin 0; the
  projection of 𝒪_h picks it up. Mitigation: tighten window to [1.9, 2.1] at c=7/10 and Gram–Schmidt
  𝒪_h against it explicitly; if Ising (no such contaminant) gives 4.0 but TCI does not, this is the
  suspect — report as such, not as a physics failure.
- **R3 — finite-χ tower truncation.** T,T̄ sit above σ,ε in the tower; at χ=6 they may be poorly
  represented (PEV needed χ=22 for tight OPE numbers). Signature: Δ of the "T" eigenoperator far from
  2.0, C_TTT far from 4 with LARGE basin spread but G3 OK. Mitigation: this is the expected reason to
  escalate χ; NOT a route failure. Distinguish from R1/R2 by whether G3 passes.
- **R4 — normalization convention drift.** If C_TTT comes out ≈ 4·(c/2)^{±k} for some integer k, the
  operator was not unit-normalized under Eq. 10 (e.g. normalized to ⟨TT⟩=c/2 instead of 1). Signature:
  a clean but wrong-by-a-c-power number. Mitigation: the C_σσε=0.5 check in the SAME run pins the
  normalization convention — if C_σσε≠0.5 the whole normalization is off, discard C_TTT.
- **R5 — the honest null result.** If G3 passes (T,T̄ clean) across ≥3 basins but C_TTT stabilizes at
  a value ≠ 4.0 (Ising) that does NOT move toward 4 as χ increases χ=6→8→10, the PEV-route 3-pt
  extraction does not capture the stress-tensor self-coupling on the lattice — a genuine negative to
  report, analogous to the OPE-cone honest negatives already in the record. In that case the finding is
  "MERA one-site PEV extracts scalar OPE (C_σσε) but not spin-2 self-coupling (C_TTT)," which is itself
  publishable methodology and seeds a width-2 (Route B) follow-up.

**What success looks like:** C_TTT = 4.00 ± 0.4 stable across ≥3 clean Ising basins with G3 cross-2pt
< 0.05, C_σσε = 0.50 in the same run (normalization pinned), C_T̄T̄T̄ = C_TTT (parity). Then the novel
claim: C_TTT = 3.38 ± 0.4 at tricritical Ising c=7/10 = the emergent graviton self-coupling at the
novel central charge.


