"""Does pair composition explain the between-animal spread of the connectivity effect?

For each animal, predict its effect using ONLY which pairs it happened to measure and each pair's
LEAVE-ONE-ANIMAL-OUT mean response.  Leave-one-out is essential: using an animal's own data to predict its
own effect would be circular.

  high correlation  -> the between-animal spread is pair composition, i.e. sampling
  low  correlation  -> the spread is a genuine per-animal difference
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
# per (animal, pair): list of responses  -> then per-animal, per-pair mean
cell=collections.defaultdict(list)
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
                cell[(i,i_,j_)].append(float(sm[kk]))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(cell):,} 个 (动物,配对) 单元")
# per (animal,pair) mean, in log space (heavy tails)
def tf(x): return np.log(abs(x)+1.0)*(1.0 if x>=0 else -1.0)
ap=collections.defaultdict(list)
for (a,i_,j_),v in cell.items(): ap[(a,i_,j_)].append(np.mean([tf(x) for x in v]))
A=collections.defaultdict(dict)
for (a,i_,j_),v in ap.items(): A[a][(i_,j_)]=float(np.mean(v))
animals=sorted(A)
print(f"  进入分析的动物: {len(animals)}")
# leave-one-animal-out pair mean
pair_an=collections.defaultdict(dict)     # (i,j) -> {animal: value}
for a,d in A.items():
    for k,v in d.items(): pair_an[k][a]=v
loo={}
for k,d in pair_an.items():
    s=sum(d.values()); n=len(d)
    for a,v in d.items():
        if n>=2: loo[(a,k)]=(s-v)/(n-1)
print(f"  可算留一均值的 (动物,配对) 单元: {len(loo):,}")
obs=[]; pred=[]; ncomp=[]
for a in animals:
    o=[]; p=[]; nc=[]
    for (i_,j_),v in A[a].items():
        if (a,(i_,j_)) not in loo: continue
        isc=conn[i_,j_]; o.append(v); p.append(loo[(a,(i_,j_))]); nc.append(isc)
    if sum(nc)<10 or (len(nc)-sum(nc))<50: continue
    o=np.array(o); p=np.array(p); nc=np.array(nc)
    obs.append(o[nc].mean()-o[~nc].mean())          # observed effect, animal's own data
    pred.append(p[nc].mean()-p[~nc].mean())         # predicted from composition + leave-one-out pair means
    ncomp.append((int(nc.sum()), int((~nc).sum())))
obs=np.array(obs); pred=np.array(pred)
n=obs.size
print(f"\n  === 配对构成预测 vs 观测 ===")
print(f"    动物数 {n}")
print(f"    观测效应: 均值 {obs.mean():+.4f}  SD {obs.std(ddof=1):.4f}")
print(f"    构成预测: 均值 {pred.mean():+.4f}  SD {pred.std(ddof=1):.4f}")
r=np.corrcoef(obs,pred)[0,1]
print(f"    corr(构成预测, 观测) = {r:+.4f}   R^2 = {r*r:.4f}")
print()
print(f"  === 判读 ===")
print(f"    若 R^2 高   ⟹ 跨动物离散由配对构成解释（抽样，不是生物学）")
print(f"    若 R^2 低   ⟹ 配对构成之外还有真实的逐动物差异")
# how much of the observed variance does composition explain?
print(f"    构成预测解释了观测方差的 {100*r*r:.1f}%")
# also: does the prediction's own spread match the observed spread?
print(f"    预测 SD / 观测 SD = {pred.std(ddof=1)/obs.std(ddof=1):.4f}")
json.dump({"n_animals":int(n),"obs_mean":float(obs.mean()),"obs_sd":float(obs.std(ddof=1)),
           "pred_mean":float(pred.mean()),"pred_sd":float(pred.std(ddof=1)),
           "corr":float(r),"R2":float(r*r),"sd_ratio":float(pred.std(ddof=1)/obs.std(ddof=1))},
          open("/tmp/osf/composition.json","w"), indent=2)
