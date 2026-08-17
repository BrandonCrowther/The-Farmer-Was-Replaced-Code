# exp-008 — finish-and-score (5-tile reroll pipeline)

**Hypothesis.** 007's 5-tile reroll-pipeline design, wired to the real
`Items.Carrot >= 100,000,000` termination condition (and with the
warm-up gap fixed — the initial per-tile setup now resolves the
companion the same way every later visit does, instead of planting
unresolved), scores near its ≈477s (≈7:57) projection — beating 005's
real 11:54.303 by a wide margin.

**Variable.** 005's 3-tile walk-always driver → 007's 5-tile
reroll-before-walk driver, target-gated.

**Metric.** The completion modal's displayed time and global rank.

**Baseline.** 005: real score, 11:54.303, Global Rank #118.
007's projection: ≈477s (≈7:57) at ≈42.2 carrots/tick.

**Procedure.**
1. `saves/carrots_single/main.py`: 5-tile round-robin, reroll-before-walk
   resolved immediately at plant time (both during setup and every
   later visit — no separate unresolved warm-up plant), target-gated
   `while` loop.
2. `tools/cycle.sh carrots_single exp-carrots_single-008-r1 --from <worktree>`.
3. Read `SHOT=` with vision for the time and rank; read `OUTPUT=` for
   the `DONE` diagnostic line.

**Falsifier.** If the score lands far from ≈477s, or global rank doesn't
improve on #118, check for a bug the bounded 007 probe (75 cycles)
couldn't surface — same caveat 005's hypothesis noted for 004→005.
