# exp-015 — self-correcting-map

**Hypothesis.** Contention cannot be designed away (32 drones on a 32x32 farm sit
~5.66 apart; disjoint companion ranges need 7), so handle it in the map: a tile
found holding something other than its record has been touched by another drone,
and should be marked untrusted so later passes always walk and check.

**Variable.** `polyculture_mapped` marks a disagreeing tile `None` permanently.
Also folds in `move_to_wrapped` for initial placement — one-time, ~0.0007% of a
drone's ticks, and therefore not expected to be measurable.

**Metric.** One run vs 03:05.323; floor 0.15 s.
