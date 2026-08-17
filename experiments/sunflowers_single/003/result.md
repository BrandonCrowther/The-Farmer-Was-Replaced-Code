# exp-003 — finish-and-score (reroll-to-15, 10-tile round robin) — result

**Outcome.** adopted — sunflowers_single's first-ever leaderboard entry.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 20:53.149, PB 20:53.149, Global Rank #300 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 6 internal samples, `TICK_FINAL` 7,508,147–7,650,580 (avg 7,569,027), `POWER` 10,001.6–10,005.3 | all 6/6 crossed target cleanly, no bugs |

**Baseline.** 002's projection: ≈909s (≈15.2 min) at ≈7.97 net
Power/harvest, 4,399.1 ticks/harvest (30-cycle sample).
**Variant.** 20:53.149 (1253.15s) real average. **Delta.** **+37.8%
above the 002 projection** — the 30-cycle probe's `AVG_REROLLS` 6.17
undersampled the true average (target=15 is drawn with p=1/9, a
geometric distribution with a long right tail; 30 samples isn't enough
to catch the true mean of 9, so the real ~1,255-harvest run pulled in
more of that tail). Not a bug — a known risk of small-sample probes for
a heavy-tailed cost, flagged here rather than re-litigated.

**Noise floor.** The 6 internal repeats' own spread (7.5M-7.65M ticks,
~1.9%) is tight — the real driver's variance is small run-to-run despite
the underlying per-tile reroll geometric variance averaging out over
~1,255 harvests.

**Screenshots.** `logs/captures/20260817-020648-exp-sunflowers_single-003-r1.png`

**Verdict.** The reroll-to-15 + 10-tile round-robin paradigm works
end-to-end for a real score. Adopting `saves/sunflowers_single/main.py`
as champion. The reroll cost's heavy tail (geometric, p=1/9, true mean 9
not 6.17) is the clearest lever for a follow-up: a `REROLL_LIMIT` cap
with a fallback to accepting a slightly-lower-but-still-safe petal
value (or a dynamic "match the current farm-wide max" target instead of
the fixed ceiling of 15) would cut the long right tail's cost without
losing correctness.
