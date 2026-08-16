# The Farmer Was Replaced Code

Code for The Farmer Was Replaced, plus the automation that iterates on it. The
`main` branch is the frozen 100%-achievements save; **`autofarmer` is the working
branch** and the champion set: the current best code for each of the 16
leaderboard categories.

## Layout

| Path | What |
| --- | --- |
| `saves/<category>/` | source of truth per leaderboard category, one folder each |
| `saves/*/zzRunner.py` | the harness — named to sort last so it is always the top window |
| `live/` | what the game actually reads; deployed copies, gitignored |
| `docs/leaderboards.md` | the 16 categories — **generated**, see below |
| `docs/wiki/` | offline mirror of thefarmerwasreplaced.wiki.gg, 59 pages |
| `docs/api/` | snapshot of `__builtins__.py`, the authoritative API surface |
| `docs/PLAN.md` | plan of record: telemetry, measurements, workflow |
| `experiments/<category>/` | `queue.md`, `record.json`, and one dir per experiment |
| `tools/` | the driver and the loop's scripts |
| `mcp/` | automation stack evaluation and the decisions behind it |

## How code reaches the game

```
Saves/Save0  ->  <repo>/live/     fixed symlink, set once, never moves
                   save.json      game-owned, gitignored, never touched by us
                   __builtins__.py game-generated, gitignored
                   *.py           deployed copies of one category
```

```sh
tools/deploy.sh fastest_reset     # sync a category into live/
```

Deploy copies the category's `.py` files in and deletes any it does not own. It
exits **10 with `RELOAD_REQUIRED`** when the *set* of files changed, because the
game only notices added or deleted files on a save reload (Escape → Load →
Save0). Content-only edits need no reload — File Watcher picks those up in ~1 s.

Deploy also refuses a category that `import`s a module it does not contain. That
failure is otherwise expensive: the run starts, freezes, and only then shows an
error tooltip.

## Branching

```
main                                  frozen, protected, never touched
└── autofarmer                        champion set: best code per category
    └── auto_experiment/<cat>/<NNN>    one experiment, in its own worktree
```

An experiment branch writes **only** `saves/<cat>/**` and `experiments/<cat>/**`.
Because categories are disjoint, winners merge into `autofarmer` without
conflicts. `docs/leaderboards.md` is generated from the per-category
`record.json` files for the same reason — no shared file to fight over.

```sh
tools/new_experiment.sh hay          # next NNN, branch + worktree + scaffold
python3 tools/render_leaderboards.py # regenerate the table (idempotent)
```

## Driving the game

```sh
tools/tfwr.sh run              # select the harness window, F5, verify it started
tools/tfwr.sh state            # idle | running | result
tools/tfwr.sh wait-result      # block until the completion modal appears
tools/tfwr.sh dismiss          # clear the modal
tools/tfwr.sh capture [label]  # screenshot -> logs/captures/
```

Keys go in via `hyprctl dispatch sendshortcut` (no root). Clicks need `ydotool` —
run `tools/setup_input.sh` once — because **F5 does nothing unless a code window
is selected**, and selecting one takes a click. Capture requires the game's
workspace to be visible, so `tfwr.sh` switches to it and back.

The harness is called `zzRunner.py` in every category for a reason: code windows
all stack at one default position, and the file whose name sorts last is the one
on top. That makes the harness clickable at a fixed coordinate no matter which
category is deployed. Dragging windows does not help — positions live in
`save.json` and only persist across a reload if you explicitly save.

`state` works by sampling the top banner twice and looking for *motion*: a run's
timer ticks, the completion modal does not. See `mcp/README.md` for the two
detectors that failed before this one.

## `save.json` is off limits

The game owns `live/save.json` — live state, rewritten as you play. It is
gitignored, never read as telemetry, and never written by us. Measurement happens
by running code in-game and reading the result off the screen; see `docs/PLAN.md`.

`live/__builtins__.py` is gitignored for the same reason. The reviewed snapshot
lives in `docs/api/`.

## Undoing the wiring

```sh
GAME=~/.local/share/Steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced
rm "$GAME/Saves/Save0"                                     # removes the symlink only
cp -r ~/dev/The-Farmer-Was-Replaced-Code/live "$GAME/Saves/Save0"
```

Close the game first. Snapshots are in `~/dev/tfwr-safety-backups/`, and the game
keeps its own rolling copies in `…/TheFarmerWasReplaced/Backup/`.
`~/dev/farmer` is a shortcut to this repo.
