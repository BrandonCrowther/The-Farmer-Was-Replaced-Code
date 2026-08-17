# exp-001 — mechanics-probe

**Hypothesis.** Sunflowers are not a polyculture crop and not a
cascade/merge crop like Cactus/Pumpkin — Sunflowers.md describes a
max-petal-tracking mechanic: harvesting the sunflower with the most
petals (7-15, fixed at plant time, measurable before fully grown) while
≥10 sunflowers stand on the farm gives 8x power; harvesting any other
one first "wastes" the bonus for the next harvest too. Unknown and
must be measured directly: base (non-bonus) power yield per harvest,
growth time, planting cost, and whether the "Power speeds up the drone
2x, consuming 1 per 30 actions" side effect meaningfully drains the
10,000 target as we accumulate it.

**Variable.** None — first probe for this category.

**Metric.** Starting stockpile, `get_cost(Entities.Sunflower)`, growth
ticks, base harvest yield (`Items.Power` gained from harvesting a
lone/non-max-petal sunflower with fewer than 10 on the farm), and the
8x-bonus yield (harvest the genuine max-petal one with ≥10 standing).

**Baseline.** None — first probe.

**Procedure.**
1. Record starting stockpile and `get_cost(Entities.Sunflower)`.
2. Plant one, measure growth ticks to `can_harvest()==True`, `measure()`
   its petal count (check it's readable pre-maturity too, per
   Sunflowers.md).
3. Harvest it alone (< 10 on farm) — read the base yield.
4. Plant 10, `measure()` all, harvest the true max-petal one, read the
   bonus yield and compare to `8 * base`.

**Falsifier.** If the numbers don't make a repeated-harvest design
obviously tractable inside a reasonable tick budget for 10,000 total
Power, say so plainly and compute the real projected cost before
committing to a design, the way carrots_single's 001 did.
