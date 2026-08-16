# exp-004 — true-companion

**Hypothesis.** `Common.p_planting_table` maps `Entities.Tree` to a callback
that plants **Grass**, so a Tree companion request is satisfied with the wrong
plant — silently, with no warning — on roughly a third of every drone's
companion visits. Planting the tree it asked for should win far more than any
tick-shaving, because the polyculture multiplier is 5x before upgrades and
doubles per upgrade.

**Variable.** What gets planted when the companion request is `Entities.Tree`.
Everything else is the 002 champion, unchanged.

**Metric.** Completion modal time vs the 04:55.320 baseline. Floor is 0.15 s.

**Baseline.** `autofarmer` at 0685f3d — 04:55.320 (mean of 3).

**Why it was invisible.** Grass rolls its companion over Bush, Tree and Carrot
(never itself). `get_cost` says Bush and Tree cost nothing and only Carrot costs
(512 hay + 512 wood). The Carrot third announces itself in `output.txt`; the
Tree third fails silently, because planting grass where a tree was wanted is a
perfectly legal action that simply earns no multiplier.
