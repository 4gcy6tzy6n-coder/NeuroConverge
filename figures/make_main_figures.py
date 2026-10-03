#!/usr/bin/env python3
"""Generate six source-linked NeuroConverge figures for internal review."""
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
PROSPECTIVE = ROOT / "new_experiments/PROSPECTIVE_V1/results"
FISH15 = ROOT / "evidence/FISH15_PRIMARY_RESULT.json"
OUTS = [
    FIG / "Fig1_motivation", FIG / "Fig2_framework",
    FIG / "Fig3_structure_boundary", FIG / "Fig4_motor_feedback",
    FIG / "Fig5_temporal_credit", FIG / "Fig6_evidence_map",
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


# Figure 1: motivation. Source evidence does not uniquely specify a useful model.
fig, ax = plt.subplots(figsize=(7.2, 3.45))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
ax.text(.03, .96, "Biological evidence leaves key implementation choices open",
        fontsize=11.5, fontweight="bold", color=DARK, va="top")
columns = [
    (.035, .205, BLUE, "SOURCE EVIDENCE", "Anatomy · activity\nperturbation · behaviour"),
    (.285, .205, TEAL, "COMPUTATION", "Which operation is\nsupported in the source?"),
    (.535, .205, ORANGE, "TRANSLATION", "Signal · representation\nobjective · learning rule"),
    (.785, .18, RED, "AI UTILITY", "Benefit under task\nand comparator controls"),
]
for x, w, color, title, body in columns:
    ax.add_patch(FancyBboxPatch((x, .50), w, .28,
                                boxstyle="round,pad=.012,rounding_size=.016",
                                fc=PALE, ec=color, lw=1.2))
    ax.text(x+w/2, .69, title, ha="center", va="center", fontsize=7.8,
            color=color, fontweight="bold")
    ax.text(x+w/2, .585, body, ha="center", va="center", fontsize=7.1,
            color=DARK, linespacing=1.25)
for x in (.255, .505, .755):
    ax.annotate("", xy=(x+.025, .64), xytext=(x-.015, .64),
                arrowprops={"arrowstyle":"->", "lw":1, "color":GRAY})
ax.text(.50, .37, "Each transition needs its own evidence and comparator",
        ha="center", va="center", fontsize=8.0, color=BLUE, fontweight="bold")
ax.text(.50, .24,
        "A biological label alone does not fix the model input, objective,\n"
        "training procedure or the alternative that defines an advantage.",
        ha="center", va="center", fontsize=8.0, color=DARK, linespacing=1.3)
ax.text(.50, .08,
        "Motivating distinction; not a causal model or a result established by these portfolios.",
        ha="center", va="center", fontsize=6.8, color=GRAY)
fig.subplots_adjust(left=.015, right=.985, bottom=.03, top=.97)
write_csv(OUTS[0], "figure_source_data.csv",
          ["stage", "elements", "interpretation"], [
    ["Source evidence", "Anatomy, activity, perturbation, behaviour",
     "Evidence types do not uniquely specify an artificial implementation"],
    ["Computation", "Source-supported operation", "Requires computational interpretation"],
    ["Translation", "Signal, representation, objective, learning rule",
     "Implementation choices must be stated and tested"],
    ["AI utility", "Task performance under comparator controls",
     "Utility is task- and comparator-dependent"],
])
save(fig, OUTS[0], "Fig1_motivation", [ax], ["a"])


# Figure 2: evidence map. Separators are not causal arrows.
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
ax.plot([0.15, 0.97], [0.15, 0.15], color=ORANGE, lw=3, solid_capstyle="round")
ax.text(0.03, 0.045, "Retrospective organizing questions; not a validated transfer law",
        fontsize=7.0, color=RED, fontweight="bold", va="center")
write_csv(OUTS[1], "figure_source_data.csv",
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
save(fig, OUTS[1], "Fig2_framework", [ax], ["a"])


# Figure 3: source-linked Fish1.5 result. M0 is described in the main text/SI,
# but omitted from this quantitative figure because canonical round-level data
# are not part of the frozen integration snapshot.
fish15 = json.loads(FISH15.read_text(encoding="utf-8"))
fig, axs = plt.subplots(1, 2, figsize=(7.2, 3.15),
                        gridspec_kw={"width_ratios": [1.08, 1]})
lo = fish15["bootstrap_ci95_low"]
est = fish15["primary_spearman_rho"]
hi = fish15["bootstrap_ci95_high"]
ax = axs[0]
ax.axvline(0, color=GRAY, lw=1, ls="--")
ax.errorbar(est, 0, xerr=[[est - lo], [hi - est]], fmt="o",
            color=BLUE, ecolor=BLUE, capsize=4, lw=2, ms=6)
ax.set(xlim=(-0.42, 0.28), ylim=(-0.55, 0.55), yticks=[])
ax.set_xlabel("Spearman correlation (95% neuron-bootstrap CI)")
ax.set_title("Fish1.5 E1: one specimen, 82 neurons", loc="left", fontweight="bold")
ax.text(0.02, 0.08, f"ρ = {est:.3f}\nP = {fish15['positive_permutation_p']:.3f}",
        transform=ax.transAxes, fontsize=7.2, color=DARK, va="bottom",
        bbox={"facecolor": "white", "edgecolor": "none", "pad": 1.2})
panel_label(ax, "a")
ax = axs[1]
defined = fish15["topology_null_defined_rho_n"]
undefined = fish15["topology_null_undefined_rho_n"]
null_total = fish15["topology_null_n"]
ax.barh([0], [defined], left=[0], color=TEAL, height=0.42)
ax.barh([0], [undefined], left=[defined], color="#D7DEE3", height=0.42)
ax.set(xlim=(0, null_total), ylim=(-0.55, 0.55), yticks=[])
ax.set_xlabel(f"Frozen topology-null graphs (n = {null_total:,})")
ax.set_title("Frozen null was not estimable", loc="left", fontweight="bold")
ax.text(defined + 3, 0.30, f"{defined} defined", ha="left", va="center",
        color=TEAL, fontweight="bold", fontsize=7.0)
ax.text(defined + undefined / 2, 0, f"{undefined} undefined", ha="center", va="center",
        color=DARK, fontweight="bold", fontsize=7.3)
panel_label(ax, "b")
fig.suptitle("Fish1.5 structure-to-dynamics evidence is indeterminate",
             x=0.03, ha="left", y=0.97, fontsize=11, fontweight="bold")
fig.text(
    0.03, 0.055,
    "One specimen; neuron-level resampling does not estimate between-animal uncertainty.\n"
    "The frozen topology-null P value was not estimable because most null correlations were undefined.",
    fontsize=6.8, color=GRAY, va="bottom")
fig.subplots_adjust(left=0.08, right=0.975, bottom=0.29, top=0.78, wspace=0.28)
write_csv(OUTS[2], "figure_source_data.csv",
          ["record", "estimate", "ci_low", "ci_high", "permutation_p", "unit_or_status", "source"], [
    ["Fish1.5 E1 recurrence-persistence", est, lo, hi, fish15["positive_permutation_p"],
     f"one specimen; {fish15['n_primary_cohort']} neurons", "evidence/FISH15_PRIMARY_RESULT.json"],
    ["Fish1.5 frozen topology null defined", defined, "", "", "", "graphs",
     "evidence/FISH15_PRIMARY_RESULT.json"],
    ["Fish1.5 frozen topology null undefined", undefined, "", "", "", "graphs",
     "evidence/FISH15_PRIMARY_RESULT.json"],
])
save(fig, OUTS[2], "Fig3_structure_boundary", list(axs), ["a", "b"])


# Figure 3: causal M2 workflow plus paired primary/diagnostic contrasts.
m2_result = json.loads((M2 / "summary.json").read_text(encoding="utf-8"))
primary = m2_result["primary_summary"]
revealed = m2_result["revealed_gap_summary"]
no_reversal = m2_result["no_reversal_gap_summary"]
contrasts = [
    ["Action-only − state | hidden", primary["mean"], primary["ci95_low"], primary["ci95_high"], 32],
    ["Event-revealed − state", revealed["mean"], revealed["ci95_low"], revealed["ci95_high"], 32],
    ["Action-only − state | no reversal", no_reversal["mean"], no_reversal["ci95_low"], no_reversal["ci95_high"], 32],
]
write_csv(OUTS[3], "figure_source_data.csv",
          ["contrast", "mean_mse_difference", "ci_low", "ci_high", "paired_seed_blocks", "positive_favors"],
          [row + ["second named arm (lower MSE)"] for row in contrasts])
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
ax.set_xlabel("Paired MSE difference\n(positive favors second-named arm)")
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
save(fig, OUTS[3], "Fig4_motor_feedback", list(axs), ["a", "b"])


# Figure 5: M5 algorithm, paired correspondence effects and absolute means.
m5_metrics = pd.read_csv(M5 / "per_seed_metrics.csv")
m5_effects = pd.read_csv(M5 / "per_seed_correspondence_effects.csv")
order = ["CF_TIMED_LOCAL", "NO_TRACE", "CF_TIME_SHUFFLE",
         "GENERIC_MATCHED_RBF", "EXACT_REPLAY_REFERENCE"]
display = ["CF-timed local", "No trace", "CF-time shuffle",
           "Generic ridge (same features)", "Full-input replay"]
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
write_csv(OUTS[4], "figure_source_data.csv",
          ["arm", "display_label", "task_seeds", "aligned_mean_nmae",
           "broken_mean_nmae", "effect_broken_minus_aligned", "ci_low",
           "ci_high", "estimand"], rows)
fig = plt.figure(figsize=(7.2, 4.65))
grid = fig.add_gridspec(2, 2, height_ratios=[.82, 1.5],
                        left=.275, right=.98, bottom=.24, top=.80,
                        hspace=.56, wspace=.15)
algorithm = fig.add_subplot(grid[0, :])
algorithm.set(xlim=(0, 1), ylim=(0, 1))
algorithm.axis("off")
algorithm.set_title("Fixed local-rule pipeline and correspondence manipulation",
                    loc="left", fontweight="bold", pad=2)
algo_boxes = [
    (.015, .25, .22, .52, "40-bin temporal pulse\n+ target interval"),
    (.275, .25, .22, .52, "16 RBF eligibility\nfeatures from full trial"),
    (.535, .25, .20, .52, "One-pass local update\n28-class softmax"),
    (.775, .25, .21, .52, "Predicted interval\nheld-out nMAE"),
]
for x, y0, w, h, label in algo_boxes:
    algorithm.add_patch(FancyBboxPatch((x, y0), w, h,
        boxstyle="round,pad=.012,rounding_size=.018", fc=PALE,
        ec="#AEBBC4", lw=.9))
    algorithm.text(x+w/2, y0+h/2, label, ha="center", va="center",
                   fontsize=6.7, color=DARK, linespacing=1.2)
for x in (.24, .50, .74):
    algorithm.annotate("", xy=(x+.03, .51), xytext=(x-.005, .51),
                       arrowprops={"arrowstyle":"->", "lw":.9, "color":GRAY})
algorithm.text(.50, .10,
    "Aligned: input–target pairs retained  |  Broken: targets independently permuted in train and test",
    ha="center", va="center", fontsize=6.2, color=ORANGE, fontweight="bold")
panel_label(algorithm, "a")
axs = [fig.add_subplot(grid[1, 0]), fig.add_subplot(grid[1, 1])]
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
panel_label(ax, "b")
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
panel_label(ax, "c")
fig.suptitle("M5: preserved correspondence helped prediction, not mechanism specificity",
             x=0.03, ha="left", y=0.97, fontsize=10.5, fontweight="bold")
fig.text(
    0.03, 0.045,
    "30 paired task seeds; paired-seed bootstrap 95% CIs. Outcome-informed test; full-trial features are offline.\n"
    "Ridge shares 16 features but has a different, smaller head and objective; replay receives all 40 bins.",
    fontsize=6.8, color=GRAY, va="bottom")
write_csv(OUTS[4], "algorithm_panel_source_data.csv",
          ["stage", "definition"], [
    ["Input", "40-bin noisy temporal pulse and interval target"],
    ["Representation", "16 Gaussian RBF features computed from the complete trial array"],
    ["Update", "One-pass eligibility-gated softmax update; artificial, not biological LTD"],
    ["Aligned regime", "Each input remains paired with its generating target"],
    ["Broken regime", "Targets independently permuted within training and test splits"],
    ["Endpoint", "Held-out normalized mean absolute error"],
])
save(fig, OUTS[4], "Fig5_temporal_credit", axs, ["b", "c"])


# Figure 6: record-level evidence map with explicit inference ceilings.
fig, ax = plt.subplots(figsize=(7.2, 5.10))
ax.set(xlim=(0, 1), ylim=(0, 1))
ax.axis("off")
headers = ["Evidence question", "Record-level status", "Inference ceiling"]
rows = [
    ["Connectome structure → task computation",
     "M0 bounded (round linkage pending); Fish1.5 association unsupported; null indeterminate",
     "Frozen assay / one specimen"],
    ["Biological computation in source system",
     "Published worm evidence; project reanalysis schema-blocked",
     "Published cell-class scope"],
    ["Execution feedback → artificial utility",
     "M2: realized-state input worse than action-only; GRU/PF lower MSE",
     "One synthetic plant"],
    ["Temporal correspondence → artificial utility",
     "M5: local-rule effect; generic ridge and replay effects larger",
     "One synthetic generator"],
    ["Fast–slow dynamics × correspondence",
     "DMP: no family passed specificity; contextual small-data signal only",
     "Three synthetic families; post-result"],
    ["Feature-matched inhibition × correspondence",
     "V1: interaction opposite prediction; aligned selective pool worse",
     "One synthetic visual task; sign error"],
    ["General transfer law", "Not established by portfolios or V1 test",
     "Retrospective synthesis + one synthetic test"],
]
column_lefts = [0.025, 0.35, 0.74]
wrap_widths = [27, 37, 21]
for left, header in zip(column_lefts, headers):
    ax.text(left, 0.89, header, fontweight="bold", fontsize=8.2,
            color=BLUE, va="center")
for index, (center, row) in enumerate(zip(np.linspace(0.805, 0.205, len(rows)), rows)):
    ax.add_patch(Rectangle((0.015, center - 0.041), 0.97, 0.082,
                           transform=ax.transAxes,
                           facecolor="#F4F7F8" if index % 2 == 0 else "white",
                           edgecolor="none", zorder=-1))
    for left, width, value in zip(column_lefts, wrap_widths, row):
        wrapped = textwrap.fill(value, width=width, break_long_words=False)
        ax.text(left, center, wrapped, fontsize=7.0, color=DARK,
                va="center", ha="left", linespacing=1.15)
ax.text(
    0.025, 0.075,
    "Endpoints and units differ; no cross-task effect is calculated. V1 was selected after earlier results, overlaps the prior visual domain,\n"
    "and its frozen AP contrast had a sign-direction wording error. This evidence map is retrospective, not a validated causal hierarchy.",
    fontsize=6.8, color=RED, fontweight="bold", va="center")
fig.suptitle("Evidence map: what is supported, blocked or unresolved",
             x=0.03, ha="left", y=0.975, fontsize=11, fontweight="bold")
fig.subplots_adjust(left=0.015, right=0.985, bottom=0.03, top=0.95)
write_csv(OUTS[5], "figure_source_data.csv", headers, rows)
save(fig, OUTS[5], "Fig6_evidence_map", [ax], ["a"])


# Reproducibility manifest. Layout assessment is not submission clearance.
basenames = ["Fig1_motivation", "Fig2_framework", "Fig3_structure_boundary",
             "Fig4_motor_feedback", "Fig5_temporal_credit", "Fig6_evidence_map"]
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
            FISH15,
            ROOT / "new_experiments/DMP_FAST_SLOW_CORRESPONDENCE_2X2_V1/results/SUMMARY.json",
            ROOT / "new_experiments/DMP_FAST_SLOW_CORRESPONDENCE_2X2_V1/results/VERIFICATION.json",
            PROSPECTIVE / "VERIFIED_SUMMARY.json",
            PROSPECTIVE / "TASK_INSTANCE_MEANS.csv",
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
        "additional_source_data": (["algorithm_panel_source_data.csv"]
                                   if figure_number == 5 else []),
        "alignment": f"{basename}.alignment.json", "files": {},
    }
    for filename in ([entry["pdf"], entry["svg"], entry["png"],
                      entry["source_data"], entry["alignment"]]
                     + entry["additional_source_data"]):
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
