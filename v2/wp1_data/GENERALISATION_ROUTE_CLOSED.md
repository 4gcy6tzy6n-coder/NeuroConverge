# The DANDI generalisation route is closed for this environment, and the attempt's budget is accounted

**Status: a second dataset was pursued to test whether the line's reliability structure generalises, and the
fetch failed three times. The route is closed, the failure modes are recorded, and the extraction was written
and de-risked in advance so the analysis can be resumed if the data ever arrives by another means.** No model
was fitted.

**This is the twenty-first self-found defect, and the third consecutive round in which the fault was in this
line's own execution rather than in its reasoning.**

---

## 1. Why this route, and why it was thought closed before

**The line's central reliability measurement -- a pair's response agrees across animals at `r_full = 0.0405`
while agreeing within an animal at `0.5223` -- rests on ONE atlas from ONE laboratory.** **Round 26 recorded
the generalisation test as infeasible because DANDI `000541` totals 30.53 GB against a 10 GB Stage-2 cap.**

**Round 45 re-read that and found it was true of the WHOLE dataset and false of ENOUGH of it.** **Six sessions
cost about 8.7 GB, within the cap, and six animals suffice for the cross-animal half of the measurement.**
**The earlier conclusion was right about the whole and wrong about the part, and it had not been re-examined.**

## 2. What the dataset is, established before the fetch

**Reading the one session already downloaded, `sub-20190929-07`:**

| property | value |
| --- | --- |
| cells per session | **177**, NeuroPAL names shared across sessions |
| signal array | `(936, 177)`, `starting_time` 0.0 |
| **sampling interval** | **0.25 s (4 Hz)** |
| chemical stimuli per session | **3**, at 60.5, 120.5 and 180.5 s, each **10.0 s** |
| record length | 234.0 s |

**The 0.25 s interval was confirmed by two independent checks: it makes the record span the last stimulus
(234.0 s against 190.5 s), and it maximises the number of cells whose stimulus response exceeds three
pre-stimulus standard deviations, 57 cells against 21 for the next-best value and 2 to 8 for the others.**

**And the record drifts substantially: the all-cell median falls from 0.2611 in the first third to 0.1505 in
the last, and the spread of the cell-mean falls from 0.0647 to 0.0086.** **That makes a per-stimulus baseline
correction necessary rather than optional, and the extraction applies one.**

## 3. What the dataset could and could not have tested

**Three stimuli per session means NO within-animal split-half is possible.** **So this dataset could have
tested the cross-animal half of the reliability structure and not the within-animal half.**
**`r_full = 0.0405` was the quantity to compare against; `0.5223` was not reachable here, and the comparison
would have been reported with that half missing.**

## 4. The three failures

| attempt | method | outcome |
| --- | --- | --- |
| **1** | `curl --max-time 3600`, sequential | **5 of 5 truncated by mid-transfer disconnects; all five unreadable** -- `h5py` reports `truncated file: eof = 706987024` and refuses to open |
| **2** | `curl -C -` with retries in a loop | **stalled at 59, 59, 39, 0.4 and 0 per cent; zero complete files** |
| **3** | **concurrent resume** | **this line's own bug:** a manual resume test ran while the loop's `curl` still held its own byte offset, so the later write truncated the file back from 859,626,536 to 433,753,128 bytes |

**The third failure is the instructive one, and it is not a network problem.** **Two writers on one file,
each with a cached offset, produced a file shorter than either had reached.** **Checking whether a stalled
download is progressing by resuming it by hand is exactly the operation that corrupts it.**

## 5. The budget, accounted

```
already held before this route      0.675 GB   (the OSF atlas export and the connectome tables)
spent on this route                 1.866 GB   (truncated, unusable)
total                               2.541 GB   /  10 GB
remaining                           7.459 GB
```

**The 1.866 GB bought nothing.** **Whether it should have been spent is a fair question and the answer is not
obviously no: the attempt was justified by the generalisation question, and it failed on execution rather than
on planning.**

## 6. What is left in place so the route can be resumed

* **`d541_generalise.py`**, written and syntax-checked, which loads sessions, extracts a per-stimulus
  per-cell response with a 30 s pre-stimulus baseline, and reports the cross-session correlation matrix
  against the atlas's `0.0405`.
* **The extraction is verified against the one session available:** 177 of 177 cells produce non-zero
  responses of plausible magnitude, median -0.0120 and range -0.495 to +0.303 for the first stimulus.
* **`fetch_d541.sh`** with resume and retries, whose flaw is that it must not run while any other writer
  touches the same files.
* **The one complete session**, `nwb541.nwb` at 1.42 GB.

## 7. What this does to the line

**Nothing measured changes.** **What changes is that the generalisation question is now known to be blocked by
infrastructure rather than by budget, and the earlier "infeasible" verdict is corrected to "infeasible here,
and the reason is known".**

**And it removes the last item from the list of work this line can do by itself.**

## 8. Provenance

* Assets enumerated from the DANDI API; the URL prefix was wrong on the first attempt
  (`/api/dandi/dandisets/`) and correct on the second (`/api/dandisets/000541/versions/draft/assets/...`),
  which was established by probing three prefixes and reading the HTTP codes.
* Attempt records: `/tmp/osf/d541_attempt.json`, `/tmp/osf/d541_attempt2.json`, `/tmp/osf/d541_closed.json`.
* **No model was fitted. No causal claim is made.**
