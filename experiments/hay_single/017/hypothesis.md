# exp-017 — port Hay(multi)'s stray-tick fixes (075/076/079/081/082)

**Hypothesis.** `hay_single`'s current champion (016) only ported
Hay(multi)'s *macro* two-tile design from exp-073 — it predates every
micro-optimization Hay(multi) found afterward (075's dropped no-op
`instructions()` calls, 076's `move_to_wrapped`, 079's three fixes,
081's redundant-target-check drop, 082's water-check reorder). Since
`hay_single` is single-drone, none of 077/078/080's spawn-tree/
territory-partitioning material applies, but everything else does — and
`hay_single`'s own code is actually *worse* than Hay-multi's pre-075
state on the `instructions()` front: it calls it twice per reroll cycle
(once before the loop, once every iteration), not once.

**Variable.** Port all five applicable fixes verbatim into
`hay_single/main.py`'s single-drone driver: drop the two redundant
`instructions()` calls in the reroll chase, `move_to`→`move_to_wrapped`
for the initial placement walk, the reroll chase's constant-comparison
fix, the bush-wall setup's `wdist` short-circuit and cached
`get_entity_type()`, drop the move()-guarding redundant target check,
reorder the water-check `and`.

**Correctness check.** Every one of these fixes was already proven
correct (by code-reading and/or live validation) in Hay(multi)
tonight — porting is mechanical, not a fresh design. Still validated
live before the real run: the real `TARGET=100,000,000` is unusable
(persistent save inventory is already ~54 billion, shared across every
category via the same `live/save.json`, so the loop would never even
enter) — used `TARGET = current inventory + 3,000,000` instead. Result:
clean termination, overshoot 31,040 (well under one satisfied harvest),
no warnings, 3-line output only.

**Baseline.** 016 (`auto_experiment/hay_single/016`): 03:08.281, #89.
