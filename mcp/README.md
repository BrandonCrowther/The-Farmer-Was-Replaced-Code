# Phase 2 — automation stack: what was evaluated, what we run

**Decision: no third-party MCP server. Hyprland's own IPC plus `grim` covers the
whole loop, with no root, no `/dev/uinput`, and no extra daemon.** The driver is
`tools/tfwr.sh`, called through Claude Code's native Bash.

## What was tested on this machine (Omarchy / Hyprland, TFWR under Proton)

| Capability | Mechanism | Status |
| --- | --- | --- |
| Locate game window | `hyprctl clients -j`, class `steam_app_2060160` | works — XWayland, 2048x1152 logical |
| Screen capture | `grim -g "<geometry>"` | works — emits native 2560x1440 px (1.25 scale) |
| Key injection | `hyprctl dispatch sendshortcut ",escape,class:steam_app_2060160"` | **works** — verified by opening and closing the in-game menu |
| Mouse click | — | **gap**, see below |
| Read numbers off screen | Claude vision on the PNG | works |
| Read numbers via `tesseract` | `tesseract hud.png -` | unreliable — read `11.1B` as `1B`, merged adjacent counters. Do not use. |

### The workspace gotcha

`grim` captures a region of an **output**, not a window buffer. The game sits on
workspace 4; capturing its geometry while another workspace is visible silently
returns a screenshot of whatever else is on that monitor — a picture of your
terminal, not the game, with no error. `tools/tfwr.sh` therefore switches to the
game's workspace, captures, and switches back. Key injection does *not* need this
(keys reach the window on an inactive workspace), but any capture does.

### The one gap: mouse clicks

`sendshortcut` sends keys only. Anything that needs a pointer — clicking a
different in-game code window to focus it, hitting the ▶ button, navigating shop
or menu buttons — has no root-free path. `hyprctl dispatch movecursor` positions
the cursor but cannot press a button.

Consequences for the overnight loop:

- Fine without clicks: edit files, F5 to run the *already focused* code window,
  Shift+F5 to stop, capture, read.
- Needs clicks: switching which code window is focused, buying upgrades by hand,
  menu navigation.

Keep the intended code window (`Leaderboard_run`) focused when you leave the
machine, and the keyboard-only path is enough. To close the gap, run
`tools/setup_input.sh` — it installs `ydotool` plus the udev rule and user
service. That is the only step here that needs sudo, and it must be done
interactively before an unattended run.

## Servers considered and rejected

**`someaka/wayland-mcp`** — the candidate from the plan. Rejected:

- Marked WIP, 17 stars, no commits since Sep 2025, and no `LICENSE` file despite
  claiming GPL-3 in the README.
- Ships a VLM integration that wants an `OPENROUTER_API_KEY` and posts your
  screenshots to a third-party model. We have native vision; sending frames off
  the machine is strictly worse on privacy, latency, and accuracy.
- Drives input via `evemu-event` and a `setup.sh` that loosens device
  permissions — a bigger blast radius than `sendshortcut`, which needs nothing.
- Requires `uvx` (not installed here).
- Whole-screen oriented, with no per-window targeting, so it would hit the
  workspace gotcha above with no way to fix it.

**PyAutoGUI-based servers** (`computer-control-mcp` and similar) — rejected up
front, as the plan anticipated: they target X11/Win32 input APIs that do not work
under Wayland's input security model.

**Filesystem / git MCP servers** — unnecessary. Claude Code already edits files
and runs git natively, and File Watcher means the edit loop is just file writes.

## If you later want a real MCP server

The useful shape is a thin stdio server wrapping `tools/tfwr.sh` (`capture`,
`key`, `run`, `stop`, `geo`) so non-Bash clients can drive the game. It is a
small amount of code and no new dependencies — but it buys nothing for a Claude
Code session, so it is deliberately not built yet.
