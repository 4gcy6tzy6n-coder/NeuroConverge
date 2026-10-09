"""Is the per-animal connectivity effect a stable property of that animal?

Per-animal split-half reliability of the effect itself.  Within each animal, split its stimulus events
into two halves, compute the connected-minus-unconnected contrast from each half, and correlate the two
across animals (Spearman-Brown corrected).  This mirrors the round-9 test of pair responses and answers
the question round 12 left open: is the between-animal spread of the EFFECT (I^2 = 57.3 %) a property of
the animals, or an artefact of which pairs each animal happened to measure?

  high r_full -> the effect is stable within an animal, so the between-animal spread is real
  low  r_full -> the effect is not stable even within an animal, so the spread is measurement noise
"""
import numpy as np, h5py, csv, pathlib, re, collections, json, math
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
SHIFT=60
# per animal: list of (event_index, connected values, unconnected values), so events can be split
perA=collections.defaultdict(list)
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
        for k,(sv,vi) in enumerate(zip(stim,vols)):
            if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            n_ev+=1
            inter=(vols[k+1]-vi) if k+1<len(vols) else 62
            mv=max(12, min(int((inter*0.5-5)/0.5), 60))
            end=min(T, vi+mv)
            if end-vi<12: continue
            raw=G[vi-SHIFT:end,:]
            base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
            seg=raw-base
            sm=np.nansum(seg[SHIFT:, keep], axis=0)
            co=[]; un=[]
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                (co if conn[i_,j_] else un).append(float(sm[kk]))
            if co and un: perA[i].append((co,un))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(perA)} 只有成对事件")
# within-animal split-half of the EFFECT
rng=np.random.default_rng(0)
m1=[];m2=[];n_use=0
for i,evs in perA.items():
    if len(evs)<8: continue
    o=rng.permutation(len(evs)); h=len(evs)//2
    def eff(sel):
        co=[v for e in sel for v in e[0]]; un=[v for e in sel for v in e[1]]
        if len(co)<5 or len(un)<5: return None
        # standardise within the half so the animal's own scale does not enter
        allv=np.array(co+un); mu=allv.mean(); sd=allv.std()
        if not np.isfinite(sd) or sd<=0: return None
        return (np.mean((np.array(co)-mu)/sd) - np.mean((np.array(un)-mu)/sd))
    a=eff([evs[j] for j in o[:h]]); b=eff([evs[j] for j in o[h:]])
    if a is None or b is None: continue
    n_use+=1; m1.append(a); m2.append(b)
m1=np.array(m1); m2=np.array(m2)
r=np.corrcoef(m1,m2)[0,1]; rfull=2*r/(1+r)
print(f"\n  === 逐动物分半：效应本身的可复现性 ===")
print(f"    动物数 {n_use}")
print(f"    两半效应相关 r = {r:.4f}   r_full = {rfull:.4f}")
print(f"    同半内的效应: 半1 均值 {m1.mean():+.4f} SD {m1.std(ddof=1):.4f}")
print(f"                  半2 均值 {m2.mean():+.4f} SD {m2.std(ddof=1):.4f}")
print()
# compare with the between-animal spread of the FULL-data effect
full=[]
for i,evs in perA.items():
    co=[v for e in evs for v in e[0]]; un=[v for e in evs for v in e[1]]
    if len(co)<10 or len(un)<50: continue
    allv=np.array(co+un); mu=allv.mean(); sd=allv.std()
    if not np.isfinite(sd) or sd<=0: continue
    full.append(np.mean((np.array(co)-mu)/sd)-np.mean((np.array(un)-mu)/sd))
full=np.array(full)
print(f"  === 对比 ===")
print(f"    全数据效应的跨动物 SD          {full.std(ddof=1):.4f}   (n={full.size})")
print(f"    分半效应差(m1-m2)的 SD         {(m1-m2).std(ddof=1):.4f}")
print(f"    ==> 若分半差与跨动物 SD 同量级，则跨动物离散主要是估计噪声")
print(f"    比率 SD(m1-m2)/SD(full) = {(m1-m2).std(ddof=1)/full.std(ddof=1):.4f}")
# variance attributable to noise: var(m1-m2)/2 estimates the noise variance of the effect
noise_var=(m1-m2).var(ddof=1)/4.0; total_var=full.var(ddof=1)
print(f"\n    效应估计的噪声方差 var(m1-m2)/4 = {noise_var:.6f}")
print(f"    全数据效应的方差               = {total_var:.6f}")
print(f"    噪声占比 = {noise_var/total_var:.4f}")
print(f"    ==> 可复现(信号)占比 = {max(0.0,1-noise_var/total_var):.4f}")
json.dump({"n_animals_used":int(n_use),"split_half_r":float(r),"split_half_r_full":float(rfull),
           "noise_var":float(noise_var),"total_var":float(total_var),
           "noise_frac":float(noise_var/total_var),
           "signal_frac":float(max(0.0,1-noise_var/total_var)),
           "sd_halfdiff":float((m1-m2).std(ddof=1)),"sd_full":float(full.std(ddof=1))},
          open("/tmp/osf/effect_reliab.json","w"), indent=2)
