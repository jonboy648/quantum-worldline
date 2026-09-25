# 12. The honest test, and what it found instead

*Draft 1, 2026-09-07. Jon's first person. Sources: `research/tools/channel-test/PREREGISTRATION-T.md`
(commit 82b7b4e), SIM-2026-075.json, HYP-2026-008.json. Numbers are in SIM-075.*

---

The hypothesis still had a question in it, under all the wreckage. Does the force between two
pokes on the chain travel by the heavy carrier or the light one? The old test could not ask it.
The direct replacement was blocked by the wall between symmetry rooms. But the symmetry that had
wrecked the old test also handed us a way around it.

Kramers and Wannier's mapping swaps two ingredients of the chain. Some combinations of those
ingredients are unchanged by the swap; others flip sign. The energy density, the thing the whole
chain is made of, is unchanged. And a thing that is unchanged by the swap cannot contain any
ingredient that flips, which means the energy density, poked locally, cannot contain the light
carrier at all. Its leading content, in the theory of the edge, is the heavy one. Its partner, the
combination that flips sign, is purely the light one. Both of them stay in the same symmetry room.
Two clean probes, one for each candidate, built from pieces the code already had.

We wrote the rules first, again, and this time we wrote harder ones. The probes had to prove
themselves before they were allowed to measure anything: each one's own two-point correlation had
to fall off with distance at the rate its candidate demands, or the probe was void and no force
would be read from it. A second gate identified the heavy carrier directly in the chain's spectrum
of excitations and checked that the probe had zero overlap with the light one, an exact zero that
the symmetry guarantees. Three sizes, a convergence rule fixed in advance, a control experiment off
the critical point that had to stay boring. And a null hypothesis, stated before running, that
would have been the most likely and least interesting outcome: that the force simply follows the
probe's own correlation, four for the heavy probe and two for the light, in which case the
hypothesis closes as a validation of the tools and nothing more.

Here is what happened.

The heavy probe passed its identification gate perfectly. The spectrum had the heavy carrier where
it should be, and the probe's overlap with the light carrier was zero to thirteen decimal places.
It was the right operator. And it failed its correlation gate at every size. Its own two-point
function fell off as roughly the seventh power of distance, not the fourth, because on a chain of
twenty-four magnets a local poke of this kind is dominated by short-wavelength junk that the
theory of the edge does not describe. The right operator, at these sizes, cannot be read.

The light probe passed its correlation gate cleanly. Its two-point function fell off as the second
power, exactly as it should. And its force was zero.

Not small. Zero. To fourteen decimal places, at every separation, at every size we tried. Move the
chain off the critical point by a hair and the force reappears. Come back, and it vanishes again.
We scanned a mixture of the two probes, and the force scaled as the square of the amount of the
heavy probe in the mix. The energy-difference measurement we had built the entire project around
is exactly blind to the light carrier at the critical point. It responds only to the heavy
admixture, and to nothing else.

That was not in anyone's plan. It was not among the registered outcomes. It is the one genuinely
new fact the test produced, and it is a fact about the measurement, not about the geometry.

It also reaches backward. The ring measurement from chapter nine, the one that looked like it was
heading toward two, was made with an ordinary poke that contains both probes. Its force came from
the cross-term between them. It was never the light carrier's exponent. The correction notice was
reworded that afternoon to stop saying it might be.

By the rules, the verdict was void: both probes failed a gate, at every size, including the one
retry the rules allowed. And by the rules, that closes the hypothesis: untestable, in this
framework, at any size we can reach. Not refuted. Not confirmed. Closed, with the reason written
down.

I had expected to feel worse about that than I do. The hypothesis had been the project's headline
for five months and its heart for longer. But a question you cannot ask with your instrument is a
fact about your instrument, and we now know something about ours that we did not know when we
built it, that we had never thought to check, and that the next person to try this will need. Whether
someone else already knew it is a literature question we have not yet answered, so I make no
claim about that. That is not nothing. It is, by the standards we adopted in chapter seven, a
method result, second level, honestly labeled. It is the first result of this project I would
defend to a stranger without a caveat.

---

*The pre-registration was committed at 82b7b4e on the evening of 2026-09-06, before the driver
existed; the runs and the retry are SIM-2026-075. The closure is recorded in HYP-2026-008 with the
rule that produced it.*
