# C_TTT Route B — the circle realization (design, 2026-07-19)

**STATUS:** DESIGN → implementing. Successor to Route A (CLOSED, SIM-065/066: the one-site
MERA Δ≈2 eigenbasis cannot support stable {T,T̄} extraction; gates certify the chiral split
but not span membership).

**Target (unchanged):** PEV-normalized C_TTT = 2√2/√c — Ising **4.000**, TCI **3.381**,
Potts **3.162**.

---

## 1. Why the circle, not the width-2 MERA translation superoperator

SIM-066 named "width-2 translation-phase eigenbasis (momentum as an actual quantum number)"
as the successor. Working the design through, the *line* version of that idea is shakier than
the original design doc suggested: a scale-invariant fixed-point operator on the line must
satisfy θ = 3θ (mod 2π) for its translation eigenphase under one ternary RG step, so the only
allowed fixed-point phases are θ ∈ {0, π}. Conformal spin is NOT a lattice translation
eigenphase on the infinite line — it only becomes a genuine quantum number on the **circle**,
where momentum is quantized as P = (2π/N)(s + n) and the s=±2 states |T⟩, |T̄⟩ are *exact,
distinct eigenstates* of the translation operator. That is the rigorous content of "momentum
as an actual quantum number", and it is the setting of the established conformal-data-from-
spin-chains program (Koo–Saleur lattice Virasoro; Milsted–Vidal; Zou–Milsted–Vidal).

So Route B is realized on the **periodic critical chain** (exact diagonalization, local CPU),
not inside MERA. If it validates, the ED-validated operator construction can later be fed
back into a width-2 MERA cross-check; that is optional, not blocking.

## 2. The two structural facts that make it work

**(a) Kramers–Wannier parity kills the ε contamination — exactly.**
At the self-dual point g=1 of H = −Σ(X_j X_{j+1} + Z_j), the energy density
ĥ_j = −(X_j X_{j+1} + Z_j) is KW-EVEN (KW exchanges X_jX_{j+1} ↔ Z_j), while ε is KW-ODD
(ε̂_j = X_jX_{j+1} − Z_j is the ε lattice representative). Therefore ĥ has **zero ε content
at the critical point** — its leading connected scaling content is purely the Δ=2 spin-0
combination a·(T+T̄), with the next KW-even contributions in the identity module at Δ=4
(L₋₂²𝟙-type), giving relative corrections O(x⁻²) to correlators. This is what Route A never
had: a lattice operator whose leading content is *guaranteed* pure stress tensor.

**(b) Equal-time chiral factorization: no mixed kinematics on the slice.**
The design doc's §1.4 trap ("feeding T+T̄ into the scalar 3-pt formula gives a wrong number")
does not bite here, because on an equal-time slice every mixed correlator vanishes exactly:
⟨TT̄⟩ = 0 and ⟨TTT̄⟩ = ⟨TT̄T̄⟩ = 0 by chiral factorization. Hence
  ⟨(T+T̄)(T+T̄)⟩ = ⟨TT⟩ + ⟨T̄T̄⟩   and   ⟨(T+T̄)³⟩ = ⟨TTT⟩ + ⟨T̄T̄T̄⟩,
i.e. the h-only correlators are exactly twice the (real, equal-time) chiral answers. No spin
resolution step is needed at all — the chirality bookkeeping is *exact* instead of extracted.

## 3. Exact cylinder kinematics and the extraction formulas

Map the plane to the cylinder of circumference N, z = exp(2πiw/N), equal time w = x real.
With the chord kernel  **s(x) ≡ (π/N) / sin(πx/N)**  (which automatically handles ring
distance), the Schwarzian constants drop from *connected* correlators, and:

  ⟨T(x)T(0)⟩_conn  = (c/2) · s(x)⁴
  ⟨T(x₁)T(x₂)T(x₃)⟩_conn = c · s(x₁₂)² s(x₂₃)² s(x₁₃)²      (from ⟨TTT⟩ = c/(z₁₂z₂₃z₃₁)²)

For ĥ = const + a(T+T̄) + O(Δ=4):

  ⟨ĥĥ⟩_conn(x)      = A₂ · s(x)⁴,           A₂ = a²c
  ⟨ĥĥĥ⟩_conn(x_i)   = A₃ · s₁₂²s₂₃²s₁₃²,    A₃ = 2a³c

Both unknowns (a, c) drop out of the ratio; the PEV-normalized chiral structure constant is

  **C_TTT^meas = √2 · A₃ / A₂^{3/2}**   (target 2√2/√c; Ising 4.000)

equivalently c_meas = (2A₂^{3/2}/A₃)². The √2 converts the unit-normalized *scalar* (T+T̄)/√2
coefficient to the chiral C_TTT convention (both recorded; they carry the same content).

## 4. Gates (in order)

- **G1 spectrum**: ED spectrum matches Ising CFT towers; the Δ≈2 even-sector states carry
  lattice momentum s = ±2 (translation-operator eigenphase e^{±2·2πi/N}) — the "momentum is
  a real quantum number" statement, verified directly.
- **G2 exponents**: log-log slope of ⟨ĥĥ⟩_conn vs chord distance ≈ −4 (this is α=4 on the
  circle), σ: −1/4, ε̂: −2.
- **G3 pin (C_σσε=0.5)**: same machinery, σ̂=X (Z2-odd), ε̂=XX−Z (KW-odd):
  C_σσε = A₃^{σσε} / (A₂^{σσ} · √A₂^{εε}) with scalar cylinder kinematics
  s₁₂^{Δσ+Δσ−Δε} s₂₃^{…} s₁₃^{…}. Must give 0.50 before C_TTT is read.
- **G5 the number**: C_TTT^meas → 4.000 under N-extrapolation (N = 8…16+), stable across
  separation windows. Success = 4.00 ± ~0.1 with monotone finite-size convergence.

## 5. Corrections / risks

- Δ=4 identity-module content of ĥ (L₋₂²𝟙 etc.): relative O(x⁻²) — use maximally separated
  triples (x ~ N/3) and fit/extrapolate in N. This is the main finite-size systematic.
- Descendant corrections to cylinder forms for the *lattice* operator: same O(x⁻²) class.
- TCI (O'Brien–Fendley chain, λ₃=0.856): ĥ there may contain ε′ (Δ=6/5) if ε′ is KW-even —
  the Route-A R2 risk returns. Handle by multi-exponent fit (exponents known exactly) or an
  improved operator (mix two KW-even lattice densities to cancel the ε′ channel, calibrated
  on the 2-pt function). Cross that bridge only after Ising 4.000 locks.
- Ising has a free-fermion backstop: ĥ is a Majorana bilinear, so ⟨ĥĥĥ⟩ is exact via Wick at
  N ~ 10³ if ED finite-size proves too coarse. Phase 2 if needed.

## 6. Honest framing

On the circle, ⟨TTT⟩ ∝ c is Virasoro-fixed, so this measurement is of the same epistemic kind
as C_σσε = 0.5: the nontrivial statement is that the *lattice* operator, normalized only by
its own 2-pt function, reproduces the number conformal symmetry dictates — i.e. the emergent
stress-tensor sector behaves as a c-central-charge Virasoro algebra, quantified by the 3-pt/
2-pt ratio hitting 2√2/√c per class. That is the "graviton self-coupling across the c-ladder"
claim, now with exact kinematics instead of a struggling variational basis. The Route-A
negative (one-site PEV cannot do spin-2) stands as its own methods finding.

Driver: `research/tools/cttt-circle/qw_cttt_circle.py` (Python, sparse ED, local).

---

## 7. ADDENDUM (2026-07-19, same day): §3 falsified empirically → matrix-element realization

ED falsified the equal-time-correlator formulas of §3 as written: ⟨ĥĥ⟩_conn is **negative**,
decays faster than the cylinder s⁴ form (no plateau of val/s⁴), and vanishes **exactly** at
antipodal separation x=N/2 — while ⟨ε̂ε̂⟩/s² and ⟨σ̂σ̂⟩/s^{1/4} plateau perfectly and the
correlator-based C_σσε extrapolates to 0.4996. So the machinery is right and the *equal-time
ĥ 2-pt/3-pt route* is wrong: the naive "h ⊃ a(T+T̄) ⇒ +a²c·s⁴ tail" bookkeeping fails on the
slice (exact free-fermion form of the tail: −(16/π²)/(4x²−1)², *negative*). The sign/shape
resolution is a chiral-bookkeeping subtlety left OPEN and flagged for a literature check; do
not quote §3's A₂/A₃ formulas.

The working realization is the **Koo–Saleur matrix-element route** (Milsted–Vidal style),
which is also the purer expression of "momentum as a quantum number":
- Resolve exact (E, Z₂ charge, translation phase) eigenstates; |T⟩ = lowest even-sector
  state with s = +2. (Z₂ resolution is essential: the σ-tower's level-2 descendants are
  accidentally degenerate with T at small N and sit at s=±2 in the odd sector.)
- H_n ≡ (N/2πv) Σ_x e^{inx·2π/N}(ĥ_x − e₀) ≈ L_n + L̄_{−n};  c_meas = 2|⟨T|H_{±2}|0⟩|².
- Momentum conservation does the chiral split for free; the wrong-chirality element
  ⟨T|H_{∓2}|0⟩ (= L̄₂|0⟩-type) is a **structural zero** — measured 0.0000 at every N. This is
  the G4-analog gate, and unlike Route A's G4 it cannot be satisfied vacuously.
- C_sse pin via state-ratio: ⟨σ|ε̂(0)|σ⟩/⟨ε|ε̂(0)|0⟩ (lattice normalization cancels).
- C_TTT = 2√2/√c_meas. Ward-locking honesty: on the circle the T-sector 3-pt data is
  Virasoro-fixed, so this *is* a measurement of the emergent Virasoro central extension
  (§6 framing) — same epistemic status as C_σσε.

**ISING RESULT (2026-07-19, N=8…18, 1/N² extrapolation):**
  c_meas → 0.49871 (0.5), **C_TTT → 3.9936 (4.000, 0.16%)**, C_sse → 0.49996 (0.5),
  G4 = 0.0000 at every N. **GATE PASSED.** Literature anchor found afterward: Zou–Milsted–
  Vidal (arXiv:1710.05397, PRL 121, 230402) use exactly this c-formula (c ≈ 2|⟨T|H₋₂|I⟩|²).

**T-identification note:** T = the LOWEST even-sector |s|=2 state. Max-element ID was tried
and falsified — lattice band-edge states carry ~2× larger raw UV elements than T (the KS
suppression applies only to low CFT states as N→∞); verified on Ising (the Δ→3 ε-tower
s=2 state has element 0.96 vs T's 0.50 at N=12).

**TCI STATUS (O'Brien–Fendley λ₃=0.856 project convention = 2×H_OF(λ=0.428)): NOT
CONVERGED AT ED SIZES — expected, not a route failure.** Spectrum G1 is beautiful (σ→0.071
vs 3/40, ε→0.195 vs 1/5, σ'→0.876 vs 7/8, towers right), but the T-element gives c_meas
1.45→1.21 (N=10→16), far from 0.7 and drifting slowly. Mechanism: TCI has L₋₂ε at Δ=2.2
with the SAME quantum numbers as T (even, s=2), only 0.2 above — element contamination dies
as ~N^{-0.2}. Ising converges fast because its nearest same-quantum-number state is at Δ=3.
This is exactly why ZMV needed **N ≤ 128 with puMPS (D=28–44)** for the OF model. N≤22 ED
cannot close it. Velocity self-calibration also unreliable at these N (v_σ≈3.2, v_desc≈3.5
mutually inconsistent).

**NEXT STEP (TCI/Potts):** puMPS at N ~ 64–128. Ashley Milsted's open-source `puMPS`
package is in **Julia** (github.com/amilsted) — same stack as our MERAKit setup (Julia 1.8
+ TensorKit env already proven, RunPod CPU recipe available if heavy). Vendor it, drive the
OF chain, reuse this driver's H_n/element machinery translated to puMPS Bloch states.
Deep irony worth recording: Route A (one-site MERA, χ≤12) never had a chance at TCI — even
exact diagonalization needs N~128-scale IR resolution to separate T from L₋₂ε.
