# Sunflowers — experiment queue

Target: **100_000 power**
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Sunflowers, "main", 5000)`

Branches: `auto_experiment/sunflowers/NNN` · Results: `experiments/sunflowers/NNN/result.md`

## The mechanic

Seeded design: 32 drones, each farming its own dedicated column (32
tiles, wrapping) of the 32x32 world — 1,024 tiles total — continuous
harvest+replant, base yield only (no max-petal 8x bonus tracking, see
sunflowers_single for that mechanic). Just needed target-gating (the
seed's `while True:` never terminated) and a water-topup guard
(`num_items(Items.Water) > 0` — 32 drones racing a shared pool produces
expected, harmless "not enough water" warnings otherwise, matching
`saves/hay/main.py`'s documented pattern).

## Queued

- [ ] 002 reroll-to-max-petal — sunflowers_single (tonight) proved
      rerolling every replant to petals=15 (the max) makes every
      harvest hit the 8x bonus for free, since nothing can exceed the
      ceiling. This driver doesn't use that at all — an 8x throughput
      multiple is plausible if it transfers cleanly to 32 concurrent
      drones sharing one "at least 10 standing" bonus-eligibility
      check across all 1,024 tiles (should be trivially satisfied at
      this scale).

## Done

- [x] 001 terminate — **adopted, first-ever score.** Real scored run:
      **04:03.434, Global Rank #126**, all 30 internal repeats crossed
      the target cleanly. `experiments/sunflowers/001/result.md`
