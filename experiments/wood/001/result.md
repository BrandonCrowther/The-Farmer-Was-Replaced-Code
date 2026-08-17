# exp-001 — terminate the seeded achievement driver — result

**Outcome.** adopted — Wood (multi)'s first-ever leaderboard entry, no
bugs, much faster than projected.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 06:07.889, PB 06:07.889, Global Rank #111 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 20 internal samples, `TICK_FINAL` 2,217,646–2,246,904 (avg 2,232,112) | all 20/20 crossed the 10,000,000,000 target cleanly |
| r1 | 588 "tried to use Water but didn't have enough" warnings | expected concurrency noise across 32 drones, matches sunflowers (multi) 001 and Hay's documented pattern |

**Baseline.** Smoke-test projections: naive (5-harvest sample,
7,215 ticks/harvest) → ≈8 hours; steady-state (64-harvest sample,
1,016 ticks/harvest) → ≈68 minutes.
**Variant.** Real run: 06:07.889 (367.9s ≈ 6.1 min) — **≈11x faster
than the steady-state smoke projection**, and ≈78x faster than the
naive one. Real full-run average was ≈91 ticks/harvest-equivalent
(2,232,112 ticks / 24,415 harvests) — the smoke test's "steady state"
at 64 harvests still hadn't converged; true throughput needed a much
larger sample to reveal, consistent with this session's other
warm-up-dilution findings but more extreme here.

**Noise floor.** The 20 internal repeats' own spread (~1.3%) is tight.

**Screenshots.** `logs/captures/20260817-040801-exp-wood-001-r1.png`

**Verdict.** The seeded interleaved Tree/Grass achievement driver only
needed target-gating and a water-guard to score a 10-billion-wood
target in about 6 minutes real time. Adopting `saves/wood/main.py` as
champion. Confirms this session's broader lesson: smoke-test
projections for un-pipelined-looking designs can be wildly pessimistic
once true steady-state (many more harvests than a quick sample) kicks
in — worth just running the real attempt rather than over-modeling from
a small sample, when the downside of guessing wrong is only a
background wait, not a hang.
