# Route X derivation: the exact lattice object behind "timelike entanglement entropy"

Transcribed 2026-09-07 from PAPER-2026-139 (Doi, Harper, Mollabashi, Takayanagi, Taki 2023),
sections 2.1-2.4, into the construction that the HYP-2026-032 drivers implement. Written BEFORE
any driver code, as PREREGISTRATION-HYP032.md requires. Equation numbers are the paper's.

## 1. What the paper defines

- **Replica definition (2.1-2.4).** Analytically continue the spacelike interval EE to a timelike
  interval. Infinite line: `S = (c/3) log(T0/eps) + i pi c/6` (2.4). Circle of circumference R:
  `S = (c/3) log((R/(pi eps)) sin(pi T0/R)) + i pi c/6` (2.7). Thermal line at inverse temperature
  beta: `(c/3) log((beta/(pi eps)) sinh(pi T0/beta)) + i pi c/6` (2.10).
- **Wick-rotation definition (2.2, "useful for numerical calculations").** Rotate the spacetime by
  ninety degrees: the original time t becomes "space", the original (periodic, circumference R)
  space x becomes Euclidean time. The partition function on the circle becomes
  `Z = Tr[e^{-R H}] = Tr[e^{i R Htilde}]` (2.17-2.18) with `Htilde = i H` the ordinary Hamiltonian of
  the rotated theory (2.19). The reduced object is
  **`rho_A = Tr_B[ e^{i R Htilde} ]`** (2.20),
  i.e. the ordinary finite-temperature reduced density matrix with the substitutions
  **`beta -> i R`, `m -> i m`, `eps -> i eps`** (2.21). At m = 0 this is universal for every 2d CFT.
  The paper then reads (2.7) off the thermal formula (2.22) under (2.21).
- **Transition-matrix reading (section 2.3, eq. 2.26).** `e^{i R Htilde}` is the partial trace of a
  thermofield double at imaginary temperature, so `rho_A` is a reduced TRANSITION matrix and the
  quantity is a pseudo entropy `S = -Tr[rho_A log rho_A]` (1.5), complex in general.
- **Their numerics (2.3-2.4).** Free scalar and free Dirac fermion on a lattice, Gaussian method:
  the two-point functions of `e^{i R Htilde}` restricted to the interval, entropy from the spectrum
  of the restricted correlator by the standard Gaussian formula (2.44). Their stated caveat: the
  continuum identity `i k = i omega_k` "is not true on the lattice"; they "introduce the
  aforementioned expressions for the correlators as the correct prescription".

## 2. The lattice object we compute (both routes)

Chain: critical TFIM, `H = -sum_j Z_j Z_{j+1} - sum_j X_j`, h = 1, c = 1/2, **open** boundaries,
length L. The chain runs along the ORIGINAL TIME direction t (the rotated theory's space); by
Lorentz invariance of the Ising CFT the rotated theory is the same CFT, and on the lattice we simply
use the same Hamiltonian, whose continuum limit is that CFT with velocity **v = 2** (single-particle
dispersion `4 |sin(k/2)|`, slope 2 at k -> 0). Open boundaries are chosen so that no fermion-parity
sector bookkeeping (NS/R) enters the trace; the interval sits in the middle of the chain, far from
both ends, and L is increased until the end effect is below the pass tolerance.

**Definition (exact, no prescription):**

    tau_A(R_H, T0) = Tr_B[ e^{i R_H H} ] / Tr[ e^{i R_H H} ],        A = T0 contiguous sites, centred
    S_X(R_H, T0)   = - Tr[ tau_A log tau_A ]                          principal branch, see section 4

`R_H` multiplies H, so the paper's circumference is **`R = v R_H = 2 R_H`** in lattice units. This
gives a TWO-parameter prediction to test, not the paper's one:

    S(R_H, T0) = (1/6) log( (2 R_H / pi) sin( pi T0 / (2 R_H) ) ) + const + i pi/12      (c = 1/2)

`T0` and `R = 2 R_H` are in lattice units; `eps` is absorbed into `const` and into the branch of the
imaginary part (section 4). The Level-1 pass criteria of the pre-registration (slope of Re S
against `log((R/pi) sin(pi T0/R))` within 3 percent of 1/6; Im S within 3 percent of pi/12) apply
with `R = 2 R_H`.

## 3. The two routes and what "agreement" now means

- **Route X (exact).** Full diagonalization of H at L = 10, 12, 14 (dimension 2^L), form
  `e^{i R_H H}` from the spectrum, partial-trace by reshaping, normalize, diagonalize the
  non-Hermitian `tau_A`, sum `-lambda log lambda`.
- **Route G (Gaussian).** Jordan-Wigner to 2L Majoranas; H quadratic. The "state"
  `e^{i R_H H}/Tr` is Gaussian with the imaginary-temperature occupation
  `n_k = 1 / (e^{i R_H eps_k} + 1)`; its Majorana correlation matrix `Gamma` (complex, not
  Hermitian) restricted to A has eigenvalues `+/- i nu_j`; the pseudo entropy is the standard
  Gaussian expression
  `S = sum_j [ -(1+nu_j)/2 log((1+nu_j)/2) - (1-nu_j)/2 log((1-nu_j)/2) ]` with complex `nu_j`.
  Sizes L = 64, 128, 256, 512 (and L = 10-14 for the cross-check).

**Honest consequence, recorded before running.** Because H is exactly quadratic, Route G is an
EXACT evaluation of the same operator as Route X; there is no lattice prescription in our
construction at all, unlike the paper's continuum-dispersion substitution. Therefore the
pre-registration's Level-2a leg ("do the two lattice definitions agree at finite n") is, for this
model, an identity check: **Route G and Route X must agree to 1e-10 at L = 10, 12, 14 for every
(R_H, T0)**, and that agreement is a CONTROL on the code, not a finding. It is kept, as the
pre-registration says, as a gate. The substantive Level-1 content is the c = 1/2 reproduction of
(2.7) in both parameters, which the paper did only for a Dirac fermion (c = 1) and a scalar.
No novelty is claimed for it.

## 4. Branch of the logarithm and the imaginary part

`tau_A` is not Hermitian; its eigenvalues are complex and `-lambda log lambda` needs a branch.
Rule, fixed now: principal branch (`-pi < arg lambda <= pi`), with the eigenvalues tracked
continuously as `T0` increases from 1 site at fixed `R_H`, and separately as `R_H` increases from
`R_H -> 0+` at fixed `T0` (where `tau_A -> 1/2^{T0}`, real, and S is real). A branch crossing
(an eigenvalue's argument passing through pi) is DETECTED and REPORTED as a discontinuity in Im S;
it is never absorbed by re-choosing branches. The paper's sign convention gives `+ i pi c/6`; the
Level-1 criterion is `|Im S| = pi/12` within 3 percent with a single sign throughout the window,
and the sign is reported. If Im S is not constant across the window (2.4-2.10 say it is, for every
geometry), that is a Level-1 failure, i.e. VOID.

## 5. Windows and gates, restated with the lattice parameters

- `R_H` values: 6, 8, 12 (so R = 12, 16, 24) at L >= 256; `T0` from 2 to `R - 2` in unit steps;
  the fit window for the slope is `T0` in `[3, R/2]` (the sine is symmetric about R/2, which is
  itself a check: `S(T0) = S(R - T0)` must hold to the same tolerance, a free control like the
  ring-symmetry gate G2 of the force tests).
- End-effect gate: doubling L from 256 to 512 must change S by less than 1e-3 in both parts over
  the window, or the window is shrunk (recorded) until it does.
- Exactness gate: Route G at L = 10, 12, 14 equals Route X to 1e-10 for every (R_H, T0) in the
  overlap, or Route G is VOID.
- L = 10-14 are too short for a slope fit; they exist for the exactness gate only.

## 6. What the geometry legs will consume

Level 2b (written): a plain MERA has no time direction and integer cuts; nothing here changes that.
Level 3: the glued network for `Tr_B[e^{i R_H H}]` is the MERA for the GS glued to ITSELF through
a brickwork realization of `e^{i R_H H}` (this is the transition-matrix network: `e^{i R_H H}`
inserted between a MERA and its conjugate, traced over B). The Trotter gate (fidelity loss < 1e-6
against exact `e^{i R_H H}` at L = 16-24) and the cut prescription are as pre-registered.
