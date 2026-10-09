import numpy as np, pathlib, re, collections, json
d = pathlib.Path("/tmp/osf/w/exported_data")
ids = sorted({int(m.group(1)) for p in d.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))})
PRE=POST=8
# Two event filters, mirroring the source paper's stated inclusion rule:
#   keep an event only if the TARGETED cell itself responded to its own stimulation.
# "Responded" operationalised two ways so the choice is visible:
#   A) absolute: dF of target > 2 * (its pre-stimulation SD)
#   B) relative: target's dF is in the top decile of that event's cell responses
res = {}
for tag in ("A_abs2sd","B_topdecile","NONE"):
    per_pair = collections.defaultdict(list)
    n_an=0; used=0; n_ev=0; n_kept=0
    for i in ids:
        gp,lp,sp,vp = (d/f"{i}_gcamp.txt", d/f"{i}_labels.txt", d/f"{i}_stim_neurons.txt", d/f"{i}_stim_volume_i.txt")
        if not all(p.exists() for p in (gp,lp,sp,vp)): continue
        try: G=np.loadtxt(gp)
        except Exception: continue
        lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
        stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
        vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
        T,ncol=G.shape
        if len(stim)!=len(vols): continue
        n_an+=1
        cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*", x or ""))
        uniq={name for name,c in cnt.items() if c==1}
        keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
        if not keep: continue
        used+=1
        with np.errstate(all='ignore'):
            for sv,vi in zip(stim,vols):
                if sv<0 or vi>=T or vi<PRE: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                seg=G[max(0,vi-PRE):min(T,vi+POST), sv]
                if np.all(np.isnan(seg)): continue
                n_ev+=1
                tgt_d = np.nanmean(G[vi:min(T,vi+POST),sv]) - np.nanmean(G[max(0,vi-PRE):vi,sv])
                if tag=="A_abs2sd":
                    base=G[max(0,vi-PRE):vi,sv]; sd=np.nanstd(base)
                    ok = np.isfinite(tgt_d) and np.isfinite(sd) and sd>0 and tgt_d > 2*sd
                elif tag=="B_topdecile":
                    post=np.nanmean(G[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
                    dv=post-pre; v=dv[keep]; v=v[np.isfinite(v)]
                    ok = np.isfinite(tgt_d) and v.size>10 and tgt_d >= np.quantile(v,0.9)
                else:
                    ok = True
                if not ok: continue
                n_kept+=1
                post=np.nanmean(G[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
                dv=post-pre; v=dv[keep]
                m=np.nanmean(v); s=np.nanstd(v)
                if not np.isfinite(s) or s==0: continue
                z=(v-m)/s
                for kk,c in enumerate(keep):
                    if np.isfinite(z[kk]): per_pair[(lab[sv],lab[c])].append((i,float(z[kk])))
    rng=np.random.default_rng(0)
    def sh(pp,minm):
        xs=[];ys=[]
        for k,v in pp.items():
            if len(v)<minm: continue
            idx=rng.permutation(len(v)); h=len(v)//2
            xs.append(np.mean([v[j][1] for j in idx[:h]])); ys.append(np.mean([v[j][1] for j in idx[h:]]))
        if len(xs)<50: return None,None,0
        r=np.corrcoef(xs,ys)[0,1]; return float(r),float(2*r/(1+r)),len(xs)
    row={"animals_used":used,"events_total":n_ev,"events_kept":n_kept,
         "keep_frac":n_kept/max(n_ev,1),"n_pairs":len(per_pair),
         "n_meas":sum(len(v) for v in per_pair.values())}
    for m in (4,10,20):
        r,rf,n=sh(per_pair,m); row[f"r_min{m}"]=r; row[f"rfull_min{m}"]=rf; row[f"n_min{m}"]=n
    res[tag]=row
    print(f"  === 过滤 {tag} ===")
    print(f"    动物 {used}  事件 {n_ev:,} -> 保留 {n_kept:,} ({100*row['keep_frac']:.1f}%)  配对 {row['n_pairs']:,}  测量 {row['n_meas']:,}")
    for m in (4,10,20):
        print(f"      >= {m:>2} 次: r={row[f'r_min{m}'] if row[f'r_min{m}'] is None else round(row[f'r_min{m}'],4)}  "
              f"r_full={row[f'rfull_min{m}'] if row[f'rfull_min{m}'] is None else round(row[f'rfull_min{m}'],4)}  n={row[f'n_min{m}']:,}")
    print()
pathlib.Path("/tmp/osf/reliab4.json").write_text(json.dumps(res,indent=2))
