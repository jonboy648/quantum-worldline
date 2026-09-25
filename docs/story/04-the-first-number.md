# 4. The first number

*Draft 1, 2026-09-07. Jon's first person. Sources: SIM-2026-011-interaction.json, SIM-2026-015d.json,
SIM-2026-017-statistics.json, the v4 Zenodo abstract. The claims in this chapter are stated as they were
claimed at the time. Chapter 8 is where they come apart.*

---

I need to explain three things before the number means anything: the chain, the network, and the
force. I will do it without equations, which means I will be slightly wrong in places, and I will
say where.

**The chain.** Take a row of tiny magnets, each of which can point up or down. Make them want to
agree with their neighbours, and at the same time push each of them sideways with a field that
makes them want to point neither up nor down but somewhere in between. Turn the sideways push up
slowly. At one exact strength, the row stops being able to decide whether it is magnetized or not,
and at that strength something remarkable happens: the row forgets how long it is. Patterns repeat
at every scale. A stretch of ten magnets looks statistically like a stretch of a hundred. Physicists
call this a critical point, and the reason it matters here is that a critical row of magnets is
described exactly by a theory that also describes the surface of a much stranger object. That
theory is the edge. The strange object is the space behind it.

**The network.** The state of even a short critical chain is an enormous list of numbers, one for
every possible arrangement of ups and downs. For twenty-four magnets that is about sixteen million
numbers. A tensor network is a way of writing that list as a circuit: layers of small boxes, each
box taking in a few magnets and passing out fewer, coarse-graining the chain step by step until one
box at the top holds the whole thing. The particular network we used is called MERA, and it has a
property that made a lot of people sit up when it was noticed: if you draw it, the layers stack
into a shape that looks like a curved space, and distances measured through the layers behave like
distances in the kind of space that holographic physics says should live behind an edge like ours.
The chain is the shadow. The network is a picture of what casts it. Whether it is more than a
picture is the question this project was about.

**The force.** Here is the experiment we invented, and I still think it was a good idea. Poke the
chain at one spot, in a specific way that the theory of the edge tells you how to do, and measure
how much energy the poke costs. Poke it at a second spot and measure that. Now poke both spots at
once. If the two pokes do not know about each other, the cost of both is the cost of each added
together. If they do, there is a leftover: the energy of two disturbances feeling each other across
the distance between them. Call that leftover the force. Measure it at every separation you can,
and see how it falls off with distance.

If the space behind the edge is real, that falling-off should follow a rule, and the rule should
say what kind of thing is carrying the interaction between the two pokes. The theory of the edge
offers two natural candidates: a light one and a heavy one. Each would make the force fade with a
different power of the distance. The heavy one, the one connected to the geometry itself, would
make it fade as the fourth power. The light one, as the second. Those two numbers, four and two,
are fixed by symmetry and cannot be argued with. What we could argue about was which one nature
picked.

We built the chain of twenty-four magnets exactly, no approximation, and measured the force at
every separation from one to eleven. We fit a curve to it. The exponent came out at three point
nine two, give or take a sixth. Four, within two percent.

Here is the number, and here is what we said about it at the time:

| What we measured | What it matched | How close |
|---|---|---|
| force exponent 3.92 ± 0.16 | the heavy candidate, exactly 4 | 2 percent |

Then we did it again at sixteen magnets and got 3.97. Then we did it a third way, with the network
itself standing in for the exact chain, and got 4.07. Three measurements, all within a hair of the
same round number, and that round number belonged to the candidate that means the geometry is
real.

I remember exactly how that felt, and I am going to try to be honest about it rather than wise
after the fact. It felt like the reel. It felt like the question I had asked the machine a year
before had an answer, and the answer was yes. The machine agreed. It wrote, in the abstract we
would later publish, that this established quantitative physical content in the correspondence,
and I believed it, because it had never been more certain about anything, and
neither had I.

We were both wrong about what the number meant, and it would take five months and a deliberately
hostile audit to find out how. But I want this chapter to end where that day ended, because that is
where it did end: with a number that matched, three times, and two collaborators who had stopped
asking whether it could have come out any other way.

---

*Where the numbers live: the 24-site exact profile and fit are SIM-2026-011; the 16-site and network
evaluations are SIM-2026-015d; the error estimates are SIM-2026-017. What was wrong with them is
E6 and D7 in `research/ERRATA.md`, and chapter 8.*
