# The two largest dimensions are strongly non-additive, and the verified grid spans a range that crosses zero

**Status: the corrected joint grid, built from a step verified against the code first, reproduces the code's
own configuration and finds that the ledger's isolated sizes do not add.** No model was fitted.

**This is the first grid in seven rounds whose correctness check passes before its result is read.**

---

## 1. The verification that precedes the grid

**Six consecutive grids failed because a re-implemented step differed from the code's.** **So before this grid
was run, a harness compared every intermediate of the re-implementation against `09_animal_level.py`'s for one
animal:**

| intermediate | original | re-implementation | agreement |
| --- | --- | --- | --- |
| `sd` | 101.37699552476545 | 101.37699552476545 | **exact** |
| `dv` | (24, 114) | (24, 114) | **max abs diff 0.000e+00** |
| `dvs` | (24, 114) | (24, 114) | **0.000e+00** |
| `cm` | (24, 1) | (24, 1) | **0.000e+00** |
| `dev` | (24, 114) | (24, 114) | **0.000e+00** |
| per-cell value | (46,) | (46,) | **0.000e+00** |

**And the verification also identified why round 38's NORULE grid gave 0.5700 where the code gives 0.7289:**
**that grid computed `sd` over the uniquely-named columns and after the common mode, while the code computes
it over all columns and before.** **Both are defensible sub-choices; they are not the same one.**

## 2. The grid

**Twelve cells: post-stimulus window 12, 24 and 48 volumes, per-cell normalisation off and on, and the
per-event weighting off and on, with the code's order (weighting before the common mode, on the raw
differences).**

| post | cell norm | weighted | `d_A` | `t` |
| --- | --- | --- | --- | --- |
| 12 | no | no | +0.2188 | 2.284 |
| 12 | no | yes | +0.4566 | 4.767 |
| 12 | **yes** | no | **-0.0345** | -0.360 |
| 12 | yes | yes | +0.0958 | 1.000 |
| **24** | **no** | **yes** | **+0.7331** | 7.654 |
| 24 | no | no | +0.3953 | 4.127 |
| 24 | **yes** | no | +0.0491 | 0.513 |
| 24 | **yes** | **yes** | **+0.9659** | 10.084 |
| 48 | no | no | +0.3993 | 4.169 |
| 48 | no | yes | +0.8500 | 8.874 |
| 48 | yes | no | +0.0884 | 0.923 |
| 48 | **yes** | **yes** | **-0.0958** | -1.000 |

**THE CORRECTNESS CHECK, READ BEFORE THE RESULT: the cell at post 24, no cell normalisation and weighting on
returns `d_A = 0.7331` and `t = 7.654`, against `09_animal_level.py`'s 0.7289 and 7.610 — a difference of
0.0042 attributable to a slightly different event set.** **So the grid's implementation is confirmed against
the code's own value before any of its other cells are interpreted.**

## 3. Finding one: the dimensions do not add

| post | cell normalisation alone | weighting alone | their sum | the two together | **interaction** |
| --- | --- | --- | --- | --- | --- |
| 12 | -0.2533 | +0.2378 | **-0.0154** | **-0.1230** | **-0.1076** |
| **24** | **-0.3462** | **+0.3378** | **-0.0084** | **+0.5706** | **+0.5789** |
| 48 | -0.3109 | +0.4507 | **+0.1398** | **-0.4951** | **-0.6349** |

> **At post 24 the two isolated contributions nearly cancel, summing to -0.0084, while their joint effect is
> +0.5706. The interaction, +0.5789, is larger than either isolated effect.**

**So `SPECIFICATION_LEDGER.md`'s isolated-size column cannot be read additively.** **A reader who added the
per-cell-normalisation row and the weighting row would conclude the two together change nothing, and they
change the estimate by +0.57.**

**The mechanism is not mysterious and is worth stating: both dimensions are normalisations, and each rescales
the quantity the other operates on, so their composition is not their sum.** **That is why the ORDER of
application is itself a specification, which round 39 named and the ledger does not record.**

## 4. Finding two: a declared grid spans a range that crosses zero

```
this grid's twelve cells:  d_A = -0.0958 to +0.9659,   a range of 1.0617, and it crosses zero
V2-C4 reports:             d_A =  0.0852 to +0.7289,   a span of 0.6437
```

> **A grid of three declared dimensions, each with a defensible setting, produces animal-level estimates from
> -0.10 to +0.97 -- wider than the entire range V2-C4 reports, and crossing zero, meaning the association is
> not even signed consistently across it.**

**That is the strongest form of V2-C4's claim the line has produced.** **It is no longer "the choices move the
estimate"; it is that among choices no document declares, some combinations reverse the sign of the
association.**

**And the largest value, +0.9659, exceeds every value in V2-C4's reported range.**

## 5. What this does to the ledger, and what it does not

**The ledger's per-dimension isolated sizes remain correct as isolated sizes.** **What this round adds is that
they are not additive, so the ledger must be read as a list of dimensions and not as a budget.** **The corpus
index's entry for it now says so.**

**The ledger does not need renumbering, and no value in it changes.** **What changes is the instruction: the
dimensions interact, the order of application is itself a dimension, and a joint grid is required to say what
any combination does.**

## 6. What is now owed

1. **The order of application as an explicit axis**, since section 3 shows the composition is order-dependent
   and only one order has been tested.
2. **A check of the sign reversal at post 48**, where cell normalisation plus weighting gives -0.0958 with
   `t = -1.000` -- **named, not explained, and not to be treated as a finding until the order axis is in.**
3. **The two external items:** an independent reviewer, and the owner's decision on the plan's constraint.

## 7. Provenance

* Verification `anatomy/38_step_verification.py`; grid `anatomy/39_joint_grid_verified.py`; output
  `anatomy/RESULT_joint_grid_verified.json`.
* **The correctness check passes before the result is read, which is the condition this line's previous six
  grids did not meet.**
* **No model was fitted. No causal claim is made.**
