# HYP-033 — v3 amendment (APPROVED by Jon 2026-09-22, "approved"; in force, see PREREGISTRATION-HYP033.md §v3)

**Written 2026-09-22, before any registered f value was printed.** The registered grid is running blinded.
Prompted by a devil's-advocate review of `PREREGISTRATION-HYP033.md`. Checked numerically on an
UNREGISTERED network (Haar chi = 3, seed 9999, outside every registered seed range and chi).

## The problem: the registered statistic is pinned by an identity

For the pure state on R_low, A, and everything else, f(A) + f(complement of A) = 1 exactly (the G2 purity sum).
Monotonicity of mutual information then gives f(A_m from the left) <= 1 - f(A_{17-m} from the right).
So m_L + m_R <= 17, and the registered m_half (the two-edge average) is <= 8.5 **for every isometric network on this graph**.
The cut predictor puts the drop between m = 8 and 9, which is m_half = 8.5: the saturation point of the bound.

**Numerical check (unregistered Haar network, `haar_test/haar_chi3_seed9999/da_check.json`):**

| edge | m_half | w |
|---|---|---|
| left | 8.50 | 9 |
| right | 8.50 | 9 |

f_L(8) + f_R(9) = 0.724 + 0.276 = 1.000. The outside of the cone plus R_up adds essentially nothing.
A random network lands at 8.50, inside the "cut-like" window [7, 10]. **m_half cannot tell cut-like apart
from random, and outcome 2 ("tracks the cut in the MERA but not in C-HAAR") cannot occur on m_half.**
Only w can separate the two, and w registers "smooth" for Haar (w = 9 > 6).

**Weighted-capacity recount (`g0_cut_recount_weighted.py`, registered observable I(R_low:A)):**
with log-dimension capacities at chi = 6 and chi = 8, the cut drop stays between m = 8 and 9 on both edges.
Unit capacities were not what put the predictor at the saturation point; the geometry of this family did.

## Proposed changes (for Jon's approval)

1. **Report m_L and m_R separately, plus the side-information gap g = 17 - (m_L + m_R).** g = 0 means the
   outside and R_up give no help. Along this family that is the only content m_half has.
2. **Make the onset of loss the primary cut-versus-random statistic: m_0.9 per edge, the first m with f < 0.9.**
   The cut predictor keeps f at about 1 until the cut flips. Its m_0.9 is 9 with unit capacities and 7 with
   log-dimension capacities (f = 0.89 at m = 7 and 8). The unregistered Haar network starts losing
   information at once: f = 0.90 at m = 3 and 0.72 at m = 8, so m_0.9 = 3. Complementarity does not pin
   m_0.9. It only links it to the far tail of the other edge (f_L(m) >= 0.9 forces f_R(17 - m) <= 0.1).
   Proposed reading: cut-like if m_0.9 >= 6 on both edges AND at least 3 above the C-HAAR mean at the
   same chi. Thresholds to be fixed by Jon before unblinding.
   *(Checked and rejected: regions that extend past the cone. `g0_cut_recount_weighted.py` gives f_cut = 1
   for the cone minus m sites plus j outside sites at every m <= 5 and j <= 8, so they add nothing
   over A_m. The "168 intervals" in `g0_window_count.py` used the old two-leg normalization.)*
3. **Downgrade outcome 2 to "Level 3, holographic-code-like encoding"** unless a CFT-matched
   non-geometric ansatz is added. C-HAAR is a different state, not a matched control on CFT observables.
4. Keep everything else: the observable, gates G1 to G5, the controls, the blinding, and the cap order.

The registered f(A_m) grid stays useful under all of this. Items 1 and 2 are computed from the points it already produces. No new regions and no second pass are needed.
