# Quantum-Chemistry Method-Combination Hunt — Framing QC-A (2026-05-17)

**Question:** Not a field survey. Hunt for novel *combinations* of quantum-chemistry
computational methods (VQE, QPE, QITE, quantum Krylov/subspace, DMRG/MERA/PEPS, DMET/DMFT/QM-MM,
QMC, FermiNet/PauliNet, classical shadows, symmetry-adapted ansatze, error mitigation) where the
*coupling* produces an emergent capability neither method has alone.

**Scoring (integers 1–5):** NOVELTY (5 = no prior art located), BUILDABILITY (5 = runs now on a
laptop / free cloud quantum credits; 1 = needs FT hardware), USEFULNESS (5 = produces a chemistry
result people want), MECHANISM-FAITHFUL (5 = principled coupling; 1 = coincidental/hand-wavy).
**Product = N × B × U.** Mech is a tie-break / quality flag.

**Prior-art protocol:** arXiv MCP recency feed is stale and was NOT trusted. Claims checked via
WebSearch; URLs/arXiv IDs cited inline.

---

## Ranked table (by Product desc)

| Rank | Combination | Emergent capability | N | B | U | Mech | Product |
|------|-------------|---------------------|---|---|---|------|---------|
| 1 | **FermiNet/Psiformer VMC → locally-biased classical-shadow estimator on a shallow VQE state** (NQS as the *measurement bias*, not the ansatz) | Chemical-accuracy 2-RDM/property readout from a hardware-shallow circuit with ~10–100× fewer shots, because the NQS supplies the optimal per-Pauli measurement weighting it would cost a quantum device nothing to query | 4 | 4 | 4 | 5 | 64 |
| 2 | **QITE-generated non-orthogonal block as a barren-plateau-free *initializer* for a symmetry-adapted VQE, recycling QITE intermediates as the Krylov basis** (one quantum run, two products) | A single circuit family yields both a good VQE start (no plateau) *and* a free excited-state spectrum from the discarded QITE intermediates — the warmup cost is amortized into spectroscopy | 4 | 4 | 4 | 4 | 64 |
| 3 | **Classical-shadow 2-RDM → generalized-DMET bath descriptor in a self-consistent loop** (shadow RDM *is* the low-level descriptor, closing the embedding fixpoint on quantum data) | Quantum-accurate bath that self-consistently re-fragments strongly-correlated regions; the embedding adapts to the *measured* correlation, not an HF guess | 4 | 3 | 5 | 4 | 60 |
| 4 | **Neural-quantum-state surrogate trained on classical shadows of a noisy VQE state, used as the QITE imaginary-time propagator's domain oracle** | Noise-robust QITE: the NQS denoises the state *and* supplies the operator-domain correlations QITE needs, so imaginary-time steps converge under hardware noise that breaks bare QITE | 4 | 3 | 4 | 4 | 48 |
| 5 | **MERA disentangler layer as the DMET bath-construction map for a quantum impurity solver** | Multi-scale bath that captures critical/long-range correlation a single Schmidt cut misses — embedding for metals/conjugated systems, not just gapped fragments | 5 | 2 | 4 | 4 | 40 |
| 6 | **Symmetry-adapted ansatz used to *precondition* the quantum-Krylov overlap matrix (symmetry sectors block-diagonalize the ill-conditioned S-matrix)** | Krylov diagonalization that stays well-conditioned at large subspace depth because degenerate near-linear-dependent vectors are separated by quantum number | 3 | 4 | 4 | 4 | 48 |
| 7 | **Classical-shadow off-diagonal matrix elements feeding a tensor-network (DMRG) contraction to extrapolate the Krylov spectrum to infinite subspace** | Excited-state energies at MPS-extrapolated accuracy from a constant-depth shadow protocol | 2 | 3 | 4 | 3 | 24 |

---

## Editorial notes (top-5)

### #1 — NQS-biased classical shadows on a shallow VQE state (N4·B4·U4·Mech5 = 64)

**The two methods coupled:** a classically-trained FermiNet/Psiformer (or MPS) neural quantum
state and locally-biased classical-shadow tomography of a shallow hardware VQE/ADAPT state.
**Emergent capability:** chemical-accuracy 2-RDM and derived properties (dipoles, forces,
correlation functions) from a circuit too shallow for those properties to be read out by naive
shadows. **Why it beats either alone:** a bare NQS is variationally biased and never sees the
hardware state; bare classical shadows on a shallow state have variance that explodes for the
high-weight fermionic Paulis chemistry needs. **Mechanism (the object that passes):** the NQS is
*not* the ansatz — it is queried only classically to produce the per-observable importance weights
of the locally-biased shadow estimator (the LBCS bias distribution β\*(P) ∝ |⟨P⟩_NQS|·w_P). The
NQS is an excellent, free classical approximation of exactly the quantity LBCS needs; the quantum
device only ever runs random Cliffords. **Closest prior art:** Hadfield et al.,
*Locally-Biased Classical Shadows* (Springer CMP 2022, arXiv:2006.15788) bias from a *classical
mean-field/CISD* approximation; Neural Error Mitigation (arXiv:2105.08086) uses an NQS to
*re-tomograph* the state. **How this differs:** neither uses a high-accuracy continuum NQS
(FermiNet-class) purely as the shadow *bias oracle* while keeping the quantum state untouched —
the NQS replaces the weak CISD prior with a near-FCI one, which is where the 10–100× variance gain
comes from. **Hardest obstacle:** the NQS is in first quantization / continuum; mapping its
amplitudes onto the second-quantized Pauli basis the shadow lives in is non-trivial and basis-set
dependent (cost may eat the shot saving for large active spaces). **Usable result:** ground-state
2-RDM and dipole of strongly-correlated small molecules (N2 dissociation, benzene π-space, [4Fe-4S]
minimal model) to ~1 mHa from a depth-≤20 circuit on a free IBM/IQM cloud allocation.

### #2 — QITE block as plateau-free VQE initializer with recycled Krylov spectroscopy (64)

**Coupled:** quantum imaginary-time evolution (large-domain, non-variational) and a
symmetry-adapted VQE, with the QITE intermediates retained as a quantum-Krylov basis.
**Emergent capability:** one quantum run delivers a barren-plateau-free VQE warm start *and*, for
free, the low-lying excited-state spectrum — the warmup compute is amortized into spectroscopy
instead of discarded. **Why it beats either alone:** large-domain QITE alone is accurate but its
domain cost grows; standalone VQE on a random init hits a plateau; standalone QLanczos throws away
the converged endpoint. **Mechanism:** the non-orthogonal set {e^{−τ_k H}|ψ0⟩} produced *en route*
to the QITE fixed point is exactly a Krylov basis; the final iterate is the VQE init. One object
(the QITE trajectory) is read twice — terminal state → VQE θ-init; full trajectory → generalized
eigenproblem (S,H). **Closest prior art:** QLanczos (Motta et al., Nat. Phys. 2020) builds Krylov
*from* QITE; ADAPT-VQE warm starts exist separately. **How this differs:** the explicit *dual use*
of a single QITE run as both a plateau-escape initializer for a downstream symmetry-projected VQE
*and* the Krylov generator — the spectroscopy is a zero-marginal-cost byproduct of the warmup, not
a separate protocol. **Hardest obstacle:** QITE domain-size growth for strongly correlated systems
and ill-conditioning of S as the trajectory self-overlaps; symmetry projection mitigates but does
not remove this. **Usable result:** ground + first 2–3 excited states of H4/H6 chains, LiH,
H2O-bending, to chemical accuracy in a single hardware session.

### #3 — Shadow-2-RDM as a self-consistent generalized-DMET descriptor (60)

**Coupled:** classical-shadow 2-RDM estimation and generalized DMET (arbitrary-1-RDM
descriptor, disentanglement-optimized bath) in a closed self-consistency loop. **Emergent
capability:** the embedding bath is rebuilt from the *measured* quantum correlation each
iteration, so fragment boundaries adapt to where correlation actually is rather than to an HF
projector. **Why it beats either alone:** standard DMET freezes the bath from a mean-field 1-RDM
(wrong for metals/strong correlation); a one-shot shadow RDM has no embedding feedback.
**Mechanism:** the shadow-estimated fragment 2-RDM (and its 1-RDM marginal) is fed back as the
generalized-DMET *low-level descriptor*, and the disentanglement criterion re-derives the bath —
the RDM is the fixpoint variable of the embedding loop. **Closest prior art:** DMET+SQD
(arXiv:2511.22158), generalized DMET (arXiv:2503.09881), shadow-2-RDM with N-representability
(arXiv:2411.18430) — all *one-directional*. **How this differs:** the shadow RDM is not just a
solver output but the *self-consistency variable* feeding the generalized (not orthogonal-
projector) bath construction — a measured-correlation-adaptive embedding fixpoint. **Hardest
obstacle:** shadow shot noise in the 2-RDM propagating into bath instability across the
self-consistency loop (noise-driven non-convergence); needs N-representability projection inside
the loop, raising classical cost. **Usable result:** energies of stretched-bond / biradical
fragments and 1-D Hubbard-like organic chains where fixed-bath DMET fails, at near-FCI fragment
accuracy with NISQ-depth impurity solves.

### #4 — Shadow-trained NQS surrogate as the QITE domain oracle (48)

**Coupled:** classical shadows of a noisy VQE state → NQS surrogate → that NQS supplies the
local operator-domain correlators QITE needs for its linear-system step. **Emergent capability:**
QITE that converges under hardware noise that breaks the bare algorithm, because the imaginary-
time update is computed from a denoised NQS rather than directly from noisy expectation values.
**Mechanism:** QITE's per-step least-squares solve needs ⟨domain Pauli⟩; these are read off the
shadow-trained NQS (which is noise-regularized) instead of re-measured noisily. **Closest prior
art:** Neural Error Mitigation (arXiv:2105.08086) denoises a *static* VQE state; QITE noise studies
exist separately. **How this differs:** the NQS is inserted *inside* the QITE iteration as the
correlator oracle, making the imaginary-time dynamics itself noise-robust, not just the final
energy. **Hardest obstacle:** NQS retraining cost every QITE step (or staleness if not retrained)
and guaranteeing the surrogate stays in the correct symmetry sector. **Usable result:**
ground-state energies of BeH2 / H2O on real noisy hardware where unmitigated QITE diverges.

### #5 — MERA disentangler as the DMET bath map (40)

**Coupled:** a MERA entanglement-renormalization layer and DMET bath construction for a
quantum impurity solver. **Emergent capability:** a *multi-scale* bath capturing long-range /
critical correlation that a single Schmidt cut (standard DMET bath) structurally cannot, extending
embedding to metals and conjugated/aromatic systems. **Mechanism:** the MERA disentanglers +
isometries define the fragment↔environment map; the bath is the coarse-grained MERA boundary
rather than a one-shot Schmidt decomposition — scale-resolved entanglement passes between them.
**Closest prior art:** DMET's tensor-network interpretation is known (JCTC 2016); MERA-DMET as an
explicit bath constructor is not located. **How this differs:** uses MERA's defining property
(scale-invariant entanglement renormalization) as the embedding map, targeting exactly the
gapless regime standard DMET fails. **Hardest obstacle:** MERA optimization cost and fermionic
MERA sign structure; buildability is low (B2) — likely classical-simulation proof-of-concept only
near term. **Usable result:** proof-of-concept embedding energy for a 1-D critical Hubbard chain
or polyacene π-system where single-cut DMET bath is qualitatively wrong.

---

**Prior-art note:** every candidate has at least one *component* published; the located novelty is
in the *coupling direction and the passed object*. #1's novelty is the FermiNet-grade NQS as a
pure shadow-bias oracle (not ansatz, not re-tomographer). #2's is the dual-use of one QITE run.
#3's is the closed self-consistent loop with the *generalized* (non-projector) bath. The arXiv
MCP recency feed was not used; all checks via WebSearch (URLs in-line above).
