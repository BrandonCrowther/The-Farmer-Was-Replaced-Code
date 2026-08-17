# exp-015 — bush-blanket-quad

**Hypothesis, per the user's proposal (a genuinely different strategy
shape, not a parameter tweak on the existing design).** 4 grass tiles
clustered together, with the entire rest of the 8x8 board pre-planted with
Bush (one-time setup, ~36,000 ticks estimated), then reroll (uncapped)
until a draw is Bush *and* doesn't name one of our own hay tiles. Stated
prediction before running: since this hinges on the same p=1/3 type-match
draw as the existing design's proven steady state (011), it should
converge to the same ~1,200 ticks/harvest once setup is amortized — a
different-looking mechanism reaching the same mathematical ceiling, not a
way past it. Testing this directly rather than assuming it, per the user's
point that the specific example matters less than genuinely checking
fundamentally different shapes.

**Variable.** Single tile, position-based memory (012's champion) → 4
clustered tiles, pre-established total-board Bush blanket, type-only
reroll (no per-position memory needed at all).

**Metric.** `SETUP_TICKS` (the one-time cost), then post-setup steady-state
ticks/harvest from the `CYCLE` trace, compared to 012's real ≈68.7 hay/tick
(≈1,192 ticks/harvest).

**Baseline.** 012 (champion): ≈68.7 hay/tick. Stated model prediction for
this design: ≈68.3 hay/tick asymptotic (same ceiling), worse when the
one-time setup and any inter-tile commute are included.

**Procedure.**
1. `saves/hay_single/main.py`: blanket the board (excluding the 4 hay
   tiles) with Bush, then round-robin 300 harvest cycles across the 4
   tiles, rerolling (uncapped) until Bush at a non-hay-tile position.
2. `tools/cycle.sh hay_single exp-hay_single-015-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute `SETUP_TICKS` and post-setup ticks/harvest.

**Falsifier.** If post-setup ticks/harvest is clearly *below* ≈1,200 (not
just close to it), the model is missing something real and this reopens
multi-tile as a genuine lever — say explicitly what the model missed, not
just that it happened. If it's at or above ≈1,200 plus real commute/setup
overhead, this confirms the ceiling is real regardless of *how* full
coverage is achieved (organic vs. pre-established), which is the stronger,
more general result either way.
