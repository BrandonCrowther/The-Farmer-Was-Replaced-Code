# exp-054 — reroll on distance>=2 (not just ==3), REROLL_LIMIT=5 — result

**Outcome.** rejected — worse than 053's narrower trigger.

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `TICKS_PER_HARVEST` 2,087.08 | vs 047's 1,390 baseline and 053's 1,482.65 |

**Baseline.** 047: 1,390. 053: distance==3-only, REROLL_LIMIT=2, 1,482.65.

**Variant.** (Carrot OR distance>=2), `REROLL_LIMIT=5`. **Delta.**
+50.1% vs 047, +40.8% vs 053 — worse in both directions at once.

**Noise floor.** Not established — single 150-cycle sample.

**Screenshots.** None — probe.

**Verdict.** By cell count, `distance>=2` covers 20/24 cells, so
combined with Carrot the trigger rate is ≈8/9 — even `REROLL_LIMIT=5`
(6 total draws) only gives ≈51% odds of ever landing the rare
distance-1 draw (4/24 cells). Raising both the trigger aggressiveness
and the attempt budget simultaneously made things worse, not better —
the reroll-cost side of the tradeoff scales faster than the commute
savings. Closes the "tune the distance threshold higher" direction.
