# qw_cttt_circle.py -- C_TTT Route B: periodic critical TFIM chain, exact diagonalization.
#
# Design: research/tools/merakit-setup/CTTT-ROUTE-B-CIRCLE-DESIGN.md
# Target: C_TTT = 2*sqrt(2)/sqrt(c) = 4.000 (Ising c=1/2), via
#   <hh>_conn(x)        = A2 * s(x)^4,            A2 = a^2 c
#   <hhh>_conn(x1,x2,x3)= A3 * s12^2 s23^2 s13^2, A3 = 2 a^3 c
#   C_TTT = sqrt(2) * A3 / A2^(3/2)
# with the chord kernel s(x) = (pi/N)/sin(pi x/N), and h_j = -(X_j X_{j+1} + Z_j)
# (KW-even at g=1 => zero eps content; leading content a*(T+Tbar)).
#
# Gates: G1 spectrum+momentum (s=+-2 at Delta=2), G2 exponents, G3 pin C_sse=0.5, G5 number.

import json
import sys
import numpy as np
import scipy.sparse as sp
import scipy.sparse.linalg as spla

I2 = sp.identity(2, format="csr")
SX = sp.csr_matrix(np.array([[0.0, 1.0], [1.0, 0.0]]))
SZ = sp.csr_matrix(np.array([[1.0, 0.0], [0.0, -1.0]]))


def place(ops, N):
    """Tensor product over sites 0..N-1 with ops[site] (2x2 sparse) inserted, identity elsewhere.
    Site j corresponds to bit j of the basis index (site 0 = least significant bit)."""
    out = sp.identity(1, format="csr")
    for j in range(N):
        out = sp.kron(ops.get(j, I2), out, format="csr")  # site j -> bit j
    return out


def build_ops(N):
    """Return H, h[j], eps[j], sig[j] for the critical TFIM on a ring of N sites."""
    h = []
    eps = []
    sig = []
    for j in range(N):
        xx = place({j: SX, (j + 1) % N: SX}, N)
        z = place({j: SZ}, N)
        h.append((-(xx + z)).tocsr())
        eps.append((xx - z).tocsr())
        sig.append(place({j: SX}, N))
    H = h[0].copy()
    for j in range(1, N):
        H = H + h[j]
    return H.tocsr(), h, eps, sig


def build_ops_of(N, lam3):
    """O'Brien-Fendley chain (TCI point lam3=0.856, project convention qw_of_pregate.py),
    Hadamard-rotated so the Z2 charge is prod_j Z_j (diagonal):
      h_j = -2(Z_j + X_j X_{j+1}) + lam3*(Z_j X_{j+1} X_{j+2} + X_j X_{j+1} Z_{j+2}).
    At lam3=0 this is 2x the critical TFIM (v=4)."""
    h = []
    eps = []
    sig = []
    for j in range(N):
        xx = place({j: SX, (j + 1) % N: SX}, N)
        z = place({j: SZ}, N)
        hj = -2.0 * (z + xx)
        if lam3 != 0.0:
            hj = hj + lam3 * place({j: SZ, (j + 1) % N: SX, (j + 2) % N: SX}, N)
            hj = hj + lam3 * place({j: SX, (j + 1) % N: SX, (j + 2) % N: SZ}, N)
        h.append(hj.tocsr())
        eps.append((xx - z).tocsr())
        sig.append(place({j: SX}, N))
    H = h[0].copy()
    for j in range(1, N):
        H = H + h[j]
    return H.tocsr(), h, eps, sig


def translation_matrix(N):
    """Permutation matrix for site j -> j+1 (bit rotate-left by one)."""
    dim = 1 << N
    src = np.arange(dim)
    dst = ((src << 1) | (src >> (N - 1))) & (dim - 1)
    return sp.csr_matrix((np.ones(dim), (dst, src)), shape=(dim, dim))


def chord_kernel(x, N):
    return (np.pi / N) / np.sin(np.pi * x / N)


def ring_sep(a, b, N):
    d = abs(a - b) % N
    return min(d, N - d)


def spectrum_gate(H, N, v=2.0, k=14):
    """G1: low spectrum -> (Delta_n, conformal spin s_n via translation eigenphase)."""
    vals, vecs = spla.eigsh(H, k=k, which="SA")
    order = np.argsort(vals)
    vals, vecs = vals[order], vecs[:, order]
    T = translation_matrix(N)
    out = []
    i = 0
    while i < k:
        # cluster degenerate energies, diagonalize T in the cluster
        j = i + 1
        while j < k and vals[j] - vals[i] < 1e-8:
            j += 1
        block = vecs[:, i:j]
        Tblk = block.conj().T @ (T @ block)
        phases = np.angle(np.linalg.eigvals(Tblk))
        for ph in phases:
            s = ph / (2 * np.pi / N)
            delta = N * (vals[i] - vals[0]) / (2 * np.pi * v)
            out.append((float(delta), float(s)))
        i = j
    return out, float(vals[0])


def momentum_states(H, N, k=24, degtol=1e-6):
    """Low eigenstates resolved into exact (Z2 charge, translation) eigenstates.
    Returns list of (E_raw, s, q, vec); scaling dimensions are assigned downstream
    once the velocity is fixed (exact or self-calibrated)."""
    vals, vecs = spla.eigsh(H, k=k, which="SA")
    order = np.argsort(vals)
    vals, vecs = vals[order], vecs[:, order]
    T = translation_matrix(N)
    # Z2 charge prod_j Z_j is diagonal in the computational basis
    dim = 1 << N
    qdiag = np.array([1 - 2 * (bin(i).count("1") % 2) for i in range(dim)], dtype=float)
    out = []
    i = 0
    while i < k:
        j = i + 1
        while j < k and vals[j] - vals[i] < degtol:
            j += 1
        block = vecs[:, i:j].astype(complex)
        # split the degenerate cluster by Z2 charge first (Q commutes with H and T)
        Qblk = block.conj().T @ (qdiag[:, None] * block)
        qev, qU = np.linalg.eigh(Qblk)
        for qval in (1.0, -1.0):
            cols = [c for c in range(len(qev)) if abs(qev[c] - qval) < 0.5]
            if not cols:
                continue
            sub = block @ qU[:, cols]
            Tblk = sub.conj().T @ (T @ sub)
            ev, U = np.linalg.eig(Tblk)
            for col in range(U.shape[1]):
                s = np.angle(ev[col]) / (2 * np.pi / N)
                out.append((float(vals[i]), float(s), qval, sub @ U[:, col]))
        i = j
    return out


def calibrate_v(raw_states, N):
    """Velocity from the lowest even-sector s=+2 state (the stress tensor, Delta_T=2
    exactly in any CFT). Model-independent: momentum labels need no velocity."""
    E0 = min(t[0] for t in raw_states)
    cands = [t for t in raw_states if t[2] == 1.0 and abs(t[1] - 2.0) < 0.1]
    if not cands:
        return None
    ET = min(t[0] for t in cands)
    return N * (ET - E0) / (4 * np.pi)


def with_dimensions(raw_states, N, v):
    E0 = min(t[0] for t in raw_states)
    return [(N * (E - E0) / (2 * np.pi * v), s, q, vec) for (E, s, q, vec) in raw_states]


def koo_saleur(N, raw_states, h, eps, v_exact=None, sig_delta=0.125, eps_delta=1.0):
    """Matrix-element route: c from <T|H_{-2}|0> -> sqrt(c/2) (Koo-Saleur / Milsted-Vidal).
    T is identified among even-sector s=+-2 states by MAXIMAL |<state|H_{+-2}|0>| (the
    state-operator correspondence: |T> = L_{-2}|0>; any accidental s=+-2 state, e.g. an
    aliased k~pi state, has a tiny element). Velocity: v_exact if given, else calibrated
    from the identified T-state via Delta_T = 2 (exact in any CFT).
    Chiral gate: wrong-chirality element / right-chirality element.
    C_sse pin from state ratios (lattice normalization cancels)."""
    E0 = min(t[0] for t in raw_states)
    vac = min(raw_states, key=lambda t: t[0])[3]
    e0 = E0 / N
    dim = h[0].shape[0]
    # raw (velocity-free) H_n modes without the (N/2 pi v) prefactor
    Hmode = {}
    for n in (2, -2):
        Hn = sp.csr_matrix((dim, dim), dtype=complex)
        for x in range(N):
            Hn = Hn + np.exp(1j * n * x * 2 * np.pi / N) * (h[x] - e0 * sp.identity(dim, format="csr"))
        Hmode[n] = Hn
    # T identification: LOWEST even-sector |s|=2 state. (Max-element ID was tried and
    # falsified: lattice band-edge states carry LARGER raw UV elements than T; the KS
    # suppression only applies to low CFT states. Verified on Ising: the Delta->3 L_{-2}eps
    # state has element ~2x T's.)
    cands = [t for t in raw_states if t[2] == 1.0 and abs(abs(t[1]) - 2.0) < 0.1]
    if not cands:
        return {"error": "no even-sector s=+-2 states retrieved (raise k)"}
    Tst = min(cands, key=lambda t: t[0])
    best_raw = max(abs(complex(np.vdot(Tst[3], Hmode[2] @ vac))),
                   abs(complex(np.vdot(Tst[3], Hmode[-2] @ vac))))
    best_bad = min(abs(complex(np.vdot(Tst[3], Hmode[2] @ vac))),
                   abs(complex(np.vdot(Tst[3], Hmode[-2] @ vac))))
    v_cal = N * (Tst[0] - E0) / (4 * np.pi)
    v = v_exact if v_exact is not None else v_cal
    res = {"v_cal": v_cal, "v_used": v}
    good = (N / (2 * np.pi * v)) * best_raw
    res["c_meas"] = 2 * good ** 2
    res["G4_wrong_chirality"] = best_bad / best_raw if best_raw > 0 else float("inf")
    res["C_TTT"] = 2 * np.sqrt(2) / np.sqrt(res["c_meas"])
    res["Delta_T"] = N * (Tst[0] - E0) / (2 * np.pi * v)
    res["s_T"] = Tst[1]
    # C_sse pin: <sigma|eps(0)|sigma> / <eps|eps(0)|0>
    states = with_dimensions(raw_states, N, v)
    def find(dl, sp_, q, tol):
        c = [t for t in states
             if abs(t[0] - dl) < tol and abs(t[1] - sp_) < 0.1 and t[2] == q]
        return min(c, key=lambda t: abs(t[0] - dl)) if c else None
    sig_st = find(sig_delta, 0.0, -1.0, tol=0.5 * sig_delta + 0.05)
    eps_st = find(eps_delta, 0.0, 1.0, tol=0.4 * eps_delta)
    if sig_st is not None and eps_st is not None:
        num = complex(np.vdot(sig_st[3], eps[0] @ sig_st[3]))
        den = complex(np.vdot(eps_st[3], eps[0] @ vac))
        res["C_sse_ME"] = abs(num) / abs(den)
    return res


def conn2(v0, A, B, meanA, meanB):
    return float(np.vdot(A @ v0, B @ v0).real) - meanA * meanB


def conn3(v0, A, B, C, mA, mB, mC, cAB, cAC, cBC):
    raw = float(np.vdot(A @ v0, B @ (C @ v0)).real)
    return raw - mA * cBC - mB * cAC - mC * cAB - mA * mB * mC


def analyze(N, verbose=True):
    H, h, eps, sig = build_ops(N)
    vals, vecs = spla.eigsh(H, k=1, which="SA")
    v0 = vecs[:, 0]
    E0 = float(vals[0])

    mh = float(np.vdot(v0, h[0] @ v0).real)
    meps = float(np.vdot(v0, eps[0] @ v0).real)
    msig = float(np.vdot(v0, sig[0] @ v0).real)  # 0 by Z2

    res = {"N": N, "E0": E0, "e_site": E0 / N, "mean_h": mh, "mean_eps": meps}

    # ---- 2-point functions vs separation ----
    hh, ee, ss = {}, {}, {}
    for x in range(2, N // 2 + 1):
        hh[x] = conn2(v0, h[0], h[x], mh, mh)
        ee[x] = conn2(v0, eps[0], eps[x], meps, meps)
        ss[x] = conn2(v0, sig[0], sig[x], msig, msig)

    # G2: log-log slopes vs chord distance (drop smallest separations)
    def slope(tab, xs):
        lx = np.log([np.sin(np.pi * x / N) * N / np.pi for x in xs])
        ly = np.log([abs(tab[x]) for x in xs])
        return float(np.polyfit(lx, ly, 1)[0])

    xs = [x for x in range(2, N // 2 + 1)]
    if len(xs) >= 3:
        res["slope_hh"] = slope(hh, xs)     # expect -4
        res["slope_ee"] = slope(ee, xs)     # expect -2
        res["slope_ss"] = slope(ss, xs)     # expect -0.25
    # amplitudes at max separation
    xm = N // 2
    A2h = hh[xm] / chord_kernel(xm, N) ** 4
    A2e = ee[xm] / chord_kernel(xm, N) ** 2
    A2s = ss[xm] / chord_kernel(xm, N) ** 0.25
    res["A2_h"], res["A2_eps"], res["A2_sig"] = A2h, A2e, A2s
    res["c_from_hh_slope_check"] = res.get("slope_hh")

    # ---- 3-point <hhh>: all well-separated triples (pairwise ring sep >= 3) ----
    trips = []
    for x in range(1, N):
        for y in range(x + 1, N):
            if ring_sep(0, x, N) >= 2 and ring_sep(x, y, N) >= 2 and ring_sep(0, y, N) >= 2:
                trips.append((0, x, y))
    a3_vals = []
    for (i, j, k) in trips:
        cij = conn2(v0, h[i], h[j], mh, mh)
        cik = conn2(v0, h[i], h[k], mh, mh)
        cjk = conn2(v0, h[j], h[k], mh, mh)
        c3 = conn3(v0, h[i], h[j], h[k], mh, mh, mh, cij, cik, cjk)
        kin = (chord_kernel(ring_sep(i, j, N), N) ** 2
               * chord_kernel(ring_sep(j, k, N), N) ** 2
               * chord_kernel(ring_sep(i, k, N), N) ** 2)
        d = min(ring_sep(i, j, N), ring_sep(j, k, N), ring_sep(i, k, N))
        a3_vals.append((d, (i, j, k), c3 / kin))
    res["A3_h_by_minsep"] = {}
    for d in sorted(set(t[0] for t in a3_vals)):
        vals_d = [t[2] for t in a3_vals if t[0] == d]
        res["A3_h_by_minsep"][d] = (float(np.mean(vals_d)), float(np.std(vals_d)), len(vals_d))
    # use the most-separated class for the headline number
    dbest = max(res["A3_h_by_minsep"].keys())
    A3h = res["A3_h_by_minsep"][dbest][0]
    res["A3_h"] = A3h
    res["C_TTT"] = float(np.sqrt(2) * A3h / abs(A2h) ** 1.5) * np.sign(A2h)
    res["c_meas"] = float((2 * abs(A2h) ** 1.5 / abs(A3h)) ** 2)

    # ---- G3 pin: C_sse from <sig sig eps> ----
    Ds, De = 0.125, 1.0
    e_ss, e_se = 2 * Ds - De, De  # exponents: s1s2 leg, each s-e leg
    pin_vals = []
    for x in range(2, N - 3):
        for y in range(x + 2, N - 1):
            if ring_sep(0, x, N) >= 2 and ring_sep(x, y, N) >= 2 and ring_sep(0, y, N) >= 2:
                cij = conn2(v0, sig[0], sig[x], msig, msig)
                cik = conn2(v0, sig[0], eps[y], msig, meps)
                cjk = conn2(v0, sig[x], eps[y], msig, meps)
                c3 = conn3(v0, sig[0], sig[x], eps[y], msig, msig, meps, cij, cik, cjk)
                kin = (chord_kernel(ring_sep(0, x, N), N) ** e_ss
                       * chord_kernel(ring_sep(x, y, N), N) ** e_se
                       * chord_kernel(ring_sep(0, y, N), N) ** e_se)
                d = min(ring_sep(0, x, N), ring_sep(x, y, N), ring_sep(0, y, N))
                pin_vals.append((d, c3 / kin))
    dbest_p = max(t[0] for t in pin_vals)
    A3p = float(np.mean([t[1] for t in pin_vals if t[0] == dbest_p]))
    res["C_sse"] = A3p / (abs(A2s) * abs(A2e) ** 0.5) * np.sign(A2s) * np.sign(A2e)

    if verbose:
        print(f"== N={N}  E0/N={E0/N:+.6f}  (exact -4/pi = {-4/np.pi:+.6f})")
        print(f"   slopes: hh {res.get('slope_hh', float('nan')):+.3f} (want -4)   "
              f"ee {res.get('slope_ee', float('nan')):+.3f} (want -2)   "
              f"ss {res.get('slope_ss', float('nan')):+.3f} (want -0.25)")
        print(f"   A2_h={A2h:+.6e}  A3_h={A3h:+.6e} (minsep {dbest})")
        print(f"   C_sse = {res['C_sse']:+.4f}   (target 0.5000)")
        print(f"   C_TTT = {res['C_TTT']:+.4f}   c_meas = {res['c_meas']:.4f}   (targets 4.000 / 0.500)")
    return res


def main():
    args = [a for a in sys.argv[1:]]
    model = "ising"
    lam3 = 0.856
    if "--model" in args:
        i = args.index("--model")
        model = args[i + 1]
        del args[i:i + 2]
    use_vcal = "--vcal" in args
    if use_vcal:
        args.remove("--vcal")
    Ns = [int(a) for a in args] or [8, 10, 12, 14, 16]
    # model-specific: exact velocity (None = must self-calibrate), sigma/eps target dims
    if model == "ising":
        v_exact, sig_d, eps_d, c_tgt = 2.0, 0.125, 1.0, 0.5
    elif model == "of":
        v_exact, sig_d, eps_d, c_tgt = None, 0.075, 0.2, 0.7
    else:
        raise SystemExit(f"unknown model {model}")
    print(f"model={model}" + (f" lam3={lam3}" if model == "of" else "")
          + f"  v={'self-calibrated' if (use_vcal or v_exact is None) else v_exact}"
          + f"  c target={c_tgt}, C_TTT target={2*np.sqrt(2)/np.sqrt(c_tgt):.4f}")
    allres = []
    for N in Ns:
        if model == "ising":
            H, h, eps, sig = build_ops(N)
            kk = 24
        else:
            H, h, eps, sig = build_ops_of(N, lam3)
            kk = 48
        raw = momentum_states(H, N, k=kk)
        E0 = min(t[0] for t in raw)
        ks = koo_saleur(N, raw, h, eps,
                        v_exact=None if use_vcal else v_exact,
                        sig_delta=sig_d, eps_delta=eps_d)
        if "error" in ks:
            print(f"== N={N}: {ks['error']}")
            continue
        v_use, v_cal = ks["v_used"], ks["v_cal"]
        states = with_dimensions(raw, N, v_use)
        low = sorted((d, s, q) for d, s, q, _ in states)[:10]
        r = {"N": N, "E0": E0, "spectrum": low, "v_used": v_use}
        for key in ("c_meas", "C_TTT", "G4_wrong_chirality", "C_sse_ME", "Delta_T", "s_T", "v_cal"):
            if key in ks:
                r[key] = ks[key]
        print(f"== N={N}  (v_used={v_use:.4f}, v_cal={v_cal if v_cal else float('nan'):.4f})")
        print("   G1 (Delta, s, q):", ", ".join(f"({d:.3f},{s:+.2f},{q:+.0f})" for d, s, q in low))
        if "c_meas" in r:
            print(f"   c_meas = {r['c_meas']:.5f} (target 0.5)   "
                  f"C_TTT = {r['C_TTT']:.4f} (target 4.000)   "
                  f"G4 wrong-chirality = {r['G4_wrong_chirality']:.4f}")
        if "C_sse_ME" in r:
            print(f"   C_sse (matrix-element) = {r['C_sse_ME']:.4f} (target 0.5)")
        allres.append(r)
        sys.stdout.flush()
    if len(allres) >= 3 and all("c_meas" in r for r in allres):
        Ns_a = np.array([r["N"] for r in allres], float)
        for key, tgt in (("c_meas", c_tgt), ("C_TTT", 2 * np.sqrt(2) / np.sqrt(c_tgt)),
                         ("C_sse_ME", None)):
            ys = np.array([r[key] for r in allres if key in r])
            if len(ys) == len(Ns_a):
                coef = np.polyfit(1.0 / Ns_a ** 2, ys, 1)
                lbl = f"(target {tgt:.4f})" if tgt is not None else ""
                print(f"\n== extrapolation: {key}(N->inf) = {coef[1]:+.5f}  {lbl}")
    with open(f"qw_cttt_circle_results_{model}.json", "w") as f:
        json.dump(allres, f, indent=1, default=str)


if __name__ == "__main__":
    main()
