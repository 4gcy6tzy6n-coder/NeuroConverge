# The window question is answered: 500 ms stimulus, 4 s criterion, and why longer windows inflate

**Status: the window dependence of round 2 is EXPLAINED, and the correct window is determined from the
source protocol rather than chosen from the data.** This refines -- and in one respect corrects -- the
round-2 retraction. No model was fitted.

---

## 1. The two facts that settle it, read from the source Methods

**Fact 1 -- the stimulus is short.**

> *"a **500-ms** (300-ms for the `unc-31`-mutant strain) train of light pulses was used to optogenetically
> stimulate that neuron"*

**Fact 2 -- the source's own analysis window is 4 seconds, and it is an inclusion criterion.**

> *"Stimulation events that did not meet both thresholds for a **contiguous 4 s** were excluded."*

**Fact 3 -- the protocol spacing**, measured this session from `stim_volume_i` across all 113 animals:
**median inter-stimulus interval 62 volumes = 31.0 s** (p5 30.5 s, p95 37.5 s), **and 0 % of events have
the next stimulus within 24 volumes (12 s).**

## 2. What the measured time course then means

Measured post-stimulus trajectory, 112 animals, 3,380 events, normalised by the event's across-cell SD:

| post-stimulus | connected | unconnected | chemical | gap junction |
| --- | --- | --- | --- | --- |
| 0.5 s | +0.061 | +0.038 | +0.052 | +0.078 |
| 4.0 s | +0.119 | +0.056 | +0.090 | +0.180 |
| **10.0 s** | **+0.232 (peak)** | +0.105 | +0.164 | **+0.352 (peak)** |
| 24.0 s | +0.225 | +0.100 | +0.160 | +0.349 |

**The response peaks at 10 seconds -- twenty times the 500 ms stimulus -- and is still near its peak at
24 seconds.**

> **A 10-second rise is not a synaptic or gap-junction response.** GCaMP6s rises in roughly 100 ms and
> decays in roughly 0.5-1 s; the stimulus lasted 500 ms. **Whatever the 10-second component is, it is
> not the event the atlas is named for.**

**And the round-2 window dependence is now explained rather than mysterious.** With a 31-second stimulus
spacing and a component whose decay extends past 20 seconds, **the pre-stimulus baseline of 8 volumes
(4 s) sits inside the tail of the previous event.** A longer post-stimulus window accumulates more of
that slow component, **which is exactly the component the source excludes by requiring a contiguous 4 s
response.** Hence chemical `d` rising from 1.154 at 1 s to 3.118 at 16 s: **not a chemical relay
revealing itself, but a slow component accumulating.**

## 3. What this corrects in round 2

**Round 2 retracted the claim that the association is carried by gap junctions rather than chemical
synapses, on the grounds that the effect is window-dependent.** That retraction was **too strong**, and
this document corrects the correction:

* **The 4-second window originally used was the defensible one all along**, because it matches both the
  500 ms stimulus and the source's own stated criterion. **The round-2 retraction treated the window as
  an arbitrary choice; it was not arbitrary, and the number the retraction withdrew was computed at the
  right window.**
* **The window dependence is nevertheless real and is the finding.** An analyst who chose 16 seconds --
  32 times the stimulus duration -- with no stated reason would inflate the chemical association by a
  factor of 2.70 **and would have no way to know it.**
* **What does NOT change:** the effect remains stronger for gap junctions than chemical synapses at every
  window, and the ordering is stable even though the magnitudes are not.

**The process error, recorded because it is the same class as the five already in this line's ledger:
the stimulation duration was available in the source text from the start and was not checked before
declaring the window arbitrary. Reporting a sensitivity to an unreported choice, without first
establishing which choice the source made, produced a retraction of a correct number.**

## 4. The common-mode correction, which stands and matters

Computed this session with a stable normalisation (the event's across-cell SD, not a per-cell
pre-stimulus SD -- an earlier attempt divided by near-zero and produced values of order 1e11, which is
the sixth self-found defect in this line).

Removing the across-cell mean at each timepoint, which is the global common mode:

| at 10.5 s | raw | common-mode removed | reduction |
| --- | --- | --- | --- |
| connected | +0.2267 | +0.1337 | 1.7x |
| **unconnected** | +0.1055 | **+0.0118** | **8.9x** |
| chemical | +0.1640 | +0.0776 | 2.1x |
| gap junction | +0.3473 | +0.2454 | 1.4x |

**Eighty-nine per cent of the unconnected "response" is common-mode drift, but only 41 % of the
connected response is.** The connectivity contrast sharpens from 2.1x to 11.3x.

**So the connectivity effect is a genuine cell-specific component, not global drift** -- and the
common-mode correction is a real improvement in the read-out that should be applied in every subsequent
contrast. **It does not by itself remove the slow component**, which is why the window still has to be
fixed by the protocol.

## 5. Where this leaves the finding

**The defensible statement, using the source's own window and the common-mode-corrected read-out:**

> **In this atlas, the association between anatomical connectivity and functional response is real and
> cell-specific, is stronger for gap junctions than chemical synapses, and is confined to cross-class
> pairs. Its measured magnitude depends by a factor of 2.70 to 5.57 on the post-stimulus window, and the
> defensible window -- 4 seconds -- is fixed by a 500 ms stimulus and the source's own inclusion rule.
> The published atlas reports per-pair response values without documenting that window.**

**The evidential transition that requires separate support, stated precisely:** *from a published per-pair
response magnitude to an inference about connectivity-function correspondence.* **The magnitude is a
function of a window the atlas does not report, and of a baseline that sits inside the previous event's
tail under a 31-second protocol.**

**Still not claimed:** that the source is wrong. **It reports its window and applies an inclusion rule --
this audit's difficulty is that the published derived matrix does not carry either, and downstream users
of that matrix do not inherit them.**

## 6. Revised next steps

1. **Re-run every contrast at the 4-second window with the common-mode correction**, since both are now
   justified rather than chosen. **This is the estimate to report.**
2. **Implement an inclusion rule equivalent to the source's contiguous-4-second criterion**, so that the
   comparison is against the events the source would retain.
3. **Re-run the class control at the 4-second window** with the common-mode read-out.
4. **Add a tail-aware baseline**: with 31-second spacing, the pre-stimulus window should be checked for
   contamination by the previous event rather than assumed clean.

## 7. Provenance

* Source protocol and inclusion criterion: `randi.xml`, Europe PMC full text of PMC10632145, quoted
  verbatim above.
* Time course and common-mode scripts: `anatomy/04_timecourse.py`, `anatomy/06_common_mode.py`.
* Inter-stimulus intervals: measured from all 113 `{i}_stim_volume_i.txt`.
* **No model was fitted. No biological claim beyond the measured contrasts is made.**
---

> **SPECIFICATION MISMATCH NOTICE, appended 2026-10-09.** Every `d` value in this document was computed
> under a specification that differs from the source's in at least five respects -- window, amplitude
> reference, contiguous-run requirement, derivative criterion and tail handling. The source's actual rule
> is recovered in [`SOURCE_RULE_RECOVERED.md`](SOURCE_RULE_RECOVERED.md). **These numbers are therefore not
> estimates of the paper's quantity and must not be read as such.** The text is left unaltered so the
> mismatch remains auditable.
