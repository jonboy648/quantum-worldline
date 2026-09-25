# =====================================================================================
# qw_ope_pev.jl  --  v3: OPE structure constants via the PEV route, PARITY-FIXED
# =====================================================================================
#
# GOAL (unchanged): extract Ising C_{sigma sigma eps} from a scale-invariant ternary MERA
# and pass the validation gate (C_sse -> 0.5 AND Z2-forbidden C_sss -> 0, stable across
# >=3 CLEAN basins at chi=6) before trusting tricritical C_TTT.
#
# WHAT CHANGED vs v2 (qw_ope_constants_v2.jl, SIM-058 STILL_BROKEN) -- 2026-07-02:
#   Re-read of the actual PEV paper (arXiv:0810.0580, on disk) + index-level audit of v2
#   against MERAKit's own ascend/descend conventions concluded:
#   (1) v2's rho3 GEOMETRY IS CORRECT. PEV Eq. 13 is literally "trace on three consecutive
#       sites against rho^(3) obtained from rho-hat, times 2^Omega kinematics". Their Fig
#       2(iii) landing sites (x, x+3^q, x+2*3^q -> 0,1,2 after q layers) have registration
#       (center-child, u-out1, u-out2) = exactly build_rho3_cone. The 2^{Delta_eps}
#       kinematic prefactor (v2's r13=2 fix) is PEV's own 2^Omega. Geometry NOT the bug.
#   (2) THE REAL BUG was operator contamination: v1/v2's coarse_parity PARTIAL-TRACES the
#       ascended width-2 parity -- but parity is TRACELESS, so the partial trace annihilates
#       it to noise, and the "re-converge" loop amplifies that noise into the identity
#       (hence "p_sig came out +1" and parity projection was dropped). Without parity
#       projection, a basin whose emergent fixed point slightly breaks Z2 (e.g. a weakly
#       magnetized direction) gives eigsolve operators with parity-even admixture in sigma;
#       C_sss then leaks ~ admixture * C_sse. Evidence: v2's best basin gave C_sse=0.485,
#       C_sss=0.008 (nearly perfect!) while other clean-dim basins leaked 0.084/1.92 --
#       basin-dependent contamination, not a systematically wrong 3-point object.
#   FIXES in v3:
#   (a) PROPER coarse parity by LIFTING the physical parity through every layer:
#       P_int (x) P_int' = u' (P_fine (x) P_fine) u   [rank-1 SVD factorization],
#       P_above = w' (P_i2 (x) P_fine (x) P_i1) w,     iterated to the SI layer.
#       No partial trace anywhere. Covariance residuals reported as diagnostics.
#   (b) Parity-PROJECT sigma (odd) and eps (even) before Gram-Schmidt.
#   (c) Normalization per PEV Eq. 10 under the width-2 fixed point rho-hat (primary),
#       with C_ssI -> 1 and C_seI -> 0 as free marginal-consistency diagnostics.
#   (d) BOTH width-3 registrations (center,u1,u2) and (u1,u2,center) computed; their
#       difference is a translation-invariance error bar; gate judged on the average.
#   DELIBERATE DEVIATION from OPE-PEV-ROUTE-DESIGN.md: no ChargedTernaryOperator
#   ascend-to-adjacency machinery. Reading the paper showed Eq. 13 IS the consecutive-site
#   trace; the design doc's structural fix (parity preserved by ascending) is delivered
#   directly by (a)+(b). Validation gate UNCHANGED.
#
# Run (RUN-MERAKIT.md env):  julia +1.8 --project=. qw_ope_pev.jl [CHI] [NSEED] [MAXITER]
#   defaults: 6 8 2500.  Smoke: julia +1.8 --project=. qw_ope_pev.jl 4 2 300
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit, KrylovKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

# single-thread BLAS => deterministic basins (verified project-wide; see v1 header)
LinearAlgebra.BLAS.set_num_threads(1)

const SFACT = 3.0          # ternary MERA scale factor

# reuse: build_rho3_cone (registration A), ope_from_rho3 (kinematic factor), marginals
include(joinpath(@__DIR__, "ope_cone_v2.jl"))

# ===== (1) optimize Ising MERA (verbatim from v1/v2) =================================
function optimize_ising_mera(chi::Int; layers::Int = 3, seed::Int = 1, maxiter::Int = 2500)
    Random.seed!(seed)
    h = DemoTools.ising_hamiltonian(; symmetry = :none, block_size = 2)   # phys dim 4
    exact = -4 / pi
    Vv = ComplexSpace(chi)
    Vs = (space(h, 1), ntuple(_ -> Vv, layers - 1)...)
    m = random_MERA(TernaryMERA, ComplexF64, Vs)
    pars = (gradient_delta = 1e-8, maxiter = maxiter, method = :lbfgs, verbosity = 0)
    m = minimize_expectation(m, h, pars)
    E = real(expect(h, m))
    @printf("  seed=%d chi=%d  E=%.8f  err=%.3e\n", seed, chi, E, E - exact)
    flush(stdout)
    return m, E, exact
end

# ===== (2) one-site scaling operators (verbatim from v1/v2) ==========================
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

# ===== (2b) physical Z2 parity on the blocked (dim-4) site ===========================
# DemoTools ising_hamiltonian(:none) is H = J*XX + (h/2)*(ZI+IZ) with J=-1: the coupling is
# along X and the field along Z, so the Z2 spin-flip symmetry is Z^{ox N} (Z X Z = -X),
# NOT X^{ox N}. v1/v2 used X ox X here -- lifting a NON-symmetry (second root-cause layer:
# discovered when the v3 lift flowed to the trivial +-I, the only covariant involution left).
# Blocking convention (product then fuse) matches block_op's isomorphism convention.
function blocked_physical_parity()
    Vspin = ComplexSpace(2)
    Zs = TensorMap(ComplexF64[1 0; 0 -1], Vspin, Vspin)
    fs = Vspin ⊗ Vspin
    ftop = isomorphism(fuse(fs), fs); fbot = isomorphism(fs, fuse(fs))
    return ftop * (Zs ⊗ Zs) * fbot
end

# ===== (2c) PARITY LIFTING: physical P -> SI-layer coarse P, layer by layer ==========
# For a Z2-covariant layer there exist one-site parities with
#     u' (P_fine ox P_fine) u  =  P_i1 ox P_i2      (on u's two domain/Vint legs)
#     P_above = w' (P_i2 ox P_fine ox P_i1) w       (w legs: 1<-P_i2, 2<-P_fine, 3<-P_i1;
#                                                    u domain leg 1 pairs w_L leg 3 => P_i1,
#                                                    u domain leg 2 pairs w_R leg 1 => P_i2)
# Dense tensors are only approximately covariant; we extract P_i1, P_i2 by rank-1 SVD
# factorization of the exactly-computed M = u'(P ox P)u and report residuals. NO partial
# traces anywhere (parity is traceless; tracing it annihilates it -- the v1/v2 bug).

# purify a matrix that should be exp(i*theta) * (Hermitian involution): remove the phase,
# Hermitize, round eigenvalues to +-1. Returns (P, residual_before_rounding).
function purify_involution(A::Matrix{ComplexF64})
    lam = eigvals(A)
    ph2 = sum(l -> l^2, lam) / length(lam)      # ~ exp(2i*theta)
    th = angle(ph2) / 2
    B = A .* exp(-im * th)
    B = (B + B') / 2
    F = eigen(Hermitian(B))
    P = F.vectors * Diagonal(sign.(F.values)) * F.vectors'
    return P, norm(B - P) / max(norm(B), 1e-300)
end

# factor M (TensorMap V1xV2 <- V1xV2, M ~ A ox B) into one-site A, B by rank-1 SVD across
# the (leg1)|(leg2) site partition. Returns (A, B, s1/s2 dominance, recon_overlap).
function factor_rank1_pair(M)
    d1 = dim(space(M, 1)); d2 = dim(space(M, 2))
    arr = reshape(convert(Array, M), d1, d2, d1, d2)      # [o1 o2 i1 i2]
    X = reshape(permutedims(arr, (1, 3, 2, 4)), d1 * d1, d2 * d2)
    F = svd(X)
    A = reshape(F.U[:, 1], d1, d1) .* sqrt(F.S[1])
    B = reshape(conj(F.Vt[1, :]), d2, d2) .* sqrt(F.S[1])
    dominance = F.S[1] / max(F.S[2], 1e-300)
    # purify to involutions, then fix the RELATIVE sign so A ox B ~ +M
    A, resA = purify_involution(Matrix{ComplexF64}(A))
    B, resB = purify_involution(Matrix{ComplexF64}(B))
    recon = reshape(A, d1, 1, d1, 1) .* reshape(B, 1, d2, 1, d2)
    s = dot(vec(recon), vec(arr)) / dot(vec(recon), vec(recon))
    real(s) < 0 && (B = -B)
    overlap = abs(s) * norm(vec(recon)) / max(norm(vec(arr)), 1e-300)
    return A, B, dominance, overlap, max(resA, resB)
end

tm(A::Matrix{ComplexF64}, V) = TensorMap(A, V, V)

# lift the fine-site parity Pb through ONE layer; returns (P_above, diagnostics)
function lift_parity_layer(Pb, layer)
    u, w = layer.disentangler, layer.isometry
    @tensor M[-1 -2; -3 -4] := conj(u[a1 b1; -1 -2]) * Pb[a1; a2] * Pb[b1; b2] * u[a2 b2; -3 -4]
    Pi1m, Pi2m, dom, ov, res = factor_rank1_pair(M)
    # u domain leg 1 pairs w_L leg 3 slot; u domain leg 2 pairs w_R leg 1 slot (ascend_left)
    Pi1 = tm(Pi1m, space(w, 3))
    Pi2 = tm(Pi2m, space(w, 1))
    @tensor Pa[-1; -2] := conj(w[a1 b1 c1; -1]) * Pi2[a1; a2] * Pb[b1; b2] * Pi1[c1; c2] * w[a2 b2 c2; -2]
    Pam, resP = purify_involution(Matrix{ComplexF64}(convert(Array, Pa)))
    Pa = tm(Pam, space(w, 4)')
    return Pa, (dominance = dom, overlap = ov, inv_res = max(res, resP))
end

# full lift: physical parity -> converged SI-layer one-site coarse parity
function coarse_parity_v3(m)
    nt = num_translayers(m)
    Pb = blocked_physical_parity()
    diag = nothing
    for tau in 1:nt
        Pb, diag = lift_parity_layer(Pb, getlayer(m, tau))
    end
    lsi = getlayer(m, nt + 1)
    delta = NaN
    for _ in 1:12
        Pnew, diag = lift_parity_layer(Pb, lsi)
        delta = norm(Pnew - Pb) / max(norm(Pb), 1e-300)
        Pb = Pnew
        delta < 1e-10 && break
    end
    return Pb, (diag..., si_delta = delta)
end

parity_of(phi, P) = (den = real(dot(phi, phi)); den < 1e-14 ? NaN : real(dot(phi, P * phi * P)) / den)
project_parity(phi, P, p) = (phi + p * (P * phi * P)) / 2

# ===== (3) fixed-point density matrices =============================================
function fixedpoint_rho2(m)
    rho2 = fixedpoint_densitymatrix(m)        # width-2, includes disentanglers (correct)
    rho2 = (rho2 + rho2') / 2
    return rho2 / real(tr(rho2))
end

function rho1_from_rho2(rho2)
    @tensor r1[-1; -2] := rho2[-1 a; -2 a]
    r1 = (r1 + r1') / 2
    return r1 / real(tr(r1))
end

# MIRROR registration (u1, u2, centerR): sites 1,2 = disentangler outputs, site 3 = center
# child of the RIGHT isometry. Same coarse pair (A,B) and same rho2; traced legs mirror
# build_rho3_cone. Difference vs registration A = translation-invariance error bar.
function build_rho3_mirror(u, w, rho2)
    @tensor rho3[-1 -2 -3; -4 -5 -6] :=
        rho2[22 42; 21 41] *
        w[11 12 51; 22] * conj(w[11 12 61; 21]) *
        w[52 -3 32; 42] * conj(w[62 -6 32; 41]) *
        u[-1 -2; 51 52] * conj(u[-4 -5; 61 62])
    return rho3
end

# ===== (4) 2-pt normalization per PEV Eq. 10 (under the width-2 fixed point) =========
function twopoint(phi_a, phi_b, rho2)
    @tensor val = (phi_a[a; ap] * phi_b[b; bp]) * rho2[ap bp; a b]
    return val
end

onept(phi, rho1) = (@tensor t = phi[a; ap] * rho1[ap; a]; t)

function gram_schmidt(ops, rho2)
    out = eltype(ops)[]
    for o in ops
        v = o
        for q in out
            v = v - (twopoint(q, v, rho2) / twopoint(q, q, rho2)) * q
        end
        push!(out, v / sqrt(twopoint(v, v, rho2)))
    end
    return out
end

# ===== (5) per-MERA analysis ========================================================
function analyze_mera(m)
    nt = num_translayers(m)
    lsi = getlayer(m, nt + 1)
    w = lsi.isometry
    u = lsi.disentangler

    # width-2 dims (basin selection -- select by spectrum, not energy)
    sd = scalingdimensions(m, 16)
    w2dims = sort(real.(get(sd, Trivial(), Float64[])))
    w2nz = filter(d -> d > 0.02, w2dims)
    w2_sig = isempty(w2nz) ? NaN : w2nz[1]
    w2_eps = isempty(w2nz) ? NaN : w2nz[argmin(abs.(w2nz .- 1.0))]
    basin_clean = isfinite(w2_sig) && abs(w2_sig - 0.125) < 0.10 &&
                  isfinite(w2_eps) && abs(w2_eps - 1.0) < 0.20

    # one-site scaling operators
    S, U, dims, V, chidim = onesite_scaling_operators(w; howmany = 16)
    order = sortperm(dims)
    dims_s = dims[order]; U_s = U[order]
    iI = argmin(abs.(dims_s))
    nz = [i for i in 1:length(dims_s) if dims_s[i] > 0.02]
    if isempty(nz) || length(nz) < 2
        println("  [bail] one-site dims lack sigma/eps candidates: ", round.(dims_s[1:min(8, end)], digits = 3))
        return nothing
    end
    isig = nz[1]
    ieps = nz[argmin(abs.(dims_s[nz] .- 1.0))]
    D_sig = dims_s[isig]; D_eps = dims_s[ieps]

    # coarse parity (v3 lift -- the fix) + RAW parity diagnostics
    P, pdiag = coarse_parity_v3(m)
    p_sig_raw = parity_of(U_s[isig], P)
    p_eps_raw = parity_of(U_s[ieps], P)
    trP = tr(P) / dim(space(P, 1))
    @printf("  [parity] p_sig_raw=%+.3f p_eps_raw=%+.3f tr(P)/chi=%+.3f dom=%.1e ov=%.4f inv=%.1e si_d=%.1e\n",
            p_sig_raw, p_eps_raw, real(trP), pdiag.dominance, pdiag.overlap, pdiag.inv_res, pdiag.si_delta)
    flush(stdout)

    # fixed-point rho2 (PEV rho-hat) and rho1
    rho2 = fixedpoint_rho2(m)
    rho1 = rho1_from_rho2(rho2)

    # parity-PROJECT then orthonormalize under rho2 (PEV Eq. 10)
    Id = id(V)
    sig_p = project_parity(U_s[isig], P, -1)
    eps_p = project_parity(U_s[ieps], P, +1)
    keep_sig = norm(sig_p) / max(norm(U_s[isig]), 1e-300)
    keep_eps = norm(eps_p) / max(norm(U_s[ieps]), 1e-300)
    if keep_sig < 1e-6
        @printf("  [bail] parity projection killed sigma (kept %.2e; P~identity or basin Z2-broken)\n", keep_sig)
        return nothing
    end
    local basis_even
    try
        basis_even = gram_schmidt([Id, eps_p], rho2)
        sig_p = sig_p / sqrt(twopoint(sig_p, sig_p, rho2))
    catch err
        println("  [bail] Gram-Schmidt/normalization failed: ", err)
        return nothing
    end
    phi_eps = basis_even[2]
    phi_sig = sig_p - twopoint(basis_even[1], sig_p, rho2) * basis_even[1] -
              twopoint(phi_eps, sig_p, rho2) * phi_eps          # belt-and-braces GS
    phi_sig = phi_sig / sqrt(twopoint(phi_sig, phi_sig, rho2))
    n_se = twopoint(phi_sig, phi_eps, rho2)
    one_sig = onept(phi_sig, rho1)                               # magnetized-basin detector
    one_eps = onept(phi_eps, rho1)

    Dsig_use = isnan(w2_sig) ? D_sig : w2_sig
    Deps_use = isnan(w2_eps) ? D_eps : w2_eps

    # BOTH registrations of the 3-consecutive-site fixed-point marginal
    rho3A = build_rho3_cone(u, w, rho2)
    rho3A = (rho3A + rho3A') / 2; rho3A = rho3A / real(tr(rho3A))
    rho3B = build_rho3_mirror(u, w, rho2)
    rho3B = (rho3B + rho3B') / 2; rho3B = rho3B / real(tr(rho3B))
    ti_err = norm(rho3A - rho3B) / norm(rho3A)
    rho3avg = (rho3A + rho3B) / 2

    # structure constants (PEV Eq. 13 with full kinematic factor; r12=r23=1, r13=2)
    function ctable(rho3)
        C_ssI, rawI, _ = ope_from_rho3(phi_sig, phi_sig, Id, Dsig_use, Dsig_use, 0.0, rho3)
        C_seI, _, _ = ope_from_rho3(phi_sig, phi_eps, Id, Dsig_use, Deps_use, 0.0, rho3)
        C_sse, raw_sse, _ = ope_from_rho3(phi_sig, phi_sig, phi_eps, Dsig_use, Dsig_use, Deps_use, rho3)
        C_ses, _, _ = ope_from_rho3(phi_sig, phi_eps, phi_sig, Dsig_use, Deps_use, Dsig_use, rho3)
        C_sss, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_sig, Dsig_use, Dsig_use, Dsig_use, rho3)
        C_eee, _, _ = ope_from_rho3(phi_eps, phi_eps, phi_eps, Deps_use, Deps_use, Deps_use, rho3)
        return (ssI = C_ssI, seI = C_seI, sse = C_sse, ses = C_ses, sss = C_sss, eee = C_eee)
    end
    cA = ctable(rho3A); cB = ctable(rho3B); cAvg = ctable(rho3avg)

    return (w2dims = w2dims, w2_sig = w2_sig, w2_eps = w2_eps, basin_clean = basin_clean,
            D_sig = D_sig, D_eps = D_eps,
            P_diag = pdiag, p_sig_raw = p_sig_raw, p_eps_raw = p_eps_raw,
            n_se = n_se, one_sig = one_sig, one_eps = one_eps, ti_err = ti_err,
            cA = cA, cB = cB, c = cAvg)
end

# ===== self-test: lifting the IDENTITY through any layer must return the identity =====
# (u'(I ox I)u = I ox I exactly; SVD factor -> I, I; sandwich -> w'w = I). Catches index/
# duality mistakes in the lift machinery independent of any physics.
function parity_selftest(m)
    l1 = getlayer(m, 1)
    Iphys = id(space(l1.disentangler, 1))
    Pa, d = lift_parity_layer(Iphys, l1)
    errI = norm(Pa - id(space(Pa, 1))) / sqrt(dim(space(Pa, 1)))
    ok = errI < 1e-8 && d.overlap > 1 - 1e-8
    @printf("  [selftest] identity lift: err=%.2e  dominance=%.1e  overlap=%.6f  -> %s\n",
            errI, d.dominance, d.overlap, ok ? "PASS" : "FAIL")
    return ok
end

# ===== main =========================================================================
function main()
    chi   = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 6
    nseed = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 8
    miter = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 2500
    println("="^78)
    println("qw_ope_pev.jl (v3) -- parity-fixed PEV OPE gate (Ising)")
    println("chi=$chi  seeds=$nseed  maxiter=$miter")
    println("CFT targets: C_sse=0.5  C_sss=0 (Z2, decisive)  C_eee=0  C_ssI=1  C_seI=0")
    println("="^78)
    t0 = time()

    results = []
    selftested = false
    for s in 1:nseed
        println("\n[seed $s] optimizing...")
        local m
        try
            m, _, _ = optimize_ising_mera(chi; seed = s, maxiter = miter)
        catch err
            println("  seed $s optimization FAILED: ", err); flush(stdout); continue
        end
        if !selftested
            parity_selftest(m) || (println("SELFTEST FAILED -- aborting."); return)
            selftested = true
        end
        local a
        try
            a = analyze_mera(m)
        catch err
            println("  seed $s analyze FAILED: ", err); flush(stdout); continue
        end
        if a === nothing
            println("  seed $s: no usable sigma/eps (or parity killed sigma); skipped"); continue
        end
        flag = a.basin_clean ? "CLEAN" : "BAD-BASIN"
        @printf("  dims: Dsig=%.4f (.125) Deps=%.4f (1.0) [%s]\n", a.w2_sig, a.w2_eps, flag)
        @printf("  parity: p_sig_raw=%+.3f (want -1) p_eps_raw=%+.3f (want +1) | lift: dom=%.1e ov=%.4f inv=%.1e si_d=%.1e\n",
                a.p_sig_raw, a.p_eps_raw, a.P_diag.dominance, a.P_diag.overlap,
                a.P_diag.inv_res, a.P_diag.si_delta)
        @printf("  diag: <sig>=%.4f <eps>=%.4f <s|e>=%.4f  TI(rho3A-rho3B)=%.3f\n",
                abs(a.one_sig), abs(a.one_eps), abs(a.n_se), a.ti_err)
        @printf("  C(avg): ssI=%.4f (1) seI=%.4f (0) | sse=%.4f ses=%.4f (.5) | sss=%.4f (0!) eee=%.4f (0)\n",
                abs(a.c.ssI), abs(a.c.seI), abs(a.c.sse), abs(a.c.ses), abs(a.c.sss), abs(a.c.eee))
        @printf("  C(regA): sse=%.4f sss=%.4f | C(regB): sse=%.4f sss=%.4f\n",
                abs(a.cA.sse), abs(a.cA.sss), abs(a.cB.sse), abs(a.cB.sss))
        flush(stdout)
        push!(results, (seed = s, a = a))
    end

    isempty(results) && (println("\nALL SEEDS FAILED."); return)
    clean = [r for r in results if r.a.basin_clean]

    println("\n" * "="^78)
    println("PER-SEED SUMMARY (gate judged on CLEAN basins only):")
    @printf("  %-5s %-8s %-8s %-8s %-8s %-8s %-8s %-8s %-6s\n",
            "seed", "Dsig", "Deps", "p_sig", "|C_sse|", "|C_sss|", "|C_ssI|", "<sig>", "clean")
    for r in results
        a = r.a
        @printf("  %-5d %-8.4f %-8.4f %-+8.3f %-8.4f %-8.4f %-8.4f %-8.4f %-6s\n",
                r.seed, a.w2_sig, a.w2_eps, a.p_sig_raw, abs(a.c.sse), abs(a.c.sss),
                abs(a.c.ssI), abs(a.one_sig), a.basin_clean ? "yes" : "NO")
    end

    if length(clean) < 3
        println("\nFEWER THAN 3 CLEAN BASINS (n=$(length(clean))) -- gate INCONCLUSIVE; add seeds.")
        println("="^78); @printf("wall: %.0f s\n", time() - t0); println("QW_OPE_PEV DONE"); return
    end

    css  = [abs(r.a.c.sse) for r in clean]
    csss = [abs(r.a.c.sss) for r in clean]
    mean_sse = sum(css) / length(css)
    @printf("\nCLEAN basins n=%d.  |C_sse|: min=%.4f max=%.4f mean=%.4f spread=%.4f\n",
            length(clean), minimum(css), maximum(css), mean_sse, maximum(css) - minimum(css))
    @printf("|C_sss|: min=%.4f max=%.4f  (ALL must be <0.02)\n", minimum(csss), maximum(csss))

    sss_ok = maximum(csss) < 0.02
    sse_ok = abs(mean_sse - 0.5) <= 0.05 && (maximum(css) - minimum(css)) < 0.10
    println("\n" * "="^78)
    if sss_ok && sse_ok
        println("VALIDATION GATE: PASS (C_sss~0 AND C_sse~0.5 STABLE across >=3 clean basins).")
        println("  -> OPE pipeline TRUSTWORTHY. Next: chi=10-12 RunPod tight number, then tricritical C_TTT.")
    elseif sss_ok
        println("VALIDATION GATE: PARTIAL (geometry+parity correct: C_sss~0 stable; C_sse off 0.5 at chi=$chi).")
        println("  -> likely finite-chi; escalate chi before RunPod C_TTT.")
    else
        println("VALIDATION GATE: FAIL (C_sss still leaks on clean basins).")
        println("  -> parity fix insufficient; inspect p_sig_raw / <sig> / TI columns for the discriminant.")
    end
    println("="^78)
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_OPE_PEV DONE")
end

main()
