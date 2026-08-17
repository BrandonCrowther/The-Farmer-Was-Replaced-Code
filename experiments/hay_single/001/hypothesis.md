# exp-001 — mechanics-probe

**Hypothesis.** The per-tile handling cost (move+till+plant, 200 ticks each on
success) matches the wiki's global constant here too, and grass growth ticks
(G) and the water equilibrium a single drone can hold on one 8x8-farm tile are
*not* the same as the Hay category's figures, because those were taken under a
different drone-count/tile-count water economy. Both numbers are needed before
any multi-tile "floor" design can be justified rather than guessed.

**Variable.** None being varied — this is a read-only instrumentation pass over
the (as yet unwritten) hay_single driver.

**Metric.** `get_tick_count()` deltas and `get_water()` samples read from
`output.txt` via `quick_print`. The run is expected to end in "Run Failed"
(target not reached, deliberately) — the duration on the modal is not read or
recorded.

**Baseline.** None — hay_single has never scored. This probe exists to supply
the constants the write-driver experiment (queued as 002) designs against.

**Procedure.**
1. Probe `main.py`: op-cost sanity check (move/till/plant), water-equilibrium
   sampling (5 samples), then 5 plant→ripen→harvest cycles recording growth
   ticks, water at plant and at ripeness, and the companion request (type +
   Manhattan distance) each cycle.
2. `tools/cycle.sh hay_single exp-hay_single-001-r1 --from <worktree>`.
3. Read `OUTPUT=` directly (`quick_print` lines) — no vision needed, nothing
   on the modal matters here.
4. If growth ticks vary a lot across the 5 samples, don't trust a single probe;
   note it and widen in a follow-up rather than trying to fit a distribution to
   n=5.

**Falsifier.** If `MOVE_TICKS`/`TILL_TICKS`/`PLANT_TICKS` are not 200, the
wiki's operation-cost table does not apply as-is here and every tick budget
below has to be redone. If `GROWTH ... TICKS` comes back near the Hay
category's unverified "422" figure (docs/LOOP.md cites this as measured by an
`experiments/hay/037`, but no such experiment was ever actually run — no
directory, no result.md), treat any match as coincidence, not confirmation,
until a same-water comparison exists.
