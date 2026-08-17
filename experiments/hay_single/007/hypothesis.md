# exp-007 — single-tile-long-run

**Hypothesis.** A single tile, given enough cycles (200 vs 002's 60), also
accumulates wood from companion-tile churn (006's mechanism: harvesting a
now-mature standing Bush/Tree on a type mismatch) and Carrot becomes
satisfiable partway through, the same as it did in 006's 2-tile run — and
the steady-state ticks/harvest once that happens is the real number to
design 008's finishing driver against.

**Variable.** Cycle count only: 002's exact single-tile design, run to 200
cycles instead of 60.

**Metric.** `WOOD` over time, `CARROT_AFFORDED` count, hit rate and
ticks/harvest in the tail window (last 40-50 cycles) vs. 002's ~1,469-tick
baseline and 006's ~2,286-tick (2-tile, worse) result.

**Baseline.** 002 (60 cycles, `WOOD` stayed 0, Carrot never affordable,
~1,469 ticks/harvest). 006 (90 cycles, 2 tiles, wood reached 573,952 by
cycle ~22, but ~2,286 ticks/harvest due to inter-tile commute).

**Procedure.**
1. `saves/hay_single/main.py`: identical logic to 002, single tile, 200
   cycles, with `WOOD` and `CARROT_AFFORDED` added to the instrumentation.
   Printed every 5th cycle (plus the first 10) to keep output manageable.
2. `tools/cycle.sh hay_single exp-hay_single-007-r1 --from <worktree>`.
3. Read `OUTPUT=`; find the cycle where `WOOD` first goes nonzero and
   `CARROT_AFFORDED` first increments, and compute tail-window
   ticks/harvest the same way 002/006 did.

**Falsifier.** If `WOOD` stays 0 for all 200 cycles, single-tile genuinely
doesn't generate wood the way 2-tile did (needs more distinct companion
positions in play, not just more time) and 003's original conclusion stands
for the single-tile design specifically, even if not universally.
