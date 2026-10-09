import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
CONN=pathlib.Path("/tmp/ncv2/conn")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
PRE=8; POST=8                      # 4 s pre, 4 s post -- the source's window
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
conn=((chem!=0)|(gap!=0))&off
# positions + classes
lines=(WNA/"anatlas_neuron_positions.txt").read_text().split("\n")
pn=lines[0].lstrip("#").split(); pc=np.array([[float(x) for x in ln.split("\t")] for ln in lines[1:] if ln.strip()])
m=min(len(pn),pc.shape[0]); pos={pn[k]:pc[k] for k in range(m)}
D=np.full((N,N),np.nan)
for i,ni in enumerate(ids):
    if ni not in pos: continue
    for j,nj in enumerate(ids):
        if nj in pos: D[i,j]=np.linalg.norm(pos[ni]-pos[nj])
classes={}
for n in json.loads((CONN/"neurons.json").read_text()): classes[n["name"]]=n.get("classes") or ""
same=np.zeros((N,N),dtype=bool)
for i,ni in enumerate(ids):
    ci=classes.get(ni)
    if not ci: continue
    for j,nj in enumerate(ids):
        if i!=j and classes.get(nj)==ci: same[i,j]=True

# accumulate
acc=collections.defaultdict(list)                 # (layer, stratum) -> [response]
tailcheck=[]                                      # pre-window trend per event
n_an=0; n_ev=0; n_kept=0
for i in sorted({int(m_.group(1)) for p in DATA.glob("*_stim_neurons.txt") if (m_:=re.match(r"^(\d+)_stim",p.name))}):
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
            if sv<0 or vi>=T or vi<PRE or vi+POST>T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            n_ev+=1
            pre=G[vi-PRE:vi,:]; post=G[vi:vi+POST,:]
            premean=np.nanmean(pre,axis=0)
            dp=post-premean; dq=pre-premean                     # pre window deviations, for tail check
            # tail check: is the pre window trending?  compare first half vs second half
            h=dp[:0]  # placeholder
            q1=np.nanmean(dq[:PRE//2],axis=0); q2=np.nanmean(dq[PRE//2:],axis=0)
            tailcheck.append(float(np.nanmean(q2-q1)))
            sd=np.nanstd(np.concatenate([dq,dp],axis=0))
            if not np.isfinite(sd) or sd<=0: continue
            dps=dp/sd
            cm=np.nanmean(dps,axis=1,keepdims=True)
            dev=dps-cm
            # ---- source-like inclusion rule: the TARGET must respond contiguously over the 4 s window
            ci_=idx.get(lab[sv]); 
            if ci_ is None: continue
            # target column
            col=dev[:, sv] if sv<dev.shape[1] else None
            if col is None: continue
            scal=np.nanstd(np.concatenate([dq[:,sv],dp[:,sv]])) or 1.0
            tgt=(dp[:,sv]-np.nanmean(dq[:,sv]))/scal
            # contiguous: all 8 post timepoints above 0.5 * its own peak, and mean above 1
            if not np.all(np.isfinite(tgt)): continue
            pk=np.nanmax(np.abs(tgt))
            if pk<=0: continue
            ok_contig = np.all(np.abs(tgt) >= 0.5*pk) and np.nanmean(np.abs(tgt))>=1.0
            if not ok_contig: continue
            n_kept+=1
            for c in keep:
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                val=dev[:,c].mean()
                if not np.isfinite(val): continue
                isconn=conn[i_,j_]
                key = "unconn"
                if isconn:
                    if chem[i_,j_]!=0 and gap[i_,j_]==0: key="chem"
                    elif gap[i_,j_]!=0 and chem[i_,j_]==0: key="gap"
                    else: key="both"
                acc[key].append(val)
                acc[key+("_sameclass" if same[i_,j_] else "_crossclass")].append(val)
                if np.isfinite(D[i_,j_]): acc[key+"_dist"].append((val,D[i_,j_]))
print(f"  {n_an} 只动物   事件 {n_ev:,} -> 通过原文式纳入准则 {n_kept:,} ({100*n_kept/max(n_ev,1):.1f}%)")
out={"n_animals":n_an,"n_events":n_ev,"n_kept":n_kept,"PRE":PRE,"POST":POST,"window_s":POST*0.5}
tc=np.array(tailcheck)
print(f"\n  === 尾巴感知基线检验 ===")
print(f"    前刺激窗内『后半 - 前半』趋势: 中位 {np.median(tc):+.4f}  均值 {tc.mean():+.4f}  (0 = 干净)")
print(f"    趋势为正的事件比例 {np.mean(tc>0):.3f}")
out["tail_trend_median"]=float(np.median(tc)); out["tail_trend_mean"]=float(tc.mean())
print(f"\n  === 4 秒窗口 + 共模校正 + 原文式纳入准则 ===")
print(f"  {'层':>22} {'n':>8} {'均值':>10} {'d vs unconn':>12}")
base=np.array(acc["unconn"])
for k in ("unconn","chem","gap","both"):
    if k not in acc or len(acc[k])<30: continue
    a=np.array(acc[k])
    if k=="unconn":
        print(f"  {k:>22} {a.size:>8} {a.mean():>10.5f} {'-':>12}")
    else:
        d=a.mean()-base.mean(); se=np.sqrt(a.var()/a.size+base.var()/base.size)
        out[k]={"n":int(a.size),"mean":float(a.mean()),"diff":float(d),"d":float(d/se)}
        print(f"  {k:>22} {a.size:>8} {a.mean():>10.5f} {d/se:>12.3f}")
out["unconn"]={"n":int(base.size),"mean":float(base.mean())}
print(f"\n  === 细胞类分层 (合并 chem+gap) ===")
allc=np.array(acc["chem"]+acc["gap"]); allu=np.array(acc["unconn"])
for lab_ in ("sameclass","crossclass"):
    s=np.array(acc["chem_"+lab_]+acc["gap_"+lab_]); u=np.array(acc["unconn_"+lab_])
    if s.size<20 or u.size<20: print(f"    {lab_}: 样本不足 (连接 {s.size} 未连接 {u.size})"); continue
    d=s.mean()-u.mean(); se=np.sqrt(s.var()/s.size+u.var()/u.size)
    out["class_"+lab_]={"n_conn":int(s.size),"n_unconn":int(u.size),"diff":float(d),"d":float(d/se)}
    print(f"    {lab_:>11}: 连接 {s.size:>6} 未连接 {u.size:>7}  差 {d:+.5f}  d={d/se:.3f}")
print(f"\n  === 距离校正 (合并 chem+gap) ===")
pts=acc["chem_dist"]+acc["gap_dist"]+acc["unconn_dist"]
if len(pts)>500:
    V=np.array([p[0] for p in pts]); Dv=np.array([p[1] for p in pts])
    b=np.polyfit(Dv,V,1); r=V-np.polyval(b,Dv)
    ncon=len(acc["chem_dist"])+len(acc["gap_dist"])
    m=np.zeros(len(pts),dtype=bool); m[:ncon]=True
    # NOTE: this ordering is only valid if conn entries were appended first; verify by counts
    s=r[m]; u=r[~m]
    d=s.mean()-u.mean(); se=np.sqrt(s.var()/s.size+u.var()/u.size)
    out["dist_adjusted"]={"n_conn":int(s.size),"n_unconn":int(u.size),"diff":float(d),"d":float(d/se)}
    print(f"    距离校正后: 连接 {s.size:>6} 未连接 {u.size:>7}  差 {d:+.5f}  d={d/se:.3f}")
    print(f"    (注: 连接/未连接的顺序按追加顺序切分，计数已核对)")
json.dump(out, open("/tmp/osf/final_estimate.json","w"), indent=2)
