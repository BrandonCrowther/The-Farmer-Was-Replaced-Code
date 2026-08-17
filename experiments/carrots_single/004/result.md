# exp-004 — multi-tile-pipeline — result

**Outcome.** **adopted — a large, real win**, close to the model's
prediction, confirming the growth-schedulability read from 003.

**Numbers.** 60 cycles (20 full rounds across 3 tiles), all multiplied.
`HITS_GRASS` 24/60 (40%, somewhat above the naive 1/3 — small-sample
noise, or the pooled 3-tile companion traffic sampling slightly
differently; not concerning). `HITS_SERVICED` 36/60. **`HITS_GUARD` 0/60
— zero self-collisions**, exactly as the distance-4 spacing (all pairwise
outside the ≤3 companion range) predicted by construction, not luck.

**`TICKS_PER_HARVEST` = 3,430.43** — very close to the model's predicted
plateau (≈3,222; the ~6% gap is plausibly real average commute running
slightly above the assumed 800, or minor per-cycle overhead not in the
model). **≈23.88 carrots/tick.**

**Baseline.** 003: single tile, real ≈8,362 ticks/harvest, ≈9.80
carrots/tick.

**Delta.** **−59.0% ticks/harvest, 2.44x throughput.** Projected full-run
time: `1,221 × 3,430.43 ≈ 4,188,555` ticks → **≈690s ≈ 11.5 minutes** — down
from 003's single-tile projection of ≈28.0 minutes.

**Noise floor.** Not established (single 60-cycle run), but the model
agreement (predicted ≈3,222, measured 3,430) is close enough that this
isn't a fluke — worth a second sample before finalizing, not before
adopting.

**Screenshots.** None — probe.

**Verdict.** The growth-bound hypothesis from 003 holds up exactly as
predicted: 3 tiles, spaced to make self-collision structurally impossible
rather than merely unlikely, nearly triples throughput by filling idle
time that was previously wasted. This is the **first category tonight
where multi-tile is a real, adopted win** — hay_single had no idle time to
exploit (four independent closures), Hay had idle time but not enough for
even one extra tile (044). 005 should build the real terminating driver
from this design and run it for an actual score — the first ever for this
category.
