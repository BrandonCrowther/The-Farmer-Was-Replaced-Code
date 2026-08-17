# exp-008 — finish-and-score (5-tile reroll pipeline) — result

**Outcome.** adopted — new champion.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 07:49.969, PB 07:49.969, Global Rank #85 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 16 internal `TIME_FINAL` samples, 459.81s–481.69s | all 16 finished with `CARROT` 100,025,344–100,028,928 (≥ target), no lost hits, no crashes |

**Baseline.** 005: real score, 11:54.303, Global Rank #118.
**Variant.** 07:49.969 (469.969s). **Delta.** **−34.2% wall time,
+33 ranks (#118 → #85).** Matches 007's ≈477s projection closely (the
16-sample internal spread, 459.8–481.7s, brackets it).

**Noise floor.** The 16 internal repeats' own spread (~4.5%) stands in
as the run-to-run noise floor, same approach as 005.

**Screenshots.** `logs/captures/20260817-011945-exp-carrots_single-008-r1.png`

**Verdict.** The reroll-before-walk + multi-tile combination (006+007)
translates cleanly into a real score: three real wins stacked
(3-tile walk-always → 5-tile reroll pipeline) took carrots_single from
11:54.303/#118 to 07:49.969/#85 in three experiments after the first
score. Adopting `saves/carrots_single/main.py` (008) as champion.
