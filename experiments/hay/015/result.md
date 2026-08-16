# exp-015 — self-correcting-map — result

**Outcome.** rejected

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:09.234** | +3.911 s vs champion |

**Baseline.** 03:05.323 · **Variant.** 03:09.234 · **Delta.** **+3.911 s (+2.1%)**

**Noise floor.** 0.15 s. The regression is 26x the floor.

**Verdict. Optimism pays.** Marking contested tiles permanently untrusted turns
the map into "always walk" over time — contention is common, tiles accumulate in
the untrusted set, and 013's savings drain away while the bookkeeping stays. The
trips a slightly-wrong map saves are worth more than the multipliers it
occasionally forfeits.

That is worth stating as a rule, because the instinct ran the other way: the
asymmetry argument (a wrong skip costs 67x, a wrong walk costs 800 ticks) is
about a *single* event, and it is correct about single events. What it misses is
frequency. Wrong skips are rare — a tile has to be overwritten between two visits
by the same drone — while the walks saved are constant. Reasoning from the cost
of one mistake, without its rate, picked the wrong design.

**A confound, recorded.** This run also switched initial placement to
`move_to_wrapped`. Placement is one-time and about 0.0007% of a drone's ticks, so
it cannot account for a 3.9 s swing — but two variables moved in one run and that
was a mistake regardless of how safe the arithmetic makes it look.

**Kept anyway:** `Common.move_to_wrapped` stays in the shared module. It is
correct, it is cheap, it is off the hot path, and the Maze categories will need
it. Only the self-correction is rejected.
