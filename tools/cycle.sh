#!/usr/bin/env bash
# cycle.sh — one measurement cycle, from deployed code to a dismissed modal.
#
#   tools/cycle.sh <category> <label> [--from <checkout>] [--retries N]
#
# This is the mechanical half of the Phase 3 loop. It does everything that does
# not need judgement, and stops at the one thing that does: the run's time, PB
# and rank exist only on screen, so a human or a model still has to read
# SHOT= with vision. Everything else it prints is machine-readable.
#
# Output, one KEY=VALUE per line:
#   DEPLOYED=<category>     what is actually in the live save, verified by hash
#   SHOT=<path>             screenshot of the completion modal — read this
#   OUTPUT=<path>           archived output.txt for this run
#   WARN=<count> <text>     one line per distinct runtime warning
#   STATUS=ok|failed
#
# Exit 0 on a run that produced a modal, non-zero otherwise. A non-zero exit is
# a failed cycle for the loop's consecutive-failure count; it is never a
# silently wrong number, which is the property that matters at 3am.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
LIVE="${TFWR_LIVE:-$HOME/dev/The-Farmer-Was-Replaced-Code/live}"
GAME_ROOT="${TFWR_GAME_ROOT:-$HOME/.local/share/Steam/steamapps/compatdata/2060160/pfx/drive_c/users/steamuser/AppData/LocalLow/TheFarmerWasReplaced/TheFarmerWasReplaced}"
SHOTS="$REPO/logs/captures"

die() { echo "cycle: $*" >&2; echo "STATUS=failed"; exit 1; }

cat_name=${1:-}; label=${2:-}
[[ -n "$cat_name" && -n "$label" ]] || die "usage: cycle.sh <category> <label> [--from <checkout>] [--retries N]"
shift 2

from="$REPO"; retries=1
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from)    from="${2:?--from needs a path}"; shift 2 ;;
    --retries) retries="${2:?--retries needs a number}"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done

src="$from/saves/$cat_name"
[[ -d "$src" ]] || die "no such category: $src"
mkdir -p "$SHOTS"

# --- 0. Is there memory left to run in? ---------------------------------------
#
# The game leaks badly across leaderboard runs. On 2026-08-16 the Steam scope
# reached a 56 GB peak after ~14 hours of continuous cycling and was OOM-killed
# by systemd, taking the game with it — and the earlier "Fatal error in GC" crash
# that day was almost certainly the same pressure showing up inside Mono first.
#
# So watch it. A cycle started with little memory left will not finish, and it
# will take the game down on its way out; better to say so and let the caller
# relaunch, which is what actually reclaims the leak.
avail_mb=$(awk '/MemAvailable/ {print int($2/1024)}' /proc/meminfo)
echo "MEM_AVAIL_MB=$avail_mb"
if (( avail_mb < ${TFWR_MIN_AVAIL_MB:-4096} )); then
  die "only ${avail_mb}MB available — relaunch the game (tfwr.sh relaunch) to reclaim it before running"
fi

# --- 1. Is the game running the code we think it is? --------------------------
#
# Steam Cloud restored the original save over a deployed category once already,
# on a game restart. A loop that trusts a deploy from an hour ago can measure
# code it is not looking at and journal the result as if it meant something.
# Hashing is cheap; do it every cycle. save.json and __builtins__.py are
# game-owned and deliberately not part of the comparison.
live_hash() { (cd "$LIVE" && ls *.py 2>/dev/null | grep -v '^__builtins__\.py$' | sort | xargs -r md5sum) | md5sum | cut -d' ' -f1; }
src_hash()  { (cd "$src"  && ls *.py 2>/dev/null | sort | xargs -r md5sum) | md5sum | cut -d' ' -f1; }

if [[ "$(live_hash)" != "$(src_hash)" ]]; then
  echo "cycle: live save does not match $cat_name — redeploying" >&2
  # exit 10 is RELOAD_REQUIRED, which is expected here and handled by the reload
  # below; anything else is fatal.
  set +e; "$REPO/tools/deploy.sh" "$cat_name" --from "$from"; rc=$?; set -e
  (( rc == 0 || rc == 10 )) || die "deploy failed (exit $rc)"
  "$REPO/tools/tfwr.sh" reload >/dev/null || die "reload after redeploy failed"
  [[ "$(live_hash)" == "$(src_hash)" ]] || die "live save still does not match $cat_name after redeploy"
fi
echo "DEPLOYED=$cat_name"

# --- 2. Run it ----------------------------------------------------------------
#
# Always reload first. A finished run leaves the file it executed on top of the
# window pile, so without this the click at HARNESS_XY selects main.py and F5
# runs the wrong file — with no error, and a plausible-looking number at the end.
attempt=0
while :; do
  attempt=$((attempt + 1))
  if "$REPO/tools/tfwr.sh" reload >/dev/null && "$REPO/tools/tfwr.sh" run >/dev/null; then
    break
  fi
  if (( attempt > retries )); then die "run did not start after $attempt attempts"; fi
  echo "cycle: run did not start, recovering (attempt $attempt)" >&2
  # The two states that swallow a run: a completion modal nobody dismissed, and
  # a stray dialog. dismiss clears the first; reload's own probe clears the
  # second. Both are harmless when the thing they clear is not there.
  "$REPO/tools/tfwr.sh" dismiss >/dev/null 2>&1 || true
  sleep 2
done

"$REPO/tools/tfwr.sh" wait-result "${TFWR_RUN_TIMEOUT:-3600}" >/dev/null \
  || die "no result modal (timed out, or the run ended without one)"

# --- 3. Harvest ----------------------------------------------------------------
shot=$("$REPO/tools/tfwr.sh" capture "$label")
echo "SHOT=$shot"

# A modal is not the same thing as a score. The game shows the same panel, with
# the same big duration and the same personal best, whether the run succeeded or
# failed — the only difference is an orange "Run Failed" line. A run fails if it
# is stopped, if the program never terminates, or if it ends without meeting the
# target, and its duration reads exactly like a result. Without this check the
# loop journals that duration as a score.
verdict=$("$REPO/tools/tfwr.sh" verdict || true)
echo "VERDICT=$verdict"

out="$SHOTS/$label-output.txt"
if cp "$GAME_ROOT/output.txt" "$out" 2>/dev/null; then
  echo "OUTPUT=$out"
  # Warnings are the cheapest signal there is about *why* a variant is slow,
  # and unlike the modal they are machine-readable.
  grep -o "^Warning: .*" "$out" | sort | uniq -c | sort -rn \
    | sed 's/^ *\([0-9]*\) /WARN=\1 /' || true
fi

"$REPO/tools/tfwr.sh" dismiss >/dev/null

if [[ "$verdict" != "scored" ]]; then
  echo "cycle: the modal says the run failed — its time is not a score" >&2
  echo "STATUS=failed"
  exit 2
fi
echo "STATUS=ok"
