# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **04:49.565, global rank #302** (exp-008)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Scored, and a large win queued to land

001-009 in one line each:

- 001: 1-tile schedulability floor (growth isn't the bottleneck).
- 002: single-tile short probe, ~39.2 hay/tick, Carrot looked permanently dead.
- 003: priced a *dedicated* wood tile for Carrot — dead, ~20x over budget.
- 004: clustering's hit-rate ceiling is ~1/3 — arithmetic said "maybe worth it".
- 005: clustering (dist 2) self-collides with its own farm tiles — bug.
- 006: clustering (dist 4) fixes the bug but the inter-tile commute costs
  more than it buys — multi-tile closed for good. Also found wood
  accumulates *for free* from ordinary companion churn, correcting 003.
- 007: single tile run long (200 cycles) — ≈49.9 hay/tick steady state.
- **008: real terminating driver, run to an actual score —
  04:49.565, global rank #302 (≈55.8 hay/tick, ≈2.1x off the leader).**
- **009: reroll-before-walk probe — a miss's true structural hit rate is
  1/3 (004), so most misses are cheaper to resolve with up to 2 cheap
  rerolls (~400 ticks each, destroy-unripe + replant, no travel) than one
  ~1,600-tick walk. Measured steady-state throughput ≈98.75 hay/tick —
  **~77% higher than the champion.** `experiments/hay_single/009/result.md`.**

## Queued

- [ ] 010 finish-and-score-v2 — build 009's reroll-before-walk logic into a
      real terminating driver (same shape as 008: `while num_items(Hay) <
      TARGET`) and run it as a real scored cycle. If it lands near 009's
      ≈167s (02:47) projection, adopt it as the new champion — a ~1.2x gap
      to the leader instead of ~2.1x. Falsifier: none needed, same as 008 —
      first correctness check for this variant, not a comparison.
- [ ] 011 (open, after 010) — if 010 lands close to the leader, worth asking
      whether `REROLL_LIMIT` itself is tuned right (2 was chosen by analogy
      to Hay's own constant, not derived here) before declaring the queue
      exhausted again.

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
- [x] 008 finish-and-score — adopted, first champion. 04:49.565, #302.
      `experiments/hay_single/008/result.md`
- [x] 009 reroll-before-walk — probe measured ≈77% throughput gain; feeds
      010. `experiments/hay_single/009/result.md`
