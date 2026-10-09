import numpy as np, pathlib, re, collections, json
d = pathlib.Path("/tmp/osf/w/exported_data")
ids = sorted({int(m.group(1)) for p in d.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))})
PRE=POST=8
# Collect per-animal: for each stimulus event, the response vector over uniquely-named cells.
# Then z-score THE EVENT RESPONSE VECTOR within the animal (removes animal-level scale/offset).
per_pair = collections.defaultdict(list)          # (target,rec) -> [(animal, z)]
per_pair_raw = collections.defaultdict(list)
n_an=0; used=0
for i in ids:
    gp,lp,sp,vp = (d/f"{i}_gcamp.txt", d/f"{i}_labels.txt", d/f"{i}_stim_neurons.txt", d/f"{i}_stim_volume_i.txt")
    if not all(p.exists() for p in (gp,lp,sp,vp)): continue
    try: G=np.loadtxt(gp)
    except Exception: continue
    lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
    stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
    T,ncol=G.shape
    if len(stim)!=len(vols): continue
    n_an+=1
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*", x or ""))
    uniq={name for name,c in cnt.items() if c==1}
    keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
    if not keep: continue
    used+=1
    with np.errstate(all='ignore'):
        for sv,vi in zip(stim,vols):
            if sv<0 or vi>=T or vi<PRE: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            post=np.nanmean(G[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
            dv=post-pre
            v=dv[keep]
            m=np.nanmean(v); s=np.nanstd(v)
            if not np.isfinite(s) or s==0: continue
            z=(v-m)/s                                   # <-- within-event, within-animal standardisation
            for kk,c in enumerate(keep):
                if not np.isfinite(z[kk]): continue
                per_pair[(lab[sv],lab[c])].append((i,float(z[kk])))
                per_pair_raw[(lab[sv],lab[c])].append((i,float(dv[c])))
out={"n_animals_scanned":n_an,"n_animals_used":used,
     "n_pairs":len(per_pair),"n_meas":sum(len(v) for v in per_pair.values())}
rng=np.random.default_rng(0)
def splithalf(pp, minm):
    xs=[];ys=[]
    for k,v in pp.items():
        if len(v)<minm: continue
        idx=rng.permutation(len(v)); h=len(v)//2
        xs.append(np.mean([v[j][1] for j in idx[:h]])); ys.append(np.mean([v[j][1] for j in idx[h:]]))
    if len(xs)<50: return None,None,len(xs)
    r=np.corrcoef(xs,ys)[0,1]
    return float(r), float(2*r/(1+r)), len(xs)
print("  === A) 逐事件 z 标准化后（去动物层面尺度/偏移）===")
for m in (4,6,10,20):
    r,rf,n = splithalf(per_pair, m)
    out[f"Z_split_r_min{m}"]=r; out[f"Z_split_rfull_min{m}"]=rf; out[f"Z_n_min{m}"]=n
    print(f"    >= {m:>2} 次: r={r if r is None else round(r,4)}  r_full={rf if rf is None else round(rf,4)}  n={n:,}")
print()
print("  === B) 未标准化（对照，即上一次的结果）===")
for m in (4,10):
    r,rf,n = splithalf(per_pair_raw, m)
    print(f"    >= {m:>2} 次: r={round(r,4)}  r_full={round(rf,4)}  n={n:,}")
print()
# variance components after z-scoring
allv=[np.array([x[1] for x in v]) for v in per_pair.values() if len(v)>=3]
out["Z_within_var"]=float(np.mean([np.var(a) for a in allv]))
out["Z_between_var"]=float(np.var([a.mean() for a in allv]))
out["Z_between_frac"]=out["Z_between_var"]/(out["Z_within_var"]+out["Z_between_var"])
print(f"  === C) z 标准化后的方差成分 ===")
print(f"    测量内 {out['Z_within_var']:.4f}   配对间 {out['Z_between_var']:.4f}   配对间占比 {out['Z_between_frac']:.4f}")
pathlib.Path("/tmp/osf/reliab3.json").write_text(json.dumps(out,indent=2))
