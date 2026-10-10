"""Verify each re-implemented step against the code's own value, BEFORE using it in a grid.

Six consecutive grids of this line failed because a re-implemented step differed from the code's and the
difference was attributed to a scientific cause.  The rule that follows -- verify a step against the original's
value for THAT step alone -- has been written into the corpus index and not yet followed.  This follows it.

Step 1, one animal, both pipelines, comparing AFTER EACH INTERMEDIATE:
    dv    : post - baseline
    sd    : nanmedian(nanstd(dv, axis=1))          <- the code's axis
    dvs   : dv / sd
    cm    : nanmean(dvs, axis=1, keepdims=True)    <- per VOLUME
    dev   : dvs - cm
    per-cell value : dev[:, c].mean()

If every intermediate matches, the re-implementation is the code for that animal, and only then is a grid over
it meaningful.
"""
import numpy as np, pathlib, collections, re
DATA=pathlib.Path("/tmp/osf/w/exported_data")
POST=24; SHIFT=60
i=0
gp,lp,sp,vp=(DATA/f"{i}_gcamp.txt",DATA/f"{i}_labels.txt",DATA/f"{i}_stim_neurons.txt",DATA/f"{i}_stim_volume_i.txt")
G=np.loadtxt(gp); lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
T,ncol=G.shape
cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
uniq={n for n,c in cnt.items() if c==1}
keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
sv,vi=next((a,b) for a,b in zip(stim,vols) if a>=0 and b>=SHIFT and b+POST<T and a<len(lab) and lab[a] in uniq)
print(f"  动物 {i}, 首个可用事件 sv={sv} vi={vi}, G {G.shape}, keep {len(keep)}\n")

# --- ORIGINAL, transcribed line for line from 09_animal_level.py
post_m=G[vi:vi+POST,:]; base=G[vi-30:vi,:]
b_=np.nanmean(base,axis=0); dv=post_m-b_
sd=np.nanmedian(np.nanstd(dv,axis=1))
dvs=dv/sd; cm=np.nanmean(dvs,axis=1,keepdims=True); dev=dvs-cm
orig=np.array([dev[:,c].mean() for c in keep])
# --- RE-IMPLEMENTATION, written independently
dv2=G[vi:vi+POST,:]-np.nanmean(G[vi-30:vi,:],axis=0)
sd2=np.nanmedian(np.nanstd(dv2,axis=1))
if not np.isfinite(sd2) or sd2<=0: raise SystemExit("sd invalid")
d2=dv2/sd2
cm2=np.nanmean(d2,axis=1,keepdims=True)
dev2=d2-cm2
reimpl=np.array([np.nanmean(dev2[:,c]) for c in keep])
print("  === 逐步对照 ===")
def cmp(name,a,b):
    if np.isscalar(a) or (hasattr(a,'ndim') and a.ndim==0):
        ok=np.isclose(a,b,rtol=1e-12,atol=1e-12); print(f"    {name:<10} 原始 {a!r:>22}  重实现 {b!r:>22}  {'OK' if ok else 'MISMATCH'}")
        return ok
    a=np.asarray(a); b=np.asarray(b)
    same=a.shape==b.shape and np.allclose(a,b,rtol=1e-12,atol=1e-12)
    d=np.nanmax(np.abs(a-b)) if a.shape==b.shape else float('nan')
    print(f"    {name:<10} shape {a.shape} vs {b.shape}   最大绝对差 {d:.3e}   {'OK' if same else 'MISMATCH'}")
    return same
oks=[cmp("sd",sd,sd2),cmp("dv",dv,dv2),cmp("dvs",dvs,d2),cmp("cm",cm,cm2),cmp("dev",dev,dev2),
     cmp("per-cell",orig,reimpl)]
print(f"\n  ==> {'全部中间量一致：重实现就是代码，可安全用于网格' if all(oks) else '**存在不一致，网格不得使用**'}")
print(f"\n  sd 的量级: {sd:.6g}   （这就是逐事件加权的分母）")
print(f"  dev 的量级: 中位 {np.nanmedian(np.abs(dev)):.4g}   max {np.nanmax(np.abs(dev)):.4g}")
