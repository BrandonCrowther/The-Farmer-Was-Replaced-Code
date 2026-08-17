# exp-073 — first real leaderboard run of the two-tile champion

**Hypothesis.** 070-072's single-drone smoke tests measured 923.53
ticks/harvest for the two-tile interleaving design (water=0.75, direct
move, all-static-bush companion policy) — a real, attributable ~13.5%
improvement over the single-tile champion's measured ~1068-1220. If
that translates to the real 32-drone leaderboard run, the score should
improve meaningfully from 02:42.421/#111.

**Variable.** Single-tile-per-drone champion (057) → two-tile-per-drone
champion, full 32-drone macro-layout. Each drone owns two adjacent Hay
tiles (base, base+East), round-robining between them; every position
within distance 3 of either tile pre-seeded once as permanent Bush.

**Metric.** The completion modal's displayed time and global rank,
compared to 057's 02:42.421 / #111.

**Baseline.** 057 (current champion): 02:42.421, #111.

**Procedure.**
1. `saves/hay/main.py`: multi-drone two-tile design, reusing the
   champion's existing 6x6/spacing-5/HOLES macro-grid so drone
   placement didn't need to be redesigned from scratch. Each drone's
   second tile is `base + (1, 0)`. A global `ALL_CROPS` set (every
   drone's two tiles, computed once at module scope before any
   spawning) is checked by *every* drone's setup loop, not just its
   own — geometry alone (a 1-tile margin at 5-spacing) was judged too
   tight to trust without a second, independent safety check.
2. **Validation pass first, not a blind real run**: deployed a
   TARGET-reduced copy (200,000, not 2,000,000,000) with `zzRunner.py`
   removed so nothing could trigger a real scored attempt, plus an
   explicit post-run check that walks all 64 crop-tile positions and
   confirms every one is still `Entities.Grass` (common failure mode
   being guarded against: one drone's bush-wall setup bulldozing a
   neighbor's actual crop). Real, not simulated — same live save, same
   real game mechanics, just a cheap target and no scoring path.
3. Only after that passed clean: restored `TARGET = 2_000_000_000` and
   `zzRunner.py`, ran the real scored attempt via `tools/cycle.sh`.

**Falsifier.** If the real 32-drone run scores worse than 057, either
the single-drone smoke tests don't generalize to the full macro-layout
(e.g. concurrency effects between 32 drones not present with one), or
the crop-tile safety check missed something the validation pass didn't
catch.
