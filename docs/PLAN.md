# TFWR automation — plan of record

Goal: an unattended Claude session that writes and iterates game code through the
External Editor integration, runs experiments, reads the results back, and keeps
the journal in git.

Phases 1 and 2 are **done**; this document records what was built, what was
measured on this machine, and what Phase 3 still has to decide.

---

## Hard constraint: `save.json` is off limits

The game owns `live/save.json`. We do not read it as a telemetry source and
we never write it. It is gitignored precisely so that a checkout, stash, or reset
can never put a stale save under a running game.

That removes the plan's original "just parse the save file" shortcut, so all
measurement goes through the game's own code execution instead — which is more
faithful anyway, because it measures what the runtime actually did.

## Telemetry: the `Leaderboard_run` channel

Live state is measured by running code in an in-game code window and reading its
output, not by inspecting files.

Two facts from `docs/api/__builtins__.py` make this precise rather than
screenshot-guesswork:

- **`simulate(filename, unlocks, items, globals, seed, speedup) -> float` returns
  the run time.** A harness can capture that number as a value, not a stopwatch
  reading.
- **`quick_print()` costs 0 ticks** and writes to the output page, so
  instrumentation does not perturb the thing being measured. (`print()` costs a
  full second of drone time — never use it for benchmarking.)

The measurement loop:

1. Write the variant into `saves/<category>/` and `tools/deploy.sh <category>`.
2. Wait for File Watcher pickup (see the measured latency below).
3. `tools/tfwr.sh run` — it clicks the harness window to select it (needs
   `ydotool`; F5 alone does not start a run) and verifies the run began.
4. `tools/tfwr.sh capture` and read the numbers with vision.
5. Record in `experiments/<NNN-slug>/result.md`, commit.

Make the output easy to read: emit few values, one per line, with a fixed marker,
e.g. `quick_print("RESULT", seed, run_time)`. Machine-legible in a screenshot
beats dense tables.

The resource bar along the top of the window is a useful cross-check but is
rounded for display (`53B`, `11.1B`), so it confirms magnitudes, not deltas.
**Do not OCR it with tesseract** — it misread `11.1B` as `1B` and merged adjacent
counters. Use vision.

## Measured on this machine

| Question | Answer |
| --- | --- |
| File Watcher pickup latency for an external write | **between 0.66 s and 1.32 s** — unchanged at 0.66 s, changed at 1.32 s, over a 16-frame probe |
| Does File Watcher work through the save symlink | **yes** — probe wrote through the symlinked save dir, the game rendered the change |
| Key injection without root | **partly** — `sendshortcut` delivers keys (menu opens/closes, `W`/`S` pan the camera) |
| Starting a run with F5 alone | **no** — F5 does nothing as keysym or as `code:71`, focused or not; execution starts only with a code window selected, and selection needs a click |
| Mouse clicks without root | **no** — needs `ydotool`, so `tools/setup_input.sh` is a prerequisite, not an extra |
| Capture while game is on another workspace | **broken and silent** — `grim` photographs the visible workspace instead; `tools/tfwr.sh` switches and restores |
| File Watcher enabled | yes (`options.txt`: `file watcher = enabled`) |
| Full loop, end to end | **works** — select, F5, run, read result, dismiss; `Fastest_Reset 15:23:55.099`, ~2 min wall clock. See `experiments/000-e2e-validation/` |
| Does a leaderboard run disturb the main save | **no** — resource bar returned to its pre-run values afterwards |
| Harness window targeting | **solved** — windows stack at one default spot and the alphabetically-last filename is on top, so the harness is `zzRunner.py` everywhere and always sits at a fixed, clickable coordinate |
| Do dragged window positions persist | **no** — positions live in `save.json`, which the game only writes on an explicit save (autosave is off) |
| "Did the run start?" signal | the top banner's timer **ticks**; `tools/tfwr.sh state` samples it twice and compares |
| Restructured layout, end to end | **works** — deploy, reload, run, read: `Fastest_Reset 15:13:15.781`, `experiments/fastest_reset/000/` |
| Noise floor | **~10 min** — identical code scored 15:23:55 and 15:13:15 on two runs |

Recommended settle: poll at ~0.5 s intervals up to a 3 s cap rather than a fixed
sleep, and confirm pickup by diffing a tight screenshot crop of the editor before
pressing F5. There is no explicit "reload done" signal from the game.

## Repo layout

```
saves/<category>/   source of truth per leaderboard category (16 of them)
live/               what the game reads; deployed copies + the game-owned files
docs/               wiki mirror, API snapshot, generated leaderboards.md
experiments/<cat>/  queue.md, record.json, one directory per experiment
tools/              deploy.sh, tfwr.sh, new_experiment.sh, render_leaderboards.py
mcp/                automation stack evaluation and decision
logs/               screenshots and run artifacts (gitignored)
```

`Saves/Save0` symlinks at `live/`, and that symlink never moves. `tools/deploy.sh`
copies one category's files in. The live directory is deliberately a real
directory rather than a symlink that swings between category folders: the
game-owned `save.json` lives there, and an atomic rewrite by the game would
replace a swinging symlink with a real file and fork the save.

## Phase 3 — experiment workflow

Per queue item, driven from `autofarmer`:

1. `tools/new_experiment.sh <category>` → worktree + `auto_experiment/<cat>/<NNN>`.
2. Edit `saves/<cat>/`, then `tools/deploy.sh <cat> --from <worktree>`.
   Exit 10 means the file set changed and the save needs a reload first.
3. `tools/tfwr.sh run` — selects the harness window, F5, and **fails loudly** if
   the run did not start.
4. `tools/tfwr.sh wait-result`, read the modal, `tools/tfwr.sh dismiss`.
5. Write `result.md`, update `record.json`, commit, push the branch.
6. Beat the PB? Re-run to confirm against the ~10 min noise floor, then merge into
   `autofarmer` and re-render `docs/leaderboards.md`.

### Still to decide

- **Loop shape.** Long-running Claude Code session with a bash loop, or a systemd
  timer re-invoking Claude per queue item.
- **Stop condition.** Queue empty, wall-clock budget, or consecutive failures.
- **Termination.** Every seeded category is an endless `while True` achievement
  farmer. A leaderboard run only scores if the program ends — item 001 in each
  queue.

## Open risks

- A crash or a modal dialog leaves the loop pressing F5 into a window that is not
  running anything. Every result read should verify the window title and state in
  the screenshot before trusting a number.
- Workspace switching during capture is visible to anyone at the machine, and a
  user interacting at the same time can steal focus mid-run.
