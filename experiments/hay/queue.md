# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [x] 035 query-until-hit — **the unlock.** 033 found `get_companion()` rerolls
      on every call, and a call costs **1 tick**; every reroll so far has
      replanted at 200 ticks to get a fresh request. Call it repeatedly until it
      names a tile the map already satisfies, cap the attempts, and the pass
      becomes a 26-tick skip instead of a 1,455-tick walk. 034 shows the skip rate
      must reach ~66% (from 45%) before a second plot can pay.
- [ ] 037 preference-stability — **the crux, and it bears on a merged result.**
      Does the companion in force at `harvest()` match the one we satisfied? 033
      showed `get_companion()` rerolls per call, so a skip decided from an earlier
      query may forfeit the 160x multiplier. Record the companion at the skip
      decision, query again immediately before harvesting, compare. If they
      disagree often, 013's 18.5 s map win rests on something narrower than its
      write-up claims.
- [ ] 036 skip-then-two-plots — once 035 lands, retry two plots. 034's arithmetic:
      a second tile pays only when work per harvest is under ~509 ticks, and the
      leader implies 2.2 tiles per drone at 466 ticks. 029 failed because it added
      the plot before cutting the work.

Cleaned 2026-08-16 13:05: the merge-conflict resolution in 020 resurrected
entries that were already finished (017, 018, 019, 023, 013, 008). Those are in
Done. What follows is genuinely open.

- [x] 031 why-carrot-fails — **the largest measurable prize.** 019 measured Bush
      5/5 and Tree 7/7 satisfied against Carrot 1/8, and a satisfied companion is
      worth **160x**. A third of requests are Carrot, so a third of passes collect
      512 instead of 81,920 — satisfying them all would be ~2.8x, against a 2.9x
      gap to the leader.
      The cause is assumed to be `till()` refusing ground a plant stands on, but
      that has never been checked. A probe that prints `get_ground_type()`,
      `get_entity_type()` and `can_harvest()` at the moment a carrot planting
      fails settles whether the blocker is the ground, the occupancy, or both —
      and therefore whether it is fixable at all.
- [x] 032 reroll-for-map-hit — **replaces empty-companion-tiles, which 031
      voided.** The farm is already ~97% multiplied, so the gap is ticks per
      harvest: 967 against the ~330 the leader implies. The dominant term is the
      companion round trip on the 52% of passes that need one, and the skip path
      costs 462 ticks against 1,459.
      020 already rerolls on an empty tile for 200 ticks a throw. Reroll instead
      until the request names a tile the map says is *already correct*: at a 45%
      hit rate that is ~1.2 throws, ~240 ticks, to turn a 1,459-tick pass into a
      462-tick one. Cap it, and measure the resulting skip rate.
- [ ] 033 probe-the-reroll — **prerequisite for trusting 020.** 032 found that
      `harvest()` fails on an unripe plant, so the reroll loop replants nothing
      and `get_companion()` returns the same preference every iteration. If that
      is right the reroll has never rerolled, and 020's 12.4 s win came from the
      single post-harvest replant rather than from rerolling. Print the companion
      before and after each attempt and count how many ever change.
- [ ] 022 reroll-limit — 020 caps rerolls at 2, leaving ~4% of passes still on a
      carrot request. Each reroll is one 200-tick plant. Try 3 and 4. Small, and
      only worth running if 031/032 do not make carrot succeed outright.
- [ ] 033 monocrop-checkerboard — the user's design: permanent Bush/Tree stock on
      alternating tiles so a companion stops being work at all. Deprioritised
      against 031 because a permanent stock makes carrot requests *harder* to
      satisfy, not easier, and carrot is where the gap is.

### Closed lines — do not reopen without new information

- **Layout/spacing.** Disjoint diamonds +15.9% (021, 024), dense packing +36.6%
  (022). Per-pass profiles are identical to within 1% (025 vs 026), so layout is
  not a lever.
- **Multi-plot.** Four plots +47 s (027), two plots +28 s (029). 030 found why:
  29% of visits reach an unripe plot and pay a 200-tick move for nothing.
  **Waiting in place beats walking to check** while growth is the constraint.
- **Trading companion yield for ticks.** Polyculture is worth 160x (019); no
  variant that gives up the multiplier can win (011 at 67x apparent, 016 +11.5 s).

## Done

- [x] 030 instrument-two-plots — **found the missing ticks.** 29% of visits reach
      an unripe plot and pay a 200-tick move for nothing; with movement in the
      accounting it is 1,160 ticks a harvest against the champion's 967, matching
      the measured +16%. A two-plot cycle revisits every ~2,320 ticks against
      ~2,819 of growth. **Waiting in place beats walking to check** — multi-plot
      is closed. `experiments/hay/030/result.md`

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
