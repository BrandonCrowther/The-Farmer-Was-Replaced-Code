# Wood_Single — experiment queue

Target: **500_000_000 wood** on an 8x8 farm with a single drone
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
- [ ] 004 (open) — resolve 003's open question first: re-measure
      Tree's real growth time at real water levels via `simulate()`
      (controlled, not the live world) before designing anything. Then:
      does full upfront pre-seeding alone (single Tree tile, no second
      tile) already close most of the gap, the way it did for Hay
      before 070's two-tile layer was even needed? Only if there's
      still real idle/growth-wait *after* that does a multi-tile layout
      become worth the extra risk — and any such layout must space
      Tree tiles to avoid the 2.44x cardinal-neighbor growth penalty
      (diagonal offset or wider spacing, not Hay's exact adjacent-tile
      choice). Leader gap is 9.6x (03:20.446 vs current 31:59.849) —
      investigate before assuming any single lever closes all of it;
      Hay's own leader-gap-unexplained history (038-045) is the
      standing caution against over-attributing a large gap to one
      mechanism.

## Done

- [x] 001 mechanics-probe — free to plant, base yield 2,560, full
      multiplier 409,600 (160x), growth 34,718 ticks isolated, 2.44x
      neighbor-growth-penalty confirmed. `experiments/wood_single/001/result.md`
- [x] 002 finish-and-score — **adopted, first-ever score.** hay_single's
      champion paradigm transplanted directly (own_tile_ready() fix
      for the Grass-vs-Tree planting-table quirk). Real scored run:
      **31:59.849, Global Rank #232**, all 4 internal repeats crossed
      the target cleanly. `experiments/wood_single/002/result.md`
