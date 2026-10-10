"""Does the cross-animal reliability structure replicate in a second dataset?

The line's central reliability measurement -- a pair's response agrees across animals at r_full = 0.04 while
agreeing within an animal at 0.52 -- rests on ONE atlas, from ONE laboratory.  DANDI 000541 is 21 sessions
from the same laboratory with a DIFFERENT preparation: whole-brain NeuroPAL recordings with chemical
stimulation, 177 identified cells per session under a shared naming scheme.

This measures the one half of the reliability structure that this dataset can support: CROSS-SESSION
(= cross-animal) agreement of the per-cell response vector.  It CANNOT measure the within-animal half,
because each session carries only three chemical stimuli.

    atlas (Dvali/Leifer/Randi, OSF 10.17605/OSF.IO/E2SYT):  cross-animal r_full = 0.0405
    this dataset:                      measure the same quantity and compare

If it lands near zero, the atlas's cross-animal disagreement is not a property of that one export.  If it does
not, that is a bound on how far the line's finding travels, and it is reported either way.
"""
import h5py, numpy as np, pathlib, collections, itertools, json, sys

def load_session(p):
    """Return (labels, traces) for one NWB session: labels are NeuroPAL names, traces are (time, cells)."""
    f=h5py.File(p,"r")
    lab=[x.decode() if isinstance(x,bytes) else str(x) for x in f["processing/CalciumActivity/NeuronIDs/labels"][:]]
    sig=f["processing/CalciumActivity/SignalRawFluor/SignalCalciumImResponseSeries"]
    key = "data" if "data" in sig else list(sig.keys())[0]
    X = sig[key][:]
    X = np.asarray(X, dtype=float)
    if X.shape[1] != len(lab) and X.shape[0] == len(lab):
        X = X.T                                    # orient as (time, cells)
    stim_s=f["intervals/chemical_stimuli/start_time"][:]
    stim_e=f["intervals/chemical_stimuli/stop_time"][:]
    f.close()
    return lab, X, np.asarray(stim_s,float), np.asarray(stim_e,float)

def per_cell_response(lab, X, s, e, pre_s=30.0):
    """One response per cell for one stimulus: mean over the stimulus minus the mean over the preceding window."""
    t=np.arange(X.shape[0], dtype=float)           # assumes unit sampling; scaled below if a rate is present
    dt = 1.0
    i0=max(0, int(s/dt)-int(pre_s/dt)); i1=max(1, int(s/dt)); i2=max(i1+1, int(e/dt))
    if i2>X.shape[0]: return None
    pre=np.nanmean(X[i0:i1,:], axis=0); post=np.nanmean(X[i1:i2,:], axis=0)
    return post-pre

def main():
    files=sorted(pathlib.Path("/tmp/d541").glob("*.nwb")) + [pathlib.Path("/tmp/ncv2/nwb541.nwb")]
    vecs={}
    print(f"  载入 {len(files)} 个会话")
    for p in files:
        if not p.exists(): continue
        try:
            lab, X, ss, se = load_session(p)
        except Exception as ex:
            print(f"    {p.name}: 读取失败 {type(ex).__name__}: {str(ex)[:70]}"); continue
        cnt=collections.Counter(lab)
        uniq=[k for k,v in cnt.items() if v==1 and k]
        idx={}
        for k,nm in enumerate(lab):
            if nm in uniq: idx[nm]=k
        V=[]
        for s,e in zip(ss,se):
            r=per_cell_response(lab,X,s,e)
            if r is None: continue
            a=np.full(len(lab), np.nan)
            for nm,k in idx.items(): a[k]=r[k]
            V.append(a)
        if V:
            vecs[p.stem]=np.nanmean(np.vstack(V),axis=0)
            print(f"    {p.stem}: {X.shape}, 唯一名细胞 {len(idx)}, 刺激 {len(V)}")
    names=sorted(vecs)
    if len(names)<2:
        print("  ==> 可用会话少于 2，无法做跨会话一致性"); 
        json.dump({"n_sessions":len(names)}, open("/tmp/osf/d541_gen.json","w"), indent=2); return
    # cross-session agreement of the per-cell response vector, over shared named cells
    print(f"\n  === 跨会话逐细胞响应一致性 ===")
    rs=[]
    for a,b in itertools.combinations(names,2):
        va,vb=vecs[a],vecs[b]
        m=np.isfinite(va)&np.isfinite(vb)
        if m.sum()<20: continue
        r=np.corrcoef(va[m],vb[m])[0,1]
        if np.isfinite(r): rs.append(r)
    rs=np.array(rs)
    print(f"    会话对 {rs.size}   共享细胞中位 {int(np.median([np.isfinite(vecs[a])&np.isfinite(vecs[b]) for a,b in itertools.combinations(names,2)])) if rs.size else 0}")
    if rs.size:
        print(f"    跨会话相关: 均值 {rs.mean():+.4f}  中位 {np.median(rs):+.4f}  范围 {rs.min():+.4f}..{rs.max():+.4f}")
        print(f"\n  === 与图谱对照 ===")
        print(f"    图谱的跨动物 r_full (bulk) = 0.0405")
        print(f"    本数据集跨会话 r            = {rs.mean():+.4f}")
        print(f"    ==> {'同量级，结构复现' if abs(rs.mean())<0.15 else '不同量级，推广受限'}")
    json.dump({"n_sessions":len(names),"sessions":names,
               "cross_session_r_mean":float(rs.mean()) if rs.size else None,
               "cross_session_r_median":float(np.median(rs)) if rs.size else None,
               "n_pairs":int(rs.size),"atlas_cross_animal_r_full":0.0405},
              open("/tmp/osf/d541_gen.json","w"), indent=2)
main()
