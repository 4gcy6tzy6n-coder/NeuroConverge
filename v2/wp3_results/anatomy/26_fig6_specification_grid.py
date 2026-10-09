"""Is V2-C2 robust? A specification grid for the Fig-6 reproduction and its bound.

V2-C2 is the one live claim never stress-tested.  It states that the source's own
anatomy-versus-spontaneous-activity comparison reproduces at r = +0.0368 and -0.0064 in its two animals, and
that the quantity it predicts has cross-animal agreement of only r = 0.208 on the 23 shared cells.

The same treatment rounds 26 to 29 applied to V2-C3: vary every defensible choice and see whether the numbers
move.

Grid, per animal:
  transform : raw fluorescence  |  dF/F against the session median  |  z-score each cell
  correlate : Pearson             |  Spearman
  detrend   : none                |  remove each cell's linear trend
Both quantities are recomputed at each cell: the animal's own anatomy-activity correlation, and the
cross-animal agreement of the two animals' correlation matrices on their shared cells.
"""
import numpy as np, json, pathlib, csv, re, collections, itertools
SP=pathlib.Path("/tmp/osf/sp/spont_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
NAMES=set(); rows=[]
with open(WNA/"aconnectome_witvliet_2020_8.csv", newline="") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append((r["pre"],r["post"],r["type"],float(r["synapses"]))); NAMES.add(r["pre"]); NAMES.add(r["post"])
with open(WNA/"aconnectome_white_1986_whole.csv", newline="") as fh:
    for r in csv.DictReader(fh, delimiter="\t"):
        rows.append((r["pre"],r["post"],r["type"],float(r["synapses"]))); NAMES.add(r["pre"]); NAMES.add(r["post"])
names=sorted(NAMES); ni={n:i for i,n in enumerate(names)}; M=len(names)
chem=np.zeros((M,M)); gap=np.zeros((M,M))
for p,q,ty,s in rows:
    if p not in ni or q not in ni: continue
    if ty=="chemical": chem[ni[p],ni[q]]+=s
    elif ty=="electrical": gap[ni[p],ni[q]]+=s; gap[ni[q],ni[p]]+=s
anat=chem+gap
def load(a):
    G=np.loadtxt(SP/f"{a}_gcamp.txt")
    lab=[x.strip() for x in (SP/f"{a}_labels.txt").read_text(errors="replace").split("\n")]
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
    uniq={k for k,v in cnt.items() if v==1}
    cols=[c for c in range(min(G.shape[1],len(lab))) if lab[c] in uniq]
    return G[:,cols], [lab[c] for c in cols]
def prep(X, transform, detrend):
    X=np.asarray(X,float)
    if transform=="raw": Y=X.copy()
    elif transform=="dff":
        med=np.nanmedian(X,axis=0); med=np.where(med!=0,med,np.nan)
        Y=(X-med)/med
    else:  # z
        mu=np.nanmean(X,axis=0); sd=np.nanstd(X,axis=0); sd=np.where(sd>0,sd,np.nan)
        Y=(X-mu)/sd
    if detrend:
        t=np.arange(Y.shape[0],dtype=float); t=t-t.mean()
        for k in range(Y.shape[1]):
            y=Y[:,k]; m=np.isfinite(y)
            if m.sum()>10:
                b=np.polyfit(t[m],y[m],1); Y[m,k]=y[m]-np.polyval(b,t[m])
    return Y
def corrmat(Y, method):
    Y=np.nan_to_num(Y,nan=0.0)
    if method=="pearson": return np.corrcoef(Y.T)
    # spearman: rank each column then Pearson
    R=np.apply_along_axis(lambda v: np.argsort(np.argsort(v)),0,Y)
    return np.corrcoef(R.T)
A0,nm0=load("0"); A1,nm1=load("1")
shared=sorted(set(nm0)&set(nm1))
print(f"  动物 0: {A0.shape}  动物 1: {A1.shape}  共享名 {len(shared)}\n")
out=[]
print(f"  {'transform':>10} {'method':>9} {'detrend':>8} | {'r_animal0':>10} {'r_animal1':>10} | {'r_cross':>9} {'n_shared':>9}")
for transform,method,detrend in itertools.product(("raw","dff","z"),("pearson","spearman"),(False,True)):
    Y0=corrmat(prep(A0,transform,detrend),method)
    Y1=corrmat(prep(A1,transform,detrend),method)
    def fig6(nm,C):
        ii=[ni[n] for n in nm if n in ni]; kk=[k for k,n in enumerate(nm) if n in ni]
        if len(kk)<20: return None
        Am=anat[np.ix_(ii,ii)]; Cc=C[np.ix_(kk,kk)]
        off=~np.eye(len(kk),dtype=bool)
        x=Am[off]; y=Cc[off]; m=np.isfinite(x)&np.isfinite(y)
        return float(np.corrcoef(x[m],y[m])[0,1])
    r0=fig6(nm0,Y0); r1=fig6(nm1,Y1)
    i0=[nm0.index(n) for n in shared]; i1=[nm1.index(n) for n in shared]
    if len(shared)>=15:
        B0=Y0[np.ix_(i0,i0)]; B1=Y1[np.ix_(i1,i1)]
        off=~np.eye(len(shared),dtype=bool)
        rc=float(np.corrcoef(B0[off],B1[off])[0,1])
    else: rc=float('nan')
    out.append({"transform":transform,"method":method,"detrend":detrend,
                "r_animal0":r0,"r_animal1":r1,"r_cross":rc,"n_shared":len(shared)})
    print(f"  {transform:>10} {method:>9} {str(detrend):>8} | {r0:>10.4f} {r1:>10.4f} | {rc:>9.4f} {len(shared):>9}")
a0=np.array([o["r_animal0"] for o in out]); a1=np.array([o["r_animal1"] for o in out]); cr=np.array([o["r_cross"] for o in out])
print(f"\n  === 跨规格范围 ===")
print(f"    动物0 的解剖-活动相关: {a0.min():+.4f}..{a0.max():+.4f}   极差 {a0.max()-a0.min():.4f}")
print(f"    动物1 的解剖-活动相关: {a1.min():+.4f}..{a1.max():+.4f}   极差 {a1.max()-a1.min():.4f}")
print(f"    跨动物一致性 (V2-C2 边界): {cr.min():+.4f}..{cr.max():+.4f}   极差 {cr.max()-cr.min():.4f}")
print(f"\n  === 与 V2-C2 所报值对照 ===")
print(f"    V2-C2 报: 动物0 +0.0368, 动物1 -0.0064, 跨动物 +0.2084")
for o in out:
    tag=" <- V2-C2 的规格" if (o["transform"]=="raw" and o["method"]=="pearson" and not o["detrend"]) else ""
    if tag: print(f"    该规格: 动物0 {o['r_animal0']:+.4f}, 动物1 {o['r_animal1']:+.4f}, 跨动物 {o['r_cross']:+.4f}{tag}")
print(f"\n  === 判读 ===")
print(f"    若跨动物一致性在所有规格下都远低于动物内 ⟹ V2-C2 的核心成立")
print(f"    若某个规格使其接近或超过 0.5 ⟹ 边界不稳健")
json.dump(out, open("/tmp/osf/fig6_grid.json","w"), indent=2)
