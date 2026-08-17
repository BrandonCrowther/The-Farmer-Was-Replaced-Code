# exp-004 — finish-and-score (8x8 grid sort + single cascade)

**Hypothesis.** 003's design (plant a full grid, bubble-sort every row
then every column via adjacent `measure()`/`swap()`, harvest one
corner) scales cleanly to the full 8x8 grid and yields `32 * 64**2 =
131,072` in a single cascade harvest — exactly `Cactus_Single`'s target,
completing the category in one shot rather than a repeated-harvest loop.
003's naive full-`n-1`-pass sort projects ≈430,000 ticks total; this adds
an early-exit flag per bubble pass (stop once a pass makes zero swaps)
since much of the worst-case pass count does no real work once already
sorted.

**Variable.** 003's 4x4 validation grid → the real 8x8 grid, wired to
score (the run terminates once `Items.Cactus >= 131072`, which the
single cascade harvest should satisfy directly).

**Metric.** The completion modal's verdict and displayed time.

**Baseline.** 003: n=16 cascade, exact `32*n**2` match, 53,685 ticks
total (no early exit). Projected 8x8: ≈430,000 ticks (≈70-75s) without
early exit, likely somewhat less with it.

**Procedure.**
1. `saves/cactus_single/main.py`: 8x8 grid, till+plant all 64, wait for
   the last-planted tile to be fully grown, row-sort then column-sort
   with early exit, harvest corner, `quick_print` a `DONE` line, natural
   termination (the harvest itself should cross the target).
2. `tools/cycle.sh cactus_single exp-cactus_single-004-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If the cascade doesn't harvest all 64 (yield short of
131,072), the row-then-column sort didn't fully converge at this
scale — check for a bug in the sort (e.g. an off-by-one in pass/step
counts) before doubting the lemma itself, since 003 confirmed it exactly
at n=16.
