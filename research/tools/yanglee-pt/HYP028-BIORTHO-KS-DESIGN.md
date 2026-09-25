# HYP-028 — Biorthogonal Koo-Saleur route via PAPER-133 (2606.16785v2)

**Written 2026-08-11 from a full read of the v2 main text.** (v2 = clarity revision per scan #19;
method unchanged from v1. Dated 2026-08-03 on the PDF.)

## What PAPER-133 actually provides (Liu, Shimizu, Liu, Kawabata)

Projected-partition-function spectroscopy on PERIODIC non-Hermitian critical chains:

- Model (their Eq. 13): `H_YL = -Σ_j (σ^z_j σ^z_{j+1} + λ σ^x_j + i h σ^z_j)`, PBC.
  PT via P = Πσ^x, T = K. For λ > 1 there is h_c(λ) where PT breaks → M(2,5) Yang-Lee.
- **The PT-edge dodge (the thing SIM-053/055 lacked):** evaluate everything at
  `h = h_c^∞(λ)`, the INFINITE-SIZE critical field extrapolated from finite-size
  exceptional points h_c^L(λ). Finite L at that h sits INSIDE the PT-unbroken phase —
  no exceptional-point singularity, η-pseudo-Hermitian with **η = P** (parity!).
- Biorthogonal projection (their Eq. 2): `Z_{Φ,i}(L) = ⟨Φ̃|Ψ_{i,R}⟩⟨Ψ_{i,L}|Φ⟩ / ⟨Ψ_{i,L}|Ψ_{i,R}⟩`
  with dual `⟨Φ̃| = ⟨Φ|P / ⟨Φ|P|Φ⟩` (their Eq. 10). Preparations: X = ⊗(|↑⟩+|↓⟩)/√2
  (η-invariant, the good one), Z = ⊗|↑⟩, Rand (ratio diagnostics).
- Extraction: fit `−log Z_{Φ,i} = αL − log G_{a,i} + β/L + O(L^−ω)` (Eq. 7) or the
  extensive-term-cancelling ratio R = Z_{Φ,1}/Z_{Φ,φ} (Eq. 8/15).
- **Benchmarks to reproduce (λ = 4, their Table I / Eq. 14):**
  - g_1 = ((5−√5)/10)^{1/4}: num 0.725339(51) vs BCFT 0.725073
  - R_∞ = Z_{X,1}/Z_{X,φ} → −(1+√5)/2: num −1.62184(94) vs −1.618034 (NEGATIVE —
    impossible in any unitary CFT; the microscopic signature of nonunitarity)
- Their Fig. 1 runs 1/L ≤ 0.12 (L ≳ 8, up to L ~ 40 → beyond-ED sizes are likely
  MPS-based; SM has details). ED-scale L ≤ 20 should reproduce at reduced precision.

## Reproduction plan (Phase 1 — the G4-gate prerequisite)

`qw_yanglee_pt.jl` (sparse ED, L = 8..18, λ = 4):
1. Build H_YL sparse; per L, scan h for the lowest PT-pair coalescence → h_c^L (track
   the two lowest-Re eigenvalues' collision / imaginary-part birth).
2. Extrapolate h_c^L → h_c^∞ (they cite a known form; fit h_c^L = h_c^∞ + a L^{−b}).
3. At h = h_c^∞: right eigenstates (Arpack/KrylovKit on H), left via η-pairing
   ⟨Ψ_L| = (P|Ψ_R⟩)^† (η-pseudo-Hermitian ⇒ left = parity-image of right; verify
   ⟨Ψ_L|Ψ_R⟩ ≠ 0 and biorthogonality across states).
4. Project X preparation → Z_{X,1}, Z_{X,φ}; fit Eq. 7 / ratio Eq. 15.
5. GATE: g_1 within ~1% of 0.7251 AND R_∞ negative within ~2% of −1.618.

## Phase 2 — the NEW measurement (our contribution, the falsifiable surprise)

The same left-right pairing defines **biorthogonal KS elements**:
`M_T = ⟨T_L| H_{±2} |0_R⟩ / ⟨T_L|T_R⟩^{1/2}⟨0_L|0_R⟩^{1/2}` (normalization TBD — the
biorthogonal norm can be NEGATIVE; both sign conventions must be tracked).

Question HYP-028 actually asks: does `c_KS ≡ 2|M_T · N/(2πv_T)|²` (the relation
validated at Ising/TCI/Potts, SIM-067/068/069) reproduce Yang-Lee's central charge —
and WHICH one:
- c = −22/5 (true central charge; would require M_T² < 0 → the biorthogonal element
  squared goes negative, only possible with indefinite norms), or
- c_eff = 2/5 (effective/Casimir charge, what governs finite-size gaps: E_0(L) ~ −π c_eff v/6L).
The two predictions differ by sign AND magnitude → cleanly distinguishable. Either
outcome is informative; agreement with −22/5 including the sign would be the striking
result (KS elements seeing the indefinite-metric structure). v calibration: from the
φ tower (Δ_φ = −2/5 < 0! gaps INVERT — the φ state sits BELOW the "vacuum" 1 in
finite-size spectrum; identify towers by momentum + PT quantum numbers, not energy order).
Also: Δ_T = 2 still exact (T is always (2,0)) — v_T calibration from the T gap itself,
cross-checked against c_eff in E_0(L) scaling.

## Phase-2 refinements (2026-08-11, pre-gate)

1. **Use the PRODUCT form, not |M|²:** define
   `c_KS = 2 · ⟨0_L|H_{−2}|T_R⟩⟨T_L|H_{+2}|0_R⟩ / (⟨T_L|T_R⟩⟨0_L|0_R⟩) · (N/2πv_T)²`.
   No square roots → no branch ambiguity; reduces to 2|M_T|² in the unitary case; can go
   NEGATIVE via indefinite biorthogonal norms — which is exactly what c = −22/5 requires.
   Sign is now part of the measurement, not a convention.
2. **The KS "vacuum" is |1⟩, an EXCITED state at YL:** the c-relation reads ⟨T|H₂|1⟩ with
   |1⟩ = the conformal vacuum = the 1-tower base = the SECOND k=0 state (the physical GS is
   |φ⟩, Δ_φ = −2/5 < 0). Elements must be taken against the 1-sector base, biorthogonally
   on both sides.
3. **M(2,5) null vectors reshape the k=±2 cluster:** φ has a level-2 null (L₋₂ − (5/2)L₋₁²)|φ⟩ = 0,
   so the φ-tower contributes only ONE spin-2 state (at Δ−Δ_φ = 2.0 above the physical GS);
   T = L₋₂|1⟩ sits at 2.4 above the physical GS (Δ_T = 2 above |1⟩). Expect a SPARSE k=2
   cluster: one φ-descendant below T. Δ_T-gate: measure gaps from |1⟩, not from |φ⟩.
4. v_T from (E_T − E_1)·L/(2π·2); cross-check v from (E_1 − E_φ)·L/(2π·(2/5)) — the 1−φ split
   is Δ = 0 − (−2/5) = 2/5 exactly.

## Traps / discipline

- σ ordering: in YL the ground state on the cylinder is φ (lowest Re E), NOT 1.
  PAPER-133 Eq. 6 makes exactly this point (ι_g sector). All "gap" definitions must
  anchor on the actual lowest-Re state.
- Do NOT work at h_c^L (exceptional point — defective, no biorthogonal basis).
  Always h_c^∞ at finite L.
- ⟨Ψ_L|Ψ_R⟩ → 0 signals proximity to an EP; monitor it as the health metric.
- S_res = log(ΔL) (PAPER-138) is a secondary diagnostic only — does NOT satisfy G4.
- The 2607.14732 (Vander Linden et al., non-Herm 5-state Potts, PRB 113) in their ref
  list [18] is the puMPS-adjacent tooling if we outgrow ED.

## Files

- This design: research/tools/yanglee-pt/HYP028-BIORTHO-KS-DESIGN.md
- Paper: research/downloads/2606.16785v2.pdf (v2, dated 2026-08-03)
- Driver (Phase 1): research/tools/yanglee-pt/qw_yanglee_pt.jl (to be written)
