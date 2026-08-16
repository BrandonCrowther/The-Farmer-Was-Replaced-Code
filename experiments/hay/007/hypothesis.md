# exp-007 — farm-state-diagnostic

**Hypothesis.** Not an optimisation. Two unverified assumptions underpin 004 and
006: that our own tile still holds a plant at the top of each pass, and that
`get_companion()` therefore returns a real preference every time. If the tile is
empty, `polyculture()` returns immediately and both experiments measured much
less than they appear to.

**Variable.** None. Champion code plus `quick_print`, which costs 0 ticks.

**Metric.** The `STATE` lines in `output.txt`, not the clock.
