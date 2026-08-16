# exp-017 — water-threshold

**Hypothesis (inferred, not measured).** `while get_water() < 0.75` targets a
level the farm cannot supply — wiki arithmetic puts 32 tiles at 0.75 draining
~0.24 water/s against ~0.025/s of supply — so the loop spins on failed `use_item`
calls at a tick each.

**Variable.** Gate the loop on `num_items(Items.Water) > 0` as well, so the
condition can actually become false.

**Metric.** One run vs 03:05.323; floor 0.15 s.

**Caveat.** The starvation figure is arithmetic on wiki constants; no water level
or tank count has ever been sampled in-game. exp-019 measures it.
