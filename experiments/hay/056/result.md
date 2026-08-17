# exp-056 — clean, isolated growth-floor measurement — result

**Outcome.** adopted as the new ground-truth growth constant, replacing
the Plant-growth.md-derived estimate.

**Numbers.**

| trial | water at plant | growth ticks | gained |
| --- | --- | --- | --- |
| 0 | 0 (unwatered) | 952 | 512 |
| 1 | 1 | 459 | 512 |
| 2 | 1 | 415 | 512 |
| 3 | 1 | 415 | 512 |
| 4 | 1 | 415 | 512 |

**Baseline.** Plant-growth.md's stated 0.5s at water=0 (unwatered),
scaling linearly to 5x speed at water=1 — naively converts to ≈608
ticks at water=1 and ≈3,038 at water=0, using the session's established
6,074.97 ticks/s constant.

**Variant.** Real measured: 415 ticks steady-state at water=1 (952 at
water=0). **Delta.** Real watered growth is **32% faster** than the
wiki-table-derived estimate; real unwatered growth is **69% faster**
than the naive linear-scaling estimate (952 vs 3,038) — the water-to-
speed relationship isn't simply "0.5s ÷ speed-multiplier" the way the
naive read of Watering.md implied, or the two numbers aren't
calibrated to the same base unit. Not fully explained, but the direct
measurement is what matters for the floor calculation.

**Noise floor.** Trial 1 (459) vs trials 2-4 (415, 415, 415) — trial 1
likely caught water still stabilizing right after planting; trials 2-4
are the clean steady-state reading.

**Screenshots.** None — probe.

**Verdict.** Real growth floor at water≈1 is **415 ticks**, not the
~608-724 estimated from the wiki table. Combined with own handling
(400, confirmed by `PLANT_TICKS 200` here plus harvest's known 200),
the zero-servicing single-tile floor is **≈815 ticks/harvest** — inside
the leaderboard's #3-10 cluster's implied band (≈750-856), not below
it as the wiki-derived estimate suggested. This is the number the rest
of tonight's push toward the cluster is calibrated against.
