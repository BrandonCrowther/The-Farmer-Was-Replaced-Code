# exp-027 — multi-plot — result

**Outcome.** rejected

**Numbers.**

| run | metric | note |
| --- | --- | --- |
|  1  | **03:37.380** | vs a champion mean of 02:50.405 |

**Delta.** **+46.975 s (+27.6%)**, which is 19 sd — unambiguous.

**Verdict.** Four plots per drone costs more than the idling it removes. A lap of
the 2x2 block is four moves at 200 ticks — 800 ticks — and only some plots are
ripe on any given lap, so the drone often pays the full circuit for one harvest.
The 437 ticks of waiting it was meant to reclaim are cheaper than the movement
that replaced them.

The reasoning behind it still looks sound: 026 measured that 45% of passes do 26
ticks of work and then wait 437, which is ~21% of drone time idle. The error was
in the remedy. Walking four tiles to find one ripe plant is not how to use that
time; the drone needs work that does not require travelling to discover whether
it exists.

**Worth retrying at two plots rather than four** — one move between them, so the
overhead is 200 ticks against 437 of waiting — before concluding the idea is dead.

**This run also surfaced something much more important.** Its modal showed a
personal best of 02:47.682, set by exp-023, which no one had looked at because
diagnostics were read for their telemetry and their modal times were ignored.
Three champion-equivalent runs — 02:47.682, 02:51.263, 02:52.271 — give a
standard deviation of **2.41 s**, not the 0.15 s inherited from exp-002 and used
ever since. See the corrections stamped on 012, 014 and 017.
