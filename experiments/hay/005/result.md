# exp-005 — use-shared-helper — result

**Outcome.** adopted — champion unchanged, duplication removed

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:40.911** | identical to 004, to the millisecond |

**Baseline.** 03:40.911 · **Variant.** 03:40.911 · **Delta.** **0.000 s**

**Warning histogram.**

| warning | 004 | 005 |
| --- | --- | --- |
| Didn't have the required items to plant `Entities.Carrot` | 987 | 997 |
| Tried to use `Items.Water` but didn't have enough of it | 931 | 936 |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 10 | 9 |

**Verdict.** Confirmed: the shared helper is behaviourally identical, hay's local
override is gone, and the fix now lives in the one place all nine categories
read.

**One thing to watch.** A tie to the millisecond is a stronger coincidence than
this experiment needed. The warning counts differ across the two runs, so these
were genuinely different executions with different random outcomes that happened
to average to the same number — believable, since each score is already a mean
over roughly 33 repeats inside the leaderboard's 2-hour window, and Hay's
measured spread is only 0.15 s.

Believable, but worth a tripwire: **if the next variant also returns exactly
03:40.911, the score is not responding to the code**, and that is a measurement
fault to debug rather than a result to record. Check `DEPLOYED=` and the harness
window text in the screenshot before trusting any further number.
