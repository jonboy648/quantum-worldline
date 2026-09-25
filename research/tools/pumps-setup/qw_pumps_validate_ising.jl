# qw_pumps_validate_ising.jl — VALIDATION GATE for the vendored ZMV puMPS codebase
#
# Purpose: reproduce SIM-067's circle/Koo-Saleur C_TTT extraction at ED-accessible N using
# puMPS Bloch states, BEFORE trusting the method at N=64-128 (TCI/Potts production).
# Run from inside research/tools/puMPS/ :
#   OPENBLAS_NUM_THREADS=1 julia --project=. qw_pumps_validate_ising.jl
#
# Convention (matches qw_cttt_circle.py / SIM-067):
#   h_j = -(X_j X_{j+1} + Z_j)  [= ising_local_MPO defaults, hz=1]   v_exact = 2
#   H_n(puMPS) = sum_j e^{i n j 2pi/N} h_j          (models.jl ising_Hn_MPO_split)
#   KS-normalized element:  M_T0 = (N / (2pi v)) * <T| H_n |0>
#   c_meas  = 2 |M_T0|^2          C_TTT = 2 sqrt(2) / sqrt(c_meas)
#   Delta_T = (E_T - E_0) * N / (2pi v)   (should -> 2)
# The wrong-chirality element <s=+2| H_{-2} |0> is a STRUCTURAL zero here: Hn_in_basis
# enforces spin(bra) = spin(ket) + n, i.e. momentum conservation is exact on the ring.
# (In SIM-067's dense-ED route this zero was a measured 0.0000 gate; here it is by construction.)

include("MPS.jl")
include("puMPS.jl")
using .MPS
using .puMPS
using LinearAlgebra, Printf

const v_exact = 2.0

function converge_gs!(M, H_MPO; tol=1e-6, rounds=8, itr=300)
    # CG optimizer (the PRL's choice). The plain-gradient version's linesearch thrashes
    # ("Initial step was too large" spam) -- do not switch back.
    ng = Inf
    for r in 1:rounds
        M, ng = puMPS.minimize_energy_local_CG!(M, H_MPO, itr, tol=tol)  # not exported
        @printf("  [round %d] |grad| = %.3e\n", r, ng)
        ng < tol && break
    end
    M, ng
end

function validate(N::Int, D::Int; tol=1e-7)
    println("="^70)
    println("N=$N  D=$D")
    H_MPO = ising_local_MPO(ComplexF64)                 # local 2-site term
    M = rand_puMPState(ComplexF64, 2, D, N)
    normalize!(M)
    M, _, _ = canonicalize_left!(M)
    M, ng = converge_gs!(M, H_MPO)
    e_gs = real(expect(M, H_MPO))
    @printf("GS converged: |grad|=%.2e   e0(per site)=%.10f\n", ng, e_gs)

    # Bloch excitations: k=0 (identity tower incl. GS), k=+2 and k=-2 (T and Tbar)
    H_split = ising_PBC_MPO_split(ComplexF64, hz=1.0)
    ens, ks, exs = excitations!(M, H_split, [0, 2, -2], [3, 2, 2])
    ens = real.(ens)
    println("\n  k    E (abs)        Delta = (E-E0)*N/(2 pi v)")
    E0 = minimum(ens[ks .== 0])
    for i in eachindex(ens)
        @printf("  %+d   %.8f   %.6f\n", ks[i], ens[i], (ens[i]-E0)*N/(2pi*v_exact))
    end

    # basis: GS + two lowest states in each of k=+2, k=-2
    idx0  = findall(k->k==0,  ks); idx0  = idx0[sortperm(ens[idx0])]
    idxp2 = findall(k->k==2,  ks); idxp2 = idxp2[sortperm(ens[idxp2])]
    idxm2 = findall(k->k==-2, ks); idxm2 = idxm2[sortperm(ens[idxm2])]
    gs_i  = idx0[1]
    basis = [exs[gs_i]; exs[idxp2[1:2]]; exs[idxm2[1:2]]]
    bl    = ["GS", "k+2 lowest (T?)", "k+2 next (ddsigma?)", "k-2 lowest (Tbar?)", "k-2 next"]
    ksarg = [0.0, 2.0, -2.0]

    for n in (2, -2)
        Hn = ising_Hn_MPO_split(ComplexF64, n, N)
        Mel = Hn_in_basis(M, Hn, basis, ksarg)
        println("\n  H_{n=$n} elements vs GS (KS-normalized |M| = |<a|Hn|0>|*N/(2 pi v)):")
        for b in 2:length(basis)
            m = Mel[b, 1] * N / (2pi * v_exact)
            @printf("    <%-22s|H_%+d|GS>:  |M| = %.6f\n", bl[b], n, abs(m))
        end
        # the T element: spin +n sector, lowest state
        t_b = n == 2 ? 2 : 4
        MT0 = abs(Mel[t_b, 1] * N / (2pi * v_exact))
        c_meas = 2 * MT0^2
        if MT0 > 1e-8
            @printf("  --> c_meas(n=%+d) = %.6f    C_TTT = %.6f  (exact 4.0)\n",
                    n, c_meas, 2*sqrt(2)/sqrt(c_meas))
        end
    end

    # Delta_T gate from energies
    DT = (ens[idxp2[1]] - E0) * N / (2pi * v_exact)
    @printf("\n  Delta_T(energy) = %.6f  (exact 2.0)\n", DT)
    println("="^70)
end

validate(12, 8)
validate(16, 12)
