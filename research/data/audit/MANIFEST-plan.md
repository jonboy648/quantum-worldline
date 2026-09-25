# Reproducibility Freeze — Execution Plan

**Written:** 2026-08-17 · **Status:** PLAN ONLY — nothing in this document has been executed.
**Closes:** AUDIT-2026-08-11 defects **D-9** (data-availability statement unsatisfied at both
endpoints), **D-25** (no frozen snapshot for a manuscript under review), and the freeze half of
**D-21** (reproducibility metadata absent).
**Governing standard:** `docs/governance/RESEARCH-DIRECTOR.md` §21 (reproducibility), §32
(corrections are additive, never silent rewrites).

> **No git command, no network call and no upload in this document has been run.** Every fenced
> block is a proposed command for a human to review and execute. The only commands actually
> executed while writing this plan were read-only inspections (`git log`, `git ls-files`,
> `git check-ignore`, `git status`, `find`, `stat`), and each measured number below is labelled
> with how it was obtained.

---

## 0. Measured starting state

All values read off the repository on 2026-08-17.

| Fact | Value | How measured |
|---|---|---|
| Branch | `public-release`, local HEAD `9470d69` | `git log` |
| **Existing tags** | **0** — the repo has never been tagged | `git tag -l \| wc -l` |
| **Submission commit** | **`f124038f52aeb672b901bf25e4e6bfc0aa6cb4f6`** (`f124038`), 2026-08-07 11:51:45 -0500, *"SUBMITTED to Physical Review D 2026-08-07 -- accession DV13971, status 'With editors'"* | `git log -1 f124038` |
| Is it reachable? | **Yes** — ancestor of HEAD; **18 commits** now sit on top of it | `git merge-base --is-ancestor`, `git rev-list --count` |
| SIM records added after submission | **5**: SIM-2026-068, -069, -070, -071, **-072** | `git diff --name-only --diff-filter=A f124038 HEAD` |
| Public endpoint | `origin/public-release` at `13b8292`, 2026-06-17 — **85 commits behind** at audit time | audit §0, live fetch |
| Tracked tree size | **812 files, 48,214,595 B (46.0 MB)** | `git ls-files -z \| xargs -0 stat -c %s` |
| Newly un-ignorable inputs | **31 files, 394,432 B (385 KB)** — `.gitignore` exceptions landed 2026-08-17 | `git status --porcelain` after the edit |
| The one oversized input | `gs_24q_exact.npy` = **134,217,856 B (128 MB)** — stays out of git | `find … -printf %s` |

**The single most consequential fact on this list:** `SIM-2026-072.json`, added after `f124038`,
**withdraws the submitted manuscript's central claim.** The published α = 3.92 ± 0.16 is an
estimator artifact (95.8 % of the least-squares objective on the single point dr = 2); the
corrected measurement is **α = 2.6 ± 0.2 with the exchange channel OPEN**. The freeze plan is
therefore not a filing exercise — it is what makes the difference between *what was submitted* and
*what is now believed* auditable by a third party. That requirement drives §1.

## 1. Why three tags, not one

Two sources give conflicting instructions and both are half right. AUDIT §9 item 7 says *"tag
`f124038` as `prd-DV13971-v1`"*. `raw/reproducibility-audit.md` §6 says *commit the missing inputs
first, then tag*. They cannot both be satisfied by one tag, because:

- `f124038` **is** the submitted state, but a `git archive` of it **does not contain the `.npy`
  inputs** — they were gitignored on that commit and are still gitignored in its tree. A deposit
  built from it is faithful but not reproducible.
- A commit that adds the inputs **is** reproducible but is **not** what was submitted, and tagging
  it `prd-DV13971-v1` would quietly assert that it was.

Resolution — **three tags, additive, per §32**. Each answers a different question, and the diff
between them is the audit trail:

| Tag | Points at | Answers | Contains inputs? |
|---|---|---|---|
| **`prd-DV13971-v1`** | **`f124038` exactly, unmodified** | *"What did they submit to PRD on 2026-08-07?"* | No — and the tag message says so |
| **`prd-DV13971-v1-repro`** | a new commit whose tree adds inputs + manifest + provenance and **changes no recorded result** | *"How do I re-run it?"* — this is the tag that gets archived to Zenodo | Yes |
| **`prd-DV13971-v2-corrected`** | a later commit, after the α correction lands | *"What does the project believe now?"* | Yes |

**The gate that makes this honest, and it is machine-checkable.** `…-v1-repro` must differ from
`…-v1` by **added files and documentation only**. Before creating it, run:

```sh
# Must list ONLY 'A' (added) lines, plus 'M' lines confined to .gitignore, README.md,
# RUN-MERAKIT.md and docs/. Any 'M' on a research/data/**/*.json record means a RESULT
# moved inside a snapshot that claims not to have moved one -- stop and split the commit.
git diff --name-status prd-DV13971-v1 prd-DV13971-v1-repro
```

The α correction is **deliberately excluded** from `…-v1-repro` and deferred to
`…-v2-corrected`. Folding a retraction into a snapshot labelled "reproducibility, no result
changed" is exactly the silent rewrite §32 forbids.

### 1.1 Sequencing caveat — HEAD is already past the "no result changed" line

As of 2026-08-17 the working tree carries **uncommitted audit remediation** to
`SIM-2026-011-interaction.json`, `SIM-2026-015d.json`, `SIM-2026-017-statistics.json`,
`SIM-2026-042.json`, `SIM-2026-071.json`, six `HYP-*.json`, `ERRATA.md`, `RESEARCH-LOG.md`,
`README.md` and `NEXT-SESSION.md`. Those are §32 corrections written into the corrected records —
**exactly the changes the gate above is designed to catch.** So `…-v1-repro` cannot be built as
"HEAD plus the `.npy` files"; HEAD is already the corrected state.

Practical sequencing, in order:

1. **`prd-DV13971-v1` on `f124038`** — do this first and independently. It touches nothing and is
   the artifact D-25 actually names as missing. **If only one thing on this page gets done, this
   is it.**
2. **Land the audit remediation** as ordinary commits on `public-release`.
3. **`prd-DV13971-v2-corrected`** on the result, with the inputs and `MANIFEST.sha256` added
   (Steps 2–6 apply unchanged; only the tag name differs). This is the tag worth archiving.
4. **`prd-DV13971-v1-repro` is optional** and should be built only if someone specifically needs a
   *runnable* copy of the submitted state — as a short side branch off `f124038` that adds the 31
   `.npy` files and nothing else, so the gate in §1 passes by construction. It is not on the
   critical path; the deposit can be built from `…-v2-corrected` alone provided
   `README-deposit.md` (§6) carries the withdrawal notice.

## 2. Step-by-step execution order

Ordered because the dependencies are real: the tag must exist before the archive, the archive
before the checksums-of-record, the checksums before the deposit, and the deposit before the DOI
that the corrected manuscript will cite.

> **Tag name in Steps 4–6 depends on the §1.1 sequencing choice.** If the audit remediation lands
> before the freeze — the recommended order — substitute **`prd-DV13971-v2-corrected`** for
> `prd-DV13971-v1-repro` throughout Steps 4–6 and adjust the two commit/tag messages accordingly.
> Step 1 is unaffected and should be done first regardless.
>
> **One deliberate exception to the "added files only" gate:** Step 3 also *modifies* two tracked
> files — `merakit-setup/qw_tci.jl` (un-drifting it, §7.3) and `merakit-setup/setup.jl`'s companion
> (§7.4). Both are drivers, not results. Call them out in the commit message by name so the gate's
> reviewer does not have to guess whether an `M` line is benign.

**Step 1 — tag the submission, changing nothing.** Annotated (not lightweight): a lightweight tag
carries no message, and the message is where the caveat lives.

```sh
git tag -a prd-DV13971-v1 f124038 -m "PRD accession DV13971, submitted 2026-08-07, status 'With editors'.
Repository state AS SUBMITTED. Does NOT contain the .npy numerical inputs (gitignored on this commit)
-- see tag prd-DV13971-v1-repro for the reproducible tree.
KNOWN DEFECT, recorded after the fact: the central claim of the manuscript at this commit
(alpha = 3.92 +/- 0.16) is WITHDRAWN. Corrected value alpha = 2.6 +/- 0.2, exchange channel OPEN.
See research/data/simulations/SIM-2026-072.json and docs/governance/AUDIT-2026-08-11.md D-2/D-3.
This tag is preserved unaltered as the record of what was submitted."
```

**Step 2 — stage the reproducibility additions.** The `.gitignore` exceptions landed 2026-08-17;
the files are now visible to `git add` but are not yet committed.

```sh
git add research/data/simulations/theta_*.npy \
        research/data/simulations/transport_*.npy \
        research/data/simulations/boundary_density_*.npy \
        research/data/simulations/*_dims.npy \
        research/data/builds/target_Cr_8site.npy        # 31 files, 385 KB
git status --porcelain --ignored=no | grep '\.npy$' | wc -l   # expect 0 left unstaged
```

**Step 3 — resolve the MERAKit artifacts (BLOCKED — see §7.1).** The `Manifest.toml`, 7 run logs
and 2 operator arrays inside `research/tools/MERAKit.jl/` (172,077 B) **cannot be reached by a
`.gitignore` exception at all** — the tree holds its own `.git`. Copy them into the already-tracked
mirror `research/tools/merakit-setup/` before Step 4, or the deposit ships without the project's
only resolved Julia dependency manifest.

```sh
cp research/tools/MERAKit.jl/Manifest.toml \
   research/tools/MERAKit.jl/hb_lam3_0.npy research/tools/MERAKit.jl/hb_lam3_0856.npy \
   research/tools/MERAKit.jl/*.log \
   research/tools/merakit-setup/
cp research/tools/MERAKit.jl/instantiate.jl research/tools/merakit-setup/   # see §7.4
cp research/tools/MERAKit.jl/qw_tci.jl      research/tools/merakit-setup/   # see §7.3 — un-drifts the mirror
```

Note that `merakit-setup/` is **not** covered by the `*.npy` rule's exceptions, so
`hb_lam3_*.npy` landing there needs its own `.gitignore` line
(`!research/tools/merakit-setup/*.npy`) or a `git add -f`.

**Step 4 — commit, with a message that states the invariant.**

```sh
git commit -m "PRD DV13971 reproducibility snapshot: add numerical inputs, manifest, vendor provenance

Adds the 31 .npy state/parameter arrays (385 KB) that the figures and the force/transport
measurements consume, the MERAKit vendor provenance block, and MANIFEST.sha256.
NO RECORDED RESULT IS CHANGED BY THIS COMMIT -- verify with:
  git diff --name-status prd-DV13971-v1 HEAD -- research/data/**/*.json
Closes AUDIT-2026-08-11 D-21 (inputs), D-9/D-25 (freeze)."
```

**Step 5 — generate `MANIFEST.sha256` (§5), then amend it into that commit** so the manifest and
the tree it describes are the same object.

**Step 6 — tag the reproducible tree.**

```sh
git tag -a prd-DV13971-v1-repro -m "Reproducible tree for PRD DV13971 (submitted state + inputs + manifest).
Tree differs from prd-DV13971-v1 by added files only; no result record modified.
gs_24q_exact.npy (128 MB) is NOT in this archive -- it is a separate file in the Zenodo deposit,
and is regenerable in ~1228 s by research/data/simulations/interaction_energy_24q.py."
```

**Step 7 — push.** `git push origin public-release --follow-tags`. The public endpoint was **85
commits behind** at audit time; **everything else in this plan is inert until this runs.**

**Step 8 — build the archive and deposit it** (§3, §6).

**Step 9 — correct `README.md:203`,** which claims a "full reproduction package" is archived on
Zenodo. Until Step 8 completes, the Zenodo record holds one PDF — and it is the *SciPost* version,
not the submitted PRD manuscript.

**Step 10 — after the α correction lands, tag `prd-DV13971-v2-corrected`** and deposit it as a
further Zenodo version. Do not overwrite the v1 deposit.

## 3. What the `git archive` deposit contains

```sh
git archive --format=tar.gz \
            --prefix=quantum-worldline-prd-DV13971-v1/ \
            -o quantum-worldline-prd-DV13971-v1.tar.gz \
            prd-DV13971-v1-repro
```

`git archive` exports **exactly the tracked tree at that tag** — it honours `.gitignore` by
construction (an ignored file is an untracked file and is simply absent) and it excludes `.git/`.
That is the property that makes it the right tool: the archive cannot contain anything that was not
committed, so the deposit and the repository cannot silently disagree.

**Contents, by measurement of the current tracked tree (812 files / 46.0 MB) plus the additions:**

| Group | What | Size |
|---|---|---|
| `research/data/simulations/` | 86 tracked `.json`, of which **74** are `SIM-*.json` — incl. all six universality records absent from the public repo — plus the legacy `holographic_transport*.json`, `effective_mass_analysis.json`, `worldline_mc_results.json` and the analysis scripts | — |
| `research/data/{papers,hypotheses,hardware,builds}/` | **139** PAPER, **30** HYP, **76** HW, **18** build tracked `.json` records (counted 2026-08-17) | — |
| `research/data/theory/` | **8 prose `.md` files, 0 structured records** — no `templates/theory-record.json` exists, so the tier cannot be conformant even in principle (audit §14 / minor-defects list). Archived as-is | — |
| **`*.npy` inputs (NEW)** | 14 `theta_*`, 8 `transport_*`, 4 `boundary_density_*`, 4 `*_dims`, 1 `target_Cr_8site` | **394,432 B** |
| `research/tools/` | `merakit-setup/`, `pumps-setup/`, `yanglee-pt/`, `force-reanalysis/` — drivers, `VENDOR.md`, `RUN-MERAKIT.md`, the three tracked `.jsonl` raw-result files | — |
| `research/submission-package/prd/` | `paper-prd.tex`, `references.bib`, figures | — |
| `docs/governance/` | `RESEARCH-DIRECTOR.md`, `AUDIT-2026-08-11.md`, and `research/data/audit/raw/` (20 investigation artifacts) | — |
| `research/` | `ERRATA.md`, `RESEARCH-LOG.md`, `README.md`, `CLAUDE.md`, `templates/` | — |
| **`MANIFEST.sha256` (NEW)** | one line per file (§5) | ~90 KB |
| **Total** | | **~46.4 MB** |

**Deliberately NOT in the archive:**

| Excluded | Why | Where it goes instead |
|---|---|---|
| `gs_24q_exact.npy` (128 MB) | 2²⁴ × float64; wrong object for git | Separate file in the same Zenodo deposit (§6) |
| `research/tools/MERAKit.jl/` (upstream source) | Vendored clone. **MIT-licensed, so redistribution is permitted** (unlike puMPS) — excluded for size and cleanliness, not law. Pinned to `ace2f92`; a reproducer clones it. | Provenance block in `merakit-setup/RUN-MERAKIT.md` |
| `research/tools/puMPS/` (upstream source) | **No upstream license — must not be redistributed.** | Fetch recipe in `pumps-setup/VENDOR.md` |
| `.venv311/`, `__pycache__/`, `.env*`, `CREDENTIALS-*.local.md`, `.mcp.json` local token | Environments and secrets | Nowhere |

## 4. The manuscript's 19 data-availability items

`paper-prd.tex` §"Data and code availability" states: *"All simulation data and scripts are
available at github.com/jonboy648/quantum-worldline"*, then names 19 files. **8 are absent from that
URL** (verified live against `origin/public-release` = `13b8292` in `raw/reproducibility-audit.md`
§1.3). **All 19 exist and are tracked locally** — verified 2026-08-17 by `git ls-files`, so every
gap closes on Step 7 (push) with no new work.

| # | Named in manuscript | On the public repo? | Tracked locally at | Closed by |
|---|---|---|---|---|
| 1 | `holographic_transport.json` | yes | `research/data/simulations/` | — |
| 2 | `holographic_transport_24q.json` | yes | `research/data/simulations/` | — |
| 3 | `composite_geodesic_results.json` | yes | `research/data/simulations/` | — |
| 4 | `SIM-2026-008b-8q-test.json` | yes | `research/data/simulations/` | — |
| 5 | `SIM-2026-008c.json` | yes | `research/data/simulations/` | — |
| 6 | `effective_mass_analysis.json` | yes | `research/data/simulations/` | — |
| 7 | `worldline_mc_results.json` | yes | `research/data/simulations/` | — |
| 8 | `SIM-2026-011-interaction.json` | yes | `research/data/simulations/` | — |
| 9 | `SIM-2026-015.json` | yes | `research/data/simulations/` | — |
| 10 | `SIM-2026-015c.json` | yes | `research/data/simulations/` | — |
| 11 | `SIM-2026-015d.json` | yes | `research/data/simulations/` | — |
| 12 | `SIM-2026-051.json` | **NO** | `research/data/simulations/` | Step 7 |
| 13 | `SIM-2026-052.json` | **NO** | `research/data/simulations/` | Step 7 |
| 14 | `SIM-2026-062.json` | **NO** | `research/data/simulations/` | Step 7 |
| 15 | `SIM-2026-063.json` | **NO** | `research/data/simulations/` | Step 7 |
| 16 | `SIM-2026-061.json` | **NO** | `research/data/simulations/` | Step 7 |
| 17 | `SIM-2026-064.json` | **NO** | `research/data/simulations/` | Step 7 |
| 18 | `qw_ope_pev_z2.jl` | **NO** — all of `research/tools/` is absent | `research/tools/merakit-setup/` | Step 7 |
| 19 | `qw_potts_z3.jl` | **NO** — same | `research/tools/merakit-setup/` | Step 7 |

**The pattern in the eight misses is not random.** Items 12–17 are exactly the six records backing
the abstract's universality claim, and 18–19 are the two drivers that produced them. A referee
following the availability statement today finds the force and transport data and **none** of the
universality data or tensor-network code.

**Three defects the list itself carries — fixes for the corrected manuscript, not for this plan:**

1. **Item 1 points at a superseded record.** `holographic_transport.json` is the coarse-grid
   N = 16 run reporting T = 2.25; the grid-converged result of record is `SIM-2026-025.json`
   (ERRATA E2 retracted the 0.72 % residual to −1.21 %). The availability list still points at the
   retracted number's source.
2. **Item 7 failed its own validation.** `worldline_mc_results.json` carries
   `mc_quality: "POOR"`, and ERRATA D2 records it as containing invalid JSON (`NaN`).
3. **Two load-bearing records are named nowhere.** `SIM-2026-017-statistics.json` — the source of
   the ± 0.16, the χ²_red = 6.008 and the bootstrap σ = 0.635 — is cited nowhere in the manuscript
   and absent from this list; so is `SIM-2026-072.json`, which withdraws the headline. Both must
   appear in the corrected statement.

## 5. MANIFEST.sha256 — generation and verification

D-21 measured **output checksums 0/73**. This is the cheapest of all the repairs and the only
defence against the SIM-070-style divergence in which a record and its own log disagree.

### 5.1 A trap that must be handled first

The repo is configured **`core.autocrlf = true` with no `.gitattributes`** (verified 2026-08-17).
Every tracked text file therefore has **CRLF in this Windows working tree and LF in the git blob**,
and `git archive` emits the blob. **A manifest generated over the working tree would fail
verification for every text file on any machine that extracts the archive** — the exact false alarm
that trains people to ignore checksums.

> Generate the manifest **from the extracted archive**, never from the working tree.
> Independently, consider committing a `.gitattributes` containing `* text=auto eol=lf` so the
> normalization is pinned rather than inherited from whoever cloned it. *(Outside this plan's
> scope — flagged, not done.)*

### 5.2 Generation — run at Step 5, over the archive

Archive **`HEAD`** — the Step 4 commit. Not the tag: the tag is not created until Step 6, precisely
so that it can point at the amended commit that already contains the manifest.

```sh
set -e
TMP=$(mktemp -d)
git archive --format=tar --prefix=snap/ HEAD | tar -x -C "$TMP"
( cd "$TMP/snap" \
  && find . -type f ! -name MANIFEST.sha256 -print0 \
  | LC_ALL=C sort -z \
  | xargs -0 sha256sum -b ) \
  | sed 's| \*\./| *|' > MANIFEST.sha256
rm -rf "$TMP"
wc -l MANIFEST.sha256          # expect ~843 = 812 tracked at HEAD + 31 new .npy
```

`LC_ALL=C sort -z` makes the line order locale-independent, so regenerating the manifest on another
machine produces a byte-identical file. `-b` forces binary reads. The manifest excludes itself, so
the archive holds 844 files described by 843 lines.

Then fold it into the same commit — `git add MANIFEST.sha256 && git commit --amend --no-edit` — and
only then run Step 6. **If a tag was created before the amend, delete and re-create it**: amending
writes a new commit object, and the old tag would still point at the discarded one.

### 5.3 Verification — the command a referee runs

```sh
tar -xzf quantum-worldline-prd-DV13971-v1.tar.gz
cd quantum-worldline-prd-DV13971-v1/
sha256sum -c MANIFEST.sha256        # expect "OK" on every line; non-zero exit on any mismatch
```

### 5.4 The two files outside the archive

`gs_24q_exact.npy` and the tarball itself cannot be covered by a manifest inside the tarball. Ship a
separate top-level `CHECKSUMS.txt` in the Zenodo deposit:

```sh
sha256sum -b quantum-worldline-prd-DV13971-v1.tar.gz \
             research/data/simulations/gs_24q_exact.npy > CHECKSUMS.txt
```

Record the `gs_24q_exact.npy` hash **in `SIM-2026-011-interaction.json` as well**, so the record that
consumes the file names the bytes it consumed. Expected size 134,217,856 B (2²⁴ × float64).

## 6. Zenodo deposit layout

A **new version under the existing concept DOI `10.5281/zenodo.19660302`** — not a new record — so
the citation chain from the manuscript stays intact.

| File | Size | Notes |
|---|---|---|
| `quantum-worldline-prd-DV13971-v1.tar.gz` | ~46.4 MB | `git archive` of `prd-DV13971-v1-repro` (§3) |
| `gs_24q_exact.npy` | 134,217,856 B (128 MB) | The one input too large for git. Regenerable in ~1,228 s by `interaction_energy_24q.py`; deposited as a convenience, not as the sole copy |
| `paper-prd.pdf` | ~1 MB | **The submitted PRD manuscript.** The current record holds the *SciPost* PDF instead — a different document |
| `CHECKSUMS.txt` | <1 KB | §5.4 |
| `README-deposit.md` | small | Tag name, commit SHA `f124038…`, PRD accession DV13971, the `sha256sum -c` verification command, **and the α withdrawal notice** |
| **Total** | **~175 MB** | Well inside Zenodo's 50 GB per-record limit |

**`README-deposit.md` must carry the correction on its face.** A deposit of a submitted manuscript
whose central claim is withdrawn, that does not say so, is a misleading artifact regardless of what
the repository records say. One paragraph:

> The manuscript archived here reports α = 3.92 ± 0.16. **That value is withdrawn.** It is an
> artifact of unweighted least-squares fitting in linear space, which placed 95.8 % of the fit
> objective on a single data point. The corrected measurement is **α = 2.6 ± 0.2**, with the
> exchange-channel identification **open**. See `research/data/simulations/SIM-2026-072.json` and
> `docs/governance/AUDIT-2026-08-11.md` (D-2, D-3). The manuscript is archived unaltered as the
> record of what was submitted to Physical Review D on 2026-08-07.

**Operational notes** (from project memory `[zenodo-doi]` — verify before relying on them): the
deposit token with the required scopes is at `C:\Users\jonca\.zenodo-token` and belongs to the
**joncackler@gmail.com** account (the GitHub-SSO Zenodo account owns nothing). A record `GET` is
**not** `PUT`-safe — round-tripping silently strips `resource_type`, `creators`, `rights`,
`subjects`, `publisher` and `related_identifiers`, so rebuild those in canonical id-shape rather
than echoing back what `GET` returned.

## 7. What this plan does NOT fix

Stated plainly so nothing here reads as a clean bill of health.

**7.1 The MERAKit artifacts are unreachable by `.gitignore` (BLOCKER for Step 3).** Attempted and
reverted 2026-08-17, measured rather than assumed. Rewriting the rule as
`research/tools/MERAKit.jl/*` plus `!` negations for `Manifest.toml`, the 7 run logs and the 2
`hb_lam3_*.npy` operator arrays makes `git check-ignore` report all three patterns as trackable —
but `git add -n` **and** `git add -nf` on those paths staged nothing, and
`git status --porcelain -uall` still collapsed the whole tree to one entry. Cause: the directory
holds its own `.git` (a plain clone of `mhauru/MERAKit.jl` at `ace2f92`, no `.gitmodules`), and git
will not descend into an embedded repository. The `/*` form also made `git add -A` want to register
`research/tools/MERAKit.jl` as an embedded-repo **gitlink** — an active hazard while staging the
freeze commit — so the rule was returned to its bare-directory form and the reasoning left in
`.gitignore` as a comment. **Step 3's `cp` into `merakit-setup/` is the fix.** Until it runs, the
deposit ships **without the project's only resolved Julia dependency manifest**.

**7.2 Nine of our own scripts exist only in the gitignored tree** and would not be in the archive:
`diag_prefactor.jl`, `dump_ising.jl`, `instantiate.jl`, `qw_block_test.py`, `qw_diag_blocking.jl`,
`qw_diag_blocking2.jl`, `qw_diag_fusion.jl`, `qw_potts_smoke.jl`, `test_cone_v2.jl`. (The audit said
"four further drivers"; the measured count is nine.)

**7.3 `merakit-setup/qw_tci.jl` has drifted from the vendored copy, and the tracked mirror holds the
stale side** — it is the TCI driver behind the α = 4 universality claim. Confirmed by `diff`
2026-08-17; it is the **only** drifted file of 21 mirrored scripts. Archiving the mirror as-is
deposits a driver that did not produce the recorded result.

**7.4 The mirror ships the destructive setup script and not the working one.**
`merakit-setup/setup.jl` runs `rm("Manifest.toml"; force=true)` then re-resolves against a fresh
registry, which fails; `instantiate.jl`, the script that works, is **not** in the mirror. A
reproducer working only from the deposit gets the one that breaks the environment.

**7.5 Reproducibility metadata inside the records is untouched by this plan.** D-21's other counts
stand: code revision 1/73, environment spec 5/73, dependency versions 0/73, analysis-script revision
0/73, RNG seeds 9/73 (none after 2026-04). A frozen snapshot of under-documented records is still a
snapshot of under-documented records. `SIM-2026-072.json` is the counter-example to copy — it carries
driver path, figure script, RNG seed, inputs and environment in one `reproducibility` block.

**7.6 `figure3` and `figure4` fail soft.** `figure3_transport_trace.py` wraps its `.npy` loads in
`try/except` and silently draws from substitute values when the arrays are missing. Un-ignoring the
arrays removes the trigger but not the defect; the fallback should raise. (Audit §9 item 8.)

**7.7 Two Zenodo ambiguities were not resolved.** Project memory cites
`10.5281/zenodo.21381474` ("v4 published, v5 content") while ERRATA cites v3 at
`10.5281/zenodo.19661227` and the live fetch of the concept DOI returned v4 with one PDF. Enumerate
every version record before depositing, or the new version may attach to the wrong concept.

**7.8 Nothing here touches the manuscript.** `research/submission-package/**` is handled by the
human. The corrected data-availability statement (§4's three defects) and the PRD erratum are that
workstream, not this one.

## 8. Standing rule

Adopt, because this will recur:

> **Every manuscript submission and every Zenodo version gets an annotated git tag at the moment of
> submission, created before the submission is sent, and a `MANIFEST.sha256` generated over the
> archived tree. A submission without a tag is not a submission that can be defended.**

The project came within one `git tag -a` of having this already: `f124038` is a clean,
correctly-messaged commit made at submission time. What was missing was not discipline — it was one
command. Codify it in `CLAUDE.md` under Development Rules so it is not re-derived a third time.

