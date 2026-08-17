# exp-003 — reactive-single-tile

**Hypothesis.** A single Carrot tile, skipping Grass companions for free
(002's finding) and fully servicing Bush/Tree (walk, plant, revert to
Grass afterward), will show real, substantial idle time (`IDLE_TICKS`)
because growth (~7,196 ticks, 001) is much larger than own-handling plus
even a full Bush/Tree service (~400 + ~1,800 ≈ 2,200 ticks worst case) —
unlike hay_single (zero idle, 001) and unlike Hay (idle real but too small
for a second tile, 041/044).

**Variable.** None — this is the first real driver design for the
category, not a variant of anything existing.

**Metric.** Per-cycle `SVC_TICKS` (companion handling), `IDLE_TICKS`
(wait-for-ripe after servicing), `TOTAL_TICKS`; aggregate
`TICKS_PER_HARVEST`, `HITS_GRASS` (should be ≈1/3 of cycles) vs
`HITS_SERVICED`.

**Baseline.** 001: growth ≈7,196 ticks mean. hay_single 001: zero idle
time on any pass, own-handling ≈ growth almost exactly.

**Procedure.**
1. `saves/carrots_single/main.py`: single-tile reactive driver, 40 cycles,
   instrumented per-cycle and in aggregate.
2. `tools/cycle.sh carrots_single exp-carrots_single-003-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute `IDLE_TICKS` distribution and `TICKS_PER_HARVEST`.

**Falsifier.** If `IDLE_TICKS` is near zero on most cycles (own-handling +
service already exceeds growth), this category is servicing-bound like
hay_single after all and multi-tile shouldn't be pursued — 001's
17.8x-slower-growth read would need revisiting (e.g. if servicing here is
also proportionally much more expensive than assumed).
