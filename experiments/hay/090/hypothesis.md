# exp-090 — full stagger-axis search (completes 088's search, plus a diagonal-domino check)

**Hypothesis.** User asked to explore two ideas after 089 closed the
hot-loop-mechanism avenues: (1) a non-horizontal crop-pair (domino)
shape, since 088 found the horizontal domino costs exactly one tile of
packing margin the vertical axis doesn't pay; (2) whether a different
macro layout could still capture more setup-phase savings. Both
resolved analytically before touching any code:

1. **Domino shape.** Reach/window size (the setup-phase scan cost
   driver) is identical (30 tiles) for every distance-1-adjacent
   domino offset — horizontal `(1,0)`, vertical `(0,1)`, and diagonal
   `(1,1)` all tie. Diagonal doesn't cost more to scan. But at its own
   best-optimized spacing/offset, diagonal's minimum achievable total
   walk-in (384) is worse than horizontal/vertical's true optimum
   (336, found below) — not a win.
2. **088's own search was incomplete.** It only tried staggering the
   X-axis per alternating row. A fair search (staggering *either* axis)
   finds horizontal and vertical domino shapes converge on the exact
   same true optimum by x/y symmetry — **336 total walk-in, 19
   max-single-drone**, using the *same* horizontal domino shape 088
   already deployed, just a different spacing/stagger/offset
   combination (`spacing (3,4)`, stagger axis Y, stagger `2`, offset
   `(23,22)`, vs 088's `spacing (5,3)`, stagger axis X, stagger `2`,
   offset `(18,25)`).

**Variable.** `ALL_BASES` construction constants in
`saves/hay/main.py`: `X_OFFSET/Y_OFFSET` 18,25 → 23,22; `X_SPACING`
5 → 3; `Y_SPACING` 3 → 4; stagger axis X → Y (`ROW_STAGGER` applied to
`y` gated on `i % 2` instead of `x` gated on `j % 2`); `ROW_STAGGER`
value unchanged at 2. `driver()`'s hardcoded root-base reference
(`ALL_BASES[0]`) needs no change — same pattern as 088.

**Metric.** Real leaderboard time via `tools/cycle.sh`.

**Baseline.** 088 (champion, merged): 01:54.162, Global Rank #52.

**Offline sizing (done before writing driver code).** Exhaustive
search (`domino_shapes.py`/`domino_refine.py`, scratch) over every
domino offset up to distance 2, every spacing pair 1-6 on each axis,
every stagger value 0-31 on *both* axes, and offset 0-31×0-31 for the
winning shape:
- Diagonal domino: best achievable is 384 total / 24 max — does not
  beat horizontal/vertical's optimum.
- Horizontal domino, spacing (3,4), Y-axis stagger 2, offset (23,22):
  **336 total walk-in, 19 max** — confirmed the true optimum for this
  shape (fine-grained exhaustive offset/stagger sweep at this spacing,
  plus a broader spacing sweep at step-2 offset resolution finding
  nothing better).
- Re-verified exhaustively (`verify_090.py`): 32 unique base positions,
  64 unique crop tiles (no collisions), full 32×31-pair × 4-crop-
  combination safety check confirms global minimum cross-base crop
  distance is exactly 4 (this session's measured safe floor, matching
  088's own margin exactly — not tighter, not looser), and every
  base's own candidate window is still a uniform 30 positions (no
  regression from 088).
- Base index 18 lands exactly on `(0,0)` — the actual spawn origin —
  giving that one drone zero walk-in distance.

**Predicted effect.** Using this session's measured walk-in tick model
(`walk_ticks ≈ 208 * wdist((0,0), base) + 236`): total fleet walk-in
ticks drop from 088's ~79,872 to ~69,888 (**-9,984 ticks, -12.5%**),
worst-single-drone from ~4,368 to ~3,952 (**-416 ticks, -9.5%**).
Roughly 30% the magnitude of 088's own win (-33,280 ticks) — same
mechanism and measurement method, so the *direction* is trusted, but
the *size* is close enough to the noise floor (per 088's real -0.425s
scaled down proportionally, a rough ~-0.13s estimate) that this needs
the standard re-run-if-close protocol, not a single-run assumption.

**Falsifier.** Same hard correctness gate as 088: any duplicate
position, crop-tile collision, candidate-window size other than 30, or
pairwise crop distance below 4 rejects this before a real run. If live
validation passes but the real `cycle.sh` run doesn't beat 088 by more
than the 0.069s noise floor (or is within ~2x it), re-run once before
concluding either way.

**Procedure.**
1. Implement the new `ALL_BASES` geometry in the worktree.
2. Live validation (reduced-TARGET `import main` trick): confirm all
   32 `(bx,by)` positions match the offline model exactly, confirm
   candidate-window visit counts are 30/drone, confirm no warnings.
3. `tools/cycle.sh hay exp-hay-090-r1 --from <worktree>` for the real
   run. Re-run once if the delta is within ~2x the noise floor.
4. Journal either way; merge only if it beats 088 by more than the
   floor.
