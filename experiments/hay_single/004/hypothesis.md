# exp-004 — overlap-arithmetic

**Hypothesis.** Clustering grass tiles so their companion balls overlap can
push the solo hit rate *toward* its structural ceiling faster, but the
ceiling itself is fixed by the type-match probability (not position
coverage) and caps out well short of what's needed — a bound worth computing
before spending a run on the design.

**Variable.** None — geometry + probability arithmetic, no code, no cycle.

**Metric.** Ball-overlap fraction as a function of inter-tile distance
(computed), and the best-case (perfect position coverage) hit-rate ceiling
derived from it.

**Baseline.** 002's measured ~25-30% solo hit rate, ~1,300 ticks/harvest.

**Procedure.**
1. Compute, on the real 8x8 wrapped grid, the radius-3 companion-ball size
   and its overlap with a second ball at each possible distance (Python, not
   a game run — this is pure grid geometry, already known exactly from the
   API's move rules).
2. Derive the best-case hit rate: even with 100% of a cluster's companion
   positions covered, a fresh draw only matches if the stocked type equals
   the drawn type — bounded at 1/2 for Bush/Tree-only positions, so the
   *whole-run* average (including Carrot's dead 1/3) caps at exactly 1/3.
3. Convert that ceiling to ticks/harvest using 001/002's component costs and
   compare to the 686-tick budget.

**Falsifier.** If the best-case ceiling clears 686 ticks/harvest, clustering
is worth building for real (005). If it doesn't, clustering is a genuine
improvement over 002's measured design but not a route to beating the
leader, and 005 should say so rather than chase it further on hope.
