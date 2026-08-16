# exp-034 — growth-ceiling — result

**Outcome.** diagnostic — the ceiling is computable, and it says 32 single-tile
drones cannot reach the leader

**1. The farm is already fully watered.** Water level on the sampled tile:

| level | samples |
| --- | --- |
| 1.00 | 5,861 |
| 0.99 | 5,079 |
| 0.98 | 622 |
| <0.98 | 68 |

Watered and unwatered passes were indistinguishable — 1181 vs 1192 ticks — because
water persists between passes at 1% decay a second, so a pass that skips watering
still starts at 0.97. **The "farm is 10x water-starved" arithmetic in 016/017 was
wrong**, and water is not a lever: growth already runs at ~5x.

**2. The tick rate is 6,074.7 ticks/second**, measured from `get_time()` against
`get_tick_count()`. This is what makes the ceiling computable at all — the wiki
prices water per second while everything else here is in ticks.

**3. The ceiling.**

```
harvests needed        2e9 / 81,920      = 24,414        (763 per drone across 32)
growth per tile        ~1,018 ticks       [INFERENCE, see below]
floor, 32 tiles        763 x 1,018        = 776,672 ticks = 2:07.9
champion today         172.3 s            = 1,046,792 ticks
leader                 58.5 s             = 355,668 ticks
```

**The leader is below the floor for 32 single-tile drones.** No routing
improvement can close that: 32 tiles cannot produce 24,414 harvests faster than
2:07.9 if each tile needs ~1,018 ticks to regrow.

Working backwards, the leader implies **~70 productive tiles — 2.2 per drone — at
466 ticks of work per harvest.**

**What that means for multi-plot.** 027 (four plots, +47 s) and 029 (two plots,
+28 s) were not wrong in principle; they were premature. A second tile only pays
if the drone can service both inside one growth period:

```
2 x work <= growth   ->   work <= ~509 ticks
```

Work today is 822. From 026's census — 52% of passes walk-and-replant at 1,455
ticks, 45% skip at 26 — the mean falls below 509 once the **skip rate reaches
~66%**, against 45% today.

**So the order is: raise the skip rate first, then add the second plot.** Doing
it the other way round is what made 029 look like a failed idea.

**And 033 supplies the mechanism.** `get_companion()` rerolls on every call and a
call costs **1 tick**. Every reroll so far has replanted the tile at 200 ticks to
get a fresh request — when simply asking again is 200x cheaper. Queued as 035.

**Inference flagged.** The 1,018 tick growth figure is derived from 026's pass
structure (work 822 + wait 196), not observed directly: this probe's `growticks`
spans the whole pass, so it measures pass duration, not growth. A drone that
harvests and then waits with no work in between would measure it directly, under
real farm conditions. That is worth doing before the ceiling number is trusted to
three digits.
