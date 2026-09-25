# QCHEM-COMBO-C — Hardware-Faithful Quantum-Chemistry Combination Hunt (2026-05-17)

Framing QC-C. Goal: novel COMBINATIONS that yield a runnable quantum-chemistry result on
free/cheap cloud quantum hardware (QuEra Aquila / IBM free tier), a laptop, or cataloged DIY
instruments (NV magnetometer, Rydberg vapor cell, EF-NMR). Brutally honest on classical
competitiveness. VQE chemistry "advantage" skepticism baked in.

Hardware ground truth carried from prior run:
- Real QuEra Aquila: $0.01/shot, $0.30/task, 1000-shot/task cap, **z-basis (Rydberg occupation)
  readout ONLY** — no rotated/Pauli-X/Y measurement. Analog Rydberg Hamiltonian only.
- IBM Quantum free tier (Open plan): ~10 min/month QPU, Heron r2 ~133q, gate-based, arbitrary
  basis rotation, but deep circuits noise-limited at depth.
- Laptop: exact diagonalization to ~16–20 spin-orbitals; DMRG/coupled-cluster far beyond that.
- DIY instruments on hand / designed: UncutGem-class NV magnetometer (~$100–200), EF-NMR rigs
  (pyppm / RowleyLab, ~$300–500), Rydberg EIT electrometer (BUILD-A, ~$4.3k, not yet built).

SCORING: N=novelty, B=buildability (5 = runnable this month <$300 / on a laptop),
U=usefulness (5 = result actually wanted AND not trivially beaten by classical;
classical-beats-it ⇒ U≤2), Mech=mechanism-faithful (5 = hardware genuinely simulates the
target chemistry; 1 = tenuous exponent/analogy). Product = N·B·U.

---

## Ranked table

| Rank | Combination | System + property | Hardware | N | B | U | Mech | Product |
|---|---|---|---|---|---|---|---|---|
| 1 | DIY EF-NMR / NV-NMR run as a **field-independent heteronuclear J-coupling spectrometer** + classical spin-Hamiltonian fit to extract a bond-electronic-structure observable (J = Fermi-contact ∝ s-character) | Trimethyl phosphate / fluorophosphate: ¹H–³¹P or ¹⁹F–³¹P J-coupling (Hz); reports through-bond electron-mediated coupling, a genuine electronic-structure quantity | RowleyLab / pyppm EF-NMR rig (~$300–500) OR UncutGem-class NV at mm standoff | 3 | 5 | 4 | 5 | **60** |
| 2 | **Auxiliary-spin-solver Fermi–Hubbard**: classical free-fermion self-consistency loop + analog Rydberg z-basis density readout supplies the interacting-spin impurity response (Pasqal 2510.05897 mapping, ported to Aquila) | 2-band/2-site Hubbard proxy for a correlated TM dimer (Mott gap, double occupancy) | QuEra Aquila via AWS Braket (~$60–180, z-basis only — native to this scheme) | 4 | 3 | 3 | 4 | **36** |
| 3 | Analog Rydberg blockade-graph encoding of a **frustrated antiferromagnetic exchange (Heisenberg-J) cluster** + classical Lanczos extrapolation for the singlet–triplet gap | Polynuclear Cu/Fe magnetic cluster spin-gap (a real coordination-chemistry quantity) | QuEra Aquila (~$60–120) | 3 | 3 | 2 | 4 | **24** |
| 4 | Classical shadows on a 2–4-qubit symmetry-projected ansatz + group-theoretic error mitigation, single small IBM circuit | H₂ / HeH⁺ dissociation curve, ground-state energy to chemical accuracy | IBM Heron free tier (~10 min QPU) | 2 | 4 | 2 | 4 | **16** |
| 5 | Analog Rydberg tweezer **vibronic / conical-intersection** emulator (electronic 2-level ⊗ phonon) + classical envelope reconstruction of the geometric-phase observable | Model 2-mode pyrazine-like S₁/S₂ conical intersection: diabatic population transfer rate | Aquila (positions only, no phonon bus — see Mech caveat) | 3 | 2 | 2 | 2 | **12** |
| 6 | NV magnetometer reading bulk para-H₂-hyperpolarized sample → reaction-monitoring of a catalytic hydrogenation (rate constant, not structure) | Para-H₂ hydrogenation of a small alkene; turnover via ¹H signal enhancement | DIY NV + pHIP generator (~$400 + chemistry) | 3 | 2 | 3 | 4 | **18** |

---

## Editorial — top 5

### #1 — EF-NMR / NV-NMR as a field-independent J-coupling spectrometer (N3·B5·U4·Mech5 = 60)

This is the one candidate that is *both* runnable this month *and* produces a chemistry result a
laptop cannot trivially manufacture, because the result is a **measurement of a real molecule**,
not a simulation of one. The crucial physics, surfaced in prior art: at Earth/low field the
Larmor frequency is ~2 kHz and chemical shifts are sub-mHz — **chemical shift is dead at low
field** (sciencedirect.com S1090780712001577; nanalysis blog). But **heteronuclear
scalar J-coupling is field-independent** and is fully resolvable even at Earth field
(ScienceDirect "Earth's Field Spectroscopy"; PubMed 22595293). The J-coupling of, e.g., ¹H–³¹P
in trimethyl phosphate (~10–15 Hz) or ¹⁹F–³¹P in a fluorophosphate is a *bona fide
electronic-structure observable*: J is dominated by the Fermi-contact term, which is
proportional to the s-electron density at both nuclei and the bond's s-character — it directly
probes the molecular wavefunction at the nuclei. The "combination" is the instrument (DIY
EF-NMR rig: RowleyLab or pyppm, ~$300–500, in the catalogued survey) + a classical
spin-Hamiltonian least-squares fit that turns the FID multiplet into J in Hz and then into a
hybridization statement. **Why novel:** nano/microscale NV-NMR has resolved J-couplings in
picoliter volumes (Glenn et al.), and EF-NMR J-spectroscopy is known — but the *specific
combination* of a sub-$500 DIY EF-NMR rig used deliberately as an electronic-structure probe
(J → s-character), framed as a chemistry deliverable rather than a physics demo, has no located
precedent at this price point. **Hardest obstacle:** SNR on a hobby rig — needs prepolarization
(a permanent magnet, exactly the S1 load-bearing component from the prior run) and mains-hum
rejection at the 2 kHz Larmor line; realistic cost ~$400–700 incl. prepolarizer. **What you
actually get:** J to ±0.5–1 Hz on a known compound — *not* competitive with a $30k benchtop
NMR for throughput, but the point is it is a real, validated, end-to-end DIY quantum-sensor
chemistry measurement; a laptop cannot produce an experimental J-coupling. Mechanism-faithful
= 5: the NV/proton spins literally are the molecule's nuclear spins; there is no analogy gap.

### #2 — Auxiliary-spin-solver Fermi–Hubbard on Aquila (N4·B3·U3·Mech4 = 36)

The most mechanism-honest *quantum-hardware* candidate. Pasqal's Oct-2025 method
(arXiv:2510.05897) is purpose-built for exactly Aquila's limitation: it never encodes fermions
on qubits. It splits a 2D Fermi–Hubbard model into a classically-tractable free-fermion piece
and an interacting-spin impurity piece, and the spin piece is *natively* an Ising/XY Rydberg
Hamiltonian read out in the **occupation (z) basis** — precisely and only what Aquila offers.
A 2-site/2-band Hubbard dimer is a defensible minimal proxy for a correlated transition-metal
pair (e.g. a Cu–Cu or Fe–Fe magnetic core), and the observable (double occupancy / Mott gap)
is a real correlated-chemistry quantity. **Why novel:** the published demonstrations target
condensed-matter Hubbard physics; reframing the same auxiliary-spin loop as a *molecular*
TM-dimer correlation calculation, and actually executing it on the free/cheap Aquila tier under
the 1000-shot cap, is the novel combination. **Hardest obstacle:** the self-consistency loop
needs many Aquila tasks (each $0.30 + shots), and the 1000-shot/task cap plus z-basis-only
readout limits how finely the spin response is resolved — convergence may need 20–60 tasks
(~$60–180). **Brutally honest:** a 2-site Hubbard model is *trivially* exact on a laptop;
USEFULNESS is held at 3 because the deliverable is a hardware-method demonstration (does the
auxiliary-spin loop converge on real Aquila noise?), not a chemistry number anyone wants — at
this size classical wins outright. Mech = 4 (the spin sector is genuinely the Hubbard impurity,
but the "molecule" is a coarse proxy).

### #3 — Rydberg blockade-graph frustrated-exchange cluster, singlet–triplet gap (N3·B3·U2·Mech4 = 24)

Map a small polynuclear magnetic coordination cluster's Heisenberg exchange network onto
Aquila's blockade graph (atom positions set Jᵢⱼ via the C₆/r⁶ tail), prepare the
adiabatic ground state, read z-basis correlators, and Lanczos-extrapolate the singlet–triplet
gap classically. The spin gap of a Cu₄ or Fe₃ cluster is a genuine inorganic-chemistry
observable. **Why novel:** Rydberg AFM ground states are standard physics demos; targeting a
named coordination cluster's magnetic gap as the deliverable is the new framing. **Honest
verdict:** the prior-run lesson bites here — Aquila gives you an Ising-like blockade
Hamiltonian, not the true Heisenberg exchange of the real complex; matching a gap is at risk of
being an *exponent/number coincidence* rather than a faithful mechanism (Mech held to 4, not 5,
and USEFULNESS to 2 because exact diagonalization of a <20-spin cluster is a laptop afternoon).
Keep as a fallback to #2, not a headline.

### #4 — Classical shadows + symmetry-projected 2–4q on IBM free tier (N2·B4·U2·Mech4 = 16)

Technically clean and genuinely runnable in the 10-min IBM free allotment: classical shadows
plus group-theoretic error mitigation (Nature npj QI s41534-024-00854-5) can pull H₂/HeH⁺
ground-state energy to chemical accuracy from a shallow circuit. **But this is the textbook
walked-back result**: Lee/Chan et al. (Nature Comms s41467-023-37587-6) found no exponential
advantage for ground-state chemistry, and a laptop reproduces H₂ to machine precision in
microseconds. Novelty ≈ 2 (every piece is published and widely reproduced); USEFULNESS = 2 by
the rubric's classical-beats-it rule. Included only to document that it was considered and is
*not* worth the project's time as a chemistry result — its only value is as a hardware
shakedown.

### #5 — Analog Rydberg vibronic / conical-intersection emulator (N3·B2·U2·Mech2 = 12)

Conceptually the most exciting (arXiv:2506.09865; trapped-ion precedent Valahu et al. Nature
Chemistry 2023 already *did* an analog conical-intersection simulation), but the
mechanism-faithful axis kills it for *Aquila specifically*: the proposals require a
**phonon/vibrational bus** coupled to the electronic levels. Aquila has only atomic positions
and Rydberg blockade — no engineered phonon mode, no rotated readout — so a pyrazine-like
vibronic CI cannot be faithfully encoded on the free/cheap platform (Mech = 2: it would be an
analogy, the exact failure mode the project lesson warns against). It is mechanism-faithful on
*trapped-ion* hardware, which is not in the free/cheap/DIY budget. Documented so it is not
re-proposed for Aquila.

---

## Tier X — considered and rejected

| Candidate | Killer |
|---|---|
| VQE for any molecule on IBM free tier | Walked back across the literature (Lee/Chan, Nature Comms 2023, s41467-023-37587-6). Measurement count prohibitive; classical (DMRG/CCSD(T)/AFQMC) and neural-net wavefunctions beat NISQ chemistry at every size that fits the free tier. USEFULNESS ≤ 2 by rule; not novel. |
| QuEra Aquila for molecular electronic-structure energy directly | Aquila is an analog Rydberg Hamiltonian with **z-basis readout only** (arXiv:2306.11727). It cannot represent a fermionic molecular Hamiltonian or measure off-diagonal terms. Any "molecular energy" from it is an analogy, not a mechanism (the project's HYP-017 lesson, verbatim). |
| NV-NMR for chemical-shift fingerprinting at low/Earth field | Physically forbidden: chemical shift dispersion is sub-mHz at ~2 kHz Larmor; needs ≳1 T (sciencedirect S1090780712001577). Only J-coupling (field-independent) survives — that is candidate #1, the salvage. |
| Rydberg vibronic conical-intersection on Aquila | No phonon bus on Aquila; faithful only on trapped-ion (Valahu Nature Chem 2023), outside free/cheap/DIY budget. Kept at #5 as documented-not-recommended. |
| DIY Rydberg EIT electrometer (BUILD-A) for chemistry | $4.3k and 16 weeks; measures RF E-fields, not a chemistry observable. No molecular path. Out of scope/budget. |

---
## Prior-art sources (WebSearch; arXiv MCP stale)

- Aquila platform / z-basis-only readout: arXiv:2306.11727 (https://arxiv.org/abs/2306.11727)
- Auxiliary-spin-solver Fermi–Hubbard on neutral atoms (Pasqal): arXiv:2510.05897 (https://arxiv.org/abs/2510.05897)
- Programmable molecules/materials w/ reconfigurable processors (Nature Phys 2025): arXiv:2312.02265 / https://www.nature.com/articles/s41567-024-02738-z
- Rydberg arrays as molecular-dynamics / vibronic simulators: arXiv:2506.09865 (https://arxiv.org/abs/2506.09865)
- Trapped-ion conical-intersection analog (precedent): Valahu et al., Nature Chemistry 2023; trapped Rydberg ion CI arXiv:2512.04941
- No exponential quantum advantage in ground-state chemistry: Lee/Chan et al., Nature Comms 2023 — https://www.nature.com/articles/s41467-023-37587-6
- Low-field chemical-shift impossibility / J-coupling field-independence: https://www.sciencedirect.com/science/article/abs/pii/S1090780712001577 ; PubMed 22595293 ; https://www.nanalysis.com/nmready-blog/2017/9/30/...
- Picoliter NV-NMR resolving J-couplings & chemical shift (Glenn et al.): https://pmc.ncbi.nlm.nih.gov/articles/PMC9301930/ ; arXiv:2205.12178
- Classical shadows + group-theoretic error mitigation: https://www.nature.com/articles/s41534-024-00854-5
- DIY instruments on hand: DIY-SENSOR-SURVEY-2026-05-NV-vapor.md (UncutGem, RowleyLab/pyppm EF-NMR), BUILD-A-rydberg-electrometer.md

*Methodology note: the project's standing lesson — "a power-law / number match is not a
mechanism" — was applied as the Mech axis. Every Aquila-based chemistry candidate was
pressure-tested for whether the Rydberg hardware *contains* the target chemistry's physics or
merely *reproduces a number*; #2 passes partially (it is literally the Hubbard impurity spin
sector), #3/#5 do not and are scored down accordingly.*
