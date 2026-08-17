# exp-005 — finish-and-score — result

**Outcome.** adopted — carrots_single's first-ever leaderboard score.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 11:54.303, PB 11:54.303, Global Rank #118 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 11 internal `TIME_FINAL` samples, 705.01s–723.81s | game repeats internally until 2 real hours simulated (Leaderboard.md); all 100,024,320/100,024,320 carrots multiplied, 0 lost hits |

**Baseline.** 004's projection: ≈690s (≈11:30) at ≈23.88 carrots/tick.
**Variant.** 11:54.303 (714.303s). **Delta.** +24.3s, +3.5% over
projection — 004's ≈3,430 ticks/harvest was sampled over only 60 cycles;
the full ~1,221-cycle run likely saw slightly costlier average
non-Grass companion draws, or simple sampling noise in the shorter
probe. Not investigated further — this is a first score, not a
regression, and well within the same order as the projection.

**Noise floor.** Not separately measured for this experiment (a real
scored run, not a same-conditions A/B) — the 11 internal repeats' own
spread (705.01s–723.81s, ~2.6%) stands in as the run-to-run noise floor
for this category.

**Screenshots.** `logs/captures/20260817-005353-exp-carrots_single-005-r1.png`

**Verdict.** The reactive-multi-tile-pipeline playbook (mechanics probe
→ direct mechanic confirmation → single-tile reactive baseline →
growth-bound idle-time measurement → multi-tile pipeline sized from the
handling-vs-growth ratio → real terminating driver) works end-to-end and
produced a competitive first score (#118) in 5 experiments without
guessing at any unverified mechanic. Adopting `saves/carrots_single/main.py`
as champion. Next: either tune tile count/spacing further for
carrots_single, or reapply this exact playbook to an untouched category
(cactus_single, wood_single, pumpkins_single, sunflowers_single,
maze_single, or their multi-drone counterparts).
