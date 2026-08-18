# exp-077 — spawn-tree parallelization — result

**Outcome.** **Adopted, new champion.** 01:56.890, Global Rank #59 —
down from 076's 01:57.195/#60. A real -0.305s, +1 rank — smaller than
076's -0.864s, as expected: the spawn tree only shortens the
*critical-path* latency to the single last-to-start drone (a one-time
constant, ~443 ticks max vs the old design's up to 6745), where 076's
fix shaved distance off every one of the 32 drones' own individual
walks.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| probe (isolated `spawn_drone()` call) | 200 ticks | matches Operation-Costs.md's generic "successful operating function" row |
| probe (old design's real 31-call sequential loop) | 6745 ticks total, 217.58 ticks/call avg | close to 076's ~6200 estimate |
| validation (target=200,000, `zzRunner.py` → `import main`, every drone prints its own `(bx,by)` + local `get_tick_count()`) | 32/32 `MY_POS`, 32/32 unique positions matching the expected grid exactly, `SPAWNED_ROOT_CHILDREN 2`, clean `VALIDATE_DONE`, max child tick 443 | confirms both correctness (no dupes/gaps/double-spawns) and the shortened critical path |
| real (target=2,000,000,000) | **01:56.890, #59** | `VERDICT=scored`, `WARN=1666 Water` (routine) |

**Baseline.** 076: 01:57.195, #60.

**Delta.** -0.305s (-0.26%), +1 global rank.

**Verdict.** Confirms the setup-phase-spawn theory: replacing one
drone's 31 sequential `spawn_drone()` calls with a binary spawn tree
(depth `ceil(log2(32))=5`, ≤2 sequential spawns per level) is a real,
if small, win — consistent with 043's tick-rate-independence finding
(drones genuinely execute in parallel, not time-sliced), which is the
one assumption the validation pass couldn't test directly (its
`get_tick_count()` reads are per-drone-local, confirmed by children
showing *lower* absolute ticks than the root despite being spawned
strictly later). Small relative to 076 because this only removes a
one-time critical-path constant shared by the whole run, not a
per-drone cost multiplied by 32. `saves/hay/main.py` updated and merged
to `main`. `record.json` and `queue.md` updated. Second half of 077
(shared bush-wall planting / territory partitioning) still open, plus
a general pass for remaining stray-tick overhead in the champion.
