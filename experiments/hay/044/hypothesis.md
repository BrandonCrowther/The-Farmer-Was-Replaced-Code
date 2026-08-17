# exp-044 — multi-tile-scheduled

**Hypothesis.** Tending a second tile (distance 1, cheapest commute) only
during the ~492-tick idle window 041 measured on tile A's hit-cycles
(~32% of passes) — never on miss-cycles, where there's no slack — raises
total harvests/tick above the single-tile champion's real ~1,300
ticks/harvest (039), because it's spending currently-wasted idle time
rather than adding unconditional overhead.

**Variable.** Single tile (020's champion, main drone) → two tiles at
distance 1, second tile serviced only when the first tile's companion
request is cheap (memory hit, unaffordable-skip, or self-collision) —
peeked via `get_companion()` before deciding, not discovered by walking.

**Metric.** `TICKS_PER_HARVEST` = total ticks / (harvests on A + harvests
on B), compared to 039's real ≈1,300.

**Baseline.** 039: main drone, single tile, real ≈1,300 ticks/harvest
steady state.

**Procedure.**
1. `saves/hay/main.py`: main drone runs the scheduled 2-tile logic for 80
   cycles (bounded, not chasing the target); other 31 drones run 020's
   normal logic for a small bounded 5 cycles each (avoiding 043's
   infinite-loop trap) and are reaped with `wait_for()`.
2. `tools/cycle.sh hay exp-hay-044-r1 --from <worktree>` — bounded probe,
   should be much faster than a full scored run.
3. Read `OUTPUT=`; compute ticks/harvest and compare to 039's baseline.

**Falsifier.** If ticks/harvest doesn't clearly beat 1,300, either the idle
window isn't as reliably exploitable as 041 suggested (e.g. tile B's own
miss rate eats into the borrowed time more than expected), or the
scheduling logic has a bug — check `HARVESTS_B` first (should be roughly
32% of `HARVESTS_A`, matching the hit rate) before concluding the whole
approach doesn't work.
