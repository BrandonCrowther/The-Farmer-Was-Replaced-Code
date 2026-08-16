# exp-014 — thirty-two-drones — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:05.323** | PB; rank **#177**. `SPAWNED 32 of 32` |

**Baseline.** 03:05.789 · **Variant.** 03:05.323 · **Delta.** **−0.466 s (−0.25%)**

**Noise floor.** 0.15 s. The win is 3.1x the floor, over the 2x bar for trusting
a single run.

**Verdict.** Small, and worth having for the reason rather than the number: the
farm is now demonstrably fully staffed. `SPAWNED 32 of 32` is the first direct
confirmation of the drone count — thirteen experiments ran with four positions
silently empty, absorbed by the `if d:` guard, and no measurement would have
caught it because nothing reported it.

The gain is small because position barely affects a drone's own yield; it only
changes how much neighbouring companion ranges overlap. Moving the four holes
inward trims a little contention and nothing else.

**Contention cannot be fixed by geometry.** Eliminating overlap needs drones 7
apart (companion range 3, twice). Thirty-two drones on a 32x32 farm have 32 tiles
each, so the best achievable spacing is sqrt(32) ~= 5.66 — under 7 whatever the
arrangement, and the farm wraps, so no clever edge packing helps either. Overlap
is a property of the drone count, not the layout.

That points the next experiment at the map rather than the placement: make it
self-correcting, so a tile found to disagree with its record is marked contested
and always walked thereafter.
