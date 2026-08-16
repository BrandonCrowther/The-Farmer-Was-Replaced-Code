# Handoff — 2026-08-16, 01:10

The overnight loop ran from 23:45 to 01:05 and stopped early: **the game
crashed.** Everything is committed and pushed; nothing is half-finished.

## First, two things to do by hand

1. **Re-enable idle locking:** `omarchy-toggle-idle`. It was turned off so the
   screen would not lock mid-run. Waybar shows the state.
2. ~~Restart the game through Steam.~~ **Done, and now automated.** The crash was
   recovered at 01:15 and the protocol is `tools/tfwr.sh relaunch`: kill the
   game, restart through Steam, wait for the window, reload to canonical state.
   The save came back intact and Steam Cloud did *not* clobber the deployed
   code, though `cycle.sh` hashes it every run regardless.

## Where Hay got to

**04:55.320 → 03:24.552. A 30.8% improvement, global rank #422 → #232.**

| exp | change | result |
| --- | --- | --- |
| 001 | terminate the endless farmer | 04:55.393 — scores at all for the first time |
| 002 | baseline, 3 runs | 04:55.320, noise floor **0.15 s** |
| 003 | plant grass on unaffordable companion tiles | rejected, +1.23 s |
| 004 | **plant the tree a Tree request asks for** | **03:40.911, −25.2%** |
| 005 | move the fix into shared `Common` | 03:40.911, unchanged — confirms 004 |
| 006 | reroll an unaffordable companion | rejected, +0.10 s (inside the floor) |
| 007 | diagnostic: farm state | tile always holds grass; companion faces are uniform thirds |
| 008 | plot rotation | rejected, **~59x slower** |
| 009 | diagnostic: tick accounting | busy-wait is **0.2%** of ticks |
| 010 | **skip companion harvest/replant when already correct** | **03:24.552, −7.4%** |
| 011 | no polyculture | rejected — polyculture is worth **67x** |
| 012 | skip the walk to an unaffordable companion | **never ran — the game crashed** |

## What is actually known now

- **A successful operating function costs 200 ticks; a failed one costs 1.**
  Movement dominates everything. This is the single most useful fact for Hay.
- **Polyculture is worth ~67x** and costs ~800 ticks of walking per pass. Nothing
  that trades companion yield for ticks can win — that whole line is closed.
- **The companion preference rerolls every pass**, so the walk cannot be
  amortised and there is nothing to cache.
- **The loud warnings were never the problem.** ~1000 failed carrot plants and
  ~950 failed water calls cost 1 tick each. Chasing them was wasted effort in
  003, 006 and the original 008/009 queue items.
- **Idle waiting is 0.2% of ticks.** 007's "94% of passes start unripe" is a
  frequency, not a duration; misreading it cost the 59x regression in 008.

## Next experiment, already written and never run

`auto_experiment/hay/012` (worktree `~/dev/tfwr-worktrees/hay-012`) is complete
and committed-ready but unrun: when the companion is Carrot and unaffordable,
return before walking. It is ~800 wasted ticks on roughly a third of passes,
detectable for about a tick beforehand. Just:

```sh
tools/cycle.sh hay exp-hay-012-skipunaff --from ~/dev/tfwr-worktrees/hay-012
```

After that, the open question worth real thought: **carrot requests currently
earn no multiplier at all** (wood sits at 0, so 512 hay + 512 wood is never
affordable). That is a third of passes yielding 1x instead of 67x. Deliberately
banking wood by harvesting Bush and Tree companions could unlock it — the prize
is large and nothing has tested it.

## Harness changes tonight

All in `tools/`, all pushed:

- `tfwr.sh reload` — Escape **toggles** the pause menu, so a failed cycle that
  left it open inverted every reload after it. It now probes before acting.
- `tfwr.sh verdict` — a scored modal and a failed one are identical apart from an
  orange "Run Failed" line. `cycle.sh` was reporting `STATUS=ok` for a failed
  run, which is the single most dangerous thing an unattended loop can do,
  because the duration looks entirely plausible.
- `tfwr.sh` crash detection — a Proton crash dialog shares the game's window
  class, which used to surface as `grim: invalid geometry`.
- `key` and `stop` now focus the window first; both silently dropped their
  shortcut before.
- `cycle.sh` — one full measurement cycle, hash-verifying the deployed code
  against the category before every run.

**Do not abort a running experiment lightly.** Shift+F5 does not work, and the
red stop button in the code window's title bar is what killed the game tonight.
See `docs/LOOP.md`.

## Restarting the loop

```
/loop Run the next queued Hay experiment following docs/LOOP.md in
/home/bcrowthe/dev/The-Farmer-Was-Replaced-Code. One experiment per tick. ...
```

`docs/LOOP.md` is the tick protocol and carries the stop conditions, the
merge-and-journal policy, and the failure table.
