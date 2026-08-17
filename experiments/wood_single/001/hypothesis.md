# exp-001 — mechanics-probe

**Hypothesis.** Tree is a polyculture crop (one of Grass/Bush/Tree/Carrot
— Polyculture.md), free to plant (Entity-Planting-Costs.md:
`Entities.Tree: {}`), so the carrots_single/hay_single playbook
(reactive single-tile companion service → reroll-before-walk →
multi-tile pipeline) should transfer directly. Unknowns: base Wood
yield per harvest and multiplied yield, growth ticks (Plant-growth.md:
7.0s mean, same as Sunflower — unwatered baseline), and Entities.md's
warning that "trees take longer to grow if other trees grow next to
them" — this could break the multi-tile pipeline's tile-spacing
assumptions if neighboring farm tiles (not just companion positions)
slow each other down.

**Variable.** None — first probe for this category.

**Metric.** Starting stockpile, growth ticks (isolated, no neighboring
trees), growth ticks with an adjacent tree planted (to quantify the
neighbor-slowdown effect), base and multiplied Wood yield.

**Baseline.** None — first probe.

**Procedure.**
1. Record starting stockpile.
2. Plant one Tree in isolation, measure growth ticks to
   `can_harvest()==True`, harvest, read base Wood yield (no companion
   satisfied).
3. Plant two adjacent Trees, measure growth ticks for one of them,
   compare to the isolated case to quantify the neighbor-slowdown.
4. Companion-satisfy a Tree (per Common.py's existing polyculture
   pattern) and harvest, read the multiplied yield.

**Falsifier.** If the neighbor-slowdown effect is large, multi-tile
designs (which necessarily place several Trees within the same 8x8
farm) may need much wider spacing than the wrapped-distance-4 safety
margin used for carrots_single — say so plainly and recompute before
assuming the existing playbook transfers unchanged.
