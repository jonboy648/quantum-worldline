"""
Final VQE run — lean, saves incrementally, runs L-BFGS-B then COBYLA polish.
Designed to complete within 8 minutes.
"""
import numpy as np, json, time, sys
from copy import deepcopy
from scipy.optimize import minimize
from scipy.sparse import lil_matrix
from scipy.sparse.linalg import eigsh
from qiskit import QuantumCircuit
from qiskit.circuit import ParameterVector
from qiskit.quantum_info import SparsePauliOp, Statevector

N, J, h = 16, 1.0, 1.0
L_ADS   = 1.0 / np.log(2)
C1_P, C2_P = 0.080, 13.6
ANGLE   = np.pi / 3
DRHO    = list(range(1, 9))
OUT     = "D:/quantum-worldline/research/data/simulations/SIM-2026-002.json"
NP_OUT  = "D:/quantum-worldline/research/data/simulations/theta_opt_SIM2026002.npy"

# --- Hamiltonian ---
def build_H_op():
    terms, coefs = [], []
    for i in range(N-1):
        s = ['I']*N; s[i]='Z'; s[i+1]='Z'
        terms.append(''.join(reversed(s))); coefs.append(-J)
    for i in range(N):
        s = ['I']*N; s[i]='X'
        terms.append(''.join(reversed(s))); coefs.append(-h)
    return SparsePauliOp(terms, coeffs=coefs)

HAM = build_H_op()

# --- Exact E0 (sparse) ---
def exact_e0():
    dim = 2**N
    H = lil_matrix((dim,dim), dtype=np.float64)
    for i in range(N-1):
        for s in range(dim):
            si=(s>>i)&1; sj=(s>>(i+1))&1
            H[s,s] += -J*(1 if si==sj else -1)
    for i in range(N):
        for s in range(dim): H[s, s^(1<<i)] += -h
    v,_ = eigsh(H.tocsr(), k=1, which='SA')
    return float(v[0])

# --- Circuit: NO Hadamard, starts from |0>^N ---
def add_dis(qc,q0,q1,p,o):
    qc.ry(p[o],q0); qc.rz(p[o+1],q0)
    qc.ry(p[o+2],q1); qc.rz(p[o+3],q1)
    qc.cx(q0,q1)
    qc.ry(p[o+4],q0); qc.ry(p[o+5],q1)
    return o+6

def add_iso(qc,q0,q1,p,o):
    qc.ry(p[o],q0); qc.ry(p[o+1],q1)
    qc.cx(q0,q1)
    qc.ry(p[o+2],q0); qc.rz(p[o+3],q1)
    return o+4

def n_params():
    t=0
    for l in range(3):
        np2 = N//(2**l)//2
        t += np2*6 + np2*4
    return t+6

NP = n_params()

def build_qc(theta, hadamard=False):
    pv = ParameterVector('t', NP)
    qc = QuantumCircuit(N)
    if hadamard:
        for i in range(N): qc.h(i)
    o = 0; aq = list(range(N))
    for l in range(3):
        na = len(aq)
        if na < 2: break
        for k in range(0, na-1, 2): o = add_dis(qc, aq[k], aq[k+1], pv, o)
        naq = []
        for k in range(0, na-1, 2):
            o = add_iso(qc, aq[k], aq[k+1], pv, o)
            naq.append(aq[k])
        if na%2: naq.append(aq[-1])
        aq = naq
    if len(aq)>=2 and o+6<=NP:
        o = add_dis(qc, aq[0], aq[1], pv, o)
    bd = {pv[i]: float(theta[i]) for i in range(NP)}
    return qc.assign_parameters(bd)

# --- Energy ---
eh = []; ec = [0]; t0_g = [time.time()]

def energy(theta, hd=False):
    qc = build_qc(theta, hd)
    E = float(Statevector(qc).expectation_value(HAM).real)
    eh.append(E); ec[0]+=1
    if ec[0]%50==0:
        print(f"  eval {ec[0]:4d}  E={E:+.5f}  t={time.time()-t0_g[0]:.0f}s", flush=True)
    return E

# --- Initial params ---
def init_theta(seed=7, hd=False):
    rng = np.random.default_rng(seed)
    th  = np.zeros(NP); idx=0
    for l in range(3):
        np2 = N//(2**l)//2
        base_d = np.array([np.pi/2,np.pi/4]*3) if not hd else np.array([np.pi/4,np.pi/2,np.pi/4,np.pi/2,np.pi/4,np.pi/4])
        base_i = np.array([np.pi/3,np.pi/4,np.pi/3,np.pi/4])
        for _ in range(np2):
            th[idx:idx+6]=base_d+rng.normal(0,0.12,6); idx+=6
        for _ in range(np2):
            th[idx:idx+4]=base_i+rng.normal(0,0.12,4); idx+=4
    base_t = np.array([np.pi/2,np.pi/4,np.pi/2,np.pi/4,np.pi/3,np.pi/4])
    th[idx:idx+6]=base_t+rng.normal(0,0.12,6)
    return th

# --- Correlator ---
def corr(qc_bound, i, j):
    sv = Statevector(qc_bound)
    def op(sites):
        s=['I']*N
        for x in sites: s[x]='Z'
        return SparsePauliOp(''.join(reversed(s)))
    zi = sv.expectation_value(op([i])).real
    zj = sv.expectation_value(op([j])).real
    zij= sv.expectation_value(op([i,j])).real
    return float(zij - zi*zj)

def force_sweep(theta, hd=False):
    vac = build_qc(theta, hd)
    anchor = N//4
    seps, Vs, Cvs, Cts = [], [], [], []
    for dr in DRHO:
        js = anchor+dr
        if js>=N: continue
        cv = corr(vac, anchor, js)
        tw = deepcopy(vac); tw.ry(ANGLE,anchor); tw.ry(ANGLE,js)
        ct = corr(tw, anchor, js)
        V = ct-cv
        seps.append(dr); Vs.append(float(V)); Cvs.append(float(cv)); Cts.append(float(ct))
        print(f"  dr={dr}: V={V:+.6f}  C_vac={cv:.5f}  C_two={ct:.5f}", flush=True)
    return seps, Vs, Cvs, Cts

def fit_V(seps, Vs):
    from scipy.optimize import curve_fit
    def m(x,C1,C2,xi): return C1-C2*np.exp(-np.array(x,float)/xi)
    try:
        po,pc = curve_fit(m, seps, Vs, p0=[C1_P,C2_P,L_ADS],
                          bounds=([-5,-200,.1],[5,200,10]), maxfev=10000)
        pe = np.sqrt(np.diag(pc))
        return {"success":True,"C1":float(po[0]),"C2":float(po[1]),"xi":float(po[2]),
                "C1_err":float(pe[0]),"C2_err":float(pe[1]),"xi_err":float(pe[2])}
    except Exception as e:
        return {"success":False,"C1":None,"C2":None,"xi":None,"error":str(e)}

# ======================== MAIN ================================================
print("="*60)
print("Final VQE — SIM-2026-002")
print("="*60)
T = time.time()

print("\n[1] Exact E0 ...", flush=True)
t0=time.time(); E0=exact_e0(); print(f"  E0={E0:.6f}  [{time.time()-t0:.1f}s]", flush=True)

# Try multiple random seeds; keep best
best_E   = 0.0
best_th  = None
best_hd  = False
all_hist = []

# Multi-start L-BFGS-B
for seed in [7, 13, 42, 99]:
    for hd_flag in [False]:
        print(f"\n[2] L-BFGS-B seed={seed} hd={hd_flag}...", flush=True)
        th0 = init_theta(seed, hd_flag)
        E0i = energy(th0, hd_flag)
        print(f"  E_init={E0i:.4f}", flush=True)
        t0_g[0] = time.time()
        res = minimize(lambda p: energy(p, hd_flag), th0, method='L-BFGS-B',
                       jac='2-point',
                       options={'maxiter':300,'ftol':1e-8,'gtol':1e-5,'eps':0.015})
        Ef = res.fun
        print(f"  E_final={Ef:.4f}  evals={ec[0]}", flush=True)
        if Ef < best_E:
            best_E = Ef; best_th = res.x.copy(); best_hd = hd_flag
        all_hist += eh[:]
        eh.clear(); ec[0]=0

print(f"\n  Best after multi-start: E={best_E:.6f}", flush=True)

# COBYLA polish on best
print("\n[3] COBYLA polish ...", flush=True)
t0_g[0]=time.time()
res2 = minimize(lambda p: energy(p, best_hd), best_th, method='COBYLA',
                options={'maxiter':500,'rhobeg':0.08,'catol':1e-6})
Ef2 = res2.fun
print(f"  COBYLA polish: E={Ef2:.6f}  evals={ec[0]}", flush=True)
all_hist += eh[:]
eh.clear(); ec[0]=0

theta_final = res2.x
E_opt = min(best_E, Ef2)
if Ef2 < best_E:
    theta_final = res2.x; best_hd_final = best_hd
else:
    theta_final = best_th; best_hd_final = best_hd

pct = abs(E_opt-E0)/abs(E0)*100
conv = bool(pct < 1.0)
print(f"\n  E_opt={E_opt:.6f}  error={pct:.2f}%  converged={conv}", flush=True)

np.save(NP_OUT, theta_final)

# Force profile
print("\n[4] Force profile ...", flush=True)
seps, Vs, Cvs, Cts = force_sweep(theta_final, best_hd_final)
V_anal = [float(C1_P - C2_P*np.exp(-dr/L_ADS)) for dr in seps]
fit = fit_V(seps, Vs)
print(f"  Fit: C1={fit['C1']} C2={fit['C2']} xi={fit['xi']}", flush=True)

# Save
T_tot = time.time()-T
structured = {
    "id":"SIM-2026-002",
    "description": (
        "VQE optimization of 16-qubit binary MERA (3 layers, 146 params) "
        "to critical Ising ground state (J=h=1, OBC). Multi-start L-BFGS-B "
        "followed by COBYLA polish. Force profile measured with Ry hologrons."
    ),
    "type":"vqe_optimization","date":"2026-03-10",
    "hypothesis_id":"HYP-2026-002","paper_ref":"PAPER-2026-003",
    "circuit":{
        "qubits":int(N),"layers":3,"n_params":int(NP),
        "architecture":"binary_MERA_disentanglers_isometries",
        "hologron_gate":"Ry","hologron_angle_rad":float(ANGLE),
        "initial_state":"computational_zero_multistart",
    },
    "vqe":{
        "optimizers":["L-BFGS-B_multistart","COBYLA_polish"],
        "n_total_evals":int(len(all_hist)+len(eh)),
        "E_optimized":float(E_opt),"E0_exact":float(E0),
        "pct_error":float(round(pct,4)),"converged_1pct":conv,
        "energy_history":[float(x) for x in all_hist],
        "theta_optimized":[float(x) for x in theta_final.tolist()],
        "elapsed_seconds":float(round(T_tot,2)),
    },
    "force_profile":{
        "delta_rho":[int(x) for x in seps],
        "V_quantum":[float(x) for x in Vs],
        "V_analytical":[float(x) for x in V_anal],
        "C_vac":[float(x) for x in Cvs],
        "C_two":[float(x) for x in Cts],
        "anchor_site":int(N//4),
    },
    "fit":{k:(float(v) if isinstance(v,(int,float,np.floating))
               else bool(v) if isinstance(v,(bool,np.bool_))
               else v)
           for k,v in fit.items()},
    "comparison":{
        "paper_C1":float(C1_P),"paper_C2":float(C2_P),"paper_l_AdS":float(L_ADS),
        "fitted_C1":float(fit["C1"]) if fit.get("C1") is not None else None,
        "fitted_C2":float(fit["C2"]) if fit.get("C2") is not None else None,
        "fitted_xi":float(fit["xi"]) if fit.get("xi") is not None else None,
    },
    "hardware_target":"simulator_qiskit_aer_statevector",
    "total_elapsed_seconds":float(round(T_tot,2)),
}

with open(OUT,'w') as f: json.dump(structured, f, indent=2)
print(f"\nSaved: {OUT}")
print(f"Saved theta_opt: {NP_OUT}")
print(f"Total time: {T_tot:.0f}s")
print("="*60)
