# exp-002 — finish-and-score (single-tile reroll-before-walk) — result

**Outcome.** adopted — wood_single's first-ever leaderboard entry.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 31:59.849, PB 31:59.849, Global Rank #232 | modal, `VERDICT=scored`; game crashed once mid-launch (routine, recovered via `tools/tfwr.sh relaunch`, no data lost) |
| r1 (internal repeats) | 4 internal samples, `TICK_FINAL` 11,626,941–11,691,164 (avg 11,662,887), `WOOD` 500,036,608–500,374,528 | all 4/4 crossed target cleanly |

**Baseline.** 001's projection: `500,000,000/409,600 ≈ 1,221` harvests
at full multiplier. Smoke test (500k target, 2 harvests) suggested
≈21,375 ticks/harvest, but that's dominated by one-time setup overhead
amortized over only 2 harvests.
**Variant.** Real average ≈9,551 ticks/harvest (11,662,887 / ~1,221) —
**less than half** the smoke-test figure once setup cost is diluted
over the real ~1,221-harvest run, and noticeably *cheaper* than
hay_single's real single-tile average despite Tree's much larger
isolated growth constant (34,718 vs Grass's ~404) — the reroll-before-
walk paradigm's per-harvest cost is dominated by handling, not raw
growth, once it converges.

**Noise floor.** The 4 internal repeats' own spread (~0.6%) is tight.

**Screenshots.** `logs/captures/20260817-025249-exp-wood_single-002-r1.png`

**Verdict.** hay_single's champion paradigm transplants cleanly to
wood_single with only the `own_tile_ready()` fix noted in the
hypothesis (plant `Entities.Tree` directly, not via
`get_planting_instructions`). Adopting `saves/wood_single/main.py` as
champion. **The leader (`□萌萌的新□`) scores 03:20.446 — 9.6x faster** —
a large gap, similar in kind to Hay's earlier unexplained leader gap.
Given 001's 2.44x neighbor-growth-penalty for adjacent Trees, a
multi-tile pipeline here needs real spacing (not just companion-range
self-collision safety) — worth a follow-up experiment, though the size
of the leader gap suggests something more structural may also be at
play, same caution as Hay's `leader-gap-unexplained` status.
