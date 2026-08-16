#!/usr/bin/env bash
# tfwr.sh — drive The Farmer Was Replaced under Hyprland/XWayland.
#
# Everything here is keyboard + screen capture only: no root, no /dev/uinput, no
# ydotool. Hyprland's own `sendshortcut` dispatcher delivers keys straight to the
# game window, and `grim` captures it. See mcp/README.md for why this beat the
# off-the-shelf MCP servers.
#
# Usage:
#   tools/tfwr.sh geo                  # window geometry + workspace (JSON)
#   tools/tfwr.sh capture [label]      # screenshot -> logs/captures/<ts>-<label>.png
#   tools/tfwr.sh hud [label]          # just the resource bar, for reading counts
#   tools/tfwr.sh key <keyspec>        # e.g. ",F5"  or  "SHIFT,F5"
#   tools/tfwr.sh click <x> <y>        # click at logical compositor coords
#   tools/tfwr.sh drag <x1> <y1> <x2> <y2>   # drag a code window by its title bar
#   tools/tfwr.sh select               # click the harness code window to select it
#   tools/tfwr.sh run                  # select, then F5. F5 alone does nothing.
#   tools/tfwr.sh stop                 # Shift+F5: stop execution
#   tools/tfwr.sh state                # idle | running | result
#   tools/tfwr.sh verdict              # scored | failed (exit 1) — read the modal
#   tools/tfwr.sh wait-result [secs]   # block until the completion modal appears
#   tools/tfwr.sh dismiss              # clear the completion modal (click OK)
#   tools/tfwr.sh reload               # Escape -> Load -> Save0 -> Escape
#   tools/tfwr.sh running              # is the game up? exit 0/1
set -euo pipefail

CLASS="steam_app_2060160"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHOTS="$REPO/logs/captures"

# The resource bar sits top-left in native pixels. The window is 2048x1152
# logical at 1.25 scale = 2560x1440 captured pixels; this crop is in captured px.
HUD_CROP="1120x150+0+0"

# Where to click to select the harness code window, in logical compositor coords.
#
# This is a fixed point and stays correct because of two measured facts: every
# code window without a saved position opens at the same default spot, and the
# one on top is the file whose name sorts last, case-insensitively. The harness
# is therefore called zzRunner.py in every category — it wins that ordering, so
# it is always the window sitting at this coordinate, whatever else is deployed.
#
# Dragging a window somewhere nicer does NOT survive a reload: positions live in
# save.json, and with autosave off the game only writes them on an explicit save.
HARNESS_XY=${TFWR_HARNESS_XY:-"1520 624"}
# OK button on the run-completion modal.
OK_XY=${TFWR_OK_XY:-"461 938"}
# Pause-menu "Load", then "Save0" in the save list. Both in logical coords, and
# both well clear of the rename and delete icons that sit to the right of each
# save row.
LOAD_XY=${TFWR_LOAD_XY:-"444 390"}
SAVE0_XY=${TFWR_SAVE0_XY:-"506 479"}
# "Don't Save" on the "Do you wish to save before loading?" confirmation. That
# dialog only appears when the session is dirty, which a finished run makes it,
# so a reload has to cope with it being there and with it not being there.
# Don't Save is the right answer twice over: the canonical window layout is the
# one on disk, and writing save.json is the game's business, not ours.
DONT_SAVE_XY=${TFWR_DONT_SAVE_XY:-"1141 601"}
# Where to sample to see if that dialog is up: the centre of the Don't Save
# button, in captured pixels. The button is the only strongly green-dominant
# thing at this spot — behind it is either grey UI or blue-grey sky, both of
# which have far more blue.
DIALOG_PROBE=${TFWR_DIALOG_PROBE:-"1426 751"}
# Centre of the pause menu's "Start" button, in captured pixels — the probe for
# whether the pause menu is open.
MENU_PROBE=${TFWR_MENU_PROBE:-"555 333"}
# The band of the completion modal holding the orange "Run Failed" line, as an
# ImageMagick crop geometry in captured pixels.
FAIL_PROBE=${TFWR_FAIL_PROBE:-"200x1+480+470"}

# ydotool's absolute coordinates are exactly half the compositor's logical
# coordinates on this setup — measured, not guessed: sending (300,200) landed the
# cursor at (600,400), and (1024,576) landed at the screen edge (2047,1151).
YDO_DIV=2

die() { echo "tfwr: $*" >&2; exit 1; }

client() { hyprctl clients -j | jq -e --arg c "$CLASS" '.[] | select(.class==$c)'; }

need_game() {
  client >/dev/null 2>&1 || die "game window ($CLASS) not found — is TFWR running?"
}

geometry() { client | jq -r '"\(.at[0]),\(.at[1]) \(.size[0])x\(.size[1])"'; }
game_ws()  { client | jq -r '.workspace.id'; }

# grim reads the compositor's *output*, not a window buffer, so a game sitting on
# an inactive workspace captures whatever is visible there instead. Switch to it,
# capture, switch back. This is also what a run needs anyway — keys go to the
# window regardless, but the render must be on screen to be photographed.
capture_to() {
  local out="$1" geo cur ws
  need_game
  geo=$(geometry); ws=$(game_ws); cur=$(hyprctl activeworkspace -j | jq -r .id)
  if [[ "$ws" != "$cur" ]]; then
    hyprctl dispatch workspace "$ws" >/dev/null
    sleep "${TFWR_WS_SETTLE:-0.6}"
  fi
  grim -g "$geo" "$out"
  if [[ "$ws" != "$cur" ]]; then hyprctl dispatch workspace "$cur" >/dev/null; fi
}

stamp() { date +%Y%m%d-%H%M%S; }

focus_game() {
  need_game
  local ws cur
  ws=$(game_ws); cur=$(hyprctl activeworkspace -j | jq -r .id)
  [[ "$ws" == "$cur" ]] || { hyprctl dispatch workspace "$ws" >/dev/null; sleep 0.4; }
  hyprctl dispatch focuswindow "class:$CLASS" >/dev/null; sleep 0.3
}

# Click at logical compositor coordinates, then put the pointer back where the
# user left it — this runs on a live desktop, so stealing the cursor is rude.
click_at() {
  command -v ydotool >/dev/null || die "ydotool not installed — run tools/setup_input.sh"
  local x=$1 y=$2 before
  before=$(hyprctl cursorpos | tr -d ' ')
  ydotool mousemove -a -x $((x / YDO_DIV)) -y $((y / YDO_DIV)); sleep 0.2
  ydotool click 0xC0; sleep 0.3
  ydotool mousemove -a -x $((${before%%,*} / YDO_DIV)) -y $((${before##*,} / YDO_DIV))
}

# Three states, read from the top-centre banner rather than any code window:
#
#   running  the run timer is ticking, so the region changes between two samples
#   result   the completion modal covers it with static text
#   idle     plain sky, static and blue
#
# Two earlier versions of this got it wrong. Sampling the harness title bar went
# stale the moment the game re-laid-out its windows on a save reload. Replacing
# that with a contrast test on this banner then read the modal's own text as a
# running timer. Motion is what actually separates them.
run_state() {
  local a b crop va vb
  crop="${TFWR_BANNER_CROP:-500x120+1060+140}"
  a=$(mktemp /tmp/tfwr-a-XXXX.png); b=$(mktemp /tmp/tfwr-b-XXXX.png)
  capture_to "$a"; sleep "${TFWR_TICK_GAP:-1.5}"; capture_to "$b"

  # A run is *ticking*: the timer digits change between two samples. That is the
  # discriminator, not contrast — the completion modal also puts bright text in
  # this region, which is what fooled the previous two attempts (a title-bar crop
  # that went stale on relayout, then a contrast test that read the modal as a
  # running timer). Motion separates them cleanly.
  if ! magick compare -metric AE -fuzz 5% \
        \( "$a" -crop "$crop" +repage \) \( "$b" -crop "$crop" +repage \) \
        null: 2>&1 | awk '{ exit ($1 < 500) ? 0 : 1 }'; then
    rm -f "$a" "$b"; echo "running"; return
  fi

  # Static: plain sky means idle, anything else there means the modal is up.
  va=$(magick "$b" -crop "$crop" +repage -format '%[fx:mean.r] %[fx:mean.b]' info:)
  rm -f "$a" "$b"
  awk -v v="$va" 'BEGIN {
    split(v, c, " ")
    print (c[2] > c[1] + 0.05) ? "idle" : "result"
  }'
}

# Is there a green UI button at this captured-pixel coordinate? The game's
# buttons are the only strongly green-dominant thing on screen — behind them is
# either grey UI or blue-grey sky, both with far more blue — so one probe
# answers "is this piece of UI showing" for menus and dialogs alike.
green_at() {
  local shot v
  shot=$(mktemp /tmp/tfwr-probe-XXXX.png)
  capture_to "$shot"
  v=$(magick "$shot" -crop "1x1+$1+$2" +repage \
        -format '%[fx:mean.r] %[fx:mean.g] %[fx:mean.b]' info:)
  rm -f "$shot"
  awk -v v="$v" 'BEGIN {
    split(v, c, " ")
    exit (c[3] < 0.15 && c[2] > c[1]) ? 0 : 1
  }'
}

# Is the "Do you wish to save before loading?" confirmation showing?
save_prompt_up() { green_at $DIALOG_PROBE; }

# Is the pause menu showing? Escape *toggles* it, so anything that sends Escape
# blind will invert the state it meant to set: one failed cycle that leaves the
# menu open turns every subsequent reload into open-close-open, the Load click
# lands on empty sky, and the loop fails identically forever. Probe, don't
# assume.
menu_up() { green_at $MENU_PROBE; }

# Did the completion modal say "Run Failed"?
#
# The modal looks the same whether a run scored or failed — same layout, same
# big time, same personal best — except for an orange "Run Failed" line above the
# time. Without this check a failed run's duration reads exactly like a result,
# and the loop will happily journal it as one. A run fails if it is stopped, if
# the program never terminates, or if it ends without meeting the target.
#
# Scored: the band is flat modal grey (0.337 everywhere). Failed: orange text,
# so red saturates while blue stays low.
run_failed() {
  local shot v
  shot=$(mktemp /tmp/tfwr-fail-XXXX.png)
  capture_to "$shot"
  v=$(magick "$shot" -crop "${FAIL_PROBE}" +repage \
        -format '%[fx:maxima.r] %[fx:mean.b]' info:)
  rm -f "$shot"
  awk -v v="$v" 'BEGIN {
    split(v, c, " ")
    exit (c[1] - c[2] > 0.4) ? 0 : 1
  }'
}

# Block until the run finishes, i.e. until the completion modal appears.
wait_result() {
  local timeout=${1:-600} start now st
  start=$(date +%s)
  while :; do
    st=$(run_state)
    case "$st" in
      result) echo "result"; return 0 ;;
      idle)   echo "run ended without a result modal (state=idle)" >&2; return 2 ;;
    esac
    now=$(date +%s)
    if (( now - start > timeout )); then
      echo "timed out after ${timeout}s still running" >&2; return 3
    fi
    sleep "${TFWR_POLL_INTERVAL:-15}"
  done
}

cmd=${1:-help}; shift || true
case "$cmd" in
  geo)
    need_game; client | jq -c '{class,title,at,size,workspace:.workspace.id,xwayland}'
    ;;
  running)
    client >/dev/null 2>&1
    ;;
  capture)
    mkdir -p "$SHOTS"
    out="$SHOTS/$(stamp)${1:+-$1}.png"
    capture_to "$out"; echo "$out"
    ;;
  hud)
    mkdir -p "$SHOTS"
    full=$(mktemp /tmp/tfwr-hud-XXXX.png)
    out="$SHOTS/$(stamp)${1:+-$1}-hud.png"
    capture_to "$full"
    magick "$full" -crop "$HUD_CROP" +repage "$out" 2>/dev/null \
      || convert "$full" -crop "$HUD_CROP" +repage "$out"
    rm -f "$full"; echo "$out"
    ;;
  key)
    # focus_game, not just need_game: sendshortcut reaches an unfocused window
    # for some keys but Escape is silently dropped, which reads as "the menu
    # never opened" with no error anywhere.
    focus_game
    [[ $# -ge 1 ]] || die "key needs a spec, e.g. ',F5' or 'SHIFT,F5'"
    hyprctl dispatch sendshortcut "$1,class:$CLASS" >/dev/null
    ;;
  click)
    [[ $# -ge 2 ]] || die "click needs <x> <y> in logical coords"
    focus_game; click_at "$1" "$2"
    ;;
  drag)
    # Drag an in-game code window by its title bar, so the layout can be made
    # canonical once per category and clicked blindly thereafter.
    [[ $# -ge 4 ]] || die "drag needs <x1> <y1> <x2> <y2> in logical coords"
    command -v ydotool >/dev/null || die "ydotool not installed"
    focus_game
    before=$(hyprctl cursorpos | tr -d ' ')
    ydotool mousemove -a -x $(($1 / YDO_DIV)) -y $(($2 / YDO_DIV)); sleep 0.3
    ydotool click 0x40; sleep 0.3
    # Step the pointer there rather than teleporting: a single jump between press
    # and release is not seen as a drag, it just lands as a click on the title bar.
    steps=${TFWR_DRAG_STEPS:-12}
    for i in $(seq 1 "$steps"); do
      ydotool mousemove -a \
        -x $((($1 + ($3 - $1) * i / steps) / YDO_DIV)) \
        -y $((($2 + ($4 - $2) * i / steps) / YDO_DIV))
      sleep 0.03
    done
    sleep 0.2; ydotool click 0x80; sleep 0.2
    ydotool mousemove -a -x $((${before%%,*} / YDO_DIV)) -y $((${before##*,} / YDO_DIV))
    ;;
  select)
    focus_game; click_at $HARNESS_XY
    ;;
  run)
    # F5 only starts execution when a code window is selected, so always select
    # first. Then verify, because a missed run is silent.
    focus_game; click_at $HARNESS_XY
    hyprctl dispatch sendshortcut ",F5,class:$CLASS" >/dev/null
    sleep 2
    st=$(run_state); echo "$st"
    [[ "$st" == "running" ]] || die "F5 did not start a run (state=$st)"
    ;;
  stop)
    # focus_game, not need_game — an unfocused window drops the shortcut, and a
    # stop that silently does nothing is worse than no stop at all: the caller
    # believes the run is over and starts reading a screen that is still moving.
    # Same bug the `key` subcommand had.
    focus_game
    hyprctl dispatch sendshortcut "SHIFT,F5,class:$CLASS" >/dev/null
    sleep 1
    st=$(run_state)
    [[ "$st" != "running" ]] || die "run still going after Shift+F5 (state=$st)"
    echo "stopped ($st)"
    ;;
  state) run_state ;;
  verdict)
    # Only meaningful once the completion modal is up.
    if run_failed; then echo "failed"; exit 1; else echo "scored"; fi
    ;;
  wait-result) wait_result "${1:-600}" ;;
  dismiss)
    # The completion modal must be cleared before another run can start.
    #
    # Close the pause menu first if it is up. OK_XY sits about 20 logical pixels
    # below the menu's Quit button, and dismiss is called from recovery paths
    # precisely when the screen is in an unexpected state — which is the worst
    # possible moment to be clicking blind next to Quit.
    focus_game
    if menu_up; then
      hyprctl dispatch sendshortcut ",Escape,class:$CLASS" >/dev/null
      sleep "${TFWR_MENU_SETTLE:-1.2}"
    fi
    click_at $OK_XY
    ;;
  reload)
    # Escape -> Load -> Save0 -> Escape.
    #
    # Two jobs. It is how the game notices an added or deleted file, which is
    # what deploy.sh's exit 10 is asking for. It is also the only way to get the
    # window stacking back to its canonical state: a run leaves the file it
    # executed on top of the pile, so a second `run` would click whatever is
    # sitting at HARNESS_XY by then — `main`, not the harness — and F5 would
    # execute the wrong file. A reload puts them back in filename order with
    # zzRunner.py on top, which is the whole premise of the fixed coordinate.
    focus_game
    # Open the menu only if it is not already open — see menu_up().
    if ! menu_up; then
      hyprctl dispatch sendshortcut ",Escape,class:$CLASS" >/dev/null
      sleep "${TFWR_MENU_SETTLE:-1.2}"
    fi
    menu_up || die "pause menu did not open"

    click_at $LOAD_XY;  sleep "${TFWR_MENU_SETTLE:-1.2}"
    click_at $SAVE0_XY; sleep "${TFWR_MENU_SETTLE:-1.2}"
    if save_prompt_up; then click_at $DONT_SAVE_XY; fi
    sleep "${TFWR_RELOAD_SETTLE:-3}"

    # A load drops back to the pause menu, so it is normally open here — but
    # only close it if it actually is.
    if menu_up; then
      focus_game
      hyprctl dispatch sendshortcut ",Escape,class:$CLASS" >/dev/null
      sleep "${TFWR_MENU_SETTLE:-1.2}"
    fi
    ! menu_up || die "pause menu still open after reload"

    st=$(run_state)
    [[ "$st" == "idle" ]] || die "after reload the game is not idle (state=$st)"
    echo "reloaded"
    ;;
  help|*)
    sed -n '2,24p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'
    ;;
esac
