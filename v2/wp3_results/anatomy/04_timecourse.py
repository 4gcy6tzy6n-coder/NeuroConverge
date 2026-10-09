import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
PRE=8; MAXPOST=48            # 0 .. 24 s post-stimulus
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
# accumulate the response trajectory for connected vs unconnected pairs, and per layer
traj={"conn":[], "unconn":[], "chem":[], "gap":[]}
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
            if sv<0 or vi>=T or vi<PRE: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            end=min(T, vi+MAXPOST)
            if end-vi < 16: continue
            seg=G[vi:end,:]                                   # (post, cells)
            pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
            if not np.isfinite(np.nanmean(pre)): continue
            # normalise by the pre-stim SD across cells in this event (keeps scale comparable)
            sd=np.nanstd(pre)
            if not np.isfinite(sd) or sd==0: continue
            dv=(seg-pre)/sd
            n_ev+=1
            m=min(MAXPOST, dv.shape[0])
            for c in keep:
                tg=lab[sv]; rc=lab[c]
                if tg not in idx or rc not in idx: continue
                col=dv[:m,c]
                if np.all(~np.isfinite(col)): continue
                if conn[idx[tg],idx[rc]]:
                    traj["conn"].append(col)
                    if chem[idx[tg],idx[rc]]!=0: traj["chem"].append(col)
                    if gap[idx[tg],idx[rc]]!=0: traj["gap"].append(col)
                else:
                    traj["unconn"].append(col)
print(f"  {n_an} 只动物, {n_ev:,} 次事件")
res={"n_animals":n_an,"n_events":n_ev,"PRE":PRE,"MAXPOST":MAXPOST,"dt_s":0.5}
print(f"\n  === 经验刺激后时间过程（以事件内前刺激 SD 为单位）===")
print(f"  {'vol':>4} {'s':>5} " + " ".join(f"{k:>9}" for k in ("conn","unconn","chem","gap")))
series={}
for k,v in traj.items():
    if not v: continue
    A=np.array([x for x in v if len(x)==MAXPOST])
    if A.shape[0]<50: continue
    mu=np.nanmean(A,axis=0); se=np.nanstd(A,axis=0)/np.sqrt(A.shape[0])
    series[k]={"mean":[float(x) for x in mu],"se":[float(x) for x in se],"n":int(A.shape[0])}
for t in range(0,MAXPOST,2):
    row=f"  {t:>4} {t*0.5:>5.1f} "
    for k in ("conn","unconn","chem","gap"):
        row += f" {series[k]['mean'][t]:>9.3f}" if k in series else f" {'-':>9}"
    print(row)
print()
for k in ("conn","unconn","chem","gap"):
    if k not in series: continue
    mu=np.array(series[k]["mean"]); pk=int(np.argmax(mu))
    base=np.mean(mu[:2]); tail=np.mean(mu[-4:])
    half=base+(mu[pk]-base)/2
    above=np.where(mu>=half)[0]
    print(f"  {k:>7}: n={series[k]['n']:>7,}  峰 @ {pk} vol ({pk*0.5:.1f} s) = {mu[pk]:.3f}   "
          f"基线(0-1s) {base:+.3f}  尾部(22-24s) {tail:+.3f}  半峰持续 {above.min()}..{above.max()} vol "
          f"({above.min()*0.5:.1f}..{above.max()*0.5:.1f} s)" if above.size else "")
res["series"]=series
json.dump(res, open("/tmp/osf/timecourse.json","w"), indent=2)
