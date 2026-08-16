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

**~~Contention cannot be fixed by geometry.~~ CORRECTED — see exp-018.** This
section originally argued that eliminating overlap needs drones 7 apart, that 32
drones over 1024 tiles gives 32 tiles each, and that the best achievable spacing
is therefore sqrt(32) ~= 5.66, under 7 whatever the arrangement.

**That is wrong.** It reasons about circles in a world with no diagonal movement.
Distance here is Manhattan, so "within 3 moves" is a *diamond* of 2r^2+2r+1 = 25
tiles, not a 7x7 square of 49. Thirty-two diamonds need 800 tiles against the
farm's 1024, so disjoint territories fit — and a staggered lattice (rows 4 apart,
centres 8 apart along a row, odd rows offset by 4) places exactly 32 centres at a
minimum L1 separation of 8, wrap included.

The area-per-drone argument was sound; using the Euclidean intuition for what
that area buys was not.

This pointed the next experiment at the map rather than the placement (015,
rejected). With the correction above, the placement route is open after all and
is exp-018.
