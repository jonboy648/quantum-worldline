"""
Reusable scaling-dimension readout from a saved scale-invariant MERA checkpoint.

Uses the VALIDATED 3-site grad-based ascending scaling superoperator from
binary_mera_superop.py (ascend_matrix), NOT the older one-site construction (which was
gauge-trivial / disentangler-absorbable; see REFERENCE-binary-mera-superop.md).

Δ = -log2(λ), normalized so the identity (λ=1) gives Δ=0. For critical Ising the leading
tower is [0, 0.125 (σ), 1.0 (ε), 1.125 (σ'), 2.0 (T), ...].

Usage: python read_spectrum.py <checkpoint.npz>
"""
import sys

import numpy as np

from binary_mera_superop import ascend_matrix

try:
    sys.stdout.reconfigure(encoding="utf-8")
except Exception:
    pass


def dims_from_matrix(S, n=14):
    """Leading scaling dimensions from the ascending superoperator matrix S (chi^6 x chi^6).
    Returns (deltas, lambdas) sorted by |λ| descending, normalized to Δ[0]=0."""
    from scipy.sparse.linalg import eigs
    k = min(n, S.shape[0] - 2)
    lam = eigs(S, k=k, which="LM", return_eigenvectors=False)
    lam = np.sort(np.abs(lam))[::-1]
    lam = lam[lam > 1e-9]
    d = -np.log2(lam)
    return d - d[0], lam


def central_charge_correct(w, u, chi, n_descend=40):
    """c = 3(S(ρ2) - S(ρ1))/ln2  (Calabrese-Cardy; the /ln2 is essential).
    ρ1, ρ2 from the bulk descending fixed point."""
    import torch
    from binary_mera_superop import binary_mera_energy_torch

    def _T(a):
        return torch.tensor(a, dtype=torch.complex128)

    wt, ut = _T(w), _T(u)
    rho = _T((np.eye(chi ** 3) / chi ** 3).reshape((chi,) * 6))
    # Descending fixed point: ρ ← descend(ρ) = grad(E, op) with current ρ as the rho-arg.
    # E = <rho, A(op)> is LINEAR in op, so grad wrt op = A†(rho) = the descended density matrix
    # (independent of op's value). Iterate to the fixed point.
    for _ in range(n_descend):
        ot = torch.zeros((chi,) * 6, dtype=torch.complex128, requires_grad=True)
        E = binary_mera_energy_torch(ot, rho, wt, ut)
        g, = torch.autograd.grad(E, ot)
        Mx = torch.conj(g).resolve_conj().reshape(chi ** 3, chi ** 3)
        Mx = 0.5 * (Mx + Mx.conj().T)
        rho = (Mx / torch.trace(Mx)).reshape((chi,) * 6)
    r3 = np.asarray(rho.detach()).reshape((chi,) * 6)
    rho2 = np.trace(r3, axis1=2, axis2=5).reshape(chi * chi, chi * chi)
    rho1 = np.trace(rho2.reshape(chi, chi, chi, chi), axis1=1, axis2=3)

    def S(r):
        ev = np.linalg.eigvalsh((r + r.conj().T) / 2)
        ev = ev[ev > 1e-12]
        return float(-np.sum(ev * np.log(ev)))
    s1 = S(rho1)
    c = 3 * (S(rho2) - s1) / np.log(2)
    return c, s1


def main():
    path = sys.argv[1] if len(sys.argv) > 1 else "uw_ISING_evsched.npz"
    d = np.load(path)
    w, u = d["w"], d["u"]
    chi = w.shape[0]
    print(f"checkpoint: {path}  chi={chi}")
    if "c" in d:
        print(f"  stored c = {float(d['c']):.4f}")

    c, s1 = central_charge_correct(w, u, chi)
    print(f"  recomputed c = {c:.4f}  (CFT: Ising 0.5 / TCI 0.70);  s1 = {s1:.4f}  (CFT ~0.47)")

    print("  building ascending superoperator matrix (chi^6 = %d)..." % (chi ** 6), flush=True)
    S = ascend_matrix(u, w)
    deltas, lam = dims_from_matrix(S)
    print("  Ising tower target: [0, 0.125 (sigma), 1.0 (eps), 1.125, 2.0 (T)]")
    print("  measured D:", np.round(deltas[:8], 4))
    print("  lambda   :", np.round(lam[:8], 4))


if __name__ == "__main__":
    main()
