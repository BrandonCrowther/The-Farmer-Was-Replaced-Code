# exp-003 — guarded-polyculture

**Hypothesis.** `Common.polyculture()` is not merely wasting a call on the Hay
leaderboard, it is destroying farmland: the companion is usually Carrot, the run
starts with no carrot seeds, and the planting callback tills the tile to Soil
*before* discovering it cannot plant. Every such visit converts productive
grassland into bare soil. Planting grass instead when the companion is
unaffordable should beat the baseline by well over the noise floor.

**Variable.** What gets planted on the companion tile when the companion cannot
be afforded — grass instead of nothing. The walk and the harvest are unchanged,
because those are real yield.

**Metric.** Completion modal time vs the 002 baseline of 04:55.320. The floor is
±0.15 s, so anything over ~0.3 s is real. Cross-check: the "Didn't have the
required items to plant Entities.Carrot" count in `output.txt` should collapse.

**Baseline.** `auto_experiment/hay/002` at 56986e7 — 04:55.320 (mean of 3).

**Procedure.** `tools/cycle.sh hay exp-hay-003-r1 --from <worktree>`, read the
modal, compare warning histograms.

**Note.** The affordability guard costs ~3 ticks per iteration (`get_companion`,
`get_cost`, one `num_items` per required item). If the result is a wash, that
overhead is the first suspect, and dropping the companion trip entirely is the
comparison to run next.
