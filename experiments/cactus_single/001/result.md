# exp-001 — mechanics-probe — result

**Outcome.** probe — established the basics, raised more questions than
it answered (resolved in 002).

**Numbers.**

| run | metric | note |
| --- | --- | --- |
| r1 | `START` Hay 0, Wood 0, Carrot 0, Water 0, Cactus 0 | no bootstrap stock in the categories checked (missed Pumpkin — see 002) |
| r1 | `COST_CACTUS {Items.Pumpkin:64}` | matches Entity-Planting-Costs.md |
| r1 | `TILE0 GROWTH_TICKS 5876 SIZE_AT_RIPE 2` unchanged after +2000 and +6000 extra wait ticks | size is fixed once fully grown, does not converge by waiting |
| r1 | `AFTER_HARVEST CACTUS 32` | lone (non-cascading) harvest — not `1**2=1` as Cactus.md's literal formula alone predicts, some multiplier is in play |
| r1 | `TILE1 GROWTH_TICKS 5876 SIZE_AT_RIPE 5` unchanged after +2000 | growth time is a real fixed constant (matches Plant-growth.md's 1.0/1.0/1.0, zero variance) |

**Baseline.** None — first probe.

**Noise floor.** Not established.

**Screenshots.** None — probe.

**Verdict.** Cactus is not a polyculture crop (Polyculture.md excludes
it) — it's Cactus.md's size/sort cascade mechanic instead. Key finding:
size (0-9) is randomly fixed once a cactus is fully grown and never
changes with more waiting, so achieving a multi-cactus cascade requires
a real `swap()`-based sort, not a wait-it-out trick. The single-harvest
yield of 32 (not 1) means a flat multiplier is stacked on top of
Cactus.md's `n**2` cascade formula — likely `num_unlocked(Unlocks.Cactus)`
related, per Unlocks.md ("increases the yield and cost of cactus").
002 measures the missing pieces directly.
