# Sunflowers — experiment queue

Target: **100_000 power**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Sunflowers, "main", 5000)`

Branches: `auto_experiment/sunflowers/NNN` · Results: `experiments/sunflowers/NNN/result.md`

## Queued

- [ ] 001 terminate — the seeded driver is an endless `while True` achievement
      farmer; a leaderboard run only scores if the program ends. Add a
      termination check on the target and stop the drones. Metric: the run
      completes and reports a time at all.
- [ ] 002 baseline — record the time the terminating seed produces, as the
      number every later variant has to beat. Metric: mean over 3 runs.

## Done

_(nothing yet)_
