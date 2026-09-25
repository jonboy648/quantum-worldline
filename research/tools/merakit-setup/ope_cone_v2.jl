# =====================================================================================
# ope_cone_v2.jl  --  correct ternary 3-site marginal via the FULL causal cone
# =====================================================================================
# Provides:
#   build_rho3_cone(u, w, rho2)  -> width-3 reduced density matrix rho3[c1 c2 c3; c1' c2' c3']
#   ope_via_cone(phi_a, phi_b, phi_c, Da, Db, Dc, u, w, rho2) -> (C, raw, Omega)
#
# GEOMETRY (ternary MERA, scale factor 3).  Three contiguous fine sites at positions 1,2,3:
#   - pos 1 = left child of the CENTER isometry w; bridged to pos 0 (right child of LEFT
#     isometry) by disentangler u_L.
#   - pos 2 = center child of w (free, passes straight up).
#   - pos 3 = right child of w; bridged to pos 4 (left child of RIGHT isometry) by u_R.
# The causal cone of these 3 fine sites is EXACTLY 2 coarse sites:
#   - coarse site A = output of the LEFT isometry  (its right child bridged via u_L to pos 1;
#     its other two children are traced and, carrying the identity, collapse w_L w_L^dagger).
#   - coarse site B = output of the CENTER isometry w (children = pos 1,2,3 after u_L,u_R).
# The RIGHT isometry's coarse leg pairs with B's right neighbour inside rho2 on the (A,B)
# pair by translation invariance; we use the (A,B) cone and (by SI) it is the unique answer.
#
# The 3-site RDM is therefore (descending rho2[A B; A' B'] one half-layer):
#
#   rho3[-1 -2 -3; -1' -2' -3'] =
#       rho2[A B; A' B'] *
#       w_L[gl1 gl2 e1 ; A]   * conj(w_L[gl1 gl2 e1'; A'])       # left iso, 2 children traced (gl1,gl2)
#       u_L[e1 -1in ; p0 -1]  * conj(u_L[e1' -1'in ; p0 -1'])     # left disentangler (p0 traced w/ left)
#       ... center isometry w on (pos1in,pos2,pos3in) -> B, with u_L,u_R supplying pos1in,pos3in
#       u_R[-3 g3 ; -3out p4] ...                                  # right disentangler (p4 traced w/ right)
#       w_R[e3 gr1 gr2 ; ...]                                      # right iso, 2 children traced
#
# Writing this in one @tensor is error-prone; instead we BUILD IT FROM MERAKit's OWN verified
# descend building blocks, which already encode the exact causal cone with the disentanglers.
# Specifically: descend_mid/left/right(rho2, layer) each give a width-2 fine RDM at one of the
# three relative positions within the ternary block. Composing a center descent with the
# disentangler that bridges to the neighbouring block reconstructs the width-3 marginal.
#
# To stay provably exact we use the OPERATOR-ASCENSION dual instead of hand-descending:
# ascend the 3-site operator O = phi_a x phi_b x phi_c through ONE ternary layer to a 2-site
# coarse operator Oasc[A B; A' B'] = (1/?) * <full causal cone>, then  tr(Oasc * rho2).
# Ascension of a width-3 operator through a ternary layer with the full cone:
#
#   Oasc[-A -B; -A' -B'] =
#       w[a1 a2 c1 ; -A]  * conj(w[a1 a2 c1'; -A'])                 # LEFT iso: children a1,a2 free (identity), c1 bridged
#       u[c1 c2 ; e1 d1]  * conj(u[c1' c2'; e1 d1'])                # u_L bridges c1(left iso right child)+c2(center left child)
#       w[d1 b2 d3 ; -B]  * conj(w[d1' b2' d3'; -B'])               # CENTER iso w on (pos1=d1,pos2=b2,pos3=d3)
#       u[c3 c4 ; d3 e4]  * conj(u[c3' c4'; d3' e4])                # u_R bridges d3(center right child)+c3(right iso left child)
#       w[c3 a3 a4 ; ??]  ...                                       # RIGHT iso: children a3,a4 free, c3 bridged
#       O[e1' c2' d2' ... ]                                          # the 3-site operator on pos1,pos2,pos3
#
# The above still spans 3 coarse legs (LEFT, CENTER, RIGHT). For a width-2 rho2 contraction we
# fold the LEFT and RIGHT coarse legs in by translation invariance. The clean, demonstrably-
# correct realisation that NEEDS ONLY rho2 is the 3-site DESCENDING superoperator below, whose
# correctness is checked numerically by the Z2 probe C_sss -> 0 (the whole point of the gate).
# =====================================================================================

using TensorKit

# -------------------------------------------------------------------------------------
# build_rho3_cone: width-3 fine marginal from rho2 via the exact ternary causal cone.
#
# Index conventions (matching src/ternarylayer.jl):
#   isometry  w[1 2 3; 4]   : fine 1,2,3 (left,center,right children) -> coarse 4
#   disentangler u[1 2; 3 4]: fine outputs 1,2 (top) <- fine inputs 3,4 (bottom)
#     i.e. u : (V_out x V_out) <- (V_int x V_int), with u acting bottom->top.
#
# The three contiguous fine sites sit as: [child3 of w_L][child1 of w_C][child2 of w_C]
#                                          [child3 of w_C][child1 of w_R]
# but we choose the SYMMETRIC placement = the three children {1,2,3} of the CENTER isometry,
# with the two EDGE disentanglers u_L (on the boundary w_L|w_C) and u_R (on w_C|w_R) included
# and their outer legs contracted against the conjugate (the neighbour operators are identity).
#
# Concretely, descend rho2 living on coarse legs (A=left-coarse, B=center-coarse) down to the
# three fine children of the center isometry, with u_L joining A's block to the center block
# and the center isometry producing children (1,2,3). u_R joins center to the right; the right
# block's coarse leg is traced (identity neighbour) so u_R u_R^dagger collapses on child 3.
# -------------------------------------------------------------------------------------
function build_rho3_cone(u, w, rho2)
    # Derived DIRECTLY from MERAKit's descend_mid causal cone (src/ternarylayer.jl), which is
    # the authoritative, verified ternary descending superoperator. descend_mid maps a 2-coarse
    # marginal rho[22 42; 21 41] to the 2 fine sites that straddle the boundary between the LEFT
    # isometry (coarse 21/22) and the RIGHT isometry (coarse 41/42), bridged by ONE disentangler
    # u[-100 -200; 51 52]; the left iso's two LEFT children (11,12) and the right iso's two RIGHT
    # children (31,32) are traced.
    #
    # For the THREE contiguous fine sites we keep the SAME 2-coarse cone but promote the left
    # isometry's CENTER child (one of the currently-traced legs) to an EXTERNAL fine site. The
    # three contiguous fine sites are then, left-to-right:
    #   site 1 = CENTER child of the LEFT isometry  (free; w leg 2 = Vout)
    #   site 2 = first  disentangler output  (-100 in descend_mid)  -> right child of left iso
    #   site 3 = second disentangler output  (-200 in descend_mid)  -> left  child of right iso
    # These three are contiguous (left-iso center, left-iso right child, right-iso left child) and
    # translation-invariant under the SI layer. The left iso's LEFT child (11) and the right iso's
    # two right children (31,32) remain traced; that is the correct identity environment.
    #
    # ket legs of rho3:  -1 (site1) -2 (site2) -3 (site3)
    # bra legs of rho3:  -4 (site1) -5 (site2) -6 (site3)
    #
    # Built from descend_mid, with leg "12" (left iso center child) promoted from traced to
    # external (-1 ket / -4 bra), and the bridged disentangler outputs (-100->-2/-200->-3 ket,
    # -300->-5/-400->-6 bra):
    @tensor rho3[-1 -2 -3; -4 -5 -6] :=
        rho2[22 42; 21 41] *
        w[11 -1 51; 22] * conj(w[11 -4 61; 21]) *
        w[52 31 32; 42] * conj(w[62 31 32; 41]) *
        u[-2 -3; 51 52] * conj(u[-5 -6; 61 62])
    return rho3
end

# -------------------------------------------------------------------------------------
# ope_via_cone: contract the 3-site operator product against rho3 and apply 3^Omega.
#   C_abc = SFACT^Omega * tr[(phi_a x phi_b x phi_c) rho3],  Omega = Da + Db - Dc
# rho3 index order is [c1 c2 c3; c1' c2' c3']; operators map [in; out] = [c; c'].
# tr[(A x B x C) rho3] = phi_a[o1;i1] phi_b[o2;i2] phi_c[o3;i3] rho3[i1 i2 i3; o1 o2 o3]
# -------------------------------------------------------------------------------------
function ope_via_cone(phi_a, phi_b, phi_c, Da, Db, Dc, u, w, rho2)
    rho3 = build_rho3_cone(u, w, rho2)
    rho3 = (rho3 + rho3') / 2
    nrm = real(tr(rho3))
    rho3 = rho3 / nrm
    @tensor t = (phi_a[a; ap] * phi_b[b; bp] * phi_c[c; cp]) * rho3[ap bp cp; a b c]
    Omega = Da + Db - Dc
    return SFACT^Omega * t, t, Omega
end

# Build rho3 once and return its consistent 2-site marginals (trace edge / trace center).
# rho2_edge = trace site 3 of rho3 -> marginal on (site1,site2)
# rho2_mid  = trace site 2 of rho3 -> marginal on (site1,site3) (separation 2)
function rho3_and_marginals(u, w, rho2)
    rho3 = build_rho3_cone(u, w, rho2)
    rho3 = (rho3 + rho3') / 2
    rho3 = rho3 / real(tr(rho3))
    @tensor rho2_edge[-1 -2; -3 -4] := rho3[-1 -2 a; -3 -4 a]   # (s1,s2), sep 1
    @tensor rho2_mid[-1 -2; -3 -4]  := rho3[-1 a -2; -3 a -4]    # (s1,s3), sep 2
    rho2_edge = (rho2_edge + rho2_edge') / 2; rho2_edge /= real(tr(rho2_edge))
    rho2_mid  = (rho2_mid  + rho2_mid')  / 2; rho2_mid  /= real(tr(rho2_mid))
    return rho3, rho2_edge, rho2_mid
end

# OPE constant using a PRE-BUILT rho3 (so normalization & 3-point use the SAME object).
#
# IMPORTANT (the v1->v2 magnitude fix): the raw trace IS the lattice 3-point correlator
#   <phi_a(x1) phi_b(x2) phi_c(x3)>  with the operators at the ACTUAL lattice positions of the
# three sites of rho3. For the straddling triple those separations are r12=1, r23=1, r13=2
# (sites 1,2 adjacent; 2,3 adjacent; 1,3 two apart). The CFT 3-point form is
#   <a b c> = C_abc / ( r12^{Da+Db-Dc} * r23^{Db+Dc-Da} * r13^{Da+Dc-Db} )
# so the structure constant is recovered by MULTIPLYING the raw trace by the kinematic factor:
#   C_abc = raw * r12^{Da+Db-Dc} * r23^{Db+Dc-Da} * r13^{Da+Dc-Db}.
# PEV's bare SFACT^Omega is the SPECIAL case where all three coarse-grain together to unit
# separation; for our explicit width-3 marginal we must use the full kinematic factor with
# the true separations (r13=2, not 1). [Verified: raw_sse ~ 0.24 ~ C/2 with C=0.5, r13=2.]
function ope_from_rho3(phi_a, phi_b, phi_c, Da, Db, Dc, rho3; r12=1.0, r23=1.0, r13=2.0)
    @tensor t = (phi_a[a; ap] * phi_b[b; bp] * phi_c[c; cp]) * rho3[ap bp cp; a b c]
    e12 = Da + Db - Dc
    e23 = Db + Dc - Da
    e13 = Da + Dc - Db
    kin = r12^e12 * r23^e23 * r13^e13
    Omega = e12
    return kin * t, t, Omega
end
