# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [ ] 009 harvest-before-till — `p_make_callback` tills before planting, but
      `till()` will not convert ground a plant stands on, so an affordable
      carrot companion fails on an occupied tile (9 -> 183 such warnings in
      006). Harvest first in the companion callback. Cheap, and it applies to
      every category. Metric: one run vs champion.
- [ ] 011 plot-rotation — **the fork.** 94% of passes find the plant unripe:
      drones busy-wait while ~96% of the 32x32 field lies empty. Give each drone
      a plot and walk it in rotation so a tile has the whole circuit to grow.
      Drop polyculture for this run to isolate the idle-time hypothesis.
      Metric: one run vs 03:40.911; expect a large win.
- [ ] 012 rotation-with-polyculture — restore the companion multiplier on top of
      whatever 011 shows. Only meaningful if 011 wins.
- [ ] 007 carrot-when-rich — 003 showed carrot becomes affordable partway
      through a run (failures fell 760 -> 66 with no logic change), so wood is
      arriving from Bush companions. If the multiplier justifies 512 hay + 512
      wood, take the carrot face late even though it is unaffordable early.
      Depends on 004 and 005 landing first.
- [ ] 008 water-when-available — `while get_water() < 0.75` reached for water
      that was not there 711 times in 001. Condition it on
      `num_items(Items.Water)`. Metric: mean over 3 runs vs the 002 baseline.

## Done

- [x] 007 farm-state-diagnostic — **the bottleneck is growth, not ticks.** 825
      samples: the tile always holds grass (so 004/006 stand), companion faces
      are uniform thirds (confirming 004's premise), and `can_harvest()` is
      False on 94.1% of passes. Drones idle-wait while 96% of the field is
      unused. Invalidates the *rationale* for 006/008/009 and opens 011.
      `experiments/hay/007/result.md`

- [x] 006 reroll-companion — **rejected**, 03:41.013 (+0.102 s, inside the
      floor, so: no effect). The mechanic works — unaffordable carrot requests
      fell 73% — but a harvest plus a plant per reroll costs exactly what the
      multiplier wins. Prices the mechanic, and cleared the 005 tripwire.
      `experiments/hay/006/result.md`

- [x] 005 use-shared-helper — **adopted**, 03:40.911, delta 0.000 s. Confirms
      `Common.plant_companion()` matches 004's local override exactly; hay's
      private polyculture() is gone. Also serves as 004's confirming run.
      Tripwire noted: an identical time to the millisecond twice would mean the
      score has stopped tracking the code. `experiments/hay/005/result.md`

- [x] 004 true-companion — **adopted, new champion.** 03:40.911, −74.4 s
      (−25.2%) vs baseline; rank #422 -> #278. `p_planting_table` mapped Tree to
      a callback that plants Grass, silently forfeiting the polyculture
      multiplier on ~1/3 of companion visits. `experiments/hay/004/result.md`

- [x] 003 guarded-polyculture — **rejected**, 04:56.552 (+1.23 s). Planting
      grass on an unaffordable companion tile is not the repair: `till()` will
      not convert ground a plant stands on, so it traded 760 rare failures for
      259 common ones. Taught two things that reshaped the queue — carrot
      becomes affordable mid-run, and the Tree mapping is a silent miss.
      `experiments/hay/003/result.md`

- [x] 002 baseline — **04:55.320** (mean of 3), noise floor ±0.15 s. The score
      the game reports is already averaged over 2 h of repeats, so Hay barely
      varies and one run per variant is enough to rank candidates.
      `experiments/hay/002/result.md`
- [x] 001 terminate — bounded every drone's loop on `num_items(Items.Hay)` and
      reaped the spawns with `wait_for`. **04:55.393**, global rank #422 — the
      category scores at all for the first time. `experiments/hay/001/result.md`
