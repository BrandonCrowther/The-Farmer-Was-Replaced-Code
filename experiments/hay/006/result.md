# exp-006 — reroll-companion — result

**Outcome.** rejected — the mechanic works, the trade does not

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:41.013** | +0.102 s vs champion — inside the noise floor |

**Baseline.** 03:40.911 · **Variant.** 03:41.013 · **Delta.** +0.102 s (0.05%)

**Noise floor.** 0.15 s. The delta is *smaller* than the floor, so the honest
reading is **no effect**, with no evidence it helps and none that it hurts.

**Warning histogram.**

| warning | 005 | 006 |
| --- | --- | --- |
| Didn't have the required items to plant `Entities.Carrot` | 997 | **267** |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 9 | **183** |
| Tried to use `Items.Water` but didn't have enough of it | 936 | 953 |

**Verdict.** The reroll does exactly what it was supposed to — unaffordable
carrot requests fell 73% — and it bought nothing. Each reroll costs a harvest
plus a plant, and that cost cancels the multiplier it wins. Rejected on the
number, but this is a finding rather than a dead end: it prices the mechanic.

**The tripwire cleared.** 005 tied 004 to the millisecond and this run did not,
so the score does respond to code changes and that coincidence was just a
coincidence.

**Two things this exposes for later.**

1. **"Cannot plant Carrot on Grassland" jumped 9 -> 183.** Same root cause as
   003: `till()` will not convert ground a plant is standing on, and the
   companion callback tills before it plants. Once carrot becomes affordable
   mid-run, every attempt on an occupied tile fails. A companion callback that
   harvests before tilling would fix this everywhere, and it is cheap. Queued
   as 009.
2. **Whether our own tile is even replanted between iterations is unverified.**
   The driver plants grass once before the loop and harvests at the end of every
   iteration; nothing obviously replants it. If the tile is empty at the top of
   the next iteration then `get_companion()` returns None, the reroll is a no-op
   after the first pass, and this experiment measured far less than it looks
   like it did. That is a question about the farm's actual state, and
   `quick_print` costs 0 ticks — queued as 010, a diagnostic run rather than an
   optimisation.
