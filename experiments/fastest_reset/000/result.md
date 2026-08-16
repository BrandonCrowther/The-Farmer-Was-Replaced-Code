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

Three runs of this same driver, unchanged apart from file names:

| run | time |
| --- | --- |
| before restructure (`000-e2e-validation`) | 15:23:55.099 |
| after restructure | 15:13:15.781 |
| after the zzRunner rename | 15:19:53.359 |

**The noise floor is ~10.7 minutes.** None of these differences mean anything —
the code is identical. No single run can prove an improvement smaller than that,
which is what `002 sim-variance` exists to pin down properly.

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

## How window targeting was solved

Selecting the harness window needs a click, and the click needs a coordinate that
survives category switches. Four things were measured:

1. A reload with an **unchanged file set** restores the layout pixel-identically.
2. Every code window with no saved position opens at the **same** default spot —
   they stack, they do not cascade.
3. The window on top is the file whose name **sorts last, case-insensitively**.
   With `{Common, main, Runner}` the top window was `Runner`; add `Sim` and the
   top became `Sim`.
4. Dragging a window somewhere better **does not survive a reload**: positions
   live in `save.json` and, with autosave disabled, the game only writes them on
   an explicit save. The dragged position was silently lost on the next load.

So the harness is named `zzRunner.py` in every category. It wins the ordering, so
it is always the top window at the fixed default position, whatever else is
deployed — no dragging, no saving, no per-category layout to maintain. Verified
by running `tools/tfwr.sh run` with no coordinate override after a category
switch and a reload.

Also worth knowing: the window title is an **editable name field**. Dragging by
the title text puts it into rename mode instead of moving the window; the drag
has to grab empty title-bar space.
