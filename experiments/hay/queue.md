# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [ ] 030 instrument-two-plots — 029 lost 16% where the tick model predicted a
      wash, so ~150 ticks a harvest are unaccounted for. Run the two-plot driver
      with 025/026's instrumentation (work, wait, arrival class per pass) and
      find them. Do not guess: two invented mechanisms have already been wrong.

- [ ] 023 measure-preplanted — count arrivals where the companion tile already
      holds the requested plant, with `quick_print`, under the spacing-5 grid.
      021 claims overlap is cooperation; this is the measurement that would
      confirm or kill that claim instead of arguing it.

- [ ] 022 reroll-limit — 020 caps rerolls at 2, leaving ~4% of passes still on a
      carrot request. Each reroll is one 200-tick plant. Try 3 and 4.

- [ ] 019 mechanics-probe — **method fix.** Measure what has only been inferred:
      the polyculture multiplier (hay delta across one harvest, satisfied vs not,
      single drone so `num_items` is uncontaminated), growth ticks with no walk
      in the way, companion distance distribution, and real water levels and tank
      counts. Will not score; the telemetry is the point.
- [ ] 018 diamond-lattice — 32 drones at minimum L1 separation 8 (rows 4 apart,
      centres 8 apart, odd rows offset 4) give every drone a private 25-tile
      diamond, so no planting is overwritten and no map entry can go stale.
      Depends on 019 confirming the companion range is really 3.
- [ ] 017 water-threshold — `while get_water() < 0.75` targets a level the farm
      cannot supply: 32 tiles at 0.75 drain ~0.24 water/s against a supply of
      ~0.025/s, so the loop spins on failed `use_item` calls, ~200 ticks a pass.
      Water only when a tank is actually in hand. Metric: one run vs 03:05.323.

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

- [x] 029 two-plots — **rejected**, 03:20.637 (+28.3 s). Multi-plot loses at two
      plots as well as four, and the tick model predicted a wash, so ~150 ticks a
      harvest are unexplained. Recorded as an open question rather than a third
      invented mechanism. `experiments/hay/029/result.md`
- [x] 028 renoise — **the floor is 0.069 s (4 clean runs)**, so the original
      0.15 s stands and the 2.41 s correction was withdrawn. The real finding:
      identical code scores 67 sd faster when run deep into the memory leak, so
      comparisons are only valid under matching game conditions.

- [x] 027 multi-plot — **rejected**, 03:37.380 (+47 s, 19 sd). Four plots cost
      more in movement than the idling they remove. Surfaced the real finding of
      the day: the noise floor is **2.41 s, not 0.15 s**, and 012/014/017 are
      noise. `experiments/hay/027/result.md`

- [x] 024 lattice-wrapaware — **rejected**, 03:19.655 against 021's 03:19.653.
      Two milliseconds apart, so the wrap fix changed nothing and that
      explanation is dead as well. The lattice penalty is structural and
      deterministic; 025 instruments it instead of guessing a third time.
      `experiments/hay/024/result.md`

- [x] 022 denser-spacing — **rejected, +63.1 s (+36.6%).** With 021 this brackets
      an optimum: disjoint (L1 8) +15.9%, champion (L1 5) best, dense (L1 4)
      +36.6%. Layout tuning is not where the remaining gap lives.
      `experiments/hay/022/result.md`

- [x] 021 diamond-lattice — **rejected, +27.4 s (+15.9%).** Disjoint territories
      work exactly as designed and make the farm 16% slower: **contention was
      cooperation.** Neighbours pre-plant each other's companion tiles, so 010's
      skip fires far more often when territories overlap. Casts doubt on 014 and
      re-explains 015. `experiments/hay/021/result.md`

- [x] 020 reroll-after-harvest — **adopted, new champion.** 02:52.271, −12.4 s
      (−6.7%), rank #177 -> #149. 006's idea with its placement fixed: reroll
      after the multiplied harvest, not before it. `experiments/hay/020/result.md`

- [x] 017 water-threshold — **adopted**, 03:04.715, −0.608 s. Gate the watering
      loop on `num_items(Items.Water) > 0` so it stops spinning on an unreachable
      level; water warnings 1042 -> 120. Smaller than predicted, and this run
      cannot say why. `experiments/hay/017/result.md`
- [x] 019 mechanics-probe — **the multiplier is 160x, not 67x**, and carrot is
      satisfied only 1 time in 8 while Bush and Tree never fail. A third of
      passes therefore yield 512 instead of 81,920; satisfying all of them would
      be 2.8x, against a 3x gap to the leader. Growth is 2819 ticks at water 0.
      Companion distances are 1–3 and never wrap. `experiments/hay/019/result.md`

- [x] 016 no-carrot — **rejected**, 03:16.787 (+11.5 s). Skipping a doomed
      planting should have been free and was not: **the companion walk is how
      grass growth time gets hidden.** Walk time ~= growth time, which is why
      008, 011 and 016 all failed. The remaining gap needs faster growth, not
      shorter walks — and growth is water-limited.
      `experiments/hay/016/result.md`

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
