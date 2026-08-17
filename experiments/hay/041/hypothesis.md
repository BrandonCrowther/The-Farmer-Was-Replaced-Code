# exp-041 — growth-schedulability

**Context.** This is the old, never-executed "037 growth-schedulability"
plan from Hay's queue — flagged early tonight as referenced in docs/LOOP.md
as if measured, but no `experiments/hay/037/` ever existed. Running it for
real now, motivated by 039's ~441-tick leader estimate and the old queue's
own independent "leader implies 2.2 tiles per drone at 466 ticks" note —
two separate estimates landing near the same number.

**Hypothesis.** Unlike hay_single (001: own-tile handling ≈ growth time,
zero idle time), Hay's servicing cost (`polyculture_mapped`, ~900 ticks
average per 039) may leave real idle time before the plant is ripe, or may
not — this measures it directly rather than assuming hay_single's
conclusion transfers.

**Variable.** None — 020's champion unchanged, instrumented with
`get_tick_count()` at three points per pass on the main drone only: right
after planting, right after `polyculture_mapped` returns, and the moment
`can_harvest()` first turns true.

**Metric.** `SVC_DONE - PLANT` (servicing cost), `RIPE - SVC_DONE` (idle
time, if positive), `RIPE - PLANT` (total growth-to-ripe time), and
`WATER` at ripeness, for 60 samples.

**Baseline.** hay_single's 001: own-tile handling (~400) ≈ growth (~404),
zero idle time, multi-tile closed. The question is whether Hay's numbers
land the same way or differently.

**Procedure.**
1. `saves/hay/main.py`: instrument the main drone's pass with the three
   tick-count reads; real scored run (background).
2. `tools/cycle.sh hay exp-hay-041-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute the three deltas per sample, check for real idle
   time in steady state.

**Falsifier.** If idle time is at or near zero (matching hay_single), the
farm is tick-limited the same way and multi-tile-per-drone is not
obviously a bigger lever here than it was there — the ~441/2.2-tiles
hypothesis needs a different explanation. If there's real, consistent idle
time, that's the headroom a genuine multi-tile-per-drone design could
target, and it would be worth testing for real before concluding anything
about the leader.
