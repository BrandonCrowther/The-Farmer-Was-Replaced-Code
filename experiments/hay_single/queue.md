# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Where this stands after 001-004 — the fork search is closed

- **001** (arithmetic): leader's pace needs ~686 ticks/harvest; growth isn't
  the bottleneck (1-tile schedulability floor).
- **002** (measured): solo skip rate ~25-30%, not the hoped ≥75%; steady
  state ~1,300 ticks/harvest, **~3x off the leader**.
- **003** (arithmetic): wood-funded Carrot is dead, ~20x over budget even at
  the most generous floor.
- **004** (arithmetic): clustering tiles for shared companion coverage has a
  **hard ceiling of 1/3 hit rate** (type-match probability, not position
  coverage — pre-planting can't beat 1-in-2 odds per already-stocked
  position, and Carrot is a permanent third). Best case ≈800 ticks/harvest —
  closer, but still ~17% over the 686 budget, before charging for the extra
  inter-tile movement a real cluster would add.

**No lever found closes the gap to 02:17.995.** Per docs/LOOP.md's bar for
an empty queue, that's genuinely checked now, not assumed — four different
angles (schedulability, reactive skip, an alternate resource path, and
shared-coverage clustering) all independently land short. **005 stops
chasing the record and instead builds the best design found (clustering) as
a real, correct, terminating driver** — worth having as a working scored
entry even though it won't be #1.

## Queued

- [ ] 005 clustered-driver — implement a small cluster of grass tiles (2-3,
      close together so their companion balls overlap heavily per 004's
      table) with the same reactive skip-and-remember approach as 002, run
      long enough to see the hit rate stabilize, and terminate on the real
      100,000,000 target this time (or run to a fixed large cycle count if
      that's a cleaner way to extrapolate first). Falsifier: if the
      clustered hit rate doesn't clearly beat 002's ~25-30%, clustering
      isn't worth its added movement overhead and the single-tile design
      from 002 is simpler and should be the one finished instead.
- [ ] 006 finish-and-score — once 005 (or 002's single-tile fallback) is
      picked, extend it to actually run to 100,000,000 and terminate, so
      hay_single has a real leaderboard time on record for the first time —
      correctness and a score matter even at ~2-3x off the leader.

## Done

- [x] 001 mechanics-probe. `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe. `experiments/hay_single/002/result.md`
- [x] 003 price-carrot-lever. `experiments/hay_single/003/result.md`
- [x] 004 overlap-arithmetic — closes the fork search; no lever found beats
      the leader, clustering is the best of what's left.
      `experiments/hay_single/004/result.md`
