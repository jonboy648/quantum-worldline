# qw_yanglee_ks.jl — HYP-028 Phase 2: biorthogonal Koo-Saleur c_KS at Yang-Lee
#
#   julia qw_yanglee_ks.jl <Lmin> <Lmax>        (even L; default 10 16)
#
# At the SIM-070 working point h = h_c^inf = 1.5587127 (lambda=4, PT-unbroken at all
# finite L, spectrum REAL): momentum-resolved biorthogonal ED via the translation-
# composed trick, then the PRODUCT-form KS central charge
#   c_KS = 2 * <0_L|H_-2|T_R><T_L|H_+2|0_R> / (<T_L|T_R><0_L|0_R>) * (L/(2 pi v_T))^2
# with |0> = THE CONFORMAL VACUUM |1> = SECOND k=0 state (physical GS is |phi>,
# Delta_phi = -2/5). Left states via eta = parity: |psi_L> = P|psi_R> (real spectrum).
#
# DISCRIMINATION: c = -22/5 = -4.4 (true central charge; requires the indefinite-metric
# sign -- CFT says <T|T> = c/2 < 0, so watch the T biorthogonal norm) vs c_eff = 2/5.
# M(2,5) structure checks: E_1 - E_phi gap = (2/5)*2piv/L; phi level-2 null => k=+-2
# cluster has ONE phi-descendant (2.0 above GS) below T (2.4 above GS).
# Design: HYP028-BIORTHO-KS-DESIGN.md. Phase-1 gate: SIM-2026-070 (PASSED).

using LinearAlgebra, SparseArrays, Printf
using KrylovKit

# mode: "yl" (default) or "ising" = UNITARY CONTROL (critical TFIM, same code path,
# must return c = +1/2; vacuum = the physical GS there, and Z2 gives structural zeros)
const MODE   = length(ARGS) >= 3 ? ARGS[3] : "yl"
const LAMBDA = MODE == "ising" ? 1.0 : 4.0
const HC     = MODE == "ising" ? 0.0 : 1.5587127

# --- sparse H and KS-phased H_n on the 2^L basis (bit b=0 -> sz=+1) ---------------
function build_Hn(L::Int, h::Float64, n::Int)
    # n=0 reproduces H itself. Phases: site j term e^{i n j th}, bond (j,j+1) e^{i n (j+.5) th}
    dim = 2^L
    th  = 2pi/L
    rows = Int[]; cols = Int[]; vals = ComplexF64[]
    diag = zeros(ComplexF64, dim)
    sph = [cis(n*j*th)       for j in 1:L]
    bph = [cis(n*(j+0.5)*th) for j in 1:L]
    for s in 0:dim-1
        acc = ComplexF64(0)
        for j in 1:L
            bj  = (s >> (j-1)) & 1
            bj1 = (s >> (j % L)) & 1
            zz  = (bj == bj1) ? 1.0 : -1.0
            mz  = (bj == 0) ? 1.0 : -1.0
            acc += -zz*bph[j] - im*h*mz*sph[j]
        end
        diag[s+1] = acc
        for j in 1:L
            push!(rows, xor(s, 1 << (j-1)) + 1); push!(cols, s+1); push!(vals, -LAMBDA*sph[j])
        end
    end
    sparse(rows, cols, vals, dim, dim) + spdiagm(0 => diag)
end

parity_perm(L::Int) = [xor(s, 2^L - 1) + 1 for s in 0:2^L-1]
# translation: site labels j -> j-1 (bit 1 becomes bit L)
function transl_perm(L::Int)
    dim = 2^L
    p = Vector{Int}(undef, dim)
    for s in 0:dim-1
        p[s+1] = ((s >> 1) | ((s & 1) << (L-1))) + 1
    end
    p
end

function stage(L::Int)
    println("="^70); @printf("YL KS stage: L=%d  (lambda=%g, h=%g)\n", L, LAMBDA, HC)
    dim = 2^L
    H  = build_Hn(L, HC, 0)
    tp = transl_perm(L); pp = parity_perm(L)
    S  = 2.0*L
    f  = x -> (H*x .- S .* x)[tp]
    vals, vecs, info = eigsolve(f, randn(ComplexF64, dim), 24, :LM;
                                ishermitian=false, krylovdim=90, tol=1e-11, maxiter=400)
    nst = length(vals)
    ens = S .- abs.(vals)
    ks  = [round(Int, mod(angle(-l)/(2pi/L) + L/2, L) - L/2) for l in vals]
    ord = sortperm(ens); ens, ks, vecs = ens[ord], ks[ord], vecs[ord]

    i0  = [i for i in 1:nst if ks[i]==0]
    ip2 = [i for i in 1:nst if ks[i]==2]
    im2 = [i for i in 1:nst if ks[i]==-2]
    Ephi, E1 = ens[i0[1]], ens[i0[2]]
    # YL: physical GS = |phi>, conformal vacuum = SECOND k=0 state; v from Delta split 2/5.
    # Ising control: vacuum = physical GS; v not needed separately (v_T self-calibrates).
    ivac = MODE == "ising" ? i0[1] : i0[2]
    # v reference: YL from the 1-phi split (Delta = 2/5 exact); Ising from the sigma gap (1/8)
    v    = MODE == "ising" ? (E1-Ephi)*L/(2pi*(1/8)) : (E1-Ephi)*L/(2pi*(2/5))
    println("low spectrum (gap above phi-GS, k):")
    for i in 1:min(14,nst); @printf("   %2d: %.6f  k=%+d\n", i, ens[i]-Ephi, ks[i]); end
    @printf("E_phi=%.8f  E_1=%.8f  v(1-phi gap)=%.6f\n", Ephi, E1, v)

    # biorthogonal pairing: left = P*right (real spectrum, eta = P); EP alarm on <L|R> -> 0
    # (for the Hermitian Ising control P-pairing is harmless: it composes with Z2 parity)
    lv = i -> conj.(vecs[i][pp])            # left as a bra vector (conjugated for dot)
    biod = (i, j) -> transpose(lv(i)) * vecs[j]   # <psi_iL|psi_jR>
    n_phi, n_1 = biod(i0[1], i0[1]), biod(ivac, ivac)
    @printf("biorth norms: <GS|GS>=%.4e%+.1eim  <vac|vac>=%.4e%+.1eim\n",
            real(n_phi), imag(n_phi), real(n_1), imag(n_1))

    Hp2 = build_Hn(L, HC, +2); Hm2 = build_Hn(L, HC, -2)
    res = Dict{String,Any}("L"=>L, "v"=>v, "Ephi"=>Ephi, "E1"=>E1)
    for (tag, idxs) in (("n=+2", ip2), ("n=-2", im2))
        isempty(idxs) && (println("$tag: NO k-states found -- raise nev"); continue)
        # product elements against |1> (the conformal vacuum, i0[2]) for every cluster
        # state. The lattice translation direction fixes whether H_{+2} raises or lowers
        # the measured k -- compute BOTH orientations and let momentum conservation pick
        # (the dead orientation is a structural zero ~1e-26).
        prods = ComplexF64[]; norms = ComplexF64[]; orient = String[]
        for i in idxs
            pa = (transpose(lv(ivac)) * (Hm2 * vecs[i])) * (transpose(lv(i)) * (Hp2 * vecs[ivac]))
            pb = (transpose(lv(ivac)) * (Hp2 * vecs[i])) * (transpose(lv(i)) * (Hm2 * vecs[ivac]))
            den = biod(i, i) * n_1
            if abs(pa) >= abs(pb)
                push!(prods, pa/den); push!(orient, "a")
            else
                push!(prods, pb/den); push!(orient, "b")
            end
            push!(norms, biod(i, i))
        end
        println("   orientation per state: ", join(orient, " "))
        # T-ID: Delta-GATE above the VACUUM, then element dominance inside the window.
        # (Raw argmax fails at YL: the phi-descendant at Delta_vac=1.6 has a LARGER
        # cross-module product than T -- non-unitary lattice operators mix modules hard.)
        Dvac = [(ens[i]-ens[ivac])*L/(2pi*v) for i in idxs]
        cand = [j for j in eachindex(idxs) if 1.75 < Dvac[j] < 2.25]
        isempty(cand) && (@warn "no state in the T window (1.75,2.25) above vacuum"; cand = collect(eachindex(idxs)))
        jT = cand[argmax(abs.(prods[cand]))]
        ET = ens[idxs[jT]]
        v_T = (ET-ens[ivac])*L/(2pi*2.0)
        cks = 2 * prods[jT] * (L/(2pi*v_T))^2
        @printf("%s cluster: Delta above vacuum: %s\n", tag,
                join([@sprintf("%.3f", d) for d in Dvac], "  "))
        @printf("   product elements: %s\n",
                join([@sprintf("%.4e%+.1eim", real(p), imag(p)) for p in prods], "  "))
        @printf("   T = cluster state %d: Delta_vac %.4f (expect 2.0); v_T=%.6f (v_ref %.4f)\n",
                jT, Dvac[jT], v_T, v)
        @printf("   <T_L|T_R> = %.4e%+.1eim\n", real(norms[jT]), imag(norms[jT]))
        @printf("   c_KS = %.6f%+.2eim   (YL: -22/5 = -4.4 vs c_eff = 0.4; Ising control: +0.5)\n",
                real(cks), imag(cks))
        res[tag] = Dict("cks"=>cks, "vT"=>v_T, "Tnorm"=>norms[jT], "DT"=>Dvac[jT],
                        "prods"=>prods, "Dvac"=>Dvac)
    end
    open("qw_yanglee_ks_results.jsonl", "a") do io
        println(io, replace(repr(res), "Dict{String, Any}"=>"", "=>"=>":"))
    end
end

Lmin = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 10
Lmax = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 16
for L in Lmin:2:Lmax
    stage(L)
end
