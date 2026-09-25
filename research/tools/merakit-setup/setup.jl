ENV["JULIA_PKG_SERVER"] = "https://pkg.julialang.org"   # HTTPS PkgServer: no git, no ssh
ENV["JULIA_PKG_USE_CLI_GIT"] = "false"
import Pkg
rm("Manifest.toml"; force=true)
Pkg.Registry.update()
Pkg.resolve()
Pkg.instantiate()
using MERAKit
println("MERAKIT LOADS OK")
