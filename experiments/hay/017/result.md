# exp-017 — water-threshold — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:04.715** | PB; rank #177 |

**Baseline.** 03:05.323 · **Variant.** 03:04.715 · **Delta.** **−0.608 s (−0.33%)**

**Noise floor.** 0.15 s. The win is 4x the floor, over the 2x bar.

**Warning histogram.** `Tried to use Items.Water` fell **1042 -> 120**, so the
spinning is real and is now mostly gone.

**Verdict.** Correct as far as it goes: the loop was burning ticks on a condition
it could not satisfy, and gating on tank count fixes that. The win is smaller
than the ~200 ticks a pass that 009's accounting suggested, which is worth being
honest about — either the spinning cost less than that, or the extra `num_items`
call per iteration eats into it, or watering less lowers growth enough to give
some back. **This experiment cannot distinguish those**, because it never
measured water levels or growth.

The residual 120 warnings are the race: `num_items` sees a tank, another drone
spends it first.

**Standing caveat.** The starvation figure motivating this change is arithmetic
on wiki constants, not measurement — exp-019 samples `get_water()` and
`num_items(Items.Water)` directly.

---

**CORRECTION WITHDRAWN (exp-028).** The correction above was itself wrong. It
computed a 2.41 s floor by pooling clean champion runs with *instrumented* ones —
comparing different code, which is the error it was written to correct.

Four clean champion runs measure **sd 0.069 s, range 0.148 s**. The 0.15 s floor
this result was originally judged against was correct, and this delta stands.

What survives from the correction is different and more important: runs made deep
into the memory leak score very differently on identical code (exp-023 at 67 sd,
exp-026 at 15 sd from the clean mean). **Comparisons are only valid between runs
made under similar game conditions** — see `record.json`.
