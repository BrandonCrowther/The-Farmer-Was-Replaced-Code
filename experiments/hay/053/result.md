# exp-053 — reroll away from distance-3 draws too, not just Carrot — result

**Outcome.** rejected — small regression.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `HITS_SKIP` 60/150 (40%), `HITS_WALK` 90/150 | skip rate up slightly vs 047's 36.7% baseline |
| r1 | `TICKS_PER_HARVEST` 1,482.65 | vs 047's 1,390 baseline |

**Baseline.** 047: 1,390 ticks/harvest.

**Variant.** Reroll on (Carrot OR distance==3), `REROLL_LIMIT=2`.
**Delta.** +6.7% (regression).

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** By cell-count, distance 1/2/3 cover 4/8/12 of the 24
candidate cells — so `distance==3` alone triggers on roughly half of
all draws, and combined with Carrot the total trigger rate is ≈2/3.
`REROLL_LIMIT=2` (3 total draws) isn't enough attempts to reliably
escape at that trigger rate, so many cycles pay the extra reroll cost
without ever landing a cheap draw. 054 tests a wider trigger with a
higher limit to see if the underlying idea can be made to pay off with
better-tuned parameters.
