# exp-051 — tighter packing (spacing 4, not 5) to raise physical neighbor-cooperation

**Hypothesis.** 050 confirmed drones are truly isolated (no shared
mutable state across spawned drones — a top-level dict written by one
drone is invisible to another) — the only channel between drones is
the physical game world. "Neighbor cooperation" (some walk cycles
finding the entity already correct on arrival, because a *different*
drone planted it earlier — 047: 3/95 walks) can only be grown by
increasing how much drones' companion-request footprints (radius-3
discs around each home) overlap. Current spacing is 5 (chosen so
companion range 3 never reaches another drone's own tile — 5 > 3,
self-collision-safe). Reducing spacing to 4 (still stricty > 3, still
self-collision-safe by the same margin, confirmed via brute-force
pairwise-distance check) packs the same 32 drones into a smaller
region, increasing footprint overlap density and should raise the real
(non-reroll, non-shared-memory) skip rate.

**Variable.** Champion's spacing-5 6x6-minus-4-holes grid → spacing-4
6x6-minus-4-holes grid, same 32 drones, same REROLL_LIMIT=2 Carrot-only
escape reroll (unchanged from champion).

**Metric.** `TICKS_PER_HARVEST` and skip/walk split over a 150-cycle
bounded probe (main drone only), compared to 047's corrected baseline
(1,390 ticks/harvest, 37% skip / 63% walk).

**Baseline.** 047: 1,390 ticks/harvest, `HITS_SKIP` 55/150 (36.7%),
`HITS_WALK` 95/150 (63.3%).

**Procedure.**
1. `saves/hay/main.py`: same champion logic, spacing changed from
   `3 + i*5, 3 + j*5` to `2 + i*4, 2 + j*4`.
2. `tools/cycle.sh hay exp-hay-051-r1 --from <worktree>`, bounded to
   150 cycles, main drone instrumented (skip/walk counters +
   TICKS_PER_HARVEST, matching 047/049's instrumentation).
3. Compare skip rate and ticks/harvest to 047's baseline.

**Falsifier.** If skip rate doesn't clearly rise, physical neighbor
cooperation isn't meaningfully density-sensitive at this scale (maybe
32 drones' footprints already overlap about as much as they're going
to, or contention/collision costs offset the gain) — say so and close
this line rather than trying yet-tighter spacing blindly.
