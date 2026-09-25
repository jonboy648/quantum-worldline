import numpy as np, qw_tlee_level1 as q, json, time
t0=time.time(); L=1024; out={}
for R_H in (25.0, 50.0):
    R=q.V*R_H; T0s=list(range(2,int(R)-1)); win=[t for t in T0s if 3<=t<=R/2]
    for delta in (1.0, 2.0, 5.0, 10.0, 20.0, 50.0):
        S=q.route_G(L,R_H,T0s,delta=delta)
        re=[S[t]["S_mode_branch"].real for t in win]; im=np.array([S[t]["S_mode_branch"].imag for t in win])
        sl,_=q.fit_slope(R,win,re)
        small=[t for t in win if t<=R/8]; ims=np.array([S[t]["S_mode_branch"].imag for t in small])
        out[f"R{R}_d{delta}"]={"slope":sl,"Im_mean_win":float(im.mean()),"Im_std_win":float(im.std()),"Im_mean_small":float(ims.mean()),"Im_std_small":float(ims.std()),
                               "Im_by_T0":{t:S[t]["S_mode_branch"].imag for t in T0s},"Re_by_T0":{t:S[t]["S_mode_branch"].real for t in T0s}}
        print(f"R={R:5.0f} delta={delta:4.0f}: slope {sl:+.4f} (1/6)  Im window {im.mean():+.4f}+/-{im.std():.4f}  Im small-T0 {ims.mean():+.4f}+/-{ims.std():.4f}  (pi/12={np.pi/12:.4f})", flush=True)
json.dump(out,open('tlee_delta_scan_L1024.json','w'),indent=1,default=float); print('%.0fs'%(time.time()-t0))
