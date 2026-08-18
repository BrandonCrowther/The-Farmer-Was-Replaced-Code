# exp-088 — staggered base grid — result

**Outcome.** **Adopted, new champion.** 01:54.162, Global Rank #52 —
down from 085's 01:54.587, a real **-0.425s** (-0.37%), 6.2x the
0.069s noise floor, unambiguous in one run.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| offline sizing (`stagger_search.py`, `verify_staggered.py`, scratch) | `total_walkin=384, max_walkin=21` vs today's `544, 28` | exhaustive search over every offset (0-31 x 0-31), every stagger (0-31), y-spacing in {2,3,4,5} — this is the true optimum of the rectangular-plus-row-stagger family, not a lucky first candidate |
| offline safety re-verification | 32 unique base positions, 64 unique crop tiles (no collisions), global min cross-base crop distance = 4 across all 32x31 pairs x 4 crop-tile combinations | matches this session's live-measured safe boundary (distance 3 = 10/400 dilution hits, distance 4 = 0/400) exactly, not just theory |
| live validation (target=200,000, `zzRunner.py` → `import main`) | 32/32 unique `VALIDATE_088` positions, exact match to the offline model, all report `visits 30` (matches today's champion's per-drone window size — no regression), no warnings | confirms the real game's `move_to_wrapped`/`wdist` arithmetic agrees with the offline Python model, not just that the model is self-consistent |
| real (target=2,000,000,000) | **01:54.162, #52** | `VERDICT=scored`, `WARN=1289 Water` (routine) |

**Baseline.** 085: 01:54.587, #52.

**Delta.** -0.425s (-0.37%), better. Adopted.

**Why it won.** Every drone spawns at `(0,0)` (established this
session: `spawn_group()` never moves before spawning children) and
walks once, straight to its own base — a real, setup-phase,
once-per-repeat cost, same class as 076/077. 085's grid (offset
`(3,3)`, uniform spacing 5) centered its 6x6 footprint at
`(15.5,15.5)`, almost exactly the single farthest point from `(0,0)`
on this 32-wide wrapped world. This experiment repositions the grid
(offset `(18,25)`) and exploits an asymmetry the user spotted directly
from the on-screen layout: the horizontal crop pair (`c2 = bx+1`) eats
one tile of anchor spacing that the vertical axis never pays, so
vertical spacing had one full tile of unused safety margin (distance 5
where only 4 is required) — tightening it to 3 (giving distance-4,
matching horizontal's own floor) plus a `+2` horizontal stagger on
alternate rows (letting diagonal neighbors, not just direct N/S ones,
absorb the distance-4 budget) cuts total fleet walk-in distance from
544 to 384 tiles (-29.4%) and worst-single-drone from 28 to 21 (-25%),
per an exhaustive offline search, not a single hand-picked candidate.
Every pairwise base-to-base distance — the only thing the dilution-
safety boundary depends on — is unaffected by the offset shift, so
repositioning the grid could not have introduced a correctness risk;
this was re-verified anyway, exhaustively, before writing driver code.

**What this confirms.** The vertical-spacing asymmetry and the grid's
poor placement relative to the origin were both real, previously-
unexploited costs — distinct from, and unrelated to, the shared-
territory-planting family closed in exp-087 the same session. This is
a pure packing/placement fix: every drone still does 100% of its own
planting, nothing is shared, no cross-drone coordination risk exists
here at all.

**Verdict.** `saves/hay/main.py` updated to 088 (`ALL_BASES` offset
`(18,25)`, x-spacing 5, y-spacing 3, row stagger 2). Merged to `main`.
`record.json`/`queue.md` updated.
