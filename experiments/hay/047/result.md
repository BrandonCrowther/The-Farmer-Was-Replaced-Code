# exp-047 — pinpoint the walk-servicing tick blowup — result

**Outcome.** probe — found and fixed a real bug in my own diagnostic,
not the champion.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 (buggy) | `MOVE_OUT` up to 12,913 ticks for `dist` up to 62 | looked like `Common.move_to` walking the long way around a 32-wide wrapped world |
| r1 (buggy, root cause) | `ax,ay` captured as the drone's un-moved starting position (0,0), not the champion's real home (3,3) | `Common.move_to(ax,ay)` was a no-op; all logged distances were relative to the wrong point |
| r2 (fixed) | `MOVE_OUT`/`MOVE_BACK` 225/433/641 ticks for `dist` 1/2/3 exactly (≈208×dist+17) | fully consistent with `move()`'s flat 200-tick cost, no blowup |
| r2 | 95 walks: 84 at `SVC_ACTION` 411 (Bush/Tree, no till), 8 at 611 (Carrot, +till), 3 at 3 (already-correct, free neighbor-cooperation hit) | matches expectations exactly |

**Baseline.** 046: real walk-rate 63%, skip-rate 37%.

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** The champion's real (3,3) home position (per the grid's
own spacing-5 design, minimum coordinate 3) never needs to cross the
world's wraparound seam within its ≤3 companion range — `Common.py`'s
own comment about this was right. The "blowup" was entirely a
diagnostic-script bug (measuring from the wrong origin), caught and
corrected before it could lead anywhere. No real bug found here; real
servicing costs are exactly as expected, no hidden inefficiency.
