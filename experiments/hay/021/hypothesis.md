# exp-021 — diamond-lattice

**Hypothesis.** Overlapping territories let drones overwrite each other's
plantings and invalidate each other's map entries. Movement is Manhattan (the API
defines exactly four Directions) so "within 3 moves" is a 25-tile diamond, and 32
diamonds need 800 of the farm's 1024 tiles — disjoint territories fit. A lattice
of rows 4 apart, centres 8 apart, odd rows offset 4 gives 32 centres at minimum
L1 separation 8, verified including the wrap. 019 confirmed by measurement that
companion requests are always at L1 1–3 and never wrap.

**Variable.** Drone placement only.

**Metric.** One run vs 02:52.271; floor 0.15 s.
