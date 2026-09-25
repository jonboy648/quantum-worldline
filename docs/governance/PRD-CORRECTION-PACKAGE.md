# PRD Correction Package - accession DV13971

**Prepared 2026-08-17. NOTHING IN THIS FILE HAS BEEN SENT.** Two draft letters are included; both
require Jon's explicit approval before any contact with APS.

> ## ⛔ OVERTAKEN BY FACTS 2026-08-17: DV13971 WAS ALREADY REJECTED
>
> **The manuscript was desk-rejected on 2026-08-12 18:16 UTC, five days before this package was
> written.** No letter is owed, and none was sent.
>
> - From: `prd@aps.org` — **Dr. Alin Tirziu, Senior Editor, Physical Review D**
> - Subject: *Decision DV13971 Cackler* (Gmail id `19ff730cc7add0c1`; DKIM/SPF/DMARC pass on aps.org)
> - Verbatim: *"Regrettably, this manuscript fails to match the minimal threshold for the APS
>   journals. APS will not consider this manuscript further."*
> - Submission itself was real and is separately confirmed: `esub-adm@aps.org`, 2026-08-07 16:49 UTC,
>   TEMPID `es2026jul20_951`, RECVD Fri Aug 07 12:49:40 2026.
>
> **Sequence matters, and the two facts are independent.** The rejection (08-12) came *before* our
> audit found the estimator artifact (08-17). Tirziu rejected on scope/threshold grounds; there is no
> indication he caught the α defect. **Do not conflate them** — we did not get rejected for the
> error, and we should not narrate it that way. Nor does the rejection validate the error: the
> α = 3.92 result is withdrawn on its own evidence regardless of what any editor thought.
>
> ### How this was missed, which is the part worth keeping
> Every local record said "With editors": memory `paper_status.md`, `TASKS.md`, and
> `RESEARCH-LOG.md:1031` — all three written by the same process on 2026-08-07, all agreeing, none
> independent. The last actual inbox check was **2026-08-04**, eight days before the decision, and
> the reply-watcher cron had expired. This is **RESEARCH-DIRECTOR.md §7** (agreement among
> same-origin sources is a consistency check, not evidence) reproducing itself in the project's
> operational records rather than in its physics. It was caught only because Jon asked
> *"we have editors?"* and the question was checked against the inbox rather than against our notes.
>
> ### Where the correction obligation actually goes now
> Nothing is owed to APS. The manuscript is not published and not under review, so **there is no
> journal record to correct.** The obligation collapses to the two surfaces we control:
> 1. **Zenodo** (concept DOI 10.5281/zenodo.19660302, v4 published 2026-07-15) — **the only live
>    public artifact asserting α = 3.92.** This is now the whole correction job.
> 2. The **public GitHub repo**, which Jon has decided stays un-pushed for now — so the
>    data-availability statement (D-9) is moot for APS but still false as printed on the Zenodo PDF.
>
> Letters A and B below are **retained as a record of a decision overtaken by facts**, not deleted.
> Neither was sent.

**Manuscript:** "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits"
**Status:** Regular Article, submitted 2026-08-07, "With editors" (no referee reports received)
**Trigger:** `docs/governance/AUDIT-2026-08-11.md` D-2/D-3, confirmed by independent recomputation
and recorded in `research/data/simulations/SIM-2026-072.json`

---

## 1. What changed, in one paragraph

The paper's central finding, alpha = 3.92 +/- 0.16, is an artifact of the fitting procedure rather
than a property of the data. The fit is an unweighted least-squares fit of a steeply falling
profile in linear space, which places **95.8 percent** of its objective on the single point
dr = 2. Changing nothing but the error model, and discarding no data, gives 2.82 (relative-error
weighting) or 2.89 (log-space regression, the textbook power-law estimator). Across a 3 x 5 matrix
of standard estimator and fit-window choices the exponent spans 2.53 to 3.92, and **the published
value is the maximum of all fifteen**. The data do contain a power law, but at
**alpha = 2.6 +/- 0.2**, visible as six consecutive local log-slopes flat to 7.5 percent. That
value matches neither 2*Delta_T = 4 (stress tensor) nor 2*Delta_epsilon = 2 (scalar), so the
exchange-channel identification is open.

## 2. Why the corrected result is scientifically stronger

This is worth stating plainly because it changes what the paper is for. The withdrawn value was
**fixed in advance by a theorem**: Delta_T = 2 in every two-dimensional CFT, so alpha = 2*Delta_T = 4
was the only outcome the experiment could report if the implementation worked. Under the governing
standard (§6) that is near-zero counterfactual novelty. The corrected value is not predicted by
either candidate channel, so it is an open question rather than a confirmation. The paper moves
from "we measured the number theory already required" to "we measured a number theory does not yet
explain."

## 3. Evidence

| Estimator \ window | dr>=2 | dr>=3 | dr>=4 | dr>=5 | dr>=6 |
|---|---|---|---|---|---|
| linear unweighted (**published**) | **3.922** | 2.559 | 2.534 | 2.621 | 2.756 |
| linear, relative-error weighted | 2.822 | 2.710 | 2.768 | 2.864 | 2.986 |
| log-space OLS | 2.890 | 2.700 | 2.760 | 2.858 | 2.981 |

- Leverage of dr = 2 in the published fit: **95.8%** (N=24), 96.0% (N=16 exact), 96.3% (N=16 MERA)
- Local log-slopes (N=24): 2.035, **4.232**, 2.603, 2.456, 2.461, 2.533, 2.658, 2.841, 3.102,
  3.482, 4.064. No flat region at 4; a genuine plateau at 2.59
- Recorded but unpublished in the manuscript: chi2_reduced = **6.008** (dof 9, p ~ 1e-7, a formally
  rejected fit) and a 1000-resample bootstrap giving mean 3.369, sigma **0.6335**, four times the
  quoted +/-0.16
- Figure: `research/tools/force-reanalysis/alpha_reanalysis_figure.pdf`
- Reproduce with: `python research/tools/force-reanalysis/qw_alpha_reanalysis.py` (seed 20260817)

**Also found, not in the audit:** the chi = 3 MERA profile (SIM-2026-015d `.mera.V_data`) changes
sign at dr = 9 and dr = 10, while the published fit spans dr = 2..11 with a fixed-sign model. A
power law cannot change sign. That third "independent evaluation" is invalid beyond dr = 8 and its
alpha = 4.071 should not be quoted at all.

## 4. Other defects requiring correction in the same pass

| # | Defect | Status |
|---|---|---|
| D-3 | chi2_red = 6.008 and bootstrap sigma = 0.635 recorded but never reported; alpha = 2 exclusion is ~2.2 sigma, not ~12 sigma | must be disclosed |
| D-4 | Four wrong author given-names and four wrong titles in the bibliography, each contradicted by the project's own catalogue | verification in progress |
| D-5 | Five ungated priority claims ("first", "to our knowledge") in the manuscript | must be struck |
| D-1 | "Wang and He proved t_trans = pi" is **correct** (Supplemental S3.A) but their result is explicitly independent of the AdS radius, so it does not support T = (pi/2)*l_AdS | citation must be re-scoped |
| D-9 | Data-availability statement unsatisfiable: 8 of 19 named items absent from the public repo (85 commits stale); the cited Zenodo record holds one PDF, of the SciPost version | must be fixed before any resubmission |
| D-12 | The transport script never applies a MERA (`holographic_transport_16q.py:347` prints "Skipping full MERA bulk computation") | must be stated or the computation performed |
| D-13 | The paper's own chi = 3 result gives l_AdS = 0.9102, moving the transport prediction to 1.430 against a measurement of 2.239 (+57%) | unresolved |

## 5. The recommendation

**Withdraw, rebuild, resubmit.** This is not an erratum. The central number changes value and
meaning, the abstract changes, and the title's "Power-Law Holographic Forces" no longer describes
the result: the measured exponent is not the stress-tensor value, and the audit's §24 word test
found that deleting every occurrence of "geometry"/"geometric" costs the manuscript no technical
content. Correcting in place would leave a paper whose framing outruns its evidence in exactly the
way the correction is meant to fix, and would still carry the unresolved transport-anchor problem
(the AdS radius that Wang and He's own derivation says should cancel).

What survives and should anchor the rebuilt paper: the two-phase ALM plus Z2-projection optimizer,
the chi = 3 criticality threshold, the exact-diagonalization pre-gates, the measured OPE placement
systematic, and the corrected alpha = 2.6 as an open question. That is a competent methods paper.

**The alternative, if you prefer to keep the submission alive:** letter B below requests to replace
the manuscript with a corrected version. It is honest and it preserves the submission date, but it
asks an editor to accept a paper whose title and abstract both change.

---

## 6. DRAFT LETTER A - withdrawal (recommended)

> Subject: Withdrawal request, accession DV13971
>
> Dear Editors,
>
> I am writing to withdraw manuscript DV13971, "Power-Law Holographic Forces and Causal Transport
> in MERA Quantum Circuits."
>
> During a systematic internal audit conducted after submission, I found that the paper's central
> result, the force exponent alpha = 3.92 +/- 0.16, is an artifact of the fitting procedure rather
> than a property of the data. The fit was an unweighted least-squares fit in linear space, which
> places 95.8 percent of its objective on a single data point at the shortest separation retained.
> Re-fitting the same data with no points discarded, changing only the error model, gives 2.82 with
> relative-error weighting and 2.89 with log-space regression. Across fifteen combinations of
> standard estimator and fit window the exponent spans 2.53 to 3.92, and the published value is the
> largest of them. The local logarithmic slope shows no plateau at 4; it shows a genuine plateau at
> 2.6, which matches neither the stress-tensor value nor the scalar value.
>
> The audit also found that the reduced chi-squared of the published fit, 6.008, and a bootstrap
> standard deviation of 0.63 were computed and recorded before submission but were not reported in
> the manuscript. That omission is mine and I regret it.
>
> The corrected result is a different paper: the exponent changes value and interpretation, the
> abstract changes, and the title no longer describes the finding. Rather than ask you to process a
> correction of that scope during review, I would prefer to withdraw, rebuild the analysis properly,
> and submit the corrected work as a new manuscript.
>
> I am grateful for the editorial time already spent, and I am sorry to have taken it on a result I
> should have tested more carefully before submitting.
>
> Sincerely,
> Jon Cackler

## 7. DRAFT LETTER B - correction in place (alternative)

> Subject: Correction to manuscript under review, accession DV13971
>
> Dear Editors,
>
> I am writing to report a significant error in manuscript DV13971, which I found in an internal
> audit after submission, and to ask whether the manuscript may be replaced with a corrected
> version.
>
> The paper's central result, alpha = 3.92 +/- 0.16, is an artifact of the fitting procedure. The
> fit was unweighted least squares in linear space, which places 95.8 percent of its objective on
> the single point at the shortest retained separation. Re-fitting the same data with nothing
> discarded gives 2.82 under relative-error weighting and 2.89 under log-space regression; across
> fifteen standard estimator and window choices the exponent spans 2.53 to 3.92, with the published
> value the largest. The data do support a power law, at alpha = 2.6 +/- 0.2, seen as six
> consecutive local slopes flat to 7.5 percent. That value matches neither 2*Delta_T = 4 nor
> 2*Delta_epsilon = 2, so the exchange channel is unidentified.
>
> I additionally found that the fit's reduced chi-squared, 6.008, and a bootstrap standard
> deviation of 0.63 were recorded before submission and not reported, and that several
> bibliography entries carry incorrect author names and titles. All of these are being corrected.
>
> The corrected manuscript would report the measured exponent with the channel identification left
> open, would include the full fit-window and weighting analysis and the local-slope diagnostic as
> a figure, and would revise the title and abstract accordingly. If you would prefer that I
> withdraw and resubmit instead, I am glad to do that.
>
> Sincerely,
> Jon Cackler

---

## 8. Checklist before any letter is sent

Updated 2026-08-17 after the remediation pass and an independent verification sweep. Every box below
marked done was confirmed by reading the file on disk, not by an agent's report.

- [x] Bibliography verification complete — `research/data/audit/bibliography-verification.md`;
      `references.bib` rebuilt (33 entries), including **Koo & Saleur 1994** (hep-th/9312156), whose
      construction every central charge in this project is computed from and which was uncited
- [x] ERRATA E6 (α withdrawal) and E7 (failed §8 priority gate) written, with propagation ledgers
- [x] ERRATA D7 added — the χ=3 sign-flip defect the audit missed
- [x] ERRATA D2 corrected: four records contain literal `NaN`, not one. Root cause recorded —
      Python's `json.load` accepts `NaN` by default, so the project's own validator could not fail
- [x] Supersession write-backs verified present: `SIM-2026-011-interaction`, `SIM-2026-015d`,
      `SIM-2026-017-statistics`, `SIM-2026-042`
- [x] Hypothesis records reconciled — **HYP-008** → NOT_ESTABLISHED / low (its own killer test, V_T
      vs V_X, named as never run); **HYP-006** → confidence high → low (the transport formula's
      l_AdS dependence is contradicted by its own source; narrow numeric content preserved);
      **HYP-025 / HYP-027** → NOT_ESTABLISHED; **HYP-028** → OPEN / low
- [x] README corrected — headline row struck, correction box added, counts re-verified on disk,
      citation block now warns readers off both the manuscript and the Zenodo record
- [x] NEXT-SESSION.md reconciled — withdrawal is HOT STATE #1; the HYP-028 contradiction resolved
- [x] knowledge-base.md advisory header added
- [ ] **Jon reads and approves the chosen letter verbatim** ← the gate
- [ ] **Push / tag decision (Jon's call, not a default).** The data-availability statement stays
      false until the public repo is pushed and a `prd-DV13971-v1` tag exists — but pushing also
      publishes the audit, which states the under-review manuscript's central claim is an artifact,
      while it is under review. Standing project rule is commits LOCAL / never push. Staged plan:
      `research/data/audit/MANIFEST-plan.md`
- [ ] Zenodo v4 record annotated or superseded (it carries the withdrawn number publicly)
- [ ] `research/learning/` guides swept for the withdrawn number

**Order matters.** If letter A (withdrawal) is chosen, the Zenodo annotation should go up at or
before the same time, so the public record and the journal record never disagree.
