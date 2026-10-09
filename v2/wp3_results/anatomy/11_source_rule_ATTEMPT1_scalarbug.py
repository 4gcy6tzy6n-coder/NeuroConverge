"""Implement the source's autoresponse criterion (pumpprobe/Fconn.py) and re-run the contrasts.

Specification traced in SOURCE_RULE_RECOVERED.md and SPECIFICATION_COMPLETE.md:
  shift_vol = 60 (delta_t_pre = 30.0 s at dt = 0.5)      baseline_range = [30, 60]
  max_vol_n = int((int_btw_stim - 5)/dt)                 ~52 volumes at 31 s spacing
  ampl_thresh = 1.0   deriv_thresh = 1.0
  ampl_min_vols = 10  deriv_min_vols = 4
  criterion 1a  : run of r >  +absmax*ampl_thresh        longer than 10
  criterion 1a2 : run of r >  +absmax*0.5*ampl_thresh    longer than 20
  criterion 1b/b2: the same two, negative
  derivative    : sum(|post_dr - prev_dr| / pre_avg_sig > deriv_thresh) >= 4
                  prev_dr = mean(|dr[0:shift_vol-6]|) ;  pre_avg_sig = median(pre[0:shift_vol])
OMITTED, and recorded rather than silently skipped: criterion 2 (the tail rule for previously-selected
neurons, which requires tracking selection across consecutive stimulations), criterion 2* (the slope
check), and the exact Savitzky-Golay derivative (np.gradient is used instead).
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
        cur = cur+1 if b else 0
        best=max(best,cur)
    return best

def target_passes(seg, shift, absmax, pre, dt=0.5):
    """seg: baseline-subtracted segment, index 0 = start of pre-window."""
    post = seg[shift:]
    if post.size < AMPL_MIN: return False, {}
    # ---- amplitude criteria 1a/1a2/1b/1b2, contiguous runs
    th = AMPL_THR*absmax
    c1a  = post >  th;            c1a2 = post >  0.5*th
    c1b  = post < -th;            c1b2 = post < -0.5*th
    r1a=longest_run(c1a); r1a2=longest_run(c1a2); r1b=longest_run(c1b); r1b2=longest_run(c1b2)
    ampl_ok = (r1a>AMPL_MIN) or (r1a2>2*AMPL_MIN) or (r1b>AMPL_MIN) or (r1b2>2*AMPL_MIN)
    # ---- derivative criterion
    dr = np.gradient(seg)
    prev_dr = np.mean(np.abs(dr[0:max(1,shift-6)])) or 1e-12
    pre_avg = np.median(pre) or 1e-12
    post_dr = dr[shift:]
    deriv_ok = int(np.sum(np.abs(post_dr-prev_dr)/pre_avg > DERIV_THR)) >= DERIV_MIN
    return (ampl_ok and deriv_ok), {"r1a":r1a,"r1a2":r1a2,"r1b":r1b,"r1b2":r1b2,
                                    "ampl_ok":bool(ampl_ok),"deriv_ok":bool(deriv_ok)}

per_event=collections.defaultdict(list); n_an=0; n_ev=0; n_pass=0; rej=collections.Counter()
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
            # per-event window from the spaced interval, as the source does
            inter = (vols[k+1]-vi) if k+1<len(vols) else 62
            max_vol_n = int((inter*0.5 - 5)/0.5)
            max_vol_n = max(10, min(max_vol_n, 60))
            end = min(T, vi+max_vol_n)
            if end-vi < AMPL_MIN+2: rej["short"]+=1; continue
            seg_raw = G[vi-SHIFT:end, :]                      # (SHIFT+post, cells)
            if seg_raw.shape[0] < SHIFT+AMPL_MIN: rej["short"]+=1; continue
            base = np.nanmean(seg_raw[SHIFT//2:SHIFT, :], axis=0)   # baseline_range=[30,60]
            seg = seg_raw - base
            pre = seg[:SHIFT, sv]
            absmax = np.nanmax(np.abs(pre)) if np.isfinite(pre).any() else np.nan
            if not np.isfinite(absmax) or absmax<=0: rej["no_absmax"]+=1; continue
            ok, info = target_passes(seg[:,sv], SHIFT, absmax, seg_raw[:SHIFT,sv])
            if not ok:
                rej["ampl" if not info.get("ampl_ok") else "deriv"]+=1; continue
            n_pass+=1
            r_restr = seg[SHIFT:, keep]                        # response = baseline-subtracted trace
            sm = np.nansum(r_restr, axis=0)                    # signed integral, the source's ampl_post without abs
            for kk,c in enumerate(keep):
                if not np.isfinite(sm[kk]): continue
                tg=lab[sv]; rc=lab[c]
                i_,j_=idx.get(tg),idx.get(rc)
                if i_ is None or j_ is None: continue
                per_event[(i_,j_, "conn" if conn[i_,j_] else "unconn")].append((i,float(sm[kk])))
print(f"  {n_an} 只动物   事件 {n_ev:,} -> 通过 {n_pass:,} ({100*n_pass/max(n_ev,1):.1f}%)")
print(f"  拒绝原因: {dict(rej)}")
# animal-level paired contrast on this read-out
from collections import defaultdict
byA=defaultdict(lambda: {"conn":[], "unconn":[]})
for (i_,j_,k),vals in per_event.items():
    for (an,v) in vals: byA[an][k].append(v)
d=[]
for an,dd in byA.items():
    if dd["conn"] and dd["unconn"]:
        d.append((an, np.mean(dd["conn"])-np.mean(dd["unconn"])))
d=np.array([x[1] for x in d])
n=d.size; m=d.mean(); s=d.std(ddof=1); se=s/np.sqrt(n); t=m/se
print(f"\n  === 动物级配对对比（原文准则通过的事件）===")
print(f"    n={n}  差 {m:+.5f}  跨动物SD {s:.5f}  t={t:.3f}  d={m/s:.4f}")
out={"n_animals":n_an,"n_events":n_ev,"n_pass":n_pass,"pass_frac":n_pass/max(n_ev,1),
     "rejections":dict(rej),"n_animals_with_both":int(n),"paired_diff":float(m),
     "sd":float(s),"t":float(t),"d":float(m/s),"SHIFT":SHIFT,
     "ampl_min_vols":AMPL_MIN,"deriv_min_vols":DERIV_MIN}
json.dump(out, open("/tmp/osf/sourcerule.json","w"), indent=2)
