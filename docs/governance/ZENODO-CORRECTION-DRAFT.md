# Zenodo correction -- DRAFT FOR REVIEW. NOTHING PUBLISHED.

**Record:** v4, DOI `10.5281/zenodo.21381474` · concept `10.5281/zenodo.19660302`
**Published:** 2026-07-15 · **File on record:** `paper-draft-scipost.pdf` (one file)
**Drafted:** 2026-08-23. **Requires Jon's explicit go-ahead before anything is uploaded.**

## Why this is now the whole job

PRD rejected the manuscript on 2026-08-12, so no journal record exists to correct. The repository
stays local by decision. **This Zenodo record is therefore the only public artifact anywhere that
still asserts alpha = 3.92.** Anyone who finds this work today finds the withdrawn number, stated as
established fact, with a citable DOI attached.

## What the live record says right now (fetched 2026-08-23)

Its description opens by asserting the retracted result as the headline:

> "...the interaction energy between boundary-primary excitations follows a power law F(dr) ~
> dr^(-alpha) with three consistent evaluations yielding **alpha = 3.92 +/- 0.16** (24q), 3.97 +/-
> 0.15 (16q), and **4.07 +/- 0.18** (16q chi=3 MERA), all consistent with stress-tensor exchange
> (alpha = 2*Delta_T = 4) and inconsistent with scalar exchange (alpha = 2)..."
>
> "...Because Delta_T = 2 is fixed by conformal symmetry in every unitary 2D CFT, **alpha = 4 is
> universal**... giving **alpha = 4.00 at all three universality classes.**"

Every bolded claim is withdrawn. Note the third one especially: alpha was never measured at TCI or
Potts. The towers were measured there; the exponent was inherited from the Ising fit that failed.
And the 4.07 leg is doubly void -- that profile changes sign inside its own fit window (ERRATA D7).

## Recommended action: publish a v5 that is explicitly a correction

Not a silent metadata edit. Zenodo versioning keeps v4 permanently resolvable, so anyone holding the
v4 DOI must be able to see that it is superseded and why. Three parts:

### 1. A correction notice prepended to the description

> **CORRECTION NOTICE (v5, 2026-08-23). The central result of v1-v4 is withdrawn.**
>
> The force exponent reported in earlier versions as alpha = 3.92 +/- 0.16 is an artifact of the
> fitting procedure, not a property of the data. The fit was unweighted least squares in linear
> space applied to a steeply falling profile, which places 95.8 percent of its objective on the
> single point at the shortest retained separation. Re-fitting the same data with nothing discarded,
> changing only the error model, gives 2.82 (relative-error weighting) or 2.89 (log-space
> regression). Across fifteen combinations of standard estimator and fit window the exponent spans
> 2.53 to 3.92, and the previously published value is the largest of them.
>
> The corrected measurement is **alpha = 2.6 +/- 0.2**, identified as a genuine plateau in the local
> logarithmic slope over six consecutive separations. This value matches neither stress-tensor
> exchange (2*Delta_T = 4) nor scalar exchange (2*Delta_epsilon = 2), so **the exchange channel is
> an open question** rather than an identification.
>
> Consequently withdrawn: the claim that the exponent is universal across the three CFT classes (the
> exponent was measured only at Ising; the tricritical and Potts results are accurate measurements of
> the operator spectra, not of the force exponent), and the third "independent evaluation"
> alpha = 4.07, whose profile changes sign within its own fit window and cannot be fit by a
> fixed-sign power law.
>
> Also disclosed, having been computed before the original release and not reported: the fit's
> reduced chi-squared is 6.008 (9 dof), and a bootstrap gives a standard deviation of 0.63 rather
> than the quoted 0.16.
>
> **What is not affected:** the two-phase optimization method, the chi = 3 criticality threshold, the
> measured OPE coefficient C_sigma-sigma-epsilon = 0.50 +/- 0.03 against the exact 1/2, the conformal
> towers at all three classes, and the stress-tensor self-coupling C_TTT values. The transport result
> is separately disputed on two grounds and should be treated as unresolved.
>
> Full re-analysis, driver and figure: see the correction record cited below. This work was not
> published in a peer-reviewed venue; it was submitted to Physical Review D and rejected on
> 2026-08-12, on separate grounds and before this error was found.

### 2. Files to add alongside the existing PDF

- `SIM-2026-072.json` -- the re-analysis record
- `qw_alpha_reanalysis.py` + `qw_alpha_figure.py` -- driver and figure (seed 20260817, one command)
- `alpha_reanalysis_figure.pdf` -- the two-panel diagnostic
- `ERRATA.md` -- the full error register, E6/E7/D7 included

**Do NOT re-upload the manuscript PDF unchanged.** Either upload it with a visible correction banner
on page 1, or leave v4's PDF as the historical artifact and let the notice carry the correction.
My recommendation is the banner, since PDFs get downloaded and separated from their landing page.

### 3. Metadata

- Title: unchanged (renaming breaks citations). The notice carries the correction.
- Version: `v5`
- Add `related_identifiers`: `isSupplementedBy` -> the audit, `isNewVersionOf` -> v4 (automatic)
- Keep the concept DOI as the thing to cite.

## Honest note on what this costs

Publishing this makes the retraction permanently and publicly attached to your name and DOI. That is
the point, and it is the right call, but it should be a decision made with open eyes rather than a
box ticked. The alternative -- leaving a wrong number public and citable because no journal is
forcing the issue -- is worse, and it is the kind of thing this project's own ERRATA rule 5 was
written to prevent: *record retractions at full strength, in the project's own words, before anyone
else writes them down.*

## Mechanics when approved

Token: `~/.zenodo-token` (deposit scopes, joncackler account -- the GitHub-SSO account owns nothing).
**Gotcha, already learned the hard way:** a record GET is NOT PUT-safe -- round-tripping silently
strips `resource_type`, `creators`, `rights`, `subjects`, `publisher` and `related_identifiers`.
Rebuild those in canonical id-shape rather than echoing back what GET returned. Cookie-auth API
writes need an `X-CSRFToken` header. Details in memory `[[zenodo-doi]]`.

Sequence: new version -> upload files -> set metadata -> **verify the draft renders** -> publish.
I will stop before the publish step and show you the rendered draft.
