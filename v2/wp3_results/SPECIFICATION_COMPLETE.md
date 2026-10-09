# The complete source specification, and the root cause of everything in this line

**Status: the specification is now complete. It identifies the root cause of the anomalies this line spent
four documents chasing, and it shows the root cause was this audit's baseline, not the data.** No model
was fitted.

---

## 1. The last unknown

`pumpprobe/Fconn.py` line 170:

```python
shift_vol = int(delta_t_pre/rec.Dt)
```

**`delta_t_pre` is supplied by the caller, and the caller is in the same package.**
`pumpprobe/Funatlas.py`, lines 2214 and 2426:

```python
delta_t_pre = 30.0
```

**So `shift_vol = int(30.0/0.5) = 60 volumes = 30 seconds`.**

## 2. The complete specification, every element traced to a line

| element | value | source |
| --- | --- | --- |
| pre-stimulus window `shift_vol` | **60 volumes = 30 s** | `Fconn.py:170` with `Funatlas.py:2214` |
| **baseline used for normalisation** | **`baseline_range = [shift_vol//2, shift_vol]`, i.e. volumes 30-60, the second half** | `Fconn.py:256-257` |
| segment length | `int(i0 + 60/dt + shift_vol)` = **60 s plus the pre-window** | `Fconn.py:245` |
| analysis window `max_vol_n` | `int((int_btw_stim-5)/dt)` = **52 volumes = 26 s** at the measured 31.0 s spacing | `Fconn.py:261` |
| `prev_dr` | `average(abs(dr[0 : shift_vol-6]))` = `abs(dr[0:54])` | `Fconn.py:277` |
| `pre_avg_sig` | `median(signal[i0 : i0+shift_vol])` | `Fconn.py:279` |
| `loc_std_seg` | `get_loc_std(sig_seg[6 : shift_vol-6], 4)` = `sig_seg[6:54]`, window 4 | `Fconn.py:315` |
| `nan_thresh` | 0.05, applied to the longest **contiguous** NaN run | `Fconn.py:9, 272` |
| `deriv_thresh`, `deriv_min_time` | 1.0, **2.0 s** -> 4 volumes | `Fconn.py:141, 280` |
| `ampl_thresh`, `ampl_min_time` | 1.0, **5.0 s** -> 10 volumes | `Fconn.py:141, 319` |
| amplitude criterion 1a | `r > ampl_thresh * absmax(pre[0:60])` for **> 10 contiguous** volumes | `Fconn.py:348, 353` |
| criterion 1a2 | same at **half** the threshold for **> 20** contiguous volumes | `Fconn.py:358` |
| criteria 1b, 1b2 | the same two, below zero | `Fconn.py:382, 392` |
| derivative criterion | `sum(abs(post_dr - prev_dr)/pre_avg_sig > deriv_thresh) >= 4` | `Fconn.py:282` |
| tail criterion 2 | for `old_selected_` neurons only, `abs(r) > ampl_thresh * loc_std_seg` for > 10 contiguous volumes | `Fconn.py:430-437` |
| slope check 2* | pre-window last 25 volumes fitted slope `<= 5e-2` **and** post-window slope `>= 5e-2`, else the response is excluded in general | `Fconn.py:459-467` |

## 3. The root cause, stated plainly

**This audit used an 8-volume (4-second) pre-stimulus window. The source uses 60 volumes (30 seconds), and
takes its baseline from the second half of that, 15 to 30 seconds before the stimulus.**

**With a 31-second inter-stimulus interval and a response that this audit itself measured as peaking at
10 seconds and still elevated at 24 seconds, an 8-volume pre-window sits *inside the previous event's
rising phase*.** The consequence is that the pre-stimulus reference against which every response was
measured was itself already elevated and still climbing.

**That single choice explains the anomalies this line spent four documents on:**

* **the measured "response peaks at 10 seconds"** -- the slow apparent rise is what remains after
  subtracting a baseline that was captured mid-rise of the previous event;
* **the monotonic growth of `d` with window length** -- a longer post-window accumulates more of the
  response while the contaminated baseline stays fixed, so the contrast grows without bound;
* **why the chemical layer looked weak at short windows and strong at long ones** -- both layers were being
  measured against the same contaminated baseline, and the ratio between them drifted as the window grew;
* **why a common-mode correction changed the answer so much** -- the global component being removed was
  partly the shared tail of the previous stimulus.

**The source's design avoids all of this deliberately**: a 30-second pre-window, a baseline taken from its
late half, and an explicit tail criterion for previously-responding neurons.

## 4. What this means for the record of this line

**Every `d` value in `ANATOMY_FUNCTION_RETEST.md`, `CONFOUND_TESTS.md`,
`RETRACTION_window_dependence.md`, `WINDOW_RESOLVED.md` and `FINAL_ESTIMATE_AND_COLLIDER_WARNING.md` was
computed against a contaminated baseline, with an analysis window 6.5 times too short, an amplitude
reference of SD rather than `absmax`, no contiguous-run requirement, no derivative criterion, no tail
handling and no slope check.**

**They should not be used, cited, or repaired.** They are retained with mismatch notices appended because a
deleted wrong analysis cannot be audited.

**What survives, and is now the only quantitative result this line has:** the reliability measurement of
`ATLAS_RELIABILITY_AUDIT.md`, `r_full = 0.226` for the bulk of pairs and `0.819` for the best-measured 638.
**It uses no window, no baseline, no inclusion rule and no anatomical matrix.** It is unaffected by
everything in this document.

## 5. The implementation task, now fully specified

**To produce a defensible estimate, implement exactly the section-2 table:**

1. **60-volume pre-window**, baseline from **volumes 30-60** of it.
2. **52-volume analysis window**, or the per-event `max_vol_n` where the interval is recoverable.
3. **`absmax` reference**: `max(abs(pre[0:60]))` per cell.
4. **Contiguous-run test**: longest run of `abs(r) > 1.0 * absmax` must exceed 10 volumes, or the run
   above `0.5 * absmax` must exceed 20.
5. **Derivative criterion** with `prev_dr = mean(abs(dr[0:54]))` and `pre_avg_sig = median(pre[0:60])`.
6. **Criterion 2** for previously-selected neurons, using `loc_std` over `sig_seg[6:54]` with window 4.
7. **Slope check 2\***.
8. **NaN criterion**, contiguous runs below 5 % of the interval.

**Two things must be verified rather than assumed:** the exact value of `int_btw_stim` per event, and
whether `dt` is 0.5 s in all animals — **the exported files give `t` with a 0.5 s step for the one animal
checked, and that has not been confirmed across all 113.**

## 6. Honest assessment of this line's position

**Five rounds in, the line has one solid measurement (the reliability gradient) and a complete, traced
specification of what a correct estimate would require.** It does not yet have that estimate, and it
cannot have one until the section-5 implementation is run.

**For an NMI-level manuscript this is currently insufficient.** The reliability result alone is a
measurement about one atlas, with no demonstration that it changes a conclusion anyone has drawn. **The
route to sufficiency is now clear and bounded, but it is not yet travelled.**

**And the process record is itself part of the finding: seven self-found defects, two discarded numerical
results, four occasions on which a check rather than an artifact was wrong, and a root cause that was
available in the public code from the first round and was reached only by following the anomalies. Every
one of those is retained in the repository.**

## 7. Provenance

* `pumpprobe/Fconn.py` and `pumpprobe/Funatlas.py`, `github.com/leiferlab/pumpprobe`, fetched this
  session; all quotations carry line numbers.
* Stimulus duration, inclusion-criterion prose, and 113-animal count: Europe PMC full text of PMC10632145.
* Inter-stimulus interval: measured from all 113 `stim_volume_i` files.
* **No model was fitted. No biological claim is made.**
