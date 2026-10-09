"""Fast iteration harness: run the criterion on ONE animal and print diagnostics.
Only when the pass rate is plausible does the full run get launched."""
import numpy as np, pathlib, re, collections, sys
DATA=pathlib.Path("/tmp/osf/w/exported_data")
SHIFT=60; AMPL_THR=1.0; DERIV_THR=1.0; AMPL_MIN=10; DERIV_MIN=4
def longest_run(mask):
    if not mask.any(): return 0
    best=cur=0
    for b in mask:
        cur=cur+1 if b else 0; best=max(best,cur)
    return best
def run(animal, verbose=True):
    G=np.loadtxt(DATA/f"{animal}_gcamp.txt")
    lab=[x.strip() for x in (DATA/f"{animal}_labels.txt").read_text(errors="replace").split("\n")]
    stim=[int(x) for x in (DATA/f"{animal}_stim_neurons.txt").read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in (DATA/f"{animal}_stim_volume_i.txt").read_text().split() if x.strip().isdigit()]
    T,ncol=G.shape
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
    uniq={n for n,c in cnt.items() if c==1}
    ev=0; ok=0; why=collections.Counter(); stats=[]
    with np.errstate(all='ignore'):
        for k,(sv,vi) in enumerate(zip(stim,vols)):
            if sv<0 or vi<SHIFT or vi+SHIFT>=T: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            ev+=1
            inter=(vols[k+1]-vi) if k+1<len(vols) else 62
            mv=max(AMPL_MIN+2, min(int((inter*0.5-5)/0.5), 60))
            end=min(T, vi+mv); raw=G[vi-SHIFT:end,:]
            if raw.shape[0]<SHIFT+AMPL_MIN: why["short"]+=1; continue
            base=np.nanmean(raw[SHIFT//2:SHIFT,:],axis=0); seg=raw-base
            absmax_cell=np.nanmax(np.abs(seg[:SHIFT,:]),axis=0)
            post=seg[SHIFT:,:]
            th=AMPL_THR*absmax_cell[sv]                       # <-- FIX: target's scalar
            r=post[:,sv]
            r1a=longest_run(r>th); r1a2=longest_run(r>0.5*th)
            r1b=longest_run(r<-th); r1b2=longest_run(r<-0.5*th)
            ampl_ok=(r1a>AMPL_MIN) or (r1a2>2*AMPL_MIN) or (r1b>AMPL_MIN) or (r1b2>2*AMPL_MIN)
            dr=np.gradient(seg,axis=0)
            prev_dr=np.mean(np.abs(dr[0:max(1,SHIFT-6),:]),axis=0)
            pre_avg=np.median(seg[:SHIFT,:],axis=0); pre_avg=np.where(np.abs(pre_avg)<1e-12,1e-12,pre_avg)
            frac=np.abs(dr[SHIFT:,sv]-prev_dr[sv])/np.abs(pre_avg[sv])
            deriv_ok=int(np.sum(frac>DERIV_THR))>=DERIV_MIN
            if ampl_ok and deriv_ok: ok+=1
            why["ampl" if not ampl_ok else ("deriv" if not deriv_ok else "pass")]+=1
            stats.append((absmax_cell[sv], float(np.nanmax(r)), r1a, r1a2, int(np.sum(frac>DERIV_THR))))
    if verbose:
        print(f"  动物 {animal}: 事件 {ev} -> 通过 {ok} ({100*ok/max(ev,1):.1f}%)   {dict(why)}")
        if stats:
            A=np.array(stats)
            print(f"    absmax 中位 {np.median(A[:,0]):.2f}  post峰 中位 {np.median(A[:,1]):.2f}  "
                  f"r1a 中位 {np.median(A[:,2]):.0f}  r1a2 中位 {np.median(A[:,3]):.0f}  "
                  f"deriv 计数中位 {np.median(A[:,4]):.0f}")
    return ev, ok
if __name__=="__main__":
    print("  === 先在 5 只动物上验证判据形状 ===")
    for a in (0,1,2,3,4): 
        try: run(a)
        except Exception as e: print(f"  动物 {a}: 异常 {type(e).__name__}: {e}")
