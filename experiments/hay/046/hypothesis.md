# exp-046 — full diagnostic re-probe (post-checkpoint)

**Hypothesis.** The champion's 3x gap to the leader has been narrowed
down (038-045) to "not the mechanism-level things already tested", but
no single fresh probe has captured the *whole* per-harvest cost and
yield breakdown at once, under real 32-drone contention, since 039/041
each measured one slice. Re-running a full instrumented pass — per-
cycle yield, companion type, servicing outcome (map-skip / real-walk /
Carrot-give-up-reroll), ticks spent servicing vs idle, and the real
achieved water level — over a longer bounded sample should either (a)
surface a concrete numeric target for a real fix (e.g. Carrot's true
current failure rate, which real water level is actually achieved), or
(b) rule out enough that a structurally different design (not a
parameter tweak) is the only remaining explanation.

**Variable.** None — a measurement pass, not a design change. Uses the
exact current champion logic on the main drone, with real 32-drone
contention, just adds `quick_print` instrumentation.

**Metric.** Per-cycle: `GAINED` (Hay yield), `COMPANION_TYPE`,
`OUTCOME` (skip/walk/carrot-giveup), `SVC_TICKS`, `IDLE_TICKS`,
`WATER_AT_HARVEST`. Aggregated: yield/tick, hit-rate by outcome,
real average water level.

**Baseline.** 039: ≈1,300 ticks/harvest (mean only, no breakdown). 041:
idle ≈3 (miss) / ≈492 (hit) ticks, ~32%/68% split. Champion comment:
Bush 5/5, Tree 7/7, Carrot 1/8 (small, old sample).

**Procedure.**
1. `saves/hay/main.py`: keep the 32-drone spawn structure unchanged;
   instrument only the main drone's loop, bounded to ~150 cycles.
2. `tools/cycle.sh hay exp-hay-046-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute the aggregates above.

**Falsifier.** If nothing in the breakdown suggests a lever bigger than
the ~10-15% pieces already estimated by hand, say so plainly and pivot
to designing a structurally different layout (dense shared-garden
cluster) rather than continuing to slice the existing design thinner.
