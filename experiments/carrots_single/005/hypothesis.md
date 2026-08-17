# exp-005 — finish-and-score

**Hypothesis.** 004's 3-tile design, given the real `Items.Carrot >=
100,000,000` termination condition instead of a fixed cycle count, scores
near its ≈690s (≈11.5 minute) projection — carrots_single's first-ever
leaderboard time.

**Variable.** 004's probe (fixed 60 cycles, never reaches target) → a real
driver (loops on `num_items(Items.Carrot) < TARGET`, terminates on hitting
it).

**Metric.** The completion modal's verdict (`scored`) and displayed time.

**Baseline.** 004's projection: ≈690s (≈11:30) at ≈23.88 carrots/tick. No
prior score exists for this category — this *is* the baseline, once it
exists.

**Procedure.**
1. `saves/carrots_single/main.py`: 3-tile design, target-gated `while`
   loop.
2. `tools/cycle.sh carrots_single exp-carrots_single-005-r1 --from <worktree>`
   — background; per Leaderboard.md a scored run repeats internally until
   2 real hours of simulated time accumulate.
3. Read `SHOT=` with vision for the time and rank.

**Falsifier.** If the run fails to terminate or scores far from the
projection, check for a bug the bounded probes couldn't surface (neither
003 nor 004 ever exercised the real target-gated exit path).
