# Hay_Single — experiment queue

Target: **100_000_000 hay** on an 8x8 farm with a single drone
Leader: **02:17.995** (confirmed on the in-game leaderboard, rank #1)
Entry point: `main` · Runner: `leaderboard_run(Leaderboards.Hay_Single, "main", 5000)`

Branches: `auto_experiment/hay_single/NNN` · Results: `experiments/hay_single/NNN/result.md`

## Where this stands after 001-003

- **001** (arithmetic): leader's pace needs ~686 ticks/harvest average;
  growth (~404 ticks) is not the bottleneck, so the schedulability floor is
  **1 hay tile**; closing the gap looked like it needed a ≥~75% companion
  skip rate.
- **002** (measured): confirmed 81,920 satisfied yield and the Carrot dead
  end, but found the *solo* skip-rate ceiling is **~25-30%**, not ≥75% — Hay's
  44-66% depended on neighbour drones (021's "contention is cooperation"),
  which a lone drone doesn't have. Measured steady state ≈1,300 ticks/harvest,
  **~3x slower than the leader** at full extrapolation.
- **003** (arithmetic): a dedicated wood income to unlock Carrot is dead —
  Tree.md's 5-wood yield against Carrot's 512-wood cost makes even the most
  generous floor ~20x over the whole run's tick budget.

**Every queued lever is now closed.** Per docs/LOOP.md's "Empty queue" rule,
before stopping: is there a fundamental fork left, not just another tweak?

## The one live fork: a solo drone with a cluster, not for idle-hiding but for cooperation-with-itself

001 ruled out multi-tile *for schedulability* (growth isn't the bottleneck,
so extra tiles only add movement with nothing to hide it behind — matches
Hay's 027/029). That argument is still correct on its own terms. But 002's
real finding reframes the bottleneck as **companion-type-match probability**,
not idle time, and there's a mechanism multi-tile could help *that* which
001 never considered: if 2+ grass tiles are placed close enough that their
wrapped-distance-3 companion zones **overlap**, then a real trip this drone
makes to satisfy tile A's companion can leave a plant standing that also
happens to satisfy a *later* request from tile B at the same position —
recreating Hay's 021 "contention is cooperation" effect with one drone
servicing several tiles instead of several drones servicing one each. This is
genuinely different from the schedulability question 001 answered, and
hasn't been tested.

It is not obviously a win: more tiles also means more total companion
requests to service, and 002's ~1,300-tick-a-harvest cost already has no
slack — extra movement between tiles is a real cost 027/029 already showed
can dominate. But it's the one candidate left that isn't a re-run of an
already-closed question, and 001's own arithmetic can bound it before a run:
compute the actual overlap fraction between two nearby tiles' 25-cell
companion balls (an 8x8 wrapped grid gives no room for two tiles to have
*disjoint* radius-3 balls — every pair of tiles' balls overlap substantially
on a board this small) before writing any code.

## Queued

- [ ] 004 overlap-arithmetic — before running anything: on the 8x8 wrapped
      grid, compute how much two grass tiles' companion balls overlap as a
      function of the distance between the tiles, and whether shared
      coverage can plausibly lift the ~25-30% solo hit rate enough to close
      even half the ~3x gap. If the arithmetic says no (e.g. overlap helps
      only marginally, or the extra per-tile companion traffic cancels the
      gain), that closes the queue for real and 005 is the point to report
      "tried everything, here's what's left" per docs/LOOP.md rather than
      inventing a fourth lever.
      Falsifier: if overlap-adjusted hit rate projects to less than, say,
      40%, this cannot plausibly close a 3x gap (would need close to 75%+
      averaged across a design that also pays more total movement) and 005
      should say the achievement is out of reach for a single-drone-optimal
      driver, then pivot to writing a *correct* (terminating, scored) driver
      at whatever pace this design achieves rather than continuing to chase
      the leader's time.

## Done

- [x] 001 mechanics-probe — computed the arithmetic floor.
      `experiments/hay_single/001/result.md`
- [x] 002 reactive-companion-probe — measured the real solo skip-rate
      ceiling (~25-30%) and confirmed 81,920/Carrot-dead-end.
      `experiments/hay_single/002/result.md`
- [x] 003 price-carrot-lever — rejected from the wiki alone: 5-wood trees
      can't fund 512-wood carrots within 20x of the tick budget.
      `experiments/hay_single/003/result.md`
