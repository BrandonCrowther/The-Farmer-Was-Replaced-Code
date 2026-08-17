# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **03:57.198, global rank #169** (exp-012)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Three champions tonight; REROLL_LIMIT tuning treated as done

001-012 in one line each — see individual result.md files for full detail:

- 001-007: design settled (single tile, reroll-before-walk, wood accumulates
  for free from companion churn, multi-tile closed three ways).
- 008: first champion, 04:49.565, #302, ≈55.8 hay/tick.
- 009: reroll-before-walk probe, ≈98.75 hay/tick (200-cycle tail — later
  shown unrepresentative).
- 010: champion, `REROLL_LIMIT=2`. 04:13.399, #182, ≈64.7 hay/tick real.
- 011: full-run tick profile confirms 010's real steady state (~1,200-1,300
  ticks/harvest) and fits an exact reroll-probability model to real data
  (K=0 reproduces 008's 55.8 hay/tick almost exactly); predicts diminishing
  returns past K≈5 (K=5→66.33, K=7→67.39 modeled hay/tick).
- **012: `REROLL_LIMIT=5`, real scored run. Champion —
  **03:57.198, global rank #169 (−6.4% vs 010, ≈68.7 hay/tick, ≈1.72x off
  the leader).** Beat its own model prediction (66.33), the same direction
  010 beat its. `experiments/hay_single/012/result.md`.**
  (Hit and recovered from the documented memory-leak crash on the first
  attempt — see 012's result.md.)

## Queued

- [ ] 013 fundamental-fork-check — `REROLL_LIMIT` tuning is treated as
      exhausted (011's model: K=5→7 only +1.06 hay/tick, and 012 already
      landed above the K=5 prediction). Multi-tile is closed three ways
      (001/005/006). Carrot's wood-funding question is resolved (003,
      corrected by 006/007). Per docs/LOOP.md's bar for an empty queue,
      look explicitly for a genuinely different strategy before stopping:
      candidates to weigh (not yet run) — does the *own-tile handling* cost
      (harvest + replant, ~400 ticks) have any slack left, e.g. is `till()`
      ever called unnecessarily on the home tile; is there a cheaper way to
      discover a companion match than a full reroll-and-check when the
      position space is only ~24 cells (e.g., precomputing/caching more
      than one candidate before committing); does watering ever cost a
      wasted tick once the tank is empty. If none of these look like a real
      lever on inspection, say so and stop chasing further — 003 was a
      generous number even 20x over budget; check whether the remaining
      1.72x gap has any single-drone-achievable path left at all before
      declaring victory at #169.

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
- [x] 010 finish-and-score-v2 — champion. 04:13.399, #182.
      `experiments/hay_single/010/result.md`
- [x] 011 champion-tick-profile — confirmed 010's real steady state and
      modeled `REROLL_LIMIT` headroom. `experiments/hay_single/011/result.md`
- [x] 012 reroll-limit-5 — **adopted, champion.** 03:57.198, #169.
      `experiments/hay_single/012/result.md`
