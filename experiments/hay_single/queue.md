# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **04:49.565, global rank #302** (exp-008)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Scored — the category is no longer empty

001-008 in one line each:

- 001: 1-tile schedulability floor (growth isn't the bottleneck).
- 002: single-tile short probe, ~39.2 hay/tick, Carrot looked permanently dead.
- 003: priced a *dedicated* wood tile for Carrot — dead, ~20x over budget.
- 004: clustering's hit-rate ceiling is ~1/3 — arithmetic said "maybe worth it".
- 005: clustering (dist 2) self-collides with its own farm tiles — bug.
- 006: clustering (dist 4) fixes the bug but the inter-tile commute costs
  more than it buys — multi-tile closed for good. Also found wood
  accumulates *for free* from ordinary companion churn, correcting 003.
- 007: single tile run long (200 cycles) — ≈49.9 hay/tick steady state,
  ≈05:30 projected.
- **008: real terminating driver, run to an actual score —
  04:49.565, global rank #302 (≈55.8 hay/tick, ≈2.1x off the leader),
  beating 007's own projection.**

## Queued

- [ ] 009 (open) — no specific lever identified yet. The obvious next
      question, if picked up: does the champion's ~2.1x gap to the leader
      close further with the same kind of measurement discipline that moved
      002→008 (e.g. is there headroom in *how fast* wood accumulates —
      right now it's a byproduct of type-mismatch churn, never optimised
      for), or is #302 close to what a single-drone-optimal design can
      reach and the gap is now mostly the leader's own cleverness? Not
      obviously worth another multi-tile attempt — 001/005/006 closed that
      three ways already. Start with an instrumented probe on the *current
      champion*, not a new design, per docs/LOOP.md's own rule (measure
      before designing around it).

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
- [x] 008 finish-and-score — **adopted, new (first) champion.** 04:49.565,
      global rank #302. `experiments/hay_single/008/result.md`
