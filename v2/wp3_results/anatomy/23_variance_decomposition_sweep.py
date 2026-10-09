"""Does V2-C3 hold when the decomposition is made well-posed?

Two things had to be fixed after a replication attempt failed.

1. The replication script added an atlas-membership filter that V2-C3 does not need, because the
   decomposition is over ALL pairs and never consults connectivity.  That alone moved the unit count from
   192,303 to 173,954.  This script uses the round-12 filter, so the WT run should reproduce 55.1 / 37.5 /
   5.5 / 1.9 exactly.

2. The unc-31 run produced beta = -35.7 per cent, an impossible negative variance.  The cause is that
   var_pair is computed from pair means, and with few animals per pair those means are noisy, so the
   components can sum to more than the total.  This script therefore adds a minimum-animals-per-pair
   restriction and reports the decomposition as a function of it, for BOTH arms.

If the WT shares are stable as the restriction tightens, V2-C3 is well-posed.  If they move, V2-C3 needs
the restriction stated as part of its specification.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
DATA=pathlib.Path("/tmp/osf/w/exported_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
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
                    cell[(i, lab[sv], lab[c])].append(float(sm[kk]))   # round-12 filter: names only
    return cell,n_an,n_ev
def tf(x): return np.log(abs(x)+1.0)*(1.0 if x>=0 else -1.0)
def decompose(cell,minan,label):
    # keep pairs measured in at least minan animals
    pa=collections.defaultdict(set)
    for (a,tg,rc) in cell: pa[(tg,rc)].add(a)
    sel={k for k,v in pa.items() if len(v)>=minan}
    sub={k:v for k,v in cell.items() if (k[1],k[2]) in sel}
    if len(sub)<500: return None
    eps=np.array([np.var([tf(x) for x in v],ddof=1) for v in sub.values() if len(v)>=2])
    eps=eps[np.isfinite(eps)]
    var_eps=float(np.median(eps)) if eps.size else 0.0
    cm={k:float(np.mean([tf(x) for x in v])) for k,v in sub.items()}
    var_tot=float(np.var(list(cm.values())))
    an=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): an[a].append(m)
    var_alpha=float(np.var([float(np.mean(v)) for v in an.values()]))
    pv=collections.defaultdict(list)
    for (a,tg,rc),m in cm.items(): pv[(tg,rc)].append(m)
    var_pair=float(np.var([float(np.mean(v)) for v in pv.values()]))
    var_beta=var_tot-var_alpha-var_pair-var_eps
    return {"n_units":len(sub),"n_pairs":len(sel),"n_repeat":int(eps.size),
            "var_total":var_tot,"var_pair":var_pair,"var_eps":var_eps,
            "var_beta":float(var_beta),"var_alpha":var_alpha,
            "frac_pair":var_pair/var_tot,"frac_eps":var_eps/var_tot,
            "frac_beta":float(var_beta/var_tot),"frac_alpha":var_alpha/var_tot}
out={}
for root,lab in (("/tmp/osf/w/exported_data","WT"),("/tmp/osf/u/exported_data_unc31","unc-31")):
    cell,n_an,n_ev=collect(root)
    print(f"\n########## {lab}: {n_an} 只动物, {n_ev:,} 事件, {len(cell):,} 单元 ##########")
    print(f"  {'min_an':>7} {'pairs':>8} {'units':>9} {'repeat':>8} {'pair%':>7} {'eps%':>7} {'beta%':>7} {'alpha%':>7}")
    res={}
    for minan in (1,2,3,5,10):
        r=decompose(cell,minan,lab)
        if r is None: print(f"  {minan:>7}  -- 单元不足，跳过"); continue
        res[minan]=r
        print(f"  {minan:>7} {r['n_pairs']:>8,} {r['n_units']:>9,} {r['n_repeat']:>8,} "
              f"{100*r['frac_pair']:>6.1f} {100*r['frac_eps']:>6.1f} {100*r['frac_beta']:>6.1f} {100*r['frac_alpha']:>6.1f}")
    out[lab]=res
print("\n\n=== 判读 ===")
wt=out.get("WT",{}); mu=out.get("unc-31",{})
if 1 in wt:
    print(f"  WT min_an=1 是否复现第12轮 (55.1/37.5/5.5/1.9):")
    r=wt[1]
    print(f"    {100*r['frac_pair']:.1f} / {100*r['frac_eps']:.1f} / {100*r['frac_beta']:.1f} / {100*r['frac_alpha']:.1f}"
          f"   单元 {r['n_units']:,}")
    ok = abs(r['n_units']-192303)<500
    print(f"    ==> 单元数 {'匹配 192303' if ok else '不匹配'}")
print(f"\n  beta 何时转正（WT）:")
for k in sorted(wt): print(f"    min_an={k}: beta {100*wt[k]['frac_beta']:.1f}%")
print(f"\n  beta 何时转正（unc-31）:")
for k in sorted(mu): print(f"    min_an={k}: beta {100*mu[k]['frac_beta']:.1f}%  (pairs {mu[k]['n_pairs']:,})")
json.dump(out, open("/tmp/osf/vardecomp_fixed.json","w"), indent=2, ensure_ascii=False)
