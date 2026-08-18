# exp-080 — precompute NEAR_OFFSETS once at module level

**Hypothesis.** The bush-wall setup loop's (dx,dy) window scan is a pure
function of the offset alone (c1 is always this drone's own base, c2 is
always base+(1,0)) — every one of the 32 drones computes the exact same
qualifying set via the exact same wdist() calls. 077's own validation
showed spawned children do NOT re-pay for `ALL_BASES`/`ALL_CROPS`'s
build cost (root's setup tick count was ~1619; children's were ≤443),
implying module-level state computed before any drone spawns is shared
(read for free), not silently recomputed per drone. If that holds,
precomputing the qualifying offset list once at module level (the same
way `ALL_BASES`/`ALL_CROPS` already are) instead of recomputing it via
wdist() inside every drone's own `driver()` call should cut real ticks;
if the hypothesis is wrong and every drone actually does redo module-
level work, the change is still tick-neutral (same total work, just
relocated) — not a regression either way.

**Variable.** Replace the per-drone nested `for dx in range(-3,5): for
dy in range(-3,4):` scan (56 cells, up to 2 `wdist()` calls each) with a
`NEAR_OFFSETS` list — computed once at module level using the same
`wdist()` logic against the fixed relative points (0,0) and (1,0) — and
iterate that list directly in `driver()` (~32 elements, no `wdist()`
calls left at all in the hot path).

**Correctness check (before any live run).** Verified offline in plain
Python that the new offset-list approach produces an *identical* set of
qualifying `(dx,dy)` pairs to the old per-drone `wdist()` scan, checked
against 6 different base positions including every seam-crossing corner
of the 32-wide world ((28,28), (31,31), (0,0), (28,3), (3,28)) — exact
match every time, 32/32 offsets. Also validated live (target=200,000):
32/32 drones each planted exactly 30 tiles (32 offsets minus each
drone's own 2 `ALL_CROPS`-excluded tiles), clean, no warnings.

**Metric.** Real leaderboard time/rank — the effect (if any) is entirely
setup-phase, invisible to the single-drone hot-loop smoke-test
methodology by construction (same blind spot 076/077/079's setup-only
components had).

**Baseline.** 079 (`auto_experiment/hay/079`): 01:56.092, #58.
