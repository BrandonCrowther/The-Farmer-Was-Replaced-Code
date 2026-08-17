# exp-003 — finish-and-score (reroll-to-15, 10-tile round robin)

**Hypothesis.** 002's design (10 tiles, reroll every replant to
petals=15 before letting it grow, round-robin harvest), wired to the
real `Items.Power >= 10000` termination condition, scores near its
≈909s (≈15.2 min) projection — sunflowers_single's first-ever
leaderboard time.

**Variable.** 002's bounded 30-cycle probe → a real driver (loops on
`num_items(Items.Power) < TARGET`, terminates on hitting it).

**Metric.** The completion modal's verdict and displayed time.

**Baseline.** 002's projection: ≈909s (≈15.2 min) at ≈7.97 net
Power/harvest, 4,399.1 ticks/harvest.

**Procedure.**
1. `saves/sunflowers_single/main.py`: 10-tile round robin, reroll-to-15
   on every plant, target-gated `while` loop.
2. `tools/cycle.sh sunflowers_single exp-sunflowers_single-003-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the diagnostic line.

**Falsifier.** If the run fails to terminate or scores far from the
projection, check for a bug the bounded 30-cycle probe couldn't
surface (e.g. the background Power-for-speed consumption compounding
differently over ~1,255 harvests than it did over 30).
