# Running MERAKit.jl (working invocation, 2026-06-19)

## VENDOR PROVENANCE (added 2026-08-17 — AUDIT-2026-08-11 defect D-21)

D-21: *"MERAKit.jl is gitignored with no upstream revision recorded anywhere."* It was true; this
section closes it. Model: `research/tools/pumps-setup/VENDOR.md`, which the project already got
right for puMPS. Every field below was read off the vendored tree on 2026-08-17, not recalled.

| Field | Value | How verified |
|---|---|---|
| **What** | `MERAKit.jl` — scale-invariant / ternary MERA in Julia, by **Markus Hauru** and **Jutho Haegeman**. The optimizer behind pipeline P1 (SIM-051/052/061/062/063 and the α = 4 universality claim). | `Project.toml` `authors` |
| **Upstream URL** | **`https://github.com/mhauru/MERAKit.jl`** | `git remote -v` inside `research/tools/MERAKit.jl/` |
| **Pinned revision** | **`ace2f92eac2fb782d2f24a3e7f5123b1f104510e`** (short `ace2f92`), branch `master`, committed **2021-08-21 17:42:56 +0100** by Markus Hauru, *"Replace Travis with Actions"* | `git log -1` in the vendored tree |
| **Upstream tag** | **None.** `git describe --tags --always` returns the bare SHA — the upstream repo publishes no tags, so the SHA above is the only durable identifier. Cite the SHA, never "latest". | `git describe --tags --always` |
| **Declared package version** | `version = "0.1.0"` in `Project.toml` — **not a release identifier**; it has never been bumped. Do not use it to pin anything. | `Project.toml` |
| **Fetch command** | `git clone https://github.com/mhauru/MERAKit.jl research/tools/MERAKit.jl && git -C research/tools/MERAKit.jl checkout ace2f92eac2fb782d2f24a3e7f5123b1f104510e` | acquisition method inferred from the intact `.git` clone with an `origin` remote |
| **License** | **MIT (permissive), full text in `LICENSE`:** *"Copyright (C) 2020 Markus Hauru, Jutho Haegeman … permission … to deal in the Software without restriction, including … the rights to use, copy, modify, merge, publish, distribute, sublicense, and/or sell copies …"*, conditioned on carrying the notice. **Redistribution IS permitted.** This is the opposite of puMPS (no upstream license → never redistribute). The tree is gitignored by project convention — size and cleanliness — **not** by legal necessity, so a Zenodo deposit may include it provided `LICENSE` travels with it. | `cat LICENSE` |
| **Local patches to upstream files** | **NONE.** `git status --porcelain -uno` inside the tree is empty: not one upstream-tracked file is modified. | `git status --porcelain -uno` |
| **Local additions** | **49** untracked paths, all ours: **30** `.jl`/`.py` scripts (the `qw_*`/`of_*`/`ope_*`/`diag_*`/`dump_*`/`test_*` drivers plus `setup.jl` and `instantiate.jl`), **7** run `*.log`, **7** `*.txt` operator/spectrum dumps, **2** `hb_lam3_*.npy` operator arrays, `Manifest.toml`, `Project.toml.orig`, `__pycache__/`. | `git status --porcelain` filtered to `??`, bucketed by extension |
| **Resolved environment** | `Manifest.toml` (14,148 B, generated locally — untracked upstream) records `julia_version = "1.8.5"`, `manifest_format = "2.0"`, `project_hash = cde5eb2a7a2b7bf2aa883db0b7a36f4b98ae981e`. **This is the only resolved dependency manifest anywhere in the project** (D-21 measured "dependency versions 0/73"). | `head -5 Manifest.toml` |

### Correction to this file's own earlier text

The line *"Compat pinned to TensorOperations 3 era; Project.toml.orig is the upstream original"*
implied a local pin. **There is no local pin.** `Project.toml` is byte-identical to both
`Project.toml.orig` and to upstream `ace2f92`, and `TensorOperations = "^3"` is upstream's own
`[compat]` entry. `Project.toml.orig` is a redundant backup of an unmodified file. The operative
constraint is real but comes from upstream, not from us — kept here rather than deleted, per §32
(preserve the original claim alongside the correction).

### `setup.jl` is destructive — use `instantiate.jl`

`setup.jl` line 4 is `rm("Manifest.toml"; force=true)`, then `Pkg.Registry.update()` + `Pkg.resolve()`.
It **deletes the known-good pinned manifest** and re-resolves against a fresh registry, which then
fails. Use `instantiate.jl` (`Pkg.instantiate()` only) instead. **Reproducibility trap:** the tracked
mirror `merakit-setup/` carries `setup.jl` — the destructive one — and does **not** carry
`instantiate.jl`, so a reproducer working only from the public repo gets the script that breaks the
environment and not the one that builds it. Copying `instantiate.jl` into the mirror is the fix.

### Known gaps (stated, not fixed here)

- **`Manifest.toml`, the 7 run logs and the 2 `hb_lam3_*.npy` arrays inside this tree cannot be
  tracked by a `.gitignore` exception — this was attempted and reverted, 2026-08-17.** Rewriting
  the rule as `research/tools/MERAKit.jl/*` plus `!` negations makes `git check-ignore` report the
  paths as trackable, but they still cannot be staged: the tree holds its own `.git` (plain clone,
  no `.gitmodules`) and git will not descend into an embedded repository — `git add -n` and
  `git add -nf` both staged nothing. The `/*` form additionally made `git add -A` want to register
  MERAKit.jl as an embedded-repo **gitlink**, so it was reverted to the bare-directory rule.
  The two ways that do work: **(A)** copy the 10 artifacts (172,077 B) into this `merakit-setup/`
  mirror — the convention CLAUDE.md already mandates for the drivers; or **(B)** move
  `research/tools/MERAKit.jl/.git` out of the tree, which is now safe because the upstream URL and
  pinned revision are recorded above rather than only in the clone's own history.
- **`merakit-setup/qw_tci.jl` has drifted from the vendored copy** and the mirror holds the *stale*
  side. It is the TCI driver behind the α = 4 universality claim. Confirmed by `diff` 2026-08-17;
  it is the **only** drifted file of the 21 mirrored scripts — the other 20 are byte-identical.
- **Nine of our scripts exist only in the gitignored tree**, not in the mirror: `diag_prefactor.jl`,
  `dump_ising.jl`, `instantiate.jl`, `qw_block_test.py`, `qw_diag_blocking.jl`,
  `qw_diag_blocking2.jl`, `qw_diag_fusion.jl`, `qw_potts_smoke.jl`, `test_cone_v2.jl`. (The audit
  said "four further drivers"; the measured count is nine.)

Julia 1.8.5 (via juliaup `+1.8`) + MERAKit.jl pinned. The ESSENTIAL env vars (the ~/.ssh/known_hosts
ACL-denial poisons all Julia downloads; a clean HOME with a readable empty known_hosts fixes it):

```powershell
$env:Path = [System.Environment]::GetEnvironmentVariable("Path","User") + ";" + [System.Environment]::GetEnvironmentVariable("Path","Machine")
$env:JULIA_DEPOT_PATH = "C:\Users\jonca\.julia"
$env:JULIA_PKG_SERVER = "https://pkg.julialang.org"
$env:HOME = "D:\quantum-worldline\research\tools\juliahome"        # clean HOME w/ readable .ssh/known_hosts
$env:USERPROFILE = "D:\quantum-worldline\research\tools\juliahome"
Set-Location "D:\quantum-worldline\research\tools\MERAKit.jl"
julia +1.8 --project=. <script.jl>
```

- Compat pinned to TensorOperations 3 era; Project.toml.orig is the upstream original.
- Julia 1.12 does NOT work (CUDA/GPUCompiler + TensorKit 1.x API breaks). Use 1.8.
- Demo: `julia +1.8 --project=. demo/demo.jl` (Ising chi=8 ternary -> scaling dims).
