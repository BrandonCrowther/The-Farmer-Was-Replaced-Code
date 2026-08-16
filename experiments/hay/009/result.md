# exp-009 — measure-idle-ticks — result

**Outcome.** diagnostic — the idle-time hypothesis is dead, and the real cost
structure is now known

**What was measured.** `get_tick_count()` (0 ticks) around the busy-wait and the
whole pass, for the first 25 passes of the drone at (3,3).

**The wait is 3 ticks. Every single pass.**

| | ticks |
| --- | --- |
| cumulative wait over 25 passes | 75 |
| cumulative total over 25 passes | 36,764 |
| **share of ticks spent idle** | **0.2%** |

exp-007's 94.1% was never evidence of a growth bottleneck, and exp-008 spent a
run finding that out the expensive way. Frequency of arriving early is not
duration spent waiting.

**Where the time actually goes.** Per-pass work clusters at 867 / 1284 / 1700 /
2628 ticks — quantised ~416 apart. The cost table explains it: **a successful
operating function costs 200 ticks** (`move()`, `harvest()`, `plant()`), while a
*failed* one costs 1.

A champion pass is therefore roughly:

| step | moves/ops | ticks |
| --- | --- | --- |
| walk to companion tile | ~2 moves | ~400 |
| harvest the companion | 1 | 200 |
| plant the companion | 1 | 200 |
| walk back | ~2 moves | ~400 |
| harvest our grass | 1 | 200 |
| **total** | | **~1,400** |

**The lever this exposes.** The companion is a Bush or a Tree, so **harvesting it
yields wood, not hay** — it contributes nothing whatsoever to the 2e9 hay target.
Yet it costs 200 ticks, and by emptying the tile it forces a 200-tick replant on
the next visit. When the companion tile already holds the plant it is supposed to
hold, both operations are pure waste: ~400 of ~1,400 ticks per pass.

Note also that the 944 water and 1000 carrot warnings cost **1 tick each**, not
200, because failed fallible operations are cheap. They are noise in the tick
budget, not a target — which retires 008's and 009's original rationale for
good.

**Next.** 010: skip the companion harvest-and-replant when the tile already holds
the right plant. Expected ~29% off the per-pass tick cost with the multiplier
fully preserved.
