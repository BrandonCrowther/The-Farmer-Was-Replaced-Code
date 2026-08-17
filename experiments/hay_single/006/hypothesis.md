# exp-006 — clustered-v2-distance4

**Hypothesis.** Two grass tiles at wrapped distance 4 (41.7% ball overlap,
004; outside each other's own companion range so 005's self-collision is
structurally impossible) will show `SELFGUARD` staying at 0, and a hit rate
above 002's single-tile baseline without 005's corruption tax.

**Variable.** Distance-2 cluster (005, buggy) → distance-4 cluster (this
experiment), same-tile guard added defensively.

**Metric.** `SELFGUARD` count (should be 0 — confirms the spacing fix
actually works), hit rate, and ticks/harvest, compared cleanly against 002's
baseline this time (005's numbers were contaminated).

**Baseline.** 002: ~25-30% hit rate, ~1,300 ticks/harvest steady state.

**Procedure.**
1. `saves/hay_single/main.py`: 2 tiles at `(0,0)` and `(4,0)`, 90 cycles,
   same reactive skip/service/remember logic as 002/005 plus the guard.
2. `tools/cycle.sh hay_single exp-hay_single-006-r1 --from <worktree>`.
3. Read `OUTPUT=`; confirm `SELFGUARD == 0`, then compute hit rate and
   ticks/harvest as in 002.

**Falsifier.** If `SELFGUARD` is nonzero, the distance-4 reasoning itself is
wrong (not just the previous spacing) and needs redoing from the API, not
just widened further by guesswork. If hit rate doesn't clearly beat 002 once
clean, clustering earns nothing and 007 should finish the single-tile design
instead.
