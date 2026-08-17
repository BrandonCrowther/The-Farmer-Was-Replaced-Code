# exp-064 — does RNG-seed luck alone explain #1's implied budget? — result

**Outcome.** No. Across 24 explicit seeds, growth time never went below
the modal/floor value — a few seeds made it *worse*, none made it
better. RNG luck cannot explain a below-floor budget; the seed-timing
sketch in `docs/RNG-Seed-Mechanism.md` is moot even before its
practicality problems are counted.

**Numbers.** 24 seeds (0-23), `GROWTH_TICKS` per seed, sandboxed via
`simulate()`:

| GROWTH_TICKS | count | seeds |
| --- | --- | --- |
| 107 | 20 | 0,1,3,4,5,6,7,9,10,11,12,13,14,15,16,17,18,19,21,22 |
| 214 | 4 | 2,8,20,23 |

214 is exactly 2×107 — consistent with growth resolving in discrete
check-cycle quanta (a geometric-style "does this cycle complete the
stage" roll), not a continuously-random duration. No seed landed below
107; unlucky seeds only ever cost a *whole extra cycle*, never a
fraction of one, and never in the favorable direction.

**Caveat on the absolute number.** 107 ≠ 056's 415 (same measurement
design, real farm, uncontrolled seed). This run used `speedup=2000`
inside `simulate()` vs whatever the live champion runs at; if a "growth
check" is paced in real seconds internally, its tick-equivalent length
plausibly scales with speedup, which would fully explain 107 vs 415 as
a units artifact rather than a contradiction. This does not affect the
conclusion below — the *shape* of the distribution (one floor value
most of the time, occasional whole-cycle-worse, never better) is what
matters, and it held regardless of the absolute scale.

**Verdict.** Directly falsifies the "a sufficiently lucky seed could
shrink growth time toward zero" premise behind pursuing the seed-timing
exploit further. Combined with 063's practicality problems (unverified
sub-ms timing, and the 2-hour repeat-averaging rule capping any single
controlled seed's benefit to ~1% of the final score), this closes the
RNG angle for real: even a perfectly executed exploit has nothing to
exploit here. #1's implied budget is not explained by seed luck on
growth time. (Companion-draw luck on the *servicing* side was not
re-tested here — 046-061 already showed every accept-policy variant
topping out at 057's numbers, which is the more relevant bound for that
component.)
