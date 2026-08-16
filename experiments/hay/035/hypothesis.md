# exp-035 — query-until-hit

**Hypothesis.** 033 measured `get_companion()` rerolling on every call at 1 tick,
while every reroll so far has replanted at 200. Asking repeatedly until the
request names a tile the map already satisfies should turn a 1,455-tick
walk-and-replant into a 26-tick skip, and 034 says the skip rate must reach ~66%
before a second plot per drone can pay.

**Variable.** A query loop (cap 12) before the affordability check in
`polyculture_mapped`.

**Metric.** One run vs 02:52.32 under matching conditions.
