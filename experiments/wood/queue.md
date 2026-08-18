# Wood — experiment queue

Target: **10_000_000_000 wood**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Wood, "main", 5000)`

Branches: `auto_experiment/wood/NNN` · Results: `experiments/wood/NNN/result.md`

## The mechanic

Seeded design: 32 drones (one per column, world 32x32), each cycling
North by 2, harvest+replant with an interleaved Tree/Grass companion
pattern (not growth-pipelined the way wood_single's reroll-before-walk
champion is — each drone fully waits via `Common.await_harvest()`
before moving on). Just needed target-gating (the seed's `while True:`
never terminated) and a water-topup guard (same fix as sunflowers
(multi) 001).

**Smoke-test projections were badly wrong** — a 5-harvest sample
projected ≈8 hours, a 64-harvest sample projected ≈68 minutes, the
real ~24,415-harvest run finished in ≈6 minutes. True steady-state
throughput needed a much larger sample than either smoke test to
reveal; don't over-trust small-sample smoke tests for this kind of
32-drone design.

## Queued

- [x] 002 raise-water-threshold-blocking-growth — **CLOSED, no code
      change, no live run.** wood_single's exp-004 tonight found real
      Tree growth at water~1 is only 4,412 ticks (7.87x faster than an
      old unwatered measurement) — since this design blocks fully on
      growth with no interleaving, raising its 0.5 water threshold
      looked like a free lever borrowed from that win. Reconsidered
      against 001's own numbers before touching anything: 588 "not
      enough water" warnings already occur at the current threshold
      (32 drones sharing one pool — raising demand risks *worse*
      contention, not free speed), and the design's real per-drone
      efficiency (~2,912 ticks/harvest-equivalent, converting 001's
      91-ticks/harvest-summed-across-32-drones figure) is already
      comparable to wood_single's hard-won 2,682 — just achieved via
      parallelism (32 drones scanning forward, never revisiting a
      tile) instead of per-drone interleaving. The premise didn't
      survive contact with already-recorded numbers; not worth a real
      cycle to confirm what the numbers already argue against.
      `experiments/wood/002/result.md`
- [ ] 003 leader-gap — check the real leader time before assuming
      there's more headroom; this category wasn't benchmarked against
      the leaderboard's #1 during 001. A genuine redesign (full
      pre-seed + interleaving à la wood_single) remains a real but
      large lead — cross-drone Tree-adjacency avoidance in a packed
      32-drone grid is harder than wood_single's single-drone 4-tile
      layout — not attempted, flagged for a future session.

## Done

- [x] 001 terminate — **adopted, first-ever score.** Real scored run:
      **06:07.889, Global Rank #111**, all 20 internal repeats crossed
      the target cleanly. `experiments/wood/001/result.md`
