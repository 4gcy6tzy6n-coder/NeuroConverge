# DMP fast–slow correspondence V1 results

**Status:** independently recalculated from the stored per-trial losses. This is a post-result project extension with a pre-run-frozen module protocol, not a project-level preregistration or biological validation.

The primary unit is the synthetic task-instance seed. Families and endpoints are reported separately; raw classification loss and normalized state-estimation MSE are not pooled.

## Primary 2 × 2 interaction

Positive values mean the cost of breaking slow-context correspondence is larger for the fast–slow model than for its matched short-state control.

| Task family | Interaction mean (95% paired task-instance bootstrap CI) | Raw permutation P | Holm-adjusted P | Aligned DMP advantage | Task gate |
|---|---:|---:|---:|---:|---|
| DELAYED_ASSOCIATION | -0.00212 [-0.00615, 0.00173] | 0.32377 | 0.64755 | 0.00208 [-0.00345, 0.00814] | FAIL |
| STATE_ESTIMATION | -0.00218 [-0.00383, -0.00054] | 0.01686 | 0.050579 | -0.00243 [-0.00363, -0.00123] | PASS |
| CONTEXTUAL_DECISION | 0.00101 [-0.00537, 0.00778] | 0.77924 | 0.77924 | 0.00156 [-0.00573, 0.00931] | PASS |

## Data scaling

| Task family | N=128 DMP advantage (95% CI) | N=512 | N=2048 | Advantage slope per log₂(N) (95% CI) |
|---|---:|---:|---:|---:|
| DELAYED_ASSOCIATION | -0.00160 [-0.00521, 0.00107] | -0.00313 [-0.00830, 0.00133] | 0.00208 [-0.00348, 0.00827] | 0.00092 [-0.00046, 0.00244] |
| STATE_ESTIMATION | -0.00713 [-0.01183, -0.00235] | -0.00013 [-0.00211, 0.00177] | -0.00243 [-0.00361, -0.00122] | 0.00118 [-0.00018, 0.00246] |
| CONTEXTUAL_DECISION | 0.07236 [0.05036, 0.09557] | 0.03506 [0.01335, 0.05954] | 0.00156 [-0.00563, 0.00941] | -0.01770 [-0.02288, -0.01274] |

## Longer-delay OOD

Per-family and per-model IID/OOD losses are retained in `SUMMARY.json`. OOD results are secondary and use the unchanged fitted model.

## Interpretation ceiling

A positive interaction would support only the tested computational abstraction in these synthetic tasks. It would not validate cortical biology, prove biological provenance caused an advantage, establish a general transfer law, or make the manuscript NMI-ready. The fast–slow idea and DMP-SNN have substantial published precedent.
