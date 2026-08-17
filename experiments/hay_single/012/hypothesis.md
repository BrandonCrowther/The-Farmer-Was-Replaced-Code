# exp-012 — reroll-limit-5

**Hypothesis.** Raising `REROLL_LIMIT` from 2 to 5 lands near 011's modeled
≈66.33 hay/tick (vs. 010's real ≈64.7), a further ≈+2.5% — small because
010's real number already sits close to where the model puts K=2-3, not
because the model is wrong at K=5.

**Variable.** `REROLL_LIMIT`: 2 (010's champion) → 5. Nothing else changed.

**Metric.** The completion modal's time and rank, same as 008/010.

**Baseline.** 010 (champion): 04:13.399, rank #182, ≈64.7 hay/tick. 011's
model: K=5 → 66.33 hay/tick.

**Procedure.**
1. `saves/hay_single/main.py`: 010's exact logic, `REROLL_LIMIT = 5`.
2. `tools/cycle.sh hay_single exp-hay_single-012-r1 --from <worktree>` —
   background, real scored run.
3. Read `SHOT=` with vision; compare to 010's 04:13.399/#182.

**Falsifier.** If this scores *worse* than 010, the model's constant-W
assumption breaks down at higher K (plausible if repeatedly re-rolling
delays new-position discovery more than the model accounts for) and 013
should say REROLL_LIMIT tuning is done, not try a higher K on the same
logic.
