# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Champion: **03:57.198, global rank #169** (exp-012) — **paused here, see below**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## 014/015 — the user's fundamental-shift challenge, tested empirically

013's pause was challenged (fairly): does the model's ceiling actually
survive a *genuinely different* strategy shape, not just parameter tweaks
on the same reactive design? Two real tests, both against the champion's
real 68.7 hay/tick:

- **014 (prepared, superseded by 015's more literal test):** two adjacent
  tiles with a same-tile guard.
- **015 bush-blanket-quad:** the user's literal proposal — 4 clustered
  tiles, the entire rest of the board pre-planted with Bush, reroll
  (uncapped) until Bush. Real run: 1,237.6 ticks/harvest post-setup
  (≈66.19 hay/tick), ≈64.99 hay/tick full-run-projected once the
  27,675-tick one-time setup is amortized — **matching or slightly
  trailing** the champion, not beating it. `experiments/hay_single/015/result.md`.

**The ceiling holds under a from-scratch alternative shape, empirically,
not just by the same model re-applied.** This is the strongest version of
the closure yet: four independent tests (schedulability 001, self-
collision 005, commute-tax 006, and now a genuinely different
full-coverage strategy 015) all land in the same place.

## PAUSED — the companion-servicing paradigm is provably at its ceiling

001-013 in one line each — see individual result.md files for full detail:

- 001-007: design settled (single tile, reroll-before-walk, wood accumulates
  for free from companion churn, multi-tile closed three ways).
- 008: first champion, 04:49.565, #302, ≈55.8 hay/tick.
- 009: reroll-before-walk probe, ≈98.75 hay/tick (200-cycle tail — later
  shown unrepresentative).
- 010: champion, `REROLL_LIMIT=2`. 04:13.399, #182, ≈64.7 hay/tick real.
- 011: full-run tick profile + exact probability model. **Proved the
  reroll-only asymptote (K→∞, full coverage) is exactly 1,200
  ticks/harvest ≈ 68.27 hay/tick** — a hard ceiling, not an estimate.
- 012: `REROLL_LIMIT=5`, champion. **03:57.198, #169, ≈68.7 hay/tick —
  already at the K→∞ ceiling.**
- **013: checked whether the ceiling's IID-uniform assumption could be
  false (a predictable draw sequence would break it). 300 raw draws:
  type frequencies within 0.4% of 1/3 each, all 24 positions reached by
  all 3 types, no autocorrelation, no type-position correlation. The
  draws are genuinely IID uniform — there is no hidden structure to
  exploit. `experiments/hay_single/013/result.md`.**

**The leader's implied pace needs ≈119 hay/tick; this design tops out at
≈68-70 hay/tick, mathematically, not by estimate.** Multi-tile is closed
three ways (001/005/006), Carrot/wood is resolved (003, corrected by
006/007), `swap()` and Fertilizer were considered and don't reduce the
fixed costs involved (013's result.md). Every avenue inside "harvest,
replant, satisfy the companion" has been checked.

**Decision (per the user's own instruction): pivot to `Hay` (the regular,
32-drone category) and carry the two lessons that transfer:**
1. **Reroll-before-walk** when the structural hit rate is low — Hay's
   current champion (020, 02:47.682, #130) only rerolls specifically for
   Carrot misses, not as a general "cheap reroll before an expensive walk"
   policy the way hay_single's does.
2. **Wood/Carrot accumulates for free from ordinary companion churn on a
   long run** — worth checking whether Hay's own champion already benefits
   from this incidentally (32 drones churning companions constantly) or
   whether there's a similar short-probe blind spot there too.

hay_single is left at **#169, 03:57.198** — a real, working, competitively
scored design, 1.72x off the world #1, not abandoned mid-failure.

## Queued (if picked back up later)

- [ ] 014 (deferred) — if a genuinely different mechanism is ever found
      (not another companion-servicing tweak — 013 closed that
      mathematically), it goes here. Candidates already ruled out:
      `swap()`-based tile access (013), Fertilizer-accelerated growth
      (013 — growth was never the bottleneck), sequence prediction (013).

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
- [x] 011 champion-tick-profile — proved the REROLL_LIMIT ceiling.
      `experiments/hay_single/011/result.md`
- [x] 012 reroll-limit-5 — champion. 03:57.198, #169.
      `experiments/hay_single/012/result.md`
- [x] 013 reroll-sequence-pattern — confirmed IID-uniform, no exploit.
      **Closes the paradigm; pivoting to Hay.** `experiments/hay_single/013/result.md`
