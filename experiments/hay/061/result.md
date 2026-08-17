# exp-061 — accept cheap draws only late in the reroll sequence — result

**Outcome.** rejected — worse than 057, worse than 060's tie. Closes
the distance-aware accept-policy family for real.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 02:49.099, PB stays 02:42.421 (#111, unchanged) | modal, `VERDICT=scored` |

**Baseline.** 057: memory-only, 02:42.421 (champion). 060: every-
attempt hybrid, 02:42.439 (tied 057).

**Variant.** Late-only hybrid (memory-hit always OR
`rerolls>=REROLL_LIMIT-2` AND distance<=2`). **Delta.** +4.1% vs 057,
worse than both prior variants.

**Noise floor.** Single real run — but this is the third distinct
policy variant to land at-or-below 057 in a row (053/054/055 also all
regressed), a consistent enough pattern not to be noise.

**Screenshots.** `logs/captures/20260817-110447-exp-hay-061-r1.png`

**Verdict.** The "only accept late" refinement didn't fix 060's
opportunity-cost problem — it made it *worse*: widening the accept
distance to `<=2` for the sake of catching something before the
budget runs out means giving up 1-2 remaining free-hit chances (each
still ~1/3 likely) for a *guaranteed* payment that's sometimes the
more expensive distance-2 case, not just distance-1. Four variants now
(058 higher limit, 059 lower limit, 060 every-attempt hybrid, 061
late-only hybrid) have all tied or lost to 057's simple "reroll toward
any memory match, `REROLL_LIMIT=5`, unconditional fallback walk"
design. That's a strong, consistent signal that 057 sits at or very
near the true local optimum for this whole paradigm — not adopting
further variants of this idea without a genuinely different mechanism
in hand. Champion stays 057 (02:42.421, #111).
