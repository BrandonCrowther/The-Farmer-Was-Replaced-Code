# exp-006 — finish-and-score (8x8, insertion sort)

**Hypothesis.** 005 validated insertion-sort-via-adjacent-swap at 4x4
(exact `32*16**2=8192` match, `SORT_TICKS` 20,059 vs 003's bubble-sort
34,852 — 42% fewer). Swapping 004's bubble sort for insertion sort on
the real 8x8 grid should cut the real average total ticks (004: ≈329k)
by a comparable fraction, improving on 004's real score of 00:54.267 /
Global Rank #350.

**Variable.** 004's bubble sort (full row/column re-walk per pass) →
005's insertion sort (single forward walk, backward-correct on each
inversion) — same setup and cascade-harvest logic otherwise.

**Metric.** The completion modal's displayed time and global rank,
compared to 004's 00:54.267 / #350.

**Baseline.** 004: real score, 00:54.267, Global Rank #350, real
average ≈329,568 ticks/run.

**Procedure.**
1. `saves/cactus_single/main.py`: 004's 8x8 setup (boustrophedon
   planting) + 005's insertion_row/insertion_col in place of
   bubble_row/bubble_col.
2. `tools/cycle.sh cactus_single exp-cactus_single-006-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line, compare average ticks to 004's.

**Falsifier.** If `GAINED` isn't exactly 131,072 every time, the
insertion-sort implementation has a bug at this scale that the 4x4
validation didn't surface — check for it before assuming the algorithm
itself is unsound (005 already proved it correct at 4x4).
