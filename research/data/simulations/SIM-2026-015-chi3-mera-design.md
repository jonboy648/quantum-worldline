# SIM-2026-015: chi=3 MERA Optimizer Design for 8-Site TFIM

**Date:** 2026-04-01
**Hypothesis:** HYP-2026-009 — Bond dimension chi=2 -> chi=3 RTN phase boundary
**Predecessor:** SIM-2026-008c (chi=2, ALM+projection, 3.33% error at 24q)
**Scope:** Design document only — architecture and algorithm, not running implementation

---

## 1. Motivation and Context

The chi=2 MERA converges to 1.12% at 8q and 3.33% at 24q. SIM-2026-009 diagnosed the 24q
ground state as GHZ-like with flat two-point correlations, not the critical power-law
C(r) ~ r^{-1/4} expected at the TFIM critical point. The root cause is architectural:
chi=2 cannot simultaneously enforce Z2, minimize energy, AND reproduce the entanglement
structure of the critical ground state.

chi=3 provides three concrete improvements:
1. The bond dimension directly controls how much entanglement can be distributed across
   causal cuts in the MERA. chi=2 allows 1 ebit/cut; chi=3 allows log2(3) ~ 1.58 ebits/cut.
2. The MERA isometry at chi=3 acts on a chi^2 = 9-dimensional input space, capturing
   short-range correlations across 3 sites vs. chi^2 = 4 at chi=2.
3. The additional freedom enables the optimizer to find states in the correct entanglement
   universality class, which chi=2 provably cannot represent for the critical TFIM.

The expected phase transition signature (HYP-2026-009): a sudden jump in the von Neumann
entropy of the top-layer density matrix S_top, and a change in the scaling of bipartite
entanglement S(l) vs. block size l, from the chi=2 plateau at S_max = log(2) to a new
plateau near S_max = log(3). The two-point function should begin to show power-law decay
consistent with c=1/2 CFT once chi is sufficient.

---

## 2. MERA Layer Structure for 8 Sites at chi=3

### 2.1 Layer Count

8 sites -> 2 MERA layers (same as chi=2 for 8 sites):
- Layer 1 (fine): 8 sites -> 4 sites (4 disentanglers, 4 isometries)
- Layer 2 (coarse): 4 sites -> 2 sites (2 disentanglers, 2 isometries)
- Top tensor: 2-site density matrix at chi=3 bond dimension

At chi=2, 3 layers were used to fully coarse-grain 8 sites down to 1 effective site.
At chi=3, 2 layers suffice because each layer retains more information per kept index.
The top tensor at chi=3 is a 3x3 = 9-dim space (vs. 2x2 = 4-dim at chi=2), allowing
the top-level state to be richer without adding a third layer.

### 2.2 Index Dimensions at Each Layer

Physical dimension: d = 2 (qubit)
chi = 3 (virtual bond dimension)

**Layer 1 input:** physical legs, dim = 2 each
  - Disentangler u1: acts on 4 physical qubits (2 pairs), shape (2,2,2,2) -> (2,2,2,2)
    After disentangling, two pairs of legs have chi=2 physical dimension.
  - Isometry w1: coarse-grains 2 physical legs into 1 virtual leg of dim chi=3
    Shape: (2, 2, 3) — maps C^2 x C^2 -> C^3
    Isometry constraint: w1^dag @ w1 = I_{3x3}  (3x3 identity)

**Layer 2 input:** virtual legs from Layer 1, dim = 3 each
  - Disentangler u2: acts on 4 virtual legs (2 pairs), shape (3,3,3,3) -> (3,3,3,3)
    Unitarity constraint: u2 is a unitary on C^9 x C^9 (9-dim -> 9-dim)
    Actually: u2 acts on 2 virtual legs: (3,3) -> (3,3), shape (3,3,3,3) as a map
    C^{3x3} -> C^{3x3}, i.e., a 9x9 unitary matrix with 81 real parameters (minus 9
    for phases on columns = 72 independent real params, or 9^2 - 9 = 72 for U(9)/U(1)^9).
    In practice: parameterize as exp(iA) where A is 9x9 skew-Hermitian, 81 real params.
  - Isometry w2: coarse-grains 2 virtual legs of dim 3 into 1 virtual leg of dim 3
    Shape: (3, 3, 3) — maps C^3 x C^3 -> C^3
    Isometry constraint: w2^dag @ w2 = I_{3x3}
    Real parameters: 3x9 - 3x3 = 27 - 9 = 18 independent real params (Stiefel manifold St(3,9))

**Top tensor:**
  - 2 virtual legs of dim 3 remaining after Layer 2
  - Density matrix rho_top: shape (3, 3, 3, 3) = 3x3 density matrix on C^9
  - Can parameterize as |psi_top><psi_top| for pure state: dim-9 normalized vector = 8 real params

### 2.3 Summary of Tensor Shapes

| Tensor | Shape | Constraint | Independent Params |
|--------|-------|------------|-------------------|
| u1 (disentangler, Layer 1) | (2,2,2,2) as 4x4 unitary | U(4), 4x4 unitary | 16 (U(4)/phases: 12 real) |
| w1 (isometry, Layer 1) | (2,2,3) = (4,3) matrix | w1^T w1* = I_3 | 12 (St(3,4): 4*3 - 3*4/2... see note) |
| u2 (disentangler, Layer 2) | (3,3,3,3) as 9x9 unitary | U(9) | 81 (or 72 reduced) |
| w2 (isometry, Layer 2) | (3,3,3) = (9,3) matrix | w2^T w2* = I_3 | 24 (St(3,9)) |
| psi_top (top tensor) | (9,) normalized | unit norm | 16 real (normalized C^9 up to phase) |

Note on isometry count: The Stiefel manifold St(k,n) of k-frames in R^n has dimension k*n - k*(k+1)/2.
For complex: St(k,n)_C has real dimension 2*k*n - k^2.
w1: St(3,4)_C: 2*3*4 - 9 = 24 - 9 = 15 real params
w2: St(3,9)_C: 2*3*9 - 9 = 54 - 9 = 45 real params

For the disentanglers (full unitaries):
u1: U(4): 16 real params
u2: U(9): 81 real params

**Total parameters for 2-layer chi=3 MERA on 8 sites:**
- Layer 1: 4 disentanglers u1 (4x16) + 4 isometries w1 (4x15) = 64 + 60 = 124
- Layer 2: 2 disentanglers u2 (2x81) + 2 isometries w2 (2x45) = 162 + 90 = 252
- Top tensor: 16
- **Total: 392 real parameters**

Compare to chi=2 at 8 sites: ~84 parameters (from SIM-2026-008a: 84 params, 3 layers).
chi=3 has ~4.7x more parameters for 8 sites with only 2 layers.

---

## 3. Z2 Symmetry Enforcement at chi=3

### 3.1 The Z2 Constraint in Tensor Notation

At chi=2, the two approaches were:
- **ALM (Augmented Lagrangian Method):** Add penalty (1-<P>)/2 term with increasing mu
- **Z2 projection:** Post-multiply by symmetrizer (I + P)/2 at each gradient step

At chi=3, both approaches generalize, but the projection approach is cleaner.

### 3.2 Z2-Equivariant Tensors at chi=3

The most elegant solution is to build Z2 equivariance directly into the tensor structure.

The Z2 symmetry P = prod(X_i) acts on the physical qubits. A MERA with Z2 equivariant
tensors automatically preserves <P>=+1 by construction, no penalty needed.

For a Z2-equivariant MERA, each tensor must commute with the symmetry action:
- On physical legs: P acts as X (Pauli X on qubits, rep {0,1} mod 2)
- On virtual legs: we assign each virtual index a Z2 charge in {0, 1}

For chi=3: the virtual bond decomposes as chi=3 = 2 + 1, meaning 2 indices in Z2-charge
sector 0 (even) and 1 index in Z2-charge sector 1 (odd). This forces the isometry to
map between Z2-charge-consistent sectors.

**Practical implementation for the 8-site TFIM:**
Use the ALM+projection two-phase method from SIM-2026-008c, extended to chi=3:

Phase 1 (ALM): Optimize with Z2 penalty term:
  L(theta) = E(theta) + mu * g(theta) + (rho/2) * g(theta)^2
  where g(theta) = (1 - <P(theta)>) / 2

Phase 2 (Projection): After ALM forces <P>~1, refine with explicit projection:
  At each gradient step: sv -> (sv + P*sv) / ||sv + P*sv||

The Phase 2 projection is still O(2^N) for an N-qubit system via the bit-flip trick:
  sv_plus[i] = sv[i] + sv[i XOR (2^N - 1)]
  (Flip all N bits = action of X^{otimes N})

This scales identically to chi=2 — the chi increase only affects the number of parameters,
not the projection operation on the full 2^N statevector.

### 3.3 ALM Schedule Adaptation

Chi=3 has 392 parameters vs. 84 at chi=2. The landscape is higher-dimensional but also
richer (fewer local minima due to more expressive ansatz). Recommended schedule:

| Phase | Method | Rounds | Evals/Round | Total Evals |
|-------|--------|--------|-------------|-------------|
| 1 (ALM) | L-BFGS-B | 10 | 5000 | 50,000 |
| 2 (Projection) | L-BFGS-B | 1 | 30,000 | 30,000 |
| Total | | | | ~80,000 |

Compare to chi=2 SIM-2026-008b (8q): 8 rounds x 3000 + 5000 = ~29,000 evals.
~3x more evals needed due to ~4.7x more parameters.

---

## 4. Tensor Parameterization

### 4.1 Representing Isometries (Stiefel Manifold)

At chi=2, isometries were implicitly parameterized via rotation angles (Ry+Rz+CX).
At chi=3, we need to parameterize St(3,9)_C — 3 orthonormal columns in C^9.

**Recommended: Cayley/Procrustes parameterization**
Given a base point W_0 on St(3,9), nearby points can be written as:
  W = (I + A/2)^{-1} (I - A/2) W_0
where A is a 9x9 skew-Hermitian matrix (45 real params after constraint A^dag = -A).

**Alternative: QR decomposition approach (simpler for optimization)**
Parameterize a 9x3 complex matrix M (free, 54 real params), then:
  W = QR_decomp(M)[:, :3]  (first 3 columns of Q from QR of M)
This gives a valid isometry and differentiable w.r.t. M. More parameters than needed
but gradient methods handle the redundancy via null-space projections.

**Recommended for implementation:** Use QR parameterization with 9x3 complex matrix M.
Gradient w.r.t. M, then project back to Q via QR. SciPy L-BFGS-B works in real vector;
represent each complex number as (real, imag) pair -> 54 real params per isometry.

### 4.2 Representing Disentanglers (Unitary Group)

**Recommended: Skew-Hermitian exponent (matrix exponential parameterization)**

For U(4) (Layer 1 disentangler):
  u = expm(iA) where A is 4x4 Hermitian, 16 real params
  Flatten A to 16 real params, then reconstruct via scipy.linalg.expm(1j * reshape(params, (4,4)))

For U(9) (Layer 2 disentangler):
  u = expm(iA) where A is 9x9 Hermitian, 81 real params

Matrix exponential is differentiable; autograd/JAX handles it naturally. For scipy L-BFGS-B,
compute numerical gradients (or use JAX with jax.scipy.linalg.expm).

**Alternative for chi=2 compatibility:** Keep the gate-based parameterization (Rx, Rxx, Ryy, Rzz)
but for chi=3 this requires qutrit gates, which is non-standard. The matrix exponential
approach is cleaner for the pure classical simulation.

### 4.3 Statevector Contraction Order

For 8 sites, the full statevector lives in C^{2^8} = C^{256}. At each optimization step:

1. Build isometries W1[layer1_pairs], W2[layer2_pairs] from parameters
2. Build disentanglers U1, U2 from parameters
3. Contract MERA from bottom (physical) to top (virtual):
   - Apply U1 to pairs (0,1), (2,3), (4,5), (6,7) on 256-dim statevector
   - Apply W1 (as truncation): contract pairs -> chi=3 virtual indices
     After Layer 1: effective state is in C^{3^4} = C^{81}
   - Apply U2 to pairs of chi=3 virtual indices
     After U2: still C^{81}
   - Apply W2: contract pairs -> C^{3^2} = C^9
   - Top state: psi_top in C^9

4. Energy: E = <psi_top | H_eff | psi_top> where H_eff is the effective Hamiltonian
   obtained by contracting the full Hamiltonian with the MERA tensors bottom-up.

**Computational note:** For 8 sites, contracting via the full 256-dim statevector and
then reducing is straightforward. Alternatively, work in the reduced space throughout:
after Layer 1, the system lives in C^81 (9-dim x 9-dim for 4 effective sites), then
C^9 after Layer 2. This is much cheaper: energy evaluation at O(9^2) vs O(256).

**Recommended hybrid approach:**
- For Z2 parity projection: work in full C^256 (projection is O(256) via bit flip)
- For energy evaluation: work in reduced C^9 after full tensor contraction
- Gradient: use numerical finite differences on the parameter vector (L-BFGS-B handles this)
  or JAX autodiff for exact gradients

---

## 5. Observable Extraction

### 5.1 Energy

E = <psi | H | psi> where H = -sum_i Z_i Z_{i+1} - sum_i X_i (TFIM, OBC)

Via full statevector (256-dim): same formula as chi=2, unchanged.
Via reduced tensor contraction: contract H into the MERA causal cones, compute
partial traces. For nearest-neighbor H, only pairs of adjacent sites contribute.
Each two-site term: E_{i,i+1} = Tr[rho_{i,i+1} (Z_i Z_{i+1} + X_i + X_{i+1})]
where rho_{i,i+1} is the 2-site reduced density matrix obtained by tracing over all
other indices in the contracted MERA.

### 5.2 Von Neumann Entanglement Entropy

S(A) = -Tr[rho_A log rho_A] for contiguous interval A of length l.

At chi=3 the maximum entropy per causal cut is log(chi) = log(3) ~ 1.099 nats (0.585 * log(2) ebits? No: log2(3) ~ 1.585 ebits per cut).

Key observable for HYP-2026-009: compare S(l) vs. l curve between chi=2 and chi=3.
If chi=3 achieves S(l) ~ (c/3) log(l) with c=1/2 (CFT prediction for TFIM), this
confirms chi=3 is in the correct entanglement universality class.

At chi=2, S_max ~ log(2) = 1 ebit, which bounds S(l) <= 2 * log(2) = 2 ebits for
a cut through 2 MERA layers. At chi=3, S_max ~ 2 * log(3) ~ 3.17 ebits, enough to
match the CFT prediction for 8 sites.

### 5.3 Two-Point Correlation Functions

C(r) = <Z_i Z_{i+r}> - <Z_i><Z_{i+r}>

At the TFIM critical point, the exact result is C(r) ~ r^{-1/4} (1D Ising universality).
Chi=2 produced flat C(r) ~ 0.70 (SIM-2026-009 diagnosis: GHZ-like state).
Chi=3 target: C(r) ~ A * r^{-0.25} — a clear power-law decay.

Measurement: same as existing code, directly from optimized statevector:
  C[r] = <psi | Z_i Z_{i+r} | psi> - <psi | Z_i | psi>^2

### 5.4 Holographic Force Profile

After obtaining the chi=3 ground state, apply boundary-primary operator insertion
(Ry rotation on boundary site) and measure the resulting energy shift as a function
of distance. Procedure identical to SIM-2026-011 but using the chi=3 ground state.

If chi=3 achieves correct critical ground state, the force profile should more clearly
exhibit the power-law F(dr) ~ dr^{-alpha} seen in SIM-2026-011 (alpha ~ 3.92).
The key test: does chi=3 give cleaner power-law with smaller error bars?

### 5.5 Top-Layer Density Matrix

The 3x3 density matrix rho_top (obtained by tracing out all but the 2 top virtual indices)
encodes the coarse-grained state. Its von Neumann entropy S_top = -Tr[rho_top log rho_top]
is the most direct signal for HYP-2026-009: a jump in S_top between chi=2 and chi=3
indicates a phase transition in the RTN phase structure.

At chi=2: rho_top is 2x2, S_top bounded by log(2)
At chi=3: rho_top is 3x3 (on C^3 from each of 2 top virtual legs)
If S_top saturates the chi=3 bound (log(3)) vs. being near log(2), this is the phase
transition signature.

---

## 6. Layer-by-Layer Initialization

Following Miao & Barthel 2025 (validated in SIM-2026-008), use layer-by-layer init:

**Stage 1:** Optimize Layer 1 tensors only (U1, W1), freeze Layer 2, top tensor at identity.
  Params: 4*16 + 4*54 = 64 + 216 = 280 real (Layer 1 only)
  Evals: ~10,000 with ALM

**Stage 2:** Freeze Layer 1, optimize Layer 2 (U2, W2) + top tensor.
  Params: 2*81 + 2*54 + 16 = 162 + 108 + 16 = 286 real (Layer 2 + top)
  Evals: ~10,000 with ALM

**Stage 3:** Joint optimization, all 392 parameters, projected L-BFGS-B.
  Evals: ~30,000

**Stage 3 seeds:** Run 3 independent seeds from different random initializations.
  Recommended seeds: 7, 42, 99 (consistent with existing seed conventions).

---

## 7. Compute Requirements

### 7.1 Memory

Full 8q statevector: 2^8 complex128 = 256 * 16 bytes = 4 KB — negligible.
MERA tensors (392 real params at float64): ~3 KB.
Hamiltonian (dense 256x256 complex128): 256^2 * 16 bytes = 1 MB.
Working memory for L-BFGS-B (history buffer, 10 vectors): ~30 KB.

**Total: < 5 MB** — easily fits in RAM, no GPU needed for 8 sites.

### 7.2 CPU Time

Layer 1 eval: 10,000 evals * ~1 ms/eval (statevector contraction, 256-dim) = ~10 s
Layer 2 eval: 10,000 evals * ~1 ms/eval = ~10 s
Joint: 30,000 evals * ~1 ms/eval = ~30 s
Per seed: ~50 s
3 seeds: ~2.5 minutes

**Estimated wall time: ~5-10 minutes on a modern CPU** (local laptop is sufficient).

Compare to chi=2 at 8 sites: SIM-2026-008b completed in <5 min on local CPU.
Chi=3 is ~3-5x slower per eval due to larger matrix multiplications (9x9 vs 4x4),
but still well within local compute budget.

### 7.3 For Larger System Sizes (Future)

For 16q at chi=3:
  - Full statevector: 2^16 * 16 bytes = 1 MB — still feasible on CPU
  - MERA layers: 3 layers needed (16 -> 8 -> 4 -> 2 sites)
  - Parameters: ~800-1000 real
  - Estimated time: ~1-2 hours on CPU, ~5-10 min on GPU
  - Memory pressure: Hamiltonian (dense 65536^2 complex128) = 68 GB — USE SPARSE

For 24q at chi=3:
  - Full statevector: 2^24 * 16 bytes = 256 MB — GPU needed
  - MERA layers: 5 layers (as with chi=2)
  - Parameters: ~2000-2500 real
  - Recommended: RunPod A100 (same setup as SIM-2026-008c)
  - Estimated time: 15-30h on A100 (vs. ~9h for chi=2 in SIM-2026-008c)

---

## 8. Expected Outcomes vs. Chi=2

| Observable | Chi=2 (SIM-2026-008c/009) | Chi=3 (predicted) |
|------------|--------------------------|-------------------|
| Energy error (8q) | 1.12% | < 0.5% (more expressive) |
| Energy error (24q) | 3.33% | < 1.5% (if GHZ trap avoided) |
| S_top | log(2) ~ 0.693 | Up to log(3) ~ 1.099 |
| C(r) structure | Flat ~0.70 (GHZ) | Power-law ~ r^{-0.25} |
| <P> parity | 1.000 (enforced) | 1.000 (ALM+projection) |
| Force alpha | Inconclusive (GHZ) | Clearer alpha ~ 3.9-4.0 |
| Params (8q) | ~84 | ~392 |
| Wall time (8q) | ~5 min CPU | ~5-10 min CPU |

**Key test for HYP-2026-009:** If S_top jumps from ~log(2) to ~log(3) as we increase chi
from 2 to 3, this is evidence for a phase transition in the entanglement structure of the
MERA variational state — consistent with the RTN phase transition interpretation.

---

## 9. Implementation Roadmap

1. **Tensor library setup:** Use numpy + scipy.linalg.expm for matrix exponential.
   Optional: port to JAX for autodiff gradients (removes need for finite differences).

2. **Core contraction engine:** Implement MERA contraction for 8 sites in reduced space
   (C^81 after Layer 1, C^9 after Layer 2). Verify against full C^256 statevector on test case.

3. **Z2 projection:** Reuse existing project_z2() bit-flip trick from sim2026008b.
   Works identically for chi=3 (acts on full 2^8 statevector, not on virtual indices).

4. **ALM loop:** Reuse ALM structure from sim2026008b/c. Increase n_rounds from 8 to 10,
   increase ALM_EVALS from 3000 to 5000 to handle larger parameter space.

5. **Observable extraction:** After optimization, compute S(l) for all 28 contiguous
   intervals of 8 sites (l = 1, 2, ..., 7 for OBC), C(r) for r = 1..7, and force profile.

6. **Comparison:** Plot S(l) vs. l for chi=2 and chi=3 on same axes. If chi=3 shows log(l)
   scaling, HYP-2026-009 is supported.

---

## 10. File Naming Conventions

Following existing SIM-XXXX pattern:
- Design: `SIM-2026-015-chi3-mera-design.md` (this file)
- Implementation: `sim2026015_chi3_8q.py`
- Results: `SIM-2026-015.json`
- Theta file: `theta_opt_SIM2026015.npy`

---

## Summary

The chi=3 MERA for 8-site TFIM requires ~392 parameters (vs. ~84 for chi=2), organized
as 4 U(4) disentanglers + 4 St(3,4) isometries in Layer 1 and 2 U(9) disentanglers +
2 St(3,9) isometries in Layer 2 plus a 9-dim top vector. The ALM+projection two-phase
method from SIM-2026-008 carries over unchanged — only the tensor dimensions and parameter
count grow. Expected compute: ~5-10 minutes locally. The critical test is whether S_top
saturates log(3) and C(r) shows power-law decay — both signal the phase transition
that HYP-2026-009 predicts.
