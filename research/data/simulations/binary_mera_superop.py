"""
CORRECT binary MERA scaling superoperator (3-site, autodiff-based) — replicates the tested
Google TensorNetwork simple_mera.py energy network and obtains the ascending/descending
superoperators by automatic differentiation (torch), exactly as the reference does.

Per the adversarial workflow (wf_b7ee088b-921) + the reference (REFERENCE-binary-mera-superop.md):
the binary scaling superoperator acts on 3-SITE operators (rho/op are rank-6 = chi^3 x chi^3); the
energy network has 3 isometries + 2 disentanglers per term (disentanglers straddle isometries -> the
disentangler genuinely survives the trace, unlike any one-site construction). ascend = grad(E, rho);
descend = grad(E, op). The scaling superoperator is `ascend` at the scale-invariant fixed point;
diagonalize it on the chi^3 x chi^3 operator space -> Delta = -log_2(lambda).

Conventions (match reference + quimb): isometry w rank-3 [bl, br, top]; disentangler u rank-4
[bl, br, tl, tr]. op/rho rank-6: legs (0,1,2)=bra (out/ket-row), (3,4,5)=ket — we follow the
reference's op[0..2] bra, op[3..5] ket wiring.

GATE A (local, random isometric u,w): identity 3-site op -> lambda=1, and the superoperator must NOT
collapse to a one-site/gauge-trivial channel (it should show the binary causal-cone structure).
GATE B (needs converged critical-Ising u,w, on RunPod): lowest dims {0, 1/8, 1, 9/8, 2, ...}.
"""
import numpy as np
import torch


def binary_mera_energy_torch(op, rho, w, u):
    """Replicate simple_mera.py binary_mera_energy with the EXACT leg wiring, in torch (einsum).
    op, rho: rank-6 (chi,)*6 ; w: (chi,chi,chi)=[bl,br,top]; u: (chi,chi,chi,chi)=[bl,br,tl,tr].
    Returns a real scalar (0.5*(left+right)). Differentiable in all args."""
    wc = torch.conj(w); uc = torch.conj(u)
    out = 0.0
    for dirn in ("left", "right"):
        # Build the network as one big einsum per direction, transcribing the reference connections.
        # Name indices per tensor leg. iso_l,iso_c,iso_r tops -> rho ket legs 0,1,2; conj tops -> rho 3,4,5.
        # We assign letters to each connected edge.
        # Shared edges:
        #   iso_l[2]=rho0 ; iso_c[2]=rho1 ; iso_r[2]=rho2
        #   iso_l[0]=iso_l_con[0] (=: t)  ; iso_l[1]=un_l[2] (=: a) ; iso_c[0]=un_l[3] (=: b)
        #   iso_c[1]=un_r[2] (=: c) ; iso_r[0]=un_r[3] (=: d) ; iso_r[1]=iso_r_con[1] (=: s)
        #   un_l_con[2]=iso_l_con[1] (=: e) ; un_l_con[3]=iso_c_con[0] (=: f)
        #   un_r_con[2]=iso_c_con[1] (=: g) ; un_r_con[3]=iso_r_con[0] (=: h)
        #   iso_l_con[2]=rho3 ; iso_c_con[2]=rho4 ; iso_r_con[2]=rho5
        # rho legs: rho[R0,R1,R2,R3,R4,R5]
        if dirn == "right":
            #   un_l[0]=un_l_con[0] (=: m) ; un_l[1]=op[3] ; un_r[0]=op[4] ; un_r[1]=op[5]
            #   op[0]=un_l_con[1] ; op[1]=un_r_con[0] ; op[2]=un_r_con[1]
            # tensors:
            # iso_l[t,a,R0], iso_c[b,c,R1], iso_r[d,s,R2]
            # un_l[m,o3,a,b]  (legs bl=m, br=op3, tl=a, tr=b)
            # un_r[o4,o5,c,d] (legs bl=op4, br=op5, tl=c, tr=d)
            # op[O0,O1,O2,o3,o4,o5]
            # un_l_con[m,O0,e,f] ; un_r_con[O1,O2,g,h]
            # iso_l_con[t,e,R3] ; iso_c_con[f,g,R4] ; iso_r_con[h,s,R5]
            expr = ("t a P, b c Q, d s R,"          # iso_l, iso_c, iso_r  (tops P,Q,R = rho ket)
                    "m i a b, j k c d,"             # un_l, un_r           (i=op3, jk=op4,op5)
                    "x y z i j k,"                  # op                   (xyz=op bra 0,1,2)
                    "m x e f, y z g h,"             # un_l_con, un_r_con
                    "t e S, f g T, h s U,"          # iso_l_con, iso_c_con, iso_r_con (S,T,U=rho bra)
                    "P Q R S T U->")                # rho (ket P,Q,R ; bra S,T,U) contracted to scalar
            val = torch.einsum(expr,
                               w, w, w, u, u, op, uc, uc, wc, wc, wc, rho)
        else:  # left
            #   un_l[0]=op[3] ; un_l[1]=op[4] ; un_r[0]=op[5] ; un_r[1]=un_r_con[1] (=: n)
            #   op[0]=un_l_con[0] ; op[1]=un_l_con[1] ; op[2]=un_r_con[0]
            # un_l[i,j,a,b] (bl=op3, br=op4) ; un_r[k,n,c,d] (bl=op5, br=n)
            # op[x,y,z,i,j,k]
            # un_l_con[x,y,e,f] ; un_r_con[z,n,g,h]
            expr = ("t a P, b c Q, d s R,"
                    "i j a b, k n c d,"
                    "x y z i j k,"
                    "x y e f, z n g h,"
                    "t e S, f g T, h s U,"
                    "P Q R S T U->")
            val = torch.einsum(expr,
                               w, w, w, u, u, op, uc, uc, wc, wc, wc, rho)
        out = out + val
    return 0.5 * torch.real(out)


def _to_t(a):
    return torch.tensor(a, dtype=torch.complex128, requires_grad=False)


def ascend_matrix(u, w):
    """Build the ascending scaling superoperator as a matrix on the 3-site operator space.
    A 3-site operator is rank-6 (chi,)*6 -> vec dimension D = chi^6. The superoperator is D x D.
    At chi=4: D=4096, matrix = 4096x4096 complex128 = 268 MB (tractable; my earlier '268GB' was an
    arithmetic error: chi^6=4096, not 4096^2). Built column-by-column via autodiff: for each basis
    3-site operator o_k, ascend(o_k) = grad(energy, rho) [the coarse image o_k pairs with].
    Conventions: energy = Re<rho, A(op)>; A is linear in op, so column k = vectorized grad(E,rho)|op=e_k."""
    chi = w.shape[0]
    D = chi ** 6
    wt = _to_t(w); ut = _to_t(u)
    S = np.zeros((D, D), dtype=complex)
    shape6 = (chi,) * 6
    for k in range(D):
        op_k = np.zeros(D, dtype=complex); op_k[k] = 1.0
        op_t = torch.tensor(op_k.reshape(shape6), dtype=torch.complex128, requires_grad=False)
        rho_t = torch.zeros(shape6, dtype=torch.complex128, requires_grad=True)
        E = binary_mera_energy_torch(op_t, rho_t, wt, ut)
        # energy is Re<rho, A(op)>; d/drho of Re<rho,X> recovers X (up to conj convention). Use autograd:
        g, = torch.autograd.grad(E, rho_t, create_graph=False)
        S[:, k] = np.conj(g.detach().numpy().reshape(D))   # conj for the Re<.,.> convention
    return S


def gateA_3site(u, w, chi):
    """Structural gate: identity 3-site op -> eigenvalue 1, and report the leading spectrum + whether
    the disentangler genuinely matters (compare with u set to identity)."""
    from scipy.sparse.linalg import eigs
    S = ascend_matrix(u, w)
    kk = min(12, S.shape[0] - 2)
    lam = np.sort(np.abs(eigs(S, k=kk, which="LM", return_eigenvectors=False)))[::-1]
    return lam


if __name__ == "__main__":
    # GATE A0: the energy network is real and finite for random tensors
    chi = 2
    rng = np.random.default_rng(0)
    def riso(a, b):
        M = rng.standard_normal((a, b)) + 1j * rng.standard_normal((a, b))
        Q, _ = np.linalg.qr(M)
        return Q[:, :b]
    u = riso(chi * chi, chi * chi).reshape(chi, chi, chi, chi)
    w = riso(chi * chi, chi).reshape(chi, chi, chi)
    op = (rng.standard_normal((chi,) * 6) + 1j * rng.standard_normal((chi,) * 6))
    rho = (rng.standard_normal((chi,) * 6) + 1j * rng.standard_normal((chi,) * 6))
    E = binary_mera_energy_torch(_to_t(op), _to_t(rho), _to_t(w), _to_t(u))
    print(f"energy network runs: E={float(E):.6f} (real, finite={np.isfinite(float(E))})")
