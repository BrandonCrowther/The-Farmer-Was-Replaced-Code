# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **04:13.399, global rank #182** (exp-010)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## 011 confirmed 010's number and modeled the remaining headroom

001-011 in one line each — see individual result.md files for full detail:

- 001-007: design settled (single tile, reroll-before-walk, wood accumulates
  for free from companion churn, multi-tile closed three ways).
- 008: first champion, 04:49.565, #302, ≈55.8 hay/tick.
- 009: reroll-before-walk probe, ≈98.75 hay/tick (200-cycle tail — later
  shown unrepresentative).
- 010: **champion.** 04:13.399, #182, ≈64.7 hay/tick real.
- **011: full-run tick profile (real scored run, 04:13.634, PB unchanged —
  confirms 010 is reproducible). Real steady state is ≈1,200-1,300
  ticks/harvest from harvest 100 onward, matching 010's real average far
  better than 009's optimistic 829.5. The exact reroll-probability model
  (R=400, W=1,600, p=1/3) reproduces 008's real 55.8 hay/tick at K=0
  almost exactly and predicts diminishing returns past K≈5:
  K=0→55.85, K=2→62.13, K=5→66.33, K=7→67.39 hay/tick.
  `experiments/hay_single/011/result.md`.**

## Queued

- [ ] 012 reroll-limit-5 — one more real run with `REROLL_LIMIT=5` (model
      predicts ≈66.33 hay/tick, ≈+7% over 010's ≈62-65). If it lands near
      that, adopt as champion. Diminishing returns past K≈5-7 are already
      clear from 011's model (K=5→7 only +1.06 hay/tick) — this is meant to
      be the last tuning pass on `REROLL_LIMIT`, not the start of a sweep.
      Falsifier: if it doesn't beat 010, the model's assumptions (fixed
      W=1,600, clean p=1/3) don't hold precisely enough to bank on for
      further K increases, and 013 should stop tuning this knob.
- [ ] 013 (open, after 012) — if 012 lands close to model, the queue is
      genuinely thin: multi-tile closed (001/005/006), Carrot lever
      resolved (003/006/007), reroll-vs-walk tuned near its ceiling (011,
      012). Check for a fundamental fork before declaring this exhausted
      (docs/LOOP.md, "Empty queue") rather than assuming one doesn't exist.

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
- [x] 010 finish-and-score-v2 — adopted, champion. 04:13.399, #182.
      `experiments/hay_single/010/result.md`
- [x] 011 champion-tick-profile — confirmed 010's real steady state and
      modeled `REROLL_LIMIT` headroom. `experiments/hay_single/011/result.md`
