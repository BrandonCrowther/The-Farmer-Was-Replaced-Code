# exp-072 — water threshold + direct move — result

**Outcome.** Both predictions confirmed almost exactly. Real,
attributable ~7.6% improvement over 071's baseline — the first
micro-optimization pass on the two-tile design, landing within 68
ticks of the #2-10 cluster's upper bound.

**Numbers.**

```
TOTAL_HARVESTS 900  ELAPSED_TICKS 831176  TICKS_PER_HARVEST 923.53
BREAKDOWN_PER_HARVEST  water 9.66  wait 1.00  harvest 200.00  reroll 484.85  move 201.00
SUM_CATEGORIES 806862  vs ELAPSED 831176  unaccounted 24314 (27.02/harvest, same as 071 -- consistent, not noise)
WATER_CALLS 16  per_harvest 0.018
REROLL_HIST [280,184,155,93,75,32,25,16,9,6,5,7,2,1,3,4,2,1,0,...]
```

| category | 071 (baseline) | 072 (optimized) | delta |
| --- | --- | --- | --- |
| water | 62.76 | 9.66 | **-53.10** |
| move | 226.00 | 201.00 | **-25.00** |
| reroll | 482.63 | 484.85 | +2.22 (noise) |
| harvest | 200.00 | 200.00 | 0 |
| wait | 1.00 | 1.00 | 0 (growth still fully hidden) |
| **total** | **999.41** | **923.53** | **-75.88 (-7.6%)** |

`WATER_CALLS` dropped from 248 to 16 (a 15.5x reduction) — matches the
prediction that a 0.75 threshold would be crossed far less often than
0.999, given water only decays ~1%/sec of its current value. `move`
landed at 201, one tick over the 200 theoretical floor for a bare
distance-1 hop — essentially exact. `wait` stayed at 1, confirming the
lower water threshold didn't push growth past the away-window; the
margin (518 ticks needed vs ~900 available) held.

**Baseline.** 071: 999.41 ticks/harvest.

**Verdict.** Both fixes worked exactly as measured, not guessed. `reroll`
(484.85, ~52% of the total) is now clearly the dominant remaining cost,
and it's already at its p=1/3 structural floor per 069 — not further
reducible without changing the type-space. `unaccounted` (27.02/harvest,
identical in both 071 and 072) is real, consistent instrumentation/
control-flow overhead from this test harness itself (the windowed-print
check, the accumulator bookkeeping) — a non-instrumented production
version of this design would likely shed most of it. Current total
(923.53) sits 67.5 ticks above the cluster's upper bound (856) and
144.53 above the two-tile design's own single-drone measurements'
optimistic end — close enough that the remaining gap is plausibly
closeable with the same kind of direct measurement, not more guessing.
No champion change yet — still a single-drone smoke test; the 32-drone
macro-layout question (fitting tile-pairs into the grid without
neighbor bush-wall conflicts) remains the real blocker before this can
become the actual champion.
