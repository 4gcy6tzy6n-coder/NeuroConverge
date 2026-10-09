"""Is the measurement-error share robust across the OTHER specification choices?

Round 26 concluded that eps (within-cell measurement error) is stable at 37-39 per cent while beta is not.
But it only varied min_an -- the minimum number of animals per pair.  It did not vary the response read-out,
the post-stimulus window, the pre-stimulus baseline, or whether the values are standardised per cell.

If eps moves under those, the surviving claim of round 26 is also fragile, and this tests that directly.

Grid:
  readout : signed sum over the window  |  mean over the window
  window  : 12 volumes (6 s)  |  24 volumes (12 s)  |  48 volumes (24 s)
  baseline: volumes 30..60 (source convention)  |  volumes 0..60
  cellnorm: none  |  divide each cell by its own median absolute deviation
Each cell of the grid gives the four shares at min_an = 1 and at min_an = 3.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, itertools
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
SHIFT=60
def tf(x): return np.log(abs(x)+1.0)*(1.0 if x>=0 else -1.0)

def collect(readout, post, base_lo, cellnorm):
    cell=collections.defaultdict(list); n_an=0; nev=0
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
            mad=None
            if cellnorm:
                med=np.nanmedian(G,axis=0)                       # ALL columns
                mad=np.nanmedian(np.abs(G-med),axis=0)           # ALL columns, shape matches dv
                mad=np.where((mad>0)&np.isfinite(mad), mad, np.nan)
            for sv,vi in zip(stim,vols):
                if sv<0 or vi<base_lo or vi+post>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                nev+=1
                post_m=np.nanmean(G[vi:vi+post,:],axis=0)
                base_m=np.nanmean(G[vi-base_lo:vi,:],axis=0)
                dv=post_m-base_m
                if cellnorm and mad is not None:
                    dv=np.where(np.isfinite(mad), dv/mad, np.nan)
                if readout=="sum":
                    # the sum over the window, baseline-corrected per volume
                    seg=G[vi:vi+post,:]-base_m
                    if cellnorm and mad is not None:
                        seg=np.where(np.isfinite(mad)[None,:], seg/mad[None,:], np.nan)
                    val=np.nansum(seg[:,keep],axis=0)
                else:
                    val=dv[keep]
                for kk,c in enumerate(keep):
                    if not np.isfinite(val[kk]): continue
                    cell[(i, lab[sv], lab[c])].append(float(val[kk]))
    return cell,n_an,nev

def decompose(cell,minan):
    pa=collections.defaultdict(set)
    for (a,tg,rc) in cell: pa[(tg,rc)].add(a)
    sel={k for k,v in pa.items() if len(v)>=minan}
    sub={k:v for k,v in cell.items() if (k[1],k[2]) in sel}
    if len(sub)<3000: return None
    eps=np.array([np.var([tf(x) for x in v],ddof=1) for v in sub.values() if len(v)>=2])
    eps=eps[np.isfinite(eps)]
    if eps.size<200: return None
    var_eps=float(np.median(eps))
    cm={k:float(np.mean([tf(x) for x in v])) for k,v in sub.items()}
    var_tot=float(np.var(list(cm.values())))
    if var_tot<=0: return None
    an=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): an[a].append(m)
    var_alpha=float(np.var([float(np.mean(v)) for v in an.values()]))
    pv=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): pv[(tg,rc)].append(m)
    var_pair=float(np.var([float(np.mean(v)) for v in pv.values()]))
    var_beta=var_tot-var_alpha-var_pair-var_eps
    return {"n_units":len(sub),"frac_pair":var_pair/var_tot,"frac_eps":var_eps/var_tot,
            "frac_beta":float(var_beta/var_tot),"frac_alpha":var_alpha/var_tot}

rows=[]
grid=list(itertools.product(("sum","mean"),(12,24,48),(60,),("none","mad")))
grid=[g for g in grid if not (g[3]=="mad" and g[1]!=24)]   # cellnorm tested at one window only
print(f"  网格 {len(grid)} 格（readout × window × baseline × cellnorm）\n")
print(f"  {'readout':>7} {'post':>5} {'cellnorm':>9} {'min_an':>7} {'units':>8} {'pair%':>7} {'eps%':>7} {'beta%':>7} {'alpha%':>7}")
for readout,post,b_lo,cn in grid:
    cell,n_an,nev=collect(readout,post,b_lo,cn)
    for minan in (1,3):
        r=decompose(cell,minan)
        if r is None:
            print(f"  {readout:>7} {post:>5} {cn:>9} {minan:>7}  -- 单元不足"); continue
        rows.append({"readout":readout,"post":post,"base_lo":b_lo,"cellnorm":cn,"min_an":minan,**r})
        print(f"  {readout:>7} {post:>5} {cn:>9} {minan:>7} {r['n_units']:>8,} "
              f"{100*r['frac_pair']:>6.1f} {100*r['frac_eps']:>6.1f} {100*r['frac_beta']:>6.1f} {100*r['frac_alpha']:>6.1f}")
e=np.array([r["frac_eps"] for r in rows])
b=np.array([r["frac_beta"] for r in rows])
print(f"\n  === eps 与 beta 的跨规格范围 ===")
print(f"    eps : min {100*e.min():.1f}%  中位 {100*np.median(e):.1f}%  max {100*e.max():.1f}%   极差 {100*(e.max()-e.min()):.1f} 点")
print(f"    beta: min {100*b.min():.1f}%  中位 {100*np.median(b):.1f}%  max {100*b.max():.1f}%   极差 {100*(b.max()-b.min()):.1f} 点")
# split by min_an
for m in (1,3):
    sub=[r for r in rows if r["min_an"]==m]
    if sub:
        ee=np.array([r["frac_eps"] for r in sub])
        print(f"    min_an={m}: eps {100*ee.min():.1f}–{100*ee.max():.1f}%  (中位 {100*np.median(ee):.1f}%)  n规格 {len(sub)}")
print(f"\n  === 判读 ===")
print(f"    若 eps 的极差远小于 37-39 点的宽度 ⟹ 第 26 轮的存活主张成立")
print(f"    若 eps 极差与 beta 极差同量级 ⟹ 第 26 轮也需再收窄")
json.dump(rows, open("/tmp/osf/eps_grid.json","w"), indent=2)
