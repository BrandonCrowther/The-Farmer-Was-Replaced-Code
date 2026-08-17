# exp-071 — find the real source of 070's 145-tick/harvest gap

**Hypothesis.** 070's result.md guessed the gap between predicted
(814.69) and measured (959.57) ticks/harvest was water decaying further
over the longer two-tile revisit interval. That guess doesn't survive
the math: Watering.md says the ground loses ~1% of its *current* water
per second; over both the single-tile (~0.176s) and two-tile (~0.316s)
revisit intervals, water only drops from 0.999 to ~0.996-0.997 either
way — nowhere near enough of a difference to explain 145 ticks via
extra `use_item()` calls. Rather than guess again, instrument every
category of tick spend directly (water, wait, harvest, reroll, move)
and let the categories sum to the measured total.

**Variable.** None — pure instrumentation of the unmodified 070 design.

**Metric.** Per-category ticks/harvest (water, wait, harvest, reroll,
move), plus a sum-of-categories-vs-elapsed check to catch anything
missed.

**Baseline.** 070: predicted 814.69 (harvest+reroll+hop only, no water
modeled at all), measured 959.57.

**Procedure.**
1. `saves/hay/main.py` (as `zzDriver.py`): same two-tile layout as 070,
   with `get_tick_count()` deltas wrapped around each category of work
   inside `service_tile()` and around the inter-tile move.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, poll `output.txt`.

**Falsifier.** If the categories don't sum close to the measured total,
something is happening outside the instrumented boundaries and the
breakdown itself is incomplete.
