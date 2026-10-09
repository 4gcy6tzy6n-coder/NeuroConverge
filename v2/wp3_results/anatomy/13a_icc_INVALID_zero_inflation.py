"""INVALID -- DO NOT USE for the ICC.

The split-half reliabilities in this script ARE sound and are reported in
WITHIN_VS_BETWEEN_ANIMAL.md section 1.  The ICC computation at the end is NOT: it computes the
within-animal variance as np.var(vs) if len(vs)>1 else 0.0, and the majority of (animal, pair)
units contain exactly one measurement, so mean(W) is a mean over a mostly-zero vector and the
ICC is inflated by construction.  The tell was that per-animal centring left the ICC identical
to four decimals.  Retained so the failure is auditable.
"""
"""Is the ICC = 0.93 animal-specific PAIR structure, or a global animal offset?

Two competing explanations for a high intraclass correlation:
  A) each pair's response really differs between animals (pair-specific heterogeneity)
  B) each animal has a global scale/offset -- GCaMP level, baseline, dissection quality -- that shifts
     ALL of its pairs together, which produces a high ICC with NO pair-specific animal difference.

Test: recompute the ICC after removing each animal's own centre, and after standardising each animal.
If the ICC collapses, B explains it.  If it survives, A does.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
SHIFT=60
# collect (animal, pair) -> list of raw responses
unit=collections.defaultdict(list)
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
                unit[(i, i_, j_)].append(float(sm[kk]))
# per (animal,pair) mean
cell=collections.defaultdict(dict)     # pair -> {animal: mean}
for (an,i_,j_),v in unit.items():
    cell[(i_,j_)][an]=float(np.mean(v))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(cell):,} 个配对")
def icc(cellmap, transform=None):
    W=[];B=[]
    for key,arms in cellmap.items():
        if len(arms)<2: continue
        vals=np.array(list(arms.values()),float)
        if transform is not None:
            allv=np.array([v for vs in arms.values() for v in ([vs] if np.isscalar(vs) else vs)],float)
            vals=transform(vals)
        if vals.size<2: continue
        B.append(np.var(vals))
        # within-animal variance is not available from means alone; recompute from unit level below
    return np.array(B)
# Build the three versions at the cell level so within-animal variance is available
def build(tf):
    """tf: 'raw' | 'center' (subtract animal mean) | 'z' (standardise animal)"""
    out=collections.defaultdict(lambda: collections.defaultdict(list))
    for (an,i_,j_),v in unit.items():
        out[(i_,j_)][an].extend(v)
    if tf=="raw":
        return out
    # per-animal offset = mean over ALL pairs measured in that animal
    for key,arms in out.items():
        pass
    per_an=collections.defaultdict(list)
    for key,arms in out.items():
        for an,vs in arms.items(): per_an[an].extend(vs)
    mu={an:float(np.mean(v)) for an,v in per_an.items()}
    sd={an:float(np.std(v)) or 1.0 for an,v in per_an.items()}
    new=collections.defaultdict(lambda: collections.defaultdict(list))
    for key,arms in out.items():
        for an,vs in arms.items():
            if tf=="center": new[key][an]=[v-mu[an] for v in vs]
            else:            new[key][an]=[(v-mu[an])/sd[an] for v in vs]
    return new
res={}
for tf,label in (("raw","原始"),("center","逐动物中心化"),("z","逐动物标准化")):
    cm=build(tf)
    W=[];B=[]
    for key,arms in cm.items():
        if len(arms)<2: continue
        means=np.array([np.mean(vs) for vs in arms.values()],float)
        ws=[np.var(vs) if len(vs)>1 else 0.0 for vs in arms.values()]
        B.append(np.var(means)); W.append(np.mean(ws))
    W=np.array(W);B=np.array(B)
    icc=B.mean()/(B.mean()+W.mean())
    res[label]={"ICC":float(icc),"within":float(W.mean()),"between":float(B.mean()),"n_pairs":int(W.size)}
    print(f"\n  === {label} ===")
    print(f"    配对 {W.size:,}   动物内方差 {W.mean():.4g}   动物间方差 {B.mean():.4g}")
    print(f"    ICC = {icc:.4f}")
print(f"\n  === 判读 ===")
r=res["原始"]["ICC"]; c=res["逐动物中心化"]["ICC"]; z=res["逐动物标准化"]["ICC"]
print(f"    原始 {r:.3f} -> 中心化 {c:.3f} -> 标准化 {z:.3f}")
print(f"    若中心化后崩塌 ⟹ 高 ICC 由动物层面全局偏移解释（混淆 B）")
print(f"    若中心化后保持 ⟹ 配对特异的动物间异质性（解释 A）")
json.dump(res, open("/tmp/osf/icc_centered.json","w"), indent=2)
