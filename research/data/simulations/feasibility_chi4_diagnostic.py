"""
HYP-027 chi=4 feasibility diagnostic (READ-ONLY, no optimization).
1. Re-confirm the TCI exact GS Schmidt spectrum at the middle cut (independent check).
2. Inspect the SIM-036 chi=3 checkpoint state: is it product-like (optimizer collapse)
   or genuinely entangled-but-truncated? Report its Schmidt spectrum + single-site <Z>.
3. Print the chi=4 MERA param-count arithmetic and the dominant per-energy-eval cost terms.
Fast: seconds. Uses sparse eigsh + a single 16q statevector build.
"""
import sys
import numpy as np
from scipy.sparse.linalg import eigsh

sys.stdout.reconfigure(line_buffering=True)
import sim036_tci_mera_stage2 as S2

N = S2.N_QUBITS  # 16


def schmidt(sv, n, l):
    m = sv.reshape(2 ** l, 2 ** (n - l))
    s = np.linalg.svd(m, compute_uv=False)
    p = (s ** 2)
    p = p / p.sum()
    S = float(-np.sum(p[p > 1e-15] * np.log(p[p > 1e-15])))
    return S, p


def avg_abs_Z(sv, n):
    # <|Z_j|> averaged over sites: product-state ferromagnet -> ~1; critical -> small
    vals = []
    probs = np.abs(sv) ** 2
    for j in range(n):
        # Z_j eigenvalue is +1 if bit j == 0 else -1; compute <Z_j>
        idx = np.arange(len(sv))
        bit = (idx >> (n - 1 - j)) & 1
        z = np.where(bit == 0, 1.0, -1.0)
        vals.append(abs(float(np.sum(probs * z))))
    return float(np.mean(vals)), vals


print("=" * 70)
print("HYP-027 chi=4 FEASIBILITY DIAGNOSTIC")
print("=" * 70)

# --- exact TCI GS ---
H = S2.build_OF_tricritical(N)
Earr, gsarr = eigsh(H, k=1, which="SA")
E0 = float(Earr[0])
gs = S2.project_z2(gsarr[:, 0], N)
S_ex, p_ex = schmidt(gs, N, N // 2)
print(f"\nexact TCI GS: E0={E0:.6f}  S_half={S_ex:.5f}")
print("  top-8 Schmidt^2:", np.round(p_ex[:8], 6).tolist())
print("  Schmidt rank (>1e-10):", int(np.sum(p_ex > 1e-10)))
azx, _ = avg_abs_Z(gs, N)
print(f"  exact GS  mean |<Z_j>| = {azx:.4f}  (critical -> small; product ferro -> ~1)")

# --- SIM-036 chi=3 checkpoint state ---
import os
CKPT = "D:/quantum-worldline/research/data/simulations/theta_tci_SIM2026036.npy"
if os.path.exists(CKPT):
    theta = np.load(CKPT)
    sv = S2.project_z2(S2.build_mera_sv(theta), N)
    E_m = float(np.real(np.vdot(sv, H @ sv)))
    ov = float(abs(np.vdot(gs, sv)) ** 2)
    S_m, p_m = schmidt(sv, N, N // 2)
    azm, _ = avg_abs_Z(sv, N)
    print(f"\nSIM-036 chi=3 MERA checkpoint ({len(theta)} params):")
    print(f"  E_mera={E_m:.6f}  rel_err={abs(E_m-E0)/abs(E0)*100:.3f}%  overlap={ov:.4f}")
    print(f"  S_half(MERA)={S_m:.6f}")
    print("  top-8 Schmidt^2:", np.round(p_m[:8], 6).tolist())
    print("  Schmidt rank (>1e-10):", int(np.sum(p_m > 1e-10)))
    print(f"  MERA mean |<Z_j>| = {azm:.4f}")
    print("  --> if |<Z>|~1 and S~0: state collapsed to a product/cat ferromagnet (optimizer trap)")
else:
    print("\n(no SIM-036 checkpoint found)")

# --- chi=4 param-count arithmetic ---
print("\n" + "=" * 70)
print("chi=4 MERA PARAMETER COUNT")
print("=" * 70)
for chi in (3, 4, 5):
    # layer1: disentanglers U(4) [physical legs, d=2 so d^2=4 -> unchanged]; isometries U(4)->chi
    #   actually w1 maps 2 phys legs (dim 4) -> chi ; param of isometry generator = full U(n_big)=n_big^2
    # The script uses make_isometry(params, n_big, n_small) -> expm of n_big x n_big Hermitian.
    # chi=3: u1 U(4)=16, w1 U(4)=16 ; u2/w2 U(9)=81 ; u3/w3 U(9)=81. Top tensor = chi^2 complex.
    # For general chi: coarse-leg dim is chi, so 2 coarse legs -> chi^2; disentangler on 2 coarse
    #   legs is U(chi^2); isometry maps chi^2 -> chi i.e. generator U(chi^2)=(chi^2)^2=chi^4.
    HP_phys = 16  # U(4) always (physical legs dim 2)
    HP_coarse = (chi * chi) ** 2  # U(chi^2) generator param count = (chi^2)^2
    # layer counts (8-boundary-site, 3-layer, mirrors sim036 structure):
    #  L1: 8 u1 (U4) + 8 w1 (U4 isometry ->chi)
    #  L2: 4 u2 (U(chi^2)) + 4 w2 (U(chi^2) isometry)
    #  L3: 2 u3 (U(chi^2)) + 2 w3 (U(chi^2) isometry)
    #  top: chi^2 complex amps -> 2*chi^2 real
    # Note: at chi=3, U(chi^2)=U(9)=81 -> matches the 81 in the script. At chi=4 -> U(16)=256.
    n = 8 * HP_phys + 8 * HP_phys + 4 * HP_coarse + 4 * HP_coarse + 2 * HP_coarse + 2 * HP_coarse + 2 * chi * chi
    print(f"  chi={chi}: U(chi^2)=U({chi*chi}) generator={HP_coarse} params each; "
          f"top={2*chi*chi}; TOTAL n_params = {n}")

print("\n" + "=" * 70)
print("PER-EVAL COST DRIVERS (16q statevector build, all chi)")
print("=" * 70)
print("  - statevector dim is ALWAYS 2^16 = 65536 (independent of chi) -> no blowup from chi")
print("  - H @ sv : sparse matvec, ~O(nnz)=O(16 * 2^16), unchanged by chi")
print("  - expm() calls: 8x U(4) + 8x U(4) + 12x U(chi^2). At chi=4, U(16) expm is 16x16 -> trivial")
print("  - tensordot contractions: intermediate tensors are chi^k; chi=4 vs 3 -> (4/3)^8 ~ 10x on")
print("    the largest L1 intermediate, but absolute size (4^8=65536) is tiny -> sub-second")
print("  CONCLUSION: chi=4 does NOT blow up any dense step. 2^16 statevector is the ceiling.")
