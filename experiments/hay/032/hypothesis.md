# exp-032 — reroll-for-map-hit

**Hypothesis.** The farm is ~97% multiplied (031 + 026), so the gap is ticks per
harvest: 462 when the map says the companion tile is already correct, 1,459 when
it must be walked to. Rerolling until the request names an already-correct tile
should convert expensive passes into cheap ones at ~200 ticks a throw.

**Variable.** The reroll predicate: "is Carrot" -> "is not already satisfied".
Cap raised 2 -> 3.

**Metric.** One run vs 02:52.32 under matching conditions; floor 0.069 s.
