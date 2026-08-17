# exp-001 — mechanics-probe

**Hypothesis.** Cactus is not a polyculture crop (Polyculture.md: only
Grass/Bush/Tree/Carrot participate) — it's a size/sort cascade-harvest
mechanic instead (Cactus.md: harvesting n simultaneously-cascading
cacti yields n² Items.Cactus). Growth time is fixed at exactly 1.0s
(Plant-growth.md, zero variance, unlike every other crop measured
tonight). What's unknown and must be measured directly: does `measure()`
size (0-9) get assigned once (at plant time or at "fully grown"), or does
it keep increasing the longer a fully-grown cactus sits un-harvested? If
size only increases post-maturity, then planting many cacti at the same
moment and waiting the same extra time should make them all reach the
same size simultaneously — trivially satisfying the sorted-order
condition (equal neighbors satisfy both "≥" and "≤") without ever
needing `swap()`.

**Variable.** None yet — first measurement of this category.

**Metric.** Starting stockpile, `get_cost(Entities.Cactus)`, ticks from
plant to first `can_harvest()==True`, `measure()` immediately at that
point and again after further waiting, across several plantings.

**Baseline.** None — first probe for this category.

**Procedure.**
1. Record starting `num_items` for Hay/Wood/Carrot/Water/Cactus.
2. `get_cost(Entities.Cactus)`.
3. Plant on one tile, till first if needed. Poll `can_harvest()`,
   record tick count when it flips true, then `measure()` immediately.
4. Wait a further fixed number of ticks without harvesting, `measure()`
   again — does size change?
5. Repeat on a second tile planted at a different tick, to see if
   final size (after the same extra wait) depends on anything other
   than elapsed time since maturity.

**Falsifier.** If size is fixed at plant time (like Sunflower's
petals, "already be measured before fully grown" per Sunflowers.md) and
never changes afterward, or if it's assigned at the fully-grown moment
and is static thereafter, the "wait longer to converge sizes" idea in
the hypothesis is wrong and a real `swap()`-based sort is required
instead — say so plainly, this determines whether 002 builds a
sort-free or a sort-based design.
