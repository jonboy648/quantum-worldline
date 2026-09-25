# =====================================================================================
# qw_ope_z2smoke.jl -- does the Z2-SYMMETRIC-tensor route work on this platform?
# =====================================================================================
# v3 gate run (qw_ope_pev.jl chi=6, 2026-07-02) FAILED with the discriminant: dense LBFGS
# MERAs sit in a GENERIC GAUGE, where the Z2 symmetry on internal legs is a finite-depth
# circuit, NOT a product of one-site P's -- so any one-site parity lift/projection is
# structurally invalid on dense basins. The clean fix is Z2-symmetric tensors (Z2Space):
# parity is then EXACT by construction, sigma = lowest ODD-sector scaling operator, zero
# cross-sector contamination possible.
# v1's header warned "Z2-symmetric tensors trip a TensorKitManifolds polar-Newton LAPACK
# bug (LAPACKException(23)) on this platform", but the demo (RUN-MERAKIT.md's documented
# working invocation) IS Z2 + ternary; the bug note plausibly refers to the expand_bonddim
# RAMP path. THIS SMOKE: direct-init at target chi with Z2Space, LBFGS, small iters --
# just answer: does it optimize without LAPACK exceptions, and do the two sectors give the
# Ising even/odd towers (even: 0, ~1, ~2; odd: ~0.125, ~1.125)?
#
# Run: julia +1.8 --project=. qw_ope_z2smoke.jl [K0] [K1] [NSEED] [MAXITER]
#   defaults: 3 3 2 250  (chi = K0+K1 split as Z2Space(0=>K0, 1=>K1))
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

LinearAlgebra.BLAS.set_num_threads(1)

function main()
    k0    = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 3
    k1    = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 3
    nseed = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 2
    miter = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 250
    println("="^78)
    println("qw_ope_z2smoke.jl -- Z2-symmetric direct-init viability test")
    println("Z2Space(0=>$k0, 1=>$k1)  seeds=$nseed  maxiter=$miter  layers=3")
    println("="^78)
    h = DemoTools.ising_hamiltonian(; symmetry = :Z2, block_size = 2)
    exact = -4 / pi
    Vv = Z2Space(0 => k0, 1 => k1)
    Vs = (space(h, 1), Vv, Vv)
    for s in 1:nseed
        println("\n[seed $s] optimizing (direct-init, no ramp)...")
        flush(stdout)
        Random.seed!(s)
        local m
        try
            m = random_MERA(TernaryMERA, Float64, Vs)
            pars = (gradient_delta = 1e-8, maxiter = miter, method = :lbfgs, verbosity = 0)
            m = minimize_expectation(m, h, pars)
        catch err
            println("  seed $s FAILED: ", sprint(showerror, err)[1:min(end, 300)])
            flush(stdout)
            continue
        end
        E = real(expect(h, m))
        @printf("  E=%.8f  err=%.3e\n", E, E - exact)
        sd = scalingdimensions(m, 12)
        for (sector, dims) in sd
            ds = sort(real.(dims))
            @printf("  sector %-12s dims: %s\n", string(sector), string(round.(ds[1:min(6, end)], digits = 4)))
        end
        flush(stdout)
    end
    println("\nQW_OPE_Z2SMOKE DONE")
end

main()
