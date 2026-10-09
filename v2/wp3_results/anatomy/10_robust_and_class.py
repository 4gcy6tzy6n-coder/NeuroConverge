import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
CONN=pathlib.Path("/tmp/ncv2/conn")
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
classes={}
for n_ in json.loads((CONN/"neurons.json").read_text()): classes[n_["name"]]=n_.get("classes") or ""
same=np.zeros((N,N),dtype=bool)
for i,ni in enumerate(ids):
    ci=classes.get(ni)
    if not ci: continue
    for j,nj in enumerate(ids):
        if i!=j and classes.get(nj)==ci: same[i,j]=True
POST=24; SHIFT=60
# Per animal: POOLED pair-level means AND pair-level values for a mixed-model style check
per={}
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
    acc=collections.defaultdict(list)
    with np.errstate(all='ignore'):
        for sv,vi in zip(stim,vols):
            if sv<0 or vi<SHIFT or vi+POST>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            post=G[vi:vi+POST,:]; base=G[vi-30:vi,:]
            b=np.nanmean(base,axis=0); dv=post-b
            sd=np.nanmedian(np.nanstd(dv,axis=1))
            if not np.isfinite(sd) or sd<=0: continue
            dvs=dv/sd; cm=np.nanmean(dvs,axis=1,keepdims=True); dev=dvs-cm
            for c in keep:
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                v=float(dev[:,c].mean())
                if not np.isfinite(v): continue
                if conn[i_,j_]:
                    acc["conn"].append(v)
                    acc["same" if same[i_,j_] else "cross"].append(v)
                    if chem[i_,j_]!=0: acc["chem"].append(v)
                    if gap[i_,j_]!=0:  acc["gap"].append(v)
                else:
                    acc["unconn"].append(v)
                    acc["unconn_same" if same[i_,j_] else "unconn_cross"].append(v)
    if acc["conn"] and acc["unconn"]:
        per[i]={k:(float(np.mean(v)),len(v)) for k,v in acc.items()}
print(f"  动物数 {len(per)}")
keys=set().union(*[set(v) for v in per.values()])
print(f"  每个键的动物覆盖: " + ", ".join(f"{k}={sum(1 for v in per.values() if k in v)}" for k in sorted(keys)))
def paired(key_a, key_b, label):
    d=[]; w=[]
    for i,v in per.items():
        if key_a in v and key_b in v:
            d.append(v[key_a][0]-v[key_b][0]); w.append(min(v[key_a][1],v[key_b][1]))
    if len(d)<15: print(f"    {label}: 动物不足 ({len(d)})"); return None
    d=np.array(d); w=np.array(w,float)
    n=d.size; m=d.mean(); s=d.std(ddof=1); se=s/np.sqrt(n); t=m/se
    # weight by min pair count (precision proxy)
    mw=np.average(d,weights=w); sew=np.sqrt(np.average((d-mw)**2,weights=w)/n); tw=mw/sew
    # cluster-robust style: the animal IS the cluster, so the paired t is already cluster-level.
    return {"label":label,"n":int(n),"diff":float(m),"sd":float(s),"se":float(se),"t":float(t),
            "d":float(m/s),"wt_diff":float(mw),"wt_se":float(sew),"wt_t":float(tw)}
res={}
print("\n  === 动物级配对对比 ===")
for a,b,lab_ in (("conn","unconn","连接 vs 未连接"),("chem","unconn","化学 vs 未连接"),
                 ("gap","unconn","缝隙 vs 未连接"),("same","unconn_same","同类: 连接 vs 未连接"),
                 ("cross","unconn_cross","跨类: 连接 vs 未连接"),
                 ("same","cross","同类连接 vs 跨类连接")):
    r=paired(a,b,lab_)
    if r:
        res[lab_]=r
        print(f"    {lab_:>22}: n={r['n']:>3}  差 {r['diff']:+.5f}  d={r['d']:.4f}  t={r['t']:.3f}   "
              f"(加权: 差 {r['wt_diff']:+.5f} t={r['wt_t']:.3f})")
# intraclass correlation of the per-animal means, as a check on whether the animal mean is well estimated
print("\n  === 动物均值的精度检查 ===")
for k in ("conn","unconn"):
    ns=[per[i][k][1] for i in per if k in per[i]]
    print(f"    {k}: 每动物配对数 中位 {np.median(ns):.0f}  范围 {min(ns)}..{max(ns)}")
# how much of the across-animal variance is explained by pair count?  (precision weighting matters if so)
d=np.array([per[i]["conn"][0]-per[i]["unconn"][0] for i in per])
nc=np.array([per[i]["conn"][1] for i in per],float)
print(f"    corr(配对差, 连接配对数) = {np.corrcoef(d,nc)[0,1]:+.4f}")
json.dump(res, open("/tmp/osf/robust.json","w"), indent=2)
