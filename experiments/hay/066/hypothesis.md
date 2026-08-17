# exp-066 — does harvest() auto-replant Grass?

**Hypothesis.** User pushback on the "400-tick own-handling floor"
explanation: `harvest()`'s doc says only "returns True if an entity was
removed," with no mention of replanting, and there's no Replant unlock
in the game — but per this project's own rule, a conclusion needs a
test that is not a full run. Direct test: plant grass, harvest it
repeatedly, and watch `get_entity_type()` and `get_companion()` across
several cycles *without ever calling `plant()` again* to see whether the
tile actually goes empty (matching the doc-only reading) or regrows on
its own.

**Variable.** None — pure observation across repeated harvest cycles on
one tile.

**Metric.** `get_entity_type()` immediately after `harvest()` (None vs
Grass), `get_companion()` per cycle (does it change without a `plant()`
call), and the tick cost of the champion's actual post-harvest call
(`instructions()`, a guarded `plant(Grass)`) once entity_type never
leaves Grass.

**Baseline.** My prior claim: 400 = `harvest()` (200) + `instructions()`
→ `plant()` (200), paid every cycle including every reroll attempt.

**Procedure.**
1. `saves/hay/main.py`: plant once, then loop `harvest()` +
   `instructions()` 6 times, printing tick costs and state each time.
2. Smoke test only — no `zzRunner.py` in this deploy, nothing here can
   trigger a real `leaderboard_run()`.
3. `tools/tfwr.sh run`, read `output.txt`.

**Falsifier.** If `entity_type` ever reads `None` after `harvest()`, or
if `instructions()` costs 200 (meaning `plant()` actually fired), the
400-tick claim stands as originally stated.
