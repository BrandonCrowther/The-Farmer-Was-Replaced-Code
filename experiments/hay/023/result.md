# exp-023 — measure-preplanted — result

**Outcome.** diagnostic — the 021 explanation is wrong, and a real bug surfaces

**Arrivals, one drone, 32,727 companion events.**

| outcome | count | share |
| --- | --- | --- |
| `mismatch_own` — had a record, tile now differs | 16,342 | 49.9% |
| `skip_own_record` — map hit, no walk at all | 14,748 | 45.1% |
| `mismatch_new` — no record | 964 | 2.9% |
| `match_stale_own` | 629 | 1.9% |
| **`match_neighbour`** — neighbour had stocked it | **44** | **0.13%** |

**"Contention is cooperation" is dead.** A neighbour has pre-stocked the
requested tile on one arrival in 750. There was never any shared infrastructure
to lose, so it cannot be why the disjoint lattice was slower. 021 invented a
mechanism that fitted the number and then wrote it up; this is what that costs.

**What the data does say.** The map earns its keep — 45% of companion requests
are served without moving at all. And the 50% `mismatch_own` is not neighbour
interference: it is the *same tile requested with a different type*, since the
preference rerolls every pass and a tile we stocked with Tree gets asked for Bush
next time.

**The likely real cause of 021 and 022: a broken assumption of mine.** "Companion
requests never cross the seam" was established for the **champion** layout, whose
drones sit at 3..28 on a 32-wide farm — from x=3 the range bottoms out at 0, from
x=28 it tops out at 31, so no request wraps. Both 021 and 022 placed drones on
**x=0 and y=0**, whose companions land at 31, across the wrap. `Common.move_to`
walks the direct path, so that is **31 moves east instead of 1 west — 6,200 ticks
instead of 200.**

The doses match the damage: 021 put ~7 of 32 drones on a zero edge and lost
15.9%; 022 put ~11 of 32 and lost 36.6%.

`move_to_wrapped` has been sitting in `Common` since 015, deliberately kept off
the hot path *because the champion layout never needs it*. That reasoning was
correct and then silently expired the moment the layout changed. Retested as 024.
