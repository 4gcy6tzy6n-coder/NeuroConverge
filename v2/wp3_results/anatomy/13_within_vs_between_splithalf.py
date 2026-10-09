"""INVALID -- DO NOT USE for the ICC.

The split-half reliabilities in this script ARE sound and are reported in
WITHIN_VS_BETWEEN_ANIMAL.md section 1.  The ICC computation at the end is NOT: it computes the
within-animal variance as np.var(vs) if len(vs)>1 else 0.0, and the majority of (animal, pair)
units contain exactly one measurement, so mean(W) is a mean over a mostly-zero vector and the
ICC is inflated by construction.  The tell was that per-animal centring left the ICC identical
to four decimals.  Retained so the failure is auditable.
"""
"""Within-animal versus between-animal variance in per-pair functional response.

If the atlas's low cross-animal split-half reliability (r_full ~ 0.23) were measurement noise, then
within-animal repeats would ALSO be unreliable.  If within-animal repeats are reliable while cross-animal
agreement is not, the heterogeneity is BIOLOGICAL, and aggregating into one atlas entry suppresses it.

Decomposition: for every neuron pair measured in >=2 animals, split the total variance of its
measurements into a within-animal component and a between-animal component, and report the intraclass
correlation ICC = between / (between + within).
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
SHIFT=60
# pair-level (pooled over animals) lists of (animal, value)
pair=collections.defaultdict(list); pair_meas=collections.defaultdict(list)
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
                pair[(i_,j_)].append((i,float(sm[kk])))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(pair):,} 个配对")
# --- within-animal reliability: for (animal,pair) with >=2 measurements, split-half
wa_m1=[];wa_m2=[]; n_wa=0
for key,vals in pair.items():
    arms=collections.defaultdict(list)
    for an,v in vals: arms[an].append(v)
    for an,vs in arms.items():
        if len(vs)<2: continue
        n_wa+=1
        h=len(vs)//2
        wa_m1.append(np.mean(vs[:h])); wa_m2.append(np.mean(vs[h:]))
# --- between-animal reliability: for pairs in >=4 animals, split the ANIMALS into halves
rng=np.random.default_rng(0)
ba_m1=[];ba_m2=[]; n_ba=0
for key,vals in pair.items():
    arms=collections.defaultdict(list)
    for an,v in vals: arms[an].append(v)
    if len(arms)<4: continue
    n_ba+=1
    ans=list(arms); o=rng.permutation(len(ans)); h=len(ans)//2
    ba_m1.append(np.mean([np.mean(arms[ans[k]]) for k in o[:h]]))
    ba_m2.append(np.mean([np.mean(arms[ans[k]]) for k in o[h:]]))
def sb(a,b):
    a=np.array(a);b=np.array(b); r=np.corrcoef(a,b)[0,1]; return r, 2*r/(1+r)
print(f"\n  === 两种信度 ===")
if len(wa_m1)>100:
    r,rf=sb(wa_m1,wa_m2)
    print(f"    同一动物内重复 (n={n_wa:,} 个单元):   r={r:.4f}  r_full={rf:.4f}")
if len(ba_m1)>100:
    r,rf=sb(ba_m1,ba_m2)
    print(f"    跨动物 (n={n_ba:,} 个配对, >=4 只动物): r={r:.4f}  r_full={rf:.4f}")
# --- variance decomposition: ICC over pairs seen in >=2 animals
W=[];B=[]
for key,vals in pair.items():
    arms=collections.defaultdict(list)
    for an,v in vals: arms[an].append(v)
    if len(arms)<2: continue
    w=np.mean([np.var(vs) if len(vs)>1 else 0.0 for vs in arms.values()])
    b=np.var([np.mean(vs) for vs in arms.values()])
    W.append(w); B.append(b)
W=np.array(W); B=np.array(B)
icc = B.mean()/(B.mean()+W.mean())
print(f"\n  === 方差成分 (配对 >=2 只动物, n={W.size:,}) ===")
print(f"    动物内方差 均值 {W.mean():.4g}   动物间方差 均值 {B.mean():.4g}")
print(f"    ICC = 动物间/(动物间+动物内) = {icc:.4f}")
print(f"    ==> ICC 高 ⟹ 配对响应是动物的稳定属性、且动物间不同 ⟹ 异质性是生物学的")
print(f"    ==> ICC 低 ⟹ 主要是测量噪声")
json.dump({"n_animals":n_an,"n_events":n_ev,"n_pairs":len(pair),
           "within_animal_units":n_wa,"within_animal_rfull":float(2*np.corrcoef(wa_m1,wa_m2)[0,1]/(1+np.corrcoef(wa_m1,wa_m2)[0,1])) if len(wa_m1)>100 else None,
           "between_animal_pairs":n_ba,"between_animal_rfull":float(2*np.corrcoef(ba_m1,ba_m2)[0,1]/(1+np.corrcoef(ba_m1,ba_m2)[0,1])) if len(ba_m1)>100 else None,
           "ICC":float(icc),"within_var":float(W.mean()),"between_var":float(B.mean())},
          open("/tmp/osf/variance_decomp.json","w"), indent=2)
