"""Per-animal connectivity-function effect, its distribution, and meta-analytic heterogeneity.

Round 9 established that a pair's response agrees across animals at r_full = 0.04 while agreeing within an
animal at r_full = 0.52.  If that is right, then the population-average association (d ~ 0.45) may describe
no individual animal.  This script computes the effect PER ANIMAL and asks whether one common effect is
adequate, using Cochran's Q and I^2 -- the standard heterogeneity statistics, which is exactly the question.

Also reports the within-animal standardised effect, which unlike the cross-animal one is not attenuated by
between-animal variance.
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
# per animal: the values of connected and unconnected pairs, pooled over that animal's events
byA=collections.defaultdict(lambda: {"conn":[], "unconn":[]})
n_an=0; n_ev=0
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
    n_an+=1
    # z-scored WITHIN the animal, so the contrast is not driven by that animal's absolute scale
    with np.errstate(all='ignore'):
        for k,(sv,vi) in enumerate(zip(stim,vols)):
            if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            n_ev+=1
            inter=(vols[k+1]-vi) if k+1<len(vols) else 62
            mv=max(12, min(int((inter*0.5-5)/0.5), 60))
            end=min(T, vi+mv)
            if end-vi<12: continue
            raw=G[vi-SHIFT:end,:]
            base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
            seg=raw-base
            sm=np.nansum(seg[SHIFT:, keep], axis=0)
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                byA[i]["conn" if conn[i_,j_] else "unconn"].append(float(sm[kk]))
rows=[]
for an,dd in byA.items():
    if len(dd["conn"])<10 or len(dd["unconn"])<50: continue
    a=np.array(dd["conn"]); b=np.array(dd["unconn"])
    # standardise within the animal so scale differences do not drive the between-animal spread
    allv=np.concatenate([a,b]); mu=allv.mean(); sd=allv.std()
    if not np.isfinite(sd) or sd<=0: continue
    az=(a-mu)/sd; bz=(b-mu)/sd
    diff = az.mean()-bz.mean()
    se = math.sqrt(az.var(ddof=1)/az.size + bz.var(ddof=1)/bz.size)
    rows.append({"animal":int(an),"n_conn":int(a.size),"n_unconn":int(b.size),
                 "d":float(diff),"se":float(se),"vi":float(se*se)})
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(rows)} 只进入分析")
d=np.array([r["d"] for r in rows]); se=np.array([r["se"] for r in rows]); vi=se**2
w=1/vi
# fixed-effect pooled
fe=(d*w).sum()/w.sum(); se_fe=math.sqrt(1/w.sum())
Q=float((w*(d-fe)**2).sum()); k=len(d); df=k-1
# I^2
I2=max(0.0,(Q-df)/Q) if Q>0 else 0.0
# DerSimonian-Laird tau^2 and random-effects
C=w.sum()-(w**2).sum()/w.sum()
tau2=max(0.0,(Q-df)/C) if C>0 else 0.0
wr=1/(vi+tau2); re_=(d*wr).sum()/wr.sum(); se_re=math.sqrt(1/wr.sum())
print(f"\n  === 逐动物效应分布 ===")
print(f"    d 中位 {np.median(d):+.4f}  均值 {d.mean():+.4f}  SD {d.std(ddof=1):.4f}")
print(f"    范围 [{d.min():+.4f}, {d.max():+.4f}]   四分位 [{np.percentile(d,25):+.4f}, {np.percentile(d,75):+.4f}]")
print(f"    为正的动物: {int((d>0).sum())}/{k} ({100*(d>0).mean():.1f}%)")
print(f"    单独显著的动物 (|d|>1.96*se): {int((np.abs(d)>1.96*se).sum())}/{k}")
print(f"\n  === 异质性 ===")
print(f"    Cochran Q = {Q:.1f}  df = {df}   (Q~df 表示一个共同效应足够)")
print(f"    I^2 = {100*I2:.1f}%   (0% 同质, 越高表示动物间差异越大)")
print(f"    tau^2 (DL) = {tau2:.6f}   tau = {math.sqrt(tau2):.4f}")
print(f"\n  === 合并估计 ===")
print(f"    固定效应   d = {fe:+.4f}  SE {se_fe:.4f}   95% CI [{fe-1.96*se_fe:+.4f}, {fe+1.96*se_fe:+.4f}]")
print(f"    随机效应   d = {re_:+.4f}  SE {se_re:.4f}   95% CI [{re_-1.96*se_re:+.4f}, {re_+1.96*se_re:+.4f}]")
# prediction interval: where would a NEW animal's effect fall?
pi_se=math.sqrt(se_re**2+tau2)
print(f"    预测区间 (新动物) [{re_-1.96*pi_se:+.4f}, {re_+1.96*pi_se:+.4f}]   <- 若跨零，则新动物可能反向")
json.dump({"n_animals":len(rows),"d_median":float(np.median(d)),"d_mean":float(d.mean()),
           "d_sd":float(d.std(ddof=1)),"d_min":float(d.min()),"d_max":float(d.max()),
           "frac_positive":float((d>0).mean()),"Q":Q,"df":df,"I2":I2,"tau2":tau2,
           "fe":float(fe),"se_fe":float(se_fe),"re":float(re_),"se_re":float(se_re),
           "pi_lo":float(re_-1.96*pi_se),"pi_hi":float(re_+1.96*pi_se),
           "per_animal":rows}, open("/tmp/osf/peranimal.json","w"), indent=2)
