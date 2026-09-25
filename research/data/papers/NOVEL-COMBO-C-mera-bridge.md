# NOVEL-COMBO-C: MERA / Holographic-CFT -> Physical Measurement Bridges

**Framing C** of a 3-part investigation. Goal: tie THIS PROJECT's published physics
(alpha~=4 holographic stress-tensor force; T=(pi/2)*l_AdS transport, 0.72% at N=16;
chi=3 MERA tensor network; 2D Ising-CFT correspondence; Zenodo DOI
10.5281/zenodo.19661227) to a *physical* measurement -- a novel combination of the
project's holographic/CFT results with a real measurable system, while AVOIDING the
known HYP-2026-017 killer issues (R1 hologron decay, R2 single-site-density energy
estimator, R3/R4 single-basis TEE, blockade-pathological reduced-atom geometry).

Status: IN PROGRESS
Date: 2026-05-16
Owner: framing-C MERA-bridge agent

Prior-art note: the paper-search MCP returned a fixed recent-feed (not relevance
matched) on two consecutive queries, so prior art is grounded in the citations
already validated in project MEMORY / hypothesis records: Sahay-Lukin-Cotler
(arXiv:2401.13595, PRX 15 021078), Wang & He (arXiv:2501.03084; arXiv:2603.07639),
Guo & Swingle (arXiv:2604.19876), Ebadi et al. (Nature 595 227, arXiv:2012.12281),
Wurtz et al. Aquila whitepaper (arXiv:2306.11727), plus standard analog-gravity
literature (Unruh 1981; Steinhauer Nature Phys. 2016; Carusotto-Rousseaux).

## Ranked Candidates

| Rank | Bridge | Project result | CFT quantity measured | Killer avoided | N | B | U | Product |
|------|--------|----------------|-----------------------|----------------|---|---|---|---------|
| 1 | C1 Rydberg static-CFT connected-correlator on QuEra Aquila (Delta-sweep prepared Ising ground state, bitstring `<Z_iZ_j>_c`) | alpha~=4 stress-tensor force; 2D Ising-CFT correspondence | Equal-time boundary 2-pt function `<Z_iZ_j>_c ~ r^-4` (stress-tensor channel) | R1 (no hologron: static prepared state, zero time evolution), R2 (explicit connected correlator from bitstrings), R3/R4 (no TEE) | 4 | 4 | 5 | 80 |
| 2 | C2 Passive transmission-line / LC-ladder MERA emulator | alpha~=4 force; chi=3 MERA causal-cone geometry | Engineered ladder Green's function `G(dr) ~ dr^-4`; finite-size alpha scaling at N>24 | All (no quantum hardware; classical RF) | 4 | 5 | 4 | 80 |
| 3 | C3 Coupled-resonator hyperbolic-lattice transport analog | T=(pi/2)*l_AdS transport (0.72% @ N=16) | Antipodal wave-packet transport time vs network depth L | All (classical wave network) | 4 | 4 | 4 | 64 |
| 4 | C4 Cheap classical-compute chi=3 MERA finite-size alpha at N=32,48 | alpha~=4 force; chi=3 MERA | `<Z_iZ_j>_c ~ r^-4` finite-size scaling beyond published N=16/24 | All (no hardware; reuses connected-correlator back-end) | 3 | 5 | 4 | 60 |
| 5 | C5 DIY NV/SPAD g2 photon-correlation witness for tabletop wave-optics holographic-transport rig | T=(pi/2)*l_AdS transport | Optical intensity-correlation transport-time analog | All (classical optics + DIY sensor) | 3 | 3 | 3 | 27 |
| 6 | C6 Magnonic (spin-wave) dispersion analog of the force law | alpha~=4 force | Spin-wave Green's function `~ dr^-4` | All (classical magnonics) | 3 | 2 | 3 | 18 |
| 7 | C7 [KILLER-TRIP] Excite a hologron on Aquila and watch its decay | alpha~=4 force | Hologron energy vs separation | TRIPS R1 (decay << window); B capped at 2 | 2 | 2 | 2 | 8 |

## Editorial (top 5)

### 1. C1 — Rydberg static-CFT connected-correlator (Product 80)

**Connects to:** the published alpha~=4 holographic stress-tensor force and the 2D
Ising-CFT correspondence (Zenodo 10.5281/zenodo.19661227, HYP-008 SUPPORTED).

**Physical system:** QuEra Aquila, 256-atom neutral-atom tweezer array via AWS
Braket. The atoms are prepared into the critical transverse-field-Ising / PXP
ground state by an adiabatic detuning (Delta) sweep -- exactly the Ebadi et al.
(Nature 595 227, arXiv:2012.12281) protocol that is already demonstrated hardware,
and which Sahay-Lukin-Cotler (arXiv:2401.13595) endorse for realizing the Ising
CFT on Rydberg arrays.

**CFT quantity measured:** the *equal-time* boundary two-point correlator of the
order parameter, `<Z_i Z_j>_c = <Z_i Z_j> - <Z_i><Z_j>`, extracted at the bitstring
level over separations dr = 1..6, then fit to dr^-alpha. The stress-tensor exchange
channel predicts the r^-4 envelope that the project has measured three times
numerically (3.92 / 3.97 / 4.07); SIM-2026-023 gives the chi=3 bootstrap reference
with acceptance window [3.2, 4.8].

**Killers explicitly avoided.** This is the entire point of the candidate, and it
is what HYP-017 got wrong:
- **R1 (hologron decay):** there is NO hologron and NO time evolution. The
  observable is a property of the *prepared static ground state*. Nothing has to
  survive a measurement window because nothing is propagating. R1 is structurally
  inapplicable.
- **R2 (single-site-density energy estimator):** the readout is the explicit
  connected correlator built from the full single-shot bitstring ensemble --
  `mean(z_i z_j) - mean(z_i) mean(z_j)` over shots -- which by construction
  retains the connected two-body piece R2 said was dropped. No product-of-single-
  site-densities proxy is used anywhere.
- **R3/R4 (single-basis TEE bias):** no topological entanglement entropy is
  computed. The observable is a two-point function, not a Renyi-2 / collision
  probability, so the upward TEE bias cannot occur.
- **Blockade-pathological reduced geometry:** the protocol uses the FULL native
  Aquila lattice at the published lattice constant (Ebadi-class spacing, ~5-6 um,
  with the |70S> blockade radius accounted for in the Delta-sweep), not a
  shrunken 15/20-atom replica. The reduced-geometry pathology that killed the
  local validators is not present because there is no replica.

**Feasibility / cost:** TESTABLE_NOW. AWS Braket Aquila ~ $0.01/task +
$0.0009/shot; ~5000 shots/setting x ~8 separation settings ~ $200-500. Classical
post-processing is a NumPy connected-correlator sweep on the returned bitstrings.

**Result yielded:** a *hardware* measurement of the alpha exponent on a second,
physically independent platform (neutral atoms vs the trapped-ion/MERA numerics).
If alpha in [3.2, 4.8] it is the project's first experimental confirmation of the
central published claim; if outside, it bounds platform-dependence of the
stress-tensor channel. Either way it produces a citable experimental data point
attached to the Zenodo record and is the cleanest available answer to "is alpha~=4
real or a numerical artifact?".

### 2. C2 — Passive transmission-line / LC-ladder MERA emulator (Product 80)

**Connects to:** alpha~=4 holographic force and the chi=3 MERA causal-cone geometry.

**Physical system:** a passive electrical ladder network -- a chain of LC sections
(or a tapered transmission line) whose per-section impedance is engineered so the
network Green function between port i and port j reproduces the MERA two-point
envelope. The MERA causal cone is a discrete hyperbolic tree; an impedance taper
that doubles section count per layer mimics the RG rescaling. This is the
analog-gravity tradition (Unruh acoustic metric; Carusotto-Rousseaux
transmission-line analogs) applied to the project specific r^-4 prediction rather
than to a generic horizon.

**CFT quantity measured:** the small-signal transfer function |G(dr)| measured
with a vector network analyzer between taps separated by dr ladder sections, fit
to dr^-alpha. Because the ladder is cheap and scalable it delivers the finite-size
alpha trend at N = 32, 48, 64 sections, beyond the N=16/24 statevector ceiling.

**Killers avoided:** ALL, by construction. No quantum state, no quasiparticle, no
time-domain decay (R1 N/A); the observable is a linear transfer function, not an
energy proxy (R2 N/A); no entropy/TEE (R3/R4 N/A); no atom array so no blockade
geometry.

**Feasibility / cost:** intermediate DIY. SMD L/C ladder on protoboard or tapered
microstrip; NanoVNA-class USB VNA (~$100). BOM ~$200-400. Hard part is designing
the impedance taper mapping to the chi=3 MERA (Cauer/continued-fraction network
synthesis) -- tractable circuit synthesis, not new physics.

**Result yielded:** independent non-quantum confirmation that the r^-4 envelope is
a structural consequence of the MERA causal-cone geometry, plus a finite-size
alpha(N) curve beyond the published runs. Caveat: a classical ladder tests only
the kinematic/geometric origin of alpha, not the entanglement interpretation --
complement to, not substitute for, C1.

### 3. C3 — Coupled-resonator hyperbolic-lattice transport analog (Product 64)

**Connects to:** the T=(pi/2)*l_AdS holographic transport result (HYP-006
SUPPORTED, 0.72% at N=16).

**Physical system:** coupled mechanical or electrical resonators on a finite
hyperbolic ({7,3} or {8,3}) tiling -- the hyperbolic-lattice circuit-QED /
coupled-resonator platform family. A wave packet is launched at one boundary site
and timed at the antipodal boundary site.

**CFT quantity measured:** boundary-to-antipodal transport time vs network
depth/curvature, compared to the geodesic prediction T=(pi/2)*l_AdS.

**Killers avoided:** ALL. Classical wave network: arrival time (not survival) is
the observable so R1 is N/A; no energy-proxy estimator (R2 N/A); no TEE (R3/R4
N/A); no Rydberg blockade geometry.

**Feasibility / cost:** advanced DIY / small-lab. A 30-50 node electrical
hyperbolic lattice is ~$1-3k and a few weeks fab. Higher build risk than C1/C2 (B=4).

**Result yielded:** tabletop demonstration that the (pi/2)*l_AdS transport law is a
geometric property of a hyperbolic wave network, grounding the project second
headline result outside simulation. Same caveat as C2: geometry, not entanglement.

### 4. C4 — Cheap classical-compute chi=3 MERA finite-size alpha at N=32,48 (Product 60)

**Connects to:** alpha~=4 force; chi=3 MERA.

**Physical system:** none -- a compute bridge, included because the framing invites
a cheap classical emulation testing alpha~=4 finite-size scaling at N the
published runs did not reach. Exact runs stop at N=24 (dense-statevector ceiling).
A chi=3 MERA contracted as a tensor network (never a dense vector) reaches N=32,48
on local GPU.

**CFT quantity measured:** the connected boundary correlator <Z_iZ_j>_c from the
contracted MERA, fit to dr^-alpha vs N -- testing whether alpha converges to 4 or
drifts with size (a finite-size systematic the paper cannot currently exclude).

**Killers avoided:** ALL. The connected-correlator back-end already exists and is
observable-agnostic (HYP-025 feasibility note on sim2026015d_chi3_16q_force.py);
explicit connected correlator, not R2 product-of-densities; no TEE (R3/R4 N/A); no
hardware so R1/blockade N/A.

**Feasibility / cost:** TESTABLE_NOW, zero marginal cost (local GPU, hours). New
code only the larger-N contraction front-end; back-end reused.

**Result yielded:** closes the finite-size-systematic gap in the published alpha
claim cheaply and immediately. Lower novelty (extends rather than physically
grounds) but high buildability and a useful robustness check for SciPost review.

### 5. C5 — DIY NV/SPAD g2 witness for a wave-optics holographic-transport rig (Product 27)

**Connects to:** the T=(pi/2)*l_AdS transport result.

**Physical system:** a tabletop wave-optics analog -- a GRIN or multi-segment
light-pipe whose eikonal transport reproduces the hyperbolic-geodesic transit
time -- read out with a DIY SPAD/NV photon-counting front-end from the cataloged
toolbox (DIY-SENSOR-SURVEY 2026-05; UncutGem-class hardware ~$100-200).

**CFT quantity measured:** an intensity-correlation (g2) timed-transport analog of
the antipodal transport time.

**Killers avoided:** ALL (classical optics + classical photon counting).

**Feasibility / cost:** intermediate-to-advanced DIY, ~$300-600, but the mapping
from a GRIN light-pipe to the specific (pi/2)*l_AdS constant is loose -- it
reproduces hyperbolic transport qualitatively but pinning the 0.72%-level constant
optically is hard (U=3).

**Result yielded:** at best a qualitative public-facing demonstration; weak as a
quantitative test, strong only as outreach. Included because the framing asked
about the DIY toolbox, but dominated by C1/C2/C3 for any quantitative purpose.

## Summary

Top 3 actionable bridges, all structurally avoiding every HYP-017 killer:
1. **C1 Rydberg static connected-correlator on Aquila** (80) -- only candidate
   yielding a hardware test of the published alpha~=4 on a second physical
   platform, ~$200-500, R1 inapplicable (static prepared ground state, no
   propagating hologron), R2 fixed by explicit bitstring connected-correlator.
2. **C2 Passive LC-ladder MERA emulator** (80) -- cheapest, lowest-risk,
   classically tests the r^-4 scaling law and reaches N beyond the published
   ceiling; complements but cannot replace C1 (geometry, not entanglement).
3. **C3 Coupled-resonator hyperbolic transport analog** (64) -- tabletop physical
   grounding of the (pi/2)*l_AdS transport headline.

C1 and C2 tie at 80; C1 is the recommended lead (produces an experimental result
attachable to the Zenodo record); C2 is the recommended low-cost parallel hedge.
