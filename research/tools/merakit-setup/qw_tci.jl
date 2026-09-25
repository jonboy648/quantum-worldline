# QW: O'Brien-Fendley TCI via MERAKit. Loads the CORRECTLY-WEIGHTED dim-8-blocked OF 2-site operator
# (built + weight-verified in Python: term fully-in-a-block -> 1/2, straddling -> 1, the block_op tiling).
# block_size=3 -> dim-8 effective sites so the first MERA layer (8->chi) admits chi=6. TernaryMERA.
# lam3=0 -> Ising control (must give sigma=0.125, Delta_T=2); lam3=0.856 -> TCI c=7/10, read Delta_T.
using Random, LinearAlgebra, TensorKit, MERAKit, DelimitedFiles

function load_hb(tag)
    M = readdlm("hb_lam3_$(tag).txt", Float64)            # 64x64 real
    Vb = ComplexSpace(8)
    return TensorMap(ComplexF64.(M), Vb ⊗ Vb, Vb ⊗ Vb)
end

function run_of(tag, lam3, chi, maxiter; seed=1, layers=3)
    Random.seed!(seed)
    h = load_hb(tag)
    Vphys = ComplexSpace(8); Vv = ComplexSpace(chi)
    Vs = (Vphys, ntuple(_->Vv, layers-1)...)
    m = random_MERA(TernaryMERA, ComplexF64, Vs)
    pars = (gradient_delta=1e-7, maxiter=maxiter, method=:lbfgs, verbosity=1)
    m = minimize_expectation(m, h, pars)
    E = expect(h, m); sd = scalingdimensions(m)
    dims = sort(real.(get(sd, Trivial(), Float64[])))
    println("=== OF lam3=$lam3 chi=$chi seed=$seed: E=$E ===")
    println("SCALDIMS sorted: ", round.(dims[1:min(10,end)], digits=4))
    flush(stdout)
    return m, dims
end

# Ising control FIRST. Gate: lowest nonzero dim ~ 0.125 (sigma), a dim ~1 (eps), a dim ~2 (Delta_T).
run_of("0", 0.0, 6, 2500; seed=1)
println("QW_OF_CONTROL DONE")
