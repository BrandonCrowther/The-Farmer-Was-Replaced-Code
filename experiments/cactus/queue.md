# Cactus — experiment queue

Target: **33_554_432 cacti**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Cactus, "main", 5000)`

Branches: `auto_experiment/cactus/NNN` · Results: `experiments/cactus/NNN/result.md`

## The mechanic

Same cascade mechanic as cactus_single (see that category's queue.md
for the full derivation): harvesting a fully-grown, sorted n-cactus
region yields `32 * n**2` (32 from `num_unlocked(Unlocks.Cactus)`, same
save state). This category's world is **32x32** (confirmed via probe,
bigger than the 8x8 single-drone farms), and `32 * 1024**2 =
33,554,432` — exactly the target. One fully-sorted 32x32 grid,
harvested once, completes the whole run in a single cascade.

The seeded achievement code (`Cactus_Achievement.py`) already
implements this correctly: up to 32 drones spawn recursively, one per
row for a parallel row-sort pass, then one per column for a parallel
column-sort pass (selection sort + physical `move_item` dragging,
proven correct by 001's first-try 100% success rate across 119 internal
repeats) — this is the same row-then-column lemma cactus_single
validated independently. It only needed the endless `while True:` loop
replaced with a single execution to ever terminate.

## Queued

- [ ] 002 faster-sort — leader is 7.8x faster (00:07.800 vs 001's
      01:00.697). The seeded selection sort does an O(n) linear search
      per rank plus an O(distance) physical drag — likely the same
      class of win cactus_single found swapping bubble sort for
      insertion sort (O(n+inversions) instead of O(n²)) would apply
      here too, per-row/per-column, before assuming the gap is
      structural.

## Done

- [x] 001 terminate — **adopted, first-ever score.** Seeded selection-
      sort grid algorithm worked correctly on the first real attempt,
      no bugs. Real scored run: **01:00.697, Global Rank #961**,
      33,554,432/33,554,432 on all 119 internal repeats (100%
      reliability). `experiments/cactus/001/result.md`
