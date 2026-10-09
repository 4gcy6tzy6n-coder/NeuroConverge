"""Technical covariates against the per-animal effect.

Round 15 left about 40 per cent of the between-animal variance in the effect unexplained.  If a technical
property of the recording explains it, that portion is technical rather than biological.  Every covariate
here is read from the per-animal files the atlas exported, so none requires new data.

Covariates: recording duration, event count, identified-cell count, median GCaMP level, GCaMP variability,
NaN fraction, and the fraction of identified cells that are in the connectome.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, math
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
def build(fn):
    C=np.zeros((N,N)); G=np.zeros((N,N))
    with open(WNA/fn, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            p,q=r["pre"],r["post"]
            if p not in idx or q not in idx: continue
            s=float(r["synapses"]); i,j=idx[p],idx[q]
            if r["type"]=="chemical": C[i,j]+=s
            elif r["type"]=="electrical": G[i,j]+=s; G[j,i]+=s
    return C,G
c1,g1=build("aconnectome_witvliet_2020_8.csv"); c2,g2=build("aconnectome_white_1986_whole.csv")
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool); conn=((chem!=0)|(gap!=0))&off
SHIFT=60
rows=[]
for i in sorted({int(m.group(1)) for p in DATA.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))}):
    gp,lp,sp,vp=(DATA/f"{i}_gcamp.txt",DATA/f"{i}_labels.txt",DATA/f"{i}_stim_neurons.txt",DATA/f"{i}_stim_volume_i.txt")
    if not all(p.exists() for p in (gp,lp,sp,vp)): continue
    try: G=np.loadtxt(gp)
    except Exception: continue
    lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
    stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
    T,ncol=G.shape
    if len(stim)!=len(vols) or T<200: continue
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
    uniq={n for n,c in cnt.items() if c==1}
    keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
    if not keep: continue
    co=[]; un=[]; nev=0
    with np.errstate(all='ignore'):
        for k,(sv,vi) in enumerate(zip(stim,vols)):
            if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            inter=(vols[k+1]-vi) if k+1<len(vols) else 62
            mv=max(12, min(int((inter*0.5-5)/0.5), 60))
            end=min(T, vi+mv)
            if end-vi<12: continue
            nev+=1
            raw=G[vi-SHIFT:end,:]
            base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
            seg=raw-base
            sm=np.nansum(seg[SHIFT:, keep], axis=0)
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                (co if conn[i_,j_] else un).append(float(sm[kk]))
    if len(co)<10 or len(un)<50 or nev<8: continue
    allv=np.array(co+un); mu=allv.mean(); sd=allv.std()
    if not np.isfinite(sd) or sd<=0: continue
    eff=float(np.mean((np.array(co)-mu)/sd) - np.mean((np.array(un)-mu)/sd))
    with np.errstate(all='ignore'):
        nan_frac=float(np.mean(~np.isfinite(G)))
        med=float(np.nanmedian(G)); iqr=float(np.nanpercentile(G,75)-np.nanpercentile(G,25))
        inconn=float(np.mean([1.0 if (lab[c] in idx) else 0.0 for c in keep]))
    rows.append(dict(animal=int(i), effect=eff, n_events=nev, n_cells=len(keep),
                     duration=float(T), nan_frac=nan_frac, gcamp_med=med, gcamp_iqr=iqr,
                     frac_in_connectome=inconn, n_conn=len(co), n_unconn=len(un)))
print(f"  进入分析的动物: {len(rows)}")
E=np.array([r["effect"] for r in rows])
print(f"  效应: 均值 {E.mean():+.4f}  SD {E.std(ddof=1):.4f}")
COVS=["n_events","n_cells","duration","nan_frac","gcamp_med","gcamp_iqr","frac_in_connectome",
      "n_conn","n_unconn"]
print(f"\n  === 协变量与效应的相关 ===")
print(f"  {'covariate':>20} {'median':>12} {'corr':>9} {'r2':>7} {'p (approx)':>11}")
out={"n_animals":len(rows),"effect_mean":float(E.mean()),"effect_sd":float(E.std(ddof=1)),"covs":{}}
def tp(t,df):
    # two-sided p for Student t via a series-free approximation using the incomplete beta
    from math import lgamma, log, exp
    x=df/(df+t*t)
    def betacf(a,b,x):
        MAXIT=200; EPS=3e-16; FPMIN=1e-300
        qab=a+b; qap=a+1; qam=a-1; c=1.0; d_=1-qab*x/qap
        if abs(d_)<FPMIN: d_=FPMIN
        d_=1/d_; h=d_
        for m in range(1,MAXIT+1):
            m2=2*m
            aa=m*(b-m)*x/((qam+m2)*(a+m2)); d_=1+aa*d_
            if abs(d_)<FPMIN: d_=FPMIN
            c=1+aa/c
            if abs(c)<FPMIN: c=FPMIN
            d_=1/d_; h*=d_*c
            aa=-(a+m)*(qab+m)*x/((a+m2)*(qap+m2)); d_=1+aa*d_
            if abs(d_)<FPMIN: d_=FPMIN
            c=1+aa/c
            if abs(c)<FPMIN: c=FPMIN
            d_=1/d_; de=d_*c; h*=de
            if abs(de-1)<EPS: break
        return h
    def betai(a,b,x):
        if x<=0: return 0.0
        if x>=1: return 1.0
        bt=exp(lgamma(a+b)-lgamma(a)-lgamma(b)+a*log(x)+b*log(1-x))
        return bt*betacf(a,b,x)/a if x<(a+1)/(a+b+2) else 1-bt*betacf(b,a,1-x)/b
    return betai(df/2,0.5,x)
for c in COVS:
    X=np.array([r[c] for r in rows],float)
    if not np.isfinite(X).all() or X.std()==0:
        print(f"  {c:>20} {'-':>12} {'-':>9} {'-':>7} {'-':>11}"); continue
    r=np.corrcoef(X,E)[0,1]; n=len(E); t=r*math.sqrt((n-2)/max(1e-12,1-r*r)); p=tp(t,n-2)
    out["covs"][c]={"median":float(np.median(X)),"corr":float(r),"r2":float(r*r),"p":float(p)}
    print(f"  {c:>20} {np.median(X):>12.4g} {r:>+9.4f} {r*r:>7.4f} {p:>11.3g}")
# multiple regression on the standardised covariates, to see total explained
Xm=np.column_stack([np.array([r[c] for r in rows],float) for c in COVS])
good=np.isfinite(Xm).all(axis=1)&np.isfinite(E)
Xs=(Xm[good]-Xm[good].mean(0))/np.where(Xm[good].std(0)==0,1,Xm[good].std(0))
y=(E[good]-E[good].mean())/E[good].std()
Xd=np.column_stack([np.ones(len(y)),Xs])
beta,res,rank,sv=np.linalg.lstsq(Xd,y,rcond=None)
pred=Xd@beta; ss_res=((y-pred)**2).sum(); ss_tot=((y-y.mean())**2).sum()
R2=1-ss_res/ss_tot
print(f"\n  === 全部技术协变量的多元回归 ===")
print(f"    动物数 {int(good.sum())}   调整前 R^2 = {R2:.4f}")
k=Xd.shape[1]-1; n=int(good.sum())
R2adj=1-(1-R2)*(n-1)/(n-k-1)
print(f"    自由度校正后 R^2 = {R2adj:.4f}   (k={k})")
out["multi_R2"]=float(R2); out["multi_R2_adj"]=float(R2adj); out["n_multi"]=n
print(f"\n  === 判读 ===")
print(f"    若技术协变量能解释大部分效应方差 ⟹ 未解释部分是技术性的")
print(f"    若 R^2 校正后接近 0        ⟹ 技术协变量不解释效应，生物学解释仍然活着")
json.dump(out, open("/tmp/osf/covariates.json","w"), indent=2)
