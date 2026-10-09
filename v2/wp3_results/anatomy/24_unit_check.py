"""What does treating pair-measurements as replicates actually inflate: significance, or effect size?

V2-C1 states that treating pair-measurements as independent replicates inflates the standardised
connectivity-function effect by 11 to 18 times.  Tracing every d in the corpus to its defining line found
that the pair-level numbers come from

    d = diff / sqrt(var_a/n_a + var_b/n_b)

which is diff over the STANDARD ERROR, a z-score, while the animal-level number comes from

    d = mean(diff) / sd(diff)

which is a Cohen's d.  Their ratio is therefore SD/SE = sqrt(n_effective), not an effect-size inflation.

This computes BOTH at BOTH units from the same records so the comparison is like for like.
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
# the source convention, mirroring 08_baseline_conventions.py: shift_vol 60, 24-volume post window,
# baseline = volumes 30..60, no common-mode removal, no per-cell standardisation
POST=24
per_pair=collections.defaultdict(list); per_animal=collections.defaultdict(lambda: {"c":[],"u":[]})
n_an=0; nev=0
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
        for sv,vi in zip(stim,vols):
            if sv<0 or vi<60 or vi+POST>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            nev+=1
            post=np.nanmean(G[vi:vi+POST,:],axis=0); base=np.nanmean(G[vi-30:vi,:],axis=0)
            dv=post-base
            for c in keep:
                v=dv[c]
                if not np.isfinite(v): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                isconn = (i_ is not None and j_ is not None and conn[i_,j_])
                per_pair[(tg,rc)].append(float(v))
                per_animal[i]["c" if isconn else "u"].append(float(v))
print(f"  {n_an} 只动物, {nev:,} 事件")
# --- pair level: treat every pair-measurement as an independent observation
allc=[]; allu=[]
for (tg,rc),v in per_pair.items():
    i_,j_=idx.get(tg),idx.get(rc)
    (allc if (i_ is not None and j_ is not None and conn[i_,j_]) else allu).extend(v)
allc=np.array(allc); allu=np.array(allu)
diff=allc.mean()-allu.mean()
se=math.sqrt(allc.var(ddof=1)/allc.size + allu.var(ddof=1)/allu.size)
sd_pool=math.sqrt(((allc.size-1)*allc.var(ddof=1)+(allu.size-1)*allu.var(ddof=1))/(allc.size+allu.size-2))
print(f"\n  === 配对级（把每个配对测量当作独立观测）===")
print(f"    有连接 {allc.mean():+.5f} (n={allc.size:,})   无连接 {allu.mean():+.5f} (n={allu.size:,})")
print(f"    差 {diff:+.5f}   合并 SD {sd_pool:.5f}   SE {se:.6f}")
print(f"    **z = diff/SE   = {diff/se:.4f}**   ← 语料中报为「d = 11.048」")
print(f"    **Cohen's d    = {diff/sd_pool:.4f}**   ← 真正的配对级效应量")
# --- animal level: paired Cohen's d
pc=[];pu=[]
for i,d_ in per_animal.items():
    if len(d_["c"])>=10 and len(d_["u"])>=50:
        pc.append(np.mean(d_["c"])); pu.append(np.mean(d_["u"]))
pc=np.array(pc); pu=np.array(pu); dd=pc-pu; n=dd.size
m=dd.mean(); s=dd.std(ddof=1); t=m/(s/math.sqrt(n))
print(f"\n  === 动物级（配对）===")
print(f"    动物 {n}   差 {m:+.5f}   跨动物 SD {s:.5f}   SE {s/math.sqrt(n):.5f}")
print(f"    **t = diff/SE  = {t:.4f}**")
print(f"    **Cohen's d    = diff/SD = {m/s:.4f}**")
print(f"\n  === 判读 ===")
print(f"    配对级 z / 动物级 t      = {(diff/se)/t:.2f}   （这是两个显著性之比）")
print(f"    配对级 Cohen d / 动物级 d = {(diff/sd_pool)/(m/s):.4f}   （这是两个效应量之比）")
print(f"    sqrt(n_eff) 预言值        = {math.sqrt(2/(1/allc.size+1/allu.size)):.1f}")
print(f"\n    ==> 若「膨胀」= z 之比，则它等于 sqrt(n) 之比，是同义反复")
print(f"    ==> 真正的效应量之比是 {(diff/sd_pool)/(m/s):.4f}，即配对级效应量**更小**")
json.dump({"pair":{"mean_conn":float(allc.mean()),"mean_unconn":float(allu.mean()),
                   "diff":float(diff),"sd_pool":float(sd_pool),"se":float(se),
                   "z":float(diff/se),"cohens_d":float(diff/sd_pool),
                   "n_conn":int(allc.size),"n_unconn":int(allu.size)},
           "animal":{"n":int(n),"diff":float(m),"sd":float(s),"se":float(s/math.sqrt(n)),
                     "t":float(t),"cohens_d":float(m/s)},
           "ratio_of_significance":float((diff/se)/t),
           "ratio_of_effect_sizes":float((diff/sd_pool)/(m/s)),
           "sqrt_n_eff":float(math.sqrt(2/(1/allc.size+1/allu.size)))},
          open("/tmp/osf/unit_check.json","w"), indent=2)
