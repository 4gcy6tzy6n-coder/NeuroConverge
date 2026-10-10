# Figure render manifest

**Each PNG with the sha256 of the script that produced it and the commit at which it was rendered.**
**This exists because an isolated reviewer found that the six committed images preceded the final state of
the script said to render them, and that nothing recorded which script revision produced a given image.**

**Script:** `make_figures.py`

| png | bytes |
| --- | --- |
| `Fig1_specification_ledger.png` | 74963 |
| `Fig2_nonadditivity.png` | 49260 |
| `Fig3_order.png` | 68093 |
| `Fig4_decomposition.png` | 103621 |
| `Fig5_like_for_like.png` | 78271 |
| `Fig6_defect_ledger.png` | 174067 |

**Script sha256 at this render:** `a47ee7b4b510b687d581949e4e9f7a758d98f009d7f8fd06a3ab22c9ff7d08ff`

**Rendered at commit:** `9fcb555`

**Every image above was regenerated after this manifest's script revision, so no committed PNG
predates the script that is said to render it.**
