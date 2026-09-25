# inv:pipelines — Numerical Pipeline Audit

**Auditor task:** `inv:pipelines`. Governing standard: `docs/governance/RESEARCH-DIRECTOR.md`
(§5 contribution levels, §6 counterfactual novelty, §7 independence ledger, §8 novelty gates,
§12 killer tests, §20 uncertainty, §21 reproducibility, §38 audit assignment).
**Date of audit:** 2026-08-17. **Repo state:** branch `public-release`, HEAD `9470d69`.

All paths below are repo-relative to `D:/quantum-worldline/`.

---

## 0. Executive summary of this artifact

Five de facto numerical pipelines exist; the task named four. Findings in one paragraph:

- **Every raw per-point number I re-derived from tracked data reproduced exactly.** I re-ran the
  SIM-067/068/069 extrapolations from the tracked raw files, the SIM-070 `h_c^inf` fit from the
  tracked `h_c^L` table, the SIM-070 Richardson tail, and the SIM-071 Richardson tail. All match
  the recorded values to the quoted digits.
- **I additionally re-implemented `qw_yanglee_ks.jl` from scratch in Python (ARPACK instead of
  KrylovKit) and reproduced both the Yang-Lee c_KS ladder and the unitary control to 6 decimals.**
  This is an *independent code path* the project does not itself have, and it confirms the raw
  measurements. It does **not** confirm the extrapolation or the physics interpretation.
- **The single largest defect is a mislabelled cross-pipeline comparison** in
  `pumps-setup/VENDOR.md`: the puMPS Ising gate is compared against SIM-067's *extrapolated*
  number rather than SIM-067's value *at the same N*, hiding a 7 % same-N disagreement in `c`.
  I traced the cause: the two pipelines use **different Koo–Saleur mode discretizations** (naive
  vs. half-bond phase). I verified this by rebuilding SIM-067's ED with the puMPS convention —
  agreement then becomes 5e-6 at N=12. The convention difference is documented **nowhere**.
- **The second largest defect is an understated systematic in SIM-071.** Its claim that residual
  `h_c^inf` error contributes "≤0.01" to `c_KS` at L=18 is wrong by roughly a factor of 5–6 for the
  Δh the record itself cites, and by more than an order of magnitude across the plausible fit-model
  spread. Measured directly (see §5.6).
- **`C_TTT` is not an independent measurement in any of the three ladder rungs.** In every driver it
  is computed as the literal line `C_TTT = 2*sqrt(2)/sqrt(c)`. The "C_TTT ladder" is an algebraic
  restatement of a central-charge measurement. The design docs say so; the headline framing in
  memory/`NEXT-SESSION.md` does not.
- **The Yang-Lee unitary control shares 148 of 152 lines with the measurement it validates**, and
  the four differing lines include the one (`HC = 0.0`) that switches non-Hermiticity **off**. It
  is a strong test of the Koo–Saleur estimator and a null test of the plumbing; it exercises none
  of the biorthogonal machinery — the biorthogonal norms are exactly +1.000000 in the control.
  Full component-by-component breakdown in §5.3–5.4.
- **Raw artifacts are missing for the entire MERAKit pipeline** (every SIM cites `scratchpad *.log`,
  none in repo) and for the **Yang-Lee unitary control** (the single most load-bearing validation in
  the program's strongest result has zero retained output).

---

## 1. Pipeline inventory (what actually exists)

| # | Pipeline | Tracked dir | Vendored/gitignored code | Language / runtime | SIM records produced |
|---|---|---|---|---|---|
| P1 | Scale-invariant **MERA** (Z₂/Z₃-symmetric), scaling dims + OPE constants | `research/tools/merakit-setup/` | `research/tools/MERAKit.jl/` (gitignored, `.gitignore` L58) | Julia **1.8.5** via `+1.8`, pinned TensorKit/TensorOperations-3 era | 050, 051, 052, 056, 058, 059, 060, 061, 062, 063, 064, 065, 066 |
| P2 | **Periodic-chain ED** Koo–Saleur (circle route) | `research/tools/cttt-circle/` | none — fully self-contained | Python + scipy sparse | 067 |
| P3 | **puMPS** Bloch-state Koo–Saleur | `research/tools/pumps-setup/` | `research/tools/puMPS/` (gitignored, `.gitignore` L61) | Julia **1.12.x** default channel | 068, 069 (+ the Ising validation gate) |
| P4 | **Biorthogonal non-Hermitian ED** (Yang-Lee) | `research/tools/yanglee-pt/` | none — fully self-contained | Julia + KrylovKit | 070, 071 |
| P5 | *(not in scope but real)* boundary-primary **force / transport** pipeline | `research/data/simulations/*.py` (131 loose scripts) | — | Python | 011, 015d, 023, 025, 053, 055, … |

**Structural note (defect, minor):** P5 is a full production pipeline with no `research/tools/`
home, no design doc, and no VENDOR-style provenance file — 131 loose `.py` files sitting in the
*data* directory (`research/data/simulations/`). Every headline in the submitted PRD manuscript
(α=4 force, transport T=(π/2)·l_AdS, m_eff) comes from P5, i.e. from the *least* organised
pipeline in the repo. `CLAUDE.md` documents P1/P3 conventions and says nothing about P5.

### 1.1 What is vendored and therefore NOT reproducible from this repo alone

- **`research/tools/MERAKit.jl/`** — external clone. `.gitignore` line 58:
  `# external MERAKit.jl clone (keep RUN-MERAKIT.md + our pinned Project.toml/setup tracked separately)`.
  No upstream commit pin is recorded anywhere (contrast puMPS, which pins `0557b12a...`).
  `merakit-setup/Project.toml.pinned` records the dependency pin but not the MERAKit revision.
  **This is a reproducibility gap**: the P1 results (SIM-050/051/052/061/062/063/064) cannot be
  reconstructed without knowing which MERAKit.jl revision was used.
- **`research/tools/puMPS/`** — vendored `yijian-physics/puMPS`, commit `0557b12a387091f96b83900e99bdb13c5f393839`
  (2025-09-14, branch `main`), with the exact `curl` fetch line recorded in `pumps-setup/VENDOR.md:10-12`.
  Gitignored because **the upstream repo carries no license** (`VENDOR.md:13-16`) — a deliberate,
  correctly-reasoned decision, with `FuTen/puMPS.jl` (MIT) named as the redistribution fallback.
  This is the *good* pattern; MERAKit should be brought to the same standard.
- `research/tools/juliahome/` — the clean-`HOME` shim required by the Windows ACL workaround
  (`merakit-setup/RUN-MERAKIT.md:10-11`); gitignored, environment-only, no scientific content.

### 1.2 Local patches to vendored code (`pumps-setup/VENDOR.md:79-88`)

Two patches, both to the gitignored `puMPS/` tree, both documented and both re-applied by hand
after any re-fetch (there is **no patch file and no script** — the instructions are prose):

1. **`models.jl` `weylops` (~L492)** — upstream pre-Julia-1.0 syntax `V = diagm(ones(p-1), 1)`
   throws `MethodError`; patched to `V = diagm(1 => ones(p-1))`. **Required** for the 3-state Potts
   path (SIM-069). Only `potts3` calls `weylops`, which is why upstream's 2025-09-14 "Julia 1.11
   refresh" missed it.
2. **`states.jl` `minimize_energy_local_CG!`** — added kwarg `pinv_tol::Real=1e-12`, threaded to
   `gradient_central(...)` in the `use_phys_grad` branch. Honestly recorded as **not** having moved
   the d=3 CG floor (`VENDOR.md:87-88`, and again in `SIM-2026-069.json:44`).

**Defect (minor):** the patches are prose-only. A `.patch` file (or a `git apply`-able diff) in
`pumps-setup/` would make the vendored tree reconstructible in one command. As written, an
independent reproducer must hand-edit two files in a repo they must fetch themselves.

**Verified:** `pumps-setup/*.jl` are **byte-identical** to the run copies in `puMPS/`, and the two
tracked `*_results_*.jsonl` files are byte-identical to `puMPS/qw_cttt_of_results.jsonl` and
`puMPS/qw_cttt_potts3_results.jsonl`. The P3 mirror discipline is clean.

**Defect (minor), P1 mirror drift:** `CLAUDE.md` states that after editing any `qw_*.jl` in
`MERAKit.jl/` it must be copied to `merakit-setup/`. Byte-comparison of all 17 mirrored drivers:
16 identical, **`qw_tci.jl` DRIFTED**. The tracked mirror (`merakit-setup/qw_tci.jl`, mtime
Jun 20 22:57) uses `block_size=3` → dim-8 blocked sites, 3 layers, `load_hb`; the vendored working
copy (`MERAKit.jl/qw_tci.jl`, mtime Jun 20 23:13, **newer**) uses `block_size=2` → dim-4 sites,
4 layers, `load_hb4`. These are different physical setups, and the *tracked* file is the stale one.
Additionally **9 scripts exist only in the gitignored tree** and were never mirrored:
`qw_diag_blocking.jl`, `qw_diag_blocking2.jl`, `qw_diag_fusion.jl`, `dump_ising.jl`,
`diag_prefactor.jl`, `instantiate.jl`, `qw_potts_smoke.jl`, `test_cone_v2.jl`, `qw_block_test.py`.

---

## 2. P1 — MERAKit (scale-invariant MERA, `merakit-setup/`)

### 2.1 What it computes
Optimises a ternary scale-invariant MERA on a blocked lattice Hamiltonian, then reads:
- **scaling dimensions** from the scaling superoperator (Δ_σ, Δ_ε, Δ_T → the α = 2Δ_T claim);
- **OPE structure constants** via the PEV route (`qw_ope_pev_z2.jl`, design in
  `merakit-setup/OPE-PEV-ROUTE-DESIGN.md`): C_σσε, C_σσσ, C_εεε;
- an attempted **C_TTT "Route A"** (`qw_ope_cttt.jl`, design `CTTT-SPIN-RESOLUTION-DESIGN.md`).

Models: critical Ising (`qw_ising_chi6.jl`), O'Brien–Fendley TCI (`qw_tci*.jl`, `of_build_v2.jl`,
`build_of_blocked.py`), 3-state Potts (`qw_potts_z3.jl`, `qw_potts_chi8.jl`).

### 2.2 Validated against what, and what the validation achieved

| Gate | Target (exact) | Achieved | Record |
|---|---|---|---|
| Ising Δ_σ | 1/8 | 0.1234–0.1253 across 8 seeds (worst 1.3 %) | `SIM-2026-061.json:13` |
| Ising Δ_ε | 1 | 1.008–1.020 | `SIM-2026-061.json:14` |
| TCI Δ_σ, Δ_ε, Δ_T | 3/40, 1/5, 2 | 0.092 / 0.204 / 1.9994 (χ=8, best basin) | `SIM-2026-052.json` verdict |
| Potts Δ_σ | 2/15 = 0.1333 | 0.089 (χ=6) → 0.14 (χ=9) → 0.133 (χ=12) | `SIM-2026-063.json` |
| **C_σσε** | 0.5 (BPZ 1984) | χ=6 mean 0.5075, spread 0.128; χ=8 mean 0.5069, spread 0.0315; χ=10/12 drifted 5.6 % **low** | `SIM-2026-061.json:15,21`, `SIM-2026-064.json` |
| C_σσσ (Z₂-forbidden) | exactly 0 | **exactly 0** on all 8 seeds — structural, not fitted | `SIM-2026-061.json:17` |
| C_εεε (KW-forbidden) | 0 | 0.03–0.28 — **did not** shrink with χ; correctly downgraded to "diagnostic only" | `SIM-2026-061.json:21` |
| **C_TTT Route A** | 4.000 | χ=10: 8.29, 146.1. χ=12: 2.22, 2.15, 25.7, 0.057. One seed 6e8. | `SIM-2026-066.json` verdict |

**Assessment.** P1's honest negatives are its best feature. `SIM-2026-066` is a clean, correctly
reported **decisive negative**: χ-escalation made C_TTT scatter *worse* (450× spread among
"perfect-gate" seeds), and Route A was closed rather than salvaged. `SIM-2026-064` flags an
**accuracy puzzle** (precision improved 40× while the mean drifted through the exact answer to
5.6 % low) instead of quoting the tight-spread number. Both are RESEARCH-DIRECTOR §32 behaviour.

**Counterfactual novelty (§6): near-zero for every P1 number.** Δ_σ=1/8, Δ_ε=1, Δ_T=2, C_σσε=1/2 are
all fixed by the Ising Virasoro minimal model; Δ_T=2 holds in *every* 2D CFT. C_σσσ=0 and C_εεε=0 are
selection rules. The only possible outcomes were "implementation works" / "implementation fails".
That is Level 1 (validation) under §5, and `CTTT-ROUTE-B-CIRCLE-DESIGN.md:96-102` says so explicitly
("this measurement is of the same epistemic kind as C_σσε = 0.5"). The **methodological** content
(Z₂/Z₃-symmetric tensors converting a "dense basin lottery" — 2/8 clean at χ=8 — into 8/8 clean
basins; `SIM-2026-061.json:12`, `SIM-2026-062.json`) is a genuine Level 2 contribution.

### 2.3 Reproducibility — the worst in the repo

**Every P1 SIM record cites raw artifacts that are not in the repository.** Verified by
`git ls-files research/tools` and by `ls -d scratchpad*` (no such directory anywhere):

- `SIM-2026-061.json:23` → `"scratchpad z2_v4_gate.log"` — **absent**
- `SIM-2026-062.json` files → `"scratchpad potts_z3_chi6.log"` — **absent**
- `SIM-2026-063.json` files → `"scratchpad potts_chi9.log / potts_chi12.log"` — **absent**
- `SIM-2026-064.json` files → `"scratchpad ope_chi10.log / ope_chi12.log / ope_chi12_m8000.log"` — **absent**
- `SIM-2026-065.json` files → `"scratchpad cttt_smoke0.log / cttt_chi6_smoke.log / …"` — **absent**
- `SIM-2026-066.json` files → `"scratchpad cttt_chi10_s1..8.log / cttt_chi12_s1..8.log"` — **absent**

`merakit-setup/` contains **only drivers and design docs — zero result files.** Consequence: every
per-seed number in the P1 records (the 8 C_σσε values, the χ=12 Route-A scatter, the Potts χ-ladder)
exists **only as prose inside the SIM JSON**. Nothing can be recomputed, re-fitted, or checked
without re-running the whole pipeline against an unpinned MERAKit revision. This fails
RESEARCH-DIRECTOR §21 on: code revision, output checksums, input records, analysis-script revision.
Contrast P3/P4, which both retain tracked `.jsonl`/`.log` artifacts.

Also: some P1 result logs *do* exist inside the gitignored tree (`MERAKit.jl/qw_potts_chi8.log`,
`qw_tci_measure.log`, `v2_smoke.log`, `qw_of_control_correct.log`, `diag.log`) — i.e. the artifacts
were produced and then left on the ignored side of the boundary. This is a one-line `.gitignore`
fix, not a re-run.

### 2.4 P1 adversarial-test record (§22) — good
`memory: of_blocking_was_never_wrong` and `SIM-2026-051/052` record a real caught failure mode:
**MERA energy is flat across basins at χ=6, so basins must be selected by spectrum, not energy.**
An exact-diagonalisation pre-gate (`qw_of_pregate.py`, `qw_of_pregate_compare.py`, both tracked)
was built specifically to prove the 3-site OF blocking exact (λ₃=0 and 0.856). That is exactly the
"recreate the known failure so it cannot silently return" discipline §22 asks for.

---

## 3. P2 — Periodic-chain ED Koo–Saleur (`cttt-circle/`)

### 3.1 What it computes
`qw_cttt_circle.py` (397 lines, self-contained, scipy sparse). Two *distinct* routes in one file:
- `analyze()` — equal-time connected correlators ⟨hh⟩, ⟨hhh⟩ against chord kinematics, giving
  `C_TTT = √2·A₃/|A₂|^{3/2}` (L293) — a genuinely independent 3-point measurement;
- `koo_saleur()` — Fourier modes `H_n = Σ_x e^{inx·2π/N}(h_x − e₀)` (L180-184) and
  `c_meas = 2|⟨T|H_{±2}|0⟩|²` (L201), with **`C_TTT = 2√2/√c_meas` (L203)**.

### 3.2 What was validated, and what it achieved

`CTTT-ROUTE-B-CIRCLE-DESIGN.md:108-117` records a **same-day falsification of the design's own
§3**: the equal-time correlator route was killed by ED within the hour (⟨hh⟩_conn came out
*negative*, decayed faster than s(x)⁴, and vanished exactly at antipodal separation; exact
free-fermion tail −(16/π²)/(4x²−1)²). The design doc says plainly: *"do not quote §3's A₂/A₃
formulas."* That is model behaviour under §32 — and it means **the one independent 3-point route
in the whole program was retracted**, leaving only the algebraic `2√2/√c`.

The surviving KS route's gates (from `qw_cttt_circle_results_ising.json`, N=8…18, tracked):

| Gate | Target | Achieved |
|---|---|---|
| conformal spin s_T | ±2 exactly | `s_T` = 2.0000000000000004 at every N (translation eigenphase) |
| G4 wrong-chirality element | 0 (structural) | 2.3e-15 … 2.1e-14 at every N |
| c_meas → | 0.5 | **0.49871** (1/N² fit; I re-ran the fit — exact match) |
| C_TTT → | 4.000 | **3.99361** (independent 1/N² fit; re-ran — exact match) |
| C_σσε (matrix-element) → | 0.5 | **0.49996** (re-ran — exact match) |
| TCI (`--model of`, λ₃=0.856) | c → 0.7 | **FAILED**: c_meas 1.446 → 1.209 over N=10…16, drifting. Honestly reported as not-converged, cause diagnosed (L₋₂ε at Δ=2.2, element mixing ~N^−0.2) |

### 3.3 DEFECT (major): `C_TTT` is algebraically `c`, and the two extrapolations disagree

`qw_cttt_circle.py:203` is literally `res["C_TTT"] = 2*np.sqrt(2)/np.sqrt(res["c_meas"])`.
The `main()` extrapolator (L382-390) then fits `c_meas` and `C_TTT` **separately** in 1/N².
Consequence, which I computed from the tracked results file:

- fitted `c_meas(N→∞) = 0.49871` ⟹ implied `C_TTT = 2√2/√0.49871 = **4.00517**` (0.13 % high)
- separately fitted `C_TTT(N→∞) = **3.99361**` (0.16 % low)

The two are **0.29 % apart** — larger than either quoted deviation. SIM-067 quotes the second.
The headline "C_TTT = 3.9936 vs 4.000 (0.16 %)" is therefore an estimator-choice artifact of
extrapolating a nonlinear function of the measured quantity rather than the quantity itself.
Neither number is wrong; quoting one as *the* result without the other overstates precision.

### 3.4 DEFECT (major): non-standard Koo–Saleur mode discretization, undocumented

`qw_cttt_circle.py:183` applies **one** phase `e^{inx·2π/N}` to the whole 2-site term
`h_x = −(X_xX_{x+1} + Z_x)`. Every other KS implementation in the repo — the vendored ZMV
`puMPS/models.jl:105,320-321,460,554-555`, the Potts ED gate `pumps-setup/qw_potts_ed_gate.jl:92`,
and the Yang-Lee driver `yanglee-pt/qw_yanglee_ks.jl:35` — applies the **half-bond** convention:
site phase `e^{inj·2π/N}`, **bond phase `e^{in(j+½)·2π/N}`**.

**I tested this directly.** Re-running SIM-067's own ED with only the bond phase changed:

| N | naive phase (as in SIM-067) | half-bond phase (ZMV/puMPS) |
|---|---|---|
| 10 | c = 0.448547 | c = 0.495901 |
| 12 | c = 0.463848 | c = **0.497151** |
| 14 | c = 0.473251 | c = 0.497905 |
| 16 | c = 0.479427 | c = 0.498396 |

The half-bond convention has ~10× smaller finite-size error at every N. **No SIM record, design
doc, or VENDOR note mentions that the conventions differ.** SIM-067's "0.16 %" is the result of a
1/N² extrapolation rescuing a comparatively poor discretization.

---

## 4. P3 — puMPS Bloch-state Koo–Saleur (`pumps-setup/`)

### 4.1 What it computes
Periodic uniform MPS ground state (`minimize_energy_local_CG!`), Bloch-state excitations at
k = 0, ±2 (`excitations!`), KS matrix elements via `Hn_in_basis`, then
`c = 2|M_T|²` and — again — `C_TTT = 2√2/√c`
(`qw_cttt_of.jl:116-117`, `qw_cttt_potts3.jl:131-132`, `qw_pumps_validate_ising.jl:79-82`).

### 4.2 Validation ladder — what it achieved

**(a) Ising gate, `qw_pumps_validate_ising.jl`, N=12 D=8** (`validate_run_2026-08-09.log:2411-2462`):

| quantity | puMPS | exact |
|---|---|---|
| e₀/site | −1.2768824787 | ED at N=12 gives −1.2768824... (matches to 10 digits) |
| Δ_T (energy) | 1.960387 | 2 (finite-N) |
| KS \|M\| for T | 0.498576 (n=+2), 0.498575 (n=−2) | chirality-symmetric to 1e-6 |
| c_meas | 0.497156 / 0.497155 | 0.5 |
| other k=2 state element | 0.000078 (6400× smaller) | — |
| wrong-chirality element | 0.000000 | structural (momentum conservation in `Hn_in_basis`) |

**(b) Potts ED gate, `qw_potts_ed_gate.jl`, N=10** (`SIM-2026-069.json:7-10`): E₀/site to 1.4e-6,
T gap to 1.8e-4 relative, velocities to <1e-4, gap ratio 6.1929 vs ED 6.1924. This gate exists
because the d=3 CG optimiser plateaus at |grad| ≈ 2.5e-4 and cannot be driven lower; the record
is explicit that "measurement quality is certified by the N=10 ED gate, **not** by |grad|"
(`qw_cttt_potts3.jl:64-66`). Correct methodology, honestly labelled.

**(c) Production ladders** — both fully reproducible from tracked `.jsonl`:

| model | N ladder (best D) | c per rung | fit → c_∞ | C_TTT |
|---|---|---|---|---|
| TCI (OF, λ₂=0.428) | 14/20/28/40/56 | 0.8295, 0.75633, 0.72421, 0.71065, 0.70375 | **0.69858** (p=2.31) | 3.381 ± 0.005 vs 3.38062 |
| Potts (h=1) | 14/20/28/40 | 0.82201, 0.81054, 0.80500, 0.80197 | **0.79891** (p=1.92) | 3.163 ± 0.003 vs 3.16228 |

I re-ran both three-parameter `c(N) = c_∞ + a·N^{−p}` fits from
`pumps-setup/qw_cttt_of_results_2026-08-10.jsonl` and
`pumps-setup/qw_cttt_potts3_results_2026-08-11.jsonl`. Reproduced to 5 decimals:
`all5` → 0.69858/p=2.31 (record: 0.69858/2.31); `all4` → 0.79891/p=1.92 (record: 0.79892/1.93);
`drop_N14` → 0.79886 (record: 0.79887); `with_N10` → 0.79906 (record: 0.79906). **Clean.**

### 4.3 Genuine strengths worth recording
- **L₋₂ε contamination suppression** (`SIM-2026-068.json:32`): the ~N^−0.2 element mixing that
  made TCI unreachable by ED is suppressed to ≤0.0003 vs T's 0.109 (≈400×) at N=56, and the
  observed correction exponent is p ≈ 2.4, not 0.2. This is a real Level-2 methodological result
  and is the strongest candidate in the repo for RESEARCH-DIRECTOR §25 Candidate Paper C.
- **Two-error cancellation used *predictively*** (`SIM-2026-069.json:23`): N=40 D=28 was called at
  0.8022 ± 0.0005 from D-shift systematics *before* the run and landed at 0.80197. That is §18
  out-of-sample prediction, correctly executed and correctly recorded.
- **Stopping rule stated and honoured** (`SIM-2026-069.json:36`): N=56 omitted deliberately because
  a 5th rung "cannot change the verdict". §30/§31 behaviour.

### 4.4 DEFECT (major): the step-1 validation table compares mismatched quantities

`pumps-setup/VENDOR.md:50` puts **"C_TTT 4.0114 (raw N=12)"** in the same row as
**"4.000 (SIM-067 extrapolated 3.9936)"** and concludes "The puMPS pipeline reproduces the SIM-067
circle/KS extraction."

SIM-067's own value **at N=12** is `C_TTT = 4.152954`, `c_meas = 0.463848`
(`cttt-circle/qw_cttt_circle_results_ising.json`, N=12 entry). puMPS at N=12 gives `c = 0.497156`.
**That is a 7.2 % disagreement in c between the two pipelines at matched N**, presented as
agreement by substituting the extrapolated number for the same-N number.

The disagreement is **fully explained** by the convention difference of §3.4 — and once corrected
the cross-check becomes far *stronger* than claimed. From my §3.4 table, ED at N=12 with the
half-bond convention gives `c = 0.497151`, `|M| = 0.498573`, against puMPS's `0.497156`/`0.498576`:
**agreement to 5e-6 in c and 3e-6 in the matrix element.** That is a real, matched-N,
independent-implementation (Python/scipy dense ED vs Julia/puMPS variational Bloch states)
cross-validation. The project has it and does not know it, because the record compares the wrong
pair of numbers.

**Recommendation:** replace the VENDOR.md step-1 row with the matched-N comparison, and add a
paragraph documenting the KS mode-discretization convention (it is the difference between a
1e-5-level and a 7 %-level cross-check).

### 4.5 Lesser findings
- The Ising gate is **a single point** (N=12, D=8). `validate_run_2026-08-09.log` shows the
  `validate(16, 12)` stage started (line 2465) and the log ends mid-CG — the external kill that
  `VENDOR.md:53-56` documents. Recorded honestly; still, the gate rests on one (N, D).
- `qw_pumps_validate_ising.jl:24` hardcodes `v_exact = 2.0` rather than self-calibrating, so the
  Ising gate does not exercise the `v_T`-from-Δ_T=2 calibration that the TCI/Potts production runs
  depend on. That calibration is first exercised only in production.
- No fit/analysis script is tracked for P3 either — the `variants` tables in
  `SIM-2026-068.json:21-27` and `SIM-2026-069.json:25-34` were produced by untracked code. Unlike
  P1 this is recoverable (I recovered it), because the raw `.jsonl` **is** tracked.

---

## 5. P4 — Biorthogonal non-Hermitian ED, Yang-Lee (`yanglee-pt/`)

This is the program's strongest frontier claim, so it gets the longest treatment.

### 5.1 What the two drivers compute

**Phase 1 — `qw_yanglee_pt.jl` (152 lines).** Builds `H_YL = -Sum(sz sz + lam sx + i h sz)` PBC
(`build_H`, L23-44), lam=4. Bisects the finite-size exceptional point `h_c^L` on Im(E) of the lowest
pair (`find_hcL`, L56-69), fits `h_c^L = h_c^inf + a L^-b` with a **free-b scan over 0.8:0.01:4.0**
(L98-105), then computes biorthogonal projected amplitudes `Z_{X,i} = <X|Psi_R><Psi_L|X>/<Psi_L|Psi_R>`
with left = parity-image of right (L72-84), targeting PAPER-133's `g_1` and the **negative** ratio
`R_inf -> -(1+sqrt5)/2`.

**Phase 2 — `qw_yanglee_ks.jl` (152 lines).** Same model plus **KS-phased** operators
`H_{+-2}` (`build_Hn`, L28-51, using the half-bond phase of section 3.4), momentum-resolved via a
translation-composed non-Hermitian Arnoldi (L69-76), then the **product-form** estimator (L109-129):

```
c_KS = 2 * <0_L|H_-2|T_R><T_L|H_+2|0_R> / (<T_L|T_R><0_L|0_R>) * (L/2 pi v_T)^2
```

### 5.2 INDEPENDENT REPRODUCTION (strongest positive finding of this audit)

I re-implemented `qw_yanglee_ks.jl` line-for-line in Python — different language, different
eigensolver (ARPACK `scipy.sparse.linalg.eigs` vs KrylovKit `eigsolve`), independently written
sparse builders — and ran both modes:

| L | mode | my Python `c_KS` | repo value | source |
|---|---|---|---|---|
| 10 | yl | -1.413195 | -1.413195 | `qw_yanglee_ks_results.jsonl:1` |
| 12 | yl | -1.702883 | -1.702883 | `...jsonl:2` |
| 14 | yl | -1.953729 | -1.953729 | `...jsonl:3` |
| 12 | **ising** | **+0.517483** | 0.517483 | `SIM-2026-071.json:9` |
| 14 | **ising** | **+0.512776** | 0.512776 | `SIM-2026-071.json:9` |
| 16 | **ising** | **+0.509748** | 0.509748 | `SIM-2026-071.json:9` |

**All six agree to 6 decimals.** The raw per-L measurements of SIM-071 — including the unitary
control, for which the repo retains *no artifact at all* — are confirmed by an independent code
path. This is the RESEARCH-DIRECTOR section-40 "reproduce the Yang-Lee result through an
independent code path" slice, and it passes at the level of the raw numbers. It says nothing about
the extrapolation or the interpretation.

Additional facts my run exposed that are **not** in any record:
- **Vacuum biorthogonal norm <1|1> at Yang-Lee: -0.010656 (L=10), -0.003996 (L=12), -0.001507 (L=14).**
  SIM-071 claims the sign ("NEGATIVE at every L", `SIM-2026-071.json:17`) with no supporting
  artifact; the sign is **confirmed**, and the magnitude is now on record.
- In the **Ising control** the same quantity is exactly **+1.000000** at every L (imag <= 2e-16), and
  <T|T> = +1.000000 exactly. See 5.4 — this is the crux of the control's weakness.
- At Yang-Lee, <T_L|T_R> decays 0.09615 -> 0.04786 -> 0.02359 -> 0.01150 -> 0.005539 over
  L = 10..18 (`qw_yanglee_ks_results.jsonl`, `Tnorm` field) — a factor ~2.03 per dL = 2, i.e.
  **exponential**. <1|1> decays even faster (~2.65 per dL = 2). See 5.7.

### 5.3 ANSWER TO THE TASK'S SPECIFIC QUESTION — what the unitary control shares with the Yang-Lee run

`qw_yanglee_ks.jl:23-25` is the entire mode switch:

```julia
const MODE   = length(ARGS) >= 3 ? ARGS[3] : "yl"
const LAMBDA = MODE == "ising" ? 1.0 : 4.0
const HC     = MODE == "ising" ? 0.0 : 1.5587127
```

plus two later branches, L84 (`ivac`) and L86 (`v`). **Four scalar/branch differences in a
152-line file.** Precisely:

**SHARED — byte-identical code executed in both modes:**

| Component | Lines | Note |
|---|---|---|
| Hamiltonian + KS-operator builder `build_Hn` | 28-51 | same function; only `LAMBDA`, `h` differ as *arguments* |
| parity permutation `parity_perm` | 53 | |
| translation permutation `transl_perm` | 55-62 | |
| translation-composed Arnoldi `f = x -> (H*x .- S.*x)[tp]`, `eigsolve(..., 24, :LM; ishermitian=false, krylovdim=90, tol=1e-11, maxiter=400)` | 70-72 | identical call, `ishermitian=false` **even in the Hermitian case** |
| energy decoding `ens = S .- abs.(vals)` | 73 | |
| momentum decoding `ks = round(mod(angle(-l)/(2pi/L) + L/2, L) - L/2)` | 75 | |
| **biorthogonal pairing** `lv(i) = conj.(vecs[i][pp])`, `biod(i,j) = transpose(lv(i))*vecs[j]` | 93-94 | identical definition |
| both-orientation product + structural-zero selection (`pa` vs `pb`) | 109-117 | |
| **Delta-gate window `1.75 < D_vac < 2.25`** | 124 | same hard-coded window in both modes |
| in-window element-dominance `jT = cand[argmax(abs.(prods[cand]))]` | 127 | |
| `v_T = (E_T - E_vac)*L/(2 pi * 2.0)` | 128 | Delta_T = 2 **imposed**, not measured, in both modes |
| product-form estimator `c_KS = 2*prods[jT]*(L/(2 pi v_T))^2` | 129 | |

**DIFFERENT:**

| # | Component | Yang-Lee | Ising control | Consequence |
|---|---|---|---|---|
| 1 | `LAMBDA` | 4.0 | 1.0 | different model |
| 2 | `HC` | 1.5587127 | **0.0** | **at h=0 the `-im*h*mz*sph[j]` term in `build_Hn` (L43) vanishes identically, so H becomes real symmetric — i.e. Hermitian** |
| 3 | `ivac` | `i0[2]` (2nd k=0 state = conformal vacuum \|1>) | `i0[1]` (physical GS) | different state-identification rule |
| 4 | `v` reference | `(E1-Ephi)L/(2 pi (2/5))` | `(E1-Ephi)L/(2 pi (1/8))` | different exact input |

### 5.4 What that means for the strength of the control

**The control validates:** the KS Fourier-mode construction including the half-bond phase; the
translation-composed momentum resolution and its `angle(-lambda)` decoding; the product-form
estimator and its factor of 2; the orientation-selection logic; the Delta-gate + in-window
dominance machinery; the `v_T`-from-Delta_T=2 normalization; the overall `(L/2 pi v_T)^2` prefactor.
In the control these deliver 0.5097 at L=16 (1.9% from exact) and 0.49986 extrapolated (0.03%).
**That is a real and non-trivial pass, and it is the right control to have built.**

**The control does NOT validate anything non-Hermitian.** Because difference #2 sets h=0, the
Hermitian limit is exact, and every non-Hermitian risk surface collapses:

1. **Indefinite metric never exercised.** With h=0, parity P commutes with H, eigenvectors are
   parity eigenstates, and `biod(i,i) = psi^dag P psi = +-1`. I measured **exactly +1.000000** for
   both the vacuum and T at L=12/14/16. SIM-071 says so itself: *"all biorthogonal norms +1.0000
   (Hermitian limit)"* (`SIM-2026-071.json:11`). The headline claim depends on the **negative**
   <1|1> and on a negative product surviving into the estimator — the control has no analogue of
   either.
2. **Non-normality / eigenvector conditioning never exercised.** At h=0 the matrix is normal;
   eigenvector condition number is 1 by construction. At Yang-Lee `1/|<psi_L|psi_R>|` reaches ~181
   for T and ~4700 (extrapolated) for the vacuum at L=18. The control cannot detect a conditioning
   failure because it operates at condition number 1.
3. **Cross-state biorthogonality is never checked, in either mode.** The design document mandates
   it — `HYP028-BIORTHO-KS-DESIGN.md:36`: *"verify <Psi_L|Psi_R> != 0 **and biorthogonality across
   states**"* — but `qw_yanglee_ks.jl` only ever evaluates `biod(i,i)` (L95, L111, L117).
   `<psi_i^L|psi_j^R>` for i != j is never computed. In the Hermitian control this is automatic; at
   Yang-Lee it is an assumption.
4. **No PT-unbroken guard in Phase 2.** `qw_yanglee_pt.jl:75` asserts
   `maximum(abs.(imag.(vals[1:2]))) < 1e-8`. **`qw_yanglee_ks.jl` has no such assertion** — and it
   could not detect breakage anyway, because `ens = S .- abs.(vals)` (L73) silently discards any
   imaginary part. If the working point were ever pushed past the PT edge the driver would return
   plausible-looking garbage. The Hermitian control cannot surface this.
5. **The state-identification rule is inverted at Yang-Lee, and only there.** In the Ising control
   the Delta-window admits two states (D_vac = 1.9575 and 2.0321 at L=12) and element dominance
   picks the right one (0.27259 vs a Z2 structural zero) — dominance and the Delta-gate **agree**.
   At Yang-Lee they **disagree**: the cluster products at L=18 are 28.451 (phi-descendant,
   D_vac=1.524), **-2.588 (T, D_vac=1.982)**, -7.335 (D_vac=3.355). T carries the **smallest**
   element in the cluster — 11.0x smaller than the phi-descendant and 2.8x smaller than the third
   state. Since only one state falls inside (1.75, 2.25) at every L, `argmax` is a no-op and
   **T is selected by energy alone**, against a window centred on the exact CFT answer Delta_T = 2,
   in units of a velocity fixed by imposing the exact CFT value Delta_1 - Delta_phi = 2/5.
   SIM-071 reports the 10x inversion (`SIM-2026-071.json:23`) — honestly and prominently. What it
   does not say is the consequence: **at Yang-Lee the T identification has no empirical
   discriminator left.** The unitary discriminator (element dominance) is not merely weaker there,
   it points at the wrong state. The identification rests entirely on M(2,5) theory input.
   *(Minor incompleteness: SIM-071 mentions only the phi-descendant; the D_vac ~ 3.0-3.4 state also
   carries a 2.8x larger element than T and is not mentioned.)*

**Verdict on the control (section-7 classification): PARTIALLY INDEPENDENT / primarily a
consistency check of the *unitary* estimator.** It is a strong test of the KS algebra and a null
test of the code plumbing. It is **not** a test of the biorthogonal extension, which is the actual
novel content. Under section 19 ("a serious control should be capable of defeating the preferred
interpretation") this control cannot defeat the interpretation, because the mechanism the
interpretation depends on is switched off in it.

**Controls that would test the non-Hermitian layer and do not exist:** (i) a second non-unitary
model (section-13 Q10); (ii) synthetic non-normal matrices with known Jordan/biorthogonal structure
(section 13, "synthetic matrices with known behavior"); (iii) an alternate left-eigenvector
construction — solve `H^T w = E w` directly instead of assuming `w = P v` — the cheapest and most
direct pairing-invariance test, well under an hour of work; (iv) an alternate eigensolver at
higher precision; (v) an h-scan showing `c_KS` is stationary at the working point.

### 5.5 One thing the estimator gets right, provably

`c_KS` is **exactly invariant under rescaling of the eigenvectors**, including complex phases.
Under `v_i -> alpha v_i`: `lv(i) -> conj(alpha) lv(i)`, so the numerator picks up
`conj(alpha)*alpha = |alpha|^2` from the two elements and `biod(i,i)` picks up the same
`|alpha|^2`, which cancels; likewise for the vacuum. This directly answers section-13 Q3 ("how
sensitive is the extracted c to left/right eigenvector normalization?") — **answer: exactly zero
sensitivity, by algebra.** The product-form choice recorded in `HYP028-BIORTHO-KS-DESIGN.md:61-66`
earns this. It is currently claimed nowhere and should be stated as a proved property.

### 5.6 DEFECT (critical): the `h_c^inf` systematic is understated by more than an order of magnitude

`SIM-2026-071.json:27` states: *"Residual h_c^inf error contributes <=0.01 at L=18."*
I measured it directly by re-running Phase 2 at the three `h_c^inf` values the record's own data
support (all refits of `SIM-2026-070.json:8`'s `h_c^L` table):

| h_c^inf | provenance | c_KS(L=12) | c_KS(L=16) |
|---|---|---|---|
| 1.5585927 | **free-b fit — what `qw_yanglee_pt.jl:98-105` actually outputs** (`yl_run_8_18.log:11`) | -1.683506 | -2.113807 |
| 1.5587127 | b=12/5 + L^-4 fit — the adopted value | -1.702883 | -2.169926 |
| 1.5588876 | pure b=12/5 fit | -1.731749 | -2.255611 |

The dh = 1.2e-4 that SIM-070 itself cites moves c_KS by **0.056 at L=16** — 5.6x the claimed
"<=0.01" — and the sensitivity is still growing with L (0.019 at L=12 -> 0.056 at L=16, consistent
with SIM-070's own `L^{12/5}` observation, `SIM-2026-070.json:17`).

**Worse: propagated through the extrapolation, the fit-model choice moves the headline ~3x.**
Same pairwise-intercept + geometric-tail estimator on L = 10,12,14,16 for each h:

| h_c^inf | c_KS ladder (L=10..16) | intercepts | extrapolated c_KS | dev. from -22/5 |
|---|---|---|---|---|
| 1.5585927 | -1.40366, -1.68351, -1.91917, -2.11381 | -3.083, -3.333, -3.476 | **-3.667** | 16.7% |
| 1.5587127 | -1.41320, -1.70288, -1.95373, -2.16993 | -3.151, -3.459, -3.683 | **-4.291** | 2.5% |
| 1.5588876 | -1.42729, -1.73175, -2.00578, -2.25561 | -3.254, -3.650, -4.005 | **-7.044** | 60.1% |

(the middle row reproduces SIM-071's -4.285/-4.29, confirming the 4-point estimator is a fair proxy
for the 5-point one the record used).

**Consequences.**
- The quoted band `c_KS = -4.29 +/- 0.15` does **not** contain the h-model systematic. The
  realistic band from fit-model choice alone spans roughly **[-7.0, -3.7]**.
- **The sign and the exclusion of c_eff = +2/5 survive all three**, by a wide margin (every value is
  negative and >= 9x |c_eff|). SIM-071's *discrimination* verdict is robust.
- The *agreement with -22/5 at 2.6%* is **not** robust. It is specific to one of three defensible
  `h_c^inf` fits.

**Fairness to the record:** the adopted `h_c^inf = 1.5587127` is the best-motivated of the three —
theory-fixed exponent b = 12/5 = y_phi, and a 10x smaller fit residual (I reproduced all three fits
from the tracked `h_c^L` table: residuals 1.20e-6 / 1.33e-5 / 1.18e-4). It is not arbitrary. See
5.8 for why the *order* in which it was adopted still matters.

### 5.7 DEFECT (major): the designated EP health metric is degrading exponentially, unremarked

`HYP028-BIORTHO-KS-DESIGN.md:85`: *"<Psi_L|Psi_R> -> 0 signals proximity to an EP; monitor it as the
health metric."* The driver prints it (L96-97, L136) but applies **no threshold and no alarm**, and
neither SIM-070 nor SIM-071 discusses its trend. From the tracked `Tnorm` field plus my own run:

| L | <T_L\|T_R> | <1\|1> (vacuum) | implied 1/\|<L\|R>\| for T |
|---|---|---|---|
| 10 | 0.09615 | -0.010656 | 10.4 |
| 12 | 0.04786 | -0.003996 | 20.9 |
| 14 | 0.02359 | -0.001507 | 42.4 |
| 16 | 0.01150 | — | 87.0 |
| 18 | 0.005539 | — | 180.5 |

Both are exponential in L (~2.03x and ~2.65x per dL = 2). Two readings, both worth recording:
1. **Benign:** `psi^dag P psi` decaying exponentially with size is generic for a state that is not
   parity-symmetric — an extensivity effect, not EP proximity. If so, the design document's health
   metric **conflates extensivity with EP proximity and is not fit for purpose as written.**
2. **Adverse:** it is the eigenvalue condition number, doubling every two sites. At L=18
   (kappa ~ 180 for T, ~4700 for the vacuum) double precision with `tol=1e-11` is still ample —
   **the L <= 18 numbers are not compromised** — but the trend extrapolates to kappa ~ 1e5-1e6 by
   L ~ 30 and ~1e9-1e10 by L ~ 40.

Either way this bears on SIM-071's own proposed next step — *"puMPS-scale L would sharpen the third
digit"* (`SIM-2026-071.json:25`). Nothing in the record analyses whether the biorthogonal
construction survives to the N ~ 56-128 where P3 operates. On the adverse reading it does not.

### 5.8 DEFECT (major): the Phase-1 gate, as coded, FAILS; the recorded PASS came from untracked re-analysis

`yl_run_8_18.log` is the tracked output of the tracked driver. Its last line is:

```
GATE: NOT PASSED -- inspect before Phase 2
```

with `h_c^inf = 1.5585927 (a=3.6002, b=2.34)`, `R_inf = -1.6444 / -1.6500 / -1.6566` across
windows, `g_1 = 0.7377 / 0.7419 / 0.7462` — 1.6-2.4% off the exact -1.618034 and 1.7-2.9% off
0.725073, against the driver's own thresholds (`qw_yanglee_pt.jl:131`).

`SIM-2026-070.json` records **PASSED** with `R_inf = -1.61820` (0.01%) and `g_1 = 0.725347`
(0.04%). Neither is producible by the tracked driver. Both come from:
1. a **different `h_c^inf`** (1.5587127, from a `b = 12/5 + L^-4` fit that exists nowhere in the
   repo — I reproduced it from the tracked `h_c^L` table: `h_inf = 1.5587127`, residual 1.20e-6,
   exact match), fed back through the driver's `proj` mode (`yl_proj.log`); and
2. a **different extrapolator** — "two-level Richardson (pairwise 1/L intercepts, then geometric
   tail sum)" (`SIM-2026-070.json:11`) — which also exists nowhere in the repo. The tracked driver
   fits `R_inf + r1/L + r2/L^2` over drop-smallest-L windows (L117-128).

Reproducing the Richardson result from `yl_proj.log` exposes the sharpest sub-defect:

```
intercepts: -1.54226, -1.57026, -1.58589, -1.59549, -1.60189, -1.60649
diffs:      -0.02800, -0.01563, -0.00960, -0.00640, -0.00460
ratios:      0.5581,   0.6142,   0.6671,   0.7181      <-- monotonically RISING, not stable
geometric tail with the MEAN ratio (0.6394)  ->  -1.61464   (0.21% dev)
geometric tail with the LAST ratio (0.7181)  ->  -1.61820   (0.011% dev)   <-- the quoted number
```

**The headline "0.01%" requires selecting the last ratio.** With the mean ratio the same data give
0.21%. SIM-070 is transparent that the ratios run "0.56->0.72" (`SIM-2026-070.json:11`), so nothing
is concealed — but a rising ratio sequence means the geometric-tail assumption is not satisfied,
and quoting 0.01% as *the* agreement presents an estimator-selection coincidence as precision.

**Why this matters for SIM-071, not just SIM-070.** SIM-071 defends its own extrapolation with
*"the same two-level Richardson estimator that hit 0.01% on SIM-070's R_inf shows MORE stable
ratios here (0.730/0.728)"* (`SIM-2026-071.json:25`). Three observations:
- SIM-070's ratios were **not** stable (0.558 -> 0.718, rising monotonically over exactly this L
  range); its 0.01% came from the last-ratio choice, not from stability.
- SIM-071 has **two** ratios (from 5 points), from which "STABLE" cannot be established. If the
  Phase-2 ratio rises with L the way Phase-1's demonstrably did, the tail sum **underestimates**
  |c_KS|: q=0.75 -> -4.34, q=0.80 -> -4.50, q=0.85 -> -4.77.
- The whole ladder is conditioned on the `h_c^inf` choice that made the Phase-1 gate pass (5.6),
  and the Phase-1 gate metric (`R_inf` vs a known exact number) is *itself* the criterion by which
  that `h_c^inf` was adopted. There is no pre-registration of the `b = 12/5 + L^-4` model
  (section 36). I am **not** claiming the number was tuned to the Phase-2 answer — Phase 2 ran
  afterwards — but the working point was selected against a known exact target and carries a ~3x
  lever arm on the Phase-2 headline.

**Cheap required fix:** commit the analysis script (the h fit + the Richardson estimator), and
update `qw_yanglee_pt.jl` so its built-in gate reflects the accepted method instead of printing
"NOT PASSED" for the run of record.

### 5.9 DEFECT (major): the pre-registered G4 criticality gate was substituted, not satisfied

`HYP-2026-028.json:24` lists as a **mandatory gate**:
> *"HARD non-unitary criticality gate: confirm c_eff=2/5 via the established non-unitary
> biorthogonal entanglement-entropy scaling AND Delta_phi=-1/5 from the dilation/lightest-primary
> spectrum BEFORE reporting alpha. If the fixed point is not reached, the result is INVALID."*

`HYP-2026-028.json:54` now records: *"G4 gate satisfied at ED scale via SIM-070 (0.01%) + SIM-071."*
But SIM-070 measured `g_1` and `R_inf` — **boundary-state g-function data, not `c_eff` and not
`Delta_phi`.** Neither quantity named in the mandatory gate was ever computed. The substitute
evidence is strong (a negative `R_inf -> -(1+sqrt5)/2` is unitarity-forbidden and M(2,5)-specific),
but a mandatory pre-registered gate was replaced by a different observable with no recorded
amendment. Under section 36 the original entry should be preserved and the substitution argued.

**Related record defect (medium).** `HYP-2026-028.json` states `Delta_phi = -1/5` in six places
(lines 15, 16, 20, 24, 38, 51) and it was the target the SIM-053/055 G4 gates were checked against.
The correct Yang-Lee M(2,5) **scaling dimension** is `Delta_phi = h + hbar = -2/5`; `-1/5` is the
chiral weight `h_phi`. Current drivers use the right value (`qw_yanglee_ks.jl:86` divides by
`2pi*(2/5)`; `HYP028-BIORTHO-KS-DESIGN.md:56,76` says `-2/5`), so Phase 1/2 are unaffected — but the
earlier gates were checked against a value off by a factor of 2, and the live gate text in
`HYP-2026-028.json` still carries it.

### 5.10 Missing artifacts (P4)
- **No Phase-2 stdout log.** `yanglee-pt/` tracks `yl_run_8_18.log` and `yl_proj.log` for Phase 1,
  but `ylks_warn.log` is **0 bytes** (stderr only). The Phase-2 spectra, the biorthogonal-norm
  printout (L96-97) and the per-state diagnostics (L119, L130-136) were printed and discarded.
  The `.jsonl` retains products and norms, so this is recoverable — but the "<1|1> negative" claim
  had no artifact until this audit produced one.
- **No unitary-control artifact of any kind.** `qw_yanglee_ks_results.jsonl` contains **5 lines,
  all Yang-Lee** (L=10..18, `v` ~ 4.24-4.28). A repo-wide grep for
  `0.517483|0.512776|0.509748|0.49986` returns only prose files: `SIM-2026-071.json`,
  `HYP-2026-028.json`, `NEXT-SESSION.md`, `docs/governance/PROJECT-REVIEW-2026-08-11.md`. The
  control carrying the entire credibility of the frontier result was run, three numbers were
  transcribed by hand into a JSON, and the output was thrown away. (They are correct — see 5.2 —
  but the repository could not have established that.)
- **No extrapolation/analysis script for either phase.**

---

## 6. CODE-PATH INDEPENDENCE LEDGER (RESEARCH-DIRECTOR section 7)

### 6.1 Shared components across pipelines

| Component | P1 MERAKit | P2 cttt-circle | P3 puMPS | P4 yanglee |
|---|---|---|---|---|
| Language / runtime | Julia 1.8 + TensorKit | Python + scipy | Julia 1.12 + vendored ZMV | Julia + KrylovKit |
| State construction | scale-inv. MERA (variational) | exact sparse ED | puMPS Bloch (variational) | exact sparse ED (non-Herm.) |
| Momentum resolution | none (scale-inv. line) | translation permutation, `np.linalg.eig` on degenerate blocks | `Hn_in_basis` enforces spin(bra)=spin(ket)+n structurally | translation-composed Arnoldi, `angle(-lambda)` |
| KS mode discretization | n/a | **naive** (whole 2-site term, one phase) | **half-bond** (upstream `models.jl`) | **half-bond** |
| `C_TTT` | attempted independently (Route A, FAILED) | `2 sqrt2/sqrt(c)` (L203) | `2 sqrt2/sqrt(c)` (L117 / L132 / L82) | n/a (imaginary at c<0) |
| `v` calibration | n/a | `v_exact=2` (Ising) or self-cal | `v_T` from Delta_T=2 | `v_T` from Delta_T=2 |
| Result artifacts in repo | **none** | JSON, tracked | JSONL + one log, tracked | JSONL + 2 logs, tracked (Phase 1 only) |

**Genuine code lineage (not independent).** `yanglee-pt/qw_yanglee_ks.jl` is a direct port of
`pumps-setup/qw_potts_ed_gate.jl`: identical translation-composed eigensolve idiom
(`f = x -> (apply_H(x) .- SHIFT .* x)[perm]`, ED gate L60 vs KS L70), identical momentum decoding
(`round(Int, mod(angle(-l)/(2pi/N) + N/2, N) - N/2)`, ED gate L66 vs KS L75), identical
`ens = SHIFT .- abs.(vals)` (L65 vs L73), identical half-bond phase construction (L91-92 vs L34-35).
This is fine — that machinery was validated against puMPS at N=10 — but it means **P3 and P4 are
not independent in their momentum/KS layer**. Only P2 has an independently written momentum layer,
and P2 uses a *different* KS discretization.

### 6.2 Comparison classification

| Comparison | Classification | Basis |
|---|---|---|
| `C_TTT` vs `2 sqrt2/sqrt(c)` (all three rungs) | **ALGEBRAICALLY EQUIVALENT** | `C_TTT` is computed as that expression, in code, in every driver |
| `c_meas` vs exact c (Ising/TCI/Potts) | **primarily a consistency check** | c is fixed by the minimal model; only implementation success/failure was possible |
| Delta_T = 2 -> alpha = 4 | **ALGEBRAICALLY EQUIVALENT to the CFT theorem** | Delta_T=2 in every 2D CFT; and in P3/P4 `v_T` is *defined* by imposing Delta_T=2, so Delta_T is not even measured there |
| C_sigma-sigma-epsilon = 0.50 vs 0.5 | **primarily a consistency check** | BPZ 1984; near-zero counterfactual novelty |
| puMPS N=12 vs ED N=12 (once conventions matched) | **FULLY INDEPENDENT** | different language, different state construction (variational MPS vs exact ED), agreement 5e-6 in c. **The strongest cross-check in the repo — currently mis-stated in VENDOR.md (see 4.4)** |
| Potts ED gate N=10 vs puMPS N=10 | **PARTIALLY INDEPENDENT** | different state construction; but the same KS phase convention and the same translation-composed idiom |
| YL `c_KS` vs the Ising control | **PARTIALLY INDEPENDENT / structurally dependent** | same file, same 148 of 152 lines; the biorthogonal layer is inert in the control (see 5.4) |
| YL `c_KS` vs my Python port (this audit) | **FULLY INDEPENDENT at raw-number level** | different language and eigensolver; 6-decimal agreement; extrapolation and interpretation untested |
| SIM-070 Phase-1 gate vs PAPER-133 Table I | **FULLY INDEPENDENT external anchor** | genuinely external data (Liu-Shimizu-Liu-Kawabata); the only fully external validation target in P4 |
| SIM-071 vs SIM-070 | **structurally dependent** | same model, same `h_c^inf`, same chain, same left-pairing choice; Phase 2 inherits every Phase-1 systematic |

### 6.3 Contribution-level assignment (section 5)

| Result | Level | Justification |
|---|---|---|
| Delta_sigma, Delta_eps, Delta_T at Ising/TCI/Potts (P1) | **1** | fixed by minimal-model representation theory |
| C_sigma-sigma-epsilon = 0.50 +/- 0.03 (P1) | **1** | BPZ 1984 exact value |
| C_TTT ladder 3.9936 / 3.381 / 3.163 (P2, P3) | **1** | Virasoro identity, computed as an algebraic transform of c |
| Z2/Z3-symmetric optimisation converting 2/8 -> 8/8 clean basins (P1) | **2** | reproducible method improvement |
| L-2 epsilon contamination suppression, ~400x, p ~ 2.4 vs 0.2 (P3) | **2** | strongest methods result in the repo; candidate Paper C |
| Predictive use of two-error cancellation (P3) | **2** | genuine out-of-sample prediction (section 18) |
| Route A closure / equal-time correlator falsification (P1, P2) | **2** (negative) | well-executed no-go on a specific extraction route |
| Biorthogonal KS extension recovering c with its sign (P4) | **2, aspiring to 3** | the *method* is the contribution; the c value is a known M(2,5) number, so it is Level 3 only if "KS survives non-unitarity carrying true c" is shown to be new (novelty gate NOT run — see 7.3) |
| Any geometry-discriminating result (section 5, Level 4) | **none exists in any pipeline** | no matched non-geometric control appears anywhere in `research/tools/` |

**Counterfactual novelty (section 6).** For P1/P2/P3 the honest field value is **near-zero**:
conformal symmetry fixed every target in advance, so only implementation failure or success was
possible. `CTTT-ROUTE-B-CIRCLE-DESIGN.md:96-102` states this in the project's own words. P4 is the
sole pipeline with **moderate-to-high** counterfactual novelty: before running, `c_KS` could
plausibly have returned +2/5, -22/5, or noise, and the three outcomes carry different
interpretations. That is the only place in `research/tools/` where the pre-calculation outcome
space had more than one physically meaningful member.

---

## 7. Reproducibility scorecard (section 21)

| Requirement | P1 | P2 | P3 | P4 |
|---|---|---|---|---|
| Driver code tracked | yes (1 drifted, 9 unmirrored) | yes | yes | yes |
| Vendored dependency pinned to a commit | **NO** | n/a | yes (`0557b12a...`) | n/a |
| Vendored patches reproducible | n/a | n/a | prose only, no `.patch` | n/a |
| Environment spec | yes (`RUN-MERAKIT.md`, `Project.toml.pinned`) | implicit (numpy/scipy) | partial (`VENDOR.md`: "Julia 1.12.x") | none stated |
| Raw per-point outputs tracked | **NO** | yes | yes | **partial** (no control, no Phase-2 log) |
| Analysis / fit script tracked | **NO** | fits are in the driver | **NO** (recoverable) | **NO** (recoverable) |
| Random seeds recorded | in prose ("8 seeds") | n/a (deterministic) | n/a | **NO** (`randn` start vector, no seed) |
| Recorded numbers reproducible by me | **no** (nothing to reproduce from) | **yes, exact** | **yes, exact** | **yes, exact** (raw); extrapolation reproducible but estimator-sensitive |
| One-command reproduction of a headline | no | close (`python qw_cttt_circle.py`) | no (multi-stage, checkpointed) | no |

**Seed note (minor, P4):** `qw_yanglee_ks.jl:71` and `qw_yanglee_pt.jl:50` start Arnoldi from
`randn(ComplexF64, dim)` with **no seed set**. The results are effectively deterministic here
(well-separated targets, `tol=1e-11`), and my independent ARPACK run agreed to 6 decimals, so this
is not currently biting — but at larger L with a degrading `<L|R>` it could, and section 21 requires
seeds to be recorded.

### 7.1 Novelty-gate status (section 8) for the one Level-2/3 candidate

`SIM-2026-071.json:22` asserts: *"First lattice extraction (to our knowledge) of a NEGATIVE central
charge from stress-tensor matrix elements."* That phrase is **explicitly forbidden** by the task
brief and by section 8 without recorded evidence. I find **no literature-gate record anywhere** for
this claim: no search log, no prior-art table, no nearest-paper comparison in
`research/data/papers/`, `NEXT-SESSION.md`, or `docs/governance/PROJECT-REVIEW-2026-08-11.md`.
Section 8 lists thirteen required search variants for exactly this result (negative central charge,
biorthogonal CFT, Koo-Saleur generators, lattice Virasoro generators, non-Hermitian spin chains,
PT-symmetric criticality, ...). None is recorded as having been run.
**The novelty claim in SIM-071 should be struck until the gate is executed.**

---

## 8. UNVERIFIED

Things I could not check, stated explicitly rather than passed over in silence.

1. **P1 numbers entirely.** No raw artifacts exist for any MERAKit result (2.3). Every P1 figure in
   this audit is quoted from the SIM JSON prose and is **unverified**. That includes C_sigma-sigma-epsilon
   = 0.50 +/- 0.03, the Potts chi-ladder 0.089/0.14/0.133, the Route-A scatter, and all
   scaling dimensions. I did not re-run MERAKit (Julia 1.8 + unpinned vendored clone).
2. **The MERAKit.jl revision actually used.** Not recorded anywhere; I could not determine it.
3. **`qw_tci.jl` drift impact.** I established that the tracked mirror and the vendored copy are
   materially different (dim-8/3-layer vs dim-4/4-layer) and that the *vendored* one is newer. I did
   **not** establish which produced SIM-051/052, nor whether any published number depends on it.
   The later drivers (`qw_tci_chi8.jl`, `qw_tci_measure.jl`, Jun 22) are in sync, which suggests low
   impact — suggestive, not verified.
4. **P3 Ising gate at N=16 D=12.** The log stops mid-CG; I cannot confirm it ever completed.
   `VENDOR.md:53-56` says it was externally killed twice.
5. **YL at L=18 under alternative `h_c^inf`.** My 5.6 systematic table uses L=10..16 (4 points,
   1 ratio). The L=18 point at the alternative h values was not computed (2^18 non-Hermitian
   ARPACK; the L=10..16 sweep already ran several minutes per h). The middle row reproduces
   SIM-071's 5-point answer to 0.006, so I judge the proxy sound — but the 5-point systematic
   at the two alternative h values is **extrapolated from a 4-point estimator, not measured.**
6. **Whether `<psi_L|psi_R>` decay at Yang-Lee is EP proximity or generic extensivity.** I present
   both readings in 5.7 and did not discriminate them (would require an h-scan of the norm at fixed
   L, or comparison against a known-benign non-Hermitian reference).
7. **Cross-state biorthogonality `<psi_i^L|psi_j^R>` for i != j at Yang-Lee.** Not computed by the
   driver and not computed by me. If the low k=0/k=+-2 states are not mutually biorthogonal, the
   product-form denominators are ill-defined. This is the cheapest remaining check and it is
   outstanding.
8. **Prior art for the biorthogonal-KS result.** Not searched (out of scope for this task; flagged
   in 7.1 as a missing gate, not as a novelty judgement either way).
9. **Whether the half-bond vs naive KS convention has any effect on P4's Yang-Lee numbers.** P4
   already uses the half-bond convention, so no correction is implied; I did not run the naive
   variant at Yang-Lee to size the difference there.
10. **P5 (the force/transport pipeline) entirely.** Out of scope for `inv:pipelines` as briefed;
    flagged in 1 only as a structural observation. Every headline in the submitted PRD manuscript
    comes from it, and it was not audited here.

---

## 9. Prioritised defect list

| Sev | Where | What |
|---|---|---|
| **critical** | `SIM-2026-071.json:27` | `h_c^inf` systematic stated as "<=0.01 at L=18"; measured 0.056 at L=16 for the record's own dh, and the fit-model spread moves the extrapolated headline from -3.67 to -7.04. The +/-0.15 band excludes the dominant systematic. Sign/`c_eff`-exclusion survive; the "2.6% from -22/5" claim does not. |
| **major** | `pumps-setup/VENDOR.md:50` | Validation table compares puMPS raw N=12 against SIM-067 *extrapolated*, hiding a 7% same-N disagreement in c. Root cause = undocumented KS phase-convention difference. Correcting it turns a fake agreement into a real 5e-6 cross-validation. |
| **major** | `cttt-circle/qw_cttt_circle.py:183` | Non-standard KS mode discretization (no half-bond phase), differing from every other implementation in the repo and from upstream ZMV; documented nowhere; ~10x larger finite-size error. |
| **major** | `research/tools/MERAKit.jl/` + all P1 SIM records | No raw artifacts for the entire MERAKit pipeline; every cited `scratchpad *.log` is absent; vendored clone has no commit pin. |
| **major** | `qw_yanglee_ks.jl` (whole file) | Unitary control shares 148/152 lines and switches the non-Hermitian mechanism **off** (`HC=0.0`); biorthogonal norms are exactly +1 in the control. Validates the KS estimator, not the biorthogonal extension. |
| **major** | `yl_run_8_18.log` vs `SIM-2026-070.json` | Tracked driver's gate prints "NOT PASSED"; the recorded PASS used an untracked `h` refit and an untracked Richardson estimator. `R_inf` 0.01% requires selecting the last (rising) ratio; mean ratio gives 0.21%. |
| **major** | `HYP-2026-028.json:24 vs :54` | Mandatory pre-registered G4 gate (`c_eff=2/5` AND `Delta_phi`) replaced by different observables (`g_1`, `R_inf`) with no recorded amendment. |
| **major** | `qw_yanglee_ks.jl:73` | No PT-unbroken guard in Phase 2; `ens = S .- abs.(vals)` silently discards imaginary parts, so PT breakage would return plausible garbage. Phase 1 has the assertion (`qw_yanglee_pt.jl:75`); Phase 2 does not. |
| **major** | `qw_yanglee_ks.jl:95,111,117` + `HYP028-BIORTHO-KS-DESIGN.md:36` | Design mandates cross-state biorthogonality verification; only `biod(i,i)` is ever computed. |
| **major** | `SIM-2026-071.json:22` | "First ... (to our knowledge)" novelty claim with no literature-gate record anywhere in the repo. |
| **major** | `qw_yanglee_ks.jl:96,136` + records | Designated EP health metric `<L|R>` decays exponentially (0.096 -> 0.0055 over L=10..18) with no threshold, no alarm, and no discussion — while the record proposes scaling to puMPS-size L. |
| medium | `SIM-2026-067.json:12` / `qw_cttt_circle.py:382-390` | `c_meas` and `C_TTT` extrapolated separately though algebraically linked; the two answers differ by 0.29%, more than either quoted deviation. |
| medium | `HYP-2026-028.json:15,16,20,24,38,51` | `Delta_phi = -1/5` is the chiral weight, not the scaling dimension (-2/5). Live gate text still wrong; SIM-053/055 gates were checked against it. |
| medium | `merakit-setup/qw_tci.jl` | Tracked mirror is stale and materially different from the newer vendored copy (dim-8/3-layer vs dim-4/4-layer), violating the `CLAUDE.md` mirror rule; 9 further scripts never mirrored at all. |
| medium | `yanglee-pt/qw_yanglee_ks_results.jsonl` | Unitary control produced no artifact; three hand-transcribed numbers are the only record of the program's most load-bearing validation. |
| minor | `pumps-setup/VENDOR.md:79-88` | Vendor patches are prose-only; no `.patch` file for one-command reconstruction. |
| minor | `qw_pumps_validate_ising.jl:24` | Ising gate hardcodes `v_exact=2.0`, so the `v_T` self-calibration used in production is not exercised by the gate. |
| minor | `qw_yanglee_ks.jl:71`, `qw_yanglee_pt.jl:50` | Unseeded `randn` Arnoldi start vectors; section 21 requires recorded seeds. |
| minor | `research/data/simulations/*.py` | 131 production scripts live in the *data* directory with no `research/tools/` home, no design doc, no provenance file — and they carry every manuscript headline. |
| minor | `research/data/theory/` | Empty (known defect, section 14). No pipeline links to a structured theory record; the dependency chain `spectrum -> T-identification -> normalization -> c-estimator -> interpretation` (section 15) exists only in prose. |

---

## 10. What would most improve the program, from this pipeline's vantage

Ranked by (evidence gained) / (effort), all cheap:

1. **Publish the corrected puMPS <-> ED matched-N cross-check** (4.4). It is already true, already
   computed, and turns a mis-stated agreement into the repo's strongest independence claim. ~1 hour.
2. **Solve `H^T w = E w` directly for the left eigenvectors** instead of assuming `w = P v`, and
   confirm `c_KS` is unchanged (5.4 control iii). This is the single most informative missing test
   of the biorthogonal layer. ~1 hour.
3. **Propagate the `h_c^inf` systematic into SIM-071's quoted band** (5.6) and restate the result as
   "sign and `c_eff` exclusion decisive; magnitude consistent with -22/5 within a large
   estimator+working-point systematic". The scientific claim survives; the precision claim does not.
4. **Commit the analysis scripts** for both the `h` fit and the Richardson estimator, and re-run the
   Yang-Lee control with output retained (5.8, 5.10). ~1 hour.
5. **Add the P1 result logs to git** — they exist inside `MERAKit.jl/`; this is a `.gitignore`
   exception, not a re-run (2.3).
6. **Pin the MERAKit.jl revision** the way puMPS is pinned (1.1).
