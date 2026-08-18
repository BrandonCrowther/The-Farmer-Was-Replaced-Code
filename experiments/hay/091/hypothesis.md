# exp-091 — scan-order optimization (TSP-style reorder of the setup candidate-window walk)

**Hypothesis.** User watched the champion at 0.1x speed and noticed
setup taking close to 5 seconds before drones start harvesting. Every
setup-phase fix in this arc (076-090) optimized *walk-in* (getting to
the base) or *packing* (where bases sit) — none has ever touched the
*scan* itself: the ~30-tile candidate-window walk, visited in a fixed
`dx`-outer/`dy`-inner raster order. This session's own live probe
(exp-089-era methodology) measured this scan's real cost at
23,846-27,126 ticks/drone, by far the largest single component of
setup — dwarfing walk-in's now-tiny ~4,000-tick max (090). The raster
order was never chosen for minimal total walking distance between
consecutive tiles; it's an accident of loop nesting.

**Variable.** `driver()`'s setup-phase candidate loop in
`saves/hay/main.py`: nested `for dx in range(-3,5): for dy in
range(-3,4):` (computing `near()` at runtime, walking in raster order)
→ iteration over a hardcoded, offline-computed, offline-verified
static list of 30 `(dx, dy)` offsets in a distance-minimizing visiting
order. The `near()`/`ALL_CROPS` runtime checks are removed entirely —
the static list already excludes both, matching the "hardcode a
verified static table, never compute it live" pattern this project
already uses for `ALL_BASES`/`OWNED_OFFSETS`.

**Metric.** Real leaderboard time via `tools/cycle.sh`.

**Baseline.** 090 (champion, merged): 01:54.045, Global Rank #52.

**Offline sizing and live calibration (done before writing driver
code).**
- The 30-tile window is translation-invariant (same relative shape
  regardless of base position) — confirmed both offline and via this
  session's own probe (`SCAN_COST` output: every one of 32 drones
  reports the identical window regardless of base coordinate).
- Computed the raster order's total path cost (c1 → 30 tiles → c1) as
  a pure-movement model: 62 tiles (12,400 ticks). A greedy nearest-
  neighbor reorder gets to 42 tiles; adding 2-opt and or-opt local
  search across 30 different greedy seeds finds **36 tiles (7,200
  ticks)** — a **~42% reduction** in pure movement distance. Sanity-
  checked against a minimum-spanning-tree lower bound (30 tiles over
  the 31-point set including `c1`) — 36 is only 20% above a bound that
  doesn't even need to return to start, so this is close to the
  achievable optimum for this exact point set, not a lucky first find.
- **Live-calibrated the model directly** (`hay-scan-probe` worktree,
  scratch): instrumented the real, currently-deployed champion's scan
  loop to report `move_ticks` in isolation from `plant`/`harvest`
  overhead. Result: **`move_ticks` = 12,482 ticks, identical across
  all 32 drones**, matching the raster model (12,400) almost exactly
  (the ~82-tick gap is `move_to_wrapped()`'s own small per-call
  overhead, 30 calls × ~2.7 ticks). This directly validates the model
  against reality before committing to the reorder — the predicted
  36-tile/7,200-tick reordered cost should be equally trustworthy,
  giving an expected **~5,200-5,300 tick/drone reduction in the
  movement component alone** (~166,000 ticks fleet-wide before
  accounting for the removed runtime `near()`/`ALL_CROPS` check
  overhead, a further small saving on top).
- **Note on a confound found during calibration, not part of this
  change**: the same probe found `plant_ticks` varies wildly (4,200-
  12,020) correlated with a `nonvirgin` tile count (10-30) — traced to
  leftover entities from this session's own accumulated probe/
  experiment history on the shared persistent save, which the
  `import main` trick runs directly against. This does **not** affect
  real scored runs: `leaderboard_run()`/`simulate()` explicitly start
  from fixed, sandboxed conditions each time (`docs/wiki/Leaderboard.md`,
  `docs/wiki/Simulation.md`), never touching the messy persistent
  save. Confirmed as a probe-methodology artifact, not a real cost —
  recorded here so a future session doesn't re-chase it. The `move_ticks`
  isolation this hypothesis relies on is unaffected by this artifact.

**Falsifier.** The reordered list must be the exact same 30-position
*set* as the raster scan (verified offline: `set(order) ==
set(raster)`, True) — any drift would be a correctness bug, not a
performance question. Live validation must show the same 30 positions
visited per drone as before. If the real `cycle.sh` run doesn't beat
090 by more than the 0.069s noise floor, reject regardless of how
clean the offline/calibration numbers look.

**Procedure.**
1. Hardcode the computed order as a `SCAN_ORDER` literal (list of 30
   `(dx, dy)` tuples) in `saves/hay/main.py`; rewrite the setup loop to
   iterate over it directly.
2. Live validation (reduced/computed-TARGET `import main` trick):
   confirm every drone's `planted` dict ends up with the same 30
   positions as before (same keys, same coverage), no warnings.
3. `tools/cycle.sh hay exp-hay-091-r1 --from <worktree>` for the real
   run. Re-run once if the delta is within ~2x the noise floor.
4. Journal either way; merge only if it beats 090 by more than the
   floor.
