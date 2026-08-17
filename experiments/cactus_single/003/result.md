# exp-003 — 4x4 grid sort + full cascade harvest — result

**Outcome.** adopted — validates the whole design end-to-end, first try,
no bugs.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `GAINED` 8192 (predicted `32 * 16**2 = 8192`), `WORLD_SIZE` 8 | exact match |
| r1 | `SETUP_TICKS` 11530, `GROWTH_WAIT_TICKS` 5876, `SORT_TICKS` 34852, `TOTAL_TICKS` 53685 | 16-cell grid, naive full `n-1`-pass bubble sort (no early exit) |

**Baseline.** 002: n=2 cascade, 128 gained (formula prediction: exact).
**Variant.** n=16 cascade, 8192 gained. **Delta.** Formula holds exactly
at a second, much larger scale — the row-then-column bubble-sort lemma
(sorting columns of a row-sorted matrix leaves the rows sorted) fully
sorts the grid in one row pass + one column pass, no shearsort/snake
pattern needed, confirmed by the full-cascade yield (a partial cascade
would have under-shot 8192).

**Noise floor.** Not applicable — a formula match this exact isn't
noise.

**Screenshots.** None — probe.

**Verdict.** The design is validated: plant a full grid, bubble-sort
every row then every column (adjacent `measure()`/`swap()`, no
shearsort needed), harvest one corner for `32 * n**2`. Extrapolating to
the full 8x8 (n=64, 4x the cells, ~10.9x the sort inner-loop work per
the row/col/pass/step scaling): setup ≈4x ≈46,000 ticks, one growth wait
≈5,876, sort ≈34,852 × ~10.9 ≈380,000 ticks (naive, no early exit),
harvest 200 — projecting a real total in the ballpark of ~430,000 ticks
(≈70-75s), which would land 32*64**2 = 131,072 -- exactly
Cactus_Single's target -- in a single cascade harvest. 004 builds the
real 8x8 driver, adding an early-exit flag to each bubble pass (stop
once a pass makes zero swaps) since most of the naive worst-case
`n-1` passes do no work once the array is already sorted.
