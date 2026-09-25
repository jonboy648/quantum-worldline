# puMPS — vendored ZMV codebase (C_TTT continuation: TCI + Potts)

**What:** `research/tools/puMPS/` holds a vendored copy of **`yijian-physics/puMPS`** — the authors'
own implementation of periodic uniform Matrix Product States from
**Zou, Milsted & Vidal, PRL 121, 230402 (2018)** (arXiv:1710.05397), i.e. the exact method our
SIM-067 C_TTT Route B is anchored on. README provenance: "Original development: Yijian Zou, Ashley
Milsted and Guifre Vidal with Julia 0.6 and Julia 1.0 in 2017. Code updated for compatibility with
Julia 1.11 on 2025-09-14."

- **Pinned commit:** `0557b12a387091f96b83900e99bdb13c5f393839` (2025-09-14, branch `main`)
- **Fetch:** `for f in MPS.jl models.jl puMPS.jl states.jl tangentspace.jl UnitTestED.jl; do
  curl -s -O https://raw.githubusercontent.com/yijian-physics/puMPS/0557b12/$f; done`
- **License: NONE on the yijian repo** — do not redistribute; the vendored copy is GITIGNORED
  (like MERAKit.jl) and only our own driver scripts are tracked. The README asks for citation of
  PRL 121, 230402 — already our SIM-067 anchor. **`FuTen/puMPS.jl`** (Milsted's packaging of the
  same code, MIT-licensed, 2017–2023) is the fallback if redistribution is ever needed.
- **History note (correcting the record):** the 2026-07-20 verification "no public puMPS package
  exists" was itself wrong — it checked only `amilsted/puMPS`. A GitHub search for the exact phrase
  "periodic uniform matrix product" (NOT "puMPS", which every search engine stems to "pumps") finds
  both repos immediately. Recorded in scan #19 and here so it isn't re-derived wrong a third time.

## Why this kills the from-scratch build

Everything SIM-067's continuation needs is already implemented:

| Need | Function (all exported from module `puMPS`) |
|---|---|
| GS optimization on a ring | `minimize_energy_local!` (CG, per PRL) / `vumps_opt!` |
| Bloch excitations at momentum k | `excitations!(M, H, ks, num_states)` — k in units 2π/N |
| Koo-Saleur H_n matrix elements | `Hn_in_basis(M, Hn_split, Tvec_basis, ks)` |
| Ising H_n MPOs | `ising_Hn_MPO_split(T, n, N)` |
| **O'Brien-Fendley H_n MPOs** (TCI!) | `OBF_Hn_MPO_split(T, n, N; lambda1, lambda2, ...)` |
| **3-state Potts H_n MPOs** | `potts3_Hn_MPO_split(T, n, N; h)` (`weylops` for clock/shift) |
| ED cross-check harness | `UnitTestED.jl` (Ising PBC eigenstates via Arpack) |
| Worked benchmark | `Ising_XXZ_benchmark.ipynb` in the upstream repo (not vendored, 484 KB) |

Deps: TensorOperations, LinearMaps, KrylovKit, Optim (+ Arpack for the ED test). Julia project env
lives at `research/tools/puMPS/Project.toml` (created locally, gitignored with the source).
**Julia: use the default channel (1.12.x)** — upstream targets 1.11; MERAKit's `+1.8` env is NOT
needed here and should not be mixed in.

## Plan of record (C_TTT TCI/Potts)

1. **Validation gate (Ising, small N): PASSED 2026-08-09** (N=12, D=8; `validate_run.log`):
   | quantity | puMPS | exact / SIM-067 |
   |---|---|---|
   | Δ_σ, Δ_ε (spectrum) | 0.125179, 0.997176 | 0.125, 1 |
   | Δ_T (energy) | 1.960387 | 2 (finite-N, matches ED scale) |
   | c_meas (n=+2 / n=−2) | 0.497156 / 0.497155 | 0.5; chirality-symmetric to 1e-6 |
   | **C_TTT** | **4.0114** (raw N=12) | 4.000 (SIM-067 extrapolated 3.9936) |
   | T-discrimination | other k=2 state element 0.000078 (6400× smaller) | — |
   | selection-rule zeros | 0.000000 | by construction |
   The puMPS pipeline reproduces the SIM-067 circle/KS extraction. **Notes for production:**
   (a) use `puMPS.minimize_energy_local_CG!` (NOT exported; the plain-gradient optimizer's
   linesearch thrashes); (b) two consecutive background runs were externally killed mid-N=16 —
   the production driver MUST checkpoint the GS to JLD2 after convergence and accept a
   resume-from-file flag, so a kill costs one stage, not the run.
2. **Convention check for OF — RESOLVED on paper 2026-08-09 (still verify vs ED at N=12):**
   contracting `OBF_local_MPO`'s 3-site MPO paths gives
   `h = −λ1(ZZ + X) + λ2(ZZX + XZZ)` (dual/ZZ frame). Our SIM-067 `build_ops_of` uses the
   Hadamard-rotated frame with an overall factor 2: `−2(Z + XX) + λ3(ZXX + XXZ)`. Therefore
   **λ1 = 1, λ2 = λ3/2 = 0.428** reproduces our TCI point (λ3 = 0.856), with puMPS energies
   HALF ours (factor-2 Hamiltonian normalization) — velocities scale the same way, and the KS
   ratio c is normalization-invariant once v is calibrated consistently. Keep `lambdaC = 0`
   (the Y-term is the integrable-direction perturbation; not our point). **v must be CALIBRATED
   at the OF point** (port SIM-067's `calibrate_v` descendant-gap method); do not assume v = 2.
3. **TCI production:** OF chain at N ≈ 64–128 (ZMV used N ≤ 128 for exactly this model), D scaled
   until the L₋₂ε contamination (~N^−0.2) is beaten. Target **C_TTT = 3.381** (= 2√2/√c, c = 7/10).
4. **Potts production:** `potts3_*` at the critical point, target **C_TTT = 3.162** (c = 4/5).
   Watch Z3 charge resolution (weylops basis) — same degeneracy discipline as SIM-063.
5. SIM-068 record; single-thread BLAS (`OPENBLAS_NUM_THREADS=1`) for deterministic basins, per
   the MERAKit lesson.

Driver scripts (ours, tracked here in pumps-setup/, copied into puMPS/ to run):
- `qw_pumps_validate_ising.jl` — step 1 (PASSED)
- `qw_cttt_of.jl` — step 3, TCI (SIM-068 PASSED)
- `qw_cttt_potts3.jl` + `qw_potts_ed_gate.jl` — step 4, Potts (in flight 2026-08-11)

## LOCAL PATCHES to the vendored source (gitignored — reapply after any re-fetch)

1. **`models.jl` `weylops` (line ~492), REQUIRED for potts3 on Julia ≥1.0:** upstream uses
   pre-1.0 syntax `V = diagm(ones(p - 1), 1)` → `MethodError`. Patch:
   `V = diagm(1 => ones(p - 1))`. Only the potts3 path hits this (Ising/OBF never call weylops),
   which is why the 2025-09-14 "Julia 1.11 refresh" missed it.
2. **`states.jl` `minimize_energy_local_CG!`:** added kwarg `pinv_tol::Real=1e-12` passed through
   to `gradient_central(...; pinv_tol=pinv_tol, ...)` in the `use_phys_grad` branch. Lets drivers
   regularize the tangent-metric pseudo-inverse. (Tested 1e-8 on Potts d=3: did NOT move the CG
   floor — kept for future use; harmless at default.)

## Potts production notes (2026-08-11)

- **d=3 CG floor is ~2.5e-4** (vs ~9e-5 on OF d=2); NOT fixed by step-size tuning or pinv_tol.
  Driver uses plateau-accept: energy flat <1e-8/round for 3 rounds AND |grad|<5e-4 → accept.
- **ED gate (N=10, `qw_potts_ed_gate.jl`) PASSED**: puMPS E0/site within 1.4e-6, T gap within
  1.8e-4 relative, v's within 1e-4, gap ratio 6.1929 vs ED 6.1924 → plateau harmless for
  spectroscopy. ED confirms charged σ-descendant elements are STRUCTURAL ZEROS (exact doublets,
  elem=0) and reconfirms the SIM-067 band-edge trap: raw-ED max element is a UV state at Δ≈2.53
  (4.5× T's element) → ED c would be nonsense (5.9); puMPS Bloch elements suppress it (~1000×
  dominance of T). ED certifies ENERGIES; elements are certified by puMPS-internal discipline
  (chirality symmetry, D-stability, N-trend).
- Ladder so far (chirality-mean): N=10 D=12 c=0.8435 C=3.0796 · N=14 D=12 c=0.8170 C=3.1291 ·
  N=20 D=20 c=0.8095 C=3.1437 (target c=0.8, C=3.16228). N=20 D=14 truncation check in flight.
