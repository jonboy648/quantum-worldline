# The story: outline (S workstream, started 2026-09-07 after Zenodo v5 published)

Decisions of record (PLAN-2026-09-06.md, section S): one long-form document; audience = the reel's
audience, curious non-physicists; Jon's first person; Claude and the agent team named as
collaborators; all of the failure, in the order it happened; opens on the reel (credit by handle,
brief quote, link, no redistribution); ends at the HYP-008 result with the trunk question as the
open door. No em dashes. Every number in the text traces to a record listed under its chapter.

**Amended by Jon, 2026-09-18 and 2026-09-21 (supersedes "Jon's first person" above):**
- Audience: the general public. Audio first; the text is the transcript.
- Voice: an unnamed third-person narrator telling a story ABOUT Jon. The AI appears as a character,
  "the machine". Every "we" gets resolved into a named actor (Jon, the machine, or both).
- Jon's real typed words (chapter 2 transcript lines, chapter 6 "We have editors?") stay as direct quotes.
- No pandering, no performed humility, no owing or gratitude lines, no decorative description.
  Explain, do not gesture: every term gets a plain picture on first use.
- Plain language throughout. A few real numbers allowed from chapter 4 on.
- Chapter 1 defines yes and no but does not give away the specific noes. The approved plain
  pictures for them are in `PLAIN-PICTURES.md`, to be used in the chapter where each happens.
- The ADHD idea (attention spread out, not missing, so far-apart ideas touch) is a light thread:
  a mind good at spotting patterns also spots ones that are not there.
- Settle each chapter's text with Jon before spending narration credits.

Working title: **Shadow of a Worm** (placeholder; Jon picks).

## Chapters and beats

1. **The reel.** A psychology grad in a physics class: the birth-to-death worm, the triple integral as
   the shadow of a 4D thing. Quote two sentences, credit the handle, link. What it did to Jon.
   Sources: `the video - origin transcript.md`.
2. **Can math prove any of this?** The 2025 conversation: ADHD as superposition, frosted glass,
   "I would choose to integrate". The decision to build a team instead of going alone.
   Sources: `the beginning.txt`; memory origin story.
3. **Building the machine.** Fourteen agents, three tiers, a plugin. What an agent team is, honestly:
   fast, tireless, and exactly as wrong as its instructions. Sources: `docs/specs/2026-03-10-...`.
4. **The first number.** Emergent geometry from a spin chain: what MERA is (a picture, no equations),
   the "force" between two kicks, and the exponent 3.92 that matched a beautiful prediction to 2%.
   Sources: SIM-2026-011, SIM-2026-015d, SIM-2026-017 (the original claims, quoted as claimed).
5. **Believing it.** Three "independent" evaluations, universality at three fixed points, a paper,
   a DOI, seven emails to physicists, a journal submission. Zero replies. A desk rejection.
   Sources: RESEARCH-LOG, outreach memory, `paper_status.md`, ERRATA E6 "where it appears".
6. **Eleven days of "with editors".** Three notes agreeing with each other and with nothing outside.
   The rule that came out of it. Sources: CLAUDE.md "External Status Must Be Freshly Checked".
7. **The audit.** Twenty-three agents told to be hostile. What "counterfactual novelty" means: if the
   answer could not have come out otherwise, you did not learn anything. Twenty-one of thirty-four.
   Sources: `docs/governance/AUDIT-2026-08-11.md`, RESEARCH-DIRECTOR sections 5-8.
8. **One point.** 95.8 percent of the fit sat on a single data point. The same data, a different
   error model: 2.8. Fifteen ways to fit, the published one was the largest. The bootstrap error
   computed before release and left out. Sources: SIM-2026-072, ERRATA E6.
9. **The test that compared a thing to itself.** Kramers-Wannier: two probes that were one operator.
   The spin probe that the observable cannot see at all. Sources: SIM-2026-073/074, ERRATA E8.
10. **Gates that could not fail.** The code review: every safety check computed a verdict and
    nothing branched on it. Mutation testing catching my own toothless tests, twice.
    Sources: commits 7124e2d, 424a359, f315ac7; `test_gates.py` docstring.
11. **Saying it out loud.** The correction notice: what it withdraws, what it keeps, why it does not
    name the journal. Publishing a retraction against your own DOI. Sources: Zenodo v5 notice.
12. **The honest test, and what it found instead.** Two clean probes, gates fixed before running,
    a null hypothesis that would have been boring. Verdict: void. And the thing nobody planned to
    find: the force is exactly blind to half of what it was pointed at. Sources: SIM-2026-075,
    PREREGISTRATION-T.md.
13. **Snapshots along the worm.** The reel's second idea, made precise: timelike entanglement and
    "emergent time" in the literature. What the lattice said when asked literally. (To be written
    from SIM-2026-076; the chapter's ending depends on Jon's next decision.)
14. **The open door.** The trunk question: does the geometry ever add anything beyond the CFT?
    What a yes would look like. What we would do differently. Sources: RESEARCH-DIRECTOR section 29.

## Rules for the draft
- Numbers in tables or on their own line, never more than one per sentence.
- Every failure named with who made it. The agent team's errors are mine to describe, not Jon's.
- No claim of novelty anywhere without the section-8 record behind it.
- Appendix A: glossary. Appendix B: the full withdrawal table from the notice. Appendix C: how to
  rerun everything (drivers, seeds, sizes).
