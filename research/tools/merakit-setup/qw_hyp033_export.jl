# qw_hyp033_export.jl -- HYP-033 (PREREGISTRATION-HYP033.md, REGISTERED 2026-09-22).
#
# Optimize the Z2-symmetric critical-Ising ternary MERA with the VALIDATED SIM-061 pipeline
# (qw_ope_pev_z2.jl: optimize_ising_mera_z2, sector_dims, densify_mera -- included, not copied, so
# there is exactly one definition of each), then export what the Python cut-Gram driver needs:
#   layer l = 1..3 : dense u_l (bottom1 bottom2 top1 top2) and w_l (leg1 leg2 leg3 top), ComplexF64,
#                    column-major, TensorKit convert(Array) layout (codomain first, then domain)
#   H2             : the 2-site Hamiltonian ascended through layers 1 and 2, i.e. the operator that
#                    lives on the 3-site ring below the scale-invariant layer  (out1 out2 in1 in2)
#   info.txt       : E_inf = expect(h, m), sector-resolved Delta_sigma / Delta_eps (gate G4 input),
#                    the SIM-061 basin verdict, wall time
# The 27-site state itself (layers 1, 2 + a top tensor on the 3-site ring = ground state of the
# H2 ring) is assembled in Python; nothing here evaluates the registered observable.
#
# ARGS: k0 k1 seed_lo seed_hi maxiter hfield outdir      (chi = k0 + k1; SIM-061: 3 3 = chi 6, 4 4 = chi 8)
#   hfield = 1.0 critical (registered), 1.5 = control C-GAPPED
using Random, LinearAlgebra, Printf, TensorKit, MERAKit, KrylovKit
include(joinpath(@__DIR__, "qw_ope_pev_z2.jl"))   # guarded: does not run its main()

function optimize_z2(k0, k1; layers = 3, seed = 1, maxiter = 2500, hfield = 1.0)
    # identical to optimize_ising_mera_z2 except that h is a parameter (C-GAPPED needs 1.5)
    Random.seed!(seed)
    h = DemoTools.ising_hamiltonian(-1.0, hfield; symmetry = :Z2, block_size = 2)
    Vv = Z2Space(0 => k0, 1 => k1)
    Vs = (space(h, 1), ntuple(_ -> Vv, layers - 1)...)
    m = random_MERA(TernaryMERA, Float64, Vs)
    pars = (gradient_delta = 1e-8, maxiter = maxiter, method = :lbfgs, verbosity = 0)
    m = minimize_expectation(m, h, pars)
    return m, h, real(expect(h, m))
end

function dump(io_meta, dir, name, A::AbstractArray)
    A = ComplexF64.(A)
    open(joinpath(dir, name * ".bin"), "w") do io
        write(io, A)                      # column-major, ComplexF64
    end
    println(io_meta, name, " ", ndims(A), " ", join(size(A), " "))
end

function export_seed(k0, k1, seed, maxiter, hfield, outdir)
    t0 = time()
    m_z2, h, E = optimize_z2(k0, k1; seed = seed, maxiter = maxiter, hfield = hfield)
    d_sig, d_eps, deven, dodd = sector_dims(m_z2)
    basin_clean = isfinite(d_sig) && abs(d_sig - 0.125) < 0.10 &&
                  isfinite(d_eps) && abs(d_eps - 1.0) < 0.20      # SIM-061 analyze() criterion
    md = densify_mera(m_z2)
    nt = num_translayers(md)
    H2 = convert(Array, ascend(h, m_z2, 3, 1))     # through layers 1 and 2; same sector-ordered basis
    dir = joinpath(outdir, @sprintf("chi%d_h%.2f_seed%d", k0 + k1, hfield, seed))
    mkpath(dir)
    open(joinpath(dir, "meta.txt"), "w") do meta
        for l in 1:(nt + 1)
            layer = getlayer(md, l)
            dump(meta, dir, "u$l", convert(Array, layer.disentangler))
            dump(meta, dir, "w$l", convert(Array, layer.isometry))
        end
        dump(meta, dir, "H2", H2)
    end
    open(joinpath(dir, "info.txt"), "w") do io
        @printf(io, "chi %d\nk0 %d\nk1 %d\nseed %d\nhfield %.4f\nmaxiter %d\nlayers %d\n", k0 + k1, k0, k1, seed, hfield, maxiter, nt + 1)
        @printf(io, "E_inf %.12f\nexact_critical %.12f\n", E, -4 / pi)
        @printf(io, "d_sig %.6f\nd_eps %.6f\nbasin_clean %s\n", d_sig, d_eps, basin_clean)
        println(io, "deven ", join([@sprintf("%.5f", x) for x in deven], " "))
        println(io, "dodd ", join([@sprintf("%.5f", x) for x in dodd], " "))
        @printf(io, "seconds %.1f\n", time() - t0)
    end
    @printf("seed %d  chi %d  h %.2f  E=%.8f  Dsig=%.4f Deps=%.4f  clean=%s  [%.0fs] -> %s\n",
            seed, k0 + k1, hfield, E, d_sig, d_eps, basin_clean, time() - t0, dir)
    flush(stdout)
end

function main()
    k0     = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 3
    k1     = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 3
    s_lo   = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 1
    s_hi   = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 8
    miter  = length(ARGS) >= 5 ? parse(Int, ARGS[5]) : 2500
    hfield = length(ARGS) >= 6 ? parse(Float64, ARGS[6]) : 1.0
    outdir = length(ARGS) >= 7 ? ARGS[7] : "hyp033_networks"
    println("HYP-033 export: Z2($k0,$k1) chi=$(k0+k1) seeds $s_lo..$s_hi maxiter=$miter h=$hfield -> $outdir")
    for s in s_lo:s_hi
        try
            export_seed(k0, k1, s, miter, hfield, outdir)
        catch err
            println("seed $s FAILED: ", sprint(showerror, err)[1:min(end, 400)])
        end
    end
end

if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
