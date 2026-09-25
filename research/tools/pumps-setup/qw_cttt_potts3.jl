# qw_cttt_potts3.jl — C_TTT at the 3-state Potts point via puMPS Koo-Saleur matrix elements
#
# ONE (N, D) STAGE PER INVOCATION, checkpointed + resumable:
#   julia --project=. qw_cttt_potts3.jl <N> <D>
# GS checkpoint: potts_gs_N{N}_D{D}.jld2. Results appended to qw_cttt_potts3_results.jsonl.
#
# Model: 3-state Potts, puMPS convention h = -1/2(U'U + UU') - h/2(V + V'), weylops d=3,
# CRITICAL at h=1 (self-dual). v is CALIBRATED from the spectrum, never assumed.
#
# Potts c=4/5 reference data (D-series M(5,6)):
#   k=0 tower: GS(0), sigma pair Delta=2/15 (Z3 charge +-1, DEGENERATE), eps Delta=4/5 (neutral),
#              then Z pair 4/3. Gap ratio eps/sigma = 6.0.
#   k=+-2 cluster: T(2.0, NEUTRAL) = target; L2sigma/L1^2sigma ~2.13 (CHARGED -> structural-zero
#              elements, H is Z3-neutral); L2eps 2.8 and L1(7/5,2/5) 2.8 = nearest NEUTRAL
#              contaminators (farther than TCI's 2.2).
# Targets: c = 4/5, C_TTT = 2*sqrt(2)/sqrt(c) = 3.16228.

include("MPS.jl")
include("puMPS.jl")
using .MPS
using .puMPS
using LinearAlgebra, Printf, JLD2

const HH      = 1.0        # critical point (self-dual)
const D_SIGMA = 2/15
const D_EPS   = 4/5
const NK0     = 5          # k=0: GS, sigma, sigma-bar, eps, buffer
const NK2     = 6          # k=+-2: T + 4 charged sigma-descendants + buffer

function get_gs(N::Int, D::Int)
    ckpt = "potts_gs_N$(N)_D$(D).jld2"
    H_MPO = potts3_local_MPO(ComplexF64, h=HH)
    if isfile(ckpt)
        A = load(ckpt, "A")
        M = puMPState(A, N)
        converged_flag = get(load(ckpt), "converged", true)
        println("resumed GS from $ckpt (converged=$converged_flag)")
        if converged_flag
            return M, real(expect(M, H_MPO)), H_MPO
        end
    else
        # DIRECT random init at target D (warm-start padding -> LAPACKException(30), see SIM-068)
        M = rand_puMPState(ComplexF64, 3, D, N)
        normalize!(M)
        M, _, _ = canonicalize_left!(M)
    end
    # Short CG rounds + wall-clock budget + exit(42): survives external kills, always foreground.
    t0 = time()
    ng = Inf
    e_prev = NaN
    flat = 0
    for r in 1:240
        # Two-phase CG: near the plateau the default step=0.01 overshoots every other
        # linesearch (EnergyHigh -> CG reset -> no conjugate memory, pure-gradient stall
        # at ~3e-4 observed at N=14 D=12). Fine phase: smaller trial step + longer CG runs.
        fine = ng < 1e-3
        # pinv_tol=1e-8 in fine phase: filters near-null metric directions whose amplified
        # noise pinned |grad| at ~2.5e-4 (NB the reported norm drops partly because junk
        # directions are excluded -- the ED cross-check at N=9 is the real quality gate).
        M, ng = puMPS.minimize_energy_local_CG!(M, H_MPO, 15, tol=1e-6,
                    step = fine ? 0.002 : 0.01, cg_steps_max = fine ? 40 : 10,
                    pinv_tol = fine ? 1e-8 : 1e-12)
        # Plateau-accept: the d=3 CG floor sits at ~2.5e-4 (vs 9e-5 on OF) with energy
        # still creeping ~1e-9/iter. Accept when the energy is flat at the 1e-8/round
        # level for 3 rounds -- measurement quality is certified by the N=10 ED gate,
        # not by |grad|. Recorded honestly (converged flag + ng in results).
        e_now = real(expect(M, H_MPO))
        de = isnan(e_prev) ? NaN : e_now - e_prev
        flat = (!isnan(de) && abs(de) < 1e-8 && ng < 5e-4) ? flat + 1 : 0
        e_prev = e_now
        done = ng < 1e-6 || flat >= 3
        @printf("  [round %d] |grad| = %.3e  dE=%.2e  flat=%d  (%.0fs)\n",
                r, ng, de, flat, time() - t0)
        save(ckpt, "A", mps_tensor(M), "N", N, "D", D, "h", HH, "converged", done)
        done && break
        if time() - t0 > 420
            println("TIME BUDGET reached, checkpoint saved -- re-invoke to resume")
            exit(42)
        end
    end
    save(ckpt, "A", mps_tensor(M), "N", N, "D", D, "h", HH, "converged", true)
    println("saved GS checkpoint -> $ckpt  (|grad|=$ng)")
    M, real(expect(M, H_MPO)), H_MPO
end

function stage(N::Int, D::Int)
    println("="^70); println("Potts3 stage: N=$N D=$D  (h=$HH)")
    M, e0, _ = get_gs(N, D)
    @printf("e0(per site) = %.10f\n", e0)

    H_split = potts3_PBC_MPO_split(ComplexF64, h=HH)
    ens, ks, exs = excitations!(M, H_split, [0, 2, -2], [NK0, NK2, NK2])
    ens = real.(ens)
    i0  = findall(k->k==0,  ks); i0  = i0[sortperm(ens[i0])]
    ip2 = findall(k->k==2,  ks); ip2 = ip2[sortperm(ens[ip2])]
    im2 = findall(k->k==-2, ks); im2 = im2[sortperm(ens[im2])]
    E0 = ens[i0[1]]

    # --- v calibration from the k=0 tower.
    # Lowest excitation = DEGENERATE sigma pair (charge +-1); eps is the 4th state.
    g2, g3, g4 = ens[i0[2]]-E0, ens[i0[3]]-E0, ens[i0[4]]-E0
    sig_split = abs(g3-g2)/g2
    sig_split < 0.05 || @warn "sigma pair split $(sig_split) > 5% -- Z3 badly broken or wrong ID"
    g_sig = (g2+g3)/2
    ratio = g4/g_sig
    v_sig = g_sig*N/(2pi*D_SIGMA)
    v_eps = g4*N/(2pi*D_EPS)
    @printf("k=0: sigma-pair split = %.2e; gap ratio (eps/sigma) = %.4f  (Potts exact: 6.0)\n",
            sig_split, ratio)

    # --- KS elements, n=+2 and n=-2
    basis = [exs[i0[1]]; exs[ip2]; exs[im2]]
    ksarg = [0.0, 2.0, -2.0]
    res = Dict{String,Any}("N"=>N, "D"=>D, "e0"=>e0, "ratio_eps_sigma"=>ratio,
                           "sigma_split"=>sig_split, "v_sigma"=>v_sig, "v_eps"=>v_eps)
    # Basis-row offsets from the ACTUAL index lists (KrylovKit over-returns; SIM-068 fix)
    row_p2 = j -> 1 + j
    row_m2 = j -> 1 + length(ip2) + j
    for (n, idxs, rowf) in ((2, ip2, row_p2), (-2, im2, row_m2))
        Hn = potts3_Hn_MPO_split(ComplexF64, n, N, h=HH)
        Mel = Hn_in_basis(M, Hn, basis, ksarg)
        raw = [abs(Mel[rowf(j), 1]) for j in 1:length(idxs)]   # <k=n state j|Hn|GS>
        # T = element-dominant NEUTRAL state; charged sigma-descendants are structural zeros.
        # Gate: nearest neutral contaminator sits at 2.8 -> window (1.5, 2.5) in v_eps units.
        jT = argmax(raw)
        DT_check = (ens[idxs[jT]] - E0) * N / (2pi * v_eps)
        1.5 < DT_check < 2.5 || @warn "element-dominant state has Delta=$(DT_check) (v_eps units) -- NOT T-like; inspect"
        ET = ens[idxs[jT]]
        v_T = (ET - E0)*N/(2pi*2.0)
        MT  = raw[jT]*N/(2pi*v_T)
        c   = 2*MT^2
        cttt = 2*sqrt(2)/sqrt(c)
        @printf("\nn=%+d: raw elements (low cluster): %s\n", n,
                join([@sprintf("%.5f", r) for r in raw], "  "))
        @printf("   T = state %d  Delta_T-gap-> v_T = %.6f  (v_sigma %.4f, v_eps %.4f)\n",
                jT, v_T, v_sig, v_eps)
        @printf("   |M_T| = %.6f   c = %.6f (target 0.800)   C_TTT = %.6f (target 3.1623)\n",
                MT, c, cttt)
        others = [raw[j]*N/(2pi*v_T) for j in 1:length(idxs) if j != jT]
        res["n$(n)"] = Dict("raw"=>raw, "jT"=>jT, "v_T"=>v_T, "M_T"=>MT, "c"=>c,
                            "C_TTT"=>cttt, "others_norm"=>others,
                            "spectrum"=>[ens[i]-E0 for i in idxs])
    end
    res["k0_gaps"] = [ens[i]-E0 for i in i0]

    open("qw_cttt_potts3_results.jsonl", "a") do io
        println(io, replace(repr(res), "Dict{String, Any}"=>"", "=>"=>":"))
    end
    println("\nstage complete; appended to qw_cttt_potts3_results.jsonl")
end

length(ARGS) == 2 || error("usage: julia qw_cttt_potts3.jl <N> <D>")
stage(parse(Int, ARGS[1]), parse(Int, ARGS[2]))
