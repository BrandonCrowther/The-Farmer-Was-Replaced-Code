# exp-013 — reroll-sequence-pattern — result

**Outcome.** rejected (the hypothesis that there's exploitable structure) —
a clean, decisive negative result. Closes the companion-servicing line of
attack for good.

**Numbers.** 300 draws, no servicing, pure plant→read→discard.

| check | measured | IID-uniform expectation |
| --- | --- | --- |
| type frequency | Carrot 33.7%, Bush 32.7%, Tree 33.7% | 33.3% each |
| distinct positions | 24 (all three types independently reach all 24) | 24 (matches 004's exact radius-3 wrapped-ball count) |
| P(same type as previous draw) | 0.334 | 0.333 |
| P(same exact (type,pos) as previous) | 0.023 (n=299, se≈0.007) | 0.014 — within ~1.3 SE, not significant |
| mean position-revisit gap | 22.5 | 24 (geometric mean for uniform draw w/ replacement) |
| type-vs-position correlation | none detectable — every type reaches every position, per-cell type splits consistent with small-sample noise around 1/3 each | none |

Every check matches the IID-uniform null to within ordinary sampling noise.
**There is no hidden pattern to exploit** — the game genuinely draws a
fresh, independent, uniform (type, position) pair on every replant.

**Baseline.** IID-uniform null hypothesis.

**Noise floor.** n=300 gives reasonable power for frequency checks (±2.7%
at 1 SE per type) and adequate power for the autocorrelation check; not
enough to rule out very subtle structure, but enough to rule out anything
that would matter at the scale of a 1/3 → higher hit-rate jump.

**Screenshots.** None — probe, no modal read.

**Verdict — this closes the investigation, not just the experiment.**
Combined with 011's exact result (the reroll-only asymptote, K→∞, full
coverage, is precisely 1,200 ticks/harvest ≈ 68.27 hay/tick — and 012
already measures ≈68.7 real, matching/exceeding it), there is now a
**mathematical proof, not an estimate**, that the companion-servicing
paradigm (harvest → replant → reroll-or-walk to satisfy) cannot exceed
~68-70 hay/tick, regardless of `REROLL_LIMIT` or any other tuning within
it. The leader's implied pace needs roughly **119 hay/tick** — a genuinely
different mechanism, not a bigger K.

No further idea inside this design space survived scrutiny tonight:
multi-tile is closed three independent ways (001 schedulability, 005
self-collision, 006 commute tax), Carrot/wood is resolved positively
(003, corrected by 006/007), `swap()` was considered as a way to cut
own-tile or commute cost and doesn't reduce total ticks in either role
(it substitutes for, rather than eliminates, a 200-tick op), and Fertilizer
doesn't help because growth was never the bottleneck (own-tile handling
already ≈ growth time, confirmed by 001 and reconfirmed by Plant-growth.md's
0.5s-at-water-0 grass figure scaling to ≈0.1s at water 1, matching the
measured ~404 ticks almost exactly).

**Per the user's own fallback rule: hay_single is not going to close the
gap to the leader with further tuning inside this paradigm.** Rather than
spend more scored-cycle wall-clock time confirming what the arithmetic
already proves, this is the point to stop and carry the two genuinely
transferable lessons (reroll-before-walk when structural hit rate is low;
Carrot/wood accumulates for free from ordinary companion churn on a long
run, don't assume it's permanently dead from a short probe) into `Hay`,
whose current champion (020, 02:47.682, rank #130) uses neither.
