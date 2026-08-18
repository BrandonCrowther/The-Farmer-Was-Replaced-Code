# exp-088 — staggered base grid (offset + row-stagger walk-in reduction)

**Hypothesis.** Every drone spawns at `(0,0)` (established this
session: `spawn_group()` never moves before spawning children, so the
entire 32-drone fan-out happens from the root's post-`clear()`
position) and walks once, straight to its own base — a real,
measured, one-time-per-repeat cost (076/077 already won on this exact
class of cost). Today's champion centers its 6x6 base grid at offset
`(3,3)`, which puts the grid's midpoint at `(15.5, 15.5)` — almost
exactly the single farthest point from `(0,0)` on a 32-wide wrapped
world (worst case `wdist` to origin is 16). Repositioning the grid
(offset) and tightening its shape (vertical spacing, and a row
stagger) while holding every pairwise base-to-base distance fixed
(so the polyculture-dilution safety boundary this session already
measured — distance 3 = unsafe, distance 4 = safe — is provably
unaffected) should cut total fleet walk-in distance substantially.

**Variable.** `ALL_BASES`' construction in `saves/hay/main.py`:
`(3 + i*5, 3 + j*5)` for `i,j` in `0..5` minus 4 holes → replaced with
offset `(18,25)`, x-spacing `5` (unchanged — already at the true
minimum, domino-constrained), y-spacing `3` (down from 5), and a
horizontal stagger of `+2` on odd `j` rows. `driver()`'s hardcoded
root call (`driver(3, 3)`) updates to match `ALL_BASES[0]`.

**Metric.** Real leaderboard time via `tools/cycle.sh`.

**Baseline.** 085 (champion, merged): 01:54.587, Global Rank #52.

**Offline sizing (done before writing any driver code, this
session).** Exhaustive search (`stagger_search.py`/
`verify_staggered.py`, scratch) over every offset (0-31 x 0-31), every
stagger (0-31), and y-spacing in `{2,3,4,5}` (x fixed at 5, the
horizontal floor):
- x-spacing below 5, or y-spacing below 3, is infeasible at any
  stagger (global min cross-base crop distance drops below 4 — the
  measured-live safety boundary from this session's `simulate()`
  probes — for every combination tried).
- The winning shape (`offset=(18,25)`, `x_spacing=5`, `y_spacing=3`,
  `stagger=2` on odd rows) is the true optimum of this family
  (rectangular grid with a single per-row horizontal stagger): full
  offset sweep at that shape found `total_walkin=384, max_walkin=21`,
  strictly better on *both* metrics than the best non-staggered
  rectangular layout found (`432, 23`) and far better than today's
  `544, 28`.
- Re-verified independently and exhaustively (`verify_staggered.py`):
  32 unique base positions, 64 unique crop tiles (no collisions),
  full 32×31-pair × 4-crop-combination safety check confirms global
  minimum cross-base crop distance is exactly `4` (the measured floor,
  not violated), and every base's own candidate window is still a
  uniform 30 positions (no regression from today's champion).

**Predicted effect.** Using this session's measured walk-in tick
model (`walk_ticks ≈ 208 * wdist((0,0), base) + 236`, fit against 32
real probe measurements, R²=1.0000): total fleet walk-in ticks drop
from ~113,152 to ~79,872 (**-33,280 ticks, -29.4%**), worst-single-
drone from ~5,824 to ~4,368 (**-1,456 ticks, -25%**). Same class of
setup-phase, once-per-repeat cost as 076 (-0.864s) and 077 (-0.305s),
larger in raw ticks than either — a real, not noise-floor-scale,
candidate.

**Falsifier.** If live validation finds any duplicate position, any
crop-tile collision, any candidate-window size other than 30, or any
pairwise crop distance below 4, the change is rejected before ever
reaching a real run — this is a hard correctness gate, not a
performance question, exactly like 086's `OWNED_OFFSETS` validation.
If validation passes but the real `cycle.sh` run doesn't beat 085 by
more than the 0.069s noise floor, rejected on the real number
regardless of how clean the offline model looked (086's own lesson:
a provably-correct, well-modeled change can still lose or tie for
reasons the model didn't capture).

**Procedure.**
1. Implement the new `ALL_BASES` geometry in the worktree.
2. Live validation (reduced-TARGET `import main` trick): print all 32
   `(bx,by)` positions and confirm uniqueness, confirm setup-phase
   candidate-window visit counts match the offline model (30/drone,
   960 total), confirm no warnings.
3. `tools/cycle.sh hay exp-hay-088-r1 --from <worktree>` for the real
   run. Re-run once if the delta is within ~2x the noise floor.
4. Journal either way; merge only if it beats 085 by more than the
   floor.
