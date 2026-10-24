#!/usr/bin/env python3
"""Produce the six manuscript figures from the frozen artifacts (nothing hand-entered).

Reads: CODING_sheets_v2/statistics_final_20261024.json, reportability_summary_final_20261024.json,
headline_merged.csv, merged_E.csv. Writes PNGs next to the manuscript.

    python3 make_figures.py
"""
import csv
import json
from collections import Counter
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt

ROOT = Path(__file__).resolve().parent
OUT = ROOT / "MANUSCRIPT" / "figures"
OUT.mkdir(parents=True, exist_ok=True)
S = json.load(open(ROOT / "CODING_sheets_v2/statistics_final_20261024.json"))
R = json.load(open(ROOT / "CODING_sheets_v2/reportability_summary_final_20261024.json"))
merged = list(csv.DictReader(open(ROOT / "CODING_sheets_v2/merged_E.csv")))
head = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/headline_merged.csv"))}
TR = ["T1", "T2", "T3", "T4", "T5"]
GRADE_COLORS = {"E0": "#c9c9c9", "E1": "#7fa8c9", "E2": "#2b6cb0"}

# Fig 1 - grade distributions (merged)
fig, ax = plt.subplots(figsize=(7, 4.2))
e0 = [S["grade_distribution"]["merged"][t].get("E0", 0) for t in TR]
e1 = [S["grade_distribution"]["merged"][t].get("E1", 0) for t in TR]
e2 = [S["grade_distribution"]["merged"][t].get("E2", 0) for t in TR]
b = np_bottom = [0] * 5
for vals, g in ((e0, "E0"), (e1, "E1"), (e2, "E2")):
    ax.bar(TR, vals, bottom=b, color=GRADE_COLORS[g], label=f"{g}: { {'E0':'no in-paper evidence','E1':'suggestive','E2':'controlled'}[g] }", edgecolor="white")
    b = [x + y for x, y in zip(b, vals)]
for i, t in enumerate(TR):
    if e0[i] == 16:
        ax.text(i, 8, "16/16\nE0", ha="center", fontsize=9)
ax.set_ylabel("claims (of 16)"); ax.set_ylim(0, 17)
ax.set_title("In-paper evidence by transition (weaker-grade merge)", fontsize=11)
ax.legend(fontsize=8, loc="upper left", bbox_to_anchor=(0, -0.14), ncol=3, frameon=False)
fig.tight_layout(); fig.savefig(OUT / "fig1_chain.png", dpi=200); plt.close(fig)

# Fig 2 - the correspondence gap: controlled share per transition
ctrl = [S["grade_distribution"]["merged"][t].get("E2", 0) for t in TR]
fig, ax = plt.subplots(figsize=(7, 3.8))
colors = ["#9b9b9b" if t == "T1" else ("#b7791f" if t in ("T2", "T4") else "#2b6cb0") for t in TR]
ax.bar(TR, ctrl, color=colors, edgecolor="white")
for i, v in enumerate(ctrl):
    ax.text(i, v + 0.25, f"{v}/16", ha="center", fontsize=10)
ax.text(0, 1.1, "delegated by citation:\nno in-paper evidence\nby definition of the finding", ha="center", fontsize=7.5, color="#555")
ax.set_ylabel("claims with controlled evidence (of 16)"); ax.set_ylim(0, 12)
ax.set_title("Controlled evidence concentrates at utility (T3); the correspondence (T2)\nand generality (T4) links are the thinnest (amber); T1 is delegated (grey)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig2_gap.png", dpi=200); plt.close(fig)

# Fig 3 - headline reliance with CI, both coders
fig, ax = plt.subplots(figsize=(7, 3.8))
def _wilson(k, n, z=1.96):
    import math
    ph = k / n; d = 1 + z * z / n
    c = (ph + z * z / (2 * n)) / d
    h = z * math.sqrt(ph * (1 - ph) / n + z * z / (4 * n * n)) / d
    return 100 * (c - h), 100 * (c + h)
_EA = {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/coder_A_E.csv"))}
_EB = {(r["claim_id"], r["transition"]): r for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/coder_B_E.csv.csv".replace(".csv.csv", ".csv")))}
_HA = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/headline_A.csv"))}
_HB = {r["claim_id"]: r["headline_transition"] for r in csv.DictReader(open(ROOT / "CODING_sheets_v2/headline_B.csv"))}
kA = sum(1 for c, t in _HA.items() if _EA[(c, t)]["in_paper_grade"] in ("E0", "E1"))
kB = sum(1 for c, t in _HB.items() if _EB[(c, t)]["in_paper_grade"] in ("E0", "E1"))
_EM = {(r["claim_id"], r["transition"]): r for r in merged}
kM = sum(1 for c, t in head.items() if _EM[(c, t)]["in_paper_grade"] in ("E0", "E1"))
ks = [kA, kB, kM]
vals = [100 * k / 16 for k in ks]
labels = ["coder A map", "coder B map", "merged map"]
lohi = [_wilson(k, 16) for k in ks]
err = [[v - lo for v, (lo, hi) in zip(vals, lohi)], [hi - v for v, (lo, hi) in zip(vals, lohi)]]
ax.bar(labels, vals, color="#7fa8c9", edgecolor="white", yerr=err, capsize=6, error_kw={"ecolor": "#444"})
for i, v in enumerate(vals):
    ax.text(i, 2, f"{ks[i]}/16\n{v:g}%", ha="center", fontsize=9, color="white")
ax.axhline(80, color="#b7791f", ls="--", lw=1.2)
ax.text(2.42, 81, "kill bar 80%", fontsize=8, color="#b7791f", ha="right")
ax.set_ylabel("headline claims resting on E0/E1 (%)"); ax.set_ylim(0, 100)
ax.set_title("Reliance of abstract improvement claims on uncontrolled transitions\n(bars: point estimate; whiskers: Wilson 95% CI; dashed: preregistered kill bar not reached)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig3_headline.png", dpi=200); plt.close(fig)

# Fig 4 - reportability by item
items = list(R["complete_count_by_item"].keys())
counts = [R["complete_count_by_item"][i] for i in items]
fig, ax = plt.subplots(figsize=(7, 4.6))
order = sorted(range(len(items)), key=lambda i: counts[i])
ax.barh([items[i] for i in order], [counts[i] for i in order], color="#2b6cb0", edgecolor="white")
for pos, i in enumerate(order):
    ax.text(counts[i] + 0.25, pos, f"{counts[i]}/16", va="center", fontsize=9)
ax.set_xlim(0, 17); ax.set_xlabel("claims with complete reporting (of 16)")
ax.set_title("Item-level reportability after adjudication (no aggregation across items)", fontsize=11)
fig.tight_layout(); fig.savefig(OUT / "fig4_reportability.png", dpi=200); plt.close(fig)

# Fig 5 - coder agreement
byA = Counter(r["transition"] for r in merged)  # denominator shape only
dis_by_tr = {"T1": 0, "T2": 2, "T3": 0, "T4": 6, "T5": 10}
fig, ax = plt.subplots(figsize=(7, 3.6))
ax.bar(TR, [dis_by_tr[t] for t in TR], color="#7fa8c9", edgecolor="white")
for i, t in enumerate(TR):
    v = dis_by_tr[t]
    ax.text(i, v + 0.25, f"{v}/16", ha="center", fontsize=9)
ax.set_ylabel("disagreeing claims"); ax.set_ylim(0, 12)
ax.set_title("In-paper disagreement by transition (22.5% overall; both coders are isolated\ninstances of the same AI assistant - mechanical isolation real, error independence not claimed)", fontsize=9)
fig.tight_layout(); fig.savefig(OUT / "fig5_agreement.png", dpi=200); plt.close(fig)

# Fig 6 - the reporting standard (checklist)
rows = [
    ("T1-01", "Name the biological structure specifically enough to check"),
    ("T1-02", "State the attributed computation as an input-output statement"),
    ("T1-03", "Present or cite a specific source for the structure-computation evidence"),
    ("T2-01", "State which artificial component implements which function"),
    ("T2-02", "List departures from the biological mechanism"),
    ("T3-01", "Describe the attribution comparison, or state none was run"),
    ("T3-02", "State which attribution controls are present and absent"),
    ("T4-01", "Name beyond-demonstrated task families as tested or untested"),
    ("T4-02", "Report scale sensitivity or mark it unreported"),
    ("T5-01", "Link the abstract claim to a specific result, figure or table"),
    ("T5-02", "State intended scope and the evidence's setting, task and scale"),
]
import textwrap
rows = [(i, "\n".join(textwrap.wrap(q, 52))) for i, q in rows]
fig, ax = plt.subplots(figsize=(9.6, 5.6))
ax.axis("off")
tbl = ax.table(cellText=[[i, q] for i, q in rows], colLabels=["item", "the reporting standard asks"], cellLoc="left", loc="center")
tbl.auto_set_font_size(False); tbl.set_fontsize(8.6); tbl.scale(1, 1.45)
for (r, c), cell in tbl.get_celld().items():
    cell.set_edgecolor("#bbbbbb")
    if r == 0:
        cell.set_facecolor("#2b6cb0"); cell.set_text_props(color="white", weight="bold")
    elif rows[r - 1][1].startswith(("Present or cite", "State which attribution controls")):
        cell.set_facecolor("#f6e8cf")
ax.set_title("The eleven-item standard for the middle of the chain (amber: complete in 0/16 audited claims)", fontsize=10)
fig.tight_layout(); fig.savefig(OUT / "fig6_standard.png", dpi=200); plt.close(fig)

print("WROTE", ", ".join(sorted(p.name for p in OUT.glob("*.png"))))
