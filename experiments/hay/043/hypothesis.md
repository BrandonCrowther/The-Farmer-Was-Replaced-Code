# exp-043 — tick-rate-check

**Hypothesis.** Hay's real growth-to-ripe time (041: ~1,183 ticks) is
nearly 3x hay_single's directly-measured growth time (001: ~404 ticks) for
the same crop at similar water. If the tick rate (ticks/simulated-second)
is lower with 32 concurrent drones active than solo — e.g. a shared
compute/"Power" budget divided among active drones — that would explain
the gap directly, without needing any difference in per-harvest *work*.

**Variable.** None — measures `get_time()`/`get_tick_count()` deltas over
an identical fixed operation sequence (40 moves), once before spawning any
other drones (solo) and once immediately after spawning all 31 (swarm).

**Metric.** `RATE = DTICK / DTIME` for `SOLO` vs `SWARM32`, compared
against hay_single's directly-measured ~6,070 ticks/s (001).

**Baseline.** hay_single: ~6,070 ticks/s, solo, single-drone category.

**Procedure.**
1. `saves/hay/main.py`: measure 40-move tick/time delta solo, then spawn
   all 31 drones (each executing the normal champion loop, so real
   concurrent load exists), measure again immediately.
2. `tools/cycle.sh hay exp-hay-043-r1 --from <worktree>` — does not chase
   the target or reap drones, so this should be a fast probe like
   hay_single's, not a full ~7-10 minute scored cycle.
3. Read `OUTPUT=`; compare `SOLO` and `SWARM32` rates.

**Falsifier.** If `SOLO` and `SWARM32` rates match closely (and both are
near hay_single's ~6,070/s), drone count does not affect tick rate, and
041's 3x growth-time gap needs a different explanation (water, a
category-specific Power grant, or something else) — recheck rather than
assume the shared-budget hypothesis.
