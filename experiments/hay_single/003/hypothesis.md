# exp-003 — price-carrot-lever

**Hypothesis.** A dedicated wood income cannot make Carrot affordable often
enough to pay for itself, because Tree.md states trees yield only **5 wood
each** against Carrot's 512-wood cost — this should be decisive from the
wiki alone, with no run needed, the same way the no-diagonals question was
settled by reading the API (docs/LOOP.md, "Check the API and the wiki
first").

**Variable.** None — arithmetic only, no code changes, no cycle.

**Metric.** Ticks required to farm enough wood for one Carrot satisfaction,
compared against the ~837,600-tick whole-run budget from 001.

**Baseline.** 002's measured design: ~1,221 harvests needed, ~1/3 (≈407) are
Carrot requests, each currently scoring 512 instead of 81,920 (a foregone
81,408/occurrence).

**Procedure (arithmetic, not a game cycle):**
1. Wood needed for all Carrot occurrences: `407 * 512 = 208,384` wood.
2. Trees per that much wood: `208,384 / 5 = 41,677` tree-harvests.
3. Minimum ticks per tree-harvest (plant 200 + harvest 200, ignoring growth
   wait and any move to/from a separate wood tile — a floor, not a real
   estimate): `41,677 * 400 = 16,670,800` ticks.
4. Compare to the ~837,600-tick budget for the *entire* run.

**Falsifier.** If step 3's floor (which already ignores growth time and
movement, both certainly nonzero) is smaller than the ~837,600-tick budget,
the lever might be worth a real probe. If it's already many times larger
using the most generous possible assumptions, no probe can rescue it and none
is needed.
