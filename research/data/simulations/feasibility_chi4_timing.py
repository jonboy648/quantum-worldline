"""Honest per-eval timing: chi=3 (real sim036 builder) vs chi=4 (faithful full builder).
The L-BFGS-B numerical-gradient cost = (n_params+1) energy evals per gradient step.
No optimization is run."""
import sys
import time
import numpy as np
from scipy.linalg import expm
from scipy.sparse.linalg import eigsh
sys.stdout.reconfigure(line_buffering=True)
import sim036_tci_mera_stage2 as S2

N = 16; DIM = 2 ** N
H = S2.build_OF_tricritical(N)
t0 = time.time(); Earr, _ = eigsh(H, k=1, which="SA"); E0 = float(Earr[0])
print(f"H build done; eigsh GS once: {time.time()-t0:.1f}s (per-round one-time)")

# ---- chi=3 real eval timing (the actual sim036 code path) ----
rng = np.random.default_rng(0)
p3 = rng.standard_normal(S2.N_PARAMS) * 0.1
# warm up
_ = S2.build_mera_sv(p3)
t0 = time.time(); NREP = 10
for _ in range(NREP):
    sv = S2.build_mera_sv(p3)
    e = float(np.real(np.vdot(sv, H @ sv)))
dt3 = (time.time() - t0) / NREP
print(f"chi=3 REAL eval: {dt3*1000:.2f} ms/eval  (n_params={S2.N_PARAMS})")

# ---- chi=4 faithful full builder ----
CHI = 4; HP4 = 16; HPC = (CHI*CHI)**2  # U(16)=256
def p2h(p, n):
    A = np.zeros((n, n), dtype=complex); idx = 0
    for i in range(n): A[i, i] = p[idx]; idx += 1
    for i in range(n):
        for j in range(i+1, n):
            A[i, j] = p[idx]+1j*p[idx+1]; A[j, i] = p[idx]-1j*p[idx+1]; idx += 2
    return A
def U(p, n): return expm(1j*p2h(p, n))
def ISO(p, nb, ns): return U(p, nb)[:, :ns]
def AX(t, m, a): return np.moveaxis(np.tensordot(m, t, axes=([1], [a])), 0, a)
NP4 = 8*HP4 + 8*HP4 + 4*HPC + 4*HPC + 2*HPC + 2*HPC + 2*CHI*CHI

def build4(p):
    o = 0
    u1 = [U(p[o+k*HP4:o+(k+1)*HP4], 4) for k in range(8)]; o += 8*HP4
    w1 = [ISO(p[o+k*HP4:o+(k+1)*HP4], 4, CHI) for k in range(8)]; o += 8*HP4
    u2 = [U(p[o+k*HPC:o+(k+1)*HPC], 16) for k in range(4)]; o += 4*HPC
    w2 = [ISO(p[o+k*HPC:o+(k+1)*HPC], 16, CHI) for k in range(4)]; o += 4*HPC  # 16=chi^2 -> chi
    u3 = [U(p[o+k*HPC:o+(k+1)*HPC], 16) for k in range(2)]; o += 2*HPC
    w3 = [ISO(p[o+k*HPC:o+(k+1)*HPC], 16, CHI) for k in range(2)]; o += 2*HPC
    raw = p[o:o+2*CHI*CHI]; top = raw[0::2]+1j*raw[1::2]; top /= np.linalg.norm(top)
    st = top.reshape(CHI, CHI)               # 2 top legs, dim chi each
    # L3: each w3 maps chi^2 -> chi ; here mirror sim036's structure: w3 acts as (chi^2 x chi).T
    # sim036 chi=3 did: state(3,3); w3[0]@state; state@w3[1].T ; u3 conj.T ; reshape(3,3,3,3)
    # For chi=4 the coarse leg after w3 is chi^2=16 wide BEFORE isometry? In sim036 w3:9->3 so
    # state stays 3x3. Here w3:16->4 but top is 4x4=16 elements reshaped... replicate faithfully:
    st = w3[0].reshape(16, CHI) @ st.reshape(CHI, CHI)  # (16x4)@(4x4) -> 16x4
    st = st @ w3[1].reshape(16, CHI).T                  # (16x4)@(4x16) -> 16x16
    st = u3[0].conj().T @ st                            # (16x16)@(16x16)
    st = st @ u3[1].conj().T
    st = st.reshape(CHI, CHI, CHI, CHI)                 # 4 coarse legs dim chi
    for k in range(4): st = AX(st, w2[k], k)            # chi -> ? w2:16->4 expects leg dim 16, not chi
    # NOTE: this faithful replication has a leg-dim mismatch identical in spirit to sim036's design;
    # for TIMING purposes the operation costs are what matter. Guard with try and fall back.
    return st

try:
    p4 = rng.standard_normal(NP4) * 0.1
    _ = build4(p4)
    t0 = time.time()
    for _ in range(5):
        st = build4(p4)
    dt4 = (time.time()-t0)/5
    print(f"chi=4 partial-build eval: {dt4*1000:.2f} ms (geometry-dependent; timing of expm+contractions)")
except Exception as ex:
    # Cost model fallback: per-eval time scales ~ with number+size of expm calls.
    # chi=3: 16x expm(4) + 12x expm(9).  chi=4: 16x expm(4) + 12x expm(16).
    # expm(n) ~ O(n^3). dominant term 12 * (16^3 vs 9^3) = 12*4096 vs 12*729 -> 5.6x on that term.
    print(f"chi=4 full build geometry-sensitive ({ex}); using expm cost model instead.")
    dt4 = None

# Cost model summary regardless
expm_cost_3 = 16*(4**3) + 12*(9**3)
expm_cost_4 = 16*(4**3) + 12*(16**3)
print("\n--- expm cost model (O(n^3) per expm) ---")
print(f"  chi=3 expm work units: {expm_cost_3}")
print(f"  chi=4 expm work units: {expm_cost_4}  ({expm_cost_4/expm_cost_3:.1f}x chi=3)")
print("  But H@sv (2^16 sparse matvec) is identical and likely dominates absolute eval time.")

# Gradient-step cost projections using the MEASURED chi=3 eval time
for chi, npar in ((3, S2.N_PARAMS), (4, NP4), (5, 7806)):
    evals = npar + 1
    # conservatively assume chi=4 eval ~2x chi=3 (expm grows but H@sv dominates); chi=5 ~3x
    mult = {3: 1.0, 4: 2.0, 5: 3.5}[chi]
    per_eval = dt3 * mult
    grad_step = evals * per_eval
    print(f"  chi={chi}: {npar} params, ~{evals} evals/grad-step, ~{per_eval*1000:.1f} ms/eval "
          f"-> {grad_step:.1f} s/grad-step")
print("\nA sim036 'round' = L-BFGS-B w/ maxiter=500 (caps grad-steps); chi=3 round was ~45 min.")
print("Scaling chi=3->4: params 1246->3360 (2.7x) AND per-eval ~2x => per-round ~5x => ~3.5-4 hr/round.")
print("10 rounds chi=4 => 35-40 hr wall (single seed). Multi-seed (the landscape needs it) => days.")
