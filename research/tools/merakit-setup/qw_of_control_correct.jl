# REAL CONTROL: feed the exact-diag-VERIFIED dim-4 OF operator (lam3=0) to MERAKit chi=6 and confirm
# Delta_sigma~0.125, Delta_eps~1, Delta_T~2 (matching SIM-050). Multi-seed; dense ComplexSpace(4) phys.
# Layer structure mirrors the WORKING Ising chi=6 driver (qw_ising_chi6.jl): layers=3, scale-inv space chi.
using Random, LinearAlgebra, TensorKit, MERAKit
include("demo/demo_tools.jl"); using .DemoTools

V = ComplexSpace(2)
X = TensorMap(ComplexF64[0 1; 1 0], V, V)
Z = TensorMap(ComplexF64[1 0; 0 -1], V, V)
e = id(V)
function place(pos_ops)
    ops = [e, e, e, e]
    for (p, o) in pos_ops; ops[p] = o; end
    return ops[1] ⊗ ops[2] ⊗ ops[3] ⊗ ops[4]
end
superset(pos) = Set(p<=2 ? 0 : 1 for p in pos)
wt(pos) = length(superset(pos))==1 ? 0.5 : 1.0
function of_blocked(lam3; lam=1.0)
    H4 = zero(place([(1,X)]))
    for p in 1:4;  H4 += -2.0*lam*wt([p])*place([(p,X)]); end
    for p in 1:3;  H4 += -2.0*lam*wt([p,p+1])*place([(p,Z),(p+1,Z)]); end
    if lam3 != 0.0
        for (a,b,c) in ((1,2,3),(2,3,4))
            H4 += lam3*wt([a,b,c])*place([(a,X),(b,Z),(c,Z)])
            H4 += lam3*wt([a,b,c])*place([(a,Z),(b,Z),(c,X)])
        end
    end
    H4 = 0.5*(H4 + H4')
    fs = V ⊗ V
    ft = isomorphism(fuse(fs), fs); fb = isomorphism(fs, fuse(fs))
    h = (ft ⊗ ft) * H4 * (fb ⊗ fb)
    # divide by block_size (2) to match per-site energy convention used by DemoTools
    return h / 2
end

function run_of(lam3, chi, maxiter; seed=1, layers=3)
    Random.seed!(seed)
    h = of_blocked(lam3)
    Vphys = ComplexSpace(4); Vv = ComplexSpace(chi)
    Vs = (Vphys, ntuple(_->Vv, layers-1)...)
    m = random_MERA(TernaryMERA, ComplexF64, Vs)
    pars = (gradient_delta=1e-7, maxiter=maxiter, method=:lbfgs, verbosity=1)
    m = minimize_expectation(m, h, pars)
    E = expect(h, m); sd = scalingdimensions(m)
    dims = sort(real.(get(sd, Trivial(), Float64[])))
    println("=== OF lam3=$lam3 chi=$chi seed=$seed: E=$E ===")
    println("SCALDIMS: ", round.(dims[1:min(12,end)], digits=4))
    flush(stdout)
    return dims
end

for s in (1, 2, 3)
    try
        run_of(0.0, 6, 1500; seed=s)
    catch err
        println("seed $s FAILED: ", err); flush(stdout)
    end
end
println("QW_OF_CONTROL_CORRECT DONE")
