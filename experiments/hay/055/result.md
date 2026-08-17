# exp-055 — tight packing + distance-biased reroll, combined — result

**Outcome.** rejected — the combination is worse than either
component alone.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `HITS_SKIP` 44/150 (29.3%), `HITS_WALK` 106/150 | lower than 047's 36.7% baseline, and lower than 051's spacing-4-alone 32% |
| r1 | `TICKS_PER_HARVEST` 2,605.73 | worse than 051 (2,347.27) and 054 (2,087.08) individually |

**Baseline.** 047: 1,390 (neither). 051: spacing 4 alone, 2,347.27.
054: distance-reroll alone, 2,087.08.

**Variant.** Both combined. **Delta.** Worse than either component in
isolation — the two negatives compounded rather than cancelling.

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** The user's hypothesis (tighter packing creates a richer
shared "garden," and biasing draws toward the near/shared zone should
increase the odds of landing on it) is a reasonable mechanism, but
doesn't survive contact with the two component failure modes it's
built from: tight packing's thrashing problem and distance-reroll's
unfavorable cost math both still apply, and combining them adds their
downsides rather than letting either's upside dominate. Closes the
tight-packing-plus-distance-bias family with a real, direct test
rather than leaving it as an untried "what if."
