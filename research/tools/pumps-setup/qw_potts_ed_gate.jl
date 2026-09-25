# qw_potts_ed_gate.jl — exact-diagonalization gate for the Potts C_TTT puMPS pipeline
#
#   julia --project=. qw_potts_ed_gate.jl <N>       (N=10 -> 59049-dim, seconds)
#
# Momentum-resolved ED of the 3-state Potts chain in the EXACT puMPS convention:
#   H = sum_j [ -1/2 (U'_j U_{j+1} + U_j U'_{j+1}) - h/2 (V_j + V'_j) ],  h=1 critical.
# Trick (UnitTestED.jl generalized to base 3): eigensolve T.(H - shift*N): |lambda| gives E,
# arg(lambda) gives momentum k. Then Koo-Saleur H_n with the puMPS phase convention
# (on-site phase e^{i n j 2pi/N}, bond phase e^{i n (j+0.5) 2pi/N}) and the raw element
# |<T|H_2|GS>| for direct comparison with the puMPS driver at the same N.
#
# PURPOSE: certify that the d=3 CG plateau (|grad| ~ 2.5e-4) does not bias gaps/elements.

using LinearAlgebra, Printf, KrylovKit

const N  = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 10
const HH = 1.0
const SHIFT = 2.0 * N

om = cis(2pi/3)
U  = diagm(ComplexF64[om^j for j in 0:2])
V  = zeros(ComplexF64, 3, 3); for j in 1:2; V[j, j+1] = 1; end; V[3,1] = 1

# 2-site block, site j = FAST index: kron(B,A) acts A on fast (site j), B on site j+1.
hbond = -0.5*(kron(U, U') + kron(U', U))          # -1/2(U'_j U_{j+1} + U_j U'_{j+1})
hsite = kron(Matrix{ComplexF64}(I,3,3), -(HH/2)*(V + V'))   # field on site j only
h2 = hbond + hsite

const DIM = 3^N
# one-site translation permutation: site labels shift j -> j-1 (site 2 becomes fast).
# index i-1 has base-3 digits (s1..sN), s1 fastest.
perm = Vector{Int}(undef, DIM)
for i in 0:DIM-1
    s1 = i % 3
    perm[i+1] = 1 + (i - s1) ÷ 3 + s1 * 3^(N-1)
end

function apply_H(v::Vector{ComplexF64}; phases::Union{Nothing,Vector{ComplexF64}}=nothing,
                 bphases::Union{Nothing,Vector{ComplexF64}}=nothing)
    # rotating-frame accumulation: at iteration j, fast pair = original sites (j, j+1)
    w  = copy(v)
    Hw = zeros(ComplexF64, DIM)
    for j in 1:N
        wm  = reshape(w, (9, DIM ÷ 9))
        if phases === nothing
            Hw .+= reshape(h2 * wm, DIM)
        else
            Hw .+= phases[j]  .* reshape(hsite * wm, DIM)
            Hw .+= bphases[j] .* reshape(hbond * wm, DIM)
        end
        w  = w[perm]
        Hw = Hw[perm]
    end
    Hw   # after N rotations both are back in the original frame
end

println("="^70)
println("Potts3 ED gate: N=$N  (h=$HH, dim=$DIM)")

f = x -> (apply_H(x) .- SHIFT .* x)[perm]
vals, vecs, info = eigsolve(f, randn(ComplexF64, DIM), 42, :LM;
                            ishermitian=false, krylovdim=110, tol=1e-10, maxiter=400)
println("eigensolve: $(info.converged) converged of $(length(vals)) returned")

ens = SHIFT .- abs.(vals)
ks  = [round(Int, mod(angle(-l)/(2pi/N) + N/2, N) - N/2) for l in vals]
# angle(lambda) = k*2pi/N + pi (since E-SHIFT < 0): angle(-lambda) = k*2pi/N
ord = sortperm(ens)
ens, ks, vecs = ens[ord], ks[ord], vecs[ord]

E0 = ens[1]
@printf("E0 = %.10f  (per site %.10f), k=%d\n", E0, E0/N, ks[1])
println("\nlow spectrum (gap, k):")
for i in 2:min(28, length(ens))
    @printf("  %2d: gap = %.6f   k = %+d\n", i, ens[i]-E0, ks[i])
end

# v calibrations (Delta_sigma = 2/15 from the k=0 sigma pair; Delta_eps = 4/5)
i0 = findall(j -> ks[j]==0, 1:length(ens))
g2, g3, g4 = ens[i0[2]]-E0, ens[i0[3]]-E0, ens[i0[4]]-E0
g_sig = (g2+g3)/2
v_sig = g_sig*N/(2pi*(2/15))
v_eps = g4*N/(2pi*(4/5))
@printf("\nsigma pair split %.2e; ratio eps/sigma = %.4f (exact 6.0); v_sig=%.4f v_eps=%.4f\n",
        abs(g3-g2)/g2, g4/g_sig, v_sig, v_eps)

# KS elements at n = +2 and -2
gs = vecs[1]
theta = 2pi/N
for n in (2, -2)
    ph  = ComplexF64[cis(n*j*theta)       for j in 1:N]
    bph = ComplexF64[cis(n*(j+0.5)*theta) for j in 1:N]
    Hn_gs = apply_H(gs; phases=ph, bphases=bph)
    idx = [j for j in 1:length(ens) if ks[j] == n && ens[j]-E0 < 3.2]
    raw = [abs(dot(vecs[j], Hn_gs)) for j in idx]
    jT  = idx[argmax(raw)]
    ET  = ens[jT] - E0
    v_T = ET*N/(2pi*2.0)
    MT  = maximum(raw)*N/(2pi*v_T)
    c   = 2*MT^2
    @printf("\nn=%+d: elements over k=%d cluster: %s\n", n, n,
            join([@sprintf("%.5f(D=%.3f)", raw[i], (ens[idx[i]]-E0)*N/(2pi*v_eps)) for i in eachindex(idx)], "  "))
    @printf("   T: gap=%.6f  v_T=%.6f  raw|M|=%.6f  KS|M_T|=%.6f  c=%.6f  C_TTT=%.6f\n",
            ET, v_T, maximum(raw), MT, c, 2*sqrt(2)/sqrt(c))
end
println("\nED gate complete. Compare against puMPS driver at the same N.")
