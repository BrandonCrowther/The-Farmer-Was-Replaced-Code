# The Farmer Was Replaced Code

Code repository for The Farmer Was Replaced. This as it stands represents the code
used to achieve 100% completion of the game's achievements — plus the tooling for
iterating on it automatically.

## Layout

| Path | What |
| --- | --- |
| `save/Save0/` | the actual game scripts — this is the live save, see below |
| `docs/wiki/` | offline mirror of thefarmerwasreplaced.wiki.gg, 59 pages |
| `docs/api/` | snapshot of `__builtins__.py`, the authoritative API surface |
| `docs/PLAN.md` | plan of record: telemetry design, measurements, Phase 3 |
| `experiments/` | `queue.md` backlog and one directory per experiment |
| `tools/` | `tfwr.sh` game driver, `fetch_wiki.py`, `setup_input.sh` |
| `mcp/` | automation stack evaluation and the decision that came out of it |

## The save symlink

`save/Save0/` holds the **real** files. The game's save folder points at them:

```
~/.local/share/Steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/
  AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced/Saves/Save0
    -> ~/dev/The-Farmer-Was-Replaced-Code/save/Save0
```

So editing a file in this repo edits the game's code directly, and File Watcher
(enabled in the game's options) picks it up in about a second. Verified working
through the symlink.

This direction — repo owns the files, prefix links to them — is deliberate. Git
does not follow a symlinked directory, so pointing the repo at the prefix would
have tracked nothing. It also means the code survives a Proton prefix rebuild.

`~/dev/farmer` is a shortcut to this repo.

### Undoing it

```sh
GAME=~/.local/share/Steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced
rm "$GAME/Saves/Save0"                                   # removes the symlink only
cp -r ~/dev/The-Farmer-Was-Replaced-Code/save/Save0 "$GAME/Saves/Save0"
```

Close the game first. Pre-reorg snapshots are in `~/dev/tfwr-safety-backups/`, and
the game keeps its own rolling copies in `…/TheFarmerWasReplaced/Backup/`.

## `save.json` is off limits

The game owns `save/Save0/save.json` — it is live state, rewritten as you play. It
is gitignored so no checkout can ever clobber a live save, it is never a telemetry
source, and nothing here writes it. Measurement happens by running code in-game
and reading its output instead; see `docs/PLAN.md`.

`save/Save0/__builtins__.py` is gitignored for the same reason (the game
regenerates it). The reviewed copy lives in `docs/api/`.

## Tooling

```sh
tools/tfwr.sh geo              # game window geometry + workspace
tools/tfwr.sh capture [label]  # screenshot -> logs/captures/
tools/tfwr.sh hud [label]      # just the resource bar
tools/tfwr.sh run              # F5 — run the focused in-game code window
tools/tfwr.sh stop             # Shift+F5

python3 tools/fetch_wiki.py    # refresh docs/wiki (needs pandoc)
tools/setup_input.sh           # optional: ydotool, only needed for mouse clicks
```

Keys go to the game with `hyprctl dispatch sendshortcut` — no root, no daemon.
Capture requires the game's workspace to be visible, so `tfwr.sh` switches to it
and back; see `mcp/README.md` for why that matters and what else was ruled out.
