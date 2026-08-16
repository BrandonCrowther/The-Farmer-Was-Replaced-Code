# Hay — experiment queue

Target: **2_000_000_000 hay**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay, "main", 5000)`

Branches: `auto_experiment/hay/NNN` · Results: `experiments/hay/NNN/result.md`

## Queued

- [ ] 002 baseline — record the time the terminating seed produces, as the
      number every later variant has to beat. Metric: mean over 3 runs.
- [ ] 003 no-polyculture — the Hay start has no carrot seeds, so
      `Common.polyculture()` failed to plant a companion 760 times in 001.
      Drop it, or only run it when the companion is plantable. Metric: mean
      over 3 runs vs the 002 baseline.
- [ ] 004 water-when-available — `while get_water() < 0.75` reached for water
      that was not there 711 times in 001. Condition it on
      `num_items(Items.Water)`. Metric: mean over 3 runs vs the 002 baseline.

## Done

- [x] 001 terminate — bounded every drone's loop on `num_items(Items.Hay)` and
      reaped the spawns with `wait_for`. **04:55.393**, global rank #422 — the
      category scores at all for the first time. `experiments/hay/001/result.md`
