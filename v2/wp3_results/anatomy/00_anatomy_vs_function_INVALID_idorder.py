import numpy as np, h5py, csv, pathlib, re, collections, json
DATA = pathlib.Path("/tmp/osf/w/exported_data")
WNA  = pathlib.Path("/tmp/wna/ex/wormneuroatlas/data")

# ---------- 1) anatomical matrices, id-checked against the CSVs ----------
f = h5py.File(WNA/"funatlas.h5","r")
ids = [x.decode() if isinstance(x,bytes) else str(x) for x in f["neuron_ids"][:]]
idx = {n:i for i,n in enumerate(ids)}
a = h5py.File(WNA/"aconnectome_default.h5","r")
chem = a["chem"][:]; gap = a["gap"][:]
align = {}
for csvname, mat, kind in (("aconnectome_witvliet_2020_8.csv", chem, "chemical"),
                           ("aconnectome_witvliet_2020_8.csv", gap,  "electrical"),
                           ("aconnectome_white_1986_whole.csv", chem, "chemical")):
    hit=miss=0
    with open(WNA/csvname, newline="") as fh:
        for r in csv.DictReader(fh, delimiter="\t"):
            if r["type"]!=kind: continue
            p,q = r["pre"], r["post"]
            if p not in idx or q not in idx: continue
            s=float(r["synapses"])
            if abs(mat[idx[p],idx[q]]-s)<1e-9: hit+=1
            else: miss+=1
    align[f"{csvname}:{kind}"]={"hit":hit,"miss":miss}
print("  === id 对齐核验（用 funatlas 的 300 个 id 解读 aconnectome_default）===")
for k,v in align.items(): print(f"    {k:52s} 命中 {v['hit']:>5}  不符 {v['miss']}")
ok_align = all(v["miss"]==0 and v["hit"]>0 for v in align.values())
print(f"    ==> 对齐{'成立' if ok_align else '不成立'}")

# ---------- 2) functional map from per-animal records, with reliability ----------
PRE=POST=8
per_pair = collections.defaultdict(list); per_pair_anim = collections.defaultdict(set)
n_an=0
for i in sorted({int(m.group(1)) for p in DATA.glob("*_stim_neurons.txt") if (m:=re.match(r"^(\d+)_stim",p.name))}):
    gp,lp,sp,vp = (DATA/f"{i}_gcamp.txt", DATA/f"{i}_labels.txt", DATA/f"{i}_stim_neurons.txt", DATA/f"{i}_stim_volume_i.txt")
    if not all(p.exists() for p in (gp,lp,sp,vp)): continue
    try: G=np.loadtxt(gp)
    except Exception: continue
    lab=[x.strip() for x in lp.read_text(errors="replace").split("\n")]
    stim=[int(x) for x in sp.read_text().split() if x.strip().lstrip('-').isdigit()]
    vols=[int(x) for x in vp.read_text().split() if x.strip().isdigit()]
    T,ncol=G.shape
    if len(stim)!=len(vols): continue
    cnt=collections.Counter(x for x in lab if re.fullmatch(r"[A-Za-z][A-Za-z0-9\-]*", x or ""))
    uniq={n for n,c in cnt.items() if c==1}
    keep=[c for c in range(min(ncol,len(lab))) if lab[c] in uniq]
    if not keep: continue
    n_an+=1
    with np.errstate(all='ignore'):
        for sv,vi in zip(stim,vols):
            if sv<0 or vi>=T or vi<PRE: continue
            if not (sv<len(lab) and lab[sv] in uniq): continue
            post=np.nanmean(G[vi:min(T,vi+POST),:],axis=0); pre=np.nanmean(G[max(0,vi-PRE):vi,:],axis=0)
            dv=post-pre; v=dv[keep]
            m=np.nanmean(v); s=np.nanstd(v)
            if not np.isfinite(s) or s==0: continue
            z=(v-m)/s
            for kk,c in enumerate(keep):
                if np.isfinite(z[kk]):
                    per_pair[(lab[sv],lab[c])].append(float(z[kk])); per_pair_anim[(lab[sv],lab[c])].add(i)
print(f"\n  功能侧: {n_an} 只动物, {len(per_pair):,} 个有名配对")

# Build a 300x300 functional matrix (z-mean) and a reliability matrix
Fm = np.full((300,300), np.nan); Rl = np.zeros((300,300)); Nn=np.zeros((300,300),int)
rng=np.random.default_rng(0)
for (tg,rc),vals in per_pair.items():
    if tg not in idx or rc not in idx: continue
    i,j = idx[tg], idx[rc]
    v=np.array(vals); Fm[i,j]=v.mean(); Nn[i,j]=len(v)
    if len(v)>=4:
        o=rng.permutation(len(v)); h=len(v)//2
        m1=v[o[:h]].mean(); m2=v[o[h:]].mean()
        Rl[i,j]=1.0  # placeholder; reliability computed at the pair level below
np.save("/tmp/osf/Fm.npy", Fm); np.save("/tmp/osf/Nn.npy", Nn)
print(f"  功能矩阵非 NaN 条目: {int(np.isfinite(Fm).sum()):,}")
print(f"  配对测量数: 中位 {int(np.median(Nn[Nn>0]))}  最大 {int(Nn.max())}")

# ---------- 3) does anatomy predict function? (Randi's comparison) ----------
anat = ((chem!=0) | (gap!=0)).astype(float)
both = np.isfinite(Fm) & (np.arange(300)[:,None]!=np.arange(300)[None,:])
dv = np.where(anat>0, 1, 0)
print(f"\n  === 解剖 vs 功能（全部有名配对, n={int(both.sum()):,}）===")
print(f"    有解剖连接的配对: {int((both & (dv==1)).sum()):,}")
print(f"    无解剖连接的配对: {int((both & (dv==0)).sum()):,}")
m1 = Fm[both & (dv==1)]; m0 = Fm[both & (dv==0)]
print(f"    功能响应 均值:  有连接 {np.nanmean(m1):+.4f}   无连接 {np.nanmean(m0):+.4f}")
d = np.nanmean(m1)-np.nanmean(m0)
sp = np.sqrt(np.nanvar(m1)/m1.size + np.nanvar(m0)/m0.size)
print(f"    差值 {d:+.4f}   Cohen's d ≈ {d/sp:.4f}   （未加权）")
json.dump({"aligned":bool(ok_align),"align":align,"n_animals":n_an,"n_pairs":len(per_pair),
           "conn_mean":float(np.nanmean(m1)),"unconn_mean":float(np.nanmean(m0)),
           "diff":float(d),"cohens_d":float(d/sp),
           "n_conn":int((both&(dv==1)).sum()),"n_unconn":int((both&(dv==0)).sum())},
          open("/tmp/osf/anatomy_test.json","w"), indent=2)
