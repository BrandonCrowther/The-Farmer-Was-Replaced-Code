# exp-010 — finish-and-score-v2 — result

**Outcome.** **adopted — new champion.**

**Numbers.** Modal: **04:13.399**, `VERDICT=scored`, **global rank #182**
(up from #302), PB 04:13.399. Leader unchanged at 02:17.995 (#1).

29 internal repeats in `output.txt`: `TIME_FINAL` range 246.39s-261.45s,
mean ≈253.4s ≈ 04:13.4 — matches the displayed time. `HAY` at finish
100,051,456-100,069,888 (small overshoot, same as 008, expected). `TICK_FINAL`
range 1,496,791-1,588,289. Implied hay/tick ≈ 63.0-66.9 (e.g.
100,062,720/1,550,921 = 64.5).

**Baseline.** 008 (champion before this): 04:49.565, rank #302, ≈55.8
hay/tick. 009's probe projected ≈02:47 (≈98.75 hay/tick) from a 200-cycle
sample.

**Delta.** **−35.7s (−12.8%)** vs. 008; rank #302 → #182. Real throughput
≈64.7 hay/tick average — better than 008's 55.8, but well short of 009's
98.75 steady-state projection. Gap to the leader: `253.399 / 137.995 ≈
1.836x` (from 008's 2.10x).

**Why the real run undershot 009's projection.** 009's tail window (cycles
175-199) was fully warmed up — every companion position it needed had
already been visited. A full ~1,221-harvest run visits far more distinct
positions over its lifetime than 200 cycles can establish, and the
`REROLL_LIMIT=2` reroll-before-walk trade only pays off once a position is
*already* in memory; every first-ever visit to a new position still costs a
walk regardless of rerolling. 009's 200-cycle sample likely overstates how
much of the full run spends in a "well-covered" state. Not a bug — a real
"the probe's window was too short to be the true steady state" gap, the
kind docs/LOOP.md's own methodology section warns about.

**Noise floor.** Not established for real scored runs (each is already a
29-repeat average, so should be stable — matches 008's own note on this).

**Screenshots.** `logs/captures/20260816-220644-exp-hay_single-010-r1.png`.

**Verdict.** Real, solid improvement — adopt as champion. But the gap
between 009's probe estimate (≈98.75 hay/tick) and this real result (≈64.7)
is itself worth a note for 011: a longer probe (or reading the real run's
own tick trajectory) would likely give a tighter estimate before the next
lever gets built, rather than trusting a 200-cycle tail window as "steady
state" for a run 6x that length.
