# Carrots — experiment queue

Target: **2_000_000_000 carrots**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Carrots, "main", 5000)`

Branches: `auto_experiment/carrots/NNN` · Results: `experiments/carrots/NNN/result.md`

## The mechanic

Structurally identical to wood (multi)'s seeded driver (32 drones, one
per column of the 32x32 world, interleaved Grass companion pattern,
not growth-pipelined). Same fix as wood/sunflowers (multi): target-gate
both loops, guard the water-topup against depletion. No design work
needed beyond the fix already proven twice.

## Queued

- [ ] 002 leader-gap — check the real leader time; not benchmarked
      during 001.

## Done

- [x] 001 terminate — **adopted, first-ever score.** Real scored run:
      **06:39.725, Global Rank #143**, all 19 internal repeats crossed
      the target cleanly. `experiments/carrots/001/result.md`
