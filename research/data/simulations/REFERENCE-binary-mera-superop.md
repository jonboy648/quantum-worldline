# Authoritative binary MERA scaling superoperator — reference (Google TensorNetwork simple_mera.py)

Source: github.com/google/TensorNetwork `examples/simple_mera/simple_mera.py` (tested, runnable).
Fetched 2026-06-18. This is the CORRECTION to the SIM-041 hand-rolled superoperator, which the
adversarial workflow (wf_b7ee088b-921) proved wrong: any ONE-SITE superoperator (with or without u)
is gauge-equivalent to a bare isometry channel — the disentangler is absorbable. A disentangler only
survives the trace when it STRADDLES TWO isometries, which requires the genuine binary causal cone
(3 isometries + 2 disentanglers per term). Neither one-site build ever produced Ising {0,1/8,1}.

## Key facts
- Tensor conventions: isometry rank-3 `[bottom-left, bottom-right, top]`; disentangler rank-4
  `[bottom-left, bottom-right, top-left, top-right]`. (Match quimb: w=(low,low,up), u=(low,low,up,up).)
- The ascending superoperator = `grad(binary_mera_energy, state)`; descending = `grad(..., hamiltonian)`.
  state = 3-SITE reduced density operator (rank-6); hamiltonian = 3-site operator (rank-6). So the
  natural binary scaling object acts on THREE-site operators (NOT one- or two-site).
- env_iso = grad(energy, isometry); env_dis = grad(energy, disentangler) — the optimization environments.
- Energy network averages 'left' and 'right' placements with weight 0.5 (not 1/3 — that's the
  3-site-operator convention, distinct from EV's 2-site 1/3).

## binary_mera_energy connectivity (VERBATIM leg wiring — the ground truth)
Three isometries iso_l, iso_c, iso_r (+ conjugates); two disentanglers un_l, un_r (+ conj);
op = 3-site hamiltonian (rank-6: legs 0,1,2 = bra; 3,4,5 = ket); rho = 3-site state (rank-6).

Shared (both directions):
  iso_l[2]-rho[0], iso_c[2]-rho[1], iso_r[2]-rho[2]          # isometry tops -> state (ket)
  iso_l[0]-iso_l_con[0]                                       # left isometry outer leg traced
  iso_l[1]-un_l[2], iso_c[0]-un_l[3]                          # un_l straddles iso_l & iso_c  <-- u survives
  iso_c[1]-un_r[2], iso_r[0]-un_r[3]                          # un_r straddles iso_c & iso_r  <-- u survives
  iso_r[1]-iso_r_con[1]                                       # right isometry outer leg traced
  un_l_con[2]-iso_l_con[1], un_l_con[3]-iso_c_con[0]
  un_r_con[2]-iso_c_con[1], un_r_con[3]-iso_r_con[0]
  iso_l_con[2]-rho[3], iso_c_con[2]-rho[4], iso_r_con[2]-rho[5]   # conj isometry tops -> state (bra)

dirn == 'right':
  un_l[0]-un_l_con[0]; un_l[1]-op[3]; un_r[0]-op[4]; un_r[1]-op[5]
  op[0]-un_l_con[1]; op[1]-un_r_con[0]; op[2]-un_r_con[1]
dirn == 'left':
  un_l[0]-op[3]; un_l[1]-op[4]; un_r[0]-op[5]; un_r[1]-un_r_con[1]
  op[0]-un_l_con[0]; op[1]-un_l_con[1]; op[2]-un_r_con[0]

energy = 0.5 * (left + right)

## Implementation plan (correct)
1. Replicate binary_mera_energy(op3, rho3, w, u) in torch (or numpy+autograd) with this EXACT wiring.
2. Ascending superoperator A on 3-site ops: A(op3) = grad(energy, rho)  (or build the matrix by
   applying to each basis 3-site operator). Descending D = grad(energy, op).
3. Scaling superoperator = A at the scale-invariant fixed point. Diagonalize A as a linear map on the
   3-site operator space (chi^6 x chi^6) -> eigenvalues lambda; Delta = -log_2(lambda); pin identity to 0.
4. GATE B: on a CONVERGED critical-Ising (u,w), the lowest dims must be {0, 1/8, 1, 9/8, 2, ...}.
   (chi^6 is large at chi=4 = 4096-dim operator space -> 4096x4096 superop; eigs() for the lowest ~20.
   Memory: 4096^2 complex ~ 270 MB, fine; building it = 4096 grad evals — do on RunPod.)
5. Only after GATE B passes -> TCI, hunt Delta_T=2.

## Why this matters
The one-site shortcut (SIM-041 v1) passes the identity gate (S(I)=I is automatic for any isometric
assembly) but gives the WRONG spectrum because it cannot represent the binary causal cone. The
3-site grad-of-energy superoperator is the tested, correct object. Use autodiff (torch) for the
contraction so there are zero hand-wiring bugs — replicate the connectivity above, differentiate.
