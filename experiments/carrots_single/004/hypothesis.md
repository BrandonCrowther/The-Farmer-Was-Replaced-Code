# exp-004 — multi-tile-pipeline

**Hypothesis.** 3 tiles round-robin (own-tile handling ≈2,422 ticks +
≈800 average commute at distance 4 = ≈3,222/visit), against growth
≈7,196, crosses the idle-elimination threshold at N≈2.23 — so N=3 should
already be at or past the throughput plateau, giving ≈25.4 carrots/tick
(≈2.6x over 003's single-tile 9.80).

**Variable.** Single tile (003) → 3 tiles at (0,0), (0,4), (2,2), pairwise
wrapped distance exactly 4 (safely outside every tile's own companion
range, avoiding the self-collision hazard by construction rather than by
distance-based luck).

**Metric.** `TICKS_PER_HARVEST` (60 cycles / 3 tiles = 20 full rounds),
compared to 003's real ≈8,362.

**Baseline.** 003: single tile, real ≈8,362 ticks/harvest, ≈9.80
carrots/tick.

**Procedure.**
1. `saves/carrots_single/main.py`: 3-tile round-robin, same reactive logic
   as 003 (free Grass, service+revert Bush/Tree), 60 cycles (20 full
   rounds).
2. `tools/cycle.sh carrots_single exp-carrots_single-004-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute ticks/harvest and compare.

**Falsifier.** If ticks/harvest doesn't clearly beat 8,362, the commute-
cost model is wrong somewhere (e.g. real average commute is higher than
the 800 assumed, or growth doesn't line up with 001's isolated
measurement once multiple tiles are actually growing concurrently) — say
what the model missed, don't just report the miss, the way Hay's 044 did.
