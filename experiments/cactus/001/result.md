# exp-001 — terminate the seeded achievement driver — result

**Outcome.** adopted — Cactus (multi-drone)'s first-ever leaderboard
entry, and the seeded algorithm worked correctly on the very first real
attempt, no bugs found.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 01:00.697, PB 01:00.697, Global Rank #961 | modal, `VERDICT=scored` |
| r1 (internal repeats) | 119 internal samples, `TICK_FINAL` 329,303–412,199 (avg 368,640) | **all 119/119 harvested exactly 33,554,432/33,554,432** — 100% reliability |

**Baseline.** None — first score for this category.
**Variant.** 01:00.697 (60.697s), real average ≈368,640 ticks/run.
**Delta.** N/A (first score).

**Noise floor.** The 119 internal repeats' own spread (~22%,
329k-412k) reflects real per-run variance in the random cactus sizes
driving different amounts of selection-sort search+drag work, same
kind of variance cactus_single itself showed.

**Screenshots.** `logs/captures/20260817-032120-exp-cactus-001-r1.png`

**Verdict.** The pre-existing seeded achievement code (selection sort +
physical drag, one drone per row then one drone per column, up to 32
parallel drones) already implemented the row-then-column sort lemma
correctly — it only needed the endless `while True:` loop replaced with
a single execution to ever terminate and score. No algorithm changes
were needed. Adopting `saves/cactus/main.py` as champion. The leader
(`const arch *`) scores 00:07.800 — 7.8x faster, a gap of similar shape
to every other single-shot-cascade category tonight (cactus_single:
7.3x→4.3x, wood_single: 9.6x) — likely the same class of headroom
(a smarter sort than selection-sort-with-linear-search, mirroring
cactus_single's bubble→insertion-sort win) rather than anything
structurally wrong with this design.
