# REDTEAM — QCHEM-COMBO-C (Devil's Advocate, 2026-05-17)

Brutal test applied to each top-5: **does this beat doing the chemistry on a classical
laptop, and is the hardware genuinely simulating the target chemistry rather than a
tenuous analogy?**

Source under review: `research/data/papers/QCHEM-COMBO-C-hardware.md`

---

## TL;DR verdict

- **Only #1 (DIY EFNMR ¹H–³¹P J-coupling) survives the brutal test** — and *only*
  because it is an experimental measurement, not a hardware simulation, so "beats a
  laptop" is category-correct (a laptop can't produce an experimental J). But its
  **novelty is overstated**: it is a faithful reproduction of Appelt 2006 / Barskiy 2021
  organophosphate ZULF J-spectroscopy on a cheap rig. Strike "no precedent at this price
  point." Re-score 60 → **40** (N 3→2).
- **#3 (Rydberg blockade exchange cluster) is the one to kill** → move to Tier X. Aquila
  delivers Ising, not Heisenberg exchange; matching a singlet–triplet gap is the
  project's exact "number-match ≠ mechanism" / HYP-017 trap. 24 → **4**.
- **#2 down-score 36 → 12**: 2-site Hubbard is laptop-trivial (closed-form), the
  "TM-dimer" framing is an analogy, cost ~3–5× optimistic. Hardware-shakedown only.
- **#4 (16) and #5 (12) fair / could go lower** — both already correctly self-rejected.
- **Does anything beat a laptop? Only #1, and only as a measurement.** Every
  Aquila/IBM candidate loses to exact diagonalization on a laptop.

---

## #1 — DIY EF-NMR / NV-NMR field-independent J-coupling spectrometer

**Brutal-test result: SURVIVES the laptop test, but the novelty claim (N=3) is
overstated and should be cut to N=1–2. The "no located precedent at this price point /
framed as electronic-structure probe" claim is false.**

### Killer objection: this is textbook ZULF / EFNMR J-spectroscopy, not a novel combination

The editorial frames the novelty as "the *specific combination* of a sub-$500 DIY EF-NMR
rig used deliberately as an electronic-structure probe (J → s-character), framed as a
chemistry deliverable" with "no located precedent at this price point." Every clause of
that is contradicted by mainstream prior art the editorial itself half-cites:

1. **"Pure J-coupling spectroscopy" IS the established name for this entire
   subfield.** Zero-field NMR spectra are "entirely determined by J-couplings between
   nuclei and hence referred to as *pure J-coupling spectroscopy*"
   (en.wikipedia.org/wiki/Zero_field_NMR; Blanchard & Budker review,
   ScienceDirect S2667325820300157). The interpretation of J as an
   electron-mediated, Fermi-contact, s-character bonding observable is the *textbook
   motivation* for the field, not a new framing — it is in every ZULF review (Pines/
   Weitekamp 1983 origin; Ledbetter/Budker; Blanchard).

2. **The exact proposed target — heteronuclear `¹H–³¹P` J-coupling in a phosphate /
   organophosphorus compound, read as a bonding observable — is published.** Barskiy,
   Blanchard, Budker et al., *"Zero-Field NMR J-Spectroscopy of Organophosphorus
   Compounds,"* J. Phys. Chem. Lett. 2021 (https://pubs.acs.org/doi/10.1021/acs.jpclett.0c03532)
   does precisely this on dichlorvos and related phosphates, resolving `³¹P–¹H` multi-bond
   J. Earth's-field detection of organophosphate (nerve-agent surrogate) `³¹P–¹H` J was
   published in *Applied Magnetic Resonance* 2023
   (https://link.springer.com/article/10.1007/s00723-023-01565-4). Appelt, Häsing,
   Blümich et al., *Nature Physics* 2 (2006) 105 (https://www.nature.com/articles/nphys211)
   measured heteronuclear `¹H–¹⁹F` and `¹H–³¹P` J in Earth's field to **mHz precision**
   two decades ago and explicitly interpreted it as molecular-structure analysis. The
   candidate's "trimethyl phosphate / fluorophosphate, J → hybridization" deliverable is
   a re-run of Appelt 2006 + Barskiy 2021.

3. **The "sub-$500 DIY rig used as a J spectrometer" is also published, and the
   project's own catalog points at it.** A peer-reviewed low-cost EFNMR design
   "enables detection of 10-Hz splitting of the proton spectrum due to scalar coupling
   to a `³¹P` nucleus" with "1 Hz resolution… even in grossly inhomogeneous fields"
   (low-cost EFNMR spectrometer, ResearchGate 230972230; "Inexpensive Earth Field NMR
   Spectrometer with Improved Shimming," PubMed 35381158; DIY builds <$130, Hackaday
   project 21703; Trevelyan, *MRI and NMR Spectroscopy in the Earth's Field*, 2019).
   The pyppm / RowleyLab rigs in the project's own DIY-SENSOR-SURVEY are these designs.
   So the price-point novelty claim is refuted by the same survey it cites.

**Conclusion on novelty:** N should drop to **1–2**. There is no new combination here —
it is standard EFNMR/ZULF J-spectroscopy of an organophosphate, a 2006–2021 result,
on the standard cheap rig.

### Does the cheap rig actually resolve the J-splitting? — YES (this is the saving grace)

This is the one place the editorial is *right* and conservative. Independent sources
confirm a hobby-grade EFNMR rig genuinely resolves heteronuclear J:
- 1 Hz spectral resolution achievable even in inhomogeneous Earth field; 10-Hz `¹H–³¹P`
  splitting explicitly demonstrated on a low-cost build (ResearchGate 230972230).
- Prepolarization (a permanent/electromagnet mT coil) is mandatory and is the genuine
  load-bearing component — consistent with the editorial's honest S1 caveat. Sample
  volume ~100–125 mL, proton Larmor ~1.6–2.6 kHz, mains-hum rejection required
  (PMC7538153; chemospec.org DIY-NMR 2023). Realistic all-in cost with prepolarizer
  ~$400–700, as the editorial states.

So the **mechanism is genuinely faithful (Mech = 5 stands): the detected spins are
literally the molecule's nuclei; there is zero analogy gap.** And it **beats a laptop
in the only sense that matters**: a laptop cannot produce an *experimental* J value —
it can only predict one (DFT/CCSD `³¹P–¹H` spin–spin coupling is itself a hard,
error-prone DFT property, so an experimental number is independently valuable).

### Net: keep as #1, but for the right reason, and re-scored

It survives the brutal test because it is a *measurement*, not a simulation — the laptop
comparison is category-correct only here. But it is **not novel**; it is a faithful
reproduction of a well-known experiment on cheap hardware. Honest score:
**N=2, B=5, U=4, Mech=5 → 40** (was 60). Still the top candidate by a wide margin once
the others are stress-tested below — but the editorial's "no precedent" sentence must be
struck and replaced with "reproduction of Appelt 2006 / Barskiy 2021 on a DIY rig;
value is pedagogical + an independent experimental datum, not discovery."

## #2 — Auxiliary-spin-solver Fermi–Hubbard on Aquila

**Brutal-test result: FAILS the laptop test outright. Down-score U to 1–2. The "novel
combination" is thin and the cost numbers are optimistic by a large factor.**

### Killer objection: the deliverable is trivially classical AND the "molecule" is an analogy

The editorial already concedes "a 2-site Hubbard model is *trivially* exact on a laptop"
and holds U=3 anyway on a "method-demonstration" exemption. Apply the rubric honestly:
the rubric says **classical-beats-it ⇒ U≤2**. A 2-site/2-band Hubbard dimer is not just
laptop-tractable — it is an analytically closed problem (the Hubbard dimer has a
closed-form ground state; it is a standard pedagogical exercise, e.g. Carrascal et al.,
*"The Hubbard dimer: a density functional case study,"* dft.uci.edu/pubs/CFSB15.pdf).
Exact diagonalization of any <20-orbital Hubbard cluster is microseconds on a laptop.
By the project's own rule U must be **≤2**, not 3. The "method demonstration" carve-out
is exactly the kind of exemption the project's "number-match ≠ mechanism" lesson exists
to forbid: it lets a result that no one wants score as useful.

Second blade — the molecular faithfulness (Mech=4) is also too generous. The
spin sector of the auxiliary-spin solver *is* genuinely the Hubbard impurity (this part
is honest). But the editorial then maps "2-site Hubbard dimer" → "correlated TM dimer
(Cu–Cu / Fe–Fe magnetic core)." A real Cu₂ or Fe₂ coordination core is a
multi-orbital, ligand-bridged, spin–orbit-coupled system; a single-band 2-site Hubbard
dimer captures essentially none of its actual coordination chemistry. That is the
project's canonical failure mode — matching a Mott-gap number from a 2-site toy and
calling it a "molecular TM-dimer calculation" is precisely a number-match dressed as a
mechanism. Mech for the *chemistry claim* is **2**, not 4 (the Hubbard physics is
faithful; the *molecular* identification is the analogy).

### The cost / shot numbers are optimistic

The published method (arXiv:2510.05897, Pasqal, Oct 2025;
https://arxiv.org/abs/2510.05897) uses a **36-qubit** Rydberg simulator (Orion Alpha)
in a *self-consistent iterative* loop for the equilibrium Mott transition — not a
handful of tasks. Each self-consistency iteration requires re-preparing the analog
spin state and re-reading occupation statistics; mapping a Mott-transition sweep needs
many interaction points × many self-consistency iterations × shots. The editorial's
"20–60 tasks (~$60–180)" assumes ~1 task per iteration and convergence in tens of
iterations with 1000 shots resolving the spin response. With Aquila's hard **1000-shot
cap** and **z-basis-only** readout, statistical resolution of the impurity response per
iteration is ~1/√1000 ≈ 3% — likely too coarse for clean self-consistency convergence,
forcing iteration re-runs and pushing realistic cost well above the stated band
($0.30/task + $0.01/shot × 1000 = $10.30/task; 60 tasks ≈ $618, not $180; and a Mott
sweep is multiple such loops). The cost estimate is low by roughly 3–5×, and that is
before noise-driven non-convergence on real hardware. B=3 is fair only if "buildable"
ignores whether it converges; as a result-producing run it is closer to B=2.

### Net: down-score

This is the most *mechanism-honest quantum-hardware* candidate (the spin sector really
is the Hubbard impurity) — that much of the editorial is correct and worth preserving.
But it **does not beat a laptop**, the molecular framing is an analogy, and the budget is
optimistic. Honest score: **N=3, B=2, U=2, Mech=2 (chemistry) → 12** (was 36). Keep only
as a *hardware-method shakedown*, never as a chemistry deliverable. It is strictly
dominated by #1 on the brutal test.

## #3 — Rydberg blockade-graph frustrated-exchange cluster

**Brutal-test result: FAILS both halves. The mapping is the project's exact
"Ising ≠ Heisenberg" failure mode, and the target is a laptop afternoon. Kill or
deep-down-score.**

### Killer objection: Aquila gives Ising, not Heisenberg exchange — this is the HYP-017 lesson, verbatim

A polynuclear Cu/Fe magnetic cluster's singlet–triplet gap is set by **isotropic
Heisenberg exchange** `J Sᵢ·Sⱼ` (a full `XXX`/`XXZ` spin-flip term). Aquila's
analog Hamiltonian is the **Rydberg-blockade Ising model**: a diagonal van-der-Waals
`nᵢnⱼ` density–density interaction plus a transverse drive — there is no native
`Sᵢ⁺Sⱼ⁻` exchange. Realizing a genuine Heisenberg/`XXZ` magnet on Rydberg hardware
requires *two* Rydberg states coupled through pair states to engineer the spin-exchange
term (Heidelberg dissertation, archiv.ub.uni-heidelberg.de/.../31511; "extremely
anisotropic Heisenberg magnet in Rydberg arrays," ResearchGate 372247956; Nature
s41586-021-03585-1, s41586-023-05859-2). **Aquila exposes none of that** — it is the
single-Rydberg-state blockade Ising machine with z-basis readout only
(arXiv:2306.11727). So reproducing a Cu₄/Fe₃ singlet–triplet gap on Aquila is, by
construction, the project's canonical pathology: matching a *number* with a Hamiltonian
that does **not contain the target's mechanism** (Heisenberg exchange). The editorial's
Mech=4 is too charitable — it is **Mech=2 at best**; this is the HYP-017 "wrong operator"
lesson restated.

### Laptop test: lost outright

The editorial concedes "exact diagonalization of a <20-spin cluster is a laptop
afternoon." Cu₄/Fe₃ Heisenberg clusters are routinely solved exactly classically; the
singlet–triplet gap of such clusters is a standard inorganic-magnetochemistry
calculation. U must be **≤2 by the rubric**, and given the Mech failure the result is
not even a faithful hardware demonstration. Honest score:
**N=2, B=3, U=1, Mech=2 → 4** (was 24). Recommendation: **move to Tier X (rejected)**.
It is the cleanest example in the list of the exact analogy trap the project exists to
catch.

## #4 — Classical shadows + symmetry-projected 2–4q on IBM free tier

**Brutal-test result: the editorial already self-immolates this one correctly. Confirmed
FAIL; no rescue. Scoring is fair.**

### Killer objection: the editorial's own verdict is right and well-sourced

This is the textbook walked-back result. Lee, Lee, Zhai, Chan et al.,
*"Evaluating the evidence for exponential quantum advantage in ground-state quantum
chemistry,"* Nature Communications 14, 1952 (2023)
(https://www.nature.com/articles/s41467-023-37587-6; arXiv:2208.02199) concludes
"evidence for such an exponential advantage across chemical space has yet to be found"
and that one should "assume exponential speedups are not generically available." H₂ and
HeH⁺ are solved to machine precision in microseconds on a laptop (full CI in a minimal
basis is a 4×4 / small matrix). The candidate produces a *worse, noisier* answer than a
laptop, more slowly, using a scarce 10-min QPU allotment. U=2 by rule; N=2 (every
component is published and reproduced hundreds of times — classical shadows
arXiv:2002.08953, group-theoretic mitigation Nature s41534-024-00854-5). It does **not**
beat a laptop in any sense and is not a chemistry result. The editorial correctly keeps
it only as a documented "hardware-shakedown." No revision needed; **score 16 stands**,
and it should never be presented as a chemistry deliverable.

## #5 — Analog Rydberg vibronic / conical-intersection emulator

**Brutal-test result: the editorial's Mech=2 kill is correct and if anything generous.
Confirmed FAIL for Aquila. Scoring fair; could go lower.**

### Killer objection: no phonon bus on Aquila → it is an analogy by construction

A vibronic conical intersection requires an electronic two-level system **coupled to
quantized vibrational (phonon) modes** with a geometric (Berry) phase. The faithful
hardware precedents are trapped-ion: Valahu et al., *Nature Chemistry* 15, 1503 (2023),
and trapped Rydberg-ion CI (arXiv:2512.04941) — both exploit the ion's *motional modes*
as the phonon bus and use rotated readout. **Aquila has only atomic positions and
blockade Ising interactions; there is no engineered vibrational mode and no
non-z-basis readout.** Encoding a pyrazine-like S₁/S₂ CI on Aquila would map the
phonon onto … nothing available — it is a pure analogy, the precise failure the project
lesson forbids. The editorial's Mech=2 is correct; arguably Mech=1 (there is no
mechanism at all on Aquila, only a hand-wave). It does not beat a laptop either: model
2-mode vibronic CI dynamics (e.g. 2-mode pyrazine LVC model) is a small,
well-established **classical** wavepacket / MCTDH calculation. **Score 12 stands (or
lower to N=3·B=2·U=1·Mech=1 = 6).** Correctly documented as not-for-Aquila.

---

## Scorecard revision (devil's-advocate)

| Rank | Candidate | Original (N·B·U·Mech=P) | Red-team (N·B·U·Mech=P) | Verdict |
|---|---|---|---|---|
| 1 | DIY EF-NMR/NV J-coupling | 3·5·4·5 = **60** | 2·5·4·5 = **40** | **SURVIVES** — only one that beats a laptop (it's a *measurement*); but NOT novel (Appelt 2006 / Barskiy 2021). Strike "no precedent." |
| 2 | Auxiliary-spin Hubbard / Aquila | 4·3·3·4 = **36** | 3·2·2·2 = **12** | **DOWN-SCORE** — laptop-trivial, molecular framing is analogy, cost ~3–5× low. Hardware-shakedown only. |
| 3 | Rydberg blockade exchange cluster | 3·3·2·4 = **24** | 2·3·1·2 = **4** | **KILL → Tier X** — Ising≠Heisenberg = the HYP-017 trap, verbatim. |
| 4 | Classical shadows H₂/HeH⁺ / IBM | 2·4·2·4 = **16** | 2·4·2·4 = **16** | **Fair as-is** — editorial self-killed correctly (Lee/Chan 2023). Not a chemistry result. |
| 5 | Rydberg vibronic CI / Aquila | 3·2·2·2 = **12** | 3·2·1·1 = **6** | **Fair / lower** — no phonon bus on Aquila; analogy by construction. |

### Which survive / which to down-score
- **Survives the brutal test: only #1**, and only because it is an experimental
  *measurement*, not a hardware *simulation* — the laptop comparison is category-correct
  there alone. Its novelty must be cut hard (N 3→2; "no precedent at this price point"
  is false — strike it).
- **Down-score: #2 (36→12), #3 (24→4, move to Tier X), #5 (12→6).**
- **#4 unchanged** — it was already correctly self-rejected.

### The single most defensible candidate
**#1, the DIY EFNMR `¹H–³¹P` J-coupling measurement**, re-framed honestly as: *a
faithful, end-to-end reproduction of Appelt-2006 / Barskiy-2021 organophosphate
J-spectroscopy on a sub-$700 DIY rig, delivering an independent experimental J value
and a pedagogical electronic-structure (s-character) readout.* Its strength is that it
is the **only candidate where "hardware genuinely simulates the chemistry" is trivially
true — because there is no simulation: the detected spins ARE the molecule's nuclei.**

### Does any candidate genuinely beat a classical laptop?
**Yes — only #1, and only in the strict sense that a laptop cannot produce an
*experimental* observable.** A laptop *predicts* `³¹P–¹H` J (an error-prone DFT/CCSD
spin–spin-coupling property); the rig *measures* it, so the two are not in competition —
that is why #1 is the only honest survivor. **Every Aquila/IBM candidate (#2–#5) loses
to a laptop outright**: their targets (2-site Hubbard dimer, <20-spin Heisenberg
cluster, H₂/HeH⁺, 2-mode vibronic CI) are all closed-form or microsecond exact-diagonal
problems classically, and the hardware mappings are either analogies (#3, #5),
laptop-trivial method demos (#2), or known-walked-back NISQ chemistry (#4). No
quantum-hardware candidate in this list beats a laptop or faithfully contains its target
chemistry's mechanism — consistent with Lee/Chan 2023 and the project's own
"number-match ≠ mechanism" standing lesson.

## Sources

- Zero/ultralow-field NMR = "pure J-coupling spectroscopy": https://en.wikipedia.org/wiki/Zero_field_NMR ; Blanchard & Budker review https://www.sciencedirect.com/science/article/pii/S2667325820300157
- ZULF J-spectroscopy of organophosphorus compounds (dichlorvos, ³¹P–¹H): Barskiy/Blanchard/Budker, J. Phys. Chem. Lett. 2021 — https://pubs.acs.org/doi/10.1021/acs.jpclett.0c03532
- Earth's-field NMR organophosphate / nerve-agent ³¹P–¹H J: Applied Magnetic Resonance 2023 — https://link.springer.com/article/10.1007/s00723-023-01565-4
- Heteronuclear ¹H–¹⁹F / ¹H–³¹P J in Earth's field to mHz, framed as structure analysis: Appelt et al., Nature Physics 2 (2006) 105 — https://www.nature.com/articles/nphys211
- Low-cost DIY EFNMR resolves 10-Hz ¹H–³¹P scalar splitting, 1 Hz resolution: https://www.researchgate.net/publication/230972230 ; "Inexpensive Earth Field NMR Spectrometer with Improved Shimming" PubMed 35381158 ; DIY <$130 Hackaday project/21703 ; chemospec.org/posts/2023-06-12-DIY-NMR ; Trevelyan, *MRI and NMR Spectroscopy in the Earth's Field* (2019)
- Low-field NMR instrumentation review (prepolarization, SNR, sample volume): PMC7538153
- Auxiliary-spin-solver Fermi–Hubbard, 36-qubit Rydberg, self-consistent loop: Pasqal arXiv:2510.05897 — https://arxiv.org/abs/2510.05897
- Hubbard dimer is closed-form / pedagogical: Carrascal et al. — https://dft.uci.edu/pubs/CFSB15.pdf
- Rydberg blockade = Ising; Heisenberg/XXZ needs engineered two-Rydberg-state exchange: Heidelberg diss. archiv.ub.uni-heidelberg.de/volltextserver/31511 ; ResearchGate 372247956 ; Nature s41586-021-03585-1 ; Nature s41586-023-05859-2
- Aquila analog Rydberg / z-basis-only readout: arXiv:2306.11727 — https://arxiv.org/abs/2306.11727
- No exponential quantum advantage in ground-state chemistry: Lee, Lee, Zhai, Chan et al., Nature Communications 14, 1952 (2023) — https://www.nature.com/articles/s41467-023-37587-6 ; arXiv:2208.02199
- Classical shadows + group-theoretic mitigation: https://www.nature.com/articles/s41534-024-00854-5 ; classical shadows arXiv:2002.08953
- Trapped-ion conical-intersection analog (faithful precedent, needs phonon bus): Valahu et al., Nature Chemistry 15, 1503 (2023) ; trapped Rydberg-ion CI arXiv:2512.04941
