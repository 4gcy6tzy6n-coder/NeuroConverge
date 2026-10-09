"""The correct per-volume common-mode removal, and whether it reaches 0.7289.

Round 32 found that this grid's common-mode axis tested the WRONG operation.  This grid subtracted one scalar
per event -- the across-cell mean of the volume-summed values.  The code in 09_animal_level.py subtracts the
across-cell mean AT EACH VOLUME and only then averages over volumes:

    dv   = post - baseline                     (POST volumes, cells)   -- a 2-D array
    dvs  = dv / sd                             (sd is a scalar and cancels in d_A)
    cm   = nanmean(dvs, axis=1, keepdims=True)  -- across cells, PER VOLUME
    dev  = dvs - cm
    v_c  = dev[:, c].mean()                    -- then average over volumes

That is a stronger operation than removing one scalar, and it is the step this grid must vary to isolate the
contribution correctly.  This runs it.
"""
import numpy as np, pickle, pathlib, collections, itertools, json, math
events=pickle.loads(pathlib.Path("/tmp/osf/v2c4_cache.pkl").read_bytes())
print(f"  缓存 {len(events)} 个事件, {len({e['anim'] for e in events})} 只动物\n")

def compute(post, base_lo, cellnorm, commonmode_volume, commonmode_scalar, inclusion):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
    for e in events:
        seg=e["seg"][:post].astype(np.float64)                    # (post, ncells)
        base=(e["b3060"] if base_lo==60 else e["b060"]).astype(np.float64)
        with np.errstate(all='ignore'):
            d=seg-base[None,:]                                    # (post, ncells)
            if cellnorm:
                s=e["sp"].astype(np.float64); ok=np.isfinite(s)&(s>0)
                d=np.where(ok[None,:], d/s[None,:], np.nan)
            if commonmode_volume:
                # the code's operation: across-cell mean PER VOLUME, subtracted before averaging
                cmv=np.nanmean(d,axis=1,keepdims=True)
                d=d-cmv
            val=np.nanmean(d,axis=0)                              # (ncells,)  average over volumes
            if commonmode_scalar:
                val=val-np.nanmean(val)                           # one scalar per event
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
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),
            "d_A":float(m/s),"t":float(m/(s/math.sqrt(len(diffs))))}

print(f"  {'post':>5} {'base':>5} {'cellnorm':>9} {'cm_vol':>7} {'cm_scal':>8} {'d_A':>8} {'t':>7}   （09_animal_level 用 post=24 base=30..60 cm_vol=True）")
rows=[]
for post,base_lo,cn,cmv,cms in itertools.product((12,24,48),(60,0),(False,True),(False,True),(False,True)):
    r=compute(post,base_lo,cn,cmv,cms,False)
    if r is None: continue
    rows.append({"post":post,"baseline_lo":base_lo,"cellnorm":cn,"cm_volume":cmv,"cm_scalar":cms,**r})
    mark=" <== 代码的配置" if (post==24 and base_lo==60 and not cn and cmv and not cms) else ""
    print(f"  {post:>5} {base_lo:>5} {str(cn):>9} {str(cmv):>7} {str(cms):>8} {r['d_A']:>8.4f} {r['t']:>7.2f}{mark}")
d=np.array([r["d_A"] for r in rows])
print(f"\n  === 范围 ===")
print(f"    全部 {len(rows)} 规格: {d.min():.4f} .. {d.max():.4f}   极差 {d.max()-d.min():.4f}")
for cmv in (False,True):
    sub=np.array([r["d_A"] for r in rows if r["cm_volume"]==cmv])
    print(f"    逐体积共模={'是' if cmv else '否'}: {sub.min():.4f} .. {sub.max():.4f}   (n={sub.size})")
print(f"    V2-C4 报 0.0852 .. 0.7289 ; 09_animal_level 的值是 0.7289")
code=[r for r in rows if r["post"]==24 and r["baseline_lo"]==60 and not r["cellnorm"] and r["cm_volume"] and not r["cm_scalar"]]
if code:
    c=code[0]
    print(f"\n  === 与代码的配置对照 ===")
    print(f"    本网格该配置: d_A {c['d_A']:.4f}  t {c['t']:.4f}  n {c['n_animals']}")
    print(f"    代码报的是  : d_A 0.7289  t 7.610  n 109")
    _diff = abs(c["d_A"] - 0.7289)
    _verdict = "reproduced" if _diff < 0.02 else ("differs by %.4f, so steps remain unreproduced" % _diff)
    print(f"    ==> {_verdict}")
print(f"\n  === 逐体积共模的隔离贡献 ===")
for cfg in ((24,60,False),(24,60,True),(48,0,False)):
    post,bl,cn=cfg
    a=[r["d_A"] for r in rows if (r["post"],r["baseline_lo"],r["cellnorm"])==cfg and not r["cm_volume"] and not r["cm_scalar"]]
    b=[r["d_A"] for r in rows if (r["post"],r["baseline_lo"],r["cellnorm"])==cfg and r["cm_volume"] and not r["cm_scalar"]]
    if a and b: print(f"    post={post} base={bl} cellnorm={cn}:  无 {a[0]:.4f} -> 有 {b[0]:.4f}   变化 {b[0]-a[0]:+.4f}")
json.dump(rows, open("/tmp/osf/v2c4_grid4.json","w"), indent=2)
