# OF Hamiltonian blocked to dim-4 (block_size=2) as a SINGLE SquareTensorMap{2}, block_op-faithful.
# Strategy (the space-consistency fix): build ONE 4-physical-site (A,B) window operator, where
#   - the 1+2-site OF density is FOLDED into a 2-site density d_j = -2lam*ZZ - lam*(X_j + X_{j+1})
#     and placed on the 3 bonds of the window with block_op weights (cross=1, intra-block=0.5);
#   - the 3-site OF terms are tiled with weight 1/(#super-pair-windows containing the site-set):
#     inside-one-block=0.5 (never happens for k=3), spanning-two-blocks=1.0.
# Then fuse (1,2)->A,(3,4)->B with ONE isomorphism set. Everything is a {2}-op so addition is legal.
using TensorKit, MERAKit, LinearAlgebra
include("demo/demo_tools.jl"); using .DemoTools

function of_hamiltonian_blocked(lam3; lam=1.0)
    V = ComplexSpace(2)
    X = TensorMap(ComplexF64[0 1; 1 0], V, V)
    Z = TensorMap(ComplexF64[1 0; 0 -1], V, V)
    e = id(V)
    function place(pos_ops)
        ops = [e, e, e, e]
        for (p, o) in pos_ops; ops[p] = o; end
        return ops[1] ⊗ ops[2] ⊗ ops[3] ⊗ ops[4]
    end
    H4 = zero(place([(1,X)]))
    # --- 1+2 site: folded 2-site density on each bond, block_op weights ---
    ZZ(i) = place([(i,Z),(i+1,Z)])
    Xi(i) = place([(i,X)])
    dens(i) = -2.0*lam*ZZ(i) - lam*(Xi(i) + Xi(i+1))   # OF folded 2-site density on bond (i,i+1)
    H4 += 1.0*dens(2)          # cross bond (2,3): straddles A|B -> weight 1
    H4 += 0.5*dens(1)          # intra-A bond (1,2): weight 0.5
    H4 += 0.5*dens(3)          # intra-B bond (3,4): weight 0.5
    # --- 3 site: window tiling, weight = 1/(#windows containing the 3 sites) ---
    if lam3 != 0.0
        w3(S) = (all(s<=2 for s in S) || all(s>=3 for s in S)) ? 0.5 : 1.0  # 3 sites always straddle -> 1.0
        for p in 1:2
            H4 += lam3*w3([p,p+1,p+2])*place([(p,X),(p+1,Z),(p+2,Z)])
            H4 += lam3*w3([p,p+1,p+2])*place([(p,Z),(p+1,Z),(p+2,X)])
        end
    end
    # --- fuse with ONE isomorphism set (matches block_op) ---
    fusionspace = V ⊗ V
    fusetop = isomorphism(fuse(fusionspace), fusionspace)
    fusebottom = isomorphism(fusionspace, fuse(fusionspace))
    h = (fusetop ⊗ fusetop) * H4 * (fusebottom ⊗ fusebottom)
    return h
end

# ---- GATE 1: lam3=0 must EQUAL block_op of the folded Ising density (machine precision) ----
V = ComplexSpace(2)
X = TensorMap(ComplexF64[0 1; 1 0], V, V)
Z = TensorMap(ComplexF64[1 0; 0 -1], V, V)
e = id(V)
ising_dens = -2.0*(Z⊗Z) - 1.0*((X⊗e) + (e⊗X))   # matches dens() above
href = DemoTools.block_op(ising_dens, 2)
hours = of_hamiltonian_blocked(0.0)
Mr = reshape(convert(Array, href), 16, 16)
Mo = reshape(convert(Array, hours), 16, 16)
println("GATE1 lam3=0: max|of_blocked - block_op(folded Ising)| = ", maximum(abs.(Mo - Mr)))
println("  eigs ours: ", round.(real.(sort(eigvals(Mo))[1:5]), digits=6))
println("  eigs ref : ", round.(real.(sort(eigvals(Mr))[1:5]), digits=6))

# ---- GATE 2: Hermiticity + spectra at lam3=0.856 ----
ht = of_hamiltonian_blocked(0.856)
Mt = reshape(convert(Array, ht), 16, 16)
println("GATE2 lam3=0.856: Hermiticity err = ", maximum(abs.(Mt - Mt')))
println("  eigs: ", round.(real.(sort(eigvals(Mt))[1:5]), digits=5))
println("OF_BUILD_V2 DONE")
