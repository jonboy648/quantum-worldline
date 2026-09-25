"""
Part 2: the decisive question. At L=8 does the THERMAL transport observable
actually move with beta? Compute N_eff(beta) participation ratio, and a proxy
transport signal: the thermal real-time response <Z0(t)>_beta after a Y-kick,
to see whether the *envelope/structure* changes with beta at all at this size.
Also: does the curve emerge, or is the 256-state spectrum too sparse?
"""
import numpy as np
import scipy.linalg as sla

I2 = np.eye(2, dtype=complex)
X = np.array([[0, 1], [1, 0]], dtype=complex)
Y = np.array([[0, -1j], [1j, 0]], dtype=complex)
Z = np.array([[1, 0], [0, -1]], dtype=complex)

def pauli_full(n, i, P):
    mats = [P if k == i else I2 for k in range(n)]
    out = mats[0]
    for m in mats[1:]:
        out = np.kron(out, m)
    return out

def build_H(L):
    dim = 2 ** L
    H = np.zeros((dim, dim), dtype=complex)
    pref = L / (4 * np.pi)
    Xs = [pauli_full(L, i, X) for i in range(L)]
    Zs = [pauli_full(L, i, Z) for i in range(L)]
    for j in range(L):
        H += pref * (Xs[(j-1)%L] @ Zs[j] @ Xs[(j+1)%L] - Xs[j] @ Xs[(j+1)%L])
    return H

L = 8
H = build_H(L)
evals, evecs = np.linalg.eigh(H)
print(f"L={L}, dim={2**L}, E0={evals[0]:.6f}")
print(f"First 8 levels (relative to E0): {(evals[:8]-evals[0]).round(4)}")

print("\nParticipation ratio N_eff(beta) = (sum w)^2 / sum w^2, w=exp(-beta E_n):")
for beta in [100, 20, 8, 5, 3, 2, 1, 0.5, 0.25]:
    w = np.exp(-beta * (evals - evals[0]))
    Neff = (w.sum())**2 / (w**2).sum()
    print(f"  beta={beta:6.2f}  N_eff={Neff:8.3f}")

# Thermal real-time transport proxy: kick Y on site 0, watch <Z on antipode>(t)
# at several beta. We do this on the physical Hilbert space directly (mixed rho),
# which is exactly what the TFD physical half reproduces.
print("\nThermal transport proxy: kick = exp(-i*eps*Y_0), observable Z_{L/2} (antipode).")
print("Tr[U(t) Uk rho_th Uk^d U^d Z_anti] minus baseline, peak->dip->reappear structure.")
site_kick = 0
site_obs = L // 2
eps = 0.5
Yk = pauli_full(L, site_kick, Y)
Zo = pauli_full(L, site_obs, Z)
Uk = sla.expm(-1j * eps * Yk)
ts = np.arange(0, 6.01, 0.05)
# precompute eigen-time evolution: U(t) = evecs diag(e^{-i E t}) evecs^d
def evolve_expect(rho0):
    # returns <Zo>(t) - <Zo>_baseline(thermal, no kick) for the time series
    sig = np.zeros(len(ts))
    # diagonalize once: work in energy basis
    rho_e = evecs.conj().T @ rho0 @ evecs
    Zo_e = evecs.conj().T @ Zo @ evecs
    for k, t in enumerate(ts):
        phase = np.exp(-1j * evals * t)
        # U rho U^d in energy basis: element (m,n) -> phase_m * rho_e[m,n] * conj(phase_n)
        rt = (phase[:, None] * rho_e) * np.conj(phase)[None, :]
        sig[k] = np.real(np.sum(rt * Zo_e.T))  # Tr[rt Zo] = sum_mn rt[m,n] Zo_e[n,m]
    return sig

results = {}
for beta in [100, 5, 2, 1, 0.5]:
    rho_th = evecs @ np.diag(np.exp(-beta*(evals-evals[0]))) @ evecs.conj().T
    rho_th /= np.trace(rho_th).real
    base = evolve_expect(rho_th)  # no kick -> stationary baseline (commutes with H)
    rho_k = Uk @ rho_th @ Uk.conj().T
    sig = evolve_expect(rho_k) - base
    results[beta] = sig
    # find peak, dip, reappear in |sig|
    a = np.abs(sig)
    pk = np.argmax(a[:40])
    diprel = np.argmin(a[pk:pk+80]); dip = pk+diprel
    rep = dip + 10 + np.argmax(a[dip+10:]) if dip+10 < len(a) else dip
    Ttrans = ts[rep]-ts[dip]
    print(f"  beta={beta:6.2f}  peak_t={ts[pk]:.2f} (|{a[pk]:.4f}|)  "
          f"dip_t={ts[dip]:.2f} (|{a[dip]:.5f}|)  reapp_t={ts[rep]:.2f}  T={Ttrans:.2f}  "
          f"max|sig|={a.max():.5f}")

# Quantify how much the *shape* differs between cold and hot
import numpy as np
cold = results[100]; hot = results[1]
print(f"\nShape divergence cold(beta=100) vs hot(beta=1): "
      f"max|diff|={np.max(np.abs(cold-hot)):.5f}, "
      f"rms={np.sqrt(np.mean((cold-hot)**2)):.5f}, "
      f"cold_amp={np.max(np.abs(cold)):.5f}, hot_amp={np.max(np.abs(hot)):.5f}")
