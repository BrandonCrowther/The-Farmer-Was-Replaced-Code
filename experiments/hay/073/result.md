# exp-073 — first real leaderboard run of the two-tile champion — result

**Outcome.** **Adopted, new champion.** 02:00.734, Global Rank #65 —
down from 02:42.421/#111. A 41.687-second, 25.7% real improvement, 46
ranks gained. The single-drone smoke-test findings (068-072) fully
generalized to the real 32-drone macro-layout on the first real
attempt.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| validation (target=200,000, no `zzRunner.py`) | `VALIDATE_DONE bad 0 of 64` | zero crop-tile collisions across all 32 drones × 2 tiles |
| real (target=2,000,000,000) | **02:00.734, #65** | `VERDICT=scored` |

**Baseline.** 057: 02:42.421, #111.

**Delta.** -41.687s (-25.7%), +46 global ranks.

**Verdict.** The macro-layout risk flagged at the end of 070 — fitting
tile-pairs into the 32-drone grid without neighbor bush-wall conflicts
— resolved cleanly: reusing the champion's existing spacing-5 grid with
each drone's second tile offset `+1` east left just enough margin
(confirmed both by geometry and by a live, zero-cost validation check
before committing to the real 2-hour-equivalent run), and overlapping
bush walls between neighbors are harmless by construction since every
drone wants the same static Bush at any shared position — only the
actual crop tiles needed protecting, and the global `ALL_CROPS`
exclusion set handled that with no observed failures. This validates
the entire chain of reasoning from 066 through 072: the corrected
207-tick reroll cost, the 615-tick perfect-timing floor, the growth-
hiding mechanism, and the water/move micro-optimizations all held up
under real, adopted, scored conditions — not just single-drone
approximations. `saves/hay/main.py` updated and merged to `autofarmer`.
`record.json` and `queue.md` updated to reflect the new champion.
