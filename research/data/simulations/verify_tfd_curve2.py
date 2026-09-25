"""
Part 3: clean transport-time extraction T(beta) at L=8 using the
Wang-He-style protocol (localized Gaussian Y-kick across the ring, observable
= max boundary response envelope) on the thermal mixed state, to confirm a
RESOLVABLE non-flat T(beta) curve. dt=0.02 fine grid.
"""
import numpy as np
import scipy.linalg as sla

I2 = np.eye(2, dtype=complex)
X = np.array([[0,1],[1,0]], dtype=complex)
Y = np.array([[0,-1j],[1j,0]], dtype=complex)
Z = np.array([[1,0],[0,-1]], dtype=complex)

def pauli_full(n,i,P):
    mats=[P if k==i else I2 for k in range(n)]
    o=mats[0]
    for m in mats[1:]: o=np.kron(o,m)
    return o

def build_H(L):
    dim=2**L; H=np.zeros((dim,dim),dtype=complex); pref=L/(4*np.pi)
    Xs=[pauli_full(L,i,X) for i in range(L)]; Zs=[pauli_full(L,i,Z) for i in range(L)]
    for j in range(L):
        H+=pref*(Xs[(j-1)%L]@Zs[j]@Xs[(j+1)%L]-Xs[j]@Xs[(j+1)%L])
    return H

L=8
H=build_H(L); evals,evecs=np.linalg.eigh(H)
Ys=[pauli_full(L,i,Y) for i in range(L)]
# Gaussian Y-kick localized near phi=-3pi/4 site, as in HYP-006 protocol
phi=np.array([2*np.pi*i/L - 3*np.pi/4 for i in range(L)])
sig_phi=0.4
amp=np.exp(-phi**2/(2*sig_phi**2)); amp/=amp.max()
eps=0.4
Kgen=sum(eps*amp[i]*Ys[i] for i in range(L))
Uk=sla.expm(-1j*Kgen)

ts=np.arange(0,6.001,0.02)
Yo=[evecs.conj().T@Ys[i]@evecs for i in range(L)]  # in energy basis

def envelope(rho0):
    rho_e=evecs.conj().T@rho0@evecs
    env=np.zeros(len(ts))
    for k,t in enumerate(ts):
        ph=np.exp(-1j*evals*t)
        rt=(ph[:,None]*rho_e)*np.conj(ph)[None,:]
        mx=0.0
        for i in range(L):
            v=abs(np.real(np.sum(rt*Yo[i].T)))
            if v>mx: mx=v
        env[k]=mx
    return env

def extract_T(env):
    pk=np.argmax(env[:int(2.0/0.02)])   # first peak in t<2
    seg=env[pk:pk+int(3.0/0.02)]
    dip=pk+np.argmin(seg)
    post=env[dip+int(0.3/0.02):]
    rep=dip+int(0.3/0.02)+np.argmax(post)
    return ts[dip], ts[rep], ts[rep]-ts[dip], env.max()

print(f"L={L}  clean Wang-He-style transport, dt=0.02")
print(f"{'beta':>7} {'T(beta)':>9} {'dip_t':>7} {'reapp':>7} {'env_max':>9} {'N_eff':>8}")
betas=[100,20,8,5,3,2,1,0.5]
Tvals=[]
for beta in betas:
    rho=evecs@np.diag(np.exp(-beta*(evals-evals[0])))@evecs.conj().T
    rho/=np.trace(rho).real
    base=envelope(rho)
    rho_k=Uk@rho@Uk.conj().T
    env=envelope(rho_k)-base
    env=np.abs(env)
    dip,rep,T,mx=extract_T(env)
    w=np.exp(-beta*(evals-evals[0])); Neff=(w.sum())**2/(w**2).sum()
    Tvals.append(T)
    print(f"{beta:7.2f} {T:9.3f} {dip:7.2f} {rep:7.2f} {mx:9.5f} {Neff:8.3f}")

Tvals=np.array(Tvals)
print(f"\nT range: {Tvals.min():.3f} to {Tvals.max():.3f}, spread={Tvals.max()-Tvals.min():.3f}")
print(f"Monotonic decrease cold->hot? T(100)={Tvals[0]:.3f} vs T(0.5)={Tvals[-1]:.3f}")
print(f"Cold-limit self-consistency: T(beta=100)={Tvals[0]:.3f} (HYP-006 target=2.250)")
