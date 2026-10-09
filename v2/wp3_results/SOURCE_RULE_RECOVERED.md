# The source's actual analysis rule, recovered from its own code

**Status: specification recovered and quoted. It shows that every contrast this audit has computed so far
used the wrong analysis window and an invented inclusion rule.** No model was fitted.

**Why this document exists.** `FINAL_ESTIMATE_AND_COLLIDER_WARNING.md` identified the blocking task as
*obtain the source's two thresholds*. **They are in the public code and are recovered below, together with
three further parts of the rule that this audit had not even guessed.** The consequence is that the
numbers in every earlier document of this line were produced under a different specification from the
source's, and **that is now the most important thing to say about them.**

---

## 1. Where it came from

`github.com/leiferlab/pumpprobe`, `pumpprobe/Fconn.py`, the `Fconn` class, `from_objects` and the
autoresponse-detection block. Quoted verbatim with line numbers from the file as fetched this session.

## 2. The parameters

```python
nan_thresh     = 0.05      # class default, line 9
deriv_thresh   = 1.0       # signature default, line 141
ampl_thresh    = 1.0       # signature default, line 141
deriv_min_time = 2.0       # signature default, line 141   -> seconds
ampl_min_time  = 5.0       # signature default, line 141   -> seconds
```

converted inside the analysis by

```python
deriv_min_vols = deriv_min_time/rec.Dt      # line 280   -> 4 volumes at Dt = 0.5 s
ampl_min_vols  = ampl_min_time/rec.Dt       # line 319   -> 10 volumes
```

and the analysis window is **not** the response duration but the whole inter-stimulus interval:

```python
max_vol_n = int((int_btw_stim-5)/rec.Dt)    # line 261, with int_btw_stim in seconds
if max_vol_n*rec.Dt > 30: max_vol_n_p = int(30/rec.Dt)   # line 286-287
```

**With the measured inter-stimulus interval of 31.0 s** (median, from all 113 animals — see
`WINDOW_RESOLVED.md`), **`max_vol_n = int((31-5)/0.5) = 52 volumes, i.e. about 26 seconds.**

## 3. The amplitude criterion, verbatim

```python
# 1) Either rise above (or below) a multiple of the absmax of the pre-stimulus signal, at least for a
#    minimum amount of time.
# 1a: Go above.  1b: Go below.
# 1_b: Go above/below with half the threshold but for twice the minimum contiguous time.
# The neuron needs to pass the threshold in a CONTIGUOUS number of volumes.
...
condition1a  = r_restr[:,i_neu] >  ampl_thresh*absmax[i_neu]
condition1a2 = r_restr[:,i_neu] >  0.5*ampl_thresh*absmax[i_neu]
condition1b  = r_restr[:,i_neu] < (-ampl_thresh*absmax[i_neu])
condition1b2 = r_restr[:,i_neu] < (-0.5*ampl_thresh*absmax[i_neu])
```

**The reference quantity is `absmax` — the maximum absolute value of the pre-stimulus signal — not a
standard deviation.** **And the test is on the maximum length of a run of consecutive volumes satisfying
it**, via

```python
contcond1a = np.diff(np.where(np.concatenate(([condition1a[0]],
                                 condition1a[:-1] != condition1a[1:],
                                 [True])))[0])[::2]
ampl_selection1a[i_neu] = np.max(contcond1a) > ampl_min_vols
```

**So: a run of more than 10 consecutive volumes above `1.0 x absmax(pre)`, or of more than 20 above half
of it.**

## 4. Three further parts of the rule this audit had not guessed

**4a -- the tail problem, handled explicitly.** This is the same phenomenon this audit identified
independently and named "the pre-stimulus window sits inside the previous event's tail":

```python
# SECOND CRITERION ON THE AMPLITUDE
# 2) But the above selection would discard traces that have a large pre-stimulus signal because they were
#    responding to the previous stimulation.
# So, for the previously responding neurons (old_selected_) allow to rise even only above a multiple of
# the rolling standard deviation.  The neuron needs to pass the threshold in a CONTIGUOUS number of
# volumes.
condition2 = np.abs(r_restr[:,i_neu]) > ampl_thresh*loc_std_seg[i_neu]
```

**4b -- a shape or slope check, to reject a V-shaped artefact.** Criterion 2* requires that the fitted
slope in the last 25 volumes of the pre-window be non-positive and the slope at the start of the post
window be non-negative, else the response is discarded:

```python
# 2*) But traces that pass this condition need to be subject to a further check, to avoid including
#     /|\ in addition to /\|/\
...
if not (dr_2a<=5e-2 and dr_2b>=5e-2):
    ampl_selection2[i_neu] = False
    # If the response should be excluded based on this criterion, then it should be excluded in general.
```

**4c -- a derivative criterion, separate from the amplitude one.**

```python
deriv_selection = np.sum(np.absolute(post_dr-prev_dr)/pre_avg_sig>deriv_thresh,axis=0)>=deriv_min_vols
```

**and a NaN criterion** limiting contiguous missing stretches, `nan_thresh*(i1-i0)`.

## 5. What this means for every number this audit has produced

**Comparison of the source's specification with what this audit actually did:**

| element | source | this audit, all documents to date |
| --- | --- | --- |
| analysis window | `max_vol_n` = 52 volumes, **about 26 s** | **8 volumes (4 s)**, then 2-32 volumes in the window sweep |
| amplitude reference | **`absmax` of the pre-stimulus signal** | **standard deviation** |
| contiguous requirement | **> 10 volumes** above `1.0 x absmax`, or > 20 above half | none, or an invented 8-volume rule |
| derivative criterion | present, 4 volumes | **absent** |
| tail handling | present, criterion 2 | **absent** |
| shape or slope check | present, criterion 2* | **absent** |
| NaN handling | present, 5 % | partial |

> **This audit's contrasts differ from the source's specification in at least five respects
> simultaneously. The `d` values in `ANATOMY_FUNCTION_RETEST.md`, `CONFOUND_TESTS.md`,
> `RETRACTION_window_dependence.md`, `WINDOW_RESOLVED.md` and `FINAL_ESTIMATE_AND_COLLIDER_WARNING.md`
> are therefore not estimates of the paper's quantity and should not be read as such.**

**What survives unchanged:** the reliability measurement of `ATLAS_RELIABILITY_AUDIT.md`, which uses no
window, no inclusion rule and no anatomical matrix — **it measures split-half reproducibility of the
per-pair values themselves, and is independent of all of the above.**

**What is now much weaker than this audit implied:** anything about which layer carries a connectivity
association. **The audit has been comparing windows and filters of its own construction, not the source's
analysis.**

## 6. The one claim this strengthens

**The published derived matrix `funatlas.h5` carries per-pair values produced by the pipeline above. Its
provenance record, as far as this audit can see, does not carry the specification.** A downstream user
receives a `(300, 300)` array of numbers and, from the file alone, cannot recover:

* that the analysis window is the inter-stimulus interval minus five volumes, not a fixed response window;
* that the amplitude criterion is relative to `absmax(pre)` rather than to noise or SD;
* that more than ten contiguous volumes are required;
* that tail inheritance from the previous stimulation is handled by a separate criterion;
* that a slope check rejects V-shaped artefacts.

**Those five elements are all in the public code, and none of them is in the data file.** That is the
evidential transition this line has been circling, now stated with the specifics attached rather than as a
generality.

## 7. The bounded next task, now fully specified

1. **Reimplement the criterion above** — `absmax` reference, `ampl_min_vols = 10`, `deriv_min_vols = 4`,
   the two half-threshold variants, criterion 2 for previously-selected neurons, and the slope check —
   and verify it reproduces a plausible retention fraction.
2. **Use a 52-volume analysis window**, or the source's own `max_vol_n` if the exact interval is
   recoverable per event.
3. **Then, and only then, re-run the anatomical contrasts** and compare against the source's reported
   result rather than against this audit's own earlier numbers.
4. **Determine `shift_vol`**, the pre-stimulus reference length, which this audit has not yet read out of
   the code; the value used above, 8 volumes, is likewise unverified.

**Until step 3 is done, this line has no defensible estimate of the connectivity-function association.**

## 8. Provenance

* `pumpprobe/Fconn.py`, `github.com/leiferlab/pumpprobe`, fetched this session; all quotations carry their
  line numbers.
* Inter-stimulus interval: measured from all 113 `{i}_stim_volume_i.txt` files, median 31.0 s.
* Stimulus duration and the source's prose statement: Europe PMC full text of PMC10632145.
* **No model was fitted. No biological claim is made. Every earlier `d` value in this line is marked as
  computed under a different specification.**
