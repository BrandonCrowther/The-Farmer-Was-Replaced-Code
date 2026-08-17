# exp-001 — terminate the seeded achievement driver

**Hypothesis.** The seeded `saves/sunflowers/main.py` (32 drones, each
farming its own column of the 32x32 world, continuous harvest+replant,
base yield only — no max-petal bonus tracking) just needs an endless
`while True:` replaced with a target check to terminate and score.
Unlike `saves/hay/main.py`'s documented water-supply shortfall (32
drones sharing a limited Water pool spun forever on failed
`use_item()` calls when the threshold couldn't be sustained), this
driver's `while get_water() < 0.75: use_item(Items.Water)` has the same
unguarded shape — add the `num_items(Items.Water) > 0` guard
defensively before running the real scored attempt, since a hang here
would be expensive to discover mid-run.

**Variable.** Seeded `while True:` per-drone loop (never terminates) →
`while num_items(Items.Power) < TARGET:`, same condition checked by the
main drone so it doesn't return before its spawned drones finish.
Also: guard the water-topup loop against depletion.

**Metric.** The completion modal's verdict and displayed time — this
category's first-ever leaderboard entry.

**Baseline.** None — first attempt for this category. Target: 100,000
Power (Leaderboard.md).

**Procedure.**
1. `saves/sunflowers/main.py`: target-gate both the spawned-drone loop
   and the main drone's loop, guard the water topup.
2. `tools/cycle.sh sunflowers exp-sunflowers-001-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If the run hangs or times out, check the water guard
first (matching Hay's documented failure mode) before assuming
anything about the sunflower-farming logic itself is broken.
