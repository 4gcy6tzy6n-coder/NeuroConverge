# Verification tooling for the v2 line

## Why this exists

Across rounds 2 to 6 of this line, **five verification checks failed and all five were the checks, not
the artifacts.** The tally, recorded so the pattern is not forgotten:

| round | check that failed | actual cause |
| --- | --- | --- |
| 2 | "no v1 path was modified" | tested whether a path was *dirty*, which flags another lane's in-flight edits; the correct test is whether the **last commit** touching it is this lane's |
| 2 | emoji scan | searched the wrong scope |
| 3 | "both retraction notices are at the end" | the Markdown bold marker `**` sits after the final period |
| 4 | "the earlier `d` values are marked not-as-estimates" | the document says "should not", the pointer says "must not"; the check searched one file for the other's wording |
| 6 | "pairs are still not independent" and "the earlier text is unaltered" | **no whitespace normalisation**, so phrases broken by a line wrap never matched |

**Five failures, five self-inflicted.** Each was individually fixed at the time, which is exactly the
wrong response: the same class of error recurred four times because the fix was always local.

## `check_artifacts.py`

One reusable checker that removes all four failure modes by construction.

* **Whitespace is normalised on both sides**, so a phrase broken across lines matches.
* **Every requirement names its own file**, or `ALL` to search every text artifact — so a sentence can
  no longer be hunted for in the wrong document.
* **Alternatives are a list** (`a | b | c`), so intent is testable without demanding one particular
  phrasing.
* **On failure it prints what it searched, how large that was, and the nearest fragment it could find**,
  so a failure is diagnosable instead of merely red.

Exit code is the number of failed requirements, so it can gate a commit.

### Use

```
python3 check_artifacts.py <<'SPEC'
# FILE :: label :: alternative1 | alternative2
ALL :: the animal is the unit :: Unit: the animal | the unit is the animal
wp3_results/ANIMAL_LEVEL_ESTIMATE.md :: d = 0.7289 :: 0.7289
SPEC
```

A deliberately failing requirement, used once as a self-test:

```
FAIL  无未替换占位符
        searched : ALL (51 files)  (334964 chars)
        wanted   : one of ['TODO', 'FIXME', 'XXX-HACK']
        nearest  : ...(no word from the requirement found at all)...
```

**That run also established something real: there are no `TODO`, `FIXME` or placeholder markers anywhere
in the 51 text artifacts of this line, across 334,964 characters.**

## The lesson worth keeping

**The numbers in this line have held up under re-examination; the interpretations attached to them have
not.** Two rounds retracted a previous round's reading, and neither retraction touched a measurement.
Adding a third pattern: **the verification has been less reliable than the work it verifies.** Both
observations point the same way — the failure-prone step is the human-and-agent judgement layer, not the
computation, and that layer is where tooling pays for itself.

## Two defects found in the checker itself, during its first use

Recorded because they are the same class of error the checker exists to catch.

**1. No absence semantics.** The first version passed when a needle was *found*, so a requirement like
"there are no emoji" could not be expressed at all. Fixed with a `!` label prefix.

**2. A substring test cannot tell a placeholder from a sentence about placeholders.** Searching for
`TODO` matched `tools/README.md`'s own prose, *"there are no TODO, FIXME or placeholder markers"*.
**This is precisely this project's known "guard satisfied by a substring" defect class**, and it is
recorded here as a fresh instance rather than as a hypothetical. Fixed by adding a `re:` needle form so a
requirement can be context-aware; the working pattern is

```
ALL :: ! 无真的占位符 :: re:^\s*(#|//|--)?\s*(TODO|FIXME|XXX-HACK)\b
```

which matches a marker at the start of a line or comment and **does not** match prose. Verified both ways:
it fires on `# TODO: fix this later` and stays silent on the sentence above.

**3. The alternative separator collided with regex alternation.** The first regex-capable version split
alternatives on `|`, which every regex also uses, so a pattern containing `(#|//|--)` was shredded into
three literal needles. **Fixed by moving the separator to `;;`.** A checker whose own input format cannot
express the requirement is worse than no checker, because it reports a red result that means nothing.

## A fourth requirement form: `num:`

**Round 7 added `num:<value>` for numeric matching with 5e-4 relative tolerance.** The reason is a fresh
instance of the same class: a check searched the JSON for `0.4495` and failed, because the JSON stores
`0.4494511406066225` and a rounded figure is **not a substring** of its full-precision value. **The two
represent the same fact**, so the check was wrong and the artifact was right -- the sixth self-inflicted
check failure in this line, and the first one the checker's own diagnostic output made obvious in
seconds rather than minutes.

The four requirement forms now are:

| form | meaning |
| --- | --- |
| `text` | literal substring, whitespace-normalised |
| `re:<pattern>` | multiline regular expression, for context-aware requirements |
| `num:<value>` | numeric match with tolerance, so a rounded quote matches its full-precision source |
| `!`-prefixed label | the requirement is **absence**, not presence |

Alternatives are separated by `;;`, because `|` is needed inside regexes.

## What the tool has already earned

* It fixed a defect class that recurred in **five consecutive rounds**.
* Its **first full run** established a real fact: no `TODO`, `FIXME`, emoji or silent control characters
  anywhere in the line's 51 text artifacts, across 337,955 characters.
* **Its diagnostic output turned a mystery into a two-second diagnosis twice in one round** -- once when
  a path was written `v2/tools/...` inside the `v2/` root, and once when a rounded number was searched
  for in a full-precision JSON.

## Two more masking characters, both found the moment a document quoted sources heavily

**Round 18's survey quotes verbatim, and two Markdown constructs sit *inside* the quoted sentences.**

**1. Emphasis markers.** A requirement for the phrase `not a systematic sample` failed against
`**not** a systematic sample`. **`strip_md` now removes `**bold**`, `*italic*`, `__bold__` and `` `code` ``
before matching.**

**2. Blockquote continuation markers.** A sentence spanning two quoted lines is

```
> ... and which it
> cannot, is unknown.
```

which normalises to `... and which it > cannot, is unknown.`, so a requirement for `which it cannot` fails.
**Leading `>` markers of blockquote lines are now stripped too.**

**Both were latent from the first version and neither had been triggered**, because earlier documents
bolded at the edges of sentences rather than inside a searched phrase, and quoted at most one line at a
time. **A checker is only as good as the documents it has been pointed at.**

### The requirement forms, complete

| form | meaning |
| --- | --- |
| `text` | literal substring, case-insensitive, whitespace-normalised, Markdown-stripped |
| `re:<pattern>` | multiline regular expression, for context-aware requirements |
| `num:<value>` | numeric match with relative tolerance, percentage and fraction interchangeable |
| `!`-prefixed label | the requirement is **absence**, not presence |
| `;;` | separates alternatives, because `|` is needed inside regexes |

### The tally

**Thirteen self-inflicted check failures across rounds 2 to 18, every one the check's and not an artifact's
-- with one exception, round 14, where the checker caught a genuine document-versus-JSON contradiction
that its author had introduced.** Each of the thirteen narrowed the checker; the one real catch is why it
is worth the trouble.

## A requirement form this corpus needs: the `d` in a result file is not always an effect size

**Rounds 27 and 28 established that `d` in this corpus means four different things.** **The census in
`../wp3_results/CENSUS_d_z_versus_d_effect.md` found seventy-six fields across five result files that store
`diff / SE`, a z-score, under that name.** **A document quoting such a value as an effect size overstates the
effect by `sqrt(n)`, which here is hundreds.**

**So a requirement about an effect size must name the quantity, and there is an arithmetic check that a
requirement can encode:**

```
wp3_results/SOME_DOC.md  :: effect size is not a z  :: ! re:num:([2-9]|[1-9][0-9])   <- not usable as written
```

**The usable form is a plain bound on the value, because the largest genuine effect size anywhere in this
corpus is 0.7690:**

```
wp3_results/SOME_DOC.md  :: any d above 1.5 must be labelled a z-score :: z-score
```

**The heuristic, stated so it can be tested: a `d` of 2 or more in this corpus is a z-score.** **The tooling
cannot enforce that by itself, because it does not know which quantity a number denotes; what it can do is
require that the distinction be stated, which is what the requirement above does.**

## A fourth way a check can be wrong: a notice about a broken citation looks like a broken citation

**Round 49 ran a citation scan across the corpus and found ten broken links.** **Four were in
`PATH_LAYOUT.md`, which cited `05_common_mode.py`, `08_animal_level.py`, `11_source_rule.py` and
`13_measurement_structure.py`; the same round that created that document had renamed them to
`06_common_mode.py`, `09_animal_level.py`, `11b_source_rule.py` and `13_within_vs_between_splithalf.py`.**
**The body was corrected and a dated notice was appended that NAMES the four wrong names, as a notice must.**

**The scan then flagged the document again, because the notice names them.** **That is a false positive of the
same family as round 10's, where a guard was satisfied by prose ABOUT a placeholder: a check that searches
text cannot distinguish an assertion from a statement about the assertion.**

**The practical rule: a citation scan must be run against a document WITHOUT its appended notices, or the scan
must report a name found only inside a notice as informational rather than broken.** **Neither is implemented
here; this records the limitation.**

**And the round-49 scan's real yield, which is why it was worth running:** **one artifact from round 41 had
never been committed at all** — `39_joint_grid_verified.py` and `RESULT_joint_grid_verified.json`, cited by
`JOINT_GRID_VERIFIED_NONADDITIVE.md` and by the manuscript's figure legends, and present only in a temporary
directory. **A document that cites an artifact is not evidence that the artifact exists.**
