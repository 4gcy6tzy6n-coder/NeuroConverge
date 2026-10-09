"""Reproduce the source's Fig-6 left bar, and test whether n=2 can support it.

The paper states: "A matrix of bare anatomical weights (synapse counts) was a poor predictor of the
correlations of spontaneous activity (left bar, Fig ...)".  Its spontaneous-activity data, in the same
OSF record, contains TWO animals.  This script:
  1. builds each animal's spontaneous activity correlation matrix,
  2. builds the synapse-count matrix restricted to the shared cell names,
  3. reproduces the left bar as corr(synapse count, activity correlation),
  4. and asks whether the two animals' correlation matrices agree, which is what decides whether a
     two-animal estimate of (3) can support a general claim.
"""
import numpy as np, csv, pathlib, re, collections, json, itertools
SP=pathlib.Path("/tmp/osf/sp/spont_data"); WNA=pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")
# synapse-count matrix over the union of names, built from both source tables
NAMES=set()
def load(fn):
    rows=[]
    with open(WNA/fn, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            rows.append((r["pre"], r["post"], r["type"], float(r["synapses"])))
            NAMES.add(r["pre"]); NAMES.add(r["post"])
    return rows
rows=load("aconnectome_witvliet_2020_8.csv")+load("aconnectome_white_1986_whole.csv")
names=sorted(NAMES); ni={n:i for i,n in enumerate(names)}; M=len(names)
chem=np.zeros((M,M)); gap=np.zeros((M,M))
for p,q,ty,s in rows:
    if p not in ni or q not in ni: continue
    if ty=="chemical": chem[ni[p],ni[q]]+=s
    elif ty=="electrical": gap[ni[p],ni[q]]+=s; gap[ni[q],ni[p]]+=s
anat=(chem+gap)
print(f"  解剖矩阵: {M} 个名字, chem 非零 {int((chem!=0).sum())}, gap 非零 {int((gap!=0).sum())}")

def animal(a):
    G=np.loadtxt(SP/f"{a}_gcamp.txt")
    lab=[x.strip() for x in (SP/f"{a}_labels.txt").read_text(errors="replace").split("\n")]
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*",x or ""))
    uniq={k for k,v in cnt.items() if v==1}
    cols=[c for c in range(min(G.shape[1],len(lab))) if lab[c] in uniq]
    nm=[lab[c] for c in cols]
    X=G[:, cols]
    # correlation between cells, on cells with enough non-nan variance
    good=[k for k in range(X.shape[1]) if np.isfinite(X[:,k]).sum()>50 and np.nanstd(X[:,k])>0]
    X=X[:, good]; nm=[nm[k] for k in good]
    C=np.corrcoef(np.nan_to_num(X, nan=0.0).T)
    return nm, C
nm0,C0=animal("0"); nm1,C1=animal("1")
print(f"\n  动物 0: {len(nm0)} 个可用细胞, 相关矩阵 {C0.shape}")
print(f"  动物 1: {len(nm1)} 个可用细胞, 相关矩阵 {C1.shape}")
def fig6(nm, C, label):
    """left bar: corr(synapse count, activity correlation) over pairs with anatomical connection info"""
    ii=[ni[n] for n in nm if n in ni]; kk=[k for k,n in enumerate(nm) if n in ni]
    if len(kk)<20: return None
    A=anat[np.ix_(ii,ii)]; Cc=C[np.ix_(kk,kk)]
    off=~np.eye(len(kk),dtype=bool)
    # the paper compares the anatomical weight magnitude against the activity correlation, signed
    x=A[off]; y=Cc[off]
    m=np.isfinite(x)&np.isfinite(y)
    r=np.corrcoef(x[m],y[m])[0,1]
    rs=np.corrcoef(np.log1p(x[m]),y[m])[0,1]
    print(f"    {label}: n_pairs {int(m.sum()):,}  corr(synapse, activity) = {r:+.4f}   "
          f"corr(log1p(synapse), activity) = {rs:+.4f}")
    return {"label":label,"n_pairs":int(m.sum()),"r":float(r),"r_log":float(rs)}
print(f"\n  === 复算原文 Fig 6 左柱 ===")
f0=fig6(nm0,C0,"动物 0"); f1=fig6(nm1,C1,"动物 1")
# cross-animal agreement of the activity correlation matrix
shared=sorted(set(nm0)&set(nm1))
print(f"\n  === 两只动物的活动相关矩阵是否一致 ===")
print(f"    共享细胞名: {len(shared)}")
if len(shared)>=15:
    i0=[nm0.index(n) for n in shared]; i1=[nm1.index(n) for n in shared]
    A0=C0[np.ix_(i0,i0)]; A1=C1[np.ix_(i1,i1)]
    off=~np.eye(len(shared),dtype=bool)
    r=np.corrcoef(A0[off],A1[off])[0,1]
    print(f"    同一批 {len(shared)} 个细胞的配对相关矩阵, 两动物间 corr = {r:+.4f}")
    print(f"    配对间相关的 SD: 动物0 {A0[off].std():.4f}  动物1 {A1[off].std():.4f}")
out={"M":M,"n0":len(nm0),"n1":len(nm1),"shared":len(shared),
     "fig6_animal0":f0,"fig6_animal1":f1}
if len(shared)>=15: out["cross_animal_r_of_corr_matrix"]=float(r)
json.dump(out, open("/tmp/osf/fig6.json","w"), indent=2)
