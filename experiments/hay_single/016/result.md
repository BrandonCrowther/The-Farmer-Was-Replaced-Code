# exp-016 — port Hay(multi)'s two-tile champion — result

**Outcome.** **Adopted, new champion.** 03:08.281, Global Rank #89 —
down from 03:57.198/#169. A 48.917-second, 20.6% real improvement, 80
ranks gained — an even bigger rank jump than Hay(multi)'s exp-073.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| auto-regrow confirmation (6 cycles, no `plant()`) | `instructions_ticks` 7 (6/6) | matches Hay-multi's exp-066 exactly, in this leaderboard's own 8x8/single-drone context |
| validation (target=100,000, no `zzRunner.py`) | `VALIDATE_C1 Entities.Grass`, `VALIDATE_C2 Entities.Grass` | no self-collision — both crop tiles survived the bush-wall setup |
| real (target=100,000,000) | **03:08.281, #89** | `VERDICT=scored` |

**Baseline.** 012: 03:57.198, #169.

**Delta.** -48.917s (-20.6%), +80 global ranks.

**Verdict.** The auto-regrow correction and the two-tile interleaving
design both transferred cleanly from Hay(multi) to `hay_single` with no
adaptation beyond the world size and drone count already being handled
generically (both designs compute everything from `get_world_size()`
and the drone's own position, nothing hardcoded to 32x32). Single-drone
categories have no macro-layout risk at all — the only failure mode
checked was self-collision (the bush-wall setup accidentally
overwriting the drone's own second crop tile), and the design's
explicit exclusion check handled it with zero observed failures, same
as Hay-multi's neighbor-exclusion check. This confirms the underlying
insight (auto-regrow entities can hide their growth wait behind a
sibling tile's reroll-chase) is a property of the *entity*, not the
leaderboard, and is worth checking against any other Grass-farming
category before assuming it's Hay-specific. `saves/hay_single/main.py`
updated and merged to `autofarmer`. `record.json` and `queue.md`
updated to reflect the new champion.
