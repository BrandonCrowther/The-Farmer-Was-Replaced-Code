# exp-001 — terminate

**Hypothesis.** The seeded Hay driver already reaches 2e9 hay; it just never
stops, so it never scores. Bounding every drone's loop by
`num_items(Items.Hay) < TARGET` and reaping the spawned drones with `wait_for`
will make the run end and report a time.

**Variable.** Loop termination only. The farming strategy — 36 drones on a 6x6
grid of 5-spaced plots, grass with polyculture companions — is untouched.

**Metric.** The run completes and the completion modal reports a time at all.
Read from the modal with vision on `tools/tfwr.sh capture`.

**Baseline.** None. `experiments/hay/record.json` has `personal_best: null` and
the seed at `2335f39` cannot finish by construction.

**Procedure.**
1. `tools/deploy.sh hay --from ~/dev/tfwr-worktrees/hay-001`.
2. The file *set* changes (the live save still holds the achievement scripts),
   so exit 10 `RELOAD_REQUIRED` is expected: Escape → Load → Save0.
3. `tools/tfwr.sh run`, then `wait-result`.
4. `tools/tfwr.sh capture` and read the modal.
5. Record the time and whether the run was accepted as successful.

**Risks.**
- A drone stuck in the ripeness wait would hang the run past `wait-result`'s
  timeout. The wait is bounded by the target check for exactly this reason.
- The leaderboard's farm may be smaller than the 32x32 the 6x6 spawn grid
  assumes, or the drone cap lower than 36. `spawn_drone` returning `None` is
  handled; an out-of-bounds `move_to` is not, and would show as a stalled run.
- Steam Cloud restored the original save once already on a game restart. If the
  game is restarted mid-experiment, re-deploy before trusting a result.
