# exp-002 — reroll-to-15 + 10-tile round robin validation

**Hypothesis.** Rerolling every tile (harvest the unripe just-planted
sunflower + replant, ~400 ticks/attempt, `p=1/9` per attempt since
petals are uniform 7-15) until it hits petals=15 before letting it grow,
then round-robin harvesting across 10 such tiles, gives the 8x bonus on
every single harvest with zero tracking/ordering logic — since nothing
can exceed 15, a farm-wide tie for max is permanent. This validates
that end-to-end at a small scale (10 tiles, a handful of harvest cycles)
before committing to the real driver.

**Variable.** 001's single-lone-harvest probe → a real 10-tile
round-robin with reroll-to-15 on every (re)plant.

**Metric.** `GAIN` per harvest (expect 8 every time, no misses),
average reroll attempts to hit 15 (expect ≈9, geometric with p=1/9),
and `TICKS_PER_HARVEST` over several full round-robin cycles, to
project the real ~1,250-harvest total for the 10,000-Power target.

**Baseline.** 001: lone harvest, base 1 / bonus 8 (exact 8x, single
data point).

**Procedure.**
1. `saves/sunflowers_single/main.py`: plant 10 tiles (simple grid, no
   spacing concerns — no companion mechanic here, unlike carrots_single),
   reroll each to petals=15 before letting it grow.
2. Round-robin harvest+reroll-replant for ~20-30 cycles, instrumented
   like carrots_single's probes (`GAIN`, `REROLLS`, ticks per visit).
3. Read `OUTPUT=`; confirm 100% bonus rate, compute average ticks/harvest,
   project the full 1,250-harvest run.

**Falsifier.** If any harvest comes back at 1 instead of 8, either the
"≥10 on farm" condition isn't being met at that moment (e.g. a
mid-cycle gap where fewer than 10 sunflowers exist) or the reroll isn't
reliably reaching 15 — check which before assuming the whole paradigm
is wrong.
