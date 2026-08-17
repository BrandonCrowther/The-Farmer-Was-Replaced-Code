# Sunflowers_Single — experiment queue

Target: **10_000 power** on an 8x8 farm with a single drone
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Sunflowers_Single, "main", 5000)`

Branches: `auto_experiment/sunflowers_single/NNN` · Results: `experiments/sunflowers_single/NNN/result.md`

## The mechanic

Sunflowers are not polyculture (Polyculture.md excludes them) and not a
cascade/merge crop like Cactus/Pumpkin — Sunflowers.md: harvesting the
sunflower with the *most petals* (7-15, uniform, fixed at plant time,
measurable before fully grown) while ≥10 sunflowers stand on the farm
gives 8x power; harvesting a non-max one poisons the *next* harvest too.
Base yield is 1 Power/harvest (001).

The key structural finding (001): `harvest()` on an *unripe* entity
destroys it for 200 ticks rather than requiring `can_harvest()==True`
(Available-Functions.md) — combined with petals being fixed and
readable immediately at plant time, a cheap reroll (harvest the
just-planted unripe sunflower + replant, ~400 ticks/attempt) redraws
petals *before* paying the ~17,643-tick growth cost. Rerolling every
tile to petals=**15** (the maximum possible) before letting it grow
means nothing can ever exceed it — a farm-wide tie for max is
permanent, so every harvest gets the 8x bonus with zero tracking or
ordering logic. 10 tiles is both the mandatory minimum for bonus
eligibility and already comfortably above the idle-elimination
threshold for this growth/handling ratio (no measurable idle at N=10).

Note: Power passively speeds the drone 2x while any is held, consuming
1 Power/30 actions (Sunflowers.md) — a small, real background drain
that shows up as slightly-under-8 gains on some harvests (002), not a
bug.

## Queued

- [ ] 004 cap-the-reroll-tail — the fixed target=15 reroll is a
      geometric distribution (p=1/9, true mean 9 attempts) with a long
      right tail; 003's real run landed 37.8% above 002's small-sample
      (n=30) projection because of it. A `REROLL_LIMIT` cap with a
      fallback to accepting a lower-but-still-safe value, or tracking
      the dynamic current farm-wide max instead of the fixed ceiling of
      15, would cut the tail's cost without losing correctness.

## Done

- [x] 001 mechanics-probe — starting stockpile (Carrot 1B, Sunflower
      costs 1 Carrot), growth 17,643 ticks (unwatered), petals fixed at
      plant time (readable pre-maturity), base yield 1, genuine 8x
      bonus confirmed exact. Found the reroll opportunity: `harvest()`
      destroys an unripe entity for 200 ticks instead of requiring
      ripeness. `experiments/sunflowers_single/001/result.md`
- [x] 002 reroll-to-15-validation — **adopted the paradigm.** 10-tile
      round robin, reroll every replant to petals=15, 29/30 harvests
      exact 8x (1/30 fractional from the background Power-for-speed
      drain, not a miss). `experiments/sunflowers_single/002/result.md`
- [x] 003 finish-and-score — **adopted, first-ever score.** Real 10-tile
      reroll-to-15 driver, real scored run: **20:53.149, Global Rank
      #300**, all 6 internal repeats crossed the target cleanly.
      `experiments/sunflowers_single/003/result.md`
