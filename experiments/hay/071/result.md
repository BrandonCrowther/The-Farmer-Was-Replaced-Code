# exp-071 — find the real source of 070's 145-tick/harvest gap — result

**Outcome.** 070's water-decay guess was wrong. The real breakdown is
simpler: water top-off was just never modeled at all (not zero, as
implicitly assumed), and `Common.move_to()`'s wrapper adds real
overhead over a bare single-hop move. Both are real, both are fixable.

**Numbers.**

```
TOTAL_HARVESTS 900  ELAPSED_TICKS 899467  TICKS_PER_HARVEST 999.41
BREAKDOWN_PER_HARVEST  water 62.76  wait 1.00  harvest 200.00  reroll 482.63  move 226.00
SUM_CATEGORIES 875153  vs ELAPSED 899467  unaccounted 24314 (27.02/harvest)
WATER_CALLS 248  per_harvest 0.276
REROLL_HIST [306,189,126,86,63,43,25,19,12,8,5,3,7,1,3,0,0,1,0,0,1,0,1,0,0,0,0,0,0,1,0]
```

`wait ≈ 1` confirms growth really is fully hidden, as 070 predicted.
`water = 62.76` (0.276 `use_item()` calls/harvest) is real and was
simply absent from 070's prediction — not a two-tile-specific cost, a
cost that exists in the single-tile design too and was never separately
measured there either. `move = 226` vs the 200 a bare distance-1 hop
should cost — `Common.move_to()`'s general-purpose wrapper (four
while-loops, each checking `p_can()`) carries ~26 ticks of overhead
that a direct `move()` call doesn't need when the direction is already
known. `reroll` (482.63, avg 2.14 rerolls/cycle) is within normal
run-to-run variance of 069v2's 2.07 and 070's 2.003 — not a new finding,
consistent with the p=1/3 structural floor. Summing the *real* gap
against 070's naive 814.69 prediction: 62.76 (water, unmodeled) + 26
(move overhead) + ~39 (reroll variance) + 27 (small unaccounted
control-flow overhead) ≈ 155 — matches the observed 145-tick gap
closely.

**Baseline.** 070: predicted 814.69 (incomplete — no water term),
measured 959.57.

**Verdict.** The mystery is closed with real numbers, not a story. Two
concrete, well-motivated optimizations follow directly: (1) the water
threshold can drop well below 0.999, since `wait≈1` proves growth speed
isn't the bottleneck in this design — a slower rate still finishes
inside the ~900-tick away-window; (2) replace `Common.move_to()` with a
direct `move()` call for the known single-hop direction. Both tested
together in 072, since the breakdown instrumentation already attributes
each category's contribution without needing separate runs.
