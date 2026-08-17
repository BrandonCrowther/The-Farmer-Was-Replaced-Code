# exp-006 — reroll-before-walk (single tile)

**Hypothesis.** hay_single's winning paradigm (008-013: reroll the
companion preference cheaply instead of walking to service it, since the
preference is fixed at plant time and a fresh reroll costs far less than
a walk-and-service round trip) transfers to carrots_single and wins by
an even larger margin, because the cost ratio here is more favorable:

- Reroll cost R ≈ 400 ticks (harvest 200 + plant 200, same as hay_single).
- Hit probability p = 1/3 (Grass is always free-standing, same structural
  fact as 002 established — no memory needed for the first hit type).
- Full walk-and-service cost, backed out from 003's real numbers:
  `TICKS_PER_HARVEST` 8,361.55 = (1/3)(own-only, ≈600: harvest+till+plant)
  + (2/3)(X) → X ≈ 3,333 ticks for a serviced cycle (walk out, till/
  harvest/plant the companion tile, walk back, and *later* a second
  round trip to revert it to Grass so the free rate doesn't erode).

Using hay_single's own asymptotic model (011: reroll-only asymptote =
`R×(1-p)/p` extra ticks over the always-paid own-tile cost), the
predicted floor here is `600 + 2×400 = 1,400` ticks/harvest — a **58%
cut** from 003's 8,362 (which was growth-bound, not handling-bound, so
this number only matters once idle time is also addressed — see
Falsifier).

**Variable.** 003's walk-and-service single-tile design → hay_single's
`Common.py` reroll-before-walk pattern (memory dict + `REROLL_LIMIT`),
transplanted directly, `Entities.Carrot` in place of `Entities.Hay`,
`REROLL_LIMIT=5` (hay_single's near-optimal cap, though the more
favorable cost ratio here — W/R ≈ 8.3 vs hay_single's ≈4 — may justify a
higher cap; start with the known-good value).

**Metric.** `TICKS_PER_HARVEST` on a single tile, 40 cycles, compared to
003's real 8,361.55.

**Baseline.** 003: 8,361.55 ticks/harvest (single tile, walk-and-service),
~71% idle (growth-bound). 004: 3,430.43 ticks/harvest (3-tile pipeline,
current champion).

**Procedure.**
1. `saves/carrots_single/main.py`: single tile, hay_single's memory +
   reroll-before-walk pattern transplanted for Carrot, 40 cycles, log
   `HITS_REROLL`/`HITS_WALK`/idle ticks per cycle same as 003.
2. `tools/cycle.sh carrots_single exp-carrots_single-006-r1 --from <worktree>`.
3. Read `OUTPUT=`; compute `TICKS_PER_HARVEST` and the handling-only
   figure (subtracting idle wait), compare to the 1,400 prediction.

**Falsifier.** Even if own-tile *handling* drops sharply, this category
is growth-bound (003: ~71% idle) — cutting handling cost alone doesn't
cut `TICKS_PER_HARVEST` below growth (~7,196) on a *single* tile; it
should still land near 003's number if idle absorbs the savings. The
real test of this hypothesis is whether *handling* time (idle
subtracted) drops as predicted — measure both, not just the headline
number. If handling drops close to ~1,400 as predicted, the next
experiment combines this with multi-tile pipelining (fewer tiles needed
now, since per-visit handling is cheaper — recompute the crossing point
before building it).
