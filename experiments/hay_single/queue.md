# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## The design is settled: single tile, reactive skip-and-remember

001-007 in one line each:

- 001: 1-tile schedulability floor (growth isn't the bottleneck).
- 002: single-tile short probe, ~39.2 hay/tick, Carrot looked permanently dead.
- 003: priced a *dedicated* wood tile for Carrot — dead, ~20x over budget.
- 004: clustering's hit-rate ceiling is ~1/3 — arithmetic said "maybe worth it".
- 005: clustering (dist 2) self-collides with its own farm tiles — bug.
- 006: clustering (dist 4) fixes the bug but the inter-tile commute costs
  more than it buys — multi-tile closed for good. Also found wood
  accumulates *for free* from ordinary companion churn (not a dedicated
  tile), correcting 003.
- 007: single tile run long (200 cycles) confirms the free-wood mechanism
  there too, and gives the real number: **≈49.9 hay/tick steady state,
  ≈330s (05:30) projected to 100,000,000 — ≈2.4x off the leader**, a real
  improvement over 002's ~7:00 estimate.

**No further design exploration queued.** The remaining work is building
this into a real terminating driver and running it for a genuine score.

## Queued

- [ ] 008 finish-and-score — take 007's exact single-tile logic, add the
      `num_items(Items.Hay) >= 100_000_000` termination condition, and run
      it as a real (non-probe) leaderboard cycle. Report the actual time,
      not the ≈330s projection — the projection ignores warm-up drag and
      hasn't been checked against a real full run. If it lands close to
      007's estimate, adopt it as hay_single's first-ever real score.
      Falsifier: none needed — this is the category's first correctness
      check (does it actually terminate and score at all), not a comparison.

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
- [x] 007 single-tile-long-run — **adopted as the design.** ≈49.9 hay/tick
      steady state, ≈05:30 projected. `experiments/hay_single/007/result.md`
