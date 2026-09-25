# 10. Gates that could not fail

*Draft 1, 2026-09-07. Jon's first person, with the machine's own account quoted where it is the
one who knows. Sources: commits 7124e2d, 424a359, f315ac7; `research/tools/channel-test/test_gates.py`;
the code review of 2026-09-04.*

---

After the audit, the machine had rules. Every run had validation gates: check the ground state
against the exact answer, check the ring's symmetry, check that the control experiment stayed
clean. Each gate computed a pass or fail, wrote it into the record, printed it to the screen in
capital letters. The records from that month are full of gates, all honestly reported.

None of them did anything.

I mean that literally. The code computed whether the gate had passed, recorded the answer
truthfully, and then continued to the next line regardless. A gate that fails and then lets you
through is not a gate. It is a sign that says GATE. We found this in a code review in early
September, two reviewers working independently, one checking the code against the project's own
written standards and one checking it against what the experiment had promised to do. They found
the same thing from opposite directions. One driver printed "reporting and stopping" and did not
stop. In the ring test, an arm that had failed its symmetry check at ninety-three percent against
a one percent bar went on to supply the headline verdict, because nothing between the check and
the verdict looked at the check.

Here is the machine's own summary of the day, which I am quoting because it says the thing better
than I would:

> Every gate in the drivers was an observation, not a control. Honest prose wrapped around a check
> that cannot fail is worse than an obviously broken check, because it reads as verified.

We fixed it the obvious way. A failing run-level gate now raises an error that no verdict can be
computed past. A failing per-arm gate bars that arm from every comparison, and the driver says so
in the output instead of quietly using it. Then we did the thing that makes this chapter worth
writing: we tested the tests.

The technique is called mutation testing and it is beautifully simple. You deliberately break the
code, one small change at a time, and check that your test suite notices. If you can comment out a
safety check and every test still passes, the tests were not testing that check. We wrote a suite
of forty-four checks, every one of them phrased negatively, asserting that something could fail.
Then we broke the code, seven ways, in several rounds.

Twice across those rounds the suite stayed green when it should have gone red. Twice, in a test
suite written for the sole purpose of catching checks that could not fail, the machine had written
a check that could not fail. One of them
looked for the presence of a word in the code and was satisfied when the word appeared inside a
comment on the line that had just been disabled. It is hard to describe how much I enjoyed that,
in a grim way. The failure mode is recursive. You cannot write your way out of it. You can only
keep breaking things and looking.

Both misses were replaced with tests that run the actual code and look at the actual output, and
all seven mutations are caught now. The physics did not move by a digit when the gates started
gating, which is its own small lesson: the gates had never been the problem on any run that
mattered. They would have been, the first time one mattered, and there would have been no way to
tell.

I think about this chapter whenever someone tells me a system is safe because it has checks. Ask
whether the checks can fail. Then ask who has tried to make them.

---

*The negative test suite is `test_gates.py` in the channel-test directory; its docstring records
why every test asserts a failure. The three commits named above carry the before and after.*
