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

- [ ] 002 leader-gap — check the real leader time before assuming
      there's more headroom; this category wasn't benchmarked against
      the leaderboard's #1 during 001.

## Done

- [x] 001 terminate — **adopted, first-ever score.** Real scored run:
      **06:07.889, Global Rank #111**, all 20 internal repeats crossed
      the target cleanly. `experiments/wood/001/result.md`
