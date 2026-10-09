"""Three-level variance decomposition: homogeneous animal offset vs pair-specific animal deviation.

Model:  y[a,p,i] = mu + alpha[a] + beta[a,p] + eps
  alpha[a]    homogeneous animal offset (technical: GCaMP level, dissection, baseline scale)
  beta[a,p]   pair-specific animal deviation  <- the BIOLOGICAL heterogeneity of interest
  eps         within-cell measurement error

Identification.  Most (animal,pair) cells hold ONE measurement, so beta and eps are not separable there.
But cells with >=2 measurements identify eps directly, which then removes eps from the observed
cell-to-cell variance and leaves beta.  Round 9's ICC failed because it treated one-measurement cells as
contributing ZERO within-variance instead of as contributing NO INFORMATION.

This matters because a HOMOGENEOUS animal offset (alpha) would produce cross-animal disagreement with no
pair-specific biology.  If beta vanishes once alpha and eps are removed, the heterogeneity is technical.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
SHIFT=60
# collect y per (animal, pair) with all repeats
cell=collections.defaultdict(list)
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
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                cell[(i, tg, rc)].append(float(sm[kk]))
print(f"  {n_an} 只动物, {n_ev:,} 事件, {len(cell):,} 个 (动物,配对) 单元")
# geometric-mean-scale transform: the responses are heavy-tailed (raw fluorescence sums), so work in
# log space for the variance decomposition, otherwise a few huge values dominate every component.
vals=np.concatenate([np.array(v) for v in cell.values()])
pos=vals[vals>0]
print(f"  响应值: min {vals.min():.3g} max {vals.max():.3g}  正值比例 {(vals>0).mean():.3f}")
USE_LOG = (vals.max()/max(abs(vals[vals!=0]).min() if (vals!=0).any() else 1,1e-9)) > 1e4
print(f"  ==> 使用 log 空间: {USE_LOG}  (量级跨度过大时方差成分会被极值支配)")
def tf(x):
    if not USE_LOG: return x
    return np.log(np.abs(x)+1.0)*(1.0 if x>=0 else -1.0)
# --- component 1: eps, from cells with >=2 measurements
eps=[]
for v in cell.values():
    if len(v)>=2:
        eps.append(np.var([tf(x) for x in v], ddof=1))
eps=np.array([e for e in eps if np.isfinite(e)])
var_eps=float(np.median(eps)) if eps.size else 0.0
print(f"\n  === 成分估计 ===")
print(f"    eps (测量内方差, 由 {eps.size:,} 个 >=2 次的单元估出): 中位 {var_eps:.6f}")
# --- per (animal,pair) means
cellmean={k: float(np.mean([tf(x) for x in v])) for k,v in cell.items()}
# --- total cell-level variance
allm=np.array(list(cellmean.values()))
var_tot=float(np.var(allm))
# --- alpha: animal-level mean, then its variance
anmean=collections.defaultdict(list)
for (a,tg,rc),m in cellmean.items(): anmean[a].append(m)
anmu={a: float(np.mean(v)) for a,v in anmean.items()}
var_alpha=float(np.var(list(anmu.values())))
# --- per-pair mean, then variance of pair means = the pair-specific (between-pair) component
pairvals=collections.defaultdict(list)
for (a,tg,rc),m in cellmean.items(): pairvals[(tg,rc)].append(m)
pairmu={k: float(np.mean(v)) for k,v in pairvals.items()}
var_pair=float(np.var(list(pairmu.values())))
print(f"    var(总, 单元水平)          {var_tot:.6f}")
print(f"    var(alpha, 动物均值)       {var_alpha:.6f}   ({100*var_alpha/var_tot:.1f}% of total)")
print(f"    var(配对均值, 配对间)      {var_pair:.6f}   ({100*var_pair/var_tot:.1f}% of total)")
# --- beta: the animal x pair interaction = residual cell variance after alpha, pair and eps
var_beta = var_tot - var_alpha - var_pair - var_eps
print(f"    var(eps, 测量内)           {var_eps:.6f}   ({100*var_eps/var_tot:.1f}% of total)")
print(f"    var(beta, 配对特异动物偏差) {var_beta:.6f}   ({100*var_beta/var_tot:.1f}% of total)")
print()
if var_beta > 0:
    print(f"  === 判读 ===")
    print(f"    beta/total = {var_beta/var_tot:.3f}")
    print(f"    若 beta 相对 alpha 与 eps 大 ⟹ 异质性是配对特异的（生物学）")
    print(f"    若 beta 相对 alpha 小    ⟹ 异质性主要是同质动物偏移（技术）")
    print(f"    alpha/(alpha+beta+eps) = {var_alpha/(var_alpha+max(var_beta,0)+var_eps):.3f}")
else:
    print(f"  === 判读: beta <= 0 ⟹ 在 alpha、配对间与 eps 之后没有剩余的配对特异动物成分 ===")
json.dump({"n_units":len(cell),"var_total":var_tot,"var_alpha":var_alpha,"var_pair":var_pair,
           "var_eps":var_eps,"var_beta":float(var_beta),"used_log":bool(USE_LOG),
           "n_eps_units":int(eps.size),"beta_frac":float(var_beta/var_tot)},
          open("/tmp/osf/vardecomp3.json","w"), indent=2)
