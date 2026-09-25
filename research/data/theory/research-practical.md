# Practical Submission Readiness Assessment

**Assessor:** Practical Analysis Agent (Task #3)
**Date:** 2026-04-02
**Paper:** "Power-Law Holographic Forces and Causal Transport in MERA Quantum Circuits" (draft v3)

---

## 1. Page Count / Word Count

**Main text word count (Sections I-IX, excluding Supplemental):** ~6,081 words (raw markdown including headers, table markup, equations).

**Estimated prose-equivalent:** ~5,200-5,500 words after stripping markdown formatting, table delimiters, and section headers. This significantly exceeds the PRL limit.

**PRL limit:** 3,750 words (or 4 REVTeX pages in twocolumn format). Each display equation counts as ~16 words. Each figure counts as ~170 words (single-column) or ~340 words (double-column). With 5 figures (assume 3 single-col + 2 double-col = 3*170 + 2*340 = 1190 words equivalent), the text budget drops to ~2,560 words.

**VERDICT: OVER LIMIT by approximately 2,500-3,000 words.** The paper as written is approximately 1.5x-2x the PRL format. This is the single biggest blocking issue.

**Options:**
- (A) Cut aggressively: move Sections IV (worldline correspondence), VI (chi=3), and parts of VII (hardware) to Supplemental Material. The core letter would be: force profile (alpha=3.92) + transport (0.72%) + ALM method. This is feasible but loses the chi=3 narrative.
- (B) Switch target journal to PRX Quantum (no strict page limit, tensor-network audience). This is the better fit -- see Section 6.
- (C) Submit as-is to PRL; they will desk-reject on length.

---

## 2. Figures

All 5 referenced figures exist as both `.py` generation scripts and `.png` output:

| Figure | File | Status |
|--------|------|--------|
| Fig 1 (MERA schematic) | `figure1_mera_schematic.png` | EXISTS |
| Fig 2 (ALM convergence) | `figure2_alm_convergence.png` | EXISTS |
| Fig 3 (Transport trace) | `figure3_transport_trace.png` | EXISTS |
| Fig 4 (Force/worldline) | `figure4_force_worldline.png` | EXISTS |
| Fig 5 (Helios error budget) | `figure5_helios_error_budget.png` | EXISTS |

**Chi=3 figure (potential Fig 6):** The paper's Section VI presents substantial chi=3 results (8q and 16q MERA, force profile comparison) but does NOT reference a Fig 6. If chi=3 stays in the main text, it needs at least one figure showing the correlation function comparison (chi=2 flat vs chi=3 power-law) and/or the three-way force profile comparison. This is a gap.

**Fig 4 note from MEMORY.md:** "Regenerate Fig 4 with scipy curve_fit (proper alpha=3.92 label)" is listed as a next step. Unclear if the current PNG has the correct label.

---

## 3. References

22 references listed [1]-[22]. Specific issues:

| Ref | Issue |
|-----|-------|
| [3] Kim & Swingle | "PRX Quantum (2017)" -- missing volume, pages, DOI. PRX Quantum launched in 2020, so a 2017 paper cannot be in PRX Quantum. This is likely Phys. Rev. X or another journal. **Needs correction.** |
| [6] Sahay, Lukin, Cotler | "PRX Quantum (2025)" -- no volume/pages/DOI. May be arXiv-only or in press. Needs arXiv ID at minimum. |
| [12] Zou, Milsted, Vidal | "Phys. Rev. Lett. (2020)" -- missing volume, pages. |
| [14] Anand et al. | "PRX Quantum (2023)" -- missing volume, pages. |
| [17] Wang et al. | "Nature Computational Science (2026)" -- no volume/DOI. |
| [18] Sun et al. | "Nature (2026)" -- no volume/DOI. |
| [19] Di Francesco et al. | Textbook reference -- OK but could use chapter/page for fusion rules. |

**No missing arXiv IDs for arXiv papers** -- refs [7], [8], [9], [10], [11], [13], [15] all have IDs.

**Nocedal and Wright** is cited in-text (Section II.B) but not in the reference list. Needs a formal [N+1] entry.

**VERDICT:** 6-7 references need volume/page/DOI completion. Ref [3] has a journal name error. One in-text citation (Nocedal & Wright) is missing from the reference list.

---

## 4. Author Info

- **Author:** Jon Cackler (Independent Researcher) -- PRESENT
- **Contact:** joncackler@gmail.com -- PRESENT
- **Institutional affiliation:** "Independent Researcher" -- This is acceptable for PRL/PRX Quantum. Many papers use this. However, no ORCID is listed, which is increasingly expected.
- **Missing:** ORCID iD, postal address (some journals still require this for independent researchers).

**VERDICT:** Minimally complete. Add ORCID before submission.

---

## 5. arXiv Blocking

**Current status (from MEMORY.md):** "arXiv endorsement pending (Cotler/Swingle/Zaletel/Kim contacted)"

**Risk:** arXiv endorsement in hep-th or quant-ph requires an existing author with endorsement privileges. If none of the four professors respond, there is no fallback within arXiv.

**Fallback options:**
1. **SciPost Physics** -- no endorsement required, open-access, good tensor-network audience. Accepts letters (SciPost Physics Letters) or full papers (SciPost Physics).
2. **Quantum** (journal) -- open-access, no endorsement barrier, strong quantum-info audience.
3. **Find endorsers through other channels:** Post on tensor-network community forums, contact other MERA researchers (Evenbly, Hauru, Bridgeman). Independent researchers have successfully obtained endorsement by emailing authors of papers they cite.
4. **Submit to journal first, arXiv after acceptance:** Some journals provide their own arXiv endorsement pathway.

**VERDICT:** Not a hard blocker, but a real risk. Pursue multiple endorser contacts simultaneously. Have SciPost as a parallel submission target.

---

## 6. Journal Targeting

### PRL
- **Pro:** Highest impact, broad physics audience, prestige.
- **Con:** 3,750 word limit (paper is ~2x over). Requires ruthless cutting. Referees may object that 5 results dilutes the letter format -- PRL prefers ONE main result with supporting evidence. The paper tries to be both a methods paper (ALM+projection, chi=3) and a results paper (forces, transport, effective mass).
- **Fit:** Poor given current length and scope.

### PRX Quantum
- **Pro:** No strict page limit (typical papers are 15-25 pages). Tensor-network and holography audience. Open access. High-quality referees. Still APS family. Impact factor growing rapidly.
- **Con:** Lower prestige than PRL. Longer review times.
- **Fit:** EXCELLENT. The paper's multi-result structure, detailed methods, and chi=3 extension all belong in a longer format. The audience (quantum information + gravity) is exactly PRX Quantum's sweet spot.

### PRA
- **Pro:** Easier acceptance, good for methods papers.
- **Con:** Lower impact, less appropriate for the holographic-gravity angle.
- **Fit:** Moderate. Would work for the ALM+projection method alone but undersells the physics.

### SciPost Physics
- **Pro:** No endorsement barrier, open-access, strong European HEP/condensed-matter audience.
- **Con:** Less name recognition in US physics.
- **Fit:** Good alternative if PRX Quantum review is slow.

**RECOMMENDATION: PRX Quantum as primary target.** The paper is already structured as a PRX Quantum article. Trying to force it into PRL format would require cutting the chi=3 results, the OPE interpretation, and the hardware path -- all of which are significant contributions. PRX Quantum also has the right referee pool (tensor networks + holography).

If PRL is strongly preferred: cut to 3 results (force profile + transport + ALM method), move chi=3 and effective mass to supplemental, cut Section VIII.E (AI methodology) entirely, compress hardware to one paragraph. This would require a near-total rewrite.

---

## 7. GitHub Repo and Data Availability

**Repo exists:** `github.com/jonboy648/quantum-worldline` (PUBLIC)

**Paper S5 says:** "All simulation data and scripts are available at [repository URL]"

**Problem: `[repository URL]` is a placeholder.** Must be replaced with the actual URL.

**What's in the repo (main branch):**
- SIM-2026-001 through SIM-2026-014 JSON files: YES
- Figure 1-5 PNGs and .py scripts: YES
- holographic_transport.json, holographic_transport_24q.json: YES
- effective_mass_analysis.json, worldline_mc_results.json: YES (in main branch)
- composite_geodesic_results.json: YES

**What's NOT in the repo (only on local `public-release` branch):**
- SIM-2026-015.json, 015b.json, 015c.json, 015d.json (chi=3 data): NOT IN REPO
- SIM-2026-016.json (kinematic space): NOT IN REPO
- paper-draft.md, paper-draft.tex, paper-draft.html, paper-draft-preview.pdf: NOT IN REPO
- Chi=3 simulation scripts (sim2026015*.py, sim2026016*.py): NOT IN REPO

**VERDICT:** The data availability statement references a placeholder URL. More critically, the chi=3 results (Section VI) -- which are a major paper finding -- have no supporting data in the public repo. The `public-release` branch has uncommitted/unpushed files that need to be merged to `main` before submission.

**Action items:**
1. Replace `[repository URL]` with `https://github.com/jonboy648/quantum-worldline`
2. Push SIM-2026-015 series data to the repo
3. Add SIM-2026-015d force profile data explicitly (this supports the alpha=3.97/4.07 claims)

---

## 8. LaTeX Status

**File:** `research/paper-draft.tex` exists (996 lines)

**Currency:** The .tex file is STALE. It corresponds to draft v2 (dated 2026-03-25), while the .md is v3 (dated 2026-04-03). Specific differences:

| Feature | .tex (v2) | .md (v3) |
|---------|-----------|----------|
| Results count | "four results" | "five results" |
| Section VI (chi=3) | Absent (listed as open question in Discussion) | Full section with 8q and 16q results |
| Section VIII.F (OPE) | Absent | Full OPE/fusion rule analysis |
| Force measurements | 1 (24q exact) | 3 (24q exact, 16q exact, 16q chi=3 MERA) |
| Supplemental S1 table | 12 entries (through SIM-2026-011) | 15 entries (through SIM-2026-015d) |
| References | 15 | 22 |

**The .tex file needs complete regeneration from the current .md.** The pandoc-generated .tex also has formatting issues:
- `\author{}` is empty (should use REVTeX `\author` + `\affiliation` macros)
- Math is not in proper LaTeX math mode (e.g., "dr^{-alpha}" instead of `$\mathrm{d}r^{-\alpha}$`)
- Tables use `longtable` instead of REVTeX-compatible `table`/`tabular`
- No `\bibliography` command -- references are hardcoded text
- No proper abstract environment

**VERDICT:** The .tex is unusable in current form. It needs either:
- (A) Full regeneration via pandoc with a proper REVTeX template, followed by manual cleanup of author info, math, and bibliography
- (B) Manual conversion from the .md with proper LaTeX authoring (preferred for journal submission)

---

## 9. Summary: Blocking Issues

### Must Fix Before ANY Submission
1. **Word count:** Paper is ~2x over PRL limit. Either cut to PRL format or retarget to PRX Quantum.
2. **`[repository URL]` placeholder** in S5 -- replace with actual GitHub URL.
3. **LaTeX:** .tex is stale v2, needs complete regeneration to match v3 .md.
4. **Reference [3]:** Journal name error (PRX Quantum didn't exist in 2017).
5. **6-7 incomplete references:** Missing volume/pages/DOI.
6. **Nocedal & Wright:** Cited in text but missing from reference list.
7. **Push chi=3 data to GitHub:** SIM-2026-015 series not in public repo.

### Should Fix
8. **Add ORCID** to author info.
9. **Fig 4 label:** Verify alpha=3.92 label is present (memory says regeneration needed).
10. **Chi=3 figure:** Add a figure for Section VI results (correlation comparison or force profile).
11. **arXiv endorsement:** Continue pursuing; have SciPost fallback.

### Nice to Have
12. **Supplemental formatting:** Currently inline in the .md; should be a separate file for journal submission.
13. **Cover letter** for journal submission.
14. **Suggested referees** list (most journals request 3-5).

---

## 10. Recommended Submission Path

1. **Retarget to PRX Quantum** (avoids the word-count crisis entirely)
2. Fix references [3], [6], [12], [14], [17], [18]; add Nocedal & Wright
3. Replace `[repository URL]` placeholder
4. Push chi=3 data to GitHub repo
5. Regenerate .tex with proper REVTeX4-2 formatting
6. Add Fig 6 (chi=3 correlation comparison)
7. Verify Fig 4 has correct alpha label
8. Write cover letter with suggested referees
9. Submit to PRX Quantum
10. Simultaneously submit to arXiv (once endorsement secured) or SciPost if arXiv blocked

**Estimated time to submission-ready:** 1-2 weeks of focused work, dominated by LaTeX preparation and reference cleanup.
