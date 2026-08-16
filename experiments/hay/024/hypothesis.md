# exp-024 — lattice-wrapaware

**Hypothesis.** 021's lattice put drones on x=0 and y=0, whose companions land at
31 across the wrap, and `Common.move_to` walks the direct path — 31 moves instead
of 1, 6200 ticks instead of 200. Making the polyculture hot path use
`move_to_wrapped` should recover the regression.

**Variable.** `move_to` -> `move_to_wrapped` inside `polyculture_mapped`. Layout
identical to 021.

**Metric.** One run vs 02:52.271 champion, and vs 021's 03:19.653.
