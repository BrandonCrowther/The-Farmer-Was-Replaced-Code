# exp-070 — two-tile interleaving hides the growth wait behind a sibling's reroll-chase

**Hypothesis.** Ticks are a single global clock — growth is a passive
function of elapsed ticks since last replant, independent of where the
drone physically is. A single-tile drone (068/069) wastes the 415-tick
growth wait doing nothing. A drone alternating between two adjacent
Hay tiles (distance 1, all-static-bush companion policy per 069v2)
should get that wait for free: the sibling tile's own local service
(harvest + reroll-chase, ~628 ticks average, no walk) already exceeds
415, so growth is fully hidden by the time the drone returns.

**Variable.** Single tile (068/069 baseline) vs. two adjacent tiles,
round-robin, shared bush-wall companion setup (see the layout
illustration in the conversation — 30 static Bush tiles covering the
union of both tiles' radius-3 diamonds, minus the two tiles themselves).

**Metric.** Same windowed ticks/harvest measurement as 068/069, 900
total harvests split across both tiles, single drone, no target gate.

**Baseline.** 069v2: 1068.35 ticks/harvest, single tile, all-static
bush, avg 2.07 rerolls/cycle. Predicted for two-tile: harvest(200) +
reroll(207×~2.0) + hop(200) ≈ 815-828.

**Procedure.**
1. `saves/hay/main.py` (as `zzDriver.py`): plant both crop tiles, one-
   time setup pre-seeding 30 shared Bush positions (excluding both crop
   tiles), then round-robin service loop with windowed reporting.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, poll `output.txt`.

**Falsifier.** If measured ticks/harvest doesn't drop meaningfully below
069v2's 1068.35, the growth-hiding mechanism doesn't work as modeled in
practice (e.g. an unmodeled per-visit cost, like water decaying further
over the longer inter-visit interval, eats the predicted gain).
