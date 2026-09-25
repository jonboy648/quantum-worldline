"""Ensemble-harden the dynamics-sensitivity crossover at beta*gap ~ O(1).
Denominator-safe metric: f(beta) = |<O>_A - <O>_B|(beta) / |<O>_A - <O>_B|(cold), in [0,1].
Efficiency: the eigenbasis diagonal <n|O|n> is beta-INDEPENDENT -> compute once per (H,O).
Ensemble: 2 sizes x 3 non-symmetry permutations x 2 observables.
"""
import numpy as np
import hyp024_tfd_btz_transport as TFD
from scipy.linalg import eigh

def perm_unitary(perm, L):
    dim = 2 ** L
    P = np.zeros((dim, dim))
    for idx in range(dim):
        bits = [(idx >> (L - 1 - j)) & 1 for j in range(L)]
        nb = 0
        for j in range(L):
            nb |= (bits[perm[j]] << (L - 1 - j))
        P[nb, idx] = 1.0
    return P

def eig_diag(evecs, Op):
    """<n|O|n> for all n, beta-independent. M = O @ evecs; diag = sum_i conj(evecs)_in M_in."""
    M = Op @ evecs
    return np.real(np.sum(evecs.conj() * M, axis=0))   # shape (dim,)

def thermal_from_diag(evals, diag, beta):
    w = np.exp(-beta * (evals - evals[0]))
    return float(np.sum(w * diag) / w.sum())

perms = {8: [[1,0,2,3,4,5,6,7],[2,0,1,3,4,5,6,7],[0,2,4,6,1,3,5,7]],
         10: [[2,0,1,3,4,5,6,7,8,9],[1,0,2,3,4,5,6,7,8,9],[0,2,4,6,8,1,3,5,7,9]]}
betas = np.array([200,50,20,10,5,3,2,1.5,1,0.7,0.5,0.3,0.2,0.1])

print("Denominator-safe crossover: f(beta)=|<O>_A-<O>_B|/cold, vs beta*gap. f=0.5 crossing.")
crossings = []
for L in [8, 10]:
    H = TFD.build_H_boundary(L).toarray()
    ev, evec = eigh(H); gap = ev[1] - ev[0]
    obs = {'Y0Ymid': (TFD.sparse_pauli_full(L,0,'Y') @ TFD.sparse_pauli_full(L,L//2,'Y')).toarray(),
           'Z0Zmid': (TFD.sparse_pauli_full(L,0,'Z') @ TFD.sparse_pauli_full(L,L//2,'Z')).toarray()}
    bg = betas * gap
    for perm in perms[L]:
        P = perm_unitary(perm, L); HB = P @ H @ P.T
        evB, evecB = eigh(HB)
        for onm, Op in obs.items():
            dA = eig_diag(evec, Op); dB = eig_diag(evecB, Op)
            disc = np.array([abs(thermal_from_diag(ev, dA, b) - thermal_from_diag(evB, dB, b)) for b in betas])
            cold = disc[0]
            if cold < 1e-9:
                continue
            f = disc / cold
            cross = None
            for i in range(len(f) - 1):
                if (f[i] - 0.5) * (f[i+1] - 0.5) < 0:
                    t = (0.5 - f[i]) / (f[i+1] - f[i])
                    cross = np.exp(np.log(bg[i]) + t * (np.log(bg[i+1]) - np.log(bg[i])))
                    break
            if cross:
                crossings.append(cross)
                print(f"  L={L} perm={perm[:3]}... obs={onm}: f=0.5 at beta*gap={cross:.2f}")
    print(f"L={L} done (gap={gap:.4f})")

crossings = np.array(crossings)
print(f"\nCrossover beta*gap (f=0.5), {len(crossings)} ensemble members:")
print(f"  mean={crossings.mean():.2f}, std={crossings.std():.2f}, "
      f"range=[{crossings.min():.2f},{crossings.max():.2f}], CV={crossings.std()/crossings.mean():.2f}")
print(f"  => crossover beta*gap ~ {crossings.mean():.2f} +/- {crossings.std():.2f}; "
      f"{'CONSISTENT (established)' if crossings.std()/crossings.mean()<0.5 else 'SCATTERED (not established)'}")
