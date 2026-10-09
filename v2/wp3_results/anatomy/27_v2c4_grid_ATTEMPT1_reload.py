"""Is V2-C4's range the true range? A grid over specification choices at the animal unit.

V2-C4 states that analysis choices live in the pipeline's code and not in the data file, and that
re-analysing the same records under defensible choices moves the animal-level estimate across d 0.085 to
0.729.  That range came from four specifications chosen by hand.  Round 29 showed that adding read-outs
widened a similar range by 18 points, so this sweeps a declared grid and reports the range it produces.

Axes, each checked to actually vary the statistic before being used:
  readout   : signed sum over the analysis window  |  sum of that window minus the pre-stimulus mean
  window    : 12, 24, 48 volumes of post-stimulus signal
  baseline  : volumes 30..60 (the source convention)  |  volumes 0..60
  per-cell  : none  |  divide by the cell's own pre-stimulus spread
  inclusion : none  |  require at least 10 connected and 50 unconnected pairs

The statistic is d_A = mean(across-animal differences) / SD(across-animal differences), which round 28
confirmed is the quantity V2-C4's range is measured in.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, itertools, math
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
def run(readout, post, base_lo, cellnorm, inclusion):
    per=collections.defaultdict(lambda: {"c":[], "u":[]}); n_an=0; nev=0
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
                if sv<0 or vi<base_lo or vi+post>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                nev+=1
                base=np.nanmean(G[vi-base_lo:vi,:],axis=0)
                seg=G[vi:vi+post,:]-base
                if cellnorm:
                    sp_=np.nanstd(G[vi-base_lo:vi,:],axis=0)
                    sp_=np.where((sp_>0)&np.isfinite(sp_),sp_,np.nan)
                    seg=np.where(np.isfinite(sp_)[None,:], seg/sp_[None,:], np.nan)
                val=np.nansum(seg[:,keep],axis=0) if readout=="sum" else np.nanmean(seg[:,keep],axis=0)
                for kk,c in enumerate(keep):
                    v=val[kk]
                    if not np.isfinite(v): continue
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    isconn=(i_ is not None and j_ is not None and conn[i_,j_])
                    per[i]["c" if isconn else "u"].append(float(v))
    diffs=[]; nc=[]; nu=[]
    for i,d_ in per.items():
        if inclusion and (len(d_["c"])<10 or len(d_["u"])<50): continue
        if not d_["c"] or not d_["u"]: continue
        diffs.append(np.mean(d_["c"])-np.mean(d_["u"])); nc.append(len(d_["c"])); nu.append(len(d_["u"]))
    if len(diffs)<30: return None
    d_=np.array(diffs); m=d_.mean(); s=d_.std(ddof=1)
    if not np.isfinite(s) or s<=0: return None
    return {"n_animals":len(diffs),"animals_scanned":n_an,"events":nev,
            "diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}
grid=list(itertools.product(("sum","mean"),(12,24,48),(60,0),(False,True),(False,True)))
print(f"  网格 {len(grid)} 格\n")
print(f"  {'readout':>7} {'post':>5} {'base':>5} {'cellnorm':>9} {'incl':>6} {'n_an':>5} {'diff':>10} {'sd':>10} {'d_A':>8} {'t':>7}")
rows=[]
for readout,post,b_lo,cn,inc in grid:
    r=run(readout,post,b_lo,cn,inc)
    if r is None: print(f"  {readout:>7} {post:>5} {b_lo:>5} {str(cn):>9} {str(inc):>6}  -- 动物不足"); continue
    rows.append({"readout":readout,"post":post,"baseline_lo":b_lo,"cellnorm":cn,"inclusion":inc,**r})
    print(f"  {readout:>7} {post:>5} {b_lo:>5} {str(cn):>9} {str(inc):>6} {r['n_animals']:>5} "
          f"{r['diff']:>10.4f} {r['sd']:>10.4f} {r['d_A']:>8.4f} {r['t']:>7.2f}")
d=np.array([r["d_A"] for r in rows])
print(f"\n  === V2-C4 的范围 ===")
print(f"    d_A: min {d.min():.4f}  中位 {np.median(d):.4f}  max {d.max():.4f}   极差 {d.max()-d.min():.4f}")
print(f"    V2-C4 报的是 0.0852 到 0.7289，极差 0.6437")
print(f"    本网格的极差 {d.max()-d.min():.4f}  {'更宽' if (d.max()-d.min())>0.6437 else '不更宽'}")
print(f"\n  === 冗余检查（第 30 轮的方法注）===")
for ax in ("readout","post","baseline_lo","cellnorm","inclusion"):
    vals=collections.defaultdict(set)
    for r in rows: vals[r[ax]].add(round(r["d_A"],6))
    nlev=len(vals); ndistinct=len(set().union(*vals.values()))
    print(f"    {ax:>12}: {nlev} 级, 产出 {ndistinct} 个不同 d_A  {'（无冗余）' if ndistinct>1 else '（冗余，该轴不构成规格）'}")
json.dump(rows, open("/tmp/osf/v2c4_grid.json","w"), indent=2)
