"""V2-C4's four values recomputed in a single framework: a 2x2 of specification and weighting.

V2-C4's range 0.085 to 0.729 mixes a weighted pipeline (10_robust_and_class.py) against three unweighted ones
(11b_source_rule.py, 12_inverse_variance_weighting.py).  Round 37 corrected the claim to say the range is
0.085 to 0.450 within the unweighted family and 0.39 to 0.73 within the weighted one, but that correction was
CONSTRUCTED by subtraction rather than measured.

This measures it.  Two specifications are implemented in one pass:

  NORULE : post-stimulus window from the stimulus volume, baseline the 30 volumes before it, mean over the
           window, per-volume across-cell common mode, per-cell mean over volumes   (10_robust_and_class.py)
  SOURCE : signed sum from 60 volumes before the stimulus to the end of the per-event analysis window, with
           the amplitude and derivative criteria applied to the target                    (11b_source_rule.py)

and each is computed with and without the per-event across-cell-SD weighting, giving four values in one
framework instead of four values from three scripts.
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
chem=c1+c2; gap=g1+g2; off=~np.eye(N,dtype=bool); CONN=((chem!=0)|(gap!=0))&off
SHIFT=60; AMPL_THR=1.0; DERIV_THR=1.0; AMPL_MIN=10; DERIV_MIN=4
def longest_run(mask):
    if not mask.any(): return 0
    best=cur=0
    for b in mask:
        cur=cur+1 if b else 0; best=max(best,cur)
    return best
def target_passes(seg, absmax_cell, target_col):
    post=seg[SHIFT:,:]; npost=post.shape[0]
    if npost<AMPL_MIN: return False
    r=post[:,target_col]; th=AMPL_THR*absmax_cell[target_col]
    ampl_ok=(longest_run(r>th)>AMPL_MIN) or (longest_run(r>0.5*th)>2*AMPL_MIN) \
          or (longest_run(r<-th)>AMPL_MIN) or (longest_run(r<-0.5*th)>2*AMPL_MIN)
    drc=np.gradient(seg[:,target_col])
    prev=np.mean(np.abs(drc[0:max(1,SHIFT-6)])); pre=np.median(seg[:SHIFT,target_col])
    if abs(pre)<1e-12: pre=1e-12
    frac=np.abs(drc[SHIFT:]-prev)/abs(pre)
    return bool(ampl_ok and int(np.sum(frac>DERIV_THR))>=DERIV_MIN)
def run(spec, weighted):
    per=collections.defaultdict(lambda: {"c":[], "u":[]}); nev=0
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
        with np.errstate(all='ignore'):
            for k,(sv,vi) in enumerate(zip(stim,vols)):
                if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
                if not (sv<len(lab) and lab[sv] in uniq): continue
                inter=(vols[k+1]-vi) if k+1<len(vols) else 62
                mv=max(12, min(int((inter*0.5-5)/0.5), 60))
                end=min(T, vi+mv)
                if end-vi<12: continue
                if spec=="SOURCE":
                    raw=G[vi-SHIFT:end,:]
                    base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0)
                    seg=raw-base
                    absmax=np.nanmax(np.abs(seg[:SHIFT,:]),axis=0)
                    if not target_passes(seg, absmax, sv): continue
                    val=np.nansum(seg[SHIFT:,keep],axis=0)
                    ref=np.nanstd(seg[SHIFT:,keep],axis=1) if weighted else None
                else:
                    post=G[vi:vi+24,:]; base=np.nanmean(G[vi-30:vi,:],axis=0)
                    seg=post-base
                    cm=np.nanmean(seg,axis=1,keepdims=True); dev=seg-cm
                    val=np.nanmean(dev[:,keep],axis=0)
                    ref=np.nanstd(dev[:,keep],axis=1) if weighted else None
                nev+=1
                if weighted and ref is not None:
                    sd=np.nanmedian(ref)
                    if not np.isfinite(sd) or sd<=0: continue
                    val=val/sd
                for kk,c in enumerate(keep):
                    v=val[kk]
                    if not np.isfinite(v): continue
                    tg=lab[sv]; rc=lab[c]
                    i_,j_=idx.get(tg),idx.get(rc)
                    if i_ is None or j_ is None: continue
                    per[i]["c" if CONN[i_,j_] else "u"].append(float(v))
    diffs=[]
    for i,d_ in per.items():
        if d_["c"] and d_["u"]: diffs.append(np.mean(d_["c"])-np.mean(d_["u"]))
    if len(diffs)<30: return None
    a=np.array(diffs); m=a.mean(); s=a.std(ddof=1)
    return {"n_animals":len(diffs),"events":nev,"diff":float(m),"sd":float(s),
            "d_A":float(m/s),"t":float(m/(s/math.sqrt(len(diffs))))}
print(f"  {'spec':>8} {'weighted':>9} {'animals':>8} {'events':>8} {'diff':>10} {'sd':>10} {'d_A':>8} {'t':>7}")
rows={}
for spec in ("NORULE","SOURCE"):
    for w in (False,True):
        r=run(spec,w)
        if r is None: print(f"  {spec:>8} {str(w):>9}  -- 不足"); continue
        rows[(spec,w)]=r
        print(f"  {spec:>8} {str(w):>9} {r['n_animals']:>8} {r['events']:>8} {r['diff']:>10.5f} {r['sd']:>10.5f} {r['d_A']:>8.4f} {r['t']:>7.3f}")
print(f"\n  === 同族内范围（这是要测的量）===")
for w in (False,True):
    vals=[rows[(s,w)]["d_A"] for s in ("NORULE","SOURCE") if (s,w) in rows]
    if vals: print(f"    {'加权' if w else '未加权'}族: {min(vals):.4f} .. {max(vals):.4f}   极差 {max(vals)-min(vals):.4f}")
if (("NORULE",False) in rows) and (("NORULE",True) in rows):
    print(f"\n  加权对 NORULE 的贡献: {rows[('NORULE',True)]['d_A']-rows[('NORULE',False)]['d_A']:+.4f}")
if (("SOURCE",False) in rows) and (("SOURCE",True) in rows):
    print(f"  加权对 SOURCE 的贡献: {rows[('SOURCE',True)]['d_A']-rows[('SOURCE',False)]['d_A']:+.4f}")
print(f"\n  === 与 V2-C4 所报四个值对照 ===")
print(f"    V2-C4: 0.7289 (10_robust, 有加权) · 0.4495 (11b, 无) · 0.1580 (12, 无) · 0.0852 (12, 无)")
for k,r in sorted(rows.items()): print(f"    本框架 {k[0]:>7} weighted={str(k[1]):>5}: d_A {r['d_A']:.4f}")
json.dump({f"{k[0]}|{k[1]}":v for k,v in rows.items()}, open("/tmp/osf/family2x2.json","w"), indent=2)
