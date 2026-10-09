"""Verify: the per-event sd division is a WEIGHTING, and it explains 0.39 versus 0.73.

The instrumented comparison found the code's per-cell values are ~80 to ~103 times the grid's, with a
NON-UNIFORM ratio.  A non-uniform ratio means no single global scalar explains it, which rules out the
"sd cancels in d_A" argument: the code computes sd PER EVENT, inside the event loop, so

    dev[:,c] = (dv[:,c] - mean_c'(dv[:,c'])) / sd_event

weights each event by 1/sd_event.  This runs the grid's own pipeline with and without that weighting, on the
same events, and reports d_A for each.
"""
import numpy as np, h5py, csv, pathlib, re, collections, math
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
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool); CONN=((chem!=0)|(gap!=0))&off
POST=24; SHIFT=60
def run(use_sd, post=POST, allcols=True):
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
                if sv<0 or vi<SHIFT or vi+post>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                nev+=1
                post_m=G[vi:vi+post,:]; base=G[vi-30:vi,:]
                dv=post_m-np.nanmean(base,axis=0)
                if use_sd:
                    sd=np.nanmedian(np.nanstd(dv,axis=1))
                    if not np.isfinite(sd) or sd<=0: continue
                    dv=dv/sd
                cm=np.nanmean(dv,axis=1,keepdims=True); dev=dv-cm
                for c in keep:
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    if i_ is None or j_ is None: continue
                    v=float(dev[:,c].mean())
                    if not np.isfinite(v): continue
                    per[i]["c" if CONN[i_,j_] else "u"].append(v)
    diffs=[]
    for i,d_ in per.items():
        if d_["c"] and d_["u"]: diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    return {"n_animals":len(diffs),"events":nev,"diff":float(m),"sd":float(s),
            "d_A":float(m/s),"t":float(m/(s/math.sqrt(len(diffs))))}
print(f"  {'use per-event sd':>18} {'animals':>8} {'diff':>10} {'sd':>10} {'d_A':>8} {'t':>7}")
res={}
for use_sd in (False,True):
    r=run(use_sd)
    if r is None: print(f"  {str(use_sd):>18}  -- 不足"); continue
    res[use_sd]=r
    print(f"  {str(use_sd):>18} {r['n_animals']:>8} {r['diff']:>10.5f} {r['sd']:>10.5f} {r['d_A']:>8.4f} {r['t']:>7.3f}")
print()
if False in res and True in res:
    a=res[False]["d_A"]; b=res[True]["d_A"]
    print(f"  === 判读 ===")
    print(f"    无 per-event sd 加权: d_A {a:.4f}")
    print(f"    有 per-event sd 加权: d_A {b:.4f}   （代码报 0.7289, 重跑确认逐位一致）")
    print(f"    ==> {'复现' if abs(b-0.7289)<0.02 else '仍差 %.4f' % abs(b-0.7289)}")
    print(f"    这一步的贡献: {b-a:+.4f}")
