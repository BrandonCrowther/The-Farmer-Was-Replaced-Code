# exp-013 — companion-map

**Hypothesis.** 010 skips the companion harvest-and-replant when the tile is
already correct, but only learns that after walking there. If each drone
remembers what it planted where, the whole ~800 tick round trip can be skipped
when the tile has not changed.

**Variable.** `Common.polyculture_mapped(planted)` — a per-drone dict of its own
plantings, consulted before moving.

**Metric.** Time vs 03:24.327; floor 0.15 s.

**Risk.** Asymmetric. A stale entry causes a *skip*, forfeiting the 67x
multiplier on that harvest, which is far worse than a needless walk. Drone
neighbourhoods overlap — spacing is 5 and companion range is 3, so a drone at
x=3 reaches x=6 and one at x=8 reaches x=5 — so entries for the boundary band
can go stale. Mitigated by recording only this drone's own plantings and still
verifying with `get_entity_type()` whenever we do walk.

**Also measured, free:** `max_drones()` and `get_world_size()`, one line, two
ticks. The 6x6 spawn grid is inherited and has never been checked against the
cap.
