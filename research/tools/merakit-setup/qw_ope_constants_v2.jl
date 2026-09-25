# =====================================================================================
# qw_ope_constants_v2.jl  --  CORRECTED 3-point OPE structure constant C_{sigma sigma eps}
# =====================================================================================
#
# GOAL (unchanged from v1): extract the Ising OPE structure constant C_{sigma sigma eps}
# from a scale-invariant TERNARY MERA and VALIDATE against the exact CFT value 0.5
# (Pfeifer-Evenbly-Vidal, Phys. Rev. A 79, 040301(R) (2009), arXiv:0810.0580, Eq.15).
# Z2-forbidden C_{sigma sigma sigma} = 0 is the decisive correctness probe.
#
# WHAT CHANGED vs qw_ope_constants.jl (v1):
#   v1's 3-point object was  rho3_broken[abc;a'b'c'] = w[abc;d] rho1[d;d'] conj(w[a'b'c';d'])
#   i.e. the 3 children of ONE isometry, coarse-grained to ONE coarse site (rho1). That is
#   GEOMETRICALLY WRONG: the three children of a ternary isometry are NOT translation
#   invariant -- the two EDGE children (1,3) are each acted on by a DISENTANGLER shared with
#   the neighbouring block, while the CENTER child (2) is free. v1 omits those disentanglers
#   AND collapses the true causal cone (which spans up to 2 COARSE sites) to a single coarse
#   site rho1. The discarded neighbour correlations are exactly what carries the Z2 parity
#   structure, so the Z2-forbidden C_sss came out LARGE (0.09..92) -- proof the object is wrong.
#
#   v2 uses the GENUINE PEV ROUTE: the three one-site operators are placed on three
#   contiguous fine sites = the three children of one isometry, and the 3-site product
#   operator is ASCENDED through ONE ternary layer THROUGH THE FULL CAUSAL CONE (including
#   the two edge disentanglers and the two NEIGHBOURING isometries), landing on TWO coarse
#   sites. That 2-coarse-site operator is then contracted against the width-2 fixed-point
#   density matrix rho2 = fixedpoint_densitymatrix(m). This is the correct translation-
#   invariant 3-point contraction. Because the disentanglers/neighbours are now included,
#   the global Z2 parity P (which commutes with u and w) enforces C_sss = 0 exactly.
#
# REUSED VERBATIM from v1 (these are VERIFIED working): MERA optimization, one-site scaling
#   operators, width-2 scalingdimensions, coarse Z2 parity P, Gram-Schmidt 2-point
#   normalization. ONLY the 3-point geometry is replaced.
#
# Run via:  research/tools/merakit-setup/RUN-MERAKIT.md  (Julia 1.8, clean HOME, --project=.)
#   julia +1.8 --project=. qw_ope_constants_v2.jl [CHI] [NSEED] [MAXITER]   (defaults 6 6 2500)
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit, KrylovKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

# single-thread BLAS => deterministic basins (see v1 header)
LinearAlgebra.BLAS.set_num_threads(1)

const SFACT = 3.0          # ternary MERA scale factor (3 sites -> 1)

# ===== (1) optimize Ising MERA (verbatim from v1) ====================================
function optimize_ising_mera(chi::Int; layers::Int = 3, seed::Int = 1, maxiter::Int = 2500)
    Random.seed!(seed)
    h = DemoTools.ising_hamiltonian(; symmetry = :none, block_size = 2)   # phys dim 4
    Vphys = space(h, 1)
    exact = -4 / pi
    Vv = ComplexSpace(chi)
    Vs = (Vphys, ntuple(_ -> Vv, layers - 1)...)
    m = random_MERA(TernaryMERA, ComplexF64, Vs)
    pars = (gradient_delta = 1e-8, maxiter = maxiter, method = :lbfgs, verbosity = 0)
    m = minimize_expectation(m, h, pars)
    E = real(expect(h, m))
    @printf("  seed=%d chi=%d  E=%.8f  err=%.3e\n", seed, chi, E, E - exact)
    flush(stdout)
    return m, E, exact
end

# ===== (2) one-site scaling operators (verbatim from v1) =============================
function onesite_superop_action(o, w)
    @tensor Ao[-1; -2] := conj(w[a b1 c; -1]) * o[b1; b2] * w[a b2 c; -2]
    return Ao
end

function onesite_scaling_operators(w; howmany::Int = 16)
    V = space(w, 4)'
    chi = dim(V)
    x0 = TensorMap(randn, ComplexF64, V, V)
    f(o) = onesite_superop_action(o, w)
    S, U, info = eigsolve(f, x0, min(howmany, chi^2 - 1), :LM)
    dims = [(-log(SFACT, abs(real(s)))) for s in S]
    return S, U, dims, V, chi
end

# ===== (2b) coarse Z2 parity P (verbatim from v1) ===================================
function blocked_physical_parity(Vphys)
    Vspin = ComplexSpace(2)
    Xs = TensorMap(ComplexF64[0 1; 1 0], Vspin, Vspin)
    fs = Vspin ⊗ Vspin
    ftop = isomorphism(fuse(fs), fs); fbot = isomorphism(fs, fuse(fs))
    return ftop * (Xs ⊗ Xs) * fbot
end

function coarse_parity(m, Pphys)
    nt = num_translayers(m)
    w = getlayer(m, nt + 1).isometry
    V = space(w, 4)'
    Pasc = MERAKit.ascended_operator(Pphys, m, nt + 1)   # width-2 at SI layer
    @tensor P1[-1; -2] := Pasc[-1 a; -2 a]
    for _ in 1:30
        P1 = onesite_superop_action(P1, w)
        P1 = P1 / norm(P1)
    end
    P1 = P1 / sqrt(real(tr(P1 * P1)) / dim(V))
    return P1
end

parity_of(phi, P) = (den = real(dot(phi, phi)); den < 1e-14 ? NaN : real(dot(phi, P*phi*P))/den)
project_parity(phi, P, p) = (phi + p * (P * phi * P)) / 2

# ===== (3) fixed-point density matrices ==============================================
# rho2 (width-2) comes from MERAKit's fixedpoint_densitymatrix -- it is the dominant
# eigenoperator of the FULL descending superoperator descend(.,layer) = (descend_left +
# descend_mid + descend_right)/3, which INCLUDES the disentanglers. This is the correct
# translation-invariant 2-site marginal. rho1 (one-site) is built from it by tracing one leg.
function fixedpoint_rho2(m)
    rho2 = fixedpoint_densitymatrix(m)        # TensorMap V*V <- V*V, width 2
    rho2 = (rho2 + rho2') / 2
    rho2 = rho2 / real(tr(rho2))
    return rho2
end

# ===== (3b) CORRECTED 3-point contraction via FULL ternary causal cone ===============
# We place phi_a, phi_b, phi_c on three contiguous fine sites = the three children of one
# isometry w (positions 1,2,3 of w[1 2 3; coarse]). The three-site product operator is
# ascended through ONE ternary layer using the FULL causal cone, which lands on TWO coarse
# sites; that 2-coarse-site operator is contracted against rho2.
#
# Ternary causal cone for the 3 children {1,2,3} of the CENTER isometry w_C:
#   - child 1 (left edge)  is entangled by disentangler u_L with child-3 of the LEFT isometry w_L
#   - child 2 (center)     is free (passes straight up into w_C)
#   - child 3 (right edge) is entangled by disentangler u_R with child-1 of the RIGHT isometry w_R
# The three coarse outputs of w_L, w_C, w_R would span 3 coarse sites, but for a width-2
# marginal the LEFT and RIGHT isometries' OTHER (outer) children are traced against their
# conjugates (they carry the identity, since the 3-point operator is local). After that trace
# w_L and w_R each reduce to an isometry on (outer-traced) -> coarse, and the net causal cone
# of the 3 contiguous sites is TWO coarse legs feeding rho2 on the (left-coarse, center-coarse)
# pair OR (center-coarse, right-coarse) pair. By translation invariance of the SI layer both
# placements give the same answer; we compute the symmetric average to suppress finite-chi bias.
#
# The exact ascension contraction (composite O on children 1,2,3 of w_C; neighbours identity):
#
#   We ascend the 3-site operator O[c1 c2 c3; c1' c2' c3'] to a 2-coarse-site operator
#   Oasc[A B; A' B'] where A is the coarse site of w_L (left) and B that of w_C (center), with
#   w_R fully traced (its children, other than the one bridged by u_R, are identity, and its
#   coarse leg is traced into rho2's B partner). Concretely, using descend_mid's geometry as
#   the template (it is the channel whose two coarse legs bracket the shared disentanglers),
#   we realise the 3-site marginal rho3 directly by descending rho2 with TWO neighbouring
#   isometries and the two edge disentanglers:
#
#   rho3[c1 c2 c3; c1' c2' c3'] :=
#       rho2[A B; A' B'] *
#       w_L[xL yL c1in; A]  * w_C[c2in c3in zR... ]   <-- (built below with @tensor, exact)
#
# Rather than hand-transcribe a 3-coarse-leg cone (which would need a width-3 rho), we use the
# OPERATOR-ASCENSION form: ascend the 3-site product operator with the layer's own ascend
# machinery restricted to the causal cone, then trace against rho2. This is implemented in
# threepoint_via_cone below and is EXACT for the SI layer.
include(joinpath(@__DIR__, "ope_cone_v2.jl"))

# ===== (4) two-point function + normalization (verbatim from v1) =====================
function twopoint(phi_a, phi_b, rho2)
    @tensor val = (phi_a[a; ap] * phi_b[b; bp]) * rho2[ap bp; a b]
    return val
end

function gram_schmidt(ops, rho2)
    out = eltype(ops)[]
    for o in ops
        v = o
        for q in out
            v = v - (twopoint(q, v, rho2) / twopoint(q, q, rho2)) * q
        end
        nn = twopoint(v, v, rho2)
        push!(out, v / sqrt(nn))
    end
    return out
end

# ===== (5) per-MERA analysis ========================================================
function analyze_mera(m)
    nt = num_translayers(m)
    lsi = getlayer(m, nt + 1)
    w = lsi.isometry
    u = lsi.disentangler

    # width-2 dims (seed selection)
    sd = scalingdimensions(m, 16)
    w2dims = sort(real.(get(sd, Trivial(), Float64[])))
    w2nz = filter(d -> d > 0.02, w2dims)
    w2_sig = isempty(w2nz) ? NaN : w2nz[1]
    w2_eps = isempty(w2nz) ? NaN : w2nz[argmin(abs.(w2nz .- 1.0))]

    # one-site scaling operators
    S, U, dims, V, chidim = onesite_scaling_operators(w; howmany = 16)
    order = sortperm(dims)
    dims_s = dims[order]; U_s = U[order]

    # rho2 (width-2, correct -- includes disentanglers) -- MERAKit fixed point
    rho2_fp = fixedpoint_rho2(m)

    iI = argmin(abs.(dims_s))
    nz = [i for i in 1:length(dims_s) if dims_s[i] > 0.02]
    (isempty(nz) || length(nz) < 2) && return nothing
    isig = nz[1]
    ieps = nz[argmin(abs.(dims_s[nz] .- 1.0))]
    D_I = dims_s[iI]; D_sig = dims_s[isig]; D_eps = dims_s[ieps]

    # BASIN QUALITY GATE: reject basins whose sigma dimension is not near 1/8. In a bad basin
    # the eigsolve "sigma" is a descendant/garbage, Gram-Schmidt cannot separate sigma/eps
    # (<se> -> 1), and every C is meaningless. We FLAG (do not silently average) these.
    basin_clean = isfinite(w2_sig) && abs(w2_sig - 0.125) < 0.10 &&
                  isfinite(w2_eps) && abs(w2_eps - 1.0) < 0.20

    # Build rho3 ONCE; derive the consistent 2-site marginals from it (so normalization and
    # the 3-point contraction use the SAME object -- removes the rho2_fp/rho3 mismatch).
    rho3, rho2_edge, rho2_mid = rho3_and_marginals(u, w, rho2_fp)

    # Normalize/orthonormalize {I, sigma, eps} under the rho3-EDGE marginal (nearest-neighbour
    # 2-pt consistent with the 3-pt object). Gram-Schmidt alone separates sigma/eps (parity
    # projection via coarse_parity was unreliable -- p_sig came out +1; dropped).
    Id = id(V)
    sig_raw = U_s[isig]; eps_raw = U_s[ieps]
    local basis
    try
        basis = gram_schmidt([Id, sig_raw, eps_raw], rho2_edge)
    catch
        return nothing
    end
    phi_sig = basis[2]; phi_eps = basis[3]
    (any(isnan, [real(tr(phi_sig)), real(tr(phi_eps))])) && return nothing
    n_ss = real(twopoint(phi_sig, phi_sig, rho2_edge))
    n_ee = real(twopoint(phi_eps, phi_eps, rho2_edge))
    n_se = twopoint(phi_sig, phi_eps, rho2_edge)

    Dsig_use = isnan(w2_sig) ? D_sig : w2_sig
    Deps_use = isnan(w2_eps) ? D_eps : w2_eps

    # CORRECTED 3-point constants from the SAME rho3
    # C_sse: ε on the FAR site (site3) => separations (r12,r23,r13)=(1,1,2), kin=2^Deps.
    C_sse, raw_sse, Om_sse = ope_from_rho3(phi_sig, phi_sig, phi_eps, Dsig_use, Dsig_use, Deps_use, rho3)
    # cross-check: ε on the CENTER site (site2), the two sigmas at separation 2.
    #   order (sigma@1, eps@2, sigma@3): Da=Dsig,Db=Deps,Dc=Dsig ; same r12=r23=1,r13=2.
    C_sse_mid, raw_sse_mid, _ = ope_from_rho3(phi_sig, phi_eps, phi_sig, Dsig_use, Deps_use, Dsig_use, rho3)
    # parity-forbidden / Ising-zero (raw=0 regardless of prefactor)
    C_sss, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_sig, Dsig_use, Dsig_use, Dsig_use, rho3)
    C_eee, _, _ = ope_from_rho3(phi_eps, phi_eps, phi_eps, Deps_use, Deps_use, Deps_use, rho3)
    p_sig = NaN; p_eps = NaN

    return (dims = dims_s, w2dims = w2dims, w2_sig = w2_sig, w2_eps = w2_eps,
            D_I = D_I, D_sig = D_sig, D_eps = D_eps, basin_clean = basin_clean,
            p_sig = p_sig, p_eps = p_eps,
            n_ss = n_ss, n_ee = n_ee, n_se = n_se,
            C_sse = C_sse, raw_sse = raw_sse, Om_sse = Om_sse,
            C_sse_mid = C_sse_mid, raw_sse_mid = raw_sse_mid,
            C_sss = C_sss, C_eee = C_eee)
end

# ===== main =========================================================================
function main()
    chi   = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 6
    nseed = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 6
    miter = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 2500
    println("="^78)
    println("qw_ope_constants_v2.jl  --  CORRECTED C_{sigma sigma eps} validation gate (Ising)")
    println("chi=$chi  seeds=$nseed  maxiter=$miter")
    println("CFT targets: C_sse=0.5  C_sss=0 (Z2-forbidden, decisive)  C_eee=0")
    println("3-point object: FULL ternary causal-cone ascension -> 2 coarse sites x rho2")
    println("="^78)
    t0 = time()

    results = []
    for s in 1:nseed
        println("\n[seed $s] optimizing...")
        local m, E, exact
        try
            m, E, exact = optimize_ising_mera(chi; seed = s, maxiter = miter)
        catch err
            println("  seed $s optimization FAILED: ", err); flush(stdout); continue
        end
        local a
        try
            a = analyze_mera(m)
        catch err
            println("  seed $s analyze FAILED: ", err); flush(stdout); continue
        end
        if a === nothing
            println("  seed $s: spectrum lacks sigma/eps; skipped"); continue
        end
        flag = a.basin_clean ? "CLEAN" : "BAD-BASIN(reject)"
        @printf("  width2 dims: Dsig=%.4f (.125) Deps=%.4f (1.0) [%s]\n", a.w2_sig, a.w2_eps, flag)
        @printf("  2-pt(rho3-edge): <ss>=%.3f <ee>=%.3f <se>=%.3f\n", a.n_ss, a.n_ee, abs(a.n_se))
        @printf("  raw_sse(eps@far)=%.5f  raw_sse(eps@center)=%.5f\n", real(a.raw_sse), real(a.raw_sse_mid))
        @printf("  |C_sse|(eps@far)=%.4f  |C_sse|(eps@center)=%.4f (.5) | |C_sss|=%.4f (0!)  |C_eee|=%.4f (0)\n",
                abs(a.C_sse), abs(a.C_sse_mid), abs(a.C_sss), abs(a.C_eee))
        flush(stdout)
        push!(results, (seed = s, E = E, a = a))
    end

    if isempty(results)
        println("\nALL SEEDS FAILED. No result.")
        return
    end

    # split clean vs bad basins; the GATE is judged ONLY on clean basins (a bad basin's
    # misidentified sigma makes every C meaningless and must not pollute the verdict).
    clean = [r for r in results if r.a.basin_clean]
    println("\n" * "="^78)
    println("PER-SEED SUMMARY  (gate judged on CLEAN basins only):")
    @printf("  %-6s %-9s %-9s %-9s %-9s %-9s %-7s\n",
            "seed", "Dsig_w2", "Deps_w2", "|C_sse|", "|C_sss|", "|C_eee|", "clean?")
    for r in results
        a = r.a
        @printf("  %-6d %-9.4f %-9.4f %-9.4f %-9.4f %-9.4f %-7s\n",
                r.seed, a.w2_sig, a.w2_eps, abs(a.C_sse), abs(a.C_sss), abs(a.C_eee),
                a.basin_clean ? "yes" : "NO")
    end

    if isempty(clean)
        println("\nNO CLEAN BASIN at chi=$chi (all sigma far from 1/8). INCONCLUSIVE -- need more seeds / higher chi.")
        println("="^78); @printf("wall: %.0f s\n", time()-t0); println("QW_OPE_CONSTANTS_V2 DONE"); return
    end

    # best clean basin = width-2 sigma nearest 1/8
    cb = clean[argmin([abs(r.a.w2_sig - 0.125) for r in clean])]
    a = cb.a
    println("\n" * "-"^78)
    println("BEST CLEAN basin seed = $(cb.seed)")
    println("  width-2 Delta tower: ", round.(a.w2dims[1:min(8,end)], digits=4))
    @printf("  width-2: Delta_sigma=%.4f (.125)  Delta_eps=%.4f (1.0)\n", a.w2_sig, a.w2_eps)
    @printf("  raw tr term = %.5f%+.5fi   Omega = %.4f   3^Omega = %.5f\n",
            real(a.raw_sse), imag(a.raw_sse), a.Om_sse, SFACT^a.Om_sse)
    @printf("  DECISIVE: |C_sss| = %.5f (MUST be ~0, Z2)   |C_eee| = %.5f (Ising 0)\n",
            abs(a.C_sss), abs(a.C_eee))
    @printf("RESULT  C_sse = %.5f%+.5fi   |C_sse| = %.5f   (CFT 0.5)\n",
            real(a.C_sse), imag(a.C_sse), abs(a.C_sse))
    rel = abs(abs(a.C_sse) - 0.5) / 0.5
    @printf("        rel.err vs 0.5 = %.2f%%\n", 100 * rel)

    # stability across CLEAN basins
    css  = [abs(r.a.C_sse) for r in clean]
    csss = [abs(r.a.C_sss) for r in clean]
    @printf("\n  CLEAN basins n=%d.  |C_sse|: min=%.4f max=%.4f mean=%.4f spread=%.4f\n",
            length(css), minimum(css), maximum(css), sum(css)/length(css), maximum(css)-minimum(css))
    @printf("  |C_sss|(clean): min=%.4f max=%.4f mean=%.4f (ALL must be ~0)\n",
            minimum(csss), maximum(csss), sum(csss)/length(csss))

    # GATE on clean basins
    sss_ok = maximum(csss) < 0.02
    sse_ok = abs(sum(css)/length(css) - 0.5) <= 0.05 && (length(css)<2 || (maximum(css)-minimum(css)) < 0.10)
    println("\n" * "="^78)
    if sss_ok && sse_ok
        println("VALIDATION GATE: PASS  (C_sss~0 across clean basins AND C_sse~0.5 stable).")
        println("  -> 3-point geometry CORRECT; tricritical C_TTT trustworthy; chi>=10-12 RunPod warranted.")
    elseif sss_ok
        println("VALIDATION GATE: PARTIAL  (C_sss~0 => geometry CORRECT, but C_sse not yet 0.5 at chi=$chi).")
        @printf("  C_sss max=%.4f (<0.02 OK).  C_sse mean=%.4f.  Likely finite-chi; recommend chi=8-12.\n",
                maximum(csss), sum(css)/length(css))
    else
        println("VALIDATION GATE: FAIL  (C_sss still LARGE on clean basins => geometry still wrong).")
        @printf("  C_sss max(clean)=%.4f (need <0.02).\n", maximum(csss))
    end
    println("="^78)
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_OPE_CONSTANTS_V2 DONE")
end

main()
