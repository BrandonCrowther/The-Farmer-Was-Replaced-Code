# exp-084 — reroll accept-check reorder + avoid rebuilding an existing tuple

**Hypothesis.** The reroll chase's accept check missed two more of the
same class 079 already found in the *same statement*:

1. `ctype, (cx, cy) = companion; key = (cx, cy)` unpacks the position
   out of `companion` only to immediately rebuild an identical tuple
   from the pieces — `cx`/`cy` are never used for anything else. Bind
   the position directly (`ctype, pos = companion`) instead; unpacking
   is free either way, but this skips the 1-tick tuple-literal rebuild.
2. `if key in planted and ctype == Entities.Bush:` puts the
   almost-always-True operand (`key in planted` — coverage is nearly
   total) first, so `and` almost never short-circuits — both operands
   pay on nearly every attempt. `ctype == Entities.Bush` is False 2/3
   of the time (069's uniform 1/3 draw) — checking it first lets `and`
   skip the tuple-keyed dict lookup (~2 ticks) on 2/3 of attempts, the
   same reorder-for-short-circuit trick 082 used for the water check.

**Variable.** In the reroll chase only: `ctype, pos = companion` (was
`ctype, (cx, cy) = companion` + `key = (cx, cy)`), and
`if ctype == Entities.Bush and pos in planted:` (was `if key in
planted and ctype == Entities.Bush:`). Semantically identical — `and`
is commutative and `pos` is the same tuple object/value the old `key`
was rebuilt from — only evaluation order/cost changes.

**Correctness check.** Same proof class as 079/082: no new game
mechanic assumed, both changes are pure rewrites of already-true facts
about this exact code (single write site for `planted`'s value; `and`
short-circuit is a documented, already-confirmed language rule; a
tuple bound directly from `companion[1]` is definitionally the same
value as one rebuilt from its own unpacked pieces).

**Metric.** Single-drone smoke test (900 cycles, hot loop only):
865.09 ticks/harvest (windows 819–881) vs. 082's own 873.02 baseline
— a small, directionally-correct ~8-tick difference, smaller than the
window-to-window noise (~63 ticks) so not independently conclusive
(same "small-sample undersamples a small effect" shape 079's own smoke
test had). Real run is the actual arbiter, per that precedent.

**Baseline.** 082 (`auto_experiment/hay/082`): 01:55.590, #56.
