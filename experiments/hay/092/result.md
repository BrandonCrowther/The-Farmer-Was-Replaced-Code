# exp-092 — water-tank contention at launch — result

**Outcome.** **Confirmed real, but small and transient — closed, no
code change.** The user's observation was correct (there genuinely is
contention, visually confirmed live via a captured screenshot showing
the warning firing mid-run next to a fully-grown, 0-water Bush), but
the measured cost is a one-time, self-resolving transient concentrated
in a single early iteration, not a sustained or recurring problem —
and it's small in absolute terms.

**Numbers** (sandboxed `simulate()` probe, 26 iterations/drone, all
32 drones, `sim_items={}`):

| iteration | wait mean | wait max | fails | pool min-max |
| --- | --- | --- | --- | --- |
| 0-2 | 4.0 (baseline) | 4 | 0 | 0-130 |
| **3** | **12.1** | **242** | **1** | 0-98 |
| 4-26 | 4.0 (baseline) | 4 | 0 | 0→60, recovering |

Only iteration 3, out of 26 measured, shows any deviation from
baseline — 2 of 607 total drone-iteration samples (0.3%) had elevated
wait (242 and 24 ticks), and exactly 1 of 257 water-use attempts
failed. Total excess wait across the whole sample: **258 ticks**. Pool
size dips toward 0 in the first ~14 iterations, then recovers
steadily (5→60) as fewer drones remain in the sampled window and
passive regen (1 tank/10s + upgrades) catches up — a genuine one-time
transient, not a recurring drain, matching the shape of 089's own
burst-catch-up finding (which measured the *typical* cost; this
measures the *tail risk* of an unlucky drone during the same window).

**Real run's `WARN` count (2121) is larger than what this sample
extrapolates to** — an open, acknowledged gap. Even taking the real
`WARN=2121` count at face value and assuming every single one costs
the documented failed-`use_item()` price (1 tick, `docs/api/
__builtins__.py`), that's **~2,121 ticks total, fleet-wide, across
the entire run** — negligible next to this session's real wins (091
alone was -0.992s ≈ several thousand ticks per drone). The gap between
the sample and the real count is most likely because the sandbox's
exact starting water amount doesn't precisely match a real
`leaderboard_run()`'s (undocumented exactly) starting conditions, but
the *scale* conclusion doesn't change either way: whether the real
cost is 258 ticks or 2,121, it's small relative to what's already been
found and adopted this session, and small relative to the risk 089
already established for touching water-management timing.

**Why this isn't worth building a fix for.** 089 already found that
`WATER_THRESHOLD=0.75` is correctly tuned — a lower threshold (which
would reduce launch contention by needing fewer tanks per catch-up)
costs *more* overall via a persistent steady-state idle penalty that a
short probe window couldn't see until extended. Any fix aimed at this
launch transient specifically (staggering catch-up timing, pre-topping
during setup) risks the same class of backfire for a cost that's
already confirmed small and bounded to a narrow window. Not a
promising trade.

**Verdict.** No code change. `record.json`/`queue.md` updated to close
092. Game verified restored to 091 (`live/main.py` hash
`415bfe1a45bf2adf01631a70f2dab7b0`, matches `saves/hay/main.py`).
