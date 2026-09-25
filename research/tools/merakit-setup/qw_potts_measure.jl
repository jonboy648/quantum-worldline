# HYP-025: alpha=4 universality at a THIRD CFT class -- the 3-state quantum Potts critical point (c=4/5).
# This extends the universality ladder beyond Ising (c=1/2, HYP-008) and tricritical Ising (c=7/10, HYP-027).
#
# Sharp a-priori test: Delta_T=2 in EVERY unitary 2D CFT, so alpha=2*Delta_T=4 MUST hold at c=4/5 too.
# This is a confirm-or-find-a-bug test, not a fishing expedition.
#
# Model: 3-state quantum Potts chain on a qutrit (d=3) substrate.
#   H = -f * sum_j (X_j + X_j^dag) - sum_j (Z_j Z_{j+1}^dag + h.c.),  critical at f=1.
#   Z = diag(1, w, w^2), X = cyclic shift, w = exp(2pi i/3) (Z3 clock/shift operators).
#   This is the standard self-dual 3-state Potts / Z3 clock critical point, c=4/5.
#
# CFT targets (3-state Potts, c=4/5):
#   Delta_sigma = 2/15 = 0.1333 (order/spin field), Delta_eps = 4/5 = 0.8 (energy),
#   Delta_T = 2.0 (stress tensor; the alpha-relevant universal dimension).
#
# VALIDATION GATE: the MERA must recover c=4/5 primaries (Delta_sigma~0.13, Delta_eps~0.8) before
# Delta_T (and hence alpha) is trusted -- exactly the discipline that caught the wrong basins in TCI.
#
# Adapts the VALIDATED qw_tci_measure.jl driver. The Potts H is 2-site (Z Z^dag + X), so blocking is the
# SIMPLE block_op case (no 3-site straddle like OF) -- block_size=2 -> dim-9 super-sites.
using Random, LinearAlgebra, TensorKit, MERAKit
include("demo/demo_tools.jl"); using .DemoTools

# ---- qutrit Z3 clock/shift operators (d=3) ----
const W = exp(2pi*im/3)
V3 = ComplexSpace(3)
# Z = diag(1, w, w^2) ; X = cyclic shift |k> -> |k+1 mod 3>
Zc = TensorMap(ComplexF64[1 0 0; 0 W 0; 0 0 W^2], V3, V3)
Xc = TensorMap(ComplexF64[0 0 1; 1 0 0; 0 1 0], V3, V3)   # X|0>=|1>,|1>=|2>,|2>=|0>
e3 = id(V3)

# 3-state Potts 2-site local term at criticality f=1, Hermitian:
#   h_local = -(Z (x) Z^dag + Z^dag (x) Z)   [bond]   - f*( (X+X^dag)(x)I + I(x)(X+X^dag) )/2  [field, split over 2 bonds]
# We build the standard self-dual critical Potts Hamiltonian density on a 2-site window, then block.
function potts_local(f=1.0)
    Zd = Zc'                      # Z^dag
    Xsum = Xc + Xc'               # X + X^dag (Hermitian)
    bond = -(Zc ⊗ Zd + Zd ⊗ Zc)  # -(ZZ^dag + Z^dag Z), Hermitian
    field = -f * 0.5 * (Xsum ⊗ e3 + e3 ⊗ Xsum)  # transverse field split across the 2-site density
    h = bond + field
    return 0.5*(h + h')           # enforce Hermiticity numerically
end

function run_potts(chi, maxiter; seed=1, layers=3, f=1.0)
    Random.seed!(seed)
    hloc = potts_local(f)
    h = DemoTools.block_op(hloc, 2)   # block 2 sites -> dim-9 super-site, 2-site blocked op (simple case)
    h = h / 2                          # per-site normalization (block_size=2)
    Vphys = ComplexSpace(9); Vv = ComplexSpace(chi)
    Vs = (Vphys, ntuple(_->Vv, layers-1)...)
    m = random_MERA(TernaryMERA, ComplexF64, Vs)
    pars = (gradient_delta=1e-7, maxiter=maxiter, method=:lbfgs, verbosity=1)
    m = minimize_expectation(m, h, pars)
    E = expect(h, m); sd = scalingdimensions(m)
    dims = sort(real.(get(sd, Trivial(), Float64[])))
    nz = filter(d -> d > 0.02, dims)
    dsig = isempty(nz) ? NaN : nz[1]                       # lowest primary -> Delta_sigma (CFT 0.1333)
    deps = length(nz) >= 2 ? nz[argmin(abs.(nz .- 0.8))] : NaN  # nearest 0.8 -> Delta_eps
    dT   = isempty(nz) ? NaN : nz[argmin(abs.(nz .- 2.0))]      # nearest 2.0 -> Delta_T
    println("=== POTTS c=4/5 chi=$chi seed=$seed: E=$E ===")
    println("SCALDIMS: ", round.(dims[1:min(16,end)], digits=4))
    println("  Delta_sigma (lowest) = ", round(dsig, digits=4), " (Potts CFT 0.1333)")
    println("  Delta_eps (near 0.8) = ", round(deps, digits=4), " (Potts CFT 0.8)")
    println("  Delta_T (near 2.0)   = ", round(dT, digits=4), "  => alpha = ", round(2*dT, digits=4), " (CFT 2 => alpha 4)")
    flush(stdout)
    return (seed=seed, E=E, dsig=dsig, deps=deps, dT=dT, dims=dims)
end

# Multi-seed; select by SPECTRUM (Delta_sigma nearest CFT 0.1333), NOT by energy (flat across basins).
results = []
for s in 1:8
    try
        push!(results, run_potts(6, 2500; seed=s))
    catch err
        println("seed $s FAILED: ", err); flush(stdout)
    end
end
println("\n===== SUMMARY (all seeds) =====")
for r in results
    println("seed $(r.seed): E=$(round(r.E,digits=6))  Dsig=$(round(r.dsig,digits=4))  Deps=$(round(r.deps,digits=4))  DeltaT=$(round(r.dT,digits=4))  alpha=$(round(2*r.dT,digits=4))")
end
if !isempty(results)
    best = results[argmin([abs(r.dsig - 0.1333) for r in results])]
    println("\nBEST-SPECTRUM seed = $(best.seed): Dsig=$(round(best.dsig,digits=4)) Deps=$(round(best.deps,digits=4)) DeltaT=$(round(best.dT,digits=4)) => alpha=$(round(2*best.dT,digits=4))")
    println("VALIDATION GATE: Dsig~0.133 AND Deps~0.8 must hold before trusting alpha.")
end
println("QW_POTTS_MEASURE DONE")
