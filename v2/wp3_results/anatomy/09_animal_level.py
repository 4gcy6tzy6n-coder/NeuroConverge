import numpy as np, h5py, csv, pathlib, re, collections, json
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
POST=24; SHIFT=60
# per ANIMAL: mean response of connected and of unconnected pairs, common-mode corrected
per_animal={}
for i in sorted({int(m.group(1)) for p in DATA.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))}):
    gp,lp,sp,vp=(DATA/f"{i}_gcamp.txt",DATA/f"{i}_labels.txt",DATA/f"{i}_stim_neurons.txt",DATA/f"{i}_stim_volume_i.txt")
    if not all(p.exists() for p in (gp,lp,sp,vp)): continue
    try: G=np.loadtxt(gp)
    except Exception: continue
    lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
    stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
    T,ncol=G.shape
    if len(stim)!=len(vols): continue
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
    uniq={n for n,c in cnt.items() if c==1}
    keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
    if not keep: continue
    cc=[]; cu=[]; cch=[]; cg=[]
    with np.errstate(all='ignore'):
        for sv,vi in zip(stim,vols):
            if sv<0 or vi<SHIFT or vi+POST>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            post=G[vi:vi+POST,:]; base=G[vi-30:vi,:]
            b=np.nanmean(base,axis=0); dv=post-b
            sd=np.nanmedian(np.nanstd(dv,axis=1))
            if not np.isfinite(sd) or sd<=0: continue
            dvs=dv/sd; cm=np.nanmean(dvs,axis=1,keepdims=True); dev=dvs-cm
            for c in keep:
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                v=float(dev[:,c].mean())
                if not np.isfinite(v): continue
                if conn[i_,j_]:
                    cc.append(v)
                    if chem[i_,j_]!=0: cch.append(v)
                    if gap[i_,j_]!=0:  cg.append(v)
                else: cu.append(v)
    if cc and cu:
        per_animal[i]={"conn":float(np.mean(cc)),"unconn":float(np.mean(cu)),
                       "n_conn":len(cc),"n_unconn":len(cu),
                       "chem":float(np.mean(cch)) if cch else None,"gap":float(np.mean(cg)) if cg else None}
print(f"  有可用对照的动物数: {len(per_animal)}")
d=np.array([v["conn"]-v["unconn"] for v in per_animal.values()])
n=d.size; mean=d.mean(); sd=d.std(ddof=1)
se=sd/np.sqrt(n); t=mean/se
from math import lgamma, log, exp
def tp(t_,df):
    x=df/(df+t_*t_); 
    # regularized incomplete beta via continued fraction (Numerical Recipes betacf)
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
        if x<(a+1)/(a+b+2): return bt*betacf(a,b,x)/a
        return 1-bt*betacf(b,a,1-x)/b
    return betai(df/2,0.5,x)
p=tp(t,n-1)
print(f"\n  === 动物级配对对比（单位 = 动物, n={n}）===")
print(f"    连接均值   {np.mean([v['conn'] for v in per_animal.values()]):+.5f}")
print(f"    未连接均值 {np.mean([v['unconn'] for v in per_animal.values()]):+.5f}")
print(f"    配对差 {mean:+.5f}   跨动物 SD {sd:.5f}   SE {se:.5f}")
print(f"    t = {t:.3f}  df = {n-1}  p = {p:.4g}")
print(f"    标准化效应 d = {mean/sd:.4f}   （配对设计，这正是第 1 轮那张功效表的 d）")
print()
# same for chem and gap strata, animal-level
for key,lab_ in (("chem","化学"),("gap","缝隙")):
    vals=[(v[key], v["unconn"]) for v in per_animal.values() if v[key] is not None]
    if len(vals)<20: continue
    dd=np.array([a-b for a,b in vals]); nn=dd.size; mm=dd.mean(); ss=dd.std(ddof=1)
    tt=mm/(ss/np.sqrt(nn)); pp=tp(tt,nn-1)
    print(f"  {lab_}: n={nn}  差 {mm:+.5f}  d={mm/ss:.4f}  t={tt:.3f}  p={pp:.4g}")
out={"n_animals":n,"paired_diff":float(mean),"sd":float(sd),"t":float(t),"p":float(p),
     "cohens_d_paired":float(mean/sd),"per_animal":per_animal}
json.dump(out, open("/tmp/osf/animallevel.json","w"), indent=2)
