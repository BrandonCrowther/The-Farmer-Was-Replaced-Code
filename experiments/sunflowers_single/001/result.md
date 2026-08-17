# exp-001 — mechanics-probe — result

**Outcome.** probe — key finding opens a strong design direction
(reroll-to-max, tested next).

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `START` Carrot 1,000,000,000, `COST_SUNFLOWER {Items.Carrot:1}` | huge stockpile, cost a non-issue |
| r1 | `TILE0 GROWTH_TICKS 17643 PETALS_PRE 12 PETALS_RIPE 12 BASE_GAIN 1` | petals fixed at plant time, unwatered growth |
| r1 | `BONUS BEST_PETALS 15 GAIN 8 RATIO 8` | genuine max-petal harvest with 10 standing gives exactly 8x |

**Baseline.** None — first probe.

**Noise floor.** Not established.

**Screenshots.** None — probe.

**Verdict.** `harvest()` on an unripe entity destroys it for 200 ticks
(Available-Functions.md) rather than requiring `can_harvest()==True` —
combined with petals being fixed and readable *immediately* at plant
time (matches `PETALS_PRE == PETALS_RIPE` here), this means a cheap
reroll (harvest the just-planted unripe sunflower + replant, ~400
ticks) can redraw the petal count *before* paying the ~17,643-tick
growth cost — exactly hay_single/carrots_single's reroll paradigm,
applied to petals instead of companions. The strongest version: reroll
every tile until it hits petals=15 (the maximum possible) before
letting it grow. Since nothing can ever exceed 15, once every standing
sunflower is rerolled to 15, **every subsequent harvest is guaranteed
the 8x bonus forever** — no tracking, no ordering, no risk of poisoning
the next harvest. The 8x-bonus rule also requires ≥10 sunflowers
standing at all times, which happens to already exceed the
growth/handling-ratio tile count a carrots_single-style pipeline would
want anyway. 002 validates the reroll-to-15 loop and a small
multi-tile round-robin before committing to the real 10-tile driver.
