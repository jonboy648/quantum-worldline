# ana:reproducibility — RESEARCH-DIRECTOR §21 Conformance Audit

**Task:** `ana:reproducibility`. Governing standard: `docs/governance/RESEARCH-DIRECTOR.md` §21
(with §5 contribution levels, §7 independence, §32 retraction discipline, §38.A.4 "which
simulation records lack reproducibility metadata").
**Date of audit:** 2026-08-17. **Repo state:** branch `public-release`, local HEAD `a82069f`.
**Public remote state (verified live, see §1.3):** `origin/public-release` HEAD `13b8292`, dated
**2026-06-17** — 85 commits behind local.

All paths are repo-relative to `D:/quantum-worldline/` unless absolute.

---

## 0. Executive summary

Six findings, in order of consequence.

1. **The submitted PRD manuscript's Data-and-Code-Availability statement is not satisfied at either
   endpoint it names.** `research/submission-package/prd/paper-prd.tex:690-711` names 17 data files
   and 2 Julia drivers at `github.com/jonboy648/quantum-worldline`. **8 of those 19 items do not
   exist on the public repository** (verified by `git cat-file -e origin/public-release:<path>` and
   confirmed live against GitHub, §1.3). The Zenodo record the paper also cites
   (`10.5281/zenodo.19660302`) contains **one file: `paper-draft-scipost.pdf` (1.1 MB)** — no code,
   no data (verified live, §5.2). This is the §21 last-paragraph failure in its most direct form.
2. **Zero of 85 records carry an output checksum; one of 73 pins the project's own code revision;
   zero name an analysis or fit script.** Full table in §2.
3. **Every state/parameter array the manuscript's headline force and transport results depend on is
   gitignored.** `.gitignore:19` is `*.npy`; there are **30 `.npy` files on disk and 0 tracked**.
   These include `gs_24q_exact.npy` (input to the α = 3.92 measurement) and the four transport
   arrays that `figure3_transport_trace.py` loads.
4. **Of the 8 headline results in scope, 2 are reproducible from this repo alone** (SIM-067 fully;
   SIM-070/071 conditionally — the drivers and raw outputs are tracked, but the analysis
   estimators are not). **4 are not reproducible at any effort** without an unpinned external
   dependency. Table in §3.
5. **A frozen snapshot for the submitted manuscript does not exist and was never created** — the
   repository carries **zero git tags**, and the commit that would serve
   (`f124038`, 2026-08-07, *"SUBMITTED to Physical Review D … accession DV13971"*) has never been
   pushed. Concrete proposal in §5.
6. **One-command reproduction of headline figures is achievable for 3 of 6 figures with about a
   day of work, and for 5 of 6 with the addition of two `.gitignore` exceptions and one vendored
   commit pin.** Figure 5 is a schematic and needs nothing. Detail in §6.

Nothing in this artifact disputes any physics number. The phase-1 pipeline audit re-derived the
raw values it could reach and they held. This audit is about whether a third party could get there.

---

## 1. Scope, denominators, and what "this repo alone" means

### 1.1 The record count

The task brief says 85 SIM records. `research/data/simulations/` contains **85 `.json` files**, of
which:

- **73** are named `SIM-2026-0NN*.json` and carry (or attempt) a SIM identity;
- **12** are headerless result files with no SIM filename. Four of those carry a `sim_id` field
  (`classical_baseline_SIM2026002/3`, `composite_geodesic_results`, `worldline_mc_results`);
  **eight carry no id at all** (`dewitt_correction_results`, `effective_mass_analysis`,
  `holographic_transport`, `holographic_transport_24q`, `hyp010_criticality_scan`,
  `normalization_convention_analysis`, `runpod_gpus`, `skin_depth_data`).

This matters because **five of the twelve headerless files are cited by the submitted manuscript
as primary data** (`paper-prd.tex:694-701`), and two of them —
`holographic_transport.json` and `holographic_transport_24q.json`, the source of manuscript
Result 2 — have **no `id`, no `date`, no `description`, no `type`, no `script_path` and no
verdict field**. I verified this by key inspection: `holographic_transport.json`'s complete top-level
key set is `experiment, hypothesis_id, boundary_sites, hamiltonian, E_gs, perturbation,
time_evolution, transport_signature, total_time_s`.

**Denominators used below:** the §21 item table is computed over the **73** `SIM-*.json` files
(the population the earlier auditors also used, so the numbers are comparable). The twelve
headerless files are worse on every item and are treated separately in §2.4.

### 1.2 What is and is not in the repository

| Category | Status | Evidence |
|---|---|---|
| Python drivers (`research/data/simulations/*.py`) | 130 of 131 tracked (only `set_runpod_key.py` ignored, deliberately) | `git ls-files` vs `ls` |
| Julia/Python pipeline drivers (`research/tools/{merakit-setup,cttt-circle,pumps-setup,yanglee-pt}`) | 48 files tracked | `git ls-files research/tools/` |
| `research/tools/MERAKit.jl/` | **gitignored**, `.gitignore:51`; **no upstream commit pin anywhere** | `git check-ignore -v` |
| `research/tools/puMPS/` | **gitignored**, `.gitignore:54`; pinned to `0557b12a…` in `pumps-setup/VENDOR.md:10-16` | ibid. |
| `*.npy` (30 files, 129 MB — 128 MB of it one file) | **all gitignored**, `.gitignore:19`; **0 tracked** | `git ls-files … \| grep .npy` → empty; `du -ch` |
| `*.npz` (27 on disk) | 17 tracked, 10 uncommitted at audit time | `git ls-files`; `git status` |
| `research/data/theory/` | 8 prose `.md` files, **0 structured records**, and **no `templates/theory-record.json` exists** | `ls research/data/theory/`, `ls templates/` |
| Repo-level environment spec | `requirements.txt` (Python, fully pinned); `research/tools/merakit-setup/Project.toml.pinned` (Julia deps only) | root listing |
| Git tags | **0** | `git tag` |

"Reproducible from this repo alone" therefore means: **a third party clones the public GitHub
repository, installs `requirements.txt`, and attempts to regenerate the number.** Where a result
needs MERAKit.jl or puMPS, that party must additionally fetch external code — and for MERAKit
there is no recorded revision to fetch.

### 1.3 The public endpoint — verified live

This is the load-bearing check and I ran it two ways.

**Local git:** `git log --oneline origin/public-release..public-release | wc -l` = **85**.
`git log -1 --format="%h %ad" --date=short origin/public-release` = `13b8292 2026-06-17`.
`.git/FETCH_HEAD` is dated 2026-06-27, so this alone would be stale evidence.

**Live check (WebFetch, `https://github.com/jonboy648/quantum-worldline/commits/public-release`):**
most recent commit **"KB refresh to scan #10 + launch seeded chi=3 TCI MERA (HYP-027 stage-2b)",
June 17, 2026**; repository confirmed public and accessible. The local mirror is accurate.

Consequences, measured:

| | public `origin/public-release` | local `HEAD` |
|---|---|---|
| total tracked files | **614** | **784** |
| `SIM-*.json` records | **44** | **73** |
| files under `research/tools/` | **0** | 48 |
| `research/submission-package/` | **absent** | present |

**Per-item check of the manuscript's availability list** (`paper-prd.tex:693-711`), run as
`git cat-file -e origin/public-release:<path>`:

| item | on public repo? |
|---|---|
| `holographic_transport.json`, `holographic_transport_24q.json`, `composite_geodesic_results.json` | yes |
| `SIM-2026-008b-8q-test.json`, `SIM-2026-008c.json` | yes |
| `effective_mass_analysis.json`, `worldline_mc_results.json` | yes |
| `SIM-2026-011-interaction.json`, `SIM-2026-015.json`, `SIM-2026-015c.json`, `SIM-2026-015d.json` | yes |
| **`SIM-2026-051.json`, `SIM-2026-052.json`** (tricritical Ising spectra) | **NO** |
| **`SIM-2026-061.json`, `SIM-2026-064.json`** (C_σσε) | **NO** |
| **`SIM-2026-062.json`, `SIM-2026-063.json`** (Z₃ Potts spectra) | **NO** |
| **`qw_ope_pev_z2.jl`, `qw_potts_z3.jl`** (the two named drivers) | **NO** — all of `research/tools/` is absent |

**8 of 19 named items are unavailable at the URL the manuscript gives.** The six missing SIM
records are precisely the ones backing the abstract's universality claim ("we confirm this at two
further fixed points … tricritical Ising … three-state Potts"), i.e. the material added between
2026-06-17 and submission. A referee following the availability statement today would find the
force and transport data but not the universality data, and none of the tensor-network drivers.

**This defect is absent from `research/ERRATA.md`** (grep for `availab`, `github`, `npy`,
`snapshot` — the only hits are E-series entries about which *text* the appendix contains, never
about whether the referenced artifacts are reachable).

---

## 2. §21 conformance table

### 2.1 Method

§21 enumerates twelve items. I scored each one **strictly** — the metadata must let a third party
reconstruct the run, not merely gesture at it — with a machine scan over the flattened key paths
and string values of all 73 `SIM-*.json` files, followed by hand verification of every low-count
item and every borderline hit. Where the machine scan produced false positives I corrected the
count downward and say so. Scan scripts used are throwaway; the tests are stated below so any
number here can be re-derived by grep.

### 2.2 The table (n = 73 `SIM-*.json` records)

| # | §21 item | records carrying it | % | what counted, and what did not |
|---|---|---|---|---|
| 1 | **code revision** | **1 / 73** | **1 %** | Only `SIM-2026-052.json` `notes` pins this project's own driver: *"(committed merakit-setup/qw_tci_chi8.jl **51f2c0c**)"*. Two near-misses excluded on inspection: `SIM-2026-068.json` cites `commit 0557b12` but that is the **vendored upstream puMPS** revision, not this project's code; `SIM-2026-045.json` cites `commit b31c01b` for a **data file** (`uw_ISING_stable_chi4.npz`), not code. Lenient count including both: 3/73 (4 %). |
| 2 | **environment specification** | **5 / 73** | **7 %** | A language-runtime version appears in exactly five records — `050, 051, 052, 056` ("Julia 1.8.5") and `062` ("Julia 1.8"). A further 8 records say only *"local CPU (single-thread BLAS)"* or similar, which is platform colour, not an environment spec. Lenient count: 13/73 (18 %). **No record anywhere states a Python version**, though 43 of the 73 were produced by Python drivers. |
| 3 | **dependency versions** | **0 / 73** | **0 %** | No record names any package with a version. `requirements.txt` exists at repo root and is fully pinned (`numpy==2.2.6, scipy==1.16.0, qiskit==2.3.0, qiskit-aer==0.17.2, matplotlib==3.10.3, pytket==2.15.0, …`) — but it is a **single current-state file with no per-record binding**. SIM-001 ran 2026-03-10; `requirements.txt` describes the environment of some later date. Nothing links a record to the versions it actually used. For Julia there is `merakit-setup/Project.toml.pinned` (deps only) and **no `Manifest.toml` anywhere** — `git ls-files \| grep -i manifest` is empty. |
| 4 | **platform information** | **54 / 73** | **74 %** | Counted a `hardware` / `hardware_target` / `backend` field or an in-prose platform string. Uniformly free text: `"local CPU"`, `"RunPod A100 (cupy + qiskit-aer)"`, `"local CPU, sparse ED (scipy)"`. **No record gives a CPU model, core count, RAM, OS, or RunPod pod id.** The single most specific is `SIM-2026-068.json`'s note about `OPENBLAS_NUM_THREADS=1` discipline. |
| 5 | **random seeds** | **9 / 73** | **12 %** | Actual RNG seed **values** appear only in the 2026-03/04 VQE family: `003, 005, 006, 008, 008a, 008b-8q-test, 008c, 015, 015c` (e.g. `"seeds": [0,1,2,3,42,7,13,99,5,17]` in SIM-003). **Five machine hits were false positives** and I excluded them: `SIM-051`'s `best_spectrum_seed.seed = 5` and `SIM-052`'s `= 1` are **run-index labels**, not RNG values (confirmed by key path; the records elsewhere label runs `seed1…seed8`), and `056/057/059` use the same convention. **After SIM-2026-015c (2026-04), not a single record states an RNG seed.** Independently corroborated: `inv-sims-mid.md:688` finds 0/21 in its range, with SIM-039/040's seeds hard-coded in the scripts (`sim039_autograd_mera.py:168` `default_rng(42)`) but never written to the record; `inv-pipelines.md:740-744` finds `qw_yanglee_ks.jl:71` and `qw_yanglee_pt.jl:50` start Arnoldi from unseeded `randn(ComplexF64, dim)`. |
| 6 | **model parameters** | **66 / 73** | **90 %** | The project's consistent strength. N/L, χ, couplings, λ₃, h, dt are present and usually explicit. The 7 misses are stubs and resource-estimate records (`014, 044, 058, 060, 061, 064, 067` score by prose rather than fields in some cases; `SIM-2026-044.json` is a 352-byte stub with no results object at all — `inv-sims-mid.md:763`). |
| 7 | **solver settings** | **32 / 73** | **44 %** | Counted a named solver (`eigsh`, ARPACK, KrylovKit, L-BFGS-B, COBYLA, Riemannian LBFGS, CG, `expm_multiply`) **or** an explicit setting (`maxiter`, `niter`, `krylovdim`). Tolerances are almost never given at record level. Worked example of the gap: SIM-071's actual solver settings — `nev=24, krylovdim=90, tol=1e-11, maxiter=400` — exist **only inside `qw_yanglee_ks.jl`**, never in `SIM-2026-071.json` (`inv-sims-late.md:1055`). |
| 8 | **convergence criteria** | **19 / 73** | **26 %** | Counted an explicit tolerance, gradient-norm threshold, stated gate, or a `converged_*` boolean. Frequently the record reports *whether* it converged without saying *against what*. Notable good case: `SIM-2026-069.json` states the d=3 CG plateaus at `|grad| ≈ 2.5e-4` and that "measurement quality is certified by the N=10 ED gate, **not** by `\|grad\|`" — the criterion is named *and* its inadequacy is disclosed. |
| 9 | **input records** | **73 / 73 pointer** — **~52 / 73 resolvable** | 100 % / ~71 % | Every record points at *something* (a `script_path`, a `driver`/`files` block, a predecessor SIM id, or a `.npy`/`.npz`/`.jsonl`). **The pointers frequently do not resolve.** I extracted every file reference from all 73 records and resolved each against the working tree and the git index: **69 present-and-tracked, 35 present-but-untracked, 30 unresolvable**. **20 of 73 records reference at least one artifact that does not exist anywhere in the repository; 22 of 73 reference at least one artifact that exists on disk but is gitignored.** Breakdown in §2.3. |
| 10 | **output checksums** | **0 / 73** | **0 %** | Repo-wide grep for `checksum\|md5\|sha256\|digest` across all SIM records: no hits. Not one number in the program has an integrity hash. |
| 11 | **runtime metadata** | **43 / 73** | **59 %** | `elapsed_seconds`, `wall_s`, `wall_seconds`, `runtime_s`, `total_time_s`, or a prose duration ("~45 min at chi=8"). Where present it is usually good. |
| 12 | **analysis script revision** | **0 / 73** | **0 %** | The machine scan returned 6 hits; **all six are `visualization_path` fields pointing at output PNGs** (`001, 018, 019, 020, 021, 022`), which are not analysis scripts. **No record names a fit or analysis script, with or without a revision.** This is corroborated independently three times: `inv-sims-early.md:611` (0/43), `inv-sims-mid.md:695` (0/21), `inv-pipelines.md:735` (P1/P3/P4 all "NO"). Concretely: the SIM-070 Richardson estimator and the `b = 12/5 + L^-4` h-fit — the two analyses that produce the project's flagship number — **exist nowhere in the repository** (`inv-pipelines.md:583-589`), and the SIM-068/069 `variants` fit tables were produced by untracked code. |

**Aggregate:** mean **4.4 of 12** items per record. **20 of 73 records (27 %) carry 3 or fewer.**

### 2.3 The artifact-link finding, in detail

The §21 phrase "input records" is only meaningful if the link resolves. Measured over every
file reference in all 73 records (134 references total):

- **69 present and tracked** — fine.
- **35 present but gitignored** — the reference is dead for anyone who clones. These are the
  `theta_*.npy` optimized-parameter files (SIM-003, 009, 036, 037, 039, 040), `gs_24q_exact.npy`
  (SIM-013, 024 — and it is the input to the α = 3.92 measurement), the four `transport_*_finedt_*.npy`
  arrays (SIM-025), and **17 references into the gitignored `research/tools/MERAKit.jl/` tree**
  (SIM-051, 052, 056, 057, 058, 059, 060, 061, 062, 063, 064, 065).
- **30 unresolvable anywhere on disk.** The substantive ones:
  - **11 scratchpad `.log` files**, the sole raw records for SIM-060/061/062/063/064/065/066:
    `pev_chi6_gate.log`, `z2_v4_gate.log`, `potts_z3_chi6.log`, `potts_chi9.log`, `potts_chi12.log`,
    `ope_chi10.log`, `ope_chi12.log`, `ope_chi12_m8000.log`, `cttt_smoke0.log`, `cttt_chi6_smoke.log`,
    `cttt_chi8.log` / `cttt_chi8_v2.log`, plus the wildcarded `cttt_chi10_s1..8.log` and
    `cttt_chi12_s1..8.log`. Verified absent by `find`. Independently confirmed at
    `inv-sims-late.md:1253-1258` and `inv-pipelines.md:157-163`.
  - `SIM-2026-022.json` → `visualization_path` → `SIM-2026-022_aquila_protocol.png` — **broken link**.
  - `SIM-2026-042.json` → `simple_mera.py` — **not present anywhere** (`find` returns nothing).
  - The remainder are package names in prose (`MPSKit.jl`, `ITensorInfiniteMPS.jl`) or `.jsonl`
    paths my extractor clipped to `.json`; those are not defects.

### 2.4 The twelve headerless records, and the project's own schema

The §21 picture is worse for the twelve non-`SIM-` JSON files, and the project's **own** minimal
schema is already failing.

`templates/simulation-result.json` requires only four fields — `id`, `description`, `type`, `date` —
and **none of the twelve §21 items**. Measured against that four-field bar across the 73 SIM records:

| requirement | violations |
|---|---|
| `id` present | **3 missing** (`005`, `006`, `011`) |
| `id` matches `^SIM-\d{4}-\d{3,}$` | **11 fail** (`005`, `006`, `011` empty; `008a`, `008b-8q-test`, `008c`, `015b`, `015c`, `015d`, `032b`, `033b` carry letter suffixes) |
| `description` present | **30 missing** |
| `type` present | **24 missing** |
| `type` within enum `{quantum, classical, comparison}` | **20 outside** (e.g. `vqe_optimization`, `resource-estimation`, and SIM-067's `type` is a 90-character sentence) |
| `date` present | **17 missing** |

ERRATA D3 (`research/ERRATA.md:75`) already records *"only 9/36 SIM files … satisfy `templates/*.json`"*.
That entry is from the 2026-06-08 audit and was never refreshed; the population has since grown from
36 to 73 and the conformance rate has not improved.

For the twelve headerless files: 4 carry a `sim_id`, **8 carry no identifier of any kind**, 5 have
no `date`, 6 have no `description`. Five of them are cited as primary data by the submitted
manuscript. `worldline_mc_results.json` additionally contains a literal `NaN` (invalid strict JSON;
ERRATA D2), and so does `SIM-2026-031.json` (`inv-sims-early.md:652`, not in ERRATA).

---

## 3. Headline results — could a third party reproduce them from this repo alone?

### 3.1 Grading scale

| grade | meaning |
|---|---|
| **A** | Driver tracked; all inputs tracked or regenerable by tracked code; parameters and determinism recorded or discoverable in the tracked driver; the recorded number can be recomputed end-to-end. |
| **B** | Recomputable, but the record does not supply the link — the reproducer must infer the driver from filenames, read the seed out of the source, or re-derive the analysis/fit step from scratch. |
| **C** | Blocked on an external dependency that the repo does not pin (or, for puMPS, pins but cannot redistribute). Re-running requires fetching third-party code at a guessed or manually-patched revision. |
| **D** | Not reproducible at any effort from this repository: the raw artifacts are absent and the analysis code does not exist. |

Two separate questions are graded: **(i) re-run** — can the calculation be executed? and
**(ii) re-derive the published number** — can the specific quoted value be recovered from what is
in the repo? They diverge often.

### 3.2 The table

| # | Headline result | Primary record(s) | Re-run | Re-derive number | Public-repo availability |
|---|---|---|---|---|---|
| H1 | α = 3.92 ± 0.16 (24 q exact) | `SIM-2026-011-interaction.json` | **B** | **B** | yes |
| H2 | α = 3.97 ± 0.15 (16 q exact) and 4.07 ± 0.18 (16 q χ=3 MERA) | `SIM-2026-015d.json` | **B** | **B** | yes |
| H3 | Universality: TCI Δ_T = 1.999, Potts Δ_T = 2.001 → α = 4.00 at three classes | `SIM-2026-051/052` (TCI), `SIM-2026-062/063` (Potts) | **C** | **D** | **NO — all four absent** |
| H4 | Transport T = (π/2)·l_AdS, residual −1.21 % at N = 16 (grid-converged) | `holographic_transport.json` + `SIM-2026-025.json` | **A** | **B** | yes |
| H5 | Two-phase ALM + Z₂-projected L-BFGS-B: 1.12 % @ 8 q, 3.33 % @ 24 q | `SIM-2026-008b-8q-test.json`, `SIM-2026-008c.json` | **A** | **A** | yes |
| H6 | χ = 3 MERA, 0.15 % energy error at 16 q, C(r) ~ r^(−1/4) | `SIM-2026-015c.json` | **A** | **A** | yes |
| H7 | m_eff = 0.693 vs MERA 0.670 (3.5 %) | `effective_mass_analysis.json`, `worldline_mc_results.json` | **B** | **B** | yes |
| H8 | Helios hardware path: 57 CNOTs, 0.57 % logical error | `SIM-2026-019/021/022` | **B** | **B** | yes |
| H9 | C_σσε = 0.50 ± 0.03 (paper v5 §7.4) | `SIM-2026-061`, `SIM-2026-064` | **C** | **D** | **NO — both absent** |
| H10 | C_TTT Ising = 3.9936 vs 4.000 | `SIM-2026-067.json` | **A** | **A** | **NO — `research/tools/` absent** |
| H11 | C_TTT TCI = 3.381 vs 3.3806 | `SIM-2026-068.json` | **C** | **B** | **NO** |
| H12 | C_TTT Potts = 3.163 vs 3.16228 | `SIM-2026-069.json` | **C** | **B** | **NO** |
| H13 | SIM-070 Phase-1 gate: R_inf = −1.61820 (0.01 %), g₁ = 0.725347 (0.04 %) | `SIM-2026-070.json` | **A** | **D** | **NO** |
| H14 | SIM-071: c_KS = −4.29 ± 0.15 = true c = −22/5; c_eff = +2/5 excluded | `SIM-2026-071.json` | **A** | **B** (sign/ladder) / **D** (the −4.29 centre) | **NO** |

**Score:** from a clone of this repository at local HEAD — 5 A, 5 B, 4 C, and 3 D on the
"re-derive the published number" axis. **From a clone of the public repository**, six of the
fourteen have no primary record at all.

### 3.3 Why each grade

**H1 (α = 3.92, 24 q) — B / B.** The driver `research/data/simulations/interaction_energy_24q.py`
exists and **is tracked** (21 750 bytes, verified). It computes exactly the recorded observable
`F(dr) = E_dual − E_0 − 2·dE_single` and caches the ground state to `gs_24q_exact.npy`. The
ground state is obtained by `eigsh(H, k=1, which='SA')` on a non-degenerate spectrum, so the run
is effectively deterministic without a seed. **But `SIM-2026-011-interaction.json` names no script
at all** — its complete key set is `id, date, description, hypothesis, predecessor_sim,
ground_state, observable, anchor, dr_values, boundary_primary_coeffs, E_singles, E_duals,
F_interaction_avg, F_interaction_probe_only, norms_single, norms_dual, fits, force_profile,
decay_analysis, runtime_s, hardware, status`. There is no `script_path`, no `.py` reference, no
`.npy` reference. A reproducer must match the record to a driver by filename inference. The cached
`gs_24q_exact.npy` is gitignored, so the ~1 228 s `eigsh` must be re-run. **Independently, the
phase-1 sims audit reports a substantive analysis-fragility issue that this repo cannot help
with:** dropping the single point dr = 2 moves α from 3.92 to 2.56 (`inv-sims-early.md`
executive summary), and the fit code that produced ± 0.16 is not identified in the record.

**H2 (16 q, exact and χ=3 MERA) — B / B.** `sim2026015d_chi3_16q_force.py` is tracked. The record
`SIM-2026-015d.json` again names no script (key set: `id, description, n_qubits, chi, anchor,
dr_values, E0_exact, E_mera, exact, mera, status`). The MERA branch needs
`theta_opt_SIM2026015c.npy` — **gitignored** — or a full re-optimization.

**H3 (universality, TCI + Potts) — C / D.** All four records depend on
`research/tools/MERAKit.jl/`, which is gitignored with **no upstream revision recorded anywhere**
(`inv-pipelines.md:67-72` establishes the same; `merakit-setup/Project.toml.pinned` pins the
*dependencies*, not MERAKit itself). Re-running therefore requires guessing a MERAKit revision. And
the recorded numbers cannot be re-derived at all: the cited raw logs
(`potts_z3_chi6.log`, `potts_chi9.log`, `potts_chi12.log`, `qw_tci_measure.log` beyond the
gitignored tree) are absent, so the per-seed spectra exist **only as prose inside the SIM JSON**.
Two further complications recorded by other auditors and relevant here: `SIM-2026-051`'s stated
8-seed mean Δ_T (1.9913) does not match the mean of its own listed values (2.0163)
(`inv-sims-mid.md:463-467`), and `merakit-setup/qw_tci.jl` has drifted from the newer vendored copy
so the *tracked* mirror is the stale one (`inv-pipelines.md:102-110`).

**H4 (transport) — A / B.** `holographic_transport_16q.py` is tracked and writes all four
`.npy` outputs (`transport_times.npy`, `boundary_density_{Y,Z}.npy`, `transport_max_rho.npy`,
lines 424-427). The fine-dt re-run that supersedes it is the one record in the whole set with an
exemplary provenance block: `SIM-2026-025.json` gives `circuit.script_path =
research/data/simulations/holographic_transport_finedt.py` (tracked), the full Wang–He Hamiltonian,
Ω, σ_t, σ_φ, dt and the integrator. **Re-run: A.** *Re-derive:* the published residual moved from
+0.72 % (retracted, ERRATA E2) to −1.21 %, and the record that the manuscript's availability list
actually points at — `holographic_transport.json` — is headerless, carries the superseded
`transport_time: 2.25` against a `predicted_transport_time: 4.5324` (a different normalization),
and has no id/date/script. The reproducer must know from ERRATA which number is live.

**H5 (ALM two-phase) — A / A.** The best-documented headline in the program.
`sim2026008c_alm_proj_24q.py:180` hard-codes `SEEDS = [7, 42, 99, 13, 77]` and line 191 calls
`np.random.seed(seed)`; the record `SIM-2026-008c.json` **independently lists the same
`seeds` array**, plus `alm_rounds`, `alm_evals_per_round`, `proj_evals`, `best_seed`, `best_E`,
`best_error_pct`, `total_time_s`. Driver tracked, all inputs synthetic, fully deterministic.
This is the template the rest of the repo should follow.

**H6 (χ=3 at 16 q) — A / A.** `sim2026015c_chi3_16q.py:37` is `SEEDS = [42]`, line 277
`np.random.seed(seed)`; the record lists `chi`, `n_layers`, `n_params`, `E0_exact`, per-seed
results. Tracked, deterministic, self-contained.

**H7 (m_eff) — B / B.** `effective_mass_analysis.json` is headerless (no `id`, no `type`,
no script) but records the full input spectrum (E0…E3) and every intermediate, so the 0.693 is
recomputable by hand from the record. The MERA-side comparand 0.670 comes from
`worldline_mc_results.json`, which contains a literal `NaN` and whose ξ input carries a documented
uncorrected error (`inv-sims-early.md:688`, "A7": ξ = 1.233 was fitted to values read off a plot;
never written back, not in ERRATA). Reproducible arithmetic; unreproducible provenance.

**H8 (Helios path) — B / B.** Analytic resource estimates; the records carry the configuration
tables. `SIM-2026-022.json`'s `visualization_path` is a **broken link**
(`SIM-2026-022_aquila_protocol.png` does not exist).

**H9 (C_σσε) — C / D.** Same MERAKit blocker as H3, plus all three cited logs
(`ope_chi10.log`, `ope_chi12.log`, `ope_chi12_m8000.log`) are absent. The 8 per-seed C_σσε values
that produce "0.50 ± 0.03" exist only as prose.

**H10 (C_TTT Ising, SIM-067) — A / A.** The cleanest result in the repository from a §21
standpoint. `research/tools/cttt-circle/qw_cttt_circle.py` (397 lines) is tracked, imports only
`numpy`/`scipy`, needs no vendored code, and **its raw per-N outputs are tracked**
(`qw_cttt_circle_results_ising.json`, `…_of.json`). The extrapolation is inside `main()`, so the
analysis is committed too. The phase-1 pipeline auditor re-ran the fits from the tracked file and
matched exactly (`inv-pipelines.md:210-212`). *Caveat, not a reproducibility defect:* the driver
uses a non-standard Koo–Saleur mode discretization documented nowhere
(`qw_cttt_circle.py:183`; `inv-pipelines.md:229-248`), and `c_meas` and `C_TTT` are extrapolated
separately although algebraically linked, giving two answers 0.29 % apart. Both are *checkable*
precisely because the artifacts are tracked — which is the point.

**H11/H12 (C_TTT TCI, Potts) — C / B.** The drivers `pumps-setup/qw_cttt_of.jl`,
`qw_cttt_potts3.jl`, `qw_potts_ed_gate.jl` are tracked and **the raw per-rung `.jsonl` outputs are
tracked** (`qw_cttt_of_results_2026-08-10.jsonl`, `qw_cttt_potts3_results_2026-08-11.jsonl`),
so the fits can be — and were — re-derived (`inv-pipelines.md:286-290`, reproduced to 5 decimals).
That is why re-derive is **B** not D: the fit script is untracked but recoverable from the raw data.
Re-run is **C**: `qw_cttt_potts3.jl:18` is `include("MPS.jl")`, inside the gitignored `puMPS/`
tree, which additionally needs **two hand-applied patches described in prose only**
(`pumps-setup/VENDOR.md:79-88`) — no `.patch` file exists. The vendoring decision itself is
correct and well-reasoned (upstream carries no license, `VENDOR.md:13-16`) and the commit
**is** pinned (`0557b12a…`) — this is the good pattern, one `.patch` file short of complete.

**H13 (SIM-070 Phase-1 gate) — A / D.** The driver `yanglee-pt/qw_yanglee_pt.jl` is tracked and
so are **two output logs** (`yl_run_8_18.log`, `yl_proj.log`) — better artifact retention than
anywhere else in the program. But the **recorded number is not producible by the tracked code**:
`yl_run_8_18.log`'s last line is `GATE: NOT PASSED -- inspect before Phase 2`, with
`h_c^inf = 1.5585927`, `R_inf = −1.6444…−1.6566`, against the record's `PASSED` / `−1.61820`
(`inv-pipelines.md:570-589`). The recorded value requires (a) a different `h_c^inf` from a
`b = 12/5 + L^-4` fit that **exists nowhere in the repo**, and (b) a two-level Richardson
estimator that **also exists nowhere in the repo**. Both were re-derivable by a determined auditor
from the tracked `h_c^L` table, but that is reconstruction, not reproduction. Grade D on
re-derive is a direct §21 "analysis script revision" failure with a headline consequence.

**H14 (SIM-071, c_KS) — A / B-and-D.** The driver `qw_yanglee_ks.jl` (152 lines) is tracked and
depends only on `LinearAlgebra, SparseArrays, Printf, KrylovKit` — no vendored code. The five
Yang-Lee stages are in a tracked `.jsonl` with per-state products, `Dvac`, `Tnorm`, `vT`.
**The raw ladder (the sign result, which is the defensible half of the claim) is reproducible: B.**
The `−4.29` centre is **D**: it needs the same untracked Richardson estimator as H13, and the
phase-1 pipeline audit measured that the choice of `h_c^inf` fit model moves the extrapolated
headline from **−3.67 to −7.04** (`inv-pipelines.md:518-528`) — a systematic that the quoted
± 0.15 band does not contain. Three further §21 absences on the program's flagship result:
**(a) the unitary control has no persisted output anywhere** — a repo-wide grep for
`0.517483|0.512776|0.509748|0.49986` returns only prose restatements
(`inv-sims-late.md:1040-1044`); **(b) `ylks_warn.log` is 0 bytes**, so the biorthogonal-norm
printout backing the "⟨1|1⟩ NEGATIVE at every L" claim was discarded; **(c) no RNG seed** — the
Arnoldi start vector is unseeded `randn(ComplexF64, dim)`. Mitigating and worth recording: the
phase-1 auditor re-implemented the driver in Python/ARPACK and reproduced both the Yang-Lee ladder
and the unitary control to 6 decimals (`inv-pipelines.md:366-375`) — so the numbers are right;
the repository simply could not have established that on its own.

### 3.4 The pattern

The grades split cleanly along one axis, and it is **not** the axis the project's own framing would
predict. The oldest, least-celebrated pipeline — the loose Python scripts in
`research/data/simulations/` that carry every manuscript headline — is the **most** reproducible
(all 130 drivers tracked, seeds hard-coded, deterministic solvers). The newest, most scientifically
ambitious work is the least reproducible, because its analysis moved out of the drivers and into
untracked ad-hoc estimators, and because two of the four pipelines depend on gitignored vendored
code. Reproducibility here degraded as the science improved.

---

## 4. Blocking gaps, per headline result

"Blocking" = the specific missing artifact without which the recorded number cannot be recovered.
Ordered by how cheap the fix is. Effort estimates are for someone with the working environment
already in hand.

| # | Result | Blocking gap(s) | Cheapest fix | Effort |
|---|---|---|---|---|
| H10 | C_TTT Ising 3.9936 | **None for reproduction.** (Two *accuracy* caveats — undocumented KS phase convention, and separate extrapolation of `c` and `C_TTT` giving 4.00517 vs 3.99361 — are documentation defects, not repro blockers.) | Push to public; document the convention in a comment block | 15 min |
| H5 | ALM 1.12 % / 3.33 % | **None.** | — | — |
| H6 | χ=3 MERA 0.15 % | `theta_opt_SIM2026015c.npy` gitignored (only needed to skip the ~45 min re-optimization) | `.gitignore` exception for `research/data/simulations/theta_*.npy` (17 files, small) | 10 min |
| H4 | Transport −1.21 % | (i) the manuscript's availability list points at the **superseded** `holographic_transport.json`, not at `SIM-2026-025`; (ii) `transport_*.npy` gitignored so Figure 3 cannot be redrawn without a re-run; (iii) that headerless record has no id/date/type/script | Repoint the availability list at SIM-025; add a `.gitignore` exception for the four transport arrays; add a header block to the JSON | 1 h |
| H1, H2 | α = 3.92 / 3.97 / 4.07 | (i) records name **no driver** — link is by filename inference only; (ii) `gs_24q_exact.npy` and `theta_opt_*.npy` gitignored; (iii) **the fit script that produced ± 0.16 is not identified** — and the fit is the fragile step (dropping dr = 2 → α = 2.56) | Add `script_path` + a tracked `fit_force_profile.py`; `.gitignore` exceptions | 2–3 h |
| H7 | m_eff 0.693 / 0.670 | (i) headerless record; (ii) the 0.670 comparand inherits an **uncorrected** ξ error (fitted to numbers read off a published plot) that was never written back and is not in ERRATA | Write the ξ correction into ERRATA and into `worldline_mc_results.json`; add headers | 1 h |
| H8 | Helios 57 CNOT / 0.57 % | broken `visualization_path` in `SIM-2026-022.json` | regenerate or drop the field | 10 min |
| H13 | SIM-070 R_inf 0.01 % | **(a) the `h_c^inf` refit (`b = 12/5 + L^-4`) script does not exist in the repo; (b) the two-level Richardson estimator does not exist in the repo; (c) the tracked driver's own gate prints `NOT PASSED` for the run of record** | Commit both analysis scripts; update the driver's built-in gate to the accepted method **or** record explicitly that the built-in gate is superseded | 1–2 h |
| H14 | c_KS = −4.29 ± 0.15 | Same (a)+(b) as H13, plus: **no persisted output for the unitary control** (the single most load-bearing validation); `ylks_warn.log` 0 bytes so the ⟨1\|1⟩-negative evidence was discarded; no RNG seed; solver settings only in source | Re-run both modes with stdout captured into `yanglee-pt/`; append the ising rows to the `.jsonl`; commit the estimator; set an explicit Arnoldi seed | 2 h (mostly compute) |
| H11, H12 | C_TTT TCI 3.381 / Potts 3.163 | (i) `puMPS/` gitignored (license-correct) and **patched by prose instructions only** — no `.patch`; (ii) fit/variants script untracked; (iii) exact Julia dependency versions unrecoverable (`VENDOR.md` says the Project.toml "lives at `research/tools/puMPS/Project.toml` … gitignored with the source") | Add `pumps-setup/vendor-patches.patch` + a `fetch_and_patch.sh`; commit the fit script; commit a copy of the puMPS `Project.toml`/`Manifest.toml` (metadata, not source — no license issue) | 2–3 h |
| H3, H9 | Universality (TCI/Potts Δ) and C_σσε | **(i) `MERAKit.jl` gitignored with NO revision pin anywhere** — the single worst gap in the repo; (ii) **all 11 cited raw logs absent**, so the per-seed values exist only as prose and nothing can be re-fitted; (iii) `merakit-setup/qw_tci.jl` is a stale mirror of a materially different vendored file; (iv) 9 further drivers exist only inside the gitignored tree | (a) record the MERAKit upstream URL + commit in `merakit-setup/RUN-MERAKIT.md`, the way `VENDOR.md` does for puMPS; (b) **the logs that do exist inside `MERAKit.jl/` (`qw_potts_chi8.log`, `qw_tci_measure.log`, `v2_smoke.log`, `qw_of_control_correct.log`, `diag.log`) can be added with a one-line `.gitignore` exception — no re-run needed**; (c) re-sync the mirror; (d) the 11 truly-absent scratchpad logs require re-running | (a)+(b)+(c): 1 h. (d): days of compute |

**Cross-cutting blockers that hit every result:**

1. **No output checksums (0/85).** There is no way to tell whether a tracked `.jsonl`/`.json`
   corresponds to the run described. When SIM-070's log and record disagree, nothing in the
   metadata adjudicates.
2. **No dependency manifest for any Julia run.** `git ls-files | grep -i manifest` is empty.
   `Project.toml.pinned` names deps without versions resolved.
3. **`requirements.txt` is a single current-state file.** It cannot describe both a 2026-03 qiskit
   run and a 2026-08 scipy run. No record binds to it.
4. **The publication endpoint is 85 commits stale** (§1.3), which converts every "yes, tracked"
   above into "no" for six of the fourteen results.

---

## 5. Proposal: a frozen snapshot for the submitted manuscript (§21, last paragraph)

> *"A submitted manuscript should be linked to a frozen research snapshot. Do not allow later
> repository changes to silently alter the evidentiary basis of an existing paper."*

### 5.1 Current state — verified, not assumed

- **Git tags: zero.** `git tag` returns nothing.
- **The natural anchor commit exists but is unpushed:** `f124038`, 2026-08-07,
  *"SUBMITTED to Physical Review D 2026-08-07 -- accession DV13971, status 'With editors'"*.
  It sits 8 commits below local HEAD and **68 commits above** the public remote.
- **The Zenodo record is not a snapshot.** Fetched live from
  `https://zenodo.org/doi/10.5281/zenodo.19660302`: **v4, published 2026-07-15, one file —
  `paper-draft-scipost.pdf` (1.1 MB). No source code, no simulation data.** Metadata carries
  *"Is supplemented by Software: https://github.com/jonboy648/quantum-worldline"* — i.e. it
  delegates the evidence to a moving repository, which is exactly what §21 forbids.
- **`README.md:203` claims otherwise:** *"Preprint and **full reproduction package** are archived
  on Zenodo."* Against the fetched record, **that claim is false.** It should be corrected
  regardless of whether the snapshot proposal below is adopted.
- **Version mismatch:** the archived PDF is the **SciPost-formatted** `paper-draft-scipost.pdf`
  (v4, 2026-07-15). The **submitted** manuscript is `paper-prd.tex` → `paper-prd.pdf`
  (REVTeX/PRD, 2026-08-07, 713 lines vs the SciPost file's 743). The DOI in the submitted
  manuscript's acknowledgements therefore resolves to a *different document* from the one under
  review. Diff of the two `.tex` files confirms they diverge from line 1 (`\documentclass`) and
  differ in length by 30 lines.

### 5.2 What the snapshot must contain

Target: a referee, given one archive, can regenerate every number and figure in `paper-prd.pdf`
without network access and without guessing anything.

**Tier 1 — must be in the snapshot (all already exist locally):**

| item | where it is now | action |
|---|---|---|
| `paper-prd.tex`, `.bbl`, `references.bib`, the 6 figure PNGs | `research/submission-package/prd/` | include as-is |
| the 17 named data files + 2 named drivers | tracked locally | include; **6 of the SIMs and both drivers are not yet public** |
| the 130 tracked `research/data/simulations/*.py` drivers | tracked | include |
| `requirements.txt` | tracked | include, plus a `pip freeze` of the actual interpreter as `requirements.frozen.txt` |
| `research/ERRATA.md` at submission date | tracked | include — it is the only place the retracted 0.72 % transport number is corrected |

**Tier 2 — must be *added* before the snapshot is meaningful:**

| gap | fix | why it is blocking |
|---|---|---|
| `*.npy` excluded by `.gitignore:19` | **Measured:** all 30 `.npy` = 129 MB, but 128 MB of that is the single file `gs_24q_exact.npy` (2^24 × float64). Add `.gitignore` exceptions for `theta_*.npy` (12), `transport_*.npy` (8), `boundary_density_*.npy` (4) — **432 KB combined, commit directly**; deposit `gs_24q_exact.npy` on Zenodo only (regenerable in ~1 228 s by the tracked driver) | without them Figures 3 and 6 cannot be redrawn and the α measurement must be re-run from scratch |
| no `script_path` on the α records | add `script_path` to `SIM-2026-011-interaction.json` (`interaction_energy_24q.py`), `SIM-2026-015c/d.json`, `SIM-2026-008b/c.json` | the record→code link currently exists only by filename inference |
| no fit script for α | commit the power-law fitting code as `research/data/simulations/fit_force_profile.py` with the dr-window it used | ± 0.16 is unreproducible, and the fit window is the result's most fragile parameter |
| headerless primary records | add `id`, `date`, `type`, `description`, `script_path` to `holographic_transport.json`, `holographic_transport_24q.json`, `effective_mass_analysis.json`, `composite_geodesic_results.json`, `worldline_mc_results.json` | five files the manuscript cites as primary data have no identity |
| MERAKit revision unrecorded | add the upstream URL + commit SHA to `merakit-setup/RUN-MERAKIT.md`, mirroring `pumps-setup/VENDOR.md:10-16` | H3 and H9 (the universality and OPE claims in the abstract) are otherwise unreconstructible |
| checksums absent | emit a `MANIFEST.sha256` over every data file in the snapshot | §21 item 10; also the only defence against the SIM-070-style log/record divergence |
| broken/stale links | fix `SIM-2026-022.json` `visualization_path`; re-sync `merakit-setup/qw_tci.jl` | dangling references in a frozen artifact are worse than none |

**Tier 3 — should be in, cheaply:**
the 5 MERAKit result logs that exist inside the gitignored tree (`qw_potts_chi8.log`,
`qw_tci_measure.log`, `v2_smoke.log`, `qw_of_control_correct.log`, `diag.log`) — a `.gitignore`
exception, not a re-run.

### 5.3 The mechanism

1. Create the branch `submission/prd-DV13971` from `f124038`.
2. Apply the Tier-2 additions **as a single commit on that branch**, message
   *"PRD DV13971 reproducibility snapshot: adds inputs, fit script, manifest — no result changed"*.
   Adding evidence is not editing history; §32 is satisfied as long as the commit says so and no
   recorded number moves.
3. Tag it `prd-DV13971-v1` (annotated, with the accession number and submission date in the tag
   message). **This is the currently missing artifact — there are zero tags in the repo.**
4. `git archive` the tag → upload as a **new Zenodo version** alongside `paper-prd.pdf`, so the
   record contains *paper + code + data* rather than paper alone.
5. Amend `paper-prd.tex`'s availability appendix to cite **the versioned DOI and the tag**, not the
   bare GitHub URL. Keep the concept DOI in the acknowledgements for "current version".
6. **Push.** All of the above is inert while `origin/public-release` sits at 2026-06-17.
7. Correct `README.md:203` ("full reproduction package are archived on Zenodo") to match whatever
   is actually deposited.

### 5.4 Going forward

Adopt a standing rule, since this will recur: **every manuscript submission and every Zenodo
version gets an annotated tag at the moment of submission, and the tag is created before the
submission email is sent.** The repo already has the discipline to write a commit at submission
time (`f124038`); it is one `git tag -a` short of a snapshot.

---

## 6. One-command reproduction of headline figures (§21, "where practical")

### 6.1 Present state

There is no build entry point of any kind: **no `Makefile`, no `run_all.sh`, no `repro/` directory,
no notebook.** `scripts/` contains only `sync-agents.sh` and five RunPod helpers. `README.md`'s
"Quick Start" section is about deploying the *agent team*, not about reproducing results — the word
"reproduce" appears once in the README, in the sentence about Zenodo.

Per-figure assessment. All six generators exist under `research/data/simulations/` and **all six
are tracked**:

| figure | generator | one-command today? | blocker |
|---|---|---|---|
| **1** MERA schematic | `figure1_mera_schematic.py` | **YES** | none — pure matplotlib drawing, no data |
| **5** Helios error budget | `figure5_helios_error_budget.py` | **YES** | none — configuration table hard-coded in-script (lines 35+) |
| **2** ALM convergence | `figure2_alm_convergence.py` | **YES** | none — reads its series from in-script literals |
| **6** χ=3 comparison | `figure6_chi3_comparison.py` | **almost** — reads tracked `SIM-2026-015.json`, `SIM-2026-011-interaction.json`, `SIM-2026-015d.json` (lines 49-79) | absolute `D:/quantum-worldline/...` paths; and three comparison series are hard-coded literals (`chi2_C_r`, `F_16q_exact`) whose provenance is not stated |
| **3** transport trace | `figure3_transport_trace.py` | **NO** | loads `transport_times.npy` and `boundary_density_Y.npy` (lines 25-37) — **both gitignored**. Has a `try/except` fallback, so it will silently draw a figure from substitute values if the arrays are missing, which is worse than failing |
| **4** force worldline | `figure4_force_worldline.py` | **NO** | reads a SIM JSON (line 42) but then falls back to hard-coded `dr_vals`/`F_vals` literals at lines 62-63 |

**Score: 3 of 6 today, 5 of 6 after two `.gitignore` exceptions and a path fix.**

### 6.2 What one-command reproduction would take

Achievable, and cheap. Concretely:

1. **De-hardcode the paths.** All six scripts write to absolute `D:/quantum-worldline/...`. Replace
   with a repo-root resolved from `__file__`. (~30 min, mechanical.)
2. **Un-ignore the ≤ 24-qubit arrays** the figures read (24 `.npy` files: transport ×8,
   boundary density ×4, theta ×12). These are small and they are the *inputs* the manuscript's
   availability statement implicitly promises. (~15 min.)
3. **Remove the silent fallbacks.** `figure3` and `figure4` currently draw *something* when their
   data is missing. Make missing data a hard error. This is the single most important change: a
   figure script that cannot fail is the plotting analogue of a test that cannot fail. (~30 min.)
4. **Trace the remaining literals.** `figure4:62-63` (`F_vals = [-0.562, -0.089, -0.032, -0.011,
   -0.002]`), `figure6:60,79` (`chi2_C_r`, `F_16q_exact`) — either point them at the SIM records
   that contain those values or add a comment naming the record. Until then those series have no
   provenance at all. (~1 h, and it is a provenance audit, not typing.)
5. **Add `repro/make-figures.sh`** (and a `.ps1` twin for the Windows primary environment) that runs
   all six in order and diffs the output PNGs against the committed ones. (~1 h.)
6. **Optional but high-value: `repro/make-numbers.sh`** regenerating the four abstract numbers from
   tracked data — α from `interaction_energy_24q.py` + the (to-be-committed) fit script, the
   transport residual from `holographic_transport_finedt.py`, the ALM percentages from
   `sim2026008c_alm_proj_24q.py`, the χ=3 error from `sim2026015c_chi3_16q.py`. Runtime is dominated
   by the 24 q `eigsh` (~20 min) and the χ=3 optimization (~45 min) — well inside an overnight
   referee-check budget. (~half a day.)

**Total: about one day of work for figures + numbers, all six figures, no compute beyond an
overnight run.** Nothing here needs MERAKit or puMPS, because none of the six manuscript figures
depends on them.

### 6.3 What one-command reproduction would *not* reach

The universality and OPE claims (H3, H9) have no figure and no reachable raw data; they enter the
manuscript as numbers quoted from SIM records whose underlying logs are gone. They cannot be
brought into a reproduction script without re-running MERAKit at a revision nobody recorded. Any
honest `repro/` directory should say so in its README rather than imply full coverage.

### 6.4 One thing done right, worth copying

`figure2_alm_convergence.py:29-52` hard-codes its series **but labels each block with the record it
came from** (`# SIM-2026-008b: 8q, seeds 7 and 42`, `# SIM-2026-008c: 24q/5-layer, 5 seeds`).
I checked the transcription against the source: figure literals `3.3637 / 3.3370 / 4.0938 / 5.2397
/ 3.3718` (phase 1) and `3.3365 / 3.3340 / 3.3398 / 4.3014 / 3.3345` (phase 2) against
`SIM-2026-008c.json` `results[].phase1_err` / `phase2_err` = `3.3636791… / 3.3370364… / …` and
`3.3365378… / 3.3339872… / …` — **exact to the quoted digits**, and the `best_error_pct
= 3.33398726605265` is the abstract's "3.33 %". That is a checkable literal. `figure4:62-63` and
`figure6:60,79` are the same *pattern* with the provenance comment omitted, and they are therefore
uncheckable. The difference is one comment line.

---

## 7. UNVERIFIED

Stated explicitly rather than passed over.

1. **Whether the owner has pushed since I checked.** The live GitHub fetch was performed once, on
   2026-08-17, and returned a 2026-06-17 HEAD. If a push happened in the interval this finding's
   *magnitude* changes (though the Zenodo PDF-only finding does not).
2. **Whether Zenodo holds a later, richer version.** I fetched the concept DOI
   `10.5281/zenodo.19660302`, which resolved to **v4 (2026-07-15), one PDF**. Project memory
   references a `10.5281/zenodo.21381474` "v4 published, v5 content" and ERRATA references a v3 DOI
   `10.5281/zenodo.19661227`. I did **not** enumerate every version record; it is possible a
   version exists with attached code that the concept DOI does not surface. The README claim of a
   "full reproduction package" is unsupported by what the concept DOI resolves to, which is the
   link a reader would follow.
3. **Whether any headline number is *wrong*.** Out of scope here and largely settled elsewhere:
   `inv-pipelines.md` re-derived the SIM-067/068/069/070/071 raw values from tracked data and
   independently re-implemented the Yang-Lee driver, matching to 6 decimals. I did not re-run
   anything numerically in this audit; my checks were structural (existence, tracking, resolution,
   key inspection) plus the one transcription cross-check in §6.4.
4. **The exact Python environment any given run used.** `requirements.txt` is pinned but undated
   and unbound to records; I could not determine which records it describes. I did not inspect
   `git log -p requirements.txt` to date the pins.
5. **Whether `interaction_energy_24q.py` as currently tracked is the version that produced
   SIM-2026-011-interaction.** The record names no script and carries no revision. The file mtime
   is 2026-03-18; the record's date is earlier in March. Match is plausible and unproven — which is
   precisely the defect.
6. **Whether the 12 gitignored-but-present `.npy`/`.npz` inputs are byte-identical to what produced
   the recorded numbers.** No checksums exist, so this is unknowable by construction.
7. **The MERAKit.jl upstream identity.** Neither the fork/URL nor a revision is recorded anywhere
   I could find (`RUN-MERAKIT.md`, `Project.toml.pinned`, `CLAUDE.md`, any SIM record). I did not
   attempt to fingerprint the local clone against upstream history.
8. *(Resolved during the audit — kept for the record.)* **Storage cost of un-ignoring the `.npy`
   files: measured.** All 30 total **129 MB**, but that is dominated by one file:
   `gs_24q_exact.npy` is **134 217 856 bytes = 128 MB** (2^24 × float64). Every *other* input the
   figures and headline records need — the 8 `transport_*`, 4 `boundary_density_*` and 12
   `theta_*` arrays — comes to **432 KB combined**. So the §5.2 Tier-2 recommendation splits
   cleanly and needs no Git-LFS: **commit the 432 KB directly**, and deposit `gs_24q_exact.npy`
   on Zenodo only (it is regenerable in ~1 228 s by the tracked `interaction_energy_24q.py`,
   whose own `eigsh` timing the record preserves as `ground_state.eigsh_time_s = 1228.207`).

---

## 8. Defect register (severity-ordered)

| # | sev | defect | evidence |
|---|---|---|---|
| 1 | **critical** | The submitted manuscript's Data-and-Code-Availability statement is unsatisfied at both named endpoints: 8 of 19 named items absent from the public repo; the Zenodo record holds only a PDF | `paper-prd.tex:690-711`; `git cat-file -e origin/public-release:…` per item; live GitHub + Zenodo fetches (§1.3, §5.1) |
| 2 | **critical** | No frozen snapshot exists for a manuscript under review at PRD. Zero git tags; the submission commit `f124038` is unpushed | `git tag` (empty); `git log origin/public-release..public-release` = 85 |
| 3 | **critical** | 0 / 85 records carry an output checksum; 1 / 73 pins the project's own code revision; 0 / 73 name an analysis or fit script | §2.2 items 1, 10, 12 |
| 4 | **major** | Every state/parameter input to the manuscript's force and transport results is gitignored (`*.npy`, 30 files, 0 tracked), while the paper states "all simulation data and scripts are available" | `.gitignore:19`; `git ls-files … \| grep .npy` empty; `paper-prd.tex:693` |
| 5 | **major** | `MERAKit.jl` is gitignored with **no upstream revision recorded anywhere**, and all 11 cited raw logs for SIM-060…066 are absent — so H3 (universality) and H9 (C_σσε), both in the abstract, are neither re-runnable nor re-derivable | `.gitignore:51`; `find` for the 11 logs returns nothing; corroborated `inv-pipelines.md:155-169`, `inv-sims-late.md:1253-1258` |
| 6 | **major** | The two analysis steps producing the program's flagship number (the `h_c^inf` refit and the two-level Richardson estimator) exist nowhere in the repo, and the tracked driver's own gate prints `NOT PASSED` for the run of record | `yl_run_8_18.log` last line vs `SIM-2026-070.json`; `inv-pipelines.md:570-604` |
| 7 | **major** | SIM-071's unitary control — the load-bearing validation of the strongest frontier claim — has **no persisted output anywhere**; `ylks_warn.log` is 0 bytes; the three control values exist only as hand-transcribed prose | `qw_yanglee_ks_results.jsonl` (5 lines, all YL); `inv-sims-late.md:1040-1049` |
| 8 | **major** | `README.md:203` claims a "full reproduction package" is archived on Zenodo; the record contains one PDF | README vs live Zenodo fetch |
| 9 | **major** | No RNG seed recorded in any record after SIM-2026-015c (2026-04). 9 / 73 overall; the five later "seed" fields are run-index labels, not RNG values | §2.2 item 5; `best_spectrum_seed.seed` key-path inspection |
| 10 | **major** | The manuscript's central α record names no driver, no input file, and no fit script | `SIM-2026-011-interaction.json` complete key set (§3.3) |
| 11 | **major** | `figure3_transport_trace.py` and `figure4_force_worldline.py` **silently fall back to substitute values** when their data is missing, rather than failing | `figure3:34-45` `try/except np.load`; `figure4:42,62-63` |
| 12 | medium | 5 of the 12 headerless JSON files are cited as manuscript primary data; 2 of those have no `id`, `date`, `description`, `type` or `script_path` | §1.1, §2.4 |
| 13 | medium | The Zenodo-archived PDF is the SciPost version (v4, 2026-07-15), not the submitted PRD manuscript (2026-08-07); the DOI in the submitted paper resolves to a different document | `diff` of the two `.tex`; live Zenodo fetch |
| 14 | medium | Project schema conformance has not improved since ERRATA D3 was written: 30 / 73 lack `description`, 24 lack `type`, 17 lack `date`, 11 fail the `id` regex, 20 have `type` outside the enum | §2.4; `ERRATA.md:75` |
| 15 | medium | No Julia dependency manifest is tracked for any run (`git ls-files \| grep -i manifest` empty); the puMPS `Project.toml` is explicitly gitignored with the source | `VENDOR.md`; repo scan |
| 16 | medium | `requirements.txt` is a single current-state file bound to no record and cannot describe both the 2026-03 and 2026-08 environments | root `requirements.txt`; no per-record reference to it anywhere |
| 17 | medium | 20 / 73 records reference at least one artifact absent from the repository; 22 / 73 reference at least one present-but-gitignored artifact | §2.3 link resolution |
| 18 | minor | `SIM-2026-022.json` `visualization_path` is a broken link; `SIM-2026-042.json` references `simple_mera.py`, which does not exist | `ls`, `find` |
| 19 | minor | `research/data/theory/` holds 8 prose `.md` files and 0 structured records, and **no `templates/theory-record.json` exists** — so the tier cannot be conformant even in principle (§14) | `ls research/data/theory/`, `ls templates/` |
| 20 | minor | No `.patch` file for the two prose-described puMPS patches; a reproducer must hand-edit two files in a repo they must fetch themselves | `VENDOR.md:79-88`; corroborated `inv-pipelines.md:94-96` |
| 21 | minor | `figure4:62-63` and `figure6:60,79` hard-code comparison series with no provenance comment, unlike `figure2` which names its source records | §6.4 |
| 22 | minor | `README.md:119` and `:157` both say "69 simulation records (through SIM-067)"; there are 73 through SIM-071 | README vs `ls research/data/simulations/SIM-*.json` |

---

## 9. What would most improve reproducibility, ranked by evidence-gained / effort

1. **Push.** Everything else is inert while the public endpoint is 61 days and 85 commits stale, and
   a referee following the manuscript's own URL finds no universality data and no drivers. Minutes.
2. **Tag `f124038` and deposit a `git archive` of it as a Zenodo version alongside the PDF**, then
   correct `README.md:203`. This is the §21 last-paragraph requirement and it is currently
   unsatisfied for a paper under review. ~1 hour.
3. **Add `.gitignore` exceptions for the 24 small `.npy` inputs (432 KB total, measured) and for
   the 5 MERAKit logs that already exist inside the ignored tree.** No re-runs, no LFS; converts
   several D grades to B. ~30 min. (Handle the one 128 MB ground-state file via Zenodo, not git.)
4. **Commit the two missing analysis scripts** (`h_c^inf` fit, Richardson estimator) and re-run the
   Yang-Lee unitary control with stdout captured. This is the difference between the program's
   flagship claim being reproducible and being a transcription. ~2 hours.
5. **Record the MERAKit upstream URL + commit in `RUN-MERAKIT.md`**, copying the `VENDOR.md`
   pattern the project already got right for puMPS. ~15 min, unblocks two abstract claims.
6. **Add `script_path` (and, where it exists, the seed) to the eight headline records that lack
   it**, and a header block to the five headerless files the manuscript cites. ~1 hour.
7. **`repro/make-figures.sh` with hard failures on missing data.** ~2 hours, gets 5 of 6 figures to
   one command.
8. **Emit `MANIFEST.sha256` at snapshot time.** The cheapest possible fix for the 0 / 85 checksum
   item, and the only thing that would have caught the SIM-070 log/record divergence automatically.
   ~15 min.
