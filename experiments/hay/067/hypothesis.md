# exp-067 — does the champion's exact reroll pattern (no ripeness check) match 066's cost?

**Hypothesis.** 066 measured `instructions()` at 7 ticks and confirmed
Grass auto-regrows, but only ever called `harvest()` after confirming
`can_harvest()` first. The champion's actual reroll loop calls
`harvest()` on a just-regrown (presumably immature) tile with no
ripeness check at all. `harvest()`'s doc says cost depends on whether an
entity was *removed*, not whether it was ripe — so this should still
cost 200, not fail cheap at 1 tick. Confirm directly, in the exact
pattern the champion uses.

**Variable.** None — reproduces the champion's literal reroll call
sequence and instruments it.

**Metric.** Tick cost and Hay yield of `harvest()` called immediately
after a prior harvest, with no `can_harvest()` check in between, six
times in a row.

**Baseline.** 066: `instructions()` = 7 ticks, `harvest()` (ripeness
confirmed first) = 200 ticks.

**Procedure.**
1. `saves/hay/main.py`: harvest once (ripeness confirmed), then 6x
   `harvest()` with zero ripeness checks, printing ticks/yield/state
   each time.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, read `output.txt`.

**Falsifier.** If any reroll-pattern `harvest()` costs 1 tick (fails) or
yields nonzero Hay, the champion's real reroll cost differs from 066's
finding and needs its own correction.
