import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
f=h5py.File(WNA/"funatlas.h5","r")
ids=[x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx={n:i for i,n in enumerate(ids)}; N=len(ids)
PRE=8; MAXPOST=24
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

# Two response definitions, so the effect of the common-mode correction is visible:
#   RAW  : post - pre, per cell
#   CMsub: subtract, at each post timepoint, the across-cell mean of that event, then post - pre
#          (the across-cell mean is the common mode; removing it isolates cell-specific deviation)
traj={"raw":{"conn":[],"unconn":[],"chem":[],"gap":[]},
      "cm":{"conn":[],"unconn":[],"chem":[],"gap":[]}}
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
            end=min(T,vi+MAXPOST)
            if end-vi<8: continue
            pre=G[max(0,vi-PRE):vi,:]
            post=G[vi:end,:]
            # per-cell pre baseline and pre SD
            b=np.nanmean(pre,axis=0); s=np.nanstd(pre,axis=0)
            # common mode = across-cell mean at each timepoint, relative to its own pre mean
            cm_t=np.nanmean(post,axis=1)                    # (nt,)
            cm_b=np.nanmean(pre,axis=1)
            cm=cm_t-np.nanmean(cm_b)                         # common-mode deviation at each post timepoint
            cmfull=np.concatenate([np.zeros(PRE) if False else np.zeros(0), cm])
            n_ev+=1
            nt=end-vi
            dv_raw=(post-b)/np.where(s==0,np.nan,s)
            dv_cm=(post-b-cm[:,None])/np.where(s==0,np.nan,s)
            for c in keep:
                tg=lab[sv]; rc=lab[c]
                if tg not in idx or rc not in idx: continue
                i_,j_=idx[tg],idx[rc]
                key = "conn" if conn[i_,j_] else "unconn"
                if nt==MAXPOST:
                    traj["raw"][key].append(dv_raw[:,c])
                    traj["cm"][key].append(dv_cm[:,c])
                    if conn[i_,j_]:
                        if chem[i_,j_]!=0: traj["raw"]["chem"].append(dv_raw[:,c]); traj["cm"]["chem"].append(dv_cm[:,c])
                        if gap[i_,j_]!=0:  traj["raw"]["gap"].append(dv_raw[:,c]);  traj["cm"]["gap"].append(dv_cm[:,c])
print(f"  {n_an} 只动物, {n_ev:,} 次事件")
out={"n_animals":n_an,"n_events":n_ev,"PRE":PRE,"MAXPOST":MAXPOST}
for mode in ("raw","cm"):
    print(f"\n  === {mode} 时间过程（单位：事件内前刺激 SD）===")
    print(f"  {'s':>5} " + " ".join(f"{k:>9}" for k in ("conn","unconn","chem","gap")))
    ser={}
    for k,v in traj[mode].items():
        A=np.array([x for x in v if len(x)==MAXPOST])
        if A.shape[0]<50: continue
        ser[k]={"mean":[float(x) for x in np.nanmean(A,axis=0)],"n":int(A.shape[0])}
    for t in range(0,MAXPOST,3):
        row=f"  {t*0.5:>5.1f} "
        for k in ("conn","unconn","chem","gap"):
            row += f" {ser[k]['mean'][t]:>9.3f}" if k in ser else f" {'-':>9}"
        print(row)
    for k in ("conn","unconn","chem","gap"):
        if k not in ser: continue
        mu=np.array(ser[k]["mean"]); pk=int(np.argmax(mu))
        deltas = mu[0]-mu[pk]
        print(f"    {k:>7}: n={ser[k]['n']:>7,}  峰 {mu[pk]:+.4f} @ {pk*0.5:.1f}s   0.5s 处 {mu[1]:+.4f}   24s 处 {mu[-1]:+.4f}")
    out[mode+"_series"]=ser
    # contrast at several windows
    print(f"    窗口对比:")
    for W in (1,2,4,8,12,24):
        if W>=MAXPOST: continue
        a=[]
        for k in ("chem","gap"):
            if k not in ser: continue
            # rebuild per-window mean from the arrays would be costly; approximate by cumulative mean
            pass
json.dump(out, open("/tmp/osf/commonmode.json","w"), indent=2)
