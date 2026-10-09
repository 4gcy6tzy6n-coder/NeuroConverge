import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)

# ---------- positions (format: line 1 = '#name name ...', then tab-separated xyz) ----------
lines=(WNA/"anatlas_neuron_positions.txt").read_text().split("\n")
names=lines[0].lstrip("#").split()
coords=np.array([[float(x) for x in ln.split("\t")] for ln in lines[1:] if ln.strip()])
print(f"  坐标: {len(names)} 个名字, {coords.shape[0]} 行坐标")
if len(names)!=coords.shape[0]:
    print(f"  !! 名字数与坐标行数不等，按较小者对齐")
m=min(len(names),coords.shape[0]); names=names[:m]; coords=coords[:m]
pos={n:coords[k] for k,n in enumerate(names)}
covered=set(ids)&set(pos)
print(f"  funatlas 300 id 中有坐标的: {len(covered)}   无坐标: {len(set(ids)-set(pos))}")
print(f"    无坐标样例: {sorted(set(ids)-set(pos))[:10]}")

# ---------- anatomical matrices BY NAME ----------
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
chem,gap=build("aconnectome_witvliet_2020_8.csv"); chemW,gapW=build("aconnectome_white_1986_whole.csv")
chem=chem+chemW; gap=gap+gapW
print(f"  合并 witvliet_2020_8 + white_1986_whole: chem 非零 {int((chem!=0).sum())}  gap 非零 {int((gap!=0).sum())}")

# ---------- functional side ----------
PRE=POST=8
per_pair=collections.defaultdict(list); n_an=0
for i in sorted({int(m.group(1)) for p in DATA.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))}):
    gp,lp,sp,vp=(DATA/f"{i}_gcamp.txt",DATA/f"{i}_labels.txt",DATA/f"{i}_stim_neurons.txt",DATA/f"{i}_stim_volume_i.txt")
    if not all(p.exists() for p in (gp,lp,sp,vp)): continue
    try: Gm=np.loadtxt(gp)
    except Exception: continue
    lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
    stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
    T,ncol=Gm.shape
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
            post=np.nanmean(Gm[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(Gm[max(0,vi-PRE):vi,:],axis=0)
            dv=post-pre; v=dv[keep]; mu=np.nanmean(v); sd=np.nanstd(v)
            if not np.isfinite(sd) or sd==0: continue
            z=(v-mu)/sd
            for kk,c in enumerate(keep):
                if np.isfinite(z[kk]): per_pair[(lab[sv],lab[c])].append(float(z[kk]))
print(f"  功能侧: {n_an} 只, {len(per_pair):,} 配对")

Fm=np.full((N,N),np.nan); NN=np.zeros((N,N),int)
for (tg,rc),v in per_pair.items():
    if tg in idx and rc in idx:
        i,j=idx[tg],idx[rc]; Fm[i,j]=np.mean(v); NN[i,j]=len(v)
off=~np.eye(N,dtype=bool); have=np.isfinite(Fm)&off
print(f"  功能矩阵有值且非对角: {int(have.sum()):,}")

# ---------- C3: distance covariate ----------
D=np.full((N,N),np.nan)
for a,i in enumerate(ids):
    if a not in set(): pass
for i,ni in enumerate(ids):
    if ni not in pos: continue
    for j,nj in enumerate(ids):
        if nj in pos: D[i,j]=np.linalg.norm(pos[ni]-pos[nj])
dist_ok=have&np.isfinite(D)
res={}
print(f"\n  === C3: 距离协变量（有坐标的配对数 {int(dist_ok.sum()):,}）===")
for tag,cm in (("chem",(chem!=0)&off),("gap",(gap!=0)&off),("chem_or_gap",((chem!=0)|(gap!=0))&off)):
    s=dist_ok&cm; u=dist_ok&~cm
    if s.sum()<30 or u.sum()<30: print(f"    {tag}: 样本不足"); continue
    ds=D[s].mean(); du=D[u].mean()
    dresp=Fm[s].mean()-Fm[u].mean()
    # distance-adjusted: regress Fm on D over all dist_ok, take residuals, then contrast
    x=D[dist_ok]; y=Fm[dist_ok]
    b=np.polyfit(x,y,1); resid=y-np.polyval(b,x)
    cs=cm[dist_ok]
    dres=resid[cs].mean()-resid[~cs].mean()
    se=np.sqrt(resid[cs].var()/cs.sum()+resid[~cs].var()/(~cs).sum())
    pair_d=(D[s].mean()-D[u].mean())
    res[f"C3_{tag}"]={"n_conn":int(s.sum()),"n_unconn":int(u.sum()),
        "dist_conn":float(ds),"dist_unconn":float(du),"dist_diff":float(pair_d),
        "raw_diff":float(dresp),"dist_adjusted_diff":float(dres),"dist_adjusted_d":float(dres/se)}
    print(f"    {tag:12s} 连接 {int(s.sum()):>5} 对, 距离 {ds:.3f} vs {du:.3f} (差 {pair_d:+.3f})")
    print(f"                 响应差 {dresp:+.4f}   距离校正后 {dres:+.4f} (d={dres/se:.3f})")

# ---------- C2: is measurement count confounded with response? ----------
print(f"\n  === C2: 测量次数是否与响应相关（分层内）===")
for tag,cm in (("chem",(chem!=0)&off),("gap",(gap!=0)&off),("none",~((chem!=0)|(gap!=0))&off)):
    a=have&cm
    if a.sum()<100: continue
    x=NN[a].astype(float); y=Fm[a]
    r=np.corrcoef(x,y)[0,1]
    # quartiles of measurement count
    q=np.quantile(x,[0,.25,.5,.75,1.0])
    means=[y[(x>=q[k])&(x<=q[k+1])].mean() for k in range(4)]
    res[f"C2_{tag}"]={"n":int(a.sum()),"corr_nmeas_response":float(r),
                      "quartile_means":[float(v) for v in means],"quartiles":[float(v) for v in q]}
    print(f"    {tag:12s} n={int(a.sum()):>5}  corr(测量次数, 响应) = {r:+.4f}   四分位均值 {[round(v,4) for v in means]}")
print()
print("    判读: 若 corr 明显为正，则测量次数携带结果信息 => C2 成立，'按次数加权'不是外生权重")

# ---------- C1: undirected-only fair contrast ----------
print(f"\n  === C1: 限制到无向子图（只保留对称边）===")
both=(chem!=0)&(chem.T!=0)&off            # chemically reciprocal -- rare
gap_und=(gap!=0)&off                       # gap already symmetric
for tag,cm in (("gap_only_undirected",gap_und),("chem_reciprocal_only",both)):
    a=have&cm
    if a.sum()<20: print(f"    {tag}: n={int(a.sum())} 太小，跳过"); continue
    b=have&~cm
    d=Fm[a].mean()-Fm[b].mean(); se=np.sqrt(Fm[a].var()/a.sum()+Fm[b].var()/b.sum())
    res[f"C1_{tag}"]={"n_conn":int(a.sum()),"n_unconn":int(b.sum()),"diff":float(d),"d":float(d/se)}
    print(f"    {tag:24s} n_conn={int(a.sum()):>5}  差 {d:+.4f}  d={d/se:.3f}")
json.dump(res, open("/tmp/osf/confounds.json","w"), indent=2)
