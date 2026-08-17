# exp-001 — terminate the seeded achievement driver

**Hypothesis.** The seeded `saves/cactus/main.py` (from
`Cactus_Achievement.py`) already implements exactly the row-then-column
sort lemma cactus_single validated tonight (sorting every row, then
every column, of a matrix leaves the rows still sorted), parallelized
across up to `max_drones()` drones — one per row for the row-sort pass,
one per column for the column-sort pass — via selection sort with
physical `move_item` dragging instead of adjacent swaps. If
`get_world_size()` and `num_unlocked(Unlocks.Cactus)` match
cactus_single's save state (world 32, unlock level 6 giving a 32x
cascade multiplier), then `32 * 32**2 * 32**2` — wait, precisely:
`32 * (world_size**2)**2`? No — `32 * n**2` where `n` = cells in the
full grid = `world_size**2`. `32 * 1024**2 = 33,554,432` — exactly this
category's target (confirmed via probe: `WORLD_SIZE 32`,
`CACTUS_UNLOCK 6`, `MAX_DRONES 32`). One full 32x32 grid, sorted and
harvested once, should complete the whole run in a single cascade — the
seed's `while True:` outer loop is unnecessary and is what's currently
blocking the run from ever terminating (queue.md's 001: "the seeded
driver is an endless while True achievement farmer").

**Variable.** Seeded `while True:` outer loop (never terminates, so
never scores) → run the row-sort + column-sort + harvest sequence
exactly once.

**Metric.** The completion modal's verdict and displayed time —
this category's first-ever leaderboard entry.

**Baseline.** None — first probe/score attempt for this category.
Probe: `WORLD_SIZE 32`, `CACTUS_UNLOCK 6`, `MAX_DRONES 32`,
`PUMPKIN 1,000,000,000`.

**Procedure.**
1. `saves/cactus/main.py`: keep the seeded `driver()`/`Cactus.py` logic
   unchanged, replace the outer `while True:` with a single execution
   (row-sort pass, wait for drones to reap, column-sort pass, wait,
   harvest, `quick_print` diagnostics).
2. `tools/cycle.sh cactus exp-cactus-001-r1 --from <worktree>` — no
   smaller-scale validation was practical here (the algorithm is tied
   to `get_world_size()`=32 directly, unlike the incrementally-testable
   cactus_single grid); ran the real scored attempt directly.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If the cascade doesn't harvest the full 33,554,432 (a
partial cascade, or a hang in `perform_sort`'s linear search for a
target value that's never found), the seeded selection-sort
implementation has a real bug — investigate `Cactus.py`'s
`perform_sort`/`move_item` before assuming the row-then-column lemma
itself doesn't apply at this scale (cactus_single already proved the
lemma independently, twice).
