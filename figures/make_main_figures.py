#!/usr/bin/env python3
"""Generate five provisional, source-linked NeuroConverge figures."""
from pathlib import Path
import csv
import hashlib
import json
import sys
import textwrap

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
from matplotlib.patches import FancyBboxPatch, Rectangle
import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]
FIG = Path(__file__).resolve().parent
M2 = ROOT / "new_experiments/M2_REALIZED_STATE_VS_ACTION_BELIEF_V1/runs/canonical_1"
M5 = ROOT / "new_experiments/M5_CORRESPONDENCE_PRESERVED_TIMING_V1/results"
OUTS = [
    FIG / "Fig1_framework", FIG / "Fig2_structure_boundary",
    FIG / "Fig3_motor_feedback", FIG / "Fig4_temporal_credit",
    FIG / "Fig5_evidence_map",
]
for path in OUTS:
    path.mkdir(parents=True, exist_ok=True)

sys.path.insert(0, str(Path.home() / ".codex/skills/nature-figure/scripts"))
from audit_panel_alignment import require_matplotlib_panel_alignment  # noqa: E402

plt.rcParams.update({
    "font.family": "sans-serif",
    "font.sans-serif": ["Arial", "Helvetica", "DejaVu Sans", "sans-serif"],
    "font.size": 8.0, "axes.titlesize": 9.0, "axes.labelsize": 8.0,
    "xtick.labelsize": 7.0, "ytick.labelsize": 7.0, "legend.fontsize": 7.0,
    "pdf.fonttype": 42, "ps.fonttype": 42, "svg.fonttype": "none",
    "axes.spines.top": False, "axes.spines.right": False,
    "axes.linewidth": 0.8, "savefig.facecolor": "white",
})
BLUE = "#2864A5"
TEAL = "#138A8A"
ORANGE = "#D47A18"
RED = "#B64C4C"
GRAY = "#68737D"
PALE = "#F2F5F7"
DARK = "#202A33"


def panel_label(ax, label):
    ax.text(-0.12, 1.08, label, transform=ax.transAxes, fontsize=8,
            fontweight="bold", ha="left", va="bottom", clip_on=False)


def save(fig, out, basename, axes, panel_ids):
    """Audit the final plot-area geometry, then export vector and review files."""
    fig.canvas.draw()
    require_matplotlib_panel_alignment(
        fig, axes=axes, panel_ids=panel_ids,
        json_out=out / f"{basename}.alignment.json",
        overlay_svg=out / f"{basename}.alignment.svg",
        tolerance_pt=1.5, gutter_tolerance_pt=1.5,
        require_panel_labels=len(axes) > 1, strict=True,
    )
    fig.savefig(out / f"{basename}.pdf")
    fig.savefig(out / f"{basename}.svg")
    fig.savefig(out / f"{basename}.png", dpi=300)
    plt.close(fig)


def write_csv(out, name, header, rows):
    with open(out / name, "w", newline="", encoding="utf-8") as handle:
        writer = csv.writer(handle)
        writer.writerow(header)
        writer.writerows(rows)


# Figure 1: evidence map. Separators are not causal arrows.
fig, ax = plt.subplots(figsize=(7.2, 3.55))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
ax.text(0.03, 0.95, "Two evidence portfolios ask four distinct questions",
        fontsize=12, fontweight="bold", color=DARK, va="top")
boxes = [
    (0.03, "BIOLOGICAL\nSTRUCTURE", "Connectome topology\nM0; Fish1.5"),
    (0.275, "SOURCE-SUPPORTED\nCOMPUTATION", "Published/source evidence\nWorm; modeled CF data"),
    (0.52, "INFORMATION\nCORRESPONDENCE", "What reaches the model?\nM2/M5 synthetic tests"),
    (0.765, "ARTIFICIAL\nUTILITY", "Task performance vs\ngeneric/reference models"),
]
for x, title, body in boxes:
    ax.add_patch(FancyBboxPatch(
        (x, 0.44), 0.205, 0.31, boxstyle="round,pad=.010,rounding_size=.016",
        fc=PALE, ec="#B7C2CB", lw=0.9))
    ax.text(x + 0.1025, 0.655, title, ha="center", va="center",
            fontweight="bold", color=BLUE, fontsize=7.6)
    ax.text(x + 0.1025, 0.525, body, ha="center", va="center",
            color=DARK, fontsize=7.1, linespacing=1.25)
for x in (0.252, 0.497, 0.742):
    ax.plot([x, x], [0.48, 0.70], color="#BAC3CA", lw=0.8, ls=(0, (2, 2)))
    ax.text(x, 0.39, "separate test", ha="center", va="center",
            fontsize=6.3, color=GRAY)
ax.text(0.03, 0.245, "NeuroMotif", fontweight="bold", color=TEAL, fontsize=8.5)
ax.plot([0.15, 0.43], [0.25, 0.25], color=TEAL, lw=3, solid_capstyle="round")
ax.text(0.03, 0.145, "NeuroMech", fontweight="bold", color=ORANGE, fontsize=8.5)
ax.plot([0.15, 0.73], [0.15, 0.15], color=ORANGE, lw=3, solid_capstyle="round")
ax.text(0.76, 0.20, "Retrospective evidence map\n(proposed requirements, not a law)",
        fontsize=7.3, color=RED, fontweight="bold", va="center")
write_csv(OUTS[0], "figure_source_data.csv",
          ["element", "label", "evidence_note"], [
    ["question", "Biological structure", "M0 bounded assay; Fish1.5 single specimen"],
    ["question", "Source-supported computation", "Published worm finding; modeled source data"],
    ["question", "Information correspondence", "Separate outcome-informed synthetic M2 and M5 tests"],
    ["question", "Artificial utility", "Task-specific results versus generic/reference controls"],
    ["separator", "Separate test", "Ordering organizes evidence questions; it is not causal inference"],
    ["portfolio", "NeuroMotif", "Structure/dynamics line"],
    ["portfolio", "NeuroMech", "Mechanism/transfer line"],
])
fig.subplots_adjust(left=0.02, right=0.985, bottom=0.06, top=0.98)
save(fig, OUTS[0], "Fig1_framework", [ax], ["a"])


# Figure 2: bounded topology/Fish1.5 result.
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.15),
                        gridspec_kw={"width_ratios": [1.08, 1]})
lo, est, hi = -0.2932283, -0.10961965, 0.1338241
ax = axs[0]
ax.axvline(0, color=GRAY, lw=1, ls="--")
ax.errorbar(est, 0, xerr=[[est - lo], [hi - est]], fmt="o",
            color=BLUE, ecolor=BLUE, capsize=4, lw=2, ms=6)
ax.set(xlim=(-0.42, 0.28), ylim=(-0.55, 0.55), yticks=[])
ax.set_xlabel("Spearman correlation (95% neuron-bootstrap CI)")
ax.set_title("Fish1.5 E1: one specimen, 82 neurons", loc="left", fontweight="bold")
ax.text(0.02, 0.09, "ρ = −0.110\npositive-direction permutation p = 0.834",
        transform=ax.transAxes, fontsize=7.5, color=DARK, va="bottom")
panel_label(ax, "a")
ax = axs[1]
ax.barh([0], [139], left=[0], color=TEAL, height=0.42)
ax.barh([0], [861], left=[139], color="#D7DEE3", height=0.42)
ax.set(xlim=(0, 1000), ylim=(-0.55, 0.55), yticks=[])
ax.set_xlabel("Frozen topology-null graphs (n = 1,000)")
ax.set_title("Frozen null was not estimable", loc="left", fontweight="bold")
ax.text(142, 0.30, "139 defined", ha="left", va="center",
        color=TEAL, fontweight="bold", fontsize=7.0)
ax.text(569.5, 0, "861 undefined", ha="center", va="center",
        color=DARK, fontweight="bold", fontsize=7.3)
panel_label(ax, "b")
fig.suptitle("Structure-to-dynamics evidence is bounded to the tested records",
             x=0.03, ha="left", y=0.97, fontsize=11, fontweight="bold")
fig.text(
    0.03, 0.055,
    "M0 tested whole-connectome off-diagonal recurrence against passive identity-like persistence, which retains diagonal state memory.\n"
    "The result bounds that frozen assay; the single-specimen topology null is indeterminate because 861/1,000 graphs were undefined.",
    fontsize=6.8, color=GRAY, va="bottom")
fig.subplots_adjust(left=0.08, right=0.975, bottom=0.29, top=0.78, wspace=0.28)
write_csv(OUTS[1], "figure_source_data.csv",
          ["record", "estimate", "ci_low", "ci_high", "unit_or_status", "source"], [
    ["Fish1.5 E1 recurrence-persistence", est, lo, hi, "one specimen; 82 neurons",
     "NeuroMotif 1adc07f; paper-level audit summary"],
    ["Fish1.5 frozen topology null defined", 139, "", "", "graphs",
     "NeuroMotif 1adc07f; summary record"],
    ["Fish1.5 frozen topology null undefined", 861, "", "", "graphs",
     "NeuroMotif 1adc07f; summary record"],
    ["M0 whole-connectome assay", "not numeric", "", "",
     "off-diagonal recurrence versus passive identity-like persistence retaining diagonal state memory",
     "local Route-D report; see source snapshot"],
])
save(fig, OUTS[1], "Fig2_structure_boundary", list(axs), ["a", "b"])


# Figure 3: causal M2 workflow plus paired primary/diagnostic contrasts.
m2_result = json.loads((M2 / "summary.json").read_text(encoding="utf-8"))
primary = m2_result["primary_summary"]
revealed = m2_result["revealed_gap_summary"]
no_reversal = m2_result["no_reversal_gap_summary"]
contrasts = [
    ["Hidden reversals", primary["mean"], primary["ci95_low"], primary["ci95_high"], 32],
    ["Reversal revealed", revealed["mean"], revealed["ci95_low"], revealed["ci95_high"], 32],
    ["No reversals", no_reversal["mean"], no_reversal["ci95_low"], no_reversal["ci95_high"], 32],
]
write_csv(OUTS[2], "figure_source_data.csv",
          ["contrast", "mean_mse_difference", "ci_low", "ci_high", "paired_seed_blocks", "positive_favors"],
          [row + ["first named arm"] for row in contrasts])
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.55), gridspec_kw={"width_ratios": [1.12, 1]})
ax = axs[0]
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
ax.set_title("Causal task and controller inputs", loc="left", fontweight="bold", pad=8)
boxes = [
    (0.04, 0.56, 0.40, 0.28, "Current inputs\nrelative position + validity\nprevious command\nprior sign: realized-state only"),
    (0.56, 0.56, 0.40, 0.28, "AcRKN state update + policy\nproduces command"),
    (0.56, 0.14, 0.40, 0.26, "Stochastic actuator\n+ tracking plant"),
]
for x, y, w, h, label in boxes:
    ax.add_patch(FancyBboxPatch((x, y), w, h, boxstyle="round,pad=.012,rounding_size=.018",
                                fc=PALE, ec="#AEBBC4", lw=0.9))
    ax.text(x+w/2, y+h/2, label, ha="center", va="center", fontsize=5.8, color=DARK)
for a, b in [((.44,.70),(.56,.70)), ((.76,.56),(.76,.40))]:
    ax.annotate("", xy=b, xytext=a, arrowprops={"arrowstyle":"->", "lw":1, "color":GRAY})
ax.annotate("prior executed-displacement sign", xy=(.15,.56), xytext=(.45,.48),
            ha="center", va="center", fontsize=5.6, color=TEAL,
            arrowprops={"arrowstyle":"->", "connectionstyle":"arc3,rad=-.32", "lw":1.1, "color":TEAL})
panel_label(ax, "a")
ax = axs[1]
y = np.arange(len(contrasts))[::-1]
for yi, row in zip(y, contrasts):
    color = BLUE if yi == y[0] else GRAY
    ax.errorbar(row[1], yi, xerr=[[row[1]-row[2]], [row[3]-row[1]]], fmt="o",
                color=color, ecolor=color, capsize=3, lw=1.5, ms=5)
ax.axvline(0, color=RED, ls="--", lw=1)
ax.set_yticks(y, [row[0] for row in contrasts])
ax.set_xlabel("Paired MSE difference\n(positive favors first-named arm)")
ax.set_title("AcRKN contrasts", loc="left", fontweight="bold")
ax.grid(axis="x", color="#E7EBEE", lw=.6)
panel_label(ax, "b")
fig.suptitle("M2: exact execution feedback did not improve the tested controller",
             x=.03, ha="left", y=.98, fontsize=10.5, fontweight="bold")
fig.text(.03, .045,
         "32 paired training-seed blocks; error bars are paired block-bootstrap 95% CIs. The primary hidden-reversal contrast favored action-only.\n"
         "Synthetic post-actuator sign is not the worm premotor RIM→AIY signal; outcome-informed test, not biological-transfer validation.",
         fontsize=6.5, color=GRAY, va="bottom")
fig.subplots_adjust(left=.18, right=.98, bottom=.27, top=.79, wspace=.18)
save(fig, OUTS[2], "Fig3_motor_feedback", list(axs), ["a", "b"])


# Figure 4: M5 paired correspondence effects and absolute means.
m5_metrics = pd.read_csv(M5 / "per_seed_metrics.csv")
m5_effects = pd.read_csv(M5 / "per_seed_correspondence_effects.csv")
order = ["CF_TIMED_LOCAL", "NO_TRACE", "CF_TIME_SHUFFLE",
         "GENERIC_MATCHED_RBF", "EXACT_REPLAY_REFERENCE"]
display = ["CF-timed local", "No trace", "CF-time shuffle",
           "Generic ridge (same features)", "Exact replay (full input)"]
m5_result = json.loads((M5 / "primary_result.json").read_text(encoding="utf-8"))
rows = []
for arm, label in zip(order, display):
    subset = m5_metrics[m5_metrics.arm == arm]
    aligned = subset[subset.regime == "ALIGNED"].nmae.to_numpy()
    broken = subset[subset.regime == "BROKEN"].nmae.to_numpy()
    effect = m5_effects[m5_effects.arm == arm].broken_minus_aligned_nmae.to_numpy()
    ci = m5_result["effects"][arm]["bootstrap_95_ci"]
    rows.append([arm, label, len(effect), aligned.mean(), broken.mean(),
                 effect.mean(), ci[0], ci[1],
                 "nMAE(BROKEN) − nMAE(ALIGNED); positive favors preserved correspondence"])
write_csv(OUTS[3], "figure_source_data.csv",
          ["arm", "display_label", "task_seeds", "aligned_mean_nmae",
           "broken_mean_nmae", "effect_broken_minus_aligned", "ci_low",
           "ci_high", "estimand"], rows)
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.55),
                        gridspec_kw={"width_ratios": [1.12, 1]})
ax = axs[0]
for index, row in enumerate(rows[::-1]):
    color = TEAL if row[0] == "CF_TIMED_LOCAL" else GRAY
    ax.errorbar(row[5], index, xerr=[[row[5] - row[6]], [row[7] - row[5]]],
                fmt="o", color=color, capsize=3, lw=1.6, ms=5)
ax.axvline(0, color=RED, ls="--", lw=1)
ax.set_yticks(range(len(display)), display[::-1])
ax.set_xlabel("nMAE broken − aligned")
ax.set_title("Paired correspondence effect", loc="left", fontweight="bold")
ax.grid(axis="x", color="#E7EBEE", lw=0.6)
panel_label(ax, "a")
ax = axs[1]
y = np.arange(len(rows))[::-1]
for yi, row in zip(y, rows):
    ax.plot([row[3], row[4]], [yi, yi], color="#ADB7BE", lw=1)
    ax.scatter(row[3], yi, color=BLUE, s=24,
               label="Aligned" if yi == y[0] else None, zorder=3)
    ax.scatter(row[4], yi, color=ORANGE, s=24,
               label="Broken" if yi == y[0] else None, zorder=3)
ax.set_yticks(y)
ax.tick_params(axis="y", labelleft=False)
ax.set_xlabel("Mean normalized MAE")
ax.set_title("Regime means (lower is better)", loc="left", fontweight="bold")
ax.grid(axis="x", color="#E7EBEE", lw=0.6)
ax.legend(frameon=False, loc="lower right")
panel_label(ax, "b")
fig.suptitle("M5: correspondence helped the local rule; generic references gained more",
             x=0.03, ha="left", y=0.97, fontsize=11, fontweight="bold")
fig.text(
    0.03, 0.055,
    "30 paired task seeds; paired-seed bootstrap 95% CIs. Outcome-informed synthetic test.\n"
    "Ridge shares 16 features but has a different, smaller head and objective; replay receives all 40 bins.",
    fontsize=6.8, color=GRAY, va="bottom")
fig.subplots_adjust(left=0.275, right=0.98, bottom=0.27, top=0.78, wspace=0.15)
save(fig, OUTS[3], "Fig4_temporal_credit", list(axs), ["a", "b"])


# Figure 5: record-level evidence map with explicit inference ceilings.
fig, ax = plt.subplots(figsize=(7.2, 4.65))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
headers = ["Evidence question", "Record-level status", "Inference ceiling"]
rows = [
    ["Connectome structure → task computation",
     "Bounded M0 result; Fish1.5 directional association not supported; topology null indeterminate",
     "Frozen assay / one specimen"],
    ["Biological computation in source system",
     "Published worm evidence; animal-level project reanalysis blocked by schema",
     "Published cell-class scope"],
    ["Cross-system substrate resolution",
     "R20-01 supports projection-level evidence only", "Mechanism unresolved"],
    ["Direct realized-state input → artificial utility",
     "M2: no AcRKN advantage; generic references had lower MSE",
     "One synthetic plant/task"],
    ["Preserved temporal information → artificial utility",
     "M5: local-rule correspondence effect; generic ridge and replay effects were larger",
     "One synthetic generator/task"],
    ["General transfer requirement or law", "Not established by either portfolio",
     "Retrospective evidence proposal"],
]
column_lefts = [0.025, 0.36, 0.72]
wrap_widths = [34, 45, 28]
for left, header in zip(column_lefts, headers):
    ax.text(left, 0.89, header, fontweight="bold", fontsize=8.2,
            color=BLUE, va="center")
for index, (center, row) in enumerate(zip(np.linspace(0.79, 0.21, len(rows)), rows)):
    ax.add_patch(Rectangle((0.015, center - 0.051), 0.97, 0.102,
                           transform=ax.transAxes,
                           facecolor="#F4F7F8" if index % 2 == 0 else "white",
                           edgecolor="none", zorder=-1))
    for left, width, value in zip(column_lefts, wrap_widths, row):
        wrapped = textwrap.fill(value, width=width, break_long_words=False)
        ax.text(left, center, wrapped, fontsize=7.0, color=DARK,
                va="center", ha="left", linespacing=1.15)
ax.text(
    0.025, 0.075,
    "M2 and M5 have different endpoints and independent units; no cross-task effect is calculated.\n"
    "The ordering is an editorial evidence map, not a validated hierarchy, scale or causal chain.",
    fontsize=7.0, color=RED, fontweight="bold", va="center")
fig.suptitle("Evidence map: what is supported, blocked or unresolved",
             x=0.03, ha="left", y=0.975, fontsize=11, fontweight="bold")
fig.subplots_adjust(left=0.015, right=0.985, bottom=0.03, top=0.95)
write_csv(OUTS[4], "figure_source_data.csv", headers, rows)
save(fig, OUTS[4], "Fig5_evidence_map", [ax], ["a"])


# Reproducibility manifest. Layout assessment is not submission clearance.
basenames = ["Fig1_framework", "Fig2_structure_boundary", "Fig3_motor_feedback",
             "Fig4_temporal_credit", "Fig5_evidence_map"]
manifest = {
    "generator": Path(__file__).name,
    "generator_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    "source_inputs": {
        str(path.relative_to(ROOT)): hashlib.sha256(path.read_bytes()).hexdigest()
        for path in [
            M2 / "summary.json",
            M5 / "primary_result.json",
            M5 / "per_seed_metrics.csv",
            M5 / "per_seed_correspondence_effects.csv",
        ]
    },
    "matplotlib": matplotlib.__version__,
    "figures": [],
    "status": "PROVISIONAL_LAYOUT_ASSESSED",
    "limitations": [
        "Source ownership and reuse rights remain pending.",
        "Final source-revision audit remains pending.",
        "Layout assessment does not establish submission readiness.",
    ],
}
for figure_number, (out, basename) in enumerate(zip(OUTS, basenames), 1):
    entry = {
        "figure": figure_number, "directory": str(out.relative_to(ROOT)),
        "pdf": f"{basename}.pdf", "svg": f"{basename}.svg",
        "png": f"{basename}.png", "source_data": "figure_source_data.csv",
        "alignment": f"{basename}.alignment.json", "files": {},
    }
    for filename in [entry["pdf"], entry["svg"], entry["png"],
                     entry["source_data"], entry["alignment"]]:
        payload = (out / filename).read_bytes()
        entry["files"][filename] = {
            "sha256": hashlib.sha256(payload).hexdigest(),
            "bytes": len(payload),
        }
    manifest["figures"].append(entry)
(FIG / "FIGURE_EXPORT_MANIFEST.json").write_text(
    json.dumps(manifest, indent=2) + "\n", encoding="utf-8")
print(json.dumps({"status": "generated", "figures": len(manifest["figures"]),
                  "manifest": str(FIG / "FIGURE_EXPORT_MANIFEST.json")}, indent=2))
