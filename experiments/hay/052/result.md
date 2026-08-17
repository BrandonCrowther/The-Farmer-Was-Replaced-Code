# exp-052 — check every remaining unlock level, including Speed — result

**Outcome.** rejected — every checked unlock confirmed maxed, no lever.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `Unlocks.Speed` level 5, `Unlocks.Grass` 10, `Unlocks.Polyculture` 5, `Unlocks.Watering` 9, `Unlocks.Megafarm` 5, `Unlocks.Fertilizer` 4, `Unlocks.Carrots` 10, `Unlocks.Trees` 10, `Unlocks.Expand` 9 | all show `cost {}` |
| r1 | `TICKS 4002 REAL_TIME 0.66 TICKS_PER_SEC 6074.97` | a trivial busy-loop, cross-checking the tick-rate constant directly — matches every prior measurement exactly |
| r3 | `unlock(Unlocks.Speed)` → `False`, level unchanged; `unlock(Unlocks.Fertilizer)` → `False`, level unchanged | live confirmation both are genuinely maxed |

**Baseline.** 045: Grass/Polyculture/Watering checked and maxed. 048:
Megafarm checked and maxed.

**Noise floor.** N/A — deterministic queries.

**Screenshots.** None — probe.

**Verdict.** `Unlocks.Speed` ("increases the speed of both the drone
and code execution") was a genuinely new, previously-unchecked
hypothesis — if it affected the ticks-per-real-second conversion
(not just raw tick counts), an unmaxed level could have explained a
real-time gap independent of tick-level logic. Confirmed maxed via a
live `unlock()` attempt, and the direct `TICKS_PER_SEC` measurement
(6,074.97, matching exp-043 exactly) confirms the conversion itself is
correct and stable. Every unlock this project can check is now
confirmed maxed — closes the "we're missing a purchasable upgrade"
line of inquiry for real.
