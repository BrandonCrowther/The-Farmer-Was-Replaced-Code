# exp-008 — plot-rotation

**Hypothesis.** exp-007 found `can_harvest()` False on 94.1% of passes, so drones
are growth-bound, not tick-bound. Giving each drone a 5x5 plot and walking it in
a circuit should remove the idle waiting — a tile gets the whole circuit to grow
— and plant the whole field instead of 36 tiles of 1024.

**Variable.** One drone, one tile, busy-wait → one drone, one plot, circuit.
Polyculture dropped for this run to isolate the idle-time hypothesis.

**Metric.** One run vs 03:40.911.
