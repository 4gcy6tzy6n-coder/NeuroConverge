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
