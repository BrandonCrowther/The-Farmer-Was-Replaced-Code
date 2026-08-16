# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [ ] 004b confirm-champion — one more run of 004 to pin the new champion's
      number precisely, since every later delta is measured against it.
- [ ] 004c use-shared-helper — hay/main.py carries a local polyculture() from
      004; Common.plant_companion() now does the same thing for every category.
      Drop the override and call Common.polyculture(). Behaviour should be
      identical, so this is a confirming run, not an improvement: it must come
      back at 03:40.9 +/- the floor.
- [ ] 005 reroll-companion — a plant's companion preference is rerolled when it
      is replanted, and grass is free. When the roll is Carrot (the only costly
      face: 512 hay + 512 wood) replant rather than paying or wasting the trip.
      Only ever reroll at the moment we replant anyway, never mid-growth, and
      cap the attempts — each costs a plant plus a get_companion. Metric: one
      run vs whatever 004 leaves as the champion. Do this after 004, since 004
      changes which faces are worth keeping. **Reference implementation exists:**
      the seeded `saves/wood/main.py` driver already rerolls, replanting until
      `get_companion()` returns a Grass companion at the distance it wants.
- [ ] 006 carrot-when-rich — 003 showed carrot becomes affordable partway
      through a run (failures fell 760 -> 66 with no logic change), so wood is
      arriving from Bush companions. If the multiplier justifies 512 hay + 512
      wood, take the carrot face late even though it is unaffordable early.
      Depends on 004 and 005 landing first.
- [ ] 007 water-when-available — `while get_water() < 0.75` reached for water
      that was not there 711 times in 001. Condition it on
      `num_items(Items.Water)`. Metric: mean over 3 runs vs the 002 baseline.

## Done

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
