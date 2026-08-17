# exp-015 — bush-blanket-quad — result

**Outcome.** rejected as a route to more throughput — but a genuinely
useful, decisive test of a real alternative shape, not a restatement of
the existing design.

**Numbers.** `SETUP_TICKS` 27,675 (close to the ~30,000 estimate). Tail
ticks/harvest (50-harvest windows, post-setup): 1,206.7 / 1,109.5 / 1,422.9
/ 1,165.7 / 1,324.4 — noisy but centred almost exactly on the predicted
~1,200 asymptote, same as the existing design's proven ceiling (011).
Post-setup average: **1,237.6 ticks/harvest ≈ 66.19 hay/tick** — slightly
*below* 012's real 68.7 hay/tick, not above it.

**Full-run projection, setup amortized over the real ~1,221 harvests
needed:** `27,675 + 1,221 × 1,237.6 ≈ 1,538,793` ticks → **≈64.99 hay/tick**
— worse than the champion once the one-time setup cost is properly
included, not just matching it.

**Baseline.** 012 (champion): 68.7 hay/tick real, no setup cost (memory
builds during the run itself, "for free" alongside real harvests, rather
than as an unproductive up-front phase).

**Noise floor.** Not established (single probe). The 5 tail windows swing
1,109-1,423 (noisy, as expected for a reroll process), but the mean across
all of them is close enough to the model's prediction that this isn't a
sampling artifact — it's the same ceiling from a different angle.

**Screenshots.** None — probe.

**Verdict — this settles the question the user raised, empirically, not
just on paper.** The literal "4 tiles + total-board Bush blanket, reroll
until Bush" design was implemented and run for real. It does **not** beat
the existing single-tile champion — it lands at the same ~1,200-tick
asymptote the reactive design already reaches, and comes out slightly
*behind* once the one-time blanket-setup cost is counted, because that
setup buys nothing the reactive design's own gradual, harvest-by-harvest
coverage-building doesn't already get for free. The reframing (pre-commit
to one type everywhere vs. learn a mix reactively) changes *how* the ~1/3
ceiling is reached, not *what* it is — confirming 011's proof from a
genuinely different angle rather than just re-deriving it.

This closes the multi-tile question a fourth way (schedulability 001,
self-collision 005, commute-tax 006, and now a from-scratch alternative
shape combined with the reroll trick that didn't exist when 005/006 ran).
`hay_single` stands at **03:57.198, rank #169**, and the pivot to `Hay`
stands.
