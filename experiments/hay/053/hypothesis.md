# exp-053 — reroll away from distance-3 draws too, not just Carrot

**Hypothesis.** The champion only rerolls to escape `Entities.Carrot`
(expensive because it needs `till()`). It never rerolls to escape an
expensive *distance*, even though a distance-3 walk costs meaningfully
more round-trip movement (2×641=1,282) than a distance-1 walk
(2×225=450). Rerolling away from BOTH Carrot and distance-3 draws (up
to the same `REROLL_LIMIT=2`) should bias the realized walk-distance
distribution toward the cheaper end, cutting average commute cost on
real-walk cycles.

**Variable.** Champion's Carrot-only escape reroll → reroll on
(`type==Carrot` OR `wrapped_distance==3`), same `REROLL_LIMIT=2`.

**Metric.** `TICKS_PER_HARVEST` over a 150-cycle bounded probe (main
drone, real 32-drone contention), compared to 047's 1,390.

**Baseline.** 047: 1,390 ticks/harvest. Fresh leaderboard check (this
session): #2-10 cluster tightly at 01:27-01:48 (vs our real
02:47-02:52) — a "normal good implementation" tier roughly 1.6x
faster, distinct from #1's further 1.8x edge on top of that. Targeting
closing ground toward that cluster, not necessarily #1.

**Procedure.**
1. `saves/hay/main.py`: extend the reroll condition to include
   distance-3 draws.
2. `tools/cycle.sh hay exp-hay-053-r1 --from <worktree>`, bounded to
   150 cycles, same instrumentation as 047/049/051.
3. Compare ticks/harvest and skip/walk split to 047.

**Falsifier.** If ticks/harvest doesn't clearly improve, the extra
reroll cost on the wider trigger condition outweighs the commute
savings — say so and close this specific variant rather than tuning
the distance threshold further by guesswork.
