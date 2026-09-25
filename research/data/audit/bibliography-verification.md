# Bibliography verification — `research/references.bib`

**Defect:** AUDIT-2026-08-11 **D-4** (Tier 0, item 2 of §9).
**Executed:** 2026-08-17.
**Scope:** every entry in `research/references.bib`, checked field by field.
**Method:** each entry cross-checked against (a) the matching record in
`research/data/papers/`, and (b) a **primary source** — the arXiv abstract page
(`https://arxiv.org/abs/ID`), a locally downloaded PDF of the paper itself
(`research/downloads/`), or the Crossref REST API record for the DOI
(`https://api.crossref.org/works/DOI`). Publisher landing pages were used only to
confirm a journal reference the arXiv page did not carry.
**Validation:** `bibtex` (MiKTeX 0.99e) parses all 32 entries with **0 errors**;
brace balance 0; no duplicate keys; file is pure ASCII.

---

## 0. Headline

| | Before | After |
|---|---|---|
| Entries | 26 | 32 (26 corrected + 6 added) |
| Entries with **wrong author names** | **8** | 0 |
| Entries with **wrong titles** | **8** | 0 |
| Entries with a wrong journal / volume / page / DOI | **3** | 0 |
| Entries carrying a verifiable arXiv ID | 9 | 29 |
| Entries carrying a DOI | 11 | 24 |

The audit alleged *four* wrong given-names and *four* wrong titles. Verification
against primary sources found **twice that**: eight entries with wrong authorship
and eight with wrong titles, across **13 of 26** entries. Three of the newly found
errors are worse than anything the audit listed, because they name **people who are
not authors of the cited work at all** — see §2.

**Nothing in this file was rewritten silently.** Per RESEARCH-DIRECTOR §32, every
citation *key* that is now known to be a misnomer has been **retained** (the
manuscript under review at PRD, accession DV13971, cites those keys), and a `note`
field plus a header comment in `references.bib` records the original error, the
correction, and why the key was kept. The old claim is preserved; the corrected
claim sits next to it.

---

## 1. Full entry table

Legend — **Verdict:** `OK` all fields verified correct · `FIXED` at least one field
was wrong and is now corrected · `ENRICHED` nothing was wrong; missing identifiers
added · `ADDED` new entry.

### 1.1 Entries that were wrong

| Key | Field checked | Was it right? | What it is now | Primary source |
|---|---|---|---|---|
| **`KimSwingle2017`** | author | **NO** — `Kim, Chris H. and Swingle, Brian`. There is no "Chris H. Kim"; Swingle is not an author. | `Kim, Isaac H. and Kastoryano, Michael J.` | arXiv:1701.00050 abs |
| | title | NO — title-cased variant | `Entanglement renormalization, quantum error correction, and bulk causality` | same |
| | volume/pages | **NO** — `2017` / `168` | `04` / `040` (JHEP 04 (2017) 040) | same |
| | doi | **NO** — `10.1007/JHEP04(2017)168` | `10.1007/JHEP04(2017)040` | same |
| | year, eprint | yes | unchanged (2017, 1701.00050) | same |
| **`SahayLukinCotler2025`** | title | **NO** — `Holographic forces in tensor networks` | `Emergent Holographic Forces from Tensor Networks and Criticality` | arXiv:2401.13595 abs; `PAPER-2026-003/009.json` |
| | author | yes — Sahay, Lukin, Cotler | unchanged | same |
| | journal/volume/pages/year | yes — PRX 15, 021078 (2025) | unchanged; **DOI + arXiv ID added** (`10.1103/PhysRevX.15.021078`, 2401.13595) | journals.aps.org/prx/abstract/10.1103/PhysRevX.15.021078 |
| **`BohraSivaramakrishnan2025`** | author | **NO** — `Bohra, Kausik` / `Sivaramakrishnan, Mythili` | `Bohra, Hardik` / `Sivaramakrishnan, Allic` | arXiv:2511.22168 abs; `PAPER-2026-020.json` |
| | title | **NO** — `Composite geodesics in AdS spacetimes` | `Composite AdS geodesics for CFT correlators and timelike entanglement entropy` | same |
| | eprint, year | yes | unchanged; `primaryClass = hep-th` added | same |
| **`Roux2026`** | author | **NO** — `Roux, Antoine` | `Roux, Jean-Baptiste` | arXiv:2601.07382 abs; `PAPER-2026-023.json`; Crossref 10.1088/1361-6382/ad56ef |
| | title | **NO** — `Superspace worldline formalism as quantum gravity` | `Superspace worldline formalism approach to quantum gravity: dimensional reduction and holography` | same |
| | journal | **MISSING** — none | `Class. Quantum Grav.` **41**, 147001; DOI `10.1088/1361-6382/ad56ef` | Crossref |
| | year | **NO** — `2026` (the arXiv posting date) | `2024` (the publication year); key `Roux2026` retained with a `note` | Crossref |
| **`AshokMurthy2017`** | author | **NO — the cited work is by neither person.** arXiv:1712.00885 is by **Henry Maxfield**, sole author. | `Maxfield, Henry` | arXiv:1712.00885 abs |
| | title | **NO** — `Worldline path integrals on AdS backgrounds` | `A view of the bulk from the worldline` | same |
| | eprint, year | yes (1712.00885, 2017) | unchanged | same |
| **`CorradiniMuratori2020`** | author | **NO** — `Corradini, Roberto` / `Muratori, Luca` | `Corradini, Olindo` / `Muratori, Maurizio` | arXiv:2006.02911 abs; `PAPER-2026-024.json` |
| | title | **NO** — `Worldline Monte Carlo on D-hyperboloids` | `A Monte Carlo Approach to the Worldline Formalism in Curved Space` | same |
| | journal | **MISSING** | JHEP **11** (2020) 169; DOI `10.1007/JHEP11(2020)169` | same |
| **`ZouMilstedVidal2020`** | title | **NO** — `Boundary operators in MERA` | `Conformal Fields and Operator Product Expansion in Critical Quantum Spin Chains` | arXiv:1901.06439 abs |
| | volume/pages/doi/eprint | **MISSING** (journal named, nothing else) | PRL **124**, 040604; `10.1103/PhysRevLett.124.040604`; arXiv:1901.06439 | same |
| | author, journal, year | yes — Zou, Milsted, Vidal, PRL, 2020 | unchanged | same |
| **`Quantinuum2026`** | author | **NO** — `{Quantinuum}` (corporate stand-in) | `Dasu, Shival and DeCross, Matthew and Guo, Andrew Y. and Lavasani, Ali and others` (45 authors) | arXiv:2602.22211 abs; `PAPER-2026-081.json` |
| | title | **NO** — `94 logical qubits beyond break-even with iceberg error codes` | `Computing with many encoded logical qubits beyond break-even` | same |
| | eprint, year | yes (2602.22211, 2026) | unchanged; `primaryClass = quant-ph` added | same |
| **`Anand2023`** | author | **NO** — `Anand, Natalie and others` | `Anand, Sajant and Hauschild, Johannes and Zhang, Yuxuan and Potter, Andrew C. and Zaletel, Michael P.` | arXiv:2203.00886 abs; `PAPER-2026-017.json` |
| | title | **NO** — `MERA on a Trapped-Ion Quantum Computer` | `Holographic quantum simulation of entanglement renormalization circuits` | same |
| | volume/pages/doi/eprint | **MISSING** | PRX Quantum **4**, 030334; `10.1103/PRXQuantum.4.030334`; arXiv:2203.00886 | same |
| | journal, year | yes — PRX Quantum, 2023 | unchanged | same |
| **`Rosenfeld2025`** | author | **NO — no author named Rosenfeld exists on this paper.** | `Mitchener, Ludovico and Yiu, Angela and Chang, Benjamin and others` (37 authors) | arXiv:2511.02824 abs |
| | title | **NO** — `Kosmos: Autonomous scientific discovery with multi-agent AI` | `Kosmos: An AI Scientist for Autonomous Discovery` | same |
| | eprint, year | yes (2511.02824, 2025) | unchanged; `primaryClass = cs.AI` added | same |
| **`Wang2026SciSciGPT`** | author | **NO** — `Wang, Dashun and others`. Dashun Wang is the **last** author, not the first. | `Shao, Erzhuo and Wang, Yifang and Qian, Yifan and Pan, Zhenyu and Liu, Han and Wang, Dashun` | Crossref 10.1038/s43588-025-00906-6 |
| | title | **NO** — `SciSciGPT: A multi-agent system for science of science research` | `SciSciGPT: advancing human--AI collaboration in the science of science` | same |
| | volume/pages/doi | **MISSING** | Nat. Comput. Sci. **6**, 301--315; `10.1038/s43588-025-00906-6` | same |
| | journal, year | yes (Nature Computational Science; March 2026 issue) | unchanged | same |
| **`Sun2026`** | author | **NO — no author named Sun exists on this paper.** | `Hao, Qianyue and Xu, Fengli and Li, Yong and Evans, James` | Crossref 10.1038/s41586-025-09922-y |
| | title | **NO** — `AI tools expand individual scientific impact but contract collective exploration` | `Artificial intelligence tools expand scientists' impact but contract science's focus` | same |
| | volume/pages/doi/eprint | **MISSING** | Nature **649**, 1237--1243; `10.1038/s41586-025-09922-y`; arXiv:2412.07727 | same + arXiv listing |
| | journal, year | yes (Nature, 2026) | unchanged | same |
| **`EvenblyVidal2010`** | title | **NO** — `Quantum criticality with the multi-scale entanglement renormalization ansatz` is a **different Evenbly--Vidal work** (2013 Springer chapter, arXiv:1109.5334). | `Entanglement renormalization in noninteracting fermionic systems` — the title that actually belongs to the DOI/volume/page in the entry | Crossref 10.1103/PhysRevB.81.235102; arXiv:0710.0692 |
| | author/journal/volume/pages/year/doi | yes — Evenbly & Vidal, PRB 81, 235102 (2010) | unchanged; arXiv:0710.0692 added | same |
| **`HauruDamleVidal2021`** | author | **NO** — `Vidal, Guifr\'e` is not an author; the key also mis-spells Van Damme as "Damle" | `Hauru, Markus and Van Damme, Maarten and Haegeman, Jutho` | local PDF `research/downloads/2007.03638.pdf` p.1; Crossref 10.21468/SciPostPhys.10.2.040 |
| | title/journal/volume/pages/year/doi | yes — SciPost Phys. 10, 040 (2021) | unchanged; `number = 2` and arXiv:2007.03638 added | same |

### 1.2 Entries that were already correct

| Key | Fields checked | Verdict | What changed | Primary source |
|---|---|---|---|---|
| `Vidal2007` | author, title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = cond-mat/0512165` | arXiv abs + Crossref 10.1103/PhysRevLett.99.220405 |
| `Swingle2012` | author, title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 0905.1317` | arXiv abs + Crossref 10.1103/PhysRevD.86.065007 |
| `RyuTakayanagi2006` | author, title, journal, vol, pages, year, doi | **OK** (title is the arXiv form; the published PRL title is the expanded "…from the anti-de Sitter Space/Conformal Field Theory Correspondence") | ENRICHED: `eprint = hep-th/0603001` | arXiv abs + Crossref 10.1103/PhysRevLett.96.181602 |
| `EvenblyVidal2011` | author, title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 1106.1082` | arXiv abs + Crossref 10.1007/s10955-011-0237-4 |
| `WangHe2025` | author, title, eprint, year | **OK** | ENRICHED: `primaryClass`, `note` (no journal ref as of 2026-08-17) | local PDF `research/downloads/2501.03084.pdf` p.1; arXiv abs; `PAPER-2026-010.json` |
| `WangHe2026` | author, title, eprint, year | **OK** | none | local PDF `research/downloads/2603.07639.pdf` p.1; `PAPER-2026-088.json` |
| `DiFrancesco1997` | author, title, publisher, year | **OK** | ENRICHED: series, address, `doi = 10.1007/978-1-4612-2256-9` | publisher record |
| `Hayden2016` | author (all six), title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 1601.01694` | arXiv abs + Crossref 10.1007/JHEP11(2016)009 |
| `Vasseur2019` | author (all four), title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 1807.07082` | arXiv abs + Crossref 10.1103/PhysRevB.100.134203 |
| `NocedalWright2006` | author, title, edition, publisher, year | **OK** | ENRICHED: series, address, `doi = 10.1007/978-0-387-40065-5` | publisher record |
| `OBrienFendley2018` | author, title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 1712.06662` | arXiv abs + Crossref 10.1103/PhysRevLett.120.206403 |
| `PfeiferEvenblyVidal2009` | author, title, journal, vol, pages, year, doi | **OK** | ENRICHED: `eprint = 0810.0580` | local PDF `research/downloads/0810.0580.pdf` p.1 |

### 1.3 Entries added (audit §4.1, §4.2, §4.4)

| Key | Reference | Why it is load-bearing | Primary source |
|---|---|---|---|
| `IoHuangHsieh2026` | Io, Huang & Hsieh, *Non-Hermitian free-fermion critical systems and logarithmic conformal field theory*, arXiv:2602.02649 [cond-mat.str-el], v1 2026-02-02 | **The prior art that failed the §8 gate for the Yang-Lee claim.** Non-Hermitian critical chain, biorthogonal pairing, Koo-Saleur modes named, true negative *c*. Posted 6 months 9 days before SIM-2026-071. It is reference [24] of PAPER-133, which this project read in full. | arXiv abs (RIKEN-iTHEMS-Report-26) |
| `CouvreurJacobsenSaleur2017` | Couvreur, Jacobsen & Saleur, *Entanglement in non-unitary quantum critical spin chains*, PRL **119**, 040601 (2017), arXiv:1611.08506 | **Second, independent kill.** Lattice measurement of a negative true *c* alongside the positive `c_eff` of the same model; the introduction names this project's exact headline pair for Yang-Lee. Nine years prior, in PRL. | arXiv abs |
| `MilstedVidal2017` | Milsted & Vidal, *Extraction of conformal data in critical quantum spin chains using the Koo-Saleur formula*, PRB **96**, 245105 (2017), arXiv:1706.01436 | Publishes the estimator this project's whole Koo-Saleur pipeline uses, its Eq. (22) contamination fix (the CLM-027 "novelty"), and *c* for Ising and 3-state Potts. | arXiv abs |
| `ZouMilstedVidal2018` | Zou, Milsted & Vidal, *Conformal data and renormalization group flow in critical quantum spin chains using periodic uniform matrix product states*, PRL **121**, 230402 (2018), arXiv:1710.05397 | Publishes *c* for Ising and the O'Brien-Fendley tricritical point — the remaining rung of the C_TTT ladder. | arXiv abs |
| `MilstedVidal2018` | Milsted & Vidal, *Geometric interpretation of the multi-scale entanglement renormalization ansatz*, arXiv:1812.00529 | States that MERA on the real line is a light sheet and that "MERA describes neither the hyperbolic plane nor de Sitter spacetime". Any geometric reading in the manuscript must answer it. | arXiv abs |
| `Bao2015` | Bao, Cao, Carroll, Chatwin-Davies, Hunter-Jones, Pollack & Remmen, *Consistency conditions for an AdS/MERA correspondence*, PRD **91**, 125036 (2015), arXiv:1504.06632 | The published AdS/MERA **no-go**. A PRD referee in the gauge/gravity section will know it. | arXiv abs |

---

## 2. The three errors that are worse than "a wrong given name"

The audit framed D-4 as wrong given-names and wrong titles. Three entries are a
different and more serious kind of error, because the **person named is not an
author of the cited work at all**:

1. **`AshokMurthy2017`** — arXiv:1712.00885 is **Henry Maxfield**, *A view of the
   bulk from the worldline*. Ashok and Murthy's 2017 paper is *Stringy AdS₃ from
   the worldsheet* — a **worldsheet** (string) result, not a worldline
   path-integral result, and it does **not** support the claim the key is cited
   for. `paper-prd.tex:228` names "Ashok and Murthy 2017" **in the prose**, so
   fixing the `.bib` is not sufficient; the sentence must be corrected to
   "Maxfield 2017". The project's own catalogue record `PAPER-2026-012.json`
   carries the same wrong authorship and needs the same correction.
2. **`Rosenfeld2025`** — arXiv:2511.02824 has **no author named Rosenfeld**. First
   author is Ludovico Mitchener.
3. **`Sun2026`** — Nature 649, 1237 has **no author named Sun**. Authors are Hao,
   Xu, Li and Evans.

`KimSwingle2017` is a fourth of this kind (Swingle is not an author of
arXiv:1701.00050) and is the most consequential, because it is cited twice in the
manuscript, including at `paper-prd.tex:61` as the source of the
`l_AdS = 1/ln χ` architecture definition — the shared root the audit's §5.3 shows
sits on **both sides** of claims CLM-010 and CLM-016.

---

## 3. What was NOT changed, and why

- **No citation key was renamed.** `KimSwingle2017`, `AshokMurthy2017`,
  `HauruDamleVidal2021`, `Rosenfeld2025`, `Sun2026` and `Roux2026` are all now
  known misnomers. Renaming them would break `\cite` in a manuscript that is with
  PRD editors and that this task does not own. Each carries a `note` field and a
  header comment recording the discrepancy (§32: additive, not silent).
- **`research/submission-package/references.bib`,
  `research/submission-package/prd/references.bib`** — byte-identical copies of the
  pre-correction file (verified with `diff`, exit 0 on both). They are **out of
  scope for this task** (the human is handling the manuscript) and are therefore
  **still wrong**. They must be re-synced from `research/references.bib` before any
  resubmission or erratum.
- **`EvenblyVidal2010`** was re-titled to match its own DOI rather than
  re-pointed, because the entry is **uncited** in both `paper-prd.tex` and
  `paper-draft-scipost.tex`, so no manuscript context establishes which of the two
  Evenbly--Vidal works was intended. If the 2013 Springer chapter
  (arXiv:1109.5334) was meant, replace the entry rather than editing this one.
- **Koo & Saleur 1994 (hep-th/9312156)** — the parent of the entire Koo-Saleur
  estimator, flagged by audit §4.5 as an uncatalogued methodological parent — was
  **not added**, because it is outside the six additions this task enumerated.
  Recommended as a follow-up.

## 4. Process change (for the PRD response letter)

The failure mode was **bibliography entries written from memory rather than
transcribed from a source**, in a repository that already held the correct data:
`research/data/papers/` contradicted the `.bib` on `Anand2023`,
`BohraSivaramakrishnan2025`, `Roux2026`, `CorradiniMuratori2020`,
`SahayLukinCotler2025` and `Quantinuum2026` **before** this audit ran. The gate
that should have caught it is a cheap one.

Proposed standing rule: **no `.bib` entry may be created or edited without a
recorded primary-source check** (arXiv abs page, publisher page, or Crossref DOI
record), and every entry must carry a resolvable identifier (DOI or arXiv ID) so
the check is repeatable. 29 of 32 entries now carry an arXiv ID (up from 9) and 24
carry a DOI (up from 11); the three without an arXiv ID are the two books and the
Nature Computational Science article, all of which carry DOIs instead.
