# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## The floor — 001's arithmetic, corrected by 002's measurement

001 computed a floor from arithmetic: ≈686 ticks/harvest budget, growth is not
the bottleneck (schedulability floor = 1 tile), and a ≥~75% companion-skip
rate would close the gap via a "monocrop-stock" pre-planted ring. 002 built
and ran exactly that and found the ceiling is real but much lower than hoped:

- **81,920 satisfied-harvest yield: confirmed.**
- **Carrot: 1/3 of requests, permanently unaffordable (needs 512 wood; nothing
  in this design ever produces wood) — confirmed, 0/19 satisfied.**
- **Solo-drone skip rate settles near 25-30%, not ≥75%.** Hay's 44-66% relied
  on neighbour drones incidentally pre-stocking each other's tiles (021) —
  hay_single has no neighbours. No static stock beats ~1/3 per position
  because each of the ~24 reachable positions gets an independent fresh type
  draw on every visit; more pre-planting cannot raise a per-visit match
  probability that low-level.
- **Measured steady-state: ≈1,300 ticks/harvest, ~1.9-2x over budget.**
  Extrapolated finish ≈6:59, **~3x slower than the leader.** Full numbers in
  `experiments/hay_single/002/result.md`.

**So the companion-servicing-efficiency lever is close to exhausted at ~3x
short — tuning the skip rate further cannot close a gap that size.** The next
question is not "how do we service companions faster" but "is there a lever
outside companion-servicing at all," and if not, whether ~3x off the world
#1 is where this category actually settles for a first working driver.

## Queued

- [ ] 003 price-the-carrot-lever — the single largest number on the table:
      1/3 of requests currently score 512 instead of 81,920. Price a
      dedicated wood income (grow one off-tile Tree purely for wood,
      amortized) against how much drone-time it costs versus how often it
      then lets a Carrot request clear at full multiplier. A cheap
      *arithmetic* pass first (ticks to grow+harvest one Tree for wood vs.
      512 wood cost vs. 1/3-of-passes frequency) before spending a run —
      002's harvest()-destroys-unripe finding was settled this way and it
      held.
      Falsifier: if the wood-tile's own amortized tick cost, spread over the
      Carrot requests it unlocks, exceeds the ~163,840 hay/harvest gain
      (81,920 - 512) it buys, the lever is a net loss and 004 should look
      elsewhere (e.g. whether *any* single-drone hay_single driver design can
      beat ~3x off the leader, or whether the achievement is simply farmed
      for correctness — a working, terminating driver — rather than pace).
- [ ] 004 (placeholder) — whatever 003 leaves open, or the fundamental-fork
      question if 003 closes this line (docs/LOOP.md, "Empty queue").

## Done

- [x] 001 mechanics-probe — growth ticks (404 mean), tick rate (~6,070/s),
      wrapped companion distance (confirmed ≤3), op costs (confirmed 200),
      bare yield (confirmed 512). Computed the arithmetic floor.
      `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe — confirmed 81,920 and the Carrot dead end;
      **overturned** 001's ≥75%-skip-rate design (solo ceiling is ~25-30%).
      Measured ~3x off the leader's pace at steady state.
      `experiments/hay_single/002/result.md`
