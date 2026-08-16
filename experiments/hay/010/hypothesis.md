# exp-010 — lazy-companion

**Hypothesis.** The companion harvest-and-replant is ~400 ticks of a ~1400 tick
pass (two 200-tick operating functions), and it yields wood rather than the crop
being farmed — nothing that counts toward the target. When the companion tile
already holds the right plant, both operations are pure waste. Skipping them
should cut per-pass cost with the multiplier fully preserved.

**Variable.** `Common.polyculture()` checks `get_entity_type()` (1 tick) before
disturbing the companion tile.

**Metric.** One run vs 03:40.911; floor 0.15 s.

**Baseline.** `autofarmer` at the 009 journal commit — 03:40.911.

**Why this is the opposite of 008.** 008 removed yield to save work and lost 59x.
This removes work and keeps all the yield.
