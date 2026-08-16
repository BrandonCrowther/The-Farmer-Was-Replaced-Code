# exp-019 — mechanics-probe

**Not an optimisation.** Measures four things the category's reasoning depends on
but never measured: the polyculture multiplier, growth time, companion distance
distribution, and real water levels.

**Design.** One drone — `num_items` is global, so with 32 drones the hay delta
across our own harvest is contaminated by everyone else's. Alternating passes
satisfy or skip the companion; the difference between the yields is the
multiplier. 40 passes, then terminate. Will not score.
