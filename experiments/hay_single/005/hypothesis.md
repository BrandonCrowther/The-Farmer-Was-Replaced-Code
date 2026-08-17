# exp-005 — clustered-probe

**Hypothesis.** Three grass tiles at pairwise wrapped distance 2 (50% ball
overlap, 004) sharing one memory dict will show a hit rate measurably above
002's single-tile ~25-30%, approaching but not exceeding 004's derived 1/3
ceiling — and ticks/harvest will land nearer the ~800-tick best case than
002's measured ~1,300, but still above the 686 budget.

**Variable.** Single tile (002) → three-tile cluster, distance 2 apart,
shared companion memory. Everything else identical to 002's design.

**Metric.** Hit rate and ticks/harvest from `quick_print` lines, same
computation as 002's result.md, compared directly against it.

**Baseline.** 002: ~25-30% hit rate (rising, not yet plateaued in 60
cycles), ~1,300 ticks/harvest steady state. 004: derived ceiling ~33.3% hit
rate, ~800 ticks/harvest best case.

**Procedure.**
1. `saves/hay_single/main.py`: plant grass on all 3 tiles, then round-robin
   harvest/service/replant for 90 cycles (more than 002's 60, since 3x the
   tiles means the shared memory needs more visits to reach the same
   per-position coverage).
2. `tools/cycle.sh hay_single exp-hay_single-005-r1 --from <worktree>`.
3. Read `OUTPUT=`, compute hit rate over the second half (as 002 did, to
   exclude cold-start bias) and steady-state ticks/harvest.

**Falsifier.** If the hit rate does not clearly exceed 002's ~27.6%
second-half rate, clustering isn't earning its added movement and 006 should
finish the *simpler* single-tile design from 002 instead, not this one.
