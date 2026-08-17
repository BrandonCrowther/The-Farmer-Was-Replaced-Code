# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Where this stands after 001-005

- **001** (arithmetic): ~686 ticks/harvest budget; growth isn't the
  bottleneck (1-tile schedulability floor).
- **002** (measured): solo skip rate ~25-30%; steady state ~1,300
  ticks/harvest, **~3x off the leader**.
- **003** (arithmetic): wood-funded Carrot is dead (~20x over budget).
- **004** (arithmetic): clustering's hit-rate ceiling is ~1/3; best case
  ≈800 ticks/harvest, still short of 686 — closes the fork search on paper.
- **005** (measured): tried distance-2 clustering and found a bug 004's
  arithmetic couldn't see — **companion requests can name another farm
  tile's own coordinates**, and an unguarded satisfy overwrites it (harvest +
  replant as Bush/Tree), corrupting the farm for one cycle before it
  self-heals. Overlap tight enough for sharing (≤3 apart) is *exactly* tight
  enough for this collision (a tile's own coordinate always sits inside
  another tile's ball once they're within distance 3 of each other) — the
  two can't be separated by tuning distance downward, only avoided by
  keeping distance **> 3**. `experiments/hay_single/005/result.md`.

## Queued

- [ ] 006 clustered-driver-v2 — retry 005's design at **distance 4** (still
      41.7% ball overlap per 004's table, but *outside* every tile's own
      companion range, so no tile's coordinate can ever be a valid target for
      another's request — removes 005's bug by construction, not by adding a
      guard). Same instrumentation as 002/005: hit rate, ticks/harvest,
      compare cleanly against 002's ~1,300 baseline this time.
      Falsifier: if hit rate doesn't clearly beat 002 once the collision bug
      is gone, clustering earns nothing over the simpler single-tile design
      and 007 should finish *that* one instead.
- [ ] 007 finish-and-score — take whichever design (006's cluster or 002's
      single tile) wins on ticks/harvest, extend it to actually terminate on
      the real 100,000,000 target, and run it to completion so hay_single has
      a real recorded time for the first time. Correctness and a score matter
      even at ~2-3x off the leader — see 004's closing verdict on why chasing
      02:17.995 further isn't the goal anymore.

## Done

- [x] 001 mechanics-probe. `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe. `experiments/hay_single/002/result.md`
- [x] 003 price-carrot-lever. `experiments/hay_single/003/result.md`
- [x] 004 overlap-arithmetic. `experiments/hay_single/004/result.md`
- [x] 005 clustered-probe — found and diagnosed the self-collision bug in
      distance-2 clustering; self-healing but costly. Points 006 at
      distance-4 spacing instead. `experiments/hay_single/005/result.md`
