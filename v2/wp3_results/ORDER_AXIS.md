# The order of application is the largest single specification dimension

**Status: the order axis is measured. The exact correctness check now passes, the order effect dwarfs the
dimensions the ledger lists, and one order is stable across windows while the other swings by a full unit and
crosses zero.** No model was fitted.

**This is the twentieth self-found defect: round 41's correctness check was read as passing when the exact
match is a different cell of this grid.**

---

## 1. The correctness check, and where round 41 read it wrong

**`09_animal_level.py` applies, in this order: the raw difference; per-cell normalisation if any; the per-event
weighting; the common mode; the average over volumes.** **That is ORDER A in this grid when both are on.**

**But the code applies NO per-cell normalisation.** **So the cell of this grid that is exactly the code is
`w` -- weighting alone -- and it returns:**

```
order w, post 24:  d_A = 0.7289   t = 7.610   n = 109
09_animal_level.py: d_A = 0.7289   t = 7.610   n = 109
```

> **Exact to four decimal places.** **That is the correctness check this line has been trying to pass since
> round 34, and this round passes it.**

**Round 41 read `post=24, cellnorm=off, weighted=on` as its check cell and got 0.7331, then attributed the
0.0042 difference to a "slightly different event set".** **That attribution was wrong: the exact match is
available in this grid, and round 41's 0.0042 was an implementation difference it did not find.** **The round-41
grid's joint value at post 24, 0.9659, agrees with this grid's ORDER A value, 0.9685, so its ORDER A arm is
sound; only its check cell was mislabelled.**

## 2. The grid

| order | definition | post 12 | post 24 | post 48 |
| --- | --- | --- | --- | --- |
| **none** | raw difference only | +0.2175 | +0.3933 | +0.3984 |
| **cn** | per-cell normalisation only | **-0.0358** | +0.0475 | +0.0879 |
| **w** | weighting only (**the code's step**) | +0.4550 | **+0.7289** | +0.8474 |
| **A** | per-cell normalisation, **then** weighting | +0.0958 | **+0.9685** | **-0.0958** |
| **B** | weighting, **then** per-cell normalisation | +0.1192 | +0.1192 | +0.1133 |

```
all fifteen cells:  d_A = -0.0958 to +0.9685,   a range of 1.0643, and it crosses zero
```

## 3. Finding: the order is the largest dimension

**ORDER A and ORDER B differ only in which array the weighting's denominator is computed from:**

```
A:  sd = nanmedian(nanstd(dv / s_cell, axis=1))     -- from the cell-normalised differences
B:  sd = nanmedian(nanstd(dv,            axis=1))   -- from the raw differences
```

**They coincide only if every cell's scale is equal, and they are not equal, so the two orders give different
estimators.**

| post | ORDER A | ORDER B | **the order effect** |
| --- | --- | --- | --- |
| 12 | +0.0958 | +0.1192 | **+0.0234** |
| **24** | **+0.9685** | **+0.1192** | **-0.8493** |
| **48** | **-0.0958** | **+0.1133** | **+0.2091** |

> **At post 24 the two orders differ by 0.85, which is larger than any dimension in the ledger and larger than
> V2-C4's entire reported span of 0.64.**

**And their stability differs as much as their values:** **ORDER B gives 0.1192, 0.1192 and 0.1133 across the
three windows, a spread of 0.006; ORDER A gives 0.0958, 0.9685 and -0.0958, a spread of 1.064.** **One order is
essentially window-independent and the other is not.**

## 4. What this does to the ledger and to V2-C4

**The ledger gains a seventh dimension, and it is the largest.** **Its measured size is not a fixed number --
it is 0.02 at one window and 0.85 at another -- so it cannot be entered as a scalar at all, which is the
strongest instance yet of the ledger's list-not-budget warning.**

**And V2-C4's claim is now demonstrated in its sharpest form:**

> **Two orderings of the same two normalisations, both defensible, applied to the same records, give
> animal-level estimates of +0.97 and +0.12 at the same window. No document declares which order the pipeline
> uses; the order is recoverable only by reading four lines of code; and one of the two orderings is stable
> across windows while the other ranges over a full unit and changes sign.**

**V2-C4 has never claimed more than that the specification is in the code and not in the file.** **This round
supplies the single largest instance of it.**

## 5. A caveat that must travel with section 3

**ORDER A is not a pipeline that anyone wrote.** **It is per-cell normalisation followed by the weighting, and
the code does the weighting without any per-cell normalisation.** **So ORDER A is a CONSTRUCTED specification,
defensible in the sense that both steps are defensible, and not a description of the artifact.**

**What makes the comparison meaningful is that a reader choosing to add per-cell normalisation must then decide
where to put it, and the two placements are not equivalent.** **That is the point: the choice a user faces is
not only whether to normalise but where, and the difference is 0.85.**

## 6. What is owed

1. **A check of the `cn`-only arm's negative value at post 12 (-0.0358)**, which is the first negative in the
   grid that does not involve ORDER A. **Named, not explained.**
2. **The two external items:** an independent reviewer, and the owner's decision on the plan's constraint.

## 7. Provenance

* Script `anatomy/40_order_axis.py`; output `anatomy/RESULT_order_axis.json`.
* **The `w` arm at post 24 reproduces `09_animal_level.py` exactly, which is the correctness check this line
  has been unable to pass since round 34.**
* **No model was fitted. No causal claim is made.**
