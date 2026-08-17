# Carrots_Single — experiment queue

Target: **100_000_000 carrots** on an 8x8 farm with a single drone
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Carrots_Single, "main", 5000)`

Branches: `auto_experiment/carrots_single/NNN` · Results: `experiments/carrots_single/NNN/result.md`

## Two findings from 001/002 that shape the whole design

- **Free money, no bootstrapping.** Starts with 1,000,000,000 Hay and
  1,000,000,000 Wood — Carrot costs 512 of each to plant, and even ~1,221
  plantings (the full run) need ~625k of each. Resource cost is a
  complete non-issue; only ticks matter, same as hay_single.
- **Free Grass companions.** Untouched grassland already has standing
  Grass on it from tick ~2 (002, directly confirmed, not something that
  grows in over time). A plant's companion is Grass, Bush, or Tree
  (never itself — Polyculture.md), uniform ~1/3 each. **The Grass third is
  satisfied for free, always, at any position this drone hasn't
  overwritten** — a structural floor no reroll or memory design gave
  hay_single, which had to earn its ~1/3 hit rate the hard way (011).
- **Growth is slow — ~7,196 ticks mean (001), ~17.8x hay_single's Grass
  (~404).** Own-tile handling (harvest 200 + till-if-needed + plant 200,
  Carrot needs Soil so till is likely needed every cycle unlike Grass) is
  almost certainly much smaller than growth, meaning **this category is
  growth-bound, not servicing-bound** — the opposite of hay_single (001,
  zero idle time) and unlike Hay (idle time real but too small for a
  second tile, 041/044). A large idle window here could make multi-tile
  genuinely pay off for the first time tonight.

## Queued

- [x] 003 reactive-single-tile — **adopted, after fixing two real bugs**
      (forgot to water at all in r1; `plant()` doesn't overwrite an
      existing entity so a revisited reverted-to-Grass position needs
      `harvest()` first, r2 lost the multiplier on 2/40 for this). Fixed
      (r3): **40/40 harvests multiplied, 100%.** ~71% of the ~8,362-tick
      average cycle is idle wait — this category is growth-bound.
      Projects ≈9.80 carrots/tick, ≈28.0 minutes for the full target.
      Handling cost (~2,422 ticks) vs growth (~7,196) implies **~3 tiles
      could nearly perfectly pipeline**. `experiments/carrots_single/003/result.md`.
- [x] 004 multi-tile-pipeline — **adopted, a large win.** 3 tiles at
      (0,0)/(0,4)/(2,2), pairwise wrapped distance 4 (self-collision
      impossible by construction, `HITS_GUARD` 0/60 confirmed). Real
      **3,430.43 ticks/harvest** vs 003's 8,362 — **2.44x throughput**,
      close to the model's ≈3,222 prediction. Projects ≈11.5 minutes for
      the full target (down from ≈28.0). `experiments/carrots_single/004/result.md`.
- [x] 005 finish-and-score — **adopted, first-ever score.** Real 3-tile
      terminating driver, real scored run: **11:54.303, Global Rank
      #118**, 100% multiplier rate (0 lost hits over the full ~1,221-cycle
      run). ~3.5% above 004's ≈690s projection (likely a full-run vs.
      60-cycle-sample averaging difference, not a bug).
      `experiments/carrots_single/005/result.md`.
- [x] 006 reroll-before-walk (single tile) — **adopted the technique,
      after fixing a real bug** (Grass-companion draws on a position this
      drone had already converted to Bush/Tree via a walk were wrongly
      treated as still-free — the no-revert memory pattern needs to gate
      the Grass case on the memory dict too). Fixed: 40/40 multiplied,
      handling (idle subtracted) drops from 003's ~2,422 to **~1,571**
      ticks/visit, a 35% cut — invisible on a single tile (still
      growth-bound) but sets up 007. `experiments/carrots_single/006/result.md`.
- [x] 007 5-tile reroll pipeline — **adopted, a large win**, after fixing
      a second real bug (reroll timing: must resolve the companion
      *immediately* at plant time, in the same visit, before moving to
      the next tile — checking it a lap later throws away a full growth
      cycle on a miss). Fixed: **2,370.29 ticks/harvest** vs 004's
      3,430.43 — **1.45x throughput**, ≈42.2 carrots/tick, matching the
      handling(1,571)+commute(≈800)≈2,371 model almost exactly. Idle
      effectively eliminated (`COMMUTE_AND_WAIT_TICKS` ≈1052 nearly
      every cycle). `experiments/carrots_single/007/result.md`.

## Done

- [x] 001 mechanics-probe — starting stockpile, costs, growth ticks
      (~7,196 mean), companion distances (≤3, wrapped, confirmed),
      indirect evidence of free Grass satisfaction (3/3).
      `experiments/carrots_single/001/result.md`
- [x] 004 multi-tile-pipeline — adopted, 2.44x throughput.
      `experiments/carrots_single/004/result.md`
- [x] 002 natural-grass-growth-check — **direct confirmation**: untouched
      grassland has standing Grass from tick ~2, not something that grows
      in. `experiments/carrots_single/002/result.md`
- [x] 003 reactive-single-tile — adopted, 100% multiplier rate, ~71% idle.
      `experiments/carrots_single/003/result.md`
- [x] 005 finish-and-score — adopted, first score 11:54.303, #118.
      `experiments/carrots_single/005/result.md`
- [x] 006 reroll-before-walk — adopted, handling cut 35% (single tile,
      invisible until combined with multi-tile). `experiments/carrots_single/006/result.md`
- [x] 007 5-tile reroll pipeline — adopted, 2,370.29 ticks/harvest, 1.45x
      over 004. `experiments/carrots_single/007/result.md`
