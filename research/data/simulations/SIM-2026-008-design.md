# SIM-2026-008: Z2-Preserving MERA VQE Design

## Problem Statement

All SIM-2026-007 seeds converge to ferromagnetic states (<M>~0.84, <P>=0) despite lambda=20 penalty. Root cause: CNOT (CX) gates do NOT preserve Z2 parity, so the circuit can freely access P=-1 states. The penalty fights a losing battle against a circuit that structurally violates the constraint.

## Solution: Parity-Preserving MERA Gates

### Gate Block Design

Replace each `U(p0,p1,p2,i) + U(p3,p4,p5,j) + CX(i,j)` block with:

```python
def add_parity_preserving_gate(qc, i, j, params, offset):
    """Z2 parity-preserving two-qubit gate block.
    All gates commute with P = prod(X_i), guaranteeing <P>=+1."""
    qc.rz(params[offset], i)
    qc.rz(params[offset+1], j)
    qc.rxx(params[offset+2], i, j)  # XX rotation (preserves parity)
    qc.ryy(params[offset+3], i, j)  # YY rotation (preserves parity)
    qc.cz(i, j)                      # CZ commutes with P (unlike CX!)
    qc.rz(params[offset+4], i)
    qc.rz(params[offset+5], j)
    return offset + 6
```

**Why this works**: Every state reachable from |+...+> (P=+1 eigenstate) by parity-preserving gates automatically has P=+1. No penalty needed. No projection needed.

**Key insight**: CX maps X_control -> X_control * X_target, changing parity structure. CZ commutes with all X_i, preserving parity. The XX and YY rotations also commute with P = prod(X_i).

### Parameters per block: 6 (vs 7 current)
### Total parameters (24q, 5-layer): ~210 (vs 252 current)

## Initialization: Layer-by-Layer (Miao & Barthel 2025)

Instead of optimizing all layers simultaneously from random init:

1. **Phase 1** (layer 1 only): Optimize finest-scale layer, layers 2-5 frozen at identity. ~3000 evals.
2. **Phase 2** (layer 2 only): Freeze layer 1, optimize layer 2. ~3000 evals.
3. **Phase 3-5**: Continue layer by layer. ~3000 evals each.
4. **Phase 6** (all layers): Unfreeze everything, joint optimization from good initial point. ~10000 evals.

Total: ~25000 evals (similar to SIM-2026-007's 20000).

## Circuit Specification

| Parameter | Value |
|---|---|
| Qubits | 24 |
| Layers | 5 |
| Gate type | Parity-preserving (Rz + Rxx + Ryy + CZ) |
| Params/block | 6 |
| Total params | ~210 |
| Z2 enforcement | By construction (guaranteed <P>=1.000) |
| Optimizer | L-BFGS-B (landscape is smooth within P=+1 sector) |
| Seeds | 5 (7, 42, 99, 13, 77) |
| Init | Layer-by-layer |
| Backend | RunPod A100 SXM 80GB |

## Validation Plan

1. **8q test** (SIM-2026-008a): Validate on 8-qubit TFIM first
   - Confirm <P>=1.000 throughout all evals
   - Target <1% energy error
   - Compare to exact diag (E0 = -10.252)
   - Run locally, ~5 min

2. **24q production** (SIM-2026-008b): Full 5-layer MERA on RunPod
   - Target <2% energy error (E > -29.6, E0 = -30.200)
   - If achieved: immediately run boundary-primary force measurements
   - Estimated cost: ~$20-40

## Fallback: Adiabatic Parameter Sweep

If parity-preserving gates + layer-by-layer still don't converge below 2%:

1. Start at g/J = 2.0 (deep paramagnetic, unique ground state)
2. Optimize MERA to convergence at g=2.0
3. Step g to 1.5, re-optimize from previous solution
4. Step g to 1.2, re-optimize
5. Step g to 1.0 (critical), re-optimize

Cost: ~4x single run, but each step converges faster.

## Literature Sources

- Miao & Barthel (2025): Layer-by-layer MERA init, no barren plateaus
- Gard et al. (2020): Symmetry-preserving state preparation circuits
- NeurIPS 2024: Parity-check enhanced symmetry-preserving ansatz
- Symmetry-Enhanced VQE (Quantum, 2023): Circuit > penalty for symmetry
- ADAPT-VQE symmetry breaking (JCTC, 2022): Explains our ferromagnetic trap

## Expected Outcomes

- Z2 symmetry: GUARANTEED (<P>=1.000 by construction)
- Energy: target <2% error
- Force profile: non-flat (boundary-primary excitations after convergence)
- Timeline: 8q validation (~1 day), 24q production (~2 days on RunPod)
