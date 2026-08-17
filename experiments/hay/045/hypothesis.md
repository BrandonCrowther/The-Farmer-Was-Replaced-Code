# exp-045 — unlock-level-check

**Hypothesis.** docs/wiki/Unlocks.md documents a `Unlocks.Grass` unlock
("Increases the yield of grass") that is entirely separate from
`Unlocks.Polyculture` and has never been checked in this project's history
(no prior experiment mentions it). If leaderboard runs don't actually start
with it maxed despite the general "all unlocks, fully upgraded" claim, this
is a real yield lever independent of every companion-servicing question
chased tonight.

**Variable.** None — pure read.

**Metric.** `num_unlocked(Unlocks.Grass)` vs. its max level (10, per
Unlocks-Data.md's `grass` cost array length), and whether `get_cost`
reports a further affordable upgrade.

**Baseline.** Assumed max (per Simulation.md's `sim_unlocks = Unlocks`
semantics for full-unlock categories) — never independently verified.

**Procedure.**
1. `saves/hay/main.py`: read and print the levels, 0-tick.
2. `tools/cycle.sh hay exp-hay-045-r1 --from <worktree>`.
3. Read `OUTPUT=`.

**Falsifier.** If `GRASS_LEVEL` is already at its max (10), this unlock is
already fully captured in the measured 512/81,920 figures and isn't a new
lever. If it's below max, that's a real, previously unexamined gap.
