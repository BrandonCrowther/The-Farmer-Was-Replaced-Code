# TFWR automation — plan of record

Goal: an unattended Claude session that writes and iterates game code through the
External Editor integration, runs experiments, reads the results back, and keeps
the journal in git.

Phases 1 and 2 are **done**; this document records what was built, what was
measured on this machine, and what Phase 3 still has to decide.

---

## Hard constraint: `save.json` is off limits

The game owns `save/Save0/save.json`. We do not read it as a telemetry source and
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

1. Write the variant into `save/Save0/<Name>.py`.
2. Wait for File Watcher pickup (see the measured latency below).
3. Click the `Leaderboard_run` window to select it (needs `ydotool` — F5 alone
   does not start a run; see `mcp/README.md`), then press F5 with
   `tools/tfwr.sh run`.
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
| Does File Watcher work through the save symlink | **yes** — probe wrote through `save/Save0/`, the game rendered the change |
| Key injection without root | **partly** — `sendshortcut` delivers keys (menu opens/closes, `W`/`S` pan the camera) |
| Starting a run with F5 alone | **no** — F5 does nothing as keysym or as `code:71`, focused or not; execution starts only with a code window selected, and selection needs a click |
| Mouse clicks without root | **no** — needs `ydotool`, so `tools/setup_input.sh` is a prerequisite, not an extra |
| Capture while game is on another workspace | **broken and silent** — `grim` photographs the visible workspace instead; `tools/tfwr.sh` switches and restores |
| File Watcher enabled | yes (`options.txt`: `file watcher = enabled`) |

Recommended settle: poll at ~0.5 s intervals up to a 3 s cap rather than a fixed
sleep, and confirm pickup by diffing a tight screenshot crop of the editor before
pressing F5. There is no explicit "reload done" signal from the game.

## Repo layout

```
docs/          wiki mirror (59 pages) + authoritative __builtins__.py snapshot
save/Save0/    the actual game scripts — the Proton save folder symlinks here
experiments/   queue.md backlog + one directory per experiment
mcp/           automation stack evaluation and decision
tools/         tfwr.sh driver, fetch_wiki.py, setup_input.sh
logs/          screenshots and run artifacts (gitignored)
backups/       zip snapshots (gitignored)
```

The symlink runs **repo → game**, not the other way around: the real files live
in `save/Save0/` and
`…/TheFarmerWasReplaced/Saves/Save0` is a symlink pointing at them. The plan
originally had it reversed, but git does not follow a symlinked directory — it
would have stored the link and tracked nothing. This direction is also why the
code survives a Proton prefix rebuild.

## Phase 3 — experiment workflow (not yet built)

1. `experiments/queue.md` holds the backlog: one entry per idea, each with a
   hypothesis and a target metric.
2. Per item: write the variant, wait for pickup, run, capture, read, write
   `result.md`, commit as `exp-NNN: <slug>, <outcome>`.
3. The commit log is the journal.

### Still to decide

- **Loop shape.** Long-running Claude Code session with a bash loop, or a systemd
  timer re-invoking Claude per queue item.
- **Stop condition.** Queue empty, wall-clock budget, or consecutive-failure
  threshold — needed so a bad variant cannot burn the night.
- **Run verification.** F5 into an unselected window is a silent no-op, and the
  screenshot of a farm that did not start looks much like one that did. Every run
  needs a positive signal that execution actually began — the cleanest is a
  `quick_print` marker emitted as the first statement of the harness script, so
  its absence means the run never started.
- **Seed the queue.** Depends on what is left to optimize now that the save is at
  100% achievements — most likely leaderboard categories.

## Open risks

- A crash or a modal dialog leaves the loop pressing F5 into a window that is not
  running anything. Every result read should verify the window title and state in
  the screenshot before trusting a number.
- Workspace switching during capture is visible to anyone at the machine, and a
  user interacting at the same time can steal focus mid-run.
