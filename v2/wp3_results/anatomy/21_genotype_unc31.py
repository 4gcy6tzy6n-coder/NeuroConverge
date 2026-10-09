"""The unc-31 arm: the pre-registered prediction and the power that bounds it.

The source reports that extrasynaptic signalling, invisible to anatomy, contributes to the gap between
anatomical prediction and measured propagation.  IF that is right, then removing the extrasynaptic
component -- which is what the unc-31 dense-core-vesicle mutant does -- should leave the anatomically
mediated part, so the connectivity-function association should be LARGER in unc-31 than in WT.

    prediction:  d_unc31  >  d_WT

The prediction is registered here BEFORE the comparison is computed, and the power is reported with it,
because the mutant arm has 15 usable animals against 112 and a null result is therefore weak evidence.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, math
WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
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
SHIFT=60
def per_animal_effect(root, label):
    D=pathlib.Path(root); rows=[]; nev=0
    for i in sorted({int(m.group(1)) for p in D.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))}):
        gp,lp,sp,vp=(D/f"{i}_gcamp.txt",D/f"{i}_labels.txt",D/f"{i}_stim_neurons.txt",D/f"{i}_stim_volume_i.txt")
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
        co=[]; un=[]; n_ev_a=0
        with np.errstate(all='ignore'):
            for k,(sv,vi) in enumerate(zip(stim,vols)):
                if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                inter=(vols[k+1]-vi) if k+1<len(vols) else 62
                mv=max(12, min(int((inter*0.5-5)/0.5), 60))
                end=min(T, vi+mv)
                if end-vi<12: continue
                n_ev_a+=1; nev+=1
                raw=G[vi-SHIFT:end,:]
                base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
                seg=raw-base
                sm=np.nansum(seg[SHIFT:, keep], axis=0)
                for kk,c in enumerate(keep):
                    if not np.isfinite(sm[kk]): continue
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    if i_ is None or j_ is None: continue
                    (co if conn[i_,j_] else un).append(float(sm[kk]))
        if len(co)<10 or len(un)<50: continue
        allv=np.array(co+un); mu=allv.mean(); sd=allv.std()
        if not np.isfinite(sd) or sd<=0: continue
        rows.append({"animal":int(i),"effect":float(np.mean((np.array(co)-mu)/sd)-np.mean((np.array(un)-mu)/sd)),
                     "n_conn":len(co),"n_unconn":len(un),"n_events":n_ev_a,
                     "n_cells":len(keep),"volumes":int(T)})
    print(f"  {label}: {len(rows)} 只动物进入分析, {nev:,} 事件")
    return rows
WT=per_animal_effect("/tmp/osf/w/exported_data","WT")
MU=per_animal_effect("/tmp/osf/u/exported_data_unc31","unc-31")
def summary(rows,label):
    d=np.array([r["effect"] for r in rows]); n=d.size
    m=d.mean(); s=d.std(ddof=1); se=s/math.sqrt(n); t=m/se
    print(f"\n  === {label} ===")
    print(f"    动物 {n}   效应 均值 {m:+.4f}  SD {s:.4f}  SE {se:.4f}  t={t:.3f}  d={m/s:.4f}")
    print(f"    95% CI [{m-1.96*se:+.4f}, {m+1.96*se:+.4f}]")
    print(f"    效应为正的动物 {int((d>0).sum())}/{n} ({100*(d>0).mean():.1f}%)")
    return {"n":int(n),"mean":float(m),"sd":float(s),"se":float(se),"t":float(t),"cohens_d":float(m/s),
            "ci":[float(m-1.96*se),float(m+1.96*se)],"frac_positive":float((d>0).mean())}
sw=summary(WT,"WT"); sm=summary(MU,"unc-31")
# the pre-registered comparison
diff=sm["mean"]-sw["mean"]; se_d=math.sqrt(sm["se"]**2+sw["se"]**2)
print(f"\n  === 预注册预测: d_unc31 > d_WT ===")
print(f"    差 {diff:+.4f}  SE {se_d:.4f}  z = {diff/se_d:+.3f}")
from math import erfc
p_one=0.5*erfc((diff/se_d)/math.sqrt(2))
print(f"    单侧 p = {p_one:.4f}   (预测有方向，故单侧)")
print(f"    ==> {'预测获支持' if (diff>0 and p_one<0.05) else '预测未获支持' if diff<0 else '方向正确但不显著'}")
# power
print(f"\n  === 功效 ===")
for dd in (0.2,0.3,0.5,0.8):
    need = ((1.96+0.84)/dd)**2
    print(f"    要在两组独立设计下以 80% 功效检出 d={dd}，每组需 {need:.1f} 只")
print(f"    unc-31 实际 {sm['n']} 只, WT {sw['n']} 只   (等效每组 {2/(1/sm['n']+1/sw['n']):.1f})")
eq=2/(1/sm['n']+1/sw['n']); d80=(1.96+0.84)*math.sqrt(2/eq)
print(f"    该设计在 80% 功效下的可检出 d = {d80:.4f}")
print(f"    观测到的组间差 = {abs(diff):.4f}  ==> {'达到' if abs(diff)>=d80 else '未达到'}可检出阈值")
json.dump({"WT":sw,"unc31":sm,"diff":float(diff),"se_diff":float(se_d),"z":float(diff/se_d),
           "p_one_sided":float(p_one),"equiv_n_per_group":float(eq),"d80":float(d80),
           "supported": bool(diff>0 and p_one<0.05),
           "WT_animals":[r["animal"] for r in WT],"MU_animals":[r["animal"] for r in MU]},
          open("/tmp/osf/genotype.json","w"), indent=2)
