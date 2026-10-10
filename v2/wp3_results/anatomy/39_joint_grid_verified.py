"""The corrected joint grid, built from a step that was verified against the code first.

Round 39's joint grid is void because it divided by the wrong axis.  Before rebuilding it, the step-verification
harness compared every intermediate of the re-implementation against 09_animal_level.py's for one animal and
found bit-identical agreement for sd, dv, dvs, cm and dev, and for the per-cell value.  This grid uses that
verified sequence and the code's ORDER:

    dv   = post - baseline                     (over ALL columns)
    sd   = nanmedian(nanstd(dv, axis=1))       (the code's axis, BEFORE any common mode)
    dvs  = dv / sd
    cm   = nanmean(dvs, axis=1, keepdims=True) (per VOLUME)
    dev  = dvs - cm
    v_c  = dev[:, c].mean()

Per-cell normalisation is inserted where the code has it (on the raw differences, before the weighting), and
the grid reports the ISOLATED sizes so additivity can finally be tested.
"""
import numpy as np, pathlib, re, collections, itertools, json, math
DATA=pathlib.Path("/tmp/osf/w/exported_data")
POSTS=(12,24,48)
def run(post, cellnorm, weighted):
    per=collections.defaultdict(lambda: {"c":[], "u":[]}); nev=0
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
        with np.errstate(all='ignore'):
            for sv,vi in zip(stim,vols):
                if sv<0 or vi<60 or vi+post>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                dv=G[vi:vi+post,:]-np.nanmean(G[vi-30:vi,:],axis=0)     # ALL columns
                if cellnorm:
                    s=np.nanstd(G[vi-30:vi,:],axis=0)
                    ok=np.isfinite(s)&(s>0)
                    dv=np.where(ok[None,:], dv/s[None,:], np.nan)
                if weighted:
                    sd=np.nanmedian(np.nanstd(dv,axis=1))               # the code's axis
                    if not np.isfinite(sd) or sd<=0: continue
                    dv=dv/sd
                cm=np.nanmean(dv,axis=1,keepdims=True); dev=dv-cm
                val=np.array([np.nanmean(dev[:,c]) for c in keep])
                nev+=1
                for kk,c in enumerate(keep):
                    v=val[kk]
                    if not np.isfinite(v): continue
                    tg=lab[sv]; rc=lab[c]
                    per[i]["c" if False else "u"]  # placeholder; connection decided below via a mask built once
    return None
# the per-cell connection decision needs the atlas; build it once
import h5py, csv
WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
fh=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in fh["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
def build(fn):
    C=np.zeros((N,N)); G=np.zeros((N,N))
    with open(WNA/fn, newline="") as f:
        for r in csv.DictReader(f, delimiter="\t"):
            p,q=r["pre"],r["post"]
            if p not in idx or q not in idx: continue
            s=float(r["synapses"]); i,j=idx[p],idx[q]
            if r["type"]=="chemical": C[i,j]+=s
            elif r["type"]=="electrical": G[i,j]+=s; G[j,i]+=s
    return C,G
c1,g1=build("aconnectome_witvliet_2020_8.csv"); c2,g2=build("aconnectome_white_1986_whole.csv")
CONN=(((c1+c2)!=0)|((g1+g2)!=0))&~np.eye(N,dtype=bool)
def run2(post, cellnorm, weighted):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
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
        with np.errstate(all='ignore'):
            for sv,vi in zip(stim,vols):
                if sv<0 or vi<60 or vi+post>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                dv=G[vi:vi+post,:]-np.nanmean(G[vi-30:vi,:],axis=0)
                if cellnorm:
                    s=np.nanstd(G[vi-30:vi,:],axis=0); ok=np.isfinite(s)&(s>0)
                    dv=np.where(ok[None,:], dv/s[None,:], np.nan)
                if weighted:
                    sd=np.nanmedian(np.nanstd(dv,axis=1))
                    if not np.isfinite(sd) or sd<=0: continue
                    dv=dv/sd
                cm=np.nanmean(dv,axis=1,keepdims=True); dev=dv-cm
                tg=sv and lab[sv]; ti=idx.get(tg)
                for c in keep:
                    v=float(np.nanmean(dev[:,c]))
                    if not np.isfinite(v): continue
                    nm=lab[c]; j_=idx.get(nm)
                    if ti is None or j_ is None: continue
                    per[i]["c" if CONN[ti,j_] else "u"].append(v)
    diffs=[]
    for i,d_ in per.items():
        if d_["c"] and d_["u"]: diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}
print(f"  {'post':>5} {'cellnorm':>9} {'weighted':>9} {'n_an':>6} {'d_A':>8} {'t':>7}")
rows={}
for post,cn,w in itertools.product(POSTS,(False,True),(False,True)):
    r=run2(post,cn,w)
    if r is None: print(f"  {post:>5} {str(cn):>9} {str(w):>9}  -- 不足"); continue
    rows[(post,cn,w)]=r
    print(f"  {post:>5} {str(cn):>9} {str(w):>9} {r['n_animals']:>6} {r['d_A']:>8.4f} {r['t']:>7.3f}")
print(f"\n  === 与代码的值对照（这是正确性检验）===")
code=rows.get((24,False,True))
if code:
    print(f"    本网格 post=24 cellnorm=off weighted=on: d_A {code['d_A']:.4f}  t {code['t']:.4f}  n {code['n_animals']}")
    print(f"    09_animal_level.py 报的是            : d_A 0.7289  t 7.610  n 109")
    print(f"    ==> {'复现' if abs(code['d_A']-0.7289)<0.01 else '差 %.4f' % abs(code['d_A']-0.7289)}")
print(f"\n  === 可加性检验 ===")
for post in POSTS:
    b=rows.get((post,False,False)); c=rows.get((post,True,False)); w=rows.get((post,False,True)); j=rows.get((post,True,True))
    if all(x is not None for x in (b,c,w,j)):
        ic=c["d_A"]-b["d_A"]; iw=w["d_A"]-b["d_A"]; jo=j["d_A"]-b["d_A"]
        print(f"    post={post}: 基线 {b['d_A']:.4f}  仅cellnorm {ic:+.4f}  仅weight {iw:+.4f}  "
              f"联合 {jo:+.4f}  孤立和 {ic+iw:+.4f}  交互 {jo-(ic+iw):+.4f}")
d=[r["d_A"] for r in rows.values()]
print(f"\n  === 全部 {len(rows)} 格范围 === {min(d):.4f} .. {max(d):.4f}   极差 {max(d)-min(d):.4f}")
json.dump({f"{k[0]}|{k[1]}|{k[2]}":v for k,v in rows.items()}, open("/tmp/osf/joint_verified.json","w"), indent=2)
