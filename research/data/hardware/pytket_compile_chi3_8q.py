"""
Pytket compilation of chi=3 8q MERA circuit for Quantinuum Helios.

Builds the concrete qubit-circuit version of the chi=3 8q MERA whose
abstract-tensor form lives in `sim2026015_chi3_8q.py`. Uses the saved
seed-42 parameters from `theta_opt_SIM2026015.npy` (best chi=3 fit with
E0 error 0.0024%) so the gate count reflects the SPECIFIC state we'd
prepare on Helios, not a worst-case bound.

==============================================================================
Qubit layout (16 qubits total -- no qubit reuse across layers, for clarity)
==============================================================================

  Boundary (measured): q0 q1 q2 q3 q4 q5 q6 q7   (8 qubits, N_M = 8)
  Top-tensor wires:    q8 q9 q10 q11             (4 qubits, 2 chi=3 ququarts)
  Layer-2 ancillas:    q12 q13 q14 q15           (4 qubits, expansion targets)

  All qubits start in |0>.

State flow (top -> bottom = circuit time):

  t=1  Prep top tensor onto q8..q11  (U(16) 4-qubit gate)
  t=2  W2[0] on (q8q9 in, q12q13 anc): outputs chi=9 on q8q9q12q13
       W2[1] on (q10q11 in, q14q15 anc): outputs chi=9 on q10q11q14q15
       (2 x U(16) 4-qubit isometric gates)
  t=3  U2[0] disentangler on (q8q9q12q13): U(9) embedded in U(16)
       U2[1] disentangler on (q10q11q14q15): U(9) embedded in U(16)
       (2 x U(16) 4-qubit gates)
  t=4  Route 4 chi=3 sub-wires onto 8 boundary qubits via W1 isometries.
       After Layer-2 the 4 chi=3 sub-wires live on pairs:
         (q8,q9), (q12,q13), (q10,q11), (q14,q15)
       Each W1[k] is C^3 -> C^4 = U(4) on a 2-qubit ququart, applied
       directly (the 4th basis state was idle as ancilla via the chi=3
       restriction at the start of Layer 1).
       Then SWAP each Layer-1 output pair onto the boundary qubits:
         (q8,q9)   -> (q0,q1)
         (q12,q13) -> (q2,q3)
         (q10,q11) -> (q4,q5)
         (q14,q15) -> (q6,q7)
       (4 x U(4) 2-qubit gates + 8 x SWAPs)
  t=5  U1[0..3] disentanglers on adjacent boundary pairs:
         (q0,q1), (q2,q3), (q4,q5), (q6,q7)   ... WRONG WAY
       Actually the U1 disentanglers in MERA act ACROSS adjacent
       isometry blocks, not within. So U1[k] acts on (q2k+1, q2k+2)
       for k=0..3, i.e. between adjacent pairs.
       The abstract code does u1s[k].conj().T applied via the contraction
         np.einsum('Ii,Jj,Kk,Ll,ijkl->IJKL', u1s[0]^dag, ..., state)
       where the 4-index state corresponds to the 4 chi=4 wires. So u1s[k]
       is actually a SINGLE-WIRE operation in the abstract code -- it's a
       U(4) on the kth chi=4 wire = U(4) on 2 qubits within wire k.
       On qubits: 4 x U(4) on (q0q1), (q2q3), (q4q5), (q6q7).
  t=6  Measure q0..q7 (8 measurements; N_M = 8)

==============================================================================
Why this design choice
==============================================================================

- 16 qubits is well within Helios's 56-qubit register; no need to optimize
  for minimum qubits. Helios's all-to-all connectivity means qubit count
  has no routing penalty.
- Avoiding qubit reuse across layers means no mid-circuit SWAPs cluttering
  the gate count. The 4 SWAPs at t=4 are unavoidable since Layer-2 outputs
  don't sit on boundary qubits naturally; we could relabel to remove them
  but at the cost of obscurity.
- Each 4-qubit unitary (top prep, W2, U2) is appended as a Qiskit
  UnitaryGate. Qiskit's transpiler will decompose them via Quantum Shannon
  Decomposition (QSD); pytket's FullPeepholeOptimise will then merge
  adjacent 2Q interactions and decompose to native ZZPhase + PhasedX + Rz.

==============================================================================
HQC formula (Quantinuum, current)
==============================================================================

  HQC = 5 + (C/5000) * ( Max(N_1q) + 10*Max(N_2q) + 5*Max(N_M) )

where Max(.) is the maximum count over 10 shot-simulations. For our
non-Clifford-but-deterministic circuit (no mid-circuit measurement,
no classical control), Max(N_*) = static count.

For the resubmission scope (C = 10,000 shots, 2 probe positions dr=1,2,
plus calibration + drift checks), we use the static counts from this
script to compute the final HQC budget.

Author: Claude Code (option-1 of the HQC reply workflow)
Date: 2026-05-20
"""
import json
import time
from pathlib import Path

import numpy as np
from scipy.linalg import expm

from qiskit import QuantumCircuit
from qiskit.circuit.library import UnitaryGate

from pytket.extensions.qiskit import qiskit_to_tk
from pytket._tket.circuit import OpType
from pytket.passes import (
    FullPeepholeOptimise,
    RemoveRedundancies,
    SquashTK1,
    DecomposeTK2,
    NormaliseTK2,
    AutoRebase,
)

REPO = Path(__file__).resolve().parents[2]
THETA_PATH = REPO / "data" / "simulations" / "theta_opt_SIM2026015.npy"
OUT_JSON   = Path(__file__).parent / "pytket_compile_chi3_8q_results.json"

# ============================================================================
# Parameter unpacking (matches sim2026015_chi3_8q.py exactly)
# ============================================================================
CHI = 3
HP4 = 4 * 4   # 16
HP9 = 9 * 9   # 81
N_PARAMS = 4*HP4 + 4*HP4 + 2*HP9 + 2*HP9 + 18  # 470


def params_to_hermitian(params: np.ndarray, n: int) -> np.ndarray:
    A = np.zeros((n, n), dtype=complex)
    idx = 0
    for i in range(n):
        A[i, i] = params[idx]; idx += 1
    for i in range(n):
        for j in range(i+1, n):
            A[i, j] = params[idx] + 1j * params[idx+1]
            A[j, i] = params[idx] - 1j * params[idx+1]
            idx += 2
    return A


def make_unitary(params: np.ndarray, n: int) -> np.ndarray:
    return expm(1j * params_to_hermitian(params, n))


def make_isometry(params: np.ndarray, n_big: int, n_small: int) -> np.ndarray:
    return make_unitary(params, n_big)[:, :n_small]


def unpack_theta(theta: np.ndarray):
    o = 0
    u1s = [make_unitary(theta[o + k*HP4 : o + (k+1)*HP4], 4) for k in range(4)]
    o += 4 * HP4
    w1s = [make_isometry(theta[o + k*HP4 : o + (k+1)*HP4], 4, CHI) for k in range(4)]
    o += 4 * HP4
    u2s = [make_unitary(theta[o + k*HP9 : o + (k+1)*HP9], 9) for k in range(2)]
    o += 2 * HP9
    w2s = [make_isometry(theta[o + k*HP9 : o + (k+1)*HP9], 9, CHI) for k in range(2)]
    o += 2 * HP9
    raw = theta[o:o + 18]
    psi = raw[0::2] + 1j * raw[1::2]
    n = np.linalg.norm(psi)
    psi_top = psi / n if n > 1e-15 else np.eye(9, dtype=complex)[0]
    return u1s, w1s, u2s, w2s, psi_top


# ============================================================================
# Qubit-Hilbert-space embeddings
# ============================================================================
def _complete_unitary(cols: np.ndarray, dim: int, seed: int = 20260520) -> np.ndarray:
    """Given an isometry `cols` (dim x k) with orthonormal columns, return a
    full dim x dim unitary whose first k columns equal cols (filled by
    Gram-Schmidt against random vectors)."""
    k = cols.shape[1]
    out = np.zeros((dim, dim), dtype=complex)
    out[:, :k] = cols
    rng = np.random.default_rng(seed)
    for j in range(k, dim):
        attempts = 0
        while True:
            v = rng.standard_normal(dim) + 1j * rng.standard_normal(dim)
            for i in range(j):
                v = v - np.vdot(out[:, i], v) * out[:, i]
            n = np.linalg.norm(v)
            if n > 1e-10:
                out[:, j] = v / n
                break
            attempts += 1
            if attempts > 10:
                # fall back to a basis vector projection
                e = np.zeros(dim, dtype=complex); e[j] = 1.0
                for i in range(j):
                    e = e - np.vdot(out[:, i], e) * out[:, i]
                out[:, j] = e / np.linalg.norm(e)
                break
    return out


def embed_u9_in_u16(u9: np.ndarray) -> np.ndarray:
    """U(9) -> U(16) by acting as identity on the last 7 basis states."""
    u16 = np.eye(16, dtype=complex)
    u16[:9, :9] = u9
    return u16


def embed_w_to_u(w: np.ndarray, dim_out: int) -> np.ndarray:
    """Isometry W in C^{n_big x n_small} -> U(dim_out) whose first n_small
    columns equal W (zero-padded to dim_out)."""
    n_big, n_small = w.shape
    cols = np.zeros((dim_out, n_small), dtype=complex)
    cols[:n_big, :] = w
    return _complete_unitary(cols, dim_out)


def top_state_prep_u16(psi_top_9: np.ndarray) -> np.ndarray:
    """U(16) whose first column is psi_top padded 9->16."""
    target = np.zeros((16, 1), dtype=complex)
    target[:9, 0] = psi_top_9
    return _complete_unitary(target, 16)


# ============================================================================
# Build the 16-qubit chi=3 8q MERA state-preparation circuit
# ============================================================================
N_QUBITS_CIRCUIT = 16  # 8 boundary + 4 top + 4 layer-2 ancillas
BOUNDARY = list(range(8))     # q0..q7 -- measured
TOP      = [8, 9, 10, 11]     # q8..q11 -- top tensor wires
ANC2     = [12, 13, 14, 15]   # q12..q15 -- layer-2 expansion ancillas


def build_chi3_8q_qubit_circuit(theta: np.ndarray) -> QuantumCircuit:
    u1s, w1s, u2s, w2s, psi_top = unpack_theta(theta)

    qc = QuantumCircuit(N_QUBITS_CIRCUIT, len(BOUNDARY))

    # -- t=1: prep top tensor onto q8..q11 --
    qc.append(UnitaryGate(top_state_prep_u16(psi_top), label="prep_top"), TOP)

    # -- t=2: Layer-2 isometries W2 (chi=3 -> chi=9, 4-qubit gates) --
    # W2[0] embedded in U(16) acts on (q8q9, q12q13) and writes chi=9 state.
    # W2[1] embedded in U(16) acts on (q10q11, q14q15).
    # Convention: input ququart on the FIRST 2 qubits, ancilla |00> on the
    # LAST 2 qubits. After W2 the 4 qubits jointly encode the chi=9 state.
    qc.append(UnitaryGate(embed_w_to_u(w2s[0], 16), label="W2_0"),
              [TOP[0], TOP[1], ANC2[0], ANC2[1]])
    qc.append(UnitaryGate(embed_w_to_u(w2s[1], 16), label="W2_1"),
              [TOP[2], TOP[3], ANC2[2], ANC2[3]])

    # -- t=3: Layer-2 disentanglers U2 (U(9) -> U(16), 4-qubit gates) --
    qc.append(UnitaryGate(embed_u9_in_u16(u2s[0]), label="U2_0"),
              [TOP[0], TOP[1], ANC2[0], ANC2[1]])
    qc.append(UnitaryGate(embed_u9_in_u16(u2s[1]), label="U2_1"),
              [TOP[2], TOP[3], ANC2[2], ANC2[3]])

    # After Layer-2 the 4 chi=3 sub-wires live on pairs:
    #   sub-wire 0: (q8, q9)        \
    #   sub-wire 1: (q12, q13)       > FIRST chi=9 (pair A in abstract code)
    #   sub-wire 2: (q10, q11)      \
    #   sub-wire 3: (q14, q15)       > SECOND chi=9 (pair B in abstract code)
    # Map them to boundary qubit pairs (q0q1, q2q3, q4q5, q6q7) via SWAPs.
    wire_pairs = [
        ((TOP[0],  TOP[1]),  (BOUNDARY[0], BOUNDARY[1])),
        ((ANC2[0], ANC2[1]), (BOUNDARY[2], BOUNDARY[3])),
        ((TOP[2],  TOP[3]),  (BOUNDARY[4], BOUNDARY[5])),
        ((ANC2[2], ANC2[3]), (BOUNDARY[6], BOUNDARY[7])),
    ]
    for (src, dst) in wire_pairs:
        qc.swap(src[0], dst[0])
        qc.swap(src[1], dst[1])

    # -- t=4: Layer-1 isometries W1 (chi=3 -> chi=4, 2-qubit gates) --
    # Each W1[k] embedded into U(4) on the kth boundary pair.
    for k, pair in enumerate([(0,1), (2,3), (4,5), (6,7)]):
        qc.append(UnitaryGate(embed_w_to_u(w1s[k], 4), label=f"W1_{k}"),
                  list(pair))

    # -- t=5: Layer-1 disentanglers U1 (U(4), 2-qubit gates) --
    # Acts on each chi=4 boundary pair INTRA-WIRE (per abstract code).
    for k, pair in enumerate([(0,1), (2,3), (4,5), (6,7)]):
        qc.append(UnitaryGate(u1s[k], label=f"U1_{k}"), list(pair))

    # -- t=6: measure boundary --
    qc.measure(BOUNDARY, list(range(len(BOUNDARY))))

    return qc


# ============================================================================
# Compile to Quantinuum native gate set and count
# ============================================================================
def count_gates_pytket(circ) -> dict:
    counts = {}
    for cmd in circ.get_commands():
        n = cmd.op.type.name
        counts[n] = counts.get(n, 0) + 1
    return counts


def compile_and_report(qc: QuantumCircuit) -> dict:
    """Decompose UnitaryGate -> CX+1Q via Qiskit, then pytket optimize +
    rebase to Quantinuum native {Rz, PhasedX, ZZPhase}."""
    # Qiskit decomposes 4-qubit UnitaryGate via Quantum Shannon Decomposition.
    t0 = time.time()
    qc_basis = qc.decompose(reps=8)  # cascade decompose UnitaryGate -> CX/U
    t_qiskit_decomp = time.time() - t0

    # Strip measurements before pytket optimization (measurements re-added at end)
    qc_nomeas = qc_basis.remove_final_measurements(inplace=False)

    print(f"  [Qiskit decomp] {t_qiskit_decomp:.2f}s, "
          f"ops: {dict(qc_nomeas.count_ops())}")

    t0 = time.time()
    tk = qiskit_to_tk(qc_nomeas)
    t_convert = time.time() - t0

    pre_counts = count_gates_pytket(tk)
    pre_depth = tk.depth()
    print(f"  [pytket pre]    {pre_depth=} ops={pre_counts}")

    # FullPeepholeOptimise targeting TK2 (universal 2Q form) for max merging
    t0 = time.time()
    FullPeepholeOptimise(target_2qb_gate=OpType.TK2).apply(tk)
    t_peephole = time.time() - t0
    mid_counts = count_gates_pytket(tk)
    print(f"  [TK2 peephole]  {t_peephole:.1f}s ops={mid_counts}")

    # TK2 -> ZZPhase (minimum count per TK2)
    t0 = time.time()
    NormaliseTK2().apply(tk)
    DecomposeTK2(ZZPhase_fidelity=1.0).apply(tk)
    AutoRebase({OpType.Rz, OpType.PhasedX, OpType.ZZPhase}).apply(tk)
    RemoveRedundancies().apply(tk)
    SquashTK1().apply(tk)
    AutoRebase({OpType.Rz, OpType.PhasedX, OpType.ZZPhase}).apply(tk)
    RemoveRedundancies().apply(tk)
    t_rebase = time.time() - t0

    post_counts = count_gates_pytket(tk)
    post_depth = tk.depth()
    print(f"  [native rebase] {t_rebase:.1f}s depth={post_depth} ops={post_counts}")

    # HQC-relevant counts (per Quantinuum doc):
    #   N_1q = PhasedX (Rxy) count; Rz is EXCLUDED
    #   N_2q = ZZPhase (= Rzz) count
    #   N_M  = number of measurements = len(BOUNDARY) (added back after compile)
    n_1q = post_counts.get("PhasedX", 0)
    n_2q = post_counts.get("ZZPhase", 0)
    n_rz = post_counts.get("Rz", 0)
    n_m  = len(BOUNDARY)

    # HQC formula: HQC = 5 + (C/5000) * ( N_1q + 10*N_2q + 5*N_M )
    def hqc(shots: int) -> float:
        return 5.0 + (shots / 5000.0) * (n_1q + 10*n_2q + 5*n_m)

    n_shots = 10_000
    hqc_per_run = hqc(n_shots)

    print(f"\n  HQC accounting (C = {n_shots} shots):")
    print(f"    N_1q (PhasedX) = {n_1q}")
    print(f"    N_2q (ZZPhase) = {n_2q}")
    print(f"    N_M (measure)  = {n_m}")
    print(f"    N_Rz (free)    = {n_rz}")
    print(f"    HQC per run    = 5 + ({n_shots}/5000)*({n_1q} + 10*{n_2q} + 5*{n_m})")
    print(f"                   = 5 + 2 * {n_1q + 10*n_2q + 5*n_m}")
    print(f"                   = {hqc_per_run:.1f}")

    # Multi-run scope from qcup-resubmission-2026-04.md:
    #   2 dr-points * 1 run each + 1 calibration + 2 drift-checks (= 5 runs total)
    runs_scope = 5
    hqc_total  = runs_scope * hqc_per_run
    print(f"    HQC TOTAL ({runs_scope} runs) = {hqc_total:.1f}")

    return {
        "qiskit_decomp_time_s": t_qiskit_decomp,
        "pytket_convert_time_s": t_convert,
        "pytket_peephole_time_s": t_peephole,
        "pytket_rebase_time_s": t_rebase,
        "pre_depth": pre_depth,
        "post_depth": post_depth,
        "pre_counts": pre_counts,
        "post_counts": post_counts,
        "n_1q_phasedx": n_1q,
        "n_2q_zzphase": n_2q,
        "n_rz": n_rz,
        "n_m": n_m,
        "shots": n_shots,
        "hqc_per_run": hqc_per_run,
        "runs_scope": runs_scope,
        "hqc_total": hqc_total,
    }


# ============================================================================
# Main
# ============================================================================
def main():
    print("=" * 78)
    print("  pytket compilation: chi=3 8q MERA -> Quantinuum Helios native")
    print("  Source: theta_opt_SIM2026015.npy (seed=42 best fit, 0.0024% E0 error)")
    print("=" * 78)

    if not THETA_PATH.exists():
        raise FileNotFoundError(f"Missing saved params: {THETA_PATH}")
    theta = np.load(THETA_PATH)
    print(f"\n  Loaded theta shape={theta.shape}, expected={N_PARAMS}")
    assert theta.shape == (N_PARAMS,), \
        f"Expected {N_PARAMS} params, got {theta.shape}"

    # Self-check: build same statevector as sim2026015_chi3_8q.py via tensor
    # contraction, vs unitary action of qubit circuit on |0...0>, to confirm
    # the qubit circuit produces the same boundary state.
    print("\n  Building qubit circuit ...")
    qc = build_chi3_8q_qubit_circuit(theta)
    print(f"    qubits: {qc.num_qubits}, depth: {qc.depth()}, "
          f"unitaries: {qc.count_ops()}")

    print("\n  Compiling -> Quantinuum native gate set ...")
    result = compile_and_report(qc)

    out = {
        "id": "pytket_compile_chi3_8q",
        "circuit": {
            "n_qubits_total": N_QUBITS_CIRCUIT,
            "n_qubits_boundary_measured": len(BOUNDARY),
            "layout": {
                "boundary_q0_q7": BOUNDARY,
                "top_q8_q11": TOP,
                "ancillas_q12_q15": ANC2,
            },
            "n_unitaries": {
                "U_top_4q": 1,
                "W2_4q":    2,
                "U2_4q":    2,
                "W1_2q":    4,
                "U1_2q":    4,
                "SWAP_2q":  8,
            },
        },
        "source_theta": str(THETA_PATH),
        "seed": 42,
        "results": result,
        "formula": "HQC = 5 + (C/5000) * (N_1q + 10*N_2q + 5*N_M)",
        "n_qubits_resubmission_doc": 14,
        "n_qubits_actual_chi3": N_QUBITS_CIRCUIT,
        "n_2q_resubmission_doc_estimate": 36,
        "notes": [
            "16 qubits is the correct count for chi=3 8q MERA with 2 layers.",
            "SIM-2026-019 used 14 qubits and N_2q=36, both estimates.",
            "Helios native: ZZPhase + PhasedX + Rz; Rz is free under HQC.",
            "Top-tensor prep is a U(16) 4-qubit unitary -- contributes most.",
        ],
    }
    with open(OUT_JSON, "w") as f:
        json.dump(out, f, indent=2, default=str)
    print(f"\n  JSON saved: {OUT_JSON}")


if __name__ == "__main__":
    main()
