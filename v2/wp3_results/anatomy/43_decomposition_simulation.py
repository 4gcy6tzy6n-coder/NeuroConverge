"""Does the variance decomposition recover components it was not told, under a known truth?

An isolated reviewer objected that the manuscript's reliability numbers come from a decomposition that returns a
NEGATIVE variance share at its unrestricted specification, that this is admitted unresolved, and that no reader
can tell whether the retained specifications are inside or outside the failure region.

This simulates the decomposition under a truth it is given, so the estimator's behaviour is known rather than
inferred.  The model is the one the manuscript uses: y = mu + alpha[animal] + beta[animal,pair] + eps, fitted in
log space, with eps identified from repeated-measurement cells and the rest obtained BY SUBTRACTION.
"""
import numpy as np, json, pathlib

rng = np.random.default_rng(20261010)
# truth, in the same units the manuscript's decomposition reports
VAR_ALPHA, VAR_BETA, VAR_EPS = 0.30, 0.55, 0.75       # animal offset, pair-specific animal, within-cell error
N_ANIMALS = 109
N_PAIRS_PER_ANIMAL = 200
# a fraction of (animal, pair) cells carry repeat measurements, which is what identifies eps
REPEAT_FRAC = 0.20
N_REPEATS = 2

def simulate(p_repeat=REPEAT_FRAC, n_rpt=N_REPEATS):
    rows = []                                          # (animal, pair, value)
    for a in range(N_ANIMALS):
        al = rng.normal(0, np.sqrt(VAR_ALPHA))
        be = rng.normal(0, np.sqrt(VAR_BETA), N_PAIRS_PER_ANIMAL)
        for p in range(N_PAIRS_PER_ANIMAL):
            k = n_rpt if rng.random() < p_repeat else 1
            for _ in range(k):
                rows.append((a, p, al + be[p] + rng.normal(0, np.sqrt(VAR_EPS))))
    return np.array(rows, dtype=float)

def decompose(rows, min_an=1):
    """The manuscript's estimator: mu + alpha[animal] + beta[animal,pair] + eps, rest by subtraction."""
    y = np.log(np.abs(rows[:, 2]) + 1e-9)              # log space, as the manuscript specifies
    a = rows[:, 0].astype(int); p = rows[:, 1].astype(int)
    # restrict to pairs measured in at least min_an distinct animals
    key = {}
    for ai, pi in zip(a, p):
        key.setdefault(pi, set()).add(ai)
    keep_pairs = {pi for pi, s in key.items() if len(s) >= min_an}
    m = np.isin(p, list(keep_pairs))
    y, a, p = y[m], a[m], p[m]
    if y.size == 0:
        return None
    mu = y.mean()
    # alpha: animal means
    am = {ai: y[a == ai].mean() for ai in np.unique(a)}
    alpha = np.array([am[ai] - mu for ai in a])
    # eps: within (animal, pair) variance, from cells with >1 measurement
    resid = y - mu - alpha
    eps_num, eps_den = 0.0, 0
    seen = {}
    for ai, pi, r in zip(a, p, resid):
        seen.setdefault((ai, pi), []).append(r)
    for v in seen.values():
        if len(v) > 1:
            eps_num += np.var(v, ddof=1) * (len(v) - 1)
            eps_den += len(v) - 1
    var_eps = eps_num / eps_den if eps_den else np.nan
    # beta: variance of (animal,pair) means about the animal mean, minus the eps contribution
    pm = {}
    for ai, pi, r in zip(a, p, resid):
        pm.setdefault((ai, pi), []).append(r)
    cell_mean = np.array([np.mean(v) for v in pm.values()])
    cell_n = np.array([len(v) for v in pm.values()])
    var_cellmean = cell_mean.var(ddof=1)
    var_beta = var_cellmean - np.mean(var_eps / cell_n)          # subtract the estimation noise
    var_total = y.var(ddof=1)
    var_alpha = np.var([am[ai] - mu for ai in sorted(am)], ddof=1)
    var_pair = var_total - var_alpha - var_beta - var_eps        # by subtraction, as the manuscript does
    return dict(var_total=var_total, var_alpha=var_alpha, var_beta=var_beta,
                var_eps=var_eps, var_pair=var_pair,
                frac_alpha=var_alpha/var_total, frac_beta=var_beta/var_total,
                frac_eps=var_eps/var_total, frac_pair=var_pair/var_total)

out = {"truth": {"var_alpha": VAR_ALPHA, "var_beta": VAR_BETA, "var_eps": VAR_EPS},
       "n_animals": N_ANIMALS, "n_pairs_per_animal": N_PAIRS_PER_ANIMAL,
       "simulation": []}
print(f"  Truth: alpha={VAR_ALPHA}, beta={VAR_BETA}, eps={VAR_EPS}")
print(f"  {'min_an':>7} {'beta_hat':>10} {'eps_hat':>10} {'beta_frac':>10} {'beta<0':>7}")
for min_an in (1, 2, 3, 5):
    recs = []
    for rep in range(8):                      # replicate the whole experiment
        r = decompose(simulate(), min_an=min_an)
        if r: recs.append(r)
    if not recs: continue
    bh = np.mean([x["var_beta"] for x in recs])
    eh = np.mean([x["var_eps"] for x in recs])
    bf = np.mean([x["frac_beta"] for x in recs])
    neg = sum(1 for x in recs if x["var_beta"] < 0)
    print(f"  {min_an:>7} {bh:>10.3f} {eh:>10.3f} {bf:>10.3f} {neg:>4}/{len(recs)}")
    out["simulation"].append({"min_an": min_an, "var_beta_hat": float(bh), "var_eps_hat": float(eh),
                              "frac_beta_hat": float(bf), "n_negative_beta": int(neg), "n_replicates": len(recs)})
pathlib.Path("v2/wp3_results/anatomy/RESULT_decomposition_simulation.json").write_text(
    json.dumps(out, indent=2))
print(f"\n  ==> 真值 beta = {VAR_BETA}；若估计量在 min_an=1 处系统性偏低或为负，则不良态是估计量的性质而非数据的")
