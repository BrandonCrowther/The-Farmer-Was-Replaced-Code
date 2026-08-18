# exp-076 — fix setup-phase movement (move_to → move_to_wrapped)

**Hypothesis.** User-flagged, both real: (1) the initial long walk from
each drone's spawn point to its own base tile used `Common.move_to()`
— unwrapped, always the direct path — instead of
`Common.move_to_wrapped()`, even though `move_to_wrapped`'s own
docstring exists specifically for this ("use it for placement"); with
drones at 3..28 on a 32-wide farm, some assignments pay a much longer
walk than necessary. (2) `move_to()` also carries a leftover
`protocol()` indirect-call parameter and a `num_unlocked(Unlocks.Mazes)`
check, evaluated on every move, for a maze-avoidance feature this
category never uses; `move_to_wrapped()` has neither. Switching every
`Common.move_to()` call in `driver()` to `Common.move_to_wrapped()`
should reduce setup-phase latency, which — per the "repeat until 2h
simulated time, average the runs" scoring rule — is paid again every
repeat, not amortized away by one long run.

**Variable.** `Common.move_to()` → `Common.move_to_wrapped()`,
everywhere in `driver()` (both the initial spawn-to-base walk and the
bush-wall setup loop).

**Status: RESOLVED — adopted, new champion.** Picked up next session:
validated (64/64 arrival checks clean, see `result.md`), then run for
real: **01:57.195, #60** (was 075's 01:58.059/#63). See `result.md` for
the full writeup.

**Also flagged in the same review, not attempted at all:**
1. **Spawn-tree parallelization** — 073's spawn pattern has one drone
   sequentially spawn all 31 others (~6200 ticks of pure spawn latency
   before the last drone starts). A tree-spawn redesign (each spawned
   drone also spawns some of the remainder) would reduce this to
   roughly log2(32)≈5 sequential rounds, but needs its own correctness
   validation (every position covered exactly once, no gaps) that
   didn't fit in the time available.
2. **Shared bush-wall planting** — every drone currently walks and
   checks all ~30 of its reachable companion positions even when a
   neighbor already planted a shared one (the code skips the redundant
   *plant*, via the `get_entity_type() != Bush` guard, but not the
   redundant *walk-to-check*). Partitioning tile ownership across
   neighbors so each shared position is only ever visited by one drone
   would cut this further, but risks silently leaving a tile unassigned
   if the partition has a gap — needs careful design, not a rushed fix.

**Next session**: pick up this branch, run the validation pass that was
interrupted (reduced target, no `zzRunner.py`, crop-tile collision
check across all 64 tiles) before attempting a real run.
