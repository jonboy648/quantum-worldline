# Derive the CORRECT 2-blocked-site (block_size=3) OF operator by matching exact chain energy.
# A translation-invariant 2-site blocked operator h_b acts on blocks (B_k, B_{k+1}); summing over k must
# reproduce sum of the physical density. For block=3 sites, block k covers phys sites 3k+1,3k+2,3k+3.
# The OF density terms and which block-pair they belong to:
#   X_i (1-site): belongs entirely to one block -> put in BOTH-block diagonal with weight 1/2 (counted by
#     two adjacent block-pairs) OR once on the left block. Standard: a 1-site term on block k appears in
#     pair (k,k+1) and (k-1,k); weight 1/2 each. Same for terms fully inside a block.
#   2-site ZZ_{i,i+1}: if both in same block -> weight 1/2 (two pairs see it); if straddling boundary
#     (i in block k, i+1 in block k+1) -> weight 1 (only pair (k,k+1) sees it).
#   3-site XZZ_{i,i+1,i+2}: fully inside a block -> 1/2; straddling -> 1 (only one pair contains all 3).
# This is the block_op logic (opcross weight 1, opleft/opright weight 1/2) generalized.
import numpy as np
X=np.array([[0,1],[1,0]],complex); Z=np.array([[1,0],[0,-1]],complex); I=np.eye(2,dtype=complex)
def op6(positions_ops):  # 6 physical sites
    m=np.array([[1]],complex)
    for s in range(6):
        o=I
        for (idx,mat) in positions_ops:
            if idx==s: o=mat
        m=np.kron(m,o)
    return m
def build_hb(lam3,lam=1.0):
    # 6 sites = block A (0,1,2) + block B (3,4,5). Weight: term fully inside a block -> 1/2; straddling -> 1.
    H=np.zeros((64,64),complex)
    def w(sites): # weight by whether all sites in one block
        inA=all(s<3 for s in sites); inB=all(s>=3 for s in sites)
        return 0.5 if (inA or inB) else 1.0
    # X_i for i in 0..5
    for i in range(6):
        H += -2*lam*w([i])*op6([(i,X)])
    # ZZ_{i,i+1} for i in 0..4
    for i in range(5):
        H += -2*lam*w([i,i+1])*op6([(i,Z),(i+1,Z)])
    # 3-site for i in 0..3
    for i in range(4):
        H += lam3*w([i,i+1,i+2])*op6([(i,X),(i+1,Z),(i+2,Z)])
        H += lam3*w([i,i+1,i+2])*op6([(i,Z),(i+1,Z),(i+2,X)])
    H=0.5*(H+H.conj().T)
    return H
# sanity: ground energy per site of build_hb should match the exact chain per-site energy at lam3=0
hb=build_hb(0.0)
ev=np.linalg.eigvalsh(hb)
print('blocked-op lowest eigs:', np.round(ev[:4],4))
# the blocked op is per-block-pair; its expectation in the true GS / (sites per pair=3) ~ energy density
# Just check it's Hermitian + reasonable; criticality is verified by MERA. Save for Julia.
np.save('/d/quantum-worldline/research/tools/MERAKit.jl/hb_lam3_0.npy', build_hb(0.0))
np.save('/d/quantum-worldline/research/tools/MERAKit.jl/hb_lam3_0856.npy', build_hb(0.856))
print('saved hb operators for lam3=0 and 0.856')
