# exp-029 — two-plots — result

**Outcome.** rejected

**Numbers.**

| run | metric | note |
| --- | --- | --- |
|  1  | **03:20.637** | vs 02:52.32 fresh-game champion mean |

**Delta.** **+28.317 s (+16.4%)** — hundreds of sd. Unambiguous.

**Verdict.** Multi-plot loses at four plots (027, +47 s) and at two (+28 s). The
idea is dead in this shape.

**And the model that motivated it was wrong.** Costing it out from 026's
measurements:

| | champion | two plots |
| --- | --- | --- |
| mismatch pass (52%) | 1459 | 1459 + 200 move = 1659 |
| skip pass (45%) | 26 + 437 wait = 462 | 26 + 200 move, no wait = 226 |
| **weighted mean** | **967** | **965** |

The model predicts a wash and the measurement says +16%. **Something in the
two-plot arrangement costs ~150 ticks a harvest that this accounting does not
capture**, and rather than invent a third mechanism — after "contention is
cooperation" and "wrapped walks" both turned out to be fiction — it is recorded
as an open question.

Candidates worth measuring, not asserting:

- **Plots cannibalising each other.** A companion request can target the drone's
  other plot, and planting a Tree there destroys grass mid-growth. With adjacent
  plots that is roughly 1 position in 24, which looks too small to explain 16% —
  but it is measurable with the 023 probe and has not been measured.
- **Growth not actually overlapping.** The premise is that plot B ripens while
  the drone works plot A. If ripening is slower than assumed, the drone arrives
  at B unripe, skips, and pays the movement for nothing.
- **The reroll interacting with alternation.** 020's reroll runs per harvest and
  resets the growth clock; with two plots that may land differently.

The instrumented driver from 025/026 would answer all three in one run: it
already reports work, wait and arrival class per pass.
