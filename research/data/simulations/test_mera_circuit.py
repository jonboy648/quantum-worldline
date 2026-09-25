"""
Test: what does U_MERA |0...0> look like?
Find the correct circuit structure for the analytical MERA state preparation.
"""
import numpy as np
from scipy.sparse import csr_matrix, eye as speye, kron as skron
from scipy.sparse.linalg import eigsh

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

sqrt3 = np.sqrt(3.0)
u_dag = ((sqrt3+2)/4 * np.kron(I2,I2) + (sqrt3-2)/4 * np.kron(Z,Z) +
         1j/4 * np.kron(X,Y) + 1j/4 * np.kron(Y,X))
u = u_dag.conj().T
sqrt2 = np.sqrt(2.0)
w_dag = ((sqrt3+sqrt2)/4 * np.kron(I2,I2) + (sqrt3-sqrt2)/4 * np.kron(Z,Z) +
         1j*(1+sqrt2)/4 * np.kron(X,Y) + 1j*(1-sqrt2)/4 * np.kron(Y,X))
w = w_dag.conj().T

print("u matrix:")
print(np.round(u.real, 4))
print("w matrix:")
print(np.round(w.real, 4))

# u[:,0] maps |00> -> ?
print("\nu|00> =", np.round(u[:,0], 4))
print("w|00> =", np.round(w[:,0], 4))
# w[:,0] = [sqrt3/2, 0, 0, 1/2] = sqrt3/2 |00> + 1/2 |11>
# This is an entangled state! Good -- it will spread entanglement through the circuit.

def apply_gate_to_sv(sv, gate, a, b, n):
    dim = 2**n
    result = np.zeros(dim, dtype=complex)
    for idx in range(dim):
        bit_a = (idx >> (n-1-a)) & 1
        bit_b = (idx >> (n-1-b)) & 1
        old_2bit = bit_a * 2 + bit_b
        idx_base = idx & ~(1 << (n-1-a)) & ~(1 << (n-1-b))
        for new_2bit in range(4):
            coeff = gate[new_2bit, old_2bit]
            if abs(coeff) < 1e-15: continue
            new_bit_a = (new_2bit >> 1) & 1
            new_bit_b = new_2bit & 1
            new_idx = idx_base | (new_bit_a << (n-1-a)) | (new_bit_b << (n-1-b))
            result[new_idx] += coeff * sv[idx]
    return result

L = 8
I2s = speye(2, format="csr")
Xs = csr_matrix(X)
Zs = csr_matrix(Z)

def sp(n, i, p):
    paulis = {"X": Xs, "Z": Zs}
    mats = [paulis[p] if k == i else I2s for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = skron(out, m, format="csr")
    return out

def zz_corr(sv, i, j, n):
    ZZ = sp(n, i, "Z") @ sp(n, j, "Z")
    return float(np.real(sv.conj() @ (ZZ @ sv)))

def get_energy(sv, H):
    return float(np.real(sv.conj() @ (H @ sv)))

# TFIM OBC ground state
H_tfim = csr_matrix((2**L, 2**L), dtype=complex)
for i in range(L-1):
    H_tfim = H_tfim - sp(L, i, "Z") @ sp(L, i+1, "Z")
for i in range(L):
    H_tfim = H_tfim - sp(L, i, "X")
E0_arr, psi0_arr = eigsh(H_tfim, k=1, which="SA")
E0 = E0_arr[0]
psi0 = psi0_arr[:, 0]
print(f"\nTFIM L=8 OBC: E0={E0:.6f}")

print("\nExact TFIM ZZ correlators from site 0:")
for dr in range(1, 8):
    ZZ = sp(L, 0, "Z") @ sp(L, dr, "Z")
    c = float(np.real(psi0.conj() @ (ZZ @ psi0)))
    print(f"  C(0,{dr}) = {c:.6f}")

print("\nPredicted power-law: C(r) ~ r^(-1/4):")
for dr in range(1, 8):
    print(f"  C(0,{dr}) ~ {dr**(-0.25):.6f}")

# ---------------------------------------------------------------
# The key insight: The analytical MERA (Evenbly-White 2016) is
# specifically designed for the CRITICAL TFIM or equivalently the
# XX model. The state U|0> should already have power-law correlations
# because the MERA tensors are optimized to encode a CFT.
#
# Let me try the standard brick-wall MERA circuit for TFIM:
# The MERA for TFIM uses H gates (or X rotations) at the IR.
# Following the standard MERA for free fermions:
# - At each layer: Hadamard on even sites, then CX (CNOT) between adjacent pairs

# APPROACH: Build U_MERA as a CIRCUIT and apply to |0>
# The standard MERA circuit for a CFT:
# Layer 1 (coarsest, operates on all qubits):
#   Apply w to pairs: (0,1),(2,3),(4,5),(6,7) -- these are the isometries
#   Apply u to pairs: (1,2),(3,4),(5,6)       -- disentanglers between
# Layer 2 (finer, operates on all qubits):
#   Apply w to pairs: (0,1),(2,3),(4,5),(6,7)
#   Apply u to pairs: (1,2),(3,4),(5,6)
# This is the "MERA as a quantum circuit" state prep.

# Try all combinations of w,u orderings and which gates go where
configs = []

# Config 1: w then u, same pairs for both, 2 layers
sv = np.zeros(2**L, dtype=complex); sv[0] = 1.0
for layer in range(2):
    for i in range(0, L, 2):
        sv = apply_gate_to_sv(sv, w, i, i+1, L)
    for i in range(1, L-1, 2):
        sv = apply_gate_to_sv(sv, u, i, i+1, L)
E = get_energy(sv, H_tfim)
print(f"\nConfig 1 (w_even + u_odd, 2 layers): E={E:.4f} (err={100*(E-E0)/abs(E0):.1f}%)")
configs.append(("w_even+u_odd x2", sv.copy(), E))

# Config 2: u then w
sv = np.zeros(2**L, dtype=complex); sv[0] = 1.0
for layer in range(2):
    for i in range(1, L-1, 2):
        sv = apply_gate_to_sv(sv, u, i, i+1, L)
    for i in range(0, L, 2):
        sv = apply_gate_to_sv(sv, w, i, i+1, L)
E = get_energy(sv, H_tfim)
print(f"Config 2 (u_odd + w_even, 2 layers): E={E:.4f} (err={100*(E-E0)/abs(E0):.1f}%)")
configs.append(("u_odd+w_even x2", sv.copy(), E))

# Config 3: alternating offsets
sv = np.zeros(2**L, dtype=complex); sv[0] = 1.0
for i in range(0, L, 2):
    sv = apply_gate_to_sv(sv, w, i, i+1, L)
for i in range(1, L-1, 2):
    sv = apply_gate_to_sv(sv, u, i, i+1, L)
for i in range(1, L-1, 2):
    sv = apply_gate_to_sv(sv, w, i, i+1, L)
for i in range(0, L, 2):
    sv = apply_gate_to_sv(sv, u, i, i+1, L)
E = get_energy(sv, H_tfim)
print(f"Config 3 (alternating offset): E={E:.4f} (err={100*(E-E0)/abs(E0):.1f}%)")
configs.append(("alternating", sv.copy(), E))

# Config 4: w_dag (ascending) + u_dag (ascending) = the coarsening direction
# This is what holographic_transport_16q.py uses as the "ascending" operator
sv = np.zeros(2**L, dtype=complex); sv[0] = 1.0
for layer in range(2):
    for i in range(0, L, 2):
        sv = apply_gate_to_sv(sv, w_dag, i, i+1, L)
    for i in range(1, L-1, 2):
        sv = apply_gate_to_sv(sv, u_dag, i, i+1, L)
E = get_energy(sv, H_tfim)
print(f"Config 4 (w_dag + u_dag, 2 layers): E={E:.4f} (err={100*(E-E0)/abs(E0):.1f}%)")
configs.append(("wdag+udag x2", sv.copy(), E))

# Show ZZ correlators for the best config
best = min(configs, key=lambda x: x[2])
print(f"\nBest config: {best[0]} with E={best[2]:.4f}")
sv_best = best[1]
print("ZZ correlators:")
for dr in range(1, 8):
    c = zz_corr(sv_best, 0, dr, L)
    pl = dr**(-0.25)
    print(f"  C(0,{dr}) = {c:.6f}  (power-law: {pl:.6f})")

# ---------------------------------------------------------------
# IMPORTANT ALTERNATIVE: Don't prepare the MERA state from scratch.
# Instead, use the FACT that holographic_transport_16q.py already
# found the true ground state of H_W&H (via eigsh).
#
# That ground state HAS power-law ZZ correlations (it IS the CFT vacuum).
#
# For hardware, prepare the MERA ground state using the OPTIMAL CIRCUIT ANSATZ:
# - Use our VQE theta parameters (already in theta_opt_SIM2026002.npy)
# - The VQE circuit is already parameterized by u,w-style gates
# - At 1.87% error, it SHOULD have reasonable ZZ correlations
#
# Or: Use the EXACT ground state and decompose into a circuit using
# qiskit's state_preparation feature.

print("\n\nChecking VQE ground state ZZ correlators from SIM-2026-002...")
import os
theta_path = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026002.npy"
if os.path.exists(theta_path):
    theta = np.load(theta_path)
    print(f"  Theta loaded: {len(theta)} params")
else:
    print("  theta_opt_SIM2026002.npy not found")
