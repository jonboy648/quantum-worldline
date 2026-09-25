# =====================================================================================
# qw_ope_cttt.jl -- C_TTT (stress-tensor OPE self-coupling) via spin-resolved extraction
# =====================================================================================
# DESIGN: research/tools/merakit-setup/CTTT-SPIN-RESOLUTION-DESIGN.md (Route A).
# Target (PEV unit-normalized): C_TTT = 2*sqrt(2)/sqrt(c). Ising c=1/2 -> 4.000 (the
# VALIDATION GATE); tricritical c=7/10 -> 3.381 (the novel number); Potts c=4/5 -> 3.162.
#
# ROUTE A: the Delta~2 even one-site subspace is span{T, Tbar} (exactly 2-dim for Ising).
# Resolve the spin basis with two PHYSICAL reference operators ascended to the SI layer:
#   energy density h  (reflection-even, continuum spin-0  -> T + Tbar)
#   momentum density p = i[h_{r-1,r}, h_{r,r+1}]  (reflection-odd, -> T - Tbar)
# Then T = (O+_hat + O-_hat)/sqrt(2) after PEV Eq. 10 unit normalization, and
# C_TTT = ope_from_rho3(T,T,T, 2,2,2) -- kinematic exponents use EXACT h=2 (all-holomorphic,
# see design Sec 1.4; feeding the h mixture directly would be kinematically WRONG).
#
# GATES (design Sec 4), checked in order:
#   G3  natural (pre-orthogonalization) overlap |<O+_hat O-_hat>| < 0.05  (chiral split real)
#   G4  |C_{T Tbar 1}| ~ 0  (3-pt structural probe; NOT automatic after Gram-Schmidt)
#   PIN C_sse = 0.5 in the SAME run (normalization convention, catches R4)
#   G5  C_TTT within +-10% of 4.000 STABLE across >=3 clean basins (chi>=8; chi=6 = smoke)
#   PAR C_TbTbTb = C_TTT (reflection self-check)
#
# Run (RUN-MERAKIT.md env): julia +1.8 --project=. qw_ope_cttt.jl [K0] [K1] [NSEED] [MAXITER]
#   defaults: 3 3 4 2500 (chi=6 smoke). Real attempt: 4 4 4 3000 (chi=8).
# =====================================================================================

# pulls in: optimize_ising_mera_z2, sector_dims, densify_mera, diag_parity,
# onesite_scaling_operators, verify_covariance, parity_of, project_parity,
# fixedpoint_rho2, rho1_from_rho2, build_rho3_mirror, twopoint, onept, gram_schmidt,
# build_rho3_cone + ope_from_rho3 (via ope_cone_v2.jl), and MERAKit/TensorKit/DemoTools.
include(joinpath(@__DIR__, "qw_ope_pev_z2.jl"))

# ===== physical reference operators (graded build -> block -> densify) ===============

# densify a graded 2-site operator exactly like densify_layer does for tensors:
# convert(Array) lays each leg out in sector order, matching the densified MERA basis.
function densify_op2(op)
    d = dim(space(op, 1))
    arr = convert(Array, op)
    V = ComplexSpace(d)
    return TensorMap(ComplexF64.(reshape(arr, d * d, d * d)), V ⊗ V, V ⊗ V)
end

# blocked energy density in the densified basis -- the SAME h the optimizer used.
function build_h_dense()
    h = DemoTools.ising_hamiltonian(; symmetry = :Z2, block_size = 2)
    return densify_op2(h)
end

# momentum density p_r = i[h_{r-1,r}, h_{r,r+1}]: 3-spin operator on the UNBLOCKED
# graded chain, embedded in a 4-spin window both ways, blocked with the exact block_op
# fusion convention, then densified. Reflection-ODD by construction (energy current).
function build_p_dense()
    h1 = DemoTools.ising_hamiltonian(; symmetry = :Z2, block_size = 1)
    V = space(h1, 1)
    e = id(V)
    h1c = h1 * (1.0 + 0.0im)
    A = h1c ⊗ e            # h on spins (1,2) of a 3-spin window
    B = e ⊗ h1c            # h on spins (2,3)
    p3 = 1.0im * (A * B - B * A)
    # embed into 4 spins (two placements, translation-average), then fuse pairs
    e4 = id(V)
    p4 = 0.5 * (p3 ⊗ e4 + e4 ⊗ p3)
    fusionspace = V ⊗ V
    ft = isomorphism(fuse(fusionspace), fusionspace)
    fb = isomorphism(fusionspace, fuse(fusionspace))
    pB = (ft ⊗ ft) * p4 * (fb ⊗ fb)
    pd = densify_op2(pB)
    herm = norm(pd - pd') / max(norm(pd), 1e-300)
    return pd, herm
end

# ===== reduction of an ascended width-2 operator to one-site content =================
# rho1-weighted partial trace over ONE side (single-sided on purpose: the symmetric
# average can cancel the reflection-odd p's one-site content). Both sides returned as
# a diagnostic; site-2-traced is the working copy for h AND p consistently.
function onesite_reduce(O2, rho1)
    @tensor O1a[-1; -2] := O2[-1 b; -2 bp] * rho1[bp; b]   # trace site 2 (rho-weighted)
    @tensor O1b[-1; -2] := O2[a -1; ap -2] * rho1[ap; a]   # trace site 1
    return O1a, O1b
end

# ===== spin resolution: project h,p onto the Delta~2 even block, form T/Tbar =========
# Least-squares in the rho2 2-pt metric: solve G c = b, G_ij = <phi_i phi_j>, b_i = <phi_i O1>.
function project_block(O1, block_ops, rho2)
    n = length(block_ops)
    G = Matrix{ComplexF64}(undef, n, n)
    b = Vector{ComplexF64}(undef, n)
    for i in 1:n
        b[i] = twopoint(block_ops[i], O1, rho2)
        for j in 1:n
            G[i, j] = twopoint(block_ops[i], block_ops[j], rho2)
        end
    end
    c = G \ b
    Oproj = sum(c[i] * block_ops[i] for i in 1:n)
    nrmO = sqrt(abs(twopoint(O1, O1, rho2)))
    resid = sqrt(abs(twopoint(O1 - Oproj, O1 - Oproj, rho2))) / max(nrmO, 1e-300)
    return Oproj, c, resid
end

# ===== v3 spin resolution: rho3-CORRELATOR pairing (2026-07-15 redesign) =============
# The v1/v2 width-2 -> one-site REDUCTIONS were the accuracy bottleneck (SIM-065: v1
# single-sided degrades with chi; v2 sym/antisym side-combos FALSIFIED). The fix: never
# reduce. Measure each reference operator's block coefficients through a genuine 3-site
# correlator against the reflection-symmetric rho3avg:
#   left pairing   bL_i = < phi_i(site1) O(sites2,3) >_rho3
#   right pairing  bR_i = < O(sites1,2) phi_i(site3) >_rho3
# Reflection now acts on POSITIONS (site1 <-> site3 with O leg-swap), and the bare
# operators have EXACT leg-swap signatures (h_swap = +h, p_swap = -p, verified below), so
#   O+ coefficients = (bL^h + bR^h)/2   (reflection-even part of h -> T + Tbar)
#   O- coefficients = (bL^p - bR^p)/2   (reflection-odd  part of p -> T - Tbar)
# Within the near-degenerate Delta~2 block all ops share the same dimension, so the fixed
# separations drop out of the RELATIVE coefficients -- exactly what we need, since O+/O-
# get unit-normalized afterwards anyway.
mixed3_left(phi, O, rho3)  = (@tensor t = phi[a; ap] * O[b c; bp cp] * rho3[ap bp cp; a b c]; t)
mixed3_right(O, phi, rho3) = (@tensor t = O[a b; ap bp] * phi[c; cp] * rho3[ap bp cp; a b c]; t)
swap2(O) = (@tensor Os[-1 -2; -3 -4] := O[-2 -1; -4 -3]; Os)

# intra-block spin reversal on the fused (blocked) physical site, densified: spatial
# reflection of the blocked chain = block swap AND reversal WITHIN each block. Plain
# leg-swap alone is NOT reflection (v3 chi=6: h_refl=1.0 flagged exactly this).
function build_R_dense()
    h1 = DemoTools.ising_hamiltonian(; symmetry = :Z2, block_size = 1)
    V = space(h1, 1)
    e = id(V)
    @tensor Sw[-1 -2; -3 -4] := e[-1; -4] * e[-2; -3]     # swap on V (x) V
    fusionspace = V ⊗ V
    ft = isomorphism(fuse(fusionspace), fusionspace)
    fb = isomorphism(fusionspace, fuse(fusionspace))
    Rb = ft * Sw * fb
    d = dim(space(Rb, 1))
    Vc = ComplexSpace(d)
    return TensorMap(ComplexF64.(reshape(convert(Array, Rb), d, d)), Vc, Vc)
end

# full spatial reflection of a blocked 2-site operator
refl2(O, R) = (RR = R ⊗ R; RR * swap2(O) * RR)

# Route A core (v3). Returns O+/O- + diagnostics, or nothing on a structural bail.
function resolve_stress_tensor(md, rho2, rho3avg, U_s, dims_s, ps, phi_eps, Id, P;
                               win_lo = 1.6, win_hi = 2.4)
    hd = build_h_dense()
    Op_dense, herm = build_p_dense()
    # exact FULL-reflection signatures of the bare operators (block swap + intra-block
    # reversal R) -- must be ~0. Plain leg-swap is NOT reflection for blocked operators.
    R = build_R_dense()
    h_refl = norm(refl2(hd, R) - hd) / norm(hd)
    p_refl = norm(refl2(Op_dense, R) + Op_dense) / norm(Op_dense)
    Oh = ascend(hd, md)
    Op = ascend(Op_dense, md)
    exp_p = abs(@tensor Op[a b; ap bp] * rho2[ap bp; a b])
    exp_h = abs(@tensor Oh[a b; ap bp] * rho2[ap bp; a b])
    # the Delta~2 even block (parity-projected with the EXACT P)
    blk = [i for i in 1:length(dims_s)
           if isfinite(ps[i]) && ps[i] > +0.5 && win_lo <= dims_s[i] <= win_hi]
    if length(blk) < 2
        println("  [bail] Delta~2 even block has $(length(blk)) ops (need >=2) in [$win_lo,$win_hi]")
        return nothing
    end
    blk_dims = dims_s[blk]
    # orthonormalize {1, eps, block...} together so the block is orthogonal to the
    # identity and eps towers by construction (kills the leakage-stripping step)
    local chain
    try
        chain = gram_schmidt(vcat([Id, phi_eps], [project_parity(U_s[i], P, +1) for i in blk]), rho2)
    catch err
        println("  [bail] block orthonormalization failed: ", err)
        return nothing
    end
    block_ops = chain[3:end]
    n = length(block_ops)
    # rho3-correlator pairings
    bLh = ComplexF64[mixed3_left(q, Oh, rho3avg) for q in block_ops]
    bRh = ComplexF64[mixed3_right(Oh, q, rho3avg) for q in block_ops]
    bLp = ComplexF64[mixed3_left(q, Op, rho3avg) for q in block_ops]
    bRp = ComplexF64[mixed3_right(Op, q, rho3avg) for q in block_ops]
    # combinations at the correlator level. h's block content IS (T+Tbar) and p's IS
    # (T-Tbar) by the operators' own physics, gauge notwithstanding; the L/R combination
    # only AVERAGES the two independent estimates. The relative L/R sign at the SI level
    # is GAUGE-DEPENDENT (non-covariant tensors), so it is SELF-CALIBRATED per seed:
    # pick the sign that preserves the signal (the wrong sign annihilates it -- v3 chi=6
    # seed 1: |cp| collapsed 3 orders and C_TTT blew up).
    ch = (bLh .+ bRh) ./ 2
    sh = 1.0
    if norm(bLh .- bRh) > norm(bLh .+ bRh)
        sh = -1.0; ch = (bLh .- bRh) ./ 2
    end
    sp = 1.0
    cp = (bLp .+ bRp) ./ 2
    if norm(bLp .- bRp) > norm(bLp .+ bRp)
        sp = -1.0; cp = (bLp .- bRp) ./ 2
    end
    even_frac_h = 2 * norm(ch) / max(norm(bLh) + norm(bRh), 1e-300)   # -> 1 (signal coherence)
    odd_frac_p  = 2 * norm(cp) / max(norm(bLp) + norm(bRp), 1e-300)   # -> 1
    Oplus  = sum(ch[i] * block_ops[i] for i in 1:n)
    Ominus = sum(cp[i] * block_ops[i] for i in 1:n)
    nplus = sqrt(abs(twopoint(Oplus, Oplus, rho2)))
    nminus = sqrt(abs(twopoint(Ominus, Ominus, rho2)))
    if nplus < 1e-10 || nminus < 1e-10
        @printf("  [bail] pairing annihilated a reference op (|O+|=%.2e |O-|=%.2e)\n", nplus, nminus)
        return nothing
    end
    Oplus = Oplus / nplus
    Ominus = Ominus / nminus
    # G3: the NATURAL overlap before enforced orthogonalization -- the real gate
    o_hp = abs(twopoint(Oplus, Ominus, rho2))
    Ominus = Ominus - twopoint(Oplus, Ominus, rho2) * Oplus
    Ominus = Ominus / sqrt(abs(twopoint(Ominus, Ominus, rho2)))
    # theta-scan convention note: see v2 comment history; main scans theta and selects
    # by the C_TTbarI structural zero.
    return (Oplus = Oplus, Ominus = Ominus, o_hp = o_hp,
            even_frac_h = even_frac_h, odd_frac_p = odd_frac_p, sh = sh, sp = sp,
            nh = norm(ch), np = norm(cp), h_refl = h_refl, p_refl = p_refl,
            blk_dims = blk_dims, exp_p = exp_p, exp_h = exp_h, herm = herm)
end

# ===== per-seed C_TTT analysis: v4 front end + Route A + 3-pt table ==================
function analyze_cttt(m_z2, k0::Int, k1::Int)
    d_sig, d_eps, deven, dodd = sector_dims(m_z2; howmany = 16)
    ev_nz = filter(d -> d > 0.02, deven)
    d_T = isempty(ev_nz) ? NaN : ev_nz[argmin(abs.(ev_nz .- 2.0))]
    basin_clean = isfinite(d_sig) && abs(d_sig - 0.125) < 0.10 &&
                  isfinite(d_eps) && abs(d_eps - 1.0) < 0.20 &&
                  isfinite(d_T) && abs(d_T - 2.0) < 0.30

    md = densify_mera(m_z2)
    nt = num_translayers(md)
    lsi = getlayer(md, nt + 1)
    w = lsi.isometry
    u = lsi.disentangler
    P_phys = diag_parity(2, 2)
    P = diag_parity(k0, k1)
    cov = verify_covariance(md, P_phys, P)

    S, U, dims, V, chidim = onesite_scaling_operators(w; howmany = 20)
    order = sortperm(dims)
    dims_s = dims[order]; U_s = U[order]
    ps = [parity_of(o, P) for o in U_s]
    odd_idx  = [i for i in 1:length(dims_s) if isfinite(ps[i]) && ps[i] < -0.5 && dims_s[i] > 0.02]
    even_idx = [i for i in 1:length(dims_s) if isfinite(ps[i]) && ps[i] > +0.5 && dims_s[i] > 0.02]
    @printf("  dense 1-site towers: odd %s | even %s\n",
            string([round(dims_s[i], digits = 3) for i in odd_idx[1:min(3, end)]]),
            string([round(dims_s[i], digits = 3) for i in even_idx[1:min(6, end)]]))
    (isempty(odd_idx) || isempty(even_idx)) && (println("  [bail] missing parity class"); return nothing)
    isig = odd_idx[1]
    ieps = even_idx[argmin(abs.(dims_s[even_idx] .- d_eps))]

    rho2 = fixedpoint_rho2(md)
    rho1 = rho1_from_rho2(rho2)
    Id = id(V)
    sig_p = project_parity(U_s[isig], P, -1)
    eps_p = project_parity(U_s[ieps], P, +1)
    local basis_even
    try
        basis_even = gram_schmidt([Id, eps_p], rho2)
        sig_p = sig_p / sqrt(twopoint(sig_p, sig_p, rho2))
    catch err
        println("  [bail] Gram-Schmidt failed: ", err); return nothing
    end
    phi_eps = basis_even[2]
    phi_sig = sig_p

    rho3A = build_rho3_cone(u, w, rho2)
    rho3A = (rho3A + rho3A') / 2; rho3A = rho3A / real(tr(rho3A))
    rho3B = build_rho3_mirror(u, w, rho2)
    rho3B = (rho3B + rho3B') / 2; rho3B = rho3B / real(tr(rho3B))
    rho3avg = (rho3A + rho3B) / 2

    # Route A spin resolution (v3: rho3-correlator pairing)
    rst = resolve_stress_tensor(md, rho2, rho3avg, U_s, dims_s, ps, phi_eps, Id, P)
    rst === nothing && return nothing

    # kinematic exponents: EXACT h=2 for the all-holomorphic T (design Sec 1.4)
    DT = 2.0
    function cttt_table(T, Tb, rho3)
        C_TTT, _, _ = ope_from_rho3(T, T, T, DT, DT, DT, rho3)
        C_bbb, _, _ = ope_from_rho3(Tb, Tb, Tb, DT, DT, DT, rho3)
        C_TbI, _, _ = ope_from_rho3(T, Tb, Id, DT, DT, 0.0, rho3)
        C_TTe, _, _ = ope_from_rho3(T, T, phi_eps, DT, DT, d_eps, rho3)
        C_sse, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_eps, d_sig, d_sig, d_eps, rho3)
        C_sss, _, _ = ope_from_rho3(phi_sig, phi_sig, phi_sig, d_sig, d_sig, d_sig, rho3)
        return (TTT = C_TTT, bbb = C_bbb, TbI = C_TbI, TTe = C_TTe, sse = C_sse, sss = C_sss)
    end

    # phase scan: the 2-pt metric leaves a U(2) freedom; the 3-pt structure picks theta*
    thetas = (0.0, pi / 2, pi, 3pi / 2)
    tabs = []
    for th in thetas
        z = exp(1.0im * th)
        T  = (rst.Oplus + z * rst.Ominus) / sqrt(2.0)
        Tb = (rst.Oplus - z * rst.Ominus) / sqrt(2.0)
        push!(tabs, (theta = th, c = cttt_table(T, Tb, rho3avg),
                     cA = cttt_table(T, Tb, rho3A), cB = cttt_table(T, Tb, rho3B)))
    end
    # select theta* by the STRUCTURAL zero (min |C_TTbarI|), not by max |C_TTT| --
    # unbiased: the correct chiral combination is the one whose T-Tbar cross 3-pt
    # vanishes; tie-break toward larger |C_TTT| only within a factor 2 of the min
    g4s = [abs(t.c.TbI) for t in tabs]
    g4min = minimum(g4s)
    cand = [i for i in 1:length(tabs) if g4s[i] <= max(2 * g4min, g4min + 1e-6)]
    ibest = cand[argmax([abs(tabs[i].c.TTT) for i in cand])]
    best = tabs[ibest]

    return (d_sig = d_sig, d_eps = d_eps, d_T = d_T, basin_clean = basin_clean, cov = cov,
            rst = rst, tabs = tabs, theta_star = best.theta,
            cA = best.cA, cB = best.cB, c = best.c)
end

# ===== main ==========================================================================
function main_cttt()
    k0    = length(ARGS) >= 1 ? parse(Int, ARGS[1]) : 3
    k1    = length(ARGS) >= 2 ? parse(Int, ARGS[2]) : 3
    nseed = length(ARGS) >= 3 ? parse(Int, ARGS[3]) : 4
    miter = length(ARGS) >= 4 ? parse(Int, ARGS[4]) : 2500
    seed0 = length(ARGS) >= 5 ? parse(Int, ARGS[5]) : 0   # seed offset for parallel pods
    println("="^78)
    println("qw_ope_cttt.jl -- C_TTT spin-resolved extraction (Ising validation)")
    println("Z2Space(0=>$k0, 1=>$k1) [chi=$(k0+k1)]  seeds=$nseed  maxiter=$miter")
    println("TARGET: C_TTT = 2*sqrt(2)/sqrt(c) = 4.000 at c=1/2  (TCI 3.381, Potts 3.162)")
    println("gates: G3 |<O+O->| < 0.05 -> G4 C_TTbarI ~ 0 -> PIN C_sse ~ 0.5 -> G5 C_TTT ~ 4")
    println("="^78)
    t0 = time()

    results = []
    for s in (seed0 + 1):(seed0 + nseed)
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
            a = analyze_cttt(m_z2, k0, k1)
        catch err
            println("  seed $s analyze FAILED: ", sprint(showerror, err)[1:min(end, 300)])
            flush(stdout); continue
        end
        a === nothing && continue
        r = a.rst
        @printf("  sector dims: Dsig=%.4f (.125) Deps=%.4f (1.0) D_T=%.4f (2.0) [%s]\n",
                a.d_sig, a.d_eps, a.d_T, a.basin_clean ? "CLEAN" : "BAD-BASIN")
        @printf("  refs: herm(p)=%.1e <p>=%.2e <h>=%.3f  swap-sig: h_refl=%.1e p_refl=%.1e (both->0)\n",
                r.herm, r.exp_p, r.exp_h, r.h_refl, r.p_refl)
        @printf("  block dims: %s  frac_h=%.3f(s%+.0f) frac_p=%.3f(s%+.0f) (->1) |ch|=%.2e |cp|=%.2e\n",
                string(round.(r.blk_dims, digits = 3)), r.even_frac_h, r.sh, r.odd_frac_p, r.sp, r.nh, r.np)
        @printf("  G3 natural |<O+ O->| = %.4f (<0.05)\n", r.o_hp)
        @printf("  theta scan |C_TTT|: %s -> theta*=%.2f\n",
                string([round(abs(t.c.TTT), digits = 3) for t in a.tabs]), a.theta_star)
        @printf("  C(avg,theta*): TTT=%.4f (4.0) TbTbTb=%.4f (par) | TTbarI=%.4f (0) TTeps=%.4f | sse=%.4f (.5) sss=%.2e\n",
                abs(a.c.TTT), abs(a.c.bbb), abs(a.c.TbI), abs(a.c.TTe), abs(a.c.sse), abs(a.c.sss))
        @printf("  C(regA): TTT=%.4f | C(regB): TTT=%.4f\n", abs(a.cA.TTT), abs(a.cB.TTT))
        flush(stdout)
        push!(results, (seed = s, a = a))
    end

    isempty(results) && (println("\nALL SEEDS FAILED."); return)
    # clean = basin gate AND parity split coherent AND the G4 structural zero holds.
    # G4 = |C_TTbarI| is the per-seed self-flag (chi=6 v3.1: the 4.20 seed had G4=0.001,
    # the 12.2/67.5 junk seeds had G4=0.12/0.15 -- perfect discriminant, like C_sss was
    # for the sigma-eps pipeline).
    isclean(a) = a.basin_clean && a.rst.even_frac_h > 0.8 && a.rst.odd_frac_p > 0.8 &&
                 abs(a.c.TbI) < 0.05
    clean = [r for r in results if isclean(r.a)]
    println("\n" * "="^78)
    println("PER-SEED SUMMARY (clean = basin + fracs>0.8 + G4<0.05):")
    @printf("  %-5s %-8s %-8s %-7s %-7s %-9s %-9s %-9s %-9s %-6s\n",
            "seed", "Dsig", "D_T", "evenH", "oddP", "|C_TTT|", "G3", "|C_TTbI|", "|C_sse|", "clean")
    for r in results
        a = r.a
        @printf("  %-5d %-8.4f %-8.4f %-7.3f %-7.3f %-9.4f %-9.4f %-9.4f %-9.4f %-6s\n",
                r.seed, a.d_sig, a.d_T, a.rst.even_frac_h, a.rst.odd_frac_p, abs(a.c.TTT),
                a.rst.o_hp, abs(a.c.TbI), abs(a.c.sse), isclean(a) ? "yes" : "NO")
    end

    if length(clean) >= 3
        ct = [abs(r.a.c.TTT) for r in clean]
        g3 = maximum(r.a.rst.o_hp for r in clean)
        g4 = maximum(abs(r.a.c.TbI) for r in clean)
        pin = sum(abs(r.a.c.sse) for r in clean) / length(clean)
        mean_t = sum(ct) / length(ct)
        par = maximum(abs(abs(r.a.c.TTT) - abs(r.a.c.bbb)) for r in clean)
        @printf("\nCLEAN n=%d: C_TTT mean=%.4f spread=%.4f | G3max=%.4f G4max=%.4f pin_sse=%.4f par=%.4f\n",
                length(clean), mean_t, maximum(ct) - minimum(ct), g3, g4, pin, par)
        g3ok = g3 < 0.05; g4ok = g4 < 0.10; pinok = abs(pin - 0.5) < 0.07
        g5ok = abs(mean_t - 4.0) < 0.4 && (maximum(ct) - minimum(ct)) < 0.8
        println("\n" * "="^78)
        if g3ok && g4ok && pinok && g5ok
            println("C_TTT GATE: PASS -- Ising graviton self-coupling reproduced. Next: chi up, then TCI 3.381.")
        elseif g3ok && pinok
            println("C_TTT GATE: PARTIAL -- chiral split + normalization OK; number/G4 not converged (expected at chi=6; escalate chi).")
        else
            println("C_TTT GATE: FAIL -- " * (g3ok ? "" : "chiral split broken (G3); ") *
                    (pinok ? "" : "normalization pin broken (R4); ") * "diagnose before escalating.")
        end
        println("="^78)
    else
        println("\nFEWER THAN 3 CLEAN BASINS (n=$(length(clean))) -- add seeds.")
    end
    @printf("wall: %.0f s\n", time() - t0)
    println("QW_OPE_CTTT DONE")
end

main_cttt()
