# exp-020 — reroll-after-harvest

**Hypothesis.** 019 measured a 160x multiplier and showed carrot is satisfied
only 1 time in 8 while Bush and Tree never fail. Carrot is a third of requests,
so a third of passes collect 512 instead of 81,920. Replanting rerolls the
preference and grass is free, so rerolling away from carrot should recover most
of that.

**Variable.** After the harvest, replant and reroll while the companion is
Carrot, capped at 2.

**Why 006 failed and this should not.** 006 rerolled at the *top* of the pass,
harvesting the mature grass while its companion was still unsatisfied — taking
512 for a harvest that would have been 81,920. It paid for the reroll by
destroying the thing it was buying. Here the multiplied harvest has already
happened and the tile is empty, so a reroll is one plant rather than a harvest
plus a plant.

**Metric.** One run vs 03:04.715; floor 0.15 s.
