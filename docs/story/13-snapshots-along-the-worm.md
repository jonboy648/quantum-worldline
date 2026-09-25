# 13. Snapshots along the worm

*Draft 1, 2026-09-08. Jon's first person. Sources: PAPER-2026-139 (Doi, Harper, Mollabashi,
Takayanagi, Taki 2023), SIM-2026-076, SIM-2026-077, `PREREGISTRATION-HYP032.md` and `-A.md`. Numbers
in the table are from those records.*

---

The reel had a second idea, and I had been saving it.

Memory as touching another point on the worm. A vision as touching a point you have not lived yet.
If a person is one object stretched through time, then the correlation between you-now and
you-then is not a metaphor, it is a quantity, and quantities can be computed. It took a year to
find the physics that says this precisely, and when we found it, it had the reel's own word in its
abstract.

In 2023 a group in Kyoto defined something they called timelike entanglement entropy. Ordinary
entanglement entropy measures how much a region of space knows about the rest of space. Theirs
measures the same thing for an interval of time: how much one stretch of a system's history is
tied to the rest of its history. The number comes out complex. Its real part looks like the
ordinary entropy with time in place of distance. Its imaginary part is a constant, fixed by the
theory of the edge, and the authors proposed that this imaginary part "describes an emergent time,"
generalizing the way ordinary entanglement is said to describe emergent space.

Snapshots along the worm, with a formula. I could not have asked for a cleaner translation.

So we asked our chain. We wrote the rules first, as always now: reproduce the published formula on
the lattice as the gate, then ask whether an emergent geometry built from the chain can carry the
imaginary part. And we asked in the most literal way possible. The paper gives an exact recipe for
the object whose entropy this is, a kind of density matrix at an imaginary temperature. We built
that object on the chain, exactly, with no approximation, and computed its entropy.

The imaginary part was zero.

Not small. Zero to fourteen decimal places, at every size, every interval, every temperature. And
when we looked for the reason, it was a two-line argument: the critical chain has a symmetry that
sends its energy to minus itself, and that symmetry forces the entropy of this object to be real.
Always. The "emergent time" the formula promised is not a property of the lattice object the
formula is supposed to describe. It comes from the way the formula is continued from one kind of
interval to the other, a choice of branch in a logarithm.

The Kyoto paper, to its credit, had half-said this. Its own figure on the imaginary part is
captioned as "the challenge," and it shows the imaginary part appearing only as a regulator is
turned up. We turned the same regulator up, exactly, on our chain. The real part snapped into the
predicted form, to two or three percent, in both of the parameters the formula has. The imaginary
part stayed near zero all the way up.

That is where the first pre-registration stopped, by its own rules, so we wrote a second one with
the imaginary part as the question. Is there any consistent way to build this object on a lattice
that produces the promised constant? We registered four. Break the symmetry with a small field.
Follow the logarithm's branch continuously from a real temperature, the way the continuation
actually does. Use the paper's own free-fermion case instead of ours. Close the chain into a ring
and trace over everything. Each one had a gate and a pass rule fixed in advance, and all four ran
on rented machines over two days.

| Candidate | What it does | Result |
|---|---|---|
| broken symmetry | small field, exact diagonalization | no, with one caveat below |
| tracked branch | follow the log continuously | no |
| paper's own case | free Dirac fermion, c = 1 | no |
| ring, full trace | periodic chain, exact | no |

Four noes. By the rule, that is the negative result we registered: among these constructions, the
imaginary part of timelike entanglement is a feature of the continuum bookkeeping and not of any
lattice object we can build. The real part, the ordinary entropy with time in place of space, is
real and reproducible. The "emergent time" is not there to be found.

The caveat, and then the part of the caveat I got wrong the first time I described it.

With the symmetry broken by a field, the imaginary part does appear, and at the largest chain we
could reach, at one particular field and one particular regulator, it landed within seven percent
of the predicted constant. The rule we had written required the same setting to pass at two
sizes, and the smaller chains had been run with a shorter interval, so the identical setting never
existed twice. Recorded as a no, and flagged as the one thread worth following.

A day later I went back and read the stored numbers instead of my own summary of them, and found
three things. The window that passed was three points wide, and it was a slice cut out of a curve
that rises steadily by half its own value across every interval length we had. There was no
plateau. It crossed the predicted number on its way up. Second, with the field switched off
entirely, the imaginary part is not zero once the regulator is on, because the symmetry argument
only forces zero when the regulator is off, and nobody had measured whether that background grows
with the size of the chain. Third, I had told the story of a peak: vary the field, and the effect
dies on both sides. That peak is real, but it is at a smaller chain and a shorter interval. At the
size that passed, only three fields were ever run, the value climbs across all three, and the run
was cut before it reached the fourth. I had repeated my own sentence about it twice before
checking.

So the thread survives, but thinner than I described it, and the follow-up is written around the
three corrections rather than around the number that excited me. There is also now an ordinary
physical explanation on the table with a prediction of its own. The field is the kind of
perturbation that gives the chain a length scale, and at the field where the effect appeared, that
length is about eight sites on a chain of fourteen. Things look special when the scale you added
happens to equal the box you put it in. If that is what this is, the effect must move to a much
smaller field as the chain grows, by a specific amount we can compute in advance. If it stays put,
it is not that.

I want to say clearly what this does and does not mean for the reel. It does not mean the worm is
wrong. A person is still, in relativity, one object in time. It means that the specific, beautiful,
quotable claim that the correlation between your moments carries an imaginary signature of
emergent time is, on the one system where we could check it exactly, a property of the algebra
and not of the system. The snapshots are real. The part of the formula that made them mysterious
was the part we could not find.

And this is the first time in the project that a result came out of a pre-registered gate, was
labeled the way the standard demands, ran on the one instrument we have that cannot be fooled by
an approximation, and gave a clean answer to a question I actually cared about. It is a no. It is
the best no we have.

---

*SIM-2026-076 holds the exact-zero result and the symmetry argument; SIM-2026-077 the four
candidates. Both pre-registrations are committed before their code; the second was approved by Jon
in writing before commit. Compute for both: about six dollars.*
