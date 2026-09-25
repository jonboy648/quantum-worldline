# =====================================================================================
# qw_potts_z3.jl -- 3-state Potts with Z3-SYMMETRIC tensors (sector-resolved dims)
# =====================================================================================
# WHY (2026-07-03): dense Potts (SIM-057/059) had a severe basin lottery (2/8 clean at
# chi=8). The v4 Ising lesson (qw_ope_pev_z2.jl, SIM-061): symmetric tensors eliminate it
# (12/12 clean) and make charge sectors exact. Port: optimize the Potts chain with Z3-graded
# tensors; sigma lives in charge-1 (Delta = 2/15 = 0.1333), sigma-bar in charge-2, eps and T
# in charge-0 (0.8 and 2.0). This is the RunPod chi=10-12 payload for HYP-025 (Delta_sigma).
#
# CONSTRUCTION SAFETY: the Hamiltonian is built in the X-eigen (charge/Fourier) basis and
# injected into the graded TensorMap via an EMPIRICALLY DERIVED fusion-tree index map (probe
# blocks -> convert(Array) -> see which dense entry lights up). Machine-precision validation
# against the dense reference spectrum is a hard gate before any optimization.
#
# Run: julia +1.8 --project=. qw_potts_z3.jl [K] [NSEED] [MAXITER]   (chi = 3K; default 2 2 800)
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

LinearAlgebra.BLAS.set_num_threads(1)

const W3 = exp(2im * pi / 3)

# ---- dense reference (standard clock basis), identical to qw_potts_measure.jl ----------
function potts_dense(f::Float64 = 1.0)
    Z = ComplexF64[1 0 0; 0 W3 0; 0 0 W3^2]
    X = ComplexF64[0 0 1; 1 0 0; 0 1 0]
    e3 = Matrix{ComplexF64}(I, 3, 3)
    Xs = X + X'
    bond = -(kron(Z, Z') + kron(Z', Z))
    field = -0.5 * f * (kron(Xs, e3) + kron(e3, Xs))
    return bond + field
end

# ---- charge (Fourier) basis: F[j,q] = w^(jq)/sqrt(3); X becomes diagonal ---------------
function charge_basis_h(f::Float64 = 1.0)
    F = [W3^(j * q) / sqrt(3) for j in 0:2, q in 0:2]
    @assert norm(F * F' - I) < 1e-12
    X = ComplexF64[0 0 1; 1 0 0; 0 1 0]
    Xq = F' * X * F
    @assert norm(Xq - Diagonal(Xq)) < 1e-12   # X diagonal in charge basis
    h9 = kron(F, F)' * potts_dense(f) * kron(F, F)
    @assert norm(imag.(h9)) < 1e-12           # real in charge basis
    return real.(h9), real.(diag(Xq))
end

# ---- graded 2-site H via empirical fusion-tree index map -------------------------------
# dense h9 index convention: kron(A,B) => site1 = SLOW index: dense (a-1)*3+b for (q1=a-1,q2=b-1)
function build_graded_h(f::Float64 = 1.0)
    h9, xdiag = charge_basis_h(f)
    V = ℂ[ℤ₃](0 => 1, 1 => 1, 2 => 1)
    VV = V ⊗ V
    t = TensorMap(zeros, Float64, VV, VV)
    # empirical map: for each sector block entry, which dense (row,col) does it hit?
    # probe each block entry of each charge sector once.
    secs = (ℤ₃(0), ℤ₃(1), ℤ₃(2))
    idxmap = Dict{Tuple{Int, Int, Int}, Tuple{Int, Int}}()   # (sector, i, j) -> dense (r, c)
    for (si, s) in enumerate(secs)
        blk = block(t, s)
        n = size(blk, 1)
        for i in 1:n, j in 1:n
            fill!(block(t, s), 0.0)
            block(t, s)[i, j] = 1.0
            arr = reshape(convert(Array, t), 9, 9)
            nz = findall(x -> abs(x) > 0.5, arr)
            @assert length(nz) == 1
            idxmap[(si, i, j)] = (nz[1][1], nz[1][2])
        end
        fill!(block(t, s), 0.0)
    end
    # fill from dense h9
    for ((si, i, j), (r, c)) in idxmap
        block(t, secs[si])[i, j] = h9[r, c]
    end
    # HARD GATE: graded == dense to machine precision
    err = norm(reshape(convert(Array, t), 9, 9) - h9)
    @printf("  [gate] graded-vs-dense injection err = %.2e\n", err)
    @assert err < 1e-12
    return t, V
end

# ---- optimize + sector dims ------------------------------------------------------------
function main()
    k     = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 2
    nseed = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 2
    miter = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 800
    chi = 3k
    println("="^78)
    println("qw_potts_z3.jl -- 3-state Potts, Z3-symmetric tensors")
    println("Z3Space(0=>$k,1=>$k,2=>$k) [chi=$chi]  seeds=$nseed  maxiter=$miter  layers=3")
    println("CFT targets: sigma(charge1)=2/15=0.1333  eps(charge0)=0.8  T(charge0)=2.0")
    println("="^78)
    t0 = time()

    hloc, V = build_graded_h(1.0)
    h = DemoTools.block_op(hloc, 2)     # 2-site block -> dim-9 super-site (Z3Space(0=>3,1=>3,2=>3))
    h = h / 2
    Vv = ℂ[ℤ₃](0 => k, 1 => k, 2 => k)
    Vs = (space(h, 1), Vv, Vv)

    results = []
    for s in 1:nseed
        println("\n[seed $s] optimizing (Z3 direct-init)...")
        flush(stdout)
        Random.seed!(s)
        local m
        try
            m = random_MERA(TernaryMERA, Float64, Vs)
            pars = (gradient_delta = 1e-8, maxiter = miter, method = :lbfgs, verbosity = 0)
            m = minimize_expectation(m, h, pars)
        catch err
            println("  seed $s FAILED: ", sprint(showerror, err)[1:min(end, 300)])
            flush(stdout); continue
        end
        E = real(expect(h, m))
        @printf("  E=%.8f\n", E)
        sd = scalingdimensions(m, 12)
        tower = Dict{Int, Vector{Float64}}()
        for (sec, dims) in sd
            q = sec == ℤ₃(0) ? 0 : (sec == ℤ₃(1) ? 1 : 2)
            tower[q] = sort(real.(dims))
        end
        d_sig  = haskey(tower, 1) && !isempty(tower[1]) ? tower[1][1] : NaN
        d_sigb = haskey(tower, 2) && !isempty(tower[2]) ? tower[2][1] : NaN
        ch0 = get(tower, 0, Float64[])
        ch0nz = filter(d -> d > 0.05, ch0)
        d_eps = isempty(ch0nz) ? NaN : ch0nz[argmin(abs.(ch0nz .- 0.8))]
        d_T   = isempty(ch0nz) ? NaN : ch0nz[argmin(abs.(ch0nz .- 2.0))]
        clean = isfinite(d_sig) && abs(d_sig - 2 / 15) < 0.08 && isfinite(d_eps) && abs(d_eps - 0.8) < 0.2
        for q in 0:2
            haskey(tower, q) && @printf("  charge-%d tower: %s\n", q, string(round.(tower[q][1:min(5, end)], digits = 4)))
        end
        @printf("  Dsig=%.4f (.1333)  Dsig_bar=%.4f  Deps=%.4f (.8)  D_T=%.4f (2.0)  alpha=2*D_T=%.3f  [%s]\n",
                d_sig, d_sigb, d_eps, d_T, 2 * d_T, clean ? "CLEAN" : "BAD")
        flush(stdout)
        push!(results, (seed = s, d_sig = d_sig, d_sigb = d_sigb, d_eps = d_eps, d_T = d_T, clean = clean))
    end

    isempty(results) && (println("\nALL SEEDS FAILED."); return)
    println("\n" * "="^78)
    println("SUMMARY:")
    for r in results
        @printf("  seed %d: Dsig=%.4f Dsig_bar=%.4f Deps=%.4f D_T=%.4f alpha=%.3f %s\n",
                r.seed, r.d_sig, r.d_sigb, r.d_eps, r.d_T, 2 * r.d_T, r.clean ? "CLEAN" : "BAD")
    end
    nclean = count(r -> r.clean, results)
    @printf("clean basins: %d/%d (dense chi=8 was 2/8 -- symmetric route target: most/all)\n",
            nclean, length(results))
    println("="^78)
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_POTTS_Z3 DONE")
end

main()
