# exp-004 — finish-and-score (8x8 grid sort + single cascade) — result

**Outcome.** adopted — first-ever score, worked on the first real
attempt, no bugs.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 00:54.267, PB 00:54.267, Global Rank #350 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 133 internal `TICK_FINAL` samples, min 247,206 / avg 329,568 / max 381,526 | **every single repeat harvested exactly 131,072/131,072** — 100% reliability, single-cascade design never partially failed |

**Baseline.** None — first score for this category.
**Variant.** 00:54.267 (54.267s). Real average total ticks ≈329,568 —
close to 003's naive-worst-case extrapolation (≈430,000) despite the
early-exit optimization, suggesting the sort passes rarely exit
early on truly random size data (10 values spread over 64 cells means
most passes still find at least one out-of-order adjacent pair until
the array is nearly fully sorted).

**Noise floor.** The 133 internal repeats' own spread (247k-382k
ticks, ~54%) is real variance from the random per-cactus sizes
affecting how many bubble-sort swaps are needed each run, not
measurement noise.

**Screenshots.** `logs/captures/20260817-014637-exp-cactus_single-004-r1.png`

**Verdict.** The `32 * n**2` yield formula and the row-then-column
adjacent-swap sort lemma both hold exactly at full 8x8 scale, completing
Cactus_Single in a single cascade harvest as 002's formula match
predicted. Adopting `saves/cactus_single/main.py` as champion. **The
leader (`□萌萌的新□`) scores 00:07.447 — 7.3x faster** — a real, large
gap. The sort is very likely the dominant cost (≈290k of the ≈330k
average ticks, vs ≈38k for setup) and is the clearest target for further
optimization: the current bubble sort makes no use of the fact that
there are only 10 possible size values across 64 cells (heavy
duplication), doesn't parallelize row and column work, and re-walks the
full row/column on every pass even when most of it is already settled.
A counting-sort-style or partial-selection-sort approach exploiting the
small value range, or a smarter bound on how many passes are truly
needed, is the next thing to try.
