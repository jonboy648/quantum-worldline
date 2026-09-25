# QW: Ising chi=6 control via MERAKit Riemannian LBFGS, initialized DIRECTLY at the target bond dim
# (avoids the broken expand_bonddim -> LAPACKException(15)). Random init at sector-3 (total dim 6),
# optimize from scratch. Multi-seed since random-init MERA can hit local minima.
using Random, LinearAlgebra, TensorKit, MERAKit
include("demo/demo_tools.jl"); using .DemoTools

function run_direct(sectordim, maxiter; seed=1, layers=3)
    Random.seed!(seed)
    h = DemoTools.ising_hamiltonian(; symmetry=:Z2, block_size=2)
    exact = -4/pi
    Vphys = space(h, 1)
    Vv = Z2Space(0=>sectordim, 1=>sectordim)          # total bond dim = 2*sectordim
    Vs = (Vphys, ntuple(_->Vv, layers-1)...)
    m = random_MERA(TernaryMERA, Float64, Vs)
    pars = (gradient_delta=1e-7, maxiter=maxiter, method=:lbfgs, verbosity=1)
    m = minimize_expectation(m, h, pars)
    E = expect(h, m); sd = scalingdimensions(m)
    println("=== DIRECT sector=$sectordim total=$(2*sectordim) seed=$seed: E_err=$(E-exact) ===")
    println("SCALDIMS even: ", get(sd, Z2Irrep(0), []))
    println("SCALDIMS odd:  ", get(sd, Z2Irrep(1), []))
    flush(stdout)
    return m, E-exact, sd
end

# chi=6 = sector 3. Try a couple seeds, keep going.
for s in (1, 2)
    try
        run_direct(3, 3000; seed=s)
    catch e
        println("seed $s FAILED: ", e); flush(stdout)
    end
end
println("QW_ISING_CHI6 DONE")
