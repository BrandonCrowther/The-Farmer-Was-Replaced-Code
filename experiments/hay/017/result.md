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

**CORRECTION (exp-027, 2026-08-16).** This result was adopted against a noise
floor of 0.15 s taken from exp-002 — measured on the 4:55 seed, 25 experiments
earlier. The floor at champion speed is **2.41 s (1 sd)**, from three
champion-equivalent runs scoring 02:47.682, 02:51.263 and 02:52.271.

This delta is **0.25 of one standard deviation**. It is not a measured improvement.
The change may still be right on its reasoning, and it is not harmful, but it
should not be counted as evidence.
