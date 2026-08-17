# exp-072 — water threshold + direct move: closing 071's measured gaps

**Hypothesis.** 071's real category breakdown identified two concrete,
fixable costs: water top-off (62.76/harvest, 0.276 calls/harvest) and
`Common.move_to()`'s wrapper overhead (226 vs a bare 200 for one hop).
Lowering the water threshold to 0.75 should cut top-off frequency
sharply — growth still finishes in ~518 ticks at that speed (base 1x
time 2073 / 4x speed), comfortably inside the ~900-tick away-window
that 071 confirmed is fully idle (`wait≈1`) — and using a direct
`move(East)`/`move(West)` for the known single-hop direction should
drop `move` to ~200.

**Variable.** Water threshold: 0.999 → 0.75. Movement: `Common.move_to()`
→ direct `move()` call. Both changed together — the breakdown
instrumentation from 071 carries over unchanged, so each category's
contribution is still directly attributable without separate runs.

**Metric.** Same per-category breakdown as 071, plus total
ticks/harvest.

**Baseline.** 071: 999.41 ticks/harvest (water 62.76, move 226, reroll
482.63, harvest 200, wait 1).

**Procedure.**
1. `saves/hay/main.py` (as `zzDriver.py`): same two-tile layout and
   instrumentation as 071, `WATER_THRESHOLD = 0.75`, inter-tile move
   replaced with direct `move(East)`/`move(West)`.
2. Smoke test only — no `zzRunner.py` in this deploy.
3. `tools/tfwr.sh run`, poll `output.txt`.

**Falsifier.** If `wait` rises meaningfully above ~1, the lower water
threshold pushed growth time past the away-window and the margin was
too aggressive. If `water` or `move` don't drop close to their
predicted floors, the attribution from 071 was wrong.
