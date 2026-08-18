# exp-017 — port Hay(multi)'s stray-tick fixes — result

**Outcome.** **Adopted, new champion.** 03:00.347, Global Rank #74 —
down from 016's 03:08.281/#89. A real -7.934s (-4.3%), +15 ranks — by
far the largest single win of this category's stray-tick-scour work,
and larger than any individual fix's effect on Hay(multi) tonight.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| validation (target = current inventory + 3,000,000) | clean termination, overshoot 31,040, no warnings | confirms correctness given the real 100M target is unreachable from persistent save state |
| real (target=100,000,000) | **03:00.347, #74** | `VERDICT=scored` |

**Baseline.** 016: 03:08.281, #89.

**Delta.** -7.934s (-4.3%), +15 global ranks.

**Verdict.** Confirms tonight's cross-category hypothesis: proven fixes
transfer without needing fresh design work, exactly like this category's
own exp-016 transplant of Hay-multi's exp-073 macro design. The larger
magnitude here (vs. each individual Hay-multi fix's own -0.1 to -0.9s)
has two likely causes: (1) `hay_single`'s pre-017 code was *worse* than
Hay-multi's pre-075 baseline specifically on `instructions()` — it
called the no-op guard twice per reroll cycle, not once, so removing it
here recovers more; (2) this category is single-drone, so every tick
saved converts directly into this one drone's own throughput, with no
32-way dilution the way Hay-multi's per-drone savings have. Worth
checking whether other single-drone categories with the same lineage
(any other `_single` category built on this reroll-servicing shape)
have the same unclaimed gap. `saves/hay_single/main.py` updated and
merged to `main`. `record.json` and `queue.md` updated.
