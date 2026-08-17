# exp-007 — single-tile-long-run — result

**Outcome.** adopted — this is the design for 008. Confirms 006's wood
mechanism on a single tile and gives a real steady-state number, better than
any prior estimate.

**Numbers.** 200 cycles, 15,963,648 hay, 344,561 ticks, 56.72s.
`HITS` 50, `SAT` 145, `UNAFFORD` 5 (all in the first ~10 cycles, before wood
accumulated), `CARROT_SEEN` 78, `CARROT_AFFORDED` 50 — **every Carrot
request from cycle ~25 onward was affordable.** `WOOD` reached **2,221,568**
by the end, first going nonzero at cycle 15 (512) and crossing 81,000 by
cycle 25.

**Wood accumulates on a single tile too**, and slightly *faster* in wall
terms than 006's 2-tile run (nonzero by cycle 15 vs 006's ~cycle 20) —
006's worry that it might need multiple distinct companion positions to fire
doesn't hold; one tile's own churn is enough.

**Throughput, not ticks/harvest alone, is the number that matters.**
Steady-state ticks/harvest (tail window, cycles 100-195) is **≈1,568-1,639**
— *higher* than 002's ~1,469, not lower: once Carrot is affordable, the
drone pays a real walk for it too instead of skipping it for free, so nearly
every miss now costs a real trip. But the yield per harvest went from a
blended ~54,784 (002: 2/3 at 81,920, 1/3 at bare 512) to ~81,700+ (near
every harvest multiplied, net of Carrot's own 512-hay planting cost) — a
~49% yield increase that swamps the ~7-12% tick-cost increase.

**Net: whole-run throughput improved 18%** — 46.33 hay/tick overall
(15,963,648/344,561) vs. 002's 39.24 hay/tick (3,459,584/88,164). Steady-
state (tail window) throughput is even better: **≈49.9 hay/tick.**

**Corrected projection to 100,000,000:** at 49.9 hay/tick steady state,
`100,000,000 / 49.9 ≈ 2,004,800` ticks → at ~6,070 ticks/s, **≈330s ≈
05:30** — down from 002's naive ~6:59 extrapolation. Still **≈2.4x slower
than the leader's 02:17.995**, not a record, but a real, measured
improvement over every earlier estimate in this queue, simply from letting
the run go long enough for the mechanic 003 didn't know about.

**Baseline.** 002 (39.24 hay/tick, ~7:00 projected). 006 (2-tile, worse
throughput despite the same wood mechanism, due to commute tax).

**Noise floor.** Not established (single run). The tail window (95 cycles)
is a reasonable steady-state sample, but a second run would be worth taking
before quoting 05:30 as more than an estimate.

**Screenshots.** None — probe.

**Verdict.** This is the design: single tile, reactive skip-and-remember,
no dedicated wood investment needed — wood arrives for free from ordinary
companion churn and Carrot stops being a structural loss once it does. 008
should build the real terminating driver from this exact logic and run it
to the actual 100,000,000 target, reporting whatever real time it gets
rather than continuing to refine the estimate further.
