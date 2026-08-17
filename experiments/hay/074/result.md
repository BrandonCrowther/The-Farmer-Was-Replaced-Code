# exp-074 — measure the real adopted champion's actual ticks/harvest — result

**Outcome.** Confirmed and better than predicted. Real deployed code:
889.78 ticks/harvest, beating 072's instrumented 923.53 by 33.75 ticks
— close to the ~27-tick overhead 071 attributed to bookkeeping, within
normal run-to-run variance.

**Numbers.**

```
SETUP_DONE ticks 28204 memory_size 30
WINDOW_END 150   TICKS_PER_HARVEST_THIS_WINDOW 865.91
WINDOW_END 300   TICKS_PER_HARVEST_THIS_WINDOW 876.82
WINDOW_END 450   TICKS_PER_HARVEST_THIS_WINDOW 869.85
WINDOW_END 600   TICKS_PER_HARVEST_THIS_WINDOW 938.36
WINDOW_END 750   TICKS_PER_HARVEST_THIS_WINDOW 938.62
WINDOW_END 900   TICKS_PER_HARVEST_THIS_WINDOW 849.11
CYCLES 900   ELAPSED_TICKS 800803   TICKS_PER_HARVEST 889.78
```

**Baseline.** 072 (instrumented): 923.53. Cluster band: 750-856.

**Verdict.** The real, deployed, adopted champion (already scoring
02:00.734/#65 in exp-073's live run) measures 889.78 ticks/harvest in
isolation — only **33.78 ticks above the cluster's upper bound (856)**,
tighter than the 67.5-tick gap 072's instrumented measurement implied.
`reroll` remains the dominant, structurally-floored cost (per 069's
p=1/3 analysis) and there is no further concrete, well-motivated lever
identified for closing the remaining gap — REROLL_LIMIT retuning
doesn't change the average cost (only affects an already-negligible
exhaustion tail at p=1/3, `(2/3)^30 ≈ 5×10⁻⁶`), and 3+ tile round-robins
were already reasoned (070) to give no further per-harvest gain since a
single sibling's service time already exceeds the growth floor. This is
treated as the practical ceiling for the two-tile-interleaving paradigm
absent a new structural idea. No champion change from this measurement
alone — confirms, does not improve, exp-073's adopted design.
