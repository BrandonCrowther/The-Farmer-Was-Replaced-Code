# exp-055 — tight packing (spacing 4) + distance-biased reroll, combined

**Hypothesis.** 051 (spacing 4 alone) regressed (2,347 vs 1,390) —
attributed to thrashing (neighbors overwriting each other's companion
tiles with conflicting needs). 054 (distance>=2 reroll alone, spacing
5) also regressed (2,087 vs 1,390) — the cheap-distance draws are too
rare (1/6 by cell count) for the reroll cost to pay for itself. Neither
alone works, but the user's combined idea is structurally different
from either: pack drones tighter (spacing 4, more footprint overlap)
*and* bias every companion draw toward the near, densely-shared zone
(reroll away from distance>=2). This should increase how often a
drone's OWN close-in draw lands on a position a *neighbor* already
serviced (raising the physical "already correct" skip rate — 047's
neighbor-cooperation effect, seen at 3/95 walks with spacing 5) rather
than fighting over far-flung, less-overlapping territory.

**Variable.** Both 051's spacing-4 layout AND 054's (Carrot OR
distance>=2) reroll trigger, `REROLL_LIMIT=5`, combined in one variant.

**Metric.** `TICKS_PER_HARVEST` and skip/walk split over a 150-cycle
bounded probe, same instrumentation as 047/049/051/053/054.

**Baseline.** 047 (spacing 5, no distance reroll): 1,390. 051 (spacing
4 alone): 2,347.27. 054 (distance-reroll alone, spacing 5): 2,087.08.

**Procedure.**
1. `saves/hay/main.py`: spacing 4 (051's grid) + (Carrot OR
   distance>=2) reroll trigger with `REROLL_LIMIT=5` (054's trigger).
2. `tools/cycle.sh hay exp-hay-055-r1 --from <worktree>`.
3. Compare to all three baselines above, and specifically check
   whether the *skip rate* (not just ticks/harvest) rises — that's the
   direct signal the mechanism is working even if the net tick cost is
   still unfavorable.

**Falsifier.** If skip rate doesn't rise noticeably above 047's 36.7%
baseline, physical neighbor cooperation isn't meaningfully densifiable
this way even combined — the two negatives don't cancel out into a
positive, and this family is closed for real.
