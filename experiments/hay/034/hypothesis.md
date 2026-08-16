# exp-034 — growth-ceiling

**Not an optimisation.** Establishes the theoretical floor on ticks per harvest:
measure the water/growth relationship directly (alternating watered and unwatered
passes) and pin the tick/second rate with `get_time()` against
`get_tick_count()`, so the wiki's per-second water numbers become comparable.

Runs on the full 32-drone farm: 031 showed a single-drone probe is a different
farm.
