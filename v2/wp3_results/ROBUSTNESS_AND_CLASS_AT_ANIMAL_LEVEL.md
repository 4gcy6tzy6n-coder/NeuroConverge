# Robustness and the class control at the animal level, and a retraction of this line's own caveat

**Status: the animal-level estimate survives weighting, the class structure is now resolved at the correct
unit, and one self-criticism from the previous round is withdrawn.** No model was fitted.

---

## 1. The estimate is robust to precision weighting

The previous document reported a paired `t` at the animal level and cautioned that the `p` was
"optimistic" because connected and unconnected pairs within an animal share events and indicator state.
**That caution is withdrawn: it was reasoning, not measurement, and the measurement contradicts it.**

Each animal's contrast was re-computed weighting by its pair counts, which is a precision proxy:

| contrast | animals | difference | `d` | unweighted `t` | **weighted `t`** |
| --- | --- | --- | --- | --- | --- |
| connected vs unconnected | 109 | +0.07702 | 0.7289 | 7.610 | **7.829** |
| chemical vs unconnected | 108 | +0.04753 | 0.4145 | 4.307 | 3.780 |
| gap junction vs unconnected | 109 | +0.12856 | 0.7690 | 8.028 | **10.008** |

**The weighted and unweighted statistics agree closely, and the weighting moves the gap-junction
statistic further from the null, not toward it.** So the animal-level paired test **does** account for the
dependence that matters -- pairs sharing an event enter the same animal's mean and cancel in the paired
difference -- and the reported `p` is not inflated by the mechanism the previous document worried about.

**A second check on the same concern:** the correlation between an animal's paired difference and its
number of connected pairs is **-0.124**, so there is no systematic relationship between how many pairs an
animal contributes and the size of its contrast.

> **Where the caution was right and remains:** the pairs are not independent replicates, and **any analysis
> that treats them as such is inflated by the factor measured in the previous document, 11 to 18 times.**
> **The caution applies to the wrong unit, not to this one.** The previous document attached it to the
> right unit, which was an error of placement, and it is corrected here.

## 2. The class control at the animal level

The earlier class result was computed at the pair level and was therefore inflated in the same way as
everything else. Re-run with the animal as the unit:

| contrast | animals | difference | `d` | `t` | weighted `t` |
| --- | --- | --- | --- | --- | --- |
| **same-class**: connected vs unconnected | 102 | +0.04790 | **0.1126** | **1.137** | 1.321 |
| **cross-class**: connected vs unconnected | 109 | +0.04903 | **0.4539** | **4.739** | 5.148 |
| same-class connected vs cross-class connected | 108 | +0.22347 | 0.6489 | 6.744 | 9.066 |

**Reading, and it is a clean structural result:**

* **Within same-class pairs the connectivity association is not distinguishable from zero** (`d = 0.113`,
  `t = 1.14`).
* **Across classes it is clear** (`d = 0.454`, `t = 4.74`).
* **And same-class connected pairs nonetheless respond strongly** -- 0.223 higher than cross-class
  connected pairs, `t = 6.74` -- **but so do same-class unconnected pairs, which is why the contrast
  inside the stratum vanishes.**

**Interpretation, stated as an interpretation.** Same-class partners -- bilateral homologues and similar
-- co-respond whether or not they are connected, so a within-stratum contrast cannot see the wiring.
**The connectivity-specific component appears only across classes.** This is the animal-level version of
what the pair-level analysis suggested in the negative direction, and **it is the version to keep.**

**What this does NOT explain:** why same-class partners co-respond. Shared identity, shared input, shared
position and shared physiology are all candidates and **none was tested.**

## 3. Where the line now stands

**Two solid results, both at the animal level, both robust to weighting:**

1. **Anatomically connected pairs show a higher functional response, `d = 0.729` across 109 animals,
   with gap junctions larger (`d = 0.769`) than chemical synapses (`d = 0.415`).**
2. **The association is confined to cross-class pairs; within same-class pairs it is null.**

**And one measurement about the artifact, from the previous document and unaffected by this one:**
**treating pair-measurements as the unit inflates the same contrast by 11 to 18 times.**

**Still owed, unchanged and ordered:**

1. **Re-run both results with the source's actual inclusion rule**, which is the only way either number
   becomes comparable to the published atlas. **This remains the blocking item.**
2. **Establish why same-class pairs co-respond**, since the structural result in section 2 currently rests
   on an untested mechanism.
3. **Then** the reliability-weighted version, if it is still worth doing.

## 4. The retraction ledger for this line

**This is the second time a round has retracted something from a previous round, and both are recorded.**

| round | what was retracted | why |
| --- | --- | --- |
| 3 | the round-2 claim that the association is carried by gap junctions rather than chemical synapses | the effect is window-dependent -- **itself corrected in round 3's own part 3, because the 4 s window turned out to be the correct one** |
| **6** | **the round-5 caution that the animal-level `p` is optimistic** | **measured: weighted and unweighted `t` agree closely** |

**Both retractions were of this line's own reasoning rather than of its measurements**, which is the
pattern worth noting: **the numbers have held up under re-examination; the interpretations attached to
them have not.**

## 5. Provenance

* Script `anatomy/10_robust_and_class.py`; output `anatomy/RESULT_robust_class.json`.
* Inputs and checksums as in `ANIMAL_LEVEL_ESTIMATE.md` section 7.
* **No model was fitted. The associations are observational and cross-individual; no causal claim is
  made.**
