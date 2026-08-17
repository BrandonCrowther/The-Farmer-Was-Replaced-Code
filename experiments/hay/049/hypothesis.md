# exp-049 — reroll-before-walk retest, correctly timed, REROLL_LIMIT=5

**Hypothesis.** 038's "reroll-before-walk-general" was rejected because
its OWN measurement claimed a 44-66% baseline hit rate, leaving little
slack. 046/047's fresh, corrected measurement (with the real (3,3) home
position) shows walk-rate 63% (hit-rate only ~37%) — at the *low* end
of or below that claimed range. If the real hit rate is genuinely lower
than 038 assumed, there should be real slack for reroll-before-walk to
capture. Full generalized reroll (against the memory dict, any type,
`REROLL_LIMIT=5` — hay_single's proven near-optimal cap, not 038's
untold limit or the champion's Carrot-only `REROLL_LIMIT=2`) should cut
the walk rate and average ticks/harvest.

**Variable.** Champion's real-walk-on-any-miss (Carrot-only escape
reroll) → reroll toward *any* memory-matched companion before falling
back to a real walk, `REROLL_LIMIT=5`.

**Metric.** `TICKS_PER_HARVEST` over a 150-cycle bounded probe (main
drone only, same real 32-drone contention), compared to 047's 1,390.

**Baseline.** 047 (corrected): 1,390 ticks/harvest, 63% walk-rate, 37%
skip-rate.

**Procedure.**
1. `saves/hay/main.py`: reroll-before-walk on all 32 drones (needed for
   realistic shared memory/contention conditions during the probe, not
   just the main drone).
2. `tools/cycle.sh hay exp-hay-049-r1 --from <worktree>`, bounded to
   150 cycles on the main drone.
3. Compare `TICKS_PER_HARVEST` to 1,390.

**Falsifier.** If ticks/harvest doesn't clearly improve, 038's
rejection stands (correctly) and the remaining gap is not explained by
anything mechanism-level — say so plainly rather than re-testing a
third variant of the same idea.
