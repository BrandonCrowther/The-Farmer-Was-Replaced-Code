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
#   tools/tfwr.sh run                  # F5: run the focused in-game code window
#   tools/tfwr.sh stop                 # Shift+F5: stop execution
#   tools/tfwr.sh running              # is the game up? exit 0/1
set -euo pipefail

CLASS="steam_app_2060160"
REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
SHOTS="$REPO/logs/captures"

# The resource bar sits top-left in native pixels. The window is 2048x1152
# logical at 1.25 scale = 2560x1440 captured pixels; this crop is in captured px.
HUD_CROP="1120x150+0+0"

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
  run)   need_game; hyprctl dispatch sendshortcut ",F5,class:$CLASS" >/dev/null ;;
  stop)  need_game; hyprctl dispatch sendshortcut "SHIFT,F5,class:$CLASS" >/dev/null ;;
  help|*)
    sed -n '2,20p' "${BASH_SOURCE[0]}" | sed 's/^# \?//'
    ;;
esac
