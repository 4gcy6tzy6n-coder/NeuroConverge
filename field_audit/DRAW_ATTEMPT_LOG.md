# Draw attempt log

Every attempt at the corpus draw, with its outcome. A route failure is an instrument fact, recorded, not
evidence of absence (the precedent is MICA `69_` section 52, where two zero-result queries were recorded as
instrument defects).

## Attempt 1 - 2026-10-18 - BLOCKED (external quota)

`python3 draw_corpus.py --query` could not fetch: the OpenAlex free shared-IP daily budget is exhausted.

Exact error body (first line, both to the bare endpoint and the polite-pool retry):

    {"error":"Rate limit exceeded","message":"Insufficient budget. This request has no API key, so it counts
    against the free daily budget shared by everyone on your network's IP address, and that budget is used up
    ($0.0003 remaining; resets at midnight UTC). Use your own key instead: add ?api_key=YOUR_KEY..."}

Disposition: re-attempt after 00:00 UTC, or earlier with an owner-supplied API key (the key's existence and
holder would be recorded here; the key itself never enters the repository). No candidate list exists yet, the
corpus is NOT frozen, and the frozen protocol's 8-week clock has not started. No corpus was improvised from
web-search snippets: the frozen rule requires a scriptable, hash-pinnable snapshot.
