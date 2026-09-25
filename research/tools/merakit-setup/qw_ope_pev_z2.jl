# =====================================================================================
# qw_ope_pev_z2.jl  --  v4: OPE constants from a Z2-SYMMETRIC-tensor MERA (PEV route)
# =====================================================================================
#
# WHY v4 (2026-07-03): the v3 chi=6 gate run (SIM-2026-060) FAILED with a decisive
# discriminant: dense random-init LBFGS MERAs sit in a GENERIC GAUGE where the Z2 symmetry
# on internal legs is a finite-depth circuit, NOT a product of one-site P's. Any one-site
# parity lift/projection is structurally invalid there (lift diagnostics: rank-1 dominance
# ~1.4, overlap 0.05-0.26, SI non-convergent, on ALL 8 seeds). PEV-2009 worked because
# environment-SVD updates preserve covariance; Riemannian LBFGS from dense random init
# does not.
#
# v4 STRATEGY: make covariance exact by construction, then reuse the validated machinery.
#   (1) OPTIMIZE with Z2-symmetric tensors (Z2Space; demo.jl's documented-working route;
#       the old LAPACKException(23) warning was about the expand_bonddim RAMP -- direct
#       init at target chi verified working, qw_ope_z2smoke.jl 2026-07-03: clean Ising
#       towers per sector at 250 iters, sigma=0.131 odd, eps=1.02 even).
#   (2) Read the BASIN GATE from the sector-resolved scaling dimensions of the symmetric
#       MERA (sigma = lowest ODD dim, eps = even dim nearest 1) -- sharper than the dense
#       heuristic, zero misidentification possible.
#   (3) DENSIFY the tensors (convert to plain ComplexSpace; basis = sector order, so the
#       one-site parity is EXACTLY P = diag(+1_k0, -1_k1) on every leg) and run the v3
#       analysis unchanged: one-site eigsolve, PEV Eq. 10 normalization under the width-2
#       fixed point, both width-3 registrations, full C-table.
#   (4) The v3 parity LIFT now serves as a covariance VERIFIER (must reproduce the diag
#       P with dominance >>1); projection uses the EXACT expected P.
#   (5) With covariant tensors, C_sss is a STRUCTURAL zero (P-odd trace) -- it degrades to
#       a plumbing check (~1e-12). The physics gate shifts to: C_sse -> 0.5 (+-10%) STABLE
#       across >=3 clean basins; C_eee -> 0 stays a live dynamical zero-probe.
#
# Run (RUN-MERAKIT.md env):  julia +1.8 --project=. qw_ope_pev_z2.jl [K0] [K1] [NSEED] [MAXITER]
#   defaults: 3 3 8 2500  (chi = K0+K1, Z2Space(0=>K0, 1=>K1)).  Smoke: 3 3 2 250
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit, KrylovKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

LinearAlgebra.BLAS.set_num_threads(1)

const SFACT = 3.0

# reuse: build_rho3_cone (registration A), ope_from_rho3 (kinematics), mirror added below
include(joinpath(@__DIR__, "ope_cone_v2.jl"))

# ===== (1) optimize the Z2-SYMMETRIC Ising MERA (direct-init, no ramp) ===============
function optimize_ising_mera_z2(k0::Int, k1::Int; layers::Int = 3, seed::Int = 1, maxiter::Int = 2500)
    Random.seed!(seed)
    h = DemoTools.ising_hamiltonian(; symmetry = :Z2, block_size = 2)  # phys Z2Space(0=>2,1=>2)
    exact = -4 / pi
    Vv = Z2Space(0 => k0, 1 => k1)
    Vs = (space(h, 1), ntuple(_ -> Vv, layers - 1)...)
    m = random_MERA(TernaryMERA, Float64, Vs)
    pars = (gradient_delta = 1e-8, maxiter = maxiter, method = :lbfgs, verbosity = 0)
    m = minimize_expectation(m, h, pars)
    E = real(expect(h, m))
    @printf("  seed=%d Z2(%d,%d)  E=%.8f  err=%.3e\n", seed, k0, k1, E, E - exact)
    flush(stdout)
    return m, E
end

# sector-resolved dims from the SYMMETRIC MERA: the exact basin gate
function sector_dims(m_z2; howmany::Int = 12)
    sd = scalingdimensions(m_z2, howmany)
    deven = Float64[]; dodd = Float64[]
    for (sec, dims) in sd
        ds = sort(real.(dims))
        if sec == ℤ₂(0)
            deven = ds
        elseif sec == ℤ₂(1)
            dodd = ds
        end
    end
    d_sig = isempty(dodd) ? NaN : dodd[1]
    ev_nz = filter(d -> d > 0.02, deven)
    d_eps = isempty(ev_nz) ? NaN : ev_nz[argmin(abs.(ev_nz .- 1.0))]
    return d_sig, d_eps, deven, dodd
end

# ===== (2) densify: Z2-symmetric MERA -> plain dense ComplexSpace MERA ===============
# convert(Array, t) lays out each index in sector order (charge 0 block first), so the
# one-site Z2 parity on a densified leg of Z2Space(0=>k0,1=>k1) is EXACTLY
# diag(+1_k0, -1_k1). Verified downstream by the covariance lift diagnostic.
function densify_layer(l)
    u, w = l.disentangler, l.isometry
    Vout = ComplexSpace(dim(space(u, 1)))
    Vint = ComplexSpace(dim(space(w, 1)))
    Vin = ComplexSpace(dim(space(w, 4)'))
    ua = convert(Array, u)
    wa = convert(Array, w)
    du1, du2 = dim(space(u, 1)), dim(space(u, 2))
    di1, di2 = dim(space(u, 3)'), dim(space(u, 4)')
    ud = TensorMap(ComplexF64.(reshape(ua, du1 * du2, di1 * di2)), Vout ⊗ Vout, Vint ⊗ Vint)
    dw1, dw2, dw3 = dim(space(w, 1)), dim(space(w, 2)), dim(space(w, 3))
    dw4 = dim(space(w, 4)')
    wd = TensorMap(ComplexF64.(reshape(wa, dw1 * dw2 * dw3, dw4)), Vint ⊗ Vout ⊗ Vint, Vin)
    return TernaryLayer(ud, wd)
end

function densify_mera(m_z2)
    nt = num_translayers(m_z2)
    layers = ntuple(i -> densify_layer(getlayer(m_z2, i)), nt + 1)
    return GenericMERA(layers)
end

# exact one-site parity on a densified leg with sector split (k0, k1)
function diag_parity(k0::Int, k1::Int)
    V = ComplexSpace(k0 + k1)
    P = Matrix{ComplexF64}(Diagonal(vcat(ones(k0), -ones(k1))))
    return TensorMap(P, V, V)
end

# ===== (3) v3 analysis machinery (dense; verbatim where possible) ====================
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

# covariance VERIFIER: lift the exact physical parity through one layer and compare to the
# expected diag parity (v3's lift machinery; on covariant tensors it must factor perfectly)
function purify_involution(A::Matrix{ComplexF64})
    lam = eigvals(A)
    ph2 = sum(l -> l^2, lam) / length(lam)
    th = angle(ph2) / 2
    B = A .* exp(-im * th)
    B = (B + B') / 2
    F = eigen(Hermitian(B))
    P = F.vectors * Diagonal(sign.(F.values)) * F.vectors'
    return P, norm(B - P) / max(norm(B), 1e-300)
end

function factor_rank1_pair(M)
    d1 = dim(space(M, 1)); d2 = dim(space(M, 2))
    arr = reshape(convert(Array, M), d1, d2, d1, d2)
    X = reshape(permutedims(arr, (1, 3, 2, 4)), d1 * d1, d2 * d2)
    F = svd(X)
    A = reshape(F.U[:, 1], d1, d1) .* sqrt(F.S[1])
    B = reshape(conj(F.Vt[1, :]), d2, d2) .* sqrt(F.S[1])
    dominance = F.S[1] / max(F.S[2], 1e-300)
    A, resA = purify_involution(Matrix{ComplexF64}(A))
    B, resB = purify_involution(Matrix{ComplexF64}(B))
    recon = reshape(A, d1, 1, d1, 1) .* reshape(B, 1, d2, 1, d2)
    s = dot(vec(recon), vec(arr)) / dot(vec(recon), vec(recon))
    real(s) < 0 && (B = -B)
    overlap = abs(s) * norm(vec(recon)) / max(norm(vec(arr)), 1e-300)
    return A, B, dominance, overlap, max(resA, resB)
end

tm(A::Matrix{ComplexF64}, V) = TensorMap(A, V, V)

function lift_parity_layer(Pb, layer)
    u, w = layer.disentangler, layer.isometry
    @tensor M[-1 -2; -3 -4] := conj(u[a1 b1; -1 -2]) * Pb[a1; a2] * Pb[b1; b2] * u[a2 b2; -3 -4]
    Pi1m, Pi2m, dom, ov, res = factor_rank1_pair(M)
    Pi1 = tm(Pi1m, space(w, 3))
    Pi2 = tm(Pi2m, space(w, 1))
    @tensor Pa[-1; -2] := conj(w[a1 b1 c1; -1]) * Pi2[a1; a2] * Pb[b1; b2] * Pi1[c1; c2] * w[a2 b2 c2; -2]
    Pam, resP = purify_involution(Matrix{ComplexF64}(convert(Array, Pa)))
    Pa = tm(Pam, space(w, 4)')
    return Pa, (dominance = dom, overlap = ov, inv_res = max(res, resP))
end

# verify covariance: lift phys parity through all layers; report worst-layer diagnostics
# and the sign-fixed distance of the final P from the expected diag parity.
function verify_covariance(md, P_phys, P_expected)
    nt = num_translayers(md)
    Pb = P_phys
    worst_dom = Inf; worst_ov = 1.0
    local diag
    for tau in 1:(nt + 1)
        Pb, diag = lift_parity_layer(Pb, getlayer(md, tau))
        worst_dom = min(worst_dom, diag.dominance)
        worst_ov = min(worst_ov, diag.overlap)
    end
    dplus = norm(Pb - P_expected); dminus = norm(Pb + P_expected)
    dist = min(dplus, dminus) / norm(P_expected)
    return (worst_dom = worst_dom, worst_ov = worst_ov, P_dist = dist)
end

parity_of(phi, P) = (den = real(dot(phi, phi)); den < 1e-14 ? NaN : real(dot(phi, P * phi * P)) / den)
project_parity(phi, P, p) = (phi + p * (P * phi * P)) / 2

# ===== (4) fixed-point rho + registrations + 2-pt (verbatim v3) ======================
function fixedpoint_rho2(m)
    rho2 = fixedpoint_densitymatrix(m)
    rho2 = (rho2 + rho2') / 2
    return rho2 / real(tr(rho2))
end

function rho1_from_rho2(rho2)
    @tensor r1[-1; -2] := rho2[-1 a; -2 a]
    r1 = (r1 + r1') / 2
    return r1 / real(tr(r1))
end

function build_rho3_mirror(u, w, rho2)
    @tensor rho3[-1 -2 -3; -4 -5 -6] :=
        rho2[22 42; 21 41] *
        w[11 12 51; 22] * conj(w[11 12 61; 21]) *
        w[52 -3 32; 42] * conj(w[62 -6 32; 41]) *
        u[-1 -2; 51 52] * conj(u[-4 -5; 61 62])
    return rho3
end

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

# ===== (5) per-seed analysis: symmetric gate -> densify -> dense OPE extraction ======
function analyze(m_z2, k0::Int, k1::Int)
    # exact sector-resolved basin gate (from the SYMMETRIC MERA)
    d_sig, d_eps, deven, dodd = sector_dims(m_z2)
    basin_clean = isfinite(d_sig) && abs(d_sig - 0.125) < 0.10 &&
                  isfinite(d_eps) && abs(d_eps - 1.0) < 0.20

    md = densify_mera(m_z2)
    nt = num_translayers(md)
    lsi = getlayer(md, nt + 1)
    w = lsi.isometry
    u = lsi.disentangler

    # exact parities in the densified basis + covariance verification
    P_phys = diag_parity(2, 2)
    P = diag_parity(k0, k1)
    cov = verify_covariance(md, P_phys, P)

    # one-site scaling operators on the dense SI layer, identified BY PARITY CLASS
    # (the exact P is available -- never identify by dimension alone; that's what
    # misassigned eps to an odd operator in the first v4 smoke)
    S, U, dims, V, chidim = onesite_scaling_operators(w; howmany = 16)
    order = sortperm(dims)
    dims_s = dims[order]; U_s = U[order]
    ps = [parity_of(o, P) for o in U_s]
    odd_idx  = [i for i in 1:length(dims_s) if isfinite(ps[i]) && ps[i] < -0.5 && dims_s[i] > 0.02]
    even_idx = [i for i in 1:length(dims_s) if isfinite(ps[i]) && ps[i] > +0.5 && dims_s[i] > 0.02]
    @printf("  dense 1-site towers: odd %s | even %s\n",
            string([round(dims_s[i], digits = 3) for i in odd_idx[1:min(3, end)]]),
            string([round(dims_s[i], digits = 3) for i in even_idx[1:min(4, end)]]))
    if isempty(odd_idx) || isempty(even_idx)
        println("  [bail] missing a parity class: odd n=$(length(odd_idx)) even n=$(length(even_idx))")
        return nothing
    end
    isig = odd_idx[1]                                          # sigma = lowest odd
    ieps = even_idx[argmin(abs.(dims_s[even_idx] .- d_eps))]   # eps = even nearest sector-eps
    p_sig_raw = ps[isig]
    p_eps_raw = ps[ieps]
    D_sig_dense = dims_s[isig]; D_eps_dense = dims_s[ieps]

    rho2 = fixedpoint_rho2(md)
    rho1 = rho1_from_rho2(rho2)

    # parity-project with the EXACT P, then PEV Eq. 10 normalization
    Id = id(V)
    sig_p = project_parity(U_s[isig], P, -1)
    eps_p = project_parity(U_s[ieps], P, +1)
    keep_sig = norm(sig_p) / max(norm(U_s[isig]), 1e-300)
    keep_eps = norm(eps_p) / max(norm(U_s[ieps]), 1e-300)
    if keep_sig < 1e-6 || keep_eps < 1e-6
        @printf("  [bail] projection killed an operator (keep_sig=%.2e keep_eps=%.2e)\n", keep_sig, keep_eps)
        return nothing
    end
    local basis_even
    try
        basis_even = gram_schmidt([Id, eps_p], rho2)
        sig_p = sig_p / sqrt(twopoint(sig_p, sig_p, rho2))
    catch err
        println("  [bail] Gram-Schmidt failed: ", err)
        return nothing
    end
    phi_eps = basis_even[2]
    phi_sig = sig_p   # exact-parity sigma is orthogonal to the even sector by construction
    n_se = twopoint(phi_sig, phi_eps, rho2)
    one_sig = onept(phi_sig, rho1)
    one_eps = onept(phi_eps, rho1)

    Dsig_use = d_sig   # sector-exact dims in the kinematic exponents
    Deps_use = d_eps

    rho3A = build_rho3_cone(u, w, rho2)
    rho3A = (rho3A + rho3A') / 2; rho3A = rho3A / real(tr(rho3A))
    rho3B = build_rho3_mirror(u, w, rho2)
    rho3B = (rho3B + rho3B') / 2; rho3B = rho3B / real(tr(rho3B))
    ti_err = norm(rho3A - rho3B) / norm(rho3A)
    rho3avg = (rho3A + rho3B) / 2

    function ctable(rho3)
        C_ssI, _, _ = ope_from_rho3(phi_sig, phi_sig, Id, Dsig_use, Dsig_use, 0.0, rho3)
        C_seI, _, _ = ope_from_rho3(phi_sig, phi_eps, Id, Dsig_use, Deps_use, 0.0, rho3)
        C_sse, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_eps, Dsig_use, Dsig_use, Deps_use, rho3)
        C_ses, _, _ = ope_from_rho3(phi_sig, phi_eps, phi_sig, Dsig_use, Deps_use, Dsig_use, rho3)
        C_sss, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_sig, Dsig_use, Dsig_use, Dsig_use, rho3)
        C_eee, _, _ = ope_from_rho3(phi_eps, phi_eps, phi_eps, Deps_use, Deps_use, Deps_use, rho3)
        return (ssI = C_ssI, seI = C_seI, sse = C_sse, ses = C_ses, sss = C_sss, eee = C_eee)
    end
    cA = ctable(rho3A); cB = ctable(rho3B); cAvg = ctable(rho3avg)

    return (d_sig = d_sig, d_eps = d_eps, deven = deven, dodd = dodd, basin_clean = basin_clean,
            cov = cov, p_sig_raw = p_sig_raw, p_eps_raw = p_eps_raw, keep_sig = keep_sig,
            D_sig_dense = D_sig_dense, D_eps_dense = D_eps_dense,
            n_se = n_se, one_sig = one_sig, one_eps = one_eps, ti_err = ti_err,
            cA = cA, cB = cB, c = cAvg)
end

# ===== main =========================================================================
function main()
    k0    = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 3
    k1    = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 3
    nseed = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 8
    miter = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 2500
    println("="^78)
    println("qw_ope_pev_z2.jl (v4) -- Z2-symmetric-tensor OPE gate (Ising)")
    println("Z2Space(0=>$k0, 1=>$k1) [chi=$(k0+k1)]  seeds=$nseed  maxiter=$miter")
    println("physics gate: C_sse -> 0.5 (+-10%) stable over >=3 clean basins; C_eee -> 0")
    println("structural checks: C_sss ~ 0 (covariance), C_ssI ~ 1, C_seI ~ 0")
    println("="^78)
    t0 = time()

    results = []
    for s in 1:nseed
        println("\n[seed $s] optimizing (Z2 direct-init)...")
        local m_z2
        try
            m_z2, _ = optimize_ising_mera_z2(k0, k1; seed = s, maxiter = miter)
        catch err
            println("  seed $s optimization FAILED: ", sprint(showerror, err)[1:min(end, 300)])
            flush(stdout); continue
        end
        local a
        try
            a = analyze(m_z2, k0, k1)
        catch err
            println("  seed $s analyze FAILED: ", sprint(showerror, err)[1:min(end, 300)])
            flush(stdout); continue
        end
        a === nothing && continue
        flag = a.basin_clean ? "CLEAN" : "BAD-BASIN"
        @printf("  sector dims: Dsig=%.4f (.125) Deps=%.4f (1.0) [%s]\n", a.d_sig, a.d_eps, flag)
        @printf("    odd tower: %s | even tower: %s\n",
                string(round.(a.dodd[1:min(4, end)], digits = 4)), string(round.(a.deven[1:min(5, end)], digits = 4)))
        @printf("  covariance: worst dom=%.1e worst ov=%.6f  |P_lift-P_exact|=%.2e | p_sig=%+.4f p_eps=%+.4f\n",
                a.cov.worst_dom, a.cov.worst_ov, a.cov.P_dist, a.p_sig_raw, a.p_eps_raw)
        @printf("  dense dims used: Dsig=%.4f Deps=%.4f (sector: %.4f %.4f)\n",
                a.D_sig_dense, a.D_eps_dense, a.d_sig, a.d_eps)
        @printf("  diag: <sig>=%.2e <eps>=%.2e <s|e>=%.2e  TI=%.4f\n",
                abs(a.one_sig), abs(a.one_eps), abs(a.n_se), a.ti_err)
        @printf("  C(avg): ssI=%.4f (1) seI=%.2e (0) | sse=%.4f ses=%.4f (.5) | sss=%.2e (0) eee=%.4f (0)\n",
                abs(a.c.ssI), abs(a.c.seI), abs(a.c.sse), abs(a.c.ses), abs(a.c.sss), abs(a.c.eee))
        @printf("  C(regA): sse=%.4f | C(regB): sse=%.4f\n", abs(a.cA.sse), abs(a.cB.sse))
        flush(stdout)
        push!(results, (seed = s, a = a))
    end

    isempty(results) && (println("\nALL SEEDS FAILED."); return)
    clean = [r for r in results if r.a.basin_clean]

    println("\n" * "="^78)
    println("PER-SEED SUMMARY (physics gate on CLEAN basins only):")
    @printf("  %-5s %-8s %-8s %-9s %-9s %-9s %-9s %-6s\n",
            "seed", "Dsig", "Deps", "|C_sse|", "|C_sss|", "|C_eee|", "cov_ov", "clean")
    for r in results
        a = r.a
        @printf("  %-5d %-8.4f %-8.4f %-9.4f %-9.2e %-9.4f %-9.4f %-6s\n",
                r.seed, a.d_sig, a.d_eps, abs(a.c.sse), abs(a.c.sss), abs(a.c.eee),
                a.cov.worst_ov, a.basin_clean ? "yes" : "NO")
    end

    if length(clean) < 3
        println("\nFEWER THAN 3 CLEAN BASINS (n=$(length(clean))) -- INCONCLUSIVE; add seeds.")
        println("="^78); @printf("wall: %.0f s\n", time() - t0); println("QW_OPE_PEV_Z2 DONE"); return
    end

    css  = [abs(r.a.c.sse) for r in clean]
    csss = [abs(r.a.c.sss) for r in clean]
    ceee = [abs(r.a.c.eee) for r in clean]
    mean_sse = sum(css) / length(css)
    @printf("\nCLEAN basins n=%d.  |C_sse|: min=%.4f max=%.4f mean=%.4f spread=%.4f\n",
            length(clean), minimum(css), maximum(css), mean_sse, maximum(css) - minimum(css))
    @printf("|C_sss| max=%.2e (structural ~0)   |C_eee| max=%.4f (dynamical 0)\n",
            maximum(csss), maximum(ceee))

    struct_ok = maximum(csss) < 0.02
    sse_ok = abs(mean_sse - 0.5) <= 0.05 && (maximum(css) - minimum(css)) < 0.10
    println("\n" * "="^78)
    if struct_ok && sse_ok
        println("VALIDATION GATE: PASS (C_sse~0.5 STABLE across >=3 clean basins; covariance clean).")
        println("  -> OPE pipeline TRUSTWORTHY. Next: chi=10-12 RunPod tight C_sse, then tricritical C_TTT.")
    elseif struct_ok
        println("VALIDATION GATE: PARTIAL (covariance clean, C_sss structural-zero OK; C_sse not yet 0.5-stable).")
        println("  -> likely finite-chi or sector-split; try (4,2)/(2,4) split or higher chi before RunPod.")
    else
        println("VALIDATION GATE: FAIL (C_sss NOT a structural zero => densify/covariance plumbing broken).")
    end
    println("="^78)
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_OPE_PEV_Z2 DONE")
end

# guard so qw_ope_cttt.jl can include this file for its machinery without running the gate
if abspath(PROGRAM_FILE) == @__FILE__
    main()
end
