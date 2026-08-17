# exp-001 — terminate the seeded achievement driver — result

**Outcome.** adopted — Sunflowers (multi)'s first-ever leaderboard
entry, no bugs.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 04:03.434, PB 04:03.434, Global Rank #126 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 30 internal samples, `TICK_FINAL` 1,434,388–1,461,023 (avg 1,449,602) | all 30/30 crossed target cleanly |
| r1 | 931 "tried to use Water but didn't have enough" warnings | expected concurrency noise across 32 drones sharing one water pool (each failed call costs 1 tick, harmless) — matches Hay's documented pattern |

**Baseline.** Smoke test (target 200, 32 drones): 37,471 ticks, naive
linear extrapolation to 100,000 projected ≈51 minutes.
**Variant.** Real run: 04:03.434 (243.4s) — **≈12.5x faster than the
naive linear projection.** The smoke test's ratio didn't account for
all 32 drones' columns being far from "warmed up" yet at only 200 power
total (≈6 harvests/drone) — steady-state throughput across 1,024
parallel tiles is much higher than the early-cycle sample suggested.

**Noise floor.** The 30 internal repeats' own spread (~1.8%) is tight.

**Screenshots.** `logs/captures/20260817-033208-exp-sunflowers-001-r1.png`

**Verdict.** The seeded achievement driver (32 drones, one dedicated
column each, continuous base-yield harvest+replant, no max-petal bonus
tracking) only needed target-gating and a water-guard to score for
real. Adopting `saves/sunflowers/main.py` as champion. No 8x-bonus
logic is used here at all — sunflowers_single's reroll-to-max-petal
trick (proven tonight) is the obvious next lever if this category gets
revisited, worth roughly an 8x throughput multiple if it transfers
cleanly to 32 concurrent drones.
