# Wood_Single — experiment queue

Target: **500_000_000 wood** on an 8x8 farm with a single drone
Leader: **03:32.980** (shifted since 002's 03:20.446 measurement — ranks move as others submit)
Champion: **09:17.980, global rank #93** (exp-004)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Wood_Single, "main", 5000)`

Branches: `auto_experiment/wood_single/NNN` · Results: `experiments/wood_single/NNN/result.md`

## The mechanic

Tree is a polyculture crop (Polyculture.md), free to plant
(Entity-Planting-Costs.md: `Entities.Tree: {}`). Base yield 2,560; full
Polyculture multiplier (160x at this save's unlock level) gives 409,600
(001). `500,000,000 / 409,600 ≈ 1,221` harvests at full multiplier —
almost exactly carrots_single's harvest count.

**Real, measured constraint**: a Tree planted immediately adjacent to
another growing Tree takes **2.44x longer** to grow (Entities.md's
neighbor-slowdown warning, confirmed real and large — 001). A Tree's
companion is always Grass, Bush, or Carrot, never Tree itself
(Polyculture.md excludes the plant's own species), so a *single-tile*
design never triggers this penalty — it only matters if a future
multi-tile pipeline places multiple farm tiles as Trees near each other.

`own_tile_ready()` must `plant(Entities.Tree)` directly, **not** via
`Common.get_planting_instructions(Entities.Tree)` — that table entry
deliberately plants Grass instead, for a different wood-farming pattern
(see Common.py's own comment on the Tree entry).

## Queued

- [x] 003 measure-tree-harvest-and-reroll-mechanics — **probe-only,
      no champion change.** While porting Hay's tonight fixes to
      `hay_single` (a real -7.9s win), found `wood_single`'s champion
      (002) never got Hay's later 069/070 upgrade (full upfront
      position pre-seeding) — its `planted` memory only grows
      reactively, the "natural accumulation" shape 068 already proved
      worse for Hay. Measured Tree's own mechanics via `simulate()`
      (genuine sandbox, not the contaminated shared live world — see
      result.md for why the live world gave inconsistent reads):
      `harvest()` on an unripe Tree yields 0 wood and **destroys it**,
      reverting to Grassland's natural Grass (no Grass-style
      auto-regrow exception for Tree) — the current champion's reroll
      idiom still works (it recovers via `own_tile_ready()`), but pays
      the *old*, ~400-tick-per-attempt cost Hay itself moved away from
      for Grass specifically, not a mistake to fix here. A naive
      ticks/harvest model using 001's 34,718-tick isolated growth
      figure predicts ~37,000, a ~3.9x gap against the real measured
      9,551 — most likely because 001's figure is an unwatered (water
      ≈0) measurement, the same mistake Hay's own 019 made before 037
      corrected it 6.7x. `experiments/wood_single/003/result.md`
- [x] 004 measure-tree-growth-at-real-water-and-redesign — **ADOPTED,
      new champion. 09:17.980, #93 (was 31:59.849, #232) — -22:41.869
      (-70.9%), +139 ranks — the biggest win of the whole overnight
      session.** Resolved 003's open question via `simulate()` (water
      sustained 0.999): real growth is **4,412 ticks**, a 7.87x
      reduction from 001's unwatered 34,718 figure — the same
      water-measurement mistake Hay's own 019 made before 037 corrected
      it. Built a full redesign on that number: 4 tiles (not Hay's 2 —
      sized so `(N-1)×~1800`-tick servicing ≥ 4,412-tick growth),
      placed diagonally `(0,0)/(1,1)/(2,2)/(3,3)` relative to spawn
      (Tree's 2.44x cardinal-neighbor penalty is cardinal-only,
      diagonal is free — verified pairwise offline before coding), full
      upfront Bush pre-seed (42 positions) + Hay's exact reroll pattern
      otherwise. Two real parser bugs hit and fixed during validation:
      list comprehensions aren't supported by this language, and a
      tuple literal passed directly as a function argument with its own
      first element also parenthesized trips "Expected a comma or
      closing bracket" (use an intermediate variable). Smoke-tested
      (2,682.46 ticks/harvest vs the old champion's real 9,551) before
      the real run. Leader gap dropped from 9.6x to ~2.63x.
      `experiments/wood_single/004/result.md`

- [ ] 005 (open) — 004's design has two untuned knobs, mirroring the
      shape of Hay's own post-070 tuning arc (071-082): water threshold
      (kept at 0.999, matching the exact condition the growth figure
      was measured under, never re-examined for headroom the way Hay's
      072 found) and tile count (4, sized from a rough ~1800-tick
      per-visit-cost estimate, not independently verified — could be
      3 with less setup overhead, or need a 5th if the estimate was
      optimistic). Measure before retuning either, same discipline 003/
      004 already used. Also worth a stray-tick scour of the new
      `driver()`-equivalent hot loop itself (079/081/082-style) once
      the macro design is confirmed stable — it was ported from Hay's
      pattern directly but never independently re-checked line by line
      the way Hay's own code was tonight.

## Done

- [x] 001 mechanics-probe — free to plant, base yield 2,560, full
      multiplier 409,600 (160x), growth 34,718 ticks isolated, 2.44x
      neighbor-growth-penalty confirmed. `experiments/wood_single/001/result.md`
- [x] 002 finish-and-score — **adopted, first-ever score.** hay_single's
      champion paradigm transplanted directly (own_tile_ready() fix
      for the Grass-vs-Tree planting-table quirk). Real scored run:
      **31:59.849, Global Rank #232**, all 4 internal repeats crossed
      the target cleanly. `experiments/wood_single/002/result.md`
