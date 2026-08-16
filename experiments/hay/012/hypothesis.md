# exp-012 — skip-unaffordable

**Hypothesis.** A Carrot companion costs 512 hay + 512 wood and wood sits at 0,
so the trip plants nothing and earns no multiplier — while costing the full round
trip at 200 ticks a move. Checking affordability first costs about a tick.

**Variable.** `Common.polyculture()` returns before moving when the companion is
unaffordable.

**Metric.** Time vs 03:24.552; floor 0.15 s, so a sub-0.3 s win needs confirming.
