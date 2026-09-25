# Running MERAKit.jl (working invocation, 2026-06-19)

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
