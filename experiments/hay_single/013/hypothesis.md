# exp-013 — reroll-sequence-pattern

**Hypothesis.** The 1/3 structural hit-rate ceiling (004, confirmed by
011's exact asymptote match) assumes each replant's (type, position) draw
is IID uniform. If the draw sequence is instead predictable (e.g. avoids
immediate repeats, cycles through positions, or otherwise correlates with
recent history), the ceiling is not real and there is a genuinely large
lever left — worth checking directly before accepting ~68 hay/tick as the
limit of this whole approach.

**Variable.** None — pure observation. Plant, read `get_companion()`,
discard (harvest immediately, unripe, 0 yield), repeat, with no servicing
at all.

**Metric.** The raw sequence of 300 (type, position) draws, checked for:
repeated exact (type, position) pairs close together, type-only runs
(same type twice in a row more/less often than 1/3 chance implies),
and position reuse patterns.

**Baseline.** IID-uniform null hypothesis: `P(type)=1/3` each independent
draw, `P(same position within a short window)` matching what a uniform draw
over ~24 cells implies.

**Procedure.**
1. `saves/hay_single/main.py`: 300 cycles of plant→read→discard, printing
   every draw.
2. `tools/cycle.sh hay_single exp-hay_single-013-r1 --from <worktree>`.
3. Read `OUTPUT=`, parse the 300 `DRAW` lines, and check offline (Python)
   for autocorrelation / repeat structure against the IID-uniform null.

**Falsifier.** If the sequence looks statistically indistinguishable from
IID uniform (no detectable autocorrelation, type frequencies near 1/3,
position frequencies near uniform over the ~24-cell ball), the ceiling is
real and 013 should say the reroll/companion-service lever is exhausted,
pointing 014 at something outside this mechanism entirely (or at stopping
per the 8-attempts rule and pivoting to Hay).
