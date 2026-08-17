# exp-002 — resources, unlocks, cascade-yield scaling

**Hypothesis.** 001 left three open questions that determine whether
this category needs a real `swap()`-based sort or not: (a) 001 never
checked `Items.Pumpkin` (Cactus costs 64 Pumpkin to plant, per
Entity-Planting-Costs.md) despite planting succeeding twice with 0
recorded Hay/Wood/Carrot — there must be starting Pumpkin stock, or a
Cactus unlock that changes the cost. (b) 001's single-cactus harvest
yielded 32 Items.Cactus, not `1**2 = 1` as Cactus.md's literal formula
would predict for a lone (non-cascading) harvest — some multiplier
(likely `num_unlocked(Unlocks.Cactus)`, described as "increases the
yield and cost of cactus") must apply on top of the `n**2` cascade
formula. (c) 001 found size is fixed once a cactus is fully grown
(constant across 2000 and 6000 extra wait ticks) — sizes are randomly
assigned per cactus, not something that converges by waiting, so a real
neighbor-swap sort will be needed for any cascade bigger than 1.

**Variable.** None — still first-contact measurement.

**Metric.** `num_items(Items.Pumpkin)` at start, `num_unlocked(Unlocks.Cactus)`,
and the yield from harvesting a real 2-cactus cascade (plant 2 adjacent
tiles, force them into sorted order by construction or brute-force
retry, harvest one, read the actual `Items.Cactus` gained) compared to
a 1-cactus harvest, to back out the per-cascade formula.

**Baseline.** 001: single harvest yielded 32 Items.Cactus (size 2 at
harvest). `COST_CACTUS {Items.Pumpkin:64}`.

**Procedure.**
1. `num_items(Items.Pumpkin)`, `num_unlocked(Unlocks.Cactus)`, `get_cost`
   again to see if it matches 64 or was already discounted somehow.
2. Plant two adjacent tiles (East-West). Wait for both to be fully
   grown. `measure()` both. If not already sorted (a 2-tile pair is
   sorted iff the East one's size >= West one's size, matching
   Cactus.md's rule applied to a single neighbor pair), `swap()` to fix
   it — a 2-cactus case never needs more than one swap.
   Harvest the West one, read `Items.Cactus` gained.
3. Compare to 001's lone-harvest yield to isolate the cascade formula
   from any flat multiplier.

**Falsifier.** If the yield doesn't scale in an interpretable way (e.g.
neither a clean `k * n**2` nor `k * (size_sum)` pattern), report the raw
numbers and flag this as needing a longer, more controlled series
before designing anything — don't force-fit a formula to two data
points.
