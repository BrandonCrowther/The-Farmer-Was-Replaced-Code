# exp-000 — restructure verification — result

**Outcome.** adopted — the per-category layout runs end to end and reproduces a
valid leaderboard time.

Numbered 000 because this validates the *plumbing*, not a code change. Real
experiments for this category start at 001.

## Result

| field | value |
| --- | --- |
| leaderboard | Fastest_Reset |
| this run | **15:13:15.781** |
| personal best | 15:11:42.399 (stood) |
| global rank | #834 |
| code | `saves/fastest_reset/` deployed to `live/`, entry `main` |

For reference, the same driver scored 15:23:55.099 before the restructure
(`experiments/000-e2e-validation/`). The ~10 min difference is run-to-run
variance, not an improvement — the code is byte-identical apart from file names.
That spread is exactly why `002 sim-variance` exists: **the noise floor is at
least 10 minutes**, so no single run proves anything smaller.

## The path that was verified

1. `tools/deploy.sh fastest_reset` → `live/`, stale files removed, `RELOAD_REQUIRED`
2. save reload via the Load menu (needed because the file set changed)
3. `tools/tfwr.sh run` → selects the harness window, F5, verifies it started
4. `tools/tfwr.sh wait-result` → blocked ~2 min, returned on the modal
5. read the modal, `tools/tfwr.sh dismiss`, farm back to 53B / 75B / 11.1B

## Two bugs this caught

**Missing modules.** `Full_Reset_Algs.py` imports `Cactus`, `Dinosaurs` and
`Mazes`; the first migration copied only `Common.py`. The run started, then froze
at `00:00.052` with an ERROR tooltip — it does not fail fast, it burns the run.
`tools/deploy.sh` now refuses to deploy a category that imports a module it does
not contain.

**Run detection, twice wrong.** Sampling the harness title bar broke as soon as
the game re-laid-out its windows on reload. Replacing it with a contrast test on
the top banner then read the *completion modal's* text as a running timer. What
works is motion: sample the banner twice and compare — a run's timer ticks, a
modal does not.
