# exp-031 — why-carrot-fails — result

**Outcome.** diagnostic — carrot does not fail, and 019's conclusion was an
artifact of its own design

**1,114 carrot plantings traced.**

| stage | dominant state | count |
| --- | --- | --- |
| before harvest | `Grassland` + Tree/Bush, mostly unripe | 1,114 |
| after harvest | `Grassland` + **Grass** | 1,112 |
| **after plant** | **`Soil` + `Carrot`, ok=True** | **1,110** |

**Carrot succeeds 1,110 times out of 1,114 — 99.6%.** The assumed blocker does
not exist: `harvest()` clears the tile, `till()` converts it, and the carrot goes
in. Both the "occupancy blocks till" story and the empty-companion-tile fix built
on it (032) are void.

**Why 019 said otherwise, and it is my error.** 019 ran a *single drone* so that
`num_items(Items.Hay)` would measure only its own yield. But carrot costs 512 hay
and **512 wood**, and wood only arrives from harvesting Bush and Tree companions —
which, on a 32-drone farm, other drones supply constantly. One drone harvests
almost none, so wood stayed at zero and every carrot attempt was unaffordable.

The isolation that made the yield measurement clean destroyed the economy the
result depended on. **A single-drone probe is not a small farm; it is a different
farm.** That is now the second time isolating a variable has removed the thing
being measured — 008 dropped polyculture "to isolate the idle-time hypothesis"
and lost 59x to the missing multiplier.

**What this changes.** The claim that a third of passes collect 512 instead of
81,920, and that fixing carrot is worth ~2.8x, is withdrawn. Combining this with
026's arrival census — 52% mismatch (walk, harvest, replant: satisfied) and 45%
skip (already correct: satisfied) — the farm is already **~97% multiplied**.

**So the remaining gap is ticks per harvest, not lost multipliers.** The champion
spends ~967 ticks a harvest; the leader implies ~330. The dominant term is the
companion round trip on the 52% of passes that need one, and the lever is the
*skip rate* — currently 45%, set by how often a request happens to name a tile
already holding that type.

That points at a specific, cheap experiment: **reroll for a map hit.** 020 already
rerolls on an empty tile for 200 ticks a throw; rerolling until the request names
a tile we know is already correct converts a 1,459-tick pass into a 462-tick one.
Queued as 032.
