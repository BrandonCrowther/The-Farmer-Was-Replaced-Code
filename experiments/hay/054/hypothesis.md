# exp-054 — reroll on distance>=2 (not just ==3), REROLL_LIMIT=5

**Hypothesis.** 053 tested rerolling away from `distance==3` alone with
the champion's existing `REROLL_LIMIT=2` and got a small regression
(1,482.65 vs 1,390 baseline) — not because the *idea* is wrong, but
because the trigger rate is high (`P(Carrot or dist==3) ≈ 2/3` given
the ≤3 companion range's cell-count-weighted distance distribution:
4/8/12 cells at distance 1/2/3) and `REROLL_LIMIT=2` (3 total draws)
isn't enough attempts to reliably land a cheap draw before giving up,
so many cycles pay the extra reroll cost for nothing. Extending the
trigger to `distance>=2` (keep only the rare, cheap distance-1 draws
outright) makes the trigger rate even higher (~8/9 by the same
cell-count math) — needs a correspondingly higher `REROLL_LIMIT` (5,
hay_single's proven cap) to actually have good odds of finding a
distance-1 draw within the attempt budget, rather than mostly paying
for failed escapes.

**Variable.** 053's (Carrot OR distance==3) trigger, `REROLL_LIMIT=2`
→ (Carrot OR distance>=2) trigger, `REROLL_LIMIT=5`.

**Metric.** `TICKS_PER_HARVEST` over a 150-cycle bounded probe, same
instrumentation as 047/049/051/053.

**Baseline.** 047: 1,390 (no distance-aware reroll). 053: 1,482.65
(distance==3 only, REROLL_LIMIT=2 — regression).

**Procedure.**
1. `saves/hay/main.py`: trigger condition `ctype==Carrot or
   wdist>=2`, `REROLL_LIMIT=5`.
2. `tools/cycle.sh hay exp-hay-054-r1 --from <worktree>`.
3. Compare to both prior baselines.

**Falsifier.** If this is also worse, the distance-aware-reroll family
is closed for real — the trigger-rate/attempt-budget tradeoff doesn't
have a sweet spot here, distinct from hay_single where a *much* lower
baseline hit rate (no neighbor cooperation at all) made rerolling
unconditionally profitable.
