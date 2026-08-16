# exp-008 — plot-rotation — result

**Outcome.** rejected, emphatically

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **3:38:11.132** | three hours thirty-eight minutes — note the format |

**Baseline.** 03:40.911 (mm:ss) · **Variant.** 3:38:11.132 (h:mm:ss) ·
**Delta.** **~59x slower**

The modal switches from `mm:ss.mmm` to `h:mm:ss.mmm` when a run passes an hour.
Worth knowing before misreading a future result as a 2-second regression.

**Warning histogram.** Only `Tried to use Items.Water` (32, down from 945) — the
carrot warnings vanish because there is no polyculture to request companions.

**Verdict: the hypothesis was wrong, and it was wrong for a reason worth
recording.**

exp-007 measured that `can_harvest()` was False on 94.1% of passes and I read
that as "drones are growth-bound". **It does not say that.** It is the
*frequency* of arriving early, not the *duration* spent waiting. A drone can
arrive early nineteen passes in twenty and still lose only a handful of ticks
each time, which is a rounding error rather than a bottleneck. I inferred a time
budget from a statistic that never measured time.

Acting on it cost two ways at once:

1. **The 5x polyculture multiplier was dropped** to "isolate the variable". On a
   yield-bound farm that alone is close to a 5x regression.
2. **A 25-tile circuit was added.** Every tile now costs the walk to reach it,
   and the old loop's "wasted" wait was cheaper than the movement that replaced
   it.

Isolating the variable was itself the mistake: polyculture was not a confound to
be removed, it was most of the yield.

**What to do instead.** Measure the wait properly. `get_tick_count()` costs 0
ticks, so wrapping the champion's busy-wait in it gives the actual share of ticks
spent idle rather than the share of passes that begin idle. If that number is
small, the whole idle-time line of attack is dead and the queue should go back to
yield per harvest. Queued as 013.
