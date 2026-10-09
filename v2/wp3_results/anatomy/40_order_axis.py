"""The order of application as an explicit axis.

Round 41 found the two largest dimensions are strongly non-additive because both are normalisations and each
rescales the quantity the other operates on.  That implies the ORDER matters, and only the code's order has
been tested:

    ORDER A (the code's):  dv  ->  /s_cell   ->  /sd(dv/s_cell)  ->  common mode
    ORDER B:               dv  ->  /sd(dv)   ->  /s_cell        ->  common mode

The two differ because the weighting's denominator is computed on different arrays: sd_A from the
cell-normalised differences and sd_B from the raw ones, and those differ unless every cell's scale is equal.

Uses the verified step sequence, so the ORDER A arm at post 24 with weighting on must reproduce 0.7289.
"""
import numpy as np, h5py, csv, pathlib, re, collections, itertools, json, math
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
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
def run(order, post=24, weighted=True, cellnorm=True):
    """order: 'A' = cellnorm then weighting (the code's); 'B' = weighting then cellnorm;
              'none' = neither; 'cn' = cellnorm only; 'w' = weighting only."""
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
                s=np.nanstd(G[vi-30:vi,:],axis=0); ok=np.isfinite(s)&(s>0)
                def cn(x): return np.where(ok[None,:], x/s[None,:], np.nan)
                def wg(x):
                    sd=np.nanmedian(np.nanstd(x,axis=1))
                    return x/sd if (np.isfinite(sd) and sd>0) else None
                if order=="A":      # cellnorm -> weighting
                    d=cn(dv); d=wg(d)
                elif order=="B":    # weighting -> cellnorm
                    d=wg(dv);  d=cn(d) if d is not None else None
                elif order=="cn":   d=cn(dv)
                elif order=="w":    d=wg(dv)
                else:               d=dv
                if d is None: continue
                cm=np.nanmean(d,axis=1,keepdims=True); dev=d-cm
                ti=idx.get(lab[sv])
                if ti is None: continue
                for c in keep:
                    v=float(np.nanmean(dev[:,c]))
                    if not np.isfinite(v): continue
                    j_=idx.get(lab[c])
                    if j_ is None: continue
                    per[i]["c" if CONN[ti,j_] else "u"].append(v)
    diffs=[]
    for i,d_ in per.items():
        if d_["c"] and d_["u"]: diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}
print(f"  {'order':>6} {'post':>5} {'d_A':>9} {'t':>7} {'n_an':>6}")
rows={}
for order,post in itertools.product(("none","cn","w","A","B"),(12,24,48)):
    r=run(order,post)
    if r is None: print(f"  {order:>6} {post:>5}  -- 不足"); continue
    rows[(order,post)]=r
    print(f"  {order:>6} {post:>5} {r['d_A']:>9.4f} {r['t']:>7.3f} {r['n_animals']:>6}")
print(f"\n  === 正确性检验（ORDER A, post=24, 代码的顺序）===")
chk=rows.get(("A",24))
if chk:
    print(f"    ORDER A post=24: d_A {chk['d_A']:.4f}  t {chk['t']:.4f}")
    print(f"    代码报的是     : d_A 0.7289  t 7.610")
    print(f"    ==> {'复现' if abs(chk['d_A']-0.7289)<0.01 else '差 %.4f' % abs(chk['d_A']-0.7289)}")
print(f"\n  === 顺序是否重要 ===")
for post in (12,24,48):
    a=rows.get(("A",post)); b=rows.get(("B",post))
    if a and b:
        print(f"    post={post}: A (cellnorm->weight) {a['d_A']:+.4f}   B (weight->cellnorm) {b['d_A']:+.4f}   "
              f"顺序效应 {b['d_A']-a['d_A']:+.4f}")
print(f"\n  === 全部范围 ===")
d=[r["d_A"] for r in rows.values()]
print(f"    {min(d):.4f} .. {max(d):.4f}   极差 {max(d)-min(d):.4f}   跨零: {min(d)<0<max(d)}")
json.dump({f"{k[0]}|{k[1]}":v for k,v in rows.items()}, open("/tmp/osf/order_axis.json","w"), indent=2)
