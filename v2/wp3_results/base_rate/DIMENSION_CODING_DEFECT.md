# The dimension-coding exercise was invalid, and the defect is recorded rather than repaired quietly

**A second coder, asked to code two papers' declared specification dimensions from a packet, opened its result by
refusing to let the table be used: the packet contained no Methods body.** **Checking that claim confirms it, and
checking further shows a second and worse defect in the same exercise.**

---

## Defect 1: the packet was truncated, and it truncated exactly the wrong part

**`DIMENSION_CODING_PACKET.md` was built by slicing each paper's stripped text at 40,000 characters.** **Both
journals place Methods AFTER the Results, so the slice contained the front matter and none of the Methods, and
every `(Materials and Methods)` pointer inside it was a dangling cross-reference.**

**The second coder measured it: each entry is exactly 40,001 characters and each stops mid-sentence inside a
figure legend.**

**So its U codes, and the ones this line had produced before it, largely record what the first 40,000 characters
of front matter say about the Methods, which is nothing.**

## Defect 2, which is worse: the two coders did not see the same input

**This line's dimension coding reported the mouse paper's global-mode dimension as D, on the sentence
"Neuropil contamination was corrected by subtracting the common time series (1st PC) of a spherical surrounding
mask of each neuron".**

**That sentence is NOT in the packet.** **It was found in a separate search this line ran against the raw XML
after building the packet.** **So coder 1 coded from material coder 2 never received, which makes the comparison
between them void and not merely noisy.**

**The verification, run against the two files:**

```
v1 packet contains 'neuropil': False
v1 packet contains 'Suite2p':   False
v1 packet contains 'dF/F':      False
```

## Defect 3: a protocol deviation this line made and did not record

**The protocol named three matrices: the Human Connectome Project, UK Biobank, and the larval zebrafish citing
work.** **This line substituted the mouse V1/HVA paper for the first two without amending the protocol.** **The
second coder noticed and said so.** **The substitution is defensible, since the mouse paper is same-kind and
open-access while HCP and UK Biobank are large-document cases, but a substitution made silently is a deviation,
and the protocol exists so that such choices are visible.**

## What happens next, and what does not

**A version-2 packet was built with the FULL text of each paper and a section index, 310,233 bytes against
version 1's 80,347.** **It contains each paper's Methods, and it is the input for any re-coding.**

**The following is NOT done and is not claimed:** **the two coders' tables are not compared, no agreement rate is
reported from them, and no dimension count from either is used anywhere in the manuscript.** **The dimension
counts currently in `DOCUMENTATION_INSPECTION_two_matrices.md` and `DOCUMENTATION_INSPECTION_zebrafish.md` rest
on this line's own reading of the full papers and are labelled there as ILLUSTRATIVE; that labelling now has a
concrete reason behind it.**

**And a re-coding would need a NEW second coder on the version-2 packet**, because the existing second coder's
result is void by defect 2 rather than merely superseded.

## What this defect is an instance of

**It is the same class as everything else in this corpus: a number was produced by a procedure that looked
right, and only an independent reader asking "what is actually in this file" showed that the procedure could not
produce what it claimed.** **The specific mechanism is new: a fixed-width slice was applied to text whose section
order put the relevant material beyond the slice.** **The generalisable rule is that a slice must be justified by
what it contains and not by its length, and that the FIRST check on any packet is a search for the sections it is
supposed to carry.**

**It is also the second time a second coder has caught this line: the base-rate coder was right on all three
disagreements, and this dimension coder was right before it produced a table at all.**

## Provenance

* **Found by:** the second dimension coder, in isolated context, as the first line of its report.
* **Confirmed by:** a search of the version-1 packet for three strings that the papers do contain.
* **Version-2 packet:** `DIMENSION_CODING_PACKET_v2.md`, 310,233 bytes, with Methods present.
* **No model was fitted. No measurement in the manuscript depends on the invalid table.**
