import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
conn=pathlib.Path("/tmp/ncv2/conn")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
PRE=8
WINDOWS=[2,4,8,16,32]          # post-stimulus windows in volumes (dt = 0.5 s)
# anatomical
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
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool)
# cell classes from the NemaNode neurons.json already downloaded
classes={}
try:
    import json as J
    for n in J.loads((conn/"neurons.json").read_text()):
        classes[n["name"]]=n.get("classes") or ""
    print(f"  cell classes: {len(classes)} 个名字有类别")
except Exception as e:
    print(f"  !! 类别文件不可读: {e}")

# functional: accumulate per (target,record) per window
per=collections.defaultdict(lambda: collections.defaultdict(list))
n_an=0
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
            if sv<0 or vi>=T or vi<PRE: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
            for W in WINDOWS:
                if vi+W>T: continue
                post=np.nanmean(G[vi:vi+W,:],axis=0)
                dv=post-pre; v=dv[keep]; mu=np.nanmean(v); sd=np.nanstd(v)
                if not np.isfinite(sd) or sd==0: continue
                z=(v-mu)/sd
                for kk,c in enumerate(keep):
                    if np.isfinite(z[kk]): per[(lab[sv],lab[c])][W].append(float(z[kk]))
print(f"  功能侧: {n_an} 只动物, {len(per):,} 配对")
res={"n_animals":n_an,"n_pairs":len(per),"windows_volumes":WINDOWS,"dt_s":0.5}
print("\n  === 时间尺度检验：关联强度随刺激后窗口变化 ===")
print(f"  {'window(s)':>10} {'pair n':>8} {'chem d':>9} {'gap d':>9} {'gap/chem':>9}")
for W in WINDOWS:
    Fm=np.full((N,N),np.nan)
    for (tg,rc),d in per.items():
        if W in d and tg in idx and rc in idx:
            Fm[idx[tg],idx[rc]]=np.mean(d[W])
    have=np.isfinite(Fm)&off
    out={}
    for tag,cm in (("chem",(chem!=0)&off),("gap",(gap!=0)&off)):
        a=have&cm; b=have&~cm
        if a.sum()<50: out[tag]=None; continue
        d=Fm[a].mean()-Fm[b].mean(); se=np.sqrt(Fm[a].var()/a.sum()+Fm[b].var()/b.sum())
        out[tag]={"n_conn":int(a.sum()),"diff":float(d),"d":float(d/se)}
    res[f"W{W}"]={"n_have":int(have.sum()),**out}
    cd = out["chem"]["d"] if out["chem"] else float('nan')
    gd = out["gap"]["d"] if out["gap"] else float('nan')
    print(f"  {W*0.5:>10.1f} {int(have.sum()):>8} {cd:>9.3f} {gd:>9.3f} {gd/cd if cd else float('nan'):>9.2f}")
print()
print("    判读: 若化学关联随窗口拉长而增强 => 存在时间尺度解释；若各窗口都弱 => 化学层在此读数下确实弱")

# ---------- cell-class control on the 8-volume window ----------
print("\n  === 细胞类控制 (8 卷窗口) ===")
Fm=np.full((N,N),np.nan)
for (tg,rc),d in per.items():
    if 8 in d and tg in idx and rc in idx: Fm[idx[tg],idx[rc]]=np.mean(d[8])
have=np.isfinite(Fm)&off
sameclass=np.zeros((N,N),dtype=bool)
n_known=0
for i,ni in enumerate(ids):
    ci=classes.get(ni)
    if not ci: continue
    n_known+=1
    for j,nj in enumerate(ids):
        if i==j: continue
        if classes.get(nj)==ci: sameclass[i,j]=True
print(f"  有类别的 id: {n_known}/300   同类配对总数 {int(sameclass.sum()):,}")
for tag,cm in (("chem",(chem!=0)&off),("gap",(gap!=0)&off)):
    a=have&cm
    if a.sum()<50: continue
    sc=a&sameclass; dc=a&~sameclass
    b=have&~cm
    print(f"    {tag}: 连接 {int(a.sum())}  其中同类 {int(sc.sum())} ({100*sc.sum()/a.sum():.1f}%)")
    # class-matched contrast: connected vs unconnected, both restricted to same-class pairs
    cs=have&cm&sameclass; cu=have&~cm&sameclass
    if cs.sum()>30 and cu.sum()>30:
        d=Fm[cs].mean()-Fm[cu].mean(); se=np.sqrt(Fm[cs].var()/cs.sum()+Fm[cu].var()/cu.sum())
        res[f"class_matched_{tag}"]={"n_conn":int(cs.sum()),"n_unconn":int(cu.sum()),"diff":float(d),"d":float(d/se)}
        print(f"       同类内对比: 连接 {int(cs.sum())} vs 未连接 {int(cu.sum())}  差 {d:+.4f}  d={d/se:.3f}")
    # cross-class contrast
    xs=have&cm&~sameclass; xu=have&~cm&~sameclass
    if xs.sum()>30 and xu.sum()>30:
        d=Fm[xs].mean()-Fm[xu].mean(); se=np.sqrt(Fm[xs].var()/xs.sum()+Fm[xu].var()/xu.sum())
        res[f"crossclass_{tag}"]={"n_conn":int(xs.sum()),"n_unconn":int(xu.sum()),"diff":float(d),"d":float(d/se)}
        print(f"       跨类内对比: 连接 {int(xs.sum())} vs 未连接 {int(xu.sum())}  差 {d:+.4f}  d={d/se:.3f}")
json.dump(res, open("/tmp/osf/timescale_class.json","w"), indent=2)
