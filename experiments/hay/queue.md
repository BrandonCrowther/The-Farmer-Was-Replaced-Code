# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [ ] 016 no-carrot — carrot is the only companion that can fail. It needs Soil,
      and `till()` will not convert ground a plant stands on, so an unripe plant
      on the tile blocks it — ~230 "cannot plant on Grassland" per run. Test
      never attempting carrot at all: skip the walk outright, accept 1x on those
      passes, and save every wasted round trip. Metric: one run vs 03:05.323.

- [ ] 009 harvest-before-till — `p_make_callback` tills before planting, but
      `till()` will not convert ground a plant stands on, so an affordable
      carrot companion fails on an occupied tile (9 -> 183 such warnings in
      006). Harvest first in the companion callback. Cheap, and it applies to
      every category. Metric: one run vs champion.
- [ ] 013 measure-idle-ticks — settle what 007 only guessed at. Wrap the
      champion's busy-wait in `get_tick_count()` (0 ticks) and report the share
      of ticks actually spent waiting, not the share of passes that begin
      waiting. That number decides whether idle time is worth attacking at all.
      Diagnostic, not an optimisation.
- [ ] 007 carrot-when-rich — 003 showed carrot becomes affordable partway
      through a run (failures fell 760 -> 66 with no logic change), so wood is
      arriving from Bush companions. If the multiplier justifies 512 hay + 512
      wood, take the carrot face late even though it is unaffordable early.
      Depends on 004 and 005 landing first.
- [ ] 008 water-when-available — `while get_water() < 0.75` reached for water
      that was not there 711 times in 001. Condition it on
      `num_items(Items.Water)`. Metric: mean over 3 runs vs the 002 baseline.

## Done

- [x] 015 self-correcting-map — **rejected**, 03:09.234 (+3.9 s). Marking
      contested tiles permanently untrusted degrades the map to "always walk".
      **Optimism pays**: the asymmetry argument was right about single events and
      wrong about their frequency. `move_to_wrapped` kept in Common regardless.
      `experiments/hay/015/result.md`

- [x] 014 thirty-two-drones — **adopted**, 03:05.323, −0.466 s, rank #177.
      Confirms `SPAWNED 32 of 32`: thirteen experiments ran with four positions
      silently empty. Small win, because position only affects contention — and
      contention cannot be fixed by geometry at this drone count.
      `experiments/hay/014/result.md`

- [x] 013 companion-map — **adopted, new champion.** 03:05.789, −18.5 s (−9.1%),
      rank #230 -> #178. Each drone remembers what it planted where and skips the
      ~800 tick round trip when the tile is unchanged. Also measured
      `max_drones() = 32` against a spawn grid of 36 — we have been at the drone
      cap all along. `experiments/hay/013/result.md`

- [x] 012 skip-unaffordable — **adopted**, 03:24.347 (mean of 2), −0.205 s.
      Do not walk to a companion we cannot plant. Confirmed with a second run
      because the first cleared the floor by only 1.5x. Carrot is still never
      *successfully* planted, so a third of requests earn no multiplier — the
      biggest remaining prize. `experiments/hay/012/result.md`

- [x] 011 no-polyculture — **rejected decisively.** Polyculture is worth **67x**,
      not the ~5x it needs to break even against its ~800 ticks of movement per
      pass. Aborted at 1.26e9 hay / 2:24:43 in-game (145k hay/s vs the champion's
      9.78M hay/s). Retires every "trade yield for ticks" idea, 008's shape
      included. Surfaced two harness faults: `stop` never worked, and a failed
      run was being reported as a score. `experiments/hay/011/result.md`

- [x] 008 plot-rotation — **rejected, ~59x slower** (3:38:11 vs 03:40.911). The
      premise was a misreading of 007: 94% of passes *beginning* unripe is a
      frequency, not a duration. Dropping polyculture "to isolate the variable"
      threw away the 5x multiplier that was most of the yield, and a 25-tile
      circuit cost more movement than the waiting it removed.
      `experiments/hay/008/result.md`

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
