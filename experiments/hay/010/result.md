# exp-010 — lazy-companion — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:24.552** | PB; rank **#232**, up from #278 |

**Baseline.** 03:40.911 · **Variant.** 03:24.552 · **Delta.** **−16.359 s (−7.4%)**

**Noise floor.** 0.15 s. The win is ~109x the floor.

**Verdict.** Straight off the cost model from 009: a successful operating
function is 200 ticks, so not performing two of them when they change nothing is
worth ~400 ticks against a ~1400 tick pass. The measured 7.4% is smaller than
that arithmetic suggests, which makes sense — the tile only *sometimes* already
holds the right plant, so the saving is collected on a fraction of passes.

**An important negative result, from 007's data rather than a new run.** The
obvious follow-up was to cache the satisfied companion and skip the trip
entirely on later passes. **That will not work: the companion preference rerolls
every pass.** 007's samples for a single drone read Carrot, Carrot, Tree, Carrot,
Bush, ... — a fresh face each time. Harvesting the grass and letting it regrow
produces a new preference, so there is nothing to cache and the walk cannot be
amortised. Checking the existing data cost nothing and saved a run.

**Next, and it is the real question.** With the preference rerolling every pass,
the companion trip is ~800 ticks of movement per pass, unavoidably, in exchange
for the polyculture multiplier. Is that trade even positive? A pass without
polyculture is roughly 200 ticks — five times cheaper. If the multiplier is
about 5x, the two are a wash; below that, polyculture is a net loss.

008 appeared to test this and did not: it removed polyculture *and* added a
25-tile circuit, confounding the two. 011 removes polyculture alone, keeping the
one-tile loop, which measures the multiplier's worth directly.
