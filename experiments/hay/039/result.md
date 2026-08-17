# exp-039 — drone-tick-profile — result

**Outcome.** measurement — confirms 020 unchanged (02:52.501, matching the
fresh baseline within noise) and supplies the arithmetic the leader's gap
needed.

**Numbers.** Main drone (3,3), steady-state windows (harvest 300-725):
1,292.2 / 1,337.2 / 1,283.1 ticks/harvest — mean **≈1,300.1**. This is the
*same order of magnitude* as hay_single's proven ~1,200-tick ceiling,
despite Hay's documented 44-66% skip rates (021) — see the analysis below
for why that isn't actually a contradiction.

**Leader comparison.** Real score this run: 02:52.501 (172.501s). Real
confirmed leader (`const arch *`): **00:58.549**. Ratio: `58.549/172.501 ≈
0.339`. Applying that ratio directly to our measured ticks/harvest (this
is a same-drone-count, same-target-share assumption — see caveats):
`1,300.1 × 0.339 ≈ 441` implied ticks/harvest for the leader — **only ~41
ticks above the bare own-tile floor (harvest+plant, 400)**. A single
memory-hit dictionary lookup costs single-digit ticks; a real walk costs
600-1,600. An average this close to the bare floor is only consistent with
**near-100% instant-hit servicing**, not the ~33% asymptotic hit rate 011
proved is the ceiling for a memory-based reactive design (solo or,
per the argument below, cooperative).

**Why 44-66% (021) doesn't already explain this.** `polyculture_mapped`
gates the *entire trip* on this drone's *own* `planted` dict — even when a
neighbour has already left the physically correct entity standing at a
position, this drone's own memory doesn't know that, so it **still walks
there** (600-1,600 ticks) and only saves the harvest+replant portion (400)
on arrival. Neighbour cooperation raises the *physical-match-on-arrival*
rate, not the *skip-the-trip-entirely* rate — those are different
quantities, and only the second one can produce a ~41-tick average.
Structurally, no amount of neighbour activity should raise a *single
drone's own* memory-hit probability above 1/3 in steady state either (a
fresh, independent draw still only matches whatever a shared position
*currently* holds with probability 1/3, regardless of how many independent
actors are refreshing it) — so on the numbers, the champion should be, and
is, in the same ~1,200-1,300-tick range hay_single reached, not close to
441.

**Baseline.** Fresh conditions (038's 02:52.338).

**Noise floor.** N/A — this is a measurement pass, not a comparison.

**Screenshots.** `logs/captures/20260816-231944-exp-hay-039-r1.png`.

**Caveats on the 441 figure.** It assumes the leader uses ~32 drones with a
similar per-drone harvest share and a similar tick rate — neither
independently confirmed. It is a first-order estimate from one ratio, not
a proof. But it is specific and striking enough (barely above the bare
floor) to take seriously rather than dismiss.

**Verdict.** If the 441 figure is even roughly right, the leader is not
running a variant of our reactive/memory design tuned better — they are
achieving something close to *always-satisfied* companions at near-zero
marginal cost, which the 1/3 IID-uniform draw (013, confirmed for
hay_single) should make structurally impossible under this mechanic.
**040 checks directly whether the (type, position) draw is actually
IID-uniform in Hay's multi-drone context** — 013 only verified this for
hay_single's solo case; it has never been checked here, and if Hay's
version of the mechanic behaves differently (correlated with nearby board
state, biased by drone density, or anything else), that would be the real
explanation, not a cleverer walk-avoidance trick.
