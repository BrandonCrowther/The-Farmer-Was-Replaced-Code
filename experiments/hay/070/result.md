# exp-070 — two-tile interleaving — result

**Outcome.** Real, meaningful improvement — the core mechanism works —
but short of the idealized prediction, likely because of a real cost
the simple model didn't include: less frequent visits mean more water
decay to make up per visit.

**Numbers.**

```
SETUP_DONE ticks 28550 memory_size 30
WINDOW_END 150   TICKS_PER_HARVEST_THIS_WINDOW 948.56   MEMORY_SIZE 30
WINDOW_END 300   TICKS_PER_HARVEST_THIS_WINDOW 892.13   MEMORY_SIZE 30
WINDOW_END 450   TICKS_PER_HARVEST_THIS_WINDOW 994.14   MEMORY_SIZE 30
WINDOW_END 600   TICKS_PER_HARVEST_THIS_WINDOW 922.27   MEMORY_SIZE 30
WINDOW_END 750   TICKS_PER_HARVEST_THIS_WINDOW 984.27   MEMORY_SIZE 30
WINDOW_END 900   TICKS_PER_HARVEST_THIS_WINDOW 1016.02  MEMORY_SIZE 30

TOTAL_HARVESTS 900   ELAPSED_TICKS 863614   TICKS_PER_HARVEST 959.57
REROLL_HIST [293,218,130,74,66,32,27,23,15,7,2,7,4,0,2,0,...]
```

`MEMORY_SIZE 30` matches the layout illustration exactly (union of two
overlapping radius-3 diamonds, minus the two crop tiles). Avg
rerolls/cycle = 2.003 — matches the p=1/3 prediction almost exactly,
confirming the companion-draw math is unaffected by having two tiles
(as expected — it's a per-draw property, not a spatial one).

Predicted total: harvest(200) + reroll(207×2.003≈414.6) + hop(200) =
814.69. Measured: 959.57 — a 144.88-tick gap. The most likely
explanation: the two-tile design visits each tile roughly half as
often in real terms as the single-tile design (since the drone spends
its time on the *other* tile), giving water more time to decay below
0.999 between visits, which means more `use_item(Items.Water)` calls
(200 ticks each) are needed per visit than the single-tile baseline
needed. Not directly instrumented in this run — a plausible, unverified
explanation, not a confirmed one.

**Baseline.** 069v2 (single tile, all-static bush): 1068.35
ticks/harvest.

**Verdict.** **959.57 vs 1068.35 — a real ~10% improvement**, the
first one in this whole family (051, 053-055, 058-061, 069v1, 069v2 all
either tied or lost). The growth-hiding mechanism is real and
confirmed: interleaving two tiles beats the single-tile ceiling that
nine independent designs converged on. It falls short of the ~815-828
idealized prediction and doesn't yet reach the #2-10 cluster's implied
750-856 band, most likely due to the unmodeled water-decay cost above.
Worth a follow-up that either (a) directly instruments water top-up
frequency to confirm the theory, or (b) tests whether pre-topping water
to a higher threshold before leaving a tile closes the gap. Not yet a
champion change — this was a single-drone, 900-cycle smoke test, not a
real full run, and the multi-drone macro-layout implications (fitting
paired tiles into the 32-drone grid without new inter-drone conflicts)
haven't been worked out.
