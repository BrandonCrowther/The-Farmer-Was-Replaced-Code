# exp-075 — drop instructions() from the hot loop — result

**Outcome.** **Adopted, new champion.** 01:58.059, Global Rank #63 —
down from 02:00.734/#65. A real 2.675-second improvement, +2 ranks —
smaller than 073's structural change, exactly as expected for a
~17-22-tick/harvest micro-optimization on top of an already-optimized
design.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| single-drone smoke test (900 cycles) | 873.02 ticks/harvest | down from 074's 889.78 (real champion baseline), -16.76 |
| validation (target=200,000, no `zzRunner.py`) | `VALIDATE_DONE bad 0 of 64` | zero crop-tile collisions |
| real (target=2,000,000,000) | **01:58.059, #63** | `VERDICT=scored` |

**Baseline.** 073/074: 02:00.734, #65, measured 889.78 ticks/harvest.

**Delta.** -2.675s, +2 global ranks (real run). -16.76 ticks/harvest
(smoke test).

**Verdict.** The optimization worked exactly as reasoned — no surprises,
no interaction effects with the reroll chase's memory lookups. This is
now within striking distance of the cluster's own upper bound: smoke-
test ticks/harvest (873.02) is only 17 ticks above 856. The remaining
gap is almost entirely `reroll` (structurally floored at p=1/3 per 069)
— there is no further concrete lever identified. `saves/hay/main.py`
updated and merged to `autofarmer`. `record.json` and `queue.md`
updated.
