# exp-048 — Megafarm unlock check — result

**Outcome.** rejected — confirmed genuinely maxed, no lever here.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `MAX_DRONES` 32, `MEGAFARM_LEVEL` 5, `MEGAFARM_COST {}` | matches other maxed unlocks' empty-cost pattern |
| r1 | `unlock(Unlocks.Megafarm)` → `UNLOCK_ATTEMPT_RESULT False`, `NEW_MAX_DRONES` 32 (unchanged) | live confirmation, not just an inferred-from-cost guess |

**Baseline.** None — first direct check of this unlock tonight.

**Noise floor.** N/A — deterministic query.

**Screenshots.** None — probe.

**Verdict.** 32 drones is a hard cap for this save, confirmed by an
actual failed `unlock()` attempt, not just an empty `get_cost()` (which
turned out to be ambiguous — 052 later found `Fertilizer` shows the
same empty cost while genuinely still maxed too, so the live-attempt
check is the reliable signal). No drone-count lever available.
