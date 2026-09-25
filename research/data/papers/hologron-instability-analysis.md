# Hologron Instability: Deep Analysis and Practical Implications
**Date:** 2026-03-11
**Source paper:** Wang & He, arXiv:2501.03084 (Jan 2025)
**Status:** ACTIONABLE — concrete code changes identified

---

## 1. What Exactly Makes Hologrons Unstable

A hologron is defined as a bulk spin-flip state: `|Psi_j^h> = X_j |GS>`, where `X_j` is the Pauli X operator on the j-th bulk spin and `|GS>` is the MERA ground state. An n-hologron state is `prod(X_{j1}...X_{jn}) |GS>`.

**The mechanism of instability:**

The MERA bulk Hilbert space has dimension `2^(L-4) * 2^4 = 2^L`. The bulk ground state has the structure `|GS> = |0>^(x(L-4)) tensor |psi_0>`, where the last 4 qubits form the infrared (IR) core region with 16 independent states `{|psi_k>, k=0..15}`.

The hologron basis `{X_{j1}...X_{jn} |GS>}` only uses the ground state of the IR region (`k=0`). This means the n-hologron subspace is a proper subspace of a larger "generalized n-hologron subspace" that includes all 16 IR states:

```
Generalized n-hologron: |Psi^{j1..jn}_{n,k}> = X_{j1}...X_{jn} |0>^(x(L-4)) tensor |psi_k>
```

The energy ranges of 1-hologron states and 2-hologron + IR-excited states overlap substantially. There is no energy gap protecting the 1-hologron sector from decaying into generalized multi-particle states. Unitary time evolution under `H = U^dag H_boundary U` conserves energy, and there are always accessible states outside the 1-hologron subspace at the same energy.

Wang & He confirm this numerically:
- `P_1^h(t)` (probability of staying in 1-hologron subspace) decays exponentially: tau = 0.51 (bulk site j=7) or tau = 0.85 (bulk site j=4)
- Even the generalized 1-hologron subspace (all 16 IR sectors) shows decay with tau = 0.76 or 2.39
- The 2- and 3-hologron populations grow as the 1-hologron decays — these are decay products

**Key contrast:** Hologrons ARE stable in the Chua et al. (2017) model which uses `H_C-Ising = -(L/4pi) sum(Z_j + X_j X_{j+1})`. In that model, the bulk spin-flip operator `X_j` happens to be the leading-order lattice approximation of the Ising CFT spin primary operator `sigma_CFT`. Since `sigma_CFT` creates an eigenstate by the operator-state correspondence, the 1-hologron subspace = primary eigenspace, and there is no decay.

**Why our model differs:** The Sahay-Lukin-Cotler model (which we use) has `H_boundary = (J*L/4pi) sum(X_{j-1} Z_j X_{j+1} - X_j X_{j+1})`. This Hamiltonian is related to `H_C-Ising` by the unitary `V = prod_j (i X_j X_{j+1} - I_j I_{j+1}) / sqrt(2)`. Under this transformation, the spin-flip `X_j` in the new basis is NOT the primary operator `sigma_CFT` — it has non-trivial expansion in primary + descendant operators. Therefore X_j (our Ry hologron) creates a superposition of many energy eigenstates, which dephase under time evolution.

---

## 2. The Stable Alternative: Boundary-Primary Excitations

Wang & He construct stable quasiparticles as follows.

**Step 1: Identify the lattice primary operator for H_C-Ising.**
From Zou, Milsted & Vidal (PRL 2020), the lattice realization of `sigma_CFT` for `H_C-Ising` is:
```
sigma^{C-Ising}_j = 0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})
```
(higher-order terms are small and can be neglected)

**Step 2: Transform to our boundary Hamiltonian.**
Using `V = prod_j (i X_j X_{j+1} - I_j I_{j+1}) / sqrt(2)` (the Evenbly-White unitary connecting the two models):
```
sigma^boundary_j = V^dag sigma^{C-Ising}_j V
```
The explicit result (Wang & He Eq. 3):
```
sigma^boundary_j = V^dag [0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})] V
```

**Step 3: Create the bulk quasiparticle state.**
```
|Psi_j>^{sigma} = U^dag sigma^boundary_j U |GS>
                = U^dag sigma^boundary_j |GS_boundary>
```
where `U` is the MERA unitary map (boundary -> bulk direction), `|GS_boundary> = U|GS>` is the boundary ground state.

This state has 97.5% probability within the primary + first- and second-derivative descendant subspace at late times. It is dynamically stable because the CFT operator-state correspondence guarantees that (in the thermodynamic limit) `sigma_CFT |GS_CFT>` is an energy eigenstate.

**Key property:** The stable quasiparticles have attractive interactions (Wang & He Fig. 2b): `U_int(j,j') < 0` for all separations measured (j'=5,6,7,8 relative to j=4). This is the same attractive force signature as the original Sahay et al. hologron result — but now from stable excitations.

---

## 3. Holographic Transportation: What It Is and How to Measure It

**Definition:** A boundary excitation created by a spacetime-localized perturbation `delta_H(t) = -sum_i J_i(t) Y_i` (Y_i coupling) temporarily vanishes from the boundary while the excitation propagates radially inward through the MERA bulk, then reappears on the opposite side of the boundary.

**Geodesic interpretation:** The parameters of the source `J_i(t) = A * exp[-(t^2/2 sigma_t^2) - (phi_i^2/2 sigma_phi^2) - i*Omega*t + i*M*phi_i]` encode the energy `Omega` and angular momentum `M` of an AdS bulk null geodesic. The transportation time is set by the AdS null geodesic traversal time through the extra dimension.

**Observable timescales (L=16, J=1, Omega=5, sigma_t=sigma_phi=0.4, M=0):**
- t=0: boundary excitation appears
- t~1.5: boundary excitation vanishes (excitation is traversing the bulk radially inward)
- t~2.5: boundary excitation reappears on the opposite side

**What to track:**
- Boundary: `rho^boundary_i[Y_i](t) = <Psi(t)|Y_i|Psi(t)> - <GS|Y_i|GS>` — should show vanishing then reappearance
- Bulk: `rho^bulk_i(t) = <Psi(t)|(I+Z_i)/2|Psi(t)> - <GS|(I+Z_i)/2|GS>` (accessed via reverse MERA) — should show radial inward propagation

**Why Y_i and not X_i or Ry?** The Y_i operator couples to the time-derivative descendant `d_tau sigma_CFT` of the primary (see Supplemental Material Eq. S11: `Y_j ~ 0.803 i d_tau sigma_CFT`). This creates the right wavepacket energy-momentum profile to excite a geodesic mode. X_i would excite the primary itself (which is a standing mode, not a traveling wavepacket).

---

## 4. Does Hologron Instability Explain Our Flat Force Profile in SIM-2026-005?

**Short answer: Probably not directly. Two separate problems are at play.**

**Problem 1 (dynamic instability, Wang & He):** Hologrons decay in real-time evolution with timescale tau ~ 0.5-0.85/J. This matters for DYNAMIC measurements (time evolution, transport). Our SIM-2026-002 and SIM-2026-005 use STATIC energy differences `U_int = E_2h - 2*E_1h`, not time evolution. Static energy differences are well-defined even for unstable states — they just don't correspond to observable quasiparticle dynamics.

**Problem 2 (flat force profile, SIM-2026-005):** The flat profile `V(dr) ~ -0.001` for all dr in SIM-2026-005 (Z2-projected, 16q) is almost certainly due to poor VQE convergence rather than hologron instability. Evidence:
- The Z2 projection creates a non-smooth optimization landscape (normalization discontinuities)
- Convergence rate was ~6x slower than no-Z2 (0.25 energy/500 evals vs 1.5/500)
- The best energy E=-19.373 (3.22% error) was worse than no-Z2 E=-19.642 (1.87% error)
- The ground state was poorly approximated — so the hologron energy differences measure noise, not physics

**The connection:** However, there IS a related issue. If the MERA circuit with Z2 projection converges to a ground state that has different symmetry structure than the true critical ground state, then:
- The boundary primary operators `sigma^boundary_j` may not create well-defined quasiparticles in the projected state
- The hologron X_j overlap with the actual lowest-energy excitations may be suppressed
- This could amplify the flatness of any force measurement

**Bottom line:** The Z2-projected VQE has two compounding problems — poor convergence AND using Ry hologrons that are not the stable excitation type. Fixing convergence (penalty method or layer-by-layer init) is the first priority. Using boundary primaries for the force measurement is the second priority and would also give a cleaner observable.

---

## 5. Practical Code Changes

### 5a. Switching from Ry Hologrons to Boundary-Primary Excitations

Our current hologron insertion code (from vqe_z2_enforced_24q_runpod.py and related scripts):
```python
# Current: insert hologron at bulk qubit index j
def insert_hologron(circuit, bulk_qubit_index, angle=np.pi/3):
    circuit.ry(angle, bulk_qubit_index)
```

**New approach (boundary-primary, conceptually):**

This requires understanding the circuit structure. The MERA circuit `U` maps bulk state -> boundary state. In our Qiskit implementation, we:
1. Start with bulk ground state `|0...0>|psi_0>` (the MERA ansatz)
2. Apply `U` (the MERA layers) to get boundary state
3. Measure boundary Hamiltonian H_boundary

For boundary-primary excitation, the protocol is:

```python
def insert_boundary_primary(circuit, boundary_qubit_j, L):
    """
    Apply the boundary primary operator sigma^boundary_j to boundary qubit j.
    To leading order: sigma^boundary_j ~ 0.635*(X_j + X_{j+1})

    Since this is not unitary, we use the following approach:
    - Compute the state |Psi_j> = sigma^boundary_j |GS_boundary> / norm
    - This is done by first preparing |GS_boundary> (run MERA forward),
      applying sigma^boundary_j as a projector (not a gate), then applying
      U^dag to get the bulk quasiparticle state.

    Practical circuit approximation:
    The leading-order term 0.635*(X_j + X_{j+1}) applied to |0>^L gives
    a state with weight on both |...1_j...> and |...1_{j+1}...>.
    We can approximate this by applying a CNOT-type entangler:

    Actually, the cleanest way: do NOT insert hologrons as gates.
    Instead compute energy expectation values by:
    1. Measure E_GS = <GS|H|GS>
    2. Compute E_1(j) = <GS| sigma_j^dag H sigma_j |GS> / <GS|sigma_j^dag sigma_j|GS>
       = <GS_boundary| sigma^boundary_j U H U^dag sigma^boundary_j |GS_boundary> / norm^2
    3. Compute E_2(j,j') analogously with sigma_j * sigma_{j'}
    4. U_int(j,j') = E_2(j,j') - E_1(j) - E_1(j') + E_GS

    This can be done classically (statevector simulation) or as a circuit with
    ancilla-based measurement.
    """
    pass

# The simplest classical implementation for statevector sim:
def compute_force_profile_boundary_primary(theta_opt, n_qubits, n_layers, L):
    """
    Compute force profile using boundary-primary excitations.

    theta_opt: optimized MERA parameters from VQE
    L: number of boundary qubits (= n_qubits in our setup)
    """
    import numpy as np
    from qiskit.quantum_info import Statevector, SparsePauliOp

    # 1. Build MERA circuit with optimal parameters
    mera_circuit = build_mera_circuit(theta_opt, n_qubits, n_layers)
    sv_ground = Statevector(mera_circuit)  # boundary ground state

    # 2. Build boundary Hamiltonian H_boundary
    H = build_boundary_hamiltonian(L)

    # 3. Ground state energy
    E_GS = sv_ground.expectation_value(H).real

    # 4. For each site j, compute single-quasiparticle energy E_1(j)
    energies_1 = []
    for j in range(L):
        # Apply sigma^boundary_j ~ 0.635*(X_j + X_{j+1}) to boundary state
        # Leading order approximation: (X_j + X_{j+1}) |GS>
        sv_j = apply_boundary_primary(sv_ground, j, L)
        norm_sq = sv_j.inner(sv_j).real
        E_1j = sv_j.expectation_value(H).real / norm_sq
        energies_1.append(E_1j)

    # 5. For each pair (j,j'), compute E_2(j,j')
    # U_int(j,j') = E_2(j,j') - E_1(j) - E_1(j') + E_GS
    forces = {}
    for j in range(2, L//2):  # reference site in bulk center
        for jp in range(j+1, L-2):
            sv_jjp = apply_boundary_primary_pair(sv_ground, j, jp, L)
            norm_sq = sv_jjp.inner(sv_jjp).real
            E_2 = sv_jjp.expectation_value(H).real / norm_sq
            U_int = E_2 - energies_1[j] - energies_1[jp] + E_GS
            dr = jp - j
            forces[dr] = U_int

    return forces

def apply_boundary_primary(sv, j, L):
    """Apply (X_j + X_{j+1})/sqrt(2) to statevector. Leading order sigma^boundary_j."""
    from qiskit.quantum_info import Operator, Statevector
    import numpy as np

    # Build X_j operator on L qubits
    X_j = build_single_pauli('X', j, L)
    X_j1 = build_single_pauli('X', (j+1) % L, L)

    sv_j = sv.evolve(X_j)
    sv_j1 = sv.evolve(X_j1)

    # (X_j + X_{j+1})|GS> — unnormalized, will normalize when computing energy
    sv_sum = Statevector(0.635 * np.array(sv_j) + 0.635 * np.array(sv_j1)
                         - 0.026 * (np.array(apply_two_pauli(sv, 'X', j, 'Z', (j+1)%L, L))
                                  + np.array(apply_two_pauli(sv, 'Z', j, 'X', (j+1)%L, L))))
    return sv_sum
```

**Important note:** The leading-order approximation `sigma^boundary_j ~ 0.635*(X_j + X_{j+1})` is quite good — higher-order corrections change normalization by a few percent. For an initial test of whether the boundary-primary force profile is better than hologrons, the leading-order approximation is sufficient.

### 5b. Holographic Transportation Circuit Protocol

```python
def measure_holographic_transportation(theta_opt, n_qubits, n_layers, L,
                                        Omega=5.0, sigma_t=0.4, sigma_phi=0.4, M=0,
                                        t_max=5.0, n_steps=50):
    """
    Measure holographic transportation observable on MERA circuit.

    Protocol:
    1. Prepare boundary ground state
    2. Time-evolve under H_boundary + delta_H(t)
    3. At each time step, measure:
       - boundary excitation density rho^boundary_i[Y_i]
       - bulk excitation density rho^bulk_i (via reverse MERA)
    """
    import numpy as np
    from scipy.linalg import expm

    # Build MERA circuit and get boundary ground state
    mera_circuit = build_mera_circuit(theta_opt, n_qubits, n_layers)
    sv_0 = Statevector(mera_circuit)  # boundary ground state

    H_boundary = build_boundary_hamiltonian_matrix(L)

    # Time evolution
    dt = t_max / n_steps
    times = np.linspace(0, t_max, n_steps+1)

    boundary_densities = []  # shape: (n_steps+1, L)
    bulk_densities = []      # shape: (n_steps+1, L-4)

    sv_t = np.array(sv_0)

    for step, t in enumerate(times):
        # Measure boundary excitation density rho^boundary_i[Y_i]
        rho_boundary = []
        for i in range(L):
            Y_i = build_single_pauli_matrix('Y', i, L)
            rho_i = np.real(sv_t.conj() @ Y_i @ sv_t)
            rho_i_gs = np.real(np.array(sv_0).conj() @ Y_i @ np.array(sv_0))
            rho_boundary.append(rho_i - rho_i_gs)
        boundary_densities.append(rho_boundary)

        # Get bulk state via reverse MERA (U^dag |Psi_boundary(t)>)
        sv_bulk = apply_reverse_mera(sv_t, theta_opt, n_qubits, n_layers)
        sv_bulk_gs = apply_reverse_mera(np.array(sv_0), theta_opt, n_qubits, n_layers)

        # Measure bulk excitation density rho^bulk_i
        rho_bulk = []
        for i in range(L-4):  # bulk has L-4 sites
            Zi = build_single_pauli_matrix('Z', i, L-4)
            Ii = np.eye(2**(L-4))
            proj_i = (Ii + Zi) / 2
            rho_i_bulk = np.real(sv_bulk.conj() @ proj_i @ sv_bulk)
            rho_i_bulk_gs = np.real(sv_bulk_gs.conj() @ proj_i @ sv_bulk_gs)
            rho_bulk.append(rho_i_bulk - rho_i_bulk_gs)
        bulk_densities.append(rho_bulk)

        # Time-evolve: U(dt) = exp(-i (H_boundary + delta_H(t)) dt)
        phi_i = np.array([2*np.pi*i/L - 3*np.pi/4 for i in range(L)])
        A = np.sqrt(2*L / (sigma_t * sigma_phi)) / (40 * np.pi)
        J_i = A * np.exp(-(t**2)/(2*sigma_t**2) - (phi_i**2)/(2*sigma_phi**2)
                         - 1j*Omega*t + 1j*M*phi_i)

        delta_H = np.zeros_like(H_boundary, dtype=complex)
        for i in range(L):
            Y_i_mat = build_single_pauli_matrix('Y', i, L)
            delta_H -= J_i[i] * Y_i_mat

        H_total = H_boundary + delta_H
        U_dt = expm(-1j * H_total * dt)
        sv_t = U_dt @ sv_t

    return times, boundary_densities, bulk_densities
```

**Expected signal:** Plot `rho^boundary_i[Y_i](t)` as a function of boundary site `i` and time `t`. Should show:
- A localized excitation appearing at t=0 near the source location
- The excitation density going to zero at t~1.5 (excitation has entered the bulk)
- The excitation reappearing on the opposite side at t~2.5

This is a clean experimental signal — it does NOT require measuring energies, does NOT require VQE optimization, and does NOT require Z2 symmetry considerations.

---

## 6. Connection to Z2 Flat-Force Problem

**Revised diagnosis of SIM-2026-005:**

The flat force profile in SIM-2026-005 has two compounding causes:
1. **VQE convergence failure** (primary): Z2 projection creates non-smooth landscape, poor Hessian approximation for L-BFGS-B, 3.22% energy error (vs 1.87% without Z2). The ground state is poorly approximated, so all downstream observables are contaminated.
2. **Hologron basis issue** (secondary, less certain): With Z2 projection enforcing `<P>=+1`, the Z2-odd component of the Ry hologron is projected out. The primary operator `sigma_CFT` has scaling dimension `Delta_sigma = 1/8` and is Z2-odd. The Ry rotation creates `cos(pi/6)|0> + sin(pi/6)|1>`, which has a Z2-odd component. The Z2 projection `(I+P)/2` partially projects this out, leaving a state with less overlap on the primary excitation subspace.

**Recommended test:** After fixing Z2 convergence (penalty method), compare two force profiles:
- Profile A: Ry(pi/3) hologrons (current approach, but with good convergence)
- Profile B: Boundary-primary excitations `(X_j + X_{j+1})|GS>`

If Profile B is substantially better even at good convergence, it confirms the boundary-primary approach is necessary. If both give similar results at good convergence, the hologron basis was fine and the flat profile was purely a convergence artifact.

---

## 7. Priority Action Items

**Priority 1 (zero cost, test immediately):**
Compute the force profile using boundary-primary operators on the ALREADY OPTIMIZED theta_opt from SIM-2026-002 (16q, no-Z2, 1.87% error). This requires only statevector operations, no VQE. If the boundary-primary force profile looks better than the Ry hologron force profile on the same ground state, we have confirmed the instability connection.

**Priority 2 (ongoing):**
Wait for SIM-2026-006 results (24q Z2-projected RunPod run). If force profile is still flat, diagnose whether it is convergence (check energy error vs E0) or hologron-basis (compare boundary-primary on same ground state).

**Priority 3 (new simulation):**
Implement boundary-primary force profile measurement as a separate script `measure_boundary_primary_forces.py` that takes `theta_opt_SIM2026002.npy` as input and outputs `U_int(dr)` for dr=1..7.

**Priority 4 (new experiment):**
Implement holographic transportation measurement on L=16 MERA circuit. This is a completely new observable that requires only time evolution — no VQE. Script: `measure_holographic_transport.py`. Expected runtime: fast (L=16, statevector, 50 time steps, dense 2^16 matrix).

---

## 8. Key Numbers and Formulas to Implement

### Boundary primary operator (to leading order)
```
sigma^boundary_j = 0.635*(X_j + X_{j+1}) - 0.026*(X_j Z_{j+1} + Z_j X_{j+1})
```
Note: this is for the H_boundary Hamiltonian with the XZX - XX structure. The prefactors 0.635 and 0.026 come from the Zou-Milsted-Vidal (2020) variational calculation of the Ising CFT primary on the lattice.

### MERA unitary (for reversing)
The MERA unitary U has analytic form from Evenbly & White (2016):
```
u^dag_{j,j+1} = ((sqrt(3)+2)/4)*I_j I_{j+1} + ((sqrt(3)-2)/4)*Z_j Z_{j+1}
                + (i/4)*X_j Y_{j+1} + (i/4)*Y_j X_{j+1}

w^dag_{j,j+1} = ((sqrt(3)+sqrt(2))/4)*I_j I_{j+1} + ((sqrt(3)-sqrt(2))/4)*Z_j Z_{j+1}
                + (i*(1+sqrt(2))/4)*X_j Y_{j+1} + (i*(1-sqrt(2))/4)*Y_j X_{j+1}
```
Applied as: `U = prod_{l=2}^{D-1} (prod_j u^dag_{2j,2j+1}) * w^dag^{tensor 2^l}`
where D = log2(L).

### Holographic transportation perturbation
```
J_i(t) = A * exp[-(t^2/2 sigma_t^2) - (phi_i^2/2 sigma_phi^2) - i*Omega*t + i*M*phi_i]
phi_i = 2*pi*i/L - 3*pi/4  (for i = 1..L)
A = sqrt(2*L / (sigma_t * sigma_phi)) / (40*pi)
delta_H(t) = -sum_i J_i(t) * Y_i  (Y-coupling, not X)
```
Default parameters: Omega=5, sigma_t=sigma_phi=0.4, M=0

---

## Summary

Hologron instability (Wang & He 2025) is a real dynamical effect: bulk spin-flip states decay with tau ~ 0.5-0.85/J due to the incomplete basis structure of the hologron subspace. The stable alternative is boundary-primary excitations constructed from the Ising CFT primary operator `sigma_CFT` mapped through the MERA unitary.

For our static force measurements, hologron instability is not directly responsible for the flat force profile in SIM-2026-005. That is primarily a VQE convergence failure. However, using boundary-primary excitations would give cleaner force profiles even at good convergence, and opens the door to dynamical measurements (holographic transportation) that are entirely out of reach with the current Ry hologron approach.

The practical boundary-primary operator to leading order is `sigma^boundary_j ~ 0.635*(X_j + X_{j+1})`, which is implementable in ~20 lines of Python using existing SIM-2026-002 ground state parameters.
