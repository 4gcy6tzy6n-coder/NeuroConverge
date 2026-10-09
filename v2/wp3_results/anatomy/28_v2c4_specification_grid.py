"""V2-C4's range, with a cached load and without the redundant read-out axis.

Two changes from the first attempt, both recorded rather than silent:

1. The read-out axis is dropped.  If val_mean = val_sum / post then d_A = diff/SD is unchanged, because a
   global scale factor cancels in a ratio.  So sum and mean cannot produce different d_A values, and
   including both would double the table without adding a specification.  This is round 30's redundancy
   lesson applied BEFORE the grid was run rather than after.

2. The data are loaded once into memory.  The first attempt reloaded 113 files totalling 1.2 GB for each of
   48 cells and had completed none after two minutes.

Remaining axes, each of which changes d_A for a real reason:
  window    : 12, 24, 48 volumes of post-stimulus signal
  baseline  : volumes 30..60 (the source convention)  |  volumes 0..60
  per-cell  : none  |  divide by each cell's own pre-stimulus SD   (a PER-CELL scale, does not cancel)
  inclusion : none  |  require at least 10 connected and 50 unconnected pairs per animal
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, itertools, math, pickle
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
CACHE=pathlib.Path("/tmp/osf/v2c4_cache.pkl")
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

if CACHE.exists():
    events=pickle.loads(CACHE.read_bytes()); print(f"  从缓存载入 {len(events)} 个事件")
else:
    events=[]; n_an=0
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
            base60=np.full((T,),np.nan)
            for sv,vi in zip(stim,vols):
                if sv<0 or vi<60 or vi+48>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                # store the 48-volume segment and the two baselines, plus per-cell pre SD
                seg=G[vi:vi+48, keep]                       # (48, nkeep)
                b3060=np.nanmean(G[vi-30:vi, keep],axis=0)
                b060 =np.nanmean(G[vi-60:vi, keep],axis=0)
                sp_  =np.nanstd(G[vi-60:vi, keep],axis=0)
                names=[(lab[sv], lab[c]) for c in keep]
                flags=[bool(conn[idx[lab[sv]], idx[lab[c]]]) if (lab[sv] in idx and lab[c] in idx) else None for c in keep]
                events.append({"anim":i,"seg":seg.astype(np.float32),"b3060":b3060.astype(np.float32),
                               "b060":b060.astype(np.float32),"sp":sp_.astype(np.float32),
                               "names":names,"flags":flags})
    pickle.dump(events, CACHE.open("wb")); print(f"  已载入 {len(events)} 个事件并缓存")
print(f"  动物数 {len({e['anim'] for e in events})}")

def compute(post, base_lo, cellnorm, inclusion):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
    for e in events:
        seg=e["seg"][:post]; base=e["b3060"] if base_lo==60 else e["b060"]
        with np.errstate(all='ignore'):
            d=seg-base[None,:]
            if cellnorm:
                s=e["sp"]; ok=np.isfinite(s)&(s>0)
                d=np.where(ok[None,:], d/s[None,:], np.nan)
            val=np.nansum(d,axis=0)
        for k,(nm,fl) in enumerate(zip(e["names"], e["flags"])):
            if fl is None: continue
            v=val[k]
            if not np.isfinite(v): continue
            per[e["anim"]]["c" if fl else "u"].append(float(v))
    diffs=[]
    for i,d_ in per.items():
        if inclusion and (len(d_["c"])<10 or len(d_["u"])<50): continue
        if not d_["c"] or not d_["u"]: continue
        diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    if not np.isfinite(s) or s<=0: return None
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}
print()
print(f"  {'post':>5} {'base':>5} {'cellnorm':>9} {'incl':>6} {'n_an':>5} {'diff':>10} {'sd':>10} {'d_A':>8} {'t':>7}")
rows=[]
for post,base_lo,cn,inc in itertools.product((12,24,48),(60,0),(False,True),(False,True)):
    r=compute(post,base_lo,cn,inc)
    if r is None: print(f"  {post:>5} {base_lo:>5} {str(cn):>9} {str(inc):>6}  -- 动物不足"); continue
    rows.append({"post":post,"baseline_lo":base_lo,"cellnorm":cn,"inclusion":inc,**r})
    print(f"  {post:>5} {base_lo:>5} {str(cn):>9} {str(inc):>6} {r['n_animals']:>5} "
          f"{r['diff']:>10.4f} {r['sd']:>10.4f} {r['d_A']:>8.4f} {r['t']:>7.2f}")
d=np.array([r["d_A"] for r in rows])
print(f"\n  === V2-C4 的范围 ===")
print(f"    d_A: min {d.min():.4f}  中位 {np.median(d):.4f}  max {d.max():.4f}   极差 {d.max()-d.min():.4f}")
print(f"    V2-C4 报 0.0852..0.7289, 极差 0.6437")
print(f"    本网格极差 {d.max()-d.min():.4f}  ==>  {'更宽' if (d.max()-d.min())>0.6437 else '不更宽'}")
print(f"\n  === 冗余检查 ===")
for ax in ("post","baseline_lo","cellnorm","inclusion"):
    vals=collections.defaultdict(set)
    for r in rows: vals[r[ax]].add(round(r["d_A"],6))
    nd=len(set().union(*vals.values()))
    print(f"    {ax:>12}: {len(vals)} 级 -> {nd} 个不同 d_A  {'（无冗余）' if nd>1 else '（冗余）'}")
json.dump(rows, open("/tmp/osf/v2c4_grid2.json","w"), indent=2)
