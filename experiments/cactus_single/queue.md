# Cactus_Single — experiment queue

Target: **131_072 cacti** on an 8x8 farm with a single drone
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Cactus_Single, "main", 5000)`

Branches: `auto_experiment/cactus_single/NNN` · Results: `experiments/cactus_single/NNN/result.md`

## The mechanic (nothing like the polyculture categories)

Cactus is **not** a polyculture crop (Polyculture.md only lists
Grass/Bush/Tree/Carrot) — it's Cactus.md's size/sort cascade instead:
cacti grow to a random size 0-9 (fixed once fully grown, never converges
by waiting — 001), and harvesting a fully-grown cactus whose neighbors
are also fully-grown and in "sorted order" (size non-decreasing to the
North and East) cascades the harvest recursively through the whole
connected sorted region, yielding `32 * n**2` `Items.Cactus` for an
n-cactus cascade (002, `32` being a flat multiplier — likely from
`num_unlocked(Unlocks.Cactus)` — independent of the actual sizes
involved). `32 * 8**2 = 131,072`, **exactly** the target: the category
is designed to be solved by building one fully-sorted 8x8 grid and
harvesting a single corner.

Sorting needs real `swap()`s (sizes don't converge), but a classical
lemma makes it cheap: **sorting every row of a matrix, then every
column, leaves the rows still sorted** — so one row-bubble-sort pass
over every row followed by one column-bubble-sort pass over every
column is provably sufficient to sort the whole grid in both dimensions
at once. No shearsort/snake pattern needed. Validated exactly at 4x4
(003, 8192 = `32*16**2`, first try) and at full 8x8 (004, 131,072/131,072
every single time across 133 internal repeats).

## Queued

- [ ] 007 tighter-movement — `move_to` re-queries position every call;
      the planting phase (~38k ticks) is now a much larger share of a
      smaller total. Leader is still 4.3x faster (00:07.447 vs 006's
      00:32.063) — real headroom remains.

## Done

- [x] 005 insertion-sort-validation (4x4) — **adopted the technique.**
      Insertion sort (single forward walk, backward-correct on each
      inversion — O(n+inversions) vs bubble sort's O(n²) full re-walk
      per pass) hit the exact `32*16**2=8192` formula match and cut
      `SORT_TICKS` 42.4% (20,059 vs 003's 34,852) on the same 4x4 grid.
      `experiments/cactus_single/005/result.md`.
- [x] 006 finish-and-score (insertion sort) — **adopted, new champion.**
      Real 8x8 insertion-sort driver, real scored run: **00:32.063,
      Global Rank #228** (up from #350), 131,072/131,072 on all 225
      internal repeats. Real average ticks −40.9% (194,688 vs 004's
      329,568), matching 005's 4x4 prediction closely.
      `experiments/cactus_single/006/result.md`.

- [x] 001 mechanics-probe — starting stockpile (Pumpkin 1B, Cactus costs
      64 Pumpkin), growth fixed at 5,876 ticks (zero variance), size
      fixed once fully grown (doesn't converge by waiting), lone harvest
      yields 32 (not 1). `experiments/cactus_single/001/result.md`
- [x] 002 resources-unlocks-yield-scaling — **found the formula**:
      `32 * n**2`, confirmed via a forced 2-cactus cascade (128 = 32*4).
      `32 * 64 = 131,072` matches the target exactly at n=64.
      `experiments/cactus_single/002/result.md`
- [x] 003 4x4-grid-sort-validation — **adopted**, exact formula match
      (8192 = 32*16**2) on the first try, validating the row-then-column
      bubble-sort lemma end-to-end before spending ticks on 8x8.
      `experiments/cactus_single/003/result.md`
- [x] 004 finish-and-score — **adopted, first-ever score.** 8x8 grid,
      real scored run: **00:54.267, Global Rank #350**, 131,072/131,072
      every one of 133 internal repeats (100% reliability).
      `experiments/cactus_single/004/result.md`
- [x] 005 insertion-sort-validation — adopted, 42.4% fewer sort ticks
      at 4x4. `experiments/cactus_single/005/result.md`
- [x] 006 finish-and-score (insertion sort) — adopted, new champion
      00:32.063, #228. `experiments/cactus_single/006/result.md`
