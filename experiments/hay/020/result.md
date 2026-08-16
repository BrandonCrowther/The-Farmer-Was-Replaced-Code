# exp-020 — reroll-after-harvest — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **02:52.271** | PB; rank **#149**, up from #177 |

**Baseline.** 03:04.715 · **Variant.** 02:52.271 · **Delta.** **−12.444 s (−6.7%)**

**Noise floor.** 0.15 s. The win is 83x the floor.

**Warning histogram.**

| warning | 017 champion | 020 |
| --- | --- | --- |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 142 | **48** |
| Didn't have the required items to plant `Entities.Carrot` | — | 21 |
| Tried to use `Items.Water` but didn't have enough of it | 120 | 152 |

**Verdict.** The idea in 006 was right and its placement was wrong. Rerolling
before the harvest destroyed the multiplied harvest to pay for the reroll;
rerolling after it costs a single 200-tick plant on an already-empty tile and
throws away nothing.

This is the third time a rejected idea has come back and won once the mechanism
underneath it was measured rather than assumed — and it only happened because
019 established that the multiplier is 160x and that carrot specifically fails.
With the 67x figure and no per-companion breakdown, there was no reason to
revisit 006 at all.

**Still on the table.** 48 carrot plantings still fail, and `REROLL_LIMIT = 2`
leaves roughly (1/3)^3 ~= 4% of passes still holding a carrot request. Raising
the cap is cheap to test. The larger prize is making a carrot request
*satisfiable* rather than rerolling away from it — see 021.
