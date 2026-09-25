# 9. The test that compared a thing to itself

*Draft 1, 2026-09-07. Jon's first person. Sources: SIM-2026-073.json, SIM-2026-074.json, ERRATA E8,
`research/tools/channel-test/PREREGISTRATION.md` and `PREREGISTRATION-RING.md`.*

---

The audit had said the exponent was wrong. It had not said what the right one was, and it had
pointed at the way to find out: the hypothesis had always carried, in its own file, a description
of the experiment that would decide it. Poke the chain with the heavy candidate and measure the
force. Poke it with the light one and measure again. If the two exponents differ, the force knows
what it is made of. That test had been written down in March and never run. So we ran it.

We did it properly this time, or so I thought. Before a line of code existed, we wrote down the
rules: which separations counted, which fitting method was banned, what result would be called
which outcome, what would void the run. We committed the rules to the record with a timestamp, so
nobody, including us, could move them after seeing the data. That is called pre-registration and
it is the single most useful habit this project acquired.

The test ran. The two exponents came out different, but not by enough, and one of the two probes
was so much weaker than the other that the difference was within the noise. Outcome: indeterminate.
Honest, unsatisfying, recorded.

Then the machine did something I want to give it credit for. It noticed that the two exponents on
a second, cleaner geometry were not just close. They were identical. Not to a few percent. To one
part in a billion. And instead of calling that a coincidence, or a bug, it stopped and asked why.

The answer is a piece of physics that is nearly a hundred years old and that neither of us had
thought to apply. The critical chain has a hidden symmetry, discovered by Kramers and Wannier in
the nineteen-forties, that maps the chain onto itself with the roles of two of its ingredients
swapped. And under that swap, the operator we had been calling the heavy candidate turns into the
operator we had been calling the light one. At the critical point they are not two different ways
of poking the chain. They are one poke, described in two dialects.

The registered test, the one written in March, the one that was supposed to decide the hypothesis,
had compared a thing to itself. Whatever it returned, it could not have distinguished anything.
Both of the labels in the hypothesis file were wrong: the "heavy" probe was not the heavy candidate
at all, and the "light" probe was the same light candidate wearing a disguise.

We checked it numerically, because a symmetry argument is exactly the kind of thing you can talk
yourself into. The two probes' average values agreed to fifteen decimal places. Their force profiles
agreed to thirteen. On the ring, where the symmetry is exact, the identity held at one part in a
billion at the largest size we could reach. It was not close. It was the same number.

Then the second shoe. The actual light candidate, the one that had never been in the test, turned
out to be something our measurement cannot see at all. Our force is an energy difference: the cost
of two pokes minus the cost of each alone. That subtraction only makes sense if all the states you
are subtracting live in the same room. The true light probe flips the chain into a different room,
a different symmetry sector, and the subtraction reaches across the wall and returns nonsense. Not
a small nonsense. A gate we had set at one percent failed at ninety-three.

So, by the end of August, here is where the hypothesis stood. Its headline number had been an
artifact. Its registered test had been a tautology. Its corrected test was blocked by a symmetry.
And the only clean thing to come out of the whole exercise was a number on the ring that looked
like it might be heading toward two, the light candidate, at a single size, not converged, which
we wrote down with every one of those caveats attached and which, as chapter twelve will explain,
turned out not to mean that either.

I keep coming back to the fact that this was caught by a number being too good. Two results that
agree to a billionth are not a triumph. They are a question. The habit of treating a perfect match
as a warning rather than a win is, I think, the second most useful thing this project taught me,
right behind writing the rules down first.

---

*Kramers and Wannier's duality is textbook material; the specific identity used here, and its
numerical verification at three sizes, are in SIM-2026-074. The parity obstruction to the light
probe is in the same record. The withdrawal of the registered test is ERRATA E8.*
