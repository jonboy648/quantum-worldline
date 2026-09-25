# qw_yanglee_pt.jl — PAPER-133 (2606.16785v2) reproduction, Phase 1
#
#   julia qw_yanglee_pt.jl <Lmin> <Lmax>       (defaults 8 16; even L only not required)
#
# H_YL = -sum_j (sz_j sz_{j+1} + lambda sx_j + i h sz_j), PBC, lambda = 4 (their Table I).
# Per L: bisect the finite-size exceptional point h_c^L (lowest PT pair coalescence),
# then evaluate biorthogonal projected amplitudes at h = h_c^inf (extrapolated) with the
# X preparation, and extract g_1 and the NEGATIVE ratio R -> -(1+sqrt5)/2 = -1.618034.
# Gate: g_1 within ~1% of 0.725073, R negative within ~2%.
#
# eta = parity P = prod sx (their Eq. 10): left eigenvector = P * right eigenvector
# (valid while the spectrum is real, i.e. h < h_c^L: ALWAYS work at h_c^inf < h_c^L).
# Design + traps: HYP028-BIORTHO-KS-DESIGN.md. Phase 2 (biorthogonal KS elements) waits
# on this gate.

using LinearAlgebra, SparseArrays, Printf
using KrylovKit

const LAMBDA = 4.0
const NEV    = 6

# --- operators on the 2^L basis (bit b=0 -> up, sz=+1) ---------------------------
function build_H(L::Int, h::Float64)
    dim = 2^L
    rows = Int[]; cols = Int[]; vals = ComplexF64[]
    diag = zeros(ComplexF64, dim)
    for s in 0:dim-1
        # sz_j sz_{j+1} (PBC) and i h sz_j on the diagonal
        zz = 0.0; mz = 0.0
        for j in 0:L-1
            bj  = (s >> j) & 1
            bj1 = (s >> ((j+1) % L)) & 1
            zz += (bj == bj1) ? 1.0 : -1.0
            mz += (bj == 0) ? 1.0 : -1.0
        end
        diag[s+1] = -zz - im*h*mz
        # -lambda sx_j : spin flips
        for j in 0:L-1
            push!(rows, xor(s, 1 << j) + 1); push!(cols, s+1); push!(vals, -LAMBDA)
        end
    end
    Hs = sparse(rows, cols, vals, dim, dim)
    Hs + spdiagm(0 => diag)
end

parity_apply(v::Vector{ComplexF64}, L::Int) = v[[xor(s, 2^L - 1) + 1 for s in 0:2^L-1]]

# --- lowest eigenpairs (non-Hermitian, smallest real part) ------------------------
function low_eigs(H, dim; nev=NEV)
    vals, vecs, info = eigsolve(x -> H*x, randn(ComplexF64, dim), nev, EigSorter(real; rev=false);
                                ishermitian=false, krylovdim=max(30, 3nev), tol=1e-11, maxiter=300)
    vals[1:min(nev, length(vals))], vecs[1:min(nev, length(vals))]
end

# --- finite-size exceptional point: bisect on Im(E) of the low pair ---------------
function find_hcL(L::Int; hlo=0.0, hhi=6.0, tol=2e-6)
    dim = 2^L
    broken = h -> begin
        vals, _ = low_eigs(build_H(L, h), dim, nev=4)
        maximum(abs.(imag.(vals[1:2]))) > 1e-6
    end
    @assert !broken(hlo) "h_lo already PT-broken"
    @assert broken(hhi)  "h_hi not PT-broken -- raise hhi"
    while hhi - hlo > tol
        hm = (hlo + hhi)/2
        broken(hm) ? (hhi = hm) : (hlo = hm)
    end
    (hlo + hhi)/2
end

# --- biorthogonal projected amplitudes with the X preparation ---------------------
function projections(L::Int, h::Float64)
    dim = 2^L
    vals, vecs = low_eigs(build_H(L, h), dim)
    @assert maximum(abs.(imag.(vals[1:2]))) < 1e-8 "complex low spectrum at h=$h (working point must be PT-unbroken)"
    X = fill(ComplexF64(2.0^(-L/2)), dim)          # eta-invariant: P|X> = |X>
    Zs = ComplexF64[]
    for i in 1:2                                    # phi-tower GS (global lowest), 1-tower GS
        R = vecs[i]
        Lv = parity_apply(R, L)                     # left eigenvector as a ket
        push!(Zs, (dot(X, R) * dot(Lv, X)) / dot(Lv, R))
    end
    real(vals[1]), real(vals[2]), Zs[1], Zs[2]      # E_phi, E_1, Z_{X,phi}, Z_{X,1}
end

function main(Lmin::Int, Lmax::Int)
    println("="^70)
    println("Yang-Lee PT chain (lambda=$LAMBDA): PAPER-133 Phase-1 reproduction")
    Ls = collect(Lmin:2:Lmax)
    hcs = Float64[]
    for L in Ls
        hc = find_hcL(L)
        push!(hcs, hc)
        @printf("  L=%2d  h_c^L = %.7f\n", L, hc)
    end
    # h_c^inf: fit h_c^L = h_c^inf + a L^-b  (expect b ~ 12/5 from y_phi)
    best = (Inf, 0.0, 0.0, 0.0)
    for b in 0.8:0.01:4.0
        A = [ones(length(Ls)) [Float64(L)^-b for L in Ls]]
        coef = A \ hcs
        r = norm(A*coef - hcs)
        r < best[1] && (best = (r, coef[1], coef[2], b))
    end
    _, hcinf, a, b = best
    @printf("h_c^inf = %.7f  (a=%.4f, b=%.2f; expect b~2.4)\n", hcinf, a, b)

    println("\nbiorthogonal projections at h = h_c^inf:")
    println("L, E_phi, E_1, Z_phi, Z_1, R=Z_1/Z_phi")
    Rs = Float64[]; logZphi = Float64[]
    for L in Ls
        Ephi, E1, Zphi, Z1 = projections(L, hcinf)
        R = real(Z1/Zphi)
        push!(Rs, R); push!(logZphi, -log(abs(real(Zphi))))
        @printf("  %2d  %+.6f  %+.6f  %+.6e%+.1e im  %+.6e  R=%.6f\n",
                L, Ephi, E1, real(Zphi), imag(Zphi), real(Z1), R)
    end
    # R extrapolation: R(L) = R_inf + r1/L + r2/L^2, with drop-smallest-L variants
    Rinfs = Float64[]; g1s = Float64[]
    for drop in 0:min(2, length(Ls)-4)
        Lw = Ls[1+drop:end]; Rw = Rs[1+drop:end]; Zw = logZphi[1+drop:end]
        A = [ones(length(Lw)) [1.0/L for L in Lw] [1.0/L^2 for L in Lw]]
        cR = A \ Rw
        A2 = [Float64.(Lw) ones(length(Lw)) [1.0/L for L in Lw]]
        c2 = A2 \ Zw
        g1v = sqrt(abs(exp(-c2[2])))
        push!(Rinfs, cR[1]); push!(g1s, g1v)
        @printf("\n[window L>=%d]  R_inf = %.6f   g_1 = %.6f\n", Lw[1], cR[1], g1v)
    end
    Rbest = Rinfs[end]; g1best = g1s[end]
    println("targets: R = -(1+sqrt5)/2 = -1.618034,  g_1 = ((5-sqrt5)/10)^(1/4) = 0.725073")
    ok = abs(g1best - 0.725073) < 0.01 && Rbest < 0 && abs(Rbest + 1.618034) < 0.05
    println(ok ? "\nGATE: PASSED" : "\nGATE: NOT PASSED -- inspect before Phase 2")
end

# projections-only mode at an externally supplied h (skips EP bisection):
#   julia qw_yanglee_pt.jl proj <h> <Lmin> <Lmax>
if length(ARGS) >= 1 && ARGS[1] == "proj"
    hfix = parse(Float64, ARGS[2])
    Ls = collect(parse(Int, ARGS[3]):2:parse(Int, ARGS[4]))
    println("projections at fixed h = $hfix")
    println("L, E_phi, E_1, Z_phi, Z_1, R")
    for L in Ls
        Ephi, E1, Zphi, Z1 = projections(L, hfix)
        @printf("  %2d  %+.6f  %+.6f  %+.6e%+.1e im  %+.6e  R=%.6f\n",
                L, Ephi, E1, real(Zphi), imag(Zphi), real(Z1), real(Z1/Zphi))
    end
else
    Lmin = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 8
    Lmax = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 16
    main(Lmin, Lmax)
end
