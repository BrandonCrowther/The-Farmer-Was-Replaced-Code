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
#   tools/tfwr.sh select               # click the harness code window to select it
#   tools/tfwr.sh run                  # select, then F5. F5 alone does nothing.
#   tools/tfwr.sh stop                 # Shift+F5: stop execution
#   tools/tfwr.sh state                # idle | running, from the title-bar buttons
#   tools/tfwr.sh running              # is the game up? exit 0/1
set -euo pipefail

CLASS="steam_app_2060160"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHOTS="$REPO/logs/captures"

# The resource bar sits top-left in native pixels. The window is 2048x1152
# logical at 1.25 scale = 2560x1440 captured pixels; this crop is in captured px.
HUD_CROP="1120x150+0+0"

# Where to click to select the harness code window, in logical compositor coords,
# and where its title-bar run/stop buttons are, in captured px. Both depend on
# where you dragged the window inside the game, so override if you move it.
HARNESS_XY=${TFWR_HARNESS_XY:-"1178 748"}
BUTTON_CROP=${TFWR_BUTTON_CROP:-"120x50+1065+805"}

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

# The harness window's title bar shows green play arrows when idle and orange
# stop/pause buttons while executing. That colour flip is the only reliable
# "the run actually started" signal: F5 into an unselected window is a silent
# no-op, and an unstarted farm looks much like a running one.
run_state() {
  local shot rg
  shot=$(mktemp /tmp/tfwr-state-XXXX.png)
  capture_to "$shot"
  rg=$(magick "$shot" -crop "$BUTTON_CROP" +repage -resize 1x1 -format '%[fx:r] %[fx:g]' info:)
  rm -f "$shot"
  awk -v r="${rg%% *}" -v g="${rg##* }" 'BEGIN { print (r > g) ? "running" : "idle" }'
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
    need_game
    [[ $# -ge 1 ]] || die "key needs a spec, e.g. ',F5' or 'SHIFT,F5'"
    hyprctl dispatch sendshortcut "$1,class:$CLASS" >/dev/null
    ;;
  click)
    [[ $# -ge 2 ]] || die "click needs <x> <y> in logical coords"
    focus_game; click_at "$1" "$2"
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
    [[ "$st" == "running" ]] || die "F5 did not start a run (still idle)"
    ;;
  stop)  need_game; hyprctl dispatch sendshortcut "SHIFT,F5,class:$CLASS" >/dev/null ;;
  state) run_state ;;
  help|*)
    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'
    ;;
esac
