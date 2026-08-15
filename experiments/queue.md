# Experiment queue

Backlog for the Phase 3 driving loop. One entry per idea, worked top to bottom.
Move an entry to `## Done` with its `exp-NNN` id once a `result.md` is committed.

Format:

```
- [ ] NNN slug — hypothesis, in one line. Metric: <what decides it>.
```

Rules the loop must respect:

- Never read or write `save/Save0/save.json`.
- Measure by running code and reading its output, not by inspecting files.
- Instrument with `quick_print` (0 ticks), never `print` (1 second of drone time).
- One variable per experiment, or the result is not attributable.

## Queued

- [ ] 001 watcher-settle — a 0.5 s poll with a 3 s cap detects File Watcher
      pickup more reliably than a fixed sleep. Metric: false-start rate over 20
      writes (F5 pressed before the reload landed).
- [ ] 002 sim-variance — `simulate()` run time varies run to run at fixed seed.
      Metric: spread over 10 runs at one seed; sets the noise floor that every
      later result has to beat.
- [ ] 003 speedup-ceiling — the `speedup` argument stops paying off past some
      value because the loop cannot feed it. Metric: run time vs speedup across
      64 / 256 / 1000 / 5000.

Seed the rest once the leaderboard categories worth attacking are chosen — see
"Still to decide" in `docs/PLAN.md`.

## Done

_(nothing yet)_
