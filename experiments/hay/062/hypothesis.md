# exp-062 — checking two exploit-adjacent candidates before brainstorming further

**Hypothesis.** The user's counter-point (the leaderboard was reset, so #1's
post-patch time should in principle be replicable if it rests on a residual
version of one of the three exploit classes the Dec 4 2025 patch notes name)
is worth two cheap, concrete checks before further brainstorming:
(a) is `Items.Hay` — or any item — directly tradeable in a way that bypasses
growth/servicing entirely; (b) is there any tick-cost gap for calling an
imported-module (`Common.py`) function versus an inline/raw builtin call,
direct-by-name vs indirect-via-variable, that would hint at a residual
version of the patched "free function calls in dynamic modules" exploit.

**Variable.** Not a champion variant — a read-only diagnostic probe, no
`saves/hay/main.py` gameplay change.

**Metric.** (a) Whether `get_cost(Items.Hay)` (or any Item) succeeds and
what it returns. (b) `get_tick_count()` deltas around four call shapes:
local function by def-name, raw builtin, module function by def-name,
module function via variable — plus the same via-variable comparison for
a local function, to isolate "imported module" as the variable.

**Baseline.** Operation-Costs.md's documented rules: direct user-defined
call = free + body cost; indirect user-defined call = 1 + body cost;
indirect builtin call = same as direct. No documented rule for
imported-module functions specifically — that gap is what's being probed.

**Procedure.**
1. `saves/hay/main.py`: read-only probe script, `quick_print` the tick
   deltas and the `get_cost` result/error.
2. `tools/cycle.sh hay exp-hay-062-r1 --from <worktree>` — script exits
   immediately after the prints (no target-gated full run needed).
3. Read `output.txt` for the printed numbers.

**Falsifier.** If `get_cost` fails on any `Items.*` argument and the tick
deltas for module-function calls (direct and indirect) exactly match
direct-cost + real extra work and the documented +1-for-indirect rule, both
candidates are closed — no residual exploit reachable this way, look
elsewhere (RNG predictability, the concurrency race) or accept the cluster,
not #1, as the real target.
