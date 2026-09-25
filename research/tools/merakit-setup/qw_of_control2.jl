# Validate: OF lam3=0 built PURELY from block_op (1-site X + 2-site ZZ, the proven primitive) -> chi=6
# MERA -> must give sigma=0.125, Delta_T=2. If yes, the 1+2-site path is correct (only 3-site needs care).
using Random, LinearAlgebra, TensorKit, MERAKit
include("demo/demo_tools.jl"); using .DemoTools

function of_12site(lam=1.0)
    V = ComplexSpace(2)
    X = TensorMap(ComplexF64[0 1; 1 0], V, V)
    Z = TensorMap(ComplexF64[1 0; 0 -1], V, V)
    h1 = DemoTools.block_op(-2.0*lam*X, 2)      # dim-4 blocked 1-site
    h2 = DemoTools.block_op(-2.0*lam*(Z ⊗ Z), 2) # dim-4 blocked 2-site
    return h1 + h2
end

Random.seed!(1)
h = of_12site()
Vphys = ComplexSpace(4)
Vs = (Vphys, ComplexSpace(4), ComplexSpace(6), ComplexSpace(6))
m = random_MERA(TernaryMERA, ComplexF64, Vs)
pars = (gradient_delta=1e-7, maxiter=2500, method=:lbfgs, verbosity=1)
m = minimize_expectation(m, h, pars)
sd = scalingdimensions(m); dims = sort(real.(get(sd, Trivial(), Float64[])))
println("=== OF lam3=0 (block_op 1+2-site) chi=6: E=$(expect(h,m)) ===")
println("SCALDIMS: ", round.(dims[1:min(10,end)], digits=4))
println("QW_CONTROL2 DONE")
