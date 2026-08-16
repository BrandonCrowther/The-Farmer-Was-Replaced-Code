# exp-022 — denser-spacing — result

**Outcome.** rejected — and together with 021 it brackets an optimum

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:55.341** | +63.070 s vs champion. `SPAWNED 32 of 32` |

**Baseline.** 02:52.271 · **Variant.** 03:55.341 · **Delta.** **+63.070 s (+36.6%)**

**Verdict.** Both directions lose:

| layout | min L1 separation | time | vs champion |
| --- | --- | --- | --- |
| 021 diamond lattice | 8 (disjoint) | 03:19.653 | +15.9% |
| **014 champion grid** | **5** | **02:52.271** | — |
| 022 dense grid | 4 | 03:55.341 | +36.6% |

Spacing 5 sits near an optimum, and the curve is steep on both sides. The
reading — still inference, and 023 is the measurement — is that sharing has two
opposing effects. Some overlap means neighbours pre-stock companion tiles, and
arriving to find the right plant already there skips a 400-tick
harvest-and-replant. Too much overlap means neighbours *overwrite* each other's
companions, so tiles are constantly wrong on arrival and every drone pays that
400 ticks anyway, plus its map is stale.

**A confound, recorded.** The dense grid used y in {0,4,8,12}, so it packed the
drones into half the farm as well as tightening the spacing — two changes in one
run. Density is the more plausible cause, since a drone farms only its own tile
and the rest of the map matters only as companion targets, but this run cannot
separate them.

**What is worth taking from 021 and 022 together.** Layout tuning is not where
the remaining 3x lives; the champion grid is already close to the best of a bad
family, and both departures cost more than any layout change has ever gained
(014's +0.466 s being the only layout win, now looking like noise). The next
design should remove the sharing question rather than tune it — which is the
monocrop proposal in 025.
