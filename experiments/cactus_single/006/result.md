# exp-006 — finish-and-score (8x8, insertion sort) — result

**Outcome.** adopted — new champion.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 00:32.063, PB 00:32.063, Global Rank #228 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 225 internal samples, min 162,968 / avg 194,688 / max 228,059 ticks | **all 225/225 harvested exactly 131,072/131,072** — 100% reliability |

**Baseline.** 004: real score, 00:54.267, Global Rank #350, real average
≈329,568 ticks/run.
**Variant.** 00:32.063 (32.063s), real average ≈194,688 ticks/run.
**Delta.** **-40.9% wall time, -40.9% average ticks** — matches 005's
4x4 prediction (-42.4%) closely.

**Noise floor.** The 225 internal repeats' own spread stands in as the
noise floor, same approach as previous scored wins tonight.

**Screenshots.** `logs/captures/20260817-015327-exp-cactus_single-006-r1.png`

**Verdict.** Insertion sort's O(n+inversions) cost transfers cleanly
from the 4x4 validation to the real 8x8 scored run. Adopting
`saves/cactus_single/main.py` as champion: 00:54.267/#350 →
00:32.063/#228 in two experiments. **The leader is still 4.3x faster
(00:07.447)** — real headroom remains. The next lever is likely
avoiding full re-derivation of position every outer-loop iteration
(`move_to` re-queries `get_pos_x()`/`get_pos_y()` repeatedly) and/or a
genuinely different approach to the ≈38k-tick planting phase, which is
now a much larger fraction of the (smaller) total.
