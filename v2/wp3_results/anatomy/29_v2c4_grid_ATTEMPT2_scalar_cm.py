"""V2-C4's range with common-mode removal and the across-cell normalisation as axes.

Round 31 found that this grid's ceiling was 0.4408 while V2-C4's reported ceiling was 0.7289, and inferred
that the difference was carried by common-mode removal, which 10_robust_and_class.py applies and no grid here
varied.  This runs that grid, so the step's contribution is isolated rather than inferred.

The two steps 10_robust_and_class.py applies that the previous grid did not:
  across-SD : divide the per-event vector of differences by the ACROSS-CELL SD of that vector
              (its code: sd = nanmedian(nanstd(dv, axis=1)); dvs = dv/sd), not by the pre-stimulus SD
  commonmode: subtract, per event, the mean of the normalised vector across cells
              (its code: cm = nanmean(dvs, axis=1, keepdims=True); dev = dvs - cm)

Uses the cached events, so no reload.  Every axis is checked for redundancy before the table is read.
"""
import numpy as np, pickle, pathlib, collections, itertools, json, math
CACHE=pathlib.Path("/tmp/osf/v2c4_cache.pkl")
events=pickle.loads(CACHE.read_bytes())
print(f"  缓存 {len(events)} 个事件, {len({e['anim'] for e in events})} 只动物\n")

def compute(post, base_lo, cellnorm, acrossnorm, commonmode, inclusion):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
    for e in events:
        seg=e["seg"][:post].astype(np.float64)
        base=(e["b3060"] if base_lo==60 else e["b060"]).astype(np.float64)
        with np.errstate(all='ignore'):
            d=seg-base[None,:]                                  # (post, ncells)
            if cellnorm:
                s=e["sp"].astype(np.float64); ok=np.isfinite(s)&(s>0)
                d=np.where(ok[None,:], d/s[None,:], np.nan)
            val=np.nansum(d,axis=0)                             # (ncells,)
            if acrossnorm:
                sd=np.nanmedian(np.nanstd(d,axis=0))            # scalar: across-cell SD of the difference
                if np.isfinite(sd) and sd>0: val=val/sd
            if commonmode:
                cm=np.nanmean(val); val=val-cm
        for k,(nm,fl) in enumerate(zip(e["names"], e["flags"])):
            if fl is None: continue
            v=val[k]
            if not np.isfinite(v): continue
            per[e["anim"]]["c" if fl else "u"].append(float(v))
    diffs=[]; n_excl=0
    for i,d_ in per.items():
        if inclusion and (len(d_["c"])<10 or len(d_["u"])<50): n_excl+=1; continue
        if not d_["c"] or not d_["u"]: continue
        diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    if not np.isfinite(s) or s<=0: return None
    return {"n_animals":len(diffs),"n_excluded":n_excl,"diff":float(m),"sd":float(s),
            "d_A":float(m/s),"t":float(m/(s/math.sqrt(len(diffs))))}

# --- redundancy pre-check on a coarse sample before the full table
print("  === 冗余预检（每个新轴单独变化，其余固定）===")
base_cfg=dict(post=24, base_lo=60, cellnorm=False, acrossnorm=False, commonmode=False, inclusion=False)
def dA(**kw):
    c=dict(base_cfg); c.update(kw); r=compute(**c); return round(r["d_A"],6) if r else None
for ax,levels in (("acrossnorm",(False,True)),("commonmode",(False,True))):
    vals=[dA(**{ax:lv}) for lv in levels]
    print(f"    {ax:>12}: {vals}  {'（无冗余）' if len(set(vals))>1 else '（冗余，该轴不构成规格）'}")
print()
print(f"  {'post':>5} {'base':>5} {'cellnorm':>9} {'across':>7} {'commonmode':>11} {'incl':>5} {'n_an':>5} {'d_A':>8} {'t':>7}")
rows=[]
for post,base_lo,cn,an,cm_,inc in itertools.product((12,24,48),(60,0),(False,True),(False,True),(False,True),(False,)):
    r=compute(post,base_lo,cn,an,cm_,inc)
    if r is None: continue
    rows.append({"post":post,"baseline_lo":base_lo,"cellnorm":cn,"acrossnorm":an,
                 "commonmode":cm_,"inclusion":inc,**r})
    print(f"  {post:>5} {base_lo:>5} {str(cn):>9} {str(an):>7} {str(cm_):>11} {str(inc):>5} "
          f"{r['n_animals']:>5} {r['d_A']:>8.4f} {r['t']:>7.2f}")
d=np.array([r["d_A"] for r in rows])
print(f"\n  === 范围 ===")
print(f"    全部 {len(rows)} 个规格: d_A {d.min():.4f} .. {d.max():.4f}   极差 {d.max()-d.min():.4f}")
for cmv in (False,True):
    sub=np.array([r["d_A"] for r in rows if r["commonmode"]==cmv])
    if sub.size: print(f"    共模={'是' if cmv else '否'}: {sub.min():.4f} .. {sub.max():.4f}   (n={sub.size})")
print(f"    V2-C4 报 0.0852 .. 0.7289")
print(f"\n  === 共模那一步的隔离贡献 ===")
for cfg in ((24,60,False,False),(24,60,False,True),(24,60,True,False),(24,60,True,True)):
    post,bl,cn,an=cfg
    a=[r["d_A"] for r in rows if (r["post"],r["baseline_lo"],r["cellnorm"],r["acrossnorm"])==cfg and not r["commonmode"]]
    b=[r["d_A"] for r in rows if (r["post"],r["baseline_lo"],r["cellnorm"],r["acrossnorm"])==cfg and r["commonmode"]]
    if a and b:
        print(f"    post={post} base={bl} cellnorm={cn} across={an}:  无共模 {a[0]:.4f}  有共模 {b[0]:.4f}  "
              f"变化 {b[0]-a[0]:+.4f}")
json.dump(rows, open("/tmp/osf/v2c4_grid3.json","w"), indent=2)
