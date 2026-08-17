# exp-001 — terminate the seeded achievement driver — result

**Outcome.** adopted — Carrots (multi)'s first-ever leaderboard entry,
transferred cleanly from wood (multi)'s just-proven fix.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 06:39.725, PB 06:39.725, Global Rank #143 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 19 internal samples, `TICK_FINAL` 2,413,132–2,443,198 (avg 2,425,520) | all 19/19 crossed the 2,000,000,000 target cleanly |
| r1 | 549 "tried to use Water but didn't have enough" warnings | expected concurrency noise, same as wood/sunflowers (multi) |

**Baseline.** wood (multi) 001: 06:07.889 for a 10B target with the
identical driver shape.
**Variant.** 06:39.725 for a 2B target (5x smaller). **Delta.** Real
time is *not* proportionally smaller than wood's — Carrot's growth/
handling constants differ from Tree's, so a direct tick-for-tick
comparison isn't meaningful; both hit their real targets comfortably
inside a few minutes.

**Noise floor.** The 19 internal repeats' own spread (~1.2%) is tight.

**Screenshots.** `logs/captures/20260817-043920-exp-carrots-001-r1.png`

**Verdict.** The "check the seed, target-gate it, water-guard it"
pattern transferred a third time (Cactus, Wood, now Carrots — all
multi-drone) with zero design work beyond the fix already proven on
wood (multi). Adopting `saves/carrots/main.py` as champion.
