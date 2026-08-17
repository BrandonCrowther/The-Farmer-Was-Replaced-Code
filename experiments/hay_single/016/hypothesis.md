# exp-016 — port Hay(multi)'s two-tile champion, corrected auto-regrow cost

**Hypothesis.** 012's paused "proven ceiling" (011's reroll-only
asymptote, R=400 reroll cost) rests on the same stale assumption
Hay(multi)'s exp-066 corrected: Grass auto-regrows ("Grass grows
automatically on grassland", `Grass.md`) — an entity property, not
specific to Hay(multi)'s world size or drone count. `hay_single`'s
champion also calls `instructions()` (a guarded `plant(Grass)`) right
after every harvest assuming a 200-tick replant. If the correction
transfers, the real reroll cost here is ~207, not 400, and — since this
category is single-drone — the two-tile interleaving trick (hide the
growth wait behind a sibling tile's reroll-chase) needs no macro-layout
work at all, just two tiles the one drone can reach.

**Variable.** 012 (single-tile, `REROLL_LIMIT=5`, walk-on-miss after
exhausting rerolls) → two-tile interleaving, all-static-bush companion
policy, water threshold 0.75, direct `move()` — the exact design
ported from Hay(multi)'s exp-073.

**Metric.** The completion modal's displayed time and global rank,
compared to 012's 03:57.198 / #169.

**Baseline.** 012: 03:57.198, #169.

**Procedure.**
1. Confirm the auto-regrow correction transfers: measure
   `instructions()` cost directly in `hay_single`'s own 8x8/single-
   drone context (not assumed from Hay-multi).
2. Port 073's design: two tiles at distance 1 (the drone's own start
   position and the tile east of it), every position within distance 3
   of either pre-seeded once as permanent Bush (excluding both crop
   tiles), water threshold 0.75, direct `move()` for the known
   single-hop.
3. **Validation pass first**: reduced target (100,000, not
   100,000,000), no `zzRunner.py`, explicit check that both crop tiles
   are still `Entities.Grass` after a full run (self-collision is the
   failure mode here, not neighbor-collision, since there's only one
   drone).
4. Only after that passed clean: restored `TARGET = 100_000_000` and
   `zzRunner.py`, ran the real scored attempt.

**Falsifier.** If the real run scores worse than 012, either the
correction doesn't transfer as cleanly as measured, or something about
the 8x8 world (vs Hay-multi's 32x32) breaks an assumption the design
depends on.
