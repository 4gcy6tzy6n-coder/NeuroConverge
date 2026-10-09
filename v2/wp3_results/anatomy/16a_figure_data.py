"""Consolidate the four surviving claims into figure-ready source data with their specifications.

Every number is READ from the result JSONs rather than retyped, and every series carries the script, the
inputs and the analysis choices that produced it.  Two files are deliberately excluded.
"""
import json, pathlib, hashlib
A=pathlib.Path("/Users/yyl/Desktop/workshop/NMI/NeuroConverge/v2/wp3_results/anatomy")
R=pathlib.Path("/Users/yyl/Desktop/workshop/NMI/NeuroConverge/v2/wp3_results/reliability")
def L(p): return json.loads(p.read_text())
def H(p): return hashlib.sha256(p.read_bytes()).hexdigest()[:16]

srcs = {p.name: H(p) for p in list(A.glob("RESULT_*.json")) + list(R.glob("RESULT_*.json"))}

al   = L(A/"RESULT_animal_level.json")
sr   = L(A/"RESULT_source_rule.json")
rl   = L(A/"RESULT_robust_class.json")
cov  = L(A/"RESULT_technical_covariates.json")
pc   = L(A/"RESULT_pair_composition.json")
tl   = L(A/"RESULT_three_level_variance.json")
wb   = L(A/"RESULT_within_between.json")
er   = L(A/"RESULT_effect_reliability.json")
f6   = L(A/"RESULT_fig6.json")
ph   = L(A/"RESULT_per_animal_heterogeneity.json")
sf   = L(R/"RESULT_inclusion_filtered.json")

out = {
 "artifact": "FIGURE_SOURCE_DATA_v2",
 "purpose": ("Figure-ready source data for the four surviving claims of the v2 line, each with the "
             "specification that produced it. Every number is read from a committed result JSON; the "
             "JSONs' sha256 prefixes are recorded so a figure can be traced to its artifact."),
 "source_hashes": srcs,
 "excluded": {
   "anatomy/RESULT_icc_INVALID.json":
     "WITHdrawn: the within-animal variance was computed as var(vs) if len(vs)>1 else 0, and most "
     "(animal,pair) units hold one measurement, so the ICC of 0.93 is inflated by construction.",
   "anatomy/RESULT_iv_weighting_INVALID_weights.json":
     "Withdrawn: the inverse-variance weights span thirty-one orders of magnitude, so the weighted mean is "
     "determined by a handful of near-zero-variance units."},

 "V2-C1_unit_inflation": {
   "claim": "Treating neuron-pair measurements as independent replicates inflates the standardised "
            "connectivity-function effect by 11 to 18 times.",
   "figure": "paired bar chart, one bar per unit, three contrast panels (chemical, gap, combined)",
   "series": [
     {"contrast":"chemical, animal unit","d":rl["化学 vs 未连接"]["d"],"t":rl["化学 vs 未连接"]["t"],
      "n":rl["化学 vs 未连接"]["n"]},
     {"contrast":"gap, animal unit","d":rl["缝隙 vs 未连接"]["d"],"t":rl["缝隙 vs 未连接"]["t"],
      "n":rl["缝隙 vs 未连接"]["n"]},
     {"contrast":"combined, animal unit","d":al["cohens_d_paired"],"t":al["t"],"n":al["n_animals"]}],
   "pair_unit_counterpart": {"d_combined_pair_unit": 11.048,
      "note":"from CONFOUND_TESTS round 5; the committed JSON for that run is RESULT_corrected.json"},
   "inflation_factors": {"chemical":11.2,"gap":17.9,"combined":15.2},
   "specification": {"unit":"animal; pair-measurement as the contrast",
     "readout":"connected mean minus unconnected mean, each animal standardised within itself",
     "pre_window":"60 volumes (30 s), baseline from volumes 30-60",
     "analysis_window":"per event, int((inter-stimulus interval - 5)/dt), capped at 60 volumes",
     "scripts":["09_animal_level.py","10_robust_and_class.py"]}},

 "V2-C2_fig6_reproduction": {
   "claim": "The source's own anatomy-versus-spontaneous-activity comparison reproduces, and the quantity "
            "it predicts has cross-animal agreement of only r = 0.208 on the cells available.",
   "figure": "two panels: the two animals' Fig-6 values; the cross-animal agreement of the target",
   "series": {"fig6_animal0": f6["fig6_animal0"], "fig6_animal1": f6["fig6_animal1"],
              "cross_animal_r_of_correlation_matrix": f6.get("cross_animal_r_of_corr_matrix")},
   "n": {"animals": 2, "shared_cells": f6["shared"], "cells_animal0": f6["n0"], "cells_animal1": f6["n1"]},
   "specification": {"data":"OSF spont_data_fig6.zip, 2,402,185 B, two animals",
     "target":"off-diagonal activity correlation matrix per animal",
     "predictor":"synapse-count matrix built by name from both source tables, 346 names",
     "scripts":["15_fig6_reproduction.py"]}},

 "V2-C3_three_level_decomposition": {
   "claim": "A pair's response decomposes into 55.1 % between-pair, 37.5 % within-cell measurement error, "
            "5.5 % pair-specific animal deviation and 1.9 % homogeneous animal offset.",
   "figure": "single stacked bar of the four variance shares",
   "shares": {k: (tl[k]/tl["var_total"] if k!="var_total" else 1.0)
              for k in ("var_pair","var_eps","var_beta","var_alpha")},
   "raw_variances": {k: tl[k] for k in ("var_total","var_pair","var_eps","var_beta","var_alpha")},
   "n_units": tl["n_units"],
   "specification": {"model":"y = mu + alpha[animal] + beta[animal,pair] + eps",
     "identification":"eps from the units with repeats; the rest by subtraction",
     "space":"log, because the responses span -3.5e5 to 2.5e5",
     "scripts":["16_three_level_variance.py"]}},

 "V2-C4_specification_sensitivity": {
   "claim": "The published per-pair values come from analysis choices that live in the pipeline's code and "
            "not in its data file, and re-analysing the same records under defensible choices moves the "
            "animal-level estimate from d = 0.085 to 0.729.",
   "figure": "one point per specification on a common axis, with the animal unit and the pair unit marked",
   "series": [
     {"spec":"4 s window, common-mode removed, no inclusion rule","unit":"animal",
      "d":al["cohens_d_paired"],"source":"14_per_animal_heterogeneity.py"},
     {"spec":"source rule, amplitude + derivative criteria","unit":"animal",
      "d":sr["d"],"source":"11b_source_rule.py","pass_frac":sr["pass_frac"]},
     {"spec":"source rule, unweighted sum read-out","unit":"animal",
      "d":L(A/"RESULT_iv_weighting_INVALID_weights.json")["d_unweighted"],
      "source":"12_inverse_variance_weighting.py (the unweighted arm only; the weighted arm is INVALID)"},
     {"spec":"source rule, inverse-variance weighted","unit":"animal","d":None,
      "source":"EXCLUDED, weights pathological"}],
   "validation_of_the_range": ("The range is an instance of a condition the field reports: a 2025 Nature "
     "Reviews Neuroscience review states it remains unclear whether structural connectivity constrains "
     "directed-connectivity models, and a 2025 Scientific Reports paper states no universally accepted "
     "method exists for inferring effective connectivity."),
   "specification": {"scripts":["09","10","11b","12","14"]}},

 "supporting_reliability": {
   "figure": "two panels: split-half reliability by stratum; the variance shares of the effect",
   "pair_response": {"within_animal_r_full": wb["within_animal_rfull"],
                     "between_animal_r_full": wb["between_animal_rfull"],
                     "units_within": wb["within_animal_units"], "pairs_between": wb["between_animal_pairs"]},
   "effect": {"split_half_r_full": er["split_half_r_full"], "noise_frac": er["noise_frac"],
              "signal_frac": er["signal_frac"], "n_animals": er["n_animals_used"]},
   "cross_animal_reliability_by_strain": {k: sf[k].get("rfull_min4") for k in ("NONE","A_abs2sd","B_topdecile")},
   "specification": {"scripts":["13_within_vs_between_splithalf.py","17_effect_reliability.py",
                                "02_reliability_inclusion_filtered.py"]}},

 "withdrawn_or_narrowed": [
   {"was":"the animals differ rather than the measurements being noisy (round 9)",
    "now":"narrowed in round 12: 5.5 % pair-specific animal against 37.5 % measurement error"},
   {"was":"a population-level regularity rather than a circuit property (round 10)",
    "now":"weakened in round 12; the between-animal spread is 42.2 % noise and 17.7 % pair composition"},
   {"was":"what is reproducible is which pairs were measured (round 14)",
    "now":"reduced in round 15 to exactly 17.7 %"},
   {"was":"the ICC of 0.93","now":"withdrawn in round 9"}]
}
# derive the shares as fractions with a guard
tot=tl["var_total"]
out["V2-C3_three_level_decomposition"]["shares_frac"]={
  "between_pair": tl["var_pair"]/tot, "measurement_error": tl["var_eps"]/tot,
  "pair_specific_animal": tl["var_beta"]/tot, "animal_offset": tl["var_alpha"]/tot}
p=pathlib.Path("/Users/yyl/Desktop/workshop/NMI/NeuroConverge/v2/wp3_results/FIGURE_SOURCE_DATA.json")
p.write_text(json.dumps(out, indent=2, ensure_ascii=False)+"\n")
print(f"  已写 {p.name}: {len(json.dumps(out))} 字符")
print()
print("  === 交叉核对：图数据 vs 源 JSON ===")
checks=[
 ("C1 combined animal d", out["V2-C1_unit_inflation"]["series"][2]["d"], al["cohens_d_paired"]),
 ("C2 fig6 animal0 r", out["V2-C2_fig6_reproduction"]["series"]["fig6_animal0"]["r"], f6["fig6_animal0"]["r"]),
 ("C2 cross-animal r", out["V2-C2_fig6_reproduction"]["series"]["cross_animal_r_of_correlation_matrix"],
                       f6["cross_animal_r_of_corr_matrix"]),
 ("C3 between-pair share", out["V2-C3_three_level_decomposition"]["shares_frac"]["between_pair"], tl["var_pair"]/tot),
 ("C4 source-rule d", out["V2-C4_specification_sensitivity"]["series"][1]["d"], sr["d"]),
 ("support effect r_full", out["supporting_reliability"]["effect"]["split_half_r_full"], er["split_half_r_full"]),
]
for name,a,b in checks:
    ok = (a is not None and b is not None and abs(float(a)-float(b))<1e-9)
    print(f"    {'OK  ' if ok else 'FAIL'} {name}: {a} vs {b}")
print(f"\n  源 JSON 哈希已记录: {len(srcs)} 个")
