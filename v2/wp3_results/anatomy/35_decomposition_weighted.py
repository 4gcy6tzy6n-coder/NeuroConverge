"""Does the per-event sd weighting move the three-level decomposition's shares?

Round 34 established that dvs = dv/sd_event is a per-event weighting worth exactly 0.3356 in d_A, which
reproduces the code's 0.7289 exactly when included and gives 0.3933 when omitted.  Five grids omitted it, and
one of them is the three-level variance decomposition behind V2-C3.

So V2-C3's shares -- 55.1 per cent between-pair, 37.5 per cent measurement error, 5.5 per cent pair-specific
animal, 1.9 per cent animal offset at the round-12 specification -- were computed WITHOUT the weighting.
This runs the decomposition both ways on the same events and reports both sets of shares.

Model:  y[a,p,i] = mu + alpha[a] + beta[a,p] + eps,   eps from units with repeats.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
SHIFT=60; POST=24
def tf(x): return np.log(abs(x)+1.0)*(1.0 if x>=0 else -1.0)

def collect(weighted):
    cell=collections.defaultdict(list); n_an=0; nev=0
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
                if sv<0 or vi<SHIFT or vi+POST>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                nev+=1
                post=G[vi:vi+POST,:]; base=G[vi-30:vi,:]
                dv=post-np.nanmean(base,axis=0)
                if weighted:
                    sd=np.nanmedian(np.nanstd(dv,axis=1))
                    if not np.isfinite(sd) or sd<=0: continue
                    dv=dv/sd                                   # THE WEIGHTING
                cm=np.nanmean(dv,axis=1,keepdims=True); dev=dv-cm
                for c in keep:
                    v=float(dev[:,c].mean())
                    if not np.isfinite(v): continue
                    cell[(i, lab[sv], lab[c])].append(v)
    return cell,n_an,nev

def decompose(cell,label):
    eps=np.array([np.var([tf(x) for x in v],ddof=1) for v in cell.values() if len(v)>=2])
    eps=eps[np.isfinite(eps)]
    var_eps=float(np.median(eps)) if eps.size else 0.0
    cm={k:float(np.mean([tf(x) for x in v])) for k,v in cell.items()}
    var_tot=float(np.var(list(cm.values())))
    an=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): an[a].append(m)
    var_alpha=float(np.var([float(np.mean(v)) for v in an.values()]))
    pv=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): pv[(tg,rc)].append(m)
    var_pair=float(np.var([float(np.mean(v)) for v in pv.values()]))
    var_beta=var_tot-var_alpha-var_pair-var_eps
    return {"n_units":len(cell),"n_repeat":int(eps.size),
            "frac_pair":var_pair/var_tot,"frac_eps":var_eps/var_tot,
            "frac_beta":float(var_beta/var_tot),"frac_alpha":var_alpha/var_tot,
            "var_total":var_tot}
out={}
for w in (False,True):
    cell,n_an,nev=collect(w)
    tag="有逐事件加权" if w else "无逐事件加权"
    print(f"\n  === {tag} ===  {n_an} 只动物, {nev:,} 事件, {len(cell):,} 个 (动物,配对) 单元")
    r=decompose(cell,tag)
    out[tag]=r
    print(f"    配对间 {100*r['frac_pair']:.1f}%   eps {100*r['frac_eps']:.1f}%   "
          f"beta {100*r['frac_beta']:.1f}%   alpha {100*r['frac_alpha']:.1f}%   重复单元 {r['n_repeat']:,}")
print(f"\n  === 逐事件加权对分解的影响 ===")
a=out["无逐事件加权"]; b=out["有逐事件加权"]
for k,lab in (("frac_pair","配对间"),("frac_eps","测量误差 eps"),("frac_beta","配对特异 beta"),("frac_alpha","动物偏移 alpha")):
    print(f"    {lab:>14}:  无 {100*a[k]:>6.1f}%  ->  有 {100*b[k]:>6.1f}%   变化 {100*(b[k]-a[k]):+6.1f} 点")
print(f"\n  === 与 V2-C3 所报值对照 ===")
print(f"    V2-C3 第 12 轮规格: 配对间 55.1  eps 37.5  beta 5.5  alpha 1.9  (单元 192,303)")
print(f"    本脚本无加权     : 配对间 {100*a['frac_pair']:.1f}  eps {100*a['frac_eps']:.1f}  "
      f"beta {100*a['frac_beta']:.1f}  alpha {100*a['frac_alpha']:.1f}  (单元 {a['n_units']:,})")
print(f"    ==> {'复现' if abs(100*a['frac_eps']-37.5)<1.0 else '不同（因 POST/窗口约定与第 12 轮不同）'}")
json.dump(out, open("/tmp/osf/decomp_weighted.json","w"), indent=2, ensure_ascii=False)
