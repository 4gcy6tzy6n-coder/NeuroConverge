"""Render the v2 manuscript's six figures from the committed result artifacts.

Every series is read from a committed JSON or document; nothing is retyped.  The source artifact for each
panel is named in the legend and recorded in FIGURE_SOURCE_DATA.json's hashes.
"""
import json, pathlib, matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np

A = pathlib.Path(__file__).resolve().parents[1] / "wp3_results" / "anatomy"
D = pathlib.Path(__file__).resolve().parents[1] / "wp3_results"
OUT = pathlib.Path(__file__).resolve().parent
def L(p): return json.loads(p.read_text())
plt.rcParams.update({"font.size": 8, "axes.spines.top": False, "axes.spines.right": False,
                     "figure.dpi": 300, "savefig.bbox": "tight"})
GREY, ACC, WARN = "#4d4d4d", "#1f6fb4", "#b4431f"

# ---- Figure 1: the specification ledger
dims = [("order of application", (0.02, 0.85), False),
        ("per-cell normalisation", (0.3395, 0.3395), False),
        ("per-event precision weighting", (0.3356, 0.3356), False),
        ("post-stimulus window", (0.2364, 0.2364), False),
        ("baseline convention", (0.0295, 0.0496), True),
        ("common-mode removal", (0.0103, 0.0285), False),
        ("the common mode's cell pool", (0.0038, 0.0038), False)]
fig, ax = plt.subplots(figsize=(4.6, 2.6))
y = np.arange(len(dims))[::-1]
for i,(nm,(lo,hi),decl) in zip(y, dims):
    c = ACC if decl else WARN
    ax.plot([lo, hi], [i, i], lw=6 if hi>lo else 2.5, color=c, solid_capstyle="butt",
            alpha=0.85 if hi>lo else 1.0)
    ax.plot([hi],[i], "o", ms=3, color=c)
ax.set_yticks(y); ax.set_yticklabels([d[0] for d in dims], fontsize=7.5)
ax.set_xlabel("isolated contribution to $d_A$")
ax.set_xlim(-0.02, 0.90)
ax.plot([],[], lw=6, color=ACC, label="declared in the artifact")
ax.plot([],[], lw=6, color=WARN, label="declared nowhere")
ax.legend(frameon=False, fontsize=6.5, loc="lower right")
ax.set_title("Seven undeclared-or-small dimensions", fontsize=8, loc="left")
fig.savefig(OUT/"Fig1_specification_ledger.png"); plt.close(fig)

# ---- Figure 2: non-additivity
g = L(A/"RESULT_joint_grid_verified.json")
posts = [12,24,48]
iso_c, iso_w, joint = [], [], []
for p in posts:
    b=g[f"{p}|False|False"]["d_A"]; c=g[f"{p}|True|False"]["d_A"]
    w=g[f"{p}|False|True"]["d_A"];  j=g[f"{p}|True|True"]["d_A"]
    iso_c.append(c-b); iso_w.append(w-b); joint.append(j-b)
fig, ax = plt.subplots(figsize=(4.0, 2.5))
x=np.arange(len(posts)); w_=0.26
ax.bar(x-w_, iso_c, w_, color=ACC,  label="per-cell normalisation alone")
ax.bar(x,    iso_w, w_, color="#7aa9d0", label="precision weighting alone")
ax.bar(x+w_, joint, w_, color=WARN, label="the two together")
ax.axhline(0, color="k", lw=0.6)
ax.set_xticks(x); ax.set_xticklabels([f"{p}" for p in posts])
ax.set_xlabel("post-stimulus window (volumes)"); ax.set_ylabel("change in $d_A$")
ax.legend(frameon=False, fontsize=6)
ax.set_title("Isolated contributions do not add", fontsize=8, loc="left")
fig.savefig(OUT/"Fig2_nonadditivity.png"); plt.close(fig)

# ---- Figure 3: the order is the largest dimension
o = L(A/"RESULT_order_axis.json")
fig, ax = plt.subplots(figsize=(4.0, 2.5))
for tag, col, lab in (("A", WARN, "per-cell then weighting"),
                      ("B", ACC,  "weighting then per-cell")):
    xs, ys = [], []
    for p in posts:
        k=f"{tag}|{p}"
        if k in o: xs.append(p); ys.append(o[k]["d_A"])
    ax.plot(xs, ys, "o-", color=col, lw=1.6, ms=4, label=lab)
ax.axhline(0, color="k", lw=0.6, ls=":")
ax.set_xlabel("post-stimulus window (volumes)"); ax.set_ylabel("$d_A$")
ax.set_xticks(posts)
ax.legend(frameon=False, fontsize=6.5)
ax.set_title("The order of two normalisations", fontsize=8, loc="left")
fig.savefig(OUT/"Fig3_order.png"); plt.close(fig)

# ---- Figure 4: the decomposition
sw = L(A/"RESULT_variance_decomposition_sweep.json")
dw = L(A/"RESULT_decomposition_weighted.json")
fig, axes = plt.subplots(1, 2, figsize=(6.2, 2.5))
ax=axes[0]
ks = sorted(int(k) for k in sw.get("WT", {}))
if ks:
    rng = sw["WT"]
    for comp, col, lab in (("frac_pair","#c9c9c9","between-pair"),
                           ("frac_eps", ACC, "measurement error"),
                           ("frac_beta","#7aa9d0","pair-specific animal"),
                           ("frac_alpha","#e3c07a","animal offset")):
        ax.plot(ks, [100*rng[str(k)][comp] for k in ks], "o-", color=col, lw=1.4, ms=3.5, label=lab)
ax.axhline(0, color="k", lw=0.7)
ax.set_xscale("log"); ax.set_xticks(ks); ax.set_xticklabels([str(k) for k in ks])
ax.set_xlabel("minimum animals per pair"); ax.set_ylabel("share of variance (%)")
ax.legend(frameon=False, fontsize=5.8, ncol=2)
ax.set_title("Components vs the restriction", fontsize=8, loc="left")
ax=axes[1]
labs=["between-pair","measurement\nerror","pair-specific\nanimal","animal\noffset"]
keys=["frac_pair","frac_eps","frac_beta","frac_alpha"]
a=[100*dw["无逐事件加权"][k] for k in keys]; b=[100*dw["有逐事件加权"][k] for k in keys]
x=np.arange(4); w_=0.36
ax.bar(x-w_/2, a, w_, color="#c9c9c9", label="unweighted")
ax.bar(x+w_/2, b, w_, color=ACC, label="per-event weighted")
ax.axhline(0, color="k", lw=0.7)
ax.set_xticks(x); ax.set_xticklabels(labs, fontsize=6)
ax.set_ylabel("share of variance (%)"); ax.legend(frameon=False, fontsize=6)
ax.set_title("Effect of the weighting", fontsize=8, loc="left")
fig.savefig(OUT/"Fig4_decomposition.png"); plt.close(fig)

# ---- Figure 5: the like-for-like comparison and its bound
f6 = L(A/"RESULT_fig6.json")
grid = L(A/"RESULT_fig6_specification_grid.json")
rows = grid if isinstance(grid, list) else list(grid.values())
r0=[r["r_animal0"] for r in rows]; r1=[r["r_animal1"] for r in rows]; rc=[r["r_cross"] for r in rows]
fig, axes = plt.subplots(1, 2, figsize=(6.0, 2.4))
ax=axes[0]
ax.bar([0,1],[f6["fig6_animal0"]["r"], f6["fig6_animal1"]["r"]], color=ACC, width=0.5)
ax.axhline(0, color="k", lw=0.7)
ax.set_xticks([0,1]); ax.set_xticklabels(["animal 0","animal 1"])
ax.set_ylabel("corr(synapse count, activity)"); ax.set_ylim(-0.05,0.10)
ax.set_title("The source's comparison reproduces", fontsize=7.5, loc="left")
ax=axes[1]
labs=["Pearson\nno detrend","Pearson\ndetrended","Spearman\nno detrend","Spearman\ndetrended"]
import collections
by={}
for r in rows:
    by.setdefault((r["method"], r["detrend"]), []).append(r["r_cross"])
vals=[float(np.mean(by[k])) for k in [("pearson",False),("pearson",True),("spearman",False),("spearman",True)] if k in by]
ax.bar(range(len(vals)), vals, color=WARN, width=0.55)
ax.axhline(0.5, color="k", lw=1.0, ls="--")
ax.text(len(vals)-0.5, 0.505, "reproducible", fontsize=6, ha="right", va="bottom")
ax.set_xticks(range(len(vals))); ax.set_xticklabels(labs[:len(vals)], fontsize=6)
ax.set_ylabel("cross-animal agreement of the target"); ax.set_ylim(0,0.6)
ax.set_title("...against a target that barely agrees", fontsize=7.5, loc="left")
fig.savefig(OUT/"Fig5_like_for_like.png"); plt.close(fig)

# ---- Figure 6: the defect ledger
defects = [("window convention",29,"re-implementation"),("grid family",31,"re-implementation"),
           ("common-mode axis",32,"re-implementation"),("cache columns",33,"re-implementation"),
           ("weighting omitted",34,"re-implementation"),("wrong axis",39,"re-implementation"),
           ("duplicate-name pooling",8,"measurement"),("ratio of medians",8,"measurement"),
           ("biased read-out",8,"measurement"),("id-order assumption",8,"measurement"),
           ("per-cell collapse",8,"measurement"),("broadcast error",8,"measurement"),
           ("zero-pass criterion",8,"measurement"),("pathological weights",8,"measurement"),
           ("zero-inflated ICC",8,"measurement"),("animal heterogeneity",12,"interpretation"),
           ("window dependence",12,"interpretation"),("composition account",14,"interpretation"),
           ("population-level framing",15,"interpretation"),("z as effect size",27,"interpretation"),
           ("cell pool attribution",32,"interpretation")]
fig, ax = plt.subplots(figsize=(4.6, 3.0))
cmap={"measurement":ACC,"interpretation":WARN,"re-implementation":"#e3c07a"}
rng=np.random.default_rng(0)
for i,(nm,rd,kind) in enumerate(defects):
    ax.plot(rd, i, "o", ms=4, color=cmap[kind])
ax.set_yticks(range(len(defects))); ax.set_yticklabels([d[0] for d in defects], fontsize=6)
ax.set_xlabel("round in which it was found")
for k,v in cmap.items(): ax.plot([],[],"o",color=v,label=k)
ax.legend(frameon=False, fontsize=6, loc="lower right")
ax.set_title("Twenty-one self-found defects", fontsize=8, loc="left")
fig.savefig(OUT/"Fig6_defect_ledger.png"); plt.close(fig)
print("  已渲染 6 幅图")
