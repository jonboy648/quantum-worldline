# Run A (HYP-028) — Yang-Lee non-unitary force: realization, gates, protocol

**Status:** EXECUTED 2026-06-26 (228.7 s, local CPU). Verdict **INVALID** (honest negative):
G3 unitary control PASSED (α(N=16)=3.951), G5 PT-unbroken PASSED, but **G4 criticality
gate FAILED at all N** — c_eff=0.520–0.525 (target 0.40) and Δ_φ=+0.453…+0.457 (target
−0.20) stayed at the *unitary* Ising values inside the PT-unbroken window. The two-end
realization does not reach the bulk Yang-Lee fixed point at ED sizes; the non-unitary
α=3.75–3.78 (drift 0.03) is the unitary α by proximity and is NOT reported as a
non-unitary observable. HYP-028 stays OPEN. Full numbers in SIM-2026-055.json.
**Script:** `research/data/simulations/hyp028b_yanglee_force.py`
**Predecessor:** SIM-2026-053 (`hyp028_nonunitary_force.py`), verdict INCONCLUSIVE.

## 1. The realization problem

The goal is to measure the holographic force exponent α at a *non-unitary* (Yang-Lee)
critical point and ask whether α=4=2·Δ_T survives the loss of unitarity. The mechanism
hinges on Δ_T=2, which is a theorem only in **unitary** 2D CFT; at the non-unitary
Yang-Lee M(2,5) fixed point (c=−22/5, effective c_eff=2/5, lightest primary
Δ_φ=−1/5) that protection is revoked.

SIM-053 used the **uniform imaginary field** Ising chain
`H = −ΣZZ − ΣX − iγ ΣZ`. Its Yang-Lee critical point sits **at** the PT-breaking
edge, with κ_c(N) ~ 1/N (smoke scan: 0.0105/0.0074/0.0056/0.0043 at N=10/12/14/16).
Staying PT-unbroken forces γ ≈ 0.9·κ_c ≈ 0.004 at N=16 — a ~0.1% non-Hermitian
perturbation. The resulting α≈4 reflected **proximity** to the unitary point, not
survival at a genuine non-unitary fixed point. Verdict: INCONCLUSIVE; the realization
was structurally obstructed at ED sizes.

## 2. The realization chosen for Run A

The design asked for a realization whose Yang-Lee point sits at a **finite distance
inside the PT-unbroken phase**. Single-particle (number-conserving free-fermion)
probing (`scratchpad/probe_ff.py`) showed:

| imaginary potential | single-particle PT window (real gaps) |
|---|---|
| uniform iγ | trivial (uniform Im shift; gauge, not Yang-Lee) |
| staggered iγ(−1)^i | shrinks with N (0.2→0.1) |
| boundary iγ on site 0 | window 0 (defective) |
| **two-end iγ(δ_0 − δ_{N−1})** | **finite, N-independent (~0.7 at N=12,14,16)** |

The two-end PT-symmetric imaginary **boundary** field
`H = −ΣZZ − ΣX − iγ(Z_0 − Z_{N−1})` was selected as the Run A realization.
PT = (reflection)·(complex conjugation): reflection swaps sites 0↔N−1 and K conjugates
iγ→−iγ, so the antisymmetric pair (+iZ_0, −iZ_{N−1}) is PT-invariant.

## 3. Honest caveat carried into the gate (NOT assumed away)

A free-fermion single-particle window is **not** the many-body window of the spin
TFIM: the spin chain `−ZZ−X` is a *paired* (BdG) fermion problem, and the imaginary
boundary field interacts with the pairing. Moreover an imaginary **boundary** field
drives a **boundary** Yang-Lee criticality, whereas the M(2,5) data (c_eff=2/5,
Δ_φ=−1/5) is a **bulk** fixed point. Whether the two-end realization reaches the
bulk Yang-Lee fixed point at ED sizes is exactly what the G4 criticality gate decides.
If G4 fails, the run is **INVALID** (the realization did not reach the fixed point),
which is an honest negative, not a refutation and not a forced number.

## 4. Mandatory gates (executed in order)

- **G2 — biorthogonal layer.** All expectations are ⟨L|O|R⟩/⟨L|R⟩ from left+right
  ground vectors via `scipy.sparse.linalg.eigs` (non-Hermitian), biorthonormalized
  ⟨L|R⟩=1. Reused verbatim from the validated SIM-053 pipeline.
- **G3 — unitary control (γ=0).** The identical biorthogonal layer at the Hermitian
  Ising point must reproduce α≈3.95. (Smoke: α=4.086 at N=10; full run reports N=16.)
- **G4 — non-unitary criticality.** Two independent diagnostics, both across N=12,14,16:
  1. **c_eff** from biorthogonal entanglement entropy. RDM ρ_A = Tr_B|R⟩⟨L|; fit
     S(L) = (c_eff/6)·ln[(2N/π)·sin(πL/N)] + const over interior cuts. Target 2/5±0.05.
  2. **Δ_φ** from the finite-size gap. E_1−E_0 = (πv/N)·Δ_φ with v fixed at the Ising
     sound speed v=2; Δ_φ = (E_1−E_0)·N/(πv). Target −1/5±0.04.
  Gate PASS requires both, at all three N. Else INVALID.
- **G5 — PT-unbroken.** max|Im(E)| < 1e−6 over the low spectrum; α reported across
  N=12,14,16 with drift < 0.4.

## 5. Force estimator (identical to the validated pipeline)

Boundary-primary interaction energy
`V(dr) = E_dual − E_gs − dE_anchor − dE_probe`, with the boundary-primary operator
σ_j = α_BP(X_j + X_{j+1}) + β_BP(X_jZ_{j+1} + Z_jX_{j+1}), α_BP=0.635, β_BP=−0.026,
applied to both bra and ket and renormalized ⟨L|R⟩=1 at each step. Fit V(dr≥2) to
A·dr^{−α} (exclude the dr=1 contact term). This is the SIM-015d / SIM-053-validated
estimator (γ=0 control reproduces α≈3.95–4.09), NOT the superseded connected-ZZ
observable (which gave spurious α≈0.54).

## 6. Verdict logic (pre-registered)

1. G3 control fails → **INVALID** (estimator broken).
2. G4 gate fails → **INVALID** (not at the Yang-Lee fixed point; α uninterpretable).
3. PT broken at γ_c → **INCONCLUSIVE**.
4. drift > 0.4 across N → **INCONCLUSIVE** (finite-size dominated).
5. G3+G4+G5 pass AND 3.2 ≤ α_16 ≤ 4.8, stable → **REFUTED** (α=4 generic, survives
   loss of unitarity — stronger universality).
6. G3+G4+G5 pass AND α_16 outside [3.2,4.8] → **SUPPORTED** (α=4 conditional on
   unitarity; force tracks the model-specific primary).
