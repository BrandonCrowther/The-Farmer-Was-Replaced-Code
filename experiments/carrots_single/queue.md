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

- [ ] 003 single-tile-reactive-probe — build the direct analogue of
      hay_single's 007/008: single Carrot tile, skip Grass companions for
      free (checking `planted` only to catch positions this drone has
      itself overwritten), reactive skip-or-walk for Bush/Tree, revert a
      serviced position back to Grass after use to keep the free rate from
      eroding. Instrument real ticks/harvest and measure the real
      steady-state hit rate (should structurally exceed 1/3 given the free
      Grass third) before committing further.
      Falsifier: if own-tile handling turns out close to growth (~7,196),
      idle time is smaller than 001 suggests and multi-tile shouldn't be
      pursued — check this explicitly (analogous to hay_single's 001)
      before assuming.
- [ ] 004 (after 003) — if real idle time is confirmed large, design and
      test a multi-tile layout properly scheduled around it (the
      hay_single 015 / Hay 044 playbook: measure first, schedule around
      the *measured* window, verify a same-tile guard if tiles are close
      enough to risk self-collision).
- [ ] 005 (after 003/004) — real terminating driver, run to score. First
      recorded time for this category.

## Done

- [x] 001 mechanics-probe — starting stockpile, costs, growth ticks
      (~7,196 mean), companion distances (≤3, wrapped, confirmed),
      indirect evidence of free Grass satisfaction (3/3).
      `experiments/carrots_single/001/result.md`
- [x] 002 natural-grass-growth-check — **direct confirmation**: untouched
      grassland has standing Grass from tick ~2, not something that grows
      in. `experiments/carrots_single/002/result.md`
