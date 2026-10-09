"""Are the specification dimensions additive, or do they interact?

SPECIFICATION_LEDGER.md reports each dimension's ISOLATED size, measured by varying that dimension alone and
holding the others fixed.  Two dimensions have nearly equal isolated sizes: per-cell normalisation at 0.3395
and the per-event weighting at 0.3356.  If they interact, the ledger's single-number column is misleading and
a reader adding two rows would get the wrong answer.

This runs them jointly with the post-stimulus window, from the cached all-columns events, and reports
isolated sizes alongside the joint effect so additivity can be tested rather than assumed.

Uses v2c4_pool_cache.pkl: per event, seg (48 volumes x all columns), base, sp, isuniq, conn.
"""
import numpy as np, pickle, pathlib, collections, itertools, json, math
events=pickle.loads(pathlib.Path("/tmp/osf/v2c4_pool_cache.pkl").read_bytes())
print(f"  缓存 {len(events)} 个事件, {len({e['anim'] for e in events})} 只动物, "
      f"列 {len(events[0]['isuniq'])} 其中唯一名 {int(events[0]['isuniq'].sum())}\n")

def compute(post, cellnorm, weighted):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
    for e in events:
        seg=e["seg"][:post].astype(np.float64); base=e["base"].astype(np.float64)
        uq=e["isuniq"]; fl=e["conn"]
        with np.errstate(all='ignore'):
            d=seg-base[None,:]
            if cellnorm:
                s=e["sp"].astype(np.float64); ok=np.isfinite(s)&(s>0)
                d=np.where(ok[None,:], d/s[None,:], np.nan)
            if weighted:
                sd=np.nanmedian(np.nanstd(d,axis=0))          # the code's: median over VOLUMES of across-cell SD
                if not np.isfinite(sd) or sd<=0: continue
                d=d/sd
            cm=np.nanmean(d,axis=1,keepdims=True); dev=d-cm   # per-volume common mode, as the code
            val=np.nanmean(dev,axis=0)
        for k in range(val.shape[0]):
            if not uq[k] or fl[k]<0: continue
            v=val[k]
            if not np.isfinite(v): continue
            per[e["anim"]]["c" if fl[k]==1 else "u"].append(float(v))
    diffs=[]
    for i,d_ in per.items():
        if d_["c"] and d_["u"]: diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}
print(f"  {'post':>5} {'cellnorm':>9} {'weighted':>9} {'n_an':>6} {'d_A':>8} {'t':>7}")
rows={}
for post,cn,w in itertools.product((12,24,48),(False,True),(False,True)):
    r=compute(post,cn,w)
    if r is None: print(f"  {post:>5} {str(cn):>9} {str(w):>9}  -- 不足"); continue
    rows[(post,cn,w)]=r
    print(f"  {post:>5} {str(cn):>9} {str(w):>9} {r['n_animals']:>6} {r['d_A']:>8.4f} {r['t']:>7.3f}")
print(f"\n  === 可加性检验（在 post=24 上）===")
b=rows.get((24,False,False)); c=rows.get((24,True,False)); w=rows.get((24,False,True)); j=rows.get((24,True,True))
if all(x is not None for x in (b,c,w,j)):
    iso_c=c["d_A"]-b["d_A"]; iso_w=w["d_A"]-b["d_A"]; joint=j["d_A"]-b["d_A"]
    print(f"    基线 (无标准化, 无加权)        d_A = {b['d_A']:.4f}")
    print(f"    仅逐细胞标准化                 d_A = {c['d_A']:.4f}   孤立贡献 {iso_c:+.4f}")
    print(f"    仅逐事件加权                   d_A = {w['d_A']:.4f}   孤立贡献 {iso_w:+.4f}")
    print(f"    两者同时                       d_A = {j['d_A']:.4f}   联合贡献 {joint:+.4f}")
    print(f"    可加性预言 (孤立之和)                        {iso_c+iso_w:+.4f}")
    print(f"    交互项 (联合 - 孤立之和)                     {joint-(iso_c+iso_w):+.4f}")
    print(f"    交互占联合的比例                             {100*(joint-(iso_c+iso_w))/joint if joint else float('nan'):.1f}%")
    print(f"    ==> {'近似可加（偏差 < 10%）' if abs(joint-(iso_c+iso_w)) < 0.1*abs(joint) else '**存在实质交互**'}")
print(f"\n  === 同一检验在 post=12 与 post=48 上 ===")
for post in (12,48):
    b=rows.get((post,False,False)); c=rows.get((post,True,False)); w=rows.get((post,False,True)); j=rows.get((post,True,True))
    if all(x is not None for x in (b,c,w,j)):
        ic=c["d_A"]-b["d_A"]; iw=w["d_A"]-b["d_A"]; jo=j["d_A"]-b["d_A"]
        print(f"    post={post}: 孤立和 {ic+iw:+.4f}   联合 {jo:+.4f}   交互 {jo-(ic+iw):+.4f}")
print(f"\n  === 全部 d_A 的范围 ===")
d=[r["d_A"] for r in rows.values()]
print(f"    {min(d):.4f} .. {max(d):.4f}   极差 {max(d)-min(d):.4f}")
json.dump({f"{k[0]}|{k[1]}|{k[2]}":v for k,v in rows.items()}, open("/tmp/osf/joint_grid.json","w"), indent=2)
