#!/usr/bin/env bash
# new_experiment.sh — start the next experiment for a category.
#
#   tools/new_experiment.sh <category> [slug-words]
#
# Creates auto_experiment/<category>/<NNN> off autofarmer in its own worktree and
# scaffolds experiments/<category>/<NNN>/ from the template. NNN is per-category
# and is derived from both existing branches and existing result directories, so
# it stays correct even if a branch was deleted after merging.
set -euo pipefail

REPO="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
BASE="${TFWR_BASE_BRANCH:-autofarmer}"
TREES="${TFWR_WORKTREES:-$HOME/dev/tfwr-worktrees}"

die() { echo "new_experiment: $*" >&2; exit 1; }

cat_name=${1:-}; shift || true
[[ -n "$cat_name" ]] || die "usage: new_experiment.sh <category> [slug-words]"
[[ -d "$REPO/saves/$cat_name" ]] || die "no such category: $cat_name"

git -C "$REPO" show-ref --verify --quiet "refs/heads/$BASE" || die "no $BASE branch"

# Highest NNN seen in either branches or recorded results, +1.
highest=0
while read -r n; do
  [[ -n "$n" ]] && (( 10#$n > highest )) && highest=$((10#$n))
done < <(
  { git -C "$REPO" for-each-ref --format='%(refname:short)' "refs/heads/auto_experiment/$cat_name/*" \
      | sed 's|.*/||'
    git -C "$REPO" ls-tree -d --name-only "$BASE" "experiments/$cat_name/" 2>/dev/null \
      | sed 's|.*/||'
  } | grep -E '^[0-9]+$' || true
)
next=$(printf '%03d' $((highest + 1)))

branch="auto_experiment/$cat_name/$next"
tree="$TREES/$cat_name-$next"
[[ -e "$tree" ]] && die "worktree already exists: $tree"

git -C "$REPO" worktree add -q -b "$branch" "$tree" "$BASE"

dir="$tree/experiments/$cat_name/$next"
mkdir -p "$dir"
for f in hypothesis.md result.md; do
  sed -e "s|exp-NNN|exp-$next|g" -e "s|<slug>|${*:-unnamed}|g" \
      "$REPO/experiments/TEMPLATE/$f" > "$dir/$f"
done

cat <<EOF
branch:   $branch
worktree: $tree
scaffold: experiments/$cat_name/$next/

next:
  tools/deploy.sh $cat_name --from $tree
  tools/tfwr.sh run
EOF
