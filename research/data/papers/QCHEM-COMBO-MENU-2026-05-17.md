# Quantum-Chemistry Novel-Method Hunt — Consolidated Menu (2026-05-17)

**Question asked:** novel-method hunt in quantum chemistry — same machinery as the
2026-05-16 novel-combinations run (3 generation framings + 6-agent deep-dive/red-team
second wave). Scoring: NOVELTY × BUILDABILITY × USEFULNESS, plus a MECHANISM-FAITHFUL
axis (added after the last run's lesson: *an exponent/curve match is not a mechanism*).

> **Headline: every wave-1 winner was knocked down again.** Quantum chemistry on
> near-term hardware is the most overclaim-prone field touched so far. The dominant
> failure mode here is **circularity** — the classical component already solves the
> chemistry, so the quantum/novel part adds nothing — closely followed by the
> project's own recurring **curve-fit-not-mechanism** trap. **Net result: there is no
> Tier-0 "build this" survivor. One candidate survives demoted as a validation artifact.**

---

## Tier 1 — Survives, but only demoted (a validation artifact, not a discovery)

### S1-QC. DIY Earth-field-NMR rig as a field-independent ¹H–³¹P J-coupling spectrometer
*(Framing C #1 — and it is the SAME instrument as S1 from the 2026-05-16 run, reused)*

- **What genuinely works:** at Earth's field, chemical shift is dead (sub-mHz at the
  2.13 kHz proton Larmor), but **scalar J-coupling is field-independent** and
  resolvable. Deep-dive confirmed the numbers: resolving a ~10 Hz heteronuclear J
  needs only Δν½ ≈ 3 Hz ⇒ **T2* ≳ 0.1 s**, which a pyppm/RowleyLab-class EF-NMR rig
  (~$360–780 with prepolarizer) clears with margin. It measures a real molecule and
  a real electronic-structure-related observable (Fermi-contact s-character via J).
- **Why it's demoted, not Tier-0:** the experiment is **already published on this
  exact hardware class** — Earth-field ¹H–³¹P J of trimethyl phosphate
  (Glover/Appelt, *J. Magn. Reson.* 200 (2009) 88); NV-detected ¹H–³¹P J of the same
  molecule (Glenn, *Nature* 555, 351 (2018)); ZULF organophosphorus J-spectroscopy
  is a mature subfield (Budker/Blanchard, Barskiy/Budker JPCL 2021). The measured J
  reproduces a textbook value laptop DFT predicts to ≲2 Hz for free. Both the
  deep-dive and red-team independently struck the novelty claim (N 3→2).
- **The honest pitch:** a closed validation loop — *DFT predicts → a $360–780 DIY
  quantum sensor measures → both agree with each other and the literature.* Useful as
  an instrument-validation / outreach artifact, **not** as a new chemistry result.
- **Scores:** N2 · B5 · U3 · Mech5 = **30** (down from rubric's 60). Below the prior
  run's true Tier-0 survivor (S1 NV+EF-NMR device, 48).
- **Recommended molecule:** dimethyl phosphite (¹J ≈ 690 Hz self-calibration line +
  ³J ≈ 10–12 Hz resolution test); fallback trimethyl phosphate. **Note:** the chemistry
  result should use the **coil-detected EF-NMR rig, not an NV** — a bare UncutGem NV is
  a strictly worse 2 kHz B-transducer than a tuned pickup coil.

---

## Tier 2 — Conceptually interesting, de-risk before any claim (not buildable now)

### S2-QC. Classical-shadow 2-RDM as the self-consistent descriptor in generalized DMET
*(Framing A #3 — the red-team's single most defensible method candidate)*

- The only method-combination with **genuine bidirectional feedback that is not
  circular**: the embedding genuinely needs the quantum 2-RDM (an HF projector bath
  fails for strong correlation / metallic cases). All located prior art is
  one-directional; closing the loop with a non-projector measured bath is the novel slice.
- **Killer is quantitative, not conceptual:** ~2.6×10⁸ shots per self-consistency
  iteration to hit the ~1e-3 precision DMET needs. Buildability honest at 2, not 3.
- **Scores (red-teamed):** N3 · B2 · U?  ≈ **24**. De-risk path: prove the loop on an
  FCI-emulated 2-RDM with injected O(1/√M) noise *before* any hardware claim.

### S3-QC. Near-FCI NQS as a locally-biased-shadow bias oracle for shallow-VQE readout
*(Framing A #1 — the flashy 64 winner; survives only in a narrow niche)*

- **Mostly circular and mostly not novel.** The "10–100× fewer shots" is dominated by
  the 4ᵏ LBCS weight prefactor a better prior does not touch; published HF/MP2-biased
  LBCS already gives 11–41× (Hadfield arXiv:2006.15788). For weakly-correlated small
  molecules a near-FCI NQS *is* the answer → quantum readout is vacuous self-confirmation
  (the HYP-014 / LC-ladder trap, in algorithm form).
- **The one genuinely non-circular regime:** strong correlation (stretched N₂,
  post-Coulson–Fischer H₂O, π-biradicals) — NQS optimizes energy (2nd-order accurate)
  so it is a good *measurement prior* but carries 1st-order error on the *reported*
  observable, so the debiased shadow off the physical state delivers something the
  classical prior cannot self-certify. Honest novel increment there: ~3–10× shots, not
  10–100×.
- **Scores (red-teamed):** ≈ **18–36**. Interesting theory; not a build.

---

## Tier X — Refuted / killed. Do NOT re-propose.

| Candidate | Framing | Killer |
|---|---|---|
| **RG-flow criticality method-router** (B #1, the TN-bridge flagship) | B | **REFUTED, Mech 2.** Verbatim HYP-014 pattern: swaps the *validated* class (c=1/2 Ising) for the *chemical* class (long π-system) without justification. Half-filled Hubbard/PPP π-chain is a **gapped Mott insulator** (exact Bethe ansatz) or c=1 Luttinger liquid — NOT c=1/2; the Ising-tuned chi=3 tensors are not its RG. Worse: the "validated RG-flow extractor" **does not exist in validated form** — the project validated a force exponent and transport coeff, never a central-charge classifier (HYP-009 is only PARTIAL). Names a validation that was assumed, not demonstrated. |
| Logarithmic causal cone for long-range π correlation | B | **KILL outright.** Stacks all three fatal flaws: category error (acene DMRG blowup is 2D + Mott, which MERA does NOT fix), zero buildability (fermionic ab-initio MERA unsolved; project has spin chi=3 only), and an explicit PPP-toy fallback that *is* the documented repeat-failure move. |
| Scale-resolved disentangler correlation spectroscopy | B | Pre-empted by arXiv:2503.09881 (Negre/Faulstich/Lin/Cancès, "New perspectives on DMET," Mar 2025) — already builds embedding baths from a maximal-disentanglement criterion. Project has no fermionic MERA. |
| QITE-as-VQE-initializer + recycled Krylov | A | "Barren-plateau-free" is literature-false (warm starts only mitigate, fail under gap closure — arXiv:2407.02569). Dual-use is QLanczos (Motta, npj QI 2020) + reading the endpoint, relabeled. |
| Shadow-NQS → QITE oracle | A | **Maximally circular.** An NQS good enough to feed QITE the correlators to reach the ground state is itself a ground-state approximation; the quantum device only makes training data. Noise robustness inherited wholesale from Neural-Shadow QST (arXiv:2305.01078). |
| MERA disentangler as DMET bath | A | NOVELTY=5 is wrong — Vidal-Evenbly arXiv:1312.0303 (MERA impurity bath) and arXiv:2212.09798 (fermionic disentangler bath for SIAM, sign already solved) pre-empt the defining claim. |
| Auxiliary-spin Fermi-Hubbard on QuEra Aquila | C | 2-site Hubbard is closed-form / laptop-trivial; "TM-dimer" is an analogy not a simulation; cost 3–5× optimistic given Aquila's 1000-shot cap, $0.30/task, z-basis-only. Loses outright to laptop exact diagonalization. |
| Rydberg blockade frustrated-exchange cluster | C | Aquila's analog Hamiltonian is blockade-**Ising** (diagonal nᵢnⱼ); a Cu/Fe cluster singlet–triplet gap is set by **Heisenberg** exchange. Matching the gap = the project's exact "number-match ≠ mechanism" / HYP-017 trap. |

---

## Cross-cutting verdict

Two failure modes dominated, both already in the project's scar tissue:

1. **Circularity (new, specific to quantum chemistry):** if a classical method good
   enough to feed/bias the quantum step exists, it has already solved the chemistry —
   the quantum part is self-confirmation. This killed the two flashiest Framing-A
   winners. *Diagnostic for any future QC proposal: "if the classical prior is good
   enough to make this work, did it already produce the answer?"*
2. **Curve-fit-not-mechanism (the recurring project trap):** the entire Framing-B
   tensor-network bridge collapsed on it — applying Ising-CFT structure to molecular
   Hamiltonians that are in a different universality class (gapped Mott / Luttinger),
   then reading a finite-entanglement-scaling artifact as if it were the real physics.
   HYP-014, on a chemistry label.

**Bottom line / recommendation:** no Tier-0 build came out of quantum chemistry. The
only thing worth anything is **S1-QC** — and it is not a discovery, it is a *use* for
the NV/EF-NMR instrument the *previous* run already identified: a published-result
validation loop, good for instrument bring-up and outreach, not a paper. The strongest
honest move is **(a) do not pursue any Tier-X item**, **(b) treat S1-QC only as a
validation milestone if/when the S1 device from the 2026-05-16 run is built**, and
**(c) keep the project's effort on the holographic paper / SciPost track**, which
remains the highest-value work. Quantum chemistry did not produce a new direction here
— and saying so plainly is the useful result.

---
*Source files (all in research/data/papers/): QCHEM-COMBO-{A,B,C}-*.md (generation);
DEEPDIVE-qchem-{jcoupling,rgrouter,shadowbias}.md (physics deep-dives);
REDTEAM-QCHEM-{A,B,C}.md (adversarial). Prior-art caveat: paper-search arXiv MCP
returned a stale recency feed throughout; all prior-art via WebSearch with cited
URLs/arXiv IDs. Companion: NOVEL-COMBO-MENU-2026-05-16.md (the sensor run this reuses S1 from).*
