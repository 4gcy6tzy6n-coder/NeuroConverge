"""Instrumented single-animal comparison: where does the grid diverge from the code?

The original 09_animal_level.py reproduces d = 0.7289, so the grid differs from it somewhere not visible on
reading.  This runs both pipelines on ONE animal, step by step, on the SAME events, and reports the first
place their per-cell values differ.
"""
import numpy as np, h5py, csv, pathlib, re, collections
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
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool); CONN=((chem!=0)|(gap!=0))&off
POST=24; SHIFT=60
i=0   # animal 0
gp,lp,sp,vp=(DATA/f"{i}_gcamp.txt",DATA/f"{i}_labels.txt",DATA/f"{i}_stim_neurons.txt",DATA/f"{i}_stim_volume_i.txt")
G=np.loadtxt(gp); lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
T,ncol=G.shape
cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
uniq={n for n,c in cnt.items() if c==1}
keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
print(f"  动物 {i}: G {G.shape}  T={T}  ncol={ncol}  len(lab)={len(lab)}")
print(f"  keep {len(keep)} 列 (范围 {min(keep)}..{max(keep)})   stim 事件 {len(stim)}\n")
# --- pipeline A: the code, verbatim
A=collections.defaultdict(list); nA=0
with np.errstate(all='ignore'):
    for sv,vi in zip(stim,vols):
        if sv<0 or vi<SHIFT or vi+POST>=T: continue
        if not (sv<len(lab) and lab[sv] in uniq): continue
        post=G[vi:vi+POST,:]; base=G[vi-30:vi,:]
        b=np.nanmean(base,axis=0); dv=post-b
        sd=np.nanmedian(np.nanstd(dv,axis=1))
        if not np.isfinite(sd) or sd<=0: continue
        dvs=dv/sd; cm=np.nanmean(dvs,axis=1,keepdims=True); dev=dvs-cm
        nA+=1
        for c in keep:
            v=float(dev[:,c].mean())
            if np.isfinite(v): A[c].append(v)
# --- pipeline B: the grid's arithmetic, verbatim, on the same events
B=collections.defaultdict(list); nB=0
with np.errstate(all='ignore'):
    for sv,vi in zip(stim,vols):
        if sv<0 or vi<SHIFT or vi+48>=T: continue                   # the cache's filter
        if not (sv<len(lab) and lab[sv] in uniq): continue
        seg=G[vi:vi+48,:]; base=np.nanmean(G[vi-30:vi,:],axis=0)
        d=seg[:POST]-base
        cmv=np.nanmean(d,axis=1,keepdims=True)
        d=d-cmv
        val=np.nanmean(d,axis=0)
        nB+=1
        for c in keep:
            v=float(val[c])
            if np.isfinite(v): B[c].append(v)
print(f"  管线 A（代码）: 事件 {nA}")
print(f"  管线 B（网格）: 事件 {nB}")
print(f"  ==> 事件数差 {nA-nB}（缓存过滤器 vi+48>=T 比代码的 vi+24>=T 更严）")
# per-cell comparison on the cells both have
common=[c for c in keep if A[c] and B[c]]
print(f"\n  两侧都有值的细胞: {len(common)}")
if common:
    diffs=[]
    for c in common:
        a=np.array(A[c]); b=np.array(B[c])
        n=min(a.size,b.size)
        diffs.append((c, a[:n].mean(), b[:n].mean(), abs(a[:n].mean()-b[:n].mean())))
    diffs.sort(key=lambda t:-t[3])
    print(f"  {'cell':>5} {'A mean':>12} {'B mean':>12} {'|diff|':>10}")
    for c,a,b,dd in diffs[:6]: print(f"  {c:>5} {a:>12.6f} {b:>12.6f} {dd:>10.6f}")
    print(f"  ... 最大差 {diffs[0][3]:.6f}   中位差 {np.median([d[3] for d in diffs]):.6f}")
    # now the ANIMAL EFFECT under each, over the same cells
    def eff(store):
        cc=[np.mean(store[c]) for c in common if CONN[idx[lab[0]] if False else 0,0] or True]
    co_a=[c for c in common if lab[c] in idx and 0<=stim[0]<len(lab)]
    # use the first event's target for the connection mask, as the scripts do per event; here use animal-0 target set
    tgts=[lab[sv] for sv in stim if 0<=sv<len(lab)]
    conn_cells=set(); unconn_cells=set()
    for c in common:
        nm=lab[c]
        if nm not in idx: continue
        # a cell is 'connected' if ANY of this animal's targets connects to it
        isc=any((CONN[idx[t],idx[nm]] if t in idx else False) for t in tgts)
        (conn_cells if isc else unconn_cells).add(c)
    print(f"\n  按动物 0 的靶点集合: 连接细胞 {len(conn_cells)}, 未连接细胞 {len(unconn_cells)}")
    for tag,store in (("A 代码",A),("B 网格",B)):
        ec=[np.mean(store[c]) for c in conn_cells if store[c]]
        eu=[np.mean(store[c]) for c in unconn_cells if store[c]]
        if ec and eu: print(f"    {tag}: 连接均值 {np.mean(ec):+.6f}  未连接 {np.mean(eu):+.6f}  差 {np.mean(ec)-np.mean(eu):+.6f}")
