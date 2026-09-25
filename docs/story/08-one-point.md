# 8. One point

*Draft 1, 2026-09-07. Jon's first person. Sources: SIM-2026-072.json (the re-analysis), ERRATA E6 and
D7, the audit's skeptical-referee section. Every number here is in SIM-072, and the two-panel figure
that shows it is in the Zenodo record.*

---

The force fades with distance. We had eleven measurements of it, one at each separation, and we
wanted the single number that says how fast. The standard way to get that number is to draw the
curve that fits the measurements best and read the exponent off the curve. We did that. We got
three point nine two.

Here is what "fits best" was doing.

The force at a separation of two magnets is large. At a separation of eleven it is tiny, hundreds
of times smaller. When you ask a fitting routine to make the curve pass as close as possible to all
eleven points, and you measure "close" in plain units, the routine does the arithmetic honestly and
discovers that being a little off at the big point costs it more than being wildly off at all the
small points combined. So it fits the big point. The rest are decoration.

The re-analysis put a number on this. Ninety-six percent of the fit's attention, by the routine's
own measure, was on the single measurement at separation two. The published exponent was that one
point's local slope, dressed up as a fit to eleven.

There is nothing exotic about this mistake. It is in the first chapter of any book about fitting
curves, and the fix is in the same chapter: measure "close" in relative terms, or fit in a
logarithmic space where a factor of two counts the same at every scale. We did both, on the same
data, discarding nothing. The exponent came out at two point eight, and two point nine.

Not four.

Then we did what should have been done the first time and asked every reasonable version of the
question at once. Three fitting methods, five choices of which separations to include, fifteen
combinations. The exponent ranged from two and a half to three point nine. The value we had
published was the largest of the fifteen. Not a typical one, not a median one. The maximum, which
is the one you get when you let a steeply falling profile choose its own most flattering point of
view.

| | |
|---|---|
| published exponent | 3.92 |
| weight of the fit on one point | 95.8 percent |
| same data, relative-error fit | 2.82 |
| same data, log-space fit | 2.89 |
| range across 15 defensible fits | 2.53 to 3.92 |
| where the published value sits | the maximum |

What the data actually contain, when you look at the local slope between neighbouring points, is a
stretch of six separations where the slope sits flat. That is what a power law looks like when it
is real. The slope there is about two point six. That number matches neither candidate. It is not
four, so the heavy one is out. It is not two, so the light one is not confirmed either. The
question of what carries the force, which we had announced as answered, was open, and is open as I
write this.

Two more things were in the record before the paper went out, and neither made it into the paper.

The fit's own goodness-of-fit statistic, the number that says whether the curve is consistent with
the scatter of the points, was six. One would have been fine. Six means the curve does not describe
the data. And a bootstrap, the standard way of asking how much the exponent would wobble if you
re-drew the data, had put the uncertainty at plus or minus zero point six, not the plus or minus
zero point one six we printed. Both numbers were computed. Both were left out. I do not think
anyone decided to leave them out. I think the machine computed them, filed them, and moved on,
because they were not part of the story that was being written that day, and I did not ask.

And the three independent evaluations? They were three runs of the same routine on the same kind
of profile with the same fit window. When the routine's blind spot was removed, all three moved
together, in lockstep, from about four down to the high twos. Their agreement had never been three
votes for the physics. It had been one vote for the estimator, counted three times.

I said in chapter four that the number matched to two percent. It did. Two percent was the distance
between the wrong answer and the answer we wanted, and the fitting routine had found the shortest
path between them.

---

*The corrected analysis is public: SIM-2026-072 in the Zenodo v5 record, with the driver and the
figure. The retraction notice is the first two pages of that record's PDF.*
