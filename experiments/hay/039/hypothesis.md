# exp-039 — drone-tick-profile

**Context.** exp-038's baseline/variant screenshots surfaced something
Hay's own record.json never stated: the real leader (`const arch *`) is
at **00:58.549** — nearly 3x faster than our 02:47-02:52, a much larger gap
than anything in the existing 001-038 trail addressed. Before designing
around that gap, measure this category's real per-drone economics with the
same rigor hay_single got tonight, rather than reasoning from the
approximate figures ("~967 ticks/pass", "~330 the leader implies" from old
queue text) that were themselves estimates, not direct measurements.

**Hypothesis.** The real tick rate and per-harvest cost for the main
drone, measured directly, will let the leader's 58.549s be converted into
an implied ticks/harvest-per-drone figure that can be compared against our
own champion's real number — the same kind of arithmetic 001 did for
hay_single, not yet done for Hay itself.

**Variable.** None — 020's exact champion logic, unchanged, with a
`quick_print` every 25 harvests on the main drone only (harmless, 0-tick
per Timing.md, so this scores identically to 020/038's baseline).

**Metric.** `PROFILE` lines' tick deltas per harvest for the main drone,
plus the real scored time (confirms this instrumented run still performs
like 020).

**Baseline.** 020/038-baseline: fresh-conditions 02:52.338. Leader:
00:58.549.

**Procedure.**
1. `saves/hay/main.py`: 020's logic + profiling on the (3,3) drone.
2. `tools/cycle.sh hay exp-hay-039-r1 --from <worktree>` (background —
   real scored run, same shape as 038's baseline).
3. Read `OUTPUT=`; compute per-drone ticks/harvest, and use it plus the
   measured tick rate to work out what the leader's pace implies about
   *their* design (companion-servicing efficiency vs. something else
   entirely).

**Falsifier.** None specific — this is measurement, feeding the next
design question rather than testing one itself.
