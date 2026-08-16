# exp-013 — companion-map — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:05.789** | PB; rank **#178**, up from #230 |

**Baseline.** 03:24.327 · **Variant.** 03:05.789 · **Delta.** **−18.538 s (−9.1%)**

**Noise floor.** 0.15 s. The win is ~124x the floor.

**Verdict.** Remembering what you planted beats walking to find out. The
contention risk was real but did not dominate: overlapping neighbourhoods make
some entries stale, and each stale entry costs a multiplier — but the trips saved
outweigh them comfortably. The conservative construction is doing work here: the
map only ever causes a *skip*, only ever holds this drone's own plantings, and
any pass that does walk re-verifies with `get_entity_type()`.

**A prediction that was wrong, recorded because it was wrong.** Mid-run the HUD
showed 342M hay and what looked like a 4:02 clock, and that was read as the map
failing. It was a misread — the overlapping glyphs were the carrot counter, not
the run timer. The lesson is narrow and practical: **the HUD crop overlaps the
run clock and is not safe to read mid-run.** Wait for the modal.

**The measurement that matters more than this win.**

```
FARM world 32 max_drones 32
```

**The cap is 32 drones and the seeded grid attempts 36.** The spawn loop is 6x6
with the origin skipped — 35 spawns plus the main drone — so four calls return
`None` on every run and four grid positions have never been farmed at all. The
`if d:` guard means this has been silently true since 001.

Two consequences:

1. **The farm is 32x32 = 1024 tiles with a hard cap of 32 drones.** More drones
   is not a route to anything; we have been at the cap all along. The remaining
   4x gap to the leader must come from fewer ticks per multiplied harvest, not
   from more parallelism.
2. **The layout should be built for exactly 32 drones**, not 36-minus-whatever-
   fails. Four unmanned positions is four wasted plots. Queued as 014.
