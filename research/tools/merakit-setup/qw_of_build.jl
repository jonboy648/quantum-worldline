# Build OF Hamiltonian blocked to dim-4 (block 2 sites) as a single 2-blocked-site TensorMap, with ALL
# terms (1,2,3-site) tiled on a 4-physical-site window and fused (1,2)->A,(3,4)->B with ONE consistent
# fusion (so spaces always match). Tiling weights mirror block_op: a k-site term placed at each window
# position; weight = 1 if it straddles the A|B boundary (covers a site<=2 AND a site>=3), else 0.5.
using TensorKit, MERAKit, LinearAlgebra

function of_hamiltonian_blocked(lam3; lam=1.0)
    V = ComplexSpace(2)
    X = TensorMap(ComplexF64[0 1; 1 0], V, V)
    Z = TensorMap(ComplexF64[1 0; 0 -1], V, V)
    e = id(V)
    # helper: place a list of single-site ops at given 1-based positions in a 4-site window; identity else
    function place(pos_ops)
        ops = [e, e, e, e]
        for (p, o) in pos_ops; ops[p] = o; end
        return ops[1] ⊗ ops[2] ⊗ ops[3] ⊗ ops[4]
    end
    straddle(positions) = (minimum(positions) <= 2) && (maximum(positions) >= 3)
    wt(positions) = straddle(positions) ? 1.0 : 0.5
    H4 = zero(place([(1,X)]))   # 4-site zero operator
    # 1-site X at positions 1..4
    for p in 1:4
        H4 += -2.0*lam*wt([p])*place([(p,X)])
    end
    # 2-site ZZ at (1,2),(2,3),(3,4)
    for p in 1:3
        H4 += -2.0*lam*wt([p,p+1])*place([(p,Z),(p+1,Z)])
    end
    # 3-site XZZ+ZZX at (1,2,3),(2,3,4)
    if lam3 != 0.0
        for p in 1:2
            H4 += lam3*wt([p,p+1,p+2])*place([(p,X),(p+1,Z),(p+2,Z)])
            H4 += lam3*wt([p,p+1,p+2])*place([(p,Z),(p+1,Z),(p+2,X)])
        end
    end
    # fuse (1,2)->A, (3,4)->B with ONE isomorphism set (consistent spaces)
    fs = V ⊗ V
    ft = isomorphism(fuse(fs), fs)
    fb = isomorphism(fs, fuse(fs))
    h = (ft ⊗ ft) * H4 * (fb ⊗ fb)
    return h
end

for lam3 in (0.0, 0.856)
    h = of_hamiltonian_blocked(lam3)
    M = reshape(convert(Array, h), 16, 16)
    println("lam3=$lam3 eigs: ", round.(real.(sort(eigvals(M))[1:5]), digits=4))
end
