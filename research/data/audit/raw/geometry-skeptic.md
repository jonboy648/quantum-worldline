# adv:geometry-skeptic — The case that Hypothesis A is true

**Role:** Geometry Skeptic (RESEARCH-DIRECTOR §27).
**Assumption granted by the assignment:** RESEARCH-DIRECTOR §4 **Hypothesis A** — *MERA is an
efficient hierarchical representation of critical quantum states; apparent geometry is descriptive
or computational and adds no independently predictive content beyond the underlying CFT and
tensor-network structure.*
**Task:** make that case as strongly as the evidence permits, apply §34 quantity-by-quantity, address
§33, test the 012/014/022/026 pattern, and name the experiment that would refute me.
**Date:** 2026-08-17 · **Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md`

Every claim below is cited to a repo-relative path plus a field, line, or a computation I ran and
show. Where I could not verify, see **§10 UNVERIFIED**. I have flagged where my own case is weakest
(§8) rather than only where the project's is.

---

## 0. Headline

**In the project's four flagship "geometric" measurements, the tensor network is either never
executed, or is executed and then shown to be irrelevant.**

Three findings carry this, in descending order of severity:

1. **The holographic-transport measurement never applies a MERA.**
   `research/data/simulations/holographic_transport_16q.py:347` prints
   `"  Skipping full MERA bulk computation (complex to implement correctly)"`. The MERA tensors `u`,
   `w` are built at lines 46–58, their unitarity is printed at lines 60–61, and they are then
   **never used again**. The entire measurement is: exact ground state of the Wang–He boundary spin
   chain (`eigsh`, line ~150), a Gaussian Y-coupled pulse, time evolution under that same boundary
   Hamiltonian, and one-site boundary expectation values ⟨Y_j⟩, ⟨Z_j⟩. The 24-qubit and fine-dt
   re-runs are the same: `holographic_transport_24q.py` and `holographic_transport_24q_v3.py` contain
   the string "MERA" only in their docstring and banner (2 and 1 occurrences respectively, both in
   comments), and `holographic_transport_finedt.py` mentions MERA only inside analysis prose at lines
   499–581. **The project's only dynamical, "causal-structure" evidence for emergent geometry is a
   boundary-Hamiltonian measurement on a state with no tensor-network representation in the loop.**

2. **The one constant that carries all the geometry, `l_AdS`, is declared by the manuscript itself to
   be a property of the representation.** `research/submission-package/prd/paper-prd.tex:64–66`:
   `\lAdS = 1/\ln\chi = 1/\ln 2 = 1.4427` followed verbatim by *"This value is set by the MERA
   architecture, not by optimization."* Under §34 that sentence **is** the concession: an
   architecture-set number is a representation property by definition. The same manuscript's fourth
   headline result is a **χ = 3** MERA of the same critical Ising state
   (`SIM-2026-015d.json` → `chi: 3`); under the paper's own Eq. (2) that state has
   `l_AdS = 1/ln 3 = 0.9102`, and the transport prediction becomes `(π/2)(0.9102) = 1.4296` against a
   measurement of 2.239 — a **+57 % failure**. The paper reports both numbers and never notices that
   its own bond-dimension upgrade destroys its own geometric prediction.

3. **The force exponent α = 4 is proved analytically, from BPZ 1984 fusion rules, inside this
   repository, with no geometry anywhere in the derivation.**
   `research/data/theory/epsilon-channel-proof.md:1–14`: *"The Ising fusion rule epsilon x epsilon = 1
   (identity only) means C_{eps,eps,eps} = 0 exactly. There is no epsilon conformal block to cancel.
   The stress tensor T is the leading nontrivial primary in the s-channel decomposition, giving
   alpha = 2*Delta_T = 4 automatically."* The measurement that "confirms" it is performed on an
   **exactly diagonalized** 24-qubit chain (`exact_gs_force_profile_24q.py`) — a state with no
   network, no layers, no bulk. The χ=3 MERA reproduces the same number (4.071 vs 3.975,
   `SIM-2026-015d.json`) precisely because it is a good approximation to that same state.

A fourth, sharpening the third: **α = 3.92 ± 0.16 is not a plateau.** I refit the record's own data
(§3.1). The local log-slope of `SIM-2026-011-interaction.json` → `F_interaction_avg` runs
2.04 → **4.23** → 2.60 → 2.46 → 2.46 → 2.53 → 2.66 → 2.84 → 3.10 → 3.48 → 4.06 across dr = 1…12.
The recorded α = 3.9218 ± 0.1590 is exactly reproduced by an **unweighted linear-space**
`curve_fit` over dr ≥ 2 (I recovered A = 8.6727, α = 3.9218, σ = 0.1590 to four decimals), a fit in
which the single point dr = 2 carries ~99 % of the weight because the data span three decades. The
statistically appropriate log-space fit over the same window gives **α = 2.89**.

Conclusion of this audit: **on the present evidence, Hypothesis A is not merely tenable — it is the
position the project's own records support.** Every geometry-flavored quantity the project has
measured either (a) reduces to a boundary CFT number fixed in advance by symmetry, (b) reduces to a
constant chosen by the network architecture, or (c) has been formally refuted. I could not find a
single measured quantity that is simultaneously (i) sensitive to the network's internal organization
and (ii) not recoverable from boundary observables. §9 states the experiment that would change my
mind, with failure criteria fixed before it is run.

---

## 1. Method and scope

**What I read.** All 30 hypothesis records; the geometry-relevant simulation records
(`SIM-2026-011`, `-011-interaction`, `-015d`, `-016`, `-018`, `-023`, `-024`, `-031`, `-051`,
`-062`, `-063`, plus `composite_geodesic_results.json`, `effective_mass_analysis.json`,
`holographic_transport.json`, `hyp010_criticality_scan.json`, `worldline_mc_results.json`); the
pipeline scripts behind them (`holographic_transport_16q.py`, `holographic_transport_24q*.py`,
`holographic_transport_finedt.py`, `composite_geodesic_test.py`, `sim2026024_pee_crofton.py`,
`cmi_crofton_test.py`, `exact_gs_force_profile_24q.py`, `hyp010_criticality_scan.py`);
`research/ERRATA.md`; `research/data/theory/epsilon-channel-proof.md`;
`research/submission-package/prd/paper-prd.tex` and `references.bib`.

**What I computed.** Independent refits of the force profile (log-space, linear-space, sliding
windows, local slopes, two-channel CFT model). Numbers and code shown inline in §3.1 and §11 so they
can be checked.

**Phase-1 overlap, declared.** `independence-ledger.md` L-01/L-02 already established that the
transport comparison is convention-dependent with three competing `l_AdS` values, and that
m_eff 0.693 vs 0.670 is algebraically `1/l_AdS` vs `l_AdS/ξ`. `inv-sims-early.md` §0 already
established the dr = 2 fragility of α. `inv-manuscript-claims.md` C-10/CL-2 already established that
the manuscript itself states Δ_T = 2 is fixed by symmetry. **I do not re-derive those; I cite them
and build on them.** Everything marked **NEW** below is not in any phase-1 artifact (I grepped
`research/data/audit/raw/` for each).

---

## 2. The nine geometry-flavored quantities

Inventory first, then §3 works each one.

| # | Quantity | Where measured | Reduces to | §34 verdict |
|---|---|---|---|---|
| G1 | Force exponent α ≈ 4 in F(dr) ~ dr^−α | `SIM-2026-011-interaction.json`, `-015d`, `-023` | 2Δ_T = 4, BPZ fusion rules | **state property** — and therefore geometry-blind |
| G2 | "Worldline" framing of the force | `worldline_mc_results.json`, paper §5 | a linear relabelling r_geod = dr · l_AdS | **representation, and self-contradictory** |
| G3 | Transport T = (π/2)·l_AdS | `holographic_transport.json`, `composite_geodesic_results.json` | one lattice→continuum time-unit conversion | **representation** — MERA never executed |
| G4 | m_eff = 0.693 vs 0.670 (3.5 %) | `effective_mass_analysis.json` | ξ_2pt ≈ l_AdS², one two-point ratio | **algebraically dependent** |
| G5 | Synge distance d(r), HYP-026 | `SIM-2026-031.json` | 2Δ_σ = 1/4, exactly | **state property**, guaranteed in advance |
| G6 | CMI thread density σ(dr), HYP-012 | `SIM-2026-016.json` | CMI decay of the ED ground state | **state property**, and NOT_SUPPORTED |
| G7 | Crofton integrals, HYP-014 / HYP-022 | `SIM-2026-018.json`, `SIM-2026-024.json` | nothing — **both REFUTED** | n/a |
| G8 | l_AdS itself | `paper-prd.tex:64` | 1/ln χ, a declared architecture constant | **pure representation** |
| G9 | Bulk geodesic distance d_geo | paper §5 L257/L529 vs `worldline_mc_results.json` | two mutually incompatible definitions | **representation, and ill-defined** |

---

## 3. Quantity-by-quantity reduction

### 3.1 G1 — the force exponent α ≈ 4

**What is claimed.** `paper-prd.tex:29` (abstract): *"the interaction energy between boundary-primary
excitations follows a power law F(dr) ~ dr^−α with three consistent evaluations yielding
α = 3.92 ± 0.16 (24 qubits), 3.97 ± 0.15 (16 qubits), and 4.07 ± 0.18 (16-qubit χ=3 MERA), all
consistent with stress-tensor exchange (α = 4, conformal dimension Δ_T = 2)."*

**Reduction to ordinary CFT data — the project has already done it.**
`research/data/theory/epsilon-channel-proof.md:5–9` derives α = 2Δ_T = 4 from the M(3,4) fusion rule
ε × ε = 1 (BPZ 1984), i.e. from the Kac table and nothing else. The manuscript concedes the same at
`paper-prd.tex:427`: *"Δ_T = 2 is a kinematic constant of conformal symmetry, independent of the
central charge."* §6 counterfactual novelty is therefore **near zero**: before running, the only
outcomes were "the implementation works" or "it doesn't."

**The geometry adds nothing, demonstrated internally.** The probe operator is
`exact_gs_force_profile_24q.py:105–113`:
`sigma^boundary_j = ALPHA*(X_j + X_{j+1}) + BETA*(X_j Z_{j+1} + Z_j X_{j+1})`, with
ALPHA = 0.635, BETA = −0.026 (`SIM-2026-011-interaction.json` → `boundary_primary_coeffs`). This is a
**local boundary operator** acting on a state obtained by **exact diagonalization**
(`SIM-2026-011-interaction.json` → `ground_state.method: "eigsh(H, k=1, which='SA')"`, `qubits: 24`).
There is no network in the 24-qubit measurement at all. The observable is
`F(dr) = E_dual − E_0 − 2·dE_single_avg` — three energies of the same boundary Hamiltonian.
A quantity computable from ED on a bare spin chain cannot be evidence for structure in a
representation that was not used to compute it.

**The χ = 3 MERA agreement is the wrong way round.** `SIM-2026-015d.json` gives exact 3.9748 and
χ=3 MERA 4.0712 for the same 16-qubit system. The MERA agrees with ED because the MERA is a good
approximation to the ED state (`E_mera = −19.9861` vs `E0_exact = −20.0164`, 0.15 %). Agreement here
measures **ansatz fidelity**, not bulk physics. Under Hypothesis B one would need the MERA to predict
something ED does not; here it reproduces what ED already gives, less accurately.

**And the number is fragile.** I refit `SIM-2026-011-interaction.json` → `F_interaction_avg` directly
(code in §11):

| fit | window | α | note |
|---|---|---|---|
| linear-space `curve_fit` (the record's method) | dr ≥ 2 | **3.9218 ± 0.1590** | exactly reproduces `fits.F_avg_dr_ge2.power_law` incl. A = 8.6727 |
| linear-space `curve_fit` | dr ≥ 3 | **2.5593 ± 0.0187** | drop one point → −1.36, ≈ 8.6 σ |
| linear-space `curve_fit` | dr ≥ 4 | 2.5340 ± 0.0377 | |
| log-space OLS (equal relative weight) | dr = 2…12 | **2.890** | the statistically correct fit |
| log-space OLS | dr = 3…12 | 2.700 | |
| log-space OLS | dr = 6…12 | 2.981 | |

Local log-slopes −d ln|F| / d ln dr, dr = 1→12:
`2.04, 4.23, 2.60, 2.46, 2.46, 2.53, 2.66, 2.84, 3.10, 3.48, 4.06`.
There is **no plateau at 4**. The single interval dr = 2→3 has slope 4.23; the interior of the range
sits at 2.45–2.7; the rise at the far end (3.48, 4.06 at dr = 10→12) is where the probe approaches
the open boundary of the 24-site chain, i.e. a finite-size edge effect, not a deeper bulk.
The same behaviour holds at 16 qubits in **both** evaluations: exact 3.975 → 2.753 on dropping dr=2;
χ=3 MERA 4.069 → 2.650. The three "consistent evaluations" are consistent because they share the
same single dominant point, not because three independent measurements converged
(§7: **structurally dependent**, not independent).

**Alternative conventional explanation, tested and reported honestly.** The probe's β term
(X_jZ_{j+1} + Z_jX_{j+1}) is Z₂-odd under P = ∏X while the α term is Z₂-even, so the probe is ~96 %
ε-channel with a ~4 % σ admixture; that admixture opens σ × σ = 1 + ε and would add a slower
dr^−2Δ_ε = dr^−2 tail, which would explain the drift from ~4 to ~2.5. **I fitted it and it does not
work**: a two-channel model A·dr^−4 + B·dr^−2 fitted in log space gives max relative residual 30.5 %
versus 29.4 % for a single power law — no improvement. So I cannot attribute the drift to channel
mixing. The honest statement is weaker and still fatal to the precision claim: **the recorded F(dr)
is not described by any clean CFT power law over dr = 2…12 at better than ~30 %**, and the quoted
±0.16 uncertainty does not represent that.

**§5 level:** Level 1 (reproduction/validation) of a BPZ-1984 identity, measured on an ED state.
**§34:** invariant across representations (ED = MERA), recoverable from boundary observables,
independent of bond dimension (χ=3 vs exact agree within 2.4 %), independent of gauge, independent of
optimization history. It is a **state property** — which is exactly why it cannot discriminate
Hypothesis A from B. A state property is the same whatever you represent it with.

### 3.2 G2 — the "worldline" framing

The word is doing the load-bearing work in the project title and in `paper-prd.tex:219–231`
("Level 1 … Level 2 … Together, these establish: quantum gravity in ADM superspace = worldline path
integral on AdS = measurable MERA observables"). What is actually computed?

`research/data/simulations/worldline_mc_results.json`:
- `parameters.geometry: "Poincare disk H^2"`, `mass: 1.0`, `l_AdS: 1.443`, 100 000 MC paths.
- `force_profile.r_geod_vals = [1.443, 2.886, 4.329, 5.772, 7.215, 8.658, 10.101]` — i.e.
  **r_geod = dr × 1.443, exactly linear in the boundary lattice separation.**

So the "geodesic distance in H²" against which the worldline Monte Carlo is compared is the boundary
separation times a constant. Every H²-specific feature (curvature, geodesic focusing, the
Camporesi–Higuchi heat kernel's non-trivial radial dependence) enters the comparison **only through a
multiplicative rescaling of the abscissa**. A comparison in which the curved-space input is a linear
relabelling of the flat-space input cannot test curvature.

- `heat_kernel_validation`: `Delta_theory = 2.0272` vs `Delta_fit = 2.2821` (12.6 % off);
  `xi_theory = 0.7118` vs `xi_from_analytic_fit = 0.6323` (11.2 % off). The validation of the H²
  machinery itself is at the ~12 % level.
- `force_profile.mera_V` = `[−0.0114, −0.00717, +0.000185, +1.69e−6, −3.0e−15, +2.4e−15, …]` — the
  SIM-2026-002 values that `HYP-2026-005.json` → `analysis.key_findings[1]` calls
  *"numerical noise"* beyond dr = 2 (see `inv-sims-early.md` §1 SIM-2026-002 for the uncorrected-record
  defect). The worldline comparison is anchored on retracted data.
- ERRATA D2: the file *"contains a literal NaN (invalid strict JSON)."*

**§34:** the worldline framing is not a measured quantity at all; it is a naming convention applied
after the fact to a boundary energy difference. It is not invariant, not architecture-specific, not
gauge-dependent — it is **not an observable**. Per §1 of the standard it should be labelled
*motivation*, not *result*. The paper itself half-concedes this at `paper-prd.tex:579`: *"this is
based on only 2 signal points and a post-hoc fit; a systematic study … would be needed to elevate
this from observation to quantitative result."*

### 3.3 G3 — transport T = (π/2)·l_AdS  **[the strongest single case for Hypothesis A]**

**NEW — the MERA is never executed.** `holographic_transport_16q.py`:
- lines 46–58 build the Evenbly–White `u`, `w`;
- lines 60–61 print their unitarity check;
- line 103: comment *"For simplicity, we work in the full 2^L Hilbert space"*;
- lines 276–346 contain the intended bulk computation as **comments only**;
- **line 347: `print("  Skipping full MERA bulk computation (complex to implement correctly)")`**;
- the reported observable is `boundary_density_Y[step, i] = ⟨ψ(t)|Y_i|ψ(t)⟩ − ⟨GS|Y_i|GS⟩`, a
  **one-site boundary expectation value**, from which a dip time and a reappearance time are read off.

The 24-qubit and fine-dt versions never build the tensors at all: `grep -ci mera` gives 2, 1 and 10
occurrences in `holographic_transport_24q.py`, `_24q_v3.py`, `_finedt.py`, and every one is inside a
docstring, a banner, or an analysis comment.

So the measured object is: *how long does a localized wave packet on a 16-site periodic spin chain
take to traverse to the antipode and come back into view.* That is a lattice light-cone crossing
time. It is measured on the Wang–He chain
`H = (L/4π) Σ_j (X_{j−1}Z_jX_{j+1} − X_jX_{j+1})` (`holographic_transport_16q.py:132–142`), whose
`L/4π` prefactor is precisely the normalization that puts the chain on a CFT circle of circumference
2π. **In that normalization the continuum answer for antipodal transport is a pure number with no
geometry input in it at all.**

**The prediction is one fitted unit conversion, and the paper endorses two incompatible values for
it.**
- `composite_geodesic_test.py:56` — `L_ADS_MERA = 1.0 / np.log(K)` with `K = 2` the **MERA blocking
  ratio** (line 53: `K = 2  # sites per MERA block (binary MERA)`), giving 1.4427.
- `paper-prd.tex:64` — `l_AdS = 1/ln χ` with χ the **bond dimension**, giving the same 1.4427
  *only because binary MERA at χ=2 makes the two conventions numerically coincide.*
  They are different conventions and the project has never reconciled them.
- The prediction is then `T = (π/2)·l_AdS = 2.2662`
  (`composite_geodesic_results.json` → `calculations.composite_geodesic.T_null_MERA`).
- But `paper-prd.tex:195, 538, 605` simultaneously assert that *"Wang and He recently proved the null
  geodesic formula t_trans = π analytically in the continuum limit, confirming that the N = 16 result
  agrees with the correct theoretical prediction."* **π = 3.1416 and 2.2662 are not the same
  prediction.** The grid-converged measurement is 2.239 (ERRATA E2). It agrees with 2.2662 to −1.2 %
  and disagrees with π by −28.7 %. The manuscript cites the second as confirmation of the first.
  (Phase-1 `inv-manuscript-claims.md` flags this citation as unsupported by the project's own record
  of the paper; **the numerical incompatibility of the two endorsed predictions is NEW here.**)

Strip the language away and the entire claim is one dimensionless statement:

> T_measured / π = 2.23888 / π = **0.71265**, versus l_AdS / 2 = 1/(2 ln 2) = **0.72135** — agreement
> to 1.2 %.

i.e. *"the lattice-to-continuum time conversion for this chain equals 1/(2 ln 2)."* That is a
**velocity/normalization constant of the boundary Hamiltonian**, compared against a number
(1/ln 2) taken from a network architecture that was never applied to the state. No geometric
quantity was measured on either side.

**The prediction was changed after seeing the data (§18/§36 violation).** The script's own
pre-registered prediction is `T_predicted = np.pi * l_AdS = 4.5324`
(`holographic_transport_16q.py`, tail: `# Geodesic prediction: T = pi … T_predicted = np.pi * l_AdS`),
giving `ratio_measured_predicted = 0.4964` (`holographic_transport.json` → `transport_signature`).
The factor of 2 was then removed by adopting a *different* geodesic (null instead of spacelike) from
a *different* paper (Bohra & Sivaramakrishnan, PAPER-2026-020) in
`composite_geodesic_results.json` → `calculations.composite_geodesic`. §18 requires parameters be
locked before the out-of-sample prediction; here the geodesic class itself was selected after the
measurement, from a binary menu {π, π/2}, choosing the one that fit. The record even preserves the
alternative: `inputs.l_AdS_fitted: 1.233` gives `T_null_fitted_vs_measured.percent_error: −13.92`.
**Two candidate l_AdS values were available; the one that produced 0.7 % was reported as the result
and the one that produced −13.9 % was not.**

**HYP-006's own killer test was never run.** `HYP-2026-006.json` → `test_design`: *"Measure the
transport time T as a function of boundary separation … If the functional form matches arccosh, the
worldline-geodesic interpretation is supported."* → `refutation_criteria`: *"If transport time shows
no systematic dependence on boundary separation, or if the functional form is linear rather than
arccosh, the geodesic worldline interpretation is wrong."* **No arccosh test exists anywhere in the
repository.** A single T at a single antipodal configuration was measured. Status is
`SUPPORTED` / `high`. (Phase-1 `inv-hypotheses.md:162–164, 317` found the same; I confirm it and add
that the substituted formula (π/2)·l_AdS is not the formula in the hypothesis record either.)

**The finite-size behaviour points away from geometry.** `paper-prd.tex:195`: at N = 24 the raw
deviation is **−31.6 %**, rescued by an empirical observation that T·L ≈ const. But
T = (π/2)·l_AdS is an **N-independent** prediction — l_AdS is set by χ (or K), not by system size.
An observable that scales as 1/L is a finite-size boundary timescale, not a fixed bulk geodesic
length. The paper concedes: *"The 3.3 % consistency in T·L … is an empirical observation, not a
derived result. We do not claim a theoretical derivation of T ~ C/L scaling from the MERA geometry."*

**NEW — the project's own control fails at the critical point.** `paper-prd.tex:181`: *"We also scan
seven TFIM coupling values … Transport times range from T = 3.45 to 5.2 in a non-systematic pattern.
None are close to the holographic prediction T = 2.266. The MERA transport time T = 2.25 is uniquely
consistent with the AdS null geodesic formula."* I extracted the scan
(`hyp010_criticality_scan.json` → `approach_B_tfim.results`):

| g | T | residual vs 2.2662 | S_half |
|---|---|---|---|
| 0.75 | 5.20 | +129.5 % | 0.730 |
| 0.85 | 5.10 | +125.0 % | 0.761 |
| 0.90 | 5.00 | +120.6 % | 0.776 |
| 0.95 | 4.00 | +76.5 % | 0.776 |
| **1.00** | **3.80** | **+67.7 %** | **0.750** |
| 1.05 | 3.55 | +56.7 % | 0.697 |
| 1.10 | 3.45 | +52.2 % | 0.631 |

**g = 1.00 is the critical TFIM — the same Ising CFT, c = 1/2, same operator content, same
Δ_T = 2 — and it misses the "holographic prediction" by 68 %.** If the transport time were a
property of the emergent AdS geometry of the critical Ising universality class, two lattice
representatives of that class could differ only by a velocity factor. Instead:
`hyp010_criticality_scan.py:41–58` shows the two Hamiltonians are normalized differently —
Wang–He carries `prefactor = n/(4*np.pi)` = 1.2732 at L = 16, the TFIM control carries
`H = -sum Z_i Z_{i+1} - g sum X_i` with **no prefactor at all**. Correcting for that leaves
3.80/1.2732 = 2.985, still +32 %. And the half-chain entropies differ (1.2895 for Wang–He at δ=0 vs
0.7501 for critical TFIM), so the two states are not even matched on ordinary entanglement data.
**This is not a matched control (§19); it is a comparison in which the Hamiltonian, the
normalization, the state and the entanglement all change at once.** Read straight, its actual content
is the opposite of the paper's reading: *the transport time is not universal across representatives
of the same CFT, therefore it is not a CFT/geometric quantity.*

**The same scan undercuts "uniqueness" from the other side.** `approach_A_wang_he_detuning.results`,
detuning the Wang–He chain by δ·ΣZ:

| δ | T | residual |
|---|---|---|
| −0.3 | 2.00 | −11.7 % |
| −0.2 | 1.95 | −14.0 % |
| −0.1 | 1.70 | −25.0 % |
| **0.0** | **2.25** | **−0.71 %** |
| +0.1 | 3.30 | **+45.6 %** |
| +0.2 | 2.10 | −7.3 % |
| +0.3 | 0.55 | −75.7 % |

The response is **non-monotonic** in the detuning (+45.6 % at δ=+0.1, then −7.3 % at δ=+0.2), which
no smooth geometric deformation produces; and detunings of ±0.2–0.3 — which should destroy the
criticality that supposedly generates the geometry — still land within 12 % of the "geodesic
prediction." Every value in both tables is a multiple of the dt = 0.05 grid, because T is read off as
`reappear_time − dip_time` from a coarse peak-find; ERRATA E2 records that this quantization alone
moved the headline residual from −0.72 % to −1.205 %.

**§5 level:** not Level 4. It is a Level-1/2 measurement of a lattice light-cone time, presented as a
Level-4 causal-structure result.
**§34:** the measured side is a state/Hamiltonian property (boundary dynamics of a chain);
the predicted side is a **pure representation property** (1/ln 2, "set by the MERA architecture") that
was never applied to the state. The comparison is between a boundary observable and an architecture
constant. That is the definition of descriptive geometry.

### 3.4 G4 — m_eff = 0.693 vs 0.670 (3.5 %)

`effective_mass_analysis.json` → `ads_mass_dimension.epsilon_m_squared_l2 = −1.0`,
`epsilon_m_eff = 0.6931`; `comparison_to_measurements.xi_MERA = 2.154`,
`m_eff_from_MERA = 0.6698`.

Side A: Δ_ε = 1 (exact Ising) → m²l² = Δ(Δ−2) = −1 → |m| = 1/l_AdS = ln 2 = 0.693147.
Side B: 1.4426950 / 2.154 = 0.669777 → the record's 0.6698, i.e. side B = l_AdS/ξ.
The claimed agreement is therefore **ξ_2pt ≈ l_AdS² = (1/ln 2)² = 2.0814 vs 2.154**, one two-point
ratio compared against a squared architecture constant. `independence-ledger.md` L-02 reaches the same
reduction; I confirm the arithmetic independently.

Three further facts make this weaker than 3.5 % suggests:
- ξ_MERA = 2.154 is, by the record's own words, *"from only 2 data points (dr=1,2) with limited
  causal cone"* (`effective_mass_analysis.json` → `resolution.explanation`).
- The underlying V(dr) is the SIM-2026-002 data that `HYP-2026-005.json` calls noise beyond dr = 2.
- ERRATA E4 records that the paper's stated derivation (`m²l² = Δ(Δ−1)`, "for Δ=1 this gives m²=0")
  **contradicts the record's own convention** (Δ(Δ−2) = −1), that the two data records disagree with
  each other on convention, and that *"0.693 = ln 2 follows only from Δ=1 exactly."*
- The record's own verdict is `PARTIALLY_RESOLVED`, and its recommendation is *"Re-run worldline MC
  with m = 0.693"* — never done.

**§34:** algebraically dependent on l_AdS on **both** sides. §7 classification: **algebraically
equivalent**, not an independent cross-check. §6 counterfactual novelty: near zero given Δ_ε = 1.

### 3.5 G5 — the Synge distance, HYP-026

This is the project's most methodologically careful geometric test, and it is **the clearest
Hypothesis-A result in the repository — because it was designed to be.**

`HYP-2026-026.json` → `confidence_rationale`: *"The operator accounting is a CFT theorem, not a fit:
a two-point function C(r) ~ r^{−2Δ_σ} of the spin field carries Δ_σ = 1/8 (Ising), so any distance
functional of C alone is controlled by Δ_σ … These are different numbers by construction, so the
distance-cannot-be-the-force conclusion is strongly motivated a priori."*

That is a full concession under §6: the answer was known before the run. `SIM-2026-031.json` then
measures `kappa_loglog_chord = 0.24289` against the CFT value 2Δ_σ = 0.25 (a 2.8 % validation), and
the "dichotomy gate" was 0.25 versus 4 — a factor-16 window that no correct implementation could
fail.

Two record defects, **NEW**:
1. **A pre-registered sub-claim was falsified and the status stayed SUPPORTED.** The registered claim
   (`HYP-2026-026.json` → `claim`, item (i)) is *"d(r) = sqrt(−2 eps² ln|C(r)|) versus r is
   well-described by d(r) proportional to r (linear …)"*. `SIM-2026-031.json` →
   `results.linear_subclaim_r2_synthetic = 0.7299` and `results.analytic_note`:
   *"d(r) = eps*sqrt(0.5*ln r) for C = r^−1/4 — sqrt-log, monotone but NOT linear."*
   The record documents the change honestly as a *"WORDING CORRECTION to the claim"*
   (`HYP-2026-026.json` → `result_note_2026_06_08_sim031`) — but the hypothesis status is
   `SUPPORTED` and the falsified linear prediction is simply removed. Under §36 the original entry
   must be preserved *and* the outcome scored against it.
2. The synthetic tier's power-law fit is `{"exponent": NaN, "prefactor": NaN, "r2": NaN}` — a literal
   `NaN`, invalid strict JSON, same class as ERRATA D2 but not listed there. (Phase-1 `inv-sims-mid.md`
   item 10 also caught this; I confirm.)

**§34:** the Synge distance is a deterministic functional of a boundary two-point function. It is
invariant across representations, recoverable from boundary observables, independent of architecture,
gauge and bond dimension. It is a **state property with a value fixed by Δ_σ = 1/8**. Calling it
"emergent distance" is a relabelling of ln|C(r)|. HYP-026 is, correctly read, **evidence for
Hypothesis A**: the project asked whether its distance object carried independent dynamical content
and proved that it cannot.

### 3.6 G6 — CMI thread density, HYP-012 and SIM-2026-016

`cmi_crofton_test.py:5–8` and `sim2026024_pee_crofton.py:50–55` both begin by loading
`gs_24q_exact.npy` — **the exactly diagonalized ground state.** Every "kinematic space" object in the
project (the K[u,v] = ∂²S/∂u∂v matrix, the PEE thread density, the σ(dr) profile) is built from
**von Neumann entropies of intervals of a boundary state obtained without any tensor network.** The
"bulk" is a coordinate change on boundary entanglement data. Nothing about the representation enters,
so nothing about the representation can come out.

The result (`SIM-2026-016.json`):
- `verdict: "NOT_SUPPORTED"`.
- `alpha_predicted: −0.3848` vs `alpha_measured: 3.92` — wrong sign.
- `F_pred` **increases** monotonically with dr (0.341 → 0.871) while `F_measured` **decreases** by
  three decades (−2.352 → −0.00222). The predicted and measured profiles run in opposite directions.
- `HYP-2026-012.json` → `refutation_criteria` set the bar at *"systematically off … by more than a
  factor of 2"*. The failure is a factor of ~400 in shape plus a sign inversion.
- **Record defect:** `HYP-2026-012.json` → `status: "proposed"`, `last_updated: "2026-03-26"`. The
  hypothesis its own simulation refuted is still stored as untested. (Consistent with
  `inv-hypotheses.md`'s finding of seven such records; I confirm 012 specifically.)

### 3.7 G7 — Crofton / integral geometry, HYP-014 and HYP-022 — **both REFUTED**

**HYP-014 (`SIM-2026-018.json`).** `verdict: "REFUTED"`, `confidence: "high"`.
`crofton_max_residual_pct: 5863.0`, `crofton_mean_residual_pct: 2393.5`. The hypothesis had been
elevated to `medium` confidence on the strength of an amplitude ratio (7.78 measured vs 7.66
predicted, 1.6 %); the record's own `key_finding` reads: *"Amplitude ratio … is a coincidence … the
intermediate points are wildly wrong."* The measured profile is
`sigma ~ dr^(−0.87)`, `chi2_per_dof: 0.0184` — an ordinary power-law decay of conditional mutual
information in a critical chain, with no sinusoidal (Crofton) structure whatsoever.
This is the project's own recorded instance of the lesson *"exponent match ≠ mechanism."*

**HYP-022, the salvage (`SIM-2026-024.json`).** `verdict: "REFUTED"`,
`verdict_reason: "alpha=0.883 outside acceptance window [3.2, 4.8]. PEE-thread re-weighting does not
recover the known alpha~4."`

The decisive detail: **the "correct" Kirillov–Kostant measure barely moved the answer.**
SIM-018's unweighted σ exponent was 0.8723 (`power_law_fit.alpha_sigma`); after re-weighting every
interval by the hyperbolic Crofton kernel 1/sin²(θ/2), SIM-024 gets 0.8830. A change of **1.2 %**.
The integral-geometry measure — the entire alleged geometric content — is numerically a no-op. The
profile is set by the entanglement decay of the boundary state and by nothing else.

**NEW — two of the three mandatory guards are structurally incapable of failing.**
`HYP-2026-022.json` → `feasibility_notes` made three guards mandatory *"before any 'salvaged'
verdict"*, on the explicit ground that *"the 1/sin²(θ/2) divergence at θ→0 is exactly the
discretization step where HYP-014 lost the physics."* In `SIM-2026-024.json`:
- `guards.G1_alpha_range: 0.0` — α is **bit-identical (0.8830410748467233) at all 20 sweep points**
  across `alpha_vs_cutoff_table`.
- `pv_vs_hardcutoff.delta_alpha: 0.0`, and `F_pee_hard` and `F_pee_pv` are identical arrays to all
  printed digits.

The reason is visible in the code: `sim2026024_pee_crofton.py:157–158` computes
`theta = 2.0*np.pi*(v-u)/nq` and clamps `theta_eff = max(theta, theta_min)`. The summation loop
(lines 179–190) runs over `u <= i`, `v >= j = i+dr`, so `v−u >= dr`. For the fit window dr ≥ 2 the
smallest angle on the lattice is 2·2π/24 = 0.5236, which equals the **largest** θ_min in the sweep
(`4π/N`). **The regulator never binds.** G1 ("regulator stability over two decades") and G3
("PV vs hard cutoff agree") therefore test a code path that is never taken. The verdict here was
REFUTED anyway, so nothing was mis-credited — but had the number landed in [3.2, 4.8], the salvage
would have been declared SUPPORTED on the strength of two guards that cannot fail. The one guard with
real content, G2 (Néel null control, `alpha_fit: −6.2e−15`), did work.

### 3.8 G8 — l_AdS itself: the master representation constant

Every geometric claim in the project multiplies by 1/ln 2. The project holds **at least three
mutually inconsistent values and two mutually inconsistent definitions**:

| value | source | definition |
|---|---|---|
| 1.4426950408889634 | `paper-prd.tex:64`; `SIM-2026-001.json` → `results.analytical.l_AdS` | 1/ln **χ** (bond dimension) |
| 1.4426950408889634 | `composite_geodesic_test.py:53–56` | 1/ln **K** (blocking ratio, "sites per MERA block") |
| 1.233 | `composite_geodesic_results.json` → `inputs.l_AdS_fitted` | fitted ξ from SIM-2026-002 |
| 1.432394487827058 | same file → `calculations.composite_geodesic.l_AdS_needed_to_match_exact` | back-solved from T = 2.25 |

The two definitions coincide only for the binary χ=2 network. They diverge immediately elsewhere, and
the project runs elsewhere:

| network actually used | 1/ln χ | 1/ln K | ratio |
|---|---|---|---|
| binary χ=2 (force, transport, paper §3–4) | 1.4427 | 1.4427 | 1.00 |
| binary χ=3 (`SIM-2026-015d`, paper's 4th result) | **0.9102** | 1.4427 | 1.59 |
| ternary χ=6 TCI (`SIM-2026-051`, "3-site / ternary blocking") | **0.5581** | **0.9102** | 1.63 |
| ternary χ=12 Potts (`SIM-2026-063`) | **0.4024** | 0.9102 | 2.26 |

**Under the manuscript's own Eq. (2), the "emergent AdS radius" of the same critical Ising state
takes the values 1.4427 (χ=2) and 0.9102 (χ=3) — a 37 % difference produced by nothing but a change
of ansatz.** The transport prediction (π/2)·l_AdS moves from 2.266 to 1.430; the measurement 2.239
goes from −1.2 % agreement to +57 % disagreement. And the same project reports the χ=3 network as the
*better* representation (0.15 % energy error vs 1.87 % at χ=2, `SIM-2026-015d.json` vs
`SIM-2026-002.json` → `vqe.pct_error`).

This is the §34 test administered by the project's own data and failed cleanly: **a quantity that
changes by 37 % when you improve the representation of the identical state is a property of the
representation.** RESEARCH-DIRECTOR §34 is explicit that such a quantity *"may still be
computationally useful, but it should not automatically be treated as physical geometry."*

**NEW — the citation that supplies l_AdS = 1/ln χ has no record in the project's own catalogue.**
`references.bib:21–29` gives `KimSwingle2017`, arXiv:1701.00050. I grepped all 139 records in
`research/data/papers/`: **no file contains `1701.00050`.** By contrast the two other geometric
sources are catalogued (Bohra & Sivaramakrishnan 2511.22168 → `PAPER-2026-020`; Ansel 2405.02380 →
`PAPER-2026-110`). The single most load-bearing geometric input in the program has never passed the
project's own literature-cataloguing discipline, so its convention (χ vs K, and the metric
normalization it presumes) has never been checked against the source.

### 3.9 G9 — bulk geodesic distance d_geo: two incompatible definitions in the same program

- `worldline_mc_results.json` → `force_profile.r_geod_vals`: **d_geo = dr · l_AdS** (linear).
- `paper-prd.tex:257` and `:529`: **d_geo = 2·l_AdS·ln(dr)** (logarithmic), attributed to
  KimSwingle2017.

These are not two approximations of one thing; they predict different physics. Under the linear map,
a bulk propagator G ~ exp(−m·d_geo) gives an **exponential** force in dr — the Sahay–Lukin–Cotler
form the paper is arguing against. Under the logarithmic map the same propagator gives
`dr^(−2 m l_AdS)` — a **power law** (the paper spells this out at line 529). The project uses the
linear map when comparing to worldline Monte Carlo (§5 of the paper, the m_eff result) and the
logarithmic map when explaining why the force is a power law (§9 of the paper), **in the same
manuscript**, without noting that they are inconsistent.

A framework in which the central geometric quantity — distance — has two mutually exclusive
definitions selected per-argument is not making predictions. It is providing post-hoc descriptions.
That is §33's question answered empirically: the geometry, as currently specified, does not fix a
distance.

---

## 4. §34 applied: state properties vs representation properties

Legend: **Inv** invariant across representations of the same state · **MERA** specific to MERA
architecture · **Gauge** gauge-dependent · **Opt** depends on optimization history · **χ** depends on
bond dimension · **Bdy** recoverable from boundary observables alone.

| Quantity | Inv | MERA | Gauge | Opt | χ | Bdy | Classification |
|---|---|---|---|---|---|---|---|
| G1 α ≈ 4 | **yes** (ED 3.975 = MERA 4.071) | no | no | no | no (χ=3 vs exact, 2.4 %) | **yes** (energies of a spin chain) | **state property**, fixed by BPZ fusion rules |
| G2 worldline framing | n/a | n/a | n/a | n/a | n/a | n/a | **not an observable** — nomenclature |
| G3 T = (π/2)l_AdS: measured side | yes | no | no | no | no | **yes** (⟨Y_j⟩(t) on a chain) | state/Hamiltonian property |
| G3 predicted side (l_AdS) | **no** | **yes** | n/a | no (declared "not by optimization") | **yes** (1.4427 → 0.9102) | **no** | **pure representation property** |
| G4 m_eff | no (contains l_AdS twice) | yes | no | partly (ξ from a 2-point fit) | yes | partly | **algebraically dependent on G8** |
| G5 Synge d(r) | **yes** | no | no | no | no | **yes** (a functional of C(r)) | **state property**, = 2Δ_σ |
| G6 CMI σ(dr) | **yes** | no | no | no | no | **yes** (interval entropies of ED state) | **state property**, REFUTED as a force proxy |
| G7 Crofton integrals | **yes** | no | no | no | no | **yes** (same K[u,v]) | **state property**, REFUTED twice |
| G8 l_AdS | **no** | **yes** | n/a | no | **yes** | **no** | **pure representation property** |
| G9 d_geo | **no** — two definitions | **yes** | n/a | no | **yes** | **no** | **ill-defined** |

**Read the table as a whole and the argument is finished.** The column that matters is the last one.
Every quantity that is *measured* is in the "state property, recoverable from the boundary" row —
and is therefore identical for any faithful representation, geometric or not. Every quantity that is
*specific to the network* (l_AdS, d_geo) is **never measured**; it is asserted from the architecture
and then multiplied into a comparison. **There is no entry in this table that is both
representation-sensitive and empirically determined.** That is precisely the situation
Hypothesis A predicts.

**What is conspicuously absent.** I grepped the entire `research/` tree for rewiring experiments
(`grep -ril "rewir"`): **zero hits** — no §11-H network-rewiring test has ever been run. I grepped
`research/data/` and `research/tools/merakit-setup/` for gauge-invariance tests: no simulation record
addresses whether any geometric diagnostic survives a tensor-network gauge transformation. The only
matched-control script in the repository is `hyp024_gapmatched_control.py`, and HYP-024 is
`NOT_ESTABLISHED (artifact)`. **The project has therefore never performed a single experiment capable
of distinguishing Hypothesis A from Hypothesis B**, which is why the audit's answer at this date can
only be "A is unrefuted."

---

## 5. §33: is the geometry question even well-posed?

Not yet, and the project's records show why concretely.

**5.1 What would count as "the geometry"?** Three candidate objects appear in the repo, and they are
not equivalent:
- (a) the **graph metric** of the network (layer index ↔ radial coordinate, causal cone ↔ light cone);
- (b) the **entanglement metric** built from boundary entropies (the K[u,v] kinematic space of
  `sim2026016_kinematic_space.py`);
- (c) a **correlator metric** (the Synge world function of `SIM-2026-031.json`).

(b) and (c) are computed from the boundary state alone and exist for *any* state, including states
with no efficient network — they are not tensor-network objects at all. Only (a) is a property of the
representation, and it is exactly the one the project never measures.

**5.2 What equivalence relation should identify two geometries?** The project has no answer on file.
A defensible minimum would be: *two networks have the same geometry iff their graph metrics agree up
to isometry after quotienting by (i) tensor-network gauge transformations on internal legs,
(ii) trivial insertions of identity isometries, and (iii) an overall length unit.* Note what
condition (iii) alone does: it **quotients away l_AdS entirely**, since 1/ln χ is a pure scale. Under
that equivalence relation, every claim in §3.3, §3.4 and §3.8 becomes vacuous — they are all
statements about the unit. Any equivalence relation weak enough to make l_AdS meaningful must
declare the χ=2 and χ=3 MERAs of the same state to be *different geometries*, which is Hypothesis A
stated in geometric language.

**5.3 Can different networks represent the same state with incompatible internal geometries?** The
project has already demonstrated a weak version of yes, twice, without noticing:
- **Same state, different l_AdS**: χ=2 → 1.4427 and χ=3 → 0.9102 for critical Ising
  (`paper-prd.tex:64` + `SIM-2026-015d.json`), a 37 % difference with 12× better energy accuracy at
  χ=3.
- **Same universality class, different blocking**: binary blocking for Ising, ternary (3-site)
  blocking for TCI and Potts (`SIM-2026-051.json` — "ternary", "3-site blocking"), giving
  l_AdS ∈ {1.4427, 0.9102} under the K-convention. Yet the *measured* quantity, α = 4, is identical
  across all of them (`SIM-2026-051` Δ_T = 2.007; `SIM-2026-063` Δ_T = 2.001). **The observable is
  blind to the blocking; only the unmeasured "radius" tracks it.** That is a direct, internal
  demonstration that the geometric parameter and the physics are decoupled.

**5.4 Is approximate bulk locality sufficient?** Untested here — no reconstruction, entanglement-wedge
or modular-flow experiment exists in the repository (§11-A/B/C, all unattempted). So the question
cannot be answered from present evidence either way.

**5.5 Verdict on well-posedness.** The distinction is *in principle* well-posed — §9 below gives an
operational form of it — but it is **not currently well-posed inside this project**, because the
project has (i) no fixed definition of bulk distance (§3.9), (ii) no equivalence relation, (iii) two
conflicting definitions of l_AdS (§3.8), and (iv) no observable that depends on the network's
internal organization. RESEARCH-DIRECTOR §33's closing line applies exactly: *"This work may reveal
that the program needs a sharper definition before it needs a larger simulation."*

---

## 6. The pattern in HYP-012 / HYP-014 / HYP-022 / HYP-026

**Yes, there is a pattern, and it supports Hypothesis A.** Four attempts to build a geometric object
that predicts something:

| HYP | Object | Outcome | Residual / reason |
|---|---|---|---|
| 012 | CMI thread density → force | **NOT_SUPPORTED** (`SIM-2026-016`) | predicted profile rises where measured falls; α_pred = −0.385 vs 3.92 |
| 014 | Crofton, uniform chord measure | **REFUTED** (`SIM-2026-018`) | 5863 % max residual; the 1.6 % amplitude-ratio "agreement" was coincidence |
| 022 | Crofton, Kirillov–Kostant measure | **REFUTED** (`SIM-2026-024`) | α = 0.883 vs required [3.2, 4.8]; the "correct" measure changed α by 1.2 % |
| 026 | Synge world function | "SUPPORTED" but **force-blind** (`SIM-2026-031`) | κ = 0.243 ≈ 2Δ_σ = 0.25, not 4 — the distance carries Δ_σ, the force carries Δ_T |

The pattern is sharper than "geometry keeps failing." It is:

> **Every attempt to make a bulk-geometric object do dynamical work has failed, and the one that
> succeeded, succeeded by proving that it cannot.**

HYP-026 is the key. Its own confidence rationale states the reason in advance: a functional of a
single two-point function is controlled by that operator's dimension, full stop
(`HYP-2026-026.json` → `confidence_rationale`). Generalize it and the selection rule is not
about geometry at all — it is the ordinary CFT statement that **an observable built from operator O
carries Δ_O and nothing else.** HYP-012's CMI, HYP-014's and HYP-022's Crofton integrals, and
HYP-026's Synge distance are all functionals of boundary entropies or two-point functions of light
operators; the force is a stress-tensor quantity. No amount of geometric re-weighting moves an object
between conformal families, which is exactly why the Kirillov–Kostant kernel changed α from 0.872 to
0.883 and why the naive one changed nothing either.

Under Hypothesis B one would expect at least one of these four to have worked, because under B the
bulk geometry is an *additional* structure that can relate different boundary sectors. Under
Hypothesis A the outcome is forced: geometric re-parameterizations of boundary data are
measure-preserving relabellings, so they cannot generate an exponent that the underlying operator
does not have. **Four for four, the data went the way A predicts.**

The project's own philosophy note gets to the same edge and stops one step short. It reads the
pattern as *"the emergent 'spacetime' is a STACK of operator-resolved structures rather than a single
manifold-with-metric"* (`HYP-2026-026.json` → `philosophical_implications`). But "a stack of
operator-resolved structures, one per conformal family, each carrying its own Δ" **is the CFT
operator content.** Naming it a stack of geometries adds no constraint that the operator content did
not already impose. That is Hypothesis A restated with more nouns.

---

## 7. Independence: the four flagship results are one result and a constant

Applying §7 to the whole geometric program at once:

- **Shared exact CFT identity:** Δ_T = 2 (G1, and the universality claims at TCI and Potts).
- **Shared exact CFT identity:** Δ_ε = 1 (G4).
- **Shared exact CFT identity:** Δ_σ = 1/8 (G5).
- **Shared architecture constant:** l_AdS = 1/ln 2 appears in **G3 (once), G4 (twice, both sides),
  G8 (definitionally), G9 (both variants)**, and as `L_ADS = 1.0/np.log(2)` even in
  `cmi_crofton_test.py:44` where it is the file's only occurrence of the symbol — defined, never used.
- **Shared state:** `gs_24q_exact.npy` is the input to G1 (24q), G6 and G7. The three are not
  independent tests; they are three functionals of one eigenvector.
- **Shared single data point:** dr = 2 dominates the α fit in all three "consistent evaluations"
  (§3.1).

§7 classification of the geometric program: **structurally dependent**, tending to **algebraically
equivalent** in the m_eff case. Per §7's closing rule — *"A beautiful agreement is not strong evidence
if both sides are transformations of the same input"* — the accumulation of four sub-percent
agreements is not four pieces of evidence. It is one exact CFT input, one architecture constant, and
one eigenvector, re-presented.

---

## 8. Where my own case is weakest (steelmanning Hypothesis B)

Honesty requires this section, and §19 requires that a control be capable of defeating the preferred
interpretation. Four things a competent Hypothesis-B advocate can say, and my answer:

**8.1 "Absence of a discriminating experiment is not evidence for A."** Correct, and it is the
strongest objection. Everything in §3–§7 shows the project has *not established* B; it does not by
itself establish A. My claim is calibrated accordingly: **A is unrefuted and is the parsimonious
reading of the present record**, not "A is proven." A no-go proof would require §16-style work that
has not been done. I explicitly do **not** claim "no geometric content exists in MERA"; I claim "no
measured quantity in this repository has geometric content that survives §34."

**8.2 "MERA's causal cone is a real, non-trivial structural fact."** Also correct. The MERA's
logarithmic depth and light-cone structure genuinely constrain which states it can represent, and
that is not nothing. But "the ansatz has a causal structure" is a statement about the *variational
class*, not about the represented state, and the project has never measured a state observable that
detects it. Note that under Hypothesis A this structural fact is exactly what one expects: a
hierarchical representation with a causal cone is an efficient scheme, and efficiency is A's whole
content.

**8.3 "The transport result would be remarkable if it were N-independent."** It would. If T were
genuinely fixed at (π/2)·l_AdS across N = 12, 16, 24, 32 that would be hard to explain as a
finite-size timescale. The evidence runs the other way — `paper-prd.tex:195` records −31.6 % at
N = 24 and rescues it with an empirical T·L ≈ const, i.e. **T ∝ 1/L**, which is what a finite-size
crossing time does and what a fixed geodesic length does not. But the N = 24 point is on the coarse
grid and is flagged unreliable (double-lobe, ERRATA E2), so this line of evidence is weaker than it
looks in both directions. **A clean N-scaling study is the single most valuable cheap experiment the
project could run**, and it is a fair test of my position.

**8.4 "α = 4 recurring at three universality classes is impressive."** It is technically impressive
and it is Level-1 by the manuscript's own reasoning (`paper-prd.tex:427`; `SIM-2026-051.json` →
`verdict`: *"This is exactly the CFT prediction: Delta_T=2 in every unitary 2D CFT … so alpha=2*Delta_T=4
must hold at any 2D critical point. The numerics confirm the symmetry argument."*). Impressive
execution of a guaranteed calculation is a **methods** contribution (§5 Level 2), which is real and
which I am not disputing. It is not evidence about geometry.

**What would change my mind, stated plainly.** Any one of:
- a quantity that differs between two representations of the *same* state at matched boundary
  accuracy, and that is not a pure unit;
- a geometric prediction locked before measurement that survives a change of χ, of blocking ratio, or
  of gauge;
- a reconstruction/locality result that a non-geometric ansatz matched on ordinary CFT data fails to
  reproduce.

§9 is the cheapest experiment that could deliver the first two at once.

---

## 9. The sharpest experiment: **the matched-ansatz rewiring test**

Designed per §10, §19, §28, §36, with failure criteria fixed **before** it is run and with the
outcome that refutes *me* named first.

### 9.1 Question

> Does any measurable quantity in this project distinguish a MERA from a non-geometric ansatz
> matched on ordinary CFT data, at fixed representation accuracy?

### 9.2 Constructions (all at N = 16 critical TFIM, all local CPU)

| arm | construction | geometric organization |
|---|---|---|
| **M2** | binary MERA, χ = 2 (existing, `SIM-2026-002` lineage) | canonical, l_AdS = 1/ln 2 |
| **M3** | binary MERA, χ = 3 (existing, `SIM-2026-015d`) | canonical, l_AdS = 1/ln 3 under Eq. (2) |
| **T3** | **ternary** MERA, matched energy error to M3 | different blocking ⇒ different l_AdS |
| **R** | **rewired** network: M3's tensors on a scrambled connectivity (random permutation of which pairs each layer acts on), re-optimized to the same energy tolerance | causal cone destroyed |
| **P** | **MPS/puMPS** at bond dimension chosen to match M3's energy error (the project already has `research/tools/pumps-setup/`) | no bulk at all |
| **G** | M3 with a random **gauge transformation** inserted on every internal bond (X → XV, V⁻¹Y on the contracted leg) | identical state, different tensors |

**Matching requirements (§10).** All arms must agree to within stated tolerances on:
ground-state energy (target: all within 0.20 % of E₀ = −20.0164), half-chain entanglement entropy
(within 2 %), C(r) = ⟨ZZ⟩_c for r = 1…8 (within 3 % pointwise), and Δ_σ, Δ_ε where extractable
(within 5 %). Arms that cannot be matched are excluded and the exclusion is recorded; an arm may not
be dropped after its observable is computed.

### 9.3 Observables

- **O1 — α:** the force exponent, computed by the identical `exact_gs_force_profile_24q.py` code path
  on each arm's state, reported with a **log-space** fit over dr = 2…11 *and* the sliding-window
  local-slope table of §3.1. (Fixing the fit method is part of the pre-registration; the linear-space
  fit is not permitted.)
- **O2 — transport T:** identical Wang–He pulse protocol at dt = 10⁻³, N = 12, 16, and if feasible 20,
  applied to each arm's state, reported as T and as T·L.
- **O3 — Synge κ:** the `SIM-2026-031` pipeline on each arm's C(r).
- **O4 — l_AdS-as-predicted:** the arm's own architecture constant under **both** conventions
  (1/ln χ and 1/ln K), recorded but **not** used to normalize anything.

### 9.4 Pre-registered predictions

| | Hypothesis A predicts | Hypothesis B predicts |
|---|---|---|
| O1 across M2/M3/T3/R/P/G | **all equal within 5 %** (it is a state property) | **R and P differ measurably** from M2/M3/T3 |
| O2 across arms at fixed N | **all equal within the dt resolution**; and **T ∝ 1/L** across N | **T tracks the arm's own l_AdS**, i.e. M3/T3 differ from M2 by ~37–59 %; T is **N-independent** |
| O3 across arms | **all = 0.25 ± 0.02** | some arm departs from 2Δ_σ |
| G (gauge) vs M3 on all of O1–O3 | **bit-level identical** | if anything changes, the diagnostic was gauge-dependent and is disqualified either way |

### 9.5 Failure criteria — **what refutes me**

I am refuted, and Hypothesis B is supported, if **any** of the following holds:

- **F1 (architecture-tracking).** O2 measured on M3 or T3 lands within 5 % of that arm's own
  (π/2)·l_AdS (1.430 for χ=3, 0.877 for ternary χ=6) while M2 lands within 5 % of 2.266 — i.e. the
  transport time tracks the network's blocking/bond dimension rather than the state. This is the
  cleanest possible B signal and it is a *cheap* measurement.
- **F2 (rewiring separation).** O1 on arm **R** differs from O1 on **M3** by more than 5×
  the log-space fit uncertainty, while R and M3 are matched to the stated tolerances on energy, S,
  C(r) and Δ. That is §11-H's "ordinary CFT accuracy preserved, geometric diagnostic collapsed" — but
  read in the direction that helps B: a geometric diagnostic that *responds* to connectivity.
- **F3 (ansatz separation).** O1 or O3 on the non-geometric arm **P** differs from M3 by more than
  5 % while P matches M3 on all four ordinary-CFT matching criteria.
- **F4 (N-independence).** O2 is constant in N to within 3 % across N = 12, 16, 20 — i.e. the
  T·L ≈ const observation of `paper-prd.tex:195` is wrong and T really is a fixed geodesic length.

### 9.6 What confirms me (and is the more likely outcome)

- O1 identical across all six arms including the rewired and MPS arms → **α is a state property**, and
  the force result is formally severed from geometry.
- O2 identical across arms at fixed N and scaling as 1/L → **transport is a finite-size boundary
  timescale**, and the 1.2 % agreement is a coincidence of the Wang–He normalization with 1/(2 ln 2).
- O3 = 0.25 everywhere → **Synge distance is Δ_σ**, confirming HYP-026 in the stronger, general form.
- G bit-identical to M3 → all diagnostics are gauge-blind because none of them look at the network.

If that is the outcome, the project should write it up as the §16 no-go result the North Star
paragraph explicitly names as being of **equal scientific value**:
*"After controlling for shared CFT inputs and representation dependence, every proposed geometric
observable reduced to known boundary data or changed under nonphysical network choices."*

### 9.7 Why this experiment and not a bigger one

§40: choose the smallest experiment that most changes the project's decisions. Every ingredient
already exists on disk — the χ=2 and χ=3 MERA states, the force script, the transport script, the
Synge script, the puMPS toolchain in `research/tools/pumps-setup/`. The only new code is the rewiring
permutation, the gauge insertion, and a matched-accuracy optimizer loop. Cost is local CPU and a few
days. And the decision it changes is the largest one available: whether Track B (§9 of the standard,
geometry discrimination) is worth funding at all, or whether the program should consolidate on the
non-Hermitian methods track where its genuinely unconstrained result lives.

**Order of execution, cheapest first:** F1 (transport on the existing χ=3 state — one script, hours) →
F4 (N-scaling at fine dt, N=12/16 already exist in `SIM-2026-025`) → G (gauge, trivial) →
F2/F3 (rewiring and MPS arms, needs the matched optimizer).

---

## 10. UNVERIFIED

Stated explicitly per the output protocol. Silence is not a pass.

1. **Kim & Swingle's actual claim.** I could not verify from repository evidence whether
   arXiv:1701.00050 states l_AdS = 1/ln χ (bond dimension) or 1/ln K (blocking ratio), or under what
   metric normalization. No catalogued record exists (§3.8). The bibliography entry
   `references.bib:22` gives the author as "Kim, Chris H."; phase-1 `inv-manuscript-claims.md` reports
   four bibliography entries with contradicted given names, and I did not independently confirm this
   one. **My χ=3 → 0.9102 argument is watertight under the manuscript's own Eq. (2) regardless of what
   the source says**, but if the source's convention is the blocking ratio, the χ-dependence argument
   weakens to a blocking-ratio argument (binary vs ternary, 1.4427 vs 0.9102, still a 59 % effect).
2. **Whether the Wang–He L/(4π) prefactor is exactly the CFT normalization.** I read it from
   `holographic_transport_16q.py:132` and inferred its purpose. I did not verify against Wang & He
   arXiv:2501.03084 that this normalization makes the light-crossing time exactly π. My §3.3 claim
   that "the entire content is one unit conversion" depends on this; if the normalization is
   different, the conversion factor is different but the argument's structure is unchanged.
3. **The half-chain entropy discrepancy (1.2895 Wang–He vs 0.7501 critical TFIM).** I noted it from
   `hyp010_criticality_scan.json` → `S_half` fields but did not diagnose it. It could indicate the two
   chains realize different boundary conditions, different sectors, or different CFTs; I only claim
   that it means the control is **not matched on ordinary entanglement data**, which is enough for
   §19.
4. **The two-channel fit's interpretation.** I showed a Z₂-odd admixture (β/α = −0.041) exists in the
   probe and that a T+ε two-channel model does not fit better than a single power law. I did **not**
   determine what does explain the local-slope drift 4.23 → 2.46 → 4.06. It could be finite-size image
   effects from the open boundary (probe reaches site 18 of 24), lattice corrections at short dr, or
   something else. I claim only that no clean power law describes the data, not that I know why.
5. **Whether the χ=3 MERA state file still exists** to run §9 arm M3 directly. `SIM-2026-015d.json`
   records the results but `.gitignore:19` excludes `*.npy` (per `inv-sims-early.md` §5), so the state
   may need regeneration. This affects the cost estimate in §9.7, not the design.
6. **Gauge-transformation behaviour.** I asserted in §4 that all measured diagnostics are gauge-blind
   because none of them read the network. That follows from the code paths I read (all compute
   boundary expectation values from a statevector), but I did not run arm G. It is a prediction, and
   §9.5's clause makes it falsifiable.
7. **The empty-theory-tier premise.** The task brief and RESEARCH-DIRECTOR §14 state
   `research/data/theory/` is empty. **It is not** — it contains 7 files including
   `epsilon-channel-proof.md`, which is the analytic backbone of §3.1. I did not audit the other six
   (`RUN-A-methods.md`, `paper-review-synthesis.md`, `research-challenge.md`, `research-practical.md`,
   `research-primary.md`, `task4-ope-argument.md`) beyond noting that `epsilon-channel-proof.md:10–14`
   states `task4-ope-argument.md` contains an incorrect assumption (C_εεε = 1/2). Full audit of the
   theory tier is `inv-infrastructure`'s lane.

---

## 11. Reproduction

Every number I computed is regenerated by this script (Python 3, numpy + scipy); the input array is
copied verbatim from `research/data/simulations/SIM-2026-011-interaction.json` →
`F_interaction_avg` (top-level key; the same array is duplicated at
`F_interaction_probe_only` and at `force_profile.F_interaction`).

```python
import numpy as np
from scipy.optimize import curve_fit

F = {1:-2.351692205770835, 2:-0.5736905904286083, 3:-0.10316809917935998,
     4:-0.04878358875105704, 5:-0.028200650592275167, 6:-0.018005777922400767,
     7:-0.012184604917560904, 8:-0.008543928753709906, 9:-0.006114281901496099,
     10:-0.004409850656966086, 11:-0.0031643852148341978, 12:-0.0022218714808168727}
dr = np.array(sorted(F), float); y = np.abs([F[int(d)] for d in dr])

pl = lambda x, A, a: A * x**(-a)

# 1. reproduce the record's fit exactly (linear-space, unweighted)
p, c = curve_fit(pl, dr[dr>=2], y[dr>=2], p0=[8, 4])
# -> A = 8.6727, alpha = 3.9218 +- 0.1590   == SIM-2026-011-interaction.json
#    fits.F_avg_dr_ge2.power_law {A: -8.672711550, alpha: 3.921759726, dalpha: 0.158982157}

# 2. drop dr = 2
p3, _ = curve_fit(pl, dr[dr>=3], y[dr>=3], p0=[8, 4])   # -> alpha = 2.5593 +- 0.0187
p4, _ = curve_fit(pl, dr[dr>=4], y[dr>=4], p0=[8, 4])   # -> alpha = 2.5340 +- 0.0377

# 3. statistically appropriate log-space fit, same window
A = np.vstack([np.log(dr[dr>=2]), np.ones((dr>=2).sum())]).T
coef, *_ = np.linalg.lstsq(A, np.log(y[dr>=2]), rcond=None)   # -> alpha = 2.8897

# 4. local log-slopes -> 2.04, 4.23, 2.60, 2.46, 2.46, 2.53, 2.66, 2.84, 3.10, 3.48, 4.06
slopes = -np.diff(np.log(y)) / np.diff(np.log(dr))

# 5. two-channel A*dr^-4 + B*dr^-2, log space -> max|rel residual| 30.5 %
#    vs single power law 29.4 %  (no improvement)
```

Repeat items 1–2 on `SIM-2026-015d.json` → `exact.V_data` and `mera.V_data`:
- 16q exact: dr≥2 → **3.9748 ± 0.1451** (matches `exact.alpha`, `exact.dalpha`); dr≥3 → **2.7530**.
- 16q χ=3 MERA: dr≥2 → **4.0685 ± 0.2039** (record: `mera.alpha` 4.0712 ± 0.1778 with
  `fit_n_pts: 10`, i.e. dr = 2…11 including the two **sign-flipped** points
  `mera.V_data["9"] = +0.0012` and `["10"] = +0.00037`, which the record's signed fit retains and I
  excluded — n = 8); dr≥3 → **2.6500**. That the χ=3 MERA force changes sign at dr = 9, 10 is itself
  a caution: the MERA arm of the "three consistent evaluations" has no usable signal past dr ≈ 8.

Other verifications, by direct file inspection:
- `grep -n "Skipping full MERA" research/data/simulations/holographic_transport_16q.py` → line 347.
- `grep -ci mera research/data/simulations/holographic_transport_24q.py` → 2 (both comments).
- `grep -rl "1701.00050" research/data/papers/` → no output.
- `grep -ril "rewir" research/` → no output.
- `1.4426950408889634 / 2.154 = 0.669777` → the record's `m_eff_from_MERA = 0.6698`.
- `2.23888 / np.pi = 0.712645` vs `1/(2*np.log(2)) = 0.721348` → −1.207 %, the ERRATA E2 residual.
- `1/np.log(3) = 0.910239`; `(np.pi/2)*0.910239 = 1.42975` vs measured 2.239 → **+56.6 %**.

---

## 12. Defects raised by this audit

Severity per the audit convention. **NEW** = not present in any phase-1 artifact
(checked by grep over `research/data/audit/raw/`).

| # | Sev | Where | What |
|---|---|---|---|
| GS-1 | **critical**, NEW | `research/data/simulations/holographic_transport_16q.py:347` (+ `_24q.py`, `_24q_v3.py`, `_finedt.py`) | The transport measurement never applies the MERA map — `"Skipping full MERA bulk computation"`. The tensors are built, unitarity-checked, and unused. The project's only dynamical geometry evidence has no tensor network in the computation. |
| GS-2 | **critical**, NEW | `paper-prd.tex:64` (Eq. 2) vs `SIM-2026-015d.json` → `chi: 3` | Under the manuscript's own `l_AdS = 1/ln χ`, its χ=3 result gives l_AdS = 0.9102 and a transport prediction of 1.430 vs the measured 2.239 (+57 %). The paper's fourth result falsifies its second under the paper's own equation. |
| GS-3 | **major**, NEW | `paper-prd.tex:195, 538, 605` vs `composite_geodesic_results.json` | The manuscript endorses two numerically incompatible predictions for the same quantity — Wang–He's analytic t_trans = π (3.1416) and its own (π/2)·l_AdS (2.2662) — and cites the first as confirmation of the second. Measurement 2.239 cannot agree with both. |
| GS-4 | **major**, NEW | `hyp010_criticality_scan.json` → `approach_B_tfim.results[g=1.00]`; `hyp010_criticality_scan.py:41–58` | The manuscript's only MERA-specificity control includes the **critical** TFIM (same Ising CFT), which misses the holographic prediction by +67.7 %, and the two arms are not normalization-matched (`n/(4*np.pi)` vs none) nor entropy-matched (S_half 1.2895 vs 0.7501). Not a matched control (§19); read straight it argues against CFT-universality of the observable. |
| GS-5 | **major**, NEW | `sim2026024_pee_crofton.py:156–190` vs `SIM-2026-024.json` → `guards` | Two of the three guards HYP-022 made mandatory are structurally incapable of failing: the lattice min angle 2π(v−u)/N ≥ 4π/N over the fit window equals the sweep's largest θ_min, so the regulator never binds. `G1_alpha_range: 0.0`, `delta_alpha: 0.0`, `F_pee_hard` ≡ `F_pee_pv`. Verdict was REFUTED anyway, so nothing was mis-credited — but a SUPPORTED verdict would have rested on vacuous guards. |
| GS-6 | **major** (confirms + extends phase-1) | `SIM-2026-011-interaction.json` → `fits.F_avg_dr_ge2.power_law`; `SIM-2026-015d.json` | The recorded α uses an unweighted **linear-space** fit over three decades, in which dr=2 carries ~99 % of the weight. Log-space over the same window gives 2.89. The local-slope table shows no plateau (2.04, 4.23, 2.60, 2.46, …, 3.48, 4.06). No record states the fitting method or reports a goodness-of-fit for the headline α. |
| GS-7 | **major**, NEW | `paper-prd.tex:257`/`:529` vs `worldline_mc_results.json` → `force_profile.r_geod_vals` | Two mutually incompatible bulk-distance definitions are used in the same manuscript: d_geo = dr·l_AdS (linear, worldline MC / m_eff argument) and d_geo = 2·l_AdS·ln dr (logarithmic, power-law argument). They predict exponential vs power-law force respectively. |
| GS-8 | **major**, NEW | `references.bib:21–29`; `research/data/papers/` | The citation supplying `l_AdS = 1/ln χ` (arXiv:1701.00050) has **no record** in the 139-record paper catalogue, unlike the project's other geometric sources. The most load-bearing geometric input has never passed the project's own literature discipline; χ-vs-K convention consequently unchecked. |
| GS-9 | **minor**, NEW | `HYP-2026-026.json` → `claim` (i) vs `SIM-2026-031.json` → `linear_subclaim_r2_synthetic: 0.7299`, `analytic_note` | A pre-registered sub-claim ("d(r) proportional to r, linear") was falsified; the record documents a *"WORDING CORRECTION to the claim"* and keeps `status: "SUPPORTED"`. §36 requires the original entry be preserved and scored, not amended. |
| GS-10 | **minor** (confirms phase-1) | `HYP-2026-012.json` → `status: "proposed"`, `last_updated: "2026-03-26"` | Still stored as untested although `SIM-2026-016.json` returned `NOT_SUPPORTED` with a sign-inverted prediction (α_pred = −0.385 vs 3.92). |
| GS-11 | **minor** | `research/` tree-wide (`grep -ril "rewir"` → empty; no gauge-invariance record) | No §11-H rewiring experiment, no gauge-invariance test, and no matched non-geometric control has ever been run. The project has therefore never executed an experiment capable of separating Hypothesis A from B. |
| GS-12 | **minor** | `research/data/theory/` | Contrary to RESEARCH-DIRECTOR §14 and the audit brief, the directory is **not empty** (7 files). `epsilon-channel-proof.md` is the analytic backbone of the α=4 claim and should be linked from `HYP-2026-008.json` and the manuscript; it currently is not. It also records that `task4-ope-argument.md` contains a wrong assumption (C_εεε = 1/2) — an internal correction never entered into ERRATA. |

---

## 13. One-paragraph summary for the record

Assuming Hypothesis A and testing it against the project's own files, the assumption survives
everywhere and is contradicted nowhere. The force exponent is a BPZ-1984 fusion-rule consequence
proved in this repository's own theory directory and measured on an exactly diagonalized chain with
no network; it is identical for exact and MERA states because it is a property of the state. The
transport result is a boundary-Hamiltonian light-crossing time compared against an architecture
constant, measured by a script that explicitly skips the MERA step, whose pre-registered arccosh test
was never run, whose factor-of-two was removed by choosing a different geodesic after seeing the
data, whose control fails at the critical point of its own universality class, and whose prediction
changes by 57 % under the same paper's own bond-dimension upgrade. The effective mass is
1/l_AdS versus l_AdS/ξ — the same constant twice. The Synge distance was proved force-blind by design.
Both Crofton routes are refuted, and the "correct" integral-geometry measure changed the exponent by
1.2 %. Not one measured quantity in the repository is both sensitive to the network's internal
organization and not recoverable from boundary observables. The project has never run a rewiring, a
gauge, or a matched-ansatz control. **The geometry, as currently operationalized, is a change of
vocabulary applied to boundary CFT data and one architecture constant.** §9 gives the cheapest
experiment that could prove me wrong, with its failure criteria fixed in advance; the transport arm
of it (F1) can be run in hours on states already on disk.
