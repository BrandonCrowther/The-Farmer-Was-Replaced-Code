# exp-005 — clustered-probe — result

**Outcome.** rejected as designed (distance-2 spacing) — but it surfaced a
real bug/mechanism 004's arithmetic never accounted for, which matters more
than the hit-rate number.

**The bug: self-collision.** Cycle 12 (`TILE (0,0) COMPANION
(Entities.Bush,(2,0)) ... AFFORD True`) named farm tile #2's own coordinates
`(2,0)` as tile #1's companion target. The code has no check against that —
it walked to `(2,0)`, found `get_entity_type() != Bush`, and **harvested our
own standing grass and replanted it as a Bush.** Cycle 13, arriving at what
it believes is "tile (2,0)", finds a Bush (not Grass), waits far longer for
it to ripen (tick delta 4,972 vs. a typical ~2,500-3,000), harvests it for
wood (`GAINED 0` hay — confirms it wasn't grass), and reads *its* companion
preference, which legitimately includes `Entities.Grass` — explaining the
otherwise-impossible `COMPANION (Entities.Grass, ...)` line. The loop's own
end-of-cycle `instructions()` call replants Grass there immediately after,
so the corruption is **self-healing, not permanent** — but every occurrence
wastes a full slow cycle (0 hay, a multi-thousand-tick wait for a Tree/Bush
instead of ~404 for grass) and this happened repeatedly (`WOOD` ended at
**818,688**, meaning tree/bush harvests occurred far more than the visible
early cycles alone would explain).

**Why 004 missed it.** Distance-2 spacing was chosen for high ball overlap
(50%, from 004's table) — but overlap that high requires the tiles to sit
*inside* each other's companion range (radius 3), which means each tile's
own coordinate is a valid candidate position for the *other* tile's
requests. **The property that makes shared-coverage clustering work (small
inter-tile distance) is the same property that causes self-collision** — the
two aren't independent, and 004's ceiling arithmetic implicitly assumed
"satisfy" is always free of side effects on your own farm.

**Numbers (contaminated by the bug, not directly comparable to 002):** 90
cycles, 6,972,416 hay, `TICK_FINAL` 199,609, `TIME_FINAL` 32.86s, hit rate
15/90 (16.7%, and unreliable — some "hits" may be hits on a still-corrupted
tile). Average ≈2,218 ticks/cycle, *worse* than 002's ≈1,469 average, despite
more raw hay collected (more cycles ran). Not a clean comparison; the
self-collision tax dominates whatever sharing benefit existed.

**Baseline.** 002 (~1,300 ticks/harvest steady state, single tile, no
collision risk since there's only one farm tile to collide with — itself,
which `get_companion()`'s own "never itself" rule already excludes).

**Noise floor.** Not established.

**Screenshots.** None — probe, `output.txt` carries the data.

**Verdict.** Distance-2 clustering is rejected — not on throughput grounds,
but because it can silently corrupt the farm it's supposed to be growing.
**The fix is spacing, not detection logic:** pick inter-tile distance
**> 3** (outside every tile's own companion range) so no tile's coordinate
can ever be named as another tile's companion target, while distance
**4-6** still keeps 25-42% ball overlap (004's table) for whatever sharing
benefit remains. 006 should retry at distance 4 rather than add a
same-position guard to the distance-2 design — removing the hazard by
construction is simpler than detecting and recovering from it every cycle.
