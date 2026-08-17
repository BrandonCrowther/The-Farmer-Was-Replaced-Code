# exp-005 — insertion-sort validation (4x4)

**Hypothesis.** 004's naive bubble sort walks the *entire* row/column on
every pass regardless of how many real inversions exist, costing
O(n) work per pass for up to `n-1` passes — O(n²) total step-visits
(56/row for n=8) even when the real number of out-of-order adjacent
pairs (inversions) is much smaller (for 8 cells drawn from 10 values,
expected inversions ≈12.6/row, not 56). Insertion sort implemented via
adjacent swaps (walk forward once; on finding an inversion, swap and
walk backward correcting until in order, then resume forward) does
work proportional to n + inversions instead — the minimum possible for
an adjacent-swap sort, since sorting by adjacent transposition always
costs exactly the inversion count. This should cut sort ticks
substantially versus 004's ≈290k average.

**Variable.** 004's full-pass bubble sort (with early exit per pass) →
insertion sort (single forward scan, backward-correct on each
inversion).

**Metric.** `SORT_TICKS` on the same 4x4 grid 003 used, compared to
003's 34,852 (which used bubble sort, no early exit even — this run
adds the fairer baseline by comparing formula match first, ticks
second).

**Baseline.** 003: 4x4 bubble sort, `SORT_TICKS` 34,852, exact
`32*16**2=8192` yield.

**Procedure.**
1. `saves/cactus_single/main.py`: same 4x4 setup as 003, but sort with
   insertion-sort-via-adjacent-swap instead of bubble sort.
2. `tools/cycle.sh cactus_single exp-cactus_single-005-r1 --from <worktree>`.
3. Read `OUTPUT=`; confirm `GAINED` still hits the exact formula value,
   compare `SORT_TICKS` to 003's baseline.

**Falsifier.** If `GAINED` doesn't hit 8192 exactly, the insertion-sort
implementation has a bug (e.g. the backward-correction loop not fully
draining, or losing track of position) — the row-then-column lemma
itself is already proven by 003, so a mismatch here means a coding bug
in this experiment, not a broken theory.
