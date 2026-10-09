"""Source autoresponse criterion, corrected to keep per-cell structure.

FIX APPLIED (defect 7 in this line): the first implementation collapsed
  prev_dr = np.average(np.abs(dr[0:shift-6]), axis=0)        (per-cell vector)
and
  pre_avg_sig = np.median(signal[i0:i0+shift_vol], axis=0)   (per-cell vector)
to scalars, and passed only the target's column into the criterion.  Result: 0 of 3,333 events passed.
Now the full segment is carried and per-cell quantities stay per-cell.
"""
import numpy as np, h5py, csv, pathlib, re, collections, json
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

SHIFT=60; AMPL_THR=1.0; DERIV_THR=1.0; AMPL_MIN=10; DERIV_MIN=4

def longest_run(mask):
    if not mask.any(): return 0
    best=cur=0
    for b in mask:
        cur=cur+1 if b else 0; best=max(best,cur)
    return best

def target_passes(seg, shift, absmax_cell, raw_pre_cell, target_col):  # raw_pre_cell kept for signature parity
    """seg: (shift+post, cells) baseline-subtracted.  All per-cell quantities stay per-cell."""
    post = seg[shift:, :]
    npost = post.shape[0]
    if npost < AMPL_MIN: return False, {"reason":"short"}
    r = post[:, target_col]
    th = AMPL_THR*absmax_cell[target_col]      # FIX: target's scalar, not the cell vector
    r1a =longest_run(r >  th);      r1a2=longest_run(r >  0.5*th)
    r1b =longest_run(r < -th);      r1b2=longest_run(r < -0.5*th)
    ampl_ok = (r1a>AMPL_MIN) or (r1a2>2*AMPL_MIN) or (r1b>AMPL_MIN) or (r1b2>2*AMPL_MIN)
    # derivative: per-cell prev_dr and pre_avg_sig, as the source
    # derivative for the target column only -- same per-cell definition, far cheaper
    dcol = np.gradient(seg[:, target_col])
    drc  = np.gradient(seg, axis=0)[:, target_col] if False else dcol
    prev_dr_t = np.mean(np.abs(drc[0:max(1,shift-6)]))
    pre_avg_t = np.median(seg[:shift, target_col])
    if abs(pre_avg_t)<1e-12: pre_avg_t=1e-12
    frac = np.abs(drc[shift:]-prev_dr_t)/abs(pre_avg_t)
    deriv_ok = int(np.sum(frac > DERIV_THR)) >= DERIV_MIN
    return (ampl_ok and deriv_ok), {"r1a":r1a,"r1a2":r1a2,"ampl_ok":bool(ampl_ok),"deriv_ok":bool(deriv_ok),"npost":npost}

per_event=collections.defaultdict(list)
n_an=0; n_ev=0; n_pass=0; rej=collections.Counter()
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
            max_vol_n=max(AMPL_MIN+2, min(int((inter*0.5-5)/0.5), 60))
            end=min(T, vi+max_vol_n)
            raw=G[vi-SHIFT:end,:]
            if raw.shape[0] < SHIFT+AMPL_MIN: rej["short"]+=1; continue
            base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
            seg=raw-base
            absmax_cell=np.nanmax(np.abs(seg[:SHIFT,:]),axis=0)
            ok,info=target_passes(seg, SHIFT, absmax_cell, raw[:SHIFT,sv], sv)
            if not ok:
                rej["ampl" if not info.get("ampl_ok") else "deriv"]+=1; continue
            n_pass+=1
            sm=np.nansum(seg[SHIFT:, keep], axis=0)
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                per_event[(i_,j_,"conn" if conn[i_,j_] else "unconn")].append((i,float(sm[kk])))
print(f"  {n_an} 只动物   事件 {n_ev:,} -> 通过 {n_pass:,} ({100*n_pass/max(n_ev,1):.1f}%)")
print(f"  拒绝原因: {dict(rej)}")
byA=collections.defaultdict(lambda:{"conn":[],"unconn":[]})
for (i_,j_,k),vals in per_event.items():
    for an,v in vals: byA[an][k].append(v)
d=np.array([np.mean(dd["conn"])-np.mean(dd["unconn"]) for dd in byA.values() if dd["conn"] and dd["unconn"]])
n=d.size
print(f"\n  === 动物级配对对比（原文准则通过的事件, 单位=动物）===")
if n>=5:
    m=d.mean(); s=d.std(ddof=1); se=s/np.sqrt(n); t=m/se
    print(f"    n={n}  差 {m:+.5f}  跨动物SD {s:.5f}  t={t:.3f}  d={m/s:.4f}")
    out={"n_animals":n_an,"n_events":n_ev,"n_pass":n_pass,"pass_frac":n_pass/max(n_ev,1),
         "rejections":dict(rej),"n_animals_both":int(n),"paired_diff":float(m),"sd":float(s),
         "t":float(t),"d":float(m/s)}
else:
    print(f"    n={n} —— 动物数不足以做配对对比")
    out={"n_animals":n_an,"n_events":n_ev,"n_pass":n_pass,"rejections":dict(rej),"n_animals_both":int(n)}
json.dump(out, open("/tmp/osf/sourcerule_fixed.json","w"), indent=2)
