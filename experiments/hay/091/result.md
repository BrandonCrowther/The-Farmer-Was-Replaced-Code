# exp-091 — scan-order optimization — result

**Outcome.** **Adopted, new champion. Biggest single win of the whole
076-091 arc.** 01:53.053, Global Rank **#49** (up 3 ranks from 090's
#52) — a real **-0.992s** (-0.87%), 14.4x the 0.069s noise floor,
unambiguous in one run, no re-run needed.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| offline sizing (`scan_order.py`, scratch) | raster order: 62-tile path cost (12,400 ticks modeled); greedy+2-opt+or-opt over 30 seeds: **36 tiles (7,200 ticks)** — a 42% cut | sanity-checked against a minimum-spanning-tree lower bound (30) — 36 is only 20% above a bound that doesn't even need to close the loop, so close to optimal, not a lucky first find |
| live calibration (`hay-scan-probe`, scratch — isolated `move_ticks` from `plant`/`harvest` cost) | **`move_ticks` = 12,482, identical across all 32 drones**, matching the raster model (12,400) almost exactly | validated the model against the real deployed champion *before* committing to the reorder, not after |
| live validation (target=200,000, `zzRunner.py` → `import main`) | 32/32 drones report `visits 30`, `back_at_c1 True`, no warnings | `SCAN_ORDER`'s position *set* matches the raster scan's exactly (offline-verified: `set(SCAN_ORDER) == raster set`) |
| real (target=2,000,000,000) | **01:53.053, #49** | `VERDICT=scored`, `WARN=2121 Water` (routine, see note below) |

**Baseline.** 090: 01:54.045, #52.

**Delta.** -0.992s (-0.87%), better. Adopted. Global rank #52 → #49.

**Why it won.** Every setup-phase fix in this arc (076-090) optimized
*walk-in* (076, 088, 090) or *packing* (088, 090) — none had ever
touched the *scan* itself, the ~30-tile candidate-window walk, which
this session's own probe measured at 23,846-27,126 ticks/drone, by far
the largest single setup component. It was always walked in a fixed
raster (`dx` outer, `dy` inner) order, an accident of loop nesting
never chosen for minimal walking distance. A TSP-style offline search
found a visiting order cutting the pure-movement component from 62 to
36 tiles (42%), and a live probe confirmed the model tracks reality
almost exactly (12,482 measured vs 12,400 modeled) before the reorder
was ever built. Hardcoding the order as a static `SCAN_ORDER` literal
also let the runtime `near()`/`ALL_CROPS` checks be deleted entirely —
the list already encodes them — removing `ALL_CROPS`'s construction
loop too (now genuinely unused).

**Traced directly to a real user observation.** The user watched the
champion at 0.1x speed and reported setup taking close to 5 seconds
before drones start harvesting — independent confirmation (not derived
from any tick model) that setup was a large, visible fraction of total
run time, and specifically prompted looking at the *scan* rather than
walk-in (already well-optimized by 088/090) for the next win.

**Note on `WARN` count (2121, up from 090's 1434/1393).** Not
investigated as part of this experiment — flagged for the water-
contention investigation already in progress (`experiments/hay/queue.md`,
next item), prompted by the same user 0.1x observation session
(unfulfilled water requests visible at launch). Not a regression this
experiment caused: the reorder touches only movement order, not water
logic; the higher count is more likely explained by setup finishing
faster now, compressing more drones' launch-time water catch-up into a
similar window. Left for the dedicated investigation rather than
guessed at here.

**Verdict.** `saves/hay/main.py` updated to 091 (`SCAN_ORDER` literal
replacing the raster loop; `ALL_CROPS` construction removed as dead
code). Merged to `main`. `record.json`/`queue.md` updated.
