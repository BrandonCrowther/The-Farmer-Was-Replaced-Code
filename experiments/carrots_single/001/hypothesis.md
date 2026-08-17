# exp-001 — mechanics-probe

**Hypothesis.** Carrots_Single inherits the same base mechanics as
hay_single (8x8 world, 1 drone, ~6,070 ticks/s, companion range ≤3
wrapped, 200-tick successful ops) but has a fundamentally different
economy: the crop itself (Carrot) costs 512 hay + 512 wood to plant, and
its companion preference is always Grass/Bush/Tree (free) — the reverse
of hay_single, where the crop was free and one companion option was
expensive. This changes what "reroll" costs (replanting our own crop here
costs real resources, not just ticks) and what the starting resource
stockpile needs to cover.

**Variable.** None — read-only instrumentation, mirrors hay_single's 001.

**Metric.** `get_tick_count()` deltas, `get_water()` samples, starting
Hay/Wood/Carrot inventory, and companion (type, wrapped distance)
distribution, all via `quick_print`.

**Baseline.** None — first-ever run for this category. hay_single's 001
(404-tick growth, ~6,070 ticks/s, companion ≤3 wrapped) is the point of
comparison for what transfers vs. what's category-specific.

**Procedure.**
1. Probe `main.py`: op-cost check, water equilibrium, starting inventory,
   5 plant→ripen→harvest cycles on Carrot (own crop) recording growth
   ticks, water, companion (type + wrapped distance), and bare yield.
2. `tools/cycle.sh carrots_single exp-carrots_single-001-r1 --from <worktree>`.
3. Read `OUTPUT=` directly.

**Falsifier.** If `START_HAY`/`START_WOOD` are 0 (no starting stockpile),
this category needs an income source before it can plant a single Carrot
at all — a much harder bootstrapping problem than hay_single ever had, and
the design has to solve that first, not optimize companion servicing.
