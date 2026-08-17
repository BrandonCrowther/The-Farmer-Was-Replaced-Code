# exp-009 — reroll-before-walk

**Hypothesis.** Capping 2 cheap rerolls (destroy-unripe-and-replant, ~400
ticks each, per the wiki's "harvesting an entity that can't be harvested
destroys it") before falling back to a real walk (~1,600 ticks) lowers the
average miss-handling cost, because the structural hit rate is only ~1/3
(three companion types, one stocked per position — 004): expected cost
`(1/3)(0) + (2/9)(400) + (4/27)(800) + (8/27)(2,400) ≈ 918` ticks per miss,
against the champion's flat ~1,600.

**Variable.** 008's champion (walk on every miss) → reroll up to 2 times
first, then walk if still unmatched.

**Metric.** Ticks/harvest in the tail window, same computation as
002/006/007, compared against 008's real measured ~1,468-1,600 (from
008's own `TICK_FINAL`/25 runs and the 55.8 hay/tick figure). Also: does
`WOOD`/coverage still grow at a usable rate, since rerolling doesn't
establish new stock the way a walk does.

**Baseline.** 008: champion, real scored run, ≈55.8 hay/tick average,
≈1,468 ticks/harvest implied (81,920/55.8).

**Procedure.**
1. `saves/hay_single/main.py`: reroll-then-walk hybrid, `REROLL_LIMIT=2`,
   200 cycles, single tile (same as 007/008 otherwise).
2. `tools/cycle.sh hay_single exp-hay_single-009-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute tail-window ticks/harvest and compare to 008's
   ~1,468. Check `WOOD` still climbs at a comparable rate to 007's run.

**Falsifier.** If tail ticks/harvest doesn't clearly beat ~1,468, the
arithmetic missed something (likely: rerolling delays memory coverage more
than the per-miss saving is worth) and 010 should say so rather than tune
`REROLL_LIMIT` on hope.
