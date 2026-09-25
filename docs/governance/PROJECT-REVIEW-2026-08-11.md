# Quantum Worldline — Project Review, 2026-08-11

**Status:** informal review written before the formal audit (see `AUDIT-2026-08-11.md` once
produced under `docs/governance/`). Where the two disagree, the audit — which is evidence-linked
and adversarially verified — supersedes this document. Retained because it is the reasoning that
motivated adopting `RESEARCH-DIRECTOR.md` as the program's governing standard.

**Ground truth at time of writing:** 106 commits since 2026-03-29 · 85 simulation records ·
139 catalogued papers · 76 hardware records · 30 hypotheses · 17 build records · 30 weekly
literature scans · `research/data/theory/` EMPTY · HEAD `9470d69`.

---

## 1. Where it came from

The project began in early 2025 as a conversation about whether intuition and pattern
recognition might work in a "quantum-like" way, ending with one question: *can math actually
prove any of this?* The relevant fact for a review is that the metaphor-to-measurement
conversion **succeeded**: "seeing behind frosted glass" became the AdS/CFT boundary-bulk
correspondence in MERA, and then became numbers with error bars. Most speculation of this kind
never produces a falsifiable number. This produced 85 simulation records and a submitted paper.

The origin is motivation. It is not evidence, and it does not get to answer its own question.

## 2. What was built

**Research apparatus.** 14-agent tiered team, 6 skills, structured JSON records for every
paper/hypothesis/simulation/hardware milestone, 30 weekly literature scans, chronological
research log, ERRATA file. This is why the science is auditable at all. The scan gotchas
(arXiv API silently dropping parallel queries), dedup rules, and ID high-water discipline each
caught errors that would otherwise be in the record now.

**Measurement pipelines.** Three, each validated against exact results before use:
1. MERA optimization with Z₂/Z₃ symmetry (SIM-051→063)
2. Koo–Saleur circle route, ED + puMPS (SIM-067→069)
3. Biorthogonal non-Hermitian ED (SIM-070/071)

## 3. Results, sorted honestly

**Bin 1 — guaranteed before measurement.** α = 2Δ_T = 4 across Ising/TCI/Potts is fixed by
conformal symmetry (Δ_T = 2 in *every* 2D CFT). C_TTT = 2√2/√c is a Virasoro identity.
C_σσε = 0.5 has been exactly known since BPZ 1984. Excellent *pipeline validation*, near-zero
*discovery*. A referee will say so and be right.

**Bin 2 — genuine but modest.**
- L₂ε contamination ~400× suppressed in puMPS Bloch-state elements; corrections p ≈ 2.4 rather
  than the feared N^−0.2 (SIM-068). Not written down elsewhere as far as we currently know.
- Transport T = (π/2)·l_AdS at −1.2%; m_eff 0.693 vs 0.670. Caveat that must always travel with
  these: both sides descend from the same CFT data, so independence is weaker than it appears.
- The error discipline itself: 5 hypotheses formally REFUTED, 1 SHELVED with named killers, and
  a published number retracted by the project's own follow-up (ERRATA E2).

**Bin 3 — where surprise was possible.** HYP-028. Without reflection positivity nothing
guaranteed the construction would survive. Result (SIM-071): biorthogonal Koo–Saleur elements at
Yang–Lee return c = −22/5 *including sign*, excluding c_eff = +2/5 by sign and an order of
magnitude; unitary control on identical code returns 0.49986 vs 0.5. Calibrated read: strongest
result in the project, still **methodological** rather than discovery-grade — if the
lattice-to-Virasoro correspondence extends to the biorthogonal setting, true-c follows
algebraically, so the finding is "the extension holds." What makes it non-trivial is that it
could have failed (PT-breaking, exceptional points, severe module mixing — the φ-descendant
element is 10× T's, inverting the identification rule that works in every unitary chain).
**Novelty is UNVERIFIED pending the literature gate.**

## 4. The crux question

Every quantitative success so far is **ordinary CFT data**. Any good CFT method reproduces it;
no geometry required. The "holographic force" is an interpretation layered on correct CFT
numbers. The two results closest to geometry-specific (transport, m_eff) are also the least
independent.

> Is there an observable whose value differs between "MERA is an efficient CFT ansatz" and
> "MERA is a discrete geometry"?

That is the program's real question, and it has not been asked yet. It is now the trunk
(`RESEARCH-DIRECTOR.md` §4, §29).

## 5. Practical standing

- Paper 1 at Physical Review D since 2026-08-07, accession `DV13971`, "With editors".
- Structural blockers persist and are **not** about merit: no arXiv endorser, SciPost silent
  since April, QCUP stalled, 7-target outreach with zero replies over 20 days.
- Honest odds on PRD: below even for acceptance as-is. Likeliest referee response —
  *"carefully done, but what here is not fixed by symmetry or already in Zou–Milsted–Vidal?"*
  That answer should be written before the question arrives.

## 6. What follows

1. Draft the referee response now (the "isn't α=4 kinematics?" objection).
2. Paper #2 is the better paper: the unitary ladder (SIM-067/068/069) + the non-unitary
   extension (SIM-070/071) — a methods contribution that does not depend on the holographic
   interpretation surviving review.
3. Design the discriminating observable (§4 above).
4. Repair or retire `research/data/theory/` — currently empty while interpretation carries a
   large share of the scientific burden.

---

**Bottom line.** In ~5 months of active work: a validated three-way measurement pipeline, a
complete self-coupling ladder across three universality classes, a novel non-unitary extension,
a submitted paper, and a written record of the project's own retractions. The physics that is
*guaranteed* is oversold if presented as discovery; the physics that *isn't* guaranteed is where
the value lives. The main risk is not that the numbers are wrong — it is that they are right and
unsurprising, and the framing is asked to carry more weight than it can.
