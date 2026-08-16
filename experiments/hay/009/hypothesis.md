# exp-009 — measure-idle-ticks

**Hypothesis.** exp-008 assumed the farm was growth-bound on the strength of a
frequency statistic. Measure the duration instead: the share of ticks actually
spent in the busy-wait.

**Variable.** None. Champion code plus `get_tick_count()`, which costs 0 ticks.

**Metric.** cum_wait / cum_total over 25 passes.
