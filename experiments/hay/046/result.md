# exp-046 — full diagnostic re-probe (post-checkpoint) — result

**Outcome.** probe — established real, current numbers to replace
stale assumptions before further design work.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `HITS_SKIP` 55/150 (36.7%), `HITS_WALK` 95/150 (63.3%) | matches roughly the low end of the champion's own "44-66% hit rate" claim |
| r1 | `WATER` samples 0.8-1.0 throughout | **not** "10x short" as the champion's long-standing comment claims |
| r1 | Early cycles' `GAINED` values erratic (327,680-901,120, not clean 81,920 multiples) | shared-inventory contamination — `num_items(Items.Hay)` is global across all 32 drones, so a before/after delta around one drone's harvest can catch concurrent neighbors' harvests too; stabilizes to exact 81,920 by cycle ~30 |

**Baseline.** None — first fresh diagnostic pass tonight.

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** Two real corrections to long-standing assumptions: water
is fine (0.8-1.0, not "10x short"), and the shared-inventory
contamination in `GAINED` measurements (fixed in later probes by
relying on `get_tick_count()` deltas instead) is a real gotcha for
any future multi-drone Hay diagnostic. 047 drills into the `SVC_TICKS`
breakdown for walk cycles specifically.
