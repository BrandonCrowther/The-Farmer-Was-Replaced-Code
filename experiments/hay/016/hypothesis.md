# exp-016 — no-carrot

**Hypothesis.** Carrot is the only companion that can fail after the walk is
paid for: it needs Soil, and `till()` will not convert ground a plant stands on,
so an unripe plant blocks it. Skipping carrot requests outright should save those
wasted round trips.

**Variable.** `polyculture_mapped` returns immediately on a Carrot request.

**Metric.** One run vs 03:05.323; floor 0.15 s.
