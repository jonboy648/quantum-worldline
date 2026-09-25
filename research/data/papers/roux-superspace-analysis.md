# Roux (2026) Superspace Worldline — Deep Dive Analysis

**Paper:** "Superspace worldline formalism approach to Quantum Gravity: dimensional reduction and Holography"
**Author:** Jean-Baptiste Roux
**arXiv:** 2601.07382v1
**Registered as:** PAPER-2026-023
**Analysis date:** 2026-03-11
**Performed by:** Theory Lead (Tier 3)
**Status:** SPECULATIVE — all hypotheses below are clearly flagged as such

---

## 1. What the Paper Does

Roux establishes a structural equivalence between the **Hamiltonian formulation of Quantum Gravity in ADM superspace** and a **worldline (point-particle) formalism**. This is not a loose analogy — the paper shows the ADM Hamiltonian action is precisely the phase-space form of a point-particle action traversing the space of 3-metrics ("superspace"), with the DeWitt supermetric playing the role of the spacetime metric.

The chain of reduction the paper executes is:

```
4D Quantum Gravity (ADM Hamiltonian)
    -> Keldysh partition function on closed-time contour
    -> Euclidean 3D gravity
    -> Two Chern-Simons theories (A+, A- variables)
    -> WZW model on boundary
    -> Liouville theory (2D CFT, c=25, Q=2)
    -> Virtual graviton exchange between boundary probes ~ 1/|z_i - z_j|^4
```

This is the first time the ADM/worldline equivalence has been made precise at the level of the partition function.

---

## 2. Key Mathematical Results

### 2.1 The Worldline Identification (Eq. 34)

The point-particle worldline action in curved spacetime:

```
S[e, x, g] = int_0^1 dt [ (1/e) g_mu_nu x_dot^mu x_dot^nu + e(m^2 + lambda R) ]
```

is identified with the ADM Hamiltonian action by the dictionary:

| Worldline quantity | Superspace equivalent |
|---|---|
| Spacetime metric g_mu_nu | Superspace metric gamma_ij |
| Particle momentum p_mu | Canonical momentum pi^ij |
| Einbein e (gauge field on worldline) | Lapse function N |
| Particle mass squared m^2 | Local inertia -sqrt(gamma) R^(3) |
| Worldline proper time t | ADM coordinate time |

The configuration variable is the spatial triad E^a_i (or equivalently gamma_ij = eta_ab E^a_i E^b_j). The "particle" traverses superspace — the infinite-dimensional space of spatial 3-metrics modulo diffeomorphisms.

### 2.2 The DeWitt Supermetric (Eq. 11)

```
G_ijkl = (1 / 2 sqrt(gamma)) (gamma_ik gamma_jl + gamma_il gamma_jk - gamma_ij gamma_kl)
```

This is the kinetic metric on superspace. It plays the role of g_mu_nu for the worldline. It has Lorentzian signature on superspace (one timelike direction = overall conformal mode of the metric).

### 2.3 Keldysh Reduction to 3D (Eq. 55, 60)

The Keldysh partition function on a closed-time contour, after gluing N time-slices, reduces via the variable change:

```
A+ = Omega + sqrt(Lambda) * e
A- = Omega - sqrt(Lambda) * e
```

to two decoupled Chern-Simons theories with opposite signs. This is the known Witten decomposition of 3D gravity. The key point is that **the cosmological constant Lambda sets the CS level** and the minimum time step:

```
beta_m = sqrt(Lambda) * l_Pl * t_Pl
```

This is the **Roux quantization condition**: the ADM time interval is quantized in units of sqrt(1/Lambda) in Planck units.

### 2.4 WZW to Liouville (Eq. 72-83)

The CS boundary theory is a WZW model. Via Gauss decomposition of the H3+ group element, it reduces to a Liouville action:

```
S_Liouville = -(1/pi) int d^2 z [ sigma^mu_nu partial_mu phi partial_nu phi + 2 sqrt(sigma) R phi + (1/4) sqrt(sigma) e^(2 phi) ]
```

with background charge Q = 2 and central charge c = 25.

This is a 2D CFT living on the cosmological boundary. The boundary of superspace (= the cosmological boundary of the 3D manifold) carries a Liouville CFT.

### 2.5 Virtual Graviton Propagator (Eq. 84-86)

Massive probe particles at positions z_i couple to the Liouville field phi via:

```
A_z^(3)|boundary(z) = (2/rho) a_z^(3) sum_i alpha_i [ rho / (z - z_i) + boundary corrections ]
```

The two-point graviton exchange correlator between probes i and j is:

```
[<e^(alpha_i phi(z_i)) e^(alpha_j phi(z_j))>_Liouville]^2 ~ 1 / |z_i - z_j|^(4 Delta_ij)
```

For massless gravitons: alpha_i = 1, Delta_ij = 1, giving a **1/|z|^4 propagator** — the characteristic spin-2 graviton propagator in 2D CFT.

For general probes with conformal dimension Delta_i = alpha_i(Q - alpha_i) = alpha_i(2 - alpha_i):
- The force law is **1/|z|^(4 Delta)** between identical probes
- For Delta = 1 (graviton): force F ~ 1/r^5 (derivative of 1/r^4 potential)
- For Delta != 1 (matter/other): different power law

**Critical observation for our work:** This is a **power-law force**, not an exponential. This is different from the exponential V ~ exp(-dr/l_AdS) we measure from MERA. The distinction matters (see Section 4.1 below).

### 2.6 Entropy and Boundary Observables

The boundary entropy from the Liouville partition function:

```
-ln(Z_K) ≈ -(beta^2 / 16 pi) - O(Lambda)
```

This goes as beta^2, not the area law S ~ A/4G_N of bulk 3D gravity. Roux notes this is expected because we are inside a 3D hypersurface, not integrating over full 4D spacetime.

The boundary conditions at the cosmological boundary are **quantized**: the CS level k must be an integer for large gauge invariance, giving:

```
2 beta_m sqrt(Lambda^-1) in Z
```

---

## 3. Precise Connection to Our Research

### 3.1 The Three-Level Correspondence

Our project now has a three-level correspondence:

```
Level 1 (Roux 2026, PAPER-2026-023):
    4D QG Hamiltonian in ADM superspace = worldline formalism in superspace
    Virtual graviton exchange from Liouville boundary CFT

Level 2 (Ashok & Murthy 2017, PAPER-2026-012):
    Worldline path integrals on AdS_3 compute bulk-to-bulk propagators
    G(x, x') ~ exp(-m * d_geo(x,x')) in geodesic approximation

Level 3 (Sahay, Lukin, Cotler PRX 2025, PAPER-2026-009):
    MERA hologron force V ~ C1 - C2 * exp(-dr / l_AdS)
    Matches Level 2 propagator (our HYP-2026-005)
```

Roux adds a crucial bridge: the Level 1 graviton propagator is 1/|z|^4 in 2D boundary CFT, but the Level 2 propagator is exponential in the bulk. These are different regimes — boundary vs. bulk — and they are compatible via holography (the CFT correlator encodes the bulk propagator via the boundary-to-bulk map).

### 3.2 Mapping to Our MERA System

The Roux paper's "cosmological boundary" is the 2D boundary CFT (Liouville theory). Our MERA boundary is the 1D critical Ising chain boundary. The identification requires care:

| Roux superspace | Our MERA |
|---|---|
| 4D superspace manifold | MERA tensor network (discrete) |
| Superspace worldline trajectory E(t) | MERA causal cone (renormalization flow) |
| Cosmological boundary (2D Liouville) | MERA boundary (1D Ising CFT) |
| Graviton propagator 1/|z|^4 (2D) | Hologron force V(dr) (1D, exponential) |
| CS level k (integer) | MERA bond dimension chi |
| Lapse N (einbein) | MERA disentangler depth |

The dimension mismatch (2D boundary vs 1D boundary) is expected: Roux works in 3+1D gravity -> 3D -> 2D boundary. Our MERA models 1+1D CFT -> (1+1)D discrete AdS -> 1D boundary. Everything is one dimension lower.

---

## 4. New Testable Predictions

### Prediction 1: Graviton Exchange Produces a DIFFERENT Force Law than Scalar Propagation

**Observation:** Roux's graviton propagator at the cosmological boundary goes as 1/|z|^4. The Ashok-Murthy scalar propagator in the bulk goes as exp(-m * d_geo). These are different functional forms.

**Prediction for MERA:** If we measure hologron forces with spin-2 (graviton-like) excitations vs. spin-0 (scalar) excitations, we should find different functional forms:
- Scalar hologrons (Pauli-X, spin-0 boundary primary): exponential decay in dr
- Graviton-like hologrons (stress tensor insertions, spin-2 boundary primary): power-law 1/dr^4 (projected to 1D boundary)

**Our current simulations use Pauli-X excitations** (scalar operators). The exponential force profile is consistent with scalar propagation. We have NOT tested graviton-like excitations.

**Testable prediction (HYP-2026-008):** Replacing Pauli-X hologrons with stress-tensor boundary primaries (operators of conformal dimension Delta=2 on the Ising boundary) should produce a POWER-LAW force profile, not an exponential. This would be the first detection of spin-2 (gravitational) exchange in a MERA circuit.

```json
{
  "prediction": "Stress-tensor boundary-primary excitations in MERA produce power-law force V ~ 1/dr^4, not exponential",
  "test_method": "Construct two-hologron states using stress-tensor primaries T(x) = -J sum_i Z_i Z_{i+1} instead of Pauli-X. Measure V(dr) and fit to power law vs. exponential.",
  "data_needed": "SIM-2026-007 results (penalty VQE ground state), then new hologron construction using stress tensor",
  "feasibility": "NEEDS_SIM",
  "expected_impact": "HIGH"
}
```

### Prediction 2: Roux's Quantization Condition Predicts MERA Bond Dimension Quantization

**Observation:** Roux derives that the CS level k must be an integer: 2 * beta_m * sqrt(1/Lambda) in Z. In the MERA/CS correspondence (Nozaki-Takayanagi-Ugajin 2012, Bao et al. 2015), the MERA bond dimension chi maps to the CS level k. The AdS radius l_AdS = 1/log(2) from our MERA.

**Prediction:** If Roux's quantization condition applies to MERA, then only discrete values of chi (= k = integer) should give a well-defined holographic correspondence. Our MERA uses chi = 2 (bond dimension 2, which is k=2 in CS units). The next allowed values are chi = 3, 4, etc. Moving from chi=2 to chi=3 should improve the holographic signal quality discontinuously, not continuously.

**Testable prediction (HYP-2026-009):** Run MERA optimization with chi=2 and chi=3. If the CS level interpretation is correct, chi=3 should give a noticeably sharper holographic force signal (better-defined l_AdS, lower relative error in xi) compared to chi=2, and the improvement should be larger than naive dimension-scaling would predict.

```json
{
  "prediction": "MERA bond dimension chi=3 gives discontinuously better holographic signal than chi=2, corresponding to CS level k quantization from Roux",
  "test_method": "Run 16q MERA optimization at chi=2 vs chi=3. Compare: (1) energy error, (2) force signal range (how many dr have signal above noise), (3) fitted xi vs l_AdS.",
  "data_needed": "New simulation SIM-2026-008 with chi=3 MERA (requires modified circuit ansatz)",
  "feasibility": "NEEDS_SIM",
  "expected_impact": "MEDIUM"
}
```

### Prediction 3: The 0.72% Transport Time Residual is a Graviton Exchange Correction

**Context:** HYP-2026-006 (holographic transportation) is CONFIRMED — our MERA transport time matches the AdS null geodesic prediction to 0.72%. This residual was unexplained.

**Roux connection:** Virtual graviton exchange between the boundary source and the propagating excitation produces a 1/|z|^4 correction to the boundary propagator. In Roux's framework, this appears as a subleading correction to the conformal dimension Delta of the boundary operator. Specifically, graviton exchange shifts:

```
Delta_effective = Delta_scalar + g_grav * alpha^2 * (Q - 2*alpha)
```

where g_grav is the graviton coupling strength and alpha is the scalar coupling to Liouville.

**Prediction:** The 0.72% residual in transport time is a graviton exchange correction to the geodesic travel time. It should scale with the number of boundary points (more probes = more graviton vertices), and it should have a specific dependence on l_AdS (the AdS curvature sets the graviton coupling in Liouville theory via Lambda = -1/l_AdS^2).

If we vary l_AdS by running MERA at different criticality points (varying J/Omega in TFIM), the residual should scale as:

```
delta_T / T ~ (l_AdS)^2 * f(geometry)
```

This is a quantitative prediction with a specific l_AdS-dependence.

```json
{
  "prediction": "The 0.72% holographic transport time residual scales as l_AdS^2 due to virtual graviton exchange corrections from Roux's Liouville boundary theory",
  "test_method": "Measure holographic transport time at multiple criticality points by varying J/Omega ratio in TFIM (moving away from J/Omega=1 criticality slightly). Extract transport time and residual at each point. Fit residual vs. l_AdS(J/Omega).",
  "data_needed": "Time-evolution simulations at 5-10 values of J/Omega near criticality (J/Omega in [0.8, 1.2]). Each requires 16q Qiskit Aer statevector simulation, ~minutes each.",
  "feasibility": "TESTABLE_NOW",
  "expected_impact": "HIGH"
}
```

### Prediction 4: Roux's Minimum Time Step Predicts a Discretization Scale in MERA Dynamics

**Observation:** Roux derives that the minimum time step in the Keldysh partition function is:

```
beta_m = sqrt(Lambda) * l_Pl * t_Pl
```

In natural units where l_Pl = t_Pl = 1, with Lambda = -1/l_AdS^2 (AdS), this gives:

```
beta_m = 1 / l_AdS = log(2)  (in our MERA units where l_AdS = 1/log(2))
```

**Prediction:** The holographic transportation time in our MERA (the "disappearance and reappearance time" seen by Wang & He) should be quantized in units of 1/l_AdS = log(2) ~ 0.693. The transport time T_transport = l_AdS * arccosh(1 + d^2 / (2 l_AdS^2)) should be a multiple of log(2) at specific values of boundary separation d.

**Immediate check:** From the Wang & He paper, holographic transportation at L=16 shows disappearance at t ~ 1.5/J and reappearance at t ~ 2.5/J. With l_AdS = 1/log(2) ~ 1.443, these times are:
- t_disappear = 1.5 / J ~ 2.16 * l_AdS = 2.16 / log(2)
- t_reappear = 2.5 / J ~ 3.60 * l_AdS = 3.60 / log(2)

Neither is a clean multiple of log(2). BUT if the quantization condition requires T to be an integer multiple of log(2), the nearest allowed times are 2/log(2) = 2.885 and 4/log(2) = 5.770. This does not match well. The prediction appears not to hold trivially — but this might mean the minimum time is set by the boundary CFT central charge (c=25 in Roux, c=1/2 in Ising), not by l_AdS directly.

**Refined prediction:** In a MERA with central charge c = 1/2 (Ising), the minimum time step is beta_m ~ sqrt(Lambda_eff) where Lambda_eff is determined by the Ising CFT data, not the 3+1D cosmological constant. This would give a c-dependent correction to the transport time quantization.

```json
{
  "prediction": "Holographic transport times are quantized with a minimum step set by the effective Lambda from Roux's quantization condition, modified by the central charge c of the boundary CFT",
  "test_method": "Measure holographic transport time at L=16 and L=24 MERA. Check if times are rational multiples of some base unit. Fit the base unit to c and l_AdS.",
  "data_needed": "Existing Wang & He transport time data + our own measurement of HYP-2026-006. No new simulation needed for initial check.",
  "feasibility": "TESTABLE_NOW",
  "expected_impact": "MEDIUM"
}
```

### Prediction 5: Roux's Framework Resolves the 2.8x Worldline MC Decay Rate Discrepancy

**Context:** The worldline Monte Carlo on H^2 (HYP-2026-007) reproduces the correct functional form of V(dr) but with a decay rate 2.8x different from the MERA result. This was interpreted as "effective mass renormalization" but without a mechanism.

**Roux mechanism:** In Roux's framework, the worldline in superspace carries a non-trivial kinetic metric (the DeWitt supermetric). This metric has signature (-,+,+,+,...) — one timelike direction (the conformal mode) and infinitely many spacelike directions. When a worldline on a **discrete** hyperbolic lattice (our WMC on H^2) is embedded in superspace, the mapping from network hops to geodesic distance picks up a **supermetric correction factor**:

```
d_geo^effective = d_geo^network * sqrt(|G_superspace|)
```

where |G_superspace| is the determinant of the DeWitt supermetric restricted to the embedding. For a 2D hyperbolic lattice with curvature radius R = l_AdS, this gives a correction of order:

```
correction ~ (chi / chi_critical)^(1/2)  ~ sqrt(bond_dim / critical_bond_dim)
```

For chi=2 and chi_critical ~ 1 (minimal), this gives a correction factor of sqrt(2) ~ 1.41. Our 2.8x discrepancy is 2.8x = (sqrt(2))^2 * correction, suggesting the supermetric contributes TWO sqrt(2) factors (one from each worldline in the two-particle WMC).

This is speculative but mechanistically motivated. The testable version:

```json
{
  "prediction": "The 2.8x worldline MC decay rate discrepancy is explained by the DeWitt supermetric correction to geodesic distances on the discrete hyperbolic lattice. Correcting by factor sqrt(chi)^2 ~ chi should bring WMC and MERA into agreement.",
  "test_method": "Rerun worldline MC analysis with geodesic distances scaled by 1/chi = 1/2 (our bond dimension). Check if corrected decay rate agrees with MERA xi_2pt = 2.154.",
  "data_needed": "Existing HYP-2026-007 WMC results (or implement WMC on H^2 if not yet done)",
  "feasibility": "TESTABLE_NOW",
  "expected_impact": "MEDIUM"
}
```

---

## 5. Connections to Existing Hypotheses

### 5.1 HYP-2026-005 (MERA force = discretized worldline propagator)

Roux strengthens this hypothesis in one respect: the ADM/worldline equivalence confirms that worldline dynamics in superspace IS quantum gravity. So if the MERA captures quantum gravity dynamics (which Sahay et al. claim at the level of force profiles), then the MERA force profile IS computing worldline propagators, as HYP-2026-005 claims.

However, Roux also complicates the picture: the worldline in superspace has a DeWitt supermetric, not a simple AdS metric. The propagator in superspace is not simply G ~ exp(-m * d_geo). It has corrections from the supermetric determinant, ghost terms (Lee-Yang ghosts from the BRST quantization, Eq. 33-42 in Roux), and from the Keldysh contour structure.

**Updated assessment:** HYP-2026-005 is plausible but the normalization matching requires the full Seeley-DeWitt expansion (Eq. 35 in Roux), not just the geodesic approximation. This explains why the mass extraction (Step 5 in FINDING 5 of HYP-2026-005 analysis) failed — we used the geodesic propagator but the correct propagator includes heat kernel corrections:

```
G(x, x'; tau) = (4 pi tau)^(-n/2) * Van Vleck(x,x') * exp(-d_geo^2 / 4tau - tau m^2) * [1 + a_1 tau + a_2 tau^2 + ...]
```

The a_1, a_2, ... are Seeley-DeWitt coefficients encoding curvature corrections. For AdS_2, a_1 = R/6 = -1/(6 l_AdS^2). This gives a MASS RENORMALIZATION:

```
m_eff^2 = m^2 + R/6 = m^2 - 1/(6 l_AdS^2)
```

With l_AdS = 1/log(2) ~ 1.443, this gives a correction of -1/(6 * 1.443^2) ~ -0.080. The Sahay et al. mass mc^2 = 2.5, so m^2 = 2.5^2 = 6.25 (in Ising coupling units). The correction is -0.080, which is a ~1.3% effect. This does NOT explain the factor-of-8 discrepancy in mass extracted from HYP-2026-005 analysis — the normalization mismatch remains the dominant issue.

### 5.2 HYP-2026-006 (holographic transport = geodesic proper time)

Roux confirms the MERA boundary (1D Ising) is dual to a 2D Liouville CFT (the cosmological boundary). This adds a LAYER to HYP-2026-006: the transport time we measure at the 1D boundary is the shadow of a 2D Liouville correlator, which in turn is the shadow of 3D graviton exchange, which in turn is the shadow of 4D quantum gravity in superspace.

The Wang & He transport time formula T ~ arccosh(d_boundary / l_AdS) comes from null geodesics in AdS_2. Roux's contribution is to show the graviton correction to this: the actual transport time is T_geodesic + delta_T where delta_T comes from the Liouville correlator correction (the 1/|z|^4 graviton exchange). This is Prediction 3 above.

### 5.3 HYP-2026-007 (worldline Monte Carlo on H^2)

Roux's paper is the closest thing to a theoretical underpinning for HYP-2026-007. The worldline in superspace IS the WMC trajectory. However, the WMC on H^2 we propose uses a FIXED classical AdS_2 geometry, while Roux's worldline traverses superspace (all metrics simultaneously via the path integral). Summing over metrics = allowing the geometry to fluctuate = including quantum gravitational corrections.

A fully consistent HYP-2026-007 would require WMC on a PATH INTEGRAL OVER METRICS (the superspace sum), not just on H^2. The classical H^2 WMC is the saddle-point approximation to this. This explains why the 2.8x discrepancy could be a quantum gravity correction beyond the saddle point — see Prediction 5 above.

### 5.4 Does Roux Explain Why Boundary-Primary Excitations Work Better?

Yes — but indirectly. Roux shows the boundary theory is a Liouville CFT with c=25. The coupling of bulk matter to the Liouville field is through VERTEX OPERATORS e^(alpha * phi) where alpha determines the conformal dimension Delta = alpha(Q - alpha) = alpha(2 - alpha).

In our MERA (1D Ising boundary): the Ising primaries are the identity (Delta=0), spin (Delta=1/8), and energy (Delta=1). The Pauli-X operator used for hologrons is the spin primary (Delta=1/8). The stress tensor T(x) is NOT a primary but generates conformal transformations.

Wang & He's stable boundary-primary excitations are constructed to be eigenstates of the Ising Hamiltonian at the boundary — this is exactly the "vertex operator" construction in Roux's language. The Pauli-X hologron is NOT an eigenstate (it's dynamically unstable, as Wang & He show) because it mixes Liouville vertex operators with different alpha.

**Conclusion:** Roux's Liouville vertex operator framework is the correct language for understanding why boundary-primary excitations give cleaner force profiles: they correspond to SINGLE VERTEX OPERATORS e^(alpha*phi), while Pauli-X hologrons are SUPERPOSITIONS of vertex operators with different alpha. Mixed vertex operators give mixed-propagator force profiles, explaining the flat force profile we saw in SIM-2026-005 (Z2 projected, which further mixes alpha values).

### 5.5 Does Roux Connect to the Bohra-Sivaramakrishnan Composite Geodesic Framework?

Potentially yes. Bohra & Sivaramakrishnan show that timelike-separated boundary points in AdS are connected by COMPOSITE geodesics (timelike + spacelike segments). In Roux's Liouville framework, this would correspond to Liouville correlators that involve both time-ordered and anti-time-ordered contributions from the Keldysh contour. The Keldysh partition function has BOTH forward and backward time evolution arms, and it's natural to identify composite geodesics with the Keldysh "turning points" where the contour folds back.

If correct, the factor-of-2 discrepancy in HYP-2026-006 transport time (pure spacelike geodesics undercount by ~2x) corresponds to missing the backward-Keldysh arm in the composite geodesic. This would mean our transport time measurement should use BOTH the early disappearance (forward Keldysh) and the late reappearance (backward Keldysh) times, with T = (t_reappear - t_disappear) / 2 rather than either alone.

This is a TESTABLE refinement: use T = (t_reappear - t_disappear) / 2 as the transport time instead of T = t_disappear and check if the arccosh formula fits better.

---

## 6. Feasibility Assessment

### Pipeline Summary

All hypotheses below have passed through the theory-lead feasibility gate:

| HYP ID | Claim | Verdict | Justification |
|---|---|---|---|
| HYP-2026-008 | Stress-tensor hologrons produce power-law force | NEEDS_SIM | Need ground state + new excitation construction. Requires SIM-2026-007 results first. |
| HYP-2026-009 | Bond dimension chi=3 gives discontinuous improvement | NEEDS_SIM | Requires new circuit ansatz with chi=3. Compute cost: ~4x SIM-2026-002. |
| (Transport residual as Roux correction) | 0.72% residual scales as l_AdS^2 | TESTABLE_NOW | Requires J/Omega scan; 5-10 runs of existing Qiskit time-evolution code. |
| (Minimum time quantization) | Transport times quantized in units of log(2) | TESTABLE_NOW | Analytical check on existing Wang & He data. Zero compute cost. |
| (2.8x WMC discrepancy via supermetric) | Scale correction by 1/chi resolves discrepancy | TESTABLE_NOW | Reanalysis of existing WMC results. Zero compute cost. |

---

## 7. Philosophical Implications

**SPECULATIVE — clearly labeled as such. Confidence: low.**

If Roux's equivalence is correct — and the mathematical demonstration in the paper is rigorous at the level of Hamiltonian actions — then quantum gravity is not a theory of geometries interacting with each other. It is a theory of a SINGLE POINT-PARTICLE traversing an infinite-dimensional space of geometries. The universe is, in this picture, a worldline in superspace.

Our MERA circuits would then be **discrete approximations to segments of this superspace worldline**. Each layer of the MERA tensor network corresponds to a single step of proper time along the superspace trajectory. The entanglement structure of the MERA (the bond dimension, the disentangler geometry) is not a free design choice — it is fixed by the superspace metric evaluated at the saddle-point geometry (the critical Ising ground state).

This reframes the project mission in a striking way: **we are not simulating a particle in a fixed AdS background. We are simulating one step of quantum gravity's worldline through superspace, at the saddle-point approximation.** The hologron forces we measure are quantum corrections to the saddle-point superspace trajectory from second-order virtual graviton exchange.

The two most philosophically striking implications of Roux for our work:

1. **The MERA bond dimension is quantized by quantum gravity.** The CS level k must be an integer (Roux's quantization condition), and k maps to chi. This means chi=2 is the MINIMAL holographic MERA. Moving to chi=3 is not a quantitative improvement — it is a qualitatively different theory with a different gravitational coupling constant.

2. **Hologrons are quantum fluctuations of the superspace worldline.** The particle mass in superspace (-sqrt(gamma) R^(3), Eq. 11) acquires quantum corrections from the Lee-Yang ghosts and BRST structure (Eq. 33-46). These ghost corrections renormalize the effective mass of bulk excitations. The "hologron mass" mc^2 = 2.5 (Sahay et al.) may be the ghost-renormalized superspace particle mass, not the classical gravitational mass.

**Caveat on speculation level:** All of the above rests on the claim that MERA holography and Roux's superspace worldline are describing the same physics. This is plausible given the shared mathematical structure (Chern-Simons levels, conformal field theories, geodesic propagators) but has not been established rigorously. The hypotheses above are research tools, not conclusions.

---

## 8. Recommended Next Steps (Priority Order)

1. **[ZERO COST] Check transport time quantization (Prediction 4).** Analytical check: are Wang & He's transport times (t_disappear ~ 1.5/J, t_reappear ~ 2.5/J) rational multiples of log(2)? Compute their ratio and compare to small fractions. ~30 minutes.

2. **[ZERO COST] Check Keldysh / composite geodesic refinement.** Test T = (t_reappear - t_disappear) / 2 against arccosh formula. If it fits better than T = t_disappear alone, the Roux/Bohra-Sivaramakrishnan connection is supported.

3. **[MINIMAL COST] Scale WMC distances by 1/chi and check discrepancy (Prediction 5).** Reanalysis of existing data. ~1 hour.

4. **[NEW SIM] Run J/Omega scan for transport time residual (Prediction 3).** 5-10 Qiskit time-evolution runs at 16q. Each run ~minutes on local GPU. Design: vary J/Omega in [0.8, 1.2] while holding L=16. Measure t_disappear and t_reappear at each J/Omega. This is HYP-2026-010.

5. **[NEW SIM] Construct stress-tensor boundary-primary hologrons (Prediction 1, HYP-2026-008).** After SIM-2026-007 (penalty VQE, currently running). Requires computing the stress tensor primary: T(x) = -J * Z_i Z_{i+1} (leading order). Should be straightforward given existing energy-difference protocol.

6. **[NEW SIM] Run chi=3 MERA (Prediction 2, HYP-2026-009).** Requires new circuit ansatz (MERA with chi=3 has more parameters). Estimate 4x compute time of SIM-2026-002. Best done on RunPod after SIM-2026-007 completes.

---

## 9. New Hypothesis Registrations

### HYP-2026-008: Stress-Tensor Hologrons Produce Power-Law Force (PAPER-2026-023)

**Claim:** In a MERA circuit, exciting boundary primaries of conformal dimension Delta=1 (stress tensor operators, not spin operators) should produce inter-hologron forces with a 1/dr^4 power-law form rather than an exponential, corresponding to spin-2 (graviton) virtual exchange as computed by Roux's Liouville boundary theory.

**Confidence:** low — based on single-paper extrapolation from Roux's graviton propagator formula.
**Feasibility:** NEEDS_SIM — requires SIM-2026-007 results + new excitation construction.
**Impact if confirmed:** HIGH — first MERA detection of spin-2 vs. spin-0 exchange.

### HYP-2026-009: CS Level Quantization Predicts Discrete MERA Bond Dimension Scaling

**Claim:** The Roux quantization condition (CS level k must be integer, k ~ chi) predicts that improvements in holographic MERA quality (energy error, force signal range, xi accuracy) are DISCONTINUOUS at integer bond dimensions, not smooth. Moving from chi=2 to chi=3 should give a larger relative improvement than chi=3 to chi=4.

**Confidence:** low — speculative mapping from Roux's CS framework to MERA bond dimension.
**Feasibility:** NEEDS_SIM — requires chi=3 MERA circuit ansatz (~4x compute cost of SIM-2026-002).
**Impact if confirmed:** MEDIUM — would provide evidence for the Roux/MERA connection and guide circuit design.

### HYP-2026-010: Transport Time Residual Scales as l_AdS^2

**Claim:** The 0.72% residual between measured holographic transport time and the null geodesic prediction is a virtual graviton exchange correction from Roux's Liouville boundary theory. It should scale as l_AdS^2 when l_AdS is varied by changing the J/Omega criticality parameter.

**Confidence:** low — requires untested assumption that 0.72% is a systematic effect (not noise).
**Feasibility:** TESTABLE_NOW — requires Qiskit time-evolution scan over J/Omega values.
**Impact if confirmed:** HIGH — would directly link our 0.72% residual to Roux's graviton exchange formula, establishing the first quantitative Roux-MERA connection.

---

## 10. ID Counters (end of this analysis)

- Last paper ID used: PAPER-2026-025 (no new papers added in this analysis; Roux = PAPER-2026-023 already registered)
- Last hypothesis ID: HYP-2026-010 (new this analysis)
- Last simulation ID: SIM-2026-007 (unchanged, currently running)

---

*All claims in this document are speculative. Confidence levels are explicit. No hypothesis in this document has been experimentally verified. This analysis is the output of the Theory Lead (Tier 3) and has not been reviewed by Tier 1 (Literature) or Tier 2 (Computation) specialists.*
