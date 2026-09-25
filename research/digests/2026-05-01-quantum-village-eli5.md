# The Quantum Village Thing (ELI5)

*2026-05-01 — recap of where we landed after the Quantum Village investigation*

Okay, so a few days ago we were trying to figure out: how do we actually *build* a quantum sensor instead of just reading papers about other people's quantum sensors. The goal was to make something that could do four jobs at once — get us a published paper, attract grant money, be useful in real life, and connect to our holographic-physics research.

The problem was cost. The fancy version (a Rydberg atom electrometer, the thing that reads radio signals using laser-frozen atoms) was going to cost about $4,300 in parts. Doable, but a real commitment.

Then we went looking on GitHub at a group called **Quantum Village** — a hacker collective that does quantum stuff at DEF CON every year. And we found something called **UncutGem**.

UncutGem is a quantum sensor someone already built, and they posted *all the plans for free*. It uses a tiny diamond with imperfections in it (called NV centers) that can sense magnetic fields. It costs about **$100** in parts, runs on a $5 microcontroller, and there's a published paper showing it works.

This is huge because it changes our project from *"build a quantum sensor from scratch"* to *"take this existing $100 sensor and make it better in a specific way."* That's a much cheaper, faster, and more publishable project.

I gave you three ways to make it better:

- **Path 1 — Sensitivity:** Spend ~$700 more to make it 1000x more sensitive
- **Path 2 — Navigation:** Add software so it can be used like a magnetic compass for places GPS doesn't work (caves, indoors, underwater)
- **Path 3 — Heart sensor:** Use it to read the magnetic field from a human heartbeat (called magnetocardiography)

You can do all three on the same $100 hardware for about $1,000 total, and each one is its own publishable result.

Separately and in parallel, we can rent time on a real quantum computer for **$115** (the QuEra Aquila, via Amazon's cloud) to run our holographic physics test. That's totally independent of the build.

**Where we got stuck:** I asked which path you wanted to go down, and you haven't picked. That's the choice in front of you right now.

---

## The four options on the table

1. Spec the UncutGem combined build in detail (BOM, software stack, publication plan)
2. Read the UncutGem paper (arXiv:2509.18329) and summarize the actual sensitivity numbers
3. Build a playground showing all four projects side by side
4. Just decide — UncutGem-combined is the answer, go

## Source files

- `research/data/papers/QUANTUM-VILLAGE-2026-001-recon.md`
- `research/digests/2026-04-27-ghost-murmur-magnav.md`
- `research/data/papers/SKUNK-2026-002-lockheed-NV-reality.md`
- `research/data/papers/MAGNAV-2026-001-network-audit.md`
- `research/digests/2026-04-26-rydberg-sensing-report.md`
