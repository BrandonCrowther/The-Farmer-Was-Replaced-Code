# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **04:13.399, global rank #182** (exp-010)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Two real scores landed tonight

001-010 in one line each:

- 001: 1-tile schedulability floor (growth isn't the bottleneck).
- 002: single-tile short probe, ~39.2 hay/tick, Carrot looked permanently dead.
- 003: priced a *dedicated* wood tile for Carrot — dead, ~20x over budget.
- 004: clustering's hit-rate ceiling is ~1/3 — arithmetic said "maybe worth it".
- 005: clustering (dist 2) self-collides with its own farm tiles — bug.
- 006: clustering (dist 4) fixes the bug but the inter-tile commute costs
  more than it buys — multi-tile closed for good. Also found wood
  accumulates *for free* from ordinary companion churn, correcting 003.
- 007: single tile run long (200 cycles) — ≈49.9 hay/tick steady state.
- 008: **first champion.** 04:49.565, rank #302, ≈55.8 hay/tick.
- 009: reroll-before-walk probe — up to 2 cheap rerolls (~400 ticks,
  destroy-unripe + replant, no travel) before falling back to a walk,
  since a miss's true structural hit rate is only 1/3 (004). Measured
  ≈98.75 hay/tick over a 200-cycle tail window.
- **010: real terminating driver with 009's logic, run to score —
  **04:13.399, global rank #182 (−12.8% vs 008, ≈64.7 hay/tick, ≈1.84x off
  the leader).** Undershot 009's 98.75 projection: a 200-cycle probe warms
  up its own small set of companion positions faster than the full
  ~1,221-harvest run does, so 009's tail window wasn't the true steady
  state for a run 6x longer. `experiments/hay_single/010/result.md`.**

## Queued

- [ ] 011 real-run-tick-profile — before tuning `REROLL_LIMIT` or trying
      another lever, read the *actual* per-harvest tick trajectory from a
      real (or much longer, 500+ cycle) probe of the current champion, to
      get a steady-state number that isn't optimistic the way 009's 200
      cycles were. That number, not another guess, should set the next
      target.
      Falsifier: none needed — this is measurement, not a design change.
- [ ] 012 (open, after 011) — whatever 011's real steady-state number
      suggests is still on the table. `REROLL_LIMIT` (currently 2, chosen
      by analogy to Hay's own constant, never derived here) is the most
      likely next knob, but tune it from 011's real trajectory, not another
      short probe.

## Done

- [x] 001 mechanics-probe. `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe. `experiments/hay_single/002/result.md`
- [x] 003 price-carrot-lever — corrected by 006/007 (true only cold/short).
      `experiments/hay_single/003/result.md`
- [x] 004 overlap-arithmetic. `experiments/hay_single/004/result.md`
- [x] 005 clustered-probe (distance 2) — self-collision bug.
      `experiments/hay_single/005/result.md`
- [x] 006 clustered-v2 (distance 4) — commute tax closes multi-tile; found
      the free-wood mechanism. `experiments/hay_single/006/result.md`
- [x] 007 single-tile-long-run — adopted as the design.
      `experiments/hay_single/007/result.md`
- [x] 008 finish-and-score — first champion. 04:49.565, #302.
      `experiments/hay_single/008/result.md`
- [x] 009 reroll-before-walk — probe measured ≈77% throughput gain; fed
      010. `experiments/hay_single/009/result.md`
- [x] 010 finish-and-score-v2 — **adopted, new champion.** 04:13.399, #182.
      `experiments/hay_single/010/result.md`
