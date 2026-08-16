# exp-014 — thirty-two-drones

**Hypothesis.** `max_drones()` is 32 and the grid attempts 36, so four spawns
return `None` every run. Because the loop is column-major those four are always
(5,2)–(5,5): a contiguous unfarmed strip. Spreading the four holes through the
middle instead keeps all 32 drones and gives each fewer neighbours to contend
with.

**Variable.** Which four of the 36 grid positions go unused.

**Metric.** Time vs 03:05.789; floor 0.15 s. Plus `SPAWNED n of 32` to confirm
the count directly rather than trusting the `if d:` guard.
