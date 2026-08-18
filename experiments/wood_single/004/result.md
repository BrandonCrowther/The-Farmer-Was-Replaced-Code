# exp-004 — measure Tree's real growth, then apply Hay's playbook — result

**Outcome.** **Adopted, new champion.** 09:17.980, Global Rank #93 —
down from 002's 31:59.849/#232. A real **-22:41.869 (-70.9%), +139
ranks** — by far the largest single win of the entire overnight
session, and the first time a *macro*-level redesign (not just a
ported micro-fix) has landed for `wood_single`.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| `simulate()` growth measurement (water sustained 0.999) | 4,412 ticks | vs. 001's unwatered 34,718 — 7.87x |
| offline Python coverage check | 42 positions, 4 bases, all pairwise non-cardinal | exact match to the live run's own count |
| live validation (target = inventory + 100,000) | `PLANTED_COUNT 42`, clean completion, no warnings | two parser bugs found and fixed first (see hypothesis.md) |
| smoke test (200 cycles) | **2,682.46 ticks/harvest** (windows 2,486–3,039) | vs. 002's real 9,551 |
| real (target=500,000,000) | **09:17.980, #93** | `VERDICT=scored` |

**Baseline.** 002: 31:59.849, #232.

**Delta.** -22:41.869 (-70.9%), +139 global ranks.

**Verdict.** Confirms the whole chain of reasoning end to end: 003's
mechanic measurements (destructive unripe-harvest, no auto-regrow
exception) were real but didn't block the design; 004's growth
re-measurement (4,412 vs. 34,718) was the actual unlock, matching the
project's own repeated lesson that a constant carries its measurement
conditions with it; and Hay's 069/070 playbook (full pre-seed + tile
count sized to hide growth, adapted here to 4 diagonal tiles for
Tree's cardinal-neighbor constraint) transferred cleanly once the real
numbers were in hand. The smoke test's 2,682-tick projection came in
close to what the real run implies (09:17.980 for ~1,221+ harvests is
consistent with a ~2,700-3,000 real ticks/harvest average given the
leaderboard's internal-repeat-averaging). New leader gap: ~2.63x
(09:17.980 vs the live leader's 03:32.980, itself updated since 002's
measurement) — down from 9.6x, and now in the same rough range as
Hay(multi)'s own remaining gap rather than a wildly separate order of
magnitude. `saves/wood_single/main.py` updated and merged to `main`.
`record.json` and `queue.md` updated. Worth checking whether other
Tree-adjacent or long-growth categories have the same kind of
unmeasured-constant gap before assuming this design is fully tuned —
water threshold (kept at 0.999, unexamined) and tile count (4, sized
from a rough per-visit-cost estimate, not independently verified) are
both plausible next levers, mirroring Hay's own post-070 tuning arc
(071-082).
