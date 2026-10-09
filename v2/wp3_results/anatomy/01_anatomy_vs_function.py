import numpy as np, h5py, csv, pathlib, re, collections, json
DATA = pathlib.Path("/tmp/osf/w/exported_data")
WNA  = pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f = h5py.File(WNA/"funatlas.h5","r")
ids = [x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx = {n:i for i,n in enumerate(ids)}
N=len(ids)

# ---------- anatomical matrices built BY NAME from the source CSVs ----------
def build(fname):
    C=np.zeros((N,N)); G=np.zeros((N,N)); unk=0
    with open(WNA/fname, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            p,q=r["pre"],r["post"]
            if p not in idx or q not in idx: unk+=1; continue
            s=float(r["synapses"]); i,j=idx[p],idx[q]
            if r["type"]=="chemical":
                C[i,j]+=s
                if (C==0).all(): pass
            elif r["type"]=="electrical":
                G[i,j]+=s; G[j,i]+=s
            else: unk+=1
    return C,G,unk
chem, gap, unk = build("aconnectome_witvliet_2020_8.csv")
print(f"  witvliet_2020_8 按名构建: chem 非零 {int((chem!=0).sum())}  gap 非零 {int((gap!=0).sum())}  名字不在 funatlas 的边 {unk}")
chem2, gap2, unk2 = build("aconnectome_white_1986_whole.csv")
print(f"  white_1986_whole 按名构建: chem 非零 {int((chem2!=0).sum())}  gap 非零 {int((gap2!=0).sum())}  名字不在 funatlas 的边 {unk2}")

# ---------- functional side ----------
PRE=POST=8
per_pair=collections.defaultdict(list)
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
            post=np.nanmean(G[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
            dv=post-pre; v=dv[keep]; m=np.nanmean(v); s=np.nanstd(v)
            if not np.isfinite(s) or s==0: continue
            z=(v-m)/s
            for kk,c in enumerate(keep):
                if np.isfinite(z[kk]): per_pair[(lab[sv],lab[c])].append((i,float(z[kk])))

# reliability per pair (split-half on >=4) AND mean response
rng=np.random.default_rng(0)
Fm=np.full((N,N),np.nan); rel=np.full((N,N),np.nan); nn=np.zeros((N,N),int)
for (tg,rc),v in per_pair.items():
    if tg not in idx or rc not in idx: continue
    i,j=idx[tg],idx[rc]; a=np.array([x[1] for x in v]); Fm[i,j]=a.mean(); nn[i,j]=len(a)
    if len(a)>=4:
        o=rng.permutation(len(a)); h=len(a)//2
        rel[i,j]=1.0 if len(a)<6 else None
# pair-level reliability with Spearman-Brown, using the same split
for (tg,rc),v in per_pair.items():
    if tg not in idx or rc not in idx: continue
    i,j=idx[tg],idx[rc]
    a=np.array([x[1] for x in v])
    if len(a)<4: continue
    o=rng.permutation(len(a)); h=len(a)//2
    # reliability of a SINGLE measurement is not identifiable per pair; use measurement count as the weight
    rel[i,j]=len(a)
np.save("/tmp/osf/Fm2.npy",Fm); np.save("/tmp/osf/rel2.npy",rel); np.save("/tmp/osf/nn2.npy",nn)
np.save("/tmp/osf/chem.npy",chem); np.save("/tmp/osf/gap.npy",gap)

off = ~np.eye(N,dtype=bool)
have = np.isfinite(Fm) & off
connected = ((chem!=0)|(gap!=0)) & off
print(f"\n  功能侧: {n_an} 只动物, 有名配对 {int(have.sum()):,}")
print(f"  有解剖连接的功能配对: {int((have&connected).sum()):,}   无连接: {int((have&~connected).sum()):,}")

def compare(mask_conn, label, w=None):
    m1 = Fm[have & mask_conn]; m0 = Fm[have & ~mask_conn]
    if w is None:
        d = m1.mean()-m0.mean()
        sp = np.sqrt(m1.var()/m1.size + m0.var()/m0.size)
        return label, float(m1.mean()), float(m0.mean()), float(d), float(d/sp), int(m1.size), int(m0.size)
    # weighted by reliability (measurement count)
    w1 = w[have & mask_conn]; w0 = w[have & ~mask_conn]
    d = np.average(m1,weights=w1) - np.average(m0,weights=w0)
    return label, float(np.average(m1,weights=w1)), float(np.average(m0,weights=w0)), float(d), float('nan'), int(m1.size), int(m0.size)
res={}
for tag, cm in (("chem_or_gap",connected), ("chem_only",(chem!=0)&off), ("gap_only",(gap!=0)&off)):
    r=compare(cm,tag); res[tag+"_unweighted"]={"conn":r[1],"unconn":r[2],"diff":r[3],"d":r[4],"n_conn":r[5],"n_unconn":r[6]}
    print(f"\n  === {tag} ===")
    print(f"    有连接 {r[1]:+.4f} (n={r[5]:,})   无连接 {r[2]:+.4f} (n={r[6]:,})   差 {r[3]:+.4f}   Cohen's d {r[4]:.4f}")
    nw = np.where(np.isfinite(rel), rel, 0)
    r2=compare(cm,tag+"_w",w=nw)
    res[tag+"_weighted_by_nmeas"]={"conn":r2[1],"unconn":r2[2],"diff":r2[3],"n_conn":r2[5],"n_unconn":r2[6]}
    print(f"    按测量次数加权: 有连接 {r2[1]:+.4f}   无连接 {r2[2]:+.4f}   差 {r2[3]:+.4f}")
    hi = (nn>=10)&have
    m1=Fm[hi&cm]; m0=Fm[hi&~cm]
    if m1.size>50 and m0.size>50:
        dd=m1.mean()-m0.mean(); sp=np.sqrt(m1.var()/m1.size+m0.var()/m0.size)
        res[tag+"_only_wellmeasured"]={"conn":float(m1.mean()),"unconn":float(m0.mean()),"diff":float(dd),"d":float(dd/sp),"n_conn":int(m1.size),"n_unconn":int(m0.size)}
        print(f"    仅 >=10 次测量的配对: 有连接 {m1.mean():+.4f} (n={m1.size:,})  无连接 {m0.mean():+.4f} (n={m0.size:,})  差 {dd:+.4f}  d {dd/sp:.4f}")
json.dump(res, open("/tmp/osf/anatomy_test2.json","w"), indent=2)
