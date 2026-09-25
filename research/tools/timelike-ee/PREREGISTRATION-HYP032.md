# Pre-registration IV: HYP-2026-032, timelike entanglement on the critical TFIM ring

**Status: APPROVED by Jon 2026-09-07 ("yes"), committed BEFORE any code for this hypothesis existed.
Check `git log` on this file against the run record. Governs SIM-2026-076 onward. The Route X
transcription (`ROUTE-X-DERIVATION.md`) is the next artifact and precedes the first driver.**

## The question, and where it came from

The project's origin (Instagram reel DVe5jiJj1rv; `the video - origin transcript.md`) pictures a
person as one 4D object with all its moments coexisting, and memory as touching another point on
that object. The scientific translation, decided 2026-09-06: **correlations between time-separated
slices of one quantum system**, made precise as the **timelike entanglement entropy** of Doi,
Harper, Mollabashi, Takayanagi and Taki (PAPER-2026-139, -140). Its imaginary part is what those
authors call an emergent time. The personal layer stays in the story; this document is the math.

**HYP-2026-032.** An emergent geometry built from the critical TFIM ground state can reproduce the
bulk-only piece of the timelike entanglement entropy (its imaginary part) only if the construction
carries a time direction; a plain scale-direction MERA cannot, and a transition-matrix network
(ground-state MERA glued to its time-evolved conjugate) is the minimal object in which the
question is open.

## Claim levels (RESEARCH-DIRECTOR.md section 5), fixed now

- **Level 1 (validation gate).** Reproduce the CFT prediction for c = 1/2 on the lattice:
  `Re S(T) = (1/6) log((R/pi) sin(pi T/R)) + const`, `Im S = pi/12`.
- **Level 2 (method).** (a) Do the two lattice definitions below agree at finite n? (b) Written,
  not run: a plain MERA has no time direction and integer minimal cuts, so it cannot produce an
  imaginary part. Counterfactual novelty of (b): one outcome possible. It is recorded as a negative
  and given no more weight than that.
- **Level 3 (the registered question).** Does the glued transition-matrix network have a cut
  structure whose length reproduces Re S, and (stretch) whose complex-valued extension reproduces
  Im S = pi/12?

## Model

Critical TFIM ring, `H = -sum Z_j Z_{j+1} - sum X_j`, h = 1, PBC, c = 1/2. Same chain, same
gates, same conventions as SIM-2026-073/074/075.

## The two lattice definitions (Level 1 and Level 2a)

**Route G (Gaussian, PAPER-139 section 2.4).** Jordan-Wigner to free Majoranas. Timelike EE of a
temporal interval of length T at one spatial point from the eigenvalues of the Wick-rotated
correlation matrix restricted to the interval, using PAPER-139's prescription `i k -> i omega_k`
applied to the lattice dispersion. Sizes R = 64, 128, 256; lattice cutoff epsilon = 1; T from 4 to
R/2 in unit steps. **This prescription is adopted by its authors "as the correct prescription"
on the lattice; it is not derived there. That is why Route X exists.**

**Route X (exact transition matrix).** Pseudo entropy `S = -Tr(tau_A log tau_A)` of the reduced
transition matrix `tau_A = Tr_B |psi><phi| / <phi|psi>` realizing PAPER-139's thermofield-double-
at-imaginary-temperature construction on the ring, evaluated by exact state vectors at n = 16, 20,
24. No prescription; the definition is applied literally. Branch of the log: principal, with the
eigenvalue trajectory tracked continuously in T from T = 0 so a branch crossing is detected and
reported, never silently absorbed.

The exact operator content of Route X (which state plays |phi>, which subsystem is traced, the
role of the spatial point) is to be transcribed from PAPER-139 sections 2.2-2.4 into
`ROUTE-X-DERIVATION.md` BEFORE any code, and that transcription is part of what Jon approves.

## Gates and pass criteria (all controls)

- **L1-G.** Route G at all three sizes: log-OLS slope of Re S against `log((R/pi) sin(pi T/R))`
  over T in [8, R/4] within 3% of 1/6; `Im S` within 3% of pi/12 for every T in that window.
  Both parts, all three sizes, or Route G is VOID.
- **L1-X.** Route X at n = 24: same criteria on the (shorter) window T in [3, 9]; n = 16 and 20
  reported for the trend. Miss = VOID for Route X.
- **L2a.** Where both routes exist (n = 16, 20, 24 for G run at those sizes too), `|S_G - S_X|`
  per T. AGREE if within 3% in both real and imaginary parts at every T in the n = 24 window;
  DISAGREE otherwise, reported with the T-dependence of the discrepancy. Either is a result.
  Prior art (section 8): PAPER-2026-141 is a different (real-valued) object and does not pre-empt
  this; a search for a published finite-n comparison of the two Doi et al. definitions is part of
  the gate and its outcome is recorded here before running. If found, L2a becomes a cited
  reproduction with no novelty claim.
- **L3-T.** Trotter brickwork for `e^{-iHT}` (second order, step dt fixed in advance at 0.05)
  checked against exact evolution at n = 16, 20, 24: fidelity loss < 1e-6 at the largest T used,
  or the network leg is VOID.
- **L3-cut.** Minimal cut through the glued network (GS MERA, chi fixed at 4 and 8, from the
  existing MERAKit optimizer; Trotter layers; conjugate MERA), weighted `log(chi)` per bond,
  homologous to the temporal interval. Cross-check: Synge distance in the induced metric
  (HYP-2026-026 machinery). PASS if the cut length tracks `Re S` with the same slope within 10%
  over the n = 24 window for at least one chi and both readings agree within 10%.
- **L3-Im (stretch).** Any pre-specified complex-valued extension of the cut (to be written in
  `ROUTE-X-DERIVATION.md` before running; if none can be written, this item is recorded as
  NOT ATTEMPTED, not as a failure).

## Outcomes

- **VOID:** L1-G or L1-X fails. No verdict on anything downstream.
- **L2a:** AGREE / DISAGREE, always reported when L1 passes.
- **L2b:** written negative, always recorded.
- **L3 PASS:** L3-cut passes. **L3 FAIL (the kill):** L1 passes, L3-T passes, and no chi
  produces the Re S slope from the network cut. Recorded as a Level 3 negative: the glued network's
  geometry does not carry timelike correlations at these sizes.
- **L3-Im:** REPRODUCED / NOT REPRODUCED / NOT ATTEMPTED.

## Budget and stop rule

Level 1 plus one network attempt, about two weeks, RunPod under 20 USD. At the end of that,
whatever the state, a new decision is required from Jon before more is spent.

## Follow-on noted, out of scope

PAPER-2026-020's composite timelike-spacelike geodesics and their claimed factor-of-2 in transport
times (our ratio 1.7, HYP-2026-006, geometric reading at low confidence). Not part of HYP-032.

## Banned

Selecting T windows after seeing results; changing dt, chi, or the branch rule after seeing
results; "first", "novel", "to our knowledge" without the section 8 record above; calling
Level 1 or L2b a finding.
