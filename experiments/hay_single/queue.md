# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Where this stands after 001-006 — multi-tile is closed, for three independent reasons

- **001**: no idle time to hide behind (schedulability floor is 1 tile).
- **005**: useful overlap distances (≤3) let a tile's own coordinate be
  named as another tile's companion target — self-collision, self-healing
  but costly.
- **006**: safe distances (>3) avoid the collision but pay a flat commute
  tax (~800 ticks *every* cycle just to shuttle between tiles) that exceeds
  any companion-sharing benefit — measured throughput was *lower* than
  single-tile despite a better hit rate.

**Multi-tile is closed.** Single tile (002's design) is the right shape;
what's left is refining *it*.

## Correction to 003 (flag, don't silently leave standing)

003 concluded Carrot is permanently unaffordable (no wood source). 006 found
this is only true for a **short/cold run**: `Common.polyculture_mapped`-style
service logic harvests a companion tile before replanting it whenever the
stocked type no longer matches a fresh request, and once a standing
Bush/Tree companion has had real time to mature, that harvest yields real
wood. In 006's 90-cycle run, wood reached 573,952 and nearly every request
(Carrot included) was satisfiable from cycle ~22 on. 002's own 60-cycle probe
never ran long enough to see this (`WOOD` stayed 0 throughout). **003's
"dead forever" claim is wrong for the ~1,221-harvest run this category
actually needs** — it was priced for a *deliberately farmed* wood tile on a
cold start, not incidental wood from companion churn over a long run.

## Queued

- [ ] 007 single-tile-long-run — rerun 002's exact single-tile design (not
      the cluster) for ~150-200 cycles instead of 60, to see (a) whether wood
      accumulates there too and Carrot starts clearing at the same ~cycle-20
      mark, and (b) what steady-state ticks/harvest and hit rate look like
      once that happens — this is now the best candidate for "the real
      achievable pace," not the ~1,300-tick number 002 measured before wood
      kicked in anywhere.
      Falsifier: if wood never accumulates on a *single* tile the way it did
      across two (006's mismatches may have been more frequent simply from
      having 2x the distinct companion positions in play), say so — the
      mechanism might need enough tile-visits or enough distinct stocked
      positions to fire at all, not just enough time.
- [ ] 008 finish-and-score — once 007 settles the real steady-state number,
      extend the winning single-tile design to terminate on the actual
      100,000,000 target and run it for a real recorded time.

## Done

- [x] 001 mechanics-probe. `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe. `experiments/hay_single/002/result.md`
- [x] 003 price-carrot-lever — **corrected by 006**: true only for a
      short/cold run, not the full run. `experiments/hay_single/003/result.md`
- [x] 004 overlap-arithmetic. `experiments/hay_single/004/result.md`
- [x] 005 clustered-probe (distance 2) — self-collision bug found.
      `experiments/hay_single/005/result.md`
- [x] 006 clustered-v2 (distance 4) — bug fixed, but commute tax makes
      multi-tile strictly worse than single-tile; also found wood
      accumulates given enough run length, correcting 003.
      `experiments/hay_single/006/result.md`
