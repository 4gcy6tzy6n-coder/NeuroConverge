"""Per-pair inverse-variance weighting, then the animal-level paired contrast.

Unlike the measurement count (which round 5 showed is confounded: corr with response +0.03 to +0.06 in
connected strata), the inverse-variance weight  w = n / sigma_within^2  is exogenous to the MEAN response:
it depends on the pair's measurement count and the DISPERSION of its measurements, not on their level.
The prediction to test: if the connectivity association is real, weighting by precision should leave it
standing or sharpen it.  If it collapses, the association was carried by unreliable pairs.
"""
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

# Use the source's own convention: 60-volume pre-window, late-half baseline, per-event window.
SHIFT=60
per_pair=collections.defaultdict(list)          # (animal, i, j) -> [responses]
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
                per_pair[(i,i_,j_)].append(float(sm[kk]))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(per_pair):,} 个 (动物,配对) 单元")

# per-(animal,pair) mean and inverse-variance weight
rec=[]
for (an,i_,j_),v in per_pair.items():
    if len(v)<2: continue                      # need >=2 to estimate within-variance
    a=np.array(v); m=a.mean(); s2=a.var(ddof=1)
    if not np.isfinite(s2) or s2<=0: 
        # zero within-variance: uninformative for weighting; use a small floor
        s2=1e-9
    w=len(a)/s2
    rec.append((an,i_,j_,conn[i_,j_],m,w,len(a)))
print(f"  可用于加权的单元: {len(rec):,}")
W=np.array([r[5] for r in rec]); print(f"  权重分布: 中位 {np.median(W):.3g}  p95 {np.percentile(W,95):.3g}  max {W.max():.3g}")
# sanity: does the weight correlate with the MEAN response?  (it must not, to be exogenous)
for labk, mask in (("conn", np.array([r[3] for r in rec])), ("unconn", ~np.array([r[3] for r in rec]))):
    mm=np.array([r[4] for r in rec])[mask]; ww=np.array([r[5] for r in rec])[mask]
    if mm.size>30:
        print(f"  corr(权重, 均值响应) [{labk}] = {np.corrcoef(np.log10(ww+1e-30), mm)[0,1]:+.4f}   n={mm.size:,}")

# animal-level: weighted mean of connected minus weighted mean of unconnected, per animal
byA=collections.defaultdict(lambda: {"conn":[], "unconn":[]})
for an,i_,j_,isc,m,w,n in rec:
    byA[an]["conn" if isc else "unconn"].append((m,w))
def wmean(pairs):
    m=np.array([p[0] for p in pairs]); w=np.array([p[1] for p in pairs])
    return float((m*w).sum()/w.sum())
d_uw=[]; d_w=[]
for an,dd in byA.items():
    if not dd["conn"] or not dd["unconn"]: continue
    d_w.append(wmean(dd["conn"])-wmean(dd["unconn"]))
    d_uw.append(np.mean([p[0] for p in dd["conn"]])-np.mean([p[0] for p in dd["unconn"]]))
d_w=np.array(d_w); d_uw=np.array(d_uw); n=d_w.size
def stats(d):
    m=d.mean(); s=d.std(ddof=1); return m, s, s/np.sqrt(n), m/(s/np.sqrt(n)), m/s
print(f"\n  === 动物级配对对比 (n={n}) ===")
print(f"  {'':>14} {'差':>12} {'跨动物SD':>12} {'t':>8} {'d':>8}")
for labk, d in (("未加权", d_uw), ("逆方差加权", d_w)):
    m,s,se,t,dd=stats(d)
    print(f"  {labk:>14} {m:>12.5f} {s:>12.5f} {t:>8.3f} {dd:>8.4f}")
m0,s0,_,t0,d0=stats(d_uw); m1,s1,_,t1,d1=stats(d_w)
print(f"\n  加权后 d 变化: {d0:.4f} -> {d1:.4f}  ({(d1/d0-1)*100:+.1f}%)")
print(f"  判读: 若关联真实，加权应保持或增强它；若崩塌，则关联由不可靠配对承载。")
json.dump({"n_animals":int(n),"d_unweighted":float(d0),"t_unweighted":float(t0),
           "d_iv_weighted":float(d1),"t_iv_weighted":float(t1),
           "change_pct":float((d1/d0-1)*100),"n_units":len(rec),
           "corr_w_mean_conn":float(np.corrcoef(np.log10(np.array([r[5] for r in rec])[np.array([r[3] for r in rec])]+1e-30),
                                                np.array([r[4] for r in rec])[np.array([r[3] for r in rec])])[0,1])},
          open("/tmp/osf/ivweight.json","w"), indent=2)
