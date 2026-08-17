# exp-060 — hybrid accept policy (memory-hit OR distance-1) + wrapped setup movement — result

**Outcome.** inconclusive — essentially a dead tie with 057, not the
modeled improvement. Not adopted (057 stays champion, by 0.018s).

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | Time 02:42.439, PB stays 02:42.421 (#111, unchanged) | modal, `VERDICT=scored` |

**Baseline.** 057: memory-only accept, 02:42.421.

**Variant.** Accept on (memory-hit OR wrapped-distance==1), same
`REROLL_LIMIT=5`, plus wrapped setup movement. **Delta.** +0.018s
(162.439s vs 162.421s) — noise, not a real difference either way.

**Noise floor.** Single real run each side, but a 0.01% difference on
a ~162s run is well inside any plausible noise band.

**Screenshots.** `logs/captures/20260817-104706-exp-hay-060-r1.png`

**Verdict.** The model predicted a real improvement (S≈737 vs the
memory-only asymptote's ≈800-816) but missed a real cost: `resolve()`
checks the distance-1 condition on *every* attempt, including the
first — so it can accept a paid ~900-tick walk immediately, even in
cases where one or two more free reroll attempts (400 each) would have
found a genuine memory hit shortly after. That opportunity cost
plausibly cancels out the modeled benefit of accepting cheap walks at
all. The wrapped-setup-movement change is real but far too small a
fraction of the ~987,000-tick total run to be visible against this
run's own noise. Next: only fall back to accepting a cheap
(distance-1) walk on the *last* reroll attempt or two, not from the
first draw — preserves the free-hit chances early while still avoiding
paying for an expensive (distance-3) fallback walk when a cheap one
was available along the way.
