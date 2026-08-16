# exp-003 — guarded-polyculture — result

**Outcome.** rejected

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **04:56.552** | accepted run, but slower than baseline |

**Baseline.** 04:55.320 · **Variant.** 04:56.552 · **Delta.** **+1.232 s (+0.42%)**

**Noise floor.** 0.15 s. The regression is ~8x the floor, so it is real and no
confirming re-run is needed to reject it.

**Warning histogram.**

| warning | 002 | 003 |
| --- | --- | --- |
| Didn't have the required items to plant `Entities.Carrot` | 760 | **66** |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 6 | **259** |
| Tried to use `Items.Water` but didn't have enough of it | 713 | 713 |

**Verdict.** The hypothesis was half right and the fix was wrong.

Right: the companion tile was being ruined. Wrong: planting grass on it is not
the repair. Two things the run taught, both of which the time alone would not
have:

1. **Carrot becomes affordable partway through.** The "didn't have the items"
   count fell 760 → 66 without any change to the guard's logic, so the run does
   eventually hold 512 hay and 512 wood. The hay is obvious; the wood must come
   from Bush companions that other drones planted and harvested. Carrot is not
   permanently out of reach, it is out of reach *early*.
2. **`till()` does not convert ground that a plant is standing on.** The new
   259 "cannot plant on Grassland" failures are the direct cost of this change:
   the tile now holds grass, `harvest()` leaves it there when it is not ripe,
   `till()` then does nothing, and the carrot plant fails on Grassland. The old
   code left bare soil, which was ruinous for yield but at least tillable.

**What actually matters, and 003 missed it.** A plant's companion is always a
*different* species, so grass rolls uniformly over Bush, Tree and Carrot. Of
those, `get_cost` says **Bush and Tree are free** and only Carrot costs
anything. But `Common.p_planting_table` maps `Entities.Tree` to a callback that
plants **Grass**, so a Tree request is silently satisfied with the wrong plant —
no warning, no multiplier, on roughly a third of all companion visits. The
polyculture multiplier is 5x before upgrades and doubles per upgrade, so this is
worth vastly more than the tick-shaving 003 attempted.

Queued as 004 (plant the true companion) and 005 (replant to reroll an
unaffordable companion — replanting rolls a fresh preference, and with 004 in
place two of the three faces are free).
