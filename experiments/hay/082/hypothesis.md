# exp-082 — reorder the water-check AND for short-circuit benefit

**Hypothesis.** The hot loop's water top-off guard,
`num_items(Items.Water) > 0 and get_water() < WATER_THRESHOLD`, pays
both getters (2 ticks) plus the `and` (1 tick) plus the `while`-entry
(1 tick) every single iteration in the original operand order, because
`num_items(Items.Water) > 0` is almost always True (046/047: real water
sits 0.8-1.0) and `and` only short-circuits on a False first operand.
`get_water() < WATER_THRESHOLD` is the operand that's usually False
(072 measured only 16/871 cycles actually needing a top-up) — putting
it first lets `and` short-circuit and skip `num_items()` entirely on
the common no-op path, with identical truth value and identical safety
(num_items is still checked before any `use_item()` call whenever
get_water() does say a top-up is needed).

**Variable.** Swap operand order in both occurrences of the water-check
`while` condition in `driver()` (the one that runs every iteration, and
the one nested inside the rare "not ripe yet" branch). Pure boolean
commutativity — `A and B == B and A` — no semantic change, only
evaluation-order/cost.

**Correctness check.** Provable equivalent by the same kind of reading
079's fixes used: the truth table is identical regardless of operand
order, and short-circuit `and` is a documented language rule this
project already relied on and confirmed working via 079's adopted
`or`-short-circuit fix. Validated live anyway (single-drone, target =
inventory + 3,000,000, since the real 2B target is unreachable — save
inventory is already ~53.8B): clean termination, overshoot 43,328
(consistent magnitude with prior single-drone checks, e.g. 081's
45,376), no warnings.

**Baseline.** 081 (`auto_experiment/hay/081`): 01:55.779, #57.
