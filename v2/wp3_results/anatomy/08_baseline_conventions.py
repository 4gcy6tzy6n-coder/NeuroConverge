import numpy as np, h5py, csv, pathlib, re, collections, json
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

# Three baseline conventions, identical post-window (24 volumes = 12 s), so only the baseline differs.
#   SRC  : shift_vol=60, baseline = volumes 30..60   (the source's own choice)
#   SHORT: shift_vol=8,  baseline = volumes 0..8     (what this audit used)
#   FULL : shift_vol=60, baseline = volumes 0..60
MODES=("SRC","SHORT","FULL")
acc={m:{k:[] for k in ("conn","unconn","chem","gap")} for m in MODES}
n_an=0; n_ev=0
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
            if sv<0 or vi<60 or vi+24>=T: continue          # need the FULL 60-volume history
            if not (sv<len(lab) and lab[sv] in uniq): continue
            n_ev+=1
            post=G[vi:vi+24,:]
            base={"SRC":G[vi-30:vi,:], "SHORT":G[vi-8:vi,:], "FULL":G[vi-60:vi,:]}
            for m in MODES:
                b=np.nanmean(base[m],axis=0)
                dv=post-b
                sd=np.nanmedian(np.nanstd(dv,axis=1))
                if not np.isfinite(sd) or sd<=0: continue
                dvs=dv/sd
                cm=np.nanmean(dvs,axis=1,keepdims=True)
                dev=dvs-cm
                for c in keep:
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    if i_ is None or j_ is None: continue
                    val=float(dev[:,c].mean())
                    if not np.isfinite(val): continue
                    k="conn" if conn[i_,j_] else "unconn"
                    acc[m][k].append(val)
                    if conn[i_,j_]:
                        if chem[i_,j_]!=0: acc[m]["chem"].append(val)
                        if gap[i_,j_]!=0:  acc[m]["gap"].append(val)
print(f"  {n_an} 只动物, {n_ev:,} 次事件（要求事件前有完整 60 体历史）")
out={"n_animals":n_an,"n_events":n_ev}
for m in MODES:
    print(f"\n  === 基线约定 {m} ===")
    print(f"  {'层':>10} {'n':>8} {'均值':>10} {'d vs unconn':>12}")
    base=np.array(acc[m]["unconn"]); out[m]={"unconn":{"n":int(base.size),"mean":float(base.mean())}}
    print(f"  {'unconn':>10} {base.size:>8} {base.mean():>10.5f} {'-':>12}")
    for k in ("chem","gap","conn"):
        a=np.array(acc[m][k])
        if a.size<30: continue
        d=a.mean()-base.mean(); se=np.sqrt(a.var()/a.size+base.var()/base.size)
        out[m][k]={"n":int(a.size),"mean":float(a.mean()),"diff":float(d),"d":float(d/se)}
        print(f"  {k:>10} {a.size:>8} {a.mean():>10.5f} {d/se:>12.3f}")
# time course under each baseline, first 24 volumes
print(f"\n  === 时间过程对比（前 12 体 = 6 秒，连接 vs 未连接）===")
print(f"  {'vol':>4} " + " ".join(f"{m+'_conn':>10} {m+'_unc':>10}" for m in MODES))
out["timecourse"]={}
for m in MODES:
    A=np.array([x for x in acc[m]["conn"] if True]); 
for m in MODES:
    pass
json.dump(out, open("/tmp/osf/roottest.json","w"), indent=2)
