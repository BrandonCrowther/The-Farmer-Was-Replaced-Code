#!/usr/bin/env bash
# deploy.sh — sync one category's code into the live save directory.
#
#   tools/deploy.sh <category> [--from <checkout>]
#
# The game reads exactly one directory (Saves/Save0 -> $TFWR_LIVE). This copies
# the category's .py files in and removes .py files the category does not own, so
# what the game sees is precisely that category and nothing else.
#
# save.json and __builtins__.py are game-owned. They live in the live directory
# permanently and are never read, written, moved, or deleted here — that is the
# whole reason the live directory is a fixed real directory rather than a symlink
# that swings between category folders.
#
# Prints RELOAD_REQUIRED (exit 10) when the *set* of files changed, because the
# game only notices new or deleted files on a save reload. Contents-only changes
# are picked up by File Watcher in about a second, needing no reload.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
# Absolute on purpose: when running from a worktree, the live directory is still
# the one the game's symlink points at, not the worktree's own.
LIVE="${TFWR_LIVE:-$HOME/dev/The-Farmer-Was-Replaced-Code/live}"
GAME_OWNED=("save.json" "__builtins__.py")

die() { echo "deploy: $*" >&2; exit 1; }

cat_name=${1:-}; shift || true
[[ -n "$cat_name" ]] || die "usage: deploy.sh <category> [--from <checkout>]"

from="$REPO"
while [[ $# -gt 0 ]]; do
  case "$1" in
    --from) from="${2:?--from needs a path}"; shift 2 ;;
    *) die "unknown argument: $1" ;;
  esac
done

src="$from/saves/$cat_name"
[[ -d "$src" ]] || die "no such category: $src"
mkdir -p "$LIVE"

# Every `import X` must resolve to a file in the same category, because the game
# resolves module names against the files in the one save folder it can see.
# A missing one is not a startup error: the run begins, burns wall-clock, and only
# then shows an ERROR tooltip on the offending line. Catch it here instead.
missing=""
for path in "$src"/*.py; do
  while read -r mod; do
    [[ -f "$src/$mod.py" ]] || missing+=" $mod"
  done < <(grep -ho '^import [A-Za-z_][A-Za-z0-9_]*' "$path" 2>/dev/null | awk '{print $2}' | sort -u)
done
[[ -z "$missing" ]] || die "category $cat_name imports modules it does not contain:$missing"

is_game_owned() {
  local f
  for f in "${GAME_OWNED[@]}"; do [[ "$1" == "$f" ]] && return 0; done
  return 1
}

changed_set=0

# Remove .py files this category does not own.
shopt -s nullglob
for path in "$LIVE"/*.py; do
  f=$(basename "$path")
  is_game_owned "$f" && continue
  if [[ ! -f "$src/$f" ]]; then rm -f "$path"; changed_set=1; fi
done

# Copy the category in, only touching files whose contents actually differ so
# File Watcher is not woken for no reason.
for path in "$src"/*.py; do
  f=$(basename "$path")
  is_game_owned "$f" && die "category $cat_name contains game-owned file $f"
  [[ -f "$LIVE/$f" ]] || changed_set=1
  cmp -s "$path" "$LIVE/$f" 2>/dev/null || cp "$path" "$LIVE/$f"
done
shopt -u nullglob

echo "deployed $cat_name -> $LIVE ($(ls "$LIVE"/*.py 2>/dev/null | wc -l) files)"
if (( changed_set )); then
  echo "RELOAD_REQUIRED"
  exit 10
fi
