"""The cell-pool dimension, varied directly. Settles round 32's claim.

09_animal_level.py computes its across-cell common mode over ALL columns and only then selects the
uniquely-named subset for the effect.  The earlier grids cached only the uniquely-named columns, so their
common mode spanned ~46 cells instead of ~114, and at the code's own configuration they gave d_A 0.3895
against the code's 0.7289 -- a difference of 0.3394.

This re-caches the events over ALL columns, with per-column names, a uniqueness flag and a connection flag,
so the common mode's pool can be varied directly while the EFFECT stays over uniquely-named cells as the code
does.

Pools tested:  all columns  |  uniquely-named columns only

If "all" reproduces 0.7289 and "unique" does not, the cell pool is the explanation and round 32 is confirmed.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, math, pickle
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
CACHE=pathlib.Path("/tmp/osf/v2c4_pool_cache.pkl")
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
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool); CONN=((chem!=0)|(gap!=0))&off
if not CACHE.exists():
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
        if len(stim)!=len(vols) or ncol==0: continue
        cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
        uniq={n for n,c in cnt.items() if c==1}
        names=[(lab[c] if c<len(lab) else "") for c in range(ncol)]
        isuniq=np.array([bool(nm and nm in uniq) for nm in names],dtype=bool)
        # per-column connection flag, only meaningful for uniquely-named cells
        connflag=np.full(ncol,-1,dtype=np.int8)
        for k,nm in enumerate(names):
            i_=idx.get(nm)
            connflag[k]=-1 if i_ is None else 0
        n_an+=1
        with np.errstate(all='ignore'):
            for sv,vi in zip(stim,vols):
                if sv<0 or vi<60 or vi+48>=T: continue
                if not (sv<len(lab) and 0<=sv<ncol and lab[sv] in uniq): continue
                tg=lab[sv]; ti=idx.get(tg)
                flags=np.full(ncol,-1,dtype=np.int8)
                if ti is not None:
                    for k,nm in enumerate(names):
                        if not isuniq[k]: continue
                        j_=idx.get(nm)
                        flags[k]=-1 if j_ is None else (1 if CONN[ti,j_] else 0)
                seg=G[vi:vi+48,:]; base=np.nanmean(G[vi-30:vi,:],axis=0); spd=np.nanstd(G[vi-60:vi,:],axis=0)
                events.append({"anim":i,"seg":seg.astype(np.float32),"base":base.astype(np.float32),
                               "sp":spd.astype(np.float32),"isuniq":isuniq,"conn":flags})
    pickle.dump(events, CACHE.open("wb")); print(f"  已缓存 {len(events)} 个事件（全部列 + 连接标志）")
else:
    events=pickle.loads(CACHE.read_bytes()); print(f"  从缓存载入 {len(events)} 个事件")
print(f"  动物数 {len({e['anim'] for e in events})}   列数 {len(events[0]['isuniq'])}   唯一名 {int(events[0]['isuniq'].sum())}\n")

def compute(post, pool, cellnorm, cm_volume):
    per=collections.defaultdict(lambda: {"c":[], "u":[]})
    for e in events:
        seg=e["seg"][:post].astype(np.float64); base=e["base"].astype(np.float64)
        uq=e["isuniq"]; fl=e["conn"]
        with np.errstate(all='ignore'):
            d=seg-base[None,:]
            if cellnorm:
                s=e["sp"].astype(np.float64); ok=np.isfinite(s)&(s>0)
                d=np.where(ok[None,:], d/s[None,:], np.nan)
            if cm_volume:
                mask = uq if pool=="unique" else np.ones(d.shape[1],dtype=bool)
                if mask.sum()>1:
                    cmv=np.nanmean(d[:,mask],axis=1,keepdims=True)   # per volume, over the POOL
                    d=d-cmv
            val=np.nanmean(d,axis=0)
        for k in range(d.shape[1]):
            if not uq[k] or fl[k]<0: continue
            v=val[k]
            if not np.isfinite(v): continue
            per[e["anim"]]["c" if fl[k]==1 else "u"].append(float(v))
    diffs=[]
    for i,d_ in per.items():
        if not d_["c"] or not d_["u"]: continue
        diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    if not np.isfinite(s) or s<=0: return None
    return {"n_animals":len(diffs),"diff":float(m),"sd":float(s),"d_A":float(m/s),
            "t":float(m/(s/math.sqrt(len(diffs))))}

print(f"  {'post':>5} {'pool':>8} {'cellnorm':>9} {'cm_vol':>7} {'n_an':>5} {'d_A':>8} {'t':>7}")
rows=[]
for post,pool,cn,cmv in ((24,"all",False,True),(24,"unique",False,True),(24,"all",False,False),
                         (24,"unique",False,False),(24,"all",True,True),(48,"all",False,True)):
    r=compute(post,pool,cn,cmv)
    if r is None: print(f"  {post:>5} {pool:>8} {str(cn):>9} {str(cmv):>7}  -- 动物不足"); continue
    rows.append({"post":post,"pool":pool,"cellnorm":cn,"cm_volume":cmv,**r})
    print(f"  {post:>5} {pool:>8} {str(cn):>9} {str(cmv):>7} {r['n_animals']:>5} {r['d_A']:>8.4f} {r['t']:>7.2f}")
print(f"\n  === 结案检验 ===")
code=[r for r in rows if (r["post"],r["pool"],r["cellnorm"],r["cm_volume"])==(24,"all",False,True)]
uni =[r for r in rows if (r["post"],r["pool"],r["cellnorm"],r["cm_volume"])==(24,"unique",False,True)]
if code:
    c=code[0]; gap_=abs(c["d_A"]-0.7289)
    print(f"    pool=all  , 代码的配置: d_A {c['d_A']:.4f}   t {c['t']:.4f}   n {c['n_animals']}")
    print(f"    代码报的是             : d_A 0.7289   t 7.610   n 109")
    print(f"    ==> {'复现' if gap_<0.02 else '差 %.4f' % gap_}")
if uni:
    u=uni[0]
    print(f"    pool=unique（旧网格）  : d_A {u['d_A']:.4f}")
    if code: print(f"    细胞池的贡献            : {code[0]['d_A']-u['d_A']:+.4f}")
json.dump(rows, open("/tmp/osf/v2c4_pool.json","w"), indent=2)
