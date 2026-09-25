# adv:geometry-advocate — The strongest operational form of Hypothesis B, and what survives contact with the records

**Role:** Geometry Advocate (RESEARCH-DIRECTOR §27). Charter: assume Hypothesis B of §4 deserves its
strongest defense; construct the strongest **operational, falsifiable** version of the
emergent-geometry claim, or report honestly that no such version exists.

**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` §§4, 5, 6, 7, 8, 10, 11, 12, 19, 28,
33, 34, 36, 40. Applied literally.

**Date:** 2026-08-17. **Repo state:** branch `public-release`; PRD accession DV13971 with editors.

---

## 0. Bottom line

I set out to build the best case for Hypothesis B. Three things happened.

1. **I found a sharpening that makes Hypothesis B testable rather than rhetorical.** Under a literal
   reading of §4 — where Hypothesis A already grants "the CFT **and tensor-network structure**" —
   almost every observable in §11 is disqualified before any simulation, because it is either a
   functional of the state (→ fixed by CFT data) or a functional of the network (→ granted to A).
   Hypothesis B has content in exactly one band, stated as **B★** in §1.4 below. Everything in this
   artifact is organised around that band.

2. **I found new evidence against the project's single strongest geometric anchor**, and it did not
   come from the phase-1 auditors. The transport result's "AdS radius" factor appears to be
   **dimensionally spurious**. I computed the low-lying spectrum of the Wang–He boundary Hamiltonian
   myself (§2.1, code included) and it is normalised so that **energy gaps equal Ising scaling
   dimensions exactly** (0.1251, 0.99839, 1.11869, 1.9776 at N=16 vs 1/8, 1, 9/8, 2). In those units
   the boundary lives on a circle of circumference 2π with velocity 1, and the AdS radius **cancels
   out of the null-geodesic crossing time**: the ℓ-free geometric prediction is T = π/2 = 1.571 or
   T = π = 3.142, against a measurement of 2.239. The entire 1.2 % agreement is supplied by the free
   multiplicative factor ℓ_AdS = 1/ln χ = 1.4427, which the manuscript itself says "is set by the
   MERA architecture, not by optimization" (`research/submission-package/prd/paper-prd.tex:66`).

3. **The manuscript assigns three different values of ℓ_AdS to the same claimed geometry** — 1.4427
   (χ=2, transport), 0.9102 (χ=3, force), 0.4024 (χ=12, Potts) — because Eq. (2) makes ℓ_AdS a
   function of the bond dimension. A physical AdS radius of one chain cannot take three values.

I therefore report the honest answer required by the charter: **no *currently instantiated* observable
in this project supports Hypothesis B**, and the flagship geometric number is more likely a unit
convention than a measurement. But an operational Hypothesis B **does exist** in the B★ band, it is
falsifiable, and this project can test it on hardware it already owns. §6 is that design.

The top-ranked experiment is **GEO-1: unit-consistency and representation-invariance of the emergent
AdS radius**, whose slice 0 is analytic, costs zero compute, is ~70 % complete inside this artifact,
and would change what the project says in a PRD referee response. This is exactly the §40 criterion
("prove that a proposed geometry observable is algebraically dependent on existing CFT data" /
"demonstrate that rewiring destroys the observable while preserving ordinary CFT accuracy").

---

## 1. Sharpening Hypothesis B until it can be wrong

### 1.1 The two hypotheses, quoted

- **A** (`RESEARCH-DIRECTOR.md:201`): "MERA is an efficient hierarchical representation of critical
  quantum states. Apparent geometry is descriptive or computational, but adds no independently
  predictive physical content **beyond the underlying CFT and tensor-network structure**."
- **B** (`RESEARCH-DIRECTOR.md:205`): "MERA contains geometric structure that supports predictions,
  reconstruction behavior, locality properties, dynamical relations, or invariants **not
  automatically fixed by ordinary CFT data alone**."

The emphasised clauses are not symmetric, and that asymmetry is doing enormous work. A's grant
includes *tensor-network structure*; B's exclusion mentions only *CFT data*. Read literally, an
observable that is a pure combinatorial consequence of the MERA graph is **inside A** and therefore
cannot support B, even though B's own wording would let it through.

I adopt the literal reading, as instructed. It is also the scientifically correct one: §34 demands
exactly this separation ("determine whether it is invariant across representations of the same state,
specific to MERA architecture, specific to a chosen gauge…").

### 1.2 The trilemma (an advocate's own no-go sketch)

Let `O` be any candidate geometric observable. Exactly one of the following holds.

**(i) `O` is a functional of the represented state |ψ⟩ alone.**
Then `O` is determined by |ψ⟩. For a critical ground state in a known universality class, the
universal content of `O` is fixed by the CFT data {c, Δ_i, C_ijk} and the non-universal content by
the microscopic Hamiltonian. Geometry adds nothing; **A accounts for `O`**. Examples in this repo:
the Synge distance (HYP-2026-026 — the record itself says the distance "carries only the
lightest-primary dimension Δ_σ = 1/8", `research/data/hypotheses/HYP-2026-026.json` `claim`); the
PEE-thread Crofton integral (HYP-2026-022, REFUTED, `SIM-2026-024.json`); raw CMI (HYP-2026-012,
NOT_SUPPORTED, `SIM-2026-013.json` `crofton_verdict`); α = 2Δ_T = 4 (`SIM-2026-014.json`
`key_finding`: "exactly from conformal symmetry").

**(ii) `O` is a functional of the network N (graph, gauge, χ, architecture).**
Then either
  - (ii-a) `O` changes under internal gauge transformations or architecture change → `O` is not a
    property of anything physical (§34), or
  - (ii-b) `O` is invariant, in which case `O` is a structural invariant of the ansatz class — which
    §4's A **explicitly grants**.
Either branch, **A accounts for `O`**. Examples: causal-cone containment (exact by isometry
construction, a theorem about the ansatz); ℓ_AdS = 1/ln χ (`paper-prd.tex:64`); radial coordinate =
log_b r; the number of bonds cut by a cut.

**(iii) `O` is a functional of the *joint* object (state, network).**
This is the only band left.

### 1.3 Why (iii) is not automatically empty

A joint functional can be non-trivial because the *pairing* between a state and a representation
carries information neither carries alone: which states a given architecture represents *well*,
where its errors sit, and which physical quantities it predicts *without fitting*. This is where
holographic-code intuition actually lives — a code is a map, not a state and not a graph.

### 1.4 B★ — the strongest operational form of Hypothesis B

> **B★.** There exists an observable `O`, computed from the pairing of a critical state with its
> MERA representation, such that
> 1. **(invariance)** `O` is unchanged, within stated uncertainty, under (a) internal gauge
>    transformations on the network's virtual legs, (b) change of MERA architecture among
>    {ternary b=3, binary b=2, modified-binary b=2}, and (c) increase of bond dimension χ, once
>    the constructions are matched on {E₀ error, Δ_σ, Δ_ε, c};
> 2. **(non-derivability)** `O` is *not* algebraically determined by {χ, b, cone width} nor by the
>    CFT data {c, Δ_i, C_ijk} actually used to build and validate the network;
> 3. **(prediction)** `O` predicts, parameter-free and out-of-sample (§18), the value of at least one
>    quantity measured on a system the network was **not** calibrated against.

Clause 1 defeats branch (ii-a). Clause 2 defeats branches (i) and (ii-b). Clause 3 is what converts a
diagnostic into a claim. **All three are required.** Any two of them is a result the project already
has, and none of those results supports B.

**Consequence I accept as the advocate:** B★ is a hard target. Its most likely outcome is a clean
negative. §16 and the North Star (`RESEARCH-DIRECTOR.md:1643`) both say that a negative here is worth
as much as a positive, and §28 says explicitly "do not simply maximize likelihood of a positive
result". I am proposing the experiment because it is decisive, not because I expect B to win.

### 1.5 What B★ rules out immediately

Every observable the project has actually measured under a geometric heading fails clause 2 or clause
1 before a single new run:

| Project observable | Record | Fails |
|---|---|---|
| α = 2Δ_T = 4 | `SIM-2026-011-interaction.json`, `SIM-2026-014.json` | clause 2 — Δ_T = 2 in every 2D CFT |
| C_TTT = 2√2/√c | `SIM-2026-067/068/069.json` | clause 2 — Virasoro identity; `inv-pipelines.md:215` calls it "algebraically `c`" |
| C_σσε = 0.5 | `SIM-2026-061.json` | clause 2 — BPZ 1984 |
| Synge distance d(r) | `SIM-2026-031.json` | clause 2 — reduces to Δ_σ, and the record says so |
| ℓ_AdS = 1/ln χ | `paper-prd.tex:64` | clauses 1 and 2 — an explicit function of χ |
| m_eff = ℓ_AdS/ξ_MERA | `effective_mass_analysis.json` | inherits ℓ_AdS's χ-dependence |
| T = (π/2)·ℓ_AdS | `SIM-2026-025.json` | clause 2, and see §2.1 — the ℓ factor is dimensionally spurious |

That table is the honest state of play. Nothing in it is a defect of execution; the numbers are
mostly right. They are the wrong *kind* of number for the question §4 poses.

---

## 2. New evidence gathered in this pass

Four findings. GA-1 is the significant one; I generated it by running a calculation, not by reading a
record, and I have not found it in any project document or in the seven phase-1 audit artifacts
(searched `research/data/audit/raw/*.md` for `ln 2`, `l_AdS`, `AdS radius`, `bond dimension`).

### 2.1 GA-1 (CRITICAL) — the transport anchor's ℓ_AdS factor is dimensionally spurious

**What the manuscript claims.** `research/submission-package/prd/paper-prd.tex:62-66`:

> ℓ_AdS = 1/ln χ = 1/ln 2 = 1.4427. *This value is set by the MERA architecture, not by
> optimization.*

and `paper-prd.tex:151-154`:

> T_predicted = (π/2)·ℓ_AdS = (π/2)·(1/ln 2) = 2.266

measured against T = 2.23888 at N=16 (`SIM-2026-025.json` `.runs.N16.T_measured_refined`), residual
−1.205 %, quoted in the abstract as the project's second headline result (`paper-prd.tex:29`).

**What I did.** The evolution Hamiltonian is
`H_boundary = (L/4π) Σ_j [X_{j-1} Z_j X_{j+1} − X_j X_{j+1}]` (PBC), built by
`build_H_boundary()` in `research/data/simulations/holographic_transport_finedt.py:117-126`. I
imported that builder verbatim (no re-implementation) and diagonalised it. Exact reproduction:

```python
import sys, numpy as np, os
d = r'D:\quantum-worldline\research\data\simulations'
os.chdir(d); sys.path.insert(0, d)
src = open('holographic_transport_finedt.py').read()
start = src.index('def build_3body_term'); end = src.index('def measure_Y')
ns = {}
exec("import numpy as np\nfrom scipy.sparse import csr_matrix, identity, kron\n" + src[start:end], ns)
from scipy.sparse.linalg import eigsh
for L in (12, 16):
    H = ns['build_H_boundary'](L).tocsr()
    vals = np.sort(eigsh(H, k=10, which='SA', return_eigenvectors=False))
    print(L, vals[0], np.round(vals[1:] - vals[0], 5))
```

**Result (verified, runtime < 30 s):**

| N | E₀ | gaps E_n − E₀ |
|---|---|---|
| 12 | −14.632001 | 0.12518, 0.99715, 1.11379, 1.11379, 1.96032, 1.96032, 1.96032, 2.03504, 2.03504 |
| 16 | −25.979937 | **0.12510**, **0.99839**, 1.11869, 1.11869, **1.97760** (×3), 2.07409 (×2) |

E₀(16) = −25.979937 matches `holographic_transport.json` `.E_gs` = −25.979936579544773 and
`SIM-2026-025.json` `.runs.N16.E_gs` = −25.979937 — confirming I diagonalised the same operator the
transport runs evolved under.

The gaps are the **Ising CFT scaling dimensions, unrescaled**:

| gap (N=16) | exact | identification | error |
|---|---|---|---|
| 0.12510 | 1/8 = 0.125 | Δ_σ | 0.08 % |
| 0.99839 | 1 | Δ_ε | 0.16 % |
| 1.11869 (×2) | 9/8 = 1.125 | σ descendants L_{−1}, L̄_{−1} | 0.56 % |
| 1.97760 (×3) | 2 | Δ_T: T, T̄, and ε level-1 | 1.1 % |
| 2.07409 (×2) | 17/8 = 2.125 | σ level-2 | 2.4 % |

**Why this matters.** The prefactor L/(4π) has already fixed the CFT-on-a-cylinder normalisation:
H = (2πv/L)(L₀ + L̄₀ − c/12) with **v = 1** and circumference **2π**. Time in the transport
simulation is therefore *dimensionless global boundary time*, the same coordinate `t` that appears in
global AdS₃, ds² = ℓ²(−cosh²ρ dt² + dρ² + sinh²ρ dφ²).

In that coordinate a boundary-to-boundary null geodesic crosses in **Δt = π**, and the "null
condition" the project uses gives **Δt = π/2** (`composite_geodesic_results.json`
`.calculations.composite_geodesic.derivation`: "cos(T)+1=1 ⇒ T=π/2"). **ℓ_AdS does not appear.** It
multiplies the bulk metric uniformly and cancels from the ratio that defines the null cone; it can
only enter if boundary time is measured in units *other* than the CFT cylinder time — which it is
not, as the spectrum above shows.

So the geometric prediction available in these units is

- T = π/2 = 1.5708 → measured 2.23888 is **+42.5 %** off, or
- T = π = 3.1416 → measured is **−28.7 %** off,

and the reported −1.21 % agreement is produced entirely by the free factor 1.4427.

**The advocate's rescue attempts, and why they fail.**

- *R1: perhaps T is not a cylinder-time interval.* It is: T = t_reappear − t_dip from evolution under
  H_boundary (`SIM-2026-025.json` `.runs.N16.dip_time_refined` 2.49512, `.reappear_time_refined`
  4.734). Same clock as the spectrum.
- *R2: perhaps the geodesic is not antipodal, so Δt < π.* The perturbation has σ_φ = 0.4
  (`SIM-2026-025.json` `.physical_parameters.sigma_t/sigma_phi`), so it is localised. That makes any
  ℓ-free prediction **smaller** than π, worsening the gap to 2.239.
- *R3: perhaps the MERA's discrete geometry has a different time normalisation than continuum AdS₃.*
  Then ℓ_AdS is a **fitted conversion factor, not a prediction** — §18 classification changes from
  "predicted" to "calibrated", and the manuscript's Result 2 becomes a one-parameter fit to one
  number at one system size. The record already contains the fitted alternative:
  `composite_geodesic_results.json` `.inputs.l_AdS_fitted` = 1.233, which gives −13.9 %.
- *R4: perhaps 1.4427 is right for another reason.* Then the burden is to say which, and to predict
  something else with it. Note the look-elsewhere problem (§17): 5π/7 = 2.2440 is 0.2 % from the
  measurement and π/√2 = 2.2214 is 0.8 % — both **closer** than (π/2)/ln 2 = 2.2662 at 1.2 %. A
  single O(1) coincidence at one system size does not discriminate.

**Status.** The spectral fact is verified and certain. The dimensional conclusion is an analytic
argument about conventions; I present it as a strong inference that the project should check
independently, not as a completed proof. It is the zeroth slice of GEO-1 (§6.7).

### 2.2 GA-2 (MAJOR) — the manuscript carries three incompatible AdS radii

Eq. (2) makes ℓ_AdS a function of the bond dimension. The same manuscript uses three bond dimensions:

| Section | χ | ℓ_AdS by Eq. (2) | ratio to transport value |
|---|---|---|---|
| §2.1/§3.3 transport (`paper-prd.tex:64, 153`) | 2 | 1.4427 | 1.00 |
| §6 force from optimized MERA (`paper-prd.tex:344, 351`) | 3 | 0.9102 | 0.63 |
| abstract, Potts ladder (`paper-prd.tex:29`, `SIM-2026-063.json`) | 12 | 0.4024 | 0.28 |

These are all presented as evidence for one emergent geometry of critical chains. If ℓ_AdS were a
physical radius, a single chain could not have three of them. Under Hypothesis A this is unremarkable
— it is a bookkeeping constant per ansatz. **The inconsistency is only visible if you take the
geometric reading seriously, which is precisely the advocate's job.**

Corollary: had the transport comparison been performed with the project's *own best* MERA (χ = 12,
used for Potts), the prediction would have been T = 0.632 against a measurement of 2.239 — a factor
of 3.5. The reported agreement is specific to χ = 2, a value the manuscript states was chosen for a
hardware gate budget, not for physics (`paper-prd.tex:93`: "we use χ = 2 deliberately to remain
within the Quantinuum Helios gate budget").

### 2.3 GA-3 (MAJOR) — the transport anchor is not stable in N, and the manuscript's own
scaling implies ℓ_AdS → 0

Grid-converged and coarse-grid transport times, all against the fixed prediction 2.2662:

| N | T | residual | T·L | source |
|---|---|---|---|---|
| 12 | 2.20325 | −2.777 % | 26.44 | `SIM-2026-025.json` `.runs.N12.T_measured_refined` |
| 16 | 2.23888 | −1.205 % | 35.82 | `SIM-2026-025.json` `.runs.N16.T_measured_refined` |
| 24 | 1.55 | −31.60 % | 37.20 | `holographic_transport_24q.json` `.transport_signature` |

Two observations the records do not draw:

1. **The residual sequence is non-monotone**: −2.78 %, −1.21 %, −31.6 %. The manuscript reports the
   first two as evidence of a shrinking finite-size correction (`paper-prd.tex:29`, `:172`) and the
   third separately as "indicative only" (`paper-prd.tex:206`). Both statements are individually
   defensible; together they describe an observable with no established N-limit.
2. **The manuscript's own rescue implies the geometry vanishes.** §3.4 proposes T·L ≈ 36–37 as an
   empirical regularity (`paper-prd.tex:195`, correctly labelled "an empirical observation, not a
   derived result"). If T ∝ 1/L, then the implied radius ℓ_AdS = 2T/π ∝ 1/L → **0 in the continuum
   limit**, contradicting its identification with the N-independent constant 1/ln 2. And T·L is not
   in fact constant across the three sizes: 26.4, 35.8, 37.2 — the N=12 point, the one the manuscript
   uses for the finite-size argument, is 29 % away from the other two.

Setting T(N) = 36/N equal to 2.2662 gives N = 15.9. The agreement is attained at, and only at, the
single system size studied.

### 2.4 GA-4 (MAJOR) — the π → π/2 factor was selected after seeing the ratio

`composite_geodesic_results.json` records the sequence explicitly:

- `.inputs.T_spacelike_prediction` = 4.532360 (= π·ℓ_AdS) — the original prediction;
- `.inputs.ratio_measured_spacelike` = 0.49643 — the observed ratio;
- `.calculations.composite_geodesic.formula` = "T_composite = pi*R/2 (null geodesic condition)" — the
  revised prediction, giving 2.26618;
- `.comparison.ratio_null_to_spacelike` = 0.5 vs `.observed_ratio` = 0.49643.

The record also stores `.calculations.composite_geodesic.l_AdS_needed_to_match_exact` = 1.4324 — an
explicit inverted solve for the parameter. Under §18 this is a **calibrated** quantity, not a
prediction. The manuscript presents the sequence honestly in §3.3 (`paper-prd.tex:148`, "The naive
spacelike geodesic formula predicts T = π·ℓ_AdS = 4.53, a factor of ~2 larger"), so this is a
classification defect rather than concealment — but the classification matters, because a calibrated
factor times a free χ-dependent factor leaves zero predictive content.

### 2.5 GA-5 (MAJOR, novelty gate) — the prior art that would decide the geometry question is
absent from a 139-record catalogue

§8 forbids any novelty label until a literature gate has run. For the geometry claims specifically,
`grep -ril` over `research/data/papers/*.json` returns **zero records** for each of:

| search term | records | note |
|---|---|---|
| `hyperinvariant` | 0 | the standard critique/repair line for MERA-as-AdS |
| `Czech` | 0 | despite Czech being one of the seven 2026-07-15 outreach targets (memory: Active outreach) |
| `exact holographic mapping` | 0 | the main competing bulk/boundary tensor-network dictionary |
| `branching MERA` | 0 | the architecture-dependence literature |
| `Bény` / `Beny` | 0 | causal structure of entanglement renormalization |
| `rewir*` | 0 | §11-H has no catalogued prior art at all |
| `quench` | 0 | §11-F has no catalogued prior art at all |
| `Milsted` (author field) | 0 | matched only inside prose files, never as a paper record |

`Vidal` appears in `PAPER-2026-010.json` only as a citation inside another record's prose, plus
several non-record analysis markdown files. `PAPER-2026-052.json` (modular flow) is a stub whose
`authors` field literally reads "(search result, full authors not retrieved)".

I make **no claim about what those uncatalogued works say** — I have not read them in this pass, and
asserting their content without evidence is the failure mode this audit exists to prevent. The
verifiable finding is narrower and sufficient: **the project's structured literature record contains
no prior art on the architecture-dependence of tensor-network geometry, and therefore cannot
currently support or refute a novelty claim about any geometry result.** §8's literature gate is
open. A search plan is in §9.

---

## 3. Survey of §11 candidates A–H

Rule applied literally, per the task: **discard any candidate where Hypothesis A and Hypothesis B do
not actually make different predictions.** For each candidate I state (i) the exact measurement, (ii)
A's prediction, (iii) B's prediction, (iv) whether they differ, (v) verdict.

### Summary table

| # | Candidate | Predictions differ? | Verdict | Reason |
|---|---|---|---|---|
| A | Bulk reconstruction locality | **No**, as posed | **DISCARD** as posed; survives only fused with H | Commutator support is exact-by-isometry — a theorem about the ansatz, granted to A |
| B | Entanglement-wedge reconstruction | **Yes**, but only in the architecture-contrast form | **SURVIVES (rank 2)** | Ternary and binary MERA assign *different* wedges to the same interval of the same state |
| C | Modular-flow compatibility | **No** | **DISCARD** | Continuum modular Hamiltonian is CHM-fixed; lattice tails are a state property; cost is the highest of any candidate |
| D | CMI / approximate Markov | **No** | **DISCARD** standalone; fold into B | CMI is a state functional; MPS is *exactly* Markov for contiguous cuts, so the control does not separate |
| E | Defects / inhomogeneous deformation | **No** for the analytically solved cases | **DISCARD** at rank ≤4 | SSD/rainbow/interface deformations have closed-form CFT answers; the "prediction" is Level 1 |
| F | Dynamical / quench | **Yes**, in one specific out-of-sample form | **SURVIVES (rank 3)** | The c-scaling of the transport observable across the universality ladder is not fixed either way |
| G | Curvature / distance reconstruction | **No** | **DISCARD** | Documented triple failure in-project; §11-G itself warns against estimators that reduce to Δ |
| H | Network rewiring | **Yes**, decisively | **SURVIVES (rank 1)** | The only candidate that tests clause 1 of B★ directly, and §40 names it as a first slice |

### A. Bulk reconstruction locality

**Measurement.** Reconstruct operators at putative bulk nodes (x, s) by descending through the MERA;
evaluate ‖[O(x₁,s₁), O(x₂,s₂)]‖ against graph-geodesic separation; test whether reconstruction error
scales with graph distance and whether it survives gauge/χ changes (`RESEARCH-DIRECTOR.md:544-550`).

**A predicts.** The commutator is **exactly zero** whenever the two causal cones do not overlap and
generically O(1) when they do. This is not an empirical fact about the state; it follows from the
isometry conditions of the ansatz. The threshold sits at the cone boundary, computable from
`causal_cone_width` and `scalefactor` alone — `research/tools/MERAKit.jl/src/ternarylayer.jl:110-112`
(b=3, width 2), `binarylayer.jl:110-112` (b=2, width 3), `modifiedbinarylayer.jl:128-130` (b=2,
width 2). No physics enters.

**B predicts.** The same thing.

**Do they differ?** **No.** Both predict a sharp locality threshold at the cone boundary, for the
same reason. §4 grants "tensor-network structure" to A, and causal-cone locality is the canonical
example of it. Confirming it would be a Level 1 validation of the isometry conditions.

**Verdict: DISCARD as posed.** The sub-question that *does* discriminate — "is the locality structure
a property of the state or of the chosen architecture?" — is candidate H, and the reconstruction
observable is a good probe *inside* H. Retained in that role only.

### B. Entanglement-wedge reconstruction

**Measurement.** For a boundary interval A of length ℓ, compare (a) the *network* wedge W_arch(A) —
the set of nodes in A's causal cone, which is architecture-specific — against (b) an operational,
network-free recoverability measure on the state: the conditional mutual information I(X : B|A) for a
localised probe X, or the Petz-map recovery fidelity, computed by free-fermion / exact methods that
never see a tensor network.

**A predicts.** Recoverability is a functional of |ψ⟩. It tracks the CFT's own entropic structure
(RT-like: recoverable when A's entanglement entropy is large enough to purify the probe) and is
**identical for every accurate representation of the same state**. If ternary and binary MERA assign
different wedges to the same interval, at most one of them can coincide with the recoverability
threshold, and the coincidence carries no information.

**B predicts.** Recoverability tracks the *network* wedge more sharply than the entropy prediction
does — and, crucially under B★ clause 1, the wedges must agree across architectures once layer index
is converted to physical scale (b^layer).

**Do they differ?** **Yes** — but only because of the architecture contrast. Ternary MERA (b=3, cone
width 2) and binary MERA (b=2, cone width 3) tile the same interval with different node sets and
different depths (log₃ℓ vs log₂ℓ). B★ demands they agree after conversion; A predicts systematic
disagreement of the geometric prediction with the state-level threshold, in an architecture-tracking
direction. **This is a real fork.**

**Verdict: SURVIVES, rank 2.** Weaknesses recorded honestly: (i) the operational threshold is a state
property, so a B-positive would show only that the network wedge is a *good predictor*, not that it
adds content — clause 3 would still have to be earned separately; (ii) an accurate MPS also
reproduces the state, so the "non-geometric control" cannot make a competing wedge prediction at all,
which makes the control asymmetric.

### C. Modular-flow compatibility

**Measurement.** Locality of modular response for an interval; transport of modular flow through
scale layers; comparison across architectures (`RESEARCH-DIRECTOR.md:565-577`).

**A predicts.** In the continuum the modular Hamiltonian of an interval in a 2D CFT is fixed
(Bisognano–Wichmann / Casini–Huerta); on the lattice its local part is fixed and its non-local tails
are a functional of the state. Everything measurable is CFT data plus lattice non-universal data.

**B predicts.** No sharper statement is available. There is no MERA-specific modular prediction in
this project's records, and I could not construct one that is not either the CHM form or a cone
statement (→ candidate A).

**Do they differ?** **No.** Additionally, the cost is the worst of any candidate: modular flow
requires the full entanglement spectrum of large intervals plus real-time evolution generated by K_A.

**Verdict: DISCARD.**

### D. Conditional mutual information / approximate Markov structure

**Measurement.** I(A:C|B) for tripartitions at varying geometric separation; test whether geometric
separation predicts conditional independence beyond generic critical-state behaviour.

**A predicts.** CMI is a functional of |ψ⟩. For a critical chain it is fixed by the CFT (I(A:C|B) is
a conformal cross-ratio function). Furthermore the natural "non-geometric" control fails to
discriminate: an MPS is an **exact** quantum Markov chain for contiguous tripartitions, so
"approximate Markov structure" does not distinguish a geometric ansatz from a non-geometric one.

**B predicts.** Same functional form; §11-D itself warns "Do not assume a geometric interpretation
merely because conditional mutual information is small."

**Do they differ?** **No.** In-project precedent confirms the class is dead: HYP-2026-012 mapped a
CMI/thread object onto the force and produced α_thread = 0.9097 ± 0.0317 against α_F = 3.9218
(`SIM-2026-013.json`, `crofton_verdict: NOT_SUPPORTED`).

**Verdict: DISCARD standalone.** CMI is retained purely as one of the *measurement instruments* in
candidate B.

### E. Response to defects and inhomogeneous deformations

**Measurement.** Introduce a boundary, defect, interface, or spatially varying coupling (SSD, rainbow
chain, conformal interface); ask whether the inferred geometry deforms predictively.

**A predicts.** For every analytically controlled deformation in this class, the answer is already in
closed form. Sine-square-deformed and rainbow chains are CFTs in a curved background with a known
Weyl factor; conformal interfaces have exactly computed transmission coefficients — the project
already catalogues an example spanning its own three universality classes
(`research/data/papers/PAPER-2026-134.json` `key_claims`: "Exactly computed, parameter-dependent
transmission coefficients on the defect conformal manifold"). Reproducing a closed-form answer is
Level 1 with near-zero counterfactual novelty (§6).

**B predicts.** The same closed-form answer, reached via a bulk picture.

**Do they differ?** **No**, for the solved cases. They could differ for an *unsolved* deformation —
but then the geometric side has no parameter-free prediction either, so there is nothing to compare.

**Verdict: DISCARD at this stage.** §11-E's premise ("A geometry claim becomes stronger if it
predicts the response to a deformation that was not part of the original calibration") is sound, and
this candidate should be revisited **if and only if** GEO-1 finds an architecture-invariant geometric
quantity to deform.

### F. Dynamical and quench tests

**Measurement.** Local quenches, operator spreading, entanglement growth, causal-cone propagation,
transport (`RESEARCH-DIRECTOR.md:602-614`).

**A predicts.** Operator spreading and entanglement growth after a quench in a critical chain are
fixed by the CFT (Calabrese–Cardy) plus the lattice velocity. The MERA "light cone" (one layer per
scale factor b) is ansatz combinatorics. Both are accounted for.

**B predicts.** Same — *except* in one specific out-of-sample form. If ℓ_AdS is redefined
representation-independently by matching the network's own entropy law to the **measured** central
charge (rather than by the heuristic 1/ln χ), then ℓ_AdS ∝ c and the transport time must scale with
c across universality classes. The project holds three classes with c = 1/2, 7/10, 4/5 — a factor
1.6 range. **A predicts the transport time is c-independent** once the Hamiltonian normalisation is
fixed (as §2.1 shows it already is: gaps = Δ, v = 1), and is instead set by the cylinder geometry and
finite-size corrections.

**Do they differ?** **Yes**, sharply, for that one observable: T ∝ c versus T independent of c.

**Verdict: SURVIVES, rank 3.** Caveats recorded: the transport observable is the project's most
fragile (ERRATA E2 retraction of the published 0.72 %; the −31.6 % N = 24 excursion, §2.3; HYP-2026-024
finite-T transport judged artifact-leaning). Porting the Wang–He protocol to TCI and Potts requires
constructing each model's lattice primary operator — real work, and a genuine failure risk.

### G. Curvature or distance reconstruction

**Measurement.** Independently reconstruct distances/curvature from observables that do not share
immediate inputs (`RESEARCH-DIRECTOR.md:616-622`).

**A predicts.** Every distance estimator built from a two-point function reduces to the dimension of
the operator in that function. The project has proven this in its own records: HYP-2026-026 status
SUPPORTED with the finding that the Synge distance carries Δ_σ, giving κ ≈ 0.25 rather than α ≈ 4
(`SIM-2026-031.json` `.results.tiers.exact_16q.kappa_loglog_chord` = 0.2429, verdict "distance is
force-blind").

**B predicts.** Nothing sharper has been produced in three attempts: HYP-2026-014 REFUTED (Crofton
sin profile incompatible with σ data), HYP-2026-022 REFUTED (`SIM-2026-024.json`, α = 0.883),
HYP-2026-012 NOT_SUPPORTED.

**Do they differ?** **No**, and §11-G anticipates exactly this failure: "Do not create several
geometric estimators that all reduce to the same scaling dimensions."

**Verdict: DISCARD.** Three independent refutations already on record. Re-running this class would be
§30 behaviour ("do not repeatedly rediscover that the ruler is twelve inches long").

### H. Network rewiring

**Measurement.** Modify internal connectivity — internal-leg gauge transformations, and architecture
substitution among ternary/binary/modified-binary — while preserving boundary-state fidelity; ask
which observables are stable and which geometric claims change
(`RESEARCH-DIRECTOR.md:624-635`).

**A predicts.** CFT observables (E₀, Δ_σ, Δ_ε, c, α, C_σσε) are stable to within the matching
tolerance, because they are state properties. Every geometric bookkeeping quantity (ℓ_AdS, ξ_MERA,
m_eff, radial coordinate, wedge shape) shifts by factors tracking ln χ, ln b, and cone width. In
particular ℓ_AdS = 1/ln χ is *algebraically* χ-dependent (`paper-prd.tex:64`), so A's prediction here
is not a guess — it is arithmetic.

**B predicts.** Under B★ clause 1, at least one geometric quantity, suitably normalised, is invariant.

**Do they differ?** **Yes, decisively**, and the fork is testable at low cost with code already in the
repo: `research/tools/MERAKit.jl/test/runtests.jl:649` exercises
`meratypes = (ModifiedBinaryMERA, BinaryMERA, TernaryMERA)`, and all three export
`minimize_expectation`, `scalingdimensions`, `densitymatrix_entropies`, `expect`
(`research/tools/MERAKit.jl/src/MERAKit.jl:13-62`). The project has only ever used the ternary one
(`inv-pipelines.md:117`: "Optimises a **ternary** scale-invariant MERA").

**Verdict: SURVIVES, rank 1.** §11-H's own assessment — "This may be one of the cleanest ways to
separate representation quality from geometric content" — is corroborated by everything above, and
§40 lists it as an example of the highest-leverage first slice.

---

## 4. Feasibility of the survivors on this project's real hardware

### 4.1 What the hardware and codebase actually are

| Resource | Reality | Evidence |
|---|---|---|
| Local GPU | RTX 4060, 8 GB | memory `compute_infra` |
| Local CPU limit | scipy hangs after 24 q `eigsh`; use `LinearOperator` and restart Python | memory `feedback_local_memory` |
| RunPod | CPU and GPU pods, standing end-to-end authorisation; `ubuntu:22.04` + `computeType:"CPU"` | `CLAUDE.md` §Simulation Tooling, memory `feedback_runpod_autonomy` |
| MERA engine | MERAKit.jl, Julia **1.8** only, `OPENBLAS_NUM_THREADS=1`, direct-init at target χ | `research/tools/merakit-setup/RUN-MERAKIT.md:1-20` |
| MERA architectures | **all three implemented and unit-tested**: ternary (b=3, cone 2), binary (b=2, cone 3), modified-binary (b=2, cone 2) | `MERAKit.jl/README.md:6`; `test/runtests.jl:649`; `src/{ternary,binary,modifiedbinary}layer.jl:110-130` |
| MERA χ reached | χ = 12 with Z₃ symmetry (Potts, on RunPod); χ = 8 ternary is the shipped demo | `SIM-2026-063.json`; `MERAKit.jl/README.md:23` |
| puMPS | N = 14…56 ladder, vendored (gitignored), local patches documented | `SIM-2026-068.json`; `inv-pipelines.md:65-113` |
| Transport ED | N=16 (dim 6.6e4) fine-dt = 819 s; N=24 (dim 1.7e7) coarse-dt = 29,374 s ≈ 8.2 h; N=24 fine-dt ≈ 7,300 min = infeasible | `SIM-2026-025.json` `.runs.N16.evo_time_s`, `.runs.N24`; `holographic_transport_24q.json` `.total_time_s` |

### 4.2 Rank-1 (H, network rewiring): **feasible now, mostly on the laptop**

- **Slice 0 (analytic).** Zero compute. ~70 % complete in §2 of this artifact.
- **Slice 1 (gauge invariance).** Insert `w w†` on each internal bond of one optimised MERA and
  recompute all observables. Pure tensor algebra on stored tensors; **seconds**, local. MERAKit
  exposes `projectisometric`, `remove_symmetry`, `internalspace` for exactly this manipulation
  (`src/MERAKit.jl:29, 37, 54`).
- **Slice 2 (architecture swap).** Three architectures × χ ∈ {4, 6} on critical Ising with Z₂
  symmetry, multi-seed. Ternary χ=6 is already routine in this repo (`qw_ising_chi6.jl`, 3000 L-BFGS
  iterations). Binary MERA has the widest causal cone of the three (3 vs 2) and is therefore the most
  expensive per iteration; I did not find a documented cost exponent in MERAKit's README, so I flag
  this as the one real timing unknown. Expect hours per (architecture, χ, seed) on CPU; the full
  3 × 2 × 4-seed grid is a RunPod CPU-pod job of order 1 day.
- **Slice 3 (χ ladder).** χ ∈ {4, 6, 8} for the cheapest architecture, to establish the χ-trend of
  every geometric estimator. Adds ~1 day on RunPod.
- **Risk.** The blocking convention differs by architecture (the Ising driver uses `block_size=2` for
  the ternary cone: `qw_ising_chi6.jl:9`). Binary MERA (cone width 3) needs its own blocking, and
  the project already has a documented trap here — the O'Brien–Fendley 3-site blocking episode
  (memory `of_blocking_was_never_wrong`). Mitigation: an exact-diagonalisation pre-gate on each
  blocked Hamiltonian before optimisation, exactly as `qw_of_pregate.py` did.

**Verdict: feasible, days not weeks, mostly existing code.**

### 4.3 Rank-2 (B, wedge recoverability): **feasible, but the analysis is new code**

- Free-fermion CMI / recovery-fidelity computations on the critical TFIM at N ≤ 64 are cheap
  (correlation-matrix methods; the project already uses this formalism — `PAPER-2026-116.json`
  `key_claims[0]` describes the same Pfaffian/Toeplitz–Hankel machinery).
- Extracting the wedge node-sets per architecture is combinatorics on the MERA graph — trivial.
- The expensive part is honest error control on recovery fidelity, which has no precedent in this
  repo. Estimate: 1–2 weeks of new implementation. **Do not start before GEO-1 reports**, because a
  GEO-1 negative on clause 1 removes the premise of the architecture comparison.

### 4.4 Rank-3 (F, c-scaling of transport): **feasible only at small N, with real porting risk**

- Ising N = 12, 16 already done. TCI and Potts have 3 states/site: dim 3^N = 5.3e5 (N=12), 4.8e6
  (N=14), 4.3e7 (N=16). Krylov `expm_multiply` at 4.8e6 is comfortable locally; 4.3e7 needs a RunPod
  CPU pod with ≥ 64 GB, and by the N=24 Ising precedent (8.2 h at dim 1.7e7 on the coarse grid) the
  fine grid at 4.3e7 is likely out of reach.
- Realistic design: N ∈ {10, 12, 14} for all three models, fine-dt, plus the existing Ising N=16.
- **The porting risk is the dominant cost, not the compute.** The protocol needs each model's lattice
  boundary-primary operator; for Ising this was taken from Wang & He (`PAPER-2026-010.json`
  `key_claims[3]`, coefficients 0.635 / −0.026). No analogue exists for TCI or Potts in this repo.
  Construction is possible from the MERA scaling operators but is genuinely new work with a
  meaningful chance of failing to produce a clean dip/reappearance signature at small N.

### 4.5 Explicitly infeasible / rejected on cost

- N = 32 transport (`paper-prd.tex:206` proposes it): dim 4.3e9. Out of reach for exact evolution.
- Modular-flow candidate C at useful interval sizes: full entanglement spectra plus K_A-generated
  evolution. Highest cost of any candidate, zero discriminating power. Rejected twice over.

---

## 5. §28 research decision scores

Scale 1–5, **higher is better in every column** (so "computational cost" scores 5 = cheap, and
"literature saturation" scores 5 = the field is *empty*, i.e. unsaturated). Scored for the four
constructions that survived §3, plus — for calibration — a representative of the class the project
has been running, so the comparison is not self-serving.

| Dimension | **GEO-1** rewiring / ℓ_AdS invariance (H) | **GEO-2** wedge recoverability (B) | **GEO-3** c-scaling of transport (F) | *(calibration)* another CFT-constant measurement |
|---|---|---|---|---|
| Scientific importance | 4 | 4 | 3 | 2 |
| Counterfactual novelty (§6) | 4 | 4 | **5** | **1** |
| Falsifiability | **5** | 4 | 4 | 2 |
| Interpretive discrimination (§4 A vs B) | **5** | 4 | 4 | **1** |
| Methodological novelty | 3 | 4 | 2 | 3 |
| Literature saturation (5 = unsaturated) | 2 | 2 | 3 | **1** |
| Technical feasibility | **5** | 3 | 2 | 4 |
| Computational cost (5 = cheap) | **5** | 3 | 2 | 3 |
| Time to first informative result | **5** | 2 | 2 | 3 |
| Independence from existing data (§7) | 4 | **5** | 4 | 2 |
| Publication value | 3 | 4 | 3 | 2 |
| Reusable infrastructure value | 4 | 4 | 2 | 2 |
| Clarity of failure outcome | **5** | 3 | 3 | 4 |
| **Unweighted total (max 65)** | **54** | **46** | **39** | **30** |

**Score notes (the ones that are not obvious):**

- *GEO-1 counterfactual novelty = 4, not 5.* Slice 0's outcome is close to arithmetic — ℓ_AdS = 1/ln χ
  is χ-dependent by inspection. What is genuinely open is slices 1–3: whether *any* renormalised
  geometric quantity survives, and whether the matched-architecture CFT data really do agree (they
  might not, which would abort the comparison and be informative in its own right).
- *GEO-1 literature saturation = 2.* I scored this **against** my own proposal. Architecture- and
  gauge-dependence of tensor-network geometry is, to the best of my knowledge, an actively worked
  question in the published literature — and §2.5 shows this project has **no catalogued record of
  it**, so I cannot assert otherwise from evidence. The novelty gate (§8) is open and must run before
  any claim of priority. §9 is that plan.
- *GEO-3 counterfactual novelty = 5.* T ∝ c versus T independent of c are both live, and neither is
  fixed by anything currently on record. This is the highest-novelty entry in the table and the
  reason GEO-3 stays on the portfolio despite scoring third overall.
- *GEO-2 independence = 5.* The recoverability side uses free-fermion correlation-matrix methods that
  share no code path, no fitted parameter, and no state-preparation route with the MERA side. That is
  a genuinely "fully independent" comparison under §7 — rare in this repo, where `inv-sims-early.md:522`
  classifies the flagship α = 4 triple as "structurally dependent / primarily a consistency check".
- *Calibration column.* Measuring one more CFT-fixed constant scores 30/65 and 1/5 on both novelty
  and discrimination. That is the quantitative statement of §30's warning, and it is why the ranking
  above should displace, not supplement, further ladder work.

---

## 6. GEO-1 — full design: unit-consistency and representation-invariance of the emergent AdS radius

**One-line statement.** Hold ordinary CFT success approximately fixed, vary the alleged geometry, and
ask whether anything meaningful changes — the §10 logic, applied to the four geometric numbers this
project has actually published.

### 6.1 Scientific question

> Does any quantity the project calls geometric survive (a) an internal-leg gauge transformation,
> (b) a change of MERA architecture, and (c) an increase of bond dimension, once the constructions
> are matched on {E₀ error, Δ_σ, Δ_ε, Δ_T, entropy-fitted c}? And is the transport "AdS radius"
> dimensionally admissible at all in the units the simulation actually uses?

### 6.2 Competing hypotheses, stated so they can lose

- **H_A (efficient representation).** Every geometric quantity is a bookkeeping constant of the
  chosen representation. Specifically: ℓ_AdS tracks 1/ln χ exactly; ξ_MERA and m_eff shift with
  architecture and χ; the transport "radius" is a fitted conversion factor with no χ or b to track,
  and it is unit-inconsistent with the cylinder normalisation. CFT observables are invariant.
- **H_B★ (operational geometry).** There exists a renormalisation of the geometric quantities under
  which at least one of them is invariant across gauge, architecture and χ to within stated
  uncertainty, is not algebraically determined by {χ, b, cone width} or by {c, Δ_i, C_ijk}, and can
  then be used to predict something out-of-sample.
- **H_0 (abort condition, must be checked first).** The three architectures cannot be matched on CFT
  data at accessible χ. If so, the comparison is void and the run reports that instead.

### 6.3 Matched controls (§10) — exactly what is held fixed

Every construction in the grid must pass **all** of these gates before its geometric numbers are
allowed into the comparison. Gates are declared here, before any run.

| Quantity held fixed | Target | Tolerance band | Measured by |
|---|---|---|---|
| Ground-state energy | Ising exact E/site = −4/π | all constructions within [0.5×, 2×] of the grid's median \|E − E_exact\| | `expect(h, m)` (`qw_ising_chi6.jl:17`) |
| Δ_σ | 1/8 | ≤ 2.5 % (project's own ternary χ=6 achieved 1.3 %, `SIM-2026-061.json:13`) | `scalingdimensions(m)` |
| Δ_ε | 1 | ≤ 3.0 % (achieved 1.008–1.020) | `scalingdimensions(m)` |
| Δ_T | 2 | ≤ 3.0 % (achieved 1.9994 at χ=8 TCI, `SIM-2026-052.json`) | `scalingdimensions(m)` |
| Entropy-fitted c | 1/2 | ≤ 3 % | `densitymatrix_entropies(m)` fitted to S = (c/3)ln ℓ + s₀ |
| Selected OPE coefficient C_σσε | 1/2 | ≤ 5 %, **applied only at χ ≥ 8** | PEV route, `qw_ope_pev_z2.jl` |
| Bond dimension | matched pairwise across architectures | exact | construction |
| Symmetry sector | Z₂-symmetric tensors in all constructions | exact | `Z2Space` as in `qw_ising_chi6.jl:12` |
| Computational budget | equal L-BFGS iteration cap and equal seed count per cell | exact; wall time recorded, not equalised | driver |

**Why C_σσε is gated at χ ≥ 8:** the project's own χ=6 spread is 0.128 on a value of 0.5
(`SIM-2026-061.json:15`) — 25 %, far too loose to serve as a matching gate. Using it at χ=6 would be
a control designed not to bite, the §19 failure mode.

**Deliberate omission:** α = 2Δ_T = 4 is *not* a matching gate. It is algebraically Δ_T and would be
double-counting. It is instead a **positive control** (§6.5, C1).

### 6.4 Construction grid

| Axis | Values | Count |
|---|---|---|
| Architecture | TernaryMERA (b=3, cone 2), BinaryMERA (b=2, cone 3), ModifiedBinaryMERA (b=2, cone 2) | 3 |
| Bond dimension χ | 4, 6, 8 | 3 |
| Seeds | 4 independent random inits (direct-init at target χ — the ramp path throws LAPACKException, `RUN-MERAKIT.md`) | 4 |
| Gauge replicas | 8 random internal-leg gauge transformations applied to the *best* cell per architecture | 8 |

Total optimisations: 36, plus 24 zero-cost gauge replicas.

**Model:** critical Ising, Z₂-symmetric, as in `qw_ising_chi6.jl`. One model only. Universality
across models is *not* the question here and would dilute the test (§17 notwithstanding — the
functional dependence being probed is on the representation axis, not the model axis).

### 6.5 Observables

**Geometric observables under test:**

- **O1 — ℓ_AdS^Eq2 ≡ 1/ln χ.** The manuscript's Eq. (2) (`paper-prd.tex:64`). Computed, not measured.
- **O2 — ℓ_AdS^entropy.** *Attempted* extraction of an AdS radius from the MERA's own entropy law.
  **Slice-0 analytic result (see §6.7): this observable does not exist.** In AdS₃, RT gives
  S = Length/4G_N with Length = 2ℓ_AdS ln(ℓ/ε), and Brown–Henneaux gives c = 3ℓ_AdS/2G_N, so
  S = (c/3)ln(ℓ/ε): **ℓ_AdS cancels**, and entropy fixes only the ratio ℓ_AdS/G_N. Recording O2 as
  formally undefined is itself a deliverable — it removes the only route by which ℓ_AdS could have
  been a state property.
- **O3 — ℓ_AdS^transport ≡ 2T/π.** From the chain measurement. Architecture-free by construction:
  1.4253 at N=16, 1.4026 at N=12, 0.9868 at N=24 (derived from `SIM-2026-025.json` and
  `holographic_transport_24q.json`).
- **O4 — ξ_MERA.** The network correlation length feeding the m_eff result
  (`effective_mass_analysis.json` `.comparison_to_measurements.xi_MERA` = 2.154), re-extracted per
  cell by the same procedure.
- **O5 — m_eff ≡ ℓ_AdS/ξ_MERA.** The manuscript's Result 4 (0.6698 vs 0.6931, "3.5 %").
- **O6 — radial dictionary Δz/layer ≡ ℓ_AdS·ln b.** Reported per architecture.

**Positive controls (must be invariant; if they are not, H_0 fires and the run is void):**

- **C1** α = 2Δ_T across all cells.
- **C2** Δ_σ, Δ_ε, entropy-fitted c across all cells.
- **C3** the physical connected correlator C(r) of the represented state at r = 2, 3, 4 — a state
  property, must agree across architectures within the energy-matching tolerance.

**Negative control (must vary; if it does not, the gauge/architecture manipulation was ineffective):**

- **C4** the internal bond spectrum of a fixed layer, before vs after gauge transformation.

**Independent tie-break observable (the one chance for B to win on this run):**

- **O7 — the Synge/chord κ** from `SIM-2026-031.json` (`.results.tiers.exact_16q.kappa_loglog_chord`
  = 0.24289), recomputed from each cell's represented state. Because it is a pure state functional it
  **must** be invariant. It therefore serves as the calibration of what "invariant" looks like at
  this grid's noise level, against which O1/O4/O5's variation is judged.

### 6.6 Prediction table (§36) — registered before execution

Fill-in values are the *predictions*, not results. Δ denotes fractional change relative to the
ternary χ=6 reference cell.

| Observable | H_A predicts | H_B★ predicts | Discriminating? | Registered decision rule |
|---|---|---|---|---|
| C1 α | 4.00 ± 0.10, all cells | same | no (control) | if any cell deviates > 5 %, that cell is dropped, not the hypothesis |
| C2 Δ_σ, Δ_ε, c | invariant within §6.3 bands | same | no (control) | if unmatched at all χ → **H_0 fires, run reported as void** |
| C3 C(r) | invariant to ≲ energy-error scale | same | no (control) | as C2 |
| C4 bond spectrum | changes under gauge | changes | no (control) | if unchanged → gauge transform was trivial; regenerate |
| O7 Synge κ | invariant, ≈ 0.243 ± noise | invariant | no (calibrator) | sets the grid's invariance noise floor σ_inv |
| **O1 ℓ_AdS^Eq2** | **exactly 1/ln χ**: 0.7213 (χ=4), 0.5581 (χ=6), 0.4809 (χ=8) — a **50 % swing** across the grid, identical in all three architectures | **invariant**, within σ_inv | **YES** | any χ-dependence beyond σ_inv ⇒ O1 is a representation parameter |
| **O4 ξ_MERA** | varies with architecture and χ by ≳ 20 % | invariant within σ_inv | **YES** | as above |
| **O5 m_eff** | varies; in particular the "3.5 % agreement" is not reproduced outside (ternary-adjacent, χ=2-normalised) settings | invariant within 5 % and continues to sit near ln 2 | **YES** | if m_eff lands within 5 % of 0.693 in ≥ 7 of 9 (architecture, χ) cells, **that is a genuine B-positive** and must be reported as such |
| **O6 Δz/layer** | ∝ ln b: ratio ternary : binary = ln3 : ln2 = 1.585 exactly | the *total* radial distance to scale r, ℓ_AdS·ln r, is b-invariant | partly | b-invariance of the *total* is automatic and is **not** evidence for B; only the χ-behaviour discriminates |
| **O3 ℓ_AdS^transport** | no χ, no b to track; equals 2T/π and drifts with N (1.4026 / 1.4253 / 0.9868 at N = 12/16/24) | should equal O1 at the χ actually used | **YES** | O1 takes three values (1.4427, 0.9102, 0.4024) for the three χ in the manuscript; O3 takes one per N. They cannot all agree |
| **Slice 0 unit consistency** | ℓ_AdS cancels from the null-geodesic time in cylinder units; ℓ-free prediction is π/2 or π | ℓ_AdS legitimately appears | **YES** | §2.1 already indicates the H_A branch; an independent re-derivation is required before this is asserted in print |

### 6.7 Slice structure and computational plan

| Slice | Content | Compute | Wall estimate | Informative on its own? |
|---|---|---|---|---|
| **0** | Analytic: (a) re-derive whether ℓ_AdS survives in cylinder units; (b) prove O2 is formally undefined (ℓ_AdS cancels in RT + Brown–Henneaux); (c) tabulate O1 across the manuscript's three χ | **none** | hours | **Yes — decisive on its own for O1/O2** |
| **1** | Gauge orbit: 8 random internal-leg transformations on one optimised ternary χ=6 MERA; recompute O1, O4, O5, C1–C4, O7 | local, seconds | < 1 h | Yes — a §12 "reconstruction killer" outcome |
| **2** | Architecture swap at χ = 6: ternary / binary / modified-binary, 4 seeds, matched gates | CPU; binary is the costliest (cone width 3) | 1–2 days RunPod CPU | Yes |
| **3** | χ ladder 4/6/8 for all three architectures | CPU | +1–2 days RunPod CPU | Yes |
| **4** | Write-up: structured SIM record + a `research/data/theory/` record (the tier is currently **empty**, §14 — this experiment is the natural first occupant) | — | 1 day | — |

**Environment (pinned, per `RUN-MERAKIT.md`):** Julia 1.8.5 via `julia +1.8`,
`JULIA_DEPOT_PATH=C:\Users\jonca\.julia`, `HOME=D:\quantum-worldline\research\tools\juliahome`,
`OPENBLAS_NUM_THREADS=1`, launched from inside the MERAKit.jl directory with an explicit `cd` in the
same command (and again for any backgrounded job — `NEXT-SESSION.md`, "Shell gotcha").

**Reproducibility requirements (§21), declared in advance because P1 currently fails them.**
`inv-pipelines.md:153-176` establishes that *every* MERAKit SIM record cites log files that are not
in the repository, and that `merakit-setup/` contains "only drivers and design docs — zero result
files". GEO-1 must not repeat this. Required, non-negotiable outputs, all **tracked**:

1. per-cell JSON with E, all scaling dimensions, entropies, seed, iteration count, wall time;
2. the serialised MERA tensors (`pseudoserialize`, `src/MERAKit.jl:52`) for at least the best cell per
   architecture;
3. the driver script mirrored into `research/tools/merakit-setup/` **before** commit (the gitignore
   boundary rule in `CLAUDE.md`);
4. Manifest.toml hash of the MERAKit revision used.

### 6.8 Independence analysis (§7)

| Element | O1 side (network) | O3 side (chain transport) | Shared |
|---|---|---|---|
| Raw data | optimised MERA tensors | statevector evolution of H_boundary | none |
| Theoretical assumptions | MERA–AdS dictionary; entropy-per-bond heuristic | AdS₃ global geometry; null-geodesic condition | the *identification* of MERA geometry with AdS₃ — this is the shared assumption, and it is the thing under test |
| Fitted parameters | none in O1 (it is 1/ln χ) | ℓ_AdS enters as the single free multiplicative factor | — |
| Exact CFT identities | Δ_σ, Δ_ε used only as matching gates | gaps = Δ (verified §2.1) | the Ising spectrum |
| Numerical code | MERAKit.jl / Julia | scipy sparse / Python | **none** |
| State preparation | variational optimisation | exact `eigsh` ground state of a different Hamiltonian | none |

**Classification:** the O1 ↔ O3 comparison is **structurally dependent through a single shared
interpretive assumption** (that the network's radial coordinate is AdS₃'s), and otherwise fully
independent in data, code and state preparation. That is unusually clean by this repo's standards —
compare `inv-sims-early.md:522`, where the flagship α = 4 "three consistent evaluations" are
classified "structurally dependent / primarily a consistency check". GEO-1's comparison is a genuine
test of the shared assumption rather than a re-derivation of it.

**Independence caveat I must record against my own design:** slices 1–3 all use MERAKit. A MERAKit
implementation bug that affects all three architectures identically would not be caught. Mitigation:
the C1–C3 controls are known-answer checks against exact CFT values, and the O7 calibrator is
computed from the *represented state*, not from the network. Full independence would need a second
MERA implementation, which the project does not have and which I am not proposing to build.

### 6.9 Named killers (§12)

Declared before execution, in both directions.

- **K1 — Geometry killer (kills H_B★).** If O1, O4 and O5 each move by more than max(3σ_inv, 10 %)
  when χ or architecture changes, while C1–C3 stay inside their matching bands, then the project's
  geometric numbers are representation parameters. Consequence: the emergent-geometry framing must be
  demoted from Result to Interpretation throughout, and the ℓ_AdS-dependent transport claim must be
  restated without the ℓ_AdS factor or withdrawn.
- **K2 — Unit killer (kills the transport anchor specifically).** If an independent re-derivation
  confirms §2.1 — that the boundary clock is CFT cylinder time with v = 1, so the null-geodesic time
  is ℓ-free — then Result 2's agreement is an artifact of a free factor. Consequence: a correction
  to the PRD manuscript (accession DV13971) and a new ERRATA entry.
- **K3 — Advocate's killer (kills H_A for this observable set, i.e. **B wins**).** If m_eff lands
  within 5 % of ln 2 in ≥ 7 of the 9 (architecture, χ) cells while O1 varies by 50 % across the same
  cells, then something architecture-invariant is being measured that is *not* 1/ln χ, and B★
  clauses 1–2 are satisfied. This is a live possibility and must be reported loudly if it happens; it
  would immediately promote GEO-3 (out-of-sample prediction, clause 3) to the top of the portfolio.
- **K4 — Void condition (H_0).** If the three architectures cannot be matched on C2 at any χ ≤ 8, the
  experiment reports "not decidable at accessible bond dimension" and stops. That is a legitimate
  §31 stop condition, not a failure.

### 6.10 Interpretation rules, fixed in advance (§36)

1. **Invariance is judged against σ_inv**, the spread of the O7 calibrator across the same cells — not
   against a tolerance chosen after seeing O1/O4/O5.
2. **Agreement of a b-invariant combination is not evidence for B.** ℓ_AdS·ln r is b-invariant by
   construction; only χ-behaviour and gauge-behaviour discriminate. This rule exists because the
   b-invariant combination is the one most likely to be quoted as a success.
3. **No post-hoc renormalisation.** If O1/O4/O5 vary, the response may not be "define a new
   normalisation that removes the variation" unless that normalisation is derived independently and
   then tested on a cell held out from the derivation (§18).
4. **A single-cell agreement is not a result** (§17). Any B-positive requires ≥ 7 of 9 cells.
5. **The N-dependence of O3 is part of the result, not a nuisance.** The three transport values
   (§2.3) must be reported together in any statement about ℓ_AdS^transport; quoting N = 16 alone is
   prohibited.
6. **Level assignment is fixed now** (§5): a K1 outcome is a **Level 4 discriminating result**
   (negative direction — "geometric observables reduce to representation parameters"); a K3 outcome
   is Level 4 positive; a K4 outcome is Level 2 at best (a statement about method reach). Slice 0
   alone, if K2 confirms, is **Level 3** — a correction to a published correspondence, not merely a
   validation.
7. **Novelty language is banned** in the write-up until §9's literature gate has run and its results
   are recorded in `research/data/papers/`.

### 6.11 First informative milestone and stop conditions

- **First informative milestone:** end of slice 0 + slice 1 — hours to one day, no cluster. Either the
  gauge orbit already moves a "geometric" number (K1 evidence at essentially zero cost), or it does
  not, which makes slice 2 worth its budget.
- **Stop conditions (§31):** (i) K4 void; (ii) slice 1 already produces K1 at >10σ_inv, in which case
  slices 2–3 shrink to a confirmation at one extra architecture rather than the full grid; (iii) if
  binary-MERA optimisation cannot reach the C2 band in 2 days of RunPod CPU, drop BinaryMERA and run
  ternary vs modified-binary only (b=3 vs b=2 is retained, which is the axis that matters).

---

## 7. Ranks 2 and 3 — designs in outline

These are sketched, not fully specified, because §40 says not to begin with the largest possible
implementation and because both are conditional on GEO-1's outcome.

### 7.1 GEO-2 — architecture-matched entanglement-wedge recoverability (candidate B)

- **Question.** For a boundary interval A, does the operational recoverability of a localised probe
  track the *network* wedge, and do the wedges of different architectures agree once layer index is
  converted to physical scale?
- **Why it can discriminate.** Ternary (b=3, cone 2) and binary (b=2, cone 3) MERA assign different
  node sets and different depths (log₃ℓ vs log₂ℓ) to the *same* interval of the *same* state. At most
  one can coincide with the state's recoverability threshold unless the conversion works.
- **Observables.** Wedge node-sets (combinatorial, per architecture); recoverability via CMI
  I(X : Ā|A) and/or Petz recovery fidelity computed by free-fermion correlation-matrix methods that
  never touch a tensor network.
- **Independence.** The strongest in the portfolio: no shared code path, no shared fitted parameter,
  no shared state preparation (scored 5/5 in §5).
- **Killer.** If the recoverability threshold sits at the same physical scale regardless of which
  architecture's wedge you consult, the wedge adds nothing over the entropy prediction; if it tracks
  whichever architecture you happen to have built, the wedge is representation-dependent. Both
  outcomes support H_A; only a sharp, architecture-independent, *entropy-inconsistent* threshold
  supports B.
- **Precondition.** Do not start until GEO-1 slices 0–2 report. A K1 outcome there makes GEO-2's
  premise (that some geometric structure is invariant) already refuted.

### 7.2 GEO-3 — c-scaling of the transport time across the universality ladder (candidate F)

- **Question.** With the Hamiltonian normalisation fixed so that gaps equal scaling dimensions
  (verified for Ising in §2.1, must be re-verified per model), is the transport time c-dependent?
- **The fork.** H_B★-with-RT-normalisation implies ℓ_AdS ∝ c, hence T ∝ c: a factor 1.6 between
  Ising (c = 1/2) and Potts (c = 4/5), with TCI (c = 7/10) in between. H_A implies T is set by the
  cylinder geometry and finite-size corrections, hence **c-independent** at fixed N and normalisation.
- **Why it is the highest-novelty item in the table.** Neither outcome is fixed by anything on record.
  Scored 5/5 on counterfactual novelty in §5.
- **Cost and risk.** N ∈ {10, 12, 14} for three models, fine-dt Krylov; dominant cost is *not*
  compute but constructing each model's lattice boundary-primary operator, which exists only for
  Ising (`PAPER-2026-010.json` `key_claims[3]`). Realistic chance the dip/reappearance signature is
  not resolvable at N ≤ 14 for the 3-state models.
- **Mandatory control given §2.3.** The N-dependence must be mapped for every model before any
  c-comparison; comparing three models at one N each would repeat the N = 16 single-point failure.
- **Precondition.** Requires a K3 (B-positive) or at least a K1-negative-with-surviving-quantity
  outcome from GEO-1. If K1 fires cleanly, GEO-3 has nothing left to measure and should be retired
  under §31.

---

## 8. What would make me concede, and what would vindicate B

Stated symmetrically, because an advocate who cannot say what would change his mind is not doing
science (§27: "Agents should disagree productively").

### 8.1 I concede Hypothesis A on this observable set if:

1. K1 fires — O1, O4, O5 all move with χ and architecture beyond the O7-calibrated noise floor; **or**
2. K2 confirms — the boundary clock is CFT cylinder time, so ℓ_AdS is dimensionally spurious in the
   transport prediction; **or**
3. slice 1 alone shows a "geometric" number moving under a pure internal-leg gauge transformation,
   which is the cheapest and most damning of all outcomes (§12, "Reconstruction killer").

On the evidence assembled in §2, **I currently expect (1) and (2) both to fire.** Saying so in advance
is the point of §36.

### 8.2 Hypothesis B is vindicated — and I would say so loudly — if:

1. K3 fires: an architecture- and χ-invariant m_eff (or any other geometric quantity) at ≥ 7 of 9
   cells, while O1 swings 50 % across the same cells; **and then**
2. that invariant quantity makes a correct parameter-free out-of-sample prediction (clause 3 of B★) —
   GEO-3's c-scaling is the designated test; **and**
3. the §9 literature gate confirms the quantity is not a known reparameterisation of CFT data.

All three are required. Item 1 alone would be interesting and insufficient; the project's history
(HYP-014, HYP-022, HYP-012, HYP-024 — four geometry-adjacent hypotheses refuted or judged artifact)
is a history of item-1-style agreements that did not survive.

### 8.3 The honest prior

The strongest *published* geometric content in this repo is not a geometry result at all. It is the
methodological work: the Z₂/Z₃-symmetric optimisation that converted a "dense basin lottery" into
8/8 clean basins (`SIM-2026-061.json:12`, `SIM-2026-062.json`), the biorthogonal Koo–Saleur
extraction (`SIM-2026-071.json`), and the two-phase ALM + projection optimiser
(`SIM-2026-008b/008c`). Those are Level 2 contributions that survive deletion of the word
"holographic" (§24's test). The geometry claims mostly do not. As the advocate, I record that this is
the base rate my proposal has to beat.

---

## 9. §8 novelty gate — the search plan that must run before any geometry claim

None of this has been done for the geometry line (§2.5). Required before the word "novel", "first" or
"to our knowledge" appears in any GEO-1/2/3 output. Per `CLAUDE.md`, use the arXiv **export API via
WebFetch** (the paper-search MCP is query-blind), **sequentially, spaced 3–5 s** (scan #17's 429
burst-block lesson), and dedup with `grep -l "<arxiv-id>" research/data/papers/*.json` before
assigning PAPER IDs.

| # | Query axis | Terms | What a hit would decide |
|---|---|---|---|
| 1 | Architecture-dependence of TN geometry | "MERA geometry", "geometric interpretation of MERA", "hyperinvariant tensor network", "branching MERA" | whether GEO-1's question is already answered in print |
| 2 | Gauge-dependence / state-vs-representation | "tensor network gauge invariance", "gauge freedom MERA", "representation dependence tensor network" | whether slice 1 is prior art |
| 3 | AdS radius from a tensor network | "AdS radius tensor network", "emergent AdS radius MERA", "bond dimension AdS radius" | whether ℓ_AdS = 1/ln χ has a derivation, and whose |
| 4 | Causal cone as entanglement wedge | "causal cone entanglement wedge MERA", "bulk reconstruction MERA" | GEO-2 prior art |
| 5 | Holographic transport / null geodesic on a chain | "holographic transportation spin chain", "null geodesic transport tensor network" | whether the ℓ-cancellation of §2.1 is known |
| 6 | Kinematic space TN | "kinematic space tensor network", "integral geometry MERA" | already partially catalogued (`PAPER-2026-044`, `PAPER-2026-131`) |
| 7 | Author trails | Vidal; Evenbly; Swingle; Czech; Milsted; Qi; Pastawski/Preskill; Bény | the nearest-prior-work question §8 requires answering by name |

**Note on attribution defects already found by phase 1**, which this gate must also fix:
`inv-manuscript-claims.md:294` (DEF-13) records that ℓ_AdS = 1/ln χ is cited in the manuscript to
`KimSwingle2017` while the project's own record attributes it to Sahay/Lukin/Cotler
(`PAPER-2026-009.json` `key_claims[2]`). Since §2.1–2.2 make this equation load-bearing and
questionable, establishing who actually derived it, under what assumptions, is now a priority rather
than a citation-hygiene item.

---

## 10. UNVERIFIED

Stated explicitly per the protocol; silence is not a pass.

1. **The ℓ_AdS-cancellation argument in §2.1 is analytic, not proven here.** The *spectral* fact
   (gaps = Ising scaling dimensions, table in §2.1) is verified numerically and reproducible from the
   code given. The *inference* — that the boundary clock is therefore CFT cylinder time in which the
   null-geodesic crossing time is ℓ-independent — is a convention argument I did not derive from the
   Wang–He or Bohra–Sivaramakrishnan sources, neither of which I opened in this pass. It is GEO-1
   slice 0's first task, and it must be checked by someone other than me before it is asserted in
   print or in a PRD correction.
2. **I did not verify the claimed origin of Eq. (2), ℓ_AdS = 1/ln χ.** I verified that the manuscript
   asserts it and that the project's records disagree about who to credit (DEF-13). I did not open
   the cited works. Whether the equation is a heuristic bound (each bond carrying its maximal log χ
   of entropy) or a matched identity materially changes how badly §2.2's three-values problem bites.
3. **Cost scaling of BinaryMERA vs TernaryMERA in MERAKit.** I confirmed all three architectures are
   implemented and unit-tested (`test/runtests.jl:649`) and that binary has the widest causal cone
   (3 vs 2), but I found **no documented cost exponent** in the README or docs and did not benchmark
   one. GEO-1 slice 2's wall-time estimate (1–2 days) is therefore an engineering guess, not a
   measurement. It is the largest scheduling risk in the design.
4. **Whether the three architectures can actually be matched on Δ_σ, Δ_ε, c at χ ≤ 8.** This is the
   H_0 abort condition and it is genuinely unknown. Modified-binary MERA in particular has a
   different blocking structure and I did not check that the project's `block_size=2` Ising
   Hamiltonian construction (`qw_ising_chi6.jl:9`) transfers to it.
5. **ξ_MERA's extraction procedure.** `effective_mass_analysis.json` reports ξ_MERA = 2.154 and the
   phase-1 auditor separately flagged that its provenance is unscripted (`inv-sims-early.md` §8
   UNVERIFIED item 3). I did not locate a script that computes it, so GEO-1's O4 currently has a
   defined *target* but no verified *reference implementation*. Reconstructing it is a prerequisite
   for slice 2, and it may turn out that ξ_MERA is a 2-point fit (dr = 1, 2), as
   `effective_mass_analysis.json` `.resolution.explanation` states — in which case O4 and O5 carry
   uncertainties large enough to weaken K1 and K3 alike.
6. **The look-elsewhere claim in §2.1 R4 is illustrative, not a computed false-alarm rate.** I checked
   that 5π/7 = 2.2440 and π/√2 = 2.2214 are closer to the measurement than (π/2)/ln 2 = 2.2662. I did
   not enumerate a reference class of "simple constants" or compute a probability. The point stands
   qualitatively (§17) and should not be quoted as a statistical statement.
7. **§2.5 is an absence-of-record finding only.** I verified by `grep -ril` over
   `research/data/papers/*.json` that no records exist for the listed terms. I did **not** read any of
   the uncatalogued works and make no claim about their content, their existence in the literature, or
   whether they would confirm or contradict anything here.
8. **GEO-3's premise that the Wang–He normalisation generalises.** I verified gaps = Δ for the Ising
   H_boundary at N = 12 and 16. Whether an analogous normalisation exists and is achievable for the
   O'Brien–Fendley TCI chain and the 3-state Potts chain is unchecked, and it is the load-bearing
   assumption of the whole c-scaling comparison.
9. **I did not evaluate whether GEO-1's outcome obliges a correction to the in-flight PRD submission.**
   K2 would touch Result 2 of a manuscript currently with editors (accession DV13971). That is an
   editorial and ethical judgement for the user, not a technical one for this audit; I flag it, I do
   not decide it.
10. **Petz-map / recovery-fidelity feasibility for GEO-2** is asserted from the free-fermion structure
    of the critical TFIM, not from a prototype. No such computation exists in this repo.

---

## 11. Compact conclusion

- §11's candidates A, C, D, E and G **do not discriminate** between Hypotheses A and B and are
  discarded with reasons.
- H (rewiring) discriminates decisively and is cheap; B (entanglement wedge) discriminates only in
  its architecture-contrast form; F (dynamics) discriminates only through the c-scaling of transport.
- The strongest operational version of the emergent-geometry claim is **B★** (§1.4): invariance +
  non-derivability + out-of-sample prediction. All three clauses are required, and **no observable
  currently in this project satisfies even the first two.**
- The top-ranked experiment is **GEO-1**, whose analytic slice already indicates that the project's
  flagship geometric number carries a factor that should cancel, and whose gauge slice costs under an
  hour.
- The advocate's honest prior is that GEO-1 returns a negative. The North Star
  (`RESEARCH-DIRECTOR.md:1643`) says that outcome is worth as much as the positive, and — unlike the
  ladder work — it is an outcome the project does not already know.
