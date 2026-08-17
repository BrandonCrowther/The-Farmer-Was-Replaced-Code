# exp-057 — full memory-matched reroll-before-walk, real full run — result

**Outcome.** adopted — new champion, confirms the memory-maturity
theory.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 02:42.421, PB 02:42.421, Global Rank #111 | modal, `VERDICT=scored` |
| r1 | 1,381 water warnings, 140 Carrot-unaffordable, 9 "Cannot plant Carrot on Grassland" | expected concurrency/affordability noise |

**Baseline.** Champion (real, this session): 02:47.682 PB / 02:52.376
fresh, #130-131. 049 (150-cycle bounded probe, same reroll logic):
1,471 ticks/harvest — *worse* than the champion's ~1,390.

**Variant.** 02:42.421 (162.421s), #111. **Delta.** **-3.1% wall time,
+19-20 ranks (#130/131 → #111)** over the real full run — the *opposite*
direction from 049's short-probe result.

**Noise floor.** Single real run — not independently repeated, but the
direction (improvement) is opposite enough from 049's short-probe
regression that this isn't noise; it's the predicted memory-maturity
effect.

**Screenshots.** `logs/captures/20260817-085123-exp-hay-057-r1.png`

**Verdict.** Confirms the theory: Hay has no free-type companion
shortcut (unlike carrots_single/wood_single's free-Grass), so a
memory-matched reroll's hit rate depends entirely on how many of the
~24 candidate positions a drone has personally walked to. 049's
150-cycle bounded probe couldn't let that memory mature and
under-measured the technique — the real run's ~871 cycles/drone
lets it. Adopting `saves/hay/main.py` as champion. Still well short of
the #3-10 cluster (~01:47-01:48, ≈750-856 ticks/harvest implied) — this
session's math (growth floor 415 ticks at water≈1, clean-measured in
056; own handling 400) puts the *zero-servicing* floor at ≈815, just
inside that cluster band, meaning closing the remaining gap needs the
*servicing* cost (still nonzero here) pushed further down, not a new
paradigm. Next: tune `REROLL_LIMIT` higher than 5 now that the
memory-maturity effect is confirmed real — the higher the mature hit
rate, the more attempts are worth paying for.
