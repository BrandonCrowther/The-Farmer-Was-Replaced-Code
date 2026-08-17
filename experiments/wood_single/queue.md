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

- [ ] 003 multi-tile-pipeline — single-tile design is growth-bound in
      principle (Tree's isolated growth 34,718 ticks is large), but the
      real average (9,551 ticks/harvest) is already handling-dominated
      once the reroll paradigm converges — recompute the real
      growth-vs-handling ratio before assuming multi-tile helps. Any
      design must space Tree tiles wide enough to avoid the 2.44x
      neighbor-growth-penalty, not just the companion-range
      self-collision margin.
- [ ] leader-gap — leader scores 9.6x faster (03:20.446 vs 002's
      31:59.849). Investigate before assuming multi-tile alone closes
      it — Hay's equivalent gap (exp 038-045) was never fully explained
      despite exhausting every mechanism-level hypothesis; flag the
      same risk here rather than re-litigating from scratch.

## Done

- [x] 001 mechanics-probe — free to plant, base yield 2,560, full
      multiplier 409,600 (160x), growth 34,718 ticks isolated, 2.44x
      neighbor-growth-penalty confirmed. `experiments/wood_single/001/result.md`
- [x] 002 finish-and-score — **adopted, first-ever score.** hay_single's
      champion paradigm transplanted directly (own_tile_ready() fix
      for the Grass-vs-Tree planting-table quirk). Real scored run:
      **31:59.849, Global Rank #232**, all 4 internal repeats crossed
      the target cleanly. `experiments/wood_single/002/result.md`
