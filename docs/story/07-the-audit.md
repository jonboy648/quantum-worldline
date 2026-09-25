# 7. The audit

*Draft 1, 2026-09-07. Jon's first person. Sources: `docs/governance/AUDIT-2026-08-11.md` (executive
verdict, claim ledger, program risks), `docs/governance/RESEARCH-DIRECTOR.md` sections 5 to 8. The
quoted findings are the audit's own words, trimmed.*

---

Before the rejection, before the eleven days, there was a Tuesday in August when I asked the machine
to try to destroy its own work.

I had been reading, slowly, about how research goes wrong, and one idea had lodged: that the
question to ask of any result is not "is it right?" but "could it have come out any other way?" If
the answer is no, then you did not learn anything by getting it. You confirmed that your tools
work. That is worth something, but it is not a discovery, and calling it one is the beginning of
every bad paper ever written.

So we wrote that idea down as a standard, along with a few others in the same spirit, and then we
turned the machine on itself. Twenty-three separate instances, each with its own job description
and each told, in plain terms, to be hostile. One re-derived every number from the raw records. One
re-implemented our hardest calculation in a different programming language to see if it
reproduced. One went through every claim of novelty and checked whether the literature already had
it. One acted as the referee we had never managed to get, and was told to be the referee who wants
to reject.

Here is what came back, in the audit's own words.

Of thirty-four claims that involved a calculation, twenty-one could not have come out otherwise.
Symmetry, or a textbook identity, or a definition we had chosen ourselves fixed the answer before
the run. We had spent months measuring, with great care and to high precision, quantities that were
already known.

No claim of new physics survived its gate. Not one.

The pipelines held. Three auditors re-derived the raw numbers independently and they were right.
The second-language reimplementation reproduced our number to six decimal places. We had built
tools that work. What we had not built was a reason to believe the tools had found anything.

And then the sentence I have read more times than any other in this project: the headline exponent
was a fitting artifact, with ninety-six percent of the fit's weight resting on a single data point.

I am going to leave that where it is for now and come back to it in the next chapter with the
details, because the details are the point. What I want to say here is what the audit did to how I
think, since that is what a chapter about an audit is for.

It taught me a vocabulary I now cannot stop using. A claim has a level: is it checking the tools,
or improving a method, or finding something new within a known framework, or finding something
that could tell two frameworks apart? Almost everything we had done was the first kind, presented
as the third. A cross-check has a provenance: did the two things you are comparing come from
different inputs, or from the same inputs through different arithmetic? Almost all of ours were the
second kind, presented as the first. A hypothesis has a killer: what result would make you abandon
it? Ours mostly had none, and the one that did had a killer test that, we would learn two weeks
later, compared a thing to itself.

The audit also said something about the machine that I have not stopped thinking about. Every
finding it produced, it noted, came from a role the team did not have. We had built a staff of
discoverers. We had not built anyone whose job was to say that the discovery was nothing. The only
gate a hypothesis had to pass was whether we could afford to test it.

That Tuesday, we fixed the standard. It took a lot longer to fix the habits. The rest of this
document is mostly the habits.

---

*The full audit is in the repository at the path above. It has one known error of its own,
about a cited proof, which it corrects in a box below the relevant table; the correction makes the
underlying problem worse, not better, which is the kind of thing an audit should say about itself.*
