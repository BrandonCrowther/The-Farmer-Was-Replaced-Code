# exp-004 — true-companion — result

**Outcome.** adopted — new champion

**Numbers.**

| run | seed | metric | note |
| --- | --- | --- | --- |
|  1  | random | **03:40.911** | PB; global rank **#278**, up from #422 |

**Baseline.** 04:55.320 · **Variant.** 03:40.911 · **Delta.** **−74.409 s (−25.2%)**

**Noise floor.** 0.15 s. The win is ~500x the floor. No confirming run needed to
believe the direction; one is queued anyway as 004b because the champion is
worth pinning down precisely.

**Warning histogram.**

| warning | 002 | 004 |
| --- | --- | --- |
| Didn't have the required items to plant `Entities.Carrot` | 760 | 987 |
| Tried to use `Items.Water` but didn't have enough of it | 713 | 931 |
| Cannot plant `Entities.Carrot` on `Grounds.Grassland` | 6 | 10 |

Both counts went *up*, which is the expected shape of this win rather than a
contradiction of it: the farm now completes far more harvest cycles in the same
run, so every per-cycle failure mode is exercised more often. Per unit of work
they are unchanged — these are the two remaining leaks, and they are now the
biggest ones left.

**Verdict.** One line of mapping was worth 25% of the run. A third of every
drone's companion visits were satisfying a Tree request with grass: legal, silent,
and earning none of the 5x multiplier.

The general lesson is worth more than the fix: **the seeded code was written for
achievements, not leaderboards, and its failures under leaderboard start
conditions are not all loud.** `output.txt` found the two noisy ones and missed
this one entirely, because nothing here is an error — it is the wrong plant,
successfully planted. Reading the strategy against the rules beat reading the
diagnostics.

**Next.** The remaining known leaks, in expected-value order:
- **005 reroll-companion** — replanting rerolls the preference and grass is free,
  so a Carrot roll (the only costly face) can be rerolled instead of paid for or
  wasted. With Tree fixed, two of the three faces are now free, so a reroll lands
  on a free companion ~2/3 of the time.
- **007 water-when-available** — 931 failed `use_item(Items.Water)` calls.
- **006 carrot-when-rich** — carrot becomes affordable mid-run; if the multiplier
  justifies 512 hay + 512 wood, take that face late rather than rerolling it.
