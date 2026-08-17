# exp-003 — 4x4 grid sort + full cascade harvest

**Hypothesis.** 002 found harvest yield = `32 * n**2` (n = cascade
size), independent of individual cactus sizes — and `32 * 8**2 = 32 *
64 = 131,072`, exactly `Cactus_Single`'s target (Leaderboard.md: success
condition `Items.Cactus >= 131072`). This strongly implies the intended
design is: build one fully-sorted 8x8 grid of cacti, harvest one corner,
done in a single harvest. Sorting requires only `swap()` between
adjacent tiles (002: sizes are randomly fixed at maturity, never
converge by waiting — a real sort is unavoidable). A classical lemma
makes this tractable without a full shearsort: **sorting every row, then
sorting every column, of a matrix leaves the rows still sorted** — so
one row-bubble-sort pass over every row followed by one column-bubble-
sort pass over every column is provably sufficient to make the whole
grid sorted in both dimensions simultaneously (exactly Cactus.md's
sorted-order condition, applied grid-wide). This validates that pipeline
end-to-end on a 4x4 sub-grid (n=16, expected yield `32 * 16**2 = 8,192`)
before committing the ticks to the full 8x8.

**Variable.** Single ungrouped cacti (001/002) → a 4x4 planted grid,
sorted via row-then-column adjacent-swap bubble sort, harvested as one
cascade.

**Metric.** Cascade yield (`Items.Cactus` gained from the one harvest,
expect 8,192), and total ticks for plant+sort+harvest (to extrapolate
the 8x8 real driver's cost before building it).

**Baseline.** 002: n=2 cascade, 128 gained (`32 * 2**2`).

**Procedure.**
1. Confirm `get_world_size()` for this category (carrots_single's was 8;
   don't assume it's the same here).
2. Till + plant a 4x4 block, boustrophedon movement.
3. Bubble-sort every row (West→East ascending, `measure()` +
   `measure(East)` + `swap(East)` as needed, `n-1` passes per row).
4. Bubble-sort every column (South→North ascending, same pattern with
   `North`).
5. Harvest one corner; read `Items.Cactus` gained and total ticks.

**Falsifier.** If the gained amount isn't exactly `32 * 16 = 512`... 
wait: `32 * n**2` with n=16 is `32 * 256 = 8,192` — if the real gain
differs from this, the row-then-column lemma didn't fully sort the grid
(a bug in the sort, not the formula, since 002 already confirmed the
formula on n=2) — check for a partial cascade (a smaller n actually
harvested) rather than assuming the formula itself is wrong.
