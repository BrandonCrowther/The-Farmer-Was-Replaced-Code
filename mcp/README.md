# Phase 2 — automation stack: what was evaluated, what we run

**Decision: no third-party MCP server. Hyprland's own IPC plus `grim` covers
capture and keys; `ydotool` is required on top for clicks.** The driver is
`tools/tfwr.sh`, called through Claude Code's native Bash.

> **Corrected after end-to-end testing.** An earlier draft of this file claimed
> the loop needed no root at all. That was generalised from a single Escape
> keypress and is wrong: keys reach the game, but **F5 does not start execution**
> unless an in-game code window is selected, and selecting one needs a click.
> `ydotool` is a requirement, not an optional extra. See "Starting a run" below.

**The full loop has since run end to end** — click, F5, run, read the result off
the completion modal, dismiss it, main save intact. See
`experiments/000-e2e-validation/result.md`.

### ydotool coordinates are half the compositor's

Measured, not assumed: `ydotool mousemove -a -x 300 -y 200` puts the cursor at
logical `(600, 400)`, and `-x 1024 -y 576` hits the screen edge at `(2047, 1151)`.
So `ydotool_arg = logical / 2`, and since the monitor is 2560x1440 at scale 1.25,
`ydotool_arg = screenshot_px / 2.5`. `tools/tfwr.sh click` takes logical
coordinates and does the conversion, and puts the pointer back where it found it.

## What was tested on this machine (Omarchy / Hyprland, TFWR under Proton)

| Capability | Mechanism | Status |
| --- | --- | --- |
| Locate game window | `hyprctl clients -j`, class `steam_app_2060160` | works — XWayland, 2048x1152 logical |
| Screen capture | `grim -g "<geometry>"` | works — emits native 2560x1440 px (1.25 scale) |
| Key injection (global keys) | `hyprctl dispatch sendshortcut ",escape,class:steam_app_2060160"` | works — verified opening/closing the menu, and panning the camera with `W`/`S` |
| Key injection (F5 = start execution) | same, as `,F5` and as `,code:71` | **does not fire** — farm unchanged after both, while the same mechanism pans the camera |
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

### Starting a run needs the mouse

`sendshortcut` sends keys only, and `hyprctl dispatch movecursor` moves the
cursor without being able to press a button. That is a hard gap, and it lands
squarely on the critical path.

What the F5 test showed, in order:

1. F5 to the window: nothing. Farm unchanged after 20 s.
2. Compositor-focus the window first, then F5: still nothing.
3. Same mechanism, `W`/`S`: camera pans. So keys **are** being delivered.
4. F5 as raw keycode (`,code:71`): still nothing.

The remaining explanation is that the game starts execution only when one of its
own code windows is selected, and selection comes from a click. Consistent with
the evidence: the first screenshot of the session showed a text cursor in the
`Leaderboard_run` title, i.e. it was selected — and the Escape keypress used to
prove key delivery is most likely what deselected it.

So `tools/setup_input.sh` (installs `ydotool` plus a udev rule and user service)
is a **prerequisite**, not an optional extra. It needs sudo, so it must be run
interactively before any unattended session.

Even with a window selected by hand, a keyboard-only loop would be one stray
Escape away from silently pressing F5 into nothing — and, as measured, a
no-op run is not obviously distinguishable from a real one in a screenshot
without reading the farm state. The loop needs to be able to re-select the
window itself.

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
