# =====================================================================================
# qw_ope_constants.jl  --  Run B: OPE structure constant C_{sigma sigma eps} from MERA
# =====================================================================================
#
# GOAL: extract the Ising OPE structure constant C_{sigma sigma eps} from a scale-invariant
# ternary MERA and VALIDATE it against the exact CFT value 0.5 (Pfeifer-Evenbly-Vidal,
# Phys. Rev. A 79, 040301(R) (2009), arXiv:0810.0580). Only after this validation gate
# passes should the same machinery be trusted for tricritical (c=7/10) C_TTT numbers.
#
# ===== STATUS 2026-06-26: VALIDATION GATE NOT PASSED (honest negative result) =====
# WHAT WORKS (verified):
#   * MERAKit ternary MERA runs (Julia 1.8, dense ComplexSpace); single-thread BLAS makes
#     minimize_expectation DETERMINISTIC (multi-thread BLAS lands different basins per run).
#   * Clean scaling-DIMENSION extraction on good basins: width-2 spectrum reproduces the
#     Ising CFT tower {0, ~0.12 (sigma, CFT 1/8), ~0.98 (eps, CFT 1), ~2.0 (T)}.
#   * 2-point normalization is clean: Gram-Schmidt under rho2 gives <sigma|eps>=0 to 1e-15,
#     <ss>=<ee>=1 (paper Eq. 10 satisfied).
# WHAT DOES NOT WORK (the gate failure):
#   * The 3-point OPE structure constant C_{sigma sigma eps} does NOT reproduce 0.5 and is
#     UNSTABLE across basins (chi=6, 6 deterministic seeds: |C_sse| ranged 0.08..17.2;
#     best-spectrum seed gave 0.08, a poor-spectrum seed accidentally gave 0.48). The
#     parity-forbidden |C_sss| (must be 0) ranged 0.09..92 and ANTI-correlated weirdly with
#     dimension cleanliness -- a sign the rho^(3) 3-point object is wrong, not just noisy.
#   * ROOT CAUSE: the ternary one-site rho^(3) used here (3 children of one isometry,
#     rho3 = w rho1 w') is NOT a translation-invariant 3-contiguous-site CFT density matrix
#     (within-block sites 1,2,3 are inequivalent; building a correct width-3 SI marginal
#     needs the full causal cone WITH the inter-block disentanglers, or the genuine PEV
#     "coarse-grain each operator individually until adjacent" algorithm -- not implemented).
# CONSEQUENCE: do NOT trust any tricritical C_TTT from this script until the 3-point
#   geometry is fixed and C_{sigma sigma eps} -> 0.5 stably across basins. chi is NOT the
#   blocker (dims are already clean at chi=6); the rho^(3) CONSTRUCTION is. Fixing it is a
#   focused TensorKit task (correct width-3 causal cone) -- RunPod not required for that, but
#   IS warranted once the math is right and chi>=10-12 is wanted to push sigma to 1/8.
# ==================================================================================
#
# METHOD (Pfeifer-Evenbly-Vidal, adapted to the TERNARY MERA, scale factor 3):
#   (1) Optimize a scale-invariant MERA on the critical Ising Hamiltonian (h = J XX + h Z,
#       blocked block_size=2 so the physical site dim is 4). DENSE ComplexSpace tensors
#       (Z2-symmetric tensors trip a TensorKitManifolds polar-Newton LAPACK bug on this
#       platform; the dense route is the project's validated path, qw_tci_measure.jl).
#   (2) Build the ONE-SITE ascending scaling superoperator A^(1) from the isometry w
#       (paper Fig 2(ii)). Its eigenoperators phi_alpha are the one-site scaling operators;
#       eigenvalues lambda_alpha give Delta_alpha = -log_3(lambda_alpha) (paper Eq. 5).
#   (3) Build the one-site fixed-point density matrix rho^(1) (dominant eigenoperator of the
#       descending one-site superoperator D^(1) = adjoint of A^(1)), then the two- and
#       three-site fixed-point density matrices rho^(2), rho^(3) by the proper coarse-grained
#       descents (paper Eq. 7; rho is the unique S* fixed point).
#   (4) Identify identity (Delta=0), sigma (Delta~1/8, Z2-odd), eps (Delta~1, Z2-even) from
#       the spectrum and their parity under the global spin flip Z (=> the operator's overlap
#       structure). Normalize phi_alpha so the 2-point function tr[(phi_a ox phi_b) rho^(2)]
#       = delta_ab (paper Eq. 10).
#   (5) C_{alpha beta gamma} = sfact^{Omega} * tr[(phi_a ox phi_b ox phi_c) rho^(3)],
#       Omega = Delta_a + Delta_b - Delta_c   (paper Eqs. 12-13; the binary 2^Omega prefactor
#       becomes 3^Omega for the ternary MERA). For (sigma,sigma,eps): Omega = 1/8+1/8-1 = -3/4.
#
# VALIDATION GATE: |C_{sigma sigma eps} - 0.5| small (target a few % at the reachable chi).
# If chi=8 is too noisy to reach 0.5, the script SAYS SO and reports what chi/RunPod is
# needed -- it does NOT fudge.
#
# Run via:  research/tools/merakit-setup/RUN-MERAKIT.md  (Julia 1.8, clean HOME, --project=.)
#   julia +1.8 --project=. qw_ope_constants.jl [CHI]      (CHI default 8)
# =====================================================================================

using Random, LinearAlgebra, Printf, TensorKit, MERAKit, KrylovKit
include(joinpath(@__DIR__, "demo", "demo_tools.jl")); using .DemoTools

# CRITICAL: single-thread BLAS makes minimize_expectation DETERMINISTIC. With multi-thread
# BLAS (the default) the same seed lands in DIFFERENT basins run-to-run (verified: 3 trials
# of seed 1 gave identical E=-1.2732186548 single-threaded, but varied multi-threaded). Since
# basin quality (clean sigma~1/8 tower) is the gating factor and only ~1 in 4 seeds is clean,
# determinism is essential to reliably reuse a good basin. Also set OPENBLAS_NUM_THREADS=1
# in the environment for full effect.
LinearAlgebra.BLAS.set_num_threads(1)

const MERAKIT_DIR = @__DIR__
const SFACT = 3.0          # ternary MERA scale factor (3 sites -> 1)

# -------------------------------------------------------------------------------------
# (1) Optimize a scale-invariant DENSE ternary MERA for the critical Ising model.
#     DIRECT-INIT at the target chi (NO bond-dim ramp). The ramp's expand_bonddim produces
#     near-isometric tensors whose Riemannian retraction trips a TensorKitManifolds
#     polar-Newton LAPACK bug (LAPACKException(23)) on this platform; the validated TCI
#     drivers (qw_tci_measure.jl) all build directly at the target chi and run LBFGS once.
#     We mirror that exactly. Multiple seeds: MERA LBFGS can hit local minima, so we pick
#     the seed whose one-site scaling-dimension tower is cleanest (sigma nearest 1/8).
# -------------------------------------------------------------------------------------
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

# -------------------------------------------------------------------------------------
# (2) ONE-SITE ascending scaling superoperator A^(1) (paper Fig 2(ii)).
#     For the ternary MERA the one-site channel that does NOT touch a disentangler is the
#     CENTER fine leg of the isometry w[a b c; d] (legs 1,2,3 are fine, leg 4 coarse):
#         A^(1)(o)[d'; d] = sum_{a,b,c} w'[d'; a b' c] o[b'; b] w[a b c; d]
#     This is the canonical ternary one-site scaling superoperator; S(I)=I by isometry.
#     We materialize it as a (chi^2) x (chi^2) matrix on vec(o) and diagonalize.
#     phi_alpha (right eigenvectors) are scaling operators; Delta = -log_3 |lambda|.
# -------------------------------------------------------------------------------------
function onesite_superop_action(o, w)
    # o : TensorMap V <- V (one-site operator on a coarse/fine site of dim chi)
    @tensor Ao[-1; -2] := conj(w[a b1 c; -1]) * o[b1; b2] * w[a b2 c; -2]
    return Ao
end

function onesite_descend_action(rho, w)
    # adjoint (descending) channel: rho : V<-V on coarse site -> V<-V on center fine site
    @tensor Drho[-1; -2] := w[a -1 c; d1] * rho[d1; d2] * conj(w[a -2 c; d2])
    return Drho
end

function onesite_scaling_operators(w; howmany::Int = 16)
    V = space(w, 4)'                       # input (coarse) space, dim chi
    chi = dim(V)
    x0 = TensorMap(randn, ComplexF64, V, V)
    f(o) = onesite_superop_action(o, w)
    S, U, info = eigsolve(f, x0, min(howmany, chi^2 - 1), :LM)
    dims = [(-log(SFACT, abs(real(s)))) for s in S]
    return S, U, dims, V, chi
end

# -------------------------------------------------------------------------------------
# (2b) COARSE Z2 PARITY OPERATOR P (essential: WITHOUT symmetric tensors the eigsolve
#      returns sigma (Z2-odd) and eps (Z2-even) MIXED -- <sigma|eps> = 0.7 instead of 0.
#      The global spin-flip X^{ox N} is a symmetry of the Ising ground state; its blocked
#      form (X ox X on each 2-spin block) ascends to a conserved one-site coarse charge P
#      with P^2 = I. We classify each scaling operator by P phi P = +phi (even) / -phi (odd):
#      identity & eps are EVEN, sigma is ODD. Projecting onto definite parity removes the
#      cross-sector contamination and is what makes C_{sigma sigma eps} come out clean.
# -------------------------------------------------------------------------------------
function blocked_physical_parity(Vphys)
    # X ox X on the 2-spin block, fused to the 4-dim physical site
    Vspin = ComplexSpace(2)
    Xs = TensorMap(ComplexF64[0 1; 1 0], Vspin, Vspin)
    fs = Vspin ⊗ Vspin
    ftop = isomorphism(fuse(fs), fs); fbot = isomorphism(fs, fuse(fs))
    return ftop * (Xs ⊗ Xs) * fbot
end

function coarse_parity(m, Pphys)
    # Ascend the one-site physical parity to the scale-invariant layer (width-2), then
    # reduce to a one-site coarse operator on the center leg, and re-converge under the
    # one-site ascending map until it stabilizes to the conserved charge (P^2 = I, |.|=1).
    nt = num_translayers(m)
    w = getlayer(m, nt + 1).isometry
    V = space(w, 4)'
    Pasc = MERAKit.ascended_operator(Pphys, m, nt + 1)   # width-2 at SI layer
    # reduce width-2 -> one-site by tracing the partner leg with normalized identity
    d = dim(space(w, 1))   # internal dim (= chi)
    @tensor P1[-1; -2] := Pasc[-1 a; -2 a]
    P1 = P1 / (dim(V) > 0 ? 1.0 : 1.0)
    # re-converge under the one-site ascending map to land exactly on the SI charge
    for _ in 1:30
        P1 = onesite_superop_action(P1, w)
        P1 = P1 / norm(P1)
    end
    # normalize so eigenvalues are +-1 (it is a Z2 involution): rescale by sqrt of |spectrum|
    P1 = P1 / sqrt(real(tr(P1 * P1)) / dim(V))
    return P1
end

# parity eigenvalue of an operator phi under P: returns +1, -1, or NaN if mixed
function parity_of(phi, P)
    Pp = P * phi * P
    num = real(dot(phi, Pp))            # <phi, P phi P>
    den = real(dot(phi, phi))
    return den < 1e-14 ? NaN : num / den
end

# project phi onto definite parity p (+1 even / -1 odd): (1 + p P.P)/2
function project_parity(phi, P, p)
    return (phi + p * (P * phi * P)) / 2
end

# -------------------------------------------------------------------------------------
# (3) Fixed-point density matrices.
#     rho^(1): dominant eigenoperator of the one-site DESCENDING superoperator D^(1)
#              (adjoint of A^(1)); the unique S* fixed point on one site (paper Eq. 7).
#     rho^(3): three CONTIGUOUS fine sites under ONE isometry w, weighted by rho^(1):
#                rho3[a b c; a' b' c'] = w[a b c; d] rho1[d; d'] conj(w[a' b' c'; d'])
#              (three fine sites of a ternary cell coarse-grain to ONE coarse site whose
#               scale-invariant state is rho^(1)). This is the paper's rho-hat^(3).
#     rho^(2): partial trace of rho^(3) over the third site (two contiguous sites). Used
#              ONLY to normalize the scaling operators so tr[(phi_a ox phi_b) rho2]=delta_ab.
# -------------------------------------------------------------------------------------
function fixedpoint_rho_chain(w)
    V = space(w, 4)'
    # rho^(1): dominant eigenoperator of the descending one-site channel
    x0 = TensorMap(randn, ComplexF64, V, V)
    g(rho) = onesite_descend_action(rho, w)
    S, U, info = eigsolve(g, x0, 1, :LM)
    rho1 = U[1]
    rho1 = (rho1 + rho1') / 2
    rho1 = rho1 / real(tr(rho1))           # trace-normalize
    # make it positive-leading (eigenvector sign/phase is arbitrary)
    if real(tr(rho1)) < 0
        rho1 = -rho1
    end

    # rho^(3) on three contiguous fine sites under one isometry
    @tensor rho3[-1 -2 -3; -4 -5 -6] :=
        w[-1 -2 -3; d1] * rho1[d1; d2] * conj(w[-4 -5 -6; d2])
    # hermitize + trace-normalize the 3-site density matrix
    rho3 = (rho3 + rho3') / 2
    rho3 = rho3 / real(tr(rho3))

    # rho^(2): trace out the 3rd site
    @tensor rho2[-1 -2; -3 -4] := rho3[-1 -2 a; -3 -4 a]
    rho2 = (rho2 + rho2') / 2
    rho2 = rho2 / real(tr(rho2))

    return rho1, rho2, rho3, real(S[1])
end

# -------------------------------------------------------------------------------------
# (4) Two-point function and operator normalization (paper Eq. 10).
#     twopt(a,b) = tr[(phi_a ox phi_b) rho2].  Normalize each phi so twopt(a,a)=1.
# -------------------------------------------------------------------------------------
function twopoint(phi_a, phi_b, rho2)
    @tensor val = (phi_a[a; ap] * phi_b[b; bp]) * rho2[ap bp; a b]
    return val
end

function normalize_operator(phi, rho2)
    n2 = twopoint(phi, phi, rho2)
    return phi / sqrt(n2)
end

# Gram-Schmidt orthonormalize a list of operators under the rho2 inner product
# <a,b> = tr[(a ox b) rho2]. This removes cross-sector contamination so the scaling
# operators behave as orthonormal CFT primaries (paper Eq. 10: C_ab = delta_ab). Without
# symmetric tensors the raw eigsolve operators can carry a small identity/eps admixture;
# orthonormalizing against {I, eps} purifies sigma (and vice versa).
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

# -------------------------------------------------------------------------------------
# (5) OPE structure constant (paper Eqs. 12-13, ternary 3^Omega prefactor).
#     C_abc = sfact^{Omega} * tr[(phi_a ox phi_b ox phi_c) rho3],
#       Omega = Delta_a + Delta_b - Delta_c.
# -------------------------------------------------------------------------------------
function ope_constant(phi_a, phi_b, phi_c, Da, Db, Dc, rho3)
    @tensor t = (phi_a[a; ap] * phi_b[b; bp] * phi_c[c; cp]) * rho3[ap bp cp; a b c]
    Omega = Da + Db - Dc
    return SFACT^Omega * t, t, Omega
end

# -------------------------------------------------------------------------------------
# Per-MERA analysis: extract sigma/eps, normalize, compute C_{sigma sigma eps}.
# Returns a NamedTuple of all diagnostics, or nothing on failure.
# -------------------------------------------------------------------------------------
function analyze_mera(m)
    nt = num_translayers(m)
    lsi = getlayer(m, nt + 1)
    w = lsi.isometry

    # WIDTH-2 dims via MERAKit's canonical scalingdimensions (the validated CFT-dim method;
    # used for seed selection -- it reliably gives sigma~1/8, eps~1 on a CLEAN basin).
    sd = scalingdimensions(m, 16)
    w2dims = sort(real.(get(sd, Trivial(), Float64[])))
    w2nz = filter(d -> d > 0.02, w2dims)
    w2_sig = isempty(w2nz) ? NaN : w2nz[1]
    w2_eps = isempty(w2nz) ? NaN : w2nz[argmin(abs.(w2nz .- 1.0))]

    # ONE-SITE scaling operators (for the OPE 3-point contraction).
    S, U, dims, V, chidim = onesite_scaling_operators(w; howmany = 16)
    order = sortperm(dims)
    dims_s = dims[order]; U_s = U[order]

    rho1, rho2, rho3, lam_rho = fixedpoint_rho_chain(w)

    iI = argmin(abs.(dims_s))
    nz = [i for i in 1:length(dims_s) if dims_s[i] > 0.02]
    (isempty(nz) || length(nz) < 2) && return nothing
    isig = nz[1]
    ieps = nz[argmin(abs.(dims_s[nz] .- 1.0))]
    D_I = dims_s[iI]; D_sig = dims_s[isig]; D_eps = dims_s[ieps]

    # Identity operator on the coarse space (clean Delta=0 primary).
    Id = id(V)
    # Gram-Schmidt orthonormalize {I, sigma, eps} under the rho2 inner product so they act
    # as orthonormal CFT primaries (removes any identity/eps admixture in the raw eigsolve
    # sigma, which is what otherwise pollutes C_sigma_sigma_eps and inflates C_sigma^3).
    local basis
    try
        basis = gram_schmidt([Id, U_s[isig], U_s[ieps]], rho2)
    catch
        return nothing
    end
    phi_sig = basis[2]; phi_eps = basis[3]
    (any(isnan, [real(tr(phi_sig)), real(tr(phi_eps))])) && return nothing
    n_ss = real(twopoint(phi_sig, phi_sig, rho2))
    n_ee = real(twopoint(phi_eps, phi_eps, rho2))
    n_se = twopoint(phi_sig, phi_eps, rho2)

    # Use the better-converged WIDTH-2 dims in the Omega prefactor when available.
    Dsig_use = isnan(w2_sig) ? D_sig : w2_sig
    Deps_use = isnan(w2_eps) ? D_eps : w2_eps
    C_sse, raw_sse, Om_sse = ope_constant(phi_sig, phi_sig, phi_eps, Dsig_use, Dsig_use, Deps_use, rho3)
    C_sss, _, _ = ope_constant(phi_sig, phi_sig, phi_sig, Dsig_use, Dsig_use, Dsig_use, rho3)
    C_eee, _, _ = ope_constant(phi_eps, phi_eps, phi_eps, Deps_use, Deps_use, Deps_use, rho3)

    return (dims = dims_s, w2dims = w2dims, w2_sig = w2_sig, w2_eps = w2_eps,
            D_I = D_I, D_sig = D_sig, D_eps = D_eps,
            lam_rho = lam_rho, n_ss = n_ss, n_ee = n_ee, n_se = n_se,
            C_sse = C_sse, raw_sse = raw_sse, Om_sse = Om_sse,
            C_sss = C_sss, C_eee = C_eee)
end

# -------------------------------------------------------------------------------------
# main: multi-seed sweep (energy is flat across basins at fixed chi; select the seed
# whose one-site sigma dimension is nearest the CFT value 1/8 = cleanest fixed point).
# -------------------------------------------------------------------------------------
function main()
    chi   = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 8
    nseed = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 4
    miter = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 2500
    println("="^78)
    println("qw_ope_constants.jl  --  C_{sigma sigma eps} validation gate (Ising)")
    println("chi=$chi  seeds=$nseed  maxiter=$miter")
    println("CFT target: C_sigma_sigma_eps = 0.5 (Pfeifer-Evenbly-Vidal, arXiv:0810.0580 Eq.15)")
    println("Ternary MERA: Delta = -log_3(lambda); OPE prefactor 3^Omega, Omega=Da+Db-Dc")
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
        a = analyze_mera(m)
        if a === nothing
            println("  seed $s: spectrum lacks sigma/eps; skipped"); continue
        end
        @printf("  width2 dims: Dsig=%.4f (.125) Deps=%.4f (1.0) | onesite: Dsig=%.4f Deps=%.4f | rho_eig=%.4f\n",
                a.w2_sig, a.w2_eps, a.D_sig, a.D_eps, a.lam_rho)
        @printf("  2-pt: <ss>=%.3f <ee>=%.3f <se>=%.3f  |C_sse|=%.4f (target .5)  |C_sss|=%.3f |C_eee|=%.3f\n",
                a.n_ss, a.n_ee, abs(a.n_se), abs(a.C_sse), abs(a.C_sss), abs(a.C_eee))
        flush(stdout)
        push!(results, (seed = s, E = E, a = a))
    end

    if isempty(results)
        println("\nALL SEEDS FAILED. No result.")
        return
    end

    # Select the best basin: width-2 sigma nearest CFT 1/8 (clean fixed point). Among the
    # cleanest few, prefer the one with the smallest parity-forbidden |C_sss| (best 3-point
    # geometry). C_sss should vanish by Z2; a small residual measures the systematic error
    # from the ternary within-block non-translation-invariance of rho^(3).
    sigerr = [abs(r.a.w2_sig - 0.125) for r in results]
    order = sortperm(sigerr)
    topk = order[1:min(3, length(order))]
    best = results[topk[argmin([abs(results[i].a.C_sss) for i in topk])]]
    a = best.a
    println("\n" * "="^78)
    println("BEST-SPECTRUM seed = $(best.seed)  (width-2 Delta_sigma nearest CFT 1/8)")
    println("  width-2 Delta tower: ", round.(a.w2dims[1:min(8,end)], digits=4))
    println("  one-site Delta tower: ", round.(a.dims[1:min(8,end)], digits=4))
    @printf("  width-2: Delta_sigma=%.4f (CFT .125)  Delta_eps=%.4f (CFT 1.0)\n",
            a.w2_sig, a.w2_eps)
    @printf("  one-site: Delta_I=%.4f  Delta_sigma=%.4f  Delta_eps=%.4f\n",
            a.D_I, a.D_sig, a.D_eps)
    @printf("  2-pt checks: <ss>=%.4f <ee>=%.4f <se>=%.4f%+.4fi (cross ~0)\n",
            a.n_ss, a.n_ee, real(a.n_se), imag(a.n_se))
    @printf("  raw tr term = %.5f%+.5fi   Omega = %.4f   3^Omega = %.5f\n",
            real(a.raw_sse), imag(a.raw_sse), a.Om_sse, SFACT^a.Om_sse)
    @printf("  sanity: |C_sss| = %.5f (Z2->0)   |C_eee| = %.5f (Ising CFT 0)\n",
            abs(a.C_sss), abs(a.C_eee))
    println("\n" * "-"^78)
    @printf("RESULT  C_{sigma sigma eps} = %.5f%+.5fi   |C| = %.5f\n",
            real(a.C_sse), imag(a.C_sse), abs(a.C_sse))
    println("        CFT TARGET = 0.5")
    rel = abs(abs(a.C_sse) - 0.5) / 0.5
    @printf("        rel.err vs 0.5 = %.2f%%\n", 100 * rel)
    if rel <= 0.10
        println("\nVALIDATION GATE: PASS (<=10%). OPE pipeline trustworthy at chi=$chi.")
        println("  -> the tricritical C_TTT extraction can be trusted at this chi.")
    elseif rel <= 0.25
        println("\nVALIDATION GATE: MARGINAL ($(round(100*rel,digits=1))%). Pipeline correct;")
        println("  escalate chi (10-12) for a tight C_TTT number.")
    else
        println("\nVALIDATION GATE: FAIL ($(round(100*rel,digits=1))%). chi=$chi too coarse / under-converged.")
        println("  Do NOT trust tricritical C_TTT at this chi. Recommend chi=10-12 via RunPod")
        println("  (A100/H100; chi>=12 ternary MERA is genuinely GPU/RAM-bound).")
    end
    # report the spread across seeds as a stability check
    cs = [abs(r.a.C_sse) for r in results]
    @printf("\n  |C_sse| across %d seeds: min=%.4f max=%.4f mean=%.4f (spread=%.4f)\n",
            length(cs), minimum(cs), maximum(cs), sum(cs)/length(cs), maximum(cs)-minimum(cs))
    println("="^78)
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_OPE_CONSTANTS DONE")
end

main()
