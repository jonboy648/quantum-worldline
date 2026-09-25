# qw_cttt_of.jl — C_TTT at the tricritical Ising point via puMPS Koo-Saleur matrix elements
#
# ONE (N, D) STAGE PER INVOCATION, checkpointed + resumable:
#   OPENBLAS_NUM_THREADS=1 julia --project=. qw_cttt_of.jl <N> <D>
# GS checkpoint: of_gs_N{N}_D{D}.jld2 (raw A tensor; kills only cost the in-flight stage).
# Results appended as one JSON line per stage to qw_cttt_of_results.jsonl.
#
# Model: O'Brien-Fendley chain, puMPS convention h = -l1(ZZ + X) + l2(ZZX + XZZ).
# Our SIM-051/067 convention (-2(Z+XX) + l3(ZXX+XXZ), l3=0.856) maps to l1=1, l2=0.428
# at HALF our energy normalization (see pumps-setup/VENDOR.md) -- v is CALIBRATED, never assumed.
#
# TCI M(4,5) reference data: Delta_sigma=3/40, Delta_eps=1/5, Delta_sigma'=7/8, Delta_eps'=6/5;
# k=+-2 low cluster: T(2.0), L2sigma(2.075), L2eps(2.2 -- the contaminator, element ~N^-0.2).
# Targets: c = 7/10, C_TTT = 2*sqrt(2)/sqrt(c) = 3.3806.
#
# v calibration: v_T from Delta_T=2 (exact in any CFT; used for c), cross-checked by
# v_eps from Delta_eps=1/5 and v_sigma from Delta_sigma=3/40 (fixed-point-quality gate).

include("MPS.jl")
include("puMPS.jl")
using .MPS
using .puMPS
using LinearAlgebra, Printf, JLD2

const L1 = 1.0
const L2 = 0.428          # = our lambda3 0.856 / 2 (TCI point)
const D_SIGMA = 3/40
const D_EPS   = 1/5
const NK0     = 5          # states at k=0: I, sigma, eps, sigma', (eps' or desc)
const NK2     = 4          # states at k=+-2: T, L2sigma, L2eps, next

function get_gs(N::Int, D::Int)
    ckpt = "of_gs_N$(N)_D$(D).jld2"
    H_MPO = OBF_local_MPO(ComplexF64, lambda1=L1, lambda2=L2)
    converged_flag = false
    if isfile(ckpt)
        A = load(ckpt, "A")
        M = puMPState(A, N)
        converged_flag = get(load(ckpt), "converged", true)   # legacy ckpts were post-convergence
        println("resumed GS from $ckpt (converged=$converged_flag)")
        if converged_flag
            return M, real(expect(M, H_MPO)), H_MPO
        end
    else
        # DIRECT random init at target D. Do NOT warm-start by padding a smaller-D
        # checkpoint: the padded tensor's near-rank-deficient transfer matrix throws
        # LAPACKException(30) in canonicalize/eigsolve -- the SAME failure MERAKit's
        # chi-ramp hit (memory: "direct-init at target chi; ramp -> LAPACKException").
        M = rand_puMPState(ComplexF64, 2, D, N)
        normalize!(M)
        M, _, _ = canonicalize_left!(M)
    end
    # Short rounds + wall-clock budget: exit cleanly (code 42) before the foreground
    # timeout so the invocation is never backgrounded (background jobs keep getting
    # externally killed). Re-invoke until exit 0; each call resumes the checkpoint.
    t0 = time()
    ng = Inf
    for r in 1:240
        M, ng = puMPS.minimize_energy_local_CG!(M, H_MPO, 15, tol=1e-6)
        @printf("  [round %d] |grad| = %.3e  (%.0fs)\n", r, ng, time() - t0)
        save(ckpt, "A", mps_tensor(M), "N", N, "D", D, "lambda2", L2, "converged", ng < 1e-6)
        ng < 1e-6 && break
        if time() - t0 > 420
            println("TIME BUDGET reached, checkpoint saved -- re-invoke to resume")
            exit(42)
        end
    end
    save(ckpt, "A", mps_tensor(M), "N", N, "D", D, "lambda2", L2, "converged", true)
    println("saved GS checkpoint -> $ckpt  (|grad|=$ng)")
    M, real(expect(M, H_MPO)), H_MPO
end

function stage(N::Int, D::Int)
    println("="^70); println("OF TCI stage: N=$N D=$D  (lambda1=$L1, lambda2=$L2)")
    M, e0, _ = get_gs(N, D)
    @printf("e0(per site) = %.10f\n", e0)

    H_split = OBF_PBC_MPO_split(ComplexF64, lambda1=L1, lambda2=L2)
    ens, ks, exs = excitations!(M, H_split, [0, 2, -2], [NK0, NK2, NK2])
    ens = real.(ens)
    i0  = findall(k->k==0,  ks); i0  = i0[sortperm(ens[i0])]
    ip2 = findall(k->k==2,  ks); ip2 = ip2[sortperm(ens[ip2])]
    im2 = findall(k->k==-2, ks); im2 = im2[sortperm(ens[im2])]
    E0 = ens[i0[1]]

    # --- v calibrations from the k=0 tower (identify sigma, eps by gap ratio ~ (1/5)/(3/40) = 2.667)
    g2, g3 = ens[i0[2]]-E0, ens[i0[3]]-E0
    ratio = g3/g2
    v_sig = g2*N/(2pi*D_SIGMA)
    v_eps = g3*N/(2pi*D_EPS)
    # --- v_T from the k=2 cluster: use the ELEMENT-dominant state below (two-pass)
    @printf("k=0 gap ratio (eps/sigma) = %.4f  (M(4,5): 2.6667)\n", ratio)

    # --- KS elements, n=+2 and n=-2
    basis = [exs[i0[1]]; exs[ip2]; exs[im2]]
    ksarg = [0.0, 2.0, -2.0]
    res = Dict{String,Any}("N"=>N, "D"=>D, "e0"=>e0, "ratio_eps_sigma"=>ratio,
                           "v_sigma"=>v_sig, "v_eps"=>v_eps)
    # basis row of sector state j: GS is row 1, then ip2 block, then im2 block.
    # KrylovKit often returns MORE states than requested -- offsets must come from the
    # actual index lists, never from NK2 (the N=14 first run mis-sliced the -2 block).
    row_p2 = j -> 1 + j
    row_m2 = j -> 1 + length(ip2) + j
    for (n, idxs, rowf) in ((2, ip2, row_p2), (-2, im2, row_m2))
        Hn = OBF_Hn_MPO_split(ComplexF64, n, N, lambda1=L1, lambda2=L2)
        Mel = Hn_in_basis(M, Hn, basis, ksarg)
        raw = [abs(Mel[rowf(j), 1]) for j in 1:length(idxs)]   # <k=n state j|Hn|GS>, raw
        # element-dominant state = T (validated: competing physical elements are >=10x smaller;
        # gate below checks Delta_T plausibility so a band-edge false positive cannot slip through)
        jT = argmax(raw)
        DT_check = (ens[idxs[jT]] - E0) * N / (2pi * v_eps)
        1.5 < DT_check < 2.6 || @warn "element-dominant state has Delta=$(DT_check) (v_eps units) -- NOT T-like; inspect"
        ET = ens[idxs[jT]]
        v_T = (ET - E0)*N/(2pi*2.0)
        MT  = raw[jT]*N/(2pi*v_T)
        c   = 2*MT^2
        cttt = 2*sqrt(2)/sqrt(c)
        @printf("\nn=%+d: raw elements (low cluster): %s\n", n,
                join([@sprintf("%.5f", r) for r in raw], "  "))
        @printf("   T = state %d  Delta_T-gap-> v_T = %.6f  (v_sigma %.4f, v_eps %.4f)\n",
                jT, v_T, v_sig, v_eps)
        @printf("   |M_T| = %.6f   c = %.6f (target 0.700)   C_TTT = %.6f (target 3.3806)\n",
                MT, c, cttt)
        # contaminator elements (all non-T), KS-normalized with v_T
        others = [raw[j]*N/(2pi*v_T) for j in 1:length(idxs) if j != jT]
        res["n$(n)"] = Dict("raw"=>raw, "jT"=>jT, "v_T"=>v_T, "M_T"=>MT, "c"=>c,
                            "C_TTT"=>cttt, "others_norm"=>others,
                            "spectrum"=>[ens[i]-E0 for i in idxs])
    end
    res["k0_gaps"] = [ens[i]-E0 for i in i0]

    open("qw_cttt_of_results.jsonl", "a") do io
        # minimal hand-rolled JSON (no deps): flat enough to be safe
        println(io, replace(repr(res), "Dict{String, Any}"=>"", "=>"=>":"))
    end
    println("\nstage complete; appended to qw_cttt_of_results.jsonl")
end

length(ARGS) == 2 || error("usage: julia qw_cttt_of.jl <N> <D>")
stage(parse(Int, ARGS[1]), parse(Int, ARGS[2]))
