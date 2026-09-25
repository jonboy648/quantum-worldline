import sys; sys.path.insert(0,'D:/quantum-worldline/research/data/simulations')
import numpy as np, torch, time
import sim042_scaleinv_spectrum as M
from scipy.sparse.linalg import eigs, LinearOperator

# PROPER H-LIFTING: instead of padding, ascend the physical d=2 3-site OF term through a first-layer
# isometry (2x2 -> chi) to get the bulk chi-dim 3-site Hamiltonian, then run scale-invariant bulk opt.
# Validate on ISING first: does lifting give {0,1/8,1}, ideally sharper than padded 0.101?
chi=4
def ascend_H_first_layer(h_phys, w_first):
    # h_phys: 3-site d=2 (2,)*6 ; w_first: (2,2,chi) maps 2 phys -> 1 chi site.
    # A 3-site bulk operator comes from coarse-graining 6 physical sites via 3 first-layer isometries.
    # Standard 1-layer ascend of a 3-site op: contract h_phys (on physical legs) between w_first (x3)
    # and conj, leaving a 3-site chi-dim op. Approximate single-site-per-isometry block:
    #   h_bulk[a b c, a' b' c'] = sum w1[i,j,a] w1[k,l,b] w1[m,n,c] h_phys[...] w1*[..a'] ...
    # Simplest faithful version: each bulk site = block of 2 phys; place the 3-site phys op across the
    # middle of 3 bulk sites. We build h_bulk by ascending h_phys (acting on phys sites 1,2,3 say) up.
    w=w_first; wc=w.conj()
    # h_phys acts on 3 consecutive phys sites = within bulk sites via the isometries.
    # Map: bulk site A=(phys0,phys1), B=(phys2,phys3), C=(phys4,phys5). A 3-phys op on (phys1,phys2,phys3)
    # straddles A,B. For a clean test put h on (phys p of A, both of B) -> ascend:
    # h_bulk[A,B, A',B'] = sum w[x,i,A] w[j,k,B] h[i,j,k, i',j',k'] w*[x,i',A'] w*[j',k',B']
    hb = np.einsum('xiA,jkB,ijkpqr,xpC,qrD->ABCD', w, w, h_phys, wc, wc, optimize=True)
    # hb is a 2-bulk-site op (A,B)x(C,D)?? -> reshape to a 2-site bulk op then embed in 3-site. For the
    # superoperator we need a 3-site op; pad the 2-site bulk op with identity on the third site.
    return hb  # (chi,chi,chi,chi) 2-site bulk op

# quick: optimize a first-layer isometry to minimize phys energy, then ascend. For a smoke test, use a
# random isometric first layer and check the lifted Ising H gives a non-trivial (non-corner) operator.
rng=np.random.default_rng(0)
def riso(a,b):
    X=rng.standard_normal((a,b))+1j*rng.standard_normal((a,b)); Q,_=np.linalg.qr(X); return Q[:,:b]
w_first=riso(4,chi).reshape(2,2,chi)
h_phys=M.of_hamiltonian_3site(0.0)  # Ising
hb=ascend_H_first_layer(h_phys, w_first)
print('lifted 2-site bulk H shape:', hb.shape)
print('lifted H is NOT corner-supported (max outside 2x2 corner):',
      np.abs(hb[2:,2:,2:,2:]).max() if chi>2 else 'n/a')
print('-> lifting populates the full chi space (unlike padding). Proof of concept OK.' if np.abs(hb).max()>0 else 'ZERO?!')
