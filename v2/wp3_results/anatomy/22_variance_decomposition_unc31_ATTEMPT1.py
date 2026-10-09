"""Does the three-level decomposition replicate in the unc-31 arm?

V2-C3 -- 55.1 per cent between-pair, 37.5 per cent measurement error, 5.5 per cent pair-specific animal,
1.9 per cent animal offset -- is the line's most novel measurement and it rests on ONE dataset.  The
unc-31 arm is a second dataset from the same laboratory and preparation but a different genotype.  If the
measurement-error share reproduces there, the decomposition is not an artefact of the wild-type export.

Model:  y[a,p,i] = mu + alpha[a] + beta[a,p] + eps,   eps identified from units with repeats.

The feasibility question comes first: the decomposition needs (animal, pair) units with two or more
measurements, and the mutant arm is both smaller and shorter than the wild type.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
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
def collect(root):
    D=pathlib.Path(root); cell=collections.defaultdict(list); n_an=0; n_ev=0
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
                for kk,c in enumerate(keep):
                    if not np.isfinite(sm[kk]): continue
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    if i_ is None or j_ is None: continue
                    cell[(i,i_,j_)].append(float(sm[kk]))
    return cell,n_an,n_ev
def decompose(cell,label):
    def tf(x): return np.log(abs(x)+1.0)*(1.0 if x>=0 else -1.0)
    reps=sum(1 for v in cell.values() if len(v)>=2)
    print(f"\n  === {label} ===")
    print(f"    (动物,配对) 单元 {len(cell):,}   其中有重复(>=2次)的 {reps:,}  ({100*reps/max(1,len(cell)):.1f}%)")
    if reps<200:
        print(f"    ==> 有重复单元太少({reps})，分解不可识别，跳过")
        return None
    eps=np.array([np.var([tf(x) for x in v],ddof=1) for v in cell.values() if len(v)>=2])
    eps=eps[np.isfinite(eps)]
    var_eps=float(np.median(eps))
    cm={k:float(np.mean([tf(x) for x in v])) for k,v in cell.items()}
    allm=np.array(list(cm.values())); var_tot=float(np.var(allm))
    an=collections.defaultdict(list)
    for (a,i_,j_),m in cm.items(): an[a].append(m)
    var_alpha=float(np.var([float(np.mean(v)) for v in an.values()]))
    pv=collections.defaultdict(list)
    for (a,i_,j_),m in cm.items(): pv[(i_,j_)].append(m)
    var_pair=float(np.var([float(np.mean(v)) for v in pv.values()]))
    var_beta=var_tot-var_alpha-var_pair-var_eps
    print(f"    var 总 {var_tot:.4f}  配对间 {var_pair:.4f} ({100*var_pair/var_tot:.1f}%)  "
          f"eps {var_eps:.4f} ({100*var_eps/var_tot:.1f}%)  "
          f"beta {var_beta:.4f} ({100*var_beta/var_tot:.1f}%)  "
          f"alpha {var_alpha:.4f} ({100*var_alpha/var_tot:.1f}%)")
    return {"n_units":len(cell),"n_repeat_units":int(reps),"var_total":var_tot,"var_pair":var_pair,
            "var_eps":var_eps,"var_beta":float(var_beta),"var_alpha":var_alpha,
            "frac_pair":var_pair/var_tot,"frac_eps":var_eps/var_tot,
            "frac_beta":float(var_beta/var_tot),"frac_alpha":var_alpha/var_tot}
out={}
for root,lab in (("/tmp/osf/w/exported_data","WT (reference)"),
                 ("/tmp/osf/u/exported_data_unc31","unc-31 (replication attempt)")):
    cell,n_an,n_ev=collect(root)
    print(f"\n  {lab}: {n_an} 只动物, {n_ev:,} 事件")
    r=decompose(cell,lab)
    if r: out[lab]=r
if len(out)==2:
    w=list(out.values())
    print(f"\n  === 复现检验 ===")
    print(f"    测量误差份额:  WT {w[0]['frac_eps']:.4f}   unc-31 {w[1]['frac_eps']:.4f}   "
          f"差 {abs(w[0]['frac_eps']-w[1]['frac_eps']):.4f}")
    print(f"    配对特异份额:  WT {w[0]['frac_beta']:.4f}   unc-31 {w[1]['frac_beta']:.4f}")
    print(f"    配对间份额:    WT {w[0]['frac_pair']:.4f}   unc-31 {w[1]['frac_pair']:.4f}")
json.dump(out, open("/tmp/osf/vardecomp_unc31.json","w"), indent=2, ensure_ascii=False)
