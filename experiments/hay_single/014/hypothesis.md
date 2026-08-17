# exp-014 — adjacent-tiles-reroll-guard

**Hypothesis (per the user's challenge to 013's conclusion).** Two
adjacent tiles (distance 1, cheapest possible commute), sharing memory and
using the full REROLL_LIMIT=5 champion logic with a same-tile guard, might
beat single-tile's proven ~1,200-ticks/harvest ceiling — testing the one
combination (reroll-before-walk × multi-tile) 005/006 never tried, since
reroll-before-walk didn't exist when those ran.

**Variable.** Single tile (012's champion) → two adjacent tiles, shared
memory, same-tile guard instead of distance-based avoidance.

**Metric.** Tail-window ticks/harvest, same computation as every prior
probe, compared against 012's real ≈68.7 hay/tick (≈1,192 ticks/harvest).

**Baseline.** 012 (champion): ≈68.7 hay/tick real. 011's model: the
reroll-only asymptote is ≈1,200 ticks/harvest for *any* tile count (my own
prediction here, stated before running: two adjacent tiles should land
near ≈1,400 ticks/harvest — *worse* than single-tile — because commute is
pure overhead once growth is already fully hidden and the service-cost
floor doesn't improve with tile count).

**Procedure.**
1. `saves/hay_single/main.py`: two tiles at `(0,0)` and `(0,1)`, shared
   `planted` dict, same-tile guard, `REROLL_LIMIT=5`, 150 cycles.
2. `tools/cycle.sh hay_single exp-hay_single-014-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute tail-window ticks/harvest and compare directly
   to 012's real number.

**Falsifier.** Stated in the code comment and above: if this beats 012's
real throughput, the model is wrong about something (it has undershot
reality twice before tonight) and multi-tile reopens as a real lever — in
which case say what the model missed, don't just report the win. If it
lands worse, as predicted, that's the third and most rigorous closure of
multi-tile (schedulability, self-collision, commute — this time with the
best mitigations for all three already applied) and the pivot to Hay
stands confirmed.
