"""Pair-set-matched test: does the reproducible part of the between-animal spread shrink when pair
composition is held more constant?

For a range of K, restrict every animal to pairs measured in at least K animals, compute the effect per
animal from that restricted set, and separate signal from noise using the round-14 machinery:

    noise variance of the full-data effect  =  var(m1 - m2)/4      (split-half)
    signal share                            =  1 - noise/total

If the signal share falls toward zero as K rises, pair composition explains the spread.  If it persists,
composition does not.

First a feasibility probe: how many pairs survive each K, and of those, how many are CONNECTED?  Connected
pairs are the rare class, so the restriction may empty the connected subset before it constrains anything.
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
# per animal, per event: the connected and unconnected values, so events can be halved
perA=collections.defaultdict(list); pair_animals=collections.defaultdict(set)
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
            rec=[]
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                rec.append((i_,j_,float(sm[kk])))
                pair_animals[(i_,j_)].add(i)
            if rec: perA[i].append(rec)
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(pair_animals):,} 个配对")
cnts=np.array([len(v) for v in pair_animals.values()])
print(f"  每个配对被多少只动物测过: 中位 {int(np.median(cnts))}  p90 {int(np.percentile(cnts,90))}  max {int(cnts.max())}")
for K in (1,2,3,5,10):
    sel={k for k,v in pair_animals.items() if len(v)>=K}
    nconn=sum(1 for (a,b) in sel if conn[a,b])
    print(f"    K={K:>2}: 配对 {len(sel):>6,}   其中连接 {nconn:>5,}   动物数 {len({a for k in sel for a in pair_animals[k]}):>4}")
print()
rng=np.random.default_rng(0)
res=[]
for K in (1,2,3,5):
    sel={k for k,v in pair_animals.items() if len(v)>=K}
    if len(sel)<50: continue
    effs=[]; m1=[]; m2=[]
    for a,evs in perA.items():
        # restrict each event to the selected pairs
        co=[]; un=[]
        for rec in evs:
            for (i_,j_,v) in rec:
                if (i_,j_) not in sel: continue
                (co if conn[i_,j_] else un).append(v)
        if len(co)<10 or len(un)<30: continue
        allv=np.array(co+un); mu=allv.mean(); sd=allv.std()
        if not np.isfinite(sd) or sd<=0: continue
        effs.append(float(np.mean((np.array(co)-mu)/sd)-np.mean((np.array(un)-mu)/sd)))
        # split-half over EVENTS for the noise estimate
        if len(evs)<8: continue
        o=rng.permutation(len(evs)); h=len(evs)//2
        def eff_half(sub):
            c2_=[]; u2=[]
            for rec in sub:
                for (i_,j_,v) in rec:
                    if (i_,j_) not in sel: continue
                    (c2_ if conn[i_,j_] else u2).append(v)
            if len(c2_)<5 or len(u2)<10: return None
            av=np.array(c2_+u2); m_=av.mean(); s_=av.std()
            if not np.isfinite(s_) or s_<=0: return None
            return float(np.mean((np.array(c2_)-m_)/s_)-np.mean((np.array(u2)-m_)/s_))
        x=eff_half([evs[j] for j in o[:h]]); y=eff_half([evs[j] for j in o[h:]])
        if x is None or y is None: continue
        m1.append(x); m2.append(y)
    e=np.array(effs); n=e.size
    if n<15: continue
    total=e.var(ddof=1)
    if len(m1)>=15:
        m1a=np.array(m1); m2a=np.array(m2)
        r=np.corrcoef(m1a,m2a)[0,1]; rfull=2*r/(1+r)
        noise=(m1a-m2a).var(ddof=1)/4.0
        sigf=max(0.0,1-noise/total)
    else:
        rfull=float('nan'); noise=float('nan'); sigf=float('nan')
    nconn=sum(1 for (a,b) in sel if conn[a,b])
    res.append({"K":K,"n_pairs":len(sel),"n_conn_pairs":nconn,"n_animals":int(n),
                "effect_mean":float(e.mean()),"effect_sd":float(e.std(ddof=1)),
                "r_full":float(rfull),"noise_var":float(noise),"total_var":float(total),
                "signal_frac":float(sigf)})
    print(f"  K={K:>2}  配对 {len(sel):>6,} (连接 {nconn:>5,})  动物 {n:>4}  "
          f"效应 SD {e.std(ddof=1):.4f}  r_full {rfull:.4f}  信号占比 {sigf:.4f}")
json.dump(res, open("/tmp/osf/pairset.json","w"), indent=2)
