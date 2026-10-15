# RESEARCH-DIRECTOR §8 novelty gate: trunk-paper claims C1, C2, C3

**Date run:** 2026-10-15 (queries 16:20-17:16 UTC = 11:20-12:16 CDT).
**Standard:** `docs/governance/RESEARCH-DIRECTOR.md` §8 (literature gate, derivation gate, prior-art gate), read
in full for this run; §6 (counterfactual novelty) and §7 (independence) used for the derivation gate.
**Target:** `docs/philosophy/TRUNK-PAPER-OUTLINE.md` §3, §4, §5, §6 and Limitations. The Limitations section says
the §8 gate "has NOT been run" and that "the paper claims no priority and presents §3 as an application". This file
is that gate.
**Role:** literature adversary. Where an equivalent statement exists, the default is "not new".
**Verdict vocabulary (as instructed):** PRIOR STATEMENT FOUND / PARTIAL PRIOR STATEMENT / NONE FOUND IN SEARCHED
SOURCES. "Novel" is never used as a verdict.
**Independence caveat (§7):** one agent, one session, gating an outline written inside the same project. The quotes
below are external and verbatim (PDF-extracted; ligatures normalized; elisions marked "..."). The judgement that a
quote states "the same idea in other words" is mine and should be checked against the texts by the author.

---

## 0. Verdicts up front

| Claim | Verdict | Strongest prior statement | Positioning (detail in §3.6, §4.6, §5.6) |
|---|---|---|---|
| **C1** state-functional argument | **PARTIAL PRIOR STATEMENT** | Premise, in the tensor-network setting: Singh, PRD 97, 026012 (2018), arXiv:1701.04778 §VI: *"The two MERAs are an equivalent representation of the state since the expectation value of any observable is equal in both representations."* Same argument form for dual representations: Huggett, SHPMP 59 (2017), arXiv:1509.06229 (duals indistinguishable "with respect to all observables", so the dual-specific radius is "indeterminate"). Logical core: the law of likelihood (Hacking 1965, as stated in Royall 1997, p. 3). | **Cite as background; present as an application.** No source found that draws C1's evidential conclusion for tensor-network geometry ("agreement measures ansatz fidelity"). The paper may state that conclusion as its applied formulation, attributed to the sources above. The Limitations wording ("presents §3 as an application") is confirmed, not relaxed. |
| **C2** dilemma | **PARTIAL PRIOR STATEMENT** | Each horn is stated before. Horn (i): Singh 2018 §VI (bulk states lifted from gauge-equivalent MERAs "are generally different", an "ambiguity ... due to the 'gauge freedom' inherent in tensor network representations"). The band: Qi, arXiv:1309.6282 (bulk geometry "determined by the boundary state and the mapping"). The ansatz caveat: Hyatt, Garrison, Bauer, PRL 119, 140502 (2017), arXiv:1704.01974 (*"the structure of the network - and hence the geometry - is largely fixed a priori by the choice of tensor network ansatz"*); Evenbly & Vidal, J. Stat. Phys. 145 (2011). | **May present as a contribution, with caveats.** The two-horned dilemma, as a delimitation of where evidence for operational geometry could live, was not found. Every horn must be cited to the sources above; horn (i) must be stated conditionally because it rests on the contested Invariance Principle (Jacobs 2021; Rovelli 2014); the "extended-state" objection already published as Singh's bond state must be answered. |
| **C3** method | **PARTIAL PRIOR STATEMENT** | Counterfactual novelty is severity condition (S-2) assessed before the data: Mayo & Spanos, BJPS 57 (2006) p. 329; also ICH E10 §1.5 "assay sensitivity"; Parker, Synthese 163 (2008) applies severity to simulation. The independence ledger is robustness/independence analysis: Stegenga & Menon, Phil. Sci. 84 (2017) (*"Robustness arguments require the confirming evidence to be independent"*); Parker, Phil. Sci. 78 (2011); Gueguen, Phil. Sci. 87 (2020). Holography precedent: Aharony et al., Phys. Rept. 323 (2000) §4.1.3 p. 121 (direct checks "determined by properties of the supergroup SU(2, 2\|4)"). | **Cite the tools as background; present the audited ledger as an application.** Gloss the two project labels as names for pre-data severity and robustness bookkeeping; neither label has prior scholarly use (searched). Add Stegenga & Menon's point that ontic independence is not sufficient. |

**Bottom line.** Nothing in C1-C3 clears a priority bar. The defensible contribution is the assembly and the worked,
audited case: C1 applied to a program whose "geometric" numbers were computed without a network, C2's horns stated
together as one dilemma, and C3's two tools applied quantitatively to an emergent-geometry program, including its own
retraction. That is Level 2 (method/application) under §5, and the paper should say so.

## 1. The claims, decomposed

Wording from the task statement, checked against the outline (§3 lines 69-78, §4 lines 90-99, §5 lines 113-116,
§6 lines 128-131, Limitations lines 245-251).

| ID | Sub-claim | Outline location |
|---|---|---|
| C1a | Premise: a quantity fixed by the boundary state rho alone takes the same value in every faithful representation of rho (MERA, MPS, exact vector). | §3 Claim |
| C1b | Inference: therefore no degree of agreement between such a quantity and a geometric formula can discriminate A (efficient representation) from B (operational geometry). | §3 Claim |
| C1c | Conclusion: such agreement measures ansatz fidelity, not bulk physics. | §3 Claim |
| C1d | Corollary: a matched control that swaps the representation cannot separate representations on an observable that never sees the representation. | §3 Move |
| C2a | Horn (i): a candidate observable for B must be invariant under the network's internal gauge freedom, else it is surplus structure. | §4 Claim |
| C2b | Horn (ii): it must be sensitive to the network's organisation, else it is a state functional (C1). | §4 Claim |
| C2c | Band: geometric content can live only in gauge-invariant joint functionals of (state, network). | §4 Claim |
| C2d | Caveat: even such quantities may be properties of the graph/ansatz (random-tensor-network results). | §8 Move; §7 outcome-3 row |
| C3a | Counterfactual novelty: the weight of an agreement depends on how many outcomes were possible before the run; symmetry- or definition-fixed agreements confirm the code. | §5 |
| C3b | Independence ledger: agreements among quantities derived from the same inputs are one result. | §6 |
| C3c | Application of C3a + C3b to emergent-geometry claims. | §5-§6 Move |

## 2. Search record (literature gate)

### 2.1 Protocol

- **arXiv export API, curl only**, `curl -sLG https://export.arxiv.org/api/query --data-urlencode search_query=...
  sortBy=relevance max_results=25` (id_list queries for known papers). Strictly sequential, 4 s apart (batches
  b1-b3), then 5 s apart with a 30 s back-off on HTTP 429 (b4-b9). Every response parsed for
  `opensearch:totalResults`. No OR queries. Rate limiting: HTTP 429 from 16:23:30Z to 16:29:04Z (11 failed requests,
  listed below); the three lost queries (A23, A24, ID_K3) were re-run successfully at 16:40Z, so no query line is
  missing from the record. The API indexes title, abstract and comments only, so body-text statements were sought by
  searching full texts (§2.6) and by INSPIRE full-text search (§2.3).
- **INSPIRE-HEP API** `fulltext:` queries (searches the body text of arXiv papers), sequential, 4 s apart.
- **OpenAlex** works search and title lookups (abstract reconstructed from OpenAlex's index), sequential, 3 s apart.
  **Crossref** for bibliographic verification.
- **Semantic Scholar** graph API: all 6 planned queries returned HTTP 429 three times each (unauthenticated pool,
  about 17:07-17:13Z). **Not searched.**
- **PhilSci-Archive** internal search: blocked by a bot check. WebFetch got "The requested URL was rejected"; curl
  got a JavaScript/CAPTCHA page; one headless-browser navigation (16:31:36Z) got "What code is in the image?". The
  check was not bypassed. **PhilPapers** search and **PhilArchive** record pages: HTTP 403. Substitute: web search
  restricted to those two domains (engine-ranked, not exhaustive; weaker than the archives' own search).
- **Web search** (WebSearch tool, standard mode), 31 queries, listed in §2.5.
- The paper-search MCP search tools were not used (query-blind, per CLAUDE.md and the task).
- Labels absent from the tables (for example A26, A27, A29) were planned and never run.

### 2.2 arXiv export API log (2026-10-15, times UTC)

| # | Time | Query | Hits | Relevant results (used in §3-§5 unless marked) |
|---|---|---|---|---|
| A01 | 16:20:01 | `abs:"tensor network" AND abs:"gauge freedom" AND abs:holographic` | 0 | none |
| A02 | 16:20:06 | `abs:"tensor network" AND abs:gauge AND abs:"emergent geometry"` | 1 | 2010.05960 (not relevant) |
| A03 | 16:20:10 | `abs:MERA AND abs:AdS AND abs:"consistency conditions"` | 0 | phrase is in Bao et al.'s title, not abstract; fetched by id (ID_K1) |
| A04 | 16:20:15 | `abs:"entanglement renormalization" AND abs:geometry AND abs:interpretation` | 5 | 1812.00529, 1106.1082, 1209.3304 |
| A05 | 16:20:19 | `abs:"kinematic space" AND abs:"tensor network"` | 9 | 1612.05698 |
| A06 | 16:20:24 | `abs:"tensor network" AND abs:"same state" AND abs:geometry` | 1 | 1804.04964 (Molnar et al.) |
| A07 | 16:20:28 | `abs:"exact holographic mapping"` | 9 | 1309.6282 (Qi) |
| A08 | 16:20:33 | `abs:"random tensor network" AND abs:"minimal cut"` | 6 | technical RTN papers; no C2 statement |
| A09 | 16:20:37 | `abs:"path integral geometry"` | 2 | 1812.00529 |
| A10 | 16:20:41 | `abs:"tensor network" AND abs:"not unique"` | 74 | top 25 unrelated (1805.00523 checked, not relevant) |
| ID_K1 | 16:21:02 | id_list 1504.06632, 1812.00529, 1106.1082, 1209.3304, 0905.1317, 1110.4872, 1601.01694, 1512.01548, 1505.05515, 1309.6282, 1701.04778, 1606.08444 | 12 | abstracts of core papers |
| ID_K2 | 16:21:07 | id_list 1807.02501, 1805.12524, 1612.05698, 1704.04229, 2102.02619, 1005.3035, 1006.0047, hep-th/9905111, 1805.00523, 1804.04964, 1411.0690, 1812.11644 | 12 | abstracts of core papers |
| A11 | 16:22:35 | `cat:physics.hist-ph AND abs:"tensor network"` | 1 | 1708.01525 (unrelated) |
| A12 | 16:22:41 | `cat:physics.hist-ph AND abs:"emergent spacetime" AND abs:entanglement` | 1 | 2608.26282 (De Haro, Cinti, Corbeel; background) |
| A13 | 16:22:46 | `cat:physics.hist-ph AND abs:holography AND abs:emergence` | 4 | 1501.04278, 1509.09231, 2608.26282 (background) |
| A14 | 16:22:50 | `cat:physics.hist-ph AND abs:"surplus structure"` | 8 | 1712.01228, 1904.04439 (contested surplus structure) |
| A15 | 16:22:55 | `cat:physics.hist-ph AND abs:gauge AND abs:tensor` | 13 | none on tensor networks |
| A16 | 16:23:00 | `abs:MERA AND abs:holographic AND abs:representation` | 8 | 1701.04778 (Singh), 1512.01548, 1812.11644 |
| A17 | 16:23:04 | `abs:"tensor network" AND abs:holographic AND abs:"gauge invariant"` | 7 | bulk-gauge-field papers (different sense of "gauge"); none states C2 |
| A18 | 16:23:08 | `abs:"geometry from entanglement"` | 4 | 2207.02225; none states C1 |
| A19 | 16:23:13 | `abs:"spacetime from entanglement"` | 2 | 2407.20458 (Adlam; background) |
| A20 | 16:23:17 | `abs:entanglement AND abs:distance AND abs:"tensor product structure" AND abs:emergent` | 0 | none |
| A21 | 16:23:22 | `ti:"spacetime as a quantum circuit"` | 1 | 2101.01185 (physics; background) |
| A22 | 16:23:26 | `abs:"Hilbert space fundamentalism"` | 6 | 2102.08620, 2401.01793 (Stoica; background) |
| A23 | 16:23:30 | `abs:MERA AND abs:"de Sitter"` | HTTP 429 | lost; 3 retries 16:24:51-16:25:52 also 429 |
| A24 | 16:23:35 | `abs:random AND abs:MERA AND abs:Haar` | HTTP 429 | lost; 3 retries 16:26:27-16:27:28 also 429 |
| ID_K3 | 16:28:03 | id_list (11 ids) | HTTP 429 | lost; retries 16:28:34, 16:29:04 also 429 |
| A25 | 16:29:39 | `abs:"tensor network" AND abs:"emergent geometry" AND abs:representation` | 0 | none |
| A28 | 16:29:45 | `abs:"conformal data" AND abs:MERA` | 6 | 1109.5334, 0810.0580 (benchmark practice) |
| A30 | 16:29:50 | `abs:"entanglement wedge" AND abs:"causal cone"` | 1 | 1704.04229 (Evenbly; background) |
| A33 | 16:29:55 | `abs:"tensor network" AND abs:"gauge transformation" AND abs:bulk` | 0 | none |
| A34 | 16:30:01 | `cat:physics.hist-ph AND abs:severity` | 431 | stemming noise ("sever-"); none relevant in top 25 |
| A35 | 16:30:07 | `cat:physics.hist-ph AND abs:robustness` | 37 | 2401.16323, 1812.07078, 2304.14591 |
| A36 | 16:30:13 | `cat:physics.hist-ph AND abs:"novel prediction"` | 2 | 2208.12890, 2501.06095 (background) |
| A37 | 16:30:18 | `cat:physics.hist-ph AND abs:simulation AND abs:confirmation` | 7 | 1811.03859 |
| A38 | 16:30:24 | `cat:physics.hist-ph AND abs:"black hole entropy" AND abs:derivations` | 1 | 1501.06162 (background) |
| A23 | 16:40:16 | re-run of A23 | 10 | 1110.4872, 1709.03513, 1611.08581, 1812.00529 |
| A24 | 16:40:21 | re-run of A24 | 0 | none |
| ID_K3 | 16:40:27 | id_list 2608.26282, 2407.20458, 2512.11967, 1904.04439, 1712.01228, 2102.08620, 2101.01185, 1501.04278, 1509.09231, 1510.07637, 2309.06436, 1509.06229, 1501.06162, 2401.16323, 1812.07078, 1811.03859 | 16 | abstracts |
| A40 | 16:40:32 | `abs:"tensor network" AND abs:"efficient representation" AND abs:holography` | 0 | none |
| A42 | 16:40:37 | `abs:"bulk geometry" AND abs:"tensor network" AND abs:gauge` | 0 | none |
| A47 | 16:40:43 | `abs:"emergent geometry" AND abs:operational` | 16 | none relevant |
| A48 | 16:40:48 | `abs:"Fisher information metric" AND abs:"tensor network" AND abs:gauge` | 1 | 1503.07699 (Molina-Vilaplana) |
| A51 | 16:40:55 | `abs:"bulk reconstruction" AND abs:MERA` | 1 | 2403.12086 (not relevant) |
| ID_K4 | 16:42:47 | id_list 2302.07897, 2102.00010, 1109.5334, 0810.0580, 1802.01040, 1010.6134, 2208.12890, 2501.06095, 2304.14591 | 9 | abstracts |
| A53 | 16:42:52 | `abs:"peaked-size teleportation"` | 1 | 2102.00010 |
| A54 | 16:42:57 | `cat:physics.hist-ph AND abs:"AdS/CFT" AND abs:confirmation` | 2 | 1810.00949 (Dardashti et al.) |
| A55 | 16:43:03 | `cat:physics.hist-ph AND abs:"tensor networks"` | 1 | 1708.01525 (unrelated) |
| A56 | 16:43:08 | `cat:physics.hist-ph AND abs:"quantum simulation" AND abs:gravity` | 0 | none |
| A58 | 16:43:13 | `abs:MERA AND abs:gauge` | 11 | 1702.00392, 2202.02138, 1407.6552; none states C2 |
| A61 | 16:43:19 | `abs:geometry AND abs:MERA AND abs:"variational parameters"` | 2 | 1106.1082, 1110.4872 |
| A63 | 16:43:24 | `ti:"entanglement renormalization" AND ti:holography` | 1 | 0905.1317 |
| ID_K5 | 16:51:02 | id_list 1308.5599, 2301.03522, 2308.00697, 1506.03512, 1208.3469, 1703.00456, 1706.07056, 2012.05247, 1902.10157, 2605.06780, 2606.30853, 2510.07017 | 12 | abstracts |
| A64 | 16:51:07 | `abs:"tensor network" AND abs:Weyl AND abs:"path integral"` | 0 | none |
| A65 | 16:51:12 | `abs:"path integral optimization"` | 22 | 1703.00456 family |
| A67 | 16:51:18 | `abs:"tensor network" AND abs:"bulk geometry" AND abs:ambiguity` | 0 | none |
| A68 | 16:51:23 | `abs:"tensor network" AND abs:geometry AND abs:redundancy AND abs:holographic` | 1 | 1510.03784 (not relevant) |
| A69 | 16:51:28 | `abs:"tensor network" AND abs:"gauge freedom" AND abs:geometry` | 0 | none |
| A70 | 16:51:34 | `abs:MERA AND abs:"not unique"` | 4 | unrelated |
| A71 | 16:52:33 | `ti:"Extracting entanglement geometry from quantum states"` | 1 | 1704.01974 (Hyatt et al.) |
| A72 | 16:52:38 | `abs:"tensor network" AND abs:"fixed a priori"` | 1 | 1704.01974 only |
| A73 | 16:52:44 | `abs:"entanglement geometry" AND abs:"tensor network" AND abs:ansatz` | 0 | none |
| ID_K6 | 16:58:08 | id_list 1701.00050, 2401.01793, 2207.02225, 1406.5859, 1612.05698 | 5 | abstracts |
| A74 | 16:58:14 | `abs:MERA AND abs:"matrix product state" AND abs:holographic` | 5 | none states C1 |
| A75 | 16:58:19 | `abs:"emergent geometry" AND abs:"matrix product state"` | 0 | none |
| A76 | 16:58:25 | `abs:holographic AND abs:"tree tensor network" AND abs:geometry` | 0 | none |
| A77 | 16:58:30 | `abs:"state-based" AND abs:"observable-based" AND abs:entanglement` | 0 | none |

### 2.3 INSPIRE-HEP full-text log (2026-10-15, UTC)

| # | Time | Query | Hits | Outcome |
|---|---|---|---|---|
| I01 | 17:01:44 | `fulltext:"state functional" and fulltext:"tensor network" and fulltext:MERA` | 3 | none relevant |
| I02 | 17:01:48 | `fulltext:"surplus structure" and fulltext:"tensor network"` | 2 | De Haro & Butterfield book arXiv:2508.01616: "tensor network" occurs only in a reference title (grep); no discussion |
| I03 | 17:01:53 | `fulltext:"gauge freedom" and fulltext:MERA and fulltext:"bulk geometry"` | 12 | 1701.04778 (Singh), 1612.05698; others technical |
| I04 | 17:01:58 | `fulltext:"faithful representation" and fulltext:MERA and fulltext:holographic` | 17 | none states C1 |
| I05 | 17:02:02 | `fulltext:"efficient representation" and fulltext:"emergent geometry" and fulltext:MERA` | 4 | none |
| I06 | 17:02:07 | `fulltext:"property of the state" and fulltext:MERA and fulltext:geometry` | 9 | 2605.23670 uses the phrase in another sense; none |
| I07 | 17:02:11 | `fulltext:"independent of the tensor network" and fulltext:holographic` | 3 | 2102.12023 (curvature coefficients "universal independent of the tensor network"; not C1) |
| I08 | 17:02:16 | `fulltext:"merely a representation" and fulltext:"tensor network"` | 2 | none |
| I09 | 17:05:55 | `fulltext:"gauge invariant" and fulltext:MERA and fulltext:"emergent geometry"` | 19 | none states C2 |
| I11 | 17:06:00 | `fulltext:"fixed by conformal symmetry" and fulltext:MERA and fulltext:holographic` | 6 | none |
| I12 | 17:06:04 | `fulltext:"does not discriminate" and fulltext:"tensor network"` | 14 | none |
| I13 | 17:06:09 | `fulltext:"cannot distinguish" and fulltext:MERA and fulltext:AdS` | 14 | none (1609.04645 uses it in another sense) |
| I14 | 17:06:13 | `fulltext:"geometry of the tensor network" and fulltext:"gauge transformation"` | 8 | 2510.13941 (Balasubramanian & Cummings) |
| I15 | 17:06:18 | `fulltext:"emergent geometry" and fulltext:"surplus"` | 8 | none |
| I16 | 17:06:23 | `fulltext:"severe test" and fulltext:holography` | 9 | none |
| I17 | 17:06:27 | `fulltext:"consistency check" and fulltext:"tensor network" and fulltext:"independent evidence"` | 4 | none |

### 2.4 OpenAlex, Crossref, Semantic Scholar (2026-10-15, UTC)

| # | Time | Query | Hits | Outcome |
|---|---|---|---|---|
| O01 | 17:13:32 | tensor networks emergent spacetime philosophy | 960 | no philosophy paper on tensor-network geometry in top 25 |
| O02 | 17:13:36 | surplus structure tensor network holography | 39 | none |
| O03 | 17:13:40 | MERA geometry interpretation representation holography critique | 13 | none |
| O04 | 17:13:44 | robustness independent evidence emergent spacetime holography | 678 | Dardashti, Thebault & Winsberg 2017 (already cited); none on tensor networks |
| O05 | 17:13:48 | severe testing computer simulation physics confirmation | 8053 | Katzav, SHPMP 44 (2013) |
| O06 | 17:13:52 | gauge invariance criterion physical reality surplus structure | 159 | Jacobs, Synthese 199 (2021); Gueguen 2019 thesis; Earman, Phil. Sci. (2004) |
| O07 | 17:13:56 | tensor network geometry philosophy of physics | 5882 | none |
| O08 | 17:14:00 | holography emergence tensor networks Synthese | 34 | Jaksland 2020; Vistarini 2016; Jaksland 2025 |
| O09 | 17:14:04 | spacetime from entanglement philosophy | 4890 | Jaksland 2025; Jaksland 2017 (PhilSci) |
| OT | ~17:15 | title lookups: Gueguen 2020; Jaksland 2017; Vistarini 2016; Katzav 2013; Jacobs 2021; Gueguen 2019 | 22/0/1/1/1/1 | abstracts for Gueguen 2020, Jacobs 2021, Gueguen 2019; none in OpenAlex for Vistarini, Katzav |
| CR1 | ~16:56 | Crossref: Jaksland "Spacetime from Entanglement" | 3 | DOI 10.31389/pop.219, *Philosophy of Physics* 3(1), 2025 (verified) |
| CR2 | ~17:00 | Crossref: Steele & Werndl "Climate models, calibration, and confirmation" | 2 | BJPS 64(3) 609-635 (2013), no abstract (bibliographic only) |
| S01-S06 | ~17:07-17:13 | Semantic Scholar (6 queries, mirroring O01-O06) | 429 | **not searched** |

### 2.5 Web search log (WebSearch tool, 2026-10-15, about 16:30-17:05 UTC; "links" = results returned)

| # | Query (domain filter) | Links | Outcome |
|---|---|---|---|
| W01 | `"tensor network" "surplus structure" holography` | 9 | no source uses "surplus structure" for tensor networks |
| W02 | `philsci-archive tensor networks emergent spacetime MERA philosophy` | 9 | physics only; no PhilSci paper |
| W03 | `Jaksland "Entanglement as the world-making relation" distance from entanglement tensor network` | 9 | Jaksland, Synthese 2020 located; tensor-network content not shown (not read) |
| W04 | `philosophy "tensor networks" "emergent geometry" representation gauge freedom holography paper` | 9 | Molina-Vilaplana JHEP 09 (2015) 002 (gauge invariance of a network-derived metric) |
| W05 | `tensor network holography emergent spacetime` (philsci-archive.pitt.edu) | 9 | no philosophy paper on tensor networks |
| W06 | `MERA tensor network geometry entanglement` (philpapers.org) | 9 | physics only |
| W07 | `spacetime from entanglement tensor networks Swingle Van Raamsdonk philosophy` (philsci-archive.pitt.edu) | 9 | Jaksland, "Spacetime from Entanglement" (PhilSci 27009 = arXiv:2607.09823) |
| W08 | `"quantum circuit" spacetime emergence holography Bain` (philsci, philpapers) | 10 | Bain 2013 (condensed-matter emergence); no Bain tensor-network paper |
| W09 | `Huggett "Target space ≠ space" T-duality ...` | 10 | arXiv:1509.06229 |
| W10 | `Parker "Computer simulation through an error-statistical lens" Synthese 2008 severe testing` | 10 | bibliographic; abstract then read on Springer |
| W11 | `Parker "When climate models agree: ..." Philosophy of Science 2011 abstract independence` | 10 | abstract then read on Cambridge Core |
| W12 | `"tensor network" holography bulk geometry "put in by hand" graph hyperbolic tiling input not emergent` | 9 | no explicit statement found by the engine |
| W13 | `philosophy of physics paper "tensor networks" holography emergence spacetime Synthese OR ...` | 9 | no philosophy paper |
| W14 | `holographic quantum error correction philosophy emergence of spacetime ...` | 9 | none on network geometry |
| W15 | `"wormhole" "quantum processor" Jafferis philosophy confirmation ...` | 9 | Weinstein 2023 (arXiv:2301.03522, 2308.00697) |
| W16 | `Royall 1997 "Law of Likelihood" ... Hacking 1965` | 9 | Royall ch. 1 scan (read) |
| W17 | `Mayo Spanos 2006 "Severe testing as a basic concept ..." severity principle` | 9 | PDF on errorstatistics.com (read) |
| W18 | `ICH E10 "assay sensitivity" ...` | 9 | FDA-hosted ICH E10 PDF (read) |
| W19 | `Earman 2004 "Laws, symmetry, and symmetry breaking" "genuine physical magnitude" gauge invariant quote` | 9 | **quote not verified** (Cambridge shows abstract only; PhilSci blocked) |
| W20 | `"tensor network" holography "property of the state" "not of the network" ...` | 10 | Hyatt, Garrison & Bauer, PRL 119, 140502 |
| W21 | `"any accurate" OR "any faithful" representation of the critical ground state MERA "Ryu-Takayanagi" ... critique` | 9 | none |
| W22 | `De Haro Butterfield "common core" "specific structure" duality schema bosonization ...` | 9 | arXiv:1707.06681 (read) |
| W23 | `Stegenga 2009 "Robustness, discordance, and relevance" abstract ...` | 9 | Cambridge Core abstract page |
| W24 | `Stegenga Menon 2017 "Robustness and independent evidence" ...` | 9 | Cambridge Core abstract page |
| W25 | `"counterfactual novelty" philosophy of science prediction confirmation` | 9 | **no prior use of the term**; use-novelty literature only |
| W26 | `"independence ledger" evidence robustness OR "consistency check" OR "same inputs"` | 10 | **no prior scholarly use of the term** (software audit logs only) |
| W27 | `severity "use-novelty" applied to holography OR "emergent spacetime" OR "tensor network" ...` | 9 | none; Jaksland 2025 nearest |
| W28 | `Alyssa Ney "From quantum entanglement to spatiotemporal distance" ...` | 10 | chapter located (OUP 2021, pp. 78-102); **text not read** |
| W29 | `"geometry from entanglement" critique "tensor product structure" presupposes locality ...` | 9 | Stoica arXiv:2401.01793 (background) |
| W30 | `tensor network holography "gauge-invariant" quantity depends on the network not only the boundary state ...` | 9 | Singh, McMahon & Brennen 1702.00392; none states C2 |
| W31 | `"surplus structure" emergent spacetime holography bulk "redundancy" philosophy ...` | 10 | De Haro, Cinti & Corbeel 2608.26282 (redundancy in holography); none on networks |

### 2.6 Full texts retrieved and searched (PDF to text, then searched for: representation, unique, same state, gauge,
variational, fixed a priori, by hand, any state, property of the state, independent of)

arXiv: 1504.06632 (Bao et al.), 1812.00529 and 1807.02501 (Milsted & Vidal), 1106.1082 (Evenbly & Vidal),
1512.01548 (Czech et al.), 1701.04778 (Singh), 1110.4872 (Beny), 1503.07699 (Molina-Vilaplana), 1006.0047 (Headrick),
hep-th/9905111 (Aharony et al.), 2102.02619 (Jahn & Eisert), 1802.01040 (Harlow), 1601.01694 (Hayden et al.),
1810.00949 (Dardashti et al.), 2607.09823 (Jaksland 2025), 1707.06681 (De Haro & Butterfield), 1509.06229 (Huggett),
1809.01197 (Van Raamsdonk), 1209.3304 and 0905.1317 (Swingle), 1704.01974 (Hyatt et al.), 1701.00050 (Kim &
Kastoryano), 2510.13941 (Balasubramanian & Cummings); search-only: 2508.01616, 2605.23670, 2102.12023, 2308.09758,
1711.07787, 1609.04645. Non-arXiv: Mayo & Spanos 2006 (PDF), Royall 1997 ch. 1 (scan), ICH E10 (FDA PDF), Springer
pages for Parker 2008 and Bain 2021 (abstracts), Cambridge Core pages for Parker 2011, Stegenga 2009, Stegenga &
Menon 2017 (abstracts).
These texts were keyword-searched with surrounding context read, not read cover to cover. Jahn & Eisert 2102.02619,
Harlow 1802.01040 and Beny 1110.4872 returned no passage bearing on C1-C3 beyond what is cited below.

## 3. C1: state-functional argument

### 3.1 Prior-art register (ranked by how much of C1 each states)

**P1-1. Singh, "Tensor network state correspondence and holography", Phys. Rev. D 97, 026012 (2018),
arXiv:1701.04778v2, §VI "Bulk entanglement vs boundary central charge", p. 10.** States C1a for gauge-equivalent MERAs:

> "This bond freedom is an intrinsic property of tensor network representations of quantum many-body states. The two
> MERAs are an equivalent representation of the state since the expectation value of any observable is equal in both
> representations."

and, in the same passage, the network-dependence that C2 builds on:

> "even though the two MERAs ... describe the same quantum many-body state, the two corresponding bulk states ... are
> generally different e.g. they have different entanglement."

Covers: C1a (same graph, different gauge only). Does not draw C1b or C1c; Singh treats the dependence as an ambiguity
to manage, not as an evidential point.

**P1-2. Molnar, Garre-Rubio, Perez-Garcia, Schuch, Cirac, "Normal projected entangled pair states generating the same
state", New J. Phys. 20, 113017 (2018), arXiv:1804.04964, abstract.**

> "The corresponding map is not one-to-one: different sets of tensors may generate the very same state."

Covers: C1a in its general form (non-uniqueness of the representation), as a theorem-level background fact.

**P1-3. The law of likelihood: Royall, *Statistical Evidence: A Likelihood Paradigm* (Chapman & Hall, 1997), ch. 1,
p. 3, attributing it to Hacking (1965).**

> "If hypothesis A implies that the probability that a random variable X takes the value x is pA(x), while hypothesis
> B implies that the probability is pB(x), then the observation X = x is evidence supporting A over B if and only if
> pA(x) > pB(x), and the likelihood ratio, pA(x)/pB(x), measures the strength of that evidence (Hacking, 1965)."

Covers: C1b's logic exactly. C1 says both hypotheses predict the agreement whenever the representation is accurate,
so the likelihood ratio is 1 and the agreement is not evidence for either. C1b is an instance of this law, not a new
inference rule.

**P1-4. Huggett, "Target space ≠ space", Stud. Hist. Phil. Mod. Phys. 59 (2017) 81-88, doi:10.1016/j.shpsb.2015.08.007,
arXiv:1509.06229.** Abstract:

> "the indistinguishability with respect to all observables, of models attributing radically different radii to
> space" ... "Since duals are physically equivalent yet disagree on the radius of target space, it follows that the
> radius is indeterminate between them."

Body, arXiv v1 p. 11: "Rather duals are indistinguishable with respect to all physical quantities represented by
observables."

Covers: the argument form of C1 (quantities shared by every representation cannot ground a geometric property that
the representations disagree on), in T-duality. Differs: the representations are dual theories, not tensor-network
encodings of one state, and the conclusion is indeterminacy of the property, not evidential non-discrimination.

**P1-5. De Haro & Butterfield, "A schema for duality, illustrated by bosonization" (2018), arXiv:1707.06681, §1.2.2,
p. 12.**

> "For the content of the theory will be taken to be based on the common core of the models"

Covers: the background view that physical content is what equivalent representations share. Background for C1; not
a statement of it.

**P1-6. Dardashti, Dawid, Gryb, Thebault, "On the empirical consequences of the AdS/CFT duality" (2018),
arXiv:1810.00949, abstract (instrumental use of AdS/CFT for quark-gluon plasma):**

> "In the latter context, we find that neither of the two duals are confirmed by the empirical data."

Covers: an analogous evidential conclusion in holography (successful use of a dual representation does not confirm
it). Not about tensor networks or state functionals.

**P1-7. Kobrin, Schuster, Yao, "Comment on 'Traversable wormhole dynamics on a quantum processor'" (2023),
arXiv:2302.07897, abstract;** and **Schuster et al., Phys. Rev. X 12, 031013 (2022), arXiv:2102.00010, abstract.**

> "(iii) the observed perfect size winding is in fact a generic feature of small-size, fully-commuting models"
>
> "peaked-size teleportation utilizes precisely the same type of quantum circuit as traversable wormhole teleportation,
> yet has a completely distinct microscopic origin: it relies upon the spreading of local operators under generic
> thermalizing dynamics and not gravitational physics." ... "distinguishing between generic and intrinsically
> gravitational scrambling dynamics"

Covers: the C1b logic used by physicists in a holography-adjacent setting (a signature produced under both readings is
not evidence for the gravitational one, so a discriminating observable is needed). Not about state functionals.

**P1-8. Practice of the MERA's originators: Evenbly & Vidal, "Quantum criticality with the multi-scale entanglement
renormalization ansatz" (arXiv:1109.5334), abstract;** and **Pfeifer, Evenbly, Vidal, Phys. Rev. A 79, 040301(R)
(2009), arXiv:0810.0580, abstract.**

> "The performance of the MERA is benchmarked for several critical quantum spin chains ... The extraction of accurate
> conformal data, such as scaling dimensions and operator product expansion coefficients ... is also illustrated."
>
> "Given a critical Hamiltonian on the lattice, this connection can be exploited to extract most of the conformal
> data of the CFT that describes the model in the continuum limit."

Covers: C1c as practice. Agreement with CFT data is already used as a benchmark of the ansatz. No argument offered.

**P1-9. Hyatt, Garrison, Bauer, "Extracting entanglement geometry from quantum states", Phys. Rev. Lett. 119, 140502
(2017), arXiv:1704.01974, abstract.**

> "Tensor networks impose a notion of geometry on the entanglement of a quantum system. ... Conventionally, the
> structure of the network - and hence the geometry - is largely fixed a priori by the choice of tensor network ansatz."

Covers: part of C1c (the network's geometry is an input of the ansatz) and C2d.

**P1-10. Czech, Lamprou, McCandlish, Sully: "Integral geometry and holography", arXiv:1505.05515, abstract; "Tensor
networks from kinematic space", JHEP 07 (2016) 100, arXiv:1512.01548, abstract.**

> "kinematic space: an auxiliary Lorentzian geometry whose metric is defined in terms of conditional mutual
> informations and which organizes the entanglement pattern of a CFT state"
>
> "We argue that in these settings MERA is best viewed as a discretization of the space of bulk geodesics rather than
> of the bulk geometry itself."

Covers: the geometry the MERA is found to match is built from boundary entropies, i.e. from state functionals. This
is consistent with C1 and is the clearest physics reason to expect a faithful MERA to agree with such a geometry; it
is not stated as an evidential point.

**P1-11 (the position C1 answers, cite carefully).** Swingle, Phys. Rev. D 86, 065007 (2012), arXiv:0905.1317. Abstract:
"The gross features of equal time correlation functions are also reproduced in this geometric framework." Body: "Further
evidence for the connection between entanglement renormalization and holography comes from the holographic
interpretation of the extra gravitational dimension in terms of energy scale in the gauge theory." Agreements are
offered there as evidence for the connection. Van Raamsdonk (arXiv:1809.01197, introduction) adds a physicist's
caveat: "it still not clear how closely the network geometries associated to these states are related to the actual
geometries in holographic models."

**UNVERIFIED, must be read before submission.** Ney, "From quantum entanglement to spatiotemporal distance", in
*Philosophy Beyond Spacetime* (OUP, 2021), pp. 78-102. A search-engine summary of its PhilArchive record says the
results "support only a weaker conclusion, that quantum entanglement facts are constrained by spatiotemporal distance
facts, not that they are the basis from which distance facts emerge." If the chapter argues this, it is a close
non-discrimination argument for entanglement-distance agreements (both directions of dependence predict them). The
text was not accessible (PhilArchive 403).

### 3.2 Searched and not found

No source in §2 states C1b or C1c for tensor-network geometry: that agreement between a representation-invariant
(state-functional) quantity and a geometric formula cannot discriminate "efficient representation" from "operational
network geometry", or that such agreement measures ansatz fidelity. Queries that would have found it: A06, A16, A25,
A40, A74-A75; I01, I04-I08, I12; O01-O03, O07; W20-W21.

### 3.3 Derivation gate (§8)

- C1a is fixed by definition: a state functional is a function of rho, and a faithful representation reproduces rho.
- C1b follows from C1a by the law of likelihood (P1-3), given the stated assumption that both hypotheses predict the
  agreement whenever the representation is accurate.
- So the argument has near-zero counterfactual novelty in the §6 sense: once the definition is accepted it could not
  have come out otherwise. Its non-trivial content is elsewhere: (i) the audit finding that specific project
  observables are state functionals (outline §3 evidence: `holographic_transport_16q.py:347`, AUDIT §3 row 1,
  FINAL-REPORT finding 4), which is an empirical matter about the program; and (ii) the scope assumption.
- **Scope caution the paper must state.** C1 does not touch the inference-to-best-explanation argument that the
  MERA's *efficiency* on critical states (log-depth, small chi, high fidelity) is itself evidence for a geometric
  reading. That efficiency is a property of the representation class relative to the state, not a state functional.
  Evenbly & Vidal (2011) is the relevant prior on it (structural properties "preconditioned by the geometry of the
  tensor network", P2-8). Without this caution a referee can call C1 a straw man.

### 3.4 Prior-art gate (§8)

Nearest prior work: Singh 2018 (C1a, tensor-network setting), Huggett 2017 (argument form, dualities), the law of
likelihood (logic). **What the paper does that they do not:** applies the representation-invariance premise to the
evidential evaluation of MERA-geometry claims, and documents a case in which every "geometric" number of a program was
a state functional computed on an exactly diagonalized chain with no network in the measurement.

### 3.5 Verdict

**C1: PARTIAL PRIOR STATEMENT.** Premise (P1-1, P1-2), logic (P1-3) and argument form (P1-4, P1-6, P1-7) are prior.
The tensor-network-specific evidential conclusion (C1b-c applied to emergent geometry) was not found in the searched
sources.

### 3.6 Positioning recommendation

Present §3 as an application, as the Limitations section already promises. Introduce the state-functional point as a
familiar consequence of representation non-uniqueness (Molnar et al. 2018; Singh 2018) combined with the law of
likelihood (Hacking 1965; Royall 1997), and note the parallel argument form in the dualities literature (Huggett 2017;
De Haro & Butterfield 2018; Dardashti et al. 2018) and in the wormhole-simulation debate (Schuster et al. 2022; Kobrin
et al. 2023). The paper's own contribution is the application: the classification of a real program's observables and
the corollary that a representation-swapping control cannot test them (C1d, the project's P1 kill). It may say that
the searched sources contain no statement of C1b-c for tensor-network geometry, citing this record, but must not call
the argument new, and must add the §3.3 scope caution about efficiency-based arguments. Read Ney (2021) first.

## 4. C2: the gauge-invariance / network-sensitivity dilemma

### 4.1 Prior-art register

**Horn (i), C2a: network-derived quantities must survive the network's gauge freedom.**

**P2-1. Singh 2018 (arXiv:1701.04778v2, §VI, p. 10).**

> "However, in order to compare bulk properties corresponding to different boundary states, one has to first address
> the ambiguity in defining the bulk state dual to a given ground state that arises due to the 'gauge freedom'
> inherent in tensor network representations."
>
> "A possible approach to compare bulk states corresponding to different boundary states is to average the bulk
> properties over all the different bulk states that are dual to the ground state." ... "It is also possible that the
> different bulk states, dual to a ground state, obtained here are related to one another by an unidentified
> (emergent) bulk symmetry, and are thus equivalent holographic duals of the ground state."

Covers: C2a in the tensor-network setting, with candidate remedies (orbit averaging, sampling, constraining the bond
freedom). Singh leaves the choice open. He also supplies the published form of the outline's own Limitations
objection: his "bond state" treats the network's internal legs as physical degrees of freedom of an extended lattice
(§I: "we view a tensor network as representing two different states by associating a many-body Hilbert space with the
tensor network in two different ways"). That is a close published analogue of the outline's "functional of the
Choi-type state the network produces": both promote network legs to physical degrees of freedom (Singh's lifting uses
copy tensors in a fixed bond basis, so it is not identical to a Choi state).

**P2-2. Molina-Vilaplana, "Information geometry of entanglement renormalization for free quantum fields", JHEP 09
(2015) 002, arXiv:1503.07699, abstract.**

> "We show how the geometrical description remains invariant despite there is an irreducible gauge freedom in the
> definition of the tensor network."

Covers: C2a applied (a network-derived metric, the Fisher metric of the cMERA flow, checked for gauge invariance) and
an instance of C2c (the metric depends on the intermediate-scale states the network defines, not on the boundary state
alone). Limits: invariance is shown for a restricted class of scale-dependent gauge transformations (body, section
"cMERA gauge invariance and Fisher metric").

**P2-3. Milsted & Vidal, "Tensor networks as path integral geometry", arXiv:1807.02501, p. 1;** and **"Geometric
interpretation of the multi-scale entanglement renormalization ansatz", arXiv:1812.00529, Discussion.**

> "However, a CFT path integral is invariant under local (Weyl) scale transformations. Hence requiring compatibility
> with a CFT path integral only determines the tensor network geometry up to a local scale factor Ω(τ, x). A unique
> geometry (up to a global scale factor, or choice of short distance cut-off aUV) can then be assigned by adding a
> second natural requirement, namely that the proper distance between nearest neighbor tensors be constant throughout
> the network."
>
> "a geometric assignment based on rule 1 of Ref. [47] alone only determines the conformal class of the metric gµν."

Covers: what the CFT data fix (a conformal class) versus what a network-level rule adds (the metric). Close to C2b-c:
the part of the geometry beyond the conformal class is set by a network convention, not by the state.

**P2-4. Caputa, Kundu, Miyaji, Takayanagi, Watanabe, Phys. Rev. Lett. 119, 071602 (2017), arXiv:1703.00456,
abstract.**

> "We optimize the background metric in the space on which the path integration is performed. ... For two-dimensional
> CFT vacua, we find the optimized metric is given by that of a hyperbolic space"

Covers: the same point from the path-integral side; the state leaves the metric free up to Weyl rescaling and an extra
criterion selects the hyperbolic one. Background for C2b-c.

**The band, C2c: geometry as a joint functional of state and network.**

**P2-5. Qi, "Exact holographic mapping and emergent space-time geometry", arXiv:1309.6282, abstract.**

> "By defining the distance in the bulk system from two-point correlation functions, we obtain an emergent bulk
> space-time geometry that is determined by the boundary state and the mapping."

Covers: C2c as a construction, in so many words. Does not address gauge freedom or what would make such a geometry
evidence for B.

**P2-6. Bao, Cao, Carroll, Chatwin-Davies, Hunter-Jones, Pollack, Remmen, Phys. Rev. D 91, 125036 (2015),
arXiv:1504.06632v2, §II.B "An AdS/MERA Correspondence?", pp. 8-9.**

> "In this work we take the term 'AdS/MERA correspondence' to mean more than simply a matching of graph geometry and
> continuous geometry." ... "A full AdS/MERA correspondence would then be a specification of these Hilbert spaces, as
> well as a prescription which makes use of the MERA to holographically map states and operators in Hboundary to
> corresponding states and operators in Hbulk and vice-versa."

Covers: C2b-c in physics language (matching is not enough; the network must do work as a map of states and
operators).

**P2-7. Kim & Kastoryano, "Entanglement renormalization, quantum error correction, and bulk causality", JHEP 04 (2017)
040, arXiv:1701.00050.** Abstract: "Entanglement renormalization can be viewed as an encoding circuit for a family of
approximate quantum error correcting codes." Body (re-read this session): "For scale invariant MERA, ν := − log2(Reλ1)
will be referred to as the scaling dimension." Its decoupling and recovery bounds scale as 2^(-ν(s - log2|A|)) (Eq. 4.5:
"R(ρAcR) − ρAAcR 1 ≤ C2−ν(s−log2 |A|)/2", norm bars lost in extraction).

Covers: the kind of network-sensitive observable the outline's §7 uses (recovery of operators pushed through the
network) is controlled by an eigenvalue of the MERA's own coarse-graining channel, which the authors call a scaling
dimension, i.e. by data tied to the CFT and the ansatz. A published instance of C2d's worry.

**The caveat, C2d: network-sensitive quantities may be graph or ansatz properties.**

**P2-8. Evenbly & Vidal, "Tensor network states and geometry", J. Stat. Phys. 145, 891-918 (2011), arXiv:1106.1082.**
Abstract:

> "argue that certain structural properties of the resulting many-body states are preconditioned by the geometry of
> the tensor network and are therefore largely independent of the choice of variational parameters."

§I: "...those structural properties (in practice, scaling of correlators and of entanglement entropy) that follow from
the way the tensors are connected into a network – and are therefore independent of the choice of variational
parameters." §II.C: "Several structural properties of the states that can be represented by the above tensor networks
are predetermined by the choice of geometry they reproduce".

Covers: C2d, stated by the MERA's originators in 2011.

**P2-9. Hyatt, Garrison, Bauer 2017 (P1-9 above),** plus body: "this circuit is not unique: an ambiguity arises since
the unitary can always be followed by a swap of the two sites or a single-site unitary while keeping the mutual
information the same". Covers C2d and, inside their construction, C2a.

**P2-10. Hayden, Nezami, Qi, Thomas, Walter, Yang, JHEP 11 (2016) 009, arXiv:1601.01694, abstract.** "When the bond
dimension of the tensors is large, we show that the entanglement entropy of boundary regions, whether connected or
not, obey the Ryu-Takayanagi entropy formula". Already the outline's source for C2d; background.

**P2-11. Balasubramanian & Cummings, "Diffeomorphism invariant tensor networks for 3d gravity", arXiv:2510.13941,
§1 and abstract.**

> "To make this match, the geometry of the tensor network is taken to be a discretization of a static slice of an AdS
> spacetime, the tensors are taken to be Haar random [3], and the dimension of the Hilbert spaces associated to the
> bulk legs is taken to be large. Despite matching the RT formula, tensor networks have other properties that are not
> found in generic states of quantum gravity."
>
> "standard constructions are not diffeomorphism invariant"

Covers: C2d (the RT match is engineered by choosing the graph) and a gravitational analogue of C2a.

**The premise behind horn (i) is contested (must be cited, not assumed).**

- **Jacobs, "Invariance or equivalence: a tale of two principles", Synthese 199 (2021) 9337-9357, abstract:** "the
  Invariance Principle, which states that quantities that vary under a theory's symmetries aren't physically real."
  ... "I argue that this is a mistake: Leibniz Equivalence and the Invariance Principle are orthogonal to each other.
  This means that it is possible to hold that symmetry-related models represent the same state of affairs whilst
  having a realist attitude towards variant quantities."
- **Rovelli, "Why gauge?", Found. Phys. 44 (2014) 91-104, arXiv:1308.5599, abstract:** "I suggest that gauge is more
  than mathematical redundancy. Gauge-dependent quantities can not be predicted, but there is a sense in which they
  can be measured."
- **Nguyen, Teh, Wells, "Why surplus structure is not superfluous", arXiv:1712.01228 (BJPS), abstract:** "The idea
  that gauge theory has 'surplus' structure poses a puzzle: in one much discussed sense, this structure is redundant;
  but on the other hand, it is also widely held to play an essential role in the theory."
- **Bradley & Weatherall, Found. Phys. (2020), arXiv:1904.04439, abstract:** the sense of "surplus structure" in that
  criterion is "importantly different from---and in a sense, opposite to---another sense of 'surplus structure' used by
  philosophers."
- Earman, Phil. Sci. 71 (2004), doi:10.1086/428016, is commonly cited for "genuine physical magnitudes" being gauge
  invariant. **UNVERIFIED:** the text was not accessible in this run.

### 4.2 Searched and not found

No source states the two requirements together as a dilemma for the operational reading of network geometry, or the
claim that evidence for that reading can live only in gauge-invariant joint functionals of (state, network). Queries:
A01, A02, A17, A33, A42, A58, A67-A69; I03, I09, I14, I15; O02, O03, O06; W01, W04, W30, W31.

### 4.3 Derivation gate (§8)

- Given (P) the Invariance Principle and C1, the band claim C2c follows by elimination: a discriminating observable can
  be neither gauge-variant (P) nor a function of rho alone (C1), so it is a gauge-invariant quantity that is not a state
  functional, which is what "joint functional of (state, network)" names. C2a-c are therefore analytic given P and C1;
  counterfactual novelty near zero.
- C2d is an empirical possibility already stated in P2-8 to P2-11, and illustrated in the project by HYP-033 (outcome
  4, Level 2: optimized MERA indistinguishable from Haar networks on the same graph at chi = 6).
- Two weak points, both prior-art-visible. (1) P is contested (Jacobs 2021; Rovelli 2014). (2) Singh's bond state (P2-1)
  shows that a network-sensitive quantity can be rewritten as a functional of an extended state the network defines.
  Then C2's dichotomy is relative to which state counts as "the" state; the outline's Limitations already flags this
  as the most likely referee objection, and the literature confirms it is a live one.

### 4.4 Prior-art gate (§8)

Nearest prior work: Singh 2018 (gauge ambiguity of network-derived bulk states; the extended bond state), Qi 2013
(geometry determined by state and mapping), Bao et al. 2015 (matching is not a correspondence), Evenbly & Vidal 2011
and Hyatt et al. 2017 (geometry preconditioned or fixed by the ansatz), Molina-Vilaplana 2015 (a gauge-invariant
network-derived metric). **What the paper does that they do not:** puts the two requirements together as a dilemma
with an explicit evidential role (where discriminating evidence for B could possibly live), uses the project's own
C_sigma_sigma_eps = 0.5075 to show the band is not empty yet still fails non-derivability, and reports one registered
test inside the band (HYP-033).

### 4.5 Verdict

**C2: PARTIAL PRIOR STATEMENT.** Each horn, the band, and the ansatz caveat have prior statements (P2-1 to P2-11).
The dilemma as a combined, evidentially framed argument was not found in the searched sources.

### 4.6 Positioning recommendation

The paper may present the dilemma as its contribution, with three caveats written into §4. (a) Attribute each part:
gauge ambiguity of network-derived quantities to Singh (2018) and Molina-Vilaplana (2015); the conformal-class versus
metric split to Milsted & Vidal (2018) and Caputa et al. (2017); the joint state-network geometry to Qi (2013) and Bao
et al. (2015); the ansatz caveat to Evenbly & Vidal (2011), Hyatt et al. (2017), Hayden et al. (2016) and Kim &
Kastoryano (2017). Phrase it as "we make explicit a dilemma whose horns are each recognized in the literature", not
"we introduce a criterion". (b) State horn (i) conditionally, "if gauge-variant network structure is surplus", and cite
Jacobs (2021), Rovelli (2014), Nguyen, Teh & Wells and Bradley & Weatherall for the contested status of the
Invariance Principle; do not cite Earman for a verbatim claim until the text is checked. (c) Answer the extended-state
objection in §4 by engaging Singh's bond-state construction directly, since it is the published version of the
outline's own Limitations worry.

## 5. C3: counterfactual novelty and the independence ledger

### 5.1 Prior-art register: C3a, counterfactual novelty

**P3-1. Mayo & Spanos, "Severe testing as a basic concept in a Neyman-Pearson philosophy of induction", Brit. J. Phil.
Sci. 57 (2006) 323-357, p. 329.**

> "A statistical hypothesis H passes a severe test T with data x0 if, (S-1) x0 agrees with H, and (S-2) with very high
> probability, test T would have produced a result that accords less well with H than x0 does, if H were false"

Covers: C3a. "How many outcomes were genuinely possible before the run?" is (S-2) asked before the data: if symmetry
fixes the outcome, the probability of a worse fit under "H false" is zero and the severity is zero. The outline already
says this (§5: "Mayo's severity applied before the data").

**P3-2. ICH E10, "Choice of control group and related issues in clinical trials" (ICH 2000; FDA guidance May 2001),
§1.5.**

> "Assay sensitivity is a property of a clinical trial defined as the ability to distinguish an effective treatment
> from a less effective or ineffective treatment."

Covers: the same requirement, named in another field. This closes an item the project's own challenger left
UNVERIFIED (`research/data/audit/valuable-questions-2026-09-14/research-challenge.md:202-210`).

**P3-3. Parker, "Computer simulation through an error-statistical lens", Synthese 163(3) (2008) 371-384, abstract.**

> "After showing how Deborah Mayo's error-statistical philosophy of science might be applied to address important
> questions about the evidential status of computer simulation results, I argue that an error-statistical perspective
> offers an interesting new way of thinking about computer simulation models and has the potential to significantly
> improve the practice of simulation model evaluation."

Covers: severity applied to simulation results in general (the task's "severity applied to physics simulations"; the
abstract names no particular physics domain). Also located, title and bibliography only, not read: Katzav, "Severe
testing of climate change hypotheses", SHPMP 44(4) (2013) 433-441; Steele & Werndl, "Climate models, calibration,
and confirmation", BJPS 64(3) (2013) 609-635.

**P3-4. Holography's own version: Aharony, Gubser, Maldacena, Ooguri, Oz, "Large N field theories, string theory and
gravity", Phys. Rept. 323 (2000) 183-386, arXiv:hep-th/9905111v3, §4.1.3, p. 121.**

> "In the correspondence between string theory on AdS5 × S5 and d = 4 N = 4 SYM theories, some of the most direct
> checks, such as protected operator dimensions and the functional form of two- and three-point functions, are
> determined by properties of the supergroup SU(2, 2|4). Many of the normalizations of two- and three-point functions
> which have been computed explicitly are protected by non-renormalization theorems. And yet, we are inclined to
> believe that the correspondence is a fundamental dynamical principle, valid independent of group theory and the
> special non-renormalization properties of N = 4 supersymmetry."

and §4.2, p. 129: "A conservative form of the AdS/CFT correspondence would be to say that classical supergravity
captures the large N asymptotics of some quantities in field theory which are algebraically protected against
dependence on the 't Hooft coupling."

Covers: C3a's point inside holography, from its founders: symmetry-fixed agreements support only the conservative
claim. Not formalized as an outcome count.

**P3-5. Headrick, Phys. Rev. D 82, 126010 (2010), arXiv:1006.0047, abstract.** "For a single interval, the EREs are
known for a general CFT; we reproduce them using gravity. For two intervals, the RT formula predicts a phase transition
..." Covers: C3a as implicit practice (the universal case is reproduced; the discriminating case is elsewhere).

**P3-6. Kobrin et al. 2023 and Schuster et al. 2022 (P1-7).** A generic signature is not a test of the gravitational
reading; covers C3a in a holographic quantum simulation.

### 5.2 Prior-art register: C3b, the independence ledger

**P3-7. Stegenga & Menon, "Robustness and independent evidence", Phil. Sci. 84(3) (2017) 414-435, abstract.**

> "Robustness arguments hold that hypotheses are more likely to be true when they are confirmed by diverse kinds of
> evidence." "Robustness arguments require the confirming evidence to be independent." "We identify two kinds of
> independence appealed to in robustness arguments:" "ontic independence (OI)—when the multiple lines of evidence
> depend on different materials, assumptions, or theories" "and probabilistic independence." "However, we argue that,
> as typically construed, OI is not a sufficient independence condition" "for warranting robustness arguments."

Covers: C3b's core claim, and a caution. The ledger in RESEARCH-DIRECTOR §7 classifies comparisons by shared raw data,
assumptions, code and state preparation, i.e. by ontic independence. Stegenga & Menon show that this is necessary, not
sufficient.

**P3-8. Parker, "When climate models agree: the significance of robust model predictions", Phil. Sci. 78(4) (2011)
579-600, abstract.**

> "This article identifies conditions under which robust predictive modeling results have special epistemic
> significance" ... "When today's climate models agree that an interesting hypothesis about future climate change is
> true" "it cannot be inferred—via the arguments considered here anyway—that the hypothesis is likely to be true" "or
> that scientists' confidence in the hypothesis should be significantly increased"

Covers: C3b for agreeing models, the closest philosophy-of-simulation precedent.

**P3-9. Gueguen, "On robustness in cosmological simulations", Phil. Sci. 87(5) (2020) 1197-1208, abstract;** and
**Gueguen, *On Separating the Wheat from the Chaff: Surplus Structure and Artifacts in Scientific Theories*, PhD thesis,
Western University (2019), abstract.**

> "I argue that robustness analysis is not a sufficient criterion for the trustworthiness of cosmological simulations."
>
> "for them to play a useful role in generating knowledge, we need to distinguish reliably between real predictions and
> artifacts. I argue that robustness analysis fails to fulfill this task. I propose in its place another methodology,
> that of crucial simulations."

Covers: C3b for physics simulations, plus a "crucial simulation" proposal that parallels the outline's push from
agreements to a discriminating observable (§4, §7). The thesis also joins surplus structure and artifacts in one
project, which bears on C2a.

**P3-10. Stegenga, "Robustness, discordance, and relevance", Phil. Sci. 76(5) (2009) 650-661, abstract:** "Despite the
frequency of appeals to robustness, the notion itself has received scant critique." Already cited in the outline (§6
Caution).

**P3-11 (nuance against over-claiming). Doboszewski & Elder, "Robustness and the Event Horizon Telescope: the case of
the first image of M87*", arXiv:2401.16323 (2024), abstract.**

> "We argue that it takes the form of a robustness argument, with the resulting image being robust across variation in
> a range of data-analysis pipelines." ... "even in cases -- like the EHT -- where these inferences are based on
> experiments that are (for all practical purposes) unique."

Covers: agreement across analyses of one dataset can still add reliability (against pipeline artifacts). C3b's "one
result" is right about evidence for the hypothesis but should not be read as "worthless"; the outline's §7 already
says "Do not discard such agreements. Describe them correctly."

Wimsatt (1981), cited in the outline, was not read in this run (page range still unresolved there).

### 5.3 Prior-art register: C3c, application to holography and emergent spacetime

- **Jaksland, "Spacetime from Entanglement: The Emergence of Metric, Gravity, or Topology", *Philosophy of Physics*
  3(1) (2025), doi:10.31389/pop.219, arXiv:2607.09823, abstract:** "these results are not about the same spatiotemporal
  aspects. They can therefore not just be grouped as evidence for one unanimous conclusion" ... "none of the emergence
  claims satisfies the determination condition: More than entanglement is needed to furnish the emergence basis."
  Closest prior application of evidential discipline to emergent-geometry claims; it concerns heterogeneity of claims
  and the emergence basis, not shared inputs or outcome counts, and it does not discuss tensor networks (search of
  the full text: no "tensor network", no "MERA").
- **Dardashti, Dawid, Gryb, Thebault, arXiv:1810.00949**, body: "To what extent should we take confirmation of the
  theory by evidence to be suitably dual?" Bayesian confirmation applied to AdS/CFT; not to networks.
- **Gryb, Palacios, Thebault, "On the universality of Hawking radiation", BJPS (2021), arXiv:1812.07078, abstract:**
  "Our analysis is framed by the crucial distinction between robustness and universality." Robustness analysis
  applied to a quantum-gravity claim.
- **Crowther, Linnemann, Wuthrich, "What we cannot learn from analogue experiments", arXiv:1811.03859, abstract:** "As
  they must assume the physical adequacy of the modelling framework used to describe the inaccessible target system,
  arguments to the conclusion that analogue experiments can yield confirmation for phenomena in those target systems,
  such as Hawking radiation in black holes, beg the question." Related to C1 and C3 (confirmation that presupposes the
  representation's adequacy).
- **Weinstein, arXiv:2301.03522 and 2308.00697 (2023):** reliability and robustness of the learned-Hamiltonian
  wormhole experiment ("I remain skeptical about the efforts to address Kobrin et al.'s challenges").

**Terms.** "Counterfactual novelty" (W25) and "independence ledger" (W26) returned no prior scholarly use. They are
the project's labels for pre-data severity and ontic-independence bookkeeping.

### 5.4 Searched and not found; derivation gate

Not found: an explicit pre-run outcome count combined with an independence classification of agreements, applied to
tensor-network (or other) emergent-geometry claims. Queries: A34-A38, A54-A56; I16, I17; O04, O05; W25-W27.

Derivation gate: C3 is methodological; C3a and C3b follow directly from adopting severity and robustness analysis
(P3-1, P3-7), so they carry no counterfactual novelty of their own. The application's numbers (21 of 34 calculated
claims could not have come out otherwise; 4 load-bearing agreements of 24) are outputs of the project's internal audit
by AI agents, i.e. same-origin records in the §7 sense; no outside referee has checked them (outline Limitations).

### 5.5 Prior-art gate and verdict

Nearest prior work: Mayo & Spanos 2006 and Parker 2008 (severity for simulation), Stegenga & Menon 2017, Parker 2011
and Gueguen 2020 (independence and robustness for agreeing models), Aharony et al. 2000 (symmetry-fixed checks in
holography), Jaksland 2025 (evidential discipline for emergent-spacetime claims). **What the paper does that they do
not:** a quantified, claim-by-claim application of both tools to one emergent-geometry program, including the
program's own retraction of its headline number.

**C3: PARTIAL PRIOR STATEMENT.** The tools are established; holography already knows the symmetry-fixed-check point;
the quantified application to tensor-network emergent geometry was not found in the searched sources.

### 5.6 Positioning recommendation

Cite the tools as background and present the ledger as an application. In §5, gloss "counterfactual novelty" as
pre-data severity (Mayo & Spanos 2006, condition S-2; Mayo 1996) and name the clinical-trial analogue (ICH E10 assay
sensitivity) and the simulation precedent (Parker 2008). Cite Aharony et al. (2000, §4.1.3) as evidence that the point
is familiar inside holography, which strengthens rather than weakens the paper's case. In §6, cite Stegenga & Menon
(2017) beside Stegenga (2009), say plainly that the ledger tracks ontic independence and that this is necessary, not
sufficient, and cite Parker (2011) and Gueguen (2020) as the simulation precedents and Doboszewski & Elder (2024) for
the limited value that same-input agreement still has. The paper may say that the searched sources contain no
quantified application of these tools to emergent-geometry claims, citing this record. It must not present the two
labels as new concepts.

## 6. Consequences for the outline (recommendations only; no other file edited)

1. **Limitations, "No theorem" bullet.** The gate has now been run. Replace "has NOT been run" with a pointer to this
   file and keep "presents §3 as an application": the gate supports it.
2. **§3.** Add Singh (2018) and Molnar et al. (2018) for the premise and Hacking (1965) / Royall (1997) for the
   likelihood logic; add Huggett (2017) as the parallel argument in the dualities literature; add the §3.3 scope
   caution (efficiency-based arguments for B are untouched by C1). Read Ney (2021) before drafting.
3. **§3 Move ("the familiar point that gauge-variant quantities are not physical").** This is the Invariance
   Principle, and it is contested. Cite Jacobs (2021) and Rovelli (2014); do not cite Earman (2004) for a quoted
   formulation until the text is checked.
4. **§4.** Cite Qi (2013) and Bao et al. (2015, §II.B) for the band; Singh (2018), Molina-Vilaplana (2015) and
   Milsted & Vidal (2018) for horn (i) and the conformal-class/metric split; Evenbly & Vidal (2011), Hyatt et al.
   (2017), Balasubramanian & Cummings (2025) and Kim & Kastoryano (2017) for the ansatz caveat. Answer the
   extended-state objection through Singh's bond state.
5. **§5.** Add ICH E10 §1.5 and Parker (2008); cite Aharony et al. (2000, §4.1.3 p. 121, §4.2 p. 129) as the
   holography precedent for symmetry-fixed checks.
6. **§6.** Add Stegenga & Menon (2017), Parker (2011), Gueguen (2020) and Doboszewski & Elder (2024). Wimsatt (1981)
   is still unread.
7. **§2.** Jaksland's 2020 paper is already cited; add Jaksland (2025), *Philosophy of Physics* 3(1) (verified via
   Crossref), whose "determination" and "novelty" conditions for emergence are close cousins of the paper's §5, and
   Bain, "The RT formula and its discontents: spacetime and entanglement", Synthese 198(12) (2021) 11833-11860
   (abstract read: "a 'state-based' approach ... and an 'observable-based' approach", relevant to §3's state-versus-
   representation framing; full text not read). Adlam, *Philosophy of Physics* 2(1) (2024), arXiv:2407.20458, is
   optional background.
8. **References block.** All additions above must go through the same Crossref/arXiv verification as the
   2026-10-08 list before they are cited (outline citation rule).

## 7. Limits of this gate, and what is still UNVERIFIED

- **Not searched:** Semantic Scholar (HTTP 429), PhilSci-Archive's own search (bot check, not bypassed), PhilPapers and
  PhilArchive (HTTP 403), Google Scholar (only reachable through the query-blind paper-search MCP, excluded), JSTOR,
  Web of Science. The philosophy side therefore rests on domain-filtered web search, OpenAlex, INSPIRE (physics full
  text) and arXiv physics.hist-ph, which together cover the main journals' metadata but not their full text.
- **Not read (cited or located only):** Earman (2004); Redhead (1975); Wimsatt (1981); Mayo (1996, the book; the 2006
  paper was read); Hacking (1965, seen through Royall); Ney (2021); Katzav (2013); Steele & Werndl (2013); Vistarini
  (2016); Jaksland (2020); Bain (2021) beyond its abstract; Nguyen, Teh & Wells and Bradley & Weatherall beyond their
  abstracts.
- **Quote check.** After writing, 69 quoted fragments were machine-checked against the downloaded source texts
  (whitespace, ligatures, quote marks and dash variants normalized): 68 matched exactly; the 69th (Singh, "inherent")
  differs only by a PDF line-break hyphenation ("in- herent"). Royall's law was checked on its key clause (the scan's
  OCR garbles the subscripts).
- **Abstract text obtained through a summarizing fetch tool, not a raw download, and therefore not machine-checked:**
  Parker (2011), Stegenga (2009), Stegenga & Menon (2017). The wording matched across sentences and with search
  snippets, but should be re-checked against the published page before quoting in the paper.
- **Citation trails** were followed only in part (Singh to McMahon et al. and Singh, McMahon & Brennen; Jaksland 2025
  to Bain 2021; Kobrin et al. to Schuster et al.). References-of-references were not systematically walked, which §8
  asks for.
- **Same-origin judgement.** Whether a quoted passage states "the same idea in other words" is my reading. A
  different reader could rate Huggett (2017) as a full prior statement of C1's argument form, or rate the C2 horns as
  too scattered to count against the dilemma. The quotes are given so the author can rule.
- **Process note.** One headless-browser navigation (16:31:36Z) was made to PhilSci-Archive through the shared
  Playwright MCP and stopped at the bot check; it left one snapshot and one console log in the gitignored
  `.playwright-mcp/` folder. Downloads went to the session scratchpad only. The only tracked-area file written is
  this one.

## 8. Wording the paper may use, given this record

- **Allowed** (because the evidence is now recorded here): "In the sources searched for this paper (gate record,
  2026-10-15), we found no prior statement that ..." followed by exactly the not-found items of §3.2, §4.2, §5.4.
- **Allowed:** "We apply ...", "we make explicit ...", "we assemble ...", with the attributions in §3.6, §4.6, §5.6.
- **Not allowed:** "novel", "first", "to our knowledge", "we introduce", "unprecedented" for any of C1-C3.
  RESEARCH-DIRECTOR §8 allows such language only once evidence for it is recorded; this record supports nothing
  stronger than the narrow "not found in the searched sources" statements above, so the banned phrases stay banned.
- **Claim level (§5):** the paper's C1-C3 content is Level 2 (method and application). Its one registered test,
  HYP-033, unblinded at Level 2 (outcome 4), so nothing in the paper sits above Level 2.
