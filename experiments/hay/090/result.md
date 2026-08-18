# exp-090 — full stagger-axis search — result

**Outcome.** **Adopted, new champion.** 01:54.045, Global Rank #52 —
down from 088's 01:54.162, a real **-0.117s** (r2, the number that
stands as PB), confirmed by a consistent-direction re-run (r1
-0.091s). Both individually clear the 0.069s noise floor (1.3x and
1.7x respectively); same-sign across both runs, same bar 085 was
adopted on.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| offline sizing (`domino_shapes.py`/`domino_refine.py`, scratch) | horizontal/vertical domino true optimum: `total_walkin=336, max_walkin=19` vs 088's `384, 21`; diagonal domino: best achievable `384, 24` (does not beat it) | exhaustive search over domino offset, spacing 1-6 per axis, stagger 0-31 on *both* axes (088's own search only tried X-axis stagger — an incomplete search, not a shape limitation) |
| offline safety re-verification | 32 unique base positions, 64 unique crop tiles (no collisions), global min cross-base crop distance = 4 across all 32×31 pairs × 4 crop-tile combinations | matches 088's own margin exactly — not tighter, not looser |
| live validation (target=200,000, `zzRunner.py` → `import main`) | 32/32 unique `VALIDATE_090` positions, exact match to the offline model, all report `visits 30` (no regression from 088's uniform window size), no warnings | |
| real r1 (target=2,000,000,000) | **01:54.071, #52** | `VERDICT=scored`, `WARN=1434 Water` (routine); -0.091s vs 088, 1.3x floor |
| real r2 | **01:54.045, #52** | `VERDICT=scored`, `WARN=1393 Water` (routine); -0.117s vs 088, 1.7x floor, new PB |

**Baseline.** 088: 01:54.162, #52.

**Delta.** -0.117s (-0.10%), better. Adopted.

**Why it won.** 088 found the right *mechanism* (every drone spawns
at `(0,0)`, so walk-in is `wdist((0,0), base)`, and the old grid
centered its footprint on the farthest point from the origin) but its
own search for the best offset/spacing/stagger combination only ever
tried staggering the X coordinate per alternating row — an
implementation gap in the search, not a limit of the mechanism. A fair
search that also tries staggering Y per alternating column finds a
genuinely better point in the same search space: `spacing (3,4)`,
Y-axis stagger `2`, offset `(23,22)` — 336 total walk-in / 19 max vs
088's 384/21, same horizontal-domino shape, same safety margin
(distance exactly 4, this session's measured floor), zero new
geometric risk. One base (index 18) lands exactly on `(0,0)`, the
actual spawn origin, giving that drone zero walk-in.

**Also explored per the user's request: a non-horizontal domino
shape.** Reach/window size (the setup-phase scan-cost driver) is
identical (30 tiles) for every distance-1-adjacent domino offset —
horizontal, vertical, and diagonal `(1,1)` all tie, so a diagonal pair
doesn't cost more to scan. But its own best-achievable packing optimum
(384 total) doesn't beat horizontal/vertical's true optimum (336) —
not a win. Closed analytically, no live probe needed (the offline
model that found 336 already fully characterizes it).

**Verdict.** `saves/hay/main.py` updated to 090 (`ALL_BASES` offset
`(23,22)`, x-spacing 3, y-spacing 4, column stagger 2 on Y). Merged to
`main`. `record.json`/`queue.md` updated.
